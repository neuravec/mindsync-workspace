---
name: character-ke-fe3-2026-10-18
description: Character KD v2 (KE) FE3 on feat/character-kd2-v3 (052960d + 57d2f78, pushed to origin only) - KE3 skill screen, KE4 stage moment presenter, share image; fake-async hang, snackbar-in-every-Scaffold, sync-emit-before-listener and CSS border parity gotchas
metadata:
  type: project
---

FE3 of the Character tab KD v2 ("KE") is commits 052960d + 57d2f78 (skill_screen_load_failed) on `feat/character-kd2-v3` (worktree `mindsync-frontend-wt-character-kd2`), pushed to origin only. Builds on FE1 e337b05 and FE2 058266a. Parity shots: `test/character_parity_shots/fe3_ke_skill_step_parity_shot_test.dart` (KE3 renders at exactly the board's 1822 px).

**Why:** operator's 2026-10-18 three-team redesign (character / cards / workspace); integration team merges and deploys later.

**How to apply (integration / follow-ups):**
- `openKeSkill()` now pushes KE3 with `KeSkillCubit(skillId, sheet: KeSheetCubit)`; KE3 shares the sheet's manager (`KeSheetCubit.manager`) and mirrors every change back via `applySkill / applySkillStage / applyIdea / applySkillRemoved / applySkillRestored`.
- KE4 presenter lives in `character_tab_screen.dart` (`presentKeStages`): only when the Character tab is visible and the tab route is current, never while `reading_history`; unseen stage-ups after "See my map" are released (`releaseStages`) and come back next visit.
- `KeSheetCubit.load(quiet, track)`: quiet loads requested mid-flight are queued (a remove followed by a fast Undo is not lost); internal reloads pass `track: false` so `character_sheet_viewed` counts only real visits.
- Decisions: KE4 has a close X (board has none, iOS has no back button; PopScope routes back to "next stage-up"); mint pips on the solid Yours hexagon; In your words hidden when the server sends none; 404/409 on KE3 closes it and reloads the sheet.

Gotchas that cost time:
- `await Future.delayed(Duration.zero)` inside `testWidgets` (fake async) never completes: the whole run hangs. Await the cubit's own futures instead.
- ScaffoldMessenger renders a SnackBar in EVERY registered Scaffold (tab below + pushed route): finders need `findsWidgets` / `.last`.
- A mocked call that throws synchronously makes the cubit settle (e.g. on `gone`) before `BlocListener` subscribes: re-check the state in a post-frame callback.
- CSS `border-top` takes layout space; Flutter `DecoratedBox` does not, `Container` does (adds the border to its padding). 1 px per row drifted the KE3 list until switched.
- `SliverFillRemaining(hasScrollBody: false)` + `Spacer` overflowed with the wide test font; `Expanded(SingleChildScrollView(top)) + pinned bottom block` is robust.
- `tester.ensureVisible` needs a `pump()` before `tap`, or the tap uses the stale position.

Related: [[character-ke-fe2-2026-10-18]], [[project_redesign_v3_teams_2026_10_18]]
