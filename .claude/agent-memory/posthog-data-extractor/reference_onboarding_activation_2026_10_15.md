---
name: reference-onboarding-activation-2026-10-15
description: Onboarding + activation funnel pre/post 2026-10-03 redesign, step taxonomy (step_index -1..7, conditional modality/schedule), first_conversation_* family, first-week-plan has no exposure event, aha candidate = debrief in week 1; shared-scratchpad gotcha
metadata:
  type: reference
---

Extract: `analytics-reports/raw/2026-10-15-onboarding-activation.md` (30d window 09-15..10-15).

- Step taxonomy: `onboarding_step_viewed/_completed` carry `step_name` + `step_index` (100%). Index -1 = `personalise` (before `legal_gate`=0), then challenges, intensity, journey, modality, schedule, companion, lead_source (7). Since 10-03 `modality`/`schedule` are conditional (shown to ~1/3 after journey). `outcome=skipped` exists on journey/schedule/lead_source.
- No app-language property on onboarding events; only device `$locale`.
- Post-onboarding chain (all flutter): `post_onboarding_build_viewed` -> `first_conversation_intro_viewed/_started/_ended/_recap_result` (from 10-05) -> `paywall_shown` trigger `post_onboarding*` / `post_onboarding_offer_shown` (exists since 10-09, contradicts the 10-03 note "no offer_shown") / `_offer_result`.
- `first_week_plan_*`: only toggled/hidden/failed, NO shown/viewed event, 3 users by 10-15: exposure unmeasurable.
- Baselines: onboarding completion 47% (pre) -> 74% (post), n=36/38. Biggest post leak: build -> first-conversation intro 26 -> 17. 24h any-conversation 14% -> 42%.
- Aha candidate (pre cohort, n=33): `debrief_started` in week 1 -> 5/6 returned in week 2 vs base 18%. `timeline_viewed` == onboarding completion (fires on home landing), never use it as an action.
- Cohort CTE pattern with tester exclusion: HAVING no testflight/emulator/bot-device events AND no `onboarding_reset` AND `onboarding_completed` < 3.
- HogQL gotchas hit: `toInt32OrNull` unsupported; alias equal to a column name used in outer countIf (e.g. `habit`) -> illegal_aggregation, prefix aliases; `FROM coh INNER JOIN events` + `uniqIf` gave HTTP 500 "column doesn't exist", `FROM events e INNER JOIN coh` + `count(DISTINCT if(...))` worked; CTE + UNION ALL also failed, use one wide SELECT.
- The scratchpad is SHARED with parallel agents: always use a unique subfolder and unique file names (q3.sql got overwritten mid-run on 10-15).
