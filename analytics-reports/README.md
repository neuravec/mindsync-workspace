# Analytics Reports

Business-insight reports produced by the **`growth-analyst`** agent.

## Convention
- One Markdown file per analysis: `YYYY-MM-DD-<kebab-slug>.md`
  (e.g. `2026-06-28-week1-churn-deep-dive.md`, `2026-06-28-monetization.md`).
- Each report follows the template in `.claude/agents/growth-analyst.md`:
  Executive Summary → Key Metrics → Findings (by business impact) → Root-Cause &
  Hypotheses → Recommendations (with owner + expected effect) → Segments → Data
  Caveats → Appendix (queries).

## Safe to commit
Reports contain **aggregates only** — no PII, no therapy content, no raw health
scores, no secrets. Segments under 25 users are suppressed. If you ever see
identifying data in a report, treat it as a privacy incident and remove it.

## How to run
Ask in natural language, e.g. "why are users churning after week 1?" or
"how do we increase premium purchases?" — the lead delegates to `growth-analyst`,
which pulls from PostHog + Postgres + revenue and drops the report here.
