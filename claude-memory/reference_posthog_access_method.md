---
name: reference_posthog_access_method
description: "How to query PostHog in this env — MCP OAuth fails; use the posthog-data-extractor agent / scripts/posthog_query.py read-only REST runner"
metadata:
  node_type: memory
  type: reference
  originSessionId: 265b85f9-0735-4283-8ab9-5c8b981d47b2
  modified: 2026-08-10T05:43:10.531Z
---

PostHog query access in THIS environment: the **MCP PostHog OAuth flow does NOT complete** and wastes many turns. Observed 2026-06-29: full plugin scope → `invalid_scope`; narrowing to 15 read-only scopes lets the browser "Authorize" succeed, but `complete_authentication` then returns `No OAuth flow is in progress` because the plugin's pending-flow expires between turns. The localhost callback (e.g. `http://localhost:41451/callback`) is unreachable on a remote session, so the listener never catches the code.

**Working path (skip OAuth entirely):** read-only HogQL via the PostHog **REST query API** `POST /api/projects/{POSTHOG_PROJECT_ID}/query/` with header `Authorization: Bearer $POSTHOG_PERSONAL_API_KEY`. Values live in `MindSync/.env` (`POSTHOG_PERSONAL_API_KEY`, `POSTHOG_HOST`, `POSTHOG_PROJECT_ID=141170`, EU). Read-only, zero mutations. Never print the key.

**Since 2026-08-10 this is wrapped in a tool + an agent (use these, do not hand-roll):**
- `scripts/posthog_query.py` – stdlib read-only runner: `--check`, `--events [substr]`, `--props EVENT`, `--sql`, `--sql-file` (batch several queries in one call with `-- @@ label` separators), `--get PATH`, `--format table|csv|tsv|json`, `--out FILE`. Refuses mutating SQL locally, warns on PII fields / missing LIMIT, prints column headers. On Windows prefer `--sql-file` (quoting + `$` accessors).
- Agent **`posthog-data-extractor`** (Sonnet, read-only, `.claude/agents/`) owns the recipe + runner, verifies an event actually flows before reporting a number, saves raw extracts to `analytics-reports/raw/`. It is the extraction subcontractor for [[project_business_agents_track_2026_06_28]] `growth-analyst` (which interprets).

**HogQL gotchas (verified 2026-08-10):** `timestamp` is `DateTime64(6,'UTC')` → `windowFunnel` needs `toDateTime(timestamp)` (else `illegal_type_of_argument`), while `toDate`/`toStartOfWeek` take it raw. Count users with `count(DISTINCT person_id)`, not `distinct_id` (47 distinct_ids → 40 people/3d). Missing properties are `NULL` **or** `''` – filter both. `$app_version`/`$os`/`$screen*` are **client-event-only** – backend events (`api_error`, server-side `*_created`) don't carry them, so server-error splits must group by endpoint/status/time. Ingest started 2026-04-22. See [[reference_posthog_integration]], [[reference_posthog_dashboards]].
