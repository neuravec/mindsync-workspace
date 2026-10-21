# QA1 Report - MSV3.12 Habit Tracker - pre-deployment quality gate

Date: 2026-09-02
Scope: qa-testing pre-deployment gate for the Habit Tracker batch (backend commits
c8795de, dc62712, 82fedcc, 40e34c9 on `msv3.12`; frontend commits 0078fd4, 08e8d26,
734168f on `msv3.12`). Neither repo branch was switched or pushed.

## GO / NO-GO: **GO**

Zero regressions found against the documented baselines on both repos. Three backend
coverage gaps and three frontend coverage gaps were found and closed with new tests
(one frontend "gap" turned out to already be covered - see below); all new tests pass;
`flutter analyze` is clean on every habits-related file.

---

## Backend (pytest) - `C:\Users\mikol\Notebooks\MindSync\Heroku\MindSync`

### Command run (exact, per-file counts)

```
python -m pytest app/tests/test_habits.py app/tests/test_habits_ai_context.py app/tests/test_alembic_chain.py app/tests/test_reflect_summary.py app/tests/test_delete_account_cascade.py app/tests/test_character_tab.py -q
```

| File | Before (baseline run) | After (with new tests) |
|---|---|---|
| `test_habits.py` | 50 passed | 53 passed (+3 new) |
| `test_habits_ai_context.py` | 24 passed | 24 passed |
| `test_alembic_chain.py` | 9 passed | 9 passed |
| `test_reflect_summary.py` | 50 passed | 50 passed |
| `test_delete_account_cascade.py` | 13 passed | 13 passed |
| `test_character_tab.py` | 151 passed | 151 passed |
| **Total** | **297 passed, 0 failed** | **300 passed, 0 failed** |

Ran twice more after adding the new tests (once per file, once combined) - stable at
300 passed both times, no flakes.

### Regression list vs. the documented pre-existing baseline

**Empty.** No failures at all in the targeted run (baseline or after additions). The
documented 21 pre-existing backend failures live entirely in files outside this
targeted set (test_custom_therapy_sessions, test_first_impression,
test_notification_improvements, test_onboarding_v2, test_symptom_suggestions,
test_therapy_frequency, test_therapy_tracking_fix1_a12, test_voice_fixes,
test_walkthrough) and were correctly excluded from this run per the task brief - not
re-verified here, per instruction.

### Backend coverage-gap check - findings and action taken

| # | Scenario from the brief | Status found | Action |
|---|---|---|---|
| (a) | Timezone edge: two users in far-apart zones (`Pacific/Auckland` vs `America/Los_Angeles`) each checking their own "today", with the correct assertion being "each user's own today is accepted" (not "UTC instant future-for-one-but-not-other") | **Missing.** `TestTimezoneWeekStartFixtures` only exercised one shared pinned instant across both zones for *window building*, never two users hitting the check-toggle date guard at a shared instant where their local dates differ by a full day. | **Added** `test_per_user_date_guard_independent_of_shared_utc_instant` in `TestTimezoneWeekStartFixtures` (`app/tests/test_habits.py`). |
| (b) | Week completion when the 7th check is a BACKDATED one for a past week (retro XP once) | **Already covered.** `test_retro_completion_via_backdated_puts_in_permuted_order` in `TestHabitChecksAndXp` does exactly this: backdates a fully-past week, applies the 7 checks in a permuted (non-sequential) order, asserts XP awarded exactly once, on whichever call happens to be the 7th. | No new test needed. |
| (c) | Reorder with a foreign habit id → 422 and no partial write | **Partially missing.** `test_reorder_rejects_wrong_set` asserted the 422 but never verified no write occurred (the endpoint validates the full set BEFORE calling `habit_crud.reorder_habits`, so this is a legitimate no-op today, but it was unverified). | **Added** `test_reorder_rejects_wrong_set_leaves_existing_order_unchanged` in `TestHabitCrudEndpoints` - creates two habits, sends an invalid reorder set, then asserts the GET listing order is byte-for-byte unchanged. |
| (d) | DELETE then re-create keeps `active_count` correct for a free user | **Partially missing.** `test_free_tier_cap_and_refill_after_delete` created, hit the cap, deleted, and refilled (asserting only the 201), but never checked the post-refill `active_count`/`can_add`, nor that the cap re-engages on a second add attempt. | **Added** `test_refill_after_delete_active_count_and_cap_enforced_again` in `TestHabitCrudEndpoints` - asserts `active_count == 1`, `can_add == False` after refill, and a further create attempt still 403s. |

### A test-harness gotcha discovered while writing (a)

`_HabitTestBase.client_as(user_id)` overrides `deps.get_current_user` /
`deps.get_db` on the **shared** `self.test_app` FastAPI instance. Holding two
`TestClient`s built at different times (`client_as("u1")` then `client_as("u2")`) and
interleaving calls between them silently makes **both** clients act as whichever user
was overridden last - there is no per-client isolation. All existing tests in the file
avoid this by construction (always create-then-immediately-use one client before
moving to the next), so it was never exposed before. The new timezone test needed two
"live" users at once and hit this directly (a 403 `premium_required` on a brand-new
user, from the second POST silently landing on the first user's account). Fixed by
re-calling `self.client_as(...)` immediately before every request instead of holding
two client variables - no harness change was made (out of scope: `client_as` is a
shared helper other passing tests also rely on), just noting it here since a future
agent writing a multi-user interleaved test on `test_habits.py` will hit the same trap.

---

## Frontend (`flutter test`) - `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend\mindsync_app`

Each directory run separately, in the foreground, per instruction (memory limits).

### Command results (exact counts)

| Command | Before | After |
|---|---|---|
| `flutter test test/screens/main_tab/cubit/` | 145 passed, 0 failed | 146 passed, 0 failed (+1 new) |
| `flutter test test/screens/main_tab/widgets/` | 89 passed, 1 failed | 89 passed, 1 failed (unchanged - see below) |
| `flutter test test/api/` | 129 passed, 0 failed | 129 passed, 0 failed (untouched) |
| `flutter test test/core/` | 86 passed, 0 failed | 86 passed, 0 failed (untouched) |

### Regression list vs. the documented pre-existing baseline

**Empty - one known, documented failure only, no regressions.**

`test/screens/main_tab/widgets/session_setup_screen_test.dart` fails to *compile*:

```
test/screens/main_tab/widgets/session_setup_screen_test.dart:111:66: Error: A non-null
value must be returned since the return type 'Future<void>' doesn't allow null.
 - 'Future' is from 'dart:async'.
 when(() => settingsCubit.addCustomSession(any())).thenAnswer((_) {});
```

This is exactly the documented pre-existing Mocktail compile error (a `thenAnswer`
callback returning `void` where `Future<void>` is expected - a Mocktail/Dart typing
issue in the test file itself, unrelated to the Habit Tracker batch). Confirmed present
identically before and after the new tests were added; not a regression. This file is
owned by qa-testing but was intentionally left as-is per the task brief ("1 known
pre-existing failure ... not a regression") - fixing it is out of scope for this gate
and would be a separate, deliberate task since it's a compile-level fix to an unrelated
test file, not a Habit Tracker concern.

### `flutter analyze`

Ran on the full project: **138 issues found**, all pre-existing `info`/`warning`
lint items (deprecated Flutter APIs, `prefer_const_constructors`, unused imports/locals
in unrelated test files, the one `body_might_complete_normally` compile error in
`session_setup_screen_test.dart` noted above) - none of them `error`-severity except
that one already-known compile error, and none touch habits code.

**Zero issues** (grepped explicitly, confirmed empty) in:
- `lib/screens/main_tab/**habits**` (`habits_card.dart`, `habits_month_view.dart`,
 `habit_editor_sheet.dart`, `habits_cubit.dart`, `habits_state.dart` +
 `.freezed.dart`)
- `lib/api/models/habits/`
- `lib/api/api_managers/habits_manager.dart`
- `lib/core/service_locator.dart`

Also ran `flutter analyze` scoped to just the two test files this gate modified
(`test/screens/main_tab/cubit/habits_cubit_test.dart`,
`test/screens/main_tab/widgets/habits_card_test.dart`) - **no issues found**.

### Frontend coverage-gap check - findings and action taken

| # | Scenario from the brief | Status found | Action |
|---|---|---|---|
| (a) | Cubit: `toggleToday` when the server returns 400 `future_date` (clock skew) rolls back and surfaces an error, not the empty state | **Missing.** An existing test already covered a *generic* `Exception('network')` rollback, but nothing exercised the specific real failure shape: `HabitsManager.setCheck` has no 400→exception translation (unlike `createHabit`'s 403 → `HabitPremiumRequiredException`), so a 400 `future_date` surfaces to the cubit as a bare `ApiException(statusCode: 400, ...)`, caught by the cubit's generic `catch (_)`. | **Added** a `blocTest` in the `HabitsCubit.toggleToday` group (`test/screens/main_tab/cubit/habits_cubit_test.dart`) that throws exactly that `ApiException` shape and asserts: optimistic flip → rollback to unchecked → `toastKey == 'error_somethingWentWrong'` → `habits` list still present/non-empty (never collapses to an empty list). |
| (b) | Widget: error state renders a retry affordance and never the "Small daily wins add up" empty state | **Behavior differs from the brief's assumption, and the meaningful part was a real gap.** `HabitsCard`'s top-level `HabitsError` branch renders `const SizedBox.shrink()` - a deliberate "minor module, degrade silently" design (same convention as the deleted Homework module and `mood_trend`/`weekly_observations` cards), **not** a retry affordance. `HabitsMonthView`'s own `monthError` state *does* have a Retry button and was already fully tested (`habits_month_view_test.dart`: renders retry, tapping it calls `retryMonth`). The one real, unguarded gap was: nothing asserted that `HabitsCard`'s error state does NOT render the empty-state copy. | **Strengthened** the existing `'error state renders nothing -- no crash, no visible error UI'` test in `test/screens/main_tab/widgets/habits_card_test.dart` with two more assertions: `find.text('Small daily wins add up')` and `find.text('Add your first habit')` both `findsNothing` during an error state. Did not write a test asserting a retry button exists on `HabitsCard`'s top-level error, since that would assert behavior the code does not (and, per the design comment in `habits_card.dart`, is not intended to) have. |
| (c) | Month view: `goToNextMonth` from the current month is a no-op | **Already covered.** `'goToNextMonth is a no-op once the shown month is the current month -- never pages into the future'` in the `HabitsCubit.goToPreviousMonth / goToNextMonth / retryMonth (FE-C)` group (`habits_cubit_test.dart`) asserts exactly this: no further emission, and `verifyNever` on the next-month fetch call. | No new test needed. |

---

## Tests added (files + names)

### Backend - `C:\Users\mikol\Notebooks\MindSync\Heroku\MindSync\app\tests\test_habits.py`

- `TestTimezoneWeekStartFixtures.test_per_user_date_guard_independent_of_shared_utc_instant`
- `TestHabitCrudEndpoints.test_reorder_rejects_wrong_set_leaves_existing_order_unchanged`
- `TestHabitCrudEndpoints.test_refill_after_delete_active_count_and_cap_enforced_again`

All 3 pass; full targeted 6-file run after adding them: 300 passed, 0 failed.

### Frontend - `mindsync_app\test\screens\main_tab\cubit\habits_cubit_test.dart`

- New `blocTest` in the `HabitsCubit.toggleToday` group: `'a 400 future_date response
 (device clock skew vs. the server) rolls back the optimistic check and surfaces the
 error toast -- never left dangling in the optimistic-but-unconfirmed state'`

Passes; file total: 53 passed (was 52).

### Frontend - `mindsync_app\test\screens\main_tab\widgets\habits_card_test.dart`

- Strengthened (not new) `'error state renders nothing -- no crash, no visible error
 UI'` with two additional `findsNothing` assertions for the empty-state copy.

Passes; file total unchanged at 22 (same test count, stronger assertions).

---

## Git status (not pushed)

Changes staged and committed on `msv3.12` in each repo, test files only, explicit
paths (no `git add .`, no `.claude/agent-memory/**`, no `android/build/`):

- Backend: `MindSync/app/tests/test_habits.py`
- Frontend: `mindsync-frontend/mindsync_app/test/screens/main_tab/cubit/habits_cubit_test.dart`,
 `mindsync-frontend/mindsync_app/test/screens/main_tab/widgets/habits_card_test.dart`

---

## GO / NO-GO rationale

**GO.** Zero regressions in either repo against the documented baselines (backend: the
21 pre-existing failures are all outside this batch's files and were correctly not
re-verified; frontend: the single pre-existing `session_setup_screen_test.dart`
compile error is unchanged and unrelated to habits). All identified coverage gaps are
now closed or were found to already be covered. `flutter analyze` is clean on every
file this batch touches.
