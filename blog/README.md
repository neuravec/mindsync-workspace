# System produkcji bloga MindSync (Webflow)

> Pipeline „partia + drip" przeniesiony 2026-08-24 z projektu PLASMET (~80 wpisów
> opublikowanych automatem od czerwca 2026) i **zaadaptowany 2026-08-25 pod MindSync**:
> blog po angielsku na mindsync.app (Webflow CMS, kolekcja Blog Posts, wpisy pod
> `/journal/<slug>`, listing `/blog`). Architektura procesu bez zmian; wymieniona
> warstwa kontekstu (branża, agenci, kanał publikacji, bramka pokrycia, brand).
> Oryginalne materiały PLASMET: `docs/blog-plasmet-reference/`.

---

## 1. Jak działa pipeline (przegląd)

```
GSC (realny popyt)          bramka pokrycia            pisanie                jakość                publikacja
────────────────────  →  ─────────────────────  →  ────────────────  →  ────────────────  →  ─────────────────────
scripts/gsc/              blog-coverage-             agent blog-writer     skill humanizer       scripts/webflow/
blog-tematy.py            preflight.py               (per brief + frazy,   (bramka TWARDA)       blog-publish.ps1
blog-partia-frazy.py      (czy apka ma funkcję,      treść EN)             + brand-voice-        (drip 1 wpis/dzień,
(tematy i frazy            do której wpis            + karty [FEATURE:]    manager (akcept)      Task Scheduler 07:00)
 z popytu, nie             prowadzi: katalog         + hero z Gemini       + schema od           + pomiar w GSC
 z głowy)                  blog/app-features.json)                         seo-tech-lead         (regex po /journal/)
```

Kluczowa filozofia (wypracowana na ~80 wpisach PLASMET, obowiązuje 1:1):

1. **Tematy wynikają z danych, nie z burzy mózgów.** Frazy z GSC; dyrektywy frazowe
   NADRZĘDNE nad kreatywnością autora + kontrola kanibalizacji. ⚠ Stan 2026-08-25:
   właściwość GSC mindsync.app jest na innym koncie Google niż token – do odblokowania
   (patrz `scripts/gsc/gsc.config.json`); do tego czasu tematy z researchu konkurencji,
   struktura partii ta sama.
2. **Najpierw pokrycie, potem pisanie (bramka na LIŚCIE TEMATÓW).** Czy MindSync ma
   funkcję/ekran/plan, do którego wpis może uczciwie prowadzić – katalog:
   `blog/app-features.json`, skrypt: `scripts/blog-coverage-preflight.py`. Temat bez
   pokrycia = zmiana kąta albo wypada; braki → `docs/luki-funkcji.md`.
3. **Blog sprzedaje.** Wpis rekomendujący/pokazujący „jak" prowadzi do konkretnej funkcji
   kartą `[FEATURE:]` (nie samym linkiem); bogaty blok pobrania apki siedzi w szablonie
   wpisu (Designer). Bez cen w treści.
4. **Nigdy ślepy zaułek.** Brak idealnego celu = cel pochodny albo strona zbiorcza
   (`/features`). Nigdy donikąd.
5. **Kolejka plikowa + drip.** Wpisy = JSON-y w `blog/queue/` ze statusami
   (`szkic` → `gotowy` → `opublikowany`) i `planowana_data`. Publikator bierze NAJSTARSZY
   `gotowy` z datą <= dziś, publikuje JEDEN dziennie. Idempotencja po slugu + log.
6. **Pisanie tylko ścieżką skilla `/blog-write`** (od 2026-09-25): głos = styl Moniki
   (`docs/blog/brand-mindsync.md` §2, wzorzec `docs/blog/voice-sample-monika.md`), pole
   `"glos": "monika-v1"`, kontrola `scripts/blog-voice-check.py` wpięta w bramkę kolejki.
7. **Humanizer to bramka twarda** przed każdą publikacją prozy + **całkowity zakaz
   em-dash „—"** (także w EN – to sygnał AI).

## 2. Mapa plików w tym repo

### Agenci (`.claude/agents/`, przepisani pod MindSync 2026-08-25)

| Agent | Rola w pipeline |
|---|---|
| `blog-writer.md` | Pisze wpisy EN pod brief; ⛔ każdy tekst przez `humanizer`; YMYL: zero porad medycznych |
| `seo-content-writer.md` | Strategia: frazy, briefy, klastry (`blog/kalendarz-tresci.md`), dyrektywy z GSC, GEO |
| `brand-voice-manager.md` | Redaktor naczelny: głos marki (`docs/blog/brand-mindsync.md`), AKCEPT każdej treści |
| `seo-tech-lead.md` | Technika: schema JSON-LD (blog/SCHEMA.md), meta szablonu, GSC, CWV w realiach Webflow |
| `graphic-designer.md` | Hero: prompty (`scripts/image-gen/prompts-blog-mindsync/`), spec WebP, alt |
| `general-web-search-agent.md` | Research (tani Sonnet); poziomy dowodów dla treści YMYL |
| `webflow-publisher.md` | **Kanał wykonawczy** – jedyny agent piszący do żywego Webflow (API + MCP) |

### Skille (`.claude/skills/`)

| Skill | Co robi |
|---|---|
| `humanizer` | Usuwa sygnały tekstu AI (em-dash TOTAL BAN, AI-slop). Uniwersalny, bez zmian |
| `blog-publish` | Runbook publikacji end-to-end na Webflow (przepisany 2026-08-25) |

### Struktura treści (`blog/`)

```
blog/
  README.md              ← ten plik
  SCHEMA.md              ← JSON-LD: projekt grafu + kanał wstrzyknięcia w Webflow
  app-features.json      ← ⭐ katalog funkcji apki (bramka pokrycia + karty CTA)
  kalendarz-tresci.md    ← mapa klastrów MindSync (szkielet; dane > kolejność)
  published-log.json     ← log opublikowanych (idempotencja dripu; wyzerowany)
  PROMPT-adaptacja.md    ← prompt, którym wykonano adaptację (dokumentacja)
  queue/
    _format.md           ← ⭐ NAJWAŻNIEJSZY DOKUMENT: format JSON-a, mapowanie na Webflow,
                            statusy, bramka KROK 0, karty [FEATURE:], bramki dripu
    _przyklad.json       ← minimalny prawidłowy wpis (EN)
  images/                ← komplety hero per slug: hero-1600x900.* + hero-800x600.*
```

### Skrypty (`scripts/`)

| Skrypt | Co robi | Zależności |
|---|---|---|
| `scripts/gsc/pull_gsc.py` (+ blog-tematy, blog-partia-frazy, frazy-brief) | Popyt/frazy z GSC | ✅ działa na `sc-domain:mindsync.app` (od 2026-08-25) |
| `scripts/gsc/blog-performance.py` | Wyniki opublikowanych wpisów + flagi SNIPPET/KLASTER/NA-PROGU/INTENCJA | ✅ krok 0 każdej partii (skill `blog-write`); lista poprawek: `blog/queue/_gsc-odswiezenia.md` |
| `scripts/blog-coverage-preflight.py` | ⛔ Bramka KROK 0: pokrycie tematu funkcjami apki | `blog/app-features.json` |
| `scripts/blog-queue-gate.py` | Walidator kolejki (blokery/ostrzeżenia; RichText-safe HTML, em-dash, FAQ EN, daty) | – |
| `scripts/blog-tbd-inspect.py` / `blog-tbd-apply.py` | Obsługa placeholderów w kolejce | – |
| `scripts/webflow/blog-publish.ps1` | ⭐ Drip-publikator na Webflow Data API v2 (DryRun domyślnie; bramki; karty; hero przez Assets API; idempotencja po slugu; logi) | `scripts/webflow/.env` (⚠ token do uzupełnienia) |
| `scripts/image-gen/gemini-generate.ps1` + `png-to-webp.py` | Generacja/optymalizacja hero | `GEMINI_API_KEY` w `scripts/image-gen/.env` (jest) |
| `scripts/image-gen/prompts-blog-mindsync/` | Biblioteka promptów hero w stylu MindSync | – |

### Dokumentacja

- `docs/blog/brand-mindsync.md` – ⭐ brand: głos + wizual + słownik (**status: do akceptu**).
- `docs/luki-funkcji.md` – rejestr braków z bramki pokrycia (sygnał produktowy).
- `docs/blog-plasmet-reference/` – całość materiałów PLASMET: zespół agentów, strategia SEO
  (wzorzec dokumentu nadrzędnego), lekcja pomiaru (`ga4-grupa-tresci-blog.md` – regex
  po URL-ach w GSC, NIE grupy treści GA4), przykładowe wpisy/hero (`przyklady/`),
  referencyjne skrypty kanału Shoper (`scripts-shoper-api/` – wzorce odpornościowe)
  i stara bramka asortymentowa.

## 3. Cykl życia wpisu (szczegółowo)

1. **Partia tematów**: `seo-content-writer` (GSC gdy jest; inaczej research) → lista partii.
2. **Bramka pokrycia (KROK 0)**: `blog-coverage-preflight.py --temat ...` na CAŁEJ liście,
   PRZED briefami. BRAK = zmiana kąta / wypada / rejestr luk.
3. **Dyrektywy frazowe**: `blog-partia-frazy.py` (po odblokowaniu GSC) – dosłowne frazy
   do H1/H2 + wykluczenia kanibalizacyjne. Nadrzędne nad briefem.
4. **Briefy**: `seo-content-writer` per temat (fraza główna, struktura, FAQ dosłowne,
   funkcje do kart, linkowanie).
5. **Pisanie**: `blog-writer` → JSON w `blog/queue/` wg `_format.md` (status `szkic`),
   HTML RichText-safe, karty jako `[FEATURE:]`.
6. **Hero**: `graphic-designer` (prompt) → `gemini-generate.ps1` → komplet
   `blog/images/<slug>/` (1600x900 + 800x600, WebP+JPG). Drip nie generuje grafik.
7. **Jakość**: `humanizer` (bramka twarda) + akcept `brand-voice-manager`.
8. **Schema**: `seo-tech-lead` → pole `schema_jsonld` (goły JSON; blog/SCHEMA.md).
9. **Status `gotowy`** + `planowana_data` → wpis czeka w kolejce
   (walidacja: `blog-queue-gate.py`).
10. **Drip**: Task Scheduler 07:00 → `scripts/webflow/blog-publish.ps1 -DripOne
    -DryRun:$false` → 1 wpis: bramki → karty → hero upload → item create/update →
    publish → `published-log.json` + `_drip-log.txt`. Brak `gotowy` = exit 0.
11. **Pomiar**: ruch bloga w GSC regexem po `/journal/`; wnioski wracają do punktu 1
    (pętla striking-distance raz w miesiącu).

## 4. Klucze i dostępy – stan 2026-08-25

- ✅ `scripts/gsc/` – client_secret.json + token.json + config skopiowane (`.gitignore` chroni).
  ⚠ **ALE token = konto PLASMET, nie widzi mindsync.app.** Odblokowanie (jedno z dwóch):
  (A) dodać konto z tokena jako użytkownika właściwości mindsync.app w GSC, albo
  (B) `python scripts/gsc/pull_gsc.py auth` na właściwym koncie. Potem `pull_gsc.py sites`
  i korekta `site_url` w configu (sc-domain vs URL-prefix).
- ✅ `scripts/image-gen/.env` – GEMINI_API_KEY jest.
- ⚠ `scripts/webflow/.env` – **DO UZUPEŁNIENIA** (WEBFLOW_API_TOKEN; wzór `.env.example`).
  MCP Webflow w sesji Claude działa bez tego, ale drip z Task Schedulera wymaga tokenu.

## 5. Checklist adaptacji – stan wykonania (2026-08-25)

1. ✅ Lektura (README, _format, zespol-agentow) + rekonesans Webflow przez MCP.
2. ✅ Agenci przepisani (6 + nowy `webflow-publisher`). Podział ról bez zmian.
3. ✅ Brand: `docs/blog/brand-mindsync.md` (paleta z handoffów apki + głos z żywych
   wpisów) – **czeka na akcept operatora**.
4. ✅ Kanał publikacji: `scripts/webflow/blog-publish.ps1` (wzorce odpornościowe 1:1).
   ⚠ Wymaga tokenu w `.env` + testu DryRun→LIVE na 1 wpisie.
5. ✅ Bramka pokrycia: `blog-coverage-preflight.py` + katalog `blog/app-features.json`
   (**do przejrzenia przez operatora**: statusy, screenshoty, cta_url).
6. ✅ Karty CTA: `[FEATURE:]` (render w publikatorze, RichText-safe; blok pobrania apki =
   jednorazowo w szablonie wpisu – Designer).
7. ⚠ GSC: config poprawiony, `pull_gsc.py` przetestowany – **zablokowane na koncie**
   (patrz §4). Po odblokowaniu: test `pull`, zgłoszenie sitemap.
8. ✅ Hero: `prompts-blog-mindsync/` (styl bazowy + 2 warianty).
9. ⏳ Drip w Task Schedulerze – DOPIERO po teście publikatora (DryRun + LIVE na 1 wpisie
   za zgodą operatora).
10. ✅ Pomiar: zasada „regex po URL-ach w GSC" udokumentowana (referencja: ga4-grupa-tresci).
11. ✅ Porządki: przykłady PLASMET → `docs/blog-plasmet-reference/przyklady/` (+ skrypty
    Shoper → `scripts-shoper-api/`), log wyzerowany, kalendarz-szkielet MindSync.

**Jednorazowe kroki w Designerze (operator / instrukcja od seo-tech-lead):**
podpięcie pól `seo-title`/`seo-description` w SEO szablonu wpisu; custom code `<head>`
szablonu ze `schema-jsonld`; statyczny blok CTA pobrania apki pod treścią wpisu.

## 6. Zasady twarde (nie negocjować)

- ⛔ Humanizer przed KAŻDĄ publikacją prozy, także po poprawkach.
- ⛔ Zero em-dash „—" w generowanym tekście (także EN; półpauza „–" ze spacjami albo przebudowa).
- ⛔ Najpierw pokrycie (bramka na liście tematów), potem pisanie.
- ⛔ Wpis nigdy nie prowadzi w ślepy zaułek.
- ⛔ Publikatory: DryRun domyślnie TRUE; na żywo tylko jawnym przełącznikiem i za zgodą operatora.
- ⛔ Karty bez cen/danych, które statyczny HTML by zamroził.
- Dyrektywy frazowe z danych są nadrzędne nad kreatywnością autora.
- Kolejka plikowa ze statusami jest jedynym źródłem prawdy o tym, co i kiedy wychodzi.
