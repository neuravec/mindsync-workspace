---
name: project-ke-team-backfill-sizing-2026-10-19
description: Team accounts A (operator) and B (Darek) are NOT premium (purchases ended 10-16 / 10-09), so KE gave them forward-only plans with cursors at activation; full history = 124 / 266 entries, 9 / 18 jobs, 3 / 5 days at cap 60; lowering a floor cannot reach rows behind the cursors
metadata:
  type: project
---

Snapshot 2026-10-19, v576 (report: db-reports/2026-10-19-ke-team-backfill-sizing.md, run.5656).
- Neither team account was among the 23 people of the premium backfill (all 23 share activated_at 11:53:26 UTC). Each opened the tab itself, got read_plan=2 (forward only), and had its source cursors set to the newest row before activation. backfill_done_at was set at activation, so the sweep ignores them until they write something new.
- Full-history entries: A 124 (87 of them reflect_talk older than 365 days), B 266 (137 older than 365 days). The 90-day window holds 16 for A and 75 for B. Every row sits at or below the cursors.
- The only history path in the code is `hist_*` in history.plan_read: premium only and 90 days only. A full-history read needs new backend-api code (a floor override and a cursor reseed).
- Matching the operator by email: hash it in SQL (sha256 of lower(email) and of the dotless, plus-stripped local part) so the address never appears in the script echo. Apple relay accounts cannot be matched this way.

**Why:** the operator wants a full-history KE backfill for the team accounts. They assumed the accounts were premium.
**How to apply:** check is_user_premium and the read_plan before sizing any KE read for a specific account. Expired TestFlight or sandbox purchases make team accounts non-premium. Related: [[project-ke-backfill-sizing-2026-10-19]]
