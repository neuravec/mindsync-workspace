---
name: reference-churn-signals-2026-10-15
description: Churn definition (14d client silence), 90d churn baselines, re-engagement push return rate, missing subscription cancel/expire events, shared-scratchpad trap. Raw: analytics-reports/raw/2026-10-15-churn-signals.md
metadata:
  type: reference
---

- Churn definition used: last client (`posthog-flutter`, default exclusions, no `$*` except `$screen`, no Application Backgrounded/Installed/Updated) activity < now-14d. Reuse it so numbers stay comparable.
- Baselines 90d to 2026-10-15: 470 active persons, 324 churned (69%), 251 of them one-day (half end on splash/welcome/auth = pre-signup). Weekly churn 41-74% of WAU.
- First-week cohort (signed-in, first seen 07-17..09-24): 79 churned vs 12 retained; active days w1 1.53 vs 2.75 is the clearest separator. Unexpected `api_error` hits ~90-100% of new users, does not discriminate.
- RE_ENGAGEMENT (`moment.sent` moment_type) 288 sends/151 users/90d; client return <72h after only 8 sends (2.8%). `moment.opened` matched by moment_id rarely followed by client activity: suspect backend-side "opened" semantics.
- No subscription cancel/expire event exists at all (re-checked 2026-10-15) -> paid churn only via Postgres `subscription_receipts`.
- `account_deleted` (python) last seen 2026-09-26, 8 users/90d.
- TRAP: the scratchpad is shared with parallel agents in the same session; a generic `q3.sql` was overwritten by another agent mid-run. Always use a unique subfolder/filename prefix.
