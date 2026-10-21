# Styl bazowy obrazów na Instagram (Nano Banana Pro): naturalny kadr z codzienności

**Wersja 2 (obowiązuje od 2026-10-02, decyzja operatora).** Zastępuje wersję 1 („kinowy kadr",
teal-orange, nocne sceny), która dawała wygląd stockowego obrazu AI. Wzorzec zatwierdzony przez
operatora: `c08c-kitchen-table-morning.md` (pierwszy post konta). Odrzucone podejście: przebudowa
szablonu wg taste-skill (v2 `bold2-cover`), szablony `bold-*` zostają bez zmian.

**ZAKRES (doprecyzowanie operatora 2026-10-02): ta wersja dotyczy WYŁĄCZNIE wygenerowanych zdjęć z ludźmi** (slajdy wariantu C z polem `obraz`, w których kadr pokazuje osobę). Bez zmian zostają: slajdy typograficzne wariantu C (`bold-myth`, `bold-statement`, `bold-save`, `bold-cta`), warianty A, B, D, E oraz obrazy bez ludzi (dla scen bez ludzi wersja 1 poniżej nadal jest dopuszczalna).

Tekst NIGDY nie jest w obrazie: nakłada go HTML (`social/templates/bold-*.html`).

## Ustawienia generatora (bez zmian)

- Model **`gemini-3-pro-image`** (Nano Banana Pro), proporcje w API, nie kadrowanie:
  feed `--aspect 4:5`, story `--aspect 9:16`, `--size 2K`.
- Generator: `python social/scripts/image-gen/nano_banana.py --prompt-file <plik.md> --out
  social/assets/variant-c/<nazwa>.jpg --aspect 4:5 --size 2K --live` (klucz `GEMINI_API_KEY`
  z `scripts/image-gen/.env`, nigdy nie wypisywany). Koszt ok. 0,2 USD za obraz.

## Jak pisać prompt (zasady z researchu 2026-10-02 i testu c08a/b/c)

1. **Pełne zdania, narracja sceny**, nie lista tagów (oficjalna rada Google). Kolejność: kto, co
   robi, gdzie i kiedy, światło, ubranie i otoczenie, aparat, kadr i miejsce na tekst.
2. **Zwykły aparat zamiast „cinematic"**: „shot on a phone camera" albo „a Fujifilm compact
   camera with a 35mm lens", „at eye level", „slightly off-center framing", „a little noise",
   „gentle softness".
3. **Płaskie, rozproszone światło dnia**: „plain daylight from a cloudy sky", „soft overcast
   daylight", „even and low in contrast", „realistic neutral colors", „no color grading",
   „natural white balance".
4. **Drobne niedoskonałości**: włosy z kosmykami, naturalna faktura skóry, „no makeup look",
   ubranie zwykłe i lekko znoszone.
5. **Otoczenie „do życia"**: 3-4 konkretne zwykłe przedmioty (talerz z resztkami tostów,
   obrane pół pomarańczy, łyżeczka, zamknięty notes, miska owoców, deska z okruchami).
6. **Ubrania gładkie**: zawsze „with no pattern or text" / „with no print or logo"
   (model dorysowuje logo marek, np. Nike, gdy tego nie ma w prompcie).
7. **Miejsce na tekst opisane pozytywnie**: „the upper third of the image is mostly the light
   wall above the window, simple and uncluttered for a headline". Szablon `bold-cover` i tak
   kładzie ciemny welon u góry, więc twarz może wejść pod nagłówek.
8. **Postać**: spokojna, „thoughtfully but at ease", w trzech czwartych profilu albo z twarzą
   częściowo poza kadrem; twarz nie jest tematem; bez płaczu i pozy rozpaczy.
9. Negatywy ograniczaj do 1-2 krótkich (ubranie bez nadruku); resztę opisuj pozytywnie.

## Czego NIE pisać (pogarsza realizm albo psuje markę)

- „cinematic", „film still", „moody", „dramatic lighting", „color grade", „teal and orange",
  „perfect", „flawless", „8k", „ultra detailed", „hyperrealistic", „masterpiece";
- **żadnych kartek, notatek, ekranów, szyldów ani książek z widocznymi tytułami w scenie**:
  model pisze na nich czytelny tekst (test c08b: karteczka „CALL MUM" na lodówce, do tego
  brytyjskie „mum" przy odbiorcy z USA). Notes tylko „closed";
- noc i jedno ciepłe źródło światła w ciemności (to była wersja 1, za ciężka na start konta);
- nadruki, logo, marki.

## Szablon promptu (wzorzec c08c, podmień scenę)

```
An everyday photo of [osoba: wiek, płeć] [czynność] [miejsce] on a weekday morning, [co trzyma / co robi dłońmi], looking [gdzie] thoughtfully but at ease. Plain daylight from a cloudy sky fills the room evenly, low contrast, realistic neutral colors, nothing stylized. [Ubranie: kolor, materiał] with no pattern or text and [włosy z niedoskonałością]; [twarz:] natural skin texture with no makeup look. [Otoczenie: 3-4 zwykłe przedmioty]. Taken with a phone camera from [skąd] at eye level, slightly tilted horizon, gentle softness and a little noise. Vertical 4:5 frame; the upper third of the image is mostly [jasna ściana / niebo w oknie] and soft daylight, simple and uncluttered for a headline.
```

## Kontrola po generacji (Read na każdym obrazie, także w powiększeniu detali)

Odrzuć kadr z: czytelnym tekstem lub pseudo-napisem (kartki, kubki, opakowania, okładki),
logo na ubraniu lub przedmiocie, zdeformowanymi dłońmi, twarzą w centrum z silną emocją,
jasnym detalem tam, gdzie ma stać tekst. Drobne logo można usunąć lokalnie, ale lepiej
wygenerować ponownie z poprawionym promptem.

## Wersja 1 (kinowa)

Pliki c01-c06 to wersja „kinowa" (nocne sceny, teal-orange, jedno ciepłe światło). Dla zdjęć Z LUDŹMI
nie używać. Dla scen bez ludzi dopuszczalna.
