---
name: project-mc-v3-be2-recap-gate-2026-10-18
description: MC v3 BE-2 on feat/main-v3 (831bd4f..fe35bb3, not pushed) - recap step gate, rhythm null before day 7, cache TTL 29d, last7 habits, entry_count, Focus Areas label; residuals
metadata:
  type: project
---

BE-2 of team main (2026-10-18), commits `831bd4f` `5ec0d6d` `a7711a6` `8aa2eaf` `fe35bb3` on `feat/main-v3`
(worktree `MindSync-wt-main-v3`), NOT pushed. Contract: team scratchpad `teams/main/API.md` sections 2 to 4.

Non-obvious decisions:
- Recap gate lives in `recap.recap_open(ctx)` (old window OR `StepGate.ready` and plan_day <= 27). The JOB body
  (`_prepare_noticed`) gated on `plan.recap_available` too, so changing only `open_recap` would have left early
  recaps without "Orca noticed". Unreadable step plan where only the gate could open it = 503 / counted job failure.
- Cache TTL had to move to anchor + 29 days (`CACHE_TTL_LAST_RECAP`): with the old 16 days a gate recap after day 16
  got a 1-second TTL, so every open re-queued a model call. `CACHE_TTL_AFTER_ANCHOR` (16d) kept for the sweep only.
- `rhythm` is null before plan day 7 (schema made Optional): the shipped Flutter recap already treats null as
  "no rhythm card, Done closes", while an empty list would have PUT /rhythm and hit 422 rhythm_not_allowed.
- Gate-open recap is never `quiet`; `did` merges step-plan talk/talk2/note/checkin (old engine counts a step
  only on its planned day). Accounts without the gate get byte-identical old sections; /plan proven
  byte-identical vs base via a throwaway probe in both worktrees.
- `entry_count` mirrors `_gather_week_data`: recordings cap is 3 (task said 5), content field must be set;
  new module `app/crud/weekly_observation_entries.py` to stay out of the workspace team's crud file.

Residual reported, not fixed (plan_engine off limits): an early recap open (day 1 to 6) is not done for the
old engine's day-7 recap slot, so the old plan-step reminder can still push the recap on day 7 (reminder-on only).

**Why:** integration merges three teams; FE builds Main against API.md.
**How to apply:** extend `recap_open`/`StepGate`, never `plan_engine.recap_available`. See
[[project_mc_v3_first_week_steps_be1_2026_10_18]].
