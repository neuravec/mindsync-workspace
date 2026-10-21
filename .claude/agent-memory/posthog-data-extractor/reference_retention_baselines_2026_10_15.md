---
name: reference-retention-baselines-2026-10-15
description: Canonical "active" definitions (broad vs strict post-login), 90d DAU/WAU/MAU, weekly cohort, D1/D7/D30 pre/post 10-03, lifecycle and feature-stickiness baselines as of 2026-10-15; array-based single-scan retention pattern.
metadata:
  type: reference
---

**Two active definitions (reuse so numbers repeat):** broad = any posthog-flutter event minus passive/system (`$identify`,`$set`,`$exception`,`client_error`,`notification_received`,`usage_snapshot`,`app_install_attributed`,`notification_banner_shown`...). Strict = broad minus pre-login: `$screen`/`tab_switched` with `$screen_name` in splash/welcome/auth/signUp/forgotPassword/therapyOnboarding/wow, `onboarding_*`, signup/auth/consent/login/password_reset/notification_permission events, `user_logged_in/out`, `welcome_cta_tapped`. Exact lists in `analytics-reports/raw/2026-10-15-retention-engagement.md`.

**Why it matters:** broad MAU is ~3x strict (week 10-05: 234.6 vs 73.0) because install inflow since 09-21 (new/week 46, 78, 57) mostly bounces before login. Never report broad MAU as engagement.

**Baselines (2026-10-15):** strict DAU 4-10, MAU 61-83, DAU/MAU 0.066 (Jul) to 0.117 (Oct). Broad weekly W1 retention 8-18%; onboarded-only W1 27-31%. Strict D1/D7/D30 Jul-Aug cohorts: 12.2% / 27.0% / 37.8% (n=74). Post-10-03 too small to judge (D1 6/28). iOS retains far better than Android (D7 38% vs 17%, confounded). Lifecycle: dormant > new+resurrected almost every week. Feature 28d: timeline 57u, habits view 50, workspace 40, therapy loop 28, reflect 28, voice 23, trends n<5 (no event).

**Gaps:** no Trends open event (`stat_opened` new 10-14, 1 user); `subscription_tier` is person-level current state only (113 premium, mostly signup trial), so retention by status at cohort time is impossible.

**Pattern (fast, no self-join, passed 10 s limit):** one `GROUP BY person_id` with `min(toDate(timestamp))` + `groupUniqArray(toDate/toStartOfWeek(timestamp,1))`, then `has()`/`arrayExists()` outer. Rolling DAU/WAU/MAU: DISTINCT person-day, `ARRAY JOIN range(30) AS n`, `uniqExactIf(person_id, n<7)`. Lifecycle: `ARRAY JOIN arrayMap(i -> addWeeks(toStartOfWeek(today(),1), -i), range(0,13)) AS W`. Multi-dim breakdown: `arrayJoin([('os',os),('tier',tier)]) AS t` + `tupleElement(t,1)` (aliasing the tuple inside ARRAY JOIN + GROUP BY alias failed). UNION ALL needs an outer SELECT wrapper to ORDER BY an alias.

**Shared scratchpad:** parallel agents share the session scratchpad and overwrite generic names (q1.sql). Always use a private subfolder.
