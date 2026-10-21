---
name: project-msv310-cs02-add-therapy-date-investigation-2026-09-01
description: CS-02 (MSV3.10) "unset appointment time" push - REAL root cause found and fixed backend-side: a frequency-only save (weekly<->biweekly) silently wiped an unrelated one-off custom_therapy_sessions entry; stale-delivery theory (my first hypothesis) conclusively ruled out by prod evidence
metadata:
  type: project
---

## UPDATE (same session, after initial diagnosis): actual root cause found and fixed
The stale-delivery theory below (my FIRST hypothesis, before prod evidence
arrived) is WRONG and was ruled out. The REAL bug, found by re-reading DBA's
full report closely (not just the coordinator's summary of it) plus tracing
`SettingsCubit.updateTherapyFrequency` in the frontend: `crud.
update_therapy_schedule`'s `custom_therapy_sessions` clear-guard used to read
`elif frequency != "custom":` -- checking only the INCOMING frequency, not
whether the user was actually leaving "custom" mode. Any partial-update call
that omits `custom_sessions_json` while landing on a non-custom frequency
wiped the column -- including a plain weekly<->biweekly toggle, which has
NOTHING to do with a one-off calendar-picked session. **Fixed**: capture
`previous_frequency = prefs.therapy_frequency` BEFORE overwriting it; only
clear when `previous_frequency == "custom" and frequency != "custom"` (a
genuine abandonment). Commit `7dddf38` on branch `msv3.10-cs02`, NOT pushed.
See the commit message for the full trace and test list (6 new/updated
tests, confirmed red pre-fix via `git stash crud.py`-only, green after).

**Lesson for next time — read the FULL specialist report, not the
coordinator's summary of it.** The coordinator's relay message gave me four
numbered takeaways from DBA's report and I initially worked from those
alone; only when I went back and read the actual
`db-reports/2026-09-01-cs02-add-therapy-date-false-push.md` file in full did
I find the DBA's own explicit hint ("a frequency switch without re-sending
custom_sessions, a path crud.update_therapy_schedule explicitly guards
against for one specific case but which may have other triggers not
covered") that led directly to the real bug. A relayed summary is lossy by
construction — always fetch and read the primary artifact (report file,
commit, ticket) a summary refers to before finalizing a diagnosis on it.

## Original diagnosis trail (kept for the ruled-out theory + evidence)

## What happened
CS-02 spec: [użytkowniczka V] (call 2026-08-13) set her next therapy session (Wednesday
15:00) and still received the ADD_THERAPY_DATE "you haven't set a time" push.
Task brief hypothesized backend stale-state delivery as the likely cause and
asked to fix the cause, not the symptom.

## Backend-side trace (confirmed correct, not the bug)
- Generator: `app/services/moments/add_therapy_date_generator.py`
  (`AddTherapyDateGenerator`, deterministic Pass 3, fires once/day at
  `DAY_PRECISION_SEND_HOUR`=18 local). Eligibility = `compute_next_session_date`
  from `app/utils/therapy_schedule_utils.py` returning None.
- `compute_next_session_date`'s one-off `custom_sessions` branch (CS-18 bug B
  fix, already landed) correctly resolves a future one-off session regardless
  of `frequency` value -- confirmed correct by existing test
  `test_not_eligible_when_only_a_custom_session_is_set` in
  `test_msv322_new_generators.py`, and re-confirmed by my own trace. This is
  NOT where the bug is.
- Save path: `PUT /users/therapy-schedule` -> `crud.update_therapy_schedule`
  (crud.py) is the SOLE production writer of `therapy_schedule` /
  `custom_therapy_sessions` (grep-confirmed). Correctly persists both columns
  and computes `next_session_date` when called with a valid payload.
- **Stale-delivery theory ruled out by `database-administrator` prod evidence**
  (`db-reports/2026-09-01-cs02-add-therapy-date-false-push.md`): median
  generation-to-delivery lag 1.1 min, p95 5.6 min, ZERO moments over 1 hour in
  30 days, globally and for the reported user specifically. A save-vs-delivery
  race window this narrow essentially cannot explain a user-reported "still
  got it" complaint. **Lesson: don't accept a plausible-sounding
  architectural race as root cause without checking prod timing data first --
  see [[feedback_prod_evidence_before_code_only_diagnosis]].**

## The actual likely root cause: frontend save-path defect
`mindsync-frontend/mindsync_app/lib/api/api_managers/users_manager.dart`'s
`syncTherapySchedule` (~line 201) wraps its `PUT /users/therapy-schedule` call
in an **un-awaited** `try { ... } catch (_) { }` -- ANY failure (network,
expired Firebase auth token, 422 validation) is silently discarded with zero
user-facing error, zero retry, zero telemetry. The caller,
`SettingsCubit._persistAndSyncSchedule` (settings_cubit.dart ~line 74),
updates local `SharedPreferences` + Cubit UI state **unconditionally, before**
firing this fire-and-forget call -- so the app can show "Wednesday 15:00
saved" to the user while the backend never received anything. This fully
explains [użytkowniczka V]'s report AND her current DB state (`therapy_schedule`,
`custom_therapy_sessions`, `next_session_date` all NULL today, per DBA, with
no persistence trail of a save ever landing -- `user_preferences` has no
`updated_at` column so "saved then wiped" vs "never saved" can't be told
apart from data alone).

**Strong corroborating precedent, already on frontend `dev`**: commit
`d3cd092` (2026-08-10 15:55 CEST, "fix(therapy-schedule): map
TherapyScheduleEntry JSON keys to snake_case") documents that
`TherapyScheduleEntry.toJson()` emitted camelCase `dayOfWeek`/`timeOfDay` with
no `@JsonKey` mapping while the backend Pydantic schema requires snake_case
(both required) -- **every PUT with a non-empty RECURRING schedule 422'd,
silently swallowed by this exact `syncTherapySchedule` catch, for 138/138
prod users** (100% of `therapy_schedule` rows were the literal string "[]").
`CustomTherapySession` (the ONE-OFF flow) already had correct `@JsonKey`
mapping and worked for the 6/138 users who used it. This commit fixed the
model's JSON keys but did **not** touch `syncTherapySchedule`'s swallow-all
pattern itself -- confirmed via `git log` on `users_manager.dart`, no later
commit touches it either. [użytkowniczka V]'s call (2026-08-13) is 3 days after this
fix landed on `dev` -- **unconfirmed whether her installed build (TestFlight
vs public App Store/Play, which per [[reference_frontend_ci_git_topology]]
promotes to production manually, not automatically on every `dev` push) had
actually picked up this fix by the time of her report.** This is the single
most important open question for whoever picks this up next.

## What I did NOT do
Per the task's own guardrail ("if the root cause turns out to live in the
Flutter save path, STOP... report back to the lead"), I did not touch any
frontend file. I did not attempt to "fix" `syncTherapySchedule`'s error
handling myself even though I found it and it is clearly the more likely
culprit -- that is `flutter-mobile`'s file, out of my ownership.

## What I did instead (backend hardening, explicitly NOT presented as the fix)
Added `cancel_active_moments_by_type()` to `app/crud/notification_moment.py`
and wired it into `crud.update_therapy_schedule` (crud.py): when a save
resolves to a known future session, any still-active (PENDING, or
SENT-with-`push_delivered=False`) `ADD_THERAPY_DATE` moment for that user is
transitioned to `EXPIRED` (reused -- no `CANCELLED` status exists and adding
one needs a migration, out of scope) with a `scoring_signals.cancelled_reason`
marker. This closes the theoretical generation-vs-delivery race the task
brief hypothesized, even though prod data shows that race essentially never
manifests today. 21 new tests (10 CRUD-level in
`test_crud_notification_moment.py`, 11 end-to-end in the new
`test_msv310_cs02_stale_add_therapy_date_push.py`), confirmed red pre-fix via
`git stash`, green post-fix. See [[patterns_cancel_active_moments_by_type]]
for the reusable pattern.

## Follow-ups recommended (not implemented)
- `updated_at` column on `user_preferences` (DBA's ask) -- needs a migration,
  flagged to the lead, not created in this batch.
- `flutter-mobile` should: (1) verify whether the reporting user's build
  predates/postdates commit `d3cd092` (posthog `$app_version` around
  2026-08-13, correlated against release timing -- integration-devops or
  posthog-data-extractor territory), and (2) fix the underlying
  swallow-all-errors pattern in `syncTherapySchedule` regardless (surface a
  retry/error state, add telemetry on failure) since the JSON-key bug is only
  ONE instance of a class of bug this pattern permits going forward.

## Commits
Branch `msv3.10-cs02` (backend repo), NOT pushed:
- `37532c0` — secondary hardening (cancel-on-save), NOT the fix for the
  reported bug.
- `7dddf38` — the actual root-cause fix (frequency-switch clear-guard
  correction). See the UPDATE section at the top of this file.

The frontend swallow-all-errors angle (`syncTherapySchedule`, `d3cd092`
precedent) documented above remains a real, separate, still-open risk for
FUTURE incidents of this general shape, but is no longer believed to be
what caused THIS specific report — the frequency-switch wipe fully explains
it. Still worth flagging to `flutter-mobile` as a follow-up hardening item,
just not as urgent/causal as originally suspected.

**Full-suite confirmation (both commits applied)**: `python -m pytest
app/tests/ -q` → 21 failed, 5519 passed, 508.93s. The 21 failures are
EXACTLY the known pre-existing baseline (custom-therapy-sessions×2,
first-impression×1, notification-improvements×4, onboarding-v2×1,
symptom-suggestions×1, therapy-frequency×5, therapy_tracking_fix1_a12
date-relative-flake×1, voice-fixes×5, walkthrough×1) — matches the
2026-08-17 reference baseline ("21 BE fail sprzed prac to znany baseline")
exactly, zero new regressions. An EARLIER full run (only the first,
secondary-hardening commit applied) showed 25 failures with 4 extra in
`test_timeline.py::TestExistingFunctionsExcludeSoftDeleted` — confirmed
transient/order-dependent noise (passed cleanly in isolation, gone on
re-run), not caused by either of my changes — another instance of the
known SQLite-leftover-state flakiness class, see Test Patterns in
MEMORY.md.
