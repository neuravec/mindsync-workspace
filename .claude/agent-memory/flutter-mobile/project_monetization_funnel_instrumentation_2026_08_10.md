---
name: project-monetization-funnel-instrumentation-2026-08-10
description: paywall_shown/restore/failure_reason PostHog instrumentation (2026-08-10) — root causes, taxonomy, InAppPurchase test-mocking recipe
metadata:
  type: project
---

Task: make the paywall -> purchase funnel measurable (growth-analyst had zero
top-of-funnel data). Commit: `feat(analytics): monetization funnel
instrumentation` on mindsync-frontend `dev` (58d097b, on top of ec05973),
COMMITTED locally, NOT pushed.

## Root causes found (both were silent dead code, not missing features)

- `paywall_shown` had a `trackPaywallShown()` method already defined on
  `SubscriptionCubit` (lib/screens/subscription/cubit/subscription_cubit.dart)
  but it was never called from anywhere — dead code since whenever it was
  added. Replaced with `configurePaywallContext()` (call right after cubit
  construction, before `loadSubscriptionsProducts()`) + a guarded
  `_trackPaywallShownOnce()` fired once, inside `loadSubscriptionsProducts()`
  after products load, suppressed when `isPremiumAtOpen` (those users land on
  PremiumView, never the real paywall/SubscriptionBody).
- `subscription_restore_started/completed/failed` were correctly wired
  end-to-end in `SubscriptionCubit.restorePurchases()` — the actual bug was
  in `lib/screens/subscription/widgets/subscription_bottom_info.dart`: the
  "Restore" text's `GestureDetector` had `onTap: () {}` (literal no-op).
  Nothing ever called `restorePurchases()`. One-line fix:
  `context.read<SubscriptionCubit>().restorePurchases()`.
- **Lesson**: when a PostHog event is "defined but never fires," grep for
  the emission call, not just the constant — the emitting *method* can
  itself be uncalled, or the trigger UI can be a dead-letter tap handler.

## trigger_feature taxonomy (AnalyticsEvents, `lib/core/analytics/analytics_events.dart`)

Closed vocabulary constants: `triggerFeatureSettings`, `triggerFeatureDrawerMenu`,
`triggerFeatureTrialEndedPopup`, `triggerFeatureOnboarding` (unused so far —
no onboarding->subscription push exists), `triggerFeatureDeepLink` (unused —
no notification deep-links to /subscription today), `triggerFeatureUnknown`
(default fallback), and `premiumGateTrigger(feature)` -> `premium_gate_<feature>`
for locked-feature entry points. Routed via a new `?trigger=` query param on
`/subscription` (`MsRoutes.subscriptionRouteWithTrigger(trigger)` /
`parseSubscriptionTriggerParam`), same pattern as the existing `?section=`
param on `/settings`. All 9 `context.push(.../subscription)` call sites
across the app now tag a trigger_feature — see the commit diff for the
mapping (drawer_menu, premium_banner=settings, trial_popup_manager=trial_ended_popup,
record_session_flow=premium_gate_session_recording,
reflect_tab_screen×2 + reflect_usage_indicator=premium_gate_reflect_messages/
premium_gate_reflect_voice, monthly_audit_widget + therapy_tab_screen=premium_gate_monthly_audit).

## failure_reason taxonomy on subscription_purchase_failed

`user_cancelled | store_error | pending | unknown` — classified in
`SubscriptionCubit._classifyFailureReason(IAPError?)` by substring-matching
`code`/`message` for "cancel" (IAPError.code strings are NOT standardized
across platforms/plugin versions, so exact-match would silently miss
cases). Added a previously-missing `PurchaseStatus.pending` branch in
`_listenPurchaseStreamOnData` (fell through to nothing before — no event,
no state change; now emits `subscription_purchase_failed` with
`failure_reason: pending` so stuck purchases are visible in the funnel).

## Trial start/end — NOT instrumented client-side (by design)

Confirmed trial detection is 100% server-side: `UserInfo.hadTrial` comes
from the backend (`had_trial` JSON field), and
`SubscriptionRepository.markAsSubscribed()` fire-and-forgets the receipt to
`/users/...` without reading back any trial flag. The `in_app_purchase`
package here has no introductory-price/trial-period parsing wired up at
all. Per the task's own instruction ("if trials are entirely server-detected
... do not fake it client-side"), no `trial_started`/`trial_ended` was
added — this needs a backend/data-analytics spec instead (derive from
receipt verification, emit server-side like `subscription_purchase_completed`
already is).

## InAppPurchase unit-testing recipe (reusable — this was the hard part)

`InAppPurchase.instance.purchaseStream` forwards directly to
`InAppPurchasePlatform.instance.purchaseStream`
(`in_app_purchase-3.2.3/lib/in_app_purchase.dart`). To drive the real
purchase-stream-consuming code path in a unit test (restore/cancel/pending/
error) without touching platform channels:

1. Add `in_app_purchase_platform_interface` + `plugin_platform_interface` as
   **direct dev_dependencies** in pubspec.yaml (already transitive via
   `in_app_purchase`, but `depend_on_referenced_packages` lint wants them
   explicit — `flutter pub get` after adding, no version conflicts).
2. `class FakeInAppPurchasePlatform extends Mock with
   MockPlatformInterfaceMixin implements InAppPurchasePlatform {}` — the
   mixin bypasses `PlatformInterface.verify`'s private token check, the
   standard way to fake plugin-platform-interface classes.
3. Stub `fakePlatform.purchaseStream` to return a
   `StreamController<List<PurchaseDetails>>.broadcast().stream` you control,
   and stub `completePurchase(any())` (needed whenever a test purchase has
   `pendingCompletePurchase: true`, e.g. simulating a restored/purchased
   result).
4. **Gotcha**: `InAppPurchase.instance` (the *facade*, not
   `InAppPurchasePlatform`) lazily self-registers a REAL platform
   (`InAppPurchaseAndroidPlatform.registerPlatform()`) the first time it's
   ever accessed in the whole test process — this OVERWRITES whatever you
   set on `InAppPurchasePlatform.instance` in `setUp()`, and fires an
   unawaited real billing-connect attempt that rejects with
   `PlatformException` (misattributed as "test failed after it had already
   completed" on whichever test happens to run first). Fix: in `setUpAll()`,
   deliberately warm up `InAppPurchase.instance` once inside
   `runZonedGuarded(...)` (swallowing the expected `PlatformException`)
   BEFORE any test's `setUp()` installs the fake — `InAppPurchase._instance`
   is then cached and `registerPlatform()` never runs again, so your fake
   sticks for every subsequent test.
5. `ProductDetails`/`PurchaseDetails` both need `registerFallbackValue(...)`
   in `setUpAll()` if you use `any()`/`captureAny()` on them anywhere
   (mocktail requirement for non-primitive types).
6. **Mocktail gotcha (general, not IAP-specific)**: a single recorded
   invocation can only satisfy ONE `verify()` call — calling
   `verify(...).called(1)` and then separately `verify(...).captured` for
   the *same* logical call fails the second one ("No matching calls" even
   though the log shows `[VERIFIED]`). Combine count-assertion and
   capture into one `verify(...).captured` + `expect(captured, hasLength(n))`.

Full working example:
`mindsync_app/test/screens/subscription/cubit/subscription_cubit_analytics_test.dart`.
