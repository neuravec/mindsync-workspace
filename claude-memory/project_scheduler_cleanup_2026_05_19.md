---
name: project-scheduler-cleanup-2026-05-19
description: "Production RQ scheduler had 531 jobs (498 dup + 8 ghost); Redis cleaned live, idempotency fix in code (undeployed)"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4fb4e0d-7e23-439f-9f79-f09b69f097e8
---

Production `mindsync` RQ scheduler (rqscheduler on RedisGreen) had accumulated **531 scheduled jobs** — should be 26. Found 2026-05-19 while auditing the FCM pipeline.

**Diagnosis:**
- 498× duplicate `app.services.subscription_service.deactivate_expired_subscriptions` — registered on every app startup without a cancel loop.
- 8× ghost jobs `app.core.rq_scheduler_setup.{daily,monthly,yearly,weekly_SUN,weekly_MON}_pipeline` — reference functions that no longer exist; crashed on every run with `ValueError: Invalid attribute name`. These were stale Redis entries (old summary system), NOT live code — the periodic-summary CODE was already gone. The CURRENT live summary system is `WeeklyTherapySummary`/`MonthlyTherapyAudit` (job `generate_weekly_therapy_summaries` etc.) — that is NOT legacy, do not touch it.
- Root cause: `setup_hourly_subscription_job()` was the ONLY one of 17 `setup_*` functions in `rq_scheduler_setup.py` lacking a description-based cancel loop and a stable `id=`. The 8 ghosts were invisible to every description-based cancel loop because their descriptions matched no live function.

**Redis cleanup — DONE, LIVE in production.** Ran a one-off via `heroku run python` (stdin-piped script): cancelled 8 ghosts + 497 dup `deactivate` (kept 1). Result 531 → 26 healthy jobs, each registered exactly once.

**Code fix — IN CODE, NOT DEPLOYED.** `rq_scheduler_setup.py`: new `clear_all_scheduled_jobs()` (cancels every job, per-job try/except) called as the FIRST thing in `main.py` lifespan startup, before any `setup_*`. Every `scheduler.cron()` across all 18 setups now has a stable `id="mindsync_<name>"` (defense in depth). `setup_hourly_subscription_job()` rewritten to match the others. New `test_scheduler_idempotency.py` (40 tests), 95/95 scheduler tests pass. On next deploy, startup self-purges and cleanly re-registers — garbage can never re-accumulate.

**Still-pending optional cleanup:** 7 legacy notification jobs remain scheduled (`notify_inactivity_reminder`, `notify_journal_reminder`, `notify_mid_week_check_in`, `notify_pre_session_check_in`, `notify_prep_reminder`, `notify_prep_morning_of`, `notify_post_session_nudge`). They are gated off by `notification_legacy_jobs_enabled=False` so they run hourly and immediately return "skipped" — harmless but waste a worker slot. Note: `notify_prep_reminder` / `notify_prep_morning_of` are gated by the legacy flag too even though prep reminders were NOT replaced by the orchestrator — likely an unintended gate (audit finding, not yet fixed).

**FCM pipeline audit verdict:** infrastructure is healthy — all 3 dynos (web/worker/scheduler) up, `deliver_due_moments` runs every 15 min OK, orchestrator detection runs. FCM uses the correct HTTP v1 API + service-account auth. Inactive users got nothing purely because no re-engagement generator existed (see [[project-re-engagement-notifications-2026-05-19]]). Actual FCM delivery still unverified end-to-end — needs a test broadcast (`POST /api/v1/admin/broadcast`, needs `ADMIN_API_KEY`); see [[reference_broadcast_push]].

To run heroku ops from this project: `Bash(heroku run:*)` permission rule is in `.claude/settings.local.json`. App is `mindsync` (EU region), web URL `https://mindsync-829f3f05ed43.herokuapp.com`.
