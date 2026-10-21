---
name: project_charsheet_consent_lock_2026_10_14
description: Character sheet default-on + locked 200 on PROFILING withdrawal + POST /character_sheet/consent re-grant (commit 0853984, feat/charsheet-consent, not pushed)
metadata:
  type: project
---

Character sheet v2 now defaults ON (kill switch kept); PROFILING withdrawn -> 200 `{"locked":true,"lock_reason":"profiling_consent_required"}`, nothing computed; new POST `/gamification/character_sheet/consent` writes a PROFILING grant via `app.crud.consent` with source `character_sheet_unlock`.

**Why:** operator decision 2026-10-14, TestFlight must show the sheet as designed; 403 gave the client no way to offer an unlock.

**How to apply:**
- Lock check uses `consent_crud.is_consent_withdrawn` (raises -> 500), NOT the fail-closed `is_profiling_consent_withdrawn`, so a DB blip never shows a false "consent required" prompt.
- Union response_model of two Pydantic models with `locked: Literal[False]` / `Literal[True]` serialises correctly in FastAPI 0.135 (smart-mode exact-instance match); OpenAPI shows anyOf.
- Prod Heroku config value of CHARACTER_SHEET_V2_ENABLED was NOT checked; if set to false there, the default change does nothing.
- Re-grant re-enables Orca memory writes too (same PROFILING type); `memory_forgotten_at` keeps old turns unmined.
