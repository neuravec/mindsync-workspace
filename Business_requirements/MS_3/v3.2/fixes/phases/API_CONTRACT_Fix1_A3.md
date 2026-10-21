# MSV3.2 Fix.1 — API contract, PHASE A / slice A3 (backend-api: Goals lifecycle)

> Closes the Goals gap explicitly left open by slice A1 (see `STATUS_A1.md`, "Items NOT
> completed" #1: *"Goals lifecycle (part of A1's task text) — NOT implemented ... Needs
> the lead to assign it to whichever agent owns `goals.py`"*). Covers Fix.1.2 §1 contract
> item **Goals** row (CS-04 item lifecycle applied to Goals) + **CS-21** (archive of
> completed goals). CS-20 (refresh) and CS-22 (add UI / create) were already implemented
> before this slice and are UNTOUCHED — noted below for completeness only.
>
> All endpoints below are mounted under `/api/v1/goals`. Auth: Firebase bearer token via
> `deps.get_current_user`. Cross-user access always 404s (never 403 — "never leak
> existence", matches every other Workspace/Goals endpoint). Encryption: `goal_text`,
> `ai_narrative`, `achieved_narrative` are encrypted at rest (`encode`/`decode`);
> response JSON below is always the **decrypted** plaintext.

---

## What already existed (audited, NOT changed by this slice)

| Capability | Endpoint | Notes |
|---|---|---|
| List goals grouped by status | `GET /goals/` | Returns `{active, achieved, revised, dropped}`. Unchanged shape except every `GoalResponse` item now carries the new `achieved_at` field (additive). |
| Mark ACHIEVED / REVISED / DROPPED / restore to ACTIVE | `PUT /goals/{id}/status` | Body `{"status": "...", "revised_text": "..."}`. This is the pre-existing CS-04 "close"/"restore" verb for Goals — **reused as-is**, only its CRUD implementation (`update_goal_status`) gained the `achieved_at` stamp/clear logic (see below). No request/response shape change. |
| Ad-hoc narrative refresh (CS-20) | `POST /goals/{id}/refresh` | Untouched. |
| Create goal (CS-22) | `POST /goals/` | Untouched — the "+ Dodaj cel" P1 sheet UI fix (CS-22) is FE-only; this endpoint already existed and needed no BE change. |
| Reorder / suggestions / share-data / narratives archive | `PUT /goals/reorder`, `GET /goals/suggestions`, `GET /goals/share-data`, `GET /goals/{id}/narratives` | Untouched. |

**Decision:** rather than add new "close" and "restore" endpoints per the generic P2/CS-04
pattern (as A1 did for Agenda/Todo/Thread/Tematy i pytania), Goals already had a working,
tested, general-purpose lifecycle endpoint (`PUT /{id}/status`) that the FE Goals module
already calls for ACHIEVED/REVISED/DROPPED/ACTIVE transitions. Reusing it for "close"
(→ ACHIEVED) and "restore" (→ ACTIVE) satisfies CS-04/CS-21 without a breaking or
duplicate contract change — the task brief's own guidance said "reuse before adding
columns", which extends naturally to "reuse before adding endpoints" here.

---

## What this slice added

### 1. `user_goals.achieved_at` (schema change)

New nullable `DateTime(timezone=True)` column — the completion date shown on each row of
the CS-21 "Zakończone cele" archive. **Invariant enforced in `crud.update_goal_status`:
`achieved_at` is non-null iff `status == ACHIEVED`.**

- `PUT /goals/{id}/status {"status": "ACHIEVED"}` → stamps `achieved_at = now()` (UTC),
  in addition to the pre-existing `achieved_narrative` snapshot.
- `PUT /goals/{id}/status {"status": "ACTIVE"}` (restore from any archived status) →
  **clears** `achieved_at` back to `null`. This is the documented design for "restore
  clears the completion date" per the task brief's point 2 — a restored goal is active
  again and has no close date until achieved a second time.
- `PUT /goals/{id}/status {"status": "REVISED"}` / `{"status": "DROPPED"}` — also clear
  `achieved_at` on the source goal if it was previously ACHIEVED (defensive: covers a
  direct ACHIEVED → REVISED/DROPPED edit without an intermediate restore, so the
  invariant above always holds and no goal can show a stale close date once it has left
  the archive).
- **Legacy rows**: any ACHIEVED goal that existed before this migration has
  `achieved_at IS NULL`. No data backfill migration was written (kept the migration
  purely additive/low-risk per Change Safety guidance); instead the read path falls back
  to `updated_at` for those rows (see `_goal_to_response` in `goals.py`) so the archive
  never shows a blank date. `GET /goals/` and `GET /goals/archive` both go through this
  same fallback.

### 2. `GET /goals/archive` (NEW) — CS-21 "Zakończone cele" / "Completed goals" archive

P2 pattern. Returns every ACHIEVED goal, **newest-first by completion date** (falls back
to `updated_at` for legacy rows per above).

Request: none (auth only).

Response `200` — `GoalArchiveResponse`:
```json
{
  "items": [
    {
      "id": 42,
      "goal_text": "Reduce anxiety in social situations",
      "ai_narrative": "…premium only, else null…",
      "status": "ACHIEVED",
      "display_order": 3,
      "parent_goal_id": null,
      "achieved_narrative": "…snapshot of the narrative at the moment it was achieved…",
      "premium_locked": false,
      "processing_status": "COMPLETED",
      "narrative_updated_at": "2026-06-01T12:00:00Z",
      "related_data": null,
      "achieved_at": "2026-07-10T09:15:00Z",
      "created_at": "2026-05-01T08:00:00Z",
      "updated_at": "2026-07-10T09:15:00Z"
    }
  ],
  "count": 1
}
```
- `items[]` are full `GoalResponse` objects (same shape as every other Goals endpoint —
  no truncated/archive-specific projection, matching the existing `GoalResponse` reuse
  pattern already used across this router).
- `related_data` is always `null` here (only active goals compute it, same as `GET /`).
- Empty archive → `{"items": [], "count": 0}` (never 404).
- **Restore** from the archive is `PUT /goals/{id}/status {"status": "ACTIVE"}` (existing
  endpoint, re-validates the max-5-active-goals rule — returns `400` if the user already
  has 5 active goals, same as every other restore-to-ACTIVE path).
- **Badge count** ("N closed since archive last opened"): **FE-computed**, per the A1
  precedent (`API_CONTRACT_Fix1_A1.md` §1) — no backend field. FE diffs this list's
  length/ids against a locally-stored "last opened" marker.

### 3. `DELETE /goals/{id}` (NEW) — hard delete (global "Usuń" guardrail)

Permanent delete, never archived — works from **any** status (active or already
archived/revised/dropped), matching the red "Usuń" semantics used everywhere else in
Workspace (`delete_agenda_item` / `delete_todo_item` / `delete_thread` /
`delete_topic_question_item` precedent).

Request: none (auth only, `goal_id` in path).

Response: `204 No Content` on success.

Errors:
- `404` — goal not found, or belongs to another user (never `403` — no existence leak).

Side effects: `goal_narratives` rows cascade-delete at the DB level
(`ondelete=CASCADE`, `passive_deletes=True` on the ORM relationship — unchanged, was
already configured for CS-19's narrative archive). Any goal that was REVISED from the
deleted one has its `parent_goal_id` set to `NULL` at the DB level (`ondelete=SET NULL`,
pre-existing FK, unchanged) — no dangling references, no orphan crash. RAG document
cleanup is **not** performed (matches the existing precedent for every sibling
`delete_*` function in `app/crud/workspace.py` — none of them clean up `rag_documents`
either; a stale RAG doc for a deleted goal is a known, pre-existing limitation across
the whole Workspace/Goals feature set, not something newly introduced here).

### 4. `GoalResponse.achieved_at` (additive field)

Every `GoalResponse` returned by **every** Goals endpoint (`GET /`, `GET /{id}`,
`GET /share-data`, `POST /`, `PUT /{id}`, `PUT /{id}/status`, `POST /{id}/refresh`, and
the new `GET /archive`) now includes:
```json
"achieved_at": "2026-07-10T09:15:00Z"   // or null
```
Non-null only when the goal's current status is `ACHIEVED` (either a real stamp, or the
`updated_at` fallback for legacy rows — see above). Purely additive; no existing field
removed, renamed, or retyped — safe for older FE builds that don't read it yet.

---

## Summary table (contract diff)

| Verb | Method + path | Status |
|---|---|---|
| Close (mark done) | `PUT /goals/{id}/status {"status":"ACHIEVED"}` | **Pre-existing endpoint, CRUD behavior extended** (stamps `achieved_at`) |
| List-closed (archive) | **`GET /goals/archive`** | **NEW** |
| Restore | `PUT /goals/{id}/status {"status":"ACTIVE"}` | **Pre-existing endpoint, CRUD behavior extended** (clears `achieved_at`); pre-existing max-5-active validation unchanged |
| Hard-delete | **`DELETE /goals/{id}`** | **NEW** — 204, permanent, never archived |
| (unrelated) refresh narrative | `POST /goals/{id}/refresh` | Untouched (CS-20) |
| (unrelated) create | `POST /goals/` | Untouched (CS-22 UI-only fix) |

## For flutter-mobile (when Goals FE work is scheduled — PHASE E per master plan)

- Do **not** build separate "close" / "restore" calls — wire the existing status-update
  call with `"ACHIEVED"` / `"ACTIVE"`.
- The CS-21 hub-and-spoke archive view should call `GET /goals/archive` and render
  `items[].achieved_at` as the close date; `count` is available but the P2 badge itself
  must be FE-computed (no backend "unseen count" field, consistent with every other
  Workspace archive).
- Red "Usuń" in the goal's 3-dot menu → confirm dialog → `DELETE /goals/{id}` → 204 →
  remove from whichever list it was in (active list or the archive view).
- `GoalResponse.achieved_at` is now present everywhere; safe to ignore until the archive
  UI is built.
