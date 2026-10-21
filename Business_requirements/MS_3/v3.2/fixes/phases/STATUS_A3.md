# MSV3.2 Fix.1 — STATUS, PHASE A / slice A3 (backend-api: Goals lifecycle) — DONE — 2026-07-17

Closes the gap explicitly flagged in `STATUS_A1.md` ("Items NOT completed" #1): Goals was
excluded from A1's item-lifecycle-and-archives work because `goals.py` was outside that
session's file-ownership boundary. This slice closes it, working solo in the backend repo
(A1: commits `4c5759d`..`3b0a93b`, migration `aa2b3c4d5e6f`; A2: `c878e9f` — both already
landed and confirmed present before this session started).

## Session commits (repo `MindSync/`, branch `main`, NOT pushed)

| Hash | One-liner |
|---|---|
| _filled in below after commit_ | MSV3.2Fix.1 A3: Goals lifecycle — achieved_at, completed-goals archive, hard delete |

## Items completed (spec IDs)

- **CS-04** (item lifecycle, applied to Goals): DONE. Goals already had a working
  "close"/"restore" verb (`PUT /{id}/status` with ACHIEVED/ACTIVE) — reused rather than
  duplicated with new endpoints (see "Design decision" below and `API_CONTRACT_Fix1_A3.md`).
- **CS-21** (archive of completed goals): DONE.
  - New `user_goals.achieved_at` column (migration `bb3c4d5e6f70`), stamped on ACHIEVED,
    cleared on any transition away from ACHIEVED.
  - New `GET /goals/archive` endpoint — completed goals, newest-first by completion date,
    each with its close date.
  - Restore = existing `PUT /{id}/status {"status":"ACTIVE"}` (already re-validates the
    max-5-active-goals rule; now also clears `achieved_at`).
  - Badge count: FE-computed, per the A1 precedent — no backend field added.
- **Hard delete** (global "Usuń" guardrail, was entirely missing for Goals): DONE. New
  `DELETE /goals/{id}` — 204, permanent, works from any status, 404 on
  not-found/cross-user (never leaks existence).
- **CS-20** (ad-hoc narrative refresh) and **CS-22** (add UI / doubled "+" fix): audited,
  confirmed already fully implemented (`POST /{id}/refresh`, `POST /`) — **untouched**,
  per the task's explicit "keep everything else about goals UNTOUCHED" instruction.

## Design decisions / deviations from a literal P2 reading

1. **No new "close" endpoint.** The generic P2 pattern (used by A1 for
   Agenda/Todo/Thread/Tematy i pytania) is "checkbox → close → archive". Goals already
   has a general-purpose lifecycle endpoint (`PUT /{id}/status`) driving
   ACHIEVED/REVISED/DROPPED/ACTIVE, already wired to XP awards and narrative
   regeneration hooks, and (per the task brief) explicitly not to be duplicated —
   "reuse before adding columns" was read as extending to "reuse before adding
   endpoints". Marking a goal done is `PUT /{id}/status {"status":"ACHIEVED"}`; this
   slice only extended what that status transition *does* (stamps `achieved_at`).
2. **Restore clears the completion date** (task point 2's open design question,
   resolved): a goal restored to ACTIVE has `achieved_at` set back to `null`. Rationale:
   the archive's contract is "shows completion date for goals currently in the archive"
   — once restored, the goal is no longer in the archive, so a stale date would be
   misleading if the goal is achieved a second time later (the new stamp should reflect
   the *current* achievement, not a historical one). A direct ACHIEVED → REVISED/DROPPED
   edit (skipping an intermediate restore-to-ACTIVE step) also clears it, for the same
   reason — enforced as an invariant (`achieved_at` non-null iff `status == ACHIEVED`)
   rather than only handling the ACTIVE-restore case, since the status-update endpoint
   allows any of the 4 target statuses regardless of current status.
3. **No data backfill migration for legacy ACHIEVED rows.** `achieved_at` is nullable and
   purely additive (safest option per Change Safety — this migration does not assume any
   prior MSV3.2 Workspace migration ran, matching the `aa2b3c4d5e6f` precedent it chains
   onto). Instead, the API read path (`_goal_to_response`) falls back to `updated_at`
   for any ACHIEVED goal with `achieved_at IS NULL`, so the archive never shows a blank
   date for goals achieved before this column existed. `crud.get_achieved_goals`'
   ordering also uses `COALESCE(achieved_at, updated_at)` so legacy rows sort sensibly
   alongside newly-stamped ones.
4. **RAG documents are not cleaned up on hard delete.** Audited: none of the sibling
   `delete_*` functions in `app/crud/workspace.py` (agenda/todo/thread/topic-question)
   clean up `rag_documents` either — this is a pre-existing, consistent limitation
   across the whole Workspace/Goals feature, not something newly introduced by this
   slice. Flagging for a future cleanup task if the lead wants it addressed uniformly.
5. **Collateral test fixes (2 files outside this slice's literal FILES list, both
   necessary to avoid a false regression from this change — not scope creep):**
   - `app/tests/test_goals.py` — `_make_goal_mock()` now accepts/sets `achieved_at`
     (default `None`), and `TestGoalResponseSchema.test_response_expected_fields`'
     exact-field-set assertion now includes `"achieved_at"`. Without this, ~30
     pre-existing tests using `MagicMock(spec=UserGoal)` would have started returning a
     `MagicMock` (not `None`) for the new attribute, breaking Pydantic validation in
     `_goal_to_response` — a foreseeable, mechanical consequence of adding a model
     column, matching the established pattern noted in this agent's memory
     ("Tests use MagicMock with spec= for model instances — must explicitly set ALL
     model fields when new columns are added").
   - `app/tests/test_workspace_fix1_a1_migration.py` —
     `TestMigrationFileMetadata::test_is_the_single_head` asserted `aa2b3c4d5e6f` has
     zero children (i.e. is the current head). Chaining `bb3c4d5e6f70` on top of it
     (as the task explicitly instructs — "chained from the CURRENT single head")
     necessarily and correctly breaks that specific assertion. Renamed to
     `test_has_only_the_known_successor` and updated to assert the one sanctioned child
     — preserves the test's real intent (catch an *accidental* second branch), stops
     asserting a fact that any legitimate future migration would also break.

## Schema change

`user_goals.achieved_at` — nullable `TIMESTAMP WITH TIME ZONE`. Migration
`bb3c4d5e6f70_add_user_goals_achieved_at.py`, chained from `aa2b3c4d5e6f` (verified: the
only file in `alembic/versions/` with no successor before this slice — confirmed by
grep across the tree, and by the new `test_is_the_head`-equivalent migration test).
Idempotent (`inspector.get_columns()` guard, mirrors the `aa2b3c4d5e6f` precedent
exactly); downgrade drops the column, also guarded. No native Postgres enum introduced —
plain `DateTime(timezone=True)`. `python -c "import app.api.v1.api"` (the documented
Windows-safe boot-check, per this agent's memory — `app.main` itself hits a Windows-only
Firebase-cert `OSError` unrelated to this change) passes cleanly.

**Deploy-order note (same class of risk as every prior slice touching a live table):**
`user_goals` is an existing, already-deployed, actively-written table (Goals is a live
feature, unlike some of the brand-new MSV3.2 Workspace tables which have never been
migrated on prod yet). If backend code from this slice deploys before
`heroku run alembic upgrade head` runs, every query against `UserGoal` (i.e. the entire
Goals feature) will start raising `UndefinedColumn` until the migration catches up —
this is the same "deploy ≠ migrate" risk CLAUDE.md already governs, called out
explicitly here because, unlike this batch's brand-new Workspace tables, Goals is
user-facing today. **Sequence this migration with the deploy, don't let it lag.**

## Tests

New file `app/tests/test_fix1_goals_lifecycle.py` — 36 tests, all passing. Covers: the
model column (existence, nullability, non-enum type); the migration (file metadata,
single-head-successor check, SQLite upgrade/downgrade round-trip + idempotency, Postgres
DDL compile, app-import boot-safety); `crud.update_goal_status`'s `achieved_at`
invariant across all 4 transitions (including the direct ACHIEVED→REVISED/DROPPED edge
case); `crud.get_achieved_goals` ordering + legacy-row fallback + user-scoping (real
in-memory SQLite session, not mocked, for genuine query-behavior coverage);
`crud.delete_goal` (both a mock-call-shape test and a real-session
create→delete→confirm-gone test); the two new/changed schemas; both new endpoints
(happy path, empty archive, 404 not-found, 404 cross-user rather than 403, delete works
from an already-archived status); and `_goal_to_response`'s legacy-row fallback logic in
isolation.

**Baseline (per `00_MASTER_PLAN.md` / `70_PHASE_G_FINAL_QA.md`): 21 pre-existing BE
failures.**

- **After this slice, full `python -m pytest app/tests/ -q`: `21 failed, 4422 passed,
  178 warnings in 837.55s (0:13:57)`.** Exact match to the documented baseline count —
  **zero new failures, zero regressions.** The 21 failures are the same known
  pre-existing set (`test_custom_therapy_sessions.py`, `test_first_impression.py`,
  `test_health_check.py`, `test_notification_improvements.py`, `test_onboarding_v2.py`,
  `test_symptom_suggestions.py`, `test_therapy_frequency.py`, `test_voice_fixes.py`,
  `test_walkthrough.py`) — none touch Goals, Workspace, or migrations; confirmed
  unrelated to this slice by inspection of the failing test names/files.
- Targeted runs (all green) before the full-suite confirmation: `test_goals.py` (128
  passed, 0 failed — no regression from the `_make_goal_mock`/expected-fields fix),
  `test_fix1_goals_lifecycle.py` (36 passed — new), `test_workspace_fix1_a1.py` +
  `test_workspace_fix1_a1_boot.py` + `test_workspace_fix1_a1_migration.py` +
  `test_fix1_goals_notifications_therapy_relationship.py` + `test_goal_narrative_weekly.py`
  + `test_goal_narratives.py` (98 passed after the single-head test fix — that fix
  addressed 1 expected, self-inflicted-by-design failure from extending the migration
  chain, not a new regression; it's included as a pass in the full-suite number above).

## Change Safety recon (CLAUDE.md mandate)

1. **Who consumes this?** Grepped for every caller/importer:
   - `app.api.v1.endpoints.goals` — the only endpoint file referencing `UserGoal` /
     `GoalResponse` / `crud.update_goal_status` / `crud.get_goal` in this codebase.
   - `app.api.v1.endpoints.clinician_v2` imports a *different* `GoalResponse` (from
     `app.schemas.clinician_v2`, wrapping a distinct `TreatmentGoal` model) — confirmed
     by reading its import block; zero overlap, false-positive ruled out.
   - `app.tasks.goal_narrative` (data-analytics-owned) writes `ai_narrative` /
     `data_hash` / `processing_status` on `UserGoal` — none of those columns were
     touched; not affected.
   - `app.tasks.rag_indexing.index_goal_to_rag` reads goal fields for embedding — not
     touched; existing behavior unaffected (goal hard-delete leaving a stale RAG doc is
     pre-existing across the whole Workspace feature, see deviation #4 above).
   - Flutter: goals.py's request/response contract is additive-only (`achieved_at` is a
     new optional field with `None` default; 2 new endpoints) — no existing FE call site
     can break. Full FE wiring is out of scope for this slice (Goals FE work is PHASE E,
     not yet run) — `API_CONTRACT_Fix1_A3.md` has a note for that agent when it starts.
2. **What runs at boot?** `app.main` imports the full router tree including `goals.py`
   and runs `Base.metadata.create_all` — `test_app_imports_cleanly` (via
   `app.api.v1.api`, the Windows-safe substitute) confirms the router tree still imports
   cleanly with the new column/endpoints present. `Base.metadata.create_all` is
   additive/idempotent for a new nullable column on an existing table — no boot risk
   from the model change itself (the risk is entirely the deploy-before-migrate query
   failure noted above, which is a runtime query concern, not a boot-import concern).
3. **Model ↔ migration ↔ prod DB.** `user_goals.status` already uses a native Postgres
   enum (`GoalStatusEnum`) predating this slice — audited, confirmed untouched, no new
   drift introduced. The new `achieved_at` column is a plain `DateTime(timezone=True)`,
   no enum involved.
4. **SQLite vs Postgres.** `TestPostgresDDLCompiles::test_user_goals_ddl_compiles_with_achieved_at`
   compiles `UserGoal.__table__` against the `postgresql` dialect offline and asserts
   `achieved_at` appears with no enum-drift tokens nearby.
5. **Deploy ≠ migrate.** Called out explicitly above — this is the one schema change in
   the Fix.1 batch so far that touches an already-live, already-migrated table rather
   than a not-yet-deployed Workspace table.
6. **Cross-layer contract.** Additive-only; documented in `API_CONTRACT_Fix1_A3.md` for
   integration-devops / flutter-mobile to pick up when Goals FE work starts.
7. **Verified offline before prod.** All of the above ran locally; no live API/DB touched.

## Files touched (all within this slice's authorized FILES list, plus the 2 collateral
test fixes explained above)

- `app/models/models.py` — `UserGoal.achieved_at` only.
- `alembic/versions/bb3c4d5e6f70_add_user_goals_achieved_at.py` — new.
- `app/crud/crud.py` — `update_goal_status` (achieved_at set/clear), new
  `get_achieved_goals`, new `delete_goal`. No other goal function touched.
- `app/schemas/schemas.py` — `GoalResponse.achieved_at`, new `GoalArchiveResponse`. No
  other schema touched.
- `app/api/v1/endpoints/goals.py` — `_goal_to_response` (achieved_at + fallback), new
  `GET /archive`, new `DELETE /{goal_id}`. No other endpoint's logic changed.
- `app/tests/test_fix1_goals_lifecycle.py` — new, 36 tests.
- `app/tests/test_goals.py` — collateral fix (2 spots, see deviation #5).
- `app/tests/test_workspace_fix1_a1_migration.py` — collateral fix (1 spot, see
  deviation #5).

**Not touched:** `workspace.py` (endpoint, model, schema, or crud), `summaries.py`,
symptoms code, notification code, `app/tasks/*`, `app/main.py` — confirmed via
`git diff --stat` before commit.

## Coordination notes

- No `integration-devops` handoff blocking this slice — additive-only contract change,
  documented in `API_CONTRACT_Fix1_A3.md` for whenever Goals FE work (PHASE E) starts.
- No schema request from `data-analytics` was involved; this migration was
  self-originated to close A1's flagged gap.
- Per master-plan git rules: committed locally, branch `main`, NOT pushed, no migration
  run against prod. Staged only the files listed above (never `git add -A`).
