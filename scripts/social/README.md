# scripts/social: narzędzia Instagrama MindSync

Kontrakt kolejki i opis pól: `social/queue/_format.md`. Proces i mapa całości: `social/README.md`.

## Render / preview / gate

Trzy skrypty lokalne, bez sieci i bez publikowania. Wspólne stałe (typy, szablony, pola,
limity znaków) siedzą w `social_common.py`, jedno źródło dla wszystkich trzech.

Wymagania (jednorazowo): `pip install playwright pillow` i `python -m playwright install chromium`.
Font Figtree i logo leżą w `social/templates/assets/`, więc render działa offline.

### render.py: JSON do JPEG

```
python scripts/social/render.py <id albo ścieżka JSON> [kolejne...]
python scripts/social/render.py _przyklad-carousel      # pliki "_" wskazujesz po nazwie
python scripts/social/render.py --all-szkic              # wszystkie posty "szkic" (bez plików "_")
```

- Każdy slajd = `social/templates/<szablon>.html` + `base.css` + `fit.js`. Pola są escapowane,
  nowa linia w polu daje `<br>`, proste apostrofy i cudzysłowy zamieniane na typograficzne
  (tylko w grafice, JSON zostaje bez zmian).
- `fit.js` zmniejsza font krokami po 2%, gdy tekst się nie mieści, ale nigdy poniżej minimum
  szablonu (tytuł 56-68 px, tekst 36-38 px). Render ostrzega, gdy font zmalał, gdy tekst
  nie mieści się nawet przy minimum i gdy Figtree się nie załadował.
- Wynik: `social/media/<id>/01.jpg, 02.jpg...` (JPEG baseline, sRGB z profilem ICC, q=90,
  1080x1350 feed albo 1080x1920 story). Stare slajdy spoza bieżącego renderu są usuwane.
- Aktualizuje pole `media` w JSON (reszta pliku i kolejność kluczy bez zmian, UTF-8, indent 2)
  i zapisuje `social/media/<id>/_render.json` z odciskiem treści slajdów. Dzięki temu bramka
  wie, że ktoś zmienił tekst po renderze.

Szablony: `cover`, `body`, `cta` (karuzela), `quote` (single), `story` (wariant A: kolor
i typografia) oraz ze zdjęciem (wariant B): `photo-cover` (cover karuzeli albo single),
`photo-split` (body karuzeli), `photo-quote` (single), `app-screen` (CTA albo slajd produktowy
karuzeli), `photo-story` (story), a także wariant C „bold" (kinowe kadry Nano Banana Pro
i duża typografia, koncepcja: `social/variant-c-koncepcja.md`): `bold-cover` (cover karuzeli
albo single), `bold-photo-text`, `bold-statement`, `bold-myth`, `bold-save` (body karuzeli),
`bold-cta` (zamyka karuzelę), `bold-story` (story). Pole `numer` to numer punktu w treści;
licznik `2/7` w rogu render dopisuje sam.

#### Wariant C (`bold-*`)

- Szablony ładują `bold.css` (po `base.css`) i `bold.js` (przed `fit.js`); render podstawia
  pola jak w pozostałych szablonach, nic więcej nie trzeba.
- `akcent`: fragment tytułu (`bold-cover`, `bold-cta`, `bold-story`) albo nagłówka
  (`bold-photo-text`, `bold-statement`) dostaje piaskowy marker. Musi być dokładnym podciągiem
  tego pola (wielkość liter bez znaczenia), inaczej bloker bramki.
- `punkty` (`bold-save`, 3-5 linii po 40 znaków) i `opcje` (`bold-story`, 2-4 linie po
  34 znaki): jedna pozycja na linię, rozdzielone `\n`; liczba linii i limit linii to blokery.
- `tlo` (`bold-statement`): `ciemne` (domyślne), `coral` albo `piasek`; inna wartość = bloker.
- `uklad` w `bold-cover` ma domyślnie `tekst-dol` (nie `tekst-gora` jak w `photo-*`); bramka
  ostrzega, gdy nie jest ustawiony jawnie. `bold-story` ma układ stały.
- Obrazy: `social/assets/variant-c/*.jpg`; `min_bok` 1080 dla `bold-cover` i `bold-story`,
  640 dla `bold-photo-text`. Kontrast tekstu na zdjęciu mierzony jak w wariancie B.
- Nazwy własne, które nie mogą się łamać (np. Prep Card), pisz z twardą spacją (U+00A0).

#### Szablony ze zdjęciem

- `obraz`: ścieżka repo-relative do JPG/PNG/WebP, np. `blog/images/<slug>/hero-raw.png`
  (hero wpisów, ok. 30 sztuk w stylu marki) albo `social/images/app/ios-N-ekran.png`
  (czysty ekran aplikacji). Render wczytuje plik lokalnie przez `file://`; niezaładowany
  obraz = błąd renderu.
- `pozycja` (opcjonalne): CSS `object-position`, np. `"center 30%"`, `"72% center"`.
- `uklad` (opcjonalne, `photo-cover`, `photo-quote`, `photo-story`): `tekst-gora` (domyślny:
  tekst na jasnym tle u góry, zdjęcie od dołu, pasuje do hero bloga z motywem nisko)
  albo `tekst-dol`. Zdjęcie zajmuje pas ok. 65-72% wysokości i przechodzi w tło jasnym
  welonem (bez przyciemniania), więc źródła 16:9 i 1:1 są powiększane najwyżej ok. 1.3x.
  Obszar tekstu kończy się tam, gdzie welon jest gęsty: dłuższy tekst zmniejsza `fit.js`,
  zamiast wejść na motyw zdjęcia.
- **Kontrast**: dla każdego slajdu ze zdjęciem render robi drugi zrzut bez tekstu i liczy
  kontrast WCAG każdej linii tekstu wobec najgorszych 5% pikseli tła. Wynik trafia do
  `_render.json` (`kontrast`); poniżej 4.5:1 ostrzeżenie renderu, poniżej 3:1 (AA dla dużego
  tekstu; cały tekst w szablonach ma co najmniej 27 px) bloker bramki. Pigułki z własnym tłem
  (kicker, numer) mają stały kolor marki i nie są mierzone.
- `_render.json` zawiera też `obrazy` (ścieżka i odcisk sha256 każdego zdjęcia); odcisk wchodzi
  do `hash_slajdow`, więc podmiana pliku obrazu po renderze = media nieaktualne w bramce.
  Posty bez zdjęć mają odcisk bez zmian (stare `_render.json` dalej pasują).
- `app-screen`: zrzut ląduje w ramce telefonu rysowanej w CSS. Grafiki sklepowe
  `blog/images/app-screenshots/ios-N.webp` mają już nagłówek i ramkę, dlatego czysty ekran
  wycina `python scripts/social/app-screens.py` (wynik: `social/images/app/ios-N-ekran.png`).
  `ios-7` ma treść po polsku, `ios-8` to opinia bez telefonu: nie używać w postach EN.

#### Warianty D i E: nowości w aplikacji (prawdziwe ekrany)

- **D** (`feature-hero`, `feature-step`, `feature-before-after`, `feature-story`, `reel-text`)
  i **E** (`aggro-hook`, `aggro-split`, `aggro-story`, format agresywny) ładują `bold.css`,
  `feature.css` (mockup telefonu: ramka, zaokrąglenia, cień, wyspa dynamiczna, pasek statusu iOS,
  lupa) i E dodatkowo `aggro.css`.
- Pola `ekran`, `ekran_przed`, `ekran_po`: prawdziwy zrzut aplikacji z harnessu Fluttera
  (`social/images/app-shots/<shot>.png`, 1179x2556). Render traktuje je jak `obraz` (plik
  w repo, odcisk w `hash_slajdow`, podmiana pliku = media nieaktualne), dokleja pasek statusu
  iOS (harness go nie renderuje; kolor tła próbkowany z górnej krawędzi zrzutu) i skaluje ekran
  w dół (400-600 px na slajdzie), więc zostaje ostry.
- Lupa (`feature-step`, `aggro-split`): `zoom_x`, `zoom_y`, `zoom_w`, `zoom_h` w px źródła.
  Na telefonie obrys wycinka i przyciemnienie reszty ekranu, obok powiększenie. Geometria lupy
  per szablon: `SZABLONY[...]['lupa']` w `social_common.py`. W `feature-step` lupa stoi na
  wysokości obrysu, ale gdy jej dół (z obwódką) wszedłby w margines 88 px nad dolną krawędzią
  slajdu, przesuwa się w górę (hak w szablonie wołany przez `fit.js` przed zrzutem); obrys na
  telefonie zostaje na miejscu.
- `kadr` (0.3-1.0): pokazana część wysokości zrzutu od góry (`clip-path` na obrazie, reszta
  ekranu w kolorze wiersza nad cięciem); kadrowanie, nie retusz. Poza zakresem = bloker.
- `obraz` w `feature-hero`, `feature-story`, `reel-text` jest opcjonalny (tło pod ciemnym welonem);
  `ekran` w `aggro-hook` i `aggro-story` też (bez ekranu sama typografia).
- Bramka: brak pliku ekranu i czerwony ekran błędu Fluttera = bloker; wymiary inne niż
  1179x2556, zrzut węższy niż ekran telefonu w szablonie, ekran spoza `app-shots/`, lupa
  powiększająca ponad 1.25x = ostrzeżenie; zoom niepełny albo poza zrzutem = bloker;
  `zrodlo.app_feature` pusty = bloker, `zrodlo.frontend_commit` pusty albo `-dirty` = ostrzeżenie.

| szablon | pole | twardy | zalecany |
|---|---|---|---|
| feature-hero | kicker / tytul / akcent / podtytul | 28 / 50 / 24 / 110 | 24 / 40 / 16 / 80 |
| feature-step | numer / naglowek / akcent / tekst | 3 / 50 / 24 / 160 | 2 / 40 / 16 / 120 |
| feature-before-after | naglowek / akcent / tekst / etykiety | 50 / 24 / 140 / 12 | 40 / 16 / 110 / 10 |
| feature-story | kicker / tytul / akcent / tekst | 28 / 55 / 24 / 120 | 24 / 45 / 16 / 90 |
| reel-text | kicker / tytul / akcent / tekst | 28 / 70 / 30 / 120 | 24 / 55 / 20 / 90 |
| aggro-hook | kicker / tytul / akcent / podtytul | 24 / 60 / 24 / 110 | 20 / 45 / 16 / 85 |
| aggro-split | numer / naglowek / akcent / tekst | 3 / 45 / 24 / 130 | 2 / 34 / 16 / 100 |
| aggro-story | kicker / tytul / akcent / tekst | 24 / 60 / 24 / 90 | 20 / 45 / 16 / 70 |

### app-shots.py: prawdziwe ekrany z kodu aplikacji

```
python scripts/social/app-shots.py run                          # wszystkie shoty (flutter test --tags marketing)
python scripts/social/app-shots.py run --name habit_tracker_weekly
python scripts/social/app-shots.py list                         # nazwa, wymiary, KB, data renderu, commit frontu
```

Uruchamia na pierwszym planie `flutter test test/marketing_shots --tags marketing`
w `mindsync-frontend/mindsync_app` (tylko ten katalog; pełny `flutter test` w tym repo potrafi
skończyć się OOM) z `MARKETING_SHOTS_DIR=social/images/app-shots`. Niczego w repo frontu nie
zmienia. Po przebiegu dopisuje do `social/images/app-shots/_manifest.json` shoty zapisane
w tym przebiegu: plik, wymiary, rozmiar, datę i commit frontu (`git -C mindsync-frontend
rev-parse --short HEAD`, z dopiskiem `-dirty`, gdy `lib/` ma niezacommitowane zmiany). Ten sha
wpisujesz w `zrodlo.frontend_commit`. Harness i nowe shoty: `flutter-mobile`
(`mindsync_app/test/marketing_shots/README.md`).

### reel-render.py: rolka (MP4 + okładka)

```
python scripts/social/reel-render.py _przyklad-reel-feature
python scripts/social/reel-render.py <id> --klatki C:/tmp/klatki     # + 4 klatki PNG do obejrzenia
python scripts/social/reel-render.py --all-szkic
```

1. Sceny renderuje ta sama funkcja co `render.py` (`renderuj_slajd`: szablony, fit.js, pomiar
   kontrastu) do `social/media/<id>/sceny/NN.jpg`; okładka `cover.jpg` ze sceny `cover_slajd`.
2. ffmpeg (z PATH, inaczej binarka z `pip install imageio-ffmpeg`) składa MP4: H.264 high,
   yuv420p, 30 fps, GOP 60, CRF 20, `+faststart`; AAC 48 kHz stereo. Przejścia `fade`/`slide`
   to `xfade` 0.4 s, `cut` to `concat`; `ruch` to `zoompan` na obrazie 2x większym (bez drgań).
   Bez `audio` dokładana jest cicha ścieżka AAC (część pipeline'ów Instagrama źle znosi wideo
   bez audio). Muzyka tylko z licencją (`audio_licencja`); `social/CLAUDE.md` §2.3.
3. Kontrola ffprobe (te same progi co bramka) i `_render.json`: odcisk treści (sceny, okładka,
   audio z odciskiem pliku, ekrany), sceny z czasami na osi, parametry wideo, ostrzeżenia.
4. `media` = `["social/media/<id>/reel.mp4", "social/media/<id>/cover.jpg"]`.

`render.py` odmawia renderu rolki (kieruje do `reel-render.py`), `--all-szkic` je pomija.
Bramka dla rolki: sceny (`scena_sek` 1.5-10 s, `przejscie`, `ruch`), czas całości 5-90 s,
`cover_slajd`, `audio` z plikiem i licencją; media sprawdza zawsze, gdy są (przy `szkic` jako
ostrzeżenia, przy `gotowy` jako blokery): ffprobe H.264/yuv420p, 1080x1920, 23-60 fps, 5-90 s,
do 300 MB, audio AAC do 48 kHz, okładka JPEG 1080x1920, render nie starszy niż treść.

### ui-change-detector.py: pytanie o post po większej zmianie w aplikacji

```
python scripts/social/ui-change-detector.py --range A..B      # ręcznie, zakres commitów frontu
python scripts/social/ui-change-detector.py                   # ręcznie, ostatni commit
echo '{"tool_input":{"command":"git commit -m x"}}' | python scripts/social/ui-change-detector.py   # tryb hooka
```

Pod hook Claude Code `PostToolUse` (matcher `Bash`): czyta JSON hooka ze stdin, działa tylko
przy komendzie z `git commit`, sprawdza ostatni commit `mindsync-frontend`. „Większa zmiana
wizualna" (stałe na górze pliku): nowy plik `*_screen.dart` w `lib/` ALBO co najmniej 80
zmienionych linii kodu UI ALBO co najmniej 3 zmienione pliki widgetów. Kod UI to `lib/ui/**`
oraz realna struktura repo `lib/screens/**` i `lib/widgets/**`, bez cubitów, blocków, stanów
i kodu generowanego. Jako kontekst dokłada zmienione assety graficzne i nowe klucze l10n (ARB).
Wynik: JSON `{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": ...}}`
z prośbą, żeby sesja ZAPYTAŁA operatora o post albo rolkę (`/social-write` w trybie feature)
i z kandydatami na shoty. Mała zmiana = brak wyjścia. Zawsze exit 0 (błędy tylko na stderr).
Ostatnio zgłoszony commit trzyma `social/.ui-detector-state.json` (hook nie pyta dwa razy;
tryb ręczny `--range` zgłasza zawsze). Hooka w `settings.json` ten skrypt nie konfiguruje.

### pdf-export.py: PDF dla grafika

```
python scripts/social/pdf-export.py --all-przyklady            # social/preview/MindSync-Instagram-przyklady.pdf
python scripts/social/pdf-export.py --id <id> --id <id2> --nazwa probka
python scripts/social/pdf-export.py --status szkic --nazwa partia-1
```

A4 pionowo: strona tytułowa (opis + miniatury w pięciu sekcjach: wariant A kolor i typografia,
B zdjęcia z bloga, C odważny z obrazami Nano Banana Pro, D nowości w aplikacji z prawdziwymi
ekranami, E nowości w formacie agresywnym), przed każdym wariantem strona-przekładka, potem
każdy post na osobnej stronie w kolejności A-E (rolka: storyboard klatek scen z czasami na
osi, ścieżka do `reel.mp4` i parametry wideo z `_render.json`): slajdy w siatce
3 kolumny (karuzela 7+ slajdów 4 kolumny, story pojedynczo), caption z hashtagami (bez
dzielenia między strony) i alt-y. Post należy do najwyższego wariantu, którego szablon zawiera. HTML jest
zapisywany do pliku i otwierany przez `file://` (nie `set_content`, bo wtedy obrazy `file://`
się nie ładują); skrypt sprawdza, że wszystkie obrazy się załadowały (inaczej exit 1).
Wymaga wyrenderowanych mediów.

### social-gate.py: bramka kolejki

```
python scripts/social/social-gate.py                     # = --all (bez plików "_")
python scripts/social/social-gate.py --id <id> [--id <id2>]
python scripts/social/social-gate.py --status gotowy
```

Exit code 1 przy co najmniej jednym blokerze (tak woła ją `ig-publish.py`). Read-only.

BLOKERY: pola wymagane i enumy; wzór `id`, data, godzina ET; liczba slajdów wg typu
(carousel 2-10, single 1, story 1); szablon zgodny z typem; wymagane pola slajdu i twarde
limity znaków; caption z hashtagami do 2200; hashtagi 0-5, `#[A-Za-z0-9_]+`, bez duplikatów;
alt dla każdego slajdu feed; **U+2014 i U+2013 w dowolnym polu**; `kryzysowy: true` bez "988"
w caption (story: 988 musi być na slajdzie); słowa kryzysowe przy `kryzysowy: false`;
zakazane obietnice medyczne (cure, diagnose, guaranteed, replaces therapy... z wyjątkiem
zaprzeczeń typu "not a replacement for therapy"); feed bez `glos: monika-v1`; przy `gotowy`
media zgodne z wymogami Meta (JPEG, RGB, sRGB, szerokość 320-1440, proporcje 4:5 albo 9:16,
do 8 MB, liczba plików = liczba slajdów, media nie starsze niż treść).

OSTRZEŻENIA: pole dłuższe niż długość zalecana w `_format.md`; kolizja slotu (dwa posty feed
o tej samej dacie i godzinie ET); karuzela bez `cover` na początku albo `cta` na końcu; URL
albo `#hashtag` wpisany w caption; źródło spoza `blog/published-log.json`; `gotowy` z datą
w przeszłości; nieznane pola.

Limity znaków (twardy / zalecany):

| szablon | pole | twardy | zalecany |
|---|---|---|---|
| cover | kicker / tytul / podtytul | 32 / 80 / 160 | 30 / 60 / 100 |
| body | numer / naglowek / tekst | 3 / 70 / 300 | 3 / 50 / 220 |
| cta | tytul / tekst / akcja | 60 / 180 / 36 | 50 / 140 / 35 |
| quote | cytat / autor / podpis | 200 / 50 / 80 | 160 / 50 / 60 |
| story | kicker / tytul / tekst | 32 / 70 / 220 | 25 / 60 / 180 |
| photo-cover | kicker / tytul / podtytul | 32 / 70 / 130 | 30 / 55 / 90 |
| photo-split | numer / naglowek / tekst | 3 / 60 / 200 | 3 / 45 / 150 |
| photo-quote | cytat / podpis | 150 / 70 | 120 / 55 |
| app-screen | tytul / tekst / akcja | 50 / 140 / 30 | 40 / 110 / 24 |
| photo-story | kicker / tytul / tekst | 32 / 70 / 200 | 25 / 55 / 160 |
| bold-cover | kicker / tytul / akcent / podtytul | 28 / 55 / 30 / 90 | 24 / 45 / 20 / 60 |
| bold-photo-text | numer / naglowek / akcent / tekst | 3 / 50 / 24 / 150 | 2 / 40 / 16 / 120 |
| bold-statement | numer / naglowek / akcent / tekst | 3 / 60 / 24 / 180 | 2 / 45 / 16 / 140 |
| bold-myth | numer / mit / fakt / podpis | 3 / 70 / 90 / 110 | 2 / 50 / 70 / 90 |
| bold-save | kicker / tytul / punkty (na linię) / podpis | 28 / 30 / 40 / 60 | 24 / 26 / 36 / 45 |
| bold-cta | tytul / akcent / tekst / akcja | 45 / 20 / 140 / 24 | 35 / 14 / 110 / 18 |
| bold-story | kicker / tytul / akcent / opcje (na linię) / tekst | 28 / 55 / 24 / 34 / 70 | 24 / 45 / 16 / 30 / 50 |

Szablony ze zdjęciem mają dodatkowo `obraz` (wymagane, do 240 znaków), `pozycja` (do 40)
i `uklad` (`tekst-gora` albo `tekst-dol`). Bramka: brak pliku, ścieżka absolutna albo poza
repo, format inny niż JPG/PNG/WebP, zła `pozycja`/`uklad` i kontrast poniżej 3:1 to BLOKERY;
krótszy bok źródła poniżej 1080 px (pełny kadr: `photo-cover`, `photo-quote`, `photo-story`),
640 (`photo-split`) albo 380 (`app-screen`) to OSTRZEŻENIE (obraz będzie powiększany).

Twarde limity sprawdzone renderem tekstu o maksymalnej długości: wszystko mieści się
przy foncie zmniejszonym najwyżej do ok. 84% (szablony ze zdjęciem: do ok. 78%).

### preview.py: kontaktówka partii

```
python scripts/social/preview.py --status szkic --nazwa partia-1
python scripts/social/preview.py --id _przyklad-carousel --id _przyklad-single --id _przyklad-story --nazwa przyklady
```

Bez argumentów bierze całą kolejkę (bez plików `_`), nazwa domyślna to dzisiejsza data.
Wynik: `social/preview/<nazwa>.html`, otwierasz lokalnie w przeglądarce (ścieżki względne do
`social/media/`). Na karcie posta: typ, status, data i godzina ET (plus czas polski), znacznik
kryzysowy, miniatury slajdów w kolejności z altami, caption z hashtagami i licznikiem znaków,
źródło i pełny wynik bramki.

Typowa pętla: edycja JSON, `render.py`, `social-gate.py --id`, `preview.py`, akcept operatora.

## Publikacja / token / drip

Kanał: oficjalne **Instagram API with Instagram Login** (`graph.instagram.com`, wersja
w `IG_GRAPH_VERSION`, domyślnie `v23.0`), uprawnienia `instagram_business_basic` +
`instagram_business_content_publish`, bez strony na Facebooku. Wzorzec odpornościowy przeniesiony
z dripu bloga (`scripts/webflow/blog-publish.ps1`): DRY-RUN domyślnie, bramki przed zapisem,
idempotencja, płaski log publikacji, jedna linia logu na zdarzenie, osobny zrzut błędów.

### Pliki

| Plik | Rola |
|---|---|
| `ig-publish.py` | Publikator: `--id <id>` albo `--due`; `--live` dla publikacji na żywo, bez niego DRY-RUN; typy carousel, single, story, reel |
| `ig-token.py` | `status`, `refresh`, `check`, `whoami` dla tokenu long-lived (60 dni) |
| `media_host.py` | Upload JPEG i MP4 pod publiczny URL (`cloudinary` albo `webflow`; wideo tylko Cloudinary) + kontrola HEAD (`image/jpeg` albo `video/mp4`) |
| `ig_common.py` | Odczyt i zapis `.env`, klient Graph API z retry, czytelne błędy Meta |
| `ig-drip.ps1` | Jeden przebieg dripu: `ig-token.py check` (auto refresh poniżej 20 dni) + `ig-publish.py --due` |
| `register-drip-task.ps1` | Rejestracja zadania "MindSync-IG-Drip" (uruchamia **operator**; bez `-Apply` tylko podgląd) |
| `.env` / `.env.example` | Sekrety (`.env` ignorowany przez `.gitignore` w tym katalogu) |
| `tests/test_ig_publish.py` | Testy offline publikatora (także rolki), `requests` zmockowany |
| `tests/test_reel_feature_contract.py` | Kontrakt rolek i wariantu D w bramce i `social_common` |
| `tests/test_ui_change_detector.py` | Detektor zmian wizualnych na tymczasowym repo git |

Logi: `social/_drip-log.txt` (jedna linia: czas, LIVE/DRY, id, media_id, wynik),
`social/_drip-error.txt` (pełny traceback), `social/published-log.json` (płaska tablica).

### Komendy

```
python scripts/social/ig-publish.py --id 2026-10-06-sunday-scaries            # podgląd, zero wysyłki
python scripts/social/ig-publish.py --id 2026-10-06-sunday-scaries --live     # publikacja jednego posta
python scripts/social/ig-publish.py --due                                     # co poszłoby teraz
python scripts/social/ig-publish.py --due --live                              # drip
python scripts/social/ig-token.py whoami      # test po podpięciu tokenu (user_id, username)
python scripts/social/ig-token.py status
python scripts/social/ig-token.py refresh     # nowe 60 dni, zapis do .env
python scripts/social/ig-token.py check       # exit 2, gdy zostało mniej niż 10 dni albo data nieznana
python -m pytest scripts/social/tests -q
```

### Co robi `ig-publish.py` z jednym postem

1. **Idempotencja**: gdy `publikacja.ig_media_id` jest ustawione albo id jest w
   `social/published-log.json`, post jest pomijany (exit 0, linia `POMINIETO`).
2. **Status** musi być `gotowy`.
3. **Walidacja**: platforma, typ, pliki z `media[]` istnieją i są JPEG, karuzela 2-10 slajdów,
   single i story po 1, caption do 2200 znaków, do 30 hashtagów, alt do 1000 znaków.
4. **Bramka**: `social-gate.py --id <id>`; exit różny od 0 albo brak pliku bramki blokuje publikację.
5. **Limit**: `GET /{ig_user_id}/content_publishing_limit`; wyczerpany limit (100/24 h) to błąd.
6. **Media**: upload każdego JPEG na host z `SOCIAL_MEDIA_HOST`, potem `HEAD` (200 + `image/jpeg`).
7. **Kontenery**, tworzone dopiero teraz, bo wygasają po 24 h:
   - single: `image_url`, `caption`, `alt_text`
   - carousel: kontener `is_carousel_item=true` na każdy slajd (z `alt_text`), w kolejności `media[]`,
     potem `media_type=CAROUSEL`, `children=<id,id,...>`, `caption`
   - story: `media_type=STORIES`, `image_url` (bez captionu i altu)
   - reel: `media_type=REELS`, `video_url` (MP4 z hosta wideo), `cover_url` (okładka JPEG),
     `caption`, `share_to_feed=true` (rolka trafia też do feedu); bez altu. `cover_url` i
     `thumb_offset` są w referencji `POST /<IG_ID>/media` (cover_url wygrywa, jeśli podasz oba;
     my wysyłamy tylko cover_url). Limity Meta: 3 s-15 min, do 300 MB, H.264/HEVC, 23-60 fps;
     nasza bramka trzyma 5-90 s, żeby rolka kwalifikowała się do zakładki Reels.
8. **Polling** `status_code` każdego kontenera do `FINISHED` (`ERROR`, `EXPIRED` albo przekroczony
   `IG_POLL_MAX_SEC` oznaczają błąd). Rolka: wideo przetwarza się minutami, więc osobny polling
   co `IG_VIDEO_POLL_INTERVAL_SEC` (15 s) do `IG_VIDEO_POLL_MAX_SEC` (900 s); po limicie post
   zostaje `gotowy` i wraca w następnym przebiegu dripu.
9. **`media_publish`** z `creation_id`. Bez ślepego ponawiania: po błędzie przejściowym skrypt
   najpierw sprawdza, czy kontener nie ma już statusu `PUBLISHED`, żeby nie wrzucić posta dwa razy.
10. **Zapis od razu** po publikacji: `publikacja` (`ig_container_id`, `ig_media_id`, `opublikowano`),
    status `opublikowany`, wpis w `published-log.json`. Dopiero potem permalink; jego błąd to tylko
    ostrzeżenie, post zostaje zapisany jako opublikowany.

Caption to `caption`, pusta linia i `hashtagi` rozdzielone spacją (`#` dokładany, gdy go brak).

Błąd na dowolnym kroku przed `media_publish`: linia `BLAD` w logu, traceback w `_drip-error.txt`,
exit 1, status w kolejce bez zmian. Retry z backoffem (do 5 prób, z `Retry-After`) przy 429, 5xx,
błędach sieci i przejściowych kodach Meta. Błędy walidacyjne 4xx idą bez ponawiania, z
`error.message`, `code`, `subcode`, `error_user_msg` i `fbtrace_id` w komunikacie.

Kody wyjścia: 0 ok albo nic do zrobienia, 1 błąd, 3 bloker (status, walidacja, bramka),
4 inny przebieg trzyma blokadę `social/.ig-publish.lock` (blokada tylko przy `--live`,
przeterminowana po 2 h).

### Tryb `--due`

Bierze pliki `social/queue/*.json` bez prefiksu `_`, ze statusem `gotowy`, jeszcze nieopublikowane,
których `planowana_data` + `planowana_godzina_et` (strefa `America/New_York`, z czasem letnim)
już minęły. Publikuje najwyżej **1 post feed (carousel albo single) i 1 story** na przebieg,
najstarszy pierwszy (rolka liczy się jako post feed). Post zablokowany przez bramkę zostaje pominięty i drip próbuje następnego
tego samego rodzaju, żeby jeden zły plik nie zatrzymał kolejki. Błąd API kończy dany rodzaj w tym
przebiegu (kolejna próba za godzinę). Brak tokenu albo hosta mediów zgłaszany jest dopiero wtedy,
gdy coś faktycznie ma iść na żywo, więc pusty przebieg nie śmieci w logu.

### DRY-RUN

Bez `--live` skrypt wypisuje pełny plan: każdy endpoint i parametry (bez tokenu), ścieżki plików
do uploadu z kontrolą istnienia, gotowy caption i wynik bramki. Nie uploaduje mediów i nie łączy
się z `graph.instagram.com`. Blokery wypisuje na końcu i kończy się kodem 3. Linia trafia do
`_drip-log.txt` z oznaczeniem `DRY`.

```
python scripts/social/ig-publish.py --id _przyklad-carousel --dry-run
```

### Hosting mediów (`SOCIAL_MEDIA_HOST`)

Meta pobiera obraz z publicznego URL-a w chwili tworzenia kontenera, a plik musi żyć jeszcze
około godziny. `cleanup` nie jest wołany automatycznie.

- `cloudinary`: upload podpisany (`CLOUDINARY_API_KEY` + `CLOUDINARY_API_SECRET`) albo unsigned
  (`CLOUDINARY_UPLOAD_PRESET`), folder `CLOUDINARY_FOLDER`, `public_id` = `<id>/NN`.
- **Wideo (rolki)**: `SOCIAL_VIDEO_HOST` (pusty = `SOCIAL_MEDIA_HOST`). Cloudinary przyjmuje MP4
  przez `/video/upload` (limit pliku zależy od planu, darmowy 100 MB; nasze rolki mają kilka MB).
  Webflow Assets API wideo nie przyjmuje (obrazy do 4 MB, dokumenty do 10 MB, Lottie:
  https://developers.webflow.com/data/docs/working-with-assets), więc `WebflowHost` rzuca czytelny
  błąd z rekomendacją `SOCIAL_VIDEO_HOST=cloudinary`, a dry-run pokazuje to ostrzeżenie przy
  uploadzie MP4. Obrazy mogą dalej iść przez Webflow.
- `webflow`: Assets API v2 dwuetapowo (metadane z MD5, potem multipart na presigned S3), jak hero
  w dripie bloga. Token i site id czytane z istniejącego `scripts/webflow/.env`, nic nie jest
  kopiowane. Token musi mieć zakres Assets = Read and write (drip bloga już z niego korzysta).
  Każdy post dokłada assety do biblioteki strony mindsync.app.

### Token

Long-lived token żyje 60 dni. `refresh` działa tylko dla ważnego tokenu, który ma co najmniej
24 h (skrypt pilnuje tego przez `IG_TOKEN_REFRESHED_AT`). **Wygasłego tokenu nie da się odzyskać**,
trzeba wygenerować nowy w aplikacji Meta. Dlatego `ig-drip.ps1` przy każdym przebiegu woła
`check --auto-refresh-below 20`: poniżej 20 dni token odświeża się sam, poniżej 10 dni w logu
pojawia się `TOKEN UWAGA`. Po ręcznym wygenerowaniu tokenu wpisz `IG_TOKEN_EXPIRES_AT`
(dziś + 60 dni, ISO UTC) albo po 24 h uruchom `refresh`, który ustawi datę sam.

### Drip w Harmonogramie zadań

`register-drip-task.ps1` rejestruje "MindSync-IG-Drip": codziennie od 13:00 co godzinę przez 15 h
(13:00-03:00 czasu polskiego, czyli mniej więcej 07:00-21:00 ET), ustawienia jak w
"MindSync Blog Drip" (StartWhenAvailable, IgnoreNew, limit 30 min), plus start na baterii.
Ścieżka do Pythona zapisywana jest w zadaniu jako pełna, bo Harmonogram nie musi widzieć PATH.

```
powershell -ExecutionPolicy Bypass -File scripts\social\register-drip-task.ps1               # podgląd
powershell -ExecutionPolicy Bypass -File scripts\social\register-drip-task.ps1 -Apply        # zadanie w trybie DRY
powershell -ExecutionPolicy Bypass -File scripts\social\register-drip-task.ps1 -Apply -Live  # na żywo
```

### Pierwsze podpięcie (checklist)

1. Konto IG jako Professional (Creator albo Business), aplikacja Meta z produktem Instagram,
   konto dodane jako Instagram Tester, wygenerowany token.
2. `scripts/social/.env` z `.env.example`: `IG_ACCESS_TOKEN`, `IG_USER_ID`, `IG_TOKEN_EXPIRES_AT`,
   `SOCIAL_MEDIA_HOST` (plus dane Cloudinary, jeśli ten host).
3. `ig-token.py whoami`: zgadza się `username` i `user_id`.
4. `ig-publish.py --id <single>` w DRY, potem `--live` na jednym poście single i kontrola
   permalinku. Następnie karuzela, potem story.
5. Dopiero po udanym pilocie `register-drip-task.ps1 -Apply -Live`.
