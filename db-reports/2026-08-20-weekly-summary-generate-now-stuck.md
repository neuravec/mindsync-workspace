# Weekly summary "Generate Now" stuck on prod — 2026-08-20

**Operator report:** weekly summary stays on "Generating summary..." after tapping the button.
**Context:** MSV3.3.Fix.1 CS-07 (naive-datetime root cause + stale-PROCESSING sweep + retryable generate) deployed as Heroku v542 (`a817b77`, incl. `0a3ef72`). All three dynos restarted at deploy: **2026-08-20 08:09:31 UTC**. This audit ran ~09:16–09:48 UTC the same day, read-only, via the Heroku one-off dyno recipe (PowerShell `--no-tty` variant). No writes made.

## Verdict up front

The CS-07 fix **worked** — weekly/monthly summaries are being produced for the first time ever. The "stuck" symptom is real but is **not a regression of CS-07's own logic**; it's a **queue head-of-line-blocking side effect of that same fix finally unblocking a ~1,800-user backlog** hitting a single-worker, single-shared-queue RQ setup. Full mechanism below.

## 1. Weekly summary rows — table is no longer empty

```sql
SELECT count(*) AS total,
       count(*) FILTER (WHERE created_at >= '2026-08-20 00:00:00+00') AS since_deploy,
       min(created_at), max(created_at)
FROM weekly_therapy_summaries;
```
`total=145 | since_deploy=145` — **every single row in the table was created today**, confirming the table was empty before v542 (matches the known CS-07 baseline: naive/aware TypeError blocked generation "since always").

Status breakdown (enum `processingstatusenum`, labels confirmed UPPERCASE — `PENDING/PROCESSING/COMPLETED/FAILED/PLAIN_TEXT`, no drift from the model):

| status | count |
|---|---|
| COMPLETED | 143 |
| PROCESSING | 1 |
| FAILED | 1 |

So: 143/145 (98.6%) succeeded. Only 2 rows are non-COMPLETED.

## 2. The stuck row — smoking gun

- Row `id=1`, user `<UID-1>`, `created_at=2026-08-20 09:16:14.452212+00:00`.
- This is (by row id and timing) almost certainly the very first "Generate Now" tap after deploy — the table was empty, so id=1 is literally the first row ever inserted, and its creation timestamp lines up to the second with an RQ job enqueue (below).
- The **hourly stale-PROCESSING sweep worked correctly**: at `2026-08-20 09:38:49`, the hourly cron's first step swept this row from PROCESSING → FAILED ("retryable") after it sat PROCESSING for ~22.5 minutes (threshold is 15 min). Log: `[WEEKLY_THERAPY_SUMMARY] Swept stale PROCESSING summary 1 ... -> FAILED (retryable)`.
- One live PROCESSING row remains as of the last check (`id=145`, created `09:43:15`, age <1 min at query time) — a normal in-flight generation, not evidence of a new stuck case.
- No duplicate `(user_id, data_window_end)` pairs exist (`0`), so the `uq_weekly_summary_user_period` constraint (migration `kk2l3m4n5o6p`) applied cleanly — confirmed present via `pg_constraint`.

**Why row 1 sat for 22+ minutes despite the worker dyno being up the whole time (birth `08:09:31`):**

```
RQ "default" queue, job 47036fe2-c548-48fa-bab6-31a2f5e0c492
  func: app.tasks.weekly_therapy_summary.run_weekly_summary_ai_job
  enqueued_at: 2026-08-20 09:16:14.475026+00:00   <- same instant as row id=1's created_at
```

This job is **still sitting unprocessed in the queue** as of the last check (~09:45, 29+ minutes after being enqueued). It was never cancelled when the DB row was swept to FAILED — it will eventually run and silently no-op (the job code bails out if the row is no longer PROCESSING), but it never got a chance to actually generate anything within the user-visible window.

## 3. Root cause: single-worker, single-queue head-of-line blocking

```
Worker 0a9cdbf74c56403aa23a9c72fb0bee91
  state: busy
  current_job: app.tasks.weekly_therapy_summary.generate_weekly_therapy_summaries
               (id: mindsync_hourly_weekly_therapy_summary)
  birth: 2026-08-20 08:09:31   last_heartbeat: 2026-08-20 09:45:17 (alive, not crashed)
```

- Procfile runs exactly **one** `rq worker` process (`worker: rq worker --url $REDISGREEN_URL`), no concurrency, no queue priority — it services the single "default" queue strictly FIFO, one job at a time, start to finish.
- The hourly cron `generate_weekly_therapy_summaries` is itself one RQ job that loops **synchronously** over every user needing a first-ever summary (~1,800 candidates), calling OpenAI + persisting per user, ~1–2 seconds apart, with no yielding back to the queue. While this one job runs, the sole worker **cannot dequeue anything else** — not the interactive "Generate Now" job, not anything.
- Because this was the fix's first successful run ever, it also triggered a companion bulk run of `generate_monthly_therapy_audits`, which alone produced **1,752 COMPLETED rows** (100% since deploy, 0 PROCESSING now) and enqueued 1,752 `index_monthly_therapy_audit_to_rag` follow-up jobs onto the same "default" queue between `09:00:42` and roughly `09:23` (queue front sample confirms this burst). The weekly cron then queued its own `index_weekly_therapy_summary_to_rag` follow-ups behind that.
- **Queue depth at the time of the check: 2,032 jobs**, almost entirely RAG-indexing backfill (histogram of the first 300 queued jobs: 298 are `index_monthly_therapy_audit_to_rag`, 1 notification job, 1 recording-recovery job). The operator's `run_weekly_summary_ai_job` landed behind hundreds of these low-priority jobs the instant it was enqueued, and the worker itself was then captured for an extended stretch by the giant synchronous hourly-cron job on top of that.
- Net effect: an **interactive, user-facing job shares an unprioritized FIFO queue and a single-concurrency worker with a slow bulk backfill** — a large backfill (which will recur any time a big cohort needs first-time generation, or a bug causes mass retries) guarantees "Generate Now" stalls past the 15-minute sweep threshold, producing exactly the reported symptom.

## 4. FailedJobRegistry — a separate, pre-existing issue (not the cause here)

`failed_count = 565` in the "default" queue's FailedJobRegistry, spanning back to at least `2026-07-03`. Sampled entries include `mindsync_hourly_monthly_therapy_audit` itself failing today at `09:32:39` (worth a look — the 1,752 monthly rows still landed successfully in the DB before whatever caused the job-level failure, so this looks like a late-stage crash in that job run, not a generation failure) plus long-standing repeat offenders (`goal_narrative.regenerate_goal_narratives` — "Work-horse terminated unexpectedly", `recording_recovery`, `loops_sync`). This registry has evidently never been drained/monitored. Flagged separately — not diagnosed further here, out of scope for this ticket.

## 5. Monthly summaries — same code path, not currently stuck

- 1,752 total rows, all since deploy, **all COMPLETED**, **0 PROCESSING** at check time. No stuck monthly rows. This confirms the naive/aware TypeError fix itself is solid on both paths — the weekly-specific symptom is a queue-contention artifact of timing (weekly's bulk run and interactive taps overlapped the backlog window; monthly's bulk run had already finished draining by the time of this check).

## 6. Worker/dyno health

```
heroku ps -a mindsync:
  web.1:       up 2026/08/20 10:09:39 +0200 (08:09:39 UTC)
  worker.1:    up 2026/08/20 10:09:30 +0200 (08:09:30 UTC)
  scheduler.1: up 2026/08/20 10:09:30 +0200 (08:09:30 UTC)
```
All three dynos are up since the deploy restart, none crash-looping. The worker is alive and heartbeating (`09:45:17`) — it is **busy**, not dead. This rules out "worker isn't running" as the cause; it's a scheduling/prioritization problem, not an availability problem.

## 7. Logs — retention did NOT cover the operator's tap; do not infer from absence

`heroku logs -n 1500` returned only **worker.1** lines, all within a **~6.5-minute window** (`09:34:52`–`09:41:21`) — the worker's own bulk-generation chatter (one log line per user) fills the entire 1,500-line ring buffer in minutes. A `--dyno web`-filtered pull over the same budget returned **zero** web lines — any HTTP-level trace of the actual "Generate Now" POST request has already rolled off the buffer. **I cannot confirm from logs alone which user/session tapped the button or exactly when** — the DB-row/RQ-job correlation above (both timestamped `09:16:14`) is the strongest available evidence and is treated as circumstantial-but-solid, not proven identity. Do not read "no errors in the logs" as "nothing went wrong" here — the window simply doesn't reach back far enough.

## Schema/enum/migration state — clean

- `alembic_version` = `pp7q8r9s0t1u` — matches expected HEAD.
- `weekly_therapy_summaries` columns match `models.py` exactly (checked via `information_schema.columns`).
- `processingstatusenum` labels: `PENDING, PROCESSING, COMPLETED, FAILED, PLAIN_TEXT` — UPPERCASE, matching the model's enum member names (SQLAlchemy `Enum(PyEnum)` persists member *names* by default) — **no drift** on this particular enum, despite the general prod-drift precedent.
- `uq_weekly_summary_user_period` constraint present on prod (`pg_constraint` confirms) — the migration's duplicate-guard did not need to skip it.

## Handoff to backend-api / data-analytics

1. **Not a bug in CS-07's generation logic** — both weekly and monthly paths are producing COMPLETED rows correctly. No further fix needed there.
2. **Queue architecture issue** (backend-api + data-analytics, since RQ job wiring spans `app/tasks/` + `app/core/rq_queue.py`): the interactive "Generate Now"/"retry" jobs (`run_weekly_summary_ai_job` and its monthly equivalent) share one unprioritized `"default"` queue and one single-concurrency worker with bulk backfill jobs (hourly cron generation itself, plus its RAG-indexing follow-ups). Recommend either (a) a separate high-priority RQ queue for interactive user-triggered jobs, with the worker listening `rq worker high default` (RQ services queues in listed order), or (b) chunking the hourly bulk-generation cron so it doesn't monopolize the sole worker for tens of minutes at a stretch, or (c) both. Any future large backfill (new cohort, mass retry after a bug fix) will reproduce this exact "stuck" symptom otherwise.
3. **Orphaned queued job**: `run_weekly_summary_ai_job` id `47036fe2-c548-48fa-bab6-31a2f5e0c492` is still sitting in the queue behind the backlog; it will no-op harmlessly when it eventually runs (row already FAILED), but confirms jobs aren't cancelled when their DB row is swept — cosmetically wasteful, not urgent.
4. **FailedJobRegistry has 565 accumulated failures** dating back weeks, never drained — recommend someone (integration-devops or backend-api) look at `mindsync_hourly_monthly_therapy_audit`'s failure today at `09:32:39` specifically (job-level failure despite the 1,752 rows it produced landing fine), and put an eyeball on whether `goal_narrative.regenerate_goal_narratives`'s repeat "Work-horse terminated unexpectedly" failures are a real recurring problem.
5. **FE behavior not verified here** (out of my scope): confirm with flutter-mobile/data-analytics whether the client actually polls through to the FAILED state and offers "retry," or whether it just keeps spinning past a terminal FAILED — that's the other half of "stuck" from the user's perspective.

## Queries run (all read-only, bounded)

All queries executed via `heroku run --no-tty -a mindsync python < script.py` against the live prod Azure Postgres (session started with `SET statement_timeout = 20000`, `db.rollback()` after every block, no `commit()` anywhere). RQ introspection used the app's own `rq_queue`/`redis_client` from the same dyno (read-only registry/queue inspection, no job cancellation or DB mutation). Full script text available in this session's scratchpad if needed for re-run.
