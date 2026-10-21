# MSV3.2 Fix.1 — STATUS, PHASE A / slice A1 (backend-api) — DONE — 2026-07-17

Covers tasks **A1, A2, A3, A4, A5, A6, A12** per `10_PHASE_A_BACKEND.md`. A second
agent implemented A7–A11/A13 concurrently in the same repo this session (their commit
`c878e9f "MSV3.2Fix.1 A2: fix summaries raw-500, rewrite symptom narrative, expose
therapy-relationship/notification contract fields"` landed mid-session — see
"Coordination" below).

## Session commits (repo `MindSync/`, branch `main`, NOT pushed)

| Hash | One-liner |
|---|---|
| `4c5759d` | models/schemas/crud/migration for item lifecycle, Tematy i pytania, triage toggle, todo repeats |
| `b1f29f7` | endpoints for lifecycle, Tematy i pytania, triage toggle, pin sync, session-state |
| `3cd6682` | tests for lifecycle, triage toggle, pin sync, todo repeats, session-state |

(A 4th commit follows for this STATUS_A1.md + API_CONTRACT_Fix1_A1.md themselves.)

## Items completed (spec IDs)

- **A1** (item lifecycle + archives, CS-04): DONE for Agenda / Todo / Thread / Tematy i
  pytania (close, list-closed newest-first, restore, hard-delete all present for each).
  **Goals NOT done** — see "Not completed" below.
- **A2** (triage chip persistence, CS-03): DONE. New `GET .../chips` +
  `POST .../toggle` flow; added the missing `thread` proposal kind; chip state
  (unselected/selected/closed) derived live, survives card reopen forever; legacy
  batch-submit flow left untouched/working.
- **A3** (new module "Tematy i pytania", CS-05): DONE. New table, full CRUD, 7
  endpoints, `add-to-agenda` promotion.
- **A4** (agenda sourcing/tags/pin sync, CS-06/CS-14/CS-19/FIX.05): DONE. Source tags
  audited (already complete). Thread `add-to-agenda` rewritten create-only→toggle
  (fixes a duplicate-row bug). New realization `agenda-pin` toggle (fixes FIX.05
  unpin). Pin state is derived (no new column) so deleting the agenda item directly
  also clears the pin — no orphans.
- **A5** (thread statuses + context, CS-15): DONE, mostly an audit — status chain +
  context-regen hook were already correct from the MSV3.2 batch. Added: `view=closed`
  archive, and relaxed the reopen-at-capacity 409 to queue instead (CS-15 "not a cap").
  Active-count for "5 z N aktywnych" (CS-17) needs no new field — the existing
  `ThreadListResponse.count` on `view=active` already serves it.
- **A6** (todos repeats + completion log, FIX.01/CS-10): DONE. `repeat_freq` field +
  `TodoCompletion` log table + lazy self-healing rollover (no cron job — see
  "Deviations").
- **A12** (session schedule fields, CS-09 support): DONE. Schedule fields audited
  (already correct, no BE change needed). New `GET /therapy-tracking/session-state`
  computes the CS-09 Main state machine fresh every call. Root-caused the embedded
  "next session stopped displaying" bug (stale `next_session_date`) and worked around
  it in the new endpoint — see "Deviations" for why the OLD endpoint wasn't touched.
- **A13** (iOS voice upload BE audit) — audited, see "Notes for PHASE B" below.

## Items NOT completed / deviations + why

1. **Goals lifecycle (part of A1's task text) — NOT implemented.** `goals.py` (the only
   file that could host CS-21 "Zakończone cele" archive / lifecycle for goals) is owned
   by the concurrent Fix.1 agent for this session, per this slice's explicit
   file-ownership boundary (`app/api/v1/endpoints/prep_cards.py, debriefs.py,
   between_sessions.py, therapy_tracking.py` was the A12 list — `goals.py` was never in
   scope for me). Needs the lead to assign it to whichever agent owns `goals.py`, or a
   follow-up task.

2. **Mid-session file-ownership correction (worth flagging for the lead's process
   notes).** Early in A12 I initially added: a `User.topic_question_items`
   `back_populates` relationship to `app/models/models.py`, a self-heal fix +
   `has_prep_card_created_since` helper to `app/crud/crud.py`, and a
   `SessionCycleStateResponse` schema to `app/schemas/schemas.py`, and drafted the
   session-state endpoint in `users.py`. **All 4 are outside this slice's explicit
   hard file-ownership list** (`app/models/workspace.py`, `app/schemas/workspace.py`,
   `app/crud/workspace.py`, `app/api/v1/endpoints/workspace.py`, migrations, and for
   A12 specifically only `prep_cards.py`/`debriefs.py`/`between_sessions.py`/
   `therapy_tracking.py` — NOT `users.py`, NOT the general `models.py`/`crud.py`/
   `schemas.py`). `git status` confirmed the concurrent agent was actively editing
   `crud.py`/`models.py`/`schemas.py` at that same moment. **Reverted all 4 edits**
   before they could collide, and redesigned: the `User` relationship now uses
   SQLAlchemy `backref` (declared entirely on the `TopicQuestionItem` side, in
   `workspace.py` — no `models.py` edit needed), the session-state endpoint moved to
   `therapy_tracking.py` with a locally-defined Pydantic response model (no
   `schemas.py` edit needed), and it calls only pre-existing, unmodified `crud.py`
   functions (`get_therapy_schedule_with_frequency`, `has_debrief_for_session`,
   `get_latest_session_prep_card`) plus the pre-existing
   `app.utils.therapy_schedule_utils` helpers. Verified after the revert: `git diff
   --stat` on `models.py`/`crud.py` showed zero net change, and the concurrent agent's
   own (unrelated) `schemas.py` additions (A8/A11 symptom + health-check fields) were
   left untouched. **Consequence**: the OLD `GET /users/therapy-schedule` endpoint (in
   `users.py`, untouched) still returns the possibly-stale raw `next_session_date`
   column — only the NEW `session-state` endpoint self-heals this on read. A true
   root-cause fix at the `users.py`/`crud.py` layer needs coordination (see
   `API_CONTRACT_Fix1_A1.md` §10).

3. **Todo repeat rollover is a lazy, self-healing sweep on read, not a cron job.**
   `app/tasks/*` is owned by the concurrent agent for this session — no new background
   job was added. Every `GET /workspace/todos*` call runs
   `ws_crud.sweep_repeating_todos` first, which flips any DONE+repeating item back OPEN
   if its interval has elapsed. Functionally equivalent from the user's perspective
   (the item is open by the time they'd see it) but does mean a repeating item won't
   flip open in the background while the app is closed — only on next open. Flagging
   in case a "real" scheduled job is later wanted for push-notification purposes (e.g.
   "your daily task is back").

4. **`thread`-kind triage proposals need the AI layer to actually emit them.** This
   slice adds full BE plumbing (model kind, CRUD, select/merge-into-suggested-thread
   logic, contract) for a `kind="thread"` `TriageProposal`, but generating one is
   data-analytics' AI-extraction code (outside this slice's ownership, and outside
   `app/services/*` which is excluded per this session's boundary too). Until that's
   wired, the Wątki chip group on output cards will simply never have candidates —
   not a crash, just empty (CS-03: "if extraction returns nothing, hide the section").

5. **`realization_ref` chip-toggle semantics are an interpretation, not an explicit
   spec.** Fix.1.2's guardrails say "keep [the Odkrycie group] as an additional chip
   group" without specifying exact tap semantics beyond the superseded Fix.1.1 CS-07's
   generic "bookmark icon, tap = saved instantly, tap = selected state". Implemented
   as: tap ON → `in_repo=true` (visible in the Workspace Realizations repo); tap OFF →
   `in_repo=false` only (`show_on_timeline` untouched — nothing disappears from
   Timeline). Flagging for product confirmation before Phase F wires it.

6. **Todo completion history has no restore-a-specific-past-cycle capability.**
   `GET /workspace/todos/{id}/completions` is read-only. FIX.01 doesn't specify
   restoring a specific historical cycle (only "un-tap the CURRENT done item", already
   covered by the pre-existing `PUT .../undone`), and it isn't operationally
   well-defined for a repeating item (which cycle would "reopen"?) — scoped out
   deliberately.

## API contract deviations (reflected in `API_CONTRACT_Fix1_A1.md`)

- `PUT /workspace/threads/{id}/add-to-agenda` response shape changed:
  `AgendaItemResponse` → `PinToggleResponse` (`{"pinned": bool, "agenda_item_id": int}`).
  Breaking vs. the MSV3.2-batch shape, but Phase F (the only consumer) hasn't been
  built yet — nothing live breaks.
- `PATCH /workspace/threads/{id}/status {"status":"open"}` at the ~5-active threshold:
  was `409`, now `200` with `status: "queued"`.
- The legacy `GET /workspace/triage/{card_type}/{card_id}` + `POST
  /workspace/triage/submit` pair is superseded-but-kept (not removed) — Phase F should
  build against the new `GET .../chips` + `POST .../{id}/toggle` pair instead. See
  `API_CONTRACT_Fix1_A1.md` §2.

## New migrations

| id | chained from | applied on prod? |
|---|---|---|
| `aa2b3c4d5e6f` (`add_workspace_fix1_a1_tables`) | `zz6a7b8c9d0e` (verified single head at commit time) | **NO** — per master-plan rules, operator applies after PHASE G. |

Adds: `topic_question_items` table, `todo_completions` table,
`todo_items.repeat_freq`, `triage_proposals.linked_item_type`/`linked_item_id`. All
guarded (`has_table`/`get_columns` checks), idempotent, `String(n)`-only (no
`Enum(PyEnum)`). Verified offline: SQLite upgrade/downgrade round-trip + idempotency
(re-running `upgrade()` twice doesn't raise), postgresql-dialect `CreateTable` DDL
compiles clean for every new/changed table
(`app/tests/test_workspace_fix1_a1_migration.py`, 13 tests, all pass).

## Test results

- **Full suite**: `python -m pytest app/tests/ -q` → **21 failed, 4382 passed**
  (571.79s). Matches the documented baseline (21 BE failures, 2026-07-03) exactly —
  same count, and every failing test file/name (`test_custom_therapy_sessions.py`,
  `test_first_impression.py`, `test_health_check.py`,
  `test_notification_improvements.py`, `test_onboarding_v2.py`,
  `test_symptom_suggestions.py`, `test_therapy_frequency.py`, `test_voice_fixes.py`,
  `test_walkthrough.py`) is a file this slice never touched — `test_custom_frequency_
  neither_raises` specifically matches this agent's own memory notes as a known
  pre-existing baseline failure. **Zero new failures.**
- **This slice's own scope** (`test_workspace_crud.py` + `test_workspace_endpoints.py`
  + `test_workspace_models.py` + `test_workspace_fix1_a1*.py` +
  `test_therapy_tracking_fix1_a12.py` + `test_agenda_item_kind_migration.py`): **207
  passed, 0 failed** (116 pre-existing + 91 new/updated).
- Offline boot check (`app.api.v1.api` full router import, Windows substitute for
  `app.main` — see `test_workspace_fix1_a1_boot.py` for why): **passes**, including
  after the concurrent agent's `c878e9f` commit landed mid-session (re-ran after their
  commit to confirm no cross-agent interaction issue).

## Manual QA still needed (device/platform)

None for this slice specifically (pure backend, no device-dependent behavior) — normal
Phase G full-stack QA applies once Phases D/E/F wire the FE against this contract.

## Notes for next phases

- **Phase D/E/F**: read `API_CONTRACT_Fix1_A1.md` in full before wiring anything in
  §1–§4/§10's territory — it documents exact request/response shapes, including the 2
  breaking changes above and the "build against the NEW triage endpoints, not the
  legacy ones" guidance.
- **Phase B (iOS voice, A13 audit)**: reviewed `audio_v2.py` (`/transcribe`,
  `/realtime-session`, `/transcription-session`) and `session_recordings.py`'s chunked
  upload endpoints for anything that would reject iOS uploads. Found nothing
  iOS-specific at the endpoint layer — content-type validation accepts the standard
  iOS `audio/mp4`/`audio/x-m4a` variants already, size==0 is handled (413/422 paths
  exist), session-state checks are platform-agnostic. If CS-02's iOS bug reproduces
  after Phase B's FE fix, the cause is very likely FE-side (matches this agent's memory
  notes: "M4A always uploaded" was the fix for a related, already-shipped iOS issue) —
  not something visible from the BE endpoint contracts.
- **Lead**: please route Goals lifecycle (CS-21, part of A1's original task text) and
  the `users.py`/`crud.py`-layer root-cause fix for stale `next_session_date` (item 2
  above) to whichever agent/session owns those files next.
- **Coordination**: this session ran concurrently with another Fix.1 agent (A7–A11/13)
  in the same repo. One collision was caught and corrected before it landed (see
  "Deviations" item 2) — `git status`/`git diff --stat` before touching any file
  outside the explicit ownership list is what caught it. Recommend the master plan
  make crud.py/models.py/schemas.py exclusion as explicit as the endpoint-file list is,
  for any future split of a single feature area across two concurrent sessions.
