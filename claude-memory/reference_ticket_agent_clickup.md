---
name: reference-ticket-agent-clickup
description: "Agent ticket-agent + przepis dostępu do ClickUp (scripts/clickup.py, CLICKUP_API w Heroku/.env, ID workspace/list, gotchas API) i styl pisania ticketów dla odbiorcy biznesowego"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f583fa72-a76c-4e53-ac8d-446a00a1189d
  modified: 2026-08-11T14:51:46.564Z
---

Od 2026-08-11 istnieje agent **`ticket-agent`** (`.claude/agents/ticket-agent.md`, opus-5, gold, memory: project) – jedyny agent gadający z ClickUpem, w obie strony: commity → ticket biznesowy, oraz backlog ClickUp → work ordery TASK/AGENT/FILES/DONE_WHEN dla domenowych agentów. Nigdy nie implementuje i nigdy nic nie kasuje w ClickUpie.

**Dostęp:** `scripts/clickup.py` (stdlib, bez zależności), token `CLICKUP_API` w **`Heroku/.env`** (root repo, NIE `MindSync/.env`).
Komendy: `--check`, `--spaces`, `--lists <space>`, `--tasks <list>`, `--task <id>`, `--tree <id> --full`, `--comments <id>`, `--set-desc --file`, `--bulk-desc <plik z sekcjami =====id=====>`, `--create`, `--comment`, `--set-status`, `--set-name`; każda mutacja wspiera `--dry-run`. DELETE celowo nieistniejące.

**Stałe (zweryfikowane 2026-08-11):** workspace `9015587939`; spaces: Features & Knowledge `90151979306`, Tech `90152156487`, WWW & UX & Marketing `90152158165`, Business & Finances `90152158247`; lista robocza **Features `901504408777`** (36 tasków, głównie backlog pomysłów).

**Gotchas API:**
- Opisy WYSYŁAJ jako `markdown_content`. Pole `description` zapisuje escapowane literały (`\## Kontekst`, mangled backticki).
- `GET /team` (lista workspace'ów) zwraca **404 SHARD_006** tym tokenem; wszystko pod `/team/{id}/...` działa – dlatego ID workspace jest zahardkodowane.
- Tablica `subtasks` w parencie ma tylko płytkie pola; opis podtaska wymaga osobnego GET (robi to `--tree`).
- Polskie znaki w konsoli Windows wyglądają na zepsute – to codepage terminala, nie dane. Weryfikuj przez ponowny odczyt API i długość znaków.

**Styl ticketów (wypracowany na tickecie 86cb3vjj9, PostHog Audit Batch):** odbiorca nie zna kodu. W opisie ZERO nazw plików, hashy, nazw klas/eventów/tabel, kodów HTTP i żargonu (endpoint, cubit, enum, migracja, JOIN). Każda zmiana opisana efektem dla użytkownika lub dla pieniędzy, z konkretnymi liczbami (to jest cała wiarygodność). Proza, nie ściana bulletów. Zero em-dashy. Ślad techniczny (hashe, migracje, raporty) idzie w **komentarzu** do ticketa, nie w opisie. Parent = streszczenie (O co chodzi / Co z tego mamy / Status / Co zostaje otwarte), podtaski = jeden obszar każdy. Domyślnie podmieniaj TYLKO opisy – struktura i tytuły są celowe.

Powiązane: [[project_posthog_audit_batch_2026_08_10]], [[feedback_subagent_task_sizing]]
