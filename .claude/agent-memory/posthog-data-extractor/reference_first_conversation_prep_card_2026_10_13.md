---
name: reference-first-conversation-prep-card-2026-10-13
description: How to trace the onboarding first conversation -> "Before therapy" prep card in PostHog; backend job telemetry is person-less and has never arrived; use prep-cards/latest 404 polling + backend consent_granted ARTICLE9_HEALTH as proxies
metadata:
  type: reference
---

Verified 2026-10-13 (extract: `analytics-reports/raw/2026-10-13-ios-prep-card-missing.md`).

**Chain of events (first conversation, ship 2026-10-05):** client `first_conversation_intro_viewed` -> `first_conversation_started` (mode) -> `first_conversation_ended` (mode, reason, reached_open) -> `first_conversation_recap_result` (status ready/short) -> `post_onboarding_offer_shown` -> Home `today_card_viewed` -> `prep_card_opened` (source, processing_status). Backend: `reflect_session_ended` with `entry_origin='onboarding_first_conversation'` = proof /end reached the prep-card enqueue point; `orca_memory_items_saved` follows ~3 s later.

**Blind spots:** `prep_card_auto_generated` is person-less by design (random distinct_id, security H-1/M-1), so no platform/person split. As of 2026-10-13 it has NEVER carried `source=first_conversation` (only `auto_cron`), and `first_conversation_prep_card_outcome` never appeared, even for a confirmed-success Android case. Treat backend job telemetry as missing, not as "zero cards". No app lifecycle (background/terminate) events exist in the project.

**Proxies that worked:** (1) `api_error` 404 on `/api/v1/prep-cards/latest` per person after `first_conversation_ended`: polling that stops within ~20 s while the person keeps using the app = card exists; continuous 404 for hours = no card. (2) backend `consent_granted` with `consent_type='ARTICLE9_HEALTH'` (client only sends `gdpr`). On 2026-10-13: 0/4 iOS onboarders since 10-01 had ART9 vs ~half of Android; missing card correlated with missing ART9 on both OSes. iOS 2.0.110 introduced `art9_consent_step_shown`/`_declined` on Home after the conversation.

**How to apply:** for any "card not generated" bug, pull these two proxies per person and hand timestamps (onboarding_completed, first_conversation_ended to the second) to `database-administrator` for matching; never put distinct_ids (Firebase UIDs, length 28) in committed extracts. Nested aggregates (`countIf(... timestamp > minIf(...))`) fail with `illegal_aggregation`: compute the anchor in a joined subquery.

**Follow-up same day (onboarding branch):** step property is `outcome` (saved/skipped), not `step_outcome`; `onboarding_step_save_failed` has never existed. `total_steps=7` on the `journey` completion = "in therapy" branch (modality + schedule shown), `5` = not in therapy. On Android the backend ART9 consent lands right after the `intensity` step (12 of 13). As of 2026-10-13 no iOS person on a build newer than 2.0.94 took the 7-step branch or got ART9 in onboarding, and there was zero `api_error` on any consent endpoint (so the request is probably never sent). iOS App Store builds (`$is_testflight=false`): 2.0.90, 2.0.94, 2.0.100, 2.0.106; everything else on iOS is TestFlight testers. PostHog sees fewer iOS onboarders (~11) than the DB has iOS accounts (18).
