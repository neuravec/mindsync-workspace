---
name: errors-quality-gaps-2026-08-10
description: api_error root causes, recording-pipeline funnel gap, and full instrumentation-gap lists (never-fired / went-silent / low-signal) as of 2026-08-10
metadata:
  type: project
---

Full extract: `analytics-reports/raw/2026-08-10-errors-quality-14d.md`.

## api_error decomposed (previously unexplained heavy volume)
- `api_error` is NOT one problem. Two distinct causes explain nearly all of it (14d: 4507 events/60 users):
  1. **403 on `/api/v1/reflect/{conversation_id}/message`** = 1870 events, **1 user** (matches the known `reflect_limit_hit` skew). This is the daily-reflect-limit being hit repeatedly by one account (retry loop), not a bug affecting users broadly.
  2. **404s on `…/latest` endpoints** (`/prep-cards/latest` 1024/41u, `/debriefs/latest` 980/42u, `/health-check/latest` 440/34u) = 2617 events, 60 users — this is the broad, multi-user pattern. Strong hypothesis (not confirmed): "no record yet" empty-state returning 404 instead of 200-with-null, hit by nearly every active user. Worth backend-api / data-analytics confirming against the endpoint code.
- Concentration: top-1 user = 43.6% of all api_error volume (the reflect-limit account), top-5 = 75.4%. Excluding the top user, remaining volume is broad (34-42 users per endpoint), not noise.
- `error_class` breakdown: 4493/4507 are `HTTPException` (i.e., intentional `raise HTTPException` in app code, not unhandled crashes) — so "api_error" as an event name is misleading; it's capturing normal HTTP error responses, not exceptions.
- `api_error` is server-side only — cannot be split by `$app_version` (no client properties on backend events). Restated every time this event is analyzed.

## Recording pipeline funnel (14d) — mostly unmeasurable, not confirmed-failing
- Per-user funnel: of 10 people with ≥1 `recording_started`, only 3 have any completion event (`recording_chunked_upload_completed` or `recording_upload_completed`) and 0 have any failure event (`recording_upload_failed`/`recording_chunk_store_failed` — both silent, see gaps below). **7/10 users have no completion or failure signal at all** — the pipeline's outcome for most attempts is invisible in PostHog, not confirmed successful.
- `recording_saved` (42 events/14u) fires far more than `recording_started` (34/10) or completion events combined — it is NOT gated on upload completion, do not use it as a success proxy.
- Backend server-side processing events (`recording_processing_started/completed/failed` in `app/tasks/session_recording.py`) have **never fired to PostHog, ever** (checked 365d) — the server-side half of the pipeline is completely dark from a PostHog standpoint. Use Postgres (`database-administrator`) for upload_chunks/session-recording completion truth instead.

## Instrumentation gap lists (as of 2026-08-10, cross-referenced against code)
- **(a) Never fired since ingest start (365d check, 0 rows)**: notification_nudge_tapped/dismissed, notification_banner_dismissed, subscription_restore_started/completed/failed, journal_note_created, summary_viewed, report_generated (client) + report_exported (backend), onboarding_legal_gate_abandoned, recording_chunk_upload_failed, voice_transcription_failed, workspace_section_expanded, workspace_item_opened, entire Notes taxonomy (note_editor_opened/saved/discarded/deleted), entire text-Chat taxonomy (chat_opened/message_sent/message_failed), journey_viewed/journey_day_opened, summary_record_opened/shared, achievement_unlocked, streak_screen_viewed, analytics_screen_opened, bio_viewed, health_check_dismissed, monthly_audit_generated/regenerated, prep_card_auto_generated, level_up, recording_chunk_store_failed, weekly_summary_generated/regenerated, recording_processing_started/completed/failed, account_deletion_cancelled, $exception (PostHog error-tracking autocapture is not configured at all).
- **(b) Went silent in last 14d (fired before, nothing since)**: therapy_schedule_updated, timeline_generate_now, inapp_insight.generated, goal_status_changed, subscription_purchase_completed, subscription_receipt_received, notification_master_toggled, promo_code_applied, notification_interest_toggled, inapp_insight.dismissed, notification_banner_tapped, onboarding_lead_source_other_text, one_time_purchase_completed, subscription_verification_failed, one_time_receipt_received, recording_upload_completed (expected — superseded by recording_chunked_upload_completed), $feature_flag_called, recording_upload_failed, notification_intensity_changed, notification_preference_changed, symptom_suggestion_accepted/dismissed.
- **(c) Flowing but suspiciously thin**: realization_detected (1 event, ever), voice_transcription_started/completed (8/3u vs 10 recording-pipeline users), reflect_session_ended (2/2u vs reflect_session_started 24/16u — most started sessions never show an "ended"), client_error (17/6u across the whole app in 14d — implausibly low for a mobile app this size).
- No event exists anywhere for mic-permission prompts (distinct from push-notification permission) or for "too short"/empty-recording outcomes.

## Reusable pattern: per-user funnel-presence query (cheap alternative to windowFunnel for "did X ever happen" per person)
```sql
SELECT
  countIf(has_started) AS n_started,
  countIf(has_started AND has_completed) AS n_completed,
  countIf(has_started AND has_failed) AS n_failed
FROM (
  SELECT person_id,
    countIf(event = 'A') > 0 AS has_started,
    countIf(event IN ('B','C')) > 0 AS has_completed,
    countIf(event IN ('D','E')) > 0 AS has_failed
  FROM events WHERE event IN ('A','B','C','D','E') AND timestamp > now() - INTERVAL 14 DAY
  GROUP BY person_id
)
```

## Reusable pattern: current-vs-prior-window trend in one query (avoids 2 round trips)
```sql
SELECT event,
  countIf(timestamp > now() - INTERVAL 14 DAY) AS c_curr,
  count(DISTINCT if(timestamp > now() - INTERVAL 14 DAY, person_id, NULL)) AS u_curr,
  countIf(timestamp <= now() - INTERVAL 14 DAY AND timestamp > now() - INTERVAL 28 DAY) AS c_prev,
  count(DISTINCT if(timestamp <= now() - INTERVAL 14 DAY AND timestamp > now() - INTERVAL 28 DAY, person_id, NULL)) AS u_prev
FROM events WHERE event IN (...) AND timestamp > now() - INTERVAL 28 DAY
GROUP BY event ORDER BY c_curr DESC
```
`count(DISTINCT if(cond, person_id, NULL))` works fine in HogQL/ClickHouse — NULLs are excluded from DISTINCT automatically.

## Reusable pattern: concentration/skew without exposing identifiers
```sql
-- top-N sum only, no person_id in final output
SELECT sum(cnt) AS topN_sum FROM (
  SELECT person_id, count() AS cnt FROM events WHERE event='X' AND timestamp > now() - INTERVAL 14 DAY
  GROUP BY person_id ORDER BY cnt DESC LIMIT 5
)
-- per-event single-user-domination scan across ALL events at once
SELECT event, sum(cnt) AS total, max(cnt) AS top1_cnt
FROM (SELECT event, person_id, count() AS cnt FROM events WHERE timestamp > now() - INTERVAL 14 DAY GROUP BY event, person_id)
GROUP BY event HAVING total >= 10 AND (max(cnt)*1.0/sum(cnt)) > 0.6
ORDER BY (max(cnt)*1.0/sum(cnt)) DESC
```

## Bot/test traffic baseline (14d, 2026-08-10)
- Raw `$os` split over ALL events includes Linux 66u / Windows 6u / Mac OS X 5u — these are the marketing/web site, not the mobile app. Restricting to mobile-only events (`tab_switched`, `workspace_opened`, `$screen`) drops it to Android 76 / iOS 15 / iPadOS 1. Always restrict to app-specific events before reading an OS split as "app users."
- `$is_emulator`/`$is_testflight` flags exist and work: 3 users each out of 127 total in 14d — small, identifiable internal-test slice.

## C1 backend-instrumentation re-verification (2026-08-10, all-time since ingest 2026-04-22)
- Re-confirms zero all-time volume (not just 14d silence) for: weekly_summary_generated, monthly_audit_generated, report_generated, report_exported, recording_processing_started/completed/failed, recording_chunk_store_failed, prep_card_auto_generated — all match the (a) never-fired list above, now verified with a full-history grouped query rather than a 365d window.
- `inapp_insight.generated` precise history: 4 events/3 users total, 2026-06-29 to 2026-07-23, then genuinely dead (not just quiet in the last 14d). `inapp_insight.shown` ran in parallel through the same weeks (both present 06-28, 07-12, 07-19) but kept growing after generated stopped (07-26: 3/3u, 08-02: 5/5u) — this is NOT a shown-depends-on-generated timing artifact; the two code paths are decoupled, and generated specifically broke/was removed ~2026-07-23. Full detail: `analytics-reports/raw/2026-08-10-dead-instrumentation-c1-backend-events.md`.
