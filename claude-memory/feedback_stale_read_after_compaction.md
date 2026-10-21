---
name: feedback-stale-read-after-compaction
description: "After a context-compaction resume, re-read a file immediately before editing it — prior reads from before compaction are stale even though the tool doesn't know that"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b9676365-4ed7-41a2-8c69-40415833f008
  modified: 2026-08-14T17:40:55.691Z
---

When a conversation resumes after context compaction, files already edited
in the pre-compaction portion of the session are on disk but not reflected
in the model's working memory of "what I already read." The Edit tool's own
"file modified since you last read it" safety check catches some of this
(forces a re-read), but not all of it — several edits in the MSV3.3
CS-11/CS-13 session succeeded on the FIRST try with content that turned out
to already exist verbatim (written in the pre-compaction portion), and
several others hit the safety check and required a fresh Read immediately
before the Edit.

**Why:** mid-task compaction summarizes prior turns; the summary generally
does not preserve "I already fully implemented function X" at the level of
detail needed to avoid redundant work, so the resumed agent can plan to
(re)do work that is already done.

**How to apply:** after a compaction resume, before assuming a file needs a
planned change, `git diff --stat` / `git status` first to see what's already
modified, then `git diff <file>` or a fresh `Grep`/`Read` of the specific
region to check whether the planned change already landed. Don't trust a
mental plan formed before compaction against the current file state — verify
against disk every time, not just when the Edit tool complains. This saved
significant duplicated work mid-task: ~all of `openai_service.py`'s CS-11
prompt/schema changes turned out to already be done pre-compaction, and only
`generate_prep_card_mood_section`'s implementation plus `crud.py`'s
`gather_prep_card_context` extension were genuinely still missing.

See [[project_msv33_cs11_cs13_batch_2026_08_14]] for the task this came
from.
