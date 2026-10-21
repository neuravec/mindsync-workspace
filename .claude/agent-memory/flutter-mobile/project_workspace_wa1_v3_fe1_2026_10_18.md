---
name: project-workspace-wa1-v3-fe1-2026-10-18
description: Workspace WA1 v3 FE-1 (commit 91a9f7e on feat/workspace-v3, worktree mindsync-frontend-wt-workspace-v3, not pushed) - ws_v3 building blocks, check-row timing, negative-margin hit-test recipe, test/shot gotchas
metadata:
  type: project
---

FE-1 of WA1 v3 ("WAQuiet": white cards on aquaBreeze, teal agenda only, one tonal add) committed as 91a9f7e on `feat/workspace-v3` (from origin/dev 002571d). FE-2 restyles Goals/Threads/Realizations/Relationship and pushes.

- Shared v3 kit lives in `lib/screens/workspace/widgets/ws_v3.dart` (+ `ws_icons.dart` SVG paths, `ws_top_bar.dart` with `WsAboutSheet`). `WorkspacePalette` is now v3 tokens only.
- Board CSS negative margins (-12 header buttons, -4 row menus) cannot be done with Transform: hit tests fail outside the ancestor's size. Recipe used: header buttons are `Positioned` in a card-level `Stack`; row lists wrapped in `WsBleedEnd` make `WsModuleCard` shrink its right padding by 4 and pad every other child; agenda pencil positioned over the session block after a `TextPainter`-measured meta width.
- `WsCheckRow` calls the cubit after `AnimationController.forward().orCancel`; the controller reports completion on the first frame strictly AFTER its duration, so tests do tap, `pump()`, `pump(1100ms)`, `pump(1ms)`.
- Callback type `FutureOr<void> Function()` keeps full screens (todo/agenda full screen pass non-awaiting closures) compiling.
- Delta 18.10 12:29 (About Workspace sheet, one paragraph per module) was added in FE-1 with 8 `ws_about*` keys.

**Why:** three teams (workspace, cards, character) merge later; low-churn, file-scoped diffs matter.
**How to apply:** for parity shots wrap `MaterialApp.builder` in the RepaintBoundary (a `home` boundary misses modal sheets), one `runAsync` capture per test. `containsSemantics` is deprecated in Flutter 3.41: use `isSemantics`. The Write tool turns `—` escapes into real dashes (fix with `chr(0x2014)` in a script); multi-quote Python in a Bash heredoc can break, write the script to a file. Related: [[project-workspace-wa1-v2-redesign-2026-10-13]].
