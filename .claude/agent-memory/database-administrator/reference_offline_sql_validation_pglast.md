---
name: reference-offline-sql-validation-pglast
description: pglast (real Postgres parser) and SQLAlchemy 2.0 are installed locally; a fake app.db.session lets you dry-run a dyno script offline to catch SQL syntax errors, stray :bind params and non-REPL-safe lines before spending a dyno run
metadata:
  type: reference
---

The local Python has `pglast` (libpg_query, the actual Postgres grammar) and SQLAlchemy 2.0.x. No local `psql`/Postgres server. Use them to dry-run a dyno script before running it on prod:

- Put a fake package on `sys.path`: `fake/app/db/session.py` with `SessionLocal()` returning an object whose `execute(text_obj)` compiles with `postgresql.psycopg2.dialect()`, flags any `comp.params` (accidental `:name` bind params inside SQL literals), un-doubles `%%` and runs `pglast.parse_sql(sql)`; `fetchall()` returns `[]`.
- Also `compile(line, name, "single")` on every script line and flag lines starting with whitespace: that proves the script is REPL-safe for the PTY `heroku run` path.
- `exec` the whole script against the fake; expect `DONE_SENTINEL`.

It catches grammar and bind-param mistakes only. Column existence, enum labels and cast failures on real data still need the live run (put a schema/enum check query first in the script).

First used 2026-10-07 (65 statements, 0 problems). Related: [[feedback_heroku_cli_auth_blocked]]
