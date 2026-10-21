---
name: blog-adaptacja-mindsync-2026-08-25
description: "Adaptacja pipeline'u bloga PLASMET->MindSync (Webflow) wykonana 2026-08-25; stan, ID Webflow, decyzje operatora, otwarte punkty (token Webflow, GSC na innym koncie, akcept brand doc, kroki w Designerze)"
metadata: 
  node_type: memory
  type: project
  originSessionId: ad059625-79a4-4739-9e28-760a04bf7ec7
  modified: 2026-08-26T05:11:23.151Z
---

# Adaptacja systemu blogowego PLASMET → MindSync (2026-08-25) — WYKONANA

Zlecenie: `blog/PROMPT-adaptacja.md`. Architektura procesu bez zmian, wymieniona warstwa
kontekstu. Źródło prawdy stanu: `blog/README.md` (§5 = checklist wykonania).

## Decyzje operatora (z AskUserQuestion, 2026-08-25)
- Odbiorca: mix z priorytetem B2C (osoby w terapii); język: **angielski**; kadencja: **1 wpis/dzień**.
- CMS: istniejąca kolekcja Blog Posts + dodane pola SEO; CTA: karty funkcji + download.
- Brand: ze strony Webflow + handoffów (`colors_and_type.css`) → `docs/blog/brand-mindsync.md` **(czeka na akcept!)**.
- 5 placeholderów szablonowych: unpublish (zrobione; zostały w CMS jako draft).

## Fakty Webflow (potwierdzone przez MCP)
- Site **Mind Sync** `676ed8d44b863915ae191f41` (mindsync.app); kolekcja **Blog Posts**
  `67cb62e9d0afa32a03eae3f1`, slug `journal` → wpisy `/journal/<slug>`, listing = statyczna `/blog`.
- Pola dodane 2026-08-25: `seo-title`, `seo-description`, `hero-alt`, `schema-jsonld` (PlainText).
- Kategorie (Option id): All=7b64b596db0297db6abd52c266d54b08, Therapy=0093a31076e66408265a9d0907d028c2,
  MindSync Tips=9b1d0f4d9dc03f001a8409e1fd7c29c6.
- 2 realne wpisy EN live (digital-burnout-brain-rewiring, regulate-nervous-system-between-therapy-sessions) = wzorzec głosu.
- Store: App Store id6739644256, Play com.mindsync.app. Pricing: trial, $12.99/mo, therapist $10/pacjent.
- **Webflow RichText nie przepuszcza div/style/script/table** → karty [FEATURE:] renderują się
  RichText-safe; blok CTA pobrania i embed schema-jsonld = jednorazowo w szablonie (Designer).

## Co powstało/zmieniono
- Agenci przepisani: blog-writer, seo-content-writer, brand-voice-manager, seo-tech-lead,
  graphic-designer, general-web-search-agent + NOWY `webflow-publisher` (jedyny piszący do Webflow).
- `scripts/webflow/blog-publish.ps1` (drip, Data API v2, DryRun domyślnie, idempotencja po slugu,
  Assets API dla hero, bramki jak w PLASMET) + `.env.example` + README. Parse OK.
- `blog/app-features.json` (katalog 14 funkcji live + site_targets) + `scripts/blog-coverage-preflight.py`
  (KROK 0; smoke-test OK) + `docs/luki-funkcji.md`.
- `blog/queue/_format.md`, `_przyklad.json`, `blog/SCHEMA.md`, `blog/README.md`, `kalendarz-tresci.md`
  (szkielet klastrów), skill `blog-publish` – przepisane. `blog-queue-gate.py` dostosowany
  (kategorie, FAQ „Frequently asked questions", [FEATURE:], zakaz div/style/table/script).
- Prompty hero: `scripts/image-gen/prompts-blog-mindsync/` (styl bazowy + 2 warianty).
- Porządki: przykłady PLASMET → `docs/blog-plasmet-reference/przyklady/`, skrypty Shoper →
  `docs/blog-plasmet-reference/scripts-shoper-api/`, log wyzerowany, CLAUDE.md zaktualizowany.
- **Nazwy pól kolejki zostały POLSKIE** (tytul/tresc_html/status...) – ciągłość narzędzi; treść EN.

## OTWARTE PUNKTY (blokery startu publikacji)
1. **Akcept `docs/blog/brand-mindsync.md`** przez operatora.
2. **`scripts/webflow/.env`**: operator musi wygenerować WEBFLOW_API_TOKEN (Site Settings →
   Apps & Integrations; CMS+Assets read/write). MCP działa bez tego, drip nie.
3. **GSC zablokowane**: token w `scripts/gsc/token.json` = konto PLASMET, widzi tylko
   sklep.plasmet.pl/plasmet.pl. Właściwość mindsync.app jest na INNYM koncie. Fix: (A) dodać
   konto tokena do właściwości mindsync.app w GSC, albo (B) `pull_gsc.py auth` na właściwym
   koncie. Potem `pull_gsc.py sites` → skorygować `site_url` (wpisane zgadywane sc-domain:mindsync.app).
4. **Designer (jednorazowo)**: podpięcie pól seo-title/seo-description w SEO szablonu wpisu;
   custom code `<head>` z polem Schema JSONLD (+ TEST czy Webflow nie escapuje – blog/SCHEMA.md §3);
   statyczny blok CTA pobrania apki w szablonie.
5. **Przegląd `blog/app-features.json`** przez operatora (statusy, cta_url per funkcja,
   screenshoty funkcji – teraz puste, karty renderują się bez obrazka).
6. Test publikatora: DryRun → LIVE na 1 wpisie **za zgodą operatora** → dopiero Task Scheduler
   (07:00, `-DripOne -DryRun:$false`).

## Inwentaryzacja funkcji z kodu (Explore, 2026-08-25) – korekty katalogu
Katalog `blog/app-features.json` ZWERYFIKOWANY z kodem (18 pozycji, 16 live). Kluczowe:
- **streaks = planned**: backend żywy (journey_summary, cron), ale ZERO UI (streak_celebration_generator
  usunięty w CS-04, /character/streaks martwy route, JourneyStrip bez call-site).
- **therapist-sharing = planned**: portal+consent ZBUDOWANE, ale jedyne wejście patient-side ukryte
  w MSV3.4 CS-11 ("unfinished feature") → nieosiągalne. ⚠ Strona www to reklamuje – blog NIE obiecuje.
- **Zakładka Stats USUNIĘTA** (MSV3.2, Workspace zajął slot); wykresy emocji/sentymentu = martwy kod.
  Żywe trendy: MoodTrendCard + symptom_score_chart na Main. Check-iny = "Wellbeing check-ins"
  (oceny focus areas 1-10); "emotional temperature" to sekcja Prep Card, nie osobny check-in.
- Momenty: DAILY_CHECK_IN i SESSION_MORNING_OF generatory USUNIĘTE; REFLECTION_INVITATION żyje;
  13 toggli powiadomień żywych.
- Dopisane do katalogu jako live: workspace, homework, health-check (Therapy Relationship),
  daily-affirmation, mood-trends. Hero insight bez konsumenta UI; eksport PDF backend-only;
  wearables = zero kodu (mimo landingu /pre-order/wearable-ai-journal – adnotacja w site_targets).
- Bottom-nav: Main / Timeline / Reflect / Workspace / Character.
- Kalendarz: klaster "For therapists" ZAMROŻONY do odsłonięcia portalu.

## Sesja testowo-wdrożeniowa (2026-08-25, wieczór)
- **GSC DZIAŁA**: operator autoryzował konto MindSync; `sc-domain:mindsync.app` = siteFullUser;
  testowy pull 2 mies. OK (149 zapytań, 258 klików, 7644 impresji, poz. 6.58) →
  `migracja/gsc/baseline-2026-08-25/`. Config site_url już poprawny.
- **Token Webflow NIE działa**: 403 `missing_scopes cms:read` – operator wygenerował token
  bez zakresów. Fix: nowy token z CMS RW + Assets RW + Sites Read (opis w .env.example).
- **Designer przez MCP Bridge – ZROBIONE (draft, czeka na site Publish operatora!):**
  (1) sekcja „Blog CTA - Download App" w szablonie wpisu (element 24b60992-…) – style
  blog-cta-* w palecie brandu, badge'y reużyte z /freebie (assety: Play=683e0810…c0a4,
  AppStore=683e07b5…1cab; na /freebie alty są ZAMIENIONE, u nas poprawne), copy przez
  humanizer; (2) **JSON-LD = element DOM `<script type=application/ld+json>` z `text`
  ZBINDOWANYM do pola Schema JSONLD** (element dd1608c7-…, koniec body) – kanał lepszy
  niż planowany custom-code w head, zero kroków ręcznych; SCHEMA.md §3 zaktualizowane;
  test escapowania po pierwszej publikacji wpisu ze schemą.
- **Zostało**: (a) nowy token Webflow (operator), (b) krok 1 z webflow-designer-kroki.md
  (podpięcie pól SEO w page settings szablonu – page-settings poza zasięgiem bridge/API),
  (c) site Publish w Designerze (operator), (d) test publikatora na 1 wpisie.

## Runda 2 (2026-08-25, noc): token OK + analiza GSC
- **Token Webflow DZIAŁA** (przegenerowany ze scope'ami; SITE/CMS/ASSETS OK). Kanał API gotowy.
- Operator podpiął pola SEO w szablonie (krok 1) – ale `lastPublished` = 2026-07-25:
  **site Publish wciąż NIEZROBIONY** (CTA + JSON-LD + SEO binding są draftem).
- **Analiza GSC pełnej historii** (16 mies., 2295 klików / 62,3k wyśw., poz. 5.4):
  ~95-97% ruchu = brand/nawigacja; non-brand ~zero → partia 1 z researchu konkurencji,
  GSC nie dyktuje jeszcze tematów. Raport: `seo/blog/gsc-analiza-2026-08-25.md`.
  Kluczowe okazje z danych: `how to use mindsync app` 37 wyśw. poz. 3.5 ZERO klików
  (kandydat #1 partii); `mindsync download` 74+48 wyśw.; nervous-system 43 wyśw. @14.7
  (striking → rozbudowa); pre-order landingi zbierają anonimowy long-tail (duety!);
  /membership 2469 wyśw. CTR 0.77% (meta do poprawy); konfuzja brandowa (mindsync.co 665,
  mind sync meaning 443, ai photo editor). Higiena: /copy/*, /admin---under-construction/*
  rankują na brand → noindex (backlog seo-tech-lead). `blog-tematy.py` zaadaptowany
  (journal/, domena generycznie, markery EN, 365 dni); partia 1 wpisana do kalendarza.

## BLOG WYSTARTOWAŁ NA ŻYWO (2026-08-25 wieczór, za zgodą operatora)
- **Wpis 01 OPUBLIKOWANY**: https://mindsync.app/journal/how-to-use-mindsync (item
  6a8dd78d9711593bac37a6f8); weryfikacja live: karty przeżyły RichText, hero na CDN,
  0 placeholderów/em-dash. Meta/schema/CTA szablonu czekają na site Publish operatora
  (title strony to wciąż dosłowne „MindSync Blog | %s").
- **Rozbudowa 02 WGRANA i opublikowana** (PATCH itemu 69c039b1…): ~3900 słów, FAQ,
  karta debrief, korekty „free app"→out i Laborde→NBR zweryfikowane na żywo.
- **Task Scheduler „MindSync Blog Drip" założony**: codziennie 07:00, StartWhenAvailable,
  forma `-Command` (⚠ `powershell -File` + `-DryRun:$false` NIE działa – bool jako string;
  udokumentowane w scripts/webflow/README).
- Harmonogram dripu: 05→08-28, 06→08-29, 04→08-30, 03→08-31, 08→09-01, 09→09-02, 07→09-03.
- **Fixup linków po 09-03**: `blog/queue/_link-fixup.md` (5 anchorów bez linku w 01 i 02).
- Miesiąc po starcie: pętla striking-distance (blog-tematy.py) + wpisanie image/logo do schem.

## KOREKTA KALENDARZA (2026-08-26 rano)
Operator zgłosił „nie opublikowało się o 7". Diagnoza: **automat zadziałał poprawnie**
(LastRunTime 07:00:01, result 0, log „BRAK wpisow gotowych") – po prostu najwcześniejszy
`gotowy` miał datę 28.08, bo wpis 01 poszedł ręcznie 2 dni przed planem. LEKCJA: publikując
wpis przed jego `planowana_data`, od razu przesuń resztę kolejki, inaczej robi się cisza.
- Wszystkie 7 pozostałych wpisów przesunięte o -2 dni (26.08 → 01.09), nazwy plików
  i `datePublished` w schemach zsynchronizowane; wpis 01 poprawiony na realne 2026-08-25
  (plik + schema + PATCH żywego itemu).
- Drip odpalony ręcznie za dziś: **how-to-prepare-for-a-therapy-session LIVE**
  (item 6a8e7559544fa4cd5c5fcf1e), zweryfikowany: hero, meta, 2 karty, blok CTA, 0 em-dash.
- Kolejny automatyczny: 27.08 how-to-remember…, dalej codziennie do 01.09 (pillar).

## PRZYPOMNIENIE NA PARTIĘ 2 — USTAWIONE (routine w chmurze)
`trig_01NPJqYPKeSBVzoFZgBa7PjT` → **2026-09-10, 09:07 czasu PL** (07:07 UTC), jednorazowe.
https://claude.ai/code/routines/trig_01NPJqYPKeSBVzoFZgBa7PjT
Cloud (nie ma dostępu do lokalnego repo/GSC) – sprawdza przez konektor Webflow, czy cała
partia 1 wyszła i czy pola (main-image, thumbnail, seo-*, schema-jsonld) są wypełnione,
i oddaje brief z komendami do odpalenia LOKALNIE (pull_gsc, blog-tematy, porównanie
z gsc-analiza-2026-08-25.md, backlog partii 2, fixup linków, TODO image/logo w schemach).
⚠ CronCreate NIE nadaje się do takich terminów: joby są session-only i giną z sesją.

## SITE PUBLISH + SCREENY (2026-08-25, ~20:30; „Opublikuj sam" = mandat operatora)
- **Site OPUBLIKOWANY przeze mnie 2×** (MCP publish_site, obie domeny): hero na górze wpisów,
  CSS linków, meta z pól SEO (title działa!), blok CTA – wszystko live.
- **Test schemy: binding NIE przechodzi** – Webflow escapuje tekst pola w <script> (encje
  w raw-text elemencie nie są dekodowane → &quot; literalnie). FIX WDROŻONY: JS w embedzie
  szablonu dekoduje encje (textarea trick), waliduje JSON.parse i podmienia blok; bloki
  niewalidowalne USUWA – to też sprząta śmieciowy blok, który operator wkleił do head
  custom code z mojej instrukcji (dosłowny markdown!). Samoleczące dla wszystkich wpisów.
  ⚠ Weryfikacja pełna wymaga JS (Rich Results Test), curl nie wykona skryptu.
- **Screeny apki = oficjalne z listingu App Store** (operator: „używaj jak uznasz"; 8 szt.
  w blog/images/app-screenshots/): ios-1 debrief, 2 Reflect, 3 Prep, 4 Timeline,
  5 Recording, 6 Workspace; ios-7 (Character) POMINIĘTY – karty bio po polsku;
  ios-8 testimonial. 6 wgranych jako assety Webflow (app-ios-N.webp).
- **Katalog app-features.json: pole screenshot ustawione dla 6 funkcji** → karty [FEATURE:]
  renderują się teraz Z OBRAZKAMI (drip zrobi to automatycznie dla wpisów 05-07).
  Uwaga: plik przeformatowany przez PS roundtrip (& itp. – poprawny JSON).
- **Figury <figure><img> wstawione do queue**: 01×2 (Prep po „Before: the prep card",
  Timeline po „What you get after two weeks"), 04 (Timeline), 03 (Workspace),
  09 (Timeline), 07 (After-therapy). CSS w embedzie: figure img max-height 560px,
  radius, cień. Wpis 01 przerenderowany i zrepublikowany: 3 obrazki live.
- Fałszywych zrzutów UI nie generujemy nadal – store'owe assety są realne.

## FIXY SZABLONU PO FEEDBACKU OPERATORA (2026-08-25, ~20:00; przez MCP Bridge)
Operator zgłosił: brak hero na górze wpisu, niewidoczne linki w treści, ściana tekstu.
- Diagnoza: main-image renderował się w DWÓCH bocznych kolumnach szablonu (Image 28 w
  Column 35, obok tytułu i obok body); linki niewidoczne bo globalny styl `a{color:var(--100)}`
  (jasny wariant na jasnym tle).
- Naprawy w szablonie (DRAFT, czeka na site Publish!): (1) nowa sekcja „Blog Post Hero"
  między headerem a body – Image z bindingiem assetId→Main Image + altText→Hero Alt
  (klucz bindingu obrazka = `assetId`); (2) oba boczne Image 28 USUNIĘTE; (3) HtmlEmbed
  z CSS `.rich-text-block a{color:#26767b;underline}` (element 9bae8d8c…).
- Dwa stare wpisy dostały hero (Gemini, wgrane assetami + PATCH main/thumbnail/hero-alt,
  opublikowane): digital-burnout (scena telefon ekranem w dół) i nervous-system (fale oddechu).
  Wszystkie 3 żywe wpisy mają komplet obrazków; przyszłe mają je z pipeline'u.
- OTWARTE: ożywienie treści (pkt 3 operatora) – czekamy na REALNE screeny apki od operatora
  (do wpisu 01 how-to-use i do pola screenshot w app-features.json → karty CTA z obrazkami);
  plan: 1 brandowa ilustracja śródtekstowa per wpis partii przed jego datą dripu.

## PARTIA 1 WYPRODUKOWANA (2026-08-25, pełny cykl pipeline)
- 8 wpisów EN w `blog/queue/` (2026-08-27..09-03, status **gotowy**) + rozbudowa 02
  (`_02-rozbudowa-output.html` + `_02-schema.json`; edycja żywego itemu CMS 69c039b1…,
  wymaga zgody operatora, w tym korekta „free app"→„built for" w starym tekście).
- Cykl: seo-content-writer (tematy+bramka 9×OK+briefy) → 9× blog-writer równolegle
  (humanizer + weryfikacja źródeł pierwotnych; kilka twierdzeń z briefów WYCIĘTYCH jako
  niepotwierdzone) → brand-voice batch review (B1-B4: rotacja Shiffmana 5→2, founder 3→2,
  kontrakcje w 09 w dół / w rozbudowie w górę, „The honest caveat" 6→2) → poprawki → re-check
  AKCEPT PARTII → schema seo-tech-lead (9 grafów, walidator 1:1 FAQ) → hero 8/8 (Gemini,
  w budżetach wag) → gate 0/0 → DryRun publikatora na 01 CZYSTY.
- Rulingi redakcyjne dopisane przez brand-voice do brand doc §5 (kontrakcje=rozwinięte,
  cyfry od 10, dywizy przydawkowe, godziny US, limity formuł).
- LINK-LATER działa (degradacja do anchora potwierdzona w DryRun).
- CZEKA NA OPERATORA: (a) zgoda na LIVE publikację 01 (test publikatora; -Plik publikuje
  od razu, 2 dni przed planowaną datą), (b) Task Scheduler 07:00 po teście, (c) PATCH
  rozbudowy 02 + schema do pola CMS, (d) **site Publish w Designerze wciąż niezrobiony**
  (CTA, binding schema-jsonld i pola SEO szablonu są draftem – bez tego nowe wpisy
  publikują się bez meta/schemy/CTA w szablonie!). TODO publikatora: wstrzykiwanie
  image/logo do schemy po uploadzie hero (notatka seo-tech-leada).

## Nowe instrukcje dla operatora
- `scripts/gsc/INSTRUKCJA-autoryzacja-mindsync.md` – autoryzacja GSC na koncie MindSync
  (nowy projekt GCP + publish consent screen do Production, żeby refresh token nie wygasał).
- `docs/blog/webflow-designer-kroki.md` – 3 jednorazowe kroki w Designerze (meta z pól CMS,
  embed schema-jsonld, blok CTA); wykonalne też przez Webflow MCP Bridge App przy otwartym
  Designerze. Site publish zawsze robi operator.
- Plan po odblokowaniu: redesign /blog (grid kart z miniaturami, featured, filtry tematyczne –
  decyzja: rozszerzyć category czy dodać kolekcję tagów multi-ref) + struktura szablonu wpisu.

Powiązane: [[reference-backend-autodeploy-on-push]] (nie dotyczy bloga), brand doc =
źródło prawdy dla graphic-designer/brand-voice-manager.
