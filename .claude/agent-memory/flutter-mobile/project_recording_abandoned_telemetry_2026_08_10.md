---
name: recording-abandoned-telemetry-2026-08-10
description: Diagnosed recording_started-vs-upload_sessions gap (10 vs 3 users, 14d); added recording_abandoned event + flow property; fixed recovery-sheet-dismiss silent-orphan bug
metadata:
  type: project
---

## Task

growth-analyst found: 10 users fired `recording_started` in 14d, only 3 had a
matching server-side `upload_sessions` row (server confirmed healthy -
4 rows/3 users, all completed). Zero `recording_upload_failed` events ever
fired. Asked to map every client-side exit branch and make the gap
permanently diagnosable.

## Root cause (mostly apples-to-oranges, not silent loss)

`recording_started` fires from TWO independently-designed pipelines that
share the event name:
- `RecordSessionCubit` (session-recording flow) - chunked
  `POST /upload/initiate` → `upload_sessions` row. This is the ONLY flow
  that is supposed to create that row.
- `DebriefCaptureCubit` (debrief/prep/between-session voice notes) -
  `POST /audio-v2/transcribe` (Whisper). NEVER creates an `upload_sessions`
  row, by design - always has and always will.

Both already tagged `recording_kind` (session/debrief/prep/between) and
`pipeline` (v2/voice), so the split was reconstructable but not a single
filter. Added `AnalyticsEvents.recordingFlowParam` = `'flow'` with values
`session_recording` | `voice_note` to every `recording_*` event on both
cubits + `background_upload_cubit.dart` so growth-analyst's funnel can
`WHERE flow = 'session_recording'` and get an apples-to-apples number.

## New event: `recording_abandoned`

`AnalyticsEvents.recordingAbandoned` = `'recording_abandoned'`, fired
ADDITIONALLY alongside the existing `recording_stopped.stop_outcome`
taxonomy (not a replacement). Closed-vocab `reason`: `user_discarded` |
`too_short` | `permission_denied` | `error` | `app_killed_recovery`. Helper:
`AnalyticsEvents.logRecordingAbandoned({reason, flow, recordingKind, detail})`.

Goal per flow: `started ≈ uploaded(recording_saved) + abandoned + failed
(recording_processing_failed)`.

Fired at every branch that previously had ZERO telemetry:
- `RecordSessionCubit.startRecording()` mic-permission denial
- `RecordSessionCubit.discardRecording()` (guarded on `_recordingPath !=
  null || _v2SessionId != null` - no-op case must NOT fire)
- `RecordSessionCubit._stopRecordingV2()` WAV-assembly try/catch (had zero
  analytics before)
- `DebriefCaptureCubit.startRecording()` mic-permission denial
- `DebriefCaptureCubit._resetAfterDiscard()` (discardTranscript/
  deleteRecording/recordAgain - guarded on `_recordingPath != null`)
- `DebriefCaptureCubit.close()` when `state is DebriefCaptureRecording &&
  !_isStopping` (back-gesture mid-recording)
- `splash_screen.dart` `_checkAndOfferRecordingRecoveryV2`'s `case null:`
  (recovery sheet dismissed without a choice - see bug below)

Also fired (duplicate-but-useful) at the too-short branches that already had
`recording_stopped.stop_outcome=too_short`, so `recording_abandoned` alone
answers "why didn't this convert" without joining events.

## Real bugs found and fixed (both contained, both in scope)

1. **v2 crash-recovery bottom sheet could be dismissed with no action**
   (`_showV2RecoverySheet` in `splash_screen.dart` used default
   `isDismissible: true`). The session then sits orphaned in the manifest
   forever with zero signal - most plausible client-side explanation for a
   `recording_started` with no matching upload attempt. Fixed: added
   `isDismissible: false, enableDrag: false` (matches the v1 recovery
   `AlertDialog`'s existing `barrierDismissible: false`). Kept the
   `recording_abandoned(app_killed_recovery)` event at `case null:` as
   belt-and-suspenders.

2. **Mid-recording "Stop recording? → Discard" dialog didn't actually
   discard.** `record_session_flow.dart`'s `_handleClose` for
   `RecordSessionRecording` just popped the screen on Discard - the
   in-progress v2 session (PCM segments + manifest entry) survived, so the
   next app launch's recovery scan re-offered a recording the user
   explicitly said to discard. Fixed: now calls
   `cubit.discardRecording()` before exiting, matching the "Yieks!" error
   screen's discard/x exits exactly (same method, same guarantees). Capture
   the cubit via `context.read()` BEFORE `showDialog` - `_safeExit` may pop
   the screen before the dialog resolves.

## `retryUpload()` had ZERO analytics on any branch

Found while mapping: `RecordSessionCubit.retryUpload()` (used by both the
Yieks error screen's Retry and the generic error screen's Try Again) never
fired any event - a retry that failed again was completely invisible. Added
`recordingUploadStarted` at entry and `recordingProcessingFailed` (via new
`_logRetryUploadFailed` helper, `retry: true` tag) in every catch branch
(v2 chunked, v2→single-shot GCS fallback, legacy v1 single-shot).

## `recording_upload_failed` string literal - why it read zero forever

`RecordSessionCubit`'s v1 code path (raw string `'recording_upload_failed'`,
NOT the `AnalyticsEvents.recordingProcessingFailed` constant) is the only
place that event name exists. `_usePipelineV2 = true` unconditionally, so v1
is dead code - that event can never fire. Left as-is (v1 is legacy/unused,
out of scope to touch); the LIVE failure signal is
`AnalyticsEvents.recordingProcessingFailed` (`'recording_processing_failed'`),
which already fires at every real v2 upload failure branch except the one
gap closed here: `BackgroundUploadCubit._resolveWavPath` returning null
(no valid WAV/PCM segments) previously emitted `BackgroundUploadFailed`
with zero analytics - now fires `recordingProcessingFailed(error_type=
file_not_found, stage=upload, source=background_upload)`.

## Testing patterns confirmed reusable

- All existing recording-pipeline test files assert via `captureAny`/
  `any(named:...)`, never exact-map equality - adding new properties to
  event params is always safe, no existing test breaks.
- `record_session_discard_test.dart` and other cubit tests never register
  `PostHogService` in `sl` - `AnalyticsEvents.logEvent`'s try/catch around
  `sl<PostHogService>().capture(...)` swallows the missing-registration
  error silently, so adding new `logEvent`/`logRecordingAbandoned` calls to
  cubit methods never breaks tests that don't care about analytics.
- To unit-test mic-permission-denied paths without touching
  `CrashSafeRecorder`: mock the `record` plugin's method channel
  (`MethodChannel('com.llfbandit.record/messages')`, method
  `'hasPermission'` → `false`). The permission check in both
  `RecordSessionCubit.startRecording()` and
  `DebriefCaptureCubit.startRecording()` returns BEFORE touching
  `CrashSafeRecorder`/`AudioRecorder.start()`, so no other native mocking
  needed.
- `test/screens/fab_flows/record_session_appbar_close_test.dart` hangs
  under `flutter test` in this environment (pre-existing, see
  [[patterns]] Important Gotchas) - confirmed again 2026-08-10, unrelated to
  this change (only the `RecordSessionRecording` branch of `_handleClose`
  was touched, not the `RecordSessionError` branch that file exercises).
  Do not run it standalone without a bounded background timeout.

## Files changed

- `lib/core/analytics/analytics_events.dart` - `recording_abandoned` event +
  `flow` property + closed-vocab reasons + `logRecordingAbandoned()` helper
- `lib/screens/fab_flows/cubit/record_session_cubit.dart` - abandon events,
  `flow` tagging, WAV-assembly-failure telemetry, `retryUpload()` telemetry
- `lib/screens/fab_flows/record_session_flow.dart` - mid-recording Discard
  now calls `discardRecording()`
- `lib/screens/splash/splash_screen.dart` - recovery sheet non-dismissible +
  `case null:` abandon event
- `lib/services/recording_pipeline_v2/background_upload_cubit.dart` -
  file-missing failure telemetry + `flow` tagging
- `lib/screens/debrief_capture/cubit/debrief_capture_cubit.dart` - abandon
  events (permission/too-short/no-audio/discard/close-while-recording) +
  `flow` tagging
- New test: `test/screens/fab_flows/record_session_abandon_analytics_test.dart`
- Extended: `test/services/recording_pipeline_v2/background_upload_analytics_test.dart`,
  `test/screens/debrief_capture/debrief_capture_cubit_test.dart`

Committed locally on `dev` (f2fa8f4), NOT pushed, per task instructions.
