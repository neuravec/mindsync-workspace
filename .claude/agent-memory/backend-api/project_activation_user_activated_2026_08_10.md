---
name: project_activation_user_activated_2026_08_10
description: users.activated_at column + atomic check-and-set emission of user_activated exactly once per user (analytics-reports/2026-08-10-activation-definition.md rec #5)
metadata:
  type: project
---

## What shipped (commit 2eea4d8, main, COMMITTED locally, NOT pushed)

- `MindSync/alembic/versions/gg8h9i0j1k2l_add_users_activated_at.py` — nullable
  `users.activated_at TIMESTAMPTZ`, no default, no backfill. Idempotent
  (inspector-guarded), down_revision = `ff7182a3b4c5` (verified single head via
  `alembic heads`, NOT via naive down_revision regex — see gotcha below).
- `app/models/models.py` — `User.activated_at` column added.
- `app/services/posthog_service.py` — `_atomic_mark_activated()` +
  `_maybe_emit_user_activated()`, wired into the ALREADY-EXISTING
  `capture_qualifying()` / `capture_with_user_qualifying()` (added by commit
  02bdce9 the same day, for the `$set_once` activation person-properties half
  of the same report). **No endpoint files were touched** — all 7 qualifying
  call sites (debriefs.py x2, prep_cards.py x2, between_sessions.py x2,
  reflect.py x1, health_check.py x2, symptoms.py x2, goals.py x1 = 12 call
  sites) already funnel through those two functions, so extending them was
  the "same call site" the report's spec asked for, with zero blast radius
  into files whose ownership is ambiguous (those endpoint files aren't
  explicitly listed under any agent in CLAUDE.md's ownership map — the task
  prompt authorized editing them, but the service-only design needed none of
  that authorization).
- Tests: `app/tests/test_users_activated_at_migration.py` (migration
  up/down/idempotent + postgres DDL compile, mirrors
  `test_workspace_fix4_migration.py`'s pattern) and 7 new tests appended to
  `app/tests/test_activation_instrumentation.py` (`TestUserActivatedCheckAndSet`).
- Fixed a self-caused regression in `test_workspace_fix4_migration.py` (stale
  "ff7182a3b4c5 is the chain tip" assertion) — see MEMORY.md lesson.

## Design decisions worth remembering

- **Atomic UPDATE...WHERE, not literal "same DB transaction"**: the task spec
  asked for the check-and-set to happen "in the same commit as the artifact
  write," but every `crud.*` write in this codebase commits per-operation
  (see `crud.create_session_debrief`), so by the time any of the 7 endpoints
  reach the posthog capture block, the artifact is already committed and
  there's no live transaction to piggyback on. The spec's own "prefer the
  atomic variant" concurrency note resolves this: `UPDATE ... WHERE
  activated_at IS NULL` is race-safe via DB row locking regardless of
  transaction boundaries, so a small separate commit for just the
  check-and-set achieves the same "exactly once" guarantee without needing
  transaction surgery across every qualifying endpoint's multi-commit
  choreography (AI processing, XP awarding, etc. each commit independently
  too).
- `surface` property (report asked for "screen/flow the capture came from")
  was set to the raw qualifying event name (e.g. `"debrief_created"`) rather
  than duplicating `activation_action` — more granular, no new mapping table
  needed.
- `hours_since_first_open` from the report's spec was omitted (report
  explicitly allows this) — the backend has no cheap access to the client's
  first-app-open timestamp, that only lives in PostHog person state.

## Gotcha: multi-head detection via down_revision regex is unreliable

A naive `down_revision = re.search(r'down_revision\s*=\s*"([^"]+)"')` scan of
`alembic/versions/*.py` found 3 "heads" (`aa1b2c3d4e5f`, `b1c2d3e4f5g6`,
`ff7182a3b4c5`) when only 1 is real. The other two are old branch tips that
were later merged back via a dedicated merge-revision file
(`5cafadce1513_merge_notification_logs_and_token_usage.py`) whose
`down_revision` is a **tuple** (`down_revision = ("aa1b2c3d4e5f",
"b1c2d3e4f5g6")`), which a simple quoted-string regex silently misses.
**Always confirm the head with the real `alembic heads` CLI command** (or
`python -m alembic heads`), not a source-grep heuristic, before setting a new
migration's `down_revision`. Note: [[offline-verification]] says the default
Windows `python` (3.14, `C:\Python314`) lacks an importable `alembic` and
recommends the Python 3.12 install instead — as of 2026-08-10 that's stale,
`python -m alembic heads` (default python) worked fine and correctly reported
the single head (`alembic` is now importable from
`AppData\Roaming\Python\Python314\site-packages`). Re-verify which install
has it before assuming either note is still accurate.
