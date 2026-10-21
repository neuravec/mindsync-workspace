---
name: project-featureenum-b18-cost-audit-fix-2026-08-10
description: Task B18 — extended token_usage_log FeatureEnum (CLINICIAN + THREAD_CONTEXT/WEEKLY_OBS drift fix), handoff from the 2026-08-10 SYSTEM AI-cost audit
metadata:
  type: project
---

Task B18 (handoff from `analytics-reports/2026-08-10-system-ai-cost-audit.md`,
recommendations 4-5, owned by data-analytics's A13 audit) asked backend-api to:
1. Add a `CLINICIAN` FeatureEnum label and wrap `app/services/clinician_ai.py`'s
   6 `gpt_structured()` calls in `track_usage("CLINICIAN", ...)`.
2. Fix `THREAD_CONTEXT`/`WEEKLY_OBS` drift: both labels were already emitted
   by real `track_usage()` calls in `app/tasks/thread_context.py:79` and
   `app/tasks/weekly_observations.py:152`, but neither was ever added to
   `FeatureEnum` or a migration — `log_token_usage()`'s fire-and-forget
   `try/except` was silently swallowing every insert for these two labels.
   Not a SYSTEM misattribution — this AI spend was never recorded anywhere.

**Done:** `token_usage_log.feature` confirmed as a native Postgres enum
(`Enum(FeatureEnum)`, not String+constants) — so this needed a migration, not
just a Python-side enum change. Added all 3 labels to `FeatureEnum` in
`app/models/models.py` (24 -> 27 members) + migration `ii0j1k2l3m4n`
(down_revision=`hh9i0j1k2l3m`, the single head at the time — confirmed via
`alembic heads` CLI). Migration follows the more current `ff7182a3b4c5`
precedent (`op.get_context().autocommit_block()` wrapping `ALTER TYPE ...
ADD VALUE IF NOT EXISTS`), not the older `uu1v2w3x4y5z` HERO_INSIGHT
precedent which lacked the autocommit_block — **prefer autocommit_block for
any future enum-label-addition migration**, since `ADD VALUE` cannot run
inside a regular transaction on all supported Postgres versions and env.py
wraps every migration in an implicit transaction.

**Ownership note (flag for the lead):** `app/services/clinician_ai.py`'s own
file-header docstring says "Owned by: data-analytics", which contradicts
CLAUDE.md's File Ownership Map (`app/services/` is backend-api's except
`analytics.py`/`openai_service.py` — `clinician_ai.py` is neither). Treated
CLAUDE.md as authoritative (it says so explicitly) and edited the file per
the lead's task instruction, but the in-file comment is now stale/misleading
and should be corrected by whoever has authority to reconcile it (probably
just delete that line, or clarify "data-analytics designed the prompts/
contract, backend-api owns the file per CLAUDE.md").

**Offline verification recipe used (see [[offline_verification]]):** for a
new "ADD VALUE" enum migration, don't just eyeball the SQL string —
1. Load the migration module via `importlib.util.spec_from_file_location`,
   run `upgrade()`+`downgrade()` against a real in-memory SQLite engine via
   `MigrationContext.configure(bind=<engine>)` + `Operations.context(ctx)` —
   proves the dialect-skip guard doesn't error.
2. Render Postgres DDL as text with
   `MigrationContext.configure(dialect_name="postgresql", opts={"as_sql":
   True, "output_buffer": io.StringIO()})` (no live connection) — confirms
   `autocommit_block()` actually emits `COMMIT;`/`BEGIN;` framing around the
   `ADD VALUE` statements and all target labels appear in the rendered SQL.
3. `alembic heads` (default `python` on this box now has real alembic
   importable — Python312 workaround is stale, see [[offline_verification]])
   for the single-head sanity check, in addition to a manual down_revision
   graph parse.

**Test files added/touched (qa-testing normally owns `app/tests/`, but
backend-api writes its own tests per CLAUDE.md's Testing Enforcement
section — established precedent, see MEMORY.md pattern notes):**
- `app/tests/test_featureenum_hero_insight.py` — updated the hard-coded
  `code_emitted_labels` snapshot set and member-count assertion (24 -> 27).
  This is the exact test the audit's recommendation 5 flagged as stale
  (a hard-coded snapshot instead of a live grep) — I did NOT convert it to a
  live-grep-based test (out of B18's explicit scope), just fixed the
  snapshot. A future task could do the grep-based rewrite the audit
  suggested; flagging here so it isn't forgotten again.
- `app/tests/test_featureenum_b18_cost_audit_fix.py` — new file, mirrors the
  HERO_INSIGHT test shape: enum membership, migration source/idempotency/
  autocommit_block checks, clinician_ai.py wrap-coverage checks (regex scan
  ensuring every `gpt_structured(` call site is preceded by a `with
  track_usage(` within 3 lines — guards against a future call site being
  added without the wrapper), and log_token_usage roundtrip for all 3 new
  labels including a fire-and-forget-on-DB-error case.

**Test results:** `test_clinician_ai.py` (pre-existing, 46 tests) all pass
unchanged — the track_usage wrap didn't touch any mocked call signature.
New/updated featureenum tests: 54 passed. Concurrent agents were mid-edit on
`notification_orchestrator.py`/moments generators in the same working tree
at commit time — see [[feedback_concurrent_session_git_hygiene]] — staged
and committed only my own 5 files first (`40c10d2`): `app/models/models.py`,
`app/services/clinician_ai.py`, both featureenum test files, and the new
migration.

**Second pass — full-suite regression caught by running it anyway:** ran
`python -m pytest app/tests/ -q` in the background afterward (took ~9-11
min) and got **22 failed / 5003 passed** — 2 more than the known ~20
baseline. Both extras were the exact "chain-tip test" pattern from
[[project_msv32_fix1_gfix_2026_07_17]]-adjacent memory notes:
`test_users_activated_at_migration.py` and `test_workspace_fix4_migration.py`
each hard-coded "`gg8h9i0j1k2l` has no known successor" — already false
before I even started (B12's `hh9i0j1k2l3m` extended it earlier the same
day) and nobody had fixed it. Renamed both to
`test_gg8h9i0j1k2l_has_exactly_one_known_successor` asserting the real
child, following the exact precedent already documented in
`test_workspace_fix4_migration.py`'s own docstring history (the file
literally instructs the next author to do this). Added the matching new-tip
pair (`hh9i0j1k2l3m` -> `ii0j1k2l3m4n` has exactly one successor;
`ii0j1k2l3m4n` currently has none) to my own `test_featureenum_b18_cost_audit_fix.py`
so the next migration author has a fresh instance of the same instruction.
Re-ran full suite: **20 failed / 5007 passed** — back to exact known
baseline, none of the 20 introduced by this task. Committed as `69cc599`.

**Lesson reinforced:** always run the FULL suite after a migration lands,
not just the targeted files — targeted tests can't catch a stale chain-tip
assertion elsewhere in the tree, and this exact failure mode has now
recurred twice (once left broken by a prior same-day task, B12, before I
even touched it). Committed locally, not pushed (both `40c10d2` and
`69cc599`).
