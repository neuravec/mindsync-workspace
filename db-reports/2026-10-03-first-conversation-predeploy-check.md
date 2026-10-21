# Pre-deploy check: first voice conversation (migration m315a1b2c3d4 + Reflect idle job)

- **Date:** 2026-10-03, queried 20:36 UTC
- **Requested by:** lead, ahead of the deploy that ships `m315a1b2c3d4` (`user_memory_items` table, `conversations.entry_origin VARCHAR(32) NULL`) and the 15-minute `analyze_idle_reflect_threads` cron (`app/tasks/reflect_idle_analysis.py`)
- **Access:** Heroku one-off dyno `run.2357` on `mindsync`, REPL-safe script piped over stdin, app's own `SessionLocal`. Dyno stopped after capture; no one-off dynos left running.
- **Safety:** `SET TRANSACTION READ ONLY` (confirmed `transaction_read_only=on`), `statement_timeout = 30000`, SELECT / catalog reads / `EXPLAIN (ANALYZE, BUFFERS)` of SELECTs only, ended with `rollback()`. No DML, no DDL.

## Verdict

**GO from the database side.** Prod is at the expected pre-deploy head, nothing that m315 creates exists yet, the FK target types match, and the new job's queries cost well under 5 ms at today's volume. The initial backlog for the idle job is **16 threads**. One finding is not a blocker but should be fixed: **`messages` has no index on `conversation_id`**, so the job's grouped `max(created_at)` and every `ON DELETE CASCADE` from `conversations` do a full sequential scan of `messages`. Follow-up for `backend-api` in section 7.

## 1. Alembic version

| check | result |
|---|---|
| `SELECT version_num FROM alembic_version` | `m314b2c3d4e5` |
| expected before this deploy | `m314b2c3d4e5` |
| m314 artifacts on `conversations` | `modality varchar(8)`, `seed_source varchar(24)`, `seed_label text`, all present |

Matches. The `m315a1b2c3d4` file in the repo has `down_revision = "m314b2c3d4e5"`, so the chain is linear with no gap and no fork.

## 2. Indexes

`SELECT tablename, indexname, indexdef FROM pg_indexes WHERE schemaname='public' AND tablename IN ('messages','conversations','conversation_summaries')`

| table | index | columns |
|---|---|---|
| messages | `messages_pkey` (unique) | `id` |
| messages | `ix_messages_id` | `id` (duplicates the PK) |
| conversations | `conversations_pkey` (unique) | `id` |
| conversations | `conversations_uuid_key` (unique) | `uuid` |
| conversations | `ix_conversations_id` | `id` (duplicates the PK) |
| conversation_summaries | `conversation_summaries_pkey` (unique) | `id` |
| conversation_summaries | `conversation_summaries_conversation_id_key` (unique) | `conversation_id` |
| conversation_summaries | `ix_conversation_summaries_id` | `id` (duplicates the PK) |

Answers:

- **`messages` index with leading `conversation_id`: NONE.** The FK `messages.conversation_id → conversations.id ON DELETE CASCADE` is unindexed.
- **`conversations (user_id)`: NONE.**
- **`conversations (conversation_type / status)`: NONE.**
- **`conversations (created_at)`: NONE** (and none on `last_message_at`, which is the column the new job actually filters and sorts on).
- `conversation_summaries (conversation_id)` is covered by its unique constraint, so the job's third query is indexed.

### What that costs today (EXPLAIN ANALYZE of the job's own query shapes)

| query (as the job issues it) | plan | rows touched | buffers | time |
|---|---|---|---|---|
| candidate scan on `conversations` (REFLECT, ACTIVE, `last_message_at` in [now-7d, now-30min], ORDER BY `last_message_at DESC, id DESC` LIMIT 200) | Seq Scan + quicksort | 1,802 read, 18 kept | 44 shared hit | 0.19 ms |
| grouped `max(created_at), max(id)` on `messages` for 200 ACTIVE REFLECT ids (worst case: the 200 most recent, not just the 18 in window), `role='USER'` | Seq Scan + HashAggregate | 20,932 read, 2,317 kept, 155 groups | 1,140 shared hit | 3.3 ms |

Both run fully from cache. 96 runs a day add up to well under one second of DB time. **Not a blocker at this size.** The messages scan cost grows linearly with total `messages` rows, not with the 200-thread cap, so it grows with the product and not with the job's own limit.

Table sizes for scale (`pg_class.reltuples`, `pg_stat_user_tables`):

| table | live rows | total size | seq_scan | idx_scan |
|---|---|---|---|---|
| messages | 20,932 | 24 MB | 4,161 | 1,415 |
| conversations | 1,802 | 616 kB | 56,475 | 931,959 |
| conversation_summaries | 9 live (1,381 at last ANALYZE) | 2.9 MB | 33 | 61,295 |
| users | 1,905 | 656 kB | 4,894 | 1,791,722 |

`messages` is already scanned sequentially about three times as often as it is read through an index.

## 3. m315 objects must not exist yet

| check | result | expected |
|---|---|---|
| `information_schema.tables` where `table_name='user_memory_items'` | 0 | 0 |
| `pg_class` for `ix_user_memory_items_user_id_deleted_at`, `ix_user_memory_items_source_conversation_id` | 0 | 0 |
| `information_schema.columns` `conversations.entry_origin` | absent | absent |

Clean. Deploy-order note, verified against the code and not only the DB: `Base.metadata.create_all` on the first web boot of the new slug will create `user_memory_items` **before** `alembic upgrade head` runs, because `app/models/user_memory.py` declares the table. That is safe. The model's `__table_args__` declares both indexes under the **same names** as the migration, and m315 guards the table, each index and the column separately (`_has_table` / `_has_index` / `_has_column`). So it fills in only what is missing whichever runs first. `entry_origin` cannot be created by `create_all` (existing table) and depends on the manual migration.

## 4. Reflect row counts and the idle-job backlog

Enum labels on prod (`pg_enum`):

| column | PG type | labels |
|---|---|---|
| `conversations.conversation_type` | `conversationtypeenum` | `JOURNAL, REFLECT` |
| `conversations.status` | `statusenum` | `ACTIVE, PAUSED, FINISHED` |
| `messages.role` | `roleenum` | `USER, AGENT, SYSTEM` |

All UPPERCASE. These three types match the Python member names and values (`StatusEnum.ACTIVE = 'ACTIVE'` and so on), so **no drift on the columns this job touches**. The ORM comparisons `== ConversationTypeEnum.REFLECT`, `== StatusEnum.ACTIVE` and `== RoleEnum.USER` bind valid labels. The EXPLAIN above ran with those literal labels and planned without error.

`SELECT conversation_type::text, status::text, count(*) FROM conversations GROUP BY 1,2`

| type | status | threads |
|---|---|---|
| REFLECT | ACTIVE | **245** |
| REFLECT | FINISHED | **36** |
| REFLECT | PAUSED | 0 |
| JOURNAL | ACTIVE | 7 |
| JOURNAL | FINISHED | 1,514 |

Age of the 245 ACTIVE REFLECT threads by `conversations.last_message_at`:

| last message | threads |
|---|---|
| NULL | 0 |
| under 30 min ago | 0 |
| 30 min to 7 days ago (the job's window) | **18** |
| 7 to 30 days ago | 21 |
| over 30 days ago | 206 |

Backlog:

| measure | threads |
|---|---|
| ACTIVE REFLECT with any message in the last 7 days (`EXISTS` on `messages.created_at >= now()-7d`), as asked | **18** (distinct users: n<25, suppressed) |
| of those, with a USER message in the last 7 days | 16 |
| job-equivalent window (`last_message_at` between now-7d and now-30min) | 18 |
| ... with at least one USER message (otherwise the job skips the thread) | 16 |
| ... with no `conversation_summaries` row | 16 |
| ... with a summary older than the last USER message | 0 |
| **would be enqueued by the job right after deploy** | **16** |
| ACTIVE REFLECT with a message in the last 7 days but `last_message_at` NULL or older than 7 days (would be missed by the job) | 0 |

Interpretation:

- The one-off drain is **16 analysis jobs**. At the default `REFLECT_IDLE_ANALYSIS_BATCH_SIZE` of 10 per tick, that is 10 on the first tick and 6 on the second, so about 30 minutes if nothing fails. That means 16 model calls on the `default` queue. The exact number will drift by a few between now and deploy time because the window slides.
- `CANDIDATE_SCAN_LIMIT = 200` is not near being hit (18 in window).
- `conversations.last_message_at` agrees with `messages`: the window count from `last_message_at` (18) equals the count from `messages.created_at` (18), and no ACTIVE REFLECT thread has a NULL `last_message_at`. The job's choice to filter on the denormalized column is sound on today's data.
- Reflect threads effectively never move to FINISHED (245 ACTIVE against 36 FINISHED, 206 of the ACTIVE ones silent for over 30 days). Not a problem for this job because of the 7-day lookback, but every ACTIVE-REFLECT scan reads them.

## 5. Postgres version and the `users.id` type

| check | result |
|---|---|
| `server_version` | **PostgreSQL 16.13** (`server_version_num` 160013) |
| `users.id` | **`character varying`, no length, NOT NULL**, primary key `users_pkey (id)` |
| `conversations.id` | `integer`, NOT NULL, primary key |
| existing FK for reference | `conversations_user_id_fkey: FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE` |

m315 declares `user_memory_items.user_id sa.String()` (unbounded varchar) → `users.id` varchar, and `source_conversation_id sa.Integer()` → `conversations.id` integer. Both FK types match exactly. On PG 16, `ADD COLUMN entry_origin varchar(32)` with no default is a catalog-only change: it takes a short ACCESS EXCLUSIVE lock on `conversations` (1,802 rows) and rewrites nothing.

## 6. Side observation: naive timestamp columns (same family as CS-07)

| column | prod type | model declares |
|---|---|---|
| `messages.created_at` | `timestamp without time zone` | `DateTime(timezone=True)` |
| `conversation_summaries.created_at` | `timestamp without time zone` | `DateTime(timezone=True)` |
| `conversations.created_at` | `timestamp without time zone` | `DateTime(timezone=True)` |
| `conversations.last_message_at` | `timestamp with time zone` | `DateTime(timezone=True)` |

The server `TimeZone` is `UTC`, so the naive values are UTC. The new job is safe: `reflect_analysis_is_current` and the per-thread idle check both go through `orca_memory._aware()`, which treats naive values as UTC. **Any other new code** in this deploy that compares `Message.created_at` or `ConversationSummary.created_at` with `utc_now()` without `_aware()` will raise `TypeError: can't compare offset-naive and offset-aware datetimes` on Postgres only. SQLite tests hide this, and it is exactly how CS-07 failed. This is a caution, not a confirmed bug.

## 7. Handoffs

**`backend-api` (not blocking this deploy, separate migration after it):**

1. Add the missing FK index on messages. This one carries the most weight, because it also serves every ON DELETE CASCADE from `conversations` (thread delete, account deletion) and every per-thread message read:
   `CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_messages_conversation_id_created_at ON messages (conversation_id, created_at);`
2. Optionally add `CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_conversations_user_id ON conversations (user_id);` for per-user thread lists (`conversations` already sees 56k sequential scans, harmless at 1.8k rows).
3. Use `op.get_context().autocommit_block()` for `CONCURRENTLY`, guard with `_has_index`, never `bind.commit()`. Declare the same indexes in the model (`__table_args__`) so model and migration agree. No partial index on (type, status, last_message_at) is needed at this size.
4. Low priority: `ix_messages_id`, `ix_conversations_id` and `ix_conversation_summaries_id` duplicate their primary keys (from `index=True` on PK columns) and only cost write overhead. Leave them unless you are doing a deliberate cleanup.

**Deploy sequencing (unchanged, for the operator):** push, then `heroku run alembic upgrade head --app mindsync`, then confirm with `heroku run alembic current --app mindsync` that it reports `m315a1b2c3d4`.

## Method note: Heroku CLI auth

`heroku run` first failed with "Invalid credentials provided" from the CLI, although the token stored in `%USERPROFILE%\_netrc` was valid: a direct call to `api.heroku.com/account` with it returned 200, and Heroku status was green. The workaround was to export that same token as `HEROKU_API_KEY` for the command, never printing it. A future run should check `heroku auth:whoami` first.
