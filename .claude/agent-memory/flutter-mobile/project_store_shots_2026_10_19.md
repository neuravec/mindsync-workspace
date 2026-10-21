---
name: project-store-shots-2026-10-19
description: App Store + Google Play screenshot harness (store_shot.dart, 8 store_*_shot_test.dart) on feat/store-shots b0db599 local; real GoRouter + real MainPageBody shell, iOS/Android frames with drawn status bars, chrome/dash checks, known FAB overlaps
metadata:
  type: project
---

b0db599 on feat/store-shots (worktree mindsync-frontend-wt-store-shots, from origin/dev 40e3469, not pushed). PNGs in Heroku/store/renders/{ios,android}/ + manifest.json. Run one file per slide: `flutter test test/marketing_shots/store_<name>_shot_test.dart --tags marketing --run-skipped` (default output is store/renders, not social/; app-shots.py not used).

- Separate harness `store_shot.dart` (marketing_shot.dart untouched, because unmerged branches v3b and redesign both edit it with conflicting `beforeCapture` semantics). It pumps `MaterialApp.router` + one GoRoute, so `TherapyCardDetailScreen(item: TherapyTimelineItem.debrief(...))` renders with its real chrome (no BackButtonListener crash) and `MainPageBody` works via `storeShell()` + `installShell()` from test/screens/main_page/main_page_shell_harness.dart.
- Main cannot use the real shell (MainPageBody builds McMainScreen with DateTime.now): `StoreMainShell` replicates `_BottomNav` + MsFab around `McHarness.screen()`.
- Frames: iPhone 1179x2556 TargetPlatform.iOS; Android 1080x2400 @2.625, insets 40/24. Status bar + handle drawn by `StoreSystemBars` (wrap in transparent Material or the clock gets the yellow debug underline; handle stays dark even with `lightStatusIcons`).
- Chrome check uses `RenderParagraph.getBoxesForSelection` per line (paragraph box is full width and gives false hits). `STORE_SHOTS_REPORT_ONLY=1` prints instead of failing. Icons drawn by CustomPaint (KeIcon chevron) are not caught.
- Fits that needed data choices: Timeline 5 rows iOS / 6 Android so nothing runs under +/bar; Reflect 5 short turns; Workspace 2nd to-do shortened to clear the + on Android; recording summary one line shorter.
- Known real-layout overlaps (reported, not fixed): Character KE on Android 411x914 the + covers the Tools segment (whitelisted via `allowUnderFab`); on iPhone it covers the Your map chevron. Main: + touches last tile row by 1 px.
- English time formats differ: Main "5 PM", Workspace agenda "17:00", Timeline rows "19:30" (DateFormat.Hm).

**Why:** operator refreshed the store screenshot set from real renders (2026-10-19).
**How to apply:** reuse store_shot.dart for any future store/marketing shot that needs a Router or the real tab shell. Related: [[project-marketing-shots-redesign-2026-10-14]], [[project-tab-bottom-clearance-2026-10-19]].
