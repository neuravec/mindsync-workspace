# Backend API Agent Memory

## Migration Chain
- 2026-10-19: origin/main head m320c4a5r6d7; integration/redesign-v3 adds ke_a7c3e9f1b2d4 on it (single head). Verify with `py -3.12 -m alembic heads`. History: [patterns_backend_detailed.md](patterns_backend_detailed.md)

## Topic Files
- [KE team full-history backfill (2026-10-19)](project_ke_team_backfill_2026_10_19.md) - b694937 unpushed; reset-to-forward read beats hist_*; local `py -i <` REPL recipe
- [PostHog identify set_once fix (2026-10-19)](project_posthog_identify_set_once_fix_2026_10_19.md) - 75d1f0d unpushed; backend person props never flowed since 04-25; py3.12 no posthog, py3.14 has 7.x
- [KE rollout + premium history (2026-10-19)](project_ke_rollout_premium_history_2026_10_19.md) - 41f3153+87bad96 feat/ke-rollout unpushed; plan in cursors JSON; weak Orca-therapy moments
- [KE backfill recon (2026-10-19)](project_ke_backfill_recon_2026_10_19.md) - state of origin/main 1045891; superseded by the rollout branch
- [FW reminder follows Main 8-step plan (2026-10-19)](project_fw_reminder_main_plan_2026_10_19.md) - 1045891 pushed; route section=first_week_plan; quota/defer no longer rules
- [KE review round 2: ART9 purge, no-store, daily cap (2026-10-19)](project_ke_review_round2_art9_purge_2026_10_19.md) - 40be9b0..1c6bf3c pushed; growing_skill grants ART9; don't reuse first-week NoStoreRoute
- [KE review fixes: crisis, Art. 9, person-less (2026-10-19)](project_ke_review_fixes_crisis_art9_personless_2026_10_19.md) - f1c14dd; art9_consent_state for permanent skips; 409 ideas_paused; ART9 purge residual closed in round 2
- [Redesign v3 BE integration (2026-10-19)](project_redesign_v3_be_integration_2026_10_19.md) - 5915719 on d79c509; unset worktree upstream; local SQLite DDL fails x7 are base; autogenerate would drop 5 clinician tables
- [Cards v3 Timeline previews (2026-10-18)](project_cards_v3_timeline_previews_2026_10_18.md) - 7c69c66; composed 7-locale rows via ai_language; FE line removal open; NR%4 group-1 baseline 57 fails
- [MC v3 BE-2 recap gate + last7 + entry_count (2026-10-18)](project_mc_v3_be2_recap_gate_2026_10_18.md) - job gate too, TTL 29d, rhythm null <day 7, recordings cap 3, day-7 reminder residual
- [MC v3 /first-week/steps BE-1 (2026-10-18)](project_mc_v3_first_week_steps_be1_2026_10_18.md) - 34547d1 feat/main-v3; wire-set literal grep trap; session done_at=anchor; /plan side effects stay
- [KE privacy review fixes (2026-10-18)](project_ke_privacy_review_fixes_2026_10_18.md) - 0906e23; KE off by default, opt-in PROFILING, source_present purge, activation on first open
- [KE character KD v2 BE1 (2026-10-18)](project_ke_character_kd2_be1_2026_10_18.md) - 7 ke_* tables, ke_a7c3e9f1b2d4 on m320, /gamification/ke; underscore rev-id regex trap
- [Charsheet consent lock (2026-10-14)](project_charsheet_consent_lock_2026_10_14.md) - default-on, locked 200, /character_sheet/consent; lock check raises (not fail-closed)
- [KD character sheet backend (2026-10-13)](project_character_sheet_kd_2026_10_13.md) - m320c4a5r6d7 off m318 (m319 collision risk), silent first-read sync, orca_xp_breakdown
- [WP-0 M-1 person-less moment events (2026-10-08)](project_wp0_m1_personless_moment_events_2026_10_08.md) - every posthog_track_moment needs account_anchor; wall-clock test gotcha
- [WP-0 first-week push cap (2026-10-08)](project_wp0_first_week_push_cap_2026_10_08.md) - enforce_daily_push_cap; `.env` is TRACKED (never rm in worktree)
- [H-4 neutral push allowlist (2026-10-08)](project_h4_neutral_push_allowlist_2026_10_08.md) - send_templated_push; notification_logs.title = template key
- [WP-0 time zones (2026-10-08)](project_wp0_time_zones_2026_10_08.md) - parse_timezone stays pytz; resolve_tzinfo/local_date_at for new code
- [Profile re-run null-overwrite fix (2026-10-05)](project_profile_rerun_null_overwrite_2026_10_05.md) - PUT identity null ignored, "" clears; upsert_user_preferences lang/tz trap
- [Receipt fail_reason/retryable (2026-10-03)](project_receipt_retryable_outcome_2026_10_03.md) - retryable=false ONLY for terminal transaction states
- [Reflect entry flow (2026-09-17)](project_reflect_entry_flow_2026_09_17.md) - ORM `deferred` columns survive Heroku push-then-migrate; ThreadPoolExecutor ctx-manager defeats timeout
- [RE_ENGAGEMENT no-push-target skip (2026-09-13)](project_re_engagement_no_push_target_2026_09_13.md) - has_no_push_target() only; MagicMock vs real User activated_at fixture gotcha
- [MSV3.11 CS-11 notification audit (2026-09-02)](project_msv311_cs11_notification_audit_2026_09_02.md) - grep `if not schedule and not custom_sessions` for recurrences; _process_first_nudges dead
- [MSV3.11 CS-10 therapy schedule fix (2026-09-02)](project_msv311_cs10_therapy_schedule_backend_2026_09_02.md) - omitted `schedule` = untouched; `_localize_naive` for DST-safe occurrences
- [MSV3.10 CS-02 add-therapy-date push (2026-09-01)](project_msv310_cs02_add_therapy_date_investigation_2026_09_01.md) - clear-guard must check OLD frequency; read full specialist reports
- [cancel_active_moments_by_type pattern](patterns_cancel_active_moments_by_type.md) - reuse EXPIRED + scoring_signals marker; use len(x)==0 not `not x` with mocked db
- [granted_via paywall fix (2026-08-17/18)](project_granted_via_paywall_fix_2026_08_17.md) - migration-only then code commits; response_model drops undeclared keys; psycopg2 date bug
- [MSV3.4 CS-01 onboarding goal sync (2026-08-15)](project_msv34_cs01_onboarding_goal_sync_2026_08_15.md) - per-goal-text dedup; create_goal(enforce_active_cap=False); CRUD never enqueues RQ
- [C1-BE worker PostHog init (2026-08-10)](project_c1_be_telemetry_worker_posthog_init_2026_08_10.md) - RQ resolves func.__module__: wrapper must be DEFINED under app.tasks
- [FeatureEnum B18 (2026-08-10)](project_featureenum_b18_cost_audit_fix_2026_08_10.md) - enum ADD VALUE in autocommit_block; clinician_ai.py ownership header conflict
- [Prep-card zero-rows + worker logging (2026-08-10)](project_prep_card_zero_rows_logging_fix_2026_08_10.md) - app/core/logging_config.py from main.py and app/tasks/__init__.py
- [Activation check-and-set (2026-08-10)](project_activation_user_activated_2026_08_10.md) - users.activated_at atomic UPDATE...WHERE in shared helpers
- [MSV3.2 Fix.1 G-fix (2026-07-17)](project_msv32_fix1_gfix_2026_07_17.md) - legacy add-to-agenda BC, toggle on /agenda-pin; FE follow-up open
- [Notification Cadence v3 legacy cleanup](notification_cadence_v3.md) - removed flag/jobs (2026-07-03), what was kept
- [Offline verification recipes](offline_verification.md) - Alembic + `import app.main` on Windows without Postgres/Redis
- [Notification service patterns](notification_service_patterns.md) - DND/timezone helpers, FeatureEnum drift, Art.9 soft-gate
- [Recording pipeline](recording_pipeline.md) - chunked upload, GCS/Postgres storage, Whisper, recovery jobs
- [PostHog api_error classification (2026-08-10)](posthog_api_error_classification.md) - `is_expected` tagging; dependency-free classifier module
- [Detailed patterns + baseline history](patterns_backend_detailed.md) - check-and-set, chain-tip tests, psycopg2 date rule, object_session on MagicMock

## Key Patterns
- SQLAlchemy sync sessions (SessionLocal). Auth: `deps.get_current_user` returns Firebase UID string
- `award_user_track_points(xp_flag=...)`: separate idempotency keys (`viewed_xp_awarded` for view awards); SessionPrepCard has both columns
- Soft-delete `deleted_at` on SessionDebrief, BetweenSessionNote, SessionPrepCard, Realization, SessionRecording; queries filter `deleted_at.is_(None)`; deduct_* clears xp_awarded
- Soft-deleting a debrief flags `needs_regeneration` on overlapping weekly/monthly summaries; hourly run clears it
- Timeline: cursor pagination (ISO datetime), 8 item types. Purge job hourly :30 (deleted_at > 24h, 5 types + RAG docs)
- Encrypted fields: `encode()`/`decode()` from `app.services.encode_service`
- New routers: guarded try/except import in api.py. Scheduler jobs: cancel by description before re-registering
- Grep the Flutter repo before changing a response shape (old builds are consumers)
- Atomic check-and-set: UPDATE ... WHERE flag IS NULL, rowcount==1 wins (details in patterns file)
- Extend the shared helper instead of editing every call site
- Landing a migration: update chain-tip tests and run the full suite (details in patterns file)

## Test Patterns
- Never `patch(..., create=True)` on a module other suites replaced with MagicMock (e.g. app.core.rq_queue): exit deletes the attr. Patch your own wrapper (2026-10-18)
- Parallel subagents share one scratchpad: unique file names. Base-vs-branch comparisons: throwaway `git worktree add --detach`, never `git stash` (shared refs/stash)
- users router has no prefix: mount with `prefix="/users"`. test_scheduler_idempotency before test_user_memory::TestFirstConversationConfig breaks it (base too)
- Windows: rq import fails (fork), mock via sys.modules (`ke_pipeline_support.ensure_rq_mocked`); task files importing rq_queue need it too
- MagicMock(spec=Model): set ALL new columns explicitly; schema field-set tests need updating on new fields
- New db.query() in an endpoint helper: patch it in tests that use `db = MagicMock()`
- DetachedInstanceError: save `.id` to locals before the function under test commits/closes
- Baseline: ~9 pre-existing full-suite fails (2026-10-05), split into 4 groups; py3.12 local SQLite also fails 7 migration DDL tests on base (2026-10-19). Confirm on a throwaway base worktree before calling a regression
- Never `import app.main` under pytest (dummy FIREBASE_CREDENTIALS); verify main.py via source/AST. Bare import outside pytest also fails here (needs DB_URL, MESSAGE_ENCRYPTION_KEY): use conftest exec + rq mock + firebase patch
- Whisper tests: patch `session_recordings._assemble_chunks_from_pg` (None); `redis_audio=b"\x00"*1000`
- PII asserts: never `"transcript" not in str(props)` ("transcription_provider" matches)
- Workspace endpoint tests: bare FastAPI + workspace router, real in-memory SQLite, cross-user 404 instead of 401
- Date/datetime processing in migrations: pure function tested with real `date()` objects; SQLite round-trip is blind to psycopg2 types
- pytest dirties tracked `test_temp.db`: `git checkout -- test_temp.db` before committing
- [PostHog person props gated on consent (2026-10-19)](project_posthog_person_props_consent_2026_10_19.md) -- b6074de, not pushed; weekly premium_intent consented-only + flush; POST /users/ identify still ungated (needs redesign)
- [Local py has no posthog package](reference_test_env_posthog_not_installed.md) -- 2 worker-import probes fail on any branch; fake `_client` pattern; MagicMock db passes consent
