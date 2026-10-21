---
name: project-ke-privacy-review-fixes-2026-10-18
description: KE (character KD v2) privacy review fixes, commit 0906e23 on feat/character-kd2-v3: switches default OFF, opt-in PROFILING mode, source_present EXISTS filter + cleanup purge, activation at first GET /ke/sheet, 90-day feedback retention
metadata:
  type: project
---

Commit `0906e23` on `feat/character-kd2-v3` (pushed to origin only, 2026-10-18). Builds on [[project-ke-character-kd2-be1-2026-10-18]].

Decisions that are not obvious from the code:
- `CHARACTER_KE_ENABLED` / `CHARACTER_KE_EXTRACTION_ENABLED` default False until the lawyer rules on M-5; `CHARACTER_KE_REQUIRE_PROFILING_OPT_IN` defaults True (asymmetric risk: forgetting to flip it only shows a lock screen; the opposite would profile without consent). Only integration-devops flips Heroku vars. `.env.example` (theirs) still lacks the KE vars.
- Moment erasure: no FK possible (six source tables), so `app.crud.ke.source_present(restorable_since)` is one correlated EXISTS per source kind. Reads use it without the window (soft-deleted = hidden at once); the purge uses the 24 h window so a restore brings moments back.
- Purge runs first in every job and needs no switch or consent; the sweep enqueues purge-only jobs even with extraction off.
- Migration `ke_a7c3e9f1b2d4` was edited in place (never on prod) and self-heals an earlier-draft `ke_user_state` via `LATE_COLUMNS`.

Gotchas:
- Seeded test moments now need a REAL source row (`ke_pipeline_support.add_source`), or the filter hides them; a seeded `todo_done` adds a therapist TodoItem, so "count all to-dos" assertions must filter `origin == "ai"`.
- Bash tool heredocs containing `'...' % (...)` Python failed with "unexpected EOF"; write patch scripts with the Write tool and run them.

**Why:** backend review found the defaults bypassed the team's own legal gate and entry deletion left derived moments (GDPR Art. 17).
**How to apply:** any new KE source kind needs a branch in `source_present` and `add_source`; any new prompt input built from feedback must respect `FEEDBACK_RETENTION_DAYS`.
