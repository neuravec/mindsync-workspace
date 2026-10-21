---
name: project-cards-redesign-2026-10-13
description: Cards redesign direction A (all generated cards + Timeline) on branch feat/cards-redesign; shared kit lib/widgets/cards/ms_card_kit.dart, progress panel behind PostHog flag, test/analyzer gotchas on a loaded machine
metadata:
  type: project
---

Cards redesign (reviewer decisions n_fb / n_aall on the cards canvas, 2026-10-13): every generated card (Before/After therapy, Between sessions, Recording, Reflect, Weekly, Monthly, Realization) and the Timeline moved onto ONE kit, `lib/widgets/cards/ms_card_kit.dart` (MsCardKind/MsCardTone palette shared by card headers AND Timeline tiles, MsCardHeader, MsCardSummaryBlock, MsCardSection, row widgets, MsCardChrome for full-bleed host). Branch `feat/cards-redesign`, worktree `mindsync-frontend-wt-cards-redesign`, local only.

**Why:** product owner rule "change UI, not content or functionality"; every pencil, bookmark, Share, Retry stays. To-do on cards is a proposal only (never checkable). After card "Your progress in therapy" panel reads `GET /api/v1/analytics/therapy_progress` (backend branch feat/after-card-progress) behind PostHog flag `after_card_progress_panel` (default off), event `after_card_progress_viewed` booleans only.

**How to apply:**
- New card UI goes through the kit; colours come from `MsCardTone.of(kind)`, never per-widget constants.
- Small-caps labels (SUMMARY, WHY THIS MIGHT MATTER) are `.toUpperCase()` in code: finders must use the upper-case string. Section titles stay Title Case 18/w800 (old CS-18 / MSV3.4 CS-02 14px tests were superseded).
- `therapy_card_detail_screen_error_test` had been failing on baseline only because its harness lacked a Router; fixed with MaterialApp.router.
- Gotchas: `OverflowBox` inside a Row gets unbounded width (crash); `pumpAndSettle` hangs on MsProcessingBlock spinner; cards are taller than 800x600, tap via ensureVisible; filtered `build_runner --build-filter` DELETES all other generated files (restore with `git ls-files -d | xargs git checkout --`).
- On this Windows box `flutter analyze` can exceed 10 min when other sessions run analyzers (VS Code LSP holds 2-4 GB); run it through Monitor, compile errors surface faster via `flutter test`.
- Fixed 2026-10-18 on the v3 feature branches (c82bf87 cards, 9e2d0cc workspace): pubspec now registers `family: Figtree`. Therapist name on After/Recording is a pending backend field, see [[project-cards-v3-fe4-review-fixes-2026-10-18]].

Related: [[project-account-scoped-reset-2026-10-12]]
