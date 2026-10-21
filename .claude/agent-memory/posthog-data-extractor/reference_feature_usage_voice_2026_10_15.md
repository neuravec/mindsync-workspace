---
name: reference_feature_usage_voice_2026_10_15
description: 2026-10-15 30d feature-reach baselines (257 active), voice realtime path quality, GPT-Live-1 engine events (first seen 10-15, 1 TestFlight tester), moment.opened join gap, to-do has no events
metadata:
  type: reference
---

Baselines 30d to 2026-10-15 (active = flutter, no TF/emulator/bot models): 257 active (Android 234, iOS 19, iPadOS 4); last15 161 vs prior15 121.
Reach: timeline 62, habit (any) 52 but real use (create/toggle) ~10-12 (habit_tracker_viewed = load-like, 55), workspace 43, bio 40, debrief 23, reflect text 22 (9->19 doubling), picker 21, threads 20, voice realtime 16, prep 13, summaries 13, voice note 10, session recording 8, Your Session 6. Dead (<2%): character sheet (new 10-14), orca memory, today card, to-do.

Voice: voice_chat_ended p50 127s / p90 499s (51 sessions, 14 users); ~5% fail (webrtc_failure connect, ice_failed dropped); ended > started (51 vs 47) = instrumentation mismatch. No "connected"/"first utterance" event for regular voice; only first_conversation_ended has user_turns.

GPT-Live-1: `voice_engine_selected` + `voice_live_session_ended` are posthog-python; `voice_engine_changed` + `voice_engine` prop on voice_chat_* are client. First seen 2026-10-15, one TestFlight person only. The default TF filter hides ALL of it, query unfiltered.

Gotchas: moment.sent/opened join needs toString(properties.moment_id) (raw compare -> cannot_parse_number); only 10/62 opens match. To-do = only `workspace_item_action` section_name=todo. Heavy single-user skew on bio_viewed, timeline_viewed, workspace_opened, therapy_schedule_updated, stat_opened. Extract: analytics-reports/raw/2026-10-15-feature-usage-voice.md. See [[reference_moment_notification_family_and_2026_09_12_baselines]].
