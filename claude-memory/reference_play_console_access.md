---
name: reference_play_console_access
description: Google Play Console access + IDs + Android internal-testing setup for MindSync
metadata: 
  node_type: memory
  type: reference
  originSessionId: eee32327-4947-4461-8b7a-06aac1c64d85
---

Google Play Console for MindSync (reached via `claude-in-chrome`; user is logged in — landing `play.google.com/console` auto-redirects to the account).

- **Developer ID:** `6044487601472644414` (org account "MindSync")
- **App ID:** `4972536380957706052` — "MindSync - Smarter Therapy", pkg `com.mindsync.app`
- **Internal testing track URL:** `.../developers/6044487601472644414/app/4972536380957706052/tracks/internal-testing` (tabs: `?tab=releases` / `?tab=testers`)
- **Internal-test opt-in link (install on phone):** `https://play.google.com/apps/internaltest/4701648304508326424`
- **Tester lists (2026-07-03):** Closed_Beta_01 (37), internal test play (7), **MindSync Internal (1 — the user, selected+saved for the track)**, subscriptions test (4)

**Android beta = Play Internal testing** (the TestFlight analog). Codemagic (`mindsync-frontend/codemagic.yaml`, workflow `app-release`) builds the AAB and publishes to `track: internal`. On 2026-07-03 flipped `submit_as_draft: true → false` (commit `c26353c` on `origin/dev`) so each release **auto-rolls-out** to internal testers instead of sitting as a draft. Before that flip the internal track was STALE — active release stuck at version code 55 (draft 132) while prod was ~530 — because drafts were never rolled out. There is NO Android-only release path: `app-release` builds iOS+Android together, so cutting an Android internal build = a full TestFlight+Play release (push to `dev` triggers it).

To reach/inspect Play Console, drive it via `javascript_tool` only — see [[feedback_chrome_tool_js_only_env]] (visual chrome tools are broken here; the "Create email list" dialog needs a real user click and can't be automated).
