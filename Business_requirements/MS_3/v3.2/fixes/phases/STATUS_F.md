# PHASE F — full report (F1 triage chips · F2 notification deep-links · F3 Timeline summaries) — 2026-07-17

Executed as 3 parallel worktree agents + 1 integration agent (per STATUS.md NEXT STEPS / operator feedback on task sizing).
All work committed locally on `mindsync-frontend` branch **dev**; NOT pushed. Base was Phase E `67a932d`.

## Final dev history (local, ahead of origin/dev by 10)

```
019031b  merge F3 — MSV3.2Fix.1 F: integrate F1 triage chips + F2 notification deep-links + F3 Timeline summaries
3e5e939  merge F1
e57e713  merge F2
087e8f7  MSV3.2Fix.1 F3: Timeline weekly/monthly summary in-card error state + retry (1.1 CS-21)
14fda1a  MSV3.2Fix.1 F1: Triage chips redesign (CS-03 + CS-10)
03c8f49  MSV3.2Fix.1 F2: notification deep-links (1.1 CS-06)
67a932d  (Phase E — base)
```

Worktrees `.worktrees/f1|f2|f3` removed, slice branches deleted after merge.

---

## F1 — Triage chips (1.2 CS-03 + CS-10; supersedes 1.1 CS-07 mechanics) — commit `14fda1a`

- `lib/widgets/triage_section.dart` rewritten: bookmark rows + batch buffer („Save to Workspace · N", confirmation bar, Undo) **removed**; chips grouped in fixed order **Tematy · Pytania · Wątki · Action pointy · Odkrycie** (Odkrycie last per master-plan decision 2). Group header only when non-empty; whole section hidden when no proposals.
- Every chip starts UNSELECTED; tap → single shared `POST /triage/{id}/toggle`; rendered state always comes from the server's `chip_state` (3 states: unselected / selected / closed). Closed chip = muted+strikethrough with `Icons.replay`; tap restores to the module's active list. Unselected chips persist forever; Timeline reopen of old cards fully triage-able. `suggested_thread_id` renders as hint under the chip.
- Host card widgets NOT edited — `TriageSection` constructor signature unchanged, all 4 embed sites (session_card, prep_card, between_session_note, recording_summary + card detail) verified passing correct `cardType`.
- Per-kind module refresh after toggle: topic/question → `TopicsCubit.load()`, action_point → `TodoCubit.loadActive()`, thread → `ThreadsCubit.loadActive()`, realization_ref → `RealizationsRepoCubit.load()`; all guarded by `GetIt.isRegistered` (graceful degradation).
- **Deliberate deviation (Phase G audit):** NO `AgendaCubit.loadActive()` on chip tap — none of the 4 toggle outcomes touches an Agenda row directly (pinning happens in the modules), so it would be a wasted call. Old `getTriageProposals`/`submitTriage` manager methods left in place (back-compat), no longer called.
- Contract §2 (API_CONTRACT_Fix1_A1.md) verified against backend schemas/endpoints directly — **zero mismatches**.
- l10n: `triage_groupThreads`, `triage_destThreads`, `triage_destTopicsQuestions`, `triage_chipClosedHint` ×7 locales (PL translated, rest EN); gen-l10n committed.
- Tests: rewritten `test/widgets/triage_section_test.dart` 16/16; full suite 1125/30 = baseline; analyze 0 errors.

## F2 — Notification deep-links (1.1 CS-06) — commit `03c8f49`

- Audit vs contract §9 (API_CONTRACT_Fix1_A2.md): existing infra already correct for nearly everything — all 11 live moment types always carry `route: "/moment/{id}"`; `MomentDeepLinkScreen` dispatches per type; cold-start/background/foreground all funnel through `resolveNotificationRoute`.
- **The one real gap fixed:** `session_recording_ready` push now routes to the exact card — new `recordingRouteFromData()` + GoRoute `/therapy/recording/:id` (reuses `TherapyCardDetailScreen.fromTimelineItem(type:'recording')` + `RecordingManager.getRecording()`); missing/garbage `recording_id` (legacy payloads) → safe fallback to Timeline tab (prior behavior).
- `admin_broadcast`: passthrough of operator-supplied `route`, else default. Dead paths `summary_ready`, `post_session_nudge(_followup)` confirmed unreachable (A2 audit), FE handling kept inert. Phase C reminder-„open" flow verified untouched.
- Tests: resolver unit tests cover every §9 type (valid/missing/garbage payload + legacy `deep_link_route`), 55/55 targeted; full suite 30 fail = baseline; analyze 0. No l10n changes.
- **Manual device-QA matrix (type × app state)** — for Phase G:
  - 11 moment types × {cold-start, backgrounded, foreground-banner-tap, local-notif-tap} → `/moment/{id}` → type renderer / generic sheet.
  - `session_recording` + `recording_id` × same 4 states → `/therapy/recording/{id}` (exact card).
  - `session_recording` without/garbage `recording_id` → Timeline tab fallback.
  - `admin_broadcast` with/without `route`.
  - QA note: verify the new recording deep-link against a REAL push once backend A2's `recording_id` is live in prod payloads.

## F3 — Timeline weekly/monthly summaries UI (1.1 CS-21 FE) — commit `087e8f7`

- Failure → in-card ERROR STATE (friendly, localized, mapped from `error_code`) with retry via „Generate Now" — both for the empty-state CTA and an already-visible FAILED card (`_SummaryRetryFailedRow`). Never a raw 500/exception toast.
- New `lib/api/api_exception.dart` + `dio_client.dart`: `ApiException` preserves raw response body so cubits can read the A2 error envelope `{"detail": {error_code, retryable, summary_id|audit_id}}`; additive, `toString()` unchanged (existing `.contains('404')` checks unaffected).
- **Correctness finding (traced in BE, read-only):** `POST /generate` after a failed row is NOT idempotent (new window → duplicate row). Cubit therefore smart-routes to `POST /retry/{id}` whenever `retryRowId` is known. Also noted asymmetry: FAILED `monthly_audits` are excluded from timeline listing while FAILED weeklies are not — retry-on-visible-card path reachable only for weekly today; handled symmetrically anyway.
- Auto-generated per-period cards: audited only — BE cron + existing Loaded rendering already handle it, no FE change needed.
- Own widget test caught a pre-commit bug: banner was gated on `error_code != null`, hiding it for network/unrecognized errors → separate `isGenerateFailed` bool.
- l10n: `therapy_summaryGenerationFailedError`, `therapy_summaryPrepareFailedError`, `therapy_summaryGenericGenerationError`, `therapy_retryingGeneration`, `therapy_summaryCardRetryFailed` ×7 locales; gen-l10n committed.
- Tests: 16 cubit + 6 widget tests; full suite 1142/30 = baseline; analyze 0 errors.

## Integration — merges `e57e713`, `3e5e939`, `019031b`

- Merge order F2 → F1 → F3. Zero manual conflicts — git 3-way auto-merged the 7 ARBs + 8 generated l10n files (non-overlapping append positions); `flutter gen-l10n` validation pass produced **zero diff** vs the auto-merge (byte-identical ⇒ correct).
- All 9 new l10n keys verified present in all 7 ARBs. build_runner sanity run → only CRLF churn on 3 generated files (no real diff, reverted). analyze 0 errors.
- Full suite post-merge: **1161 pass / 30 fail = exact baseline**; verified all 30 failures are the pre-existing set (privacy_data_section, onboarding_lead_source_wave4, wow_screen_adaptive_cta, reflect_* , save_feedback_indicator, therapy_frequency_selector) — none touch F1/F2/F3 files. **No cross-slice interaction.**

## Known Windows gotcha (for future sessions)

`build_runner`/`flutter test` on Windows rewrites 200+ unrelated generated files as pure LF/CRLF churn (`core.autocrlf`). Check with `git diff --ignore-all-space --stat`; if no real diff → `git checkout -- <path>`. Never stage the churn.

## Device-QA consolidated list (Phase G input)

1. F1: chips on all 4 card types (section at bottom, body untouched); each chip kind creates its item in the right module instantly; second tap withdraws; close-in-module → closed chip → tap restores; old Timeline card reopen keeps states; airplane-mode mid-tap → toast + revert; narrow-device wrap (iPhone SE).
   - Note: `thread`-kind chips need data-analytics to actually emit thread proposals (known gap flagged in STATUS_A1/E).
2. F2: full type × app-state matrix above; recording deep-link against real prod push.
3. F3: weekly + monthly Generate Now failure → banner + retry (no crash/toast); FAILED weekly card shows in-card retry that doesn't also navigate to detail; cron-generated cards render alongside manual ones; PL spot-check of 5 new strings.

## Deploy notes

FE-only phase, but chips + module routing REQUIRE backend A1 migration `aa2b3c4d5e6f` (+ A3 `bb3c4d5e6f70` = Alembic HEAD) applied WITH the backend deploy; summaries error envelope + `/retry` require A2 code (`c878e9f`). Nothing pushed anywhere; operator pushes BE+FE and runs `alembic upgrade head` after Phase G per master plan.
