# **MindSync Change Spec: MSV3.2 Fix 5 (QA pass of 24.07.2026) \- MSV3.2 Fix 4 review \+ Record Session iOS**

*For Claude Code · 2026-07-24 · author: Darek (notes \+ answers), compiled with zero open questions*

## **Summary**

* Total items: 4 (DELETE: 0 · FIX: 4 · CHANGE: 0\)  
* Areas touched: Output cards (Threads pill rendering on all four card types) · Record Session on iOS (save reliability, "Yieks\!" error screen, "Recording Found" recovery pop-out)  
* Sources: CS-01 comes from the 24.07 QA pass over **MSV3.2 Fix 4** and carries a **Re-work of** pointer to Fix 4 CS-01. CS-02, CS-03 and CS-04 come from Darek's iOS QA notes of 24.07 on Record Session. Fresh CS IDs, the same convention as the earlier batches.  
* Intent: two fronts. First, the one defect left from Fix 4: a thread pill with a long title runs past the right edge of the screen, so the user can neither read the full title nor reach its flag; the pill will wrap instead. Second, make Record Session on iOS dependable: saving sometimes fails for no visible reason, the error screen ignores taps and then closes itself, and the recovery pop-out traps the user in a dead loop. After this batch a session recorded on iOS saves reliably, and when something does fail, every button the user sees actually works.

## **Global guardrails (read before touching anything)**

* This batch runs on a QA-accepted build. The rest of Fix 4 passed the 24.07 QA pass: CS-02 (Between Sessions Realizations flags), CS-03 (weekly and monthly summaries) and CS-04 (Workspace Realizations Delete) work on device and stay untouched. Do not re-open or regress them.  
* Platform scope is split. CS-01 covers Android and iOS. CS-02, CS-03 and CS-04 are iOS work: "W tym zadaniu wyklucz Android, bo na nim Record session działa dobrze." (Darek, 24.07). Android recording works today and must not regress; any fix landing in shared Flutter code has to leave Android behavior exactly as it is. QA for these three items runs on iOS, plus an Android build check to confirm nothing shifted there.  
* The Fix 4 rule "do not modify After Therapy" narrows for CS-01 only: the wrap fix does land on After Therapy's Threads pills (decision, 24.07). Beyond wrapping, After Therapy changes in nothing. Pill visual, flag behavior, context line, the 3-thread cap and section order all stay as they are.  
* CS-01 is a rendering fix. Generation, flag logic, the Workspace modules and card data are all out of scope for it.  
* The flag contract from Fix 2 stands unchanged: a flag saves the item to its named Workspace module, tap again withdraws it, nothing enters Workspace without a user tap.  
* After each item: run the app and confirm no dead references and no broken navigation.

---

## **A · Output cards**

### **CS-01 · FIX · \[Output cards\] · Threads pills: long titles overflow the right screen edge**

* **Type:** FIX  
* **Re-work of:** MSV3.2 Fix 4 · CS-01 (Threads: one design everywhere, copied from After Therapy). The unified design itself passed QA and stays. This item fixes one rendering defect inside it.  
* **Location:** The thread pill in the **"Threads"** section of all four output cards: Recording card → **"Threads"** (sixth section); Between Sessions card → **"Threads"** (fifth section); Preparation card ("Your Prep Card") → **"Threads"** (fifth section); After Therapy card → **"Threads"** (in scope for the wrap per the 24.07 decision, otherwise still the untouched reference). Reached: Timeline → open a card whose threads carry long titles. QA reproduced it on the Preparation card, iOS TestFlight build, screenshot of 24.07. Lead: the unified Threads pill widget from Fix 4 CS-01; if it shipped as the one shared component that spec suggested, the fix lands once and covers every card.  
* **What it is:** The flaggable thread pill from Fix 4 CS-01: title in a pill, flag beside it, one context line underneath. The pill currently lays the title out on a single line no matter how long it is.  
* **Now (wrong):** When a thread title is longer than the screen width allows, the pill keeps its single-line layout and runs past the margin and the right screen edge. The tail of the title is cut off and the flag sits off screen, so the thread can neither be read in full nor flagged to Workspace. QA hit this on the Preparation card (iOS, TestFlight): three sentence-length thread pills cut at the right edge, none of them flaggable. The same rendering serves all four cards, so any long title reproduces the bug anywhere.  
* **Expected:** The pill wraps. A title that does not fit within the pill's maximum width breaks onto further lines and the pill grows taller to fit it ("rozszerzenie wysokości pillsa jest dozwolone", Darek).  
* **UI anatomy (wrapped state, per thread):**  
  * Thread pill: the title text, wrapping onto as many lines as it needs. Maximum pill width: the card's content width minus the flag slot. The pill never crosses the margin.  
  * Flag icon: in its current place to the right of the pill, vertically centered against the taller pill, always on screen (decision, 24.07). Visual and behavior otherwise unchanged.  
  * Underneath the pill: the context line, exactly as in Fix 4 CS-01. Plain text, not flaggable, unchanged.  
* **Wrap rules (decisions, 24.07):**  
  * No line cap and no ellipsis: the pill grows until the whole title is visible.  
  * A pill whose title fits on one line renders exactly as today. Wrapping only kicks in when needed.  
  * If a single word is longer than one line, break the word rather than let the pill overflow (compiler call, logged).  
* **Logic:** Flag on a wrapped pill → tap → the thread saves to Workspace Threads, tap again → withdrawn. This is the existing Fix 4 CS-01 logic; the fix adds no new behavior, it makes the flag reachable for long titles.  
* **Outcome:** Every thread title is fully readable and every thread can be flagged, whatever length the AI gave the title.  
* **Value:** "pillsy z tekstem, jeżeli tekst jest dłuższy niż szerokość ekranu, wychodzą poza prawą krawędź ekranu, w efekcie nie można ich przeczytać ani oflagować jako dodane." (Darek, 24.07)  
* **Do NOT touch:** Thread title generation: titles stay as the AI writes them, sentence length included; the UI absorbs them (decision, 24.07). The pill visual beyond its height: colors, radius, typography, spacing. The context line and its plain-text, never-flaggable status. The 3-thread cap and the historical-cards convention from Fix 4\. Topic pills in Topics & Questions and every other pill in the app (decision, 24.07: Threads pills only). The Workspace Threads module and its rows. The flag contract. Section order on all cards.  
* **Done when:** On a device build, both platforms: a thread whose title exceeds the screen width renders as a multi-line pill fully inside the margins, the whole title readable; its flag is visible to the right, vertically centered, and both saves and withdraws correctly; the three long threads from the 24.07 Preparation screenshot are readable and flaggable on a re-check; short-title pills render exactly as before the fix; the wrap behaves identically on all four card types, After Therapy included; historical cards with stored long titles wrap the same way; nothing else in the Threads section moved.

---

## **B · Record Session (iOS)**

### **CS-02 · FIX · \[Record Session\] · iOS: session save fails intermittently, root cause unknown**

* **Type:** FIX  
* **Location:** The Record Session flow end to end: start recording → record → stop → save and processing → the session's output card. The failure shows at the save step. Reached: Main → **"Record Session"**. Lead: grep "Record Session"; the save/upload path that hands the recording to processing.  
* **What it is:** Record Session is the voice flow that records a therapy session and saves it for processing into its output card. On iOS the save step is unreliable.  
* **Now (wrong):** On iOS, starting or saving a recorded session sometimes fails with the "Yieks\!" error screen and sometimes completes fine: "czasem wyskakuje błąd, a czasem zapisuje się dobrze" (Darek, 24.07). No known repro pattern; the failure is intermittent under normal conditions. Android saves reliably.  
* **Expected:** Saving a recorded session on iOS works every time under normal conditions. The error screen appears only on real failures (no network, backend down), never intermittently on healthy runs.  
* **Action:** Walk the entire Record Session flow on iOS step by step (start → permissions → record → stop → save → processing → the card appears) and verify each step works; reproduce the intermittent save failure, identify the root cause, and fix it. Write the found cause up in the PR description. This item asked for verification of the whole process, so a step that turns out broken beyond the save flakiness gets reported back to Darek before any fix outside this scope.  
* **Do NOT touch:** Android behavior (works today; shared-code fixes must leave it unchanged). The Recording output card and its sections. The error screen's design and logic beyond what CS-03 defines. The mic permission flow, unless the audit proves it is the root cause (then report first).  
* **Done when:** On an iOS device build: the root cause is identified and written up; repeated back-to-back session recordings all save without the error under normal conditions (QA bar: 10 in a row, compiler call, flagged for veto); every step of the flow is verified working on iOS; forcing a real failure (airplane mode) still shows the error screen per CS-03; the Android build passes with recording behavior unchanged.

### **CS-03 · FIX · \[Record Session\] · "Yieks\!" error screen: no button responds, screen closes itself**

* **Type:** FIX  
* **Location:** Record Session → save-error state → the **"Yieks\!"** error screen and its three exits: **x** (close), **"try again"**, **"discard"**. Reached: record a session on iOS → save fails (after CS-02, force it with airplane mode). Lead: grep the "Yieks\!" title string.  
* **What it is:** The error screen shown when a session recording fails to save. It is the user's only chance to rescue or drop the recording at the moment of failure.  
* **Now (wrong):** On iOS, when the screen appears, no button responds: not the x, not "try again", not "discard". After a longer while the screen closes by itself. "To jest błąd, buttony powinny reagować od razu. Aplikacja za wolno reaguje." (Darek, 24.07). Today the self-close leaves the unsaved recording behind, which is what later surfaces the "Recording Found" pop-out of CS-04.  
* **Expected:** Every button responds the moment the screen renders, and the screen never closes itself: it stays until the user picks an exit (decision, 24.07). Lead: whatever work runs after the failed save must stop blocking the UI; the same freeze pattern shows on the CS-04 pop-out, so look for a shared cause.  
* **UI anatomy (elements as named in the notes):**  
  * **x**: closes the screen.  
  * **"try again"**  
  * **"discard"**  
* **Logic (decisions, 24.07):**  
  * x → tap → deletes the recording permanently and closes the screen, the identical end state to "discard" → user back where the flow started.  
  * "try again" → tap → re-attempts save and processing of the already-captured recording, no re-recording → on success the normal post-save flow; on another failure this screen again.  
  * "discard" → tap → deletes the recording permanently and closes the screen.  
  * No auto-close, ever. Consequence (logged): x and "discard" leave no draft behind, so after this fix the "Recording Found" pop-out triggers only when the app died before the user resolved the error (crash, kill, interruption).  
* **Outcome:** The error screen is usable at the exact moment it matters: the user reads it, then rescues the recording or drops it, in one tap each.  
* **Value:** "Buttony nie reagują od razu, żadne. \[...\] Ekran sam się zamyka po dłuższym czasie." (Darek, 24.07). A frozen error screen turns a recoverable failure into a lost session.  
* **Do NOT touch:** The screen's visual design, copy and layout; this item fixes responsiveness and exit logic only. The happy-path recording UI. Android (out of scope, works today).  
* **Done when:** On an iOS device build: trigger the error → each of the three buttons responds instantly when tapped right after the screen appears; x and "discard" delete the recording and no "Recording Found" pop-out shows at the next launch; "try again" with connectivity restored saves the session normally; the screen left untouched stays open indefinitely; Android unchanged.

### **CS-04 · FIX · \[Record Session\] · "Recording Found" pop-out: slow buttons, "Discard Recording?" dialog loops dead**

* **Type:** FIX  
* **Location:** App launch → **"Recording Found"** pop-out (shown when an unsaved session recording exists) → its buttons, and the **"Discard Recording?"** confirmation dialog with **"Keep it"** and **"Yes, Discard"**. Reached today: iOS → session save fails → close and relaunch the app. Lead: grep "Recording Found" and "Discard Recording?".  
* **What it is:** The recovery pop-out that tells the user an unsaved session recording was found and lets them save or discard it.  
* **Now (wrong):** On iOS the pop-out's buttons also respond late. Tapping **"Discard"** opens the "Discard Recording?" confirmation, and there both "Keep it" and "Yes, Discard" only return to the "Recording Found" pop-out, "tworząc martwy loop" (Darek, 24.07). Nothing ever saves or discards; the user cannot leave the cycle with a decision made.  
* **Expected (decisions, 24.07):** Every button on the pop-out and the dialog responds immediately, and each dialog button produces a real outcome per the Logic below.  
* **Logic:**  
  * "Discard" (on the pop-out) → tap → opens the "Discard Recording?" confirmation.  
  * "Yes, Discard" → tap → deletes the recording, closes the dialog and the pop-out → the user continues into the app; the pop-out never returns for that recording.  
  * "Keep it" → tap → runs the normal save and processing of the recovered recording, the same pipeline as a successful session save → dialog and pop-out close, the usual processing/result follows, the session's output card appears as after a normal save.  
* **Outcome:** The recovery pop-out does what it promises: one path saves the found session, the other removes it, both in two taps.  
* **Value:** The dead loop leaves an anxious moment (an unsaved therapy session) with no working exit; recovery is the whole point of this pop-out.  
* **Do NOT touch:** The detection logic that decides when the pop-out appears. The post-save processing pipeline ("Keep it" reuses it, does not fork it). Any other action the pop-out offers keeps its current behavior, except that its buttons must respond immediately. Android (out of scope). The CS-03 error screen.  
* **Done when:** On an iOS device build with an unsaved recording present: the pop-out's buttons respond instantly; "Discard" → "Yes, Discard" removes the recording, everything closes, relaunch shows no pop-out; "Discard" → "Keep it" saves and processes the recording into its normal session output and the pop-out never returns for it; no path returns the user to the pop-out without an outcome; Android unchanged.

