# GPT-Live-1: analiza wpływu na rozmowy głosowe MindSync (2026-10-14)

Autor: integration-devops (recon read-only, bez zmian w kodzie).
Źródła o GPT-Live-1: oficjalne strony developers.openai.com sprawdzone dziś (guides/live, live-migration, live-delegation, live-conversations, voice-webrtc?api=live, voice-server-controls?api=live, live-prompting, models/gpt-live-1) oraz notatka `docs/voice/gpt-live-1-control-research-2026-10-14.md` (głosy, cennik, języki, zgłoszenia deweloperów z poziomami pewności). Fakty z dokumentacji oznaczam [DOC], zgłoszenia deweloperów [ZGŁ], moje wnioski [WNIOSEK].

## 0. Wniosek w trzech zdaniach

GPT-Live-1 nie jest drop-inem za gpt-realtime-2.x: ma inny endpoint (`POST /v1/live/sessions`, tylko kluczem projektu po stronie serwera), inny protokół zdarzeń na data channel i niezmienną konfigurację po starcie, więc wszystko, co dziś robi `AudioChatCubit`, trzeba napisać drugi raz. Ścieżka kryzysowa przetrwa, bo już dziś nie używa narzędzi (stoi na sekcji SAFETY AND ESCALATION w prompcie plus skanie słów kluczowych po fakcie), ale pojawiają się dwa nowe ryzyka: moderacja OpenAI potrafi uciąć audio asystenta w środku wypowiedzi, a model może próbować delegować rozmowę kryzysową do backendu. Rekomenduję prototyp EN-only za flagą backendową, z nowym endpointem i jawną deklaracją zdolności klienta, bez ruszania obecnego przepływu gpt-realtime, dopóki polski i pozostałe języki aplikacji nie zostaną potwierdzone testem.

## 1. Mapa: wszystko, co dotyka Realtime

### 1.1 Backend (MindSync/app)

| # | Miejsce | Co robi dziś |
|---|---|---|
| B1 | `api/v1/endpoints/audio_v2.py:218-287` `POST /audio-v2/realtime-session` | Mintuje ephemeral key. Body od klienta: `voice`, `instructions` (pełny prompt odesłany przez klienta), `language`, `conversation_id`. Dla pierwszej rozmowy override modelu/reasoning/głosu (`:239-252`), retry z domyślnymi przy odrzuceniu (`:262-273`). |
| B2 | `api/v1/endpoints/audio_v2.py:57-107` schematy `RealtimeSessionRequest`, `VoiceSessionConfig`, `RealtimeSessionResponse` | Kontrakt BE-FE: `ephemeral_key`, `model`, `voice`, `session_type`, `expires_in_seconds`, `client_session_config` (transcription_model, transcription_language, turn_detection, output_modalities, max_output_tokens, reasoning, noise_reduction). |
| B3 | `services/openai_audio_service.py:301-437` `create_realtime_session` | Buduje body `POST /v1/realtime/client_secrets` (`:354-375`): model, instructions, audio pcm 24 kHz, `noise_reduction` near_field (`:89`), transkrypcja `REALTIME_TRANSCRIPTION_MODEL`, `semantic_vad` z `AUDIO_V2_VAD_EAGERNESS` (`:346-351`), reasoning tylko gdy `model.startswith("gpt-realtime-2")` (`:99-106`, `:381-393`). Składa `client_session_config` (`:401-410`). |
| B4 | `services/openai_audio_service.py:485-548` `_post_client_secrets_raw` | HTTP do `https://api.openai.com/v1/realtime/client_secrets`, retry 3x, loguje prefiks klucza (15 znaków, `:520`). |
| B5 | `services/openai_audio_service.py:441-481` + `audio_v2.py:290-309` | Sesja transkrypcyjna (`type: transcription`). Nie dotyczy rozmowy, ale używa tego samego `_post_client_secrets_raw`. |
| B6 | `core/config.py:40-74` | `LEGACY_REALTIME_KEY`, `REALTIME_SESSION_TTL_SECONDS=600`, `AUDIO_V2_DEFAULT_VOICE`, `REALTIME_TRANSCRIPTION_MODEL`, `REALTIME_REASONING_EFFORT`, `REALTIME_FIRST_CONVERSATION_MODEL="gpt-realtime-2.1"`, `..._REASONING_EFFORT`, `..._VOICE`. Model zwykłych sesji: `GPT_AGENT_MODEL` (lokalne `.env`: `gpt-realtime-2`; wartość na Heroku do sprawdzenia, pamięć mówi o 2.1-mini dla Reflect v3). |
| B7 | `api/v1/endpoints/conversations.py:507-620` `GET /conversations/realtime/{id}/session_data` | Głos dziennika (journal). Prompt z `settings.SYSTEM_MESSAGE` z podmianą `{FULL_NAME}`, `{GENDER}`, `{AI_LANGUAGE}`, `{LAST_SUMMARY}`, `{PROFILE}`, `{THERAPY_CONTEXT}` + RAG. Legacy beta key `POST /v1/realtime/sessions` za `LEGACY_REALTIME_KEY` (`:535-560`). |
| B8 | `api/v1/endpoints/reflect.py:1879-2047` `GET /reflect/{id}/session_data` | Głos Reflect: bramka Premium 403 (wyjątek dla pierwszej rozmowy), prompt v3 z `reflect_prompt.build_prompt(ctx, "voice", ...)` (`services/reflect_prompt.py:1106`), RAG z poprzednich wpisów, historia tury, zajęcie excerptów (`orca_memory.claim_voice_excerpts`), cache kontekstu Directora w Redis. Zwraca `model=settings.GPT_AGENT_MODEL`. Ten sam legacy key (`:1929-1951`). |
| B9 | `api/v1/endpoints/reflect.py:2050-2100` `_first_conversation_session_data` | Prompt pierwszej rozmowy (`first_conversation.build_system_prompt`), notatka kontynuacji, historia, notatka o pauzie; `data.client_session_config` = reasoning + `truncation` (`services/first_conversation.py:1320-1330`), `model=realtime_model()` (`:1296`). Bez narzędzi (tool fazy usunięty 2026-10-05). |
| B10 | `services/first_conversation.py:77-84, 1276-1365` | Lista dozwolonych głosów realtime, override modelu/effortu/głosu dla mintu (`realtime_mint_override`). |
| B11 | `api/v1/endpoints/reflect.py:2102-2227` `POST /reflect/{id}/audio/user_message_add` | Zapis tury osoby (szyfrowanie, embedding, modality VOICE, auto-tytuł, punkty), potem kanał Directora: notatka pauzy pierwszej rozmowy, `voice_director.run_pipeline` (`DIRECTOR_ENABLED`), dosłanie excerptów z przeszłych wpisów. Zwraca `director.injection_text`, który klient wstrzykuje do sesji. |
| B12 | `api/v1/endpoints/reflect.py:2229` agent_message_add; `conversations.py:301, 325` | Zapis tur agenta i osoby dla dziennika. |
| B13 | `services/voice_director.py:456-629` | Decyzja o wstrzyknięciu; `_detect_crisis_signal` tłumi wstrzyknięcia przy słowach kryzysowych. |
| B14 | `api/v1/endpoints/reflect.py:1686` `/end`, `:1805` `/recap`; `services/orca_memory.py:337` `contains_crisis_language` | Flaga `crisis` po rozmowie (skan słów kluczowych tur osoby + klasyfikacja modelu recapu). Jedyny sygnał kryzysu dla głosu po stronie klienta (bramka oferty). |
| B15 | `services/first_conversation.py:934-965` `SAFETY_SECTION`; `services/reflect_prompt.py:147` | Sekcja SAFETY AND ESCALATION w każdym prompcie Reflect (pierwsza rozmowa i v3), przypięta testem `test_reflect_prompt_v3.py`. |
| B16 | `services/openai_audio_service.py:414-428`; `services/usage_tracking.py:144-160`; `models/models.py:2083-2090, 2136` | Koszt: przy mincie log `REALTIME` z zerowymi tokenami (`is_estimate=True`). Rzeczywistych tokenów rozmowy backend NIE zna. `api_type` to natywny enum PG (`Enum(ApiTypeEnum)`). |
| B17 | `services/reflect_prompt.py:1328-1356` `start_event_properties`; `reflect.py:956` | PostHog `reflect_session_started` z `model` i `reasoning_effort` liczonymi z `GPT_AGENT_MODEL`, nie z faktycznie zmintowanej sesji. |

### 1.2 Frontend (mindsync-frontend/mindsync_app/lib)

| # | Miejsce | Co robi dziś |
|---|---|---|
| F1 | `api/api_managers/audio_v2_manager.dart:22-38` | `POST /audio-v2/realtime-session` z `voice`, `instructions`, `language`, `conversation_id`. |
| F2 | `api/models/audio/realtime_session_model.dart` | Freezed `RealtimeSessionModel` + `VoiceSessionConfig` (`clientSessionConfig` nullable, fallback w cubicie). |
| F3 | `api/api_managers/realtime_api.dart:24-76` | WebRTC: offer, multipart `sdp` + `session` (`{type, model}`) na `https://api.openai.com/v1/realtime/calls` z ephemeral key; URL zahardkodowany w `screens/audio_chat/cubit/audio_chat_cubit.dart:186`. Nie czeka na koniec ICE gathering. |
| F4 | `audio_chat_cubit.dart:610-622` | Data channel `oai-events`, JSON w `handleRealtimeEvent`. |
| F5 | `audio_chat_cubit.dart:626-747` (state machine) | Obsługiwane zdarzenia: `session.created`, `input_audio_buffer.speech_started/stopped/committed`, `response.created`, `response.output_item.added/done` (function_call), `response.done` (usage + function calls), `response.function_call_arguments.done`, `error`, `response.output_audio_transcript.delta/done`, `conversation.item.input_audio_transcription.completed/failed`. Flagi: `_responseActive`, `_userSpeechOpen`, `_awaitingTranscript` (po item_id), `_anonymousCommits`, `isAssistantSpeaking`. |
| F6 | `audio_chat_cubit.dart:1015-1031` `handleSessionCreated` | Po `session.created`: `session.update`, opcjonalnie `conversation.item.create` z promptem jako `system`, opcjonalnie opener `response.create` (`:1256-1285`). |
| F7 | `audio_chat_cubit.dart:1108-1229` `buildSessionUpdatePayload` | `session.update` z `instructions`, transkrypcją, `turn_detection`, `noise_reduction`, `voice`, `reasoning`, `truncation`, `tools`/`tool_choice`; fallback config `:1046-1062`. |
| F8 | `audio_chat_cubit.dart:906-1008` | Function calling: zbiera nazwę z output item, odpowiada `conversation.item.create` `function_call_output` bez `response.create`. Dziś żaden przepływ nie deklaruje narzędzi (pierwsza rozmowa usuwa je jawnie: `first_conversation_cubit.dart:565-575`). |
| F9 | `audio_chat_cubit.dart:695-747, 790-830` | Transkrypcja: każda zakończona transkrypcja tury osoby = `user_message_add` + `reflect_message_submitted` (PostHog, bez tekstu); tura agenta po `output_audio_transcript.done` = `agent_message_add`. |
| F10 | `audio_chat_cubit.dart:1399-1428` `_handleDirectorResponse` | Wstrzyknięcie Directora/excerptów jako `conversation.item.create` (role system) w trakcie rozmowy. |
| F11 | `audio_chat_cubit.dart:1311-1371` `_drainFinalUtterance`, `endCall`; `:1434-1491` `_disposeConnection` | End: mute ścieżek, `input_audio_buffer.commit`, czekanie na transkrypt i zapisy, potem zamknięcie data channel i peer connection. Nie ma zdarzenia zamknięcia sesji po stronie OpenAI. |
| F12 | `audio_chat_cubit.dart:870-880`, `voice_session_options.dart:1-53` `RealtimeUsage.fromResponseDone` | Suma tokenów z `response.done.usage`, trafia tylko do `first_conversation_ended` (PostHog). |
| F13 | `screens/first_conversation/cubit/first_conversation_cubit.dart:205-221, 365-395, 515-560, 625, 965-990` | Mint z `conversation_id`, opcje sesji (bez promptu jako item), planowana odnowa sesji przed limitem 60 min (`first_conversation_session_renewed`), suma usage, bramka kryzysowa oferty (OR sygnałów z `/end`, recapu, tekstu). |
| F14 | `screens/reflect_tab/cubit/reflect_chat_cubit.dart:976`; `api/api_managers/conversation_manager.dart:184` | Mint dla zwykłego Reflect voice i dla dziennika (oba odsyłają prompt w `instructions`). |
| F15 | `screens/settings/widgets/voice.dart:3-13`; `core/app_cubit/app_cubit.dart:20` | Enum głosów: alloy, ash, ballad, coral, echo, sage, shimmer, verse, marin, cedar (domyślnie marin) z próbkami audio w assets. |
| F16 | `core/analytics/analytics_events.dart:1409-1417, 676-699, 1781` | `voice_chat_started`, `voice_chat_ended` (duration, transcription_failed_count, end_drain_timed_out), `voice_session_failed` (stage, reason), `first_conversation_*` z tokenami. |

## 2. Co się psuje lub zmienia przy GPT-Live-1

Wysiłek: S (do 1 dnia), M (2-4 dni), L (tydzień i więcej). Ryzyko: N/Ś/W.

| # | Punkt | Zmiana przy GPT-Live-1 | Wysiłek | Ryzyko |
|---|---|---|---|---|
| 1 | Mint (B1, B3, B4, F1, F3) | [DOC] Live wspiera tylko `v1/live/sessions`; sesję tworzy serwer kluczem projektu, wysyłając JSON `{session, transport: {type: "webrtc", sdp}}`, odpowiedź 201 z `session.id` i SDP odpowiedzi. Client secrets dla Live nieopisane. [WNIOSEK] Flutter nie może już sam rozmawiać z OpenAI; SDP musi iść przez nasz backend (nowy endpoint typu `POST /audio-v2/live-session` z `conversation_id` i `sdp`). Dodatkowy hop przez Heroku, timeout routera 30 s wystarczy. Klient musi czekać na koniec ICE gathering przed wysłaniem offera. | M | Ś |
| 2 | Prompt i kontekst (B7, B8, B9, F6, F7) | [DOC] Instrukcje w `session.instructions` przy starcie, potem tylko `session.instructions.append` (500 tokenów), `session.update` działa wyłącznie na `session.delegation.responses`; inne pola dają `immutable_field_update`. Dzisiejszy `session.update` klienta z instrukcjami zostanie odrzucony. Plus: prompt nie musi już wędrować przez klienta (dziś klient odsyła cały prompt w `instructions` do mintu, co jest powierzchnią do manipulacji), backend buduje go i wysyła sam. Historię wznowionego wątku można dać w `input` (do 128 wiadomości, 8192 tokenów) zamiast doklejać do promptu. Prompt v3 i pierwszej rozmowy trzeba przepisać pod szablon Live (Backchannel, Interruption, Delegation policy), a ewaluacje 2.1-mini z 2026-10-06 przestają obowiązywać. | L | W |
| 3 | client_session_config (B2, B3, F2, F7) | [DOC/ZGŁ] Brak `turn_detection`/eagerness, konfigurowalnego modelu transkrypcji, `reasoning` dla warstwy głosowej, `noise_reduction`, `truncation`, `max_output_tokens`. Prawie cały blob traci sens. Dla Live potrzebny inny, mały kontrakt (`engine`, `session_id`, `voice`). Nie dokładać pól do `VoiceSessionConfig`, bo stary klient wysłałby je w `session.update` do gpt-realtime. | S | N |
| 4 | Wybór modelu (B6, B10, B17) | `_model_supports_reasoning` i cała logika override zakłada prefiks `gpt-realtime-2`. `gpt-live-1` w obecnym polu `model` odpowiedzi trafiłby do starego klienta, który wyśle SDP na `/v1/realtime/calls` z modelem nieobsługiwanym przez ten endpoint: twardy błąd połączenia. Model Live nie może nigdy przejść obecną ścieżką. | S | W (jeśli zrobione źle) |
| 5 | State machine Dart (F5) | [DOC] Zdarzenia z innymi nazwami: `session.started` zamiast `session.created`; transkrypty jako `session.input_transcript.delta` i `session.output_transcript.delta` z `start_ms`/`end_ms`, bez item_id i bez zdarzenia końca tury; brak `response.done` i `response.output_audio.done`; brak `input_audio_buffer.*`. Flagi `_responseActive`, `_awaitingTranscript`, `isAssistantSpeaking` nie mają już źródła. Stan "mówi/słucha" trzeba wyprowadzić z delt i odtwarzania lokalnie. Rekomendacja: osobny `LiveChatCubit` (albo strategia transportu w cubicie) zamiast `if` w 1500 liniach. | L | W |
| 6 | Zapis transkryptów (F9, B11, B12) | Dziś jedna zakończona transkrypcja = jeden `user_message_add`. W Live trzeba samemu kleić delty w tury (heurystyka po przerwach `end_ms`, zmianie mówiącego), a przy full duplex obie strony mogą lecieć równocześnie. Błędne cięcie tur psuje: liczbę `user_turns`, auto-tytuł (>= 2 tury), punkty, RAG, recap, skan kryzysowy. Alternatywa [WNIOSEK]: backend zbiera transkrypty sam przez sideband (`wss://api.openai.com/v1/live/sessions/{id}/attach`) i zapisuje tury po stronie serwera; klient przestaje być jedynym źródłem zapisu (dziś utrata ostatniej tury przy zerwaniu jest realnym problemem, patrz drain). | L | W |
| 7 | Director i excerpty w trakcie (F10, B11, B13) | `conversation.item.create` (role system) nie występuje na liście zdarzeń klienta Live [DOC]. Odpowiednik: `session.thinking.append` (ciche tło, 500 tokenów). Excerpty z przeszłych wpisów mogą przekraczać 500 tokenów: trzeba ciąć albo dzielić. Kontrakt `director` z backendu może zostać, zmienia się tylko sposób wysłania. | S | Ś |
| 8 | Opener agenta (F6, `maybeSendAgentOpener`) | [DOC] `response.create` w Live tylko wznawia pracę backendu, nie rozpoczyna tury. Otwarcie przez model: wiadomość `developer` w `session.input` przy starcie, bez gwarancji, że model się odezwie. Dotyczy pierwszej rozmowy i wątków z seedem (agent mówi pierwszy). | M | Ś |
| 9 | Function calling (F8) | [DOC] Narzędzia przechodzą do `delegation.responses.tools`; wyniki przez `response.item.create` + `response.create`; wywołania czytać z wewnętrznego `response.output_item.done` w kopercie `response.event`, bo `response.completed` ma puste `output` (zgadza się ze zgłoszeniami). Dziś nie używamy żadnego narzędzia, więc kod F8 po prostu nie jest potrzebny w wersji Live. | S (gdy bez narzędzi) | N |
| 10 | Delegacja (nowe) | [DOC] Tryb delegacji wybierany przy starcie, zmiana = nowa sesja. Nie znalazłem trybu "bez delegacji" (pominięcie = tryb klienta wg notatki research). Jeśli model zdeleguje, a nikt nie odpowie, może czekać ("nie zgaduj wyniku w trakcie"). [ZGŁ] model mówi przed `session.delegation.created`, dwa `response.completed` na turę. Faza 1: tryb klienta, w prompcie "nigdy nie deleguj", handler, który na każde `session.delegation.created` od razu odpowiada `session.thinking.append` z neutralną treścią i loguje zdarzenie. | M | Ś |
| 11 | Zamknięcie i odnowa (F11, F13) | [DOC] `session.close` i czekanie na `session.closed` (z `usage.seconds` i `reason`: close_requested, expired, content, remote_hangup, connection_lost), timeout ok. 15 s. Brak `input_audio_buffer.commit`, więc drain ostatniej tury opiera się na deltach już przysłanych. Mute: `session.input_audio.mute` albo jak dziś `track.enabled=false`. Limit długości sesji istnieje (`expired`), wartość nieznana; okno 128k z silnikiem zastępczym przy 90%. Logika odnowy po 60 min w pierwszej rozmowie wymaga przeglądu po pomiarze. `reason: content` to sesja zakończona przez moderację: nowy, osobny stan UI. | M | Ś |
| 12 | Głosy (F15, B10) | [DOC wg notatki research] 12 nowych głosów (quartz, ripple, vesper, willow, stone, gleam, meridian, bossa, tempo, beacon, delta, cinder), domyślny `marin`. Wybór z Ustawień (alloy...cedar) nie mapuje się 1:1. Backend musi mieć tabelę mapowania i walidację (głos niezmienny po starcie). Próbki w assets i ekran Ustawień do aktualizacji. | M | Ś |
| 13 | Języki | Brak oficjalnej listy języków; brak potwierdzenia PL, DE, ES, FR, NB. Aplikacja ma 7 języków. Nie ma konfiguracji języka transkrypcji (dziś przekazujemy `language` do `gpt-4o-mini-transcribe`). Blokada dla wszystkiego poza EN do czasu testu. | M (test) | W |
| 14 | Koszt (B16, F12) | Live: $0,05/min co sekundę, cisza się liczy, mute nie zatrzymuje licznika, 15 s naliczane z góry przy WebRTC; backend osobno. Dziś backend nie zna kosztu rozmowy wcale. Live daje `session.usage.updated` i `session.closed.usage.seconds`. Rekomendacja: zapis sekund po stronie serwera (sideband albo endpoint końca sesji), rekord z `api_type=REALTIME` i `model="gpt-live-1"`, nowa gałąź kosztu "per minute" w `usage_tracking.py` (wzór STT już tam jest, `price_per_minute`), wiersz w `model_pricing` jako dane. NIE dodawać nowej wartości do natywnego enuma `ApiTypeEnum` bez migracji `ADD VALUE IF NOT EXISTS` (ryzyko boot-crash i dryfu enumów). | M | Ś |
| 15 | PostHog (F16, B17) | `reflect_session_started.model` liczony z `GPT_AGENT_MODEL` byłby fałszywy dla sesji Live. Brak eventu o tym, który silnik faktycznie ruszył i czy był fallback. Patrz sekcja 4. | S | N |
| 16 | Legacy beta key (B7, B8) | `LEGACY_REALTIME_KEY` mintuje klucz beta `gpt-realtime` dla starych Androidów przy każdym `session_data`. Live nic tu nie zmienia, ale nowy endpoint nie może dzielić tej logiki. | brak | N |
| 17 | Sesja transkrypcyjna (B5) | Bez zmian, zostaje na Realtime. | brak | N |

## 3. Ścieżka bezpieczeństwa i kryzysu w głosie

### Jak działa dziś

1. Prompt: sekcja SAFETY AND ESCALATION (`services/first_conversation.py:941-958`), nadrzędna nad resztą promptu, wspólna dla Reflect v3 i pierwszej rozmowy, przypięta testem. Model głosowy sam mówi: jestem maszyną, kogo możesz dziś złapać, numer alarmowy cyfra po cyfrze dwa razy, nigdy metody. To jedyna reakcja w czasie rzeczywistym.
2. Brak narzędzi: żadne narzędzie kryzysowe nie istnieje. Tool fazy był jedynym narzędziem i został usunięty 2026-10-05, bo zawieszał rozmowę.
3. W trakcie rozmowy: `voice_director._detect_crisis_signal` (`services/voice_director.py:456-466, 627-629`) tylko wycisza wstrzyknięcia Directora. Klient nie dostaje żadnego sygnału kryzysu w trakcie rozmowy głosowej (w tekście jest `crisis_detected` z `/message`, `reflect.py:1458`).
4. Po rozmowie: `/end` i `/recap` zwracają `crisis` (skan `orca_memory.contains_crisis_language` plus klasyfikacja recapu). Klient w pierwszej rozmowie nie pokazuje oferty ani recapu po kryzysie (`first_conversation_cubit.dart:965-990`). Pamięć Orca nie uczy się z takiej rozmowy. Kryzys nigdy nie trafia do PostHog.

### Czy przetrwa architekturę bez narzędzi w warstwie głosowej

Tak, w zasadzie, bo dzisiejsza ścieżka i tak nie używa narzędzi. Warunki i nowe ryzyka:

- Sekcja SAFETY musi zostać w `session.instructions` warstwy głosowej, nie w promptcie backendu, a w "Delegation policy" musi być zakaz delegowania czegokolwiek z zakresu SAFETY. Delegacja rozmowy kryzysowej to opóźnienie, inny model i ryzyko, że głos będzie "czekał na wynik". [WNIOSEK]
- Moderacja OpenAI [DOC]: część zdarzeń ucina audio asystenta do końca bieżącej wypowiedzi z `error`, część kończy sesję (`reason: content`). W rozmowie o samookaleczeniu to może przerwać dokładnie zdanie z numerem pomocy albo rozłączyć osobę w kryzysie. Musi to być pierwszy test prototypu (scenariusze z eval Reflect, w EN). Klient musi mieć dla `reason: content` spokojny ekran z numerem alarmowym na ekranie, nie ogólny błąd.
- Instrukcji nie da się wymienić w trakcie, tylko dopisać (`session.instructions.append`, może przerwać mowę). To w rzeczywistości daje nową możliwość: backend na sidebandzie skanuje `session.input_transcript.delta` tym samym `contains_crisis_language` i przy trafieniu dopisuje krótkie przypomnienie SAFETY oraz blokuje wstrzyknięcia Directora. Dziś takiej reakcji w trakcie rozmowy nie ma wcale. Zastrzeżenie [DOC]: korekta nie cofa audio, które już padło.
- Ewaluacja zgodności z sekcją SAFETY była robiona na gpt-realtime-2.x. Na Live trzeba ją powtórzyć przed jakimkolwiek ruchem użytkowników, a dla języków innych niż EN dopiero po potwierdzeniu wsparcia języka.
- Rekomendacja: Critical/High od `security-guardian` blokuje wdrożenie (CLAUDE.md), a zmiana dotyka danych zdrowia psychicznego, więc przegląd jest obowiązkowy przed prototypem dla użytkowników zewnętrznych.

## 4. Rekomendowana ścieżka wdrożenia

### 4.1 Zasada nadrzędna: dwa silniki obok siebie

Live to drugi transport, nie zamiana modelu. Obecny przepływ (`session_data` + `POST /audio-v2/realtime-session` + `/v1/realtime/calls`) zostaje nietknięty i dalej obsługuje każdy build w sklepie. Live dostaje osobny endpoint i osobną ścieżkę w kliencie.

### 4.2 Wybór silnika (backend-driven, z deklaracją zdolności klienta)

1. Klient z obsługą Live wysyła w `GET /reflect/{id}/session_data` nagłówek albo query, np. `voice_engines=realtime,live` (lub `X-Voice-Engines`). Brak deklaracji = zawsze realtime. To jest twarda gwarancja dla starych buildów, niezależna od wersji aplikacji, bo stary klient nigdy tego nie wyśle.
2. Backend decyduje per typ sesji: `VOICE_LIVE_ENABLED_FOR` w Config Vars (`""` domyślnie; wartości `reflect`, `first_conversation`, `journal`) plus flaga PostHog po stronie serwera dla odsetka użytkowników (allowlista kont testowych na start) plus warunek języka (faza 1: tylko `ai_language` EN).
3. Odpowiedź `session_data` dostaje addytywne pole `voice_engine: "realtime" | "live"` w `data` (pole `data` już istnieje w `SessionDataResponse`, więc bez zmiany schematu współdzielonego z dziennikiem).
4. Dla `live` klient woła nowy `POST /audio-v2/live-session` z `{conversation_id, sdp}`. Backend sam buduje prompt (nie przyjmuje instrukcji od klienta), sam wybiera głos (mapowanie z Ustawień), tworzy sesję `POST /v1/live/sessions`, zwraca `{session_id, sdp_answer, voice, engine: "live"}` i opcjonalnie podpina sideband.
5. Fallback: jeśli `/v1/live/sessions` zwróci błąd albo przekroczy np. 8 s, backend odpowiada `{engine: "realtime", fallback_reason}`, a klient przechodzi znaną ścieżką (`POST /audio-v2/realtime-session`). Klient robi to samo, gdy połączenie Live nie dojdzie do `session.started` w zadanym czasie. Wstrzymanie całości: wyczyszczenie `VOICE_LIVE_ENABLED_FOR` na Heroku, bez deployu.

Wersja aplikacji: nowe pole i endpoint są addytywne, więc wymagany jest tylko build z nową ścieżką; stare buildy działają jak dziś. Minimalnej wersji nie trzeba wymuszać. Przy przyszłym wygaszaniu realtime trzeba będzie sprawdzić w PostHog rozkład `$app_version` sesji głosowych.

### 4.3 Fazy

1. Faza 0 (offline, S-M): skrypt eval jak `scripts/first_conversation_eval.py`, ale na Live: scenariusze SAFETY, długość wypowiedzi, opener, języki PL/DE/ES/FR/NB, moderacja. Bez kodu aplikacji. Wynik decyduje o fazie 1.
2. Faza 1 (BE, M-L): endpoint `live-session`, przepisany prompt voice pod szablon Live, mapowanie głosów, sideband z zapisem sekund i skanem kryzysowym, testy (w tym offline import aplikacji, bo endpoint ląduje w drzewie routerów ładowanym przy boocie).
3. Faza 2 (FE, L): `LiveChatCubit` lub strategia transportu, sklejanie delt w tury (albo rezygnacja z zapisu klienta na rzecz sidebandu), `session.close`/`session.closed`, stany `reason: content` i `expired`, Ustawienia głosu.
4. Faza 3: allowlista wewnętrzna na TestFlight, potem odsetek EN za flagą, porównanie kohort.

Kolejność wdrożenia: backend pierwszy (endpoint martwy, dopóki żaden klient się nie deklaruje), potem build klienta. Rollback: Config Var, bez deployu.

### 4.4 Co mierzyć w PostHog

Eventy istniejące rozszerzyć o `voice_engine` (`realtime` | `live`) i `model`: `voice_chat_started`, `voice_chat_ended`, `voice_session_failed`, `reflect_session_started` (backend, z modelu faktycznej sesji, nie z `GPT_AGENT_MODEL`), `first_conversation_ended`.

Nowe (propozycja nazw, do uzgodnienia z taksonomią):

| powierzchnia | zdarzenie | nazwa | kluczowe właściwości | gdzie |
|---|---|---|---|---|
| wybór silnika | backend wybrał silnik | `voice_engine_selected` | `engine`, `session_kind`, `reason` (flag, language, capability) | backend |
| fallback | Live nie ruszył | `voice_live_fallback` | `stage` (create, connect, started_timeout), `error_code` | backend dla create, klient dla connect |
| start | pierwsze audio agenta | do `voice_chat_started` lub osobno | `time_to_first_agent_audio_ms` | klient |
| koniec | zamknięcie potwierdzone | do `voice_chat_ended` | `close_reason` (z `session.closed`), `close_confirmed` (bool), `billed_seconds`, `user_turns`, `user_fragments` | klient |
| moderacja | audio ucięte / sesja zakończona | `voice_moderation_event` | `kind` (audio_cut, session_ended); bez treści | klient |
| delegacja | model próbował delegować | `voice_delegation_attempted` | `count` | backend (sideband) |

Porównanie kohort Live vs realtime: odsetek nieudanych startów, mediana długości, `user_turns`, powroty D1/D7 do głosu, konwersja na paywall po pierwszej rozmowie, koszt na minutę z `token_usage_log`. Odsetka rozmów z kryzysem NIE mierzyć w PostHog (zasada z `analytics_events.dart:601-604`): tylko agregat z bazy przez `database-administrator`.

Prywatność: zero transkryptów, zero tekstu, zero flag zdrowia w PostHog.

## 5. Blast radius (CLAUDE.md, Change Safety)

1. Kto konsumuje:
   - Endpointy `session_data` (Reflect, dziennik) i `realtime-session` konsumują: `reflect_chat_cubit.dart:976`, `first_conversation_cubit.dart:216`, `conversation_manager.dart:184`, `audio_chat_cubit.dart` (wszystkie przepływy głosowe), testy BE `test_audio_v2_config.py`, `test_audio_v2_noise_reduction.py`, `test_first_conversation*.py`.
   - `SessionDataResponse` jest współdzielony z głosem dziennika: zmiany tylko addytywne w `data`.
   - `_model_supports_reasoning` używają `openai_audio_service`, `first_conversation.client_session_overrides`, `reflect_prompt.realtime_reasoning_effort`.
   - `user_message_add` i `agent_message_add` zasilają embeddingi, auto-tytuł, punkty Character, recap, pamięć Orca, skan kryzysowy, joby analityczne po `/end`. Zmiana sposobu cięcia tur dotyka ich wszystkich.
2. Boot-critical: nowy router i import klienta sideband ładują się przy każdym boocie (`app/main.py` importuje całe drzewo). Sideband nie może startować w lifespan. Ma być per sesja, w workerze RQ albo w zadaniu tła z importem leniwym. Nowa zależność (np. biblioteka websocket) w `requirements.txt` z przypiętą wersją, sprawdzona importem aplikacji offline. Długie połączenie WebSocket w procesie web na Heroku to ryzyko dla gunicorna (wątki, restarty dyna co 24 h). Rekomendacja: worker lub osobny proces, decyzja przy projektowaniu fazy 1.
3. Model, migracja, prod DB: bez nowych tabel w fazie 1. Koszt jako wiersz `model_pricing` (dane) i gałąź w kodzie, bez nowej wartości natywnego enuma `api_type`. Jeśli kiedyś `LIVE` jako `api_type` albo nowy `FeatureEnum`, to tylko migracją `ADD VALUE IF NOT EXISTS` w autocommit_block, uwzględniając dryf UPPERCASE na prodzie.
4. SQLite i Postgres: dotyczy tylko punktu 3; bez DDL nie ma ryzyka.
5. Deploy i migracja: brak migracji w fazie 1. Backend jako pierwszy, endpoint nieaktywny bez flagi.
6. Kontrakt BE-FE: wszystko addytywne. Pole `model` w `RealtimeSessionResponse` i `SessionDataResponse` NIGDY nie dostaje `gpt-live-1` (stary klient połączyłby się z `/v1/realtime/calls` i padł). Błąd po stronie Live nie może skończyć się w kliencie jako 403 Premium ani "nowy użytkownik": fallback na realtime, a dopiero potem dzisiejsze stany błędów.
7. Stare buildy w sklepie: bez deklaracji `voice_engines` nie widzą żadnej zmiany. Dotyczy także Androidów na kluczu beta (`LEGACY_REALTIME_KEY`).

Koszty i limity operacyjne: Live wymaga tieru płatnego (Free nieobsługiwany), limit równoległych sesji Build 50 / Launch 300 / Grow 500. Tier konta OpenAI do sprawdzenia przez operatora przed fazą 3.

## 6. Otwarte pytania (nie zweryfikowane w dokumentacji)

- Wsparcie i jakość PL, DE, ES, FR, NB (brak listy języków). Blokada dla rynku poza EN.
- Czy istnieje tryb bez delegacji i co robi model, gdy delegacja nie dostaje odpowiedzi.
- Limit długości sesji (`expired`) i limit wiadomości data channel (262144 B tylko ze zgłoszeń; dla nas mniej istotne, bo prompt idzie HTTP z serwera).
- "Jawna detekcja tury" i keyword biasing: tylko w relacjach o premierze, brak parametru w dokumentacji.
- Czy client secrets dla `/v1/live/sessions` istnieją (zakładam, że nie, więc SDP przez backend).
- Jakie `GPT_AGENT_MODEL` stoi dziś na Heroku (lokalne `.env`: `gpt-realtime-2`), potrzebne do uczciwego porównania kosztu z 2.1-mini.
