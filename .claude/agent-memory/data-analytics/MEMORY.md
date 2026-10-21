# data-analytics Agent Memory

## Index
- [KE gate rerun 2026-10-19](ke_quality_eval_rerun_2026_10_19.md) - PASSED on 8bd2956 after backend guards; leftovers are judgment calls; forming once per job; script self-contained.
- [KE quality gate 2026-10-19](ke_quality_eval_gate_2026_10_19.md) - first FAIL (safety-plan path, names leak); its wrapper is superseded by the script; $0.0076/story.
- [Reflect summary backfill 2026-10-19](reflect_summary_backfill_2026_10_19.md) - why old Reflect threads lack summaries; script on branch, not run; backdate backfilled rows.
- [Period card endpoint 2026-10-18](period_card_endpoint_2026_10_18.md) - Weekly/Monthly chart+stats API; weekly end exclusive; Realization None->TRUE; tracked test_temp.db.
- [After card progress panel](after_card_progress_2026_10_13.md) - v1 + v2 (10-14): locked<3 sessions, local-day dedupe, PROFILING consent gate (raising check, runs first).
- [Reflect v3.1 therapy progress 2026-10-13](reflect_v31_therapy_progress_2026_10_13.md) — deflection = LIMITS line + advice rule; crisis carve-out needed for data-forward sections; voice eval needs py -3.14.
- [C1 dead instrumentation, backend, 2026-08-10](c1_dead_instrumentation_backend_2026_08_10.md) — inapp_insight.generated stopped 07-23 (not a code diff, unsolved); recording_processing_* only wired to dead Whisper fallback not AssemblyAI primary; prep_card_auto_generated has no live emitter; report_exported removed (commit 0a317e7); weekly/monthly _regenerated intentionally unified via is_regeneration flag, not separate events.
- [SYSTEM AI cost audit 2026-08-10](system_ai_cost_audit_2026_08_10.md) — SYSTEM=track_usage() default fallback not bg jobs; 22:1 waste in notification_orchestrator generate-before-select + live persist-crash bug; periodic_summary.py dead since March; FeatureEnum=native PG enum (operation=free text); THREAD_CONTEXT/WEEKLY_OBS enum drift = invisible cost.
- [PostHog instrumentation patterns](posthog_instrumentation_patterns.md) — shared-emission-point pattern for multi-trigger events, auto-job internal-retry gotcha, test-patching imported names (summaries domain); + "event fired once/never" diagnostic recipe: grep emitters first, git-ancestor for deploy status, DB row counts beat RQ registry sampling (2026-08-10, realizations B5: `realization_detected` only wired to manual tag endpoint, AI auto-detect job silently creates 149 rows with zero emission — handoff to backend-api, not fixed by me, not my files).
- [Lista poprawek 01-07-2026 release](release_2026_07_01_lista_poprawek.md) — encode()-None crash trap, OpenAI structured-output nullability, Python 3.12-vs-3.14 gotcha, boot-check recipe, baseline 4032p/56f (2026-07-02).
- [Prep cards diagnosis 2026-08-10](prep_cards_diagnosis_2026_08_10.md) — auto-gen cron runs forever, 0 rows ever produced (DB proof); manual capture is the only working path; worker INFO logs silently filtered; dead client-side auto-generate endpoint.
- [Known bugs audit 2026-02-23](known_bugs_2026_02_23.md) — TTS_MODEL config bug, key-order bugs, N+1 queries, missing else branches (verify still-present).
- [Notification Moments Phase 2/3 + adaptive scoring](notification_moments_phase2_phase3.md) — push generators, in-app detectors, scoring, 2026-05-15 audit remediation.
- [Notification Orchestrator foundation](notification_orchestrator_foundation.md) — file list, enums, rate limits, test patch gotchas (2026-05-14).
- [Security remediations 2026-05-18](security_remediations_2026_05_18.md) — Clinician AI layer + its security fixes, Hero Insight security fixes.
- [Clinician AI implementation](clinician_ai_implementation.md) — full detail behind the security-remediations summary.
- [Feature implementations 2026-03](feature_implementations_2026_03.md) — Personal Bio, Therapy Health Check, Prep Card auto-gen job internals, AI Card Content Quality Overhaul.
- [Voice + localization fixes](voice_and_localization_fixes.md) — Voice RAG/new-user detection, voice output quality gate, BUG-L04 language naturalness, Polish/7-lang label fix.
- [API contracts](api_contracts.md) — dashboard insight, weekly summaries, character card, monthly audits response shapes.
- [Realizations Collection feature](realizations_feature.md) — detection, hooks, RAG, XP, cross-feature integration.
- [Feature index](features.md) — Pre-Session Prep Card, Prep Reminder, Reflect Chat, Weekly Therapy Summary, Symptom Tracking, Between-Session Notes, Monthly Therapy Audit, Custom Calendar Sessions — one-liners + full schemas.
- [Patterns](patterns.md) — additional endpoint/response-schema patterns not covered above.

## Project Key Facts
- Backend lives at `MindSync/app/` (relative to repo root).
- All schemas in one file: `MindSync/app/schemas/schemas.py`. All CRUD in one file: `MindSync/app/crud/crud.py`.
- `deps.get_current_user` returns `str` (Firebase UID); `async def` but DB session is sync (`Session`). Endpoints use sync `def`.
- Encryption: many DB text fields are Fernet-encrypted — always `decode()` from `app/services/encode_service.py`, wrapped in try/except with fallback.
- `from app.models.models import *` wildcard import used in dashboard.py.
- `ConversationTopicSentiment.conversations_id` (plural) is the FK column name.

## Key Model Notes
- `ConversationTopicEmotion`: conversation_id, emotion_id(FK→Emotion), layer(int), value(int).
- `Emotion.name`(str); join via `ConversationTopicEmotion.emotion_id == Emotion.id`.
- `ConversationTopicSentiment`: conversations_id(FK), value(DECIMAL 3,2).
- `ConversationSummary`: conversation_id(unique), title, summary_short, summary_long (encrypted Text).
- `StatusEnum.FINISHED='FINISHED'` for finished conversations. `InputTypeEnum.AUTO="auto"` for auto-generated records.

## Testing Patterns
- Tests in `MindSync/app/tests/`. Run: `python -m pytest app/tests/ -v` (from `MindSync/`).
- Isolated test apps: `test_app = FastAPI(); test_app.include_router(router, prefix=...)` to avoid Firebase/Redis init.
- DB mocking: `_SmartDb` class dispatching `query()` by inspecting `str(first_arg)` for SQLAlchemy func calls.
- `encode_service` needs `MESSAGE_ENCRYPTION_KEY` env var for tests creating encoded fixtures.
- Windows `rq` fork issue: `_ensure_rq_importable()` helper pattern (see test_realizations.py, test_monthly_therapy_audit.py).

## Dashboard Endpoint Patterns
- `MindSync/app/api/v1/endpoints/dashboard.py`, prefix `/dashboard`.
- `def endpoint_name(param, current_user_id: str = Depends(deps.get_current_user), db: Session = Depends(deps.get_db))`.
- Outer: `except HTTPException: raise` first, then `except Exception as e: raise HTTPException(400, str(e))`.

## Background Job Patterns
- Task files in `MindSync/app/tasks/`; each opens its own `SessionLocal()`, closes in `finally`. All RQ jobs sync. Inner per-item try/except + outer fatal try/except (fatal except only logs — does NOT surface as an RQ failure; DB/registry checks, not logs, are ground truth for "did it actually do anything").
- Scheduler setup in `app/core/rq_scheduler_setup.py`: each `setup_*` creates its own Redis/Scheduler, cancels existing jobs by description, registers via `scheduler.cron(...)`.
- New setup functions must ALSO be called in `app/main.py` lifespan — request from backend-api (they own main.py).
- Imports: `from app.db.session import SessionLocal` (not `app.core.database`); `from app.utils import parse_timezone, utc_now`.
- Therapy schedule utils: `from app.utils.therapy_schedule_utils import compute_next_session_date, parse_schedule, parse_custom_sessions`. Always pass `custom_sessions=parse_custom_sessions(prefs)` to every `compute_next_session_date`/`compute_last_session_datetime` call. This module's date math is tz-aware end-to-end (verified 2026-08-10).
- New task modules: `try/except ImportError` lazy imports inside setup functions (`setup_hourly_weekly_therapy_summary` pattern).
- Diagnosing "does this cron actually run/produce data": tailing Heroku logs is unreliable here — worker log buffer covers only ~8-10 min (high per-user FCM debug volume) and INFO-level app logs may be filtered entirely (confirmed for prep_card_auto_generate, 2026-08-10; check other `app/tasks/*` loggers too). Instead query RQ's `FinishedJobRegistry`/`FailedJobRegistry` (`rq.registry`, queue `default`) filtered by `job.func_name`, and check the actual DB table the job is supposed to write to — that's ground truth.

## Notification Preferences Default Keys
`_DEFAULT_NOTIFICATION_PREFS` in crud.py: `weekly_summary`, `monthly_audit`, `post_session_nudge`, `health_check` all default `True`.
