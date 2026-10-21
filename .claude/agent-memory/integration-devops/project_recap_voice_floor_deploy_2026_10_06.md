---
name: project-recap-voice-floor-deploy-2026-10-06
description: Recap voice floor + voice turn capture deployed 2026-10-06 as Heroku v563 (main 76d5c09, no migration) and FE dev f4afaa6 (2.0.105); user_turns analytics meaning changed; device QA open
metadata:
  type: project
---

Deployed 2026-10-06 on operator approval: backend `99a2933..76d5c09` (bd47da6, a1f3560, 76d5c09) = Heroku **v563**, code only, no migration; frontend `156dbc8..f4afaa6` (71991bb, f4afaa6) on `dev`, Codemagic target 2.0.105 (bump not yet visible 27 min after push). Record + rollback + device QA: `design-specs/2026-10-06-recap-voice-floor/DEPLOY.md`.

**Why:** first voice conversations with short spoken answers were judged "short" by text-era thresholds (40 words), so testers got no recap and no memory notes; End could drop the last answer.

**How to apply:**
- Rollback target is v562; recap cache key is now `reflect:recap:v2:*` (24 h TTL), old code reads v1.
- `first_conversation_ended.user_turns` counts only voice replies of 3+ words from 2.0.105 on (`user_fragments` holds the rest); a step down in that metric is a definition change, not a drop. growth-analyst must be told before reading that funnel.
- Recap status (`ready`/`short`/`failed`) is NOT logged at info level; `[OrcaMemory] Recap` and `[FirstConversation]` lines are warnings/errors only, so absence in logs is healthy, not "no traffic proof".
- Prod Config Vars `FIRST_CONVERSATION_RECAP_PROMPT` and `FIRST_CONVERSATION_RECAP_ONLY_PROMPT` are unset; if anyone sets them, the code default prompt (with the new recap rule) is overridden.

Recipe: [[reference-heroku-oneoff-smoke]]. Earlier batch: [[project-first-voice-conversation-fe-deploy-2026-10-05]].
