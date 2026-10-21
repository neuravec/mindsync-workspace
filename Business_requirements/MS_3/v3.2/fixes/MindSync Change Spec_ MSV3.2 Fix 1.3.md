# **MindSync Change Spec: MSV3.2 Fix.1.1 (QA re-work)** 

## **Summary**

* Total items: 7 (FIX: 1 · CHANGE: 6\) \+ 2 verify-only (appendix, out of fix scope).  
* Areas touched: Session prep (input card), Output cards → Workspace triage, Main (Next therapy session, Mood Trend, AI Summary), Workspace (To do), Timeline (weekly/monthly summaries).  
* Intent: This is a QA re-work pass over items already shipped in MSV3.2 Fix.1. Each item below is something QA found still wrong after the previous batch went live. Nothing here is a new feature. The batch simplifies the session-prep input card, hard-specifies triage per card type, repairs the Next-therapy-session state machine on both platforms, redoes two AI narrative surfaces to a single qualitative rule, finishes the Workspace To-do checkbox and repeat work, and fixes the Timeline 500\. Numbering keeps the original IDs so commits and PRs still line up with the live batch; the one genuinely new item is CS-22.

## **Global guardrails (read before touching anything)**

* This is a re-work batch on already-live items. Touch only the items listed here. Do NOT re-open or regress items QA left alone in this pass: CS-02, CS-04, CS-08, CS-10, CS-20, FIX.02, FIX.04, FIX.05, and the CS-01 visual redesign. CS-06 and CS-01 are verify-only (see appendix), not fixes.  
* Do NOT touch, carried per item:  
  * CS-09: the existing reminder elements ("tak jak jest obecnie"); the settings session data model; the far-out-date display (beyond the weekday horizon the rule is "don't change anything"); the countdown time formats (QA: "godziny ok").  
  * CS-11: regeneration timing and mechanics; the module's position (CS-08); the AI Summary placement (FIX.03); the symptom rows themselves.  
  * CS-21: other Timeline views; existing cards.  
  * FIX.01: the task data shared with Main Homework (CS-10 reads the same source); the "Pokaż więcej" / "Pokaż mniej" expander and the "Pokaż zakończone" Done section (QA did not flag them).  
  * FIX.03: the Mood Trend symptom rows (CS-11); the summary's placement inside the Mood Trend box and the empty-state box deletion, both already done in FIX.03.  
  * CS-07: card sections that don't map to the four Workspace kinds; the generation logic itself; Timeline card storage (nothing is removed from cards).  
  * CS-22: the downstream prep-card generation and the proposal-generation logic; only the input card's selection and note UI changes.  
* After each item, run the app on Android and iOS and confirm no dead references or broken navigation.

## **Global content rule for AI narratives (shared by CS-11 and FIX.03)**

Both AI narrative surfaces follow one content standard, so fix them to the same rule:

* Qualitative wording about whether a symptom improved or worsened, and why, grounded in the user's own app data. For example "urosło mocno", "urosło słabo", "trochę zmalało".  
* Short, dense sentences.  
* It must NOT state point deltas between dates, cite score numbers, recite symptom history, or suggest adding a note.  
* Length: the AI Summary is at most 5 lines with no bullets; the per-symptom narrative stays short. This rule covers content only. It does not change regeneration timing or mechanics (per the source decisions in CS-11 and FIX.03).

---

## **CS-22 · CHANGE · \[Session prep\] · Prepare for your session input card: simplify selection and notes**

* **Type:** CHANGE  
* **Re-work of:** new item. Not in the live batch; surfaced during QA of the session-prep flow.  
* **Location:** "Prepare for your session" input card → the proposal list → the per-proposal controls (checkbox plus pills) and the follow-up screen reached by moving forward ("przejście dalej"), where the same selected proposals reappear with a note field. Reached: session-prep entry → "Prepare for your session" input card. Lead: grep the proposals list widget, the pill / flag control, and the note field on the follow-up screen. The exact pill and screen label strings are not in the notes; confirm them against the running screen before renaming anything.  
* **What it is:** The card where the user reviews AI-proposed session topics before a therapy session, marks which ones to bring, and optionally notes an answer. Today it carries redundant controls: a checkbox to select a proposal, plus mutually exclusive pills (flag, answer) where only one can be active at a time, plus an in-list note option, and then a second screen that shows the same selected proposals again with another note field.  
* **QA finding (now wrong):** Selecting a proposal reveals pills, but only one pill can be active at once, so the user cannot flag and answer at the same time. Flagging duplicates what the checkbox already does. Answering in the list duplicates the note field on the next screen, where the same selected proposals reappear. The flow is cluttered and needs simplifying. (Darek, QA.)  
* **UI anatomy (target, top to bottom):**  
  * Proposal list. Each row: **checkbox** (select this proposal) \+ proposal text. No flag pill, no answer pill, no in-list note control.  
  * Primary action to move forward ("przejście dalej") to step 2\.  
  * Step 2: the proposals the user checked, each with a single **notatka** field for the user's answer. This is the only place a note is added.  
* **Logic:**  
  * Checkbox → tap → proposal selected for the session → checkbox shows selected state. Tap again → deselected.  
  * Move-forward action → tap → advances to step 2 carrying only the checked proposals.  
  * Step 2 note field → type → saves the user's note against that proposal.  
  * Removed entirely: the pills (flag and answer) and the in-list note entry. Flagging and in-list answering no longer exist.  
* **Action:** From the current card (checkbox \+ mutually exclusive flag/answer pills \+ in-list note \+ a duplicate note step) to the anatomy above. Keep checkbox selection in the list, move notes to step 2 only, and remove the pills and the in-list note path.  
* **Outcome:** The user checks the proposals they want, moves forward, and writes any notes once, on the step where the selected proposals are already gathered. One way to select, one place to write.  
* **Value:** Removes the duplicated flag, answer, and note controls that made the card confusing. Darek's reasoning: selecting with a checkbox already marks the proposal, and the note belongs on the follow-up step, not in the list.  
* **Do NOT touch:** The downstream prep-card generation that consumes these selections; the proposal-generation logic; any other session-prep screen.  
* **Done when:** The input card shows a checkbox per proposal and no pills; flagging and in-list note entry are gone (grep clean); notes are entered only on step 2 against the checked proposals; selections carry from the list into step 2; the prep card still generates from the selected proposals on both platforms.

---

## **CS-07 · CHANGE · \[Output cards\] · Triage into Workspace: per-card hard spec (v3, canonical sections \+ per-item bookmarks)**

* **Type:** CHANGE  
* **Re-work of:** CS-07 (live batch). QA verdict: DO POPRAWY. v3 supersedes v2: adds the canonical-section model (create missing, merge duplicates, hide empty), per Darek 2026-07-20.  
* **Card-name aliases:** header chips render "Recording", "Preparation", "Between Sessions", "After therapy"; the live spec says Record, Prep, Between sessions, After Therapy. Same four cards, grep both spellings.  
* **Location:** Every generated output card → card body sections per the breakdowns below → bookmark controls \+ the mapping into Workspace §1 to §4. Reached: generate any card, or open one from Timeline.  
* **What it is:** Output cards present AI-generated findings; triage saves individual items into Workspace. Today only Preparation has a triage surface (the "Worth keeping?" panel routing TOPICS/QUESTIONS to "Topics & questions"), coverage of the four kinds is uneven across cards, two pairs of Preparation sections duplicate one kind each, and three cards lack sections for kinds their content can produce.  
* **Now (wrong):** Triage exists on one card of four, covers two kinds, subsets the questions, and routes to "Topics & questions" instead of the four Workspace sections. Kinds are missing on cards (no realizations on Recording, no agenda/action kinds on Between Sessions), and duplicated on Preparation. Sections can render regardless of material. (Darek, QA \+ screenshots 2026-07-20.)

  #### **Model (the hard rules)**

1. **Mapping rule (fixed):** pytania / tematy → **§1 Agenda następnej sesji** · action pointy → **§2 Do zrobienia** · wątki → **§3 Wątki** · realizations → **§4 Realizations**. Sections matching none of the kinds are reference-only, no bookmark.  
2. **One section per kind per card.** If two existing sections fit the same kind, merge them into one (Preparation has both merges).  
3. **Every card defines all four kinds.** Where a card has no section for a kind, create it (marked NEW below). Created sections generate from the card's existing input data.  
4. **No empty sections, ever.** A section with no material does not render at all: no header, no empty state, no placeholder. This applies to existing, merged, and created sections alike (general UX logic for output cards).  
5. **Bookmark per item.** Every item inside a mappable section carries a **bookmark icon (ikonka zakładki)**; the "Worth keeping?" panel is removed.

   #### **Per-card breakdown (final layout, top to bottom, labels verbatim; every mappable section renders only with material)**

**Card 1 · Recording**

1. Date · duration · **Share** — chrome → reference-only  
2. Conditional quality banners (diarization warning; "Speaker separation was not reliable for this recording.") → reference-only  
3. **Overview** — narrative → reference-only  
4. **Key Moments** — bullets (existing) → bookmark per bullet → **§3 Wątki**  
5. **Breakthroughs & Insights** — bullets (NEW; label reused from After therapy for consistency) → bookmark per bullet → **§4 Realizations**  
6. **Action Items** — list (existing) → bookmark per item → **§2 Do zrobienia**  
7. **Main topics** — chips (existing) → bookmark per chip → **§1 Agenda następnej sesji**

**Card 2 · Preparation ("Your Prep Card")**

1. Title "Your Prep Card" · **Share** — chrome → reference-only  
2. **SINCE LAST SESSION** — narrative → reference-only  
3. **Threads** / PL **"Wątki"** — MERGED from **UNFINISHED BUSINESS** \+ **NEW DEVELOPMENTS** (one header, both old headers gone; content: the thread chips followed by the new-development items) → bookmark per chip/bullet → **§3 Wątki**. Merged-section name: proposal, see question 2\.  
4. **Your Patterns This Week** — derived stats → reference-only  
5. **THINGS TO NOTICE** — warning boxes → reference-only  
6. **YOUR MOOD THIS WEEK** — symptom score rows → reference-only (CS-11 domain, do not touch)  
7. **Suggested Agenda** — MERGED from **Suggested Agenda** \+ **Questions Worth Asking** (agenda items numbered as today, then the questions with their **Targeted** / **General** / **Wildcard** groups and rationale intact) → bookmark per agenda item and per question, all 8 questions, not today's 3-chip subset → **§1 Agenda następnej sesji**. Merged-section name: proposal, see question 2\.  
8. **Action Items** — (NEW, pending question 3\) → bookmark per item → **§2 Do zrobienia**  
9. **Breakthroughs & Insights** — (NEW, pending question 3\) → bookmark per bullet → **§4 Realizations**  
10. **Worth keeping?** — REMOVED entirely, replaced by the per-item bookmarks. Aggregated TOPICS/QUESTIONS chips disappear; their source items are bookmarkable directly. Stale "…into your Therapy" copy dies with it (cross-ref CS-20; grep clean).

**Card 3 · Between Sessions**

1. Date · **Share** — chrome → reference-only  
2. **Topic** — title (existing) → bookmark, whole element → **§3 Wątki**  
3. **Summary** — paragraph (existing) → bookmark, whole element → **§4 Realizations**  
4. **Topics & questions** — (NEW; topics or questions worth bringing to the next session, extracted from this entry; name: proposal, see question 2\) → bookmark per item → **§1 Agenda następnej sesji**  
5. **Action Items** — (NEW) → bookmark per item → **§2 Do zrobienia**  
6. **Original Text** — collapsed source entry → reference-only (stays last)

**Card 4 · After therapy**

1. Date · **Share** — chrome → reference-only  
2. **Session Snapshot** — paragraph → reference-only  
3. **What Came Up** — chips (existing) → bookmark per chip → **§3 Wątki**  
4. **Emotional Journey** — narrative → reference-only  
5. **Breakthroughs & Insights** — bullets (existing) → bookmark per bullet → **§4 Realizations**  
6. **Unfinished Business** — open items (existing, REMAPPED) → bookmark per item → **§1 Agenda następnej sesji** (recommendation: unfinished business is what seeds the next session's agenda; with this remap the card covers all four kinds with zero new sections and zero merges; alternative in question 1\)  
7. **One Thing to Sit With** — reflective prompt (existing) → bookmark, whole element → **§2 Do zrobienia** (lands in Zadania domowe via CS-10, which reads §2)  
* **Mechanics:** bookmark icon per item at the granularity above (per bullet, chip, question, agenda item; whole-element for Topic, Summary, One Thing to Sit With). Pencil edit icons are a separate mechanic and stay untouched.  
* **Logic:**  
  * Bookmark → tap → item saved instantly to the section given in this card's breakdown, no batch confirm → icon shows selected state.  
  * Bookmark (selected) → tap again → item removed from Workspace → unselected.  
  * Bookmarks stay active forever: right after generation and on any later reopen from Timeline.  
  * All items stay on the card ("nic nie ginie"); the removed panel's footer promise is kept by the mechanic itself.  
  * Kind has no material → its section is absent from the card (rule 4); an absent section is never an error.  
  * Items saved earlier through "Worth keeping?" → land in §1 and show as selected bookmarks on their source items (pending question 5).  
  * The orange link-icon chip state (Preparation "UNFINISHED BUSINESS", After therapy "What Came Up") is unified with the bookmark selected state: one visual language for "this item is in Workspace" (pending question 5).  
* **Action:** Restructure the four cards to the canonical model: perform the two Preparation merges, create the NEW sections (Recording §4; Between Sessions §1 and §2; Preparation §2 and §4 pending question 3), remap After therapy Unfinished Business to §1, implement conditional rendering (no empty sections anywhere), wire per-item bookmarks everywhere, remove the "Worth keeping?" panel, re-route saves to the four Workspace sections.  
* **Outcome:** Every output card exposes the same four curatable kinds when material exists, the user saves findings item by item into the right Workspace section, cards never show empty boxes, and cards keep everything.  
* **Value:** The user, not the AI, decides what is important enough to work on; Workspace stays curated. One consistent triage model across all four cards. (Source CS-07 \+ Darek 2026-07-20.)  
* **Do NOT touch:** Reference-only sections' content (layout changes only where the breakdowns above say so); generation inputs; Timeline card storage; pencil edit affordances; YOUR MOOD THIS WEEK (CS-11); §1 agenda downstream behavior (FIX.02).  
* **AI:** Input: each card's existing generation inputs, unchanged. Output: each card's generation schema extends to cover all four kinds (new fields: Recording realizations; Between Sessions next-session topics/questions and action points; Preparation action points and realizations pending question 3); a kind with no material returns empty and its section is not rendered. Trigger: the card's existing single generation, no separate pass; triage itself adds no AI. Failure: the card's existing failure behavior; an empty kind is not a failure.  
* **Done when:** All four cards match their breakdown on both platforms; the coverage matrix holds (each kind at most one section per card); both Preparation merges done and old headers gone (grep "NEW DEVELOPMENTS" and "Questions Worth Asking" clean if renamed); NEW sections appear only when material exists; a card generated from thin material shows no empty mappable sections; every item in a mappable section has a working bookmark (including all 8 Preparation questions); tap/untap syncs instantly to the correct §; "Worth keeping?" gone (grep "Worth keeping?" and "Select what should go into your Therapy" clean); link-icon chips render as the bookmark selected state; reopening old cards from Timeline still triages; all four Workspace sections receive their kind correctly.  
* **Decisions (v3, to confirm):** D1 per-item bookmarks, panel removed · D2 canonical model: all four kinds per card, one section per kind, conditional render incl. existing sections · D3 mappings: Main topics→§1, Key Moments→§3, Topic→§3, Summary→§4, One Thing to Sit With→§2, Unfinished Business (After therapy)→§1 · D4 merged/NEW section names and placements as listed · D5 link chips \= bookmark selected state · D6 old "Worth keeping?" saves migrate to §1.  
* 

---

## **CS-09 · FIX · \[Main\] · Next therapy session: state machine and button-label bugs**

* **Type:** FIX  
* **Re-work of:** CS-09 (live batch, CHANGE). QA verdict: DO POPRAWY (logika rozwalona).  
* **Location:** Main → module 1 → "Next therapy session" (countdown \+ action area) → the state-dependent button and its transitions. Reached: open Main. Applies to Android and iOS.  
* **What it is:** The countdown module that guides the user through the session cycle with a single state-dependent button (set session, prepare, view prep card, debrief, between sessions, next session). The state machine is specified in the live CS-09; QA found the implementation does not follow it on either platform.  
* **Now (wrong):** Countdown times are correct ("godziny ok"), but the button state machine is broken. Enumerated bugs:  
  * \[Android\] After creating the prep card, the button shows "View Prep card" and the module stops there; it does not advance to debrief or between-sessions after the session. (Darek)  
  * \[Android\] Large latency between adding the prep card and the button flipping to its new state. (Darek)  
  * \[iOS\] After completing "prepare", the app opens the prep card (correct), but the button stays "prepare"; it should read "view prep card". (Darek)  
  * \[iOS\] When the calendar date shows the session already happened, the button shows "debrief" (correct), but after the debrief is completed it still shows "debrief" instead of "between sessions". (Darek)  
  * \[iOS\] The session hour repeats on later dates: further sessions display the nearest session's time instead of their own (see Decisions log). (Darek)  
* **Expected (target state machine, restated from the live CS-09):**  
  * No therapy set → button opens the hub-and-spoke to set therapy (date, time, cadence "kiedy się odbywa", with whom); writes the same fields as settings.  
  * Session upcoming, no prep done → button "prepare".  
  * Prep done, session upcoming → button "view prep card", flipping immediately after the prep card is created, with no latency.  
  * Session start time reached → button "debrief".  
  * Debrief completed → "between sessions" encouragement.  
  * Next session per cadence → button back to "prepare"; the countdown retargets to the next session.  
  * Each later session shows its own date and its own time.  
* **Labels:** the running app uses English button strings. Canonical strings for grep (per decision): "prepare", "view prep card", "debrief", "between sessions", plus the session-setup button. Normalize casing so both platforms render identical strings (QA saw "View Prep card" on Android and "view prep card" on iOS). Source PL equivalents, kept as cross-reference: "przygotowanie do terapii" (prepare), "debrief po terapii" (debrief). Confirm whether the final UI should be EN or PL. Lead: grep these strings.  
* **Logic (per transition):**  
  * Prep card created → button state → "view prep card" immediately (fixes bugs 1, 2, 3; no latency).  
  * Session start time reached → button state → "debrief".  
  * Debrief completed → button state → "between sessions" (fixes bug 4; the module must leave the debrief state).  
  * Between sessions \+ next session per cadence → button state → "prepare"; countdown retargets (source cadence rollover).  
  * Session time rendering → each session row and countdown uses its own stored start time, not the nearest session's time (fixes bug 5).  
* **Action:** Fix the state machine so it advances correctly on both platforms per Expected: prep flips to view-prep immediately, post-session goes to debrief, debrief completion goes to between-sessions, cadence rollover returns to prepare, and each session shows its own time. Do not redesign the module; correct the transitions, the button-state latency, the iOS label after prep, the debrief to between-sessions transition, and the repeated-hour rendering.  
* **Outcome:** The module always shows the one next action and never strands the user after a debrief; button labels match the actual state on both platforms; each session shows its own time.  
* **Value:** The state chain is the app's core loop; a stuck state kills the cycle. (Source CS-09.)  
* **Do NOT touch:** The existing reminder elements ("tak jak jest obecnie"); the settings session data model; the far-out-date display; the countdown time formats.  
* **Done when:** On both platforms, creating a prep card flips the button to "view prep card" with no perceptible latency; reaching session start time shows "debrief"; completing the debrief flips to "between sessions"; with cadence set, the next session retargets the countdown and the button returns to "prepare"; each later session shows its own date and time with no repeated hour; the button label strings are identical across Android and iOS.  
* **Risk:** Medium. State machine with time edge cases, for example a session starting right now. (Source CS-09.)

---

## **CS-11 · CHANGE · \[Main\] · Mood Trend: redo the narrative (action part 2\)**

* **Type:** CHANGE  
* **Re-work of:** CS-11, action part 2 only (live batch). QA verdict: do powtórki (redo action part 2).  
* **Location:** Main → Mood Trend module → the per-symptom narrative text below each symptom row. Reached: open Main, Mood Trend. Scope is the narrative content only; score input (CS-11 action 1\) and the last-update date (CS-11 action 3\) are not re-opened here, since QA flagged only action part 2\.  
* **What it is:** The per-symptom narrative under each symptom in Mood Trend. It should explain, in plain qualitative language, why a symptom rose or fell, using the user's own app data. QA found the narrative still needs the content rewrite from CS-11 action 2\.  
* **Now (wrong):** The narrative content rewrite (CS-11 action part 2\) needs redoing. (Darek)  
* **Expected:** Follows the Global content rule for AI narratives. Content only, regeneration mechanics and timing untouched (per source decision): each symptom's narrative tells the user WHY it rises or falls, grounded in data they entered into the app. Qualitative wording, for example "urosło mocno", "urosło słabo", "trochę zmalało", plus context from the user's own inputs. It must NOT state point deltas between dates, recite symptom history, or suggest adding a note.  
* **Logic:** symptom row → narrative renders below it → content follows the rule above; regeneration timing and mechanics unchanged.  
* **Outcome:** The user reads a narrative that explains changes from their own data in plain language, without numbers, history recitation, or note prompts.  
* **Value:** A narrative grounded in the user's inputs is more useful than a recital of score deltas. (Source CS-11.)  
* **AI:** Input is the user's app data relevant to the symptom (entries, scores, card content). Output is a short qualitative narrative per symptom, wording per the Global content rule, PL and ENG. Trigger is unchanged (current mechanics). Failure is unchanged (current behavior).  
* **Do NOT touch:** Regeneration timing and mechanics; score input (CS-11 action 1); the last-update date (CS-11 action 3); the module's position (CS-08); the AI Summary placement (FIX.03); the symptom rows themselves.  
* **Done when:** Every symptom's narrative uses qualitative phrasing with app-data context, states no point deltas, recites no symptom history, and suggests no note, spot-checked across symptoms in PL and ENG; regeneration timing unchanged.

---

## **CS-21 · CHANGE · \[Timeline\] · Weekly and monthly summaries: auto-generate and fix the 500 (redo)**

* **Type:** CHANGE  
* **Re-work of:** CS-21 (live batch). QA verdict: do powtórzenia (redo).  
* **Location:** Timeline → weekly and monthly views → the summary card and the **"Generate Now"** button. Reached: open Timeline, weekly or monthly view.  
* **What it is:** Weekly and monthly summary cards in Timeline. Currently the "Generate Now" button throws an on-screen error 500 and no summaries generate at all.  
* **Now (wrong):** "Generate Now" throws an on-screen 500 and no summaries generate. (Darek)  
* **Action:** Fix generation end to end so no raw 500 reaches the screen. Summary cards generate automatically for each weekly and monthly period (per author's answer). "Generate Now" stays as a manual trigger (decision: the author did not revoke it).  
* **Logic:**  
  * Period ends → card auto-generates → appears in the Timeline weekly or monthly view.  
  * "Generate Now" → tap → generates or regenerates the current period's card.  
  * Generation failure → in-app error state on the card with retry via "Generate Now" (decision), never a raw 500\.  
* **Outcome:** The user opens Timeline and finds ready weekly and monthly summaries tracking their therapy progression.  
* **Value:** Answers the user's core question: is the current therapy approach working, and am I feeling better, worse, or neutral.  
* **AI:** Input is the period's app data (entries, cards, scores, homework and work done). Output is a summary card covering the most important topics, changes, and work done in the period, oriented to the user's therapy progression, and answering whether the approach is working and whether the user feels better, worse, or neutral. Trigger is automatic at period end plus the manual "Generate Now". Failure is an error state on the card with retry, and no 500 on screen.  
* **Do NOT touch:** Other Timeline views; existing cards.  
* **Done when:** Weekly and monthly cards auto-generate at period boundaries; "Generate Now" produces a card without errors; the content covers topics, changes, and work done, and answers the approach-working and better/worse/neutral questions; a failure shows the in-card error state and never a raw 500\.

---

## **FIX.01 · CHANGE · \[Workspace\] · To do: checkboxes and repeats (partial re-work)**

* **Type:** CHANGE  
* **Re-work of:** FIX.01 (live batch). QA verdict: część do poprawy (the checkbox, repeats, and edit-hub repetition parts).  
* **Location:** Workspace → §2 Do zrobienia → the To-do list rows and the row edit (pencil) hub-and-spoke. Reached: open Workspace → §2 Do zrobienia.  
* **What it is:** The to-do list backing the Main Homework module (CS-10). FIX.01 specified checkboxes replacing bullets, a repeat setting, and a pencil-icon edit hub that manages repetition. QA found these three parts not implemented.  
* **Now (wrong):**  
  * Rows still show bullet points instead of checkboxes. (Darek: "wciąż są bullet pointsy zamiast check box")  
  * There is no visible way to set repetition. (Darek: "Nie widać możliwości ustawienia cykliczności")  
  * The edit menu offers only title edit and delete; there is no repetition editing. (Darek: "Nie ma opcji edycji powtarzalności, jest tylko edycja nazwy i usuń")  
* **UI anatomy (target, the flagged parts, top to bottom):**  
  * Each row: **checkbox** (replaces the bullet point) \+ task title \+ **edit icon (ołówek)**. "Odkliknij" stays removed from the menu entirely.  
  * Edit icon (ołówek) → hub-and-spoke: change **tytuł**, **opis**, and manage repetition. Label PL **"Powtarzaj"** / ENG **"Repeats"** \+ repeat icon; options PL **"Codziennie"**, **"Tygodniowo"**, **"Miesięcznie"** / ENG **"daily"**, **"weekly"**, **"monthly"**.  
* **Logic:**  
  * Checkbox → tap → task done → moves to the Done section with today's date; if repeating, the task reappears unchecked at its next period (each completion is a separate Done entry; a missed period just stays open, no stacking).  
  * Edit icon (ołówek) → tap → hub-and-spoke opens task edit: change tytuł, opis, set "Powtarzaj" / "Repeats" (Codziennie / Tygodniowo / Miesięcznie) → save → row updates.  
* **Action:** Finish the FIX.01 parts QA flagged: replace the remaining bullet points with checkboxes; add the repetition setting; extend the pencil edit hub-and-spoke to manage repetition, which today offers only title edit and delete.  
* **Outcome:** To-dos are checkable and repeatable, and the user can set and edit a task's repetition from the pencil edit hub.  
* **Value:** To-dos behave like tasks, not static bullets. (Source FIX.01.)  
* **Do NOT touch:** The task data shared with Main Homework (CS-10 reads the same source); the "Pokaż więcej" / "Pokaż mniej" expander and the "Pokaż zakończone" Done section, which QA did not flag.  
* **Done when:** Rows show checkboxes, not bullets (grep for the bullet widget returns none); a task's repetition can be set and edited from the pencil hub-and-spoke (Powtarzaj / Repeats with Codziennie / Tygodniowo / Miesięcznie); repeating tasks reappear per period and log each completion; checking a task moves it to Done with today's date; the shared data model with CS-10 is unchanged.

---

## **FIX.03 · CHANGE · \[Main\] · AI Summary: rewrite the copy and the prompt**

* **Type:** CHANGE  
* **Re-work of:** FIX.03 (live batch). QA verdict: do poprawy (the copy and the prompt).  
* **Location:** Main → AI Summary, now inside the Mood Trend box, above the first symptom (per FIX.03). Reached: open Main → Mood Trend box → the summary at the top. Also the generation prompt behind it ("prompt pod spodem").  
* **What it is:** The descriptive summary of symptom change shown at the top of the Mood Trend box. QA found the copy still leans on dates and scores; it should speak qualitatively about which symptoms improved or worsened, with context.  
* **Now (wrong):** The description reads too long and leans on the dates and scores it currently cites. Sentences must be shorter and denser, and speak generally about improvement or worsening of the various symptoms, with their context, not about dates and scores. The generation prompt underneath needs the same fix. (Darek)  
* **Action:**  
  1. Rewrite the AI Summary copy to the Global content rule for AI narratives: short, dense sentences; qualitative statements about which symptoms improved or worsened and why, with context from the user's data; no dates, no scores; at most 5 lines, no bullets.  
  2. Rewrite the generation prompt ("prompt pod spodem") to enforce that rule so the output stops citing dates and scores. Constraints are in the AI field below; paste the current prompt to have it rewritten in full.  
* **Logic:** new data → the summary generates and renders inside the Mood Trend box above symptom 1 → content follows the Global content rule.  
* **Outcome:** One short qualitative summary at the top of the Mood Trend box, about symptom improvement or worsening with context, and no dates or scores.  
* **Value:** A qualitative summary is easier to read and more meaningful than a recital of dates and scores. (Darek.)  
* **AI:** Input is the user's symptom data and context (entries, scores, card content). Output is a short qualitative summary, at most 5 lines, no bullets, about which symptoms improved or worsened and why, with no dates and no score numbers. Trigger is on new data (existing mechanics). Failure is the existing behavior. Prompt: rewrite to enforce qualitative wording, symptom improvement or worsening plus context, no dates, no point deltas, no scores, at most 5 lines, no bullets.  
* **Do NOT touch:** The Mood Trend symptom rows (CS-11); the summary's placement inside the Mood Trend box and the empty-state box deletion, both already done in FIX.03.  
* **Done when:** The AI Summary reads as short qualitative sentences about symptom improvement or worsening with context, cites no dates or scores, stays within 5 lines with no bullets, in PL and ENG; the generation prompt enforces the same and no longer produces date or score recitals.