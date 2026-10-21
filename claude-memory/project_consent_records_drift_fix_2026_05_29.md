---
name: project_consent_records_drift_fix_2026_05_29
description: Wave3+4 migration pp6q7r8s9t0u made idempotent after prod DuplicateTable consent_records; prefer idempotent migrations on this drifted prod DB
metadata: 
  node_type: memory
  type: project
  originSessionId: 133c2d96-2800-4cde-92ac-81c284b7a49d
---

On 2026-05-29 the Heroku prod `alembic upgrade head` failed at migration `pp6q7r8s9t0u` (Wave 3+4 onboarding profiling) with `psycopg2.errors.DuplicateTable: relation "consent_records" already exists`. Root cause: `alembic/env.py` runs the whole upgrade in ONE transaction (no `transaction_per_migration`), so the failing run rolled back the column adds — `consent_records` was left over from an earlier partial/aborted deploy. Same recurring prod schema-drift theme as [[project_postgres_enum_drift.md]].

**Fix (committed `76a5b26` on backend `main`, pushed to origin):** made `pp6q7r8s9t0u.upgrade()` and `downgrade()` IDEMPOTENT — guard each op (`currently_in_therapy`, `lead_source` columns; `consent_records` table; composite index `ix_consent_records_user_id_consent_type`) with `sa.inspect(op.get_bind())` existence checks. Edited the existing migration in place (it had never successfully applied to prod). Schema unchanged; 54 consent tests pass. Only `consent_records` is created by this one migration (no other migration/clinician-portal migration creates it).

**Lesson / how to apply:** This prod Postgres DB has ongoing drift (orphaned tables, enum label drift). New/edited migrations targeting it should be defensive/idempotent (inspector existence guards) rather than assuming a clean prior state. Migrations are MANUAL on Heroku — Procfile has NO `release` phase, so deploy does NOT auto-migrate; operator runs `heroku run alembic upgrade head` after the new slug is deployed.

**Backend repo facts:** `MindSync/` is its own git repo, branch `main`, remote `origin` = github.com/neuravec/MindSync.git. (Frontend is a separate repo on branch `dev`, see [[project_login_welcome_m3_redesign_2026_05_28]].) Heroku app name not stored in repo; CLI not authenticated in the agent sandbox (operator must run heroku commands).
