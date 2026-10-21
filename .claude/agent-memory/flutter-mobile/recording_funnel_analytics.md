---
name: recording-funnel-analytics
description: PostHog recording funnel events — 8 client-side events added Jun 2026 to make v2 pipeline observable
metadata:
  type: project
---

## What was added (Jun 2026)

8 client-side PostHog events that close the analytics gap in the recording pipeline:

| Event | Where emitted |
|-------|--------------|
| `recording_started` | `RecordSessionCubit._startRecordingV2()`, `resumeSessionV2()`, `DebriefCaptureCubit.startRecording()` |
| `recording_stopped` | `RecordSessionCubit._stopRecordingV2()` (3 branches), `DebriefCaptureCubit.stopAndSubmitRecording()` (4 branches) |
| `recording_upload_started` | `RecordSessionCubit._stopRecordingV2()` + `BackgroundUploadCubit.processEntry()` |
| `recording_chunk_upload_failed` | Via `onChunkFailed` callback on `ChunkedUploadManager.uploadFile()` |
| `recording_chunked_upload_completed` | `RecordSessionCubit._stopRecordingV2()` + `BackgroundUploadCubit.processEntry()` |
| `recording_saved` | `RecordSessionCubit._pollOnce()` on completed + `BackgroundUploadCubit` + `DebriefCaptureCubit._uploadRecording()/_submitTextContent()` |
| `recording_processing_failed` | Upload/poll failure branches in all three cubits |
| `recording_recovered` | 4 branches in `splash_screen.dart` `_checkAndOfferRecordingRecoveryV2()` |

## Key design decisions

- `recording_kind`: `'session'|'debrief'|'prep'|'between'` — differentiates pipelines
- `duration_bucket`: computed client-side via `AnalyticsEvents.recordingDurationBucket(seconds)` — `'<10s'|'10-60s'|'1-5m'|'5-20m'|'20m+'`
- `stop_outcome`: `'upload'|'too_short'|'cancelled'` — maps to what happened when user tapped Stop
- `recovery_outcome`: `'resumed'|'recovered_saved'|'discarded'`
- `_v2EffectiveDurationSeconds` field in `RecordSessionCubit` bridges `_stopRecordingV2()` (where duration is computed) and `_pollOnce()` (where `recording_saved` is emitted asynchronously later)
- `onChunkFailed` is optional callback on `ChunkedUploadManager.uploadFile()` — analytics seam, never affects upload behavior; fires on transient AND permanent failures (NOT on 409 gap fills)
- WAV duration approximation in `BackgroundUploadCubit`: `(fileBytes - 44) ~/ 32000` (44-byte header, 16kHz/mono/16-bit PCM = 32000 B/s)
- Backend owns `recording_processing_started/completed/failed` server-side — client does NOT duplicate these

## Files changed

- `lib/core/analytics/analytics_events.dart` — 8 constants + `recordingDurationBucket()` helper
- `lib/services/recording_pipeline_v2/chunked_upload_manager.dart` — `onChunkFailed` optional param + `chunkIndex` counter
- `lib/screens/fab_flows/cubit/record_session_cubit.dart` — `_v2EffectiveDurationSeconds` field + events at 6 sites
- `lib/services/recording_pipeline_v2/background_upload_cubit.dart` — import + events at 4 sites
- `lib/screens/splash/splash_screen.dart` — import + `recording_recovered` at 4 branches
- `lib/screens/debrief_capture/cubit/debrief_capture_cubit.dart` — `_recordingKind` getter + events at ~8 sites

## Test files

- `test/screens/fab_flows/record_session_analytics_test.dart` — 5 tests (poll events, no-duplicate guard)
- `test/services/recording_pipeline_v2/background_upload_analytics_test.dart` — 6 tests (full upload lifecycle)
- `test/services/recording_pipeline_v2/background_upload_cubit_test.dart` — UPDATED: all `uploadFile` stubs now include `onChunkFailed: any(named: 'onChunkFailed')` — required because new optional param is passed in actual calls (mocktail won't match stubs that omit it)

## Gotcha: mocktail stub matching

When adding an optional named parameter to a method that's already mocked, ALL existing stubs must be updated to include the new parameter (even with `any(named: ...)`) — otherwise mocktail won't match the actual call and stubs silently fail.

## Gotcha: `verify().captured` vs `verify().called`

- `.captured` is only populated if `captureAny(named: ...)` is used in the matcher (not `any(named: ...)`)
- `.called(N)` works with `any(named: ...)` — use this for simple count verification
- Never call `verify()` inside a mock's `thenAnswer` callback — ordering tests should use flag variables set during mock execution
