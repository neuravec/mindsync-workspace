---
name: reference-dyno-script-per-query-txn
description: Robust dyno-script pattern - a one-line exec() helper runs every query in its own READ ONLY transaction with a timeout and always rolls back, so one bad query cannot abort the rest; --no-tty runs report local exit 1 even on success
metadata:
  type: reference
---

Pattern used on 2026-10-19 (26 queries, 0 errors):
- Define the helper on a single REPL-safe line: `exec("def run(label, sql):\n    ...try: SET TRANSACTION READ ONLY; SET LOCAL statement_timeout = 90000; fetchall; print rows\n    except: print QUERY_ERROR\n    finally: db.rollback()")`. Each query gets its own transaction, so a missing column or a cast error prints QUERY_ERROR and the next query still runs. Nothing is ever committed.
- Generate the dyno script from a Python builder file written with the Write tool (SQL in triple quotes, whitespace collapsed, embedded with `repr()`). Do NOT generate it through a Bash heredoc: the shell ate one backslash level and turned `\n` into real newlines, which broke the exec line.
- `heroku run -a mindsync --no-tty --size=basic python < script.py > out 2>&1` (Git Bash) exits on its own, but the local command reports **exit code 1 even when the script reached DONE_SENTINEL**. Judge the run by the sentinel and the QUERY_ERROR/Traceback lines, not by the exit code. Afterwards confirm `heroku ps` shows no `run.*` dynos.
- Put a schema check first: a `VALUES` list of (table, column) LEFT JOINed to information_schema.columns, printing MISSING, plus the enum labels of every enum column the queries filter on.

Related: [[reference-offline-sql-validation-pglast]], [[feedback-heroku-run-local-stdout-buffering]]
