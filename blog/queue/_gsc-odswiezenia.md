# Poprawki opublikowanych wpisów z danych GSC

Lista robocza dla kroku 0 skilla `blog-write`. Źródło: `python scripts/gsc/blog-performance.py`
(raporty w `seo/blog/gsc-wyniki/`). Każda pozycja ma stan: `OTWARTE`, `W KOLEJCE` (plik
zmieniony, czeka na publikację), `NA ŻYWO` (opublikowane, data do oceny efektu).

Efekt poprawki oceniaj po min. 4 tygodniach, na oknach równej długości przed i po.

## Z przeglądu 2026-09-28 (dane do 25.09)

### 1. is-therapy-worth-the-money: rozbudowa klastra kosztów terapii. OTWARTE
Najmocniejszy temat bloga: cały klaster wariantów na pozycjach 5-10.
- Frazy z GSC: `is therapy worth the cost?` (18 wyśw., poz. 5,3), `is therapy actually worth the cost?` (8, poz. 5,4),
  `is therapy worth the money` (4, poz. 9,2), `is therapy expensive` (3, poz. 19,3),
  `how much is therapy a month` (1, poz. 10), `is therapy worth it` (1, poz. 42).
- Akcja: tryb „przepisz istniejący wpis” w `blog-write`. Dopisać H2 albo FAQ pod
  „Is therapy expensive?” i „How much does therapy cost a month?” (dosłowne brzmienie
  pytań z GSC, liczby tylko ze źródłem). Rozważyć dodanie słowa „cost” do `meta_title`.
- Linkowanie: nowe wpisy o finansach, wyborze terapeuty i końcu terapii
  (`when-to-stop-therapy`, `online-vs-in-person-therapy`) linkują tutaj.

### 2. sunday-scaries: snippet pod realną intencję. NA ŻYWO 2026-09-28 (ocena efektu od 26.10)
134 wyświetlenia, poz. 8,6, 0 kliknięć. Największa widoczna fraza to `sundays feel like saturday`
(43 wyśw.), czyli inna intencja; reszta zanonimizowana.
- Stare: `How to Beat the Sunday Scaries | MindSync`
- Nowe w `2026-09-10_sunday-scaries.json`:
  - meta_title: `Sunday Scaries: Why Sunday Night Anxiety Hits and 4 Fixes`
  - meta_description: `Dread every Sunday evening has a name and a pattern. What causes the Sunday scaries, whether it means you hate your job, and four small fixes that shorten it.`
- 2026-09-28 wypchnięte za zgodą operatora: tylko `seo-title` i `seo-description` (item
  `6aa77f61b0c8d2544194daf9`) + publikacja itemu, bez publikacji strony; `<title>` na żywo potwierdzony curlem.
  Pod `sundays feel like saturday` wpisu NIE przerabiamy.

### 3. therapy-hangover: warianty długości. OTWARTE
`how long does therapy hangover last` (6 wyśw., poz. 13,7). Sprawdzić, czy FAQ ma dokładnie
to pytanie; jeśli nie, dopisać.

### 4. are-mental-health-apps-private: zapytania w stylu promptów AI. OTWARTE
`what ai mental health app will not share my personal data` (poz. 11) i zapytania typu
„about me: senior traveler…”, „context: location…” (prompty asystentów AI szukających
źródeł). Akcja: upewnić się, że FAQ ma pytanie wprost „Which mental health apps don't share your data?”
z odpowiedzią w 2-3 zdaniach, którą da się zacytować bez kontekstu (passage-level citability); jeśli nie ma, dopisać.

### 5. Wpisy NA-PROGU (poz. 8-20): linki wewnętrzne z nowej partii. OTWARTE
`regulate-nervous-system-between-therapy-sessions` (67 wyśw., poz. 12,1),
`what-to-do-when-your-therapist-is-not-the-right-fit` (60, poz. 11,4; fraza z „BetterHelp”).
Każdy nowy wpis partii, który tematycznie pasuje, daje tu jeden link w treści.

### 6. Tematy następnej partii: wokół klastrów, które już łapią. OTWARTE (zaakceptowane 2026-09-28)
Google już łączy nas z trzema tematami, więc nowe wpisy budujemy wokół nich i linkujemy do istniejących:
- koszty terapii (np. jak płacić mniej za terapię, ile sesji potrzeba, terapia a ubezpieczenie),
- zmiana terapeuty i platformy (fraza z „BetterHelp”: jak zmienić terapeutę na platformie online),
- prywatność aplikacji mental health (co apki robią z danymi, na co patrzeć przed instalacją).
Każdy temat i tak przechodzi bramkę pokrycia (`blog-coverage-preflight.py`).

### 7. Stare adresy CMS: przekierowania 301 na trafne wpisy zamiast na /blog. OTWARTE (operator, Webflow Site settings -> Publishing -> 301 redirects)
Stan 2026-09-28 (curl): cztery przekierowują 301 na `/blog`, jeden zwraca 404. Razem ok. 43 wyświetlenia.
Przekierowanie na listę bloga Google traktuje zwykle jak soft 404, trafny wpis przejmuje sygnał.

| Stary adres | Dziś | Proponowany cel |
|---|---|---|
| /journal/therapy-and-progress-4 | 301 -> /blog | /journal/how-to-know-if-therapy-is-working |
| /journal/therapy-progress-1 | 301 -> /blog | /journal/how-to-know-if-therapy-is-working |
| /journal/wellbeing-in-therapy-3 | 301 -> /blog | /journal/what-to-do-between-therapy-sessions |
| /journal/therapy-tracking-2 | 301 -> /blog | /journal/why-mood-tracking-stops-working |
| /journal/therapy-and-wellbeing-5 | 404 | /journal/what-to-do-between-therapy-sessions |

### Zasada oceny
Żadnych głębszych przeróbek istniejących wpisów przed ok. 26.10: blog jest widoczny od dwóch
tygodni, pozycje się układają. Do tego czasu tylko meta, FAQ i linki wewnętrzne.
