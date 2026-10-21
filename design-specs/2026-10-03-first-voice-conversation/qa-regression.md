# QA regression: first voice conversation + Orca memory

- **Date:** 2026-10-05
- **Agent:** qa-testing (pre-deployment)
- **Branches:** backend `MindSync/` `feat/first-voice-conversation` (9 commits vs `main`, plus QA test commit `cc8288b`), frontend `mindsync-frontend/` `feat/first-voice-conversation` (5 commits vs `dev`, HEAD `bf49f58`)
- **Spec:** `SPEC.md` in this folder

## Verdict: GO

No regression in either repo. Every failure seen on the branch is in the known baseline and reproduces identically on `main` / `dev`. The Postgres-only checks (migration DDL, boot, naive vs aware datetimes) found nothing. One coverage gap on account deletion was closed with a new test. Device QA is still required before the stores (see the last section).

| layer | result |
|---|---|
| Backend pytest | 6606 run: 6596 passed, 10 failed = the 9 known baseline failures + 1 load flake (passes alone). New QA test: +1, passes. |
| Backend Postgres reality | m315 upgrade/downgrade DDL clean on the postgresql dialect, one alembic head, `app.main` boots offline, lifespan idempotent, 0 naive vs aware hazards |
| Frontend `flutter analyze` | 0 errors (10 warnings, 143 infos, none in a file this branch touched) |
| Frontend `flutter test` | 3097 passed, 24 failed, 2 hang; all 26 identical on `dev` (known baseline about 26) |
| Critical flows | every flow in the checklist has passing tests (map below) |
| PostHog | every event fires from one place and has a test asserting its properties; privacy guard is structural and covers every new event |

## 1. Backend test suite

Run in three sequential foreground chunks (the full suite is over the 10 minute tool limit, and conftest uses an on-disk SQLite file, so chunks cannot run in parallel).

| chunk | files | passed | failed |
|---|---|---|---|
| 1 | 74 | 2401 | 1 |
| 2 | 70 | 2185 | 5 |
| 3 | 70 | 2010 | 4 |
| **total** | **214** | **6596** | **10** |

Failures:

| test | class |
|---|---|
| `test_first_impression.py::TestFirstImpressionEndpoint::test_language_mapping` | baseline |
| `test_notification_improvements.py` x4 (`TestBetweenSessionsPlaceholder` x3, `TestNotificationTimezoneIndexMigration::test_migration_creates_index`) | baseline |
| `test_onboarding_v2.py::TestResetTherapyOnboarding::test_preserves_therapy_data` | baseline |
| `test_symptom_suggestions.py::TestSymptomSuggestionResponseSchema::test_from_attributes_config` | baseline |
| `test_therapy_frequency.py::TestIsOnWeekYearBoundary::test_year_boundary_dec_to_jan_known_limitation` | baseline |
| `test_walkthrough.py::TestCompleteWalkthroughStepEndpoint::test_all_five_tabs_awards_points` | baseline |
| `test_worker_logging_config.py::TestWorkerOnlyImportPath::test_worker_import_path_configures_info_logging_without_app_main` | **flake, not a regression**: its child process (cold import of `app.tasks.prep_card_auto_generate`) hit the test's 60 s `subprocess.run` timeout under the load of the chunk run. Rerun alone: 7/7 passed in 3.6 s. The branch adds one import there (`app.services.orca_context`), which imports fine on a cold worker path. |

Baseline matches the lead's list exactly (9).

## 2. Backend Postgres reality (offline)

**Migration m315a1b2c3d4.** `alembic heads` shows one head (`m315a1b2c3d4`, down_revision `m314b2c3d4e5`, the verified prod head). The migration inspects the live database, so `alembic --sql` cannot render it. Its `upgrade()` / `downgrade()` were driven through an as_sql `MigrationContext` on the postgresql dialect with the existence probes set to four states:

| state | emitted DDL |
|---|---|
| prod at m314 (nothing new exists) | `SET LOCAL lock_timeout = '5s'`, CREATE TABLE `user_memory_items` (timestamptz, varchar FKs ON DELETE CASCADE), 2 indexes, CREATE TABLE `user_memory_suppressions`, unique index, 4 `ADD COLUMN` (all nullable, no default) |
| create_all already built both tables on a web boot before the migration | only the lock timeout + the 4 `ADD COLUMN` |
| already at head | nothing (empty output) |
| downgrade | drops in reverse order, guarded |

No native enum, no table rewrite, no backfill. FK types match prod (`users.id` varchar, `conversations.id` integer, per `db-reports/2026-10-03-first-conversation-predeploy-check.md`).

**ORM create_all.** All 76 tables compile with the postgresql dialect. The ORM DDL for the two new tables matches the migration (same columns, types, FKs and index names), so a boot that runs `create_all` before `alembic upgrade head` leaves nothing for the migration to fight. No native enum on either new table.

**Boot.** `import app.main` offline (throwaway SQLite, Firebase and rq stubbed): OK, 347 routes, new routes present (`/api/v1/reflect/{conversation_id}/recap`, `/api/v1/users/memory`, `/api/v1/users/memory/{item_id}`). Lifespan run twice with a fake scheduler: 24 jobs after both boots, exactly one `mindsync_reflect_idle_analysis` (stable id, description-based dedupe). Worker cold import of `app.tasks.reflect_idle_analysis`: OK.

**Deploy gap (code live, migration not run).** Already covered by tests that really drop the four new columns and exercise ORM reads, helpers, forget endpoints, account deletion and PROFILING withdrawal (`test_memory_security_guards.py`, class around line 832; `test_user_memory.py` around line 1102). All pass.

**Queue.** The recap enqueues the Personal Bio refresh on `high`. `main:Procfile` already runs `rq worker ... high default`, and `app/core/rq_queue.py` falls back when no worker listens on `high`. No Procfile change on this branch.

### Naive vs aware datetimes (CS-07 family)

Prod columns `messages.created_at`, `conversations.created_at` and `conversation_summaries.created_at` are `timestamp without time zone`; `conversations.last_message_at` and every new m315 column are `timestamptz`. SQL-side comparisons of a naive column with an aware parameter are safe on Postgres (implicit cast with the server TimeZone, which is UTC). The danger is a Python-side compare, subtract, sort or `max` of a loaded naive value against an aware one.

Every added backend line touching datetimes was reviewed. **Result: 0 High.** Each Python-side site normalizes first:

| file:line | what | normalized by |
|---|---|---|
| `app/services/first_conversation.py:122-164` | thread exemption window vs `utc_now()` | `_aware()` on `created_at`; claim via `as_aware_utc` |
| `app/services/first_conversation.py:206-233` | billable monthly count (`conversations.created_at` via Core select) | `_window_end` -> `_aware`; message filter is SQL-side |
| `app/services/first_conversation.py:852-919` | pause clock (turn times vs `now`) | `_turns()` applies `_aware` to every `messages.created_at` |
| `app/services/conversation_analysis.py:294-380` | analysis is current (summary vs last user turn) | `_aware()` on both sides |
| `app/services/orca_memory.py:1016-1033, 1335-1342, 2094` | transcript turns vs `memory_forgotten_at`, newest turn | `created_at=_aware(...)`; `get_memory_forgotten_at` returns `as_aware_utc` |
| `app/services/orca_memory.py:1939-1955` | `_memory_written_since` | SQL-side compare (naive UTC param vs timestamptz column; correct while the server TimeZone is UTC) |
| `app/api/v1/endpoints/reflect.py:536-562, 613-635` | opening message timestamp forced past the system prompt | `first_conversation._aware(not_before)` |
| `app/tasks/reflect_idle_analysis.py:149-201, 299-300` | idle cutoffs, last user turn, last_message_at | SQL-side filters; `_aware()` before every Python compare |
| `app/crud/reflect_entry.py:503-520`, `app/crud/user_memory.py:807-826` | guarded readers of the new timestamptz columns | `as_aware_utc` |

Runtime proof (state reproduced, not just read): the functions above were called with Postgres-shaped values (naive `created_at`, aware claim and forgotten timestamps). 7 of 7 checks ran without a `TypeError`.

## 3. Frontend

**`flutter analyze`:** 0 errors. 10 warnings and 143 infos, all in files this branch did not touch (unused imports or locals in older tests, `unused_field` in `moment_bottom_sheet.dart`, `use_build_context_synchronously` infos).

**`flutter test`, per directory** (never the whole suite; `test/marketing_shots/` not run):

| directory | passed | failed |
|---|---|---|
| `test/` (root files) | 18 | 0 |
| `api` | 138 | 0 |
| `bloc` | 140 | 0 |
| `core` | 86 | 0 |
| `navigation` | 70 | 0 |
| `providers` | 16 | 0 |
| `support` | 18 | 0 |
| `services` | 120 | 0 |
| `ui` | 78 | 18 |
| `utils` | 122 | 0 |
| `widgets` | 158 | 0 |
| `screens/account` | 7 | 0 |
| `screens/audio_chat` | 24 | 0 |
| `screens/auth` | 31 | 0 |
| `screens/character_tab` | 51 | 0 |
| `screens/debrief_capture` | 61 | 0 |
| `screens/errors` | 4 | 0 |
| `screens/fab_flows` (6 files) | 43 | 0 |
| `screens/fab_flows/record_session_appbar_close_test.dart` | 0 | 2 (hang) |
| `screens/first_conversation` | 88 | 0 |
| `screens/health_check` | 30 | 0 |
| `screens/main_page` | 44 | 0 |
| `screens/main_tab/cubit` | 174 | 0 |
| `screens/main_tab/widgets` | 94 | 0 |
| `screens/moments` | 22 | 0 |
| `screens/my_therapy` | 13 | 0 |
| `screens/orca_memory` | 37 | 0 |
| `screens/reflect_entry` | 80 | 0 |
| `screens/reflect_tab` | 154 | 0 |
| `screens/settings` | 53 | 0 |
| `screens/sign_up` | 50 | 0 |
| `screens/splash` | 17 | 0 |
| `screens/stats_tab` | 40 | 0 |
| `screens/subscription` | 175 | 0 |
| `screens/therapy_capture` | 57 | 0 |
| `screens/therapy_onboarding` | 160 | 0 |
| `screens/therapy_tab` (root files) | 74 | 6 |
| `screens/therapy_tab/cubit` | 5 | 0 |
| `screens/therapy_tab/widgets` | 113 | 0 |
| `screens/usage` | 95 | 0 |
| `screens/welcome` | 8 | 0 |
| `screens/workspace` (root, agenda, goals, realizations) | 50 | 0 |
| `screens/workspace` (threads, todo, topics, widgets) | 143 | 0 |
| `screens/wow` | 136 | 0 |
| **total** | **3097** | **26** |

All 26 non-passing tests were rerun in a temporary detached `dev` worktree (removed afterwards) and fail the same way there:

| file | count | cause on both branches |
|---|---|---|
| `test/ui/reflect_tab/reflect_chat_bubble_test.dart`, `reflect_chat_input_test.dart`, `reflect_starter_chips_test.dart`, `reflect_thinking_indicator_test.dart`, `test/ui/settings/widgets/save_feedback_indicator_test.dart` | 18 | stale widget-shape assertions; failure set on `dev` is identical, line for line |
| `test/screens/therapy_tab/therapy_card_detail_screen_error_test.dart` | 6 | the harness has no Router; `BackButtonListener` (deep-link back fix) asserts |
| `test/screens/fab_flows/record_session_appbar_close_test.dart` | 2 | never completes (hits the 560 s guard on both branches) |

## 4. Critical flows: where the tests are

| flow | covered by (all passing) |
|---|---|
| Sign-up -> onboarding 5-step / 7-step | `therapy_onboarding_cubit_branching_test.dart` ("in therapy with consent: 7 steps", "status ...: 5 steps"); the hand-off to `/wow` (`justCompletedOnboarding`, `currentlyInTherapy`, `nextSession`) is unchanged on this branch |
| Reveal -> intro -> first conversation | `wow_screen_test.dart` (Reveal single CTA, intro, back, Type instead), `first_conversation_intro_cubit_test.dart`, `first_conversation_views_test.dart` |
| Conversation: phases, reconnect, mode switch, renewal before 60 min, 5 s drain, End | `first_conversation_cubit_test.dart` (connection, mode switches, End, session renewal groups), `audio_chat_first_conversation_test.dart` (session.update tools / truncation / reasoning, function_call_output without response.create, usage counts) |
| End -> recap -> offer step 1 -> step 2 -> reminders -> Home | `wow_screen_test.dart` groups "Offer step 1", "Offer step 2", "Reminders, then Home (no First step)"; `wow_cubit_test.dart` "Offer steps 1 and 2"; `offer_step_view_test.dart` (ready / writing / short / failed recap) |
| Crisis branch: no offer, no offer events, no push prompt | `wow_cubit_test.dart` "Crisis-flagged recap" group (no event at all, crisis wins over re-run, push not asked), `wow_screen_test.dart` "/end flags crisis", `first_conversation_cubit_test.dart` "crisis gate: three sources" incl. fail-closed when /end and /recap both fail |
| Prices failed + retry | `wow_cubit_test.dart` "Prices failed" group, `wow_screen_test.dart` "Prices failed", `subscription_cubit_analytics_test.dart` (`paywall_load_failed` reason / preload / trigger_feature) |
| Reset onboarding rerun | `settings_cubit_reset_onboarding_test.dart`, `wow_cubit_test.dart` "onboarding re-run from Settings: onboarding_rerun", `wow_screen_test.dart` "onboarding re-run: the recap and Continue, no prices" |
| Existing-user paywall entry points unchanged | `drawer_menu_test.dart`, `usage_chip_and_gate_test.dart`, `usage_external_entry_gate_test.dart`, `ms_routes_subscription_trigger_test.dart`, `paywall_context_test.dart`, `subscription_screen_test.dart`, `subscription_body_test.dart`. Code review: without the new `flow` parameter `SubscriptionScreen` is unchanged; the only shared change is the store-unavailable retry now calling `retryLoad()` (adds `paywall_retry_tapped`) |
| Account deletion (backend cascade + recap cleanup) | `test_delete_account.py` (cached recaps dropped after commit, failure still 204, none on commit failure), `test_delete_account_cascade.py` (memory items hard-deleted, other users untouched) and the new suppressions test below |

**Gap closed (QA commit `cc8288b`, backend branch):** `app/tests/test_delete_account_cascade.py::...::test_delete_user_with_orca_memory_suppressions_orm_path`. `user_memory_suppressions` (keyed hashes of facts the person asked Orca to forget) had no account-deletion test. The model deliberately has no `relationship()` on User, so only the FK's ON DELETE CASCADE removes the rows. The test runs with the FK pragma on, checks the user's rows are gone and another user's survive. Passes.

## 5. PostHog

The agents' commit messages list the events but carry no formal coverage table, so the table below was built from the code and the tests.

| event | fires in (one place each) | test asserting properties |
|---|---|---|
| `personal_reveal_viewed`, `personal_reveal_cta_tapped` | `wow_cubit.dart` | `wow_cubit_test`, `wow_screen_test` |
| `first_conversation_intro_viewed` (answers_filled) | `first_conversation_intro_cubit.dart` | `first_conversation_intro_cubit_test` |
| `first_conversation_started` (mode, entry_point) | `first_conversation_cubit.dart` | `first_conversation_cubit_test` |
| `mic_permission_result` (result, source) | intro cubit + conversation cubit (different moments: start vs mid-session) | both cubit tests |
| `mic_settings_opened` (source) | `first_conversation_view.dart` | `first_conversation_views_test` |
| `first_conversation_phase_reached` (phase, source) | conversation cubit | cubit test (each phase once) |
| `first_conversation_mode_switched` (from, to, reason) | conversation cubit | cubit test |
| `first_conversation_connection_lost` (reconnected) | conversation cubit | cubit test |
| `first_conversation_ended` (mode, duration_s, user_turns, reached_open, token counts) | conversation cubit | cubit test (exact values) |
| `first_conversation_recap_result` (status, latency_ms) | conversation cubit | cubit test |
| `post_onboarding_offer_shown` (recap_status, prices_loaded, starter_shown) | `wow_cubit.dart` | `wow_cubit_test` |
| `post_onboarding_offer_result` (result, step) | `wow_cubit.dart` | `wow_cubit_test` |
| `post_onboarding_offer_not_shown` (reason incl. `onboarding_rerun`, premium_source) | `wow_cubit.dart` | `wow_cubit_test` |
| `paywall_shown` trigger `post_onboarding` / `post_onboarding_all_plans` | `starter_package_cubit.dart` / `subscription_cubit.dart` | `starter_package_cubit_test`, `subscription_cubit_analytics_test`, `wow_cubit_test` |
| `paywall_load_failed` (reason, preload, trigger_feature, error_class), `paywall_retry_tapped` | `subscription_cubit.dart` (+ retry in `wow_cubit.dart`) | `subscription_cubit_analytics_test`, `wow_cubit_test` |
| `onboarding_reset` | `settings_cubit.dart` | `settings_cubit_reset_onboarding_test` |
| `orca_memory_viewed` (item_count, status), `_item_deleted`, `_cleared` (item_count), plus `_delete_undone`, `_clear_cancelled`, `_action_failed` (action, error_class) | `orca_memory_cubit.dart` | `orca_memory_cubit_test` (exact maps) |
| backend `orca_memory_items_saved` (count, source) | `reflect.py` recap, `conversation_analysis.py` analysis (only when rows were written) | `test_orca_memory_feeding.py` (exact dicts for `reflect` and `first_conversation`), `test_orca_memory_recap.py` (once on a repeat call, none when nothing saved) |

Extra client events beyond the SPEC table, all under the privacy guard: `first_conversation_session_renewed`, `_intro_dismissed`, `_mute_toggled`, `_voice_retried`, `_send_failed`, `_start_failed`, `_skipped`.

**Privacy guard** (`test/support/reflect_analytics_guard.dart`) is structural, not a checklist: every captured event is checked for fixture text (transcript lines, typed replies, the opening question, recap items, focus areas, companion and user names, memory text), forbidden keys (`crisis`, `crisis_detected`, `crisis_language`, `in_therapy`, `currently_in_therapy`, `has_schedule`, `question_set`, `category`), forbidden values (`crisis`, `crisis_conversation`, `next_session`, `therapy_wish`, `weighs_on`), a closed vocabulary per event family, primitives only and a 40 character bound, plus an anti-vacuity check that every expected event actually fired. It is driven by `first_conversation_privacy_test.dart`, `first_conversation_views_test.dart`, `wow_cubit_test.dart` ("privacy + funnel", recap text as fixture), `orca_memory_cubit_test.dart` (memory text as fixture) and has its own self-test (`reflect_analytics_guard_test.dart`). Backend: `test_first_conversation.py` (session-started event carries no text), `test_orca_memory_feeding.py` (crisis cached, never sent to PostHog), `test_first_conversation_security_guards.py`.

**SPEC section 6 is out of date versus the implementation (deliberate, security-driven, for the lead to accept):**

1. `first_conversation_cta_tapped` was retired as a duplicate; the funnel uses the existing `personal_reveal_cta_tapped`.
2. `first_conversation_intro_viewed` no longer carries `in_therapy` (therapy-status proxy, security audit M-4).
3. `orca_memory_item_deleted` no longer carries `category` (coarse label of health content, M-4).
4. The crisis branch sends no event at all (H-1), so it cannot be counted in PostHog by design.

## Notes, not blockers

| note | owner |
|---|---|
| `test_worker_logging_config.py` uses a fixed 60 s child-process timeout that a loaded machine can exceed; consider a larger timeout | qa-testing (test file) |
| `_memory_written_since` relies on Postgres casting a naive UTC parameter with the session TimeZone, correct while the server stays on UTC | data-analytics (awareness only) |
| `messages` has no index on `conversation_id`; the idle job and the deletion cascades scan it (cheap today, grows with the table), per the DBA pre-deploy report | backend-api (follow-up migration) |
| 26 pre-existing frontend failures and 1 hanging test file stay in the `dev` baseline | flutter-mobile |

## Not covered by automated tests (device QA before stores)

Live realtime behaviour of `gpt-realtime-2.1` with the phase tool and `function_call_output`, the silent reconnect and the 50 minute renewal on a real call, the 5 s final-transcript drain on a real device, iOS and Android mic permission dialogs, real StoreKit / Play purchases on offer steps 1 and 2, and the deploy sequence itself (push `main`, then `heroku run alembic upgrade head --app mindsync`, then confirm `alembic current` = `m315a1b2c3d4`).
