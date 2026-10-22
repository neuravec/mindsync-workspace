# Security Audit Report: Loops lifecycle programs (branch feat/loops-lifecycle): 2026-10-21

Scope: `git diff main...feat/loops-lifecycle` in `MindSync/` (commits 9627dc1, 7f0ac28 on top of 23a83bd), against `email/lifecycle-2026-10/SPEC.md`. Read-only review with `git show`/`git diff`. Nothing was checked out and no test was run.

Files reviewed: `app/api/v1/endpoints/email_lifecycle.py`, `app/services/email_lifecycle.py`, `app/services/loops_client.py`, `app/tasks/email_lifecycle.py`, `app/tasks/loops_sync.py` (diff), `app/models/email_lifecycle.py`, `alembic/versions/m321e4c5a6b7_add_email_lifecycle_tables.py`, `app/core/config.py`, `app/core/rq_scheduler_setup.py`, `app/main.py`, `app/api/v1/api.py`, and the hooks added to `users.py`, `conversations.py`, `posthog_service.py` and `subscription_service.py`. I also read the account deletion flow in `users.py`, plus `deps.get_db`, the `has_accepted_agreements` helper and the Procfile.

## Verdict

**BLOCKED for go-live as the SPEC describes it** (kill switch on and the Loops webhook registered), because of one High finding (H-1). The fix takes a few lines.

The code itself can be merged and deployed with no risk **as long as `LOOPS_WEBHOOK_SECRET` stays unset in Heroku**. In that state the webhook answers 503 before it touches the database, so H-1 cannot fire. Setting the secret, or registering the webhook in Loops, has to wait for the H-1 fix. M-1 should also be closed before `LOOPS_LIFECYCLE_ENABLED=true`.

## Executive summary

The two unauthenticated surfaces are well built. The HMAC link token is verified in constant time. All HTML output is escaped. The GET is read-only, so link scanners cannot record an answer. There is no redirect, the CSP and frame headers are strict, the webhook signature follows Standard Webhooks with a 5-minute tolerance and an idempotency ledger, and no email address or free text reaches PostHog. The new tables cascade on user deletion and boot is well guarded.

The main risk is availability. Both handlers are `async def` but make synchronous SQLAlchemy and Redis calls. The web dyno runs a single uvicorn worker (`--workers 1`), so a burst of Loops webhooks (one `email.delivered`, then opens and clicks, for every recipient of a campaign) blocks the event loop for every user of the app. The second risk is trust in `contactIdentity.userId`: the webhook acts on any userId it receives without checking that the contact's email belongs to that user.

## Critical findings

None.

## High findings

#### H-1: Webhook and action handlers block the single event loop with synchronous DB I/O
- **Severity**: High (availability of the whole API)
- **Location**: `app/api/v1/endpoints/email_lifecycle.py`, `loops_webhook` and `email_action_confirm` (both `async def`). They call `service.process_webhook` and `service.handle_action`, which are synchronous. Procfile: `web: uvicorn app.main:app ... --workers 1`.
- **Description**: In an `async def` route FastAPI runs the body on the event loop. `process_webhook` makes several blocking round trips per call: a receipt INSERT plus commit, `_load_user`, the `email_contact_state` read, create and commit, the `has_accepted_agreements` query inside `_capture`, and a Redis GET or SET. While one of these calls runs, no other request in the process makes progress. That includes conversations, voice, Reflect and the auth checks.
- **Failure scenario**: The "new look" campaign (scheduled for tonight, 21.10, 23:30 UTC) or any later campaign or loop sends N mails. Loops then fires N `email.delivered` webhooks within minutes, followed by opens and clicks. Each call takes several Azure round trips, so the cumulative blocking runs to tens of seconds or minutes, concentrated in exactly the window when users open the mail and then the app. The result is latency spikes, H12 timeouts and dropped realtime sessions. No attacker is needed, normal traffic is enough.
- **Remediation** (backend-api): keep the `await request.body()` read on the loop, then hand the synchronous work to the threadpool:
  ```python
  from starlette.concurrency import run_in_threadpool
  result = await run_in_threadpool(service.process_webhook, db, str(webhook_id), payload)
  ```
  Do the same for `service.handle_action` in `email_action_confirm`, and for `db.rollback()` in the except blocks. `verify_webhook_signature` is pure CPU and can stay inline. Better still, for the high-volume `email.delivered`/`email.opened` events: answer 200 right after the signature check and the receipt insert, and push the rest (state update, PostHog) to an RQ job on `default`. Add a test that the handler is non-blocking (it calls `run_in_threadpool`), or at minimum a code comment, so nobody reverts it.
- **Interim gate**: until this ships, keep `LOOPS_WEBHOOK_SECRET` unset (the endpoint then answers 503 without any DB work) and do not register the webhook in Loops.

## Medium findings

#### M-1: Webhook trusts `contactIdentity.userId` without binding it to the account's email
- **Location**: `app/services/email_lifecycle.py`, `process_webhook` (`user_id = identity.get("userId")`, then the state writes and `_capture(..., user_id, ...)`).
- **Description**: A forged webhook is not possible without `LOOPS_WEBHOOK_SECRET`; that part is correctly verified. The problem is what a genuine, Loops-signed webhook carries. The userId comes from the Loops contact record, and a Loops contact can be created without our backend. Every Loops team has a public signup form that accepts contact properties from unauthenticated visitors. Loops may also hold contacts imported or edited by hand. The Firebase UID itself is not secret: it is the plain prefix of `emailLinkToken`, which appears in every action-link URL, so it travels with forwarded mails and sits in Heroku router logs (see L-2).
- **Failure scenario** (to verify, not confirmed): if the Loops form, or any other path, lets someone set `userId` on a contact, an attacker creates a contact with their own address and the victim's UID. When the attacker unsubscribes, reports spam or clicks a link, a correctly signed webhook arrives carrying the victim's userId. The backend then sets `unsubscribed_at` or `suppressed_reason` on the victim (which excludes them from P9) and writes `last_click_at`. It also emits `email_unsubscribed`/`email_clicked` to PostHog under the victim's distinct_id, which corrupts the holdout measurement. There is a worse variant: Loops may resolve `events/send` (which carries email plus userId) by userId and attach the victim's events and contact properties to the attacker's contact, including `emailLinkToken` and the `trialEndingSoon` usage counts (`reflects`, `activeDays`). The attacker would then receive the victim's lifecycle mail. That is mental health usage metadata going to a third party, and it would make this High.
- **Remediation**:
  1. (backend-api) In `process_webhook`, act on `userId` only when `contactIdentity.email` matches `users.email` for that id (case-insensitive, compared with `hmac.compare_digest` on normalized strings). On a mismatch, skip the state update and PostHog and log only `"identity mismatch"` (no email, no uid). Add a test for it.
  2. (integration-devops) Before `LOOPS_LIFECYCLE_ENABLED=true`, verify in Loops: (a) the public form endpoint rejects or ignores `userId`, and (b) how `POST /v1/events/send` and `PUT /v1/contacts/update` resolve a contact when `email` and `userId` point to different contacts (Loops docs plus one test on a test contact, not on prod data). If (b) prefers userId, this finding is High and blocks enabling.

#### M-2: Unbounded request body read on two unauthenticated endpoints
- **Location**: `email_lifecycle.py`: `await request.body()` in `email_action_confirm` (it truncates to 4096 only AFTER reading the whole body) and in `loops_webhook` (it reads everything before verifying the signature).
- **Failure scenario**: an anonymous client sends a body of several hundred MB to either route. The single 512 MB web dyno buffers all of it and hits R14/R15 memory errors or a restart, taking the whole API down. No token or signature is needed.
- **Remediation** (backend-api): reject on `Content-Length` above a cap (4 KB for `/email/a`, 256 KB for the webhook) with 413. Then read with `request.stream()` and stop once the cap is exceeded, which covers chunked bodies with no Content-Length. The webhook still has to keep the raw bytes for the HMAC check.

#### M-3: Legal basis for lifecycle and re-engagement mail, and health-related answers sent to PostHog
- **Location**: `emit_event`/`update_contact` gate on `has_accepted_agreements` (that is, `gdpr_consent_at`, the agreements screen). `handle_action` sends `email_action_clicked {program: "P5", answer: "therapy_ended"}` and P4b answers to PostHog. `loops_sync.sync_all_users_to_loops` now adds lifecycle properties (`hasFirstConversation`, `isPremium`, `inTrial`, `emailLinkToken`, `emailPref`) for EVERY contact, regardless of the kill switch and of consent.
- **Description**: Accepting the terms is not marketing consent. P6a/P6b/P9 are re-engagement marketing mails, and P1/P2/P3 are partly promotional. In the context of a mental health app, the fact that someone is a user, together with activity flags and "my therapy ended", can be health-related data under Art. 9 GDPR, and both Loops and PostHog are processors outside the user's direct view. The nightly sync was already sending users without consent to Loops before this branch, with therapy metadata such as `therapy_duration` and the session totals. This branch widens that slightly; it did not introduce it.
- **Remediation**:
  1. (lead plus lawyer, ties to the open "ART9 gate" and gdprConsent items in memory) Confirm the legal basis for each program: transactional/service (P3b, P4a) versus marketing (P6, P7, P9). For marketing programs, require an explicit marketing opt-in or a documented soft opt-in, and make sure the Loops `subscribed` state reflects it.
  2. (backend-api) Map the P5 answer `therapy_ended` to `other` in PostHog unless an `ARTICLE9_HEALTH` consent is active (`is_consent_active`). It can stay as-is in `email_contact_state`.
  3. (data-analytics, owner of `tasks/loops_sync.py` per the team's practice) Add a consent filter to the nightly sync, or at least skip the lifecycle block for users without `gdpr_consent_at`. Track the pre-existing part as its own item.

#### M-4: Action-link token never expires and cannot be revoked per user
- **Location**: `link_token`/`verify_link_token` (stable `<uid>.<hmac>`, no timestamp, no program binding).
- **Description**: The token is a bearer credential that lives forever. It sits in every mail, in Loops contact data, in Loops click-tracking redirects and in router logs (L-2). The only revocation is rotating `EMAIL_LINK_SECRET`, which breaks every mail ever sent. What a holder can do is limited to writing the email preferences, the re-permission answer and survey answers, plus PostHog events under the user's id. No data can be read, so this stays Medium/Low; it is listed here because it is the main lever behind M-1 and L-2.
- **Remediation** (backend-api): add a version or epoch to the signed content (`uid|v1|epoch`) so a single user's token can be rotated (for example, on account email change or by support). Optionally bind the token to the program, or give it a long expiry (180 days) through the nightly sync, which rewrites `emailLinkToken` anyway. Refuse to boot-enable links when `len(EMAIL_LINK_SECRET) < 32` (log ERROR and treat it as empty), because a short secret can be brute-forced offline from any received link.

## Low findings

- **L-1: Webhook receipt committed before processing.** In `process_webhook` the receipt is committed first. If `_load_user` or a later step raises, the endpoint returns 500 and Loops retries with the same `webhook-id`, which is then answered `duplicate`. The event is lost (an unsubscribe or bounce never recorded). Fix (backend-api): insert the receipt in the same transaction as the state update, or delete it in the except path before returning 500.
- **L-2: Token and UID in logs.** Heroku router and uvicorn access logs record the full GET query (`/api/v1/email/a?t=<uid>.<hmac>&...`), and these flow to the log drain. Fix (integration-devops/backend-api): keep the query out of the logs (an uvicorn access-log filter for `/email/a`). Or move the token into the URL fragment, which the GET page then posts. A fragment needs JS, which the CSP forbids today, so the log filter is the simpler route.
- **L-3: Google Fonts on the action page.** The page loads Figtree from `fonts.googleapis.com`, which sends the visitor's IP to Google on a page that confirms they use a mental health app (EU case law: LG München 2022). `Referrer-Policy: no-referrer` is set, which helps, but the IP still goes. Fix (backend-api): drop the webfont (Arial fallback) or self-host it, and tighten the CSP to `style-src 'unsafe-inline'`.
- **L-4: Pause and updates-only are enforced only by the Loops workflow start filter.** Per SPEC 3, the filter is applied at workflow entry. A user who pauses mid-workflow will still get the remaining steps, although the page told them "We will pause these emails for 30 days." `emit_event` also never checks `email_contact_state`. Fix (integration-devops in Loops, backend-api optional): add an `emailPref != paused` filter before each send step, and/or skip `emit_event` for paused users.
- **L-5: Deletion race with more than one worker.** If a lifecycle job has already loaded the user when the account is deleted, and `loops_delete_contact` runs on another worker before that job's `events/send`, Loops re-creates the contact (email, userId, token) after the erasure. With today's single worker, jobs run one after another, so this cannot happen now. Pending RQ retries are safe: they re-load the user and return `no_user`. Fix (backend-api, when scaling workers): enqueue `loops_delete_contact` with a short delay (`enqueue_in` 10 min), or re-check the user after a successful Loops call and delete the contact if the user is gone.
- **L-6: Request-session rollback in hooks.** `notify_first_value` calls `db.rollback()` on the caller's request session when its read fails. That discards any uncommitted work of the caller (`end_redis`, `_maybe_emit_user_activated`). `is_first_paid_subscription` swallows a DB error without a rollback, which leaves the purchase request's session in a failed state. Both are unlikely, since the tables exist through `create_all`. Fix (backend-api): run these reads in a nested savepoint (`db.begin_nested()`) or on a short-lived `SessionLocal()`.
- **L-7: Pre-existing email logging in `loops_client`.** `loops_delete_contact` logs the email address, and `loops_upsert_contact` logs the Loops response body, which can echo it. `update_contact` now calls the upsert more often. The new `loops_send_event` correctly does not log the body. Fix (backend-api): log a hash or nothing, matching `loops_send_event`.
- **L-8: No rate limiting** on `/email/a` and `/webhooks/loops`. Each rejection is cheap (an HMAC compare, no DB work), so the impact is small once M-2 and H-1 are fixed. Consider a per-IP limit on POST `/email/a`.

## Items verified as correct

- **Token**: HMAC-SHA256 with a domain prefix, 22 base64url chars (132 bits), `hmac.compare_digest`, length cap 256. With an empty secret every link is rejected. The GET validates without touching the DB, so its responses do not reveal whether a user exists. The POST only reaches the DB after a valid HMAC, so there is no user enumeration through timing or content.
- **GET is read-only** (no `last_click_at`, no PostHog). State changes only on the POST. CSRF is not an issue, because a forged form needs a valid token for that user.
- **XSS**: every interpolated value goes through `html.escape(..., quote=True)`. `i` is capped at 16 chars on the GET and regex-checked on the POST. Program and answer are allowlisted. No user value reaches the headline or sentence text.
- **Headers**: `no-store`, `no-referrer`, `noindex`, `X-Frame-Options: DENY`, `nosniff`, and a CSP with `default-src 'none'`, `form-action 'self'`, `frame-ancestors 'none'`, `base-uri 'none'`. There is no redirect, so no open redirect.
- **Webhook**: 503 when no secret is set, Standard Webhooks content `{id}.{ts}.{body}`, `whsec_` base64 key, multi-signature `v1,` entries with constant-time compare, ±300 s tolerance, idempotency by `webhook-id` (PK) with 30-day retention (longer than the tolerance, so replays are covered). Error responses carry no detail.
- **PostHog**: only the program, answer enum, issue code, holdout and the source, email, campaign and loop ids. No email or free text. Every capture is gated on `has_accepted_agreements`, which fails closed. For deleted users it returns False, because the therapy context rows cascade away.
- **Loops payloads**: numbers, enums, dates and booleans only. `loops_send_event` does not log response bodies. The idempotency key is a hash.
- **Kill switch**: defaults to False, an unparsable value means OFF, and every enqueue, emit and job checks it. Secrets default to empty with safe behavior. No secret is logged. `.env.example` lists the keys without values.
- **GDPR erasure**: `email_lifecycle_log` and `email_contact_state` have FK `ON DELETE CASCADE` in both the model and the migration, and the account deletion hard-deletes the user row. `loops_webhook_receipts` and the Redis program cache contain no personal data. Pending and retried RQ jobs carry only the user id and return `no_user` after deletion. Claims on a deleted user fail on the FK and are treated as duplicates.
- **Boot safety**: the router import is guarded in `api.py`. The new model uses String/Boolean/Date only, with no `Enum`, and `create_all` builds the tables on boot. The migration is idempotent with existence checks and `lock_timeout`, has no `bind.commit()`, and has a single head (`ke_a7c3e9f1b2d4 -> m321e4c5a6b7`). `setup_email_lifecycle_jobs` never raises. The new config fields all have defaults. The `email_lifecycle` service imports only stdlib, sqlalchemy and settings at module level, so the unguarded import in `users.py` is safe.

## GDPR compliance status (this feature)

| Requirement | Status | Notes |
|---|---|---|
| Right to erasure | OK | New tables cascade; Loops contact deleted by the existing RQ job; L-5 only once there are multiple workers |
| Data minimization | Partial | Booleans and counts only; nightly sync sends to users without consent (M-3, pre-existing) |
| Right to portability | Not covered | `email_contact_state` is not in the data export; add it when the export is next touched (Low) |
| Consent for processing | Open | Agreements consent used as the gate for marketing mail; lawyer decision needed (M-3) |
| Encryption in transit | OK | HTTPS to Loops; Heroku TLS |
| Retention policy | OK | Webhook receipts purged after 30 d; log and state live as long as the account |

## Horizontal privilege escalation audit

| Endpoint | Identity source | Scoped correctly |
|---|---|---|
| GET /api/v1/email/a | HMAC token, uid inside it | Yes, read-only and no DB access |
| POST /api/v1/email/a | HMAC token | Yes, it writes only the token owner's row |
| POST /api/v1/webhooks/loops | Signed payload `contactIdentity.userId` | Partial: trusts the Loops contact's userId with no email binding (M-1) |
| Hooks in users.py / conversations.py | `current_user_id` from the Firebase token | Yes |

## Remediation priority list

1. **Before setting `LOOPS_WEBHOOK_SECRET` or registering the webhook**: H-1 (backend-api). Interim: deploy with the secret unset.
2. **Before `LOOPS_LIFECYCLE_ENABLED=true`**: M-1 code fix (backend-api) plus the Loops matching verification (integration-devops), and M-2 (backend-api).
3. **Current sprint**: M-3 (lead and lawyer, backend-api, data-analytics), M-4 (backend-api), L-1, L-3, L-4.
4. **Backlog**: L-2, L-5, L-6, L-7, L-8, and adding `email_contact_state` to the export.

Fix verification: security-guardian re-reads `email_lifecycle.py` (endpoint and service) after the H-1, M-1 and M-2 fixes.

---

## Fix verification: commit fe10aae (re-review of 7f0ac28..fe10aae), 2026-10-21

I re-read the full diff plus `app/api/v1/endpoints/email_lifecycle.py`, `app/services/email_lifecycle.py` and `app/tasks/email_lifecycle.py` at fe10aae. I ran the three lifecycle test files in a temporary detached worktree, removed afterwards (the lead's working copy was not touched): **146 passed**. A plain `import app.main` could not run locally, because `DATABASE_URL` was unresolved in that worktree (an environment gap, not a code error). The router and models import cleanly inside the test suite.

| Finding | Status | Verification notes |
|---|---|---|
| H-1 event loop blocking | **Fixed** | The webhook verifies the signature (pure CPU), then writes the receipt via `run_in_threadpool`, enqueues `process_loops_webhook` on RQ "default" and answers 200. If the enqueue fails, it releases the receipt and answers 503, so Loops retries. `handle_action` and the rollbacks run in the threadpool. All DB and PostHog work for webhooks now happens in the worker, not the web dyno. |
| M-1 trusted userId | **Fixed in code**, Loops-side check still open | `_webhook_user` acts only when `contactIdentity.email` (casefold) equals `users.email`, and logs a mismatch without the address or uid. The outbound question remains: how Loops resolves `events/send` when email and userId point to different contacts. integration-devops should confirm it, and that the public form cannot set `userId`, before `LOOPS_LIFECYCLE_ENABLED=true`. This is a pre-enable condition, not a deploy blocker. |
| M-2 unbounded body | **Fixed** | `read_capped_body`: Content-Length is checked first, then a streamed read with a running cap (4 KB / 256 KB); 413 on overflow; an unparsable Content-Length is rejected. |
| M-3 P5 answer to PostHog | **Fixed** (the code part) | `email_action_clicked` for P5 carries only `program`. Legal basis and the nightly-sync consent filter are accepted by the lead as a lawyer follow-up. |
| M-4 token | **Partially fixed**, accepted | The version is now signed in (`<uid>.v1.<hmac>`), and a secret shorter than 32 chars disables links (logged once, by length only). Per-user revocation and expiry are not implemented; the residual is Low (preference writes only). |
| L-1 receipt before processing | **Fixed** | Receipt plus enqueue; the worker job raises, so RQ retries 3 times. |
| L-3 Google Fonts | **Fixed** | Webfont removed; CSP is now `style-src 'unsafe-inline'` with no font-src. |
| L-6 request-session rollback | **Fixed** | Hooks read on their own short-lived `_HookSession` and never touch the caller's session. |
| L-2, L-4, L-5, L-7, L-8 | Open (Low, backlog) | Unchanged. |

### New observations in fe10aae (Low, not blocking)
- **N-1: Webhook payload stored in Redis.** `enqueue_webhook_processing` puts the whole Loops payload, including `contactIdentity.email`, into the RQ job args. Jobs that fail permanently stay in the FailedJobRegistry (the RQ default `failure_ttl` is one year), and account erasure does not remove them. Fix (backend-api): enqueue a minimized dict (eventName, sourceType, the campaign/loop/transactional/email ids, the names needed for the program cache, userId and `sha256(casefold(email))`), compare hashes in `_webhook_user`, and set `failure_ttl` to 7 days on the enqueue.
- **N-2: Synchronous Redis enqueue on the event loop.** `enqueue_webhook_processing` runs a few Redis commands directly in the async handler. That is a short round trip, much lighter than before, but it could be wrapped in `run_in_threadpool` for consistency.
- **N-3: Worker load.** A campaign burst now becomes N short jobs on "default" for the single worker. That is acceptable, because interactive jobs use `high`, but scheduled default jobs may run late during a large send. This is operational, not a security issue.

## Final verdict (fe10aae): DEPLOY OK

No Critical or High findings remain. Conditions for switching it on:
1. Before `LOOPS_LIFECYCLE_ENABLED=true`: integration-devops confirms how Loops resolves contacts (M-1 residual) and that the public form cannot set `userId`.
2. Set `EMAIL_LINK_SECRET` to at least 32 random characters, otherwise action links stay disabled by design.
3. The migration must run (`alembic upgrade head`, m321e4c5a6b7) together with the deploy. The tables are also created on boot, so this is a consistency step, not a crash risk.
4. Backlog: N-1 (do it in the next touch of this file), L-2, L-4, L-5, L-7, L-8, and M-3 legal follow-up with the lawyer.
