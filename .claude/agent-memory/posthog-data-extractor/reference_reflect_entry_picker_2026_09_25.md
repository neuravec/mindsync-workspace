---
name: reference-reflect-entry-picker-2026-09-25
description: Reflect entry mode-picker (shipped 2026-09-18) post-deploy usage/funnel/error pull, partial rollout state, and the single-user skew found on 2026-09-17
metadata:
  type: project
---

Pulled 2026-09-25 for the Reflect entry redesign (full-screen voice/text picker + topic sheet, shipped BE v550 / FE dev 81773ba, 2026-09-18). Full raw extract: `analytics-reports/raw/2026-09-25-reflect-mode-picker-post-deploy.md`.

**New picker events** (all `$lib='posthog-flutter'`, first seen 2026-09-18, confirming clean rollout timing): `reflect_mode_choice_shown`, `reflect_mode_selected` (property `mode`=voice/text), `reflect_entry_sources_shown`/`_served`, `reflect_entry_topic_selected`, `reflect_entry_dismissed`, `reflect_new_thread_tapped`, `reflect_thread_resumed`, `reflect_opening_question_shown`, `reflect_voice_locked_tapped`. All very thin (n=1-9 users) as of 2026-09-25 — partial TestFlight/dev-branch rollout, not yet on Store production.

**Build adoption**: picker-carrying builds are `$app_version` 2.0.91+ (first seen 2026-09-18). ~46 distinct users on 2.0.91-2.0.94 in 30d as of 2026-09-25, out of ~127-150 total 30d active users — roughly a third have the feature at all. Any usage-trend read must account for this: most users literally cannot see the new picker yet.

**New `end_reason` value `voice_interrupted` (per spec) has NOT appeared** in `reflect_ui_session_ended.end_reason` in the 2026-08-28→09-24 window. Observed values: `backgrounded`, `navigated_away`, `thread_switched`, `limit_reached`, `user_ended`. Could be low-volume-not-yet-hit or a wiring gap — flag to `flutter-mobile`/`backend-api`, don't assume either way from PostHog alone.

**Single-user skew, new instance**: person `a459f002-b841-5482-a0ba-0d4c650a2362` (Windows, `$app_version` NULL — a backend/desktop/test client, not a real phone) generated 112 of 115 `reflect_session_started` events on 2026-09-17 alone (one day before launch), nowhere else in a 4-week window. Always run a same-day person_id concentration check (`GROUP BY person_id ORDER BY count() DESC`) before trusting any single-day spike in a small-N event.

**Before/after read (skew excluded, 7d windows around 2026-09-18)**: Reflect sessions-started went 9→27 (weekday-aligned earlier week was 14) with the SAME 7 distinct users both before/after — reads as more sessions per user, not more users, on the ~third of the base that has the feature. Messages sent 13→19, also same 4 users both weeks. n is single-digit throughout — early positive signal at best, not proof. `paywall_trigger_feature` values seen in this window (`drawer_menu`, `premium_gate_session_recording`, `premium_gate_reflect_messages`) do NOT include a value distinguishing the new reflect-voice-lock paywall trigger — the voice-lock→paywall chain is not traceable via `trigger_feature` yet.

**Errors**: no endpoint/status pattern change coincident with 09-18 in reflect/conversation/audio/voice `api_error`s — all rows n=1 user both before and after, too thin to call a regression either way. `$exception` and `client_error` show steady low background rate before and after, no spike at the deploy boundary.

**Reconfirms two existing memory facts** in this fresh pull: (1) `reflect_session_started`/`reflect_message_sent`/`reflect_session_ended` are `$lib='posthog-python'` (backend), not `posthog-flutter` — same lib trap as before, still active, still easy to zero out by accident. (2) legacy `conversation_started`/`_message_sent`/`_ended` are confirmed fully dead (last event 2026-08-11), fully superseded by `reflect_*`.
