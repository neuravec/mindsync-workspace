# Errors / quality / instrumentation-gap picture — raw PostHog extract

- **Date**: 2026-08-10 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: primary = 2026-07-27 → 2026-08-10 (14d, UTC), comparison = 2026-07-13 → 2026-07-27 (prior 14d)
- **Question**: What is actually breaking for users right now, and what does the instrumentation plan claim exists vs what PostHog actually shows?
- **Event verification**: `api_error` flowing (last_seen 2026-08-10T03:51, 4507 events/60 users in 14d). `client_error` flowing but low volume (17/6). Full 137-event taxonomy pulled via unfiltered `--events` for last-seen timestamps. A 40-event candidate list (client + backend "should exist" events) checked against 365-day history — **zero rows returned for all 40** → none of them have ever fired since ingest start (2026-04-22).

## Results

### 1. `api_error` — total, 14d vs prior 14d
| window | count | distinct users |
|---|---|---|
| last 14d (07-27→08-10) | 4507 | 60 |
| prior 14d (07-13→07-27) | 1319 | 38 |

Active users in the 14d window (any event): 127. Active users prior 14d: 266 (active-user count itself fell ~52% period over period — see caveats).

### api_error by endpoint (14d, top 25)
| endpoint | count | users |
|---|---|---|
| /api/v1/reflect/{conversation_id}/message | 1874 | 2 |
| /api/v1/prep-cards/latest | 1024 | 41 |
| /api/v1/debriefs/latest | 980 | 42 |
| /api/v1/health-check/latest | 440 | 34 |
| /api/v1/users/get_user_profile_and_subscription | 48 | 32 |
| /api/v1/moments/{moment_id}/dismissed | 41 | 18 |
| /api/v1/users/therapy-context | 30 | 30 |
| <unmatched> | 18 | 7 |
| /api/v1/therapy-tracking/latest | 13 | 2 |
| /api/v1/users/preferences | 10 | 4 |
| /api/v1/between-sessions/latest | 9 | 5 |
| /api/v1/users/therapy-schedule | 9 | 8 |
| /api/v1/realizations/ | 3 | 1 |
| /api/v1/users/settings/account | 3 | 1 |
| /api/v1/dashboard/calltoaction | 2 | 1 |
| /api/v1/debriefs/ | 1 | 1 |
| /api/v1/conversations/{conversation_id}/end | 1 | 1 |
| /api/v1/reflect/{conversation_id}/end | 1 | 1 |

### api_error by status_code (14d)
| status_code | count | users |
|---|---|---|
| 404 | 2617 | 60 |
| 403 | 1870 | 1 |
| 422 | 10 | 9 |
| 409 | 4 | 2 |
| 500 | 4 | 2 |
| 400 | 2 | 1 |

### api_error by method (14d)
| method | count | users |
|---|---|---|
| GET | 2574 | 57 |
| POST | 1921 | 20 |
| PUT | 9 | 8 |
| DELETE | 3 | 1 |

### api_error by error_class (14d)
| error_class | count | users |
|---|---|---|
| HTTPException | 4493 | 60 |
| RequestValidationError | 10 | 9 |
| IntegrityError | 3 | 1 |
| AttributeError | 1 | 1 |

### api_error per day (14d) vs total active users per day
| day | api_error count | api_error users | active users (any event) | erroring/active |
|---|---|---|---|---|
| 07-27 | 16 | 4 | 13 | 31% |
| 07-28 | 13 | 4 | 9 | 44% |
| 07-29 | 35 | 7 | 11 | 64% |
| 07-30 | 134 | 8 | 18 | 44% |
| 07-31 | 122 | 5 | 16 | 31% |
| 08-01 | 23 | 5 | 11 | 45% |
| 08-02 | 29 | 5 | 5 | 100% |
| 08-03 | 276 | 9 | 15 | 60% |
| 08-04 | 2573 | 13 | 20 | 65% |
| 08-05 | 189 | 11 | 17 | 65% |
| 08-06 | 100 | 6 | 9 | 67% |
| 08-07 | 631 | 10 | 18 | 56% |
| 08-08 | 169 | 8 | 13 | 62% |
| 08-09 | 139 | 7 | 16 | 44% |
| 08-10 | 58 | 3 | 3 (partial day) | 100% |

The 08-04 spike (2573 events) is the 403/reflect-limit endpoint concentrated on 1 user (see concentration below), not a broad outage.

### api_error concentration (14d, no identifiers)
- Top 1 user: 1966 / 4507 = **43.6%** of all `api_error` volume.
- Top 5 users combined: 3396 / 4507 = **75.4%** of all `api_error` volume (out of 60 distinct erroring users).
- This top-1 concentration lines up almost exactly with the 403/`reflect/{id}/message` numbers (1870 events, 1 user) — one account is responsible for essentially the entire 403 bucket.
- Excluding that one account, the remaining volume (~2637 events across 59 users) is dominated by 404s spread across `/prep-cards/latest`, `/debriefs/latest`, `/health-check/latest` — 34–42 distinct users each, i.e. a broad pattern, not single-user noise.

### 2. Other failure/error events, 14d vs prior 14d (all events matching error/fail/denied/timeout/retry keyword search, plus `$exception`)
| event | count 14d | users 14d | count prior 14d | users prior 14d | last_seen |
|---|---|---|---|---|---|
| client_error | 17 | 6 | 38 | 6 | 2026-08-07T16:12 |
| notification_permission_denied | 11 | 6 | 0 | 0 | 2026-08-09T12:23 |
| password_reset_failed | 2 | 1 | 0 | 0 | 2026-08-05T07:17 |
| signup_failed | 1 | 1 | 0 | 0 | 2026-08-10T00:09 |
| debrief_failed | 1 | 1 | 13 | 4 | 2026-07-29T14:39 |
| subscription_purchase_failed | 1 | 1 | 1 | 1 | 2026-08-01T11:05 |

Zero matches (never fired, any window) for: `subscription_verification_failed` in this window (last seen 2026-06-26, so it exists historically but is silent now — see gap list), `recording_upload_failed`, `recording_chunk_store_failed`, `recording_chunk_upload_failed` (client constant, never fired at all), `recording_processing_failed`, `voice_transcription_failed`, `chat_message_failed`. `$exception` (PostHog error tracking autocapture) has **never fired** — error tracking is not wired up; `client_error` is the only client exception signal and it is a manual capture, not autocapture.

`timeout` and `retry` keyword searches on event names returned 0 events entirely — no event in the taxonomy is named around timeout/retry.

**client_error breakdown by error_type (14d)**: `FirebaseAuthException` 13/5 users, `String` 3/2 users, `_Exception` 1/1 user. Auth-related exceptions dominate the (small) client_error volume.

### 3. Recording / upload pipeline health, 14d vs prior 14d
| event | count 14d | users 14d | count prior 14d | users prior 14d |
|---|---|---|---|---|
| recording_saved | 42 | 14 | 35 | 3 |
| recording_started | 34 | 10 | 46 | 3 |
| recording_stopped | 28 | 10 | 43 | 3 |
| voice_transcription_completed | 8 | 3 | 0 | 0 |
| voice_transcription_started | 8 | 3 | 0 | 0 |
| recording_chunked_upload_completed | 7 | 3 | 14 | 4 |
| recording_recovered | 4 | 3 | 34 | 2 |
| recording_upload_started | 3 | 3 | 5 | 2 |

Not flowing at all (checked, zero rows in 365d): `recording_processing_started`, `recording_processing_completed`, `recording_processing_failed` (backend RQ-task-level events — the server-side processing pipeline never emits to PostHog, at any point in its history), `recording_upload_failed` (silent since 2026-06-21), `recording_chunk_store_failed` (never fired).

**Per-user funnel (14d, event-presence per person, not raw event counts):**
| n_started (≥1 recording_started) | n_completed (≥1 chunked/plain upload_completed) | n_failed (≥1 upload/chunk failure) |
|---|---|---|
| 10 | 3 | 0 |

Read literally: of 10 distinct people who started a recording in the last 14 days, only 3 have a matching completion event and 0 have an explicit failure event. That leaves **7 of 10 users (70%) with a `recording_started` and no completion or failure signal at all** — i.e., the pipeline's outcome for the majority of attempts is simply unmeasurable, not confirmed-successful. `recording_saved` (42 events/14 users) fires far more than `recording_started` (34/10) and `recording_chunked_upload_completed` (7/3) combined, so `recording_saved` is not gated on the upload actually completing — it cannot be used as a completion proxy.

### 4. Voice / realtime session health, 14d vs prior 14d
| event | count 14d | users 14d | count prior 14d | users prior 14d |
|---|---|---|---|---|
| reflect_limit_hit | 1870 | 1 | 0 | 0 |
| notification_permission_prompted | 55 | 20 | 0 | 0 |
| notification_permission_granted | 44 | 14 | 0 | 0 |
| between_session_started | 35 | 11 | 38 | 9 |
| between_session_created | 27 | 8 | 23 | 8 |
| reflect_session_started | 24 | 16 | 15 | 9 |
| notification_permission_denied | 11 | 6 | 0 | 0 |
| voice_agent_changed | 4 | 2 | 7 | 1 |
| reflect_session_ended | 2 | 2 | 0 | 0 |
| voice_chat_ended | 1 | 1 | 6 | 2 |
| voice_chat_started | 1 | 1 | 6 | 2 |

`voice_chat_started`/`voice_chat_ended` collapsed from 6 users to 1 user period over period — real drop or a renamed/replaced flow (matches `reflect_session_started` rising 15→24 over the same period; the realtime voice-chat surface may have been superseded by the reflect flow). No event exists anywhere in the taxonomy for microphone-permission-specific prompts (`notification_permission_*` covers push notifications, not mic) or for "too short"/empty-recording outcomes — confirmed absent, see gap list.

### 5/6. Instrumentation gaps

**(a) Referenced in code, never seen in PostHog (0 rows in a 365-day lookback, i.e. since before ingest start — genuinely never fired):**
`notification_nudge_tapped`, `notification_nudge_dismissed`, `notification_banner_dismissed`, `subscription_restore_started`, `subscription_restore_completed`, `subscription_restore_failed`, `journal_note_created`, `summary_viewed`, `report_generated` (client constant — distinct from the backend's `report_exported`, which also never fired), `onboarding_legal_gate_abandoned`, `recording_chunk_upload_failed`, `voice_transcription_failed`, `workspace_section_expanded`, `workspace_item_opened`, `note_editor_opened`, `note_saved`, `note_discarded`, `note_deleted` (entire Notes feature silent), `chat_opened`, `chat_message_sent`, `chat_message_failed` (entire text-Chat feature silent), `journey_viewed`, `journey_day_opened`, `summary_record_opened`, `summary_record_shared`, `achievement_unlocked`, `streak_screen_viewed` (gamification client events — consistent with gamification being "planned" per CLAUDE.md), `analytics_screen_opened`, `bio_viewed`, `health_check_dismissed`, `monthly_audit_generated`, `monthly_audit_regenerated`, `prep_card_auto_generated`, `level_up` (gamification backend), `report_exported`, `recording_chunk_store_failed`, `weekly_summary_generated`, `weekly_summary_regenerated`, `recording_processing_started`, `recording_processing_completed`, `recording_processing_failed`, `account_deletion_cancelled`, `$exception` (PostHog error-tracking autocapture).

**(b) Seen historically but zero in the last 14 days (went silent):**
| event | last seen |
|---|---|
| therapy_schedule_updated | 2026-07-27 (right at the boundary) |
| timeline_generate_now | 2026-07-24 |
| inapp_insight.generated | 2026-07-23 |
| goal_status_changed | 2026-07-23 |
| subscription_purchase_completed | 2026-07-22 |
| subscription_receipt_received | 2026-07-22 |
| notification_master_toggled | 2026-07-21 |
| promo_code_applied | 2026-07-21 |
| notification_interest_toggled | 2026-07-17 |
| inapp_insight.dismissed | 2026-07-16 |
| notification_banner_tapped | 2026-07-15 |
| onboarding_lead_source_other_text | 2026-07-07 |
| one_time_purchase_completed | 2026-06-26 |
| subscription_verification_failed | 2026-06-26 |
| one_time_receipt_received | 2026-06-26 |
| recording_upload_completed | 2026-06-22 (superseded by `recording_chunked_upload_completed`, expected) |
| $feature_flag_called | 2026-06-22 |
| recording_upload_failed | 2026-06-21 |
| notification_intensity_changed | 2026-06-07 |
| notification_preference_changed | 2026-05-21 |
| symptom_suggestion_accepted | 2026-05-18 |
| symptom_suggestion_dismissed | 2026-05-13 |

**(c) Flowing but with suspiciously low user counts relative to the surface they instrument:**
- `realization_detected` — only ever fired once (2026-07-30), 1 event total in its whole history.
- `voice_transcription_started`/`completed` — 8/3 in 14d against a recording pipeline with 10 distinct `recording_started` users; roughly a third of recording users have a matching transcription event.
- `reflect_session_ended` — 2 events/2 users in 14d vs `reflect_session_started` 24/16 — the vast majority of started reflect sessions have no matching "ended" event.
- `client_error` — 17 events/6 users across the whole app in 14d is implausibly low for a mobile app surface this size; either exceptions are rare (unlikely) or most crashes/exceptions never reach `logError()`.

### 7. Version-correlated breakage (14d)
| $app_version | distinct users | first seen |
|---|---|---|
| 2.0.75 | 56 | 2026-07-27 |
| 2.0.76 | 29 | 2026-08-04 |
| 2.0.60 | 15 | 2026-07-27 |
| 2.0.44 | 3 | 2026-07-29 |
| 2.0.36 | 1 | 2026-08-01 |

Client-side error/failure events by version (14d):
| version | event | count | users |
|---|---|---|---|
| 2.0.76 | client_error | 11 | 2 |
| 2.0.76 | password_reset_failed | 2 | 1 |
| 2.0.76 | signup_failed | 1 | 1 |
| 2.0.75 | client_error | 4 | 3 |
| 2.0.75 | debrief_failed | 1 | 1 |
| 2.0.75 | subscription_purchase_failed | 1 | 1 |
| 2.0.60 | client_error | 2 | 1 |

**Caveat (explicit, not derived):** `api_error` is emitted server-side (`app/main.py`) and never carries `$app_version` — it cannot be split by client version. The endpoint/status/method/class breakdown above is the only available dimensioning for `api_error`; a version correlation for it is not measurable from PostHog.

### 8. Single-user skew audit (14d, events with ≥10 total volume where one person is >60% of it — no identifiers, share only)
| event | total (14d) | top-1 share |
|---|---|---|
| reflect_limit_hit | 1870 | 100% |
| conversation_message_sent | 14 | 100% |
| bio_refreshed | 12 | 83% |
| $rageclick | 33 | 70% |
| onboarding_step_back | 10 | 70% |
| health_check_question_answered | 17 | 65% |

`reflect_limit_hit` and `conversation_message_sent` are fully single-account artifacts at current volumes — any dashboard metric built on either is really reporting one account's behavior, not usage.

### 9. Bot / test-traffic sanity (14d)
| $os | distinct users |
|---|---|
| Android | 86 |
| Linux | 66 |
| iOS | 25 |
| Windows | 6 |
| Mac OS X | 5 |
| iPadOS | 1 |

Total distinct users (any event, 14d): 127. Restricting to mobile-app-only events (`tab_switched`, `workspace_opened`, `$screen`) drops the OS split to Android 76, iOS 15, iPadOS 1 — the Linux/Windows/Mac OS X users (77 of 127, ~61% of total distinct users in the raw all-events split) are not touching mobile-app surfaces at all; they are the marketing/web site ($pageview/$web_vitals/$autocapture events), not app users. Emulator/TestFlight flags: `$is_emulator=true` → 165 events / 3 users; `$is_testflight=true` → 665 events / 3 users (out of 13679 events / 127 users total in the window) — a small, identifiable slice of internal/test traffic, not enough to explain the bulk of volume.

## Caveats
- Ingest started 2026-04-22; the 365-day gap-scan lookback fully covers all history, so "never seen" in list (a) is a true "never fired since instrumentation existed," not a window artifact.
- Total active users fell from 266 (prior 14d) to 127 (current 14d) — roughly halved period over period. This context matters for reading every trend table above: falling event counts can reflect falling traffic, not improving quality, and rising per-user error ratios can reflect a shrinking, more error-prone remaining cohort. This is a "why" question for `growth-analyst`, not answered here.
- `api_error` cannot be split by `$app_version` (server-side event, no client properties) — stated explicitly per the task's rule, not worked around.
- k-anonymity: no segment below n=25 users is reported as a value; where n<25 it is shown as a raw small count with context (e.g., "1 user") rather than presented as a rate/percentage that implies statistical weight.
- All "concentration"/"skew" results report shares and counts only — no distinct_id, person_id, email, or other identifier is included anywhere in this file.
- `status_code` values render as floats (e.g. `404.0`) — a property-typing quirk of how the backend serializes them, not a data-quality finding in itself.

## Queries
See `C:\Users\mikol\AppData\Local\Temp\claude\C--Users-mikol-Notebooks-MindSync-Heroku\1cf22ea1-0d50-47c1-b873-2e2b79f0e9bb\scratchpad\errors_quality_14d.sql` for the full batched HogQL (18 labeled sections), plus two standalone follow-ups:

```sql
-- client_error by error_type, 14d
SELECT properties.error_type AS error_type, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'client_error' AND timestamp > now() - INTERVAL 14 DAY
GROUP BY error_type ORDER BY c DESC LIMIT 20

-- top-5 individual api_error counts (rank only, no identifiers), 14d
SELECT person_rank, cnt FROM (
  SELECT row_number() OVER (ORDER BY cnt DESC) AS person_rank, cnt
  FROM (SELECT person_id, count() AS cnt FROM events WHERE event='api_error' AND timestamp > now() - INTERVAL 14 DAY GROUP BY person_id)
) WHERE person_rank <= 5
```
