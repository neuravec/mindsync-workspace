---
name: reference-clickup-members-and-lists
description: ClickUp member IDs for the team (Mikołaj, Darek, Dawid's two accounts) and where real work tickets live (Tech Tasks list, not Features)
metadata:
  type: reference
---

Member IDs (from `GET /list/901504408777/member`, verified 2026-10-14):
- Mikołaj Jesion 4550077 (mikolaj.jesion@gmail.com), also has a second account 82759800 (mikolaj@mindsync.app) that nobody assigns.
- Darek (Dariusz Wiśniewski) 68635855.
- Dawid has TWO accounts: 6649304 "Dawid" (liswbutach@gmail.com) is the one assigned on every MSV and design ticket; 82759802 "Dawid Woźniak" (dawid@mindsync.app) appears on none. Use 6649304 and say so.
- Monia 106500017.

The runner has no assignee or member support; a scratchpad helper that imports `clickup.call()` works (POST /list/{id}/task with `assignees` + `markdown_content`).

Where tickets live: Features `901504408777` is mostly an idea backlog. The real release tickets ("Update MSV3.x ...") live in the **Tech Tasks** list; social/IG items in WWW and Marketing lists. Search workspace-wide with `GET /team/9015587939/task?include_closed=true&subtasks=true` before concluding a ticket does not exist.
- Redesign 10-2026: cards + Workspace = 86caymgxd (MSV3.8 Global UI changes), Character = 86caymagh (MSV3.7 Character Card).

Related: [[reference_design_assets_live_on_drive]]
