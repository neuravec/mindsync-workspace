# MSV3.2 Fix.1 — PHASE E (FE Workspace modules) — STATUS

## PHASE E — Frontend: Workspace modules — DONE — 2026-07-17

- **Session commit** (repo `mindsync-frontend`, branch `dev`, **committed locally, NOT pushed**):
  - `67a932d` — "MSV3.2Fix.1 E: Workspace modules (Wątki CS-14..18, Realizations CS-19/FIX.05, Goals CS-20..22, Therapy Relationship CS-23..25)" — 61 files. Single commit (all items share the ARB + generated l10n/freezed files, so splitting fragments those). Runs on top of Phase D `861a805`; dev now ahead of origin by 4 (B+C+D+E), NOT pushed.

- **Items completed (spec IDs):** Wątki 1.2 CS-14, CS-15, CS-16, CS-17, CS-18; Realizations 1.2 CS-19 + 1.1 FIX.05; Goals 1.2 CS-20, CS-21, CS-22; Therapy Relationship 1.2 CS-23, CS-24, CS-25. All per their "Done when".

---

### Items NOT completed / deviations + why
- **Wątki reopen-at-capacity 409** is no longer reachable from the landing module: closed threads leave the active list into the CS-15 archive (correct per CS-15), so the status chip never shows `closed` inline. The reopen/queue path stays exercised at the cubit level (`ThreadsCubit.cycleStatus`) and via archive restore. Deliberate; not a gap.
- **`ThreadsFullScreen`** kept + updated to the new `ThreadCard` API but no longer linked from the landing module (P3 inline replaces "see all"). Left routed for back-compat/deep-link. Harmless dead-ish screen.
- **CS-24 module icon** rendered as a small colour dot next to the "Kontrola terapii" section title (the module header is the only "outside the card" surface `HealthCheckSection` owns). Colour = latest check-in's `relationship_state`.
- **`GoalManager.deleteGoal` / `Endpoints.goalsArchive`** wired for A3 contract completeness. `deleteGoal` is NOT surfaced in the UI — no CS item in Phase E requires a delete affordance on goal cards (CS-20/21/22 are refresh/archive/add only); available for a future 3-dot menu.
- **Goals refresh (§7 async)**: `refreshAllNarratives()` sets a per-goal loading flag, calls `POST /goals/{id}/refresh` for each active goal, then re-lists after ~3 s to surface the async-regenerated narrative. On a **cache-hit** (unchanged data) the loading flag clears on that re-list even though the text is identical — a brief harmless spinner. Failure of a refresh call returns `false` → retry toast; the previous narrative is never overwritten (backend guarantee §7).

### API contract — followed; deviations / notes
- Wired strictly per `API_CONTRACT_Fix1_A1.md` §1/§3, `A2.md` §7/§8, `A3.md`. New FE model `PinToggleResponse {pinned, agendaItemId}` matches the CHANGED shape of `PUT /threads/{id}/add-to-agenda` (was `AgendaItemResponse`) and the NEW `PUT /realizations/{id}/agenda-pin` (§3c). `GoalModel.achievedAt` (additive), `GET /goals/archive`, `DELETE /goals/{id}` per A3.
- **No mismatches found** — every endpoint/field consumed was verified present in the A1/A2/A3 contracts before wiring. No STATUS-blocking discrepancies.
- The old `WorkspaceManager.addThreadToAgenda` (create-only, returned `AgendaItemModel`) was renamed to `toggleThreadAgendaPin` (returns `PinToggleResponse`). Its only other caller, `ThreadDetailCubit.addToAgenda` (deep-link detail screen), was updated to the toggle shape.

### New migrations
- None (FE-only). Backend for this slice is A1 (`aa2b3c4d5e6f`) + A3 (`bb3c4d5e6f70` = HEAD), neither applied on prod — see below.

### CS-25 contrast ratio (computed)
- Background = `MsColors.aquaBreeze` `#DBF0ED` (relative luminance ≈ 0.835).
- P3 control text darkened to `MsColors.primary[700]` `#225E63` (luminance ≈ 0.092).
- **Contrast ratio = (0.835 + 0.05) / (0.092 + 0.05) ≈ 6.2 : 1** → passes WCAG AA (≥4.5:1) and AAA for normal text.
- For reference, the shared P3 default `primary[600]` `#26767B` on aqua-breeze is ≈ **4.47 : 1** (just below AA) — which is why CS-25 passes `controlColor: primary[700]` via the new optional param rather than forking the widget. `primary[600]` stays the default on the white/oceanMist modules (Wątki P3 on `mainWhite` ≈ 5.3 : 1, fine).

### safety_escalation colour decision
- `HealthCheckModel.relationship_state` = `green | amber | red | safety_escalation`. Colour comes from the existing shared `healthCheckStateColor()` (unchanged, per CS-24 "do not touch the scoring/colour logic"): green `#4CAF50`, amber `#FF9800` (the spec's "yellow"), red `#F44336`.
- **`safety_escalation` → red `#F44336`** (same colour value as `red`, per the phase brief default), BUT differentiated by a **distinct icon**: plain `red` uses `Icons.priority_high`, `safety_escalation` uses `Icons.warning_amber_rounded` — so it reads as the most urgent state without conflating it with a plain red rating (per `API_CONTRACT_Fix1_A2.md` §8 guidance).

### Test results (before → after vs baseline 30 FE)
- Full `flutter test`: **1125 pass / 30 fail** = exactly the 30-failure pre-existing baseline (0 new failures, 0 regressions; +5 net new passing vs Phase D's 1120/30).
- Isolated `flutter test test/screens/workspace test/screens/stats_tab`: **110 pass / 0 fail**. None of the 30 baseline failures are in any Phase-E-touched area.
- `flutter analyze lib test`: **0 errors** (remaining items are pre-existing style `info`s in untouched files).
- New/updated tests: `agenda_cubit_test` (+ pin-toggle round-trips CS-14/19/FIX.05), `threads_cubit_test` (rewritten: archive/close/restore/cycle→closed reload), `threads_module_section_test` (rewritten: counter-hidden-≤5, "+ Dodaj wątek", no odklik button, CS-14 toggle), `thread_detail_cubit_test` (toggle shape), `realizations_repo_cubit_test` (rewritten: load-only), `realizations_module_section_test` (rewritten: Agenda-derived pin), NEW `goals_module_section_test` (header icons + single "+" + refresh cubit), NEW `health_check_section_cs24_cs25_test` (green colour, no orange; P3 "Show more").

### Manual QA still needed (device — cannot be done in-session)
1. **CS-14 thread pin toggle** on device: tap "Dodaj do agendy" → thread appears at top of Agenda (tag „Wątek") instantly; tap again → removed; delete the agenda item directly → the thread's button returns to "Dodaj do agendy" (self-heal). Confirm no duplicate agenda rows on repeat taps.
2. **CS-15 swipe-left** collapses the expanded thread card (in addition to the chevron); mark-closed → thread lands in „Domknięte wątki" with a date and is restorable; agenda odhaczenie flips status to „poruszony".
3. **CS-17** counter: absent at ≤5 active, „5 z N" at >5; **≥5 nudge** shows on add-at-capacity while the thread is still added.
4. **CS-18 / CS-22 P1 Nagraj/STT** in the Wątki + Goals add sheets on device (builds on Phase B iOS WAV fix).
5. **CS-19 / FIX.05** realization pin/unpin round-trip on both surfaces; delete-agenda-item clears the pin.
6. **CS-20** refresh: tap ↻ → narrative area shows loading → updated text appears (may take a few seconds for the async regen); force a failure → old text intact + retry toast.
7. **CS-23** bottom clipping: screenshot the Therapy Relationship box fully (incl. its bottom „Nowy check-in" row) on a **small + large** device, **Android gesture-nav + iOS home indicator**. The fix adds `kBottomNavBarHeight (76) + 24` to the scroll's bottom padding on top of `SafeArea`; verify no over/under-clearance on notchless Android too.
8. **CS-24** colours: check-in entries + the module header dot reflect stored green/amber/red; a `safety_escalation` check-in shows red + the warning icon.
9. **CS-25** contrast: the P3 controls are legible against the aqua-breeze card in bright light.

### Notes for Phase F (triage chips + notifications + Timeline)
- **Thread chip-state hooks:** the odklik machinery in `ThreadsCubit` (`archive`/`restore`/`dismissedIds`) is retained but no longer surfaced on the CS-15 card — it's available for the triage chip-deselect flow. A `thread`-kind triage chip should create/merge a `Thread` (contract §2) and then call `sl<ThreadsCubit>().loadActive()` to refresh the module (which reloads the CS-15 archive + counter too).
- **Module refresh after chip taps:** the pinned state of threads/realizations is derived **live** from `AgendaCubit`'s active list (source_type `thread`/`realization`). After a triage chip creates an agenda item or a Workspace-module row, Phase F should refresh the affected cubit: `sl<AgendaCubit>().loadActive()` (agenda + derived pins), `sl<TopicsCubit>().load()`, `sl<TodoCubit>().loadActive()`, `sl<ThreadsCubit>().loadActive()`, `sl<GoalTrackingCubit>().loadGoals()`. `AgendaCubit.loadActive(silent: true)` gives a flicker-free refresh.
- **Pin toggle entry points** (if triage needs them): `AgendaCubit.toggleThreadPin(id)` / `AgendaCubit.toggleRealizationPin(id)` — both hit the toggle endpoint then silent-reload; derived pin state updates everywhere automatically.
- **Realization `in_repo` triage group** (master-plan decision 2 / contract §2 `realization_ref`): toggles the realization's `in_repo` flag, NOT an agenda pin — distinct from CS-19's agenda-pin. Keep them separate.
- **P3 `controlColor`** param now exists on `WorkspaceExpandableList` for any Phase-F list rendered on a coloured background.

### Deploy note
- FE-only slice. Backend for the Workspace modules is A1 `aa2b3c4d5e6f` + A3 `bb3c4d5e6f70` (Alembic HEAD), **neither applied on prod**. Until they run: `PUT /threads/{id}/add-to-agenda` returning `PinToggleResponse`, `PUT /realizations/{id}/agenda-pin`, `GET /goals/archive`, `DELETE /goals/{id}`, and `GoalResponse.achieved_at` are required by this FE. **⚠ `user_goals.achieved_at` (`bb3c4d5e6f70`) is a migration on a LIVE prod table** — per STATUS_A3 it must run TOGETHER with the deploy or the whole Goals feature 500s on `UndefinedColumn`. Sequence deploy + `alembic upgrade head` together.
