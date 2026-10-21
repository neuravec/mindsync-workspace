---
name: project-reflect-prompt-rewrite-2026-09-18
description: "Przebudowa promptu Reflect wdrozona 2026-09-18 (commit f4e17e0); zmiana promptu dosiega WSZYSTKICH userow natychmiast, niezaleznie od wersji apki"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6e7e7bf6-e427-4d6e-8d82-a65265770d52
  modified: 2026-09-18T09:37:37.212Z
---

Wdrozone 2026-09-18 w DWOCH rundach: **f4e17e0** (runda 1) i **166a8eb** (runda 2,
po realnym uzyciu). Obie backend-only, bez migracji.
Powod: "agent jest dzis meczacy dla usera i szybko pojawia sie irytacja".

**Najwazniejsza wlasciwosc operacyjna, nieoczywista z kodu: zmiana promptu Reflect
dosiega WSZYSTKICH uzytkownikow natychmiast po deployu, takze tych na starych
buildach aplikacji.** Prompt glosowy sklada backend (`reflect.py` `session_data`)
i zwraca go klientowi, a Flutter tylko przenosi ten string dalej jako `instructions`
(`reflect_chat_cubit.dart:946`, `audio_chat_cubit.dart:747`). W kodzie frontu nie ma
ani jednego zaszytego promptu. To odwrotnosc zwyklego rytmu tego projektu, gdzie
front czeka dni na TestFlight. Zmiana promptu nie czeka na nic.

`.env` JEST sledzony przez gita i jedzie w slugu, wiec zmiana promptu to deploy kodu,
nie flip konfiguracji. Nie da sie jej cofnac przez `heroku config:set`.

**Prompt zyje w DWOCH miejscach i musza jechac jednym commitem:** wartosc
`REFLECT_SYSTEM_MESSAGE` w `.env` oraz zaszyty fallback w `reflect.py`, ktory odpala
sie przy pustym ustawieniu. Rozjazd daje agentowi dwie rozne osobowosci zaleznie od
tego, czy setting sie rozwinie.

Ustalenie merytoryczne, ktore przestawilo kierunek prac: **dlugosc wypowiedzi nie byla
problemem** (limit 2 do 4 zdan w glosie zgadza sie z rekomendacja OpenAI dla Realtime).
Problemem byla czestotliwosc pytan. Regula "jedno pytanie na wiadomosc" jest dobra jako
sufit, ale zla jako podloga: wymog pytania w kazdej turze odtwarza pulapke
pytanie-odpowiedz. Zrodla i cala analiza w
`Business_requirements/MS_reflect_intro/research-ai-therapist-prompting.md`,
propozycja z uzasadnieniem kazdej dyrektywy w `reflect-prompt-rewrite-proposal.md`.

Typografia: tekst mial juz zakaz em-dasha przez `_FORMATTING_SUFFIX` doklejany
w `gpt_function`; glos nie mial, bo idzie przez `audio_v2.py` i tej sciezki nie dotyka.

Otwarte po tym wdrozeniu: `tone_archetype` w Reflect domysla sie na `"supportive"`,
slowa spoza kanonicznego slownika `Literal["realist","coach","friend","sage","explorer"]`;
prompt directora jest zaszyty w kodzie mimo istniejacego pustego
`DIRECTOR_INJECTION_PROMPT`; sekcja kryzysowa weszla bez przegladu klinicysty i prawnika
na jawna decyzje operatora. Szczegoly i reszta follow-upow w `TASKS-reflect-entry.md`.

## Runda 2: dwie wady wywolane przez runde 1

**Agent stracil inicjatywe i recytowal.** Runda 1 wdrozyla wylacznie simple reflection
(parafraze) i jednoczesnie zdjela przymus pytania, konfrontacje i nazywanie wzorcow.
Zostalo odbijanie cudzych slow. Naprawa sama definicja NIE wystarczyla, bo unieważnialy
ja dwie inne linie: `LIMITS` mial "Never interpret the user's experience beyond what
they have said" (kategoryczny zakaz complex reflection obok zakazu diagnozowania), a
`PATTERNS` wymagal zgody, ktora zjadala jedyne pytanie w turze, raz na rozmowe.
Narzedzie oblozone oplata i limitem = model go nie uzywa.

**Wzorzec ogolny, wart zapamietania poza tym projektem: zakaz frazy PRZESUWA problem,
nie usuwa go.** Runda 1 zakazala pustej walidacji na POCZATKU wypowiedzi, wiec
wypelniacz przeniosl sie na KONIEC ("to pierwszy krok w zrozumieniu emocji").
Runda 2 zakazuje przez KRYTERIUM (zdanie prawdziwe o prawie kazdym), nie przez liste.

**"Start fresh" otwieral kontekstem: TRZY zrodla, nie jedno.** Najmniej oczywiste
i najwazniejsze: blok `Therapy context: {THERAPY_CONTEXT}` jest w prompcie ZAWSZE,
niezaleznie od RAG, wiec samo wylaczenie zasiewania RAG nie zamykalo wady. Zamyka ja
jawna instrukcja otwarcia (`build_voice_greeting_instruction`, blok `OPENING GREETING`).
Front `reflect_tab_screen.dart:1061` ustawia `agentOpensFirst: true` bezwarunkowo
i ZOSTAJE tak celowo, bo operator chce powitania, nie ciszy.

Nazwa `OPENING GREETING`, nie `OPENING TURN`, jest wymuszona przez piec asercji na
dokladny literal w `test_reflect_entry_flow.py` i `test_reflect_entry_pre_migration.py`.

`DIRECTOR_ENABLED=True` na prodzie, mimo ze `config.py` domyslnie ma `False`.

Powiazane: [[project-reflect-entry-batch-2026-09-18]],
[[reference-backend-autodeploy-on-push]], [[feedback-claim-not-verified-until-state-reproduced]]
