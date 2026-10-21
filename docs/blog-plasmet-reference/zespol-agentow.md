# Zespół agentów PLASMET

> Mapa agentów Claude Code pracujących nad sklepem PLASMET na Shoper Premium — kto za co odpowiada,
> gdzie są granice i jak przebiega współpraca. Cel nadrzędny: nie tylko migracja Mercatum → Shoper, ale
> **utrzymanie i rozwój** sklepu z ambicją **top 1 w PL** w pozycjonowaniu (SEO + UX).

## Dwie warstwy

- **Warstwa wykonawcza (kanały do sklepu)** — dotykają żywego Shopera:
  - **`shoper-api`** — DANE przez webapi REST (produkty, kategorie, zamówienia, CMS, **301**, konfiguracja).
  - **`shoper-cli`** — WYGLĄD przez Shoper CLI (motyw Storefront: Twig + LESS + moduły).
- **Warstwa strategiczno-twórcza (nowi agenci)** — projektują, piszą, decydują; wdrażają przez warstwę
  wykonawczą:
  - **`ux-designer`** — wygląd i doświadczenie użytkownika (projekt, nie kod).
  - **`graphic-designer`** — grafiki i prompty do generatorów; system wizualny.
  - **`blog-writer`** — wpisy blogowe/poradniki (z obowiązkową bramką `humanizer`).
  - **`brand-voice-manager`** — głos marki i redakcja; nadzór nad CAŁĄ treścią.
  - **`seo-content-writer`** — strategia i treść SEO (frazy, kategorie, opisy, GEO).
  - **`seo-tech-lead`** — techniczne SEO (schema, sitemap, canonical, CWV, 301).
- **Warstwa treści produktowej (fabryka opisów, 2026-07)** — masowa poprawa tytułów i opisów ~7 900
  produktów (Leo nie aktualizuje tych pól — zweryfikowane przed startem):
  - **`product-researcher`** (SONNET — tani) — zwiadowca: web-research po SKU/EAN u producenta, fact-sheety
    z faktami+URL-ami. Cała praca wyszukiwania idzie tu; drodzy autorzy tylko komponują (zmiana 2026-07-07,
    oszczędność tokenów).
  - **`product-desc-writer`** — NOWE tytuły/opisy od zera (thin content); komponuje z fact-sheetów researchera,
    parametry tylko ze źródłem; sam NIE szuka w sieci.
  - **`product-desc-editor`** — poprawa ISTNIEJĄCYCH opisów; specyfikacja = świętość (spec-diff); fakty
    z fact-sheetów researchera, sam NIE szuka w sieci.
  - **`product-desc-auditor`** — niezależna bramka anty-halucynacyjna przed publikacją (APPROVE/FIX/REJECT).
- **Warstwa płatnego ruchu** — wydaje budżet reklamowy (za zgodą usera):
  - **`google-ads-manager`** — strategia i prowadzenie Google Ads (PMax/Search/AI Max, negatywy, feed Merchant Center, budżet 6 000 zł/mc). Źródło: `docs/google-ads.md`.
- **Warstwa danych i finansów (2026-08)** — jedyny kanał do ERP firmy:
  - **`plasmet-db`** (SONNET) – baza **Subiekt GT / InsERT GT na MS SQL**, **TYLKO ODCZYT**. Marże,
    koszt własny sprzedaży, wynik finansowy kanału **Shoper** (baza miesza sprzedaż lokalną, Allegro,
    B2B i sklep.plasmet.pl). Struktura 944 tabel poznana przez indeks w `database/docs/`; odpytywanie
    przez `scripts/plasmet-db/sql.ps1` (dwuwarstwowa bramka zapisu + rollback). ⚠ Wymaga **VPN**.
    ⛔ Zapis do Subiekta wyłącznie przez **Sferę**, nigdy surowym SQL-em. Metodyka i pułapki danych:
    `database/docs/sciagawka-sprzedaz-marza.md`.

## Kto za co odpowiada (i czego NIE robi)

| Agent | Odpowiada za | NIE robi (oddaje do…) |
|---|---|---|
| `ux-designer` | IA, nawigacja, układ stron, CRO, mobile, WCAG, sygnały zaufania (UX) | kod motywu→`shoper-cli`; grafiki→`graphic-designer`; copy→agenci treści |
| `graphic-designer` | bannery, kafelki, ikony, OG, zdjęcia/warianty, infografiki, prompty, system wizualny | osadzenie w motywie→`shoper-cli`; układ/IA→`ux-designer`; treść→agenci treści |
| `blog-writer` | wpisy i poradniki, E-E-A-T, rzetelność techniczna | strategia fraz→`seo-content-writer`; głos→`brand-voice-manager`; publikacja→`shoper-api`/`shoper-cli` |
| `brand-voice-manager` | tone of voice, terminologia, standardy, **akcept treści** | tech SEO→`seo-tech-lead`; układ/grafika→`ux`/`graphic`; masowa produkcja→`seo-content-writer` |
| `seo-content-writer` | słowa kluczowe, briefy, treść kategorii/opisów, linkowanie, GEO | wdrożenie tech→`seo-tech-lead`; proza bloga→`blog-writer`; akcept tonu→`brand-voice-manager` |
| `seo-tech-lead` | schema, sitemap, canonical, robots/llms, CWV, 301 (poprawność) | treść/copy→`seo-content-writer`/`blog-writer`; wdrożenie→`shoper-cli`/`shoper-api` |
| `google-ads-manager` | strategia/prowadzenie Google Ads, negatywy, feed Merchant Center, budżet, stawki, kreacja, integralność konwersji | mutacje konta bez zgody usera; fundament GA4/GTM (runbook analityki); SEO organiczne→agenci SEO; copy reklam→`seo-content-writer`+`brand-voice-manager`(+`humanizer`); assety→`graphic-designer` |
| `product-desc-writer` | NOWE tytuły i opisy produktów (thin content), research u producenta, mapa parametr→źródło | publikacja→`shoper-api`; audyt→`product-desc-auditor`; poprawa istniejących→`product-desc-editor`; frazy→`seo-content-writer` |
| `product-desc-editor` | poprawa ISTNIEJĄCYCH opisów (higiena HTML/mojibake, struktura, SEO) ze spec-diff; zmiana liczby tylko z dowodem u producenta | publikacja→`shoper-api`; audyt→`product-desc-auditor`; opisy od zera→`product-desc-writer`; short_description (GPSR) nie rusza bez polecenia |
| `product-desc-auditor` | niezależna weryfikacja tytułów/opisów: tożsamość SKU, liczby znak po znaku, halucynacje, zestawy; werdykt APPROVE/FIX/REJECT | nie redaguje treści (zwraca autorowi); nie publikuje; przy wątpliwości nie przepuszcza |
| `plasmet-db` | odczyt bazy Subiekt GT: marże per SKU/marka/okres, koszt własny, wynik finansowy kanału Shoper, kontrola jakości danych finansowych | ⛔ jakikolwiek zapis do Subiekta (tylko Sfera, i nie jego ręką); dane sklepu przez webapi→`shoper-api`; decyzje o stawkach i budżecie→`google-ads-manager` + user; treść→agenci treści |

## ⛔ Zasada twarda: humanizer

Każdy tekst **prozą** (wpisy bloga, copy stron, opisy) **musi** przejść przez skill **`humanizer`**
(`.claude/skills/humanizer/`) przed publikacją — bez wyjątków, także po poprawkach. Pilnuje tego
`blog-writer` (proza wpisów) i `brand-voice-manager` (weryfikacja, że humanizację wykonano). Wyjątek:
czyste snippety techniczne (JSON-LD, kod, robots/llms) — to nie proza. Skill przeniesiony 1:1 z projektu
NeuraVec-Ebook (wersja 2.5.1, bazuje na Wikipedia „Signs of AI writing").

## Typowe przepływy współpracy

**Nowy wpis na blog**
`seo-content-writer` (brief + frazy) → `blog-writer` (draft) → **`humanizer`** → `brand-voice-manager`
(akcept) → `graphic-designer` (oprawa) + `ux-designer` (layout wpisu) → `seo-tech-lead` (schema Article/FAQ)
→ `shoper-api` (publikacja treści) + `shoper-cli` (szablon wpisu).

**Treść SEO kategorii (likwidacja thin contentu)**
`seo-content-writer` (treść wg szablonu) → **`humanizer`** (proza) → `brand-voice-manager` (akcept) →
`seo-tech-lead` (schema/canonical/meta) → `shoper-api` (zapis pola treści kategorii).

**Redesign strony / komponentu**
`ux-designer` (specyfikacja + kryteria akceptacji) ↔ `graphic-designer` (zasoby) ↔ `seo-tech-lead`
(CWV/schema/mobile) → `shoper-cli` (implementacja w motywie).

**Migracja: ciągłość SEO (mapa 301)**
`seo-tech-lead` (poprawność i kompletność mapowania URL, pułapki routingu Mercatum) → `shoper-api`
(wykonanie importu przekierowań) → `seo-tech-lead` (weryfikacja: brak pętli/łańcuchów, indeksacja w GSC).

**Opis produktu**
`brand-voice-manager` (szablon) → `seo-content-writer` (treść pod frazy, bez stuffingu) → **`humanizer`**
→ `brand-voice-manager` (akcept) → `shoper-api` (zapis), zdjęcia/warianty od `graphic-designer`.

**Masowa poprawa tytułów i opisów produktów (fabryka opisów, 2026-07)**
`seo-content-writer` (brief fraz per kategoria) + `brand-voice-manager` (standard/słownik — raz na start,
potem wyrywkowe kontrole partii) → **`product-desc-writer`** (opis od zera, thin content) LUB
**`product-desc-editor`** (poprawa istniejącego, spec-diff) → **`humanizer`** (proza; liczby nietykalne)
→ **`product-desc-auditor`** (niezależna weryfikacja źródeł; FIX wraca do autora) → `shoper-api`
(backup starych wartości → zapis `translations.pl_PL.name`/`description` przez webapi).
Zasady twarde: parametr bez źródła nie istnieje; publikacja tylko po APPROVE; partie z backupem
umożliwiającym rollback; `permalink` produktów NIE jest zmieniany (ciągłość URL/SEO).

**Kampania Google Ads (PMax/Shopping)**
*Warunek wstępny:* poprawny pomiar (`docs/analityka.md` — Enhanced Conversions, dedup, Consent Mode v2). →
`google-ads-manager` (strategia, struktura, budżet) ← feed/atrybuty: `seo-content-writer` + dane `shoper-api`
(Merchant Center) ← assety: `graphic-designer` ← copy reklam: `seo-content-writer`/`brand-voice-manager` +
**`humanizer`** ← jakość LP/QS: `seo-tech-lead`/`ux-designer`. **Zmiany w koncie → propozycja → akcept usera → wykonanie.**

## Jak uruchamiać

Agentów wywołuje sesja główna (orchestrator) przez narzędzie Agent, kierując zadanie do właściwej roli wg
pola `description`. Współpraca między agentami odbywa się przez **jawne przekazania** (deliverables opisane
w każdym agencie) — orchestrator spina łańcuch i przekazuje wyniki dalej. Postęp dokumentujemy w `docs/` i
`migracja/` oraz w pamięci projektu (preferencja: ciągłość między sesjami).
