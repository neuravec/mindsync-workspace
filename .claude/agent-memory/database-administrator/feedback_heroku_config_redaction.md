---
name: feedback-heroku-config-redaction
description: "heroku config output uses 'KEY:   value' (colon), not KEY=value — an = -based sed redaction silently fails and leaks secrets to transcript"
metadata:
  type: feedback
---

Never pipe `heroku config -a mindsync` output through a `sed 's/=.*/.../ '` redaction — `heroku config` prints `KEY:            value` (colon + padding), not `KEY=value`. An `=`-anchored sed pattern matches nothing, so the full secret value (DB_URL, REDISGREEN_URL, API keys, etc.) passes through unredacted into tool output/transcript.

**Why this matters:** the project's absolute rule (CLAUDE.md + system prompt) is "never echo or write .env values — reference variable names only." A silently-failing redaction is worse than no redaction attempt, because it looks safe (a sed command ran) while actually leaking. This happened once (2026-07-03, notification audit task): grepped for `DB_URL|REDISGREEN_URL` to show which vars exist, added a `sed 's/=.*/<redacted>/'` "for safety," and both full connection strings (including passwords) were printed in full because of the colon-vs-equals mismatch.

**How to apply:** if a task genuinely needs to confirm a config key *exists* (not needed to display), use `heroku config:get KEY_NAME -a mindsync | wc -c` (proves non-empty without printing) or grep only the key names via `heroku config -a mindsync | cut -d: -f1`, never the value column. If a value must be redacted for display, match on `:` (`sed -E 's/(:\s*).*/\1<redacted>/'`), and test the redaction on a throwaway pattern before running it against anything containing real secrets. Default posture: don't fetch/print full `heroku config` output at all when only key existence is needed.
