---
name: project-prep-card-backfill-2026-10-13
description: Operator-approved RQ enqueue backfill of first-conversation prep cards (4 cards made); _existing_card makes it effectively one card per user; RQ enqueue from --no-tty dyno works
metadata:
  type: project
---

2026-10-13: backfilled "Before therapy" first-conversation prep cards by enqueueing `generate_first_conversation_prep_card(cid, uid)` on `default` from a `--no-tty` dyno (`from app.core.rq_queue import rq_queue`). 23 FINISHED first-conversation threads, 7 candidates (4 people), 4 enqueued, 4 COMPLETED (cards 3500-3503). Report: db-reports/2026-10-13-prep-card-backfill.md.

**Why:** job did not exist before v567, then failed on enum drift until m317. Art. 9 gate (user_is_in_therapy) blocks most iOS threads (iOS-B 225a543d still refused).

**How to apply:**
- `_existing_card` treats any AUTO card created after the thread's last turn as "this thread's card", so a backfill card blocks all older threads of the same user: enqueue only the newest gate-passing thread per user.
- Recap cache lives 24h, so old threads get only the keyword crisis scan (no model verdict). Flag it.
- Thread 28711 holds a claim with no card (leak); never delete claims without approval.
- RQ worker logs print job args incl. Firebase UID; strip when grepping logs.
- Each operator-approved enqueue must still re-check card/claim/gate right before enqueue; verify via Job.fetch + session_prep_cards. See [[feedback-heroku-run-local-stdout-buffering]].
