# PostHog audit – plan pozostałych zadań (odtworzony po padzie sesji, 2026-08-10)

Ukończone przed padem (19+1): S1..S5, A1..A12 (w tym A12=0ec26e9 niedomknięte na liście, ale w git), B1, B2, B14, A8; B3 backend scommitowany (e16f657), B3 frontend NIEDOKOŃCZONY w working tree.

## B3: Zinstrumentować domenę podsumowań
(stary task #15)

TIER B · ZRÓB · owner: data-analytics + flutter-mobile

PROBLEM: podsumowania to jeden z głównych obiecywanych efektów produktu, a nie wiadomo, czy ktokolwiek je czyta. Ostatni etap pętli terapeutycznej jest niemierzalny.

DOWODY: nigdy nie odpaliły: summary_viewed, weekly_summary_generated, weekly_summary_regenerated, monthly_audit_generated, monthly_audit_regenerated, report_generated, report_exported, summary_record_opened, summary_record_shared. Jedyne proxy to timeline_viewed 510/46 os., co nie mówi nic o samych podsumowaniach.

DO ZROBIENIA: minimum to summary_viewed (z typem: weekly/monthly/period) po stronie klienta oraz weekly_summary_generated po stronie zadania w tle - żeby dało się porównać wygenerowane z przeczytanymi.

DONE_WHEN: widać stosunek wygenerowanych do otwartych podsumowań w oknie tygodniowym.

## B4: Zdecydować o losie celów i symptomów
(stary task #16)

TIER B · SPRAWDŹ · owner: growth-analyst + ui-ux-designer

PROBLEM: dwa zbudowane obszary produktu są praktycznie nieużywane, a utrzymywanie ich kosztuje w każdym kolejnym batchu.

DOWODY (14d): cele - 4 zdarzenia u 2 osób, goal_status_changed zero (ostatnio 23.07). Symptomy - 47 zdarzeń u 7 osób; symptom_suggestion_accepted i symptom_suggestion_dismissed ciche od maja (18.05 i 13.05). Dla porównania timeline ma 46 osób.

DO SPRAWDZENIA: czy to problem odkrywalności (ludzie nie wiedzą, że to jest), czy funkcja nie jest potrzebna. Sprawdzić, czy wejścia w te ekrany w ogóle występują w top ekranach - w top 20 $screen_name nie ma ani celów, ani symptomów.

DONE_WHEN: jest decyzja per obszar: wypromować (z konkretnym miejscem wejścia) albo wygasić.

## B5: Sprawdzić, dlaczego realization_detected odpalił raz w historii
(stary task #17)

TIER B · SPRAWDŹ · owner: data-analytics

PROBLEM: mechanizm wykrywania realizacji był dowożony w dwóch batchach (Fix.2 i Fix.4) i odpalił dokładnie raz od startu zbierania danych.

DOWODY: realization_detected - 1 zdarzenie w całej historii projektu. Powiązane: flaga realization dla between_session była tematem CS w Fix.2 i ponownie w Fix.4, czyli funkcja została budowana dwa razy.

DO SPRAWDZENIA: czy detektor działa na produkcji, czy próg jest za wysoki, czy event jest emitowany w ogóle w tym miejscu, gdzie detekcja zachodzi. Sprawdzić też, czy propozycje realization_ref są generowane dla between_session (to był root cause CS-02 w Fix 4).

DONE_WHEN: wiadomo, czy to brak emisji eventu, czy brak detekcji, i jest zadanie naprawcze u właściwego właściciela.

## B6: Dodać brakujący 9. krok onboardingu do emisji
(stary task #18)

TIER B · ZRÓB · owner: flutter-mobile

PROBLEM: lejek onboardingu ma niewidoczne oczko dokładnie tam, gdzie szukamy wycieku z zadania A1.

DOWODY (14d): step_name emitują tylko 8 kroków: legal_gate (0), challenges (1), intensity (2), journey (3), modality (4), schedule (5), companion (6), lead_source (7). Specyfikacja opisuje 9 kroków. Dodatkowo istnieje onboarding_step_back 10 zdarzeń (70% od jednej osoby), więc cofanie się jest mierzone, a jeden krok nie.

DO ZROBIENIA: ustalić, który krok nie emituje step_name/step_index, i dodać emisję z tym samym kontraktem własności (step_name, step_index, duration_seconds).

DONE_WHEN: lejek pokazuje 9 nazwanych kroków, a suma przejść się domyka.

## B7: Ocenić, czy czat głosowy jest wart dalszej inwestycji
(stary task #19)

TIER B · SPRAWDŹ · owner: growth-analyst

PROBLEM: przed kolejnymi pieniędzmi w STT (AssemblyAI, rozważany Gemini Live) warto wiedzieć, czy ktoś tego używa.

DOWODY (14d vs poprzednie): voice_chat_started 1/1 os. (było 6/2 os.), voice_chat_ended 1/1 os. (było 6/2 os.), voice_agent_changed 4/2 os. (było 7/1 os.). Ekran audioChat - 1 osoba w top 20. Notatki głosowe v2 działają, ale wąsko: voice_transcription_started/completed 8 zdarzeń / 3 os. Dla porównania reflect_message_sent (tekst) 432/15 os.

DO SPRAWDZENIA: czy to kwestia odkrywalności (audioChat 1 osoba w rankingu ekranów sugeruje, że nikt tam nie trafia), czy funkcja nie jest chciana. Zestawić z kosztem AI z token_usage_log.

DONE_WHEN: jest rekomendacja: wypromować, utrzymać bez inwestycji, albo wygasić - z liczbą kosztu na aktywnego użytkownika głosu.

## B8: Znaleźć miejsce rage-clicków
(stary task #20)

TIER B · SPRAWDŹ · owner: ui-ux-designer

PROBLEM: jeden zdeterminowany użytkownik walczący z interfejsem to zwykle najszybszy sposób znalezienia realnego buga UI.

DOWODY (14d): $rageclick 33 zdarzenia, z czego 70% od jednej osoby.

DO SPRAWDZENIA: na jakim ekranie i którym elemencie występują (rozbić $rageclick po $screen_name i elemencie). Uwaga: session replay jest maskowany (mask all text/images), więc nie licz na czytanie treści - wystarczy lokalizacja elementu.

DONE_WHEN: wskazany ekran i element, plus ocena czy to bug (element wygląda na klikalny i nie jest) czy powolność.

## C1: Przejrzeć ~40 eventów, które są w kodzie i nigdy nie odpaliły
(stary task #21)

TIER C · ZRÓB · owner: flutter-mobile + data-analytics

PROBLEM: fałszywe poczucie pokrycia analitycznego - ktoś patrzy w kod, widzi event i zakłada, że temat jest mierzony.

DOWODY (nigdy nie odpaliły od startu zbierania 22.04): całe taksonomie notatek (note_editor_opened/saved/discarded/deleted), czatu tekstowego (chat_opened/message_sent/message_failed), journey_viewed + journey_day_opened, gamifikacji (achievement_unlocked, streak_screen_viewed, level_up), a także bio_viewed, analytics_screen_opened, health_check_dismissed, journal_note_created, onboarding_legal_gate_abandoned, notification_nudge_tapped/dismissed, notification_banner_dismissed, subscription_restore_*, workspace_section_expanded, workspace_item_opened, prep_card_auto_generated, monthly_audit_generated/regenerated, weekly_summary_generated/regenerated, report_generated/exported, recording_processing_*, recording_chunk_upload_failed, voice_transcription_failed, account_deletion_cancelled.

DO ZROBIENIA: przejść listę i per event zdecydować: podłączyć (bo mierzy coś ważnego - patrz zadania A3, B3, S4), albo usunąć z kodu (bo mierzy martwy feature). Nie zostawiać w limbo.

DONE_WHEN: lista jest przejrzana, każdy event ma decyzję, a martwe definicje są usunięte z kodu.

METADATA (z poprzedniej sesji):
```json
{
    "insight_emission_asymmetry":  "inapp_insight.shown/.acted lecą (5/5u tydz. 08-02), ale .generated = 0 w tych samych tygodniach - emisja generacji niedoraportowana względem wyświetleń (por. in_app_insight_detector.py:225-230). Przy przeglądzie C1 wyrównać emisję .generated albo uznać .shown za kanoniczny początek lejka."
}
```
```json
{
    "dead_prep_auto_path":  "PrepCardManager.autoGeneratePrepCard() ma zero call sites w lib/ - martwy klient endpointu POST /prep-cards/auto-generate, jedynego emitera prep_card_auto_generated. Przy C1: usunąć martwy kod klienta + wycofać event, ALBO podpiąć jeśli #34/#35 przywrócą auto-generację."
}
```

## C2: Oddzielić ruch strony marketingowej od metryk aplikacji
(stary task #22)

TIER C · ZRÓB · owner: integration-devops (+ data-analytics dla filtrów w dashboardach)

PROBLEM: każda liczba "aktywnych użytkowników" jest zawyżona ok. 3x przez ruch strony www w tym samym projekcie PostHog. Po wejściu consent-gate (25.07) web-ruch dodatkowo spadł o 85%, co stworzyło fałszywy obraz "załamania akwizycji" (patrz analytics-reports/2026-08-10-acquisition-collapse.md - task S3).

DOWODY: 14d po $os: 77 osób z Linux/Windows/macOS to web. Kanoniczny filtr zweryfikowany przez growth-analyst: properties.$lib = 'posthog-flutter' dla aplikacji, $lib='web' dla strony. Aktywni appki 14d: 80 → 92 (rośnie!), web 183 → 27 (consent-gate).

DO ZROBIENIA: 1) wszystkie insighty/dashboardy i domyślne zapytania filtrują $lib='posthog-flutter' dla metryk aplikacji; 2) zweryfikować realny ruch www w GA4 (G-DWNVZNWCT5), które odpala pre-consent i trzyma niezafałszowaną serię - UWAGA: po naprawie taska #27 (S6) GA4 też będzie za bramką, więc pull historyczny zrobić wcześniej; 3) zapisać zasadę w pamięci agenta posthog-data-extractor (już częściowo w reference_posthog_web_vs_app_split.md).

DONE_WHEN: dashboardy pokazują aktywnych aplikacji bez ruchu web, a historyczna seria ruchu www z GA4 jest ściągnięta i zarchiwizowana.

## C3: Odfiltrować ruch wewnętrzny z metryk
(stary task #23)

TIER C · ZRÓB · owner: integration-devops

PROBLEM: własne testy udają użycie produktu. Przy 127 aktywnych osobach kilka kont testowych realnie przesuwa liczby.

DOWODY (14d): $is_testflight=true - 665 zdarzeń / 3 osoby. $is_emulator=true - 165 zdarzeń / 3 osoby. Razem ok. 6% wolumenu z 13 679 zdarzeń.

DO ZROBIENIA: odfiltrować $is_testflight i $is_emulator w dashboardach oraz w domyślnych zapytaniach agenta posthog-data-extractor. Rozważyć też property internal_user ustawiane dla znanych kont zespołu.

DONE_WHEN: dashboardy i domyślne zapytania wykluczają ruch wewnętrzny, a zasada jest zapisana w pamięci agenta.

## C4: Przebudować dashboardy PostHog po naprawie taksonomii
(stary task #24)

TIER C · ZRÓB · owner: integration-devops (operator uruchamia skrypt, nie agent posthog-data-extractor)

PROBLEM: 9 dashboardów i ok. 50 insightów zbudowanych 23.04 opisuje taksonomię, której już nie ma. Pokazują puste wykresy tam, gdzie problem jest w instrumentacji, a nie w zachowaniu ludzi - to prowadzi do błędnych wniosków.

DOWODY: dashboardy 638505-638513 zbudowane skryptem scripts/posthog_build_dashboards.py. Insighty monetyzacji, gamifikacji i jakości opierają się na eventach, które nigdy nie zaczęły lecieć. W ostatnich 14 dniach pojawiło się 36 nowych nazw eventów (114 wobec 78 w poprzednim okresie) - dashboardy ich nie znają: workspace_opened, app_tour_*, consent_*, signup_*, account_*, quick_capture_*, prep_capture_*, voice_transcription_*, reflect_session_*, notification_permission_*.

ZALEŻNOŚĆ: robić PO zadaniach S1 (api_error) i A3 (lejek monetyzacji), inaczej przebudowa utrwali te same luki.

DONE_WHEN: dashboardy odzwierciedlają eventy, które faktycznie lecą, mają filtr ruchu wewnętrznego i web (C2, C3), a insighty na nieistniejące eventy są usunięte lub oznaczone jako oczekujące na instrumentację.

METADATA (z poprzedniej sesji):
```json
{
    "rename_mappings":  "notification_interest_toggled -\u003e notification_row_toggled (commit 4a20b19, 2026-07-24; schemat category/selected -\u003e key/value). Przy przebudowie dashboardów przepiąć wszystkie insighty filtrowane po starej nazwie."
}
```
```json
{
    "reflect_session_semantics":  "reflect_session_ended (backend) = finalizacja wątku (rzadka, celowa); reflect_ui_session_ended (klient, od 5b3af7d) = koniec sesji ekranowej z duration/messages_sent/end_reason. Dashboardy engagement mają używać pary reflect_session_started + reflect_ui_session_ended; NIE traktować niskiego reflect_session_ended jako buga."
}
```

## C5: Rozstrzygnąć stare eventy conversation_*
(stary task #25)

TIER C · SPRAWDŹ · owner: backend-api

PROBLEM: pozostałości starej ścieżki rozmów mieszają się z Reflect w analizach.

DOWODY (14d): conversation_message_sent 14 zdarzeń, 100% od jednego konta. conversation_started i conversation_ended - 1-2 osoby. Nowe w tym oknie, co sugeruje albo ruch testowy, albo świeżo odkopaną legacy ścieżkę.

DO SPRAWDZENIA: czy to legacy endpoint /conversations/ (stara architektura konwersacji z modelu danych), czy ruch testowy jednego konta. Jeśli legacy i nieużywane - wygasić emisję, żeby nie mieszała się z reflect_*.

DONE_WHEN: wiadomo, skąd te eventy, i jest decyzja: wygasić albo świadomie zostawić z opisem po co.

## S6: Naprawić odwróconą bramkę consent na stronie www (Meta Pixel/GA4 przed zgodą)
(stary task #27)

TIER S · owner: security-guardian (DONE) → integration-devops/operator (PENDING APPROVAL)

STAN 2026-08-10: orzeczenie GOTOWE - security-reports/2026-08-10-consent-gate-ruling.md. Zweryfikowane na żywo: Meta Pixel init+PageView bezwarunkowo w head (CRITICAL), Purchase event z fałszywą bramką typeof window.fbq zamiast window.__msM (CRITICAL), GA4 bezwarunkowo (HIGH). PostHog/Contentsquare/Ads/GTM gate'owane poprawnie. GA4+Meta były niegate'owane OD ZAWSZE, nie od 25.07.

CZEKA NA OPERATORA: wykonanie kroków 1-6 z raportu w Webflow (zmiana outward-facing na żywej stronie): 1) Meta Pixel za bramkę c.m, 2) fix guarda Purchase na window.fbq && window.__msM, 3) GA4 do loadAnalytics() za c.a, 4) GPC coverage, 5) test akceptacyjny zero calli do connect.facebook.net/googletagmanager przed kliknięciem banera, 6) bump do msconsent-1.1.0.js (nowy asset ID = eviction cache). PLUS krok 0 niezależny: jednorazowy pull historii GA4 (agregaty) PRZED schowaniem GA4 za bramkę (powiązane z taskiem #22). PLUS purge: Meta Business Data Deletion za cały okres pre-fix, GA4 purge po kroku 0 + retencja 2 mies.

BLOKADA: żadne zmiany banera zgód (np. poprawa opt-in rate) nie wychodzą, dopóki kroki 1-3 nie są live i krok 5 nie przechodzi.

DONE_WHEN: kroki 1-6 wykonane i test akceptacyjny przechodzi, albo udokumentowana decyzja operatora.

## B9: Dodać atrybucję instalacji (Install Referrer / deferred deep link)
(stary task #28)

TIER B (znalezione przy S3) · ZRÓB · owner: flutter-mobile

PROBLEM: PostHog nie umie przypisać ani jednej instalacji do strony www - 0 z 725 web-first person_id kiedykolwiek wyemitowało event aplikacji (po instalacji powstaje świeży person_id). Nie wiadomo, czy strona w ogóle konwertuje na instalacje.

DOWODY: analytics-reports/2026-08-10-acquisition-collapse.md.

DO ZROBIENIA: Play Install Referrer API na Androidzie (+ deferred deep link, np. parametr w linku ze strony do store), przekazywany jako property przy pierwszym evencie aplikacji / person property. iOS: rozważyć Apple Search Ads attribution albo parametryzowany link TestFlight/App Store.

DONE_WHEN: nowy user z instalacji ze strony ma ustawione źródło (np. person property install_source), i da się policzyć web → install → rejestracja.

## B10: Wyjaśnić diarization_failed=true na wszystkich nagraniach i niepodlinkowaną sesję uploadu
(stary task #30)

TIER B (znalezione przy S4) · SPRAWDŹ · owner: backend-api

PROBLEM 1: wszystkie 3 nagrania z okna 14d mają diarization_failed=true i brak assemblyai_transcript_id, mimo processing_status='COMPLETED'. Może to zaprojektowany fallback (Whisper bez diaryzacji), a może cicha awaria. n=3, za mało na trend, ale 3/3 to 100%.
KONTEKST: batch "STT AssemblyAI + PostHog + cleanup 2026-08-04" jest wg pamięci projektu UNCOMMITTED - najpierw sprawdzić, czy kod AssemblyAI w ogóle jest wdrożony na Heroku (prawdopodobnie nie, wtedy brak transcript_id jest oczekiwany, ale diarization_failed wymaga wyjaśnienia osobno).

PROBLEM 2: 1 z 4 completed upload_sessions ma recording_id IS NULL - krok linkowania nie podpiął nagrania. Pojedynczy przypadek, ale to dokładnie klasa błędu "completed bez efektu".

DOWODY: db-reports/2026-08-10-recording-pipeline-check.md.

DONE_WHEN: wiadomo, czy diarization_failed=100% to fallback czy regresja (i jest zadanie naprawcze jeśli regresja), oraz znana przyczyna niepodlinkowanej sesji.

## B11: Zbadać 66% nowych osób, które nigdy się nie uwierzytelniają
(stary task #31)

TIER B (znalezione przy A1) · SPRAWDŹ · owner: growth-analyst + ui-ux-designer

PROBLEM: 430 z 652 nowych osób app-only (66%, kohorta 05-01..07-26) nigdy nie emituje user_registered - anonimowe sesje ze średnio 8,4 zdarzeniami w 24h i powrotem 5,8%. To największy pojedynczy ubytek w całym lejku, większy niż cokolwiek w onboardingu.

DOWODY: analytics-reports/2026-08-10-activation-definition.md (growth-analyst 2026-08-10). Uwaga na artefakt $identify: 17 osób ma zapis bez user_registered, więc część "anonimowych" to zduplikowane person_id sprzed identyfikacji - trzeba oszacować skalę tego artefaktu zanim uzna się 66% za realne porzucenia.

DO SPRAWDZENIA: 1) ile z 430 to artefakt merge'owania $identify (pre-login person_id), a ile to realni ludzie odbici od ściany logowania; 2) co anonimowi robią w tych 8,4 zdarzeniach (do jakiego ekranu dochodzą, gdzie utykają - $screen_name sekwencje); 3) czy signup wall stoi przed jakąkolwiek wartością (czy da się cokolwiek zrobić bez konta).

DONE_WHEN: znany realny odsetek odbitych od signupu + rekomendacja (np. przesunięcie ściany logowania za pierwszą wartość / anonimowy tryb próbny) z właścicielem.

## B12: Emitować trial_started/trial_ended serwerowo z weryfikacji paragonów
(stary task #33)

TIER B (handoff z A3/#8) · ZRÓB · owner: data-analytics (emisja w posthog_service przy weryfikacji) + backend-api (jeśli potrzebny stan w DB)

PROBLEM: trial jest w całości wykrywany serwerowo (UserInfo.hadTrial z backendu; klient nie parsuje okresów introductory offer), więc trial_started/trial_ended nie mogą uczciwie lecieć z klienta. Nigdy nie odpaliły.

SPEC (od flutter-mobile, raport #8): emitować trial_started przy weryfikacji paragonu, który otwiera okres próbny, i trial_ended przy przejściu trial->paid albo wygaśnięciu - ten sam wzorzec co subscription_purchase_completed w POST /subscription_data (users.py) i/lub w godzinowym jobie subskrypcji (app/tasks/subscriptions.py). Właściwości: platform, product_id, trial_length_days jeśli znane. Uwaga: job godzinowy ma podejrzenie niedziałania (task #26/A8) - rozstrzygnąć #26 przed oparciem trial_ended o ten job.

DONE_WHEN: trial_started/ended lecą z backendu przy realnych paragonach trial, testy, commit lokalny.

## B13: Decyzja produktowa: therapy_schedule jako bramka pętli sesyjnej (7,7% adopcji)
(stary task #35)

TIER B (handoff z A5/#10) · SPRAWDŹ/DECYZJA · owner: ui-ux-designer (audyt+rekomendacja) → decyzja operatora

PROBLEM: ustawienie therapy_schedule (dzień/godzina sesji terapeutycznej) skonfigurowało tylko 138 z 1800 userów (7,7%), a gate'uje ono kartę "next session" i automatykę prep. W efekcie 92% użytkowników nigdy nie zobaczy proaktywnej części pętli terapeutycznej, niezależnie od naprawy #34.

DO ROZWAŻENIA: 1) krok "kiedy masz sesje?" w onboardingu (uwaga: onboarding ma już 8-9 kroków, task #18/B6); 2) pytanie o schedule w naturalnym momencie (po pierwszym debriefie: "kiedy następna?"); 3) de-gating karty - pokazywać wartość bez schedule z zachętą do ustawienia; 4) świadome zostawienie jak jest (prep tylko dla power userów).

DOWODY: analytics-reports/2026-08-10-prep-cards-diagnosis.md. Kontekst aktywacji: pierwszy zapis w 24h = 3.41x retencja (analytics-reports/2026-08-10-activation-definition.md) - schedule setup może być naturalnym drugim krokiem po aktywacji, nie barierą przed nią.

DONE_WHEN: rekomendacja z makietą/spec i szacunkiem wpływu, przedstawiona operatorowi do decyzji.

METADATA (z poprzedniej sesji):
```json
{
    "a12_reframe":  "Po #37 (0ec26e9): 138 wierszy \"[]\" to częściowo userzy, którzy PRÓBOWALI zapisać harmonogram (każdy niepusty zapis 422-ował niewidzialnie od zawsze). Realna chęć adopcji może być istotnie wyższa niż 7,7%. Po deployu fixa odczekać 1-2 tyg. i zmierzyć organiczny fill-rate niepustych harmonogramów ZANIM zapadnie decyzja o przebudowie bramki - może wystarczy sam fix."
}
```

## C6: Wersjonowanie deep-linków w pushach (backend nie zna wersji klienta)
(stary task #36)

TIER C (handoff z A7/#12) · ZRÓB (niski priorytet) · owner: backend-api + integration-devops

PROBLEM: notification_routes.py wysyła route/deep_link_route w każdym pushu bez świadomości wersji aplikacji odbiorcy (grep całego backendu: zero użyć app_version/min_version). Stare buildy dostają trasy, których nie mają - trafiają na error screen (od 3d99741 przyszłe buildy mają branded fallback, ale 19 obecnych starych instalacji nie).

SKALA: mała - 3 tapnięcia notyfikacji / 3 userów / 30 dni wśród old-build userów, z czego 1 realnie trafiło w nieistniejącą trasę (2.0.44, /main-page/tab/... zarejestrowane od buildu 131).

OPCJE: a) version-aware capping w notification_routes.py (wysyłać tylko trasy istniejące w wersji odbiorcy - wymaga mapy trasa->min_build i znajomości build_number odbiorcy, np. z tokena FCM/profilu); b) nudge aktualizacji dla userów na buildach starszych niż N; c) świadoma akceptacja ryzyka (skala mała, fallback od następnego release'u). Rekomendacja z #12: (a) lub (b) do decyzji przy okazji innej pracy w notification_routes.py, nie jako osobny sprint.

DONE_WHEN: decyzja podjęta i (jeśli a/b) wdrożona z testami.

