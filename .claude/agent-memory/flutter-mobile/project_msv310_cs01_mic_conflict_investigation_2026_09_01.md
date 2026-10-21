---
name: project-msv310-cs01-mic-conflict-investigation-2026-09-01
description: MSV3.10 CS-01 investigation-only report on telehealth call + session recording mic conflict ([użytkowniczka V], iPhone) - two-part hypothesis, backend gap confirmed by code read
metadata:
  type: project
---

Investigation-only task (no code changes). Report delivered to
`Business_requirements/MS_3/v3.10/CS-01_mic_conflict_investigation.md`. [użytkowniczka V]
(iPhone) ran a telehealth call + MindSync session recording ("Droga
terapeutyczna") simultaneously; recording came out "too garbled," no
transcript produced.

**Two-part hypothesis (device verification still needed for part A):**
- Part A (medium-high confidence): iOS AVAudioSession contention between
  MindSync's own `.playAndRecord`/`.spokenAudio` session (no `mixWithOthers`)
  and the telehealth app's competing non-mixable session. Either clean
  interruption-cycling (stitched/glitchy segments at pause/resume boundaries)
  or direct hardware/format contention with non-CallKit telehealth apps
  (genuine distortion). Android is expected to behave differently per its
  documented "silence the loser" concurrent-capture policy (since Android 10)
  vs iOS's "deactivate the loser" interruption model - untested, field report
  is iPhone-only.
- Part B (HIGH confidence, code-confirmed not speculative): `MindSync/app/tasks/session_recording.py`
  `process_session_recording` (the AssemblyAI path every session recording
  uses - never the Whisper short-form fallback, see `stt_service.py` header
  doc) has NO empty/near-empty transcript_text guard before marking
  COMPLETED (lines ~429-461). The Whisper fallback path in the SAME file
  (`process_session_recording_whisper`, lines ~774-775) DOES have this guard
  (`raise ValueError("Whisper returned empty transcription")` -> FAILED). This
  asymmetry alone explains "no transcription was produced with no error" -
  independent of whatever causes the audio degradation. Flagged as the
  cheapest, highest-value, lowest-risk fix (Option A in the report) but
  requires backend-api (flutter-mobile does not own MindSync/app/).

**Key internal precedent found (not previously connected to session
recording in memory):** `health_check_flow_cubit.dart:290-307` documents a
REAL, ALREADY-FIXED bug of the exact same class inside this codebase: CS-14,
where Health Check's open-ended voice flow ran a `record`-package
AudioRecorder AND a parallel flutter_webrtc getUserMedia session
concurrently (for a live-preview transcript box), and the in-code doc states
plainly this "fight[s] over the same hardware microphone/audio session on
both iOS ... and Android ..., degrading whichever one loses to near-silence"
- Whisper then hallucinated plausible text on the near-silent input rather
than returning empty. Fix was to remove the second in-process capture
entirely (`_recorder` is now sole mic owner). Worth checking for this pattern
first whenever a "recording sounds wrong" bug involves ANY concurrent
audio/mic usage, in-process or cross-app.

**Confirmed technical facts (useful for any future recording-quality work):**
- Session-recording iOS AVAudioSession config: category `.playAndRecord`,
  mode `.spokenAudio`, options `allowBluetooth | defaultToSpeaker |
  duckOthers` - NO `mixWithOthers`, set via `audio_session` package in
  `_configureIosAudioSessionForBackground()`, `record_session_cubit.dart:274-334`.
  Identical config confirmed in `voice_quick_capture_cubit.dart:45-51` and
  `debrief_capture_cubit.dart:403-410` (all three capture cubits consistent).
- `CrashSafeRecorder` (v2 pipeline, current default) uses raw PCM 16-bit mono
  16kHz via `record` package's `startStream`; does NOT set
  `iosConfig.manageAudioSession` itself - relies entirely on the cubit's
  separate `audio_session` configuration call before recording starts. This
  matches (does not violate) the proven pattern in
  [[feedback_record_package_ios_audio_session]].
- `interruptionEventStream` handling already exists and is fairly mature
  (pause on begin, v2 always auto-resumes on end regardless of type,
  `record_session_cubit.dart:292-318`) - but device-change/route-change
  listener only LOGS, never reacts (`record_session_cubit.dart:320-333`).
  No pre-flight check for "another app already holds the mic" before
  starting a recording.
- `recording_placementTip` l10n string ("Place your phone where it can hear
  clearly...") confirms the feature's own onboarding copy describes
  room-mic capture of an in-person conversation, NOT capture of a call the
  phone itself is making - worth flagging to product that "record my
  telehealth call" is a real but not-originally-designed-for use pattern.
- Bluetooth HFP (Hands-Free Profile) caps audio at 8kHz mono narrowband
  unless the headset supports mSBC/Wideband Speech (HFP 1.6+) - a real,
  independent quality ceiling if the telehealth call is BT-routed, on top of
  whatever the two-app contention does.

**Recommendation given:** ship backend empty-transcript guard (Option A)
first + frontend pre-flight "another app may be using your mic" warning
(Option B); hold live in-recording contention-detection banner (Option C)
until the 4 device experiments listed in the report (non-CallKit telehealth
app vs CallKit control, iOS vs Android, with/without Bluetooth) are actually
run - explicitly warned against building C's heuristic on an unverified
assumption, citing CS-14 as the precedent for what happens when you guess.
Rejected forcing `mixWithOthers`/concurrent full-quality capture as not
technically viable on either platform.

See also [[recording_pipeline_history]], [[ios_voice_note_fallback]].
