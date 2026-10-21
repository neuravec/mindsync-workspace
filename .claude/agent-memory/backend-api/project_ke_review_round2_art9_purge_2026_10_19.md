---
name: ke-review-round2-art9-purge-2026-10-19
description: KE security review round 2 on integration/redesign-v3 (40be9b0..1e69b05): ART9 withdrawal purge of therapy-derived ke_* rows, person-less ideas_paused, RQ job description, PROFILING cleanup retry, no-store, daily call cap
metadata:
  type: project
---

Round 2 of KE review fixes landed on integration/redesign-v3 on 2026-10-19 (12 commits 40be9b0..1c6bf3c on f1c14dd), pushed to origin only (f1c14dd..1c6bf3c). Full suite then: 12314 passed, 22 failed, all base or known flaky.

- ART9 withdrawal: `cleanup.purge_art9_derived` hard-deletes moments from `crud.ke.art9_source()` (session, after_therapy, todo_done of a to-do with origin "therapist"), therapy-origin tools, homework ideas, then `_delete_orphans`; sessions count -> 0, compose cache dropped. Called best effort from DELETE /users/consent/art9_health, from every KE job, and via `ensure_art9_purged` before every model call. Sweep picks leftovers with `users_needing_art9_purge`.
- Read side: `sheet._load` filters therapy moments/tools/homework ideas unless `art9_consent_active` (`_Map.art9`); validator `therapy_allowed=False` forces new tool origin "self".
- PROFILING: process_user deletes all ke_* rows when definitely withdrawn (before switch checks); sweep `users_withdrawn_with_rows`.
- Other: (409, ke ideas act route, "ideas_paused") in PERSONLESS_API_ERRORS; `USER_JOB_DESCRIPTION`; no crisis in job log; pending_stages [] in crisis; anchor fold `C.analytics_anchor`; `push_copy.normalize_language` for prompts; `has_link_or_contact` in clean_text; `NoStoreKeRoute`; forming never stored; `KE_DAILY_CALL_CAP` (60) via `orca_memory.count_up`.

**Why:** security review round 2 (High: Art. 9 data processed after withdrawal; Mediums: crisis flag on PostHog person, uid+crisis in worker logs).

**How to apply:**
- KE test fixture `growing_skill()` now grants ARTICLE9_HEALTH by default (`art9=False` to test absence); any new test seeding session/after_therapy/therapist-todo moments needs ART9 or they vanish from the map.
- Unreadable ART9 consent = no compose/extract call (status consent), never a purge.
- First-week NoStoreRoute must not be reused for other routers: it swallows api_error and turns 500 into 503 first_week_unavailable.
- Mutation-check new privacy tests (backup file, sed the fix out, run, restore) before trusting green.
- `test_ke_endpoints.NOW` is import time; consent records use the wall clock. In a 17-min full run NOW is stale: set relative timestamps from the record itself.
- test_period_card::test_requires_auth fails after any clinician test (they MagicMock firebase_admin.auth, so a forged token passes): base too, not a regression.
- Throwaway base worktree under the scratchpad fails (Filename too long): use a short path like C:/Users/mikol/r2b.
- Building a pytest path list with `sed 's#\([^ ]*\)#app/tests/\1#g'` on a space-terminated list adds a bare `app/tests/` = the whole suite.

Related: [[ke-review-fixes-crisis-art9-personless-2026-10-19]], [[redesign-v3-be-integration-2026-10-19]]
