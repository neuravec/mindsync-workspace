# Security Audit Report: subscription + onboarding redesign: 2026-10-02

Auditor: security-guardian (read-only). Scope: uncommitted working trees on `feat/subscription-onboarding-redesign` in `MindSync/` (backend) and `mindsync-frontend/` (Flutter), checked against SPEC.md sections 1, 2 and 5 and `copy-en.md`.

Method: full `git diff` and every new file in both repos, plus the unchanged code these paths call (receipt verifiers, soft-delete and restore, the hourly expiry job, sign-out, FCM, PostHog identify). One targeted backend pytest run was used to confirm H-1 (2 tests, both pass, see H-1).

## Executive summary

No horizontal privilege escalation, authentication bypass, injection or mental-health content leak was found. `GET /users/usage` is correctly scoped to the token's user and exposes only counts. Same-account receipt replay is safe: expiry is anchored to the store's purchase time and the SKU is checked against the store.

Two High findings block deployment. Both are backend-only and small:

1. **H-1 (new in this batch):** the deprecated but still routable `POST /prep-cards/auto-generate` now gives Free users unlimited AI "Before therapy" cards. The new counter ignores `generation_type="auto"` rows, and the endpoint writes exactly that type.
2. **H-2 (existing hole, in a function this batch edits):** `POST /users/one_time_purchase` accepts any SKU with a client-chosen `duration_days`. On iOS the receipt's `in_app` list also contains subscription transactions, so one month of `premium_m_01` (or a free sandbox/TestFlight purchase) can be turned into years of Premium.

The Medium items are about Free-limit bypass (delete-and-recreate, parallel requests) and a special-category attribute (`in_therapy`) going to PostHog beyond the purpose the user consented to.

**Deployment verdict: BLOCKED until H-1 and H-2 are fixed and re-verified.** The Medium items should land in this sprint. They do not block on their own.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 2 |
| Medium | 3 |
| Low | 6 |
| Info | 9 (one of them the accepted copy risk) |

---

## Critical findings

None.

---

## High findings

### H-1: Free users get unlimited AI "Before therapy" cards through `/prep-cards/auto-generate` (regression in this batch)

- **Severity:** High (it bypasses the paywall for a whole feature with no limit, and every call is a paid GPT call carrying the user's therapy context).
- **Location:**
  - `MindSync/app/api/v1/endpoints/prep_cards.py:531-589` (`auto_generate_prep_card`). The gate is at line 553. Line 563 writes `"generation_type": "auto"`. The AI call is `_process_prep_card_ai`.
  - `MindSync/app/crud/crud.py:1269-1292` (`count_prep_cards_this_month`). The new filter `or_(generation_type IS NULL, generation_type != "auto")` is at lines 1286-1289.
- **Description:** The endpoint gates on `can_use_ai(db, uid, AI_FEATURE_PREP_CARD)`, which compares `count_prep_cards_this_month` to the limit of 1. This batch changed that counter to exclude auto cards, so cron cards generated during a trial would not eat a Free allowance. But the cards this endpoint creates are also `generation_type="auto"`, so they never count either. A Free user who has made no manual Before therapy card this month passes the gate on every call, forever. Before this batch, auto cards counted against the shared pool of 5, so the endpoint was capped.
- **Evidence:** `test_subscription_onboarding_redesign.py::test_auto_prep_card_does_not_consume_before_therapy` (line 286) asserts that `can_use_ai` is still True after an auto card exists. I ran it together with `test_prep_auto_generate_403_detail_unchanged`: 2 passed. The 403 test only covers a user who already has a manual card, so the bypass path is untested. The endpoint docstring says it has had no client caller since 2026-08-10, but it is still mounted and reachable with any valid Firebase token.
- **Failure scenario:** A Free user (or a script holding their own token) calls the endpoint repeatedly. Each call creates a full AI prep card (GPT plus RAG context), so the cost per user is unbounded and the "1 a month" Free limit means nothing for this feature. The client paywall at 0 is irrelevant because the endpoint is called directly. No other user's data is exposed.
- **Remediation (backend-api):** Pick one of these.
  - Preferred, since the endpoint has zero callers: make it Premium-only. Replace the gate with `if not is_user_premium(db, current_user_id): raise HTTPException(403, "Free tier AI limit reached. Upgrade to auto-generate prep cards.")`. This keeps the detail string for old builds. Trial users stay premium through `is_user_premium`, so the cron and the endpoint behave the same way.
  - Or retire it with a `410 Gone`.
  - Do NOT bring back counting of cron auto cards. Excluding them is the right call for the cron path.
  - Add a test: Free user, no manual card, call `auto_generate_prep_card` twice. Both calls (or at least the second) must return 403, and no row may reach `COMPLETED`.

### H-2: `/users/one_time_purchase` accepts subscription SKUs with a client-chosen `duration_days` (existing hole, function changed in this batch)

- **Severity:** High (fraudulent long-term Premium for the price of one month, or for free through sandbox).
- **Location:**
  - `MindSync/app/api/v1/endpoints/users.py:626-636` (`_resolve_one_time_duration_days`: any SKU other than the starter pack returns `requested_days or 14`) and line 685 where it is used.
  - `MindSync/app/schemas/schemas.py:468-474` (`product_sku: str`, `duration_days: Optional[int]`, no allowlist, no bounds).
  - `MindSync/app/services/subscription_service.py:711-786` (`verify_apple_one_time_product`). Line 760 matches any `receipt.in_app` entry whose `product_id` equals the client-sent SKU. Line 746 falls back to the sandbox on status 21007.
  - `subscription_service.py:75-180` (`deactivate_expired_subscriptions`) only re-verifies after `end_date` has passed.
- **Description:** The server never checks that `product_sku` is a one-time product. On Apple, `verifyReceipt`'s `receipt.in_app` array also contains auto-renewable subscription transactions (Apple's documented receipt format; the subscription path uses `latest_receipt_info` for the same data). So a receipt holding a `premium_m_01` purchase matches `product_sku="premium_m_01"`. Expiry is then `purchase_date + duration_days`, with `duration_days` taken from the client. `activate_user_access_until` writes that `end_date` and labels the row `purchase`. The hourly job ignores the row until `end_date` passes, so a far-future date is never re-checked. The cross-account guard does not help because the receipt belongs to the same user. Google is not affected: `purchases.products.get` rejects a subscription token.
- **Failure scenario:** An iOS user buys one month of `premium_m_01` and calls `POST /users/one_time_purchase` with `{"platform":"apple","product_sku":"premium_m_01","base64_receipt":<their receipt>,"duration_days":36500}`. Then they cancel the subscription and keep Premium until 2126. With the 21007 sandbox fallback, a TestFlight or sandbox tester gets the same result without paying anything. I am not writing a working exploit beyond this description. The verification step below confirms it offline.
- **Why it belongs in this batch:** The batch edits this exact function and the implementer flagged the problem. The batch also starts selling the one-time product prominently. The fix is about 5 lines.
- **Remediation (backend-api):**
  1. Allowlist one-time SKUs: `ONE_TIME_PRODUCT_SKUS = {settings.STARTER_PACK_PRODUCT_SKU}`. If `data.product_sku` is not in that set, return 400 `unsupported_product` BEFORE the `SubscriptionReceipt` row is created.
  2. Ignore client `duration_days` completely. Take the duration from a server-side map (`{sku: days}`). The field can stay in the schema for old clients but must not be read.
  3. Defense in depth: in `verify_apple_one_time_product`, skip `in_app` entries that carry `expires_date_ms` (subscription transactions).
  4. Tests: (a) `product_sku="premium_m_01"` returns 400 and creates no receipt row; (b) the starter pack with `duration_days=36500` still gets 14 days; (c) a mocked Apple response with a subscription entry is not accepted as a one-time purchase.
  5. Follow-up (database-administrator, read-only): look for existing `user_subscription` rows with `granted_via='purchase'` and an `end_date` more than 400 days away whose latest VERIFIED receipt is a one-time receipt with a non-starter SKU. That shows whether this was ever abused.

---

## Medium findings

### M-1: Free limits can be reset by soft-delete then recreate (then undo the delete)

- **Location:** All three counters in `MindSync/app/crud/crud.py:1251-1310` filter `deleted_at IS NULL`. The delete endpoint is `MindSync/app/api/v1/endpoints/timeline.py:82-111`. Restore is in `crud.py` (`restore_*`, for example 3990-4010, inside the undo window). The same pattern applies to `count_completed_recordings` (`crud.py:2209`, lifetime limit 2).
- **Scenario:** A Free user creates an After therapy note (AI, 1/1 used), deletes it from the timeline (counter back to 0), creates another AI note, then restores the first one inside the undo window. Repeating this gives unlimited AI notes, and the user keeps all of them. The mechanism existed before this batch, but with limits now at 1/1/3 it becomes the obvious way around the paywall. This is cost and revenue abuse. No data is exposed.
- **Remediation (backend-api):** Count AI processing that happened, not rows that are still visible. The cheapest option needs no migration: drop the `deleted_at IS NULL` filter from the three monthly counters and from `count_completed_recordings`, since soft-deleted rows stay in the table until purge. Update the docstrings and the `/usage` doc to say that deleting a note does not give the allowance back. Add tests: create, delete, then `can_use_ai` is still False.

### M-2: Parallel requests all pass the gate (check then act race)

- **Location:** `_therapy_helpers.py:98-110` (`can_use_ai`); the create endpoints, for example `debriefs.py:416-446`; the counters only count `COMPLETED`.
- **Scenario:** AI processing runs synchronously inside the create request and takes seconds. Rows in `PENDING` or `PROCESSING` do not count. A Free user who fires N create requests at once (the web dyno runs sync endpoints in a thread pool) gets N AI notes: all N read `count < limit` before any of them completes.
- **Remediation (backend-api):** (1) Count `PENDING`, `PROCESSING` and `COMPLETED`, excluding only `FAILED` and `PLAIN_TEXT`. The PENDING row is inserted before the AI call, so this shrinks the window to milliseconds. (2) Serialize per user and feature: wrap check plus insert in `pg_advisory_xact_lock(hashtext(user_id || ':' || feature))` (Postgres only; on SQLite in tests make it a no-op). Add a test that two sequential calls without commit ordering still allow only one AI note.

### M-3: Therapy status (Art.9 special-category data) sent to PostHog beyond the consented purpose

- **Location:**
  - `mindsync-frontend/mindsync_app/lib/screens/wow/cubit/wow_cubit.dart:119-120` and `226-227` (`'in_therapy'`, `'has_schedule'`)
  - `wow_cubit.dart:92` (`_pushVariant` = `'in_therapy'` / `'no_therapy'`, sent as `variant` on `push_prompt_viewed` / `push_prompt_result`)
  - `wow_cubit.dart:434` (`capture_types_offered`, already a proxy for therapy status before this batch)
  - `therapy_onboarding_cubit.dart` `_flowProps` / `onboarding_completed` (`total_steps` 7 means "in therapy")
- **Description:** Whether a person is in psychotherapy is health data under GDPR Art.9. The Art.9 checkbox (`app_en.arb:2615`) reads "Yes, use my therapy status to personalise my experience", which covers personalisation, not product analytics. These events go to PostHog against the identified Firebase UID (identify happens at the consent step, `therapy_onboarding_cubit.dart:329`). The value is only true when the user consented, so nothing leaks without consent. The issue is purpose limitation under Art.5(1)(b) and Art.9(2)(a).
- **Remediation (flutter-mobile):** Remove `in_therapy` and `has_schedule` from `post_onboarding_build_viewed` and `personal_reveal_viewed`. Change `variant` on the push events to a neutral label that does not encode therapy status, or drop it. Remove `total_steps` from step and completion events, or send it only as `branch_skipped: true/false` after legal confirms. `capture_types_offered` (existing) should become a count. If the business needs the split, get a written legal decision and update the Art.9 consent text and privacy policy first. Do not keep sending it silently.

---

## Low findings

- **L-1: AI and speech-to-text cost reachable without using up any allowance (existing).** The `/guiding-questions` endpoints of debriefs, prep cards and between-sessions (for example `debriefs.py:385-413`) call OpenAI for a Free user who is under the limit, and never increment anything, so a 0/1 user can call them without limit. The voice create endpoints transcribe (Whisper / AssemblyAI, `debriefs.py:522-560`) before the gate, even at the limit. That is by design, because the plain-text entry needs a transcript. There is no per-user rate limit on any of these. **Owner: backend-api.** Add a Redis per-user limiter (reuse the `app/services/clinician_rate_limit.py` pattern), for example 20 guiding-question calls a day and 10 voice creates an hour for Free users.
- **L-2: `GET /users/usage` has no rate limit.** It costs about 9 indexed COUNT queries per call and is called on Home load, app resume and after each gated action. It is safe otherwise: the user id comes only from the token, there are no path or query parameters, it returns counts and plan only, errors return a generic `usage_unavailable`, and the log line has the UID only (`users.py:1046-1063`). **Owner: backend-api** (optional 30 s per-user cache), **flutter-mobile** (debounce resume refreshes to at most 1 per 30 s).
- **L-3: Starter pack refunds are not revoked (existing, all IAP).** The backend has no App Store Server Notifications or Google RTDN handling (no `refund` / `voided` handling anywhere), so a refunded starter pack keeps up to 14 days. The new "never shorten" rule cannot be abused on its own: it only keeps a longer `end_date` the user already held legitimately, and replaying a receipt cannot extend past `purchase_time + 14 d`. **Owner: backend-api**, backlog: RTDN plus App Store Server Notifications v2 handler.
- **L-4: The device-wide "onboarding completed" pref survives sign-out (existing).** `PreferenceKey.therapyOnboardingCompleted` is not keyed by uid and is not cleared in `MainPageCubit.signOut` (`main_page_cubit.dart:71-115`). `PostLoginDestinationResolver.resolve` (`post_login_destination_resolver.dart:43`) trusts it before asking the server. If a second account that never finished onboarding signs in on the same device, it lands on the main page without passing the agreements screen. This is not worse than before (login always went to the main page), but the new resolver's "single source of truth" claim does not hold for this case. **Owner: flutter-mobile.** Clear the key in `signOut`, or key it by uid. The new uid-keyed flags (`ms_post_onboarding_offer_seen_`, `ms_push_preprompt_handled_`, `ms_trial_reminder_seen_`, `ms_trial_ended_paywall_seen_`, `ms_premium_last_product_`) are fine as they are.
- **L-5: `onboarding_lead_source_other_text.first_50_chars` sends user-written free text to PostHog (existing, previously accepted in an earlier security verdict).** `onboarding_lead_source_view.dart:52-64`. Users can type names ("my therapist Dr X told me") or health details. **Owner: flutter-mobile.** Keep `text_length` only, or match the text on device against a short keyword list ("tiktok", "therapist", "reddit") and send the matched category.
- **L-6: Honest-billing details in the starter copy.**
  - (a) The VERBATIM starter body says "just for five dollars" while the store price is localized (EUR, PLN, NOK, SEK storefronts). The CTA and billing line show the real `{price}` before purchase, so the user is not misled at the point of sale. Still, locales should not translate "five dollars" literally. **Owner: flutter-mobile** (localized arbs: use the price placeholder or a neutral phrase in non-USD locales, operator to confirm).
  - (b) "Premium for 2 weeks from today" (`postOnboarding_billingStarter`) can be up to about 24 h short: `end_date` is stored as a DATE (`subscription_service.py`, `activate_user_access_until`), and `is_user_premium` stops at 00:00 UTC of that date. A purchase at 23:00 UTC gives about 13 d 1 h. **Owner: backend-api.** Round the starter end date up (`(purchase + 14 d).date() + 1 day`), or change the copy to "until {date}".

---

## Info

- **I-1 (accepted risk, does not block): "Most of our users feel like they got a second therapy session in that time."** Kept by explicit operator decision. Regulatory exposure, recorded once:
  - (1) "Most of our users" is a factual claim that needs evidence on file (EU UCPD 2005/29/EC Art.6 misleading actions, US FTC Act s.5 substantiation).
  - (2) Equating app use with a therapy session is a health-benefit implication that store reviewers watch for (App Store Review Guideline 1.4.1, Google Play Health misrepresentation policy) and that reads as a therapeutic equivalence claim.
  - Mitigation without changing the sentence: keep the survey or interview evidence behind "most" in `competitive-reports/` or `analytics-reports/`, and keep the rest of the paywall free of clinical claims (it is: no "full data export", no clinical outcomes).
  - Rating: Low on its own line, accepted.
- **I-2: Receipt replay and SKU spoofing verified safe for the starter pack.** Expiry is computed from the store's `purchaseTimeMillis` / `purchase_date_ms`, not from "now" (`subscription_service.py:663-786`). A second verification of the same receipt by the same user is idempotent. The cross-account guard (`find_cross_account_receipt`) is intact. Starter treatment requires `product_sku == ms_starter_package`, and that SKU is verified against the store, so a non-starter receipt cannot get the starter path.
- **I-3: `verify_promo_code` and `PAID_GRANTED_VIA_VALUES` (`users.py:897`).** Correct: a starter pack row gets the additive top-up and is never downgraded. When a starter pack is bought during an active open-ended promo, the row is relabelled `starter_pack` and stays open-ended. That is cosmetic, with no access change.
- **I-4: The trial cannot be re-triggered through the API.** `POST /users/subscription` reads only `is_ios`. The client's `subscription_type`, `start_date`, `end_date` and `is_active` are ignored (`users.py:428-458`, `_create_initial_subscription` returns early when a row exists). The trial length is the server constant `SIGNUP_TRIAL_DAYS = 4` (`users.py:114`). `trial_started` is at most once per user through `_atomic_mark_trial_started`. Account delete plus re-register gives a new Firebase UID and therefore a new 4-day trial. That existed before, there is no device or email dedup, and it is an accepted business risk.
- **I-5: `/users/usage` horizontal privilege escalation check passed.** `Depends(deps.get_current_user)`, no user id parameter, every counter filters by `user_id == current_user_id`.
- **I-6: Client-only gates are cosmetic.** The paywall at 0, the offer "once per account", the day-3 sheet, the trial-ended paywall and `PremiumPlanMemory` grant no access. Tampering with them only lets a Free user reach create endpoints, which then save `PLAIN_TEXT` with no AI call. The exception is H-1. None of these flags hides the legal or consent step: the agreements screen is still screen 0 and is not skippable (`goToPreviousScreen` clamps at 1).
- **I-7: Sign-in routing and consent.** Backend errors never route to onboarding as "new user". `resolveForExistingAccount` falls back to the main page, and the splash propagates the error to its retry UI (`post_login_destination_resolver.dart`). Duration and goal are sent only for an in-therapy answer with Art.9 active (`onboarding_journey_view.dart:239-245`). Skipped modality and schedule steps send nothing. Data minimization note: if a user goes forward to "therapy type", saves it, goes back and switches to "not in therapy", the modalities already saved stay on the server. Art.9 consent is still active, so this is lawful, but flutter-mobile may want to send `therapy_modalities: []` on the switch.
- **I-8: FCM.** The pre-prompt goes through `FCMTokenService.requestPermission`, which registers the token for the signed-in user as before. `signOut` still resets FCM and PostHog before the Firebase sign-out, and now also resets `UsageCubit`. When suppressed, the cold prompt uses `getNotificationSettings` only, with no registration change.
- **I-9: Other analytics checked clean.** No orca name, focus area names, goal text, bio text, email, display name or promo code appears in any new event. Usage counts in `trial_reminder_sheet_shown` (`therapy_entries_count`, `recordings_count`, `reflect_messages_count`, `days_left`) are aggregate integers: acceptable. PostHog identify for new accounts still happens only after consent (`therapy_onboarding_cubit.dart:329`). The login-time identify is unchanged from before. Housekeeping: `MindSync/test_temp.db` (1.2 MB binary) shows as modified in the backend working tree. Keep it out of the commit.

---

## GDPR compliance status (scope of this batch)

| Requirement | Status | Notes |
|---|---|---|
| Right to erasure | OK (unchanged) | No new tables. Usage is derived from existing rows. Uid-keyed local flags remain on the device after account deletion (cosmetic). |
| Data minimization | Partial | M-3 (`in_therapy` to analytics), L-5 (free text), I-7 (stale modalities). |
| Right to portability | Not in scope | Export still does not exist. The copy correctly no longer promises it. |
| Consent for processing | Partial | Art.9 gating in onboarding is correct. Analytics use of therapy status exceeds the consent purpose (M-3). |
| Data encryption at rest | Unchanged | No new storage of content. |
| Retention policy | Unchanged | Note: the M-1 fix (counting soft-deleted rows) does not extend retention, because purge still runs. |

## Horizontal privilege escalation audit

| Endpoint | Scoped to token user | Notes |
|---|---|---|
| `GET /users/usage` | Yes | No parameters. |
| `POST /users/one_time_purchase` | Yes | Receipt bound to the caller, cross-account guard intact. See H-2 for entitlement abuse. |
| `POST /users/subscription` | Yes | Server-decided trial. |
| `POST /users/promo` (verify_promo_code) | Yes | Unchanged scoping. |
| Debrief / prep / between-sessions create, retry, guiding-questions, auto-generate | Yes | Gates are per user. Cost issues: H-1, M-1, M-2, L-1. |
| `POST /timeline/{type}/{id}/delete` | Yes | `crud.soft_delete_*` filter by `user_id`. |

## Remediation priority list

1. **Before any deploy (blocking):**
   - H-1: make `/prep-cards/auto-generate` Premium-only or return 410, plus a test. Owner: backend-api.
   - H-2: allowlist one-time SKUs, ignore client `duration_days`, skip subscription entries in Apple `in_app`, plus tests. Optional prod abuse check by database-administrator. Owner: backend-api.
   - Then security-guardian re-verifies both fixes.
2. **This sprint:**
   - M-1 (count soft-deleted rows). Owner: backend-api.
   - M-2 (count in-flight rows plus a per-user advisory lock). Owner: backend-api.
   - M-3 (drop `in_therapy`, `has_schedule`, therapy-status variants and `total_steps` from PostHog, or get a legal decision plus updated consent text). Owner: flutter-mobile.
3. **Backlog:**
   - L-1 rate limits. Owner: backend-api.
   - L-2 usage cache and debounce. Owners: backend-api and flutter-mobile.
   - L-3 refund notifications. Owner: backend-api.
   - L-4 clear the onboarding pref on sign-out. Owner: flutter-mobile.
   - L-5 lead-source free text. Owner: flutter-mobile.
   - L-6 starter copy locales and DATE rounding. Owners: flutter-mobile and backend-api.
4. **Accepted:** I-1 ("second therapy session" sentence), on file with its rationale.


---

## Re-verification 2026-10-02

Method: read-only review of the updated working trees and the new tests. Per the coordinator's instruction, no pytest or flutter test run this time (a regression run was using the shared SQLite DB), so "FIXED" here means the code path and a covering test exist, not that I executed them.

### Original findings

| ID | Status | Evidence |
|---|---|---|
| H-1 | **FIXED** | `MindSync/app/api/v1/endpoints/prep_cards.py:566`: the gate is now `is_user_premium`, with the same 403 detail. Test: `test_subscription_onboarding_redesign.py:739` (`test_free_user_with_no_manual_card_is_refused_every_time`, uses an AI spy), plus 750 (expired trial refused) and 758 (trial/premium allowed). Cron auto cards stay uncounted, which is correct now that the endpoint is Premium-only. |
| H-2 | **FIXED** | `config.py:387-396`: `one_time_product_duration_days` = `{STARTER_PACK_PRODUCT_SKU: STARTER_PACK_DURATION_DAYS}`. `users.py:642-657`: duration comes only from that map, client `duration_days` is never read. `users.py:686-693`: 400 `unsupported_product` before any receipt row or event. `subscription_service.py:744-746`: the Apple verifier refuses a non-allowlisted SKU before calling Apple. `subscription_service.py:778-782`: `in_app` entries with `expires_date_ms` / `expires_date` are skipped. Tests at lines 789, 807, 820 (`duration_days=36500` ignored), 839, 857, 873, 886, 911. The Google path relies on the endpoint check alone, which is enough because Google subscription tokens fail `products.get` anyway. A one-time prod check for past abuse (database-administrator, read-only) is still recommended. |
| M-1 | **PARTIAL** | `crud.py:1286-1340`: the counters no longer filter `deleted_at`. Tests at lines 949, 961, 972. Residual: soft-deleted rows are hard-purged after 24 h (`app/tasks/purge_deleted.py`, purge cutoff `timedelta(hours=24)` in `crud.py`), so the allowance comes back a day after a delete. Rated on its own line below as R-1 (Low). |
| M-2 | **FIXED (residual Low)** | `crud.py:1251-1283` `_free_tier_ai_usage_filter`: PENDING/PROCESSING rows younger than `FREE_TIER_INFLIGHT_COUNT_WINDOW_MINUTES` (30, `config.py:183`) now count. Tests at lines 980, 985, 994 (parallel second request falls back to plain text), 1011, 1021, 1026, 1034. Residual: `can_use_ai` still runs before the PENDING insert and there is no lock, so truly simultaneous requests can still both pass within a window of milliseconds. Rated as R-2 (Low). |
| M-3 | **PARTIAL (still Medium, see the recommendation below)** | `in_therapy` and `has_schedule` are gone from client events (no matches in `lib/`). The push `variant` now carries `session_reminders` / `checkin_reminders` (`wow_cubit.dart:94-96`). But deterministic proxies for "in therapy" remain on identified persons: `prompt_variant = therapy_cta` (`wow_cubit.dart:98`), `capture_types_offered` containing `debrief` (`wow_cubit.dart:433`), `variant = session_reminders` (only users with a schedule, which means in therapy), `total_steps = 7`, step-5 `frequency` / `session_count` / `custom_session_count` (`therapy_onboarding_cubit.dart:913-917`), and the plain fact that `onboarding_step_viewed` fires for step_index 4 and 5 only on the therapy branch. |
| L-1 | OPEN (backlog) | No per-user rate limit on the guiding-questions endpoints or voice creates. |
| L-2 | OPEN (backlog) | No server cache or rate limit on `/users/usage`. |
| L-3 | OPEN (backlog) | No refund notifications from App Store or Google Play. |
| L-4 | OPEN (backlog) | `therapyOnboardingCompleted` pref is still device-wide and not cleared in `MainPageCubit.signOut`. |
| L-5 | **FIXED** | `onboarding_lead_source_view.dart:52-63`: only `text_length` is sent, once. |
| L-6 | OPEN (backlog) | (a) "five dollars" in non-USD locales and (b) DATE truncation of the starter end date are both unchanged. |
| I-1 | Accepted risk, unchanged | "Second therapy session" sentence. |

### M-3: recommendation on the remaining proxies

Inferred data counts as special-category data too. The CJEU held in C-184/20 (OT v Vyriausioji tarnybinės etikos komisija, 2022) that data which indirectly reveal health status fall under Art.9. Removing the explicit `in_therapy` flag therefore does not change the legal position. Since the 5/7-step branching, the onboarding funnel itself reveals therapy status for every identified person. Before this batch, everyone saw steps 4 and 5, so step views revealed nothing.

The mitigating fact is that the 7-step branch, and therefore every proxy, is only reached by users who ticked the explicit Art.9 checkbox. So the issue is purpose scope, not missing consent. That checkbox reads "use my therapy status to personalise my experience" (`app_en.arb:2615`), and it does not mention analytics.

My recommendation:

1. **Do not try to strip the proxies technically.** That would mean breaking the onboarding funnel. Fix the legal basis instead: extend the Art.9 consent text (all 7 locales) and the privacy policy so they cover using therapy status for product analytics with PostHog (EU) as processor. Example direction for the lawyer: "Yes, use my therapy status to personalise my experience and to improve MindSync (product analytics)." Final wording is the lawyer's call.
2. **This needs the lawyer before the production store release.** An internal TestFlight build is acceptable in the meantime. The `gdprConsent` wording is already waiting on the same lawyer review, so bundle both.
3. **Cheap hardening to do now, regardless of the legal outcome (owner flutter-mobile):** drop `frequency`, `session_count` and `custom_session_count` from the step-5 completion event. They describe the user's therapy routine and are not needed for funnel analysis. `capture_types_offered` should become a count.
4. **Fallback** if the lawyer will not extend the consent: stop sending onboarding and post-onboarding events for the therapy branch until after `onboarding_completed`, and send only an unbranched `onboarding_completed` with no step-level split.

Severity stays Medium. It does not block the backend deploy or TestFlight, but it gates the production store release on legal sign-off.

### New findings from the fix rounds

- **N-1 (Low, owner backend-api or lead decision): sign-up `trial_started` is sent before the agreements consent.** `capture_signup_trial_started` (`posthog_service.py:982`, called at `POST /users/subscription` during account creation) sends `trial_started` and the new `$set` `plan` / `premium_source` with no `has_accepted_agreements` check. The hourly `trial_ended` path is now gated with `require_consent=True` (`subscription_service.py:280-286`). This is commercial, non-health data, but it is inconsistent with lead decision G21 and with the "nothing to PostHog before consent" onboarding rule. Either pass a consent check here too (the event would then be dropped for nearly everyone, because consent comes later in onboarding), or record a lead decision that plan events rest on legitimate interest. Not blocking.
- **R-1 (Low, M-1 residual, owner backend-api): Free limit returns 24 h after a delete.** A Free user can delete their AI notes and get the allowance back the next day. That gives at most about 30 After therapy, 30 Before therapy and 90 Between Sessions AI notes a month, and the user loses each deleted note. The bypass is now bounded and costs the user their data, so it is no longer worth Medium. Full fix: a monthly usage ledger table (migration), already in the backlog.
- **R-2 (Low, M-2 residual, owner backend-api): millisecond check-then-insert window remains.** Optional: `pg_advisory_xact_lock(hashtext(user_id || ':' || feature))` around the check and the PENDING insert.
- **New analytics scanned, clean:**
  - `usage_snapshot` (`usage_cubit.dart:151-170`) sends only `plan`, `<feature>_left` integers and `features_at_zero`. These are aggregate counts with no content, acceptable at the same level as `trial_reminder_sheet_shown`.
  - `auth_validation_failed` (`auth_body.dart:161-166`) sends only `mode` and an enum `reason`, never the email.
  - `login_failed` (`auth_cubit.dart:158-166`, `auth_failure_type.dart:9-29`) sends only `method` and an enum error class. It also merges `user-not-found` into `invalid_credentials`, so analytics cannot be used to tell whether an account exists.
  - The backend `$set` `plan` / `premium_source` (`plan_usage_service.py:94-110`, `posthog_service.py:284-306`) is commercial status only, imported lazily, and returns None on failure.
  - `one_time_purchase_completed.duration_days` is now the server value.
  - Purchase handling (`subscription_repository.dart`, `ensureReceiptVerified`) treats any status other than `VERIFIED` as a failure: correct and safer.
  - External entries through `usage_gate.dart` are client-side cosmetics; the server gates remain authoritative.

### Deployment verdict (re-verification)

**NOT BLOCKED.** No Critical or High finding remains open: H-1 and H-2 are fixed in code and covered by tests. I did not execute those tests this round; QA's regression run is the execution check.

Conditions:

1. Backend deploy and the TestFlight build may go ahead once qa-testing's regression run is green.
2. The **production store release of the frontend** should wait for lawyer sign-off on the Art.9 consent wording (M-3, PARTIAL, Medium), or for the fallback in point 4 of the M-3 recommendation. The step-5 `frequency` / `session_count` / `custom_session_count` properties should be dropped now in any case.
3. N-1, R-1, R-2 and L-1 to L-6 are backlog items and do not block.
