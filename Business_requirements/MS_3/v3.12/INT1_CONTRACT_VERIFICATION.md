# MSV3.12 Habit Tracker – INT-1 contract verification (integration-devops, 2026-09-02)

Verified against `MSV3.12_API_CONTRACT.md` v1. Backend branch `msv3.12` @ affe9e2
(commits c8795de, dc62712, 82fedcc, 40e34c9 + one memory-only commit).
Frontend branch `msv3.12` @ 734168f (commits 0078fd4, 08e8d26, 734168f). Both
branches diverge cleanly from their deployed bases (backend main 728d48b,
frontend dev 587f572) – nothing else pushed in between.

Evidence gathered by reading both sides file:line, plus two live checks:
`python -m pytest app/tests/test_habits.py app/tests/test_habits_ai_context.py -q`
(74 passed) and `flutter analyze` + `flutter test` on the habit files/tests
(clean; 100 tests passed across the four habit test files).

## 1. Endpoint-by-endpoint match

### GET /habits?window=week|month&anchor=YYYY-MM-DD

| Piece | Backend | Flutter | Verdict |
|---|---|---|---|
| Path/method | `router.get("/")` mounted at prefix `/habits` (`app/api/v1/endpoints/habits.py:110`, `app/api/v1/api.py:330-335`) → `/api/v1/habits` | `Endpoints.habits = '/api/v1/habits'` (`endpoints.dart:381`), `HabitsManager.listHabits` (`habits_manager.dart:42-54`) | MATCH |
| `window` default | `Literal["week","month"] = Query(default="week")` (habits.py:112) | `listHabits({String window = 'week', ...})` (habits_manager.dart:43) | MATCH |
| `anchor` | optional `date`, default = today server-side (habits.py:113,119) | passed only when non-null (habits_manager.dart:49-51) | MATCH |
| 400 future_window | `is_future_window` check (habits.py:122-123) | FE never constructs a future anchor (`goToNextMonth` blocks via `isHabitCurrentMonth`, cubit.dart:100-109); defense-in-depth on the backend regardless | MATCH |
| Response shape `{window, habits, limits}` | `HabitListResponse` (schemas/habit.py:142-145) | `HabitListResponseModel{window, habits, limits}` snake-rename (habit_list_response_model.dart) | MATCH |
| `habits` order | `sort_order asc, id asc`, archived excluded (crud/habit.py:195-202) | FE never re-sorts (doc comment, habit_list_response_model.dart:10-11) | MATCH |

### POST /habits

| Piece | Backend | Flutter | Verdict |
|---|---|---|---|
| Body `{name, type}` | `HabitCreate` (schemas/habit.py:46-60), 1..80 trimmed, type∈{good,bad} | `{'name': name, 'type': type}` (habits_manager.dart:70) | MATCH |
| 201 → HabitResponse (week window of today) | `_week_response_for_today` (habits.py:169, 94-102) | `HabitModel.fromJson` (habits_manager.dart:72) | MATCH |
| 403 `premium_required` | `raise HTTPException(403, "premium_required")` (habits.py:166); same literal string as `monthly_audits.py:680` (`MonthlyAuditPremiumRequiredException` precedent) – the contract's own instruction ("verify the exact detail string other premium gates use") was followed | `HabitPremiumRequiredException` on `statusCode == 403` (habits_manager.dart:73-76) – matches on status code alone, not the string, so it's robust even if the string had differed | MATCH |
| 422 validation | Pydantic (`_validate_name_value`/`_validate_type_value`, schemas/habit.py:26-38) | not FE-constructed (Save disabled on empty name; type is always one of two picker values) | MATCH |

### PATCH /habits/{habit_id}

Body `HabitUpdate` requires ≥1 field (`model_validator`, schemas/habit.py:83-87) ↔ FE only sends the changed field(s) (habits_manager.dart:86-93, always at least `name` since the sheet requires it). 404 `habit_not_found` on missing/cross-user habit (habits.py:215-217) ↔ FE's `updateHabit` has no special 404 handling and lets it bubble to the sheet's generic catch (habit_editor_sheet.dart:97-103) – acceptable, see §2. MATCH.

### PUT /habits/reorder

Body `{habit_ids: [...]}`, must be exactly the caller's active-id set else 422 (habits.py:183-189) ↔ FE always derives `habitIds` from the currently-loaded, currently-displayed `state.habits` list (habits_card.dart:361-367, `onReorder`), so the sets can only disagree if a mutation raced in in another tab – handled by the cubit's catch-and-rollback (habits_cubit.dart:282-291). Response `{habits: [...]}` (`HabitReorderResponse`) ↔ `HabitReorderResponseModel.habits` (habit_reorder_response_model.dart). MATCH.

### DELETE /habits/{habit_id}

204, hard delete, cascades checks + `habit_week_awards` (explicit pre-delete queries, crud/habit.py:263-278 – not relying solely on DB `ondelete=CASCADE` because SQLite tests don't enforce it without `PRAGMA foreign_keys=ON`, matching the `delete_thread` precedent) ↔ `HabitsManager.deleteHabit` (habits_manager.dart:110-112), cubit refetches the week list afterward so the freed `limits.can_add` slot shows up immediately (habits_cubit.dart:252-262). MATCH.

### PUT /habits/{habit_id}/checks/{date}

| Piece | Backend | Flutter | Verdict |
|---|---|---|---|
| Idempotent PUT, explicit target state | `HabitCheckRequest{checked: bool}` (schemas/habit.py:96-100), `set_check` sets/deletes exactly (crud/habit.py:320-336) | `setCheck(habitId, date, {required bool checked})` passes explicit `!wasChecked` (habits_manager.dart:119-129; cubit toggleToday/toggleDay) | MATCH |
| 400 `future_date` | `check_date > today` (habits.py:262-263) | `toggleDay` bails client-side before the call if `isoDate > today` (habits_cubit.dart:309); `toggleToday` only ever sends `today` itself, never future | MATCH (defense-in-depth both sides) |
| 400 `date_too_old` (366d floor) | `(today - check_date).days > BACKDATE_FLOOR_DAYS` (habits.py:264-265, crud/habit.py:50) | FE has no reachable path to send a date >366d old today (Weekly view only ever shows/edits the current 7-day window – see §3 note) | MATCH (unreachable on FE today, correctly guarded server-side regardless) |
| Response `{habit, week_completed_now, xp_awarded}` | `HabitCheckResponse` (schemas/habit.py:152-156); `habit` = week window CONTAINING `check_date` (habits.py:297-299); `week_completed_now` true only on this call's 7/7 transition (habits.py:278-281); `xp_awarded` 10 only on first-ever award (habits.py:283-295, idempotency via `HabitWeekAward.xp_awarded` + `award_orca_track_points`'s own `xp_awarded` short-circuit at `crud/crud.py:6916-6919`) | `HabitCheckResponseModel{habit, weekCompletedNow, xpAwarded}` (snake-rename); cubit shows the XP chip only on `xpAwarded > 0`, never derives it from `weekCompletedNow` alone (doc comment, habit_check_response_model.dart:12-16; habits_cubit.dart:396-402) | MATCH |

## 2. Failure-mode tracing (CLAUDE.md rule 6)

Every mutating cubit method (`load`, `createHabit`→sheet, `updateHabit`→sheet,
`deleteHabit`, `reorder`, `toggleDay`, `toggleToday`, `_fetchMonth`) wraps its
network call in try/catch with **no rethrow that could be mistaken for
"no data"** anywhere except the two documented rethrows (`createHabit`,
`updateHabit` – both awaited synchronously by the editor sheet, never by the
card itself).

| Backend condition | Flutter handling | Verdict |
|---|---|---|
| **401** (bad/expired Firebase token) | Not intercepted specially by `HabitsManager` – propagates as `ApiException(statusCode: 401)`. `load()`'s catch-all → `HabitsState.error` → card renders `SizedBox.shrink()` (habits_card.dart:94, comment: "Minor module – degrade silently rather than a scary error card"). Global 401 handling (token refresh / re-auth) is the Dio interceptor's job app-wide, orthogonal to this module – not something Habits should special-case. | OK – never shown as empty state (see below), never onboarding |
| **403** `premium_required` (create only) | `HabitPremiumRequiredException`, caught by the editor sheet, routes to the subscription screen via `Navigator.pop(true)` → `HabitsCard`'s listener → `context.push(MsRoutes.subscriptionRouteWithTrigger(...))` (habits_card.dart:80-84). The "+ Add habit" entry points additionally gate on `limits.canAdd` BEFORE opening the sheet at all (habits_card.dart:109-117, 300, 523), so this exception path is the defensive fallback for a race, not the primary path. | MATCH contract's explicit requirement ("free-tier 403 must route to the subscription screen") |
| **404** `habit_not_found` (PATCH/DELETE/checks on a missing/cross-user habit) | No special handling anywhere on the FE – becomes a generic `ApiException`, caught by the same catch-all as any other failure in each method (rollback + `toastKey: 'error_somethingWentWrong'` for `toggleDay`/`toggleToday`/`reorder`; generic inline error for the editor sheet's update path; silent toast for delete). This can only actually fire if a habit was deleted in another session/tab between load and action – an edge case, and the fallback (toast + optimistic rollback, or generic sheet error) is safe and never confused with "no habits". | OK – no crash, no false empty state |
| **400** `future_date`/`future_window`/`date_too_old` | Pre-empted client-side wherever the UI can construct one (future cells are `HabitDayCellKind.futureLocked` and non-tappable in every mode, habits_cubit.dart:466 `resolveHabitDayCellKind`; `goToNextMonth` blocks past `today`'s month). If the server still rejects (clock skew, or a value outside what the FE currently constructs), it falls into the same generic catch → rollback + toast. Never crashes, never shown as success. | OK |
| **422** (reorder id-set mismatch, PATCH with zero fields) | Same generic catch. `reorder`'s optimistic list is rolled back to `original` + toast (habits_cubit.dart:287-291) – the drag visually snaps back rather than silently "succeeding". | OK |
| **5xx** | Same generic catch-all everywhere; no code path distinguishes 5xx from 4xx, which is fine here since every case above already degrades safely (error state / rollback+toast / sheet inline error), never as "empty" or onboarding. | OK |
| **Network timeout** (no response) | `DioClient._handleError` (dio_client.dart:329-341) converts any `DioException` (including connect/receive timeout, no `err.response`) into `ApiException(statusCode: null, ...)`. Falls into the exact same generic catch-all as any other failure. | OK |

**Empty state vs. error state – explicitly distinct**, verified by reading
`_HabitsBody.build`'s `switch` (habits_card.dart:88-99):
- `HabitsLoading()` → spinner card
- `HabitsError()` → `SizedBox.shrink()` (card vanishes entirely – "minor
  module" convention shared with the deleted Homework card)
- `HabitsLoaded()` with `habits.isEmpty` → `_HabitsEmptyCard` (illustration +
  "Small daily wins add up" + Add button)

A backend error can only ever reach the `HabitsError` branch (every catch in
`load()` maps to `HabitsState.error`), never the empty-habits branch, which
requires a **successful** `200` with an empty `habits: []` array. The two are
structurally impossible to conflate from this code path. **No onboarding
push exists anywhere in this module** – confirmed by grep, there is no
`context.push`/`context.go` to any onboarding route in `habits_cubit.dart`,
`habits_card.dart`, `habit_editor_sheet.dart`, or `habits_month_view.dart`;
the only navigation call in the whole feature is the subscription-screen
push on the premium gate.

**Optimistic-update rollback** verified for both `toggleToday` (habits_cubit.dart:373-412)
and `toggleDay` (habits_cubit.dart:305-339) and `reorder` (habits_cubit.dart:268-292):
each emits the optimistic state first, and on any caught exception re-emits
the pre-mutation `original` value plus `toastKey: 'error_somethingWentWrong'`.
`createHabit`/`updateHabit` do not need a rollback (nothing was optimistically
applied before the await resolves).

## 3. Deploy sequencing

- **Migration idempotency vs. `create_all()` boot race**: `app/models/__init__.py`
  imports `app.models.habit` (line added this batch, `git diff` confirmed),
  so `Base.metadata.create_all(bind=engine)` at every web-dyno boot
  (`app/main.py:85`, wrapped in `try/except Exception` that only logs –
  never crashes the dyno, lines 84-90) will create `habits`/`habit_checks`/
  `habit_week_awards` on first boot of the new code, before anyone runs
  `alembic upgrade head`. The migration itself (`m312a4b5c6d7_create_habit_tables.py`)
  guards every `create_table`/`create_index` with `if not _table_exists(...)`,
  so running it afterward against a DB `create_all()` already populated is a
  safe no-op. `down_revision = "m311c3d4e5f6"`, which matches the confirmed
  prod alembic head (per project memory, verified on prod 2026-09-02) – no
  branch/merge conflict in the chain.
- **New code, backend not yet migrated**: covered by the point above –
  `create_all()` makes the endpoints fully functional even before the
  explicit `alembic upgrade head` run. Running the migration afterward is
  still required so the alembic version table stays truthful (CLAUDE.md
  "deploy != migrate" rule), but it is not a crash-prevention dependency
  here.
- **New FE build, OLD backend** (i.e., if frontend somehow reached
  TestFlight before the backend deploy – not the intended order, but traced
  per the task's request): `GET /habits` 404s (route doesn't exist yet).
  `HabitsCubit.load()`'s catch-all → `HabitsState.error` → the card renders
  `SizedBox.shrink()` – the whole Habits card silently disappears from Main,
  the rest of the app is unaffected. No crash, no stuck spinner, no false
  empty-state, no onboarding redirect. Degrades gracefully.
- **New backend, OLD FE** (the actual interim state between the two deploy
  steps in the checklist below): the old app never calls any `/habits`
  route (doesn't know it exists) – harmless, purely additive on the backend
  side. Confirmed no existing endpoint/schema/model was modified, only new
  files added plus three purely-additive call sites in
  `app/api/v1/endpoints/reflect.py` and the three cron task files (guarded
  behind a `"[Habits]" in therapy_context` marker check so even a double
  call is idempotent, not just harmless).
- **Scope check** – `git diff --stat 728d48b..affe9e2` for the whole batch:
  **no changes to `Procfile`, `requirements.txt`, `.env.example`, or
  `app/core/rq_scheduler_setup.py`** (confirmed absent from the diff). The
  three cron task files touched
  (`monthly_therapy_audit.py`, `prep_card_auto_generate.py`,
  `weekly_therapy_summary.py`) only add a private `_append_habit_context`
  helper and one call site each into their existing generation flow – no
  new registration, no new schedule, no new queue. No env var is introduced
  by this batch.

## 4. Deploy checklist

Written into `STATUS.md` (see the replaced "Deploy checklist" section at the
bottom of that file) – summary here for reference:

1. Backend: `git checkout main && git merge msv3.12 && git push heroku main`
   (auto-deploys), then immediately
   `heroku run alembic upgrade head --app mindsync`. Verify via
   `heroku logs --tail --app mindsync` (grep for `[Habits]`/`habits` router
   mount and absence of tracebacks) and a smoke `GET /api/v1/habits` from a
   real signed-in session (expect `200` with `window`/`habits`/`limits`, not
   `404`/`500`).
2. Frontend: merge `msv3.12` → `dev`, push → Codemagic → TestFlight. Device
   QA per the spec's CS-02..04 done-when lists, especially: XP lands on the
   Character tab; free user's "+ Add habit" opens the subscription screen
   (not the sheet); a retro-completed week (checking several past days of
   the current week in Edit mode) pays +10 XP exactly once even across
   multiple toggles.

## 5. Open questions for Darek

No new open questions beyond the two already logged in `STATUS.md`
(SEC MED-001 XP-farming-via-delete-recreate, and the Character-tab
per-activity breakdown row). This verification did not surface anything
that needs a product decision – all findings below are implementation
notes, not blockers.

## Findings summary

No BLOCKERs found on either side.

**SHOULD-FIX**: none.

**NOTE** (non-blocking, informational):
1. `_habits_mod` import at `app/api/v1/api.py:325-328` is guarded with
   `except ImportError` only (not a broader `except Exception`), matching
   the exact same pattern already used for every other optional router in
   that file (`_workspace_mod`, `_admin_recordings_mod`, etc.) – if a
   non-`ImportError` exception occurred during `habits.py`'s module-level
   execution, boot would still fail loudly rather than degrade. This is
   pre-existing repo convention, not something introduced by this batch,
   so not flagged as a blocker; noting for awareness only.
2. `HabitCheckResponse.habit.month_summary` is computed anchored on
   `check_date` (the day being toggled), not necessarily "today" – for a
   same-day toggle (the common `toggleToday` path) these coincide, so this
   only matters for backdated `toggleDay` corrections. Verified this is
   inert in practice: `HabitModel.monthSummary` is never read anywhere in
   the weekly-view widget tree (`habits_card.dart` grep confirmed) – only
   `habits_month_view.dart` reads `monthSummary`, and it always sources
   its habits from the dedicated `GET /habits?window=month` fetch
   (`_fetchMonth`), never from a check-toggle response. No user-visible
   effect.
3. The backend's 366-day backdating floor and "retro-complete an arbitrary
   past week" capability (CS-01 item 3) currently has no FE entry point:
   the Weekly view's Edit mode only ever exposes the 7 cells of the
   *currently displayed* (current) week for correction – there is no
   weekly-view paging to a prior week, and the Monthly view is read-only
   per CS-04. So "retro week pays XP" in practice means "a past day
   *within the current week* was corrected before the week ended", not an
   arbitrarily old week. This matches the actual device-QA scenario
   described in `STATUS.md`'s deploy checklist and is not a contract
   violation – the backend capability is simply broader than what today's
   UI exercises (forward-compatible, e.g. if a future round adds weekly
   paging).
4. Three cosmetic color-token near-misses are already self-flagged in the
   FE code's own comments (empty-state illustration dot, future-weekday
   label tone, month-view chevron color) – these are `ui-ux-designer`
   territory, not an API-contract concern, listed here only so they aren't
   lost.

## Test evidence

- Backend: `python -m pytest app/tests/test_habits.py app/tests/test_habits_ai_context.py -q`
  → **74 passed**, 0 failed (MindSync branch `msv3.12` @ affe9e2).
- Frontend: `flutter analyze` on all habit source files → **no issues**.
  `flutter test` on all four habit test files
  (`habits_cubit_test.dart`, `habits_card_test.dart`,
  `habits_month_view_test.dart`, `habit_editor_sheet_test.dart`) →
  **100 passed**, 0 failed (mindsync-frontend branch `msv3.12` @ 734168f).
- l10n: all 7 locale ARB files (`app_de/en/es/fr/nb/pl/sv.arb`) carry the
  same 25 `mainTab_habits*`/`habitEditor_*` keys – no locale is missing a
  string this feature introduced.

## Verdict

**GO.** No blockers on either side. The API contract is implemented and
consumed consistently; failure modes degrade safely and never masquerade as
"no habits" or trigger onboarding; deploy order is safe in either direction
during the interim window; nothing outside the expected file set was
touched.

> **Correction (2026-09-02, post-deploy):** the "Path/method" row above was wrong. `router.get("/")`
> mounted at prefix `/habits` resolves to `/api/v1/habits/` (with the slash), while the client
> constant was `/api/v1/habits` (without). The mismatch surfaced as a 307 redirect that Dio does not
> follow for POST, so adding a habit failed on device. Fixed on both sides (backend accepts both
> spellings since v547; `Endpoints.habits` now ends with `/`). Future contract checks must compare
> the exact resolved path including the trailing slash.
