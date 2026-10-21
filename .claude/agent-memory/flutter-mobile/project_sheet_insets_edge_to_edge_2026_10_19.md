---
name: sheet-insets-edge-to-edge-2026-10-19
description: fd70889 fix/week-plan-cta-visible (pushed, ff from dev bc878ce) - Android edge-to-edge root cause, McSheetFrame bottomPaddingOf/footer/topGap, plan CTA pinned, device harness + sheet case catalog, open app-wide list
metadata:
  type: project
---

fd70889 on `fix/week-plan-cta-visible` (worktree mindsync-frontend-wt-week-plan-cta), pushed, not merged.

**Root cause (applies app-wide):** targetSdk = flutter.targetSdkVersion = 36, so Android 15+ runs edge to edge: the 3-button bar (48) and gesture bar (24) and the status bar lie over the app and arrive as MediaQuery padding. Any fixed bottom padding < 48 ends under the 3-button bar. Do not opt out in the manifest (Play policy, impossible on 16 anyway). The bc878ce shell harness `ShellDevice.androidButtons` still models bottom 0 (pre edge-to-edge); real 3-button is 48.

**Main sheets now:** `McSheetFrame.bottomPaddingOf(ctx)` = max(viewInsets + 34, padding.bottom + 16); `McSheetRoute(useSafeArea: true)` + frame LayoutBuilder caps height at room - 24 (`topGap`); optional `footer` (showMcSheet `footerBuilder`) pins header + footer, body scrolls. Plan CTA = `McWeekPlanCta` in the footer; `McWeekPlanSheet` is Stateful and jumps the active row into view post-frame; helpline shares the reminder slot (Stack passthrough) to keep H-1 equal height.

**Test kit:** test/screens/main_tab/mc/mc_device_support.dart (McDevice with real insets, applyMcDevice, showMcKeyboard sets viewInsets AND zeroes padding.bottom, McSystemBars overlay for PNGs, expectSheetClearOfSystemBars) and sheets/mc_sheet_cases.dart (37 states of every Main sheet/pop-out/FAB). Shots: test/main_parity_shots/mc_device_insets_shot_test.dart with MC_DEVICE_SHOTS_DIR (86 PNGs in ~15 s).

**Why:** the lead asked for an app-wide follow-up; these seams make it measurable.
**How to apply:**
- New sheets/pages: bottom = fixed gap + MediaQuery.paddingOf(context).bottom, never a bare constant.
- Open outside Main (Explore audit 2026-10-19, not fixed): ws_top_bar.dart:141 WsAboutSheet fixed 34; skill_detail_sheet.dart:35 fixed 24; record_session_flow.dart:516 fixed 32; debrief_capture_screen.dart:1589 HC prompt "Skip"; custom_calendar_view.dart:435 "Add" (viewInsets only); session_setup_screen.dart "Add" (20 + viewInsets in a Scaffold body); recently_deleted_screen.dart:198; persona_picker_screen.dart:51; check_email_view.dart top; privacy/terms/notes/chart_info text pages.
- Stack default fit is loose: children lose the Column's stretch width; use StackFit.passthrough.

Related: [[tab-bottom-clearance-2026-10-19]], [[project-main-mc-v3-fe6-2026-10-18]]
