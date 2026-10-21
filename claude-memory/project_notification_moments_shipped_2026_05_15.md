---
name: project-notification-moments-shipped-2026-05-15
description: "Notification Moments redesign shipped end-to-end (4 fazy, ~695 testów). Hard cutover legacy zrobiony, 4 push generators + 5 in-app detectors + adaptive scoring + redesigned Settings działają w prod."
metadata: 
  node_type: memory
  type: project
  originSessionId: 0440417d-53d8-4f1f-9b47-3c74e8e8e8aa
---

# Notification Moments — SHIPPED 2026-05-15

Zakończony multi-faza redesign systemu notyfikacji. Plan w [[project_notification_moments_redesign_2026_05_14]]. Started z audytem który znalazł 3 P0 bugi (fix'nięte) + 7 P1/P2. Po 4 fazach implementacji system w produkcji.

**Why:** stary system był scheduler-driven push z hardcoded textem o 22:00 dla wszystkich; user nazwał "irytujące". Cel: każda notyfikacja = AI-personalized lub templated z dynamic data, smart timing per-user, w-app micro-popupy dla WOW effect.

**How to apply:** wszystkie nowe notyfikacje (push + in-app) idą przez orchestrator/detector framework. Nie dodawać hardcoded jobów. Dodawanie nowego typu = nowy generator/detector pluggable do framework.

## Architektura w prod

### Tabele DB
- `notification_moments` (migracja `ff6g7h8i9j0k`): id, user_id, moment_type (8 enums), status (6 states), push_title, push_body, payload JSON, deep_link_route, scoring_signals JSON, is_ai_generated, scheduled_at, sent_at, opened_at, dismissed_at, acted_at, expires_at
- `app_insights_shown` (ta sama migracja): id, user_id, insight_type (6 enums), form_factor (3: TOAST/INLINE_BANNER/BOTTOM_SHEET), title, body, payload JSON, cta_label, cta_route, dedup_key UNIQUE, is_ai_generated, generated_at, shown_at, dismissed_at, acted_at, expires_at
- `user_preferences` (migracja `gg7h8i9j0k1l`) dodała 3 pola: `notification_enabled BOOLEAN`, `notification_intensity INTEGER 0/1/2`, `notification_interests JSON[6 categories]`

### FCM delivery (CRIT-01 remediacja — kluczowe)
- `app/tasks/notification_orchestrator_job.py` `deliver_due_moments()` — job co 15 min: `get_moments_due_for_delivery` → `claim_moment_for_delivery` (atomic PENDING→SENT) → `send_fcm_to_all_user_tokens` z data payload {moment_id, deep_link_route}. Claim PRZED send = idempotent na RQ retry. `setup_frequent_moment_delivery()` wpięty w `main.py` lifespan.
- Orchestrator (hourly) TWORZY momenty PENDING; delivery job (15 min) WYSYŁA. Dwa osobne joby.

### Timing — UWAGA: fixed-window, NIE adaptive
- Mimo wcześniejszych założeń: timing to **fixed engagement window 10-19 local**, NIE adaptive per-user learning z PostHog. Adaptive timing to future work (HIGH-02 z audytu). Nie zakładać że istnieje.

### Backend services
- `app/services/notification_orchestrator.py` — `NotificationOrchestrator` singleton z scoring layer: base_score × dismissal_downweight × action_rate_boost. Interest filter + intensity respect + DND quiet hours adjustment.
- `app/services/in_app_insight_detector.py` — `InAppInsightDetector` z trigger routing (6 InsightTrigger values), per-session rate limit (1/30min, 0/60min after BOTTOM_SHEET), dedup_key based
- `app/services/notification_categories.py` — moment/insight type → category mapping (6 categories)
- `app/services/moment_text_generator.py` — AI helper via `gpt_structured` (GPT_MODEL_41_MINI), supports 7 languages + 5 tone archetypes

### Push moment generators (4)
- `PostSessionReflectionGenerator` (base_score 9.0, AI) — debrief w 26h
- `MoodDipAlertGenerator` (8.0, AI) — 3 high scores in row, anti-spam 5d
- `PatternInsightGenerator` (7.5, AI) — recurring topic 3+ w 14d, anti-saturate 14d
- `StreakCelebrationGenerator` (7.0, TEMPLATED) — milestone 3/7/30/100/365

### In-app insight detectors (5)
- `RevealInsightDetector` (TOAST, templated) — STATS_TAB_OPENED, ±20% delta week-over-week
- `CelebrateTeaseInsightDetector` (INLINE_BANNER, templated) — APP_OPENED/DEBRIEF_SAVED/NOTE_ADDED, streak 2/6/29
- `NoticeInsightDetector` (INLINE_BANNER, templated) — APP_OPENED, best_time_of_day / most_active_day
- `RecoveryMomentInsightDetector` (BOTTOM_SHEET, AI) — STATS_TAB_OPENED/APP_OPENED, symptom score recovery
- `ComparativeInsightDetector` (TOAST, templated) — DEBRIEF_SAVED/NOTE_ADDED, cumulative milestone

### API endpoints
- `GET /api/v1/moments/upcoming` → moment | null
- `POST /api/v1/moments/{id}/{opened,dismissed,acted}` 204
- `GET /api/v1/insights/pending` → list
- `POST /api/v1/insights/trigger` z trigger_type + context → {created_count}
- `POST /api/v1/insights/{id}/{shown,dismissed,acted}` 204

### Frontend (Flutter)
- 3 reusable widgety: `MomentBottomSheet`, `InsightToast` (BotToast), `InlineNoticeBanner`
- 7 type-specific renderers: `PostSessionReflectionSheet`, `MoodDipAlertSheet`, `StreakCelebrationSheet`, `PatternInsightSheet`, `NoticeBannerRenderer`, `ComparativeToastRenderer`, `RecoveryMomentSheet`, `RevealToastRenderer`, `CelebrateTeaseRenderer`
- `MomentsCubit` ze `loadOnAppOpen()`, `onTrigger(type, context)`, status mutators
- Trigger hooks w existing flows: app_open, debrief_save, note_save, symptom_log, stats_tab_open, therapy_tab_open
- Deep-link `/moment/:id` route w GoRouter
- Settings UI: 11 togglei → master toggle + intensity slider (0/1/2) + 6 interest chips

### Localization
7 języków (en/de/fr/nb/sv/es/pl) — ARB keys: `moments_*`, `insights_*`, `notifSettings_*`

## Hard cutover legacy

`settings.notification_legacy_jobs_enabled: bool = False` (default flipped 2026-05-14).

Usunięte (Faza 4):
- 4 scheduler entries: `setup_hourly_post_session_nudge`, `setup_hourly_symptom_tracking_reminder`, `setup_hourly_mid_week_check_in`, `setup_hourly_pre_session_check_in`
- 3 schema fields: `between_sessions`, `streaks`, `milestones` (zombie preferences)
- 13 Flutter state fields (zombie SettingsLoadedState toggles)
- 27 ARB keys × 7 locales = 189 deletions
- `NotifToggleLegacy` widget (108 LOC)
- 1 cubit method (`toggleNotification(...)` 11-case switch)

Zachowane jako tombstones (data generation poza notifications):
- `generate_weekly_therapy_summaries` (data dla UI)
- `generate_monthly_therapy_audits` (data)
- `notify_health_check_due` (3 P0 gates dodane 2026-05-14, używane w fallback)

## Adaptive scoring

`NotificationOrchestrator.select_moment_for_user`:
- 0.5× downweight gdy ≥3 dismissals tego moment_type w 7d
- 1.5× boost gdy action_rate ≥ 0.6 w 30d (sent_count ≥ 3 jako minimum samples)
- Interest filter: jeśli moment_type.category nie w user.notification_interests → skip
- Intensity 0 → no push generated (only in-app insights)
- Intensity 1/2 → max 1/2 per day
- DND quiet hours: scheduled_at pushed to after DND end

## P0 bugfixy z audytu (2026-05-14, przed Fazą 1)

1. ✅ Frontend: `FCMTokenService.reset()` + `signOut()` wiring (`fcm_token_service.dart`, `main_page_cubit.dart`)
2. ✅ Backend: `health_check.py` fallback — 3 gates (`is_banner_suppressed` + 30d window + 14d activity)
3. ✅ Backend: `add_fcm_token` LRU rotation zamiast Exception

## Code audit (devils-advocate 2026-05-15) — werdykt BLOCK, w pełni remediowany

Audyt znalazł 5 CRITICAL + 10 HIGH. Wszystkie naprawione:
- **CRIT-01**: system NIE wysyłał push (orchestrator tworzył PENDING, nic nie wysyłało FCM). Naprawione: `deliver_due_moments()` job.
- **CRIT-02**: duplikat Alembic revision ID `ff6g7h8i9j0k`. Naprawione: notification_moments migracja przeniesiona na `hh8i9j0k1l2m`, chain linearny.
- **CRIT-03**: brak unique constraint → duplikaty momentów. Naprawione: `dedup_key` kolumna + `UniqueConstraint(user_id, dedup_key)` (migracja `ii9j0k1l2m3n`).
- **CRIT-04**: delivery nie idempotentna. Naprawione: `claim_moment_for_delivery` atomic claim + RQ Redis lock.
- **CRIT-05**: interest backfill wyłączał kategorie. Naprawione: wszyscy backfilled z 6 kategoriami (master toggle to on/off, interests to nowy opt-out).
- HIGH-03 timezone abbreviations (CET/EST/PST → IANA), HIGH-05 crisis-safety clause w prompcie, HIGH-06 terminal-state precedence guard, HIGH-09 rollback przywrócony (legacy setup_* za flagą), HIGH-10 `GET /moments/{id}` endpoint, etc.
- Final: 682/682 backend notification testów pass, deterministyczne; 40/40 frontend.

## Pozostałe P1 do dorobienia (nie scope tego sprintu)

- iOS APNS retry on null token (TODO comment w `fcm_token_service.dart:79`)
- DELETE `/api/v1/users/fcm_token` endpoint przy logoucie (backend nadal go nie ma — frontend gotowy konsumować)
- Backend logging gdy user has 0 FCM tokens (silent failure currently)
- PostHog events dla token registration + permission denied (frontend analytics)
- Migracja DROP COLUMN dla zombie UserPreferences kolumn DB (`between_sessions`, `streaks`, `milestones`) — bezpieczniej na osobne sprzątanie
- **Pre-existing bug (NIE z redesignu)**: `crud.get_users_eligible_for_notification()` ma `str.format()` KeyError bug — legacy kod, qa-testing wykrył przy okazji
- `_actionTaken` dead field w `moment_bottom_sheet.dart` — HIGH-06 działa przez `result == null` mechanizm, pole zbędne (lint warning)
- Adaptive per-user timing (HIGH-02) — obecnie fixed-window 10-19; prawdziwy adaptive to future feature

## Statystyki testów

- Faza 1: 79 (backend models/CRUD) + 79 (orchestrator/endpoints) + 36 (Flutter widgets/Cubit) = **194**
- Faza 2: 38 (legacy guards/trigger hooks) + 89 (generators/detectors registration) + 61 (Flutter renderers) = **188**
- Faza 3: 49 (UserPreferences v2) + 93 (6 generators/detectors + adaptive + Settings UI) = **142+93 = 235**
- Faza 4: 55 (cleanup tests + observability) + 23 (Flutter cleanup) = **78**
- **Razem: ~695 nowych testów**
- Phase 1-3 regression after Phase 4: 366/366 pass

## Pliki klucz

Backend:
- `app/models/notification_moment.py`, `app/models/app_insight_shown.py`
- `app/services/notification_orchestrator.py`, `app/services/in_app_insight_detector.py`, `app/services/moment_text_generator.py`, `app/services/notification_observability.py`, `app/services/notification_categories.py`
- `app/services/moments/{post_session_reflection,mood_dip_alert,streak_celebration,pattern_insight}_generator.py`
- `app/services/insights/{reveal,celebrate_tease,notice,recovery_moment,comparative}_insight_detector.py`
- `app/api/v1/endpoints/moments.py`, `app/api/v1/endpoints/app_insights.py`
- `app/tasks/notification_orchestrator_job.py`
- `app/crud/notification_moment.py`, `app/crud/app_insight_shown.py`
- `app/alembic/versions/ff6g7h8i9j0k_create_notification_moments_and_app_insights.py`
- `app/alembic/versions/gg7h8i9j0k1l_add_notification_preferences_v2.py`

Frontend:
- `lib/widgets/moments/{moment_bottom_sheet,insight_toast,inline_notice_banner}.dart`
- `lib/widgets/moments/renderers/{post_session_reflection_sheet,mood_dip_alert_sheet,streak_celebration_sheet,pattern_insight_sheet,recovery_moment_sheet,reveal_toast_renderer,celebrate_tease_renderer,notice_banner_renderer,comparative_toast_renderer,insight_dispatcher}.dart`
- `lib/screens/moments/{cubit/moments_cubit,cubit/moments_state,moment_deep_link_screen}.dart`
- `lib/data/models/{notification_moment,app_insight}.dart`
- `lib/api/api_managers/notification_moments_manager.dart`
- `lib/screens/settings/widgets/notifications_section.dart` (V2 redesign)
- `lib/screens/settings/cubit/{settings_cubit,settings_state}.dart` (V2 fields)

Linkuje do: [[project_notification_moments_redesign_2026_05_14]] (plan), [[reference_posthog_integration]] (analytics events), [[project_postgres_enum_drift]] (migracja convention).
