---
name: reference-loops-access-2026-10-21
description: "Jak dać Claude dostęp do Loops (MCP OAuth, CLI, Content API) i czego API nie umie: publikacja kampanii tylko w panelu"
metadata:
  node_type: memory
  type: reference
  originSessionId: db1e99c7-e101-428c-8d00-812c9a1c6024
  modified: 2026-10-21T08:32:27.552Z
---

Stan na 2026-10-21 (research general-web-search-agent, docs loops.so):
- Oficjalny MCP zdalny: `claude mcp add loops https://mcp.loops.so --scope user --transport http`, potem `/mcp` i logowanie OAuth w przeglądarce (robi operator). Narzędzia: search, describe, execute, teams.
- Oficjalne CLI (beta, v0.13.0 z 2026-10-20), Windows: `irm https://raw.githubusercontent.com/loops-so/cli/main/install.ps1 | iex`, auth `loops auth login <nazwa>` albo `LOOPS_API_KEY`. Skille: `npx skills add loops-so/skills --global`.
- Content API (od 2026-06-22): list/get kampanii, email-messages jako LMX, themes, components, create/update szkicu, audience i scheduling, preview, Guardian. Limit 60 req/min. Brak HTML w API (tylko LMX); MJML tylko ręcznie w edytorze i API zwraca 409 dla takich wiadomości.
- Brak endpointu publish/send: docs "Open the campaign in the dashboard to publish and send". Ostatni klik robi operator.
- Transakcyjne do masówki zabronione przez Loops.
- Backend ma `LOOPS_API_KEY` w `MindSync/.env` (sync kontaktów, transakcyjne). Użycie tego klucza przez sesję zablokował klasyfikator auto mode (Credential Exploration) 21.10; rekomendacja: osobny klucz albo MCP OAuth.

**How to apply:** do maili masowych idź przez MCP albo CLI: odczytaj LMX i motyw ostatniej wysłanej kampanii, szkic z tym samym themeId, treść głosem Moniki + humanizer, preview do operatora, publikacja w panelu przez operatora. Powiązane: [[project-blog-voice-monika-2026-09-25]].
