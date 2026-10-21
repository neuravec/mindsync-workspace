---
name: ios-voice-note-fallback
description: iOS voice note falsely shows "too short" when WebRTC wins AVAudioSession — fix is transcript fallback in DebriefCaptureCubit
metadata:
  type: feedback
---

On iOS, `WebRTC getUserMedia` wins the shared `AVAudioSession`, starving the `record` package. The M4A stays ~28 bytes (bare ftyp header). The live transcript IS the content.

**Fix (2026-06-22):** `decideStopOutcome` now takes `hasTranscript: bool`. Priority order:
1. `path == null || size == 0` → `noAudio`
2. `size >= kMinUsefulBytes (2048)` → `upload` (Android + iOS when not contested)
3. `size < kMinUsefulBytes && hasTranscript` → `transcriptFallback` (iOS fix)
4. `size < kMinUsefulBytes && !hasTranscript` → `tooShort`

`transcriptFallback` case in `stopAndSubmitRecording`: settles transcription (waits `_kStopSettleMs=1200ms`), then calls `_submitTextContent(finalTranscript)` — same as manual text entry.

`submitText()` now delegates to shared `_submitTextContent()` (deduplication). MomentsCubit `onTrigger` calls preserved for debrief and betweenSession in both paths.

`hasTranscript` threshold: `_currentTranscript.trim().length >= 5` chars.

**Why:** Old code used M4A size alone → every iOS recording was "too short". Regression from change that moved from transcript-first to file-size-first without handling iOS contention.

**How to apply:** If any future recording flow on iOS returns "nothing captured" but transcript was visible, check `decideStopOutcome` call site passes `hasTranscript`. Never gate on M4A size alone when WebRTC is running concurrently.
