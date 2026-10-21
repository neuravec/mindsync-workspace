---
name: project-first-conversation-prep-card-fix-2026-10-08
description: "Karta Before therapy z 1. rozmowy nie powstawała przez dryf enuma inputtypeenum (brak 'AUTO' na prodzie); fix BE v569, migracja m317 i FE branch czekały na operatora"
metadata:
  node_type: memory
  type: project
  originSessionId: f8364321-0567-4c21-a0cc-1b731df5a4d5
  modified: 2026-10-08T05:10:36.678Z
---

Zgłoszenie 2026-10-07: tester (Darek) po resecie onboardingu nie dostał karty Before therapy. Przyczyna z proda (db-reports/2026-10-07-first-conversation-prep-card-missing.md): job przeszedł wszystkie bramki, a INSERT padł, bo `InputTypeEnum.AUTO` wysyła nazwę `'AUTO'`, a prod miał tylko `VOICE`, `TEXT` i małe `auto` (migracja d0y1z2a3b4c5 dodała wartość zamiast nazwy). Od 2026-03-28 nie zapisała się ŻADNA karta AUTO, cron auto-generate też był martwy. Drugi brakujący label: featureenum `MOOD_TREND` (gubiony koszt AI trendu nastroju). Sweep wszystkich enumów: tylko te dwa.

Stan na 2026-10-08 rano:
- BE 0c7d275 (fd662c1 migracja m317 + FeatureEnum.MOOD_TREND, d147c83 dedup per wątek, zwalnianie claimu, limit 2/24 h, uczciwa obietnica recapu, 0c7d275 poprawki security H-1/M-1: zero eventów PostHog dla kryzysu/short/braku terapii, eventy joba i crona bez osoby) jest LIVE jako v569.
- Migracja m317 NIE uruchomiona: klasyfikator blokuje `heroku run alembic upgrade head` subagentowi; potrzebna wyraźna zgoda operatora w sesji głównej albo uruchomienie przez operatora.
- FE 5ec58ed na `fix/first-conversation-prep-card-arrival` (odświeżenie po lądowaniu, watcher karty 10 min, poll Timeline, stan "przygotowywana", retry /end), QA czyste, NIE wypchnięte.
- Decyzje operatora: cron kart ożywiony świadomie; Darek robi reset jeszcze raz po wdrożeniu (bez backfillu wątku 28711); luka PostHog dla pominięć zdrowotnych akceptowana (mierzyć z DB/logów).

**Why:** testy na SQLite nie łapią dryfu enumów; nowy test_enum_label_drift_guard.py pilnuje tego od teraz.
**How to apply:** przed pracą nad kartami sprawdź `alembic current` na prodzie (m317?) i czy FE branch trafił do dev. Otwarte follow-upy: H-1 voice excerpts (zob. [[project-cloud-session-review-2026-10-07]]), sweep zawieszonych PROCESSING, F4 enqueue z /recap, hide_parameters w engine, log `{e}` w openai_service, zaokrąglanie czasu eventów bez osoby. Dryf: [[project_postgres_enum_drift]].
