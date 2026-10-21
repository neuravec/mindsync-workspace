---
name: offline-verification
description: Recipes for verifying Alembic migrations and `import app.main` offline on this Windows dev box, without a real Postgres/Redis
metadata:
  type: reference
---

## Offline Alembic Verification Recipe (Windows, no local Postgres)

**Update 2026-10-13**: default `python` (C:\Python314) now LACKS `cryptography` and alembic env deps; boot check, `alembic heads` CLI and pytest all worked with `/c/Users/mikol/AppData/Local/Programs/Python/Python312/python.exe`. Use Python312 explicitly. Also set `DATABASE_URL` for the boot script. Pre-existing on origin/main 7e281ff: `test_reflect_summary.py::...roundtrip_on_sqlite` fails (SQLite syntax error in reflect_summary_cards DDL); test_consent.py has a timestamp-order flake (different test each run).

**Update 2026-08-10**: re-verified and this Python-312-workaround appears STALE — the default `python` (3.14, `C:\Python314`) now has a real importable `alembic` at `AppData\Roaming\Python\Python314\site-packages\alembic`, and `python -m alembic heads` / `python -m pytest` both worked fine directly, no Python312 needed. Environment may have been updated since this note was written. Check `python -c "import alembic; print(alembic.__file__)"` first before routing around it.

This machine's default `python` (3.14, `C:\Python314`) does NOT have `alembic` installed as an importable package — `import alembic` silently resolves to the LOCAL `alembic/` versions directory as a namespace package and `from alembic import op` fails.

Use `/c/Users/mikol/AppData/Local/Programs/Python/Python312/python.exe` instead — has the real `alembic` + `pytest` installed (matches requirements.txt). The `alembic` CLI shim on PATH also resolves to this same install (`alembic heads` works standalone).

To verify a new migration compiles+behaves correctly for BOTH dialects without a real DB:
- Load the module via `importlib.util.spec_from_file_location`.
- Use `alembic.migration.MigrationContext.configure(bind=<sqlite engine>)` + `Operations.context(ctx)` to actually run `upgrade()`/`downgrade()` against a real in-memory SQLite (proves the dialect-skip branch is safe).
- Separately use `MigrationContext.configure(dialect_name="postgresql", opts={"as_sql": True, "output_buffer": io.StringIO()})` to render the DDL as text WITHOUT a live connection — this proves `op.get_context().autocommit_block()` correctly emits `COMMIT;`/`BEGIN;` around `ADD VALUE` statements and that target labels appear in the rendered SQL.

`python -m alembic heads` fails ("No module named alembic.__main__") even when the package IS importable — always invoke the `alembic` console-script entry point directly, not `python -m alembic`.

## Offline `import app.main` Recipe (Windows dev sandbox, no real Redis/full deps)

- Mock `rq`, `rq.*` submodules, and `rq_scheduler` in `sys.modules` before importing (real packages fail with `ValueError: cannot find context for 'fork'` on Windows) — mirrors the existing test-suite `_ensure_rq_importable()` pattern.
- Set env vars before import: `DB_URL=sqlite:///:memory:`, `MESSAGE_ENCRYPTION_KEY=<any Fernet.generate_key()>`, `REDISGREEN_URL=redis://localhost:6379/0` (dotenv is NOT auto-loaded — config.py has `load_dotenv()` commented out).
- This sandbox is also missing a few real third-party packages regardless of any code change: `tiktoken`, `fpdf`, `assemblyai` — stub only these 3 with `MagicMock()` in `sys.modules`. Do NOT blanket-stub `google`/`google.auth` — those ARE installed for real (needed by firebase_admin) and a generic MagicMock stub breaks firebase_admin's own internal import of `google.auth.credentials`.
- Expect one harmless failure inside `Base.metadata.create_all(bind=engine)` at import time: SQLite can't compile a Postgres `ARRAY` column (`rag_documents.embedding`) — this is caught by main.py's own try/except (by design, documented in-file) and does not block boot. `IMPORT APP.MAIN: OK` printing after that traceback is the correct, expected outcome.
