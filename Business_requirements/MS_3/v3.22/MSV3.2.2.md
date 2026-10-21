# MindSync Change Spec: MSV3.2.2 Notifications & Settings Fix 1 (23.07.2026)

*For Claude Code · 2026-07-23, updated 2026-07-24 · author: Darek (notes \+ answers \+ review round), compiled with zero open questions*

## Summary

- Total items: 7 (DELETE: 2 · FIX: 1 · CHANGE: 4\)  
- Areas touched: app-wide deep links (section IDs) · Settings → Notifications screen · the notification set and its backend logic · system notifications  
- Sources: Darek's notes of 23.07 on the in-app notifications screen and settings, plus one question round. This is a new document series next to the MSV3.2 Fix chain; it references that chain where the two meet (session state machine, summaries, week definition).  
- Intent: the notification screen gets cleaned up and reordered now that the notification set has sensible logic. One list under one header, every row a title, a short description and a toggle, thirteen notifications in a fixed order with defined triggers and tap targets that actually open the right feature. Insights, Streaks and the whole Quiet hours section leave the app. One new system nudge reminds fresh accounts to finish their setup. On top of that, every notification the app sends, listed here or not, must land on the specific input card it targets; today none of them lead anywhere sensible.

## Global guardrails (read before touching anything)

- Stay inside the notifications domain: the Settings → Notifications screen, the notification scheduling and sending logic, and the deep-link anchors. Do not touch other Settings sections.  
- Notifications link INTO features; they do not change them. The Workspace modules, the capture flows, Mood Trend, Goals, Reflect, Therapy Relationship and the summary cards stay exactly as their own specs left them. A tap opens a screen; nothing more.  
- The settings session data model stays untouched (protected since Fix 2 CS-09). The 60-minute session length in CS-03 is a computed assumption, not a new field.  
- Dependency: the Weekly summary and Monthly summary notifications (CS-03 rows 12 and 13\) can only fire once MSV3.2 Fix 4 CS-03 (the summary cards) is live. Build them behind that precondition; they must not fire while there is no card to open.  
- The OS notification permission flow is out of scope; only the in-app screen and sending logic change.  
- All \[notification title\] and \[notification subtext\] strings below are final UI copy. Typo corrections against the raw notes are listed in the Decisions log, flagged for veto.  
- After each item: run the app on Android and iOS, confirm no dead references and no broken navigation.

---

- 

---

## B · Settings → Notifications screen

### CS-02 · CHANGE · \[Settings → Notifications\] · The "Notify me about:" list: header, row anatomy, order, defaults, spacing

- **Type:** CHANGE  
- **Blocked by:** CS-03 (the rows render the titles, subtexts and toggles of the notification set defined there).  
- **Re-work of:** none; the selectable-notifications group as it is live today.  
- **Location:** Settings → Notifications screen → the selectable notifications group (currently headed "What interests you?"). Reached: Settings → Notifications. Lead: grep "What interests you?".  
- **What it is:** The list where the user picks which notifications they want. Today it carries stale entries, loose spacing and the old header.  
- **UI anatomy (target):**  
  1. Group header, final string: **"Notify me about:"** (replaces "What interests you?").  
  2. One row per notification, in exactly the CS-03 order (rows 1 to 13). Per row, top to bottom and left to right:  
     1. \[notification title\] as the row name  
     2. under it, the short \[notification subtext\]  
     3. on the right, a toggle on/off  
  3. Vertical spacing between rows reduced against today's layout (tighter list, same information).  
- **Logic:**  
  - Toggle → tap → that notification (all its pushes) turns on or off; state persists.  
  - Rows 1 (Therapy appointment) and 4 (Prepare for therapy) each cover two scheduled pushes; the row's single toggle controls both of its pushes (decision).  
  - Default state: every notification on. This is the fresh-install default; existing users keep the choices they already made, and rows that are new to them arrive on (decision, flagged for veto).  
- **Outcome:** One tidy list under one plain header: what MindSync notifies about, in a deliberate order, each row switchable.  
- **Value:** "Pozbyć się głupot i poustawiać, teraz skoro już mamy sensowne notyfikacje z sensowną logiką." (Darek)  
- **Do NOT touch:** The top-of-screen banner (CS-05 owns its color, nothing else changes); the rest of the Settings → Notifications screen beyond this group and CS-06's deletion.  
- **Done when:** A fresh install shows the header "Notify me about:" and 13 rows in CS-03 order, each with title, subtext and toggle, all on, with visibly tighter spacing; grep "What interests you?" returns no live reference; toggling any row on and off persists across app restarts; both platforms.

### CS-05 · CHANGE · \[Settings → Notifications\] · Top banner: color to alert category 2 (yellow)

- **Type:** CHANGE  
- **Re-work of:** none; UI note of 23.07.  
- **Location:** Settings → Notifications screen → the banner rendered at the top of the screen (the single banner above the list). Reached: Settings → Notifications. Lead: grep the banner widget at the top of the notifications screen.  
- **What it is:** The notice banner at the top of the notifications screen. Its current color does not match the alert palette.  
- **Action:** From: the banner's current color. To: the design system's category 2 alert color, yellow ("alert 2 kategorii, czyli żółty", Darek). Content, copy and behavior stay as they are; only the color changes.  
- **Outcome:** The top banner reads as a standard category 2 alert.  
- **Value:** Consistent alert coloring on the notifications screen.  
- **Do NOT touch:** The banner's text and tap behavior; banners elsewhere in the app; the alert palette itself.  
- **Done when:** A screenshot of Settings → Notifications shows the top banner in the category 2 yellow on both platforms; no other banner changed.

---

## C · The notification set

### CS-03 · CHANGE · \[Notifications \+ backend\] · The 13 notifications: final copy, logic, tap targets

- **Type:** CHANGE  
    
- **Blocked by:** CS-01 (every tap target below needs its anchor working).  
    
- **Re-work of:** the live notification set, including three renames with backend updates: "Therapy prep" → **"Prepare for therapy"**, "Reflections" → **"Reflect"**, and "Summaries" → split into **"Weekly summary"** \+ **"Monthly summary"**.  
    
- **Location:** The notification definitions: their titles, subtexts, scheduling logic and tap routing. Surface: the CS-02 list renders rows 1 to 13 in this exact order. Lead: grep the current notification registry and the strings "Therapy prep", "Reflections", "Summaries", "insights", "streaks".  
    
- **What it is:** The full set of user-selectable notifications. Titles and subtexts below are final UI strings; each row also defines its trigger and where its tap lands.  
    
- **UI anatomy (the set, in list order; per row: title · subtext · logic · tap):**  
    
  1. **Therapy appointment** (two separate pushes: 1 day before and 3 hours before)  
     - Subtext: "Remind me of next upcoming session (a day before and 3 hours before)."  
     - Logic: with a next session set, one push 1 day before its start and one push 3 hours before its start. One row, one toggle, both pushes.  
     - Tap → Workspace → Next session agenda (anchor 1).  
  2. **Add a therapy date**  
     - Subtext: "Notify me if I don't select a date for an upcoming session."  
     - Logic: while the user has no next session set, one push per day until they add one.  
     - Tap → the therapy date setup in Settings (anchor 2).  
  3. **After therapy**  
     - Subtext: "Receive a reminder 15 minutes after a session ends, to take therapy notes with fresh memory."  
     - Logic: session end is computed as start \+ 60 minutes (decision), so the push fires 75 minutes after the session's start time. Skipped when the After Therapy entry for that session is already done (decision, flagged for veto).  
     - Tap → the After Therapy note input (anchor 3; the notes' "prepare for therapy date input screen" was a paste slip, corrected in the question round).  
  4. **Prepare for therapy** (two separate pushes: 1 day before and 3 hours before)  
     - Subtext: "Remind me to prepare for an upcoming therapy session 1 day and 3 hours before."  
     - Logic: with a next session set, one push 1 day before and one push 3 hours before its start. Rename from "Therapy prep", backend updated to this schedule. Skipped when the prep card for that session already exists (decision, flagged for veto; mirrors the "View prep card" state of the session state machine). Overlap with row 1 at the same moments is intended; the rows say different things and toggle separately (decision).  
     - Tap → the Prepare for Therapy data input flow (anchor 4).  
  5. **Between sessions**  
     - Subtext: "Remind me to add a note between sessions if I didn't." (trimmed against the notes to match the chosen logic; decision, flagged for veto)  
     - Logic: "Prostu codziennie" (Darek): one push per day while the Between Sessions window is active (After Therapy completed, next session known, more than 3 days to it, per the CS-09 state machine) and no between-sessions note exists for this cycle. Adding a note stops the series; the window ending stops it too. Window scope confirmed in the review round, 24.07: a skipped debrief means no note reminders.  
     - Tap → a new, opened Between Sessions note input (anchor 5).  
  6. **Record a session**  
     - Subtext: "Right before a session, remind me to record it."  
     - Logic: one push 3 minutes before the session's start time.  
     - Tap → Record a session, ready to record (anchor 6).  
  7. **Homework**  
     - Subtext: "Notify me if I have unfinished homework from a therapist."  
     - Logic: 3 days before the upcoming session, one push if any unchecked To-do task labeled "from a therapist" exists.  
     - Tap → Workspace → To-do, scrolled to the section (anchor 7).  
  8. **Mood trends**  
     - Subtext: "If you haven't updated your mood trends in 3 days, the app will remind you to update."  
     - Logic: fires when 3 days pass without a mood trends update, and again after each further 3 update-free days (rolling; decision). Watches the same data the reworked Mood Trend module uses (Fix 3 CS-11 and CS-12; "update mood trends logic to new mood trends logic").  
     - Tap → Mood trends, scrolled to the section (anchor 8).  
  9. **Reflect**  
     - Subtext: "Remind me to have a conversation about my therapy with MindSync."  
     - Logic: rename from "Reflections". Once a week, only if the Reflect feature was not used that week (week \= Monday to Sunday, user's timezone, per the Fix 4 convention).  
     - Tap → a new Reflect conversation (anchor 9).  
  10. **Goals**  
      - Subtext: "Remind me to check how my therapy goals have progressed, once a week."  
      - Logic: fires when the weekly goals update is done.  
      - Tap → the Therapy goals section, scrolled to it, showing the updated narrative (anchor 10).  
  11. **Therapy relationship**  
      - Subtext: "Remind me once a week to check the health of the relationship with my therapist."  
      - Logic: once a week, only if no relationship check-in was done that week.  
      - Tap → the new check-in data input card in Therapy Relationship (anchor 11).  
  12. **Weekly summary**  
      - Subtext: "How my therapy journey is going. Let me know when my weekly summary is ready."  
      - Logic: fires when the weekly summary card has generated (split of the old "Summaries" notification, backend updated). Delivery hour: a card generated between 21:00 and 8:00 sends its push at 8:00, a card generated in the daytime pushes at once (decision, 24.07). Precondition: MSV3.2 Fix 4 CS-03 live; never fires without a card to open.  
      - Tap → the newest Weekly summary card (anchor 12).  
  13. **Monthly summary**  
      - Subtext: "How my therapy journey is going. Let me know when my monthly summary is ready."  
      - Logic: fires when the monthly summary card has generated (same split, backend updated). Same delivery-hour rule and the same precondition.  
      - Tap → the newest Monthly summary card (anchor 13).


- **Logic (cross-cutting):**  
    
  - Day-precision pushes with no natural hour (rows 2, 5, 7, 8, 9, 11\) fire at one shared local hour: 18:00, kept as a single constant (decision, flagged for veto). CS-07 is the exception: it fires in 24-hour steps from account creation, per Darek's verbatim answer. Event-anchored pushes (rows 1, 3, 4, 6, 10, 12, 13\) fire at their computed moments.  
  - Weekly checks (rows 9 and 11\) evaluate and fire on Sunday at the shared hour, judged against the Monday-to-Sunday week (decision, 24.07).  
  - Only future moments get scheduled: when a session is created or changed, push moments already in the past (a session added 2 hours ahead has its 1-day-before moment behind it) are skipped, never sent late (decision, flagged for veto).  
  - Toggle-state migration: renamed notifications keep the user's previous on/off state; the "Summaries" state carries into both new rows; rows that are new to an existing user arrive on (decision, flagged for veto).


- **Outcome:** Every push has one clear reason, one moment, and a tap that lands exactly on the feature it talks about.  
    
- **Value:** "Głównie w tym fixie chodzi o to, żeby naprawić wewnątrz aplikacji screena z notyfikacjami, pozbyć się głupot i poustawiać." (Darek)  
    
- **Do NOT touch:** The features behind the anchors; the session data model (the 60-minute end is computed); the OS permission flow; the CS-02 list rendering beyond feeding it these rows.  
    
- **Done when:** Each of the 13 rows fires per its logic line in a test pass (stale entries gone: grep "Therapy prep", "Reflections", the unsplit "Summaries" returns no live notification IDs); each tap lands on its anchor; rows 3 and 4 skip when their skip condition holds; rows 12 and 13 stay silent until Fix 4 CS-03 is live, then fire on generation; toggle states migrate per the rule; both platforms.

### CS-04 · DELETE · \[Settings → Notifications \+ backend\] · "Insights" and "Streaks" notifications

- **Type:** DELETE  
- **Re-work of:** none; note of 23.07 ("usuń 'insights' oraz 'streaks' razem z logiką na backendzie").  
- **Location:** Settings → Notifications → the selectable notifications group → the "Insights" and "Streaks" entries, plus their backend scheduling and sending logic. Reached: Settings → Notifications. Lead: case-insensitive grep "insights" and "streaks" in the notification registry, scheduler and strings.  
- **Action:** Full removal, UI and supporting logic: both rows leave the list, their scheduled jobs and triggers leave the backend, nothing sends. Stored history of past sends may remain.  
- **Do NOT touch:** Any feature named Insights or Streaks outside the notifications domain, if grep finds one; the other 13 rows.  
- **Done when:** Neither row renders; no insights or streaks push can be scheduled or sent; case-insensitive grep in the notifications domain returns no live reference; both platforms.

---

## D · System notifications

### CS-07 · CHANGE · \[Notifications, system\] · New-account setup nudge

- **Type:** CHANGE  
- **Blocked by:** CS-01 (anchor 14).  
- **Re-work of:** none; new notification from the notes of 23.07 ("po założeniu nowego konta, aplikacja wysyła notyfikację przypominającą o uzupełnieniu danych, np. nie masz goalsa → dodaj goalsa").  
- **Location:** The system notification group (not in the CS-02 toggle list; decision). Trigger side: account creation. Reached: create a fresh account, add no data.  
- **What it is:** A setup reminder for fresh accounts whose key data is still missing. Darek's example: no goal set.  
- **Logic:**  
  - Schedule: up to 4 pushes, one every 24 hours from account creation (t+24h, t+48h, t+72h, t+96h). Each push sends only if the key data is still missing at that moment; completing the data ends the series early; after the fourth touch the series ends for good ("4 dotknięcia, każde po 24 godzinach, dopóki nie będą uzupełnione rzeczy", Darek).  
  - Scope of "missing key data": a missing therapy goal (Darek's named example). The therapy date is excluded: row 2 of CS-03 already nags for it daily (decision, flagged for veto).  
  - Copy, draft flagged for veto: title "Add your first goal", body "Set a therapy goal so MindSync can track your progress."  
  - Tap → Goals setup (anchor 14).  
  - System-level: always active, no toggle row (decision).  
- **Outcome:** A fresh account that stalls after signup gets up to four daily nudges toward its first goal, then MindSync stops asking.  
- **Value:** New users who never set a goal get a reason to come back and finish setup.  
- **Do NOT touch:** The Goals feature itself; the CS-02 list (this notification does not appear there); the "Add a therapy date" notification, which keeps owning the date nag.  
- **Done when:** A fresh account with no goal receives pushes at t+24h, \+48h, \+72h, \+96h and nothing after; adding a goal mid-series stops the remaining pushes; the tap lands on Goals setup; the notification appears in no toggle list; both platforms.

---

## A · Deep links

### CS-01 · FIX · \[App-wide\] · Tap routing: every notification in the app lands on its target input card

- **Type:** FIX  
- **Re-work of:** none; General fix from the notes of 23.07, widened on 24.07: fix every notification in the app, including ones this spec does not list.  
- **Location:** The deep-link layer between a notification tap and the app's screens and sections. Reached: tap any MindSync push. Lead: grep the existing notification tap handlers and the section/anchor IDs they reference.  
- **Now (wrong):** Section IDs are broken, so a notification cannot open the app at the height of a specific feature ("trzeba naprawić ID sekcji tak, żeby notyfikacje mogły otwierać aplikację już na wysokości konkretnego feature", Darek), and tap routing is broken across the board: "Obecne notyfikacje nie przenoszą do żadnego sensownego miejsca." (Darek, 24.07.) Taps land the user somewhere generic instead of on the input card the push talks about.  
- **Expected:** Two layers. First, audit: grep the full notification registry and list every notification the app can send, including system and legacy ones this spec does not name. Second, fix: every notification's tap opens the app on the specific input card or section it targets, scrolled to it, on cold start and warm start alike. For the set this spec defines, the targets are the anchors below. Any live notification found outside this spec's set (and not deleted by CS-04 or CS-06) that has no defined target: stop, list it for Darek, and confirm its target instead of inventing one. The full anchor list this batch needs:  
  1. Workspace → Next session agenda module  
  2. Settings → the therapy date setup (the place where a session date is set)  
  3. The After Therapy note input  
  4. The Prepare for Therapy data input flow (the Supporting questions step)  
  5. The Between Sessions note input, opened as a new note  
  6. Record a session, ready to record  
  7. Workspace → To-do section (scrolled to the section ID)  
  8. Main → Mood trends section (scrolled to the section ID)  
  9. A new Reflect conversation  
  10. Main → Therapy goals section (scrolled to the section ID)  
  11. Therapy Relationship → the new check-in data input card  
  12. The newest Weekly summary card on the Timeline  
  13. The newest Monthly summary card on the Timeline  
  14. Goals setup (for the CS-07 account nudge)  
- **Do NOT touch:** The screens behind the anchors; the OS-level push plumbing beyond the tap routing.  
- **Done when:** The audit lists every live notification with its verified landing; every anchor above passes a tap test from a cold start and from background on both platforms; no notification in the app remains whose tap opens a generic or dead landing; any unlisted survivor got its target confirmed by Darek, not guessed.