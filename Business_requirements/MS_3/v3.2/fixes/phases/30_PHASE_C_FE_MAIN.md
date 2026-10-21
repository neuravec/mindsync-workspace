# PHASE C — Frontend: Main screen (MSV3.2 Fix.1) — run in repo `mindsync-frontend/`

## SYSTEM INSTRUCTIONS (read fully before any tool call)

You are a fresh Claude Code session acting as the team lead for the MAIN-SCREEN slice of the MSV3.2
Fix.1 batch. Project rules come from `CLAUDE.md` (auto-loaded). Delegate implementation to
`flutter-mobile` (+ `qa-testing` at the end); keep the agent count lean.

- Repo: `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend` — branch **dev**. App code in `mindsync_app/`.
- **Commit locally, stage only files you touched, NEVER push.**
- Runs AFTER Phase B is committed. May overlap the backend Phase A — read `STATUS.md` and
  `API_CONTRACT_Fix1.md` first; if a BE piece you need isn't ready, build the FE against the contract and
  record the gap in STATUS.md (do NOT invent endpoints not in the contract).
- No other FE session may run at the same time.
- l10n PL + ENG for every string; gen-l10n + build_runner; commit generated code.
- Test baseline: 30 FE failures pre-exist; `flutter analyze` no new errors.
- iOS parity is the POINT of several items here (previous batch failed on iOS) — implementation must be
  platform-agnostic single-codebase; flag any platform-conditional code you find as a smell.

## Spec items (implement exactly)

### CS-08 · CHANGE · Main feature order (re-implement — iOS failed)
Final Main order, top to bottom:
1. Next therapy session (CS-09)
2. Zadania domowe / Homework (CS-10)
3. Mood Trend (CS-11) — with AI Summary inside its box (FIX.03)
4. Therapy relationship prompt (conditional — visible only until the weekly check-in is done)
5. Weekly Observations
6. [Afirmacja] — unchanged content/behavior, only position
**Realizations and Goal leave Main** (their Workspace homes are live; removal loses nothing).
Done when: Main renders exactly these modules in this order on BOTH platforms; Realizations and Goal no
longer on Main; AI Summary appears only inside Mood Trend.

### CS-09 · CHANGE · „Next therapy session" — formats + state-dependent buttons
Keep the countdown + existing action-reminder elements; change format and add state-dependent buttons.
Formats: >24h → day + time („jutro o 12:45", „czwartek o 10:00"), no minute countdown; sessions beyond
the weekday horizon → keep current display as-is. <24h → „dzisiaj o [godzina], za x godz y minut".
State chain: set session → prep CTA → session happens (begins AT the session's start time) → debrief CTA
→ between-sessions encouragement → next session (loops).
States & buttons:
- No therapy set → button opens a hub-and-spoke flow to set date, time, cadence and with whom — writes the
  SAME fields as settings' session data.
- No prep done before upcoming session → button → przygotowanie do terapii.
- Session already happened → button → debrief po terapii.
- After debrief → between-sessions encouragement → tap → between sessions feature.
- Cadence rollover: after debrief (or when between-sessions begins) the next session per cadence becomes
  the new countdown target.
Embedded bugs to fix: after completing the debrief the module did NOT switch to between-sessions, and the
next session stopped displaying even with weekly cadence set.
Do NOT touch: existing reminder elements; settings' session data model; current far-out-date display.
Done when: both formats render; each state shows its button; hub-and-spoke saves settings' fields;
debrief completion flips to between-sessions; weekly cadence auto-advances; transitions correct across
day boundary and at session start. Risk: state machine time edge cases — write cubit tests around them.

### CS-10 · CHANGE · „Zadania domowe / Homework" module (re-implement — iOS missing)
Today's view of the homework queue whose repository lives in Workspace §2 Do zrobienia. Max 3 items with
checkboxes: the 3 OLDEST open items (FIFO); rest wait in Workspace. Checkbox → done (appears as done in
Workspace archive) → next oldest surfaces. Repeating tasks re-enter per period (repeat mechanics = BE +
Phase D; here only display/consume). Single data source shared with Workspace §2 — no duplicate state.
Done when: ≤3 oldest open items with working checkboxes on BOTH platforms; checking surfaces next;
same data as Workspace §2.

### CS-11 · CHANGE · Mood Trend — restore score input, narrative display, update dates (FE part)
(a) Restore score input: user can again add and change symptom scores as the old Stats version allowed
(use the endpoint from `API_CONTRACT_Fix1.md` §5). (b) Narrative content is backend work (Phase A) — FE
just renders it. (c) Last-update date: small („malutka") relative date next to each symptom name — PL
„2 dni temu" / ENG „2 days ago".
Done when: scores addable/editable per symptom; relative dates render in PL/ENG.

### FIX.03 · CHANGE · AI Summary — merge into Mood Trend box (FE part)
Move AI Summary INSIDE the Mood Trend box, above the first symptom; ≤4–5 lines, NO bullets; it stops
being a standalone Main module. DELETE outright the „add an entry" / „it's been a while" box (stale
„Nie dodałeś od kilku dni notatki" defect) — grep clean, PL + ENG. Summary must render after new data
(generation fixed in Phase A).
Done when: summary inside Mood Trend above symptom 1; standalone module gone; empty-state boxes gone.

### FIX.04 · FIX · Weekly check-in doesn't dismiss after completion
After adding the therapy-relationship note the Main prompt must disappear until the next weekly cycle and
the relationship card must reflect the completed state (state exposure per contract §8; audit whether the
bug is FE state or BE — coordinate via STATUS.md).
Done when: adding the note removes the Main prompt until next cycle; card shows the completed entry.

### 1.2 CS-01 · FIX · Reminder card — dead „open" button
App-launch bottom-sheet „przypomnienie o missing therapy relationship check-in": tapping **open** must
navigate directly into a NEW Therapy Relationship check-in (quiz started) and dismiss the card.
Do NOT touch the trigger logic or other dismissal paths.
Done when: open navigates to the check-in and dismisses the card; scheduling unchanged.

## Definition of done (Phase C)
- All items per their "Done when"; cubit tests for the CS-09 state machine (incl. time edges) and CS-10;
  widget tests for the new module order.
- `flutter analyze` no new errors; `flutter test` no new failures vs baseline.
- Commits local on dev; STATUS.md report appended (note explicitly: which parts wait on Phase A backend,
  and that Phase D will restyle the Workspace „Do zrobienia" UI over the same repository).

## Code anchors (planner-provided; verify before use)
All paths under `mindsync_app/`.

**Main stack** — `lib/screens/main_tab/main_tab_screen.dart`: `MainTabScreen` L38; module stacker
`_NormalBody._buildCardMap` L321 with id→widget map: `next_session`→`_NextSessionCard` L1015 (live
countdown, 4 states incl. `_SessionHappenedCard`, `_BetweenSessionsEncouragementCard`,
`_EmptyNextSession`), `homework_today`→`HomeworkTodayCard` (**module exists — the iOS gap is likely
ordering/registration, audit why iOS differs**), `mood_trend`→`MoodTrendCard`,
`weekly_observations`→`WeeklyObservationsCard`, `health_check_banner`→`TherapyRelationshipPromptCard`,
`affirmation`→`DailyAffirmationCard`. **User reorder/hide edit mode exists via `MainTabCubit` (L570)** —
reconcile CS-08's fixed order with edit mode (spec order = default; investigate whether edit-mode saved
layouts are why iOS "failed" previously) and report the chosen semantics in STATUS.md.
Module widgets `lib/screens/main_tab/widgets/`: `homework_today_card.dart`, `mood_trend_card.dart`,
`weekly_observations_card.dart`, `therapy_relationship_prompt_card.dart`, `daily_affirmation_card.dart`,
`session_setup_screen.dart` (likely the set-therapy hub-and-spoke), `health_check_banner_widget.dart`,
plus **`last_realization_widget.dart` and `treatment_goal_anchor_widget.dart` — these must LEAVE Main**.
Cubits `lib/screens/main_tab/cubit/`: `main_tab_cubit.dart`, `homework_today_cubit.dart`,
`mood_trend_cubit.dart`, `weekly_observations_cubit.dart`.

**CS-10 data** — BE endpoint `/workspace/todos/today` already exists (workspace.py L445); shared models
`lib/api/models/workspace/todo_item_model.dart`, manager `lib/api/api_managers/workspace_manager.dart`.

**CS-11/FIX.03** — `mood_trend_card.dart` + `mood_trend_cubit.dart`; symptom AI summary currently
surfaces via `lib/screens/stats_tab/cubit/symptom_tracking_cubit.dart` (Stats screen shell was deleted in
MSV3.2 — the cubit survives); score input previously lived in the Stats symptom UI. BE: symptoms endpoints
per contract §5 (`/symptoms/{id}/score` exists — see Phase A anchors); AI summary = `MoodTrendSummary`
via `app/tasks/mood_trend.py` (BE side fixed in Phase A).

**FIX.04 / 1.2 CS-01** — `therapy_relationship_prompt_card.dart` + `health_check_banner_widget.dart`;
BE `TherapyHealthCheck` + `HealthCheckDismissal` (contract §8). The launch reminder bottom-sheet: find its
presenter (grep for the health-check reminder sheet around app launch / `main_page`); dead „open" button
must navigate into a NEW check-in and dismiss.

**CS-09** — countdown source: `UserPreferences.therapy_schedule` JSON + `next_session_date` (contract §10);
prep/debrief markers via `SessionPrepCard`/`SessionDebrief` endpoints (`prep_cards.py`, `debriefs.py`,
`between_sessions.py`). FE session-setup: `session_setup_screen.dart`. Write cubit tests around the state
machine (day boundary, session-start instant, debrief→between-sessions, cadence rollover).
