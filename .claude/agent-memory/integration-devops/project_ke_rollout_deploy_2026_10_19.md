---
name: project-ke-rollout-deploy-2026-10-19
description: KE (Character KD v2) rollout 2026-10-19 - Heroku v575 (main 73081cc) + v576 config (KE on for all, no separate opt-in), Reflect summary backfill and KE premium backfill done, first sweep ok
metadata:
  type: project
---

Deployed 2026-10-19: branch release/ke-rollout = 54a5529 (feat/ke-rollout) + cherry-picks of fbb3e5b/64c1aa8 (Reflect summary backfill script) as 38637fa/73081cc, fast-forward pushed to origin/main from 1045891 (v574). Heroku v575 "Deploy 73081cc0", about 80 s after push. No migration, no Procfile/requirements change.

- Reflect summary backfill (premium only): 17 threads from 5 users analyzed, 0 failed, actual $0.0192 + $0.5403.
- v576 = operator's own `heroku config:set CHARACTER_KE_ENABLED=true CHARACTER_KE_EXTRACTION_ENABLED=true CHARACTER_KE_REQUIRE_PROFILING_OPT_IN=false`. The same command from this agent was denied by the auto-mode classifier even with the lead relaying operator approval.
- KE premium backfill (all premium, not paying-only): premium 23, eligible 23, with_entries 13, activated 23, errors 0.
- First sweep 12:17 UTC: candidates=13 enqueued=5 errors=0; 5 jobs status=ok, failed=0, 3.5-19 s each (the sweep's 60 s/job estimate is very pessimistic, so the 13 take several ticks).

**Why:** operator approved KE for all users and an all-premium backfill on 2026-10-19 after the legal sign-off.

**How to apply:** kill switches are CHARACTER_KE_EXTRACTION_ENABLED=false (stops model calls, keeps the sheet) and CHARACTER_KE_ENABLED=false; prod config changes may need the operator to run them. See [[reference-heroku-oneoff-smoke]].

Warnings seen: RAG indexer logs a user id at INFO despite the backfill script lowering `app` logging; summary model sometimes emits misspelled emotion labels that the validator drops; backend PostHog `identify()` fails on every call with `TypeError: unexpected keyword argument 'set_once'` (posthog SDK pinned >=3.7,<4; pre-existing, not KE).
