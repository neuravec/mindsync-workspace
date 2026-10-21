---
name: ke-review-fixes-crisis-art9-personless-2026-10-19
description: KE review fixes on integration/redesign-v3 (c9a8708, 4f90419, f1c14dd): server-side crisis idea pause, Art. 9 gate on KE sources, person-less skill_stage_reached; art9_consent_state helper
metadata:
  type: project
---

Three KE review fixes landed on integration/redesign-v3 on 2026-10-19 (pushed to origin only, 5915719..f1c14dd).

- Crisis: `_visible_ideas` returns [] while `ke_user_state.latest_entry_crisis`; POST /ke/ideas/{id}/act answers 409 `ideas_paused` to agenda/todo/orca on a not-yet-acted idea (not_now/undo still work, acted idea returns first result). Client reverts any failed act generically, so no FE change.
- Art. 9: `therapy_consent.art9_consent_state` (True/False/None) added; `art9_consent_active` delegates to it. KE extract skips session/after_therapy/therapist-homework rows for good without ARTICLE9_HEALTH (cursor advances, no crisis check); unreadable consent stops the job instead. Compose `_open_homework` and sheet `_next_session_date` gate on `art9_consent_active`.
- `skill_stage_reached` now person-less (`personless_distinct_id()` + `personless()`); `distinct_id` params removed from build_sheet/observe_stage_changes.

**Why:** review findings (2026-10-19): crisis suppression was client-only; H-3 says therapy_consent is the one gate; M-1 requires person-less health-inference events.

**How to apply:**
- Use `art9_consent_state` whenever a "no" is permanent (cursor skip, deletion); `art9_consent_active` only when retrying later is automatic.
- Tests: `ke_pipeline_support.add_art9_consent(db, uid)`; the test_ke_extract `db` fixture grants ART9 to u1/u2, `TestArt9Gate.bare` does not. Endpoint tests use `self.art9_consent()` before asserting `next_session_date`.
- Open residual: moments already extracted from therapy entries are not purged on an ART9 withdrawal (only PROFILING withdrawal wipes ke_*). Legal M-5 still open.
- Git Bash `sed -i` turns a CRLF working file into LF (index stays LF, diff fine); `git checkout -- <file>` after the commit restores CRLF.

Related: [[ke-privacy-review-fixes-2026-10-18]], [[redesign-v3-be-integration-2026-10-19]]
