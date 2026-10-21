---
name: reference-gsc-mindsync-dostep-i-baseline
description: "GSC mindsync.app DZIALA (token przelogowany 25.08); baseline 2026-09-03: 100% klikniec brandowych, blog 0 klikniec"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a9774c70-6009-42cb-bfd1-56d8fc27e23e
  modified: 2026-09-03T09:40:54.772Z
---

**Dostep do GSC mindsync.app DZIALA** (sprawdzone 2026-09-03). `python scripts/gsc/pull_gsc.py sites` zwraca `siteFullUser sc-domain:mindsync.app`. Token przelogowano 2026-08-25 wieczorem, wiec starsze notatki („token z konta PLASMET nie widzi mindsync.app") sa NIEAKTUALNE – poprawione w `scripts/gsc/gsc.config.json` i w [[project-blog-adaptacja-mindsync-2026-08-25]].

Pobranie: `python scripts/gsc/pull_gsc.py pull --months 3 --full` → `migracja/gsc/baseline-RRRR-MM-DD/` (queries, pages, dates, query-page, summary).
⚠ Pobrania z roznym `--months` maja rozne zakresy dat. Baseline z 25.08 to **16 miesiecy** (2025-04-24..2026-08-22), a nie 3, wiec porownanie per-URL miedzy nimi jest obciazone. Porownuj tylko okna tej samej dlugosci z jednego pobrania.

**Ahrefs MCP nie zastapi GSC**: `management-projects` i narzedzia `gsc-*` zwracaja `{"error": "Insufficient plan"}`.

## Baseline 2026-09-03 (okno 2026-06-01..2026-08-31, 92 dni)

Calosc: **353 klikniecia, 11 028 wyswietlen, CTR 3,2%, poz. 6,53**.

**Struktura ruchu – to jest najwazniejsza liczba:**
- `/` (strona glowna) = 9830/11028 wyswietlen (**89%**) i 337/353 klikniec (**95%**)
- zapytania brandowe = **239 z 240 klikniec (100%)**. Niebrandowych klikniec w 3 miesiace: **1**
- czesc „brandowych" to nie my: `mind sync meaning`, `mindsync solutions`, `haptech mindsync`, `sync people szkolenia`, `minds in sync` – kolizja nazwy ze slownikiem i innymi firmami

**Blog `/journal/` jest praktycznie niewidoczny:**
- 77 wyswietlen w 3 miesiace = **0,59% witryny**, **0 klikniec**, poz. 11,31
- dane maja tylko 2 realne wpisy: `regulate-nervous-system…` (42 wysw., poz. 14,93) i `digital-burnout…` (12 wysw., poz. 8,33)
- **8 wpisow opublikowanych dripem 25.08-01.09 ma ZERO wierszy w GSC** (dane koncza sie 31.08, wiec mialy 0-6 dni + 6 z nich nie bylo w sitemapie do 03.09)
- **0 par zapytanie-strona** dla bloga: zadne zapytanie nie kojarzy sie jeszcze z wpisem
- listing `/blog`: 99 wysw., 0 klikniec, poz. 15,07

**Trend tygodniowy** (W23-W35): klikniecia plaskie 17-46/tydz., wyswietlenia plaskie 750-1030/tydz., pozycja dryfuje w gore (gorzej) z ~5,7 na ~8,1. Dryf zaczal sie PRZED poprawkami SEO z 26.08.

**Efekt poprawek SEO z 26.08 jest NIEMIERZALNY**: dane GSC koncza sie 31.08 (opoznienie ~3 dni), czyli okno po poprawkach ma 6 dni. Okna rownej dlugosci: 620→583 wysw., 19→17 klik., poz. 7,10→9,58. To szum, nie sygnal. Realna ocena mozliwa najwczesniej po ~4-6 tygodniach od naprawy sitemapy (03.09).

Stare slugi zbierajace jeszcze wyswietlenia (`/journal/therapy-progress-1`, `/untitled`, `/copy/sign-in`, `/admin---under-construction/*`) zwracaja **404** – wygasaja z indeksu same, nie wymagaja akcji.

Powiazane: [[project-blog-partia2-i-audyt-2026-09-03]], [[project-seo-overhaul-mindsync-2026-08-26]], [[reference-webflow-seo-gotchas]]
