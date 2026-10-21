# PHASE E — Frontend: Workspace modules (MSV3.2 Fix.1) — run in repo `mindsync-frontend/`

## SYSTEM INSTRUCTIONS (read fully before any tool call)

You are a fresh Claude Code session acting as the team lead for the WORKSPACE-MODULES slice of the
MSV3.2 Fix.1 batch. Project rules from `CLAUDE.md`. Delegate to `flutter-mobile` (+ `qa-testing`).

- Repo: `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend` — branch **dev**. App code in `mindsync_app/`.
- **Commit locally, stage only files you touched, NEVER push.** No other FE session at the same time.
- REQUIRES: Phase D finished — REUSE its shared P1 (add-sheet), P2 (archive), P3 (expand/collapse)
  widgets (paths in STATUS.md Phase D report). Do NOT build parallel implementations.
- Wire API calls per `API_CONTRACT_Fix1.md` (§1 lifecycle, §3 agenda/pins/threads, §7 goals, §8 relationship).
  Mismatch → stop that piece, log in STATUS.md.
- l10n PL + ENG; gen-l10n + build_runner; commit generated code. Baselines: 30 FE failures; analyze clean.
- Red „Usuń" = confirm dialog → permanent delete, never archives.

## Module: Wątki (1.2 CS-14..CS-18)

### CS-14 · FIX · „Dodaj do agendy" on the thread card
Currently dead. One tap → thread appears as a topic at the TOP of Agenda (tag „Wątek"); button switches
to an added state; tap again → removes from Agenda (toggle). Agenda reflects both instantly.

### CS-15 · CHANGE · Thread card cleanup + statuses
Thread card (hub-and-spoke) anatomy: short AI context description (where the thread came from, what
happened recently — BE provides; on failure show sources without description); sources list (the Timeline
cards it originates from — display-only this batch); actions: „Dodaj do agendy" (CS-14) + mark closed.
**REMOVE the archive button on the expanded thread** — only closed + add-to-agenda remain.
Navigation: close card via swipe-left OR chevron-left → previous view.
Mark closed → thread leaves active list → archive „Domknięte wątki" / "Closed threads" via a P2 archive
icon in the Wątki header; restorable.
Status chain: otwarty → after a session where the thread was on the agenda and got checked off as
discussed, status flips to „poruszony" automatically → from the card the user picks: domknij (→ archive)
or back to otwarty. No forced prompt.
Full-list nudge: when ≥5 threads are active and triage sends a new one → gentle message: PL „Masz już
sporo otwartych wątków — warto najpierw coś domknąć." / ENG "You already have quite a few open threads —
worth closing something first." The new thread is STILL added (5 = display default, not a cap).

### CS-16 · CHANGE · Expand/collapse — P3 at the bottom of the module box; chronological, oldest lowest.

### CS-17 · FIX · „1 z 5 aktywnych" counter
Hidden while active count ≤5. When >5: „5 z [total] aktywnych" (ENG "5 of 12 active"), static (does not
change as the user expands the list).

### CS-18 · CHANGE · Add UI
Remove the TOP plus icon. Add ghost button „+ Dodaj wątek" / "+ Add thread" per P1 (sheet title „Dodaj
wątek"); new thread lands at top. Must look and behave exactly like the Agenda and Do zrobienia adds.

## Module: Realizations (1.2 CS-19 + 1.1 FIX.05)
„Pin to Agenda" on a realization card: currently dead, and a pinned realization cannot be unpinned.
Tap → realization at TOP of Agenda (tag „Realizacja"); button switches to pinned state; tap again →
unpins + removes from Agenda (realization stays in §4). Deleting the agenda item also clears the pin
state (no orphans, no stuck pins). Do NOT touch the three-point list with expandable full list.

## Module: Goals (1.2 CS-20..CS-22)

### CS-20 · Narrative ad-hoc refresh
↻ refresh icon in the Goals header, LEFT of the archive icon. Tap → narrative regenerates via the contract
§7 endpoint; loading state on the text area meanwhile; failure → keep previous text + error toast with
retry. Do NOT touch scheduled/automatic generation.

### CS-21 · Archive of completed goals
P2 archive, title „Zakończone cele" / "Completed goals": marking a goal done moves it there with its
completion date; badge + restore per P2.

### CS-22 · Add UI (fixes the doubled „+")
Remove the current „+ + dodaj cel" control entirely. Bottom of the Goals frame: ghost button „+ Dodaj
cel" / "+ Add goal" per P1 (sheet title „Dodaj cel"); saved goal lands at top. Exactly one „+" ever
visible; full P1 round-trip incl. Nagraj/STT.

## Module: Therapy Relationship (1.2 CS-23..CS-25)

### CS-23 · FIX · Content cut off at the bottom
Whole module box must display in full — safe-area padding / layout fix. Verify against Android gesture-nav
overlap and the iOS home indicator, small and large screens.

### CS-24 · FIX · Rating icon colors
Scoring + color systems already exist — only bind and surface stored values (contract §8): each check-in
entry's icon shows its stored color (red/yellow/green); the module icon on the Workspace overview shows
the color of the MOST RECENT check-in. Remove the hardcoded orange. Do NOT touch scoring/mapping logic.

### CS-25 · CHANGE · Check-in list expand + contrast
Replace the one-off link „zobacz wszystkie 5 check-iny" with P3 (default 5, batches of 10, „Wszystkie
widoczne", „Zwiń wszystko ∧"), visually coherent with Wątki. Control text darker — WCAG AA contrast
(≥4.5:1) against the blue background (verify the ratio numerically).

## Definition of done (Phase E)
- All items per their "Done when" clauses in the spec texts above; pin/toggle round-trips covered by
  cubit tests; contrast ratio for CS-25 documented in the PR/commit message.
- `flutter analyze` no new errors; `flutter test` no new failures vs baseline (30).
- Commits local on dev (generated code committed). STATUS.md report appended (note anything Phase F
  needs: thread chip-state hooks, module list cubits to refresh after chip taps).

## Code anchors (planner-provided; verify before use)
All paths under `mindsync_app/`.

**Wątki** — `workspace/threads/threads_module_section.dart`, `threads/widgets/thread_card.dart`,
`threads/thread_detail_screen.dart`, `threads_full_screen.dart`; cubits `threads/cubit/threads_cubit.dart`
+ `thread_detail_cubit.dart`; model `lib/api/models/workspace/thread_model.dart` (context_snippet already
surfaced — FE commit b368387). BE (`workspace.py`): add-to-agenda L566, close L606, status L631,
archive L691, restore L705; `ThreadStatus` open/**touched**(=poruszony)/closed/archived/queued with
MAX_ACTIVE=5 (`app/models/workspace.py` L135) — the nudge threshold and the „5 z N" counter derive from
active counts (contract §3).

**Realizations** — `workspace/realizations/realizations_module_section.dart`,
`realizations/cubit/realizations_repo_cubit.dart`; model `realization_repo_item_model.dart`. BE:
realizations GET L724 + **`/toggles` L736** — pin/unpin plumbing exists server-side; the FE button is
what's dead. Agenda-side delete must clear pin state (contract §3; Phase A guarantees no orphans).

**Goals** — `workspace/goals/goals_module_section.dart`, `goals/workspace_goal_card.dart`,
`goals/goal_detail_screen.dart`; cubits `goals/cubit/goal_narrative_archive_cubit.dart` (narrative archive
already has a cubit!) + `lib/screens/stats_tab/cubit/goal_tracking_cubit.dart`. BE: POST
`/goals/{id}/refresh` L451 EXISTS, narratives archive GET L486 (contract §7). The doubled „+ + dodaj cel"
control lives in the goals module section/card — grep for the add-goal control.

**Therapy Relationship** — module = `HealthCheckSection` reused from stats (see
`workspace_screen.dart` L114–142 imports); BE `TherapyHealthCheck` `models.py:1350` with
**`relationship_state` "green"/"amber"/"red"/"safety_escalation"** — spec's "yellow" = `amber`; ask
contract §8 for the exposed field; decide + document how `safety_escalation` colors (treat as red unless
the contract says otherwise). Endpoint `app/api/v1/endpoints/health_check.py`.

**Shared widgets** — P1/P2/P3 paths are listed in STATUS.md by Phase D. Do not fork them.
