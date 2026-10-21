---
name: posthog-flowing-events-baselines
description: Which PostHog events actually flow vs only-planned, plus 2026-06 baseline metrics and scale caveats for MindSync
metadata:
  type: reference
---

# Flowing events + baselines (verified 2026-06-29, last-30d window)

## SCALE — read this first
MindSync is effectively an early/closed beta. Real public daily-active base ≈ **3–13 users/day** (App Store build 2.0.44). Reported "DAU 20–54" is inflated by web `$pageview` (null app_version, ~379 users/30d on marketing site) + internal QA testers on TestFlight builds. **Almost every segment is < 25 users → k-anon suppression applies to nearly everything.** Treat all numbers as directional, not significant. Don't over-read swings of 1–5 events.

## Events that FLOW (~81 distinct, 30d) — selected with volumes
`$screen`(4657), `api_error`(3535 — see caveat), `tab_switched`, `timeline_viewed`, onboarding_started/step_viewed/step_completed/completed, `therapy_context_updated`, `character_card_viewed`, `reflect_message_sent`/`reflect_session_started`/`reflect_limit_hit`, `symptom_scored`/`symptom_created`/`symptom_archived`, debrief_started/created/failed, between_session_started/created, prep_card_started/created, health_check_started/completed, user_registered/logged_in/logged_out, `profile_updated`, subscription_screen_opened/product_selected/purchase_started/completed/failed, subscription_receipt_received, `promo_code_applied`, recording_upload_started/completed/failed, **`recording_chunked_upload_completed`** (v2 Postgres pipeline), voice_chat_started/ended, goal_created/status_changed, orca_named/color_changed, `bio_refreshed`, `content_shared`, `client_error`, `inapp_insight.generated` (new 2026-06-29).

## Events that do NOT flow (gaps — confirmed absent)
`paywall_shown` (no top-of-monetization-funnel), `conversation_started/message_sent/ended` (journaling uninstrumented; only `voice_chat_*`), `level_up`, `account_deleted` (churn signal), `prep_card_auto_generated`, and the whole **v2 recording funnel** (`recording_*_started/processing/saved/failed` for chunked pipeline — only the `_completed` success event exists, so start→saved funnel is impossible).

## Onboarding instrumentation (verified 2026-06-29)
- **8 steps** via `onboarding_step_viewed`/`onboarding_step_completed`, props `step_index 0-7`, `step_name`: `legal_gate(0) challenges(1) intensity(2) journey(3) modality(4) schedule(5) companion(6) lead_source(7)`. Core (0–6) step→step retention 88–99%, ~67% finish companion. **`lead_source` (step 7) is a cliff: reached by only ~7 users** (vs 71 companion) despite being live since 05-29.
- **Added profiling fields land in `profile_updated.updated_fields`** (a JSON array of field KEYS in the write, NOT proof of non-empty value). Current 7-field payload (live since 2026-05-29): `[age,age_band,currently_in_therapy,full_name,gender,lead_source,pronouns]` (~93 users). Old 4-field `[age,full_name,gender,pronouns]` retired 05-29.
- **By-design PostHog blindness (models.py comments)**: `currently_in_therapy` = Art.9, ARTICLE9_HEALTH-consent-gated; `lead_source` = "NOT sent to PostHog (re-identification risk)". On persons only `gender`/`age_band` land sparsely; `currently_in_therapy`/`lead_source`/`pronouns`/`age` not at all. So **per-field VALUE fill-rate is NOT answerable from PostHog → query Postgres `user_profile` (count non-null) + `consent_records`**.
- **`therapy_context_updated.updated_section` = null for ALL 808 events** (section not populated). No consent/Art.9/withdrawal/challenge-value events exist. Selected values of challenges/intensity/modality/schedule are NOT captured (only step completion). `onboarding_lead_source_other_text` carries `first_50_chars` of real free text (1 user) = privacy-smell to fix.
- Real acquisition source IS captured automatically on persons via UTM/referrer: `utm_source/campaign/medium`, `fbclid`, `gclid` — makes the in-app `lead_source` question largely redundant.

## CAVEAT: `api_error` is mostly benign, not errors
~80%+ of `api_error` = expected **404 on `/latest` endpoints** (prep-cards/debriefs/health-check/therapy-tracking/latest) and `get_user_profile_and_subscription` 404 for brand-new users (profile not created yet). These are empty-states, not failures, and scale with #active users. Real signals: 5xx and unexpected 4xx. Persistent real bug: `/users/notification-preferences` **500** (~constant before/after).

## app_version telemetry
- Public App Store build = **2.0.44** (257 users/30d, dominant). TestFlight builds 2.0.49–2.0.60 = testers (~8–10 each). Current frontend `pubspec` = **2.0.60+133**.
- New builds appear in telemetry days BEFORE App Store publish (TestFlight). So calendar before/after ≠ old-vs-new build. For release-effect analysis, split by `app_version` and wait ~7–10d for adoption, not a date cut.

## 2026-06 baselines (for anomaly detection next time)
- Registrations: ~2.4/day (`user_registered`).
- Onboarding completion: ~61% (19/31 users over 06-13..26); core step→step retention 88–99%.
- subscription_purchase_completed: 4 in 14 days (~0.3/day) — PostHog can't give MRR; revenue truth = Postgres `subscription_receipts`.
- Data anomaly: `reflect_limit_hit` 1191 events / **2 users** (06-03..07) = one account looping the free limit; exclude from metrics, flag as abuse/rate-limit gap.

See also [[posthog-access-fallback]]. Reports: `analytics-reports/posthog_post_update_2026_06_29.md` (post-update health) + `analytics-reports/posthog_onboarding_fields_2026_06_29.md` (onboarding field-fill).
