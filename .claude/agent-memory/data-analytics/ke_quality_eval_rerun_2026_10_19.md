---
name: ke-quality-eval-rerun-2026-10-19
description: KE v2 prompts + self-contained gate script on feat/ke-rollout (e7ebfa4); rerun verdict NOT passed only on therapy-only skills / Orca-as-therapy (needs validator guard); G3 possessive bugs; how to run the gate now
metadata:
  type: project
---

Rerun of the KE quality gate after the [[ke-quality-eval-gate-2026-10-19]] FAIL. Commit e7ebfa4 on feat/ke-rollout
(worktree MindSync-wt-ke-rollout, not pushed): prompts ke-extract-v2 / ke-compose-v2, scripts/ke_quality_eval.py
rewritten, app/tests/test_ke_quality_eval_gate.py. Raw runs: analytics-reports/raw/ke-quality-eval-2026-10-19-rerun/
(full_it1 = first v2, full_it3 = after iter 2, full_it4 = final D, full_E = final with validator stats, replicate_1/2).

**Why:** rollout to everyone was gated on this; blockers were crisis/safety-plan paths and first names.

**How to apply:**
- Run the gate with the script alone now (no wrapper): it seeds flags, consents, premium sub, record_open, counts tokens
  in memory, fails on empty pipelines. Chunks of 7-8 stories fit a 10 min foreground call (~1.5 min each); then
  `--merge a.json b.json ...` re-checks and prints RESULT. Model judgement (precision) is still manual: use review.py
  in the raw folder.
- Final result: crisis/help row, names, dashes, focus language (o/über/sobre), stability: PASS in all runs. Strict
  precision 97.7% and 97.1% on the two full runs (the 9 hard stories: ~94%). Coverage 22-24/30 (old 24/30).
- Still failing after 3 prompt iterations: the composer keeps making a skill from a from_therapy moment alone (2-3 per
  run: S07, S26, S13, S30), and S27's Orca talk gets kind from_therapy, which makes shame eligible and yields a
  "session" skill. Prompts cannot fix it reliably; ask backend-api for a validator guard (skill needs a non-from_therapy
  moment; from_therapy from reflect_talk recast or not counted for eligibility; optionally drop done with helped=false).
- G3 bugs found (backend-api's validate.py): "Monday's"/"Orca's" taken for names (S02 loses a moment every run);
  "Tom's"/"Anna's" not matched (possessive of a short name slips through). Eval checker is possessive-aware.
- Variance is high run to run (temperature default, reasoning_effort none in shared gpt_structured); judge on 2+ runs.
- Cost with final prompts ~$0.009/story (cache 72-81%); whole rerun session ~$1.44.
- UPDATE same day: backend-api added the guards (87bad96, 46f2357) and I added ExtractorInput.forming (8bd2956).
  Gate PASSED on 8bd2956 (full_F, full_G, replicate_F1/F2): 0 story problems in all 4 runs, precision 98.1% over
  527 moments, coverage 23-24/30, path_unbacked dropped 1 path (correct). Leftovers are judgment calls: family drift
  ("the signals" not fear), still_hard guessed, helped=false also drops positive dones (painting, telling the
  therapist) = recall loss; forming reaches only 16/157 extractor calls because load_context runs once per job.
  One run had a cold OpenAI cache (22%) = $0.016/story; warm is ~$0.008.
- 181a810: eval forward-only mode (`--forward` runs ke_synthetic_stories_forward.json F01/F02/F03/U01; `--forward-only`
  drops premium for any story; story fields open_days_ago/upgrade_days_ago/checkpoints_days_ago). Forward set passed
  3/3 on 44d5f52 (H-1 pre-scan works, L-1 turns the help row off after the window). Running the 30 stories with
  --forward-only correctly fails the run-level gate (nothing after the open to read), by design.
- L-4 in openai_service: safe_error(e) (type/status/request id) in gpt_structured, gpt_function, retry decorator.
- Known gap: idea "why" can carry a copied ISO date (validator checks digits in idea text only).
