---
name: business-agents-track-growth-analyst
description: New track of business-oriented agents started 2026-06-28; first agent growth-analyst (PostHog+Postgres+revenue → reports)
metadata: 
  node_type: memory
  type: project
  originSessionId: bfcb78f7-0aa9-462a-938a-d9ea37385eeb
---

User is starting a track of **business-oriented agents** (counterpart to the existing
engineering-focused team). First one shipped 2026-06-28: **`growth-analyst`**.

- File: `.claude/agents/growth-analyst.md`. Model **Opus** (`claude-opus-4-8`), color cyan,
  `memory: project`, `disallowedTools: Edit, NotebookEdit`.
- Purpose: answer **business "why"** questions (why users churn, how to grow
  purchases/retention/activation), not just technical issues.
- **Read-only** on all data sources; owns no code. Only output = Markdown report in
  `analytics-reports/` (seeded with README; convention `YYYY-MM-DD-<slug>.md`).
- Sources (user-chosen): **PostHog** (EU proj 141170, via posthog MCP plugin + skills;
  `querying-posthog-data` required before HogQL) + **prod Postgres** (read-only SELECT;
  revenue truth = `subscription_receipts`, AI-cost/margin truth = `token_usage_log` ×
  `model_pricing`) + **revenue** (store/RevenueCat). Web for benchmarks.
- Anchored to `POSTHOG_ANALYTICS_PLAN.md` (12 business scenarios, ~89 events) — but agent
  must verify events ACTUALLY flow before relying (plan ≠ live).
- Privacy: aggregates only, no therapy content/PII/raw scores/secrets, suppress segments <25.
- Registered in `CLAUDE.md` roster. Memory dir: `.claude/agent-memory/growth-analyst/`.

**Why:** user wants effective business insight, not dashboards. **How to apply:** for
churn/monetization/retention/activation/growth questions, delegate to growth-analyst.
More business agents (marketing, finance, etc.) likely to follow — reuse this read-only +
report-to-disk pattern. Related: [[reference_posthog_dashboards]], [[reference_posthog_integration]].
