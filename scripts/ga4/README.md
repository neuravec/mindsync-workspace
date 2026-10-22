# GA4: dane ruchu na mindsync.app

Skrypt `pull_ga4.py` pobiera z Google Analytics 4 ruch na stronie mindsync.app i na blogu (`/journal/`). Używa **tylko biblioteki standardowej Pythona**, nic nie trzeba instalować. Działa wyłącznie w trybie odczytu (zakres `analytics.readonly`).

Klient OAuth jest **wspólny z GSC**: skrypt czyta `scripts/gsc/client_secret.json` (klient typu Desktop z projektu Google Cloud `mindsync-8f534`). Nie kopiuj go do tego folderu. Token GA4 jest osobny i zapisuje się w `scripts/ga4/token.json`.

## A. Jednorazowa konfiguracja w Google Cloud (ok. 3 min)

Zaloguj się kontem Google, które ma dostęp do projektu `mindsync-8f534` i do właściwości GA4 mindsync.app.

1. Wejdź na <https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com?project=mindsync-8f534> i kliknij **Włącz** (Enable) przy "Google Analytics Data API".
2. Wejdź na <https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com?project=mindsync-8f534> i kliknij **Włącz** przy "Google Analytics Admin API".
3. Sprawdź ekran zgody OAuth: *APIs & Services -> OAuth consent screen*. Jeśli aplikacja jest w trybie "Testing", Twój adres Google musi być na liście **Test users** (ten sam, którego używasz do GSC). Nie trzeba ręcznie dodawać zakresu, skrypt poprosi o niego przy logowaniu.
4. Sprawdź dostęp w GA4: *GA4 -> Administracja -> Zarządzanie dostępem do usługi*. Twoje konto potrzebuje roli co najmniej **Wyświetlający** (Viewer).

## B. Autoryzacja i pobranie danych

Wszystkie komendy uruchamiasz z katalogu głównego workspace (`Heroku`):

```powershell
python scripts/ga4/pull_ga4.py auth         # otworzy przeglądarkę: zaloguj się i zatwierdź dostęp do Analytics (tylko odczyt)
python scripts/ga4/pull_ga4.py properties   # wypisze konta i właściwości GA4, np. properties/123456789
```

Utwórz plik `scripts/ga4/ga4.config.json` z identyfikatorem właściwości z poprzedniej komendy:

```json
{"property_id": "properties/123456789"}
```

Pobierz dane:

```powershell
python scripts/ga4/pull_ga4.py pull                      # ostatnie 28 dni (do wczoraj)
python scripts/ga4/pull_ga4.py pull --days 90
python scripts/ga4/pull_ga4.py pull --property properties/123456789   # bez pliku konfiguracyjnego
python scripts/ga4/pull_ga4.py pull --blog-prefix /journal/          # domyślny prefiks bloga
```

## C. Co powstaje

`analytics-reports/raw/ga4/RRRR-MM-DD/`:

| Plik | Zawartość |
|---|---|
| `overview_by_date.csv` | dziennie: sessions, activeUsers, newUsers, screenPageViews, engagementRate, averageSessionDuration |
| `landing_pages.csv` | top 500 stron wejścia: sessions, activeUsers, engagementRate, keyEvents (jeśli dostępne) |
| `channels.csv` | domyślna grupa kanałów (sessionDefaultChannelGroup) |
| `source_medium.csv` | źródło i medium sesji |
| `countries.csv` | kraje |
| `devices.csv` | typ urządzenia (desktop, mobile, tablet) |
| `blog_pages.csv` | strony bloga (pagePath zaczynający się od `/journal/`) |
| `summary.json` | zakres dat, liczby wierszy, sumy zbiorcze |

## D. Najczęstsze błędy

- **"API ... nie jest włączone w projekcie mindsync-8f534"**: wykonaj krok A1 lub A2 (skrypt poda dokładny link), odczekaj kilka minut.
- **HTTP 403 przy pull**: konto nie ma dostępu do tej właściwości GA4 (krok A4) albo zły `property_id`.
- **"Refresh token wygasł"**: aplikacja OAuth w trybie "Testing" wydaje tokeny ważne 7 dni. Uruchom ponownie `auth`.
- **Brak `keyEvents`**: jeśli właściwość nie ma zdarzeń kluczowych, skrypt spróbuje starszej metryki `conversions`, a potem pominie tę kolumnę.

`token.json` i `ga4.config.json` są w `.gitignore`. Skrypt nigdy nie wypisuje tokenów.
