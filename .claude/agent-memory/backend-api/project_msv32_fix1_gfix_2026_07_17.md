---
name: msv32-fix1-gfix-2026-07-17
description: MSV3.2 Fix.1 G-fix — restored add-to-agenda backward compat for shipped builds, moved toggle to new /agenda-pin route; FE still needs to switch which URL it calls
metadata:
  type: project
---

Commit `646bda1` on MindSync main (2026-07-17, local only, NOT pushed — branch
was already 6 ahead of origin before this, now 7 ahead).

**What happened**: Phase G found that `API_CONTRACT_Fix1_A1.md` §3c wrongly claimed
`PUT /workspace/threads/{id}/add-to-agenda` had "no live consumer" when A1 changed its
response shape from `AgendaItemResponse` to `PinToggleResponse` (toggle semantics).
In reality, already-shipped production app builds call exactly this route and parse
the response with a strict `AgendaItemModel.fromJson` requiring non-nullable
`text`/`source_type`/`status`/`created_at` — the toggle response would throw for them.
Old builds live for weeks (per CLAUDE.md's own change-safety rationale), so this was a
live backward-compatibility bug waiting to ship.

**Fix**: old route restored to its pre-Fix.1 ADD-only, idempotent `AgendaItemResponse`
contract (never toggles off; ws_crud.get_or_create_agenda_pin, new helper). Toggle
semantics moved to a NEW route, `PUT /workspace/threads/{id}/agenda-pin`, mirroring
the existing `PUT /workspace/realizations/{id}/agenda-pin` pattern.

**Why this matters going forward**: [[msv32-fix1-phase-plan]] — the concurrent, NOT-YET-shipped
Fix.1 frontend work (Phase C/D/E, local/uncommitted-to-TestFlight per project memory)
had ALREADY been built against the (wrong) toggle contract on the OLD url:
`workspace_manager.dart`'s `toggleThreadAgendaPin()` calls
`Endpoints.workspaceThreadAddToAgenda(id)` (the `/add-to-agenda` path) and parses
`PinToggleResponse`. After this backend fix, that FE code will get an
`AgendaItemResponse` shape instead and break (or at best silently misparse `pinned`).

**How to apply**: next time flutter-mobile touches thread agenda-pin, they must:
1. Add a new endpoint constant mirroring `workspaceRealizationAgendaPin`, e.g.
   `Endpoints.workspaceThreadAgendaPin(id) => '/api/v1/workspace/threads/$id/agenda-pin'`.
2. Point `toggleThreadAgendaPin()` in `workspace_manager.dart` at the new constant
   instead of `workspaceThreadAddToAgenda`.
3. `workspaceThreadAddToAgenda`/`addTopicQuestionToAgenda`-style plain-add semantics
   are untouched — no FE change needed for the topic-questions add-to-agenda flow.
This was flagged to the lead as part of the G-fix task; not yet actioned by
flutter-mobile as of 2026-07-17 (their local changes predate this backend fix).

Full before/after contract for both routes is in
`Business_requirements/MS_3/v3.2/fixes/phases/API_CONTRACT_Fix1_A1.md` §3c (updated
in this same task — that file lives OUTSIDE any git repo, no commit needed/possible
for it).
