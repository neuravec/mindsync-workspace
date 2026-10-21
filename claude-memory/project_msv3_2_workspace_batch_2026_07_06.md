---
name: msv3-2-workspace-batch-2026-07-06
description: "MSV3.2 batch (13 CS items) + Workspace feature — COMMITTED lokalnie w obu repo, NIE wypchnięte; sekwencja deploy + otwarte decyzje"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1e56ab8f-c62b-48c3-84df-1b3e9393a7bf
---

# MSV3.2 + Workspace — pełny batch (2026-07-05/06)

**Status: COMMITTED lokalnie, NIE PUSHED.** Spec: PDF "MSV3.22020Change_Spec" rev.2 (13 pozycji) + brief Workspace (PDF). Kopie tekstowe: scratchpad sesji 1e56ab8f. Kontrakty: `Business_requirements/MS_3/{WORKSPACE_API_CONTRACT.md, CS-06_deeplink_contract.md, SECURITY_AUDIT_MSV3_2.md}`.

## Commity
- **BE main** (5 przed origin/48f3091): `5c75d39` fundament (8 tabel, migracja `xx4y5z6a7b8c`, 27 endpointów /workspace, XP hooki) → `12543e3` warstwa AI (triage proposals, thread context, goal narrative weekly, mood-trend summary, weekly observations, 2 generatory momentów, fixy CS-06) → `f789a4b` integracja (hooki enqueue, wiring main.py, migracja `yy5z6a7b8c9d` enum momentów, view=active=open, context_snippet) → `3b5f701` test kaskady MED-002 → `3ce9087` design-alignment (migracja `zz6a7b8c9d0e` agenda.kind = HEAD; pin realization→agenda; PATCH thread status).
- **FE dev** (7 przed origin/a5fd523): `8f3cb29` voice (CS-01/02/04/05) → `90e0c93` tab Workspace + nav swap → `e978969` Main redesign (CS-08..13) → `24a2f44` triage UI + deep-linki → `4b25f93` kasacja Stats (CS-21) → `b368387` contextSnippet → `2ace27a` redesign wg handoffu (66 plików).

## Runda design-alignment (2026-07-06, handoff "MSV3.2 Workspace Screen")
Handoff: `Business_requirements/MS_3/MSV3.2 Workspace Screen-handoff.zip` — wybrany kierunek 1a "Papier" (`WorkspacePrep.dc.html`), triage wg `TriageCard.dc.html`; `WorkspaceBoard` = odrzucona alternatywa 1b. Design NADPISAŁ spec w 2 miejscach (decyzja leada za zgodą usera): (1) triage realizations = grupa "Odkrycie" z zakładką (in_repo=true przez istniejące toggles), bramka 2 toggli USUNIĘTA; (2) homework na Main = MAX 2 (nie 3 FIFO). Ponadto: agenda-hero z terminem sesji, wątki = akordeon inline z mini-mapą + cykl statusu chipem (PATCH, 409 przy reopen>5), Odkrycia (nowa nazwa PL) z pin-do-agendy, Cel inline z "Dziennikiem narracji", CS-12 prompt od 24h po sesji. Świadome adaptacje FE: checkbox agendy = touch→remove (realna reguła, nie kosmetyczny toggle z dema); licznik todo = liczba otwartych (endpoint nie zwraca done-count — drobny odchył od "X / Y zrobione"); undo celu przez toast (karta unmountuje się natychmiast). ThreadDetailScreen/GoalDetailScreen zostały w kodzie (deep-linki), tylko nawigacja z modułów wymieniona na akordeony.

## Kluczowe fakty techniczne
- **iOS dead mic (CS-02)**: `record_darwin` konfiguruje AVAudioSession TYLKO przy `manageAudioSession:true`; `debrief_capture_cubit` (3 z 4 flow) nie ustawiał sesji → zero ramek. Fix: playAndRecord przed start/resume. **Wymaga QA na fizycznym iPhone.**
- **CS-06 root cause**: backend słał `deep_link_route`, Flutter czytał tylko `route` → 9 typów pushy nie deep-linkowało. Teraz BE śle OBA klucze; FE resolver w `lib/utils/notification_route_resolver.dart` (route + fallback legacy).
- Migracje do ręcznego uruchomienia na Heroku: `xx4y5z6a7b8c` (8 tabel workspace) + `yy5z6a7b8c9d` (ALTER TYPE moment_type_enum ADD VALUE IF NOT EXISTS MOOD_UPDATE_REQUEST/THERAPY_RELATIONSHIP_CHECKIN, autocommit). Head = `yy5z6a7b8c9d`.
- Rejestr generatorów momentów = **11** (9 + MoodUpdateRequest + TherapyRelationshipCheckin); rejestracja module-scope (lekcja Cadence v3).
- XP mapping (zatwierdzony): todo_done=orca 2, agenda_touched=orca 1, thread_closed=user 3; odklik neutralny.
- Rozstrzygnięcia konfliktów spec vs brief: homework Main = 3 najstarsze FIFO; triage BEZ pre-zaznaczeń AI.
- Baseline'y testów po batchu: BE 21 fail (te same nazwy), FE 30 fail (2 pliki z baseline'u przeszły na zielono, total wciąż 30). Nowych failów zero.
- Stats skasowany; KEEP: `stats_tab_cubit`+`health_check_section` (Workspace), `unified_symptom_module` (Main mood), `goal_tracking_cubit`, `snapshots_cubit`, całe `lib/api/`.

## Sekwencja wdrożenia (operator)
1. BE: `git push origin main` + `git push heroku main`, potem NATYCHMIAST `heroku run alembic upgrade head --app mindsync` (create_all i tak dotworzy tabele bezpiecznie — brak natywnych enumów — ale migracje mają być autorytatywne).
2. Ustawić (opcjonalnie) nowe env: TRIAGE_EXTRACTION_PROMPT, THREAD_CONTEXT_PROMPT, MOOD_TREND_SUMMARY_PROMPT, WEEKLY_OBSERVATION_PROMPT (mają bezpieczne defaulty).
3. FE: `git push origin dev` → Codemagic → TestFlight/Play internal.
4. Manualne QA: fizyczny iPhone (mikrofon, 3 flow głosowe) + macierz deep-linków `mindsync-frontend/mindsync_app/docs/CS-06_manual_test_matrix.md`.

## Otwarte decyzje / backlog
- **MED-001 (decyzja produktowa)**: GET /goals/{id}/narratives bez premium gate (ai_narrative jest gate'owane, achieved_narrative nie) — ujednolicić w którąś stronę.
- MED-003: `detail=str(e)` w dashboard.py (13 istniejących + 1 nowe) — ticket data-analytics.
- Low: hardening `touch_agenda_item` (filtr Thread.user_id), walidacja card_type w triage GET, rate limiting na write-endpointach workspace.
- Backlog FE: badge na share-kartach hardcoded EN ([[archive]] share_card_config.dart); martwy `TreatmentGoalAnchorWidget`+`TreatmentGoalsCubit` (nigdzie nie montowany); orphaned klucz l10n `capture_useTextInsteadButton`.
- mood_dip_alert deep-link → /main-page (ogólny); docelowo może celować w moduł mood na Main, gdy powstanie route z parametrem.

Powiązane: [[reference_frontend_ci_git_topology]], [[project_notification_cadence_v3_2026_07_03]], [[project_ms_v3_fix1_fix2_2026_07_03]], [[feedback_memory_write_after_commit]].
