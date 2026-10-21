# Production Push Notification Audit — 2026-07-03

**Auditor:** database-administrator (read-only)
**Scope:** why users get almost no push notifications — deploy state, RQ scheduler state, notification tables, reach (FCM tokens), schedule data, worker/scheduler health.
**Method:** `heroku releases/config/ps/logs` (direct CLI) + `heroku run -a mindsync python < REPL-safe_script.py` (Azure Postgres + RedisGreen, via one-off dyno) + targeted read of `app/services/notification_orchestrator.py`, `app/tasks/notification_orchestrator_job.py`, `app/services/notification_service.py`, `app/tasks/health_check.py`, `Procfile` (read-only, for root-cause tracing only — no files edited). All one-off dynos stopped after use. No DML/DDL executed.

---

## Headline finding (read this first)

**The entire "Notification Moments" + "In-App Insights" framework — the system that is supposed to send post-session reflections, mood-dip alerts, streak celebrations, pattern insights, weekly recaps, achievement unlocks, re-engagement pushes, and (new) therapy-prep reminders — has never fired a single time in production, for any user, since it shipped (~2026-05-15).**

`notification_moments` and `app_insights_shown` both have **0 rows**, full stop. This is not a rate/eligibility problem — it is a **wiring bug**: the plugin generators/detectors self-register into an in-memory singleton via side-effect imports (`import app.services.moments`, `import app.services.insights`) that only happen in `app/main.py` — the **web** dyno's entrypoint. The **worker** dyno (`Procfile`: `worker: rq worker --url $REDISGREEN_URL`) never imports `app.main`; RQ only imports the specific job module by dotted path when it dequeues a job. Neither `app/tasks/notification_orchestrator_job.py` nor anything it imports pulls in `app.services.moments` / `app.services.insights`. Result: in the actual process that executes the jobs, the registries are permanently **empty**.

Verified directly on prod (read-only, no mutation) by importing exactly what RQ imports to run these jobs, in a fresh interpreter:

```
import app.tasks.notification_orchestrator_job   # <- this is all RQ imports to run the job
get_orchestrator().generator_count   -> 0
'app.services.moments' in sys.modules -> False
get_detector().detector_count        -> 0
'app.services.insights' in sys.modules -> False
```

Consequences match every symptom observed below:
- `deliver_due_moments` (every 15 min) and `run_daily_orchestrator` (hourly) both log "Job OK" / no exceptions, because the code path that would create a moment is gated by `if orchestrator.generator_count == 0: skip` (info-level log, not an error) — nothing ever throws, nothing ever gets flagged.
- `run_insight_detection` fires very frequently (dozens of times/hour just from 3 active users' `stats_tab_opened`/`therapy_tab_opened` events) and "Successfully completed" every time — but produces zero `app_insights_shown` rows, same root cause.
- The only push notifications actually reaching users in the last 30 days are the **32 `session_recording` "your summary is ready"** sends in `notification_logs` — a completely separate, directly-invoked send path that doesn't depend on the generator registry.

**Live confirmation, captured during this audit:** the hourly orchestrator's next scheduled tick fired exactly as expected —
```
2026-07-03T17:00:14+00:00 app[worker.1]: default: Notification orchestrator (hourly) (mindsync_hourly_notification_orchestrator)
2026-07-03T17:00:15+00:00 app[worker.1]: Successfully completed Notification orchestrator (hourly) job in 0:00:00.735436s ...
2026-07-03T17:00:15+00:00 app[worker.1]: default: Job OK (mindsync_hourly_notification_orchestrator)
```
**0.735 seconds total runtime** for a job whose code path (`expire_stale_moments` + `purge_expired_insights` + `_load_eligible_users` joining/iterating ~1,720 `user_preferences` rows + per-user scoring) would take meaningfully longer if it were actually evaluating the user base. This duration is exactly what "generator_count == 0 → skip the entire user-selection loop" produces, and matches the process-level test above. Live production evidence and static code tracing agree.

**Handoff to `backend-api`:** import `app.services.moments` and `app.services.insights` (or the two lines from `app/main.py:58-59`) somewhere that actually executes in the RQ worker process — e.g. at the top of `app/tasks/notification_orchestrator_job.py`, or in a `app/tasks/__init__.py` that RQ's module resolution will always touch, or via an RQ `worker_module`/preload hook. Add a boot-time assertion/log (`generator_count > 0`) so this class of bug pages instead of silently no-op'ing for 50 days. This is the single highest-leverage fix available — it turns on 8 of 9 notification types at once.

---

## 1. Deploy state

`heroku releases -a mindsync -n 15`:

| Release | Description | When |
|---|---|---|
| v514 | Deploy `74632f3e` | 2026-07-03 10:02 (~8h before audit) |
| v513 | Deploy `4c2579a2` (MS_3 backend) | 2026-07-03 07:42 |
| v512 | Set `WHISPER_MODEL` config var | 2026-06-25 |
| v511 | Deploy `a3b10498` | 2026-06-22 |
| v510–v501 | recording-pipeline / hero-insight / GCS-config deploys | 2026-06-21–22 |

**MS_3 backend (`4c2579a2`) IS live** (v513/v514, deployed today) — project memory calling this "Heroku deploy PENDING operator approval" is stale as of this audit; it has since been approved and shipped.

`heroku run alembic current -a mindsync` → **`vv2w3x4y5z0a (head)`** — prod is fully migrated, matches the last known chain (recording-chunks-to-Postgres migration). No pending migration debt.

`heroku config -a mindsync` — searched for `NOTIF*`, `RE_ENGAGEMENT*`, `LEGACY*` keys: **none exist**. Notification behavior is governed entirely by code-level `Settings` defaults, not env vars. Confirmed in code: `app/core/config.py:245` → `notification_legacy_jobs_enabled: bool = False` (hardcoded default, no override present). *(DB_URL / REDISGREEN_URL values were not written anywhere beyond ephemeral tool output during this audit and are not reproduced in this report.)*

## 2. RQ scheduler state (Redis, via `rq_scheduler.Scheduler`)

**22 scheduled jobs total, each registered exactly once** — no duplicates, no ghosts. The 2026-05-19 "531 duplicate jobs" incident ([[project_scheduler_cleanup_2026_05_19]]) has **not recurred**; scheduler hygiene is healthy today.

Notification-related jobs, all present and correctly firing on schedule:

| Scheduler id | Function | Cadence | Verified via logs |
|---|---|---|---|
| `mindsync_frequent_moment_delivery` | `deliver_due_moments` | every 15 min | fires on schedule, "Job OK" (16:15, 16:30, 16:45 all observed) |
| `mindsync_hourly_notification_orchestrator` | `run_daily_orchestrator` | hourly | registered, next_run correct; see headline finding for why it's a no-op |
| `mindsync_hourly_health_check_notify` | `notify_health_check_due` | hourly | registered; **gated off** (see §3) |
| `mindsync_hourly_prep_reminder` / `mindsync_hourly_prep_morning_of` | `notify_prep_reminder` / `notify_prep_morning_of` | hourly | registered; **gated off** (see §3) |
| `mindsync_daily_notification_log_cleanup` | `cleanup_notification_logs` | daily 03:00 | registered |

Conclusion: **the scheduling layer is not the problem.** Every job that should run, does run, exactly once, on time.

## 3. Volume actually sent (30-day window + all-time)

Schema drift note: prod enums are UPPERCASE (`moment_status_enum`: `PENDING, SENT, OPENED, DISMISSED, ACTED, EXPIRED`; `moment_type_enum`: `POST_SESSION_REFLECTION, MOOD_DIP_ALERT, STREAK_CELEBRATION, PATTERN_INSIGHT, THERAPY_PREP, REFLECTION_INVITATION, WEEKLY_RECAP, ACHIEVEMENT_UNLOCK, RE_ENGAGEMENT`) — consistent with known drift, not a factor here since the tables are simply empty.

| Table | Row count (all-time) |
|---|---|
| `notification_moments` | **0** |
| `app_insights_shown` | **0** |
| `notification_logs` | 32 |

`notification_logs` (the only non-empty send record) — **by type**: 100% `session_recording` (32/32). **By status**: 31 `sent`, 1 `token_invalid`. **By day** (all-time, not just 30d — table only has 32 rows ever): scattered single-digit counts from 2026-06-03 through 2026-07-03, last real send **2026-07-03 16:23:52 UTC**. This table is written by the recording-summary-ready push, a direct-call path unrelated to the Moments framework — it is not evidence the Moments/legacy notification system works.

Three additional legacy hourly jobs (`notify_health_check_due`, `notify_prep_reminder`, `notify_prep_morning_of`) are scheduled and firing, but each starts with:
```python
if not settings.notification_legacy_jobs_enabled:   # hardcoded False, no env override
    return {"status": "skipped", "reason": "legacy_disabled"}
```
so they no-op every hour too — consistent with project memory flagging this as "likely an unintended gate" ([[project_scheduler_cleanup_2026_05_19]]): prep/health-check reminders were never actually migrated to a working Moments-framework equivalent, yet the legacy path that used to serve them was switched off anyway.

Separately, `crud.get_users_eligible_for_notification()` (`app/crud/crud.py:497-552`) has a genuine `str.format()` bug: the SQL template contains `\d{1,2}` / `\d{2}` regex quantifiers inside a string that is later passed through `.format(notification_type, notification_type)` — every `{...}` in the whole string gets format-parsed, so this raises `KeyError: '1,2'` whenever called. **This is currently dead code** — its only two callers (`notify_journal_reminder`, `notify_inactivity_reminder`) are both deprecated stubs, no longer registered in the scheduler at all (Faza 4 cutover) — but flag it now so it isn't silently reawakened if anyone re-enables `notification_legacy_jobs_enabled` or copies this pattern.

## 4. Reach capacity

| Metric | Value |
|---|---|
| Total users | 1,730 |
| Users with ≥1 FCM token | **232 (13.4%)** |
| `user_preferences` rows | 1,722 |
| `notification_enabled` = True / False | 1,720 / 2 |
| `re_engagement_push` = True / False | 1,719 / 3 |
| `notification_interests` — proper array (e.g. `["REFLECTIONS","INSIGHTS",...]`) | 147 (8.5%) |
| `notification_interests` — malformed `{}` object (not a list) | **1,575 (91.5%)** |
| Active users last 14 days (`conversations.created_at`) | 14 (0.8%) |
| Active users last 14 days (`messages` join) | 14 (0.8%) |
| Users created last 14d / 30d | 34 / 76 |

Two additional, independently real findings here:

- **FCM reach is only 13.4% of the user base.** Even with the wiring bug fixed, at most ~232 users are reachable by push today. Worth a separate flutter-mobile/integration-devops look at the token-registration flow and permission-prompt funnel.
- **`notification_interests` is the wrong JSON shape for 91.5% of rows.** The column is meant to hold a JSON array of up to 6 category strings (`models.py:196-198` docstring: `list[str]`), and the orchestrator's `_get_allowed_categories()` (`notification_orchestrator.py:584-618`) explicitly branches on `isinstance(col_val, list)`. A value of `{}` (empty JSON *object*, not array) is neither a `list` nor a `str`, so it falls through to a bare `except Exception: return None` a few lines later — which happens to be treated as "no filter, allow all" — **so this specific shape bug is currently benign** (fails safe, not closed) rather than a second blocker. Still worth a fix: it means the CRIT-05 backfill described in project memory ("wszyscy backfilled z 6 kategoriami") either never ran against this column or targeted the wrong default (`{}` instead of `[...]`) for the bulk of the pre-existing user base; only users who set/re-saved preferences after some point ended up with the correct array. Flag to `backend-api` to confirm the true default/backfill statement in migration `gg7h8i9j0k1l` / `mm3n4o5p6q7r`.
- **Active-user base is tiny (14/1730, 0.8%, in 14 days).** This caps the addressable population for activity-triggered generators (post-session reflection, mood dip, streak, pattern) almost to zero regardless of the wiring bug — but does **not** explain the RE_ENGAGEMENT gap, since that generator specifically targets the other 99.2% (inactive users) and is explicitly exempted from the interest filter in code (`_INTEREST_FILTER_EXEMPT` includes `RE_ENGAGEMENT`, `THERAPY_PREP`, `POST_SESSION_REFLECTION`). RE_ENGAGEMENT should have produced pushes for a large fraction of the ~230 FCM-reachable, notification-enabled, inactive users over 50 days — it produced **zero**, consistent with the headline wiring bug being the true blocker, not eligibility logic.

## 5. Pre/post-session reminder schedule data

`user_preferences` scheduling fields (n=1,722):

| Field | Filled | % |
|---|---|---|
| `next_session_date` | **0** | **0%** |
| `therapy_schedule` (legacy free-text/JSON) | 114 | 6.6% |
| `custom_therapy_sessions` | 5 | 0.3% |
| `therapy_frequency` set (weekly/biweekly/custom) | 1,722 | 100% |

**`next_session_date` — the column the orchestrator's schedule-driven pass and `notify_prep_reminder` both read as the scheduling anchor — is populated for 0 of 1,722 users.** Everyone has a *frequency* (weekly/biweekly/custom — effectively 100% filled), but nobody has an actual anchor *date* to compute "your next session is in 24h" from. `therapy_schedule` (the older free-text field some of this logic falls back to) covers only 6.6%.

This is a second, independent reason pre/post-session reminders (`THERAPY_PREP` moment type, `notify_prep_reminder`/`notify_prep_morning_of` legacy jobs) would produce near-zero output even if the wiring bug and the legacy-flag gate were both fixed today: there's essentially no schedule data to act on. **Key-present-but-value-null pattern** — `therapy_frequency` (the "how often" half of scheduling) is fully captured, `next_session_date` (the "when exactly" half) is not, for any user. Handoff to `backend-api`/`flutter-mobile`: confirm whether the UI ever collects/persists a concrete next-session date (vs. only a cadence), and whether `_util_compute_next_session_date()` (`notification_service.py`) is expected to derive it dynamically rather than read a stored column — if so, the orchestrator's `_load_schedule_users()` filter on `therapy_schedule IS NOT NULL` (only 114 users) is itself excluding ~93% of users who might otherwise be schedulable via frequency alone.

## 6. Worker/scheduler health

`heroku ps -a mindsync`:
```
scheduler.1: up 2026/07/03 10:02:59 (since MS_3 deploy, ~8h)
web.1:       up 2026/07/03 10:03:08
worker.1:    up 2026/07/03 10:02:59
```
All three dynos up and healthy since the MS_3 deploy this morning — no crash-looping, no restarts. This matters: the notification gap is **not** an infra-outage story. The infrastructure (scheduler cron, RQ worker process, Redis, DB) is fully healthy; the bug is a Python import/registration gap inside otherwise-healthy processes.

---

## Summary of findings, ranked

1. **[Critical, root cause] Moment generators / insight detectors never register in the RQ worker process** — `app.services.moments` / `app.services.insights` are only imported by `app/main.py` (web dyno). The worker dyno (which actually runs `run_daily_orchestrator`, `deliver_due_moments`, `run_insight_detection`) never imports them, so both singleton registries are permanently empty (`generator_count == 0`, `detector_count == 0`, verified directly on prod). Every related job logs success and does nothing. This alone explains `notification_moments` = 0 rows and `app_insights_shown` = 0 rows since the system shipped ~50 days ago. **→ backend-api, highest priority.**
2. **[High] `notify_health_check_due` / `notify_prep_reminder` / `notify_prep_morning_of` are hourly-scheduled but permanently gated off** by `notification_legacy_jobs_enabled=False` (hardcoded, no env override) even though they were never actually superseded by a working replacement (see #1 for THERAPY_PREP). **→ backend-api: decide intentionally — re-enable these three specifically, or ship a working THERAPY_PREP generator path (blocked on #1 anyway).**
3. **[High] `next_session_date` is 0% filled** across 1,722 `user_preferences` rows — no anchor date exists for any user to compute "session in 24h" from, independent of #1/#2. **→ backend-api + flutter-mobile: confirm whether this is meant to be user-entered or derived; today it's neither.**
4. **[Medium] FCM token coverage is 13.4%** (232/1,730) — even a fully-fixed notification system can only reach ~1 in 7 users today. **→ flutter-mobile/integration-devops: audit token registration + permission-prompt funnel.**
5. **[Low, currently benign] `notification_interests` holds `{}` (wrong JSON shape) for 91.5% of rows** instead of the documented `list[str]`. Fails safe today (falls through to "no filter") but is real data drift from the claimed CRIT-05 backfill. **→ backend-api: confirm true default/backfill in migrations `gg7h8i9j0k1l`/`mm3n4o5p6q7r`.**
6. **[Low, dead code] `get_users_eligible_for_notification()` has a `str.format()` KeyError bug** (regex `{1,2}`/`{2}` quantifiers collide with `.format()` placeholders). Currently unreachable (only called by two deprecated, unscheduled stub functions) — flag so it isn't silently reawakened. **→ backend-api, low priority cleanup.**

Not a factor: RQ scheduler hygiene (clean, 22 jobs, no duplicates), dyno health (all up), migration state (fully current, `vv2w3x4y5z0a`), MS_3 deploy status (confirmed live).
