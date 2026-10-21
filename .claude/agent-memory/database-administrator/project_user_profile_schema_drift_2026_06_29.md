---
name: project_user_profile_schema_drift_2026_06_29
description: Prod user_profile has two orphaned columns (country, about) not present in models.py — known schema drift, not a bug
metadata:
  type: project
---

Discovered 2026-06-29 via information_schema query on prod.

**Orphaned columns in prod `user_profile` not in current `models.py`:**
- `country` (character varying, nullable) — ordinal position 3, between user_id and pronouns
- `about` (text, nullable) — ordinal position 6, between gender and age

These are legacy columns from an earlier schema version. The model was updated to remove them but the columns remain in prod (no DROP COLUMN migration was run).

**Not a bug:** These columns don't affect current functionality. They're orphaned but harmless.

**How to apply:** When writing queries against user_profile on prod, expect these extra columns. Do NOT use `SELECT *` assuming columns match the model — use explicit column lists.

**Why:** Part of known prod schema drift (see CLAUDE.md: "prod has orphaned tables"). Same category as enum drift.
