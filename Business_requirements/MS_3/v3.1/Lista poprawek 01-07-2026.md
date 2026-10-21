# MindSync Change Spec — MASTER (Main, Timeline, Character, Stats, Recording, Reflect)

*For Claude Code · 2026-07-01 · author: Darek* *Supersedes: `MindSync-change-spec_main-cleanup_2026-07-01.md` (now deprecated — work only from this file).*

## Summary

- Total items: 33  (DELETE: 8 · CHANGE/rename: 13 · FIX: 12\)  
- Areas touched: Main, Timeline, Character, Stats, Settings, Reflect, Output – Recording, Output – Check-in, Output – Therapy Relationship  
- Intent: A single cleanup \+ rename \+ bug-fix pass. Three goals: (1) strip the Main screen of dead/duplicate sections, (2) fix the naming chaos so every surface uses the same word for the same feature, and (3) clear a batch of UI bugs and small feature corrections. Naming is the highest-value part — today the same feature is called four different things across Main/Stats/Timeline/Output, which confuses users *and* an AI agent reading the code.

---

## Global guardrails (read before touching anything)

**⚠️ The single biggest trap in this batch — "Therapy Relationship" vs "Check-in samopoczucia":**

- There is **one** feature about *how healthy the user's therapeutic relationship is*. It is currently surfaced under **four different names** and must be **renamed to one consistent name** everywhere: **PL `Relacja Terapeutyczna` / ENG `Therapy Relationship`**. Treat all four as the **same feature, different surfaces** — do NOT create new features, just rename:  
  - Main: `How are you right now` → Therapy Relationship  
  - Stats: `Therapy Health Check` → Therapy Relationship  
  - Timeline tab: `Chek-in terapii` → Therapy Relationship  
  - Output: `Refleksja` → Therapy Relationship  
- **`Check-in samopoczucia` is a DIFFERENT, mood-based feature and is being DELETED** (see D-05). Do **NOT** confuse it with the Therapy Relationship feature above, and do **NOT** delete the Therapy Relationship feature. One is a mood/health check (deleted); the other is about the therapeutic relationship (kept \+ renamed).  
- Exception on the delete: the Stats `Check-in samopoczucia` **endpoint** is kept (see FX-03).

**Deletion scope:**

- All DELETE items in this spec are **full removals** — remove the UI **and** the supporting widgets/data/logic — *unless* the item's "Do NOT touch" line says otherwise (e.g. shared data that a surviving feature still reads).

**Naming rules (applies to every RENAME item):**

- Keep the user's original labels verbatim when searching the code (they're the grep anchor), then apply the new PL \+ ENG names from the **Naming Reference** table below.  
- Rename **user-facing strings and localization keys**; do not rename internal class/file names unless it's trivial and safe — the goal is UX consistency, not a refactor.

**After every item:** run the app (Android \+ iOS), confirm no dead references, no broken navigation, and that renamed strings show in both PL and ENG locales.

---

## Naming Reference (old → new)

| Area | Old label | New PL | New ENG |
| :---- | :---- | :---- | :---- |
| Timeline tab | Podsumowania (De-briefs) | Po terapii | After therapy |
| Timeline tab | Notatki (Notes) | Między sesjami | Between sessions |
| Timeline tab | Chek-in terapii (Therapy Checkin) | Relacja Terapeutyczna | Therapy Relationship |
| Main | How are you right now | Relacja Terapeutyczna | Therapy Relationship |
| Stats | Therapy Health Check | Relacja Terapeutyczna | Therapy Relationship |
| Output – Check-in | Refleksja | Relacja Terapeutyczna | Therapy Relationship |
| Output – Recording | Przegląd | Podsumowanie | Overview |
| Output – Recording card | Topics with timestamps | Główne tematy | Main topics |
| Character | Voice AI | Persona AI | Persona AI |
| Character | How I see you | Overview | Overview |
| Settings (side drawer / Main view) | Ton AI | Persona AI | Persona AI |

---

# 1 · Deletions (DELETE)

## D-01 · DELETE · \[Main\] Goals

- **Type:** DELETE (full)  
- **Location:** Main screen, "Goals" section. Lead: grep `lib/` for the Goals widget on Main / `Goals`.  
- **Action:** Delete the Goals feature entirely — section, entry point, widget(s), and Goals-only data/logic.  
- **Why:** Being cut ("w obecnej formie usunąć", confirmed full removal).  
- **Do NOT touch:** Any Goals data/logic shared with a feature that stays — if found, stop and flag (OQ-1). Otherwise remove all.  
- **Done when:** Goals no longer on Main; widgets/models removed; app builds; grep `Goals` shows no live references.  
- **Risk:** Medium — verify nothing else reads Goals data before deleting.

## D-02 · DELETE · \[Main\] Recent Sessions

- **Type:** DELETE (full UI \+ widget; keep data)  
- **Location:** Main screen, "Recent Sessions" section.  
- **Action:** Delete the Recent Sessions section and its widget from Main.  
- **Why:** Being cut.  
- **Do NOT touch:** The underlying **session data** and the **Therapy Timeline** (which also lists sessions) — remove the Main block, not the sessions.  
- **Done when:** Recent Sessions gone from Main; Timeline still shows sessions; app builds; no dead references.  
- **Risk:** Low.

## D-03 · DELETE · \[Main\] Therapy tracking

- **Type:** DELETE (full)  
- **Location:** Main screen, "Therapy tracking" section.  
- **Action:** Delete the Therapy tracking feature entirely — section, entry point, widgets, and its data/logic.  
- **Why:** Being cut.  
- **Do NOT touch:** Any tracking data shared with a progress/reporting feature that stays — flag if found (OQ-1). Otherwise remove all.  
- **Done when:** Therapy tracking gone from Main; widgets/models removed; app builds; no dead references.  
- **Risk:** Medium — verify progress/reporting doesn't read its data first.

## D-04 · DELETE · \[Main\] Session preparation \+ De-brief after session

- **Type:** DELETE (Main copies only)  
- **Location:** Main screen — the "Session preparation" and "De-brief after session" blocks.  
- **Action:** Remove **both** blocks from Main.  
- **Why:** Duplicates of what's already in the **Therapy Timeline**.  
- **Do NOT touch:** The Session preparation / De-brief functionality **in the Therapy Timeline** — that stays and must keep working. Remove only the Main entry points; if Main reuses the Timeline widgets, delete only the Main references, not the shared widget.  
- **Done when:** Neither block on Main; same functions still reachable in Timeline; app builds; no dead references from Main.  
- **Risk:** Medium — confirm shared vs. separate code (OQ-2).

## D-05 · DELETE · \[Main\] Check-in samopoczucia

- **Type:** DELETE  
- **Location:** Main screen, "Check-in samopoczucia" section. Lead: grep `Check-in samopoczucia`.  
- **Action:** Remove the "Check-in samopoczucia" (mood) block from Main.  
- **Why:** Being cut.  
- **Do NOT touch:** ⚠️ The Therapy Relationship feature (formerly "How are you right now") — that STAYS and is renamed (see RN-04). These are different features. Also see FX-03: the Stats endpoint for this feature is kept.  
- **Done when:** "Check-in samopoczucia" gone from Main; the Therapy Relationship / "How are you right now" block still present; app builds; no dead references.  
- **Risk:** Medium — high confusion risk; confirm the exact widget before deleting.

## D-06 · DELETE · \[Output – Recording\] "Jak płynęła rozmowa"

- **Type:** DELETE (full feature)  
- **Location:** Recording output — the "Jak płynęła rozmowa" section. Lead: grep `Jak płynęła rozmowa`.  
- **Action:** Delete the entire feature — remove from the Recording output including its generation/logic.  
- **Why:** Feature cut entirely.  
- **Do NOT touch:** Other Recording-output sections and the recording/transcription pipeline.  
- **Done when:** "Jak płynęła rozmowa" gone everywhere; generation code removed; app builds; other outputs work; no dead references.  
- **Risk:** Medium — confirm nothing downstream consumes its output (OQ-3).

## D-07 · DELETE · \[Output – Recording card\] Emotional arc

- **Type:** DELETE (full feature)  
- **Location:** Recording output card — "Emotional arc" element.  
- **Action:** Remove the Emotional arc element and its generation entirely ("do wyjebania").  
- **Why:** Cut.  
- **Do NOT touch:** Other card elements (see the card order in RC-01).  
- **Done when:** Emotional arc gone from the Recording card; generation removed; app builds; no dead references.  
- **Risk:** Low–Medium.

## D-08 · DELETE · \[Output – Recording card\] Unresolved topics

- **Type:** DELETE (full feature \+ endpoint)  
- **Location:** Recording output card — "Unresolved topics" element, including its endpoint.  
- **Action:** Remove the Unresolved topics element **and** its endpoint.  
- **Why:** Cut.  
- **Do NOT touch:** Other card elements / endpoints.  
- **Done when:** Unresolved topics gone from card; endpoint removed; app builds; no dead references.  
- **Risk:** Medium — confirm the endpoint isn't shared before deleting (OQ-4).

---

# 2 · Naming changes (CHANGE / rename)

All names below come from the **Naming Reference** table. Rename user-facing strings \+ localization keys in both PL and ENG.

## RN-01 · CHANGE · \[Timeline\] Rename three tabs

- **Location:** Therapy Timeline tab bar.  
- **Action:** Rename tabs — `Podsumowania`/`De-briefs` → **Po terapii / After therapy**; `Notatki`/`Notes` → **Między sesjami / Between sessions**; `Chek-in terapii`/`Therapy Checkin` → **Relacja Terapeutyczna / Therapy Relationship**.  
- **Why:** Tab names don't match the features they come from and create information chaos (e.g. "Podsumowanie" tab opens on "Podsumowanie sesji", which users confuse with the session recording).  
- **Do NOT touch:** The tab contents/logic — labels only. The Timeline "Therapy Relationship" tab is the **same** feature as RN-04/RN-05/RN-06 (see guardrail).  
- **Done when:** All three tabs show the new PL \+ ENG labels; no old labels remain in either locale; navigation unchanged.  
- **Risk:** Low.

## RN-02 · CHANGE · \[Output – Recording\] Rename "Przegląd" → Podsumowanie / Overview

- **Location:** Recording output — the "Przegląd" section (the card's first element, see RC-01).  
- **Action:** Rename to **PL Podsumowanie / ENG Overview**.  
- **Why:** Naming consistency.  
- **Do NOT touch:** The section's content/logic (its enhancement is handled in RC-01).  
- **Done when:** Section shows "Podsumowanie"/"Overview"; no "Przegląd" label remains.  
- **Risk:** Low. See OQ-5 (the PL word "Podsumowanie" is reused across Timeline and Recording — flagged).

## RN-03 · CHANGE · \[Output – Check-in\] Rename "Refleksja" → Therapy Relationship

- **Location:** Output – Check-in, "Refleksja" element.  
- **Action:** Rename to **Relacja Terapeutyczna / Therapy Relationship**.  
- **Why:** "Refleksja" already means something specific in the app; this element is really about the therapeutic relationship. Same feature as RN-01(Timeline)/RN-04/RN-05.  
- **Do NOT touch:** Content/logic — label only.  
- **Done when:** Shows the new name in both locales; no "Refleksja" label remains here.  
- **Risk:** Low.

## RN-04 · CHANGE · \[Main – Check-in\] Rename "How are you right now" → Therapy Relationship

- **Location:** Main screen — the "How are you right now" check-in.  
- **Action:** Rename to **Relacja Terapeutyczna / Therapy Relationship**.  
- **Why:** The name is misleading — this is NOT a mood/health check; it measures how healthy the user's therapeutic relationship is.  
- **Do NOT touch:** ⚠️ This feature STAYS — it is not the deleted "Check-in samopoczucia" (D-05). Content/logic unchanged; label only.  
- **Done when:** Main shows "Relacja Terapeutyczna"/"Therapy Relationship"; feature still works; no "How are you right now" label remains.  
- **Risk:** Medium — confusion with D-05; verify you're renaming the relationship check-in, not the deleted mood one.

## RN-05 · CHANGE · \[Stats\] Rename "Therapy Health Check" → Therapy Relationship

- **Location:** Stats — "Therapy Health Check".  
- **Action:** Rename to **Relacja Terapeutyczna / Therapy Relationship**.  
- **Why:** Same feature as RN-04; consistency.  
- **Do NOT touch:** Its data/logic — label only. (Note: Stats also keeps the Check-in samopoczucia endpoint per FX-03 — different thing.)  
- **Done when:** Stats shows the new name in both locales; no "Therapy Health Check" remains.  
- **Risk:** Low–Medium (naming overlap with FX-03 area).

## RN-06 · CHANGE · \[Character\] Rename "Voice AI" → Persona AI

- **Location:** Character screen — "Voice AI".  
- **Action:** Rename to **Persona AI** (PL \+ ENG).  
- **Do NOT touch:** Logic — label only. Coordinate with RN-08 (Settings "Ton AI" → Persona AI) so all three point at the same concept.  
- **Done when:** "Voice AI" reads "Persona AI"; no old label remains.  
- **Risk:** Low.

## RN-07 · CHANGE · \[Character\] Rename "How I see you" → Overview

- **Location:** Character screen — "How I see you" section.  
- **Action:** Rename to **Overview**.  
- **Do NOT touch:** Section content (its behavior changes are FX-08 and FX-09).  
- **Done when:** Section titled "Overview"; no "How I see you" remains.  
- **Risk:** Low.

## RN-08 · CHANGE · \[Settings – side drawer / Main view\] Rename "Ton AI" → Persona AI

- **Location:** Settings side drawer and Main-screen view — "Ton AI".  
- **Action:** Rename to **Persona AI** (PL \+ ENG).  
- **Why:** Same concept as RN-06.  
- **Do NOT touch:** Logic — label only.  
- **Done when:** "Ton AI" reads "Persona AI" in both places; no old label remains.  
- **Risk:** Low.

## RN-09 · CHANGE · \[Output – Recording card\] Rename "Topics with timestamps" → Main topics

- **Location:** Recording card — "Topics with timestamps" element.  
- **Action:** Rename to **Główne tematy / Main topics**. (Timestamp removal \+ reposition handled in FX-11 / RC-01.)  
- **Done when:** Element titled "Główne tematy"/"Main topics"; no old label remains.  
- **Risk:** Low.

---

# 3 · Bugs (FIX)

## BG-01 · FIX · \[Main – Latest realisation\] Truncated content

- **Location:** Main — "Latest realisation" card.  
- **Action:** Current: only the first two lines of the content show. Expected: show the full content.  
- **Done when:** The full realisation text renders on Main (no 2-line clamp).  
- **Risk:** Low.

## BG-02 · FIX · \[Main – Latest realisation\] Wrong tap target

- **Location:** Main — "Latest realisation" card tap action.  
- **Action:** Current: tapping opens the realisations **list** in Therapy Timeline. Expected: open **that specific realisation card** (view source of that entry).  
- **Done when:** Tapping the card deep-links to that specific realisation, not the list.  
- **Risk:** Low–Medium — needs the entry ID passed through navigation.

## BG-03 · FIX · \[Character\] Orka name not refreshing \+ "Mimik" in sub-name

- **Location:** Character screen — the AI character's displayed name and sub-name.  
- **Action:** Two bugs: (a) after the user changes Orka's name it doesn't refresh in the UI; (b) the sub-name shows "Mimik" (seen on several devices). Expected: name updates immediately after change; sub-name shows the correct value, not "Mimik".  
- **Done when:** Renaming the character updates the display without restart; no stray "Mimik" label; verified on multiple devices.  
- **Risk:** Medium — likely a state/cache refresh issue; check where the name is read vs. written.

## BG-04 · FIX · \[Logout\] Spinner hangs, no redirect

- **Location:** Logout button flow.  
- **Action:** Current: tapping logout shows a spinner that never resolves; app must be killed and reopened to reach login/registration. Expected: spinner briefly, then automatic navigation to the login/registration screen.  
- **Done when:** Tapping logout signs out and routes to login automatically, no manual restart.  
- **Risk:** Medium — check async gap / missing navigation after the sign-out future completes.

---

# 4 · Feature changes (FIX / adjust existing)

## FX-01 · FIX · \[Main – Next therapy session\] Remove redundant "Notes" button

- **Location:** Main — "Next therapy session" block, its "Notes" button.  
- **Action:** Remove the "Notes" button — it's a redundant duplicate of the FAB.  
- **Do NOT touch:** The FAB (which provides the same action) and the rest of the block.  
- **Done when:** No "Notes" button on the Next therapy session block; FAB still opens notes.  
- **Risk:** Low.

## FX-02 · CHANGE · \[Main – Next therapy session\] Prep-aware button state

- **Location:** Main — "Next therapy session" block button.  
- **Action:** Make the block reflect whether the user prepared for the next scheduled session. If **not** prepared: button reads **"Prepare"**. If prepared: button switches to **secondary** style and reads **"View prepcard"**, navigating to that specific prep card's results.  
- **Do NOT touch:** The scheduling logic — only the button state/label/target.  
- **Done when:** Button shows "Prepare" (primary) with no prep, and "View prepcard" (secondary) → that prep card's results once prep exists.  
- **Risk:** Medium — needs a reliable "has the user prepped for the next session?" check.

## FX-03 · CHANGE · \[Stats\] Remove Check-in samopoczucia feature, keep \+ improve its endpoint

- **Location:** Stats — "Check-in samopoczucia" feature, and the endpoint used before the symptom charts in "Trend nastroju".  
- **Action:** Remove the Check-in samopoczucia **feature/UI**, BUT **keep the endpoint** used to generate the descriptions of tracked topics shown before the symptom charts in "Trend nastroju". **Improve the prompt** in that endpoint so it suggests which activities or notes may correlate with changes in symptom intensity.  
- **Do NOT touch:** The "Trend nastroju" charts and the endpoint's wiring — keep them working; only remove the standalone feature UI and update the prompt.  
- **Done when:** Check-in samopoczucia feature UI is gone from Stats; "Trend nastroju" still renders its topic descriptions via the retained endpoint; the endpoint prompt now surfaces activity/note ↔ symptom correlations.  
- **Risk:** Medium — this is the endpoint exception to D-05; don't delete it.

## FX-04 · FIX · \[Reflect\] Don't save empty chats

- **Location:** Reflect — chat save logic.  
- **Action:** Empty chats should not be saved.  
- **Done when:** Starting and leaving a Reflect chat with no content creates no saved entry.  
- **Risk:** Low.

## FX-05 · CHANGE · \[Character\] Overview: show full text (remove chevron expand)

- **Location:** Character — "Overview" section (renamed in RN-07).  
- **Action:** Current: text expands via a chevron. Change: show the full text immediately, no expand control.  
- **Done when:** Full Overview text is visible without tapping a chevron.  
- **Risk:** Low.

## FX-06 · CHANGE · \[Character\] Overview: surface Refresh & Share as icons, remove 3-dot menu

- **Location:** Character — "Overview" section actions.  
- **Action:** Current: a 3-dot vertical menu contains Refresh and Share. Change: pull Refresh and Share out as standalone icons placed where the menu was, and **remove** the 3-dot menu icon.  
- **Done when:** Refresh and Share appear as direct icons; the 3-dot menu is gone; both actions still work.  
- **Risk:** Low.

## FX-07 · CHANGE · \[Character\] Persona AI selection opens hub-and-spoke, not Settings

- **Location:** Character — Persona AI selection (see RN-06).  
- **Action:** Current: tapping Persona AI navigates to Settings. Change: tapping opens the **hub-and-spoke** view showing **only the Persona AI options**.  
- **Do NOT touch:** The rest of Settings.  
- **Done when:** Tapping Persona AI opens hub-and-spoke limited to Persona AI choices; no jump to full Settings.  
- **Risk:** Medium — confirm the hub-and-spoke component exists / can be scoped to Persona AI options.

## FX-08 · FIX · \[Output – Recording\] Remove timestamps from topics

- **Location:** Recording output — the topics-with-timestamps element (renamed to "Main topics", RN-09).  
- **Action:** Remove the timestamps; keep the topics.  
- **Done when:** Topics show without timestamps.  
- **Risk:** Low. (Overlaps RC-01 item 6.)

## FX-09 · DELETE · \[Output – Therapy Relationship\] Remove "Tematy do rozmowy z terapeutą" (current form)

- **Location:** Output – Therapy Relationship — element "Tematy do rozmowy z terapeutą".  
- **Action:** Remove this element in its current form ("do wyjebania").  
- **Do NOT touch:** Other elements in the Therapy Relationship output.  
- **Done when:** The element is gone from the Therapy Relationship output; app builds; no dead references.  
- **Risk:** Low–Medium — confirm "in current form" means full removal here, not a redesign hold (OQ-6).

## FX-10 · CHANGE · \[Output – Therapy Relationship\] Longer, more developed Reflections

- **Location:** Output – Therapy Relationship — the "Reflections" element inside the response.  
- **Action:** Make the Reflections content longer and more developed (richer generated response).  
- **Done when:** Reflections returns a fuller, more elaborated answer than today.  
- **Risk:** Low — likely a prompt/generation change; keep format stable.

---

# 5 · Recording card — structure & order

## RC-01 · CHANGE · \[Outputs – Cards\] Reorder the Recording card and fix/remove elements

- **Location:** Recording output card element order \+ several of its elements.  
- **Action:** Set the card to this **final order** (after the deletions below):  
  1. **Overview** (PL "Podsumowanie", was "Przegląd" — RN-02) — make the summary **longer**, use **bullets**, and **reference the previous session**.  
  2. **Therapist observations** — FIX: exists on the backend but doesn't render on the frontend; make it appear (see FX/BG note below).  
  3. **Patient insights** — FIX: exists on the backend but doesn't render on the frontend; make it appear.  
  4. **Key moments** — no change.  
  5. **Action items** — move to **second-to-last**. Adapt its prompt to the prep flow (this is where therapist homework is saved / checked off).  
  6. **Main topics** (was "Topics with timestamps" — RN-09) — remove timestamps (FX-08) and move to the **very bottom / last**.  
  - **Delete from the card:** Emotional arc (D-07) and Unresolved topics \+ its endpoint (D-08).  
- **Why:** Current order is confusing; some elements are broken (not shown), some are unwanted.  
- **Do NOT touch:** The "Jak płynęła rozmowa" feature is removed separately (D-06) and is not part of this card order. Don't reintroduce Emotional arc / Unresolved topics while reordering.  
- **Done when:** The card renders in the exact order above; Therapist observations and Patient insights are visible on the frontend; Overview is longer/bulleted and references the prior session; Action items sits second-to-last; Main topics is last with no timestamps; Emotional arc and Unresolved topics are gone; app builds.  
- **Risk:** Medium–High — touches many elements at once; do the deletes (D-07, D-08) and fixes (Therapist observations, Patient insights) first, then reorder, then re-test the whole card.

**Sub-fix — Therapist observations / Patient insights (backend-visible, frontend-missing):** treat as a rendering/data-mapping bug. Confirm the backend response includes both fields, then find why the frontend drops them (missing widget, null-guard hiding them, or a parse/key mismatch). Done when both render with real backend content.

---

## Open Questions (resolve before or during execution)

- **OQ-1 — shared data on full deletes (D-01 Goals, D-03 Therapy tracking):** Default is full delete incl. data. Pause only if their data/logic is shared with a surviving feature (e.g. progress/reporting). Confirm none is before deleting models.  
- **OQ-2 — D-04 shared code:** Confirm the Main "Session preparation"/"De-brief" blocks reuse the Timeline widgets. If yes, remove only Main entry points; if separate, delete the Main ones outright.  
- **OQ-3 — D-06 downstream use:** Confirm nothing (reports, summaries, history) consumes "Jak płynęła rozmowa" output before deleting its generation logic.  
- **OQ-4 — D-08 endpoint:** Confirm the "Unresolved topics" endpoint isn't shared with another card element before removing it.  
- **OQ-5 — "Podsumowanie" reuse:** After renames, the PL word "Podsumowanie" appears both as the Recording Overview (RN-02) and near the Timeline. Confirm this isn't re-introducing the exact confusion RN-01 is meant to fix. Recommendation: keep Recording \= "Podsumowanie/Overview" and Timeline de-briefs \= "Po terapii/After therapy" (distinct enough) — confirm OK.  
- **OQ-6 — FX-09 scope:** "Tematy do rozmowy z terapeutą … w obecnej formie do wyjebania" — treated as full removal. Confirm it's not meant to return in a redesigned form (in which case keep the data).  
- **OQ-7 — Persona AI naming:** "Voice AI" (RN-06) and "Ton AI" (RN-08) both → "Persona AI". Confirm they're the same concept and should fully merge under one name/control, not two controls sharing a label.

## Suggested execution order

1. **Renames first (RN-01…RN-09)** — low risk, and they make the rest of the code easier to navigate by grep. Do the Therapy Relationship consolidation (RN-01/03/04/05) as one careful pass, watching the D-05 guardrail.  
2. **Isolated deletes** — D-02, D-01, D-03, D-04, D-05, D-06 (respect each "Do NOT touch").  
3. **Standalone bugs** — BG-01, BG-02, BG-03, BG-04.  
4. **Standalone feature changes** — FX-01…FX-07, FX-09, FX-10; FX-03 carefully (keep the endpoint).  
5. **Recording card last (RC-01)** — do its deletes (D-07, D-08) and the Therapist observations / Patient insights fixes, then reorder, then FX-08 (timestamps) and RN-02/RN-09 labels, then full re-test of the card.

