---
name: project-stats-tab-redesign-2026-05-18
description: Full Stats tab redesign — Hero Insight, Unified Symptom Module, Premium Surface — shipped 2026-05-18
metadata:
  type: project
---

Stats tab was fully redesigned in session 2026-05-18.

**Key architecture decisions:**
- `StatsOverviewState` is a standalone Freezed file (`stats_overview_state.dart`) with its own `part 'stats_overview_state.freezed.dart'`. It is NOT a `part of` the cubit file.
- `StatsOverviewCubit` imports `stats_overview_state.dart` directly; no `part` directives.
- `StatsOverviewManager` handles `GET /api/v1/stats/overview` and `POST /api/v1/stats/hero-insight/refresh`.
- `HeroInsightResponse` is a manual sealed class with `fromJson()` discriminating on `state` field: `insight` / `empty_first` / `empty_stale`.

**New files created:**
- `lib/screens/stats_tab/cubit/stats_overview_state.dart` — standalone Freezed state
- `lib/screens/stats_tab/widgets/premium_surface.dart` — deepOcean paywall card (free users only)
- `lib/screens/stats_tab/widgets/share_strip.dart` — dashed share button using `ShareCardConfig.symptomTracking()`
- `lib/screens/stats_tab/hero_insight_detail_screen.dart` — full-screen detail view
- `lib/screens/stats_tab/widgets/hero_insight_card.dart` — HeroInsightArea with 4 states + shimmer
- `lib/screens/stats_tab/widgets/unified_symptom_module.dart` — collapsible rows, M3 slider, 14-day chart
- `test/screens/stats_tab/stats_overview_cubit_test.dart` — 14 cubit unit tests
- `test/screens/stats_tab/hero_insight_area_test.dart` — 6 widget tests

**Removed from stats tab screen:**
- FAB (floating action button)
- TreatmentGoalsSection
- SnapshotsSection
- All inline Subscribe buttons
- `SnapshotsCubit` provision

**Section order in stats_tab_screen.dart:**
HeroInsightArea → UnifiedSymptomModule → GoalsSection → HealthCheckSection → TherapyTrackingSection → ShareStrip → PremiumSurface

**Pre-existing test failures (NOT caused by this work):**
- l10n_completeness_test: `error_requiresRecentLogin` and `error_emptyPassword` missing from all 6 non-English locales — pre-existing gap
- settings_cubit_delete_account_test: 7 failures — pre-existing
- reflect_chat_bubble/input tests: ~7 failures — pre-existing

**Why:** Full design spec implementation. Backend endpoints provided by integration-devops contract.
**How to apply:** If touching stats tab, check these files first. If adding new cubit states, remember the standalone state file pattern.
