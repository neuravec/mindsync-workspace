# DEPLOY: recap voice floor (backend) + voice turn capture (frontend)

## 2026-10-06: deployed to production (backend) and dev/TestFlight (frontend)

Operator approval: 2026-10-06, "Tak, backend i front", given after green QA.
Gates: QA GO (`qa-regression.md` sections 1-4, including the `-vf` security-fix branches), security GO (`design-specs/2026-10-03-first-voice-conversation/audit-security.md`, section "Voice floor and turn capture review 2026-10-06").
Executed by: integration-devops.

### 1. What shipped

**Backend, Heroku `mindsync`, release v563** (`Deploy 76d5c093`, created 09:45:24 UTC / 11:45:24 CEST).
`origin/main` moved `99a2933..76d5c09` as a fast-forward of `fix/recap-voice-floor-vf` (no force):

| commit | what it does for the user |
|---|---|
| `bd47da6` | A voice first conversation is no longer judged "too short" by text-era thresholds. A reply counts when it has at least 3 real words (fillers like "um" do not count), and a recap needs 2 such replies and 10 counted words in total (was 40 words). A short recap keeps its memory notes. Recap cache key moved to `v2` so old "short" verdicts cached under `v1` are not reused; account and thread deletion clear both versions. |
| `a1f3560` | `POST /api/v1/audio-v2/realtime-session` now returns `client_session_config.noise_reduction` (the same `{"type": "near_field"}` the key was minted with), so the app can send it back in `session.update` and the setting cannot silently drop. Additive and optional: older apps ignore it. |
| `76d5c09` | Security review VF-M1: a recap answer without recap items writes no memory. |

No migration (no `alembic` file in the diff; models, `app/db`, `app/core`, Procfile, requirements and `.env*` untouched). Alembic head on prod stays as it was.

**Frontend, `mindsync-frontend` `dev`**: `156dbc8..f4afaa6` (fast-forward of `fix/voice-turn-capture-vf`, no force), pushed 09:55:04 UTC / 11:55 CEST. Base was `156dbc8` = tag `app_2.0.104`. Codemagic picks it up as **2.0.105** (TestFlight + Play internal). As of 10:22 UTC (27 minutes after the push) the Codemagic "Pre-release updates" bump commit and tag `app_2.0.105` had not landed on `origin/dev` yet; earlier bumps took up to 22 minutes, so check the Codemagic dashboard if it is still missing.

| commit | what it does for the user |
|---|---|
| `71991bb` | No answer is lost or miscounted when the person taps End: the last spoken answer is drained and kept. Sends the backend's `noise_reduction` in `session.update`. New analytics properties (see section 5). |
| `f4afaa6` | Security review VF-L1: once End has started, the microphone cannot be switched back on. |

### 2. Config Vars checked (read-only, nothing changed)

- `FIRST_CONVERSATION_RECAP_PROMPT`: not set (empty). The code default, which carries the new recap rule, is what prod uses.
- `FIRST_CONVERSATION_RECAP_ONLY_PROMPT`: not set (empty). Same.
- No Config Var was added, changed or removed in this deploy. Release v563 is a code release only.

### 3. Verification evidence

- Boot (09:45:51 to 09:45:58 UTC): web `Application startup complete`, scheduler cleared and re-registered its jobs as usual, worker `*** Listening on high, default...`. No traceback at import or lifespan, no H10/H1x, no R10/R1x.
- `heroku ps`: `web.1`, `worker.1`, `scheduler.1` all `up` since 11:45:52-11:45:58 CEST, still up 18 minutes later.
- `GET /api/v1/audio-v2/health`: HTTP 200 in 0.19 s.
- One-off smoke dyno `run.7010` (read-only import script, exited by itself):
  - recap cache version `v2`, legacy `('v1',)`, key format `reflect:recap:v2:<conversation_id>`
  - floor: `RECAP_MIN_USER_TURNS=2`, `RECAP_MIN_USER_WORDS=10`, `RECAP_MIN_TURN_WORDS=3`, `MEMORY_EXTRACTION_MIN_USER_WORDS=10`, 72 filler words
  - prompt versions `first-conversation-recap-v3`, `first-conversation-recap-only-v2`
  - `VoiceSessionConfig` has `noise_reduction`; `RealtimeSessionResponse` has `client_session_config`; `input_noise_reduction()` = `{'type': 'near_field'}`; a config with `noise_reduction` validates and keeps it
- Logs 09:45 to 10:02 UTC: 0 tracebacks, 0 router 5xx. No `[OrcaMemory] Recap` or `[FirstConversation]` lines yet (no first conversation happened in that window; low midday traffic). Worker warnings in that window were only the expected free-tier fallback for notification text (premium gate from 2026-09-13), not related to this change. `[OrcaBackfill]` sweep ran clean (candidates=0, errors=0).
- Contract: backend `noise_reduction: Optional[Dict[str, str]] = None` matches the app model `noise_reduction` (nullable map, omitted from `session.update` when null). Mixed versions are safe both ways: old apps ignore the new field; the new app against a rolled-back backend gets null and omits the key.

### 4. Rollback

**Backend** (code only, no migration, so a slug rollback is complete):

```bash
heroku rollback v562 -a mindsync
```

Then make it durable on `main`, or the next push redeploys the change (push to `main` auto-deploys):

```bash
git -C MindSync revert --no-edit 99a2933..76d5c09
git -C MindSync push origin main
```

Side effect after a rollback: recaps cached under `reflect:recap:v2:*` are not read or cleared by the old code; they expire on their own within 24 h (`RECAP_STORE_TTL_SECONDS`). The old code reads `v1` again.

**Frontend** (the two commits are plain commits, not merges):

```bash
git -C mindsync-frontend fetch origin
git -C mindsync-frontend checkout -b revert/voice-turn-capture origin/dev
git -C mindsync-frontend revert --no-edit 156dbc8..f4afaa6
git -C mindsync-frontend push origin HEAD:dev
```

Then expire build 2.0.105 in App Store Connect (TestFlight) and halt it in the Play internal track. Codemagic builds the reverted state as the next version.

The frontend works against both backend versions, so the two rollbacks are independent. If both are needed, roll back the backend first only if the backend is the cause; otherwise the order does not matter.

### 5. Analytics change (tell growth-analyst)

- `first_conversation_ended.user_turns` now counts a voice reply only when it has **3 or more words**. Shorter voice fragments go to the new property `user_fragments`. The old meaning is `user_turns + user_fragments`. Text replies always count as turns. Any insight that trends `user_turns` will step down from build 2.0.105 on; this is a definition change, not fewer replies.
- `voice_chat_ended` gains `transcription_failed_count` (int) and `end_drain_timed_out` (bool).

Follow-up for **posthog-data-extractor**, once 2.0.105 has sessions on devices (TestFlight testers first): confirm that `voice_chat_ended.transcription_failed_count` arrives as an int, `voice_chat_ended.end_drain_timed_out` as a bool, and `first_conversation_ended.user_fragments` as an int, filtered to `properties.$app_version = '2.0.105'`. Until then the properties cannot exist in PostHog.

### 6. Device QA (open, build 2.0.105)

1. A first conversation of about 2 minutes with ordinary short answers shows a real recap (not the "too short" state), and notes appear in "What Orca remembers".
2. Tapping End right after speaking keeps that last answer (it appears in the transcript and counts toward the recap).
3. The microphone cannot be turned back on during End on the Reflect voice screen and on the journal voice screen.
4. No echo turn right after Orca's opening line (no person turn saved within about a second of the opening).
5. Analytics: see section 5; growth-analyst informed of the `user_turns` definition change.

Backend logs while doing 1-4: the recap status (`ready`, `short`, `failed`) is not logged at info level; it is in the response of `POST /api/v1/reflect/{conversation_id}/recap` (router line should show `status=200`) and on screen. `[OrcaMemory] Recap ...` and `[FirstConversation] ...` lines are warnings and errors only, so for a healthy run there should be none, and no `Traceback`.
