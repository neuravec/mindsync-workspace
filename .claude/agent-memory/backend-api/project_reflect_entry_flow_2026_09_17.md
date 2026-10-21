---
name: project-reflect-entry-flow-2026-09-17
description: Reflect entry flow backend (mode choice, topic seeding, modality) - the ORM-deferred-column trick that makes an additive column on a hot table survive Heroku's push-then-migrate window, plus SQLite test gotchas hit along the way
metadata:
  type: project
---

Commit `d3aca01` on `main` in the MindSync backend repo, NOT pushed (lead pushes).
Migration `m314b2c3d4e5` (down_revision `m313a1b2c3d4`) adds
`conversations.modality` String(8), `.seed_source` String(24), `.seed_label` Text
(Fernet). New modules: `app/services/reflect_entry.py`, `app/crud/reflect_entry.py`,
`app/tests/test_reflect_entry_flow.py` (65 cases).

**Why:** the Flutter app was dropping users straight into a thread list with voice
hidden behind a tiny icon. The new entry screen offers voice vs text plus up to
three topics from therapy context. Modality has to be persisted so tapping an
existing thread resumes it in the mode it was last used in.

**How to apply:** the pieces below generalise well beyond this feature.

## Adding a column to a HOT table on Heroku: exclude_properties, NOT deferred

`conversations` is read by 20 modules. Heroku has no release phase and
`heroku run alembic` executes from the CURRENTLY DEPLOYED slug, so the migration
file only exists on the dyno AFTER the push: migrate-before-deploy is impossible
and the pre-migration window is unavoidable.

**I got this wrong first and shipped the wrong claim into two docstrings.**
ORM `deferred()` governs LOADING only. Measured against a database with the
columns physically dropped:

| shape | deferred | exclude_properties |
|---|---|---|
| default entity SELECT | PASS | PASS |
| `Query(Entity).count()` | **FAIL** (wraps the full entity in a subquery) | PASS |
| ORM flush INSERT | **FAIL** (unit of work names every mapped column) | PASS |
| explicit Core read of the column | FAIL (correct, that site is guarded) | FAIL (same) |

So deferral left thread creation broken for Reflect AND the journal, plus
`get_user_data_richness` (a `count()`) which sits on both voice `session_data`
routes. The fix:

```python
modality = Column(String(8), nullable=True)      # stays on the Table
__mapper_args__ = {"exclude_properties": ["modality", "seed_source", "seed_label"]}
```

Table keeps the column so `create_all` and Alembic autogenerate still work; the
ORM cannot name it in any statement. All access goes through Core
(`Entity.__table__.c.x`) in guarded crud helpers.

**Sharp edge:** `Entity(modality="voice")` does NOT raise after exclusion.
Declarative `__init__` setattrs anything it is handed, the name is not
instrumented, and the value is **silently discarded**. Three of my own test
fixtures were doing exactly that. Pin it with a test.

Also: `Entity.column` still exists as a bare `Column` (not an
`InstrumentedAttribute`), so `hasattr` is True. Assert
`not isinstance(attr, InstrumentedAttribute)` and absence from
`__mapper__.columns` / `all_orm_descriptors`, not `hasattr`.

**Verification that actually catches this**: compiling statements is not enough,
because `insert(Entity)` as a Core construct names every Table column whatever
the mapper thinks. Capture the REAL flush via a `before_cursor_execute` event
listener, and physically `ALTER TABLE ... DROP COLUMN` in a test database and
drive the real HTTP routes. See `app/tests/test_reflect_entry_pre_migration.py`.

## Rollback sweep of reflect.py (commits `99b02f1`, `5479dcf`, `7f981ee`)

Three passes, each scoped by the operator rather than fixed wholesale. Fixed so
far: both embedding handlers, `_get_rag_context`, and the three optional context
blocks in `_build_reflect_system_prompt`. **Still open on a follow-up ticket**:
the voice-director block in `send_reflect_message` (sits before that handler's
commit, so it is the last genuinely reachable 500 in this file), the
`conversation.title` read after the try in `end_reflect_thread`, and eleven
read-only or post-commit blocks. AST scan count went 16 unguarded -> 13.

Triage rule that made the scoping arguable: a try block only causes a 500 if a
`db.commit()` or an ORM attribute read happens after it **in the same request**,
which can be in the CALLER, not just the same function. The
`_build_reflect_system_prompt` trio looked harmless to an intra-function scan
and was actually the highest priority, because `/start` commits the system
message immediately after.

**Contract-enum tuples beat bare string literals.** Declaring
`SEED_REJECTION_REASONS` in the crud module and
`OPENING_QUESTION_FAILURE_REASONS` in the endpoint, then having the privacy test
assert its allowed vocabulary covers both exhaustively, means a future fifth
value fails the test instead of silently sailing past the free-text assertions.
Verified by temporarily adding one.

## What the security audit caught that I missed (MED-001, commit `2579a9e`)

I turned an AI-free endpoint into one that issues a billed completion and
shipped it with nothing in front of the call. Worth remembering as a checklist,
because none of the three holes were obvious while writing the feature:

- **A "resolved" object is not an authorised one.** `resolve_seed` returned a
  perfectly valid seed built from a client-supplied label with no row lookup at
  all. Anything that gates spend must test a flag that is set ONLY on the branch
  that actually verified ownership (`verified_owner`, defaulting to False), not
  a proxy like "the object is not None" or "source_id happens to be set".
- **Gates live where the feature was, not where the cost is.** The Reflect
  monthly limit is in `send_reflect_message`; the new AI call was in `/start`,
  which nobody had ever needed to gate. Adding an AI call to an endpoint means
  re-asking who is allowed to trigger it, from scratch.
- **`ThreadPoolExecutor` queues without limit.** The bounded `max_workers` I
  added earlier bounded CONCURRENCY, not ADMISSION, so a burst queued and each
  queued caller then reported a timeout for a call that never started, which
  would have read as an OpenAI fault in the dashboard. Fix is a
  `BoundedSemaphore` acquired non-blocking, released by the WORKER in a finally
  so a slot tracks real in-flight spend rather than who is still waiting.
- **`future.result(timeout=...)` abandons the caller, never the task.** The real
  billing bound has to be at the HTTP layer. `gpt_function` is wrapped in
  `retry_on_exception(max_attempts=5)`, so an abandoned call could bill five
  times; calling `client.with_options(timeout=..., max_retries=0)` directly and
  logging tokens by hand is the way to bound it without touching
  `openai_service.py` (data-analytics owns that file).

Rate limiting DOES already exist in this repo: `app/services/clinician_rate_limit.py`,
Redis INCR + `expire(nx=True)`. Reuse the pattern. Note it fails OPEN by design
(guards feature access); a spend gate should fail CLOSED, and that divergence is
worth stating in the code.

## Things that would have bitten later

- `ThreadPoolExecutor` used as a context manager DEFEATS a `future.result(timeout=)`
  budget: `__exit__` calls `shutdown(wait=True)` and blocks for the full call
  anyway. Use a module-level bounded pool that is never shut down from a request.
  Needed here because `OpenAIService.gpt_function` is wrapped in
  `retry_on_exception(max_attempts=5, backoff_factor=1.0)`, so a "one fast call"
  can really take a minute.
- `track_usage` stores its context in a contextvar, which a worker thread does NOT
  inherit from the request thread. Enter the `with track_usage(...)` block INSIDE
  the thread function or the usage row is mis-attributed.
- Writing a literal em dash or en dash through a tool call whose arguments are
  JSON: a six-character unicode escape for the dash, typed into the argument, is
  decoded by the JSON parser into the real character, so the file ends up
  containing the banned character even though the intent was a Python escape.
  Write such escapes from a script file (`chr(92) +
  "u2014"`), not from a heredoc or an inline tool argument, and verify with
  `grep -P "[\x{2013}\x{2014}]"` afterwards. A `<<'EOF'` heredoc through the Bash
  tool also ate the doubled backslashes on this box.
- `grep -c` exits 1 when the count is 0, so `grep -c ... && git commit ...`
  silently skips the commit. Use `;` between the check and the action.

## Reflect-specific constraints worth remembering

`reflect.py` treats message 0 as the system prompt everywhere: `messages_db[0]`,
`.offset(1)` twice, `messages[1:]` twice, and two empty-thread guards
(`len(messages) < 2`, `len(messages) <= 1`). Anything that wants to add an
"opening" turn must live in the system prompt, never as a Message row.
`SessionDataResponse` is shared with the journal voice agent
(`conversations.py`) and asserted on in `test_voice_fixes.py`, so voice-side
additions must be string appends to `system_message`, never schema changes.
`GET /workspace/overview` WRITES (marks the workspace visited), so never reuse it
as a read source for a new read-only endpoint.

Related: [[offline-verification]], [[project_upload_session_boot_crash]] for the
String-plus-constants-instead-of-native-enum convention this follows.
