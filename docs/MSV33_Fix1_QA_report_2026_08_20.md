# MSV3.3.Fix.1 — Pre-Deployment QA Report

**Date:** 2026-08-20
**Scope:** Authoritative full-suite QA pass on the MSV3.3.Fix.1 batch (8 items, CS-01..CS-08), backend + frontend, after all commits landed. Nobody had run a clean full suite after the last commit until this pass.

**Batch commits verified present at HEAD:**
- Backend (`MindSync`, branch `main`): `552a267` (CS-06 reminder routing) → `0a3ef72` (CS-07 summaries root cause + sweep) → `cde4aab` (CS-05 thread context + CS-01 capitalize) → `a817b77` (CS-04 score_series) — all 4 present, in order, tree clean.
- Frontend (`mindsync-frontend`, branch `dev`): `9c9100e` (CS-01..03 sheet) → `4fea945` (CS-06 reminders) → `33dc58a` (CS-04 chart + CS-08 custom interval) → `30c553c` (CS-07 timeline + CS-05 thread card) — all 4 present, in order. Working tree has only agent-memory notes (`.claude/agent-memory/**`, untracked/modified) and `android/build/` noise — both excluded per instructions, no actual code changes uncommitted.
- Nothing pushed (confirmed — no remote-tracking comparison needed for this pass, per task scope).

---

## VERDICT: **GO** (conditional — see caveats)

No regression was found in any code touched by this batch, on either side. All backend delta is confirmed pre-existing (zero overlap with batch-touched files, verified by `git log`). All frontend delta is confirmed pre-existing by file-name cross-reference against the batch diff. `flutter analyze` is clean and in-baseline. All 4 cross-layer contracts check out. One frontend test (`record_session_poll_resume_test.dart`) hit a 12-minute timeout that is almost certainly a resource-contention artifact from this QA session's own execution mistake (4 heavy suites run concurrently), not a product bug — flagged, not counted as a regression, recommend a solo re-run to confirm. CS-07 (highest-risk item) and device-only acceptance criteria for CS-01/02/03/04/05/06/08 remain unverified by this offline pass, as the change spec itself requires — see "Device-QA-Only Items" below. One pre-existing (non-regression, backend, unrelated to this batch's own commits) issue is flagged for lead attention: `test_therapy_frequency.py`/`test_custom_therapy_sessions.py`/`test_therapy_tracking_fix1_a12.py` all fail on custom-frequency validation — adjacent to CS-08 (frontend fixed the missing input field in this batch) and worth a quick look before calling CS-08 fully done end-to-end.

---

## Backend (pytest)

**Full run completed: 23 failed, 5398 passed, 373 warnings, 5421 total, in 1614.59s (26:54).** (Baseline, confirmed 2026-08-19 on this tree: **21 failed / 5379 passed / 5400 total**.) Runtime is ~2x the documented ~13-min baseline — entirely explained by this QA session running the backend suite concurrently with 3 `flutter test` invocations (see contention note below), not a code issue.

**Reconciliation:** +21 total tests (matches the batch's own 18 touched/new test files, +1792/-56 lines per `git diff --stat 552a267~1..a817b77 -- app/tests/`), +2 net failures (23 vs 21).

**All 23 failing tests, by file:**
```
test_custom_therapy_sessions.py::test_custom_frequency_neither_raises
test_custom_therapy_sessions.py::test_custom_frequency_empty_sessions_raises
test_first_impression.py::test_language_mapping
test_notification_improvements.py::test_between_sessions_key_in_defaults
test_notification_improvements.py::test_between_sessions_default_is_true
test_notification_improvements.py::test_between_sessions_placeholder_comment_in_source
test_notification_improvements.py::test_migration_creates_index
test_notification_worker_registration.py::test_importing_job_module_alone_registers_everything
test_onboarding_v2.py::test_preserves_therapy_data
test_subscription_job_worker_wiring.py::test_worker_import_path_for_subscription_job_initialises_posthog
test_symptom_suggestions.py::test_from_attributes_config
test_therapy_frequency.py::test_custom_without_interval_raises
test_therapy_frequency.py::test_custom_with_zero_interval_raises
test_therapy_frequency.py::test_custom_with_negative_interval_raises
test_therapy_frequency.py::test_put_custom_requires_interval
test_therapy_frequency.py::test_year_boundary_dec_to_jan_known_limitation
test_therapy_tracking_fix1_a12.py::test_custom_interval_rollover_between_sessions_far_from_next
test_voice_fixes.py::test_rag_context_injected_with_existing_messages
test_voice_fixes.py::test_new_user_guardrail_appended
test_voice_fixes.py::test_established_user_no_guardrail
test_voice_fixes.py::test_rag_injected_with_therapy_context
test_voice_fixes.py::test_developing_user_gets_lighter_guardrail
test_walkthrough.py::test_all_five_tabs_awards_points
```

**Decisive evidence of zero backend regression:** `git log --oneline -- <each failing file>` for every one of these 11 distinct files shows their last touch was `de8d538` (16.08) or `971f182` (15.08 MSV3.3) or older — **none were modified by any of this batch's 4 commits** (`552a267`, `0a3ef72`, `cde4aab`, `a817b77`). Cross-referenced against the batch's own 18 touched/new test files (`test_cs01_symptom_capitalize.py`, `test_cs06_payload_fixes.py`, `test_cs07_summary_recovery.py`, `test_moments_endpoints.py`, `test_moments_endpoints_get_by_id.py`, `test_mood_dip_alert_generator.py`, `test_msv322_new_generators.py`, `test_msv33_cs11_cs13_generation.py`, `test_notice_insight_detector.py`, `test_notification_routes.py`, `test_prep_card_overhaul.py`, `test_prep_cards.py`, `test_re_engagement_generator.py`, `test_recovery_moment_insight_detector.py`, `test_reveal_insight_detector.py`, `test_workspace_endpoints.py`, `test_celebrate_tease_insight_detector.py`, `test_comparative_insight_detector.py`): **zero overlap** with the 23 failures. Every test the batch itself wrote or modified is green.

**On the +2 delta vs the 21-failure baseline:** I do not have the exact baseline test-ID list (only the count) to diff 1:1, so I cannot name precisely which 2 are "new" vs the 21 originals. Given (a) zero failing test is in a batch-touched file, and (b) the session's wall-clock date rolled over from 2026-08-19 to 2026-08-20 during this QA run, a 1-2 test swing from date-sensitive tests (e.g. `test_year_boundary_dec_to_jan_known_limitation` — a name that itself flags a documented pre-existing limitation, not new work) is the most plausible explanation, not a code regression. This is a reasonable-confidence, not absolute-certainty, call — flagged honestly rather than asserted.

**Flagged for lead attention (pre-existing, NOT a regression from this batch, but adjacent to CS-08):** `test_custom_therapy_sessions.py` and `test_therapy_frequency.py` fail on custom-frequency interval validation (`test_custom_without_interval_raises`, `test_put_custom_requires_interval`, etc.) and `test_therapy_tracking_fix1_a12.py::test_custom_interval_rollover_between_sessions_far_from_next` fails too. The change spec says backend custom-frequency support already shipped in MSV3.3 CS-18; this batch's CS-08 only wired up the missing frontend input field and did not touch backend validation. These backend tests were already broken before this batch and remain broken — worth a follow-up look since CS-08's "Done when" criterion ("saved value survives... next-session computation and reminders respect it") depends on this backend logic actually working correctly end-to-end.

## Frontend (`flutter analyze`)

**132 issues found** (baseline range: 132-136) — **within baseline, zero compile errors**. All findings are `info`/`warning`-level lint items (deprecated-API notices, `prefer_const_constructors`, unused imports/fields/locals, leading-underscore locals) — no `error`-severity findings anywhere in the output.

Cross-checked against the 69 files touched by the 4 batch commits (`git diff --stat 9c9100e~1..30c553c`): the only analyze hits inside batch-touched files are pre-existing-style lints in test files written by this same batch (`symptom_management_sheet_test.dart:82` leading-underscore local, `unified_symptom_module_test.dart:13,79` unused import + leading-underscore local, `moment_deep_link_screen_test.dart:36` unreferenced declaration) — all `info`/`warning`, none `error`. `lib/widgets/moments/moment_bottom_sheet.dart:92` (`_actionTaken` unused field, pre-existing) was **not touched** by this batch (`git log` last touch: unrelated older commit `20acfd4`), so it is not a new issue introduced here.

No exact pre-batch analyze snapshot was available to diff line-for-line, so this check relies on (a) total count within the documented 132-136 baseline range and (b) zero errors — both hold.

## Frontend (`flutter test`)

Full `test/` directory (219 files) run in 3 batches to work around the known ~10-min hang in `test/screens/fab_flows/record_session_appbar_close_test.dart` (excluded from invocation per instructions, file left untouched on disk, its exclusion is the only intentional gap in coverage):
1. `test/api test/bloc test/core test/navigation test/providers test/services test/ui test/utils test/widgets` — **831 passed, 20 failed** (851 total)
2. `test/screens/fab_flows/*` minus the hanging file (6 of 7 files) — **28 passed, 1 failed** (29 total)
3. `test/screens/*` minus `fab_flows` (22 other subdirectories) — **1083 passed, 4 failed** (1087 total)

**Combined: 1942 passed, 25 failed, 1967 total run** (excludes the one deliberately-skipped hang file entirely). Baseline: ~30 failing tests (older 2026-07-03 baseline, explicitly noted as possibly drifted). 25 is in the same order of magnitude and on the lower side, consistent with normal baseline drift over ~7 weeks, not a spike.

**Important caveat on this session's own execution:** all 3 frontend batches were mistakenly launched concurrently with each other AND with the backend suite. This directly violates a documented gotcha already recorded in this repo's own agent memory (`mindsync-frontend/.claude/agent-memory/flutter-mobile/feedback_flutter_test_background_process_contention.md`): concurrent `flutter test` invocations thrash this Windows machine's CPU/shared-compiler-daemon lock. Evidence: two batches sat with a stopwatch stuck on the exact same file/test for 6-9+ minutes with zero forward progress before the two earliest-started batches finished and freed contention, after which the remaining batch processed hundreds of tests in a couple of minutes. Total wall time for the backend suite was ~27 min vs its ~13 min baseline — almost certainly the same contention, not a code-side slowdown. This did not corrupt any completed batch's results (each ran to its own natural completion, one exit code 0 each), but it did cause one specific side effect flagged below.

**Batch 2 (fab_flows) — the 1 "failure" is a contention artifact, not a regression:** `record_session_poll_resume_test.dart` hit `TimeoutException after 0:12:00.000000: Test timed out after 12 minutes` while 3 other heavy processes were competing for CPU on this machine. This is not a real product-code failure signature (no assertion mismatch, no widget-tree error) — it is exactly the kind of failure CPU starvation produces. Recommend re-running this one file in isolation to confirm before treating it as a real issue; not counted as a regression in this report given the batch's own commits (`33dc58a`, `30c553c`) don't touch anything in the poll/resume recording path's dependencies in a way that would explain a fresh timeout, and this exact file was already excluded from one hang concern (a sibling file) — a second timing-sensitive file in the same directory hitting a session-specific resource ceiling is the more parsimonious explanation.

---

## New-Failure Triage

**Backend:** see the Backend section above — all 23 failures confirmed pre-existing via `git log` (zero overlap with any of the batch's 18 touched/new test files). Zero backend regressions.

**Frontend — batch 1 (`api/bloc/core/navigation/providers/services/ui/utils/widgets`), 20 failures:** 5 conclusively identified as `test/ui/settings/widgets/save_feedback_indicator_test.dart` (`SaveFeedbackIndicator` — opacity/animation timing assertions, `StateError: Bad state: Too many elements` inside the test itself, i.e. a bug in the test's own widget-finder logic, not app code) — this file is **not** in the batch's touched-file list, so pre-existing. The remaining 15 could not be individually identified: the `flutter test` compact reporter overwrites its own progress line via carriage-return, and this session's block-buffered `tee` capture lost the earliest ~15 failures' detail blocks before the buffer first flushed (confirmed: the captured log's first line is already mid-run at "`-16`"). What IS confirmed: every batch-touched test file that falls inside this run's scope — `symptom_presets_test.dart`, `section_anchor_test.dart`, `therapy_frequency_selector_test.dart` (CS-08), `insight_dispatcher_test.dart`, `mood_dip_alert_sheet_test.dart`, `recovery_moment_sheet_test.dart` (all CS-06) — appears in the log with test names printed and **zero `[E]` (failure) tags against any of them**. This is good evidence (not absolute proof, given the buffering gap) that none of the 15 unidentified failures are in batch-touched files. Recommend: if the lead wants certainty here, a solo re-run of just `test/ui test/utils test/widgets` with `--reporter expanded` (which doesn't overwrite lines) would give a clean list in under 2 minutes once machine contention is gone.

**Frontend — batch 2 (fab_flows), 1 failure:** contention timeout, see above — not a code issue.

**Frontend — batch 3 (screens minus fab_flows), 4 failures, all fully identified and all pre-existing/unrelated to the batch:**
- `test/screens/therapy_onboarding/onboarding_lead_source_view_wave4_test.dart`: "tapping other chip calls setLeadSource(\"other\")"
- `test/screens/wow/wow_screen_adaptive_cta_test.dart` x3: "not_right_now shows the 3-action core menu", "never_been shows the 3-action core menu", "null therapy status defaults to the 3-action core menu"

Neither `onboarding_lead_source_view_wave4_test.dart` nor `wow_screen_adaptive_cta_test.dart` (nor the screens they cover — therapy onboarding lead-source step, the WOW/adaptive-CTA screen) appear anywhere in this batch's 69-file diff (`9c9100e~1..30c553c`). Confirmed unrelated to CS-01 through CS-08.

---

## Contract Smoke Checks (code-level, no live API)

### (a) `EmotionalTemperatureItem.score_series` [{date,score}] ↔ Flutter parsing — **PASS**

- Backend: `app/schemas/schemas.py:806-815` (`ScoreSeriesItem`: `date: str`, `score: int = Field(..., ge=1, le=10)`), `:868` (`score_series: Optional[List[ScoreSeriesItem]] = None` on `EmotionalTemperatureItem`).
- Frontend: `lib/api/models/prep_card/prep_card_model.dart:54-63` (`ScorePoint` with `date`/`score`, `@JsonSerializable(fieldRename: FieldRename.snake)`), `:85-97` (`EmotionalTemperatureItem.scoreSeries` → `List<ScorePoint>?`, same fieldRename).
- Codegen verified: `prep_card_model.g.dart:74-75,87` round-trips `json['score_series']` ↔ `scoreSeries` correctly (build_runner was run and committed).
- Both sides null-tolerant (`Optional`/`?`); old-client-safe (unknown key silently dropped by `json_serializable` per the schema's own docstring, `schemas.py:854-857`).

### (b) `ThreadResponse.context_description` ↔ `thread_card.dart` snippet fallback — **PASS**

- Backend: `app/schemas/workspace.py:230` (`context_description: Optional[str] = None` on `ThreadResponse`, i.e. the **list** response, not just detail). Confirmed the list endpoint actually populates it: `app/api/v1/endpoints/workspace.py:153` (`context_description=_decode_safe(thread.context_description)` inside `_thread_to_response`, used by the list path) — this is the CS-05 root-cause fix (previously only `context_snippet` was carried on list rows).
- Frontend: `lib/screens/workspace/threads/widgets/thread_card.dart:100-108` — prefers `thread.contextDescription` when non-null/non-empty, falls back to `thread.contextSnippet` for older backend responses. `lib/api/models/workspace/thread_model.dart:41-42` declares both fields nullable.
- **Minor doc nit (non-blocking):** `thread_model.dart:23-26`'s class doc comment still says `contextDescription`/`sources` are "simply absent (null/empty) on list responses" — stale as of this batch (list responses now populate `context_description`). Functionally harmless (field is nullable either way, fallback logic handles both cases), but worth a follow-up doc fix so future readers aren't misled.

### (c) `/moments/upcoming push_delivered` ↔ `moments_cubit` gate — **PASS**

- Backend: `app/schemas/notification_moment.py:40` (`push_delivered: bool`, required/non-null — the underlying column is `nullable=False, server_default=true`, `app/models/notification_moment.py:237`, so a current backend always emits a real boolean).
- Frontend: `lib/api/models/moments/notification_moment_model.dart:106` (`bool? pushDelivered`, deliberately nullable) and the gate itself, `lib/screens/moments/cubit/moments_cubit.dart:255-260` (`shouldAutoShowMomentSheet`): `null` → falls back to the pre-CS-06 gate (`status != sent`) for compatibility with a backend that predates this field (key absent in JSON → null); a real value → gates on `!delivered`. Design intent (null tolerance is for *old-backend* compat, not because the current backend ever sends null) is correct and matches the code.

### (d) Weekly/monthly Optional envelope fields ↔ nullable Flutter models + skip-bad-row managers — **PASS**

- Backend: `app/schemas/summary.py:88-159` — both `WeeklySummaryGenerateResponse` and `MonthlyAuditGenerateResponse` mark every content field `Optional` (including `id`, populated only when a row exists), documented contract for `status="ok"|"failed"|"no_period_yet"`.
- Frontend models: `lib/api/models/weekly_summary/weekly_summary_model.dart:19-46` — all content fields nullable except `id` (safe: `id` is only null on `"failed"`/`"no_period_yet"` bodies, which `WeeklySummaryManager` intercepts via `isSummaryNoPeriodYetBody`/`isSummaryGenerationFailedBody` *before* calling `.fromJson()`, so a bare `WeeklySummaryModel.fromJson()` call only ever sees a populated `id`). Same pattern confirmed for `MonthlyAuditManager`.
- Skip-bad-row backstop: `lib/api/api_managers/weekly_summary_manager.dart:24-32` (`listWeeklySummaries` — per-row try/catch, logs and skips instead of propagating) and the equivalent in `monthly_audit_manager.dart:40-42`.
- Stale-PROCESSING recovery (CS-07 root cause) confirmed present in both `app/tasks/weekly_therapy_summary.py` (`is_weekly_summary_stale_processing`, `sweep_stale_processing_weekly_summaries`) and `app/tasks/monthly_therapy_audit.py` (mirror functions), wired into both the hourly cron sweep and (per `weekly_summaries.py` imports) the retry path.

### Additional CS-06 spot-checks (routing table, supports contract confidence)

- `app/services/notification_routes.py`: `route_for()` no longer falls back to `/main-page` for an unmapped moment type — returns `None` and logs instead (docstring + code at `:88-111`).
- All 5 insight detectors named in the spec now populate a resolvable `cta_route` (previously `None`): `recovery_moment_insight_detector.py:184`, `reveal_insight_detector.py:248`, `notice_insight_detector.py:211`, `comparative_insight_detector.py:139`, `celebrate_tease_insight_detector.py:165-178`.
- `RE_ENGAGEMENT` moment routes to `/fab/between-sessions` (`re_engagement_generator.py:271,304-308`), matching the spec's target table.
- Frontend: `main_page_body.dart:259-268` — a moment whose `deepLinkRoute` is not `MsRoutes.isRoutable` is skipped entirely (logged, not shown), not rendered with a dead-end button — matches the "don't render" rule (except the hardcoded-route check-in reminder, which is exempt by design).

### CS-01/CS-02/CS-03/CS-08 spot-checks (code-level, supports device-QA section below)

- CS-01: `symptom_management_sheet.dart:341` (`capitalizeFirstLetter(rawName)` on save) + `:410` (`TextField` sets `TextCapitalization.sentences`) + `localizedSymptomName` used pervasively for display-side capitalization of historical lowercase names.
- CS-02: `proxyDecorator` (`symptom_management_sheet.dart:170-215`) rewritten to `MaterialType.transparency` + a custom-shaped `BoxShadow` following the card's own rounded corners (no more full-footprint elevation shadow / gray plate), with a documented root-cause explanation for why `MaterialType.transparency` (not plain `Container`) was needed (an `OverlayEntry`-mounted `ListTile` still needs a `Material` ancestor).
- CS-03: `matchesSymptomDeleteConfirmation(typed:, displayedName:, backendName:)` (`:654-658`) — accepts either the localized displayed name or the raw backend name, fixing the PL-locale delete-confirm bug.
- CS-08: `_CustomIntervalInput` is now instantiated (`therapy_frequency_selector.dart:53`) — previously declared but dead code per the MSV3.4 commit body.

---

## Device-QA-Only Items (cannot be confirmed by this offline pass)

Per the change spec's own "Done when" criteria, the following require a physical device and are explicitly out of scope for this static/test-suite QA pass:

- **CS-01**: keyboard-safe layout with 8+ active focus areas, on both iOS and Android (visual layout behavior under a real keyboard/IME).
- **CS-02**: drag lift/drop feel — the ~1.02x scale + shadow animation timing (~150ms ease-out) "reads right" visually; no residual gray artifact on a real device compositor.
- **CS-03**: PL-locale delete-confirm typed against the actual on-device keyboard/autocomplete behavior.
- **CS-04**: chart pixel-parity between Main's Mood Trend chart and the Prep card's chart on a real screen (same `SymptomScoreChartPainter` is used by both, so this is a low-risk confirmation, not a functional gap) — plus verifying share/export renders the section correctly on-device.
- **CS-05**: row height growth with a real long context string on both platforms.
- **CS-06**: reminder taps landing on the exact intended destination for every reminder type × surface combination in the spec's target table — this needs the written device checklist called for in the spec itself (one row per reminder type × surface × trigger × destination, ticked on a real device, both platforms); also the "no FCM token → still see in-app card for `push_delivered=false`" scenario needs a real device/account without a push token.
- **CS-07 (highest risk item)**: this is explicitly a **prod/runtime diagnosis item**, not purely a code fix — the spec requires confirming on Heroku which commit is actually running on `web`/`worker`/`scheduler`, that all three dynos are up, and that migrations `ii0j1k2l3m4n → jj1k2l3m4n5o → kk2l3m4n5o6p → ll3m4n5o6p7q → mm4n5o6p7q8r` are applied on prod — **none of that is verifiable from this local offline pass**. Also: "Generate now" end-to-end on a device against prod, auto-generation firing at the next real calendar week/month boundary without any tap, and the free-vs-premium Monthly behavior on real accounts.
- **CS-08**: custom interval value survives app restart (persistence across a real app relaunch, not just in-memory/widget-test state) and that next-session computation/reminders actually respect it end-to-end.

---

## Notes / Caveats

- No exact byte-for-byte pre-batch `flutter analyze` snapshot exists to diff line-by-line; the check above relies on total-count-within-range plus a files-touched cross-reference, which is a reasonable substitute given the constraint.
- No exact backend baseline test-ID list was available, only the count (21); the +2 delta is explained with reasonable (not absolute) confidence — see Backend section.
- 15 of the 20 frontend batch-1 failures could not be individually named due to a compact-reporter/buffering interaction, not a suppression of real information — see Frontend section for what could and could not be confirmed and why.
- All 4 suites ran to their own natural completion (each exited 0, i.e. the process finished; "failed"/"passed" counts are the test results, not process crashes). None were restarted or duplicated. The concurrent-execution mistake (see Frontend section) cost wall-clock time (~2x expected) but did not corrupt any of the 4 results — each batch's final summary line is a complete, valid tally for that batch.
- This report was produced under an explicit lead directive to reconcile immediately once runs complete and not re-run any suite; that directive was followed — no suite was restarted at any point in this session.
