---
name: competitive-strategist-agent
description: "2nd business agent (2026-06-28) — competitive intel + product strategy, light-pivot recommendations, reports to competitive-reports/"
metadata: 
  node_type: memory
  type: project
  originSessionId: bfcb78f7-0aa9-462a-938a-d9ea37385eeb
---

Second agent in the business track (after [[project_business_agents_track_2026_06_28]]):
**`competitive-strategist`** — shipped 2026-06-28.

- File: `.claude/agents/competitive-strategist.md`. Model **Opus** (`claude-opus-4-8`),
  color blue, `memory: project`, `disallowedTools: Edit, NotebookEdit`. Read-only.
- Purpose: study competitors **with a verified real user base**, diagnose what's
  underperforming at MindSync, recommend a **LIGHT pivot** (reposition/repackage/
  re-segment/re-price) that reuses existing assets. Output = Markdown report in
  `competitive-reports/` (seeded with README).
- **Core framing (deliberately hard-coded):** mature product + ~3–4 subscribers ⇒
  bottleneck is positioning / ICP / distribution (CAC) / packaging / activation / trust,
  NOT missing features. Agent is told to resist the "build more" reflex and lead with
  positioning/distribution; big feature bets go in a separate "optional bigger bets" section.
- Sources (user-chosen, all four): **Ahrefs MCP** (traffic/keywords/brand radar = traction
  filter; call `doc` before first use; USD cents ÷100; honor render_with; credit-efficient) +
  **App Store/Play review mining** via Chrome browser MCP (public pages only; 50–100 recent
  reviews/competitor; ≥15% recurrence = signal) + **web/market reports** (WebSearch/WebFetch;
  cite everything) + **internal linkage** (reads repo + analytics-reports/*; does NOT query
  PostHog/DB itself — defers to growth-analyst).
- Default competitor set: AI therapy companions (Wysa/Youper/Woebot), mood/journaling+habit
  (Finch/Daylio/How We Feel/Bloom), AI companions (Replika/Pi). Calm/Headspace = reference only.
- Frameworks: traction-first filter, JTBD 2×2, feature/value matrix (win/lose/toss-up),
  positioning map, monetization & acquisition teardown, retention loops, Blue Ocean ERRC.
- Registered in CLAUDE.md roster. Memory dir `.claude/agent-memory/competitive-strategist/`.

**Why:** complementary to growth-analyst (outward vs inward); user wants to capture an
existing audience via a light pivot. **How to apply:** competitor/market/pivot/positioning
questions → competitive-strategist; internal "why our numbers" → growth-analyst.
Methodology reused both times: web-research the agent design + domain, ground in MindSync,
AskUserQuestion on high-impact decisions, then build + seed folder + register + memory.
Related: [[project_business_agents_track_2026_06_28]], [[reference_posthog_dashboards]].
