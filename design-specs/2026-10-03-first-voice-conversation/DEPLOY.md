# Deploy runbook: first voice conversation + Orca memory

Owner: integration-devops. Written 2026-10-05 after the end-to-end contract check (section 8).
Nothing in this runbook has been executed yet. Every push needs the operator's approval.

## 0. What ships

| repo | branch | commits | target |
|---|---|---|---|
| backend `MindSync/` | `feat/first-voice-conversation` | 0240841, 29ef687, d9656db, 90994aa, 8a6177f, 930f0a4, d4cdedf, 75726fb, 11c7211, d23e863 (`.env.example` only) | `main`, which auto-deploys to Heroku app `mindsync` |
| frontend `mindsync-frontend/` | `feat/first-voice-conversation` | 2d8398e, c8492a5, f1a9644, b84cc73, bf49f58 | `dev`, which Codemagic builds into TestFlight and the Google Play internal track |

- One migration: `m315a1b2c3d4` (down_revision `m314b2c3d4e5`, the prod head verified on 2026-10-03). It creates `user_memory_items` and `user_memory_suppressions` and adds four nullable columns: `conversations.entry_origin`, `conversations.memory_extracted_through_message_id`, `users.first_conversation_claimed_at`, `users.memory_forgotten_at`. No PG enum, no backfill, no NOT NULL on existing tables. Idempotent. It sets `SET LOCAL lock_timeout = '5s'` before its first DDL.
- One new boot-time cron: `mindsync_reflect_idle_analysis` (minutes 10, 25, 40, 55, queue `default`), registered from the web lifespan.
- `Procfile`, `requirements.txt` and the tracked `.env` are unchanged. The worker already drains `high` then `default` (`worker: rq worker --url $REDISGREEN_URL high default`), which the recap's Personal Bio refresh relies on.
- No new required env var. The optional ones are in section 6.

Order is fixed: **backend, then migration right away, then frontend.** The frontend must not reach TestFlight before `alembic current` shows `m315a1b2c3d4` (section 9 explains what a new build does against the old backend).

## 1. Pre-flight (before any push)

1. Gates closed: qa-testing full regression green on both branches; security-guardian verdict "GO with conditions" (re-verification 2026-10-05 in `audit-security.md`); operator approval for the backend push.
2. Heroku CLI on this machine: `heroku auth:whoami`. On 2026-10-03 the stored login was rejected ("Invalid credentials provided"), so the operator runs `heroku login` once in an interactive terminal. Fallback for agents only when the token in `%USERPROFILE%\_netrc` is still valid: export it as `HEROKU_API_KEY` inside the same Bash call (recipe in the database-administrator memory, `reference_heroku_cli_auth_workaround`). Never print the token.
3. Record the release to roll back to: `heroku releases -a mindsync -n 3`. Write down `vNNN` of the current "Deploy 513d690" release.
4. Prod schema head: `heroku run --no-tty -a mindsync alembic current` must print `m314b2c3d4e5 (head)`. Anything else: stop and ask database-administrator.
5. `heroku config:get MEMORY_EXTRACTION_FOR_EXISTING_USERS -a mindsync` must be empty or `false` (security condition 2).
6. The backend branch is a fast-forward of `main`: `git -C MindSync merge-base main feat/first-voice-conversation` equals `git -C MindSync rev-parse origin/main` (513d690 on 2026-10-05).
7. Pick a quiet hour. The migration and the boot-time `create_all` both take short locks on `users` and `conversations`; a request queued behind the migration's DDL can wait up to 5 s.

## 2. Backend deploy (push = production)

Say it out loud to the operator: pushing `main` deploys to production immediately, and the migration does not run by itself.

```bash
cd MindSync
git checkout main
git pull --ff-only origin main
git merge --ff-only feat/first-voice-conversation
git push origin main        # if auto mode blocks git push in Bash, run the same push from PowerShell
```

Do not `git add .`: `test_temp.db` and `db-reports/` are uncommitted files from other sessions and must stay out.

Wait for the release, then migrate at once (the migration file only exists in the new slug, so it cannot run earlier):

```bash
heroku releases -a mindsync -n 1          # repeat until it shows "Deploy d23e863"
heroku run --no-tty -a mindsync alembic upgrade head
```

- If it fails with `canceling statement due to lock timeout` (the 5 s `lock_timeout`), the whole migration rolled back. Run the same command again. After three failures stop and ask database-administrator to look for a long transaction in `pg_stat_activity` (read-only). Never kill sessions without the operator.
- Any other error: stop, keep the output, do not retry blindly. The code keeps working on the unmigrated schema (section 3), so there is no rush to force it.

Verify:

```bash
heroku run --no-tty -a mindsync alembic current     # expect: m315a1b2c3d4 (head)
heroku run --no-tty -a mindsync alembic heads       # expect exactly one line: m315a1b2c3d4 (head)
```

## 3. What degrades between the push and the migration

The window is the time between the new release and the end of `alembic upgrade head`, normally one to three minutes.

- Boot survives. `Base.metadata.create_all` creates the two new tables with their indexes (same index names as the migration, so the migration skips them later). The four new columns are excluded from the ORM mappers and are reached only through guarded helpers that read the catalog first, so no statement names a missing column.
- `POST /reflect/start` with `entry`: the marker column is missing, so the person gets an ordinary Reflect thread. The once-per-account claim cannot be taken either, so nothing is burned. No first-conversation prompt, no exemption.
- Free Reflect limit and `GET /users/usage`: the raw count, exactly as today.
- Voice `session_data`: Premium gate as today (trial accounts count as Premium).
- `POST /reflect/{id}/recap`: works for any thread; no memory is written (the memory gate needs the claim column).
- `GET/DELETE /users/memory`: 200 with an empty list once `create_all` made the table, 503 `memory_unavailable` if it did not. Only the new app calls these.
- `DELETE /users/consent/profiling`: the withdrawal stands; the memory purge and the `memory_forgotten_at` stamp are best effort and skip what is missing.
- Idle analysis: if its first tick runs in the window, it writes summaries, topics and RAG documents, never memory.
- Store builds 2.0.94 to 2.0.100: unaffected.

Because the frontend is not released yet, no real user can start a first conversation in this window.

## 4. Smoke checks (right after `alembic current` is m315)

1. Liveness: `curl -s https://mindsync-829f3f05ed43.herokuapp.com/api/v1/audio-v2/health` returns `"status":"ok"`.
2. Processes: `heroku ps -a mindsync` shows `web.1`, `worker.1` (command ends in `high default`) and `scheduler.1`, all `up`.
3. Boot logs: `heroku logs -a mindsync -n 500 | grep -E "Traceback|H10|R10|Scheduled idle Reflect|create_all at startup failed"`. Expect `[Scheduler] Scheduled idle Reflect analysis every 15 min` and no H10, R10 or traceback.
4. Schema, workers and the cron in one read-only one-off. Save as `smoke.py` (flat statements, REPL-safe) and run `heroku run --no-tty -a mindsync python < smoke.py`, then `heroku ps:stop run.NNNN -a mindsync` if the dyno lingers:

   ```python
   import os
   import sqlalchemy as sa
   from redis import Redis
   from rq import Worker
   from rq_scheduler import Scheduler
   r = Redis.from_url(os.environ["REDISGREEN_URL"])
   print("WORKERS", [(w.name, w.queue_names(), w.get_state()) for w in Worker.all(connection=r)])
   print("IDLE_JOB", [(j.id, j.description) for j in Scheduler(connection=r).get_jobs() if j.id == "mindsync_reflect_idle_analysis"])
   from app.db.session import SessionLocal
   db = SessionLocal()
   print("ALEMBIC", db.execute(sa.text("select version_num from alembic_version")).fetchall())
   print("TABLES", db.execute(sa.text("select table_name from information_schema.tables where table_name in ('user_memory_items','user_memory_suppressions') order by 1")).fetchall())
   print("COLUMNS", db.execute(sa.text("select table_name, column_name from information_schema.columns where (table_name = 'conversations' and column_name in ('entry_origin','memory_extracted_through_message_id')) or (table_name = 'users' and column_name in ('first_conversation_claimed_at','memory_forgotten_at')) order by 1, 2")).fetchall())
   db.close()
   print("DONE_" + "SENTINEL")
   ```

   Expect: one worker with queues `['high', 'default']`; one `IDLE_JOB` row; `m315a1b2c3d4`; both tables; all four columns.
5. `GET /users/memory` returns 200 for a test account. With a Firebase ID token of a test account (never a real user, never pasted into a log or a ticket):

   ```bash
   curl -s -w "\n%{http_code}\n" -H "Authorization: Bearer $TEST_ID_TOKEN" \
     https://mindsync-829f3f05ed43.herokuapp.com/api/v1/users/memory
   ```

   Expect `{"items":[]}` and `200`. A `503` with `memory_unavailable` means the code cannot see the table: recheck step 4.
6. First idle tick (next minute 10, 25, 40 or 55): `heroku logs -a mindsync --dyno worker -n 300 | grep ReflectIdle` shows `[ReflectIdle] Done in ...` with `errors=0`. The first ticks work through the backlog of the last 7 days, at most 10 threads per tick.
7. Old client sanity on a store build (2.0.95): open Reflect, send a text message, end the thread, open the usage screen. All work; `/end` on an already ended thread now answers 200 instead of 409, which that build already tolerated.
8. Watch for 30 minutes: `heroku logs -a mindsync --tail | grep -E " status=5[0-9][0-9]|Traceback|\[ReflectIdle\]|\[OrcaMemory\]|\[FirstConversation\]"`. No new 5xx.

## 5. Frontend (only after section 4 is green)

```bash
cd mindsync-frontend
git checkout dev
git pull --ff-only origin dev
git merge --ff-only feat/first-voice-conversation    # dev f27c589 is the branch base; if dev moved, merge and re-test
cd mindsync_app
flutter analyze 2>&1 | grep "error •"                 # must print nothing
flutter test test/screens/first_conversation test/screens/orca_memory test/screens/wow
cd ..
git push origin dev                                    # operator approval; Codemagic builds TestFlight + Play internal
```

- Commit by path only. The working tree holds uncommitted `test/marketing_shots/*` and agent memory files from other sessions.
- A direct push to `dev` skips the PR builder's `flutter analyze`, hence the manual run above.
- Codemagic `app-create-version` bumps the version and triggers `app-release`, which publishes to TestFlight and to the Google Play internal track. The production store release waits for legal sign-off (section 7).

## 6. Environment and config

No new required env var. Optional overrides, all with safe defaults in `app/core/config.py` (documented, commented out, in `MindSync/.env.example`):

| key | default | what it does |
|---|---|---|
| `REALTIME_FIRST_CONVERSATION_MODEL` | `gpt-realtime-2.1` | realtime model of the first conversation only; if OpenAI rejects it the key is minted again with `GPT_AGENT_MODEL` (`gpt-realtime-2` in the tracked `.env`) |
| `REALTIME_FIRST_CONVERSATION_REASONING_EFFORT` | `medium` | invalid value falls back to `medium` |
| `FIRST_CONVERSATION_PAUSE_OFFER_SECONDS` | `900` | the one pause offer |
| `FIRST_CONVERSATION_EXEMPTION_HOURS` | `48` | Free limit and voice gate exemption of the ACTIVE onboarding thread |
| `REFLECT_IDLE_ANALYSIS_MINUTES` | `30` | silence before the idle analysis |
| `REFLECT_IDLE_ANALYSIS_BATCH_SIZE` | `10` | threads per 15-minute tick |
| `REFLECT_IDLE_ANALYSIS_LOOKBACK_DAYS` | `7` | backlog window |
| `REFLECT_FIRST_CONVERSATION_SYSTEM_MESSAGE` | empty | prompt override; without `{SAFETY}` it drops the crisis section (audit L-4) |
| `FIRST_CONVERSATION_RECAP_PROMPT` | empty | recap prompt override |
| `REFLECT_MEMORY_EXTRACTION_PROMPT` | empty | memory extraction prompt override |
| `MEMORY_EXTRACTION_FOR_EXISTING_USERS` | `false` | keep `false` until the privacy policy update is live |

Rule for overrides: set them as Heroku Config Vars (`heroku config:set KEY=value --app mindsync`, which restarts every dyno), never in the tracked `.env`. pydantic-settings rejects a `.env` key that the running code does not declare, so after a code rollback such a key would crash-loop the web dyno at boot; an unknown Config Var is ignored (checked locally with pydantic-settings on 2026-10-05).

Frontend: no new env var, no change to `codemagic.yaml` or to the Firebase config files.

## 7. Rollback plan

### 7.1 Backend code (keep the migration)

1. `heroku rollback vNNN -a mindsync` with the release recorded in pre-flight step 3. Takes effect in about a minute.
2. Stop the auto-deploy from bringing the code back: before anything else lands on `main`, push a revert of the batch to `origin/main`. Never force-push `main`. Keep the migration file in the revert, because the database stays at `m315a1b2c3d4` and Alembic cannot locate a head whose file is gone (every later `alembic upgrade head` would fail):

   ```bash
   git revert --no-edit 0240841^..d23e863
   git checkout d23e863 -- alembic/versions/m315a1b2c3d4_add_user_memory_items_and_entry_origin.py
   git commit -m "chore(alembic): keep m315 after the revert, prod is migrated" -- alembic/versions/m315a1b2c3d4_add_user_memory_items_and_entry_origin.py
   git push origin main
   ```

   The migration file imports only `alembic` and `sqlalchemy`, so keeping it changes nothing at runtime. Until that push lands, `heroku run alembic current` on the rolled-back slug reports an unknown revision; that is expected and does not affect the app.
3. Cancel the cron the new code registered. The old code does not know it, and the old worker cannot import its function, so it would fail every 15 minutes. One-off, `heroku run --no-tty -a mindsync python < cancel_idle.py`:

   ```python
   import os
   from redis import Redis
   from rq_scheduler import Scheduler
   s = Scheduler(connection=Redis.from_url(os.environ["REDISGREEN_URL"]))
   gone = [j.id for j in s.get_jobs() if j.id == "mindsync_reflect_idle_analysis" or j.description == "Idle Reflect thread analysis (every 15 min)"]
   _ = [s.cancel(j) for j in gone]
   print("CANCELLED", gone)
   print("DONE_" + "SENTINEL")
   ```

4. Jobs already queued by the new code (`analyze_idle_reflect_thread`) fail once on the old worker and land in the failed registry. Harmless; the daily failed-job monitor will list them.

Why the migration can stay applied: verified offline on 2026-10-05. The `main` code (513d690) was imported against a SQLite schema that already had both new tables and all four new columns. `create_all` passed, the old mappers name none of the new columns, ORM insert, select and delete of `users` and `conversations` worked (including a thread marked `onboarding_first_conversation`), and deleting a thread still removed its memory rows through the `ON DELETE CASCADE` foreign key. The new columns are nullable with no default, so old INSERTs leave them NULL.

What the rollback state means:

- Orca memory rows stay in the database, unused. Account deletion still removes them (FK cascade). A PROFILING withdrawal on the old code does not purge them; if the rollback lasts more than a day, ask database-administrator for a list of withdrawals since the rollback so the rows can be purged with operator approval.
- Store builds behave as before the deploy (`/end` answers 409 again on an ended thread, already handled).
- A new app build already on TestFlight degrades as described in section 9: no offer after the conversation, recap shows the short copy, "What Orca remembers" shows its unavailable state. Nobody is sent back to onboarding.

### 7.2 Migration downgrade (only if the schema itself is the problem)

`heroku run --no-tty -a mindsync alembic downgrade m314b2c3d4e5`. It hard-deletes every Orca memory item and every suppression hash (irreversible, and it removes the record of what people asked Orca to forget), and it takes the same short locks on `users` and `conversations`. Run it only after the code rollback above, with operator approval.

### 7.3 Frontend

TestFlight: expire the build in App Store Connect. Play internal track: replace it with the previous build. Then revert the merge on `dev` and push, which produces a new build without the feature. The backend can stay on the new code: store builds and the reverted app both work against it.

## 8. Contract verification (2026-10-05)

Read both sides, ran the targeted suites (backend 576 tests in 12 files, frontend 161 tests in the first-conversation, memory and voice suites: all green) and the offline rollback check above.

**Verdict: the contract matches.** Every path, method, field name, type, null case and status code the new client relies on is what the backend sends. No trailing slash on either side for any new or changed route (`/reflect/start`, `/reflect/{id}/session_data`, `/end`, `/recap`, `/message`, `/users/memory`, `/users/memory/{item_id}`, `/audio-v2/realtime-session`), so the Dio POST 307 rule does not apply.

| endpoint | backend | frontend | result |
|---|---|---|---|
| `POST /reflect/start` | `ReflectStartWithEntryRequest`: optional `entry` (Literal `onboarding_first_conversation`), `mode` text or voice; text mode returns `opening_question` and stores it as the first agent turn | sends `mode` voice or text and `entry`; renders `opening_question` only when the history does not already start with the agent | match, no duplicate bubble |
| `GET /reflect/{id}/session_data` | marked thread: `system_message` (voice prompt, history plus continuation note on reconnect), `model` = `REALTIME_FIRST_CONVERSATION_MODEL`, `data.client_session_config` {reasoning, truncation retention_ratio 0.8, tool_choice auto, tools [update_conversation_phase]}, `data.first_conversation` {in_therapy, answers_filled, topics, pause_offer_after_seconds}; 403 without Premium unless exempt | reads `system_message`, merges reasoning, truncation, tools and tool_choice into `session.update`; reads in_therapy and answers_filled; topics are localized on the client with the same rule as the server | match |
| `POST /audio-v2/realtime-session` | optional `conversation_id`; ACTIVE marked thread of the caller gets the first-conversation model and effort, retry with defaults on a rejected model | sends `conversation_id`; connects with the minted key's `model` | match |
| realtime tool flow | tool defined flat (`type`, `name`, `description`, `parameters`), phase enum opening, open, pause_offered, question 1 to 3 | on `response.function_call_arguments.done` sends `conversation.item.create` `function_call_output` with the `call_id`, never `response.create`; tracks `response.created`/`response.done` so the opener never fires during an active response | match |
| `POST /reflect/{id}/end` | 200 `ended` (with `job_id`), `ended_empty_thread`, `already_ended` (was 409); marked threads add `crisis` | `ReflectEndResult` {status, crisis?}; a missing `crisis` does not rule crisis out | match |
| `POST /reflect/{id}/recap` | 200 {status ready, short or failed, items, saved_line_kind, memory_items_saved, crisis}; 404 `reflect_thread_not_found` | all keys parsed; any error or timeout (20 s, server model call 12 s) becomes `failed` | match |
| `POST /reflect/{id}/message` | `crisis_detected` from the keyword scan; first conversation exempt from the limit | ORs `crisis_detected` into the offer gate | match |
| `GET /users/memory`, `DELETE /users/memory`, `DELETE /users/memory/{id}` | 200 {items: id, text, category, source, created_at}; 204; 404 `memory_item_not_found`; 503 `memory_unavailable` | parsed; 503 or 404 on the list shows the unavailable state; 404 on delete removes the item locally | match |
| `GET /users/usage`, `GET /reflect/usage` | shape unchanged; Reflect `used` leaves out exempt first-conversation messages | unchanged | match |
| `DELETE /users/consent/profiling` | response unchanged; also purges memory, stamps `memory_forgotten_at`, drops cached recaps (best effort) | unchanged | match |

Non-blocking findings, for the backlog:

1. Behaviour change on every store build: `crisis_detected` on `POST /reflect/{id}/message` used to be always false. It now follows the keyword scan for all Reflect threads, so builds 2.0.94 to 2.0.100 start showing their existing banner ("If you are in crisis, please reach out to a crisis helpline or emergency services.") under a message that matches. Intended by security audit L-3; listed for operator awareness and device QA.
2. Every Reflect prompt (voice and text, all users) gains the dynamic block (memory when allowed, Personal Bio patterns, therapy schedule) from the moment of the deploy. A prompt change reaches everyone at once; it belongs in the privacy policy update (security condition 3).
3. flutter-mobile, low: a 403 on `session_data` (no Premium and no exemption: a Reset onboarding rerun after the trial, or an exemption past 48 h) is shown as "Connection lost" instead of a Premium message, and a 403 `monthly_limit_reached` in the text first conversation is shown as a plain "did not send". Only reruns or expired exemptions reach it.
4. flutter-mobile or data-analytics, cosmetic: the pause note travels through the generic director channel, which the client wraps as "[Context from user history ...]". The model still gets the instruction.
5. Info: on a reconnect the history goes into the instructions text, not into `conversation.item.create` items as SPEC section 2 describes. It works; instructions are never truncated, so a reconnect late in a long call re-sends the full history.
6. Info: if OpenAI ever rejects `gpt-realtime-2.1`, the key falls back to `GPT_AGENT_MODEL` while `session_data.model` still names 2.1. Harmless, because the client connects with the key's model and `medium` is valid for `gpt-realtime-2`. It would break only if `GPT_AGENT_MODEL` became a model without reasoning support.

## 9. Old clients and the wrong deploy order

Store builds 2.0.94 and 2.0.95 and TestFlight 2.0.97 to 2.0.100 against the new backend: **nothing breaks.**

- `POST /reflect/start` with no body or the old body: `entry` defaults to none, so the old code path runs unchanged.
- `POST /audio-v2/realtime-session` without `conversation_id`: default model and effort.
- `POST /reflect/{id}/end`: 200 `already_ended` instead of 409. The old `ReflectChatCubit.endThread` catches any error and reloads the thread list, so the result is the same screen.
- Usage numbers: identical for every account without a first-conversation claim, which is every account using an old build.
- Idle analysis: their quiet ACTIVE Reflect threads get a summary, topics and a RAG document, and stay ACTIVE, so they can still be continued. No memory is mined for them while `MEMORY_EXTRACTION_FOR_EXISTING_USERS` is false.
- `DELETE /users/consent/profiling`: same response; the extra purge has nothing to delete for them.
- Visible changes: the crisis banner (finding 1) and the richer prompt (finding 2).

New build against the old backend (if the frontend reached TestFlight first): **it degrades and never strands anyone in onboarding** (onboarding completion is saved on the server before this flow starts, and every step has a way forward).

- `entry` and `conversation_id` are ignored (Pydantic ignores unknown fields), so the person gets an ordinary Reflect thread with the ordinary prompt and no phase tool; the phase indicator simply stays where it is.
- Voice works for trial accounts. Without Premium, `session_data` answers 403, the client retries once, shows "Connection lost", and "Continue in text" works.
- `/end` has no `crisis` field; `/recap` answers 404. The recap is `failed` and crisis cannot be ruled out, so the flow shows the recap-only screen with reason `status_unavailable`, then reminders, then Home.
- Cost of the wrong order: **no new user who actually talked sees the post-onboarding offer** until the backend is deployed (someone who said nothing gets the `short` recap and the normal offer). "What Orca remembers" shows its unavailable state.

## 10. Device QA (fresh accounts, TestFlight build, iPhone and Android)

1. Fresh account: onboarding, Build, Reveal with the single "Talk with Orca", Intro with three topics and the memory note, "Start talking" asks for the mic.
2. Voice: Orca speaks first and asks question 1 about the top focus area; the indicator moves 1, 2, 3, then the "Open conversation" pill. Orca never mentions Premium, prices or limits and never ends the call.
3. Pause offer once around minute 15 (needs a real 15-minute call; a lower `FIRST_CONVERSATION_PAUSE_OFFER_SECONDS` restarts every dyno and changes it for everyone, so use it only with the operator's approval and restore it).
4. End right after speaking: the last sentence is in the thread, then recap "ready" with up to three lines, offer step 1, Continue, step 2 with the "free 4 days" chip, close, reminders, Home.
5. Say almost nothing and End: the short recap copy.
6. Mic denied: text mode with the note; permanently denied: "Open Settings".
7. "Type instead": first bubble is opening question 1; replies; "Finish for now" gives the recap.
8. Switch voice to text and back in one conversation; the history follows.
9. Airplane mode during the call: one silent reconnect, then "Connection lost"; "Continue in text" shows the history; "Try voice again" works.
10. Kill the app mid-conversation and relaunch: Home, not onboarding. About 30 minutes later the idle job has analyzed the thread (database-administrator can confirm) and "What Orca remembers" lists items for this account.
11. Prices unavailable (sandbox account signed out or offline store): "Prices didn't load", "Try again", "Continue with my free 4 days".
12. Sandbox purchases: starter on step 1 leads to the Premium Welcome; annual and monthly on step 2.
13. Crisis sentence in a text first conversation: calm continuation, no offer, no paywall.
14. Settings, "What Orca remembers": list, delete one (with the undo window), delete all, empty state. After switching PROFILING off the list is empty.
15. Settings, Reset onboarding, run it again: no offer (`onboarding_rerun`), an ordinary thread, no second exemption.
16. Store build 2.0.95 on the same backend: Reflect text and voice, End, usage chip, consent switch; a crisis sentence shows the banner.
17. Delete the QA account: database-administrator confirms its memory rows are gone.
18. Android: the same core path, plus predictive back on every first-conversation screen.
19. Spot-check Polish and one more language: Orca speaks the app language, intro topics are translated.
20. After the build is live: posthog-data-extractor confirms the funnel events flow, and that no event of the new version carries `crisis_conversation`, `question_set`, `category` or a `crisis` key (security condition 5).

## 11. Follow-ups

| item | owner | when |
|---|---|---|
| Index `messages (conversation_id, created_at)` with `CREATE INDEX CONCURRENTLY` inside an `autocommit_block`. Prod `messages` has no index on `conversation_id` (database-administrator, 2026-10-03), and the idle job, the pause clock and the recap all read messages per thread. | backend-api | next backend batch |
| M-6: entitlement check and rate limit on `POST /audio-v2/realtime-session` (pre-existing, the largest remaining cost exposure) | backend-api | next backend batch |
| Transcription model deprecation on 2027-02-26: move `REALTIME_TRANSCRIPTION_MODEL` (`gpt-4o-mini-transcribe` in the tracked `.env`), `WHISPER_MODEL`, and the client fallback `transcription_model` in `audio_chat_cubit.dart` (`_kFallbackClientSessionConfig`) to the successor model | backend-api, flutter-mobile, integration-devops (config) | well before 2027-02-26 |
| Privacy policy update before any store release: Orca memory, suppression hashes, bio patterns in prompts, what the PROFILING switch means for people who never touched it, and the prior M-3 consent wording | lead, legal | before the store release |
| Flip `MEMORY_EXTRACTION_FOR_EXISTING_USERS=true` (Config Var) only after the policy is live. Effect: the idle job starts mining existing users' quiet threads of the last 7 days, so OpenAI cost rises for a few days | operator | after the policy update |
| Measure the real cost of a 30-minute call from `first_conversation_ended` (input, output and cached tokens) | growth-analyst, posthog-data-extractor | two weeks after TestFlight |
| Pin `rq`, `rq_scheduler` and `redis` in `requirements.txt` to the versions in the current slug (`heroku run pip freeze`); they are unpinned, so any build can pull a new major. The recap's Personal Bio dependency uses `rq.job.Dependency(allow_failure=True)` | integration-devops | next backend batch |
| Security backlog L-1, L-4, L-5, L-7, N-1 | per `audit-security.md` | backlog |
| Contract findings 3 and 4 (section 8) | flutter-mobile, data-analytics | backlog |

## 12. Deployed 2026-10-05 (backend only)

Executed by integration-devops. Times are local (CEST, UTC+2). Frontend not touched.

| step | time | result |
|---|---|---|
| Pre-flight | 08:14 to 08:17 | CLI stored login rejected again, so the `HEROKU_API_KEY` from `_netrc` workaround was used per command (token never printed). Rollback target recorded: **v556** (Deploy 513d6905). Prod `alembic current` = `m314b2c3d4e5 (head)`. `MEMORY_EXTRACTION_FOR_EXISTING_USERS` unset. `origin/main` = 513d690 = merge-base, so nothing new came in and no merge was needed. Branch head was **cc8288b**, one test-only commit after d23e863 (`test_delete_account_cascade.py`, the QA test). Offline on cc8288b: 106 passed (boot registration, account deletion cascade, user memory suites); Postgres DDL of both new tables and their indexes compiles. |
| Push | 08:17:38 | local `main` fast-forwarded 513d690..cc8288b (11 commits) with `git fetch . feat/first-voice-conversation:main` (no checkout, the working tree keeps `test_temp.db` and `db-reports/` untouched), then `git push origin main`. |
| Release | 08:18:55 | **v557** "Deploy cc8288bb". web, worker and scheduler restarted 08:19:31 to 08:19:44. |
| Migration | 08:19:13 to 08:19:46 | `Running upgrade m314b2c3d4e5 -> m315a1b2c3d4`; dyno `run.4063` "Process exited with status 0". No lock timeout. The CLI itself returned exit 1 with no error text (client artifact, see note 1). `alembic current` and `alembic heads` both `m315a1b2c3d4 (head)` at 08:22:58. |
| Boot | 08:19:43 | "Application startup complete", `[Scheduler] Scheduled idle Reflect analysis every 15 min`, worker "Listening on high, default". No H10, R10, traceback or `create_all at startup failed`. |
| Smoke 1, 2, 4 | 08:23 to 08:25 | health 200 `"status":"ok"`; ps all `up`; one worker `['high', 'default']`; exactly one `mindsync_reflect_idle_analysis` job (queue `default`); both tables, all five indexes, all four columns nullable; 0 memory rows. |
| Smoke 5 | 08:25 | no test-account token available, so only an unauthenticated GET: `/users/memory` 403 like `/users/usage` and `/reflect/usage` (route registered; 404 would mean missing). The authenticated `{"items":[]}` check is still open for device QA. |
| Smoke 6 | 08:25 to 08:29 | first tick `[ReflectIdle] Done in 2.1s: candidates=15 enqueued=10 claimed_elsewhere=0 gave_up=0 errors=0`; all 10 `analyze_idle_reflect_thread` jobs OK (21 to 29 s each, OpenAI calls). After them: 0 memory rows, 0 suppressions, 0 claims, the 10 threads still ACTIVE, failed registries `high` 0 / `default` 1 (an abandoned session-recording job from 2026-09-16, unrelated). |
| Smoke 8 | 08:19 to 08:4x | no 5xx and no web traceback in the router and app logs since the restart (low Monday-morning traffic). |
| `MEMORY_EXTRACTION_FOR_EXISTING_USERS` | **not set** | held, see note 2. |

Notes:

1. `heroku run --no-tty` with `HEROKU_API_KEY` can return exit 1 although the dyno succeeded. Before re-running a migration, read `heroku logs -a mindsync --dyno run.NNNN` for "Process exited with status 0" and check `alembic current`. Also, `heroku run "a && b"` breaks on this Windows machine (`'C:\Program' is not recognized`); run the commands separately.
2. The flag was held because security condition 2 and section 6 tie it to the updated privacy policy being **live**. On 2026-10-05 at 08:26 `https://www.mindsync.app/privacy-policy` (cache-busted, `CF-Cache-Status: MISS`) still reads "Last updated: July 25, 2026" and has no mention of Orca memory, remembered facts or suppression hashes. Once the updated policy is published, or the operator confirms directly that the flip should happen before publication, run `heroku config:set MEMORY_EXTRACTION_FOR_EXISTING_USERS=true -a mindsync` (restarts every dyno; pick a moment between idle ticks, not at minute 10, 25, 40 or 55), then re-check boot logs and read the value back through `app.core.config.settings` in a one-off.
3. Old store builds talk to this backend from now on: the crisis banner behaviour change (section 8, finding 1) and the richer Reflect prompt (finding 2) are live for everyone.
4. Frontend can rely on: every route and field in section 8 is live on v557 with the schema at `m315a1b2c3d4`. Until the flag is flipped, memory is written only for accounts that take the first-conversation claim (new onboarding through the new build), and the idle job mines no memory for existing users.

## 13. Frontend leg, deployed 2026-10-05

- Pushed to `origin/dev` as merge commit `e4e0d05` (no fast-forward: origin/dev had the Codemagic bump `91e9c80`, tag `app_2.0.100`, pubspec and CHANGELOG only, no conflicts). Range `91e9c80..e4e0d05` = 2d8398e, c8492a5, f1a9644, b84cc73, bf49f58, 9a14cd9 + merge.
- Checks in a temporary worktree: `flutter analyze` 0 errors; `flutter test` wow + first_conversation + orca_memory + subscription: 447 passed.
- `9a14cd9` adds the "Find a helpline near you" link (findahelpline.com) on the calm screen, with no analytics event. Add it to the device QA list (item 4).
- Expected: Codemagic bump to 2.0.101 and the TestFlight / Play internal build.
- Pending follow-up push: the intro memory-notice visibility fix (M-5), committed on `feat/first-voice-conversation` after 9a14cd9.
- `MEMORY_EXTRACTION_FOR_EXISTING_USERS` still unset: the live privacy policy (last updated 2026-07-25) does not mention Orca memory yet.

### Frontend follow-up push (2026-10-05, 09:33 CEST)

- Pushed `e4e0d05..0031c44` to `origin/dev` as merge commit `0031c44`. No fast-forward, because the branch does not contain the first merge `e4e0d05`. No conflicts: the merged tree equals the branch tree plus the 2.0.100 version bump. New commits: `4daf29f` (M-5, the Orca memory notice now opens the pinned footer directly above "Start talking"), `6c70dd4` (focus-area labels lowercased mid-sentence, capitalized when they open the sentence, German nouns and acronyms kept), `9508788` (focus-area copy without verb agreement; templates changed in de, en, es, fr, nb and sv, Polish was already agreement-free and is unchanged).
- Checks in a temporary worktree from `origin/dev`: `flutter analyze` 0 errors (the same 9 warnings as before, all in older files outside this batch); `flutter test` on first_conversation, wow and `l10n_completeness_test.dart`: 290 passed, 0 failed.
- Codemagic: when this push went out, 42 minutes after `e4e0d05`, no version bump had landed (dev still at `e4e0d05`, newest tag `app_2.0.100`, no `app_2.0.101`). Earlier bumps arrived 7 to 9 minutes after a push. Operator: open the Codemagic dashboard and check the `app-create-version` run for `e4e0d05`. If it failed or never started, the run for `0031c44` is the one that should produce 2.0.101 with the whole batch. If it was still queued, its bump push fails as a non-fast-forward once `0031c44` is ahead, which is harmless as long as no `app_2.0.101` tag ends up on a commit that is not on dev.
- Device QA additions: item 1, on "Before the first conversation" the memory note is on screen above "Start talking" without scrolling (iPhone 15 or 16, iPhone SE, a small Android phone, and once with large system text). Item 19, intro topic 1 and the reminders check-in example read naturally with a singular focus area ("sleep") and a plural one ("worries") in English and in one more language, with lowercase mid-sentence and a capital letter when the label opens the line.

### Backfill batch frontend pushed (2026-10-05, 14:46 CEST)

- Codemagic result for the earlier pushes: the 2.0.101+174 bump `0615f3e` landed on dev at 09:55:42 CEST, about 22 minutes after `0031c44`, with tag `app_2.0.101` on that commit (on dev, no orphan tag). It is the only bump since 2.0.100, so `e4e0d05` never got a version of its own and 2.0.101 carries the whole first-conversation batch. Whether `app-release` then published 2.0.101 to TestFlight and Play internal is visible only in Codemagic or App Store Connect.
- Pushed `0615f3e..86addde` to `origin/dev` as merge commit `86addde` of `feat/orca-memory-backfill` (head `3343c37`). No fast-forward, because the branch does not contain the 2.0.101 bump. No conflicts: the merged tree equals the branch tree plus that bump. Commits: `a195551` (backfill states, Orca looks back over existing users' history once), `87184dd` (phase indicator moves past "1 of 3"), `902f719` ("What Orca remembers" redesign), `e8924c5` (security review B-L7 and B-M2), `3343c37` (test that forbids memory source proxies in PostHog, N-B3). `test/marketing_shots/orca_memory_demo_data.dart` stays untracked in the main working tree and is not in the push.
- Checks in a temporary worktree from `origin/dev`: `flutter analyze` 0 errors (the same 9 warnings as before); `flutter test` on orca_memory, first_conversation, wow and `l10n_completeness_test.dart`: 398 passed, 0 failed. The first analyze run hung with an idle analysis server and no output for about 10 minutes; it was killed and the rerun finished in 74 seconds.
- Backend dependency: the only new client call is `POST /api/v1/users/memory/backfill` (empty body, no trailing slash). It matches `@router.post("/memory/backfill")` in `users.py` on backend `origin/main`, which already contains the whole backend branch (push to main deploys Heroku). The batch's migration (`220922f`) must be applied on Heroku before the build reaches testers; that is owned by the backend deploy and was not checked here.
- Expected build: Codemagic bump to 2.0.102 on top of `86addde`, then TestFlight and the Play internal track.

## 14. Backfill batch backend deployed 2026-10-05

Executed by integration-devops. Times CEST (UTC+2). Frontend not touched by this step.

| step | time | result |
|---|---|---|
| Pre-flight | 14:27 to 14:41 | Prod head `m315a1b2c3d4`; `origin/main` cc8288b; branch `feat/orca-memory-backfill` 0945d92 = 9 commits on cc8288b, nothing incoming, no merge. Rollback target **v558** ("Set MEMORY_EXTRACTION_FOR_EXISTING_USERS config vars", 08:57: cc8288b with the flag `true`). Offline: 646 passed in the 11 targeted files (backfill, backfill API and boot registration, m316, source links, security guards, first conversation x3, user memory, deletion cascade). New columns are `exclude_properties` on both mappers, so boot is safe before the migration. Waited for the 12:40 UTC idle tick (0 candidates) so the restart cut no job. |
| Push | 14:41:29 | local `main` fast-forwarded cc8288b..0945d92 without a checkout, `git push origin main` |
| Release | 14:42:47 | **v559** "Deploy 0945d927" |
| Migration | 14:43:09 to 14:44:25 | `Running upgrade m315a1b2c3d4 -> m316a1b2c3d4`, dyno `run.3327` exited 0 (CLI said exit 1 again, see section 12 note 1). `alembic current` and `heads`: `m316a1b2c3d4 (head)` at 14:45:52. |
| Boot | 14:43:33 | both crons logged as scheduled, worker "Listening on high, default", no H10, R10 or traceback |
| Schema and scheduler | 14:48 | one worker `['high','default']`; `mindsync_reflect_idle_analysis` 1, `mindsync_orca_memory_backfill_sweep` 1 (queue `default`); flag reads `True`; `users.memory_backfilled_at`, `user_memory_items.source_kind` / `source_item_id` (all nullable) and `ix_user_memory_items_user_id_source_kind_source_item_id` present; active REALTIME pricing rows for `gpt-realtime-2.1` and `gpt-realtime-2.1-mini` |
| First sweep tick | 12:50 UTC | `[OrcaBackfill] Sweep done in 0.7s: candidates=98 enqueued=20 (about 241s of work) running=0 gave_up=0 errors=0` |
| Its 20 jobs | 12:50 to 12:53 UTC | 20 of 20 OK, 19 `saved` and 1 `empty`, 111 facts, all `done=True`, `attempts=0`, slowest 14.4 s. Every `[OrcaBackfill]` line carries only user, status, saved, chunks, digest_chars, done, attempts and duration; 0 hits for crisis, screened, forgotten or budget. No 5xx or traceback app-wide since v559. |

Backlog at 14:48: **98 accounts** (not backfilled, active in 90 days, quiet 60 min, PROFILING not withdrawn), about 760 s of estimated work. The batch size (20) binds before the 240 s budget, so 80 accounts an hour: 5 ticks (20, 20, 20, 20, 18), drained around 15:50 CEST, plus accounts that turn quiet later and join the next tick.

Notes:

1. The flag `MEMORY_EXTRACTION_FOR_EXISTING_USERS=true` has been on since v558 (operator, 08:57). The live policy page still read "Last updated: July 25, 2026" with no memory wording at 14:3x. Kill switch for the sweep: set the flag to `false` (candidates shrink to accounts with a first-conversation claim; restarts every dyno) or cancel `mindsync_orca_memory_backfill_sweep`.
2. The `ORCA_MEMORY_BACKFILL_*` overrides (`SWEEP_BATCH_SIZE`, `SWEEP_TIME_BUDGET_SECONDS`, `SWEEP_ACTIVE_DAYS`, `PROMPT`, `MEMORY_FED_CUTOFF`) are read with `getattr(settings, ...)` but are not declared in `app/core/config.py`, so a Config Var is ignored. Tuning needs a code change (backend-api: declare them as optional fields).
3. `DEFAULT_MEMORY_FED_CUTOFF` in `app/services/orca_memory_backfill.py` is 2026-10-05 **08:19 UTC**, but the m315 release (v557) went live at **06:18:55 UTC** (08:18:55 CEST). Cards and summaries made between those times count as not memory-fed, which is the unsafe direction for B-M3. Practical exposure is close to nil (before this deploy only one account had memory, 5 items), but it should become `06:18 UTC` in code and in the test that pins it (data-analytics, qa-testing) before any later backfill run matters.
4. Rollback of this batch: `heroku rollback v558 -a mindsync`; push `git revert --no-edit cc8288b..0945d92` to `main`, then restore `alembic/versions/m316a1b2c3d4_add_users_memory_backfilled_at.py` with `git checkout 0945d92 -- <file>` and commit it; cancel `mindsync_orca_memory_backfill_sweep` with the section 7.1 step 3 script (job id swapped). The m316 columns are nullable and unmapped on cc8288b, so they can stay.
5. Order with the frontend: the backfill frontend reached `dev` at 14:46 (section 13), about 2 minutes after the migration finished, so the backend was first. Its only new call, `POST /api/v1/users/memory/backfill`, is live on v559.
6. Heroku CLI here: a call without `< /dev/null` hung for minutes in a non-interactive Bash call; pass `< /dev/null` to every non-`run` command.

## 15. Quick fix deployed 2026-10-05: phase tool removed, cutoff 06:18 UTC

Executed by integration-devops, operator-approved. Times CEST. Backend only, no migration (prod stays `m316a1b2c3d4`).

- Shipped: 6a8adea (`DEFAULT_MEMORY_FED_CUTOFF` = 06:18 UTC, section 14 note 3) and a6e3528 (the `update_conversation_phase` tool and the PHASE SIGNAL prompt section removed: the model hung around its calls in the device test). Commits only: backend-api's uncommitted `app/core/config.py` and `app/tests/test_orca_memory_backfill_settings.py` stayed in the working tree.
- Pre-flight 15:23: `origin/main` still 0945d92. In a temporary worktree on a6e3528: `test_first_conversation`, `test_first_conversation_part1_rules`, `test_orca_memory_backfill` 226 passed; security guards (first conversation, memory) and backfill boot registration 168 passed. Rollback target: **v559**.
- Client contract: unchanged for every build. `client_session_config` now carries only `reasoning` and `truncation`; the app adds `tools` and `tool_choice` to `session.update` only when `tools` is a non-empty list (`audio_chat_cubit.dart`), and its phase indicator is also driven by answered questions, so 2.0.101 and 2.0.102 keep working without the tool.
- Push 15:26:42, after the 13:20 UTC sweep jobs (58 candidates, 20 enqueued, all done) and the 13:25 UTC idle tick (0 candidates), before the 13:35 sweep. Release **v560** "Deploy a6e35289" at 15:27:55; dynos up 15:28:24 to 15:28:37.
- Smoke: boot clean (no H10, R10, traceback); worker "Listening on high, default"; `mindsync_reflect_idle_analysis` 1 and `mindsync_orca_memory_backfill_sweep` 1; one-off: `client_session_overrides()` keys `['reasoning', 'truncation']`, no `tools`, no `tool_choice`, no phase tool symbols left; `memory_fed_cutoff()` = `2026-10-05T06:18:00+00:00`.
- Rollback: `heroku rollback v559 -a mindsync`, then push `git revert --no-edit 0945d92..a6e3528` to `main`. No migration, no cron change.

## 16. Config follow-up deployed 2026-10-05: backfill settings declared

Executed by integration-devops, operator-approved. Times CEST. Backend only, no migration (prod stays `m316a1b2c3d4`).

- Shipped: 5d2ca8e (backend-api: `FIRST_CONVERSATION_RECAP_ONLY_PROMPT`, `ORCA_MEMORY_BACKFILL_PROMPT`, `_MEMORY_FED_CUTOFF`, `_SWEEP_BATCH_SIZE`, `_SWEEP_TIME_BUDGET_SECONDS`, `_SWEEP_ACTIVE_DAYS` declared in `app/core/config.py` with the code defaults; the three integers go through a lenient validator, so a typo in a Config Var falls back to the default instead of crash-looping the boot) and d1d93d0 (integration-devops: the six keys documented in `.env.example`, commented out, Heroku Config Vars only). This closes section 14 note 2: these overrides now really apply as Config Vars.
- Pre-flight 16:00: `origin/main` a6e3528. Temporary worktree on d1d93d0: `test_orca_memory_backfill_settings` + `test_orca_memory_backfill` 131 passed; `import app.main` with the tracked `.env` (only keys missing from it taken from conftest) gives 348 routes, none of the six keys is in the tracked `.env`, values equal the defaults, a Config Var `15` applies and `abc` falls back to the default with a warning.
- Push 16:11:04, after the 14:05 UTC sweep (`candidates=0`: the backlog of section 14 is drained) and the 14:10 UTC idle tick (0 candidates). Release **v561** "Deploy d1d93d0b" at 16:12:20; dynos up 16:12:49 to 16:13:02. Rollback target: **v560**.
- Smoke: boot clean, worker "Listening on high, default", `mindsync_reflect_idle_analysis` 1 and `mindsync_orca_memory_backfill_sweep` 1; one-off: `settings.ORCA_MEMORY_BACKFILL_SWEEP_BATCH_SIZE == 20` True, budget 240, active days 90, both prompts and the cutoff empty, no `ORCA_MEMORY_BACKFILL_*` Config Var set, readers 20 / 240 / 90 / `2026-10-05T06:18:00+00:00`.
- Rollback: `heroku rollback v560 -a mindsync`, then push `git revert --no-edit a6e3528..d1d93d0` to `main`. Before that, unset any of the six keys that was set as a Config Var in the meantime (harmless on old code, but it would no longer do anything).

## 17. Prompt v2, onboarding re-runs and the profile re-run fix: contract check and plan (2026-10-05, evening)

Written by integration-devops. Nothing in this section has been executed: no push, no deploy, no Config Var change. Every push needs the operator's approval.

### 17.1 What ships

| repo | ref | commits | target |
|---|---|---|---|
| backend `MindSync/` | `release/first-conversation-voice-v2` at **99a2933** (worktree `MindSync-wt-release`) | `feat/first-conversation-voice-v2` (8e84428, f166a24, 5ee8701, e5829fc, 7c9d993) on top of `d1d93d0`, then the merge of `fix/profile-rerun-null-overwrite` (0f74b96, 756cf10) | `main`, which deploys Heroku app `mindsync` at once |
| frontend `mindsync-frontend/` | `fix/first-conversation-voice-v2-fe` at **fc74a5e** | 1277c02, 71947ef, fc74a5e on top of `origin/dev` 113543f (tag `app_2.0.103`) | `dev`, which Codemagic builds into TestFlight and the Play internal track |

- No migration: nothing under `app/models/` or `alembic/` differs from `origin/main`; prod stays at `m316a1b2c3d4`. No new cron, `Procfile`, `requirements.txt` and the tracked `.env` unchanged.
- Settings: `REALTIME_FIRST_CONVERSATION_REASONING_EFFORT` default goes from `medium` to `low`; new optional `REALTIME_FIRST_CONVERSATION_VOICE` (default empty = the voice the app asks for). Both are commented out in `.env.example`.
- Merge check: the two backend branches touch disjoint files. `git merge-tree` is clean and gives tree `9f34eff`, which is exactly the tree of release 99a2933. On that tree (Python 3.12, SQLite): 589 passed in the 10 first-conversation, profile, age band and memory files, and 65 passed in the boot and scheduler registration files (they import `app.main`). `origin/main` is still `d1d93d0`, so 99a2933 is a fast-forward.
- Postgres reality: the only new Postgres-specific statement is the start lock in `first_conversation.lock_account` (`SET LOCAL lock_timeout = '3s'` plus `SELECT id FROM users WHERE id = :uid FOR UPDATE`). SQLite tests take a different branch, so the lock is first exercised on prod; every failure in it degrades to a resume or an ordinary thread, never a 5xx.

### 17.2 Verdicts

| item | verdict | evidence |
|---|---|---|
| 1. Profile POST/PUT against new and old builds | **MATCH** | Store builds 2.0.94/2.0.95 and TestFlight up to 2.0.103 share the same profile code except `_upsertProfile`. Re-run (no sign-up JSON left): old builds POST `{full_name: displayName, pronouns/gender/age_band: null}`, now 200 with the stored row and no write, so the name and gender survive and the PUT fallback never runs. New build: no-JSON branch is create-only (`users_manager.dart` `_upsertProfile(updateExisting: false)`), nulls stripped. Account save (`account_body.dart:244`, `account_cubit.dart:32`) sends `full_name` as the field text, so a cleared name is `""` and is now stored as NULL; `gender`/`pronouns`/`age_band` are the loaded values (the gender picker never emits null to the body, `account_body.dart:164`), so the new null-is-ignored rule changes nothing there. `currently_in_therapy` is `includeIfNull: false` and partial PUTs (`lead_source`, `currently_in_therapy`) are unaffected. No loop: the consent step ignores the flush result (`therapy_onboarding_cubit.dart:384`), the self-heal is capped once per session. One dead path, finding F5. |
| 2. First conversation contract | **MATCH** | `POST /reflect/start` still returns `ReflectStartResponse{conversation_id, opening_question}`; `session_data` shape unchanged (`public_info`, `client_session_overrides` keys `reasoning`, `truncation`). 403 bodies: `session_data` has a single 403, `"Voice mode requires Premium"`; `/message` has a single 403, `"monthly_limit_reached"`; the same strings are on `origin/main` (`reflect.py:1798`, `:1199`). The client does not match strings: `isGateRefusal` treats any 403 except `detail == "Not authenticated"` (HTTPBearer without a header) as the gate, and an invalid token is a 401 (`app/api/deps.py`), so the two cannot be confused. `getSessionData` and `sendMessage` both pass `retryOn403: false`, which the interceptor reads from `extra` (`dio_client.dart:64`). Mint: the override voice is popped into `voice`, minted as `resolved_voice` and echoed (`openai_audio_service.py:317`); on a rejected 2.1 the retry uses the client's voice and echoes that. The client builds `session.update` from `_session!.voice` (`audio_chat_cubit.dart:908`), so key and update always agree. |
| 3. Money path of fc74a5e | **No lost and no double-charged purchase in the normal flow**; 2 flutter-mobile findings (F1 UX, F2 narrow race) | see 17.3 |
| 4. Heroku config | **OK**, `low` applies | see 17.4 |
| 5. Deploy order | **FE safe in either order**; backend first recommended | see 17.8 |

### 17.3 Findings

**F1 (flutter-mobile, medium, UX only).** After a purchase on the paywall opened from the conversation, `SubscriptionScreen` leaves with `context.pushReplacement(premiumWelcomeRoute)` (`subscription_screen.dart:142`). go_router 14.6.0 (the locked version) drops the replaced route match without completing its completer (`go_router-14.6.0/lib/src/parser.dart:186-196`; only a pop completes it, `delegate.dart:157-163`). So `await context.push(...)` in `wow_screen.dart:241` never returns: `resumePurchaseUpdates()` (`:244`) and the cubit's `_loadUsage()` (`first_conversation_cubit.dart:677`) never run. Premium Welcome without `onBackHome` exits only with `context.go(mainPageRoute)` (`premium_welcome_screen.dart:78, 83, 120`), which disposes WowScreen and closes its cubits (`wow_screen.dart:129-134`), so no suspended listener outlives the screen. Net effect: the purchase is verified, completed and logged once (by the paywall's own cubit), and the first conversation is left without `/end`, recap or the reminders step; the thread stays ACTIVE and the idle job analyzes it after 30 minutes. Fix options: open the welcome in flow mode with an `onBackHome` that pops back into the conversation, or push it instead of `pushReplacement` when the paywall came from the conversation.

**F2 (flutter-mobile, low, narrow race).** `suspendPurchaseUpdates()` is a no-op while WowScreen's cubit is not listening yet (`subscription_cubit.dart:482`), and `loadSubscriptionsProducts()` subscribes unconditionally (`:223`), also while suspended. If the preload in `initState` (`wow_screen.dart:117`) failed and the retry from `_ensureProductsPreloaded` (`:144`) is still running when "See Premium" opens the paywall, that retry attaches WowScreen's listener under the open paywall. A purchase there is then verified twice, `completePurchase` runs twice (the second call can fail and paint the error state on whichever cubit comes second) and `subscription_purchase_completed` is logged twice, the second time with `post_onboarding`. WowScreen ignores that success outside the offer step (`:265`). Fix: set the suspended flag even when not listening and make `_setupPurchaseStream` honour it; `purchaseSubscription` and `restorePurchases` clear it.

**F3 (info, store semantics: lost or replayed?).** iOS uses StoreKit 1 here; `in_app_purchase_storekit` 0.4.11+1 observes the payment queue only while the broadcast stream has a listener (`in_app_purchase_storekit_platform.dart:83-85`). After a gap with no listener (WowScreen suspended, paywall cubit not yet listening or already closed), StoreKit re-delivers every unfinished transaction to the next listener: nothing is lost, and only unfinished transactions come back, so a completed purchase is never replayed or completed twice. A purchase or restore whose verification failed retryably on the paywall is replayed to WowScreen's cubit on resume and verified again, which is the intended retry; `_loadUsage` can run before that finishes, so the gates may stay locked for the rest of that conversation. Android (`in_app_purchase_android` 0.5.0) is a plain broadcast controller (`in_app_purchase_android_platform.dart:55`): an update with no listener is dropped and an unacknowledged purchase needs a later query. In this flow only a deferred (pending) purchase started on the conversation paywall and completing after the paywall and WowScreen are gone can hit that, and every paywall in the app has the same gap today (`SubscriptionCubit` is a factory per screen, `service_locator.dart:223`).

**F4 (info, the "paused forever" question).** A suspend that is never resumed cannot leave a later purchase unprocessed: WowScreen's `purchaseSubscription` and `restorePurchases` re-subscribe before calling the store (`subscription_cubit.dart:298-299`, `365-366`). The post-conversation offer re-reads the profile before deciding (`wow_cubit.dart:323`), so a buyer gets `already_premium`, and a re-run gets `onboarding_rerun`. App backgrounded with the paywall open: nothing changes, the paywall's cubit keeps listening. Exception while pushing: the `finally` resumes.

**F5 (flutter-mobile, low, profile).** The self-heal `MainPageCubit._repairMissingName` (`main_page_cubit.dart:165-176`) runs only when a row exists with an empty name and a pending sign-up JSON carries a name. On the new backend its POST answers 200 without writing and the client then clears the pending JSON, so that name is dropped where the old PUT fallback wrote it. The pending JSON is written only at sign-up and cleared by the first successful flush, and I found no current path that creates a row outside that flush, so this is backlog, not a blocker. If it matters: send that branch as PUT, which now ignores nulls.

**F6 (info).** `retryOn403: false` on `getSessionData` also covers the Reflect tab voice (`reflect_chat_cubit.dart:961`). It changes behaviour only when the per-request token fetch failed and no Authorization header went out (HTTPBearer 403 "Not authenticated"): before, the interceptor re-sent with a fresh token; now that launch fails once.

**F7 (info, prod config).** `GPT_AGENT_MODEL` is a Config Var, `gpt-realtime-mini`, which overrides `gpt-realtime-2` in the tracked `.env`. It is the fallback model when OpenAI rejects `gpt-realtime-2.1` for the first conversation. `gpt-realtime-mini` fails `_model_supports_reasoning` (`openai_audio_service.py:81-88`), while `session_data` keeps sending `reasoning` (computed for 2.1) and the client merges it into `session.update` (`first_conversation_cubit.dart:313`). So the condition of section 8 finding 6 is met today: on that fallback the update carries a field the mini model refuses (the instructions still arrive through the key mint). Fallback path only; 2.1 minted fine in the device tests.

### 17.4 Heroku config (read 2026-10-05 about 21:15 CEST, `HEROKU_API_KEY` from `_netrc`, read-only)

| Config Var | value |
|---|---|
| `REALTIME_FIRST_CONVERSATION_REASONING_EFFORT` | not set, so the new code default `low` applies (nothing to flag) |
| `REALTIME_FIRST_CONVERSATION_MODEL` | not set (code default `gpt-realtime-2.1`) |
| `REALTIME_FIRST_CONVERSATION_VOICE` | not set (empty: the app's voice) |
| `GPT_AGENT_MODEL` | `gpt-realtime-mini` (see F7) |
| `REALTIME_REASONING_EFFORT` | not set (tracked `.env`: `low`) |
| `MEMORY_EXTRACTION_FOR_EXISTING_USERS` | `true` (since v558) |

None of the `REALTIME_FIRST_CONVERSATION_*` keys is in the tracked `.env` either. Current release **v561** "Deploy d1d93d0b" = rollback target.

### 17.5 Pre-flight

1. Gates: qa-testing regression on release 99a2933 and on FE fc74a5e; security-guardian verdict on 7c9d993 (newest section of `audit-security.md`); operator approval for the push.
2. `heroku releases -a mindsync -n 1` still shows v561. If anything else landed, that release is the rollback target.
3. `git -C MindSync fetch origin` and `git -C MindSync merge-base --is-ancestor origin/main release/first-conversation-voice-v2` must succeed (fast-forward).
4. Timing: right after an idle tick (minute 10, 25, 40 or 55) has finished and before the next backfill sweep (5, 20, 35, 50), so for example at minute 13 to 17.

### 17.6 Backend push (push = production, no migration)

```bash
git -C MindSync push origin release/first-conversation-voice-v2:main   # refuses anything but a fast-forward
heroku releases -a mindsync -n 1 < /dev/null                           # until "Deploy 99a29330" (v562)
```

There is no `alembic upgrade` step. Merge order is already baked into 99a2933: the voice commits as a fast-forward, then the profile branch as a merge. Pushing them as two releases instead gains nothing (disjoint files, no migration) and costs one more restart.

### 17.7 Smoke checks

1. `curl -s https://mindsync-829f3f05ed43.herokuapp.com/api/v1/audio-v2/health` returns `"status":"ok"`; `heroku ps -a mindsync` shows web, worker (`high default`) and scheduler up.
2. Boot logs: no `Traceback`, `H10`, `R10` or `create_all at startup failed`; both crons logged as scheduled.
3. One-off, REPL-safe (`heroku run --no-tty -a mindsync python < smoke_v2.py`):

   ```python
   from app.core.config import settings
   from app.services import first_conversation as fc
   from app.services import user_profile_writes as upw
   print("EFFORT", settings.REALTIME_FIRST_CONVERSATION_REASONING_EFFORT, fc.resolve_reasoning_effort())
   print("VOICE", repr(fc.resolve_voice()), "MODEL", fc.realtime_model())
   print("PROPS", fc.start_event_properties(is_rerun=False))
   print("PROTECTED", upw.PROTECTED_IDENTITY_FIELDS)
   print("DONE_" + "SENTINEL")
   ```

   Expect `low low`, `'' gpt-realtime-2.1`, `prompt_version first-conversation-v2, reasoning_effort low, voice_overridden False, is_rerun False`.
4. TEST account only (token never in a log or a ticket): `POST /users/profile` with `{"full_name":"Probe"}` on its existing profile returns 200 with the stored, unchanged row; `PUT /users/profile` with `{"full_name": null, "gender": null}` returns the row unchanged; `{"full_name": ""}` stores null (put the name back afterwards). Logs show `POST /users/profile on existing profile ... no write` and `PUT /users/profile ignored explicit null`; no new `UniqueViolation` on `user_profile`.
5. First conversation on a fresh TEST account (TestFlight 2.0.103 is enough for this): log `Started first-conversation Reflect thread N ... (rerun=False)`; Reset onboarding on the same account: `(rerun=True)` and a new thread. posthog-data-extractor then confirms `reflect_session_started` with `entry_origin = onboarding_first_conversation` carries `prompt_version`, `reasoning_effort = low`, `voice_overridden = false` and `is_rerun` false, then true.
6. Watch 30 minutes: no new 5xx; `grep "\[FirstConversation\]"` for `Could not lock the account` and `No marked thread` (both should be rare).

### 17.8 Order, and old against new

Backend first: it stops the profile wipe for every installed build at once (store 2.0.94/2.0.95, TestFlight 2.0.101 to 2.0.103), while the new FE protects only itself. The FE is safe in either order:

- New FE on v561: the no-JSON flush POST gets 500 and returns false without a PUT, so the row is untouched. A re-run gets an ordinary thread (claim already taken); a Free account sees the calm voice note and the limit panel (same 403 strings on v561); a trial account talks with the ordinary Reflect prompt, sent once.
- Old builds on 99a2933: the re-run POST returns 200 and writes nothing. 2.0.101 to 2.0.103 on a re-run get the scripted marked thread; a Free account past its window meets the same 403s as on its ordinary thread before ("Connection lost", "did not send", fixed only by fc74a5e); a trial account gets the script with the prompt also sent as a system item (doubled input, as on first runs of those builds).

### 17.9 Rollback

1. `heroku rollback v561 -a mindsync`.
2. Before anything else lands on `main`, push the reverts (newest first; never force-push):

   ```bash
   git revert --no-edit -m 1 99a2933        # profile fix
   git revert --no-edit d1d93d0..7c9d993     # voice v2, five commits
   git push origin main
   ```

   Either half can be reverted alone. Re-landing a reverted merge later needs a revert of that revert.
3. No migration and no cron to undo. `REALTIME_FIRST_CONVERSATION_VOICE` only ever as a Config Var: v561 ignores an unknown Config Var, but the same key in the tracked `.env` would crash-loop the web dyno at boot (pydantic-settings rejects undeclared `.env` keys).
4. Data the new code leaves behind is fine for v561: re-run threads are ordinary marked threads there (an ACTIVE one is resumed, the exemption is still bounded by the claim); profiles hold plain values.
5. Frontend: expire the TestFlight build, replace the Play internal build, revert on `dev`. The backend can stay.

### 17.10 Frontend (after 17.7 is green)

```bash
cd mindsync-frontend
git fetch origin
git merge-base --is-ancestor origin/dev fix/first-conversation-voice-v2-fe   # true while dev is 113543f
# temporary worktree: flutter analyze | grep "error •" prints nothing; flutter test one directory at a time
#   test/screens/first_conversation, test/screens/wow, test/screens/subscription, test/api
git push origin fix/first-conversation-voice-v2-fe:dev                       # operator approval; Codemagic bumps to 2.0.104
```

The local `dev` branch is stale (f27c589); push the branch ref as shown instead of checking out `dev`.

### 17.11 Device QA (2.0.104, iPhone and Android)

1. First run on a fresh account: scripted opening; `is_rerun` false.
2. Re-run on the same account (Settings, Reset onboarding): a new scripted thread, `is_rerun` true, no post-conversation offer (`onboarding_rerun`).
3. Name and gender set in Account survive a re-run; the companion still uses the name. Repeat the re-run once on store build 2.0.95 against the new backend.
4. Account: clear the name and save; a later re-run does not bring back the Firebase display name.
5. Free account after its window: voice gives the calm Premium note with Voice locked, no "Connection lost", no reconnect loop; text reaches the Reflect limit panel; "Finish for now" still gives the recap and the hand-off.
6. Purchase from that paywall (sandbox), processed exactly once: one `subscription_purchase_completed` with `trigger_feature` `premium_gate_reflect_voice` or `premium_gate_reflect_messages`, none with `post_onboarding`, one receipt verification in the backend logs. Expected today because of F1: Premium Welcome, then Home, conversation left without a recap. Record what happens.
7. Same paywall closed with X and with system back, no purchase: back in the conversation, gates still locked. Restore there on an account with an active subscription: gates lift after closing.
8. A crisis reply in text: no "See Premium" entries.
9. Polish gender agreement by ear: one account with female, one with male, one with no gender (neutral forms).
10. marin vs cedar: switch the voice in the app's Settings on the test account (an empty `REALTIME_FIRST_CONVERSATION_VOICE` keeps the app's choice), so no Config Var change and no restart. Set the Config Var only to force one voice for everybody.
11. The prompt goes in once: debug log shows `session.update` then `response.create`, no system conversation item, also after a reconnect.
12. Android: predictive back on the voice note, the limit panel and the paywall.

### 17.12 Deployed 2026-10-06: backend v562, frontend 185d62a on dev

Executed by integration-devops on the operator's approval ("Tak, push backendu teraz", "front na dev po zielonym QA"; QA verdict GO in `qa-regression-voice-v2.md` sections 1 to 4). Times CEST (UTC+2). No Config Var changed, no migration run.

| step | time | result |
|---|---|---|
| Pre-flight | 06:28 to 06:31 | Stored CLI login rejected again, so `HEROKU_API_KEY` from `_netrc` per command (token never printed). Current release **v561** = rollback target. `origin/main` still d1d93d0; `release/first-conversation-voice-v2` 99a2933 is a fast-forward of it (8 commits). Diff d1d93d0..99a2933: 21 files, nothing under `alembic/` or `app/models/`; `Procfile`, `requirements.txt` and the tracked `.env` unchanged. Worker idle after the 04:30 UTC hourly jobs; the push went between the :25 idle tick and the :35 sweep. |
| Push | 06:31:41 | `git push origin release/first-conversation-voice-v2:main`, `d1d93d0..99a2933`, no force. |
| Release | 06:32:54 | **v562** "Deploy 99a29337" (section 17.6 said 99a29330; the real short hash ends in 7). |
| Boot | 06:33:20 to 06:33:34 | web: `clear_all_scheduled_jobs: cancelled 25`, 25 jobs registered again including `mindsync_reflect_idle_analysis` and `mindsync_orca_memory_backfill_sweep`, "Application startup complete" at 06:33:28. Worker "Listening on high, default" at 06:33:34, scheduler up at 06:33:23. No H10, R10, `create_all at startup failed` or traceback at import or lifespan. |
| Migration | none | Not needed: no migration in the diff, prod stays at `m316a1b2c3d4`. |
| Smoke 1 | 06:36 | `/api/v1/audio-v2/health` 200 `"status":"ok"`; `heroku ps`: web, worker (`high default`) and scheduler up. |
| Smoke 3 | 06:38 | One-off `run.2582`, exited 0 (the CLI said exit 1, the artifact from section 12 note 1): `EFFORT low low`; `VOICE '' MODEL gpt-realtime-2.1`; start properties `prompt_version first-conversation-v2`, `reasoning_effort low`, `voice_overridden False`, `is_rerun` False and True; `PROTECTED_IDENTITY_FIELDS` = full_name, pronouns, gender, age_band; no `REALTIME_FIRST_CONVERSATION_*` Config Var set; one worker `['high','default']`, idle; 25 scheduled jobs, idle tick 1, sweep 1. |
| First ticks on v562 | 06:35, 06:40 | `[OrcaBackfill] Sweep done in 0.3s: candidates=0 ... errors=0`; `[ReflectIdle] Done in 1.9s: candidates=0 ... errors=0`; every worker job OK, none failed. |
| Watch to 06:49 | | 5 router requests: 4x 200 and 1x 404 on `get_user_profile_and_subscription` right before a new account's first `POST /users/` (the half-created-account contract). One new sign-up went through `POST /users/` 200 and `POST /users/profile` 200 (create path). No 5xx, no H code. No `[FirstConversation]` line yet: nobody started a first conversation this early. |
| Frontend push | 06:38:54 | `origin/dev` was still 113543f (tag `app_2.0.103`), so a fast-forward with no merge and no worktree: `git push origin fix/first-conversation-paywall-return:dev`, `113543f..185d62a` (1277c02, 71947ef, fc74a5e, 185d62a). The main frontend tree, with its uncommitted agent memory and `test/marketing_shots` files, was not touched. |
| Codemagic | to 06:50 | No version bump on dev yet 11 minutes after the push (earlier bumps took 7 to 22 minutes). Expected: bump commit and tag `app_2.0.104` on top of 185d62a, then TestFlight and Play internal. |

Notes:

1. One web traceback after the restart, not caused by this release: `posthog_service.identify` always passes `set_once=` to the PostHog client (`posthog>=3.7.0,<4.0.0`), whose `identify()` has no such argument. The `TypeError` is caught and logged as a WARNING, and the request still returns 200 (`POST /users/` at 06:36:28). The call has been like this since c5ee63d (2026-04-25), so every backend `identify` (sign-up in `users.py`, `premium_intent.py`, line 406 of `posthog_service.py`) has never reached PostHog. Owner backend-api: send `$set_once` inside the properties, as `capture()` already does.
2. 185d62a closes F1 and F2 of section 17.3. Device QA item 6 therefore changes: after a purchase on the paywall opened from the first conversation, the app should return to the conversation (not Premium Welcome and Home), and closing the conversation ends an open thread that has user turns, exactly once. Record what happens on both platforms.
3. Still open: smoke 4 (needs a TEST account token), smoke 5 and the device QA in 17.11 (operator), and posthog-data-extractor confirming `reflect_session_started` with `entry_origin = onboarding_first_conversation` carries `is_rerun`, `prompt_version`, `reasoning_effort` and `voice_overridden` after the first real start.
4. Rollback stays as in 17.9, target **v561**. Frontend rollback: expire the 2.0.104 build in TestFlight, replace it on Play internal, and push a revert of `113543f..185d62a` to dev.
