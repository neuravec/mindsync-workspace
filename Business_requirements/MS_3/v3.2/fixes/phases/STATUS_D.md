# MSV3.2 Fix.1 — PHASE D (FE Workspace core) — STATUS

## PHASE D — Frontend: Workspace core — DONE — 2026-07-17

- **Session commit** (repo `mindsync-frontend`, branch `dev`, **committed locally, NOT pushed**):
  - `861a805` — "MSV3.2Fix.1 D: Workspace core (shared P1/P2/P3, rename, Agenda CS-06..09, Tematy i pytania CS-05, Do zrobienia FIX.01/CS-11..13)" — 58 files, +5092 / −646. Single commit (all items share the ARB + generated l10n/freezed files, so splitting would fragment those). Runs on top of Phase C `914ddc3` + Phase B `716f33b`; dev now ahead of origin by 3, NOT pushed.

- **Items completed (spec IDs):** Part 1 (P1/P2/P3 shared widgets), Part 2 (rename 1.1 CS-20 = 1.2 CS-02), Part 3 (item lifecycle wiring §1), Part 4 (Agenda CS-06/07/08/09), Part 5 (Tematy i pytania CS-05), Part 6 (Do zrobienia FIX.01 + CS-11/12/13). All per their "Done when".

---

### Shared widget paths (Phase E CONSUMES these — do not move/rename)
- **P1 add/edit sheet:** `lib/screens/workspace/widgets/voice_or_text_capture_sheet.dart` — extended the pre-existing Phase-B sheet with `initialText` (prefilled edit mode) and a todos-only repeat control (`showRepeatControl` + `initialRepeatFreq` + `onSaveWithRepeat(text, repeatFreq)`). Non-repeat callers keep the `onSave(text)` signature. Reuse for CS-18 (Wątki add), CS-22 (Goals add).
- **P2 archive:** `lib/screens/workspace/widgets/workspace_archive_view.dart` — exports `WorkspaceArchiveIconButton(badgeCount, onTap)`, `WorkspaceArchiveView(title, entries, onRestore)`, and the `WorkspaceArchiveEntryData(id, text, closedAt, metaLabel)` row DTO. Badge marker store: `lib/utils/workspace_archive_badge_store.dart` (`WorkspaceArchiveBadgeStore` lazySingleton + `WorkspaceArchiveModuleKey` constants incl. `threads`/`goals` for Phase E). Reuse for CS-15 (Domknięte wątki), CS-21 (Zakończone cele).
- **P3 expand/collapse:** `lib/screens/workspace/widgets/workspace_expandable_list.dart` — `WorkspaceExpandableList(children, initialVisible: 5, step: 10)`. Reuse for CS-16 (threads), CS-25 (therapy relationship).
- **Shared 3-dot menu + delete confirm:** `lib/screens/workspace/widgets/workspace_item_menu.dart` — `WorkspaceItemMenu(onEditName, onDelete, onAddToAgenda?)` + `showWorkspaceDeleteConfirm(context) -> Future<bool>` (red "Usuń" always → confirm → PERMANENT delete, never archives). Reuse everywhere a row needs Edytuj nazwę/Usuń.

### New module (Tematy i pytania, CS-05)
- Model: `lib/api/models/workspace/topic_question_item_model.dart` (Freezed + json_serializable).
- Cubit: `lib/screens/workspace/topics/cubit/topics_cubit.dart` (+ `topics_cubit_state.dart`).
- UI: `lib/screens/workspace/topics/topics_module_section.dart` + `topics/widgets/topic_item_tile.dart`.
- Inserted directly below Agenda in `lib/screens/workspace/workspace_screen.dart`; registered `TopicsCubit` + `WorkspaceArchiveBadgeStore` in `lib/core/service_locator.dart`; provided + refreshed on tab enter.

### Files changed (touched — staged individually, no `git add .`)
- API: `lib/api/api_managers/workspace_manager.dart` (agenda edit/delete; todo edit/delete/completions-not-yet-consumed; full topic-questions CRUD + add-to-agenda), `lib/api/dio_settings.dart/endpoints.dart` (new paths), `lib/api/models/workspace/todo_item_model.dart` (`repeatFreq`).
- Cubits/state: agenda + todo cubit & state (archive list + badgeCount + editItem/deleteItem/restoreFromArchive/markArchiveSeen; agenda `touch` now moves to the archive; todo `markDone` now moves to the archive).
- UI: `agenda_module_section.dart`, `agenda_full_screen.dart`, `agenda/widgets/agenda_item_tile.dart`, `todo_module_section.dart`, `todo_full_screen.dart`, `todo/widgets/todo_item_tile.dart`, `workspace_screen.dart`.
- Infra: `lib/utils/workspace_archive_badge_store.dart` (new), `lib/services/preference_keys.dart` (`workspaceArchiveSeenJson`), `lib/resources/ms_colors.dart` (`workspaceBadgeGreen`).
- l10n: 35 new keys × 7 locales (PL + EN verbatim from spec; de/es/fr/nb/sv fully translated) + rename `nav_workspace`/`workspace_title`. `flutter gen-l10n` + `build_runner` run; generated code committed.

---

### Part 2 — Rename (1.1 CS-20 = 1.2 CS-02)
- `nav_workspace` + `workspace_title`: PL **Pracownia** / EN **Workspace** (de Arbeitsbereich, es Espacio(de trabajo), fr Atelier, nb Arbeidsrom, sv Arbetsyta). These are the ONLY two keys code references (`main_page_body._BottomNav` L582, `workspace_screen` L103); grep confirms no other section-name string.
- **NOT touched:** `nav_therapy` = Timeline/Oś czasu (index 1). `info_workspaceTabTitle`/`Body` left as-is — they describe *managing your therapy* (the therapy concept), not the section name, so per master-plan decision 3 they are not renamed.

### Part 3 — Lifecycle wiring (§1)
- Agenda: close = checkbox `touch` (unchanged mechanic) → CS-07 archive via `?view=touched`; restore = `PUT /agenda/{id}/restore`; edit = new `PUT /agenda/{id}`; delete = new `DELETE /agenda/{id}`.
- Todos: close = `PUT /todos/{id}/done` → CS-11 "Zrobione" via `?view=done`; restore = `PUT /todos/{id}/undone`; edit(+repeat) = new `PUT /todos/{id}`; delete = new `DELETE /todos/{id}`.
- Tematy i pytania: full new CRUD per §3a. Restore-from-source-card is Phase F.

### Part 4 — Agenda
- CS-06 source tags render via the existing `workspaceSourceLabel` helper (fixed vocabulary already localized) — carried through unchanged.
- CS-07 archive "Twoje zakończone tematy" = P2, fed by the checkbox close; reachable from BOTH the module hero header and the AgendaFullScreen app-bar (same data).
- CS-08 X → 3-dot menu with exactly Edytuj nazwę (P1 prefilled) + red Usuń (confirm → permanent). No odklik entry on the row.
- CS-09 "+ Dodaj temat" wide ghost button → P1 sheet (title "Dodaj temat"), tag "Dodane ręcznie", lands at top; full Nagraj/STT round-trip.

### Part 5 — Tematy i pytania (CS-05) — full anatomy renders
- Header + P2 archive ("Zamknięte tematy i pytania"); ≤5 rows (P3); each row: checkbox · text · kind chip · source tag · 3-dot (Edytuj nazwę / Dodaj do agendy / red Usuń); "+ Dodaj temat lub pytanie" P1. "Dodaj do agendy" copies to the TOP of Agenda with the source tag carried over (backend copies `source_type`/`source_id` verbatim) and the entry STAYS open here (not a toggle). Kind auto-detected from a trailing "?" (same rule as Agenda add).

### Part 6 — Do zrobienia (FIX.01 + CS-11..13)
- Checkbox is the ONLY close affordance (no row-body tap, no swipe/Dismissible — removed). Each done = a server completion-log row (backend §4).
- 3-dot menu = exactly Edytuj nazwę + red Usuń. "odklik"/"Odkliknij" removed entirely (grep-clean in `lib/screens/workspace/todo/`).
- Header task-count indicator REPLACED by the "Zrobione" P2 archive icon + badge (CS-11).
- Repeats: the edit sheet (P1 prefilled) manages Powtarzaj (Codziennie/Tygodniowo/Miesięcznie → `repeat_freq`); a set repeat shows a small repeat chip on the row. Rollover/reappear is backend-lazy (§4) — FE just renders `repeat_freq`.
- P3: ≤5 visible + expander (6+ tasks).
- CS-13 "+ Dodaj zadanie" P1 (title "Dodaj zadanie"); no due-date UI anywhere.
- **Main Homework unaffected:** this cubit never calls `/workspace/todos/today`; Main's `HomeworkTodayCubit` (3 oldest open, limit=3) is untouched — single data source preserved.

---

### API contract — followed; deviations / notes
- Wired strictly per `API_CONTRACT_Fix1_A1.md` §1/§3/§4. All endpoints verified to exist in `app/api/v1/endpoints/workspace.py` + `app/schemas/workspace.py` before wiring (agenda `PUT`/`DELETE {id}`, todo `PUT`/`DELETE {id}` + `repeat_freq`, full `topic-questions` CRUD + `add-to-agenda`). No mismatches found.
- Todo edit sheet always sends BOTH `text` and `repeat_freq` (the sheet is the single source of truth for both), so `repeat_freq: null` explicitly clears a repeat — matches the backend's sentinel contract (§4).
- **NOT consumed this slice (available, deferred):** `GET /workspace/todos/{id}/completions` (completion history) — no UI surface specced in Phase D; endpoint + manager path left for a future "history" affordance. Flagged, not a gap.
- **Badge counts** are FE-computed per §1: timestamp-per-module marker (`WorkspaceArchiveBadgeStore`, one SharedPreferences blob). "N closed since the archive was last opened" = count of archived items whose close-date is after the local marker; opening+exiting the archive stamps the marker → badge resets to 0. Self-heals across restores (timestamp-based, not id-set-based).

### Deliberate design choices (for Phase G audit)
- **Agenda active list stays compact** (top-3 + "see all" full screen) rather than inline P3 — Part 4 does not require P3 for Agenda (P3 is specced for Tematy/Do zrobienia/Phase E), and the Agenda hero is intentionally short. The full backlog + archive are reachable from the hero.
- **Do zrobienia list order is server FIFO** (homework first, oldest-first) inside P3, NOT re-sorted newest-first — this keeps it consistent with Main's "3 oldest open". P3's "newest at top" default applies to the chronological modules (Tematy i pytania); todos keep their queue order.
- **Agenda odklik machinery retained in the cubit** (`archive`/`restore`/`dismissedIds`) for the triage chip-deselect flow (contract §1 documents it as a separate mechanism); it is simply no longer exposed on the CS-08 row.
- `TodoFullScreen`/`AgendaFullScreen` (still routed) updated to the new tile API + archive + add sheet for consistency.

### Tests
- **New:** `topics_cubit_test.dart`, `topics_module_section_test.dart`, `workspace_expandable_list_test.dart` (P3), `workspace_archive_view_test.dart` (P2 badge + hub-and-spoke restore), `voice_or_text_capture_sheet_test.dart` (P1 edit mode + repeat control).
- **Rewritten for the new UI/lifecycle:** `agenda_cubit_test.dart`, `todo_cubit_test.dart`, `agenda_module_section_test.dart`, `todo_module_section_test.dart` (checkbox-only close, 3-dot Edytuj/Usuń + confirm, repeats, archive move).
- Added `ValueKey` test hooks to the three checkboxes (`agenda_checkbox_{id}` / `todo_checkbox_{id}` / `topic_checkbox_{id}`).
- `flutter test test/screens/workspace`: **91 pass / 0 fail.**
- `flutter analyze lib`: no new errors/warnings in touched files (my new files are const-clean; remaining ~98 issues are pre-existing infos/warnings in untouched files).
- Full `flutter test`: **1120 pass / 30 fail** = exactly the 30-failure baseline (0 new failures, 0 regressions; +27 net new passing tests vs Phase C's 1093/30). The 30 failures are the pre-existing baseline — none are in Workspace files (the isolated `test/screens/workspace` run is 91/0).

### Manual QA still needed (device — cannot be done in-session)
1. **P1 Nagraj/STT** on device in each add/edit sheet (Agenda, Tematy i pytania, Do zrobienia) — record → transcript lands in the field → edit → Zapisz. (Builds on Phase B's iOS WAV fix — verify no regression.)
2. **P2 badge** across app restarts: close items, confirm the green count reflects "closed since last opened"; open+exit archive → badge resets; Przywróć returns the item to the top of the active list.
3. **P3** expander on a module with 6+ items (Do zrobienia / Tematy i pytania): Pokaż więcej / Pokaż mniej / Zwiń wszystko / "Wszystkie widoczne".
4. **Repeats:** set Powtarzaj on a to-do, complete it, confirm it reappears unchecked at the next period (backend-lazy sweep — needs the aa2b3c4d5e6f migration applied on prod to exercise `repeat_freq`).
5. **Rename** reads correctly on both tabs: bottom-nav slot 3 = Pracownia/Workspace, slot 1 still Oś czasu/Timeline; header matches.
6. **Cross-module hand-off:** Tematy i pytania → "Dodaj do agendy" lands at the top of Agenda with the correct source tag, and the topic stays open in its module.

### Deploy note
- Backend for this slice (migration `aa2b3c4d5e6f`, new Workspace tables + `todos.repeat_freq` + `TopicQuestionItem` + completion log) is committed on `MindSync/main` but NOT applied on prod. The new module + repeats + edit/delete endpoints require that migration; until it runs, `topic-questions`/`repeat_freq`/`DELETE`/`PUT {id}` endpoints will 404/500. Sequence deploy + `alembic upgrade head` together (per Phase A STATUS / CLAUDE.md deploy≠migrate).
