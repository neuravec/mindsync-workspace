---
name: project-shared-workspace-2026-10-21
description: "Wspólny workspace dla dwóch osób (repo neuravec/mindsync-workspace): sync.py pull na start (hook), pytanie o commit+push na koniec, pamięć w claude-memory/"
metadata:
  type: project
---

21.10 operator zlecił udostępnienie całego środowiska wspólnikowi (end2end) z regułami: na początku pracy pull wszystkiego, na końcu pytanie o commit i push na wspólne repo.

- Katalog Heroku = repo `neuravec/mindsync-workspace` (git init 21.10, gałąź main, remote origin). Repo kodu i social są osobne, w .gitignore; setup klonuje je obok.
- `scripts/workspace/sync.py`: `pull` (fetch wszystkich repo; workspace i social pull --rebase --autostash; repo kodu tylko fast-forward przy czystym drzewie), `status`, `push -m` (tylko workspace i social, skan sekretów przed commitem, pull --rebase przed push).
- `.claude/settings.json` (wspólne): hook SessionStart `startup|resume` uruchamia `sync.py pull --hook`; hook PostToolUse ui-change-detector przeniesiony z settings.local.json ze ścieżką `$CLAUDE_PROJECT_DIR`; MCP heroku/clickup/loops z `.mcp.json` (HEROKU_API_KEY z env); pluginy firebase, posthog, chrome-devtools.
- Pamięć: `autoMemoryDirectory` w `.claude/settings.local.json` każdej osoby wskazuje `<workspace>/claude-memory`. Stary katalog w profilu operatora został jako kopia (nieusuwany).
- `.mcp.json` z hasłem do Postgresa przeniesiony do `.mcp.local-backup.json` (gitignore); postgres MCP i tak nie łączył się lokalnie.
- `setup/claude-user/`: agenci seo-* i td-*, skille seo*, globalny CLAUDE.md (zakaz myślników) do zainstalowania u partnera przez `scripts/workspace/setup.ps1`. Instrukcja: `ONBOARDING.md`.
- Reguły w CLAUDE.md, sekcja "Wspólny workspace i synchronizacja z partnerem".

- 21.10 wieczorem: repo neuravec/mindsync-workspace utworzone przez operatora i WYPCHNIĘTE (main, 4 commity), social wypchnięty (bff76ce). Audyt security-guardian: 13 blokerów usuniętych (handoffy z danymi prawdziwych kont w .gitignore, redakcja testerów, UID, terapeutki, webhook Slacka i hasła podpisu). OTWARTE dla operatora: zaproszenie wspólnika do 6 repo, rotacja webhooka Slacka i hasła podpisu Androida, backend MindSync śledzi .env, który config.py czyta ze slugu Heroku: usunięcie z gita dopiero po przeniesieniu wartości do config vars (backend-api + integration-devops), inaczej boot się wywróci.

**Why:** dwie osoby z własnym Claude muszą mieć ten sam stan treści, kolejek i pamięci; bez tego drip publikuje podwójnie, a wiedza się rozjeżdża.
**How to apply:** na koniec każdej sesji `sync.py status` i pytanie o push; dripy tylko na maszynie operatora; nowe sekrety tylko do `.env.example` bez wartości. Powiązane: [[reference-backend-autodeploy-on-push]], [[feedback-concurrent-session-git-hygiene]].
