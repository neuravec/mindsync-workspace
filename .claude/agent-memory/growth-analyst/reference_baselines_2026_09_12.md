---
name: baselines-and-unit-economics-2026-09-12
description: Full-product baseline as of 2026-09-12 – retention (D1 7.5/D7 4.0/D30 0.8), revenue truth (7 real payers), AI cost structure (97% spent on push-generated content), break-even math, and the traps that make each number easy to misread
metadata:
  type: reference
---

# Baseline 2026-09-12 – retencja, monetyzacja, jednostkowa ekonomia

Źródła: `db-reports/2026-09-12-subscription-revenue-30d.md` + `analytics-reports/raw/2026-09-12-usage-retention-monetization-extract.md`.
Raport wynikowy: `analytics-reports/2026-09-12-diagnoza-retencja-monetyzacja.md`.

## Baseline liczbowy (okno 2026-08-13 .. 2026-09-12)

| Metryka | Wartość |
|---|---|
| Konta ogółem | 1855 |
| MAU (app, po odfiltrowaniu botów) | **127** |
| Konta dotykane przez backend (crony) | 1874 (**14,8x MAU**) |
| D1 / D7 / D30 | **7,5% / 4,0% / 0,8%** (24/319, 12/303, 2/244) |
| One-and-done 90d | 66,2% (253/382) |
| Jeden aktywny dzień w 30d | 68,5% (87/127) |
| Ukończenie onboardingu | 76,7% (43→33), 9 kroków, minimalny drop między krokami |
| Stickiness DAU/WAU | 26-31% |
| Konta bez ani jednej rozmowy | 67,9% (1259/1855) |
| Rejestracje | ~13/tydz., płasko od 12 tygodni |
| Nowe person w PostHogu | ~25/tydz. |
| Aktywne premium | 18 (0,97%); realny zakup **7**, signup_trial 8, promo 2, null 1 |
| Zakupy 30d | **2** (Apple 08-19, Google 09-07, oba `premium_m_01`) |
| Zakupy w historii | 60 od 2025-03; płasko 1-3/mies od marca 2026 |
| Koszt AI 30d | **112,13 USD** (~449 zł @4 PLN/USD) |
| Open rate push | **1,4%** (26/1815 odbiorców), 0,19% event-do-eventu |

## Cztery liczby, które rozstrzygają diagnozę (używaj ich jako punktu wyjścia)

1. **Retencja płacących = 7/37 = 18,9%.** 37 kont kiedykolwiek miało premium z `granted_via='purchase'`,
   dziś aktywnych 7. **To jest dowód, że problem NIE jest w paywallu ani w cenie** – ludzie, którzy już
   zapłacili, też odchodzą. Zawsze podnoś tę liczbę, zanim ktoś zaproponuje pracę nad monetyzacją.
2. **96,8% kosztu AI idzie na treść generowaną DLA użytkowników, nie na ich życzenie.**
   NOTIFICATION 91,96 + WEEKLY_SUMMARY 11,88 + MONTHLY_AUDIT 4,70 = 108,54 z 112,13 USD.
   Terapeutyczna AI (`CONVERSATION`) = **0,07 USD**. Dostarczanie wartości jest tanie; drogi jest
   mechanizm, który nie działa.
3. **4319 uderzeń w pusty stan vs 173 zdarzenia "Your Session" = 25:1.** Trzy najczęstsze `api_error`
   to zaprojektowane 404 na `/prep-cards/latest` (58 os., 45,7% MAU), `/debriefs/latest` (51 os.),
   `/health-check/latest` (47 os.). Ludzie szukają treści 25x częściej, niż ją tworzą.
4. **5 z 7 wyświetleń `paywall_shown` przyszło z `drawer_menu`/`settings`**, tylko 2 z bramki premium.
   Bramki free są ustawione POWYŻEJ tego, gdzie użytkownik dochodzi (debriefy 5/mies vs mediana 2,5
   zdarzenia Your Session; nagrania 2 free vs mediana 1,0 przy 7 osobach w 30d). Zaostrzanie free
   ani podnoszenie ceny nic nie da.

## Jednostkowa ekonomia i break-even (wzór do ponownego użycia)

Koszty ~830 zł/mies = AI 449 (zmierzone) + Heroku ~200 + Loops ~180 (dwa ostatnie to szacunek operatora, niezweryfikowane).

- Koszt/MAU = 6,53 zł · Koszt/płacącego = **118,43 zł** · Koszt/konta z rozmową w 30d = 33,16 zł
- **Netto dla wydawcy = cena_brutto / 1,23 × (1 - prowizja)**; VAT 23% pobiera sklep, prowizja 15%
  (program dla małych wydawców) lub 30%. Np. 39,99 zł → 27,64 zł netto @15%.
- Break-even @830 zł, 15% prowizji: 19,99→61 subów, 29,99→41, 39,99→**31**, 49,99→25. Masz 7.
- Po cięciu kosztów do ~450 zł: 39,99→**17** subów.
- **Cena `premium_m_01` NIEZNANA** – `subscription_receipts` nie ma kolumny kwoty ani waluty.
  Odczytać z App Store Connect / Play Console.
- **Killer argument:** przy konwersji 0,38% bazy, 31 płacących wymaga 8158 kont = +6300 rejestracji
  = **9,3 roku** przy 13/tydz. Przy 127 MAU break-even wymaga, żeby **24,4% MAU płaciło**
  (benchmark freemium: 2,2% mediana, górne 25% robi 10-15%). Monetyzacja nie jest dźwignią przy tej skali.
- Średni czas życia użytkownika ≈ MAU / nowi_na_miesiąc = 127/108 ≈ **1,2 miesiąca**.
  Do 560 MAU (break-even przy 450 zł i 3% konwersji) potrzeba 5,2 mies. życia, czyli 4,4x.

## Pułapki interpretacyjne (sprawdzone w tej analizie)

- **`moment.sent` do 1815 odbiorców ≠ 1815 aktywnych.** Crony wysyłają do całej historycznej bazy.
  Ta sama pułapka co `$lib` – nigdy nie raportuj populacji backendowej jako aktywnych.
- **Ściana rejestracji ~50%** liczona przez porównanie PostHog (~25 nowych person/tydz.) z Postgresem
  (~13 rejestracji/tydz.). Dwa systemy, różny dedup, okna przesunięte o tydzień → **rząd wielkości
  40-55%, nie precyzyjne 50%**. Zgodne z wcześniejszym pomiarem 41% z raportu 2026-08-10.
- **`conversation_*` MARTWE od 2026-08-11** (0 zdarzeń w 30d). Dopóki nie wiadomo, czy to urwana
  instrumentacja czy świadome wycofanie, **liczba "67,9% kont bez rozmowy" ma niepewną interpretację**.
  To jedyna luka, która może odwrócić główną liczbę raportu. Sprawdzić przed następną analizą.
- **W0 kohorty n=102: `workspace` 0,0% i `recording` 0,0% wśród 97 odpadających**, przy 33% i 5,5%
  adopcji w całym MAU → to są powierzchnie WYŁĄCZNIE dla wracających, nowy użytkownik ich nie widzi.
- **`subscription_purchase_completed` z PostHoga (5 os.) ≠ 2 paragony z Postgresu.** Prawda przychodowa
  to zawsze `subscription_receipts`.
- **Trial 4-dniowy jest KRÓTSZY niż pętla produktowa** (sesja terapeutyczna raz na 1-2 tygodnie) → część
  użytkowników nigdy nie doświadcza premium w czasie trialu. Nadawany backendowo (`granted_via='signup_trial'`),
  odrębnie od `'purchase'` → prawdopodobnie brak automatycznego momentu obciążenia na końcu. Do potwierdzenia.
- **Górna granica trial→paid = ≤37/554 = ≤6,7%** (krzyżowanie `had_trial=true` z kontami `purchase`).
  Nie porównuj do benchmarku 30-50% bez zastrzeżenia – tamten dotyczy trialu sklepowego z kartą.

## Luki pomiarowe blokujące decyzje (stan 2026-09-12)

`trial_started`/`trial_ended` nigdy nie płynęły · `trial_outcome` NULL w 100% (1852/1852, błąd zapisu)
· `paywall_shown` dopiero od 2026-08-16, 10 zdarzeń w historii, systematycznie zaniża (7 vs 15 dla
`subscription_screen_opened`) · brak eventu odbicia od bramki z `trigger_feature` · **Habit Tracker zero
instrumentacji** (widget na `mainPage`, brak nawet `$screen`) · `subscription_receipts` bez kwoty, waluty
i środowiska (sandbox vs production nierozróżnialne) · `moment.opened` bez `moment_type` · brak
potwierdzenia doręczenia push (`notification_received` tylko w foreground) · 93% `api_error` to
zaprojektowane puste stany zasłaniające realne 404 na `/users/get_user_profile_and_subscription` (38 os.)
i `/users/therapy-context` (40 os.).

## Wybrana metryka North Star do cotygodniowego przeglądu

**D1 retencja, średnia krocząca z 4 tygodni.** Dziś 7,5%, próg 15% do 2026-12-12, poniżej 12% →
tryb utrzymaniowy. Powód: najwyżej w łańcuchu przyczynowym (92,5% znika przed zobaczeniem oferty),
odpowiada w 48h, nie da się jej oszukać cięciem kosztów ani spamem, i celują w nią wszystkie
rekomendacje naprawcze. **Pojedynczy tydzień jest bezwartościowy** (25 nowych/tydz. → 7,5% to 2 osoby);
czytać wyłącznie 4-tygodniowo (n≈100).

## Diagnoza kierunkowa (teza do przetestowania w kolejnych analizach)

MindSync nie ma złego pomysłu – ma **niedopasowanie częstotliwości**. Pętla produktowa (prep card →
sesja terapeutyczna → debrief) ma okres 1-2 tygodni, a forma (apka mobilna) wymaga pętli dziennej.
Adopcja to potwierdza: dwie najpopularniejsze funkcje to powierzchnie **czytania** (timeline 52%,
workspace 33%), wszystko, co wymaga wysiłku, siedzi w 5-22%. Jedyna funkcja z dzienną pętlą
(Habit Tracker, wdrożony 2026-09-02) jest kompletnie niezmierzona. **Zmierz ją, zanim ktokolwiek
podejmie decyzję kierunkową.**

## Benchmarki użyte (zweryfikowane 2026-09-12)

D1 ~26-35% / D7 ~15-20% / D30 ~3-4% health-fitness: businessofapps.com/data/health-fitness-app-benchmarks,
uxcam.com/blog/mobile-app-retention-benchmarks · download→paid 2,2% mediana freemium, górne 25% robi
10-15%: revenuecat.com/state-of-subscription-apps-2025, userpilot.com/blog/freemium-to-premium ·
trial→paid 30-50% (trial sklepowy): adapty.io/blog/trial-conversion-rates-for-in-app-subscriptions ·
push open rate ~7,8% średnia, 14,2% health/iOS: airship.com, pushwoosh.com/blog/push-notification-benchmarks.
