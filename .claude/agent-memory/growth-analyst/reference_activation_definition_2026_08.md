---
name: activation-definition-2026-08
description: MindSync's empirically derived activation metric (first therapy-loop capture within 24h), its baselines, the retention lift per candidate action, and the reusable cohort-lift HogQL pattern
metadata:
  type: reference
---

# Activation definition (derived empirically 2026-08-10)

Report: `analytics-reports/2026-08-10-activation-definition.md`. Cohort = 652 app-only
persons first seen 2026-05-01..2026-07-26.

## THE DEFINITION (use this everywhere)
**Activated** = new user who **starts or creates >=1 therapy-loop artifact within 24h of
first app open**. Qualifying set (any one):
`debrief_started|debrief_created`, `prep_card_started|prep_card_created|prep_capture_started|prep_capture_submitted`,
`between_session_started|between_session_created`, `reflect_message_sent`,
`health_check_started|health_check_completed`, `symptom_created|symptom_scored`,
`goal_created`, `recording_started|recording_saved`, `quick_capture_submitted`.

- Denominator = new **registered** persons (has `user_registered`). Secondary denominator
  = all new app persons (shows the auth-screen leak).
- **Baseline 2026-08-10: 41.5% (85/205) of registered; 17.0% (111/652) of all new app persons.**

## Window discipline (non-negotiable, avoids the tautology)
Action window `[first_ts, first_ts+24h)`; return d2-7 = `[first_ts+48h, first_ts+8d)`;
return d8-28 = `[first_ts+8d, first_ts+29d)` (only for `first_ts < now-29d`).
Windows must NOT overlap or "activity predicts activity" wins trivially.

## Baselines to detect anomalies against
- Return d2-7: **10.4%** all new app persons (68/652); **17.6%** registered; **5.8%** never-authed.
- Return d8-28: 10.1% (61/602 full-obs).
- Activated: return d2-7 **25.2%** vs 7.4% (3.41x, p<0.0001); d8-28 21.7% vs 7.7% (2.83x).
  On the registered denominator the lift is only **1.98x** (24.7% vs 12.5%, p=0.024) and
  d8-28 loses significance (p=0.18). Always report both; use registered for OKRs.
- >=2 active weeks: 35.7% activated vs 13.7% not (2.61x). >=3 weeks 15.2% vs 4.8%.
- TTFV: median `user_registered` -> first capture = **4 min**, p90 126 min; 93/118 capture
  within 1h. TTV is NOT the problem; 80.5% never capture at all.
- Cohort composition: **430/652 (66%) never authenticate** (no `user_registered`, no
  `user_logged_in`), 8.4 events in 24h, 5.8% return. Biggest absolute leak, upstream of activation.
- Weekly activation trend declining ~25-27% (May) -> 7-15% (July). Week 2026-06-21 (94 new
  app persons vs 27-32 baseline) is a QA-contaminated anomaly.

## What was rejected (do not re-litigate)
- **`onboarding_completed` is NOT activation.** 2x2: onb-only 11.4% (n=35, ns) vs
  onb+capture 25.8% (n=93) vs neither 7.1% (n=506). Onboarding is necessary-not-sufficient.
  Its raw 3.01x lift disappears under session-depth control; capture's does not.
- **Threshold is ONE capture, not 2+.** Dose-response 0->7.4%, 1->24.4%, 2->21.6%, 3+->30.0%.
  Within onboarded, `cap>=2` and `cap>=3` add nothing (25.0% vs 20.5%/21.9%).
- **No single capture type beats the set** (all CIs overlap, n=23-79 per type). Must be an
  action SET. Best raw singles: reflect 35.7% n=28, between_session 33.3% n=27, health_check 28.9% n=38.
- **Confound honesty**: stratified by d0-1 event volume, capture survives only in the 21-50
  band (25.0% n=28 vs 5.6% n=54, 4.50x, p=0.011); in the 51+ band lift falls to 1.6x
  (control n=19). It is a leading indicator, not proven causal. Only an A/B settles it.

## Instrumentation verdict: DERIVED metric, NOT a client-side `user_activated`
Three reasons: (1) `reflect_message_sent`, `symptom_*`, `goal_created` and all `*_created`
are **backend-only** (`$lib='posthog-python'`) - a Flutter listener would miss 3 of 9
categories, exactly the highest-lift ones; (2) derived works retroactively on all 652
historic persons today; (3) "once per user ever" is stateful and client state dies on
reinstall (already 17 persons have a capture but no `user_registered` = `$identify` merge noise).
Recommended additions: person props `activated_at` (`$set_once`), `activation_action`,
`time_to_activation_hours`, `activation_within_24h` set **server-side** by `data-analytics`,
plus a server-side `user_activated` event for targeting only.
`flutter-mobile`'s real gap = `first_capture_prompt_shown` / `_dismissed` (we cannot tell
whether the 82.9% who never capture were ever ASKED) + `hours_since_signup`/`is_first_capture`
on client capture events + a client `reflect_message_submitted`.

## Reusable HogQL pattern (cohort-lift analysis)
Self-join `events e` against a subquery giving `person_id, min(timestamp) AS first_ts`
(filtered to `$lib='posthog-flutter'`), then `GROUP BY pid, fts` with `countIf(<event> AND
e.timestamp < f.first_ts + INTERVAL N HOUR) > 0` flags. To emit a long-format lift table
from one query, `arrayJoin(arrayZip(['name1','name2',...],[flag1,flag2,...]))` then
`GROUP BY cand`. Canonical SQL in the report's Appendix A; batch files kept in scratchpad
(`act1_discovery.sql` .. `act6.sql`).
**GOTCHA: `toUInt8()` does not exist in HogQL - use `toInt()`.** Booleans must be cast to
int before `arrayZip`. Sub-select columns used in `GROUP BY` must be SELECTed.

## Event availability cutoffs (verified via min(timestamp), 2026-05-01..08-10)
`user_registered` from 2026-05-06 (backend). `recording_started/saved` from 2026-07-03.
`notification_permission_granted/prompted/denied`, `workspace_opened` from **2026-08-04**.
`quick_capture_*` from 2026-08-07. `app_tour_*`, `signup_*`, `consent_*` from ~2026-07-27.
=> notification-permission and recording could NOT be tested as activation candidates.
**Retest after 2026-09-15.**
Also verified: **0 of 852 app-first persons ever emitted a `web` event**, so for an app-first
cohort you may safely use ALL their events (flutter + python) without web pollution -
filtering every query to `$lib='posthog-flutter'` would wrongly drop backend capture events.

## Benchmarks used
Health & Fitness mobile retention D1 ~27% / D7 ~10% / D30 ~4% (vmobify, Prooflytics, Plotline).
SaaS activation median ~36-37.5%, SMB target 35-50%, top quartile 68% (Tandem, Perspective AI,
ProductQuant). NOTE: our "returned any day 2-7" is LOOSER than exact-D7, so parity with the
10% D7 benchmark actually means we are below it.

See also [[posthog-access-fallback]], [[posthog-web-vs-app-split]], [[posthog-flowing-events-baselines]].
