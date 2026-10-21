---
name: reflect-summary-backfill-2026-10-19
description: Why old Reflect threads lack conversation_summaries, the one-off backfill script (not yet run on prod), and the "date backfilled rows at the talk, not today" rule
metadata:
  type: project
---

Reflect threads are summarized only on POST /reflect/{id}/end and, since BE-B2 (2026-10-03), by
the idle job `app/tasks/reflect_idle_analysis.py` with a 7-day lookback. The nightly auto-close
(`app/services/close_all_notes.py`) skips REFLECT since 2026-03-01. So threads left without "End"
before ~2026-09-26 never got a summary (prod 2026-10-19: 53 in 90 days, Jul 6/6, Aug 27/29,
Sep 20/32, Oct 0/58). No code fix needed going forward.

Script `MindSync/scripts/backfill_reflect_summaries.py`, branch `fix/reflect-summary-backfill`
(commits fbb3e5b, 64c1aa8, worktree `MindSync-wt-reflect-summaries`), NOT run on prod as of
2026-10-19; operator runs it before the KE history backfill.

**Why:** KE reads Reflect talks only from conversation_summaries.

**How to apply (rule for any future summary/analysis backfill):** never write backfilled
analysis rows with created_at = now. `ConversationSummary.created_at` feeds "recent" windows
(prep card 30d, Orca recent conversations, weekly/monthly crud windows), `ConversationAction.created_at`
orders the dashboard CTA, `ConversationTopic.created_at` feeds topic windows. Date them at the
last user turn: that also keeps the Reflect watermark (`reflect_analysis_is_current`) true. KE's
cursor is `ConversationSummary.id` (monotonic) but its floor filters on created_at >= now-90d.
Skip streak/memory/PostHog/first-week side effects of `_analyze_reflect_thread` in backfills.

Test gotchas: `TokenUsageLog` BigInteger PK needs explicit `id` on SQLite; RAG upsert silently
fails on SQLite (ARRAY embedding); REPL-safety of a `heroku run python < file` script can be
checked locally with `py -3.12 -i < file`. See [[c1-dead-instrumentation-backend-2026-08-10]].
