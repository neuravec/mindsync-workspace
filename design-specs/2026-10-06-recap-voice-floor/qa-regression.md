# QA regression: recap voice floor (backend) + voice turn capture (frontend)

Date: 2026-10-06. Author: qa-testing. Scope: pre-deploy regression run. Nothing was pushed or deployed, and no product code was changed.

## Verdict: GO

There is no regression in either repo. Every failure is in the known baseline and matches it by name: 9 backend failures (same names as `qa-regression-voice-v2.md`) and 26 frontend failures (same sorted list as the `origin/dev` baseline file from that run). The backend boots offline with the same 348 routes as `99a2933` and a byte-identical Postgres DDL. No model, migration, Procfile, requirements or config file changed. The frontend generated files match a from-scratch regeneration.

| check | result |
|---|---|
| Backend targeted files (5) | 262 passed, 0 failed |
| Backend full pytest | 7416 run: 7407 passed, 9 failed = exactly the 9 baseline names |
| Offline boot `import app.main` | OK on branch and on `99a2933`: 348 routes, same route-set hash |
| Postgres DDL compile | identical hash on branch and `99a2933` |
| Model / migration / Procfile / requirements / config diff vs `99a2933` | none |
| Frontend `flutter test` (all dirs, `--exclude-tags marketing`) | 3300 run: 3274 passed, 26 failed = exactly the 26 baseline names |
| Test files executed | 291 of 291 (all except `test/marketing_shots/`) |
| Frontend `flutter analyze` | 0 errors, 9 warnings, 138 infos; issue list identical to base `156dbc8`; none in a changed file |
| Generated files | worktree clean; 242 part directives resolve; fresh regeneration identical (0 content differences) |

## 1. Backend

Tree: `C:\Users\mikol\Notebooks\MindSync\Heroku\MindSync-wt-recap`, branch `fix/recap-voice-floor`, commits `bd47da6` (recap: voice conversations are no longer "short") and `a1f3560` (realtime `client_session_config` carries the minted `noise_reduction`), on top of `99a2933` (= `origin/main`, merge-base confirmed). Local Python 3.14.3.

### Diff scope

`git diff --stat 99a2933..HEAD` lists 7 files: `app/api/v1/endpoints/audio_v2.py`, `app/services/openai_audio_service.py`, `app/services/orca_memory.py`, plus the tests `test_audio_v2_noise_reduction.py` (new), `test_orca_memory_recap_voice_floor.py` (new), `test_first_conversation_security_guards.py`, `test_orca_memory_recap.py`.

```
git diff --stat 99a2933..HEAD -- app/models alembic app/alembic app/db Procfile requirements.txt runtime.txt .env .env.example app/core
```

Empty. No new `settings.*` key or `os.environ` read in the added lines. No `alembic upgrade` is needed for this deploy.

Contract change: `VoiceSessionConfig` (realtime session response) gains an optional `noise_reduction: Optional[Dict[str, str]] = None`. Additive; older clients ignore it. The FE branch reads it as a nullable field (`realtime_session_model.dart`, `@JsonKey(includeIfNull: false)`), so a new app on an old backend simply leaves the key out of `session.update`.

### Targeted files

```
python -m pytest app/tests/test_orca_memory_recap_voice_floor.py app/tests/test_orca_memory_recap.py \
  app/tests/test_first_conversation_security_guards.py app/tests/test_audio_v2_noise_reduction.py \
  app/tests/test_audio_v2_config.py -q -rf
```

262 passed, 0 failed (23 s).

### Full suite

230 test files, sorted and split into 8 chunks, each run in the foreground as `python -m pytest <files> -q -rf --junitxml=...` with its own SQLite file via `DB_URL` / `DATABASE_URL` (removed afterwards).

| chunk | first file | passed | failed | time |
|---|---|---|---|---|
| 0 | `test_a14_orchestrator_cost_fixes.py` | 1197 | 0 | 177 s |
| 1 | `test_crud_app_insight.py` | 845 | 1 | 70 s |
| 2 | `test_fix1_mood_trend_symptoms.py` | 874 | 0 | 56 s |
| 3 | `test_moments_endpoints.py` | 657 | 4 | 42 s |
| 4 | `test_notification_premium_gate.py` | 1132 | 1 | 365 s |
| 5 | `test_prep_card_overhaul.py` | 1029 | 0 | 136 s |
| 6 | `test_scalability_fixes.py` | 853 | 2 | 168 s |
| 7 | `test_triage_proposals.py` | 820 | 1 | 175 s |
| **total** | | **7407** | **9** | |

JUnit totals: 7416 tests, 9 failures, 0 errors, 0 skipped. That is 76 more passing tests than the 7331 on `99a2933` in the previous report, all from this branch's test changes.

Failures, diffed mechanically by name (JUnit vs the baseline table in `qa-regression-voice-v2.md`):

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

New failures: 0. Baseline failures no longer failing: 0.

### Offline boot and Postgres DDL

Same recipe as `test_orca_memory_backfill_settings.py::test_app_main_imports_with_the_keys_set`, in a clean process: conftest env executed first, SQLite `DB_URL`, the `rq.*` modules mocked in `sys.modules`, `firebase_admin.credentials.Certificate` and `initialize_app` patched, then `import app.main`, then explicit imports of the three changed modules (`app.services.orca_memory`, `app.services.openai_audio_service`, `app.api.v1.endpoints.audio_v2`). Then every table in `app.db.session.Base.metadata` compiled with `sqlalchemy.dialects.postgresql` (`CreateTable` plus each `CreateIndex`, tables and indexes sorted by name) and hashed. The same script was run on the branch and on a `git archive 99a2933` export.

| tree | boot | routes | route-set sha256 | tables | DDL sha256 |
|---|---|---|---|---|---|
| branch `a1f3560` | OK | 348 | `e236c809904cc61b` | 81 | `b3a768c417fce480` |
| base `99a2933` | OK | 348 | `e236c809904cc61b` | 81 | `b3a768c417fce480` |

The table count comes from this run's probe, which counts differently from the earlier report's (76). The comparison that matters is branch vs base with the same script, and they are identical, as the empty model diff predicts.

## 2. Frontend

Tree: `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend-wt-capture`, branch `fix/voice-turn-capture`, commit `71991bb` on top of `156dbc8` (= `origin/dev`, 2.0.104, merge-base confirmed). System Flutter 3.41.1 (`C:\Users\mikol\flutter`), Dart 3.11.0.

Diff scope (11 files): `realtime_session_model.dart` with its `.freezed.dart` and `.g.dart`, `analytics_events.dart`, `audio_chat_cubit.dart`, `voice_session_options.dart`, `first_conversation_cubit.dart`, and the tests `test/bloc/audio_chat_turn_capture_test.dart` (new), `test/screens/first_conversation/first_conversation_turn_capture_test.dart` (new), `first_conversation_cubit_test.dart`, `first_conversation_test_helpers.dart`.

### `flutter test`, per directory

```
flutter test <dir...> --exclude-tags marketing --concurrency=4 --file-reporter json:<out>.json
```

One invocation per directory group, all in the foreground. `test/marketing_shots/` was not run. The known hanging file was run alone with `--timeout 60s` under a shell `timeout 240`.

| directory group | passed | failed |
|---|---|---|
| root files (`widget_test`, `l10n_completeness_test`) | 18 | 0 |
| `api` | 140 | 0 |
| `bloc` | 168 | 0 |
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
| `screens/fab_flows/record_session_appbar_close_test.dart` | 0 | 2 (1 fail, 1 timeout) |
| `screens/first_conversation` | 155 | 0 |
| `screens/main_tab` | 268 | 0 |
| `screens/moments, my_therapy, orca_memory, reflect_entry, splash, stats_tab, welcome` | 270 | 0 |
| `screens/reflect_tab` | 154 | 0 |
| `screens/settings` + `sign_up` | 103 | 0 |
| `screens/subscription` | 181 | 0 |
| `screens/therapy_capture` + `therapy_onboarding` | 217 | 0 |
| `screens/therapy_tab` | 192 | 6 |
| `screens/usage` | 97 | 0 |
| `screens/workspace` | 193 | 0 |
| `screens/wow` | 150 | 0 |
| **total** | **3274** | **26** |

Compared with the last full run (`185d62a`, 3243 passed): +31 passing tests, all from this branch (`bloc` +19, `screens/first_conversation` +12). Both directories with new or changed tests are green. A file-level check against the JSON suites shows all 291 test files outside `test/marketing_shots/` were executed.

### Failures diffed by name

The sorted list of 26 `path :: name` entries was diffed against `dev_all.failed`, the `origin/dev` baseline list from the 2026-10-05 run: identical (`diff` empty). New failures: 0. Some names contain a long dash in the source; below they are cut at that character.

- `test/ui/reflect_tab/reflect_chat_bubble_test.dart` (3): agent variant has 16px border radius; agent variant has 4px deepOcean left border; user variant has aquaBreeze 70% background and no left border.
- `test/ui/reflect_tab/reflect_chat_input_test.dart` (5): bottom accent bar AnimatedContainer has height 0 at rest; bottom accent bar has height 3 after text entered; outer AnimatedContainer decoration has borderRadius 12; renders send SVG button; send button is disabled when isWaitingForAi=true.
- `test/ui/reflect_tab/reflect_starter_chips_test.dart` (1): minimum tap target height is 48px.
- `test/ui/reflect_tab/reflect_thinking_indicator_test.dart` (4): bubble has 16px border radius; bubble has white background and deepOcean left border; dots are 12px wide and 12px tall; renders exactly 3 dot containers.
- `test/ui/settings/widgets/save_feedback_indicator_test.dart` (5): icon is fully opaque during the hold phase; icon is invisible again after full 1500 ms animation; initially has opacity 0 (invisible); multiple trigger() calls restart animation from 0; trigger() starts animation.
- `test/screens/therapy_tab/therapy_card_detail_screen_error_test.dart` (6): a 404 still shows the distinct "source removed" message; a DioException WITH a 500 response never leaks the raw backend body; a bare DioException with NO response (network error) also shows the friendly message; any other exception type (e.g. a JSON decode error) also shows the friendly message; the Retry button has a >=48x48 tap target (CS-06); the retry button re-fetches and clears the error on success.
- `test/screens/fab_flows/record_session_appbar_close_test.dart` (2): AppBar-X on a Yieks-class error (mic permission) calls discardRecording(); AppBar-X on a non-Yieks error (network upload failure) does NOT call discardRecording() (never completes; same on dev).

### `flutter analyze`

Branch `71991bb`: 147 issues, 0 errors, 9 warnings, 138 infos. Base `156dbc8` (clean `git archive` export, `flutter pub get --offline`, `flutter analyze`): the same 147. The set difference of the two issue lists is empty both ways, and none of the 147 is in one of the 11 changed files.

### Generated files

The brief warned that about 200 generated files had been restored by hand after a filtered `build_runner` run deleted them. Checks:

1. `git status --porcelain` in the worktree before any run: 0 lines. `git status --ignored` shows only the standard ignored paths (`.dart_tool`, `build`, platform `ephemeral` dirs), no `*.g.dart` or `*.freezed.dart`. The commit `71991bb` itself deletes no generated file (only the two `realtime_session_model` outputs change).
2. Part directives: all 242 `part '...'` directives in non-generated `lib/` and `test/` files resolve to an existing, git-tracked file (0 missing, 0 untracked). All 238 tracked generated files (148 `.freezed.dart`, 88 `.g.dart`, 2 `.gen.dart`) are referenced; 0 orphans.
3. Fresh regeneration: a `git archive 71991bb` export in scratch, with every `*.g.dart`, `*.freezed.dart`, `*.gen.dart` and `lib/l10n/generated/*.dart` deleted first (238 + 8 files), then `flutter pub get --offline` (regenerated the 8 l10n files) and `dart run build_runner build --delete-conflicting-outputs` (72 s, 326 outputs, regenerated all 238). Compared with the worktree, ignoring CR: 246 files on each side, the same set, 0 content differences. This includes `realtime_session_model.freezed.dart` and `.g.dart`, the generated files changed on this branch.

Side effect of this run, reverted: the implicit `pub get` of the first `flutter test` rewrote 7 desktop plugin registrants (`linux/flutter/generated_plugin*`, `macos/Flutter/GeneratedPluginRegistrant.swift`, `windows/flutter/generated_plugin*`) with LF line endings. Their content is identical to `HEAD` ignoring CR (the blobs store CRLF). They were restored with `git checkout --`. Final `git status --porcelain`: 0 lines in both worktrees.

## 3. Notes and residual risk

| item | owner |
|---|---|
| Deploy: no migration, no Procfile, requirements or config change. Backend is a plain push of `fix/recap-voice-floor`. The response gains the additive optional `noise_reduction`; the FE handles its absence, so backend-first or FE-first both work. | integration-devops |
| Analytics meaning change: on `first_conversation_ended` a voice transcript now counts in `user_turns` only with at least 3 words; shorter fragments go to the new `user_fragments` (old count = `user_turns + user_fragments`). `voice_chat_ended` gains `transcription_failed_count` and `end_drain_timed_out`. The new properties are asserted in the new tests. Any insight trending `user_turns` will show a step down from this build on; whoever reads that funnel should be told. | growth-analyst / posthog-data-extractor (awareness) |
| Local Python is 3.14.3; Heroku runs 3.12.2. Nothing in the diff needs 3.13+, but this run does not prove 3.12 behaviour. | integration-devops (awareness) |
| Pre-existing failures remain: 9 backend, 26 frontend (18 `ui`, 6 `therapy_tab` error screen, 2 in the hanging AppBar-X file). | backend-api, data-analytics / flutter-mobile |
| Not covered by automated tests: real `gpt-realtime` behaviour with `near_field` noise reduction, End's final drain timing on a real device and network, recap quality from the live model on short voice conversations. Device QA before the stores. | flutter-mobile + operator |
| Process note: one Flutter call holding five directory groups ran past the 10-minute tool limit and was moved to the background by the harness. It finished normally (exit 0) and its results are included above; after that, every call ran at most two groups. | qa-testing |

## 4. Follow-up: security-fix branches (`-vf`)

Verdict: **GO**. No regression. Same method as sections 1 and 2, all runs in the foreground.

### Backend: `fix/recap-voice-floor-vf` (`76d5c09` on `a1f3560`)

Tree: `C:\Users\mikol\Notebooks\MindSync\Heroku\MindSync-wt-recap-vf`. Scope (VF-M1, `generate_recap` writes memory only when there are recap items): `app/services/orca_memory.py` and `app/tests/test_orca_memory_recap_voice_floor.py`. The sensitive-path diff vs `99a2933` (`app/models`, `alembic`, `app/db`, `app/core`, Procfile, requirements, runtime, `.env*`) is empty.

| chunk | passed | failed |
|---|---|---|
| 0 | 1197 | 0 |
| 1 | 845 | 1 |
| 2 | 874 | 0 |
| 3 | 657 | 4 |
| 4 | 1137 | 1 |
| 5 | 1029 | 0 |
| 6 | 853 | 2 |
| 7 | 820 | 1 |
| **total** | **7412** | **9** |

These are the same 8 chunks (same 230 files) as section 1. JUnit totals: 7421 tests, 9 failures, 0 errors. The by-name diff against the baseline table gives 0 new failures and 0 missing. Chunk 4 has +5 passing tests over section 1, from the inverted and added recap tests.

Offline boot (same probe): `BOOT_OK`, 348 routes, route-set hash `e236c809904cc61b`, 81 tables, DDL hash `b3a768c417fce480`. That is identical to `a1f3560` and `99a2933`.

### Pre-existing test-ordering issue (not a regression, reported separately)

The implementing agent saw 188 failures when the last chunk started at `test_users_activated_at_migration.py`. My standard chunk 7 (starting at `test_triage_proposals.py`, same files after it) passes, so it did not show up in the run above. Reproduced on purpose:

| tree | split `test_users_activated_at_migration.py` .. end (23 files) |
|---|---|
| `-vf` `76d5c09` | 188 failed, 474 passed |
| base `99a2933` (`git archive` export) | 188 failed, 474 passed |

The two failure lists are identical by name. 187 are in workspace files (`test_workspace_fix1_a1` 70, `test_workspace_endpoints` 50, `test_workspace_msv32_fix2` 32, `test_workspace_cs07_repeat_periods` 14, `test_workspace_msv32_fix4` 10, `test_workspace_msv311_cs01` 7, `test_workspace_realization_posthog` 4), plus the baseline `test_walkthrough` failure. 186 of them raise `StopIteration`. This predates the branch.

Bisect: `test_voice_fixes.py` followed by `test_workspace_endpoints.py` alone reproduces it (50 failed). Each other preceding file paired with `test_workspace_endpoints.py` passes. Likely mechanism: a test in `test_voice_fixes.py` runs under `@patch("httpx.Client")` and does `from fastapi.testclient import TestClient` inside the test body (line 244). When that is the first import of `fastapi.testclient` in the session, Starlette's `TestClient` class is built on the mocked `httpx.Client` and stays that way. Later endpoint tests then get `MagicMock` responses (`assert <MagicMock name='Client.put().status_code'> == 200`). The same file also leaves a mocked `app.core.rq_queue` in `sys.modules` when it is the first importer. Fix direction: import `fastapi.testclient` at module top of `test_voice_fixes.py`, and scope the `sys.modules` stubs to a fixture. Owner: qa-testing (test files only), not done in this pass.

### Frontend: `fix/voice-turn-capture-vf` (`f4afaa6` on `71991bb`)

Tree: `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend-wt-capture-vf`. Scope (VF-L1, microphone toggles ignored after End): `audio_chat_cubit.dart` and `test/bloc/audio_chat_turn_capture_test.dart`. No generated file, `.arb` or `pubspec` change, so the codegen check of section 2 still holds.

| directory | passed | failed | vs `71991bb` |
|---|---|---|---|
| `test/bloc` | 174 | 0 | +6 new tests |
| `test/screens/audio_chat` | 24 | 0 | same |
| `test/screens/reflect_tab` | 154 | 0 | same |
| `test/screens/first_conversation` | 155 | 0 | same |
| `test/screens/wow` | 150 | 0 | same |
| `test/screens/reflect_entry` | 80 | 0 | (inside group A in section 2) |
| **total** | **737** | **0** | |

`flutter analyze`: 147 issues, 0 errors, 9 warnings, 138 infos. The issue list is identical to base `156dbc8` (set difference empty both ways), with none in the 11 files changed since `156dbc8`.

`git status`: clean before the run. `flutter test`'s implicit `pub get` again rewrote the 7 desktop plugin registrants with LF endings (content identical to `HEAD` ignoring CR). They were restored with `git checkout --`. Final `git status --porcelain` is 0 lines in both `-vf` worktrees.
