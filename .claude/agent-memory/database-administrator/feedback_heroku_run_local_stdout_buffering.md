---
name: feedback-heroku-run-local-stdout-buffering
description: heroku run output redirected to a file can sit at 0 bytes for minutes even though the dyno already finished — don't assume it hung, don't double-launch
metadata:
  type: feedback
---

When running `heroku run -a mindsync python < script.py > outfile 2>&1` in the background (Bash `run_in_background: true`), the local `outfile` can stay at **0 bytes for several minutes** even after the remote dyno has fully executed the script and is sitting idle at the `>>>` prompt (per the normal, expected REPL-hang behavior in the access recipe). This looks identical to "the dyno never started" or "it's hung" but isn't — it's the local heroku CLI (Node) buffering its own stdout when that stdout is redirected to a file instead of a real TTY, only flushing once enough data accumulates or something forces it (observed: after issuing `heroku ps:stop` on an *unrelated* stray dyno, the file for the still-running one also flushed — timing suggests it may just have crossed a buffer-size threshold around the same time, not that stopping caused it).

**Why:** On 2026-08-16, first attempt used a redundant trailing `&` inside a command that was ALSO passed `run_in_background: true` — this double-backgrounds the job, the wrapper shell returns almost instantly ("launched bg pid"), and the actual `heroku run` process's output never reliably reached the redirected file (this attempt's dyno was one of two strays cleaned up). A clean second attempt (no trailing `&`, just `run_in_background: true` on the Bash call itself) also sat at 0 bytes for ~4 minutes before the full session (including `DONE_SENTINEL`) appeared all at once.

**How to apply:**
1. Never add a manual trailing `&` to a command already passed `run_in_background: true` — that's double-backgrounding and makes the job un-trackable (no `run.NNNN` line ever reliably reaches you). Let the Bash tool's own backgrounding handle it.
2. If the outfile is still 0 bytes after ~1-2 min, don't assume failure — check `heroku ps -a mindsync` for a `run.NNNN up` line first; if a run dyno is up, the query likely already finished and is just buffered locally. Keep polling (up to the ~5 min budget in the access recipe) rather than killing and relaunching, which just creates stray duplicate dynos to clean up (both had to be `ps:stop`'d this session — `run.7137` and `run.9114`).
3. Always reconcile with `heroku ps -a mindsync` before assuming a launch failed — it's the ground truth for whether the dyno is actually up, independent of local output buffering.

Related: [[reference_database_administrator_agent]], [[project_hi001_receipt_reuse_check_2026_08_16]]
