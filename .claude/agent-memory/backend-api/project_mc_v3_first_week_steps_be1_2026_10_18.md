---
name: project-mc-v3-first-week-steps-be1-2026-10-18
description: GET /first-week/steps (Main MC v3, 8 steps no days) on feat/main-v3 commit 34547d1; wire-set literal trap, session done_at, /plan side effects, 405 bypasses NoStoreRoute
metadata:
  type: project
---

BE-1 of team main (2026-10-18): `GET /api/v1/first-week/steps`, commit `34547d1` on `feat/main-v3`
(worktree `MindSync-wt-main-v3`), NOT pushed. Contract lives in the team scratchpad `teams/main/API.md` section 1.
Old `/first-week/plan` engine untouched; new pure engine `app/services/first_week/step_plan.py`.

Non-obvious points:
- `test_first_week_constants::test_no_other_module_redefines_the_wire_sets` greps EVERY non-test app module for the
  literals `"talk2"`, `"quota_out"`, `"today.`, `"step.`, `"before_after_session"`. New code must import
  `plan_engine.STEP_TALK2` etc. instead of retyping them (also watch docstrings).
- `session` step: the therapy schedule has no stored creation instant, so `done_at` = the anchor. Pop-out ordering
  on the client is the only consumer of `done_at`.
- `therapy_consent.therapy_schedule_if_consented` fails closed (read failure == no consent == variant C), so
  "503 on any read failure" has that one documented exception, same as the old plan.
- `/plan` GET carries side effects `/steps` does not: first-week client marker + follow-up question request
  (`plan_service.first_week_client_task`). Main must keep calling `/plan` or those break.
- Starlette answers a wrong-method 405 before the route handler, so `NoStoreRoute` cannot add `no-store` to it.
- Clean-process boot probes can reuse `_PRELUDE` from `app/tests/test_first_week_api_boot.py` (~25 s each).

**Why:** BE-2 (recap gate, last7 habits, entry_count) builds on this branch next; integration merges three teams.
**How to apply:** extend `step_plan`/`step_service` rather than `plan_engine`; keep the variant out of logs and repr.
See [[project_wp0_time_zones_2026_10_08]] for the tz helpers used (`resolve_tzinfo`).
