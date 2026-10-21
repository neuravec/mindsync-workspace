# MSV3.12 Habit Tracker – execution status (lead log)

Started 2026-09-02. **DEPLOYED 2026-09-02 ~16:50 CEST:** backend main 37b3f7b = Heroku release v546, `alembic upgrade head` applied (`alembic current` = m312a4b5c6d7 (head)), web/worker/scheduler up, no Traceback/H10/H12 in logs; frontend merged to dev (cdae5d7) and pushed (Codemagic -> TestFlight build in progress). Device QA still OPEN.
Final commits: backend `msv3.12` = c8795de, dc62712, 82fedcc, 40e34c9, affe9e2, 9cf969a, 37b3f7b (HEAD); frontend `msv3.12` = 0078fd4, 08e8d26, 734168f, 79d8c7a, 0aadbd1 (HEAD). Branches: backend `MindSync` `msv3.12` (from deployed main 728d48b),
frontend `mindsync-frontend` `msv3.12` (from dev 587f572). Nothing pushed by agents; the
operator deploys (push main = auto-deploy Heroku, push dev = TestFlight build).

Hard dependency MSV3.11 CS-08 (Homework removed from Main): SATISFIED, commit ecdf0f8 on dev.
Design colours: every hex in the design already exists in `MsColors` swatch shades, no new
palette needed, nothing to flag to Darek on colours.

Contract: `MSV3.12_API_CONTRACT.md` (this folder). Design: `design/Habit_Tracker.dc.html`.

## Task board

| ID | Task | Agent | Depends on | Status |
|---|---|---|---|---|
| BE-1 | CS-01 backend: models, migration m312a4b5c6d7, CRUD, endpoints, XP ledger, reflect ctx, tests | backend-api | none | DONE c8795de (44 tests green, migration idempotent, PG DDL compiled) |
| FE-A | Data layer + CS-02 weekly view + empty state + XP moment + registry + l10n + tests | flutter-mobile | contract (parallel with BE-1) | DONE 0078fd4 (30 tests green; token substitutions: #C2CFCC→MsColors.neutral[200], #C99A6E→sunsetOrange) |
| DA-1 | Wire `fetch_habit_context_for_prompt` into session-prep / weekly / monthly prompts in openai_service.py | data-analytics | BE-1 | DONE dc62712 (cron paths: weekly, monthly, prep auto-gen; manual Generate Now paths NOT covered, see BE-2) |
| FE-B | CS-03 edit mode: dashed frame, past-cell correction, drag reorder, editor sheet, premium gate, delete confirm | flutter-mobile | FE-A | DONE 08e8d26 (129 cubit + 72 widget tests green; reuses subscription route trigger 'habits' + showWorkspaceDeleteConfirm) |
| FE-C | CS-04 monthly view: dot heat-grid, checked/elapsed summary, month paging, read-only | flutter-mobile | FE-A (after FE-B, same files) | DONE 734168f (145 cubit + 89 widget tests green) |
| INT-1 | Contract verification backend vs Flutter | integration-devops | BE-1 + FE-C | DONE (2026-09-02) - GO, no blockers; report `Heroku/Business_requirements/MS_3/v3.12/INT1_CONTRACT_VERIFICATION.md`; re-ran BE tests (74 passed) + `flutter analyze`/`flutter test` on habit files (clean, 100 passed) |
| SEC-1 | Security review of the new user-data endpoints (scoping, premium gate, input) | security-guardian | BE-1 | DONE, no Critical/High, report `Heroku/security-reports/2026-09-02-msv312-habits.md` |
| BE-2 | Harden `fetch_habit_context_for_prompt` (SEC MED-002) + inject habit block inside crud gatherers so manual Generate Now paths get it too | backend-api | DA-1 | DONE 40e34c9 (lead re-ran test_habits + test_habits_ai_context: 74 passed; tree clean) |
| DA-2 | Remove the now-redundant `_append_habit_context` calls in the three cron task files (or guard on the `[Habits]` marker) | data-analytics | BE-2 | DONE 82fedcc (guard on `[Habits]` marker, 6 tests; full BE suite 5738 pass / 21 pre-existing fail = baseline) |
| QA-1 | Full backend suite + Flutter per-directory suites + analyze | qa-testing | all impl | DONE, GO: BE 300 targeted tests green, FE cubit 146 / widgets 89 (+1 known Mocktail) / api 129 / core 86; +5 gap tests (BE 9cf969a, FE 79d8c7a); report `QA1_REPORT.md` |

## Deploy checklist (operator)

Full trace behind these steps: `INT1_CONTRACT_VERIFICATION.md` (this folder) - GO
verdict, no blockers on either side. Reminder (CLAUDE.md): push to `main` deploys
the backend IMMEDIATELY (no release phase), and migrations are always run manually
afterward - never assume a push alone applied the schema.

### 1. Backend first (dependency: frontend calls the new routes)

```bash
cd MindSync
git checkout main
git pull
git merge msv3.12          # or: git merge --no-ff msv3.12
git push heroku main       # auto-deploys - live within ~1-2 min
heroku run alembic upgrade head --app mindsync   # revision m312a4b5c6d7
```

Verify before moving to step 2:
- `heroku logs --tail --app mindsync` (or `heroku logs -n 200 --app mindsync`) -
  confirm a clean boot (no traceback), and that `[Habits]`/`habits` shows up if
  you grep the startup log for the router mount; no `create_all`-related
  exception logged (that block only logs and continues, so absence of a
  traceback around boot is the signal, not its presence).
- `heroku pg:psql --app mindsync -c "\d habits"` (or `alembic current` via
  `heroku run alembic current --app mindsync`, expect `m312a4b5c6d7 (head)`) -
  confirms the migration actually applied, not just that `create_all` created
  the tables as a side effect.
- Smoke test from a real signed-in session (device or the app's existing
  API-testing flow): `GET /api/v1/habits` should return `200` with
  `{window, habits: [], limits}` for a fresh account, not `404`/`500`.

Rollback if the boot is unhealthy: `heroku rollback --app mindsync` (returns to
the previous release/728d48b's slug); the migration is additive-only (three new
tables, no altered columns) so it is safe to leave applied even after a code
rollback - nothing before this batch reads those tables.

### 2. Frontend (only after step 1's smoke test passes)

```bash
cd mindsync-frontend
git checkout dev
git pull
git merge msv3.12
git push origin dev        # triggers Codemagic -> TestFlight build
```

Device-QA checklist (from the spec's CS-02..04 Done-when lists plus INT-1's
failure-mode trace):
- Habits card renders in the old Homework slot (between Next Session and Mood
  Trend) with real data; empty state shows for a fresh account with its
  "Add your first habit" button opening the sheet.
- A good and a bad habit render their distinct teal-check / amber-shield cues
  and fills; only today's cell responds outside Edit mode, with the
  fill-and-bounce animation.
- Completing a week (7/7) shows the mint highlight + "+10 XP" chip, and the XP
  actually lands on the Character tab's orca total.
- Free account, second habit: "+ Add habit" opens the subscription screen
  directly (no sheet flash) - both from the empty-state button and Edit mode's
  footer row.
- Edit mode: dashed sand frame appears; a past cell in the current week can be
  checked/unchecked and the change survives an app restart; drag-reorder
  persists across restart; tapping a habit name opens the pre-filled editor
  sheet; Delete asks for confirmation and removes the habit from the list,
  the month view, and (indirectly, unverifiable from the UI) the AI context.
- Retro-completing the current week (checking several already-past days of
  the current week while in Edit mode) pays +10 XP exactly once, even across
  multiple corrections/un-checks within that same week.
- Monthly toggle swaps the card body without losing state; the grid matches
  the weekly data; chevrons page backward through past months only (right
  chevron disabled/dimmed on the current month); view is read-only (no dot
  responds to a tap).
- Kill and reopen the app - Weekly is always the default view on a fresh open,
  and the app does not crash or lose data if it was left open across a day
  boundary or timezone change.
- `flutter analyze` clean (already verified by INT-1, re-check if anything
  changed since).

If the frontend build ships before the backend deploy completes (out of order,
should not happen per the sequencing above): the Habits card silently
disappears from Main (verified by INT-1 - `GET /habits` 404s against the old
backend, the cubit's catch-all maps that to an error state the card renders as
nothing) rather than crashing or showing a false empty/onboarding state. No
rollback action needed in that scenario beyond completing step 1.

## Open questions for Darek
- SEC MED-001 (XP farming): the XP ledger is keyed by habit id and a hard delete cascades it, so delete + recreate + 366-day back-fill can re-earn the same weeks' XP without limit. This follows the spec's own rules (hard delete, retro weeks pay XP, unlimited premium habits). Options: accept (XP is cosmetic orca level), or keep a user-level award ledger keyed by (user, week_start, habit name hash) so a recreated habit cannot re-earn a week. Not changed this round, needs Darek's call.
- Character tab: the headline XP (`orca_total_points`) DOES include habit-week XP, but the per-activity breakdown list on that card has no "habit weeks" row (spec forbids touching gamification logic beyond the award call). Decide whether a breakdown row is wanted in a later round.

## Post-deploy fixes (2026-09-02 evening, operator session, no subagents)

### Add-habit failed with "something went wrong" (good and bad habits alike)
- Root cause: the app calls `POST /api/v1/habits` without a trailing slash, the router
  only registered `"/"` under the `/habits` prefix, so Starlette answered 307 -> `/habits/`.
  Dio follows redirects for GET only, never for POST, so every add died on the 307
  (Heroku router logs 18:33 UTC: five bare 307s, no follow-up). GET paid a second
  round-trip on every card load. `test_habits.py` used `/habits/` everywhere and INT-1's
  path row was marked MATCH by mistake, so nothing caught it before device QA.
- Fix: backend `f4e27e8` (release v547, 21:03 CEST) registers GET/POST at both `""` and
  `"/"` plus a no-redirect regression test; frontend `6d79e5b` on dev sets
  `Endpoints.habits = '/api/v1/habits/'` like every other collection constant plus a test
  pinning the trailing slash. Prod probe after deploy: `POST /api/v1/habits` -> 403 (auth),
  no 307. No migration involved.

### Related check (rest of MSV3.12)
- Item routes (`/habits/{id}`, `/habits/reorder`, `/habits/{id}/checks/{date}`) never had
  the slash problem. Response shapes match the Freezed models. AI-context injection and XP
  ledger untouched. Nothing else found broken.
