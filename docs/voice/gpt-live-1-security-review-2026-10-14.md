# Security Audit Report: GPT-Live-1 backend (feat/gpt-live-1, fbec276), 2026-10-14

Zakres: worktree `MindSync-live`, commit `fbec276`, diff względem `origin/main`. Przeczytane: `app/api/v1/endpoints/audio_v2.py`, `app/services/live_session.py`, `app/services/live_voice.py`, `app/services/openai_live_service.py`, diff `reflect.py`, `conversations.py`, `first_conversation.py`, `reflect_prompt.py`, `voice_director.py`, `usage_tracking.py`, `schemas/voice_director.py`, `config.py`, lista testów `app/tests/test_gpt_live_voice.py`, kontekst `docs/voice/gpt-live-1-impact-analysis-2026-10-14.md`. Audyt statyczny, bez uruchamiania kodu i bez prób na żywym API.

## Executive Summary

Rdzeń jest zrobiony dobrze: oba endpointy wymagają tokenu Firebase, własność wątku jest sprawdzana zapytaniem po `user_id`, prompt powstaje wyłącznie na serwerze (klient nie przesyła instrukcji, `voice` przechodzi przez allowlistę, `language` jest ignorowany), klucz OpenAI, SDP i transkrypty nie trafiają do logów ani do odpowiedzi, PostHog dostaje tylko enumy i liczniki, a SAFETY AND ESCALATION w Reflect i pierwszej rozmowie siedzi w nieprzycinanej części promptu. Jest jedno znalezisko High: brak jakiegokolwiek limitu na `POST /audio-v2/live-session`, przy czym każdy create jest płatny (min. 15 s) i dostępny dla każdego darmowego konta przez `session_kind=journal`. To blokuje włączenie Live. Do tego sześć Medium (zaufanie do `session_kind`, zaufanie do `/end`, pamięć w `injection_text` przy kryzysie, flaga kryzysu w logach, możliwe ucięcie SAFETY w journalu, timeout per-faza w jedynym workerze).

**Werdykt: wdrożenie z `VOICE_LIVE_ENABLED=true` ZABLOKOWANE do czasu naprawy H-1.** Kod może wejść na prod uśpiony, ale wtedy domyślna wartość w `config.py` musi zmienić się na `False` (dziś `True`, `app/core/config.py:84`), a Config Var na Heroku trzeba ustawić jawnie przed deployem. Medium do naprawy w tym samym sprincie, najlepiej w tym samym PR (wszystkie są małe).

## Critical Findings

Brak.

## High Findings

### HIGH-001: Brak limitu i kosztowa amplifikacja na `POST /audio-v2/live-session`

- **Severity**: High (świadomie powyżej domyślnego "Medium" dla braku rate limitu, uzasadnienie niżej)
- **Location**: `app/api/v1/endpoints/audio_v2.py:358-394`, `app/services/live_session.py:109-185`, `app/services/openai_live_service.py:76-132`
- **Description**: Endpoint nie ma rate limitu, limitu równoległych sesji ani dziennego budżetu na użytkownika. Każde wywołanie od razu robi `POST /v1/live/sessions` kluczem projektu, a według analizy wpływu każdy create jest rozliczany minimum 15 s. Bramka Premium dotyczy tylko `reflect`; `journal` nie ma żadnej bramki Premium (realtime journal też jej nie ma), więc każde darmowe konto Firebase (rejestracja nic nie kosztuje) może wołać endpoint w pętli na własnym wątku journala. `max_session_seconds` jest `None`, więc pojedyncza sesja może też trwać bez górnej granicy po naszej stronie.
- **Dlaczego High, a nie Medium**: ścieżka realtime ma podobną powierzchnię (mint `client_secret` bez limitu), ale mint nie jest płatny sam w sobie. Live dodaje koszt naliczany per request, bez udziału klienta WebRTC. Przy około 40 req/s (realne z jednego skryptu) to około 0,50 USD/s, czyli rząd 1800 USD na godzinę na jednym koncie, a kont można założyć wiele. Kill switch istnieje, ale jest reaktywny i wymaga, żeby ktoś zauważył rachunek.
- **Impact**: nieograniczony wydatek na koncie OpenAI, możliwe wyczerpanie limitów organizacji OpenAI (co uderzy też w realtime, Whisper, GPT dla wszystkich użytkowników), plus obciążenie jedynego workera web (patrz MED-006).
- **Reproduction Steps (do weryfikacji, bez exploita)**: w teście jednostkowym z zamockowanym `create_live_session` wywołać endpoint N razy z rzędu dla jednego użytkownika i sprawdzić, że każde wywołanie trafia do mocka. Dziś trafia N razy.
- **Remediation**:
  1. Limit per użytkownik w Redis przed jakimkolwiek odczytem kontekstu i przed wywołaniem OpenAI, np. maks. 6 create na 10 min i 30 na dobę (wartości w `config.py`, np. `LIVE_CREATE_MAX_PER_10MIN`, `LIVE_CREATE_MAX_PER_DAY`). Przekroczenie: zwykły fallback 200 `{"engine": "realtime", "fallback_reason": "rate_limited"}` (zgodny z kontraktem, klient nie wymaga zmian) i zdarzenie `voice_live_fallback`. Wzorzec licznika: `INCR` + `EXPIRE` na kluczu `live:rl:{user_id}:{okno}`. Przy niedostępnym Redis: fail closed do realtime, nie fail open.
  2. Limit jednej aktywnej sesji Live na użytkownika: klucz `live:active:{user_id}` ustawiany przy create (TTL np. 2 h), zdejmowany w `/end`; kolejny create przy aktywnym kluczu to fallback `concurrent_session`.
  3. Globalny bezpiecznik na proces: `threading.BoundedSemaphore` (np. 8) wokół wywołania OpenAI; brak wolnego slotu to fallback `busy` bez czekania.
  4. Rozważyć górną granicę długości sesji (`max_session_seconds` w odpowiedzi i rozłączenie po stronie klienta), uzgodnioną z flutter-mobile przez integration-devops.
  5. Testy: limit okna, limit dzienny, aktywna sesja, Redis down = fallback, brak wywołania OpenAI po przekroczeniu.
- **Owner**: backend-api (kontrakt `max_session_seconds`: integration-devops, potem flutter-mobile)

## Medium Findings

### MED-001: `session_kind` od klienta pozwala ominąć bramkę Premium na wątku Reflect

- **Location**: `app/services/live_session.py:97-106` (`_build_context`), `app/api/v1/endpoints/conversations.py:692-709` (`build_journal_live_session`)
- **Description**: Gałąź journala sprawdza tylko `id` i `user_id`, bez `conversation_type`. Darmowy użytkownik może wysłać `session_kind="journal"` z `conversation_id` własnego wątku REFLECT i dostać sesję Live (prompt journala, ale historia wątku Reflect w `session.input`), z pominięciem 403 "Voice mode requires Premium". Kolejne tury może zapisywać przez journalowy `user_message_add`, który też nie sprawdza typu. Odwrotny kierunek jest bezpieczny (`reflect` na wątku JOURNAL daje 404). To odpowiednik istniejącej luki realtime (`GET /conversations/realtime/{id}/session_data` też nie sprawdza typu), więc nie jest regresją, ale docstring nowego endpointu obiecuje bramkę, której nie ma. Danych innych osób to nie ujawnia.
- **Remediation**: rodzaj sesji wyprowadzać z serwera, nie od klienta. W `start_live_session` odczytać `conversation_type` wątku (z filtrem `user_id`) i: REFLECT zawsze przez `build_live_voice_session`, JOURNAL zawsze przez `build_journal_live_session`; w `build_journal_live_session` dodać filtr `models.Conversation.conversation_type == models.ConversationTypeEnum.JOURNAL`. `session_kind` klienta zostaje tylko jako wskazówka do analityki. Test: darmowe konto, wątek REFLECT, `session_kind=journal` daje 403. Osobno (poza tym PR) ta sama poprawka dla realtime `session_data` i journalowego `user_message_add`.
- **Owner**: backend-api

### MED-002: `/live-session/{id}/end` zapisuje koszty dla nieznanych sesji i ufa `billed_seconds`

- **Location**: `app/services/live_session.py:189-241` (szczególnie 210-221), `app/services/usage_tracking.py` (`log_live_session_usage`)
- **Description**: Gdy Redis nie zna `session_id`, endpoint i tak zapisuje wiersz `token_usage_log` dla wołającego. Każdy zalogowany użytkownik może więc wysyłać dowolne poprawne składniowo identyfikatory i tworzyć dowolnie wiele wierszy, każdy do 4 h (około 12 USD fikcyjnego kosztu), bez limitu. Własną prawdziwą sesję może zamknąć z `billed_seconds=0`. Rachunek OpenAI się nie zmienia, ale nasz jedyny rejestr kosztu Live (nie ma sideband ani rozliczenia z OpenAI) staje się niewiarygodny, a tabela rośnie bez kontroli. Dodatkowo różnica odpowiedzi (404 dla cudzej, 200 dla nieznanej) to wyrocznia istnienia, praktycznie nieużyteczna przy entropii identyfikatorów OpenAI (Low).
- **Remediation**: w `_remember_session` zapisać też `created_at` (epoch). W `end_live_session`: brak rekordu w Redis to 404 (lub zapis z `is_estimate=True` i zerowym kosztem, bez przyjmowania liczby od klienta); `billed_seconds` przyciąć do `now - created_at + 30 s` zapasu; po zapisie usunąć klucz (lub oznaczyć jako zamknięty). Objąć `/end` tym samym limitem per użytkownik co create. Gdy klient nie poda sekund, zapisać szacunek z `now - created_at`. Testy: nieznane id, sekundy powyżej zegara, ponowne `/end`.
- **Owner**: backend-api

### MED-003: Przy turze kryzysowej `injection_text` nadal niesie pamięć (excerpty z przeszłych wpisów)

- **Location**: `app/api/v1/endpoints/reflect.py:2594-2626`
- **Description**: Przy `suppresses_memory(data.text)` kod zeruje tylko `injection_chunks`. `director_payload` zostaje z `should_inject=True` i `injection_text` zawierającym excerpty z `_voice_past_entries_text` (blok jest liczony i "claimowany" także w turze kryzysowej). Klient realtime wstrzyknie je jak dotąd (to otwarte znalezisko H-1 z przeglądu 2026-10-07), a klient Live zachowa się poprawnie tylko wtedy, gdy nigdy nie sięga po `injection_text` jako fallback przy `injection_chunks == null`. To zależność od kontraktu klienta przy najwrażliwszym momencie rozmowy, sprzeczna z `SAFETY_REMINDER` ("Bring nothing from their history into this").
- **Remediation**: przy `suppresses_memory(data.text)` ustawić `director_payload = None` (albo `should_inject=False`, `injection_text=None`, `injection_chunks=None`) dla obu silników i nie wywoływać `_voice_past_entries_text` w ogóle, żeby nie claimować excerptów. To zamyka też H-1 dla realtime; jeśli operator chce H-1 załatwić osobno, minimum to zerowanie `injection_text` dla `voice_engine == "live"`. Test: tura kryzysowa daje `director` null lub bez tekstu, a `safety_reminder` ustawiony. Weryfikacja po stronie flutter-mobile: klient Live nie używa `injection_text`.
- **Owner**: backend-api (weryfikacja klienta: flutter-mobile przez integration-devops)

### MED-004: Flaga kryzysu powiązana z identyfikatorem wątku w logach

- **Location**: `app/api/v1/endpoints/reflect.py:2627-2633`
- **Description**: `logger.info("[Live] Voice turn on thread %d: chunks=%d safety_reminder=%s", ...)` zapisuje w logach Heroku, że w wątku o danym id osoba właśnie powiedziała coś, co uruchomiło skan kryzysowy. Id wątku łączy się z użytkownikiem jednym zapytaniem. To wskaźnik ryzyka samobójczego (dane art. 9 RODO) w systemie logów, który nie ma polityki retencji ani kontroli dostępu na poziomie bazy. Istniejący log Directora mówi o kryzysie bez identyfikatora.
- **Remediation**: usunąć `safety_reminder` z tego logu (zostawić `chunks`), albo usunąć id wątku. Jeśli potrzebna jest metryka częstotliwości przypomnień, liczyć ją zagregowaną licznikiem bez identyfikatora, nie w PostHog per osoba.
- **Owner**: backend-api

### MED-005: W sesji journala SAFETY jest w części, którą `fit_instructions` może uciąć

- **Location**: `app/api/v1/endpoints/conversations.py:717-730`, `app/services/live_voice.py:141-145`
- **Description**: W Reflect i pierwszej rozmowie SAFETY jest w `head`, więc awaryjne cięcie od końca go nie dotyka. W journalu SAFETY jest w `tail` (`guardrail + SAFETY + LIVE CONVERSATION`), a `head` to `SYSTEM_MESSAGE` z `.env` plus `LAST_SUMMARY`, `PROFILE`, `THERAPY_CONTEXT`, czyli tekst o rozmiarze nieograniczonym w kodzie. Gdy `head + tail` przekroczy budżet, `_cut_to_tokens(head + tail)` utnie koniec, czyli właśnie SAFETY. Dziś mało prawdopodobne (budżet to około 46 KB), ale skutek to sesja głosowa bez zasad kryzysowych. Test `test_fit_never_cuts_safety` sprawdza tylko wariant z SAFETY w `head`.
- **Remediation**: w journalu wstawić `reflect_safety_section()` na początek `head` (przed `SYSTEM_MESSAGE`), a w `fit_instructions` przy `room <= 0` nie ciąć, tylko zgłosić błąd, który `start_live_session` zamieni na fallback `instructions_too_long`. Dodać test journala z bardzo długim `SYSTEM_MESSAGE`/profilem, sprawdzający obecność `SAFETY_SECTION` albo fallback.
- **Owner**: backend-api

### MED-006: Timeout 8 s jest per faza, a handler blokuje wątek jedynego workera web

- **Location**: `app/services/openai_live_service.py:98`, `app/api/v1/endpoints/audio_v2.py:359` (handler `def`), `Procfile` (`uvicorn --workers 1`)
- **Description**: `httpx.Timeout(8)` ustawia osobno connect, write, read i pool na 8 s, a read timeout liczy się między porcjami danych, więc jedno wywołanie może trwać wyraźnie dłużej niż 8 s. Handler synchroniczny zajmuje wątek z puli anyio (domyślnie 40) jedynego procesu web. Kilkadziesiąt równoległych create przy spowolnieniu OpenAI zajmuje całą pulę i zatrzymuje wszystkie synchroniczne endpointy aplikacji (praktycznie całe API). Rozmiar SDP jest ograniczony (20 KB, walidacja Pydantic), to jest w porządku.
- **Remediation**: `httpx.Timeout(timeout, connect=3.0, pool=2.0)` plus twardy deadline całości (np. sprawdzenie `time.monotonic()` i przerwanie przez `httpx` z `timeout` na `read` liczonym od pozostałego czasu), oraz semafor z HIGH-001 pkt 3, żeby Live nigdy nie zajął więcej niż kilka wątków. Test: mock transportu, który odpowiada wolno, kończy się fallbackiem `timeout` w czasie <= deadline.
- **Owner**: backend-api

## Low Findings

- **LOW-001** `openai_live_service.build_session_body`: `store` nie jest ustawiony jawnie, polegamy na domyślnym `false`. Ustawić `"store": False` w `session`, jeśli API Live to pole przyjmuje (sprawdzić w dokumentacji offline, bez eksperymentu na żywym API). Owner: backend-api.
- **LOW-002** Tryb delegacji `client`: model może wysłać do klienta prośbę o delegację mimo polityki "never delegate". Klient Flutter musi takie zdarzenia ignorować i nigdy nie wykonywać niczego na ich podstawie. Weryfikacja: flutter-mobile przez integration-devops.
- **LOW-003** Wyrocznia istnienia w `/end` (404 dla cudzej sesji, 200 dla nieznanej). Znika po poprawce MED-002.
- **LOW-004** Prompt journala (`_journal_voice_prompt_parts`) wstawia `LAST_SUMMARY` i `PROFILE` bez sprawdzenia zgody PROFILING. Stan sprzed tego commitu, wspólny dla obu silników, nieweryfikowany w tym audycie. Zalecany osobny przegląd zgód journala. Owner: backend-api.
- **LOW-005** `build_live_voice_session` claimuje excerpty i zapisuje kontekst Directora przed wywołaniem OpenAI; przy fallbacku do realtime te excerpty nie trafią do promptu realtime. To kwestia funkcjonalna, nie bezpieczeństwa, odnotowana dla backend-api.
- **LOW-006** Brak globalnego limitu rozmiaru ciała żądania w aplikacji (stan istniejący); pole `sdp` jest ograniczone, ale całe JSON nie. Do backlogu integration-devops.

## Co zweryfikowano i jest poprawne

- **Auth**: oba nowe endpointy mają `Depends(deps.get_current_user)`; `user_message_add` (Reflect i journal) bez zmian w auth.
- **Własność**: Reflect filtruje `id + user_id + REFLECT`, journal `id + user_id`; cudzy wątek daje 404 (testy `test_someone_elses_thread_is_404`, `test_someone_elses_journal_is_404`). `/end` z cudzym znanym `session_id` daje 404. `user_id` zawsze z tokenu, nigdy z ciała.
- **Bramka Premium dla Reflect**: ta sama funkcja `_reflect_voice_gate` co `session_data`, kolejność 403 przed 404 zachowana, wyjątek pierwszej rozmowy identyczny (z zastrzeżeniem MED-001).
- **Prompt wyłącznie serwerowy**: klient nie przesyła instrukcji; `voice` przechodzi przez allowlistę `LIVE_VOICES` i mapowanie (`live_voice.py:413-421`), więc nie da się nim wstrzyknąć tekstu; `language` jest ignorowany, język bierze się z profilu. Treści w `session.input` i w bloku "about" to dane samej osoby (samowstrzyknięcie bez wpływu na innych), bloki pamięci są ogrodzone tagami.
- **Wycieki**: klucz OpenAI tylko w nagłówku; logi zawierają nazwy typów wyjątków i skrócone kody błędów (`_safe_code`); SDP, instrukcje, historia i transkrypty nie są logowane; odpowiedź zawiera tylko pola kontraktu.
- **PostHog**: `voice_engine_selected`, `voice_live_fallback`, `voice_live_session_ended` niosą enumy, liczniki i sekundy; `close_reason` sprowadzony do enuma; brak tekstu i flag zdrowia (test `test_no_sdp_or_prompt_reaches_analytics`).
- **PROFILING**: Reflect i pierwsza rozmowa używają tych samych loaderów (`reflect_prompt.load_context`, `first_conversation.load_context`) z bramką `profiling_withdrawn`; Live nie dodaje nowego źródła danych z bio ani Orca.
- **SAFETY**: w Reflect i pierwszej rozmowie w `head`, nieprzycinane, przycinany jest tylko blok "about" całymi blokami; przy przekroczeniu w pierwszej rozmowie wypadają pamięć i bio, nie SAFETY. `safety_reminder` używa wielojęzycznego `contains_crisis_language` (EN, PL, DE i dalej) plus słów Directora; tłumienie pamięci w chunkach działa (z zastrzeżeniem MED-003).
- **Boot safety**: `audio_v2.py` importuje `live_session` leniwie; `live_voice` (importowany na górze `reflect.py` i `conversations.py`) zależy tylko od `math`, `re` i `settings`; brak migracji, enumów i nowego kodu w lifespan.
- **RODO**: `token_usage_log.user_id` ma `ondelete="SET NULL"`; klucz Redis `live:session:*` trzyma tylko `user_id`, rodzaj i id wątku, TTL 6 h, bez treści.

## GDPR Compliance Status (zakres tej zmiany)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Right to erasure | OK | Nowe dane: wiersz kosztu (SET NULL przy usunięciu), klucz Redis z TTL 6 h. Treść rozmów nie jest nigdzie nowo przechowywana. |
| Data minimization | Częściowo | PostHog i logi minimalne, poza MED-004 (flaga kryzysu z id wątku w logach). |
| Right to portability | Bez zmian | Nowe dane to tylko koszty i analityka. |
| Consent for processing | OK dla Reflect, do sprawdzenia dla journala | PROFILING respektowany w Reflect i pierwszej rozmowie; journal: LOW-004 (stan istniejący). |
| Data encryption at rest | Bez zmian | Tury zapisywane istniejącą ścieżką (szyfrowanie wiadomości). |
| Retention policy | Częściowo | Logi Heroku z MED-004 nie mają retencji kontrolowanej przez nas. |
| Przekazanie do OpenAI | Jak dotąd | Ten sam zakres treści co realtime; `store` domyślnie false (LOW-001: ustawić jawnie). |

## Horizontal Privilege Escalation Audit

| Endpoint | Scoping | Wynik |
|----------|---------|-------|
| `POST /audio-v2/live-session` (reflect, first_conversation) | `id + user_id + REFLECT` w `_reflect_voice_gate` | OK |
| `POST /audio-v2/live-session` (journal) | `id + user_id` w `build_journal_live_session` | OK dla cudzych danych; brak filtra typu (MED-001) |
| `POST /audio-v2/live-session/{id}/end` | właściciel z Redis porównany z tokenem | OK dla znanych sesji; nieznane przyjmowane (MED-002) |
| `POST /reflect/{id}/audio/user_message_add` | `id + user_id` (bez zmian) | OK |
| `POST /conversations/{id}/audio/user_message_add` | `id + user_id` (bez zmian, bez filtra typu, stan istniejący) | OK dla cudzych danych |

## Remediation Priority List

1. **Przed włączeniem Live (blokuje)**: HIGH-001 (limity per użytkownik, jedna aktywna sesja, semafor). Do tego czasu `VOICE_LIVE_ENABLED` domyślnie `False` w `config.py` i jawnie `false` na Heroku.
2. **W tym samym PR (zalecane, małe)**: MED-003 (zerowanie pamięci przy kryzysie, zamyka też H-1), MED-004 (log), MED-005 (SAFETY na początek journala), MED-006 (timeout), MED-002 (`/end` z `created_at`), MED-001 (rodzaj sesji z typu wątku).
3. **Backlog**: LOW-001 do LOW-006.

Po poprawkach security-guardian zweryfikuje kod ponownie (HIGH-001 i wszystkie MED) przed włączeniem flagi.

## Re-review (commit 316c9b2, 2026-10-14)

Zweryfikowane statycznie na diffie `fbec276..316c9b2` i testami: `test_gpt_live_voice.py` + `test_gpt_live_voice_security.py`, 71 passed lokalnie (SQLite).

| Finding | Status | Dowód |
|---------|--------|-------|
| HIGH-001 | Naprawione | `live_session.py:117-156`: INCR okna 10 min (6) i doby (40) liczone przed zajęciem slotu, slot `SET NX` (jedna aktywna sesja, TTL 4500 s), Redis niedostępny daje `limiter_unavailable` (fail closed, `_redis_call(default=_MISSING)`); `:302-305` semafor procesu 8, nieblokujący, fallback `busy`; slot zwalniany na każdej ścieżce błędu (`:304, 310, 314, 320, 338, 351`) i w `/end` (`:416`, tylko gdy trzyma tę sesję). |
| MED-001 | Naprawione dla Live | `_thread_kind` (`:234-253`) bierze rodzaj z `conversation_type`, klient decyduje tylko o kolejności 403/404 dla cudzego wątku; `conversations.py:716` filtr `JOURNAL`. Ścieżka realtime bez zmian (follow-up). |
| MED-002 | Naprawione | `/end` (`:387-447`): nieznane lub cudze id daje 404 bez zapisu, sekundy przycięte do `now - created_at + 30 s`, brak sekund to szacunek z zegara, ponowne `/end` nic nie zapisuje (`closed`). |
| MED-003 | Naprawione (zamyka H-1 z 10-07) | `reflect.py:2571-2574`: przy kryzysie lub żałobie `director` null dla obu silników, excerptów nie szuka ani nie claimuje. |
| MED-004 | Naprawione | `reflect.py:2631-2635`: debug bez id wątku i bez flagi kryzysu. |
| MED-005 | Naprawione | `conversations.py:733` SAFETY na początku `head`; `live_voice.py:132-148` brak cięcia, `InstructionsTooLong` daje fallback (także pierwsza rozmowa, `first_conversation.py:1208`). |
| MED-006 | Naprawione | `openai_live_service.py:68-122`: limity per faza sumują się do terminu, twardy deadline przy czytaniu body, limit odpowiedzi 256 KB. |
| LOW-001 | Naprawione w kodzie, do potwierdzenia | `store: False` (`:145`). Jeśli API Live odrzuci to pole, każdy create skończy się fallbackiem `http_400`; potwierdzić jednym smoke testem przed włączeniem toggla w aplikacji. |
| LOW-004 | Naprawione dla Live | `conversations.py:518-541, 728-730`: bez podsumowań i profilu przy wycofanym PROFILING; realtime `session_data` bez zmian (follow-up). |
| voice_rejected | OK | `live_session.py:340-344` tylko przemapowuje kod 403 na enum analityczny; bez treści, bez wpływu na bezpieczeństwo (może źle etykietować 403 z innego powodu, tylko analityka). |

Otwarte follow-upy (nie blokują): MED-001 i LOW-004 na ścieżce realtime oraz w journalowym `user_message_add`; LOW-005; LOW-006; brak rate limitu na `/end` (ryzyko po MED-002 niskie, bo zapis wymaga rekordu z udanego create, a ten jest limitowany). Dodatkowa uwaga Low: slot trzyma 75 min, gdy klient nie wywoła `/end` (blokuje Live tylko temu kontu, fallback do realtime).

**Werdykt re-review: brak otwartych Critical i High. Live może wejść na prod z `VOICE_LIVE_ENABLED=True` przy toggle w aplikacji domyślnie wyłączonym.** Warunki: (1) Redis produkcyjny działa, bo bez niego wszystkie create dostają fallback; (2) przed włączeniem toggla dla użytkowników jeden smoke test potwierdza, że `store: false` nie daje 400; (3) flutter-mobile potwierdza przez integration-devops, że klient Live ignoruje zdarzenia delegacji (LOW-002).
