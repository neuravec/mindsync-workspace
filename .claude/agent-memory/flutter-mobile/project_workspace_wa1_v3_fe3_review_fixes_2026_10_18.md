---
name: project-workspace-wa1-v3-fe3-review-fixes-2026-10-18
description: WA1 v3 FE-3 review fixes (9e2d0cc fonts + 7183eff, pushed feat/workspace-v3) - pubspec Figtree family fix, no row menus on To-do/Threads, sub-page kit, 200% clipped-text test recipe, test cascade cause, Python-to-Dart regex escape trap
metadata:
  type: project
---

FE-3 fixed 15 frontend review findings on WA1 v3 (Workspace) and pushed `feat/workspace-v3` (9e2d0cc, 7183eff). Integration still decides on: the app-wide font change, top-bar unification (boards disagree: Workspace 64/24/700, Character 64/22/700, Main 56/22/700), and the board 11/12 px chips and meta vs Darek's 13 px minimum.

- **Font bug fixed** in its own commit: pubspec `family: Lato` -> `Figtree` (theme asks for Figtree, so devices fell back to Roboto/SF). Guard test `test/ui/app_font_family_test.dart` reads FontManifest.json. Parity shots now load fonts from FontManifest.json, not a hand-registered family. 9e2d0cc also carries the deletion of the dead `realization_repo_tile.dart` (a `git rm` staged earlier gets swept into the next commit).
- **Rows without a board menu**: `WorkspaceItemMenu.showAt(context, rect)` and `semanticActions(l10n)`. `WsCheckRow.onOpenMenu` turns the text column into a tap and long-press target. Threads open the actions on a long press, and `ThreadDetailScreen` has a Pin/Delete menu.
- `ws_subpage.dart` (WsSubpageScaffold/List/Card) is the v3 look of every "See all", archive and detail screen.
- Queued threads are a historical status (PATCH answers 409), so their chip is static. The cubit also refuses to send the PATCH.

**Why:** the landing had to match the board 1:1, and a designer would see the font, the extra menus and the old sub-pages first.
**How to apply:**
- 200% text check: `RenderParagraph.getMaxIntrinsicHeight(size.width) > size.height` catches fixed-height Row parents but not Wrap ones. It was proven non-vacuous by mutation.
- Test cascade: one failing widget test broke every later test, because GetIt reset ran before the tree was disposed and dispose() called `sl<>`. Cache `sl` lookups in initState.
- In `isSemantics(customActions:)` order and ids differ. Map `customSemanticsActionIds` through `CustomSemanticsAction.getAction`. `onTapHint` adds an action with a null label.
- Python writing Dart regex `\b` produced 0x08 bytes and a vacuous test. Check with `od -c`.
- On this machine `flutter analyze` prints `error -`, not `error •`.
- A worktree under the scratchpad path fails with "Filename too long". Use a short sibling path and remove it afterwards.

Related: [[project-workspace-wa1-v3-fe1-2026-10-18]].
