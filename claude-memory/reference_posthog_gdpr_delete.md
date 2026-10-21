---
name: PostHog GDPR person delete endpoint
description: Use POST /persons/bulk_delete/ — the legacy DELETE /persons/?distinct_id= returns 403 with personal API keys
type: reference
originSessionId: 4ba60075-8a3b-4f21-945a-b81a50d5c9a4
---
PostHog person deletion (GDPR right-to-erasure) only works via the bulk_delete endpoint with personal API keys. Verified empirically against PostHog Cloud EU (eu.i.posthog.com) on 2026-05-04.

## Working endpoint
```
POST /api/projects/{project_id}/persons/bulk_delete/
Authorization: Bearer phx_<personal_api_key>
Content-Type: application/json
{
  "distinct_ids": ["<firebase_uid>"],
  "delete_events": true,
  "delete_recordings": true
}
→ 202 Accepted
{
  "persons_found": N, "persons_deleted": N,
  "events_queued_for_deletion": bool,
  "recordings_queued_for_deletion": bool,
  "deletion_errors": []
}
```

## Broken endpoint (don't use)
```
DELETE /api/projects/{project_id}/persons/?distinct_id=<id>
→ 403 {"detail":"This action does not support personal API key access"}
```

## Why it matters
- `delete_events=true` purges historical event stream — without it, person profile is gone but events linger keyed by distinct_id (insights still pickup old data, GDPR-incomplete)
- `delete_recordings=true` purges session replays — same reasoning
- 202 means "queued for async deletion in PostHog backend" — not synchronous
- Implementation: `MindSync/app/services/posthog_service.py:delete_person`. Called from RQ worker (not request thread) via `rq_queue.enqueue(posthog_delete_person, distinct_id)` in `users.py:delete_own_account`.

## RQ worker context note
`delete_person` does NOT depend on the PostHog SDK `_client` (it uses raw `requests.post` directly). This makes it safe to call from RQ workers, which don't run the FastAPI lifespan that initialises the SDK. Guard is `settings.POSTHOG_ENABLED + POSTHOG_PERSONAL_API_KEY + POSTHOG_PROJECT_ID`.

## Order of operations for account_deleted
1. Gather pre-deletion telemetry (subscription_tier with "is currently entitled" semantic, total_debriefs filtered for `deleted_at IS NULL`)
2. Emit `account_deleted` event via `_capture_payment_event` BEFORE db.delete (distinct_id still derivable)
3. db.delete(user) + db.commit() — DB erasure is the legal contract
4. `rq_queue.enqueue(posthog_delete_person, distinct_id)` — best-effort PostHog cleanup, fire-and-forget; if Redis is down it logs WARNING and proceeds (manual PostHog cleanup signal)
5. Return 204 No Content
