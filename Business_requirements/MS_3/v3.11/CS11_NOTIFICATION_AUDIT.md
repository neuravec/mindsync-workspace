# CS-11 Notification Audit — MSV3.11 (post-CS-10 pass)

**Author:** backend-api · **Date:** 2026-09-02 · **Spec:** MSV3.11 CS-11 (Change Spec, Grace)

Format mirrors `Business_requirements/MS_3/v3.22/CS01_NOTIFICATION_AUDIT.md`
(the MSV3.2.2 audit). This round re-analyzes the trigger logic of every
notification type after CS-10 (therapy-schedule end-to-end fix, this branch's
base commit `5f7211b`), per the spec's instruction to run CS-11 after CS-10
"since the schedule fix changes what several generators see." Prod evidence
cited throughout is `db-reports/2026-09-02-msv311-prod-evidence.md` section E
(14-day volume by type/status/day) and section B (schedule population), both
pulled fresh for this task, plus `analytics-reports/2026-08-16-post-release-review-12-08.md`
(prior audit that introduced `CooldownGiveUpThrottle`).

## Answers to the three spec questions

1. **Do any types overlap / fire together without reason?**
   No *undocumented* overlap was found. Two documented-by-design overlap
   patterns exist and are called out per-row below: (a) THERAPY_APPOINTMENT +
   THERAPY_PREP fire in the same T-24h/T-3h windows for the same session —
   intentional, two different CTAs (agenda vs. prep). (b) Pass 3
   (deterministic pipeline) has **no cross-type daily cap by design** (see
   `notification_orchestrator.py` module docstring, "Pass 3 ... bypasses ...
   the daily cap ... entirely") — up to 6 Pass-3 types could in theory all
   fire for the same user in the same 18:00-local hour (worst case: Sunday,
   ADD_THERAPY_DATE + BETWEEN_SESSIONS_NOTE + HOMEWORK_REMINDER +
   MOOD_UPDATE_REQUEST + REFLECTION_INVITATION + THERAPY_RELATIONSHIP_CHECKIN
   all independently eligible). This is flagged as **SUSPECT / worth
   Darek's attention** but **not fixed** here — it is an explicit
   architectural choice (each row independently toggleable, "deterministic"
   was the point), not something the audit found evidence is actually
   happening at volume, and changing it is a product decision beyond "fix
   the cycle."

2. **Does each type trigger for the right feature at the right time?**
   One systemic **DEFECT**, found and **FIXED** in this round: 6 of the 13
   generators (all schedule-anchored Pass 2/Pass 3 types) plus the
   `/session-state` endpoint's `no_therapy_set` guard bailed out on
   `if not schedule and not custom_sessions` — true for a **third legitimate
   schedule shape** (`frequency=="custom"` with only `custom_interval_days`
   set, no recurring entries, no calendar-picked sessions) that the CS-18
   fix's comment explicitly did not anticipate. See "Custom-interval-only
   defect" below. One smaller, related **DEFECT** also fixed: HOMEWORK_REMINDER's
   "any open homework" check bypassed the CS-07 repeating-to-do self-heal.

3. **Are the daily and weekly cycles of all notifications correct?**
   One confirmed **DEFECT**, **FIXED**: REFLECTION_INVITATION and
   THERAPY_RELATIONSHIP_CHECKIN had no give-up mechanism — prod evidence
   (fresh pull) confirms both reach ~1805-1806/1835 users almost every week
   and expire un-acted-on 99.97% of the time (1 ACTED out of ~3371-3373 in
   14 days each). Two **SUSPECT** findings **PARKED** (see table): the
   WEEKLY_SUMMARY_READY / MONTHLY_SUMMARY_READY SENT-rate anomaly, and the
   14-day volume's 4 burst days (85% of total).

## Reach note (applies to every row below)

Only **139 of 1835 users (7.6%)** have a registered FCM token (prod,
`db-reports/2026-09-02-msv311-prod-evidence.md` §E) — down from 13.4% at the
2026-07-03 audit. Every type below also has an in-app pull surface
(`GET /moments/upcoming`), so a "sent" moment is not necessarily unseen —
but push reach specifically is capped at ~7.6% of the base regardless of
generator logic. Not a cycle defect; noted once here rather than repeated
per row.

---

## A. The 13-row deterministic/schedule-driven set + CS-07 system nudge

| # | Type | Trigger predicate (file:line) | Timing | Toggle | Dedup / cap / cooldown | Cycle verdict | Overlap verdict | Action |
|---|---|---|---|---|---|---|---|---|
| 1 | `THERAPY_APPOINTMENT` | `is_eligible` — next session known (`therapy_appointment_generator.py:~165-215`, `_compute_next_session`) | T-24h and T-3h before session start (Pass 2) | `therapy_appointment` | dedup per (session datetime, slot) | Was **DEFECT** (custom-interval-only users invisible) → **FIXED** (removed the CS-18 bail-out guard at line ~212; compute_next_session_date already handles empty entries/custom_sessions safely) | Fires alongside row 4 in the same windows — **documented intent**, two distinct CTAs | Fixed this round |
| 2 | `ADD_THERAPY_DATE` | `is_eligible` — no next session known + `has_no_push_target`/`is_throttled` gates (`add_therapy_date_generator.py:167-183`) | Daily at 18:00 local (Pass 3) | `add_therapy_date` | 1/local-day dedup (defensive); real cadence = 7d cooldown + 3-unengaged give-up (`CooldownGiveUpThrottle`, already landed 2026-08-16, commit `de8d538`) | **CORRECT** — confirmed holding: 0 false pushes since the v544 fix for the 13 users who now have a real schedule (DBA §B) | Mutually exclusive with rows 1/4/6/7/5 (all require a *known* session; this row requires the opposite) — correct by construction | No change needed |
| 3 | `POST_SESSION_REFLECTION` | `is_eligible` — session ended in last ~26h lookback, no debrief yet, no existing moment (`post_session_reflection_generator.py:~158-227`, `_compute_last_session`) | Fixed 75 min after session start (Pass 2) | `after_therapy` | dedup per session/debrief id | Was **DEFECT** (custom-interval-only invisible via `_compute_last_session`'s identical bail-out guard) → **FIXED** | No trigger overlap (fires only after a session has already started/ended) | Fixed this round |
| 4 | `THERAPY_PREP` | `is_eligible` — next session known, no completed prep card (`therapy_prep_generator.py:~148-226`) | T-24h and T-3h (Pass 2) | `prepare_for_therapy` | dedup per (session datetime, slot) | Was **DEFECT** (same custom-interval-only bail-out) → **FIXED** | With row 1 — documented intent | Fixed this round |
| 5 | `BETWEEN_SESSIONS_NOTE` | `is_eligible` — debrief done for last session, next session **>3 days** away, no note this cycle (`between_sessions_note_generator.py:100-124`, `_compute_schedule`) | Daily 18:00 local while window active (Pass 3) | `between_sessions` | 1/local-day dedup; real stop condition = note added or window closing (self-limiting, no give-up needed) | Was **DEFECT** (custom-interval-only invisible in `_compute_schedule`) → **FIXED**; otherwise **CORRECT** | Mutually exclusive with row 7 by construction (`>3` vs `==3` days-to-next — never both true) | Fixed this round |
| 6 | `RECORD_SESSION` | `is_eligible` — next session known (`record_session_generator.py:~180-232`) | ~8 min before start, delivered in [-8,-3] min window + clamp-to-now exception (Pass 2) | `record_session` | dedup per session occurrence | Was **DEFECT** (custom-interval-only invisible) → **FIXED** | With rows 1/4 near session start — documented intent (different angle: record vs. agenda vs. prep) | Fixed this round |
| 7 | `HOMEWORK_REMINDER` | `is_eligible` — next session known AND ≥1 open therapist-origin to-do, exactly 3 days before session (`homework_reminder_generator.py:92-113`) | 18:00 local, day = session_date − 3 (Pass 3) | `homework` | dedup per (user, session local date) | Was **DEFECT ×2**: (a) custom-interval-only invisible → **FIXED**; (b) `_has_open_homework` bypassed the CS-07 repeating-to-do self-heal (a repeating homework item that rolled into a new period but hadn't been read in-app yet still looked DONE) → **FIXED** (now calls `ws_crud.sweep_repeating_todos` first, matching every other read path) | Mutually exclusive with row 2 (session known vs not) and row 5 (`==3` vs `>3` days) | Fixed this round — see also CS-08 sanity check below |
| 8 | `MOOD_UPDATE_REQUEST` | `is_eligible` — no `SymptomScore` in ≥3 days, rolling (`mood_update_request_generator.py:112-132`) | 18:00 local, rolling 3-day renotify (day 3, 6, 9, ...) (Pass 3) | `mood_trends` | self-healing anchor on `last_entry_at`; `sent_count` resets to 0 the moment the user logs a new entry | **CORRECT** — verified the anchor/reset logic is sound, no give-up needed since it naturally stops the instant tracking resumes | Independent of session state; may coincide with other Pass-3 rows on the same day — see the Pass-3-stacking finding (Q1) | No change |
| 9 | `REFLECTION_INVITATION` | `is_eligible` — no REFLECT conversation this Mon–Sun week (`reflection_invitation_generator.py:79-95`) | Sunday 18:00 local (Pass 3) | `reflect` | dedup per ISO week; **was** no cooldown/give-up | Was **DEFECT** ("iterate every user, ~99.97% expire unsent" — DBA §E: 1 ACTED / ~3371 in 14d, 1805/1835 users reached) → **FIXED**: adopted `CooldownGiveUpThrottle` (`give_up_after_unengaged=3`, `cooldown_days=7`, deliberately **not** `has_no_push_target` — see reasoning in the generator's module docstring) | With row 11 (same Sunday/hour) — both independently toggleable, different features, not flagged as wrong; documented as intentional stacking | Fixed this round |
| 10 | `GOALS_WEEKLY` | Event-hooked — weekly goal-narrative regen completes, `trigger_source="weekly_scheduled"` (`moment_hooks.py:161-215`) | Event-anchored + night rule (21:00–08:00 → push to 08:00) | `goals` | dedup per ISO week | **CORRECT** — event-anchored, fires once/week per user by construction | Independent event; may coincide with Pass-3 same-day rows | No change |
| 11 | `THERAPY_RELATIONSHIP_CHECKIN` | `is_eligible` — no `TherapyHealthCheck` this Mon–Sun week (`therapy_relationship_checkin_generator.py:103-117`) | Sunday 18:00 local (Pass 3) | `therapy_relationship` | dedup per ISO week; **was** no cooldown/give-up | Was **DEFECT** — identical shape to row 9 (DBA §E: 1 ACTED / ~3373 in 14d, 1806/1835 users) → **FIXED**: same `CooldownGiveUpThrottle` treatment | With row 9 — see above | Fixed this round |
| 12 | `WEEKLY_SUMMARY_READY` | Event-hooked — `WeeklyTherapySummary` card created (`moment_hooks.py:223-280`) | Event-anchored + night rule | `weekly_summary` | dedup per (user, summary_id) | **SUSPECT** — only 1811/5407 (33.5%) of 14d volume reaches SENT, rest EXPIRE (DBA §E). **PARKED**: DBA explicitly flags this ratio as unreliable pending job-log tracing (4 burst days = 85% of 14d total volume distort any per-day average); plausible innocent explanation is the 7.6% token-coverage ceiling, but that is not confirmed from data alone, and root-causing the specific job(s) behind the burst days is outside this audit's reach | Independent event | Parked — see "Items parked for Darek" below |
| 13 | `MONTHLY_SUMMARY_READY` | Event-hooked — `MonthlyTherapyAudit` created (`moment_hooks.py:288-343`) | Event-anchored + night rule | `monthly_summary` | dedup per (user, audit_id) | **SUSPECT** — 1807/3555 (50.8%) SENT rate. **PARKED**, same reasoning as row 12 | Independent event | Parked |
| CS-07 | `ACCOUNT_SETUP_NUDGE` | `is_eligible` — account created, no `UserGoal` yet (`account_setup_nudge_generator.py:75-88`) | t+24/48/72/96h, up to 4 touches, only-future rule (Pass 3) | none (system, master toggle only) | hard cap of 4 touches, dedup per touch index | **CORRECT** — clean cap, clean stop condition (any goal ends the series) | Independent trigger (account age × goal absence) | No change |

## B. Pass 1 (scored) survivors

| Type | Trigger | Timing | Cap/cooldown | Cycle verdict | Overlap verdict | Action |
|---|---|---|---|---|---|---|
| `MOOD_DIP_ALERT` | Negative-category symptom, 3 consecutive scores ≥7 (severe ≥9 suppressed) (`mood_dip_alert_generator.py:79-`) | now+1h delivery; Pass 1 slot-gated (≤1/slot, 2/day flat cap shared with RE_ENGAGEMENT) | 5-day anti-spam per symptom | **CORRECT** | Competes with RE_ENGAGEMENT for the same Pass-1 slot by score — documented, correct | No change |
| `RE_ENGAGEMENT` | 3+/7+ days inactive | now+2h delivery; Pass 1 slot-gated | Max 2 sends per inactivity window, resets on any activity | **CORRECT** | Same slot competition as above | No change |

## C. Historical-only / dead code (unchanged from the 2026-07-24 audit, re-confirmed live)

- `SESSION_MORNING_OF`: enum member retired, no generator produces it. Confirmed unchanged.
- `notify_summary_notification`, `_process_first_nudges`, `_process_followup_nudges`
  (`app/services/notification_service.py`): **CS-10 leftover (b), resolved.**
  Re-grepped for this task: `_process_first_nudges`/`_process_followup_nudges`
  have **zero callers anywhere in `app/`** outside their own definitions and
  test files. `settings.notification_legacy_jobs_enabled` — the flag the
  CS-10 handoff described these as "gated by, default False" — **does not
  exist at all** on `Settings` any more (confirmed by grep + by
  `test_legacy_cutover.py`'s own assertion that it was removed in
  Notification Cadence v3, 2026-07-03). This sharpens the CS-10 handoff's
  premise: it is not merely defaulted off, it is **fully dead, unreachable
  code** in every deployed process (web/worker/scheduler). The `IndexError`
  risk on `schedule[0]` flagged by CS-10 is real *in the source* but cannot
  execute in production. **Not fixed** — matches this codebase's established
  convention (see the 2026-07-24 audit's own section E, "delete only if
  trivially safe... removal is a separate cleanup, not required").

## Custom-interval-only defect — full detail

**Root cause.** `frequency=="custom"` supports three independent
configurations: (1) recurring `therapy_schedule` entries, (2) calendar-picked
`custom_therapy_sessions`, (3) a pure interval (`custom_interval_days` +
`next_session_date` as anchor, no entries, no calendar picks — e.g. "every 10
days"). `compute_next_session_date`/`compute_last_session_datetime`
(`app/utils/therapy_schedule_utils.py`) correctly branch on
`frequency=="custom"` FIRST and resolve configuration (3) from
`custom_interval_days`+anchor alone. But 6 call sites had their own **local**
guard, added under CS-18, of the shape:

```python
schedule = parse_schedule(prefs) or []
custom_sessions = parse_custom_sessions(prefs)
if not schedule and not custom_sessions:
    return None  # (or "no_therapy_set")
```

CS-18's own comment says "only bail when BOTH are absent" — but for
configuration (3), *both are legitimately absent*, so this guard fired and
the generator never even called the compute function that would have
resolved it. This is the same bug class CS-10 already fixed in
`crud.get_therapy_schedule_with_frequency` and
`should_generate_for_therapy_day` — those two calls were in this round's CS-10
scope; these 7 were not.

**Fixed (7 call sites, this round):**
1. `app/api/v1/endpoints/therapy_tracking.py` — `/session-state`
   (`no_therapy_set` guard) — **CS-10 leftover (a), the other named handoff item**
2. `app/services/moments/therapy_appointment_generator.py`
3. `app/services/moments/therapy_prep_generator.py`
4. `app/services/moments/record_session_generator.py`
5. `app/services/moments/post_session_reflection_generator.py`
6. `app/services/moments/homework_reminder_generator.py`
7. `app/services/moments/between_sessions_note_generator.py`

**Fix applied.** Removed the local guard entirely (rather than patching it to
special-case configuration 3) — `compute_next_session_date`/
`compute_last_session_datetime` already return `None` safely for a genuinely
empty schedule of any frequency, so there is nothing unsafe about always
calling them and letting them decide. This exactly mirrors the fix CS-10
already applied and validated at `get_therapy_schedule_with_frequency`.
`therapy_tracking.py`'s guard could not be simply deleted (it also gates the
`no_therapy_set` early-return's shape), so it was extended to also allow
`frequency=="custom" and custom_interval_days is not None`.

**Population size.** DBA prod evidence (§B): 28 users have
`therapy_frequency='custom'`. Not all 28 are custom-interval-only (some use
calendar-picked sessions instead, which were already unaffected by this
bug) — the exact overlap isn't queryable from the data pulled for this
task, so the affected subset is bounded but not exactly counted.

**Not touched (out of this task's FILES scope, flagged for a follow-up):**
- `app/tasks/prep_card_auto_generate.py:134` — same guard pattern, drives
  automatic `SessionPrepCard` generation. Not a notification generator and
  not one of the two named CS-10 leftover files, so left alone per file-scope
  discipline, but it has the identical bug and should be fixed by whichever
  agent owns that file next.
- `app/services/notification_service.py:584` (`_process_first_nudges`,
  `if not schedule:` before the custom branch) — confirmed dead code, see
  section C above; not fixed since it cannot execute.
- `app/tasks/weekly_observations.py:181` (`if not schedule:`) —
  data-analytics-owned file, out of scope; flagged only.

## CS-08 sanity check — HOMEWORK_REMINDER routing

**Before:** `route_for(HOMEWORK_REMINDER)` == `/main-page/tab/workspace?section=todo`
(`app/services/notification_routes.py:77`, unchanged since MSV3.2.2).

**After:** unchanged — **no backend route change needed.** Verified two
things read-only against the frontend (`mindsync-frontend/mindsync_app/lib/`,
per the task's read-only grep instruction):

1. `lib/screens/moments/moment_deep_link_screen.dart` dispatches
   `MomentType.homeworkReminder` (along with every MSV3.2.2 deterministic
   type) through the **generic** renderer (`_showGenericSheet`), which
   navigates via `moment.deepLinkRoute` — the backend-supplied route string,
   verbatim, via `context.go(moment.deepLinkRoute)`. There is no
   homework-specific hardcoded path on the client to retarget.
2. `lib/navigation/ms_routes.dart` (~line 145: "`?section=<id>` ->
   `scrollTo`, consumed by the tab's ... Workspace: agenda/todo/goals")
   confirms `section=todo` is a live, recognized Workspace scroll-anchor —
   it already lands on the Workspace To-do module, which is exactly where
   CS-08 requires this reminder to go now that Main's Homework module is
   deleted. `MsRoutes.isRoutable()` gates unroutable/unknown routes to a
   silent skip (no dead-button sheet) per the existing MSV3.3.Fix.1 CS-06
   behavior — an old app build with an unrecognized route string degrades
   safely, it does not crash or dead-end.

**Trigger-condition sanity check (the actual ask):** confirmed and fixed a
real mismatch — see row 7 in the table above ((b), the self-heal bypass).
With no Main Homework surface, the *only* way a user now interacts with
homework items is via Workspace To-do, where CS-05/06/07 (this same MSV3.11
round) apply repeat-freq + self-heal semantics to every to-do item including
origin=therapist ones. `_has_open_homework`'s raw status query, unpatched,
would have silently skipped a legitimately-due repeating homework reminder.

## CS-10 leftovers — resolution

1. **`app/api/v1/endpoints/therapy_tracking.py` `/session-state` (~line 263):**
   confirmed live, confirmed bug (custom-interval-only → `no_therapy_set`).
   **Fixed** — see "Custom-interval-only defect" above.
2. **`app/services/notification_service.py::_process_first_nudges` (~line 583):**
   confirmed **dead code** — zero callers, and the flag the CS-10 handoff
   described it as gated by (`notification_legacy_jobs_enabled`) does not
   exist on `Settings` at all (fully removed 2026-07-03, not merely
   defaulted off). **Not fixed** — cannot execute in any deployed process.

## Items parked for Darek's decision

1. **Pass-3 cross-type stacking** (Q1 above) — up to 6 deterministic types
   could theoretically fire for one user in the same hour with no shared
   cap. Architectural, explicitly documented, not evidenced as a live
   problem at volume — flagged, not changed.
2. **WEEKLY_SUMMARY_READY / MONTHLY_SUMMARY_READY low SENT rates** (rows 12,
   13) — needs a job-log trace of the 4 burst days in the 14-day window
   before the SENT/EXPIRE ratio can be trusted as steady-state; handed to
   `data-analytics`/`backend-api` per the DBA report's own handoff note.
3. **`app/tasks/prep_card_auto_generate.py`** — same custom-interval-only
   bug pattern, out of this task's file scope; needs a follow-up fix by
   whichever agent owns that file.

## Tests

New/updated coverage (see commit for full list): custom-interval-only
regression tests on all 6 fixed generators + the `/session-state` endpoint;
a homework self-heal regression test; `CooldownGiveUpThrottle`
cooldown/give-up tests for both `ReflectionInvitationGenerator` (new real-
SQLite test class, since the existing suite used `MagicMock` and needed its
throttle calls stubbed) and `TherapyRelationshipCheckinGenerator` (extended
the existing real-SQLite test class, mirroring `AddTherapyDateGenerator`'s
already-established throttle-test pattern).
