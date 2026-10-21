---
name: project-posthog-person-props-consent-2026-10-19
description: Backend PostHog person-property paths gated on accepted agreements (gdpr_consent_at); weekly premium_intent job flushes and sends consented users only; which paths are still ungated and why
metadata:
  type: project
---

Commit `b6074de` on branch `fix/posthog-person-props-consent` (worktree `MindSync-wt-ph-consent`), based on 75d1f0d (the identify set/set_once fix). NOT pushed as of 2026-10-19.

**Why it mattered:** before 75d1f0d every backend `identify()` raised TypeError (posthog-python 3.x has no `set_once` kwarg on identify), so NO backend person property had reached PostHog since 2026-04-25. The first live run of `refresh_premium_intent_scores_weekly` after the fix is Sunday 2026-10-25 03:00 UTC. Without this gate it would have created a PostHog person (raw Firebase UID) for every row in `users`, consent or not.

**What changed:**
- `posthog_service.user_ids_with_accepted_agreements(db)` is the batch form of `has_accepted_agreements`. Same rule (non-null `UserTherapyContext.gdpr_consent_at`, user_id unique), joined to `users` to drop orphans. Unlike the per-user check it RAISES on a DB error, so a batch cannot read "nobody consented" as truth.
- Weekly job: consented users only, `flush_posthog(timeout_seconds=30)` in finally, failed score = counted `failed` and NOT sent (it used to send 0), rollback after a failed user, returns `{"sent","skipped_no_consent","failed"}`.
- `_identify_profile_demographics(db, ...)` in users.py and `refresh_behavioral_properties` are both gated on consent.
- Warnings in plan_person_properties / has_accepted_agreements / refresh_behavioral_properties / calculate_premium_intent_score log the exception type only.

**Still ungated (left for operator decision, reported to lead):**
- POST /users/ (create_user) identify runs on every cold start, BEFORE consent for new users. Its `set_once` (signup_date, auth_provider) only fires on the new-user branch, so a naive consent gate would lose those forever for new users. It needs a redesign, not a one-line gate.
- Event-attached `$set`/`$set_once` (capture_with_user, capture_qualifying, payment events with plan props, trial_started). These are user-initiated in-app actions. Only the hourly trial_ended uses `require_consent=True`.

**How to apply:** for any new backend path that sets person properties, gate on `has_accepted_agreements` (or the batch helper in jobs). Any RQ job that captures must call `flush_posthog()` in a finally. Log `type(exc).__name__` only, since SQLAlchemy error text and tracebacks carry the bound uid. See [[test-env-posthog-not-installed]] for the local probe failures.
