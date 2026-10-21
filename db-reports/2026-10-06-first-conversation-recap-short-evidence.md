# First conversation: why the recap said "You kept it short" (2026-10-06)

**Author:** database-administrator (read-only)
**Scope:** prod Postgres (Azure, via Heroku one-off dynos run.1409, run.8377, run.7733, all stopped), prod Redis (read-only `EXISTS/TTL/GET`), Heroku log buffer (05:35:59 to 06:01:58 UTC).
**Build under test:** backend v562 (main 99a2933, deployed 2026-10-06 06:32 CEST), frontend 2.0.104 (dev 185d62a).
**Privacy:** metadata only. No message was decrypted. Lengths below are lengths of the stored encrypted envelope. The account is identified by a sha256 prefix (`225a543db2`), never by UID or email. The one value read from an encrypted Redis entry is the recap's `status`, item count, `saved_line_kind` and `memory_items_saved`; that recap has zero items, so no recap text exists to expose.

## Verdict

| Question | Answer |
|---|---|
| Were the person's turns saved? | **Yes.** 6 USER rows, none empty, all with an embedding, 05:56:31 to 05:58:39 UTC. All 6 `audio/user_message_add` calls returned 200. |
| Were the agent's turns saved? | **Yes.** 7 agent rows (stored as role `SYSTEM`, the voice convention), 05:56:30 to 05:58:40 UTC, plus the system prompt at index 0. All 7 `audio/agent_message_add` calls returned 200. |
| When was `/end` called? | 05:58:52.735 UTC: **13.6 s after the last saved user turn** and 11.9 s after the last agent turn. Nothing was posted to the thread after `/end` (no late transcript, no 404). |
| Which recap branch ran? | **`short` from the word-count gate**, with no model call: log line `Recap for thread 28613: status=short items=0 memory=0 cached=False in 9ms`. |
| Why? | `generate_recap` answers `short` when `user_turns < 2` **or** `user_words < 40`. User turns were 6, so the gate that fired is **fewer than 40 words in the person's stored transcript**. The stored person text is 176 to 266 bytes across 6 turns (per turn 0 to 95 bytes). |
| Was it a race (recap before turns persisted)? | **No.** The recap ran 70 ms after `/end`, on a thread whose last turn had been committed 13 s earlier. |
| Error or failure? | **No.** No 4xx/5xx on any `/reflect/` path in the buffer, no recap failure counter in Redis, and `failed` is a different status (the client shows different copy for it). |

So the copy "You kept it short" is the exact intended mapping of the server's `short`, and the server's `short` is the exact result of the 40-word gate on what was transcribed. Nothing was lost between the phone and the database. The open question is upstream of the database: **why two minutes of speaking produced only about 25 to 50 words of stored transcript** (see section 5).

## 1. Threads (step 1)

Query (Core SQL against `conversations.entry_origin`, which the ORM mapper excludes):

```sql
SELECT id, created_at, status::text, last_message_at, modality, (title IS NOT NULL) AS has_title,
       memory_extracted_through_message_id AS mem_watermark,
       left(encode(sha256(convert_to(user_id,'UTF8')),'hex'),10) AS uid_h
FROM conversations
WHERE entry_origin = 'onboarding_first_conversation' AND created_at >= '2026-10-06 00:00:00'
ORDER BY created_at DESC LIMIT 5;
```

| id | created_at (UTC) | status | last_message_at (UTC) | modality | title | memory watermark | uid_h |
|---|---|---|---|---|---|---|---|
| **28613** | 05:56:23.083 | FINISHED | 05:58:40.845 | voice | set | NULL | 225a543db2 |
| 28612 | 05:34:08.320 | FINISHED | 05:35:17.976 | voice | set | NULL | 225a543db2 |

Both belong to the same account (the operator). Thread 28613 was started as an onboarding re-run (`Started first-conversation Reflect thread 28613 ... (rerun=True)`). The account has 3 marked threads in total (2026-10-05 08:32 = 28546, plus the two above), all FINISHED. There is no `ended_at` column; `last_message_at` and the `/end` log line give the end time. Prod `alembic_version = m316a1b2c3d4`.

Prod column types worth knowing: `conversations.created_at` and `messages.created_at` are `timestamp without time zone` (stored as UTC wall time), `last_message_at` is `timestamptz`.

## 2. Messages (step 2)

```sql
SELECT role::text, count(*), min(created_at), max(created_at),
       sum(CASE WHEN content IS NULL OR content = '' THEN 1 ELSE 0 END) AS empty_n,
       min(length(content)), max(length(content)), sum(length(content))
FROM messages WHERE conversation_id = :c GROUP BY 1;
-- and per message, in the order the recap reads them (created_at, id):
SELECT row_number() OVER (ORDER BY m.created_at, m.id) - 1 AS idx, m.id, m.role::text, m.created_at,
       length(m.content) AS enc_len, (e.id IS NOT NULL) AS has_emb
FROM messages m LEFT JOIN message_embeddings e ON e.message_id = m.id
WHERE m.conversation_id = :c ORDER BY m.created_at, m.id LIMIT 120;
```

**By role, thread 28613:** SYSTEM 8 rows (system prompt + 7 agent turns), USER 6 rows, 0 empty rows.

**Per message, thread 28613.** The plaintext range is derived from the envelope length only: the column holds base64 of a Fernet token, so each envelope length maps to one 16-byte plaintext band.

| idx | role | created_at (UTC) | envelope | plaintext bytes | embedding |
|---|---|---|---|---|---|
| 0 | SYSTEM (prompt) | 05:56:23.118 | 17996 | n/a | no |
| 1 | agent | 05:56:30.099 | 332 | 112-127 | no |
| 2 | **USER** | 05:56:31.051 | 136 | **0-15** | yes |
| 3 | agent | 05:56:32.670 | 332 | 112-127 | no |
| 4 | **USER** | 05:57:05.523 | 160 | **16-31** | yes |
| 5 | agent | 05:57:06.891 | 332 | 112-127 | no |
| 6 | **USER** | 05:57:25.091 | 136 | **0-15** | yes |
| 7 | agent | 05:57:28.022 | 588 | 256-271 | no |
| 8 | **USER** | 05:57:56.542 | 220 | **48-63** | yes |
| 9 | agent | 05:57:57.895 | 332 | 112-127 | no |
| 10 | **USER** | 05:58:19.044 | 272 | **80-95** | yes |
| 11 | agent | 05:58:21.268 | 444 | 176-191 | no |
| 12 | **USER** | 05:58:39.139 | 188 | **32-47** | yes |
| 13 | agent | 05:58:40.841 | 504 | 208-223 | no |

Person total: **176 to 266 bytes** of text in 6 turns. At 5 to 7 bytes per spoken word (with spaces; more for Polish in UTF-8) that is roughly 25 to 50 words, and the server's own count landed under 40.

Thread 28612 (the attempt 22 minutes earlier, 70 s long): 5 USER rows, 80 to 155 bytes in total, recap also `short`.

## 3. Recap state (step 3)

Where it lives: `app/services/orca_memory.py`. `generate_recap` caches its result in Redis under `reflect:recap:v1:{conversation_id}` for `RECAP_STORE_TTL_SECONDS = 24 h` (Fernet-encrypted JSON: `status`, `items`, `saved_line_kind`, `memory_items_saved`, `crisis`). Related keys: `reflect:recap:fail:{id}` (failure counter), `reflect:recap:lock:{id}`, the bio flag, and the analysis-job key written by `/end`.

| Thread | recap key | TTL left | status | items | saved_line_kind | memory_items_saved | fail counter | lock | bio flag | analysis-job key |
|---|---|---|---|---|---|---|---|---|---|---|
| 28613 | present | 85930 s | **short** | 0 | check_in | 0 | none | released | set | set |
| 28612 | present | 84531 s | **short** | 0 | check_in | 0 | none | released | set | set |
| 28546 (2026-10-05, calibration) | present | 8784 s | **ready** | 3 | n/a | 5 | n/a | n/a | n/a | n/a |

The branch, from the code deployed in 99a2933 (identical to local HEAD for `orca_memory.py` and `reflect.py`):

```python
RECAP_MIN_USER_TURNS = 2
RECAP_MIN_USER_WORDS = 40
...
if transcript.user_turns < RECAP_MIN_USER_TURNS or transcript.user_words < RECAP_MIN_USER_WORDS:
    result = RecapResult(status=RECAP_STATUS_SHORT, ...)   # no model call, cached
```

`user_words` is the sum of `len(text.split())` over every decrypted USER turn after message 0. The other way to get `short` (the model returns no usable items) needs a model call, and a 9 ms recap rules that out.

Calibration: thread 28546 had 7 user turns with 272 to 377 bytes of person text, and got `ready` with 3 items and 5 memory facts. 28613 had 176 to 266 bytes and got `short`. The cut-off sits between the two, which fits the 40-word gate.

**Memory (`user_memory_items`, counts only):** 0 rows created since 04:30 UTC (06:30 CEST) for this account, with any `source`/`source_kind`. The extraction watermark on both of today's threads is NULL, because the `short` branch returns before memory planning. The account has 12 active memory items, all older. The Personal Bio refresh was skipped (`already refreshed ... in the last 24 h`).

**What did run after `/end`:** the analysis job (conversation summary row at 05:58:55, `[ReflectAnalysis] Thread 28613 analyzed (trigger=end, topics=4)` at 05:59:12), symptom suggestions (2 created), RAG indexing of the summary, and the auto-title (05:57:09). The same transcript that was too short for the recap was enough for these jobs.

## 4. Request sequence, thread 28613 (step 4)

From the router and uvicorn lines (no bodies, no identities). Every call returned 200.

| UTC | request | note |
|---|---|---|
| 05:56:23.130 | POST /reflect/start | marked thread created, rerun=True |
| 05:56:23.666 | GET /reflect/28613/session_data | logged `Legacy /v1/realtime/sessions returned 404, falling back` (the fallback works) |
| 05:56:24.839 | POST /audio-v2/realtime-session | client secret minted, model gpt-realtime-2.1 |
| 05:56:30.110 | POST .../audio/agent_message_add | opening |
| 05:56:31.978 | POST .../audio/user_message_add | **0.95 s after the opening was saved** |
| 05:56:32.682 | POST .../audio/agent_message_add | |
| 05:57:06.402 | POST .../audio/user_message_add | |
| 05:57:06.902 | POST .../audio/agent_message_add | |
| 05:57:25.314 | POST .../audio/user_message_add | |
| 05:57:28.034 | POST .../audio/agent_message_add | |
| 05:57:56.762 | POST .../audio/user_message_add | |
| 05:57:57.907 | POST .../audio/agent_message_add | |
| 05:58:19.261 | POST .../audio/user_message_add | |
| 05:58:21.279 | POST .../audio/agent_message_add | |
| 05:58:39.358 | POST .../audio/user_message_add | last user turn |
| 05:58:40.853 | POST .../audio/agent_message_add | last agent turn |
| 05:58:52.749 | POST /reflect/28613/end | `ended`, analysis enqueued (job logged at 05:58:52.735) |
| 05:58:52.820 | POST /reflect/28613/recap | `status=short items=0 memory=0 cached=False in 9ms` |

The client called `/recap`, so its own turn counter was above zero (with 0 it shows "short" without calling the server). No non-2xx on any `/reflect/` path in the whole buffer. Thread 28612's `/end` and `/recap` (about 05:35:20 to 05:35:40) fall just before the buffer starts; Redis shows that recap was also `short`.

## 5. Interpretation: where the words went

The database holds everything the client sent, in order, before `/end`. The recap logic did what it was written to do. The gap is between what was said and what was transcribed and sent:

- The thread lasted 138 s from creation to the last turn. Between an agent turn being saved and the next user turn being saved there were gaps of 33, 18, 28, 21 and 18 s. Part of each gap is the agent still speaking (agent transcripts are saved when generation ends, before playback finishes; the agent turns here are about 20 to 45 words). Even so, if the person spoke for most of the remaining time, 176 to 266 bytes is well short of normal speech (about 2.5 words per second).
- **Not a regression of v562 / 2.0.104.** The operator's own earlier voice Reflect threads have the same per-turn sizes: median envelope 136 to 190 (0 to 47 bytes per turn) in every voice thread since 2026-09-18. Pooled baseline over non-marked voice Reflect threads in the last 60 days (7 users, 17 threads, 301 user turns; fewer than 25 users, so a pooled length distribution only, with no per-user breakdown): per-turn plaintext median 32 to 47 bytes, p75 112 to 127, p90 about 192 to 207. **In this app, voice user turns are consistently short**, so a two-minute voice conversation can easily stay under 40 words. That makes the 40-word gate a poor fit for voice.
- The first USER row in 28613 was saved 0.95 s after the opening and is 0 to 15 bytes. That is too fast for an answer to an opening that takes several seconds to play, so it is probably an echo, noise or barge-in fragment, and it counts as a turn. 28612 (two USER rows 2.5 s apart right after the opening) and 28546 show the same pattern. This is a hypothesis that only the content or the client's audio events can confirm.

What the database cannot answer as asked: whether the transcription dropped speech (truncated per-utterance transcripts) or the operator answered briefly with pauses. Separating the two needs either the per-turn input audio duration (realtime usage on the client, e.g. `first_conversation_ended.input_tokens` in PostHog, or the realtime transcription events) or, with explicit operator consent, an in-dyno decrypt that prints **only the integer `user_words`** for 28613 (the exact number compared with 40) and nothing else.

## 6. Handoffs

1. **backend-api** (owner of `app/services/orca_memory.py`): the gate `user_turns < 2 or user_words < 40` is tuned for text and rejects ordinary short voice conversations. Options: lower the word floor for voice threads (for example 15 to 20 words), or accept on turns (for example at least 3 person turns) and let the model's own "no usable items" path decide `short`. Keep `short` cached as today. Add a test with a 6-turn, about 30-word voice transcript.
2. **flutter-mobile:** (a) "You kept it short" is shown for server `short` regardless of duration; the hand-off already carries `durationSeconds`, so a conversation of 60 s or more could get the neutral copy instead. (b) Check whether realtime input transcription captures whole utterances (compare per-turn audio duration with transcript length), and whether a user turn fired within about 1 s of the agent's opening is an echo artifact that should not count.
3. **posthog-data-extractor** (optional): `first_conversation_ended` for this session (`duration_s`, `user_turns`, `input_tokens`) and `first_conversation_recap_result` (`status=short`) to cross-check the client-side counts against the 6 stored turns.
4. **Incidental, backend-api:** worker log 06:00:49 UTC, `usage_tracking.log_token_usage` failed with `invalid input value for enum featureenum: "MOOD_TREND"`. `FeatureEnum.MOOD_TREND` exists in `app/models/models.py:746` but not in prod's native `featureenum`, so mood-trend token usage is silently not logged (non-fatal). Needs an idempotent `ALTER TYPE featureenum ADD VALUE IF NOT EXISTS 'MOOD_TREND'` migration (autocommit block). Not verified against `pg_enum` in this pass.

## Appendix: method notes

- Access: `heroku run -a mindsync python < script.py` with REPL-safe scripts, `SET TRANSACTION READ ONLY`, `statement_timeout`, `db.rollback()`/`close()`, no commit. Dynos run.1409, run.8377 and run.7733 were stopped after capture.
- Envelope to plaintext: plaintext `p` bytes gives Fernet raw length `57 + 16*(floor(p/16)+1)`, the token is `4*ceil(raw/3)` chars, and the stored column is base64 of that again (`4*ceil(token/3)`). Each stored length therefore identifies a 16-byte plaintext band (136 = 0-15, 160 = 16-31, 188 = 32-47, 220 = 48-63, 272 = 80-95).
- Logs: `heroku logs -n 1500` (all, `--dyno web`, `--dyno worker`, router). The buffer covered 05:35:59 to 06:01:58 UTC. UIDs, IPs and emails in raw lines were masked before reading and are not reproduced here.
