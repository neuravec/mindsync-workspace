---
name: system-ai-cost-audit-2026-08-10
description: token_usage_log feature=SYSTEM root-cause audit (task A13) — SYSTEM is the track_usage() default fallback, not background jobs; found + fixed a 22:1 AI-generation waste bug in the notification orchestrator
metadata:
  type: project
---

## What SYSTEM actually is
`feature='SYSTEM'` in `token_usage_log` is NOT a deliberate category for background jobs — it's the
**default fallback** `log_token_usage()` writes (`app/services/usage_tracking.py:212`) whenever an
OpenAI call fires with no `with track_usage(...)` context active. `operation` defaults to `"unknown"`
the same way. Any time a `SYSTEM`/`unknown` cost shows up big in a future audit, the fix is: grep for
`openai_service\.(gpt_structured|gpt_function|generate_embeddings|tts_response|speech_to_text)` call
sites and check each is inside a `track_usage()` block up its call stack — don't assume it's summaries.

`periodic_summary.py` (daily/weekly/monthly/yearly conversation summaries) DOES deliberately label
itself `track_usage("SYSTEM", "generate_daily_summary", ...)` etc. — but as of 2026-08-10 it has ZERO
rows in the last 60d and is **dead code in prod**: not registered in `rq_scheduler_setup.py` or
`main.py` lifespan, not in the Procfile (no clock/cron dyno), last `periodic_summaries` row per
period_type: DAILY 2026-03-06, WEEKLY 2026-03-02, MONTHLY 2026-02-28, YEARLY 2026-01-01. If asked about
"conversation summaries" as a live feature, check this first — it may not be what the user thinks it is.

## The real 93%-of-spend bug (found + partially fixed)
7 files call `generate_moment_text()` → `openai_service.gpt_structured()` with **no track_usage wrapper**:
`app/services/moments/{mood_dip_alert,mood_update_request,post_session_reflection,re_engagement,
therapy_prep,therapy_relationship_checkin}_generator.py` + `app/services/insights/recovery_moment_insight_detector.py`.
All 7 are mine (built in Notification Moments Phase 2/3, see [[notification_moments_phase2_phase3]]).

**Fixed 2026-08-10**: wrapped each in `track_usage("NOTIFICATION", "<op>_text", user_id=...)` — reused
the existing `NOTIFICATION` FeatureEnum value (no migration needed; `operation` is free-text varchar,
only `feature`/`api_type` are native Postgres enums). Labeling only, no logic change. 280 tests pass.
Committed locally (BE main `6b8e05e`), NOT pushed.

**Root cause of the actual $ waste (NOT fixed — flagged as follow-up, needs a dedicated task)**:
`app/services/notification_orchestrator.py::_run_reactive_for_user` (mine) calls `generator.generate()`
— which pays for the LLM call — for **every** `is_eligible()=True` generator, THEN scores and picks one
winner (`candidates.sort(); winner = candidates[0]`, ~line 497-499). Runs hourly (`0 * * * *` cron).
`is_eligible()` mostly checks a business condition unrelated to "was this dedup window already filled"
(e.g. THERAPY_RELATIONSHIP_CHECKIN checks `TherapyHealthCheck`, not `NotificationMoment`), so the same
user can get re-generated (and discarded) AI copy every hourly tick for days. Measured: 155,380
unattributed GPT calls / 60d vs 7,008 persisted `is_ai_generated=true` moments in the same window ≈
**22:1 waste ratio, ~95% of spend never shown to a user**.

**Compounding live bug (confirmed in prod worker logs same day)**: `_persist_moment` (line ~1160)
returns `None` on dedup-collision by design ("skip silently" per its own docstring), but the caller
(line ~516-524) doesn't check for `None` before `moment.id` → `AttributeError`, caught by a broad
except and logged as `"[ORCH] Failed to persist moment for user %s: 'NoneType' object has no attribute
'id'"`. Pulled 1,500 lines of `heroku logs -a mindsync`, found 433 occurrences in a single 4m27s window
(one hourly tick) — this is happening continuously in prod, not historical. Fix is a one-line `if moment
is not None:` guard — cheap, low-risk, but NOT done this session (scoped as a recommendation, not
implemented, since the real fix is restructuring `generate()` to run after winner-selection).

**If asked to implement the actual savings fix**: split `MomentGenerator.generate()` into (a) cheap
rule-based candidate+score (no AI call) and (b) AI-copy rendering, called only for the winner after
`candidates.sort()`. Touches the shared `MomentGenerator` interface used by all 6 competitive/schedule-
driven generators — treat as a medium-effort, coordinated change, run full notification test suite
after. Estimated savings ~$85-105/month at observed run-rate.

## Useful mechanics learned this session
- `settings.GPT_MODEL`, `GPT_MODEL_MINI`, `GPT_MODEL_41_MINI`, `GPT_MODEL_41` all currently alias to
  the SAME model string (`gpt-5.4-mini`, confirmed via `.env` and 100% of prod CHAT_STRUCTURED rows) —
  the "which model tier" question is currently moot in this codebase; don't assume a mini/full split
  exists without checking `.env` / prod `model` column first.
- `TokenUsageLog.feature` is `Column(Enum(FeatureEnum), nullable=False)` — a **native Postgres enum**.
  Any new `track_usage("SOME_NEW_LABEL", ...)` needs `SOME_NEW_LABEL` added to `FeatureEnum` in
  `app/models/models.py` (backend-api's file) via an `ALTER TYPE featureenum ADD VALUE IF NOT EXISTS`
  migration (backend-api's file) — mirror the `HERO_INSIGHT` precedent (migration `uu1v2w3x4y5z`,
  2026-06-21). `operation` is a plain varchar — free to reuse/extend without any migration. This is why
  the cheap fix reused `NOTIFICATION` instead of inventing `MOOD_DIP_ALERT` etc. as new features.
- **Confirmed enum drift, not yet fixed**: `THREAD_CONTEXT` (`app/tasks/thread_context.py:79`) and
  `WEEKLY_OBS` (`app/tasks/weekly_observations.py:152`) are used in `track_usage()` calls but are
  **NOT in `FeatureEnum`** (24 members, neither present) and have no migration. Since
  `log_token_usage()` is fire-and-forget (blanket try/except), every insert for these two labels
  silently fails on Postgres (`InvalidTextRepresentation`) and is swallowed — this cost is invisible,
  not even in SYSTEM. Also: `test_all_track_usage_labels_are_in_feature_enum` in
  `test_featureenum_hero_insight.py` is a **hard-coded snapshot** ("as of 2026-06-21"), not a live grep
  — it will NOT catch future drift of this kind. Handoff to backend-api: add both labels + fix the
  test to grep live instead of using a frozen set.
- `clinician_ai.py` (mine, see [[clinician_ai_implementation]]) has the same unwrapped-call problem as
  the moment generators but wasn't fixed this session — no existing FeatureEnum value fits it cleanly;
  needs a new `CLINICIAN` label + migration from backend-api first.

## Prod DB access mechanics that worked this session
- `heroku run -a mindsync python < script.py` where script.py is `exec(r'''...''')`-wrapped — this
  avoids the REPL indentation/paste problems entirely (the whole multi-line block becomes one `exec()`
  call, parsed as a real module internally, not line-by-line by the REPL). More robust than trying to
  keep every line un-indented per the older recipe note.
- One query batch (~10 queries) against `token_usage_log` (188K+ rows) + a few smaller tables completed
  in under 3 minutes. A second batch of similar size **hung for 20+ minutes with zero output** (likely
  one query against a clinician table, or an unflushed-buffer issue) — had to `heroku ps:stop` it
  manually. Lesson: if a `heroku run python` one-off produces literally zero output after ~5 minutes for
  a batch that should be fast, don't wait indefinitely — check `heroku ps` age, and be ready to kill
  and re-run a smaller/split batch rather than trusting it'll eventually flush.
- `heroku logs -a mindsync -n 1500` (no `--dyno` filter needed, `--dyno run.NNNN` returned nothing even
  for a real dyno — filter by grepping the combined stream instead) is a fast, high-value cross-check:
  live worker logs caught the `_persist_moment` bug in the act, which the DB aggregate alone wouldn't
  have explained as clearly.
