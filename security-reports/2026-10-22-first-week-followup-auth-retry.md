# Audyt bezpieczeństwa: follow-up pierwszego tygodnia i ponowienie po 401 (2026-10-22)

Zakres: przegląd read-only przed wdrożeniem dwóch gałęzi.

- Backend `MindSync`, gałąź `fix/first-week-followup-404-plan`, commit `ea396f5`, diff względem `main` (5 plików, 316 linii dodanych).
- Frontend `mindsync-frontend`, gałąź `fix/first-week-followup-and-main-loops`, commity `069db2f` i `b3b8920`, diff względem `dev` (25 plików).

Kodu nie edytowałem. Testów nie uruchamiałem (przegląd statyczny diffu i kodu wokół niego).

## Podsumowanie

Werdykt: **można wdrażać**. Brak znalezisk Critical i High.

| Severity | Backend | Frontend |
|---|---|---|
| Critical | 0 | 0 |
| High | 0 | 0 |
| Medium | 0 | 1 (FE-M1) |
| Low | 1 (BE-L1) | 3 (FE-L1, FE-L2, FE-L3) |

Nowa ścieżka backendu nigdy nie podaje cytatu, a pytanie ogólne i spokojne to ten sam ciąg znaków, więc odpowiedź nie zdradza tonu ani sygnału kryzysowego. Ponowienie po 401 na froncie jest dobrze ograniczone (jedno ponowienie, ten sam uid, bez FormData). Ma jedną lukę w obronie warstwowej: wspólne odświeżanie tokena nie jest przypisane do konta (FE-M1). Scenariusz wymaga zbiegu trzech mało prawdopodobnych warunków, dlatego Medium, a nie High. Poprawka ma kilka linii i zalecam ją przed pushem na `dev`, choć nie blokuje.

---

## Część 1: backend (`ea396f5`)

### (a) Cytat i treść kryzysowa (H-1, M-2, M-6, D-L1)

Sprawdzone w `app/services/first_week/follow_up.py`:

- `_question_from_steps` zwraca wyłącznie `_generic(language)` albo `_calm(language)`. Oba budują `ResolvedQuestion(question=_fixed_question(language), quoted=False)`, czyli bajt w bajt ten sam stały ciąg z allowlisty (H-1). Żadna nowa gałąź nie czyta `first_week_crud.get_follow_up`, elementu pamięci Orki ani transkryptu. Cytatu nie da się więc podać, nawet gdy kontrole M-2 i M-6 (które dotyczą tylko cytatu) byłyby niespełnione.
- Ton łagodny po sygnale kryzysowym: `_tone_is_standard` zwraca False przy błędzie (fail closed), a wtedy idzie pytanie spokojne. Ponieważ jest identyczne z ogólnym, ani treść, ani `quoted`, ani kod statusu nie zależą od tonu.
- Kod 200 albo 404 w nowej ścieżce zależy tylko od `steps_offer_follow_up`, a ta od `step_plan.cta_for(key, first_talk_done)`, które nie czyta tonu (sprawdzone w `step_plan.py:245`). `load_steps` jest tylko do odczytu (bez `commit`/`add`), loguje bez uid. Nowa ścieżka nie tworzy więc śladu zależnego od tonu w Postgresie ani w logach (D-L1 bez zmian).
- `POST /reflect/start` z `seed_source=first_week_followup` (`reflect.py`, `_start_first_week_follow_up`) bierze pytanie z `resolve_follow_up` po stronie serwera; klient go nie przysyła. Zdarzenie `reflect_session_started` ma te same właściwości dla każdego rodzaju pytania. Otwarcie głosowe (`resolve_thread_opening`) już wcześniej spadało na pytanie ogólne/spokojne poza dniem talk; nowa ścieżka daje ten sam wynik.
- Ponieważ wątek follow-up jest teraz osiągalny w więcej dni planu, sprawdziłem, czy `seed_source=first_week_followup` daje gdziekolwiek zwolnienie z limitów: nie (jedyne odwołania to `reflect.py`, `follow_up.py` i schemat Literal).

Wynik: OK.

### (b) Scoping po current_user

- `GET /first-week/follow-up` (`first_week_follow_up.py:60-67`) i `POST /reflect/start` (`reflect.py:998`) mają `Depends(deps.get_current_user)`; uid trafia do `resolve_follow_up` tylko z tokena. Brak parametru id.
- `steps_offer_follow_up` woła `load_steps(db, user_id, now)` z tym samym uid; `load_steps` czyta kotwicę, strefę czasową i stan planu po `user_id`.
- Brak nowego wejścia od klienta. Mass assignment niemożliwy.

Wynik: OK.

### (c) Logi

- Nowy log w `_first_week_http.py` (`_log_if_slow`): `"[FirstWeek] slow response on %s: %d in %d ms"` z `self.path`, czyli szablonem trasy FastAPI (np. `/first-week/probe/{user_id}`), nie z faktycznym URL. Nie ma uid, query stringa, nagłówków ani treści. Test `test_first_week_http_slow_log.py` to sprawdza na trasie z parametrem uid. Owinięte w `try/except`, nie przerwie odpowiedzi. OK.
- BE-L1 (Low) poniżej dotyczy innego nowego logu, w `follow_up.py`.

### (d) Boot-safety

- Na poziomie modułu dochodzą tylko stałe (`STEPS_SERVICE_MODULE`, `STEPS_READER_NAME`, alias typu) oraz `import time` w `_first_week_http.py`.
- `step_service` jest ładowany przez `importlib.import_module` w `_default_steps_reader` w `try/except`; błąd importu daje False, czyli 404 jak dotąd.
- `from app.services.first_week import step_plan` jest wewnątrz funkcji, poza jej `try`, ale cały `resolve_follow_up` jest w `try/except` i zwraca 503 (`UNAVAILABLE`). W `reflect.py` wyjątek daje zwykły wątek. Nic z tej zmiany nie jest osiągalne przy imporcie ani w lifespan.
- Brak modeli, migracji i zmian enumów.

Wynik: OK.

### BE-L1 (Low): nowy log ostrzeżenia zawiera Firebase UID

- Lokalizacja: `app/services/first_week/follow_up.py`, `steps_offer_follow_up`, `logger.warning("[FirstWeekFollowUp] steps read failed for user %s (%s)", user_id, type(exc).__name__)`.
- Opis: UID w połączeniu z kontekstem „first week follow-up” mówi, że konto jest w pierwszym tygodniu aplikacji. Treści i nazwy wyjątku poza typem brak. To zgodne z resztą pliku (te same linie dla `plan read failed`, `display check failed`), a `step_service` loguje świadomie bez uid (L-5).
- Wpływ: minimalny, pseudonimowy identyfikator w logach Heroku.
- Zalecenie: przy okazji usunąć uid z tej linii, tak jak w `step_service` (L-5). Nie blokuje. Właściciel: backend-api.

---

## Część 2: frontend (`069db2f`, `b3b8920`)

### Przebieg ponowienia po 401 (`lib/api/dio_client.dart:127-170`, `:234-262`)

Sprawdzone zachowania:

1. **Pętle.** Ponowienie ma w `extra` `authRetried401: true` i `retryOn403: false`, przechodzi przez ten sam interceptor, więc drugi 401 i 403 wracają do wołającego. Najgorszy przypadek: 403, ponowienie dla 403 dostaje 401, to jeszcze jedno ponowienie (3 żądania), dalej koniec. Ograniczone. Test `a second 401 goes back to the caller` to potwierdza.
2. **Wylogowanie.** Gdy nikt nie jest zalogowany, `sameAccount` jest false, więc nie ma ani odświeżenia, ani ponowienia. Gdy wylogowanie nastąpi w trakcie `getIdToken(true)`, warunek z linii 143 (`_signedInUid() == sentForUid`) odrzuca ponowienie. `clearAuthorization()` zeruje `_authorizationUid`, więc linia 147 nie ustawi nagłówka domyślnego. Między linią 143 a `_dio.request` nie ma `await`, wyścigu w tym miejscu nie ma.
3. **Zmiana konta, gdy żądanie było w drodze.** `sentForUid` (A) różny od `uidNow` (B): brak ponowienia. Test jest.
4. **Ponowienie przechodzi przez `onRequest`.** `_applyAuthorization` ponownie odczytuje uid i nadpisuje nagłówek tokenem z `getToken()` bieżącego konta. To dobra właściwość: zwykle nagłówek odpowiada aktualnie zalogowanemu kontu, nie temu z odświeżenia. Zob. jednak FE-M1.
5. **FormData** pominięte (body nie da się wysłać drugi raz). Strumieni jako body w `lib/api` nie znalazłem.
6. **Bezpieczeństwo POST.** 401 pochodzi z `deps.get_current_user` (`app/api/deps.py:35`), czyli przed wykonaniem endpointu, więc ponowienie nie dubluje skutków. Inne 401 w backendzie są w `clinician.py` i webhooku Loops, których aplikacja nie woła.
7. **Wyciek tokena do logów i PostHoga.** Nowe logowanie to tylko `Fimber.d("... ${refreshError.runtimeType}")`. Token nie trafia do `RecordingDebugLog`, PostHoga ani `ApiException` (`_handleError` buduje komunikat ze statusu i `err.message` Dio, bez nagłówków). OK.
8. **Konto wyłączone lub cofnięty refresh token.** `getIdToken(true)` rzuca wyjątek, 401 wraca do wołającego, brak pętli.

### FE-M1 (Medium): wspólne odświeżanie tokena nie jest przypisane do konta

- **Severity:** Medium (obrona warstwowa reguły B-4; nie blokuje, zalecana poprawka przed pushem na `dev`).
- **Lokalizacja:** `mindsync_app/lib/api/dio_client.dart:246-262` (`_refreshTokenShared`), użycie w `:141-149`; `clearAuthorization()` w `:203-206`.
- **Opis:** `_lastRefresh` jest sprawdzany po uid, ale `_tokenRefresh` (odświeżanie w toku) nie. Jeśli odświeżanie trwa dla konta A, a 401 przyjdzie dla żądania konta B, B dostaje future A. Po jego zakończeniu warunek z linii 143 porównuje bieżący uid z `sentForUid` żądania B (oba B), więc przechodzi. Wtedy:
  - nagłówek żądania B dostaje token A (linia 144),
  - jeśli `init()` zdążył ustawić nagłówek domyślny dla B (`_authorizationUid == B`), nagłówek domyślny klienta też dostaje token A (linia 148).
  Zwykle `onRequest` nadpisze nagłówek ponowienia tokenem B z `getToken()`. Gdy jednak `getToken()` dla B się nie uda (przejściowy błąd, ten sam, który ta zmiana naprawia), fallback z `_applyAuthorization` zostawia nagłówek, bo `_authorizationUid == B`. Żądanie B idzie wtedy z tokenem A. Ten sam token A zostaje też nagłówkiem domyślnym dla kolejnych żądań B z nieudanym `getToken()`. Dodatkowo `clearAuthorization()` nie czyści `_tokenRefresh` ani `_lastRefresh`, więc token A zostaje w pamięci do 30 s po wylogowaniu (z uwagi na klucz po uid nie zostanie wtedy użyty dla innego konta).
- **Wpływ:** zapis danych B (np. wiadomość Reflect, notatka) na koncie A albo odczyt danych A w sesji B. Dane zdrowia psychicznego dwóch osób na wspólnym urządzeniu. Dokładnie tego zabrania B-4.
- **Dlaczego Medium, a nie High (uzasadnienie):** potrzebne są jednocześnie: (1) wymuszone odświeżanie dla A wciąż w toku, (2) w tym czasie wylogowanie A i pełne logowanie B przez Apple/Google OAuth (kilka do kilkunastu sekund, wymaga sieci, której brak zwykle zawiesza też odświeżanie), (3) 401 na żądaniu B tuż po świeżym logowaniu, (4) dla gałęzi z wysłaniem tokena A: nieudany `getToken()` dla B. Testy nie pokrywają tego przypadku. Prawdopodobieństwo jest bardzo małe, ale skutek dotyczy danych zdrowotnych innej osoby, a poprawka jest tania.
- **Odtworzenie (test, bez kodu exploita):** w `dio_client_authorization_test.dart` zasymulować `refreshToken()` dla uid A jako niezakończony `Completer`, przełączyć `uid` na B, zwrócić 401 na żądaniu B, dokończyć Completer tokenem A i sprawdzić nagłówek ponowienia oraz `_dio.options.headers` przy rzucającym `getToken()`.
- **Remediacja (owner: flutter-mobile):**
  1. Przypisać odświeżanie w toku do konta: `({String uid, Future<String> future})? _tokenRefresh` i współdzielić je tylko przy `running.uid == uid`; inaczej uruchomić nowe.
  2. W `AuthService.refreshToken()` po `await user.getIdToken(true)` sprawdzić, że `_auth.currentUser?.uid == user.uid`; jeśli nie, rzucić wyjątek.
  3. W `clearAuthorization()` wyzerować `_tokenRefresh` i `_lastRefresh`.
  4. Testy: odświeżanie w toku dla A, a 401 dla B, nie współdzieli tokena; `clearAuthorization` czyści pamięć odświeżenia; zmiana konta w trakcie odświeżania nie ponawia (dla wariantu, w którym konto zmienia się między wysłaniem 401 a końcem odświeżania).

### FE-L1 (Low): brak testów wyścigów w trakcie odświeżania

- Lokalizacja: `mindsync_app/test/api/dio_client_authorization_test.dart`, grupa `401 resend`.
- Testy obejmują zmianę konta przed 401, ale nie zmianę konta ani wylogowanie w trakcie `refreshToken()` (linia 143) ani przypadek z FE-M1. Dopisać razem z poprawką FE-M1. Owner: qa-testing albo flutter-mobile.

### FE-L2 (Low): ponowienie nie kopiuje wszystkich opcji żądania

- Lokalizacja: `dio_client.dart:150-161` (i istniejąca ścieżka 403 w `:111-121`).
- `Options` w ponowieniu nie przenosi `responseType`, `contentType`, `sendTimeout`, `validateStatus`. W `lib/api` wszystkie żądania używają JSON, więc dziś bez skutku. To kwestia poprawności, nie bezpieczeństwa; przy przyszłym żądaniu bajtowym ponowienie mogłoby źle zinterpretować odpowiedź. Rozważyć `e.requestOptions.copyWith(...)` i `_dio.fetch`. Owner: flutter-mobile.

### FE-L3 (Low, wcześniej istniejące): logowanie pełnego wyjątku przy pobieraniu tokena

- Lokalizacja: `dio_client.dart:124` (`Fimber.d("Error refreshing token: $e")`) i `:227-228` (`RecordingDebugLog ... 'TOKEN FETCH FAILED: $e'`).
- Nie zmienione w tej gałęzi. Wyjątki Firebase nie zawierają tokena, ale `RecordingDebugLog` bywa eksportowany. Dla spójności z nową linią logować `runtimeType`. Owner: flutter-mobile, backlog.

### Właściwości PostHog

| Zdarzenie | Nowe właściwości | Ocena |
|---|---|---|
| `first_week_plan_failed` | `failure_reason` (enum 9 wartości), `http_status` (int, opcjonalnie), `source` (`home_plan`/`main_steps`) | OK. Enum i liczba, bez detail, komunikatu i body. `McAnalytics.weekLoadFailed` mapuje nieznaną wartość na `unknown`. |
| `follow_up_failed` | `failure_reason`, `http_status` | OK. Zdarzenie istniało już wcześniej. |
| `follow_up_unavailable` | `fallback: reflect_new` | OK. Jedna stała wartość. |

Czy to zdradza zdrowie lub terapię: nie. Przynależność do pierwszego tygodnia i sam ekran follow-up były już widoczne w istniejących zdarzeniach. 404 z backendu nie zależy od tonu ani od kryzysu (patrz część 1a), więc `follow_up_unavailable` nie jest kanałem bocznym dla sygnału kryzysowego. `http_status` może przyjąć wartość 403, ale `art9_consent_required` nie dotyczy tych tras (bramka Art. 9 jest na zapisach harmonogramu terapii), więc nie ujawnia stanu zgody. Guard `test/support/reflect_analytics_guard.dart` dopuszcza dokładnie te klucze i wartości oraz typ `int` dla `http_status`.

### Fallback 404 do nowego wątku Reflect a zgoda ART9 i bramki

- `follow_up_reflect_bridge.dart` otwiera `openTabDeepLinkInPlace(MsRoutes.reflectNewThreadRoute)`, czyli `/main-page/tab/reflect?new=true`. To ta sama trasa co już istniejący krok `reflect_new` na Main (`mc_week_steps.dart:212`), Quick check-in (`quick_check_in_screen.dart:140`) i ekran pamięci Orki (`orca_memory_screen.dart:185`). Nie powstaje nowa droga do Reflect.
- Ekran follow-up jest osiągalny tylko z aplikacji po zalogowaniu i przejściu bramki prawnej, a zakładka Reflect stosuje swoje zwykłe bramki (limity Free, premium dla głosu, uprawnienia mikrofonu). Bramka Art. 9 w backendzie dotyczy zapisów harmonogramu terapii i nie jest omijana. Fallback nie przekazuje seed ani pytania, więc wątek jest zwykły.
- Wynik: brak obejścia zgody ani bramek.

### Pozostałe zmiany frontu (krótko)

- `main_tab_cubit.dart`: zatrzymanie minutowego zegara w tle i rzadsze `GET /debriefs/latest`. Zmniejsza liczbę żądań z wygasłym tokenem w tle. Bez uwag.
- `therapy_flow_launcher.dart`: statyczna blokada `_fetchingLatest` z timeoutem 8 s, zwalniana w `finally`. Brak ryzyka trwałej blokady. Bez uwag bezpieczeństwa.

---

## Lista priorytetów

1. Critical: brak.
2. High: brak.
3. Medium, zalecane przed pushem frontu na `dev`: FE-M1 (flutter-mobile) plus testy FE-L1.
4. Low, backlog: BE-L1 (backend-api), FE-L2, FE-L3 (flutter-mobile).

## Werdykt

**Można wdrażać** obie gałęzie: brak znalezisk Critical i High. Backend można wypchnąć bez warunków. Na froncie zalecam dołożyć poprawkę FE-M1 (kilka linii i dwa testy) przed pushem na `dev`, bo ta gałąź trafia od razu na TestFlight, a luka dotyczy reguły B-4 (token jednego konta w żądaniu drugiego). Nie traktuję tego jako blokady, bo scenariusz wymaga zbiegu kilku mało prawdopodobnych warunków (uzasadnienie w FE-M1). Po poprawce chętnie zweryfikuję diff.

---

## Weryfikacja poprawki (commit `651f263`, diff względem `b3b8920`)

Przegląd read-only diffu `lib/api/auth_service.dart`, `lib/api/dio_client.dart` i testów.

**FE-M1: zamknięte.**

- `_tokenRefresh` to teraz `({String uid, Future<String> future})`. Odświeżanie w toku jest współdzielone tylko przy `running.uid == uid`, a 401 innego konta uruchamia własne odświeżanie. `finally` z `identical` nie skasuje cudzego wpisu.
- Po `await` `_refreshTokenShared` rzuca `StateError`, gdy zalogowane konto nie jest już tym uid. Wyjątek łapie istniejący `catch (refreshError)`, więc nie ma ponowienia ani zmiany nagłówka domyślnego.
- `AuthService.refreshToken()` sprawdza po `getIdToken(true)`, czy `currentUser.uid` się nie zmienił. Token jest więc zawsze wybity dla konta, które o niego prosiło (druga, niezależna warstwa).
- `_lastRefresh` zapisuje się tylko przy niezmienionym `_refreshGeneration` i tym samym uid. `clearAuthorization()` zeruje `_tokenRefresh` i `_lastRefresh` oraz podbija licznik. Token konta, które się wylogowało, nie jest już ani współdzielony, ani użyty ponownie.
- Linie 143-148 (ponowne sprawdzenie uid i nagłówek domyślny tylko dla `_authorizationUid == uid`) zostały bez zmian. Razem z powyższym token A nie może trafić do żądania ani nagłówka domyślnego B.

**FE-L1: zamknięte.** Trzy nowe testy w `test/api/dio_client_authorization_test.dart`:
- A odświeża, w tym czasie przełączenie na B: osobne odświeżanie dla B, A nie jest ponawiane, `token-A-fresh` nigdy nie wychodzi;
- wylogowanie w trakcie odświeżania: brak ponowienia, a późniejsze żądanie idzie bez Authorization;
- `clearAuthorization` wymusza nowe odświeżanie zamiast użyć zapamiętanego tokena.

Pokrywają dokładnie scenariusz FE-M1. Testów nie uruchamiałem.

**FE-L3: zamknięte.** `Fimber.d` i `RecordingDebugLog` logują przy błędach tokena tylko `runtimeType`, w ścieżkach 403, `init()` i `_applyAuthorization`.

**Nowe ryzyka:** brak. Zmiana `_refreshTokenShared` na `async` nie wprowadza pętli: każde żądanie dalej ma co najwyżej jedno ponowienie, a błąd odświeżania wraca do wołającego jako pierwotne 401. Uwaga informacyjna spoza zakresu: `AnalyticsEvents.logError(e, stackTrace)` w `init()` dalej wysyła wyjątek z `getToken()` do analityki. To wcześniej istniejący kod, nie należy do tej zmiany, a wyjątki Firebase nie zawierają tokena. Można to ujednolicić przy okazji (backlog, flutter-mobile).

**Aktualny stan:**
- Critical 0, High 0, Medium 0.
- Low otwarte: BE-L1 (backend-api) i FE-L2 (flutter-mobile), oba w backlogu.

**Werdykt po weryfikacji: można wdrażać obie gałęzie bez zastrzeżeń.**
