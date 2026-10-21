---
name: posthog-integration
description: PostHog Flutter integration phases 2/3/5 — init, identity chain, dual-send analytics, and frontend event instrumentation
metadata:
  type: project
---

## Phase 2 — Foundation (DONE, Apr 2026)

- `posthog_flutter: ^5.0.0` added to pubspec.yaml
- AUTO_INIT=false: AndroidManifest.xml `<meta-data>` + Info.plist `<key>com.posthog.posthog.AUTO_INIT</key><false/>` (manual init required for session replay)
- `PostHogService`: `lib/core/analytics/posthog_service.dart` — plain singleton (not Cubit), `registerSingleton<PostHogService>()` BEFORE FirebaseAnalytics in service_locator.dart
- Config: `PostHogConfig(apiKey)` with host `https://eu.i.posthog.com`, `sessionReplay=true`, `PostHogSessionReplayConfig()` with `maskAllTexts=true` + `maskAllImages=true`
- Init: `sl<PostHogService>().init()` in `main()` after `setupAppLocator()` + `setAnalyticsCollectionEnabled()`; empty API key = no-op (safe for CI builds)
- `PostHogWidget` wraps `WithForegroundTask` as outermost widget in `mind_sync_app.dart`
- API key via `--dart-define=POSTHOG_API_KEY=xxx` — never hardcoded
- CRITICAL: `maskAllTexts=true` + `maskAllImages=true` MUST stay — mental health privacy requirement, never relax

## Phase 3 — Identity Chain & Dual-Send (DONE, Apr 2026)

- `X-PostHog-Distinct-ID` header added in `DioClient` `onRequest` interceptor (async await, inside try/catch)
- `AnalyticsEvents.logEvent()`: PostHog fires FIRST (even in debug), Firebase skipped in debug unless `forceLog`
- `AnalyticsEvents.logError()`: PostHog gets only `error_type` (runtimeType) + optional `screen_name` — NEVER message/stack
- `PosthogObserver()` added to `MsRoutes.router` observers list (import from `posthog_flutter`)
- `AuthCubit._identifyPostHog(User, String authProvider)` — private helper, called after all 3 login paths (email/google/apple)
- `AnalyticsEvents.logEvent(name: 'user_logged_in', parameters: {auth_provider, platform})` after each login
- `AnalyticsEvents.logEvent(name: 'user_logged_out')` + `sl<PostHogService>().reset()` BEFORE Firebase signOut in `MainPageCubit.signOut()` and `SettingsCubit.deleteAccount()` (`AccountCubit.deleteAccount` removed May 2026 as dead code)
- `_identifyPostHog` uses `sl<LocaleCubit>().state.languageCode` for language property
- CRITICAL: Never put therapy text, notes, symptom names, or emotional data in event properties
- `logError` signature extended: `logError(Object error, StackTrace? stackTrace, {String? screenName})` — backward compatible

## Phase 5 — Frontend Event Instrumentation (DONE, Apr 2026)

- ~55 PostHog events added across cubits/widgets using `AnalyticsEvents.logEvent()` (dual-send)
- New helper methods added to cubits (call from UI): `SymptomTrackingCubit.trackSuggestionShown(id)`, `GoalTrackingCubit.trackGoalViewed(id)`, `SnapshotsCubit.trackSnapshotViewed(period)`, `StatsTabCubit.trackTherapyTrackingViewed(signal)`, `StatsTabCubit.trackChartViewed(chartType, period)`, `TherapyTabCubit.trackSummaryViewed(type, id)`, `TherapyTabCubit.trackMonthlyAuditViewed(id)`, `CharacterTabCubit.trackBioViewed()`, `HealthCheckFlowCubit.dismissPrompt()`, `SubscriptionCubit.trackPaywallShown(triggerFeature, gateType)`
- Onboarding: step_viewed/step_completed use `_stepStartTimes` map for duration tracking; `_onboardingStartTime` for total duration
- `debrief_started` / `prep_card_started` / `between_session_started` all fire in `loadGuidingQuestions()` of `DebriefCaptureCubit`
- `tab_switched` only fires when index actually changes (guards against same-tab re-press)
- `notification_opened` in `main.dart` now includes `deep_link_route` property
- `content_shared` added to `CardShareUtil._trackShare()` before the existing `logShare()` call
- `realization_viewed` fires in `RealizationDetailWidget.initState()` — only non-cubit event
- `recording_upload_started` buckets: short <600s, medium 600-1800s, long >1800s
- `flutter analyze`: 0 errors (60 pre-existing infos/warnings unchanged)

See also [[recording_funnel_analytics]] for the Jun 2026 recording-specific event additions.
