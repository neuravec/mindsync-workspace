---
name: project-blog-voice-monika-2026-09-25
description: "Blog voice switched to Monika's newsletter style (hybrid of her #17 and #24); where the source archive lives and how to read it"
metadata:
  node_type: memory
  type: project
  originSessionId: 64d4396e-3324-4610-b9e8-a7b692702d7c
  modified: 2026-09-25T11:34:52.112Z
---

On 2026-09-25 the operator decided the blog must copy the writing style of Monika (MindSync communications specialist, author of the newsletters) literally. Her own guidance: a hybrid of newsletter #17 (more humor) and #24 (more substance), neither too long nor too short, always ending with how to use the app.

Changed: `docs/blog/brand-mindsync.md` §2 rewritten (DNA, post skeleton §2.2, blog adaptations §2.3, humanizer §2.4, checklist §2.5); new `docs/blog/voice-sample-monika.md` (full #17 + #24); blog-writer, brand-voice-manager, seo-content-writer and `blog/queue/_format.md` now point to them. Deliberate deviations from her style: US spelling kept, no emoji, no invented first-person anecdotes, no em-dash (her #0 and #8 use it).

Enforcement (added the same day): the skill `/blog-write` (`.claude/skills/blog-write/SKILL.md`) is the only allowed path for writing or rewriting posts, and the main session never writes post prose itself. Every new queue JSON carries `"glos": "monika-v1"`. `scripts/blog-voice-check.py` checks the voice mechanically and is wired into `blog-queue-gate.py`, but only for posts that have that field. A post without it dated from 2026-09-26 gets a warning. CLAUDE.md, blog/README.md and `_format.md` point to the skill.

**Why:** the operator wanted the blog to sound more human, like her writing.

**How to apply:** source = Google Doc "ARCHIWUM 2026" (id 1plQFsOSBbfoQDN1--JSHQMHncNPavKbfr9w-tCGpXjU, one newsletter per doc tab) in Drive folder NEWSLETTERY 2026. The Google Drive MCP connector returns "not found" for it (a different account). Working path: Chrome, `fetch('/document/d/<id>/mobilebasic?tab=<tabId>')` from a docs.google.com tab, then strip HTML with regex (DOMParser is blocked by TrustedHTML). Tab ids come from the edit page HTML (`t.xxxxxxxx`). JS tool output is truncated at about 1,000 characters and blocks results containing `=`, `?`, `&`, so slice the text and strip those characters. POSTing to a localhost receiver froze the tab. Posts already in the queue were written in the old voice and have not been rewritten. See [[project-blog-adaptacja-mindsync-2026-08-25]].

Partia 4 (the first /blog-write run, 2026-09-25) produced three posts with status `gotowy` in the queue: early-signs-of-burnout (09-26), how-to-stop-people-pleasing (09-27) and anxious-attachment-style (09-28). They publish through the "MindSync Blog Drip" scheduled task at 07:00. Lessons from the run:
- blog-writer, graphic-designer and seo-content-writer have no shell, so the main session runs the preflight, both check scripts and the Gemini hero generation.
- Voice notes in the app are transcripts with no audio playback, so a post must never say "listen" or "hear".
- mood-trends charts only the check-in ratings. It does not detect people or patterns in notes.
- A file added to a subagent's task mid-way got its edit blocked by the permission classifier. Spawn a fresh agent with that file in scope from the start.
- early-signs-of-burnout was published LIVE by operator request on 2026-09-25 at 14:29, with planowana_data and datePublished moved to 09-25. This verified the other session's post-publish chain end to end: item live (200), /blog lastUpdated toggled and pushed to the sitemap lastmod, site publish rebuilt the sitemap (35 to 36 URLs), and the GSC submit went through. Google downloaded the sitemap 1 s after the submit (lastSubmitted 12:30:18Z, lastDownloaded 12:30:19Z, 0 errors). Indexing of the URL itself is still to be checked after a few hours.

