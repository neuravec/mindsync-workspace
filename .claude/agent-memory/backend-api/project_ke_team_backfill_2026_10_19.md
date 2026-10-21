---
name: project-ke-team-backfill-2026-10-19
description: KE full-history read for listed team accounts (scripts/ke_backfill_users.py, b694937 on feat/ke-team-backfill, unpushed); why reset-to-forward beats the hist_* read; local REPL recipe
metadata:
  type: project
---

b694937 on feat/ke-team-backfill (worktree MindSync-wt-ke-team-backfill, off origin/main 73081cc), NOT pushed. No app/ change; script runs against the deployed slug (v576) via `heroku run ... python < scripts/ke_backfill_users.py`, ids only from KE_BACKFILL_USER_IDS.

Route chosen: reset the read state to a forward-only read from `since` (read_plan=2, fwd_from=since via history.forward_cursors, hist_done=1, marker `team_since`, backfill_done_at/initial_sync_done cleared). extend-history when no KE output and no entry read (prod state of both accounts per DBA: forward-only, 0 KE rows); rebuild (delete output) otherwise, gated by user-acted items and KE_BACKFILL_REBUILD_OK=1; resume when the marker exists.

**Why:** cursors are id-based, so lowering a floor never reaches older rows; the hist_* read is premium-gated (worker cannot resume it for non-premium), its window is fwd-BACKFILL_DAYS, and crisis_at keeps only the newest date so an older crisis window is masked if a newer one is stored (G1 gap). Reset-to-forward needs no premium override and the worker continues it under normal limits.

**How to apply:** for any future "read more history for X" request, prefer the reset-to-forward pattern over hist_*; old moments alone do not form paths (compose needs 3 entries of a family in 60 days, shows newest 60 unassigned moments), tell the operator. Local REPL check: `py -3.12 -i < script` with DB_URL to a seeded sqlite, OPENAI_API_KEY=dummy, POSTHOG_ENABLED=false, POSTHOG_API_KEY= (tracked .env has real keys). Keep REPL lines < 1000 chars (canonical tty line limit 4095).
