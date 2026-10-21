---
name: project-first-voice-conversation-fe-deploy-2026-10-05
description: First voice conversation + Orca memory batches, frontend pushed to dev 2026-10-05 as merges e4e0d05, 0031c44 (bumped to 2.0.101) and backfill 86addde; backend went first each time; device QA still open
metadata:
  type: project
---

Frontend of the "first voice conversation + Orca memory" batch was pushed to `mindsync-frontend` `dev` on 2026-10-05: `91e9c80..e4e0d05`, a `--no-ff` merge of `feat/first-voice-conversation` (head 9a14cd9, 6 commits 2d8398e..9a14cd9) onto the Codemagic bump 91e9c80 (`app_2.0.100`). The merge tree equals the branch tree plus that version bump only. Verified in a temp worktree: analyze 0 errors, 447 tests green in wow, first_conversation, orca_memory and subscription.

**Why:** operator approved both repos 2026-10-05; backend went first (Heroku v557, alembic `m315a1b2c3d4`, smoke green), satisfying the backend-first rule in `design-specs/2026-10-03-first-voice-conversation/DEPLOY.md`.

Follow-up push the same day at 09:33: `e4e0d05..0031c44` (merge of 4daf29f M-5 notice pinned above Start talking, 6c70dd4 focus-area casing, 9508788 agreement-free focus-area copy), 290 tests green. Logged in DEPLOY.md section 13. At that point NO Codemagic bump had landed for e4e0d05 after 42 minutes (normal is 7 to 9), cause unknown because there is no Codemagic API token or `gh` CLI on this machine; operator asked to check the dashboard.

Resolved: Codemagic bump `0615f3e` (2.0.101+174, tag `app_2.0.101`) landed 09:55:42 CEST, about 22 minutes after the 0031c44 push; e4e0d05 never got a bump of its own, so 2.0.101 carries the whole batch. Then the Orca memory backfill batch: `0615f3e..86addde` (merge of `feat/orca-memory-backfill` head 3343c37, 5 commits) pushed 14:46 CEST, 398 tests green; backend branch was already fully on `origin/main` (route `POST /users/memory/backfill`, migration 220922f, migration run owned by the backend deploy). Expected next bump 2.0.102.

**How to apply:** a bump can take 20+ minutes and a push can be superseded by the next one without its own bump, so do not treat "no bump after 40 minutes" as a broken trigger until a later push also stays unbumped. Device QA is section 10 of that DEPLOY.md and is still open. The helpline link (commit 9a14cd9, H7) is not in DEPLOY.md's commit table or QA list, so QA it explicitly. Production store promotion still waits for legal sign-off. Rollback = DEPLOY.md section 7.3 (expire build, revert merges 0031c44 then e4e0d05 on dev with `git revert -m 1`). The backend-leg note of this batch was written by an earlier session into `mindsync-frontend/.claude/agent-memory/integration-devops/` (wrong directory, untracked there).

Recipe used: [[reference-fe-dev-push-via-worktree]].
