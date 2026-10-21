---
name: reference-release-impact-oct-2026-10-15
description: Build-to-feature map for Oct 2026 releases (2.0.100 store redesign, 2.0.107 Android store first-conversation v2, 2.0.109+ first-week guidance, 2.0.111 cards, 2.0.112 GPT-Live-1), which new events flow vs never fired, weekly baselines 09-19..10-15
metadata:
  type: reference
---

Verified 2026-10-15 (extract `analytics-reports/raw/2026-10-15-recent-changes-impact.md`).

**Build map (store reach is the real "after" date, not the deploy date):**
- 2.0.100 = first store build with 03.10 subscription/onboarding redesign (Android 53 users, iOS 8), same day 10-03.
- First conversation v2 (FE 05.10) reached store users only in 2.0.107 Android (first seen 10-07, first real `first_conversation_started` 10-09 23:11) and 2.0.106 iOS. 2.0.107 is the main Android store build as of 10-15 (41 users/7d).
- 2.0.109 (10-12) first carries first-week guidance events; 2.0.111 (10-14) cards/Workspace redesign; 2.0.112 (10-15) GPT-Live-1. All testers only (TestFlight 1-3 people/build + a few Android). 2.0.110 Android had 9 users: unclear if Play test track or staged rollout.
- Android store vs test track cannot be separated in PostHog; infer from user counts per version.

**Event status 10-15:** flowing (tiny, testers): `today_card_viewed/_tapped`, `first_week_plan_*`, `side_card_tapped`, `reminder_optin_result`, `session_sheet_completed`, `follow_up_started`, `fab_*`, `workspace_item_action`, `after_card_progress_viewed`, `profiling_*`, `art9_consent_step_shown/_declined`, `voice_engine_changed`, backend `voice_engine_selected` + `voice_live_session_ended`. Never seen: `first_week_recap_*`, `quick_checkin_*`, `today_card_deferred`, `side_card_dismissed`, `session_sheet_opened`, `rhythm_*`, `getting_started_card_tapped`, `voice_live_fallback`, `voice_moderation_event`, `voice_delegation_attempted`, `user_fragments_merged`. Re-check once these builds hit the store.
- `voice_chat_started.voice_engine` only present from 2.0.112 (live); Classic on older builds = property absent. Split is "live" vs "absent".
- Backend `trial_started` flows since 10-03 (1 event per user, clean): W3 21, W4 33 users.

**Weekly baselines (app, bots excluded):** active 54/97/94/54(6d) for weeks starting 09-19/09-26/10-03/10-10; new persons 33/76/66/34; `signup_started` users 11/17/14/22; `onboarding_completed` users 6/10/13/20. "New persons" overcount real signups heavily (W2: 76 new vs 17 signup_started), so use signup_started as funnel denominator.
- Skew traps: `subscription_purchase_completed` W3 291 events/6 users (one person 140, iOS payment-fix testing), `user_activated` W3 197/6.

**How to apply:** for any before/after question on an Oct-2026 feature, anchor "after" to the store build date above, not the deploy date; see [[reference-post-onboarding-offer-and-test-accounts-2026-10-03]] for tester heuristics.
