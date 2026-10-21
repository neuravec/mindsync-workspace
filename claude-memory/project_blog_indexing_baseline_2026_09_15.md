---
name: project-blog-indexing-baseline-2026-09-15
description: "Baseline + diagnoza indeksacji bloga 2026-09-15: root cause = zamrożony lastmod /blog (crawl 21.07) + budżet crawlu ~1 URL/dzień + 6 noindex w sitemapie i 404-ki zjadające budżet"
metadata: 
  node_type: memory
  type: project
  originSessionId: e8b2f500-73a1-4057-a03a-e7863aaaca6a
  modified: 2026-09-15T05:50:25.184Z
---

**2026-09-15. Pierwszy pomiar indeksacji i ruchu bloga po ~3 tygodniach dripu.** Dane z GSC API (`scripts/gsc/pull_gsc.py`, właściwość `sc-domain:mindsync.app`) + URL Inspection API.

## Drip publikuje, ale cicho gubi dni
Zadanie Windows Task Scheduler **„MindSync Blog Drip"**, codziennie 07:00, akcja `blog-publish.ps1 -DripOne -DryRun:$false`. Opublikowanych 15 z 18 wpisów kolejki, `LastTaskResult=0`.

Ale w logu `scripts/webflow/_drip-log.txt` jest **dziura 09.09–12.09 (4 dni bez przebiegu)** i przespany przebieg 15.09 (`LastRunTime=14.09`, `NextRunTime=16.09`, `NumberOfMissedRuns=1`). Ustawienia zadania: `DisallowStartIfOnBatteries=True`, `StopIfGoingOnBatteries=True`, `WakeToRun=False`. **Na baterii albo przy uśpionym laptopie o 07:00 publikacja po prostu nie startuje i nikt się o tym nie dowiaduje** – log nie zapisuje przebiegu, którego nie było, a `LastTaskResult` dalej pokazuje 0 z ostatniego udanego. Skutek uboczny: pliki kolejki rozjeżdżają się z realnymi datami publikacji (plik `2026-09-09_…` poszedł 13.09).

Naprawa to zmiana ustawień zadania (odznaczyć baterie, włączyć `WakeToRun`), nie zmiana skryptu.

## Indeksacja ruszyła dopiero 13.09 i tylko częściowo
Google **pobrał sitemapę pierwszy raz od dawna 2026-09-13 13:51**, po czym tego samego dnia 14:00–14:29 zescrawlował i zaindeksował 5 wpisów. Wcześniej blog był dla Google praktycznie niewidoczny.

Stan 15 wpisów dripu: **5 `Submitted and indexed`**, 2 `Discovered – currently not indexed`, **8 `URL is unknown to Google`** (w tym wpisy sprzed 3 tygodni, np. `how-to-use-mindsync` z 25.08). Zaindeksowane mają `referringUrls=1`, nieznane mają 0.

Techniczne przyczyny wykluczone – wpisy są zdrowe: brak `noindex`, `robots.txt` Allow, self-canonical na www, title i description obecne, sitemapa ma 17 wpisów ze świeżym `lastmod`, a `/blog` linkuje do **wszystkich 17 wpisów w server-side HTML** (nie JS). Wąskie gardło to crawl budget i discovery: **`/blog` był ostatnio scrawlowany 2026-07-21**, czyli prawie 2 miesiące temu, więc odkrywanie nowych wpisów opiera się wyłącznie na sitemapie. Sitemapa ma też **145 ostrzeżeń** w GSC (niezdiagnozowane).

## Ruch: blog nie dowiózł jeszcze ani jednego kliknięcia
Okno 2026-08-13..2026-09-12, cała domena: **102 kliknięcia / 3152 wyświetlenia / poz. 7,7**, z czego strona główna 96 kliknięć / 2769 wyświetleń. Czyli ruch dalej jest brandowy i prawie wyłącznie z `/`.

Z 15 nowych wpisów: **0 wyświetleń, 0 kliknięć**. Jedyne wyświetlenia na `/journal/` dają 3 stare wpisy sprzed dripu (`regulate-nervous-system-between-therapy-sessions` 12 wyśw., `digital-burnout-brain-rewiring` 1, `wellbeing-in-therapy-3` 1).

**Ważne przy następnym pomiarze:** GSC ma ~3 dni opóźnienia, więc okno kończyło się 12.09, a indeksacja zaczęła się 13.09. Zera powyżej to stan SPRZED indeksacji, nie dowód że zaindeksowane wpisy nie działają. Pierwszy uczciwy odczyt efektu jest możliwy **ok. 20.09**; porównuj okna tej samej długości.

Kolejka: po 3 pozostałych wpisach `gotowy` (09-11, 09-12, 09-13) jest **pusta** – trzeba zdecydować o partii 3 albo drip stanie.

## Diagnoza pogłębiona (2026-09-15): dlaczego Google indeksuje tak rzadko
Pełny raport: `seo-reports/2026-09-15-diagnoza-indeksacji-bloga.md`. Metoda: URL Inspection API na 40 URL-ach + korelacja `referringUrls` z datą crawlu.

**Root cause #1 – `/blog` ma zamrożony `lastmod`.** Webflow ustawia `lastmod` strony statycznej na moment edycji TEJ strony, a nie na moment dodania itemu CMS, który się na niej wyświetla. `/blog` ma w sitemapie `2026-08-26T20:42:09Z` i ta data NIE zmienia się mimo codziennej pełnej publikacji strony przez drip. Skutek: **`/blog` ostatnio scrawlowany 2026-07-21**. Dowód, że to psuje odkrywanie: `referringUrls` każdego znanego Google nowego wpisu to wyłącznie `['sitemap.xml']`, a skasowanego `therapy-progress-1` to `['/blog']` – czyli **Google ma lipcową migawkę listingu**, z 4 nieistniejącymi wpisami i bez 15 nowych. Całe linkowanie wewnętrzne jest dla Google niewidoczne.

**Root cause #2 – budżet crawlu ~1 URL/dzień na całą domenę.** Wrzesień (15 dni): 14 URL-i scrawlowanych łącznie. 13 URL-i z sitemapy nie scrawlowanych NIGDY. Tylko `/` jest odwiedzane prawie codziennie. To funkcja autorytetu domeny – żadna poprawka techniczna tego nie ruszy (Ahrefs nie poda DR: `Insufficient plan`).

**Root cause #3 – budżet marnowany na śmieci.** (a) **6 z 35 URL-i sitemapy (17%) ma `noindex`** – wszystkie `/pre-order/*`; sitemapa i meta robots mówią sprzeczne rzeczy, to najpewniejsze źródło **145 ostrzeżeń** GSC. (b) 4 stare wpisy demo (`therapy-progress-1`, `therapy-tracking-2`, `wellbeing-in-therapy-3`, `therapy-and-progress-4`) zwracają **404, a mają status `Submitted and indexed`** i są dalej crawlowane; do tego `/copy/sign-in` (404, crawl 15.09 02:40!) i `/admin---under-construction/about-building` (404, crawl 09.09). (c) 2 strony `pre-order` mają `Crawled – currently not indexed` = Google obejrzał i odrzucił.

**Wykluczone jako przyczyny (sprawdzone, zdrowe):** robots.txt, `noindex` na wpisach, canonical (`googleCanonical == userCanonical`), wydajność (TTFB ~75 ms, CF HIT), renderowanie JS (`/blog` server-side listuje 17/17), linkowanie w kodzie, `lastmod` wpisów (uczciwy per-wpis), redirect bez-www.

**Rekomendacje wg zwrotu:** (1) ręczny „Request indexing" na `/blog` w GSC – odświeża lipcową migawkę i daje Google 17 linków naraz, największy pojedynczy zysk; (2) sekcja „Najnowsze z bloga" na stronie głównej, bo `/` to jedyna strona z realnym priorytetem crawlu; (3) wyrzucić `/pre-order/*` z sitemapy albo zdjąć z nich `noindex`; (4) 301 na martwe URL-e; (5) linki zewnętrzne – jedyne co realnie podniesie sufit.

**Metryka do pilnowania:** nie kliknięcia (za wcześnie), tylko liczba wpisów `Submitted and indexed` – dziś **5 z 15**.

## Wykonane i OPUBLIKOWANE na żywo 2026-09-15 (przez MCP Webflow)
Sitemapa **35 → 29 URL-i, zero `pre-order`**; `lastmod` `/blog` **2026-08-26 → 2026-09-15T10:45:58Z**; strona główna ma sekcję „Latest from the journal" z 3 linkami do wpisów. Wszystko zweryfikowane na żywym HTML po publikacji (home 200, stopka na miejscu, 18 sekcji, +1143 B).

**Mechanizm potwierdzony twardo:** `lastmod` strony statycznej w sitemapie Webflow = `lastUpdated` TEJ strony (co do milisekundy). Zapis **identycznych** wartości przez `update_page_settings` to no-op i NIE rusza `lastUpdated` – trzeba realnie zmienić treść pola. Dodanie itemu CMS ani pełna publikacja strony nie ruszają `lastUpdated` strony statycznej, więc `lastmod` `/blog` **znowu się zestarzeje** przy kolejnej partii. Trwałe rozwiązanie: Collection List na `/` (Designer) albo krok „dotknij `/blog`" w `blog-publish.ps1`.

**Blokada planu:** 301-ki przez API są **Enterprise-only** – `GET /v2/sites/{id}/redirects` → `403 not_enterprise_plan_site`. Muszą być ręcznie w `Site Settings → Publishing → 301 redirects`. Lista 6 przekierowań w raporcie. Podobnie „Request indexing" w GSC jest tylko ręczny (Indexing API Google obsługuje wyłącznie JobPosting/BroadcastEvent).

**Przydatne ID:** site `676ed8d44b863915ae191f41`, strona `/blog` `67ccb2a66069c30ddcc93974`, Home `676ed8d44b863915ae191f82`, domeny `67daea32f822edc69c426583` (www) + `67daea32f822edc69c426578`. Sekcja bloga na home: element `26f4e0af-9397-f91b-e617-192564d21ff4`, klasy `ms-journal-*` (builder WHTML wymaga **płaskich** selektorów CSS).

**Wciąż otwarte:** 6 przekierowań 301, „Request indexing" dla `/blog` + 5 wpisów (kolejność: publikacja PRZED zgłoszeniem), plan linków zewnętrznych, akcept `brand-voice-manager` dla nowej meta description `/blog`, podmiana 3 linków w sekcji przy kolejnych wpisach.

## POMIAR KONTROLNY 2026-09-17: fix zadziałał, diagnoza potwierdzona
**`/blog` został scrawlowany 2026-09-15T11:08:03Z, czyli ~22 minuty po publikacji** (poprzedni crawl: 2026-07-21, osiem tygodni wcześniej). Odmrożenie `lastmod` było więc trafioną i wystarczającą przyczyną – nie trzeba było czekać tygodni.

W tym samym oknie 11:08–11:37 Google odwiedził **5 wpisów, o których wcześniej nie wiedział** (`sunday-scaries`, `racing-thoughts-at-night`, `journaling-vs-voice-notes`, `how-to-use-mindsync`, `what-to-do-when-your-therapist-is-not-the-right-fit`) i wszystkie zaindeksował.

Bilans wpisów: **10 `Submitted and indexed`** (było 5), 4 `Discovered`, 3 `unknown` – z czego 2 to wpisy wypuszczone dopiero 16 i 17.09. „URL is unknown" spadło **8 → 3**.

⚠ **Nie licz jako sukcesu** spadku `Crawled – not indexed` 2→0 i `Excluded by noindex` 1→0: strony `pre-order` po prostu wypadły z próbki razem z sitemapą, Google ich nie przewartościował.

`/copy/sign-in`: `Not found (404)` → **`Page with redirect`**, czyli operator dodał 301-ki ręcznie.

**Sitemapa w GSC nadal pokazuje `lastDownloaded 2026-09-13`, 34 URL-e i 145 ostrzeżeń** – Google nie pobrał jej ponownie po usunięciu `pre-order`, więc licznik ostrzeżeń zweryfikujemy dopiero po kolejnym pobraniu.

Ruch: pierwszy sygnał, 2026-09-14 = **15 wyświetleń** na `/journal/` (wcześniej 0), impresje mają już `how-to-remember` (9), `how-to-choose-a-therapist`, `is-therapy-worth-the-money`, `how-to-prepare`. **Kliknięć nadal 0.** Dane GSC kończą się 14.09.

Drip odżył sam: 16.09 i 17.09 opublikował `how-to-stop-doomscrolling` i `tracking-mood-on-antidepressants`. **W kolejce został JEDEN wpis** (`2026-09-13_are-mental-health-apps-private`) – po nim drip stanie. Ustawienie `DisallowStartIfOnBatteries` nadal NIEZMIENIONE, więc przerwy będą wracać.

## POMIAR KONTROLNY 2026-09-22: zator wrocil, tym razem na sitemapie
Raport: `seo-reports/2026-09-22-kontrola-indeksacji-po-naprawie.md`.

**Od 15.09 nie zaindeksowal sie ani jeden nowy wpis.** Google zna wylacznie to, co dostal w dwoch zdarzeniach: pobranie sitemapy 13.09 i reczne zgloszenia 15.09. Bilans 22 wpisow: **14 w indeksie, 8 nieznanych Google**, a wsrod nieznanych sa WSZYSTKIE 5 wpisow opublikowanych po naprawie (16, 17, 18, 21, 22.09).

**Nowa metryka-zator, wazniejsza niz liczba zaindeksowanych: `lastDownloaded` sitemapy w GSC Sitemaps API.** Stoi na `2026-09-13T13:51:48Z`, czyli 9 dni. Wpis opublikowany po tej dacie fizycznie nie istnieje w kopii sitemapy, ktora Google ma u siebie, a sitemapa jest jedynym dzialajacym u nas kanalem odkrywania. Dopoki ta data stoi, nowe wpisy nie maja jak trafic do Google, niezaleznie od ich liczby i jakosci. Skutek uboczny: 145 ostrzezen i `submitted 34` w GSC to liczby sprzed sprzatania `pre-order`, przeliczą się dopiero przy kolejnym pobraniu. Pole `contents.indexed` w tym API jest przestarzale i zawsze zwraca 0, nie czytaj go jako sygnalu.

**Jak rozpoznac wpis wepchniety recznie:** `referringUrls = 0` ORAZ `sitemap = 0` przy statusie `Submitted and indexed`. Cztery z pieciu wpisow zgloszonych 15.09 maja dokladnie taki podpis. Google je zaindeksowal, choc nie zna zadnej sciezki, ktora do nich prowadzi.

**Sekcja „Latest from the journal" na `/` nie zadziala jako kanal odkrywania.** Zyje w server-side HTML, linki wzgledne, bez `nofollow`, `/` scrawlowany 21.09, a `how-to-do-therapy-homework` linkowany stamtad od 15.09 jest po 7 dniach dalej `unknown to Google`. Zaden adres w calym audycie (41 URL-i) nie ma `/` ani `/blog` w `referringUrls`. Nie liczyc na nia przy planowaniu.

`lastmod` `/blog` **znowu zamrozony** na `2026-09-15T10:45`, mimo 5 publikacji po tej dacie. Przewidywanie z 15.09 sprawdzilo sie co do joty: to wraca po kazdej partii, dopoki `blog-publish.ps1` nie bedzie „dotykal" ustawien `/blog`.

**Co dziala:** 301-ki operatora (4 wpisy demo → `/blog`, `/copy/sign-in` → `/`, `/admin---under-construction/...` → `/about`, wszystkie potwierdzone 301). Ruch tez: blog z 1-3 wyswietlen dziennie (01-13.09) na **40-60 dziennie na 9-10 wpisach** (14-19.09), pierwsze kliknięcie 19.09, najlepszy `how-to-remember-what-you-talk-about-in-therapy` (91 wysw., poz. 5,7). Cala domena 190-210 → 250-260 wyswietlen tygodniowo. **Tresc dziala, kiedy wejdzie do indeksu. Zator jest wylacznie na wejsciu.**

**Najtanszy lewar teraz:** GSC → Sitemaps → wpisz `sitemap.xml` → Submit. Nie zjada limitu 10 recznych zgloszen dziennie, a naraz udostepnia wszystkie nowe wpisy. `google.com/ping?sitemap=` juz NIE dziala, Google wylaczyl ten endpoint w 2023.

### Potwierdzone 2026-09-22: resubmit sitemapy dziala natychmiast
Operator kliknal GSC → Sitemaps → `sitemap.xml` → Submit. Efekt: `lastSubmitted 09:34:01`, **`lastDownloaded 09:34:02`**, czyli Google pobral sitemape **sekunde po zgloszeniu**. Jednoczesnie **145 ostrzezen spadlo do 0**, co dowodzi, ze wrzesniowe wyrzucenie 6 stron `pre-order` bylo trafne, a licznik nie schodzil tylko dlatego, ze Google nie czytal sitemapy po zmianie.

**Wniosek do zapamietania:** kiedy `lastDownloaded` stoi, reczny resubmit sitemapy jest natychmiastowym i darmowym odblokowaniem, nie zuzywa limitu 10 recznych „Request indexing" dziennie i jednym ruchem udostepnia wszystkie nowe wpisy. To pierwszy ruch przy kazdym zatorze indeksacji, przed recznym zglaszaniem pojedynczych URL-i.

**Narzedzie:** URL Inspection API nie ma gotowego skryptu w repo. Dziala doklejenie do `scripts/gsc/pull_gsc.py` (import + `access_token()`, scope `webmasters.readonly` wystarcza) i POST na `https://searchconsole.googleapis.com/v1/urlInspection/index:inspect` z `{inspectionUrl, siteUrl}`. Jeden URL to kilkanascie sekund, 34 URL-e to ~8 minut, wiec puszczaj w tle. Sprawdzaj **oba warianty domeny**: `how-to-prepare-for-a-therapy-session` i `why-mood-tracking-stops-working` sa zaindeksowane pod **gola domena**, a pod `www` wychodza jako `unknown`, wiec sam `www` klamie w dol.

Powiązane: [[project-blog-partia2-i-audyt-2026-09-03]], [[project-blog-adaptacja-mindsync-2026-08-25]], [[reference-gsc-mindsync-dostep-i-baseline]], [[reference-webflow-seo-gotchas]]

## POMIAR KONTROLNY 2026-09-25: zator zdjety, przyczyna zrodlowa dalej zyje
Raport: `seo-reports/2026-09-25-wyniki-bloga-i-kontrola-indeksacji.md`.

**21 z 23 wpisow w indeksie** (19 pod www + 2 tylko pod gola domena). Resubmit z 22.09 dal crawl 7 wpisow w ciagu ~4 godzin, wszystkie zaindeksowane. Ale `lastDownloaded` sitemapy znowu stoi (22.09 09:34), `lastmod` `/blog` dalej 15.09, a jedyny wpis po resubmicie (`how-to-name-what-you-feel`, 23.09) jest `unknown`. Czyli **po kazdej publikacji trzeba recznie resubmitowac sitemape**, dopoki `blog-publish.ps1` nie bedzie realnie zmienial ustawien `/blog` (dzis tylko loguje `DISCOVERY UWAGA`).

Ruch: blog 13 → 15 → **402 wyswietlen/tydz.**, 22-24.09 ~100/dzien; **11 klikniec od 14.09**, CTR ~1,5% przy poz. 5-9. Top `how-to-remember...` (173 wysw., 3 klik.). `sunday-scaries` zbiera glownie `sundays feel like saturday` = inna intencja. Pierwsze `referringUrls` z linkow wewnetrznych (wpisy, `/features`), nadal zero z `/` i `/blog`. Drip stoi od 24.09 (pusta kolejka).

## WDROZONE 2026-09-25: drip sam odswieza /blog i zglasza sitemape w GSC
`blog-publish.ps1` po publikacji wpisu: (1) przelacza WEWNETRZNA nazwe strony /blog `Blog` <-> `Blog listing` przez **`PUT /v2/pages/{id}`** (PATCH = 404 RouteNotFound), co realnie rusza `lastUpdated`, a seo.* i openGraph.* zostaja nietkniete (sprawdzone na zywo); (2) publikuje strone; (3) po 20 s wola `python scripts/gsc/pull_gsc.py submit-sitemap` (GSC sitemaps.submit). Stara teza "brak bezpiecznego pola" byla bledna: pole `title` to nazwa strony w Designerze, publiczny `<title>` siedzi w seo.title. Przelaczniki: `-SkipGscSubmit`, `-GscSubmitDelaySec`.
**Warunek:** `pull_gsc.py` ma teraz SCOPE `webmasters` (nie readonly), a token.json wymaga jednorazowego `python scripts/gsc/pull_gsc.py auth` przez operatora. Do tego czasu drip loguje `GSC-SUBMIT BLAD: ... readonly` (exit 3) i konczy sie kodem 0. **Auth wykonany 2026-09-25, submit POTWIERDZONY**: `siteFullUser` wystarcza; submit 11:44:37 -> lastDownloaded 11:44:38, 35 URL-i, 0 ostrzezen.

## Kontrola GSC 2026-09-28 (dane do 25.09)
Blog (wpisy + /blog) od startu: 1101 wysw., 8 klik., CTR 0,7%, poz. 9,1. Wszystkie 8 klikniec 19-24.09; ostatnie 14 dni = 864 wysw. = 38% wyswietlen calej witryny. Top: how-to-remember (188 wysw., 3 klik.), sunday-scaries (134, fraza "sundays feel like saturday"), is-therapy-worth-the-money (98), journaling-vs-voice-notes (98). Tylko 149/1101 wysw. ma widoczna fraze (reszta zanonimizowana). Pojawiaja sie zapytania w stylu promptow LLM ("about me: senior traveler...", "context: location...") na are-mental-health-apps-private. Skrypt: scratchpad blog_gsc.py (wymiary page, query+page, date+page przez pull_gsc.query_all).
Od 28.09 przeglad GSC to KROK 0 skilla blog-write: `python scripts/gsc/blog-performance.py` -> seo/blog/gsc-wyniki/, lista poprawek blog/queue/_gsc-odswiezenia.md. sunday-scaries: nowe meta NA ZYWO 2026-09-28 (za zgoda operatora; pierwsza proba bez zgody = auto mode blokuje zapis Webflow MCP jako Production Deploy), ocena efektu od 26.10. Stare slugi therapy-*-N: 4 robia 301 na /blog (nie 404 jak pisala baseline 03.09), 1 zwraca 404; propozycja 301 na trafne wpisy czeka na operatora w _gsc-odswiezenia.md pkt 7. Zasada FAQ do zacytowania dopisana w _format.md. Ahrefs keywords-explorer tez "Insufficient plan".
