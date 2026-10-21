# Użycie, aktywacja, retencja i lejek paywalla – surowy wyciąg z PostHog

- **Data**: 2026-09-12 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okno**: 2026-08-13 -> 2026-09-13 (30 dni), dodatkowo 2026-06-14 -> 2026-09-13 (90 dni) i 12 tygodni wstecz dla kohort. Wszystkie znaczniki czasu UTC.
- **Pytanie**: Kompletny materiał źródłowy o użyciu, aktywacji, retencji i lejku paywalla dla MindSync, pod raport biznesowy (operator obawia się złego kierunku produktu i że użytkownicy zostają wyłącznie na darmowej wersji).
- **Filtr domyślny „app"**: `properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')` – wyklucza stronę marketingową (web), zdarzenia backendowe (posthog-python), wewnętrzne testy (TestFlight/emulator) i znany bottraffic (2 modele urządzeń). Tam gdzie ten filtr NIE jest zastosowany (bo trzeba złapać zdarzenia backendowe typu `reflect_message_sent` czy `moment.sent`), jest to jawnie zaznaczone.
- **Populacja w oknie 30d**: użytkownicy realnie otwierający appkę (`$lib=posthog-flutter`, po odfiltrowaniu botów) = **127**. Użytkownicy „dotknięci" przez backend (dowolne zdarzenie `posthog-python`, np. wysyłka powiadomienia, generacja podsumowania) = **1874**. To kluczowa liczba do zapamiętania w całym raporcie: backend „obsługuje" analitycznie ok. 15x więcej kont niż realnie otwiera appkę w danym miesiącu.

## Weryfikacja instrumentacji (skrót, szczegóły w tabelach niżej)

| Event / funkcja | Płynie? | Ostatnio widziany | Uwaga |
|---|---|---|---|
| `moment.sent` / `.scheduled` / `.expired` / `.opened` | TAK (backend) | 2026-09-12 | populacja odbiorców ~1800+, nie pokrywa się z aktywną bazą |
| `paywall_shown` | TAK, ale bardzo cienko | 2026-09-07 | istnieje dopiero od 2026-08-16; 10 zdarzeń/7 osób w 30d i 90d łącznie |
| `subscription_purchase_completed` | TAK | 2026-09-07 | 5 osób w 30d, 8 w 90d – PostHog to NIE jest prawda przychodowa, patrz Zastrzeżenia |
| `trial_started` / `trial_ended` | NIE PŁYNIE | – | zero zdarzeń w całej historii projektu (sprawdzone w pełnym katalogu event_definitions) |
| `conversation_started/_message_sent/_ended` | MARTWE od miesiąca | 2026-08-11 | zero zdarzeń w oknie 30d mimo że istnieją w katalogu; żywy proxy to `reflect_*` |
| habit tracker (dowolny event) | BRAK INSTRUMENTACJI | – | zero eventów zawierających „habit" w całej historii projektu; funkcja jest widgetem na `mainPage`, nie osobnym ekranem, więc nawet `$screen` jej nie łapie |
| „Your Session" jako pojedynczy event | BRAK dedykowanego eventu | – | flow pokryty pośrednio przez `prep_capture_started`/`prep_card_started` + `recording_started` + `debrief_started`/`debrief_created` (3 osobne etapy) |
| Threads | pokryte przez `reflect_thread_opened/_deleted` | 2026-09-12 | brak osobnego eventu „Threads", to część Reflect |
| `summary_viewed` period_type=`daily` | NIE ISTNIEJE | – | jedyne wartości `period_type` w danych to `weekly` i `monthly_audit` – podsumowania dzienne nie są mierzalne w PostHogu w ogóle |
| `recording_processing_started/_completed` (backend pipeline) | TERAZ PŁYNIE | 2026-09-07 | poprzednia notatka z 2026-08-10 mówiła „nigdy nie wystąpił” – to się zmieniło, ale wolumen wciąż mały (5 użytkowników/30d) |

---

## 1. Inwentarz eventów (30d), posortowany malejąco

Top 30 z ~150 aktywnych nazw eventów (pełna lista w pliku wynikowym zapytania, dostępna na żądanie). `events_30d` = liczba zdarzeń, `users_30d` = distinct `person_id`.

| event | events_30d | users_30d |
|---|---|---|
| moment.sent | 24473 | 1815 |
| moment.expired | 21499 | 1825 |
| moment.scheduled | 16683 | 1829 |
| weekly_summary_generated | 7233 | 1817 |
| api_error | 4639 | 82 |
| $screen | 3830 | 134 |
| monthly_audit_generated | 3584 | 1810 |
| tab_switched | 3092 | 51 |
| timeline_viewed | 947 | 66 |
| workspace_opened | 620 | 42 |
| first_capture_prompt_shown | 617 | 60 |
| character_card_viewed | 392 | 37 |
| onboarding_step_viewed | 384 | 52 |
| bio_viewed | 368 | 34 |
| notification_permission_prompted | 349 | 61 |
| onboarding_step_completed | 349 | 46 |
| therapy_context_updated | 348 | 48 |
| notification_permission_granted | 330 | 52 |
| reflect_message_submitted | 314 | 19 |
| $exception | 309 | 32 |
| app_tour_step_viewed | 307 | 37 |
| realization_detected | 294 | 5 |
| timeline_filter_changed | 252 | 12 |
| app_install_attributed | 191 | 115 |
| reflect_message_sent | 178 | 16 |
| welcome_cta_tapped | 168 | 66 |
| client_error | 148 | 11 |
| reflect_thread_opened | 136 | 27 |
| profile_updated | 112 | 49 |
| recording_upload_completed | 105 | **1** |

**Odczyt**: pierwsze 7 pozycji to prawie wyłącznie zdarzenia generowane automatycznie przez backend (planowanie/wysyłka powiadomień, generacja podsumowań) – nie mierzą one realnego użycia appki, tylko to, że system coś komuś wysłał. Pierwszy prawdziwy sygnał użycia to `api_error` (pozycja 5, sam w sobie problem), potem `$screen`/`tab_switched` (nawigacja) i dopiero `timeline_viewed`/`workspace_opened` jako pierwsze realne funkcje produktowe. `recording_upload_completed`: 105 zdarzeń od **1 osoby** – klasyczny skew pojedynczego konta, nie wzorzec.

---

## 2. DAU / WAU / MAU (30d, filtr app, po odfiltrowaniu botów) + podział $os i $app_version

**MAU (30 dni)**: **127** unikalnych użytkowników.

DAU dzień po dniu (min 4, max 16, mediana ok. 8):

| dzień | DAU | dzień | DAU | dzień | DAU |
|---|---|---|---|---|---|
| 08-13 | 16 | 08-23 | 8 | 09-02 | 12 |
| 08-14 | 10 | 08-24 | 11 | 09-03 | 12 |
| 08-15 | 11 | 08-25 | 7 | 09-04 | 7 |
| 08-16 | 12 | 08-26 | 7 | 09-05 | 4 |
| 08-17 | 8 | 08-27 | 8 | 09-06 | 6 |
| 08-18 | 16 | 08-28 | 8 | 09-07 | 12 |
| 08-19 | 8 | 08-29 | 4 | 09-08 | 14 |
| 08-20 | 12 | 08-30 | 6 | 09-09 | 7 |
| 08-21 | 13 | 08-31 | 11 | 09-10 | 8 |
| 08-22 | 7 | 09-01 | 4 | 09-11 | 5 |
| | | | | 09-12 | 7 (dzień niepełny) |

WAU po tygodniach kalendarzowych (`toStartOfWeek`):

| tydzień od | WAU |
|---|---|
| 2026-08-09 | 28 (tydzień częściowy, okno zaczyna się 08-13) |
| 2026-08-16 | 51 |
| 2026-08-23 | 34 |
| 2026-08-30 | 35 |
| 2026-09-06 | 37 (tydzień częściowy, trwa) |

Stickiness (śr. DAU / WAU) dla pełnych tygodni ~09/28-35 ≈ 26-31%.

**Podział $os (30d, jedna wartość na osobę)**: Android **108**, iOS **19** (suma = 127, zgadza się z MAU). iOS to próbka poniżej progu 25 – traktować kierunkowo, nie jako stabilny wskaźnik.

**Podział $app_version (30d, distinct users per wersja – osoba może wystąpić w >1 wersji przy aktualizacji w trakcie okna, suma > 127)**:

| wersja | użytkownicy |
|---|---|
| 2.0.77 | 56 |
| 2.0.85 | 45 |
| 2.0.89 | 38 |
| 2.0.76 | 9 |
| 2.0.44 | 5 |
| 2.0.75 | 4 |
| 2.0.60 | 3 |
| 2.0.88 | 2 |
| 2.0.80 | 2 |
| 2.0.87 / 2.0.79 / 2.0.82 / 2.0.36 / 2.0.84 / 2.0.83 / 2.0.78 | po 1 |

Rollout wygląda zdrowo: trzon bazy jest na 3 najnowszych wersjach (2.0.77/2.0.85/2.0.89), długi ogon starych wersji (2.0.36 sprzed miesięcy) to pojedyncze osoby.

---

## 3. Nowi użytkownicy tydzień po tygodniu (12 tygodni) + powrót w kolejnym tygodniu

Kohorta = pierwszy event danej osoby w historii (app, po odfiltrowaniu botów). `returned_next_week` = ta sama osoba miała jakiekolwiek zdarzenie w kalendarzowym tygodniu bezpośrednio po tygodniu rejestracji.

| tydzień kohorty | nowi użytkownicy | wrócili w kolejnym tygodniu | % powrotu |
|---|---|---|---|
| 2026-06-14 | 37 | 2 | 5.4% |
| 2026-06-21 | 29 | 5 | 17.2% |
| 2026-06-28 | 30 | 6 | 20.0% |
| 2026-07-05 | 33 | 4 | 12.1% |
| 2026-07-12 | 20 | 1 | 5.0% |
| 2026-07-19 | 24 | 2 | 8.3% |
| 2026-07-26 | 25 | 3 | 12.0% |
| 2026-08-02 | 30 | 7 | 23.3% |
| 2026-08-09 | 27 | 5 | 18.5% |
| 2026-08-16 | 25 | 3 | 12.0% |
| 2026-08-23 | 9 | 1 | 11.1% |
| 2026-08-30 | 14 | 3 | 21.4%* |
| 2026-09-06 | 18 | 0 | n/d* |

`*` Okna niekompletne: dla kohorty 2026-08-30 tydzień następny dopiero się kończy (dane z 2026-09-12), dla 2026-09-06 tydzień następny jeszcze się nie zaczął – 0% tam to artefakt okna, nie realny wynik, nie czytać jako spadek.

**Odczyt**: powrót w kolejnym tygodniu mieści się w paśmie 5-23%, mediana w okolicach 12%. Nie ma wyraźnego trendu wzrostowego ani spadkowego w 12 tygodniach – to płaskie, niskie utrzymanie tydzień-po-tygodniu.

---

## 4. Retencja tygodniowa (kohorta wg tygodnia pierwszego zobaczenia, W0-W4, 8 tygodni wstecz)

| kohorta | wielkość | W0 | W1 | W2 | W3 | W4 |
|---|---|---|---|---|---|---|
| 2026-07-12 | 20 | 20 | 1 | 2 | 1 | 1 |
| 2026-07-19 | 24 | 24 | 2 | 0 | 0 | 0 |
| 2026-07-26 | 25 | 25 | 3 | 1 | 0 | 0 |
| 2026-08-02 | 30 | 30 | 7 | 7 | 5 | 2 |
| 2026-08-09 | 27 | 27 | 5 | 2 | 1 | 0 |
| 2026-08-16 | 25 | 25 | 3 | 3 | 2 | 0 |
| 2026-08-23 | 9* | 9 | 1 | 2 | 0 | 0 |
| 2026-08-30 | 14* | 14 | 3 | 0 | 0 | 0 |
| 2026-09-06 | 18* | 18 | 0 | 0 | 0 | 0 |

`*` n<25 (kohorty 08-23, 08-30, 09-06) – małe próbki, kierunkowe. Dla kohort 08-23/08-30/09-06 kolumny W2-W4 są też częściowo lub całkowicie ucięte przez okno obserwacji (jeszcze nie minęło tyle tygodni) – zera tam nie oznaczają realnego zera.

**Odczyt z kompletnych kohort (07-12 do 08-16)**: W1 zwykle 10-25% wielkości kohorty, W2 spada dalej, W4 to pojedyncze osoby lub zero. Kohorta 08-02 wygląda relatywnie najlepiej (W1=23%, W2=23%, W4=7%) ale to wciąż mała próbka (n=30) – nie ma dowodu na trwałą poprawę, raczej szum.

### D1 / D7 / D30 (kohorty z ostatnich 90 dni, okna liczone tak by nie ucinać prawego ogona)

| metryka | wielkość kohorty kwalifikującej się | powrócili | % |
|---|---|---|---|
| D1 (kohorty sprzed 2026-09-11) | 319 | 24 | 7.5% |
| D7 (kohorty sprzed 2026-09-05) | 303 | 12 | 4.0% |
| D30 (kohorty sprzed 2026-08-13) | 244 | **2** | **0.8%** |

**D30 = 2 osoby na 244** – to najtwardsza liczba w tym raporcie i bezpośrednio odpowiada na obawę operatora: prawie nikt, kto zainstalował appkę w ostatnich ~2-3 miesiącach, nie wraca po miesiącu.

---

## 5. One-and-done (90 dni)

Wśród 382 użytkowników z jakąkolwiek aktywnością w ostatnich 90 dniach: **253 (66.2%)** miało aktywność tylko w jednym dniu kalendarzowym w całej swojej historii w appce.

---

## 6. Lejek onboardingu (30d), per krok, iOS/Android

Instrumentacja urosła: teraz widać **9 kroków** (poprzednio w projekcie widziano tylko 8 – `personalise` to nowość). `viewed`=osoby, które zobaczyły krok, `completed`=osoby, które go ukończyły.

| krok | Android viewed/completed | iOS viewed/completed* |
|---|---|---|
| legal_gate | 34 / 31 | 7 / 7 |
| challenges | 32 / 29 | 7 / 7 |
| intensity | 29 / 28 | 7 / 7 |
| journey | 28 / 28 | 8 / 8 |
| modality | 28 / 28 | 8 / 8 |
| schedule | 28 / 28 | 8 / 8 |
| companion | 28 / 25 | 8 / 8 |
| personalise | 39 / 35 | 7 / 7 |
| lead_source | 25 / 25 | 8 / 8 |

`*` próbki iOS (7-8 osób) są poniżej progu 25 – czysto kierunkowe.

**Start vs koniec (30d, po os)**: Android – `onboarding_started` 35 → `onboarding_completed` 25 (71.4%); iOS – 8 → 8 (100%, próbka za mała by cokolwiek wnioskować). Razem: 43 startujących → 33 kończących = **76.7%** ukończenia całego onboardingu.

**Odczyt**: drop-off między krokami jest minimalny (każdy krok kończy prawie kto go zaczął, >85-100%). Cały „wyciek" onboardingu dzieje się na wejściu (legal_gate) i przy `companion`/pierwszym kroku – nie ma jednego dramatycznego kroku-zabójcy, to raczej rozłożone ścieranie się liczby osób w miarę przechodzenia przez ankietę.

---

## 7. Adopcja funkcji (30d) – distinct users, liczba użyć, mediana użyć/os.

Nazwy eventów zweryfikowane w PostHogu (nie zgadywane) – tam gdzie nie ma dedykowanego eventu, jest to jawnie opisane jako proxy.

| funkcja | event(y) źródłowe | użytkownicy (n=127 MAU) | % MAU | zdarzenia | mediana/os. |
|---|---|---|---|---|---|
| Statystyki / Timeline | `timeline_viewed` | 66 | 52.0% | 947 | 2.0 |
| Dashboard / Workspace | `workspace_opened` | 42 | 33.1% | 620 | 4.0 |
| „Your Session" (dowolny etap: prep/nagranie/debrief) | `prep_capture_started`∨`prep_card_started`∨`recording_started`∨`debrief_started`∨`debrief_created` | 28 | 22.0% | 173 | 2.5 |
| Threads (Reflect) | `reflect_thread_opened` | 27 | 21.3% | 136 | 2.0 |
| Reflect – rozpoczęte sesje | `reflect_session_started` | 25 | 19.7% | 57 | 1.0 |
| Powiadomienia otwarte (backend `moment.opened`) | `moment.opened` | 26 | 20.5% | 47 | 1.0 |
| Reflect – wysłane wiadomości | `reflect_message_sent` | 16 | 12.6% | 178 | 6.5 |
| Powiadomienia otwarte (klient) | `notification_opened` | 16 | 12.6% | 47 | 1.0 |
| Podsumowanie tygodniowe – obejrzane | `summary_viewed` + `period_type='weekly'` | 14 | 11.0% | 49 | 2.0 |
| Voice note | `recording_started` + `flow='voice_note'` | 9 | 7.1% | 54 | 4.0 |
| Nagrywanie sesji (session recording) | `recording_started` + `flow='session_recording'` | 7 | 5.5% | 11 | 1.0 |
| Podsumowanie miesięczne (audit) – obejrzane | `summary_viewed` + `period_type='monthly_audit'` | 5* | 3.9% | 16 | 2.0 |
| Rozmowa/czat (legacy `conversation_*`) | `conversation_started` | **0** | 0% | 0 | – |
| Habit Tracker | brak eventu | – | – | – | – |

`*` n<25, kierunkowo.

**Uwagi ważne dla interpretacji**:
- „Rozmowa/czat" w rozumieniu starego modelu `Conversation`/`Message` (`conversation_started/_message_sent/_ended`) jest **martwe od 2026-08-11** – zero zdarzeń w ostatnich 30 dniach mimo że event istnieje w katalogu. Żywym odpowiednikiem czatu jest Reflect (`reflect_session_started`/`reflect_message_sent`).
- **Habit Tracker (wdrożony 2026-09-02, MSV3.12) nie ma ŻADNEJ instrumentacji PostHog** – zero eventów zawierających „habit" w całej historii projektu, i nie pojawia się nawet jako osobny `$screen`, bo widget siedzi na `mainPage` a nie na dedykowanym ekranie. Adopcja tej funkcji jest dziś niemierzalna w PostHogu w ogóle – jeśli operator chce wiedzieć, czy ktokolwiek jej używa, jedyne źródło prawdy to tabela `habits`/`habit_logs` w Postgresie (przez `database-administrator`).
- „Your Session" nie ma jednego eventu wejścia – złożyłem proxy z 3 etapów (prep/nagranie/debrief). To zaniża realną liczbę, bo część osób mogła wejść na ekran flow bez odpalenia żadnego z tych trzech eventów (np. tylko obejrzeć, nie zacząć).
- **Statystyki/Timeline i Dashboard/Workspace to najsilniej używane funkcje po nawigacji podstawowej** – wyżej niż Reflect, Threads czy nagrywanie. To ważny, pozytywny sygnał: ludzie wracają głównie po to, żeby zobaczyć swoją historię/pulpit, nie żeby aktywnie „robić" coś nowego.

---

## 8. Częstotliwość: liczba aktywnych dni na użytkownika (30d, n=127)

| aktywne dni | użytkownicy | % |
|---|---|---|
| 1 dzień | 87 | 68.5% |
| 2-3 dni | 24 | 18.9% |
| 4-7 dni | 11 | 8.7% |
| 8-15 dni | 2* | 1.6% |
| 16+ dni | 3* | 2.4% |

`*` n<25, kierunkowo (i tu dosłownie liczone w pojedynczych osobach).

**68.5% z 127 aktywnych w 30 dniach użytkowników ma tylko JEDEN aktywny dzień w całym miesiącu.** To spójne z one-and-done 66.2% w oknie 90-dniowym (pkt 5) – ten sam obraz, dwa niezależne okna czasowe.

---

## 9. PAYWALL I MONETYZACJA

### WIELKIMI LITERAMI: instrumentacja paywalla jest SZCZĄTKOWA

- `paywall_shown` **istnieje dopiero od 2026-08-16** (23 dni przed końcem okna) i w całej swojej historii ma **10 zdarzeń / 7 użytkowników** – identycznie w oknie 30-dniowym i 90-dniowym, bo to cała historia eventu.
- `trial_started` / `trial_ended` **NIE PŁYNĄ W OGÓLE** – zero zdarzeń w całym projekcie od początku ingestu (2026-04-22).
- To oznacza: **nie da się w PostHogu policzyć klasycznego lejka "zobaczył paywall → kupił"** poza garstką z ostatnich 4 tygodni, i nie da się w ogóle zmierzyć trial→paid.

### Lejek, jaki jest możliwy do policzenia (30 dni, distinct users)

| krok | event | użytkownicy |
|---|---|---|
| Zobaczył paywall | `paywall_shown` | 7* |
| ↳ z czego trigger `drawer_menu` | | 5 |
| ↳ z czego trigger `settings` | | 1 |
| ↳ z czego trigger `premium_gate_session_recording` | | 1 |
| ↳ z czego trigger `premium_gate_reflect_messages` | | 1 |
| Otworzył ekran subskrypcji | `subscription_screen_opened` | 15* |
| Wybrał produkt | `subscription_product_selected` | 7* |
| Rozpoczął zakup | `subscription_purchase_started` | 3* |
| Dokończył zakup | `subscription_purchase_completed` | 5* |
| Zakup nieudany | `subscription_purchase_failed` | 2* |

`*` wszystkie n<25 – to są rzeczywiste, bardzo małe liczby, nie zaokrąglenia.

**Ważna niespójność do zanotowania**: więcej osób trafia na `subscription_screen_opened` (15) niż widziało `paywall_shown` (7) – oznacza to, że **większość wejść na ekran subskrypcji NIE przechodzi przez zdarzenie „paywall_shown"** (np. wejście przez ustawienia/menu bez modalnego triggera). `paywall_shown` systematycznie zaniża realną liczbę odsłon oferty premium.

### To samo w oknie 90 dni (dla porównania – prawie cała historia `paywall_shown`)

| krok | użytkownicy |
|---|---|
| paywall_shown | 7 |
| subscription_screen_opened | 27 |
| subscription_product_selected | 19 |
| subscription_purchase_started | 10 |
| subscription_purchase_completed | 8 |
| one_time_purchase_completed | 1 |

**Zastrzeżenie krytyczne**: `subscription_purchase_completed` w PostHogu (5-8 osób) to **NIE jest prawda przychodowa**. Ten event bywa niekompletny (poprzednie audyty PostHog wykazały, że jest niedoszacowany względem realnych zakupów). Do policzenia faktycznych płacących, MRR i churnu subskrypcji – to zadanie dla `database-administrator` na tabeli `subscription_receipts` w produkcyjnym Postgresie, nie dla PostHoga.

---

## 10. Retencja vs funkcje – co robili w 1. tygodniu ci, co przeżyli, vs ci, co odpadli

Kohorta: osoby pierwszy raz widziane między 2026-07-05 a 2026-07-26 (n=102, wystarczający zapas czasu do sprawdzenia W2 do dziś). „Przeżył do W2+" = miał aktywność w tygodniu kalendarzowym 14 dni po tygodniu rejestracji.

| segment | n | onboarding ukończony w W0 | Reflect w W0 | nagranie w W0 | workspace w W0 | timeline w W0 | prep w W0 |
|---|---|---|---|---|---|---|---|
| Odpadli po W0 (nie wrócili do W2) | 97 | 19.6% | 10.3% | 0.0% | 0.0% | 23.7% | 4.1% |
| Przeżyli do W2+ | **n=5 – SUPRESJA (próg k-anonimowości <25)** | – | – | – | – | – | – |

**Twardy wynik tej kohorty**: tylko **5 z 102 (4.9%)** przetrwało do W2. To zgadza się z D30=0.8% z punktu 4 – różne metody liczenia, ten sam wniosek.

Ze względu na regułę k-anonimowości (próg 25 użytkowników) **nie pokazuję rozbicia zachowań dla 5-osobowego segmentu przeżywających** – przy tak małej próbie procenty byłyby złudnie precyzyjne i w praktyce opisywałyby zachowania możliwych do zidentyfikowania pojedynczych osób. Segment odpadających (n=97) jest wystarczająco duży, żeby go pokazać: nawet wśród tych, co odpadli, prawie jedna czwarta (23.7%) obejrzała timeline w pierwszym tygodniu, a jedna piąta (19.6%) ukończyła onboarding – żadna z tych akcji sama w sobie nie chroni przed odejściem.

**Zalecenie do `growth-analyst`**: żeby dostać wiarygodny (>=25 osób) obraz „co robią ci, którzy zostają", trzeba rozszerzyć okno kohortowe (więcej tygodni historii) i powtórzyć to zapytanie – przy obecnym tempie przetrwania (~5%) potrzeba kohorty rzędu 500+ nowych użytkowników, żeby mieć 25 przeżywających.

---

## 11. Błędy i tarcie (30d)

### Top zdarzenia błędowe

| event | zdarzenia | użytkownicy |
|---|---|---|
| api_error | 4639 | 82 |
| $exception | 309 | 32 |
| client_error | 148 | 11 |
| debrief_failed | 12 | 3 |
| voice_transcription_failed | 11 | 2 |
| recording_processing_failed | 11 | 3 |
| password_reset_failed | 9 | 3 |
| onboarding_symptom_sync_failed | 9 | 2 |
| recording_chunk_upload_failed | 8 | 2 |
| subscription_purchase_failed | 3 | 2 |

**82 z 127 aktywnych użytkowników (64.6%) trafiło na co najmniej jeden `api_error` w 30 dni.** Koncentracja: jedna osoba wygenerowała 1083 z 4639 zdarzeń (23.3%) – warto to sprawdzić, ale nie tłumaczy większości wolumenu (pozostałe 76.7% rozłożone na 81 osób).

### Rozbicie `api_error` po endpointzie (top, 30d)

| endpoint | status | is_expected | zdarzenia | użytkownicy |
|---|---|---|---|---|
| /prep-cards/latest | 404 | True | 2120 | 58 |
| /debriefs/latest | 404 | True | 1364 | 51 |
| /health-check/latest | 404 | True | 835 | 47 |
| /users/get_user_profile_and_subscript… | 404 | **False** | 65 | **38** |
| /users/therapy-context | 404 | **False** | 50 | **40** |
| /moments/{moment_id}/dismissed | 404 | **False** | 23 | **16** |
| /between-sessions/latest | 404 | True | 18 | 10 |
| /users/preferences | 422 | **False** | 17 | 3 |
| /users/preferences | 404 | **False** | 14 | 2 |
| /dashboard/calltoaction | 400 | **False** | 8 | 1 |
| /session-recordings/upload/initiate | 403 | True | 76 | 1 (pojedyncze konto, zapętlone próby) |

**Odczyt**: ~4319 z 4639 zdarzeń `api_error` (93%) ma `is_expected=True` – to są zaprojektowane 404 dla „brak jeszcze danych" (pusty stan `/latest` dla prep-cards/debriefs/health-check), nie awarie. To NIE jest sygnał jakości, tylko szum instrumentacyjny wart wyciszenia u źródła.

**Ale**: `is_expected=False` na `/users/get_user_profile_and_subscript…` (38 użytkowników) i `/users/therapy-context` (40 użytkowników) to razem prawie **1/3 z 127 aktywnych użytkowników trafiająca na nieoczekiwany 404 na jednym z dwóch kluczowych endpointów profilu/kontekstu terapii w ciągu miesiąca**. To wygląda jak realny problem, nie szum – warto przekazać do `backend-api` do zbadania (poza zakresem tego zadania ekstrakcji).

---

## 12. Powiadomienia: wysłane vs otwarte

### Backend (moment.*, `posthog-python`) – główny mechanizm powrotu

| metryka | wartość |
|---|---|
| Wysłane (`moment.sent`) – zdarzenia | 24 473 |
| Wysłane – unikalni odbiorcy | **1815** |
| Otwarte (`moment.opened`) – zdarzenia | 47 |
| Otwarte – unikalni użytkownicy | **26** |
| **Open rate (odbiorcy, którzy choć raz otworzyli / wszyscy odbiorcy)** | **26 / 1815 = 1.4%** |
| Open rate (zdarzenie-do-zdarzenia) | 47 / 24 473 = 0.19% |

### Klient (Flutter) – sygnał lokalny, mniejsza próbka

| metryka | wartość |
|---|---|
| `notification_received` (dostarczone gdy appka w foreground) – zdarzenia/użytkownicy | 18 / 5* |
| `notification_opened` – zdarzenia/użytkownicy | 47 / 16* |

`*` n<25, kierunkowo, ale rząd wielkości zgadza się z `moment.opened` (26 użytkowników) – dwa niezależne pomiary tego samego zjawiska.

### Rozbicie wysyłki wg typu (30d) – tylko `sent`, bo `moment.opened` NIE niesie property `moment_type` (100% wartości null) i nie da się przypisać otwarć do konkretnego typu

| typ | wysłane | odbiorcy |
|---|---|---|
| WEEKLY_SUMMARY_READY | 6628 | 1799 |
| ADD_THERAPY_DATE | 4882 | 1717 |
| REFLECTION_INVITATION | 4756 | 1752 |
| THERAPY_RELATIONSHIP_CHECKIN | 4756 | 1738 |
| MONTHLY_SUMMARY_READY | 3323 | 1799 |
| pozostałe 13 typów łącznie (RE_ENGAGEMENT, MOOD_UPDATE_REQUEST, THERAPY_APPOINTMENT, THERAPY_PREP, post_session_reflection, RECORD_SESSION, GOALS_WEEKLY, POST_SESSION_REFLECTION, DAILY_CHECK_IN, HOMEWORK_REMINDER, BETWEEN_SESSIONS_NOTE, ACCOUNT_SETUP_NUDGE, MOOD_DIP_ALERT) | 128 | każdy typ ma <25 odbiorców – niepokazywane per-typ (próg k-anonimowości), zagregowane |

**To jest prawdopodobnie najważniejsze pojedyncze znalezisko w całym raporcie**: 5 głównych typów powiadomień jest wysyłanych do **1700-1830 odbiorców każdy** – czyli praktycznie do całej historycznej bazy kont, które kiedykolwiek dotknęły backendu, NIE tylko do 127 osób realnie aktywnych w appce w danym miesiącu. Mimo tej ogromnej skali wysyłki (prawie 8 powiadomień/miesiąc/odbiorcę tylko z top 5 typów), otwiera je **1.4% odbiorców**. Główny zaprojektowany mechanizm powrotu do appki nie działa w praktyce – i jednocześnie potwierdza to, że baza „dotknięta" przez backend (1815-1874) jest ok. 14x większa niż baza realnie aktywna (127), co samo w sobie jest twardym dowodem na skalę odpływu, o którym mówi punkt 4 (D30=0.8%).

---

## Zastrzeżenia (caveats) – przeczytać przed użyciem tych liczb w raporcie biznesowym

1. **Ingest zaczął się 2026-04-22.** Żadne dane sprzed tej daty nie istnieją; kohorty i okna retencyjne sięgające tak daleko wstecz są przycinane przez początek zbierania danych.
2. **Populacja „dotknięta przez backend" (1815-1874) to NIE jest to samo co „aktywni użytkownicy".** Zdarzenia `moment.*`, `weekly_summary_generated`, `monthly_audit_generated` są generowane przez crony dla praktycznie całej zarejestrowanej bazy, niezależnie od tego, czy dana osoba otworzyła appkę w danym miesiącu. Traktowanie tych liczb jako „aktywnych użytkowników" byłoby błędem – prawdziwa aktywna baza (otwiera appkę) to 127/miesiąc.
3. **k-anonimowość**: każdy segment poniżej 25 użytkowników jest oznaczony `*` i/lub opisany jako „kierunkowy"; jeden segment (5-osobowa grupa „przeżyła do W2+" w punkcie 10) został w pełni supresowany zgodnie z twardą regułą progu 25 – nie pokazuję rozbicia zachowań dla tej grupy.
4. **`paywall_shown` istnieje dopiero od 2026-08-16** – porównania 30d vs 90d dla tego eventu są tożsame, bo to cała jego historia. Nie ekstrapoluj trendu z 10 zdarzeń.
5. **`subscription_purchase_completed` z PostHoga nie jest prawdą przychodową.** Do MRR/liczby płacących/churnu subskrypcji użyj `subscription_receipts` w Postgresie przez `database-administrator`.
6. **Habit Tracker nie ma żadnej instrumentacji analitycznej** – to nie znaczy, że nikt go nie używa, tylko że PostHog nie może na to pytanie odpowiedzieć. Backend Postgres (`database-administrator`) to jedyne źródło prawdy dla adopcji tej funkcji.
7. **„Rozmowa/czat" (`conversation_*`) jest martwe od 2026-08-11** – jeśli to nadal aktywna ścieżka produktowa (a nie zastąpiona przez Reflect), to sam brak zdarzeń w PostHogu jest sygnałem do sprawdzenia z `flutter-mobile`/`backend-api`, czy instrumentacja nie została przypadkiem urwana przy jakimś refaktorze, zamiast świadomie wycofana.
8. **`trial_started`/`trial_ended` nigdy nie płynęły** – jeśli model biznesowy zakłada okres próbny, ta ścieżka jest całkowicie niewidoczna w PostHogu; ewentualne dane o trialach trzeba szukać w Postgresie (`database-administrator`) po polu `granted_via`/analogicznym w tabeli subskrypcji.
9. **`moment.opened` nie niesie property `moment_type`** – nie da się w PostHogu odpowiedzieć „który typ powiadomienia konwertuje najlepiej", tylko „ile w ogóle się otwiera".
10. **Skewy pojedynczych kont zgłoszone wprost, nie ukryte**: `recording_upload_completed` (105 zdarzeń/1 osoba), `/session-recordings/upload/initiate` 403 (76 zdarzeń/1 osoba, prawdopodobnie zapętlone retry), top1 udział w `api_error` (23.3% od jednej osoby).
11. Wszystkie liczby użytkowników liczone po `person_id`, nie po `distinct_id` ani po liczbie zdarzeń.

---

## Zapytania HogQL (verbatim)

Pełne pliki zapytań (do odtworzenia lub rozszerzenia) zapisane w trakcie sesji ekstrakcji:

```sql
-- Populacja / filtr botów, weryfikacja $lib
SELECT
  count(DISTINCT if(properties.$lib = 'posthog-flutter', person_id, NULL)) AS client_app_users,
  count(DISTINCT if(properties.$lib = 'posthog-python', person_id, NULL)) AS backend_touched_users,
  count(DISTINCT if(properties.$lib = 'web', person_id, NULL)) AS web_users,
  count(DISTINCT person_id) AS all_users
FROM events WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')

-- Inwentarz eventów 30d (pkt 1)
SELECT event, count() AS events_30d, count(DISTINCT person_id) AS users_30d
FROM events
WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
GROUP BY event ORDER BY events_30d DESC LIMIT 150

-- DAU / WAU / MAU + os/app_version (pkt 2) -- filtr app powtórzony w każdym zapytaniu:
--   properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true
--   AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
SELECT toDate(timestamp) AS day, count(DISTINCT person_id) AS dau
FROM events WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
  AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
  AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
GROUP BY day ORDER BY day

SELECT os, count() AS users FROM (
  SELECT person_id, any(properties.$os) AS os
  FROM events WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
    AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
    AND properties.$os != '' AND properties.$os IS NOT NULL
  GROUP BY person_id
) GROUP BY os ORDER BY users DESC

-- Nowi użytkownicy tydzień po tygodniu + powrót (pkt 3)
WITH first_seen AS (
  SELECT person_id, toStartOfWeek(min(timestamp)) AS cohort_week
  FROM events WHERE properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true
    AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  GROUP BY person_id
),
activity AS (
  SELECT DISTINCT person_id, toStartOfWeek(timestamp) AS active_week
  FROM events WHERE properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true
    AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
)
SELECT f.cohort_week AS cohort_week, count(DISTINCT f.person_id) AS new_users,
  count(DISTINCT if(a.active_week = f.cohort_week + INTERVAL 7 DAY, a.person_id, NULL)) AS returned_next_week
FROM first_seen f LEFT JOIN activity a ON a.person_id = f.person_id
WHERE f.cohort_week >= toStartOfWeek(toDateTime('2026-06-15'))
GROUP BY f.cohort_week ORDER BY f.cohort_week

-- Retencja tygodniowa W0-W4 (pkt 4a) -- ten sam wzorzec first_seen/activity, dodatkowo:
SELECT f.cohort_week, count(DISTINCT f.person_id) AS cohort_size,
  count(DISTINCT if(a.active_week = f.cohort_week, a.person_id, NULL)) AS w0,
  count(DISTINCT if(a.active_week = f.cohort_week + INTERVAL 7 DAY, a.person_id, NULL)) AS w1,
  count(DISTINCT if(a.active_week = f.cohort_week + INTERVAL 14 DAY, a.person_id, NULL)) AS w2,
  count(DISTINCT if(a.active_week = f.cohort_week + INTERVAL 21 DAY, a.person_id, NULL)) AS w3,
  count(DISTINCT if(a.active_week = f.cohort_week + INTERVAL 28 DAY, a.person_id, NULL)) AS w4
FROM first_seen f LEFT JOIN activity a ON a.person_id = f.person_id
WHERE f.cohort_week >= toStartOfWeek(toDateTime('2026-07-18'))
GROUP BY f.cohort_week ORDER BY f.cohort_week

-- D1/D7/D30 (pkt 4b) -- wzorzec dla D30, analogicznie D1 (+1 DAY, cutoff < 09-11) i D7 (+7 DAY, cutoff < 09-05):
WITH first_seen AS (
  SELECT person_id, toDate(min(timestamp)) AS cohort_day, min(timestamp) AS first_ts
  FROM events WHERE properties.$lib='posthog-flutter' AND properties.$is_testflight!=true
    AND properties.$is_emulator!=true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  GROUP BY person_id
  HAVING first_ts >= toDateTime('2026-06-14') AND first_ts < toDateTime('2026-08-13')
),
activity AS (
  SELECT DISTINCT person_id, toDate(timestamp) AS active_day
  FROM events WHERE properties.$lib='posthog-flutter' AND properties.$is_testflight!=true
    AND properties.$is_emulator!=true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
)
SELECT count(DISTINCT f.person_id) AS cohort_size_eligible,
  count(DISTINCT if(a.active_day = f.cohort_day + INTERVAL 30 DAY, a.person_id, NULL)) AS d30_retained
FROM first_seen f LEFT JOIN activity a ON a.person_id = f.person_id

-- One-and-done 90d (pkt 5)
SELECT countIf(active_days=1) AS one_and_done_users, count() AS total_users_90d,
  round(100.0*countIf(active_days=1)/count(),1) AS pct_one_and_done
FROM (
  SELECT person_id, count(DISTINCT toDate(timestamp)) AS active_days
  FROM events WHERE timestamp >= toDateTime('2026-06-14') AND timestamp < toDateTime('2026-09-13')
    AND properties.$lib='posthog-flutter' AND properties.$is_testflight!=true AND properties.$is_emulator!=true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  GROUP BY person_id
)

-- Onboarding per krok/os (pkt 6)
SELECT properties.step_name AS step, properties.$os AS os,
  count(DISTINCT if(event='onboarding_step_viewed', person_id, NULL)) AS viewed_users,
  count(DISTINCT if(event='onboarding_step_completed', person_id, NULL)) AS completed_users
FROM events WHERE event IN ('onboarding_step_viewed','onboarding_step_completed')
  AND timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
  AND properties.$lib='posthog-flutter'
GROUP BY step, os ORDER BY step, os

-- Adopcja funkcji (pkt 7) -- wzorzec UNION ALL, jedna gałąź na funkcję, np.:
SELECT 'reflect_wiadomosci_wyslane' AS feature, count() AS users, sum(cnt) AS events, median(cnt) AS median_per_user FROM (
  SELECT person_id, count() AS cnt FROM events WHERE event='reflect_message_sent'
    AND timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13') GROUP BY person_id)
-- (11 dalszych gałęzi UNION ALL analogicznie dla pozostałych funkcji z tabeli w pkt 7)

-- Częstotliwość aktywnych dni (pkt 8)
SELECT countIf(active_days=1) AS d1, countIf(active_days BETWEEN 2 AND 3) AS d2_3,
  countIf(active_days BETWEEN 4 AND 7) AS d4_7, countIf(active_days BETWEEN 8 AND 15) AS d8_15,
  countIf(active_days >= 16) AS d16_plus, count() AS total
FROM (
  SELECT person_id, count(DISTINCT toDate(timestamp)) AS active_days
  FROM events WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
    AND properties.$lib='posthog-flutter' AND properties.$is_testflight!=true AND properties.$is_emulator!=true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  GROUP BY person_id
)

-- Lejek paywalla (pkt 9)
SELECT
  count(DISTINCT if(event='paywall_shown', person_id, NULL)) AS paywall_shown_users,
  count(DISTINCT if(event='subscription_screen_opened', person_id, NULL)) AS sub_screen_users,
  count(DISTINCT if(event='subscription_product_selected', person_id, NULL)) AS product_selected_users,
  count(DISTINCT if(event='subscription_purchase_started', person_id, NULL)) AS purchase_started_users,
  count(DISTINCT if(event='subscription_purchase_completed', person_id, NULL)) AS purchase_completed_users,
  count(DISTINCT if(event='subscription_purchase_failed', person_id, NULL)) AS purchase_failed_users
FROM events WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
  AND event IN ('paywall_shown','subscription_screen_opened','subscription_product_selected',
                'subscription_purchase_started','subscription_purchase_completed','subscription_purchase_failed')

-- Retencja vs funkcje (pkt 10) -- CTE first_seen/cohort/activity/status jak wyżej, dodatkowo:
w0_flags AS (
  SELECT s.person_id AS person_id, s.survived_w2 AS survived_w2,
    countIf(e.event='onboarding_completed')>0 AS did_onboarding,
    countIf(e.event IN ('reflect_message_sent','reflect_session_started'))>0 AS did_reflect,
    countIf(e.event='recording_started')>0 AS did_recording,
    countIf(e.event='workspace_opened')>0 AS did_workspace,
    countIf(e.event='timeline_viewed')>0 AS did_timeline,
    countIf(e.event IN ('prep_capture_started','prep_card_started'))>0 AS did_prep
  FROM status s JOIN cohort c ON c.person_id = s.person_id JOIN events e ON e.person_id = s.person_id
  WHERE e.timestamp >= c.cohort_week AND e.timestamp < c.cohort_week + INTERVAL 7 DAY
  GROUP BY s.person_id, s.survived_w2
)
SELECT survived_w2, count() AS n, round(100.0*sum(did_onboarding)/count(),1) AS pct_onboarding, ...
FROM w0_flags GROUP BY survived_w2

-- Błędy top 10 + rozbicie api_error (pkt 11)
SELECT event, count() AS events, count(DISTINCT person_id) AS users
FROM events WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
  AND event IN ('api_error','client_error','$exception','recording_upload_failed','recording_chunk_upload_failed',
                'recording_processing_failed','voice_transcription_failed','subscription_purchase_failed',
                'subscription_verification_failed','debrief_failed','signup_failed','password_reset_failed',
                'onboarding_symptom_sync_failed')
GROUP BY event ORDER BY events DESC LIMIT 10

SELECT properties.endpoint AS endpoint, properties.status_code AS status_code, properties.is_expected AS is_expected,
  count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event='api_error' AND timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
GROUP BY endpoint, status_code, is_expected ORDER BY c DESC LIMIT 15

-- Powiadomienia sent vs opened (pkt 12)
SELECT
  countIf(event='moment.sent') AS backend_sent_events,
  count(DISTINCT if(event='moment.sent', person_id, NULL)) AS backend_sent_recipients,
  countIf(event='moment.opened') AS backend_opened_events,
  count(DISTINCT if(event='moment.opened', person_id, NULL)) AS backend_opened_users
FROM events WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
  AND event IN ('moment.sent','moment.opened')

SELECT properties.moment_type AS moment_type,
  countIf(event='moment.sent') AS sent, count(DISTINCT if(event='moment.sent', person_id, NULL)) AS sent_users,
  countIf(event='moment.opened') AS opened, count(DISTINCT if(event='moment.opened', person_id, NULL)) AS opened_users
FROM events WHERE timestamp >= toDateTime('2026-08-13') AND timestamp < toDateTime('2026-09-13')
  AND event IN ('moment.sent','moment.opened') GROUP BY moment_type ORDER BY sent DESC
```
