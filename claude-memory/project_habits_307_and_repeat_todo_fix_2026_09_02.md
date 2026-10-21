---
name: project_habits_307_and_repeat_todo_fix_2026_09_02
description: "2026-09-02 evening: two post-MSV3.12 fixes done solo (no subagents). (1) Habit Tracker add-habit 'something went wrong' = POST /api/v1/habits 307 trailing-slash redirect Dio never follows; BE alias DEPLOYED v547 + FE endpoint fixed on dev. (2) Repeating to-do stays checked in the list -> FE-only behaviour change: leaves list, lands in Zrobione, backend rollover reopens it."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f64104b-203a-4bd5-9752-112f35dd9b6b
  modified: 2026-09-02T19:19:51.642Z
---

## Fix 1 – Habit Tracker: cannot add a good/bad habit ("something went wrong")

**Root cause (evidence: Heroku router logs 2026-09-02 18:33 UTC):** the Flutter client calls
`POST /api/v1/habits` (no trailing slash) while `app/api/v1/endpoints/habits.py` registered
the collection routes only at `"/"` under the `/habits` prefix. Starlette answered with
`307 Temporary Redirect` to `/api/v1/habits/`; Dio (dart:io HttpClient) follows redirects
for GET only, never for POST, so every add failed with a bare 307. GET "worked" only via a
second round-trip. Backend tests never caught it because `test_habits.py` always used
`/habits/`, and INT1_CONTRACT_VERIFICATION.md marked the path as MATCH by mistake.

**Fix, both sides:**
- BE `f4e27e8` on main -> Heroku **v547** (2026-09-02 21:03 CEST): GET/POST registered at
  both `""` (hidden from OpenAPI) and `"/"`; regression test
  `test_collection_routes_resolve_without_trailing_slash` (follow_redirects=False must give
  201/200). Prod probe after deploy: `POST /api/v1/habits` -> 403 (auth), no 307.
- FE `6d79e5b` (merge `49ecd7c`, dev `d5f61ff` after pulling Codemagic's "Pre-release
  updates" bump): `Endpoints.habits = '/api/v1/habits/'` like goals/symptoms/realizations/
  prep-cards, plus `test/api/endpoints_collection_trailing_slash_test.dart`.

**Rule to keep:** every FastAPI collection router here mounts at `"/"`, so Flutter collection
constants MUST end with `/` (item routes must not). A 307 in Heroku logs on a POST with no
follow-up request is this bug.

## Fix 2 – Repeating to-do stays in the list with a green check

Operator (Mikołaj) 2026-09-02: a ticked repeating to-do should vanish from the active list,
be recorded in "Zrobione" each time, and come back unchecked when the user's period
(daily/weekly/monthly) starts again. That replaces the CS-07 (MSV3.11, Darek 31.08)
"row stays checked in place until the period resets" UX.

**Backend needed no change:** `view=active` = OPEN only; `/done` logs `todo_completions`
and moves the item to `view=done`; `sweep_repeating_todos` lazily flips it back to OPEN at
the period start and stamps `reactivated_at` (sorts to top). FE-only commit on
`mindsync-frontend` branch `fix/todo-repeat-leaves-list` merged to dev: `TodoCubit.markDone`
always active -> archive; `undoRepeatingCompletion` + `TodoItemTile.onUndone` removed
(undo = archive Restore -> `/undone` voids that period's completion); tile plays the full
CS-08 draw-in + fade/collapse for repeating rows; tests updated (42 todo tests, 193 workspace
tests green).

**Known nuance (flagged to operator):** when the period rolls over the same row goes back to
OPEN, so it also leaves the "Zrobione" archive; the per-completion history survives only as
the "Done N× · last <date>" caption and `GET /workspace/todos/{id}/completions`. If a
persistent per-completion archive entry is wanted, that is a backend change to the done view
(one entry per completion or repeating items with completion_count>0 regardless of status).

**Process:** full BE suite = 23 fails / 5756 pass, all in the documented untouched-module
drift set (test_voice_fixes, test_therapy_frequency, test_notification_improvements, ...),
zero in habits/workspace. FE `test/screens/main_tab` has the known Mocktail compile failure
in `session_setup_screen_test.dart`. Heredoc python scripts with many quotes broke the Bash
tool parser once; writing the script to the scratchpad and running it worked.

Related: [[project_msv312_habit_tracker_2026_09_02]], [[project_msv311_threads_reflect_grace_batch_2026_09_02]],
[[reference_backend_autodeploy_on_push]], [[feedback_concurrent_session_git_hygiene]].
