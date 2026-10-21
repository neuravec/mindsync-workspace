# **MindSync Change Spec: MSV3.2 Fix 3 (QA pass of 22-23.07.2026) \- MSV3.2 Fix 2 review**

*For Claude Code · 2026-07-23 · author: Darek (notes \+ answers), compiled with zero open questions*

## **Summary**

* Total items: 8 (DELETE: 1 · FIX: 3 · CHANGE: 4\)  
* Areas touched: Preparation card · question generation (app-wide) · Between Sessions card · Recording card · Main (Your Session) · Timeline (weekly and monthly summaries)  
* Sources: this batch is the QA pass over **MSV3.2 Fix 2**. Fix 2 reused CS numbers from earlier batches, so this document assigns fresh IDs again; every item carries a **Re-work of** pointer to its Fix 2 source. Everything Fix 2 shipped that QA passed stays untouched; this document carries only what is still wrong plus the new simplifications from the notes.  
* Intent: two specced pieces still do not work (the Your Session state chain on iOS, the weekly and monthly summary cards, which never made it into the build), the Between Sessions card is missing its realization flags, and the Preparation card gets one more round of simplification: a flat Topics & Questions list, thread pills, and a humanized Patterns narrative. On top of that, the Wildcard question kind leaves the app entirely and the Recording card goes white.

## **Global guardrails (read before touching anything)**

* This is a QA re-work batch on live items. Touch only what is listed here. Do not re-open or regress anything QA left alone.  
* Confirmed OK in the 22-23.07 review, do NOT change: the **After therapy** card, the standalone **Realization (auto-detected)** card, the **Therapy Relationship check-in** card, and the **Between Sessions** card apart from the missing flags in CS-05. "Is ok, do not change" (Darek) covers their section order, content, and behavior.  
* The **section order of every card type stays exactly as the Fix 2 appendix**. This batch changes what renders inside sections, never their order. The only whole-card visual change is the Recording background (CS-06).  
* The four Workspace names and the flag contract from Fix 2 (CS-02, CS-04, CS-16) stand: the flag icon saves an item to its named Workspace module, tap again withdraws it, and nothing enters Workspace without a user tap. CS-01, CS-02, and CS-05 change what renders or add missing flags; none of them change the mechanics or the routing.  
* Triage never deletes content: flagged or not, every item stays on its card on the Timeline ("nic nie ginie").  
* UI strings ship in English; AI-generated content follows the language of the user's own data.  
* After each item: run the app on Android and iOS, confirm no dead references and no broken navigation.

## **Global content rule for AI narratives (carried from Fix 2; applies to CS-03 and to CS-08's "How you felt")**

* Say whether something improved or worsened and how strongly, in qualitative words.  
* Say WHY, using the user's own app data: entries, actions, behaviors, context, history. Direction plus reason, always both.  
* Plain, blunt language. Short, dense sentences.  
* Banned outright: dates, score numbers, point deltas, digits of any kind, symptom-history recitals, and "add a note" style suggestions.

---

## **A · Preparation card ("Your Prep Card")**

### **CS-01 · CHANGE · \[Preparation card\] · Topics & Questions: one flat list, max 3 topics \+ 3 questions, nothing else**

* **Type:** CHANGE

* **Re-work of:** MSV3.2 Fix 2 · CS-02 (action 2\) and appendix 2.3, which carried the former Suggested Agenda items plus all 8 questions with their Targeted / General / Wildcard groups and rationale into this section. QA: still too heavy.

* **Location:** Preparation card ("Your Prep Card") → section **"Topics & Questions"** (third section, directly after Summary) → the whole section body and its generation. Reached: Timeline → open a Preparation card, or generate one. Lead: grep the group header strings "Targeted", "General", "Wildcard" and the per-question rationale rendering in this section's widget.

* **What it is:** The flaggable section that feeds Workspace Topics & Questions before a session. Today it renders agenda items plus 8 questions in three labeled groups, each question with a rationale line.

* **UI anatomy (target, top to bottom):**

  * Section header **"Topics & Questions"** (string unchanged, per Fix 2 CS-02).  
  * Up to 3 **topics**: short pills, title only, no description and no subtext, the same pill pattern Threads uses. Flag icon per pill.  
  * Up to 3 **questions**: one line each, the bare question, no rationale and no explanatory subtext. Flag icon per question.  
* One flat list: no group subheaders, no Targeted / General / Wildcard labels, no split into separate topic and question blocks. Topics render before questions (kept from the current layout order; decision).

* **Logic:**

  * Flag on a topic or question → tap → saved to Workspace **Topics & Questions** (routing per Fix 2 CS-04), row lands on top per Fix 2 CS-05 → tap again → withdrawn.  
  * No material → the section renders its one-line info state per the Fix 2 empty-kind rule: "No topics or questions found this week."  
* **AI:** Input: the prep card's existing generation inputs, unchanged. Output: at most 3 topics as short titles and at most 3 questions of the former Targeted kind, phrased as plain questions; the schema carries no group labels, no rationale field, and no General or Wildcard output. Pull the current generation prompt from the codebase and rewrite it in full against these limits. Trigger and failure: the card's existing behavior.

* **Action:** From: agenda items \+ 8 grouped questions with rationale. To: the anatomy above. The General questions go away with their group (Darek: "usuń zupełnie sekcję General questions. Zostaw tylko Targeted"); the Wildcard kind is removed app-wide by CS-04. Historical Preparation cards render through the new flat layout too: group labels and rationale stop rendering, all stored items still show, and the 3+3 cap applies only to newly generated cards (decision, flagged for veto).

* **Outcome:** The user opens the prep card and scans at most six short flaggable rows: up to 3 topic pills, then up to 3 bare questions.

* **Value:** "Needs to be simplified even more. Topics & Questions must be max 3 topics and 3 questions in total." (Darek) The grouped 8-question block was still too heavy to read before a session.

* **Do NOT touch:** The section header string and its flag routing; the other Preparation sections; the Supporting questions list in the prep input flow (Fix 2 CS-01 scope, a different surface); existing Workspace rows.

* **Done when:** A newly generated Preparation card shows at most 3 title-only topic pills and at most 3 bare questions in one flat list with no group labels and no rationale; grep for "Targeted" and "General" returns no live reference on this card ("Wildcard" is CS-04's app-wide check); every row flags to Workspace Topics & Questions and withdraws on the second tap; the empty info line still renders on a thin card; historical cards show no group labels; both platforms.

### **CS-02 · CHANGE · \[Preparation card\] · Threads: thread pills only, same look and behavior as After Therapy**

* **Type:** CHANGE  
* **Re-work of:** MSV3.2 Fix 2 · appendix 2.5 (Threads on Preparation: the merged former UNFINISHED BUSINESS \+ NEW DEVELOPMENTS content).  
* **Location:** Preparation card ("Your Prep Card") → section **"Threads"** (fifth section) → the section body and its generation. Reached: Timeline → open a Preparation card. Lead: the Threads section on the After therapy card is the reference; grep that widget and prefer reusing it here over keeping a separate copy.  
* **What it is:** The flaggable section that feeds Workspace Threads. On After therapy every thread is a short pill with a flag. On Preparation the same section still renders the merged material as longer flaggable text.  
* **Action:** From: long-text flaggable items. To: identical rendering and behavior to After therapy's Threads. Each thread is one short pill, title only, flag icon per pill. The descriptive texts leave the section; the merged UNFINISHED BUSINESS \+ NEW DEVELOPMENTS material stays only as the source the pills are generated from (decision).  
* **Logic:**  
  * Flag on a pill → tap → saved to Workspace **Threads**, row on top per Fix 2 CS-05 → tap again → withdrawn.  
  * No material → "No threads found this week." per the empty-kind rule.  
* **AI:** Input: unchanged (the merged since-last-session material). Output: one short thread title per thread, phrased like the After therapy thread pills; no descriptive body text in this section's schema. Trigger and failure: the card's existing behavior.  
* **Outcome:** Prep Threads scans exactly like After therapy Threads: a pill per thread, flag it or not, done.  
* **Value:** "Jest krótsze i lepiej się odznacza. Ma wyglądać i zachowywać się tak samo." (Darek)  
* **Do NOT touch:** The Threads section on After therapy (it is the reference, not a change target); Between Sessions Threads; Workspace Threads and its status logic (Fix 2 CS-07); the section's content sources.  
* **Done when:** Side by side, the Preparation and After therapy Threads sections look and behave the same; every thread on Preparation renders as one title-only pill with a working flag; no descriptive thread text renders in the section; both platforms.

### **CS-03 · CHANGE · \[Preparation card\] · Patterns: up to 3 humanized recognitions, no numbers (redo)**

* **Type:** CHANGE  
* **Re-work of:** MSV3.2 Fix 2 · CS-18 (action 2), which merged "Your Patterns This Week" \+ "THINGS TO NOTICE" into **"Patterns"** and specced it qualitative, no digits. QA: the live narrative still leans on numbers and raw data.  
* **Location:** Preparation card ("Your Prep Card") → section **"Patterns"** (seventh section) → the narrative content and its generation prompt. Reached: Timeline → open a Preparation card → Patterns.  
* **What it is:** The reference-only reading section about the user's week. No flags; it exists to be read.  
* **Now (wrong):** The narrative includes a lot of numbers and raw data and reads like a data recital instead of insight. (Darek, notes of 23.07.)  
* **Expected:** Up to 3 recognitions, the most important ones, written as approachable, humanized insights: direction plus reason from the user's own data, per the Global content rule. Each recognition runs 1 to 2 sentences (decision). No dates, no scores, no digits, no raw-data recitals.  
* **Action:** Pull the current generation prompt from the codebase and rewrite it in full against the rule above. Cap the output at 3 recognitions.  
* **AI:** Input: unchanged (the week's pattern material). Output: at most 3 short qualitative recognitions in the user's language. Trigger and failure: the card's existing behavior.  
* **Outcome:** The user reads at most three plain-language recognitions about their week instead of a block of numbers.  
* **Value:** "The AI narrative should be more approachable and humanized. Now it includes a lot of numbers and raw data. Instead, text should be insightful recognitions. Up to 3 most important." (Darek)  
* **Do NOT touch:** The section's name and position (Fix 2 CS-18); **Your Mood This Week** right below it (the score readout keeps its numbers, protected per Fix 2); the Mood Trend narratives on Main (Fix 2 CS-11 and CS-12 scope, separate prompts).  
* **Done when:** Spot-checked on an account with data: Patterns shows at most 3 recognitions, each naming a direction and a because, with no date, score, or digit anywhere in the section; the prompt enforces the same; both platforms.

---

## **B · Question generation (app-wide)**

### **CS-04 · DELETE · \[App-wide\] · The Wildcard question kind, everywhere**

* **Type:** DELETE  
* **Re-work of:** MSV3.2 Fix 2 · CS-02 (action 2\) and appendix 2.3, which carried the Wildcard group into the Preparation card's Topics & Questions.  
* **Location:** Every surface and every generation path that produces, tags, or renders "Wildcard" questions. Known live spot: Preparation card → Topics & Questions → the Wildcard question group (its rendering is already removed by CS-01's flat layout). Reached: Timeline → open a Preparation card. Lead: repo-wide case-insensitive grep "wildcard" across UI strings, prompts, and generation schemas.  
* **Action:** Full removal, UI and supporting logic: the group label, the wildcard question generation (prompt text and schema fields), and any wildcard-tagged handling anywhere else grep finds it ("Wherever it is", Darek). If the prep input flow's Supporting questions list carries wildcard-tagged proposals, they fall under this delete too. Stored historical data may remain; it just never renders or generates again (the same render-time approach Fix 2 used for renames; decision, flagged for veto).  
* **Do NOT touch:** The former Targeted-kind questions that remain as CS-01's 3 bare questions; the Supporting questions list beyond wildcard-tagged entries; unrelated grep hits outside the questions domain (check before deleting).  
* **Done when:** Case-insensitive repo grep "wildcard" returns no live UI string, prompt line, or schema field in the questions domain; no card, new or historical, renders a Wildcard label or a wildcard-kind question; the app builds and runs on both platforms.

---

## **C · Between Sessions card**

### **CS-05 · FIX · \[Between Sessions card\] · Realizations: the per-statement flags are missing**

* **Type:** FIX  
* **Re-work of:** MSV3.2 Fix 2 · CS-02 (action 3, Realizations as a flaggable section on this card) \+ CS-16 (the modules fill only through flags).  
* **Location:** Between Sessions card → section **"Realizations"** (sixth section) → the per-statement flag icon. Reached: Timeline → open a Between Sessions card whose note produced detected realizations. Lead: the flag control the other kind-sections use; grep the Realizations section widget on the Between Sessions card.  
* **Now (wrong):** The Realizations statements on the Between Sessions card render with no flag to tap, so the user cannot send one to Workspace from this card. ("In between sessions Realisations nie posiadają flagi do zaznaczenia." Darek.)  
* **Expected:** Flag per statement, like every other kind-section. Only a flagged realization lands in Workspace → Realizations ("Tylko zaznaczenie powinno sprawiać, że dana realizacja trafia do Workflow \- realisation", read as Workspace → Realizations; decision). All detected realizations keep landing on the Timeline as standalone Realization cards regardless of flag state; that already works and stays ("Na timeline trafiają normalnie wszystkie").  
* **Logic:**  
  * Flag on a realization statement → tap → row at the top of Workspace **Realizations** with its source tag (per Fix 2 CS-05 and CS-16) → tap again → withdrawn.  
  * No flag → no Workspace row, ever (the CS-16 contract).  
  * Flag state has no effect on the standalone Timeline Realization cards.  
* **Do NOT touch:** The detection and its quality; the standalone Realization (auto-detected) card, which carries no flag by decision (Fix 2 CS-16); every other section of the Between Sessions card ("is ok, do not change", Darek); the Realizations sections on the other card types where the flag already works.  
* **Done when:** On a Between Sessions card with detected realizations, every statement shows the flag icon; flagging creates the Workspace Realizations row and unflagging removes it; nothing enters the module without a tap; the standalone Timeline cards still appear for every detection; both platforms.

---

## **D · Recording card**

### **CS-06 · CHANGE · \[Recording card\] · Card background: light blue → white**

* **Type:** CHANGE  
* **Re-work of:** none; new in the notes of 23.07. Extends the white standard Fix 2 CS-08 set for To-do rows.  
* **Location:** Recording card → the card surface behind all sections. Reached: Timeline → open a Recording card. Lead: grep the light blue fill color or token on the Recording card container.  
* **What it is:** The Recording output card. Its container currently sits on a light blue fill while the app's feature surfaces are white.  
* **Action:** From: light blue card background. To: white, unified with the feature background. Scope: the Recording card container only (decision).  
* **Outcome:** The Recording card reads on white like the rest of the app.  
* **Value:** "The background of the card must be unified to white → change light blue background to white." (Darek)  
* **Do NOT touch:** The Recording card's section order and content (confirmed as the Fix 2 appendix); quality banners; the backgrounds of the other card types.  
* **Done when:** The Recording card renders on a white background on both platforms, screenshot-checked; no light blue fill remains on its container.

---

## **E · Main**

### **CS-07 · FIX · \[Main → Your Session\] · State machine: unstick the post-debrief flow, add the Between Sessions window (iOS re-do)**

* **Type:** FIX  
* **Re-work of:** MSV3.2 Fix 2 · CS-09, itself a re-work of Fix 1.3 · CS-09. QA 22.07: still broken on iOS. The whole item is to be redone on iOS; Android works and gets a regression pass only (decision, 23.07).  
* **Location:** Main → module 1 **"Your Session"** → the state-dependent button and its transitions. Reached: open Main. Lead: grep the module title "Your Session" and the button strings "Prepare", "View prep card", "Debrief", "Between Sessions", "After Therapy".  
* **What it is:** The countdown module that walks the user through the session cycle with one button.  
* **Now (wrong):**  
  * \[iOS\] After the session the button reads "Debrief" (correct entry point). The debrief was then completed from the FAB and again from Your Session, and the button still read "Debrief". The module never advances. (Darek, 22.07.)  
  * The "Debrief" label itself is stale: the feature is named **After Therapy** everywhere now; "Debrief" was its previous name (decision).  
  * There is no "Between Sessions" state at all: nothing prompts the user to add between-session notes after a completed debrief.  
* **Expected (target chain, in order):**  
  * No therapy set → button opens the hub-and-spoke to set therapy (date, time, cadence, with whom); writes the same fields as settings.  
  * Session upcoming, no prep done → button **"Prepare"**.  
  * Prep done, session upcoming → button **"View prep card"**, flipping immediately after the prep card is created, with no latency.  
  * Session start time reached → button **"After Therapy"** (opens the debrief flow; no "Debrief" label survives anywhere in the module).  
  * After Therapy completed and a next session is known (cadence or explicit date) → button **"Between Sessions"** (opens the Between Sessions capture). This state stays visible the whole time, however many between-session notes the user adds, until 3 days before the next session. If no next session is known (a one-off session, no cadence), the module does not sit in this state: it returns to the start of the flow, state 1, the set-therapy prompt. Setting the next date is always the beginning of the cycle (Darek); Between Sessions stays reachable from the FAB.  
  * 3 days before the next session → button back to **"Prepare"**; the countdown retargets to the next session. If the next session is already under 3 days away when After Therapy completes, skip state 5 and show "Prepare" straight away (decision, derived from the 3-day rule).  
  * Each later session shows its own date and its own time, never the nearest session's hour. The cycle restarts.  
* **Logic (per transition):**  
  * Prep card created → button flips to "View prep card" at once.  
  * Session start time reached → "After Therapy".  
  * After Therapy completed, from the FAB or from the module → "Between Sessions".  
  * "Between Sessions" → tap → the Between Sessions capture opens; on save the button stays "Between Sessions" while the window lasts.  
  * 3 days before the next session → "Prepare"; countdown retargets.  
* **Do NOT touch:** The countdown time formats (QA: fine); the reminder elements; the settings session data model; the far-out-date display; the working Android implementation beyond the regression pass.  
* **Done when:** On iOS: completing the debrief flips the button to "Between Sessions" whether the debrief was started from the FAB or from the module; the state holds until exactly 3 days before the next session, then shows "Prepare"; with no cadence and no next date, completing After Therapy returns the module to the set-therapy state; grep finds no live "Debrief" label in the module; the prep flip is immediate; each session renders its own date and time; the full cycle loops across a cadence boundary. On Android: a regression pass confirms the chain behaves exactly as it did before this item.  
* **Risk:** Medium. Time edge cases: a session starting right now, cadence gaps shorter than 3 days, the day boundary.

---

## **F · Timeline**

### **CS-08 · FIX · \[Timeline\] · Weekly and monthly summary cards: absent from the build; deliver the specced structure**

* **Type:** FIX

* **Re-work of:** MSV3.2 Fix 2 · CS-13, itself a re-work of Fix 1.3 · CS-21. QA 22.07: the feature never made it into the build. Fix 1.3 CS-21's generation repairs (auto-generate at period end, the "Generate Now" button, an in-card error state instead of a raw 500\) stay in force and are this item's precondition.

* **Location:** Timeline ("Therapy Journey") → the Weekly and Monthly views → the summary card. Reached: Timeline → filter Weekly or Monthly.

* **What it is:** The automatic period summary built from the app's overall data: what the user raised in therapy and in their notes, and where they progressed on goals and symptoms. Shown in the Timeline only for now (Darek).

* **Now (wrong):** The Weekly and Monthly views show no summary cards at all. (QA 22.07, confirmed by Darek 23.07: "Kart w ogóle nie ma.")

* **Expected:** One card per period: a descriptive part on top plus the period's most important items grouped into fixed categories.

* **UI anatomy (target, top to bottom):**

   Weekly summary:

  1. Period header (chrome)  
  2. Descriptive part  
  3. **What you worked on**: themes from sessions and notes  
  4. **How you felt**: symptom and mood movement, qualitative, per the Global content rule  
  5. **What you got done**: homework, to-dos, goal progress  
* Monthly summary:

  1. Period header (chrome)  
  2. Descriptive part  
  3. **What you worked on**  
  4. **How you felt** (qualitative, Global content rule)  
  5. **What you got done**  
  6. **Realizations & breakthroughs**  
  7. **Where your goals stand**: goal progress over the month  
* Keep the structure plain: a short descriptive paragraph, then the categories, each with its few most important elements. A category with nothing behind it in the period is omitted rather than padded (Fix 2 decision, consistent with the no-empty-sections logic on these cards). These cards are reference-only: they carry no flag icons.

* **AI:** Input: the period's app data (entries, cards, scores, homework and work done, goals). Output: one card per period, descriptive part plus the categories above, oriented to what the user actually did and how they progressed. Trigger: automatic at period end plus manual "Generate Now" (per Fix 1.3 CS-21). Failure: the in-card error state with retry, never a raw 500 (per Fix 1.3 CS-21).

* **Outcome:** The user opens Timeline and reads, per week and per month, what they worked on, how they felt, and what got done.

* **Value:** The summaries answer the user's core question about their therapy: what has actually been happening, and is it moving.

* **Do NOT touch:** Other Timeline views; existing cards; the filter chips.

* **Done when:** Summary cards actually render in the Weekly and Monthly views; a generated weekly card shows the description plus its 3 categories and a monthly card its 5; content covers therapy topics, note topics, and goal and symptom progress; the "How you felt" part contains no dates or scores; empty categories are absent; auto-generation and "Generate Now" work with no 500 on screen; both platforms.