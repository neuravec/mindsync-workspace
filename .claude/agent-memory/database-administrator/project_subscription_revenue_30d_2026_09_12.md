---
name: project-subscription-revenue-30d-2026-09-12
description: 30-day prod subscription revenue truth check (2026-08-13..2026-09-12) - 2 verified purchases total, 68% of users never had a conversation, notification job dominates AI cost
metadata:
  type: project
---

Full report: `db-reports/2026-09-12-subscription-revenue-30d.md`.

**Core finding:** in the 30-day window only **2 VERIFIED receipts** exist in `subscription_receipts`
(1 apple 2026-08-19, 1 google 2026-09-07, both `product_sku='premium_m_01'`, 2 distinct users).
Not zero, but statistically noise. Cross-checked against [[project_hi001_receipt_reuse_check_2026_08_16]]:
that check saw 120 total receipt rows; this check saw 122 - exactly +2, consistent.

**`granted_via` breakdown of the 18 currently-active-premium users** (column added
[[project_trial_paywall_block_fix_2026_08_18]]): only **7 are real purchases**, 8 are the free
signup_trial, 2 are promo, 1 is legacy/null. So "active premium" as a headline number is misleading -
most of it is not revenue.

**No amount/price/currency column exists anywhere in `subscription_receipts`** - revenue in PLN/USD is
NOT computable from this DB, only purchase-event counts. Confirmed again: no environment/sandbox column
either, so Apple TestFlight vs production purchases remain indistinguishable at the DB level (same
conclusion as [[project_testflight_sub_renewal_audit_2026_08_18]]). Tried a cadence heuristic (repeat
apple receipts <36h apart = TestFlight signal): the single 30d apple receipt has no repeats, so the
heuristic is inconclusive either way for this specific receipt - flagged as an honest "can't confirm"
rather than guessed.

**Historical context (all-time):** 60 VERIFIED receipts total since 2025-03-31 (48 google + 12 apple).
Monthly VERIFIED count has been 1-3/month since March 2026 (one outlier spike: Oct 2025 google=11,
likely a campaign, ~11 months stale). **The 30-day near-zero is NOT an anomaly - it's the norm for the
last 6+ months.** Don't chase "what broke this month" - the flatline predates it by a long way.

**Engagement is the real story, and it fully explains the revenue number:** 1259/1855 users (67.9%)
have NEVER had a single conversation, ever. Only 25/1855 (1.35%) had any conversation in the last 30
days. 360 users (60.4% of everyone who ever started >=1 conversation) have exactly 1 conversation total
(one-and-done). Functionally-free users (not is_active premium) = 1837/1855 = 99.03%.

**AI cost anomaly worth a dedicated look:** 30d total AI cost = $112.13 USD (132,773 token_usage_log
rows, 1826 distinct user_ids logged - nearly the whole user base, NOT just the 25 actually-active
users). Per-feature breakdown: **NOTIFICATION feature alone = $91.96 (82% of total cost, 106,789 rows)**
- dwarfs everything else including actual CONVERSATION cost ($0.07/38 rows). This means the
notification-generation background job is running against essentially the entire user base regardless
of engagement, and is the dominant cost driver, not therapy conversations. Worth flagging to
data-analytics/growth-analyst: is this job scoped/throttled by recent activity, or blasting everyone?

**New data-quality finding (report it, don't fix it):** `user_subscription_trial.trial_outcome` is
**100% NULL (1852/1852 rows)** despite the column existing specifically for this
(`'converted'`/`'expired'`, added for PostHog B12 instrumentation per the model comment). Classic
key-present-value-null save-path bug signature - handed to backend-api/data-analytics to diagnose,
not investigated further in this pass (out of scope, would need code trace of
`deactivate_expired_subscriptions` and the post-trial purchase path).

**Minor edge case:** 3 users have zero `user_subscription` row at all (out of 1855). Not investigated,
flagged for backend-api.

**registrations:** 158 new users over the last 12 weeks (~13/week average, one spike week 2026-08-03=25,
last week in window is partial (6 days)).
