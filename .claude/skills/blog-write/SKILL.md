---
name: blog-write
description: >
  JEDYNA ścieżka pisania i przepisywania wpisów bloga MindSync (mindsync.app/journal, EN)
  stylem Moniki, naszej specjalistki od komunikacji (głos obowiązujący od 2026-09-25).
  Używaj ZAWSZE, gdy ktoś prosi o nowy wpis, partię wpisów, artykuł na bloga, szkic,
  przepisanie albo poprawę treści wpisu („napisz wpisy na bloga", „nowa partia",
  „przepisz wpis nowym stylem", „/blog-write"). Prowadzi: temat → bramka pokrycia → brief →
  blog-writer (próbka głosu + humanizer) → mechaniczna kontrola głosu → akcept
  brand-voice-manager → hero i schema → status `gotowy`. Publikacja to osobny skill
  `blog-publish`.
---

# Pisanie wpisów bloga MindSync stylem Moniki: runbook

Ten skill istnieje po to, żeby każdy wpis szedł jedną ścieżką i brzmiał jak newslettery
Moniki. Źródła prawdy (nie duplikuj ich treści, czytaj je):

| Co | Gdzie |
|---|---|
| Specyfikacja głosu, szkielet, adaptacja, checklist | `docs/blog/brand-mindsync.md` §2 |
| Wzorzec dosłowny (newslettery #17 i #24) | `docs/blog/voice-sample-monika.md` |
| Format JSON kolejki i mapowanie na CMS | `blog/queue/_format.md` |
| Katalog funkcji do kart `[FEATURE:]` | `blog/app-features.json` |
| Pipeline całości | `blog/README.md` |

## Zasady twarde (bez wyjątków)

1. **Sesja główna nie pisze prozy wpisu sama.** Nawet jeden krótki wpis albo „szybka
   poprawka akapitu” idzie przez agenta `blog-writer`. Sesja główna orkiestruje.
2. **Każdy wpis ma w JSON-ie pole `"glos": "monika-v1"`.** Bez niego
   `scripts/blog-voice-check.py` blokuje wpis, a bramka kolejki ostrzega.
3. **Humanizer zawsze z próbką głosu** (`docs/blog/voice-sample-monika.md` jako writing
   sample). Zakaz em-dash i półpauzy wygrywa z próbką.
4. **Status `gotowy` dopiero, gdy** `blog-voice-check.py` i `blog-queue-gate.py` mają
   0 blokerów, a `brand-voice-manager` zaakceptował wpis checklistą §2.5.
5. **Nic nie idzie na żywo z tego skilla.** Publikacja: skill `blog-publish`, live tylko
   za jawną zgodą operatora.
6. W promptach subagentów: zakaz `run_in_background`, lista kroków do końca, raport na końcu.

## Krok 0. Przegląd GSC opublikowanych wpisów (przed każdą nową partią)

Nowe wpisy piszemy dopiero, gdy wiemy, co z już opublikowanych trzeba poprawić. Sesja
główna (subagent bez terminala tego nie uruchomi):

```
python scripts/gsc/blog-performance.py
```

Wynik: `seo/blog/gsc-wyniki/BLOG-WYNIKI-<data>.md` (sumy bloga, trend tygodniowy, ranking
wpisów, frazy per wpis, flagi). Co robić z flagami:

| Flaga | Znaczy | Akcja w tej partii |
|---|---|---|
| `SNIPPET` | duże wyświetlenia, pozycja do 10, CTR ok. 0 | nowy `meta_title` i `meta_description` pod realne zapytania |
| `KLASTER` | min. 3 warianty tej samej frazy | H2 albo pytanie FAQ pod warianty (tryb „przepisz istniejący wpis”, fakty zostają) |
| `NA-PROGU` | pozycja 8-20, sensowne wyświetlenia | linki wewnętrzne do tego wpisu z nowych wpisów partii (dopisz do briefu w kroku 2) + ewentualna rozbudowa |
| `INTENCJA` | główna fraza nie pasuje do tematu wpisu | sprawdź SERP; nie przerabiaj wpisu pod cudzą intencję, najwyżej doprecyzuj snippet |

Konkretne zaległe poprawki i ich stan: `blog/queue/_gsc-odswiezenia.md`. Otwarte pozycje
z tej listy wchodzą do partii jako osobne zadania (przez `blog-writer` dla prozy, przez
`seo-content-writer` dla samych meta), a tematy z flagą `KLASTER` lub `NA-PROGU` podpowiadają
też tematy wpisów, które mogą do nich linkować. Na koniec raportu dla operatora: które
poprawki weszły do partii, które czekają. Poprawka już opublikowanego wpisu idzie na żywo
tą samą ścieżką co każdy wpis (`blog-publish`, za zgodą operatora).

## Krok 1. Temat i bramka pokrycia

- Temat podał operator → bierz go. Brak tematu → `seo-content-writer` proponuje partię
  (GSC przez `scripts/gsc/blog-tematy.py`, inaczej research).
- Dla listy tematów, PRZED briefem: zapisz tematy z keywordami do
  `blog/queue/_preflight-<partia>.json` (format `{ "temat": ["keyword", ...] }`, wzór:
  poprzednie `_preflight-partia*.json`) i uruchom
  `python scripts/blog-coverage-preflight.py --temat blog/queue/_preflight-<partia>.json`.
  Subagent bez terminala nie uruchomi skryptu: sesja główna robi to sama.
  Brak pokrycia w apce = zmiana kąta albo temat wypada (wpis zawsze kończy się apką).
- Tryb „przepisz istniejący wpis”: temat i brief już są, krok 2 pomiń, w kroku 3 podaj
  ścieżkę JSON-a i powiedz, że fakty, frazy, FAQ i karty zostają, a zmienia się głos
  i szkielet.

## Krok 2. Brief

Spawn `seo-content-writer`: fraza główna i poboczne, intencja, pytania FAQ dosłownie
z zapytań, funkcje do kart (id z katalogu, status `live`), linkowanie wewnętrzne.
Struktura H2 ma iść za szkieletem z brand doc §2.2 (otwarcie-rozpoznanie, skąd to się
bierze, jak to wygląda, badania, co spróbować, apka, pytanie, FAQ), nagłówki w stylu
§2.1 pkt 12.

## Krok 3. Pisanie (agent `blog-writer`)

Prompt dla `blog-writer` MUSI zawierać ten blok (uzupełnij pola w nawiasach):

```
TASK: Napisz wpis bloga MindSync EN stylem Moniki: [temat]
FILES: blog/queue/[YYYY-MM-DD]_[slug].json (status "szkic", pole "glos": "monika-v1")
BRIEF: [brief z kroku 2 albo ścieżka]
KROKI (wszystkie, po kolei, bez run_in_background):
1. Przeczytaj w całości docs/blog/voice-sample-monika.md i docs/blog/brand-mindsync.md §2.
2. Napisz draft wg szkieletu §2.2: otwarcie-rozpoznanie 60-120 słów, humor przez konkretny
   przesadzony obrazek (2-4 razy, nie przy cierpieniu), badania jako historia z rokiem
   i autorem, uczciwe granice wiedzy, 3-5 kroków w trybie rozkazującym z gotowym zdaniem
   do powiedzenia, akapit o apce w rytmie "This is what... Log... Give it time... Then..."
   z kartą [FEATURE:], ostatnie zdanie przed FAQ = osobiste pytanie do czytelnika.
   Treść bez FAQ 900-1400 słów. Zero anegdot w pierwszej osobie, zero emoji.
3. Uruchom Skill humanizer na drafcie, podając docs/blog/voice-sample-monika.md jako
   writing sample. Zakaz em-dash i półpauzy wygrywa z próbką.
4. Sanity check: fakty, liczby, nazwiska, fraza główna, FAQ i karty przetrwały humanizer.
5. python scripts/blog-voice-check.py [plik] -> popraw do 0 blokerów (każda poprawka
   prozy = ponowny humanizer).
6. python scripts/blog-queue-gate.py -> 0 blokerów dla tego pliku.
DONE_WHEN: plik w kolejce, status "szkic", glos "monika-v1", oba skrypty bez blokerów.
RAPORT: ścieżka pliku, liczba słów, wynik obu skryptów, lista źródeł badań z URL.
```

Partia wpisów: jeden `blog-writer` na 1-2 wpisy (taski ok. 20-40 min), niezależne wpisy
równolegle w jednej wiadomości.

## Krok 4. Kontrola mechaniczna (sesja główna, sama)

```
python scripts/blog-voice-check.py blog/queue/<plik>.json
python scripts/blog-queue-gate.py
```

Nie ufaj raportowi agenta, uruchom oba skrypty sam. `blog-writer` nie ma narzędzia shell
(tylko Read/Write/Edit/Web/Skill), więc kroki 5-6 z jego promptu sprawdza ręcznie, a ten krok
jest jedyną prawdziwą kontrolą. Bloker „brak pliku hero” w `blog-queue-gate.py` jest na tym
etapie oczekiwany (hero powstaje w kroku 6), reszta blokerów nie. Bloker → wraca do `blog-writer`
(SendMessage z listą blokerów). Uwagi `pierwsza osoba "..."` sprawdź ręcznie: opinia jest
OK, zmyślona historia z życia nie.

## Krok 5. Akcept głosu (`brand-voice-manager`)

Spawn z poleceniem: przeczytaj próbkę i §2, oceń wpis checklistą §2.5 punkt po punkcie,
sprawdź wyrywkowo 2 badania ze źródłem, odpowiedz AKCEPT albo lista poprawek z cytatami.
Test końcowy: „czy to brzmi jak jej newsletter #24 z odrobiną #17?”. Poprawki → krok 3
(blog-writer, humanizer, skrypty) → ponowny akcept.

## Krok 6. Hero i schema

Wg skilla `blog-publish`: hero od `graphic-designer` (`blog/images/<slug>/`), pole
`schema_jsonld` od `seo-tech-lead` (`blog/SCHEMA.md`), pole `kolor` z zestawu brandowego.

## Krok 7. Status `gotowy`

Ustaw `status: "gotowy"` i `planowana_data` (bez dziur i kolizji; pokaże je
`blog-queue-gate.py`). Ostatni przebieg obu skryptów musi być czysty. Raport dla operatora:
lista wpisów z datami, wynik skryptów, werdykt `brand-voice-manager`, otwarte kwestie.
Publikacja na żywo = osobna decyzja operatora przez `blog-publish`.

## Kiedy głos się zmieni

Nowa wersja stylu = nowa wartość pola (`monika-v2`) i aktualizacja `GLOS` w
`scripts/blog-voice-check.py`, `GLOS_MONIKA` w `scripts/blog-queue-gate.py` oraz tego skilla.
