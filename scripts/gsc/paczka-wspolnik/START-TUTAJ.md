# Google Search Console dla mindsync.app – uruchomienie u siebie

Paczka daje dostęp **tylko do odczytu** danych z Google Search Console dla domeny
mindsync.app: frazy, adresy URL, kliknięcia, wyświetlenia, CTR i pozycje. Nic nie
zapisuje w Google i nie rusza strony. Całość zajmuje około 10 minut.

## 1. Czego potrzebujesz

- **Python 3.9 lub nowszy** (`python --version` w terminalu). Jeśli nie masz:
  <https://www.python.org/downloads/> i przy instalacji zaznacz „Add Python to PATH".
  Żadnych bibliotek nie doinstalowujesz, skrypt używa wyłącznie standardowej biblioteki.
- **Konto Google, które ma dostęp do właściwości mindsync.app w Search Console.**
  Jeśli po zalogowaniu na <https://search.google.com/search-console> nie widzisz
  mindsync.app, napisz do mnie, dodam Cię, zanim ruszysz dalej.
- Plik **`client_secret.json`** z tego maila.

## 2. Rozpakuj i wgraj klucz

Rozpakuj paczkę gdziekolwiek, na przykład do `C:\mindsync-gsc`. Struktura katalogów
musi zostać taka, jaka jest, bo od niej zależy, gdzie wylądują wyniki:

```
mindsync-gsc\
  CLAUDE.md
  START-TUTAJ.md
  scripts\gsc\pull_gsc.py
  scripts\gsc\gsc.config.json
```

Załączony `client_secret.json` wrzuć do `scripts\gsc\`. Nazwy nie zmieniaj.

## 3. Autoryzacja (jednorazowo)

Otwórz terminal w katalogu `scripts\gsc` i uruchom:

```powershell
python pull_gsc.py auth
```

Otworzy się przeglądarka. Wybierz konto Google z dostępem do mindsync.app.

Google pokaże ostrzeżenie **„Google hasn't verified this app"**. To normalne, bo to jest
nasza wewnętrzna aplikacja, której nie zgłaszamy do weryfikacji. Kliknij
**Advanced → Go to ... (unsafe)** i zaakceptuj dostęp *read-only* do Search Console.

Skrypt zapisze `token.json` obok siebie i od tej pory loguje się sam.

## 4. Sprawdź, czy widzisz właściwość

```powershell
python pull_gsc.py sites
```

Na liście musi pojawić się `mindsync.app`. Zapamiętaj dokładną formę wpisu.

- Jeśli widzisz `sc-domain:mindsync.app` – nic nie zmieniasz, tak jest w konfiguracji.
- Jeśli widzisz inną formę, na przykład `https://www.mindsync.app/` – wpisz ją w pole
  `site_url` w pliku `gsc.config.json`.
- Jeśli obok właściwości jest `siteUnverifiedUser` – dane nie spływają, daj znać.
- Jeśli listy nie ma wcale albo nie ma na niej mindsync.app – jesteś zalogowany złym
  kontem Google. Wyloguj się w przeglądarce i powtórz `auth`.

## 5. Pobierz dane

```powershell
python pull_gsc.py pull --months 3 --full
```

Wyniki trafiają do `migracja\gsc\baseline-RRRR-MM-DD\`:

| Plik | Co zawiera |
|---|---|
| `queries.csv` | frazy: kliknięcia, wyświetlenia, CTR, pozycja |
| `pages.csv` | adresy URL z tymi samymi metrykami |
| `dates.csv` | trend dzienny |
| `query-page.csv` | fraza x URL (tylko przy `--full`) |
| `summary.json` | właściwość, zakres dat, liczba wierszy, sumy |

Bez `--months` skrypt bierze maksymalny zakres, jaki trzyma GSC, czyli około
16 miesięcy. Pobranie można powtarzać kiedy chcesz, dane się nie psują.

## 6. Praca z Claude Code

Odpal Claude Code w katalogu `mindsync-gsc` (tam, gdzie leży `CLAUDE.md`). Claude sam
wczyta ten plik i będzie wiedział, jakich komend używać, gdzie lądują dane i na jakie
pułapki uważać. Możesz po prostu napisać: „pobierz z GSC ostatnie 3 miesiące i pokaż mi
20 fraz z największą liczbą wyświetleń i zerowymi kliknięciami".

Krok `auth` z punktu 3 musisz zrobić sam w przeglądarce, tego Claude za Ciebie nie kliknie.

## 7. Dwie rzeczy, o których trzeba pamiętać przy analizie

- **Dane mają opóźnienie około 3 dni.** Skrypt kończy zakres na `dziś − 3 dni`, więc
  efektu wczorajszej zmiany na stronie po prostu jeszcze nie ma w danych. Sensowna ocena
  zmiany w SEO to 4-6 tygodni, nie kilka dni.
- **Nie porównuj pobrań o różnym `--months`.** Mają różne zakresy dat i porównanie per URL
  wychodzi wtedy krzywo. Porównuj okna tej samej długości z jednego pobrania.

## 8. Bezpieczeństwo

`client_secret.json` i `token.json` to sekrety. Nie wrzucaj ich do repozytorium, na dysk
współdzielony ani do żadnego czatu. Jeśli zakładasz w tym katalogu repo git, najpierw
dopisz oba pliki do `.gitignore`.

Dostęp jest read-only, więc nawet przy najgorszym scenariuszu nikt tym kluczem nie zmieni
niczego w Search Console ani na stronie. Cofnąć go możesz w każdej chwili na
<https://myaccount.google.com/permissions>.

## Gdy coś nie działa

| Objaw | Co zrobić |
|---|---|
| `Brak client_secret.json w scripts/gsc/` | plik nie leży w tym katalogu albo ma inną nazwę |
| `python` nie jest rozpoznawane jako polecenie | Python nie jest w PATH, przeinstaluj z zaznaczoną opcją „Add Python to PATH" |
| Google: `Access blocked` albo `access_denied` | napisz do mnie, muszę dopisać Twój adres na listę kont testowych |
| `Google hasn't verified this app` | to jest oczekiwane, Advanced → Go to ... (unsafe) |
| `sites` nie pokazuje mindsync.app | złe konto Google albo brak dostępu do właściwości, napisz do mnie |
| HTTP 403 przy `pull` | `site_url` w `gsc.config.json` nie zgadza się z tym, co pokazuje `sites` |
| Po tygodniu przestało działać | napisz do mnie, trzeba opublikować aplikację w Google Cloud (tryb produkcyjny) |
