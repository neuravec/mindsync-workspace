---
name: project-msv32-fix4-batch-2026-07-24
description: "MSV3.2 Fix 4 (QA pass 23.07) — 4 itemy COMMITTED lokalnie (BE 3c55f8d main + FE eaa7471 dev, NIE pushed); migracja ee6f7182a3b4 = HEAD; kluczowe root cause'y CS-02/CS-03"
metadata: 
  node_type: memory
  type: project
  originSessionId: 00a3a98a-0537-4b03-b847-87f715082c0b
  modified: 2026-07-24T11:56:21.376Z
---

MSV3.2 Fix 4 (spec: Business_requirements/MS_3/v3.2/MSV3_2_Fix_4.md, QA pass 23.07.2026) — 4 itemy zaimplementowane e2e 2026-07-24, **COMMITTED lokalnie, NIE pushed**: BE `3c55f8d` (main, ahead 1 nad b8c28e3) + FE `eaa7471` (dev, ahead 1 nad 55cbf90).

**Root cause'y (ważne na przyszłość):**
- CS-03 "raw 500 / zero kart": feature był zbudowany w kodzie od Fix.1, ale **Heroku stało na v515 (2026-07-03)** — Fix.1/2/3 wypchnięte na GitHub, NIGDY nie zdeployowane na Heroku. QA testowało nowy FE (TestFlight) przeciwko staremu BE.
- CS-02 "brak flagi": FE flaga istniała od Fix 3 (`triageBookmark('summary', 0)`), ale backend nie emitował mechanicznej propozycji `realization_ref` dla between_session — naprawione bezwarunkowym kandydatem (index None→0, realization_detection w lockstep).

**Co weszło:**
- CS-01: pole `threads [{label, context, is_continuation}]` (cap 3) na recording/between_session/prep — modele AI + prompty + zaszyfrowane kolumny Text-as-JSON + triage preferuje `threads` nad legacy (bez duplikatów chipów); FE wspólny `ThreadsSectionList`/`ThreadPill` (`lib/widgets/threads_section.dart`) = piksel-kopia After Therapy (referencja NIETKNIĘTA); legacy shapes renderowane dla kart historycznych.
- CS-03: kalendarzowe okna (pon.–niedz. / miesiąc, strefa usera; helpery `get_calendar_week/month_range_utc` w time_utils, DST-safe — złapany realny bug pytz), auto-trigger = pierwszy hourly tick po końcu okresu (dedup per okres, ZERO backfillu), Generate Now celuje w ostatni ZAKOŃCZONY okres, `summary_sections` = czyste przepakowanie pól Fix2 (bez drugiego wywołania AI; weekly got_done/goals pochodzą z key_insights/patterns repurposed w Fix2), digit-ban backstop na how_you_felt po OBU stronach (weekly dodany po review). FE renderuje sekcje (puste kategorie pomijane, bez flag), nagłówki = istniejące klucze l10n (therapy_periodSummary*).
- CS-04: `DELETE /api/v1/workspace/realizations/{id}` = in_repo=False + pin clear + deselect_proposal (treść NIGDY nie kasowana, karta Timeline zostaje); FE "Delete" w menu 3-kropek TYLKO Realizations, bez dialogu.

**Werdykty:** security-guardian GO (0 Crit/High; OBS-01 pre-existing: weekly summaries NIE gate'owane premium vs monthly gate'owane — do decyzji produktowej). integration-devops GO (kontrakty FE↔BE zgodne co do klucza/indeksu). Suity: BE 4819 pass / 21 fail = baseline; FE 1424 testy / 30 fail = baseline; analyze 0 nowych.

**Deploy (checklist operatora):** push BE main → `git push heroku main` (catch-up 4 batchy!) → NATYCHMIAST `heroku run alembic upgrade head --app mindsync` (5 pending: aa→bb→cc→dd→**ee6f7182a3b4**=HEAD, wszystkie addytywne/idempotentne; boot-safe przy lagu) → `heroku ps` + logi → smoke: POST /weekly-summaries/generate + /monthly-audits/generate (200 envelope, nigdy raw 500) → potem push FE dev (Codemagic→TestFlight). CS-02/CS-03 zamykać WYŁĄCZNIE po device-QA na iPhone+Android (spec: close-against-build, trzecie podejście).

**Zanotowane na później:** pre-existing hazard strict-output (bare `default=` na RecordingSummaryResult.emotional_arc, EnhancedPrepCardResult.limited_data, PrepCardTopic.from_open_thread) — ta sama klasa buga co dawne A7 500; wymaga osobnego taska (~15 call sites w testach). Patrz [[project-msv32-fix3-batch-2026-07-23]].
