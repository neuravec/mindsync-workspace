---
name: project_msv312_habit_tracker_2026_09_02
description: "MSV3.12 Habit Tracker (Grace) batch, implemented 2026-09-02 on branches msv3.12 in both repos, COMMITTED not pushed; migration m312a4b5c6d7; XP ledger on orca track; deploy sequence and open questions for Darek"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4151fb09-e291-4a14-900f-0ad48c6a67ae
  modified: 2026-09-02T13:03:18.984Z
---

MSV3.12 "Habit Tracker" (spec by Darek 31.08.2026, 4 CHANGE items: CS-01 backend, CS-02 weekly
view, CS-03 edit mode + sheet, CS-04 monthly view). Implemented 2026-09-02.

**State (evidence-based):** DEPLOYED 2026-09-02 ~16:50 CEST. Backend main fast-forwarded to 37b3f7b and pushed -> Heroku release v546; `heroku run alembic upgrade head` ran m311c3d4e5f6 -> m312a4b5c6d7, `alembic current` = m312a4b5c6d7 (head); all dynos up, logs clean. Frontend dev merged (cdae5d7, no-ff) and pushed -> Codemagic/TestFlight. Device QA NOT done yet.
Branch history: Backend `MindSync` branch `msv3.12` (from
deployed main 728d48b): c8795de, dc62712, 82fedcc, 40e34c9, affe9e2, 9cf969a, 37b3f7b = HEAD.
Frontend `mindsync-frontend` branch `msv3.12` (from dev 587f572): 0078fd4, 08e8d26, 734168f,
79d8c7a, 0aadbd1 = HEAD. Gates: security-guardian no Critical/High; integration-devops GO;
qa-testing GO (full BE suite 5750 pass / 21 pre-existing baseline fails; FE per-directory green,
1 known Mocktail failure in session_setup_screen_test.dart). Device QA NOT done (operator).

**Where things live:** `Business_requirements/MS_3/v3.12/`: spec, `MSV3.12_API_CONTRACT.md`
(source of truth for both sides), `STATUS.md` (task board + operator deploy checklist + open
questions), `INT1_CONTRACT_VERIFICATION.md`, `QA1_REPORT.md`, `design/Habit_Tracker.dc.html`
(extracted from the Claude Design zip; the original design file is a ZIP without extension).
Security report: `Heroku/security-reports/2026-09-02-msv312-habits.md`.

**Key decisions:** XP on the ORCA track via `crud.award_orca_track_points` with a
`habit_week_awards` ledger (unique habit_id + week_start) as the idempotency source record;
`ORCA_TRACK_POINTS["habit_week"] = 10`; `type` is String(8) + constants; check endpoint is an
idempotent PUT with explicit `checked`; free tier = 1 active habit via
`_therapy_helpers.is_user_premium` (403 `premium_required`), client gates on `limits.can_add`;
week = `UserProfile.first_day_of_week`, tz = `UserPreferences.time_zone`; habit AI context is
injected ONCE inside `crud.gather_weekly_summary_data` / `gather_prep_card_context` (marker
`[Habits]`, names sanitised), the three cron task files guard on the marker. Migration
`m312a4b5c6d7` (down_revision m311c3d4e5f6) is idempotent against create_all-at-boot.
Main registry: `'habits'` sits between `next_session` and `mood_trend` in
`mainTabDefaultWidgetOrder` (no per-user override exists, so every user gets it).

**Open for Darek:** (1) SEC MED-001 XP farming via delete + recreate + 366-day back-fill
(follows the spec's own rules; accept or add a user-level ledger); (2) Character tab activity
breakdown has no "habit weeks" row (headline XP does include it).

**Deploy done as:** push origin/main -> poll `heroku releases -n 1` until the new release -> `heroku run --no-tty -a mindsync "alembic upgrade head"` (git push via PowerShell tool, Bash push may be blocked). Device-QA list in STATUS.md.

**Process lessons this batch:** two agents committing concurrently in the same backend working
tree worked but needed care (one had to split the other's uncommitted test class out of a shared
file); flutter-mobile once wrote its agent memory under Business_requirements (moved back to
`MindSync/.claude/agent-memory/flutter-mobile/`); a mechanical em-dash sweep on the branch diff
was still needed at the end (10 occurrences) despite prompts forbidding it.
Related: [[project_msv311_threads_reflect_grace_batch_2026_09_02]], [[reference_backend_autodeploy_on_push]],
[[feedback_agents_stop_on_background_jobs]], [[feedback_concurrent_session_git_hygiene]].
