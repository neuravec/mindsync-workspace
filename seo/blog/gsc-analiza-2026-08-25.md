# Analiza GSC mindsync.app – kontekst pod start bloga (2026-08-25)

Źródło: pełna historia właściwości `sc-domain:mindsync.app`, 2025-04-24..2026-08-22
(surowe dane: `migracja/gsc/baseline-2026-08-25/`: 287 zapytań, 35 stron, 410 par
query×page). Autor: sesja adaptacyjna bloga. Odbiorcy: `seo-content-writer` (partia 1),
`seo-tech-lead` (higiena), operator (decyzje).

## 1. Profil ruchu: to jest domena brandowa, nie contentowa (jeszcze)

- 16 miesięcy: **2 295 kliknięć / 62 328 wyświetleń, śr. pozycja 5.4** – zdrowo, ALE
  ~95-97% to zapytania brandowe i nawigacyjne: `mindsync` (17,2 tys. wyśw.), `mind sync`
  (6,8 tys.), `mindsync app`, `mindsync ai`, literówki (`mindsyn`, `mindsyc`, `myndsync`).
- Non-brand organic praktycznie nie istnieje. Realne zapytania produktowo-informacyjne to
  pojedyncze wiersze: `therapy journaling app to share with your therapist` (poz. 53),
  `ai journaling coach` (poz. 81), `ai journal therapy` (poz. 4, 1 wyśw.).
- **Wniosek dla pipeline'u:** GSC jeszcze NIE podyktuje tematów partii (sekcje LUKI
  i RANKINGI w `blog-tematy.py` są puste – potwierdzone po adaptacji skryptu). Pierwsza
  partia jedzie z researchu konkurencji wg klastrów (`blog/kalendarz-tresci.md`),
  dokładnie tak, jak przewiduje plan awaryjny w `blog/README.md` §1 pkt 1. Pętlę
  striking-distance włączamy od 1. miesiąca po starcie dripu.

## 2. Natychmiastowe okazje wynikające z DANYCH (nie z teorii)

1. **`how to use mindsync app` – 37 wyśw., pozycja 3.5, ZERO kliknięć.** Nie mamy żadnej
   strony pod tę intencję (klik ląduje w homepage). Wpis „How to use MindSync" /
   getting-started guide (kategoria MindSync Tips) to kandydat #1 partii – jedyny temat,
   który już TERAZ ma popyt potwierdzony w GSC.
2. **`mindsync download` 74 wyśw. + `mindsync app download` 48 wyśw.** (poz. ~7) – intencja
   pobrania bez dedykowanego celu. Do decyzji: sekcja/strona download albo mocniejsze
   sitelinki; wpis blogowy niekonieczny.
3. **Striking distance bloga już istnieje:**
   `journal/regulate-nervous-system-between-therapy-sessions` – 43 wyśw. @ poz. 14,7
   (klasyczny kandydat na ROZBUDOWĘ sekcji/FAQ zamiast nowego wpisu);
   `journal/digital-burnout-brain-rewiring` – 12 wyśw. @ poz. 8,3.
4. **Landingi /pre-order/* zbierają long-tail bez kliknięć:** track-interventions
   (158 wyśw. @ 6,7), tracking-therapy-effectiveness (97 @ 5,9),
   understand-behavioural-patterns (84 @ 13,1), wearable (94 @ 5,5). Zapytania są
   w większości zanonimizowane przez GSC (long-tail), ale sygnał jest jasny: te strony
   Google już lubi → wpisy-partnerzy (duety z frazowym anchorem) + poprawa meta mają
   realny punkt zaczepienia. Priorytet duetów: track-interventions i
   tracking-therapy-effectiveness (najwięcej wyświetleń, dobra pozycja).
5. **`/membership`: 2 469 wyśw., poz. 11,4, CTR 0,77%.** Po podpięciu meta (zrobione
   w Designerze) warto przepisać title/description pod CTR – dziś tytuł nie sprzedaje.
   Na brand query `mindsync` membership wisi na poz. 24 – wzmocnić linkowaniem wewn.
6. **Konfuzja brandowa = osobne zjawisko:** `mindsync.co` (665 wyśw.!), `mind sync meaning`
   (443), `mindsync ai photo editor` (~100 łącznie), `mental sync (program 2.0)` (~150),
   `mindsync consulting/solutions` (~90), `brain sync` (~45). Ludzie szukają INNYCH
   produktów o podobnej nazwie i trafiają na nas. Niska wartość konwersyjna; opcjonalny
   wpis/FAQ „What is MindSync (and what it isn't)" uporządkowałby brand SERP, ale to
   zadanie na koniec kolejki, nie start.

## 3. Higiena (backlog `seo-tech-lead`)

- Na brand rankują strony śmieciowe: `/copy/sign-in` (925 wyśw.), `/copy/home-copy`,
  `/admin---under-construction/*` (2,5 tys. wyśw. łącznie), `/untitled` – do `noindex`
  albo wycięcia z indeksu (obecnie rozmywają brand SERP).
- Placeholdery `/journal/therapy-*` (unpublished 2026-08-25) miały śladowe wyświetlenia
  (~42 łącznie) – ich zniknięcie z indeksu to koszt zerowy, zysk jakościowy.
- `/blog` (109 wyśw. @ 12,7) i `/faq` (141 @ 9,5) rankują tylko na brand – wzmocnią się
  same wraz z treścią.

## 4. Rekomendacja partii 1 (dla `seo-content-writer`)

8-10 tematów w tej proporcji:
- 1× **How to use MindSync / getting started** (jedyny temat z popytem w GSC – pkt 2.1),
- 1× **rozbudowa** nervous-system (pkt 2.3; sekcja/FAQ pod frazy, na które już się
  wyświetla – wyciągnąć z GSC po miesiącu więcej long-taili),
- 2× duety pod /pre-order/track-interventions i /tracking-therapy-effectiveness (pkt 2.4),
- reszta z klastrów 1-3 kalendarza (getting more from therapy / between sessions /
  patterns) wg researchu konkurencji (Ahrefs + skille seo-*).
Bramka KROK 0 (`blog-coverage-preflight.py`) obowiązuje na całej liście PRZED briefami.

## 5. Stan narzędzi po tej analizie

- `scripts/gsc/blog-tematy.py` zaadaptowany pod MindSync (ścieżki /journal/, domena
  generycznie, markery intencji EN, domyślny zakres 365 dni). Wyniki (na razie puste
  sekcje 2-3) w `seo/blog/gsc-frazy/`.
- Pull pełnej historii: `python scripts/gsc/pull_gsc.py pull --months 16 --full`.
- Re-run tej analizy: raz w miesiącu po starcie dripu (pętla striking-distance).
