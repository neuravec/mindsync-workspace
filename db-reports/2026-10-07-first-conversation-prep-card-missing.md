# First-conversation "Before therapy" card missing after an onboarding re-run (2026-10-07)

**Author:** database-administrator (read-only)
**Data as of:** 2026-10-07 19:52 UTC, prod Postgres (alembic head `m316a1b2c3d4`), RedisGreen, Heroku release v568 (`79f1787`)
**Access:** two Heroku one-off dynos (`run.3252`, `run.6656`, `--no-tty`, both exited on their own). Every DB connection was forced read-only at connect time (`SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY`, verified `transaction_read_only=on`). Redis: GET / EXISTS / TTL / SMEMBERS / ZRANGE / LRANGE / HGET / SCAN only. No DML, no DDL, no Redis writes, no job requeue or delete, no app code edits.

## TL;DR

The card was **enqueued, ran, passed every gate and then crashed on its own INSERT.** The job builds the card row with `input_type=InputTypeEnum.AUTO`. SQLAlchemy sends the member **name** `'AUTO'`, but the prod Postgres type `inputtypeenum` only has the labels `VOICE`, `TEXT` and lowercase `auto`. Postgres rejects the row (`invalid input value for enum inputtypeenum: "AUTO"`, reproduced on prod with a plain `SELECT CAST(...)`), the job's catch-all turns that into outcome `failed`, and no row is ever written. The Redis once-per-thread claim was already taken one line earlier, so the job will never retry this thread (the claim lives 30 days).

This is the enum-drift class of bug from CLAUDE.md rule 3/4: SQLite tests pass, Postgres refuses. The same `InputTypeEnum.AUTO` insert lives in the hourly auto-generate cron, which is why **prod has never stored a single AUTO prep card (0 rows all-time)**.

Not the cause: therapy status, Art. 9 consent, crisis, short transcript, schedule/timezone, an existing card, the reset, or a missing enqueue. All of them were checked and passed.

## Who the tester is

Resolved from the operator-supplied account identity inside the dyno only (never printed): user `CtRpjcn2`. Account created 2024-12-19, so this is an old account doing an onboarding re-run. Their first-conversation claim was taken 2026-10-05 16:14:41Z (thread 28584), so today's threads are re-run threads (marked, no claim). That is by design since 2026-10-05.

Other marked threads since 2026-10-06 belong to two other test accounts (`YTbaXiHB`, `Ho0vY6fZ`), all created on 2026-10-06, before the feature existed, and both accounts fail the therapy gate anyway. They are out of scope.

## The tester's two runs today

| | Thread 28679 | Thread 28711 |
|---|---|---|
| Created (UTC) | 14:31:04 | 18:42:56 |
| Release live then | v565 (no prep-card job in the code) | v568 (job present since v567, 15:50:20Z) |
| Person turns | 6 | 5 (4 stored as transcript turns after cleanup) |
| Recap verdict (Redis cache) | `ready`, `saved_line_kind=before_therapy_card` | `ready`, `saved_line_kind=before_therapy_card` |
| Card promised on screen | yes | yes |
| Prep-card job | did not exist | enqueued, ran, failed at INSERT |
| Card row | none | none |

So the tester was promised the card twice. The first time (14:31) the generator was not deployed yet: the recap's promise line shipped before the card generator did. The second time (18:42) is the real failure.

## Timeline of thread 28711 (all UTC, 2026-10-07)

| Time | Event | Evidence |
|---|---|---|
| before 18:41:56 | Reset onboarding | `user_therapy_context` consent timestamps were cleared and re-set; exact reset time is gone (row's `updated_at` was overwritten by later saves, log buffer starts 19:00:58) |
| 18:41:56.976 | Re-run consent screen: disclaimer, GDPR, age all set in one write | `user_therapy_context.medical_disclaimer_accepted_at = gdpr_consent_at = age_verified_at` |
| 18:42:45 | Onboarding answers saved, `onboarding_completed=true` | `user_therapy_context.updated_at` |
| 18:42:47 | Personal bio restyle (onboarding flow) | `token_usage_log` PERSONAL_BIO |
| 18:42:56 | Marked thread 28711 created | `conversations.created_at`, `entry_origin='onboarding_first_conversation'` |
| 18:43:34 to 18:44:55 | Person speaks (voice, 5 turns) | `messages` role USER |
| 18:44:57 | Last message | `messages` |
| ~18:45:06 | **POST /end** moves thread to FINISHED, enqueues analysis, stores the analysis job id, enqueues the prep-card job behind it | Redis `reflect:analysis_job:28711` written at ~18:45:06 (from its 6 h TTL); exactly one analysis run followed |
| 18:45:08 | **POST /recap**: model call, recap cached, memory facts written | `token_usage_log` `first_conversation_recap` 18:45:08.05; recap cache written ~18:45:08; 7 `user_memory_items` at 18:45:08 |
| 18:45:08 to 18:45:52 | Analysis job (summary, topics, emotions, RAG embed) | `conversation_summaries`, `conversation_topics`, token rows |
| 18:45:56 to 18:46:34 | Dependent job 1: rolling chart explanations | 20 CHART_EXPLANATION token rows |
| **~18:46:37** | **Dependent job 2: prep-card job runs, passes all gates, takes the claim** | Redis `reflect:first_conversation:prep_card:28711` exists, TTL 2588059 s of 2592000 at 19:52, i.e. written ~18:46:37 |
| right after | `_generate`: context, habits and memory read fine, then `INSERT session_prep_cards (input_type='AUTO', ...)` is rejected by Postgres; job catches it, rolls back, returns `failed` | no `session_prep_cards` row for this user since 2026-09-03 (none soft-deleted either); zero PREP_CARD token rows for this user today (the model call comes after the INSERT, so it never ran) |

The job's own log lines (`[FC-PREP] Prep card job for thread 28711 failed: DataError` and `[FC-PREP] thread 28711: failed`) would have been written around 18:46:37, but the Heroku log buffer only reaches back to 19:00:58, so they cannot be shown. The RQ job hash and result stream are also gone (RQ's default 500 s result TTL), and the job is not in any failed or deferred registry, which is what a job that **returned** `failed` instead of raising looks like.

## Gate-by-gate (dry evaluation on prod at 19:48 UTC, no claim, no generate)

| # | Gate in `make_prep_card_for_thread` | 28711 | Notes |
|---|---|---|---|
| 0 | `/end` enqueues only for in-therapy people (`should_enqueue`) | pass | same inputs as gate 3 |
| 1 | thread FINISHED, REFLECT, owned | pass | |
| 2 | marked first conversation | pass | |
| 3 | in therapy + active Art. 9 | pass | Art. 9 record granted 2026-08-17 17:11:06, never withdrawn. Therapy status row last written before 2026-10-06 05:34 (xmin bracketing). Both were true long before /end. The reset does not touch `consent_records` or `user_profile` (it only clears `user_therapy_context`), and the re-run wrote no new consent row. |
| 4 | crisis keyword scan | pass | no hit |
| 5 | recap floor (`>=2` turns, `>=10` words) | pass | 4 turns, 113 counted words |
| 6 | cached recap verdict | pass | `ready`, not crisis, not short |
| 7 | next session + existing card | pass | `next_session_utc` = 2026-10-08 15:00Z; `_existing_card` = none (newest card is from 2026-09-03, manual, undated) |
| 8 | Redis claim | taken by the 18:46:37 run | this is the evidence the job got this far |
| 9 | INSERT of the PROCESSING card | **FAILS** | enum label mismatch, see below |

Thread 28679 evaluates the same way today (all gates pass, no claim key). It never had a job because the code was not deployed when it ended.

## Proof of the INSERT failure (prod, read-only)

Pure `SELECT CAST(:v AS inputtypeenum)` on prod:

| Value | Result |
|---|---|
| `'AUTO'` | **rejected**: `invalid input value for enum inputtypeenum: "AUTO"` |
| `'auto'` | ok |
| `'TEXT'` | ok |
| `'text'` | rejected |
| `'VOICE'` | ok |

What the app sends, checked inside the dyno with the real model and the Postgres dialect:

- `session_prep_cards.input_type` SQLAlchemy labels: `['VOICE', 'TEXT', 'AUTO']` (member names, no `values_callable`)
- bind value for `InputTypeEnum.AUTO` = `'AUTO'`, for `InputTypeEnum.TEXT` = `'TEXT'`
- `processing_status` binds `'PROCESSING'`, which prod has, so that column is fine.

Why: `inputtypeenum` was created on prod with uppercase names (`VOICE`, `TEXT`), matching the model. Migration `d0y1z2a3b4c5_prep_card_overhaul_phase1` then ran `ALTER TYPE inputtypeenum ADD VALUE IF NOT EXISTS 'auto'`, i.e. the Python **value** (lowercase), not the name the ORM sends. The model and the migration disagree, and SQLite tests cannot see it.

The steps of `_generate` before the INSERT (`gather_prep_card_context`, `_append_habit_context`, `attach_memory_to_prep_context`, profile/prefs reads) were dry-run for the tester on prod and all succeed. The INSERT is the first thing that can fail, and it always will.

## Blast radius: every AUTO card insert is broken, and always has been

| Writer | File | Status on prod |
|---|---|---|
| First-conversation card (new, v567) | `app/tasks/first_conversation_prep_card.py:264` | fails every time it gets past the gates |
| Hourly auto-generate cron (since 2026-03-28) | `app/tasks/prep_card_auto_generate.py:226` | fails every time a user is inside the window; the per-user `except` counts it as `errors` and the cron job still reports OK |
| `POST /prep-cards/auto-generate` | `app/api/v1/endpoints/prep_cards.py:576` | would 500; the Flutter caller was removed 2026-08-10 |

All-time `session_prep_cards`: TEXT/manual 89, TEXT/null 15, VOICE/manual 11, VOICE/null 14, **AUTO 0**. Since 15:50Z today no auto card exists for anyone. In the 19:30 cron run, 12 users were eligible and 8 were outside the window, so nobody was attempted that hour.

`session_debriefs` and `between_session_notes` share the same `inputtypeenum` type but only ever write TEXT/VOICE, so they are unaffected.

## What would make the tester's card appear

1. **Fix (backend-api, migration, idempotent):** add the label the ORM actually sends, inside an autocommit block per project convention:
   `ALTER TYPE inputtypeenum ADD VALUE IF NOT EXISTS 'AUTO'`.
   This is additive and needs no code change, and it fixes all three writers at once. The orphan lowercase `auto` label stays unused and harmless. Do **not** switch the column to `values_callable`: that would make `VOICE`/`TEXT` bind as `voice`/`text`, which prod rejects. Run `alembic upgrade head` on Heroku right after the deploy (no release phase). Add a Postgres-dialect test that compares the model's `inputtypeenum` labels with the migration's (CLAUDE.md rule 4).
2. **Thread 28711 will not heal by itself after the fix.** Its claim key `reflect:first_conversation:prep_card:28711` blocks any retry until about 2026-11-06. Two ways to get a card for the tester, either needing operator approval:
   - delete that one Redis key and enqueue `generate_first_conversation_prep_card(28711, <uid>)` once (a Redis write plus a job, not DML), or
   - have the tester reset onboarding and do the first conversation again after the fix (new thread, new key, no manual step).
   Separately, once the enum is fixed the hourly cron would also create an AUTO card for the 2026-10-08 15:00Z session when it enters the window, but only if the account passes the cron's subscription/trial filter, which was not checked here.
3. **Worth a backend-api look (not the cause today):** the job takes the claim *before* `_generate`, so any failure inside `_generate` (this enum, a DB blip, a model outage before the PROCESSING row) burns the thread's only attempt for 30 days. Releasing the claim when no row was written would make this self-healing.

## Side findings (not the cause)

1. **`featureenum` is missing `MOOD_TREND` on prod.** The hourly mood-trend job's `token_usage_log` insert fails with `invalid input value for enum featureenum: "MOOD_TREND"` (seen in the log buffer at 19:00:58). The job still completes, but mood-trend AI cost is not logged. `PREP_CARD` is present. Fix: `ADD VALUE IF NOT EXISTS 'MOOD_TREND'` (backend-api).
2. `crud.find_prep_card_for_session` does not filter `deleted_at`, so a soft-deleted card can still count as covering a session and suppress the first-conversation card and the cron card (`skipped:existing_card`). The undated branch in `_existing_card` does filter it. Not triggered for the tester (no deleted cards).
3. Timezone: the tester's stored `time_zone` is `"UTC+2"`. In the current code `parse_timezone` resolves it correctly to `FixedOffset(+120)`, and the next session computes to Thursday 17:00 local = 15:00Z, so it played no part here. Two caveats: a fixed offset ignores DST (from 2026-10-25 a Central European user's sessions would compute an hour off), and the stored anchor `user_preferences.next_session_date` holds 17:00**Z** for that same 17:00 local session (a 2 h skew in the stored anchor; only used for biweekly parity in this path, not investigated further).
4. Two `generate_rolling_chart_explanations_for_user` jobs sit in `rq:deferred:default`, so their parent never released them (likely parents lost in a restart). Harmless, but they will never run.

## What prod cannot tell us

- The exact time of the reset request: the row's `updated_at` was overwritten and the log buffer starts at 19:00:58.
- The exact `/end` request time: it is bracketed between 18:44:57 (last message) and 18:45:06 (analysis job id stored), and the recap followed at 18:45:08.
- The job's logged outcome line and the exception text: both evicted. The failure point is instead pinned by four independent facts: the claim exists, no row exists (not even FAILED or soft-deleted), no PREP_CARD model call was logged, and the `'AUTO'` cast is rejected deterministically on prod.
- Whether the client called `/end` more than once: any repeat would return `already_ended` and enqueue nothing, so it does not change the outcome.

## Queries and scripts

Scripts (scratchpad, not committed): `diag_src.py` (candidates, per-user timeline, dry gates, RQ/Redis sweep) and `diag2_src.py` (tester resolution, enum proof, SQLAlchemy bind check, all-time AUTO counts, pre-insert dry run, Redis TTL timing). Both were wrapped in the chunked `exec(compile(...))` runner and piped with `heroku run --no-tty -a mindsync python`.

Key queries (all read-only):

```sql
-- marked threads since 2026-10-06
SELECT c.id, c.created_at, c.status, u.first_conversation_claimed_at,
       (SELECT count(*) FROM messages m WHERE m.conversation_id=c.id AND m.role::text='USER') AS user_msgs
FROM conversations c JOIN users u ON u.id=c.user_id
WHERE c.entry_origin='onboarding_first_conversation' AND c.created_at >= '2026-10-06';

-- enum proof
SELECT CAST('AUTO' AS inputtypeenum);   -- rejected
SELECT CAST('auto' AS inputtypeenum);   -- ok

-- AUTO cards ever stored
SELECT input_type::text, coalesce(generation_type,'(null)'), count(*)
FROM session_prep_cards GROUP BY 1,2;
```

Timing of Redis-only writes came from `TTL` arithmetic: the write time is now minus (configured TTL minus remaining TTL), using 30 d for the prep-card claim, 6 h for the analysis job id and 24 h for the recap cache.

## Follow-up: full enum drift sweep

See `2026-10-07-enum-drift-sweep.md`. Across all 34 enum columns in `app/models`, only two labels are missing on prod: `inputtypeenum` `AUTO` and `featureenum` `MOOD_TREND`. `MOOD_TREND` must also be added to the Python `FeatureEnum`, or ORM reads of those rows will break.

## Handoffs

| To | What |
|---|---|
| backend-api | Idempotent migration `ALTER TYPE inputtypeenum ADD VALUE IF NOT EXISTS 'AUTO'` (autocommit block), deploy plus manual `alembic upgrade head`; Postgres-dialect enum consistency test; consider releasing the prep-card claim when `_generate` writes no row; `featureenum` `MOOD_TREND`; `deleted_at` filter in `find_prep_card_for_session`. |
| operator | Approve one of the two ways to get the tester's card for thread 28711 after the fix (Redis key delete plus single enqueue, or a fresh re-run). |
| posthog-data-extractor (optional) | `reflect_session_ended` for thread 28711 would give the exact `/end` timestamp, and `prep_card_auto_generated` should show zero events from `source=first_conversation`. |
