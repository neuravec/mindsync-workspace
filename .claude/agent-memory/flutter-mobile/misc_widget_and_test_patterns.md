---
name: misc-widget-and-test-patterns
description: Chat redesign widget patterns, realtime session config model, reflect-tab test patterns, and misc engineering gotchas
metadata:
  type: project
---

## Chat Redesign Widget Patterns (May 2026)

- `ReflectChatBubble`: `SingleTickerProviderStateMixin`, `FadeTransition` + `SlideTransition` entry (300ms). Agent: white bg, 4px deepOcean left border, BorderRadius.circular(16). User: aquaBreeze 0.7 alpha, no border.
- `ReflectThinkingIndicator`: 3 `AnimationController`s (500ms, `repeat(reverse:true)`), stagger via `Future.delayed` in initState. No text — dots only. Semantics liveRegion wraps row.
- `ReflectStarterChips`: `Column` (NOT Wrap), `AnimatedOpacity`+`IgnorePointer` for `isVisible`, per-chip `FadeTransition`+`SlideTransition` stagger via `Timer` list. `CustomPainter` dashed border via `path.computeMetrics()` — no package needed.
- `ReflectChatInput`: outer `AnimatedContainer` uses `Border.all(uniform color)` only — mixing border colors with borderRadius triggers Flutter assertion. Accent bar = inner `Positioned AnimatedContainer` (height 0↔3). `onTypingChanged` debounced 200ms via `Timer`.
- Flutter SDK for this project: `C:\Users\mikol\flutter\bin\flutter.bat` (system 3.41.1) — NOT FVM 3.27 for running tests.

## Realtime Session Config (May 2026)

- `RealtimeSessionModel` + `VoiceSessionConfig` at `lib/api/models/audio/realtime_session_model.dart`
- `AudioV2Manager.getRealtimeSession()` returns `RealtimeSessionModel` (was `Map<String,dynamic>`)
- `SessionData` no longer has `model: String`; has `realtimeSession: RealtimeSessionModel` + `String get model` convenience getter
- `AudioChatCubit.initialize()` now takes `required RealtimeSessionModel session` (named params) — no more `openAiKey`/`selectedVoice`/`model` positional args
- `_sendSessionUpdate()` delegates to static `buildSessionUpdatePayload()` — `reasoning` key omitted when null (older models reject it); fallback to `_kFallbackClientSessionConfig` when `clientSessionConfig` is null
- GoRouter `audioChatRoute` extra is now `Map<String,dynamic>` with `'session': RealtimeSessionModel` (was flat string map)
- `ReflectChatCubit.getSessionData()` returns `({RealtimeSessionModel session, String systemMessage})?` (Dart 3 record) — was `Map<String,dynamic>?`
- `clientSessionConfig` is nullable (`VoiceSessionConfig?`) — backend rollback/null returns gracefully use hardcoded fallback instead of crashing with TypeError
- `AppCubit` is `registerLazySingleton` (NOT `registerFactory`) — factory was silently returning fresh instances (always `Voice.marin`) to every caller
- Startup race for voice selection: both `ConversationsManager.getSessionData()` and `ReflectChatCubit.getSessionData()` defensively `await sl<AppCubit>().getSelectedVoice()` before reading `selectedVoice` — idempotent, fast, eliminates race with `MainPageScreen.initState`
- `AudioChatCubit.buildSessionUpdatePayload()` is `@visibleForTesting static` — pure function, no GetIt, testable without WebRTC

## Test Patterns (reflect_tab, May 2026)

- Widgets using `S.of(context)` need full localizations delegates in test `_wrap()`: `S.delegate + GlobalMaterialLocalizations + GlobalWidgetsLocalizations + GlobalCupertinoLocalizations`
- Continuous `repeat()` animations → never `pumpAndSettle`. Use fixed pump durations: `pump(Duration.zero)` then `pump(350ms)` then `pump(250ms)` (same root cause as the Moments-screen gotcha in [[moments_system]] / [[notification_cadence_v3_hardening]])
- `tester.tap(IconButton)` crashes with ink sparkle shader in tests — use `tester.testTextInput.receiveAction(TextInputAction.done)` to submit text
- Scope `find.byType(CustomPaint)` to `find.descendant(of: find.byType(MyWidget), ...)` — Material scaffold adds its own CustomPaints
- `BoxConstraints.minHeight` is non-nullable `double` — drop `?? 0` fallback or analyzer warns `dead_null_aware_expression`
