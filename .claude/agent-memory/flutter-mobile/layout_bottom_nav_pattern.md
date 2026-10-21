---
name: layout-bottom-nav-pattern
description: How to position Positioned/FAB widgets above the BottomNavigationBar in the main page Stack, and how to set scroll clearance padding
metadata:
  type: feedback
---

The BottomNavigationBar in `main_page_body.dart` is `Positioned(bottom: 0)` with a fixed height of **76 logical pixels**. The MsFab on other tabs uses `bottom: kBottomNavBarHeight + MediaQuery.of(context).padding.bottom` as the reference.

**Shared constant:** `kBottomNavBarHeight = 76.0` is defined in `lib/resources/ms_border_radius.dart`.
Import with: `import 'package:mindsync_app/resources/ms_border_radius.dart';`

The 76 is the bar's *content* height only — the `BottomNavigationBar` widget itself absorbs the safe-area inset internally (it renders taller on notched devices). So callers must ALWAYS add `MediaQuery.of(context).padding.bottom` separately to clear the full on-screen footprint.

Any tab widget that renders its own floating element (FAB, CTA button in a Stack/Positioned) MUST account for both:
1. The BottomNav content height: `kBottomNavBarHeight`
2. The device safe-area inset: `MediaQuery.of(context).padding.bottom`

**Correct pattern for a Positioned FAB above the BottomNav:**
```dart
import 'package:mindsync_app/resources/ms_border_radius.dart';

final safeAreaBottom = MediaQuery.of(context).padding.bottom;

Positioned(
  right: 18,
  bottom: 24 + kBottomNavBarHeight + safeAreaBottom,  // spacing + nav + safe area
  child: ...,
)
```

**Correct pattern for scroll list bottom clearance:**
```dart
SliverPadding(
  padding: EdgeInsets.only(
    bottom: kBottomNavBarHeight + safeAreaBottom + fabHeight + spacingAboveFab,
  ),
)
```
Where `fabHeight = 56` and `spacingAboveFab = 24` for the Reflect tab FAB.

**Why:** The tab content (`PageView` children) fills the full Stack height, which extends BEHIND the `Positioned` BottomNav bar. There is no automatic inset — you must add `kBottomNavBarHeight` manually.

**How to apply:** Whenever placing a `Positioned` widget at the bottom of a tab that lives inside the main `PageView`, always import and use `kBottomNavBarHeight + safeAreaBottom` in the `bottom` offset. Never use a hardcoded `76.0` locally.
