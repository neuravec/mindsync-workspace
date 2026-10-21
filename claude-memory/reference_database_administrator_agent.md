---
name: reference_database_administrator_agent
description: "New database-administrator agent — owns the prod Postgres access know-how (heroku-dyno tunnel, REPL-safe scripts)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 265b85f9-0735-4283-8ab9-5c8b981d47b2
---

New agent **`database-administrator`** created 2026-06-29 (`.claude/agents/database-administrator.md`; model sonnet, color teal, memory project, read-mostly). Spawn it for operational prod Postgres work: read-only diagnostic/audit SELECTs, value fill-rate & data-integrity checks, schema/enum-drift inspection (model vs live prod), Alembic migration-state verification, row counts, data-quality bug triage (key-present-but-value-NULL = save-path bug signal). Deliverable: results + report under `db-reports/`. It does NOT own models/migrations/app code (that's `backend-api`) and runs no DML/DDL on prod without explicit operator approval.

Its crown-jewel knowledge (born from the 2026-06-29 onboarding-fill investigation): **you cannot reach the Azure Postgres from the local machine** — host `mindsync.postgres.database.azure.com` has no public DNS (`getaddrinfo failed`); installing a local driver does NOT help. **Access = `heroku run -a mindsync python < script.py`**, where the script MUST be **REPL-safe** (heroku allocates a PTY → python goes interactive REPL; no indented def/try/for blocks, inline list-comprehensions, end with `print("DONE_SENTINEL")`). NOT `python -c` (cmd shim breaks on spaces/parens). After results, `heroku ps:stop run.NNNN -a mindsync` (REPL keeps dyno alive). Complements [[reference_posthog_access_method]] (PostHog read path) and the heroku recipe in [[project_onboarding_extra_fields_unfilled_2026_06_29]].
