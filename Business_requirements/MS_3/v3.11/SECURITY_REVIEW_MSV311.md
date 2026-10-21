## Security Audit Report – MSV3.11 backend batch (CS-01, CS-02, CS-07, CS-10, CS-11) – 2026-09-02

Scope: `git diff 7dddf38..f64216c` in `Heroku/wt-be-int` (branch `msv3.11`, HEAD `f64216c`, base `main` 7dddf38 / prod v544). Read-only review, no code changed.

### Executive Summary

This batch adds one new table (`reflect_summary_cards`, CS-02), one new self-referential column pair on `threads` (`parent_thread_id`, `narrative`, CS-01), an AI-matching call that reads only the caller's own threads, and a set of notification-eligibility / to-do-recurrence correctness fixes (CS-07, CS-10, CS-11). Every new and changed endpoint enforces `Depends(deps.get_current_user)` (48/48 routes in `workspace.py`, 14/14 in `reflect.py`), every new CRUD function filters by `user_id`, encryption-at-rest parity with `BetweenSessionNote` is exact, GDPR cascade-delete is wired at the DB FK level for the new table, and PostHog events carry no conversation content. No Critical or High findings. One Medium finding (missing cost/abuse throttle on a synchronous AI-generation endpoint for premium/unlimited users) and one Low finding (a narrow TOCTOU race on duplicate summary-card creation). **Verdict: GO** – deploy is not blocked; address MED-001 within the current sprint per CLAUDE.md's Medium-severity guidance.

### Critical Findings

None.

### High Findings

None.

### Medium Findings

#### MED-001: No cost/abuse throttle on `POST /reflect/{conversation_id}/summarize` for unlimited-message (premium) users
- **Severity**: Medium
- **Location**: `app/api/v1/endpoints/reflect.py:818-890` (`summarize_reflect_thread`), `app/services/reflect_summary.py:139-292` (`generate_reflect_summary_card`, `MIN_USER_MESSAGES_REPEAT_SUMMARY = 1`)
- **Description**: Each call to `/summarize` triggers a synchronous OpenAI structured-generation call (`openai_service.generate_between_session_note`) plus an embedding call on the triggering message. The only two guards against rapid repeated calls are (a) `ReflectSummaryTooShortError` – needs only **1** new user message since the previous summary (`MIN_USER_MESSAGES_REPEAT_SUMMARY = 1`) – and (b) the in-flight 409/`PROCESSING`-row guard, which only blocks a call while a *previous* call is still actually executing (or younger than the 180s stale window), not sequential rapid-fire calls. `POST /{conversation_id}/message` enforces `settings.REFLECT_MONTHLY_MESSAGE_LIMIT` (30) for free-tier users, but for a premium user `remaining = ... if not premium else 999999` – i.e. **no cap at all**. Because a summarize call only requires one trivial message first, a premium (or trial/compromised) account can script: send a 1-character message → call `/summarize` → repeat, generating unlimited billed OpenAI calls with no throttle, no daily cap, and no per-user quota check anywhere in this endpoint.
- **Impact**: Cost-abuse / resource-exhaustion vector scoped to a single compromised or malicious premium account (not a cross-user data exposure). At scale this is a direct OpenAI billing risk and, since generation is synchronous inside the request/response cycle, a sustained burst from one account also ties up web-dyno request slots for the duration of each GPT call.
- **Reproduction Steps**: As a premium user, in a loop: `POST /reflect/{id}/message` with 1 char of text, then `POST /reflect/{id}/summarize`; repeat as fast as OpenAI responses allow. No 429/403 is ever returned.
- **Remediation**: Add an explicit per-user throttle on `/summarize` – e.g. reuse `track_usage`'s existing bucket to enforce a daily/hourly cap (independent of premium status), or require a minimum elapsed-time / minimum-new-message-count gate scaled with the number of summaries already generated today. A simple `X summaries per user per rolling 24h` check in `generate_reflect_summary_card` (mirroring the `REFLECT_MONTHLY_MESSAGE_LIMIT` pattern) is sufficient; it does not need to block legitimate repeat-summarize usage, only sustained scripted abuse.
- **Owner**: `backend-api`

### Low Findings

- **LOW-001 – TOCTOU race on duplicate summary-card creation**: `generate_reflect_summary_card` (`app/services/reflect_summary.py:156-176`) reads the latest card, checks it isn't `PROCESSING`, then creates a new `PROCESSING` row – this check-then-create is not atomic. Two genuinely simultaneous requests (e.g. a double-tap or a retried client request that isn't actually cancelled) can both pass the check before either commits, producing two concurrent OpenAI calls and two cards instead of one being rejected with 409. Impact is wasted cost and a harmless duplicate card, not data exposure or cross-user leakage. Recommend a `SELECT ... FOR UPDATE` on the latest-card lookup or a partial unique index (`conversation_id` where `processing_status='processing'`) if duplicate-card reports start showing up in practice; not blocking. Owner: `backend-api`, backlog.
- **LOW-002 – `parse_timezone`/tz_str inputs are user-controlled and unvalidated at write time**: `get_todo_period_start_utc` (`app/utils/time_utils.py`) and `get_user_period_context` (`app/crud/workspace.py`) feed `UserPreferences.time_zone` straight into timezone parsing for every to-do read/write path (list, done, undone, overview). This is pre-existing behavior (not introduced by this diff) extended to more call sites; a malformed stored timezone string would raise inside a request rather than leak data. No new vulnerability, but worth a backlog note to validate `time_zone` at the point it is written (`PUT` preferences, owned by `backend-api`, out of this diff's scope) rather than trusting it at every read.

### GDPR Compliance Status (delta introduced by this batch)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Right to erasure | OK | `reflect_summary_cards.user_id` FK is `ON DELETE CASCADE` (migration `m311c3d4e5f6`); account deletion (`app/api/v1/endpoints/users.py:1685`, `db.delete(user); db.commit()`) relies on the DB-level cascade exactly as documented in that function's own comment ("DB FK ON DELETE CASCADE handles all children") – verified this now also covers the new table. `threads.parent_thread_id` uses `ON DELETE SET NULL` (orphan-promotion of sub-threads to mains), which is correct because parent and child always belong to the same user and are deleted together anyway. |
| Data minimization | OK | No new PII field added. `ReflectSummaryCard` stores only AI-generated summary/questions/action-items/threads text, encrypted, same shape as `BetweenSessionNote`. |
| Right to portability | Unaffected | No existing export endpoint was touched by this batch; new table not yet wired into any export path if one exists – not in scope, flag for a future round if a data-export feature is added. |
| Consent for processing | Unaffected | No new third-party data flow; OpenAI call pattern (structured generation, encrypted storage) matches existing Reflect/between-session mechanisms. |
| Data encryption at rest | OK | `ReflectSummaryCard.summary/questions/action_items/threads` and `Thread.narrative` all go through the existing Fernet-based `encode()`/`decode()` (`app/services/encode_service.py`) – confirmed parity with `BetweenSessionNote`, not a new/weaker mechanism. |
| Retention policy | OK | Soft-delete (`deleted_at`) + 24h restore window + background hard-purge after the retention cutoff, implemented identically to every other timeline card type (`app/crud/crud.py` purge functions around line 4674-4760); reflect summary cards have no separate RAG documents to clean up (explicitly noted in code – not indexed to RAG in this slice). |

### Horizontal Privilege Escalation Audit

Every endpoint below was checked for (a) a `Depends(deps.get_current_user)` auth dependency and (b) a `user_id`-scoped query/CRUD call for every read, write, or delete of another user's row.

| Endpoint | Ownership check | Verdict |
|---|---|---|
| `POST /reflect/start` | writes `user_id=current_user_id` on the new Conversation | OK |
| `GET /reflect/starters?thread_id=` | re-verifies `thread_id` ownership (`Conversation.user_id == current_user_id`) before reading any conversation content | OK |
| `GET /reflect/summaries/{card_id}` | `crud.get_reflect_summary_card(db, card_id, current_user_id)` – filters by `user_id` | OK |
| `POST /reflect/{id}/message`, `/messages`, `/end`, `/session_data`, `/audio/*`, `DELETE /{id}` | every one filters `Conversation.user_id == current_user_id` (and `conversation_type == REFLECT`) before use | OK |
| `POST /reflect/{id}/summarize` | same conversation-ownership filter, then `generate_reflect_summary_card` only ever reads/writes rows already scoped through that conversation | OK |
| `GET /reflect/{id}/summaries` | conversation-ownership filter + `crud.get_reflect_summary_cards_for_conversation(..., user_id)` | OK |
| `crud.get_reflect_summary_card / get_latest_reflect_summary_card / get_reflect_summary_cards_for_conversation / update_reflect_summary_card / soft_delete_reflect_summary_card / restore_reflect_summary_card` | all filter by `user_id` | OK |
| `POST /workspace/threads` (manual "+ Dodaj wątek") | `_match_and_create_thread` calls `ws_crud.get_thread(db, matched_main_id, user_id)` to **re-verify** the AI-returned `matched_main_id` belongs to the caller before attaching a sub-thread to it – defense-in-depth on top of `match_thread_for_content` already only sourcing candidates from `ws_crud.list_open_main_threads(db, user_id)` | OK |
| `POST /workspace/triage/{proposal_id}/toggle` (thread branch) | `proposal = ws_crud.get_triage_proposal(db, proposal_id, current_user_id)` scoped before any thread creation/matching | OK |
| `app.services.thread_matching.match_thread_for_content` | candidate set is `ws_crud.list_open_main_threads(db, user_id)` (filtered by `user_id`); `matched_thread_id` returned by the LLM is checked against `id_set` built from that same candidate list – a hallucinated or prompt-injected id outside the caller's own threads is rejected and falls back to "new main thread" | OK – see prompt-injection note below |
| `app.tasks.thread_context.generate_sub_thread_narrative` / `crud_workspace.get_latest_sub_thread(main_thread_id)` | `get_latest_sub_thread` itself takes no `user_id`, but its only caller passes a `main_thread` already fetched via the scoped `get_thread(db, matched_main_id, user_id)` – no reachable path passes an unverified id | OK (verified caller chain) |
| `app.tasks.thread_context.regenerate_thread_context(thread_id, user_id)` | `crud_workspace.get_thread(db, thread_id, user_id)` at job start | OK |
| Todo endpoints (`/workspace/todos*`, done/undone/archive/restore/pin) | unchanged ownership pattern (`ws_crud.get_todo_item(db, item_id, user_id)`), now additionally self-heals via `get_user_period_context(db, user_id)` – still scoped | OK |
| `fetch_todo_repeat_context_for_prompt(db, user_id)` (Reflect system-prompt injection) | queries `TodoItem.user_id == user_id` only | OK |
| `GET/PUT /users/therapy-schedule` | unchanged `current_user_id` scoping; `TherapyScheduleUpdate.schedule` now `Optional` but every write path still keys off `current_user_id` | OK |
| `GET /therapy-tracking/session-state` | unchanged auth/scoping; only the `no_therapy_set` guard's boolean logic changed | OK |
| Timeline `reflect` type (`GET`, `DELETE .../soft-delete`, `POST .../restore`) | `crud.soft_delete_reflect_summary_card` / `restore_reflect_summary_card` both filter by `user_id`; `_fetch_reflect_summaries_for_timeline` filters by `user_id` | OK |

No endpoint in this diff accepts a `user_id` from the request body for ownership purposes; every ownership check derives from the verified Firebase token via `deps.get_current_user`.

**Prompt-injection note (CS-01 AI matching)**: `thread_matching.py`'s structured output (`ThreadMatchResult`) is Pydantic-typed and the returned `matched_thread_id` is validated against the exact candidate-id set sent in the prompt (`id_set`, itself scoped to `user_id`) before being trusted (`hallucinated_id` fallback otherwise). Even a successful prompt-injection attempt inside a user's own thread title/content (the only attacker-controlled input here – it can only be the *same* user's own data) cannot cause data to merge into another user's thread tree, because the candidate pool and the post-hoc validation are both hard-scoped to the caller. Worst case of a successful injection is a wrong merge within the attacker's own threads, which is a correctness concern, not a security one.

### Remediation Priority List

1. **Critical** – none.
2. **High** – none.
3. **Medium** – MED-001 (add a cost/abuse throttle on `POST /reflect/{id}/summarize` independent of premium status). Fix within current sprint per CLAUDE.md's Medium-severity guidance; does not block this deployment.
4. **Low** – LOW-001 (TOCTOU on duplicate summary-card creation), LOW-002 (unvalidated `time_zone` string at read time, pre-existing pattern extended). Backlog.

### Deployment Verdict

**GO.** No Critical or High findings in the CS-01 (Threads), CS-02 (Reflect summary card), CS-07 (To-do recurrence), CS-10 (Therapy schedule), or CS-11 (Notification cycle fixes) surfaces. Ownership scoping, encryption-at-rest, GDPR cascade-delete, and auth enforcement are all correct and consistent with existing patterns in the codebase. MED-001 should be picked up promptly but is a cost/availability concern scoped to individual compromised accounts, not a data-exposure risk, and does not need to block this release per the project's own severity-vs-deployment-block policy.
