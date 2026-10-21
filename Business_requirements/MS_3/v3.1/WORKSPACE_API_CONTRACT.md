# Workspace — Backend API Contract (MSV3.2 batch)

Status: **IMPLEMENTED (backend only).** Models, migration, CRUD, schemas, endpoints, XP hooks, and tests are committed on `main`. Not deployed/migrated to prod. Flutter UI and the AI-generation pipelines (triage proposals, weekly observations, mood-trend summary) are NOT part of this contract's implementation — this document is their integration spec.

Author: backend-api · Date: 2026-07-06 · Spec refs: `spec.txt` CS-07, CS-10, CS-11, CS-12, CS-13, Global guardrails · `workspace_brief.txt` (all 6 modules, triage rules, AI functions, XP rules, edge cases).

All endpoints are under `/api/v1/workspace/*` unless noted. Auth: Firebase bearer token via `deps.get_current_user` (same as every other endpoint). DB session: `deps.get_db`. Every list/detail endpoint scopes strictly by `user_id` — cross-user access returns 404, never 403 (avoids leaking existence), verified by dedicated tests.

---

## 0. Lead decisions baked into this implementation

These override the raw spec/brief text where they conflicted, per the task's binding instructions:

1. **Homework-for-Main** = the 3 oldest OPEN to-do items, FIFO, **any origin** (homework or AI action point). Spec CS-10 wins over the brief's "max 2 due today, homework-repo-implied" reading. Endpoint: `GET /workspace/todos/today`.
2. **Triage never pre-selects.** `TriageProposal` rows are created with no "pre-selected" concept at all — there is no such column. The brief's "1–3 pre-selected" line is superseded.
3. **Triage never deletes.** Unselected `TriageProposal` rows simply stay `status="pending"` forever (or until acted on later) — nothing about them changes when other proposals on the same card are submitted. `GET /workspace/triage/{card_type}/{card_id}` always reflects exactly what's still available.
4. **Realizations toggle pair** is exactly two independent booleans (`show_on_timeline`, `in_repo`) — there is no third "valuable" flag anywhere in the schema.
5. **Every Workspace item has exactly two exits**: an active-track completion action (`touch` / `done` / `close` — verb per module) or `archive` (odklik, semi-archive, restorable, never destructive, never changes XP).

---

## 1. Data model summary

New tables (migration `xx4y5z6a7b8c_add_workspace_tables.py`, revises `ww3x4y5z0a1b`, additive-only, idempotent — see §7):

| Table | Purpose | Key columns |
|---|---|---|
| `agenda_items` | Module 1 — next-session agenda | `text`(enc), `source_type`, `source_id`, `thread_id`, `kind`, `status`, `xp_awarded` |
| `todo_items` | Module 2 — homework + AI action points, one list | `text`(enc), `origin`, `source_type`, `source_id`, `status`, `xp_awarded` |
| `threads` | Module 3 — open therapy topics | `title`(enc), `context_description`(enc), `status`, `xp_awarded` |
| `thread_sources` | Link table: thread ↔ Timeline card it came from | `thread_id`, `source_type`, `source_id` |
| `goal_narratives` | Module 5 archive — one row per successful AI narrative regeneration | `goal_id` (FK `user_goals`), `narrative`(enc) |
| `weekly_observations` | Main CS-13 — fresh table, NOT Realizations | `content`(enc), `context_description`(enc), `trigger_type` |
| `mood_trend_summaries` | Main CS-11 cache | `bullets`(enc, JSON array ≤5 strings) |
| `triage_proposals` | AI-extracted candidates per output card | `card_type`, `card_id`, `kind`, `text`(enc), `suggested_thread_id`, `realization_id`, `status` |

Additive columns on existing tables:

| Table.column | Type | Default | Purpose |
|---|---|---|---|
| `realizations.show_on_timeline` | bool, nullable | `TRUE` | Triage toggle (a) |
| `realizations.in_repo` | bool, nullable | `TRUE` | Triage toggle (b) |
| `user_preferences.workspace_last_visited_at` | timestamptz, nullable | `NULL` | Powers "new since last visit" on overview |

Default `TRUE` on the two Realization columns is deliberate: every pre-existing realization, and every realization created by any OTHER path (AI auto-detection, the existing manual `POST /realizations/`), keeps behaving exactly as before — still shown on the Timeline, still in the Workspace repo — unless a user explicitly opts one out via the toggle endpoint.

**Schema safety**: no column in any new table is a native SQLAlchemy/Postgres `Enum`. Every status/kind/origin/source_type is `String(n)` + a paired `(str, enum.Enum)` Python class used only as an app-level constant (`app/models/workspace.py`) — the `UploadSession` pattern from CLAUDE.md. Verified offline: DDL compiled against the `postgresql` dialect contains no enum-drift tokens (`app/tests/test_workspace_models.py::TestPostgresDDLCompiles`).

### Status/kind vocabularies

```
AgendaItemStatus   = open | touched | archived
TodoOrigin         = therapist | ai
TodoStatus         = open | done | archived
ThreadStatus       = open | touched | closed | archived | queued
TriageCardType     = debrief | prep_card | recording | between_session
TriageProposalKind = topic | question | action_point | realization_ref
TriageProposalStatus = pending | consumed
WeeklyObservationTrigger = post_session | monday

# Shared source_type vocabulary for agenda_items / todo_items / thread_sources
# (distinct from the pre-existing Realization.source_type set, which lacks
# prep_card/manual/thread and is unchanged). "realization" added 2026-07-06
# (see Changelog §11) — client-settable only via POST /workspace/agenda; the
# other five values are set exclusively by their own internal flows.
AgendaSourceType = debrief | prep_card | recording | between_session | manual | thread | realization

# Client-settable subset of AgendaSourceType on POST /workspace/agenda (added
# 2026-07-06, see Changelog §11):
AGENDA_CREATE_SOURCE_TYPES = manual | realization

# Visual tag on an agenda item (added 2026-07-06, see Changelog §11).
# NULL (the default for every pre-existing row) is treated as "topic" client-side.
AgendaItemKind = topic | question | NULL
```

`MAX_ACTIVE_THREADS = 5`. "Active" (capacity-counted) = `open | touched | queued`. A 6th+ thread is created with `status="queued"` instead of being rejected — closing or archiving any active thread auto-promotes the oldest `queued` thread to `open`.

---

## 2. Endpoints

### 2.1 Overview

**`GET /workspace/overview`**

One call for the Workspace landing screen. Each module trimmed to its 3 most-recent items + a count + a `has_new_since_last_visit` boolean (computed from `user_preferences.workspace_last_visited_at`, BEFORE it's updated). Calling this endpoint marks the visit (best-effort, non-fatal — a failure to persist the timestamp never breaks the response).

Response:
```json
{
  "agenda": {"count": 4, "has_new_since_last_visit": true, "preview": [ {AgendaItemResponse}, ... ]},
  "todos": {"count": 6, "has_new_since_last_visit": false, "preview": [ {TodoItemResponse}, ... ]},
  "threads": {"count": 2, "has_new_since_last_visit": false, "preview": [ {ThreadResponse}, ... ]},
  "realizations": {"count": 3, "has_new_since_last_visit": true, "preview": [ {RealizationRepoItem}, ... ]},
  "goals": {"count": 1, "has_new_since_last_visit": false, "preview": []},
  "therapy_relationship": {"count": 1, "has_new_since_last_visit": false, "preview": []}
}
```
`goals` and `therapy_relationship` previews are intentionally empty arrays (count-only) — those features already have full detail endpoints (`GET /goals/`, `GET /health-check/latest` etc.); duplicating their payload shape here would create a second source of truth. flutter-mobile: use the count/new-flag from here for the Workspace landing tiles, and call the existing endpoints for full detail when the user taps in.

### 2.2 Module 1 — Agenda

| Method | Path | Notes |
|---|---|---|
| POST | `/workspace/agenda` | Body `{"text": "..."}` → creates with `source_type="manual"`, `status="open"`. 201. **Additive as of 2026-07-06 (see Changelog §11)**: optional `kind` ("topic"\|"question"), and an alternate pin-a-Realization mode — see below. |
| GET | `/workspace/agenda?view=active\|touched\|archived` | Default `active` = **OPEN only** as of 2026-07-06 (see Changelog §11) — `touched` is its own explicit view. `GET /workspace/overview`'s `agenda` module shares this same view table. 400 on unknown `view`. |
| PUT | `/workspace/agenda/{id}/touch` | → `status="touched"`, awards XP (orca, `agenda_touched`). Cascades: if the item is linked to a thread (`thread_id` set) and that thread is currently `open`, the thread's status also becomes `touched` (brief: "jeśli była podpięta pod wątek, wątek dostaje status poruszony"). A `closed`/`archived` thread is never resurrected by this. |
| PUT | `/workspace/agenda/{id}/archive` | Odklik. `status="archived"`. **No XP change.** |
| PUT | `/workspace/agenda/{id}/restore` | `status="open"`. **No XP change.** |

`AgendaItemResponse` (additive `kind` field as of 2026-07-06 — see Changelog §11):
```json
{"id": 12, "text": "Talk about mom", "source_type": "debrief", "source_id": 88,
 "thread_id": null, "kind": "topic", "status": "open", "created_at": "...", "touched_at": null, "archived_at": null}
```

**`POST /workspace/agenda` — pin an existing Realization (2026-07-06, Changelog §11):**
Body `{"source_type": "realization", "source_id": <realization_id>}` (`text` omitted/ignored — the pinned item's text always mirrors the Realization's own text server-side). `source_id`'s Realization must exist and belong to the caller — 404 otherwise (never 403, per this router's existing "never leak existence" convention). **Idempotent**: if a non-archived agenda item is already pinned to that Realization, it's returned as-is with **200** instead of creating a duplicate (a genuinely new pin still returns 201). An archived (odklik'd) prior pin does not block a fresh one. `source_type` is otherwise restricted to `"manual"` (default) — any other `AgendaSourceType` value (`debrief`/`prep_card`/`recording`/`between_session`/`thread`) is 422 if a client attempts to pass it; those remain set only by their own internal flows.

### 2.3 Module 2 — To-do (homework + AI action points)

| Method | Path | Notes |
|---|---|---|
| POST | `/workspace/todos` | Body `{"text": "..."}` → always `origin="therapist"` (homework). Action points are NEVER created via this endpoint — only via triage. 201. |
| GET | `/workspace/todos?view=active\|done\|archived` | Default `active`. Ordering: homework (`origin=therapist`) pinned before AI action points; oldest-first within each group. |
| GET | `/workspace/todos/today?limit=3` | **Homework-for-Main.** 3 oldest OPEN items, FIFO, any origin (§0.1). `limit` is overridable (1-10) but FE should always pass 3 per spec. |
| PUT | `/workspace/todos/{id}/done` | → `status="done"`, awards XP (orca, `todo_done`). Idempotent — a second call is a no-op for points (flag-guarded) but the endpoint itself doesn't forbid re-calling. |
| PUT | `/workspace/todos/{id}/undone` | Reverts to `open`. Does **not** claw back XP already granted (see §5 note). |
| PUT | `/workspace/todos/{id}/archive` | Odklik. **No XP change.** |
| PUT | `/workspace/todos/{id}/restore` | **No XP change.** |

`TodoItemResponse`:
```json
{"id": 5, "text": "Practice breathing 2x/day", "origin": "therapist", "source_type": null,
 "source_id": null, "status": "open", "created_at": "...", "done_at": null, "archived_at": null}
```

### 2.4 Module 3 — Threads

| Method | Path | Notes |
|---|---|---|
| POST | `/workspace/threads` | Body `{"title": "...", "context_description": "...?"}`. Queues (`status="queued"`) instead of rejecting once 5 are already active. 201. |
| GET | `/workspace/threads?view=active\|archived` | Default `active` (open+touched+queued), open/touched before queued, oldest-first within each. |
| GET | `/workspace/threads/{id}` | Full detail: `context_description` (decrypted) + `sources[]`. |
| PUT | `/workspace/threads/{id}/add-to-agenda` | One-tap. Creates an `AgendaItem` (`source_type="thread"`, `thread_id=<this>`, text = thread title). Returns the created `AgendaItemResponse`. |
| PUT | `/workspace/threads/{id}/close` | Zakończ/domknij. → `status="closed"`, awards XP (**user track**, `thread_closed`). Auto-promotes the oldest `queued` thread to `open`. |
| PUT | `/workspace/threads/{id}/archive` | Odklik. `status="archived"`. **No XP change.** Also auto-promotes the oldest queued thread (frees the slot either way). |
| PUT | `/workspace/threads/{id}/restore` | `status="open"` — or re-queues (`status="queued"`) if the 5-active cap is full again at restore time. **No XP change.** |
| PATCH | `/workspace/threads/{id}/status` | **Added 2026-07-06 (Changelog §11).** Body `{"status": "open"\|"touched"\|"closed"}` — the status-chip tap-cycle. `target="closed"` reuses the exact same close logic as `PUT .../close` (same XP + queue-promotion — not forked). Reopening a `closed` thread (`closed`→`open` or `closed`→`touched`) re-checks the ~5-active cap: **409** if already full (thread stays `closed`, nothing silently re-queued). A thread currently `archived` or `queued` cannot be targeted by this endpoint (**409** — use `/restore` for archived; queued threads only auto-promote via close/archive elsewhere). Same-status is a no-op (200). |

`ThreadResponse` (list) / `ThreadDetailResponse` (detail, adds `context_description` + `sources`):
```json
{"id": 3, "title": "Contact with mom", "status": "open", "created_at": "...",
 "updated_at": "...", "closed_at": null, "archived_at": null, "queued": false,
 "context_snippet": "First ~140 chars of the decrypted context_description..."}
```
`context_snippet` is additive as of 2026-07-06 (see Changelog §11) — `null` when there's no `context_description` yet, otherwise the first ~140 decrypted chars with a trailing `"..."` when truncated. Present on both `ThreadResponse` and `ThreadDetailResponse` (the latter also still returns the full, untruncated `context_description`).
`sources[]` items: `{"id": 1, "source_type": "debrief", "source_id": 88, "created_at": "..."}`.

### 2.5 Module 4 — Realizations repo

The existing `Realization` feature/table/endpoints (`/realizations/*`, owned by backend-api, unchanged) is extended, not replaced.

| Method | Path | Notes |
|---|---|---|
| GET | `/workspace/realizations?limit=20&offset=0` | Repo listing — same exclusions as the existing Timeline query (not soft-deleted, not dismissed) **plus `in_repo == True`**. |
| PUT | `/workspace/realizations/{id}/toggles` | Body `{"show_on_timeline": bool, "in_repo": bool}` — **both required together**, no partial update. **No XP change** (never award XP for a clinical/content decision). |

`RealizationRepoItem` (distinct from the pre-existing `RealizationResponse` in `app/schemas/schemas.py`, which is untouched for backward compatibility):
```json
{"id": 40, "realization_text": "...", "source_type": "debrief", "source_id": 88,
 "created_at": "...", "show_on_timeline": true, "in_repo": true}
```

**Important for flutter-mobile / whoever owns the Timeline rendering query**: this backend change does NOT alter what the existing Timeline realization query returns — `show_on_timeline` is stored but nothing server-side currently filters on it for Timeline display (see §6 gap #1).

### 2.6 Module 5 — Goals (extends `app/api/v1/endpoints/goals.py`)

One new endpoint added; all existing goal endpoints are unchanged (see §8 for the FE-only renames that need NO backend change).

**`GET /goals/{goal_id}/narratives`** → `GoalNarrativeArchiveResponse`:
```json
{"goal_id": 7, "count": 2, "items": [
  {"id": 15, "narrative": "This week you leaned into...", "created_at": "2026-07-05T09:00:00Z"},
  {"id": 9,  "narrative": "You're circling back to...",   "created_at": "2026-06-28T09:00:00Z"}
]}
```
Newest first. 404 if the goal doesn't exist or isn't the caller's.

**Population**: fully automatic, zero changes needed to `app/tasks/goal_narrative.py`. `crud.update_goal_narrative()` (called by that task on every successful regeneration, and only then — a `FAILED`-status update with no new `ai_narrative` archives nothing) now inserts a `GoalNarrative` row whenever the update includes a new `ai_narrative`. This fires for: weekly auto-regeneration, immediate regeneration after a goal-text edit, and manual refresh — i.e. every existing trigger already covers the archive with no new plumbing.

### 2.7 Module 6 — Therapy Relationship

**No backend changes** (guardrail: "zostaje w obecnej formie"). Confirmed the FE-facing endpoint is `app/api/v1/endpoints/health_check.py`, mounted at prefix `/health-check` (`GET /health-check/latest`, `/history`, `/status`, `POST /submit`, `/submit-voice`, `/quick-check`, `/quick-check-voice`, `/dismiss-banner`). Backed by `TherapyHealthCheck` + `HealthCheckDismissal` models. This is what flutter-mobile should keep calling when it re-homes the feature's UI into the Workspace tab.

### 2.8 Weekly Observations (Main, CS-13) — storage + read path

| Method | Path |
|---|---|
| GET | `/workspace/weekly-observations?limit=20` |
| GET | `/workspace/weekly-observations/latest` (returns `null` if none yet) |

```json
{"id": 3, "content": "...", "context_description": "...", "trigger_type": "post_session", "generated_at": "..."}
```
**data-analytics fills this** via `app.crud.workspace.create_weekly_observation(db, user_id, content_encoded, trigger_type, context_description_encoded=None)`. Trigger rule per spec (shared with CS-19): regenerate the day after a session; if no session in the past week, regenerate Monday morning. `trigger_type` records which rule fired. Old "Key Observations" data is untouched — grep found no dedicated table for it (believed to live on `TherapyTrackingSignal` and/or `WeeklyTherapySummary.key_insights`); this migration does not read, migrate, or delete anything there.

### 2.9 Mood-trend narrative cache (Main, CS-11) — storage + read path

**`GET /workspace/mood-trend-summary/latest`** → `{"bullets": ["...", "...", "..."], "generated_at": "..."}` (≤5 strings) or `null`.

**data-analytics fills this** via `app.crud.workspace.create_mood_trend_summary(db, user_id, bullets_encoded)` where `bullets_encoded = encode(json.dumps(list_of_up_to_5_strings))`.

### 2.10 Triage (CS-07)

**`GET /workspace/triage/{card_type}/{card_id}`** → pending (not-yet-consumed) chips for one card:
```json
{"count": 2, "items": [
  {"id": 501, "card_type": "debrief", "card_id": 88, "kind": "topic", "text": "Work stress",
   "suggested_thread_id": null, "realization_id": null, "status": "pending", "created_at": "..."},
  {"id": 502, "card_type": "debrief", "card_id": 88, "kind": "action_point", "text": "Journal nightly",
   "suggested_thread_id": null, "realization_id": null, "status": "pending", "created_at": "..."}
]}
```

**`POST /workspace/triage/submit`** — batch-apply the user's selections for one card. Partial-success: each selection is independent; one bad `proposal_id` doesn't fail the others.

Request:
```json
{
  "card_type": "debrief",
  "card_id": 88,
  "selections": [
    {"action": "agenda", "proposal_id": 501},
    {"action": "todo", "proposal_id": 502},
    {"action": "thread_new", "proposal_id": 501, "new_thread_title": "Work stress (optional override)"},
    {"action": "thread_existing", "proposal_id": 501, "thread_id": 3},
    {"action": "realization_toggles", "realization_id": 40, "show_on_timeline": true, "in_repo": false}
  ]
}
```
`action` × `proposal.kind` compatibility (enforced server-side, mismatches reported per-item, not batch-failing):
- `topic` / `question` → `agenda` | `thread_new` | `thread_existing`
- `action_point` → `todo`
- `realization_ref` → `realization_toggles` (no `proposal_id` required — acts directly on `realization_id`; if a matching `realization_ref` proposal_id IS supplied, it's also marked consumed)

Response:
```json
{"card_type": "debrief", "card_id": 88, "results": [
  {"action": "agenda", "proposal_id": 501, "realization_id": null,
   "created_agenda_item_id": 12, "created_todo_item_id": null, "thread_id": null, "error": null},
  {"action": "todo", "proposal_id": 502, "created_todo_item_id": 5, "error": null},
  ...
]}
```
An `error` string (non-null) means that specific selection was skipped (stale/foreign proposal_id, missing required field, kind/action mismatch, cross-user access) — the rest of the batch still applies.

**Unselected proposals are untouched** — they remain `status="pending"`, visible via `GET /workspace/triage/{card_type}/{card_id}`, and this exact same submit endpoint can be called again later for a manual send-to-workspace from Timeline (no separate endpoint needed).

**data-analytics fills the proposal storage** right after generating a debrief/prep-card/recording/between-session-note, via:
```python
from app.crud.workspace import create_triage_proposals_bulk
create_triage_proposals_bulk(db, user_id, card_type="debrief", card_id=debrief.id, proposals=[
    {"kind": "topic", "text": encode("...")},
    {"kind": "question", "text": encode("...")},
    {"kind": "action_point", "text": encode("...")},
    # realization_ref: text is None; the Realization row already exists from
    # the existing auto-detection pipeline (app/tasks/realization_detection.py)
    {"kind": "realization_ref", "realization_id": <existing realization id>},
])
```
None are pre-selected — there is no field for that. Dedup guidance from the brief ("duplicates scala z istniejącymi wątkami" — merge duplicates into existing threads instead of proposing a new one) is a data-analytics-side prompt/heuristic concern; the backend doesn't enforce it, but `suggested_thread_id` exists on `TriageProposal` for exactly this — set it when the AI thinks a topic matches an existing open thread, and FE can offer "thread_existing" pre-filled with that thread as the suggested action (still requires an explicit user tap — no auto-apply).

---

## 3. XP mapping proposal (**needs your sign-off**)

Hard rule preserved everywhere: XP only for actions (did-it / touched-it / closed-it), never for clinical content, never for `archive` (odklik).

| Action | Track | `action_type` key | Points | Idempotency flag |
|---|---|---|---|---|
| To-do marked done (**any origin** — homework or AI action point) | orca | `todo_done` | 2 | `TodoItem.xp_awarded` |
| Agenda item marked touched | orca | `agenda_touched` | 1 | `AgendaItem.xp_awarded` |
| Thread closed | **user** | `thread_closed` | 3 | `Thread.xp_awarded` |
| Relationship check-in submitted | user (**pre-existing, unchanged**) | `health_check` | 5 | `TherapyHealthCheck.xp_awarded` |

Rationale for the track split (existing taxonomy: user track = formal therapy-session-lifecycle actions [debrief, recording, prep_card, prep_viewed, health_check]; orca track = self-directed between-session care [between_session_note, reflect_conversation, symptom_score, realization]):

- **To-do done** and **agenda touched** → orca. Both are, by Workspace's own premise, things the user manages *between* sessions on their own initiative — the same category as writing a between-session note or logging a symptom score. This includes homework (`origin=therapist`) even though the therapist assigned it, because the *doing* of it happens as self-directed between-session follow-through, same as the rest of the orca-track set.
- **Thread closed** → user track. A thread represents a piece of *formal therapy content* ("Przerwane EMDR", "Kontakt z mamą") — closing one is resolution of therapy-session material, weighted like debrief/recording/prep_card (3 pts), not like a between-session self-care action.

**Two things flagged for explicit confirmation, not assumed:**

1. **To-do XP applies to action points too, not just homework.** The task prompt's parenthetical only named "homework checked done" as an example; the brief's hard rule ("XP wyłącznie za działania... zrobiłem") doesn't exclude AI action points. I implemented XP for **any** to-do completion regardless of origin. If you want homework-only XP, that's a one-line change (`action_type` becomes conditional on `item.origin`) — say the word and I'll ship it.
2. **`todo_undone` / `restore` never claw back XP.** Once granted, XP stays granted even if the user un-does a checkbox or restores an archived item — matching the fact that `deduct_user_track_points`/`deduct_orca_track_points` (which exist in `crud.py` for soft-delete scenarios) are never called from any Workspace endpoint. If accidental-tap abuse becomes a real problem, wiring those deduct functions into `undone`/`restore` is straightforward.

---

## 4. FIFO / ordering rules (for flutter-mobile's mental model)

- **Homework-for-Main**: 3 oldest OPEN to-dos, any origin, `ORDER BY created_at ASC LIMIT 3`.
- **Agenda list**: oldest first (`created_at ASC`) — it's a queue building toward the next session.
- **To-do full list**: homework (`origin=therapist`) block first, then AI action points block; oldest-first within each block.
- **Threads list**: `open`/`touched` before `queued`; oldest-first within each group.
- **Realizations repo / Weekly Observations / Mood-trend**: newest first (`created_at`/`generated_at DESC`).

---

## 5. Notes for flutter-mobile

- Every mutating endpoint returns the full updated resource (not 204) so the UI can update in place without a re-fetch, except `PUT /goals/reorder` (pre-existing, unrelated) and none of the new ones use 204.
- `queued` boolean on `ThreadResponse` is a convenience derived field (`status == "queued"`) — check either.
- The realization toggle endpoint requires **both** `show_on_timeline` and `in_repo` in the body — a request with only one is a 422, matching the brief's "no partial toggle state" rule. Wire the triage UI so the user can't dismiss a realization card without both being explicitly set (client-side gate; server just refuses incomplete payloads).
- `POST /workspace/triage/submit` is safe to call multiple times for the same card as the user triages incrementally, or later from a Timeline "send to workspace" affordance — proposals not yet referenced simply stay available.
- Deep-linking a notification/card into a specific Workspace item: use the resource IDs returned here (`agenda_item.id`, `todo_item.id`, `thread.id`) — coordinate the actual route strings with integration-devops's `CS-06_deeplink_contract.md`.

## 6. Notes for data-analytics

- You own: generating `TriageProposal` rows (`create_triage_proposals_bulk`), `WeeklyObservation` rows (`create_weekly_observation`), and `MoodTrendSummary` rows (`create_mood_trend_summary`) — all three functions are in `app.crud.workspace`, already committed, ready to import.
- ~~Thread `context_description` (AI-maintained, "updates when a new source is added") has **no auto-update wiring yet**~~ — **resolved 2026-07-06**, see Changelog §11: `app.tasks.thread_context.regenerate_thread_context` (data-analytics) is now enqueued from `POST /workspace/triage/submit`'s `thread_new`/`thread_existing` actions (backend-api).
- Goal Narrative generation itself (`openai_service.generate_goal_narrative`) is unchanged — I only added the archive-on-success side effect in `crud.update_goal_narrative`.
- **Known gap, flagged not fixed**: nothing currently enqueues goal-narrative regeneration when a thread is closed/touched or a to-do is done. The existing trigger set (`debrief`, `symptom_score`, `realization`, `between_session`, `recording`, `goal_created/edited/revised`, `manual_refresh`) doesn't include any Workspace action. If you want threads/todos to influence goal narratives, that requires a small addition to `app/tasks/goal_narrative.py::_get_trigger_text` (your file to extend, or flag to me if it needs a migration-adjacent change).

## 7. Migration

`alembic/versions/xx4y5z6a7b8c_add_workspace_tables.py`. `down_revision = "ww3x4y5z0a1b"` (was the single head — verified via `alembic heads` before authoring). Additive-only: 8 new tables + 3 new nullable columns, nothing renamed/dropped/retyped. Idempotent: every `CREATE TABLE` guarded by `inspect(bind).has_table(...)`, every `ADD COLUMN` guarded by a `get_columns()` membership check — safe to re-run against a DB with partial drift. `downgrade()` mirrors this with existence checks before every drop. Verified offline (no live DB touched):
- `alembic heads` → single head (`xx4y5z6a7b8c`) after adding this migration.
- Every new table's `CREATE TABLE` DDL compiled against the `postgresql` dialect contains no enum-drift tokens.
- `upgrade()` and `downgrade()` executed directly via `alembic.operations.Operations` against a throwaway SQLite DB seeded with `Base.metadata.create_all()` minus the workspace tables (simulating "at `ww3x4y5z0a1b`") — both ran clean, and **both were re-run a second time to confirm idempotency** (no-op, no errors).
- Will be run manually on Heroku (`heroku run alembic upgrade head --app mindsync`) by the operator — deploy ≠ migrate, per CLAUDE.md. Backend code is boot-safe without the migration having run yet (new tables simply won't exist; Workspace endpoints would 500 on first use until migrated — same risk profile as every other additive migration in this codebase; not a new hazard class).

## 8. Goal card actions (brief item — confirmed FE-only, no backend change)

- **"Mark As Done"** (renamed from "Mark As Archive") maps to the existing `PUT /goals/{id}/status {"status": "ACHIEVED"}` — the backend concept was always "achieved", the UI label is what's changing. No backend change.
- **"Revise Goal"**: brief asks to remove it from the menu. I did **not** remove backend support for `status=REVISED` — it's not trivially safe (REVISED creates a new linked goal via `parent_goal_id` and archives the old one; several other code paths — narrative regeneration, RAG indexing — assume this lifecycle exists). Per the task's own instruction ("kill only if trivially safe — otherwise leave and note it"): **left in place**. flutter-mobile should simply stop calling it from the UI menu; the endpoint stays available if you change your mind or need it for support/debug tooling.
- **"drop Goal"** (icon change only) maps to the existing `PUT /goals/{id}/status {"status": "DROPPED"}`. No backend change.
- **Narratives archive**: new, see §2.6.

---

## 9. Blast-radius recon (per CLAUDE.md Change Safety mandate)

**Who consumes what I touched:**
- `app/models/models.py` (`Realization`, `UserGoal`, `UserPreferences`, `User`): every existing caller of these classes (realizations.py, goals.py, health_check.py, therapy_tracking.py, timeline.py, dashboard.py, analytics.py, all background tasks, all existing tests) — all edits were pure *additions* (new nullable columns, new relationships). Verified: full `app.api.v1.api.api_router` import succeeds (304 routes registered, no import errors) after all edits.
- `app/crud/crud.py` (`USER_TRACK_POINTS`, `ORCA_TRACK_POINTS` dicts, `update_goal_narrative`): every existing call site of `award_user_track_points`/`award_orca_track_points`/`update_goal_narrative` (health_check.py, debriefs.py, session_recordings.py, between_sessions.py, symptoms.py, reflect.py, realizations.py, app/tasks/goal_narrative.py) — dict additions are non-breaking (existing keys untouched); `update_goal_narrative`'s new archiving side-effect is additive (extra `db.add()` before the existing commit, doesn't change its return value or existing callers' behavior).
- `app/api/v1/endpoints/goals.py`: added one new route (`GET /{goal_id}/narratives`) and one new import (`app.schemas.workspace`) — no existing route signature, response shape, or status code changed.
- `app/api/v1/api.py`: added one new `try/except ImportError`-guarded router registration block, following the exact existing pattern — an import failure in `workspace.py` would silently skip registration (boot-safe), not crash the dyno.
- `app/models/__init__.py`: added one import line — required so the RQ worker / Alembic / any process importing only `app.models` gets the full mapper registry (existing comment in that file explains why this is mandatory for `User`'s relationships to resolve).

**Boot-critical paths verified safe:**
- `app.main` imports the full router tree via `app.api.v1.api.api_router`, which now includes `workspace.py` — verified this imports cleanly standalone (`python -c "from app.api.v1.api import api_router"`, 304 routes, no exceptions).
- `Base.metadata.create_all(bind=engine)` runs at every web boot (app/main.py) — verified all 8 new tables + all additive columns compile cleanly against the `postgresql` dialect (no enum-drift, no unsupported types) and round-trip correctly against an in-memory SQLite engine (`Base.metadata.create_all` succeeds, matching what boot does on a fresh/dev DB).
- `configure_mappers()` (SQLAlchemy's full relationship-resolution pass) succeeds after importing `app.models` — every new `relationship()` string reference (`"User"`, `"Thread"`, `"UserGoal"`, etc.) resolves.

**Model ↔ migration ↔ prod DB agreement:** the migration's `CREATE TABLE`/`ADD COLUMN` statements were written by hand to mirror the SQLAlchemy model column-for-column (types, nullability, server_defaults) — no autogenerate diff was used (autogenerate wasn't run against a live DB per the "never run anything against prod" guardrail). Cross-checked manually: every column in `app/models/workspace.py` has a matching statement in the migration with the same type/nullable/default, and vice versa.

**SQLite ≠ Postgres**: per CLAUDE.md, SQLite silently tolerates things that are fatal on Postgres. All schema-safety assertions above were additionally verified by compiling DDL against the actual `postgresql` dialect (not just running against SQLite), which is what would have caught the H10-class bug.

---

## 10. Test coverage

- `app/tests/test_workspace_models.py` (26 tests): no-native-Enum checks per column, Postgres DDL compilation, mapper configuration, SQLite round-trip per table, cascade-delete-on-user-removal.
- `app/tests/test_workspace_crud.py` (25 tests): FIFO ordering (agenda, homework-for-Main), homework-pinned-first ordering, thread capacity/queueing/promotion, realization repo filtering, goal-narrative auto-archiving (including "no new narrative → no archive row"), XP awarding + idempotency for all three new action types, and explicit odklik/restore-never-awards-XP tests.
- `app/tests/test_workspace_endpoints.py` (27 tests): happy path for every endpoint, cross-user 404 for every ownership-scoped resource, invalid query-param 400, the full triage-submit matrix (agenda / todo / thread_new / thread_existing / realization_toggles / kind-mismatch partial-failure / cross-user / unselected-stays-pending), and overview aggregation + visit-marking.
- `app/tests/test_goal_narratives.py` (4 tests): the new `/goals/{id}/narratives` endpoint — empty archive, populated + ordering, 404 for missing/other-user goal.

**Total new: 82 tests, all passing.** Full-suite delta against the 2026-07-03 baseline (~21 pre-existing failures) reported in the implementation summary — zero new failures introduced by this batch.

---

## 11. Changelog

### 2026-07-06 — backend-api: MSV3.2 AI-layer integration pass

data-analytics built the AI-generation layer on top of this foundation
(commit `12543e3`: `app/tasks/triage_proposals.py`, `app/tasks/thread_context.py`,
3 new scheduler `setup_*` functions in `app/core/rq_scheduler_setup.py`, and
2 new `MomentTypeEnum` members) but could not touch backend-api's files per
the ownership split. This pass wires it in, and separately fixes two
Flutter wave-2B contract findings.

**Hooks wired (§6):**
- Enqueued `app.tasks.triage_proposals.extract_triage_proposals_for_card`
  fire-and-forget from the three card-generation pipelines outside
  data-analytics' ownership: `debriefs.py::_process_debrief_ai`,
  `prep_cards.py::_process_prep_card_ai`, and all three
  `between_sessions.py` generation/retry sites (`create_text_note`,
  `create_voice_note`, `retry_note_processing`), the last three via a
  shared `_enqueue_triage_extraction` helper gated to
  `processing_status == COMPLETED` (mirrors the existing
  `_enqueue_realization_detection` gate). Verified a Redis/enqueue failure
  can never flip an already-COMPLETED card back to FAILED — each hook has
  its own isolated try/except, same pattern as every other fire-and-forget
  hook in these files.
- Enqueued `app.tasks.thread_context.regenerate_thread_context`
  fire-and-forget from `POST /workspace/triage/submit`'s `thread_new` and
  `thread_existing` actions, immediately after `add_thread_source()`
  succeeds. Verified an enqueue failure does not fail the triage-submit
  request itself. Manual thread creation (`POST /workspace/threads`) does
  **not** trigger this — the user supplies (or omits) `context_description`
  directly at creation time.
- Registered the 3 new scheduler jobs (`setup_weekly_goal_narrative_refresh`,
  `setup_hourly_mood_trend_summary`, `setup_hourly_weekly_observations`) in
  `app/main.py`'s lifespan, in the same unguarded call-per-line style as
  every other `setup_*` job (error isolation lives inside each function via
  its own `ImportError` catch, not at the call site). Verified via an
  offline `import app.main` boot check: imports cleanly, and the
  notification-moment generator registry (`get_orchestrator().generator_count`)
  still reports all 11 generators (9 pre-existing +
  `MoodUpdateRequestGenerator` + `TherapyRelationshipCheckinGenerator`).

**Migration:** `yy5z6a7b8c9d` (down_revision `xx4y5z6a7b8c`, the single head
at the time — re-verified via `alembic heads`, not trusted from memory).
`ALTER TYPE moment_type_enum ADD VALUE IF NOT EXISTS` for
`MOOD_UPDATE_REQUEST` and `THERAPY_RELATIONSHIP_CHECKIN`, inside an
`autocommit_block()`, following the exact precedent set by
`ww3x4y5z0a1b_add_cadence_v3_moment_types.py`. This is the native-Postgres
counterpart to the Python-only `MomentTypeEnum` members data-analytics
added (`create_type=False`, so no boot-time DDL runs for them) — required
before either new generator can persist a moment row on Postgres.
Idempotent by construction (`IF NOT EXISTS`); downgrade is a documented
no-op (Postgres has no `DROP VALUE`). SQLite (test env) branch is a no-op
since the enum is stored as VARCHAR there. Not yet run against prod — per
CLAUDE.md, deploy ≠ migrate; sequencing is the operator's job.

**Contract fix — Flutter wave-2B finding (a):** `GET /workspace/agenda?view=active`
(and `GET /workspace/overview`'s `agenda` module, which shares the same
`_AGENDA_VIEWS` table) now returns **OPEN-only** items; previously it
included TOUCHED too. The product brief requires touched items gone from
the active list once they've been raised in session — a touched item's job
on the active agenda is done. `view=touched` is a new explicit view so the
touched-items history stays reachable (e.g. a future "recently touched"
surface). No known consumer depended on the old (broader) semantics — the
only client is the in-development Flutter Workspace screen, which was
already client-side filtering the response down to `status=="open"`.

**Contract fix — Flutter wave-2B finding (b):** `ThreadResponse` (used by
both the list and detail endpoints, §2.4) gained an additive
`context_snippet: Optional[str]` field — see the updated §2.4 example.
Lets Threads list cards show one line of context without a second detail
fetch. `ThreadDetailResponse` is unaffected (still returns the full,
untruncated `context_description`).

**Tests:** extended `app/tests/test_workspace_endpoints.py` (agenda
active/touched split, overview count, thread `context_snippet` truncation
+ null case, thread-context-regen enqueue + failure-isolation for both
triage-submit actions) and added `app/tests/test_triage_extraction_hooks.py`
(enqueue-fires-on-success and enqueue-failure-does-not-fail-generation for
all three newly-wired card types, plus the `between_sessions.py` gating
matrix). Full suite: confirmed zero new failures vs. the pre-existing
baseline (see the implementation summary for the exact count at the time
of this commit — the number drifts release to release as other agents'
unrelated pre-existing failures are fixed/reintroduced, so this doc
intentionally doesn't pin a specific number here).

**Doc provenance note:** this file is referenced by commit `5c75d39`'s
message but the commit itself never actually touched it (it lives outside
the `MindSync` git repo, in the sibling `Business_requirements/` directory,
so it was written straight to disk and simply never got a "the doc already
existed, just verify its location" callout in the follow-up task's recon).
No content was lost — this changelog is a pure append plus two in-place
example updates (§2.2, §2.4) to keep the reference sections truthful.

### 2026-07-06 — backend-api: MSV3.2 wave-3 (Workspace/TriageCard design handoff)

Small additive batch aligning the backend to the delivered design handoff
(`WorkspacePrep.dc.html` + `TriageCard.dc.html`), agreed with flutter-mobile
as a binding contract while the Flutter Workspace screen is built in
parallel. Three additions, all additive/backward-compatible; §1, §2.2, §2.4
above already reflect the new shape.

**1. Agenda item `kind` ("Temat"/"Pytanie" chip).**
- New nullable `agenda_items.kind VARCHAR(24)` column — `'topic'` | `'question'` | `NULL` (NULL == "topic" client-side, so every pre-existing row renders correctly with zero backfill).
- `AgendaItemResponse.kind` is additive (see updated §2.2 example).
- `POST /workspace/agenda` accepts optional `kind` — 422 on anything outside `{"topic", "question"}`.
- Flows through automatically:
  - `POST /workspace/triage/submit`, action=`"agenda"`: the created agenda item's `kind` is set to the source `TriageProposal.kind` (guaranteed `"topic"`/`"question"` — `_KIND_ALLOWED_ACTIONS` only permits `action="agenda"` for those two proposal kinds).
  - `PUT /workspace/threads/{id}/add-to-agenda`: always creates `kind="topic"` (a thread's one-tap agenda entry is definitionally a topic, never a question).
  - Manual `POST /workspace/agenda` (source_type="manual" or the new realization-pin mode, below): `kind` is whatever the caller passes, or `NULL`.

**2. Realization → Agenda pin ("Przypnij do agendy", Odkrycia module).**
- `POST /workspace/agenda` gains an alternate mode: `{"source_type": "realization", "source_id": <id>}`. `text` is not required/used in this mode — the pinned item's text is always the Realization's own (already-encrypted) text, copied server-side, so the two can never drift out of sync.
- Ownership check: the Realization must exist and belong to `current_user_id` — **404** otherwise (deliberately never 403, matching this router's stated "never leak existence via status code" convention — see the doc header). No new endpoint needed; this is additive to the existing `POST /workspace/agenda`.
- `AgendaSourceType` gains `"realization"` (full internal vocabulary: `debrief | prep_card | recording | between_session | manual | thread | realization`); a new narrower `AGENDA_CREATE_SOURCE_TYPES = {"manual", "realization"}` constant gates what a client may pass directly on `POST /workspace/agenda` — the other four values stay set only by their own internal flows (triage submit, thread add-to-agenda), exactly as before. Passing e.g. `source_type="debrief"` on this endpoint is a 422.
- **Duplicate-pin semantics (chosen, not obvious — flagging explicitly)**: pinning is idempotent per Realization. If a non-archived (`open` or `touched`) agenda item already exists for that `(source_type="realization", source_id=<realization_id>)` pair, `POST /workspace/agenda` returns **that existing item with a 200** instead of creating a duplicate. A genuinely new pin (no active prior pin, or the prior pin was archived/odklik'd by the user) returns **201** as usual. Rationale: re-tapping "Przypnij do agendy" on the same Realization card is a plausible double-tap / repeat-visit UX pattern, and the module already treats agenda uniqueness this way nowhere else — this establishes the pattern rather than following an existing one, so flutter-mobile should treat both 200 and 201 as success and just render the returned `AgendaItemResponse`.

**3. Thread status set (status-chip tap-cycle).**
- New `PATCH /workspace/threads/{id}/status`, body `{"status": "open"|"touched"|"closed"}` (see updated §2.4 table). Validates against exactly those three values — 422 otherwise (e.g. `"queued"`/`"archived"` are rejected; they're not settable via this endpoint at all).
- **No forked close logic**: the existing `PUT /threads/{id}/close` handler's body was extracted verbatim into a shared `_close_thread_with_side_effects()` helper (crud `close_thread()` + `award_user_track_points(..., "thread_closed", ...)`, both already idempotent via `Thread.xp_awarded`). `PATCH .../status` with `target="closed"` calls the exact same helper — the two entry points cannot drift.
- **Reopen-at-cap guard**: transitioning a `closed` thread back onto the active track (`closed`→`open` or `closed`→`touched`) re-checks `count_capacity_threads() >= MAX_ACTIVE_THREADS` (5) and returns **409** with a descriptive `detail` if full. The thread is left `closed` — nothing is silently re-queued, because reopening one specific closed thread out of FIFO order is a deliberate user action, distinct from the automatic queue-promotion that already happens inside `close_thread`/`archive_thread` for other threads.
- **Out-of-scope statuses rejected with 409, not silently allowed**: a thread currently `archived` or `queued` cannot be targeted by this endpoint at all (its current status isn't in the settable set `{open, touched, closed}`) — attempting to PATCH one returns 409 directing the caller to `PUT /threads/{id}/restore` for archived threads. Queued threads are promoted only by the existing automatic FIFO mechanism.
- Same-status PATCH (e.g. `open`→`open`) is a no-op returning 200 with no side effects (no double XP, no queue churn) — safe for the FE to call defensively.

**Migration:** `zz6a7b8c9d0e_add_agenda_item_kind.py` (`down_revision = "yy5z6a7b8c9d"`, the single head at authoring time — re-verified via `alembic heads`, not trusted from memory). Adds one nullable `agenda_items.kind VARCHAR(24)` column, guarded by the same `inspector.get_columns()` idempotency check used throughout this migration family (safe to re-run against partial drift). `downgrade()` drops it, same guard. **No native enum** — plain `String(24)` + the `AgendaItemKind` app-level constant class (never passed to `sqlalchemy.Enum`), per the H10 guardrail. Verified offline (no live DB touched, per CLAUDE.md): `alembic heads` → single head (`zz6a7b8c9d0e`); `upgrade()`/`downgrade()` executed directly via `alembic.operations.Operations` against a throwaway SQLite DB seeded to simulate "at `yy5z6a7b8c9d`" (bare `agenda_items` table without `kind`) — both ran clean and were each re-run a second time to confirm idempotency; the column's DDL was compiled against the `postgresql` dialect and contains no enum-drift tokens. Not yet run against prod — deploy ≠ migrate; sequencing is the operator's job (`heroku run alembic upgrade head --app mindsync`).

**Triage / realization "Odkrycie" group — confirmed, no backend change needed.** The design's 4th triage group bookmarks a realization into the repo (`in_repo=true`). Checked `app/tasks/triage_proposals.py` (data-analytics' extraction job): `_VALID_KINDS = {"topic", "question", "action_point"}` — `TriageProposalKind.REALIZATION_REF` is **never actually generated** ("Realizations are NOT duplicated here — they already flow through their own pipeline", per that file's own docstring). So in practice no `TriageProposal` ever carries `kind="realization_ref"` today. The backend-side handling for it (`action="realization_toggles"` in `POST /workspace/triage/submit`, §2.10) is left in place unchanged — additive/dormant, not removed, in case data-analytics wires this up later — but flutter-mobile's new single-tap "add to repo" affordance on a Realization card should simply call the pre-existing `PUT /workspace/realizations/{id}/toggles` directly with `{"show_on_timeline": <keep current or true>, "in_repo": true}` (both fields required together, per §2.5/§5) rather than routing through triage-submit. No forced changes on either side.

**Tests:** `app/tests/test_agenda_item_kind_migration.py` (new, 7 tests — migration file metadata/single-head check, SQLite upgrade/downgrade round-trip + idempotency both directions, Postgres DDL compile). Extended `app/tests/test_workspace_models.py` (+2: kind is String not Enum, kind SQLite round-trip), `app/tests/test_workspace_crud.py` (+6: `create_agenda_item(..., kind=...)` persistence, `get_active_agenda_item_for_source` happy/absent/archived-ignored/cross-user), `app/tests/test_workspace_endpoints.py` (+21: agenda kind create/list/422/thread-add-to-agenda-sets-topic, realization pin happy/idempotent-200/re-pin-after-archive/404-missing/404-cross-user/422-missing-source_id/422-manual-without-text/422-bad-source_type, full thread-status-set matrix including reopen-at-cap 409 and close-side-effect parity with the existing close endpoint, plus a `kind` assertion added to the existing triage-submit-agenda test). Full suite run clean (see implementation summary for the exact pass/fail delta at the time of this commit — this doc intentionally doesn't pin a specific number, per the same rationale as the previous entry).
