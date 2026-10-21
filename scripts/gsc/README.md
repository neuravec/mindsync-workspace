# GSC API — baseline SEO przed migracją

Cel: zgrać „fotografię" widoczności `sklep.plasmet.pl` w Google **przed** migracją na Shoper (top frazy, pozycje, kliknięcia, CTR, wyświetlenia — per zapytanie, per URL, per dzień), żeby po migracji pilnować ciągłości SEO. Skrypt `pull_gsc.py` używa **tylko biblioteki standardowej Pythona** (masz 3.14 — bez `pip install`).

## A. Co musisz wyklikać w Google Cloud (jednorazowo, ~5 min)

> Zaloguj się kontem Google, które **ma dostęp do `sklep.plasmet.pl` w Search Console**.

1. **Projekt:** wejdź na <https://console.cloud.google.com/> → u góry utwórz projekt (np. `plasmet-gsc`).
2. **Włącz API:** <https://console.cloud.google.com/apis/library/searchconsole.googleapis.com> → **Włącz** (Enable) „Google Search Console API".
3. **Ekran zgody OAuth:** *APIs & Services → OAuth consent screen* → typ **External** → uzupełnij nazwę aplikacji i e-mail → w sekcji **Test users** dodaj swój adres Google (ten z dostępem do GSC). (Aplikacja może zostać w trybie „Testing" — to wystarczy.)
4. **Dane logowania:** *APIs & Services → Credentials → Create credentials → OAuth client ID* → typ **Desktop app** (Aplikacja komputerowa) → **Create**.
5. **Pobierz JSON** klienta (przycisk „Download JSON") i zapisz go w tym folderze jako **`client_secret.json`**.

## B. Autoryzacja i pobranie danych

W terminalu w tym folderze (`scripts/gsc`):

```powershell
python pull_gsc.py auth      # otworzy przeglądarkę -> zaloguj się i zatwierdź dostęp
python pull_gsc.py sites     # wypisze Twoje właściwości GSC (skopiuj właściwą wartość)
```

`sites` pokaże np. `sc-domain:plasmet.pl` (właściwość domenowa) **lub** `https://sklep.plasmet.pl/` (właściwość prefiksowa). Wpisz właściwą do `gsc.config.json` (skopiuj z `gsc.config.example.json`) **albo** podaj w `--site`:

```powershell
python pull_gsc.py pull --site sc-domain:plasmet.pl
# albo, jeśli wpisałeś site_url do gsc.config.json:
python pull_gsc.py pull
# pełny zakres + dodatkowo wymiar zapytanie+URL (może być duży):
python pull_gsc.py pull --full
```

## C. Co powstaje

`migracja/gsc/baseline-RRRR-MM-DD/`:
- `queries.csv` — frazy: clicks, impressions, ctr, position
- `pages.csv` — adresy URL: clicks, impressions, ctr, position
- `dates.csv` — trend dzienny
- `query-page.csv` — (tylko z `--full`) fraza × URL
- `summary.json` — właściwość, zakres dat, liczby wierszy, sumy

Zakres: ostatnie ~16 miesięcy (maks. retencja GSC), do `dziś − 3 dni`.

## D. Zgłoszenie sitemapy (`submit-sitemap`, dodane 2026-09-25)

Odpowiednik GSC -> Sitemaps -> Submit (Search Console API `sitemaps.submit`, `PUT` z pustym
body), a zaraz po nim `GET` tej samej sitemapy. Wypisuje jedną linię:
`SUBMIT-SITEMAP OK site=... feed=... lastSubmitted=... lastDownloaded=... isPending=...`.

```powershell
python pull_gsc.py submit-sitemap
# domyślnie: --site z gsc.config.json (sc-domain:mindsync.app), --feed https://www.mindsync.app/sitemap.xml
python pull_gsc.py submit-sitemap --site sc-domain:mindsync.app --feed https://www.mindsync.app/sitemap.xml
```

Woła ją automatycznie drip bloga (`scripts/webflow/blog-publish.ps1`) po udanej publikacji
całej strony Webflow; szczegóły w `scripts/webflow/README.md`.

**Zakres OAuth:** od 2026-09-25 `SCOPE` to pełne `https://www.googleapis.com/auth/webmasters`
(obejmuje odczyt, więc `sites`, `pull` i skrypty `blog-*.py` działają bez zmian). Token wydany
wcześniej ma tylko `webmasters.readonly`: odczyt dalej działa, ale `submit-sitemap` dostaje
403 i kończy się komunikatem
`SUBMIT-SITEMAP BLAD: token ma tylko readonly, uruchom: python scripts/gsc/pull_gsc.py auth`.
Wtedy raz, w przeglądarce, kontem z dostępem do `sc-domain:mindsync.app`:

```powershell
python C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\gsc\pull_gsc.py auth
```

Kody wyjścia `submit-sitemap`: 0 OK, 2 brak `--site`, 3 token readonly, 4 inne 403 (brak
uprawnień do właściwości), 5 inny błąd HTTP, 6 błąd sieci.

## Uwagi i bezpieczeństwo

- `client_secret.json` i `token.json` są w `.gitignore` — **nie udostępniaj ich**.
- Brak `refresh_token` po `auth`? Cofnij dostęp na <https://myaccount.google.com/permissions> i powtórz `auth`.
- Skrypt jest powtarzalny — **uruchom go ponownie zaraz PO migracji** (i potem co miesiąc), żeby porównać pozycje i wychwycić spadki.
- Po starcie Shopera: te `queries.csv`/`pages.csv` posłużą też do priorytetyzacji przekierowań 301 (które URL-e mają realny ruch i nie wolno ich zgubić).
