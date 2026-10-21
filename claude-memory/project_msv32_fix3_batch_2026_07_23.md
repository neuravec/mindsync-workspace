---
name: project-msv32-fix3-batch-2026-07-23
description: "MSV3.2 Fix 3 (QA pass of Fix 2): 8 itemów CS-01..08 — COMMITTED lokalnie (BE main a0af5d9 + FE dev 88dbc17), NIE pushed; 3× review GO; BEZ migracji (HEAD zostaje dd5e6f7182a3), deploy code-only"
metadata: 
  node_type: memory
  type: project
  originSessionId: 96594832-1d97-4ddf-b649-5eb864efbf56
  modified: 2026-07-23T20:47:18.293Z
---

# MSV3.2 Fix 3 — batch 8 itemów (2026-07-23)

QA re-work batch nad [[project-msv32-fix2-batch-2026-07-23]]. Spec: `Business_requirements/MS_3/v3.2/fixes/MSV3.2 Fix 3.md` (1 DELETE, 3 FIX, 4 CHANGE). **BEZ NOWEJ MIGRACJI** — wildcard to klucz w encrypted JSON-blob (`categorized_questions` Text col), summaries reużywają istniejących pól (Fix2 CS-13). Łańcuch migracji zostaje na **dd5e6f7182a3**. Deploy code-only.

## Status: COMMITTED lokalnie (NIE pushed) — BE `main` **a0af5d9**, FE `dev` **88dbc17**
- BE `main` a0af5d9 (baza 8a80e81): 6 plików app/ + 3 testy (+511/−122): `services/openai_service.py`, `schemas/schemas.py`, `api/v1/endpoints/prep_cards.py`, `tasks/prep_card_auto_generate.py`, `tasks/triage_proposals.py`, `models/models.py` (tylko komentarz), testy. **Implementował backend-api** (nie data-analytics — większość plików to jego teren; openai_service edytowany za autoryzacją leada; couplowane prompt↔schema). NIE commituj `.claude/agent-memory/` przy commicie.
- FE `dev` 88dbc17 (baza cba3f66): 37 plików = lib + 8 testów + regen l10n/freezed (7 ARB + generated) (+1831/−976). Kluczowy: `prep_card_widget.dart` (−764 netto, spłaszczenie). Staged tylko mindsync_app/lib+test.

## Co weszło (per item)
- **CS-01** (CHANGE, prep Topics&Questions): płaska lista ≤3 topic-pille (z suggested_agenda, tylko `.topic`) + ≤3 bare targeted questions; ZERO group-labels/rationale(context)/General/Wildcard. BE: prompt §4/§7 przepisane, internal schema `CategorizedQuestionsOutput`=targeted-only, `QuestionOutput` bez `context`, cap `[:3]` w kodzie. FE: `_buildTopicsAndQuestionsSection` zastąpił `_buildSuggestedAgenda`+`_buildQuestionsContent`; nowe pille `_buildPill`/`_buildAgendaTopicPill`/`_buildQuestionRow`.
- **CS-02** (CHANGE, prep Threads): pille title-only jak After-Therapy (`unresolved_topics` + `new_developments` oba jako pille, bez long-textu). FE zrobił własną kopię `_buildPill` (NIE import After-Therapy `_TopicChip` — to private w frozen-reference file) → **parity wizualny do device-QA**.
- **CS-03** (CHANGE, prep Patterns): ≤3 humanized recognitions, ZERO cyfr. BE: prompt §3 przepisany + cap `[:3]` + `_strip_banned_digits()` backstop na każdym itemie. FE: verify-only (bez zmian).
- **CS-04** (DELETE, wildcard app-wide): BE usunął z promptów/generation-schema/defaults/parse (też capture-screen `generate_categorized_guiding_questions`); client-facing schema `wildcard`/`general`/`context` **KEPT-EMPTY** (additive-only, stare buildy). FE usunął wildcard field z modelu + enum/controllers/ARB (7 locale) + flow-screen wildcard category; `general` field w modelu ZOSTAJE (BC). Zero live "wildcard" w questions domain.
- **CS-05** (FIX, Between Sessions Realizations flag): flaga przeniesiona z headera NA statement (`_buildBookmarkableBullet('summary', 0)`); jedna flaga, nie duplikat. Routing 'summary' istniał od Fix2 CS-16.
- **CS-06** (CHANGE, Recording card bg): `recording_summary_widget.dart:513` oceanMist→mainWhite (lokalnie, NIE token — wszystkie karty dzielą oceanMist). Akcenty E0F2F1 (chip/share/processing/badge) zostały jako theme. **Screenshot device-QA.**
- **CS-07** (FIX, Your Session state machine iOS): root cause = sygnał refresh zależał od nawigacji/lifecycle (kruche na iOS przez round-trip record→transcribe→review). Fix: `DebriefCaptureCubit._submitTextContent`/`retryProcessing` woła BEZPOŚREDNIO `sl<MainTabCubit>().refreshDebrief()`/`refreshPrepCard()` w momencie potwierdzenia API — jeden choke point, wszystkie 3 flow + FAB i moduł; Android bajt-w-bajt bez zmian. Widoczny label był JUŻ "After Therapy" (tylko Dart identyfikatory/klucz mówiły "Debrief"). **Device-QA iPhone: pełny cykl przez granicę kadencji.**
- **CS-08** (FIX, Timeline weekly/monthly): widgety `WeeklySummaryWidget`/`MonthlyAuditWidget` były OK od Fix2 CS-13 — luka to WIRING: filtry summaries/monthly szły przez timeline preview-feed zamiast full-list. Fix: `_fetchStateForFilter` w `TherapyTabCubit` routuje te 2 filtry do `listWeeklySummaries()`/`listMonthlyAudits()` (full modele) + nowe listy `_WeeklySummaryCardsList`/`_MonthlyAuditCardsList`. Reszta timeline bez zmian. **BEZ zmian BE.** Screenshot device-QA (weekly+monthly, obie platformy).

## Werdykty review
- **data-analytics** (BE prompty): **GO**, 0 defektów. CS-03 backstop testowany adversarialnie. LOW: gdy `_strip_banned_digits` faktycznie odpali (rzadko) — koślawa gramatyka ("score dropped on - - .") — kosmetyczny follow-up, pre-existing architektura Fix2. LOW-002 (interpolacja user-text) pre-existing, nietknięte.
- **integration-devops** (kontrakty BE↔FE): **GO**, 11/11 MATCH. Old-build: `wildcard:[]`/`general:[]`/`context:null` deserializują bez błędu (json_serializable ignoruje unknown keys, brak disallowUnknownKeys); żadne required client-facing pole nie usunięte. CS-05/06/07 = FE-only bez BE-impaktu.
- Testy na finalnych złączonych drzewach: BE 21 fail / 4734 pass (baseline), FE 30 fail / 1360 pass (baseline). Zero nowych.

## Decyzje flagged for veto (Darka)
1. **FE historical-render (lead ruling)**: płaska Topics&Questions renderuje TYLKO topics+targeted (new i historical); General/Wildcard NIE renderują się na karcie prep. Stored general/wildcard zostają w DB + w Workspace jeśli wcześniej flagowane (nic nie ginie na poziomie Workspace). Tension: CS-01 "all stored items still show" vs CS-04 "no wildcard-kind question, new or historical" vs "usuń General" — rozstrzygnięte za simplification+CS-04+CS-04-literal.
2. CS-01 cap 3+3 tylko na nowych kartach (historical bez backfill/truncation).
3. triage_proposals.py general/wildcard read-loop ZOSTAJE funkcjonalny (historical flagowane itemy dalej działają, "nic nie ginie").
4. CS-04 wildcard response-schema fields KEPT-EMPTY (nie usunięte) — additive-only > literalne CS-04 "no schema field".

## Deploy (operator) — BEZ MIGRACJI
1. BE: stage TYLKO app/ (NIE `.claude/agent-memory/`) → `git push origin main` + `git push heroku main`. **Migracja NIE wymagana** (HEAD zostaje dd5e6f7182a3; pending z Fix2 aa/bb/cc/dd nadal do uruchomienia RAZEM z pushem Fix2 jeśli Fix2 jeszcze nie wdrożony — Fix3 nie dodaje nic).
2. FE: `git push origin dev` → Codemagic → TestFlight/Play internal.
3. **Device-QA (fizyczny iPhone + Android)**: (a) CS-07 pełny cykl Your Session przez granicę kadencji (Prepare→View prep card→After Therapy z FAB I modułu→"Between Sessions" NATYCHMIAST→"Prepare" na 3d); (b) CS-06 Recording karta biała, obie platformy; (c) CS-08 weekly+monthly karty renderują kategorie w kolejności, puste pominięte, "How you felt" bez cyfr, obie platformy; (d) CS-02 prep Threads pille wyglądają jak After-Therapy; (e) CS-05 flaga na statement Realizations w Between Sessions.

## Follow-upy
- [ ] LOW: koślawa gramatyka digit-strip backstop gdy odpali (data-analytics, kosmetyka)
- [ ] LOW-002 prompt-hardening interpolacji (nadal otwarte z Fix2)
- [ ] CS-02 pill visual parity — potwierdzić na device
- [ ] Veto Darka na 4 decyzje wyżej

Powiązane: [[project-msv32-fix2-batch-2026-07-23]], [[feedback-memory-write-after-commit]], [[feedback-concurrent-session-git-hygiene]], [[postgres-enum-drift]].
