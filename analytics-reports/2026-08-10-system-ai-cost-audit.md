# SYSTEM AI Cost Audit — token_usage_log feature='SYSTEM' (task A13)

**Date:** 2026-08-10
**Owner:** data-analytics
**Trigger:** B7 audit (`analytics-reports/2026-08-10-voice-chat-assessment.md`) flagged `feature='SYSTEM'` as 93% of last-60d AI spend ($134.23 of $144.90), with 0 attributed users, never audited before.
**Access:** code recon (repo `MindSync/`) + read-only Postgres prod (`heroku run -a mindsync python`, one-off dynos run.1570 and run.9191, both stopped after capture) + live Heroku worker logs (`heroku logs -a mindsync`), no PII, no writes.

## Headline finding

**`SYSTEM` is not background summary jobs. It is the default fallback label `log_token_usage()` writes whenever an OpenAI call fires outside a `with track_usage(...)` block** (`app/services/usage_tracking.py:212`: `feature = feature_override or (ctx.feature if ctx else "SYSTEM")`, `operation = ... or "unknown"`). 100% of the 155,401 SYSTEM rows in the last 60 days carry `operation='unknown'` — not one row is the four periodic-summary jobs that also (deliberately) label themselves `SYSTEM`. Those jobs are dead (see §3).

The unattributed cost traces to **exactly two source files, both already owned by `data-analytics`**, that call `openai_service.gpt_structured(...)` with no `track_usage()` wrapper at all:

1. **7 Notification-Moment / in-app-insight AI-text generators** (`app/services/moments/*.py` ×6, `app/services/insights/recovery_moment_insight_detector.py` ×1) — the dominant driver, ~99%+ of the cost.
2. **`app/services/clinician_ai.py`** (6 functions) — a minor, low-volume co-contributor (clinician portal).

Worse, code + **live production worker logs from today** show the notification-moment cost isn't just unattributed — most of it is **wasted**: the orchestrator generates AI copy for every eligible candidate *before* picking a winner, and a separate bug crashes the persist step on duplicate candidates after the (paid) AI call already ran.

## 1. How the SYSTEM bucket breaks down (prod, last 60 days)

```sql
SELECT operation, api_type, model, COUNT(*), COUNT(DISTINCT user_id), SUM(cost_usd)
FROM token_usage_log
WHERE feature = 'SYSTEM' AND created_at >= now() - interval '60 days'
GROUP BY operation, api_type, model;
```

| operation | api_type | model | rows | distinct users | cost |
|---|---|---|---:|---:|---:|
| `unknown` | CHAT_STRUCTURED | gpt-5.4-mini | 155,380 | **0** | **$134.227000** |
| `unknown` | STT | gpt-4o-mini-transcribe | 1 | 0 | $0.003000 |
| `unknown` | STT | whisper-1 | 20 | 0 | $0.000000 |

**`generate_daily_summary` / `generate_weekly_summary` / `generate_monthly_summary` / `generate_yearly_summary` — the four operations `app/services/periodic_summary.py` deliberately labels `SYSTEM` — have zero rows in the last 60 days.** That job is not the source of this cost; it isn't running at all right now (§3).

Trend (60d daily): cost is near-zero through 2026-07-02, jumps to 208 rows on 2026-07-03, then ramps to a ~4,900-5,000 rows/day / ~$4.2-4.3/day plateau by 2026-07-10, holding roughly steady (~3,600-4,900 rows/day) through today. **This ramp date is not a coincidence** — it lines up almost exactly with the Notification Cadence v3 deploy (BE commit 2621868, Heroku v515, deployed 2026-07-03 evening per project memory) that first wired the moment-orchestrator generators into the live worker registry.

Trend totals: 7d=$22.20 (25,784 rows), 30d=$110.87 (128,393 rows), 60d=$134.23 (155,401 rows) — consistent with a steady-state daily job, not a one-off spike.

Model: 100% of the CHAT_STRUCTURED volume is `gpt-5.4-mini` — this is not a "wrong/expensive model" problem. Prod `.env` shows `GPT_MODEL`, `GPT_MODEL_MINI`, `GPT_MODEL_41_MINI`, and `GPT_MODEL_41` **all alias to the same model** (`gpt-5.4-mini`) today. Every code path in this audit (`moment_text_generator.py`, `clinician_ai.py`, `periodic_summary.py`) ultimately resolves to this one already-cheap model. The problem is 100% volume/waste, not model tier.

## 2. Root cause #1 (the big one): AI text generated for every candidate, only one ever shown

**File:** `app/services/notification_orchestrator.py` (mine), method `_run_reactive_for_user` (~lines 380-524).

The reactive pass (covers `MOOD_DIP_ALERT`, `MOOD_UPDATE_REQUEST`, `RE_ENGAGEMENT`, `THERAPY_RELATIONSHIP_CHECKIN` — the four AI-generating "competitive" moment types) works like this:

```python
for generator in self._generators:                      # line 422
    if generator.is_eligible(db, user, now):             # line 449
        candidate = generator.generate(db, user, now)    # line 450 — PAYS FOR THE LLM CALL HERE
        if candidate is not None:
            candidates.append(candidate)
...
candidates.sort(key=lambda c: c.score, reverse=True)      # line 498
winner = candidates[0]                                     # line 499 — only this one gets persisted
```

`generator.generate()` is what calls `generate_moment_text()` → `openai_service.gpt_structured()` to render the actual push/in-app copy — **before** the scoring step that picks a single winner. Every generator that is simultaneously eligible for a user on a given tick pays for a full LLM completion; only the top-scored one is ever persisted and shown. The rest — copy, tokens, dollars — are silently discarded at line 499.

This runs on an **hourly cron** (`app/core/rq_scheduler_setup.py:338`, `scheduler.cron("0 * * * *", func=run_daily_orchestrator, ...)`), and the slot-fill guard (`_slot_already_filled`, line 401) only short-circuits *after* a moment has actually been persisted for that slot/day — so while a slot is open and un-filled, **every hourly tick regenerates fresh AI copy for every currently-eligible generator**, all discarded, until one finally wins and fills the slot (or the day ends).

Compounding this: `is_eligible()` for these generators mostly checks a *business* condition (e.g. `THERAPY_RELATIONSHIP_CHECKIN`'s `is_eligible` checks "hasn't completed a `TherapyHealthCheck` this week" — a completely different table from `NotificationMoment`), not "was a candidate for this exact dedup window already generated." So a user can stay "eligible" — and get regenerated AI copy — for the same moment type on every eligible tick for days, even after that week's moment has already been created and dedup-blocked.

### Root cause #2 (live bug, confirmed in production logs *today*): the winner also frequently fails to persist

`_persist_moment` (line 1160) wraps `create_moment(...)`, whose docstring says explicitly: **"Returns None on duplicate (skip silently)."** The caller does not honor that contract:

```python
moment = self._persist_moment(db, user_id, winner)          # line 516 — may legitimately be None
log_orchestrator_decision(user_id, candidates, winner)
posthog_track_moment(user_id, "moment.scheduled", {
    ...
    "moment_id": moment.id,                                   # line 522 — CRASHES if moment is None
})
```

When `create_moment` returns `None` (duplicate `dedup_key` — e.g. this week's `THERAPY_RELATIONSHIP_CHECKIN` was already created on an earlier day), line 522 raises `AttributeError: 'NoneType' object has no attribute 'id'`, caught by the surrounding `except Exception as persist_err` (line 525) and logged as an **ERROR**: `"[ORCH] Failed to persist moment for user %s: %s"`.

This is happening live, right now. A 1,500-line sample of `heroku logs -a mindsync` pulled during this audit (2026-08-10, 17:01:04–17:05:31 UTC, one hourly-orchestrator tick) contains **433 occurrences of this exact error** in a 4m27s window — a batch of already-AI-generated candidates crashing on the persist step because the underlying dedup_key already existed. This confirms root cause #1's mechanism is not theoretical: the AI text is generated, the "winner" is picked, and a meaningful share of those winners *still* get thrown away by this bug, at ERROR-log volume high enough to bury real persist failures in noise.

### Quantifying the waste (prod, last 60 days)

| | value |
|---|---:|
| Unattributed GPT calls (`SYSTEM`/`unknown`, CHAT_STRUCTURED) | 155,380 |
| `notification_moments` rows actually persisted with `is_ai_generated=true` | 7,008 |
| — `THERAPY_RELATIONSHIP_CHECKIN` | 5,252 |
| — `RE_ENGAGEMENT` (warm/AI path) | 1,139 |
| — `MOOD_UPDATE_REQUEST` | 597 |
| — `MOOD_DIP_ALERT` | 10 |
| — `POST_SESSION_REFLECTION`, `THERAPY_PREP` (schedule-driven, separate pass) | 0 (never triggered in this window) |
| — `app_insights_shown` (`RECOVERY_MOMENT` via `recovery_moment_insight_detector`) | 0 (only `NOTICE`, non-AI, ever fired) |
| **Ratio: AI calls per persisted, user-visible AI moment** | **≈ 22:1** |
| **Implied waste share of the $134.23** | **≈ 95%** |

Put differently: of the ~$134.23 spent on this bucket in 60 days, an estimated **~$127-128 produced AI copy that was never shown to any user** — either out-scored by another candidate on the same tick, or generated and then discarded by the persist-crash on a stale-but-still-"eligible" dedup window. The legitimate cost of the notification-moment AI copy that users actually see is on the order of **$6-7/60d**.

`clinician_ai.py`'s 6 unwrapped functions (`generate_brief`, `synthesize_golden_thread`, `suggest_goals`, `assemble_session_note` ×2 formats, `analyze_voice_note`, all `model=settings.GPT_MODEL_41_MINI`) also land in this same `SYSTEM`/`unknown` bucket, but clinician-portal adoption is small (few clinician accounts, on-demand triggers only — no competitive-generation pattern) so its share of the $134.23 is minor relative to the orchestrator waste; it was not separately broken out because the row signature is indistinguishable from the moment-generator calls without the code-level attribution fix below (both use the same model/api_type). It's called out separately because the fix path differs (§4).

## 3. Related, out-of-scope finding: periodic conversation summaries are dead code in prod

`app/services/periodic_summary.py` (`generate_daily_summaries`, `generate_weekly_summaries_for_sun/mon`, `generate_monthly_summaries`, `generate_yearly_summaries` — the "Daily, weekly, monthly, yearly summary generation" feature described in this agent's own charter) is:
- **Not registered anywhere** in `app/core/rq_scheduler_setup.py` or `app/main.py` lifespan (grepped both, zero matches).
- **Not in the Heroku Procfile** (only `web`/`worker`/`scheduler` process types — no `clock`/cron dyno).
- Its only entry point, `app/run_daily_summaries.py`, is a standalone script that (even if invoked) only calls `generate_daily_summaries()` — the weekly/monthly/yearly functions are imported but never called from it.
- `periodic_summaries` table (prod): last row per period_type — DAILY 2026-03-06, WEEKLY 2026-03-02, MONTHLY 2026-02-28, YEARLY 2026-01-01. **Nothing has been written since March 2026.**

This costs nothing today (it simply doesn't run), but it means one of the analytics features this role is chartered to own is silently orphaned. Flagging for a separate decision (revive on a real schedule, or delete the dead code/table) — out of scope for this cost audit, not touching it here.

## 4. Fixes applied now (cheap, safe, no schema change)

Wrapped all 7 previously-unattributed AI-text call sites in `track_usage("NOTIFICATION", "<specific_operation>", user_id=...)`, reusing the existing `NOTIFICATION` FeatureEnum value (already used by `notification_service.py`'s `generate_nudge_text`) so **no Alembic migration is required** — `feature` is a native Postgres enum, `operation` is free-text `varchar(128)`.

Files edited (all owned by data-analytics, confirmed via prior authorship in agent memory — Notification Moments Phase 2/3, 2026-05-14/15):
- `app/services/moments/mood_dip_alert_generator.py` → operation `mood_dip_alert_text`
- `app/services/moments/mood_update_request_generator.py` → operation `mood_update_request_text`
- `app/services/moments/post_session_reflection_generator.py` → operation `post_session_reflection_text`
- `app/services/moments/re_engagement_generator.py` → operation `re_engagement_text_warm`
- `app/services/moments/therapy_prep_generator.py` → operation `therapy_prep_text`
- `app/services/moments/therapy_relationship_checkin_generator.py` → operation `therapy_relationship_checkin_text`
- `app/services/insights/recovery_moment_insight_detector.py` → operation `recovery_moment_insight_text`

**Effect:** going forward, this cost stops landing in `SYSTEM` and shows up under `feature=NOTIFICATION`, broken out per generator by `operation` — so the waste from §2 becomes directly measurable per-type in future audits (and will make the impact of a future orchestrator fix visible in the data). **This does not reduce spend** — it only fixes attribution. It does not touch `notification_orchestrator.py`'s generate-before-select logic or the `_persist_moment` None-check bug (see §5) — those are real code changes to a load-bearing production delivery path and are out of scope for a "cheap labeling fix"; they're handed off as prioritized recommendations below.

Verified: ran the full existing test suite for all 7 touched files (`test_cs06_payload_fixes.py`, `test_dedup_key_generators.py`, `test_mood_dip_alert_generator.py`, `test_msv32_notification_generators.py`, `test_phase2_registration.py`, `test_post_session_nudge_schedule_driven.py`, `test_post_session_reflection_generator.py`, `test_prep_reminder.py`, `test_re_engagement_generator.py`, `test_recovery_moment_insight_detector.py`, `test_therapy_prep_generator.py`) — **280 passed, 0 failed**. Committed locally only, not pushed (per task instructions).

## 5. Recommendations (not implemented — sized by owner, effort, and $/month)

Ranked by expected savings:

1. **[HIGH IMPACT, `data-analytics` to implement, medium effort] Fix `notification_orchestrator.py` to score before generating.** Split each `MomentGenerator.generate()` into a cheap, rule-based "build + score candidate" step (no AI call) and a separate "render AI copy" step that is only invoked for the single winner *after* `candidates.sort()`/`winner = candidates[0]` (line 497-499). This is the real fix for root cause #1. **Estimated savings: ~90-95% of this bucket's run-rate.** At the current ~$110.87/30d actual (or the more recent ~$22.20/7d ≈ $95/30d run-rate), that's roughly **$85-105/month**. Medium effort because it touches the `MomentGenerator` interface used by all 6 competitive/schedule-driven generators — needs a coordinated change across all of them, not a one-line fix; recommend a dedicated task with its own test-suite run (this file is load-bearing for real user notifications — treat with the same care as the H10-class incidents in project history).

2. **[MEDIUM IMPACT, quick, `data-analytics`] Fix the `_persist_moment` None-check bug** at `app/services/notification_orchestrator.py:516-524` — add `if moment is not None:` before the `posthog_track_moment(...)` block that reads `moment.id`, matching the documented "Returns None on duplicate (skip silently)" contract. This alone won't recover the AI spend already paid before the persist call, but it: (a) stops burying real persist failures under ~400+/hour of expected-duplicate noise in production error logs, and (b) is a prerequisite for cleanly measuring the effect of fix #1 (right now you can't tell a real failure from a benign duplicate in the logs). Low risk, single-file, isolated `if` guard — good candidate for the next small PR.

3. **[LOW EFFORT interim mitigation, if #1 is deferred] Cache AI-generated copy per (user, moment_type, dedup window)** in Redis for the duration of the dedup window, so repeated hourly ticks within the same still-open slot reuse the last-generated text instead of re-calling the LLM every time. Cheaper to ship than #1, recovers a meaningful fraction of the waste, does not fix the "candidates.sort() discards N-1 texts on a single tick" mechanism — treat as a stopgap, not a substitute for #1.

4. **[SMALL, needs a migration — handoff to `backend-api`] Give `clinician_ai.py` its own `FeatureEnum` value.** None of the 24 existing labels fit "clinician portal AI" cleanly; reusing `NOTIFICATION` (like the moment generators) would be misleading. Requested schema change:
   - **Table:** `token_usage_log` (via the `featureenum` Postgres native enum type)
   - **Change:** `ALTER TYPE featureenum ADD VALUE IF NOT EXISTS 'CLINICIAN';` — idempotent, following the exact precedent of migration `uu1v2w3x4y5z` (`HERO_INSIGHT`, 2026-06-21) already in the repo, including its dialect guard + `IF NOT EXISTS` clause.
   - **Nullable/default:** N/A (enum value addition, not a column change).
   - Once migrated, data-analytics will wrap `clinician_ai.py`'s 6 `gpt_structured` calls in `track_usage("CLINICIAN", "<function_name>", ...)`. Expected impact: small (<$1-2/month based on current clinician-portal adoption) — do this for attribution completeness, not because it's a meaningful cost lever.

5. **[PROCESS] Update the FeatureEnum drift guard test.** While tracing this, found `app/tests/test_featureenum_hero_insight.py::test_all_track_usage_labels_are_in_feature_enum` hard-codes a *snapshot* of `track_usage()` labels "as of 2026-06-21" instead of grepping the live codebase — so it silently stopped catching new drift. Two labels added since then, `THREAD_CONTEXT` (`app/tasks/thread_context.py:79`) and `WEEKLY_OBS` (`app/tasks/weekly_observations.py:152`), are **not in `FeatureEnum`** (confirmed against `app/models/models.py:1693-1704`, 24 members, neither present) and **not in any migration** (grepped `app/alembic/versions/*.py`, zero matches). Because `log_token_usage()` is fire-and-forget (blanket `try/except`, `usage_tracking.py:210-241`), every `track_usage("THREAD_CONTEXT", ...)` / `track_usage("WEEKLY_OBS", ...)` call's Postgres insert silently fails on the invalid enum label and is swallowed — meaning **this AI spend isn't in `SYSTEM` either; it's simply never recorded anywhere.** This is adjacent to, not part of, the SYSTEM/93% story (it's an invisible-cost bug, not a misattributed-cost bug) but the fix is the same shape as item 4: `backend-api` migration adding `THREAD_CONTEXT` and `WEEKLY_OBS` to `featureenum`, then the guard test should be changed from a hard-coded set to a live grep so this class of drift can't recur silently. Flagging, not fixing — outside this audit's scope and `models.py`/`alembic/` are not mine to edit.

## 6. Data-quality caveats

- Waste ratio (§2, ≈22:1) is derived by comparing raw `SYSTEM`/`unknown` call volume against `notification_moments`/`app_insights_shown` persisted-row counts in the same 60d window. It assumes the vast majority of `unknown` rows are moment-generator calls, based on: (a) the daily-trend ramp date matching the Cadence v3 deploy exactly, (b) the model (`gpt-5.4-mini`) and `api_type` (`CHAT_STRUCTURED`) matching `moment_text_generator.py`'s explicit `model=settings.GPT_MODEL_41_MINI` call signature, and (c) live logs showing the exact crash mechanism firing at high volume during the capture window. It is **not** a row-level trace (the `unknown` operation label doesn't allow one retroactively) — the fixes in §4 make this fully attributable going forward.
- The 433-error/4m27s live-log sample (§2) is one hourly-tick snapshot from today (2026-08-10, 17:01-17:05 UTC) — directional confirmation of the mechanism and its live severity, not a 60-day rate; don't extrapolate it linearly to "X failures/day" without a longer capture window.
- `clinician_ai.py`'s exact share of the $134.23 is not separately quantified — its call signature (model, api_type) is currently indistinguishable from the moment generators' in the raw data. Will be exact once fix #4 ships.
- Cost-per-summary / cost-per-insight metrics requested in the original task ("USD per generated summary/insight/personal-bio refresh") were not computed for periodic summaries (§3, feature is dead — 0 summaries generated in-window, so cost-per-summary is undefined/moot) or for personal bio (out of scope — `PERSONAL_BIO` is already correctly attributed outside `SYSTEM`, per the B7 report's by-feature table: $0.832221/393 rows over 60d ≈ $0.00212/call; the 2026-05-19 cache-cost-optimization project appears to be holding, this feature is not part of the SYSTEM problem).

## Bottom line

**Top 3 cost components of the `SYSTEM` bucket, last 60 days:**
1. **Notification-moment AI-text generation waste** (`notification_orchestrator.py` generate-before-select + persist-on-duplicate crash) — ≈$127-128 of $134.23 (≈95%), zero of it user-attributed, most of it never shown to a user.
2. **Legitimately useful notification-moment AI copy** (the ~7,008 moments that *did* get persisted and presumably sent) — ≈$6-7 of $134.23.
3. **Clinician portal AI functions** (`clinician_ai.py`, 6 functions, low volume) — small, unquantified remainder.

**Recommended savings, ranked:** fix #1 (score-before-generate in the orchestrator) ≈ **$85-105/month**; fix #2 (persist None-check) — no direct $ but unblocks clean measurement and log signal; fix #3 (Redis cache) — smaller interim recovery if #1 is deferred; fixes #4/#5 — attribution completeness, not savings.

**Files changed this session:** `app/services/moments/mood_dip_alert_generator.py`, `mood_update_request_generator.py`, `post_session_reflection_generator.py`, `re_engagement_generator.py`, `therapy_prep_generator.py`, `therapy_relationship_checkin_generator.py`, `app/services/insights/recovery_moment_insight_detector.py` (all: added `track_usage("NOTIFICATION", ...)` wrapper, no logic change). Committed locally, not pushed.

**Not changed (handoff):** `app/services/notification_orchestrator.py` (recommendations #1-#2, mine to implement as a follow-up task), `app/services/clinician_ai.py` (blocked on `backend-api` migration, recommendation #4), `app/models/models.py` / `app/alembic/versions/` (THREAD_CONTEXT/WEEKLY_OBS enum drift, recommendation #5, backend-api's files).
