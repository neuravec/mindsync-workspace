---
name: retention-priorities-2026-10-03
description: Baselines + traps from the 2026-10-03 retention/subscription priorities review - day-0 action lift table, push channel spent on summary-ready pushes, new low-intent Google Play wave since 09-20, post-onboarding offer skip risk
metadata:
  type: reference
---

Report: `analytics-reports/2026-10-03-retencja-subskrypcje-priorytety.md`.

## Baselines (registered cohorts, first client event, bots excluded)
- D1 Jun/Jul/Aug/Sep: 7.6 / 7.7 / 12.2 / 16.3% (n 105/52/74/43). Return d1-7: 20 / 25 / 29.7 / 25.6%.
- Day-0 lift (n=270, Jun-Sep 23): capture 44.1% vs 16.5%; Reflect 37.8% vs 17.2%; check-in 37.1%; neither 14.0% (215/270 = 80% do neither). Push granted d0 gives NO lift (17.9%).
- Push opt-in fine: 81 granted / 100 prompted (60d). Content is the problem.
- 30d pushes: 8798 to 1841 persons, 97% WEEKLY/MONTHLY_SUMMARY_READY (4 opens / 0). Weekly summary has NO activity gate (`weekly_therapy_summary.py:44`). Only 32.5% of new users get a non-summary push in week 1.
- `inapp_insight.shown` = 0 since 2026-08-24; realization_viewed ~2 persons/month. Reward layer is dead.
- Reflect: Sept 8 of 17 users >15 msgs/month -> the new 15 limit is the only free limit that binds.

## Traps
- **New acquisition wave from 2026-09-20**: Android low-end devices (Samsung A0x, Tecno, Infinix, itel), CI/DZ/IR/IQ/PK/SA; new persons/week 21 -> 72, account-creation share 64% -> 28%; install_source google-play, no UTM. MAU 30d jumps to 203. Segment every read after 09-20 or the 10-03 redesign gets misjudged.
- `moment.sent` has no `is_ai_generated` (only `moment.scheduled` does); `moment.opened` has no `moment_type` (join on `moment_id`, cast `toString()` or HogQL throws cannot_parse_number).
- `subscription_purchase_completed` includes Linux/Windows events with null product_id: filter `$lib`.
- Post-onboarding offer skip rule `wow_cubit.dart:268-272` treats `premiumSource == null` as already premium; 10-03 first 2 cases both `already_premium` (testers likely). Re-check offer-shown share per onboarding completer ~2026-10-10.
- HogQL: an output alias equal to an inner column name (e.g. `sum(ret) AS ret`) -> illegal_aggregation; rename aliases.
