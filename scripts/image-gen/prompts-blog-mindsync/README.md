# Prompty hero bloga MindSync

Biblioteka promptów do generacji hero wpisów (Gemini / Nano Banana przez
`scripts/image-gen/gemini-generate.ps1`). Właściciel: `graphic-designer`.
Reguły wizualne: `docs/blog/brand-mindsync.md` §4 (paleta forest/mint/sand, spokój,
ciepłe światło, zero tekstu w grafice, zero fałszywych screenshotów apki, ludzie bez
twarzy w centrum kadru).

- `_styl-bazowy.md` – blok stylu wspólny; doklejaj do promptu tematycznego każdego hero.
- `hero-01-codzienny-moment.md` – wariant „codzienny moment" (przedmioty, światło, scena).
- `hero-02-abstrakcja.md` – wariant „miękka abstrakcja" (gradienty w palecie, kształty).
- `partia2-<slug>.md` – gotowe prompty per wpis partii 2 (10 sztuk, drip 2026-09-04..09-13).
  Każdy plik: wariant, uzasadnienie sceny, JEDEN blok promptu EN (to bierze skrypt),
  proponowany `hero_image_alt` i gotowa komenda generacji.
- `partia3-<slug>.md` : prompty partii 3 (3 sztuki, drip 2026-09-21..09-23). Ten sam układ
  pliku co partia 2, plus sekcja „Kadr na wariant 800x600": skrypt kadruje miniaturę
  `gravity East`, czyli zostawia prawe 75% szerokości, więc nic istotnego nie może siedzieć
  w lewej ćwiartce kadru.
- `whats-new-in-mindsync.md` : hero wpisu produktowego o nowej wersji aplikacji (ten sam układ
  co partia 3 i 6). Nowości pokazane metaforą przedmiotu (ceramiczne płytki na tacy), nigdy
  ekranem ani interfejsem.

**Zasada per wpis:** dokładnie jeden blok ` ``` ` w pliku (skrypt bierze pierwszy), zero
podwójnych myślników `-` `-` w treści promptu (skrypt kasuje je jako flagi CLI), zero
em-dash w całym pliku.

Format wyjścia: `blog/images/<slug>/hero-1600x900.webp|jpg` (≤150 KB WebP)
+ `hero-800x600.webp|jpg` (≤90 KB). Prompt tematyczny per wpis pisze `graphic-designer`
na bazie tych szablonów; ścieżkę do niego (albo prompt inline) wpisuje się w pole
`hero_prompt` pliku kolejki.

Stare prompty PLASMET (`prompts-kategorie/`) zostają jako referencja formatu – NIE używać
ich stylu (narzędzia/warsztat) dla MindSync.
