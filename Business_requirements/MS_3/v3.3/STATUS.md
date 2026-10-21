# MSV3.3 – STATUS board

Spec: `MSV3_3_Change_Spec_v2.md` (23 items: 2 DELETE · 10 FIX · 11 CHANGE)
Batch opened: 2026-08-14

## Starting state (verified at batch open)

| | |
|---|---|
| Backend repo | `MindSync/`, branch `main`, HEAD `67b1bdc`, clean, in sync with origin |
| Frontend repo | `mindsync-frontend/`, branch `dev`, HEAD `34f2af9`, clean, in sync with origin |
| Alembic single head | `ii0j1k2l3m4n` (two side branches are joined by merge migration `5cafadce1513`) |
| Backend test baseline | **20 failed / 5022 passed** (`python -m pytest app/tests/ -q`, 505s) |
| Flutter analyze baseline | 134 issues, **0 errors** (1 warning, rest info), exit 0 |
| Flutter test baseline | **32 failed / 1790 passed** – measured, not assumed (see below) |

### Flutter regression verdict: ZERO REGRESSIONS (verified by A/B, not by agent self-report)

Full suite with all batch changes: **1790 passed / 32 failed**, the 32 spread over 10 files:
`reflect_chat_input_test` (7) · `save_feedback_indicator_test` (5) · `reflect_thinking_indicator_test` (4) · `privacy_data_section_test` (4) · `reflect_chat_bubble_test` (3) · `wow_screen_adaptive_cta_test` (3) · `therapy_frequency_selector_test` (2) · `record_session_appbar_close_test` (2) · `reflect_starter_chips_test` (1) · `onboarding_lead_source_view_wave4_test` (1).

Those same 10 files were then run against a **clean stashed `dev` checkout**: **32 failures, identical**. So every failure is pre-existing. The "~30" figure carried in project memory was stale; 32 is the true current baseline.

This also independently clears the batch's riskiest change: `reflect_chat_bubble_test` fails identically with and without our work, and no Reflect source file was modified – confirming CS-16's shared-code deletion did not break the Reflect tab.

`flutter analyze` ended at **129 issues / 0 errors**, five below the 134 baseline.

### Backend regression verdict: 7 FOUND, ALL FIXED – FINAL: 20 failed / 5145 passed = BASELINE, ZERO REGRESSIONS

Final central run after the fixes: **20 failed / 5145 passed**, failing files identical to the baseline set (`test_voice_fixes` 5, `test_therapy_frequency` 5, `test_notification_improvements` 4, `test_custom_therapy_sessions` 2, `test_walkthrough` 1, `test_symptom_suggestions` 1, `test_onboarding_v2` 1, `test_first_impression` 1). **123 more tests passing than baseline** (5145 vs 5022) from this batch's new coverage.

Resolution of the 7, with the production-vs-test split:
1. **`TestMarkMomentPushDelivered` ×2 – PRODUCTION CODE FIX (a real bug).** `mark_moment_push_delivered` writes via raw `UPDATE`, bypassing the ORM, and suppressed `expire_on_commit` to protect other session objects – but never invalidated *that row's own* identity-mapped instance. A caller re-reading it in the same session would see stale data indefinitely. Fixed by targeted-expiring just that attribute. Verified not causing a live incident today (each moment is processed once per session), but a genuine footgun for future callers.
2. **Chain-tip assertion – TEST FIX.** Rewritten to assert the single-line-of-descent INVARIANT instead of hardcoding a revision, following precedent already set twice in this repo. Future batches will no longer break it.
3. **`test_legacy_cutover` – TEST FIX (mock fidelity).** CS-23 renamed `generate_weekly_therapy_summary` → `generate_weekly_summary_pipeline` with a new result type; the mock still targeted the old name, so real code hit an unconfigured `MagicMock` and died in `json.dumps()`. **The guarantee was NOT weakened** – `fcm.assert_not_called()` and `moment_hook.assert_called_once()` are unchanged.
4. **`TestTriageChipsLazyBackfill` ×3 – TEST FIX (stale fixture), and the "real bug" risk was actively disproven.** The fixture set the now-dead `open_threads` instead of the new `therapist_questions`, so the card legitimately yielded 3 candidates instead of 4. The agent verified the mechanism is healthy by populating the correct field and confirming all 4 candidates including the question chip appear. **Workspace triage is NOT broken.**

Full backend suite with the batch: **27 failed / 5138 passed**. The 12 failing files were then re-run in a **clean detached git worktree at HEAD `67b1bdc`**: **20 failed**. Delta = exactly 7, in four files that were 100% green before this batch.

**Why this mattered:** every backend agent had individually reported "0 net new failures" from its own targeted runs, and each was telling the truth *about its own changes in isolation*. The regressions only appear once all six agents' changes are combined. Targeted per-agent runs cannot catch cross-agent interaction – only a central full-suite run against a measured baseline can.

The 7:
| Test | Suspected cause |
|---|---|
| `TestMarkMomentPushDelivered::test_sets_true` / `test_sets_false` | NEW tests for CS-20's new CRUD function, failing – agent reported this file green, so either a later interaction broke it or these two were never actually run |
| `test_ii0j1k2l3m4n_is_currently_the_chain_tip` | stale assertion – this batch added 3 migrations after that revision. Being rewritten to assert the INVARIANT rather than hardcode a revision, so future batches do not keep breaking it |
| `test_data_generated_and_fcm_not_sent_on_happy_path` | CS-23's async rework of `weekly_therapy_summary.py`. ⚠ Guards a real product rule (cutover must not fire FCM) – must NOT be weakened to go green |
| `TestTriageChipsLazyBackfill` ×3 | CS-11 removed topic candidates from triage. ⚠ **Most likely to hide a real bug**: if backfill silently stopped working for QUESTIONS too, Workspace triage is broken and nothing in the spec would catch it |

The fixing agent must state, per item, whether it changed PRODUCTION CODE or a TEST, and justify any test change.

## LEAD'S OWN INDEPENDENT VERIFICATION (2026-08-14, not agent self-reports)

Everything below was checked by the lead directly, after all agents finished. Where an agent's claim and my measurement disagreed, the measurement wins.

### Backend
| Check | Result |
|---|---|
| Alembic single head (own tuple-aware script) | **`ll3m4n5o6p7q`**, 77 revisions, single head |
| Chain | `ii0j1k2l3m4n` → `jj1k2l3m4n5o` → `kk2l3m4n5o6p` → `ll3m4n5o6p7q` |
| Router mount / boot-critical imports | **324 routes**, all modules import |
| **Postgres-dialect DDL compile (offline)** | **75 tables, ZERO failures** – CLAUDE.md requires this; green SQLite is not evidence |
| 3 new migrations: idempotency guards | present (3 / 5 / 4 guard hits) |
| 3 new migrations: forbidden `Enum(PyEnum)` | **zero** (the pattern behind the H10 outage) |
| Full suite | **20 failed / 5145 passed = baseline, zero regressions** (+123 passing) |
| Nothing committed / no secrets in diff | confirmed, HEAD still `67b1bdc`, 68 dirty files |

Backend guardrails verified in source: Focus Area still present (only its feed into the prep mood section was cut), `AgendaItemKind.TOPIC` + `TriageProposalKind.TOPIC` NOT deleted (three features depend on them), `topic_question_items` table intact, `toggle_triage_proposal` still handles TOPIC so legacy pending proposals degrade gracefully.

CS-23 core verified directly: **zero `openai_service.generate*` calls remain in either endpoint file**, 2 RQ enqueues each, and both jobs are plain top-level module functions that import cleanly – so the "registered only in the web dyno" bug class does not apply.

### Frontend
| Check | Result |
|---|---|
| Goals module (CS-15 design source only) | **0 files modified** |
| Reflect tab (shared code with CS-16) | **0 files modified** |
| `threads_section.dart` (Fix 4/Fix 5 pills) | **0 files modified** |
| Timeline filter chips (CS-23 must not touch) | untouched; only the `no_period_yet` info message added |
| Removed definitions actually gone | `RealizationBadgesMixin`, `RealizationIndicatorBadge`, `_HubAndSpoke`, `_SourcePill`, `_EditModeBody`, `shareCardAsImage`, `_buildAgendaTopicPill` – all 0 live refs (remaining hits are explanatory comments + agent-memory `.md`) |
| Required survivors | `RealizationBadge` class kept, Reflect still calls `showMarkAsRealizationSheet`, `TopicItemTile` kept for legacy rows |
| l10n parity | **1728 keys × 7 locales, zero missing, zero extra** |
| New strings genuinely translated | yes in all 7 locales (spot-checked incl. `"+ Add thread"`, the three period-summary headers) |
| `flutter analyze` | **129 issues / 0 errors** (baseline 134) |
| Full suite | **1795 passed / 30 failed** – see note below → parity with the 32 baseline, zero regressions |

⚠ **Defect found by the lead that the agent's report did not reflect:** the CS-11/12/13 agent stated it had temporarily excluded `test/screens/fab_flows/record_session_appbar_close_test.dart` and "moved it back afterward". It had NOT – the file was still deleted in the working tree, which is why the run showed a flattering 30 failures instead of 32. **Restored via `git checkout`.** Verified standalone: the file contains a test that HANGS ("did not complete"), and it fails identically at clean HEAD, so it is a pre-existing defect, not ours. Worth its own ticket outside this batch.

### Typography compliance
Zero em-dashes in the ARB lines this batch added (product strings clean). 124 em-dashes in the lead's own two batch documents were mechanically replaced with en-dashes per the global rule.

### Security
One **High**, zero Critical – see `security-reports/2026-08-14-msv33-batch-audit.md`. HIGH-001 (therapy content in Redis job payloads) **blocks deployment of the CS-23 async piece** per CLAUDE.md and is being fixed. Independently spotted by the lead before the audit landed. Everything else came back clean: no IDOR on any touched path, premium gating survived the rewrite, new columns encrypted consistently, `push_delivered` raw SQL parameterised, share export structurally unable to capture unrelated content, and GDPR cascade intact (all new columns on tables with `ondelete="CASCADE"` to `users`).

## Guardrails carried from the spec

- Do NOT regress QA-passed Fix 4 / Fix 5 items: unified thread pill design (Fix 4 CS-01) + multi-line wrap (Fix 5 CS-01), Between Sessions realization flags (Fix 4 CS-02), Workspace Realizations "Delete" in the 3-dot menu (Fix 4 CS-04).
- Do NOT touch the **Goals** module – it is the design model for CS-15 only.
- Pop-outs (action prompts) are NOT in-app reminders. CS-17 fixes pop-out sequencing; CS-20 stops in-app duplication of pushes.
- Focus Area is excluded as a data source in CS-13 but is NOT removed in this batch.
- Flag icon stays the only save control into Workspace (Fix 2 CS-16), enforced by CS-16.
- CS-23 must not touch other Timeline views, existing generated cards, or the filter chips.

## Execution plan

| Phase | Items | Owner | Status |
|---|---|---|---|
| R · Recon | all | Explore ×4 | **DONE** |
| A · CS-23 backend (REBUILD) | CS-23 | data-analytics | **DONE** |
| B · CS-23 frontend | CS-23 | flutter-mobile | **DONE** |
| C · Topics→Questions | CS-11, CS-12 | backend-api + data-analytics + flutter-mobile | **DONE** |
| D · Prep card mood | CS-13 | data-analytics + flutter-mobile | **DONE** |
| E · Timeline visuals | CS-03…CS-09, CS-16 | flutter-mobile | **DONE** |
| F · Main + duration | CS-01, CS-02, CS-10 | flutter-mobile + backend-api | **DONE** |
| G · Workspace Threads | CS-14, CS-15 | flutter-mobile | **DONE** |
| H · Notifications | CS-17…CS-21 | backend-api + flutter-mobile | **DONE** |
| I · Share | CS-22 | flutter-mobile | **DONE** |
| V · Verification | – | lead (independent) + security-guardian | **DONE** |
| S · HIGH-001 fix | security blocker | data-analytics | **DONE** |

**ALL 23 ITEMS IMPLEMENTED. Batch verdict: GO, subject to device QA.**

## FINAL NUMBERS (lead-measured, after the HIGH-001 fix)

| | Baseline | Final | Verdict |
|---|---|---|---|
| Backend pytest | 20 failed / 5022 passed | **20 failed / 5145 passed** | baseline parity, **+123 passing** |
| Flutter test | 32 failed / 1790 passed | **1795 passed / 30 failed** (+2 from the restored pre-existing hanging file = 32) | baseline parity |
| Flutter analyze | 134 issues / 0 errors | **129 issues / 0 errors** | 5 better |
| Boot | – | 324 routes, all boot-critical imports OK | clean |
| Postgres DDL (offline) | – | 75 tables, **0 failures** | clean |
| Alembic | single head `ii0j1k2l3m4n` | single head **`ll3m4n5o6p7q`** | +3 migrations |

## DEPLOY CHECKLIST (operator)

⚠ **Nothing is committed.** Both repos hold the batch as uncommitted working-tree changes (BE ~68 files, FE ~94 files). Review, then commit and deploy in this order.

1. **Backend first, deploy + migrate TOGETHER.** Heroku has no release phase; migrations are manual. Three pending migrations:
   `ii0j1k2l3m4n` → `jj1k2l3m4n5o` → `kk2l3m4n5o6p` → `ll3m4n5o6p7q`
   ```
   git push heroku main
   heroku run alembic upgrade head --app mindsync
   ```
   - `jj1k2l3m4n5o` adds `push_delivered` to **`notification_moments`, a LIVE table** – if the deploy lands without the migration, every read of that table 500s on `UndefinedColumn`.
   - `ll3m4n5o6p7q` adds `therapist_questions` to **`session_debriefs` and `session_recordings`, both LIVE tables** (additive/nullable, but still must ship together).
   - `kk2l3m4n5o6p` is idempotent and skips its constraint with a loud warning if duplicate `(user_id, data_window_end)` rows exist. **Watch the log for that warning.**
2. **Ask `database-administrator` to audit prod for duplicate weekly rows** before assuming the uniqueness constraint applied.
3. **Then frontend**: push `dev` → Codemagic → TestFlight / Play internal.
4. **Old-build safety**: `EmotionalTemperatureItem` deliberately dual-writes the legacy `current_score`/`previous_score`/`trend` alongside the new `description`. Do NOT "clean up" those redundant fields – a regression test guards them. Removing them would make every already-shipped app build fail to parse the ENTIRE prep card (non-nullable cast in the generated Dart), not just the mood section.

## DEVICE QA REQUIRED (both platforms, per spec)

The spec closes every item against a device build. Not doable from here:
- CS-03…CS-09: screenshots of the four output cards (flat prep container, white backgrounds, identical section-header sizes, no chevrons, 48×48 tap targets).
- CS-08: Threads edit flow comfortable with a thumb; pill wrap not regressed.
- CS-10: **two real recordings**, card duration matches actual length to the minute.
- CS-15: Workspace Threads – 3 rows, Goals-style, 3-dot actions, "Show more".
- CS-16: long-press anywhere on a card produces nothing; flagging still works; **Reflect long-press still works**.
- CS-17: two pending pop-outs – the second must not appear until the first flow finishes.
- CS-18: with ONLY a custom future date set, the "no next session" push must NOT fire.
- CS-19/CS-21: every notification deep-links to its target; **no "Page Not Found" anywhere** (checklist in `CS21_NOTIFICATION_AUDIT.md`).
- CS-22: every share exports the full card as JPEG.
- CS-23: Generate Now on a brand-new account shows the informative no-period state, **not** an error with a dead retry.

## KNOWN ISSUES / FOLLOW-UPS (outside this batch)

1. **Existing recordings still carry the 16× inflated duration.** Raw audio is deleted after processing, so it cannot be recomputed from audio; transcripts ARE retained, so a word-count/WPM re-estimate is cheap. Needs an affected-row count from `database-administrator` + operator sign-off. Nothing was run against prod.
2. `record_session_appbar_close_test.dart` contains a test that HANGS (pending Timer). Pre-existing, fails identically at clean HEAD. Deserves its own ticket.
3. Dead code newly documented, not deleted (out of scope): `pattern_insight_sheet.dart`, `recovery_moment_sheet.dart`, `notice_banner_renderer.dart`, plus the entire legacy `PeriodicSummary` pipeline and the old CS-23 pipeline left in `openai_service.py` with zero production callers.
4. `_therapy_helpers.py::has_session_today` has the same custom-date bug class as CS-18 but was out of scope.
5. Redis TLS (`rediss://`) is never verified in code – `integration-devops` call.
6. `workspace_threadDeleteTooltip` is now an unused l10n key.
7. 288 em-dashes exist in code comments / agent-memory files added by this batch. **User-facing ARB strings are clean (0).** Left alone deliberately: churning them adds merge noise for no user benefit.

> Every phase APPENDS its section below when done. Do not edit another phase's section.

### Phase report template

```
## PHASE <X> – <name> – <DONE | PARTIAL | BLOCKED> – <date>
- Session commits (repo + hash + one-liner):
- Items completed (spec IDs):
- Items NOT completed / deviations + why:
- Impact recon (per CLAUDE.md): consumers checked, boot-critical paths, model/migration/prod agreement:
- API contract deviations:
- New migrations (id, chained from, applied on prod? NO):
- Test results (before → after vs baseline):
- Manual QA still needed (device/platform):
- Notes for next phases:
```

---

## Operator decisions (2026-08-14)

- **CS-23 – REBUILD FROM SCRATCH as written.** Recon proved the feature already exists end to end (tables + migrations, both AI pipelines, both hourly cron jobs registered *and* scheduled, `/generate` + `/retry` returning HTTP 200 error envelopes since Fix.1 CS-21, card UI with retry). The lead recommended fixing the four real defects instead; the operator was shown both options with costs and chose the rebuild. Proceeding as instructed. Existing tables are KEPT (they hold user data) – "from scratch" scopes to pipeline, endpoints, trigger and error state. The four known defects must not be reproduced: first-run cliff, synchronous OpenAI call inside the HTTP request (Heroku H12), FAILED-row visibility inconsistency, weekly duplicate-row race.
- **CS-11 – generate questions for all four output cards.** Verified in code that After Therapy renders `_debrief.openThreads` and Recording renders `topicsWithTimestamps` under the "Topics & Questions" title – an earlier fix round retitled both sections without giving them questions (source comments: "(was Unfinished Business)", "(was Main Topics)"). Rather than dropping the section on those two cards, the operator chose to extend the AI pipeline so all four cards produce three selectable questions. This is backend work beyond CS-11's literal text and makes CS-12's "four identical Questions sections" satisfiable.
- **CS-15 – deviation by necessity.** The spec says to place the 3-dot menu "wherever Goals places its row menu", but Goals has NO row menu (it uses a chevron plus in-expansion actions). Ruling: put the 3-dot menu in the trailing slot of the title row, the position Goals uses for its chevron. Honours both "copy Goals 1:1" and "remove the chevron, no expansion".
- **CS-01 – the Settings duplicate goes too.** Edit-layout had a second, independent entry point in Settings (`MainTabWidgetsSection`). Spec says "no edit-layout entry point exists anywhere", so both were removed.
- **CS-22 – export switched PNG → JPEG** per the spec's explicit wording.

---
<!-- Phase reports below -->

## PHASE A – CS-23 backend REBUILD – DONE – 2026-08-14
- Commits: none (working tree). Files: `weekly_summaries.py`, `monthly_audits.py`, `crud.py`, `schemas/summary.py`, `openai_service.py`, `tasks/weekly_therapy_summary.py`, `tasks/monthly_therapy_audit.py`, 6 test files.
- **Rebuilt fresh** (under a `# CS-23 REBUILD` banner): `WeeklySummaryPipelineResult` / `MonthlySummaryPipelineResult` (AI now emits card categories DIRECTLY as flat string lists, no second repackaging transform), `WEEKLY_SUMMARY_PIPELINE_PROMPT` / `MONTHLY_SUMMARY_PIPELINE_PROMPT`, `generate_weekly_summary_pipeline()` / `generate_monthly_summary_pipeline()`, `assemble_weekly_summary_sections()` / `assemble_monthly_summary_sections()`, async job entry points `run_weekly_summary_ai_job` / `run_monthly_audit_ai_job`, prep-then-enqueue endpoint bodies, `crud.lock_user_for_summary_generation`, the `no_period_yet` branch.
- **Carried over unchanged** (already correct): calendar-period math (`get_calendar_week_range_utc` / `get_calendar_month_range_utc`), deterministic `activity_summary` and `breakthroughs`/`realizations`.
- **Tables 100% intact** – zero changes under `app/models/` or `app/alembic/`, verified by git status. Historical rows untouched.
- **Four defects closed:** (1) first-run cliff → new `status="no_period_yet"`, a non-failure informative state; (2) NO OpenAI call remains inside request handling – both `/generate` and `/retry` prep synchronously then `rq_queue.enqueue(..., job_timeout=600)` and return `PROCESSING`; (3) `_fetch_monthly_audits_for_timeline` no longer excludes FAILED, so retry is reachable from every view; (4) weekly race closed via `SELECT ... FOR UPDATE` on the user row, acquired before the dedup check in both the endpoint and the cron.
- RQ safety: both new jobs are plain module-level functions in the SAME two modules that already host the working hourly cron entry points, so dotted-path resolution is proven by existing production behaviour. No new module, no registry indirection. `app/tasks/__init__.py` init runs on import of either module.
- Weekly constraint recommendation handed to backend-api: `weekly_therapy_summaries (user_id, data_window_end)` as `uq_weekly_summary_user_period` – `data_window_end` chosen because it is never signup-clamped.
- Content contract: empty categories have their KEY OMITTED (not null, not empty list); no-digits rule scoped to `how_you_felt` only, with a `_strip_banned_digits` backstop; counts explicitly allowed in `got_done`/`goals`.
- Tests: 423 passed / 0 failed across 10 targeted files. `import app.main` clean (rq mocked; the Firebase placeholder-credential failure is pre-existing and unrelated).
- ⚠ **OPEN – routed to backend-api:** `app/tasks/rag_indexing.py` builds RAG content from the legacy columns that new rows now leave NULL → new summaries get thin RAG content. Real semantic-search quality regression.
- ⚠ The OLD pipeline (`generate_weekly_therapy_summary`, `build_weekly_summary_sections`, old prompts, old result models) is left in the file with ZERO production callers – deleting it would break ~30–50 tests that unit-test it in isolation. Deliberate, not an oversight. Candidate for a later cleanup pass.
- ⚠ Weekly's `at_a_glance` is still populated on new rows (same text as `summary_sections.descriptive`) because `crud._fetch_weekly_summaries_for_timeline` reads it for the "All" feed preview snippet. Found during review, not in the brief.

## PHASE C1 – CS-11 schema half – DONE – 2026-08-14
- Commits: none (working tree). Files: `models.py`, `schemas.py`, NEW migration `ll3m4n5o6p7q`, NEW `test_cs11_therapist_questions_migration.py`, one assertion fixed in `test_msv33_backend_migrations.py`.
- **Contract for the parallel generation agent and Flutter:**
  `SessionDebrief.therapist_questions` → `DebriefResponse.therapist_questions`
  `SessionRecording.therapist_questions` → `SessionRecordingResponse.therapist_questions`
  Both `Optional[List[str]]`, backed by a nullable `Text` column holding encrypted JSON `["q1","q2","q3"]` – an exact mirror of the existing `SessionPrepCard.therapist_questions` pattern.
- Migration chain: `ii0j1k2l3m4n` → `jj1k2l3m4n5o` → `kk2l3m4n5o6p` → **`ll3m4n5o6p7q` = HEAD**. Head verified independently before writing, not trusted from the brief. Idempotent add-if-missing on both tables.
- ⚠ `session_debriefs` and `session_recordings` are LIVE PROD TABLES – additive nullable column, but must still ship WITH the deploy.
- ⚠ **Gotcha the agent caught and flagged:** `DebriefResponse` / `SessionRecordingResponse` are built with explicit field-by-field constructors, NOT `.model_validate(orm_obj)`. So the new field exists but serializes as `null` forever unless the endpoint call sites are updated to populate AND decode it. Routed to the generation agent with an explicit instruction to test the full round trip to the API response, not just DB persistence – a persistence-only test would pass while the client still sees null.
- Impact recon: grepped every `SessionDebrief`/`SessionRecording` consumer (`crud.py`, `rag_indexing.py`, `clinician_service.py`, `clinician_ai.py`) – all access specific named attributes, none enumerate columns generically, so a new nullable column touches nothing.
- Postgres-dialect DDL compiled offline and verified (SQLite green is not sufficient evidence per CLAUDE.md). `import app.main` clean through model registration, router mounting and full generator/detector registration.
- Tests: 14 new + 1 fixed; ran with all existing migration guards plus debriefs/recordings/prep_cards/timeline – **323 passed, 0 failed**.

## PHASE H2 – CS-18 / CS-19 / CS-20 backend + migrations + RAG – DONE – 2026-08-14
- Commits: none (working tree). **TWO NEW MIGRATIONS** – see the deploy warning at the bottom of this section.
- **CS-18, two independent bugs, both fixed.** (A) `update_therapy_schedule` persisted custom sessions only when `frequency == "custom"`, but the Flutter one-off flow always sends the user's *current* recurring frequency (e.g. `"weekly"`), so the backend wiped the date it had just been sent. (B) `compute_next_session_date` / `compute_last_session_datetime` hit `if not entries: return None` before ever consulting `custom_sessions`.
- ⚠ **THE BIG FINDING: 6 of the 10 downstream consumers had their own copy-pasted pre-gate** (`if not schedule: return None`) that would have defeated the shared-resolver fix entirely. Fixing only the utility would have left `therapy_appointment`, `therapy_prep`, `record_session`, `homework_reminder`, `between_sessions_note` and `post_session_reflection` generators still blind to custom dates. All six now mirror the already-correct pattern. Full per-consumer table delivered.
- ⚠ Residual, flagged not fixed (out of scope): `_therapy_helpers.py::has_session_today` has the same bug class – its custom-sessions check is gated behind `if frequency == "custom":`. Used by `debriefs.py`.
- **CS-19/CS-21 dead routes, server-side half.** `/stats` → `/main-page/tab/workspace` (notice, comparative); `/character/streaks` → `/main-page/tab/character` (celebrate_tease); `/stats/symptoms/{id}` and `/stats/symptoms/{id}/history` **dropped** (no successor screen exists); `mood_dip_alert_generator`'s `/exercises/breathing/quick` and `/symptoms/log` **dropped** (the sheet already falls back gracefully). Audited every other generator – all build routes via `route_for()`, all 14 confirmed routable.
- ⚠ Client-side gap flagged for flutter-mobile: `recovery_moment_sheet.dart` and `mood_dip_alert_sheet.dart` check only `isNotEmpty`, never `MsRoutes.isRoutable()`. Safe today because both fall back, but not guarded.
- Residual risk cheap-checked: STREAK_CELEBRATION / PATTERN_INSIGHT retired 21 days ago; every moment type uses ≤7-day expiry, so the `expires_at > now` filter almost certainly already excludes surviving rows. Not acted on.
- **CS-20 needed a schema change, not just a filter.** `status=SENT` could not distinguish "genuinely delivered via FCM" from "claimed but no token / FCM raised" – a filter alone could not both stop duplication AND preserve the in-app fallback for no-token users. New column `notification_moments.push_delivered` (Boolean NOT NULL default True), written only on a confirmed token + non-raising send. Reader now returns SENT rows only when `push_delivered is False`; SENT-before-PENDING ordering removed in favour of strict `scheduled_at` FIFO. Docstrings that documented the old intentional behaviour were updated to explain the reversal.
- Bug found and fixed while wiring CS-20: `mark_moment_push_delivered`'s commit expired an ORM object a caller still held past session close (`DetachedInstanceError`) – fixed by scoping `expire_on_commit=False` to that commit only.
- **RAG regression closed**: weekly/monthly indexers now prefer `summary_sections`, falling back to the legacy encrypted columns for historical rows.
- Verification: `import app.main` clean; **Postgres DDL compiles cleanly for both changed models** (new offline test – SQLite green is not sufficient evidence per CLAUDE.md); 16+ targeted suites run; **0 net new failures**, confirmed by `git stash` A/B against the 7 pre-existing baseline failures in those files.

### ⚠⚠ DEPLOY ORDER – READ BEFORE SHIPPING
Two new migrations, chain verified single-head: `ii0j1k2l3m4n` → **`jj1k2l3m4n5o`** (push_delivered) → **`kk2l3m4n5o6p`** (weekly uniqueness) = **NEW HEAD**.
- `notification_moments` is a **LIVE PROD TABLE**. `jj1k2l3m4n5o` MUST run together with the deploy or every read of that table 500s on `UndefinedColumn`. Heroku has no release phase – migrations are manual.
- `kk2l3m4n5o6p` is idempotent and **detects duplicate `(user_id, data_window_end)` rows before attempting the constraint** – if any exist it logs a warning and skips rather than raising, so `alembic upgrade head` still completes. **`database-administrator` should audit prod for duplicates before this constraint can actually apply.**
- SQLite gets an equivalent unique index instead of an ALTER-added constraint, following this repo's own `ii9j0k1l2m3n` precedent.

## PHASE B – CS-23 frontend – DONE – 2026-08-14
- Commits: none (working tree). Files: `summary_generation_failed_exception.dart`, `weekly_summary_manager.dart`, `monthly_audit_manager.dart`, `therapy_tab_cubit.dart`, `therapy_tab_state.dart`, `therapy_tab_screen.dart`, `weekly_summary_widget.dart`, `monthly_audit_widget.dart`, all 7 ARBs + generated, 1 new + 4 extended test files.
- **THE ACTUAL "Generate Now does nothing" MECHANISM, finally pinned down:** a `no_period_yet` response fell through the existing `isSummaryGenerationFailedBody` check straight into `Model.fromJson()`, which threw a type error on the missing required fields. The cubit's generic catch swallowed that into a generic failure state **with a dead retry button** – and `can_retry` is always false for this outcome, so retrying could never work. Fixed with a dedicated `SummaryNoPeriodYetException` and a new `TherapyTabState.noPeriodYet` terminal state that renders an informative, non-error message with no retry button.
- **Unreachable empty copy fixed:** `_fetchStateForFilter`'s weekly/monthly branches hardcoded `hasItemsInOtherFilters: true`, so the screen always showed the generic "not found in this filter" text instead of `therapy_emptyWeeklyTitle` / `therapy_emptyMonthlyTitle`. Now `false`, scoped to weekly/monthly only.
- Case-insensitive `processingStatus` comparison in both card widgets (backend emits UPPERCASE).
- Bounded polling with backoff (`Timer`, 2–10s, ~10 attempts, cancelled on dispose) so a PROCESSING card resolves to COMPLETED/FAILED without user action.
- `therapy_periodSummaryWorkedOn` / `HowYouFelt` / `GotDone` translated (were English-only in de/es/fr/nb/pl/sv) plus two new `no_period_yet` keys, all 7 locales.
- Also fixed 4 pre-existing tests that leaked a poll `Timer`.
- `flutter analyze`: **129 issues / 0 errors**. **131 targeted tests green.**

## PHASE H1 – CS-17 / CS-19 / CS-20 / CS-21 frontend – DONE – 2026-08-14
- Commits: none (working tree). Files: `moments_cubit.dart`, `main_page_body.dart`, `moment_deep_link_screen.dart`, `insight_dispatcher.dart`, `ms_routes.dart`, `notification_moment_model.dart` (+codegen), 3 renderers, 5 test files.
- **CS-17 root cause + fix:** the pop-out queue lived in `MainPageBody.initState`, so any CTA doing `context.go` to another top-level route destroyed and rebuilt the widget → `initState` re-ran → the next pop-out fired on top of the screen the user had just opened. The queue now lives on `MomentsCubit`, a `lazySingleton` that survives that remount, gated by `tryStartMomentQueueDrain()` / `pauseMomentQueue()` / `resumeMomentQueue()`. "User navigated away" is detected via `mounted` after each `await` – a `context.go` disposes the State, a plain dismiss does not, so completed-vs-dismissed needs no extra bookkeeping. Resume is wired only to real user tab taps/swipes, which cannot self-trigger via go_router. All three root-cause vectors closed, including `moment_deep_link_screen.dart`'s trailing `context.go`.
- **CS-19/CS-21 dead routes:** added `MsRoutes.isRoutable()` (regex denylist for `/stats`, `/stats/symptoms/{id}`, `/stats/symptoms/{id}/history`, `/character/streaks`, defaulting to routable so go_router's errorBuilder stays the last-resort net). When a CTA is unroutable, label AND handler are BOTH nulled so no button renders at all. Applied to the inline-banner and bottom-sheet branches, the generic moment sheet, and – after a follow-up – the three live toast/banner renderers.
- **CS-20 guard:** `shouldAutoShowMomentSheet(moment) => moment.status != MomentStatus.sent`. A SENT moment is skipped for auto-popup without being consumed. Mechanism fully intact.
- **Two corrections to the lead's brief, both verified:** (a) `recordBottomSheetShown()` IS called – by `pattern_insight_sheet.dart` and `recovery_moment_sheet.dart`, which are themselves unreachable dead code; (b) it was **10** missing `MomentType` values, not 9 – `MOOD_UPDATE_REQUEST` had been missing since an earlier batch. All 10 added, codegen verified.
- `_dispatchByType` has no `default:` (exhaustive switch), so explicit cases were added for all 10 – deliberately case-by-case so a future backend addition forces a compile-time decision.
- All 14 backend `MOMENT_ROUTES` confirmed routable.
- Deliberate non-fix, flagged: `canShowContent()` remains a documented no-op from a prior decision (MED-03). The new gate supersedes it. Judged lower-risk than unilaterally reverting a previous team call.
- Newly documented dead code (NOT deleted, out of scope): `pattern_insight_sheet.dart`, `recovery_moment_sheet.dart`, `notice_banner_renderer.dart`.
- Tests: 145 passed / 0 failed across 10 targeted files. `flutter analyze`: 131 issues / 0 errors (below the 134 baseline).

## PHASE E – CS-04…CS-09 + CS-16 output cards – DONE – 2026-08-14
- Commits: none (working tree). Files: `prep_card_widget.dart`, `session_card_widget.dart`, `recording_summary_widget.dart`, `between_session_note_widget.dart`, `realization_detail_widget.dart`, `realization_badge.dart`, 7 ARBs + generated, 4 updated + 1 new test file.
- **CS-04**: inner `oceanMist` container removed; children splice into the outer Column via the existing `_wrapSection()` spreads. The flagged risk at `debrief_capture_screen.dart:1002` (PrepCardWidget mounted WITHOUT the white outer wrapper) was checked directly: that screen's `Scaffold.backgroundColor` is itself `oceanMist`, so pre-change it was an invisible oceanMist-on-oceanMist double fill with a redundant outline. Post-change the scaffold shows through – **visually identical, not unstyled**. Verified by reading the Scaffold declaration, not assumed.
- **CS-05**: `oceanMist` → `mainWhite` on the outer content container only. Post-edit grep for `oceanMist` in the file returns zero. Accent blocks (Summary `primary[50]`, To-do `sandBeige`, thread pills, badges) untouched.
- **CS-06**: To-do header 16/12/w600/primary[600] → 18/14/w700/primary[700]/ls 0.3. The share-card duplicate already had the CORRECT sizing – the main render was brought up to match it, so no edit was needed there.
- **CS-07**: exactly three sections converted off `CollapsibleCardSection` (prep T&Q, After Therapy T&Q, After Therapy Realizations). The shared widget itself is untouched and still backs prep Patterns, monthly_audit ×2, weekly_summary ×2.
- **CS-08**, all six: pencil `Padding(4)+Icon(16)` → `Padding(16)+Icon(16)` = 48×48; cancel/save gap 8→16 plus header→list gap 8→16 while editing; `Icons.link` removed both as the read-only pill icon and as the editor toggle (`isContinuation` stays in the model and still drives the pill accent colour – only the interactive control went); circle-minus → `Icons.delete_outline` at `Padding(14)+Icon(20)` = 48×48 (agent initially shipped 44×44, caught it against the DONE_WHEN and fixed it); spacing before "+ Add thread"; ARB `capture_debriefAddTopic` "Add topic" → "+ Add thread" in all 7 locales, reusing the already-shipped translations from `workspace_threadAddGhostButton` rather than inventing new ones.
- **`_TopicChip` regression check passed**: only the `if (topic.isContinuation) [Icon, SizedBox]` block was removed. The `Flexible(child: Text(...))` no-maxLines/no-ellipsis multi-line wrap block (Fix 4 CS-01 / Fix 5 CS-01) is byte-for-byte untouched.
- **CS-09**: `oceanMist` → `mainWhite` on the card content container only; gold accents, detection badge, View Source and Remove Realization untouched.
- **CS-16 – shared-code removal handled correctly.** Removed from the three output cards: the `onLongPress` handlers, the badge render calls, `RealizationBadgesMixin`, `_loadRealizations()`, `_showUpsellDialog()` and now-dead imports. Deleted `RealizationIndicatorBadge` and `RealizationBadgesMixin` only after grep proved zero remaining references anywhere in `lib/`.
  - **Reflect survives, proven**: `reflect_chat_bubble.dart` untouched – still calls `showMarkAsRealizationSheet()` at `:141` and renders `RealizationBadge` at `:276` off its own local `_taggedRealization` field (it never used the mixin). `lib/utils/realization_actions.dart` left completely untouched, and the `RealizationBadge` class was deliberately KEPT.
  - `last_realization_widget.dart` untouched – it uses the raw `realizationGold` constant, never the badge widgets.
  - On Between Sessions, long-press was removed from the reference-only **Summary** block; the actual Realizations section is a separate flag-based block (`_buildBookmarkableBullet` / `triageBookmark`) and was not touched.
  - Flag path (`triage_bookmark_mixin.dart`) and all backend files untouched.
- `flutter analyze`: **131 issues / 0 errors** (below the 133/134 baseline), and it typechecks the new test files, so everything compiles.
- ⚠ **Tests written but NONE confirmed passing** – two `flutter test` invocations were killed after build-lock contention (`PathExistsException` on `NativeAssetsManifest.json` from concurrent Flutter processes). Must be verified centrally.

## PHASE F2 – CS-01 / CS-02 / CS-03 Main + trash – DONE – 2026-08-14
- Commits: none (working tree). Files: `main_tab_screen.dart`, `main_tab_cubit.dart`, `main_tab_state.dart`, `settings_body.dart`, `settings_cubit.dart`, `settings_state.dart`, `shared_preferences_manager.dart`, `preference_keys.dart`, `unified_symptom_module.dart`, `recently_deleted_screen.dart`, 7 ARBs + generated. DELETED: `main_tab_widgets_section.dart`, `main_tab_widget_config.dart` (+ freezed/g).
- CS-01: tune icon → shared 48×48 `Icons.info_outline` treatment, tapping opens `SectionInfoSheet` directly. `_TuneBottomSheet`/`_TuneAction`/`_EditModeBody`/`_EditModeRow` deleted. Cubit: `toggleEditMode`/`toggleWidgetVisibility`/`reorderWidgets`/`refreshWidgetConfig`/`sanitizeMainTabWidgetOrder`/`getCardLabels` deleted. State: `isEditMode`/`widgetOrder`/`hiddenWidgets` removed. **Settings duplicate removed too** (second entry point). Persistence + both pref keys removed. 4 dead l10n keys removed from all 7 locales.
- CS-02: `Icons.tune` 18px → `Icons.edit_outlined` 24px, same flow. Sole consumer is Main's Mood Trend (Stats no longer mounts the widget) – verified.
- CS-03: blanket `Opacity(0.55)` card wrapper removed. Secondary chrome colours (badge / timestamp / preview / expiry) deliberately left – they are the same muted tokens used elsewhere, not part of an "inactive" treatment.
- Tests: updated `main_tab_cubit_test`, `main_tab_widget_order_no_goals_card_test`, `main_tab_cubit_session_refresh_test`, `main_tab_cubit_next_session_test`, `getting_started_card_test`; NEW `home_hero_greeting_info_button_test`, CS-02 pencil tests, CS-03 opacity test.
- `flutter analyze`: 134 issues / 0 errors = exactly baseline, no new issues. Codegen regenerated cleanly.
- ⚠ Users with a saved custom module order now see the default order – intended, spec-flagged for veto.

## PHASE I1 – CS-22 Share – DONE – 2026-08-14
- Commits: none (working tree). Files: `card_share_util.dart`, `share_card_config.dart`, `pubspec.yaml` (+lock, 1 line), NEW `test/utils/card_share_util_test.dart`, comment-only fix in `prep_card_share_content_test.dart`. `branded_share_wrapper.dart` NOT modified – no change was needed there.
- **Root cause:** `captureFromWidget` was never passed `targetSize`, so the offscreen RenderView was capped at one device screen (`screenshot-3.0.0/lib/screenshot.dart:151-167`), and the `SingleChildScrollView` in the capture root let taller content scroll out of frame instead of forcing layout to grow.
- **Fix:** switched to `captureFromLongWidget`, which measures the widget's natural intrinsic size under unbounded height and captures exactly that. The capture root had to drop `MaterialApp`/`Scaffold` (their `Navigator`/`Overlay` sizes to `constraints.biggest` and throws under unbounded height) in favour of `MediaQuery > Localizations > Directionality > Theme > Material > BrandedShareWrapper`. Effective ancestor chain for content is unchanged since `Scaffold` internally wraps its body in a `Material`.
- **Format PNG → JPEG** per spec: decode PNG, re-encode `encodeJpg(quality: 92)`, write `.jpg`, `XFile(mimeType: 'image/jpeg')`. `image` was already resolved transitively at 4.6.0; promoted to a direct dependency in `pubspec.yaml` (no version bump, 1 lock line). JPEG alpha flattening is handled by the encoder + the wrapper's opaque background.
- Personal-bio 9:16 preserved with no special-casing – `wrapperMinHeight: 640` flows into the measurement pass.
- Removed as genuinely dead (grep-proven, zero call sites): `CardShareUtil.shareCardAsImage`, `ShareCardConfig.symptomTracking/goalTracking/snapshot`.
- Public signature `shareWithBranding({content, config})` unchanged – all 9 share sites compile untouched.
- `flutter analyze`: **133 issues / 0 errors** (one self-introduced `unnecessary_import` was caught and fixed). Test file written; full-suite numbers pending central run.

## PHASE G1 – CS-14 / CS-15 Workspace Threads – DONE – 2026-08-14
- Commits: none (working tree). Files: `thread_card.dart` (rewrite), `workspace_item_menu.dart` (additive), `threads_module_section.dart`, `threads_full_screen.dart` (comment), 1 rewritten + 2 new test files.
- CS-14: `_HubAndSpoke` / `_SourcePill` / `_HubLinesPainter` and their call site deleted. All were library-private → grep-proven zero cross-file refs. Context text kept and improved (full paragraph, no longer a truncated snippet). Backend source attribution untouched; `getThreadDetail` still used by the out-of-scope detail screen.
- CS-15: row = status dot → pin icon → title (20/w700/ls −0.2/workspaceInk) → status chip → 3-dot menu, then full context paragraph (14/h1.55/abyssBlack). Shell copied 1:1 from Goals (padding 16, mainWhite, lagoonBlue border, radius 16). Chevron, expansion, `_expanded`/`_toggleExpanded`/`_collapse`, and the swipe-collapse all removed.
- **Deviation by necessity (approved by lead):** Goals has no row menu, so the 3-dot sits in the trailing slot Goals uses for its chevron.
- Status dot + status chip KEPT (guardrail: thread statuses must survive). The old one-line `contextSnippet · statusLabel` micro-line was dropped as superseded by the real context paragraph.
- `WorkspaceItemMenu` extended with OPTIONAL `agendaAdded` + `onMarkDone`, both defaulting to no-op – 6 existing callers verified byte-identical. "Mark as done" reuses the existing `workspace_threadClose` key (already translated in all 7 locales) rather than adding new ARB entries.
- `initialVisible: 3` in the module (was implicitly 5). `threads_full_screen.dart` deliberately left uncapped – it IS the "see the rest" destination. Newest-on-top (Fix 2 CS-05) reconfirmed unchanged, regression test retained.
- ⚠ `workspace_threadDeleteTooltip` is now an unused l10n key – left in place, flagged for a future cleanup pass.
- ⚠ **Tests written but NOT run** (analyzer/build-lock contention with concurrent agents). Must be verified centrally: `thread_card_test.dart` (new), `workspace_item_menu_test.dart` (new), `threads_module_section_test.dart` (rewritten).

## PHASE F1 – CS-10 recording duration – DONE – 2026-08-14
- Commits: none (working tree only, per batch convention).
- Files: `MindSync/app/tasks/session_recording.py` (+68/−3), `MindSync/app/tests/test_recording_duration_fix.py` (new, 10 tests).
- **Root cause confirmed:** `process_session_recording_whisper` estimated duration as `len(audio_bytes) // 2000`, a compressed-m4a byte rate. The recording_pipeline_v2 chunked upload actually delivers uncompressed WAV at 16 kHz/16-bit/mono = 32000 B/s → exactly 16× inflation. 206 min ÷ 16 ≈ 12.9 min, matching the reported ~11–12 min recording.
- **Worse than the ticket said:** the chunked-upload `/complete` endpoint enqueues `process_session_recording_whisper` as the ONLY processing path for that flow. So this fired on essentially every completed "Record Session" recording since recording_pipeline_v2 shipped (~2026-06-22), not just on AssemblyAI-failure fallbacks. The AssemblyAI path was never affected (it reads `audio_duration` from the API result).
- **Fix:** new `_estimate_recording_duration_seconds(audio_bytes, content_type)` – parses the real WAV header via the existing `wav_chunker._parse_wav_header` and computes `data_size / (sample_rate × channels × bytes_per_sample)`; falls back to a compressed-audio byte rate only for non-WAV/unparseable input. The `max(estimated, 60)` floor was dropped (it silently inflated sub-minute recordings).
- Impact recon: all `duration_seconds` consumers pass the int through unchanged in SECONDS (crud.py:3993, crud.py:4445, schemas.py:1094, schemas.py:1537) – no unit or contract change. NOT boot-critical (module is only imported lazily inside function bodies; `app/main.py` never references it). No model/DDL/enum change.
- debriefs/between_sessions/prep_cards `_estimate_audio_duration_seconds` (16 KB/s): investigated, **NOT the same bug**, left untouched – those endpoints are always-m4a, never receive WAV, and the value is ephemeral (an AI prompting threshold), never persisted and never returned to the client.
- Tests: new file 10/10 pass; verified as real regression tests by stashing the fix – 9/10 then fail. Targeted suite (9 files incl. test_timeline, test_session_recordings, test_chunked_upload): **348 passed, 0 failed, 0 regressions**.
- ⚠ **Existing bad data – operator decision needed.** Rows already written carry the 16× value. Raw audio is deleted as a privacy cleanup once a recording reaches COMPLETED, so recompute-from-audio is not viable. `transcript_text` IS retained, so a word-count/WPM re-estimate is possible and cheap. Recommend `database-administrator` gets an affected-row count on prod, then a one-off decrypt+recompute+UPDATE after operator sign-off. NOT run, NOT scripted.
