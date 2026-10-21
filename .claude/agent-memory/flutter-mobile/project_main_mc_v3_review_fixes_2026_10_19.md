---
name: project-main-mc-v3-review-fixes-2026-10-19
description: Main MC v3 review fixes (061c87a pushed feat/main-v3) - full-screen replay masks on McSheetRoute/pop-outs, therapy tiles send load bucket only, steps_done run-from-1 + out_of_order, MsFab column layout, first_conversation source proposal; traps (Write/heredoc CRLF, Ahem widths, sed path miss)
metadata:
  type: project
---

Review-fix round on Main MC v3 committed as 061c87a on `feat/main-v3` (worktree mindsync-frontend-wt-main-v3) and pushed. Builds on [[project-main-mc-v3-fe6-2026-10-18]].

- Replay (security H-1): `McSheetRoute.buildPage` wraps the page in a full-screen `PostHogMaskWidget` (`screenMaskKey`), `McSheetFrame` masked too, pop-outs masked full screen (`McStepPopup.screenMaskKey`), Main scroll area masked (`McMainScreen.maskKey`). Plan sheet keeps the helpline slot via `Visibility(maintainSize)` (adds 52 px under the CTA in standard tone: flagged).
- Analytics: session + relationship tiles send `state` = loading|loaded|error only, agenda no dot, `dot_tiles` excludes all three (`McAnalytics.therapyStateTiles/therapyDotTiles`). First week: steps_done = active-1, popup past first open step sends `out_of_order: true` not step_index.
- `McWeekState.showTile` false once allDone; `isPlanRenderable` gates the final pop-out.
- `mcSessionDay` one rule for tile/agenda/sheet; `showMcSheet(caption:)` for "7 days"; `MsFab` rows are a Column (rows grow), `MsFab.anchorRight/gutter/menuWidth/rowKey/pillKey/buttonKey`.
- To-do first talk relies on PROPOSED backend `source_type: first_conversation` (not built).

**Why:** integration and security re-verify read these seams; the traps cost rounds.
**How to apply:**
- Check line endings with Python (`b.count(b'\r\n')`), not `grep -q $'\r'`: analytics_events.dart, mc_session_sheet.dart, ms_fab.dart are CRLF, mc/ files LF. Use a crlf-aware load/save helper in edit scripts.
- Widget tests measure text in Ahem (1 em per glyph): for width-dependent layout tests load Figtree with FontLoader in setUpAll.
- `excludeSemantics: true` drops the child's tap action: add `onTap` to the Semantics node.
- When copying the review render tool, verify the `_out` rewrite applied (a sed miss overwrote review-extra raw renders; p_*.png composites kept the before state).
