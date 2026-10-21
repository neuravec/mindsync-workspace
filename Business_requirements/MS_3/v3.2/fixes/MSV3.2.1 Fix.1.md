# **MindSync Change Spec: fixes from the MSV3.2 Workspace implementation review**

*For Claude Code · 2026-07-21 · author: Darek*

## **Summary**

* Total items: 9 (DELETE: 0 · FIX: 3 · CHANGE: 6\)  
* Areas touched: context menus (whole app), Workspace → To dos, Workspace → Threads, the archive/restore/refresh buttons, Therapy Relationship → voice check-in.  
* Intent: a batch of fixes from the review of the MSV3.2 (Workspace) release. The spec covers only the things the review showed to be broken or off from the intended design. Nothing else gets built or touched: the rest of the release works and stays as is.  
  ---

  ## **CS-01 · CHANGE · Whole app · menu item "Edit name" → "Edit"**

* **Type:** CHANGE  
* **Location:** every context menu under the three-dot button, in every module of the app → the menu item labeled "Edit name". Example path: Workspace → Threads → three dots on a thread card → "Edit name". Lead: grep "Edit name" in the UI strings.  
* **What it is:** the menu item that opens editing for the given item (a thread, a goal, and so on).  
* **Action:** From: label "Edit name". To: label "Edit". Applies to every menu in the app, not just Workspace. The item's behavior does not change.  
* **Outcome:** every three-dot menu shows "Edit".  
* **Value:** one consistent label across all menus (from the note: "applies to all menus").  
* **Do NOT touch:** how editing works; the other menu items.  
* **Done when:** grep "Edit name" returns no live UI string; a manual pass through menus in and outside Workspace shows "Edit" everywhere.  
  ---

  ## **CS-02 · CHANGE · Workspace → To dos · subline on manually added tasks**

* **Type:** CHANGE  
* **Location:** Workspace → To dos module → a task added manually by the user → the source subline under the task name. Path to add one: Workspace → To dos → "+ homework" → typed entry or recording. Current subline: "from therapist". Lead: grep "from therapist".  
* **What it is:** the subline shows where a task came from. Today, tasks the user entered themselves are labeled "from therapist", and action points from triage are labeled "from AI".  
* **Action:** From: subline "from therapist". To: subline "added by you" (this exact wording). Covers tasks added manually through both inputs: text and recording. The subline derives from the task's source field, so the change also covers manual tasks created before this fix ships.  
* **Outcome:** tasks the user added are labeled "added by you"; "from AI" stays on action points.  
* **Value:** the subline stops crediting the therapist with tasks the user added themselves.  
* **Do NOT touch:** the "from AI" label; homework pinning at the top of the list; the two-state task logic.  
* **Done when:** a new task from text and a new task from a recording both show "added by you"; manual tasks from before the change do too; grep "from therapist" returns no live UI string in To dos (if the string truthfully means the therapist somewhere else, it stays there).  
  ---

  ## **CS-03 · CHANGE · Workspace → Threads · no thread limit, list of 5 plus expansion**

* **Type:** CHANGE  
* **Location:** Workspace → Threads module (Wątki) → the list of thread cards, plus the logic for creating a new thread (manually via "+ nowy wątek" / new thread, and via triage).  
* **What it is:** the module holds therapy threads as cards with a status. Today there can be at most \~5 active threads: a sixth waits in a queue, and with a full list the user gets a message suggesting they close or dismiss something first.  
* **Action:** From: a cap of \~5 active threads, a queue for new ones, a full-list message. To: no limit at all, the user can add any number of threads. The list shows 5 by default and hides the rest behind an expansion. The collapse and expand pattern is copied 1:1 from To dos (from the note: "Logic same as in To-do"): same component, same control label, same rule for which items make the visible five.  
* **To remove together with the cap:** the thread queue logic, the full-list message, the block on triage creating a thread while 5 are active.  
* **Logic:** expansion control → tap → the list shows all threads → tapping again collapses back to 5 (behavior identical to To dos).  
* **Outcome:** the user adds any number of threads on the spot; the list stays compact because 5 show by default.  
* **Value:** the artificial ceiling that blocked triage and held new threads in a queue is gone.  
* **Do NOT touch:** thread statuses and their logic; the thread card in hub-and-spoke; the AI context description; the To dos module (we copy its pattern, we do not touch the original).  
* **Done when:** you can create, say, 8 threads with no message and no queue; the list shows 5 plus an expansion with the rest; expanding and collapsing works like in To dos; triage creates a new thread even with 5 or more existing.  
  ---

  ## **CS-04 · CHANGE · Workspace → Threads · renamed statuses and the close button**

* **Type:** CHANGE  
* **Location:** (a) status chips on thread cards: Workspace → Threads → thread card → status chip; (b) the closing button: Workspace → Threads → tap a thread → expanded card → the "close" button. Lead: grep "touched on" and "close" in the Threads module strings; the third chip's string sits next to them.  
* **What it is:** a thread has three statuses shown as a chip on its card; the expanded card has a button that closes the thread.  
* **Action:**  
  1. Chip "touched on" → "worked on".  
  2. The "close" button on the expanded card → "mark as done".  
  3. The status chip of a closed thread → "done" (after tapping "mark as done" the thread shows the "done" chip).  
  4. Full chip set after the change: open / worked on / done.  
* **Outcome:** statuses on the list read open, worked on, done; closing happens through the "mark as done" button.  
* **Value:** the status names describe the work on a thread, and the button says the same thing as the status it sets.  
* **Do NOT touch:** the status transition logic (when a thread gets a status after a session, and so on); this changes labels only.  
* **Done when:** the Threads module UI contains no "touched on" or "close" strings as a thread status or action; the expanded thread has a "mark as done" button; a closed thread has the "done" chip.  
  ---

  ## **CS-05 · CHANGE · Workspace → Threads · expanded thread card: three buttons, including a trash can**

* **Type:** CHANGE  
* **Location:** Workspace → Threads → tap a thread → expanded thread card → the action row. Today the actions are: add to agenda, close, odklik.  
* **What it is:** the expanded thread card (hub-and-spoke) with the context description, sources, and thread actions.  
* **UI anatomy (actions after the change, order from the note):**  
  * **add to agenda** (unchanged)  
  * **mark as done** (label per CS-04)  
  * **trash can icon** (in the note: "usuń" / delete); button styled 1:1 like the trash-can delete button in Goals  
* **Logic:**  
  * add to agenda → tap → the thread appears as a topic for the next session (no change to current behavior).  
  * mark as done → tap → thread closed, "done" chip (logic unchanged, label per CS-04).  
  * trash can → tap → the thread disappears immediately, with no dialog → an "Undo" snackbar ("Cofnij" in the source spec) shows for a few seconds → tapping "Undo" restores the thread in its unchanged state; once the snackbar is gone, the deletion is permanent and irreversible.  
* **Action:** From: three actions, the last being odklik (semi-archive). To: the three buttons from the anatomy; the trash can takes the odklik slot and is a hard delete. A deleted thread cannot be recovered from its source card on the Timeline (unlike odklik). Cleanup after deletion: source cards on the Timeline stay untouched; an agenda item pinned to the deleted thread stays on the list as a plain topic with no thread link.  
* **Outcome:** the user can send a thread to the agenda, close it, or permanently delete it from one place.  
* **Value:** thread deletion works the same as in the other modules (from the note: "like in the rest, e.g. in goals").  
* **Do NOT touch:** odklik in other modules; the delete button in Goals (we copy its style, we do not touch the original); the thread card content outside the action row.  
* **Done when:** the expanded thread shows exactly three buttons in the anatomy order; tapping the trash can deletes with no dialog and shows "Undo"; "Undo" restores the thread; once the snackbar is gone the thread exists in no view, and the Timeline and agenda hold no dead references.  
  ---

  ## **CS-06 · FIX · Multiple screens · active areas of the archive, restore, and refresh buttons**

* **Type:** FIX  
* **Location:** every occurrence of the three icon buttons in the app: archive, restore, refresh. Known spots: the goal card (archive of previous Narratives), restoring a dismissed element from its source card on the Timeline (restore), refreshing the Narrative (refresh). Lead: shared IconButton components; grep the archive/restore/refresh icon names in assets. The fix must cover every occurrence, including ones not on this list.  
* **Now (wrong):** the active area of these buttons is the size of the icon itself, and hitting it with a finger is very hard. **Expected:** a tap area of at least 48×48 dp (Android) and 44×44 pt (iOS) on every occurrence; the icon's artwork and position stay unchanged, only the hit area grows.  
* **Do NOT touch:** how the icons look; the layout of lists and cards around the buttons.  
* **Done when:** every occurrence of these three buttons has an active area of at least 48×48 dp / 44×44 pt (verify with debug paint or the inspector); a tap at the edge of the area triggers the action.  
  ---

  ## **CS-07 · CHANGE · Therapy Relationship · voice check-in: transcript with a preview before saving**

* **Type:** CHANGE  
* **Location:** Therapy Relationship → "+ New Check-In" → voice note recording → the flow from the end of recording to the saved check-in. Both platforms.  
* **What it is:** a relationship check-in can be recorded by voice; the transcript feeds the generated output cards with a rating ("Strong relationship" / "Mixed signals" / "Needs attention"). Today the user never sees the raw text from the voice note and has no control over what went into the save.  
* **Action:** From: saving happens right after recording, with no preview and no visible raw text. To: the same flow as recording a homework (the pattern from the "Unreadable homework recording" edge case in the Workspace spec), steps below.  
* **Flow (in order):**  
  * The user records the voice note; the recording screen itself does not change.  
  * When the recording ends, a preview of the raw transcript appears, editable by hand.  
  * The user confirms → the check-in saves, and the output cards generate from the confirmed text.  
  * Empty transcript → nothing saves or generates; the user gets a prompt to re-record or type instead.  
  * The raw text (after any edits) is stored with the check-in and visible in the check-in's details in history.  
* **Logic:**  
  * Editing the text in the preview → the edited version is what gets saved and fed to generation.  
  * Confirming → save → cards generate from the confirmed text.  
  * Empty transcript → the prompt to re-record or type; the user goes back to recording or switches to text; nothing saves.  
* **AI:** input: the confirmed voice note transcript and nothing else. Output: the check-in's output cards. Trigger: saving the check-in. Failure: empty transcript → generation never starts, the user sees the re-record/type prompt, no red errors.  
* **Outcome:** the user sees and can correct the text the check-in is built from, and can find the raw text later in the details.  
* **Value:** the user knows what the app heard; a bad transcript stops producing a false check-in (from the note: "does not show the raw text from the voice note").  
* **Do NOT touch:** the text check-in; streak, history, and ratings; "+ New Check-In" and "Share my check-ins with my therapist"; the check-in reminder on Main; the homework recording flow (we copy its pattern, we do not touch the original).  
* **Done when:** after recording, an editable transcript preview appears; saving happens only after confirmation; the raw text is visible in the saved check-in's details; an empty transcript ends in the re-record/type prompt and saves nothing.  
  ---

  ## **CS-08 · FIX · iOS · voice check-in never saves ("recording too short or empty")**

* **Type:** FIX  
* **Blocked by:** CS-07  
* **Location:** Therapy Relationship → "+ New Check-In" → voice note recording → validation at save. Platform: iOS. Lead: grep "recording too short or empty".  
* **Now (wrong):** after recording a voice note the check-in never saves, whether or not text appeared on the recording screen. Instead of saving, a notification pops up: "recording too short or empty. please try again.". **Expected:** there is no minimum recording length; the length validation gets removed entirely. Every recording with a non-empty transcript goes through the CS-07 flow and saves, including very short ones (around a second). The only stopping case is a genuinely empty transcript, and that shows the CS-07 re-record/type prompt, not this notification.  
* **Do NOT touch:** the text check-in; recording in other modules (homework, agenda). If the length validation lives in a shared recording component, turn it off for the check-in and leave the other flows as they are.  
* **Done when:** on iOS, there’s no time limit of the recording; the notification "recording too short or empty. please try again." appears nowhere (string removed or dead); an empty transcript leads to the CS-07 flow.  
  ---

  ## **CS-09 · FIX · Android · hallucinations in output cards when the transcript runs late**

* **Type:** FIX  
* **Blocked by:** CS-07  
* **Location:** Therapy Relationship → "+ New Check-In" → voice note recording → output card generation after saving. Platform: Android.  
* **Now (wrong):** if the transcript text does not manage to appear on the recording screen in time, the saved check-in's output cards contain hallucinations and content with no basis in the recording. **Expected:** card generation starts only from the final, confirmed transcript (the CS-07 flow). Saving waits for the transcription result; the CS-07 preview forces this naturally. Empty or incomplete input never reaches the model; no transcript means no generation, and the user gets the re-record/type prompt.  
* **AI:** input: the confirmed transcript only. Failure: empty or missing input → generation does not start.  
* **Do NOT touch:** output card generation for the text check-in; the rating prompt content (this fixes the input, not the prompt).  
* **Done when:** on Android, a recording finished before the text managed to appear produces no content without basis in the transcript; a silence-only test recording ends in the re-record/type prompt and zero cards; cards can only be generated from text that was visible earlier in the preview.  
  