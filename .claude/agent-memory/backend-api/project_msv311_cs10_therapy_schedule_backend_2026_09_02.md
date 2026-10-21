---
name: project-msv311-cs10-therapy-schedule-backend-2026-09-02
description: MSV3.11 CS-10 backend fix -- frequency-only PUT wiped recurring entries (root cause, mirrors CS-02), custom-interval-only mode invisible to self-heal/should_generate_for_therapy_day, DST-unsafe weekly/biweekly computation fixed, next_session_at/timezone added to GET/PUT contract
metadata:
  type: project
---

## What happened
Grace's "no upcoming sessions scheduled" complaint (MSV3.11 spec) + fresh
`database-administrator` prod pull (`db-reports/2026-09-02-msv311-prod-evidence.md`)
arrived mid-task via coordinator message and reframed the diagnosis: her row had
`therapy_frequency='biweekly'` PERSISTED but `therapy_schedule`/`next_session_date`/
`custom_therapy_sessions` all empty -- the frequency reached the DB, the entries
did not. Population-wide: only 12/1810 users have ANY persisted schedule; 7 more
have a real schedule but `next_session_date` stuck NULL.

## Root causes found (code trace, not guesswork) -- all fixed except the flagged one
1. **`crud.update_therapy_schedule` unconditionally overwrote `therapy_schedule`
   on every PUT**, no guard at all (unlike `custom_therapy_sessions`, which already
   had a clear-guard from CS-02/7dddf38). Flutter's `SettingsCubit.updateTherapyFrequency`
   resends `current.therapySchedule` (in-memory, hydrated from SharedPreferences,
   NOT from a backend GET) on every frequency toggle -- if that local cache is
   stale/empty, the toggle silently wipes a real schedule. **Fix**: made
   `TherapyScheduleUpdate.schedule` Optional (was required) -- omitting it (or
   JSON `null`) now means "leave entries untouched," mirroring `custom_sessions`'
   existing None-means-untouched semantics exactly. `crud.update_therapy_schedule`'s
   `schedule_json` param is now `Optional[str]`, only assigns when not None.
   Endpoint response echoes back the ACTUALLY-persisted schedule (parsed from
   `prefs.therapy_schedule`) when the request omitted it, never the request's None.
2. **`get_therapy_schedule_with_frequency`'s recompute/self-heal guard was
   `if schedule or custom_sessions:`** -- False for a purely interval-based custom
   schedule (frequency=custom, custom_interval_days set, no recurring entries, no
   custom_sessions -- a legitimate config per `TherapyScheduleUpdate`'s own
   validator). Fix: removed the guard, always recompute (the compute function
   already returns None cheaply/safely when there's nothing to compute) and
   ALWAYS sync the persisted column to the recomputed value (including collapsing
   to None when every known session has passed with nothing to replace it --
   the "custom sessions in the past" staleness case).
3. **Same class of bug in `should_generate_for_therapy_day`**: `if not schedule:
   return Sunday fallback` ran BEFORE the `frequency == "custom"` branch, so every
   custom-interval-only user was treated as "no schedule at all." Fix: moved the
   `frequency == "custom"` branch to run FIRST, before the `parse_schedule`/empty
   check.
4. **DST-unsafe weekly/biweekly computation** (found while writing the mandatory
   DST tests, not initially expected): `_next_weekly_occurrence`/`_last_weekly_
   occurrence` built candidates via `now_local.replace(hour=..) + timedelta(days=N)`
   -- for a pytz zone this keeps whatever fixed UTC offset was correct for
   `now_local`'s OWN date, wrong by the DST delta once the target date crosses a
   transition (confirmed: a Sunday-6-days-out weekly occurrence across Poland's
   2026-03-29 spring-forward resolved to 17:00 UTC instead of the correct 16:00
   UTC). Fix: new `_localize_naive(tzinfo, naive_dt)` helper -- builds a naive
   datetime for the exact target date/time and calls the pytz zone's own
   `.localize()` fresh (only zones with `.localize` get this treatment;
   stdlib/zoneinfo tzinfo falls through to a plain `.replace(tzinfo=...)`, which
   is already correct for those). `_is_on_week` (biweekly parity) was NEVER
   affected -- it only ever compares `.date()` deltas, no tzinfo arithmetic.
   `_compute_next_from_custom_sessions`/`_compute_last_from_custom_sessions`
   (one-off calendar sessions) were also never affected -- they already built
   fresh naive datetimes and localized per-call.
5. **Contract addition**: GET/PUT `TherapyScheduleResponse` gained `next_session_at`
   (explicit alias, identical instant to `next_session_date`, kept for clarity/
   future migration off the older name) and `next_session_timezone` (IANA name,
   e.g. "Europe/Warsaw") so Flutter can render date+time+zone without doing its
   own tz math. Purely additive.

## The "7 users with schedule but NULL next_session_date" population -- explained, not a new bug
Traced (not guessed): `UsersManager.getTherapySchedule()` (the Dio wrapper for
`GET /api/v1/users/therapy-schedule`) exists in `lib/api/api_managers/users_manager.dart`
but is **called nowhere in the Flutter codebase** (grepped `lib/`, zero hits besides
its own definition). The self-heal-on-read logic in `get_therapy_schedule_with_
frequency` (added in an earlier session, "Fix.1.1 CS-09 bug #4" / post-release-review
task 3a) is and was already correct -- it has simply never had an opportunity to run
in production, because nothing calls GET. This is not a computation bug to fix, it's
a "the fix exists but is dead code until Flutter wires up the tile" situation. Once
`flutter-mobile` switches `main_tab_cubit.dart::_computeNextSession` to consume this
GET contract, the self-heal will fire naturally for every affected user on their next
app open. Worth remembering: **a "self-heal on read" fix is only as good as its read
path actually being called** -- always grep the consumer side, not just verify the
producer-side logic is correct.

## What Flutter must send (precise spec for the FE follow-up agent)
Any call site whose PRIMARY purpose is NOT editing recurring entries must **omit**
`schedule` from the PUT body entirely (not send `[]`, not resend `current.
therapySchedule`):
- `SettingsCubit.updateTherapyFrequency` (frequency-only toggle)
- `SettingsCubit.updateCustomIntervalDays` (interval-only change)
- `SettingsCubit.addCustomSession`/`removeCustomSession` (these currently ALSO
  resend `current.therapySchedule` alongside a custom-session edit -- same risk,
  not just the frequency toggle the coordinator originally named)
Only `SettingsCubit.addTherapySession`/`removeTherapySession` (the actual
recurring-schedule editor) should send a real `schedule` list -- including an
explicit `[]` for a deliberate "remove my last entry" action, which the backend
still honors as a genuine clear (only *omitting* the field means untouched).

## Confirmed NOT fixed (flagged, out of file-ownership scope for this task)
Same bug pattern ("empty schedule/entries treated as no-schedule-at-all") also
found live in two files NOT in this task's declared FILES set:
- `app/api/v1/endpoints/therapy_tracking.py` line ~263, `/session-state` endpoint:
  `if not schedule and not custom_sessions: return "no_therapy_set"` -- same
  custom-interval-only blind spot, feeds the Main-tab CTA state machine.
- `app/services/notification_service.py` `_process_first_nudges` (~line 583):
  `if not schedule: continue` bails BEFORE the frequency=="custom" branch, AND
  the custom branch itself does `entry_for_custom = matched_custom if matched_custom
  else schedule[0]` -- would `IndexError` crash for a custom-interval-only or
  calendar-only user with zero recurring entries, not just silently skip them.
  Riskier / more invasive to fix blind; deliberately left for a dedicated
  follow-up rather than rushed under this task's time box.
Ownership note: `app/api/v1/endpoints/` is only partially carved up in CLAUDE.md
(users.py/conversations.py/gamification.py are explicitly backend-api's;
analytics.py/summaries.py/dashboard.py are data-analytics'). `therapy_tracking.py`
and `notification_service.py` fall in the ambiguous middle -- flagged to the lead
rather than edited outside the task's explicit FILES list.

## Test/verification notes specific to this task
- New test file section in `test_therapy_frequency.py` (not a new file -- this file
  already has an extensive, well-organized suite for this exact domain with a
  reusable `_make_test_app()` / `_tz_dt()` / `TestCRUDTherapySchedule._make_db_and_prefs()`
  convention; extended it rather than duplicating).
- **Gotcha confirmed again**: adding a new field read from a MagicMock(spec=Model)
  fixture that was never explicitly set (`prefs.time_zone`) broke 3 previously-green
  PUT endpoint tests -- Pydantic tried to coerce the raw MagicMock into
  `Optional[str]` and failed validation. Fixed by adding `fake_prefs.time_zone = "UTC"`
  to those fixtures, per the established "explicitly set ALL fields touched by new
  code" rule in Test Patterns (MEMORY.md) -- reconfirmed, third occurrence of this
  exact class of break this project.
- DST test values were NOT hand-derived and trusted blind -- verified computationally
  with a standalone `python -c` script against the actual (pre-edit and post-edit)
  module before writing assertions, specifically because DST offset arithmetic is
  exactly the kind of thing that's easy to get backwards by one hour on paper.
- Full suite: 22 failed, 5539 passed. 21 match the established baseline (see
  Test Patterns in MEMORY.md); the 22nd (`test_notification_worker_registration.py::
  test_importing_job_module_alone_registers_everything`) is a NEW name not seen in
  prior baseline snapshots, but confirmed order-dependent/leftover-state noise by
  running it (a) alone and (b) as its whole file, both green, both before AND after
  this change via `git stash`. Not a regression.

## Commit
Branch `msv3.11-cs10` (worktree `wt-be-cs10`), commit `5f7211b`, NOT pushed.
No migration.
