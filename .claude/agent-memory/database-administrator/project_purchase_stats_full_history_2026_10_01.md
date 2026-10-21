---
name: project_purchase_stats_full_history_2026_10_01
description: Full-history purchase/subscription stats from subscription_receipts, user_subscription, user_subscription_trial (2026-10-01) — unique payers, recurring rate, trial conversion, data-quality gaps
metadata:
  type: project
---

Full-history (not just 30d) purchase audit, 2026-10-01: 1898 users total. subscription_receipts has 124 rows (62 VERIFIED, 62 FAILED, exactly 50/50), 45 unique payers ever, 13 of them (29%) have >=2 receipts. Top-3 "recurring" users (22, 23, 13 receipts) are almost certainly TestFlight/sandbox test accounts, not real repeat buyers — no environment column exists to filter mechanically, so this has to stay a manual flag. user_subscription active today = 26, but only 8 of those have a matching subscription_receipts row (granted_via=purchase); 15 are signup_trial, 2 promo, 1 null — confirms/extends the 2026-08-17 finding that auto-trial is indistinguishable from real premium at the user_subscription level. had_trial=true for 554/1895 trial-table rows; 28 of those later show a receipt (5.05% trial->paid). trial_outcome and trial_platform are 100% NULL on all 1895 rows despite existing as columns — same save-path-bug signature as other NULL-despite-key-exists findings, flagged to backend-api (likely _atomic_mark_trial_started/_ended not actually setting these).

platform_transaction_id (the HI-001 anti-reuse column) is populated for 68/68 Google rows (100%) but only 3/56 Apple rows (5%) — Apple coverage is effectively broken, opposite of order_id (Apple 0/56, Google 42/68). No amount/price/currency/environment column exists anywhere in subscription_receipts or user_subscription (re-confirmed; see also [[project_subscription_revenue_30d_2026_09_12]]) — revenue is not computable from Postgres, only product_sku counts (apple premium_m_01=47, google premium_m_01=32, google ms_starter_package=30 [unclear/possibly legacy SKU, flagged to backend-api], apple premium_y_01=9, google premium_y_01=6).

Why: this was the first full-history (not 30-day-window) purchase audit; prior reports only looked at recent windows and concluded "too few events" without establishing the historical base rate.
How to apply: when asked for purchase/subscription/revenue numbers, start from this snapshot instead of re-deriving; re-run the underlying queries if the question is time-sensitive (this is a point-in-time count). Full report: db-reports/2026-10-01-purchase-stats.md.
