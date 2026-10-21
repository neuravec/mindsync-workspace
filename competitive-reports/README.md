# Competitive Strategy Reports

Competitive-intelligence + product-strategy reports produced by the
**`competitive-strategist`** agent.

## Convention
- One Markdown file per analysis: `YYYY-MM-DD-<kebab-slug>.md`
  (e.g. `2026-06-28-light-pivot-strategy.md`, `2026-06-28-wysa-youper-teardown.md`).
- Each report follows the template in `.claude/agents/competitive-strategist.md`:
  Executive Summary → Market & Traction Snapshot → Competitor Teardowns →
  Feature/Value Matrix → Positioning Map → JTBD Opportunity Zones → What's NOT
  Working at MindSync → Recommended Light Pivot → Optional Bigger Bets → Risks →
  Evidence Gaps → Appendix (sources).

## Framing
This agent assumes the bottleneck for a mature product with ~0 subscribers is
**positioning / distribution / packaging / activation**, not missing features.
Recommendations are biased toward **light pivots** that reuse existing assets.
Bigger feature bets live in a clearly separated section.

## Relationship to growth-analyst
`competitive-strategist` looks OUTWARD (competitors, market). `growth-analyst`
looks INWARD (our PostHog / Postgres / revenue). The strategist cites or requests
growth-analyst's reports for internal validation — it does not query our data itself.

## How to run
Ask in natural language, e.g. "what are competitors doing that we're not, and how
do we lightly pivot to catch their users?" — the lead delegates to
`competitive-strategist`, which drops the report here.
