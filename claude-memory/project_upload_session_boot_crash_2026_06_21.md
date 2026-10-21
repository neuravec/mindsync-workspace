---
name: project-upload-session-boot-crash-2026-06-21
description: Prod H10 boot crash-loop from UploadSession.status Enum/String mismatch + create_all-at-boot; fixed & deployed v505; two follow-ups open
metadata: 
  node_type: memory
  type: project
  originSessionId: 085a1901-caa8-44b4-a365-dcb57a362f4e
---

2026-06-21: Prod backend (Heroku app `mindsync`, Azure Postgres) crash-looped (H10, 503 on EVERY request, ~38 min) after deploy of `dcc779d` (release v501). Symptom user saw: logged out → re-login → app dumped existing user into onboarding (name/gender/age) → infinite spinner after "next".

Root cause: `UploadSession.status` in `app/models/models.py` was `Column(Enum(UploadSessionStatusEnum))` — a native PG enum whose labels are the member NAMES (uppercase `IN_PROGRESS`) but with `server_default="in_progress"` (lowercase value) → self-inconsistent. `app/main.py` runs `Base.metadata.create_all(bind=engine)` at IMPORT on every web boot, which emitted a failing `CREATE TABLE upload_sessions (... status uploadsessionstatusenum DEFAULT 'in_progress')` → boot crash → crash-loop. Tests passed only because they run on SQLite (tolerates it; Postgres is fatal). Migration `tt0u1v2w3x4y` was CORRECT (used `sa.String(32)`). Prod self-recovered at 12:04 local when operator ran `alembic upgrade head` — that created the table as String, after which `create_all` skips the existing table (checkfirst=True).

Fix (commit `523946c` on backend `main`, deployed **v505**, boot verified clean — single boot, no enum error, guard never fired):
- models.py: `UploadSession.status` → `String(32)` matching the migration; Python `default` uses `.value`.
- main.py: wrapped `create_all()` in try/except (log + continue) so a future model/DB drift degrades ONE feature instead of crash-looping the whole web dyno. Alembic is the real schema manager.
- session_recordings.py:386: guarded `.status.value` (DB now returns plain str). Note Py3.14: `str(StrEnumMember)` returns the qualified name, not the value — use `.value`.
- New `test_upload_session_model_regression.py` (15 tests): asserts column is String not Enum + offline postgresql-dialect DDL compile proving no native enum emitted. 126 tests green (independently re-run).

Deploy topology learned: **GitHub→Heroku auto-deploy IS configured** — `git push origin main` auto-builds. Explicit `git push heroku main` then causes a duplicate build (harmless). In future: just push origin. No `heroku` git remote pre-existed in the clone; Heroku git = git.heroku.com/mindsync.git.

FOLLOW-UPS — BOTH SHIPPED 2026-06-21:
1. ✅ Worker enum drift `featureenum: "HERO_INSIGHT"` (broke hourly hero_insight job; same class as [[project_postgres_enum_drift]]). Fix: model `FeatureEnum` += HERO_INSIGHT + idempotent migration `uu1v2w3x4y5z` (`ALTER TYPE featureenum ADD VALUE IF NOT EXISTS`). Commit `3222d48` → backend main → **deployed v506**; migration RUN on Heroku; prod featureenum now has 24 labels incl. HERO_INSIGHT (verified via `enum_range`). Added a drift-guard test (every track_usage label must be a FeatureEnum member). Backend main is now 2 commits past origin's old state (523946c v505 + 3222d48 v506).
2. ✅ Frontend 503→onboarding eviction. Fix in `lib/screens/splash/splash_screen.dart`: only a DEFINITIVE HTTP 404 → sign-out/welcome; any other error (5xx/timeout/connectivity) → error+retry overlay, never onboarding. Removed silent `catch→therapyOnboarding` (the infinite-spinner path). +2 l10n keys (app_couldNotConnectRetry, common_retry) ×7 locales + regen. 14 tests, analyze 0 err. Commit rebased onto origin/dev as `7043175` → **pushed dev → Codemagic→TestFlight building**.

Heroku ops gotcha: `heroku run` is BROKEN from Git Bash here (`'C:\Program' is not recognized` — space-in-path). Use the **PowerShell** tool with the `--%` stop-parsing token + a `--` separator before the command, e.g. `heroku --% run:detached -a mindsync -- python -c "...single-quotes inside..."`. `heroku logs`/`curl` work fine from Bash.

Recon discipline now codified in repo `CLAUDE.md` → "Change Safety & Impact Recon (MANDATORY)" (model↔migration↔prod-DB consistency, create_all-at-boot is boot-critical, SQLite≠Postgres, deploy≠migrate). See [[project_general_fixes_2026_06_20]] (the dcc779d batch this regression rode in on).
