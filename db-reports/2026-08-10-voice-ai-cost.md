# Voice Chat AI Cost vs Text — Production Postgres Pull

**Date:** 2026-08-10
**Requested by:** growth-analyst (task B7 — realtime voice chat investment decision)
**Access:** Heroku one-off dyno (`heroku run -a mindsync python`, run.4515 + run.5755, both stopped after capture)
**Scope:** `token_usage_log` / `model_pricing`, read-only aggregates, no PII, all segments ≥25 users unless noted

## Headline finding

**`token_usage_log` cannot answer "cost per active voice user" as asked — realtime voice audio cost is architecturally uninstrumented, and every `create_realtime_session` row has `user_id = NULL`.** This is not a query limitation; it is a real gap in what our backend can see. Details below, with the exact mechanism (confirmed against `app/services/openai_audio_service.py`).

---

## 1. Schema (live prod, verified via `information_schema.columns` — not assumed from models.py)

**`token_usage_log`**

| column | type | nullable |
|---|---|---|
| id | bigint | not null |
| created_at | timestamptz | not null |
| user_id | varchar (FK users, ON DELETE SET NULL) | nullable |
| feature | enum (UPPERCASE labels, e.g. `REALTIME_VOICE`, `REFLECT`, `SYSTEM`) | not null |
| operation | varchar(128) | not null |
| api_type | enum (`CHAT`, `CHAT_STRUCTURED`, `STT`, `EMBEDDING`, `REALTIME`, `TTS`) | not null |
| model | varchar(64) | not null |
| prompt_tokens | integer | nullable |
| completion_tokens | integer | nullable |
| total_tokens | integer | nullable |
| cached_tokens | integer | nullable |
| cost_usd | numeric(10,6) | **not null**, default 0 |
| is_estimate | boolean | not null |

No separate audio-token column exists — audio tokens, if ever logged, would have to ride in `prompt_tokens`/`completion_tokens`. In practice they never are (see §2). `cost_usd` is a **precomputed cost column already stored per row** — I used it directly rather than re-deriving from `model_pricing` (and cross-checked coverage in §7).

**`model_pricing`**

| column | type | nullable |
|---|---|---|
| id | integer | not null |
| model | varchar(64) | not null |
| api_type | enum | not null |
| prompt_price_per_1m | numeric(10,4) | nullable |
| completion_price_per_1m | numeric(10,4) | nullable |
| cached_prompt_price_per_1m | numeric(10,4) | nullable |
| price_per_minute | numeric(10,4) | nullable (used for STT) |
| price_per_1m_chars | numeric(10,4) | nullable (used for TTS) |
| effective_from | timestamptz | not null |
| effective_to | timestamptz | nullable |

Table overview: **188,406 rows**, spanning **2026-04-01 → 2026-08-10 (today)**. 0 rows with null `model`, 0 rows with null `cost_usd`.

## 2. Model inventory

**All time:**

| model | rows | first seen | last seen | sum tokens | sum cost_usd |
|---|---:|---|---|---:|---:|
| gpt-5.4-mini | 178,940 | 2026-04-01 | 2026-08-10 | 142,474,456 | **171.135243** |
| gpt-4o-mini-transcribe-2025-12-15 | 90 | 2026-04-03 | 2026-06-25 | n/a (no completion col used) | 0.669000 |
| text-embedding-3-small | 9,056 | 2026-04-01 | 2026-08-10 | 449,014 | 0.007669 |
| whisper-1 | 206 | 2026-06-25 | 2026-08-05 | n/a | **0.000000** |
| gpt-realtime-2 | 61 | 2026-05-12 | 2026-07-23 | 0 | **0.000000** |
| gpt-realtime-1.5 | 52 | 2026-04-01 | 2026-05-12 | 0 | **0.000000** |
| gpt-realtime-mini | 1 | 2026-08-04 | 2026-08-04 | 0 | **0.000000** |

**Last 60 days:**

| model | rows | sum cost_usd | distinct users |
|---|---:|---:|---:|
| gpt-5.4-mini | 160,847 | 144.504273 | 276 |
| gpt-4o-mini-transcribe-2025-12-15 | 43 | 0.555000 | 6 |
| text-embedding-3-small | 4,259 | 0.003986 | 98 |
| gpt-realtime-2 | 24 | 0.000000 | **0** |
| gpt-realtime-mini | 1 | 0.000000 | **0** |
| whisper-1 | 206 | 0.000000 | 11 |

Yes — realtime models (`gpt-realtime`, `gpt-realtime-2`, `gpt-realtime-mini`) **do** appear, confirming the feature is wired to log something. But every single realtime row has `total_tokens = 0` and `cost_usd = 0`, all-time, no exceptions. Whisper is logged (206 rows) but at $0 cost — see §7 (pricing-row gap, not free). AssemblyAI does **not** appear anywhere in `model`/`operation` in this window even though it's the primary short-form STT per project memory (`project_stt_assemblyai_...`) — that batch is uncommitted, so this is expected, not a bug.

## 3. Cost by model (using the stored `cost_usd`, confirmed complete per row — see caveats)

| window | text (gpt-5.4-mini) | STT (gpt-4o-mini-transcribe) | STT (whisper-1) | embeddings | realtime/voice |
|---|---:|---:|---:|---:|---:|
| All time | $171.135243 | $0.669000 | $0.000000 | $0.007669 | $0.000000 |
| Last 60d | $144.504273 | $0.555000 | $0.000000 | $0.003986 | $0.000000 |
| Last 30d | $117.293194 | $0 (no rows) | $0.000000 | $0.002343 | $0.000000 |

Realtime/voice logged cost is **$0.00 in every window measured** — not "small," literally zero.

## 4. Per-user cost (last 60 days)

| segment | distinct users | cost | cost/user |
|---|---:|---:|---:|
| Realtime voice (`model ILIKE '%realtime%'`) | **0** | $0.00 | **not computable** |
| Text (gpt-5.4-mini, the dominant model) | 276 | $144.504273 | **$0.524/user** |
| STT overall (`api_type='STT'`, all models) | 14 | $0.555000 | $0.0396/user (n<25, small segment — reported as count only per k-anonymity) |

**"Cost per active voice user" cannot be computed from this table**, for two independent reasons, both confirmed by code recon (growth-analyst, `app/services/openai_audio_service.py:380-394`):

1. **The audio cost itself is invisible to us.** The Flutter client opens WebRTC directly to `api.openai.com/v1/realtime/calls` using an ephemeral key. The realtime audio tokens are billed by OpenAI directly against that ephemeral session and never get reported back to our backend — there is no "log actual usage after the call ends" step implemented. The `create_realtime_session` row that *is* written logs the session being **opened**, with hardcoded `prompt_tokens=completion_tokens=total_tokens=0, is_estimate=True` — a placeholder, not a measurement.
2. **`user_id` is NULL on 100% of `create_realtime_session` rows, all-time** (confirmed both by my `model ILIKE '%realtime%'` cut and by growth-analyst's per-month/per-week `operation='create_realtime_session'` breakdown — every single month/week shows `users=0`). Even if audio cost were captured, today's rows couldn't be attributed to a user.

The only real, user-attributed cost *inside* a voice session is the text-side "director" logic (`voice_director.py`) that decides what to inject/embed during the call — `director_embed_user_text` (embeddings) and `director_injection_decision` (chat). All-time these total **$0.003098** across 61 + 1 users. That is the entire measurable AI cost of the realtime voice feature to date.

## 5. Cost by feature/context label (last 60 days)

`feature` is the useful cut — it maps directly to product surface:

| feature | rows | distinct users | cost |
|---|---:|---:|---:|
| SYSTEM | 155,401 | 0 | **$134.230000** |
| REFLECT | 3,909 | 81 | $5.345881 |
| PERSONAL_BIO | 393 | 129 | $0.832221 |
| CHART_EXPLANATION | 184 | 7 (n<25, suppressed detail) | $0.798218 |
| RECORDING | 159 | 5 (n<25, suppressed detail) | $0.790851 |
| PREP_CARD | 230 | 36 | $0.644908 |
| BETWEEN_SESSION | 326 | 28 | $0.399667 |
| GOAL | 1,689 | 62 | $0.342196 |
| DEBRIEF | 261 | 44 | $0.328243 |
| THERAPY_TRACKING | 344 | 212 | $0.273059 |
| CONVERSATION | 80 | 7 (n<25, suppressed detail) | $0.243744 |
| HERO_INSIGHT | 313 | 160 | $0.221959 |
| AFFIRMATION | 379 | 112 | $0.193805 |
| SYMPTOM | 166 | 31 | $0.185275 |
| HEALTH_CHECK | 60 | 23 (n<25, suppressed detail) | $0.129492 |
| REALIZATION | 127 | 29 | $0.098635 |
| SNAPSHOT | 4 | 3 (n<25, suppressed) | $0.002390 |
| RAG_INDEXING | 671 | 90 | $0.002339 |
| **REALTIME_VOICE** | **684** | **28** | **$0.000376** |

**REALTIME_VOICE is dead last — a rounding error next to every other feature, including RECORDING (async voice notes, a completely different pipeline) which costs ~2,100x more.**

Out-of-scope but impossible not to flag: **`SYSTEM` is 93% of last-60d spend ($134.23 of $144.90 total) and carries 0 attributed users** — this is almost certainly background jobs (weekly/monthly summaries, notification generation, etc.), not a per-user product feature. It dwarfs every product surface combined and deserves its own investigation, but that's a `data-analytics`/`growth-analyst` question, not this pull.

## 6. Total AI spend, last 30 days

**$117.295537** across 133,988 rows, 174 distinct users.

Realtime voice's share of that: **$0.00 logged / $117.30 total = 0.00% of tracked spend.** Restated honestly: this reflects a measurement gap, not proof that voice is free — real OpenAI Realtime API cost is being paid outside our tracked pipeline (directly against the ephemeral key), so it simply isn't in this denominator's world at all.

## 7. Data-quality caveats

- **Realtime audio cost is structurally unmeasured** (§4) — the single biggest caveat for this whole analysis. Any "voice is cheap" conclusion drawn from `token_usage_log` alone would be wrong; it's actually "voice cost is invisible to us."
- **`user_id` NULL on every `create_realtime_session` row, all 114 rows all-time** — a logging-path bug (key present in the row schema, value never populated), separate from the missing-cost problem. Fix candidates: `app/services/openai_audio_service.py:380-394`. Flagging to the lead to route to `backend-api`/`data-analytics` (whichever owns that file) — not mine to edit.
- **Missing `model_pricing` rows** for models actively in use in the last 60 days: `gpt-realtime-mini` and `whisper-1`. `whisper-1` logged 206 real rows at $0.000000 cost specifically because there's no pricing row to compute against — its true cost is understated, not zero. (`gpt-4o-mini-transcribe-2025-12-15` *does* have a pricing row — `price_per_minute=$0.0030` — and correctly shows nonzero cost.)
- **Two realtime models *do* have `model_pricing` rows configured** (`gpt-realtime-1.5`: $10/$20/$0.30 per 1M prompt/completion/cached; `gpt-realtime-2`: $32/$64/$0.40 per 1M) — so pricing exists and is ready the moment real token counts start flowing. It's the instrumentation, not the pricing table, that's missing.
- 2,754 embedding rows in the last 60d show `cost_usd = 0` individually despite `total_tokens > 0` — this is DECIMAL(10,6) rounding on genuinely tiny embedding costs (text-embedding-3-small at $0.02/1M tokens), not a pricing gap; the aggregate ($0.003986) is nonzero and correct.
- 274 of 165,380 last-60d rows (0.17%) are flagged `is_estimate = True`, cost $0.555000 — worth knowing the estimate flag exists and is barely used, not a material caveat.
- `SYSTEM`-feature rows are not user-attributed (§5) — any per-user cost math must exclude them, which all my per-user figures already do (I used feature/model cuts that only include user-driven rows).

## Bottom line for the B7 investment decision

Given the data available, the honest framing for growth-analyst is: **we cannot compute a defensible cost-per-active-voice-user today because the number doesn't exist in our own data — not because it's small.** The only real, measured cost of realtime voice so far is under $0.01 all-time (the director text side-channel), which says nothing about the actual OpenAI Realtime API bill. To make this decision on real numbers, `backend-api`/`data-analytics` need to either (a) implement the "log actual usage after the realtime call ends" step the code comment already promises, using OpenAI's realtime usage webhook/API, and backfill `user_id` on session-open rows, or (b) pull the true number from the OpenAI platform billing dashboard directly (outside this database) as an interim proxy, keyed by API-key/time-window rather than per-user.
