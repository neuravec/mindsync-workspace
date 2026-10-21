---
name: feedback-heroku-cli-auth-blocked
description: When the Heroku CLI says "not logged in" / "Invalid credentials provided", do not inspect credential files (classifier blocks it as Credential Exploration); hand over a validated script and ask the operator to run `heroku login`
metadata:
  type: feedback
---

If `heroku auth:whoami` (or any `heroku run`) fails with `not logged in` or `Invalid credentials provided`, stop the prod-access attempt there. Do NOT read `~/_netrc`, `%LOCALAPPDATA%\heroku\*` or similar to diagnose it: on 2026-10-07 the auto-mode classifier denied that as "Credential Exploration" and forbids pursuing the same outcome by other routes. `heroku login` needs an interactive browser flow only the operator can do.

**Why:** 2026-10-07 first-week aggregates task. CLI was `heroku/11.11.0` (auto-updated); `_netrc` still existed but the CLI rejected it. The whole run was blocked; the only useful output was a ready-to-run script plus a methods report marked "results pending".

**How to apply:**
1. Check auth first with `heroku auth:whoami` before investing in the script, so the caller learns about the blocker early.
2. If blocked, still finish the deliverable that does not need prod: write the full REPL-safe script into `db-reports/`, validate it offline (see [[reference_offline_sql_validation_pglast]]), write the report with an explicit NOT EXECUTED status and the exact operator commands (Git Bash `<` redirect, or PowerShell `Get-Content -Raw file | heroku run -a mindsync --no-tty python`).
3. Never fabricate numbers; say plainly that the run is pending.

Related: [[reference_database_administrator_agent]], [[feedback_heroku_run_local_stdout_buffering]]
