# CS-07 — Weekly/Monthly summaries "Generate now" does nothing — prod root-cause diagnosis

**Date:** 2026-08-19
**Scope:** MSV3.3.Fix.1 CS-07 (read-only diagnosis only, no code/DDL changes made)
**Access:** Heroku one-off dynos (`heroku run -a mindsync python < script.py`), read-only `SELECT` / `information_schema` only, `SET TRANSACTION READ ONLY`. Both dynos stopped after use (`run.7408`, `run.9167`).

## TL;DR

**Root cause confirmed, precisely located, and it is a schema-drift bug, not a dyno or migration problem.** `users.created_at` is `timestamp without time zone` in prod (naive), while the model declares `DateTime(timezone=True)` (aware) and the window-boundary helper (`get_calendar_week_range_utc`/`get_calendar_month_range_utc`) always returns timezone-aware datetimes. The shared helper `crud.adjust_period_start_for_signup(period_start, period_end, user_created_at)` compares `user_created_at > period_end` — naive vs. aware — which raises `TypeError: can't compare offset-naive and offset-aware datetimes`.

This function is called by **all four** entry points to the pipeline: the hourly weekly cron, the hourly monthly cron, the manual weekly `POST /generate`, and the manual monthly `POST /generate`. All four hit it, on every user, every time. Result: **`weekly_therapy_summaries` and `monthly_therapy_audits` are both completely empty in prod — zero rows, ever** — not one row has been created since the 14.08 rebuild shipped (15.08 deploy), including Darek's 18.08 manual taps. This is not "stuck PROCESSING rows" or "dynos down" — it is 100% prep-phase failure before any row is ever written.

Ranked against the spec's 6 hypotheses: **none of them is the primary cause as stated**; the closest is #3 ("other request-path failures... exception in prep"), which is confirmed and now root-caused exactly. #1 (dynos down) and #2 (stuck PROCESSING dead end) are refuted by current evidence. #6 (3600s timeout kill) is refuted — the job finishes in ~10s because every user fails fast. #4/#5 are moot (nothing ever reaches persistence or the response body far enough to matter).

---

## 1. Deployed commit + dyno formation

```
heroku releases -a mindsync -n 8
```
| Release | Commit | Deployed |
|---|---|---|
| **v541 (current)** | `8dd329d1` | 2026-08-19 10:16 (~9-10h before this check) |
| v540 | `c1334e8f` | 2026-08-18 12:38 |
| v539 | `97ef3b0f` | 2026-08-18 08:44 |
| v538 | `91638ce5` | 2026-08-18 07:27 |
| v537 | `a31c954a` | 2026-08-18 07:21 |
| v536 | `a3a40869` | 2026-08-16 14:57 |
| v535 | `2d827fb9` | 2026-08-16 14:44 |
| v534 | `4bb9b2c8` | 2026-08-15 19:20 |

`git merge-base --is-ancestor 971f182 HEAD` on local `MindSync` (branch `main` @ `8dd329d`, clean) → **YES**, confirmed ancestor. The MSV3.3 backend batch (`971f182`, the 14.08 weekly/monthly rebuild) is included in what's running on prod right now (v541).

```
heroku ps -a mindsync
```
```
scheduler.1: up 2026/08/19 10:16:54 +0200 (~9h ago)
web.1:       up 2026/08/19 10:16:51 +0200 (~9h ago)
worker.1:    up 2026/08/19 10:16:44 +0200 (~9h ago)
```
All three dynos single-instance, Basic, **up**, uptime matches today's v541 deploy restart. **Spec hypothesis #1 (worker/scheduler scaled to 0 or crash-looping) is refuted for the current state.** (We cannot retroactively confirm dyno health for the 15.08–19.08 window from `heroku ps`, but it's moot — see §4, the bug fires unconditionally regardless of dyno uptime.)

## 2. Alembic migration state

```sql
SELECT version_num FROM alembic_version;
```
→ `pp7q8r9s0t1u`

Local `MindSync/alembic/versions/` chain ends at `pp7q8r9s0t1u_fix_granted_via_backfill_date_coercion.py` — this **is** the current single head (no file after it in the chain `... → nn5o6p7q8r9s → oo6p7q8r9s0t → pp7q8r9s0t1u`). **Prod migration state matches local HEAD exactly — no migration debt, no lag.** This also confirms `ll3m4n5o6p7q` (therapist_questions) and `mm4n5o6p7q8r` (moment_id) — both named in the spec as must-be-applied — are applied, being ancestors of the current head.

`weekly_therapy_summaries` and `monthly_therapy_audits` **table schemas themselves are correct** in prod (see §3) — the drift is isolated to `users.created_at` / `users.last_login`, not the summary/audit tables.

## 3. Row states — both tables are completely empty

```sql
SELECT count(*), min(created_at), max(created_at) FROM weekly_therapy_summaries;  -- 0  None  None
SELECT count(*), min(created_at), max(created_at) FROM monthly_therapy_audits;    -- 0  None  None
```

Both tables have **zero rows, full stop** — not "zero recent rows," zero ever. Consequently every other row-level check is vacuous but confirms the same thing:

- Counts by `processing_status`: no rows in either table (nothing to group).
- Stuck `PROCESSING` rows older than 15 minutes: none in either table (none exist at all).
- `FAILED` rows in the last 7 days: none in either table.
- Rows created on 2026-08-18 (Darek's manual test window): **none** — his "Generate now" taps did not create even a `PROCESSING` row.
- NULL-integrity check on `id`/`data_window_start`/`data_window_end`/`processing_status`/`created_at`/`updated_at`: `0 0 0 0 0 0` for both tables (vacuously — no rows to violate anything).

`processing_status` enum labels in prod: `PENDING, PROCESSING, COMPLETED, FAILED, PLAIN_TEXT` — this matches the Python enum's member **names** exactly (SQLAlchemy's default `Enum(PyEnum)` behavior uses member names as PG labels); **not** an instance of the known UPPERCASE-drift problem, just normal native-enum behavior. No drift risk here.

`weekly_therapy_summaries` / `monthly_therapy_audits` column types (information_schema): `data_window_start`, `data_window_end`, `created_at`, `updated_at` are all `timestamp with time zone` in prod, matching the model declarations exactly. **The summary/audit tables are schema-clean.**

## 4. The actual bug — confirmed live in worker logs, then root-caused in code, then confirmed against prod schema

### 4a. Live evidence the cron fires and fails 100% of the time

```
heroku logs --dyno worker -n 1500 -a mindsync
```
The most recent hourly weekly-summary cron tick (2026-08-19 17:09:32 UTC — i.e. today, well after the current v541 boot) processed the **entire** eligible population and logged, for essentially every one of them:

```
ERROR app.tasks.weekly_therapy_summary: [WEEKLY_THERAPY_SUMMARY] Error for user <uid>: can't compare offset-naive and offset-aware datetimes
```

...ending with:

```
INFO app.tasks.weekly_therapy_summary: [WEEKLY_THERAPY_SUMMARY] Done: generated=0 skipped=0 errors=1798
```

`1798` errors = the **entire** eligible population (see §4c). `generated=0`. The job completed in ~10.3 seconds (RQ's own "Successfully completed... job in 0:00:10.313073s") — fast, because every single user fails synchronously on this TypeError before any AI call is ever attempted. **This directly refutes spec hypothesis #6** (hourly cron killed mid-loop by the 3600s timeout) — the loop finishes fine, it just does nothing useful. The 1500-line log window was entirely consumed by this one run's error spam, so it wasn't possible to see whether the monthly cron ran in the same window or what happened on earlier hourly ticks — but it doesn't matter, because the code-level cause (below) guarantees the same outcome on every tick, for every user, unconditionally.

### 4b. Where in the code, and why

`crud.adjust_period_start_for_signup(period_start, period_end, user_created_at)` — `MindSync/app/crud/crud.py:1729-1754` — is explicitly documented as **shared** by all four call sites:

- `app/tasks/weekly_therapy_summary.py:250` (hourly cron, per-user)
- `app/tasks/monthly_therapy_audit.py` (hourly cron, per-user — same helper, same shape per its own header comment)
- `app/api/v1/endpoints/weekly_summaries.py` (`generate_weekly_summary`, manual "Generate now")
- `app/api/v1/endpoints/monthly_audits.py` (`generate_monthly_audit`, manual "Generate now") — confirmed by direct read: `data_window_start = crud.adjust_period_start_for_signup(month_start, month_end, user_created)`

Inside it:
```python
if user_created_at and user_created_at > period_end:
    return None
if user_created_at and user_created_at > period_start:
```

- `period_start`/`period_end` come from `get_calendar_week_range_utc()` / the monthly equivalent (`MindSync/app/utils/time_utils.py:206-249`) — **always timezone-aware**: built via `pytz_tz.localize(datetime.combine(...))` then `.astimezone(UTC)`, which always returns an aware `datetime`.
- `user_created_at` is `user.created_at`, read straight off the `users` row.

### 4c. Confirmed on prod: `users.created_at` is naive, not aware — schema drift from the model

```sql
SELECT column_name, data_type, is_nullable, datetime_precision
FROM information_schema.columns
WHERE table_name='users' AND column_name IN ('created_at','last_login','activated_at');
```
| column | data_type (prod) | nullable |
|---|---|---|
| `created_at` | **timestamp without time zone** | YES |
| `last_login` | **timestamp without time zone** | YES |
| `activated_at` | timestamp with time zone | YES |

Model (`MindSync/app/models/models.py:99`): `created_at = Column(DateTime(timezone=True), server_default=func.now())` — declares **`timestamp with time zone`**. Prod disagrees. Live sample confirms the practical effect:

```sql
SELECT created_at, pg_typeof(created_at) FROM users ORDER BY created_at DESC LIMIT 1;
-- 2026-08-18 23:22:32.842506 | timestamp without time zone
```

psycopg2/SQLAlchemy returns a **naive** `datetime.datetime` for a `timestamp without time zone` column. So `user_created_at > period_end` is naive-vs-aware → `TypeError: can't compare offset-naive and offset-aware datetimes` — the exact message seen in the worker logs (this specific wording is Python's for ordering comparisons `<`/`>`/`<=`/`>=` between aware and naive datetimes, which pins the fault to this comparison rather than, e.g., a subtraction elsewhere in the file).

`count(*) FROM users u JOIN user_preferences up ON up.user_id = u.id` → **1798** — exactly matches the cron's `errors=1798`. Every eligible user, no exceptions.

### 4d. Why this reads as "tapping does nothing" instead of a visible error

Both manual endpoints wrap this exact call inside a broad prep-phase `try/except` (added deliberately in MSV3.2Fix.1 A7/1.1 specifically to stop a raw 500 from reaching the client):

```python
except Exception as e:
    logger.error(...)
    return _generate_response_failed(
        "weekly_summary_prepare_failed",
        "Could not prepare your weekly summary right now. Please try again.",
    )
```

So the backend does **not** crash and does **not** 500 — it returns **HTTP 200** with `status="failed"`, `error_code="weekly_summary_prepare_failed"` (monthly: presumably an analogous `monthly_audit_prepare_failed` — not independently re-verified by request/response capture in this pass, but the code path is identical). No row of any kind is created — the crash happens *before* the `crud.create_weekly_therapy_summary(...)` call in both the cron and both manual endpoints, which is exactly why the tables are empty rather than full of stuck `PROCESSING`/`FAILED` rows.

Whether Darek's tap genuinely produces *zero visible UI change*, or a message he didn't notice/register as a UI change, is a **Flutter-side question outside this agent's read-only DB/backend scope** — the backend response is a normal 200 with a `status="failed"` envelope, which per the spec's own code recon (`therapy_tab_cubit.dart:280-352`) should route to a `generateFailed` cubit state. Recommend `flutter-mobile` verify that `generateFailed` actually renders something on-screen for this exact response shape; it's plausible the CTA appears to do nothing because the failure state is silent/toast-only and easy to miss, not because nothing happened.

## 5. Cross-check against the spec's 6 ranked hypotheses

| # | Spec hypothesis | Verdict |
|---|---|---|
| 1 | worker/scheduler dyno not running → stuck PROCESSING forever | **Refuted for current state.** All three dynos up; the cron demonstrably fires (log evidence, §4a). No `PROCESSING` rows exist anywhere to get stuck. |
| 2 | Stuck PROCESSING row is a dead end (retry 400s, dedup, 71s poll) | **Refuted.** No row is ever created, so there is nothing to get stuck and no dead end to hit — the failure happens one step earlier than this hypothesis assumes. |
| 3 | Request fails before a row exists (exception in prep) | **Confirmed and root-caused.** This is what's actually happening, on literally every attempt, both cron and manual, both weekly and monthly. The `generateFailed` cubit branch mentioned in the spec is real and should be reachable — worth device verification (§4d). |
| 4 | Free account: monthly content stripped, can't retry FAILED | **Moot.** No `FAILED` rows exist to retry; the crash happens before any row, before any premium-gating logic runs. |
| 5 | A NULL in a required field blanks the whole Weekly tab | **Moot / unverified as a current cause** — no rows exist to have a NULL in the first place. Still worth the client-side null-tolerance fix the spec asks for (§7), as a preventive measure once rows start being created. |
| 6 | Hourly crons killed mid-loop by 3600s timeout, serial | **Refuted.** The loop completes in ~10s; every user fails fast on this synchronous TypeError rather than reaching a slow OpenAI call. |

## 6. What this means for auto-generation going forward

Per CS-07's "Done when," auto-generated cards should appear at the next period boundary without a tap. **They will not**, until this is fixed — the hourly cron will keep silently producing `generated=0, errors=<full population>` every hour, forever, for both weekly and monthly, regardless of dyno health or migration state.

## 7. Handoff to `backend-api`

This is a **model/schema/prod-drift finding under CLAUDE.md's Change-Safety rule #3** ("model ↔ migration ↔ prod DB must agree; the Alembic migration + live prod DB are the source of truth"). Two independent, complementary fixes, both owned by `backend-api`:

1. **Fix `crud.adjust_period_start_for_signup` (`app/crud/crud.py:1729-1754`) to be defensive against a naive `user_created_at`** — e.g. normalize with `user_created_at.replace(tzinfo=timezone.utc)` (or equivalent using the project's existing `to_user_tz`/`local_to_utc` naive-datetime handling pattern in `app/utils/time_utils.py`, which already has a naive-datetime guard in `to_user_tz` at lines 151-152: `if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)`) before comparing. This is the minimal, immediate unblock — it does not require a migration and fixes both the cron and both manual endpoints in one place, since all four share this function.
2. **Separately, consider whether `users.created_at` (and `users.last_login`) should be migrated to `timestamp with time zone`** to close the schema drift itself, so no *other* naive/aware comparison against these two columns bites again elsewhere in the codebase (a quick grep for other comparisons against `.created_at`/`.last_login` on `User` is warranted before writing that migration — out of scope for this read-only pass). This is a genuine prod-drift item per the "known prod drift" pattern this agent tracks, not a cosmetic one: `assumed-aware` code exists (`get_calendar_week_range_utc`, the whole summary/audit pipeline) that will keep tripping on `users.created_at` wherever it's touched.

Secondary, lower-priority handoffs already named correctly by the spec and unaffected by this finding: the stale-`PROCESSING`-row sweep, client null-tolerance on the summary/audit Freezed models, and the "Generate now" reachability condition — all still worth doing, but none of them is reachable in practice until #1 above ships, because no row is ever currently created for them to apply to.

## 8. Handoff to `flutter-mobile` (verification only, not a finding this agent can confirm)

Confirm whether `TherapyTabCubit.generateFailed` (per spec: `therapy_tab_cubit.dart:280-352`) actually renders a visible state change for an HTTP 200 body shaped `{"status": "failed", "error_code": "weekly_summary_prepare_failed", ...}`, once the backend fix ships and can be tested end-to-end. If it does, "Generate now" will visibly show an in-card/toast error today already (before the backend fix) rather than "nothing" — worth a quick device check to see whether Darek's "nothing happens" is actually "something happens but it's easy to miss."

## Appendix — exact queries run

All queries executed read-only (`SET TRANSACTION READ ONLY`, `SET statement_timeout`), via two Heroku one-off dynos (`run.7408`, `run.9167`), both stopped after use. No `INSERT`/`UPDATE`/`DELETE`/DDL executed. User identifiers in row-level output were hashed (`substr(md5(user_id),1,8)`) or omitted entirely, per k-anonymity/PII rules — no raw Firebase UID appears in this report; the per-user error lines quoted in §4a are Heroku's own worker-dyno stdout capture (not queried by this agent) and are reproduced here only as evidence of the error signature, not as identifying data.

- `SELECT version_num FROM alembic_version;`
- `SELECT e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid WHERE t.typname ILIKE '%processingstatus%' ORDER BY e.enumsortorder;`
- `SELECT coalesce(processing_status::text,'(null)'), count(*) FROM weekly_therapy_summaries GROUP BY 1 ORDER BY 2 DESC;` (+ monthly equivalent)
- `SELECT count(*), min(created_at), max(created_at) FROM weekly_therapy_summaries;` (+ monthly equivalent)
- `SELECT id, substr(md5(user_id),1,8), created_at, updated_at, data_window_start, data_window_end FROM weekly_therapy_summaries WHERE processing_status::text ILIKE 'processing' AND created_at < now() - interval '15 minutes' ORDER BY created_at DESC LIMIT 25;` (+ monthly equivalent)
- Most-recent-15-rows, rows-created-2026-08-18, NULL-integrity `count(*) FILTER (...)`, and FAILED-last-7d queries — both tables, all four variants.
- `SELECT column_name, data_type, is_nullable, datetime_precision FROM information_schema.columns WHERE table_name='users' AND column_name IN ('created_at','last_login','activated_at');`
- `SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='weekly_therapy_summaries' AND column_name IN ('data_window_start','data_window_end','created_at','updated_at');`
- `SELECT created_at, pg_typeof(created_at) FROM users ORDER BY created_at DESC LIMIT 1;`
- `SELECT count(*) FROM users u JOIN user_preferences up ON up.user_id = u.id;`
- `heroku releases -a mindsync -n 8`, `heroku ps -a mindsync`, `heroku logs --dyno worker -n 1500 -a mindsync`, `heroku logs --dyno scheduler -n 500 -a mindsync` (no weekly/monthly registration lines found in this window — registration logging happens at web-dyno boot, not on the scheduler dyno, so this is expected and not itself evidence of anything).
