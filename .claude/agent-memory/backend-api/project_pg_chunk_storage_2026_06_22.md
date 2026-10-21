---
name: pg-chunk-storage-2026-06-22
description: GCS→Postgres re-implementation for chunked audio upload (503 fix); upload_chunks table; migration vv2w3x4y5z0a; 104 tests green
metadata:
  type: project
---

GCS→Postgres re-implementation of chunked session-recording upload, 2026-06-22.

**Why:** GCS/Firebase Storage requires a paid plan the operator hasn't enabled. All chunk
uploads were 503ing at `upload_chunk`. HTTP API contract unchanged — Flutter client needs zero changes.

**What changed (backend only, not committed/pushed):**
- `app/models/models.py`: added `UploadChunk` model (String/BigInteger/Text/DateTime — no Enum(PyEnum))
- `alembic/versions/vv2w3x4y5z0a_add_upload_chunks_table.py`: idempotent migration; `down_revision=uu1v2w3x4y5z`
- `app/api/v1/endpoints/session_recordings.py`:
  - `_encode_chunk` / `_decode_chunk`: base64 + Fernet round-trip for binary chunk data
  - `_store_chunk_to_pg`: inserts UploadChunk row, idempotent via IntegrityError catch
  - `_assemble_chunks_from_pg`: queries ORDER BY byte_offset, streams to NamedTemporaryFile (no RAM buffer)
  - `_delete_upload_session_chunks`: DELETE WHERE upload_session_id=... idempotent
  - Removed `_require_gcs_or_503()` from initiate/chunk/complete paths
  - Old GCS helpers kept as dead code (renamed `[CHUNKED/GCS]` prefix in logs)
- `app/tasks/session_recording.py`: worker assembles from PG when `/assembled.audio` in storage_key
- `app/tasks/recording_recovery.py`: cleanup calls `_delete_upload_session_chunks` instead of GCS delete
- `app/tests/test_chunked_upload.py`: all GCS patches removed, 87 tests pass
- `app/tests/test_server_auth_completion.py`: GCS patches removed, 17 tests pass
- `app/tests/test_pg_chunk_storage.py`: 17 new unit tests for storage helpers

**Encryption decision:** chunk `data` stored Fernet-encrypted as base64 Text.
Binary → `base64.b64encode(bytes).decode("ascii")` → `encode_service.encode(str)` → Text column.
Round-trip: `encode_service.decode(text)` → `base64.b64decode(str)` → bytes.
Chunks deleted immediately after transcription. Flagged for security review.

**Deploy + migrate sequence (operator):**
1. `git push heroku main` (deploy new code)
2. `heroku run alembic upgrade head` (creates upload_chunks table)
3. Verify: `heroku logs --tail` for clean boot

**How to apply:** migration `vv2w3x4y5z0a` is idempotent (has_table guard). Safe to run twice.
