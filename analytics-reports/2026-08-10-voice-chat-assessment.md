# Czat głosowy (realtime voice chat) – czy wart dalszej inwestycji? Raport decyzyjny (B7)

- **Data**: 2026-08-10
- **Analityk**: growth-analyst
- **Pytanie biznesowe**: Czy realtime voice chat zasługuje na dalsze pieniądze (migracja gpt-realtime-mini → Gemini Live, dalsze prace STT), czy należy go utrzymać bez inwestycji albo wygasić?
- **Okno danych**: pełna historia PostHog 2026-04-22 → 2026-08-10; `token_usage_log` 2026-04-01 → 2026-08-10
- **Źródła**: PostHog (proj. 141170 EU, `analytics-reports/raw/2026-08-10-voice-chat-b7.md`) · Postgres prod (`token_usage_log`, `model_pricing`, `user_subscription`, `subscription_receipts` – `db-reports/2026-08-10-voice-ai-cost.md`, `db-reports/2026-08-10-subscription-pipeline-check.md`) · recon kodu (Flutter + FastAPI) · benchmarki cenowe OpenAI Realtime
- **Pewność**: **Wysoka co do rekomendacji, niska co do samych liczb użycia.** Liczby użycia są mikroskopijne (11 osób w cyklu życia), ale wniosek nie zależy od ich precyzji: cztery niezależne dowody z kodu i z bazy wskazują ten sam kierunek.

---

## Executive summary

1. **Odpowiedź: UTRZYMAĆ BEZ INWESTYCJI, z twardą bramką decyzyjną za 4 tygodnie.** Ani „wypromować", ani „wygasić" – bo popytu na tę funkcję **nigdy nie zmierzyliśmy**, a wygaszanie niesprawdzonej funkcji to zgadywanie tak samo jak jej promowanie.
2. **Migracja na Gemini Live jest bezwzględnie nieopłacalna i należy ją wstrzymać.** Szacowany **cały** rachunek za realtime audio to **ok. 10–80 USD przez 4 miesiące** (rzędu 3–20 USD/mies.). Nawet 70% oszczędności daje 25–170 USD rocznie, przy koszcie migracji liczonym w dniach pracy na dwóch platformach. Optymalizujemy koszt jednostkowy funkcji, której **prawie nikt nie używa**.
3. **Root cause niskiego użycia to NIE odkrywalność – to bramka premium.** `reflect_tab_screen.dart:619` blokuje mikrofon dla nie-premium snackbarem. Przy **16 realnie aktywnych subskrypcjach premium** w bazie, „1 osoba na ekranie audioChat" jest dokładnie tym, czego należało oczekiwać. Ocenianie tej funkcji na mianowniku wszystkich użytkowników było błędem metodologicznym.
4. **Funkcja jest sierotą produktową**: zablokowana za premium, ale **nie sprzedawana na paywallu** (nie ma jej w żadnym z 10 benefitów), wejście to nieopisana ikonka mikrofonu, a **uderzenie w bramkę nie emituje żadnego eventu** – więc popyt jest strukturalnie niewidoczny.
5. **Pieniądze na STT należy przekierować na notatki głosowe, nie na czat głosowy.** To dwie różne funkcje: dyktowanie (`voice_transcription_*`) jest darmowe, siedzi w przepływach debrief i health check, czyli na ścieżce aktywacji powiązanej z **3,41x retencją**. Ma jednak dopiero 5 dni danych – decyzję o AssemblyAI/Gemini podjąć po 4 tygodniach.

---

## Kluczowe metryki

| Metryka | Wartość | Odczyt |
|---|---|---|
| Użytkownicy voice chat, cały cykl życia (3,5 mies.) | **11 osób / 65 sesji** (n<25) | krytycznie nisko |
| W tym testerzy TestFlight | **4 z 11 (36%)** | ponad 1/3 to my sami |
| W tym kiedykolwiek płacący | **2 z 11** | brak monetyzacji |
| Ostatnia sesja voice chat | **2026-08-04** (0 przez ostatnie 6 dni) | możliwa regresja |
| Sesje kończące się poniżej 30 s | **20 z 51 (39%)** | brak dopasowania do potrzeby |
| Ranking ekranu `audioChat` (60 dni) | **18. z 22** ekranów, 4 os. | poniżej wszystkich flow |
| Realnie aktywne subskrypcje premium (baza) | **16** | prawdziwy mianownik funkcji |
| Użytkownicy, którzy kiedykolwiek mieli trial | 554 | 11/554 = **2,0% adopcji** |
| Zalogowany koszt realtime w `token_usage_log` | **0,00 USD, zawsze** | koszt jest niemierzony, nie zerowy |
| Szacowany realny koszt realtime, cykl życia | **ok. 10–80 USD** | szacunek, nie pomiar |
| Całkowity koszt AI, 30 dni | 117,30 USD | voice to ok. 2–15% |
| Koszt tekstu (gpt-5.4-mini), 60 dni | 144,50 USD / 276 os. = **0,52 USD/os.** | punkt odniesienia |

Benchmark cenowy: gpt-realtime-2.1 to 32 USD/1M tokenów audio wejściowych i 64 USD/1M wyjściowych; typowy agent kosztuje **0,06–0,11 USD/min** z cache'owaniem promptu, a 0,18–0,46 USD/min bez niego ([HackerNoon, pomiary z 4000 sesji](https://hackernoon.com/openai-realtime-api-pricing-in-2026-real-world-data-from-4000-measured-sessions), [layer3labs](https://www.layer3labs.io/guides/openai-realtime-api-pricing)).

---

## Ustalenia

### F1 – Czat głosowy jest zablokowany za premium, a premium ma 16 aktywnych subskrypcji · Wpływ: krytyczny · Pewność: wysoka

**Dowód (kod).** `mindsync-frontend/mindsync_app/lib/screens/reflect_tab/reflect_tab_screen.dart:616-640`:

```dart
void _handleMicTap(BuildContext context, ReflectChatActiveState state) async {
  if (_isMicLoading) return;
  if (!state.usage.isPremium) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text(S.of(context).chat_voicePremiumOnly),
      action: SnackBarAction(label: S.of(context).chat_upgrade, ...),
    ));
    return;   // <-- voice_chat_started nigdy nie poleci dla free
  }
```

**Dowód (baza).** `user_subscription`: `is_active=True` = 34 wiersze, ale `is_active AND end_date > now()` = **16**. Czyli realna baza premium to 16 osób (18 wierszy to wygasłe, ale wciąż oznaczone jako aktywne – osobny bug dla `backend-api`, patrz `db-reports/2026-08-10-subscription-pipeline-check.md`).

**Więc co z tego.** Dane wyjściowe zadania B7 („1 osoba na ekranie audioChat w top 20") porównywały funkcję premium do mianownika ok. 94 aktywnych użytkowników aplikacji na 14 dni. Prawidłowy mianownik to 16 aktywnych premium (albo 554 osoby, które kiedykolwiek miały trial). **11 użytkowników w cyklu życia wobec 554 osób z trialem to 2,0% adopcji** – nadal bardzo mało, ale to zupełnie inna liczba i inna diagnoza niż „nikt tam nie trafia".

### F2 – Popyt na głos jest strukturalnie niemierzalny · Wpływ: krytyczny · Pewność: wysoka

Trzy niezależne luki sprawiają, że **nie wiemy, ilu ludzi chce głosu**:

1. **Uderzenie w bramkę nie emituje eventu.** Ścieżka nie-premium pokazuje snackbar i robi `return` – zero telemetrii. Nie wiemy, ilu ludzi dotyka mikrofonu.
2. **`subscription_screen_opened` nie niesie własności `trigger_feature`** – potwierdzone przez pełne wyliczenie kluczy na 220 eventach historii. Nawet gdy ktoś kliknie „Upgrade" w snackbarze, nie da się tego przypisać do głosu.
3. **`paywall_shown` nigdy nie odpalił** w całej historii projektu; `paywall_dismissed` istnieje dopiero od 2026-08-07 (5 eventów).

**Więc co z tego.** Nie da się dziś odróżnić „nikt nie chce głosu" od „setki ludzi uderzają w bramkę i odbijają się". To jest **jedyna liczba, która realnie rozstrzyga B7**, i kosztuje kilka godzin pracy klienta, a nie migrację silnika.

### F3 – Funkcja jest zablokowana za premium, ale nie jest sprzedawana jako premium · Wpływ: wysoki · Pewność: wysoka

Lista benefitów na paywallu (`lib/l10n/app_en.arb`) to: nielimitowane notatki AI, podsumowania tygodniowe/miesięczne/roczne, snapshoty 30/90 dni, insighty terapeutyczne, narracje celów, rekomendacje relacji terapeutycznej, eksport danych, nielimitowane wiadomości Reflect, nielimitowane debriefy, nielimitowane nagrania. **Tryb głosowy nie występuje w żadnym z tych 10 punktów.**

Do tego `settings_cubit.dart:135 changeSelectedVoice()` **nie ma żadnego sprawdzenia premium** – darmowy użytkownik może wybrać sobie głos w Ustawieniach, którego nigdy nie usłyszy. Stąd `voice_agent_changed`: 25 eventów / **13 osób** w cyklu życia, czyli **więcej osób konfiguruje głos niż go kiedykolwiek użyło (11)**.

**Więc co z tego.** Płacimy koszt utrzymania funkcji premium, nie zbierając za nią ani złotówki wartości postrzeganej. To najgorszy możliwy układ: koszt bramki bez korzyści z bramki. Jeżeli głos ma zostać, powinien albo trafić na listę benefitów, albo bramka powinna zniknąć.

### F4 – Koszt realtime jest architektonicznie niemierzalny (a nie zerowy) · Wpływ: wysoki · Pewność: wysoka

**Dowód (kod).** `MindSync/app/services/openai_audio_service.py:380-394` zapisuje wiersz z `prompt_tokens=0, completion_tokens=0, total_tokens=0, is_estimate=True`, z komentarzem: *„per-turn tokens are logged by the client after the session ends"*. **Grep całego klienta Flutter nie znajduje żadnego takiego wywołania** – ten mechanizm nie istnieje. Połączenie WebRTC idzie bezpośrednio klient → `api.openai.com/v1/realtime/calls` na kluczu efemerycznym, więc tokeny audio nigdy nie dotykają naszego backendu.

**Dowód (baza).** Modele realtime: 114 wierszy w całej historii (`gpt-realtime-1.5` 52, `gpt-realtime-2` 61, `gpt-realtime-mini` 1). **Każdy** ma `total_tokens=0`, `cost_usd=0` i `user_id=NULL` – 100%, bez wyjątku.

**Dodatkowy błąd atrybucji (nowy, nie był znany).** Etykieta `feature='REALTIME_VOICE'` w `token_usage_log` **zawyża głos**: `voice_director.run_pipeline` jest wołany zarówno z `POST /{id}/audio/user_message_add` (głos), jak i z `POST /{id}/message` (**tekstowy** Reflect) – `app/api/v1/endpoints/reflect.py:525` i `:954`. Dlatego 60-dniowy wycinek pokazuje `REALTIME_VOICE` = 684 wiersze / 28 osób, mimo że voice chat miał w tym czasie 1–2 użytkowników. Prawdziwy zmierzalny koszt czatu głosowego jest jeszcze niższy niż raportowane 0,000376 USD.

### F5 – Szacunek realnego kosztu: dziesiątki dolarów przez 4 miesiące · Wpływ: rozstrzygający dla migracji · Pewność: średnia (szacunek)

Skoro pomiaru nie ma, budujemy szacunek z **czasu trwania sesji**, który mamy (`voice_chat_ended.duration_seconds`, 100% pokrycia, 51 eventów):

| Kubełek | Sesje | Środek | Minuty |
|---|---:|---:|---:|
| <30 s | 20 | 15 s | 5,0 |
| 30 s – 2 min | 14 | 75 s | 17,5 |
| 2 – 5 min | 5 | 3,5 min | 17,5 |
| >5 min | 12 | ok. 8 min (zał.) | 96,0 |
| **Razem (51 zakończonych)** | | | **ok. 136 min** |

Startów było 65, a zakończeń 51, więc 14 sesji nie ma zmierzonego czasu. Skalując: **ok. 140–175 minut w całym cyklu życia** (2,3–2,9 godziny przez 3,5 miesiąca).

| Scenariusz cenowy | Stawka | Koszt całego cyklu życia |
|---|---:|---:|
| Z cache'owaniem promptu (typowy) | 0,06–0,11 USD/min | **8–19 USD** |
| Bez cache'owania (pesymistyczny) | 0,18–0,46 USD/min | **25–80 USD** |

Kontrola oddolna: przy ciągłym strumieniu wejściowym 600 tok./min × 32 USD/1M oraz mniej więcej 40% czasu mówienia asystenta 1200 tok./min × 64 USD/1M wychodzi ok. 0,05 USD/min – ten sam rząd wielkości co benchmark, więc szacunek jest wiarygodny co do skali.

**Więc co z tego.** Koszt na aktywnego użytkownika głosu to **ok. 1–7 USD w całym cyklu życia** (10–80 USD / 11 osób) wobec 0,52 USD na użytkownika tekstu na 60 dni. Jednostkowo głos jest 2–13x droższy, ale **kwota bezwzględna jest trywialna, bo nikt tego nie używa**. To jest liczba, której brakowało do decyzji o migracji.

### F6 – Możliwa regresja punktu wejścia w najnowszym buildzie · Wpływ: średni · Pewność: niska (wymaga sprawdzenia)

`voice_chat_started` **nigdy nie odpalił na buildzie 2.0.76**, mimo że ma on 31 aktywnych użytkowników w 30 dni. Ostatnia sesja w ogóle: 2026-08-04 na 2.0.75. Sześć dni ciszy.

Przy takich wolumenach 6 dni ciszy mieści się w szumie losowym (funkcja miała już zerowe tygodnie: 06-14, 07-26). **Nie twierdzę, że to regresja** – twierdzę, że jest nierozstrzygnięte, a rozstrzygnięcie kosztuje 30 minut i musi poprzedzać każdą inną decyzję. Sekwencja przed emisją eventu ma cztery punkty awarii: bramka premium → `ConnectivityService` → `getSessionData()` (wywołanie backendu) → uprawnienie do mikrofonu → dopiero wtedy `voice_chat_started`.

### F7 – Notatki głosowe to inna funkcja i to one mają uzasadnienie biznesowe · Wpływ: wysoki · Pewność: średnia

`voice_transcription_started/completed` emitują `debrief_capture_cubit.dart:715` i `health_check_flow_cubit.dart:342`, czyli **przepływy przechwytywania pętli terapeutycznej**. Nie mają żadnej bramki premium (grep: zero `isPremium` w tych plikach). Raport `analytics-reports/2026-08-10-activation-definition.md` wykazał, że pierwsze przechwycenie w 24 h wiąże się z **3,41x wyższą retencją**.

Ale: te eventy istnieją dopiero od **2026-08-05** (8 eventów / 3 osoby, 5 dni danych). `voice_transcription_failed` nie odpalił nigdy.

**Więc co z tego.** Pytanie „czy inwestować w STT" i pytanie „czy inwestować w realtime voice chat" to **dwa różne pytania**, które zadanie B7 sklejało w jedno. Dyktowanie leży na ścieżce aktywacji i jest darmowe dla wszystkich; czat głosowy leży na bocznej ścieżce za bramką. Jeżeli gdziekolwiek wydawać pieniądze na głos, to na dyktowanie – ale dopiero po 4 tygodniach danych.

---

## Analiza przyczyn i hipotezy

- **H1 (ODRZUCONA): „Problem to odkrywalność – nikt nie trafia na ekran audioChat".** Za: `audioChat` jest 18. z 22 ekranów, 4 osoby w 60 dni. Przeciw: ikona mikrofonu stoi **na stałe w kompozytorze wiadomości Reflect** (`reflect_chat_input.dart:171-196`), czyli w najbardziej widocznym możliwym miejscu, bez kłódki i bez ukrycia w menu. 64 z 74 wejść przyszło z `mainPage`, czyli z powłoki zakładek – ludzie ją widzą. **Werdykt: to nie odkrywalność, to bramka premium (F1) i brak sprzedaży funkcji (F3).** Pewność wysoka.
- **H2 (POTWIERDZONA): „Funkcja jest zablokowana dla praktycznie całej bazy".** Za: twardy `return` dla nie-premium; 16 aktywnych subskrypcji; 2 z 11 użytkowników głosu kiedykolwiek zapłaciło; 4 z 11 to testerzy TestFlight. Przeciw: brak. Pewność wysoka.
- **H3 (POTWIERDZONA): „Koszt realtime nie uzasadnia migracji".** Za: szacunek 10–80 USD za cały cykl życia, wobec 117,30 USD miesięcznego całkowitego kosztu AI, z którego 93% to `SYSTEM` (zadania w tle). Przeciw: szacunek obarczony niepewnością kubełka >5 min – ale nawet 5x wyższy koszt nie zmienia wniosku. Pewność wysoka co do decyzji, średnia co do liczby.
- **H4 (NIEROZSTRZYGNIĘTA): „Punkt wejścia zepsuł się w 2.0.76".** Za: zero eventów przy 31 użytkownikach buildu; 6 dni ciszy. Przeciw: funkcja miała już wcześniej zerowe tygodnie przy tak małych wolumenach. **Wymaga sprawdzenia kodu, nie kolejnych danych.** Pewność niska.
- **H5 (NIEROZSTRZYGALNA DZISIAJ): „Ludzie chcą głosu, ale odbijają się od bramki".** Nie do rozstrzygnięcia przy obecnej instrumentacji (F2). To jest dokładnie ta hipoteza, którą rekomendacja R2 ma przetestować.

**Czego świadomie NIE twierdzę.** Kohorta użytkowników głosu wygląda na bardziej zaangażowaną (n=6, powrót w dniach 8–28: 66,7% wobec 31,9%), ale **te liczby są suprymowane i nie wchodzą do wniosków**: n=6 to poniżej progu k-anonimowości, a selekcja jest odwrotna do przyczynowości – żeby w ogóle dotknąć funkcji premium, trzeba było już wcześniej być zaangażowanym i płacącym. **To nie jest dowód, że głos buduje retencję.**

---

## Rekomendacje (uszeregowane wg wpływ × pewność × wysiłek)

1. **NIE migrować na Gemini Live. Zamrozić wszystkie wydatki na silnik realtime do czasu R2.**
   Uzasadnienie: cały rachunek za realtime to 10–80 USD przez 4 miesiące; nawet 70% oszczędności to 25–170 USD rocznie wobec kilku dni pracy na dwóch platformach. **Oczekiwany efekt: uniknięcie 2–5 dni pracy inżynierskiej o ujemnym ROI.** Właściciel: decyzja operatora. Miara: brak zadania migracyjnego w backlogu.

2. **Zinstrumentować bramkę premium na głosie – to jedyna liczba, która rozstrzyga los funkcji.**
   Konkretnie: (a) emitować event przy pokazaniu snackbara w `_handleMicTap` dla nie-premium, np. `premium_gate_hit` z `{feature: 'reflect_voice'}`; (b) dodać `trigger_feature` do `subscription_screen_opened` (dziś nie niesie tej własności wcale). Właściciel: **`flutter-mobile`**. Wysiłek: godziny. **Oczekiwany efekt: po 4 tygodniach znamy liczbę osób miesięcznie dotykających mikrofonu – zamiana decyzji zgadywanej na policzoną.** Miara: `premium_gate_hit{feature=reflect_voice}` unikalne osoby / 4 tyg.

3. **Sprawdzić, czy punkt wejścia nie jest zepsuty w buildzie 2.0.76.**
   Ścieżka do prześledzenia: bramka premium → `ConnectivityService.hasConnection()` → `getSessionData()` → uprawnienie mikrofonu → `voice_chat_started`. Właściciel: **`flutter-mobile`**. Wysiłek: ok. 30 min. **Oczekiwany efekt: rozstrzygnięcie, czy 6 dni ciszy to szum czy regresja – bez tego R4 może wygasić działającą funkcję na podstawie zepsutego pomiaru.** Miara: ręczne przejście flow na 2.0.76 emituje `voice_chat_started`.

4. **Bramka decyzyjna 2026-09-10 (4 tygodnie po R2): wypromować albo wygasić, bez trzeciej opcji.**
   Proponowany próg: jeżeli **≥25 unikalnych osób/mies.** uderza w bramkę głosu → popyt istnieje, wtedy wypromować (dodać tryb głosowy na listę benefitów paywalla i przetestować odblokowanie go dla trialu). Jeżeli **<10 osób/mies.** → wygasić: usunąć ikonę mikrofonu, sekcję głosu z Ustawień, ekran `audioChat`, `AudioChatCubit`, `RealtimeAPIManager` i endpoint sesji efemerycznych. Między 10 a 25 – utrzymać bez zmian i zmierzyć ponownie za kwartał. Właściciel: decyzja operatora, wejście od **`ui-ux-designer`**. **Oczekiwany efekt: koniec płacenia kosztu utrzymania za funkcję bez werdyktu.**

5. **Naprawić błędną atrybucję `feature='REALTIME_VOICE'` w `voice_director.py`.**
   Dziś koszty dyrektora z **tekstowego** Reflect (`reflect.py:525`) lądują pod etykietą głosu, zawyżając ją. Rozdzielić na `REFLECT` (tekst) i `REALTIME_VOICE` (głos) wg wywołującego endpointu. Właściciel: **`data-analytics`**. Wysiłek: mały. **Oczekiwany efekt: `token_usage_log` przestaje kłamać o podziale kosztów między funkcjami – dotyczy każdej przyszłej analizy jednostkowej, nie tylko głosu.**

6. **Zdecydować o sekcji „Głos" w Ustawieniach dla nie-premium.**
   `changeSelectedVoice()` nie ma sprawdzenia premium – 13 osób skonfigurowało głos, 11 kiedykolwiek go użyło. Albo schować sekcję za premium, albo (lepiej, jeśli funkcja przeżyje R4) potraktować ją jako drugi punkt pomiaru popytu. Właściciel: **`ui-ux-designer`** → **`flutter-mobile`**. Wysiłek: mały.

7. **ŚWIADOMIE NIE ROBIĆ TERAZ: nie budować pomiaru kosztu realtime.**
   Naprawa raportowania tokenów realtime (webhook usage OpenAI + uzupełnienie `user_id` na wierszach `create_realtime_session`, które dziś jest NULL w 100% przypadków) to realna luka – ale **nie warto instrumentować kosztu funkcji, którą R4 może wygasić za 4 tygodnie**. Odłożyć do czasu, aż funkcja przejdzie bramkę. Jeżeli przejdzie – właściciel `backend-api` + `data-analytics`.

8. **Osobno i pilniej niż cały ten temat: `SYSTEM` to 93% kosztu AI (134,23 USD z 144,90 USD w 60 dni), bez atrybucji użytkownika.**
   Zadania w tle kosztują ok. 350x więcej niż wszystkie funkcje głosowe razem wzięte i nikt ich nie audytował. To znacznie większy temat oszczędnościowy niż wybór silnika głosu. Rekomendacja: osobne zadanie dla **`growth-analyst` + `data-analytics`**.

---

## Segmenty i kohorty

| Segment | n | Status |
|---|---:|---|
| Użytkownicy voice chat, cykl życia | 11 | n<25 – liczby podane jako surowe zliczenia, metryki pochodne suprymowane |
| Z tego testerzy TestFlight | 4 | n<25 – tylko zliczenie |
| Z tego kiedykolwiek płacący | 2 | n<25 – tylko zliczenie |
| Kohorta A (retencja użytkowników głosu) | 6 | **SUPRYMOWANA** – poniżej progu, nie wchodzi do wniosków |
| Kohorta B (Reflect bez głosu) | 47 | powyżej progu, ale bez kontrpartnera |
| Użytkownicy notatek głosowych | 3 | n<25 – 5 dni danych, za wcześnie na jakikolwiek odczyt |
| Aktywne subskrypcje premium | 16 | n<25 – podane jako mianownik, bez podziałów |

Rozkład częstotliwości użycia (11 osób): 2 osoby użyły raz, 1 osoba dwa razy, 2 osoby 3–5 razy, **6 osób 6+ razy**. Czyli wśród tych, którzy w ogóle weszli, większość wracała – ale przy 4 testerach w tej grupie i n=11 nie da się z tego zbudować argumentu o dopasowaniu produktu do potrzeby.

---

## Zastrzeżenia i pewność

- **Wszystko po stronie głosu jest małą próbą.** 11 osób w cyklu życia, 51 zmierzonych czasów trwania, kohorta retencji n=6. Żadna z tych liczb nie jest istotna statystycznie. Rekomendacja nie opiera się na nich – opiera się na dowodach z kodu (bramka premium, brak sprzedaży funkcji, brak pomiaru kosztu) i na rzędzie wielkości kosztu.
- **Koszt realtime to SZACUNEK, nie pomiar.** Nie mamy ani jednego rzeczywistego tokena audio w `token_usage_log`. Największa niepewność siedzi w kubełku >5 min (12 sesji bez górnego ograniczenia); przyjąłem 8 min. Gdyby to było 20 min, koszt cyklu życia rośnie do ok. 30–200 USD – **i wniosek o migracji nadal się nie zmienia**.
- **Korelacja to nie przyczynowość.** Wyższa retencja kohorty głosowej jest w całości wytłumaczalna selekcją (żeby dotknąć funkcji premium, trzeba było już płacić i być zaangażowanym). Nie użyłem tego jako argumentu za utrzymaniem funkcji.
- **Poprawka metodologiczna do brief u** (od `posthog-data-extractor`): `reflect_message_sent` i `reflect_session_started` są emitowane **serwerowo** (`$lib='posthog-python'`), więc instrukcja filtrowania wszystkiego przez `$lib='posthog-flutter'` zerowałaby je i dawała fałszywe „nie leci". Dla tych eventów użyto `$lib != 'web'`. Do zapisania w pamięci agenta.
- **Liczba płacących z PostHog (2 osoby) jest niewiarygodna** – prawda transakcyjna to `subscription_receipts` / `user_subscription` (16 aktywnych). Użyłem bazy jako mianownika.
- **Q4: 74 z 74 wyświetleń `audioChat` nie ma następnego ekranu w sesji.** To luka obserwowalności (brak `$screen` po wyjściu), a nie dowód „odbicia". Nie wyciągałem z tego wniosków.
- **Ostatnie 6 dni bez `voice_chat_started`** nie jest samo w sobie dowodem śmierci funkcji (były już zerowe tygodnie), dlatego jest hipotezą H4 do sprawdzenia, a nie ustaleniem.

---

## Aneks

### Zapytania

Pełne HogQL: `analytics-reports/raw/2026-08-10-voice-chat-b7.md` (sekcja Queries, znaczniki `-- @@ q1_weekly` … `-- @@ q13_reflect_limit_hit_skew`).
Pełne SQL Postgres: `db-reports/2026-08-10-voice-ai-cost.md` oraz `db-reports/2026-08-10-subscription-pipeline-check.md`.

Kluczowe cięcie kosztowe (60 dni, `token_usage_log`):

```sql
SELECT feature, COUNT(*), COUNT(DISTINCT user_id), SUM(cost_usd)
FROM token_usage_log
WHERE created_at >= now() - interval '60 days'
GROUP BY 1 ORDER BY SUM(cost_usd) DESC;
-- SYSTEM $134.23 (93%) | REFLECT $5.35 | ... | REALTIME_VOICE $0.000376 (ostatnie miejsce)
```

### Definicje

- **Użytkownik voice chat**: osoba, która kiedykolwiek wyemitowała `voice_chat_started` przy `$lib='posthog-flutter'`.
- **Aktywna subskrypcja premium**: `user_subscription.is_active = True AND end_date > now()` (nie samo `is_active`, które zawiera 18 wygasłych wierszy).
- **Koszt na aktywnego użytkownika głosu**: szacowany koszt cyklu życia (10–80 USD) / 11 osób = 1–7 USD. Nie jest to pomiar.
- **Próg k-anonimowości**: 25 osób. Segmenty poniżej progu raportowane wyłącznie jako surowe zliczenia potrzebne do decyzji; wszystkie metryki pochodne (retencja, konwersja) suprymowane.

### Odpowiedź na DONE_WHEN zadania B7

> „jest rekomendacja: wypromować, utrzymać bez inwestycji, albo wygasić – z liczbą kosztu na aktywnego użytkownika głosu"

**Rekomendacja: UTRZYMAĆ BEZ INWESTYCJI** przez 4 tygodnie, z bramką decyzyjną 2026-09-10 (R4), która wymusi wybór między wypromowaniem a wygaszeniem – po tym, jak R2 dostarczy pierwszą w historii projektu liczbę popytu na głos.
**Koszt na aktywnego użytkownika głosu: ok. 1–7 USD w całym cyklu życia** (szacunek z czasów trwania sesji × cennik OpenAI Realtime; pomiar niemożliwy, bo tokeny audio nigdy nie trafiają do naszego backendu).
**Migracja Gemini Live: NIE, wstrzymać.**
