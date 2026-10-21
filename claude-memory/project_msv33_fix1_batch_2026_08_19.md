---
name: project-msv33-fix1-batch-2026-08-19
description: "MSV3.3.Fix.1 – 8 itemów (CS-01..08) BE DEPLOYED Heroku v542 (a817b77, 2026-08-20, dyna up) + FE PUSHED dev 96468f6 (rebase na Codemagic bump); root cause CS-07 = naive users.created_at vs aware; bez migracji; QA GO + review GO"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b2d7bcf-7e93-4b0d-8742-9a0b75d8c17b
  modified: 2026-08-20T08:12:08.850Z
---

# MSV3.3.Fix.1 batch (2026-08-19/20) – BE DEPLOYED v542, FE PUSHED dev

Spec: `Business_requirements/MS_3/v3.3/fixes/MSV3.3.Fix.1 - Change Spec.md` (8 itemów: 7 FIX + 1 CHANGE, re-work 4 itemów MSV3.3).

## Commity / deploy (operator autoryzował push 2026-08-20)
- **BE main: DEPLOYED Heroku v542** (`Deploy a817b772`, 2026-08-20 10:09, web+worker+scheduler up, bez crash-loopa): a817b77 (CS-04 score_series) → cde4aab (CS-05 context_description + CS-01 capitalize) → 0a3ef72 (CS-07 root cause+sweep) → 552a267 (CS-06 routing+push_delivered) → 8dd329d (v541)
- **FE dev: PUSHED 96468f6** (po rebase na Codemagic auto-bump f11f72e; stare lokalne hashe 30c553c/33dc58a/4fea945/9c9100e → nowe 96468f6/7298fe7/db844c2/278e2c9) → Codemagic → TestFlight/Play internal
- **BEZ migracji** – HEAD zostaje pp7q8r9s0t1u. Deploy code-only, kolejność BE/FE dowolna (contract review potwierdził addytywność w obie strony).

## CS-07 root cause (najważniejsze odkrycie)
`users.created_at`/`last_login` na prodzie = `timestamp WITHOUT time zone` (drift vs model timezone=True). `adjust_period_start_for_signup()` (crud.py) porównywał naive vs aware → TypeError na KAŻDEJ z 4 ścieżek (crony weekly/monthly + oba POST /generate). Obie tabele weekly/monthly **puste od zawsze** (cron: errors=1798/h); endpoint zwracał HTTP 200 status="failed" → UI wyglądało jak "nic się nie dzieje". Raport: `db-reports/2026-08-19-cs07-weekly-monthly-summaries-root-cause.md`. Fix: defensywna normalizacja naive→UTC + sweep PROCESSING>15min→FAILED(retryable) w cronach + /generate re-enqueue na FAILED/stale.

## Kluczowe kontrakty (addytywne)
- Prep card `emotional_temperature[].score_series`: nullable lista `{date:"YYYY-MM-DD", score:1-10}`, ≤14 pkt chronologicznie, null (nigdy []) gdy brak; 5 starych pól nietknięte. FE: `ScorePoint`/`scoreSeries`, wykres tylko przy ≥2 pkt; wspólny painter `lib/widgets/charts/symptom_score_chart.dart` (ekstrakt z Mood Trend, Main piksel-identyczny).
- Thread list: `context_description` (pełny tekst) dodane do ThreadResponse; `context_snippet` zostaje dla starych buildów; FE fallback description→snippet.
- `/moments/upcoming`: `push_delivered: bool`; FE `pushDelivered` nullable – null→stary gate (status!=SENT), false→pokaż kartę in-app, true→nie (reguła CS-20 zachowana).
- CS-06 trasy: RECOVERY_MOMENT/REVEAL/COMPARATIVE/MOOD_DIP → `/main-page/tab/main?section=mood_trends`; NOTICE → workspace `?section=goals` (agenda/todo zarezerwowane); CELEBRATE_TEASE → character `?section=streaks` (`level` zarezerwowane); RE_ENGAGEMENT → `/fab/between-sessions`; `route_for()` bez fallbacku /main-page (unmapped → None+log, klient nie renderuje). notice_banner_renderer.dart USUNIĘTY (martwy); RecoveryMomentSheet/PatternInsightSheet podpięte. Checklist: `docs/MSV33_Fix1_CS06_reminder_checklist.md`.
- CS-07 FE: poll-timeout → karta "taking longer" z Refresh; `_GenerateNowRow` widoczny też przy niepustej liście (bezpieczne – /generate deduplikuje COMPLETED); modele weekly/monthly z nullable envelope + skip-bad-row w managerach (1 zły wiersz nie wygasza taba); 4 nowe klucze l10n (therapy_refreshButton itd., 7 ARB).

## Weryfikacja
- QA report: `docs/MSV33_Fix1_QA_report_2026_08_20.md` – **GO**: BE 23 fail/5421 (baseline 21; +2 = prawdopodobnie date rollover, nie kod – 0 plików z faili tknięte batchem); FE 25 fail/1967 (baseline ~30); analyze 132 = baseline.
- Contract review: `docs/MSV33_Fix1_contract_review_2026_08_20.md` – **GO**, 0 Crit/High.

## Follow-upy (nie zrobione, świadomie)
1. Migracja ALTER `users.created_at`/`last_login` → timestamptz (zamknięcie driftu u źródła) – osobny batch, ostrożnie (prod drift).
2. `app/tasks/premium_intent.py:115` – ten sam naive-vs-aware pattern, oflagowany (degraduje cicho, punkt scoringu 24h może nigdy nie działać).
3. CS-08: pre-existing FAILe backend walidacji custom frequency (test_therapy_frequency.py itd.) – batch naprawił tylko brakujące pole UI; walidacja BE do przejrzenia.
4. Low z review: user po downgrade z premium może zobaczyć surowy processing_status w zablokowanej karcie monthly (pre-existing).
5. Stale doc comment w thread_model.dart:23-26 ("contextDescription absent on list") – już nieaktualny.

## Device QA (operator, iPhone+Android) – z QA reportu
Klawiatura+kapitalizacja w sheet (1 i 8+ itemów), drag bez szarego boxa, delete-confirm PL, wykres prep card vs Main (pixel parity), tapnięcia wszystkich reminderów wg checklisty CS-06 (kolumna Device ✓ pusta), Generate now → karta/error+Retry na koncie premium Darka, auto-gen weekly w pon. po rollout / monthly 1-go, Custom interval przeżywa restart appki.

## Lekcja procesowa
Agenci NIE mogą czekać na pełne suity w tle przed commitem (2 agentów zawisło ~7h z gotowym kodem). Zasada: implementacja = testy targetowane + commit; JEDNA pełna suita u qa-testing na końcu batcha. Patrz [[feedback-subagent-task-sizing]], [[feedback-concurrent-session-git-hygiene]].
