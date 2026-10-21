---
name: project-msv34-cs01-onboarding-goal-sync-2026-08-15
description: MSV3.4 CS-01 backend fix — onboarding goal now appends to Workspace Goals instead of no-opping on repeat; cap-lift blast-radius pattern
metadata:
  type: project
---

CS-01 (2026-08-15): `crud.sync_goals_from_onboarding` was idempotent per-USER
("if any active goal exists, no-op") which silently dropped the goal on a
second onboarding (post Reset Onboarding). Fixed to append, with a new
per-goal-TEXT dedup guard instead (if an ACTIVE goal with that exact decoded
text already exists, skip only that line) — this is what makes it safe
against a retried/duplicate completion PUT while still allowing genuinely
different text to always add a new card. `reset_therapy_onboarding` clears
`UserTherapyContext.goals_text` but never touches `UserGoal` rows, which is
what makes "goal survives a reset" work at all.

**Why:** operator decision to also lift the 5-active-goal cap for
onboarding-created goals only (`crud.create_goal(..., enforce_active_cap=False)`)
— the manual "+ Add goal" endpoint (goals.py) keeps enforcing the cap by
default (unaffected, not touched).

**Cap-lift blast radius pattern (reusable)**: any query that assumes a
domain cap (e.g. "max 5 active goals") for prompt-injection into an AI
context is de-facto unbounded once that cap is lifted anywhere in the
system, even if you didn't touch the query itself. Found one:
`_therapy_helpers.get_active_goal_dicts` (feeds `voice_director.py` +
`prep_cards.py` realtime AI context) had no `.limit()` — added `.limit(10)`
matching the existing precedent already used for the same table in
`get_workspace_grounding_context` in the same file. Two other candidate
call sites were checked and found NOT to need bounding: `gather_goal_context`
only reads `ctx.goals_text` (single string, not per-goal), and
`compute_goal_related_data` is called ONCE per request and reused across all
active goals in the response (not looped per-goal) — neither scales with
goal count.

**How to apply:** whenever lifting a hard cap anywhere in this codebase,
grep every consumer of the now-unbounded collection specifically for
prompt-injection / GPT-call sites, not just "does this endpoint still work" —
the correctness blast radius and the cost blast radius are different searches.

**Architecture note confirmed by this task**: the CRUD layer (`crud.py`) in
this codebase NEVER enqueues RQ jobs — all `rq_queue.enqueue(...)` calls live
in the endpoint layer. `sync_goals_from_onboarding` returns the list of newly
created `UserGoal` rows; the caller (`users.py`) does XP award + narrative/RAG
enqueue + PostHog capture, mirroring goals.py's own manual-create endpoint.
Don't have CRUD functions reach into `app.api.v1.endpoints.*` even via a
deferred import — `_therapy_helpers.py` imports `from app.crud import crud`
at module scope, so `crud.py` importing anything from `_therapy_helpers.py`
(even deferred) is a live circular-import risk.

**FE call-pattern finding (useful precedent)**: `saveJourneyAndAdvance` (goal
text screen) and `_markOnboardingComplete` (final "Wyloguj"... no, final
completion) are TWO SEPARATE PUT /therapy-context calls in the Flutter cubit
(`therapy_onboarding_cubit.dart`) — the final completion call sends ONLY
`{'onboarding_completed': true}`, never `goals_text`. So a trigger condition
gated on `data.onboarding_completed is True` would need to read
`ctx.goals_text` (persisted), not `data.goals_text` (this-request-only) — this
is the exact pattern already used by the starter-bio trigger a few lines
below in the same function. Chose NOT to move the trigger point for CS-01
(kept firing at `data.goals_text` truthy, i.e. the journey/step-4 save) to
avoid a scope-expanding regression (abandoned onboarding no longer creating
any goal at all) — this was a deliberate minimal-diff call, flagged in the
task report rather than silently decided.

Tests: `app/tests/test_goals.py` new classes `TestSyncGoalsFromOnboardingCrud`
(real in-memory SQLite session, not mocked `db.query` chains — this function
does 3 different query shapes) and `TestUpsertTherapyContextGoalSyncEndpoint`
(mocked `crud`, mirrors `test_onboarding_v2.py::TestUpsertEndpointConsent`
convention). See [[offline_verification]] for the SQLite-session test
fixture pattern (borrowed from `test_workspace_endpoints.py`).
