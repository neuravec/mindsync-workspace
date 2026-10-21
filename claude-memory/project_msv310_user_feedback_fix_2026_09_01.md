---
name: project-msv310-user-feedback-fix-2026-09-01
description: "MSV3.10 batch - CS-01 mic-conflict investigation report delivered, CS-02 false \"add session date\" push fixed (COMMITTED on branch msv3.10-cs02, NOT pushed), CS-03 missing from spec"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fdc7993-d49b-4259-b20c-b7fad1a7f219
  modified: 2026-09-01T11:46:17.334Z
---

# MSV3.10 - User Feedback Fix (batch 2026-09-01)

Spec: `Business_requirements/MS_3/v3.10/MSV3.10 - User Feedback Fix.md`. Summary specu zapowiada 3 itemy, ale CS-03 (CHANGE: import dokumentów od terapeuty do Workspace) został CELOWO wyrzucony przez operatora (potwierdzone 2026-09-01) - w tym batchu tylko CS-01 i CS-02, nie dopytywać.

## CS-01 (investigation only, DELIVERED)
Raport: `Business_requirements/MS_3/v3.10/CS-01_mic_conflict_investigation.md`. Root cause dwuczęściowy:
- (A) iOS: niemiksowalna sesja AVAudioSession (.playAndRecord/.spokenAudio bez mixWithOthers, `record_session_cubit.dart:274-334`) przegrywa arbitraż z aplikacją telehealth; nagranie sklejane z segmentów PCM po cyklach przerwań = "garbled". Średnio-wysoka pewność, 4 eksperymenty na urządzeniu opisane w sekcji 3 raportu. Android ma INNY model (silence-the-loser, zerowe bufory) - niezweryfikowany.
- (B) POTWIERDZONE w kodzie: `app/tasks/session_recording.py::process_session_recording` (ścieżka AssemblyAI) NIE sprawdza pustego transkryptu przed oznaczeniem COMPLETED; fallback Whisper w tym samym pliku MA ten guard. Cicha porażka zamiast błędu.
- Rekomendacja: najpierw backendowy guard pustego transkryptu (tanie, backend-api), potem pre-flight warning FE; decyzja fix-path należy do Darka - fix to OSOBNY item, nie wdrażać bez decyzji.

## CS-02 (FIX, COMMITTED nie pushed)
Root cause: `crud.update_therapy_schedule` czyściło `custom_therapy_sessions` przy KAŻDYM zapisie z frequency != "custom" (a nie tylko przy wyjściu z trybu custom). Przełączenie weekly<->biweekly w Settings (`SettingsCubit.updateTherapyFrequency` nie wysyła custom_sessions) po cichu kasowało jednorazową sesję -> generator ADD_THERAPY_DATE słusznie widział brak sesji i słał push. Zgodne z dowodem z proda: u zgłaszającej wszystkie 3 kolumny harmonogramu NULL; stale delivery WYKLUCZONE (median lag 1.1 min, p95 5.6 min); jej 15 pushy 01-15.08 to w większości stary bug naprawiony 16.08 (cooldown+give-up).
- Branch `msv3.10-cs02` w repo backendu: `7dddf38` (fix: clear tylko przy previous_frequency=="custom" i frequency!="custom") + `37532c0` (hardening: `cancel_active_moments_by_type()` w `app/crud/notification_moment.py` wpięte w zapis harmonogramu; używa istniejącego MomentStatusEnum.EXPIRED, zero DDL/migracji).
- QA gate 2026-09-01: GO. 5519 pass / 21 fail = pre-existing (zweryfikowane po stack-trace'ach, nie po liczbie); wszystkie 4 kryteria Done-when pokryte testami (w tym tz Pacific/Auckland + America/Los_Angeles + zmiana strefy między zapisami); boot router-tree czysty. Aktualny baseline BE = 21 faili (lista w raporcie QA).
- Deploy: DEPLOYED 2026-09-01 jako Heroku release v544 (fast-forward 956be9e..7dddf38 na origin/main, na polecenie operatora); web/worker/scheduler up, bez crash-loopa. BEZ migracji. Repo backendu z powrotem na main.
- Pending device-QA: spec wymaga weryfikacji na iOS i Android (fix czysto serwerowy, ale spec tak mówi).

## Follow-upy (nie zrobione, zgłoszone)
- flutter-mobile: `UsersManager.syncTherapySchedule` połyka wszystkie błędy zapisu po cichu - hardening poza zakresem CS-02.
- Migracja: kolumna `updated_at` na `user_preferences` (DBA drugi raz trafił na brak audit-trail) - wymaga zgody operatora, backend-api tworzy.
- Znany dług: 7 pre-existing faili schema-walidacji TherapyScheduleUpdate (custom bez interval nie raise'uje) - istniało przed batchem.
- Luka strukturalna (DBA): `next_session_date` używany WYŁĄCZNIE jako anchor biweekly/custom - user z samym next_session_date bez schedule/custom_sessions jest niewidzialny dla wszystkich eligibility checks (dziś 0 dotkniętych, ale żywa pułapka).

Raporty źródłowe: `db-reports/2026-09-01-cs02-add-therapy-date-false-push.md`, raport QA w transkrypcie batcha. Powiązane: [[project-msv322-notifications-batch-2026-07-24]], [[feedback-prod-evidence-before-code-only-diagnosis]], [[project-postgres-enum-drift]].
