---
name: project_recording_pipeline_db_check_2026_08_10
description: Session recording pipeline DB ground-truth check (2026-08-10) - DB-side is healthy, but only ~30% of PostHog's recording_started users ever produce a server upload_sessions row, and one completed session has no linked recording
metadata:
  type: project
---

DB-side of the session-recording pipeline (`upload_sessions`, `upload_chunks`, `session_recordings`) is healthy for last-14d (2026-08-10): 0 stuck `in_progress` sessions, 0 orphaned `upload_chunks`, 0 NULL durations, 0 FAILED recordings - everything that reaches the server completes cleanly. `upload_chunks` cleanup (transient-by-design) is working (0 rows at rest, 0 orphans).

But DB `upload_sessions` (14d) shows only 3 distinct users / 4 rows, vs PostHog's `recording_started` = 10 distinct users / 34 events in the same window. ~70% of PostHog "starters" never produce any server-side row at all - not stuck, not lost mid-upload, just never reach `POST /upload/initiate` (or that call fails with zero trace anywhere - no PostHog `recording_upload_failed` event, no DB row). Completion tail roughly reconciles (DB: 3 recordings/2 users vs PostHog: 3 completers), so the gap is specifically at the start of the funnel, invisible in both systems.

Also found: 1 of 4 (25%) `upload_sessions` in the 14d window has `status='completed'` but `recording_id IS NULL` (the `complete()` linkage step ran but didn't attach a `SessionRecording`). And 3/3 `session_recordings` in-window have `diarization_failed=true` + `assemblyai_transcript_id=NULL` despite `processing_status='COMPLETED'` (n too small to call a trend; flagged not root-caused, needs app-code owner to check if this is the designed fallback path or silent breakage).

**Why:** confirms/extends the pre-existing finding that `recording_processing_started/completed/failed` PostHog events have never fired (365d) - this check shows the backend pipeline itself works for rows it receives, so that's purely a missing-instrumentation gap, not a broken pipeline. The NEW gap this surfaced is upstream of that: initiate-time failures/abandons are invisible in both PostHog and Postgres.

**How to apply:** Full report + exact queries: `db-reports/2026-08-10-recording-pipeline-check.md`. If asked to re-check this pipeline later, reuse the query shapes there (they're schema-verified against live prod, not just `models.py`). Handoffs are to `backend-api` (unlinked-recording bug, diarization/transcript-id check) and `backend-api`/`data-analytics` (wire `recording_processing_*` events; add initiate-failure telemetry). See also [[reference_database_administrator_agent]] for the access recipe context and [[project_notification_moments_worker_registration_bug_2026_07_03]] for a similar prior pattern (feature working server-side but its telemetry/registration silently dark).
