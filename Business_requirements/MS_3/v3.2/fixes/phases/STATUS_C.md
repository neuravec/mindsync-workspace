# MSV3.2 Fix.1 — PHASE C (FE Main) — STATUS

## PHASE C — Frontend: Main screen — DONE — 2026-07-17

- **Session commits** (repo `mindsync-frontend`, branch `dev`, **committed locally, NOT pushed**):
  - `914ddc3` — "MSV3.2Fix.1 C: Main screen (CS-08/09/10/11, FIX.03/04, reminder open)" — 35 files, +771 / −428. Single commit (all items share the ARB + generated-l10n files, so splitting would fragment those).
  - Runs on top of Phase B's `716f33b`.

- **Items completed (spec IDs):** CS-08, CS-09 (verified — see below), CS-10, CS-11 (a+c FE parts), FIX.03, FIX.04, 1.2 CS-01. All per their "Done when".

---

### CS-08 · Main order + iOS root cause + edit-mode/order semantics chosen
- The default order was already correct (`mainTabDefaultWidgetOrder` = next_session, homework_today, mood_trend, health_check_banner, weekly_observations, affirmation). Realizations (`last_realization`) and Goal (`treatment_goal_anchor`) were already OFF Main (not referenced by the card map) — nothing lost.
- **iOS root cause (found + fixed):** `sanitizeMainTabWidgetOrder()` kept ONLY the ids present in the user's saved SharedPreferences order. `homework_today` and `mood_trend` are NEW ids in this line-up; an **upgrading** user's saved layout predates them, so the old filter silently **dropped** both modules. That is why the previous batch "failed on iOS" — it was any device with a persisted layout, and the iOS testers happened to have one. (Not a platform-conditional bug; the fix is platform-agnostic.)
- **Chosen edit-mode/order semantics (documented as requested):** `sanitizeMainTabWidgetOrder` now RECONCILES a saved order against the canonical list:
  1. strips stale/removed ids (unchanged behavior — `goal_progress`, `symptom_trend`, `last_realization`, `treatment_goal_anchor`, …);
  2. **injects any canonical module missing from the saved order at its canonical (spec) position**;
  3. preserves the user's genuine reordering of modules they have already seen; hidden-widget choices (a separate `hiddenWidgets` set) are untouched.
  So: **default = spec order**; new modules always appear at their spec slot for every install (fresh AND upgrading); a user who reordered keeps their arrangement, but a module can never be *dropped*. This single function feeds both Main (`main_tab_cubit`) and Settings (`settings_cubit._buildWidgetConfigs`), so both surfaces get the new modules consistently.

### CS-09 · Next-session formats + state machine — verified, no code change (delta documented)
- The 4-state machine (empty / prep CTA / debrief CTA / between-sessions), both countdown formats (`>24h` day+time, `<24h` "dzisiaj o …, za x godz y min", `>=7d` legacy), the hub-and-spoke `SessionSetupScreen` (writes the SAME settings fields via `SettingsCubit.addTherapySession`/`addCustomSession`/`addTherapist`), and the two embedded bugs (debrief→between-sessions flip; next-session display with weekly cadence) were ALREADY implemented and tested by the prior MSV3.2 batch (`computeNextSessionAction`, `_computeNextSession`/`_computeLastSession`, `next_session_action_test.dart` covers all time edges: day boundary, session-start instant, debrief-match window, cadence rollover). I verified the logic and left it intact.
- **DELTA vs contract A1 §10 (`GET /therapy-tracking/session-state`) — documented, NOT reworked (per lead's guidance):** the FE sources CS-09 state **client-side** from the therapy schedule in SharedPreferences, recomputed fresh on every tab visit (`refreshTherapySchedule`). It does **not** read a stored `next_session_date`, so it is already immune to the stale-column bug the new endpoint was built to fix. I chose NOT to switch to the endpoint late in this pass because: (a) the client path already handles the listed embedded bugs and is fully tested; (b) `SettingsCubit` syncs the schedule to the backend only **fire-and-forget**, so consuming a BE-computed session-state would introduce a sync-race on the "set session → immediate reflection on Main" flow that the local read avoids; (c) it is a substantial rework (new model + manager + cubit rewire) that I cannot device-test.
  - **Known residual the endpoint would improve (fast-follow):** the client `debrief_cta` has no "schedule-created-at", so a brand-new recurring schedule whose last weekday occurrence is in the recent past can momentarily show a debrief CTA. The BE endpoint solves this with a narrow ~30h recency window. Recommend a follow-up to migrate `MainTabCubit`'s next-session STATE to `GET /therapy-tracking/session-state` (keeping the FE countdown formatting + cubit tests), with a client-side fall-through for the immediate-reflection case.

### CS-10 · Homework module — max 3 (was 2)
- Module already existed; the iOS gap was the CS-08 registration/ordering issue above (audited, confirmed). The card was NOT rebuilt.
- Reconciled `HomeworkTodayCubit.kMaxItems` **2 → 3** to match this Phase C spec ("Max 3 … the 3 OLDEST open items (FIFO)") AND contract A1 §4 (`GET /workspace/todos/today?limit=3`). An interim MSV3.2 build had trimmed it to 2 ("updated brief"); Fix.1.1 CS-10 restores 3. Updated the cubit + card doc comments and both tests.

### CS-11 · Mood Trend — score input + relative date (FE parts)
- **(a) Score input RESTORED** in the per-symptom expand panel (`unified_symptom_module.dart`): 1–10 slider + "Update rating" (reuses existing `stats_scoreLabel`/`stats_updateScore` keys) → `SymptomTrackingCubit.updateScore` → `SymptomManager.addScore` → `POST /api/v1/symptoms/{id}/scores`. This is exactly the "verify/wire tap-to-score against the pre-existing endpoint" action A2 §5 asked Phase C to do — **no backend gap found**, matching A2's code-trace conclusion.
- **(c) Relative "last scored" date** rendered small next to each symptom name (ICU plural key `stats_symptomLastScoredAgo`, all 7 locales: today / yesterday / "N dni temu" · "N days ago"). Sourced from the new backend `last_updated_at` field (reconciled — added `lastUpdatedAt` to `SymptomCardModel`), falling back to the newest entry in `scores` when the field is absent on an older backend build.
- (b) narrative content is Phase A backend work; FE just renders `ai_description` as before (unchanged).

### FIX.03 · AI Summary merged into Mood Trend box
- The AI summary is no longer a standalone card. It is passed into `UnifiedSymptomModule` via a new optional `header` slot and renders **inside the white symptom box, above the first symptom**, as a **bullet-free paragraph** (`data.bullets` joined into flowing prose, capped ≤5) with a small "AI SUMMARY" eyebrow + a divider. No summary yet → renders nothing (no nag).
- **Deleted outright** the "add an entry" / "it's been a while" staleness box (`needsUpdatePrompt` block) AND the empty-state text — grep-clean in PL+EN+5. Removed l10n keys `mainTab_moodTrendUpdatePrompt`, `mainTab_moodTrendUpdateButton`, `mainTab_moodTrendEmpty` from all 7 ARBs + regenerated. This matches A2 §5's explicit note that the staleness was a "FE-only box … slated for deletion, not relocation".

### FIX.04 · Weekly check-in dismissal
- **Root cause = FE (matches A2 §8 audit: no BE bug).** Main held a `latestHealthCheck` fetched at init and never refreshed after a check-in, so the session-anchored prompt gate (`therapyRelationshipPromptPending`) kept using stale data.
- Fix: new `MainTabCubit.refreshHealthCheck()` re-reads latest check-in (+status) and is called when the check-in flow **returns** — from the tab-visible listener, the `TherapyRelationshipPromptCard`, and the launch moment sheet. This is A2 §8's recommended path (b) "re-fetch right after submit succeeds; do not rely on a cached copy". The prompt then dismisses until the next cycle.

### 1.2 CS-01 · Reminder card dead "open"
- The launch reminder is the `THERAPY_RELATIONSHIP_CHECKIN` moment (backend `therapy_relationship_checkin_generator.py`, `deep_link_route "/health-check"`), surfaced via the generic `MomentBottomSheet` in `main_page_body._showMomentSheet`. The FE `MomentType` enum was **missing** that value (decoded to `unknown`), and the generic "open" relied on `moment.deepLinkRoute` (`context.go`), which no-ops when that value is empty/unresolved.
- Fix: added `MomentType.therapyRelationshipCheckin`; the sheet's "open" now **deterministically** `context.push(healthCheckFlowRoute)` (independent of `deepLinkRoute`) and marks the moment acted (dismissing the card), then refreshes Main's health-check on return. Trigger logic + other dismissal paths untouched. Also handled the new enum value in `moment_deep_link_screen.dart`'s exhaustive switch (push-tap surface routes via its `/health-check` deepLinkRoute, already correct).

---

## Backend gaps I seamed over (no invented endpoints)
- **CS-09 session-state:** used the existing client-side computation instead of `GET /therapy-tracking/session-state` (delta above). Clean seam — the widget already takes `dateTime`/`lastSessionDateTime`/`therapistName`/`action`, so a future migration only swaps the STATE source.
- **CS-11(c) `last_updated_at`:** model field added and consumed, with a `scores`-newest fallback for older backend builds (degrades gracefully).
- **FIX.04 `should_show_main_prompt`:** the NEW live-computed field (A2 §8) is NOT consumed. Main keeps the session-anchored `therapyRelationshipPromptPending` gate (CS-12's deliberate design — appears the day after a session, until a check-in is done — NOT the `is_due`/biweekly cadence `should_show_main_prompt` encodes). The dismissal bug is fixed by re-fetching `latestHealthCheck`, which the session-anchored gate already keys off. If product later wants cadence-based gating, switching to `should_show_main_prompt` is a small follow-up (add the field to `HealthCheckStatusModel` + gate on it) but changes WHEN the prompt appears — out of Phase C scope.

## API contract deviations
None introduced by the FE. All consumed endpoints match the contract as documented (`/symptoms/{id}/scores`, `/symptoms/` `last_updated_at`, `/dashboard/mood-trend`, `/health-check/status|latest`, `/workspace/todos/today?limit=3`, `THERAPY_RELATIONSHIP_CHECKIN` → `/health-check`).

## New migrations
None (FE-only phase).

## Test results (FE baseline 30 failures)
- Full `flutter test`: **1093 pass / 30 fail** → exactly the 30-failure baseline (0 new failures, 0 regressions; +net tests vs Phase B's 1090/30).
- `flutter analyze` on all touched files: **no new errors** (1 pre-existing `info` `_pt` local in the chart painter, untouched).
- Tests updated/added: `homework_today_cubit_test` (kMaxItems 3 + limit 3), `homework_today_card_test` (up-to-3), `main_tab_cubit_test` (reconciliation semantics + new `refreshHealthCheck` group), `main_tab_widget_order_no_goals_card_test` (reconciliation + iOS-root-cause case), `mood_trend_card_test` (rewritten for FIX.03 paragraph + deletions), `unified_symptom_module_test` (CS-11(a) score entry restored). CS-09 state-machine tests (`next_session_action_test`) unchanged and green.
- l10n completeness test green (key parity maintained across all 7 locales after the 3 removals + 1 addition).

## Manual QA still needed (device/platform — cannot be done in-session)
1. **CS-08 order on a real device with a pre-existing (older) saved layout** — confirm homework + mood-trend now appear at their spec positions on BOTH iOS and Android after upgrade (the reconciliation is the fix, but verify on a device that actually had the old layout).
2. **CS-11(a)** — set/change a symptom score from the Main Mood-Trend expand panel on device and confirm it persists (no "can't add score").
3. **CS-11(c)** — relative "last scored" date reads correctly (today/yesterday/N days) in PL + EN.
4. **FIX.03** — summary renders inside the box above symptom 1, ≤4–5 lines, no bullets; the old staleness box is gone in PL + EN.
5. **FIX.04** — complete a therapy-relationship check-in and confirm the Main prompt disappears on return (and stays gone until the next cycle). NOTE (A2 §8): if it still doesn't dismiss on device, suspect the CS-02 iOS voice bug for `submit-voice`/`quick-check-voice` (transcription failing before a COMPLETED row) rather than this fix.
6. **1.2 CS-01** — open the app with an overdue check-in; tap "open" on the launch reminder → lands in a fresh check-in AND the card dismisses. (Depends on the `THERAPY_RELATIONSHIP_CHECKIN` enum migration being applied on prod for the moment to be generated at all.)

## Notes for next phases
- **Phase D** will restyle the Workspace "Do zrobienia" UI over the **same todos repository** (`WorkspaceManager` / `/workspace/todos*`) that Main's Homework module (CS-10) reads via `/workspace/todos/today`. Single data source — no duplicate state; Main shows the 3 oldest open, the full backlog + repeats/archive UI belong to Phase D.
- `MomentType.therapyRelationshipCheckin` was added to the FE enum + both `MomentType` switches (`moment_deep_link_screen`, and the `==` check in `main_page_body`). Other FE phases touching moments can rely on it now.
- `UnifiedSymptomModule` gained an optional `header` slot (used by Main's Mood Trend); Stats/other callers pass nothing and are unaffected.
- `SymptomCardModel` gained `lastUpdatedAt` (nullable) — available for any other symptom consumer (e.g. the trend widget).
- Recommended fast-follow: migrate CS-09 next-session STATE to `GET /therapy-tracking/session-state` (see CS-09 delta) once someone can device-test the schedule sync timing.
