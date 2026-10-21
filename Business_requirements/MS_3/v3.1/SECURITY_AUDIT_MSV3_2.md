# Security Audit Report — MSV3.2 Workspace Batch — 2026-07-06

Auditor: security-guardian (read-only). Scope: backend commits 5c75d39, 12543e3, f789a4b (~27 new /workspace routes, /dashboard/mood-trend, /goals/{id}/narratives, 8 new tables, 4 background tasks, 2 notification generators, 2 migrations).

## Verdict
**DEPLOY-BLOCKING: NO.** No Critical or High findings — no horizontal privilege escalation, no auth bypass, no SQL injection, no plaintext mental-health content at rest, no clinical content in push payloads (new generators route through the moment_text_generator guardrail prompt; only days_since_last_entry/reminder_kind passed as context).

Pre-ship gates recommended: close MED-002 (deletion-cascade test coverage) per CLAUDE.md mandatory-testing rule; product decision on MED-001.

## Medium Findings

### MED-001: Goal-narrative archive endpoint bypasses the existing premium paywall
- Location: app/api/v1/endpoints/goals.py, list_goal_narratives (~483-511)
- Existing goal-detail gates ai_narrative by is_premium (goals.py:78); the new GET /goals/{goal_id}/narratives returns the full decrypted narrative archive to any authenticated user. Ownership IS correctly checked — monetization inconsistency only. Note: achieved_narrative is also ungated in existing code, so this may be an intentional "earned content stays visible" pattern. NEEDS PRODUCT DECISION, then apply consistently. Owner: backend-api.

### MED-002: GDPR deletion cascade for the 8 new tables has zero automated test coverage
- Mechanism verified correct by inspection: every new table FKs users.id with ondelete="CASCADE" (thread_sources/goal_narratives transitively), User relationships use cascade="all, delete-orphan", passive_deletes=True — matches the post-hero_insights fix pattern. But test_delete_account_cascade.py was NOT extended for the new tables. Given project history, "looks right" without a test is the exact gap that caused the last incident. Remediation: add test asserting zero rows in all 8 tables + goal_narratives after account deletion. Owner: qa-testing.

### MED-003: /dashboard/mood-trend returns raw exception text (detail=str(e))
- Matches a pre-existing pattern used 13× in dashboard.py — newly added instance, not a new class. Low practical severity. Remediation: generic client error + server-side log; recommend a dashboard.py-wide follow-up ticket. Owner: data-analytics.

## Low Findings
- crud/workspace.py:104 — touch_agenda_item looks up linked Thread without Thread.user_id filter. Not currently exploitable (all thread_id write paths pre-validate ownership) — defense-in-depth: add Thread.user_id == item.user_id. Owner: backend-api.
- endpoints/workspace.py:681 — GET /workspace/triage/{card_type}/{card_id} accepts unvalidated card_type (submit-side has a validator). No security impact; inconsistency. Owner: backend-api.
- No rate limiting on new write endpoints — consistent with codebase; backlog (unmetered, unpaywalled, unbounded growth per user).
- Boot/migration note: create_all() on web boot would auto-create the new tables if alembic lags (no native enums — safe/idempotent), but run both migrations (xx4y5z6a7b8c, yy5z6a7b8c9d) as part of the deploy to keep Alembic history authoritative.

## GDPR Compliance
| Requirement | Status |
|---|---|
| Right to erasure | PASS (mechanism) / GAP (test proof — MED-002) |
| Data minimization | PASS (no PII to OpenAI beyond established practice) |
| Encryption at rest | PASS (all new free-text columns encode()d on every write path) |
| Portability / Consent / Retention | Not affected by this batch |

## Horizontal Privilege Escalation — all route families SAFE
Agenda(5), Todo(7), Threads(7), Realizations(2), WeeklyObs(2), MoodTrend(2), Triage GET/submit(2, AI matched_thread_id cross-checked vs caller's threads at tasks/triage_proposals.py:117-122), Overview(1), Goal narratives(1 — ownership OK, paywall = MED-001). Concrete cross-user constructions attempted for every family; all blocked by ownership filters.

## Remediation Priority
1. MED-002 → qa-testing (pre-deployment gate)
2. MED-001 → product decision, then backend-api
3. MED-003 → data-analytics follow-up ticket
4. Lows → backend-api at convenience
