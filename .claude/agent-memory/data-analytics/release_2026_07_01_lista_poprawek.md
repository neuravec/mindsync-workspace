---
name: release-2026-07-01-lista-poprawek
description: Backend prompt/generation changes for the TestFlight-first "Lista poprawek 01-07-2026" release (RC-01 recording summary, FX-10 health-check reflection, FX-03 symptom correlation) — additive-only, coordinated around another session's concurrent uncommitted work on forbidden files.
metadata:
  type: project
---

Phase 1 of a two-phase release: shared prod backend serves BOTH old App Store
clients and new TestFlight clients simultaneously. Rule: additive-only,
generation-time content changes only, no schema/model/migration changes.
Files touched: `app/services/openai_service.py`, `app/core/config.py`
(prompt-text-only, lead-sanctioned single line). Forbidden files (another
session's uncommitted work): `session_recordings.py`, `session_recording.py`,
`users.py`, `crud.py` + their tests — read-only for this task.

## Critical trap: `encode()` crashes on `None`

`app/services/encode_service.py::encode(plaintext)` does
`plaintext.encode("utf-8")` — **crashes with AttributeError on `None`**, no
guard. `app/tasks/session_recording.py::_save_summary_sections` calls
`recording.emotional_arc = encode(summary.emotional_arc)` **unconditionally**
(no `if summary.emotional_arc:` guard) — unlike `audio_quality_warning`,
which IS guarded (`if summary.audio_quality_warning: ...`).

Lesson: before making any Pydantic structured-output field `Optional[...] =
None` to "soft-deprecate" it, grep every consumer for whether the field
reaches `encode()`/similar raw-string sinks unconditionally. If yes, do NOT
use `Optional[str] = None` — keep the field's Python type non-nullable
(`str` / `List[str]`) with a safe empty default (`""` / `default_factory=list`)
and rely on the prompt + Field `description` to steer the model toward
emptiness. `List[str]` is safe to make `None`-tolerant only if the consumer
wraps it in something null-tolerant first (e.g. `json.dumps(None)` → `"null"`
is a valid string, so `unresolved_topics` *could* have gone `Optional`, but I
kept it `default_factory=list` for consistency with sibling fields
`therapist_observations`/`patient_insights` in the same model).

## OpenAI structured outputs (`.beta.chat.completions.parse`) — nullability semantics

Every property is forced into the JSON schema's `"required"` array in strict
mode **regardless of Python `default`/`default_factory`** — a default does
NOT let the model omit the field. The ONLY way to let the model legitimately
return "nothing" for a field is `Optional[X] = None` (adds `null` to the
allowed JSON types). A non-Optional field with a Python default just means:
the model must still emit *some* value; you steer it toward the default via
prompt + Field description, but compliance is a prompt-engineering
guarantee, not a schema guarantee. See `RecordingSummaryResult.emotional_arc`
(deprecated, kept `str` type, default `""`, description says "always return
the empty string") for the working pattern.

## Windows dev-box Python version gotcha

Two Python interpreters on PATH: `python` resolves to **3.14** (missing
`tiktoken` → `app/api/v1/endpoints/conversations.py` import fails) but
**3.12** at `C:\Users\mikol\AppData\Local\Programs\Python\Python312\python.exe`
has all project deps installed (this matches CLAUDE.md's stated
"Python 3.12.2"). **Always run pytest / import-checks with the 3.12
interpreter explicitly**, not bare `python`.

## Boot-critical `import app.main` check outside pytest

`app/tests/conftest.py` is pure env-var bootstrap (65 lines, no fixtures) —
safe to `sys.path.insert` its directory and `import conftest` directly from
an ad-hoc script to replicate the full test env for a standalone
`python -c "import app.main"`-style check. Still need two extra workarounds
beyond conftest, since conftest is designed for pytest collection (which
mocks rq per-test-file), not a single top-level `import app.main`:
1. Mock the full `rq`/`rq.*` module chain into `sys.modules` (Windows can't
   `get_context('fork')`) — same list as the `_ensure_rq_importable()`
   helper duplicated across test files.
2. Monkeypatch `firebase_admin.credentials.Certificate` and
   `firebase_admin.initialize_app` before importing `app.main`, since
   `initialize_firebase()` runs at module level in `main.py` and the fake
   `FIREBASE_CREDENTIALS` env value (`{"type":"service_account"}`) is not a
   real file path.
With both in place, `import app.main` reaching `IMPORT_OK` proves the ENTIRE
router tree (`app/api/v1/api.py` → all endpoint modules → all owned
services/schemas) imports cleanly — a much stronger signal than importing
just the one file you changed.

## Pre-existing test baseline (2026-07-02)

Full suite: **4032 passed, 56 failed** (`python -m pytest app/tests/ -q`,
~5m48s on Python 3.12). All 56 failures are pre-existing and unrelated to
prompt/content changes — they cluster in notification scheduling
(`test_health_check.py`/`test_health_check_phase2.py`: missing
`_should_notify_today` import, FCM-not-called assertions),
`test_consent.py`, `test_custom_therapy_sessions.py`,
`test_symptom_suggestions.py` (schema `model_config` missing
`from_attributes`), `test_voice_fixes.py` (RAG injection), `test_walkthrough.py`,
etc. — none reference `RecordingSummaryResult`, `HEALTH_CHECK_PROMPT` text,
or `SYMPTOM_DESCRIPTION_PROMPT` content. Cross-check by grepping the failing
test body for the changed symbol before assuming causation. See also
[[reference_pre_existing_test_baseline_2026_06_01]] in the orchestrator's
memory — this is the same phenomenon, drifted forward (2895→4032 passed).

## Result of this task (for continuity)

- `generate_recording_summary()` gained an **additive, unwired** optional
  param `previous_session_context: str | None = None`. No caller populates
  it yet — wiring requires fetching the prior recording's overview inside
  `app/tasks/session_recording.py::_gather_context`, which is a forbidden
  file for this task. Follow-up: add `previous_session_context` fetch there
  and pass it through both call sites (~line 376 and ~line 658).
- `emotional_arc`/`unresolved_topics` on `RecordingSummaryResult` are now
  prompt-deprecated (model instructed to always emit `""`/`[]`) but the
  Python types stayed non-nullable for the `encode()` safety reason above.
- New test files (this session's addition, not pre-existing):
  `test_recording_summary_prompt.py`, `test_health_check_prompt.py`,
  `test_symptom_description_prompt.py` — 45 tests, all pass.
