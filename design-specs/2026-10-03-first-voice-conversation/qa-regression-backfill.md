# QA regression: Orca memory backfill batch

- **Date:** 2026-10-05
- **Agent:** qa-testing (pre-deployment)
- **Spec:** `SPEC-backfill.md` in this folder (incl. 5b), screens `screens/Memory*.dc.html`, security review `audit-security.md` (backfill section)
- **Final heads tested:**
  - backend `MindSync/` `feat/orca-memory-backfill` = **`0945d927bf245e5e95678c7bd87f34dcf2e561a4`**, 9 commits on `main` (`cc8288b`): 52c01c2, 52113e7, 220922f, 51a6202, 2842742, 3a61a38, a8ec3e6, 3172e49, 0945d92
  - frontend `mindsync-frontend/` `feat/orca-memory-backfill` = **`3343c370b1db6a982057ae92bba850581634cdcd`**, 5 commits on `origin/dev` (`0031c44`): a195551, 87184dd, 902f719, e8924c5, 3343c37

## Verdict: GO for both final heads

No regression in either repo. Every failing test is in the known baseline. The Postgres checks were done against a real Postgres 17 server with the prod drift reproduced, not only compiled: the migration runs, is idempotent both ways, and all 276 backfill, endpoint, source-link and forget-race tests pass on it. Security finding B-H1 (crisis counts in logs and job results), which blocked the first backend head, is fixed at the final head and has a test. Nothing blocking was found; the notes in section 6 are follow-ups.

| layer | final head result |
|---|---|
| Backend pytest (0945d92) | 223 files, 7102 run: 7093 passed, 9 failed = exactly the 9 known baseline failures. No timing flake this time. |
| Backend Postgres reality | one alembic head `m316a1b2c3d4` (down `m315a1b2c3d4`); m316 DDL clean offline and run for real on Postgres 17.2 (upgrade, re-upgrade, downgrade, re-downgrade, upgrade); ORM DDL equals migration DDL; `app.main` boots offline, 25 jobs after two lifespans, sweep and idle job registered once each; 0 naive vs aware hazards |
| Frontend `flutter analyze` (3343c37) | 0 errors (`error •` 0, `error -` 0), 10 warnings, 143 infos, none in a file this branch touched |
| Frontend `flutter test` (all directories, per directory) | 3229 passed, 24 failed, 2 hang: the same 26 as the `dev` baseline |
| Critical flows | every flow in the checklist has passing tests (section 4) |
| PostHog | every new or changed event fires from one place and has a test asserting its properties; privacy guard covers text, crisis, in_therapy, question_set, category and now source_kind (section 5) |

## 0. The heads moved during the run

The lead's brief named backend 2842742 and frontend 902f719. While QA ran, the security fixes landed (backend 3a61a38, a8ec3e6, then 3172e49, 0945d92; frontend e8924c5, then the test-only 3343c37), and for a while the backend working tree held them uncommitted. To keep every result attributable to a commit, the backend was tested in a detached worktree (removed afterwards), never in the shared working tree, in three full runs:

| backend run | head | files | passed | failed |
|---|---|---|---|---|
| A | 2842742 (lead's original head) | 221 | 6846 | 9 (baseline) |
| B | a8ec3e6 (security fixes) | 222 | 6980 | 9 (baseline) |
| C | **0945d92 (final)** | 223 | 7093 | 9 (baseline) |

Each run was four sequential foreground chunks (the full suite exceeds the 10 minute tool limit; conftest uses an on-disk SQLite file, so chunks never run in parallel). Postgres checks, boot check and the datetime review were redone at a8ec3e6 and again at 0945d92 (m316 and the models did not change between those two).

Frontend: the full per-directory sweep ran with `lib/` at e8924c5 (3343c37 changes test files only). Analyze plus every directory the lead listed (`test/screens/orca_memory`, `test/screens/first_conversation`, `test/screens/wow`, `test/bloc`, `test/screens/settings`, `test/support`, `test/l10n_completeness_test.dart`) were rerun on 3343c37.

## 1. Backend test suite (final head 0945d92)

| chunk | passed | failed |
|---|---|---|
| 1 | 1904 | 1 |
| 2 | 1503 | 4 |
| 3 | 2067 | 1 |
| 4 | 1619 | 3 |
| **total** | **7093** | **9** |

The 9 failures are the baseline list exactly, identical in all three runs:

| test | class |
|---|---|
| `test_first_impression.py::TestFirstImpressionEndpoint::test_language_mapping` | baseline |
| `test_notification_improvements.py` x4 (`TestBetweenSessionsPlaceholder` x3, `TestNotificationTimezoneIndexMigration::test_migration_creates_index`) | baseline |
| `test_onboarding_v2.py::TestResetTherapyOnboarding::test_preserves_therapy_data` | baseline |
| `test_symptom_suggestions.py::TestSymptomSuggestionResponseSchema::test_from_attributes_config` | baseline |
| `test_therapy_frequency.py::TestIsOnWeekYearBoundary::test_year_boundary_dec_to_jan_known_limitation` | baseline |
| `test_walkthrough.py::TestCompleteWalkthroughStepEndpoint::test_all_five_tabs_awards_points` | baseline |

`test_worker_logging_config` and `test_subscription_job_worker_wiring` (known timing flakes) passed in all three runs.

## 2. Backend Postgres reality

### 2.1 Migration m316a1b2c3d4

`alembic heads`: one head, `m316a1b2c3d4`, `down_revision = m315a1b2c3d4` (the previous batch's head, parent `m314b2c3d4e5`). The migration probes the live database, so its `upgrade()` / `downgrade()` were driven through an as_sql `MigrationContext` on the postgresql dialect with the probes set per state:

| state | emitted DDL (final head) |
|---|---|
| prod at m315 | `SET LOCAL lock_timeout = '5s'`; `ALTER TABLE users ADD COLUMN memory_backfilled_at TIMESTAMP WITH TIME ZONE`; `ALTER TABLE user_memory_items ADD COLUMN source_kind VARCHAR(32)`; `ADD COLUMN source_item_id INTEGER`; `CREATE INDEX ix_user_memory_items_user_id_source_kind_source_item_id ON user_memory_items (user_id, source_kind, source_item_id)`; two `INSERT INTO model_pricing ... VALUES ('gpt-realtime-2.1', 'REALTIME', 32.0, 64.0, 0.4, ...)` and `('gpt-realtime-2.1-mini', 'REALTIME', 10.0, 20.0, 0.3, ...)` |
| already at head | nothing |
| columns present, pricing rows missing | only the two INSERTs, no lock statement |
| downgrade | lock timeout, drop index, drop the three columns, delete only the two active 2.1 rows |
| already down | nothing |

All columns nullable, no default, no native enum, no table rewrite, no data backfill.

**Run for real on Postgres.** A throwaway Postgres 17.2 cluster (local, port 55432, `TimeZone = UTC`, data directory deleted afterwards) with the schema built by `create_all` and the three m316 objects dropped to simulate prod at m315:

| step | users.memory_backfilled_at | source_kind | source_item_id | index | active 2.1 pricing rows |
|---|---|---|---|---|---|
| create_all (fresh DB) | timestamptz | varchar(32) | integer | present | 0 |
| simulated prod at m315 | absent | absent | absent | absent | 0 |
| upgrade | timestamptz | varchar(32) | integer | present | 2 |
| upgrade again | same | same | same | same | 2 |
| downgrade, twice | absent | absent | absent | absent | 0 |
| upgrade | timestamptz | varchar(32) | integer | present | 2 |

The pricing INSERT goes into the native `apitypeenum` column (labels `CHAT ... REALTIME`, names equal values, so no enum drift risk) through psycopg2 2.9.9 without a cast error; an existing `gpt-realtime-2` row is never touched. The ORM DDL of `users` and `user_memory_items` (76 tables compile on the postgresql dialect) matches the migration column for column, so a web boot whose `create_all` runs before `alembic upgrade head` leaves nothing to fight over. All three new columns are in `exclude_properties`, so no ORM SELECT or INSERT names them before the migration.

### 2.2 The backfill code on real Postgres with prod drift

The four new SQLite suites were pointed at the Postgres server through a QA-only pytest plugin (kept outside the repo), with prod's drift reproduced: `messages.created_at`, `conversations.created_at` and `conversation_summaries.created_at` altered to `timestamp without time zone` (prod per `db-reports/2026-10-03-first-conversation-predeploy-check.md`), everything else as the migrations create it (`session_debriefs`, `session_prep_cards`, `between_session_notes`, `session_recordings`, `user_goals`, `reflect_summary_cards`: `created_at timestamptz` in their creating migrations), native enums, real row locks (`SELECT ... FOR UPDATE`), the SQLite `PRAGMA` column-drop helpers replaced by Postgres equivalents.

| head | suites | result |
|---|---|---|
| 2842742 | `test_orca_memory_backfill`, `test_orca_memory_backfill_api`, `test_memory_content_until_forget_race` | 141 passed |
| a8ec3e6 | the three above + `test_orca_memory_source_links` | 259 passed |
| **0945d92** | same four | **276 passed** |

This covers the digest over every source, the sweep selection (a `UNION ALL` mixing naive and aware timestamp columns, `max()` and `HAVING` on it), the endpoint statuses, Redis down, the column-missing deploy gap (`unavailable`, no call, source deletes a no-op), the forget race under real row locks, and the source-linked deletes.

### 2.3 Boot

`import app.main` offline (throwaway SQLite, Firebase stubbed, rq-scheduler replaced by an in-memory fake keyed by job id), lifespan run twice, at all three heads:

- 348 routes (347 before the batch): `GET` and `DELETE /api/v1/users/memory`, new `POST /api/v1/users/memory/backfill`.
- 25 jobs after the first and after the second boot (24 before the batch), no duplicate descriptions.
- `mindsync_orca_memory_backfill_sweep`: one copy, `5,20,35,50 * * * *`, queue `default`, dotted path `app.tasks.orca_memory_backfill.sweep_memory_backfill`.
- `mindsync_reflect_idle_analysis`: one copy, `10,25,40,55 * * * *`, queue `default`.
- Worker cold import of `app.tasks.orca_memory_backfill` without `app.main`: OK.

### 2.4 Naive vs aware datetimes (CS-07 family)

Every added line touching datetimes in `app/services`, `app/crud`, `app/tasks`, `app/core`, `app/api` was reviewed at each head. **0 hazards.** Python-side compares, `max`/`min`, sorts and subtractions all go through `orca_memory._aware` or `as_aware_utc` first:

| where | what | normalized by |
|---|---|---|
| `orca_memory_backfill.py` `_load_turns` | message times | `_Turn.created_at = _aware(created_at)` |
| `_before`, `_at_or_after`, `_first_time`, `_covered_through`, `_last_activity` | forget cutoff, memory-fed cutoff, idle cutoff, covered turns | `_aware()` inside each helper; `forgotten_at` from `get_memory_forgotten_at` (`as_aware_utc`) |
| `Collector.crisis_at`, `_prep_window_has_crisis` (B-M4) | crisis times vs a prep card's 14 day window | `_aware()` on append; window ends from `content_time` (aware) |
| `build_digest` sort, `Digest.newest_content_time`, `content_until` per group | chunk times | every `occurred_at` / `content_at` built with `_aware()`, `_EPOCH` aware |
| `select_backfill_candidates` | quiet period, 365 day window | SQL side (`HAVING max(at) <= :quiet_since`); returned time via `_aware()` |
| `crud/user_memory.py` `create_memory_items(content_until=...)`, `_read_forgotten_at_under_lock`, `get_memory_backfilled_at` | forget race guard | `_content_until_as_utc` / `as_aware_utc` |
| 3172e49, 0945d92 | JSON-decoded crisis scan, word lists, `failure_ttl` | no datetime code |

The Postgres runs in 2.2 are the runtime proof: the same code paths ran against naive prod-shaped columns without a `TypeError`.

### 2.5 Other backend checks

- **B-H1 (security):** at the final head the job log line is `user, status, saved, chunks, digest_chars, done, attempts, duration`; no crisis count in the log or in `as_dict()`. Both enqueue paths set `result_ttl` and `failure_ttl`. Guarded by `test_job_logs_and_result_carry_no_crisis_signal`.
- **Deploy gap (code live, migration not run):** `users.memory_backfilled_at` missing gives `backfill_status: "unavailable"`, `POST` answers 200 `unavailable` and enqueues nothing, the sweep skips; the link columns missing make source deletes a no-op (the debrief, prep card, note, recording and goal deletes still succeed) and a fact that needs a link is not written. The availability cache stores only positive results, so the app picks the columns up after `alembic upgrade head` without a restart.
- **Queue:** the on-demand job goes through `enqueue_interactive` (`high`, falls back to `default` when no worker listens there); `Procfile` on `main` already runs `high default`. No Procfile change in this batch.
- **Contract:** `MemoryItemResponse` now carries optional `source_kind`; the client reads it as optional (`OrcaMemoryItem.sourceKind`), so either side can ship first.

## 3. Frontend

**`flutter analyze`** (on 3343c37 and earlier on e8924c5): 0 errors in both output formats, 10 warnings and 143 infos, all in files this branch did not touch (the same 153 as the morning QA of the previous batch).

**`flutter test`, one directory per invocation** (never the whole suite; `test/marketing_shots/` not run, it is tagged and belongs to another session):

| directory | passed | failed |
|---|---|---|
| `test/` root (`l10n_completeness_test`, `widget_test`) | 18 | 0 |
| `api` | 138 | 0 |
| `bloc` (rerun on 3343c37) | 147 | 0 |
| `core` | 86 | 0 |
| `navigation` | 70 | 0 |
| `providers` | 16 | 0 |
| `support` (rerun on 3343c37) | 23 | 0 |
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
| `screens/first_conversation` (rerun on 3343c37) | 144 | 0 |
| `screens/health_check` | 30 | 0 |
| `screens/main_page` | 44 | 0 |
| `screens/main_tab/cubit` | 174 | 0 |
| `screens/main_tab/widgets` | 94 | 0 |
| `screens/moments` | 22 | 0 |
| `screens/my_therapy` | 13 | 0 |
| `screens/orca_memory` (rerun on 3343c37) | 90 | 0 |
| `screens/reflect_entry` | 80 | 0 |
| `screens/reflect_tab` | 154 | 0 |
| `screens/settings` (rerun on 3343c37) | 53 | 0 |
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
| `screens/workspace` (threads, todo, topics) | 118 | 0 |
| `screens/workspace/widgets` | 25 | 0 |
| `screens/wow` (rerun on 3343c37) | 147 | 0 |
| **total** | **3229** | **26** |

The 26 non-passing tests are the `dev` baseline, test for test:

| file | count | cause |
|---|---|---|
| `test/ui/reflect_tab/reflect_chat_bubble_test.dart` (3), `reflect_chat_input_test.dart` (5), `reflect_starter_chips_test.dart` (1), `reflect_thinking_indicator_test.dart` (4), `test/ui/settings/widgets/save_feedback_indicator_test.dart` (5) | 18 | stale widget-shape assertions, same names as the baseline |
| `test/screens/therapy_tab/therapy_card_detail_screen_error_test.dart` | 6 | harness has no Router (`BackButtonListener`), same names as the baseline |
| `test/screens/fab_flows/record_session_appbar_close_test.dart` | 2 | never completes (stopped by a 150 s guard) |

A temporary `dev` worktree was not needed: the names match the baseline that was rerun on `dev` this morning (`qa-regression.md`), and this branch touches neither those test files nor the widgets they test (its `lib/` changes are the memory API client and models, analytics constants, l10n, one route constant, the audio chat cubit, the first conversation cubit and turn driver, and the memory screen).

One run of `screens/workspace/widgets` ended with "Connection closed before test suite loaded" on four files while the machine was short of memory (two other sessions active); the directory passed on the rerun (25 of 25). Environment, not code.

## 4. Critical flows: where the tests are

| flow | covered by (all passing) |
|---|---|
| Memory screen: `not_started` on open, one POST, reading state, poll, `done` with notes | `orca_memory_backfill_cubit_test.dart` "one POST, the reading state, poll -> done with notes" (exact state sequence, POST once); `orca_memory_backfill_screen_test.dart` "not_started: one request, the calm reading state with skeleton notes in a live region", "the poll that finds the notes replaces the reading state" |
| Still running after 90 s: slow state, Try again | cubit "still running after the window: the slow state, then polling stops", "default timing is 4 s for up to 90 s", "Try again on the slow state polls again ... no POST", "Try again after a POST this visit never POSTs again"; screen "still running after 90 s: taking longer than usual with Try again" |
| Request fails, server could not queue it, run ends without notes: never a loop | cubit "the POST fails (500)", "fails offline", "POST says not_started", "poll says not_started: never a second POST"; screen "the request fails: the existing empty state, no loop" |
| `unavailable` and old backend without the field | cubit "unavailable ... existing empty state, no POST", "an older backend without the field parses to done", manager "GET with an unknown status is done"; screen "unavailable: the existing empty state, no request" |
| 503 / 404 during a poll, closing the screen | cubit "a poll answered 503: the calm unavailable state, polling stops", "closing the screen stops polling" |
| Forget one + Undo | `orca_memory_screen_test.dart` group "forget one (M6)" (gone at once, Undo bar, sent after 5 s, Undo restores in place, leaving sends at once, failure brings it back); `orca_memory_cubit_test.dart` group "delete one (deferred, with undo)" |
| Forget everything | screen group "forget everything" (in-app sheet, Keep my notes changes nothing, confirmed empties); cubit group "forget everything" (204, nothing to clear, failure, cancelled, 503) and "Forget everything inside a window covers the pending note" |
| Filter chips | screen "filter chips: All plus one per category with notes", "forgetting the last note of the selected category falls back to All"; cubit "a category chip filters; All clears it; one event per change, is_all only", "a refresh keeps the chip" |
| Empty state CTA route | screen "Talk with the companion opens the Reflect voice/text choice, not the onboarding conversation" (lands on `/main-page/tab/reflect?new=true`, `new=true` maps to the existing `new_thread` action in `MsRoutes.parseTabDeepLinkParams`, covered by navigation tests) |
| Backfill notes name their source (B-M2) | screen "a look-back note names what it was read from (source_kind, B-M2)", "German source labels"; cubit "source_kind is optional" |
| First conversation phase driver | `first_conversation_phase_driver_test.dart`: voice without any tool call goes 1 of 3, 2, 3, open with one log per phase (`turns`); short or empty transcripts never move it; interruption counted once; tool and turns racing never go back; reconnect restores from history; text mode crisis turn never moves it (B-L7) |
| Tool path: `output_item.added` / `response.done`, no `name` in `function_call_arguments.done` | `test/bloc/audio_chat_first_conversation_test.dart` group "function calls as the realtime API sends them": "arguments.done without a name: the name comes from output_item.added; answered once", "the name is found by item_id", "a call that only surfaces in response.done is applied and answered", one `response.create` per user turn |
| First conversation part 1 prompt (5b) | backend `test_first_conversation_part1_rules.py`: one question per topic and no follow-ups, the old dwelling rule gone, the transition turn after question 3, part 2 and safety unchanged, risk disclosures never parked for later, phase tool description matching the turns, reconnect note, no banned dashes |
| Onboarding, first conversation, recap, offer unchanged | `screens/wow` 147, `screens/first_conversation` 144, `screens/therapy_onboarding` 160, all green; the batch does not touch the wow, offer, recap or onboarding code |
| Existing paywall entry points unchanged | `screens/subscription` 175, `screens/usage` 95, `navigation` 70, `widgets` 158 green; no paywall, usage-gate or subscription file changed on this branch |
| Backend endpoint statuses, Redis down, consent, forget, crisis, cap, idempotency, watermark, sweep bound | `test_orca_memory_backfill_api.py`, `test_orca_memory_backfill.py`, `test_orca_memory_source_links.py`, `test_memory_content_until_forget_race.py`, `test_orca_memory_forget_race_writers.py`, `test_crisis_language_third_person.py`; on SQLite in the full suite and the first four also on Postgres |

## 5. PostHog

| surface | user action | event | key properties | fires in | test asserting it |
|---|---|---|---|---|---|
| memory screen | opens; sees list, empty, reading, slow, unavailable, error | `orca_memory_viewed` | `item_count`, `status` (loaded, empty, unavailable, error, **backfilling**, **backfill_slow**) | `orca_memory_cubit.dart` `_logViewed` | backfill cubit test (`viewedStatuses()` sequences, exact `{item_count: 2, status: loaded}`), `orca_memory_cubit_test` |
| memory screen | the app asks Orca to look back | `orca_memory_backfill_requested` (new) | none | `orca_memory_cubit.dart` `_requestBackfill`, once per visit | backfill cubit test (exactly one, empty props; none on Try again) |
| memory screen | taps a filter chip | `orca_memory_filter_selected` (new) | `is_all` only | `orca_memory_cubit.dart` `selectFilter` | cubit "one event per change, is_all only"; screen privacy test |
| memory empty state | taps Talk with {orcaName} | `orca_memory_empty_cta_tapped` (new) | none | `orca_memory_cubit.dart` `emptyCtaTapped` | cubit test; screen CTA test |
| memory screen | deletes, undoes, clears, cancels, action fails | `orca_memory_item_deleted`, `_delete_undone`, `_cleared` (`item_count`), `_clear_cancelled`, `_action_failed` (`action`, `error_class`) | unchanged | `orca_memory_cubit.dart` | `orca_memory_cubit_test` (exact maps) |
| first conversation | answers questions | `first_conversation_phase_reached` | `phase`, `source` (`tool`, **`turns`**) | `first_conversation_cubit.dart` `_reachPhase` | phase driver test (exact `(phase, source)` pairs, one per phase) |
| backend job | facts saved by the backfill | `orca_memory_items_saved` | `count`, `source: "backfill"` | `app/tasks/orca_memory_backfill.py` `_capture_saved` | `test_orca_memory_backfill.py` "success ... sends a content-free event" (exact dict), "no event when nothing was saved" |

No gaps. Each fact is emitted once, on one side. By lead decision there is no backend event for the gate outcomes (consent withdrawn, unavailable); what the person saw is still counted by `orca_memory_viewed`.

**Privacy guard** (`test/support/reflect_analytics_guard.dart`, extended in 3343c37): on every captured event, forbidden keys `crisis`, `crisis_detected`, `crisis_language`, `in_therapy`, `currently_in_therapy`, `has_schedule`, `question_set`, `category`, `source_kind`; forbidden values `crisis`, `crisis_conversation`, `next_session`, `therapy_wish`, `weighs_on`, plus memory-scoped `recording`, `debrief`, `prep_card`; the fixture texts (memory note texts, transcript lines, recap items) must not appear in any value. On governed events also a closed vocabulary, primitives only and a 40 character bound, plus an anti-vacuity check. Driven for this batch by `orca_memory_backfill_cubit_test` ("the look-back events carry no memory text"), `orca_memory_screen_test` ("filter and empty-CTA events carry no category and no text"), `orca_memory_cubit_test`, and the first conversation privacy tests; the guard's own self-test passes. Backend: no crisis signal in the job log or result (2.5).

## 6. Notes, not blockers

| note | severity | owner |
|---|---|---|
| The sweep fires at minutes 5, 20, 35, 50, the same minutes as the upload finalizer (`setup_frequent_upload_finalizer`), both on `default`; the idle analysis was deliberately offset from the finalizer. The sweep caps queued work at about 240 s per tick, so during the initial drain a finalizer run can wait up to about 4 minutes. Consider other minutes (for example 2, 17, 32, 47). | Low | backend-api |
| `backfill_status` is also `unavailable` when the memory gate blocks for another reason (flag off and no memory notice), not only for withdrawn PROFILING or a missing column as SPEC section 3 says. Intended (status and job share one rule, so the app never asks forever); the spec text should say so. | Info | lead (spec) |
| The empty-state CTA uses `context.go`, so the Reflect tab replaces the memory screen and Settings in the stack. Fine for "start a conversation", worth a glance on device. | Info | flutter-mobile / ui-ux-designer |
| The privacy guard has no literal `text` key in its forbidden list; free text is caught by the fixture-content scan, the closed vocabulary and the 40 character bound. Optional hardening. | Info | qa-testing |
| `flutter test` on this machine can fail to load suites under memory pressure ("Connection closed before test suite loaded"); rerun the directory alone before calling it a failure. | Info | qa-testing |
| 26 pre-existing frontend failures and 1 hanging test file stay in the `dev` baseline. | Info | flutter-mobile |

## Not covered by automated tests (device and prod checks)

- Deploy sequence: push `main` (0945d92), then right away `heroku run alembic upgrade head --app mindsync`, confirm `alembic current` = `m316a1b2c3d4 (head)`; then the frontend to `dev`. In the gap the app degrades to `backfill_status: "unavailable"` and source deletes skip the memory rows, nothing fails.
- After deploy: `heroku logs` grep shows no `crisis` in any `[OrcaBackfill]` line; database-administrator checks the `users.memory_backfilled_at` fill rate and that the `user_memory_items` rows written by the backfill carry `source_kind`; the sweep drains without starving the finalizer.
- Quality of the notes a real model writes from real histories, in all seven languages.
- On device: the reading state with VoiceOver and TalkBack (live region), the 90 s slow state, pull-to-refresh, forget one with Undo, Forget everything, filter chips, the empty CTA, and the first conversation phase indicator with live `gpt-realtime-2.1` (turns and tool path).
