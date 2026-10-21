---
name: ke-backfill-recon-2026-10-19
description: Operator asked to "backfill KE for existing users" (2026-10-19); KE is dormant in prod v574 by default and has no bulk backfill by design; sweep throughput limits and a daily-cap starvation bug found
metadata:
  type: project
---

Read-only recon on integration/redesign-v3-final (prod v574), 2026-10-19. No code changed.

- With defaults (no CHARACTER_KE_* config vars; tracked .env has none) every /gamification/ke/* answers 404 ke_unavailable, the client shows the v1 sheet, and ke_sweep only looks for purges. No extraction, no ke_user_state rows.
- There is no backfill script. "Backfill" = first GET /ke/sheet activates a person (record_open), then the 30-min sweep reads the last 90 days (floor = ke_user_state.created_at - 90 d), 15 ready entries per job, one compose at the end. Never-opened users are never read (data minimisation, security review MEDIUM). Proactive pre-activation would contradict that and needs legal M-5 + security sign-off.
- Throughput: KE_SWEEP_TIME_BUDGET_SECONDS 300 / ESTIMATED_SECONDS_BACKFILL 60 = 5 backfill jobs per tick (240/day), steady users (20 s) go first. KE_SWEEP_MAX_USERS 200 never binds.
- Bug found (not fixed): a user who hits KE_DAILY_CALL_CAP stops without a commit, so ke_user_state.updated_at does not move and select_candidates (sort by updated_at asc) puts them first every tick until UTC midnight; 5 capped users starve all other backfills.
- ART9 granted after the first read never re-reads old therapy entries (cursor already moved past them).
- Open before going wider: legal M-5, M-1 (names/in_your_words/focus/hard labels/idea why built partly from therapy moments survive ART9 purge: cleanup._delete_orphans), M-2 (crisis regex runs on summaries only, extract.py run_extraction), ke_quality_eval.py real-model run.

**Why:** operator expected a backfill to exist; the design deliberately has none.
**How to apply:** superseded the same day: the operator decided KE for everyone plus a premium-only backfill. On feat/ke-rollout (41f3153) the starvation bug, M-1 and M-2 are fixed and a backfill script exists, see [[ke-rollout-premium-history-2026-10-19]]. The notes above describe origin/main 1045891 only.

Related: [[ke-review-round2-art9-purge-2026-10-19]], [[project-ke-privacy-review-fixes-2026-10-18]]
