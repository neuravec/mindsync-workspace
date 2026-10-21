---
name: project-redesign-v3-integration-2026-10-19
description: FE integration of redesign v3 (9a11854 pushed as integration/redesign-v3, base origin/dev 002571d) - entry-level ARB merge recipe, worktree -b upstream trap, B-1 scheduleClock seam, KE gap events, week_completed, first_week_home_cards left in place
metadata:
  type: project
---

Branch `integration/redesign-v3` (worktree mindsync-frontend-wt-integration-v3) merges --no-ff workspace-v3 b023486, cards-v3 6705fe0, character-kd2-v3 a11fd4a, main-v3 061c87a on origin/dev 002571d, then 5 own commits. Pushed 2026-10-19; nothing on dev. Builds on [[project-main-mc-v3-review-fixes-2026-10-19]] and [[project-character-ke-ux-fixes-2026-10-18]].

- ARB conflicts: do NOT json.dumps the ARB (files have blank lines between some entries, a re-dump rewrites thousands of lines). Split the top-level object into raw member texts (string-aware depth scan), 3-way merge per key (base = merge-base blob, ours = index stage :2:, theirs = branch blob), append theirs-only keys after their predecessor, write back CRLF. Then `flutter gen-l10n`; verify the final ARB equals base + every team's changes and that no key changed on two sides.
- Main renamed 11-14 existing values per language (Mood trend -> Focus Areas); no other team's new key used the old name.
- `git worktree add -b X <path> origin/dev` sets X to track origin/dev: run `git branch --unset-upstream` right away.
- build_runner on the merged tree found one stale generated file (main's mc_week_state.freezed.dart doc comment): committed it alone.
- B-1: `MainTabCubit.scheduleClock` (@visibleForTesting) pins now for _computeNextSession/_computeLastSession; the four 7-day shifts use `_shiftDays`. `_isOnWeek` still uses Duration.inDays (minor: nothing writes the biweekly anchor today).
- KE events added: path_unhidden {path_index}, character_save_failed {change, surface, status_class}, rename_sheet_abandoned {field} (logged inside showKeRenameSheet for all 3 modes).
- habit_check_toggled.week_completed = server week_completed_now; the celebration is the subset with xp_awarded > 0.
- first_week/widgets: only first_week_home_cards.dart is unimported from lib, but 5 tests import it and their "through FirstWeekCubit" cases cover slot wiring still used by recap/rhythm; left in place.

**Why:** the next integration round (backend merge, release) will hit the same ARB and upstream traps.
**How to apply:** reuse the entry-level ARB merge for any multi-team l10n conflict; check `git status -sb` for a wrong upstream before any push.
