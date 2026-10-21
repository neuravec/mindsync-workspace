# MindSync Change Spec: MSV3.3 (post-release QA of 29.07.2026)

*For Claude Code · compiled 2026-08-05, v2 after author review · author: Darek (notes 29.07 \+ answer rounds 05.08) · zero open questions*

## Summary

- Total items: 23 (DELETE: 2 · FIX: 10 · CHANGE: 11\)  
- Areas touched: Main · Timeline and output cards (Preparation, After Therapy, Realizations, Recording) · Workspace (Threads, Topics & Questions) · Notifications and pop-outs · Share · Weekly/Monthly summaries  
- Intent: post-release cleanup after the MSV3.2 Fix cycle. Most of the batch falls into three groups: visual repairs on the Timeline output cards (backgrounds, nesting, sizes, spacing), a notification overhaul (broken logic, broken deep links, in-app reminders that duplicate pushes), and the app-wide reduction of "Topics & Questions" to "Questions". On top of that sits the fourth attempt at the Weekly and Monthly summary cards, which still do not work in the released build even though Fix 5 recorded them as QA-passed.

## Global guardrails (read before touching anything)

- Do NOT regress the QA-passed MSV3.2 Fix 4 and Fix 5 items: the unified thread pill design on output cards (Fix 4 CS-01) and its multi-line wrap fix (Fix 5 CS-01), the Between Sessions realization flags (Fix 4 CS-02), and the "Delete" action in the Workspace Realizations 3-dot menu (Fix 4 CS-04). Items below touch nearby UI, spacing and backgrounds included, but none of these behaviors.  
- Do NOT touch the **Goals** module. It appears below only as the design model for Workspace Threads rows (CS-15). Copy its look; change nothing in Goals itself.  
- Do NOT confuse **pop-outs** with **in-app reminders**. Pop-outs are action prompts ("how's your mood, it's been 3 days", "Add your next session date"); they stay, and CS-17 fixes their sequencing. In-app reminders are the bottom cards that today mirror system pushes; CS-20 stops that duplication but keeps the mechanism.  
- **Focus Area** is excluded as a data source in CS-13. Removing Focus Area itself is NOT in this batch, so don't delete it here.  
- The flag icon contract from Fix 2 CS-16 stands: nothing enters Workspace without a user tap, and the flag is the only save control. CS-16 below enforces it.  
- CS-23 (summaries): do NOT touch other Timeline views, existing generated cards, or the filter chips.  
- Close every item against a device build on both platforms (Fix 4 convention). After each item, run the app and confirm there are no dead references or broken navigation.

---

# A · Main

## CS-01 · CHANGE · \[Main\] · Ikona "tune" → ikona "i" (info); "edit layout" usunięty

- **Type:** CHANGE  
- **Location:** Main → top bar → right corner icon (currently the "tune" / sliders icon). Reached: open app → Main. The icon opens a view holding the screen description plus the "edit layout" mode.  
- **What it is:** The tune icon opens Main's info panel: a description of the screen and an "edit layout" capability that lets the user reorder Main's modules.  
- **Action:** Replace the "tune" icon with the "i" info icon, the same one used in the Timeline, Reflect, Workspace and Character tabs. Inside, keep only the screen description ("sam opis ekranu"). Remove the "edit layout" reordering capability entirely, "wraz z zapleczem": UI, entry points, saved layout state, persistence, backend.  
- **Logic:** "i" icon → tap → opens the same info-view pattern as the other tabs, showing only the Main screen description → close → back on Main.  
- **Outcome:** Main behaves like every other tab: an "i" that explains the screen. Module order is fixed for everyone.  
- **Value:** Consistency across tabs, and one less feature to maintain.  
- **Do NOT touch:** The info icons and views of Timeline, Reflect, Workspace, Character (they are the model, not the target); the Main modules themselves.  
- **Done when:** Main's top-right icon is the "i" info icon; its view shows only the description; no "edit layout" entry point exists anywhere; grep for the edit-layout code returns no live references; users who had a custom order see the default order (decision, flagged for veto); builds pass on Android and iOS.

## CS-02 · CHANGE · \[Main → Mood Trend\] · Ikona suwaczków → ikona ołówka (edit)

- **Type:** CHANGE  
- **Location:** Main → Mood Trend module → its edit icon (currently a sliders / "suwaczki" icon). Reached: Main → Mood Trend.  
- **Action:** Swap the sliders icon for a pencil (edit) icon rendered at min. 24 px. Behavior stays the same.  
- **Logic:** Pencil icon → tap → opens the same Mood Trend edit flow the sliders icon opens today.  
- **Do NOT touch:** Mood Trend content, narratives, AI Summary (Fix 2 CS-11 and CS-12 stand).  
- **Done when:** Mood Trend shows a pencil icon of at least 24 px that opens the existing edit flow, and the sliders icon is gone.

---

# B · Timeline and output cards: visual fixes

## CS-03 · FIX · \[Timeline → kosz\] · Wyrzucone karty wyszarzone

- **Type:** FIX  
- **Location:** Timeline ("Therapy Journey") → trash icon → trash view → the cards listed inside. Reached: Timeline → tap the trash icon.  
- **Now (wrong):** Cards thrown into the trash render greyed out ("wyszarzone"), as if they were inactive.  
- **Expected:** Trashed cards render in their default colors, the same palette they have on the Timeline.  
- **Do NOT touch:** Trash behavior itself (restore and permanent delete).  
- **Done when:** Every card type in the trash view renders in default colors on a device build.

## CS-04 · FIX · \[Timeline → Prep cards\] · Output card preparation: zagnieżdżony kontener

- **Type:** FIX  
- **Location:** Timeline → Preparation card ("Your Prep Card") → whole card body. Reached: Timeline → open any Preparation card.  
- **Now (wrong):** The container holding the prep card content (light blue background) sits inside another, larger container (white background). The nesting shows up as smaller icons, smaller text and doubled outlines.  
- **Expected:** Everything moves from the inner container into the larger white one, and the inner container is deleted. Icons, text and outlines then render at the same size as on the other output cards.  
- **Do NOT touch:** The prep card's section content and order (Fix 2 appendix layout).  
- **Done when:** The Preparation card renders as a single flat container on white, icon and text sizes match the other cards, and a device screenshot confirms it.

## CS-05 · CHANGE · \[Timeline → After therapy\] · Output card after therapy: tło na białe

- **Type:** CHANGE  
- **Location:** Timeline → After Therapy card → card background. Reached: Timeline → open any After therapy card.  
- **Action:** Remove the light blue ("jasnoniebieskie") background. The whole background becomes white. The Recording card got the same change in MSV3.2 Fix 3 CS-06; mirror it.  
- **Do NOT touch:** Card content and section order.  
- **Done when:** The After Therapy card background is white end to end on a device build.

## CS-06 · FIX · \[After therapy → to do\] · Rozmiar ikony i tytułu sekcji

- **Type:** FIX  
- **Location:** After Therapy card → "to do" section → its section icon and title. Reached: Timeline → After therapy card → scroll to the To-do section.  
- **Now (wrong):** The To-do section's icon and title render smaller than the other kind-sections on the same card.  
- **Expected:** Icon size and title size identical to the remaining categories (Topics & Questions, Threads, Realizations).  
- **Do NOT touch:** To-do section content, flags, checkbox behavior.  
- **Done when:** One screenshot shows the four kind-section headers on the After Therapy card with identical icon and title sizes.

## CS-07 · CHANGE · \[Output cards\] · Topic\&Questions i Realizations: zawsze rozwinięte, bez chevrona

- **Type:** CHANGE  
- **Location:** Noted on the After Therapy card: sections "Topic\&Questions" (after CS-11: "Questions") and "Realizations" and their collapse controls. Per the author's decision of 05.08, the same rule covers every output card: the Questions section, and Realizations wherever it appears, render expanded on all of them.  
- **Action:** Remove the collapse option together with the chevron icon. The sections render fully expanded, always.  
- **Logic:** No interactive collapse element remains; sections are open when the card opens.  
- **Do NOT touch:** The other sections; the flags inside these sections.  
- **Done when:** On every output card, both sections render expanded with no chevron and nothing can collapse them.

## CS-08 · CHANGE · \[After therapy → Threads\] · Klikalność i spacing całego feature

- **Type:** CHANGE  
- **Location:** After Therapy card → Threads section, both the view and its edit view. Reached: Timeline → After therapy card → Threads.  
- **What it is:** The card's Threads section: thread pills with a context line (unified design per Fix 4 CS-01) and an edit mode with per-thread controls and an add button at the bottom.  
- **Action, point by point:**  
  1. Pencil (edit) icon: very hard to tap because its active area is too small. Enlarge the tap target to min. 48×48 dp (decision, flagged for veto).  
  2. Edit view, "cancel" and "save" buttons: too close to each other and too close to the thread list below. Separate the buttons and add clear spacing from the list.  
  3. Link icons next to the thread list entries: remove them ("są po nic").  
  4. Red circle with a minus (the remove control): replace with a trash can icon.  
  5. The add button at the bottom, labeled "+ Add thread" (the notes wrote "+ Add topic" as shorthand; the author confirmed the real string on 05.08): too close to the content above it. Add spacing.  
  6. Then a spacing pass over the whole feature.  
- **Logic:** Pencil → tap (enlarged target) → opens the edit view as today. Trash can → tap → removes that thread from the list, exactly what the red minus did. Cancel → discards edits. Save → persists edits. "+ Add thread" → unchanged behavior.  
- **Outcome:** The Threads edit flow becomes comfortable to use with a thumb, with room between every control.  
- **Value:** "Ikona ołówka edit jest bardzo trudna do tapnięcia." The edit flow frustrates on a phone today.  
- **Do NOT touch:** The thread pill design and multi-line wrap (Fix 4 CS-01 and Fix 5 CS-01, both QA-passed); flag behavior on threads.  
- **Done when:** All six points are visibly fixed on a device build; pencil, cancel, save and trash targets are comfortably tappable; the pill layout shows no regression.

## CS-09 · CHANGE · \[Timeline → Realizations\] · Output card realizations: tło na białe

- **Type:** CHANGE  
- **Location:** Timeline → Realization card → card background. Reached: Timeline → open any Realization card.  
- **Action:** Remove the blue background; the card becomes white, the same move as CS-05.  
- **Do NOT touch:** Card content, "View Source", "Remove Realization".  
- **Done when:** The Realization card background is white on a device build.

## CS-10 · FIX · \[Timeline → Recording card\] · Czas trwania nagrania "z dupy"

- **Type:** FIX  
- **Location:** Timeline → Recording card (the card chrome shows "Date · duration · Share") → the duration value. Reached: Timeline → any Recording card.  
- **Now (wrong):** The displayed duration is wildly wrong. A recording of about 11 minutes shows as 206 min.  
- **Expected:** The duration on the Timeline card equals the real length of the saved recording. Root cause unknown; 11 → 206 matches no clean unit conversion, so trace the value from the recording's source metadata through to the card instead of assuming a formatting slip.  
- **Do NOT touch:** The recording itself, its processing, the open card view.  
- **Done when:** For at least two real recordings, the Timeline card duration matches the actual recording length to the minute, on both platforms.

---

# C · "Topics & Questions" → "Questions" (app-wide)

## CS-11 · CHANGE · \[App-wide: output cards \+ Workspace\] · Topics znikają; zostaje "Questions"

- **Type:** CHANGE  
- **Location:** Every place the section appears: Prep card, Between Sessions card, Recording card, After Therapy card (on the Timeline and inside the app), plus the Workspace module "Topics & Questions". The build shows the section title in several spellings ("Topics & Questions", "Topic\&Questions", "topics in questions"); catch all variants, not one string.  
- **What it is:** Today the section holds topic pills plus three selectable questions (flat list, max 3 \+ 3, per Fix 3 CS-01). The Workspace module collects both flagged topics and flagged questions.  
- **Action:**  
  1. On every output card the section becomes "Questions". Topics disappear from the title and from the feature itself: the topic pills are removed and only the three selectable questions remain.  
  2. In Workspace the module is renamed from "Topics & Questions" to "Questions", and from now on it accepts only questions.  
  3. Existing saved topics (decision 05.08): they stay visible in the module until the user deletes them himself, but no new topic can be saved from any card. Keep only the backend needed to display and delete legacy topic rows; remove topic generation and topic flagging from the cards.  
- **Logic:** Flag on a question → saves to Workspace → "Questions" (routing per Fix 2 CS-04, unchanged for questions). Legacy topic row in Workspace → its existing controls keep working until the row is gone.  
- **Outcome:** One concept remains: questions to bring to therapy. Topic pills are gone from the whole app.  
- **Value:** Cuts a duplicated concept and simplifies the section on all four cards.  
- **Do NOT touch:** Threads pills (they look similar but are a different feature); the "Next session agenda" module; the generation of the three questions itself.  
- **Done when:** No output card shows a topic pill or any title variant containing "Topics"; the Workspace module is named "Questions" and accepts only questions; legacy topics still render and can be deleted; grep finds no live topic generation or flagging path; both platforms.

## CS-12 · CHANGE · \[Output cards\] · Wygląd sekcji Questions zunifikowany; wzór: Prep Card

- **Type:** CHANGE  
- **Blocked by:** CS-11  
- **Location:** The "Questions" section (formerly Topics\&Questions) on all output cards: Prep, Between Sessions, Recording, After Therapy.  
- **Action:** Each card currently renders the section a little differently. Unify to one look on every card, with the current Prep Card rendering as the model ("najlepiej wygląda Prep Cards — może być wzorem"). The unification covers behavior too: per CS-07, the section is always expanded, on every card.  
- **Do NOT touch:** The Prep Card version (it is the reference); section content.  
- **Done when:** Side-by-side screenshots of the four cards show an identical Questions section: typography, spacing, rows, flags, and no collapse control.

---

# D · Prep card content

## CS-13 · CHANGE · \[Prep card → "Your Mood This Week"\] · 1:1 z Mood Trend

- **Type:** CHANGE  
- **Location:** Preparation card → section "Your Mood This Week". Reached: Timeline → Prep card, or Main → Your Session → "View prep card".  
- **What it is:** The prep card's mood section. Today it mixes in other data, including data from Focus Area.  
- **Action:** The section becomes a direct reflection of what the user tracks in Mood Trend on Main: the tracked symptoms and items appear as a copy, together with an analysis of the specific period the prep card covers ("tak żeby to było w jednym miejscu"). Per the author's answer of 05.08 this means the symptom list plus the period analysis, without copying the charts or score visualizations from the Mood Trend module. The section must not contain other data from Focus Area. Focus Area itself is slated for removal later and stays untouched in this batch.  
- **AI:** Input: the user's Mood Trend tracked symptoms and their data for the period since the last session. Output: the tracked items with a short qualitative analysis of that period, in the same narrative style and pipeline as the Mood Trend per-symptom narratives (Fix 2 CS-11: direction plus reason, no digits; compiler call, flagged for veto). Trigger: prep card generation. Failure: the same in-card failure behavior as the card's other AI sections.  
- **Outcome:** What the user tracks in Mood Trend is exactly what they see, analyzed, when preparing for a session.  
- **Value:** One source of truth for mood, and no stale Focus Area data leaking into session prep.  
- **Do NOT touch:** Mood Trend on Main; Focus Area itself.  
- **Done when:** For a user with N tracked items in Mood Trend, the prep card section lists exactly those N items with a qualitative period analysis; no charts, no scores, no Focus Area data; device check.

---

# E · Workspace → Threads

## CS-14 · DELETE · \[Workspace → Threads\] · Obrazek typu notatki źródłowej

- **Type:** DELETE  
- **Location:** Workspace → Threads module → per-thread element: the image indicating which note type the thread's latest information came from.  
- **Action:** Remove only this graphic representation of the source. The rest of the feature stays as it was; the context with features remains.  
- **Do NOT touch:** The context text itself; thread data; the source attribution stored in the backend (only its graphic rendering goes).  
- **Done when:** No source-type image renders anywhere in the Threads module and the context text is unchanged.

## CS-15 · CHANGE · \[Workspace → Threads\] · Trzy widoczne wątki, wiersze 1:1 jak w Goals, bez rozwijania

- **Type:** CHANGE  
- **Location:** Workspace → Threads module → the thread list. Reached: Workspace → Threads.  
- **What it is:** Today threads render as expandable rows: a chevron opens an expansion that holds a circular diagram and the actions.  
- **UI anatomy (target, per row, top to bottom):**  
  1. Line 1: full title (like in Goals)  
  2. Below: context text (like in Goals)  
  3. 3-dot menu, placed wherever Goals places its row menu. Per the author's answer of 05.08, copy the Goals row design 1:1: where Goals puts a menu or action, the thread row puts the same.  
- **List behavior:** 3 newest threads visible immediately ("trzy threadsy z kontekstem i pełnym tytułem widoczne od razu"); the rest sit behind the Workspace expand pattern ("Pokaż więcej", decision 05.08). Newest on top, per Fix 2 CS-05.  
- **Action:**  
  - Remove the chevron. Threads are no longer expandable.  
  - Remove the circular diagram that lived in the expansion.  
  - Move into the 3-dot menu: "Add to agenda", "Mark as done" (the notes wrote "mask as done"; read as a typo for the existing action), "Delete".  
- **Logic:**  
  - 3-dot → tap → menu with the three actions.  
  - "Add to agenda" → adds the thread to Next session agenda (existing behavior, relocated).  
  - "Mark as done" → closes the thread and moves it to the Closed threads archive (existing semantics, Fix 2 CS-07).  
  - "Delete" → removes the thread (existing delete semantics).  
  - "Pokaż więcej" → shows the list beyond the first 3; "Pokaż mniej" collapses it back.  
- **Outcome:** A compact Threads module: three rows with full titles and context, one menu per row, and no expansion layer.  
- **Value:** The expansion and its diagram added depth without value; the Goals row pattern already works.  
- **Do NOT touch:** The Goals module (design source only); thread statuses open / worked on; the Closed threads archive; threads on output cards (their design is Fix 4 CS-01 and stays).  
- **Done when:** Workspace Threads shows max 3 rows by default, copied 1:1 from the Goals row design; no chevron, no expansion, no diagram; all three actions work from the 3-dot menu; "Pokaż więcej" reveals the rest; device check.

---

# F · Realizations entry path

## CS-16 · DELETE · \[Output cards, wszystkie z flagowaniem\] · Tap-and-hold "mark as realization"

- **Type:** DELETE  
- **Location:** Every output card element that can be flagged to Workspace. Observed on After Therapy → Realizations, but the duplication exists wherever flagging exists. The duplicate path: tap and hold an element → a sheet slides up from the bottom with "mark as realization" → the element gets a category tag "Realizations x".  
- **Action:** Remove the tap-and-hold path "całkowicie wraz z zapleczem": the long-press gesture handler, the bottom sheet "mark as realization", and the "Realizations x" category tags on elements. The flag icon remains the only way to add elements to Workspace, on all elements of all output cards.  
- **Do NOT touch:** The flag icon and its contract (tap saves, tap again withdraws, per Fix 2 CS-16); realizations already saved in Workspace.  
- **Done when:** Long-pressing any card element produces nothing; the "mark as realization" sheet and the "Realizations x" tags are gone; flagging still works everywhere it did; grep for the long-press code returns no live references.

---

# G · Notifications and pop-outs

## CS-17 · FIX · \[App-wide → pop-outs\] · Pop-out przerywa akcję poprzedniego pop-outu

- **Type:** FIX  
- **Location:** App launch flow → pop-out queue. Repro (seen on iOS; fix both platforms, decision): open app → pop-out "how's your mood, it's been 3 days" → tap → user lands on the card → a second pop-out, "Add your next session date", opens immediately on top.  
- **Now (wrong):** An action started from one pop-out gets interrupted by the next pop-out.  
- **Expected:** The action from a pop-out must finish before the next message may appear. Queue pop-outs: the next one shows only after the flow started from the previous one is completed or dismissed.  
- **Do NOT touch:** The individual pop-outs' content and triggers; system pushes.  
- **Done when:** With two pending pop-outs, the second never appears until the flow from the first is done; verified on device, Android and iOS.

## CS-18 · FIX · \[Notifications\] · "Brak kolejnej sesji" ignoruje custom date

- **Type:** FIX  
- **Location:** The logic behind the "no next therapy session added" notification. It fires today on both surfaces, the system push and the in-app reminder; fix the logic itself, regardless of surface (after CS-20 the in-app copy of a pushed message goes away anyway).  
- **Now (wrong):** The notification claims no next session is set even though one exists. The session was added as a custom date, a one-off entered because of a two-week gap while the therapist is on holiday, not as a weekly or biweekly recurring session.  
- **Expected:** The logic recognizes weekly, biweekly and custom session dates. If any upcoming session exists, recurring or custom, the notification does not fire.  
- **Do NOT touch:** The set-therapy hub-and-spoke (date, time, cadence); other notifications.  
- **Done when:** With only a custom future session date set, no "no next session" notification fires on any surface; with genuinely no session set, it still fires; device check.

## CS-19 · FIX · \[Notifications\] · "Open Card" → pasek stats → "Page Not Found"

- **Type:** FIX  
- **Location:** The reminder that the user hasn't added a note in a while (in the author's words: "GORG przypomina mi, iż dawno nie dodałem żadnej notatki"; description, not a verbatim UI string) → its card → "Open Card" button → target screen. Repro: tap "Open Card" → a bar appears at the top of the screen with stats along the lines of "50% of sessions land on Thursdays" → tap "See Stats" → "Page Not Found". The bug clears after an app reload.  
- **Now (wrong):** Notification routing leaks an unrelated stats bar into the target screen, and the bar's "See Stats" link routes to a page that does not exist.  
- **Expected (decision 05.08):** Investigate and fix the notification routing, and remove the stats bar from this flow entirely. The notification leads straight to its target card. "Page Not Found" must never be reachable from a notification.  
- **Dependencies:** CS-20 stops in-app duplication of pushed messages, so this flow's remaining entry point is the system push tap. The routing fix must hold for it.  
- **Do NOT touch:** The note-adding card itself; the stats feature in its own proper location.  
- **Done when:** Tapping the note reminder always lands on the target card, with no stats bar and no route to "Page Not Found", reproduced clean on device without a reload.

## CS-20 · CHANGE · \[Notifications\] · In-app reminders przestają dublować pushe; mechanizm zostaje

- **Type:** CHANGE  
- **Location:** App-wide → the in-app reminder card ("ta karta z dołu") that today appears in addition to the system notification carrying the same message.  
- **Action (author's correction, 05.08, second round):** In-app reminders must stop duplicating notifications that already arrive as system pushes. Any message delivered as a push renders no in-app card. The in-app reminder mechanism itself stays in place, kept as a channel for other uses; those uses are deliberately not defined in this batch (decision). Until they are, the channel simply shows nothing.  
- **Logic:** Notification fires → delivered as system push only → tap on the push deep-links to the target card. No in-app card appears for it.  
- **Outcome:** The user gets each message once, as a push, and the in-app channel is free for future purposes.  
- **Value:** Ends the double delivery that today shows the same message twice.  
- **Do NOT touch:** System pushes and their content; pop-outs (CS-17), which are action prompts and stay; conditional banners inside cards (quality and safety banners); the in-app reminder mechanism's code (it stays, unused for now).  
- **Done when:** No message that goes out as a push also renders an in-app card, anywhere in the app; pushes still arrive and deep-link correctly; the in-app reminder mechanism still exists in code and can be pointed at new content later.

## CS-21 · FIX · \[Notifications\] · Audyt wszystkich nowych notyfikacji: logika \+ deep linki

- **Type:** FIX  
- **Blocked by:** CS-18, CS-19, CS-20  
- **Location:** Every notification in the app. No prior spec enumerates them, so the audit covers all of them (decision, flagged for veto).  
- **Now (wrong):** The new notifications misfire and do not reliably lead anywhere useful. CS-18 and CS-19 are the two caught examples.  
- **Expected:** For every notification: the occurrence logic is correct, so it fires when its condition is truly met and never otherwise; tapping it leads to its target card ("prowadzi do karty docelowej"); the content motivates the user to take that specific activity; and per CS-20, none of it duplicates into the in-app channel.  
- **Done when:** A written checklist enumerates every notification with its trigger condition and target destination, and each entry is verified on a device build on both platforms: fires correctly, deep-links to the target card, no dead ends, no in-app duplicate.

---

# H · Share

## CS-22 · FIX · \[App-wide → Share\] · Share wysyła kawałek karty zamiast całości

- **Type:** FIX  
- **Location:** Every existing "share" button on the output cards and anywhere else share exists in the app. Known bad example: After Therapy card → Share → the shared image is a screenshot of the top of the app, which drops about two thirds of the card.  
- **Now (wrong):** Share exports a viewport screenshot instead of the card.  
- **Expected:** Every existing share button generates a JPEG containing the entire output card, or the entire feature it belongs to, in its current form: full height, all sections, nothing cut off. This item verifies and fixes the buttons that exist; it adds no new share buttons.  
- **Do NOT touch:** What is shareable and where the buttons live. Only what they export changes.  
- **Done when:** Every share location in the app is checked on device on both platforms, and each exported JPEG shows the complete content of its card or feature.

---

# I · Weekly and Monthly summaries

## CS-23 · FIX · \[Timeline\] · Weekly and monthly summary cards: still absent, fourth attempt

- **Type:** FIX · **Priority: Highest in this batch.**  
- **Re-work of:** MSV3.2 Fix 4 · CS-03 ← MSV3.2 Fix 3 · CS-08 ← MSV3.2 Fix 2 · CS-13 ← Fix 1.3 · CS-21. Fix 5 (24.07) recorded this as QA-passed; the author's post-release notes of 29.07 order a redo, and the 29.07 finding supersedes. "Please this time develop this functionality and make it work." (Darek)  
- Do not treat Fix 1.3 CS-21's generation mechanisms (auto-generate at period end, the "Generate Now" button, an in-card error state instead of a raw 500\) as already built. Darek confirmed on 23.07 that nothing was ever built behind the UI, so those mechanisms are inside this item's scope.  
- **Location:** Timeline ("Therapy Journey") → the Weekly and Monthly views → the summary card. Reached: Timeline → filter Weekly or Monthly.  
- **What it is:** Two card types generated automatically, one after each week and one after each month: the period summary built from the app's overall data, covering what the user raised in therapy and in their notes and where they progressed on goals and symptoms. Shown in the Timeline only for now (Darek).  
- **Now (wrong):** The Weekly and Monthly views exist only as a shell. A "Generate Now" button is visible, but there is no feature behind it: tapping it returns a raw 500 and no card, and no card has ever auto-generated. ("This feature was never built. It was just visible on the timeline. There is a button for Generate Now, but it never did anything. There was a 500 error on that." Darek, 23.07.)  
- **Expected:** One card per period: a descriptive part on top plus the period's most important items grouped into fixed categories. This item builds the feature end to end: the generation pipeline for both period types, the automatic trigger at period end, the wiring of the existing "Generate Now" button, and the in-card error state with retry in place of the raw 500\.  
- **Period definition (decision, 23.07):** A week is the calendar week, Monday through Sunday; a month is the calendar month; both in the user's timezone. Auto-generation fires once the period is over; the exact fire moment within the following day is the implementer's call (logged).  
- **Backfill (decision, 23.07):** None. Periods that ended before the rollout get no cards ("don't bother going back", Darek). The first cards appear at the first period end after the rollout, which covers the week or month already in progress when the feature ships.  
- **UI anatomy (target, top to bottom):**  
  - Weekly summary:  
    1. Period header (chrome)  
    2. Descriptive part  
    3. What you worked on: themes from sessions and notes  
    4. How you felt: symptom and mood movement, qualitative, per the Global content rule  
    5. What you got done: homework, to-dos, goal progress  
  - Monthly summary:  
    1. Period header (chrome)  
    2. Descriptive part  
    3. What you worked on  
    4. How you felt (qualitative, Global content rule)  
    5. What you got done  
    6. Realizations & breakthroughs  
    7. Where your goals stand: goal progress over the month  
- Keep the structure plain: a short descriptive paragraph, then the categories, each with its few most important elements. A category with nothing behind it in the period is omitted rather than padded (Fix 2 decision). These cards are reference-only and carry no flag icons. The no-digits rule binds "How you felt" only; the descriptive part, "What you got done" and "Where your goals stand" may cite counts such as goal progress, consistent with the Goals module's numeric narrative (compiler call, flagged for veto).  
- **AI:** Input: the period's app data (entries, cards, scores, homework and work done, goals). Output: one card per period, descriptive part plus the categories above, oriented to what the user actually did and how they progressed. Trigger: automatic at period end plus manual "Generate Now". Failure: the in-card error state with retry, never a raw 500\.  
- **Outcome:** The user opens Timeline and reads, per week and per month, what they worked on, how they felt, and what got done.  
- **Value:** The summaries answer the user's core question about their therapy: what has actually been happening, and is it moving.  
- **Do NOT touch:** Other Timeline views; existing cards; the filter chips.  
- **Done when:** On a device build, both platforms: summary cards actually render in the Weekly and Monthly views; a generated weekly card shows the description plus its 3 categories and a monthly card its 5; content covers therapy topics, note topics, and goal and symptom progress; the "How you felt" part contains no dates or scores; empty categories are absent; "Generate Now" produces a card or the in-card error with retry, never a raw 500; auto-generation fires at the first period end after rollout (calendar week Monday to Sunday, calendar month, user's timezone); no cards appear for periods that ended before the rollout.

---

