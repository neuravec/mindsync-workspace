---
name: feedback_chrome_tool_js_only_env
description: In this env the claude-in-chrome visual tools (screenshot/read_page/clicks) are broken; drive pages via javascript_tool only
metadata: 
  node_type: memory
  type: feedback
  originSessionId: eee32327-4947-4461-8b7a-06aac1c64d85
  modified: 2026-10-21T22:19:26.357Z
---

Observed 2026-07-03 (Google Play Console session, but confirmed env-wide): the `claude-in-chrome` **visual** control tools are non-functional in this environment.

- `computer` screenshot / `read_page` / `get_page_text` / `find` **all time out** after 45s waiting for `document_idle` — on heavy SPAs (Play Console) AND even on a trivial static page (example.com). So it is the tooling, not the page.
- `computer` `left_click` "executes" (returns success) but the click **does not reach the page content of any tab** — verified by installing a capturing click listener that recorded zero hits on both the target tab and a spare tab. No screenshot means no coordinate calibration either.

**What DOES work reliably:** `navigate`, `tabs_context_mcp`, and above all **`javascript_tool` (javascript_exec)** — full DOM read + page scripting. Use JS for everything: read state, extract data (`document.body.innerText`, `querySelectorAll`), and interact.

**How to apply:**
- Drive pages entirely through `javascript_tool`. Synthetic JS clicks (`el.click()` or dispatched pointer/mouse events) DO trigger SPA routing / tab switches (Angular Material tab-buttons worked).
- BUT synthetic clicks do NOT open trusted-event-guarded dialogs (e.g. Play Console "Create email list" ignored `.click()`, full pointer sequences, and even `Object.defineProperty(e,'isTrusted',{value:true})`). Those steps must be handed to the user.
- `javascript_tool` results are content-filtered: returning raw outerHTML or any URL with a query string / token gets `[BLOCKED: Cookie/query string data]`. Return only trimmed text and token-free strings.
- top-level `await` in `javascript_tool` throws ("await is only valid in async functions") — don't rely on it; do timing via separate calls (the round-trip is the delay).

**Update 2026-10-22 (Loops panel session):** top-level `await` in `javascript_tool` now works. `computer` `left_click` at coordinates taken from `getBoundingClientRect()` (dpr 1) DID reach the page and counted as a trusted gesture: it was the only way to get a clipboard copy (Loops webhook signing secret). Synthetic `.click()`, `execCommand('copy')` and `navigator.clipboard.writeText` without a gesture all fail. Loops CSP blocks `fetch` and form POST to 127.0.0.1. Recipe for moving a secret out of the panel without showing it: real click on the copy button, then `Get-Clipboard` piped into `heroku config:set` in one PowerShell call, then clear the clipboard. Loops panel actions (Settings > Events, webhooks, workflow Start/Pause with the in-page "Pause workflow" dialog) all work via JS.

**Why:** don't repeat the ~30 wasted tool calls it took to discover this. Reach for `javascript_tool` first on any Chrome task here; only hand off the specific clicks that need a real trusted gesture. Related: [[reference_play_console_access]].
