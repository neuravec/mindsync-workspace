# GPT-Live-1: kontrola rozmowy i promptowanie (research 2026-10-14)

Metoda: WebFetch oficjalnych stron developers.openai.com (stan na 2026-10-14), uzupelnione o dokumentacje partnerow (Pydantic AI, LiveKit) i watek community. Strony openai.com/index/... zwracaja 403, wiec tresc posta launchowego znam tylko z relacji wtornych (oznaczone). Pewnosc: wysoka = oficjalna dokumentacja OpenAI; srednia = dokumentacja partnera lub dwa wtorne; niska = jedno zrodlo wtorne lub zgloszenie dewelopera.

Skroty zrodel:
- [GUIDE] https://developers.openai.com/api/docs/guides/live
- [PROMPT] https://developers.openai.com/api/docs/guides/live-prompting
- [DELEG] https://developers.openai.com/api/docs/guides/live-delegation
- [CONV] https://developers.openai.com/api/docs/guides/live-conversations
- [MIGR] https://developers.openai.com/api/docs/guides/live-migration
- [WEBRTC] https://developers.openai.com/api/docs/guides/voice-webrtc?api=live
- [SIDE] https://developers.openai.com/api/docs/guides/voice-server-controls?api=live
- [COST] https://developers.openai.com/api/docs/guides/voice-latency-cost?api=live
- [MODEL] https://developers.openai.com/api/docs/models/gpt-live-1
- [PRICE] https://developers.openai.com/api/docs/pricing
- [COMM] https://community.openai.com/t/introducing-gpt-live-1-in-the-api/1396471
- [PYD] https://pydantic.dev/docs/ai/realtime/openai-live/
- [LK] https://docs.livekit.io/agents/models/realtime/plugins/gpt-live

## Najwazniejszy wniosek architektoniczny

GPT-Live-1 to NIE zamiennik gpt-realtime-2 jeden do jednego. Ma wlasny endpoint (`/v1/live/sessions`, [MODEL]), wlasny protokol zdarzen i model "cienka warstwa glosowa + backend". Wiele kontroli znanych z Realtime (session.update dla instrukcji, response.cancel, reczny turn control, VAD eagerness) w Live nie istnieje albo jest mocno ograniczone. Dla MindSync (sciezka kryzysowa, rygorystyczne prompty Reflect) to istotna regresja kontroli, rekompensowana lepsza naturalnoscia rozmowy.

## 1. Promptowanie

- Instrukcje warstwy glosowej: `session.instructions`, krotki prompt o stylu rozmowy i zasadach delegacji. Szczegolowe instrukcje, reguly biznesowe i procedury narzedzi maja isc do backendu. [GUIDE] pewnosc: wysoka.
- Prompt backendu: `session.delegation.responses.instructions` (delegacja Responses) albo konfiguracja wlasnego agenta (delegacja klienta). [MIGR] wysoka.
- Limit: instrukcje do 16,384 tokenow; startowa historia (`input`) do 128 wiadomosci i 8,192 tokenow, kazda wiadomosc ma jedna czesc tekstowa, role developer/user/assistant. [CONV] wysoka.
- Okno kontekstu 128,000 tokenow (instrukcje, tekst, tokeny audio). Powyzej 90% startuje w tle silnik zastepczy z oryginalnymi instrukcjami, do 8,192 tokenami ostatniej historii i streszczeniem. Starsze szczegoly moga nie zostac dosłownie. [CONV] wysoka. Strona modelu nie podaje okna kontekstu [MODEL].
- Zmiana instrukcji w trakcie sesji: `session.update` dziala WYLACZNIE dla ustawien `session.delegation.responses` i tylko w sesji juz uzywajacej delegacji Responses; inne pola sa odrzucane. [CONV] wysoka. Zamiast tego: `session.instructions.append` (zaufane instrukcje dodatkowe, "can interrupt speech in progress" [SIDE]), `session.thinking.append` (ciche tlo), `session.commentary.append` (tekst do powiedzenia, model parafrazuje). Kazdy append do 500 tokenow, wymaga `delegation_id` (null = cala sesja). [DELEG], [CONV] wysoka. Instrukcji z `instructions` nie da sie wymienic ani usunac, tylko dopisac. Glos i obie warstwy instrukcji sa niezmienne po starcie. [LK] srednia.
- Prompt templates / prompt id: nie znalazlem wzmianki w dokumentacji Live. Prompt caching: dotyczy "eligible backend models", trzymaj stabilne instrukcje i narzedzia na poczatku promptu backendu. [COST] wysoka. Cennik nie podaje ceny cached dla warstwy glosowej (rozliczana sekundami).
- Struktura zalecana: szablon z trzema naglowkami "Backchannel policy", "Interruption policy", "Delegation policy". Pisz prompt w jezyku, w ktorym ma byc mowa; wymowe podawaj IPA. [PROMPT] wysoka. Limity dokladnych liczb strona promptowania odsyla do konfiguracji sesji.
- Kontekst uzytkownika (pamiec, historia): (a) `input` przy starcie (max 128 wiadomosci / 8,192 tokenow, tylko tekst; developer message moze ustawic jezyk i powitanie, na WebSocket w `session.start`), (b) append w trakcie, (c) pelny kontekst w backendzie (delegacja klienta: aplikacja sama buduje kontekst z `session.input_transcript.delta` i `session.output_transcript.delta`). [PROMPT], [DELEG], [CONV] wysoka. Obrazy: warstwa glosowa ich nie przyjmuje, tylko backend. [PYD] srednia, [MIGR] wysoka.

## 2. Delegacja

- Dwa tryby wybierane przy tworzeniu sesji; zmiana wymaga nowej sesji: Responses delegation (zarzadzana, OpenAI uruchamia backend) i client delegation (wlasny model/agent/usluga). Pominiecie `delegation.type` lub null = tryb klienta. [DELEG], [CONV] wysoka.
- Model backendu: przy delegacji Responses wymagany `model`. Strona sugeruje start od `gpt-6-luna`, dla trudniejszych zadan `gpt-6-sol`. [DELEG] wysoka. (Plugin LiveKit podaje domyslnie `gpt-5.6-luna` [LK], niespojnosc nazw, niska pewnosc co do nazwy domyslnej.) Zla nazwa wychodzi dopiero przy pierwszej delegacji: sesja konczy sie bledem `live_backend_model_unavailable` [PYD] srednia.
- Reasoning effort: `delegation.responses.reasoning.effort` (wartosci zalezne od modelu), `service_tier` auto/default/flex/priority, `max_output_tokens` (min 16 wg [LK]), `verbosity`. [DELEG], [PYD] wysoka/srednia. Zmiana w trakcie przez `session.update` (tylko pola Responses). `delegation` nie da sie ustawic na null w dzialajacej sesji (`immutable_field_update`). [DELEG] wysoka.
- Wymuszanie/zakaz: `tool_choice` (auto/required/none/nazwana funkcja) i `parallel_tool_calls` dzialaja TYLKO po tym, jak warstwa glosowa zdelegowala. O tym, KIEDY deleguje, decyduje prompt warstwy glosowej ("Delegation policy"). Brak twardego przelacznika "zawsze deleguj". [DELEG], [PROMPT] wysoka. Zgloszenie: model czasem odpowiada bez delegacji, wiec przeplyw zalezny od narzedzi (np. `end_conversation`) moze nie ruszyc. [COMM] niska (zgloszenie dewelopera).
- Latencja: OpenAI utrzymuje trwale polaczenia do Responses i przygotowuje konfiguracje z wyprzedzeniem; brak liczb latencji delegacji w dokumentacji. [DELEG] wysoka. Benchmark z posta launchowego: turn-taking 0.798 s vs 1.41 s dla gpt-realtime-2.1 [COMM] srednia (relacja wtorna, nie widzialem posta zrodlowego).
- Co mowi model w czasie czekania: mowa i praca backendu sa niezalezne, model moze mowic dalej. Dokumentacja nie opisuje domyslnych "fillerow". Postep wstrzykujesz przez `session.commentary.append` (np. "I'm checking the available appointments") lub cicho przez `thinking.append`. [DELEG] wysoka. Raportuj sukces dopiero po potwierdzeniu backendu.
- Przerwanie: praca backendu NIE jest anulowana przez przerwanie mowy; aplikacja decyduje, czy dokonczyc. [GUIDE] wysoka. [PYD] dodaje: brak cancelacji, akcje zmieniajace stan trzeba chronic zatwierdzeniem (srednia).
- Zgloszenia: dwa `response.completed` na ture delegacji (wewnetrzny i zewnetrzny), `response.done.output` zawsze puste, model potrafi zaczac mowic przed `session.delegation.created`. [COMM] niska.

## 3. Kontrola tury

- Turn detection: model sam decyduje o turach (full duplex, nie ma klasycznego VAD/eagerness). Dokumentacja Live NIE zawiera opcji `turn_detection` ani eagerness; migracja mowi wprost, ze "GPT-Live decides when to speak" i usuwa reczne commit audio / wyzwalanie tury. [MIGR] wysoka; [PYD] (turn_detection rzuca blad) i [LK] ("model controls turn detection") srednia. Relacja o poscie launchowym: "natywnie wspiera turn detection, mozna budowac wokol jawnych granic tur" (explicit turn detection): https://www.unite.ai/de/openais-gpt-live-1-arrives-in-the-api-at-0-05-per-minute/ niska; nie znalazlem w oficjalnej dokumentacji parametru to realizujacego. LUKA.
- Backchannele: tylko przez prompt ("moderate"), brak liczbowego pokretla. Regula zakazujaca calkowicie nakladania sie mowy potrafi je stlumic. Mozna wiec ograniczyc przez instrukcje, ale nie twardo wylaczyc. [PROMPT] wysoka.
- Przerwanie przez uzytkownika: model sam przerywa wlasna wypowiedz i slucha. Zgloszenie: klient nie wie o barge-in, odpowiedz bywa zapisana jako kompletna; brak truncation. [PYD], [LK] srednia. Przerwanie przez aplikacje: `session.instructions.append` moze przerwac mowe w toku; mute/drop audio po stronie klienta; `session.input_audio.mute` blokuje tylko wejscie. [SIDE] wysoka.
- Cisza i szum: reguly w prompcie (cisza, halas tla); OpenAI deklaruje poprawione radzenie sobie z cisza i szumem [COMM] srednia. Cisza liczy sie do rozliczenia (patrz 7).
- Wymuszenie odpowiedzi: `response.create` w Live "kontynuuje zdelegowana prace backendu", nie jest "mow teraz". Brak odpowiednika wymuszenia generacji. [MIGR] wysoka. Przez LiveKit `generate_reply()` moze zostac odrzucone, jesli model nie zacznie mowic w 10 s. [LK] srednia.
- Anulowanie odpowiedzi: brak `response.cancel` na data channel wg zgloszenia [COMM] niska; w dokumentacji nie ma zdarzenia cancel dla warstwy glosowej, tylko `session.close` (anuluje kolejkowane Responses). [CONV] wysoka.
- Wstrzykiwanie: tekst przez `conversation.item.create` (wg [WEBRTC] jako wejscie tekstowe na data channel) oraz appendy; tekst to kontekst, nie tura uzytkownika, limit 500 tokenow; `respond=false` nie gwarantuje milczenia. [PYD] srednia. Tekst wymaga plynacego audio wejsciowego. [PYD] srednia.
- Zakonczenie: `session.close`, czekac na `session.closed` (z koncowym `usage.seconds`) przed zamknieciem peer connection; powody: close_requested, expired, content, remote_hangup, connection_lost. [CONV], [WEBRTC] wysoka. Zgloszenie: pozegnania czesto nie dochodza do backendu, wiec "hangup przez narzedzie" jest zawodny. [COMM] niska.

## 4. Bezpieczenstwo i moderacja

- Wbudowana moderacja: dokumentacja mowi tylko, ze czesc zdarzen moderacyjnych konczy sesje (`reason: content`), inne ucinaja audio asystenta do konca biezacej wypowiedzi i emituja `error` bez konczenia sesji. Brak konfigurowalnej moderacji ani kategorii. [CONV] wysoka.
- Twardy guardrail w warstwie glosowej: NIE. OpenAI opisuje guardrails jako kontrole aplikacji: akumuluj `session.input_transcript.delta` i `session.output_transcript.delta`, uruchom szybki model klasyfikujacy rownolegle, zablokuj akcje, wyslij korekte. Korekta "nie cofnie dzwieku, ktory uzytkownik juz uslyszal". Opcjonalnie buforuj audio asystenta i wydawaj po akceptacji (doda latencje; brak output VAD). [SIDE], [MIGR] wysoka.
- Przechwycenie transkrypcji na zywo i przerwanie modelu: tak, przez sideband WebSocket (`wss://api.openai.com/v1/live/sessions/{id}/attach`, klucz API na serwerze) odczytujesz transkrypty i wysylasz `session.instructions.append` (przerywa mowe) albo `session.close`; klient moze tez zdusic odtwarzanie. [SIDE] wysoka.
- Implikacja dla MindSync (rekomendacja, nie fakt): sciezka kryzysowa wymaga detektora w backendzie na sidebandzie, a nie tylko promptu; przy Live nie ma gwarancji, ze model nie powie czegos niepozadanego zanim detektor zadziala.
- Dodatkowo: znak wodny SynthID dla audio z GPT-Live (aktualizacja 2026-07-31) wg relacji wtornej, niska pewnosc.

## 5. Glosy, jezyki, tempo, emocje

- 12 glosow: quartz, ripple, vesper, willow, stone, gleam, meridian (angielski, akcenty AU/UK/IE/NA), bossa, tempo (portugalski brazylijski), beacon (angielski, filipinski), delta, cinder (angielski, poludnie USA). Domyslny `marin` wg [CONV]/[LK]. Zrodlo: [CONV] wysoka. Uwaga: w opisie glosow w community pojawiaja sie Marin i Cedar jako glosy bez obcego akcentu we francuskim [COMM] niska, ale nie ma ich w tabeli [CONV].
- Polski i niemiecki: brak glosow PL/DE w tabeli, brak oficjalnej listy jezykow na stronach modelu, guide i conversations ([MODEL] "Languages: not stated"). Relacja o poscie launchowym: jezyki i akcenty maja sie rozszerzac "w nadchodzacych miesiacach", brak listy na start (unite.ai, niska). Wniosek: PL i DE NIE sa potwierdzone jako wspierane jakosciowo. Trzeba przetestowac empirycznie; to blokujaca niewiadoma dla MindSync. Zgloszenia: akcent angielski/kanadyjski we francuskim, glosy brzmia inaczej miedzy rozmowami [COMM] niska.
- Tempo, styl, emocja: tylko przez prompt ("unhurried pace", dlugosc odpowiedzi regulami, ton "calm, friendly, warm", reakcja na frustracje). Brak parametru speed ani sterowania emocja. [PROMPT] wysoka.
- Custom voices: tylko organizacje z zatwierdzonym glosem (kontakt z sales). [CONV] wysoka.

## 6. Transkrypcja, nagranie, limity

- Transkrypcja: natywne transkrypty wejscia i wyjscia przez `session.input_transcript.delta` i `session.output_transcript.delta`; nie ma konfigurowalnego `input_transcription_model` (Pydantic rzuca blad). [MIGR] wysoka, [PYD] srednia. Transkrypty przychodza po audio. [LK] srednia. Zgloszenie: na poczatku API zwracalo tylko wiadomosci agenta, workaround to delty transkryptu. [COMM] niska.
- Keyword biasing: deklarowane w poscie launchowym (relacja wtorna, niska); nie znalazlem parametru w oficjalnej dokumentacji sesji. LUKA.
- `store`: domyslnie false, ustawiane przy starcie; nagrania stereo WAV (wejscie lewy, wyjscie prawy) przez `GET /v1/live/sessions/{session_id}/content`, przechowywane 30 dni, ZDR traktuje jako false. [CONV] wysoka.
- Limit czasu sesji: istnieje (`reason: expired`), ale wartosci nie znalazlem w dokumentacji OpenAI. LUKA. Kompaktowanie kontekstu pozwala na dlugie sesje. [CONV] wysoka.
- Rate limits = rownolegle sesje: Build 50, Launch 300, Grow 500; tier Free nieobslugiwany. [MODEL] wysoka.
- Funkcje: streaming i function calling tak; structured outputs, fine-tuning, predicted outputs nie; wejscie audio+tekst, wyjscie audio+tekst; knowledge cutoff 2025-07-31. [MODEL] wysoka. Uwaga: Pydantic podaje, ze Live zawsze mowi (brak wyjscia tylko tekstowego) [PYD] srednia.

## 7. Cennik (z oficjalnych stron, [PRICE], [MODEL], [COST])

GPT-Live-1:
- $0.05 za minute sesji glosowej, rozliczane co sekunde, bez zaokraglania do pelnej minuty.
- Cisza sie liczy: czas aktywnej sesji obejmuje okresy, gdy obie strony milcza lub pracuje backend; mute nie zatrzymuje naliczania.
- Utworzenie sesji WebRTC nalicza 15 s na starcie, kredytowane pozniej na poczet czasu sesji.
- Backend (model + narzedzia) rozliczany osobno wg normalnych stawek tokenowych (wejscie, wyjscie, cached, narzedzia).
- Wzor z [COST]: (sekundy glosowe / 60 x stawka za minute) + koszty backendu. Przyklad z dokumentacji: 90 s = $0.075.
- Zamkniecie sesji podczas dlugiego zadania backendu oszczedza $0.05/min.

Realtime (za 1M tokenow, [PRICE]):

| Model | Modalnosc | Wejscie | Cached | Wyjscie |
|---|---|---|---|---|
| gpt-realtime-2 | audio | $32.00 | $0.40 | $64.00 |
| gpt-realtime-2 | tekst | $4.00 | $0.40 | $24.00 |
| gpt-realtime-2 | obraz | $5.00 | $0.50 | brak |
| gpt-realtime-2.1 | audio | $32.00 | $0.40 | $64.00 |
| gpt-realtime-2.1 | tekst | $4.00 | $0.40 | $24.00 |
| gpt-realtime-2.1 | obraz | $5.00 | $0.50 | brak |
| gpt-realtime-2.1-mini | audio | $10.00 | $0.30 | $20.00 |
| gpt-realtime-2.1-mini | tekst | $0.60 | $0.06 | $2.40 |
| gpt-realtime-2.1-mini | obraz | $0.80 | $0.08 | brak |

Przeliczenie tokenow Realtime: audio uzytkownika ok. 1 token / 100 ms, asystenta ok. 1 token / 50 ms; cala rozmowa jest wysylana przy kazdej odpowiedzi, wiec koszt rosnie wraz z dlugoscia [COST] wysoka. Porownanie $/min Realtime vs Live wymaga zalozen o cache i dlugosci rozmowy; NIE bylo w zrodlach i nie liczylem tego jako faktu. Pamietaj, ze Live to $0.05/min PLUS backend, a Reflect na 2.1-mini ma wyjscie audio $20/1M.

## 8. Roznice protokolu i WebRTC

- Nowe nazwy: `input_audio_buffer.append` -> `session.input_audio.append`; `response.output_audio.delta` -> `session.output_audio.delta`; transkrypty -> `session.output_transcript.delta` / `session.input_transcript.delta`; wynik funkcji `conversation.item.create` -> `response.item.create` (+ `response.create`); `session.tools` -> `delegation.responses.tools`. [MIGR] wysoka.
- Znikaja: reczna kontrola tur (commit/clear/trigger), `response.output_audio.done`, `response.done` (koniec wypowiedzi sledzisz po stronie klienta), bezposrednie audio do backendu. [MIGR] wysoka.
- Nowe: `session.started`, `session.delegation.created`, `response.event` (koperta na zagniezdzone zdarzenia Responses), `session.instructions/thinking/commentary.append` z `client_event_id`, `session.input_audio.mute/unmute`, `session.usage.updated`, `session.close/closed`. [MIGR], [CONV], [DELEG] wysoka.
- WebRTC: wspierany i rekomendowany dla "browser, mobile, and server"; kanal danych `oai-events`; serwer wysyla `session` + `transport: {type:"webrtc", sdp}` na `POST /v1/live/sessions` kluczem projektu, odpowiedz 201 z `session.id` i SDP. NIE wysylac `session.start` na data channel, pomijac `audio.format`. Brak dedykowanej sekcji mobilnej (odsylacz do przewodnika WARP). [WEBRTC] wysoka.
- Ephemeral tokens: guide Live NIE opisuje client secrets dla Live; mechanizm client secrets opisany jest dla legacy Realtime (`/v1/realtime/calls`). Pydantic: "Client secrets: unavailable for GPT-Live", przegladarka uzywa przeplywu sideband. [WEBRTC] wysoka (brak opisu), [PYD] srednia. Implikacja: klient Flutter nie moze sam wymieniac SDP z OpenAI kluczem tymczasowym, SDP musi isc przez backend MindSync. (Wniosek, do potwierdzenia testem.)
- Limit wiadomosci data channel 262144 B (zgloszenie, [COMM] niska). Przykladowe limity z [WEBRTC] sa przykladowe, nie dokumentacyjne.

## 9. Znane problemy (zgloszenia, [COMM], niska pewnosc, jeden watek)

- Brak `session.update`/`response.cancel`/`input_audio_buffer.clear` na data channel w porownaniu z Realtime.
- Model czasem odpowiada bez delegacji; goodbye rzadko dociera do backendu (SIP hangup).
- Zdwojone `response.completed`; pusty `response.done.output`; mowa przed `session.delegation.created`.
- Slabsze rozumowanie niz wczesniej przy wybieranym reasoning effort (odpowiedz: ma byc sparowany z konfigurowalnym modelem); zawieszenia podczas lookupow i dlugich sesji.
- Brak istotnej poprawy przerywania wzgledem Realtime-2 wg jednego dewelopera; za to chwalone naturalne turn-taking i filtrowanie szumu.
- Glosy bez charakteru glosow Realtime, wahania miedzy rozmowami, akcent polnocnoamerykanski.
- Warstwa glosowa nie przyjmuje obrazow ani nie uruchamia narzedzi sama; sztywne skrypty/przeplywy trudniejsze niz w Realtime.
- Dostep: LiveKit pisze o "GPT-Live alpha access" (srednia), a oficjalny cennik pokazuje GA od 2026-09-10; tier Free nieobslugiwany.

## Czego NIE znalazlem

- Listy wspieranych jezykow (PL, DE, EN) oraz glosow PL/DE: brak w [MODEL], [CONV], [PROMPT], [GUIDE].
- Parametru "explicit turn detection" i keyword biasing w oficjalnym API reference (jest tylko w relacjach o poscie launchowym).
- Wartosci limitu czasu pojedynczej sesji.
- Liczb latencji delegacji i okna kontekstu na stronie modelu (okno 128k jest w [CONV]).
- Prompt templates / prompt id dla Live.
- Pelnego API reference zdarzen Live (nie weszlem na reference; guide linkuje tylko do [MODEL]).
- Posta launchowego openai.com/index/introducing-gpt-live-1-in-the-api/ (403), dlatego benchmarki sa z relacji wtornych.
- Potwierdzenia, czy client secrets dzialaja dla /v1/live/sessions (wniosek z braku opisu + Pydantic).

## Rekomendacja (osobne zdanie, nie fakt)

Dopoki nie ma potwierdzonego PL/DE i parametru turn detection, zostac na gpt-realtime-2.1 / 2.1-mini dla Reflect i sesji, a GPT-Live-1 przetestowac w EN jako eksperyment z sidebandem do detekcji kryzysu.
