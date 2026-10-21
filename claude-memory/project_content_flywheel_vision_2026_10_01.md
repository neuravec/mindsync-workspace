---
name: project-content-flywheel-vision-2026-10-01
description: "Wizja operatora: blog, statystyki wyszukiwań, Instagram i rendery nowości z frontendu jako jedna maszyna treści; sesje cloud odroczone, praca lokalnie"
metadata:
  node_type: memory
  type: project
  originSessionId: 8c5a7120-5ec3-4e6b-b84a-1d3fc726fe96
  modified: 2026-10-01T17:17:25.698Z
---

Wizja operatora (2026-10-01): treść MindSync ma działać jak jedna maszyna.
1. Blog jest "good enough" i jest źródłem tematów.
2. Statystyki (kto co ogląda, frazy wyszukiwań z GSC) wyznaczają kolejne wpisy bloga, w pętli bez końca.
3. Moduł Instagrama bierze z bloga najlepsze treści i robi z nich różne formaty.
4. Moduł Instagrama bierze też z frontendu aplikacji rendery nowych funkcji i robi z nich content.

**Why:** operator chce jednego obiegu, w którym dane o odbiorze sterują tematami, a każdy kanał zasila pozostałe. Zależności między blogiem, frontendem i brand voice są za gęste, żeby dziś wydzielać Instagram do osobnego repo.

**How to apply:** nie proponuj wydzielania `social/` do samodzielnego repo ani sesji cloud, dopóki operator do tego nie wróci (odroczone 2026-10-01, przenosiny z `social/TODO.md` §0 wstrzymane). Pracujemy lokalnie w workspace `Heroku/`, gdzie blog, frontend i social widzą się nawzajem. Przy pracy nad social lub blogiem szukaj połączeń między modułami (np. wyniki wpisów z `scripts/gsc/blog-performance.py` jako priorytet recyklingu na IG), zamiast traktować je osobno. Powiązane: [[project-instagram-automation-2026-10-01]], [[project-blog-indexing-baseline-2026-09-15]], [[project-blog-app-attribution-2026-10-01]].
