---
name: project-blog-app-attribution-2026-10-01
description: "Pomiar konwersji blog -> instalacja aplikacji; Android install referrer juz istnieje (B9), brakowalo tylko oznaczonych linkow; stan wdrozenia 2026-10-01"
metadata:
  node_type: memory
  type: project
  originSessionId: 5383d233-de2a-4ede-b70e-49d134509c52
  modified: 2026-10-01T08:52:20.421Z
---

Pomiar "czytelnik bloga -> instalacja" (2026-10-01). Stan 01.10: BE PUSHED main 7d467c8 (deploy niezweryfikowany, heroku CLI niezalogowany); FE PUSHED dev 3fe6055 (po rebase na 3d6923f); skrypt Webflow LIVE: registered inline script 'blogattribution' 1.0.1 (footer, add_site_script), opublikowany 01.10 ~09:50, zweryfikowany headless Chrome (linki z referrer/ct/pt). Pole custom code Head ~10k znakow CSS = limit witryny, dlatego operator nie mogl wkleic; nowe skrypty TYLKO jako registered scripts. Apple provider token pt=127496944 wpisany do skryptu (v1.0.1).

- Android: `InstallAttributionService` (FE, od app 2.0.86) czyta Play Install Referrer -> zdarzenie `app_install_attributed` + person props `install_source/medium/campaign` ($set_once). Pusto, bo linki na stronie nie mialy `referrer=utm_...`. Raport posthog-data-extractor z 01.10 ("not flowing") sprawdzal zle pola (`install_referrer`, `utm_source`), NIE `install_source`.
- Skrypt strony: `scripts/webflow/blog-attribution/blog-attribution.min.js` (1949 B, limit inline 2000). Dokleja do linkow Play `referrer=utm_source=blog&utm_medium=badge|inline|card&utm_campaign=<slug>`, do App Store `ct=blog-<slug>` (+`pt` tylko gdy APPLE_PROVIDER_TOKEN ustawiony, obecnie pusty), event `blog_store_click` za zgoda. Wdrozenie: registered script + PUT custom_code (PUT ZASTEPUJE cala liste, snapshot najpierw, inaczej znika msconsent) + publikacja witryny przez operatora. Token dripu NIE ma dostepu do Custom Code API -> MCP Webflow albo nowy token.
- Ankieta onboarding: wartosc `blog`. BE branch `feat/lead-source-blog` 7d467c8 (bez migracji), FE branch `feat/lead-source-blog` 2b5977b+5d9c613. Kolejnosc: BE push przed FE (inaczej 422 polykane, lead_source NULL).
- Naprawione na FE branchu (cc1ccb4, 279a483): zly pakiet Play `app.mindsync.mindsync_app` -> com.mindsync.app ORAZ zly App Store id 1656144298 (to album muzyczny!) -> 6739644256 w review_request_popup.dart i drawer_menu.dart. Prawdziwy id MindSync = 6739644256 (itunes lookup).
- Auto mode blokuje push na main i zapis do Webflow (Production Deploy) -> operator robi sam; skrypt do wklejenia: scripts/webflow/blog-attribution/DO-WKLEJENIA-footer.html (Site settings > Custom code > Footer, na koncu).

**How to apply:** pytanie o konwersje z bloga = HogQL po `install_source='blog'` / `blog_store_click` / `source_value='blog'`, iOS = App Store Connect Campaigns. Status promuj dopiero po dowodzie wdrozenia ([[feedback-memory-write-after-commit]]).
