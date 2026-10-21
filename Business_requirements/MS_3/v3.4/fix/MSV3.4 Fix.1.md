# MindSync Change Spec — MSV3.4 Fix.1 (prep card polish, Share on iOS, Discord link, onboarding goal & mood)

*For Claude Code · compiled 2026-08-19 · author of the notes: Darek (notes 17–18.08 \+ answer round 19.08 \+ his 18.08 edits of the MSV3.4 doc) · zero open questions · based on repo state frontend `dev` @ f11f72e (2026-08-18, build 2.0.82+155) · backend `main` @ 8dd329d (2026-08-19)*

## Summary

- Total items: 7  (FIX: 6 · CHANGE: 1 · of which re-works of shipped items: 3\)  
- Areas touched: Prep card (headers \+ edit pencils) · Share export (iOS) · menu boczne (Discord link) · Onboarding → Goals · Onboarding → Mood Trend · drawer/Settings locale audit  
- Intent: Darek's device checks of 17–18.08 on builds 2.0.79+. Three shipped items landed wrong: the Share export still cuts the card on iOS (MSV3.3 CS-22), the onboarding goal still never shows up in Workspace Goals (MSV3.4 CS-01), and the Discord invite in the drawer expired (the link, not the icon of MSV3.4 CS-15). On top of that: the prep card's edit pencils are tiny and misplaced, five of its section titles render smaller than the other two, and the mood picked during onboarding never appears in Mood Trend. The onboarding grounding found that the goal and mood failures very likely share one backend root cause, so they are ordered as a pair. This batch is separate from MSV3.5 (compiled 18.08, still unimplemented); nothing is duplicated between the two docs.

## What changed in the app since MSV3.5 (compiled 2026-08-18)

- Nothing from MSV3.5 or from these notes has started. Frontend since `6e9adf4`: only the Pre-release build bump `f11f72e` (2.0.82+155). Backend: one subscription fix `0648e2f` (renewal re-verification \+ prod DATE alignment, 19.08) \+ agent memory `8dd329d`. No MSV/CS-tagged work, no new agent-memory notes for either batch.  
- On Drive, the original doc "MSV3.4 \- Change Spec" was deleted; the doc "MSV3.4 \- Settings" (edited by Darek 18.08 17:29) now holds his revised copy of the MSV3.4 spec. Its CS-10/CS-11 edits document the accepted implemented state (no Account spoke in Settings; Privacy & Data on Konto). Its new locale requirement in CS-06/CS-16 ("all the names in settings in the English version and Polish version respectively") is input to this batch → CS-07 below.

## Status of the previous spec (MSV3.4, 2026-08-07) — reconciled 18.08, updated 19.08

| Item | Title (verbatim) | Status | Evidence | Action in this spec |
| :---- | :---- | :---- | :---- | :---- |
| CS-01 | Cel z onboardingu trafia do Workspace → Goals | DONE DIFFERENTLY, **reported not working on device 17.08** | `4bb9b2c` (backend appends, step-4 trigger); Darek 17.08: "Cel z onboardingu trafia... Do powtórki" | **re-opened → CS-05 below** (the step-4 trigger stays accepted; the outcome does not work) |
| CS-02 | Ikona "tune" → "i"; Edit Layout usunięty | DONE | MSV3.3 CS-01 (`ff20f2a`) | — |
| CS-03 | Mood Trend: ikona toggle → ołówek | DONE | MSV3.3 CS-02 (`ff20f2a`) | — |
| CS-04 | "Edit focus areas", "+Add new", safe area | DONE | `1c20e54`, note cs04\_cs13 | defects covered in MSV3.5 CS-01..03, not here |
| CS-05 | Ikona Edit Square przy dacie → Moja terapia | DONE | `1c20e54` | — |
| CS-06 | Menu boczne: nowa struktura | DONE | `1c20e54`, note cs06\_… | locale requirement added 18.08 → CS-07 below |
| CS-07 | "Usuń konto" na dole ekranu Konto | DONE DIFFERENTLY (re-auth kept) | note cs07\_cs09\_cs10 | accepted 18.08 → intended state |
| CS-08 | Moja terapia hub | DONE | `1c20e54` | Custom-interval defect is MSV3.5 CS-08, not here |
| CS-09 | Subskrypcja: ekran za pozycją menu | DONE | `1c20e54` | — |
| CS-10 | Ustawienia: przebudowa | DONE DIFFERENTLY (Privacy & Data → Konto) | note cs07\_cs09\_cs10 | accepted 18.08; Darek's 18.08 doc edit now documents this state |
| CS-11 | Therapists schowana | DONE | `1c20e54` | — |
| CS-12 | O MindSync: chevron | DONE | `1c20e54` | — |
| CS-13 | support@ → hello@ | DONE | `1c20e54` | — |
| CS-14 | Zostaw recenzję: natywny in-app review | DONE | `1c20e54` | verify on device (unchanged) |
| CS-15 | Dołącz do społeczności: ikona Discord | DONE (icon), **invite link expired** | `1c20e54`; Darek 18.08: "Ikona poprawna, link do poprawy \- wygasł lub nieprawidłowy" | **→ CS-04 below** |
| CS-16 | Wyloguj się: pop-out | DONE | `1c20e54` | ENG header requirement added 18.08 → CS-07 below |

**MSV3.3 (shipped 15.08):** CS-22 "Share wysyła kawałek karty zamiast całości" comes back — Darek 18.08: "całe do powtórki na iOS" → **CS-03 below**. Everything else stands as reconciled on 18.08.

**MSV3.5 (compiled 18.08):** a separate, still-open work order (8 items: Edit focus areas sheet, prep card mood section WITH chart, Threads full text, in-app reminders, Weekly/Monthly, Custom interval). **None of its items are repeated here.** One correction it inherits: its "Already shipped" list records MSV3.4 CS-01 as accepted-and-intended; Darek's 17.08 device note supersedes that — the accepted part is the step-4 trigger design, not the outcome. CS-05 in this doc is the authoritative order for the onboarding goal.

**MSV3.10 – User Feedback Fix (13.08):** unchanged, separate batch, still nothing in the repos.

## Global guardrails (read before touching anything)

- **Two open specs exist.** This doc and MSV3.5 do not overlap in scope, but CS-01/CS-02 here edit `prep_card_widget.dart`, the same file MSV3.5 CS-04 rebuilds (the "Your Mood This Week" content). Whoever lands second rebases; if both are in flight, land this doc's CS-01/CS-02 together with MSV3.5 CS-04 in one pass over that file.  
- Do NOT touch `lib/widgets/questions_section.dart` for the prep card items. The prep card does not use it (doc comment in that file confirms); it feeds the After Therapy, Recording and Between Sessions cards. The prep card pencils and headers live in `prep_card_widget.dart` itself.  
- Do NOT touch the Goals module UI or the manual "+ Add goal" path. CS-05 changes only the onboarding path's ordering and the sync robustness.  
- The `PUT /api/v1/users/therapy-context` endpoint (users.py) serves every onboarding step. The CS-05/CS-06 robustness fixes there must not change its behaviour for normal step saves.  
- Old builds stay in use for weeks; any API change stays additive.  
- Both platforms (Android \+ iOS) and all 7 ARB locales for every item. After each item: app builds, no dead references, no broken navigation.

---

# A · Output cards → Preparation card

## CS-01 · FIX · \[Output cards → Preparation card\] · Ikona ołówka przy Questions i Summary: w wierszu tytułu, większa, cel 48 px

- **Type:** FIX  
- **Location:** Prep card → sections "Questions" and "Summary" → their edit pencils. Reached: Timeline → Prep card (completed card). `verified: mindsync_app/lib/screens/therapy_capture/widgets/prep_card_widget.dart` — the card has exactly three pencil implementations:  
  1. `_buildSectionHeader` `:1500-1508`: pencil IN the header row, `Icons.edit_outlined` size 16 inside `Padding(4)` on a bare `GestureDetector` → effective tap target **24×24 dp**. Used by **Summary** (`:676-681`, `editable: true`).  
  2. `_buildInlineEditTrigger` `:904-910`: pencil size 14 inside `Padding(4)` → **22×22 dp**, rendered in a separate `Align(centerRight)` row **below** the section content. Used by **Questions** (`:1334-1337`, under the header row built at `:1311-1327`) and by Threads (`:789-792`, `:814-817`).  
  3. `CollapsibleCardSection` pencil (`lib/widgets/collapsible_card_section.dart:61-72`): size 16, only left padding → **24×16 dp**. Used by **Patterns** (`:1080-1082`). No `IconButton`/`InkWell` anywhere in the card, so nothing enforces the Material 48 dp minimum. Extra defect found: the Questions pencil renders only when the section has questions (`:1329-1337`) — an empty Questions section has no edit entry point at all.  
- **Now (wrong):** The Questions pencil is 14 px, sits in its own row below the section ("mikro i za nisko"), and disappears when the section is empty. The Summary pencil is 16 px with a 24×24 target. The Patterns pencil is 24×16. All three are uncomfortable to tap.  
- **Expected:** Every edit pencil on the prep card sits **in the same row as the section icon and title** (right-aligned, the way `_buildSectionHeader` already places Summary's), is visually larger, and has a tap target of **min 48×48 dp**. Decision 19.08 (compiler): this covers all three pencil call sites (Questions, Summary, Patterns and the two Threads triggers use the same fixed control), and the Questions pencil renders in the empty state too, so a user with no questions can still add one.  
- **Logic:** header row \= icon → title → (spacer) → pencil, one shared control (e.g. `IconButton` with `constraints: BoxConstraints(minWidth: 48, minHeight: 48)` or an `InkWell` sized 48\) → tap → `_startEditing(section)` exactly as today. Edit mode and save flow unchanged.  
- **Not this:** do not add pencils to sections that are not editable today (To-do, Realizations, Your Mood This Week, card header) — only relocate and resize the existing ones.  
- **Why:** "Ikona ołówka przy Questions jest mikro i za nisko. Ma być w tym samym wierszu co ikona oraz tytuł, większa. 48px. Obszar klikalny duży, żeby wygodnie się tapowało. Tak samo Ołówek przy summary jest za mały." (Darek, 18.08)  
- **Do NOT touch:** `questions_section.dart` (other cards); which sections are editable; the edit forms themselves.  
- **Done when:** On a completed prep card, the pencils for Summary, Questions, Patterns and Threads all render in their header rows, visibly larger, and each tap lands comfortably (48 dp verified with the Flutter inspector or a debug hit-test); an empty Questions section still shows its pencil; edit and save work as before; both platforms.  
- **Risk:** Low. One file plus the small shared collapsible-section widget.

## CS-02 · CHANGE · \[Output cards → Preparation card\] · Tytuły sekcji zunifikowane do rozmiaru Patterns/Questions

- **Type:** CHANGE  
- **Location:** Prep card → section titles of **Summary, To-do, Threads, Realizations, Your Mood This Week**. `verified: prep_card_widget.dart` — two title styles exist on the card:  
  - **14 / w700 / letterSpacing 0.3 / primary\[700\]** (the target): Questions (`:1318-1323`) and Patterns (via `lib/widgets/collapsible_card_section.dart:44-50`).  
  - **11 / w700 / letterSpacing 0.8 / primary\[700\]** (too small): the shared `_buildSectionHeader` style block `:1492-1497` (feeds Summary `:676-681` and Your Mood This Week `:1207-1212`) plus three inline header rows: To-do `:1402-1418`, Threads `:727-743` **and its duplicate legacy branch `:768-784`** (both must change), Realizations `:1444-1460`. Icons are already 18 px everywhere; only the text size differs. ARB: `prep_sinceLastSession` "Summary" (`app_en.arb:1506`), `prep_patternsThisWeek` "Patterns" (`:1509`), `workspace_topicsTitle` "Questions" (`:2174`). Known wrinkle: Patterns swaps its 14 px collapsible header for the 11 px `_buildSectionHeader` while being edited (`:1048-1071`) — the same title renders at two sizes depending on mode.  
- **Now (wrong):** Five section titles render at 11 px while Questions and Patterns render at 14 px; the card looks like two different components glued together.  
- **Expected:** All section titles on the prep card render at the Questions/Patterns style: 14 / w700 / letterSpacing 0.3 / primary\[700\], icons 18 px as today. The Patterns edit-mode header keeps the same 14 px style instead of dropping to 11 px. In practice: change the one shared style block (`:1492-1497`) and the three inline rows (Threads twice, To-do, Realizations) to the target values.  
- **Not this:** do not resize the compact share-render headers (`_buildShareSectionHeader`, 11 px) — the share view applies that compact style uniformly to all its sections on purpose (MSV3.3 CS-12 decision); this item is about the on-screen card only. Do not touch the other cards' `QuestionsSection` header (already 14 px).  
- **Why:** "Zunifikować tytuł: summary, to-do, threads, realizations, your mood this week → mają wyglądać jak Patterns i Questions jeżeli chodzi o wielkość." (Darek, 18.08)  
- **Do NOT touch:** Section content, order, edit flows; the share render; other output cards.  
- **Done when:** A screenshot of a full prep card shows every section title at the same size as Questions and Patterns; Patterns keeps that size while being edited; the share export still uses its compact headers; both platforms.  
- **Risk:** Low.

---

# B · App-wide → Share

## CS-03 · FIX · \[App-wide → Share\] · Eksport karty obcięty na iOS — pełna karta na obu platformach

- **Type:** FIX · **re-work of MSV3.3 CS-22** (shipped 15.08 in `ff20f2a`: full-height offscreen capture \+ JPEG; Darek 18.08: Share still sends a piece of the card — "całe do powtórki na iOS")  
- **Location:** The one shared export pipeline: `verified: mindsync_app/lib/utils/card_share_util.dart:88-129` — `ScreenshotController.captureFromLongWidget` wrapped in `MediaQuery(const MediaQueryData()) → Localizations → Theme → Material → BrandedShareWrapper`, `constraints: BoxConstraints(maxWidth: config.wrapperWidth)` (no height limit, `:115`), `pixelRatio: 3.0` hardcoded (`:116`), `delay: 200ms` (`:117`), then `img.decodePng` → `img.encodeJpg(quality: 92)` **synchronously on the UI isolate** (`:127-129`), temp file \+ `Share.shareXFiles` without `sharePositionOrigin` (`:48-55`), everything inside a silent `try/catch → debugPrint` (`:58-60`). Nine entry points, all through this util: Prep (`prep_card_widget.dart:257`), After Therapy (`session_card_widget.dart:184`), Recording (`recording_summary_widget.dart:121`), Between Sessions (`between_session_note_widget.dart:175`), Realization (`realization_detail_widget.dart:66`), Weekly (`weekly_summary_widget.dart:338`), Monthly (`monthly_audit_widget.dart:236`), Health Check (`health_check_result_card.dart:318`), Bio (`character_tab_screen.dart:255`). No `Platform.isIOS` branch anywhere in the pipeline.  
- **Now (wrong):** On iOS the shared image still contains only part of the card. The code allows it: export width is 1200 px (400 logical × 3.0) and height is unbounded; a long card (Monthly Audit \~10 sections, a full Prep card) reaches 2 700–5 000 logical px → **8 100–15 000 physical px**, which lands in or above the Metal texture limit band (8 192 px on older iPhones, 16 384 px on newer). A render target clamped at the texture limit yields exactly a top-aligned partial image. Ranked causes from the code (mechanisms inferred, inputs verified):  
  1. `pixelRatio: 3.0` with no height cap → texture-limit clipping on iOS/Metal (the only hypothesis that produces a *partial* image rather than none).  
  2. Memory spike: decode+encode of a 1200×12 000 image is \>150 MB peak, synchronous on the UI thread — iOS kills sooner than Android (repo precedent: `msv32_fix5_record_session_ios.md` fixed the identical pattern with `compute()`; the share path never got it).  
  3. Failures are invisible: the silent catch means an iOS-only crash of the capture looks like a user cancelling; nothing reaches telemetry.  
  4. `Share.shareXFiles` without `sharePositionOrigin` breaks the share sheet on iPad (separate iOS defect in the same lines). Also: `test/screens/therapy_capture/widgets/prep_card_share_content_test.dart:72-97` still reproduces the PRE-fix `SingleChildScrollView` construct — the harness would not catch a CS-22 regression.  
- **Expected:** Every share button exports the **complete** card as JPEG on iOS and Android, long cards included.  
  1. **Verify first on an iOS device:** reproduce with the longest available card (Monthly Audit or a full Prep card); log the computed capture height. If the pixel height exceeds \~8 000, the texture-limit path is confirmed; note the finding in the PR.  
  2. **Bound the pixel height:** compute `pixelRatio` per capture so `height_logical × ratio ≤ 8 192` (floor 2.0, i.e. long cards trade some sharpness for completeness), or tile the capture and stitch — implementer's call, logged.  
  3. **Move decode/encode off the UI isolate** (`compute()`), matching the recording precedent.  
  4. **Surface failures:** replace the silent catch with a user-visible error toast \+ a logged/analytics event, so a failed share stops looking like a cancel.  
  5. **iPad:** pass `sharePositionOrigin` to `shareXFiles`.  
  6. Update the stale share-content test harness to the post-`ff20f2a` construction.  
- **Not this:** do not add new share buttons, do not change what each card's share content contains, do not change the JPEG format/branding wrapper.  
- **Why:** "CS-22 · Share wysyła kawałek karty zamiast całości — całe do powtórki na iOS." (Darek, 18.08)  
- **Do NOT touch:** The share content widgets themselves (`_buildShareContent` per card); the plain-text share of the Discord link and the WAV export (different paths).  
- **Done when:** On a physical iPhone (ideally one older device too) and one Android device: sharing the longest Monthly Audit and a full Prep card produces a JPEG showing the entire card top to bottom; a forced capture failure shows an error to the user instead of nothing; share from an iPad presents the share sheet correctly; the updated test harness matches the real composition.  
- **Risk:** Medium. One util file, but verification needs physical iOS hardware.

---

# C · Menu boczne

## CS-04 · FIX · \[Menu boczne → Dołącz do społeczności\] · Nowy link zaproszenia na Discord

- **Type:** FIX *(the icon from MSV3.4 CS-15 is correct; the link it opens expired)*  
- **Location:** Drawer → row "Dołącz do społeczności". `verified: mindsync_app/lib/screens/main_page/widgets/drawer_menu.dart:181` — `onTap: () => UrlLaunchHelper.openApp('https://discord.gg/ZWqzxdsr')`.  
- **Now (wrong):** The hardcoded invite `https://discord.gg/ZWqzxdsr` is expired or invalid; the row opens a dead invite.  
- **Expected:** The row opens **`https://discord.gg/pVWS39kpg`** (link supplied by Darek, 19.08). Replace the constant; nothing else changes. Note for the server side (no code): the invite should be configured "never expire" on Discord so this does not recur — Darek owns that setting.  
- **Do NOT touch:** The Discord icon (CS-15, correct); the row's position; `UrlLaunchHelper`.  
- **Done when:** Tap opens a working invite to the MindSync server on both platforms; grep for `ZWqzxdsr` returns nothing.  
- **Risk:** Low. One constant.

---

# D · Onboarding

## CS-05 · FIX · \[Onboarding → Cel terapeutyczny\] · Cel z onboardingu naprawdę ląduje w Workspace → Goals — trzecie podejście, z diagnozą

- **Type:** FIX · **re-work of MSV3.4 CS-01** (backend shipped 15.08 in `4bb9b2c`; Darek 17.08: the goal still reaches no feature). The accepted deviation stands: creation triggers when the goal text is saved at onboarding step 4, not at completion (decision 18.08).  
- **Location & verified chain (the wiring is CORRECT end to end at HEAD):** Onboarding screen 3 collects the goal (`onboarding_journey_view.dart:333-338, 360-365`) → `TherapyOnboardingCubit.saveJourneyAndAdvance` sends `{goals_text, onboarding_step: 4}` (`therapy_onboarding_cubit.dart:409-422`) → `PUT /api/v1/users/therapy-context` (`therapy_context_manager.dart:12-19`, `endpoints.dart:88`) → backend `upsert_user_therapy_context` (`MindSync/app/api/v1/endpoints/users.py:1206`) calls `sync_goals_from_onboarding` when `goals_text` is present (`:1246-1248`) → `crud.py:6807-6871` appends via `create_goal(..., enforce_active_cap=False)`. The FE send code is unchanged since March (`git log -S goals_text`), so build 2.0.79 sends it too; `4bb9b2c` was live on prod (v534) before Darek's 17.08 test. Reset Onboarding reruns the same path (`settings_cubit.dart:102-111` → the same onboarding screen).  
- **Now (wrong):** A fresh onboarding (and Reset Onboarding) with goal text ends with no visible goal card in Workspace → Goals. Since the wiring is correct, the loss is downstream — three verified mechanisms, in order of likelihood:  
  1. **Created but never rendered.** `create_goal` assigns `display_order = max+1` (`crud.py:5395-5402`), the list sorts ascending (`:5423-5430`), so the onboarding goal is always **last** — and the Workspace Goals module renders only the first three (`goals_module_section.dart:140` `take(3)`). A manually added goal shows instantly only because the cubit prepends it locally (`goal_tracking_cubit.dart:74-78`). On an account with 3+ active goals (Darek's Reset Onboarding test on his own account) the new goal is invisible in the module.  
  2. **Per-text idempotency:** retyping the exact same goal text as an existing active goal creates nothing (`crud.py:6864-6866`).  
  3. **Poisoned session, silent 200:** in the same PUT, the symptom sync runs BEFORE the goal sync on the same DB session (`users.py:1229-1238` then `:1246-1286`); both `except` blocks swallow every exception with a warning and **no `db.rollback()`**. One symptom-sync failure leaves the session unusable, the goal sync then throws and is swallowed too, the endpoint still returns 200\. This single fault produces CS-05 and CS-06 together — exactly the pair Darek reported.  
- **Expected:**  
  1. **Verify first** (decides which mechanism, before coding): query `user_goals` for the test account after a Reset-Onboarding run, and grep Heroku logs for the paired warnings `"Symptom sync from onboarding failed"` / `"Goal sync from onboarding failed"` (`users.py:1238, :1286`). Record the finding in the PR.  
  2. **Fix the session handling:** add `db.rollback()` in both `except` blocks, raise the log level, and emit a diagnostic event, so one sync failing can never silently kill the other or hide itself.  
  3. **Make the goal visible:** decision 19.08 (compiler) — a goal created by the onboarding path lands at the **top** of the Goals module (display\_order before existing goals, onboarding path only; the manual "+ Add goal" path and the Goals UI stay untouched). A user finishing onboarding must see the goal without opening "see all".  
  4. **Stop losing the text on the frontend:** `FullScreenTextEditor` discards typed text when closed with X or system back (`full_screen_text_editor.dart:107` pops null; `onboarding_journey_view.dart:98-101` ignores null), and the controller is never re-seeded when navigating back and forward — fix both, so typed goal text survives navigation.  
  5. **Test the contract:** add a test asserting `goals_text` is present in the step-4 PUT body (none exists today), and a backend test that a symptom-sync failure no longer prevents goal creation.  
- **AI:** unchanged from MSV3.4 CS-01: the created goal gets full "+ Add goal" parity (XP, narrative enqueue, RAG indexing, goal\_created event), each side effect guarded independently.  
- **Outcome:** A fresh onboarding with goal "X" ends with "X" visible as the first goal card in Workspace → Goals; Reset Onboarding with "Y" adds a second visible card.  
- **Not this:** do not move the trigger to onboarding completion (the step-4 trigger is the accepted design); do not touch the 5-goal cap for the manual path.  
- **Do NOT touch:** The Goals module UI and narrative pipeline; goals the user already has; the manual add path's ordering.  
- **Done when:** On a device build, both platforms: fresh onboarding with goal "X" → "X" is the top card in Workspace → Goals; Reset Onboarding with "Y" on an account that already has 4+ active goals → "Y" visible in the module without "see all"; typing a goal, closing the editor with X, reopening → text still there; the PR names which of the three mechanisms was the actual cause on prod, with the log/DB evidence; the new tests pass.  
- **Risk:** Medium. Backend session-handling change in a hot endpoint; the fix must not alter normal step saves.

## CS-06 · FIX · \[Onboarding → Mood\] · Mood z onboardingu (np. Low Mood) trafia do Mood Trend jako aktywny, śledzony obszar

- **Type:** FIX *(the sync exists on the backend and demonstrably does not deliver; this repairs it, not builds it)*  
- **Location & verified state:** Onboarding screen 1 collects focus-area chips (presets: "Low mood", "Unease", "Overwhelm", "Worries", "Stress", "Sleep", "Loss", "Focus" — `symptom_presets.dart:8-20`; the API value is the English key, display is localized; custom chips allowed), screen 2 collects severity 1–10 (cannot be skipped, defaults 5). Both are PUT to the same therapy-context endpoint (`therapy_onboarding_cubit.dart:297-318, 325-346`) and stored in `UserTherapyContext.focus_areas` / `severity_ratings` (`MindSync/app/models/models.py:677-706`). **The backend already converts them into tracked symptoms:** `crud.sync_symptoms_from_onboarding` (`crud.py:3345-3378`) creates `UserSymptom` \+ an initial `SymptomScore(score=rating)` — the same rows the "Edit focus areas" sheet creates — called from `users.py:1229-1236` on every therapy-context PUT once both blobs are stored. Mood Trend reads exactly these rows.  
- **Now (wrong):** After onboarding, the picked mood does not appear in Mood Trend or in the "Edit focus areas" sheet. Given the sync exists, the failure is one of: (a) the silent-swallow/no-rollback defect shared with CS-05 (`users.py:1237`); (b) the archived-skip: the sync skips any area whose name matches an existing symptom **including archived ones** (`get_user_symptoms` defaults `visible_only=False`, `crud.py:3165-3181`), so a previously archived "Low mood" is never re-added or re-scored.  
- **Expected (decisions 19.08):**  
  1. The mood(s) picked in onboarding appear in Mood Trend as **Active, tracked immediately** — chart and narrative start like for a symptom added via "+Add new" — with the onboarding severity as the first score.  
  2. Archived same-name symptom → **restored to Active** (compiler decision: the user just chose that area again; keep its history) instead of silently skipped.  
  3. Fix the shared swallow/rollback defect (one fix with CS-05 point 2).  
  4. **No backfill** (decision 19.08): works for onboardings and Reset Onboarding runs after rollout; existing accounts are not migrated.  
- **Logic:** onboarding steps 1–2 save focus areas \+ severities (unchanged) → the journey/each subsequent PUT triggers the sync (unchanged trigger) → per area: no symptom with that name → create Active with initial score; archived symptom with that name → restore to Active \+ record the new score; active symptom with that name → record nothing new (already tracked, unchanged) → Mood Trend shows the area at next load.  
- **Outcome:** A new user who says "Low mood" in onboarding opens Main and sees Low mood tracked in Mood Trend with their first score already on the chart.  
- **Not this:** do not build a second, client-side creation path (`POST /api/v1/symptoms/` from the onboarding screens) — the server-side sync is the existing design; repair it. Do not re-score an area the user is already actively tracking.  
- **Why:** "Dodanie Mood z Onboarding np Low Mood nie zostaje dodawany z onboardingu do Mood Trend or Focus Area \- powinien tam trafić." (Darek, 17.08)  
- **Do NOT touch:** The "Edit focus areas" sheet and its cubit (MSV3.5 territory); the Mood Trend module UI; `UserTherapyContext` storage shape; the legacy clinical preset list in ARB (display-only for old rows).  
- **Done when:** On a device build, both platforms: fresh onboarding picking "Low mood" with severity 6 → "Low mood" is in Active in the Edit focus areas sheet and renders in Mood Trend with a first score of 6/10; Reset Onboarding adding a new area adds it; an archived area picked again returns to Active with history intact; an area already active is not duplicated and its scores are not overwritten; existing accounts unchanged.  
- **Risk:** Medium. Same endpoint and session-handling area as CS-05 — implement the two as one backend change set.

---

# E · Locale

## CS-07 · FIX · \[Menu boczne \+ Ustawienia\] · Nazwy konsekwentnie po angielsku w EN i po polsku w PL

- **Type:** FIX *(from Darek's 18.08 edits of the MSV3.4 doc: "Make sure all the names in settings are in the English version and Polish version respectively"; also the CS-16 note that the logout pop-out header is "Wyloguj" PL / "Log out" ENG)*  
- **Location:** Drawer (all 16 rows \+ logout pop-out) and the Settings screen (pills, notifications, buttons), both locales. `verified:` the ARB side looks correct — `app_en.arb:699-708` has English values (`Subscription`, `Privacy Policy`, `Terms of Service`, `FAQ`, `Share MindSync`, `Log Out`, `Log out` confirm title), `myTherapy_title` \= "My Therapy" (`:2367`); `app_pl.arb` shows no English leftovers for the Settings labels ("Persona AI" is identical in both by design). No hardcoded Polish drawer strings in Dart (grep clean).  
- **Now (unverified on device):** Darek's edit implies he saw mixed-language names somewhere in the menu or Settings. The ARB sources look clean, so if the defect is real it is either a string read from outside l10n, a stale generated file in the shipped build, or it concerns a label not covered by the spot-check.  
- **Expected:** verify first: on a device build, walk the drawer (all rows, logout pop-out) and the full Settings screen in EN and in PL; every label follows the app language. Fix any string that does not switch (move it to ARB or correct the wrong value); if everything already switches correctly, record that in the PR and close the item with screenshots of both locales.  
- **Do NOT touch:** The five non-EN/PL locales beyond keeping parity for any key you add or change; the drawer structure.  
- **Done when:** Side-by-side screenshots of the drawer and Settings in EN and PL show fully consistent language on each; any fixed key is translated in all 7 ARB files; both platforms.  
- **Risk:** Low.

---

## Already shipped — verify, do not redo

- MSV3.4 CS-14 "Zostaw recenzję": still pending its physical-device verification (unchanged from 18.08).  
- All other MSV3.4 items and the rest of MSV3.3: shipped and reconciled 18.08; nothing else from those batches is reopened here.  
- MSV3.5's eight items: open, ordered in their own doc — do not pick them up from this one.

## Suggested execution order

1. **CS-04** (one constant; ship immediately).  
2. **CS-05 \+ CS-06 together** (one backend change set: rollback/log fix decides both; then the visibility fix for goals and the archived-restore for symptoms; the frontend editor fix rides along).  
3. **CS-03** (needs a physical iPhone; independent of everything else).  
4. **CS-01 \+ CS-02 together** (one pass over `prep_card_widget.dart`; coordinate with MSV3.5 CS-04 if it is in flight — same file).  
5. **CS-07** (device audit; last, after the drawer/Settings stopped moving).

