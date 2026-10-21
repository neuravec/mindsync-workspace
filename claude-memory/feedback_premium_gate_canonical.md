---
name: Premium gating canonical field
description: Use UserSubscription.is_active for all premium gates — subscription_type is legacy and must never be checked
type: feedback
originSessionId: 02c58bd2-f3cb-477d-a16a-520e2aa01d77
---
Premium gating MUST use `UserSubscription.is_active` as the sole source of truth. The `subscription_type` column (SubEnum BASIC/PREMIUM) is a LEGACY field — it is still written at registration / promo redemption / receipt verification but MUST NOT be read in any gate, analytics label, or marketing SQL.

Canonical helper: `is_user_premium(db, user_id)` in `app/api/v1/endpoints/_therapy_helpers.py`. It checks only `is_active == True`. No need to add `end_date > now()` — the hourly RQ cron `deactivate_expired_subscriptions()` in `subscription_service.py` sets `is_active=False` when `end_date` passes (max ~1h staleness).

**Why:** User discovered a promo-trial tester got `is_active=True`, dates ok, but `subscription_type=BASIC` (promo redemption only writes `is_active` + dates, which is intentional — `subscription_type` is legacy). Reflect's local `_is_premium()` was wrongly checking both, so trialers were blocked. Fixed 2026-04-20 in reflect.py, posthog_service.py, user_loops_maintenance.py, tasks/loops_sync.py.

**How to apply:**
- Any new premium gate → import and call `is_user_premium(db, user_id)` — do not roll your own check
- Any new analytics/marketing SQL → filter on `is_active` only
- When reviewing code, flag any `subscription_type == PREMIUM` / `SubEnum.PREMIUM` comparison outside of registration/receipt writes as a bug
- Writes to `subscription_type` in register/promo/receipt code can stay — legacy field, harmless
