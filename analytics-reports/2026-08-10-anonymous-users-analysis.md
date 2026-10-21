# Anonimowi użytkownicy: 66% czy 41%? Rozbiór ściany logowania – Business Insight Report

- **Data**: 2026-08-10
- **Analityk**: growth-analyst
- **Pytanie biznesowe**: Ilu z 430 „nigdy nieuwierzytelnionych" nowych osób app-only to realni ludzie odbici od ściany logowania, gdzie dokładnie utykają i czy da się zrobić w MindSync cokolwiek wartościowego bez konta?
- **Okno danych**: kohorta 2026-05-01 → 2026-07-26 (pierwsze otwarcie aplikacji), zdarzenia obserwowane do 2026-08-10
- **Źródła**: PostHog (proj. 141170, EU) · kod klienta Flutter (read-only) · `analytics-reports/2026-08-10-activation-definition.md` · benchmarki zewnętrzne (Amplitude, CleverTap, Baymard, NN/g, First Round, dokumentacja Google Play/Firebase)
- **Pewność**: **Wysoka** dla dekompozycji 430 i dla odpowiedzi „czy jest wartość przed logowaniem" (dowód w kodzie + cztery niezależne sygnatury w danych); **Średnia** dla szacunków wpływu rekomendacji (scenariusze, nie pomiar)

---

## Executive Summary

- **66% to liczba fałszywa. Realny odsetek odbitych od ściany logowania to 41,0%** (196 z 478 wiarygodnie ludzkich nowych osób), a nie 66,0% (430 z 652).
- **Największa pojedyncza korekta nie ma nic wspólnego z `$identify`: 151 z 430 „anonimowych" (35,1%) to ruch zautomatyzowany, nie ludzie.** 131 osób siedzi na jednym modelu `OnePlus8Pro`, który pojawił się na **28 różnych wersjach aplikacji**, podczas gdy wszystkie realne urządzenia razem widziały tylko 19. To jedna sesja robota na każdy wgrany build.
- **Artefakt `$identify` jest mały: 19 osób (4,0% czystej kohorty)**, bo `AuthCubit` faktycznie woła `Posthog().identify()` i PostHog scala tożsamości. Podejrzenie z planu audytu (17 osób) było trafne co do skali, ale nie to jest przyczyną 66%.
- **Druga korekta: 62 osoby (14,4% z 430) są uwierzytelnione, tylko nie mają eventu.** Mają zdarzenia backendowe (`posthog-python`) i 404 na endpointach wymagających tokenu. To błąd klasyfikacji, nie porzucenie.
- **Ściana logowania stoi przed absolutnie każdą wartością – potwierdzone w kodzie.** Zero wystąpień `signInAnonymously`, `guest`, `demoMode`, `skipAuth` w całym `lib/`. Nowy użytkownik dostaje wymuszone ≥3 s splasha, potem ekran z jednym sloganem i dwoma przyciskami. Onboarding profilujący jest **po** założeniu konta.
- **Gdzie realnie tracimy: 28,2% ginie na splash/welcome, zanim w ogóle zobaczy ekran logowania.** To większy wyciek niż sam ekran auth (23,3%). A ekran welcome **nie emituje żadnego `$screen`**, więc dziś jest analitycznie niewidzialny.
- **Najważniejsza rekomendacja: odfiltrować ruch zautomatyzowany z analityki (R1) i nazwać trasę welcome (R2), zanim ktokolwiek zacznie przebudowywać ścianę logowania.** Bez tego każda decyzja o top-of-funnel jest podejmowana na danych zawyżonych o 26%.

---

## Kluczowe metryki

| Metryka | Wartość raportowana wcześniej | Wartość skorygowana | Odczyt |
|---|---|---|---|
| Kohorta nowych osób app-first (05-01..07-26) | 652 | **478** wiarygodnie ludzkich | -26,7%, ruch zautomatyzowany usunięty |
| „Nigdy nieuwierzytelnieni" | 66,0% (430/652) | **45,0% (215/478)** | ▼ o 21 pkt proc. |
| Realne odbicie od ściany logowania | – | **41,0% (196/478)** | po odjęciu 19 artefaktów tożsamości |
| Uwierzytelnieni | 31,4% (205/652) | **55,0% (263/478)** | ▲ o 23,6 pkt proc. |
| Aktywacja (zapis w 24 h), mianownik: wszystkie nowe osoby | 17,0% (111/652) | **22,6% (108/478)** | ▲; przy medianie rynkowej 5% i P90 21% (Amplitude 2025) to wynik **powyżej P90** |
| Aktywacja, mianownik: uwierzytelnieni | 41,5% (85/205) | **41,1% (108/263)** | → metryka była odporna |
| Dotarcie do ekranu `auth` | – | **71,8% (343/478)** | wyciek 28,2% przed ścianą |
| Konwersja ekranu `auth` → konto | – | **76,7% (263/343)** | wyciek 23,3% na ścianie |

---

## Benchmarki i ich uczciwe ograniczenia

Dwie rzeczy trzeba powiedzieć wprost, zanim padnie jakakolwiek ocena „dobrze/źle".

**Nasz mianownik to „otworzył aplikację", nie „zainstalował".** PostHog nie widzi instalacji bez otwarcia, więc nasze 55,0% uwierzytelnionych **nie jest porównywalne** z często cytowanym „21% instalujących aplikację fintech rejestruje się w pierwszym tygodniu" ([CleverTap, 2023](https://clevertap.com/news/press-release/clevertaps-fintech-benchmark-report-only-1-in-5-users-that-install-fintech-apps-sign-up-within-week-one/)). Nasza liczba jest z definicji wyższa, bo mierzy węższy, lepiej zmotywowany zbiór. Z tego samego badania użyteczna jest natomiast obserwacja, że **70% rejestracji dzieje się w ciągu 75 sekund od pierwszego uruchomienia** – co pokrywa się z naszym rozkładem (160 z 263 uwierzytelnia się w pierwszej godzinie) i oznacza, że decyzja zapada natychmiast albo wcale.

**Porównywalny jest za to wskaźnik aktywacji.** [Amplitude Product Benchmark Report 2025](https://amplitude.com/resources/product-benchmark-report) (dane IX 2023 – IX 2024, 2600+ firm) podaje aktywację pierwszego dnia: **mediana 5%, P90 21%**. Nasze skorygowane **22,6% plasuje się powyżej P90** – co jest ważnym kontrapunktem: **produkt nie ma problemu z aktywacją, tylko z wpuszczeniem ludzi do środka.** Zastrzeżenie: liczby 5%/21% pochodzą z opracowań cytujących ten raport, nie z bezpośrednio zweryfikowanego PDF – przed użyciem w materiale zewnętrznym potwierdzić w źródle.

**Na ile drogo kosztuje wymuszona rejestracja.** Najlepszy dostępny dowód pierwszej ręki to [First Round Review / Duolingo (2017)](https://review.firstround.com/the-tenets-of-a-b-testing-from-duolingos-master-growth-hacker/): Gina Gotthilf (VP Growth) opisuje test A/B, w którym **samo przesunięcie ekranu rejestracji o kilka kroków dalej podniosło DAU o ~20%**. To najbliższy naszej sytuacji cytowalny wynik. [NN/g](https://www.nngroup.com/articles/optional-registration/) potwierdza zasadę („nie zmuszaj do rejestracji przed wartością"), ale **nie podaje żadnej liczby** – każdy, kto cytuje „NN/g mówi X%", zmyśla. [Baymard](https://baymard.com/lists/cart-abandonment-rate) podaje, że **18% porzucających wskazuje „serwis kazał mi założyć konto"** jako powód (4. miejsce; starsze fale badania mówiły 24–26%, dziś publikowane jest 18%) – to e-commerce, nie aplikacja, więc traktować jako rząd wielkości.

**Czego świadomie NIE użyto**, mimo że krąży po internecie: „ściana logowania traci 20–40% użytkowników", „wymóg rejestracji zwiększa porzucenia o 56%", „preferowane logowanie społecznościowe podnosi konwersję o 20–40%", „8,2% wzrostu DAU w Duolingo". **Żadna z tych liczb nie ma źródła pierwotnego** – to blogi SEO cytujące siebie nawzajem. Nie wolno ich wnieść do decyzji.

**Czego po prostu nie ma.** Nie istnieje wiarygodny opublikowany benchmark dla: (a) różnicy Android vs iOS w ukończeniu rejestracji, (b) wpływu obowiązkowej weryfikacji e-mail na konwersję, (c) liczby dostawców logowania społecznościowego. [Corbado (2025)](https://www.corbado.com/blog/social-login-conversion-rate) mówi to wprost. W tych trzech miejscach argumentujemy jakościowo i mierzymy u siebie, zamiast udawać, że mamy punkt odniesienia.

---

## Findings

### F1 – 35% „anonimowych" to ruch zautomatyzowany, nie człowiek · Impact: Critical · Confidence: H (że nie-ludzki) / M (co do źródła)

**Dowody.** Rozbicie 368 osób bez śladu uwierzytelnienia po modelu urządzenia (zapytania 27, 36):

| model urządzenia | osób w kohorcie | anonimowych | % anon | flaga emulatora | śr. czas sesji | dotarło do `auth` |
|---|---|---|---|---|---|---|
| `OnePlus8Pro` | 131 | 124 | **94,7%** | 0 | **223 s** | 122 (93%) |
| `Pixel 6 Pro` | 28 | 27 | **96,4%** | 0 | 45 797 s | 26 (93%) |
| wszystkie realne urządzenia | 478 | 215 | 45,0% | 0 | zróżnicowany | 343 (71,8%) |

Cztery niezależne sygnatury, każda osobno mocna, razem rozstrzygające:

1. **Pokrycie wersji (zapytanie 51) – dowód najsilniejszy.** `OnePlus8Pro` wystąpił na **28 różnych `$app_version`**, `Pixel 6 Pro` na 25, a **wszystkie 556 osób na realnych urządzeniach razem – tylko na 19**. Na wersjach 2.0.38–2.0.43 i 2.0.45–2.0.58 liczba realnych użytkowników wynosi 0 lub 1, a `OnePlus8Pro` ma po 3–7 osób. To jedna automatyczna sesja na każdy wgrany build, **w tym buildy, których nigdy nie zainstalował żaden człowiek**. Żadne zachowanie ludzkie tego nie wyjaśnia.
2. **Jeden model, wiele „osób".** 131 odrębnych `person_id` na dokładnie jednym modelu telefonu, przy 126 osobach Samsunga rozproszonych po wielu modelach (żaden model Samsunga nie ma nawet 7 osób). OnePlus ma ~1–2% udziału w rynku Androida.
3. **Geo / locale / OS.** Wszystkie `OnePlus8Pro`: Android 11, IP w USA, ale **locale rotowane** przez en-NZ (17), en-SG (15), en-US (15), en-BE (12), en-TT (11), en-CA, en-AU, en-NG, en-ZA, en-IE, en-JM, en-PH, en-GB. Prawdziwi użytkownicy nie zmieniają locale między instalacjami; testy lokalizacji tak. `Pixel 6 Pro`: 27 z 28 to Android 12 / en-US / US.
4. **Zachowanie.** Docierają do ekranu `auth` **częściej** niż ludzie (93% vs 71,8%), ale konwertują 11,3% vs 69,6% – robot potrafi kliknąć, ale nie ma konta Google do zalogowania. Odwiedzane ekrany to wyłącznie `splash` (129), `auth` (122), `signUp` (3), `forgotPassword` (3). **Zero ekranów produktowych.** Godzina startu klastruje się o 11:00 UTC (32 osoby).

**Skąd ten ruch pochodzi – tu trzeba być ostrożnym.** Profil zachowania odpowiada dokładnie temu, co Google dokumentuje dla **pre-launch report**: [„instalujemy aplikację na zestawie urządzeń Android w naszym laboratorium... automatycznie uruchamiamy i przeszukujemy ją przez kilka minut"](https://support.google.com/googleplay/android-developer/answer/9842757), raport **„uruchamia się automatycznie dla najpopularniejszych języków"** (rotacja locale), a **„urządzenia testowe znajdują się w Stanach Zjednoczonych"**. Zgadza się też czas (~5 min wg [bloga Google Play dev-rel](https://medium.com/googleplaydev/google-play-expands-its-pre-launch-testing-capabilities-9b51a23077cf), u nas 223 s) i wyzwalacz (jeden przebieg na wgrany release).

**Ale: ani `OnePlus 8 Pro`, ani `Pixel 6 Pro` nie występują w publicznym katalogu Firebase Test Lab** ([zrzut `gcloud firebase test android models list`, luty 2026](https://gist.github.com/akexorcist/c55af0f438f6ddea6a94e26962ea52ba); katalog zawiera Pixel 3/5/6/6a/7/8/9/10 i OnePlus Nord CE3 Lite, CPH2409, CPH2415 – ale nie te dwa modele). Możliwe wyjaśnienia: flota pre-launch report Play różni się od katalogu wystawianego przez `gcloud`; albo jest to inna zautomatyzowana farma urządzeń (np. usługa QA/testowa strony trzeciej lub ruch bez wartości ze sklepu). **To, że ruch nie jest ludzki, jest pewne. To, kto go generuje, wymaga jednego sprawdzenia w Play Console (patrz R1).**

**Ruch ustał po 2026-07-19** (0 osób `OnePlus8Pro` od tygodnia 07-26). Do zweryfikowania przy okazji R1, czy zbiega się to z zatrzymaniem częstych uploadów do Play.

**So what.** Ten ruch zawyżał licznik nowych osób o 26% i był policzony jako „porzucenie". Zatruwa każdy wskaźnik top-of-funnel: akwizycję, aktywację na mianowniku „wszystkie nowe osoby", retencję D1 i lejek onboardingu. **Tydzień 2026-06-21 miał 94 „nowe osoby", z czego 60 to roboty – realnie 34.** Każda decyzja podjęta na tych liczbach była podejmowana na szumie. Uwaga: Google jawnie pisze, że [wyklucza ten ruch z własnych statystyk reklamowych i awarii, ale wykluczenie z narzędzi zewnętrznych zostawia deweloperowi](https://support.google.com/googleplay/android-developer/answer/9844487) – nikt nie zrobi tego za nas.

### F2 – 62 osoby są uwierzytelnione, tylko brakuje im eventu · Impact: High · Confidence: H

**Dowody (zapytania 4, 6, 12, 13).** 62 osoby z kohorty nie mają ani `user_registered`, ani `user_logged_in`, ale **mają zdarzenia backendowe** (`$lib='posthog-python'`). Ich `api_error` to 404 na endpointach wymagających tokenu Firebase: `/api/v1/prep-cards/latest` (22 os.), `/api/v1/debriefs/latest` (21 os.), `/api/v1/health-check/latest` (16 os.). 404 znaczy „ten użytkownik nie ma jeszcze karty", nie „nie ma użytkownika" – gdyby byli nieuwierzytelnieni, dostaliby 401/403 (w całej grupie jest dokładnie 1 zdarzenie 403). Dodatkowo 13 z nich ma zdarzenia backendowe **inne niż błąd** (`reflect_message_sent`, `health_check_completed`, `prep_card_created`, `debrief_created`, `symptom_scored`, `goal_created`), których backend nie wygeneruje bez wiersza użytkownika.

**Przyczyna.** `user_registered` leci wyłącznie z backendu (`posthog-python`) i startuje 2026-05-06, a `user_logged_in` wyłącznie z klienta (`posthog-flutter`). Użytkownik, który założył konto przed 05-06 albo zalogował się na buildzie sprzed instrumentacji, nie zostawia żadnego z tych dwóch zdarzeń, mimo że jest w pełni zalogowany.

**So what.** Definicja „nieuwierzytelniony = brak `user_registered` i brak `user_logged_in`" jest wadliwa. **Poprawna definicja to: brak jakiegokolwiek zdarzenia `$lib='posthog-python'`**, bo backend emituje wyłącznie w kontekście rozpoznanego użytkownika. Ta zmiana sama z siebie zdejmuje 14,4% z rzekomego wycieku.

### F3 – Artefakt `$identify` jest realny, ale mały: 19 osób (4,0%) · Impact: Medium · Confidence: H

**Dowody.** Bezpośredni test przez `$device_id` był niedostępny (**0 z 24 412 zdarzeń klienckich niesie `$device_id`** – zapytanie 8), więc artefakt zmierzono strukturalnie, przez kształt `distinct_id` (zapytanie 11, bez drukowania jakichkolwiek identyfikatorów):

| segment | identyfikator UUID (anonimowy) | identyfikator 28-znakowy (Firebase UID) | wniosek |
|---|---|---|---|
| zarejestrowani (205) | 205 os. na kliencie **i** 205 na backendzie | 60 os. na obu | 145 osób ma **jeden** wspólny id klient+backend; 60 osób ma **dwa** scalone w jedną osobę |
| anon_pure (368) | 368 | 1 | brak scalenia, bo nie było logowania |

**Zero zarejestrowanych osób ma zdarzenia backendowe pod odrębnym `person_id`.** Scalanie działa: `AuthCubit` woła `Posthog().identify()` przy logowaniu i rejestracji (`auth_cubit.dart:43-74`), a aplikacja przekazuje swój `distinct_id` do backendu, więc backend emituje pod tym samym id. Osierocona osoba „sprzed logowania" może więc powstać tylko wtedy, gdy klient zresetuje identyfikator (wylogowanie, reinstalacja) i użytkownik już nie wróci.

Dokładnie tyle widać: **19 z 215 czystych anonimowych ma ślad z obszaru zalogowanego** (zapytania 40, 52) – `onboarding_started` 9 os., `user_logged_out` 7 os., `onboarding_completed` 5 os., `timeline_viewed` 6 os., `debrief_started` 4 os. Onboarding jest w kodzie **po** utworzeniu konta, więc te osoby konto miały.

**So what.** Ostrzeżenie z planu audytu było uzasadnione co do rzędu wielkości (17 vs 19), ale artefakt tożsamości odpowiada za 4,4% problemu, nie za jego istotę. **Nie warto na niego wydawać budżetu inżynierskiego.**

### F4 – Ściana logowania stoi przed każdą wartością; nie da się zrobić nic · Impact: Critical · Confidence: H

**Dowody z kodu (read-only, `mindsync-frontend/mindsync_app/lib/`).**

- Trasa startowa `/` → `SplashScreen` (`navigation/ms_routes.dart:203-207`). Splash **zawsze trwa ≥3 s**, bo animacja jest `await`owana równolegle ze stanem auth (`screens/splash/splash_screen.dart:56-59`, `95`).
- `user == null` → `context.go('/welcome')` (`splash_screen.dart:103-106`). W routerze **nie ma żadnego `redirect:`/strażnika** – nawigacja jest w całości imperatywna.
- Ekran welcome (`screens/welcome/welcome_body.dart`) zawiera: logo, nazwę, **jeden slogan** (`:67-104`), przycisk „Log in" (`:116-126`), przycisk „Sign up" (`:128-141`) i linki Terms/Privacy otwierane w przeglądarce (`:147-196`). **Brak pominięcia, brak trybu gościa, brak podglądu produktu, brak jakiejkolwiek propozycji wartości poza sloganem.**
- Grep po `signInAnonymously`, `isAnonymous`, `guest`, `demoMode`, `skipAuth`, `continueAsGuest` w całym `lib/`: **zero trafień**. Jedyne „skip" są wewnątrz onboardingu, czyli już po koncie.
- Onboarding profilujący (8 kroków + legal gate) jest **po** rejestracji: `sign_up_cubit.dart:144-224` tworzy konto Firebase → wiersz użytkownika → subskrypcję → wysyła mail weryfikacyjny; dopiero `welcome_view.dart:29-34` przechodzi do `/therapy-onboarding` z komentarzem „After successful sign-up, always go to therapy onboarding first".

**Pełna droga do pierwszej wartości na ścieżce e-mail:** splash 3 s → welcome → auth (checkbox Terms obowiązkowy, `auth_body.dart:176-179`) → ekran personalise (nick, przedział wieku, płeć/zaimki) → utworzenie konta → **obowiązkowa weryfikacja mailowa z pollingiem co 5 s** (`sign_up_cubit.dart:221`, `280-289`) → splash sukcesu **4 s** (`welcome_view.dart:24-27`) → legal gate z **dwoma** checkboxami, bez możliwości cofnięcia (`therapy_onboarding_screen.dart:163-180`) → 8 kroków profilowania → WOW → produkt. To kilkanaście ekranów i jedna wymiana maili, zanim aplikacja cokolwiek da.

**Dodatkowe tarcie platformowe.** `animated_google_apple_widgets.dart:100-104`: **iOS pokazuje wyłącznie Apple, Android wyłącznie Google**. Jeden przycisk społecznościowy na platformę, bez zapasowego dostawcy.

**So what.** Na pytanie „czy signup wall stoi przed jakąkolwiek wartością" odpowiedź brzmi: **tak, przed całą, bez wyjątku**. To nie jest kwestia stopnia. Użytkownik podejmuje decyzję o założeniu konta w aplikacji zdrowia psychicznego, mając do dyspozycji jedno zdanie sloganu – i robi to w oknie ~75 sekund, w którym wg [CleverTap](https://clevertap.com/news/press-release/clevertaps-fintech-benchmark-report-only-1-in-5-users-that-install-fintech-apps-sign-up-within-week-one/) zapada 70% takich decyzji.

### F5 – Większy wyciek jest PRZED ekranem logowania, i jest niewidzialny w analityce · Impact: Critical · Confidence: M

**Dowody (zapytania 37, 40, 41).** Czysty lejek ludzki, kohorta 478:

| krok | osób | konwersja kroku | ubytek |
|---|---|---|---|
| otwarcie aplikacji (splash) | 478 | – | – |
| dotarcie do ekranu `auth` | 343 | **71,8%** | **135 osób (28,2%)** |
| założenie konta / zalogowanie | 263 | **76,7%** | 80 osób (23,3%) |

Wśród 215 czystych anonimowych: **115 (53,5%) nigdy nie zobaczyło ekranu `auth`**, 100 zobaczyło i nie założyło konta, a tylko 14 poszło dalej na ekran `signUp`. Profil czasowy: **125 z 215 (58,1%) spędza w aplikacji <15 s przy średnio 1,4 zdarzenia**, czyli splash i wyjście.

**Ale tego kroku nie da się dziś zmierzyć.** Ekran welcome jest zdefiniowany przez `pageBuilder:` bez pola `name:` (`ms_routes.dart:208-228`), a `PosthogObserver` czyta wyłącznie `route.settings.name` – więc **welcome nie emituje żadnego `$screen`** i jego zdarzenia są przypisywane do `$screen_name='splash'`. To samo dotyczy ekranu `wow` (`:384-402`). Spadek „splash → auth" **jest** spadkiem na welcome, ale nie umiemy odróżnić „wyszedł na splashu" od „zobaczył welcome i wyszedł".

**So what.** Priorytetyzujemy dziś ekran logowania, a większa dziura jest jeden ekran wcześniej i nie ma nazwy. To jest tańsze do naprawy niż przebudowa autoryzacji.

### F6 – Android konwertuje o 27 pkt proc. gorzej niż iOS · Impact: High · Confidence: L

**Dowody (zapytanie 37, po usunięciu ruchu zautomatyzowanego).**

| platforma | osób | dotarło do `auth` | uwierzytelnionych | % uwierzytelnionych |
|---|---|---|---|---|
| Android | 449 | 323 (71,9%) | 239 | **53,2%** |
| iOS | 25 | 20 (80,0%) | 20 | **80,0%** |

Trzy zastrzeżenia, każde osłabiające ten wynik: (1) n(iOS)=25 to próba na granicy użyteczności; (2) baza iOS to w ogromnej większości TestFlight i znajomi, więc selekcja pozytywna jest niemal pewna; (3) **nie istnieje żaden opublikowany benchmark różnicy Android/iOS w ukończeniu rejestracji** – przeszukano AppsFlyer, Adjust, CleverTap, Amplitude, Mixpanel i UXCam. Jedyny obronny sygnał kierunkowy to stała przewaga iOS o 2–3 pkt proc. w retencji D1, czyli o rząd wielkości mniejsza niż nasze 27 pkt.

**Geografia (zapytanie 43, tylko kraje z n≥10).** Anonimowi są skoncentrowani: Indie 75 z 215 (34,9% wszystkich odbić, 60,0% kohorty indyjskiej), Bangladesz 18/25 (72,0%), Pakistan 6/10, Rosja 8/12. Dla porównania USA 21/75 (28,0%), Niemcy 2/10, RPA 2/12. **Indie zachowują się inaczej niż reszta świata: docierają do ekranu `auth` częściej (54,7% vs 37,9%), ale prawie nikt nie idzie dalej (4 osoby na ekran `signUp`)** – czyli widzą ścianę i się zatrzymują, zamiast odpaść wcześniej.

**So what.** Różnica Android/iOS jest najprawdopodobniej różnicą składu użytkowników (TestFlight vs organiczny Play), a nie różnicą platformy. Znacząca część „problemu ze ścianą logowania" to ruch organiczny Play Store z rynków, gdzie produkt anglojęzyczny w cenie USD ma niską intencję zakupową. Naprawa ściany podniesie liczbę kont, ale nie w tych krajach przychód. Rozdzielić te dwie rzeczy w celach.

### F7 – 30% odbitych wraca po raz drugi i nadal nie zakłada konta · Impact: Medium · Confidence: H

**Dowody (zapytania 42, 44).** Z 215 czystych anonimowych **150 (69,8%) otworzyło aplikację tylko raz**, ale **65 (30,2%) otworzyło ją 2+ razy** (41 osób dwie sesje, 18 trzy-cztery, 6 pięć i więcej) i mimo to nigdy nie utworzyło konta. Jednocześnie wśród 263 uwierzytelnionych **103 (39,2%) zalogowało się dopiero po pierwszej godzinie** (31 w ciągu doby, 26 w ciągu tygodnia, 46 po tygodniu).

**So what.** Ci ludzie nie są przypadkowi. Wracają, oglądają ścianę i wychodzą – to jest popyt, którego nie umiemy skonwertować, a nie brak zainteresowania. Zarazem fakt, że 39% uwierzytelnia się z opóźnieniem, dowodzi, że decyzja o koncie **da się** odroczyć; produkt już dziś toleruje wielokrotne powroty przed rejestracją.

---

## Analiza przyczyn i hipotezy

- **H1 (potwierdzona, wysoka pewność): większość „anonimowych" nie jest ludźmi ani porzuceniami.** Za: sygnatura 28 wersji aplikacji na jednym modelu, rotacja locale przy stałym IP US, 223 s sesji, 0% konwersji mimo 93% dotarcia do auth; do tego 62 osoby z dowodem uwierzytelnienia po stronie backendu. Przeciw: żaden z dwóch modeli nie występuje w publicznym katalogu Firebase Test Lab, więc konkretne źródło ruchu pozostaje nierozstrzygnięte. **Werdykt: przyjęta co do charakteru (nie-ludzki), otwarta co do źródła.** 151 osób nie-ludzkich + 62 błędnie sklasyfikowane = 213 z 430.
- **H2 (potwierdzona, ale mała): część anonimowych to duplikaty tożsamości sprzed identyfikacji.** Za: 19 osób z ukończonym onboardingiem/wylogowaniem bez `user_registered`. Przeciw: 0 zarejestrowanych osób ma osierocone zdarzenia backendowe, a `identify` jest wołane w `AuthCubit`. **Werdykt: przyjęta, waga 4,0%.**
- **H3 (odrzucona): to problem odkrywalności przycisku rejestracji.** Przeciw: 122 ze 131 robotów i 71,8% ludzi **dociera** do ekranu auth. Przycisk jest znajdowany. **Werdykt: odrzucona.**
- **H4 (nierozstrzygnięta, wymaga instrumentacji): 80 osób, które dotarły do ekranu auth i nie założyły konta, poległo na błędzie logowania, a nie na decyzji.** Za: 6 zdarzeń `FirebaseAuthException` u 5 osób w segmencie anonimowym; Android ma tylko jednego dostawcę OAuth bez zapasowego. Przeciw: próba śladowa; różnica platformowa (F6) jest myląca ze względu na skład próby. **Werdykt: nierozstrzygalna dzisiaj** – `signup_failed` istnieje dopiero od 2026-08-10, a zdarzenia `login_failed` nie ma wcale. To jest luka blokująca (patrz R6).
- **H5 (mocna poszlaka): ściana przed wartością jest przyczyną odbicia na welcome.** Za: 28,2% odpada, zanim zobaczy ekran logowania, przy jednym sloganie jako całej propozycji wartości; 58,1% anonimowych wychodzi w <15 s; kierunkowo zgodne z wynikiem Duolingo (~20% DAU po przesunięciu rejestracji dalej). Przeciw: nie umiemy oddzielić „wyszedł na splashu" od „odrzucił welcome", dopóki trasa welcome nie ma nazwy. **Werdykt: to korelacja, nie dowód przyczynowy** – rozstrzygnie wyłącznie test A/B (R3), poprzedzony R2.

---

## Rekomendacje (wg impact × confidence × effort)

### R1 – Odfiltrować ruch zautomatyzowany z analityki · P0 · effort: XS

Dopóki tego nie zrobimy, każda liczba top-of-funnel jest zawyżona o ~26%, a co gorsza – zawyżona **nierównomiernie w czasie** (60 z 94 osób w tygodniu 06-21, 0 od 07-26), więc trendy tygodniowe są zmyślone.

Trzy kroki, w tej kolejności:

1. **Ustalić źródło (5 minut, przed jakąkolwiek zmianą w kodzie).** Otworzyć Play Console → Testowanie → **Raport przedpremierowy** i odczytać listę urządzeń użytych w przebiegach z maja–lipca. Jeśli są tam `OnePlus 8 Pro` / `Pixel 6 Pro` – sprawa zamknięta. Jeśli nie – mamy do czynienia z inną farmą urządzeń i trzeba to zgłosić jako osobny wątek (możliwy ruch bezwartościowy/fraudowy w Play). Owner: **`integration-devops`**.
2. **Filtr natychmiastowy (analityka, bez deploya).** Transformacja w PostHogu odrzucająca zdarzenia, gdzie `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')` **i** `$geoip_country_code='US'` **i** `$is_emulator=false`. Świadomie odrzuci to garstkę realnych właścicieli tych modeli – dlatego jest to obejście, nie stan docelowy. Owner: **`integration-devops`**.
3. **Rozwiązanie docelowe (klient), jeśli krok 1 potwierdzi pre-launch report.** Na Androidzie odczytać `Settings.System.getString(contentResolver, "firebase.test.lab")` i przy wartości `"true"` nie inicjalizować PostHoga (albo ustawić `$is_test_lab=true`). To [oficjalnie udokumentowany przez Google mechanizm](https://firebase.google.com/docs/test-lab/android/android-studio) dokładnie do tego celu. **Jeśli krok 1 pokaże, że to nie Test Lab, ten mechanizm nie zadziała** i zostaje filtr behawioralny. Owner: **`flutter-mobile`**.

- Efekt: mianownik kohorty spada 652 → 478, aktywacja rośnie 17,0% → 22,6%, tygodniowy szereg akwizycji przestaje mieć fałszywe piki. Pomiar: liczba osób z `$device_model='OnePlus8Pro'` w nowej kohorcie = 0 w ciągu 2 tygodni od wdrożenia.

### R2 – Nazwać trasę `welcome` (i `wow`), żeby największy wyciek przestał być niewidzialny · P0 · effort: XS

Największy ubytek (28,2%, 135 osób w kohorcie) dzieje się na ekranie, który nie emituje ani jednego `$screen`. Dodać `name: 'welcome'` do `GoRoute` w `ms_routes.dart:208-228` oraz `name: 'wow'` w `:384-402`. Uzupełniająco: jawne `auth_screen_viewed`. Owner: **`flutter-mobile`**.
- Efekt: lejek `splash → welcome → auth → konto` domyka się i pozwala rozdzielić „nie doszedł do welcome" od „odrzucił welcome". Pomiar: `$screen_name='welcome'` płynie, a suma przejść splash→welcome→auth się bilansuje w ciągu 2 tygodni.
- **To musi wyprzedzić R3.** Bez tego nie zmierzymy, czy przebudowa ściany cokolwiek dała.

### R3 – Przesunąć ścianę logowania za pierwszą wartość · P1 · effort: zależny od wariantu

Rekomendacja: **zrobić wariant C teraz, wariant A po rozstrzygnięciu RODO.**

**Wariant C (natychmiastowy, tylko frontend): przebudować ekran welcome.** Dziś: logo, jeden slogan, dwa równorzędne przyciski. Docelowo: 2–3 ekrany propozycji wartości (co konkretnie dostaniesz po sesji terapeutycznej), wizualna dominacja „Sign up" nad „Log in", usunięcie wymuszonego 3-sekundowego splasha dla niezalogowanego (`splash_screen.dart:56-59` – nie ma powodu czekać na animację, skoro stan auth jest już znany). Owner: **`ui-ux-designer`** (spec) → **`flutter-mobile`** (implementacja).
- Szacunek scenariuszowy: jeśli dotarcie do `auth` wzrośnie z 71,8% do 85%, przy zachowanej konwersji ściany daje **263 → ~311 kont** w oknie 12,5 tygodnia, czyli **+18%** (+3,8 konta/tydzień). To projekcja, nie pomiar.

**Wariant A (docelowy): anonimowa próba przed rejestracją.** Firebase `signInAnonymously()` na splashu, jeden zapis (quick capture albo jedna wiadomość Reflect) bez konta, potem `linkWithCredential()` podnoszące konto anonimowe do pełnego **bez utraty danych**. Kluczowa zaleta: kontrakt backendowy się nie zmienia – nadal jest Firebase UID i wiersz w `users`, więc koszt serwerowy jest bliski zeru. Owner: **`flutter-mobile`** + **`backend-api`** (weryfikacja tworzenia `users` / `consent_records` dla UID anonimowego).
- **BLOKER do rozstrzygnięcia PRZED implementacją: `security-guardian` musi wydać opinię.** Pierwszy zapis to dane o zdrowiu psychicznym (art. 9 RODO), a dziś zgoda zbierana jest w legal gate **po** rejestracji. Prawdopodobne rozwiązanie: legal gate przenosi się **przed** próbny zapis, co częściowo zjada zysk z wariantu. Bez tej opinii wariantu A nie wolno zaczynać.
- Szacunek scenariuszowy: jeśli odsetek kiedykolwiek uwierzytelnionych wzrośnie z 55,0% do 70%, to **263 → ~335 kont** (+27%). Kierunkowo wsparte przez wynik Duolingo (~20% DAU po przesunięciu rejestracji), ale to inny produkt i inna metryka – traktować jako hipotezę do testu.

**Wariant B: interaktywne demo bez konta.** Największy nakład, najmniejsza pewność zwrotu. Nie rekomendowany na tym etapie.

**Warunek rzetelności:** wariant C wdrożyć jako **A/B 50/50** (flaga PostHog), nie jako zmianę dla wszystkich. Inaczej efekt będzie nie do odróżnienia od naturalnej zmienności tygodniowej (odsetek anonimowych waha się po oczyszczeniu 22,9%–72,0% tydzień do tygodnia, zapytanie 38).

### R4 – Usunąć obowiązkową weryfikację e-mail przed dostępem do produktu · P1 · effort: S

Użytkownik zakłada konto, a potem czeka na ekranie pollingowym co 5 s, aż przyjdzie mail (`sign_up_cubit.dart:221`, `280-289`), po czym dostaje jeszcze 4 s splasha sukcesu. Wpuścić do produktu od razu, weryfikować później (miękki baner) albo zrezygnować z weryfikacji, skoro i tak większość wybiera OAuth (11 z 17 wyborów metody w sierpniu to `oauth`; ścieżka e-mail n<6, suprymowana). Owner: **`flutter-mobile`**, sign-off **`security-guardian`**.
- **Uczciwie: nie istnieje żadna wiarygodna publikacja kwantyfikująca koszt obowiązkowej weryfikacji e-mail** (krążące „5–15%" to marketing dostawców bez badania). Argument jest jakościowy: przerwanie momentum i wymuszone przełączenie do skrzynki pocztowej w oknie, w którym zapada 70% decyzji o rejestracji. Dlatego mierzymy u siebie, a nie obiecujemy liczbę z góry.
- Pomiar: udział osób, które emitują `signup_started`, ale nigdy `onboarding_started`, spada w oknie 4 tygodni.

### R5 – Dać oba sposoby logowania na obu platformach · P2 · effort: S

Android widzi wyłącznie Google, iOS wyłącznie Apple (`animated_google_apple_widgets.dart:100-104`). Użytkownik Androida bez działającego konta Google nie ma alternatywy poza e-mailem z weryfikacją. Owner: **`flutter-mobile`** + **`integration-devops`** (konfiguracja dostawców w Firebase).
- Ograniczenie twarde: [App Store Review Guideline 4.8](https://developer.apple.com/app-store/review/guidelines/#sign-in-with-apple) wymaga „Sign in with Apple" wszędzie tam, gdzie oferowane jest logowanie społecznościowe stron trzecich – czyli na iOS dodanie Google **wymusza** pozostawienie Apple. To już jest spełnione.
- **Nie wdrażać przed R6.** Brak jakiegokolwiek wiarygodnego benchmarku dla liczby dostawców logowania oznacza, że bez własnych danych o porażkach logowania byłaby to zmiana na wyczucie.

### R6 – Zinstrumentować porażki na ekranie logowania · P1 · effort: XS

80 osób dotarło do ściany i odeszło; **nie wiemy, czy zrezygnowały, czy im się nie udało.** `signup_started` / `signup_method_selected` istnieją od 2026-08-05, `signup_failed` od 2026-08-10, a `login_failed` **nie istnieje wcale**. Dodać `login_failed` i `signup_failed` z `error_code` (bez treści błędu i bez adresu e-mail) oraz `auth_screen_viewed` z `tab` (login/signup). Owner: **`flutter-mobile`**.
- Efekt: rozstrzyga H4, czyli decyduje, czy R5 jest w ogóle potrzebne. Pomiar: odsetek `auth_screen_viewed` kończących się `*_failed`, widoczny po 4 tygodniach.

### R7 – Rozdzielić cele akwizycyjne dla Indii/Azji Płd. od reszty · P2 · effort: XS (decyzja)

35% wszystkich odbić pochodzi z Indii, gdzie kohorta dociera do ściany **częściej** niż reszta świata, ale nie przechodzi jej prawie wcale. To ruch organiczny Play Store o niskiej intencji zakupowej dla produktu anglojęzycznego w cenie USD. Owner: **operator** (decyzja) przy wsparciu **`competitive-strategist`**.
- Rekomendacja: raportować „nowe osoby" i „konta" z podziałem rynek docelowy vs reszta, żeby poprawa ściany nie została zmierzona jako wzrost, który nie przynosi przychodu.

---

## Segmenty i kohorty

Dekompozycja pierwotnych 430 „nigdy nieuwierzytelnionych" (kohorta 05-01..07-26):

| grupa | n | % z 430 | werdykt |
|---|---|---|---|
| Uwierzytelnieni, brak eventu (mają zdarzenia backendowe) | 62 | 14,4% | błąd klasyfikacji, **nie porzucenie** |
| Ruch zautomatyzowany – `OnePlus8Pro` | 124 | 28,8% | **nie człowiek** |
| Ruch zautomatyzowany – `Pixel 6 Pro` (podejrzenie) | 27 | 6,3% | **nie człowiek** |
| Nasze emulatory / TestFlight | 2 | 0,5% | ruch własny |
| **Ludzie, którzy nigdy nie założyli konta** | **215** | **50,0%** | **realne odbicie** |
| – w tym artefakt tożsamości (mieli konto, reinstalacja/wylogowanie) | 19 | 4,4% | artefakt `$identify` |
| **= netto odbici od ściany logowania** | **196** | **45,6%** | |

Realne odbicie na czystym mianowniku: **196 / 478 = 41,0%**.

Profil 215 ludzkich anonimowych:

| wymiar | wartość |
|---|---|
| nigdy nie zobaczyli ekranu `auth` | 115 (53,5%) |
| zobaczyli `auth`, nie założyli konta | 100 (46,5%), z czego 14 poszło na `signUp` |
| <15 s w aplikacji, śr. 1,4 zdarzenia | 125 (58,1%) |
| tylko jedna sesja | 150 (69,8%) |
| 2+ sesje, nadal bez konta | 65 (30,2%) |
| Indie / inne rynki wschodzące / reszta świata | 75 / 37 / 103 |

Segmenty poniżej n=6 suprymowane (m.in. rozbicie metody rejestracji e-mail w oknie sierpniowym, `forgotPassword` w części podziałów, iPadOS, `signup_failed`).

---

## Zastrzeżenia i pewność

1. **Ruch zautomatyzowany: charakter pewny, źródło nie.** Cztery zbieżne sygnatury (pokrycie 28 wersji aplikacji, jeden model, rotacja locale przy stałym IP US, zerowa konwersja przy 93% dotarcia do auth) nie zostawiają wątpliwości, że to nie ludzie. Ale **ani `OnePlus 8 Pro`, ani `Pixel 6 Pro` nie figurują w publicznym katalogu Firebase Test Lab (luty 2026)**, więc przypisanie do raportu przedpremierowego Play jest hipotezą, nie faktem. Rozstrzyga to jedno spojrzenie w Play Console (R1 krok 1). Ryzyko filtra po modelu: odrzuci garstkę realnych właścicieli tych telefonów – przy 131 osobach na jednym modelu i ~1–2% udziale OnePlus w rynku uznaję je za marginalne, ale docelowy filtr ma być behawioralny lub oparty na `firebase.test.lab`, nie na modelu.
2. **Ekran welcome nie emituje `$screen`**, więc rozdzielenie „wyszedł na splashu" od „odrzucił welcome" jest dziś niemożliwe. Liczba 28,2% jest sumą obu. R2 to naprawia.
3. **`$device_id` nie jest zbierane** (0 z 24 412 zdarzeń), więc bezpośredni test duplikatów per urządzenie był niedostępny. Artefakt `$identify` oszacowano strukturalnie (kształt `distinct_id` + ślad post-auth), co daje **dolne** oszacowanie: osoba, która zainstalowała aplikację ponownie i nigdy nie weszła głębiej niż ekran auth, jest nieodróżnialna od nowego użytkownika.
4. **n(iOS)=25**, przy niemal pewnej selekcji pozytywnej (TestFlight) i przy braku jakiegokolwiek opublikowanego benchmarku różnicy platformowej w rejestracji. Różnicy Android/iOS **nie należy** traktować jako zmierzonego efektu platformy (F6, pewność Niska).
5. **Korelacja ≠ przyczynowość.** Nie wykazano, że przebudowa ekranu welcome podniesie liczbę kont. Szacunki w R3 to scenariusze przy założeniu stałej konwersji kolejnych kroków. Rozstrzygnie wyłącznie test A/B.
6. **Zmienność tygodniowa jest ogromna** (odsetek anonimowych 22,9%–72,0% tydzień do tygodnia po oczyszczeniu, przy 20–53 osobach na tydzień). Każdy efekt mniejszy niż ~15 pkt proc. będzie nieodróżnialny od szumu bez kilkutygodniowego okna.
7. **Mianownik nie jest instalacją.** PostHog widzi dopiero otwarcie aplikacji, więc nasze wskaźniki nie są porównywalne z benchmarkami „install → signup". Ilu ludzi instaluje i nigdy nie otwiera – nie wiemy i z PostHoga się nie dowiemy (to pytanie do Play Console / App Store Connect).
8. **Korekta wcześniejszych raportów.** `2026-08-10-activation-definition.md`: aktywacja „17,0% (111/652)" powinna brzmieć **22,6% (108/478)**; metryka na mianowniku „zarejestrowani" (41,5%) okazała się odporna (41,1%) i to ona pozostaje właściwa do celów OKR. `2026-08-10-acquisition-collapse.md`: tygodniowy szereg nowych osób app jest zawyżony przez ruch zautomatyzowany w oknie 05-01..07-19 (szczyt: 60 z 94 osób w tygodniu 06-21), natomiast **wniosek tego raportu się utrzymuje** – po oczyszczeniu tygodnie 07-12/07-19/07-26 to 20/24/25 osób, czyli nadal płasko przez granicę consent gate.
9. **Zakres.** Analiza dotyczy wyłącznie osób app-first (`$lib='posthog-flutter'`), z wykluczeniem ruchu marketingowego (`$lib='web'`).

---

## Appendix

### A. Definicje

- **Kohorta**: `person_id` z pierwszym zdarzeniem `properties.$lib='posthog-flutter'` w oknie 2026-05-01..2026-07-26, dolna granica ingestu 2026-04-22 (spójna z raportem aktywacji).
- **Uwierzytelniony (definicja poprawiona)**: `user_registered` **lub** `user_logged_in` **lub** jakiekolwiek zdarzenie `$lib='posthog-python'`. Ostatni warunek jest kluczowy – backend emituje wyłącznie w kontekście rozpoznanego użytkownika.
- **Wiarygodnie ludzki**: `$is_emulator != true` **i** `$is_testflight != true` **i** `$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')`.
- **Ślad post-auth**: dowolne z `onboarding_*`, `user_logged_out`, `timeline_viewed`, `tab_switched`, `character_card_viewed`, `debrief_started`, `between_session_started`, `prep_card_started`, `orca_color_changed`, `subscription_screen_opened`, `notification_opened`, `debrief_failed`, albo `$screen_name` z zestawu ekranów dostępnych tylko po zalogowaniu.

### B. Mapa `$screen_name` → ekran (potwierdzone w kodzie)

| ekran | trasa | `$screen_name` |
|---|---|---|
| Splash | `ms_routes.dart:203-207` | `splash` |
| **Welcome (ściana logowania)** | `ms_routes.dart:208-228`, `pageBuilder` bez `name:` | **żaden – nie emituje** |
| Auth (login i signup w jednym) | `ms_routes.dart:229-237` | `auth` (bez rozróżnienia zakładki) |
| Sign-up (personalise + check-email + sukces) | `ms_routes.dart:238-256` | `signUp` (jedna nazwa na trzy podekrany) |
| Therapy onboarding (9 stron) | `ms_routes.dart:378-383` | `therapyOnboarding` |
| WOW | `ms_routes.dart:384-402`, bez `name:` | **żaden** |

Mechanizm: wyłącznie `PosthogObserver()` (`ms_routes.dart:194`) czytający `route.settings.name`. Brak ręcznych wywołań `Posthog().screen()` w `lib/`.

### C. Weryfikacja emiterów zdarzeń auth

| zdarzenie | `$lib` | pierwsze wystąpienie | osób |
|---|---|---|---|
| `$identify` | posthog-flutter | 2026-04-22 | 135 |
| `user_logged_in` | posthog-flutter | 2026-04-22 | 58 |
| `user_logged_out` | posthog-flutter | 2026-04-22 | 30 |
| `user_registered` | **posthog-python** | **2026-05-06** | 254 |
| `welcome_cta_tapped` | posthog-flutter | **2026-08-04** | 21 |
| `signup_started` / `signup_method_selected` | posthog-flutter | **2026-08-05** | 15 |
| `consent_screen_viewed` | posthog-flutter | 2026-08-05 | 16 |
| `signup_failed` | posthog-flutter | **2026-08-10** | n<6 |
| `login_failed` | – | **nie istnieje** | – |

Wniosek: pełny lejek przedrejestracyjny jest mierzalny dopiero od 2026-08-05, więc kohorta 05-01..07-26 musi opierać się na `$screen`.

### D. Zapytania

Wszystkie wykonane read-only przez `scripts/posthog_query.py --sql-file` (POST `/api/projects/141170/query/`, HogQL). Pliki wsadowe (52 zapytania w 11 partiach): `anon1.sql` (odtworzenie kohorty, wykrycie `$identify`, flagi emulator/testflight, rozkład `distinct_id`), `anon2.sql` (zdarzenia backendowe 62 osób, rozkład miesięczny, test `$device_id`), `anon3.sql` (kształt `distinct_id` per segment, `api_error` per endpoint, ekrany i zdarzenia segmentu anonimowego), `anon5.sql` (ślad post-auth, czas w aplikacji, podział platformowy, trend tygodniowy), `anon6.sql` (producent/model/kraj/wersja, `client_error`), `anon7.sql` (profil robota, lejek splash→auth→konto per segment, nowe zdarzenia sierpniowe), `anon8.sql` (sygnatura locale/OS/godzina, czysty lejek, czysty trend tygodniowy), `anon9.sql` (profil 215 ludzkich anonimowych, sesje, kraje, opóźniona konwersja), `anon10.sql` (wygaśnięcie ruchu robota, metoda rejestracji, przeliczona aktywacja), `anon11.sql` (pokrycie wersji aplikacji, skład 19 artefaktów).

Gotchas HogQL napotkane w tej sesji (do pamięci agenta):
- agregat nie może zawierać agregatu – warunki per-osoba liczyć w podzapytaniu, potem `sum(...)` na zewnątrz;
- alias zewnętrznej agregacji **nie może** powtarzać nazwy kolumny wewnętrznej (`sum(saw_splash) AS saw_splash` → `illegal_aggregation`);
- `greatest()` przyjmuje dokładnie 2 argumenty – dla OR po wielu flagach użyć `if(a+b+c+d>0,1,0)`;
- `$device_id` **nie jest** zbierane przez klienta, więc deduplikacja per urządzenie jest niemożliwa;
- `toUInt8()` nie istnieje, `toInt()` działa (potwierdzenie wcześniejszej notatki).

### E. Surowe agregaty kluczowe

Czysty lejek ludzki, kohorta 478 (05-01..07-26): otwarcie 478 → `auth` 343 (71,8%) → konto 263 (55,0%). Segment anonimowy 215: `splash` 205, `auth` 100, `signUp` 14, `forgotPassword` 2, ślad post-auth 19.

Czysty trend tygodniowy (nowe osoby / uwierzytelnione / % anonimowych): 05-03: 52/25/51,9 · 05-10: 47/31/34,0 · 05-17: 48/37/22,9 · 05-24: 35/21/40,0 · 05-31: 53/32/39,6 · 06-07: 45/22/51,1 · 06-14: 37/17/54,1 · 06-21: 29/22/24,1 · 06-28: 28/16/42,9 · 07-05: 33/15/54,5 · 07-12: 20/9/55,0 · 07-19: 24/7/70,8 · 07-26: 25/11/56,0 · 08-02: 30/26/13,3.

### F. Źródła benchmarków

- [Amplitude Product Benchmark Report 2025](https://amplitude.com/resources/product-benchmark-report) – aktywacja D1: mediana 5%, P90 21% (2600+ firm, IX 2023–IX 2024)
- [CleverTap Fintech Benchmark Report 2023](https://clevertap.com/news/press-release/clevertaps-fintech-benchmark-report-only-1-in-5-users-that-install-fintech-apps-sign-up-within-week-one/) – 21% instalujących rejestruje się w tydzień; 70% rejestracji w ciągu 75 s od pierwszego uruchomienia
- [First Round Review / Duolingo 2017](https://review.firstround.com/the-tenets-of-a-b-testing-from-duolingos-master-growth-hacker/) – przesunięcie ekranu rejestracji dalej: ~20% wzrostu DAU
- [NN/g – Don't Force Users to Register Before They Can Buy](https://www.nngroup.com/articles/optional-registration/) – zasada bez liczby
- [Baymard – powody porzucenia koszyka](https://baymard.com/lists/cart-abandonment-rate) – 18% wskazuje wymóg założenia konta
- [Corbado 2025](https://www.corbado.com/blog/social-login-conversion-rate) – uczciwe stwierdzenie, że benchmark konwersji logowania społecznościowego nie istnieje
- [Apple App Store Review Guideline 4.8](https://developer.apple.com/app-store/review/guidelines/#sign-in-with-apple)
- Google: [raport przedpremierowy](https://support.google.com/googleplay/android-developer/answer/9842757), [interpretacja raportu](https://support.google.com/googleplay/android-developer/answer/9844487), [właściwość `firebase.test.lab`](https://firebase.google.com/docs/test-lab/android/android-studio), [katalog urządzeń Test Lab](https://firebase.google.com/docs/test-lab/android/available-testing-devices), [zrzut listy urządzeń, luty 2026](https://gist.github.com/akexorcist/c55af0f438f6ddea6a94e26962ea52ba)
- Mixpanel 2024 Benchmarks, SplitMetrics/Adapty (konwersja karty sklepu), UXCam (retencja D1 per platforma) – użyte wyłącznie kontekstowo, nie jako podstawa wniosków
