# MindSync Change Spec: MSV3.2 Fix2 Fix.2 (QA pass of 22.07.2026) \- MSV3.2.1 Fix.1 \+ MSV3.2 Fix 1.3 review

*For Claude Code · 2026-07-22 · author: Darek (notes \+ answers), compiled with zero open questions*

## Summary

- Total items: 19 (DELETE: 1 · FIX: 5 · CHANGE: 13). CS-16 through CS-19 were added in the review rounds of 22.07 and sit next to the items they belong with, out of numeric order; IDs stay stable. The final section order of every generated card type is in the appendix at the end.  
- Areas touched: Session prep input · Output cards (all four types) · Workspace (agenda, Topics & Questions, To-do, Threads, Realizations) · Main (Your Session, Homework, Mood Trend) · Timeline (weekly and monthly summaries) · Therapy Relationship (voice check-in).  
- Sources: this batch is the QA pass over two live batches, **MSV3.2.1 Fix.1** (Workspace implementation review) and **MSV3.2 Fix 1.3** (QA re-work of MSV3.2 Fix.1). Those two specs reuse the same CS numbers for different items, so this document assigns fresh IDs; every item carries a **Re-work of** pointer to its source. Home and Workspace changes and the output cards are already in production; this batch corrects what QA found still wrong and adds nothing outside the notes.  
- Intent: simplify the prep input to two steps, make all four output cards speak the Workspace's language (same four section names, flag icon, correct routing, and Workspace filling only through the user's flags), fix ordering and status logic inside Workspace, unstick the Your Session state machine and add the Between Sessions window, purge dates and scores from the Mood Trend narratives, give the weekly and monthly summaries a fixed readable structure, and repair the voice check-in so it stops inventing text.

## Global guardrails (read before touching anything)

- This is a QA re-work batch on live items. Touch only what is listed here. Do not re-open or regress anything QA left alone.  
- **The save-to-Workspace control on output cards is the flag icon.** That is what the live build renders (screenshots of 22.07). Older specs call it a bookmark; the flag replaces that wording everywhere. Its tap mechanics (save instantly, tap again to withdraw, active forever, also on reopened cards) do not change in this batch.  
- **Triage never deletes content.** Flagged or not, every item stays on its card on the Timeline ("nic nie ginie").  
- **Naming source of truth is the Workspace module set:** "Topics & Questions", "To-do", "Threads", "Realizations". The agenda ("Next session agenda") is user-curated only; no flag save may ever write into it (CS-04).  
- Do NOT touch: reference-only card sections beyond what CS-18 and CS-19 explicitly change (their headers, the Patterns merge, the Why This Might Matter contract, the Emotional Journey removal); everything else about them, including the quality banners, the Your Mood This Week score readout, and all chrome, stays as is; card generation inputs; Timeline card storage and ordering; the Goals module and its narrative (it also cites numbers, known, out of scope here); Weekly Observations (same, out of scope); check-in scoring and color logic; the agenda checkbox close behavior.  
- UI strings ship in English (the current build's UI language). AI-generated content follows the language of the user's own data, as it does today.  
- After each item: run the app on Android and iOS, confirm no dead references and no broken navigation.

## Global content rule for AI narratives (CS-11, CS-12, and CS-13's "How you felt")

One standard for every narrative surface this batch touches:

- Say whether a symptom improved or worsened and how strongly, in qualitative words.  
- Say WHY, using the user's own app data: entries, actions, behaviors, context, history. Direction plus reason, always both.  
- Plain, blunt language. Short, dense sentences.  
- Banned outright: dates, score numbers, point deltas, digits of any kind, symptom-history recitals, and "add a note" style suggestions.  
- The AI Summary stays within 5 lines, no bullets. Per-symptom narratives stay short but understandable and with provided context. 

---

# A · Session prep (input)

## CS-01 · CHANGE · \[Session prep\] · Prep input: pick Supporting questions, then one note by voice or text

- **Type:** CHANGE  
    
- **Re-work of:** MSV3.2 Fix 1.3 · CS-22 (which cut the pills and moved notes to a second screen). QA: simplify further.  
    
- **Location:** "Prepare for your session" input flow → the Supporting questions list and the note step. Reached: session prep entry (FAB → "Prepare for Therapy", or Main → Your Session → "Prepare"). Lead: grep the proposals list widget from CS-22 and the per-proposal note fields on its step 2\.  
    
- **What it is:** The flow where the user picks AI-proposed questions and topics before a session and can add their own thoughts, feeding the prep card generation. After CS-22 it is a checkbox list followed by a screen with one note field per selected proposal.  
    
- **UI anatomy (target, in flow order):**  
    
  1. Step 1: the Supporting questions list (the AI proposals; keep the build's current list label). One select control per row, plus an action to skip this step entirely and go straight to capture.  
  2. Step 2 (capture): the choice to add a note **by voice or by text**, using the app's standard capture pattern. One note for the whole prep, not one per question.


- **Logic:**  
    
  - Question row → tap → selected; tap again → deselected.  
  - Skip → tap → step 2 opens with no questions selected.  
  - Voice → the standard recording flow with transcript preview; Text → text field.  
  - Save → the prep card generates from the selected questions plus the single note, on top of the app data it already consumes. Nothing selected and no note still produces a prep card from existing data, as today.  
  - The per-question note fields from CS-22 step 2 are removed.


- **Action:** From CS-22's select-then-annotate-each flow to the two steps above.  
    
- **Outcome:** The user picks questions or skips, then speaks or types one note, and the prep card generates.  
    
- **Value:** "Lets simplify prep card even more." (Darek) The per-question note step was still too heavy.  
    
- **Do NOT touch:** Downstream prep-card generation and the proposal generation logic; other session-prep screens; the Your Session button flip (CS-09).  
    
- **Done when:** The flow is exactly select-or-skip → one voice-or-text note; no per-question note field remains (grep clean); the skip path works; the prep card generates from selections plus note on both platforms.

---

# B · Output cards

## CS-02 · CHANGE · \[Output cards\] · One naming: the four Workspace section names on every card

- **Type:** CHANGE  
    
- **Re-work of:** MSV3.2 Fix 1.3 · CS-07 v3 (per-card breakdown). This also settles v3's open naming questions for the merged and new sections.  
    
- **Location:** Every output card (Recording, Preparation, Between Sessions, After therapy) → every section whose items save to Workspace → the section header. Reached: Timeline → open any card, or generate one.  
    
- **What it is:** Cards currently name their flaggable sections per card (Key Moments, Main topics, Suggested Agenda, Topic, Summary, What Came Up, Unfinished Business, One Thing to Sit With, Breakthroughs & Insights, Action Items). The items land in four Workspace modules whose names the user already knows.  
    
- **Action:** Every flaggable section renders under the name of the Workspace module it feeds. Final strings: **"Topics & Questions"**, **"To-do"**, **"Threads"**, **"Realizations"** (match each card's existing header type treatment, e.g. all-caps display where the card uses it). The Workspace module header itself corrects its casing too: the live "Topics & questions" becomes **"Topics & Questions"** everywhere the name appears as a title (module header, archive title, card sections); sentence-style strings such as "+ Add topic or question" stay as they are. Rename map, current live label → new label:  
    
  1. **Recording:** Main topics → **Topics & Questions** · Key Moments → **Threads** · Action Items → **To-do** · Breakthroughs & Insights → **Realizations**.  
  2. **Preparation ("Your Prep Card"):** Suggested Agenda, including its Targeted / General / Wildcard question groups → **Topics & Questions** · THREADS → **Threads** (name already right; normalize the casing to the shared treatment) · **To-do** and **Realizations** are created by CS-03.  
  3. **Between Sessions:** Topic → **Threads** · **Summary** stays reference-only (it is the note's recap, not an insight; decided in the review round) · **Realizations** is a new section listing the realization statements auto-detection finds in this note, flag per statement (see CS-16 for the propagation contract) · the v3-planned new sections take the shared names directly: **Topics & Questions**, **To-do**.  
  4. **After therapy:** What Came Up → **Threads** · Unfinished Business → **Topics & Questions** · Breakthroughs & Insights → **Realizations** · One Thing to Sit With → **To-do**.


  This item renames only the four kind-sections. The reference sections around them are handled by CS-18 and CS-19 (their own renames, one merge, one removal, one content contract).


  **Block position and order (decided in the review round):** the four kind-sections form one block, always in this order: **Topics & Questions → To-do → Threads → Realizations**, placed directly after the card's Summary section (the shared first-summary name per CS-18). The remaining reference sections follow the block in their existing relative order; Your Note on Between Sessions stays last. This supersedes the v3 per-card interleaved order. The final layout of every card type is in the appendix. Any of the four kinds still missing from a card's generation schema gets created the CS-03 way: extend the card's single generation pass, no separate AI call.


  **Empty-kind rule (supersedes v3 rule 4 for these four sections; decided in the review round):** the four kind-sections always render. When a kind has no material, the section shows its header and one short info line in the muted secondary text style, no icon, no error tone, no flag. Final strings, per kind: "No topics or questions found in this entry." · "No to-dos found in this entry." · "No threads found in this entry." · "No realizations found in this entry." On the Preparation card, whose content comes from the period rather than one entry, the wording is "found this week" instead of "found in this entry". The user sees that the AI looked and found nothing, not that something broke. Reference-only sections are untouched by this rule.


- **Logic:** Flag icon per item inside each renamed section → unchanged save and withdraw behavior; destination module per CS-04.  
    
- **Outcome:** The user sees the same four names on every card and inside Workspace, with no translating between "Key Moments" and "Threads" in their head.  
    
- **Value:** "Potrzebujemy zunifikować nazwy wszystkich elementów wewnątrz output cardów... tożsame z tym, co znajduje się w workspace." (Darek)  
    
- **Do NOT touch:** Section content and its generation; each card's section order; reference-only sections; the flag mechanics.  
    
- **Done when:** All four card types show only the four shared names on flaggable sections, in the block order and position above, matching the appendix layouts on both platforms; the Workspace module header reads "Topics & Questions"; grep for "Key Moments", "Main topics", "Suggested Agenda", "What Came Up", "Unfinished Business", "One Thing to Sit With", "Breakthroughs & Insights" returns no live card-section header; a kind with no material shows its one-line info state per the empty-kind rule; reference-only sections' content unchanged.

## CS-03 · FIX · \[Preparation card\] · The two specced sections that never shipped: To-do and Realizations

- **Type:** FIX  
- **Blocked by:** CS-02 (create them directly under the final names).  
- **Re-work of:** MSV3.2 Fix 1.3 · CS-07 v3, Preparation breakdown items 8 and 9 (Action Items and Breakthroughs & Insights, both marked NEW). The spec's pending question about them is resolved: both belong on the card.  
- **Location:** Preparation card ("Your Prep Card") → two sections at their block positions per CS-02 (To-do second and Realizations fourth in the block). Reached: Timeline → open a Preparation card, or generate one.  
- **Now (wrong):** Neither section was implemented; the card has no action-item section and no realization section. (Darek: "Tych 2 nie dodał w Prep Card Output.")  
- **Expected:** Both sections exist per the v3 model, under their CS-02 names: **To-do** (flag per item → Workspace To-do) and **Realizations** (flag per bullet → Workspace Realizations). Their content generates from the card's existing input data inside the card's single existing generation pass. No material → the section renders its one-line info state per the CS-02 empty-kind rule ("No to-dos found this week." / "No realizations found this week.").  
- **AI:** Input: the prep card's existing generation inputs, unchanged. Output: the generation schema extends with action items and realizations for this card; an empty kind returns empty and its section renders the info line. Trigger: the card's one existing generation. Failure: the card's existing failure behavior.  
- **Do NOT touch:** The card's other sections; the two Preparation merges already live; generation inputs.  
- **Done when:** A Preparation card generated from material containing action points and realizations shows both sections, each item carrying a working flag that routes to the right Workspace module; a card from thin material shows both sections with their info lines and no flags; both platforms.

## CS-04 · CHANGE · \[Output cards → Workspace\] · Topics and questions route to "Topics & Questions", never to the agenda

- **Type:** CHANGE  
- **Re-work of:** MSV3.2 Fix 1.3 · CS-07 v3 mapping (which still routed this kind to the agenda) \+ MSV3.2 Fix.1.2 · CS-05 and CS-06 (agenda is user-curated).  
- **Location:** The flag save routing on every output card → items of the topics-and-questions kind (after CS-02: the "Topics & Questions" section on all four cards). Reached: flag any such item.  
- **What it is:** Flagged topics and questions can currently land in "Next session agenda". The agenda is meant to be built by the user alone, by picking the interesting items inside Workspace and adding their own.  
- **Action:** From: flag → agenda, wherever that path exists. To: flag → the Workspace **"Topics & Questions"** module, always. The complete routing table after this item: Topics & Questions → Topics & Questions · To-do → To-do · Threads → Threads · Realizations → Realizations. The agenda's only feeds remain "Add to agenda" on Topics & Questions rows, "Add to agenda" on thread cards, "Pin to agenda" on realizations, and the manual "+ Add topic". Rows already sitting in the agenda stay where they are; no migration.  
- **Logic:** Flag on a topics-and-questions item → tap → a row appears at the top of Workspace Topics & Questions (order per CS-05) with its source tag → the flag shows selected. Tap again → the row is withdrawn.  
- **Outcome:** The agenda holds only what the user put there. The candidate pool lives in Topics & Questions.  
- **Value:** "Agenda to jest coś, co użytkownik buduje sobie sam na podstawie odkliknięcia interesujących elementów w Workspace." (Darek)  
- **Do NOT touch:** The "Add to agenda" and "Pin to agenda" actions; agenda source tags; existing agenda rows; the agenda checkbox close.  
- **Done when:** Flagging topics-and-questions items on all four card types creates rows in Topics & Questions and never in the agenda; withdraw works; existing agenda rows are untouched; both platforms.

## CS-16 · CHANGE · \[Output cards → Workspace\] · The four modules fill only through flags; auto-detected realizations stop auto-entering

- **Type:** CHANGE  
- **Re-work of:** MSV3.2 Fix 1.3 · CS-07 v3, whose flag contract the realizations pipeline bypasses today. Surfaced in this batch's review round (22.07); added as CS-16.  
- **Location:** The write path from realization auto-detection into Workspace → Realizations, and any other path that writes into the four modules without a user tap. Reached: add a note, recording, or debrief that yields a detected realization → open Workspace → Realizations. Lead: grep the auto-detection write into the Realizations store.  
- **What it is:** Auto-detection finds realizations in the user's content and today writes every one of them straight into Workspace → Realizations (the module currently lists all detected insights, e.g. "9 insights"). The triage model says the AI proposes and the user picks.  
- **Action:** From: detection → module, automatic. To: detection produces proposals only. A detected realization renders in two places: its source card's **Realizations** section, flag per statement, and its standalone "Realization / Auto-detected" card on the Timeline, which stays exactly as it is (View Source and Remove Realization, no flag there; decided). The Workspace module receives a realization only when the user flags it on the output card. The same contract holds for all four kinds: nothing enters Topics & Questions, To-do, Threads, or Realizations without a user tap (a flag, an "Add to agenda" style action, or a manual add). Rows that already auto-entered the module stay; the user can close or delete them as today; the rule applies from ship (decided).  
- **Logic:** Detection finds a realization → the card section and the Timeline card render it → flag on the card → row appears at the top of Workspace Realizations (order per CS-05) → unflag → row withdrawn. No flag → no row, ever.  
- **Outcome:** Workspace Realizations is a curated shelf of the insights the user chose to keep working with, not a feed of everything the AI noticed.  
- **Value:** "Użytkownik ma mieć możliwość zapisania tych, które mają dla niego sens... do Workspace mają trafiać tylko te, które użytkownik wybierze jako sensowne." (Darek)  
- **Do NOT touch:** The detection itself and its quality; the standalone Realization card and its View Source / Remove Realization actions; existing module rows; the manual add and "Pin to agenda" paths.  
- **Done when:** A newly detected realization shows on its source card and as a Timeline Realization card but not in Workspace; flagging creates the row and unflagging removes it; existing rows persist; a sweep across the other three kinds confirms nothing auto-writes into any module; both platforms.

## CS-18 · CHANGE · \[Output cards\] · Reference sections: one Summary, merged Patterns, grounded context, plain names

- **Type:** CHANGE  
    
- **Re-work of:** none; the final review round of 22.07 went through every section outside the four kind-sections.  
    
- **Location:** The four output cards → every section outside the four kind-sections → headers, one merge, one content contract. Reached: Timeline → open any card. Lead: grep the current header strings listed below.  
    
- **What it is:** The reading layer around the action block. Today it uses four different names for the same first-summary role, carries two overlapping pattern sections on Preparation that cite scores against the app's qualitative rule, mixes ALL CAPS with Title Case, and names the user's own words "Original Text".  
    
- **Action (per piece):**  
    
  1. **One first-summary name.** Overview (Recording), SINCE LAST SESSION (Preparation), and Session Snapshot (After therapy) all rename to **"Summary"**; Between Sessions has it already. Content stays what it is per card: what the recording covered, what happened since the last session, what the note says, how the session went. The four-section block sits directly after Summary on every card (CS-02).  
  2. **Preparation merge.** "Your Patterns This Week" \+ "THINGS TO NOTICE" → one section **"Patterns"**. Content: the week's patterns and the things worth noticing, written to the Global content rule: qualitative, direction plus reason, warnings in a calm tone, no dates, no scores, no digits. Both old headers gone.  
  3. **Between Sessions "Why This Might Matter" gets a grounding contract.** The name stays and the section always renders. When the note connects to something concrete already in the app: an active thread (named by its title), a goal, an agenda topic, or a repeating theme, the text must name that anchor and say why the note matters against it. When there is no concrete connection, the section shows one short line telling the user why: **"This note doesn't connect to any of your threads, goals, or topics yet."** (final string; muted secondary style, same treatment as the empty-kind info lines). Its generation input already includes thread and agenda context in the AI layer.  
  4. **"YOUR MOOD THIS WEEK" → "Your Mood This Week"** (Preparation). String un-shouted, content untouched: the score readout keeps its numbers, because it is a data table, not a narrative (CS-11 domain stays protected).  
  5. **"Original Text" → "Your Note"** (Between Sessions). Function unchanged: the collapsed source at the end of the card; after CS-14 it also holds the confirmed voice transcript.  
  6. **Header style.** Every section header string ships in Title Case, like "Topics & Questions"; no ALL CAPS strings remain. Renames apply at render time, so historical cards show the new headers too; stored content is untouched (decision, flagged for veto).


  Quality banners on Recording stay exactly as they are (technical notices).


- **Logic:** Why This Might Matter → generated with an in-app anchor → renders the grounded text, naming the anchor; generated without one → renders the no-context line instead. All other pieces are static renames or a merge with no behavior change.  
    
- **AI:** Patterns: the two old outputs merge into one section within the card's single generation pass, content per the Global content rule. Why This Might Matter: input adds the user's active threads, goals, and agenda topics; output either references one by name or returns empty, and an empty result renders the no-context line. Trigger and failure: the cards' existing behavior.  
    
- **Outcome:** Every card reads the same way: Summary up top, the four action sections, then card-specific context that earns its place and speaks like the rest of the app.  
    
- **Value:** "Prostsze, czytelniejsze i sensowniejsze w kontekście całej aplikacji." (Darek)  
    
- **Do NOT touch:** The four kind-sections (CS-02, CS-03, CS-16 scope); the Your Mood This Week content and mechanics; quality banners; chrome; the weekly and monthly summary categories (CS-13), which keep their own names.  
    
- **Done when:** Every card's first section header reads "Summary"; grep for "SINCE LAST SESSION", "Session Snapshot", "Your Patterns This Week", "THINGS TO NOTICE", "Original Text" returns no live card-section header, and "Overview" no longer renders on the Recording card; "Patterns" reads qualitatively with no digits (spot-check across cards); "Why This Might Matter" renders on every Between Sessions card, either naming an in-app anchor or showing the no-context line; "Your Mood This Week" and "Your Note" render; no ALL CAPS section string remains; both platforms.

## CS-19 · DELETE · \[After therapy\] · Section "Emotional Journey"

- **Type:** DELETE  
- **Re-work of:** none; final review round of 22.07.  
- **Location:** After therapy card → section "Emotional Journey" (the narrative of the session's emotional arc). Reached: Timeline → open an After therapy card. Lead: grep "Emotional Journey".  
- **Action:** Remove the section fully: the header, the rendered block, and its field in the generation schema. Rationale (Darek): how the session felt emotionally, as a standing rubric, adds little therapeutic value and duplicates the Summary's tone. One content note replaces it: when the session's emotional tone is significant (a marked shift during the session, or a repeating post-session pattern), the card's Summary carries it in at most one sentence; that is a Summary prompt note, not a new section. The removal applies at render time, so historical cards stop showing the section too; stored data may remain (decision, flagged for veto).  
- **Do NOT touch:** The emotional analysis feeding the rest of the system: weekly and monthly "How you felt", Mood Trend narratives, and Therapy Relationship all keep their inputs; every other After therapy section.  
- **Done when:** No After therapy card, new or historical, renders "Emotional Journey" (grep returns no live reference); the generation schema no longer produces the field; a session with a strong emotional shift shows it as a sentence inside Summary; both platforms.

---

# C · Workspace

## CS-05 · FIX · \[Workspace, all list modules\] · Order: newest added on top, everywhere

- **Type:** FIX  
- **Re-work of:** the ordering rule from MSV3.2 Fix.1.2 (P3: chronological by date added, newest at top) that the implementation does not follow. Raised twice in the 22.07 notes as a global fix.  
- **Location:** Workspace → every list module: Next session agenda, Topics & Questions, To-do, Threads, Realizations → row order, in the default 5-row view and the expanded views. Reached: open Workspace.  
- **Now (wrong):** Lists order by the creation time of the output card an item came from. An item flagged today from an old card sorts as old and lands deep in the list.  
- **Expected:** Every list orders by the moment the item was added to that list, newest first. A flag tap, "Add to agenda", "Pin to agenda", and a manual add all count as "added" at the moment of the tap, whatever the source card's age. A repeating task re-entering on its repeat day counts as added that day. To-do follows the same rule with no source grouping: one list, strict newest-first, "added by you" and "from AI" rows interleaved by add time (decision; this supersedes the earlier homework-pinned-on-top behavior). The only thing that sits above this order is a row the user pinned with Pin to Top (CS-17).  
- **Do NOT touch:** Archives (they keep ordering by close date, newest first, per P2); the visible-5 plus expand pattern itself; the rule only decides which rows are visible (pinned first, then the newest, per CS-17).  
- **Done when:** In every module, adding an item through each path places it on top of the unpinned rows; flagging an item today from a months-old card puts it above yesterday's rows; To-do shows no source-based grouping; both platforms.

## CS-17 · CHANGE · \[Workspace \+ Main\] · Pin to Top on every list, shared between To-do and Main Homework

- **Type:** CHANGE  
    
- **Re-work of:** none; new feature, added in the review round of 22.07. Works on top of CS-05's ordering.  
    
- **Location:** All five Workspace list modules (Next session agenda, Topics & Questions, To-do, Threads, Realizations) and Main → Homework → each row's menu plus the list ordering. Reached: open any of these lists → open a row's menu.  
    
- **What it is:** With newest-first ordering (CS-05), an older item the user cares about sinks as new items arrive. Pin to Top lets the user hold chosen items at the top of a list.  
    
- **UI anatomy:**  
    
  1. Row menu gains an entry **"Pin to top"**; on a pinned row the same entry reads **"Unpin"**. Where the menu lives per list: the 3-dot menu on agenda, Topics & Questions, and Threads rows; the pencil edit hub on To-do rows (and Main Homework rows, same data); on Realizations, the row's existing menu, and where a row has no menu yet, add the 3-dot menu pattern its sibling lists use. Lead: grep the 3-dot row menu component and the To-do pencil hub.  
  2. A pinned row shows a small pin icon next to its content. No other new chrome on rows.


- **Logic:**  
    
  - "Pin to top" → tap → row moves into the pinned block at the top of its list → menu entry becomes "Unpin" → pin icon shows.  
  - Pinned block: most recently pinned first. Below the block: the normal CS-05 order, newest added first.  
  - Pinned rows count toward the visible five; more than five pinned → the five most recently pinned show and the rest sit behind the expand control.  
  - "Unpin" → tap → row returns to its add-time position in the normal order → pin icon gone.  
  - Pin state is per list, with one exception: **To-do and Main Homework share the same pin state**, because they share the same data. Pinning in either place pins in both.  
  - Checking off, archiving, or deleting a pinned row clears its pin.


- **Outcome:** The user holds what matters at the top of any list while everything else keeps flowing in newest-first.  
    
- **Value:** "Dodajmy też funkcję Pin to Top zrównaną w głównym, jak i w Workspace." (Darek)  
    
- **Do NOT touch:** Flags, checkboxes, and archives; the Realizations "Pin to agenda" action, which is a different feature and keeps its name and behavior; do not confuse the two.  
    
- **Done when:** Every listed module offers Pin to top / Unpin from its row menu; pinned rows sit in a most-recently-pinned-first block above the newest-first rest and show the pin icon; pinning a task in Workspace To-do pins it on Main Homework and the other way round; the visible-five rule counts pinned rows; unpin, check-off, archive, and delete all clear the pin; both platforms.

## CS-06 · CHANGE · \[Workspace\] · Subline "Added manually" → "Added by you"

- **Type:** CHANGE  
- **Re-work of:** MSV3.2.1 Fix.1 · CS-02, which set "added by you" on To-do. This extends the same wording to every remaining "Added manually".  
- **Location:** Every surface rendering the source wording "Added manually", alone or composed. Known live spot: Next session agenda rows, tag "Topic added manually". Reached: Workspace → agenda → a manually added topic. Lead: grep "Added manually" and "added manually".  
- **Action:** Replace the wording "Added manually" with **"Added by you"** wherever it fits. Standalone sublines become "Added by you"; composed tags keep their pattern, so "Topic added manually" becomes "Topic added by you". Match each surface's existing casing convention (To-do sublines render lowercase "added by you" and stay that way).  
- **Outcome:** One voice for user-created items across the app.  
- **Value:** "Zmień wszędzie subline, który brzmi 'Added manually', na 'Added by you' tam, gdzie pasuje." (Darek)  
- **Do NOT touch:** The "from AI" labels; source tags that name cards (After therapy, Prep, Recording, Between sessions, Thread, Realization).  
- **Done when:** Case-insensitive grep for "added manually" returns no live UI string; the agenda shows "Topic added by you"; To-do is unchanged; both platforms.

## CS-07 · FIX · \[Workspace → Threads\] · Status toggles between Open and Worked on; closing lives only under "mark as done"

- **Type:** FIX  
- **Re-work of:** MSV3.2.1 Fix.1 · CS-04 (statuses open / worked on / done; "mark as done" on the expanded card).  
- **Location:** Workspace → Threads → thread card in the list → the status control (the chip rendering "open" / "worked on"). Reached: open Workspace → Threads, tap the status on a thread. Lead: grep "open" and "worked on" in the Threads module strings.  
- **Now (wrong):** Tapping the status walks it forward and off the list: "Open", then "Worked on", then the next tap closes the thread. The thread disappears without the user ever choosing to finish it.  
- **Expected:** The list-level status control only jumps between the two states, "Open" ↔ "Worked on", both directions, any number of times. A thread becomes done in exactly one place: expand the thread → tap **"mark as done"**. The automatic flip to "worked on" after a session where the thread was on the agenda stays as is.  
- **Do NOT touch:** "mark as done" and the "done" chip; the Closed threads archive and Restore; the trash-can delete; the automatic post-session status flip.  
- **Done when:** Cycling the list control never closes a thread (open → worked on → open, repeatedly); "mark as done" on the expanded card still closes it into the archive; both platforms.

## CS-08 · CHANGE · \[Workspace → To-do\] · Check-off animation and white row background

- **Type:** CHANGE  
    
- **Re-work of:** MSV3.2 Fix 1.3 · FIX.01 (checkboxes shipped; QA wants the transition finished).  
    
- **Location:** Workspace → To-do → task rows → the checkbox and the row container. Reached: open Workspace → To-do, tick a task.  
    
- **What it is:** Ticking a checkbox marks the task done and moves it to the Done archive. Today the row vanishes in the same frame it is tapped, and rows sit on a light blue fill while the module background is white.  
    
- **Now (wrong):** No visible feedback between the tap and the disappearance, and the row fill does not match the feature background.  
    
- **Action:**  
    
  1. Add a small checkbox animation on check-off: the mark draws in, the row holds for a beat, then leaves (fade or collapse). The user sees the task get done before it goes. Keep the whole sequence around 200 to 400 ms; the exact curve is the implementer's call (logged as a decision).  
  2. Row background: the same as the feature background, currently white. The light blue fill goes away.


- **Logic:** Checkbox → tap → animation plays → task moves to Done with today's date, unchanged → the next row moves up.  
    
- **Outcome:** Checking off reads as completing something, not deleting it.  
    
- **Value:** "Brakuje zauważalnego, wizualnego indykatora... Aby przejście było bardziej klarowne i ładniejsze dla oka." (Darek)  
    
- **Do NOT touch:** Repeat mechanics; the Done archive; the task data shared with Main Homework; row content and layout beyond the background.  
    
- **Done when:** Every tick, including on repeating tasks, plays the animation before the row leaves; rows render on white; a screen recording from each platform shows the sequence.

---

# D · Main

## CS-09 · FIX · \[Main → Your Session\] · State machine: unstick the post-debrief flow, add the Between Sessions window

- **Type:** FIX  
    
- **Re-work of:** MSV3.2 Fix 1.3 · CS-09. QA 22.07: still broken on iOS, and the chain gains one new rule (the 3-day window).  
    
- **Location:** Main → module 1 **"Your Session"** → the state-dependent button and its transitions. Reached: open Main. Lead: grep the module title "Your Session" and the button strings "Prepare", "View prep card", "Debrief", "Between Sessions", "After Therapy".  
    
- **What it is:** The countdown module that walks the user through the session cycle with one button.  
    
- **Now (wrong):**  
    
  - \[iOS\] After the session the button reads "Debrief" (correct entry point). The debrief was then completed from the FAB and again from Your Session, and the button still read "Debrief". The module never advances. (Darek, 22.07.)  
  - The "Debrief" label itself is stale: the feature is named **After Therapy** everywhere now; "Debrief" was its previous name (decision).  
  - There is no "Between Sessions" state at all: nothing prompts the user to add between-session notes after a completed debrief.


- **Expected (target chain, in order):**  
    
  1. No therapy set → button opens the hub-and-spoke to set therapy (date, time, cadence, with whom); writes the same fields as settings.  
  2. Session upcoming, no prep done → button **"Prepare"**.  
  3. Prep done, session upcoming → button **"View prep card"**, flipping immediately after the prep card is created, with no latency.  
  4. Session start time reached → button **"After Therapy"** (opens the debrief flow; no "Debrief" label survives anywhere in the module).  
  5. After Therapy completed and a next session is known (cadence or explicit date) → button **"Between Sessions"** (opens the Between Sessions capture). This state stays visible the whole time, however many between-session notes the user adds, until 3 days before the next session. If no next session is known (a one-off session, no cadence), the module does not sit in this state: it returns to the start of the flow, state 1, the set-therapy prompt. Setting the next date is always the beginning of the cycle (Darek); Between Sessions stays reachable from the FAB.  
  6. 3 days before the next session → button back to **"Prepare"**; the countdown retargets to the next session. If the next session is already under 3 days away when After Therapy completes, skip state 5 and show "Prepare" straight away (decision, derived from the 3-day rule).  
  7. Each later session shows its own date and its own time, never the nearest session's hour. The cycle restarts.


- **Logic (per transition):**  
    
  - Prep card created → button flips to "View prep card" at once.  
  - Session start time reached → "After Therapy".  
  - After Therapy completed, from the FAB or from the module → "Between Sessions".  
  - "Between Sessions" → tap → the Between Sessions capture opens; on save the button stays "Between Sessions" while the window lasts.  
  - 3 days before the next session → "Prepare"; countdown retargets.


- **Do NOT touch:** The countdown time formats (QA: fine); the reminder elements; the settings session data model; the far-out-date display.  
    
- **Done when:** On iOS and Android: completing the debrief flips the button to "Between Sessions" whether the debrief was started from the FAB or from the module; the state holds until exactly 3 days before the next session, then shows "Prepare"; with no cadence and no next date, completing After Therapy returns the module to the set-therapy state; grep finds no live "Debrief" label in the module; the prep flip is immediate; each session renders its own date and time; the full cycle loops across a cadence boundary.  
    
- **Risk:** Medium. Time edge cases: a session starting right now, cadence gaps shorter than 3 days, the day boundary.

## CS-10 · CHANGE · \[Main → Homework\] · Five newest tasks, To-do look, shared pins

- **Type:** CHANGE  
    
- **Blocked by:** CS-08 (copies its animation and row background); CS-17 (shared pin state).  
    
- **Re-work of:** MSV3.2 Fix.1 · CS-10 (the Main Homework module): look, count, and selection rule.  
    
- **Location:** Main → module 2 **"Homework"** → the task rows and the selection rule behind them. Reached: open Main.  
    
- **What it is:** Today's homework view reading the same data as Workspace To-do. It currently shows up to 3 items picked oldest-first (FIFO), rendered as bullet items with source sublines and no checkboxes.  
    
- **Action (two parts):**  
    
  1. **Selection rule:** from 3 oldest to **5 newest**. The module shows up to 5 open tasks: pinned tasks first (most recently pinned on top, per the shared CS-17 pin state), then the newest-added open tasks, the same order the Workspace To-do list uses. Both surfaces now show the same top of the same list.  
  2. **Row look:** the Workspace To-do row look from CS-08: a **checkbox** per row replacing the bullet, the same check-off animation, the same white row background. Ticking behaves exactly as in Workspace: task done → Done archive → the next task in order surfaces.


- **Logic:** Checkbox → tap → CS-08 animation → done in the shared data → the next task per the rule appears. Pin or unpin on either surface → both surfaces reorder together.  
    
- **Outcome:** Main shows the same five tasks the user would see at the top of Workspace To-do, ticked off the same way.  
    
- **Value:** "Żeby w homeworku na mainie było pięć, ale też najnowszych." (Darek) One list, one order, two surfaces.  
    
- **Do NOT touch:** The shared data source; the source sublines; repeat mechanics (a task re-entering on its repeat day counts as added that day and surfaces per the rule).  
    
- **Done when:** Main Homework shows up to 5 open tasks, pinned first, then newest, matching the top of Workspace To-do; rows have checkboxes, the CS-08 animation, and white background; ticking marks the task done in Workspace To-do as well; pinning on one surface reorders both; both platforms.

## CS-11 · CHANGE · \[Main → Mood Trend\] · Per-symptom narratives: direction plus reason, no numbers (redo)

- **Type:** CHANGE  
- **Re-work of:** MSV3.2 Fix 1.3 · CS-11. QA verdict: redo; the narratives still recite dates, results, and digits.  
- **Location:** Main → Mood Trend module → the narrative under each symptom row, and its generation prompt. Reached: Main → Mood Trend → expand a symptom.  
- **What it is:** The per-symptom explanation. Live example from 22.07: "Twoje oceny dla Scrollowanie wahały się od 10/10 do 2/10, a ostatni wynik to 2/10." Scores, and nothing else.  
- **Now (wrong):** Narratives still contain dates, scores, and digits, and describe history instead of explaining anything.  
- **Action:** Rewrite the narrative content and its generation prompt to the Global content rule: whether the symptom rose or fell and how strongly, and why, grounded in what the user put into the app (entries, actions, behaviors, context, history). Plain, blunt language. No dates, no scores, no digits.  
- **AI:** Input: the user's app data relevant to the symptom. Output: a short qualitative narrative per symptom, per the rule, in the user's language. Trigger: unchanged. Failure: unchanged.  
- **Outcome:** Under every symptom the user reads which way it moved and what in their own life the data ties it to, in plain words.  
- **Value:** "System ma opisywać nie tylko, że coś się polepszyło lub pogorszyło, ale też napisać, dlaczego i na jakiej podstawie." (Darek)  
- **Do NOT touch:** Regeneration timing and mechanics; score input; the per-symptom last-update dates; the symptom rows; the AI Summary's placement (CS-12).  
- **Done when:** Spot-checked across symptoms in an account with data: every narrative names a direction and a because, and contains no date, score, or digit; the prompt enforces the same.

## CS-12 · CHANGE · \[Main → Mood Trend\] · AI Summary: rewrite the copy and the prompt (redo)

- **Type:** CHANGE  
    
- **Re-work of:** MSV3.2 Fix 1.3 · FIX.03. QA verdict: still wrong; carried into this batch verbatim by Darek.  
    
- **Location:** Main → Mood Trend box → the **AI SUMMARY** block above the first symptom, and the generation prompt behind it ("prompt pod spodem"). Reached: open Main → Mood Trend → the summary at the top.  
    
- **What it is:** The summary of symptom change across all symptoms. The live copy of 22.07 opens with "On 2026-07-20, Sleep showed mixed movement, from 8/10 to 3/10 the same day..." Long, dated, scored.  
    
- **Now (wrong):** The description reads too long and leans on the dates and scores it cites. The prompt underneath produces exactly that.  
    
- **Action:**  
    
  1. Rewrite the AI Summary copy to the Global content rule: short, dense sentences; which symptoms improved or worsened and why, with context from the user's data; no dates, no scores; at most 5 lines, no bullets.  
  2. Rewrite the generation prompt to enforce that rule, so the output stops citing dates and scores. Pull the current prompt from the codebase and rewrite it in full against the rule.


- **Logic:** New data → the summary generates and renders inside the Mood Trend box above symptom 1 → content follows the rule.  
    
- **AI:** Input: the user's symptom data and context (entries, scores, card content). Output: at most 5 lines, no bullets, qualitative statements about which symptoms improved or worsened and why, with no dates and no score numbers, in the user's language. Trigger: on new data, existing mechanics. Failure: existing behavior.  
    
- **Outcome:** One short qualitative summary at the top of the Mood Trend box.  
    
- **Value:** "A qualitative summary is easier to read and more meaningful than a recital of dates and scores." (Darek)  
    
- **Do NOT touch:** The symptom rows (CS-11 scope); the summary's placement inside the Mood Trend box and the empty-state box deletion, both already done.  
    
- **Done when:** The summary reads as short qualitative sentences about improvement or worsening with the reason; it cites no dates or scores; it stays within 5 lines with no bullets; the prompt enforces the same and no longer produces date or score recitals.

---

# E · Timeline

## CS-13 · CHANGE · \[Timeline\] · Weekly and monthly summary cards: fixed, readable structure

- **Type:** CHANGE  
    
- **Re-work of:** MSV3.2 Fix 1.3 · CS-21. That item's generation repairs (auto-generate at period end, the "Generate Now" button, an in-card error state instead of a raw 500\) stay in force and are this item's precondition; this item specs the content the cards carry.  
    
- **Location:** Timeline ("Therapy Journey") → the Weekly and Monthly views → the summary card. Reached: Timeline → filter Weekly or Monthly.  
    
- **What it is:** The period summary of what the user did and how things moved: what they raised in therapy and in their notes, and where they progressed on goals and symptoms.  
    
- **Action:** Each card is a descriptive part on top plus the period's most important items grouped into fixed categories.  
    
  Weekly, 3 categories:  
    
  1. **What you worked on**: themes from sessions and notes.  
  2. **How you felt**: symptom and mood movement, qualitative, per the Global content rule.  
  3. **What you got done**: homework, to-dos, goal progress.


  Monthly, 5 categories: the same three, plus 4\. **Realizations & breakthroughs**. 5\. **Where your goals stand**: goal progress over the month.


  Keep the structure plain: a short descriptive paragraph, then the categories, each with its few most important elements. A category with nothing behind it in the period is omitted rather than padded (consistent with the no-empty-sections logic; logged as a decision).


- **AI:** Input: the period's app data (entries, cards, scores, homework and work done, goals). Output: one card per period, descriptive part plus the categories above, oriented to what the user actually did and how they progressed. Trigger: automatic at period end plus manual "Generate Now" (per Fix 1.3 CS-21). Failure: the in-card error state with retry, never a raw 500 (per Fix 1.3 CS-21).  
    
- **Outcome:** The user opens Timeline and reads, per week and per month, what they worked on, how they felt, and what got done.  
    
- **Value:** The summaries answer the user's core question about their therapy: what has actually been happening, and is it moving.  
    
- **Do NOT touch:** Other Timeline views; existing cards; the filter chips.  
    
- **Done when:** A generated weekly card shows the description plus its 3 categories and a monthly card its 5; content covers therapy topics, note topics, and goal and symptom progress; the "How you felt" part contains no dates or scores; empty categories are absent; auto-generation and "Generate Now" still work with no 500 on screen; both platforms.

---

# F · Therapy Relationship

## CS-14 · FIX · \[Therapy Relationship\] · Voice check-in: the preview shows words the user never said, and the transcript never reaches the card

- **Type:** FIX  
- **Re-work of:** MSV3.2.1 Fix.1 · CS-07 (transcript preview flow) with CS-08 and CS-09 (platform bugs). QA 22.07: wrong on both platforms.  
- **Location:** Therapy Relationship → "+ New Check-In" → the voice note → the transcript preview → the saved check-in card. Reached: Workspace → Therapy Relationship → \+ New Check-In → record.  
- **Now (wrong):** The preview does appear (the CS-07 flow shipped), but the text in it is hallucinated, as if the app never listened while the user spoke ("w ogóle halucynuje... tak jakby w ogóle mnie nie słuchało"). It points to an audio-recording problem inside this feature. And the raw transcript of the voice check-in still is not stored on, or visible in, the saved relationship output card. Both platforms.  
- **Expected:** The preview shows the actual transcript of what was said: real audio reaches the speech-to-text pipeline, and no model ever invents content to fill a gap. The CS-07 rules stand: generation runs only from the confirmed transcript; an empty transcript means the re-record-or-type prompt and nothing saves. The confirmed raw text is stored with the check-in and visible in its details and on the relationship output card in history.  
- **Action:** Reproduce on both platforms. Diagnose the audio path of this feature; leads, not conclusions: the recorder never starts, a wrong audio session or category, or an empty or truncated file sent to STT while a model fills the silence. Fix at the root, then wire the confirmed transcript into the saved check-in card.  
- **Do NOT touch:** The text check-in; scoring and color logic; streak and history; recording in other modules. If the fault sits in a shared recording component, fix the fault without changing the other flows' behavior.  
- **Done when:** On Android and iOS: a spoken check-in previews the words actually said (test with a distinctive sentence and compare); a silence-only recording ends in the re-record-or-type prompt with nothing saved and zero generated content; the saved check-in's details and the relationship output card show the confirmed transcript.

## CS-15 · CHANGE · \[Therapy Relationship\] · Check-in part 2: one static prompt for every user

- **Type:** CHANGE  
- **Re-work of:** none; new item on the flow CS-07 shipped.  
- **Location:** Therapy Relationship → "+ New Check-In" → part 2, the step where the user writes or records their thoughts → the question shown above the input. Reached: \+ New Check-In → past the score questions. Lead: grep "If you could change one thing about your therapy, what would it be?" and "Is there something you've been avoiding bringing up in sessions?".  
- **What it is:** Part 2 currently shows varying questions; the two above are live now, and older check-ins carried others (for example "Is there anything you wish your therapist did differently?").  
- **Action:** Remove both current questions from the app and replace them with one static headline, identical in every install, for every user, on every check-in, never updated from user data and never touched by AI. Final copy (decision): **"Share your thoughts on your therapy relationship."** Headline only, no supporting line (Darek, review round).  
- **Logic:** The prompt is a static string → the user's answer (text, or the confirmed voice transcript per CS-14) saves beneath it → new check-in cards render the same static headline above the answer. Historical check-in cards keep the question they actually asked (decision).  
- **Outcome:** Every user gets the same open invitation to talk about the relationship, instead of a rotating question steering the answer.  
- **Value:** The point of this step, per Darek: get the user talking about their therapy relationship so they can tell whether it serves them or whether something about it is off. "To ma być w każdej aplikacji. Ten tytuł nie ma się updatetować na podstawie danych wprowadzanych przez usera w żaden sposób."  
- **Do NOT touch:** Part 1, the score questions (Safety, Heard and understood, Direction) and their scoring; streak; the safety-concern detection on answers; historical cards.  
- **Done when:** Grep for both old question strings returns no live input-flow reference; every new check-in shows the static headline alone, identical across users and check-ins; historical cards are unchanged; both platforms.

---

## Decisions log

All of 2026-07-22, from the question round on the notes:

- Prep input flow → simplified to select-or-skip, then one note by voice or text; the per-question note fields die. (Darek)  
- How far does the section rename go → all four names, on every card, including Between Sessions "Topic" → "Threads". Reference-only sections keep their names. (Darek; refined in the review round: "Summary" stays reference-only and the Between Sessions "Realizations" section lists the detected statements instead, see below)  
- Flag vs bookmark → the flag icon is what the live build renders; it is the triage control from here on, and the older specs' "bookmark" wording is retired. (Darek; screenshots of 22.07)  
- Post-session button label → "After Therapy". "Debrief" was the feature's previous name; the feature is called After Therapy everywhere now, so leftover "Debrief" labels go. (Darek)  
- To-do ordering vs homework pinning → strict newest-first with no source grouping; this supersedes the earlier homework-pinned-on-top protection. (Darek)  
- Weekly and monthly categories → Darek accepted the proposed sets: weekly What you worked on / How you felt / What you got done; monthly adds Realizations & breakthroughs and Where your goals stand.  
- Voice check-in bug platform → both. (Darek)  
- Check-in part 2 copy → Darek asked for a headliner proposal; a headline plus supporting line was proposed, and in the review round Darek chose the headline alone: "Share your thoughts on your therapy relationship." Historical cards keep their original question; offered in the round and not contradicted.  
- Derived from the 3-day rule → if the next session is under 3 days away when After Therapy completes, the Between Sessions window is empty and the button goes straight to "Prepare". (Compiler's call, flagged for veto)  
- Existing agenda rows → CS-04 does not migrate them; they stay in the agenda. (Compiler's call, flagged for veto)  
- Empty summary categories (CS-13) → omitted rather than padded. Kept even after the empty-kind rule changed for cards: a summary is a recap, not a proposal surface, so an empty category carries no information worth a line. (Compiler's call, flagged for veto)  
- Languages → UI strings ship in English, matching the current build; AI-generated content follows the user's data language. (Compiler's call, flagged for veto)  
- Check-off animation → roughly 200 to 400 ms, mark draws in, row holds, then leaves; the exact curve is the implementer's call. (Compiler's call)  
- IDs and batch label → fresh CS-01 to CS-16 because the two source batches reuse the same numbers; every item carries a Re-work-of pointer. Batch labeled MSV3.2.1 Fix.2; rename it if the team numbers it differently. (Compiler's call)

From the review round, same day (Darek reread the spec and answered a second set of questions):

- Canonical name → **"Topics & Questions"**: ampersand kept, capital Q added. Applies everywhere the name appears as a title, including the Workspace module header, whose live casing is wrong; sentence-style strings like "+ Add topic or question" stay. (Darek)  
- Realizations propagation → auto-detection keeps proposing, but nothing enters any of the four Workspace modules without a user tap; today all detected realizations auto-enter the module, and that stops. New item CS-16. (Darek: "do Workspace mają trafiać tylko te, które użytkownik wybierze jako sensowne")  
- Standalone "Realization / Auto-detected" Timeline cards → no flag on them; picking happens only in the output cards' Realizations sections. (Darek)  
- Rows that already auto-entered Workspace → Realizations → they stay; the flag-only rule applies from ship. (Darek)  
- Empty kind-sections on cards → they render with a short info line instead of disappearing; this supersedes the v3 "no empty sections" rule for the four kind-sections only. Strings per CS-02; wording is the compiler's, flagged for veto. (Darek chose the option)  
- No next session set after After Therapy → the module returns to the start of the flow, the set-therapy prompt; Between Sessions stays reachable from the FAB. (Darek: setting the next date is always the beginning of the cycle)  
- Main Homework vs To-do ordering asymmetry → flagged as an observation in the first review round, then resolved in the second: Main Homework moves to 5 newest with shared pins (CS-10), so both surfaces show the same top of the same list. (Darek)

From the second review round, same day (Homework count, Pin to Top, section order):

- Main Homework → shows up to **5** tasks, **newest first**, replacing the 3-oldest FIFO rule. (Darek)  
- Pin to Top scope → all five Workspace lists plus Main Homework. Pin state is per list, except To-do and Main Homework, which share one state over their shared data. (Darek)  
- Pin to Top control → a "Pin to top" / "Unpin" entry in each row's existing menu (3-dot where lists have it, the pencil hub on To-do), plus a small pin icon on pinned rows. Included defaults, flagged for veto: pinned block on top ordered by most recently pinned; the rest newest-first below; pinned rows count toward the visible five, and with more than five pins the five most recent show; check-off, archive, and delete clear the pin. (Darek chose the option; details compiler's)  
- Section order on cards → the four kind-sections form one block in the order Topics & Questions → To-do → Threads → Realizations, placed directly after the card's first main summary section (Overview / SINCE LAST SESSION / Summary / Session Snapshot); remaining reference sections follow; Original Text stays last. Supersedes the v3 interleaved order. (Darek: "jeden blok, zaraz po pierwszym głównym podsumowaniu")  
- Repeating tasks under newest-first → a task re-entering on its repeat day counts as added that day, so it surfaces near the top. (Compiler's call, flagged for veto)  
- Stale line about Recording's Realizations section ("exists when material exists") → removed; the empty-kind rule makes all four sections always render, and any kind missing from a card's schema is created the CS-03 way. (Compiler's cleanup)

From the final review round, same day (the reference sections outside the four kinds; CS-18 and CS-19):

- First-summary name → **"Summary"** on every card, replacing Overview, SINCE LAST SESSION, and Session Snapshot. (Darek)  
- Preparation middle → "Your Patterns This Week" and "THINGS TO NOTICE" merge into one section **"Patterns"**, written to the Global content rule with no digits. (Darek)  
- After therapy "Emotional Journey" → removed (CS-19). Darek: as a standing rubric, how the session felt emotionally adds little therapeutic value. A significant emotional tone lands as at most one sentence inside Summary; the emotional analysis keeps feeding weekly and monthly "How you felt", Mood Trend, and Therapy Relationship.  
- Between Sessions "Why This Might Matter" → stays, under a grounding contract: it names a concrete in-app anchor (an active thread by title, a goal, an agenda topic, a repeating theme). (Darek: the name can stay if it truly connects to the rest of the app. The absent-when-empty part of this round was superseded by the correction below: the section now always renders.)  
- "YOUR MOOD THIS WEEK" → stays on Preparation as session context, renamed **"Your Mood This Week"**; the numbers stay, it is a data readout, not a narrative. (Darek)  
- "Original Text" → **"Your Note"**. (Darek)  
- Header style → Title Case for every section header string, no ALL CAPS; Recording's quality banners untouched. (Compiler defaults, stated and not contested)  
- Renames and the CS-19 removal apply at render time, so historical cards show the new layout too; stored content untouched. (Compiler's call, flagged for veto)

Correction after Darek's final read, same day:

- Why This Might Matter → always renders, on every Between Sessions card. With an anchor it names it; without one it shows a short line explaining why there is nothing to link: "This note doesn't connect to any of your threads, goals, or topics yet." String is the compiler's, flagged for veto. This replaces the earlier absent-when-empty version of the contract. (Darek)

---

## Appendix · Final section order of every generated card type (after this batch)

The reference for CS-02, CS-03, and CS-16. Sections marked **\[flag\]** carry the flag icon per item and save to the named Workspace module; everything else is reference-only. The four kind-sections always render; an empty one shows its one-line info state.

**1 · Recording**

1. Date · duration · Share (chrome)  
2. Quality banners, conditional (diarization warnings)  
3. Summary (was Overview)  
4. Topics & Questions **\[flag → Topics & Questions\]**  
5. To-do **\[flag → To-do\]**  
6. Threads **\[flag → Threads\]** (the former Key Moments content)  
7. Realizations **\[flag → Realizations\]**

**2 · Preparation ("Your Prep Card")**

1. Title "Your Prep Card" · Share (chrome)  
2. Summary (was SINCE LAST SESSION)  
3. Topics & Questions **\[flag → Topics & Questions\]** (the former Suggested Agenda items, then the questions with their Targeted / General / Wildcard groups and rationale, all flaggable, all 8 questions)  
4. To-do **\[flag → To-do\]** (created by CS-03)  
5. Threads **\[flag → Threads\]** (the merged former UNFINISHED BUSINESS \+ NEW DEVELOPMENTS content)  
6. Realizations **\[flag → Realizations\]** (created by CS-03)  
7. Patterns (merged from Your Patterns This Week \+ THINGS TO NOTICE; qualitative, no digits, per CS-18)  
8. Your Mood This Week (score readout; CS-11 domain, content untouched)

**3 · Between Sessions**

1. Date · Share (chrome)  
2. Summary  
3. Topics & Questions **\[flag → Topics & Questions\]**  
4. To-do **\[flag → To-do\]**  
5. Threads **\[flag → Threads\]** (the note's former Topic element)  
6. Realizations **\[flag → Realizations\]** (the realization statements auto-detection finds in this note)  
7. Why This Might Matter (always renders: the grounded text naming an in-app anchor, or the no-context line, per CS-18)  
8. Your Note (was Original Text; collapsed source entry, always last)

**4 · After therapy**

1. Date · Share (chrome)  
2. Summary (was Session Snapshot; carries a significant emotional tone in at most one sentence, per CS-19)  
3. Topics & Questions **\[flag → Topics & Questions\]** (the former Unfinished Business content)  
4. To-do **\[flag → To-do\]** (the former One Thing to Sit With content)  
5. Threads **\[flag → Threads\]** (the former What Came Up content)  
6. Realizations **\[flag → Realizations\]** (the former Breakthroughs & Insights content)

Emotional Journey is removed by CS-19 and appears on no card, new or historical.

**5 · Realization (auto-detected)**: unchanged this batch, no flag (CS-16 decision)

1. Date · "Auto-detected" badge · Share (chrome)  
2. The realization statement  
3. Source line ("From \[card type\] \- \[date\]")  
4. View Source  
5. Remove Realization

**6 · Therapy Relationship check-in**

1. Date (chrome)  
2. Safety banner, conditional ("What you described is serious", only when the safety concern triggers)  
3. Rating chip (Strong relationship / Mixed signals / Needs attention) · check-in number  
4. Narrative  
5. Your answers: Safety · Heard and understood · Direction  
6. The part-2 prompt with the user's answer (new cards: the static "Share your thoughts on your therapy relationship." per CS-15; historical cards keep their original question) and, for voice check-ins, the confirmed transcript per CS-14  
7. Share

**7 · Weekly summary (Timeline)**

1. Period header (chrome)  
2. Descriptive part  
3. What you worked on  
4. How you felt (qualitative, Global content rule)  
5. What you got done

**8 · Monthly summary (Timeline)**

1. Period header (chrome)  
2. Descriptive part  
3. What you worked on  
4. How you felt (qualitative, Global content rule)  
5. What you got done  
6. Realizations & breakthroughs  
7. Where your goals stand

