---
name: ke-rollout-premium-history-2026-10-19
description: feat/ke-rollout 41f3153 (on 1045891, NOT pushed) - KE for everyone with premium-only 90-day history, M-1/M-2 fixed, daily-cap starvation fixed, premium backfill script, quality-gate G1-G4 (crisis window 14d, safety-plan = crisis, name guard, script guard)
metadata:
  type: project
---

Operator 2026-10-19: legal M-5 closed, KE on for everyone, history backfill for premium only; CHARACTER_KE_REQUIRE_PROFILING_OPT_IN will be set to false via config var at enable (code default stays true). Branch feat/ke-rollout in worktree MindSync-wt-ke-rollout, commit 41f3153, no migration, no response-shape change. Not pushed, not deployed.

- Read plan lives in ke_user_state.cursors JSON (int keys only, parse_cursors keeps them): read_plan 1/2, fwd_from, hist_<key>, hist_done 0/1, crisis_at. States without read_plan = legacy 90-day read (all existing tests use S.activate, so they stay legacy).
- Premium = _therapy_helpers.is_user_premium (trial counts until 00:00 UTC of end_date). Batched form history.premium_user_ids = is_active superset query + per-user canonical call. Table is `user_subscription` (singular).
- Backfill: app.tasks.ke.activate_premium_history via scripts/ke_backfill_premium.py; live needs KE_BACKFILL_LIVE=1 (heroku run --env) and extraction on; activates with last_opened_at NULL (history read, then waits for a real open).
- Eval gotcha: analytics-reports/raw/ke-quality-eval-2026-10-19/run_ke_eval.py calls record_open without a subscription; after this branch that gives forward-only (empty) maps = false pass again. It must seed an active premium subscription first.
- G3 name guard is weak for German (nouns capitalised): only "role + Name" caught there; prompt must carry the rest.
- Test gotchas: SQLite reuses a deleted row id (assert by name, not `db.get(id) is None`); this Bash tool mangles heredocs with `\n` escapes or some unicode: write patch scripts with the Write tool and run them.

- Gate rerun guards (87bad96, on data-analytics e7ebfa4): therapy-only new skill dropped, new path needs an own-backed skill/hard/tool; Orca-talk from_therapy is served as noticed with MomentFact.weak (no eligibility, no forming, never a skill alone); done with helped false dropped; _WORD_RE letters only (possessives). Forming families sit in ExtractContext.forming and flow only once prompts.py declares ExtractorInput.forming (data-analytics). KE extraction variance cannot be lowered from KE code: openai_service.gpt_structured hardcodes reasoning_effort "none" and has no temperature argument.

- Security round 3 (44d5f52, after data-analytics 8bd2956): forward_cursors runs a local 14-day crisis pre-scan (extract.newest_crisis_before) and seeds crisis_at; crisis_at is authoritative in crisis_active (flag only when no date); upgrade job reads history BEFORE fresh entries; ART9 purge deletes all not-acted ideas; crisis_at popped when window clears; activate_state merges a plan into existing cursors; backfill --paying-only (purchase, starter_pack).

**Why:** rollout to all users was gated on M-1/M-2, the starvation bug and the failed real-model quality gate.
**How to apply:** before enabling, deploy this branch, set CHARACTER_KE_ENABLED/EXTRACTION_ENABLED true and OPT_IN false, then backfill dry run, then live. data-analytics edits prompts.py on this branch next.

Related: [[ke-backfill-recon-2026-10-19]], [[ke-review-round2-art9-purge-2026-10-19]]
