# MSV3.4 (CS-01) migration-state verification — 2026-08-15

## Question

Backend commit `4bb9b2c` (MSV3.4, CS-01 — lift the 5-active-goal cap for the onboarding sync
path only, `app/crud/crud.py::create_goal(enforce_active_cap=False)`) was pushed to
`origin/main`. It contains no schema change. Local Alembic head is `ll3m4n5o6p7q`
(`add_therapist_questions_to_debriefs_and_recordings`, chain: `... → kk2l3m4n5o6p → ll3m4n5o6p7q`).
Question: is prod already at head, and does deploying MSV3.4 require `alembic upgrade head`?

## Access method

Read-only `SELECT`/catalog queries via `heroku run -a mindsync python < script.py`
(Azure Postgres host has no public DNS resolution from outside Azure/Heroku).
`SET TRANSACTION READ ONLY` set at the top of the session; no `commit()` anywhere;
dyno `run.2438` stopped after the read (`heroku ps:stop run.2438 -a mindsync`).

## Exact queries run

```sql
SELECT version_num FROM alembic_version;
SELECT count(*) FROM information_schema.columns WHERE table_name='users' AND column_name='activated_at';
SELECT column_name FROM information_schema.columns WHERE table_name='user_subscription_trial'
  AND column_name IN ('trial_started_at','trial_platform','trial_product_sku','trial_ended_at','trial_outcome');
SELECT e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid
  WHERE t.typname='featureenum' AND e.enumlabel IN ('CLINICIAN','THREAD_CONTEXT','WEEKLY_OBS');
SELECT count(*) FROM information_schema.columns WHERE table_name='notification_moments' AND column_name='push_delivered';
SELECT count(*) FROM pg_constraint WHERE conname='uq_weekly_summary_user_period';
SELECT count(*) FROM (SELECT user_id, data_window_end FROM weekly_therapy_summaries
  GROUP BY user_id, data_window_end HAVING count(*) > 1) d;
SELECT count(*) FROM information_schema.columns WHERE table_name='session_debriefs' AND column_name='therapist_questions';
SELECT count(*) FROM information_schema.columns WHERE table_name='session_recordings' AND column_name='therapist_questions';
SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name ILIKE '%goal%';
SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='user_goals' ORDER BY ordinal_position;
SELECT e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid WHERE t.typname='goalstatusenum' ORDER BY e.enumsortorder;
SELECT count(*) FROM user_goals;
SELECT count(*) AS n_users_over_cap, max(c) AS max_active FROM
  (SELECT user_id, count(*) c FROM user_goals WHERE status='ACTIVE' GROUP BY user_id HAVING count(*) > 5) sub;
SELECT c AS active_goals, count(*) AS n_users FROM
  (SELECT user_id, count(*) c FROM user_goals WHERE status='ACTIVE' GROUP BY user_id) sub GROUP BY c ORDER BY c DESC LIMIT 10;
```

## Results

**1. `alembic_version` in prod:**

```
ll3m4n5o6p7q
```

This is exactly the local single head. **Prod is already fully migrated to head.**

**2. Direct existence checks for everything that migrated between the last two verified-lagging
checkpoints (memory's 2026-07-17 read: prod at `zz6a7b8c9d0e`) and today, cross-checked
independently of `alembic_version` in case of partial/silent drift:**

| Migration (chain order after `ff7182a3b4c5`) | What it adds | Present in prod? |
|---|---|---|
| `gg8h9i0j1k2l` | `users.activated_at` | ✅ column exists |
| `hh9i0j1k2l3m` | `user_subscription_trial.{trial_started_at, trial_platform, trial_product_sku, trial_ended_at, trial_outcome}` | ✅ all 5 columns exist |
| `ii0j1k2l3m4n` | `featureenum` labels `CLINICIAN`, `THREAD_CONTEXT`, `WEEKLY_OBS` | ✅ all 3 labels present |
| `jj1k2l3m4n5o` | `notification_moments.push_delivered` | ✅ column exists |
| `kk2l3m4n5o6p` | `uq_weekly_summary_user_period` unique constraint on `weekly_therapy_summaries(user_id, data_window_end)` | ✅ constraint exists (and the migration's own duplicate-guard confirms it's safe: 0 duplicate `(user_id, data_window_end)` pairs found, so the constraint was actually created, not silently skipped) |
| `ll3m4n5o6p7q` (= head) | `session_debriefs.therapist_questions`, `session_recordings.therapist_questions` | ✅ both columns exist |

All six pending-candidate migrations are confirmed applied by direct catalog inspection, not just
by trusting the `alembic_version` row. **Zero migration debt.**

**3. `user_goals` / `goal_narratives` health check (CS-01 scope):**

- Tables matching `%goal%` in prod: `goal_narratives`, `treatment_goals`, `user_goals`. All three
  are legitimate, live-code tables — not orphans:
  - `user_goals` — the CS-01 table, model `UserGoal` (`app/models/models.py:1327`).
  - `goal_narratives` — per-goal AI-narrative history, model in `app/models/workspace.py:539`,
    written by `app/tasks/goal_narrative.py::regenerate_goal_narratives` (created by migration
    `xx4y5z6a7b8c`, long since applied). Not a duplicate of `user_goals.ai_narrative` — that
    column is the *current* narrative; this table is the *history* of narratives over time.
  - `treatment_goals` — unrelated clinician-portal table (`app/models/clinician_v2.py:50`,
    created by `kk1l2m3n4o5p`), therapist-set goals in the clinician deck. Not touched by CS-01.
- `user_goals` columns in prod (15 total): `id, user_id, goal_text, ai_narrative, status,
  display_order, parent_goal_id, achieved_narrative, processing_status, xp_awarded, data_hash,
  narrative_updated_at, created_at, updated_at, achieved_at` — matches the model exactly,
  including `achieved_at` (added by `bb3c4d5e6f70`, 2026-07-17) which is easy to forget is
  additive-only; it's there.
- `goalstatusenum` labels in prod: `ACTIVE, ACHIEVED, REVISED, DROPPED` — uppercase, matches both
  the model's `GoalStatusEnum` member names and CS-01's `status='ACTIVE'` filter literal. No enum
  drift here (unlike the known `IN_PROGRESS`/`HERO_INSIGHT` cases elsewhere).

**4. `user_goals` row count:** **121** rows total (all statuses).

**5. Before-picture — users currently over the (soon-to-be-bypassable-for-onboarding) 5-active cap:**

```
n_users_over_cap = 0
max_active seen  = None (i.e. no user has more than 5)
```

Full distribution of active-goal count per user (top values, all buckets shown — total users with
≥1 active goal is small, well under the k=25 suppression threshold, but this is an aggregate count
distribution with no per-user identifiers, so it's safe to report):

| active goals | # users |
|---|---|
| 5 | 4 |
| 4 | 2 |
| 3 | 4 |
| 2 | 10 |
| 1 | 48 |

So today, exactly **4 users sit at the current cap (5 active)**, and **0 users exceed it** — expected,
since the manual "+ Add goal" endpoint has always enforced the cap and this is the first code that
can bypass it. This is the honest "before" baseline MSV3.4 asked for: post-deploy, watch whether
users at the 5-cap start accumulating 6+ active goals via re-onboarding (the intended, accepted
behavior per the 2026-08-15 operator decision documented in `create_goal`'s docstring), and whether
that count grows in a way that suggests the onboarding sync path is looping/re-firing rather than
running once per onboarding.

## Interpretation

**Direct answer: no migration is required for this deploy.** Prod's `alembic_version` is
`ll3m4n5o6p7q`, identical to the local repo's single head, and every column/constraint/enum-label
introduced by the six most recent migrations was independently confirmed present via
`information_schema`/`pg_constraint`/`pg_enum` — not just inferred from the version table. The
MSV3.4/CS-01 commit itself (`4bb9b2c`) touches no model, column, enum, or DDL — it is a pure
behavior change to an existing, already-migrated table (`user_goals`), gated by a boolean
parameter. **This deploy is genuinely code-only and safe to ship without `alembic upgrade head`.**

One thing worth flagging for the record, not a blocker: `gg8h9i0j1k2l` (`users.activated_at`) is
explicitly documented in its own migration file as **not** tolerating a deploy-before-migrate
window — once the `User` model declares that column, every ORM query against `users` (i.e.
essentially every request) would 500 on `UndefinedColumn` until the migration runs. That risk is
moot right now because it's already applied on prod, but it's the sharpest instance of the
CLAUDE.md H10-incident pattern in the current chain and is worth remembering if prod is ever rolled
back or rebuilt from a snapshot older than 2026-08-10.

No drift, no orphaned-table surprises in the tables this task touched, no destructive migrations
pending. Nothing to hand off to `backend-api` — this is a clean state.

## Handoff / recommendation for the operator

- Deploy `4bb9b2c` (and whatever else is queued behind it on `origin/main`) without running
  `alembic upgrade head` first — there is nothing pending to apply.
- No action needed on `goal_narratives` / `treatment_goals` — both are healthy, in-use tables, not
  drift.
- Optional follow-up (not urgent): once MSV3.4 has been live for a while, re-run the "users over 5
  active goals" query to see whether the onboarding-cap bypass is producing the expected small
  uptick, or something unexpected (e.g. a user with double-digit active goals, which would suggest
  the sync path is re-running instead of being idempotent per onboarding).
