---
name: project-stats-tab-redesign-2026-05-18
description: Statystyki tab full redesign — Hero Insight + unified symptom module + single Premium Surface
metadata: 
  node_type: memory
  type: project
  originSessionId: 79c23b29-353d-4ff1-8b65-fb70d8751a8e
---

Statystyki (Stats) tab redesigned 2026-05-18 from the `MindSync Statystyki-handoff` design bundle. Full-stack feature.

**Backend (data-analytics):**
- New `hero_insights` table, migration `ll2m3n4o5p6q` (chains from `aa1b2c3d4e5f`; reuses existing `ProcessingStatusEnum`, `create_type=False`).
- New endpoints: `GET /api/v1/stats/overview` (returns `hero_insight` discriminated by `state`: `insight`/`empty_first`/`empty_stale`, plus `premium_teaser` null for premium users) and `POST /api/v1/stats/hero-insight/refresh`.
- AI: `generate_hero_insight()` picks the single most important daily observation + sparkline metric; `HERO_INSIGHT_PROMPT` in config.
- Hourly RQ job `app.tasks.hero_insight.generate_hero_insights` (10 PM local, free=every 7d, premium=daily, data_hash cache skip).
- Refresh endpoint has a tier-aware cooldown (`HERO_INSIGHT_REFRESH_MIN_INTERVAL_SECONDS`=3600 premium / 7d free) — fixes a security finding (unbounded OpenAI calls).

**Frontend (flutter-mobile):** Stats tab rebuilt — Hero Insight Card + empty states A/B + detail view, Unified Symptom Module (collapsed rows + inline expand + slider + 14-day chart, replaces 4 cards), restyled Cele / Kontrola Terapii, premium-only Śledzenie Terapii, single Premium Surface (replaces all inline paywalls). `TreatmentGoalsSection` deleted, FAB removed. Models in `lib/api/models/stats_overview/`.

Tests: 48 backend + 64 frontend (stats_tab) passing; 0 regressions. See [[reference_next_wave_plan_v3]] for related feature context.
