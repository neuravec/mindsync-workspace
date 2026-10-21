---
name: project-msv32-fix2-batch-2026-07-23
description: "MSV3.2 Fix2 (QA pass 22.07): 19 itemów CS-01..CS-19 — COMMITTED lokalnie BE 8a80e81 + FE cba3f66, NIE pushed; nowa migracja dd5e6f7182a3 = HEAD; QA GO, security GO"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5b08d17d-7995-4644-a031-ea51213b8d25
  modified: 2026-07-23T08:28:33.152Z
---

# MSV3.2 Fix2 — batch 19 itemów (2026-07-23)

**Status: COMMITTED lokalnie, NIE pushed.** BE `main` = `8a80e81` (27 plików, +4628/−405), FE `dev` = `cba3f66` (109 plików). Spec: `Business_requirements/MS_3/v3.2/fixes/MSV3.2 Fix2.md` (1 DELETE, 5 FIX, 13 CHANGE). Przed batchem operator pushnął poprzedni batch (BE e922bd7 i FE 3c293ac są na originach); FE dostał pull do 68d7815 przed startem.

## Co weszło (BE)
- **CS-04**: toggle triage topic/question → `TopicQuestionItem` (nigdy AgendaItem); `linked_item_type: "topic_question_item"`. Legacy `POST /triage/submit` NIE ruszony (stare buildy, additive-only) — **decyzja do veta**.
- **CS-16**: detekcja realizacji tworzy `in_repo=False` (timeline zostaje); chips `realization_ref` dla between_session enumerują WYKRYTE wiersze Realization (statement per chip, identity zgodna z toggle — `get_detected_realizations_for_source` + `filter_visible_proposals` read-time; SELECTED stary chip z summary przechodzi). Sweep: żadnych innych auto-write'ów do 4 modułów.
- **CS-05/17**: `_pinned_then_newest()` na 5 listach; kolumny `pinned_at` ×5 + `TodoItem.reactivated_at` + `Realization.repo_added_at`; 5 endpointów `PUT .../pin-top` (toggle, 404 cross-user); done/archive/close/delete czyści pin. Migracja **`dd5e6f7182a3`** (idempotentna, down=cc4d5e6f7182) = **nowy HEAD**.
- **CS-10-BE**: `GET /workspace/todos/today` default limit 5, pinned-first.
- **CS-03**: był już shipped w e922bd7 (generacja + persystencja action_items/breakthroughs) — zweryfikowane, nie reimplementowane.
- **CS-18-AI**: Patterns zmergowane do `patterns_this_week` (pattern_alerts=[] na nowych); `significance` = anchor-or-empty z groundingiem (`get_workspace_grounding_context`: threads/goals/agenda, limit 10). **CS-19**: `emotional_tone` = "" na nowych kartach (kolumna zostaje), ton ≤1 zdanie w snapshot.
- **CS-11/12**: prompty mood-trend jakościowe + backstop `_strip_banned_digits()`. **CS-13**: weekly/monthly zmapowane na ISTNIEJĄCE pola (bez migracji): weekly at_a_glance=opis, themes_and_patterns=Worked on, symptom_shifts=How you felt, key_insights=Got done (repurposed), open_threads=RETIRED/null; monthly topic_frequency=Worked on, symptom_trends=How you felt (score'y null), breakthroughs=Realizations&breakthroughs, patterns=Got done (repurposed), movement_assessment=Where goals stand (repurposed). Puste kategorie = NULL (nie padding). Kontrakt CS-21 (200-failed envelope) nietknięty.

## Co weszło (FE)
- **CS-01**: prep = select-or-skip → jedna notatka voice/text (PrepNoteReviewScreen usunięty).
- **CS-02/18/19**: 4 karty wg appendixu — Summary + blok T&Q→To-do→Threads→Realizations (zawsze renderowany, puste = info line), renamy render-time (historyczne też), Patterns jedna sekcja, Why This Might Matter zawsze (anchor lub no-context line), Your Note, Title Case, Emotional Journey w pełni usunięte (też ze share). Therapist Observations i Thread Connection zostały ZA blokiem (appendix je pomija, proza CS-02 + "nic nie ginie" je chroni) — **decyzja do veta**.
- **CS-04/16-FE**: mixin refreshuje TopicsCubit; sekcja Realizations na Between Sessions z chipsów detekcji.
- **CS-05-FE**: usunięty jedyny kliencki re-sort (Threads). **CS-06**: "added by you". **CS-07**: chip statusu tylko open↔worked-on; done tylko przez mark-as-done. **CS-08**: animacja check-off (160ms hold + 180ms fade/collapse) + białe rzędy; fix braku `ValueKey(item.id)` (recykling State ukrywał rzędy!).
- **CS-17-FE**: Pin to top/Unpin w menu każdej listy (nowe 3-dot na Threads/Realizations/Homework), ikona pinezki, To-do↔Homework wspólny stan (cross-cubit refresh). **CS-10-FE**: Homework 5 najnowszych, checkboxy, wygląd To-do.
- **CS-09**: root cause zaciętego "Debrief" = brak `await` w gałęzi resume `TherapyFlowLauncher.launch` + tick timera bez retry fetchy; stan `betweenSessions` (okno 72h, skip gdy <3d), `noNextSessionKnown` → setup, label "After Therapy".
- **CS-14**: root cause halucynacji = DRUGI równoległy capture mikrofonu (sesja WebRTC live-preview obok AudioRecorder) → cisza → Whisper zmyśla; sesja WebRTC usunięta (wzorzec DebriefCaptureCubit), guardy `hasUsableAudio()` (min 2048 B), pusty transkrypt → prompt nagraj/napisz. Transkrypt na karcie już działał (open_ended_prompt/response). **CS-15**: statyczny nagłówek "Share your thoughts on your therapy relationship."; historyczne karty renderują zapisane pytanie.
- **CS-13-FE**: weekly 3 / monthly 5 kategorii, puste POMIJANE, score'y i open_threads nie renderują się nawet dla historycznych payloadów.

## Werdykty
- QA: **GO**. BE 4706 pass / 21 fail (= baseline, per-plik zsumowane). FE analyze 0 errorów; 1325 pass / 30 fail (= baseline). 4 spot-checki kontraktów PASS.
- Security: **GO**, 0 Crit/High/Med. LOW-001 (testy cross-user 404 pin-top) DOMKNIĘTE (+4 testy). LOW-002 backlog: prompt-hardening interpolacji tekstu usera (istniejący wzorzec).

## Deploy (operator)
1. `git push origin main` + `git push heroku main` (Heroku było 29 commitów za originem!) + **`heroku run alembic upgrade head --app mindsync`** RAZEM. Pending na prodzie: aa2b3c4d5e6f, bb3c4d5e6f70, cc4d5e6f7182, dd5e6f7182a3 (wszystkie addytywne/idempotentne; prod zweryfikowany 2026-07-17 na zz).
2. FE: `git push origin dev` → Codemagic → TestFlight/Play internal.
3. **Device-QA na fizycznym iPhone (CS-14)**: (a) voice check-in z wyraźnym zdaniem → preview = dokładnie to zdanie; (b) cisza → prompt nagraj/napisz, zero calla transcribe, nic nie zapisane; (c) transkrypt + statyczny nagłówek na zapisanej karcie; (d) 2 check-iny z rzędu = ten sam nagłówek; (e) stara karta = stare pytanie; (f) quick check-in te same testy. Plus pełny cykl Your Session przez granicę kadencji (CS-09) i pin/unpin To-do↔Homework.

## Decyzje flagged for veto (Darka)
- Legacy `/triage/submit` bez zmian (stare buildy → agenda jak dotąd).
- Therapist Observations + Thread Connection zostają jako reference za blokiem (appendix ich nie wymienia).
- CS-13: kategorie zmapowane na istniejące pola (key_insights/patterns/movement_assessment repurposed) zamiast nowych kolumn.
- Granica 3 dni CS-09 = `now >= nextSessionStart - 72h`.

## Follow-upy
- [ ] LOW-002 prompt-hardening (data-analytics, backlog)
- [ ] MED-001 z poprzedniego batcha nadal otwarty (cap/paginacja wątków)
- [ ] Martwy plik `lib/l10n/parts/part_therapy_capture.json` (stale duplikaty ARB, nieczytany przez build) — do sprzątnięcia przy okazji
- [ ] Device-QA checklist wyżej (operator, fizyczny iPhone + Android)

Powiązane: [[project-msv32-fix11-msv321-fix1-batch-2026-07-22]], [[postgres-enum-drift]], [[feedback-subagent-task-sizing]], [[feedback-memory-write-after-commit]].
