---
name: character-ke-fe2-2026-10-18
description: Character KD v2 (KE) FE2 on feat/character-kd2-v3 (058266a, pushed to origin only) - Skills/Tools tabs, shared idea block, KE2 map in board coordinates, Rename/Hide; hooks left for FE3 and parity tricks
metadata:
  type: project
---

FE2 of the Character tab KD v2 ("KE", team character) is committed as 058266a on `feat/character-kd2-v3` in the worktree `mindsync-frontend-wt-character-kd2` and pushed to origin (never dev). FE1 was e337b05.

**Why:** operator asked (2026-10-18) for three independent teams to build Character, Before/After cards and Workspace 1:1 with the artifact; integration team merges later.

**How to apply (for FE3 / integration):**
- `openKeSkill()` in `lib/screens/character_tab/ke/ke_navigation.dart` only logs `skill_opened`; FE3 must push KeSkillScreen there with `RouteSettings(name: KeRoutes.skill)` so the Orca idea action can `popUntil(!KeRoutes.isKe)` back to the tab.
- `openKeMap(context, source:, initial:, pathId:)` (ke_map_screen.dart) is the entry for KE4 "See my map" (source `step_screen`).
- `KeIdeaBlock` has a `KeIdeaVariant.skill` (radius 24, "Tell Orca how it went", short done copy) ready for KE3; `keActOnIdea()` does the Orca pop + `selectTab(2, action: 'new_thread')`.
- `KeRenameSheet` already supports `skillName` (40) and `skillWords` (280) modes for KE3.
- Map selection lives in `KeSheetLoadedState` (mapPathId / mapForming / mapSkillId), kept across quiet reloads.

Non-obvious recipes that worked:
- KE2 map: build the Stack in the board's own 390x420 coordinates and wrap in `FittedBox(fit: BoxFit.fill)` sized to card width; painter, labels and node hit-testing scale together, giving a near pixel-identical render. Node targets 48 board-px = 44 screen-px.
- Idea header: board header is 20 px with "Not now" overflowing via negative margins (not hittable in Flutter). Made the row 44 px and `Transform.translate(0,-2)` on the content below (+ bottom padding -2): exact board parity and a real 44 px target.
- Default Skills selection prefers an ACTIVE idea, so a test on an acted idea must tap that cell first.
- `SemanticsData.hasFlag` is deprecated in Flutter 3.41: use `flagsCollection.isSelected == Tristate.isTrue` (import `dart:ui show Tristate`).
- Writing `'—'` escapes into Dart through a python heredoc ended up as literal dashes in the file; in dash-guard tests compare runes (`r == 0x2014 || r == 0x2013`) instead.
- Decision log for this task: support row shows in every idea slot (KE1 card, KE2 panel) even if that skill/path has no idea; "Path hidden." snackbar carries Undo (hidden paths are not returned, so it is the only way back); with no ray the KE2 headline is "Your map is taking shape." / "Your map starts with your first note or talk." and no panel when nothing forms.

Related: [[project_character_kd_2026_10_13]], [[project_redesign_v3_teams_2026_10_18]]
