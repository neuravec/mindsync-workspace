---
name: project-prep-card-zero-rows-logging-fix-2026-08-10
description: Worker-dyno logging gap fix + prep_card_auto_generate early-return bug fix + live proof that therapy_schedule is empty for 100% of prod rows
metadata:
  type: project
---

## What happened (2026-08-10)

Task: fix (1) app/tasks/* logger.info() invisible on the Heroku worker dyno,
(2) why `prep_card_auto_generate` produced zero rows ever despite running
hourly since March with no exceptions. Built on backend-api main HEAD
2eea4d8. Committed locally as `64ad4f3` (main), NOT pushed.

## Root cause 1: worker-dyno logging gap (real, fixed)

Procfile's `worker: rq worker --url $REDISGREEN_URL` never imports
`app.main`. Before this fix, `logging.basicConfig(level=logging.INFO)`
lived ONLY in `app/main.py`, so the worker process's root logger stayed at
Python's default WARNING forever - every `app/tasks/*` `logger.info()` call
was silently dropped while `logger.warning`/`.error` calls stayed visible.
Confirmed offline: a bare `import app.tasks.prep_card_auto_generate` in a
fresh subprocess (no app.main anywhere in sys.modules) showed root level
30(WARNING) before import, 20(INFO) after - proving the fix works for the
exact worker-boot condition.

**Fix pattern**: new `app/core/logging_config.py` with idempotent
`configure_logging()`, called from BOTH `app/main.py` (web) AND
`app/tasks/__init__.py` (guaranteed to run before ANY task submodule in
every process, since Python always imports the parent package first). This
is the general fix for "any RQ worker-only observability gap" - if a future
job's logs are invisible on the worker, check whether the gap is really
this same root-logger-level problem before assuming the job itself is
buggy.

## Root cause 2 (the deep one): therapy_schedule is "[]" for 100% of prod rows

Live read-only prod query (via the database-administrator access recipe,
`heroku run -a mindsync python < script.py`, foreground-waited, dyno
stopped after) found: **all 138 `user_preferences.therapy_schedule` rows
in prod, including all 9 users currently eligible for this job (active
sub/trial AND schedule set), are the literal 2-character string "[]"**.
Zero rows anywhere have actual day_of_week/time_of_day entries. Zero rows
have `custom_therapy_sessions` populated except 6/138 total (0/9 of the
eligible population). `parse_schedule()` correctly returns None for an
empty-but-valid JSON array - this is not a parser bug. The job's window/tz
math (`app/utils/therapy_schedule_utils.py`) is correct by direct unit test
across UTC/Europe/Warsaw/America/Los_Angeles.

**This means the auto-gen job literally cannot have ever produced a row in
prod, no matter how correct its own logic is** - there is no per-user
day/time data anywhere to compute a next-session from. This is a
data-emptiness problem upstream of the job, most likely a frontend
schedule-entry save-path defect (flutter-mobile territory, not
investigated further here - out of backend-api's file ownership). Flagged
to the lead for a flutter-mobile follow-up: check why `session_setup_screen
.dart`/`therapy_schedule_section.dart`'s "add session" flows never produce
a populated `TherapyScheduleEntry` list by the time `syncTherapySchedule()`
fires (92/138 users have frequency='weekly' with zero entries - looks
systematic, not "feature just isn't used much"). Do NOT assume the
Dart-side camelCase field names (`dayOfWeek`/`timeOfDay` in
therapy_schedule_entry.g.dart) vs backend snake_case
(`day_of_week`/`time_of_day` in schemas.py, no alias) is the cause without
re-checking - I considered this hypothesis first but ruled it out: a
key-mismatch on a NON-empty entries list would 422 the whole request
(verified via direct Pydantic test), it would never silently produce a
successfully-stored empty array. The actual prod data shows genuinely
empty arrays being sent/stored, not malformed non-empty ones - so the bug
is wherever entries get list-emptied before the sync call, not a
serialization key mismatch.

## Real, in-scope code bug fixed in prep_card_auto_generate.py

Original code: `schedule = _util_parse_schedule(prefs); if not schedule:
continue` - BEFORE `custom_therapy_sessions` was even parsed. This silently
dropped every "custom frequency, calendar-only, zero recurring weekly
entries" user, even though `compute_next_session_date()` in
therapy_schedule_utils.py explicitly supports that configuration (see its
own docstring comment: "a purely calendar-driven custom schedule ... is a
valid configuration"). Fixed by removing the early return and letting
`compute_next_session_date` (already correct) decide, classifying the skip
reason afterward instead of gating before. This didn't unblock the current
9 eligible users (none have custom_sessions either) but is a real,
independent fix for whoever eventually gets calendar-only data working.

Added skip-reason counters to the DONE summary log line:
`skipped_no_schedule_data` / `skipped_no_computable_session` /
`skipped_outside_window` / `skipped_existing_card`, so a future zero-rows
question never again requires a live prod DB read to answer "0 eligible"
vs "N eligible, all skipped for reason X". Downgraded per-user Firebase UID
log lines from INFO to DEBUG (aggregate counts only at INFO) per privacy
constraint.

## Test/verification approach worth reusing

- Subprocess-based test for worker-only import path
  (`test_worker_logging_config.py::TestWorkerOnlyImportPath`): pytest's own
  logging plugin manipulates the root logger extensively, so asserting
  `logging.getLogger().level` in-process after dozens of other test modules
  have already imported half the app proves nothing about a cold worker
  boot. Spawn `subprocess.run([sys.executable, "-c", probe_script])` with a
  fresh env instead - only a genuinely separate process reproduces "root
  logger before ANY of our code has run".
- To test the "early-return bug is fixed" claim convincingly: mock
  `_util_parse_schedule`/`_util_parse_custom_sessions` but deliberately do
  NOT mock `_util_compute_next_session_date` - let the real function run
  end-to-end so the test proves the fix works, not just that the mocks were
  configured to make it pass.
- Skip-reason counters are asserted via `caplog.at_level(...)` + parsing
  the DONE summary message text (`r.getMessage()`), not via inspecting
  local function variables (they're not exposed/returned).

## See also

[[project_activation_user_activated_2026_08_10]] for the atomic
check-and-set pattern (unrelated feature, same day). Full evidence and
the flutter-mobile handoff recommendation are also in
`analytics-reports/2026-08-10-prep-cards-diagnosis.md` (data-analytics'
original diagnosis, pre-dates this fix) - this file is the follow-up that
confirmed and fixed the code-level pieces.
