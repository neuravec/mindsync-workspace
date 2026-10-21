---
name: social-write
description: >
  JEDYNA ścieżka tworzenia partii postów na Instagram MindSync (nowe konto EN pod USA):
  karuzele edukacyjne, pojedyncze grafiki/cytaty i Stories, stylem Moniki zaadaptowanym
  na IG. Używaj ZAWSZE, gdy ktoś prosi o posty na Instagram, partię, karuzelę, cytat,
  story albo przerobienie wpisu bloga na post („zrób posty na IG", „partia na instagram",
  „karuzela z wpisu", „zrób stories na ten tydzień", „make Instagram posts",
  „/social-write"). Prowadzi: zakres partii → tematy (filary + recykling bloga + katalog
  funkcji) → social-content-writer (JSON do social/queue/) → humanizer → test zimnego czytania → render.py →
  social-gate.py → akcept brand-voice-manager → preview.py → STOP. Tryb „feature": post,
  story albo rolka o nowej funkcji/zmianie w aplikacji na PRAWDZIWYCH ekranach (app-shots.py
  → feature-*/aggro-* → render.py/reel-render.py), także gdy detektor zmian wizualnych
  zapyta po commicie frontu („zrób post o nowości", „rolka o habit trackerze"). Status
  `gotowy` wyłącznie na wyraźne polecenie operatora. Publikacja to osobny skill `social-publish`.
---

# Partia postów na Instagram MindSync: runbook

Ten skill istnieje po to, żeby każdy post szedł jedną ścieżką, brzmiał jak Monika
i nigdy nie wyszedł bez decyzji operatora. Źródła prawdy (czytaj, nie duplikuj):

| Co | Gdzie |
|---|---|
| Pipeline, kadencja, zasady twarde | `social/README.md` |
| Format JSON, limity, caption, alt, `kryzysowy` | `social/queue/_format.md` |
| Głos na IG, YMYL, filary, hashtagi, checklist akceptu | `social/brand-instagram.md` |
| Głos bazowy i wzorzec dosłowny | `docs/blog/brand-mindsync.md` §2, `docs/blog/voice-sample-monika.md` |
| Funkcje apki (tylko `live`) | `blog/app-features.json` |
| Wpisy bloga do recyklingu | `blog/published-log.json` + `blog/queue/<plik>.json` |

## Zasady twarde (bez wyjątków)

1. **Sesja główna nie pisze prozy postów sama.** Slajdy, caption, alt i hashtagi pisze agent
   `social-content-writer`, także przy „szybkiej poprawce jednego słowa". Sesja główna
   orkiestruje i uruchamia skrypty.
2. **Każdy post ma `"glos": "monika-v1"`** i przechodzi humanizer z próbką głosu.
3. **Zero U+2014 i U+2013 jako separatora** w każdym polu. Sprawdza `social-gate.py`,
   ale przy poprawce przebuduj zdanie, nie podmieniaj znaku.
4. **Status `gotowy` tylko na wyraźne polecenie operatora** w tej rozmowie („akceptuję",
   „ustaw gotowy", „puszczaj"). Pozytywny akcept brand-voice to NIE jest polecenie operatora.
   Auto mode nie nadaje `gotowy` sam.
5. **Nic nie idzie na żywo z tego skilla.** Publikacja: skill `social-publish`.
6. W promptach subagentów: zakaz `run_in_background`, lista kroków do końca, raport na końcu.
   Taski ok. 20-40 min (jeden `social-content-writer` na 3-5 postów).

## Krok 0. Zakres partii i stan kolejki

- Od operatora: **ile** postów, **jakie formaty** (carousel / single / story), **okres**
  (od-do). Brak danych = zaproponuj według kadencji z `social/README.md` §5 (np. tydzień:
  2 karuzele, 1-2 single, 3-5 stories) i zapytaj o potwierdzenie jednym zdaniem.
- Przejrzyj `social/queue/*.json` (pomiń pliki z `_`) i `social/published-log.json`:
  zajęte daty i godziny, tematy z ostatnich 8 tygodni, wpisy bloga już przerobione
  (`zrodlo.blog_slug`). **Bez powtórek** tematu i wpisu-źródła w oknie 8 tygodni,
  chyba że operator chce inaczej.
- Zaplanuj sloty: daty i `planowana_godzina_et` wg kadencji, bez kolizji z kolejką.

## Krok 1. Dobór tematów

Dla każdego slotu: filar (`social/brand-instagram.md` §5), typ, temat, źródło.
- **Recykling bloga:** wpisy z `blog/published-log.json` (tylko opublikowane, bo post
  odsyła do nich linkiem w bio). Z wpisu bierz jedną myśl: krok, badanie, puentę, pytanie FAQ.
- **Tematy własne:** z filarów, których blog nie pokrywa (mity o terapii, mikro-nawyki).
- **Pokrycie:** każdy post, który pokazuje „jak", ma cel: funkcję `live` z
  `blog/app-features.json`, wpis bloga albo `https://mindsync.app/features`. Brak celu =
  zmiana kąta.
- Tematy kryzysowe domyślnie wypadają; tylko jawna decyzja operatora (`kryzysowy: true`).
- Wynik: tabela partii (id, typ, filar, temat, źródło, cel CTA, data, godzina ET). Pokaż ją
  operatorowi tylko gdy zakres był niejasny; inaczej idź dalej.

## Krok 2. Treść (agent `social-content-writer`)

Prompt dla każdego agenta MUSI zawierać ten blok (uzupełnij nawiasy):

```
TASK: Napisz [N] postów Instagram MindSync (EN, US) stylem Moniki wg tabeli niżej.
FILES: social/queue/<id>.json dla każdego posta (status "szkic", glos "monika-v1",
       media [], publikacja z wartościami null)
TABELA: [id | typ | filar | temat | zrodlo (blog_slug+url albo null) | cel CTA | data | godzina ET]
KROKI (wszystkie, po kolei, bez run_in_background):
1. Przeczytaj social/brand-instagram.md, social/queue/_format.md,
   docs/blog/voice-sample-monika.md (w całości) i social/queue/_przyklad-*.json.
2. Dla postów z bloga przeczytaj źródłowy JSON w blog/queue/ (fakty, badania, kroki).
   Nie dodawaj faktów spoza źródła bez weryfikacji (rok + autor/instytucja + URL).
3. Napisz slajdy, caption (hak w 1. linii, krótkie akapity, jedno CTA, bez URL-i),
   3-5 hashtagów z zestawu filaru, alt_text na każdy slajd z przepisanym tekstem slajdu.
4. Uruchom Skill humanizer na wszystkich tekstach posta, z docs/blog/voice-sample-monika.md
   jako writing sample. Zakaz U+2014 i U+2013 wygrywa z próbką.
5. Sanity check: fakty, liczby, nazwy funkcji, CTA i hashtagi przetrwały humanizer;
   alt nadal zgodny ze slajdami. Zasady z sekcji „Czytelność przed stylem" w Twojej
   definicji agenta są twarde: pełne zdania, zero haseł-zagadek, metafor do rozszyfrowania
   i odwołań poza slajd; za długo = nowy slajd albo caption, nie skrót.
6. Zapisz JSON-y. Przeszukaj je pod kątem U+2014 i U+2013 (Grep) i przebuduj trafione zdania.
DONE_WHEN: wszystkie pliki w social/queue/, status "szkic", zgodne z _format.md, zero U+2014/U+2013.
RAPORT: lista plików, typy, źródła badań z URL, wątpliwości YMYL.
```

## Krok 3. Humanizer (kontrola)

Agent ma humanizer w krokach. Sesja główna sprawdza wyrywkowo 1-2 posty: brak AI-słów,
brak „rule of three" na siłę, brak myślników, głos Moniki zachowany. Poprawka prozy wraca
do `social-content-writer` (SendMessage z listą uwag) i znowu przez humanizer.

## Krok 3b. Test zimnego czytania (obowiązkowy od 2026-10-07)

Powód: posty z 5-6.10 przeszły humanizer i akcept, a odbiorcy uznali je za nieczytelne.
Humanizer i brand-voice nie sprawdzają zrozumiałości, ta bramka tak.

Spawn świeżego agenta `general-purpose` (model `sonnet`), który **nie dostaje briefu,
tematu, captionu ani źródła**, tylko sam tekst slajdów danego posta (kicker, tytuł, tekst,
po kolei). Prompt:

```
Jesteś przeciętnym użytkownikiem Instagrama w USA, przewijasz feed. Dla KAŻDEGO slajdu
osobno: (a) streść jednym zdaniem po polsku, co ten slajd mówi; (b) oceń 1-5, jak łatwo
go zrozumieć przy jednym czytaniu; (c) wypisz słowa lub zdania, przy których musiałeś się
zatrzymać i zgadywać. Na końcu: o czym jest cały post i co masz z nim zrobić.
Nie poprawiaj tekstu.
```

Sesja główna porównuje streszczenia z intencją posta. **Bloker:** ocena slajdu poniżej 4,
streszczenie rozjeżdżające się z intencją albo jakikolwiek fragment „musiałem zgadywać".
Bloker wraca do `social-content-writer` z cytatem z testu, a po poprawce test idzie
ponownie. Wynik testu (oceny per slajd) trafia do raportu dla operatora i do promptu
`brand-voice-manager`.

## Krok 4. Render (sesja główna)

```
python scripts/social/render.py <id>        # dla każdego posta z partii
```

Wynik: `social/media/<id>/NN.jpg` i uzupełnione `media[]`. Tekst się nie mieści =
`social-content-writer` dzieli treść na dodatkowy slajd albo przenosi zdanie do captionu.
Nie ściska zdania w skrót i nie zmienia słów pod błąd układu (np. znak interpunkcyjny
spadający do nowej linii). Błąd samego szablonu → `graphic-designer` (`social/templates/`).
Każda zmiana tekstu po renderze wraca do kroku 3b.

## Krok 5. Bramka (sesja główna, w pętli)

```
python scripts/social/social-gate.py --id <id>     # per post
python scripts/social/social-gate.py --all         # na koniec cała kolejka
```

Nie ufaj raportowi agenta, uruchom skrypt sam. Bloker → poprawka u `social-content-writer`
→ humanizer → ponowny render → ponowna bramka, aż 0 blokerów. Ostrzeżenia oceń i opisz
w raporcie.

## Krok 6. Akcept `brand-voice-manager` (YMYL)

Spawn z poleceniem: przeczytaj `social/brand-instagram.md` (checklist §9) i próbkę głosu,
oceń każdy post z partii punkt po punkcie (slajdy z JSON-a i JPEG-i z `social/media/<id>/`,
caption, alt, hashtagi), sprawdź wyrywkowo 1-2 fakty ze źródłem, dołącz wynik testu
zimnego czytania (krok 3b) i każ odrzucić post, którego slajd nie jest zrozumiały bez
kontekstu. Poprawki redakcji też muszą być pełnymi, jasnymi zdaniami. Odpowiedź per post:
AKCEPT albo lista poprawek z cytatami. Poprawki → krok 2 (agent, humanizer) → 4 → 5 → 6.

## Krok 7. Podgląd dla operatora

```
python scripts/social/preview.py --status szkic --nazwa <partia>
```

(albo `--id <id>` kilka razy dla wybranych postów). Pokaż operatorowi ścieżkę
`social/preview/<partia>.html` (otwiera się w przeglądarce) i krótkie
podsumowanie partii:
- tabela: data, godzina ET (i czas polski), typ, temat, źródło, cel CTA;
- wynik `social-gate.py --all` (blokery/ostrzeżenia), werdykt `brand-voice-manager`;
- otwarte kwestie (np. temat graniczny, brak źródła, kolizja dat).

## Krok 8. STOP

Koniec skilla. Posty zostają `szkic`. Zapytaj jednym zdaniem, czy operator akceptuje partię.

**Dopiero na wyraźne polecenie operatora** (całej partii albo wskazanych postów): ustaw
`status: "gotowy"` (z potwierdzonymi `planowana_data` i `planowana_godzina_et`), uruchom
ponownie `social-gate.py --all` (musi być czysty) i zaraportuj, co i kiedy wyjdzie.
Posty, które operator odrzucił: `status: "odrzucony"`. Publikacja i drip: skill `social-publish`.

## Tryb „feature": nowość albo zmiana w aplikacji (post, story, rolka)

Wejście: zmiana w aplikacji (commit/batch we froncie, notatka w memory, kontekst od
`ui-change-detector.py` po `git commit`) albo prośba operatora. Detektor tylko pyta: bez
zgody operatora nic nie powstaje. Kroki (zamiast kroków 0-1, dalej jak zwykle):

F1. **Co się zmieniło, z dowodem.** Commity frontu (`git -C mindsync-frontend log`), notatka
    w memory/`Business_requirements/`, stringi UI z `lib/l10n/app_en.arb`. Spisz 3-5 faktów
    o funkcji językiem użytkownika (co może zrobić, co widzi). Zero możliwości, których
    aplikacja nie ma; zero cen i limitów planu.
F2. **Ekrany.** `python scripts/social/app-shots.py list`; brakujący ekran:
    `python scripts/social/app-shots.py run [--name <shot>]`. Shotu, którego nie ma w harnessie,
    nie robisz sam: zlecenie dla `flutter-mobile` (nowy `*_shot_test.dart` w
    `mindsync-frontend/mindsync_app/test/marketing_shots/`), potem `run`. Obejrzyj każdy PNG
    (Read): czerwony ekran błędu, spinner ładowania albo puste dane = do poprawy w harnessie.
    Sha z kolumny „commit frontu" idzie do `zrodlo.frontend_commit`.
F3. **Format i szablony** (`social/queue/_format.md`):
    - karuzela D: `feature-hero` (okładka) → 2-4 × `feature-step` (lupa `zoom_*` na detal,
      współrzędne w px zrzutu 1179x2556) → opcjonalnie `feature-before-after` (stary ekran
      ze sklepu albo starszy shot, nowy z harnessu) → CTA (`bold-cta`);
    - story: `feature-story`; single: `feature-hero` albo `feature-before-after`;
    - rolka: `reel-text` (hook) → 3-4 × `feature-story` (`ruch: zoom-in` na ekranach) →
      `reel-text` (CTA), 12-20 s, `audio: null`;
    - format agresywny (wariant E, na wyraźne życzenie operatora albo gdy partia ma mieć
      „mocny" post): `aggro-hook`, `aggro-split`, `aggro-story`, cięcia 1.5-2.5 s.
F4. **Treść** pisze `social-content-writer` (blok z kroku 2 + dopisek „TRYB FEATURE: fakty
    z F1, shoty z F2, szablony z F3, `zrodlo: {app_feature, frontend_commit}`, korzyść dla
    użytkownika zamiast żargonu, sceny rolki z `scena_sek`/`przejscie`/`ruch`").
F5. **Render**: `render.py <id>` (karuzela, story, single) albo `reel-render.py <id> --klatki
    <katalog>` (rolka); obejrzyj slajdy i 3-4 klatki rolki (Read).
F6. Dalej kroki 5-8 (bramka, akcept `brand-voice-manager`, `preview.py` i/lub
    `pdf-export.py`, STOP). Rolkę operator ogląda w `social/media/<id>/reel.mp4`.

## Kiedy głos się zmieni

Nowa wersja stylu = nowa wartość `glos` (`monika-v2`), aktualizacja `social-gate.py`
(agent A), `social/brand-instagram.md` i tego skilla.
