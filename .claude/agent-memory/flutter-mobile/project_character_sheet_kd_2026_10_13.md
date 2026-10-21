---
name: project-character-sheet-kd-2026-10-13
description: KD character sheet v2 (KD1 sheet, KD2 star of skills, KD3 new skill) behind PostHog flag character_sheet_v2, branch feat/character-sheet; gate pattern, tooling gotchas
metadata:
  type: project
---

KD character sheet FE on branch feat/character-sheet (worktree mindsync-frontend-wt-character-sheet), local commit only, backend contract from MindSync feat/character-sheet 0b9061f.

- Gate: CharacterSheetCubit starts `initial` which renders the LEGACY tab, so flag-off users see no flash. `disabled` on flag off, any 404, 403 profiling_consent_withdrawn. Code in lib/screens/character_tab/sheet/.
- Legacy CharacterTabCubit keeps loading: companion row opens CharacterCompanionScreen reusing `_legacyCharacterChildren` (name/colour/persona/bio stay reachable).
- KD3 moments: a BlocListener misses a state that was already loaded when the body mounts (load resolves before next frame), so a post-frame check in initState is also needed.
- Analytics constants live in sheet/character_sheet_analytics.dart (not analytics_events.dart) to avoid merge conflicts; skill_unlocked/star_point_added are backend-only.
- **Why:** flag default off pending legal review of PROFILING (n_kd2, n_kdstar2).
- **How to apply:** gotchas: `build_runner --build-filter` WITH `--delete-conflicting-outputs` deletes every other generated file (restore with git checkout); without the flag it still rewrites ~170 freezed files (revert all not in your allowlist). ARB edits: insert lines next to an anchor key instead of json re-dump (keeps diffs small, fewer conflicts). Full `flutter analyze` takes >10 min on this machine when many worktrees exist.

**Update 2026-10-14 (5c27b2c on feat/redesign-final, local):** flags `character_sheet_v2` and `after_card_progress_panel` REMOVED by operator decision. Sheet always on; legacy tab only for kill-switch 404 or failed first load (`disabled(reason: failed)`, retried on next tab visit). Missing PROFILING consent = 200 `{locked:true}` -> `CharacterSheetState.locked`, tap -> shared `lib/widgets/profiling_consent_dialog.dart` -> POST /character_sheet/consent. Same consent lock exists on the progress panel (`locked_reason: profiling_consent_required`). Security M-B: dialog copy must say Orca memory comes back on + withdraw in Settings (tests pin it). Consent funnel events are shared `profiling_*` with `surface`. Gotchas: heredocs with backticks/quotes in python -c get mangled by the shell, write scripts with the Write tool; Freezed getters need `const X._();`.
