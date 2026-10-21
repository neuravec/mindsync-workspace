---
name: tab-bottom-clearance-2026-10-19
description: Character tab bottom cut-off fix (bc878ce, fix/character-bottom-cutoff, pushed, not merged); shared MainTabScrollEnd/MainTabBottomClearance, MainPageBody shell test harness, SafeArea-context inset trap
metadata:
  type: project
---

Fix bc878ce on branch fix/character-bottom-cutoff (pushed 2026-10-19, fast-forward from origin/dev b8e6151, not merged to dev).

**Root cause:** main_page_body.dart overlays the bottom bar (56 + inset) and the + (MsFab, bottom 76 + inset, 56 tall) on every tab. v1 character sheet (f1aad74, live via 5c27b2c 2026-10-14) ended 40 px after SafeArea, KE (e337b05) 24 px, so the last item sat under the bar. Legacy tab cleared the bar but not the +. Timeline/Workspace (100 px) ended under the +; Main Premium (no status row) last tiles under the +. Not a Main v3 regression: + and bar unmoved since May/July.

**Shared approach now:** `MsFab.size`, `MsFab.bottomOffset(context)` (lib/widgets/ms_fab.dart) and `MainTabBottomClearance.of(context)` / `const MainTabScrollEnd()` sliver (lib/widgets/main_tab_scroll_end.dart) = 76 + inset + 56 + 16. Use it as the last sliver of any main-tab scroll view.

**Trap:** `MediaQuery.paddingOf(context)` read in a build method that itself creates the SafeArea (State context above it) returns the inset (34) and double counts it. Read it below the SafeArea: a widget (MainTabScrollEnd) or a `Builder`. Timeline/KE builders were already inside.

**Test harness:** test/screens/main_page/main_page_shell_harness.dart pumps the real MainPageBody (GoRouter needed: Reflect's BackButtonListener wants a Router), `installShell()` registers only what is not registered, `loadShellFonts()` (Figtree; test font overflowed PetHeroCard at 360 wide), `expectClearOfNavAndFab(..., gapAboveFab: 16)` catches both cut-off and double-counted inset. PageView builds only the selected page, so a test needs only that tab's DI. Related: [[main-mc-v3-fe1-2026-10-18]].
