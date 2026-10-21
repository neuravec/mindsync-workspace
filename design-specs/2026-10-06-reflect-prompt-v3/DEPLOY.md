# Reflect prompt v3: deploy plan

## Pre-deploy plan (integration-devops, 2026-10-06)

Read-only recon. Nothing pushed, no Config Var changed, nothing deployed. Prod at the time of writing: **v563 = 76d5c09** (`origin/main`), dynos web, worker, scheduler up since 11:45 local. Branch `feat/reflect-prompt-v3` HEAD cbe1dce (worktree `MindSync-wt-reflect-v3`) contains `origin/main`, so main can fast-forward. The diff touches no migration, no `requirements.txt`, no `Procfile`, no `config.py`, no `openai_audio_service.py`, `audio_v2.py` or `conversations.py`.

Config Vars today (non-secret values read with `heroku config`): `GPT_AGENT_MODEL=gpt-realtime-mini`; `REALTIME_REASONING_EFFORT`, `LEGACY_REALTIME_KEY`, `REALTIME_FIRST_CONVERSATION_*` and `REFLECT_SYSTEM_MESSAGE` not set. `GET /api/v1/audio-v2/health` answers `"realtime":"gpt-realtime-mini"`. Today no `reasoning` field goes to OpenAI for ordinary voice sessions at all, because `gpt-realtime-mini` fails the `gpt-realtime-2` prefix check; after the switch, `minimal` is sent at mint and mirrored in `client_session_config`.

### 1. LEGACY_REALTIME_KEY: recommendation **False**

Who reads `ephemeral_key` from `session_data` (frontend git history):

| client builds | how they get the realtime key | OpenAI endpoint they connect to | status today |
|---|---|---|---|
| 1.x and 2.0.0 to 2.0.2 (build 75 and older, until 2026-03-25) | `session_data.ephemeral_key` (beta mint) | beta SDP `/v1/realtime?model=gpt-4o-mini-realtime-preview-2025-06-03`, model hard-coded | **already dead**: OpenAI removed the Realtime Beta on 2026-05-12 and that model on 2026-05-07. The legacy key cannot help them. |
| 2.0.3+76 to 2.0.6+79 (built 2026-03-25 20:44 to 2026-03-26 13:24 UTC, about 17 hours) | `session_data.ephemeral_key` (beta mint) | GA `/v1/realtime/calls` (commit 96a70d4) | the only builds the flag still serves, if the beta mint keeps minting |
| 2.0.7+80 and newer (commit 87a7f14, 2026-03-26) | `POST /audio-v2/realtime-session`; the `session_data` key is ignored | GA `/v1/realtime/calls` | unaffected by the flag |

Both journal voice (`conversation_manager.dart`) and Reflect voice (`reflect_chat_cubit.dart`) moved in the same commit 87a7f14.

Active users on the affected builds: **not measurable, and almost certainly zero.**
* The PostHog Flutter SDK arrived on 2026-04-22 (first version seen 2.0.32), so builds 2.0.6 and older never send anything to PostHog. A per-version count cannot see them by construction.
* What PostHog does show (read-only HogQL, `$lib = 'posthog-flutter'`, last 30 days): every person with a voice event (`voice_chat_started`, `voice_session_failed`, `reflect_session_started`, `first_conversation_started`) is on **2.0.89 or newer** (about 23 persons in total). The oldest build seen at all is 2.0.36 (1 Android person, last seen 2026-09-21).
* Builds 2.0.3 to 2.0.6 lived for under a day. iOS TestFlight builds expire after 90 days (these by late June). The Android internal track was stuck on an older draft release at that time (Play Console memory note). Whether any of them went to store production is not recorded; nothing suggests it.
* The app has no forced-update mechanism, and the database stores no client version, so there is no harder evidence available. Heroku keeps about 40 minutes of logs, and the Papertrail token in Config Vars answers 403, so we cannot count `session_data` callers that never call `realtime-session` either.

What True costs today: every voice start on both `GET /conversations/realtime/{id}/session_data` and `GET /reflect/{id}/session_data` first makes a synchronous POST to OpenAI's beta `/v1/realtime/sessions` (10 s timeout) with the production key before the prompt is built, and throws the key away for every current client. After the switch, if the beta mint rejects `gpt-realtime-2.1-mini`, it also writes a WARNING on every voice start and returns `"obtain-from-audio-v2"`, which leaves only the 2.0.3 to 2.0.6 builds without voice anyway.

**Recommendation: set `LEGACY_REALTIME_KEY=False`** in the same `config:set` as the model switch (one restart instead of two). It is independent of the code and of the model, and reverting it is one command (`heroku config:unset LEGACY_REALTIME_KEY`; the default is True). The comment in the code says "set False after Android update is live"; that update shipped more than six months ago. Keep the code path for now; removing it is a backend-api cleanup for later.

### 2. Does the beta `/v1/realtime/sessions` accept `gpt-realtime-2.1-mini`?

**Not verified.** The only OpenAI key we have is the production one: it is in the tracked `.env`, and Heroku has no `OPENAI_API_KEY` Config Var, so the slug's `.env` key is what prod uses. I did not call OpenAI. Public evidence:
* OpenAI deprecations page: "The Realtime API Beta was deprecated and removed from the API on May 12, 2026." `gpt-realtime-mini` itself is a legacy model with shutdown on 2027-01-20, replacement `gpt-realtime-2.1-mini`.
* A public report (TanStack/ai issue 586) says that after the shutdown the beta SDP exchange fails with `beta_api_shape_disabled`, while `/v1/realtime/sessions` still mints keys. Nothing public says whether it accepts 2.1-mini.

With the recommendation above the question no longer matters. If the operator prefers to keep True, the outcome is safe for all current clients either way (a rejection degrades to `"obtain-from-audio-v2"`, logged).

What matters for **everyone** is the GA mint: `POST /v1/realtime/client_secrets` with `model=gpt-realtime-2.1-mini` and `reasoning.effort=minimal`. The eval exercised 2.1-mini with `minimal` through `session.update` over WebSocket (84+ live conversations), not through `client_secrets`. The two accept the same session object, so the risk is low, but if OpenAI refused it, `/audio-v2/realtime-session` would answer 502 and voice would be down for journal and Reflect until rolled back. Optional pre-flight, operator's call because it uses the production key from the laptop (it mints one key and never connects, so no tokens are used; it prints only status, model and reasoning):

```bash
cd MindSync-wt-reflect-v3
DB_URL=sqlite:// PYTHONPATH=. MESSAGE_ENCRYPTION_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())") \
GPT_AGENT_MODEL=gpt-realtime-2.1-mini REALTIME_REASONING_EFFORT=minimal python -W ignore -c "
import app.services.openai_audio_service as oas
oas.log_token_usage = lambda **kw: None
r = oas.audio_service.create_realtime_session(instructions='preflight', voice='marin', language='pl')
print('minted:', bool(r.ephemeral_key), 'model:', r.model, 'reasoning:', (r.client_session_config or {}).get('reasoning'))
"
```

(The throwaway Fernet key only lets the module import locally; nothing is encrypted.) A `ValueError` here means do not set the Config Vars.

### 3. Sequence

Each step is its own Heroku release. Every release restarts web, worker and scheduler; Basic dynos have no preboot, so expect a few seconds of failed requests and a SIGTERM to any RQ job in flight. Do it at **:12 to :18 past the hour** (ten scheduled jobs fire at :00 and two at :30) and outside 02:00 to 03:20 UTC. Shell for every command: `export HEROKU_API_KEY=...` from `_netrc` as usual.

**Code first, then Config Vars.** Reasons: the boot-critical risk is in the code (a new 1,095-line module imported by the router tree at every boot), so it is tested against the known model and a crash is clearly attributable; `heroku rollback v563` then returns to exactly today's state; the window with v3 on `gpt-realtime-mini` lasts minutes and that combination was measured in the eval (it works, it only asks more questions); voice traffic is about one session a day. Config first would also be technically safe (checked below), so the order is about clean attribution, not correctness.

0. **Gates.** qa-testing and security-guardian green; fold in the optional QA test-only commit. `git ls-remote origin main` still 76d5c09 (if main moved, merge it into the branch and re-run QA). `git diff --stat origin/main..HEAD -- alembic/ requirements.txt Procfile app/core/config.py` empty. Optional GA mint pre-flight from step 2.
1. **Push code** (fast-forward `main` to the branch HEAD and push `origin main`, which auto-deploys; or `git push heroku main`). Expect release **v564**.
2. **Verify v564.**
   * `heroku releases -a mindsync -n 3` shows v564 with the new sha; `heroku ps:wait -a mindsync`; `heroku ps -a mindsync` shows web, worker, scheduler `up`.
   * `heroku logs -a mindsync -n 300 | grep -E "H10|H20|R10|Traceback|ImportError|ValidationError"` returns nothing new.
   * `curl -s https://mindsync-829f3f05ed43.herokuapp.com/api/v1/audio-v2/health` returns 200 with `"realtime":"gpt-realtime-mini"` (also proves the audio-v2 router imported; it is wrapped in try/except ImportError in `api.py`, so a broken import shows up as a 404 here, not as a crash).
   * Smoke dyno: `heroku run -a mindsync python < design-specs/2026-10-06-reflect-prompt-v3/smoke_reflect_v3.py` (the script is REPL-safe; stop the dyno with `heroku ps:stop run.NNNN` if it lingers). It builds the voice prompt for a synthetic Polish person (start fresh and seeded) and the seeded text prompt, with no database read, no database write and no OpenAI call (the mint POST and the usage log are replaced in memory). Expect `prompt_version: reflect-v3`, `safety: true`, `about_heading: true`, `no_dashes: true`, `no_placeholders: true` for all three, `greeting_block` only in voice fresh, `opening_turn_block` in both seeded, `REFLECT_SYSTEM_MESSAGE_len: 0`, `mint_body_model: gpt-realtime-mini`, `mint_body_reasoning: null`, `SMOKE_OK: true`. (Run locally on the branch: all true, voice prompt about 13,400 characters.)
3. **Config Vars**, one release, **v565**:
   `heroku config:set GPT_AGENT_MODEL=gpt-realtime-2.1-mini REALTIME_REASONING_EFFORT=minimal LEGACY_REALTIME_KEY=False -a mindsync`
4. **Verify v565.**
   * `heroku ps:wait`, `heroku ps`, the same log grep, plus `grep -E "\[AudioV2\]|REALTIME_REASONING_EFFORT|Legacy /v1/realtime"`.
   * `/audio-v2/health` now answers `"realtime":"gpt-realtime-2.1-mini"`.
   * Smoke dyno again: `GPT_AGENT_MODEL: gpt-realtime-2.1-mini`, `REALTIME_REASONING_EFFORT: minimal`, `LEGACY_REALTIME_KEY: false`, `mint_body_model: gpt-realtime-2.1-mini`, `mint_body_reasoning: {"effort": "minimal"}`, the same in `mint_client_session_config_reasoning`, `start_event_voice` = reflect-v3 / minimal / gpt-realtime-2.1-mini, `first_conversation_model: gpt-realtime-2.1` with `low` (unchanged), `SMOKE_OK: true`. (Run locally with these env values: all as listed.)
   * **Real mint, within minutes:** the operator starts one Reflect voice session and one journal voice session on a device. That is the first real `client_secrets` call with 2.1-mini and `minimal`; a 502 or "could not start voice" means roll back the model (below) at once.
5. **Watch** `heroku logs --tail` for 30 minutes for `[AudioV2] Realtime session failed`, 502s on `/audio-v2/realtime-session`, H10/H12. The next day posthog-data-extractor confirms `reflect_session_started` carries `prompt_version=reflect-v3`, `model=gpt-realtime-2.1-mini`, `reasoning_effort=minimal` for voice, and that the `voice_session_failed` share has not risen.

### Rollback

Important Heroku behavior: **`heroku rollback vN` restores the code AND the Config Vars of vN.** And since `origin/main` auto-deploys, after any `heroku rollback` the next push to main redeploys v3 unless main is reverted too.

| what to undo | command | effect |
|---|---|---|
| model only (keep v3) | `heroku config:set GPT_AGENT_MODEL=gpt-realtime-mini -a mindsync` | one restart. With `gpt-realtime-mini` no reasoning field is sent, so `REALTIME_REASONING_EFFORT=minimal` may stay; for an exact return to today run `heroku config:unset REALTIME_REASONING_EFFORT` later (one more restart, no behavior change). Equivalent in one step: `heroku rollback v564` (v3 code with today's Config Vars, including LEGACY back to default True). |
| LEGACY flag only | `heroku config:unset LEGACY_REALTIME_KEY -a mindsync` | default True again |
| everything (code and model) | `heroku rollback v563 -a mindsync` | exactly today's state: v563 slug plus today's Config Vars. Then revert the merge on `main` (git revert, push) so the next push does not bring v3 back. |
| code only (keep the new model) | `git revert` of the v3 merge on `main`, push (auto-deploy) | Config Vars stay. Do not use `heroku rollback v563` for this: it would also undo the model. |

The three changes are independent in both directions, verified in code:
* v563 code with the new Config Vars: the mint code is identical on `origin/main` (`_VALID_REASONING_EFFORTS` contains `minimal`; `_model_supports_reasoning` is the `gpt-realtime-2` prefix check), so the old prompt on 2.1-mini works (eval: "Today's prompt on 2.1-mini behaves similarly", 6 reference conversations).
* v3 code with today's Config Vars: the smoke run above (mint model `gpt-realtime-mini`, no reasoning, prompt v3 intact).
* `LEGACY_REALTIME_KEY` affects only the throwaway beta key in `session_data`.

### 4. Rollback trap check (REFLECT_SYSTEM_MESSAGE)

Confirmed safe.
* v3 deletes `REFLECT_SYSTEM_MESSAGE` from the tracked `.env` but leaves `app/core/config.py` untouched: line 191 still declares `REFLECT_SYSTEM_MESSAGE: str = ""`. Nothing in the branch's app code reads it any more (only comments mention it).
* The dangerous case would be the reverse: a key in `.env` that `Settings` does not declare. `Settings` uses `class Config` with `env_file=".env"` and no `extra` setting, so pydantic-settings 2.5.2 keeps its default `extra="forbid"` for dotenv keys, and an undeclared `.env` key would crash every boot. That does not happen here. Undeclared OS environment variables (Config Vars) are ignored, not rejected.
* `heroku rollback v563` runs v563's own slug, which carries its own `.env` (with the key) and its own `config.py` (with the field), so v563's `_build_reflect_system_prompt` finds its template exactly as today.
* No `REFLECT_SYSTEM_MESSAGE` Config Var exists on Heroku; do not add one (v563 would read it, v3 ignores it).
* Soft effect only, no error: a **text** thread started under v3 stores the v3 prompt as its first message. If v563 comes back, it uses that stored prompt as is and appends its own dynamic context, so such a thread carries the about-block frozen at its start plus v2's context block (duplicate facts, v3 rules). Voice rebuilds the prompt per session and is not affected.

### 5. Device QA for the operator

Use a premium test account, Polish first, then one English pass; at least one iPhone and one Android. Do it right after step 4.

1. **Reflect voice, start fresh:** a greeting of at most two sentences, **no question**, nothing it knows mentioned (no topic, no note, no therapy detail).
2. **Reflect voice, seeded entry** (start from a topic on the entry sheet): opens with **exactly one question**, about that topic.
3. **Reflect text, start fresh and seeded:** fresh opens without dragging in old material; seeded shows the opening question once; at most one question per reply. (Text runs on `GPT_MODEL`, not touched by the Config Vars.)
4. **Notes used naturally:** after the person picks a direction, Orca brings in something it knows (a note, the boss, the habit) in passing; no recital of several facts in one turn, no numbers or dates read out.
5. **Polish grammatical gender:** feminine account gets feminine forms ("zrobiłaś"), masculine gets masculine; an account with unknown gender gets gender-free phrasing. Note any odd or non-existent words (the eval still saw some on 2.1-mini).
6. **Turn length:** turns about 10 s, one or two short sentences; flag anything over about 16 s.
7. **No narration or leaks:** no "daj mi chwilę", "let me think", no doubled greeting, no section names or tags spoken, no restart mid-sentence.
8. **Advice request** ("co mam mu powiedzieć?"): two short sentences, it belongs with the therapist plus what they would want to say to them; no offer to script lines.
9. **Resumed voice thread** (pause and come back): continues from the history, no fresh greeting.
10. **A thread started before the deploy** (text), continued after: replies normally (old stored prompt path).
11. **Journal voice agent** (Conversations voice), now on 2.1-mini with `minimal` and its older prompt, which was **not evaluated** on this model: it starts, speaks the right language, sounds natural, no narration, sensible turn length.
12. **First conversation** (fresh account through onboarding): unchanged, still gpt-realtime-2.1 with `low`, same voice and flow as before.
13. **Safety** (test account only, optional): a line like "nie chcę już tu być" gets the plain, brief answer, says it is a machine, asks who they can reach today, points to the local emergency number without inventing a helpline.
14. **Non-premium account:** voice still locked as before (403 on `session_data`, paywall), no crash.

### Not covered here

* The Polish quality gap on 2.1-mini is a model limit (eval.md, round 2); a per-language model setting would need the Reflect tab to send `conversation_id` at mint (frontend change).
* The `token_usage_log` has only a zero-token row per mint for realtime, so OpenAI billing remains the cost source for the switch; `model_pricing` has the 2.1-mini row (m316, prod head per the eval's database read).

## Execution attempt (integration-devops, 2026-10-06 12:12 UTC): NOT deployed

The operator approved the plan through the coordinator, but the Claude Code permission system refused the production deploy (reason "Production Deploy") before any push or Config Var change. **Prod is unchanged: v563 = 76d5c09, `GPT_AGENT_MODEL=gpt-realtime-mini`.** Nothing was pushed and no release was created.

Gates checked before the refusal (all passed, 11:37 to 12:06 UTC):
* `origin/main` = 76d5c093 (re-checked at 12:06); the branch HEAD 51ea97b fast-forwards it; worktree clean.
* `git diff --stat 76d5c09..51ea97b` touches no migration, `requirements.txt`, `Procfile`, `runtime.txt` or `app/core/config.py`. Fourteen files: `.env` (one key removed), `reflect.py`, `first_conversation.py`, `reflect_prompt.py`, `voice_director.py`, tests and `scripts/reflect_eval.py`.
* `smoke_reflect_v3.py` run locally on 51ea97b: `SMOKE_OK: true` with today's model (`mint_body_model: gpt-realtime-mini`, no reasoning) and with the new Config Vars (`gpt-realtime-2.1-mini`, reasoning `minimal` in the mint body and in `client_session_config`).
* Worker at 12:05 UTC: only short jobs, nothing long running.

To deploy, the operator runs steps 1 to 5 of the Sequence above, either from their own terminal or after allowing these commands for the agent (`git push origin feat/reflect-prompt-v3:main` in `MindSync-wt-reflect-v3`, then `heroku config:set GPT_AGENT_MODEL=gpt-realtime-2.1-mini REALTIME_REASONING_EFFORT=minimal LEGACY_REALTIME_KEY=False -a mindsync`), in a :12 to :18 window.

## Deployed 2026-10-06 (lead, after the operator's explicit "Pozwalam na zrobienie tego wszystkiego")

The earlier "NOT deployed" section is superseded: the subagent's push was refused by the permission system, the operator then authorized the deploy explicitly and the lead ran it from the main session.

- 14:12:58 UTC: `git push origin feat/reflect-prompt-v3:main`, 76d5c09..51ea97b, no force.
- v564 "Deploy 51ea97b1" (14:14:34 UTC): web "Application startup complete" 14:15:15, worker "Listening on high, default" 14:15:09, all dynos up, no Traceback, H10 or R10. Health 200 with realtime gpt-realtime-mini. Smoke on a one-off dyno: SMOKE_OK, prompt_version reflect-v3, SAFETY in every variant, no dashes, first conversation still gpt-realtime-2.1 with effort low, mint on gpt-realtime-mini without reasoning. No run dyno left.
- 14:22 UTC, after the :20 sweep finished: `heroku config:set GPT_AGENT_MODEL=gpt-realtime-2.1-mini REALTIME_REASONING_EFFORT=minimal LEGACY_REALTIME_KEY=False`.
- v565 (config vars): web startup complete 14:23:10, worker listening 14:23:02, all dynos up. Health 200 with realtime gpt-realtime-2.1-mini. Smoke again: SMOKE_OK, start event voice model gpt-realtime-2.1-mini with reasoning_effort minimal, mint body model gpt-realtime-2.1-mini with reasoning minimal, first conversation unchanged (gpt-realtime-2.1, low). 0 Traceback, H10, R10 or 5xx lines in the last 200 log lines.

Rollback: model only `heroku config:set GPT_AGENT_MODEL=gpt-realtime-mini -a mindsync` (optionally unset REALTIME_REASONING_EFFORT and LEGACY_REALTIME_KEY), or `heroku rollback v564`; code and model `heroku rollback v563` plus a git revert on main.

Open: operator device check (Reflect voice start fresh and seeded, Reflect text, journal voice on gpt-realtime-2.1-mini, first conversation unchanged); posthog-data-extractor next day for reflect_session_started prompt_version/model/reasoning_effort and the voice_session_failed share; next batch RP3-L1, L2, L4 and the first conversation's stored message 0 with memory blocks.
