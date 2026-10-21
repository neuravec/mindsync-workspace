---
name: project-blog-partia6-2026-10-07
description: "Blog partia 6 (5 wpisów 10-08..10-12, klastry koszty/zmiana terapeuty/prywatność AI) + analiza ruchu 07.10: 10/31 wpisów poza indeksem, 0 instalacji z bloga"
metadata:
  node_type: memory
  type: project
  originSessionId: 5be2142f-a616-4005-9cde-025774a4449e
  modified: 2026-10-07T08:55:44.510Z
---

Partia 6 (2026-10-07): how-to-afford-therapy (10-08), is-it-safe-to-talk-to-ai-about-mental-health (10-09), how-to-switch-therapists (10-10), starting-over-with-a-new-therapist (10-11), does-insurance-cover-therapy (10-12). Wszystkie: voice-check + queue-gate 0 blokerów, akcept brand-voice po poprawkach, hero + schema gotowe, status `gotowy` 2026-10-07 na wyrazne polecenie operatora. Briefy: blog/queue/_batch-partia6-briefs.md; preflight _preflight-partia6.json (7 OK).

Analiza ruchu 07.10 (GSC do 04.10): blog 1738 wyśw./17 klik., W38-W40 = 365/670/466. URL Inspection API: 10 z 31 wpisów nie w indeksie (6 "Discovered not indexed", 4 "unknown"), technicznie OK (200, sitemap, brak noindex); operator zgłasza ręcznie w GSC. PostHog: install_source=blog = 0, blog_store_click nigdy nie zarejestrowane (do ręcznego testu), web PostHog tylko po zgodzie na cookies.

Decyzje lidera: BetterHelp tylko neutralnie w FAQ na dosłowne zapytanie GSC, bez linku. W 02 nie twierdzimy, czy MindSync ma umowę ZDR z OpenAI (nieustalone); dopisane, że MindSync też nie daje tajemnicy terapeutycznej. Polityka prywatności obiecuje eksport w apce, którego nie ma (do operatora/prawnika).

Gotcha: graphic-designer i blog-writer nie mają terminala; hero generuje sesja główna (`gemini-generate.ps1 -Slug hero -Model gemini-3-pro-image -DryRun:$false`), schema można generować scratchpadowym gen_schema.py (wzór w raporcie seo-tech-lead). Pliki opublikowanych wpisów mają BOM (czytaj utf-8-sig).

Related: [[project_blog_partia5_2026_09_28]], [[project_blog_indexing_baseline_2026_09_15]], [[project_blog_app_attribution_2026_10_01]]
