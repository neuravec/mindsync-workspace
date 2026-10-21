---
name: heroku-boot-verification
description: How to verify a MindSync backend boot on Heroku after push to origin/main: timings, expected scheduler job count, log-buffer pitfalls, and why rare code paths cannot be proven from logs alone
metadata:
  type: reference
---

Observed on the v577 deploy (2026-10-19, PostHog identify fix):

- Timing: push to origin/main -> `heroku releases` shows "Deploy <sha8>" after ~75 s; all three dynos restart ~35 s after that. Poll in the foreground (`for ... sleep 20` loop works inside one Bash call; a bare foreground `sleep` is blocked).
- Healthy boot markers: web `Application startup complete.`; worker `*** Listening on high, default...`; scheduler `Registering birth`. Web exiting with status 143 on SIGTERM during restart is normal.
- Scheduler sanity: web boot logs `clear_all_scheduled_jobs: cancelled N existing job(s)` and must re-register the same N. In Oct 2026 N = 27: 24 lines `[Scheduler] Scheduled ... <Job mindsync_...>`, 2 lines `Scheduled nightly Loops sync` / `Scheduled daily streak break check` (no [Scheduler] tag), and 1 line `INFO root: Scheduled hourly subscription deactivation job.` Grepping only `[Scheduler] Scheduled` gives a false 24-vs-27 mismatch.
- Log buffer: `heroku logs -n 1500` is the max and covers only ~10-40 min because the worker dominates (~80% of lines). For a 10-min verification window, snapshot every ~90 s, concatenate, `sort -u`, then filter by timestamp >= release time.
- Benign noise that matches naive error greps: `PostHog api_error capture handlers registered: ... Exception` (INFO), pydantic V2 config UserWarning, rq_scheduler crontab FutureWarning, and 404 on `/api/v1/health-check/latest` (documented "no completed health checks").
- v578 (2026-10-19, b6074de) repeated the same timings with the CLI untouched: Platform API releases/dynos/slugs plus POST `/log-sessions` `{"lines":1500}` every ~90 s (snapshot script in scratchpad). Distinct `<Job mindsync_` ids = 26, because the hourly subscription line carries no Job tag, so 26 + 1 = 27 is the healthy count. Buffer turnover jumps to ~4 min per 1500 lines around the :00 hourly cron; keep snapshots <= 90 s apart then.
- Pre/post comparison trap: the hourly :00 notification cron emits ~70 `notification_orchestrator` WARNINGs ("not eligible for AI-generated moment text", the v549 cost-cut fallback) and `voice_director monthly_audit ... 'themes_and_patterns'` (pre-existing). A pre-release window that missed :00 shows zero warnings, which is not evidence of a regression; check whether the commit touches those files.
- Router lines print client IPs (`fwd=`) and the Release/log-session lines print the operator email; redact both in reports.
- PostHog person-property path (`posthog_service.identify`) runs only on `POST /api/v1/conversations/{id}/end`, `PUT /api/v1/users/subscription` and the weekly premium-intent cron. At normal traffic it may not fire in a 10-min window, so "no error in logs" is not proof it works; confirm positively via [[posthog-data-extractor]] looking for backend `$set` events after the release time.
