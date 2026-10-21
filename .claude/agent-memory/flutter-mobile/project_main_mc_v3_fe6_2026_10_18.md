---
name: project-main-mc-v3-fe6-2026-10-18
description: Main MC v3 FE-6 (9462956 pushed feat/main-v3) - first week on Main via GET /first-week/steps, McWeekCubit + seen store, pop-out queue, route secondaryAnimation refetch, MsFab restyled to MCHome-fab; traps (sed -i CRLF, SizeTransition clips dot, MsCubit pin, subagent report files blocked)
metadata:
  type: project
---

FE-6 of Main MC v3 committed as 9462956 on `feat/main-v3` (worktree mindsync-frontend-wt-main-v3) and pushed. Closes the Main batch. Builds on [[project-main-mc-v3-fe5-2026-10-18]].

- `lib/screens/main_tab/mc/week/`: McWeekCubit (account-scoped, must extend MsCubit), McWeekSeenStore (`mc_week_seen_<uid>`, `mc_week_final_<uid>`), mc_week_steps (copy per key, cta -> McWeekAction, McWeekActions fake seam), wide tile + McWeekTileSlot, plan sheet, mc_step_popup. Model `lib/api/models/first_week/first_week_steps.dart` (json_serializable unknownEnumValue).
- Main refetches steps on tab visit, resume, sheet close, and 2 s after a page pushed over Main pops: listen to `ModalRoute.of(context).secondaryAnimation` status `dismissed` (no RouteObserver in the app; popup routes like sheets/dialogs do not drive it, MaterialPage routes do).
- Pop-out sits in cubit state until Main shows it (visible tab, resumed, `route.isCurrent`, no sheet); `popupShown()` marks seen. First load with nothing stored seeds silently.
- MsFab (lib/widgets/ms_fab.dart) restyled to MCHome-fab; tests find `Icons.add_rounded`. Test helpers: `McWeekHarness`, `registerBoardWeek()` (MCStates shots get the wide tile), ParityShell `overlay`.
- Open: `workspace.questions` SectionAnchor does not exist (variant C step 6 lands at Workspace top); variant C copy needs Darek's OK.

**Why:** integration and later Main work reuse these seams; the traps cost rounds.
**How to apply:**
- Git bash `sed -i` rewrites a CRLF file as all-LF; edit CRLF files with Python on bytes.
- SizeTransition always clips: an overflowing corner dot gets cut; use Align(heightFactor) + ClipRect with a custom clipper that leaves room.
- DecoratedBox border does not inset the child (board inset box-shadow): keep the full padding.
- New account-scoped cubit: extend MsCubit, bump the pinned count in account_scope_reset_regression_test and the set in account_scope_reset_test.
- The harness refuses report .md files from subagents: return REPORT content in the final output.
