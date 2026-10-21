---
name: project-character-sheet-kd-2026-10-13
description: KD character sheet backend (stats, skills, star of skills) on branch feat/character-sheet, migration m320c4a5r6d7, flag CHARACTER_SHEET_V2_ENABLED; design decisions that are not obvious from code
metadata:
  type: project
---

Branch `feat/character-sheet` (worktree MindSync-wt-character-sheet, commit 0b9061f, 2026-10-13), NOT pushed, migration NOT applied anywhere.

Decisions worth remembering:
- Endpoint GET/POST `/gamification/character_sheet[/seen]`, 404 unless `CHARACTER_SHEET_V2_ENABLED` or UID in `CHARACTER_SHEET_V2_USER_IDS`; 403 `profiling_consent_withdrawn`. Legal PROFILING decision pending.
- Stats never decrease: high-water marks JSON in `character_sheet_state.stat_marks`. First sheet read = silent sync (unlocks inserted with seen_at set, no PostHog, level recorded as seen) so old history does not replay as KD3 moments. `mark_seen` must NOT create the state row (it would turn the next read into a non-first read and replay history).
- Star paths = visible `user_symptoms` (Focus Areas), max 6; ray grows with logged DAYS/WEEKS, never score values; path skills give no stat bonus; focus-area name never stored in unlock rows nor sent to PostHog (`path_ref` = symptom id).
- `activity_breakdown` on /character_card left byte-identical (shipped Flutter shows raw key for unknown keys); corrected list is new field `orca_xp_breakdown`.
- Migration id collision risk: release branch has `m319a1b2c3d4` (cte index) also off m318. If it lands on main first, re-point m320's down_revision to m319 and update `test_m318_first_week_migration.py::test_only_known_successor`.
- No rest-day record and no portrait-card ratings exist in DB, so Self-care = habit days + full habit weeks, Insight = kept realizations only.

**Why:** reviewer notes n_kd2/n_kdstar2 (no numbers from mood/symptoms, nobody fails a skill, names private).
**How to apply:** when extending the sheet or merging with the cards team, keep these invariants and recheck the alembic head. Related: [[offline-verification]].
