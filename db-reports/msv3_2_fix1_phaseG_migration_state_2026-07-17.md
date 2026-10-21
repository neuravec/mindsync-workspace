# MSV3.2 Fix.1 — Phase G Deploy-Prep: Production Alembic Migration State

**Date:** 2026-07-17
**Author:** database-administrator (read-only verification)
**Access:** Heroku one-off dyno (`heroku run -a mindsync python < script.py`, run.7467), REPL-safe script, `SET TRANSACTION READ ONLY`, no commits. Dyno stopped after read (`heroku ps:stop run.7467 -a mindsync` → confirmed; `heroku ps -a mindsync` shows only the standard web/worker/scheduler dynos afterward, no stray one-off).

## Question

Which of the 5 locally-committed migrations from the MSV3.2 / Fix.1 batch are actually applied on production Postgres, verified by schema presence (not just `alembic_version`), ahead of the Phase G deploy?

## Exact queries run (all read-only: `information_schema`, `pg_catalog`, plain `SELECT count(*)`)

```sql
SELECT version_num FROM alembic_version;

SELECT table_name FROM information_schema.tables
WHERE table_schema='public' AND table_name IN
 ('threads','thread_sources','agenda_items','todo_items','goal_narratives',
  'weekly_observations','mood_trend_summaries','triage_proposals',
  'topic_question_items','todo_completions')
ORDER BY 1;

SELECT table_name, column_name, data_type FROM information_schema.columns
WHERE (table_name='realizations' AND column_name IN ('show_on_timeline','in_repo'))
   OR (table_name='user_preferences' AND column_name='workspace_last_visited_at')
   OR (table_name='agenda_items' AND column_name='kind')
   OR (table_name='todo_items' AND column_name='repeat_freq')
   OR (table_name='triage_proposals' AND column_name IN ('linked_item_type','linked_item_id'))
   OR (table_name='user_goals' AND column_name='achieved_at')
ORDER BY 1,2;

SELECT e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid
WHERE t.typname='moment_type_enum'
  AND e.enumlabel IN ('MOOD_UPDATE_REQUEST','THERAPY_RELATIONSHIP_CHECKIN')
ORDER BY 1;

SELECT count(*) FROM user_goals;
SELECT count(*) FROM <each workspace table confirmed to exist>;
```

## Results

**`alembic_version` on prod:** `zz6a7b8c9d0e`

**Tables present** (of the 10 checked): `agenda_items`, `goal_narratives`, `mood_trend_summaries`, `thread_sources`, `threads`, `todo_items`, `triage_proposals`, `weekly_observations`
Absent: `topic_question_items`, `todo_completions`

**Columns present:**
| table.column | type |
|---|---|
| agenda_items.kind | character varying |
| realizations.in_repo | boolean |
| realizations.show_on_timeline | boolean |
| user_preferences.workspace_last_visited_at | timestamp with time zone |

Absent (checked, not found): `todo_items.repeat_freq`, `triage_proposals.linked_item_type`, `triage_proposals.linked_item_id`, `user_goals.achieved_at`

**`moment_type_enum` labels present:** `MOOD_UPDATE_REQUEST`, `THERAPY_RELATIONSHIP_CHECKIN` (both)

**Row counts:**
| table | rows |
|---|---|
| user_goals | 84 |
| threads | 8 |
| agenda_items | 22 |
| todo_items | 17 |
| triage_proposals | 119 |
| goal_narratives | 76 |
| weekly_observations | 23 |
| mood_trend_summaries | 74 |

(`thread_sources` confirmed present but not sampled for row count — it's a junction table, immaterial to migration risk.)

## Per-migration verdict

| Migration | Verdict | Evidence |
|---|---|---|
| `xx4y5z6a7b8c` (Workspace tables, 8 tables) | **APPLIED** | All 8 tables it creates exist (`threads`, `thread_sources`, `agenda_items`, `todo_items`, `goal_narratives`, `weekly_observations`, `mood_trend_summaries`, `triage_proposals`); its 3 additive columns (`realizations.show_on_timeline`, `realizations.in_repo`, `user_preferences.workspace_last_visited_at`) all present. |
| `yy5z6a7b8c9d` (moment_type_enum: `MOOD_UPDATE_REQUEST`, `THERAPY_RELATIONSHIP_CHECKIN`) | **APPLIED** | Both new enum labels present in `pg_enum` for `moment_type_enum`. |
| `zz6a7b8c9d0e` (agenda_items.kind) | **APPLIED** | `agenda_items.kind` column present (`character varying`, matches the `String(24)` declared — not a native enum, no drift risk). This is also the exact value in `alembic_version`. |
| `aa2b3c4d5e6f` (Fix.1 A1: `topic_question_items`, `todo_completions`, `todo_items.repeat_freq`, `triage_proposals.linked_item_type`/`linked_item_id`) | **PENDING** | Neither `topic_question_items` nor `todo_completions` exists; neither `todo_items.repeat_freq` nor `triage_proposals.linked_item_type`/`linked_item_id` exists. |
| `bb3c4d5e6f70` (`user_goals.achieved_at`) | **PENDING** | `user_goals.achieved_at` column absent. |

**`alembic_version` and live schema agree exactly** — prod is cleanly sitting at `zz6a7b8c9d0e` with no partial-apply drift on this batch. This is a clean state, not the "prod ahead of/behind version_num" drift pattern seen historically.

## Ordered list `alembic upgrade head` will run at deploy time

1. `aa2b3c4d5e6f` — Add Workspace Fix.1 A1 tables/columns
2. `bb3c4d5e6f70` — Add `user_goals.achieved_at` **(new HEAD** — confirmed no other file has `down_revision = bb3c4d5e6f70`)

## Risk read for the operator

- Both pending migrations are **additive-only** (new tables, or nullable columns with no backfill) and both are **idempotently guarded** (`has_table()` / `inspector.get_columns()` existence checks per the migration file docstrings) — safe to run even if a prior partial-apply attempt happened.
- `bb3c4d5e6f70` touches the **live** `user_goals` table (currently 84 rows) but only via a nullable `ADD COLUMN achieved_at` — no rewrite, no lock risk beyond a brief metadata lock, no backfill (migration docstring: API falls back to `updated_at` for legacy ACHIEVED rows).
- Neither pending migration introduces a native Postgres enum or touches `moment_type_enum`/other enum types — no interaction with the known UPPERCASE-label enum-drift issue.
- No `NOT NULL` additions, no data migrations, no destructive DDL in the pending set.
- Standard sequencing applies: deploy the backend-api commit containing these migration files together with the manual `heroku run alembic upgrade head --app mindsync` step (Heroku has no release phase); verify after with `heroku run alembic current --app mindsync` and expect `bb3c4d5e6f70`.

## Read-only / cleanup confirmation

- Script only ran `SELECT` / `information_schema` / `pg_catalog` queries; `SET TRANSACTION READ ONLY` was issued before any query; no `commit()` was called; no DML/DDL executed.
- One-off dyno `run.7467` was stopped (`heroku ps:stop run.7467 -a mindsync`); `heroku ps -a mindsync` afterward shows only the standing `web`/`worker`/`scheduler` dynos — no stray one-off dyno left running.
