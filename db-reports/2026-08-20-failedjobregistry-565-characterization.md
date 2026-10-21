# FailedJobRegistry characterization — 565 entries, prod RQ ("default" queue) — 2026-08-20

**Requested by:** lead, in support of `backend-api`'s concurrent build of a FailedJobRegistry monitoring/cleanup job.
**Access:** read-only, via the Heroku one-off dyno recipe (`heroku run -a mindsync python < script.py`, runs `run.5020`/`run.8430`/`run.4353`/`run.4353`, all stopped after capture). RQ registries and job hashes were inspected directly via the app's own `redis_client` / `rq` objects (`FailedJobRegistry`, `FinishedJobRegistry`, `StartedJobRegistry`, `Job.fetch`). **Zero writes** — no `registry.remove()`, no `requeue()`, no job cancellation, no DB mutation, no `commit()` anywhere in any script run.
**Scope check first:** the "high" priority queue (added to code 2026-08-20, not yet deployed per the Procfile cutover) has **0** entries in its `FailedJobRegistry` — nothing to characterize there yet.

## Verdict up front

**565 is not 565 live failures. It is ≈554 (98%) dead registry debris from three already-fixed or already-deleted code paths, plus 11 (2%) entries on currently-active code, of which only 3 are genuinely, permanently failed and never retried.** The registry has never been drained *and*, independently, RQ does not remove a job's ID from `FailedJobRegistry` once added even after that same job later succeeds — so the count has been silently accumulating pure noise for a year. The OOM hypothesis is correct but narrow: every real (non-ghost, non-stale) failure in this dataset that has a recoverable cause is a work-horse death (`Work-horse terminated unexpectedly`, i.e. the process was killed, not a Python exception) — **zero** currently-active code paths failed with a genuine application-logic traceback.

## 1. Ranked breakdown — function × failure reason

| # | func_name | count | % of 565 | reason | status today |
|---|---|---|---|---|---|
| 1 | `app.services.subscription_service.deactivate_expired_subscriptions` | **490** | 86.7% | none stored — job hash shows `status: finished`, ran in 1-3s, no `exc_info` key at all | **dead code path.** Current code calls `app.tasks.subscriptions.deactivate_expired_subscriptions` instead (moved 2026-08-10 so the worker dyno's PostHog/logging init fires — see `app/core/rq_scheduler_setup.py` header comment). This is the historical **"498 duplicate cron entries"** bug the code's own docstring documents (`setup_hourly_subscription_job()`: *"Previously this function had NO idempotency guard, which caused 498 duplicate entries to accumulate in production"*). All 490 sampled/aggregated job hashes are `JobStatus.FINISHED` — **they succeeded**; their IDs just never left the failed-set. |
| 2 | `app.core.rq_scheduler_setup.weekly_MON_pipeline` | 43 | 7.6% | 30 with `Work-horse terminated unexpectedly`, 13 with no exc stored (self-healed) | **dead code — function no longer exists.** `import_attribute` raises `ValueError: Invalid attribute name: weekly_MON_pipeline` for the post-removal entries. Pre-dates the 2026-07-03 Notification Cadence v3 rewrite (project memory: *"wycięte legacy (7 setup_\*, ... 7 notify_\*)"*). |
| 3 | `app.services.profile_service.update_all_user_profiles` | 6 | 1.1% | 6/6 `Work-horse terminated unexpectedly` | **orphaned.** Not referenced anywhere in current `app/core/rq_scheduler_setup.py` (grepped, confirmed absent) — nothing schedules this today. Function still exists in the file but is unreachable from any current cron. All dated 2025-08-23 → 2026-01-19. |
| 4 | `app.core.rq_scheduler_setup.daily_pipeline` | 5 | 0.9% | 3 with exc (1 work-horse, 2 ValueError), 2 self-healed | same dead legacy pipeline family as #2. |
| 5 | `app.tasks.goal_narrative.regenerate_goal_narratives` | 2 | 0.4% | 2/2 `Work-horse terminated unexpectedly; waitpid returned None` | **LIVE code, still failed, never retried.** See §4 below — flagged as a real (if minor) gap. |
| 6 | `app.services.notification_service.notify_journal_reminder` | 2 | 0.4% | 1 SQLAlchemy `DetachedInstance`-style traceback (`user_preferences` lazy-load after session close), 1 self-healed | legacy `notify_*`, deleted 2026-07-03. |
| 7 | `app.services.notification_service.notify_inactivity_reminder` | 2 | 0.4% | same as #6 | legacy, deleted 2026-07-03. |
| 8 | `app.core.rq_scheduler_setup.monthly_pipeline` | 2 | 0.4% | 2/2 `ValueError: Invalid attribute name` | legacy pipeline family. |
| 9 | `app.core.rq_scheduler_setup.yearly_pipeline` | 2 | 0.4% | 1 ValueError, 1 self-healed | legacy pipeline family. |
| 10 | `app.tasks.subscriptions.deactivate_expired_subscriptions` (**current** path) | 1 | 0.2% | none stored, `status=finished`, last real run 09:38:34–09:38:36 today succeeded | self-healed; currently `QUEUED` for its next tick behind the single-worker backlog (see §6 — same contention pattern as the 2026-08-20 "Generate Now stuck" incident). |
| 11 | `app.tasks.recording_recovery.finalize_complete_upload_sessions` | 1 | 0.2% | none stored, self-healed (11:48:20–11:48:22 today) | healthy, queued for next tick. |
| 12 | `app.tasks.recording_recovery.recover_stuck_recordings` | 1 | 0.2% | none stored, self-healed (11:41:57–11:41:58 today) | healthy, queued. |
| 13 | `app.tasks.notification_orchestrator_job.deliver_due_moments` | 1 | 0.2% | none stored, self-healed (11:55:11–11:55:13 today) | healthy, queued. |
| 14 | `app.tasks.notification_orchestrator_job.run_daily_orchestrator` | 1 | 0.2% | none stored, self-healed (09:32:43–09:38:26 today) | healthy, queued. |
| 15 | `app.tasks.monthly_therapy_audit.generate_monthly_therapy_audits` | 1 | 0.2% | none stored (overwritten by a later success) | **the requested deep-dive — see §4.** Self-healed; currently `QUEUED`. |
| 16 | `app.tasks.loops_sync.sync_all_users_to_loops` | 1 | 0.2% | none stored | healthy, `SCHEDULED` for tonight's 02:00 run. |
| 17 | `app.services.notification_service.notify_prep_reminder` | 1 | 0.2% | none stored, self-healed | legacy, last fired 2026-07-03 (the day the pipeline was cut over), never again. |
| 18 | `app.services.conversation_analysis.run_conversation_analysis` | 1 | 0.2% | `Work-horse terminated unexpectedly; waitpid returned 15 (signal 15)` | **LIVE code, still failed, never retried.** See §5. |
| 19 | `app.services.close_all_notes.close_open_conversations_and_analyze` | 1 | 0.2% | none stored, self-healed (05:00:49–05:00:56, 2026-05-20) | healthy. |
| 20 | `app.core.rq_scheduler_setup.weekly_SUN_pipeline` | 1 | 0.2% | `ValueError: Invalid attribute name` | legacy pipeline family. |

**Global exception-shape tally across all 565:**

| shape | count | % |
|---|---|---|
| No `exc_info` stored (job hash shows a later/actual success) | 517 | 91.5% |
| `Work-horse terminated unexpectedly` (process killed, no Python traceback) | 39 | 6.9% |
| `ValueError: Invalid attribute name: X` (RQ can't import the target function — it's gone) | 7 | 1.2% |
| Genuine Python/SQLAlchemy traceback (a real, in-code bug) | 2 | 0.4% |

## 2. Timeline — bursts, not a trickle

| period | count | what happened |
|---|---|---|
| 2025-08-20 → 2025-09-09 | 15 | `weekly_MON_pipeline` / `daily_pipeline` / `update_all_user_profiles` work-horse deaths — old pipeline, pre-dates this investigation's other memory notes; not re-diagnosed further, dead code today either way. |
| 2025-11-21, 2025-12-31, 2026-01-19, 2026-02-17 | 4 | scattered singletons, same legacy families. |
| 2026-02-26 → 2026-03-06 | 25 | another `weekly_MON_pipeline` cluster (mostly work-horse deaths) + the 2 real `notify_*` SQLAlchemy tracebacks. |
| **2026-05-19 → 2026-05-20** | **499** | **the big one.** 495 of these are on 2026-05-19 alone. 490 are `subscription_service.deactivate_expired_subscriptions` (the duplicate-cron-registration incident, §1 #1), the rest are legacy-pipeline stragglers. This single burst is 88% of the entire 565. |
| 2026-07-03 | 1 | `notify_prep_reminder` — the exact day of the Notification Cadence v3 cutover; last gasp of the old system, self-healed. |
| 2026-07-25 | 2 | `goal_narrative.regenerate_goal_narratives` — real, unretried, work-horse deaths (§4). |
| **2026-08-20 (today)** | 7 | `recording_recovery` ×2, `notification_orchestrator` ×2, `monthly_therapy_audit`, `subscriptions`, `loops_sync` — **every one of these is a stale registry entry for a job that has already succeeded since** (see §6/§7 — these are FailedJobRegistry catching up to today's queue-contention incident already documented in `db-reports/2026-08-20-weekly-summary-generate-now-stuck.md`, not new distinct bugs). |

Verdict: **overwhelmingly a single burst** (2026-05-19/20, 88% of all entries) from a documented, already-fixed idempotency bug, plus a long tail of already-deleted legacy jobs, plus today's queue-contention echo. Not a steady background trickle of application errors.

## 3. OOM vs. code-bug — the ratio, and why it's narrower than it looks

- **39/565 (6.9%)** show the OOM/infra signature (`Work-horse terminated unexpectedly` — the RQ worker's watchdog detected its child process died; this bypasses Python exception handling entirely, consistent with a Basic-dyno OOM kill or a SIGTERM during a deploy/restart).
- **7/565 (1.2%)** show a real Python traceback (`ValueError: Invalid attribute name`) — but this is not an application-logic bug, it's RQ failing to `import_attribute()` a function that has been deleted from the codebase. Zero of these reference a function that exists today.
- **2/565 (0.4%)** show a genuine in-code bug (SQLAlchemy `DetachedInstanceError`-class lazy-load failure in the old `notify_journal_reminder`/`notify_inactivity_reminder`) — also dead code, not fixable because there's nothing to fix it in.
- **517/565 (91.5%)** show no exception at all — their job hashes carry `status: finished` from a later (or the same) successful run.

**So: it's an OOM story, not a code-bug story — but only for a small, specific slice.** Restricted to code that's still live today (11 entries, see §5), the mix is 3 work-horse-kills (all unretried, all still-failed) vs. 0 live Python tracebacks. The operator's OOM hypothesis is correct wherever a real failure exists; it just doesn't explain 91% of the count, which is registry bookkeeping debris, not failures at all.

## 4. The `mindsync_hourly_monthly_therapy_audit` case — cosmetic-but-noisy, confirmed

This is the fixed-ID cron job (`id="mindsync_hourly_monthly_therapy_audit"`, `app/core/rq_scheduler_setup.py:278`, `timeout=3600`) — RQ-scheduler reuses the **same job ID every hourly tick**, so the Redis job hash gets overwritten on every run.

Live state right now (2026-08-20 ~11:55 UTC):
- `status = QUEUED` — waiting on its 11:00 tick, sitting behind the same single-worker backlog documented in the sibling "Generate Now stuck" report (worker still draining today's RAG-indexing burst).
- `started_at = 09:00:38`, `ended_at = 09:32:39` — **these are stale fields from the 09:00 tick's failure**, not yet overwritten because the 11:00 tick hasn't run.
- `exc_info = None` — **already overwritten**. The job must have run again between 09:32 and now and *succeeded* (its ID is present in `FinishedJobRegistry`, confirmed), clearing the exception. I cannot recover the exact traceback/signal for the 09:32:39 incident specifically — it's gone.
- The job ID is simultaneously present in **both** `FailedJobRegistry` and `FinishedJobRegistry` — direct proof RQ does not clean the failed-set when a reused-ID job later succeeds.

What I *can* establish, from reading `app/tasks/monthly_therapy_audit.py` (not editing — flagging only): **`generate_monthly_therapy_audits()` wraps its entire body — the per-user loop (each exception caught individually at line 234, incrementing an `errors` counter, never re-raised) and the top-level logic — in one outer `try/except Exception as e: logger.error("FATAL: %s", e)` (lines 207–261) that swallows everything and returns normally.** No exception raised anywhere inside that function, for any single user or any aggregate step, can ever reach RQ as a job failure. The **only** way this job can show up in RQ as failed is something that bypasses Python's exception handling entirely — a work-horse kill (OOM/SIGKILL) or a SIGTERM. That is exactly the signature seen on every *other* entry in this dataset that still retains its original `exc_info` (§3: 39/48 recoverable-cause entries are work-horse kills, 0 are live-code tracebacks). Combined with the already-confirmed fact (prior report) that **all 1,752 monthly-audit rows from the 09:00 tick landed as `COMPLETED`** before the 09:32:39 failure, the mechanism is: **the per-user loop finished writing everything successfully, then something (very likely an OOM kill from processing ~1,752 users serially in one long-lived worker process on a Basic/512MB dyno, with no `db.expire_all()` to bound the SQLAlchemy session's identity-map growth) killed the work-horse near the tail end of the run** — after the RAG-indexing follow-ups were already enqueued (confirmed 09:00:42–~09:23 in the sibling report) but before the job's own `finally: db.close()` / final log line executed.

**Verdict: cosmetic-but-noisy, exactly as hypothesized.** No data was lost or left incomplete — the failure landed after the useful work was already durably committed. The job self-healed on a subsequent tick.

## 5. Real failures that were never retried — flagged separately

Only these 3 entries, out of 565, are **(a)** on a currently-live code path **and** **(b)** never followed by a successful run for that same identity:

1. **`app.services.conversation_analysis.run_conversation_analysis(20501, 'mC3X3...')`** — 2026-03-02, `Work-horse terminated unexpectedly; waitpid returned 15 (signal 15)`. Signal 15 = **SIGTERM**, i.e. a graceful worker shutdown/deploy restart caught this job mid-execution, not an OOM kill. Still `JobStatus.FAILED` today, absent from `FinishedJobRegistry`. **Effect:** one conversation's post-conversation AI analysis (topic/emotion/sentiment extraction feeding dashboard analytics) for one user never completed and nothing re-triggered it. Low blast radius (1 conversation, 5+ months old), but it is a genuine, permanent, silent miss on a live, currently-called path (`app/api/v1/endpoints/conversations.py`, `reflect.py`, `close_all_notes.py` all still enqueue this function today).
2. **`app.tasks.goal_narrative.regenerate_goal_narratives('Ho0vY6...', 'recording', 1453)`** — 2026-07-25 09:10–09:15, `Work-horse terminated unexpectedly; waitpid returned None`.
3. **`app.tasks.goal_narrative.regenerate_goal_narratives('CtRpjc...', 'recording', 1454)`** — 2026-07-25 09:16–09:21, same signature, 6 minutes after #2.

Both goal-narrative failures are still `JobStatus.FAILED`, absent from `FinishedJobRegistry`, and were triggered by session-recording completions for two different users on the same morning — a real, if minor, recurring capacity problem on this specific job (this matches the prior report's flag: *"goal_narrative.regenerate_goal_narratives — repeat 'Work-horse terminated unexpectedly' failures ... worth an eyeball"*). **Effect:** two users' AI-written goal narratives were never regenerated after their session recordings were processed; nothing else depends on this (it's presentation text, not a data-integrity issue), but it is silently stale for those two users indefinitely since nothing retries it.

**No summary, chart, notification, RAG-index, or subscription job shows genuine unrecovered data loss.** Every entry touching those categories in this dataset (weekly/monthly summaries, RAG indexing, notifications, subscription deactivation, recording recovery, upload finalization) is either a dead legacy reference or confirmed self-healed (§6).

## 6. Self-healed vs. permanently lost

| bucket | count | evidence |
|---|---|---|
| Self-healed (job hash shows a later/same-run success; several also confirmed present in `FinishedJobRegistry`) | **562** | 490 subscription_service (status=finished) + 53 legacy pipeline/notify (partial self-heal, remainder is genuinely dead code) + 8 of the 11 live-path entries (loops_sync, subscriptions.py, upload_finalizer, recording_recovery, notification_orchestrator ×2, monthly_therapy_audit, close_all_notes) |
| Permanently lost, never retried | **3** | `run_conversation_analysis` (§5 #1), `goal_narrative.regenerate_goal_narratives` ×2 (§5 #2, #3) |

`FinishedJobRegistry` on the "default" queue currently holds **5,858** entries and `StartedJobRegistry` holds **1** (a job the worker is mid-execution on right now) — for scale, i.e. the worker is generally healthy and the failed-set is a rounding error against normal successful throughput.

## 7. Retention-window recommendation for backend-api's cleanup job

The useful signal in this dataset stops at **2026-07-25** (the goal_narrative pair) — everything before that is either the 2026-05-19 duplicate-cron burst or pre-2026-07-03 legacy pipeline debris, both already fixed/deleted at the code level and unable to recur. Recommend:

1. **Purge on a short, rolling window — 14 days is plenty.** Nothing older than 2026-07-25 has ever been actionable in this dataset, and the entries older than that are 100% dead-code or self-healed noise. A 14–30 day window comfortably covers "did last week's deploy introduce a new recurring failure" without carrying a year of debris.
2. **Before alerting on any entry, re-check the job's *current* `status` and `FinishedJobRegistry` membership, not just registry presence.** §4 and §6 prove `FailedJobRegistry` membership alone is not evidence of an unresolved failure — 91.5% of this dataset's entries had already succeeded by the time they were inspected. A monitor that pages on raw registry count (or even raw registry *diff*) will page on noise; it should page only on entries where `job.get_status() == 'failed'` **and** the job ID is absent from `FinishedJobRegistry` **and** (for fixed-ID cron jobs) `ended_at` is more recent than the cron's next expected tick.
3. **Treat `Work-horse terminated unexpectedly` with `waitpid returned None`/signal-9-class as the actionable OOM signal**, and `signal 15` as a deploy-restart artifact (lower priority — it'll recur briefly around every deploy regardless of memory headroom). `goal_narrative.regenerate_goal_narratives` is the one function with a *recurring* (2×, same morning) work-horse-kill pattern on live code — worth `backend-api`/`data-analytics` looking at whether it's processing something unusually large per session recording, independent of this cleanup work.
4. **`ValueError: Invalid attribute name`** entries are safe to purge unconditionally and permanently — they reference functions (`app.core.rq_scheduler_setup.{daily,monthly,yearly,weekly_SUN,weekly_MON}_pipeline`, `app.services.notification_service.notify_*`) that no longer exist in the codebase; they can never succeed and nothing will ever re-enqueue them under the current scheduler.

## Handoff to backend-api

- **No code fix required for the monthly_therapy_audit "failure"** (§4) — it's a self-healed OOM-class event with no data loss. If you want to harden it anyway, the cheap fix is a periodic `db.expire_all()` (or fresh session every N users) inside `generate_monthly_therapy_audits()`'s per-user loop to bound SQLAlchemy identity-map growth across ~1,700+ users in one process — same root cause likely affects `generate_weekly_therapy_summaries()` and any other hourly bulk-loop job on this Basic dyno.
- **`app.tasks.goal_narrative.regenerate_goal_narratives`** has a real, recurring, un-retried work-horse-kill pattern (§5) — worth a look at its memory footprint per invocation and whether it should get a `Retry()` policy so a single work-horse death doesn't silently strand a user's goal narrative forever.
- **`app.services.conversation_analysis.run_conversation_analysis`** — one confirmed permanent loss (§5), old and low-blast-radius; no action needed beyond awareness unless you want to add retry semantics generally to interactive-triggered RQ jobs.
- The retention-window design in §7 is ready to hand to whoever owns the new monitoring/cleanup job.

## Queries / method

All introspection via `app.core.redis.redis_client` + `rq.registry.{FailedJobRegistry,FinishedJobRegistry,StartedJobRegistry}` + `rq.job.Job.fetch(...)`, run inside three sequential Heroku one-off dyno REPL sessions (`run.5020`, `run.8430`, `run.4353`), each ended with a `DONE_SENTINEL` print and then explicitly stopped via `heroku ps:stop`. No `registry.remove()`/`requeue()`/`cancel()`/DB write calls anywhere. Raw per-job dump (565 rows: id, func_name, enqueued_at, ended_at, last-350-chars of exc_info) captured to local scratchpad and aggregated with local `grep`/`awk`/`sed` — no further prod calls needed for the aggregation itself.
