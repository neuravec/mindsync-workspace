# QA regression: Reflect prompt v3 (backend) + test-order hygiene fix

Date: 2026-10-06. Author: qa-testing. Scope: pre-deploy regression run of `feat/reflect-prompt-v3`, plus one test-only fix. Nothing was pushed or deployed. No product code was changed by QA.

## Verdict: GO

Final deploy candidate: merge `51ea97b` (this branch plus the security fixes `3d0892a`), also GO. See section 9.

No regression. The full suite fails on exactly the 9 known baseline names, and every targeted file is green. The app boots offline with the same routes and a byte-identical Postgres DDL as `76d5c09`. There is no model, migration, `app/core`, Procfile, requirements or runtime change. `.env` loses one key (`REFLECT_SYSTEM_MESSAGE`), which still has a `""` default in Settings and is no longer read by any runtime code. The frontend needs no change. The pre-existing test-ordering bug is fixed in `b70b4d4`, proven before and after.

| check | result |
|---|---|
| Hygiene fix `b70b4d4` (`app/tests/test_voice_fixes.py` only) | bad order on base: 50 failed (pair), 188 failed (split); with the fixed file: 0 and 1 baseline |
| Backend targeted (14 files) | 799 passed, 0 failed |
| Backend full pytest | 7506 run: 7497 passed, 9 failed = exactly the 9 baseline names |
| Test IDs vs `76d5c09` | 7421 -> 7506: 94 added, 9 removed (all 9 replaced, listed in section 4) |
| Offline boot `import app.main` | OK on branch and base: 348 routes, same route-set hash |
| Postgres DDL compile | 81 tables, `b3a768c417fce480` on branch and base (same value as the recap report) |
| Fresh-process import of changed modules + worker paths | 12/12 OK, no circular import |
| Model / alembic / app/core / Procfile / requirements / runtime / Dockerfile diff | none |
| `.env` keys vs `76d5c09` | removed: `REFLECT_SYSTEM_MESSAGE`; added: none; changed values: none |
| Frontend (`origin/dev` `f4afaa6`) | no change needed; `director: null` already handled |
| U+2014 / U+2013 in the branch's added lines (`app/`, `scripts/`) | 0 / 0 |

## 1. Test-order hygiene fix (`b70b4d4`)

### Mechanism

`test_voice_fixes.py` runs several tests under `patch("httpx.Client")`. `starlette.testclient` executes `class TestClient(httpx.Client)` on its first import. On `76d5c09`, `TestReflectVoiceRAGInjection` did `from fastapi.testclient import TestClient` inside a patched test body (old line 244). When that was the first import of `fastapi.testclient` in the session, TestClient was built on the MagicMock and stayed that way, so every endpoint test collected afterwards got mock responses (`StopIteration` from the mock's `side_effect`). It only shows when no earlier-collected module imports `fastapi.testclient` at module level, which is why the standard 8-chunk run never caught it.

On this branch, the v3 rewrite of `TestReflectVoiceRAGInjection` had already dropped that in-test import, so the branch itself was not affected. The hazard was still latent as long as the file patches `httpx.Client`. It is the only test file that does.

### Fix

`app/tests/test_voice_fixes.py` (+39 lines, CRLF kept, ASCII only):

1. `from fastapi.testclient import TestClient` at module level, with a comment explaining why. Pytest collects every module before running any test, so the real class is bound before any patch can be active.
2. `TestHttpxClientPatchDoesNotLeak` at the end of the file (runs after every patched test in it): asserts `httpx.Client` is a real type again, and that `httpx.Client` is in `TestClient.__mro__`. A future leak fails here by name instead of as 188 unrelated failures.

The `rq` / `app.core.rq_queue` `sys.modules` stubs were left as they are. `rq` cannot import on Windows (`get_context('fork')`), the stubs must exist at module import time, many files use the same pattern, and the green split below shows they cause no order problem.

### Proof (bad order, before and after)

Pair = `test_voice_fixes.py` then `test_workspace_endpoints.py`. Split = the 23 sorted files from `test_users_activated_at_migration.py` to the end (the split that showed 188 failures). Base = `git archive 76d5c09` export in scratch.

| tree | pair | split (23 files) |
|---|---|---|
| base `76d5c09` as is | 50 failed, 40 passed | 188 failed, 474 passed |
| base + guard only (no module-level import) | 51 failed: the 50 plus `test_testclient_is_built_on_the_real_httpx_client` | not run |
| base + fixed `test_voice_fixes.py` | 92 passed | 1 failed (baseline `test_walkthrough`), 663 passed |
| branch `cbe1dce` (before fix) | 90 passed | 1 failed (baseline), 661 passed |
| branch `b70b4d4` (after fix) | 92 passed | 1 failed (baseline), 663 passed |

The guard-only row shows the guard detects the leak. The base-plus-fix rows show the import neutralizes it even while the old in-test import is still there.

```
DB_URL=sqlite:///<scratch>.db DATABASE_URL=... python -m pytest app/tests/test_voice_fixes.py app/tests/test_workspace_endpoints.py -q -p no:cacheprovider -W ignore
DB_URL=... python -m pytest $(ls app/tests/test_*.py | sort | awk '$0 >= "app/tests/test_users_activated_at_migration.py"') -q -p no:cacheprovider -W ignore -rf
```

Commit: `b70b4d4 test(hygiene): pin TestClient to the real httpx.Client in test_voice_fixes`, staged by explicit path (`git add app/tests/test_voice_fixes.py`). Working tree clean afterwards.

## 2. Scope

Tree: `C:\Users\mikol\Notebooks\MindSync\Heroku\MindSync-wt-reflect-v3`, branch `feat/reflect-prompt-v3`: `23098df`, `6de2424`, `7179ae2`, `fa4628e`, merge `cbe1dce` of `origin/main` `76d5c09`, then `b70b4d4` (this fix). Local Python 3.14.3.

`git diff --stat 76d5c09..HEAD` before the fix: 13 files. Product code: `.env`, `app/api/v1/endpoints/reflect.py`, `app/services/first_conversation.py`, `app/services/reflect_prompt.py` (new), `app/services/voice_director.py`. Script: `scripts/reflect_eval.py` (new, not imported by the app). The rest are tests.

```
git diff --stat 76d5c09..HEAD -- app/models alembic app/alembic app/db app/core Procfile requirements.txt runtime.txt .env.example Dockerfile alembic.ini
```

Empty. No `alembic upgrade` is needed. Not a CO-DEPLOY case (no Procfile change).

`.env`, parsed with `dotenv_values` on `git show <rev>:.env`: 53 keys on base, 52 on HEAD. Removed: `REFLECT_SYSTEM_MESSAGE`. Added: none. Changed values: none. `app/core/config.py` still declares `REFLECT_SYSTEM_MESSAGE: str = ""`, so a missing key cannot fail Settings at boot. Runtime readers of it on the branch: none (only comments, two tests that prove a stale value is ignored, and `scripts/reflect_eval.py`, which reads the old prompt from `git show REV:.env` for comparison).

Removed top-level names (AST diff vs base): `reflect.py` no longer imports `get_user_data_richness`, `NEW_USER_GUARDRAIL`, `DEVELOPING_USER_GUARDRAIL`; `first_conversation.py` drops private `_HEADING_RE`, `_SAFETY_HEADING` and adds `SAFETY_SECTION`. Grep over `app/` and `scripts/`: no consumer of any removed name.

## 3. Full suite

231 test files, sorted, in the same 8 chunks as the recap report (same first-file boundaries). Each chunk ran in the foreground with its own SQLite file via `DB_URL` / `DATABASE_URL`, as 4 concurrent tool calls (12 cores):

```
python -m pytest <chunk files> -q -p no:cacheprovider -W ignore -rf --junitxml=<scratch>/br_c<k>.xml
```

| chunk | first file | passed | failed | time | vs `-vf` run on `76d5c09` |
|---|---|---|---|---|---|
| 0 | `test_a14_orchestrator_cost_fixes.py` | 1197 | 0 | 173 s | same |
| 1 | `test_crud_app_insight.py` | 845 | 1 | 67 s | same |
| 2 | `test_fix1_mood_trend_symptoms.py` | 874 | 0 | 38 s | same |
| 3 | `test_moments_endpoints.py` | 657 | 4 | 30 s | same |
| 4 | `test_notification_premium_gate.py` | 1137 | 1 | 102 s | same |
| 5 | `test_prep_card_overhaul.py` | 1112 | 0 | 132 s | +83 (`test_reflect_prompt_v3` 81, `test_reflect_prompt_content` net +2) |
| 6 | `test_scalability_fixes.py` | 853 | 2 | 135 s | same |
| 7 | `test_triage_proposals.py` | 822 | 1 | 147 s | +2 (`test_voice_fixes` net +2, incl. the 2 guard tests) |
| **total** | | **7497** | **9** | | **+85** |

JUnit totals: 7506 tests, 9 failures, 0 errors, 0 skipped.

Failures, diffed mechanically by name (JUnit vs the 9-name baseline table in the recap report):

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

## 4. Test IDs, base vs branch

`python -m pytest app/tests --collect-only -q` on the base export and on the branch, sorted and compared with `comm`: base 7421 (equals the `-vf` JUnit total), branch 7506 (equals this run). 94 added, 9 removed. Each removed test pinned v2 behaviour that v3 deliberately replaces, and each has a v3 counterpart:

| removed (v2) | replaced by (v3) |
|---|---|
| `test_first_conversation.py::TestPromptHygiene::test_safety_falls_back_when_the_setting_is_empty`, `test_safety_section_is_the_live_reflect_one` | `test_safety_does_not_depend_on_any_setting`, `test_safety_section_is_the_single_shared_copy` |
| `test_orca_memory_feeding.py::TestVoiceFeeding::test_ordinary_voice_session_gets_memory_patterns_and_schedule_before_the_guardrail` | `test_ordinary_voice_session_gets_memory_patterns_and_schedule_in_one_area` |
| `test_reflect_prompt_content.py::TestReflectSystemMessageTemplateFromEnv` (4 tests: placeholders, no dashes, no literal escapes, actually loaded) | `TestReflectPromptTemplateInCode` (5: every placeholder, no other placeholder, no dashes, real line breaks, `.env` no longer carries the old prompt) + `TestReflectSystemPromptBuiltOutput::test_a_stale_reflect_system_message_setting_is_ignored` |
| `test_voice_fixes.py::TestReflectVoiceRAGInjection::test_new_user_guardrail_appended`, `test_established_user_no_guardrail` | `test_every_user_gets_the_never_invent_rule_and_no_listen_and_ask`, `test_a_known_user_gets_no_thin_context_line` |

The other added tests are `test_reflect_prompt_v3.py` (81, new file) and the 2 guard tests from `b70b4d4`.

## 5. Targeted files

```
python -m pytest app/tests/test_reflect_prompt_v3.py app/tests/test_reflect_prompt_content.py app/tests/test_reflect_entry_flow.py \
  app/tests/test_reflect_entry_pre_migration.py app/tests/test_reflect_entry_events.py app/tests/test_voice_fixes.py \
  app/tests/test_orca_memory_feeding.py app/tests/test_voice_director.py app/tests/test_first_conversation*.py -q -rf
```

| file | tests | failed |
|---|---|---|
| `test_reflect_prompt_v3.py` | 81 | 0 |
| `test_reflect_prompt_content.py` | 8 | 0 |
| `test_reflect_entry_flow.py` | 81 | 0 |
| `test_reflect_entry_pre_migration.py` | 18 | 0 |
| `test_reflect_entry_events.py` | 44 | 0 |
| `test_voice_fixes.py` | 42 | 0 |
| `test_orca_memory_feeding.py` | 86 | 0 |
| `test_voice_director.py` | 76 | 0 |
| `test_first_conversation.py` | 55 | 0 |
| `test_first_conversation_part1_rules.py` | 88 | 0 |
| `test_first_conversation_rerun.py` | 24 | 0 |
| `test_first_conversation_rerun_limits.py` | 32 | 0 |
| `test_first_conversation_security_guards.py` | 82 | 0 |
| `test_first_conversation_v2.py` | 82 | 0 |
| **total (14 files)** | **799** | **0** |

42 s. `test_reflect_entry_pre_migration.py` drops the three entry-flow columns from the test database and drives the real HTTP routes (the deploy-before-migrate window); it stays green with the v3 prompt path.

## 6. Offline boot, Postgres DDL, isolated imports

Probe (same recipe as `test_orca_memory_backfill_settings.py::test_app_main_imports_with_the_keys_set`), clean process, cwd = tree root so the tree's own `.env` is read: conftest env executed first, SQLite `DB_URL`, `rq.*` mocked in `sys.modules`, `firebase_admin.credentials.Certificate` and `initialize_app` patched, `import app.main`, then explicit imports of the changed modules. Every table in `Base.metadata` compiled with `sqlalchemy.dialects.postgresql` (`CreateTable` plus each `CreateIndex`, sorted by name) and hashed.

| tree | boot | routes | route-set sha256 | tables | DDL sha256 | `REFLECT_SYSTEM_MESSAGE` length seen by Settings |
|---|---|---|---|---|---|---|
| branch | OK | 348 | `b69b3ec92f009a8e` | 81 | `b3a768c417fce480` | 0 |
| base `76d5c09` | OK | 348 | `b69b3ec92f009a8e` | 81 | `b3a768c417fce480` | 7202 |

The route hash formula differs from the recap report's probe, so only branch vs base is comparable; they are equal. The DDL hash equals the recap report's value. The last column confirms boot works with the key absent from `.env`.

`reflect_prompt` imports `first_conversation` at module scope, so a worker that imports modules in a different order could in principle hit a circular import. Each module below was imported alone in a fresh process: all 12 `IMPORT_OK`.

`app.services.first_conversation`, `app.services.voice_director`, `app.services.reflect_prompt`, `app.api.v1.endpoints.reflect`, `app.api.v1.endpoints._therapy_helpers`, `app.api.v1.endpoints.audio_v2`, `app.services.conversation_analysis`, `app.services.orca_memory_backfill`, `app.services.plan_usage_service`, `app.tasks.reflect_idle_analysis`, `app.tasks.premium_intent`, `app.core.rq_scheduler_setup`.

## 7. Frontend contract (no Flutter change needed)

Checked at `mindsync-frontend` `origin/dev` = `f4afaa6`.

- **System prompt.** `reflect_chat_cubit.dart` `getSessionData()` reads `oldData['system_message'] as String? ?? ''` and forwards it unchanged as `instructions` to `POST /audio-v2/realtime-session` (`audio_v2_manager.dart`, JSON body). The client never parses the prompt. Size: the v3 template is 9537 chars (old `.env` line about 7.3 KB); the rendered samples in this folder are 15-16 KB. It travels in a POST body, and `RealtimeSessionRequest.instructions` has no max length, so the router's 8 KB request-line limit does not apply.
- **Director.** Backend: `audio/user_message_add` already returned `director: null` whenever the pipeline returned nothing (`AudioMessageWithDirector.director: Optional[DirectorInjection] = None`). v3 adds one more null case: a note that is only question sentences, which `clean_director_note` empties. Text mode appends the note server-side only, so it never reaches the client. Client: the only consumer is `audio_chat_cubit.dart` `_handleDirectorResponse` (line 1401), which reads `response['director'] as Map<String, dynamic>?`, returns on `null`, returns unless `should_inject == true`, returns on an empty `injection_text`, all inside a `try`. The response is a raw map (`reflect_manager.dart` `sendUserAudioMessage`); no Freezed model parses `director`. Repo-wide grep of `lib/` for `director` finds no other consumer.

## 8. Notes and residual risk

| item | owner |
|---|---|
| Deploy: plain push of the backend, no migration, no Procfile or requirements change. Backend-only; the current app build works unchanged. Rollback is a plain redeploy (the old slug carries its own `.env` with the old prompt). | integration-devops |
| The prompt change reaches every Reflect user as soon as the web dyno restarts (prompt is server-side; the app only forwards the string). Live model behaviour is not covered by pytest; it is covered by the eval in `eval.md` and `raw/` in this folder. | operator (awareness) |
| Analytics: `reflect_session_started` gains `prompt_version` (`reflect-v3`), `reasoning_effort` and `model` (enums, `unknown` on failure; `reflect_prompt.start_event_properties`). The privacy whitelist in `test_reflect_entry_events.py` was extended to exactly those enum values, and it passes. After release, confirm the properties actually flow. | posthog-data-extractor |
| If a Heroku config var `REFLECT_SYSTEM_MESSAGE` exists, it is now ignored (no runtime reader; two tests prove a stale value changes nothing). Not verified on Heroku: the Heroku MCP server did not connect in this session, and it is not needed for the verdict. | integration-devops (optional cleanup) |
| No Flutter unit test covers `director: null` in `_handleDirectorResponse`. The path is an early return inside a `try`, and null was already a live backend value before v3. Low priority. | qa-testing / flutter-mobile (optional) |
| Local Python is 3.14.3; Heroku runs 3.12.2. Nothing in the diff needs 3.13+, but this run does not prove 3.12 behaviour. | integration-devops (awareness) |
| Pre-existing failures remain: the 9 backend baseline names. | backend-api, data-analytics |

## 9. Final combination: security fixes merged (`51ea97b`)

Verdict: **GO**. No regression. Same method as sections 1 to 6, all runs in the foreground.

Merge: in `MindSync-wt-reflect-v3`, `git merge --no-ff feat/reflect-prompt-v3-sec` on top of `b70b4d4`. No conflict (`3d0892a` touches `reflect_prompt.py`, `reflect.py`, `test_reflect_prompt_v3.py`, `test_workspace_cs07_repeat_periods.py`; `b70b4d4` only `test_voice_fixes.py`). Merge commit `51ea97b`, history `51ea97b` <- `3d0892a` (cut from `cbe1dce`) + `b70b4d4`. Working tree clean afterwards. Not pushed.

What `3d0892a` changes, per its message and its tests:

- **RP3-M1.** `POST /start` stores only the instructions and a placeholder in message 0. Every turn and voice connection builds WHAT YOU KNOW ABOUT THEM fresh. So a Forget or a PROFILING withdrawal takes effect on the next message, and a fallback or rollback never resends stored personal context.
- **RP3-M2.** Therapy status is read only through the Art. 9 gated `first_conversation.user_is_in_therapy`. Schedule, setup therapy context and symptom trends stay ungated, as decided by the operator.
- **RP3-L3.** Stored voice agent transcripts keep a dash between two digits as a hyphen, so helpline numbers and ranges stay readable.

| check | result |
|---|---|
| Full pytest (same 8 chunks, 231 files) | 7525 run: 7516 passed, 9 failed = exactly the 9 baseline names (0 new, 0 missing) |
| Bad-order pair (`test_voice_fixes` then `test_workspace_endpoints`) | 92 passed |
| Bad-order split (23 files from `test_users_activated_at_migration.py`) | 1 failed (baseline `test_walkthrough`), 663 passed |
| Targeted: the 14 files of section 5 + `test_workspace_cs07_repeat_periods.py` | 856 passed, 0 failed (`test_reflect_prompt_v3.py` 100, `test_workspace_cs07_repeat_periods.py` 38, the other 13 files unchanged from section 5) |
| Offline boot | OK, 348 routes, route-set hash `b69b3ec92f009a8e` (unchanged) |
| Postgres DDL | 81 tables, `b3a768c417fce480` (unchanged, equal to `76d5c09`) |
| Fresh-process imports (`reflect_prompt`, `first_conversation`, `endpoints.reflect`, `rq_scheduler_setup`) | 4/4 OK |
| Sensitive paths vs `76d5c09` (`app/models`, alembic, `app/db`, `app/core`, Procfile, requirements, runtime, `.env.example`, Dockerfile) | empty |
| `.env` keys vs `76d5c09` | 53 -> 52; removed `REFLECT_SYSTEM_MESSAGE`; added none; changed values none |
| U+2014 / U+2013 in added lines (`app/`, `scripts/`) | 0 / 0 |

Per chunk (passed / failed): 0: 1197 / 0, 1: 845 / 1, 2: 874 / 0, 3: 657 / 4, 4: 1137 / 1, 5: 1131 / 0, 6: 853 / 2, 7: 822 / 1. Only chunk 5 moved (+19 vs section 3), all in `test_reflect_prompt_v3.py`. The `-sec` commit message reports 7514 passed; the difference of 2 is the guard tests from `b70b4d4`.

Test IDs vs `b70b4d4` (JUnit vs the section 4 collection): 22 added, 3 removed, all in `test_reflect_prompt_v3.py`.

| removed | replaced by |
|---|---|
| `TestLoadContext::test_without_health_consent_the_data_is_still_used[False]`, `[True]` | `TestLoadContext::test_without_health_consent_only_therapy_status_is_left_out[False]`, `[True]` + `test_the_consent_is_read_once_and_only_for_therapy_status` (RP3-M2) |
| `TestMessageEndpoint::test_a_failed_build_falls_back_to_the_stored_prompt` | `TestMessageEndpoint::test_a_failed_build_falls_back_to_the_stored_instructions_and_fresh_excerpts` (RP3-M1) |

Other additions:

- `TestNothingPersonalIsStored` (9 tests): message 0 holds no note, bio or setup text in text, voice, old-client and seeded starts; `/start` reads no personal context; Forget then the next message; the fallback; a rollback-style reuse.
- `TestAgentTranscriptNumbers` (9 tests, of which 7 are parametrized dash cases).

`test_workspace_cs07_repeat_periods.py`: the to-do wiring test now checks the per-turn prompt and asserts the stored prompt does NOT carry the to-dos. That matches RP3-M1.

Frontend: `3d0892a` changes no route, response model, `director` or `system_message` handling in `reflect.py` (grep of its diff). So section 7 still holds: no Flutter change needed. The voice `system_message` still arrives as one opaque string; it is now built fresh per connection instead of read from the stored copy.

Notes added to section 8:

| item | owner |
|---|---|
| RP3-M2 is a behaviour change from the earlier "no Art. 9 gate" state of this branch: without ARTICLE9_HEALTH consent, ordinary Reflect no longer tells the model whether the person is in therapy. Everything else stays ungated, as the operator decided. Pinned by the 3 `TestLoadContext` tests above. | operator (awareness), legal review already pending |
| Rollback after RP3-M1: pre-v3 code reuses message 0, which now holds only instructions and a placeholder, and appends its own fresh PROFILING-gated blocks (`test_a_rollback_style_reuse_of_message_zero_carries_nothing_personal`). So a rollback still needs no data step. | integration-devops (awareness) |
