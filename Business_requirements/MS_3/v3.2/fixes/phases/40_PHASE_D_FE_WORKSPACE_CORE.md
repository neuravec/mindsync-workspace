# PHASE D — Frontend: Workspace core (MSV3.2 Fix.1) — run in repo `mindsync-frontend/`

## SYSTEM INSTRUCTIONS (read fully before any tool call)

You are a fresh Claude Code session acting as the team lead for the WORKSPACE-CORE slice of the MSV3.2
Fix.1 batch. Project rules from `CLAUDE.md` (auto-loaded). Delegate to `flutter-mobile` (+ `qa-testing`);
optionally `ui-ux-designer` for the shared patterns spec review. Keep the agent count lean.

- Repo: `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend` — branch **dev**. App code in `mindsync_app/`.
- **Commit locally, stage only files you touched, NEVER push.** No other FE session at the same time.
- REQUIRES: Phase A finished (`API_CONTRACT_Fix1.md` has no TBDs) and Phases B–C committed. Read
  `STATUS.md` first. Wire API calls ONLY per the contract; mismatch → stop that piece, log in STATUS.md.
- l10n PL + ENG; gen-l10n + build_runner; commit generated code. Baselines: 30 FE test failures; analyze clean.
- Binding decisions (master plan): red „Usuń" never archives; 1.2 supersedes 1.1 (details below);
  P1/P2/P3 are single shared widgets reused everywhere.

## Part 1 — Shared pattern widgets (build FIRST, in `lib/ui/widgets/`)

### P1 · Add-entry bottom sheet (used by CS-05, CS-09, CS-13, and Phase E: CS-18, CS-22)
Trigger: one wide GHOST button at the bottom of a module frame („+ Dodaj …" — label per module).
Sheet (slides up): title (= button label without „+") + X top-right; text field; bottom row: left button
„Nagraj", right primary „Zapisz". X → close, nothing saved. „Nagraj" → recording UI; on stop the STT
result lands in the text field, editable (reuses the existing speech-to-text pipeline; on STT failure show
the existing recording-error handling — the Phase B error card — text field unchanged). „Zapisz" → save →
sheet closes → entry appears at TOP of the module's list. Must also support a PREFILLED edit mode
(„Edytuj nazwę" reuses the same sheet; Zapisz updates in place) and, for todos only, a repeat control
(see Do zrobienia below).

### P2 · Archive (used by CS-05, CS-07, CS-11, and Phase E: CS-15, CS-21)
Module header, top-right: small archive icon; badge = small green circle with count of items closed since
the archive was last opened (accumulates; resets to default after the user enters and exits the archive).
Opens hub-and-spoke (full view): title (per module) + X → back. List of closed items, newest first, each
with its close date and a „Przywróć" / "Restore" action → item returns to TOP of the module's active list.
Closing an item in the module (checkbox) → leaves list → appears in archive with today's date → badge +1.

### P3 · Expand/collapse list (used by CS-05, and Phase E: CS-16, CS-25; also Do zrobienia list rule)
Default visible: 5, chronological, newest at top. Bottom controls: „Pokaż więcej ⌄"/"Show more ∨" → +10
per tap until exhausted; „Pokaż mniej ∧"/"Show less ∧" → −10 (visible only when expanded); „Zwiń
wszystko ∧"/"Collapse all ∧" → back to 5. Fully expanded → last row shows „Wszystkie widoczne"/"All
visible" with „Zwiń wszystko ∧" below.

## Part 2 — Rename (1.1 CS-20 = 1.2 CS-02)
Bottom-nav tab PL „Terapia"/ENG „Therapy" → PL **„Pracownia"** / ENG **„Workspace"** — tab label, section
screen header, every user-facing string naming this section. Grep l10n; rename ONLY section-name strings;
never copy where terapia/therapy means the therapy concept (e.g. „Therapy Relationship").
Done when: both languages correct; navigation works; grep shows no leftover section-name references.

## Part 3 — Item lifecycle everywhere (1.2 CS-04)
Every list item in: Tematy i pytania, Do zrobienia, Wątki (Phase E), Agenda, Goals (Phase E) has exactly
two states: open / closed. Closing → module's own archive (P2) with close date; restore per P2 and also
from the source output card (Phase F wires the card side). Red „Usuń" is permanent, never archives.
Wire per contract §1.

## Part 4 — Module: Agenda następnej sesji (1.2 CS-06..CS-09; 1.1 FIX.02 superseded by CS-07)
- **CS-06 sourcing**: items arrive ONLY via user taps from: Tematy i pytania „Dodaj do agendy", Wątki
  „Dodaj do agendy" (Phase E), Realizations pin (Phase E), manual add (CS-09). NOT from To-Do. Every row
  shows a source tag: PL „Po terapii"/„Prep"/„Nagranie"/„Między sesjami"/„Dodane ręcznie"/„Wątek"/
  „Realizacja" (ENG "After therapy"/"Prep"/"Recording"/"Between sessions"/"Added manually"/"Thread"/
  "Realization") — carried from the origin card through the module. Do NOT touch the existing checkbox
  close behavior.
- **CS-07 archive**: P2 archive „Twoje zakończone tematy" / "Your closed topics"; the existing checkbox
  close moves the topic there. (This supersedes 1.1 FIX.02's inline DONE section — if the Agenda renders
  on more than one surface, the archive is reachable from each, same data.)
- **CS-08 row menu**: X icon per row → 3-dot vertical menu with exactly „Edytuj nazwę" (P1 sheet prefilled,
  Zapisz updates in place, position unchanged) and red „Usuń" (confirm → permanent). No „odklik" entry.
- **CS-09 add UI**: wide ghost button „+ Dodaj temat" / "+ Add topic" per P1 (sheet title „Dodaj temat");
  saved topic lands at top, tag „Dodane ręcznie". Full P1 round-trip incl. Nagraj/STT.

## Part 5 — NEW module: Tematy i pytania (1.2 CS-05)
Placed directly BELOW „Agenda następnej sesji". Collects all tematy & pytania (chips — wired in Phase F —
or manual adds).
Anatomy: header „Tematy i pytania" / "Topics & questions" + archive icon (P2, title „Zamknięte tematy i
pytania" / "Closed topics & questions"); list default top-5 chronological (P3); each row: checkbox ·
entry text · source tag · 3-dot menu („Edytuj nazwę" — P1 prefilled; „Dodaj do agendy"; red „Usuń");
bottom: ghost button „+ Dodaj temat lub pytanie" / "+ Add topic or question" (P1; manual entries tagged
„Dodane ręcznie"). „Dodaj do agendy" → entry appears at TOP of Agenda with its source tag carried over;
the entry STAYS open here until the user closes it.
Done when: all anatomy blocks render; checkbox→archive→restore round-trips; agenda hand-off works;
P1/P2/P3 behave exactly as specced.

## Part 6 — Module: Do zrobienia (1.1 FIX.01 reconciled with 1.2 CS-11..CS-13)
Binding reconciliation (master plan decision 1): Done = **P2 archive „Zrobione"/"Done"** whose icon
REPLACES the current task-count indicator (1.2 CS-11) — NOT an inline „Pokaż zakończone" section. Row
affordance = **3-dot menu** with exactly „Edytuj nazwę" + red „Usuń" (1.2 CS-12) — NOT a pencil icon;
„odklik"/„Odkliknij" removed entirely (grep clean). Surviving 1.1 FIX.01 requirements:
- Checkbox replaces bullet point; a task closes ONLY via checkbox (row tap elsewhere does NOT close);
  each completion is a separate Done entry with date; restore („Przywróć" / un-tick in archive) reopens.
- List: max 5 visible + P3 controls (6+ tasks → expander).
- **Repeats**: the edit sheet (P1 prefilled) additionally manages repetition — label PL „Powtarzaj" /
  ENG "Repeats" + repeat icon; options PL „Codziennie"/„Tygodniowo"/„Miesięcznie" (ENG daily/weekly/
  monthly). Repeating task reappears unchecked at its next period; missed period stays open, no stacking
  (BE per contract §4).
- **CS-13 add UI**: ghost button „+ Dodaj zadanie" / "+ Add task" per P1 (sheet title „Dodaj zadanie");
  new task lands at top. No due-date UI anywhere in the module (author decision).
- Same data source as Main Homework (Phase C module) — verify Main still shows the 3 oldest open FIFO
  after your changes.
Done when: checkboxes everywhere; only checkbox closes; menu exactly two entries; counter icon replaced
by archive icon + badge; „Zrobione" archive with dates + restore; repeats save and reappear per period;
P1 round-trip incl. Nagraj; ≤5 rows + expander.

## Definition of done (Phase D)
- Parts 1–6 per their "Done when"; widget tests for P1/P2/P3; cubit tests for lifecycle + repeats display;
  `flutter analyze` clean of new errors; `flutter test` no new failures vs baseline (30).
- Commits local on dev (generated code committed). STATUS.md report appended — explicitly list the shared
  widget file paths (Phase E reuses them) and any contract mismatches.

## Code anchors (planner-provided; verify before use)
All paths under `mindsync_app/`.

**Workspace screen** — `lib/screens/workspace/workspace_screen.dart` (`WorkspaceScreen` L29,
`kWorkspaceTabIndex = 3` L58; fixed module order L114–142: Agenda→Todo→Threads→Realizations→Goals→
TherapyRelationship). Module frame: `lib/screens/workspace/widgets/workspace_module_section.dart`;
empty state `workspace_empty_state.dart`; dismissed rows `workspace_dismissed_row.dart`. Insert the new
„Tematy i pytania" module section directly below the Agenda section here.

**P1 basis** — `lib/screens/workspace/widgets/voice_or_text_capture_sheet.dart` already does voice+text
capture (uses VoiceErrorCard from Phase B): generalize/extend into the shared P1 sheet (title+X, text
field, Nagraj, Zapisz, prefilled edit mode, optional repeat control) rather than building from scratch.
**P3 basis** — `lib/widgets/collapsible_card_section.dart`. **P2/archive basis** — per-module
`*_full_screen.dart` views (`todo_full_screen.dart`, `threads_full_screen.dart`) already carry
archive/restore lists; unify into the shared P2 (badge icon + hub-and-spoke + Przywróć).

**Agenda** — `workspace/agenda/agenda_module_section.dart`, `agenda/widgets/agenda_item_tile.dart`,
`agenda/cubit/agenda_cubit.dart`; model `lib/api/models/workspace/agenda_item_model.dart`. BE: archive
L390 / restore L404 in `workspace.py`; `agenda.kind` + `source_type/source_id` exist (tags per contract §3).

**Do zrobienia** — `workspace/todo/todo_module_section.dart`, `todo/widgets/todo_item_tile.dart`,
`todo_full_screen.dart`, `todo/cubit/todo_cubit.dart`; model `todo_item_model.dart`. BE: done L461 /
undone L480 / archive L493 / restore L507 / today L445. **Recurrence is NEW** (Phase A adds fields —
contract §4); the current header task-count indicator is what CS-11 replaces with the archive icon.
Keep `/todos/today` semantics intact for Main Homework (Phase C shipped against it).

**Tematy i pytania** — new: module section + tiles + cubit under `workspace/topics/…` (follow the
existing module folder pattern), Freezed model per contract §2/§3, calls via
`lib/api/api_managers/workspace_manager.dart` (endpoints in `lib/api/dio_settings.dart/endpoints.dart`).

**Rename** — `lib/screens/main_page/main_page_body.dart` `_BottomNav` L528, items L545–573. Keys:
`nav_workspace` (EN "Therapy" `app_en.arb:2134`, PL "Terapia" `app_pl.arb:1859`) and `workspace_title`
(EN `app_en.arb:2135`) → „Workspace"/„Pracownia". **CAUTION: `nav_therapy` = "Timeline"/"Oś czasu"
(EN L695 / PL L674) is the TIMELINE tab — do not touch it.** Grep all locales for other section-name uses.

**API layer** — `lib/api/api_managers/workspace_manager.dart`; Freezed models in
`lib/api/models/workspace/` (`agenda_item_model`, `todo_item_model`, `workspace_overview_response`, …);
overview cubit `workspace/cubit/workspace_overview_cubit.dart` (badge counts likely flow through it).
