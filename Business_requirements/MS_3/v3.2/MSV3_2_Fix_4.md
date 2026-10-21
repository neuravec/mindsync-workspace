# MindSync Change Spec: MSV3.2 Fix 4 (QA pass of 23.07.2026) \- MSV3.2 Fix 3 review

*For Claude Code · 2026-07-23 · author: Darek (notes \+ answers \+ review round), compiled with zero open questions*

## Summary

- Total items: 4 (DELETE: 0 · FIX: 2 · CHANGE: 2\)  
- Areas touched: Output cards (Threads on Recording, Between Sessions, Preparation) · Between Sessions card (Realizations flags) · Timeline (weekly and monthly summaries) · Workspace (Realizations row menu)  
- Sources: the QA pass over **MSV3.2 Fix 3**. Fresh CS IDs again; every item carries a **Re-work of** pointer. Two of the four items are repeat offenders: the Between Sessions realization flags (second attempt) and the weekly and monthly summary cards (third attempt).  
- Intent: unify the Threads design across every output card around the After Therapy version that QA likes, land the two items that previous batches specced but the build still does not show, and add a Delete entry to the Workspace Realizations row menu.

## Global guardrails (read before touching anything)

- This is a QA re-work batch on live items. Touch only what is listed here. Do not re-open or regress anything QA left alone.  
- **The After Therapy card is the reference for two items and changes in none.** Its Threads section (CS-01) and its Realizations flag (CS-02) are the models to copy. Do not modify After Therapy while copying from it.  
- Fix 3's "is ok, do not change" list (Between Sessions, After therapy, Realization auto-detected, Therapy Relationship check-in) still holds with one narrowing: the Between Sessions card's **Threads** section now changes under CS-01 and its **Realizations** flags under CS-02, both per Darek's new notes. Everything else on that card stays untouched.  
- The section order of every card type stays exactly as the Fix 2 appendix. This batch changes what renders inside sections, never their order.  
- The flag contract from Fix 2 (CS-02, CS-04, CS-16) stands: the flag saves an item to its named Workspace module, tap again withdraws it, nothing enters Workspace without a user tap. CS-04 adds a delete path out of the module; it does not change how things get in.  
- CS-02 and CS-03 have shipped as specs before and the build still does not show them working (CS-03's Timeline views and its "Generate Now" button exist only as a shell over a raw 500). Close them only against a device build that visibly shows the behavior, never against code review alone.  
- Triage never deletes content: flagged or not, every item stays on its card on the Timeline ("nic nie ginie").  
- UI strings ship in English; AI-generated content follows the language of the user's own data.  
- After each item: run the app on Android and iOS, confirm no dead references and no broken navigation.

## Global content rule for AI narratives (carried from Fix 2; applies to CS-03's "How you felt")

- Say whether something improved or worsened and how strongly, in qualitative words.  
- Say WHY, using the user's own app data: entries, actions, behaviors, context, history. Direction plus reason, always both.  
- Plain, blunt language. Short, dense sentences.  
- Banned outright: dates, score numbers, point deltas, digits of any kind, symptom-history recitals, and "add a note" style suggestions.

---

## A · Output cards

### CS-01 · CHANGE · \[Output cards\] · Threads: one design everywhere, copied from After Therapy

- **Type:** CHANGE  
    
- **Re-work of:** MSV3.2 Fix 3 · CS-02 (Preparation Threads as bare pills; its "descriptive texts leave the section" call is superseded here, decision from the question round) \+ MSV3.2 Fix 2 · CS-02 and appendix (Threads on Recording and Between Sessions). If Fix 3 CS-02 is still open when this batch starts, drop it and implement this item directly; do not build the bare-pill intermediate state first (Darek, 23.07).  
    
- **Location:** Three sections: Recording card → **"Threads"** (sixth section); Between Sessions card → **"Threads"** (fifth section); Preparation card ("Your Prep Card") → **"Threads"** (fifth section); each section's rendering and generation. The After Therapy card's Threads section is the reference and does not change. Reached: Timeline → open each card type. Lead: the After Therapy Threads widget; prefer promoting it to one shared component over keeping per-card copies.  
    
- **What it is:** The flaggable Threads section that feeds Workspace Threads. On After Therapy it already renders the way Darek wants and QA confirmed it matches the target below. The other three cards still render their own older layouts.  
    
- **UI anatomy (target, per thread, identical on Recording, Between Sessions, Preparation):**  
    
  1. Thread pill: the thread title, the same pill After Therapy uses.  
  2. Flag icon on the pill: saves the thread to Workspace **Threads**.  
  3. Underneath the pill: one short context line about the thread. Plain text, not flaggable (the Fix 3 decision "only thread-pills to flag" stays in force).


  Max 3 threads per card. The whole section looks and behaves exactly like After Therapy's. The context line belongs to Threads only: the topic pills in Topics & Questions (Fix 3 CS-01) stay title-only with no context line, and the "same pill pattern" wording there means the pill visual, nothing more (decision, 23.07).


- **Logic:**  
    
  - Flag on a pill → tap → the thread saves to Workspace **Threads**, row on top per Fix 2 CS-05 → tap again → withdrawn.  
  - The context line stays on the card; it does not travel to the Workspace row.  
  - No material → the section's existing one-line empty state, unchanged.


- **AI:** Input per card unchanged (Recording: the former Key Moments material; Between Sessions: the note's threads; Preparation: the merged UNFINISHED BUSINESS \+ NEW DEVELOPMENTS material). Output: at most 3 threads per card, each a short title plus one context line, the same shape After Therapy already produces. Trigger and failure: each card's existing behavior.  
    
- **Outcome:** Threads read the same on every card: a pill, a flag, one line of context, three at most.  
    
- **Value:** "On the screen for after therapy the threads look great. Wherever threads are being shown to the user, it should look exactly the same." (Darek)  
    
- **Do NOT touch:** The After Therapy Threads section (reference; confirmed already matching, cap included). If implementation finds After Therapy deviating from the target above (more than 3 threads, or no context line), stop and confirm with Darek instead of silently editing the reference. Also untouched: the Workspace Threads module, its rows and status logic (Fix 2 CS-07); section order on all cards; the other sections of these three cards.  
    
- **Done when:** Side-by-side screenshots of all four card types show one identical Threads design; on Recording, Between Sessions and Preparation every thread renders as pill \+ flag \+ one context line with at most 3 threads on a newly generated card; flags save and withdraw correctly; historical cards render their stored threads through the unified look (all stored items still show; the 3-cap applies to newly generated cards only, per the Fix 3 convention); both platforms.

---

## B · Between Sessions card

### CS-02 · FIX · \[Between Sessions card\] · Realizations flags: still missing, second attempt

- **Type:** FIX  
- **Re-work of:** MSV3.2 Fix 3 · CS-05, which was not implemented (QA 23.07: "The fix was not implemented. In between sessions you still cannot choose to save any realization to workspace."), itself a re-work of MSV3.2 Fix 2 · CS-02 (action 3\) \+ CS-16 (the modules fill only through flags).  
- **Location:** Between Sessions card → section **"Realizations"** (sixth section) → the per-statement flag icon. Reached: Timeline → open a Between Sessions card whose note produced detected realizations. Lead: copy the working flag control from the After Therapy card's Realizations section ("There should be a flag to do so, for example after therapy." Darek); grep the Realizations section widget on the Between Sessions card.  
- **Now (wrong):** Unchanged after the Fix 3 batch: the Realizations statements on the Between Sessions card render with no flag to tap, so the user cannot send one to Workspace from this card.  
- **Expected:** Flag per statement, like every other kind-section and exactly like After Therapy's Realizations. Only a flagged realization lands in Workspace → Realizations. All detected realizations keep landing on the Timeline as standalone Realization cards regardless of flag state; that already works and stays ("Na timeline trafiają normalnie wszystkie", Fix 3).  
- **Logic:**  
  - Flag on a realization statement → tap → row at the top of Workspace **Realizations** with its source tag (per Fix 2 CS-05 and CS-16) → tap again → withdrawn.  
  - No flag → no Workspace row, ever (the CS-16 contract).  
  - Flag state has no effect on the standalone Timeline Realization cards.  
- **Do NOT touch:** The detection and its quality; the standalone Realization (auto-detected) card, which carries no flag by decision (Fix 2 CS-16); the After Therapy Realizations section (reference); every other section of the Between Sessions card except Threads, which CS-01 owns; the Realizations sections on the other card types where the flag already works.  
- **Done when:** On a device build, both platforms: a Between Sessions card with detected realizations shows the flag icon on every statement; flagging creates the Workspace Realizations row and unflagging removes it; nothing enters the module without a tap; the standalone Timeline cards still appear for every detection.

---

## C · Timeline

### CS-03 · FIX · \[Timeline\] · Weekly and monthly summary cards: still absent, third attempt

- **Type:** FIX  
    
- **Priority:** Highest in this batch. Specced in Fix 1.3 (CS-21), Fix 2 (CS-13), and Fix 3 (CS-08); the build still shows nothing. "Please this time develop this functionality and make it work." (Darek)  
    
- **Re-work of:** MSV3.2 Fix 3 · CS-08 ← MSV3.2 Fix 2 · CS-13 ← Fix 1.3 · CS-21. Do not treat Fix 1.3 CS-21's generation mechanisms (auto-generate at period end, the "Generate Now" button, an in-card error state instead of a raw 500\) as already built. Darek confirmed on 23.07 that nothing was ever built behind the UI, so those mechanisms are inside this item's scope.  
    
- **Location:** Timeline ("Therapy Journey") → the Weekly and Monthly views → the summary card. Reached: Timeline → filter Weekly or Monthly.  
    
- **What it is:** Two new card types generated automatically, one after each week and one after each month: the period summary built from the app's overall data, covering what the user raised in therapy and in their notes and where they progressed on goals and symptoms. Shown in the Timeline only for now (Darek).  
    
- **Now (wrong):** The Weekly and Monthly views exist only as a shell. A "Generate Now" button is visible, but there is no feature behind it: tapping it returns a raw 500 and no card, and no card has ever auto-generated. Third QA in a row with zero cards. ("This feature was never built. It was just visible on the timeline. There is a button for Generate Now, but it never did anything. There was a 500 error on that." Darek, 23.07.)  
    
- **Expected:** One card per period: a descriptive part on top plus the period's most important items grouped into fixed categories. This item builds the feature end to end: the generation pipeline for both period types, the automatic trigger at period end, the wiring of the existing "Generate Now" button, and the in-card error state with retry in place of the raw 500\.  
    
- **Period definition (decision, 23.07):** A week is the calendar week, Monday through Sunday; a month is the calendar month; both in the user's timezone. Auto-generation fires once the period is over; the exact fire moment within the following day is the implementer's call (logged).  
    
- **Backfill (decision, 23.07):** None. Periods that ended before the rollout get no cards ("don't bother going back", Darek). The first cards appear at the first period end after the rollout, which covers the week or month already in progress when the feature ships.  
    
- **UI anatomy (target, top to bottom):**  
    
  Weekly summary:  
    
  1. Period header (chrome)  
  2. Descriptive part  
  3. **What you worked on**: themes from sessions and notes  
  4. **How you felt**: symptom and mood movement, qualitative, per the Global content rule  
  5. **What you got done**: homework, to-dos, goal progress


  Monthly summary:


  1. Period header (chrome)  
  2. Descriptive part  
  3. **What you worked on**  
  4. **How you felt** (qualitative, Global content rule)  
  5. **What you got done**  
  6. **Realizations & breakthroughs**  
  7. **Where your goals stand**: goal progress over the month


  Keep the structure plain: a short descriptive paragraph, then the categories, each with its few most important elements. A category with nothing behind it in the period is omitted rather than padded (Fix 2 decision, consistent with the no-empty-sections logic on these cards). These cards are reference-only: they carry no flag icons. The no-digits rule binds "How you felt" only; the descriptive part, "What you got done" and "Where your goals stand" may cite counts such as goal progress, consistent with the Goals module's numeric narrative (compiler call, flagged for veto).


- **AI:** Input: the period's app data (entries, cards, scores, homework and work done, goals). Output: one card per period, descriptive part plus the categories above, oriented to what the user actually did and how they progressed. Trigger: automatic at period end plus manual "Generate Now" (per Fix 1.3 CS-21). Failure: the in-card error state with retry, never a raw 500 (per Fix 1.3 CS-21).  
    
- **Outcome:** The user opens Timeline and reads, per week and per month, what they worked on, how they felt, and what got done.  
    
- **Value:** The summaries answer the user's core question about their therapy: what has actually been happening, and is it moving.  
    
- **Do NOT touch:** Other Timeline views; existing cards; the filter chips.  
    
- **Done when:** On a device build, both platforms: summary cards actually render in the Weekly and Monthly views; a generated weekly card shows the description plus its 3 categories and a monthly card its 5; content covers therapy topics, note topics, and goal and symptom progress; the "How you felt" part contains no dates or scores; empty categories are absent; "Generate Now" produces a card or the in-card error with retry, never a raw 500; auto-generation fires at the first period end after rollout (calendar week Monday to Sunday, calendar month, user's timezone); no cards appear for periods that ended before the rollout.

---

## D · Workspace

### CS-04 · CHANGE · \[Workspace → Realizations\] · "Delete" in the row's 3-dot menu

- **Type:** CHANGE  
- **Re-work of:** none; new in the notes of 23.07. Builds on the 3-dot row menu Fix 2 CS-17 gave Realizations rows ("Pin to top" / "Unpin").  
- **Location:** Workspace → **Realizations** → a row's 3-dot menu → new entry below Pin to top. Reached: open Workspace → Realizations → tap the three dots on a row. Lead: grep the CS-17 row menu component on Realizations rows.  
- **What it is:** The row menu currently offers "Pin to top" (or "Unpin"). There is no way to remove a realization from the module from this screen.  
- **UI anatomy:**  
  1. The 3-dot menu gains one entry, final string **"Delete"**, under "Pin to top" / "Unpin". No other new chrome on the row or the list.  
- **Logic:**  
  - "Delete" → tap → the row is removed at once, no confirmation dialog (decision: opening the menu is already a deliberate step, and a deleted realization can be flagged again from its card).  
  - If the row came from a flag, the source card's flag resets: the identical end state to tapping the flag off (decision). Re-flagging on the card creates the row again.  
  - Legacy rows that auto-entered the module before Fix 2 CS-16 and have no source flag simply disappear.  
  - Deleting a pinned row clears its pin (consistent with Fix 2 CS-17: check-off, archive and delete all clear the pin).  
- **Outcome:** The user can prune Workspace Realizations directly from the list, and the card flags keep telling the truth.  
- **Value:** "Please add an option to delete realizations from the workspace screen... after tapping the three dots, you have pinned to the top, I would also like a delete option there." (Darek)  
- **Do NOT touch:** The row menus of the other four list modules (decision: Realizations only); the "Pin to top" / "Unpin" entry and its behavior; the "Pin to agenda" action, a different feature; the standalone Timeline Realization card and its "Remove Realization" action; how realizations enter the module (CS-16 contract).  
- **Done when:** Every Workspace Realizations row's 3-dot menu shows "Delete" under the pin entry; tapping it removes the row instantly with no dialog; the source card's flag is off afterward and re-flagging recreates the row; deleting a pinned row clears the pin; the other modules' menus are unchanged; both platforms.

---

## Decisions log

- 23.07.2026, question round with Darek:  
  - Threads reference → "Already matches, copy it." After Therapy stays untouched, cap included; Recording, Between Sessions and Preparation adopt its exact look and behavior. → CS-01.  
  - Delete vs the source flag → "Same as unflagging." The row disappears and the source card's flag resets, so the realization can be flagged again; legacy rows with no source flag just disappear. → CS-04.  
  - Delete UX → "Instant, label Delete." Final string "Delete", no confirmation dialog. → CS-04.  
  - Delete scope → "Realizations only." The other four list modules keep their current menus. → CS-04.  
- 23.07.2026, supersession (from the new notes plus the question round): Fix 3 CS-02 said the descriptive texts leave the Preparation Threads section entirely. The unified design now keeps one short context line under each pill on every card, After Therapy style. The Fix 3 rule that survives is "only thread-pills to flag": the context line is plain text and never flaggable. → CS-01.  
- 23.07.2026, compiler calls (recorded here instead of open questions):  
  - Historical cards and the 3-thread cap follow the Fix 3 convention: stored items all still render through the unified look, the cap applies to newly generated cards only. → CS-01.  
  - One shared Threads component is a lead, not a mandate; identical look and behavior is the requirement. → CS-01.  
  - Fix 3's "Between Sessions is ok, do not change" guardrail is narrowed by the new notes: its Threads section (CS-01) and Realizations flags (CS-02) change; the rest of the card stays protected. → Global guardrails.  
  - CS-02 and CS-03 are close-against-the-build items: their Done when lines require a device build showing the behavior, since both were reported done before and were not. → Global guardrails.  
  - Versioning: this document is MSV3.2 Fix 4 with fresh CS IDs and Re-work of pointers to MSV3.2 Fix 3, the same convention the earlier batches used.  
- 23.07.2026, review round with Darek (after the logic and UX analysis of this document):  
  - Summaries, real state → the feature was never built; the Timeline views and the "Generate Now" button are a shell and the button 500s with nothing behind it. Fix 1.3 CS-21's mechanisms are therefore inside CS-03's scope, not a met precondition. → CS-03.  
  - Period definition → calendar week Monday to Sunday and calendar month, in the user's timezone. → CS-03.  
  - Backfill → none: "When summaries ship, don't bother going back." First cards at the first period end after the rollout. → CS-03.  
  - Threads pill pattern → "The fix 4 is the right one": the context line is Threads-only; topic pills stay title-only per Fix 3 CS-01. → CS-01.  
  - After Therapy stop rule → approved ("should be fine"); on any mismatch with the reference, stop and confirm instead of editing it. → CS-01.  
  - Fix 3 CS-02 → formally dropped if still open; implement Fix 4 CS-01 directly ("yes, implement fix 4"). → CS-01.  
- 23.07.2026, compiler calls from the review round:  
  - Digits on summary cards: Darek did not answer this one, so the ban stays scoped to "How you felt" while the descriptive part, "What you got done" and "Where your goals stand" may cite counts, following the Fix 2 convention that goal narratives cite numbers. Flagged for veto. → CS-03.  
  - The exact auto-generation fire moment within the day after a period ends is the implementer's call. → CS-03.

