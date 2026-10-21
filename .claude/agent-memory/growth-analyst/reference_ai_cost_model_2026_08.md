---
name: ai-cost-model-2026-08
description: What token_usage_log can and cannot cost (realtime voice is architecturally invisible), feature-label traps, and the 2026-08 AI cost baselines
metadata:
  type: reference
---

# AI cost truth + traps (verified 2026-08-10, task B7)

## Baselines (Postgres `token_usage_log`, precomputed `cost_usd` column – use it directly)
- **Total AI spend last 30d: $117.30** (133,988 rows, 174 distinct users). Table spans 2026-04-01 →.
- Dominant model `gpt-5.4-mini`: $144.50 / 60d over 276 users = **$0.524 per user per 60d** (text baseline).
- **`SYSTEM` = 93% of 60d spend ($134.23 of $144.90), with ZERO attributed users.** Background jobs
  dwarf every product surface combined and have never been audited. Biggest cost-saving lead we have.
- Next largest features (60d): REFLECT $5.35 · PERSONAL_BIO $0.83 · CHART_EXPLANATION $0.80 ·
  RECORDING $0.79 · PREP_CARD $0.64. REALTIME_VOICE is dead last at $0.000376.

## TRAP 1: realtime voice cost does not exist in our data
`openai_audio_service.py:380-394` writes a **placeholder** row (`total_tokens=0, cost_usd=0,
is_estimate=True, operation='create_realtime_session'`) and its comment claims the client reports
per-turn tokens later. **The Flutter client contains no such call** – WebRTC goes client →
`api.openai.com/v1/realtime/calls` on an ephemeral key, so audio tokens never reach our backend.
All 114 realtime rows all-time have zero tokens, zero cost, and **`user_id = NULL` (100%)**.
=> "$0 realtime cost" means UNMEASURED, never FREE. Never report it as cheap.

**Estimate instead**, from `voice_chat_ended.duration_seconds` (PostHog, 100% coverage) ×
published rates. Benchmark: gpt-realtime-2.1 = $32/1M audio-in, $64/1M audio-out; typical agent
**$0.06–$0.11/min with prompt caching**, $0.18–$0.46/min without
(hackernoon.com/openai-realtime-api-pricing-in-2026-real-world-data-from-4000-measured-sessions).
Bottom-up cross-check (600 tok/min in, ~40% assistant talk at 1200 tok/min out) ≈ $0.05/min – same order.

## TRAP 2: `feature='REALTIME_VOICE'` over-attributes text traffic
`voice_director.run_pipeline` is called from BOTH `POST /{id}/audio/user_message_add` (voice) AND
`POST /{id}/message` (**text** Reflect) – `reflect.py:954` and `:525`. So REALTIME_VOICE showed
684 rows / 28 users in 60d while voice chat had 1–2 users. Fix pending with `data-analytics`.

## TRAP 3: missing `model_pricing` rows silently cost $0
`whisper-1` (206 real rows) and `gpt-realtime-mini` have **no pricing row**, so their cost computes
as $0.000000 – understated, not free. `gpt-4o-mini-transcribe` does have one ($0.0030/min) and is correct.
Realtime pricing rows DO exist (`gpt-realtime-1.5` $10/$20; `gpt-realtime-2` $32/$64 per 1M) and are
ready the moment real token counts start flowing – the gap is instrumentation, not pricing.

## Useful cut
```sql
SELECT feature, COUNT(*), COUNT(DISTINCT user_id), SUM(cost_usd)
FROM token_usage_log WHERE created_at >= now() - interval '60 days'
GROUP BY 1 ORDER BY SUM(cost_usd) DESC;
```
Prod enums are UPPERCASE (drift) – compare with uppercase literals.

See also [[voice-chat-b7-verdict]], [[premium-gated-features-denominator]].
