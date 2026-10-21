---
name: project-ms3-batch-2026-07-02
description: "MS_3 \"Lista poprawek 01-07-2026\" (33 items) — COMMITTED+PUSHED both repos 2026-07-03; TestFlight-first strategy adopted; Heroku deploy PENDING operator approval"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b97f07e-d104-4c18-855f-046d908de715
---

MS_3 batch (spec `Business_requirements/MS_3/Lista poprawek 01-07-2026.md`, 33 items: 8 DELETE / 13 RENAME / 12 FIX) — wykonane 2026-07-02/03 przez orkiestrację (FE-A, FE-B, data-analytics, qa-testing + 4 recon agents).

**Status:** FE COMMITTED+PUSHED `3464457` origin/dev (→Codemagic→TestFlight). BE COMMITTED+PUSHED `4c2579a` origin/main. **Heroku deploy NIE wykonany** — klasyfikator uprawnień zablokował `git push heroku main` (wymaga zgody operatora). Bez deployu BE TestFlight testuje starą generację (dłuższy Overview/brak arc dopiero po deployu); FE toleruje oba stany.

**Strategia TestFlight-first (obowiązuje od teraz):** `MindSync/docs/RELEASE_STRATEGY_TESTFLIGHT_FIRST.md` — Faza 1: FE dowolnie na dev (store release = gate), BE additive-only (wspólny prod backend dla TestFlight i prod!); Faza 2 po adopcji: kasowanie legacy wg rejestru `MindSync/docs/LEGACY_CLEANUP_MS3.md` (7 pozycji: /goals/*, /therapy-tracking/*, quick-check, suggested_questions, kolumny emotional_arc/unresolved_topics, /symptoms scores, l10n). Endpointy "skasowanych" funkcji ŻYJĄ na backendzie do Fazy 2.

**Kluczowe decyzje interpretacyjne:** D-03 "Therapy tracking"=TherapyTrackingSignal (karta Main miała tytuł "Check-iny samopoczucia"!); D-05 "Check-in samopoczucia"=symptom/mood check-in (karta symptom_trend "Trend nastroju"); D-06 "Jak płynęła rozmowa"==D-07 Emotional arc (JEDNA sekcja, pole emotionalArc); D-08 unresolved_topics NIE jest endpointem — pole na SessionRecording; bliźniacze pole na SessionPrepCard czyta PORTAL KLINICYSTY → nietykalne.

**Main po zmianach (5 kart):** health_check_banner (→"Relacja Terapeutyczna"), next_session (prep-aware "View prepcard", bez Notes), last_realization (pełny tekst+deep-link), affirmation, treatment_goal_anchor.

**Follow-upy:** (1) wiring `previous_session_context` do generate_recording_summary wymaga edycji `tasks/session_recording.py` (miał obce uncommitted zmiany) — param+prompt gotowe; (2) RN-02 "Podsumowanie" nie przetłumaczone na de/es/fr/nb/sv (tylko EN/PL per spec); (3) ⚠ PRODUKT: po FX-03 NIE MA w apce ścieżki logowania score'ów objawów (wykresy będą stagnować) — potwierdzić intencję; (4) zmieniona logika Getting-Started gate na Main (3 z 4 kart usunięte); (5) pre-existing: osierocony TreatmentGoalsSection w Stats + rozjazd FE `/me/goals` vs BE `/clinician/me/goals` (fail-soft 404).

**QA (GO):** BE 4032 pass/56 pre-existing fail + boot 280 routes OK; FE analyze 0 err, 886 pass/30 pre-existing fail (reflect/wow/privacy/save-feedback baseline), +30 nowych testów.

**Audyt pokrycia 2026-07-03 (3 niezależnych agentów):** 37/37 kontroli PASS po remediacji; guardrail nazewnictwa był PARTIAL → naprawiony commitem FE `34cc96c` (7 wtórnych powierzchni health-check + badge De-brief→Po terapii w 7 lang, sync l10n/parts, 9 martwych kluczy ARB usuniętych, FX-02 toLocal() fix, BG-04 timeouty w signOut). Pozostawione świadomie: Reflect leak przy app-kill przed 1. wiadomością, zdaniowe "check-in" w copy, EN "Other speaker"/"Your insights" (decyzja produktowa), mainTab_healthCheckReady=martwy kandydat.

Raport: `Business_requirements/MS_3/RAPORT_wykonania_2026-07-03.md`. Powiązane: [[feedback-concurrent-session-git-hygiene]] (obce pliki 2 workstreamów zostały nietknięte i niezacommitowane).
