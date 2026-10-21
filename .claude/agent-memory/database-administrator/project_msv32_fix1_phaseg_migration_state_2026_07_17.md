---
name: project-msv32-fix1-phaseg-migration-state-2026-07-17
description: Prod alembic state snapshot 2026-07-17 pre-Phase-G-deploy — prod at zz6a7b8c9d0e, 2 migrations (aa2b3c4d5e6f, bb3c4d5e6f70) verified PENDING
metadata:
  type: project
---

Snapshot only — will go stale the moment `alembic upgrade head` runs on prod. As of 2026-07-17, prod `alembic_version` = `zz6a7b8c9d0e`, verified against live schema (not just the version row) and found to agree exactly — no partial-apply drift on this batch.

Verified via schema presence (not just version_num):
- `xx4y5z6a7b8c` (Workspace tables, 8 tables) — APPLIED, all 8 tables + 3 additive columns present.
- `yy5z6a7b8c9d` (moment_type_enum: MOOD_UPDATE_REQUEST, THERAPY_RELATIONSHIP_CHECKIN) — APPLIED, both labels present in pg_enum.
- `zz6a7b8c9d0e` (agenda_items.kind) — APPLIED, matches alembic_version exactly.
- `aa2b3c4d5e6f` (Fix.1 A1: topic_question_items, todo_completions tables; todo_items.repeat_freq; triage_proposals.linked_item_type/linked_item_id) — **PENDING**, none of these exist yet.
- `bb3c4d5e6f70` (user_goals.achieved_at, new HEAD) — **PENDING**, column absent.

Row counts at time of check (small — low migration risk): user_goals=84, threads=8, agenda_items=22, todo_items=17, triage_proposals=119, goal_narratives=76, weekly_observations=23, mood_trend_summaries=74.

Both pending migrations are additive-only + idempotently guarded (has_table/get_columns checks) — low blast radius, no enum/native-DDL involved, no backfill needed.

**Why:** this was a deploy-prep gate for MSV3.2 Fix.1 Phase G (see [[project_msv3_2_workspace_batch_2026_07_06]] for the batch this migration chain belongs to) — operator needed to know the exact ordered pending list before running `alembic upgrade head` on Heroku.

**How to apply:** once the operator runs the migration and this is confirmed via a fresh `heroku run alembic current`, this snapshot is obsolete — re-verify against live prod rather than trusting this file for "is it applied" questions going forward. Full report: `db-reports/msv3_2_fix1_phaseG_migration_state_2026-07-17.md`.
