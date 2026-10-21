---
name: project-ke-character-kd2-be1-2026-10-18
description: KD v2 "KE" character tab backend BE1 (7 ke_* tables, migration ke_a7c3e9f1b2d4, /gamification/ke API); underscore revision-id regex trap in test parsers; merge-time chain-tip tests to update
metadata:
  type: project
---

BE1 of the KE character tab: commit `693de12` on `feat/character-kd2-v3` (worktree MindSync-wt-character-kd2), pushed to origin only (2026-10-18). Contract lives in the team scratchpad `teams/character/API.md`. BE2 (LLM extractor/composer/sweep cron) is a separate task that calls `sheet.observe_stage_changes` and `sheet.complete_initial_sync`.

Non-obvious decisions:
- One `pending_stages` entry per skill at its CURRENT stage (not one per stage passed), so a jump Discovered to Growing shows one KE4 screen.
- `ke_skills.stage_reported` is an analytics high-water mark (atomic UPDATE ... WHERE stage_reported = old); `stage_seen` is the KE4 ack. Rejection can lower a stage but never re-fires the event.
- Routes answer 404 `ke_unavailable` when the ke tables are missing (exception text contains "ke_" + "no such table"/"does not exist"), so a lagging schema means v1 fallback, not 500.
- `paths[].entry_count` includes sessions; `session_count` is a subset.
- Agenda via `ws_crud.create_agenda_item(source_type="manual")`; to-do inserted directly (origin ai, source_type NULL) because `create_action_point` commits before the idea link could be written.

Gotchas:
- Revision ids with an underscore (`ke_...`) are invisible to `[a-z0-9]+` regex parsers in tests: `test_alembic_chain._REVISION_RE` fell back to matching inside `down_revision` and silently mis-parsed. Fixed there (anchored `^revision`, `[a-z0-9_]+`). Many other tests still use `[a-z0-9]+` for `down_revision`; a future migration whose parent is `ke_...` will not be seen by them.
- Write tool turns `"—"` escapes into the literal character; use `chr(0x2014)` in source (see [[project_h4_neutral_push_allowlist_2026_10_08]]).

**Why:** three teams branch migrations off m320 in parallel; integration linearizes.
**How to apply:** at merge, `test_ke_migration.py::test_single_head_is_this_revision` and `test_only_child_of_m320` assert ke is THE head / only child of m320; re-chain and update them (chain-tip lesson in MEMORY.md). Re-run KE idea tests after the Workspace team's crud changes.
