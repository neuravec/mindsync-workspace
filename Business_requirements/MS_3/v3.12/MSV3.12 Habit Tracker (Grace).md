# MindSync Change Spec \- MSV3.12 "Habit Tracker"

For Claude Code · 31.08.2026 · author: Darek

## Context (max 10 lines)

* Sync: backend MindSync (main) and frontend mindsync-frontend (dev) both pulled clean 31.08, fully in sync with origin.  
* History read: newest Drive spec "MSV3.10 \- User Feedback Fix" (13.08); MSV3.11 spec authored 31.08 (local file \+ artifact, not on Drive) \- NOT yet executed, zero commits since.  
* Hard dependency: MSV3.11 CS-08 (Homework delete) must land BEFORE this round \- Habits takes the freed 'homework\_today' slot in the Main module registry. Darek 31.08: "Yes, that's this feature we've mentioned."  
* Frontend app code in mindsync-frontend/mindsync\_app/; backend paths relative to MindSync/.  
* Darek's decisions 31.08: placement \= Homework's slot on Main · "+10 XP" is REAL XP into the existing gamification system (UserLeveling) · habits and their history FEED the AI context · free account \= 1 habit, premium \= unlimited · habit week follows the user's week-start preference · free slot is refillable after delete · monthly view read-only · retro-completed weeks pay their XP.  
* Existing gamification facts: UserLeveling relationship at app/models/models.py:154, endpoints in app/api/v1/endpoints/gamification.py (journey\_summary with longestStreakDays), Character tab PetHeroCard shows XP (orca).

## Previous round \- verification

| ID | Item (short) | Evidence | Status |
| :---- | :---- | :---- | :---- |
| MSV3.11 CS-01..CS-11 (31.08) | Threads, Reflect, Repeat, Mood, Schedule round | spec delivered 31.08; no commits in either repo since | PENDING \- not started (expected; execute MSV3.11 first, at minimum CS-08) |
| CS-01 (MSV3.10) | Microphone conflict investigation | none | NOT FOUND \- parked (carried) |
| CS-02 (MSV3.10) | False "unset time" push | backend de8d538 partial | PARTIAL \- folded into MSV3.11 CS-10 (carried) |
| CS-03 (MSV3.10) | Workspace Documents section | none | NOT FOUND \- parked (carried) |

## Summary

* Total items: 4 (DELETE: 0 · FIX: 0 · CHANGE: 4 · VERIFY: 0\)  
* Areas touched: Main (new Habits section), Backend (new habit model \+ API \+ AI context feed), Gamification (XP award)  
* One-paragraph intent: a new Habit Tracker section on the Main screen tracking good habits ("Drink water") and bad habits ("Don't smoke") in one list \- weekly view with one-tap today check-off, an Edit mode for history/reorder/add, a monthly heat-grid view, per-habit flame streaks, and a real \+10 XP reward for full weeks. This is the feature the Homework slot was freed for in MSV3.11 CS-08.

## Global guardrails (read before touching anything)

* Order of rounds: do not start this spec until MSV3.11 CS-08 has landed. Habits goes into the registry position freed by 'homework\_today' in lib/screens/main\_tab/main\_tab\_screen.dart (\~line 442). Never build Habits alongside a still-live Homework card.  
* Do NOT confuse Habits with Workspace To-do and its Repeat tasks (MSV3.11 CS-05..07). Separate feature, separate data, separate UI. A daily habit is not a daily to-do; nothing in todo\_\* files is shared or touched.  
* Do NOT confuse per-habit streaks with the existing journey streak in gamification.py (journey\_summary / longestStreakDays). Habit streaks are new, per-habit, and computed from habit checks only. Existing streak logic stays untouched.  
* Checking a day always means success. For a bad habit it means "I stayed clean today". Missed days stay empty \- never red, no failure states, no guilt UI anywhere in this feature.  
* No habit notifications or reminders this round. MSV3.11's guardrail stands: no new notification types.  
* Colors named by Darek (teal check, amber shield, warm sand, mint highlight, teal ring, grey locked) are design language, not new hex values: map them to the existing MsColors token set. If a needed token has no close match, flag it to Darek instead of inventing a parallel palette.  
* Other Main modules and their order stay untouched (next\_session above, mood\_trend below the Habits slot).  
* New UI strings quoted here are working names (EN): produce PL \+ EN and follow the ARB convention (literal English into all 7 locales, one canonical key per string).  
* After each item: flutter analyze clean, run the app, no dead references / broken navigation.

---

## CS-01 · CHANGE · \[Backend\] Habit model, API, XP award, AI context feed

* Type: CHANGE (new backend capability; no existing behavior altered)  
* Location: New model file in app/models/ (two tables: habits \+ habit day-checks), new endpoints file in app/api/v1/endpoints/ (suggest habits.py), CRUD in app/crud/, Alembic migration (follow the repo's SQLite-vs-Postgres dialect-branch precedent, e.g. kk2l3m4n5o6p\_add\_weekly\_summary\_uniqueness.py). XP: existing UserLeveling (app/models/models.py:154) \+ app/api/v1/endpoints/gamification.py. AI context: the same user-context path that MSV3.11 CS-07 uses for to-do completion history (conversation analysis / context builders).  
* Action: Build the backend for the feature as one coherent API:  
  1. Habit: id, user, name, type good | bad, user-defined sort order, created/archived timestamps. Day check: one row per habit per calendar day, presence \= success. Backdated writes allowed (Edit mode corrects history); future dates rejected server-side.  
  2. Endpoints: list habits with their checks for a requested week/month window; create / rename / change type / reorder / delete a habit; toggle a day check (today by default, past dates only from Edit mode). Deleting a habit removes its checks.  
  3. Derived data returned by the API, not computed client-side: per-habit current streak (consecutive checked days ending today or yesterday \- an unchecked today does not break the streak until the day ends); per-month summary in the form checked / days-elapsed-so-far (Darek's example: "21/27 days"). Day boundary \= user's local midnight; reuse the tz-safety precedents from therapy\_schedule\_utils.py (naive-vs-aware guards).  
  4. Free-tier cap (Darek, 31.08): free account \= 1 active habit, premium \= unlimited. Enforce server-side on create (reuse the existing premium/subscription check used by other premium-gated endpoints); the cap is a count cap and the slot is refillable \- deleting the habit frees it for a new one (confirmed by Darek).  
  5. XP award (Darek, 31.08 \- real XP): when all 7 days of a habit week are checked for a habit, award \+10 XP to the user's existing UserLeveling via the gamification layer. Idempotent: once per habit per week, including weeks completed retroactively through Edit mode (confirmed by Darek: retro weeks pay XP). The API response for a toggle that completes a week says so, so the frontend can show the chip. The XP week \= the user's preference-aligned week (same 7 days the weekly view shows).  
  6. AI context feed (Darek, 31.08): habit list, types, check history, and streaks become part of the user's AI context the same way to-do completion history does (MSV3.11 CS-07) \- Reflect, session preparation, and reports can reference them.  
* Why: Foundation for CS-02..04; Darek's decisions make XP, limits, and AI integration real rather than cosmetic.  
* Do NOT touch: Existing gamification logic beyond calling the XP-award path; journey\_summary streaks; To-do models/endpoints; notification generators.  
* Done when: All endpoints work against a real device build; a habit checked 7/7 for a week yields exactly \+10 XP once (re-toggling or re-editing that week never double-awards); free user's second create returns the premium-required error; streak and month-summary values from the API match hand-computed fixtures across a month boundary and a device timezone change; deleted habit's data is gone and stops appearing in AI context; migration runs on Postgres and SQLite test env.  
* Risk: Medium \- new schema \+ XP idempotency \+ tz math, but no existing behavior modified.

## CS-02 · CHANGE · \[Main\] Habits section \- weekly view (default state)

* Type: CHANGE (new Main module)  
* Location: New module widget (suggest lib/screens/main\_tab/widgets/habits\_card.dart \+ its cubit), self-contained via GetIt like the other Main modules (homework\_today\_card.dart's doc comment describes the self-containment pattern to mirror). Registered in the Main module registry at the position freed by 'homework\_today' (main\_tab\_screen.dart, \~line 442).  
* Action: The default state of the Habits card, element by element:  
  1. Card header: section title, an Edit button (top, switches to CS-03's edit mode), and the Weekly/Monthly toggle (CS-04).  
  2. One list, both habit kinds mixed, in the user's saved order. Each row: a small teal check cue for a good habit or amber shield cue for a bad habit next to the name, the habit name, a flame streak counter, and seven day cells for the current week.  
  3. Day cells: teal fill for good-habit wins, warm sand fill for bad-habit wins, a teal ring marking today, grey locked cells for future days. Missed past days stay empty \- never red.  
  4. Out of edit mode only today's cell is tappable: one tap toggles it with a small fill-and-bounce animation. Past and future cells do nothing outside Edit mode.  
  5. When a toggle completes a full 7/7 week (per the CS-01 response flag): a quiet mint highlight on the row plus a "+10 XP" chip.  
  6. Empty state (no habits yet): a gentle card \- "Small daily wins add up" \- with a single button that opens the add-habit sheet (CS-03's sheet).  
  7. Week columns: honor the existing week-start preference (week\_start\_selector.dart) with Monday as the default \- confirmed by Darek, 31.08: "feature adapts to user preference".  
* Why: Darek's feature notes; the simple always-visible weekly loop is the core of the tracker.  
* Do NOT touch: Other Main modules and their order; mood\_trend and next\_session neighbors; Workspace.  
* Done when: The card renders in Homework's old slot with real data from CS-01; a good and a bad habit render with their distinct cues and fills; only today's cell responds outside Edit mode and toggles with the animation; completing a week shows the mint highlight \+ "+10 XP" chip and the XP lands on the Character tab; the empty state shows for a fresh user and its button opens the add sheet; week starts follow the preference. flutter analyze clean, module tests green.  
* Risk: Medium \- new module UI with animation states; layout must hold on small screens (7 cells \+ streak \+ name per row).

## CS-03 · CHANGE · \[Main, Habits\] Edit mode \+ habit editor sheet

* Type: CHANGE  
* Location: Same module as CS-02; editor as a bottom sheet (mirror the app's existing bottom-sheet patterns, e.g. voice\_or\_text\_capture\_sheet.dart for structure conventions only \- do not modify that file).  
* Action:  
  1. Tapping Edit switches the card into a clearly marked editing state: a dashed sand frame around the card.  
  2. In edit mode: past day cells become tappable to correct history (writes backdated checks via CS-01; future days stay locked); rows gain drag handles for reordering (persist the order); tapping a habit name opens the editor sheet; an "+ Add habit" row appears at the bottom of the list.  
  3. "+ Add habit" on a free account that already has 1 habit → the subscription screen opens instead of the sheet (same pattern as the Documents-section gate in MSV3.10 CS-03: gate at the entry point, no picker/sheet flash). Premium, or free with zero habits → the sheet opens.  
  4. Editor bottom sheet: a name field; a Good/Bad habit type picker with one-line explainers (working copy \- Good: "Something you want to do daily", Bad: "Something you want to stay free of"); Save; and a quiet Delete action when editing an existing habit. Delete removes the habit and its history (CS-01 behavior) \- confirm before deleting, consistent with the app's existing delete-confirm patterns.  
  5. Leaving edit mode returns to CS-02's default state; today-only tapping resumes.  
* Why: Darek's notes \- history correction, ordering, and habit management live behind an explicit Edit state so the default card stays one-tap simple.  
* Do NOT touch: voice\_or\_text\_capture\_sheet.dart and other modules' sheets (pattern reference only); the Workspace item menu; future-day locking (never editable, in any mode).  
* Done when: Edit shows the dashed sand frame; a past empty cell can be checked and a past checked cell unchecked, and the change persists after app restart; retro-completing a week awards \+10 XP exactly once; drag-reorder persists across restart; the name row opens the sheet pre-filled; type can be switched Good↔Bad and the row cues update; free user with 1 habit hits the subscription screen from "+ Add habit"; Delete asks for confirmation and removes the habit everywhere (list, month view, AI context).  
* Risk: Medium \- backdated-write edge cases (week completion, streak recompute) and drag-reorder state.

## CS-04 · CHANGE · \[Main, Habits\] Monthly view

* Type: CHANGE  
* Location: Same module; the Weekly/Monthly toggle in the card header (CS-02 item 1).  
* Action:  
  1. Toggling to Monthly swaps the card body: each habit shows a compact dot heat-grid of the whole month (one dot per day: filled teal / warm sand for wins by habit type, empty for misses, locked-grey for future days) with a "21/27 days"-style summary (checked / days elapsed so far this month, from CS-01) and the current streak.  
  2. Chevrons page between months (past months only; no paging into the future). Data loads per month via CS-01's month window.  
  3. Monthly view is read-only \- all editing (today toggle, history correction) happens in the weekly view / Edit mode (confirmed by Darek, 31.08).  
  4. The toggle state is remembered while the app is open; default on a fresh open is Weekly.  
* Why: Darek's notes \- the long-range consistency picture next to the weekly action loop.  
* Do NOT touch: The weekly view's behavior; streak/summary math (server-side per CS-01 \- the client renders, never recomputes).  
* Done when: The toggle swaps views without losing state; the current month's grid matches the weekly data exactly; the summary reads checked/elapsed (not checked/month-length); chevrons page back through months with correct data and cannot page past the current month; future days render locked; view is read-only. Tests cover a month boundary.  
* Risk: Low-Medium \- rendering-heavy but read-only; the data contract carries the logic.