---
name: project-notification-cadence-v3-2026-07-03
description: "Framework momentów NIGDY nie wysłał pusha (rejestracja generatorów tylko w web dyno) — fix + kadencja 2/dzień + pre/post-session + wycięcie legacy schedulerów; BE commit lokalny 2621868 (push DENIED), FE 895713d na origin/dev"
metadata: 
  node_type: memory
  type: project
  originSessionId: a7bf3365-4478-4789-83a1-6835e7a7a9d5
---

**Notification Cadence v3 (2026-07-03).** Audyt: system "Notification Moments" (shipped 2026-05-15) nigdy nie wysłał ANI JEDNEGO pusha — `notification_moments` 0 wierszy na prodzie. Root cause: generatory/detektory rejestrują się efektem ubocznym importu `app.services.moments`/`insights` TYLKO w web dyno (`app/main.py`); RQ worker importuje wyłącznie moduł joba → pusty rejestr → cogodzinny orchestrator kończył "Job OK" w 0.7s (pusta pętla). Zweryfikowane na prod dynie (`generator_count==0`). Ta sama luka ubiła async in-app insights (regresja HIGH-04 z 202).

**Zaimplementowane** (3 agentów: data-analytics, backend-api, flutter-mobile; QA GO):
- module-scope importy w `notification_orchestrator_job.py` + `NoGeneratorsRegisteredError` zamiast cichego no-op + subprocess cross-process test (`test_notification_worker_registration.py`)
- sloty MORNING 10-13 / EVENING 18-21 czasu lokalnego, cap 1→2; baseline fallback zero-AI: `DAILY_CHECK_IN` (nowy typ; wariant nudge "ustaw harmonogram terapii") + `REFLECTION_INVITATION` → aktywni (≤14d) dostają gwarantowane 2/dzień
- nowy `SESSION_MORNING_OF` (2-3.5h przed sesją, cap-exempt); THERAPY_PREP/POST_SESSION_REFLECTION bez zmian
- fix bug `prefs.timezone`→`prefs.time_zone` (okna/DND liczone zawsze w UTC); mocki testów ze spec=
- legacy cleanup: −3 joby-duchy, −4 setup_* za flagą, −flaga `notification_legacy_jobs_enabled`, −7 notify_*, −health_check.py, −symptom_tracking_reminder.py, −zepsuty `get_users_eligible_for_notification`; zostało 19 setup_*
- migracja `ww3x4y5z0a1b`: ALTER TYPE moment_type_enum ADD VALUE IF NOT EXISTS 'DAILY_CHECK_IN','SESSION_MORNING_OF' (autocommit block, sqlite-guard)
- FE: `MomentType` +reEngagement/dailyCheckIn/sessionMorningOf/unknown + `@JsonKey(unknownEnumValue)` (klient znał 8/11 typów; nieznany typ psuł parse /moments/upcoming i ubijał też pendingInsights przez wspólny Future.wait) + generyczny sheet dispatch

**Status:** FE PUSHED `895713d` origin/dev (rebase na auto-bump dac98f3/2.0.62) → TestFlight. BE COMMITTED lokalnie `2621868` na main (baza 74632f3) — push origin/main ZABLOKOWANY przez auto-mode classifier, operator musi: `git push origin main` → `git push heroku main` → `heroku run alembic upgrade head -a mindsync` (deploy+migrate razem; boot nie zależy od labels). Weryfikacja po deployu: log workera "Orchestrator has 9 registered generator(s)" + przyrost wierszy notification_moments.

**Otwarte:** (1) brak następcy symptom-tracking nudge (decyzja produktowa); (2) tokeny FCM tylko 13.4% userów, `next_session_date` 0/1722 — bez FE promptów (permission re-ask, wpisanie harmonogramu) pushe sesyjne nie mają danych a zasięg to ~13%; (3) `.env.example` stale linia flagi (integration-devops); (4) QA testy: 21 backend + 30 flutter fail = pre-existing baseline (spadek ze ~101); raport prod: `db-reports/notifications_prod_audit_2026-07-03.md`. Powiązane: [[project-scheduler-cleanup-2026-05-19]], [[project-notification-moments-shipped-2026-05-15]].
