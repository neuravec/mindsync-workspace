# Reflect entry: ekran wyboru trybu (glos / tekst)

Start: 2026-09-17. Design: `Business_requirements/MS_reflect_intro/` (handoff `design_handoff_reflect_entry`).
Repo FE: `mindsync-frontend` branch `dev` (baza d3ba054). Repo BE: `MindSync` branch `main` (baza bc6ee9c).

## Decyzje operatora (2026-09-17)

1. **Kiedy ekran wyboru:** Reflect otwiera liste watkow (bez zmian). Przycisk "+" prowadzi na ekran wyboru
   trybu. Kontynuacja istniejacego watku omija ekran wyboru: watek ostatnio glosowy plus aktywne premium
   idzie prosto na glos, watek glosowy bez premium spada na tekst, watek tekstowy idzie na tekst.
2. **Premium:** gorna polowka (glos) dostaje kłodke dla uzytkownika bez premium, tapniecie idzie prosto
   na paywall z `trigger_feature=reflect_voice`.
3. **Wiersze sheeta:** tematy z kontekstu terapii (etykiety `ThreadItemModel` z kart Prep, nagran sesji,
   notatek Between Sessions). Kazdy wiersz zasiewa NOWA rozmowe. Plakietka wynika z typu karty zrodlowej.
4. **Kto zaczyna:** agent otwiera pytaniem. W tekscie babelek renderowany klientowo, w glosie `response.create`.

## Odstepstwa od handoffu (swiadome)

- Cofniecie z sesji glosowej wraca do transkryptu watku, nie do ekranu wyboru.
- Trzeci przycisk z makiety ekranu glosowego (wyglada na glosnik) pominiety.
- Dialog "odrzucic nagranie?" usuniety: tury sa zapisywane na serwerze na biezaco, wiec nic nie bylo odrzucane.

## Taski

| # | Zakres | Agent | Stan |
|---|--------|-------|------|
| BE-1 | Migracja (`modality`, `seed_source`, `seed_label`), cialo `POST /reflect/start`, pytanie otwierajace, `GET /reflect/entry-sources`, modalnosc na liscie watkow, testy | backend-api | ZROBIONE, commit d3aca01 na main, nie pushowane |
| FE-1 | Restyling ekranu glosowego na ciemny, ciemne stany laczenia i bledu, naprawa Retry, obsluga zerwanego polaczenia, `permanentlyDenied`, `response.create` za flaga, analityka | flutter-mobile | ZROBIONE, commit 8cdc1ac na dev, nie pushowane |
| BE-2 | Brakujacy `db.rollback()` w bloku embeddingow (`send_reflect_message`, `audio_user_message_add`): dzis wiadomosc zapisana, ale request 500. Zatwierdzone przez operatora | backend-api | ZROBIONE, commit 99b02f1 |
| FE-2 | Nowy ekran wyboru trybu plus sheet, trasa, klient API, model, l10n | flutter-mobile | ZROBIONE, commit e457c1e na dev, nie pushowane |
| FE-3 | Przepiecie "+", usuniecie chipow i ikonki telefonu, babelek pytania otwierajacego, routing kontynuacji wg modalnosci i premium, naprawa flagi pustego watku, PopScope, kolejnosc premium i mikrofon przed mintowaniem klucza | flutter-mobile | ZROBIONE, commity 1312682 + 8b07059 + 5ff4ab4 |
| FE-3b | Domknac po FE-1: dopisac `error_voiceConnectionLost` i klucz permanently-denied do `localizeMessageKey` w `lib/utils/localized_messages.dart`, przeniesc stale z `voice_analytics.dart` do `lib/core/analytics/analytics_events.dart` | flutter-mobile | razem z FE-3 |
| BE-3 | Zdarzenia PostHog po stronie backendu: `reflect_entry_sources_served`, `reflect_seed_rejected`, `reflect_opening_question_failed` | backend-api | ZROBIONE, commit 5479dcf |
| FE-4 | Kompleksowa instrumentacja PostHog wg kontraktu ponizej: brakujace zdarzenia lejka, konsolidacja stalych z `voice_analytics.dart` i staych FE-2 do `analytics_events.dart`, testy pilnujace ze zadna tresc terapeutyczna nie wychodzi w properties | flutter-mobile | ZROBIONE, commit 7f9f897 |
| QA | Pelny pakiet testow BE i FE, delta wobec baseline, weryfikacja czy macierz jest realnie pokryta | qa-testing | w toku |
| SEC | Audyt nowego endpointu, eskalacja pozioma na `seed_id`, bramka premium, szczelnosc analityki, RODO | security-guardian | w toku |
| INT | Kontrakt miedzywarstwowy, okno rollout gap, okno migracyjne, kolejnosc na sciezce glosowej, runbook deployu | integration-devops | w toku |
| DEPLOY | Push BE, potem `alembic upgrade head` na Heroku, potem push FE na `dev` | operator plus integration-devops | czeka na zgode |
| PROMPT | Research najlepszych praktyk promptowania terapeuty AI dla gpt-realtime, potem przepisanie promptow | general-web-search-agent plus data-analytics | po pushu |

## Twarde ograniczenia (z rekonesansu, nie do podwazenia bez dowodu)

- `reflect.py` jest importowany w `api.py` POZA guardem try/except: blad importu to crash-loop calego web dyno.
- Nie wolno zapisywac wiadomosci otwierajacej jako wiadomosc nr 1: lamie straznika pustego watku
  (`len(messages) < 2`) i zalozenia o indeksach (`messages_db[0]`, `.offset(1)`, `messages[1:]`).
- Status `ACTIVE` nic nie znaczy: nic nigdy nie zamyka watku Reflect, funkcja auto-zamykania jest martwa.
- Nie wolno wolac `GET /workspace/overview`: ten endpoint ZAPISUJE (gasi plakietki "nowe od ostatniej wizyty").
- Zaden nowy `Enum(PyEnum)`. Kolumny to `String(n)` plus stale Pythona (wzor `UploadSession`).
- Migracje na Heroku sa RECZNE. Kod musi dzialac na dyno przed migracja (degradacja, nie 500).
- Testy FE uruchamiac per katalog, calosc naraz wywala pamiec. `flutter analyze` filtrowac po `error •`.
- Zakaz obu znakow myslnika (U+2014 i U+2013) we wszystkich 7 jezykach i w komentarzach.

## Dlug techniczny odkryty przy okazji (nie w zakresie, do ticketa)

- `CLAUDE.md` mowi o `lib/ui/screens/`, realne drzewo to `lib/screens/`. Mowi tez o auto-zamykaniu
  bezczynnych rozmow, ktore nie dziala.
- `AndroidManifest.xml:7` deklaruje `Manifest.permission.CAPTURE_AUDIO_OUTPUT`, czyli nazwe stalej Javy
  zamiast nazwy uprawnienia. Cichy no-op.
- `GET /reflect/threads` gubi `has_more`, wiec uzytkownik widzi tylko 20 najnowszych watkow.
- `REFLECT_NUDGE_MINUTES` zadeklarowane i nigdy nieczytane.
- Backendowe zdarzenia `reflect_session_started` i `reflect_session_ended` sa mocno przekrzywione.

## Kontrakt zdarzen PostHog (zrodlo prawdy dla BE-3, FE-3 i FE-4)

Konwencja nazw zgodna z istniejaca: prefiks `reflect_*` dla lejka Reflect, `voice_chat_*` dla sesji glosowej.

### ZASADA TWARDA: co NIGDY nie trafia do properties

Etykieta tematu, tresc pytania otwierajacego, tytul watku, jakikolwiek fragment transkryptu, podglad
wiadomosci. To sa dane zdrowotne uzytkownika. Do PostHoga ida wylacznie identyfikatory, enumy, liczniki
i wartosci logiczne. Ta sama regula co przy instrumentacji Habit Trackera (nazwa nawyku nigdy nie wychodzi).
Kazdy nowy test instrumentacji ma to pilnowac asercja, nie komentarzem.

### Wejscie w lejek (front)

| Zdarzenie | Properties |
|---|---|
| `reflect_new_thread_tapped` | `entry_point`: `plus_button` / `empty_state_cta` / `deep_link` / `notification` |
| `reflect_mode_choice_shown` | `entry_point`, `is_premium` |
| `reflect_mode_selected` | `mode`: `voice` / `text`, `is_premium` |
| `reflect_voice_locked_tapped` | `entry_point`. Tapniecie zablokowanej polowki glosowej przez usera bez premium |
| `reflect_entry_sources_shown` | `mode`, `item_count`, `sources` (lista typow), `is_empty` |
| `reflect_entry_topic_selected` | `mode`, `source`, `is_continuation`, `position` (0-2) |
| `reflect_entry_start_fresh` | `mode`, `had_topics` |
| `reflect_entry_dismissed` | `stage`: `mode_choice` / `sheet`, `mode` (moze byc null) |

### Utworzenie i kontynuacja

| Zdarzenie | Properties |
|---|---|
| `reflect_session_started` (backend, juz rozszerzone w d3aca01) | `thread_id`, `is_new_thread`, `mode`, `seed_source`, `has_opening_question` |
| `reflect_opening_question_shown` (front, tryb tekstowy) | `source` albo `none`. Bez tresci pytania |
| `reflect_thread_resumed` (front) | `stored_modality`: `voice` / `text` / `unknown`, `resumed_as`: `voice` / `text`, `premium_fallback` (bool) |

`reflect_thread_resumed` mierzy wprost regule kontynuacji: ile razy watek glosowy spadl na tekst przez brak premium.

### Sesja glosowa (front, czesciowo juz w 8cdc1ac)

| Zdarzenie | Properties |
|---|---|
| `voice_chat_started` | istniejace `conversation_id`, plus `entry_point`, plus nowe `has_seed`, `agent_opens_first` |
| `voice_session_failed` | `stage`: `permission` / `network` / `token` / `connect` / `dropped`, `reason` ze slownika zamknietego, `entry_point`, `is_reflect` |
| `voice_chat_ended` | istniejace `conversation_id`, `duration_seconds` |

### Backend

| Zdarzenie | Properties |
|---|---|
| `reflect_entry_sources_served` | `count`, `sources`, `candidates_available`. Prawda serwerowa obok pomiaru klienckiego |
| `reflect_seed_rejected` | `reason`: `not_found` / `wrong_owner` / `soft_deleted`. Istotne dla bezpieczenstwa i jakosci danych |
| `reflect_opening_question_failed` | `reason`: `timeout` / `api_error`. Widocznosc kosztu i opoznienia |

### Pytania biznesowe, na ktore ten zestaw ma odpowiadac

1. Czy nowy ekran ruszyl adopcje glosu: `voice_chat_started` z `entry_point=mode_choice` wobec `entry_point=legacy_mic_icon`.
2. Gdzie lejek cieknie: `reflect_mode_choice_shown` do `reflect_mode_selected` do `reflect_session_started` do pierwszej tury.
3. Czy sheet nie jest pusty: udzial `reflect_entry_sources_shown.is_empty=true`. To najwieksze ryzyko tego designu,
   bo pusty sheet zamienia dwa kroki wyboru w dwa kroki tarcia.
4. Ile blokady premium generuje ten ekran: `reflect_voice_locked_tapped` wobec konwersji na paywallu z `trigger_feature=reflect_voice`.
5. Czy glos sie w ogole laczy: `voice_chat_started` wobec `voice_session_failed` w rozbiciu na `stage`.
6. Czy zasiew tematu zmienia dlugosc rozmowy: `reflect_ui_session_ended.messages_sent` w rozbiciu na `seed_source`.

### Pulapki pomiarowe (udokumentowane, nie do odkrywania na nowo)

- DAU w PostHogu jest zawyzone okolo 130 razy. Filtrowac po `$lib='posthog-flutter'`.
- Backendowe `reflect_session_started` i `reflect_session_ended` sa historycznie mocno przekrzywione
  (rzad wielkosci 24 startow na 2 konce). Nie budowac na nich lejka bez kontroli.
- Przelaczenie zakladki w `PageView` nie generuje zdarzenia `$screen`, tylko `tab_switched`.
- Dashboardy w PostHogu tworzy operator skryptem, agenci nie tworza insightow ani dashboardow.

## Decyzje z instrumentacji (2026-09-17)

- `trigger_feature` ujednolicone na **`premium_gate_reflect_voice`**, czyli wartosc juz wysylana od d3ba054,
  a nie na literal `reflect_voice` z kontraktu. Powod: ta sama sciana raportowala dwa rozne kubelki,
  a zmiana nazwy wartosci potencjalnie plynacej na produkcji jest gorsza niz odstepstwo od kontraktu.
- `reflect_ui_session_ended` swiadomie NIE niesie `seed_source`. Lista watkow nie zwraca pola zasiewu,
  wiec dla watku wznowionego property byloby po cichu nieobecne dokladnie dla sesji, o ktore chodzi.
  Pytanie biznesowe 6 realizuje sie joinem po `thread_id` z backendowym `reflect_session_started`.
- `reflect_entry_sources_shown` dostalo dodatkowo `load_failed`, poza kontraktem. Bez tego
  "klient nie zdolal pobrac" i "backend uczciwie nic nie mial" to ten sam wiersz.

## Do ticketa po tym batchu (swiadomie poza zakresem)

- **Blok voice-directora w `send_reflect_message` (linia ~932).** Ostatnie realnie osiagalne 500 w tym pliku.
  Lezy PRZED commitem handlera, wiec blad bazy w directorze wywala ture juz po zapisaniu wiadomosci usera.
  Potrzebuje wlasnego QA: `run_pipeline` dotyka Redisa i kilku tabel, a tryb bledu rozni sie zaleznie od `DIRECTOR_ENABLED`.
- **Odczyt `conversation.title` po try w `end_reflect_thread` (linia ~1270).** Commit statusu juz przeszedl,
  wiec watek jest poprawnie FINISHED, ale user widzi blad dla akcji, ktora sie udala. Dwie zmiany, nie jedna:
  rollback oraz przeniesienie odczytu tytulu do zmiennej lokalnej.
- **11 blokow niskiego ryzyka** (endpointy tylko do odczytu albo pozycje po commicie). Zaden nie moze dzis zwrocic 500.
  Warte jednego przebiegu dla spojnosci, nie z pilnosci. Kryterium odbioru: skan konczy plik na zerze.
- **Skan byl uruchamiany wylacznie na `reflect.py`.** Ten sam wzorzec niemal na pewno jest w innych modulach
  endpointow. Osobny ticket, bo triage swiadomy wywolan (commit w callerze) nie automatyzuje sie tak tanio.
- **`entry_point=notification` nigdy nie zostanie wyslane.** Push REFLECTION_INVITATION i wewnetrzny deep link
  rozwiazuja sie do tej samej trasy, wiec klient ich nie odroznia i oba licza sie jako `deep_link`. Rozdzielenie
  wymaga tagowania `pendingAction` przez handler powiadomien, czyli zmiany kontraktu deep linkow. Do czasu tego,
  join po `notification_opened` w tej samej sesji.
- **Nota kontraktowa, nie defekt:** `reflect_opening_question_failed` klasyfikuje pusta odpowiedz modelu jako
  `api_error`. Jesli kiedys pojawi sie populacja `api_error` skupiona przy niskim `elapsed_ms` przy zdrowym
  OpenAI, to bedzie wlasnie to i zasluzy na wlasna wartosc.
- `CLAUDE.md`: sciezka `lib/ui/screens/` nie istnieje (realnie `lib/screens/`), a auto-zamykanie bezczynnych
  rozmow jest opisane jako dzialajace, choc funkcja wyklucza Reflect i nie ma ani jednego wywolania.
- `AndroidManifest.xml:7`: `Manifest.permission.CAPTURE_AUDIO_OUTPUT` to nazwa stalej Javy, cichy no-op.
- `GET /reflect/threads` gubi `has_more`, sufit 20 najnowszych watkow.
- `REFLECT_NUDGE_MINUTES` zadeklarowane i nigdy nieczytane.
- Przerwanie audio przez rozmowe przychodzaca: brak obslugi w sciezce czasu rzeczywistego.
- 13 zastanych failujacych testow wizualnych w `test/ui/reflect_tab/` i 6 w `test/screens/therapy_tab/`.

## Bramka weryfikacyjna przed pushem (zadana przez operatora)

Nic nie idzie na `origin` dopoki ponizsza macierz nie jest przejsta i opisana. Kazdy punkt ma byc
zweryfikowany dowodem (test, slad w kodzie z plik:linia albo uruchomienie), nie opinia.

### A. Nowa rozmowa

| # | Sciezka | Oczekiwanie |
|---|---|---|
| A1 | "+" > wybor > glos (premium) > temat | Watek utworzony z `mode=voice` i zasiewem, klucz mintowany DOPIERO tutaj, agent otwiera pierwszy, po zakonczeniu ladujemy w transkrypcie watku |
| A2 | "+" > wybor > glos (bez premium) | Paywall od razu. ZADEN watek nie powstaje, ZADEN klucz nie jest mintowany, sheet sie nie otwiera |
| A3 | "+" > wybor > tekst > temat | Watek z `mode=text` i zasiewem, babelek pytania otwierajacego, ZERO chipow |
| A4 | "+" > wybor > tekst > "Zacznij od zera" | Watek bez zasiewu, bez pytania otwierajacego, bez chipow |
| A5 | "+" > wybor > polowka > zamkniecie sheeta | Powrot na ekran wyboru, nic nie zatwierdzone, nic nie utworzone |
| A6 | "+" > wybor > cofniecie | ZADEN watek nie powstal. To jest sedno przeniesienia tworzenia watku za wybor |
| A7 | Brak kontekstu terapii | Sheet pokazuje sam przycisk "Zacznij od zera" plus alternatywny podtytul, bez pustej listy |

### B. Kontynuacja (regula operatora)

| # | Sciezka | Oczekiwanie |
|---|---|---|
| B1 | Watek `modality=voice`, premium aktywne | Prosto na glos, ekran wyboru pominiety |
| B2 | Watek `modality=voice`, brak premium | Tekst, plus `reflect_thread_resumed` z `premium_fallback=true` |
| B3 | Watek `modality=text` | Tekst |
| B4 | Watek `modality=null` (historyczny albo przed migracja) | Tekst. Nigdy blad, nigdy glos |
| B5 | Dowolna kontynuacja | Ekran wyboru NIGDY sie nie pokazuje |

### C. Awarie i brzegi

| # | Sciezka | Oczekiwanie |
|---|---|---|
| C1 | Mikrofon odrzucony | Pytanie o mikrofon PRZED mintowaniem klucza, wiec zadna platna sesja nie jest marnowana |
| C2 | Mikrofon odrzucony na stale | Wlasny komunikat plus przycisk otwierajacy ustawienia |
| C3 | Brak sieci na ekranie wyboru | `entry-sources` pada cicho, sheet dziala, "Zacznij od zera" dziala |
| C4 | Brak sieci przy starcie | Blad, ZERO osieroconych watkow |
| C5 | Zerwane polaczenie w trakcie glosu | Ekran bledu i dzialajacy Retry, nie zamrozone "Slucham" |
| C6 | Ubicie apki w trakcie glosu | Tury zapisane, watek NIE skasowany przez GC pustych watkow |
| C7 | Aplikacja w tle w trakcie glosu | Audio leci dalej, sesja analityczna nie jest falszywie zamknieta |
| C8 | Slug wdrozony, migracja jeszcze nie | Nigdzie 500. Funkcja bezwladna, `modality` null, reszta bez zmian |
| C9 | Stary build apki, nowy backend | `POST /reflect/start` bez ciala zwraca 200 i dziala jak dotad |
| C10 | Nowy build apki, backend przed migracja | `modality` null wszedzie, wszystko spada na tekst, zero bledow |

### D. Pulapka kasowania pustego watku (najgrozniejsza w calym zakresie)

| # | Sciezka | Oczekiwanie |
|---|---|---|
| D1 | Watek zalozony pod glos, user nic nie powiedzial, wychodzi | Watek posprzatany, bo faktycznie jest pusty |
| D2 | Watek zalozony pod glos, user mowil, wychodzi | Watek MUSI przetrwac. To jest ten bug utraty danych |
| D3 | Watek tekstowy z pytaniem otwierajacym, bez wiadomosci usera | Nadal liczony jako pusty. Pytanie otwierajace NIE jest wierszem Message |

### E. Cofanie

| # | Sciezka | Oczekiwanie |
|---|---|---|
| E1 | Cofniecie z ekranu wyboru | Tam, skad Reflect zostal otwarty |
| E2 | Cofniecie ze sheeta | Ekran wyboru |
| E3 | Cofniecie z sesji glosowej | Transkrypt watku (swiadome odstepstwo od handoffu) |
| E4 | Cofniecie z czatu tekstowego | Lista watkow. UWAGA: dzis na Androidzie to wychodzi z aplikacji, bo nie ma zadnego `PopScope`. Do naprawy w FE-3 |
| E5 | Sprzetowy back na kazdym kroku | Zgodny z E1 do E4, bez wyjatkow |

### F. Analityka

| # | Sprawdzenie |
|---|---|
| F1 | Zadna etykieta tematu, tresc pytania, tytul watku ani fragment transkryptu nie trafia do properties. Asercja w tescie |
| F2 | `entry_point` poprawnie atrybuowany z kazdego wejscia |
| F3 | Zdarzenia lejka odpalaja dokladnie raz, bez duplikatow przy rebuildach |

### Kto weryfikuje

- `integration-devops`: kontrakt miedzy warstwami, okno "wdrozone ale niezmigrowane", kontrakt cofania, sciezki A i B i C8 do C10.
- `qa-testing`: oba pakiety testow, delta wobec baseline, realne pokrycie macierzy testami a nie deklaracja.
- `security-guardian`: nowy endpoint, weryfikacja wlasnosciowa `seed_id`, egzekwowanie bramki premium, brak wycieku danych zdrowotnych do analityki.

---

# Stan na 2026-09-18: bramka weryfikacyjna przeszla, werdykt NO GO, trwa naprawa

## Werdykty bramki

- `security-guardian`: **GO z warunkami.** Zero krytycznych, zero wysokich. Trzy srednie, z czego jedno nasze
  (nieograniczone wywolanie AI na `POST /reflect/start`), naprawione w 2579a9e.
- `integration-devops`: **NO GO jak zsekwencjonowane.** Jedno krytyczne (okno migracyjne), jedno wysokie
  (przechwytywanie back przez zakladke), reszta srednia i nizej.
- `qa-testing`: **NO GO.** Potwierdzil okno migracyjne niezaleznie, fizycznie usuwajac kolumny z bazy testowej
  i przepuszczajac prawdziwe trasy. 28 z 34 przypadkow macierzy uznane za realnie dowiedzione.

## Bledy, ktore popelnilem jako lead i ktore zostaly wychwycone

1. **Zapewnilem operatora, ze odroczenie kolumn w ORM czyni okno migracyjne bezpiecznym.** Nieprawda.
   Odroczenie chroni odczyt, nie zapis. ORM INSERT nazywa kazda zmapowana kolumne, a `Query.count()`
   owija pelny zestaw kolumn w podzapytanie. Zweryfikowane przeze mnie offline po raporcie audytu.
   Skutek, gdyby pushnac: 500 na tworzeniu rozmowy Reflect ORAZ dziennika ORAZ na obu trasach sesji glosowej.
2. **Wiersz A4 macierzy mowi "bez chipow"**, a implementacja pokazuje tam tematy z sheeta, zgodnie z
   zalozeniem, ktore sam opisalem operatorowi na poczatku. Zly jest wiersz macierzy, nie kod. DO POPRAWY.
3. **Cytowalem liczby bazowe z raportow agentow zamiast je zmierzyc.** Backend ma 15 zastanych failujacych
   testow, nie 14. Front mial w `test/ui/reflect_tab/` 15, nie 13. Delta batcha nadal zero w obu przypadkach.

## Decyzje operatora (2026-09-18)

- **Okno migracyjne:** przeprojektowac kod, nie obchodzic runbookiem. Wybrane rozwiazanie: kolumny zostaja
  na tabeli (wiec `create_all` i testy dzialaja), ale znikaja z mappera przez `exclude_properties`.
  Zweryfikowane offline: SELECT, `count()` i INSERT przechodza na bazie bez kolumn, pada tylko jawny
  odczyt w oslonietym helperze, czyli dokladnie tam, gdzie ma degradowac.
- **Stare watki:** watek z pustym `modality` pokazuje przy otwarciu ekran wyboru trybu, bez sheeta tematow.
  Powod: nie ma zapisanego trybu, wiec nie ma do czego wracac. Samo sie leczy po pierwszej turze.
- **Sesja analityczna a tlo:** NIE zamykac sesji przy zblokowaniu ekranu w trakcie rozmowy glosowej.
  Wymog dodatkowy ode mnie: domykac przy powrocie z tla, jesli sesji glosowej juz nie ma, zeby sierota
  byla mozliwa tylko przy twardym ubiciu procesu w trakcie polaczenia.

## Do ticketa, dodane przez bramke

- **`test_voice_fixes.py::*VoiceRAGInjection` nie dziala od dawna** (lata symbol `reflect.httpx`, ktorego ten
  plik juz nie importuje). To jedyne pokrycie kontraktu wstrzykiwania RAG do sesji glosowej, a ten batch
  zmienial wlasnie ten kod. WYSOKI priorytet.
- **`POST /api/v1/audio-v2/realtime-session` mintuje klucz OpenAI bez sprawdzenia premium.** Zastane.
  Obejscie platnego uprawnienia, przez ktore nowa klodka jest w czesci dekoracja. Wymaga wlasnego QA
  i sprawdzenia, czy zaden build w recenzji nie zalezy od obecnego ksztaltu.
- **Brak sciezki eksportu danych w calym API.** Zastane, `seed_label` poszerza to, czego nie da sie wydac.
- `test/screens/fab_flows/` nie konczy sie na zadnym drzewie, katalog jest niesprawdzalny.
- `test_worker_logging_config.py` jest zalezny od kolejnosci importow.
- `entry_point=notification` zadeklarowany i nieosiagalny: push i wewnetrzny deep link rozwiazuja sie
  do tej samej trasy. Albo otagowac w handlerze powiadomien, albo usunac z kontraktu.
- Dwie sciezki sprzatania pustego watku uzywaja roznych sygnalow pustosci (liczba wiadomosci z serwera
  kontra `lastMessagePreview`). Zgadzaja sie dzis, nic ich nie trzyma w zgodzie.
- Etykiety testow E4 w `reflect_tab_entry_flow_test.dart` mowia "E2".

## Zasada na przyszlosc, wyciagnieta z tego batcha

Twierdzenie o bezpieczenstwie wdrozenia nie jest zweryfikowane, dopoki ktos fizycznie nie odtworzyl stanu,
ktorego dotyczy. Przeczytanie deklaracji w modelu i komentarza w migracji to nie jest dowod. QA zrobil to
dobrze: usunal kolumny z bazy i przepuscil prawdziwe trasy.

## Poprawki macierzy (moje bledy w specyfikacji, nie w kodzie)

- **A4.** Bylo "bez chipow" przy "Zacznij od zera". Zle. Uzgodnione zachowanie, opisane operatorowi na
  poczatku i niezakwestionowane: przy starcie bez tematu ekran tekstowy pokazuje te same tematy
  z kontekstu terapii, ktore oferowal sheet, a generyczne startery sa awaryjnym zapasem. Implementacja
  i jej testy sa poprawne, wiersz macierzy byl zly.
- **D1.** Bylo "watek glosowy porzucony natychmiast zostaje posprzatany, bo jest pusty". Nieaktualne od
  decyzji, ze agent odzywa sie pierwszy: taki watek ma zapisana ture agenta, wiec slusznie jest zachowany.
  Oczekiwanie napisalem przed istnieniem tego zachowania.
- **C7.** Bylo "sesja analityczna nie jest falszywie zamykana". Doprecyzowane decyzja operatora:
  zamkniecie jest ODROCZONE na czas trwajacej rozmowy glosowej i wyplacane przy powrocie z tla
  z nowym powodem `voice_interrupted`. Zwykle zblokowanie ekranu poza rozmowa glosowa nadal
  zamyka sesje z powodem `backgrounded`, bez zmian.

## Zamrozona referencja przed pushem

- Front `mindsync-frontend`, galaz `dev`, HEAD **3c59439**, 9 commitow przed origin.
- Backend `MindSync`, galaz `main`, HEAD **831a65c**, 6 commitow przed origin.
- Oba drzewa czyste poza plikami pamieci agentow.

## Do checklisty wdrozenia (zebrane z raportow)

1. **Kolejnosc jest niezmienna: push backendu, potem `heroku run alembic upgrade head --app mindsync`,
   potem `heroku ps:stop run.NNNN`.** Po przeprojektowaniu opoznienie migracji kosztuje funkcje,
   a nie aplikacje, ale nadal kosztuje.
2. **Front dopiero po zielonych smoke checkach backendu.** Wysylka przed backendem nie jest awaria,
   ale funkcja jest bezwladna, a poniewaz ikonka telefonu zniknela z czatu, glos staje sie nieosiagalny.
3. **Smoke check numer jeden to `POST /api/v1/conversations/start`, czyli dziennik**, nie Reflect.
   To byl kanarek dla wady okna migracyjnego i zostaje kanarkiem.
4. **Wycofanie kodu: zostawic kolumny na miejscu.** Nie uruchamiac `alembic downgrade` w ramach
   wycofania kodu, bo zdjecie kolumn przy zywym nowym dynie odtwarza dokladnie te wade.
5. **`voice_interrupted` to nowa wartosc `end_reason`.** Cokolwiek w PostHogu wylicza te wartosci
   zamiast grupowac po nich, po cichu je zgubi, dopoki nie zostanie zaktualizowane.
6. **Device QA wymaga konta z watkami sprzed migracji.** Sciezka pustej modalnosci jest nieosiagalna
   na swiezej instalacji z nowym kontem, wiec symulator jej nie dotknie.
7. **Device QA plus: rozmowa przychodzaca w trakcie sesji glosowej** (brak obslugi na poziomie aplikacji)
   oraz zblokowanie ekranu w trakcie rozmowy (nowa sciezka odroczenia sesji).

---

# Stan na 2026-09-18: przebudowa promptu Reflect (zadanie po pushu)

## Co wywolalo zmiane

Operator: "agent jest dzis meczacy dla usera i szybko pojawia sie irytacja".
Research: `Business_requirements/MS_reflect_intro/research-ai-therapist-prompting.md`.
Propozycja: `Business_requirements/MS_reflect_intro/reflect-prompt-rewrite-proposal.md`.
Operator zatwierdzil calosc, lacznie z sekcja kryzysowa, bez przegladu klinicysty.

## Ustalenie, ktore przestawilo caly kierunek prac

Dlugosc wypowiedzi NIE byla problemem. Limit 2 do 4 zdan w glosie jest zgodny
z rekomendacja OpenAI dla Realtime API (2 do 3 zdan na ture). Problemem byla
CZESTOTLIWOSC PYTAN. SAMHSA TIP 2019 i Hartzler i in. 2010: po pytaniu otwartym
maja isc co najmniej jedna, a najlepiej dwie lub trzy refleksje, zanim padnie
kolejne pytanie. Regula "dokladnie jedno pytanie na wiadomosc" jest dobra jako
sufit, ale jako wymog w kazdej turze odtwarza pulapke pytanie-odpowiedz.
Dowod na papugowanie slow uzytkownika zbiega sie w trzech niezaleznych badaniach.

## Zakres wdrozenia (jeden commit, piec zmian plus domkniecie)

1. `.env` linia 54, nowa wartosc `REFLECT_SYSTEM_MESSAGE`.
2. `reflect.py` 113-154, zaszyty fallback (musi jechac z punktem 1, inaczej
   puste ustawienie po cichu przywraca stara osobowosc agenta).
3. `reflect.py` 1423-1427, sufiks trybu glosowego.
4. `voice_director.py` 26-50, `_DIRECTOR_PROMPT_FALLBACK`.
5. `reflect.py` 994-996, usuniety U+2014 z naglowka notatki directora.
6. `voice_director.py` 372 i 391, dwa U+2014 docierajace do modelu przez
   `format_session_context_for_prompt`, doklejane w `reflect.py:216`.

## Twarde ustalenia tego zadania

- **Zmiana jest wylacznie backendowa i dosiega WSZYSTKICH userow natychmiast,
  takze tych na starych buildach.** Prompt glosowy sklada backend i zwraca go
  klientowi, a Flutter tylko przenosi string dalej jako `instructions`
  (`reflect_chat_cubit.dart:946`, `audio_chat_cubit.dart:747`). W kodzie frontu
  nie ma ani jednego zaszytego promptu. Brak czekania na TestFlight.
- `.env` jest sledzony przez gita, wiec zmiana promptu to deploy kodu, nie flip
  konfiguracji. Migracji brak.
- Budzet: calosc 4538 na 5073 znaki, ale wszystko poza sekcja kryzysowa to
  4084 na 4096, czyli plasko. Caly przyrost kupuje bezpieczenstwo.
- Tekst juz mial zakaz em-dasha przez `_FORMATTING_SUFFIX` doklejany w
  `gpt_function`. Glos go nie mial, bo idzie przez `audio_v2.py` i tej sciezki
  nie dotyka. Regula trafila do sufiksu glosowego, nie do wspolnego promptu.

## Do ticketa, odkryte przy tej zmianie (swiadomie poza zakresem)

1. **`tone_archetype` w Reflect domysla sie na `"supportive"`** (`reflect.py`,
   ok. linia 195), a kanoniczny slownik to
   `Literal["realist","coach","friend","sage","explorer"]` (`schemas.py:1997`).
   Slowa "supportive" nie ma w slowniku w ogole. `dashboard.py:768` i
   `gamification.py:522` domyslaja sie na `"friend"`. Nowy prompt neutralizuje
   skutek klauzula `Anything else: steady and gentle`, ale zrodlo zostaje.
   Naprawa to jedna linia, ale dotyka zachowania wszystkich userow bez
   preferencji, wiec nie weszla do tego commita.
2. **Prompt directora jest zaszyty w kodzie, nie w konfiguracji.**
   `DIRECTOR_INJECTION_PROMPT` istnieje w `config.py:327`, ale jest puste, wiec
   zywy jest fallback z `voice_director.py`. Lamie to zasade zespolu
   o niezaszywaniu promptow.
3. **`{RAG_CONTEXT}` jest martwy**, podmieniany na pusty string w
   `reflect.py:190`, a prawdziwy RAG dokleja sie osobnym blokiem w
   `reflect.py:972` i `1426`. Zostawiony swiadomie.
4. **Prompt kazal modelowi podac `emergency number (local)`, nie niosac kraju
   uzytkownika**, tylko `{AI_LANGUAGE}`. Model zgadywal numer alarmowy
   z jezyka. Nowa wersja zakazuje zgadywania. Podawanie konkretnego numeru
   wymaga dolozenia kraju do kontekstu promptu, to osobne zadanie.

## Luki bez pokrycia w literaturze (zgloszone, nie zasypane wymyslem)

- Nie istnieja zadne wytyczne dla obslugi kryzysu suicydalnego w interfejsie
  czysto glosowym, bez ekranu. Cala znaleziona literatura zaklada, ze da sie
  pokazac karte z numerem. Punkt K8 propozycji jest wlasna propozycja zespolu.
- Nie istnieje nic o mechanizmie typu "director", czyli krotkich instrukcjach
  wstrzykiwanych w trakcie sesji. Brak odpowiednika w literaturze.

---

# Runda 2 promptu Reflect (2026-09-18, po realnym uzyciu wdrozonej rundy 1)

## Zgloszenie operatora

"agent jest mniej irytujacy" (runda 1 zadzialala czesciowo), ale dwie nowe wady:
agent recytuje cudze slowa z malym dodatkiem i nie ma zadnej inicjatywy; oraz przy
opcji "start fresh" otwiera rozmowe kontekstem terapeutycznym zamiast powitaniem.

## Wada 1: dlaczego agent recytowal

To byla nadkorekta rundy 1 i moja diagnoza byla NIEPELNA. Poprawienie samej definicji
refleksji nic by nie dalo, bo unieważnialy ja dwie inne linie tego samego promptu:

- `LIMITS`: "Never interpret the user's experience beyond what they have said."
  Doslowny, kategoryczny zakaz complex reflection, postawiony obok zakazu
  diagnozowania, czyli z waga reguly bezpieczenstwa.
- `PATTERNS`: zauwazenie czegos, czego user nie nazwal, wymagalo zgody, a prosba
  o zgode zjadala jedyne dopuszczalne pytanie w turze, przy limicie raz na rozmowe.
  Podstawowe narzedzie agenta obłożone oplata i limitem, wiec model go nie uzywal.

Runda 1 wdrozyla wylacznie SIMPLE REFLECTION (parafraze), pomijajac COMPLEX
REFLECTION (dopowiedzenie sensu, ktorego user nie nazwal). Potwierdzone w SAMHSA
TIP 35 rozdz. 3: "Complex refections invite clients to deepen their self-exploration",
mechanika to "make a mental hypothesis about the underlying meaning (...) and then
reflect that back (...) with your best guess". Progi liczbowe MITI NIEPOTWIERDZONE,
wiec w prompcie nie ma zadnej liczby.

**Wzorzec do zapamietania: zakaz frazy przesuwa problem, nie usuwa go.** Runda 1
zakazala pustej walidacji NA POCZATKU wypowiedzi. Wypelniacz przeniosl sie NA KONIEC
("to pierwszy krok w zrozumieniu emocji"). Runda 2 zakazuje przez KRYTERIUM
("prawdziwe o prawie kazdym"), nie przez liste zwrotow.

## Wada 2: trzy zrodla wycieku kontekstu przy "start fresh", nie jedno

1. Front `reflect_tab_screen.dart:1061` ustawia `'agentOpensFirst': true`
   BEZWARUNKOWO. **Zostawione celowo**: operator chce powitania, nie ciszy.
2. `reflect.py` ok. 1455: swiezy watek bez wiadomosci zasiewal RAG kontekstem
   terapeutycznym. Naprawione warunkiem `and seed is not None`.
3. **Najsilniejsze i nieoczywiste: blok `Therapy context: {THERAPY_CONTEXT}` jest
   w prompcie ZAWSZE, niezaleznie od RAG.** Samo wylaczenie RAG nie zamykalo wady.
   Zamyka ja dopiero jawna instrukcja otwarcia.

Naprawa glowna: `build_voice_greeting_instruction()` w `reflect_entry.py`, blok
`OPENING GREETING` doklejany gdy brak seeda ORAZ brak tury uzytkownika.

**Nazwa `OPENING GREETING`, nie `OPENING TURN`, jest wymuszona przez testy.**
Piec asercji na dokladny literal `"OPENING TURN"` w `test_reflect_entry_flow.py`
(553, 628, 1054, 1069) i `test_reflect_entry_pre_migration.py` (489), z czego trzy
asertuja NIEOBECNOSC dla przypadkow bez seeda, czyli dokladnie dla nowej sciezki.

Granica swiadomie utrzymana: wylaczamy zasiewanie OTWARCIA, nie pamiec agenta.
Kontekst terapeutyczny zostaje dostepny w dalszej rozmowie.

Sciezka tekstowa tej wady NIE MA: `opening_question` powstaje tylko przy
`seed is not None and seed.verified_owner and mode == TEXT` (`reflect.py:584`).

## Budzet

Prompt 5140 na 7202 znaki (plus okolo 515 tokenow). W glosie naliczane raz na sesje,
w tekscie przy kazdej wiadomosci. Co uciac, gdyby bylo za drogo: sekcja 3.3 propozycji
`reflect-prompt-fix-2-proposal.md`.

## Do ticketa, nowe z tej rundy

1. **`NEW_USER_GUARDRAIL` (`_therapy_helpers.py:539-545`) kasuje inicjatywe dla nowych
   userow.** Doklejany dla kont z 0 do 2 punktami danych, mowi "Your job with new users
   is to LISTEN and ASK, not ANALYZE and TELL". Klóci sie z nowa inicjatywa ORAZ
   z regula "wiekszosc wypowiedzi bez pytania" z rundy 1. Nie zmieniane, bo u usera,
   o ktorym agent nic nie wie, zgadywanie sensu jest realnie ryzykowniejsze.
   `test_voice_fixes.py:194` asertuje tresc tej stalej.
2. **`DIRECTOR_ENABLED=True` na prodzie**, mimo ze `config.py` domyslnie ma `False`.
   Wstrzykniecia directora w trakcie rozmowy DZIALAJA, wiec watek glosowy nie zostaje
   z zamrozonym promptem na cale polaczenie.
3. W glosie wiadomosc systemowa powstaje RAZ w `session_data` i nic jej pozniej nie
   aktualizuje, wiec snippety RAG nie wracaja w tej samej rozmowie. W tekscie RAG
   liczy sie od nowa przy kazdej wiadomosci. Pelna parzystosc wymagalaby RAG przez
   wstrzykniecie directora na pierwszej turze.
