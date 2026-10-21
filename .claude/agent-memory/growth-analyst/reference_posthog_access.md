---
name: posthog-access-fallback
description: How to query PostHog when the MCP OAuth flow fails — read-only HogQL via REST query API + personal API key from MindSync/.env
metadata:
  type: reference
---

# PostHog access — working method (MCP OAuth is unreliable here)

## MCP OAuth flow is BROKEN in this environment (verified 2026-06-29)
- `mcp__plugin_posthog_posthog__authenticate` full scope → browser returns `error=invalid_scope` (PostHog rejects some scope in the plugin's full list).
- Hand-built reduced read-only scope URL (reusing the plugin's `code_challenge`/`state`/`redirect_uri`) DID authorize (callback had `code=`), BUT `complete_authentication` then returned **`No OAuth flow is in progress`** twice — the plugin's pending-flow state expires between conversation turns (human round-trip > flow TTL). Auto-capture on localhost:PORT also never fired.
- Net: do NOT rely on the PostHog MCP here. Go straight to the REST fallback below.

## WORKING fallback: HogQL via REST query API + personal API key
- Creds live in `MindSync/.env`: `POSTHOG_PERSONAL_API_KEY`, `POSTHOG_PROJECT_ID` (=141170), `POSTHOG_HOST` (=https://eu.i.posthog.com). NEVER print the key value.
- Endpoint: `POST {HOST}/api/projects/{PID}/query/`, header `Authorization: Bearer <key>`, body `{"query":{"kind":"HogQLQuery","query":"<SQL>"}}`. Personal key has `query:read` (HogQL works — verified).
- Reusable helper (read query from stdin, never echoes key): I keep a `phq.py` pattern — reads the 3 vars from .env via regex, posts HogQL, prints `{columns,results,n}`. Recreate in scratchpad each session.
- Run via Bash: `cat <<'SQL' | python phq.py` ... `SQL`. Use quoted heredoc so bash doesn't touch `$app_version` etc. For date literals use `toDateTime('YYYY-MM-DD 00:00:00')` (single quotes inside SQL are fine in a heredoc).
- The dashboards build script `scripts/posthog_build_dashboards.py` uses the same key/pattern (good reference for REST shape; UI host = eu.posthog.com, API host = eu.i.posthog.com).
- Postgres (DATABASE_URL also in MindSync/.env) NOT reachable in this session: no PG driver installed (psycopg2/asyncpg/pg8000 all absent; SQLAlchemy 2.0.47 present but needs a DBAPI). So "transactional truth" queries (e.g. user_profile value-fill) can't run here without installing a driver — flag + hand off the SQL instead.

## HogQL gotchas hit (IMPORTANT for correctness)
- **`properties.X != ''` is UNRELIABLE for presence** — returns true even when the key is MISSING (gave has_text=count for `$screen`, and "identified persons"=every person). Use `JSONHas(properties,'key')` or `JSONExtractKeysAndValues(properties,'String')` to test/extract presence. Never gate fill-rate on `!= ''`.
- **`persons` table count is UNRELIABLE in this query API** (returned 102 one call, ~1469 another, depending on method). Don't compute person fill-rates off raw `persons`. Trust EVENT-level data (e.g. `profile_updated.updated_fields`) instead.
- `properties['$app_version']` (bracket) works; chaining `coalesce(nullIf(properties.$x,''),'null')` with GROUP BY 500'd ("ClickHouse error") — keep property access simple.
- `$app_version` IS captured on client events (mobile SDK auto-props: `$app_version`,`$app_build`,`$os`,`$device_*`,`$lib_version`). Backend events (`api_error`, `*_created`, `profile_updated`, `therapy_context_updated`) do NOT carry it → can't build-split server/backend events; split by endpoint/status+time instead.
- Results cap 100 rows default, max 500 via LIMIT. Always timestamp-filter `events`.

See also [[posthog-flowing-events-baselines]].
