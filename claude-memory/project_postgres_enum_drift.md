---
name: Postgres enum labels drift from migrations
description: Production Postgres likely has UPPERCASE enum labels (inferred, needs verification) while migration files declare lowercase — raw SQL must match what's actually in the target DB
type: project
originSessionId: 0d7145a4-d056-48f3-be0d-d914686b50ef
---

**VERIFY BEFORE RELYING ON THIS NOTE.** The "production has UPPERCASE labels" claim below is inferred from a 2026-04-29 production error message + SQLAlchemy default behavior — NOT directly verified by querying prod. Run the verification SQL (see "How to apply") against the target DB before writing or reviewing any raw SQL with enum filters.

**Inferred state (high confidence, not verified):** Production Postgres `processingstatusenum` (and likely other enums like `inputtypeenum`) stores **UPPERCASE** labels (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`, `PLAIN_TEXT`), but migration files in `alembic/versions/` (e.g., `e5f6a7b8c9d0_create_session_debriefs_table.py:32-36`) declare **lowercase** (`'pending'`, `'completed'`...). Evidence: 2026-04-29 production log `psycopg2.errors.InvalidTextRepresentation: invalid input value for enum processingstatusenum: "completed"` — proves lowercase `'completed'` is rejected. ORM writes succeed because SQLAlchemy `Enum(PythonEnum)` without `values_callable` binds `.name` (uppercase), so `'COMPLETED'` is what hits the wire. The labels could theoretically be mixed-case or another scheme; querying `pg_enum` is the only authoritative answer.

**Why the divergence:** Likely a one-off `ALTER TYPE ... RENAME VALUE` ran manually on Heroku Postgres at some point, or the prod DB was bootstrapped from a different schema source. Migration history has no record of the rename. Migrations and runtime have diverged silently. (Discovered by devils-advocate review of loops_sync.py enum fix on 2026-04-29.)

**How to apply:**
- **VERIFY FIRST** with: `SELECT enumlabel FROM pg_enum WHERE enumtypid = '<enum_name>'::regtype ORDER BY enumsortorder;` against the target DB. The rule below assumes the verification confirmed UPPERCASE for `processingstatusenum` on current prod.
- When writing **raw SQL** (`text()` queries) against enum columns, **match the labels in the target DB** — for current prod's `processingstatusenum`, that's UPPERCASE (`'COMPLETED'`, not `'completed'`). DO NOT generalize this as "always use uppercase" for every enum or every environment — a fresh-DB created from current migrations would have lowercase labels, where uppercase would fail.
- Better: bind the enum value as a parameter keyed off the Python enum (`params={"status": ProcessingStatusEnum.COMPLETED.name}`) to keep raw SQL coupled to whatever SQLAlchemy is binding (which matches the live DB labels for any environment that successfully runs ORM writes).
- ORM queries (`models.X.processing_status == ProcessingStatusEnum.COMPLETED`) handle the binding automatically and are safe regardless of label case in the DB — *as long as* DB labels match `.name`. On a fresh-from-migrations DB, **every** enum-bound write fails — not just raw SQL — because labels are lowercase but ORM binds uppercase.
- Fresh-DB scenarios (disaster recovery, blue/green to new Postgres, fresh staging, dev laptop) are likely CURRENTLY BROKEN end-to-end. Must reconcile before any DR exercise or new environment provisioning.
- Reconciliation: pick one direction and keep migrations + ORM + raw SQL aligned. Either (a) write a new Alembic migration that renames lowercase → uppercase on existing DBs (multi-statement: one `ALTER TYPE … RENAME VALUE 'old' TO 'new'` per label, requires PostgreSQL 12+, can run inside a transaction on PG14+, cannot inside a transaction on PG12-13), AND fix the original `CREATE TYPE` migrations to declare uppercase; OR (b) add `values_callable=lambda x: [e.value for e in x]` to every `Enum(PythonEnum)` column AND backfill prod's labels uppercase → lowercase via the same per-label `RENAME VALUE` approach. Option (a) preserves prod state; option (b) preserves migration files.

**Tests blind to this:** `app/tests/conftest.py` uses SQLite (no enum types) and `test_loops_sync.py` mocks `db.execute`, so this bug class is invisible to the existing suite. Real-Postgres integration test needed (testcontainers / CI Postgres service).

**Other raw-SQL enum literals to audit:** `app/tasks/loops_sync.py:183` (`c.conversation_type = 'REFLECT'`) currently works only because `ConversationTypeEnum.REFLECT = "REFLECT"` (verified 2026-04-29 at `app/models/models.py:65` — uppercase value matches uppercase label) — pure coincidence. Any enum where `.value != .value.upper()` (e.g., `processingstatusenum` whose values are lowercase strings) is a landmine in raw SQL.
