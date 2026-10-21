---
name: c1-dead-instrumentation-backend-2026-08-10
description: C1 backend dead-instrumentation review — inapp_insight.generated stopped 2026-07-23 (not a code diff), recording_processing_* only wired to the Whisper fallback (not the AssemblyAI primary path), prep_card_auto_generated has no live emitter, report_exported removed as dead.
metadata:
  type: project
---

Full report: `analytics-reports/2026-08-10-c1-dead-instrumentation-review.md`, section "Backend". Commit `0a317e7` (BE main, local, not pushed) removed dead `report_exported` telemetry from `summaries.py::generate_report`.

## Key finding: `inapp_insight.generated` regression (unsolved, needs follow-up)
Fired 4 times / 3 users 2026-06-29→2026-07-23, then went completely silent for 18+ days while
`.shown` (14/5u) and `.acted` (5/2u) kept growing in the same window — ruling out a simple
timing/backfill artifact (if `.shown` depended on fresh `.generated`, it would have stopped too).
Checked `git log` on every file on the generation path (`in_app_insight_detector.py`,
`app/services/insights/*.py`, `notification_orchestrator_job.py`, `crud/app_insight_shown.py`,
`models/app_insight_shown.py`) for 2026-07-19..07-26 — **zero commits touch any of them**. The one
commit that touches `notification_orchestrator_job.py` in that window (`a918322`, 2026-07-24,
"CS-04 Insights/Streaks deletion") is about a DIFFERENT system — deleted PUSH "Moments" generators
(`pattern_insight`/`streak_celebration` moment types), not the in-app insight detectors. Confusing
naming collision: "Insights" in that commit message = Moments subsystem, not
`InAppInsightDetector`/`inapp_insight.*` subsystem — don't conflate them again.

So the stoppage is NOT a code diff in the emitter. Two live hypotheses, neither confirmed (out of
scope for C1 — needs prod RQ/DB access I didn't have this session):
1. Coincidence: all 5 detectors have narrow eligibility (streak∈{2,6,29}, monthly entry-count
   milestones, ≥14d symptom data + `STATS_TAB_OPENED` trigger — which per the same C1 audit's
   client section is likely unreachable now, since the old Stats tab has no screen widget file,
   same dead pattern as `AnalyticsCubit`). Plausible for a small user base over 3 weeks.
2. Same failure class as the Notification Moments registration gap (worker process not importing
   `app.services.insights` at module scope → `detector_count==0`) — a guardrail
   (`NoDetectorsRegisteredError`) was added 2026-07-03 specifically for this, and IS correctly wired
   (`import app.services.insights` at `notification_orchestrator_job.py:81`, confirmed present) —
   but a regression elsewhere could still be tripping it.

**Next step for whoever picks this up**: query prod RQ `FailedJobRegistry` for `run_insight_detection`
since 2026-07-23 for `NoDetectorsRegisteredError` — that's a `database-administrator` job (needs the
Heroku one-off dyno recipe), not something I can do with PostHog access alone.

## Key finding: `recording_processing_*` wired to the wrong (dead) path
`app/tasks/session_recording.py` has two processing functions: `process_session_recording`
(AssemblyAI, docstring literally says "Primary flow... the path taken by all new uploads", has been
primary since ~April 2026 per git history) and `process_session_recording_whisper` (fallback, only
runs when AssemblyAI fails repeatedly). The `recording_processing_started/completed/failed`
`posthog_capture` calls (added later, commit `74632f3`, 2026-07-03) were added ONLY to the Whisper
fallback function — never to the AssemblyAI primary path. Since AssemblyAI is primary and Whisper is
rare, these events essentially never fire (confirmed 0 all-time via posthog-data-extractor).
`test_recording_posthog_events.py`'s own module docstring documents "Backend emits: ... (whisper
worker, ...)" — the scope gap was apparently known/named at write time, just never extended to the
primary path. Neither `session_recording.py` nor `session_recordings.py` are mine — handoff to
backend-api with exact line numbers/property shapes is in the report. `recording_chunk_store_failed`
(different code path, PG chunk-store failure in `session_recordings.py`) is a live, correctly-wired,
legitimately-rare error event — zero volume there is a good sign, not a bug (ZOSTAWIĆ).

## Key finding: `prep_card_auto_generated` has no live emitter
Confirms/extends [[prep_cards_diagnosis_2026_08_10]]: the ONLY code that calls
`posthog_capture(event="prep_card_auto_generated")` is `POST /prep-cards/auto-generate`
(`prep_cards.py`), whose only client caller flutter-mobile deleted today (same C1 pass, client
section). The REAL auto-generation cron (`app/tasks/prep_card_auto_generate.py::auto_generate_prep_cards`,
runs hourly, 0 failures, but 0 rows ever produced per the earlier diagnosis) does NOT call
`posthog_capture` at all — builds `SessionPrepCard` directly with zero telemetry. Handoff to
backend-api: move the emission into the cron (`generated += 1` site), don't delete the event
definition — A11/A12 (same day) fixed the `therapy_schedule` save bug, so the cron's eligible
population may grow and start actually producing rows soon; the event is the only cheap way to tell
"auto-gen runs and succeeds" from "auto-gen never enters the per-user loop" without a DB read.

## Design pattern confirmed good: `weekly_summary_generated`/`monthly_audit_generated`
B3 (commit `e16f657`, same day, not mine to redo) deliberately did NOT create separate
`_regenerated` event names. `capture_summary_generated()` in `posthog_service.py` takes an
`is_regeneration: bool` and emits the SAME event name either way — verified all 6 call sites (weekly
cron + 2 manual endpoints, monthly cron + free-tier + premium + retry = covers both period types'
Generate and Retry paths). This is a better design than two event names for the stated goal
(generated-vs-read ratio) — don't "fix" this by adding `_regenerated` names if it comes up again.

## Reusable fact: `analytics-reports/` is NOT inside the MindSync git repo
`C:\Users\mikol\Notebooks\MindSync\Heroku` itself has no `.git` — only `MindSync/` and
`mindsync-frontend/` are separate repos. Report `.md` files under `analytics-reports/` at the Heroku
root are plain files, not version-controlled; only code changes inside `MindSync/` need `git add`/commit.
