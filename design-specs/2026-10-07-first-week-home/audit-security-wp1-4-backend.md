# Security review: WP-1..4 backend (first-week Home), pre-deploy, 2026-10-11

Auditor: security-guardian (read-only). No code, git, Heroku or prod changes were made. This file is the only write.

Scope: `git diff 8eb8d3f..a021da9` on branch `feat/first-week-home` in `MindSync-wt-fw-integration` (84 files, +22066 / -466, 22 commits). 8eb8d3f is the deployed WP-0 release (`audit-security-wp0-backend.md`). Question: may a021da9 go to production, followed by `alembic upgrade head` (m317a1b2c3d4, m318a1b2c3d4)? Excluded on request: the plan-step reminder generator and the week-1 mute list (separate branch).

Sources: `SPEC.md` (sections 3, 4, 5, 9, 13), `API_CONTRACT.md` (0, 1 to 9, 10, 11, 14.1, 14.2), `audit-security-design.md` (H-1 to H-4, M-1 to M-7), `audit-security-wp0-backend.md` (M-3, L-1 to L-6).

Code read in full: every new module (`api/v1/endpoints/first_week*.py`, `_first_week_http.py`, `services/first_week/{anchor,tone,follow_up,plan_service,plan_loader,recap}.py`, `services/therapy_consent.py`, `services/therapy_schedule_service.py`, `crud/first_week.py`, `crud/first_week_reads.py`, `crud/schedule_skips.py`, `models/first_week.py`, `schemas/first_week*.py`, `tasks/first_week_*.py`, both migrations), and every changed hunk in `users.py`, `reflect.py`, `conversations.py`, `symptoms.py`, `main.py`, `api.py`, `crud.py`, `orca_memory.py`, `user_memory.py`, `conversation_analysis.py`, `reflect_prompt.py`, `push_cadence.py`, `moment_privacy.py`, `notification_orchestrator.py`, the seven session generators and `weekly_therapy_summary.py`. Context read outside the diff: `deps.get_current_user`, `main.py` error handlers and `_capture_api_error`, `encode_service`, `orca_memory._chat_completion`, `tasks/prep_card_auto_generate.py`, account deletion in `users.py`.

Verification run (Python 3.12, SQLite, test DB and bytecode in the scratchpad, worktree left clean): `test_first_week_api_boot`, `test_schedule_art9_gate`, `test_therapy_consent`, `test_first_week_api` (353 passed); `test_first_week_tone`, `test_first_week_follow_up`, `test_first_week_recap`, `test_first_week_seams`, `test_m318_first_week_migration`, `test_first_week_store`, `test_first_week_anchor`, `test_onboarding_ratings_and_symptom_event`, `test_moment_privacy`, `test_push_privacy_h4` (2210 passed). I did not run the full suite (qa-testing owns that). I also computed the stored ciphertext lengths of the fixed follow-up questions (H-1 evidence).

## Verdict

**GO with conditions** for pushing a021da9 and running m317 and m318.

The core contracts hold. Every new route is token-scoped with no user id from the client, bodies are `extra="forbid"`, nothing on SPEC 4's forbidden list is settable, every first-week response (errors and auth failures included) carries `no-store` and never a 500, and the pre-migration window degrades to 503 without touching boot. Tone lives only in the padded, encrypted Redis key with silent writers (H-2). The plan, the session generators and the push-cap look-ahead read therapy status and schedule only through the Art. 9 gate (H-3, WP-0 M-2). The follow-up question follows the memory gate, is crisis-screened at generation and display, is Fernet-encrypted, cascades with its memory item, thread and account, and is purged daily. No horizontal privilege escalation, no raw SQL with input, no new PostHog event, `symptom_scored` lost its score bucket.

One High finding (H-1): the calm question that a crisis-flagged person receives is recoverable from the ciphertext length of the follow-up thread's first message in Postgres. It is latent: it becomes reachable only when a client starts follow-up threads (`seed_source=first_week_followup`), and no shipped client sends that value (contract 11.1). **It does not block this backend push; it blocks the WP-3 frontend release** (any build that starts follow-up threads). The fix is small and I recommend putting it into this push so the High is closed before anything ships.

Three Medium findings. M-1 is live for new signups right after the deploy and should be fixed this sprint. M-2 is a configuration condition for the frontend release. M-3 needs an operator decision before m317 runs, because m317 revives an hourly AI cron that has no Art. 9 gate.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 1 (H-1, latent until the WP-3 frontend ships) |
| Medium | 3 |
| Low | 8 |
| Info | 12 |

## Findings table

| ID | Sev | Title | Location | Owner | Blocks |
|---|---|---|---|---|---|
| H-1 | High | Calm follow-up question recoverable from ciphertext length in Postgres | `services/first_week/follow_up.py:179-197`, `:797-810`; `api/v1/endpoints/reflect.py:909`, `:943`, `:949`, `:559-585` | data-analytics (questions), backend-api (reflect.py) | WP-3 frontend release; recommended before this push |
| M-1 | Medium | Model-call traces split by the crisis flag (token_usage_log rows, follow-up row, one INFO line) | `follow_up.py:537-620`; `recap.py:1014`, `:1059-1061`; `crud/first_week.py:824` | data-analytics, backend-api | No; this sprint |
| M-2 | Medium | Art. 9 gate on `PUT /users/therapy-schedule` is off by default, also for builds that send `X-App-Version` | `services/therapy_schedule_service.py:84-119`; `core/config.py:277-292` | operator, integration-devops, backend-api | Frontend build with the consent step |
| M-3 | Medium | m317 revives the hourly auto prep-card cron, which reads the schedule without the Art. 9 gate | `tasks/prep_card_auto_generate.py:106-118`, `:224-237` (outside the diff) | backend-api | Operator decision before m317 |
| L-1 | Low | Log lines that encode the variant or a missed session | `plan_service.py:459`, `:481`; `therapy_schedule_service.py:448-455`; `users.py:1795` | backend-api | No |
| L-2 | Low | Per-person `api_error` on the schedule routes (403 art9, change-route 4xx/503) | `main.py:220-263` via `users.py:1801`, `:1911` | backend-api | No |
| L-3 | Low | Quoted question copied into the stored system prompt (RP3-M1 rule) | `reflect.py:943`; `reflect_prompt.py:1249` | backend-api | No |
| L-4 | Low | `step_moves` kept forever, including "session did not happen" dates | `crud/first_week.py:440-457`; `models/first_week.py:145` | backend-api | No |
| L-5 | Low | Change route lacks `no-store` on framework errors; 422 echoes the body | `users.py:1879-1913`; `main.py:285-297` | backend-api | No |
| L-6 | Low | Recap job re-enqueued on `high` after uncounted failures | `recap.py:1101-1104`, `:1125-1135` | data-analytics | No |
| L-7 | Low | No rate limit; follow-up GET decrypts and scans up to 50 threads per call | `follow_up.py:738-760`, `:786` | backend-api, integration-devops | No |
| L-8 | Low | Generation runs for new signups before any client shows it; first weekly card suppressed for old-client users | `orca_memory.py` (`_offer_first_week_follow_up`), `weekly_therapy_summary.py` (`_is_suppressed_first_calendar_week`) | lead, data-analytics | Lead decision |

---

## High findings

### H-1: The calm follow-up question is recoverable from its ciphertext length in Postgres

- **Severity:** High. It turns a crisis signal into a durable, deterministic marker in the production database. H-2 rules "never in Postgres" for tone, and the design review rated a crisis marker readable from Postgres, logs or job results High because database-administrator and growth-analyst run SELECTs on prod and backups outlive the window. This code base already treats ciphertext length as a leak: the tone key is padded to 128 bytes (`tone.py`, `_PLAINTEXT_LEN`) and the recap cache to 2048 (`recap.py`, `_CACHE_PLAINTEXT_BYTES`). The follow-up thread is not padded.
- **Location:**
  - `app/services/first_week/follow_up.py:179-197`: one fixed generic and one fixed calm question per language.
  - `follow_up.py:797-810` (`_question_for_step`): the calm question is served whenever the tone is gentle or a quoted question fails a crisis display check (`:765-790`).
  - `app/api/v1/endpoints/reflect.py:949` and `:909`: in text mode the chosen question is persisted as the thread's first agent message through `_persist_opening_message` (`:559-585`), which writes `messages.content` and `conversations.last_message_preview` with plain `encode()` (`services/encode_service.py:15-17`, no padding). `:943` also embeds it in the stored system prompt (message 0).
- **Evidence (computed with Fernet plus the outer base64, as `encode()` does):** the stored length is 160 characters for the calm question in English, Polish, German, Spanish, Norwegian and Swedish, and 188 for the generic question in all seven languages (French is 188 for both). Plaintext under 32 bytes pads to two AES blocks, 32 bytes or more to three. The `seed_source = 'first_week_followup'` marker on `conversations` is plaintext.
- **Failure scenario:** someone with read access to prod (an agent preparing a report, a backup restore, a support query) selects the second message of every thread with `seed_source = 'first_week_followup'` and filters `length(content) = 160` (or the same on `last_message_preview`). The result is, for six of seven languages, the list of first-week accounts whose follow-up opened with the calm question: a gentle tone (crisis in the first conversation or any Reflect thread in the week), or a memory item or thread that failed the crisis rescan. It stays for the life of the thread, and in backups. Voice threads carry the same signal more noisily: Orca speaks the calm question and the agent transcript is stored.
- **Reachability:** only `POST /reflect/start` with `seed_source = "first_week_followup"` creates these threads. No shipped client sends it (`API_CONTRACT.md` 11.1); the first frontend build with the follow-up screen does. A crafted request with a person's own token affects only that person's own data.
- **Remediation (data-analytics for the questions, backend-api for reflect.py):**
  1. Preferred: serve one non-quoted question for both cases. The calm and the generic question become the same string per language (brand-voice-manager picks the wording that works in both moods, for example "How are you doing right now?"). `quoted` stays the only distinction the client sees. Absence of a quote then mixes crisis with "no memory item", "first talk skipped", "gate says no", and `talk2`, which is acceptable noise (same class as M-1).
  2. Not recommended: padding the persisted plaintext to a fixed byte bucket and stripping on read. Every reader of `messages.content` and `last_message_preview` would need to strip, and the system prompt length would still differ.
  3. Tests: for each of the seven languages, the stored length of the calm question equals that of the generic one (or the strings are equal); a start-thread test in both tones asserts the same stored length for the opening message and the preview.
- **Blocks:** the WP-3 frontend release. Not this backend push, for the reachability reason above, provided the fix lands in a backend push before that build. Recommended: fix it in this push.

---

## Medium findings

### M-1: Model-call traces split by the crisis flag

- **Location and mechanism:**
  - Follow-up generation (`follow_up.py:537-620`): a crisis in the source thread (`:573`) or a gentle tone (`:575`) returns `not_eligible` before the model call. Only the eligible path calls `bounded_chat_completion(..., operation="first_week_follow_up", user_id=...)` (`:592-600`). That writes a `token_usage_log` row with the user id (`orca_memory._chat_completion`, `track_usage` plus `log_token_usage`), stores a `first_week_follow_ups` row for 7 days, and logs `INFO [FirstWeek] stored 1 follow-up for user %s` (`crud/first_week.py:824`). The job's own lines are uniform (`tasks/first_week_follow_up.py:45-46`), but these three traces are not. The module docstring itself says that after memory was saved, "not eligible" mostly means crisis.
  - Recap "Orca noticed" (`recap.py:1059-1061`): a flagged week caches "nothing to show" with no model call. Every other active, non-quiet week runs the pipeline inside `track_usage("WEEKLY_SUMMARY", "first_week_recap_noticed", user_id=...)` (`:1014`). For these accounts the first calendar-week weekly card is suppressed, so no other weekly summary row covers that week.
- **Failure scenario:** growth-analyst computes AI cost per user from `token_usage_log` (its documented method) and joins it with the signup cohort. "First-week accounts with at least two done steps and activity in days 1 to 7 but no `first_week_recap_noticed` row" is mostly the crisis cohort. "First conversation produced memory, no `first_week_follow_up` row" is mostly a crisis later in days 0 to 2. The rows have no purge.
- **Context:** the class already exists. Memory extraction returns `FILTERED` before its model call on a keyword crisis (`orca_memory.py:2689-2692`). This diff adds two more such operations, one of them for every active first-week account. It is live right after deploy and m318 for new signups whatever their app version, because the anchor is written by the backend at onboarding completion, follow-up generation is triggered from `orca_memory`, and the recap job runs from the hourly sweep.
- **Remediation (data-analytics; backend-api for the log line):**
  1. Write usage for `first_week_follow_up` and `first_week_recap_noticed` without a user id (cost stays measurable in aggregate), or route operations whose skip depends on crisis through a usage writer that drops `user_id`. Apply the same to memory extraction in the same change.
  2. Move `stored 1 follow-up` to DEBUG.
  3. Test: no `token_usage_log` row with a user id is written for these operations.
- **Timeline:** this sprint; ideally before the WP-3/WP-4 frontend release. Not blocking.

### M-2: The Art. 9 gate on `PUT /users/therapy-schedule` is off by default

- **Location:** `services/therapy_schedule_service.py:84-119` (`art9_schedule_gate_applies`), `core/config.py:277-292`.
- **Description:** contract 14.1.3 sets the default before the database-administrator count as follows: a request without `X-App-Version` is not gated, and a request WITH it is gated. The code gates by header only when `ART9_SCHEDULE_GATE_MIN_APP_VERSION` is set. With both settings unset (the current state; neither is in `.env.example`), no PUT is gated, including requests from new builds. The docstring cites a "lead correction 2026-10-08" that the contract and SPEC 13.8 do not record.
- **What still holds:** the plan, the seven session generators and the push-cap look-ahead read the schedule only through the gate, so an unconsented schedule drives no plan variant and no session push. `POST /users/therapy-schedule/change` is always gated. A full clear is always allowed. `currently_in_therapy` is set only when consent is active (`users.py` PUT, `therapy_schedule_service.py:167-218`).
- **What does not hold:** H-3 item 2 as a server-side backstop. A client without the consent step, a buggy decline path or a crafted request still stores Art. 9 schedule data without consent. Ungated readers still use it: GET, Reflect prompt per the 2026-10-06 operator decision, `weekly_observations`, and the cron in M-3.
- **Remediation:**
  1. Operator and integration-devops: before the first frontend build with the consent step reaches TestFlight, set `ART9_SCHEDULE_GATE_MIN_APP_VERSION` to that build's version, or `ART9_SCHEDULE_GATE_ALL_CLIENTS=true` once the count is small. Add both variables to `.env.example`.
  2. Lead: record the 13.8 branch in SPEC 13.8 and align contract 14.1.3 with the code.
  3. backend-api: if the contract default stands, gate a request that carries a valid header when the minimum is unset, and add a test.
- **Blocks:** the frontend release with the C-card consent flow, not this push (the backend alone changes nothing for shipped clients).

### M-3: m317 revives an hourly AI cron that reads the schedule without the Art. 9 gate

- **Location (outside the diff):** `app/tasks/prep_card_auto_generate.py:106-118` selects every account with an active subscription or trial and a stored `therapy_schedule`. `:224-237` inserts an `InputTypeEnum.AUTO` card and then calls OpenAI with the prep context (conversations, therapy context, Orca memory).
- **Description:** every AUTO insert has failed since 2026-03-28 because prod lacks the `AUTO` label, and the insert comes before the model call, so the cron has done no processing for six months. m317 adds the label. From the next hourly tick, every trial or premium account with a session 23 to 25 hours ahead gets an AI "Before therapy" card, whether or not ARTICLE9_HEALTH consent is active. Every new first-week account is on trial. This contradicts H-3 item 4, SPEC 5 ("read the schedule only through the consent-gated helper") and the `therapy_consent` module docstring. The operator revived the cron deliberately (2026-10-08). The record does not show that the consent gap was part of that decision.
- **Why Medium and not High:** pre-existing code outside this diff. It matches the operator's interim stance of 2026-10-06 that Reflect may use the schedule without Art. 9 pending legal review. It reaches only accounts that hold a schedule without active consent, a population the 13.8 count has not sized yet.
- **Remediation (backend-api, about 10 lines):** call `therapy_consent.consented_schedule_inputs(db, user, prefs=prefs)` in the loop and skip on None. Add a test with withdrawn consent. Preferred before m317 runs. Otherwise the operator accepts in writing that the cron joins the 2026-10-06 stance and the lawyer bundle.

---

## Low findings

- **L-1: Log lines that encode the variant or a missed session.**
  - `plan_service.py:459` `user %s dropped today's step`: only an `after` step can be dropped, so this line says "in therapy, consented, the session today did not happen".
  - `:481` `dismissed the side card`: B or C only.
  - `therapy_schedule_service.py:448-455` `[ScheduleChange] user %s kind=...`: the person has sessions.
  - `users.py:1795` `write refused ... reason=art9_consent_required`.

  Contract section 0 says logs never carry step keys or the variant. **backend-api:** log drop and dismiss through one neutral DEBUG line ("plan state changed"), and the schedule-change and refusal lines at DEBUG. The pre-existing `therapy-schedule updated ... frequency=` line is the same class; it is acceptable at the current level, but do not add more.
- **L-2: Per-person `api_error` on the schedule routes.** The PUT's 403 `art9_consent_required` and the change route's 403, 422 and 503 go through the global handlers (`main.py:220-263`). Each sends `api_error {endpoint, status_code}` with the person's own distinct id: "tried to store a therapy schedule without Art. 9 consent", or "used the session sheet" (a variant-A proxy). Contract 10 says schedule changes from the sheet produce nothing per person. **backend-api:** skip the capture, or send it person-less, for `/users/therapy-schedule*`, the way `NoStoreRoute` does for `/first-week/*`.
- **L-3: Quoted question in the stored system prompt.** `reflect.py:943` stores the OPENING TURN with the literal question in message 0, and every text turn reuses it. RP3-M1 says message 0 holds nothing personal. The extra exposure is small, because the same text is the thread's first Orca message and reaches the model as history anyway. After "Forget this" or a PROFILING withdrawal, though, the paraphrase keeps being sent from the instructions. **backend-api:** make the OPENING TURN refer to "the first message in this thread" without the text, or document the exception next to RP3-M1.
- **L-4: `step_moves` retention.** `first_week_plan_state.step_moves` keeps every record forever, including `dropped` records for `after` steps (plaintext "the session on date X did not happen"), and grows through the rhythm phase. **backend-api:** prune records older than `RESULT_LOOKBACK_DAYS` on every write; the plan never reads them.
- **L-5: `no-store` on the change route.** Contract section 0 asks for `no-store` on every response of `POST /users/therapy-schedule/change`. It is set on handler-produced responses only. 401 or 403 from auth, 422 from body validation and an unexpected 500 lack it, and the global 422 handler echoes the parsed `body` (`main.py:285-297`). The data is the person's own, sent over TLS on a POST. **backend-api:** reuse a `NoStoreRoute`-style wrapper for this route.
- **L-6: Recap job re-enqueue.** `prepare_noticed` releases the 15-minute pending marker in `finally` on every outcome (`recap.py:1104`). The outer-exception and `RecapUnavailable` paths are not counted, so during days 7 to 14 every plan GET can enqueue one more `high` job for that account. No model call happens on those paths, but the jobs compete with interactive work (CLAUDE.md queue note). **data-analytics:** keep the marker until its TTL on any outcome other than done or exists, or count every failure.
- **L-7: No rate limiting.** `GET /first-week/follow-up` decrypts and keyword-scans up to 50 Reflect threads on every call (`follow_up.py:738-760`). From day 10, when the tone key has expired, every recap open repeats a read-only rescan. The load is self-inflicted with the caller's own token. The app has no per-user rate limit (pre-existing). **integration-devops, backend-api:** add a per-user limit at the edge or in a dependency.
- **L-8: Processing before a consumer exists.** After deploy and m318, every new signup gets an anchor. It then gets a follow-up question (one memory note sent to OpenAI, stored 7 days) and, from day 7, a recap observation (the week's data sent to OpenAI). No shipped client shows either one (purpose limitation, Art. 5(1)(b) and (c)). For the lead, outside security: `_is_suppressed_first_calendar_week` drops the first calendar-week summary for every account under 8 days, measured from the anchor or else `created_at`. People on old builds, and accounts that signed up in the days before release (no anchor, so no recap), lose that card and get nothing in its place. **Lead, with data-analytics:** either put generation, the recap sweep and the suppression behind one switch that stays off until the frontend ships, or accept the gap.

## Info

- **I-1: H-2 holds.** One Fernet key per first-week account, padded to 128 bytes, TTL anchor + 9 days for everyone. Writers at every detection point (text message, voice turn, `/end`, `/recap`, the analysis extraction, the idle scan) are silent at INFO and above. The key is rebuilt once with `SET NX`. Readers fail toward "standard" (plan) or toward "flag" (recap). No tone in Postgres, RQ arguments, job results, PostHog or the plan state; the plan-state writer refuses unknown fields without echoing their names. The key is deleted on account deletion and on deletion of the first-conversation thread through both routes (`reflect.py:2590`, `conversations.py:751`).
- **I-2: `_http_exception_handler` header forwarding is safe.** The only `HTTPException` in app code that carries headers is the change route's `no-store` (`users.py:1911-1913`). Framework exceptions carry standard headers only (for example `Allow` on a 405). Keep user data out of exception headers.
- **I-3: `X-App-Version`** is parsed with a bounded regex (up to 32 characters, numeric tuple) and never logged. A malformed minimum is logged without its value.
- **I-4: The follow-up claim key `fw:followup:gen:{uid}`** is not deleted on account deletion. It holds no content and lives 30 minutes. Its existence briefly means "passed the generation gates". Acceptable.
- **I-5: `starter_offer_eligible` depends on tone** (provisional rule 14.1.6, `plan_service.py:136-146`). It is acceptable on the wire. The client must emit no impression that differs by it; action events only. The operator decision is pending.
- **I-6: The follow-up start event and the variant.** `reflect_session_started {seed_source: first_week_followup}` on plan day 6 (`talk2`) can only come from B or C. The contract (section 10) accepts it; it is the design-audit M-1 class and belongs in the lawyer bundle.
- **I-7: Rule 14.1.5** (a consented schedule write sets `currently_in_therapy`) is implemented on both routes with no log and no event, and only with active consent. Accuracy note for the lead: it overwrites `not_right_now` or `never_been` when a consented person adds a session.
- **I-8: m317** adds labels only, in an autocommit block, idempotently, with no table DDL and nothing on the boot path. The migration itself raises no security concern; its effect is M-3.
- **I-9: m318** adds no tone column and only `String`, `Text`, `Boolean` and timestamp columns. Both new tables have FK `ON DELETE CASCADE` and no ORM back-relationship. Both new columns are excluded from their mappers. It sets `lock_timeout`, is idempotent and calls no `bind.commit()`. The follow-up table holds at most one row per account (`replace_existing`). Offline Postgres DDL compile tests exist and pass.
- **I-10: Right to portability.** Still no data export (pre-existing). When it is built, include plan state, `skipped_dates` and the follow-up question.
- **I-11: Ungated schedule readers that remain** (pre-existing; decided or out of scope): `GET /users/therapy-schedule` (contract), the Reflect and first-conversation prompts (operator 2026-10-06), `weekly_observations`, the therapy-day checks in `hero_insight`, `period_snapshots`, `personal_bio` and `therapy_tracking_signal`, and `premium_intent`. They go to the lawyer bundle together with M-3.
- **I-12: Redis transport.** TLS for `REDISGREEN_URL` (design review L-5) is still unverified, and the new keys depend on it. Owner: integration-devops.

---

## Answers to the lead's checklist

1. **Auth and scoping.** Every route uses `Depends(deps.get_current_user)`, and there is no user id in path, query or body: `/first-week/plan` GET, `/today/defer`, `/today/defer/undo`, `/today/drop`, `/plan/hide`, `/side-card/dismiss`, `PUT /rhythm`, `PUT /reminder`, `/checkin-baseline`, `/follow-up`, `/recap`, `POST /users/therapy-schedule/change`. The Reflect follow-up start is the existing token-scoped route. Mutation bodies use an empty `extra="forbid"` model; `FirstWeekRhythmUpdate`, `FirstWeekReminderUpdate` and `TherapyScheduleChangeRequest` are `extra="forbid"` with Literal enums and patterns. Nothing on SPEC 4's forbidden list is settable. The plan-state writer has an allowlist.
2. **H-1 (tone, step, variant).** The variant stays inside `PlanResult.internal_variant_do_not_serialize`; it is never rendered, logged or sent. Tone appears only as `tone` and `support_link` on the plan, as allowed. Copy keys are tone-agnostic. No PostHog event was added. The open problems are a Postgres-length channel (H-1 above), model-call traces (M-1) and log lines (L-1).
3. **H-2.** Holds (I-1). The exception is H-1, which is a Postgres trace of the calm branch, not of the key.
4. **H-3 / 13.8.** The plan (`therapy_schedule_if_consented`), all seven generators and the look-ahead (`consented_schedule_inputs`) are gated. The change route is always gated. A clear is allowed without consent. 14.1.5 holds. `X-App-Version` is never logged. Open: the default PUT gate is off (M-2), and m317 revives an ungated cron (M-3).
5. **Follow-up.** Generated only from a live memory item written from the oldest onboarding thread, within 3 days of the anchor, with `memory_extraction_gate == allowed`, a crisis-free recap and turns, and standard tone. The note is fenced and neutralized, and the output is validated (one question, no `<>`, no dashes, crisis rescan including second-person wording). It is stored Fernet-encrypted, at most one row per account, with 7-day expiry and a daily purge at 04:40 UTC registered in the lifespan (guarded). Display checks: `profiling_withdrawn`, crisis rescan of the question and the item, the item still exists, the recap cache, and all Reflect threads since the anchor; any failure gives the calm question. "Forget this" and "Forget everything" hard-delete items, so the FK cascade removes the row. PROFILING withdrawal deletes it explicitly as well. Account deletion and thread deletion cascade. Open: the copies inside the follow-up thread (H-1, L-3).
6. **Recap.** "Noticed" is crisis-screened at creation and display (with second-person wording), hidden after any flag (fail closed on Redis), dropped when a source changed (fingerprint), and `in_timeline` is always false (truthful). `mentioned` uses `memory_extraction_gate`, live items only, crisis-screened. The prefetch runs in `BackgroundTasks` after the response, swallows everything and logs only user id and exception class. The cache is padded, encrypted and dropped on account deletion with its pending and failure keys. Volume: L-6.
7. **GDPR coverage.** See the table below.
8. **Logging.** No push text, symptom names, scores, memory text, session dates (design L-4 is closed: frequency and count only) or tone/step values. Open: L-1, and M-1's INFO line.
9. **Boot safety.** All three routers are imported under `except Exception`. The models and schemas import only the stdlib-only plan engine. The new columns are excluded from the mappers. The lifespan job is guarded. 503 instead of 500 before migration is tested. `no-store` covers success, 204, 4xx, 401/403, 422 and 503 on every `/first-week/*` route (`NoStoreRoute`), which also keeps `api_error` off them. The change route is the exception (L-5).
10. **Analytics.** `symptom_scored` is now `{symptom_id}` only (contract Q9 resolved). `onboarding_symptom_sync_missing_ratings_fallback {area_count}` now fires only for a genuinely missing key. No new backend event. The follow-up start event is identical for every question kind. Residual: L-2, I-6.
11. **WP-0 leftovers.** See below.

## Horizontal privilege escalation audit

| Route / read | Scoping | Result |
|---|---|---|
| `GET /first-week/plan` and all 7 mutations | Token uid only; every read in `plan_loader` / `first_week_reads` filters by `user_id`; the row lock is on the caller's plan-state row | Pass |
| `GET /first-week/checkin-baseline` | `UserTherapyContext`, `UserSymptom`, `SymptomScore` filtered by the token uid | Pass |
| `GET /first-week/follow-up` | Row selected by uid, no id parameter; 404 alike for missing and other | Pass |
| `GET /first-week/recap` | Uid only; `mentioned` ids are the caller's own; "Not right" uses the existing `DELETE /users/memory/{id}`, which is scoped by user (404 for another account's item) | Pass |
| `POST /reflect/start` with the follow-up seed | Question resolved server-side; `seed_id` / `seed_label` ignored; the double-tap lookup filters by uid | Pass |
| `GET /reflect/{id}/session-data` follow-up opening | Thread ownership checked before the seed read | Pass |
| `PUT /users/therapy-schedule`, `POST /users/therapy-schedule/change` | Token uid; `SELECT ... FOR UPDATE` on the caller's preferences row | Pass |
| Symptom ids (check-in saves) | Existing `POST /symptoms/{id}/scores`, 404 for another account's symptom | Pass (unchanged) |

## GDPR compliance status

| Requirement | Status | Notes |
|---|---|---|
| Right to erasure | Pass | `users.first_week_started_at` and `user_preferences.skipped_dates` live on rows deleted with the user. `first_week_plan_state` and `first_week_follow_ups` use FK cascade (tested). `fw:state`, `fw:recap`, the pending and failure keys are deleted in step 7h. The follow-up claim key holds no content and expires in 30 minutes (I-4). RQ arguments carry ids only; jobs return nothing. |
| Data minimisation | Partial | One follow-up row per account, 7 days. Open: H-1, M-1, L-3, L-4, L-8. |
| Consent for processing | Partial | The plan, generators and look-ahead are Art. 9 gated, and the follow-up uses the memory gate. Open: M-2 (default off), M-3 (cron revived by m317). |
| Encryption at rest | Pass with exception | Question, tone and recap are Fernet-encrypted (tone and recap padded). Exception: the length channel in H-1. |
| Retention | Partial | Follow-up: 7 days plus daily purge. Tone: anchor + 9 days. Recap cache: anchor + 16 days. Plan state: no limit (L-4). `token_usage_log`: no limit (M-1). Moment purge still unscheduled (WP-0 M-3). |
| Right to portability | Not available | Unchanged (I-10). |
| Transparency | Notes | Add the follow-up question and the day-7 observation to the pending privacy-policy update, next to memory. |

## Status of the WP-0 leftovers

| Item | Status |
|---|---|
| M-1 (moment events per person) | Resolved in 8eb8d3f (`moment_privacy`). This diff adds `FIRST_WEEK_STEP` to the health-revealing set. |
| M-2 (look-ahead ungated) | **Resolved in this diff** (`push_cadence._anticipated_session_rank` through `consented_schedule_inputs`; skips honoured; tested). |
| M-3 (moment purge has no caller) | **Open.** `purge_old_terminal_moments` is still not scheduled. Plan-step moments will add to the same table. |
| L-1 (cap log reveals session days) | Resolved in 8eb8d3f (`outcome=` only). Unchanged here. |
| L-2 (AST guard name-only) | Open (qa-testing). |
| L-3 (PRIVATE is defense in depth) | Backend comment reworded (`notification_service.py:68-76`). The client foreground `visibility` is frontend work, not verified here. |
| L-4 (Pass 1 probe vs persist) | **Resolved in this diff** (`notification_orchestrator.py:846`, the cap is re-checked at the persisted instant). |
| L-5 (dead legacy senders) | Open (`notification_service.py:457`, `:722`, `:880`). |
| L-6 (timing residual, privacy notice) | Open (operator). |
| Design L-4 (`next=` date in the PUT log) | Resolved (frequency and count only). |

## Conditions for this deploy

1. **Before running m317:** the operator decides M-3. Preferred: backend-api gates the auto prep-card cron in this push. Otherwise, written acceptance that it joins the 2026-10-06 stance and the lawyer bundle.
2. **qa-testing** runs the full backend suite on a021da9 (plus any fix) before the push. I ran 14 targeted suites, 2563 tests passed.
3. **Deploy equals migrate:** run `heroku run alembic upgrade head` (m317, then m318) immediately after the push. Read-only checks afterwards: `alembic current` is m318a1b2c3d4; `GET /first-week/plan` for an old account returns 204; `/users/usage` carries `free_limit`; the change route stops answering 503; no 500s on `/users/*` in the logs during the gap.
4. **H-1:** fixed in a backend push before any frontend build that starts follow-up threads reaches TestFlight. Recommended: in this push.
5. **M-2:** gate configuration set and SPEC 13.8 recorded before the frontend build with the consent step ships.
6. **M-1:** fixed this sprint. It is live for new signups from the moment m318 runs.
7. **L-8:** lead decision (switch until the frontend ships, or accept).

No Critical finding. The single High is latent until the WP-3 frontend release, so this report does not block pushing a021da9 and running m318. Running m317 additionally waits for the operator's M-3 decision.

## Remediation priority

1. **Now (this push, recommended):** H-1 (data-analytics, backend-api), M-3 gate (backend-api).
2. **Before the WP-2/WP-3 frontend release:** H-1 if it is not done now (blocking), M-2 configuration and contract alignment (operator, integration-devops, backend-api), L-2 (backend-api).
3. **This sprint:** M-1 (data-analytics, backend-api), L-1, L-3, L-4, L-5 (backend-api), L-6 (data-analytics), WP-0 M-3 purge scheduling (backend-api).
4. **Backlog:** L-7 (rate limit), WP-0 L-2 and L-5, I-10 export, I-12 Redis TLS check.
5. **Lead or lawyer:** L-8, I-5, I-6, I-7, I-11, WP-0 L-6.
