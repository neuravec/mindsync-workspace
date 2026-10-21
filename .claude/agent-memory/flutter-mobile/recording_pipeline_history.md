---
name: recording-pipeline-history
description: History of session-recording foreground service, health-check voice fixes, and the v2 crash-safe pipeline un-gating
metadata:
  type: project
---

## Background Recording & Foreground Service (Mar 2026)

- `flutter_foreground_task: ^8.12.0` added (resolves to 8.17.0 with FVM Flutter 3.27.0)
- `ForegroundRecordingService` helper: `lib/services/foreground_recording_service.dart`
- Wraps `FlutterForegroundTask.init()` / `startService()` / `stopService()` with lazy init
- TaskHandler is a no-op `_RecordingTaskHandler` (no periodic work, just keeps app alive)
- `WithForegroundTask` widget wraps root in `mind_sync_app.dart` (required by plugin)
- Android: `FOREGROUND_SERVICE_MICROPHONE` permission + `<service>` declaration in AndroidManifest.xml
- iOS: `UIBackgroundModes` already had `audio` — no changes needed
- v8.x API: no `isSticky`, no `foregroundServiceTypes`, no `NotificationForegroundServiceType` (those are v9.x)
- All 3 recording cubits call `WakelockPlus.enable()` + `ForegroundRecordingService.start()` on record start, and `WakelockPlus.disable()` + `ForegroundRecordingService.stop()` on stop/close/error

## Health Check Voice Recording Fixes (Mar 2026, BUG-THC02/03)

- `DioClient.postMultipart()` accepts optional `receiveTimeout: Duration?` via `Options(receiveTimeout:...)`
- Health check voice endpoints use `receiveTimeout: const Duration(minutes: 2)` (Whisper + AI takes >30s)
- `HealthCheckFlowCubit._safeStopRecording()` — wraps WebRTC cleanup, recorder stop, and service stop each in separate try-catch to prevent cascade failures
- Recording errors use `isRecordingError: true` on the error state — shows "Write about it" button in `_ErrorView`
- `_setRecordingError` / `_setQuickRecordingError` store recovery context in `_last*` fields; `switchToText()` restores the correct state using that context
- `_formatUploadError()` produces user-friendly messages for timeout/413/network errors
- Localized open-ended prompts: `setLocalizedPrompts(List<String>)` called in `BlocProvider.create` BEFORE `init()` — requires `BuildContext` so cannot be done in constructor
- `HealthCheckFlowState.error` has `@Default(false) bool isRecordingError` — switch pattern in screen: `HealthCheckFlowError(:final message, :final isRecordingError)`

## Session Recording v2 — Un-gated as Default (Jun 2026)

- `recording_pipeline_v2` PostHog flag REMOVED from both gate sites — v2 is now unconditional default
- `record_session_cubit.dart`: `_usePipelineV2 = true` (field init, no PostHog call in `init()`); posthog_service import removed
- `splash_screen.dart`: `_checkAndOfferRecordingRecoveryDispatch` always runs v2 first, then v1 belt-and-suspenders (no flag check)
- BUG FIXED: `_startRecordingV2.onSegmentCompleted` now appends `segmentPath` to `_activeSession.segmentPaths` (was missing — only `totalBytes` was updated; kill-recovery would rely on disk scan instead of manifest)
- v1 code paths all PRESERVED — flip `_usePipelineV2 = false` to revert; `_checkAndOfferRecordingRecovery()` still runs after v2 scan
- `DebriefCaptureCubit` (voice notes) has NO dependency on `recording_pipeline_v2` — unaffected
- See also [[ios_voice_note_fallback]] for the AVAudioSession fallback logic layered on top of this pipeline
