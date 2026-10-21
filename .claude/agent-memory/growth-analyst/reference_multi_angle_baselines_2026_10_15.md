---
name: multi-angle-baselines-2026-10-15
description: Baselines and definition reconciliations from the 8-extract PostHog synthesis of 2026-10-15 (funnel, strict MAU, fr/ar/fa traffic, post-03.10 redesign, data-hygiene list)
metadata:
  type: reference
---

Report: `analytics-reports/2026-10-15-posthog-multi-angle.md` (inputs `analytics-reports/raw/2026-10-15-*.md`).

Baselines (realni, bez botów/testerów):
- 60d 08-16..10-15: 296 nowych → 94 start onb (32%) → 71 ukończ. (24%); R7 18% (45/250), R14 10% (19/186). en: 33% ukończ., R14 18%.
- MAU ścisłe (po zalogowaniu) 73-83; MAU szerokie ~250 (2/3 to odbicia przed logowaniem). Use STRICT as "real users".
- Post-03.10 flow (n=38 starters): onb 74% (pre 47%), first conv 39%, build→intro loses 35% (26→17). Conversation in 24h 42% vs 14%.
- Paywall reach 5.8% → 14.9% of actives after 03.10. 0 yearly purchases in 60d (yearly is preselected). iOS trial→paid 0/10.
- fr/ar/fa Android wave 09-21..10-05 = ~60% of new, 5-11% onb, R14 ~0. Always split en vs rest.
- 1 active day in week 1 → 0/8 returned in week 2.

Definition traps resolved:
- `moment.opened` is NOT an app open (only 10/62 match a send); use client `notification_opened`.
- `subscription_purchase_completed` double-emitted (client+backend) + Windows dev backend writes to prod PostHog (186 events). Never count purchases from PostHog.
- 404 on get_user_profile_and_subscription / therapy-context = first-run path (100% fresh installs), mislabelled is_expected=false. Closes B3 from 09-12.
- 26% of backend `user_registered` have no app events under same person_id.
- WEEKLY/MONTHLY_SUMMARY pushes still go to ~1800 accounts (6942 sends/31d, 7 opens) despite v549 cost cut. See [[baselines-and-unit-economics-2026-09-12]].

Re-measure: 10-29 (R14 for 03.10 cohort), 11-02 (D30), 14d after 2.0.109+ hits stores.
