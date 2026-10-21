---
name: project-redesign-cards-workspace-character-2026-10-13
description: "Redesign kart (Before/After + wszystkie karty + Timeline), Workspace WA1 v2 i Character KD; design zamknięty 13.10, wdrożenie e2e przez 3 zespoły agentów"
metadata:
  node_type: memory
  type: project
  originSessionId: b6586333-3dd5-492d-905d-2c19866da247
  modified: 2026-10-14T11:58:28.076Z
---

Design: artefakt https://claude.ai/artifact/1T46tjjRbva5YaEL2M5hRF (strony Karty Before/After, Workspace, Character), decyzje Darka w komentarzach z END i w kartkach (n_fb, n_aall, n_wa, n_kd...). Pliki plansz lokalnie w scratchpad sesji b6586333 (cards/project).

Wybrane kierunki: karty A (zawartość i funkcje jak dziś, nowy UI, To-do bez odhaczania, zapis do Workspace wszędzie, Focus Areas, panel postępu na After), Timeline z filtrami i listą chronologiczną; Workspace WA1 v2 (kolejność Agenda, To-do, Questions, Goals, Threads, Realizations, Therapy relationship; żywe kolory); Character KD (karta postaci, gwiazda umiejętności, level-up). Odrzucone: B, C, WB, WC, WA2, KA, KB, KC, KD+.

Wdrożenie 13.10 ~21:45: workflow wf_680df445-a1a (3 zespoły równolegle + agent integracyjny, który scala do lokalnych gałęzi feat/redesign-integration w obu repo, worktree *-wt-redesign-int). Gałęzie zespołów: feat/after-card-progress, feat/cards-redesign, feat/workspace-redesign, feat/character-sheet (oba repo). Nic nie wypchnięte; flagi after_card_progress_panel i character_sheet_v2 domyślnie off.

Orka: rysunek orki w artefakcie NIE jest wzorem. W apce zostaje obecna orka (widget MimikOrca, lib/screens/character_tab/widgets/mimik_orca.dart, z kolorami i stadiami). Po workflow obowiązkowy krok: sprawdzić i poprawić na feat/redesign-integration, że KD1/KD3 i każde inne miejsce używa MimikOrca, a nie SVG z artefaktu (operator 13.10).

Stan 14.10 06:40: workflow zakończony, 9/9 agentów. Scalone lokalnie, NIE wypchnięte: BE feat/redesign-integration 4a10882 (alembic head m320c4a5r6d7 na m318), FE feat/redesign-integration 989181f. Warianty na niewypchniętych release 10-13: BE feat/redesign-integration-on-release-1013 737e400 (m318→m319→m320), FE feat/redesign-integration-on-release-fe-1013 0ccbfb5. Upstream (origin/main, origin/dev) odpięty od gałęzi integracyjnych, żeby gołe `git push` nie poszło na main/dev. Orka zweryfikowana: KD1 i KD3 używają MimikOrca. Security: bez Critical/High; otwarte M-2 (dane po cofnięciu zgody), M-3 prawnik przed włączeniem flagi.

Decyzje operatora 14.10 (runda 2, przed wspólnym pushem): bez flag, wszystko widoczne na TestFlight/Android test (CHARACTER_SHEET_V2_ENABLED domyślnie true jako kill switch); panel postępu zawsze widoczny, szara kłódka poniżej 3 sesji dowolnego typu, dane liczone z historii; wzór v1 zaakceptowany; cofnięta zgoda na profilowanie = kłódka + okno potwierdzenia + POST /gamification/character_sheet/consent (nie 403, nie stary ekran); migracje w jednej linii m318→m319→m320; push wszystkiego naraz, backend idempotentny dla obecnych użytkowników. Gałąź docelowa feat/redesign-final w obu repo (worktree *-wt-redesign-int-rel), BE gałęzie robocze feat/progress-panel-v2 i feat/charsheet-consent do scalenia.

Stan 14.10 po rundzie 2 (NIE wypchnięte): BE feat/redesign-final 4c7675b (worktree MindSync-wt-redesign-int-rel, FF nad origin/main 7e281ff, head m320c4a5r6d7, prod na m318), FE feat/redesign-final 5c27b2c (worktree mindsync-frontend-wt-redesign-int-rel, FF nad origin/dev 03aab0d). QA pre-deploy: GO, 0 regresji (BE 8 fail = baseline, FE 20 fail = baseline + 1 flaky reflect_thread_handoff). Kolejność pusha: BE na main, alembic upgrade head, smoke, potem FE na dev. Kill switch: CHARACTER_SHEET_V2_ENABLED=false. Brak wierszy zgody dla istniejących userów (brak rekordu = zgoda); otwarte L-1..L-5, .env w gicie, device QA.

WDROŻONE 14.10 ok. 15:00 (zgoda operatora): BE 7e281ff..4c7675b na main = Heroku v572, alembic upgrade m318→m319→m320, current m320c4a5r6d7; smoke czysty (0 Traceback/H/5xx, worker high+default). FE 03aab0d..5c27b2c na dev (Codemagic/TestFlight). Otwarte: device QA na TestFlight, weryfikacja eventów PostHog (posthog-data-extractor), L-1..L-5, copy z rundy 1. Rollback: kill switch albo heroku rollback v571 (schemat m320 addytywny, zostaje).

**Why:** operator chce mieć jutro oba repo gotowe do commita/pusha.
**How to apply:** status sprawdzić w wyniku workflow i `git log feat/redesign-integration` w worktree *-wt-redesign-int; nie pisać „wdrożone” przed pushem i migracją (zob. [[feedback-memory-write-after-commit]]). Blokery: przegląd bezpieczeństwa Character (Critical/High blokują), opinia prawnika PROFILING dla statystyk i gwiazdy.
