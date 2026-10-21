---
name: project-notification-telemetry-semantics-2026-08-10
description: Fixed notification_opened > notification_received paradox by redefining delivery/open/banner event semantics and closing undercounting gaps in main.dart's FCM handlers
metadata:
  type: project
---

Task (2026-08-10): notification_opened (22/9u,14d) exceeded notification_received (12/5u,14d) in PostHog. Root cause was NOT double-firing -- it was that both events were undercounting from narrower code paths than their names implied.

**Emission-site map found (before fix), all in `lib/main.dart`:**
- `notification_received`: ONLY fired from `FirebaseMessaging.onMessage.listen` (foreground). No signal at all for background/terminated delivery.
- `notification_opened`: ONLY fired from `FirebaseMessaging.onMessageOpenedApp.listen` (background-resume tap). Cold-start taps (`getInitialMessage()`, lines ~899-906) stored the pending route but never logged `notification_opened` at all. A locally-shown Android system notification (`FirebaseShowNotificationHelper.showNotification` via `flutterLocalNotificationsPlugin.show`, tapped through `onDidReceiveNotificationResponse`) also never logged anything.
- In-app banners (nudge/prep-card/health-check/generic BotToast banners) fired their OWN distinct names (`notification_nudge_tapped/dismissed`, `notification_banner_tapped/dismissed`) -- health-check banner had ZERO analytics at all (not even a dismiss). No `notification_banner_shown` existed anywhere -- no impression denominator for CTR.

So `notification_opened` > `notification_received` is fully explained by: users are rarely staring at the app when a push arrives (received undercounts hard, foreground-only) but often resume the app from background to tap it later (opened captured that path fine) -- not a bug requiring dedup, a *definitional* gap.

**Fix implemented** (commit pending, dev branch, NOT pushed):
- New pure/testable module `lib/utils/notification_telemetry.dart` (mirrors the CS-06 `notification_route_resolver.dart` pattern): `notificationReceivedParams`, `notificationOpenedParams` + `NotificationOpenDedupeGuard` (message_id-keyed, one-per-process, shared across cold-start + background-resume + local-tap + banner-tap call sites), `notificationBannerParams`, `notificationBannerTapEmission` (dual notification_banner_tapped + notification_opened emission).
- `notification_received` now carries `app_state` (`foreground` | `background_or_terminated`); the background bucket is emitted from `_firebaseMessagingBackgroundHandler` via `FirebaseAnalytics.instance` directly (NO `sl<>()` DI, NO PostHog attempt -- background isolate has no service locator and iOS gives it a tiny execution budget). PLATFORM LIMIT documented in code + AnalyticsEvents doc block: reliable on Android background+terminated; on iOS only reliable while backgrounded-but-resident, NOT while fully terminated (no `content-available`/APNs Notification Service Extension configured server-side).
- `notification_opened` now carries `source` (`system_tray` | `foreground_banner`) + `app_state`, and fires from 4 sites: onMessageOpenedApp, getInitialMessage (new), local-notification tap (new), and every banner's primary-CTA tap (new, alongside the existing banner-specific event, not replacing it) -- all deduped through one shared `NotificationOpenDedupeGuard` instance.
- `notification_banner_shown/tapped/dismissed` unified across all 4 banner variants with a `notification_type` label; legacy `notification_nudge_tapped/dismissed` kept firing unchanged for backward compat with existing dashboards.
- `moment_type` (13-moment taxonomy) passed through from payload when present but **backend does not currently send it**: confirmed by reading `MindSync/app/tasks/notification_orchestrator_job.py`'s `send_fcm_to_all_user_tokens` call (~line 343) -- the FCM data dict only has `type`, `moment_id`, `route`, `deep_link_route`, never `moment_type`. Spec documented in `AnalyticsEvents`' doc block: add `"moment_type": moment.moment_type.value` to that dict. This is a backend-api/data-analytics change via integration-devops, not something flutter-mobile can add client-side.

Tests: `test/utils/notification_telemetry_test.dart` (pure logic -- dedupe guard incl. the exact cold-start+background-resume double-fire scenario, param builders, banner dual-emission). `flutter analyze` clean on all touched files (project baseline has ~134 pre-existing info/warnings elsewhere, all unrelated to these files).

See also [[settings_and_data_history]] and [[notification_cadence_v3_hardening]] for prior notification-framework work this builds on.
