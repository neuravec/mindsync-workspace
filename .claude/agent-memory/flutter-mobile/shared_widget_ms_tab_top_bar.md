---
name: shared-widget-ms-tab-top-bar
description: MsTabTopBar — unified top bar widget used by all main tabs; prevents header drift
metadata:
  type: project
---

## MsTabTopBar

Location: `lib/widgets/ms_tab_top_bar.dart` (exported via `lib/widgets/_widgets.dart`)

Canonical design spec (Character tab is the reference):
- Container height: `SizedBox(height: 56)`
- Outer padding: `EdgeInsets.symmetric(horizontal: 8)` (NOT 16)
- Hamburger: `SizedBox(48×48)` + `Material(transparent)` + `InkWell(borderRadius: 24)` + `Icon(Icons.menu, size: 24, color: MsColors.deepOcean)`
- Gap after hamburger: `SizedBox(width: 8)`
- Title: `Expanded`, `fontFamily: 'Figtree'`, `fontSize: 22`, `FontWeight.w600`, `color: MsColors.deepOcean`, `letterSpacing: -0.1`, `height: 1.27`
- Optional `trailing` widget before info icon — used for Therapy tab's trash badge
- Info icon: `Semantics(button: true, label: infoTitle)` + `SizedBox(48×48)` + `Material` + `InkWell` + `Icon(Icons.info_outline, size: 22, color: MsColors.deepOcean.withValues(alpha: 0.55))`
- Tapping info opens `SectionInfoSheet` with the `infoTitle`/`infoBody` params
- No background color (transparent — inherits from Scaffold's `backgroundColor`)

Used by:
- `character_tab_screen.dart` — `character_title`, `info_characterTabTitle/Body`
- `therapy_tab_screen.dart` — `therapy_journeyTitle`, `info_therapyTabTitle/Body`, `trailing: _TrashIconBadge`
- `reflect_tab_screen.dart` — `chat_reflectTitle`, `info_reflectTabTitle/Body` (only the thread-list state; `_ChatTopBar` is separate)
- `stats_tab_screen.dart` — `stats_title`, `info_statsTabTitle/Body`

Tests: `test/widgets/ms_tab_top_bar_test.dart` — 10 tests (all pass)

**Why:** The four tabs each had their own inline `_TopBar` classes with drift: different padding (8 vs 16), extra decorative icons (psychology_outlined, bar_chart), different font styles (MsStyles.titlePage at 20 vs Figtree 22 w600), different info-icon colors (neutral[400] vs deepOcean.withValues(0.55)), and in Reflect's case a bottom border and wrong background color. Extracted to prevent future drift.
