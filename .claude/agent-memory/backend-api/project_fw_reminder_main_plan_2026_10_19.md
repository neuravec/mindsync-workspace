---
name: fw-reminder-main-plan-2026-10-19
description: Plan-step reminder (FIRST_WEEK_STEP) now follows the 8-step Main plan, commit 1045891 on integration/redesign-v3-final (pushed); new route, 4 new copy keys, decisions not visible in code
metadata:
  type: project
---

2026-10-19: `reminder.py` (due, still_due, the cap reservation) reads `step_service.load_steps` instead of `plan_loader`; commit 1045891 on `integration/redesign-v3-final` (worktree MindSync-wt-integration-v3-final, from 1c6bf3c), pushed to origin only. No migration.

Decisions worth knowing:
- Rules: plan days 1..27 only; skip the day when any step `done_at` falls on today's plan date (04:00 boundary). `session` and `setup` count from the anchor, so saving a therapy date never reads as "done today".
- Free quota and the old "Not today" deferral are NOT rules any more (Main shows no quota state). Tone fail-closed and the two-ignored rule kept; ignored now also counts agenda/question/habit rows via `LoadedSteps.facts`.
- Route `/main-page/tab/main?section=first_week_plan`: the FE ignores unknown sections today (opens Main only); the FE needs one branch in `mc_main_screen._onScrollTarget` to open the plan sheet.
- `plan_step_session` is stored in `notification_logs.title`, like `therapy_prep`. That is DB only, never app logs or PostHog. It is a residual if anyone treats notification_logs as "logs".
- `test_push_privacy_h4` parametrizes over every PUSH_COPY key: adding keys adds ~43 tests per key to the notification suite count.

**Why:** a push could name a step other than the one Main shows; the client adds an opt-in switch on PUT /first-week/reminder.
**How to apply:** extend `reminder.active_step_template` and `step_service`, never `plan_engine`, for reminder changes. Literal U+2014 typed into a test file comes out as the real character: write `"\u2014"` through a script that encodes the escape. Related: [[project-mc-v3-first-week-steps-be1-2026-10-18]], [[project-first-week-be5-reminder]].
