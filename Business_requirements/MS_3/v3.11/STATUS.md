# MSV3.11 – STATUS batcha (lead)

Start: 2026-09-02. Spec: `MSV3.11 - Change Spec (Grace).md` (11 itemów).
Baza: BE `main` 7dddf38 (Heroku v544), FE `dev` ce84551. Alembic HEAD prod: `pp7q8r9s0t1u`.

## Topologia gałęzi / worktree
- BE integracja: gałąź `msv3.11` w `Heroku/wt-be-int` (z main). Gałęzie robocze: `msv3.11-cs07` (wt-be-cs07), `msv3.11-cs10` (wt-be-cs10), `msv3.11-cs01` (wt-be-cs01), `msv3.11-cs02` (wt-be-cs02).
- FE integracja: gałąź `msv3.11` w `Heroku/wt-fe-int` (z dev). Gałęzie robocze: `msv3.11-fe-a` (CS-04+08), `-fe-b` (CS-05+06), `-fe-c` (CS-03 + wiersz przycisków), `-fe-d` (CS-09).
- Główne working tree (`MindSync/`, `mindsync-frontend/`) NIE są ruszane.
- ID migracji zarezerwowane: CS-07 `m311a1b2c3d4` (jeśli potrzebna), CS-10 `m311d4e5f6a7` (jeśli potrzebna), CS-01 `m311b2c3d4e5`, CS-02 `m311c3d4e5f6`. Wszystkie mają placeholder down_revision = pp7q8r9s0t1u; łańcuch linearyzowany przy integracji: CS-07 → CS-10 → CS-01 → CS-02.

## Fale
| Fala | Zadanie | Agent | Stan |
|---|---|---|---|
| 1 | CS-07 BE (recurrence) | backend-api | COMMITTED `9f828a3` (msv3.11-cs07); bez migracji; kontrakt: completion_count, last_completed_at, completed_in_current_period, current_period_start; AI context w Reflect prompt |
| 1 | CS-10 BE (therapy schedule) | backend-api | COMMITTED `5f7211b` (msv3.11-cs10); bez migracji; 3 root causes (PUT nadpisywał schedule pustką; brak self-heal dla custom-interval; DST w weekly/biweekly); kontrakt: next_session_at + next_session_timezone; PUT.schedule Optional. FLAGGED poza zakresem: therapy_tracking.py /session-state (custom-interval = "no_therapy_set") i notification_service.py _process_first_nudges (IndexError) → do CS-11 |
| 2 | CS-10 FE (tile z GET, payloady PUT) | flutter-mobile | COMMITTED `41ffb03` (msv3.11-fe-f); tile: GET nadpisuje lokalne (null tylko po udanym GET), resume hook; PUT bez schedule na ścieżkach metadanych + retry 422 z GET; "always []" już naprawione wcześniej |
| 1 | Dowody z proda (CS-10/07/01/11) | database-administrator | DONE – `db-reports/2026-09-02-msv311-prod-evidence.md` |
| 1 | CS-04 + CS-08 FE | flutter-mobile | COMMITTED `ecdf0f8` (msv3.11-fe-a); ikona phone_outlined; route HOMEWORK_REMINDER już celuje w workspace?section=todo (bez zmian); UWAGA: edytował todo_cubit.dart (togglePinTop) = możliwy konflikt z fe-b; pełny `flutter test` niewykonalny w czasie (chunki 921 testów, 0 nowych faili); hang w test/screens/fab_flows/record_session_appbar_close_test.dart (pre-existing) |
| 1b | CS-02 BE (reflect summary card) | backend-api | COMMITTED `3587c54` (msv3.11-cs02); migracja m311c3d4e5f6; 3 endpointy synchroniczne; timeline type "reflect" bez gate'u (stary klient ma fallback) |
| 2 | Integracja BE (cs07+cs10+cs01+cs02 → msv3.11) | lead | DONE `e5bacb2` w wt-be-int; łańcuch: pp7q8r9s0t1u → m311b2c3d4e5 → m311c3d4e5f6 (1 head); boot test + nowe suity zielone; PEŁNA SUITA: 5653 pass / 21 fail = baseline 1:1 (0 nowych); do domergowania jeszcze cs11 |
| 1 | CS-05 + CS-06 FE | flutter-mobile | COMMITTED `1a02134` (msv3.11-fe-b); 1 nowy klucz ARB (workspace_repeatDrawerSubtitle), reuse workspace_repeat*; PUT edit bez repeat_freq, PUT repeat tylko repeat_freq; pełny flutter test zawiesza się na tej maszynie (OOM) – QA per-plik |
| 1 | CS-03 FE (+ wiersz Summaries/Suggest) | flutter-mobile | COMMITTED `ff026ce` (msv3.11-fe-c); ReflectActionRow(onSummaries,onSuggest,isSuggestLoading,isSummariesLoading); klucze chat_summariesButton/chat_suggestButton; pełny flutter test niemożliwy (OOM) |
| 3 | CS-02 FE (sheet, karta, tile, filtr Reflect) | flutter-mobile | COMMITTED `6a7bccf` (msv3.11-fe-h); 10 kluczy ARB; bug ProviderNotFound w bottom sheet naprawiony; follow-up w toku: off-by-one pozycji kafelka vs covers_message_count + test interleavingu; NIE zmergowane jeszcze do msv3.11 |
| 1 | CS-09 FE | flutter-mobile | COMMITTED `dd91711`+`e889b0d` (msv3.11-fe-d); bez nowych kluczy ARB; zmergowane do msv3.11 `ccebd6b` |
| 1b | CS-01 BE (threads 2-level) | backend-api | COMMITTED `53436f6` (msv3.11-cs01); migracja m311b2c3d4e5; root cause: suggested_thread_id zawsze None = martwa gałąź merge; pełna suita NIE uruchomiona (QA zrobi) |
| 1b | CS-02 BE (reflect summary card) | backend-api | IN_PROGRESS |
| 2 | Integracja BE fala 1 (merge cs07+cs10 → msv3.11, testy) | backend-api | PLANNED |
| 2 | Integracja FE (merge a,b,c,e,g,f → msv3.11) | lead | DONE `3f3d76c` w wt-fe-int; 0 konfliktów; gen-l10n bez diffu; analyze: tylko 1 pre-existing error (session_setup_screen_test.dart:111); brakuje jeszcze fe-d (CS-09) i fe-h (CS-02) |
| 2 | CS-07 FE (checkbox z completed_in_current_period, historia) | flutter-mobile | COMMITTED `854cd54` (msv3.11-fe-g); powtarzalne zostają na liście otwartych (in-place swap), klucz workspace_repeatCompletionHistory |
| 2 | CS-11 audyt + fixy cykli (+ HOMEWORK_REMINDER route, + 2 leftovery CS-10) | backend-api | COMMITTED `f97d0f9` (msv3.11-cs11); audyt `CS11_NOTIFICATION_AUDIT.md`; fix: custom-interval-only w 6 generatorach + /session-state; homework self-heal; give-up 3× dla REFLECTION_INVITATION i THERAPY_RELATIONSHIP_CHECKIN; route HOMEWORK_REMINDER bez zmian (już workspace?section=todo); _process_first_nudges = martwy kod. PARKED dla Darka: stacking Pass-3, niskie SENT weekly/monthly summary, prep_card_auto_generate.py ta sama luka. Zmergowane do msv3.11 `f64216c` |
| 3 | Integracja BE kompletna (cs07+cs10+cs01+cs02+cs11 → msv3.11 `f64216c`) | lead | DONE; PEŁNA SUITA po CS-11: 5668 pass / 21 fail = baseline 1:1; do domergowania: msv3.11-sec (MED-001) |
| 3 | CS-01 FE | flutter-mobile | COMMITTED `d853a7d` (msv3.11-fe-e); ThreadCard stateful z chevronem, sub-wątki oldest-first, createThread refetch; klucze workspace_threadSubCount (ICU plural), workspace_threadSubThreadsTitle |
| 3 | CS-02 FE | flutter-mobile | PLANNED (po kontrakcie CS-02 BE + CS-03 row) |
| 4 | security-guardian (BE, diff 7dddf38..f64216c) | security-guardian | DONE: GO, 0 Crit/High; MED-001 brak throttle na POST /summarize (fix w toku na msv3.11-sec), LOW-001 TOCTOU duplikat karty, LOW-002 time_zone niewalidowany (backlog). Raport `SECURITY_REVIEW_MSV311.md` |
| 4 | Fix MED-001 + LOW-001 | backend-api | COMMITTED `066647f` (msv3.11-sec) → zmergowane do msv3.11 `c0a6d61`; + `728d48b` (em-dash w promptcie → en-dash) = FINALNY HEAD BE; 3 settings: REFLECT_SUMMARY_MIN_NEW_MESSAGES_REPEAT=2, REFLECT_SUMMARY_MIN_INTERVAL_SECONDS=120, REFLECT_SUMMARY_DAILY_LIMIT=20; nowe kody: reflect_summary_too_soon (400/429), reflect_summary_daily_limit (429); PEŁNA SUITA KOŃCOWA na c0a6d61: 5680 pass / 21 fail = baseline 1:1 (0 nowych) |
| 4 | integration-devops kontrakty (BE c0a6d61 ↔ FE ccebd6b + fe-h 6a7bccf) | integration-devops | DONE: GO; 1 MISMATCH (2 nowe kody throttle niezmapowane w cubicie – fix w toku na fe-h), 1 RISK (updatedAt required vs Optional – fix w toku). Raport `CONTRACT_REVIEW_MSV311.md` |
| 3 | Integracja FE kompletna (a,b,c,d,e,f,g,h → msv3.11 `7f62e99`) | lead | DONE; gen-l10n bez diffu; analyze: tylko pre-existing error |
| 4 | qa-testing FE (per katalog, wt-fe-int @7f62e99) | qa-testing | IN_PROGRESS |
| 5 | Deploy BE | lead (zgoda operatora 2026-09-02) | DEPLOYED: push 7dddf38..728d48b → Heroku **v545** (12:33:43 +0200), `alembic upgrade head` przez `heroku run --no-tty` ~45 s po release (pp7q8r9s0t1u → m311b2c3d4e5 → m311c3d4e5f6, potwierdzone `alembic current`); web/worker/scheduler up; logi: 0 Traceback, 0 5xx, 0 H1x; generatory zarejestrowane w workerze |
| 5 | Deploy FE | lead | PUSHED: dev ff ce84551..587f572 → origin/dev (2026-09-02 ~12:40 +0200) → Codemagic auto-version → TestFlight / Play internal (~30 min). Device-QA wg listy poniżej po pojawieniu się builda |

## Checklist deployu (do wykonania TYLKO za zgodą operatora)
1. BE: w `wt-be-int` (gałąź msv3.11) `git log main..msv3.11` = cały batch. NAJPIERW migracje na prodzie: `heroku run alembic upgrade head -a mindsync` – muszą przejść 2 addytywne migracje: `m311b2c3d4e5` (threads.parent_thread_id + narrative) i `m311c3d4e5f6` (tabela reflect_summary_cards). Bez migracji nowy kod = 500 na wątkach i Reflect summary (nie crash-loop bootu, ale degradacja).
2. BE: `git checkout main && git merge --ff-only msv3.11` (w wt-be-int lub main tree po sprawdzeniu, że main tree jest czysty) → `git push origin main` = NATYCHMIASTOWY deploy Heroku (auto-deploy z GitHuba). Procfile bez zmian, requirements bez zmian.
3. Weryfikacja: `heroku releases -a mindsync -n 3`, `heroku ps -a mindsync` (web/worker/scheduler up), `heroku logs -a mindsync -n 300` pod Traceback/UndefinedColumn/H10; log workera "registered generator(s)".
4. FE: w `wt-fe-int` `git checkout dev && git merge --ff-only msv3.11` → `git push origin dev` → Codemagic → TestFlight/Play internal (~30 min). Stare buildy pozostają kompatybilne (API addytywne; nowy typ timeline "reflect" ma fallback w starym kliencie).
5. Device-QA (iPhone + Android) wg listy z raportów agentów – patrz sekcja "Device-QA" poniżej (uzupełniana).

## Device-QA (iPhone + Android, po deployu BE i buildzie FE) – skonsolidowane z raportów agentów
1. CS-04: Reflect → ikona słuchawki w wierszu inputu, tap = voice mode jak dotąd, spinner isMicLoading.
2. CS-08: Main bez modułu Homework; push HOMEWORK_REMINDER (cold + warm start) ląduje na Workspace → To-do; brak crasha na Main u istniejącego usera.
3. CS-03: nowy wątek → chipy startowe automatycznie, brak wiersza przycisków; po pierwszej wiadomości wiersz Summaries | Suggest; po odpowiedzi AI chipy NIE pojawiają się same; Suggest → spinner → chipy "Pomocne pytania"; ponowny Suggest odświeża.
4. CS-05/06: menu ⋯ na zadaniu To-do ma "Repeat" (inne moduły nie); drawer: tytuł, subtext, 4 wybory z preselekcją, Save; pill na każdym zadaniu, nowe = "Nie powtarzaj"; edycja tekstu nie kasuje repeat.
5. CS-07: zadanie daily odhaczone zostaje na liście (nie idzie do "Zrobione") z podpisem "Zrobione 1× · ostatnio …"; odhacz ponownie = cofnięcie; zmiana daty urządzenia na jutro + odświeżenie = znów nieodhaczone, licznik zostaje; jednorazowe zadanie nadal idzie do archiwum.
6. CS-09: Main → Mood trend: suwak zamiast paska w każdym wierszu; przesunięcie odsłania "Update rating" tylko pod tym symptomem; powrót do wartości chowa przycisk bez zapisu; potwierdzenie = spinner i zapis; chevron w okrągłym przycisku; rozwinięcie = narracja + wykres, bez suwaka.
7. CS-10 (każdy tryb: weekly, biweekly, custom interval, custom data): ustaw sesję → kafelek Main pokazuje datę i godzinę; force-quit + reopen = nadal; zmiana strefy czasowej urządzenia = ta sama chwila w nowym czasie; zmiana samej częstotliwości lub custom session NIE kasuje wpisów cyklicznych; brak pusha "ustaw termin" gdy termin ustawiony; powiadomienia sesyjne wg daty/godziny.
8. CS-01: Workspace → Wątki: istniejące wątki jak dotąd + chevron; akcept propozycji wątku pasującej treścią do istniejącego = sub-wątek pod nim (bez duplikatu tytułu), z narracją; niepasujący = nowy main; sub-wątek → detail z narracją; "+ Dodaj wątek" i "Domknięte wątki" działają.
9. CS-02: Reflect z ≥2 wymianami → Summaries → pop-out z PL copy verbatim → "Not yet" zamyka → "Yes, summaries" spinner → karta 5 sekcji; zapis elementu (bookmark) ląduje w Workspace; zamknięcie wraca do rozmowy; kafelek "Your Reflect summary was generated" między objętymi a nowymi wiadomościami; tap kafelka → karta na Timeline → back wraca do rozmowy; Timeline chip "Reflect" filtruje; usuń/przywróć; ponowne Summaries po ≥2 nowych wiadomościach i ≥120 s tworzy drugą kartę; za wcześnie = komunikat inline, limit dzienny = toast.
10. CS-11: log workera po deployu "registered generator(s)"; przyrost notification_moments bez ADD_THERAPY_DATE dla userów z terminem; cotygodniowe REFLECTION_INVITATION/THERAPY_RELATIONSHIP_CHECKIN gasną po 3 nieodebranych.

## Decyzje lead
- CS-01 backend: dopasowanie AI także dla ręcznego "+ Dodaj wątek" (spec pkt 6 vs "manual = main") – do potwierdzenia przez operatora.
- CS-02 backend: karta idzie przez istniejący mechanizm triage proposals (nowy TriageCardType), więc matching wątków z CS-01 stosuje się automatycznie.
- Deploy tylko za jawną zgodą operatora (push = prod).

## Dowody z proda (DBA 2026-09-02, skrót)
- Prod alembic = pp7q8r9s0t1u, zero dryfu schematu w tabelach batcha.
- CS-10: zgłaszająca ma zapisane TYLKO `therapy_frequency='biweekly'`; `therapy_schedule` puste, `next_session_date` NULL, custom puste. 12/1810 userów ma jakikolwiek harmonogram; 7 userów ma harmonogram i NULL w next_session_date (recompute cicho pada). Generatory sesyjne działają dla tych 12. Guard v544 (ADD_THERAPY_DATE) trzyma.
- CS-07: w prodzie 1 powtarzalne zadanie (DONE, nie odnowione); reset = stały offset od done_at, read-triggered, bez crona.
- CS-01: brak kolumny parent; thread_sources 1:1 (merge nigdy się nie wydarzył); Grace ma 26/64 otwartych wątków, klastry po 2-3 sekundy od siebie = duplikaty.
- CS-11: REFLECTION_INVITATION/THERAPY_RELATIONSHIP_CHECKIN ~1805 userów/tydzień, 99.97% wygasa; 85% wolumenu 14d w 4 dniach-burstach; FCM 139/1835 (7.6%, spadek z 13.4% w lipcu); users.last_login nie nadaje się do "aktywnych".

## Otwarte
- (spec) GET /workspace/todos/today bez wołającego po CS-08 – zostaje, oflagowany.
- (spec) parked: MSV3.10 CS-01 (mic conflict), CS-03 (Documents).
