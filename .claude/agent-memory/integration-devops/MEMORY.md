# Integration-DevOps Agent Memory

## Project Structure

- Backend: `MindSync/` – FastAPI on Heroku, Python 3.12.2
- Frontend: `mindsync-frontend/mindsync_app/` – Flutter 3.27.0
- Router registration: `MindSync/app/api/v1/api.py` – all routers registered here
- API contract docs: `MindSync/app/docs/` (created 2026-02-22)

## Auth Pattern

- All endpoints require Firebase Bearer token → 401 if invalid
- Premium gate returns 403 (NOT 401) – Flutter must route these differently
- Premium check uses `crud.get_user_subscription()` + `is_premium()` helper from therapy_service, or direct DB query in character card endpoint

## Known API Contracts Verified

### Therapy Companion + Character Card (2026-02-22)

Contract doc: `MindSync/app/docs/therapy_character_card_api_contract.md`

Key discrepancies found vs. plan:
- `session_state` has 4 values: UPCOMING, PREP, DEBRIEF, PAST (plan only showed one example)
- `GET /therapy/next_session` requires premium – plan was silent on this
- `emotional_delta` direction has 3 values: "up", "down", "neutral" (plan omitted "neutral")
- `emotional_delta` returns up to 4 items, not 2 (plan showed 2-item example)
- In locked character card, `xp` IS still populated – only radar_stats/therapeutic_alliance/emotional_delta/computed_at are null
- DELETE returns 204 No Content – empty body, do not parse

## Pydantic v2 Behaviour (affects all contracts)

- Optional fields with `= None` are serialized as JSON `null` (not omitted)
- datetime fields serialize as ISO-8601 with timezone offset (e.g. `+00:00` not `Z`)
- `model_config = ConfigDict(from_attributes=True)` needed for ORM model validation

## Deployment Notes

- Heroku Procfile: web (uvicorn), worker (rq), scheduler (rqscheduler)
- Backend deploys FIRST when changes are dependent
- Migrations: `heroku run alembic upgrade head` after every deploy with schema changes
- [FE push to dev via temp worktree](reference_fe_dev_push_via_worktree.md) - Codemagic bot commit makes dev merge-not-ff; worktree recipe; analyze uses `error -` not `error •`
- [First voice conversation FE deploy 2026-10-05](project_first_voice_conversation_fe_deploy_2026_10_05.md) - dev e4e0d05, 0031c44 (2.0.101 bump 0615f3e), then backfill 86addde; bumps can take 20+ min; device QA open
- [Recap voice floor deploy 2026-10-06](project_recap_voice_floor_deploy_2026_10_06.md) - Heroku v563 (main 76d5c09, no migration) + FE dev f4afaa6 (2.0.105); user_turns meaning changed; device QA open
- [Heroku CLI + one-off smoke recipe](reference_heroku_oneoff_smoke.md) - HEROKU_API_KEY from ~/_netrc, REPL-safe script ending exit(), timeout wrapper, log window ~10 min
- [Redesign integration 2026-10-14](project_redesign_integration_2026_10_14.md) - DEPLOYED: BE v572 (4c7675b) + m319/m320, FE dev 5c27b2c; device QA open
- [KE rollout 2026-10-19](project_ke_rollout_deploy_2026_10_19.md) - v575 (73081cc) + v576 KE on (operator set it); both backfills done; first sweep ok

- [GA4 + ASC + Play pull scripts 2026-10-22](reference_ga4_revenue_pull_scripts.md) - scripts/ga4, scripts/revenue; deps; unverified API details to check on first run

## PostHog Dashboard Rebuild (C4, 2026-08-10)

- Updated `scripts/posthog_build_dashboards.py` (not run — operator decision) to reflect the drifted taxonomy; full report `analytics-reports/2026-08-10-dashboards-rebuild-plan.md`.
- [$lib verification before hygiene filters](reference_posthog_dashboard_rebuild_lib_verification.md) — never infer client/backend origin from filenames/comments; verify per-event with a fresh `(event, $lib, count)` query. Caught a live misclassification (`notification_received`) and two dual-sourced events (`subscription_purchase_completed`, `consent_granted`) this way.
- Script gained `--update` (PATCH existing insights by name instead of skip) and `--retire-dead` (opt-in soft-delete of superseded-by-rename insights) flags — without `--update`, re-running the idempotent script against already-built dashboards is a no-op.

## Codemagic / Play Publishing

- [Play internal testing auto-rollout](codemagic_play_internal_testing.md) – 2026-07-03: `submit_as_draft` flipped true→false in app-release; safe due to no-triggering-block dispatch-only design + monotonic build numbers; commit c26353c pushed to origin/dev

## Critical Infrastructure Issues (Audit 2026-02-23)

### Security Violations
- Real Firebase service account JSON at `MindSync/app/mindsync-8f534-839e8464e684.json` – NOT gitignored
- `MindSync/.env` contains real Azure AD and OpenAI credentials – NOT gitignored (only `.venv`, `*.pyc`, `__pycache__` ignored)
- Slack webhook URL hardcoded in `mindsync-frontend/codemagic.yaml` line 100
- `MindSync/.env.example` does not exist – `.env` is the only reference

### Environment Variable Split (CRITICAL)
- `app/db/session.py` uses `os.getenv("DB_URL")` – NOT managed through Pydantic Settings
- Pydantic Settings (`app/core/config.py`) loads `DATABASE_URL` – never used for actual DB connection
- `REDISGREEN_URL` used via `os.getenv()` in rq_scheduler_setup.py, redis.py – NOT in Pydantic Settings
- Both DB_URL and REDISGREEN_URL must be set as Heroku Config Vars separately from Settings vars

### Unpinned Dependencies
- `fpdf2`, `celery`, `redis`, `rq`, `rq_scheduler`, `pytz` are all UNPINNED in requirements.txt

### Docker Mismatch
- `MindSync/Dockerfile` uses `FROM python:3.11` but project uses Python 3.12.2
- `Dockerfile CMD` runs `gunicorn main:app` from `/code/app` – module path wrong (should be `app.main:app`)

### Flutter delete account bug
- `UsersManager.deleteAccount()` calls `Endpoints.firstDayOfWeek` (`/api/v1/users/profile/first_day_of_week`) instead of `Endpoints.deleteAccount` (`/api/v1/users/settings/account`)

### Nullable mismatch: UserInfo.subscriptionIsActive
- Backend: `UserProfileResponse.subscription_is_active: Optional[bool] = None`
- Flutter `UserInfo`: `subscriptionIsActive` cast as `bool` (non-nullable) – will throw if null

### Contract Status
- `/api/v1/gamification/journey_summary` – VERIFIED OK (JourneyModel matches JourneySummaryResponse)
- `/api/v1/dashboard/conversation/{id}/insight` – VERIFIED OK (ConversationInsightModel matches)
- `/api/v1/users/preferences` – MISMATCH: backend returns id+user_id, Flutter UserPreferences only expects ai_language+time_zone (works but drops extra fields – not a crash)
- Therapy/CharacterCard endpoints: source files missing from `app/` (only .pyc in __pycache__) – feature may be on different branch

## Flutter pubspec.yaml Dependency State (2026-02-26)

### Current pinned/upgraded versions (vs original)
- `sdk`: was `3.6.0` (exact pin) → now `'>=3.6.0 <4.0.0'`
- `flutter`: was `3.27.0` (exact pin) → now `'>=3.27.0'`
- `intl`: was `^0.19.0` → now `^0.20.0` (flutter_localizations pins to 0.20.2)
- `syncfusion_flutter_charts/gauges`: was `^27.2.5` → now `^28.2.9` (27.x required intl <0.20.0)
- `flutter_bloc`: was `^8.1.5` → now `^9.1.1` (needed for bloc 9.x compat)
- `freezed` (dev): was `^2.5.7` → now `^2.5.8` (2.5.8 uses analyzer 7.x, avoiding _macros issue)
- `json_serializable` (dev): was `^6.9.0` → now `^6.9.2`
- `bloc_test` (dev): COMMENTED OUT – cannot coexist with freezed 2.x + openai_realtime_dart

### Critical known incompatibility (UNRESOLVED)
`bloc_test` (any version) + `freezed 2.x` + `openai_realtime_dart` is an unsolvable triangle:
- `bloc_test` + flutter_test + openai_realtime_dart forces `test >=1.29.0`
- `test >=1.29.0` requires `analyzer >=8.0.0`
- `freezed 2.x` (all versions) requires `analyzer <8.0.0`
- Resolution requires upgrading to `freezed 3.x` (requires flutter-mobile to update app source)
- See `mindsync-frontend/mindsync_app/pubspec.yaml` comments for restore instructions

### Freezed 3.x migration notes (for flutter-mobile)
Breaking changes in freezed 3.x vs 2.x:
1. Classes must be `abstract`, `sealed`, or manually implement `_$MyClass`
2. `when/map` methods removed – use Dart native pattern matching instead
3. Collections become unmodifiable by default (disable per-class: `@Freezed(makeCollectionsUnmodifiable: false)`)
4. `freezed_annotation` bumps to 3.1.0 (pinned exact in freezed 3.x)

### Scheduler Notes
- All periodic jobs registered via `rq_scheduler` cron – duplicate job registration on each server restart (cancel+re-register pattern)
- `setup_weekly_jobs()` uses module-level `scheduler` not new Redis conn – inconsistent with other setup functions
- `timeout=None` on several long-running jobs is acceptable but means stale jobs never expire
- `clear_all_scheduled_jobs()` called at lifespan start before re-registering – fixes 531-job prod accumulation bug

## PostHog Metrics Hygiene (C2/C3, 2026-08-10)

- Direct access confirmed: `python scripts/posthog_query.py` works from this agent too (not just posthog-data-extractor) – `.env` creds shared, read-only, no need to delegate simple HogQL checks.
- Canonical app/web split filter (`properties.$lib`) + internal-traffic exclusion (`$is_testflight`/`$is_emulator != true`) verified fresh and written to `posthog-data-extractor`'s memory: `.claude/agent-memory/posthog-data-extractor/reference_default_exclusion_filters.md`. Key gotcha: `$is_testflight` only has ~24% event coverage on current builds (async/session-timing gap, root cause undiagnosed) – treat any `$is_testflight=true` count as a floor, not precise.
- No GA4 access exists anywhere in this environment: `.env` has no GA4/Google Analytics keys, no gcloud, no service-account JSON, and the `seo-google` skill has no configured credentials (`~/.config/claude-seo/google-api.json` absent, scripts dir not installed). GA4 historical pull for `G-DWNVZNWCT5` (marketing site) is an OPERATOR task – do not attempt OAuth setup from an agent session. See `analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md` for the exact export instructions handed to the operator.
- Full report: `analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md`.

## MSV3.13 CS-01 diagnosis (2026-09-03)

- [Your Session card stuck after After Therapy](project_msv313_cs01_diagnosis_2026_09_03.md) - root cause: `debriefMatchesSession` (FE) / `_debrief_matches_session` (BE, dead code) reject any After Therapy submitted >48h after the session; debrief's `sessionDate` is stamped `DateTime.now()` at submission, never the real session date. Both sides' own tests assert the 48h ceiling as intended - why 2 earlier "fix" rounds missed it. Report: `Business_requirements/MS_3/v3.13/CS01_DIAGNOSIS.md`.

## Async Recording Pipeline (2026-06-21)

- `POST /upload/{id}/complete` is now ASYNC: creates session_recordings row immediately (Timeline instant), enqueues `process_session_recording_whisper` RQ job. Returns `RecordingStatusResponse` (id, processing_status, created_at).
- New safety-net job `finalize_complete_upload_sessions` runs every 15 min (cron `5,20,35,50 * * * *`), registered at lifespan via `setup_frequent_upload_finalizer()` – defensive ImportError guard.
- Contract VERIFIED PASS. One minor observation: `ChunkedUploadManager` sends `content_type: 'audio/wav'` but backend schema defaults to `'audio/m4a'` – cosmetic, non-breaking, low-priority cleanup.
- Runbook: `MindSync/docs/RUNBOOK_recording_pipeline_fix.md`
- This is a code-only deploy – migration `tt0u1v2w3x4y` already run 2026-06-21. No `alembic upgrade head` needed.
- `GCS_BUCKET_NAME` already set to `mindsync-8f534.firebasestorage.app` (set 2026-06-21).
- PostHog flag `recording_pipeline_v2`: controls recording UI path. Recovery is flag-independent when manifest has entries.
- UploadSession model uses `String(32)` column + `UploadSessionStatusEnum(str, Enum)` – avoids Postgres native-enum drift boot-crash pattern.
- [Heroku boot verification](reference_heroku_boot_verification.md): release timings, 27-job scheduler check, log-buffer snapshotting, benign noise
