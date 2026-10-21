---
name: notification-cadence-v3
description: Legacy notification job/flag cleanup (2026-07-03) — what was removed, kept, and flagged; migration ww3x4y5z0a1b; test blast-radius results
metadata:
  type: project
---

## Notification Cadence v3 — Legacy Cleanup (2026-07-03, on disk, not deployed)

**Migration**: `ww3x4y5z0a1b` (add DAILY_CHECK_IN + SESSION_MORNING_OF to moment_type_enum) -> `vv2w3x4y5z0a` (upload_chunks) -> `uu1v2w3x4y5z` -> ...

Removed entirely: `notification_legacy_jobs_enabled` flag (config.py); 7 setup_* scheduler functions in rq_scheduler_setup.py (setup_hourly_prep_notification, setup_hourly_health_check_notify, setup_hourly_prep_morning_of — unconditionally-registered "ghost" jobs whose bodies no-opped via the flag; setup_hourly_post_session_nudge, setup_hourly_symptom_tracking_reminder, setup_hourly_mid_week_check_in, setup_hourly_pre_session_check_in — gated at registration time by the same flag); 7 notify_* functions in notification_service.py (notify_prep_reminder, notify_prep_morning_of, notify_post_session_nudge, notify_mid_week_check_in, notify_pre_session_check_in, notify_journal_reminder, notify_inactivity_reminder); whole files app/tasks/health_check.py and app/tasks/symptom_tracking_reminder.py; crud.get_users_eligible_for_notification (only caller was the 2 removed journal/inactivity functions).

KEPT deliberately (to preserve still-relevant test coverage / avoid scope creep beyond the named functions): private helpers `_next_session_datetime_for_entry`, `_compute_next_session`, `_process_first_nudges`, `_process_followup_nudges`, `_generate_nudge_text`, `_compute_last_session_for_entry`, `_compute_midpoint_weekday`, `NUDGE_PROMPT_DEFAULT`/`NUDGE_FOLLOWUP_PROMPT_DEFAULT`/`FALLBACK_NUDGE_*` in notification_service.py — all now unreachable from any scheduler/orchestrator entry point but still directly unit-tested; `crud.create_post_session_nudge`/`get_post_session_nudge`/`update_post_session_nudge` (unreachable but untouched, out of explicit scope); `pydantic_structures.Journal_notification` (now unused, harmless).

NOT touched (cross-cutting — flagged for lead/other agents instead of editing): `app/tasks/weekly_therapy_summary.py` and `app/tasks/monthly_therapy_audit.py` both still read `_settings.notification_legacy_jobs_enabled` for their FCM-send guard — but that block is wrapped in try/except, so post-removal it degrades to a caught AttributeError + error log (data generation unaffected, no crash); `.env.example` line 95 `notification_legacy_jobs_enabled=false` (integration-devops owned); a docstring line in data-analytics's `app/services/moments/session_morning_of_generator.py` mentions the flag (historical context only, not executable).

**Test surgical-edit pattern** — grep class boundaries first (`grep -n "^class "`), read only the affected range, and NEVER wholesale-delete a test file without checking every class: `test_phase4_cleanup.py` and `test_legacy_cutover.py` looked like "pure legacy" files by name but each had 3-5 classes covering *unrelated* still-live behavior (schema zombie-field removal, orchestrator smoke test, weekly/monthly summary dual-purpose cutover) that had to be preserved.

**Import-style severity rule**: a top-level `from module import removed_symbol` in a test file crashes that ENTIRE file's collection (all tests error, not just the ones using the symbol) — lazy/inline imports inside test methods only fail that one test. Always grep for the import style before deciding severity/whether to touch a file.

**Test results**:
- Authorized-scope test run (test_health_check.py, test_health_check_phase2.py, test_post_session_nudge.py, test_legacy_cutover.py, test_phase4_cleanup.py, test_main_lifespan_orchestrator.py): 214 passed, 1 pre-existing unrelated failure (`TestTranscriptionSessionEndpoint` in test_health_check.py, a WHISPER_MODEL config mismatch in `app/api/v1/endpoints/health_check.py` — never touched by this task).
- Full `app/tests/` run after this change: 3910 passed, 101 failed, 1 collection error (`test_prep_reminder.py` — top-level `notify_prep_reminder` import). Failures span 8 out-of-scope files not authorized for this task: test_scheduler_idempotency.py, test_notification_improvements.py, test_notification_premium_gate.py, test_prep_card_overhaul.py, test_legacy_rollback.py, test_symptom_visibility_pause.py, test_therapy_frequency.py (2 tests reference `app/tasks/health_check.py` directly), test_prep_reminder.py — flagged for qa-testing, not fixed here per FILES-scope boundary. Some of the 101 are unrelated pre-existing baseline (test_voice_fixes.py, test_walkthrough.py, test_symptom_suggestions.py).

See [[offline_verification]] for how app.main / the migration were verified without a real DB.
