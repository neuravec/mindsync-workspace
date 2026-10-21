# store/: screenshoty App Store i Google Play

Szablon i renderer screenshotów sklepowych MindSync w stylu obecnego zestawu
(`blog/images/app-screenshots/ios-1..8.webp`): jasny gradient mint, dwulinijkowy nagłówek
z jedną pogrubioną frazą, podtytuł, telefon z prawdziwym ekranem apki. Ostatni slajd App Store
to opinia z gwiazdkami i ilustracją latarni.

## Uruchomienie

```powershell
pip install playwright pillow
python -m playwright install chromium
python scripts/store/render_store.py                 # oba sklepy, wszystkie slajdy
python scripts/store/render_store.py --only main,reflect
python scripts/store/render_store.py --format play
python scripts/store/render_store.py --strict        # exit 1, gdy któryś slajd stoi na placeholderze
```

Renderer działa offline (Playwright + Chromium, Figtree z `templates/assets/`, kopiowany
z `social/templates/assets/` przy pierwszym uruchomieniu). Niczego nie wysyła do sklepów.

## Wyjście (`store/out/`)

| plik | rozmiar | co to |
|---|---|---|
| `appstore/NN-<id>.png` | 1290x2796, RGB bez alfy | App Store 6.9", ramka iPhone, render iOS |
| `play/NN-<id>.png` | 1080x1920 (9:16), RGB | Google Play, neutralna ramka Android, render Android |
| `_contact_appstore.png`, `_contact_play.png` | | wszystkie slajdy obok siebie, tylko do przeglądu |
| `_render.json` | | który shot trafił na slajd, placeholder tak/nie, skala tekstu, ostrzeżenia |

`NN` to pozycja slajdu w danym sklepie liczona na całym `slides.json`, więc `--only` nie zmienia nazw.

## `slides.json`

Tablica slajdów, kolejność = kolejność w sklepie. Pola:

- `id` (`[a-z0-9_-]`), `type`: `screen` albo `testimonial`, `targets`: domyślnie `["appstore", "play"]`.
- `headline_lines`: 1-3 linie nagłówka, każda w jednej linii obrazu; `**pogrubienie**`.
- `subtitle`: `**pogrubienie**`; bez `\n` łamie się sam (wyważone linie), `\n` wymusza złamanie.
- `shot_ios`, `shot_android`: ścieżka albo lista ścieżek (od korzenia repo). Wygrywa pierwszy
  istniejący plik, każdy kolejny to placeholder i renderer to zgłasza. Dlatego świeży render
  (`store/renders/<platforma>/store_<nazwa>.png`) stoi pierwszy i wskakuje sam, gdy plik się pojawi.
  Bez renderu Android slajd Play bierze render iOS i odcina z niego pasek statusu oraz home indicator.
- `ios_mode` / `android_mode` (opcjonalne): `fill` = shot ma własną górę (pasek statusu albo puste
  safe area) i wchodzi od y=0; `band` = treść apki zaczyna się od y=0 (shoty z harnessu w
  `social/images/app-shots/`), więc nad nią idzie pusty pas w kolorze góry shotu. Domyślnie `auto`:
  `band` dla `social/images/app-shots/`, `fill` dla reszty.
- `crop_top` (opcjonalne): ile px źródła pominąć od góry (wysokie zrzuty).
- `decor` (opcjonalne, tylko slajdy `screen`): delikatna dekoracja tła, domyślnie wyłączona.
  `"decor": "bird_wave"` włącza ją we wszystkich sklepach slajdu, `"decor": {"play": "bird_wave"}`
  tylko w wymienionych (drugi sklep zostaje bez zmian). Zestaw `bird_wave`: lecący ptak jedną linią
  (`templates/assets/decor-bird.svg`, wektor przerysowany z ilustracji powitalnej apki
  `assets/images/welcome_with_birds.png`) na marginesie między podtytułem a telefonem oraz falka
  jak wykres liniowy (`templates/assets/decor-wave.svg`) w dolnej części, schowana częściowo za
  telefonem. Kolor jasnoniebieski z rodziny Lagoon/Aqua Breeze (`#aad6dd` ptak, `#9acbd4` falka,
  ciemniejsza, bo tło na dole jest ciemniejsze), cienkie zaokrąglone linie. Warstwa leży pod
  nagłówkiem, podtytułem i telefonem, więc nigdy ich nie zasłania. Położenie ustawiają zmienne
  `--bird-*` i `--wave-t` w `templates/store.css`, osobno dla każdego formatu. Gdy ptak wejdzie
  w margines 3% szerokości wokół tekstu albo telefonu (np. po zmianie copy), renderer ostrzega
  (`decor bird near headline` w konsoli i w `_render.json`). Stan na 2026-10-19: próba tylko na
  slajdzie Play `main`.
- testimonial: `quote` (`\n` = linia, pusta linia = akapit), `attribution`, `stars` (0-5).
- `note`: komentarz, renderer go pomija.

Renderer odrzuca U+2014 i U+2013 w tekstach slajdów. Apostrofy i cudzysłowy zamienia na typograficzne
tylko w obrazie.

## Zasady

- Ekran wklejany jest tak, jak przyszedł z renderu: bez retuszu, bez dorysowanego UI, bez sztucznego
  paska statusu. Prawdziwe ekrany robi `flutter-mobile`.
- Copy pochodzi z `store/copy.md` (akcept brand-voice-manager). Tu się go nie pisze.
- Play: tekst na najwyżej ok. 20% obrazu. Renderer mierzy to (`text_share` w `_render.json`)
  i ostrzega powyżej progu. Fontów na Play nie powiększamy. Testimonial idzie tylko do App Store.
- Wygląd zmienia się w `templates/store.css` (zmienne per format), nie w pojedynczym slajdzie.
