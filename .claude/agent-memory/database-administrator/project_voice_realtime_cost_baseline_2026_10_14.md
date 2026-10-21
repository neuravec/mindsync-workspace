---
name: voice-realtime-cost-baseline-2026-10-14
description: Realtime voice tokens/cost are NOT in prod DB (mint rows are 0 tokens, $0, user_id NULL); voice minutes must be derived from director_embed_user_text (Reflect) and messages (first conv); 30d ~356 min
metadata:
  type: project
---

Realtime voice cost is unmeasurable from Postgres as of 2026-10-14 (report `db-reports/2026-10-14-voice-realtime-cost-baseline.md`).
- `token_usage_log` REALTIME rows = one per minted key (`create_realtime_session`), tokens 0, cost 0, user_id NULL. Legacy `/v1/realtime/sessions` mints are not logged at all. Client sums `response.done` usage but sends it only to PostHog `first_conversation_ended`.
- `model_pricing` has no row for `gpt-realtime-mini` (used Aug to 2026-10-05); stored rates are audio-only.
- Best duration proxies: ordinary Reflect voice = sessionize `operation='director_embed_user_text'` per user (gap 10 min; director skips first conversation); first conversation = messages in `entry_origin='onboarding_first_conversation'` threads. `conversations.modality` only exists since 2026-09-18. Journal voice durations unmeasurable (only `embed_voice_session_seed` opens).
- Baseline: 30d Reflect 67 sessions/14 users/277 min, first conv 19/10/79 min; 90d Reflect 144/31/943 min. All voice users are PREMIUM rows (trial or purchase).

**Why:** asked to compare against GPT-Live-1 per-minute pricing.
**How to apply:** do not re-hunt for realtime token columns; reuse these proxies, and point cost truth to the OpenAI usage dashboard or the fix (client reports usage to backend) handed to flutter-mobile + backend-api.
