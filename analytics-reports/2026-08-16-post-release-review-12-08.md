# Post-release review: wdrożenie z 12.08.2026

**Data raportu:** 2026-08-16
**Okno obserwacji:** 12–15.08 (4 pełne doby) + częściowy 16.08
**Źródła:** PostHog (projekt 141170, EU) + produkcyjny Postgres (read-only przez one-off dyno)
**Zakres release'u:** backend `67b1bdc` i wcześniejsze (Heroku v528–v531, 10–11.08), frontend build 2.0.77 (Codemagic z `d41dec4`, 11.08)

---

## 1. Werdykt

**Technicznie release się udał. Biznesowo nie ma czego oceniać.**

Instrumentacja, którą wdrożenie miało naprawić, faktycznie działa i już przyniosła konkretne odkrycia. Natomiast baza aktywnych użytkowników jest zbyt mała (38 unikalnych osób w 4 dni), a lejek płatności nadal nie jest oprzyrządowany od końca do końca, więc pytanie „czy poprawiliśmy konwersję" pozostaje bez odpowiedzi.

Największym odkryciem nie jest jednak sam efekt release'u, tylko to, co świeżo włączona telemetria backendu ujawniła: **system powiadomień wysyła jeden komunikat do 98,5% całej bazy użytkowników, codziennie, przy skuteczności 0,21%.**

---

## 2. Pułapka pomiarowa: fałszywy skok użytkowników

Od 11.08 metryka „aktywnych użytkowników" w PostHogu skacze z ~20 dziennie na ~1750 dziennie. To **nie są ludzie**.

| Dzień | „Użytkownicy" w PostHog | Realni ludzie w apce (`$lib = posthog-flutter`) |
|---|---|---|
| 08.08 | 13 | 8 |
| 10.08 | 23 | 12 |
| 12.08 | 1753 | 11 |
| 13.08 | 1823 | 17 |
| 14.08 | 1778 | 12 |
| 15.08 | 1658 | 13 |

Cały skok pochodzi z backendu (`$lib = posthog-python`), niemal wyłącznie z `moment.scheduled` i `moment.sent`. Przyczyna jest znana i zamierzona: naprawa inicjalizacji PostHoga w workerze sprawiła, że joby po raz pierwszy zaczęły raportować.

**Konsekwencja praktyczna:** każdy wykres aktywności w PostHogu jest teraz mylący, dopóki nie odfiltruje się `$lib = posthog-python`. Trzeba to poprawić w dashboardach, zanim ktoś podejmie decyzję na podstawie liczby 1750.

**Realna baza, po odfiltrowaniu:** 35 unikalnych osób w oknie 07–10.08, 38 w oknie 12–15.08. Bez zmian.

---

## 3. Co potwierdzone zadziałało

### 3.1 Pętla retry na Reflect – zabita
Przed release'em jeden użytkownik wygenerował **1870 błędów 403** na `/api/v1/reflect/{conversation_id}/message` w ciągu tygodnia (klient nie honorował limitu wiadomości i ponawiał w pętli). Po release'ie: **zero**. To był największy pojedynczy śmieć w danych.

### 3.2 Ogólny poziom błędów API spadł ponad dwukrotnie
Z ~570/dobę (04–10.08) do ~255/dobę (12–15.08). Głównie zasługa 3.1.

### 3.3 Tagowanie `is_expected` działa i jest bardzo użyteczne
Z 1045 zdarzeń `api_error` po release'ie:

| | Liczba | Interpretacja |
|---|---|---|
| `is_expected = true` | 949 | Spodziewane 404 („nie ma jeszcze karty prep / debriefu / health-checku") |
| `is_expected = false` | 96 | Do przejrzenia |
| z tego realne 5xx | **1** | `ClientDisconnect` przy uploadzie fragmentu nagrania, niegroźne |

Backend jest zdrowy. Jedna 500-ka na cztery doby.

### 3.4 Nowa telemetria faktycznie leci
- Raportowanie crashy (`$exception`) – działa, ze stacktrace'ami i fingerprintami
- Atrybucja instalacji z Play Install Referrer – 38 zdarzeń / 27 osób
- `$screen` z prawdziwymi nazwami ekranów (`mainPage`, `splash`, `welcome`, `subscription`, …)
- `user_activated`, `app_install_attributed`, telemetria nagrywania

---

## 4. Znalezisko krytyczne: powiadomienie ADD_THERAPY_DATE

### 4.1 Skala

Dane z produkcyjnego Postgresa, okno 10–16.08 (6 dni):

| Metryka | Wartość |
|---|---|
| Wszystkich użytkowników w bazie | 1813 |
| Z włączonymi powiadomieniami | 1791 |
| **Którzy dostali ADD_THERAPY_DATE** | **1786 (98,5% bazy)** |
| Liczba wygenerowanych momentów | 10 522 |
| Otwarte | 22 (0,21%) |
| Kliknięte (acted) | 5 (0,05%) |

Dla porównania, wszystkie pozostałe typy powiadomień razem w tym samym oknie: **170 momentów**. ADD_THERAPY_DATE to **99,1% całego ruchu powiadomień**. Zaprojektowana w MSV3.2.2 kadencja dwóch zróżnicowanych slotów dziennie zdegenerowała się w praktyce do jednego, powtarzanego w kółko komunikatu.

| Typ momentu | Momenty | Użytkownicy | Otwarte |
|---|---|---|---|
| ADD_THERAPY_DATE | 10 522 | 1786 | 22 |
| ACCOUNT_SETUP_NUDGE | 41 | 14 | 1 |
| THERAPY_RELATIONSHIP_CHECKIN | 30 | 30 | 0 |
| REFLECTION_INVITATION | 30 | 30 | 0 |
| RE_ENGAGEMENT | 27 | 26 | 1 |
| MOOD_UPDATE_REQUEST | 20 | 20 | 2 |
| GOALS_WEEKLY | 12 | 12 | 0 |
| pozostałe 6 typów | 10 | – | 6 |

### 4.2 Ile z tego to realne pushe

| | Użytkownicy | Momenty |
|---|---|---|
| Bez tokena FCM (push nie ma dokąd polecieć) | 1647 | 9705 |
| **Z tokenem FCM (realny push)** | **139** | **817** |

Czyli **139 realnych osób dostaje ten sam komunikat średnio 5,9 raza w 6 dni** – praktycznie codziennie. Pozostałe 9705 momentów to praca workera w próżnię.

Uwaga metodologiczna: kolumna `push_delivered` pokazuje `true` dla 8969 z 10 522 momentów, mimo że tylko 144 użytkowników w całej bazie ma jakikolwiek token. Kolumna ma `server_default = true` i najwyraźniej nie odzwierciedla faktycznej dostawy. Nie należy jej używać jako miary deliverability.

### 4.3 Koszt AI – sprawdzony, problemu nie ma

Tylko **66 z 10 692 momentów** ma `is_ai_generated = true`. ADD_THERAPY_DATE korzysta ze statycznych szablonów `_FALLBACK` w siedmiu językach. Wcześniejsza hipoteza o cichym paleniu budżetu AI jest **odrzucona**.

### 4.4 „Mam datę dodaną, a powiadomienie i tak przychodzi"

Zgłoszenie od operatora potwierdzone w danych, ale mechanizm jest inny niż zepsuty warunek.

W całej bazie 1793 rekordów preferencji **tylko 12 osób kiedykolwiek ustawiło jakąkolwiek datę terapii**:

| Stan | Liczba użytkowników |
|---|---|
| Ma harmonogram cykliczny (`therapy_schedule`) | 4 |
| Ma sesje z kalendarza (`custom_therapy_sessions`) | 8 |
| Ma `next_session_date` | 2 |
| Ma `next_session_date` w przyszłości | **1** |

Spośród 1786 odbiorców powiadomienia, **8 miało jakieś dane o dacie**:

| Użytkownik | Nudge'y | Ostatni | Harmonogram | Tryb | Najpóźniejsza data | Przyszłe sesje |
|---|---|---|---|---|---|---|
| a18e10b7 | 6 | 15.08 | nie | custom | 2026-07-01 | 0 |
| f034460f | 6 | 15.08 | nie | custom | 2026-05-04 | 0 |
| 0abbec3e | 6 | 15.08 | nie | custom | 2026-08-11 | 0 |
| 12175ec1 | 6 | 15.08 | nie | custom | 2026-04-04 | 0 |
| c5415ca4 | 6 | 15.08 | nie | custom | 2026-07-31 | 0 |
| dbfff546 | 6 | 15.08 | nie | custom | 2026-06-11 | 0 |
| 18478368 | 4 | 14.08 | **tak** | weekly | – | 0 |
| c1cf5af2 | 1 | 10.08 | tak | custom | 2026-08-19 | 1 |

**Wniosek:** w ostatnich 48 godzinach **zero** osób z ważną przyszłą datą dostało to powiadomienie. Warunek techniczny (`compute_next_session_date() is None`) działa poprawnie.

Problemem jest to, co ten warunek znaczy dla człowieka. Sześciu z ośmiu użytkowników **dodało datę terapii, ta data minęła i nikt ich nie poprosił o kolejną** – zamiast tego dostają codziennie komunikat „Nie ustawiłeś jeszcze nadchodzącej sesji terapii". Z ich perspektywy aplikacja twierdzi, że czegoś nie zrobili, choć to zrobili. To jest realny błąd produktowy, tylko w warstwie treści i cyklu życia daty, a nie w warunku logicznym.

Przypadek `18478368` (harmonogram cotygodniowy ustawiony, 4 nudge'e do 14.08) jest najbardziej podejrzany, ale przestał się powtarzać, co sugeruje, że użytkownik ustawił harmonogram po otrzymaniu powiadomień. Bez znacznika czasu modyfikacji preferencji nie da się tego rozstrzygnąć.

### 4.5 Poboczny defekt danych: `next_session_date` nie jest utrzymywane

**3 użytkowników ma ustawiony `therapy_schedule`, ale `next_session_date = NULL`.** Kolumna jest wyliczana przy zapisie w `crud.update_therapy_schedule` i nigdy potem nie odświeżana, więc po prostu zwietrzała. Generator powiadomień przelicza datę na żywo, więc jego to nie dotyczy, ale kolumna jest indeksowana i używana przez inne zapytania i joby, a jako źródło prawdy jest niewiarygodna.

---

## 5. Znalezisko: crash w firebase_analytics u praktycznie każdego

Nowe raportowanie crashy natychmiast złapało dominujący problem.

| | Wartość |
|---|---|
| Wyjątki od 11.08 | 111 |
| Dotknięci użytkownicy | 14 |
| Aktywni klienci w tym oknie | 41 |
| **Udział dotkniętych** | **34%** |

**83 ze 111** to jeden i ten sam błąd:

```
mechanism: PlatformDispatcher (handled: false)
package:firebase_analytics/src/firebase_analytics.dart:121
FirebaseAnalytics.logEvent
```

Dotyka **13 z 14** osób, które cokolwiek zgłosiły, czyli w praktyce każdego aktywnego użytkownika. Rozkład po wersjach: 2.0.77 – 77 crashy / 13 osób, 2.0.79 – 24 / 3, 2.0.78 – 10 / 2.

To nieobsłużony błąd asynchroniczny, więc raczej nie zabija aplikacji, ale ma dwa skutki: zaśmieca świeżo postawiony error tracking i oznacza, że **dane w Firebase Analytics również mogą być dziurawe**.

Uwaga: nie da się stwierdzić, czy to regresja z tego release'u – przed nim raportowania crashy po prostu nie było.

---

## 6. Znalezisko: lejek płatności praktycznie nie istnieje w danych

| Zdarzenie | Po release'ie (12–16.08) | Uwaga |
|---|---|---|
| `paywall_shown` | **1** (16.08, `trigger_feature = settings`) | Instrumentacja wdrożona 10.08 |
| `subscription_screen_opened` | 10 zdarzeń / 5 osób | Ekran JEST otwierany |
| `subscription_product_selected` | 1 | |
| `subscription_purchase_started` | 0 | |
| `subscription_purchase_completed` | 0 | Ostatnie: 5 zdarzeń / 4 osoby 10.08 (dzień deployu, prawdopodobnie testy) |
| `trial_started` (server-side) | **0** | Nie zapaliło się ani razu od wdrożenia |

Ludzie wchodzą na ekran subskrypcji, a `paywall_shown` się nie zapala.

> **KOREKTA (2026-08-16, po audycie kodu frontendu).** Pierwotny wniosek tej sekcji – „event jest podpięty tylko w ustawieniach" – był **błędny**. `paywall_shown` jest podpięty do **ośmiu** wejść (menu boczne, popup po wygaśnięciu triala, bramka nagrywania sesji, dwie bramki limitu wiadomości Reflect, bramka głosu w Reflect, dwie bramki audytu miesięcznego). Pojedyncze zdarzenie z `trigger_feature = settings` pochodzi z **wcześniejszego builda** – baner premium w ustawieniach został celowo usunięty w przebudowie menu z 15.08.
>
> Prawdziwe wyjaśnienie liczby „1" jest dwuczęściowe: (a) mierzone buildy 2.0.77–2.0.79 nie zawierały jeszcze części tego podpięcia, które weszło 15.08, oraz (b) ekspozycja była znikoma (maks. 29 osób na 2.0.77).
>
> **Pozostaje jednak pytanie otwarte, potencjalnie blokujące sprzedaż.** `paywall_shown` zapala się dopiero po **udanym pobraniu produktów ze sklepu** i tylko gdy użytkownik nie jest już premium. Skoro 5 osób otworzyło ekran subskrypcji 10 razy i praktycznie nie wygenerowało tego zdarzenia, to albo były to osoby już posiadające subskrypcję, albo **pobieranie produktów zawodzi** – a wtedy ci ludzie nie mieli fizycznie czego kupić. To wymaga rozstrzygnięcia, patrz sekcja 6a.

Bez działającego pomiaru nie da się policzyć ani współczynnika wyświetleń paywalla, ani konwersji.

---

## 6a. Znalezisko krytyczne: zakupy nie docierały na serwer

Wykryte podczas audytu ścieżki płatniczej, po tym jak dane z produkcji pokazały **5 zakończonych zakupów zgłoszonych przez aplikację u 4 osób wobec jednego paragonu na serwerze**. Znaleziono dwa niezależne błędy, oba naprawione w tym batchu.

**Błąd 1: transakcja finalizowana przed zapisem na serwerze.** Aplikacja wołała `completePurchase()` – czyli nieodwracalnie domykała transakcję po stronie sklepu, po czym sklep nigdy jej już nie dostarczał ponownie – **zanim** wysłała paragon do naszego backendu. Zerwana sieć, błąd serwera albo zabicie aplikacji w tym oknie oznaczały transakcję domkniętą w sklepie i **zero śladu po stronie serwera**. Użytkownik płaci i nie dostaje premium.

**Błąd 2: przywracanie zakupów nigdy nie wysyłało paragonu.** Metody zapisujące subskrypcję akceptowały wyłącznie status „kupione" i **po cichu nic nie robiły** dla statusu „przywrócone", którym posługuje się cała ścieżka przywracania zakupów. Aplikacja mimo to domykała transakcję i raportowała udane przywrócenie. W praktyce oznacza to, że **każde użycie funkcji przywracania zakupów w historii aplikacji nie zapisało paragonu na serwerze**.

Błąd 2 jest szczególnie dotkliwy, bo przywracanie zakupów to dokładnie ta funkcja, po którą sięga osoba, której subskrypcja „zniknęła" – czyli ofiara błędu 1. Obie ścieżki wyjścia z problemu były zamknięte.

Naprawa: weryfikacja na serwerze przed domknięciem transakcji, jedno ponowienie z odczekaniem 2 s, a przy nieudanej weryfikacji transakcja **zostaje otwarta**, żeby sklep dostarczył ją ponownie. Status „przywrócone" jest akceptowany.

**Ograniczenie, które zostaje:** nie ma trwałej kolejki ani nasłuchu transakcji uruchamianego przy starcie aplikacji. Zakup przerwany w trakcie weryfikacji jest teraz bezpiecznie *otwarty* zamiast po cichu domknięty, ale jego odzyskanie nadal wymaga, żeby użytkownik ponownie wszedł na ekran subskrypcji. Zgłoszone jako follow-up.

**Ta zmiana wymaga testu na fizycznym urządzeniu** z prawdziwym sandboxem sklepu (zakup, przywracanie, zabicie aplikacji w trakcie) przed wypuszczeniem. Testy jednostkowe jej nie zastąpią.

---

## 7. Pozostałe obserwacje

- **Adopcja nowego builda jest znikoma.** 2.0.77 to łącznie 29 osób, maks. 11 dziennie. Część bazy siedzi jeszcze na 2.0.76 i 2.0.75. Nawet gdyby pojawiły się sygnały biznesowe, dotyczyłyby garstki.
- **Rejestracje bez zmian:** `user_registered` 1–5 dziennie przed i po. `onboarding_completed` 1–2 dziennie.
- **`user_activated`:** 6 (11.08), 2, 3, potem trzy doby po zero. Po jednorazowym „dogonieniu" istniejących kont nowych aktywacji brak.
- **1669 z 1813 użytkowników nie ma żadnego tokena FCM.** To sugeruje bazę kont, które nigdy realnie nie weszły do aplikacji lub cofnęły zgodę na powiadomienia.
- **14.08 jeden użytkownik wygenerował 105 zdarzeń `recording_upload_completed` i 9 `recording_processing_failed`.** Albo bardzo długa sesja, albo pętla ponowień. Do sprawdzenia.
- **`moment.expired` ~20 dziennie zawsze z jednego `person_id`** – ten job najprawdopodobniej nie przekazuje `distinct_id` użytkownika i wszystko wpada na jeden anonimowy profil w PostHogu.

---

## 8. Rekomendacje w kolejności pilności

| # | Działanie | Uzasadnienie |
|---|---|---|
| 1 | **Okiełznać ADD_THERAPY_DATE**: nie planować dla kont bez tokena FCM, limit typu raz na 7 dni na osobę, twardy limit prób | 139 realnych osób dostaje codziennie ten sam push przy skuteczności 0,21%; 9705 momentów mieli w próżnię |
| 2 | **Naprawić cykl życia daty terapii**: gdy ostatnia sesja minęła, komunikat ma brzmieć „zaplanuj kolejną sesję", a nie „nie ustawiłeś sesji" | 6 z 8 osób, które faktycznie dodały datę, dostaje komunikat zaprzeczający ich działaniu |
| 3 | **Naprawić crash `FirebaseAnalytics.logEvent`** | dotyczy praktycznie każdego aktywnego użytkownika, psuje też dane w Firebase |
| 4 | **Podpiąć `paywall_shown` do realnych wejść na paywall** | bez tego lejek płatności jest niemierzalny |
| 5 | **Poprawić dashboardy PostHog**: filtr wykluczający `$lib = posthog-python` na metrykach aktywności | inaczej wszyscy czytają 1750 zamiast 13 |
| 6 | **Odświeżać `next_session_date`** lub przestać go traktować jako źródło prawdy | 3 użytkowników ma harmonogram i NULL w kolumnie |
| 7 | **Naprawić `push_delivered`** żeby odzwierciedlał faktyczną dostawę | dziś `true` dla 8969 momentów przy 144 tokenach w całej bazie |
| 8 | Zbadać `distinct_id` w jobie wygaszającym momenty | `moment.expired` trafia na jeden anonimowy profil |

---

## 9. Metodologia i ograniczenia

- Dane PostHog pobrane przez read-only REST/HogQL (`scripts/posthog_query.py`), projekt 141170 (EU).
- Dane produkcyjne pobrane przez one-off dyno Heroku, wyłącznie `SELECT`, bez DML/DDL. Dyno zatrzymane po zakończeniu.
- Identyfikatory użytkowników w sekcji 4.4 są zahaszowane (`md5`, 8 znaków), treści sesji i nazwiska terapeutów nie były pobierane.
- Dane z 16.08 są niepełne (doba w toku) – nie należy z nich czytać spadku.
- Okno 4 dni i baza 38 aktywnych użytkowników **nie wystarczają** do wnioskowania o retencji, konwersji ani przychodzie. Wszystkie wnioski biznesowe w tym raporcie są celowo wstrzymane.
