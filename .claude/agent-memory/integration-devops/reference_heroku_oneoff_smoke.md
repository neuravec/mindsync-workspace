---
name: reference-heroku-oneoff-smoke
description: How to run Heroku CLI and a read-only post-deploy smoke on a one-off dyno from this Windows machine without the run hanging (HEROKU_API_KEY from _netrc, REPL-safe script ending in exit(), timeout wrapper)
metadata:
  type: reference
---

- **Auth:** the Heroku CLI login is invalid on this machine. Per command: `export HEROKU_API_KEY=$(awk '/api.heroku.com/{f=1} f&&$1=="password"{print $2; exit}' ~/_netrc)` (Git Bash; file is `~/_netrc`, not `.netrc`). Never echo the key.
- **Checking a Config Var without leaking it:** capture `heroku config:get NAME` into a variable and print only set/unset and its length.
- **One-off smoke:** `timeout 240 heroku run -a mindsync --size=basic python < script.py > out.txt 2>&1` in the foreground. The script must be REPL-safe (one statement per line, see the database-administrator agent file) and **end with `exit()`**: then the dyno exits by itself, no `heroku ps:stop` needed, and `heroku run` returns exit code 1, which is normal. Grep `out.txt` for your `SMOKE` lines and `DONE_SENTINEL`, then confirm with `heroku ps` that no `run.N` is left.
- **Release polling:** `heroku releases -a mindsync -n 3`; the table's first data row is line 5, not 4 (line 4 is a separator). Push to `origin/main` auto-deploys; v563 appeared about 80 s after the push. `heroku builds` does not exist in this CLI.
- **Logs:** `heroku logs -n 1500` covers only about 10 minutes when the notification orchestrator tick is running (worker floods). Filter by timestamp with `awk '$1 >= "<ISO>"'` and redact emails and the Redis URL before quoting.

Used for [[project-recap-voice-floor-deploy-2026-10-06]].
