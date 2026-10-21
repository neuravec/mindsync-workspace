# QA regression: first-conversation voice v2 + profile re-run fix

Date: 2026-10-05. Author: qa-testing. Scope: pre-deploy regression run. Nothing was pushed or deployed, and no product code was changed.

## Verdict: GO

No regression in either repo. Every failure on the release tree (backend) and on the frontend branch is in the known baseline and fails with the same test names on the base (`d1d93d0` / `origin/dev`). The two backend branches merge cleanly, no model or migration file changed, `app.main` boots offline, and the Postgres DDL is byte-identical to `d1d93d0`.

| check | result |
|---|---|
| Backend merge | clean, no conflict (the two branches touch disjoint files) |
| Backend pytest (merged tree) | 7340 run: 7331 passed, 9 failed = exactly the 9 known baseline failures |
| Targeted backend files | 294 passed, 0 failed |
| Offline boot `import app.main` | OK, 348 routes (same count as `d1d93d0`) |
| Model / migration diff vs `d1d93d0` | none (`app/models`, `alembic/`, `app/db` untouched) |
| Postgres DDL compile | 76 tables, hash identical to `d1d93d0` |
| Frontend `flutter test` | 3260 run: 3234 passed, 26 failed (incl. 2 in the known hanging file), all 26 identical on `origin/dev` |
| Frontend `flutter analyze` | 0 errors (9 warnings, 138 infos; same counts on `origin/dev`; none in a file this branch changed) |
| Generated files (l10n, freezed, json, gen) | in sync: regeneration produced no content change |

## 1. Backend

### Release worktree

```
cd MindSync
git worktree add ..\MindSync-wt-release -b release/first-conversation-voice-v2 feat/first-conversation-voice-v2
cd ..\MindSync-wt-release
git merge --no-ff fix/profile-rerun-null-overwrite
```

Result: merge commit `99a2933` on `release/first-conversation-voice-v2` (local only, not pushed). History: `d1d93d0` then `8e84428`, `f166a24`, `5ee8701`, `e5829fc`, `7c9d993` (voice v2) merged with `0f74b96`, `756cf10` (profile fix). No conflict. The voice branch changes `audio_v2.py`, `reflect.py`, `config.py`, `crud/reflect_entry.py`, `services/first_conversation.py`, `services/orca_memory.py`, `.env.example`; the profile branch changes `users.py`, `schemas/schemas.py` (Pydantic only) and adds `services/user_profile_writes.py`. No file is touched by both.

`git diff --stat d1d93d0 HEAD -- app/models alembic app/alembic app/db` is empty: no model, migration or session change, so no `alembic upgrade` is needed for this deploy.

### Targeted files (merged tree)

```
python -m pytest app/tests/test_first_conversation_rerun.py app/tests/test_first_conversation_rerun_limits.py \
  app/tests/test_first_conversation_v2.py app/tests/test_first_conversation_security_guards.py \
  app/tests/test_profile_rerun_null_overwrite.py app/tests/test_age_band.py -q
```

294 passed, 0 failed (29.7 s).

### Full suite (merged tree)

228 test files, sorted alphabetically and split into 6 chunks (`python -m pytest <files> -q -rf`), each chunk with its own SQLite file via `DB_URL` / `DATABASE_URL` so the chunks never share `test_temp.db`. All in the foreground.

| chunk | first file | passed | failed |
|---|---|---|---|
| 0 | `test_a14_orchestrator_cost_fixes.py` | 1425 | 0 |
| 1 | `test_debriefs.py` | 1265 | 1 |
| 2 | `test_memory_content_until_forget_race.py` | 873 | 4 |
| 3 | `test_notification_premium_gate.py` | 1618 | 1 |
| 4 | `test_recording_summary_prompt.py` | 959 | 1 |
| 5 | `test_therapy_frequency.py` | 1191 | 2 |
| **total** | | **7331** | **9** |

Failures, diffed by name against the expected baseline:

| test | status |
|---|---|
| `test_first_impression.py::TestFirstImpressionEndpoint::test_language_mapping` | baseline |
| `test_notification_improvements.py::TestBetweenSessionsPlaceholder::test_between_sessions_default_is_true` | baseline |
| `test_notification_improvements.py::TestBetweenSessionsPlaceholder::test_between_sessions_key_in_defaults` | baseline |
| `test_notification_improvements.py::TestBetweenSessionsPlaceholder::test_between_sessions_placeholder_comment_in_source` | baseline |
| `test_notification_improvements.py::TestNotificationTimezoneIndexMigration::test_migration_creates_index` | baseline |
| `test_onboarding_v2.py::TestResetTherapyOnboarding::test_preserves_therapy_data` | baseline |
| `test_symptom_suggestions.py::TestSymptomSuggestionResponseSchema::test_from_attributes_config` | baseline |
| `test_therapy_frequency.py::TestIsOnWeekYearBoundary::test_year_boundary_dec_to_jan_known_limitation` | baseline |
| `test_walkthrough.py::TestCompleteWalkthroughStepEndpoint::test_all_five_tabs_awards_points` | baseline |

New failures: 0. Missing baseline failures: 0. Flakes: 0.

Proof that the 9 are pre-existing: the same six files run on a clean detached worktree of `d1d93d0` give the same 9 failures by name. `test_onboarding_v2 ... test_preserves_therapy_data` is the one closest to the profile fix (reset onboarding); it fails with the identical assertion on both trees (`assert None == '[{"name": "Anxiety", "is_custom": false}]'` on `focus_areas`, a MagicMock setup issue in the test), so the profile fix did not cause or change it.

### Offline boot check

Clean process, recipe from `test_orca_memory_backfill_settings.py::test_app_main_imports_with_the_keys_set`: conftest env executed first, SQLite `DB_URL`, the `rq.*` modules mocked in `sys.modules`, `firebase_admin.credentials.Certificate` and `initialize_app` patched, then `import app.main`.

Result on the merged tree: `BOOT_OK FastAPI routes= 348`, firebase init and the PostHog error handlers registered, `create_all` ran. The changed modules (`user_profile_writes`, `first_conversation`, endpoints `users`, `reflect`, `audio_v2`, `core.config`) import cleanly. `d1d93d0` also has 348 routes, so no route was added or lost.

### Postgres DDL compile

Every table in `Base.metadata` compiled with `sqlalchemy.dialects.postgresql` (`CreateTable` plus each `CreateIndex`, indexes sorted by name): 76 tables, no error, SHA-256 prefix `713e908c207468b8` on both the merged tree and `d1d93d0`. The DDL is byte-identical, which matches the empty model diff.

## 2. Frontend

Branch `fix/first-conversation-voice-v2-fe` at `fc74a5e` (`1277c02`, `71947ef`, `fc74a5e` on top of `origin/dev` `113543f`). System Flutter 3.41.1.

To keep the main checkout untouched (it has unrelated uncommitted edits under `test/marketing_shots/` and agent memories), both trees were tested in clean detached worktrees, `fe-qa-br` at `fc74a5e` and `fe-qa-dev` at `origin/dev`, then removed. A clean checkout also proves the committed generated files are enough to compile and test.

### `flutter test`, per directory

```
flutter test test/<dir> --exclude-tags marketing --concurrency=4 --file-reporter json:<out>.json
```

`test/marketing_shots/` was not run. The known hanging file `test/screens/fab_flows/record_session_appbar_close_test.dart` was run on its own with `--timeout 60s` under a shell `timeout`.

| directory | passed | failed |
|---|---|---|
| `test/` root files | 18 | 0 |
| `api` | 140 | 0 |
| `bloc` | 149 | 0 |
| `core` | 86 | 0 |
| `navigation` | 70 | 0 |
| `providers` | 16 | 0 |
| `services` | 120 | 0 |
| `support` | 23 | 0 |
| `ui` | 78 | 18 |
| `utils` | 122 | 0 |
| `widgets` | 158 | 0 |
| `screens/account, auth, character_tab, errors, debrief_capture` | 154 | 0 |
| `screens/audio_chat` | 24 | 0 |
| `screens/fab_flows` (6 files) + `health_check` + `main_page` | 117 | 0 |
| `screens/fab_flows/record_session_appbar_close_test.dart` | 0 | 2 (1 fail, 1 hang) |
| `screens/first_conversation` | 139 | 0 |
| `screens/main_tab` | 268 | 0 |
| `screens/moments, my_therapy, orca_memory, reflect_entry, splash, stats_tab, welcome` | 270 | 0 |
| `screens/reflect_tab` | 154 | 0 |
| `screens/settings` + `sign_up` | 103 | 0 |
| `screens/subscription` | 178 | 0 |
| `screens/therapy_capture` + `therapy_onboarding` | 217 | 0 |
| `screens/therapy_tab` | 192 | 6 |
| `screens/usage` | 97 | 0 |
| `screens/workspace` | 193 | 0 |
| `screens/wow` | 148 | 0 |
| **total** | **3234** | **26** |

All directories with new or changed tests on this branch are green: `api` (`reflect_manager_limit_test`, `users_manager_flush_test`), `bloc` (`audio_chat_first_conversation_test`), `screens/first_conversation` (cubit, gates, gates view, privacy), `screens/subscription` (`subscription_cubit_suspend_test`), `screens/usage` (`usage_chip_and_gate_test`), `screens/wow` (`wow_screen_test`), `support` (`reflect_analytics_guard`).

### Failures diffed against `origin/dev`

The three failing groups were rerun on `origin/dev`. The sorted name lists are identical (`diff` empty for `ui`, `screens/therapy_tab` and the hanging file): 26 on the branch, the same 26 on dev. New failures: 0.

Some test names contain a long dash in the source; below they are cut at that character.

- `test/ui/reflect_tab/reflect_chat_bubble_test.dart` (3): agent variant has 16px border radius; agent variant has 4px deepOcean left border; user variant has aquaBreeze 70% background and no left border.
- `test/ui/reflect_tab/reflect_chat_input_test.dart` (5): bottom accent bar AnimatedContainer has height 0 at rest; bottom accent bar has height 3 after text entered; outer AnimatedContainer decoration has borderRadius 12; renders send SVG button; send button is disabled when isWaitingForAi=true.
- `test/ui/reflect_tab/reflect_starter_chips_test.dart` (1): minimum tap target height is 48px.
- `test/ui/reflect_tab/reflect_thinking_indicator_test.dart` (4): bubble has 16px border radius; bubble has white background and deepOcean left border; dots are 12px wide and 12px tall; renders exactly 3 dot containers.
- `test/ui/settings/widgets/save_feedback_indicator_test.dart` (5): icon is fully opaque during the hold phase; icon is invisible again after full 1500 ms animation; initially has opacity 0 (invisible); multiple trigger() calls restart animation from 0; trigger() starts animation.
- `test/screens/therapy_tab/therapy_card_detail_screen_error_test.dart` (6): a 404 still shows the distinct "source removed" message; a DioException WITH a 500 response never leaks the raw backend body; a bare DioException with NO response (network error) also shows the friendly message; any other exception type (e.g. a JSON decode error) also shows the friendly message; the Retry button has a >=48x48 tap target (CS-06); the retry button re-fetches and clears the error on success.
- `test/screens/fab_flows/record_session_appbar_close_test.dart` (2): AppBar-X on a Yieks-class error (mic permission) calls discardRecording(); AppBar-X on a non-Yieks error (network upload failure) does NOT call discardRecording() (this one never completes, on dev too).

### `flutter analyze`

Branch: 147 issues, `error` 0, `warning` 9, `info` 138. `origin/dev`: the same 0 / 9 / 138. None of the 147 is in a file changed by the branch (checked against `git diff --name-only 113543f fc74a5e`). The 9 warnings are old: `unused_field` in `lib/widgets/moments/moment_bottom_sheet.dart:92`, the rest unused imports or locals in older tests.

### Generated files

- l10n: `flutter gen-l10n` in the clean branch worktree changed no file. The 7 `.arb` files and the 8 generated `app_localizations*.dart` files are committed together on the branch.
- Codegen: `dart run build_runner build --delete-conflicting-outputs` (53 s, 326 outputs). Git listed 238 generated files as modified, but `git diff --quiet -- lib` is clean and a byte compare of all 238 against `HEAD` with CR stripped found 0 content differences. The listing is only line-ending noise from `core.autocrlf=true` (checkout writes CRLF, the generator writes LF). `first_conversation_cubit.freezed.dart`, changed on this branch, matches its source.

Nothing to commit. The scratch regeneration was discarded with the worktree.

## 3. Notes and residual risk

| item | owner |
|---|---|
| Deploy order: no migration in this release, so backend is a plain push of `release/first-conversation-voice-v2` (merge `99a2933`) to `main`. No Procfile or queue change. The profile fix makes `POST /users/profile` return 200 with the stored row when one exists; FE `1277c02` was written against that contract, and old app builds benefit too (their PUT fallback with nulls is no longer reached). | integration-devops |
| Local test runtime is Python 3.14.3; Heroku runs 3.12.2 (`runtime.txt`). Nothing in the diff uses 3.13+ syntax, but this run does not prove 3.12 behaviour. | integration-devops (awareness) |
| 26 pre-existing frontend failures (18 `ui`, 6 `therapy_tab` error screen, 2 in the hanging AppBar-X file) and 9 backend baseline failures remain on `dev` / `main`. | flutter-mobile / backend-api, data-analytics |
| Another frontend worktree appeared during this run: `mindsync-frontend-wt-paywall` on `fix/first-conversation-paywall-return` (`185d62a`). Tested afterwards, see section 4. | lead |
| Not covered by automated tests: live `gpt-realtime` behaviour of the v2 prompt, gender-aware Polish grammar on a real call, a real onboarding re-run on device (profile kept, scripted conversation again), mic permission dialogs. Device QA before the stores. | flutter-mobile + operator |

## 4. Frontend follow-up: `fix/first-conversation-paywall-return` (`185d62a`)

Verdict: **GO**. No regression.

Scope: one commit on top of `fc74a5e`. F1: the paywall opened from the first conversation returns to it after a purchase (opt-in `after_purchase` flag on the subscription route in `ms_routes.dart`, `subscription_screen.dart`), and `FirstConversationCubit.close` ends an open thread that has user turns, once. F2: the purchase-update pause in `SubscriptionCubit` is sticky. 12 files: 6 in `lib/`, 6 in `test/`. No `.arb`, no generated file, no model change.

Method: identical to section 2. Clean detached worktree at `185d62a` (removed afterwards), system Flutter 3.41.1, `flutter test <dir> --exclude-tags marketing --concurrency=4`, one directory group per call, all in the foreground, the hanging AppBar-X file on its own with `--timeout 60s`. All directories were run, not only the priority list.

| directory | passed | failed | vs `fc74a5e` |
|---|---|---|---|
| `screens/first_conversation` | 143 | 0 | +4 new tests |
| `screens/wow` | 150 | 0 | +2 new tests |
| `screens/subscription` | 181 | 0 | +3 new tests |
| `screens/usage` | 97 | 0 | same |
| `navigation` (router tests) | 70 | 0 | same |
| `core` | 86 | 0 | same |
| `api` | 140 | 0 | same |
| `bloc`, `providers`, `services`, `support`, `utils`, `widgets`, root files | 149, 16, 120, 23, 122, 158, 18 | 0 | same |
| `ui` | 78 | 18 | same 18 |
| `screens/therapy_tab` | 192 | 6 | same 6 |
| `screens/fab_flows/record_session_appbar_close_test.dart` | 0 | 2 (1 fail, 1 hang) | same 2 |
| every other `screens/*` group (as in section 2) | 1500 | 0 | same |
| **total** | **3243** | **26** | +9 passing tests |

Failures diffed by name: the sorted list of 26 is identical to the `origin/dev` baseline from section 2 (`diff` empty). New failures: 0.

`flutter analyze`: 147 issues, `error` 0, `warning` 9, `info` 138, the same as `origin/dev` and `fc74a5e`. None is in a file changed between `113543f` and `185d62a`.

Generated files: `flutter gen-l10n` changed nothing. `build_runner build --delete-conflicting-outputs` (326 outputs) left `git diff --quiet -- lib` clean; the 238 files git lists as modified have 0 content differences against `HEAD` with CR stripped (the same `autocrlf` noise as in section 2). Nothing to commit.

Not covered by automated tests: a real StoreKit / Play purchase started from the first conversation, then the return to the conversation, on device.
