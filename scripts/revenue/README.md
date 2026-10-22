# Przychody: App Store Connect i Google Play

Dwa skrypty tylko do odczytu, pobierające raporty sprzedaży, subskrypcji i finansowe:

- `asc_reports.py`: App Store Connect API (Sales and Trends, Payments and Financial Reports)
- `play_reports.py`: bucket Cloud Storage z raportami Google Play Console

Wszystkie dane trafiają do `analytics-reports/raw/revenue/`, który jest w `.gitignore`. **Danych finansowych nie commitujemy.** Klucze (`.p8`, `.json`) i plik `.env` też są ignorowane przez git.

## 0. Instalacja zależności (jednorazowo)

Z katalogu głównego workspace (`Heroku`):

```powershell
pip install --user "pyjwt[crypto]"            # App Store Connect (podpis JWT ES256)
pip install --user google-auth requests       # Google Play (token konta serwisowego)
Copy-Item scripts/revenue/.env.example scripts/revenue/.env
```

Potem uzupełnij `scripts/revenue/.env` według kroków poniżej.

## 1. App Store Connect: konfiguracja (ok. 5 min)

Potrzebne jest konto z rolą **Admin** w App Store Connect (tylko Admin może generować klucze zespołowe).

1. Wejdź na <https://appstoreconnect.apple.com> -> **Users and Access**.
2. Zakładka **Integrations** -> w menu po lewej **App Store Connect API**.
3. Sekcja **Team Keys**. Jeśli to pierwszy klucz, kliknij **Request Access** i zaakceptuj warunki.
4. Kliknij **Generate API Key** (lub **+**). Nazwa np. `mindsync-revenue-readonly`, rola **Finance** (daje dostęp do raportów finansowych i sprzedaży; sama rola **Sales** wystarczy tylko do `sales` i `subscriptions`). Kliknij **Generate**.
5. Przy nowym kluczu kliknij **Download API Key**. Plik `AuthKey_XXXXXXXXXX.p8` **można pobrać tylko raz**. Zapisz go w `scripts/revenue/` (bez zmiany nazwy), a kopię zapasową w menedżerze haseł.
6. Skopiuj **Issuer ID** (widoczny nad listą kluczy) do `ASC_ISSUER_ID` w `.env`.
7. Skopiuj **Key ID** nowego klucza do `ASC_KEY_ID`.
8. Vendor Number: **Payments and Financial Reports** (strona główna App Store Connect) -> numer w lewym górnym rogu (pod nazwą firmy). Wpisz do `ASC_VENDOR_NUMBER`.
9. Jeśli plik `.p8` leży gdzie indziej niż `scripts/revenue/AuthKey_<KEY_ID>.p8`, podaj ścieżkę w `ASC_PRIVATE_KEY_PATH`.

Test i pobieranie:

```powershell
python scripts/revenue/asc_reports.py check                        # wypisze aplikacje: klucz działa
python scripts/revenue/asc_reports.py sales --date 2026-10-20      # raport dzienny
python scripts/revenue/asc_reports.py sales --month 2026-09        # raport miesięczny
python scripts/revenue/asc_reports.py subscriptions --date 2026-10-20
python scripts/revenue/asc_reports.py finance --month 2026-09      # region ZZ (wszystkie waluty, podsumowanie)
python scripts/revenue/asc_reports.py finance --month 2026-09 --type FINANCE_DETAIL   # region Z1
```

Wynik: `analytics-reports/raw/revenue/asc/<sales|subscriptions|finance>/` (surowy `.tsv` oraz `.csv`).

Uwagi:
- "Brak raportu dla ..." to nie błąd: Apple zwraca 404, gdy danego dnia nie było sprzedaży albo raport jeszcze nie powstał. Raport dzienny jest zwykle gotowy następnego dnia rano czasu pacyficznego.
- `finance --month` to **miesiąc fiskalny Apple**, który nie pokrywa się dokładnie z kalendarzowym.
- Raport `subscriptions` jest dostępny tylko dziennie.

## 2. Google Play: konfiguracja (ok. 10 min + do 24 h oczekiwania)

### 2a. Konto serwisowe w Google Cloud

1. Wejdź na <https://console.cloud.google.com/iam-admin/serviceaccounts?project=mindsync-8f534> (może być projekt `mindsync-8f534`).
2. Kliknij **Create service account**. Nazwa np. `play-reports-readonly`. Kliknij **Create and continue**, role w projekcie **pomiń** (nie są potrzebne), kliknij **Done**.
3. Kliknij w utworzone konto -> zakładka **Keys** -> **Add key** -> **Create new key** -> **JSON** -> **Create**.
4. Pobrany plik zapisz jako `scripts/revenue/play-service-account.json` (albo podaj ścieżkę w `PLAY_SERVICE_ACCOUNT_JSON`).
5. Skopiuj adres e-mail konta serwisowego (kończy się na `@mindsync-8f534.iam.gserviceaccount.com`).

### 2b. Zaproszenie w Play Console

1. Wejdź na <https://play.google.com/console> -> **Users and permissions** (Użytkownicy i uprawnienia).
2. Kliknij **Invite new users**, wklej e-mail konta serwisowego.
3. Zakładka **Account permissions**: zaznacz **View app information (read only)** oraz **View financial data, orders, and cancellation survey responses**.
4. Kliknij **Invite user**, potem potwierdź.
5. Uprawnienia do bucketu z raportami propagują się **do ok. 24 h**. Do tego czasu skrypt może zwracać HTTP 403.

### 2c. Identyfikator bucketu

1. Developer ID to liczba w adresie Play Console: `play.google.com/console/u/0/developers/<TEN_NUMER>/...`. Wpisz ją do `PLAY_DEVELOPER_ID` (bucket = `pubsite_prod_rev_<TEN_NUMER>`).
2. Pewniejszy sposób: Play Console -> **Download reports** -> **Financial** (lub **Statistics**) -> przycisk **Copy Cloud Storage URI**. Wklej skopiowany adres (`gs://pubsite_prod_...`) do `PLAY_BUCKET`. Ma on pierwszeństwo przed `PLAY_DEVELOPER_ID`, co ważne, bo nowsze konta mogą mieć bucket o innej nazwie.

Test i pobieranie:

```powershell
python scripts/revenue/play_reports.py check                       # pierwsze 20 plików w buckecie
python scripts/revenue/play_reports.py list --prefix earnings/
python scripts/revenue/play_reports.py pull --month 2026-09
python scripts/revenue/play_reports.py pull --month 2026-09 --kinds earnings,sales
```

Wynik: `analytics-reports/raw/revenue/play/RRRR-MM/<earnings|sales|subscriptions|installs>/`. Archiwa zip są rozpakowywane, a pliki CSV w UTF-16 dostają obok kopię `*.utf8.csv` (łatwiej je czytać w Excelu i Pythonie).

Uwagi:
- Raport **earnings** za dany miesiąc pojawia się zwykle na początku kolejnego miesiąca.
- `sales/salesreport_RRRRMM.zip` jest aktualizowany na bieżąco w trakcie miesiąca.
- Nowe konto dewelopera może mieć pusty bucket do czasu pierwszych raportów.

## 3. Bezpieczeństwo

- `.env`, `*.p8`, `*.json` w `scripts/revenue/` oraz cały `analytics-reports/raw/revenue/` są w `.gitignore`. Przed commitem sprawdź `git status`.
- Klucz API App Store Connect i klucz konta serwisowego trzymaj w menedżerze haseł. Jeśli wyciekną: App Store Connect -> Integrations -> **Revoke**, Google Cloud -> Service accounts -> Keys -> **Delete**.
- Oba skrypty tylko czytają dane, niczego nie zmieniają w App Store Connect ani w Play Console.
