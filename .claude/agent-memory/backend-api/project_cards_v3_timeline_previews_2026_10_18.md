---
name: cards-v3-timeline-previews-2026-10-18
description: Timeline one-line previews (board A3) composed server-side in 7 locales, commit 7c69c66 on feat/cards-v3 (pushed to the branch only); test-baseline and worktree gotchas
metadata:
  type: project
---

Cards v3 review finding "raw [:100] previews" fixed on `feat/cards-v3` (commit `7c69c66`, pushed to origin/feat/cards-v3 only, not main).

- Pure copy in `app/services/timeline_preview_text.py`; DB enrichment `apply_timeline_previews` in `app/services/timeline_preview.py`, called by both timeline endpoints. CRUD builders attach private `_preview_*` keys, which the service always strips.
- Language = `UserPreferences.ai_language`. The FE has ONE setting "App & AI Agents Language", so server-side copy in ai_language is the UI language, not a mismatch.
- Weekly/Monthly counts reuse data-analytics `analytics._load_session_events` / `weekly_day_span` / `monthly_spans` (read-only import, private name) so the row matches GET /analytics/period_card. A parity test guards against drift.
- **Open (not mine):** the FE must drop the extra duration, limited-data and audio lines in `_TimelineCard`. Old shipped builds show "48 min" twice on Recording rows until then. The Weekly ", anxiety easing" fragment needs per-focus-area direction from data-analytics.

**Why:** the board needs composed rows. Composing them on the backend means the FE only has to delete lines.

**How to apply:** a new preview type goes through `truncate_preview`, never a slice. Full-suite gotchas: split by `NR%4` makes group 1 fail 57 tests on base too (order pollution), and `test_period_card::TestEndpoint::test_requires_auth` fails in group order on base. Diff the failure sets against a base worktree. A worktree under the long scratchpad path fails with "Could not reset index file", so use a short sibling path such as `MindSync-wt-cardsbase` and remove it afterwards. In bash heredocs too, `\u` escapes in tool args get decoded, so build backslashes with `chr(92)`. See [[test_baseline_pytest_history]].
