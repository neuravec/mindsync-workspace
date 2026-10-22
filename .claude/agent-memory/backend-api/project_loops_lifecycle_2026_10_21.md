---
name: project-loops-lifecycle-2026-10-21
description: Loops lifecycle email backend (feat/loops-lifecycle, m321e4c5a6b7 on ke_a7c3e9f1b2d4); kill switch off by default; decisions that differ from SPEC.md
metadata:
  type: project
---

Built 2026-10-21 on branch `feat/loops-lifecycle` (MindSync repo, not pushed) from `email/lifecycle-2026-10/SPEC.md` plus lead updates sent mid-task. Migration m321e4c5a6b7 (3 tables) sits on ke_a7c3e9f1b2d4.

Decisions not obvious from the code:
- Sign-up trial is granted BEFORE the agreements screen (FE: createUser -> createUserSubscription, profile only after GDPR consent). So `trialStarted` for the sign-up trial is sent from POST /users/profile together with `signupCompleted`, and every lifecycle send is gated on `has_accepted_agreements`.
- `subscriptionCancelled` (auto-renew off) is NOT detectable: receipts are only verified at purchase and after expiry, no ASSN/RTDN. Only `subscriptionExpired` is emitted (hourly deactivation job, paid `granted_via='purchase'` only, cycle = end_date).
- `subscriptionPurchased` "first" = no other VERIFIED non-one-time receipt, or converting an open store trial. Keeps renewals of pre-deploy subscribers out.
- `hasFirstConversation` hooks into `_maybe_emit_user_activated` (won branch) + journal conversation /end; once-marker row in email_lifecycle_log.
- P9 uses an exact 90-day window (a ">= 90 days" rule would mass-mail everyone dormant on day one).
- Added `unsubscribed_at` + `suppressed_reason` to email_contact_state (not in SPEC) for webhook state.
- Webhook program mapping: email.* payloads carry only loopId/campaignId, names only on *.email.sent, so id->program is cached in Redis.

**Why:** operator (Mikolaj) wants all programs live end to end; Loops workflows are built in parallel against the exact event/property names.
**How to apply:** never rename event or property names; Heroku needs `alembic upgrade head` + env vars (LOOPS_LIFECYCLE_ENABLED etc.) after deploy. See [[patterns-backend-detailed]].
