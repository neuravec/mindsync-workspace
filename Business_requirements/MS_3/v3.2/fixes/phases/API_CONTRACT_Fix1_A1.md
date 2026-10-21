# MSV3.2 Fix.1 — API contract, PHASE A / slice A1 (backend-api)

> Covers tasks **A1** (item lifecycle + archives), **A2** (triage chip persistence),
> **A3** (new module "Tematy i pytania"), **A4** (agenda sourcing/tags/pin sync),
> **A5** (thread statuses + context), **A6** (todos repeats + completion log),
> **A12** (session schedule / prep-debrief markers).
> Maps onto `API_CONTRACT_Fix1.md` §1, §2, §3, §4, §10. A1 was told NOT to edit the
> shared `API_CONTRACT_Fix1.md` / `STATUS.md` files directly (race risk with the
> concurrent A7–A13 session) — this file + `STATUS_A1.md` are the deliverable; the
> lead merges into the shared files.
>
> All endpoints below are mounted under `/api/v1/workspace` unless noted otherwise
> (session-state is under `/api/v1/therapy-tracking`). Auth: Firebase bearer token via
> `deps.get_current_user`, same as every other Workspace endpoint. Cross-user access
> always 404s (never 403 — "never leak existence", matches the rest of the router).
> Encryption: all free-text fields are encrypted at rest (`encode`/`decode`); response
> JSON below is always the **decrypted** plaintext.

---

## §1 — Workspace item lifecycle (all list modules)

Every module below implements the same 4-verb contract: **close**, **list-closed
(archive)**, **restore**, **hard-delete**. Badge counts ("N closed since archive last
opened") are **FE-computed** from the archive list's length delta vs. a locally-stored
"last opened" marker — no BE field for it (matches the existing Workspace pattern: only
`GET /workspace/overview`'s `has_new_since_last_visit` is BE-computed, and that's a
different, module-overview-level concern, unaffected by this slice).

### Agenda (`AgendaItem`)
| Verb | Method + path | Notes |
|---|---|---|
| Close | `PUT /workspace/agenda/{id}/touch` *(pre-existing, unchanged)* | This IS the "close" action for Agenda — the checkbox tick. Sets status `touched`, cascades to a linked Thread (→ `touched`) if any. **Do not rename/alter** — CS-07 spec explicitly requires the existing checkbox-close mechanic untouched. |
| List-closed (archive) | `GET /workspace/agenda?view=touched` *(ordering FIXED this slice)* | Now newest-first by `touched_at` (was oldest-first / queue order before — that ordering is still used for `view=active`). This is the "Twoje zakończone tematy" / "Your closed topics" (CS-07) archive. |
| Restore | `PUT /workspace/agenda/{id}/restore` *(pre-existing, unchanged)* | Works from any status; sets `open`. |
| Hard-delete | **`DELETE /workspace/agenda/{id}`** *(NEW)* | 204. Permanent, never archived. |
| Edit name | **`PUT /workspace/agenda/{id}`** *(NEW)* | Body `{"text": "..."}` → `AgendaItemResponse`. Position unchanged (CS-08). |

Also exists (unchanged, pre-dates this slice, documented for completeness): `PUT
/workspace/agenda/{id}/archive` + `GET ?view=archived` + `PUT
/workspace/agenda/{id}/restore` — a **separate** "odklik" semi-archive used internally
by the triage chip-deselect flow (§2), NOT the CS-07 checkbox-close archive above. Two
distinct mechanisms on the same model, by design — see `app/models/workspace.py`
`AgendaItemStatus` docstring.

### Todos (`TodoItem`) — see also §4 for repeats
| Verb | Method + path | Notes |
|---|---|---|
| Close (done) | `PUT /workspace/todos/{id}/done` *(pre-existing; extended this slice — see §4)* | Now also logs a `TodoCompletion` row every call. |
| List-closed (archive) | `GET /workspace/todos?view=done` *(ordering FIXED this slice)* | Newest-first by `done_at`. This is CS-11 "Zrobione" / "Done". |
| Restore | `PUT /workspace/todos/{id}/undone` *(pre-existing, unchanged)* | |
| Hard-delete | **`DELETE /workspace/todos/{id}`** *(NEW)* | 204. |
| Edit name + repeat | **`PUT /workspace/todos/{id}`** *(NEW)* | See §4. |

### Threads (`Thread`)
| Verb | Method + path | Notes |
|---|---|---|
| Close (domknij) | `PUT /workspace/threads/{id}/close` OR `PATCH /workspace/threads/{id}/status {"status":"closed"}` *(pre-existing, unchanged)* | Both share one code path (`_close_thread_with_side_effects`) — never diverge. |
| List-closed (archive) | **`GET /workspace/threads?view=closed`** *(NEW view)* | Newest-first by `closed_at`. This is CS-15 "Domknięte wątki" / "Closed threads" — **distinct** from the pre-existing `view=archived` (odklik, a different/older mechanism — CS-15 removed its UI entry point on the thread card but the endpoint stays for backward-compat/internal use). |
| Restore | `PUT /workspace/threads/{id}/restore` *(pre-existing, unchanged)* | Works from `closed` or `archived`. Re-checks the ~5-active display threshold — see §3 "no queue-state cap" note. |
| Hard-delete | **`DELETE /workspace/threads/{id}`** *(NEW)* | 204. Cascades `ThreadSource` rows; any `AgendaItem.thread_id` pointing at it is set NULL (DB `ondelete=SET NULL`, pre-existing FK). No "Edytuj nazwę"/"Usuń" 3-dot menu is specced for threads (CS-14/15/18 don't mention one) — exposed for A1's generic "hard-delete per module" completeness criterion; FE may wire it or not. |

### Tematy i pytania (`TopicQuestionItem`) — NEW module, see §2/§3
See full CRUD table below (§3-adjacent). Close/list-closed/restore/hard-delete/edit-name
all present, same shape as the others.

### Goals — **NOT implemented this slice.**
A1's task text lists "goals" among the 5 lifecycle modules, but `goals.py` (the only file
that could host this) is **owned by the concurrent Fix.1 agent** for this session (per
this slice's explicit file-ownership boundary) — not touched. CS-21 ("Zakończone cele"
archive) needs coordination with that agent / the lead. See `STATUS_A1.md`.

---

## §2 — Triage chips on output cards (CS-03)

Two flows now coexist on the same `TriageProposal` table (disjoint status values, zero
interference):

### Legacy batch-submit flow (pre-existing, UNCHANGED — not touched this slice)
- `GET /workspace/triage/{card_type}/{card_id}` → pending-only proposals (status=`pending`).
- `POST /workspace/triage/submit` → batch `{action, proposal_id, ...}` selections,
  proposal status flips to `consumed` (terminal, no un-consume).
- Kept working, unmodified, for backward compatibility. **Not** what Phase F (FE
  triage) should build against — see below.

### NEW single-tap chip-toggle flow (CS-03's actual mechanic — build against THIS)
| Method + path | Purpose |
|---|---|
| **`GET /workspace/triage/{card_type}/{card_id}/chips`** | ALL proposals for the card (pending AND selected — nothing ever filtered out), each with a live `chip_state`. Response = `TriageProposalListResponse` (see shape below). |
| **`POST /workspace/triage/{proposal_id}/toggle`** | The single-tap action. Cycles: `unselected → selected` (creates the module row) → `selected+open, tap → unselected` (deletes the row, chip resets) → `selected+closed (item was closed IN ITS MODULE, not via the chip), tap → selected+open` (restores the row — same row, not a new one). Response = one `TriageProposalResponse` with `chip_state` always populated. |

**`TriageProposalResponse` shape** (both endpoints):
```json
{
  "id": 42,
  "card_type": "debrief",
  "card_id": 100,
  "kind": "topic",
  "text": "Talk about work stress",
  "suggested_thread_id": null,
  "realization_id": null,
  "status": "pending | selected",
  "created_at": "2026-07-17T10:00:00Z",
  "chip_state": "unselected | selected | closed",
  "linked_item_type": "topic_question_item | todo_item | thread | null",
  "linked_item_id": 17
}
```

**Kind → target module → linked_item_type, on select:**
| `kind` | Group label (PL / EN) | Creates in | `linked_item_type` |
|---|---|---|---|
| `topic` | Tematy / Topics | `TopicQuestionItem` (kind=topic) | `topic_question_item` |
| `question` | Pytania / Questions | `TopicQuestionItem` (kind=question) | `topic_question_item` |
| `action_point` | Action pointy / Action points | `TodoItem` (origin=ai) | `todo_item` |
| `thread` **(NEW kind, added this slice — was the "known gap")** | Wątki / Threads | `Thread` (new, OR merges into `suggested_thread_id` if that thread still exists and isn't closed/archived) | `thread` |
| `realization_ref` | Odkrycie / Realization (kept per master-plan decision 2 — 5th, non-mandatory group) | *(no new row — toggles the existing Realization's `in_repo` flag)* | *(n/a — dispatches via `realization_id`, not `linked_item_type`)* |

Group **display order** on the card per CS-03: Tematy · Pytania · Wątki · Action pointy
(Odkrycie appended after, per master-plan decision 2). Group header hidden when empty.
No AI change needed — `kind` was already produced by the existing extraction for
topic/question/action_point/realization_ref; **`thread`-kind proposals require
data-analytics' AI layer to actually emit them** (this slice adds the BE plumbing —
model/schema/endpoint support — but does not touch prompt/extraction code, which the
concurrent agent's file ownership covers, if it needs to change at all. Flagging for
the lead — see `STATUS_A1.md`).

**`realization_ref` toggle semantics** (interpretation — not explicitly specced beyond
"keep it as an additional group", flagged for product confirmation): tap ON → the
realization becomes visible in the Workspace repo (`in_repo=true`, `show_on_timeline`
left as-is). Tap OFF (deselect) → `in_repo=false` (dropped from the Workspace repo) but
`show_on_timeline` untouched — nothing is removed from Timeline, per the "nothing lost"
guardrail.

**Chip persistence**: proposals are never deleted or filtered out of the `/chips`
response — CS-03's "chip state must survive card reopen from Timeline forever" is
satisfied by construction (no TTL, no purge).

**Self-healing**: if the linked module row was hard-deleted through its OWN module
(not via the chip), the next toggle tap on that chip resets it to `unselected` instead
of erroring.

---

## §3 — Agenda feeds, source tags, thread/realization pin sync

### 3a. New module: "Tematy i pytania" (`TopicQuestionItem`, CS-05)
| Method + path | Body | Response |
|---|---|---|
| `POST /workspace/topic-questions` | `{"text": str, "kind": "topic"\|"question" (default "topic")}` | 201, item (source_type=`manual`) |
| `GET /workspace/topic-questions?view=active\|closed` | — | list. `active`=oldest-first; `closed`=newest-first (P2 archive "Zamknięte tematy i pytania") |
| `PUT /workspace/topic-questions/{id}` | `{"text": str}` | edit name |
| `PUT /workspace/topic-questions/{id}/close` | — | checkbox close → archive |
| `PUT /workspace/topic-questions/{id}/restore` | — | back to active |
| `DELETE /workspace/topic-questions/{id}` | — | 204, permanent |
| `PUT /workspace/topic-questions/{id}/add-to-agenda` | — | Creates an `AgendaItem` copy (see 3b). **The entry stays open here** — not a toggle (CS-05: "user closes it in this module when it is resolved"). **Not idempotent** — repeated taps create multiple agenda rows (deliberate: two distinct topics can share one origin card, so de-duplicating on source would risk silently merging them — see code comment in `workspace.py`). |

Item shape:
```json
{"id": 5, "text": "...", "kind": "topic|question", "source_type": "debrief|prep_card|recording|between_session|manual",
 "source_id": 100, "status": "open|closed", "created_at": "...", "closed_at": null}
```

### 3b. Agenda source tags (`AgendaItem.source_type`, CS-06)
Fixed vocabulary, unchanged this slice (`AgendaSourceType`), tag strings for FE:

| `source_type` | PL | EN |
|---|---|---|
| `debrief` | Po terapii | After therapy |
| `prep_card` | Prep | Prep |
| `recording` | Nagranie | Recording |
| `between_session` | Między sesjami | Between sessions |
| `manual` | Dodane ręcznie | Added manually |
| `thread` | Wątek | Thread |
| `realization` | Realizacja | Realization |

When a "Tematy i pytania" entry is promoted via `add-to-agenda`, the resulting
`AgendaItem.source_type`/`source_id` are **copied verbatim** from the topic/question's
own origin (so the tag reflects the ORIGINAL card, or `manual` — never a generic
"from Tematy i pytania" tag, since CS-06's fixed vocabulary has no such entry).

### 3c. Pin/toggle feeds into Agenda (CS-06 sourcing model, CS-14, FIX.05)
Nothing enters Agenda without a user tap — audited, confirmed: manual POST, the 3 pin/promote
endpoints below, and the legacy triage-submit `action=agenda` path are the **only**
agenda-item creation paths.

> **G-fix correction (post-Phase-G, operator-ordered):** this section originally
> claimed `PUT /workspace/threads/{id}/add-to-agenda` had "no live consumer" and
> changed its response shape outright. That claim was **wrong** — already-shipped
> production app builds call exactly this route/method and parse the response with
> a strict `AgendaItemModel.fromJson` requiring non-nullable
> `text`/`source_type`/`status`/`created_at` (the OLD `AgendaItemResponse` shape).
> Those builds live for weeks; shipping the toggle response on this route would
> throw for them. The fix: **the old route is restored to its pre-Fix.1
> ADD-only contract** (still made idempotent — the no-duplicates improvement is
> kept), and the toggle semantics this section originally described were **moved
> to a new, separate route**, `PUT /workspace/threads/{id}/agenda-pin`, mirroring
> the existing `PUT /workspace/realizations/{id}/agenda-pin` naming. The table
> below reflects the corrected, final contract. NEW app builds (and the Fix.1
> Phase C/D/E frontend work in progress, not yet shipped) must call the
> `/agenda-pin` route for thread toggle behavior, not `/add-to-agenda`.

| Feed | Method + path | Semantics |
|---|---|---|
| Tematy i pytania → Agenda | `PUT /workspace/topic-questions/{id}/add-to-agenda` | Plain add (see 3a) — not a toggle. Unaffected by the G-fix. |
| Thread → Agenda (legacy-compat) | **`PUT /workspace/threads/{id}/add-to-agenda`** *(RESTORED to its pre-Fix.1 shape by the G-fix)* | Returns a full `AgendaItemResponse` (id, text, source_type, source_id, thread_id, kind, status, created_at, touched_at, archived_at) — the shape already-shipped builds require. ADD semantics, idempotent, **never toggles off**: if an active pin already exists for this thread it is returned unchanged (200, no duplicate — the Fix.1 A4 no-duplicates fix is preserved); otherwise one is created (tag `Wątek`). Old builds have no UI path to call this expecting an "unpinned" result, so there is no behavior to preserve there. |
| Thread → Agenda (toggle, NEW) | **`PUT /workspace/threads/{id}/agenda-pin`** *(NEW route — G-fix; carries the toggle semantics originally, and wrongly, placed on `/add-to-agenda` above)* | Response `PinToggleResponse` `{"pinned": bool, "agenda_item_id": int}`. Idempotent toggle: tap → pin (creates, tag `Wątek`); tap again → unpin (odklik-archives the agenda item — restorable, no orphan); tap again → re-pin. This is what Phase F / new app builds should build against for the thread "Dodaj do agendy" toggle button. |
| Realization → Agenda | **`PUT /workspace/realizations/{id}/agenda-pin`** *(NEW — fixes FIX.05)* | Same toggle shape/semantics as the thread toggle route above, tag `Realizacja`. The realization itself is never touched/deleted — only its agenda presence toggles. Pre-existing `POST /workspace/agenda {"source_type":"realization","source_id":N}` (idempotent create-only, no unpin) still works unchanged and targets the same underlying pin state — both endpoints are two doors into the same derived state. Unaffected by the G-fix (this route was always new, per its own contract line above — no compat issue). |

**Pin-state derivation (no dedicated "pinned" column, by design)**: "is X pinned" = "does
an active (non-archived) `AgendaItem` exist with `source_type=X, source_id=<X.id>`".
Consequence: **deleting the agenda item directly** (`DELETE /workspace/agenda/{id}`,
§1) also un-derives the pin — no orphans, no stuck state, satisfies FIX.05's "no stuck
pins" requirement without extra bookkeeping code. This holds for both thread routes
above and the realization route — all three ultimately derive from the same
`get_active_agenda_item_for_source` query; the legacy thread route additionally
reuses `create_agenda_item` directly (via the new `get_or_create_agenda_pin` CRUD
helper) instead of `toggle_agenda_pin`, since it must never archive/unpin.

### 3d. Thread statuses + context (A5, CS-15)
Status chain `open → touched → closed` (or `→ archived` = odklik) — **unchanged, already
correct** from the MSV3.2 batch: `touch_agenda_item` cascades a linked thread to
`touched` automatically when its agenda item is checked off. `context_description`
AI-regeneration-on-new-source hook — already wired (`_enqueue_thread_context_regen`),
unchanged. `sources` list always returned even if the description generation failed
(nullable field) — matches CS-15's "on failure show sources without description".

**"5 z N aktywnych" counter (CS-17)**: no new field needed — `GET
/workspace/threads?view=active`'s existing `count` field IS the "aktywnych" total.
FE: hide the counter at `count <= 5`; else render `"{5} z {count} aktywnych"` (2nd number
= `count`, first number is always the literal "5" display default per spec, not derived).

**"No queue-state cap" (CS-15 decision — behavior CHANGED this slice)**: reopening a
closed thread via `PATCH /workspace/threads/{id}/status {"status":"open"}` while 5
threads are already active **no longer 409s**. It now queues (`status: "queued"`,
`queued: true` in the response) instead of blocking — matches CS-15's explicit "5 is a
display default, not a cap; no queue state [that blocks the user]". The pre-existing
`create_thread` at-capacity → `queued` behavior (never blocks) was left as-is; only the
reopen path's hard 409 was relaxed to match. `MAX_ACTIVE_THREADS=5` and the `queued`
mechanism itself are otherwise unchanged (still used for auto-promotion on
close/archive).

---

## §4 — Todos: repeats + completion log (A6, FIX.01, CS-10)

### Repeat field
`TodoItem.repeat_freq: string | null` — `null` (no repeat, default) | `"daily"` |
`"weekly"` | `"monthly"`. Set via `PUT /workspace/todos/{id}` (§1's edit endpoint):
```json
{"text": "optional new text", "repeat_freq": "daily" | "weekly" | "monthly" | null}
```
Both fields independently optional (send only what changed); `repeat_freq: null`
explicitly clears an existing repeat. At least one field required (422 otherwise).

### Rollover mechanics — **lazy, self-healing, no cron job**
This slice's file ownership excludes `app/tasks/*` (owned by the concurrent Fix.1
agent). Instead of a scheduled job flipping repeating to-dos back open on their repeat
day, **every `GET /workspace/todos*` call runs a sweep first**
(`ws_crud.sweep_repeating_todos`): any `DONE` item with a `repeat_freq` whose interval
has elapsed since `done_at` flips back to `OPEN` (`done_at` cleared) before the response
is built. Interval = fixed offset from `done_at` (daily=1d, weekly=7d, monthly=30d) —
calendar-simple, not calendar-exact (no "same weekday next week" alignment; not specced
beyond "on its repeat day"). Consequence: **a missed period never stacks** — reopening a
task that's been done for 40 days still yields exactly one OPEN row, not multiple queued
reopens (self-heals on next access regardless of how long the app was closed).

### Completion log
Every `PUT /workspace/todos/{id}/done` call inserts a `TodoCompletion` row
(`{id, completed_at}`) — for a non-repeating item this is its one-and-only completion;
for a repeating item it accumulates one row per cycle, which is how completion history
survives the `status`/`done_at` reset on rollover.

| Method + path | Response |
|---|---|
| **`GET /workspace/todos/{id}/completions`** *(NEW)* | `{"items": [{"id", "completed_at"}], "count"}`, newest first. Read-only history — no restore-from-a-past-cycle (only the CURRENT done state is restorable, via the pre-existing `PUT /workspace/todos/{id}/undone`; restoring a specific historical cycle isn't specced and isn't operationally well-defined for a repeating item, so it's out of scope — flagged in STATUS_A1.md). |

### Homework-for-Main (CS-10) — unchanged this slice
`GET /workspace/todos/today?limit=3` — 3 oldest OPEN, FIFO, any origin (pre-existing;
now also runs the repeat-rollover sweep first, so a just-reopened repeating task can
surface immediately). "Due dates" remain explicitly out of scope (author decision,
unaffected).

---

## §10 — Session schedule (Main "Next therapy session" state machine, A12, CS-09)

### Schedule fields (audited — unchanged, already correct)
`GET`/`PUT /users/therapy-schedule` (owned by `users.py`, not touched this slice) already
expose: `schedule: [{day_of_week, time_of_day, therapist_name}]`, `frequency`
(weekly/biweekly/custom), `custom_interval_days`, `next_session_date`,
`custom_sessions: [{date, time_of_day, therapist_name}]`. This IS "the same fields
settings write" CS-09 requires — confirmed, no BE change needed here.

### NEW: `GET /therapy-tracking/session-state`
Backend-computed state for the Main module's state machine — added because Main
currently has no single authoritative state signal to read (root cause of the embedded
"gets stuck after debrief" bug — see below).

```json
{
  "state": "no_therapy_set | prep_cta | scheduled | debrief_cta | between_sessions",
  "next_session_date": "2026-07-20T10:00:00+00:00 | null",
  "last_session_date": "2026-07-13T10:00:00+00:00 | null",
  "with_whom": "Dr. Miller | null",
  "frequency": "weekly",
  "prep_done": true,
  "debrief_done": false
}
```
- `no_therapy_set`: no schedule AND no custom sessions.
- `debrief_cta`: a session started **recently** (within ~30h — see "recency window"
  below) and has no debrief yet. Covers spec's "session already happened" — there is no
  separate `session_happened` state, the button IS the debrief CTA.
- `prep_cta`: no `debrief_cta` trigger, and no prep card exists for the current
  between-sessions window.
- `between_sessions`: prep done, and the wide-window last session IS debriefed.
- `scheduled`: prep done, session hasn't started yet (plain countdown, no CTA).
- `with_whom`: `therapist_name` of the schedule entry matching the upcoming
  occurrence's weekday; falls back to any entry's/custom session's non-null name.

**"Recency window" design note (embedded-bug fix, and why 2 lookback windows exist)**:
a recurring weekly/biweekly day-of-week always has SOME occurrence within a wide
per-cadence lookback, even the instant the schedule is first saved (no
"schedule-created-at" exists to distinguish a real past session from one that predates
the schedule). Using a wide window to DECIDE `debrief_cta` would make every brand-new
schedule look like a missed, undebriefed session. Fix: `debrief_cta` is gated on a
**narrow ~30h recency window** (mirrors the existing `_SESSION_LOOKBACK_HOURS=26.0` in
`post_session_reflection_generator.py` for the same class of problem); `last_session_date`
/ `debrief_done` (informational fields) and the `prep_done` boundary use a **wide,
per-cadence window** (weekly ≈8d, biweekly ≈15d, custom ≈interval+1d) so they stay
accurate even after the user hasn't opened the app in a while.

**Embedded bug ("after debrief the module never switched to between-sessions, next
session stopped displaying")** — root-caused to: `UserPreferences.next_session_date` is
only ever recomputed when the user edits their schedule in settings; nothing advances it
as time passes, so once a session's date passes it goes stale forever for any reader
that trusts the stored column. **This new endpoint sidesteps that** by recomputing
`next_session_date`/`last_session_date` **fresh on every call** via
`app.utils.therapy_schedule_utils.compute_next_session_date` /
`compute_last_session_datetime` (pre-existing utils, unchanged), using the stored value
only as the biweekly-parity anchor — never trusting it as "the" next date. **Caveat**:
the OLD `GET /users/therapy-schedule` endpoint (in `users.py`, out of this slice's file
ownership — see `STATUS_A1.md`) still returns the raw, potentially-stale
`prefs.next_session_date` column unchanged; a full root-cause fix there needs either (a)
`users.py`/`crud.py` access coordinated with the concurrent agent, or (b) the lead
assigning it. Phase C (FE Main) should build the "Next therapy session" module against
`GET /therapy-tracking/session-state`, not the old schedule endpoint's raw
`next_session_date`.

### Prep/debrief-done markers
Exposed via the fields above (`prep_done`, `debrief_done`) rather than as separate
endpoints — computed from the pre-existing `crud.has_debrief_for_session` and
`crud.get_latest_session_prep_card` (both unchanged, already existed before this slice).

---

## Deviations from `API_CONTRACT_Fix1.md`'s original §1–§4/§10 TBD text

- §1: badge counts confirmed FE-computed (not a BE field) — see above.
- §2: the pre-existing batch-submit endpoint is kept, NOT replaced — a new
  parallel toggle flow was added instead (`/chips` + `/{id}/toggle`). Phase F should
  build against the new one only.
- §3: `PUT /workspace/threads/{id}/add-to-agenda`'s response shape was originally
  changed (`AgendaItemResponse` → `PinToggleResponse`) on the claim that Phase F
  was the only consumer and hadn't been built yet. **That claim was wrong** (G-fix,
  post-Phase-G): already-shipped production builds call this exact route and parse
  the old `AgendaItemResponse` shape strictly. Corrected: the old route is restored
  to `AgendaItemResponse` + ADD-only idempotent semantics; the toggle semantics
  moved to a new route, `PUT /workspace/threads/{id}/agenda-pin`. See §3c.
- §4: "Homework view (Main): BE endpoint or FE-side sort?" — confirmed BE endpoint
  (`GET /workspace/todos/today`, pre-existing, unchanged contract).
