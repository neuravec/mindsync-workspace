---
name: project-seo-overhaul-mindsync-2026-08-26
description: Audyt i naprawa SEO mindsync.app z 2026-08-26 - co wdrożone na żywo i co zostało do zrobienia po stronie operatora
metadata: 
  node_type: memory
  type: project
  originSessionId: 732ad635-483b-496b-b9ae-dc93edf40966
  modified: 2026-08-26T20:47:42.394Z
---

2026-08-26: pełny audyt SEO mindsync.app + naprawa end-to-end, **WDROŻONE I OPUBLIKOWANE** (4 publikacje site-wide), zweryfikowane na produkcyjnym HTML-u. Raport: `seo-reports/2026-08-26-audyt-i-naprawa-mindsync-app.md`.

**Stan końcowy: 22/22 URL-e w sitemapie bez odchyleń** (title, description, dokładnie 1×H1, og:image, canonical, poprawny JSON-LD, ≥300 słów).

Najważniejsze naprawione: (a) **cały JSON-LD na stronie był nieważny** – escapowany do `&quot;`, zero działających danych strukturalnych; (b) skrypt `schema_markup` na stronie głównej zawierał **sfabrykowaną ocenę 4.8/150** i był HTML-em podanym jako JS (nie wykonywał się) – odpięty; (c) dwa opublikowane wpisy blogowe renderowały **pusty `<title>`**; (d) 13 osieroconych stron roboczych siedziało w sitemapie pod `Disallow` – odpublikowane; (e) `/features` i `/audience` były placeholderami („Not ready for deep dive yet.", 108 słów) mimo że blog kieruje na `/features` – napisana pełna treść z `blog/app-features.json`, tylko funkcje `live`; (f) widoczny niestylowany H1 72 px powtarzający tytuł na każdym wpisie – usunięty z szablonu.

**Druga tura tego samego dnia domknęła WSZYSTKIE punkty operatorskie** (przez panel Webflow w przeglądarce + `data_element_settings_tool`): robots.txt wpisany (bez linii Sitemap, bo Webflow dopisuje ją sam – to była przyczyna duplikatu), llms.txt poprawiony i wgrany (4 błędy: urwane zdanie, nieaktualny `support@`, „Web" jako platforma, rozjechany cennik), `lang="pl"` na `/freebie` i `/testerzy` przez custom code, nawigacja: odkryte 2 przygotowane wcześniej ukryte linki (jeden celował w odpublikowaną stronę – przepięty).

⚠ **Korekta wcześniejszego błędu:** zgłosiłem „rozbieżność marketing vs produkt" przy udostępnianiu terapeucie. To był fałszywy alarm – oparty na notatce z `app-features.json` zamiast na żywej treści. Strona obiecuje wyłącznie RĘCZNE dzielenie podsumowań (działa), a portal klinicysty jest na `/about` wprost pod „Our Roadmap → Next". Żadna zmiana copy nie była potrzebna. Zakaz z katalogu dotyczy treści BLOGA, nie strony.

`/admin/licenses` celowo zostaje odpublikowane: to boilerplate szablonu Webflow (mówi „this template", wymienia font Switzer, którego strona nie używa). Przywrócenie = publikacja nieprawdziwej informacji licencyjnej.

**Trzecia i czwarta tura:** alt-teksty (znaleziony realny błąd: 28 odznak sklepów miało zamienione opisy Apple/Google; puste alt spadły z 69% do 30%), listing bloga 361→614 słów, oraz **wydajność**: 10 z 11 skryptów blokujących render w `<head>` okazało się opakowanym CSS-em bez logiki – przeniesione do custom code (site head + zakresowo `/blog` i szablon wpisu). Strona główna: 14→4 skryptów w head, 13→3 blokujących, 11→1 plik z CDN. Kontrola regresji na wyliczonych stylach: wszystkie wartości identyczne. Strony `/pre-order/*` dostały `noindex, follow` (decyzja operatora: zostawić jako landingi walidacyjne, wyjąć z organiku).

⚠ **Punkt „zlinkować osierocone /pre-order" celowo NIEwykonany:** wszystkie sześć stron mówi „You're early, this feature is coming soon / ships Q4", w tym te opisujące funkcje `live`. Link z `/features` tworzyłby sprzeczność. Zamiast tego noindex.

**Nadal otwarte (nie do zrobienia z tego miejsca):** Ahrefs zwraca „Insufficient plan" (brak warstwy fraz/linków); GSC na innym koncie Google; ukryta stara kopia regulaminu w DOM stron prawnych (mechanizm `mslegalinject` jej używa do znalezienia miejsca wstrzyknięcia, więc nie da się jej po prostu usunąć).

Do ponownej weryfikacji: `seo-reports/seo-review.py` – jeden przebieg sprawdza sitemapę, robots, llms, przekierowania, 404, i per URL: title/desc/H1/canonical/OG/JSON-LD/słowa/lang/linki. Ostatni wynik: 0 odchyleń.

Powiązane: [[reference-webflow-seo-gotchas]], [[project-blog-adaptacja-mindsync-2026-08-25]]
