# MindSync w ośmiu przekrojach PostHog: raport zbiorczy

- **Data**: 2026-10-15
- **Analityk**: growth-analyst
- **Pytanie biznesowe**: gdzie dziś tracimy najwięcej ludzi na drodze od pierwszego otwarcia do płacenia i powrotu, i która jedna dźwignia ruszy wynik najbardziej?
- **Miara sukcesu**: odsetek nowych osób, które w ciągu 14 dni wracają do aplikacji (R14), oraz liczba realnych zakupów w miesiącu (prawda w Postgres)
- **Okno danych**: 2026-07-17 → 2026-10-15 (retencja, churn), 2026-08-16 → 2026-10-15 (pozyskanie, paywall), 2026-09-15 → 2026-10-15 (onboarding, funkcje, błędy)
- **Źródła**: 8 surowych ekstraktów PostHog (proj. 141170) z 2026-10-15 w `analytics-reports/raw/`: `recent-changes-impact`, `errors-stability`, `acquisition`, `onboarding-activation`, `retention-engagement`, `conversion-paywall`, `churn-signals`, `feature-usage-voice`. Bez nowych zapytań do PostHog i bez Postgres (rozbieżności dało się rozstrzygnąć definicjami). Kontekst: wcześniejsze raporty z 2026-09-12, 09-25 i 10-03.
- **Pewność**: średnia dla kierunków (kilka niezależnych ekstraktów mówi to samo), niska dla wszystkich stóp konwersji i efektów zmian po 03.10 (n w dziesiątkach, okna po zmianie 6-12 dni)

> Próg prywatności: grupy poniżej 5 osób oznaczone `n<5`, zgodnie z ekstraktami i poleceniem. Standardowy próg tego agenta to 25; wszystkie odsetki liczone na mniej niż 25 osobach są oznaczone jako hipotezy, nie wyniki.

---

## 1. Streszczenie dla zarządu

W ciągu 60 dni aplikację otworzyło po raz pierwszy 296 realnych osób, ale tylko 94 (32%) w ogóle zaczęło onboarding, 71 (24%) go skończyło, a po dwóch tygodniach wraca 10% (19/186). Prawdziwa baza użytkowników jest mała i stabilna: ok. 80 osób miesięcznie robi cokolwiek po zalogowaniu (MAU ścisłe 73-83), a "MAU" ok. 250 to w dwóch trzecich ludzie, którzy nie przeszli dalej niż ekran powitalny lub logowanie. Redesign z 03.10 wyraźnie poprawił środek lejka (ukończenie onboardingu ze startu 47% → 74%, rozmowa w pierwszej dobie 14% → 42%, zasięg paywalla 5,8% → 14,9% aktywnych), ale retencji i przychodu z niego jeszcze nie da się ocenić: najstarsze osoby po zmianie mają 12 dni, a zakupów jest garstka (6 osób w 13 dni, wszystkie plany miesięczne, zero rocznych, zero konwersji triala na iOS z 10 zakończonych). Wzrost liczby instalacji od 21.09 to prawie w całości ruch z Google Play w językach fr/ar/fa z Afryki Zachodniej i Bliskiego Wschodu, z ukończeniem onboardingu 5-11% i R14 bliskim zera; to nie jest wzrost biznesu. Najsilniejszy sygnał odejścia jest prosty: kto w pierwszym tygodniu był aktywny tylko jednego dnia, praktycznie nie wraca (0 z 8 w kohorcie wrześniowej). **Najważniejsza dźwignia na najbliższe dwa tygodnie to wypuszczenie do sklepów buildów 2.0.109+ (plan pierwszego tygodnia), bo to jedyna gotowa zmiana celująca w "drugi dzień", ale najpierw trzeba dodać zdarzenie ekspozycji planu, inaczej jej efektu nie zmierzymy.** Równolegle najtańszym ruchem jest zatrzymanie pushy WEEKLY/MONTHLY_SUMMARY do całej bazy (6942 wysyłki w miesiącu, 7 otwarć).

---

## 2. Lejek end-to-end

Dwie tabele, bo nie da się uczciwie skleić jednego lejka z jedną kohortą przez wszystkie kroki: pozyskanie i retencja mają długie okno (60 dni, stary i nowy przepływ razem), a nowy przepływ po 03.10 ma dopiero 38 osób.

### 2a. Kohorta 60 dni (08-16 → 10-15), realni nowi, wszystkie przepływy

| krok | osoby | % poprzedniego | % nowych | źródło (ekstrakt, zapytanie) |
|---|---|---|---|---|
| pierwsze otwarcie aplikacji (nowy `person_id` flutter, bez botów i testerów) | 296 | | 100% | acquisition, `newuser_cube` |
| zaczął onboarding (`onboarding_started`) | 94 | 32% | 32% | acquisition, `newuser_cube` |
| **strata przed onboardingiem** | **202** | **68%** | | |
| ukończył onboarding (`onboarding_completed`) | 71 | 76% | 24% | acquisition, `newuser_cube` |
| powrót w dniach 1-7 (R7, kwalifikujący się) | 45/250 | | 18% | acquisition, `newuser_cube` |
| powrót w dniach 7-13 (R14, kwalifikujący się) | 19/186 | | 10% | acquisition, `newuser_cube` |
| W1 tylko po onboardingu (kohorty 07-13..08-31) | 15/55 | | 27% | retention, `cohort_weekly_onboarded_only` |
| W2 tylko po onboardingu (te same kohorty) | 14/55 | | 25% | retention, `cohort_weekly_onboarded_only` |

Segment angielski (`$locale=en`): 144 nowych, 33% ukończenia, R7 24%, R14 18% (acquisition, tabela 3). To lepszy punkt odniesienia dla jakości produktu niż średnia z całego ruchu.

### 2b. Nowy przepływ (onboarding rozpoczęty od 03.10, n=38, bez testerów)

| krok | osoby | % startów | źródło |
|---|---|---|---|
| start onboardingu | 38 | 100% | onboarding-activation, `cohort_flow` |
| przeszedł bramkę prawną (`legal_gate`) | 29 | 76% | onboarding-activation, `step_funnel` |
| `onboarding_completed` | 28 | 74% (przed: 47%) | onboarding-activation, `cohort_flow` |
| `post_onboarding_build_viewed` | 26 | 68% | onboarding-activation |
| `first_conversation_intro_viewed` | 17 | 45% | onboarding-activation |
| **strata build → intro rozmowy** | **9** | **35% kroku** | |
| `first_conversation_started` | 15 | 39% | onboarding-activation |
| `first_conversation_ended` | 11 | 29% | onboarding-activation |
| paywall po onboardingu (`post_onboarding*`) | 12 | 32% | onboarding-activation |
| trial (backend `trial_started`, cała baza od 03.10) | 54 os. | nie do tej kohorty | conversion-paywall, trial → płatny |
| zakup (klient lub backend, realni, 03.10-15.10) | 6 os. (klient n<5) | | conversion-paywall, lejek per okres |
| trial → płatny | Android n<5 z 33; iOS 0 z 10 zakończonych | | conversion-paywall |
| powrót W1/W2 | jeszcze niemierzalne (najstarsi 12 dni) | | retention, sekcja 3 |

### Gdzie leży największa strata

1. **Przed onboardingiem: 202 z 296 nowych (68%).** To potwierdzają trzy niezależne ekstrakty: acquisition (68% nigdy nie startuje onboardingu), churn-signals (50% wszystkich odchodzących kończy na `splash`, `welcome` albo `auth`) i retention (MAU szerokie 234 vs ścisłe 73 w tyg. 10-05, czyli ok. 2/3 "aktywnych" nie przeszło logowania). Część tej straty to szum, a nie ludzie: fragmenty tożsamości (26% rejestracji backendu bez zdarzeń aplikacji pod tym samym `person_id`), niewyłapane farmy testowe Play i ruch fr/ar/fa niskiej jakości. W segmencie angielskim strata jest mniejsza, ale wciąż jest największym pojedynczym odpływem. Wcześniejszy, oczyszczony pomiar z 2026-08-10 dawał 41% realnego odbicia od ściany rejestracji.
2. **Drugi dzień.** Wśród tych, którzy przeszli onboarding, W1 wynosi 27-31%, a wśród wszystkich nowych D1 7-11%. Mediana aktywnych dni w pierwszym tygodniu u odchodzących to 1,0.
3. **W nowym przepływie: przejście z ekranu budowania do pierwszej rozmowy (26 → 17).** Mała liczba, ale to dziś największa dziura po onboardingu.

---

## 3. Wnioski przekrojowe

Każdy wniosek podaję z listą ekstraktów, które go wspierają. Kolejność: od najmocniej potwierdzonego.

### W1. Ludzie odpadają przed zalogowaniem, a nie w onboardingu · Wpływ: krytyczny · Pewność: wysoka

- **acquisition**: 94/296 startuje onboarding (32%); dwie trzecie odpada na otwarciu → logowaniu.
- **churn-signals**: ostatnie zdarzenie 163 z 324 odchodzących (50%) to `screen:auth` 67, `screen:welcome` 49, `screen:splash` 47.
- **retention**: MAU szerokie vs ścisłe 234,6 vs 73,0 (tydz. 10-05).
- **errors-stability**: `auth_validation_failed` z powodem `email_empty` u 20 osób w 14 dni (42 zdarzenia), `login_failed` `unknown` u 7 osób. Ludzie naciskają "dalej" bez wpisanego e-maila, a część logowań kończy się błędem bez rozpoznanej przyczyny.
- **onboarding-activation**: sam onboarding po redesignie traci mało (bramka prawna 38 → 32 widzi, potem prawie bez strat).
- **Co z tego wynika**: każdy procent poprawy na ekranie powitania i logowania jest wart więcej niż ten sam procent w onboardingu, bo dotyczy trzykrotnie większej grupy. Wniosek dotyczy kierunku; dokładna wielkość jest zawyżona przez szum tożsamości.

### W2. Jakość ruchu: fr/ar/fa vs US/iOS · Wpływ: wysoki (fałszywy obraz wzrostu) · Pewność: wysoka

- **acquisition**: tygodnie 09-21..10-05 dały 185 nowych, z czego ok. 60% to Android w językach fr/ar/fa (CI, IR, DZ, SN, IQ, BF, CM). Ukończenie onboardingu: `fr` 5%, `fa` 0%, `ar` 17%; R14 bliskie zera. US: 39% ukończenia, R14 22%. Rynki zachodnie razem: 40% ukończenia i R14 20%, reszta świata 11% i 3%.
- **acquisition / retention**: iOS 46% ukończenia, R14 33% (n=18 kwal.), D7 38% (n=34); Android 22%, R14 8%, D7 17%.
- **onboarding-activation**: jedyny porównywalny segment po redesignie to Android/en (8/16 → 15/20); reszta języków to `n<5`.
- **retention**: skok "nowych" w lifecycle (46/78/57 tygodniowo) przy płaskiej liczbie powracających (12-15 tygodniowo) i quick ratio < 1 we wszystkich pełnych tygodniach poza 09-21 i 09-28.
- **Co z tego wynika**: od 21.09 rosną wskaźniki objętościowe (nowi, MAU szerokie), ale nie rośnie rdzeń. Każdy wskaźnik lejka musi być od dziś raportowany osobno dla en i dla reszty, inaczej wynik redesignu utonie w zmianie miksu ruchu. Różnica iOS vs Android to korelacja z miksem (rynek, odbicia, farmy testowe), nie dowód, że platforma sama w sobie retencjonuje lepiej.

### W3. Jeden dzień aktywności w pierwszym tygodniu to najsilniejszy sygnał odejścia · Wpływ: krytyczny · Pewność: średnio-wysoka

- **churn-signals**: zalogowani z kohorty 07-17..09-24 (n=91): odchodzący mają medianę 1,0 aktywnego dnia w tyg. 1, zostający 2,5. 251 z 324 odchodzących miało w ogóle tylko 1 dzień aktywności.
- **onboarding-activation**: w kohorcie wrześniowej osoby z mniej niż 2 aktywnymi dniami w tyg. 1: 0 z 8 wróciło w tyg. 2; z 2+ dniami 6/25.
- **retention**: średnio 1,70 dnia aktywności na osobę w 28 dniach; tylko 13% aktywnych ma 3+ dni.
- **churn-signals**: pushe re-engagement (wysyłane po 3 i 7 dniach) przywracają 8 z 288 wysyłek w 72 h (2,8%). Ścieżka odzysku po fakcie nie działa.
- **Co z tego wynika**: walka toczy się o dzień +1/+2, nie o tydzień 3. Mechanizm, który daje powód do powrotu nazajutrz (plan pierwszego tygodnia, przypomnienie o wybranej porze, kontynuacja rozmowy), jest ważniejszy niż kolejne pushe odzyskowe. Kierunek przyczynowy nie jest dowiedziony: możliwe, że osoby z drugim dniem po prostu od początku miały silniejszą potrzebę.

### W4. Debrief jako kandydat na moment "aha" · Wpływ: wysoki, jeśli się potwierdzi · Pewność: niska (n=6)

- **onboarding-activation**: w kohorcie wrześniowej (n=33, bazowo 18% powrotu w tyg. 2) wpis w tyg. 1, głównie `debrief_started`, zrobiło 6 osób, wróciło 5 (83%). Wpisy innych typów są `n<5`.
- **retention**: użytkownicy pętli terapii w okresie 09-17..09-30 (n=14) wrócili w okresie 2 w 9 przypadkach; nieużytkownicy 15%.
- **feature-usage-voice**: Debrief jako jedna z nielicznych funkcji rośnie szybciej niż baza (17 vs 11 osób w połówkach okna przy wzroście bazy o 33%).
- **Zgodność z wcześniejszą wiedzą**: definicja aktywacji z 2026-08-10 (≥1 zapis pętli terapii w 24 h) dała 3,41x wyższy powrót na n=652. Dzisiejsze dane są z tym zgodne, ale same niczego nie dowodzą.
- **Kontra**: churn-signals pokazuje `debrief_started` wśród ostatnich 10 zdarzeń 9 odchodzących, więc debrief nie chroni przed odejściem automatycznie. Efekt selekcji (debrief robi ktoś, kto chodzi na terapię i już ma motywację) jest tu bardzo prawdopodobny.
- **Co z tego wynika**: debrief zostaje kandydatem, a nie faktem. Testowalna hipoteza: zaproszenie do debriefu po najbliższej sesji terapii w planie pierwszego tygodnia podnosi powrót w tyg. 2 u osób w terapii.

### W5. Redesign 03.10 poprawił onboarding i aktywację w pierwszej dobie, retencji jeszcze nie da się ocenić · Pewność: średnia dla onboardingu, brak dla retencji

- **onboarding-activation**: ukończenie onboardingu ze startu 47% (17/36) → 74% (28/38); rozmowa w 24 h 14% → 42%; "nic w 24 h" 83% → 50%. Mediana pierwszej rozmowy głosowej 358 s, 9 z 11 doszło do otwartej części.
- **recent-changes-impact**: `onboarding_completed`/`signup_started` 0,55-0,59 → 0,91-0,93; kohorta W4 (10-10..10-15) ma 56% onboardingu, 44% pierwszej rozmowy i 65% triala w ciągu 7 dni, ale zero osób z pełnym oknem 7 dni.
- **conversion-paywall**: zasięg paywalla 5,8% → 14,9% aktywnych; realni bez ani jednego `subscription_purchase_failed` po 03.10.
- **retention**: D1 ścisłe 12,2% (VII-VIII) → 16,7% (IX) → 21,4% (od 03.10, n=28); różnica to 1-2 osoby, mieści się w szumie. D7 po zmianie: 9 osób kwalifikuje się w definicji ścisłej. D30: nikt.
- **Uwaga do porównania**: część poprawy onboardingu to mniejszy mianownik (34 nowych w W4) i zmiana definicji kroku (trial i ekrany `post_onboarding_*` przesunięte), a wczesna grupa B (03-08.10) wypadła słabo, bo pierwsza rozmowa v2 dotarła do sklepowego Androida dopiero 09.10 (2.0.107).

### W6. Zmiany z 09-15.10 są tylko u testerów · Pewność: wysoka

- **recent-changes-impact**: plan pierwszego tygodnia (2.0.109, 12.10), redesign kart (2.0.111, 14.10), GPT-Live-1 (2.0.112, 15.10) mają po `n<5` użytkowników, prawie wyłącznie TestFlight. Sklepowy Android to 2.0.107 (41 osób w 7 dni), App Store 2.0.106. 2.0.110 Android (9 osób) to prawdopodobnie ścieżka testowa lub etapowe wdrożenie; z PostHog nie da się tego rozstrzygnąć.
- **feature-usage-voice / errors-stability**: GPT-Live-1 to 1 osoba, 2 sesje, brak błędów, brak porównania z Classic (Classic nie ma `voice_engine=classic`).
- **onboarding-activation**: plan pierwszego tygodnia nie ma zdarzenia ekspozycji; 3 osoby z interakcją.
- **Co z tego wynika**: o tych zmianach nie wolno dziś mówić "działa" ani "nie działa". 28 zdarzeń zdefiniowanych w kodzie nigdy nie pojawiło się w PostHog; przy tej liczbie testerów to raczej brak okazji, ale trzeba to sprawdzić przed premierą w sklepie.

### W7. Monetyzacja: za mało danych na stopy, ale są trzy twarde obserwacje · Pewność: niska co do stóp, średnia co do faktów

- **conversion-paywall**: w 60 dniach **żaden realny użytkownik nie kupił planu rocznego**, mimo że roczny jest domyślnie zaznaczony (14 z "wyborów planu" po 03.10 to preselekcja). Świadome wybory po 03.10: miesięczny 6 osób, roczny `n<5`.
- **conversion-paywall**: iOS trial → płatny 0 z 10 zakończonych; iOS App Store na 2.0.100 to 8 osób, z czego 0 widziało paywall i 0 ukończyło onboarding w oknie. Na iOS lejek po 03.10 praktycznie nie istnieje w danych.
- **conversion-paywall / churn-signals**: paywall nie jest miejscem odejścia (nie ma go w ostatnich 10 zdarzeniach żadnej zalogowanej osoby z top 40). Bramki premium w funkcjach prawie się nie pokazują (po 1 osobie), bo 4-dniowy trial wciąż ukrywa limity, co zgadza się z raportem z 2026-09-25.
- **retention**: "premium" w `subscription_tier` to w większości trial nadany przy rejestracji (52 z 57 `premium_source`), więc wysoka retencja "premium" (D7 58%) to odwrócona przyczynowość: trial dostaje każdy, kto przeszedł rejestrację.

### W8. Błędy: dużo zdarzeń, umiarkowanie dużo ludzi, jeden realny problem na Androidzie · Pewność: średnia

- **errors-stability**: realny błąd (bez walidacji formularza, anulowań i oczekiwanych 404) u 63/165 aktywnych w 14 dni (38%); po odjęciu 404 profilu przy pierwszym uruchomieniu u 35/165 (21%). Żadna wersja nie pokazuje skoku liczby osób z błędami; skoki zdarzeń to 1-3 osoby w pętli.
- **errors-stability**: `client_error` FirebaseAuthException wyłącznie na Androidzie: 1462 zdarzenia / 18 osób w 30 dni, głównie na `mainPage` (921 / 11). To wygląda na wygasający lub nieodświeżany token w zalogowanej sesji.
- **errors-stability**: 404 na `/users/get_user_profile_and_subscription` (37 osób) i `/users/therapy-context` (36) dotyczy w 100% świeżych instalacji w pierwszych 30 minutach, a 71% z nich kończy onboarding. To oczekiwana ścieżka "profil jeszcze nie istnieje", źle oznaczona jako `is_expected=false`. Zamyka to otwarty punkt B3 z raportu 2026-09-12.
- **churn-signals**: nieoczekiwany `api_error` w 90 dniach dotyka 40% zarówno odchodzących, jak i zostających, więc nie różnicuje grup. W dobie przed ostatnią aktywnością: 32% vs 23%, co jest słabym sygnałem.

### Rozbieżności liczb między ekstraktami i której liczbie ufać

| wielkość | wartości w ekstraktach | skąd różnica | której ufać |
|---|---|---|---|
| **nowi tygodniowo** | 78 (acquisition, tydz. od pn 09-28); 76 (recent-changes, W2 od sob 09-26); 78 (retention, kohorta 09-28) | granice tygodnia (pn vs sob), wykluczenie testerów na poziomie osoby (acquisition) vs na poziomie zdarzenia (recent-changes) | **acquisition** (wykluczenie per osoba, 296 w 60 dni) jako licznik nowych; żaden nie jest liczbą kont, ta jest w tabeli `users` |
| **rejestracje** | 146 `user_registered` (backend) vs 94 `onboarding_started` | 26% rejestracji backendu nie ma zdarzeń aplikacji pod tym samym `person_id` (rozbita tożsamość) | do liczby kont: **Postgres `users`**; do lejka: `onboarding_started` |
| **aktywni** | 470 (churn, 90d) / 461 (retention, 90d); 257 (feature-usage, 30d); 165 (errors, 14d, bez filtrów); 134 (conversion, 13d); MAU ścisłe 73-83 | okno, filtry (errors bez filtrów testerów), definicja "aktywny" (każde zdarzenie vs po zalogowaniu) | **MAU ścisłe ok. 80** jako liczba realnych użytkowników; MAU szerokie tylko jako licznik otwarć |
| **ukończenie onboardingu** | 24% nowych (acquisition); 74% startów (onboarding-activation, B); 0,91 `completed/signup_started` (recent-changes) | różne mianowniki: nowi vs rozpoczynający vs `signup_started` | **% startów** do oceny onboardingu, **% nowych** do oceny całego lejka; nie mieszać |
| **kupujący** | 6 os. w PO i 6 w PRZED (klient lub backend, conversion); 8 klienckich w 90d (churn); W3 6 os. z 291 zdarzeniami (recent-changes, z testerem) | podwójna emisja klient+backend, odnowienia sandbox, 186 zdarzeń backendu z `$os=Windows`, tester w pętli | **żadnej z nich**; prawda w `subscription_receipts`; ostatnia znana baza z 2026-09-12: 7 realnych płacących |
| **retencja tygodnia 1** | R7 18% (acquisition); D7 17-22% (retention, szeroko); W1 7,7-17,5% (retention, kohorty tygodniowe) | R7/D7 = dowolny dzień 1-7 kumulatywnie; W1 = aktywność w następnym tygodniu kalendarzowym | **R7/D7 ok. 18%** wśród nowych; W1 do trendów tydzień do tygodnia |
| **D1** | 7,2-11,2% szeroko vs 12,2-21,4% ściśle | ścisła liczy tylko osoby, które przeszły logowanie | ścisła do oceny produktu; baseline z 09-12 (7,5%) był szeroki, więc porównuj szeroki z szerokim |
| **trial** | 54 osoby (conversion) = 21 + 33 (recent-changes) | brak rozbieżności | 54 |
| **otwarcia pushy** | `moment.opened` 235/73 osoby (90d) vs `notification_opened` 142/31; tylko 10 z 62 `moment.opened` łączy się z wysyłką | `moment.opened` najpewniej rejestrowane po stronie backendu bez otwarcia aplikacji | **`notification_opened` (klient)** |

---

## 4. Rekomendacje w kolejności priorytetu

Ocena: wpływ (W) × pewność (P) × koszt (K), każde 1-3, gdzie 3 = duży wpływ, wysoka pewność, niski koszt. Oznaczenie **[dane]** = wynika z danych na n ≥ 25; **[hipoteza]** = oparte na n < 25 albo na korelacji, do sprawdzenia testem.

### R1. Dodać `first_week_plan_shown` i wypuścić 2.0.109+ do sklepów · W3 P2 K3 · [hipoteza co do efektu, dane co do problemu]

- **Hipoteza**: plan pierwszego tygodnia daje powód do powrotu w dniu +1/+2, czyli dokładnie tam, gdzie tracimy ludzi (W3).
- **Warunek wstępny**: bez zdarzenia ekspozycji nie odróżnimy "plan nie działa" od "plan się nie pokazał". Dodać `first_week_plan_shown` {`plan_day`, `items_count`}, celowo bez żadnej właściwości tonu planu (ton łagodny wynika z sygnału kryzysowego, audyt H-1) przed premierą sklepową oraz sprawdzić 28 zdarzeń zdefiniowanych, a niewidzianych, na urządzeniu testowym.
- **Oczekiwany efekt**: D1 ścisłe z ok. 17% do 22-25%, odsetek osób z 2+ dniami w tyg. 1 z ok. 27% do 35%.
- **Właściciel**: `flutter-mobile` (zdarzenie), `integration-devops` (wydanie do sklepów), `posthog-data-extractor` (potwierdzenie, że zdarzenia płyną).
- **Pomiar**: kohorta nowych od daty publikacji, D1 i "2+ dni w tyg. 1", osobno en i reszta, porównanie z kohortą 10-03..10-15; pierwsza ocena 14 dni po premierze. Przypomnienie z polityki prywatności: analizować wyłącznie agregaty, nigdy ton ani plan pojedynczej osoby.

### R2. Zatrzymać WEEKLY/MONTHLY_SUMMARY_READY dla kont nieaktywnych · W2 P3 K3 · [dane]

- **Hipoteza**: te pushe nie przynoszą powrotów, a kosztują (generacja AI) i uczą ludzi ignorować powiadomienia.
- **Dowód**: 5204 wysyłki WEEKLY do 1831 odbiorców i 1738 MONTHLY do 1738 w 31 dni, dopasowane otwarcia odpowiednio 6 i 1 (feature-usage-voice). Odbiorców jest ok. 22x więcej niż realnych MAU.
- **Do wyjaśnienia**: wdrożenie v549 (13.09) miało ciąć koszt AI pushy; wysyłki nadal płyną do całej bazy. Trzeba ustalić, czy v549 wyciął tylko generację treści, czy także wysyłkę.
- **Oczekiwany efekt**: spadek wysyłek o ok. 90%, zero straty w otwarciach, niższy koszt AI (wg raportu z 09-12 powiadomienia to większość wydatków AI).
- **Właściciel**: `data-analytics` (`app/tasks/notifications.py`, kryterium aktywności 30 dni po zdarzeniach klienta).
- **Pomiar**: `moment.sent` per typ i `notification_opened` per typ, tydzień przed i po; koszt z `token_usage_log` przez `database-administrator`.

### R3. Naprawić wejście: ekran powitalny i logowanie · W3 P2 K2 · [dane co do problemu, hipoteza co do rozwiązania]

- **Hipoteza**: część z 68% odpływu przed onboardingiem to tarcie, które da się usunąć: pusty e-mail przy "dalej" (20 osób w 14 dni), `login_failed` z powodem `unknown` (7 osób), brak `$screen` dla `welcome` i `wow`, przez co nie widać, gdzie dokładnie ludzie odpadają.
- **Działania**: (a) nazwać trasy `welcome`/`wow`, żeby lejek był mierzalny; (b) zablokować przycisk bez e-maila zamiast zwracać błąd walidacji i wyeksponować logowanie Google/Apple; (c) rozpoznać `unknown` w `login_failed`; (d) temat gościnnego wejścia przed rejestracją (z raportu 08-10) czeka na decyzję `security-guardian` w sprawie Art. 9.
- **Oczekiwany efekt**: nowi en → `onboarding_started` z ok. 40-45% do 55%.
- **Właściciel**: `ui-ux-designer` (audyt ekranu powitania i logowania), `flutter-mobile` (wdrożenie i nazwy tras).
- **Pomiar**: nowi (acquisition) → `onboarding_started` w 7 dni, tylko `$locale=en`, 4 tygodnie przed vs 4 po.

### R4. Raportować wszystkie wskaźniki lejka osobno dla en i dla reszty ruchu · W2 P3 K3 · [dane]

- **Hipoteza**: zmiana miksu ruchu (fr/ar/fa od 21.09) maskuje lub udaje efekty zmian produktowych.
- **Działanie**: standardowy filtr segmentu w każdym raporcie i w dashboardzie Onboarding Health (bez tworzenia przeze mnie artefaktów w PostHog); równolegle ustalić źródło skoku w Play Console (pytanie otwarte P1).
- **Oczekiwany efekt**: brak efektu na produkt, za to koniec fałszywych odczytów "wzrostu" i "spadku".
- **Właściciel**: `growth-analyst` i `posthog-data-extractor` (definicje), operator (Play Console).
- **Pomiar**: nie dotyczy; kryterium to obecność podziału w kolejnych raportach.

### R5. Zamknąć dziurę po onboardingu: ekran budowania → pierwsza rozmowa · W2 P1 K2 · [hipoteza, n=26]

- **Hipoteza**: 9 z 26 osób, które zobaczyły ekran budowania, nie dochodzi do intro pierwszej rozmowy; prawdopodobnie zamykają aplikację na ekranie oczekiwania albo trafiają na paywall przed rozmową.
- **Działanie**: sprawdzić kolejność ekranów (build → oferta → rozmowa?) i sesje z replayu dla tej grupy (maskowane); dodać `post_onboarding_build_abandoned` lub czas na ekranie.
- **Oczekiwany efekt**: intro rozmowy z 45% do 55% startów; pierwsza rozmowa w 24 h z 42% do 50%.
- **Właściciel**: `ui-ux-designer` (diagnoza), `flutter-mobile` (zmiana i zdarzenie).
- **Pomiar**: `post_onboarding_build_viewed` → `first_conversation_intro_viewed` w nowych kohortach; ocena dopiero przy n ≥ 25 w kroku.

### R6. Sprawdzić lejek zakupowy na iOS · W2 P2 K2 · [hipoteza, n=10]

- **Hipoteza**: na iOS po 03.10 paywall albo się nie pokazuje, albo zakup nie przechodzi: 0 z 10 zakończonych triali kupiło, 0 z 8 osób na App Store 2.0.100 widziało paywall.
- **Działanie**: `database-administrator` porówna `subscription_receipts` z iOS od 03.10 z PostHog; `flutter-mobile` przejdzie ścieżkę oferty na sklepowym buildzie iOS (nie TestFlight) i sprawdzi `post_onboarding_offer_not_shown`.
- **Oczekiwany efekt**: albo znaleziony defekt (wtedy natychmiastowy przychód z iOS, gdzie retencja jest najwyższa), albo potwierdzenie, że to tylko mała próba.
- **Właściciel**: `database-administrator`, `flutter-mobile`.
- **Pomiar**: liczba paragonów iOS na tydzień w Postgres; `paywall_shown` na iOS non-TF.

### R7. Przetestować domyślny plan na paywallu · W1 P1 K3 · [hipoteza, n<25]

- **Hipoteza**: preselekcja planu rocznego nie sprzedaje (0 zakupów rocznych w 60 dniach), a osoby, które same wybierają, biorą miesięczny. Domyślny miesięczny (lub starter) może podnieść start zakupu.
- **Oczekiwany efekt**: `subscription_purchase_started` / `paywall_shown` w górę, kosztem niższego ARPU na zakup. Przy obecnym wolumenie test nie da istotności przez wiele tygodni, więc to zmiana o niskim priorytecie i niskim ryzyku.
- **Właściciel**: `ui-ux-designer` + `flutter-mobile`; decyzja cenowa operatora.
- **Pomiar**: przy ≥ 25 osobach z `paywall_shown` po zmianie.

### R8. Naprawić pętlę FirebaseAuthException na Androidzie · W1 P2 K2 · [dane co do skali]

- **Hipoteza**: zalogowani użytkownicy Androida na `mainPage` dostają powtarzalny błąd tokenu (921 zdarzeń / 11 osób); część żądań może nie przechodzić, co psuje sesję bez widocznego komunikatu.
- **Oczekiwany efekt**: 18 osób w 30 dni bez cichych błędów; możliwy niewielki wzrost retencji Androida.
- **Właściciel**: `flutter-mobile` (odświeżanie tokenu w interceptorze Dio), `integration-devops` (przegląd przepływu auth).
- **Pomiar**: osoby z `client_error` FirebaseAuthException na tydzień, cel < 3.

### R9. Zaproszenie do debriefu w pierwszym tygodniu jako test "aha" · W2 P1 K2 · [hipoteza, n=6]

- **Hipoteza**: debrief po sesji terapii w tyg. 1 zwiększa powrót w tyg. 2 (83% vs 18% na n=6).
- **Działanie**: w planie pierwszego tygodnia dla osób z zadeklarowaną terapią krok "po sesji: debrief"; podział 50/50 flagą, żeby oddzielić przyczynę od selekcji.
- **Właściciel**: `flutter-mobile` (wariant), `growth-analyst` (projekt testu i analiza).
- **Pomiar**: powrót w dniach 7-14 w obu wariantach; minimum 25 osób na wariant przed jakimkolwiek wnioskiem.

---

## 5. Higiena danych: skonsolidowana lista

Priorytet: **P1** = blokuje lub zafałszowuje decyzję, która jest przed nami; **P2** = zaniża jakość pomiaru; **P3** = porządek.

| # | problem | dowód (ekstrakt) | skutek | właściciel | priorytet |
|---|---|---|---|---|---|
| 1 | Zakup liczony podwójnie: `subscription_purchase_completed` z klienta i z backendu (backend zawiera odnowienia i re-weryfikacje) | conversion-paywall, recent-changes (291 zd. / 6 os. w W3) | liczba zakupów w PostHog bezużyteczna | `backend-api`: backend emituje osobne `subscription_renewed` / `subscription_receipt_verified`; klient zostaje jedynym źródłem `purchase_completed` | P1 |
| 2 | Lokalny backend z Windows pisze do produkcyjnego PostHoga (186 zakupów z `$os=Windows`, 08-19..10-14) | conversion-paywall | fałszywe zakupy i zdarzenia backendu | `integration-devops`: pusty lub osobny klucz PostHog w lokalnym `.env`, sprawdzenie środowiska przy starcie | P1 |
| 3 | Brak zdarzeń anulowania i wygaśnięcia subskrypcji; `trial_ended` emituje tylko `converted` (2 zd.), wygaśnięcie triala bez zakupu nie istnieje | conversion-paywall, churn-signals | nie da się policzyć churnu przychodowego ani trial → nie kupił | `backend-api` (`app/tasks/subscriptions.py`, cogodzinna dezaktywacja): `subscription_expired`, `subscription_cancelled`, `trial_ended` {outcome=expired} | P1 |
| 4 | Rozbita tożsamość: 26% rejestracji backendu bez zdarzeń aplikacji pod tym samym `person_id` (tydz. 10-05: 13/33) | acquisition | zawyżeni "nowi", zaniżone konwersje z rejestracji | `flutter-mobile` (`identify` przed wywołaniem rejestracji) + `backend-api` (ten sam `distinct_id`) | P1 |
| 5 | Brak `first_week_plan_shown` (ekspozycji planu) | onboarding-activation, recent-changes | efekt planu pierwszego tygodnia niemierzalny | `flutter-mobile` | P1 (przed premierą w sklepie) |
| 6 | Pushe WEEKLY_SUMMARY_READY i MONTHLY wysyłane do całej bazy (ok. 1800 odbiorców) | feature-usage-voice | koszt, spam, zawyżone `moment.sent` | `data-analytics` | P1 |
| 7 | Semantyka `moment.opened`: 62 zd., tylko 10 łączy się z wysyłką; brak powrotu klienta po "otwarciu" | churn-signals, feature-usage-voice | zawyżona skuteczność pushy | `data-analytics`: ustalić, kiedy backend emituje; do raportów używać `notification_opened` | P2 |
| 8 | Brak `voice_engine=classic` na sesjach Classic | recent-changes, feature-usage-voice | porównanie Live vs Classic niemożliwe | `flutter-mobile` (właściwość zawsze obecna) | P2 (P1 przed jakimkolwiek testem Live) |
| 9 | Zdarzenia ładowania udające świadome otwarcie: `timeline_viewed` (1:1 z onboardingiem), `habit_tracker_viewed`, `character_card_viewed` | onboarding-activation, retention, feature-usage-voice | zawyżone użycie funkcji, fałszywi kandydaci "aha" | `flutter-mobile`: osobne `*_opened` na świadome wejście | P2 |
| 10 | Brak właściwości języka aplikacji (jest tylko `$locale` urządzenia) | onboarding-activation, acquisition | segment językowy przybliżony | `flutter-mobile`: super-property `app_language` | P2 |
| 11 | Brak `subscription_tier` / `is_trial` w czasie (tylko ostatnia wartość na osobie) | retention | retencja per status w dniu wejścia niemożliwa | `flutter-mobile`: super-property na zdarzeniach klienta | P2 |
| 12 | Pętle błędów bez limitu: `subscription_verification_failed` 478 zd. od 1 osoby, `recording_processing_failed` 136 od 1, `paywall_load_failed` 98% od 1 | errors-stability | szum w wolumenach, koszt ingestu | `backend-api` (weryfikacja, nagrania), `flutter-mobile` (klient): deduplikacja lub limit na osobę i godzinę | P2 |
| 13 | FirebaseAuthException na Androidzie (1462 zd. / 18 os., głównie `mainPage`) | errors-stability | możliwy realny defekt sesji | `flutter-mobile` | P1 (to defekt produktu, nie tylko higiena) |
| 14 | `is_expected=false` na 404 profilu i `therapy-context` przy pierwszym uruchomieniu (37 i 36 osób, 100% świeże instalacje) | errors-stability | fałszywy alarm "37 osób z błędem" | `backend-api`: oznaczyć jako oczekiwane, gdy profil nie został jeszcze utworzony | P2 |
| 15 | Brak zdarzenia otwarcia Trends | retention | stickiness Trends niemierzalna | `flutter-mobile`: `trends_viewed` {source} | P3 |
| 16 | `password_reset_failed` i `onboarding_symptom_sync_failed` bez powodu | errors-stability | błędy nie do diagnozy | `flutter-mobile` / `backend-api` | P3 |
| 17 | `voice_chat_ended` (51) > `voice_chat_started` (47) | feature-usage-voice | podwójny koniec lub brak startu | `flutter-mobile` | P3 |
| 18 | 28 zdarzeń zdefiniowanych w kodzie, nigdy niewidzianych (m.in. `first_week_recap_*`, `quick_checkin_*`, `voice_live_fallback`, `voice_moderation_event`) | recent-changes | możliwe martwe zdarzenia albo brak okazji | `flutter-mobile` (test na urządzeniu), `posthog-data-extractor` (weryfikacja po premierze) | P2 |
| 19 | Atrybucja blog → instalacja: 0 zdarzeń w 365 dni; web i aplikacja nie łączą osób | acquisition | wpływ bloga niemierzalny | `integration-devops` (App Store Connect campaigns dla iOS), `flutter-mobile` (weryfikacja `install_campaign` na Androidzie) | P3 |
| 20 | Android: sklep i ścieżka testowa nie do odróżnienia (brak odpowiednika `$is_testflight`) | recent-changes, conversion-paywall | testerzy i license testers liczeni jako realni | `flutter-mobile`: właściwość `install_channel` z Play Install Referrer lub flavour buildu | P2 |

---

## 6. Pytania otwarte dla operatora

1. **Co wywołało skok instalacji z fr/ar/fa między 21.09 a 05.10?** PostHog widzi tylko domyślny referrer Play. Potrzebny odczyt z Play Console: źródła pozyskania wg kraju, wyszukiwane frazy, ewentualne wyróżnienie w sklepie. Od tego zależy, czy to ruch do utrzymania, do odfiltrowania, czy sygnał rynku do zbadania.
2. **Ilu jest dziś realnych płacących i ile było zakupów od 03.10?** Zlecenie dla `database-administrator` (tylko agregaty): liczba aktywnych subskrypcji (`is_active AND end_date > now()`), nowe paragony w `subscription_receipts` na tydzień od 2026-08-16 z podziałem na platformę i produkt, liczba triali od 03.10 i ilu z nich ma paragon po starcie triala. Ostatnia znana wartość: 7 płacących (2026-09-12).
3. **Ile nowych kont tygodniowo w tabeli `users`?** To samo zlecenie: porównanie z 146 `user_registered` w PostHog rozstrzygnie skalę rozbitej tożsamości.
4. **Czy 2.0.110 na Androidzie (9 osób) to etapowe wdrożenie produkcyjne, czy ścieżka testowa?** Odpowiedź w Play Console; od niej zależy, czy plan pierwszego tygodnia ma już jakichkolwiek realnych użytkowników.
5. **Kiedy 2.0.109+ trafi do obu sklepów?** Od tej daty liczę okno pomiaru R1.
6. **Czy wdrożenie v549 (13.09) zatrzymało tylko generację AI dla nieaktywnych, czy także wysyłkę?** PostHog pokazuje 6942 wysyłki podsumowań w 31 dni.
7. **Czy w Google Play są license testers, których zakupy wyglądają jak realne?** Jeśli tak, potrzebna ich lista (bez danych osobowych w raporcie, tylko liczba) do wykluczenia.

---

## 7. Kiedy powtórzyć pomiar

| termin | co mierzymy | warunek |
|---|---|---|
| **2026-10-17** | 7-dniowa aktywacja kohorty 10-10..10-15 (pierwsza rozmowa v2 w sklepie Android) | pełne okno 7 dni dla W4 |
| **2026-10-29** | W2/R14 dla kohorty od 03.10 (wszyscy z pełnymi 14 dniami); pierwsza wiarygodna odpowiedź, czy redesign ruszył retencję | 14 dni od ostatniej osoby z kohorty 10-03..10-15 |
| **14 dni po wejściu 2.0.109+ do obu sklepów** | D1, 2+ dni w tyg. 1, interakcja z planem pierwszego tygodnia (wymaga `first_week_plan_shown`) | premiera sklepowa i potwierdzenie, że zdarzenia płyną |
| **2026-11-02** | D30 dla kohorty z 03.10 | 30 dni od 03.10 |
| **po zebraniu ≥ 25 osób z `paywall_shown` od ostatniej zmiany paywalla** (przy obecnym tempie ok. 3-4 tygodnie) | stopy paywall → start → zakup, plan domyślny | n ≥ 25 w kroku |
| **co miesiąc, stały rytm** | ten zbiorczy raport w skróconej formie: lejek 2a i 2b, segment en vs reszta, MAU ścisłe | |

---

## Zastrzeżenia i pewność

- **Małe liczby**: lejek nowego przepływu to 38 osób, kohorta "aha" 33 osoby, zakupy 6 osób. Każdy odsetek w tych grupach ma szeroki przedział niepewności i jest opisany jako hipoteza.
- **Próg prywatności 5 zamiast 25** przyjęty z ekstraktów i polecenia, bo przy 25 cały raport byłby pusty. Dane dotyczą zachowania w aplikacji i pozyskania (kraj, platforma, język), bez treści zdrowotnych, bez identyfikatorów i bez odczytu tonu czy planu pierwszego tygodnia pojedynczej osoby.
- **Korelacja to nie przyczyna**: związek debriefu, liczby aktywnych dni, platformy i statusu premium z retencją może wynikać z selekcji (kto ma silniejszą potrzebę, ten i robi więcej, i wraca). Przyczynowość rozstrzygnie tylko test z grupą kontrolną (R9).
- **Filtry**: boty po modelu urządzenia (`OnePlus8Pro`, `Pixel 6 Pro`) i testerzy iOS są wykluczeni; nowe modele farm testowych i testerzy Androida mogą przeciekać. Ekstrakt błędów nie stosował filtrów testerów.
- **Ingest od 2026-04-22**; "nowy" = pierwsze zdarzenie od tej daty.
- **Web**: PostHog na stronie ładuje się dopiero po zgodzie na cookies (od 2026-07-26), więc ruch na blogu jest zaniżony; ścieżki web → instalacja nie da się złożyć.
- **Przychód**: żadna liczba zakupów z PostHog nie jest prawdą przychodową; patrz pytanie 2.

## Aneks: gdzie są zapytania

Wszystkie liczby pochodzą z zapytań HogQL zapisanych dosłownie w ekstraktach (`analytics-reports/raw/2026-10-15-*.md`). Najważniejsze odwołania:

- lejek 60 dni, segmenty kraj/język/platforma/źródło: `acquisition.md`, `@@ newuser_cube`, `@@ daily_new_clean`, `@@ registered_merge_check`
- lejek kroków onboardingu, przepływ po 03.10, aktywacja 24 h i 7 d, "aha": `onboarding-activation.md`, `@@ step_funnel`, `@@ cohort_flow`, `@@ act_24h_among_7d_eligible`, `@@ aha`, `@@ aha_capture_parts`
- oś wersji, tygodniowe wskaźniki, kohorty 7 d: `recent-changes-impact.md`, `@@ q1_versions`, `@@ q2_weekly_events`, `@@ q9_new_cohort_7d`
- DAU/WAU/MAU szerokie i ścisłe, kohorty, D1/D7/D30, lifecycle, stickiness: `retention-engagement.md`, `@@ dau_wau_mau_weekly`, `@@ strict_dau_wau_mau_weekly`, `@@ d_retention_pre_post`, `@@ lifecycle_weekly`, `@@ feature_stickiness_28d`
- churn, ostatnie zdarzenia, tydzień 1, pushe re-engagement: `churn-signals.md`, `totals`, `last10_events`, `first_week_compare`, `reengagement_push`
- paywall, plany, trial → płatny, źródła zakupów backendu: `conversion-paywall.md`, lejek per okres, per trigger, trial → płatny, źródła backendowych zakupów
- zasięg funkcji, głos, GPT-Live-1, wysyłki vs otwarcia momentów: `feature-usage-voice.md`, `feature_reach`, `voice_funnel_by_os`, `moment_sent_vs_opened_by_type`
- błędy, endpointy, kohorta 404 profilu, odsetek dotkniętych: `errors-stability.md`, `@@ A_error_events_summary`, `@@ C_api_error_endpoints_14d`, `@@ K_profile404_cohort_14d`, `@@ M_real_error_share_excl_profile404_14d`

Definicje używane w raporcie: **nowy** = pierwsze zdarzenie `posthog-flutter` od 2026-04-22, bez botów i testerów (acquisition); **aktywny ścisły** = zdarzenie klienta po zalogowaniu, bez ekranów splash/welcome/auth i zdarzeń onboardingu (retention); **churn** = 14 dni bez zdarzenia klienta (churn-signals); **R7/R14** = zdarzenie aplikacji w dniach 1-7 / 7-13 po pierwszym dniu.
