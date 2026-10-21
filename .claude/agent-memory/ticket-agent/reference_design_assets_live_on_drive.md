---
name: reference-design-assets-live-on-drive
description: Dawid's design deliverables (orca, lottie, colors, handoffs) usually sit in Google Drive folders linked from ClickUp, not as ClickUp attachments; how to find them and the comment-bookmark gotcha
metadata:
  type: reference
---

When the operator says "Dawid wrzucił pliki na ClickUp", the files are often NOT ClickUp attachments. Since mid-2026 Dawid posts a Google Drive folder link in a ClickUp comment and/or in the ticket description ("Folder with all docs: ..."). Verified 2026-10-05: the new Orca animation for the Character screen (lottie + colors) lives in the Drive folder "Orca Character" `1H48ivPCBoE5eFE_Aty6G_W_xRj0MPlPh` (owner = Dawid's Google account, created 2026-10-03), linked from ticket 86c9b63kv "Update MSV3.5 - Grafiki i animacje"; the ticket itself has zero attachments.

**Gotchas:**
- `--comments` in the runner prints only `comment_text`, which DROPS links stored as `"type": "bookmark"` / `"link_mention"` parts. To see the Drive URL, read the raw `comment` parts array from `GET /task/{id}/comment`.
- Two ClickUp users named Dawid: "Dawid" (id 6649304, the current designer) and "Dawid Woźniak" (id 82759802, old 2024 account). Filter by id, not by first name.
- Older ClickUp-native orca file: `orca_1a.png` uploaded by Monia 2026-02-06 on 86c7p4mn5 (social graphics), not the app mascot.
- Drive access from an agent session: `get_file_metadata` on the folder works, but `search_files` was blocked by the auto-mode classifier (PII handling) on 2026-10-05. Do not work around it; tell the operator and let them download or grant the permission.

How to apply: for any "find Dawid's files" request, scan task attachments AND raw comment parts AND description links, then report the Drive folder if that is where the assets are. Related: [[reference-ticket-agent-clickup]]
