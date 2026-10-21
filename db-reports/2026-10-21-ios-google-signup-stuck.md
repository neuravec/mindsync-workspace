# iOS + Google: czy nowe konta utykają po rejestracji? (prod Postgres, 2026-10-21)

- **Agent**: database-administrator · **Dostęp**: `heroku run -a mindsync --no-tty python < script` (dyno run.5841 i run.6057, oba zakończone same, brak pozostałych dyno `run.*`)
- **Tryb**: wyłącznie SELECT, każde zapytanie w osobnej transakcji READ ONLY z `statement_timeout`, rollback po każdym, nic nie zostało zapisane
- **Kontekst**: `analytics-reports/raw/2026-10-21-release-onboarding.md` sekcja 0: 30/30 rejestracji iOS + Google od 04.10 bez zdarzeń klienta w PostHog, 22 konta z 10-21.10 bez onboardingu, ART9 i rozmów
- **Prywatność**: tylko agregaty, zero adresów, UID, imion i treści. Komórki poniżej 5 kont zapisane jako n<5. To liczniki lejka produktu (wiersz istnieje / nie istnieje), bez danych o zdrowiu.

## Werdykt

Dane wspierają **hipotezę (c), w konkretnej postaci: te konta pochodzą ze STAREJ wersji aplikacji**, nie z obecnego buildu z błędem logowania Google i nie od botów. Te osoby nie "utykają" w obecnym onboardingu: ich aplikacja tego onboardingu w ogóle nie ma i nie ma w niej PostHoga. Część z nich normalnie korzysta ze starego czatu.

Pewność: **wysoka**, że to nie boty (b) i że w obecnym buildzie iOS logowanie Google nie jest zepsute (a). **Średnia** co do systemu: etykieta `ios` jest prawdopodobnie prawdziwa (starsze iPhone'y dostają ostatnią zgodną wersję sprzed podniesienia minimalnego iOS), ale baza nie potrafi tego potwierdzić.

## Skąd baza wie o platformie i dostawcy logowania

- **Dostawca logowania nie jest zapisywany w bazie.** Backend wylicza `auth_provider` tylko do zdarzenia PostHog (`users.py`, z `provider_data` Firebase). Przybliżenie w SQL: domena e-maila (`gmail.com` = Google, `privaterelay.appleid.com` = Apple). Od 20.09 domen innych niż te dwie jest tylko 7, każda pojedynczo.
- **Platforma**: `user_profile.device_type` i `user_subscription_trial.trial_platform`, oba z flagi `is_ios` w `POST` tworzenia subskrypcji. **Brak flagi backend traktuje jako iOS** (`treat_as_ios = is_ios is None or is_ios`, "wsteczna kompatybilność"). Klient wysyła `isIos` dopiero od commita z 2025-09-05.
- **`device_type` zapisuje się tylko wtedy, gdy profil już istnieje** w chwili tworzenia subskrypcji. Obecny klient (od 2026-05-27, "GDPR deferral") tworzy profil dopiero po zgodzie, więc u nowych kont `device_type` zostaje NULL, a platformę niesie tylko `trial_platform`.
- Wersji aplikacji (`app_version`, build) baza nie ma nigdzie. Sprawdzone w `information_schema`: jedyne kolumny "platformowe" to te dwie powyżej i `subscription_receipts.platform`.

Z tego wynika sygnatura, którą da się policzyć. Konto z `device_type` ustawionym przy rejestracji i bez wiersza `user_therapy_context` to konto założone klientem starszym niż 2026-05-27. Dalej nazywam to **kształtem legacy**.

## 1. Kohorty 2026-10-04 do 21.10 (platforma x dostawca x kształt)

| platforma | dostawca | kształt | konta | profil | onboarding (`therapy_context.onboarding_completed`) | ART9 | ≥1 rozmowa z wiadomościami | age_band | token FCM |
|---|---|---|---|---|---|---|---|---|---|
| android | google | current | 34 | 30 | 28 | 17 | 19 | 25 | 9 |
| ios | google | **legacy** | **30** | 30 | **0** | **0** | **9** | **0** | n<5 |
| ios | google | current | n<5 (4) | 4 | 4 | 4 | n<5 | n<5 | n<5 |
| ios | apple | current | n<5 | | wszyscy | wszyscy | wszyscy | | |
| android | inna domena | current | n<5 | | | | | | |

Wszystkie konta iOS + Google, które w PostHog wyglądają na "utknięte", mają kształt legacy (30 z 34). Te 4 konta iOS + Google z obecnego klienta przeszły onboarding w 4 z 4 przypadków i dały zgodę ART9. Logowanie Google na obecnym buildzie iOS działa (mała próba, część z nich może należeć do zespołu).

Tygodniowo (iOS + Google, wszystkie kształty): tydzień od 05.10: 14 kont, 1 z onboardingiem; od 12.10: 14 i 1; od 19.10: 6 i 2. Android + Google w tych tygodniach: 16/14, 13/12, 2/1.

## 2. Profil kont iOS + Google legacy (30 kont, 04-21.10)

**To nie wygląda na automat:**
- Odstępy między kolejnymi rejestracjami: 0 poniżej 15 min, 4 w przedziale 15-60 min, 11 w 1-6 h, 11 w 6-24 h, 7 powyżej doby. Brak serii.
- Godziny UTC rozłożone na 18 różnych godzin, dni tygodnia od 3 do 7 kont każdy.
- Domeny: 100% `gmail.com`. Kształt adresu (długość lokalnej części, ciągi cyfr, aliasy `+`) taki sam jak u Androida z Google. Brak domen testowych (Test Lab, App Review, mailinator itp.).
- UID Firebase zawsze 28 znaków, czyli zwykłe konta Firebase.
- Strefa czasowa ustawiona przez urządzenie u 17/30 (format offsetu `UTC+N`). Wyraźne skupienie w UTC+5 i UTC+6 (9 kont: Azja Centralna, Bangladesz, Pakistan), dalej UTC+3. PostHog również pokazywał KG i BD.
- Pola profilu wypełnione ręcznie: imię 20/30, płeć 18/30 (tylko FEMALE/MALE, stara lista bez 5 opcji).

**To wygląda na stary klient:**
- `device_type` zapisany przy rejestracji (profil powstał przed subskrypcją). Tak działał klient sprzed 2026-05-27.
- `age_band` 0/30 (pole doszło w tym samym commicie 05-27), `orca_name` 0/30, `notification_interests` 0/30, zero wierszy `consent_records` jakiegokolwiek typu, zero `user_therapy_context`.
- Rozmowy mają wyłącznie typ `JOURNAL` (14 rozmów, 9 osób). Obecni klienci w tym samym oknie tworzą tylko `REFLECT` (29 rozmów, 24 osoby).
- Zero zdarzeń klienta w PostHog. SDK PostHog trafił do aplikacji 2026-04-22.

**Czy wracają:** 9/30 ma rozmowę z wiadomościami (1-9 wiadomości: 6 osób, 10+ wiadomości: n<5), rozmowę w kolejnym dniu po rejestracji n<5. `users.last_login` po dniu rejestracji: n<5. Uwaga: `last_login` ma `onupdate=now()`, czyli zmienia się przy każdym UPDATE wiersza `users`, a nie przy logowaniu. Sygnał słaby, ale u Androida z Google wygląda podobnie (n<5), więc nie różnicuje grup. Trial rejestracyjny (`granted_via=signup_trial`) mają 34/34 iOS i 31/34 Android, aktywny dziś: 11 iOS, 3 Android.

## 3. Od kiedy (miesięcznie, kształt legacy od 2025-06)

| miesiąc | android legacy | ios legacy | ios current |
|---|---|---|---|
| 2026-03 | 45 | n<5 | n<5 |
| 2026-04 | 34 | n<5 | n<5 |
| 2026-05 | 16 | n<5 | 10 |
| 2026-06 | 13 | n<5 | n<5 |
| 2026-07 | n<5 | 0 | 0 |
| 2026-08 | 0 | 7 | 0 |
| 2026-09 | 0 | 13 | 0 |
| 2026-10 (do 21.10) | 0 | 31 | 4 |

Dzienny przebieg iOS + Google od 01.08: konta pojawiają się pojedynczo od 08.08, każdy dzień z onboardingiem 0, aż do 05.10 (pierwsze konto iOS + Google z onboardingiem). **Nie ma momentu, w którym "seria udanych" przechodzi w porażki.** iOS + Google z obecnego klienta to w ostatnich miesiącach pojedyncze konta, a kształt legacy rośnie od sierpnia (7, 13, 31 kont na miesiąc). Data 04.10 z raportu PostHog to początek okna analizy, nie początek zjawiska.

Android legacy znika w lipcu, iOS legacy pojawia się w sierpniu. Na Androidzie stare buildy prawdopodobnie wygasły (przyczyny baza nie pokazuje). iOS 2026-04-30 podniósł minimalną wersję systemu z 13.0 na 16.0 (`IPHONEOS_DEPLOYMENT_TARGET`, commit `a161b1d`). iPhone'y z iOS 13-15 (6s, 7, SE 1. gen. i nieaktualizowane 8/X) dostają w App Store "ostatnią zgodną wersję", czyli build sprzed 30.04. Pasuje to do geografii (rynki z dużym udziałem starszych iPhone'ów) i do braku PostHoga.

## Hipotezy

- **(a) Bug po logowaniu Google na iOS w obecnym buildzie**: **nie wspierana.** 4/4 konta iOS + Google z obecnego klienta przeszły onboarding i zgodę ART9. 30 "utkniętych" ma sygnaturę innego, starego klienta, a 9 z nich rozmawia w starym czacie, więc nie stoją za ekranem logowania.
- **(b) Konta testowe / boty**: **nie wspierana.** Brak serii czasowych, brak domen testowych, ręcznie wypełnione imię i płeć, strefy czasowe z urządzeń, realne rozmowy.
- **(c) Błąd pomiaru**: **wspierana.** PostHog ich nie widzi, bo stary build nie ma SDK. Backend nie widzi u nich onboardingu, bo stary build go nie ma. Liczba "0/22 onboarding" mierzy wersję aplikacji, nie zachowanie ludzi. Etykieta `ios` jest raczej prawdziwa (wariant ze starymi iPhone'ami). Alternatywy baza nie wyklucza: bardzo stary build Androida sprzed 2025-09-05 (z APK z serwisów lustrzanych) nie wysyła `is_ios` i backend oznaczyłby go jako iOS. Słabszy wariant, bo oczekiwalibyśmy wtedy też kont z typowymi dla takiego buildu cechami sprzed września 2025.

Dlaczego tylko Google, a nie Apple: na starszym buildzie logowanie Apple może być rzadziej wybierane albo działać gorzej. Baza tego nie rozstrzyga (iOS + Apple legacy: n<5 w całej historii).

## Ryzyka, które to odsłania (handoffy)

1. **Zgoda ART9 (GDPR Art. 9)**: 9 kont z tego okna (i więcej historycznie) prowadzi rozmowy o zdrowiu psychicznym bez żadnego wiersza w `consent_records`. Backend nie wymusza zgody po stronie serwera, opiera się na kliencie. Owner: **`backend-api`** (serwerowa bramka zgody na tworzenie rozmów i wiadomości albo wymuszona aktualizacja), przegląd: **`security-guardian`**.
2. **Brak wersji klienta w danych**: dopisać zapis `app_version` + `platform` (nagłówek z Dio) na rejestracji i przy `POST` subskrypcji, a brak `is_ios` logować jako `unknown` zamiast domyślnego iOS. Owner: **`backend-api`** (kolumny + migracja idempotentna), **`flutter-mobile`** (nagłówek).
3. **Minimalna obsługiwana wersja (force update)**: stary build nie ma onboardingu, zgód ani płatności w obecnym kształcie. Decyzja produktowa: ekran "zaktualizuj" sterowany z backendu albo świadome utrzymanie starego builda. Owner: **lead + `integration-devops`**.
4. **Raporty lejka**: wykluczać kształt legacy (albo raportować osobno), inaczej iOS zaniża każdy wskaźnik aktywacji.

## Jak potwierdzić wariant iOS (poza bazą)

- App Store Connect, Analytics: pobrania i sesje według wersji aplikacji i wersji iOS w okresie 08-10.2026; czy istnieje ruch na buildzie sprzed 30.04 i na iOS < 16.
- Logi routera Heroku przy `POST /api/v1/users/...` (user agent `Dart/... (dart:io)` nie mówi o OS, więc to wymaga nagłówka z punktu 2).

## Zapytania

Skrypty budowane z plików `build.py` i `build2.py` (scratchpad sesji `a7-db`). Wspólne CTE `b` (fragment):

```sql
SELECT u.id, u.created_at, u.last_login, u.activated_at,
  CASE WHEN u.email IS NULL THEN 'no_email'
       WHEN lower(split_part(u.email,'@',2))='privaterelay.appleid.com' THEN 'apple_relay'
       WHEN lower(split_part(u.email,'@',2)) IN ('gmail.com','googlemail.com') THEN 'gmail'
       ELSE 'other_domain' END AS prov,
  coalesce(p.device_type, t.trial_platform, '(none)') AS plat,
  coalesce(tc.onboarding_completed,false) AS onb, (tc.id IS NOT NULL) AS has_tc,
  EXISTS (SELECT 1 FROM consent_records c WHERE c.user_id=u.id AND c.consent_type='ARTICLE9_HEALTH') AS art9,
  EXISTS (SELECT 1 FROM conversations cv JOIN messages m ON m.conversation_id=cv.id WHERE cv.user_id=u.id) AS msg,
  EXISTS (SELECT 1 FROM user_fcm_token f WHERE f.user_id=u.id) AS fcm, ...
FROM users u
LEFT JOIN user_profile p ON p.user_id=u.id
LEFT JOIN user_preferences pr ON pr.user_id=u.id
LEFT JOIN user_subscription_trial t ON t.user_id=u.id
LEFT JOIN user_subscription s ON s.user_id=u.id
LEFT JOIN user_therapy_context tc ON tc.user_id=u.id
WHERE u.created_at >= :since
```

Kształt legacy: `p.device_type IS NOT NULL AND tc.id IS NULL`. Pozostałe zapytania: agregaty po tygodniu/dniu/miesiącu, histogram odstępów (`lag()` po `created_at`), rozkład godzin i dni, prefiks strefy czasowej, kształt subskrypcji (`subscription_type`, `granted_via`, `is_active`), wypełnienie pól profilu i preferencji, typy zgód i rozmów, kształt lokalnej części e-maila (tylko kategorie: długość, ciąg cyfr, alias). Wszystkie z `GROUP BY`, żadne nie zwraca wierszy per konto.

Uwaga do schematu: `users.created_at` i `users.last_login` są na prodzie `timestamp without time zone` (model deklaruje `timezone=True`). Znany dryf, bez wpływu na te zapytania.
