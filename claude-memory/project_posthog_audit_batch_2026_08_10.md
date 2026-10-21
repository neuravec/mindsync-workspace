---
name: project-posthog-audit-batch-2026-08-10
description: "Batch 38 zadań z audytu PostHog 2026-08-10 – status per zadanie, commity, plan odtworzeniowy po padzie sesji"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1987f7d6-ce28-4e7b-828c-e71bea9ab40e
  modified: 2026-08-11T05:16:43.838Z
---

# Audyt PostHog 2026-08-10 – batch 38 zadań (S1-S6, A1-A12, B1-B14, C1-C6)

Sesja padła 2026-08-10 ~17:57 w trakcie B3-FE; stan odtworzony z transkryptu. Pełne opisy pozostałych zadań: `analytics-reports/2026-08-10-posthog-audit-taskplan.md`.

## UKOŃCZONE (dowody = commity lokalne, NIC nie pushed)
Backend (repo MindSync, main): S1 tag expected-4xx (7696f40), A10 activated_at+user_activated (2eea4d8, migracja!), A8 fix hourly deactivation (7b4d73d+c7d7cf3), A11 worker logging+prep early-return (64ad4f3), B14 moment_type w FCM (4adf15f), A1-BE capture_qualifying (02bdce9), B3-BE summaries generated events (e16f657).
Frontend (repo mindsync-frontend, dev): S5 reflect 403 fix (e8136c0), A1-FE aktywacja (ec05973), A3 monetyzacja paywall_shown+restore (58d097b+00f8739), A4 crash reporting PostHog (dc5b340), A6 reflect_ui_session_ended (5b3af7d), A7 branded fallback route (3d99741), A9 recording_abandoned (5616b7e+0c4792e), A12 therapy_schedule snake_case fix (0ec26e9 – 100% wierszy prod było "[]", każdy niepusty zapis 422-ował!), B1 semantyka notification received/opened (8300710), B2 Timeline capture bridge (3ae6a18).
Sprawdzone (raporty): S2 zakupy (db-reports/2026-08-10-subscription-pipeline-check.md), S3 akwizycja = consent-gate artefakt (analytics-reports/2026-08-10-acquisition-collapse.md), S4 nagrania (db-reports/2026-08-10-recording-pipeline-check.md), A5 prep cards (analytics-reports/2026-08-10-prep-cards-diagnosis.md), A1 definicja aktywacji (analytics-reports/2026-08-10-activation-definition.md; pierwszy zapis w 24h = 3.41x retencja), A2 eventy-zero rozstrzygnięte, S6-ocena security (security-reports/2026-08-10-consent-gate-ruling.md).

## W TOKU / POZOSTAŁE (sesja kontynuująca 2026-08-10 wieczorem)
B3-FE (working tree, dokańczane), B4, B5, B6, B7, B8, B9, B10, B11, B12, C1 (po B3), C2, C3, C4 (po C2+C3), C5, C6.
CZEKA NA OPERATORA: S6 kroki 1-6 w Webflow (Meta Pixel/GA4 za bramkę; przed tym pull historii GA4 = część C2). ODROCZONE: B13 (po deployu fixa A12 odczekać 1-2 tyg. i zmierzyć fill-rate therapy_schedule).

## Kluczowe ustalenia przekrojowe
- "Załamanie akwizycji" web to w dużej mierze artefakt consent-gate (25.07, opt-in ~16%); aktywni aplikacji ROSNĄ (80→92 przy $lib='posthog-flutter').
- Kanoniczny filtr aplikacji: properties.$lib = 'posthog-flutter'; web = 'web'.
- api_error: 4507 zdarzeń/14d, z czego realne awarie ~20; reszta to zamierzone 404/403 (otagowane po S1).
- DEPLOY: batch wymaga push BE (z migracją activated_at: alembic upgrade head RAZEM z deployem) + push FE. Nowy HEAD migracji po 2eea4d8 – zweryfikować łańcuch przed deployem (poprzedni head ff7182a3b4c5).

## Kontynuacja (sesja 2, wieczór 2026-08-10) – wykonane
Backend (main, lokalnie, NIE pushed): B3-BE e16f657 (wcześniej), B5-fix 7f66013 (realization_detected z detektora), C5 2ff6e10 (retire legacy conversation_*), A13-fix 6b8e05e (atrybucja NOTIFICATION w 7 generatorach), B12 991cb9a (trial_started/ended serwerowo + MIGRACJA hh9i0j1k2l3m: 5 kolumn user_subscription_trial), B18 40c10d2+69cc599 (MIGRACJA ii0j1k2l3m4n: ALTER TYPE featureenum ADD VALUE CLINICIAN/THREAD_CONTEXT/WEEKLY_OBS + track_usage w clinician_ai + fix testów chain-tip), A14 685ca9b (score-before-generate + guard None w orkiestratorze, ~85-105 USD/mies. oszczędności).
ŁAŃCUCH MIGRACJI po batchu: ff7182a3b4c5 → gg8h9i0j1k2l (A10 activated_at) → hh9i0j1k2l3m (B12 trial) → ii0j1k2l3m4n (B18 enum) = HEAD. Pełna suita BE po wszystkim: 20 failed/5007 passed = baseline.
Frontend (dev, lokalnie, NIE pushed): B3-FE 5735309 (summary_viewed), B6 ff3087c (krok personalise step_index=-1), B8-fix 768eac3 (przycisk wstecz Ustawienia), C3-fix d3955a6 (doc: $is_testflight=100% na iOS, niska wartość=miks OS), B9 498071b (Install Referrer + app_install_attributed; pakiet play_install_referrer ^0.5.0), B17 0d91e34 (name dla tras pageBuilder: welcome+wow – $screen nie leciał), C1-FE 2960a82 (12 martwych eventów usuniętych, bio_viewed podpięty).
UWAGA GIT FE: lokalny dev ROZJECHANY z origin/dev – origin HEAD = bump 2.0.76 (5208340), lokalny łańcuch odchodzi od jego rodzica; push wymaga rebase (kolizja tylko CHANGELOG/pubspec).
Werdykty/raporty: B4 cele=WYGASIĆ/symptomy=WYPROMOWAĆ (goals-symptoms-verdict), B7 voice=utrzymać bez inwestycji, Gemini Live NIE (voice-chat-assessment), B8 rage-click=bug Ustawień (rageclick-audit), B10 diaryzacja=projektowa+FK cascade (nie bug), B11 boty=26% top-of-funnel, realny bounce 41%, aktywacja 22,6% (anonymous-users-analysis), B16 brak regresji (szum), A13 95% kosztu AI=waste orkiestratora (system-ai-cost-audit), C2/C3/C7 filtry: $lib='posthog-flutter' + !$is_testflight + !$is_emulator + $device_model NOT IN (OnePlus8Pro,Pixel 6 Pro) – boty AKTYWNE nadal, C4 skrypt dashboardów przepisany (uruchamia operator PO deployu), opinia RODO anonimowy auth=dopuszczalny pod 7 MUST (anonymous-auth-gdpr-opinion).
CZEKA NA OPERATORA: S6 Webflow kroki 1-6 + pull GA4 PRZED (instrukcja w metrics-hygiene-c2-c3); ASSEMBLYAI_API_KEY decyzja; PROD-DECYZJE: cele/symptomy, ściana logowania, B13 (po 1-2 tyg. od deployu), C6 deep-linki, link Play Store z referrer= na www (format w raporcie B9), potwierdzenie botów w Play Console, uruchomienie posthog_build_dashboards.py po deployu.

## Ogon batcha (sesja 2, finał)
C1 DOMKNIĘTE w 3 częściach: FE 2960a82 (12 usuniętych, bio_viewed podpięty, prep_card_started+prep_capture_started=celowa podwójna emisja), BE 0a317e7 (report_exported usunięty, report_generated=phantom, regenerated-warianty=celowo unified przez is_regeneration), handoff 177c026 (prep_card_auto_generated w cronie z source='auto_cron', endpoint deprecated-not-deleted, recording_processing_* JUŻ dobrze umiejscowione w process_session_recording_whisper).
KRYTYCZNE ZNALEZISKO (db-reports/2026-08-10-insight-job-check.md): worker RQ nigdy nie wołał init_posthog() → KAŻDY capture z workera cicho no-opował (posthog_service.py:117-118). Fix w 177c026: init_posthog() w app/tasks/__init__.py + NIUANS RQ: job resolwowany po func.__module__, więc deactivate_expired_subscriptions przepięty przez nowy thin-wrapper app/tasks/subscriptions.py (rewire w rq_scheduler_setup.py). Bez tego fixa emisje workerowe z B3/B5-fix/B12 nie działałyby po deployu.
Insight job: NIE padł – generuje wiersze do dziś (app_insights_shown), cisza eventu = no-op workera. Otwarta drobnostka: 4 eventy .generated 06-29..07-23 niewyjaśnione mechanizmem (uczciwie odnotowane).
SUITY FINALNE: BE 20 failed/5022 passed = baseline; FE 32 failed/1650 passed = baseline (w tym 1 flaky pre-existing record_session_appbar_close). Po deployu: posthog-data-extractor ma zweryfikować, że eventy workerowe płyną.

## DEPLOY 2026-08-11 (rano)
BE: PUSHED origin/main + DEPLOYED Heroku v531 (67b1bdc, w tym housekeeping commit pamięci DBA); operator wykonuje alembic upgrade head (3 migracje: gg8h9i0j1k2l + hh9i0j1k2l3m + ii0j1k2l3m4n) zaraz po deployu – do potwierdzenia.
FE: dev zrebase'owany na origin/dev (bump 2.0.76+149, zero konfliktów, 20 commitów) i PUSHED origin/dev 34f2af9 → Codemagic → TestFlight/Play internal. UWAGA: hashe FE z sekcji wyżej są sprzed rebase (np. C1-FE 2960a82→09512ae, B17 0d91e34→6c1f7e1); housekeeping commit 34f2af9 zawiera pamięci agentów + codegen (gen-l10n reformat, stale freezed).
PO MIGRACJI (weryfikacja): posthog-data-extractor sprawdza, czy płyną eventy workerowe (weekly_summary_generated, realization_detected, inapp_insight.generated, prep_card_auto_generated, trial_ended) + user_activated/paywall_shown/summary_viewed z nowych buildów; potem operator uruchamia scripts/posthog_build_dashboards.py --update.