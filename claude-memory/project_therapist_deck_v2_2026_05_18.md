---
name: therapist-deck-v2-2026-05-18
description: "Therapist Deck V2 — full-stack clinician portal expansion (Pulpit, briefs, goals, session notes, voice notes, golden thread) shipped 2026-05-18"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8d133dce-3ae6-40ba-947f-e58ad7366df2
---

# Therapist Deck V2 — shipped 2026-05-18

Major full-stack expansion of the MindSync clinician portal, built from a Claude Design
handoff (analysis vs competitor Mentalyc → `therapist-deck/docs/FUNKCJE_DO_WDROZENIA.md`).

**Why:** competitive push — match Mentalyc's feature set but on MindSync's unique
between-session patient data (its moat: Mentalyc has no patient app).

**What shipped (7 workstreams, 6 agents):**
- Backend `MindSync/app/`: `models/clinician_v2.py` (TreatmentGoal, ClinicianSessionNote,
  ClinicianVoiceNote, ClinicianBriefCache, GoldenThreadLink), `crud/clinician_v2.py`,
  `endpoints/clinician_v2.py` (router + me_router), `schemas/clinician_v2.py`,
  `services/clinician_ai.py` (5 AI fns), `tasks/clinician_voice_notes.py` (AssemblyAI RQ
  pipeline). Migration `kk1l2m3n4o5p` off `jj0k1l2m3n4o`. 229 clinician tests pass.
- Portal `therapist-deck/`: Pulpit (triage), 6-tab patient profile (Overview/Brief/
  Progress+Golden Thread/Goals/Session Notes/Private voice notes), Sessions calendar,
  Engagement signal. BFF wiring in `src/lib/` + `actions-v2.ts`. 10 routes, build clean.
- Flutter patient app: Treatment Goals (read-only consumption of `GET /api/v1/me/goals`).
- Contract: `therapist-deck/_design-reference/API_CONTRACT_V2.md`; design handoff in
  `_design-reference/v2-handoff/`.

**Audits done & fixed:** 2 Critical (CRIT-001 `/me/goals` cross-clinician leak; CRIT-002
GDPR consent-revocation cascade — `purge_v2_data_for_consent`), 4 High (audio upload
validation, rate limits, voice-note error-log leak, AI prompt-injection hardening),
mediums. All fixed with regression tests.

**How to apply / known follow-ups:**
- NOT deployed — needs Heroku config + `alembic upgrade head` (operator-gated, like the
  original portal — see [[project_clinician_portal_integration_2026_05_15]]).
- Voice notes reuse `app/services/assemblyai_service.py`. `next.config.ts` now allows
  `microphone=(self)`.
- Loose end: `PatientExt.progress.snapshots` not yet populated in the BFF data layer —
  Progress snapshot cards render an empty state until wired.
- Pre-existing unrelated test failures noted by QA (57 backend, 35 Flutter) — NOT caused
  by this work; left for a separate cleanup decision.
