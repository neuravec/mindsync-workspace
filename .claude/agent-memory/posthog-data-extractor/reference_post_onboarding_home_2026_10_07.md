---
name: reference-post-onboarding-home-2026-10-07
description: How to measure "what new users do after onboarding lands them on Home" (landing definition, instrumentation gaps for GettingStartedCard/FAB, moment.opened join) plus 2026-10-07 baselines and the 10 s /query/ execution cap workaround
metadata:
  type: reference
---

Extract: `analytics-reports/raw/2026-10-07-post-onboarding-home-behavior.md`.

**Definitions that worked**
- `onboarding_completed` fires on `$screen_name = therapyOnboarding`; then the `wow` screen (post-onboarding flow); landing = first `$screen` with `$screen_name = 'mainPage'` after it. `mainPage` is the tab shell, not the Home tab, so "prev screen = mainPage" does not prove a tap came from Home.
- Auto-fired on first Home render: `notification_permission_prompted` (OS dialog), `app_tour_started`/`_step_viewed` (sheet opens 1 s after render), `first_capture_prompt_shown` (`entry_point = home_empty_state` = GettingStartedCard; `timeline_empty_state`; `post_onboarding` = wow first-step screen). So "zero events after landing" is always 0; count "zero product actions" instead.
- `tab_switched.tab_name` in {main, therapy, reflect, workspace, character}; app tour does NOT switch tabs.

**Instrumentation gaps (2026-10-07)**: GettingStartedCard taps and FAB expand/flow-pick have NO events (`entry_point = fab` only labels `usage_chip_tapped_at_zero`). Proxy = flow `$screen`s (`afterTherapyFlow`, `prepTherapyFlow`, `betweenSessionsFlow`, `recordSessionFlow`). `trial_reminder_sheet_shown` never fired as of 2026-10-07. `first_capture_prompt_option_tapped` flows (since 10-03) though the local FE checkout no longer references it.
- `moment.opened` carries only `moment_id` (no `moment_type`): join to `moment.sent` on `moment_id`; 12/17 opens did not match. Client `notification_opened` has `moment_type` (and a `user_id` = Firebase UID, never select it).

**Baselines (kept n=42 onboarding completers 2026-09-01..10-06, directional)**: landed 41; tour started 34/41; zero product action in 30 min 5/41; core capture in 30 min 22/41; return [24h,8d) 9/30; 3+ active 24h-days in week 1 <5/32; notif permission granted 36/42; 39/42 got a `moment.sent` in week 1 (WEEKLY_SUMMARY_READY to 35). New-wave traffic (Android CI/DZ/IR/IQ/PK/SA since 09-20): 48 persons, 7 start onboarding, 4 complete, so it can never be split at k>=5.

**Query mechanics learned**: `/query/` now runs with `max_execution_time = 10` (visible in error text), 504 on breach. Multi-CTE population joins over all flutter events time out. Fix that worked: compute the population once, keep the person_id list ONLY in the scratchpad, substitute it as `person_id IN (...)` in each query, delete the list after; the committed extract shows the defining CTE plus a `__POP_IDS__` placeholder. `toTimeZone(ts, properties.$timezone)` fails (zone must be constant): pull (tz, UTC hour, count) and convert locally with `zoneinfo`. The runner now continues past a failing section (2026-10-07 patch) instead of discarding the whole batch. See [[default-exclusion-filters]], [[reference-post-onboarding-offer-and-test-accounts-2026-10-03]].
