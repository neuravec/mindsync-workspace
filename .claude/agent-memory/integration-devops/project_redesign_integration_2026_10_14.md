---
name: project-redesign-integration-2026-10-14
description: Redesign (cards, Workspace, Character KD) merged locally into feat/redesign-integration in both repos, plus *-on-release-1013 variants that also carry the 10-13 release; NOT pushed
metadata:
  type: project
---

On 2026-10-14 the three redesign teams were merged locally (not pushed, not deployed):
- BE `feat/redesign-integration` (worktree MindSync-wt-redesign-int) = origin/main 7e281ff + feat/after-card-progress + feat/character-sheet + .env.example settings commit. Alembic head m320c4a5r6d7 on m318.
- FE `feat/redesign-integration` (worktree mindsync-frontend-wt-redesign-int) = origin/dev 03aab0d + cards, workspace, character-sheet. All merges textually clean.
- Variants that also include the unpushed release branches: BE `feat/redesign-integration-on-release-1013` (m320 re-chained onto m319, chain tests updated) and FE `feat/redesign-integration-on-release-fe-1013` (ARB union + gen-l10n).

**Why:** release/2026-10-13 adds m319a1b2c3d4 on the same parent m318; whichever lands on main second needs the re-chain. The variant branches already contain it.
**How to apply:** if the release is already on origin/main when pushing, push the *-on-release-* branches, not the plain ones. Deploy order: BE + manual `alembic upgrade head` first, then FE. Flags after_card_progress_panel, character_sheet_v2 and CHARACTER_SHEET_V2_ENABLED stay off; the Character sheet waits for the PROFILING legal sign-off. Gotchas: offline boot needs conftest env vars plus a stubbed firebase_admin (scratch script pattern), and `.env` is tracked in the BE repo, so never overwrite it. On this machine flutter analyze only finishes when it is limited to a few directories (around 2 min); the full set of 89 files timed out.

## Update 2026-10-14 (later): feat/redesign-final ready, NOT pushed
- Backend worktree MindSync-wt-redesign-int-rel, branch feat/redesign-final tip 4c7675b = release/2026-10-13 (c3c209c, never on remote) + progress-panel-v2 (7b73892) + charsheet-consent (d511624). FF over origin/main 7e281ff.
- Prod alembic read 2026-10-14: m318a1b2c3d4. Pending: m319 (CONCURRENTLY index, autocommit_block) then m320 (2 new tables, inspector-guarded). create_all on boot builds the m320 tables first; migration then skips them (verified offline).
- Offline app import on Windows needs MESSAGE_ENCRYPTION_KEY set and a multiprocessing 'fork'->'spawn' shim for rq; SQLite create_all must go per table (rag_documents/message_embeddings use ARRAY).

## Update 2026-10-14 ~13:10 UTC: DEPLOYED
- BE pushed 7e281ff..4c7675b to origin/main; Heroku v571 -> v572 (about 80 s). `alembic upgrade head` ran m319 + m320 cleanly; `alembic current` = m320c4a5r6d7. Boot clean, no H10 or Traceback; CHARACTER_SHEET_V2_ENABLED unset (default true, per lead's brief).
- FE pushed 03aab0d..5c27b2c to origin/dev (Codemagic/TestFlight). Device QA is still open.
- Gotchas: `heroku run --no-tty` returns exit 1 even on success, so read the output. Bare `heroku releases` hung for 120 s without `< /dev/null` plus `timeout`. `gh` is not installed on this machine.
