---
name: feedback-comment-watch-implementuj
description: "In the design-artifact comment watch, a comment with the word IMPLEMENTUJ means the look is approved and app implementation must start"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3db298d3-320b-4d06-a645-197780005c6a
  modified: 2026-10-19T16:52:20.869Z
---

Operator rule (2026-10-19): when a comment on the design artifact (comment watch, https://claude.ai/artifact/1T46tjjRbva5YaEL2M5hRF) contains "IMPLEMENTUJ", the design of that board is approved and I start the implementation in the app, not only a mockup edit.

**Why:** Darek and the operator approve designs in the artifact; IMPLEMENTUJ is their go signal, so nobody has to repeat the request in chat.

**How to apply:**
- Still wait for END on that thread; the board named by the comment's location is the spec.
- Mark the board with the orange n_claude_status note ("Claude implementuje: ..."), then green when the code is on dev.
- Delegate per CLAUDE.md (I do not write app code): flutter-mobile for UI, backend-api / data-analytics if the board needs API changes; tests, PostHog coverage table, worktree branch, never `git add .`.
- Frontend-only changes go to dev like the daily UI fixes (fast-forward push, Codemagic builds TestFlight). Anything touching backend or prod (push to main, migrations, config) still needs the operator's explicit OK in chat.
- Report to the operator in Polish what was implemented and the commit.

Related: [[feedback-artifact-design-rules-darek]], [[project-redesign-v3-teams-2026-10-18]].
