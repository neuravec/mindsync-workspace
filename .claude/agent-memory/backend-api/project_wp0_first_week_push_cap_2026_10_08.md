---
name: project-wp0-first-week-push-cap-2026-10-08
description: WP-0 first-week push cap (push_cadence.enforce_daily_push_cap), why priority needs a schedule look-ahead, summary-ready activity gate, tracked .env gotcha
metadata:
  type: project
---

WP-0 of the first-week Home spec (design-specs/2026-10-07-first-week-home/SPEC.md s5, s7.7-9, s13) landed on branch `fw/be0-cadence` commit `01ce71e` (from `feat/first-week-home` 0c7d275), NOT pushed. No migration.

- Single cap owner: `app/services/push_cadence.py::enforce_daily_push_cap`, called from orchestrator Pass 1 (before winner render, so no AI cost), Pass 2, Pass 3 (`_daily_cap_allows` adapter) and `moment_hooks._create`. Accounts >= 8 days return "not_first_week" before any query.
- **Why a look-ahead exists:** POST_SESSION_REFLECTION (rank 1) is created only after the session starts, and THERAPY_PREP T-3h (rank 2) is already SENT by then, so displacement alone can never honour the priority. The cap reserves a day for a higher-ranked push still expected from the schedule (mirrors Pass 2 generator timing constants, imported from the generator modules). WP-1 must (a) fill `PLAN_STEP_MOMENT_TYPE` + `_plan_step_expected_on`, (b) switch `account_age_anchor` to first_week_started_at, (c) gate the look-ahead behind the same Art. 9 consent helper it puts on the generators, or days get reserved for pushes that never come.
- Account age rule: an instant > 5 min BEFORE created_at counts as "not first week". Many existing tests use a fixed past `now` with created_at = real now (server_default); treating negative age as week 1 would have capped them all.
- Summary-ready gate: `app/crud/user_activity.py::has_user_activity_between` (conversation, USER message, symptom score, debrief, note, recording, health check, habit check). Missing card row => no push.
- Admin broadcast and session_recording "summary ready" push deliberately NOT capped (operator action / reply to the user's own upload).

**Gotcha:** `.env` is a TRACKED file in the MindSync repo (`git ls-files .env`). Copying it into a worktree shows no diff (identical), and deleting it shows ` D .env`. Restore with `git checkout -- .env`; never `rm` it in a worktree. Flagged to the lead as a secrets-in-repo concern.

**Test-run gotcha:** the 94 notification/summary-related test files take ~9 min total; one foreground call over ~600 s gets auto-backgrounded and the piped output is lost. Split with `split -n l/4` and write each group's output to a scratch file. Baseline failures seen: test_notification_improvements x4, test_therapy_frequency year-boundary x1 (both fail on clean HEAD).

Related: [[notification-cadence-v3]], [[patterns-cancel-active-moments-by-type]]
