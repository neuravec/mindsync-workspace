---
name: usage-trend-and-paywall-exposure-2026-09-25
description: Monthly app-usage series May-Sep 2026 (MAU shrinking, intensity rising), cohort D1/W1/W4, paywall reach 3.9% of MAU, and the auto 4-day trial mechanism that hides paywall+gates
metadata:
  type: reference
---

Report: `analytics-reports/2026-09-25-usage-trend-and-paywall-exposure.md`.

## Monthly series (app persons, $F = flutter + no device farm + no emulator)
- MAU full month May..Sep(24d): 246 / 218 / 162 / 144 / 111. First-24-days like-for-like: 211/189/130/129/111.
- New app persons: 213/174/116/101/73. Returning-from-prior (24d window): 30/42/37/39/38 = FLAT core ~40.
- Days/user 1.63 -> 2.05; sessions/user 2.27 -> 3.11; DAU/MAU(24d) 6.6% -> 8.6%. Part of the rise is mix (fewer 1.4-day new users).
- Cohort D1: May 6.6 / Jun 6.3 / Jul 5.2 / Aug 9.9 / Sep 11.9 (n=67). W4: 6.1/2.9/3.4/8.4(n=95). Aug+Sep D1 vs May-Jul p~0.05, RE-READ 2026-10-25.
- Raw PostHog (all libs) Aug = 97.5k events / 1916 persons vs Jul 18.6k/183: backend crons. This is the likely source of the "usage grew" impression.

## Paywall exposure
- `paywall_shown` lifetime 16 events (since 2026-08-16); 30d reach 5/127 MAU (3.9%); sub screen 10/127.
- Gate-triggered paywall/sub-screen opens: 1-2 people/month. No onboarding paywall (trigger constant unused).
- `TrialPopupManager.handleTrialPopups()` / `canAddNote()` NEVER called -> trial welcome, $5 offer, trial-ended->paywall popups are dead code (verify before recommending again).
- **Auto trial**: `POST /users/subscription` -> `_create_initial_subscription(uid, 4)` = 4 days premium, `granted_via='signup_trial'`; paywall_shown suppressed while premium; 70.7% of registered users (258/365) never active on day 4+ -> they never see free tier or a gate.
- Retained free (first seen <08-20, active last 30d) n=33 avg 1.73 active days/30d; premium n=7 avg 11.4. Free users mostly read (timeline 15/33).
- 403 retry storms: `/reflect/{id}/message` 1191 (Jun) + 1872 (Aug) from 2 users each; recording initiate 76 from 1 user (Sep). Likely client retry loop on gate.

## Traps found this session
- Backend `reflect_message_sent` dropped in Sep (87) while client `reflect_message_submitted` = 384; use `reflect_session_started` users for a consistent Reflect series.
- `subscription_tier` person prop unset for ~72% of MAU and includes trials; `is_premium` event prop only on new features (habits, reflect picker). Neither is a premium-share metric; DB is.
- Prod DB via `heroku run` was BLOCKED by the permission classifier ("Production Reads") in a subagent session; script left in scratchpad. Ask operator for the grant up front next time.
