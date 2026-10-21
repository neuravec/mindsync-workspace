# First voice conversation with Orca: onboarding ends in one conversation, then the offer

Approved by the operator on 2026-10-03 ("Teraz super. Zaimplementuj ... end2end"). Canvas: https://claude.ai/artifact/XEowEoTfciKfnxLLtXFh4S. Local copy of every screen: `screens/` (open the `.dc.html` files as reference; copy is in the markup, variants are in each file's `data-props` and `renderVals()`). Implement **Option B** for the offer (screens `OfferStarterFirst` and `AllPlans`); Option A (`Paywall` with all three plans) is NOT built, but the `Paywall.dc.html` file holds the shared recap header and the "prices failed" state.

Why: 80% of new users do nothing valuable in their first 24 h, and the paywall should come after the first moment of value. See `analytics-reports/2026-10-03-retencja-subskrypcje-priorytety.md` and `competitive-reports/2026-10-03-research-retencja-konwersja.md`.

## 0. Hard rules for every agent

1. Work on branch `feat/first-voice-conversation` in each repo (backend `MindSync/` from `main`, frontend `mindsync-frontend/` from `dev`). Create it if missing, otherwise reuse it. **Never push.** Backend push to main = instant Heroku deploy; frontend push to dev = TestFlight. The operator approves pushes.
2. Commit only files you changed, by explicit path. **Never `git add .` or `git add -A`**: both repos contain uncommitted files from other sessions (e.g. `test/marketing_shots/*`, `test_temp.db`, `db-reports/`).
3. CLAUDE.md "Change Safety & Impact Recon" applies: list consumers, boot-critical paths, model/migration/prod agreement, Postgres DDL check offline, cross-layer contracts, failure modes. A backend error must never be read by the client as "new user / needs onboarding".
4. Stay inside your file ownership. If you need a change in a file another agent owns, stop and report it.
5. Tests are part of the task. Do not run the whole `flutter test` at once (OOM): run per directory. Do not use `run_in_background`.
6. No U+2014 or U+2013 characters in any user-facing copy, prompt text or report.
7. PostHog: every surface below has its events (section 6). Never send free text, transcript, recap text, memory text, health details, emails or tokens to PostHog. Enums, counts, booleans and durations only.

## 1. The flow (new users who just finished onboarding)

Build (unchanged) → **1 Reveal** ("Your MindSync is ready", single CTA "Talk with [Orca]") → **2 Before the first conversation** (3 topics + "Then, talk about anything", privacy line, "Start talking" triggers the mic permission, small link "Can't talk right now? Type instead") → **3 First conversation** (voice) → End → **4B step 1** (recap "What [Orca] heard" + only the 2-week offer + "Continue") → **4B step 2** = the existing subscription screen with all plans (entry `onboarding`, chip "Your free 4 days are on. Close to keep them.") → Reminders pre-prompt (existing OB15 screen, moved here) → Home.

- The **First step** screen (`FlowFirstStep`) is removed from the new-user flow. Its `first_capture_prompt_*` events stop firing for this path; that is expected.
- The old post-onboarding offer screen (`PostOnboarding` with three radio options) is replaced by 4B step 1 + step 2.
- Buying the 2-week starter on step 1 → existing premium Welcome screen → reminders → Home. Buying on step 2 → same. Closing step 2 (X) → reminders → Home with the free 4-day trial.
- Offer eligibility stays as today (`wow_cubit._offerSkipReason`): just onboarded, active `signup_trial`, not already premium from a purchase, not already seen, products available. When ineligible, skip 4B entirely but still show the recap on a simple screen with "Continue" (recap is value, not a sales device). When products failed to load: show the "Prices didn't load" state (screen `PaywallPricesFailed`) with "Try again" and "Continue with my free 4 days". Never skip silently.

### 1.1 Conversation structure (prompt + UI)

- **Part 1, getting to know you: always 3 opening questions.** Each built from an onboarding answer when it exists, otherwise a general fallback question. Never 0 questions.
  - In therapy (status yes_regular / yes_occasional AND Art. 9 consent): Q1 how the top focus area (with intensity) showed up this week; Q2 what has helped, even a little; Q3 what they want from the next session (day from the schedule), "I'll turn it into your Before therapy card".
  - Not in therapy / no consent: Q3 becomes "What would you like to feel more of in the next few weeks?".
  - Answers skipped: Q1 "What made you want to try MindSync today?", Q2 "What has been on your mind lately?", Q3 "What would you like to feel more of?".
  - Mixed: fall back per question.
- **Part 2, open conversation.** No counter, no planned end. Orca follows what the person said and asks about areas not covered yet (sleep, work, relationships, what they want from therapy or from MindSync). Orca never ends the call itself and never mentions Premium, prices or limits. Only the person ends it.
- Around minute 15 Orca offers a pause once ("we can stop here or keep going"), without ending.
- Talk style = the companion's `tone_archetype`; name = companion name; language = app language (existing AI_LANGUAGE handling). Existing crisis/safety handling of the Reflect prompt must be kept.
- UI phase indicator: 3 segments "Getting to know you · n of 3 · <topic>" during part 1, then the pill "Open conversation · end whenever you like". The model signals phase changes with a realtime **function tool** `update_conversation_phase` (`{"phase": "opening", "question": 1|2|3}` or `{"phase": "open"}` or `{"phase": "pause_offered"}`). The client updates the UI and answers with `function_call_output` without forcing a new response. If no tool call arrives, the UI simply stays on the last known phase (graceful degradation, never blocks the call).
- "[Orca] remembers" chips: built client-side from onboarding answers (top focus area with intensity, second focus area, next session day/time or talk style). Hidden when answers were skipped.

## 2. Decisions taken (operator accepted the recommendations)

- "Type instead" link stays on screen 2. Text mode is the same first conversation (same thread, same prompt, same 3 opening questions, same recap).
- The first conversation is **exempt** from the Free Reflect monthly limit (15 messages) and from the Reflect voice Premium gate, regardless of trial state.
- Higher reasoning effort for this conversation only: config `REALTIME_FIRST_CONVERSATION_REASONING_EFFORT` (default `"medium"`), model `REALTIME_FIRST_CONVERSATION_MODEL` (default = the current agent model `gpt-realtime-2`; the lead will confirm after research on OpenAI realtime limits and models).
- Pause offer once around minute 15.
- Research result (2026-10-03, official OpenAI docs): a Realtime session lasts at most 60 minutes; the ephemeral key TTL only limits opening the connection, not the session. `gpt-realtime-2.1` (2026-07-06) is the newest realtime model, same price and 128k context as `gpt-realtime-2`, better silence/noise and interruption handling: **use `gpt-realtime-2.1` as `REALTIME_FIRST_CONVERSATION_MODEL` default**, reasoning effort `medium` (valid values: minimal, low, medium, high, xhigh). Each response re-sends the whole conversation, so long calls get more expensive: set `truncation` to `{"type": "retention_ratio", "retention_ratio": 0.8}` for this session (cache-friendly) and log `usage` from `response.done` totals per call (backend or client, counts only) so the real cost of a 30-minute call can be measured. Function tools: define in `session.update` (`tools`, `tool_choice: "auto"`), handle `response.function_call_arguments.done` (`call_id`, `name`, `arguments`), reply with `conversation.item.create` type `function_call_output` and do NOT send `response.create` (so the model keeps talking); never send `response.create` while a response is active.
- Long sessions: proactively reconnect around minute 50 (new session on the same thread with the history injected via `conversation.item.create`, which session_data already supports) so the 60-minute provider limit is never hit mid-sentence. If the realtime session ends because of a provider limit anyway, the client reconnects once silently on the same thread (session_data already returns the thread history); if that fails, show the "Connection lost" screen (continue in text / try voice again). Nothing said is lost.

## 3. Data: what the first conversation leaves behind (operator requirement)

"Wszystkie istotne dane mają zasilać agentów i inne funkcje." Current gaps (verified in code on 2026-10-03): analysis (summary, topics, emotions, RAG document) runs only on a manual `POST /reflect/{id}/end`; a closed screen leaves the thread ACTIVE forever and the nightly job skips REFLECT; Personal Bio and Reflect summary cards never reach any prompt; therapy schedule / next session are not in the Reflect prompt; the text Reflect prompt is frozen at `/start`; the last voice turn has only 2.5 s to be saved.

Required:
1. **Orca memory** (new table, see 4.1): short facts about the person (what weighs on them, what helps, goals, people, routines, what they want from therapy). Written from the first-conversation recap, and later from every analyzed Reflect conversation. Deduplicated, capped (keep the most recent/important ~30 active items per user).
2. **Fed into**: every Reflect prompt (voice `session_data` and text, built fresh for each message or session, not frozen), the Before therapy (prep) card generation, the Personal Bio generation, and the After therapy (debrief) analysis if it has an AI prompt. Budget: memory block at most ~1200 characters, newest and most relevant first.
3. Also feed into the Reflect prompt: therapy schedule (next session day/time), and the Personal Bio "Your Patterns" section (short).
4. **Personal Bio refresh right after the first conversation** (enqueue on the `high` RQ queue), not only on the weekly schedule.
5. **Every Reflect conversation gets analyzed**: on End, and also when the app is closed or the conversation goes quiet for 30 minutes (job). The user can still continue the thread as today. Analysis runs once per new content (idempotent).
6. **The person can see and delete** what Orca remembers (Settings, "What [Orca] remembers"): list, delete one, delete all. Account deletion removes all memory rows. If a data export exists, include memory.
7. Last voice turn: wait up to 5 s for the final transcript before calling `/end`.

## 4. API contract (backend → frontend). integration-devops verifies, flutter-mobile builds against it

### 4.1 Storage (backend-api)
Table `user_memory_items`: `id` PK, `user_id` FK users (Firebase UID, ON DELETE CASCADE), `text` (encrypted like messages, using the existing `encode`/`decode`), `category` `String(32)` (`weighs_on` | `helps` | `goal` | `person` | `routine` | `therapy_wish` | `other`, Python constants, NOT a PG enum), `source` `String(32)` (`first_conversation` | `reflect` | `debrief` | `prep_card` | `other`), `source_conversation_id` nullable FK, `created_at`, `updated_at`, `deleted_at` nullable (soft delete for "Forget this", hard delete on account deletion). Index on (user_id, deleted_at). Idempotent migration, `down_revision` = the real current head (`alembic heads` must show exactly one head after your migration).
Reflect thread marker: a nullable `String(32)` column on the Reflect thread row (name it after the existing m314 entry columns, e.g. `entry_origin`), value `onboarding_first_conversation`.

### 4.2 Endpoints
- `POST /api/v1/reflect/start` body gains optional `entry: "onboarding_first_conversation"` (with `mode: "voice"|"text"`). Server marks the thread. Once per account: if an ACTIVE first-conversation thread exists, return it; if one already FINISHED, start a normal thread (no marker). For text mode the response's `opening_question` = the first opening question (so the client renders it as the first bubble). Old clients that send no body are unaffected.
- `GET /api/v1/reflect/{id}/session_data` for a marked thread: `system_message` = first-conversation prompt (section 1.1); `data.client_session_config` carries the reasoning-effort override and `tools` (the `update_conversation_phase` definition) for the client to put into `session.update`; `data.first_conversation = {"in_therapy": bool, "answers_filled": bool, "topics": [3 short labels], "pause_offer_after_seconds": 900}`. The `model` field returns `REALTIME_FIRST_CONVERSATION_MODEL`.
- Monthly limit / voice gate: messages in a marked thread do not count and are never blocked. `GET /reflect/usage` unchanged in shape.
- `POST /api/v1/reflect/{id}/end` unchanged in shape; idempotent (a second call returns 200 and does not double-run analysis).
- **New** `POST /api/v1/reflect/{id}/recap` (owner only, any Reflect thread with at least one user message; used now for the first conversation). Synchronous, server timeout about 15 s. Idempotent: stored result returned on repeat calls. Response:
  ```json
  {"status": "ready" | "short" | "failed",
   "items": ["...", "...", "..."],
   "saved_line_kind": "before_therapy_card" | "check_in",
   "memory_items_saved": 3}
  ```
  `short` = too little was said (fewer than 2 user turns or about 40 words): no LLM call, `items: []`. `failed` = LLM error/timeout: `items: []`, the client shows the short-style copy. The same call writes the Orca memory items and enqueues the Personal Bio refresh on `high`.
- **New (BUILT, BE-A commit 0240841)** `GET /api/v1/users/memory` → `{"items": [{"id": int, "text": str, "category": str, "source": str, "created_at": iso}]}` (active only, newest first). `DELETE /api/v1/users/memory/{item_id}` → 204 (HARD delete, owner only; 404 `{"detail":"memory_item_not_found"}` for others/missing). `DELETE /api/v1/users/memory` → 204 (hard delete all, repeatable). Before the migration runs, all three return 503 `{"detail":"memory_unavailable"}`: the client shows the empty/unavailable state, never an error loop. Deleting a Reflect thread also deletes the memory items derived from it.

## 5. Frontend scope (flutter-mobile)

FE-1 (conversation): Reveal single CTA; screen 2 (`VoiceIntro`); first-conversation mode of the voice screen (phase indicator, remembers chips, End, switch to text); text mode of the same thread (`TypeFallback`); connection lost (`VoiceError`) with one silent reconnect first; mic-permission denial goes to text mode; preload store products at the start of the conversation; End → wait for final transcript (up to 5 s) → `/end` → `/recap`.
FE-2 (offer + data surfaces): 4B step 1 (recap header with states ready / writing / short + starter card + Continue; prices failed state with retry); step 2 = existing subscription screen with entry `onboarding` (chip copy above, close returns into the flow); recap-only screen when the offer is ineligible; reminders pre-prompt after the offer; First step screen removed for new users; Settings screen "What [Orca] remembers" (list, delete one, delete all, empty state); "Reset onboarding" in Settings fires `onboarding_reset` and the rerun must not be treated as a fresh account for the offer (reason `onboarding_rerun`); l10n for all 7 languages (en source copy from the screens; `Most of our users feel like they got a second therapy session` stays verbatim in English and is translated faithfully elsewhere).

## 6. PostHog events (reuse taxonomy first; snake_case; fire once, on one side)

| surface | user action | event | key properties | side |
|---|---|---|---|---|
| Reveal | viewed / tapped Talk | existing `personal_reveal_viewed`; `first_conversation_cta_tapped` | | client |
| Intro | viewed | `first_conversation_intro_viewed` | in_therapy, answers_filled | client |
| Intro | Start talking / Type instead | `first_conversation_started` | mode (voice/text), entry_point (intro/type_instead/mic_denied/connection_lost) | client |
| Mic | permission result | reuse existing mic permission event if any, else `mic_permission_result` | result | client |
| Voice | phase reached | `first_conversation_phase_reached` | phase (opening_1/2/3, open, pause_offered) | client |
| Voice | switch mode | `first_conversation_mode_switched` | from, to, reason (user/connection_lost) | client |
| Voice | connection lost / reconnect | `first_conversation_connection_lost` | reconnected (bool) | client |
| Voice/Text | End | `first_conversation_ended` | mode, duration_s, user_turns, reached_open (bool) | client |
| Recap | result shown | `first_conversation_recap_result` | status, latency_ms | client |
| Backend | memory written | `orca_memory_items_saved` | count, source | backend |
| 4B step 1 | shown | `paywall_shown` trigger_feature=`post_onboarding` + new `post_onboarding_offer_shown` | recap_status | client |
| 4B step 1/2 | outcome | `post_onboarding_offer_result` | purchased_starter / purchased_annual / purchased_monthly / continued_to_plans / closed_plans / skipped_ineligible | client |
| 4B step 2 | shown | `paywall_shown` trigger_feature=`post_onboarding_all_plans` | | client |
| Offer | not shown | existing `post_onboarding_offer_not_shown` | reason (+ `onboarding_rerun`), premium_source (enum or none) | client |
| Prices | load failed / retry | `paywall_load_failed` | reason (store_unavailable / products_not_found / query_error / timeout), preload (bool), trigger_feature; `paywall_retry_tapped` | client |
| Settings | Reset onboarding | `onboarding_reset` | | client |
| Memory screen | viewed / delete one / delete all | `orca_memory_viewed` (item_count), `orca_memory_item_deleted` (category), `orca_memory_cleared` (item_count) | | client |

The funnel Reveal → intro → started → ended → recap → offer shown → result must be reconstructable, including the skip and close branches. Add privacy tests that assert no free text is sent.

**Lead-approved deviations (2026-10-05, after the security and UX audits):** `first_conversation_cta_tapped` is retired, `personal_reveal_cta_tapped` is the single CTA event; `first_conversation_intro_viewed` carries only `answers_filled` (no `in_therapy`, no `question_set`: therapy-status proxies, audit M-4); memory events carry no `category` (M-4); the crisis (calm) branch sends NO event at all, so it is deliberately not countable in PostHog (H-1); backend gate outcomes (consent withdrawn, no notice, crisis filtered) are not events. Added: `post_onboarding_offer_result` value `closed_offer` (step 1 close X), `reflect_thread_analyzed` (backend), `mic_settings_opened`, `orca_memory_delete_undone`, `orca_memory_clear_cancelled`, `orca_memory_action_failed`, `first_conversation_session_renewed`, `first_conversation_start_failed`, `first_conversation_skipped`. The privacy guard test forbids `crisis*`, `in_therapy`, `question_set`, `category` keys on every event.

## 7. Work packages, owners, order

| id | owner | depends on | scope |
|---|---|---|---|
| BE-A | backend-api | none | 4.1 storage + migration + CRUD + memory endpoints (4.2 users part) + account deletion + config settings (`REALTIME_FIRST_CONVERSATION_*`) + thread marker column. Does NOT touch `reflect.py`. |
| FE-1 | flutter-mobile | none (builds against section 4) | section 5 FE-1 |
| BE-B1 | data-analytics (owns `app/api/v1/endpoints/reflect.py` for this batch) | BE-A | first-conversation start, prompt, session_data, tools, limit/gate exemption, `/recap`, memory extraction service, bio refresh enqueue |
| FE-2 | flutter-mobile | FE-1 | section 5 FE-2 + section 6 events |
| BE-B2 | data-analytics | BE-B1 | section 3 items 2-5: feed memory, bio patterns and schedule into Reflect (voice + text, not frozen), prep card, bio, debrief; idle analysis job (register in `rq_scheduler_setup.py` on `default`; coordinate the registration line with backend-api through the lead) |
| CHECK | integration-devops, security-guardian, qa-testing | all | contract end to end; Art. 9 memory data, scoping, deletion; full regression both repos |

Deploy (later, operator approval): backend + `alembic upgrade head` together (push main, then migrate immediately, boot must survive the gap), then frontend to dev (TestFlight). Device QA on a fresh account before stores.
