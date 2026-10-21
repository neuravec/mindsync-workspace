# CLAUDE.md – dostęp do Google Search Console dla mindsync.app

Ten katalog to samodzielna paczka do czytania danych z Google Search Console (GSC)
dla właściwości **mindsync.app**. Claude Code czyta ten plik automatycznie, gdy sesja
startuje w tym katalogu.

## Co to jest

`scripts/gsc/pull_gsc.py` korzysta **wyłącznie ze standardowej biblioteki Pythona**
(zero `pip install`). Loguje się do Google przez OAuth (przepływ „installed app" z PKCE,
lokalny redirect na `http://127.0.0.1:<losowy port>/`), zapisuje token lokalnie i sam go
odświeża. Zakres uprawnień: `webmasters.readonly`, czyli **tylko odczyt**.

Pliki w `scripts/gsc/`:

| Plik | Rola | Skąd |
|---|---|---|
| `pull_gsc.py` | runner GSC | w paczce |
| `gsc.config.json` | wskazuje właściwość (`sc-domain:mindsync.app`) | w paczce |
| `client_secret.json` | klient OAuth typu Desktop | **przyszedł mailem, wgrywa operator** |
| `token.json` | token dostępu i refresh | **powstaje sam** po `auth`, nie wysyłać nikomu |

## Komendy (uruchamiaj z katalogu `scripts/gsc`)

```powershell
python pull_gsc.py auth                      # jednorazowo: otwiera przeglądarkę, loguje konto Google
python pull_gsc.py sites                     # lista właściwości GSC widocznych dla tego konta
python pull_gsc.py pull                      # pobranie danych (site z gsc.config.json)
python pull_gsc.py pull --months 3 --full    # 3 miesiące + wymiar fraza x URL
python pull_gsc.py pull --site sc-domain:mindsync.app   # z pominięciem configu
```

Wynik ląduje w `migracja/gsc/baseline-RRRR-MM-DD/`: `queries.csv` (frazy: clicks,
impressions, ctr, position), `pages.csv` (URL-e), `dates.csv` (trend dzienny),
`query-page.csv` (tylko przy `--full`), `summary.json` (właściwość, zakres dat, sumy).

## Pierwsze uruchomienie – kolejność

1. Sprawdź, czy `scripts/gsc/client_secret.json` istnieje. Jeśli nie, zatrzymaj się
   i poproś operatora o wgranie pliku z maila. Nie próbuj tworzyć go samodzielnie.
2. `python pull_gsc.py auth` – to **musi zrobić człowiek** w przeglądarce, nie da się
   tego zaklikać z terminala. Uprzedź operatora, że otworzy się okno logowania Google
   i trzeba wybrać konto, które ma dostęp do mindsync.app w Search Console.
3. `python pull_gsc.py sites` – to jest właściwy test dostępu. Na liście musi być
   `mindsync.app`. Zanotuj **dokładną formę** wpisu (`sc-domain:mindsync.app` albo
   `https://www.mindsync.app/`) oraz `permissionLevel`.
4. Jeśli forma właściwości różni się od tej w `gsc.config.json`, popraw config.
5. `python pull_gsc.py pull --months 3 --full`, potem przeczytaj `summary.json`.

## Zasady twarde

- **Tylko odczyt.** Skrypt nie ma i nie dostanie uprawnień do zapisu w GSC. Nie dodawaj
  zakresów OAuth, nie zgłaszaj sitemap przez API, nie usuwaj URL-i z indeksu.
- **Nigdy nie commituj ani nie wysyłaj** `client_secret.json` i `token.json`. Jeśli
  w tym katalogu powstanie repo git, natychmiast dopisz oba pliki do `.gitignore`.
- **Nie modyfikuj `pull_gsc.py`** bez uzgodnienia. To ta sama wersja, której używa główny
  zespół, a rozjazd wersji skryptu oznacza rozjazd danych.
- Nie uruchamiaj `auth` ponownie „na wszelki wypadek". Token odświeża się sam.

## Pułapki, które już kosztowały nas czas

- **Dane GSC mają opóźnienie około 3 dni.** Skrypt kończy zakres na `dziś − 3 dni`.
  Ocena zmiany wdrożonej wczoraj jest niemożliwa, realny odczyt to 4-6 tygodni.
- **Różne `--months` to różne zakresy dat.** Porównuj wyłącznie okna tej samej długości
  pochodzące z jednego pobrania. Zestawienie pobrania 3-miesięcznego z 16-miesięcznym
  daje bzdurne wnioski per URL.
- **`permissionLevel: siteUnverifiedUser`** oznacza, że dane nie spływają i właściwość
  trzeba najpierw zweryfikować. `siteOwner` i `siteFullUser` są w porządku.
- Konto może widzieć **wiele właściwości naraz**. Zawsze pilnuj, która siedzi w configu.
- Jeśli po `auth` w `token.json` nie ma `refresh_token`: cofnij dostęp aplikacji na
  <https://myaccount.google.com/permissions> i powtórz `auth`.

## Najczęstsze błędy i co znaczą

| Objaw | Przyczyna | Co zrobić |
|---|---|---|
| `Brak client_secret.json w scripts/gsc/` | plik nie został wgrany | wgraj plik z maila pod dokładnie tą nazwą |
| Google: `Access blocked` / `access_denied` przy logowaniu | ekran zgody OAuth jest w trybie Testing, a to konto nie jest na liście test userów | poproś nadawcę o dopisanie adresu jako Test user albo o opublikowanie aplikacji (In production) |
| `Google hasn't verified this app` | aplikacja wewnętrzna, bez weryfikacji Google | **Advanced → Go to ... (unsafe)** i zaakceptuj dostęp read-only. To jest oczekiwane |
| `sites` nie pokazuje mindsync.app | zalogowane złe konto Google albo brak dostępu do właściwości | wyloguj się i powtórz `auth` właściwym kontem; jeśli konto nadal nie widzi właściwości, właściciel musi je dodać w GSC |
| HTTP 403 przy `pull` | konto ma dostęp do innej właściwości niż ta w configu | popraw `site_url` na dokładną wartość z `sites` |
| Token przestał działać po tygodniu | ekran zgody OAuth siedzi w trybie Testing (refresh token wygasa po 7 dniach) | aplikację trzeba opublikować (In production) po stronie właściciela projektu Google Cloud |
