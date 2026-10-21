---
name: feedback_concurrent_session_git_hygiene
description: "Multiple agent sessions share ONE git working tree — check branch, stage explicit files, use isolated worktrees; never git add ."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a765e70c-b2e6-4699-8dfa-2b4c166df0cd
---

Multiple Claude/agent sessions run CONCURRENTLY in the SAME frontend git working tree (one checkout, one HEAD). They step on each other: a branch switch by one session moves HEAD under another; commits land on the wrong branch; one session's `git add .` sweeps up another's in-progress, unrelated work.

**Why:** observed twice in 48h — voice-note fix 2026-06-19/21 ([[project_voice_note_dataloss_fix_2026_06_19]]) and de-clinicalization 2026-06-20 ([[project_declinicalization_l10n_2026_06_20]]). The de-clin session's feature commit landed on the voice session's branch mid-work and needed an isolated-worktree cherry-pick + `reset --soft`/restore recovery. In the voice session the working tree held 30+ modified files from ≥4 unrelated streams (l10n, session-recording, settings/notif, onboarding) at once.

**How to apply:**
- Before ANY commit: `git rev-parse --abbrev-ref HEAD` — confirm the branch is what you expect (it may have been switched by another session).
- Stage ONLY your files explicitly by path: `git add path/a path/b`. NEVER `git add .` / `git add -A` / `git commit -a` in this repo.
- After staging, VERIFY before commit: `git diff --cached --name-only` must list exactly your files and nothing else; after commit, `git show --stat <sha>`.
- For merges, post-merge builds, or anything that mutates the working tree, use an ISOLATED worktree: `git worktree add --detach <tmp> <ref>` (or `git worktree add <tmp> <branch>`), do the work there, push from there, `git worktree remove --force <tmp>`. The shared main working tree (full of others' uncommitted work) is never disturbed — and switching its branch usually FAILS anyway because their uncommitted edits collide with the target.
- Before deleting a branch, prove it's merged: `git merge-base --is-ancestor <sha> origin/dev`.

Repo layout + CI specifics: [[reference_frontend_ci_git_topology]]. Status discipline: [[feedback_memory_write_after_commit]].
