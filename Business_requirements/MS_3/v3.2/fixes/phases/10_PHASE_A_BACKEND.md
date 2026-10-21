# PHASE A — Backend (MSV3.2 Fix.1) — run in repo `MindSync/`

## SYSTEM INSTRUCTIONS (read fully before any tool call)

You are a fresh Claude Code session acting as the team lead for the BACKEND slice of the
MSV3.2 Fix.1 batch. Project rules come from `CLAUDE.md` (auto-loaded) — the Change Safety &
Impact Recon section is MANDATORY for every change. Delegate implementation to your domain
agents (`backend-api` for models/CRUD/endpoints/migrations, `data-analytics` for AI/prompt/
summary/analytics work, `qa-testing` at the end) per the ownership map; keep the agent count
lean (budget rules). You may do small audits/reads yourself.

- Repo: `C:\Users\mikol\Notebooks\MindSync\Heroku\MindSync` — branch **main**. Do not touch the Flutter repo.
- **Commit locally, stage only files you touched, NEVER push, NEVER run anything against prod DB.**
- Migration chain: verify the current SINGLE head by reading `alembic/versions/` (expected `zz6a7b8c9d0e`);
  any new migration chains from it, is idempotent, and follows the String(n)-not-Enum(PyEnum) rule.
  Compile new DDL with the `postgresql` dialect offline (SQLite CI hides Postgres failures).
- The 3 MSV3.2 migrations (`xx4y5z6a7b8c`, `yy5z6a7b8c9d`, `zz6a7b8c9d0e`) may NOT be applied on prod yet.
  Code must degrade gracefully if a table is missing — nothing reachable from import/lifespan may crash-loop boot.
- Coordination: read `00_MASTER_PLAN.md` (decisions log) in this folder. When done, fill **every TBD** in
  `API_CONTRACT_Fix1.md` with final shapes and APPEND your report to `STATUS.md` (template inside).
- Test baseline: 21 BE failures pre-exist (2026-07-03). No new failures allowed; new code needs tests.
- **AUDIT FIRST**: the MSV3.2 Workspace batch already shipped models/CRUD/endpoints for agenda items,
  todos, threads, realizations, goals + triage/AI hooks (commits `5c75d39`, `12543e3`, `f789a4b`, `3ce9087`).
  For every task below, first check what exists and extend rather than duplicate.

## Tasks

### A1 · Workspace item lifecycle — archives (1.2 CS-04 + P2)
Every list item in topics&questions / todos / threads / agenda / goals has exactly two states:
open and closed. Closing sets a close date and moves it to that module's own archive (separate per type);
restore reopens it (returns to top of active list); red „Usuń" = permanent delete, never archived.
Provide: close, list-closed (newest first, with close date), restore, hard-delete. Badge counts
("closed since archive last opened") may be FE-computed — decide and document in the contract.

### A2 · Triage chip persistence (1.2 CS-03; supersedes 1.1 CS-07 mechanics — see master plan decision 1)
Output cards (after-therapy, prep, between-sessions note, recording) already end with AI-extracted
elements. Each candidate must carry: type label (Temat / Pytanie / Wątek / Action point; keep existing
Odkrycie group if present), text, source ref (card id + card type), and a persisted chip state:
unselected | selected (+ linked item id) | closed. Select → instantly create the item in the target
module (Temat/Pytanie → Tematy i pytania; Wątek → Wątki; Action point → Do zrobienia); deselect →
withdraw it; item closed in its module → chip shows closed, tap restores. State survives reopening
the card from Timeline forever. No new AI pass — reuse existing extraction. If extraction returns
nothing, FE hides the section (no BE change needed beyond empty list).

### A3 · New module data: „Tematy i pytania" (1.2 CS-05)
A list collecting all tematy & pytania (from chips or manual adds). Rows: text, source tag
(the origin card type or „Dodane ręcznie"), open/closed + archive („Zamknięte tematy i pytania"),
edit-name, permanent delete, and „Dodaj do agendy" (adds to agenda; the entry itself STAYS open here).
Audit whether the workspace tables can host this (e.g. agenda-item kind or a topics table); if a new
table is needed → migration per rules above.

### A4 · Agenda sourcing, tags & pin sync (1.2 CS-06, CS-14, CS-19; 1.1 FIX.05)
Agenda items carry a source tag: PL „Po terapii"/„Prep"/„Nagranie"/„Między sesjami"/„Dodane ręcznie"/
„Wątek"/„Realizacja" (`agenda.kind` migration `zz6a7b8c9d0e` exists — audit/extend). Feeds: Tematy i
pytania „Dodaj do agendy", thread „Dodaj do agendy" (toggle), realization pin (toggle). Toggle-off or
deleting the agenda item clears the pin/added state on the source (no orphans, no stuck pins — this fixes
1.1 FIX.05 "unpin impossible"). Nothing auto-enters agenda.

### A5 · Thread statuses + context (1.2 CS-15)
Status chain: otwarty → „poruszony" (automatic when the thread's agenda topic is checked off at a
session) → user decides: domknij (→ archive „Domknięte wątki") or back to otwarty. The short context
description is AI-generated from the thread's source cards (existing summarization — `context_snippet`
shipped in MSV3.2 closeout; audit) and regenerates when a new source attaches; on failure return sources
without description. Active-count for the „5 z N aktywnych" counter (1.2 CS-17) must be derivable.

### A6 · Todos: repeats + completion log (1.1 FIX.01, CS-10)
Repeat options: none/daily/weekly/monthly. On its repeat day a completed task becomes open again and
queues FIFO by that day's date; each completion is a SEPARATE done entry (history with completion dates);
a missed period just stays open — no stacking. Restore from Done reopens. Main Homework (FE) shows the
3 oldest open items FIFO — expose whatever ordering/fields FE needs. Due dates are OUT of scope (author).

### A7 · Timeline weekly & monthly summaries — fix the 500 + auto-generate (1.1 CS-21) [data-analytics]
„Generate Now" currently throws an on-screen 500 and nothing generates. Fix end-to-end (find root cause;
never a raw 500 — error envelope with retry semantics). Auto-generate each weekly and monthly period at
period end (scheduler job — register per the rq_scheduler_setup pattern; idempotent). Content (AI): the
period's app data (entries, cards, scores, homework) → most important topics, changes, work done,
oriented to therapy progression, answering: is the approach working; better/worse/neutral. Keep the
manual „Generate Now" trigger. PL + ENG.

### A8 · Mood Trend backend (1.1 CS-11 + FIX.03) [data-analytics]
(a) Symptom score input: adding/updating scores must work again (audit the old Stats-era endpoints —
reported bug „nie można dodawać nowych punktacji"). (b) Narrative rewrite — CONTENT only (mechanics/
timing untouched): per-symptom narrative explains WHY it rises/falls grounded in the user's own app data,
qualitative wording („urosło mocno", „trochę zmalało"); it must NOT state point deltas between dates,
recite history, or suggest adding a note. PL + ENG. (c) Per-symptom `last_updated_at` for the FE relative
date. (d) AI Summary of all symptom change: must actually generate and render after new data (reported
bug: stale „Nie dodałeś od kilku dni notatki"), ≤4–5 lines, NO bullets.

### A9 · Goals narrative ad-hoc refresh (1.2 CS-20) [data-analytics]
Manual-refresh endpoint using the same pipeline that builds the goals narrative today. Failure → keep
previous narrative, return an error FE can toast. Do not touch scheduled/automatic generation.

### A10 · Notification deep-link payloads (1.1 CS-06)
Enumerate every live notification type from the codebase (post-Cadence-v3: DAILY_CHECK_IN,
REFLECTION_INVITATION, SESSION_MORNING_OF, re-engagement, broadcast …). Ensure each push `data` payload
carries enough routing info (type + entity ids) for the FE to deep-link to the exact input/output card.
Document the full type → payload table in the contract file (Phase F implements FE routing from it).
Do NOT touch scheduling/content.

### A11 · Therapy Relationship + weekly check-in state (1.2 CS-24; 1.1 FIX.04)
Scoring/color logic already works — only expose stored values: each check-in entry's rating/color and
the latest check-in's rating for the module icon. Expose weekly-check-in completion state so Main can
dismiss the prompt until the next weekly cycle after a note is added (audit why it currently doesn't).

### A12 · Session schedule fields (1.1 CS-09 support)
Audit models for: next session date/time, cadence, „with whom" — must be the SAME fields settings write.
Expose prep-done / debrief-done markers per session cycle and whatever the Main state machine needs
(states: no-therapy-set → prep CTA → session happened (from start time) → debrief CTA → between-sessions
→ next per cadence). Fix the BE part of the embedded bug if server-side (after debrief the module never
switched to between-sessions and the next session stopped displaying despite weekly cadence).

### A13 · iOS voice upload — backend-side audit (1.1 CS-02, support for PHASE B)
PHASE B (FE) owns the fix, but audit the upload/transcription endpoints for anything that would reject
iOS uploads across ALL voice features (content-type validation, size==0 handling, session state).
Report findings in STATUS.md for PHASE B.

## Definition of done (Phase A)
- All tasks implemented with tests (or explicitly reported PARTIAL in STATUS.md with reason).
- `python -m pytest app/tests/` — no new failures vs 21-failure baseline.
- App imports cleanly (`python -c "import app.main"` equivalent offline boot check); new DDL compiled
  against the postgresql dialect.
- `API_CONTRACT_Fix1.md`: zero TBD left; notification type table complete.
- `STATUS.md` report appended (commits, migrations, deviations, notes for FE phases).

## Code anchors (planner-provided; verify before use)

**Workspace (A1–A6)** — `app/models/workspace.py`: `AgendaItem` L196 (`status`+`archived_at`+`touched_at`),
`TodoItem` L243 (`status`+`done_at`+`archived_at`; `source_type/source_id`), `Thread` L286 + `ThreadSource` L320
(`closed_at`/`archived_at`), `GoalNarrative` L346, `WeeklyObservation` L379, `MoodTrendSummary` L409,
`TriageProposal` L437 (`card_type`+`card_id`). Status constants are String cols (correct pattern):
`AgendaItemStatus` open/touched/archived L95, `AgendaItemKind` topic/question L104, `TodoStatus` L126,
`ThreadStatus` open/touched/closed/archived/queued L135 (MAX_ACTIVE=5), `TriageCardType` L156,
`TriageProposalKind` topic/question/action_point/realization_ref L168, `AgendaSourceType` (incl. realization) L61.
Endpoints `app/api/v1/endpoints/workspace.py`: agenda archive L390 / **restore L404**; todos done L461 /
undone L480 / archive L493 / **restore L507** / `/todos/today` L445; threads add-to-agenda L566 / close L606 /
status L631 / archive L691 / **restore L705**; realizations GET L724 + **`/toggles` L736** (pin plumbing exists);
triage submit L847. CRUD `app/crud/workspace.py`; schemas `app/schemas/workspace.py`.

**Known gaps found in audit (your migration work)**: (1) `TodoItem` has NO recurrence fields → A6 needs
columns (e.g. `repeat_freq String(16)` + completion-log entries or equivalent). (2) `TriageProposalKind`
has NO thread/wątek kind → A2 must add it (1.2 CS-03 requires Wątek chips). (3) „Tematy i pytania" has no
dedicated storage — `AgendaItemKind` topic/question exists on agenda items, but 1.2 CS-05 requires a module
SEPARATE from Agenda that feeds it on demand → design storage (new table or a container/status dimension)
and document in the contract.

**A7 summaries** — weekly: `app/api/v1/endpoints/weekly_summaries.py` POST `/generate` L137 (**synchronous
AI call; the 500 originates in the try at L211–236** → `openai_service.generate_weekly_therapy_summary` L213),
`/latest` L125, `/{id}/retry` L332; task `app/tasks/weekly_therapy_summary.py`. Monthly:
`app/api/v1/endpoints/monthly_audits.py` POST `/generate` L220, retry L466; task
`app/tasks/monthly_therapy_audit.py`. Scheduler registration pattern: `rq_scheduler_setup.py` (boot-critical
— wired from lifespan in `app/main.py`; keep idempotent).

**A8 symptoms** — `app/api/v1/endpoints/symptoms.py`: create L367, POST `/{id}/score` ~L443 (enqueues
`regenerate_goal_narratives` L479), `/trend` L185, narrative regen `_refresh_one_description` L131 →
`SYMPTOM_DESCRIPTION_PROMPT` in `app/core/config.py` (model GPT_MODEL_41_MINI), refresh POST L206.
Models `app/models/models.py`: `UserSymptom` L884 (`ai_description`, `ai_description_generated_at`),
`SymptomScore` (1–10) L928. Mood-trend AI summary: `app/tasks/mood_trend.py` → `MoodTrendSummary`.

**A9 goals** — refresh endpoint ALREADY EXISTS: `app/api/v1/endpoints/goals.py` POST `/{id}/refresh` L451,
narratives archive GET L486; task `app/tasks/goal_narrative.py` `regenerate_goal_narratives` L34; model
`UserGoal` `models.py:1201`. → A9 is mostly audit + failure-semantics verification + contract documentation.

**A10 notifications** — `app/services/notification_orchestrator.py` candidate `payload` + `deep_link_route`
L224–225, sent L965; `app/services/notification_service.py` sends `data={"route":…,"type":…}` (L307, L659,
L742); `MomentTypeEnum` (13 values) `app/models/notification_moment.py` L41; generators
`app/services/moments/*.py`. FE resolver expects `route` (or legacy `deep_link_route`) —
`lib/utils/notification_route_resolver.dart` in the FE repo (read-only for you).

**A11 therapy relationship** — `TherapyHealthCheck` `models.py:1350`: scores 1–5,
**`relationship_state` = "green"/"amber"/"red"/"safety_escalation"** L1377 (+`state_label` L1378,
`mood_score` L1398); `HealthCheckDismissal` L1412; endpoint `app/api/v1/endpoints/health_check.py`;
generator `app/services/moments/therapy_relationship_checkin_generator.py`. (Spec says red/yellow/green —
map yellow=amber; document safety_escalation handling in the contract.)

**A12 session schedule** — `UserPreferences` `models.py:198`: **`therapy_schedule`** JSON
`[{"day_of_week","time"}]` L207, **`next_session_date`** L210. Prep/debrief: `SessionPrepCard` L682,
`SessionDebrief` L623 (`session_date`, `linked_prep_card_id`); endpoints `prep_cards.py`, `debriefs.py`,
`between_sessions.py`, `therapy_tracking.py`; tasks `prep_card_auto_generate.py`, `weekly_observations.py`.

**A13 audio** — `app/api/v1/endpoints/audio_v2.py` POST `/transcribe` L121 (multipart), `/realtime-session`
L204, GET `/transcription-session` L239; chunked upload `app/api/v1/endpoints/session_recordings.py`
initiate L477 / chunk L544 / complete L746; `UploadSession` `models.py:1669`, `UploadChunk` L1720.
