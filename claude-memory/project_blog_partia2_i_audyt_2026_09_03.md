---
name: project-blog-partia2-i-audyt-2026-09-03
description: "Partia 2 bloga MindSync (10 wpisów 09-04..09-13, status gotowy) + audyt żywych wpisów: zamrożona sitemap, martwe LINK-LATER, og:image, linki bez www"
metadata: 
  node_type: memory
  type: project
  originSessionId: a9774c70-6009-42cb-bfd1-56d8fc27e23e
  modified: 2026-09-03T09:33:26.478Z
---

**2026-09-03. Audyt 10 żywych wpisów `/journal/` + zbudowana partia 2 kolejki (10 wpisów, daty 2026-09-04..2026-09-13, wszystkie `gotowy`).** Bramka kolejki: 0 blokerów, 0 ostrzeżeń, 18 plików.

## Audyt żywych wpisów – co było zdrowe
Wszystkie 10 wpisów: HTTP 200, na listingu `/blog`, klikalne, dokładnie 1× H1, hero na każdym, alt na wszystkich obrazkach, title 44-58 zn., meta description 147-161 zn., self-canonical na www, JSON-LD parsuje się po dekoderze JS w szablonie, 1083-3628 słów. Linkowanie wewnętrzne istnieje (pillar `what-to-do-between-therapy-sessions` linkuje do 7 sióstr).

## Cztery realne problemy (2 naprawione, 2 otwarte)
1. **Sitemap zamrożony** – NAPRAWIONY publikacją strony. Mechanizm i diagnostyka: [[reference-webflow-seo-gotchas]] pkt 12. Drip ma teraz krok publikacji strony.
2. **5 martwych `[LINK-LATER:]` z partii 1** – OTWARTE. Rejestr z anchorami i item_id: `blog/queue/_link-fixup.md`. Partia 2 dołoży 5 kolejnych, fixup po 2026-09-13. Szczegóły mechanizmu: [[reference-webflow-seo-gotchas]] pkt 13.
3. **`og:image` identyczny na wszystkich 10 wpisach** – OTWARTE. Szablon wpisu podaje generyczną grafikę strony zamiast hero z CMS. Do podpięcia w Designerze (SEO szablonu Blog Posts → og:image = pole `main-image`).
4. **Wszystkie linki w treści na `https://mindsync.app` (bez www) → 301** – OTWARTE dla partii 1. Źródło: `cta_url` w `blog/app-features.json` wskazuje host bez www. Partia 2 używa już wyłącznie ścieżek względnych.

## Znaleziska produktowe z audytu kodu (przy okazji wpisu o prywatności)
- **Nie ma eksportu danych**, a obiecują go: paywall (`app_en.arb`: `subscription_featureExport` „Data export & sharing", `settings_premiumDescription` „full export access") ORAZ żywa `/privacy-policy` („If you want a copy, export it first; that also works inside the app"). Endpoint raportu PDF na e-mail (`summaries.py:461`) istnieje, ale jest martwy i nieosiągalny z UI. Brak endpointu przenoszalności (RODO art. 20); jest samo usuwanie (art. 17). **Wymaga decyzji: albo funkcja powstaje, albo polityka i paywall się zmieniają.**
- **Brak opt-outu z analityki produktowej.** Typ zgody `ANALYTICS` jest w enumie po obu stronach, ale nie ma dla niego endpointu ani UI (`consent.py` obsługuje tylko `PROFILING` i `ARTICLE9_HEALTH`). Sekcja „Privacy & Data" ma dwa przełączniki i żaden nim nie jest.
- **`/faq` mówi „We don't share it", `/privacy-policy` wymienia procesorów** (Heroku, OpenAI, PostHog, Firebase, Loops, Webflow, Contentsquare, tagi Google/Meta). Do ujednolicenia.
- Działa dobrze: usuwanie konta jest samoobsługowe („Delete Account" na dole ekranu Account) i kasuje u procesorów (Redis, AssemblyAI, Loops, PostHog, Firebase). Kosz „Recently Deleted" trzyma **24 godziny** (nie dni), bez ręcznego opróżniania.

## Uwagi do treści partii 2
- Wpis 09-12 (leki) **świadomie NIE zawiera sekcji o pogorszeniu w pierwszych tygodniach** – decyzja operatora, nie luka. Zero nazw leków, dawek i klas.
- Wpis 09-13 (prywatność) celowo **bez bloku `[FEATURES:]`** i bez twierdzeń o MindSync poza tym, co stoi w polityce.
- Redakcja usunęła **8 linków do `/pre-order/*`** z partii 2: te strony sprzedają funkcje, których nie ma („This feature ships Q4"). Najgorszy przypadek: wpis o lekach mówił „MindSync has no medication module" i linkował do strony sprzedającej moduł lekowy. `blog/app-features.json` nadal sankcjonuje te cele w `site_targets` – do przemyślenia.
- Poprawiony błąd faktograficzny: Kazantzis i wsp. 2016 to **17 badań / N=2312** (nie 23 badania / r=.26 – to inna meta-analiza). Ten sam błąd siedzi w opublikowanym `/journal/what-to-do-between-therapy-sessions`.

Powiązane: [[project-seo-overhaul-mindsync-2026-08-26]], [[project-blog-adaptacja-mindsync-2026-08-25]], [[reference-webflow-seo-gotchas]]
