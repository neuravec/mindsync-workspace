---
name: reference-tab-usage-pageview-passthrough-2026-10-13
description: Bottom-tab usage measurement - tab_switched is the only tab-open signal, it is inflated by PageView pass-through for middle tabs, and character_card_viewed is not an open signal. 2026-10-13 baselines for Character vs other tabs.
metadata:
  type: reference
---

**Tab-open signal** = `tab_switched` with `properties.tab_name` in `main, therapy, reflect, workspace, character` (legacy `stats` dead since 2026-09-22). No `$screen` per tab: tabs live inside `$screen mainPage`.

**Pass-through trap:** `MainNavCubit.selectTab` is also called from `PageView.onPageChanged`, so a bottom-nav tap across several tabs fires `tab_switched` for every intermediate page during the 300 ms animation. 30d: 54-76% of opens of every tab are followed by another switch within 3 s; pairs <1 s dominated by therapy<->reflect. Use "settled opens" (next `tab_switched` in same `$session_id` >= 3 s later or none) via `leadInFrame(...) OVER (PARTITION BY $session_id ORDER BY timestamp ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING)` for fair tab comparison. Main also under-counted (landing not tracked).

**`character_card_viewed` / `bio_viewed` are card loads**, not opens (fire on init, after capture flows, after Settings edits). Character in-tab actions: `orca_color_changed`, `orca_named`, `bio_refreshed`, `content_shared` content_type `Personal Bio`. `orca_memory_*` is a Settings screen; `personal_reveal_*` is the onboarding wow flow.

**Baselines 2026-10-13 (default filters, 30d):** shell users (mainPage or any tab_switched) = 55. Settled users: therapy 43, reflect 40, main 39, workspace 39, character 35 (64%). Character 2+ days = 10. W2 return: week-1 Character openers 16/49 = 33% vs others 7/44 = 16% (correlation). Full extract: `analytics-reports/raw/2026-10-13-character-tab-usage.md`.

`leadInFrame` window functions over 90d of `tab_switched` ran well inside the 10 s server limit; a 4-CTE retention join from 2026-04-22 also passed.
