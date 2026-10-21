---
name: gpt-realtime-2 migration (2026-05-12)
description: Switched GPT_AGENT_MODEL from gpt-realtime-1.5 to gpt-realtime-2 (Scenario A). Drop-in, cost-neutral. Transcription untouched.
type: project
originSessionId: e0a21b28-7faf-451d-b706-7d47cd73a071
---
OpenAI released `gpt-realtime-2` on 2026-05-08. Migrated `GPT_AGENT_MODEL` from `gpt-realtime-1.5` → `gpt-realtime-2` on 2026-05-12.

**Why:** Drop-in replacement — same `/v1/realtime/client_secrets` endpoint, same body shape. Audio I/O pricing IDENTICAL ($32/M in, $64/M out). Only text output rises $16 → $24/M but text output in voice flows is tiny — net cost change <1%. Gains: GPT-5-class reasoning, 128K context (vs 32K), parallel tool calls, +15.2% Big Bench Audio.

**How to apply:** This decision was Scenario A (cost-neutral upgrade only). PR-2 (`gpt-4o-mini-transcribe` → `gpt-realtime-whisper`) was REJECTED for global use because it's 5.67× more expensive ($0.003 → $0.017/min). If the question of live captions / better in-session STT comes up again, propose it as a premium-only feature, NOT a global swap. The translation model `gpt-realtime-translate` ($0.034/min) is a separate new use-case, not an upgrade — needs own UX/product decision.

**Files changed:**
- `MindSync/.env` line 23 (local — Heroku config-var must be set separately)
- `MindSync/app/tests/conftest.py:36`, `test_audio_v2_config.py:77`, `test_voice_fixes.py:775,829`
- `MindSync/docs/openai-model-migration.md` (new section appended)
- `Heroku/TOKEN_USAGE_TRACKING.md` (pricing table)
- `mindsync-frontend/mindsync_app/lib/screens/audio_chat/cubit/audio_chat_cubit.dart:41` (fallback default — overwritten by `initialize()` arg in practice)
- NEW Alembic migration `ff6g7h8i9j0k_add_gpt_realtime_2_pricing.py`, down_revision=`ee5f6g7h8i9j`. Inserts ModelPricing row for `gpt-realtime-2`/`REALTIME` with audio in=$32, audio out=$64, cached=$0.40. Historical `gpt-realtime-1.5` pricing row INTENTIONALLY KEPT so old TokenUsageLog rows resolve cost correctly.

**Deployment requirements:**
1. `git push heroku <branch>:main` (or via Codemagic) — deploys code + auto-runs `alembic upgrade head`.
2. `heroku config:set GPT_AGENT_MODEL=gpt-realtime-2` — CRITICAL, else realtime sessions still use 1.5.
3. Optional: `heroku config:set GPT_AGENT_MODEL=gpt-realtime-2 --app <staging-app>` first.
4. Optional tuning: if cost spikes (monitor in PostHog or `token_usage_log`), check `AUDIO_V2_MAX_OUTPUT_TOKENS` (currently 4096) — gpt-realtime-2 supports up to 32K but we should NOT raise unless needed.

**Known anti-patterns to avoid:**
- Do NOT set `reasoning_effort` higher than `low` (default) without a benchmark — `high`/`very_high` can multiply token output 2-5×.
- Do NOT delete the gpt-realtime-1.5 ModelPricing row — historical TokenUsageLog rows need it.
- Do NOT also swap `gpt-4o-mini-transcribe` (in `openai_audio_service.py:270` and 4 Flutter cubits) to `gpt-realtime-whisper` without an explicit cost decision — it's 5.67× more expensive.
