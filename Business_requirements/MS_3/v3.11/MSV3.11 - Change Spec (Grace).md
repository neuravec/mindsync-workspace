# MindSync Change Spec \- MSV3.11 "Threads, Reflect & Grace fixes"

For Claude Code · 31.08.2026 · author: Darek (notes \+ user feedback letter from Grace [nazwisko])

## Context (max 10 lines)

* Sync: backend MindSync (main) and frontend mindsync-frontend (dev) both pulled clean, fully in sync with origin.  
* History read: newest Drive spec "MSV3.10 \- User Feedback Fix" (13.08.2026, items CS-01..03); repo notes: frontend flutter-mobile memory, backend backend-api memory (incl. project\_post\_release\_notif\_fixes\_2026\_08\_16.md).  
* Frontend app code lives in mindsync-frontend/mindsync\_app/; backend paths are relative to MindSync/.  
* MSV3.3 post-release \+ MSV3.4 \+ MSV3.4 Fix.1 rounds are landed and pushed (commits ff20f2a, 1c20e54, df68aa8, 96468f6, 08605e6 on dev; 971f182, 4bb9b2c, de8d538 etc. on main).  
* Stale memory warning: the Main Homework module no longer follows the "2 items, day-after rule" — current code shows up to 5 newest open items via GET /workspace/todos/today (homework\_today\_cubit.dart, kMaxItems \= 5). Trust the code, not old notes.  
* Darek's decisions 31.08 (two rounds of answers): MSV3.10 CS-01 \+ CS-03 stay parked; Threads restructure is forward-only (no data migration) and the triage-accept step stays; Repeat \= same task resets per period (Daily \= local midnight, Weekly \= user's week start, Monthly \= 1st), completion history tracked backend-side; Therapy Schedule fix is end-to-end; Homework is DELETED from Main (a future feature takes its place \- To-dos live in Workspace only); the Stats tab no longer exists, mood trend is Main-only; per-symptom narrative already exists (aiDescription) \- no backend changes for it.

## Previous round \- verification

| ID | Item (short) | Evidence | Status |
| :---- | :---- | :---- | :---- |
| CS-01 (MSV3.10) | Microphone conflict investigation | no commit, no report in either repo's docs/ or agent-memory | NOT FOUND → parked (Darek, 31.08) |
| CS-02 (MSV3.10) | False "unset time" push | backend de8d538 (ADD\_THERAPY\_DATE throttle \+ never-set-vs-passed copy, post-release 16.08); no CS-02-tagged commit; Grace still reports the schedule is not recognized | PARTIAL → folded into CS-10 below |
| CS-03 (MSV3.10) | Workspace Documents section | no commit; grep for Dokumenty/DocumentsSection in frontend returns nothing | NOT FOUND → parked (Darek, 31.08) |

## Summary

* Total items: 11 (DELETE: 1 · FIX: 3 · CHANGE: 7 · VERIFY: 0\)  
* Areas touched: Workspace Threads, Reflect, Workspace To-do, Main (Homework, Mood trend, next-session tile), Timeline, Notifications  
* Intent: this round implements Darek's 31.08 notes and closes all five items from Grace's feedback letter. Threads become a two-level structure with AI matching (Grace \#1), Reflect gets pulled into the rest of the app via a summary output card (Grace \#2), repeating To-do tasks actually recur (Grace \#3), the mood trend module becomes directly editable in the collapsed state (Grace \#4), and the Therapy Schedule chain is fixed end-to-end, display and notifications both (Grace \#5), followed by a full notification-logic audit.

## Global guardrails (read before touching anything)

* Do NOT confuse the Workspace Threads module (lib/screens/workspace/threads/) with the shared Threads section inside output cards (lib/widgets/threads\_section.dart, ThreadsSectionList/ThreadDisplayItem). CS-01 touches the former; the latter stays as it is except where CS-02 reuses it read-only for the new Reflect card.  
* Do NOT confuse the Workspace To-do module with the To-do sections rendered inside output cards. CS-05..08 touch the module only.  
* EmotionalTemperatureItem (lib/api/models/prep\_card/prep\_card\_model.dart, rendered by the Preparation card) is unrelated to the Main mood trend module. Do not touch it in CS-09.  
* The Between Sessions card (between\_session\_note\_widget.dart) is the template for the new Reflect card. Copy its pattern; do not modify the Between Sessions card itself.  
* MSV3.10's notification guardrail still applies: do not add new notification types and do not rebuild the existing reminder schedule. CS-10/CS-11 fix trigger conditions and timing only.  
* Existing Workspace section order stays unchanged.  
* One DELETE this round: CS-08 removes the Main Homework module \- UI-only: TodoItem data, the Workspace To-do module, and the backend endpoints all stay. Other items remove only the specific UI elements they name (progress bar in CS-09, repeat picker inside Edit in CS-05, auto-fired suggestions in CS-03).  
* UI strings: PL labels quoted here are verbatim \- use them for grep and keep them. New labels are working names; produce PL \+ EN, and follow the project ARB convention (literal English into all 7 locales for new keys; reuse one canonical key across call sites).  
* After each item: flutter analyze clean, run the app, confirm no dead references / broken navigation.

---

## CS-01 · CHANGE · \[Workspace, Threads\] Main threads \+ sub-threads with AI matching

* Type: CHANGE  
* Location: Workspace → "Wątki" module. Frontend: lib/screens/workspace/threads/threads\_module\_section.dart, widgets/thread\_card.dart (currently a flat, non-expandable card), threads\_full\_screen.dart, thread\_detail\_screen.dart, cubit/threads\_cubit.dart. Backend: Thread model in app/models/workspace.py (line \~402 \- no parent/group concept exists today), thread creation on triage accept in app/tasks/triage\_proposals.py (POST /workspace/triage/{proposal\_id}/toggle, merge-into-open-thread logic), AI output shape ThreadOutputItem (label/context/is\_continuation) in app/services/openai\_service.py, context regeneration in app/tasks/thread\_context.py. UI pattern to mirror: the Goals module (lib/screens/workspace/goals/goals\_module\_section.dart, workspace\_goal\_card.dart, goal\_detail\_screen.dart).  
* Action: From: flat list of independent threads; every accepted thread proposal either merges into one suggested open thread or creates a new sibling \- which produces Grace's duplicate-title threads that acknowledge being continuations but never join. To:  
  1. Two-level structure: main threads, each expandable (like Goals), each containing sub-threads; each sub-thread carries a short narrative entry.  
  2. When the user adds input, the AI matches the raised content against the existing main threads: fits → new sub-thread under that main thread; doesn't fit → new main thread is created.  
  3. Each sub-thread's narrative must reference the previous sub-thread in that main thread and the thread's overall context (extend app/tasks/thread\_context.py / the ThreadOutputItem generation accordingly).  
  4. Backend needs a parent/child relation on Thread (self-referential FK or equivalent) plus schema/endpoint support in app/schemas/workspace.py, app/api/v1/endpoints/workspace.py, and the frontend ThreadModel (lib/api/models/workspace/thread\_model.dart).  
  5. Forward-only (Darek, 31.08): no migration or AI regrouping of existing data. Existing Thread rows become the initial pool of main threads; new inputs match into them or open new mains. Old duplicates stay as separate mains until content naturally attaches to one of them.  
  6. Triage-accept stays (Darek, 31.08): threads are NOT created fully automatically on input. The AI matching runs when the user accepts a thread proposal (and for "+ Dodaj wątek" input); the accept step itself is unchanged.  
* Why: Grace \#1: "I wish the threads actually expanded so you could see the progression within a single thread. Currently they are listed as separate threads even though the description acknowledges they are a continuation... and the titles are identical."  
* Do NOT touch: lib/widgets/threads\_section.dart (output-card Threads section) except for whatever minimal read-model change is unavoidable; the triage proposal chips UI on output cards; AgendaItem.thread\_id links; the "Domknięte wątki" archive and "+ Dodaj wątek" capture flow (both must keep working \- a manually added thread becomes a main thread).  
* Done when: A main thread on Workspace expands/collapses like a Goal and lists its sub-threads, each with a short narrative referencing the previous one. Accepting new input whose content matches an existing main thread adds a sub-thread under it (no new duplicate-title main thread appears); non-matching content creates a new main thread. Existing user threads still render, unmodified. Build passes on Android \+ iOS; existing thread tests updated and green.  
* Risk: High \- schema change \+ AI-matching logic \+ module rewrite. Biggest item of the round.

## CS-02 · CHANGE · \[Reflect\] "Summaries" button \+ Reflect output card

* Type: CHANGE  
* Location: Reflect conversation: lib/screens/reflect\_tab/reflect\_tab\_screen.dart, input row widgets/reflect\_chat\_input.dart, cubit/reflect\_chat\_cubit.dart. Card template: lib/screens/therapy\_tab/widgets/between\_session\_note\_widget.dart with shared lib/widgets/questions\_section.dart, lib/widgets/threads\_section.dart, lib/widgets/triage\_bookmark\_button.dart/triage\_bookmark\_mixin.dart. Timeline: lib/screens/therapy\_tab/therapy\_tab\_screen.dart (\_FilterChips, \~line 539), enum TherapyFilter in cubit/therapy\_tab\_state.dart:8. Backend: app/api/v1/endpoints/reflect.py (no user-facing summary card exists today \- POST /{id}/end only runs the generic run\_conversation\_analysis pipeline; \_generate\_summary\_from\_messages is an internal context compressor, not a card), timeline serving in app/api/v1/endpoints/timeline.py.  
* Action: Add a mid-conversation summary flow. Element by element, in Darek's order:  
  1. Above the message-input row, add a new row with two buttons side by side: left "Summaries", right "Suggest" (Suggest behavior \= CS-03).  
  2. Tap "Summaries" → pop-out with Headline "Czy chcesz podsumować rozmowę?", Subtext "Po podsumowaniu będziesz mógł kontynuować rozmowę.", below them a ghost button "Not yet" and a colored button "Yes, summaries".  
  3. "Not yet" closes the pop-out. "Yes, summaries" shows an animated spinning loading icon on the button until generation finishes, then opens the summary screen with the generated Reflect output card covering the whole conversation so far.  
  4. Reflect output card structure \= Between Sessions card pattern, sections in order: Podsumowanie rozmowy (conversation summary), Questions, To-do, Threads, Realizations. Same section widgets, same triage-bookmark behavior: items the user saves land in the matching Workspace modules (point 7 of the notes).  
  5. On the card the user can save what they want or close it and return to the conversation. Summarizing does NOT end the thread \- the conversation continues. Repeat summaries (Darek, 31.08): the user may summarize the same conversation again later; each new summary must build on the previous summary's context plus the conversation since it (the "next steps" of the dialogue), producing its own output card. The "ekran z podsumowaniem" IS the opened Reflect output card \- no separate screen.  
  6. Back in the continued conversation, a tile appears: icon \+ text "Your Reflect summary was generated". Tapping it opens the output card on the Timeline; closing the card from that path returns to the conversation.  
  7. The Reflect output card auto-saves to the Timeline. Add a new Timeline filter category "Reflect" (new TherapyFilter member \+ chip \+ timeline item type \+ backend timeline payload). Everything else on Timeline looks and behaves like the existing cards.  
  8. Backend: new summarize endpoint on the Reflect thread (generation of summary/questions/to-do/threads/realizations from the conversation so far), persisted card model, timeline integration. Reuse the existing conversation-analysis structures where they fit; do not repurpose /end.  
* Why: Grace \#2: "I wish the reflect conversation would get reflected in the workspace... The reflect section just feels so separate from the rest of the app." Darek: Reflect gets its own output card on Timeline and its content flows into Workspace.  
* Do NOT touch: The Between Sessions card itself; the /end flow and its run\_conversation\_analysis pipeline (still runs when a thread actually ends); Reflect audio routes and usage limits; existing Timeline categories and their filtering.  
* Done when: In an active Reflect conversation the two-button row shows above the input; the pop-out copy matches verbatim; "Yes, summaries" shows the spinner then the card; the card has the 5 sections and saving an item places it in the right Workspace module; the tile appears in the continued conversation and round-trips to the Timeline card and back; the card appears on Timeline under a working "Reflect" filter chip; conversation remains usable after summarizing. Build passes both platforms.  
* Risk: High \- new backend generation \+ new card type \+ Timeline category. Second-biggest item.

## CS-03 · CHANGE · \[Reflect\] "Suggest" button \- Helpful prompts on demand only

* Type: CHANGE  
* Location: lib/screens/reflect\_tab/cubit/reflect\_chat\_cubit.dart \- refreshStarters() (\~line 534\) is auto-called after every sent message (\~line 406); chips rendered via widgets/reflect\_starter\_chips.dart in reflect\_tab\_screen.dart (eyebrow key chat\_suggestionsEyebrow, EN "Helpful prompts" / PL "Pomocne pytania"). Backend GET /reflect/starters stays as is.  
* Action: From: Helpful prompts appear automatically after every user message. To: they appear only after tapping the new right-hand "Suggest" button (CS-02's button row). Tap → fetch and show the same chips in the same place. This is a relocation of the whole existing functionality into the button \- remove the auto-trigger after each message, change nothing about how prompts are generated or rendered.  
* Why: Darek's notes: move the entire Helpful prompts functionality into the Suggest button.  
* Do NOT touch: The empty-thread starter chips shown before a conversation begins (same widget, different moment \- they stay automatic; confirmed by Darek, 31.08); the GET /starters backend logic; the chip design.  
* Done when: Sending a message no longer surfaces prompts by itself; tapping "Suggest" shows them; empty-thread starters unchanged. Existing cubit tests updated.  
* Risk: Low.

## CS-04 · CHANGE · \[Reflect\] Mic icon → phone handset icon

* Type: CHANGE  
* Location: lib/screens/reflect\_tab/widgets/reflect\_chat\_input.dart (\~line 191): Icons.mic\_none on the input row.  
* Action: In the open Reflect conversation, replace the microphone icon with a phone-handset icon. All icon parameters (size, color, position, tap behavior, isMicLoading state) stay identical \- icon-only swap.  
* Why: Darek's UI note.  
* Do NOT touch: \_handleMicTap behavior, voice mode itself, mic icons anywhere else in the app (capture sheets, recording screens).  
* Done when: The Reflect input row shows a handset icon with unchanged behavior; no other screen's icon changed.  
* Risk: Low.

## CS-05 · CHANGE · \[Workspace, To-do\] "Repeat" moves from Edit into the three-dots menu

* Type: CHANGE  
* Location: Three-dots menu: lib/screens/workspace/widgets/workspace\_item\_menu.dart (shared PopupMenuButton \- "Edytuj", "Dodaj do agendy", archive, delete). Edit sheet: lib/screens/workspace/widgets/voice\_or\_text\_capture\_sheet.dart \- the showRepeatControl block currently renders the "Powtarzaj" picker inside Edit and saves via onSaveWithRepeat(text, repeatFreq, description). Cubit: lib/screens/workspace/todo/cubit/todo\_cubit.dart (editItem({..., repeatFreq})).  
* Action: From: repeat frequency is chosen inside the Edit sheet. To:  
  1. Remove the repeat picker from Edit (everything else in Edit stays as today).  
  2. Add a "Repeat" entry to the three-dots menu for To-do items only (the menu is shared with other modules \- gate it).  
  3. Tapping Repeat slides a drawer from the bottom containing only the repeat choice: title "Repeat", subtext "Wybierz z jaką częstotliwością ma pojawiać się to zadanie.", choice buttons "Don't repeat", "Daily", "Weekly", "Monthly", and a save button. Saving persists via the existing repeatFreq path (PUT /workspace/todos/{id}).  
* Why: Darek's notes \- Repeat gets its own menu position.  
* Do NOT touch: The rest of the Edit sheet (text, "Opis" description field); the three-dots menu entries of Threads/Goals/other modules; the backend repeat\_freq column semantics.  
* Done when: Edit no longer offers repeat; the To-do three-dots menu shows Repeat; the drawer matches the anatomy above and saving updates the task; other modules' menus unchanged.  
* Risk: Low-Medium (shared menu widget \- gate carefully).

## CS-06 · CHANGE · \[Workspace, To-do\] Repeat pill on every task \+ "Don't repeat" default

* Type: CHANGE  
* Location: lib/screens/workspace/todo/widgets/todo\_item\_tile.dart \- a repeat chip (Icons.repeat \+ label, \~lines 167-172) already exists for repeating tasks. Model: lib/api/models/workspace/todo\_item\_model.dart:26 (String? repeatFreq); backend TodoItem.repeat\_freq (app/models/workspace.py:330, nullable).  
* Action: From: chip shown only when a repeat frequency is set. To: every task on the To-do list carries the small pill (repeat icon \+ text of the chosen interval: "Don't repeat", "Daily", "Weekly" or "Monthly"). All newly added tasks default to "Don't repeat" (repeat\_freq \= null maps to the "Don't repeat" pill \- no schema change needed).  
* Why: Darek's notes; makes the repeat state visible per task.  
* Do NOT touch: Checkbox/check-off animation, the tile's other elements, the archive ("Zrobione") flow.  
* Done when: Every To-do row shows a pill incl. "Don't repeat" for null; a newly added task shows "Don't repeat" without user action.  
* Risk: Low.

## CS-07 · FIX · \[Workspace, To-do\] Repeating tasks actually recur

* Type: FIX  
* Location: Backend: TodoItem.repeat\_freq \+ the todo\_completions table (app/models/workspace.py:379 \- already logs each completion) \+ /done, /undone, GET /todos/{id}/completions routes in app/api/v1/endpoints/workspace.py. Frontend: todo\_cubit.dart (homework\_today\_cubit.dart is deleted by CS-08 \- don't extend it).  
* Now (wrong): Grace \#3: "daily homework appears once, labeled as a daily task, and then never again" \- a checked-off repeating task never comes back.  
* Expected (Darek, 31.08 \- "same task resets"): One task row per repeating task. At the start of each new period its checkbox resets to unchecked; no duplicate entries accumulate. Period starts (confirmed by Darek, 31.08): Daily → local midnight; Weekly → start of the user's week (respect the existing week-start preference, week\_start\_selector.dart); Monthly → 1st of the calendar month. Each check-off is logged in todo\_completions with its timestamp, and the backend must expose how many times and when the task was done, so the app can display it correctly and the completion history feeds the user's AI context (Reflect and analysis) \- Darek's explicit requirement.  
* Action: Implement the period-reset logic (backend-driven so it works regardless of app opens; the frontend renders whatever the backend says is currently open/checked). Keep todo\_completions as the source of history; surface completion count/dates in the task payload where the UI and the AI context builders can reach them.  
* Do NOT touch: Non-repeating tasks (unchanged lifecycle); the archive flow for completed one-off tasks; HOMEWORK\_REMINDER notification logic (CS-11 audits it separately).  
* Done when: A Daily task checked today is unchecked again tomorrow (device date change / backend day rollover test), same single row, no duplicates; Weekly/Monthly reset on their period starts; GET /todos/{id}/completions (or the task payload) shows the full check-off history; the Reflect/AI context can see completion stats. Verified on Android \+ iOS.  
* Risk: Medium \- date/timezone logic; test with device timezone changes (precedent: naive-vs-aware datetime gotchas in therapy\_schedule\_utils.py).

## CS-08 · DELETE · \[Main, Homework\] Delete the Homework module from Main

* Type: DELETE (UI-only: module widget \+ cubit go; data and Workspace To-do stay). Emergency edit by Darek, 31.08 \- this replaces the earlier plan to copy the To-do module onto Main.  
* Location: lib/screens/main\_tab/widgets/homework\_today\_card.dart \+ lib/screens/main\_tab/cubit/homework\_today\_cubit.dart. Wired in lib/screens/main\_tab/main\_tab\_screen.dart: imports (lines 18, 25), cubit load (sl\<HomeworkTodayCubit\>().load(), \~line 123), module registry entry 'homework\_today': const HomeworkTodayCard() (\~line 442). Check DI registration in lib/core/service\_locator.dart and any homework references in main\_tab\_cubit.dart. Deep link: lib/screens/moments/moment\_deep\_link\_screen.dart:164 handles MomentType.homeworkReminder (shared case branch).  
* Action: Remove the Homework module from the Main tab entirely: card widget, cubit, DI registration, registry entry, cubit load call. To-dos live in Workspace only from now on. The MomentType.homeworkReminder deep link must land on the Workspace To-do module afterwards \- verify the branch at moment\_deep\_link\_screen.dart:164 and retarget if it currently opens Main. Backend GET /workspace/todos/today loses its only caller \- leave the endpoint in place (a later feature may use it) and flag it as unused.  
* Why: Darek, 31.08: a feature planned for a later round will take this place on Main; keeping one To-do surface avoids building UI that gets replaced.  
* Do NOT touch: The Workspace To-do module and everything CS-05..07 build there; TodoItem data and all other /workspace/todos endpoints; the HOMEWORK\_REMINDER notification type and its settings toggle (notifications\_section.dart) \- the reminder stays, only its landing place changes; other Main modules and their order.  
* Done when: Main no longer shows the Homework module; a HOMEWORK\_REMINDER notification opens the Workspace To-do module; app builds; grep for HomeworkTodayCard / HomeworkTodayCubit returns no live references; no dead imports or DI entries.  
* Risk: Low-Medium \- clean removal, but the deep-link retarget must be verified on both platforms.

## CS-09 · CHANGE · \[Main, Mood trend\] Slider replaces progress bar; expanded view \= narrative \+ timeline

* Type: CHANGE  
* Location: lib/screens/main\_tab/widgets/mood\_trend\_card.dart (wrapper \+ \_MoodTrendSummary AI header from GET /dashboard/mood-trend) → the real module is lib/screens/stats\_tab/widgets/unified\_symptom\_module.dart. Main is its only live surface (confirmed by grep: only mood\_trend\_card.dart embeds it; the stats\_tab/ folder path is historical \- the Stats tab no longer exists, Workspace replaced it). Collapsed row today \= progress bar with trend color/arrow (\_computeTrend, \_barColor) \+ Icons.expand\_more chevron (\~line 492); expanded \_SymptomExpand (\~line 534\) today \= 1-10 slider \+ "Update rating" CTA → SymptomTrackingCubit.updateScore (\~line 563). Chart: lib/widgets/charts/symptom\_score\_chart.dart (SymptomScoreChart, driven by symptom.scores). Per-symptom narrative already exists: aiDescription \+ aiDescriptionGeneratedAt on lib/api/models/symptom/symptom\_card\_model.dart.  
* Action: Restructure the per-symptom row:  
  1. Collapsed state: each symptom shows a visible slider for changing the rating INSTEAD OF the current progress bar \- the progress bar is removed. After the user moves the slider, an update-rating button slides out below that specific symptom; the user must confirm for the rating to save (uses the existing updateScore path). No confirm → no save.  
  2. Expanded state: shows a narrative plus a timeline ("linia czasu" \- the SymptomScoreChart score-series over time). The slider/CTA that lived here moves to the collapsed row. The narrative is the existing per-symptom aiDescription \- Darek, 31.08: "per-symptom is doing fine, don't make any changes" \- so NO backend changes for the narrative, display only.  
  3. The expand/collapse chevron is placed inside a round button (same chevron up/down semantics).  
* Why: Grace \#4: "I found the mood trend chart unintuitive. It took me a little while to realize how to update my current ratings."  
* Do NOT touch: EmotionalTemperatureItem / the Preparation card's mood section; the \_MoodTrendSummary module-level AI paragraph; symptom management (add/remove) in symptom\_management\_sheet.dart; the aiDescription generation pipeline on the backend (no changes \- display only); backend symptoms.py / dashboard.py endpoints.  
* Done when: Collapsed symptom rows show sliders (no progress bars anywhere in the module); moving a slider reveals a confirm button below that symptom and only confirming saves; expanded view shows the existing aiDescription narrative \+ score timeline; chevron sits in a round button. Existing symptom tests updated and green. No backend diff for this item.  
* Risk: Low-Medium \- frontend-only rework of one module on one surface (Main).

## CS-10 · FIX · \[Notifications \+ Main\] Therapy Schedule end-to-end

* Type: FIX (end-to-end scope confirmed by Darek, 31.08)  
* Location: Backend: schedule storage on UserPreferences (app/models/models.py:214-219: therapy\_schedule JSON, therapy\_frequency weekly|biweekly|custom, custom\_interval\_days, next\_session\_date, custom\_therapy\_sessions), PUT/GET /users/therapy-schedule (app/api/v1/endpoints/users.py:1403/1427), recompute logic in app/crud/crud.py:1201-1370, canonical math in app/utils/therapy\_schedule\_utils.py (compute\_next\_session\_date etc.), notification generators in app/services/moments/ (therapy\_appointment\_generator.py, add\_therapy\_date\_generator.py, therapy\_prep\_generator.py, post\_session\_reflection\_generator.py, ...) \+ app/services/notification\_orchestrator.py. Frontend: schedule editors lib/screens/settings/widgets/therapy\_schedule\_section.dart (reused by my\_therapy\_screen.dart) and lib/screens/main\_tab/widgets/session\_setup\_screen.dart; the Main next-session tile computes the date entirely client-side from SharedPreferences in lib/screens/main\_tab/cubit/main\_tab\_cubit.dart → \_computeNextSession (\~line 618\) \- it never reads the backend's next\_session\_date, duplicating therapy\_schedule\_utils logic. Empty state renders at main\_tab\_screen.dart:1268, key mainTab\_noUpcomingSessions (EN "No upcoming sessions scheduled" / PL "Brak zaplanowanych sesji."). Known history: a "therapy\_schedule always \[\]" data-loss bug documented at lib/api/models/settings/therapy\_schedule\_entry.dart:9.  
* Now (wrong): Grace \#5: "It continues to tell me 'no upcoming sessions scheduled,' though I have tried to schedule it multiple times in the app." Darek: notifications don't see the scheduled therapy for ANY frequency mode (weekly, biweekly, custom).  
* Expected: Scheduling therapy in any of the three modes results in (a) the schedule persisting, (b) the Main tile showing the computed next session, and (c) session-related notifications firing according to the session's date and time, so every notification's flow matches the schedule mode.  
* Action: Investigate and fix the whole chain, in order: does the saved schedule reach the backend and persist (re-check the documented therapy\_schedule data-loss path); does next\_session\_date recompute correctly per mode (weekly \_next\_weekly\_occurrence, biweekly \_is\_on\_week anchor parity, custom \_compute\_next\_custom); does the frontend display read state that agrees with the backend (strongly consider making the Main tile read the backend-computed next session instead of its duplicated SharedPreferences math \- divergence here is the most likely cause of Grace's symptom); do the schedule-driven notification generators see the schedule and fire relative to the session datetime for all three modes. Fix causes, not symptoms. Timezone-shift testing is mandatory (existing naive-vs-aware precedents in therapy\_schedule\_utils.py).  
* Also closes: the remainder of MSV3.10 CS-02 \- after saving a session time, the "unset time" (ADD\_THERAPY\_DATE) push must not fire; after clearing it, it may return under the existing rule.  
* Do NOT touch: Notification types, lead times, copy, and the settings screen (MSV3.10 guardrail: no new notifications, no schedule rebuild); the schedule editor UIs beyond what the persistence fix requires.  
* Done when: For each mode (weekly, biweekly, custom): schedule a session → Main shows the next session (not "Brak zaplanowanych sesji." / "No upcoming sessions scheduled"), survives app restart and device timezone change; session notifications arrive per the session's date/time; the "unset time" push does not fire while a time is set; verified on Android \+ iOS. Grace's exact repro (schedule multiple times, then check the tile) passes.  
* Risk: High \- touches persistence, computation, display, and notification eligibility across both repos.

## CS-11 · FIX · \[Notifications\] Notification-logic autoanalysis \+ daily/weekly cycle corrections

* Type: FIX (with a mandatory audit deliverable first)  
* Location: Backend: app/services/notification\_orchestrator.py, all generators in app/services/moments/ (13 files: therapy\_appointment, add\_therapy\_date, therapy\_prep, post\_session\_reflection, record\_session, between\_sessions\_note, homework\_reminder, mood\_update\_request, mood\_dip\_alert, therapy\_relationship\_checkin, re\_engagement, reflection\_invitation, account\_setup\_nudge), MomentTypeEnum in app/models/notification\_moment.py:41 (note: SESSION\_MORNING\_OF is retired \- enum member kept for historical rows only; there is no SESSION\_REMINDER type). Prior art: post-release review analytics-reports/2026-08-16-post-release-review-12-08.md and the CooldownGiveUpThrottle mixin (commit de8d538).  
* Action: Darek: "Zrob autoanalysis logiki notyfikacji one more time." Re-analyze the display logic of every notification type and deliver a short audit report answering: (1) do any types overlap / fire together without reason; (2) does each type trigger for the right feature and at the right time; (3) are the daily and weekly cycles of all notifications correct. Then fix the daily and weekly cycle defects the audit finds ("Poprawic cykl dzienny i tygodniowy notyfikacji. wszystkich"). Run this AFTER CS-10 lands, since the schedule fix changes what several generators see. Known open lead from the 16.08 review (verify, don't assume): REFLECTION\_INVITATION and THERAPY\_RELATIONSHIP\_CHECKIN share the "iterate every user, \~98% expire unsent" shape and were flagged as mixin candidates.  
* Why: Darek's notes; complements CS-10 so the whole notification layer behaves predictably.  
* Do NOT touch: Notification copy and the settings screen; do not add new notification types; do not change lead times except where the audit shows a cycle is objectively wrong.  
* Done when: The audit report exists (per-type: trigger condition, timing, overlap verdict, daily/weekly cycle verdict) and every cycle defect it lists is either fixed in this round or explicitly parked with a reason; no two notification types fire for the same trigger without documented intent.  
* Risk: Medium \- behavior changes ripple to all users; lean on notification\_logs/push\_delivered reconciliation (already in place) for before/after evidence.

---

## Open Questions (resolve before or during execution)

All eight authoring-time questions were answered by Darek on 31.08 and are folded into the items above. What remains:

1. GET /workspace/todos/today: after CS-08 the endpoint has no caller. It stays in place (Darek's later feature may use it); flag for deletion in a future round if it stays unused.  
2. HOMEWORK\_REMINDER landing: CS-08 requires the deep link to land on Workspace To-do; CS-11's audit should confirm the reminder's trigger conditions still make sense with no Main homework surface.  
3. Parked from MSV3.10 (Darek, 31.08): CS-01 microphone-conflict investigation and CS-03 Documents section remain open and unstarted \- carry them on the backlog for a future round.

## Suggested execution order

1. CS-04 (icon swap \- trivial, isolated)  
2. CS-08 (Homework delete \- small, isolated, frees the Main layout early)  
3. CS-03 (Suggest button \- low risk; UI row is shared with CS-02, build the row here)  
4. CS-05 → CS-06 → CS-07 (Repeat: menu move, pill, then recurrence fix \- one coherent To-do batch)  
5. CS-09 (Mood trend redesign \- frontend-only)  
6. CS-10 (Therapy Schedule end-to-end \- biggest fix, both repos)  
7. CS-11 (notification audit \+ cycle fixes \- strictly after CS-10; includes the HOMEWORK\_REMINDER sanity check from CS-08)  
8. CS-01 (Threads restructure \- schema \+ AI matching)  
9. CS-02 (Reflect output card \- after CS-01 so the card's Threads section and Workspace saves target the new thread structure)

