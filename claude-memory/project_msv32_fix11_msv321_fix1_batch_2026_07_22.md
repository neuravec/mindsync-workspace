---
name: project-msv32-fix11-msv321-fix1-batch-2026-07-22
description: "Batch 16 itemów (MSV3.2 Fix.1.1 QA re-work + MSV3.2.1 Fix.1) — COMMITTED lokalnie BE e922bd7 + FE 3c293ac, NIE pushed; migracja cc4d5e6f7182 = nowy HEAD"
metadata: 
  node_type: memory
  type: project
  originSessionId: dce84259-de78-40b4-934e-092394dfd2be
  modified: 2026-07-22T05:36:01.704Z
---

# MSV3.2 Fix.1.1 + MSV3.2.1 Fix.1 (2026-07-21/22)

**Status: COMMITTED lokalnie, NIE pushed.** BE `main` commit `e922bd7` (38 plików), FE `dev` commit `3c293ac` (117 plików). Specy: `Business_requirements/MS_3/v3.2/fixes/MindSync Change Spec_ MSV3.2 Fix 1.3.md` (7 itemów QA re-work) + `MSV3.2.1 Fix.1.md` (9 itemów).

## Co weszło
- **CS-07 v3 (triage kart)**: mechaniczne TriageProposal 1:1 z treści kart (bez AI), bookmark per-item na 4 kartach, panel "Worth keeping?" USUNIĘTY, toggle topic/question tworzy AgendaItem (migracja danych z TopicQuestionItem), chips lazy-backfill dla starych kart, identity = (kind, source_field, source_item_index); skalarne pola mają source_item_index=NULL (FE aliasuje null↔0); legacy fallback `therapist_questions` ekstrahowany tylko gdy brak categorized_questions (mirror!). Nowe kolumny szyfrowane: session_prep_cards.action_items/breakthroughs, between_session_notes.agenda_suggestions/action_items. Sekcje niemapowane (Therapist Observations, Why This Might Matter, Thread Connection) = reference-only, zostają.
- **CS-09 (state machine sesji)**: BE — okno dopasowania debriefu (dzień kalendarzowy/48h zamiast ±12h), biweekly rollover last_occ, świeże next_session_date przy odczycie (stale kolumna), harmonogramy tylko-kalendarzowe; FE — timer minutowy w MainTabCubit + refresh po powrocie z flow (instant flip), kalendarz nie dziedziczy godziny z poprzedniej sesji, labele EN znormalizowane.
- **CS-21 (summaries)**: generate/retry ZAWSZE 200; failure = `{"status":"failed","error_code","message","can_retry","id"}` (schemas/summary.py); FE parsuje oba kontrakty; wyciek e.toString() w therapy_card_detail naprawiony; silent refresh Timeline.
- **CS-11 + FIX.03**: prompty jakościowe (bez dat/score'ów/delt) canonical W KODZIE — env vary SYMPTOM_DESCRIPTION_PROMPT i MOOD_TREND_SUMMARY_PROMPT są MARTWE (deploy note: można usunąć z Heroku).
- **CS-22**: prep input = checkbox-only; notatki tylko w kroku 2 (nowy prep_note_review_screen.dart); markery [Flagged]/[Will discuss via voice] usunięte.
- **FIX.01**: prawdziwe checkboxy w To-do; hub edycji: tytuł+opis (NOWE pole `description`, szyfrowane)+Powtarzaj.
- **Spec2 CS-01–CS-06**: "Edit"→7 języków; "added by you"; wątki bez limitu (kolejka/cap/bannery usunięte, migracja queued→open) + expander 5 jak To dos; statusy open/worked on/done + "mark as done"; kosz z Undo (odroczony DELETE po 4s, timer w singletonie); hit-targets ≥48×48 przez nowy `MsTouchTarget` (lib/widgets/ms_touch_target.dart).
- **Voice check-in (spec2 CS-07/08/09)**: preview transkryptu (audio-v2/transcribe → edycja → /health-check/submit tekstem), zero walidacji długości, iOS fix = AVAudioSession + WAV (wymaga QA na iPhone!), pusty transkrypt → prompt nagraj/napisz.

## Deploy (operator)
1. Push BE main + `heroku run alembic upgrade head --app mindsync` RAZEM (pending: cc4d5e6f7182; wcześniejsze pending aa+bb z Fix.1 nadal niezmigrowne? — sprawdź `alembic current` na prodzie przed deployem). 2. Push FE dev → Codemagic/TestFlight. 3. Env vary SYMPTOM_DESCRIPTION_PROMPT/MOOD_TREND_SUMMARY_PROMPT można usunąć. 4. QA na fizycznym iPhone: voice check-in.

## QA/Security (werdykty)
- QA: GO. BE full 4533 pass/27 fail (wszystkie 27 = baseline, zero-diff proof). FE 1254 pass/30 fail (= baseline). Kontrakty FE↔BE zweryfikowane klucz-po-kluczu.
- Security: 0 Crit/High. Backlog: MED-001 brak capu/paginacji wątków (celowe po CS-03 — dodać serwerowy sufit ~setki + paginację), Low: card_type jako Literal, _decode_safe fallback zwraca ciphertext.

## Follow-upy
- [ ] MED-001 sufit+paginacja wątków (backend-api)
- [ ] QA voice check-in na fizycznym iPhone (AVAudioSession/WAV)
- [ ] FE nie czyta `id` z failed-payloadu CS-21 (komentarz w therapy_tab_cubit zawyża gwarancję) — edge case stale PROCESSING row
- [ ] Martwy kod: HealthCheckManager.submitVoice / quickCheck(thoughtAudioPath:) bez callerów — decyzja o deprecacji przy okazji

Powiązane: [[project-msv32-fix1-phase-plan-2026-07-17]], [[postgres-enum-drift]], [[feedback-concurrent-session-git-hygiene]].
