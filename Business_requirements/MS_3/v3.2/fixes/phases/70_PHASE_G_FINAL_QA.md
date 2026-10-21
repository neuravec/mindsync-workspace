# PHASE G — Final QA + deploy checklist (MSV3.2 Fix.1) — both repos, read/test only

## SYSTEM INSTRUCTIONS (read fully before any tool call)

You are a fresh Claude Code session acting as the QA/integration lead closing the MSV3.2 Fix.1 batch.
Project rules from `CLAUDE.md`. Delegate to `qa-testing` (test runs / missing tests) and, for the
pre-deploy security pass on new/changed endpoints, `security-guardian`. You fix NOTHING yourself outside
test files — regressions go back as precise bug reports appended to `STATUS.md` (the operator decides
whether to rerun a phase session).

- Repos: backend `MindSync/` (branch main), frontend `mindsync-frontend/` (branch dev). **NEVER push;
  NEVER touch prod.** Commit only test files (qa-testing ownership) if you add coverage.
- REQUIRES: Phases A–F all report DONE/PARTIAL in `STATUS.md`. Read `STATUS.md` +
  `API_CONTRACT_Fix1.md` + `00_MASTER_PLAN.md` first.

## Checklist

1. **Test suites**
   - BE: `python -m pytest app/tests/` — compare against the 21-failure baseline; list any new failures
     with tracebacks.
   - FE: `flutter analyze` (no new errors) + `flutter test` — compare against the 30-failure baseline.
   - Offline Postgres safety: import the app (`python -c "import app.main"`-style) and compile any new
     DDL with the postgresql dialect; verify the alembic chain still has a SINGLE head and every new
     migration is idempotent.
2. **Done-when audit** — walk EVERY item of both specs (`SPEC_Fix1.1_full_text.txt`,
   `SPEC_Fix1.2_full_text.txt`) against its "Done when" clause by code inspection; mark
   pass / fail / needs-device-QA per item in a table appended to STATUS.md.
3. **Cross-layer contract check** — for each contract section (§1–§10) verify FE call sites match the BE
   implementation (paths, fields, error envelopes). A BE error must never be interpreted by the client as
   "new user / needs onboarding".
4. **Grep gates** (from the specs): no live `capture_recordingTranscriptHint` references; no „Odkliknij";
   no user-facing section-name „Terapia/Therapy" for the Workspace tab (but „Therapy Relationship" etc.
   untouched); no „Nie dodałeś od kilku dni notatki" / add-an-entry empty-state strings; no „+ + dodaj cel";
   no Coral Pink circle in the voice error card; no due-date UI in Do zrobienia.
5. **Security pass** — `security-guardian` on new/changed endpoints (workspace topics, chip state, restore,
   summaries): auth + user scoping (horizontal privilege escalation), since they carry mental-health data.
6. **Manual device-QA list** — consolidate everything flagged across STATUS.md (at minimum: iOS voice
   recording end-to-end incl. weekly check-in — CS-02; Main order on a physical iPhone — CS-08/CS-10;
   Therapy Relationship bottom clipping small/large screens — CS-23; notification matrix type × cold/
   background — CS-06) into a numbered checklist for the operator.
7. **Deploy checklist for the operator** (write into STATUS.md, do not execute):
   - Verify whether the 3 MSV3.2 migrations are applied on prod (database-administrator recipe:
     `heroku run -a mindsync python < script.py`); list ALL unapplied migrations incl. any new from Phase A.
   - Backend: `git push` origin main + deploy to Heroku, **together with** `heroku run alembic upgrade
     head --app mindsync` (deploy ≠ migrate; no release phase).
   - Frontend: push dev → Codemagic → TestFlight/Play internal; remind that old app builds live for weeks
     (backend must stay additive/backward-compatible — flag any breaking response change found in step 3).
8. **STATUS.md final section** — overall GO / NO-GO with the list of blockers, if any.

## Definition of done (Phase G)
All 8 checklist points executed and written up in STATUS.md; no unexplained new test failures; the operator
has a single consolidated device-QA + deploy checklist.