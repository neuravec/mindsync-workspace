# Orca memory backfill for existing users

Operator request 2026-10-05: existing users who already have conversations and entries open "What [Orca] remembers" and see "Nothing here yet". Orca must look back at their history once and build their notes. Context: `SPEC.md` in this folder, `audit-security.md` (all guards stay), `DEPLOY.md`. Backend v558 is live with `MEMORY_EXTRACTION_FOR_EXISTING_USERS=true` (operator approved after legal review).

## 0. Hard rules
Same as SPEC.md section 0. New branches: backend `feat/orca-memory-backfill` from `main` (cc8288b), frontend `feat/orca-memory-backfill` from `dev` (0031c44). Commit only your paths (`git commit -- <paths>`), never `git add .`, never push. No U+2014/U+2013 in copy, prompts or reports. Tests are part of the task. No `run_in_background`.

## 1. Behaviour
- One backfill per account, ever. It reads the person's history (newest first, bounded) and writes up to 12 durable notes with the existing categories, via `create_memory_items(..., source="backfill")`.
- History sources (use summaries where they exist, raw text only where there is no summary): Reflect conversation summaries and summary cards, journal conversation summaries, After therapy (debrief) cards, Before therapy (prep) cards, Between Sessions notes, session recording and voice note summaries, active goals. NOT the Personal Bio (it is derived, avoid circularity), NOT onboarding answers (already in prompts).
- Bounded digest: newest first, last 12 months, about 30k characters max, one cheap-model JSON call per person (`GPT_MODEL_MINI`), fenced as untrusted data. No call when the digest is empty: mark done.
- All existing guards apply: PROFILING withdrawn = no call, status `unavailable`; nothing created before `memory_forgotten_at`; suppressions (inside `create_memory_items`); crisis: any source chunk that matches the crisis scan is dropped from the digest, and if the model flags crisis or a fact contains crisis language, that fact is dropped (never the whole backfill); the 30-item cap.
- After a successful backfill, advance the extraction watermark of every Reflect thread included, so later per-thread extraction does not re-mine the same turns.
- Marked done durably (`users.memory_backfilled_at`), so "Forget everything" can never be undone by a re-run.

## 2. Triggers
- On demand: the memory screen asks for it (endpoint below), enqueued on the `high` queue.
- Background sweep: a scheduler job every 15 minutes on `default` (offset from the idle-analysis minutes, e.g. 5,20,35,50) backfills up to 20 not-yet-backfilled accounts per tick that had any activity in the last 365 days, newest activity first, bounded so it never monopolizes the single worker. Self-draining; no manual command.

## 3. API contract (additive)
- `GET /api/v1/users/memory` adds `"backfill_status": "not_started" | "running" | "done" | "unavailable"`.
  - `done`: `users.memory_backfilled_at` is set. `running`: a Redis marker `orca:memory:backfill:running:{uid}` (TTL 10 min) exists. `unavailable`: PROFILING withdrawn, the column is missing (before migration), the memory gate blocks the account (flag off and no memory notice), or 3 failed attempts are used up. Otherwise `not_started`.
- `POST /api/v1/users/memory/backfill` (empty body, owner = current user): `not_started` → set the running marker, enqueue on `high`, 202 `{"backfill_status": "running"}`; `running` → 202 same; `done` → 200 `{"backfill_status": "done"}`; `unavailable` → 200 `{"backfill_status": "unavailable"}`. Never 5xx for a Redis or queue failure: return `not_started` and log.
- Account deletion and PROFILING withdrawal also clear the running marker.

## 4. Interfaces between agents
- backend-api: migration `m316...` (down_revision `m315a1b2c3d4`): `users.memory_backfilled_at TIMESTAMPTZ NULL`, excluded from the ORM mapper like the m315 columns. CRUD in `app/crud/user_memory.py`: `get_memory_backfilled_at(db, user_id) -> Optional[datetime]`, `mark_memory_backfilled(db, user_id, *, now=None) -> bool` (only sets when NULL; degrades to False if the column is missing). Running-marker helpers `set_backfill_running(user_id)`, `clear_backfill_running(user_id)`, `is_backfill_running(user_id) -> bool` (Redis, best effort). Endpoint + `backfill_status`. Registration of the sweep job in `rq_scheduler_setup.py` + `main.py` lifespan (boot-safe, idempotent, stable job id `mindsync_orca_memory_backfill_sweep`). The endpoint enqueues the dotted path `app.tasks.orca_memory_backfill.backfill_user_memory` with the user id.
- data-analytics: `app/services/orca_memory_backfill.py` (digest builder over the sources, prompt, parsing, guards, write, watermark advance) and `app/tasks/orca_memory_backfill.py` with `backfill_user_memory(user_id: str) -> dict` (idempotent: returns early when already done; always clears the running marker in `finally`; calls `mark_memory_backfilled` only after a successful write or an empty digest; on LLM failure leaves it not done so the sweep retries later, max 3 attempts tracked in Redis) and `sweep_memory_backfill() -> dict` (selection query + per-user enqueue on `default`). Backend event `orca_memory_items_saved` `{count, source: "backfill"}`; no text, no crisis.
- flutter-mobile: memory screen states (section 5).

## 5. Frontend
- On open, read `backfill_status`. `not_started` → call `POST /users/memory/backfill` and show the reading state. `running` → reading state, poll `GET /users/memory` every 4 s for up to 90 s, then show "This is taking longer than usual. Check back in a few minutes." with a retry. `done` → list, or the existing empty state if still empty. `unavailable` → the existing empty state.
- Reading state copy (EN source, 7 languages, calm, no U+2014/U+2013): title "[Orca] is looking back", body "[Orca] is reading your past conversations and entries to pick out what's worth remembering. This takes about a minute." Skeleton note cards, accessible live region.
- Events: `orca_memory_viewed` gains status values `backfilling` and `backfill_slow`; new `orca_memory_backfill_requested` (no properties) fired once when the POST is sent. No free text.

## 5b. First-conversation fixes riding in the same batch (operator device test 2026-10-05)
- Prompt (data-analytics, `app/services/first_conversation.py`): part 1 = exactly one question per topic, one short reflecting sentence, then the next question in the same turn; no follow-ups in part 1 (something big gets one warm sentence and "we can come back to it"); after question 3 an explicit two-sentence transition: thanks for sharing, the questions are done, the rest is an open conversation about anything, end it whenever you like. Part 2 unchanged. Safety overrides all.
- Phase indicator (flutter-mobile): fix the realtime tool path (handle `response.function_call_arguments.done` and `response.done` function_call items) AND add a deterministic turn-based driver (answer 1 → 2 of 3, answer 2 → 3 of 3, answer 3 → open); tools may only move it forward earlier.
- Pricing (backend-api): add `gpt-realtime-2.1` and `gpt-realtime-2.1-mini` prices (usage tracking logged $0).
- Known, not in this batch: `POST /users/profile` returns 500 UniqueViolation on onboarding rerun (client recovers with PUT); should be 409 or an upsert.

## 6. Done when
Each agent: tests (incl. guards: consent withdrawn, forgotten_at, suppression, crisis chunk dropped, cap, idempotency, watermark advance, sweep bounded, endpoint statuses, Redis down), boot import, Postgres DDL compiled offline for the migration, full suite vs baseline (backend: 9 known failures; frontend: run per directory), PostHog coverage table, impact recon. Then lead: security-guardian quick review, qa-testing, deploy with operator approval (push main, `alembic upgrade head` immediately, then frontend to dev).
