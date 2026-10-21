# CS-01 Investigation: Microphone Conflict Between Telehealth Call and Session Recording

**Type:** Investigation only. No production code, audio configuration, or UI was changed to produce this report.
**Reporter case:** [użytkowniczka V], iPhone. Ran a telehealth call and a MindSync "Droga terapeutyczna" session recording on the same phone at the same time. Result: recording came out "too garbled," no transcription was produced.
**Author:** flutter-mobile agent, read-only investigation.
**Date:** 2026-09-01.

---

## 1. Root cause

There is no single, device-confirmed root cause yet. Based on a full code trace plus OS documentation research, the leading candidate is a **two-part failure** and both parts are independently supported by evidence already in this codebase or in Apple/Android documentation. Confidence level is stated per part.

### Part A: iOS microphone/audio-session contention between two apps (confidence: medium-high, needs device verification)

MindSync's session recording configures its own `AVAudioSession` (category `.playAndRecord`, mode `.spokenAudio`, options `allowBluetooth | defaultToSpeaker | duckOthers`) via the `audio_session` package immediately before it starts capturing (`RecordSessionCubit._configureIosAudioSessionForBackground`, `mindsync-frontend/mindsync_app/lib/screens/fab_flows/cubit/record_session_cubit.dart:274-334`). A telehealth call app running at the same time also needs an active, non-mixable audio session of its own (typically also `.playAndRecord`, often mode `.voiceChat` with system voice-processing enabled if it is a VoIP/video app).

Apple's own documentation is explicit that when a competing app activates a non-mixable session, the other app's session is interrupted and deactivated ("Interruptions happen when a competing audio session from an app is activated and that session is not categorized by the system to mix with yours" - Apple, *Handling Audio Interruptions*). Since neither MindSync's session nor most telehealth apps request `mixWithOthers`, only one of the two can hold the microphone at a given moment; the other gets an interruption. MindSync already listens for this (`session.interruptionEventStream`, same file, lines 292-318) and pauses on `event.begin`, auto-resuming on any `event.end` for the v2 pipeline. If the two apps keep trading foreground focus during a call (which is exactly what happens when someone alternates between the telehealth app and MindSync, or when the OS re-arbitrates session ownership periodically), the recording gets cut into many short PCM segments that are later stitched back together (`WavBuilder.assembleFromSegments`, invoked from `_stopRecordingV2`, same file, lines 1561-1569). Each pause/resume boundary is a known point where the hardware has not yet settled to the requested 16 kHz mono format, producing audible glitches at the seams. A user describing the result as "garbled" is consistent with a recording built from many short, discontinuous, glitch-bounded segments rather than one continuous stream.

A second, not mutually exclusive, sub-mechanism is direct hardware contention rather than clean interruption delivery: several third-party telehealth/video-call apps do not integrate Apple's CallKit (CallKit is mainly used by native-feeling VoIP apps; ordinary video-consult apps like a generic Zoom/Doxy.me-style client typically manage their own `AVAudioSession` instead). When two apps race to claim the same non-CallKit-mediated session, Apple's developer forums document real reports of the OS refusing an app's requested sample rate "when another software already had control of the audio session on the device," and of general "resource contention... hardware components compete for shared hardware access, which can degrade recording quality during simultaneous operations." If MindSync's recorder ends up receiving audio at a different underlying rate/format than the 16 kHz mono PCM it is labeling and writing to disk, decoded playback would sound genuinely distorted (pitch-shifted, "chipmunked," or noisy), not just choppy.

**This is not a hypothetical failure mode invented for this report.** The exact same class of bug (two concurrent microphone captures on the same device fighting over the shared audio session) is already diagnosed, documented, and fixed elsewhere in this codebase, for a different pair of captures. See `mindsync-frontend/mindsync_app/lib/screens/health_check/cubit/health_check_flow_cubit.dart:290-307` (CS-14 fix, dated in-code): the Health Check open-ended voice flow used to run a `record`-package `AudioRecorder` **and** a parallel `flutter_webrtc` `getUserMedia` session at the same time, purely to feed a live-preview transcript box. The code comment states plainly: "Two concurrent captures fight over the same hardware microphone/audio session on both iOS (AVAudioSession contention between AudioRecorder and WebRTC's own RTCAudioSession management) and Android (two simultaneous audio input streams contending for one input source), degrading whichever one loses to near-silence." That fix removed the second in-process capture entirely. CS-01 is the same mechanism at the OS boundary (a different app) instead of the process boundary (a second capture inside our own app), which is why device verification is still required, but it is strong internal precedent that this failure mode is real, reproducible, and has already bitten this exact app once.

### Part B: a confirmed backend gap turns "degraded audio" into "silent failure" (confidence: high, code-confirmed, not a hypothesis)

Independent of exactly how the audio gets degraded, there is a real, verifiable gap in how the backend handles a transcript that comes back empty or near-empty. `MindSync/app/tasks/session_recording.py`, function `process_session_recording` (the path every session recording takes - it always uses AssemblyAI directly, never the Whisper short-form fallback used by voice notes; see `MindSync/app/services/stt_service.py:1-14`), calls `_transcribe_with_assemblyai`, stores whatever text comes back with **no check that the text is non-empty or non-trivial** (`session_recording.py:441-461`), and then proceeds straight to AI summary generation and marks the recording `COMPLETED`.

Compare this to the Whisper fallback path in the same file, `process_session_recording_whisper`, which explicitly guards against this: `if not transcript_text or not transcript_text.strip(): raise ValueError("Whisper returned empty transcription")` (`session_recording.py:774-775`), which routes the job to a `FAILED` status instead. The primary AssemblyAI path has no equivalent check, and `AssemblyAIService` exposes no confidence/quality score that is consulted anywhere in this file.

This means that even in the "best case" where the audio-session contention only degrades quality moderately, a garbled or heavily corrupted recording can still produce a technically successful AssemblyAI job with an empty or garbage transcript, and MindSync will still mark it `COMPLETED` and generate a summary from nothing. That matches [użytkowniczka V]'s report ("no transcription was produced") precisely, and it means the user gets no actionable error, just a broken result.

---

## 2. Which layer holds the problem

This is not a single-layer bug. Three layers each contribute:

- **Hard OS restriction (not fixable in app code):** iOS and Android both enforce that only one app can be the effective "owner" of the live microphone stream at full quality at a time. This is documented, intentional platform behavior, not a MindSync bug. See section 7 (matrix) for the iOS vs Android mechanism difference.
- **Our own configuration choice (fixable, but only mitigable, not eliminable):** `RecordSessionCubit` configures a session tuned for solo, ambient-room capture (`.spokenAudio` mode, `duckOthers`, no `mixWithOthers`), and has no pre-flight check for "is another app already actively using the microphone" before starting, and no live UI signal to the user when an interruption/contention event is detected mid-recording beyond a generic `healthWarning` flag that is not specific to this scenario.
- **Confirmed backend gap (fixable, cheap, backend-api owns the file):** the missing empty-transcript guard in `process_session_recording` (`MindSync/app/tasks/session_recording.py`). This is the one piece of this investigation that is not speculative; it is a straightforward code-reading finding, and it independently explains "no transcription was produced" regardless of the exact acoustic root cause.

---

## 3. Reproduction

**Where the bug is expected to appear (untested on a physical device, described from code + OS documentation):**
- iPhone, MindSync session recording started while a telehealth video/voice call app is concurrently active on the same device, especially when the user alternates foreground focus between the two apps during the call (glancing at MindSync to check elapsed time, or the telehealth app re-asserting its session periodically).
- Most likely with telehealth apps that manage their own `AVAudioSession` rather than integrating Apple's CallKit (the common case for browser-based or generic video-consult apps).
- More likely to be visibly worse if the call is routed over a Bluetooth headset (see matrix point 4) because Bluetooth's Hands-Free Profile audio path is a further quality bottleneck layered on top of the app-contention problem.

**Where it is NOT expected to appear:**
- A MindSync session recording running alone, with no other app actively using the microphone. This is the default supported use case per the in-app copy shown at the start of a recording ("Place your phone where it can hear clearly. Sessions shorter than 10 minutes won't be processed." - `recording_placementTip`, `l10n/app_en.arb:1639`), which describes the phone's own room microphone picking up an in-person conversation, not the app recording a call the phone itself is making. A concurrent telehealth call on the same device is a real and understandable use pattern, but it is not the scenario the feature's own onboarding copy describes, which is worth flagging to product/Darek independent of the technical fix.
- Android is unverified. Per Android's documented concurrent-capture policy (see matrix point 3), the expected Android failure mode is different from iOS: the OS is documented to *silence* (deliver zero/empty buffers to) the lower-priority capture rather than corrupt it, so a "garbled" symptom specifically is less likely to reproduce as-is on Android; a near-silent or unusually quiet recording is the more likely Android analogue, and that has not been confirmed either.
- A native Phone or FaceTime call interrupting a session recording is a materially different and probably safer case: those go through CallKit, which has clean, well-documented interruption semantics, and MindSync's existing `interruptionEventStream` handling was written with exactly that scenario in mind (see code comments at `record_session_cubit.dart:288-291`).

**Exact experiment needed to confirm (requires device verification):**
1. On a physical iPhone, start a MindSync session recording, then start a video call in a non-CallKit telehealth-style app (e.g. a generic browser-based or WebRTC video-consult client). Record for 10+ minutes, alternating foreground focus between the two apps. Pull the raw WAV/PCM segments from the device (or from `RecordingDebugLog`) and listen to them directly, and check the app's own debug log (`RecordingDebugLog.instance`, already wired into every step of `RecordSessionCubit`) for `audio interruption` and `audio route change` entries during the call.
2. Repeat with a CallKit-integrated calling app (e.g. a real Phone call or FaceTime Audio) as a control, to confirm the hypothesis that clean CallKit interruption handling behaves differently (gap, not garble).
3. Repeat both on Android with a telehealth app that uses `AudioSource.VOICE_COMMUNICATION`, to confirm whether Android's documented "silence the loser" policy produces a different symptom than iOS.
4. Repeat once more with a Bluetooth headset connected during the call, isolating whether the narrowband HFP path is a compounding factor independent of the two-app contention.

---

## 4. Future risk

The same mechanism is not limited to telehealth calls:

- **Any concurrently active call on the same phone** (a plain cellular/VoIP phone call arriving mid-recording) hits the same interruption path already, but through CallKit, which is the better-behaved case MindSync's code was written for. Risk here is lower and largely already mitigated, but still worth a device-QA pass since v2's "always auto-resume regardless of interruption type" behavior (`record_session_cubit.dart:301-317`) has not been re-verified against a real incoming call recently.
- **Music or other audio playing in the background** is unlikely to trigger this specific failure mode: `duckOthers` only affects output mixing (lowering the other app's playback volume), and a pure-playback app does not compete for the *microphone*, only for audio *output*. This path was checked and found low-risk, i.e. "checked, no effect" for the core garbling mechanism, though it can still interact with matrix point 6 (system audio processing) in minor ways.
- **A second Bluetooth microphone / mid-recording route change** is a real and distinct risk, already partially observed in code: `_devicesChangedSub` only logs route changes today (`record_session_cubit.dart:320-333`), it does not react to them. A route change mid-recording (headphones connected/disconnected, a Bluetooth device auto-pairing) is a known trigger for the same kind of format-mismatch glitch described in Part A, independent of a second app being involved at all.
- **Upcoming OS releases:** Apple continues to actively develop this exact API surface (see *Enhance your app's audio recording capabilities*, WWDC 2025 session 251), meaning the precise arbitration behavior between MindSync's session and a competing app's session should be expected to shift with future iOS versions, not stay fixed. Android's concurrent-capture policy has also evolved release over release since Android 10 (refined again through Android 13, per Android's own developer documentation) and could change again. Neither platform's roadmap suggests this scenario will be *solved* for third-party apps like MindSync; if anything, both platforms' direction (tighter privacy controls, more OS-mediated audio arbitration) makes an app-level workaround less likely to exist in the future, not more.

---

## 5. Fix options

At least two are required by the spec; four are given below, ordered roughly by cost, with one explicitly marked as rejected.

### Option A: Backend empty/degraded-transcript guard (recommended, do first)
Add the same guard the Whisper fallback path already has to the primary AssemblyAI path in `process_session_recording` (`MindSync/app/tasks/session_recording.py`): if `transcript_text` is empty or below a sane minimum length/word count after transcription, mark the recording `FAILED` (or a new, more specific status) instead of `COMPLETED`, and surface a clear, actionable error to the user with a retry path.
- **Cost:** Low. Small, well-scoped change in a file `backend-api` owns; requires no new infrastructure. A few hours of implementation plus tests.
- **Risk:** Low. Purely additive validation; does not touch the transcription or audio pipeline itself. Main risk is choosing too aggressive a minimum-length threshold and rejecting legitimately short-but-valid sessions, which is tunable and testable.
- **User value:** Directly fixes the reported symptom ("no transcription was produced" with no explanation). Converts a silent, confusing failure into an honest, actionable one, regardless of whatever ends up causing the audio degradation. This is the single cheapest, highest-value fix available and is independent of resolving Part A.

### Option B: Pre-flight "another app may be using your microphone" check + warning (frontend)
Before starting a session recording, check for signs that another app is already actively using the microphone/audio session (on iOS, listening for an interruption or checking session state right at start; on Android, checking `AudioManager.getMode()` for `MODE_IN_COMMUNICATION`/`MODE_IN_CALL`). If detected, show a warning before recording starts, e.g. "Another call or app seems to be using your microphone right now. For best results, close it before recording your session."
- **Cost:** Low-medium. A few days of flutter-mobile work plus new copy in two locales and a design pass with `ui-ux-designer`.
- **Risk:** Low. Purely additive; worst case is a false positive that annoys the user (mitigate by wording it as advisory, not blocking).
- **User value:** Prevents the failure proactively for the common case (user starts the telehealth call first, then opens MindSync), before 45-75 minutes are wasted. Does not catch the case where the telehealth call starts *after* MindSync recording is already underway.

### Option C: Live in-recording contention detection and warning banner
Extend the existing `interruptionEventStream` / route-change listeners (already wired in `record_session_cubit.dart`) to detect a pattern of repeated interruptions or route changes during an active recording, and surface a live, non-blocking banner mid-recording: "Recording quality may be affected by another app using your microphone."
- **Cost:** Medium. Needs heuristic tuning (how many interruptions in how short a window counts as "a problem" vs normal single-interruption behavior), new UI state, copy, and real-device QA on both platforms.
- **Risk:** Medium. Heuristics can misfire on ordinary events (plugging in headphones, a single short interruption from a text message call). Needs careful thresholds to avoid alarming users unnecessarily during normal use.
- **User value:** The best long-term outcome of the three real options: catches the problem while there is still time to react (pause the call, or accept the risk knowingly), rather than only after the fact via Option A's honest failure message.

### Option D: Force simultaneous full-quality capture via `mixWithOthers` (rejected, listed for completeness)
Attempt to configure MindSync's session to coexist with another app's session so both can capture at full quality at once.
- **Why rejected:** Not technically viable. `mixWithOthers` (and its Android analogues) govern audio *output* mixing, not concurrent *input* capture. Neither iOS nor Android supports two arbitrary third-party apps sharing full-quality simultaneous microphone access; this is the documented, intentional OS restriction described in section 2. Pursuing this would not fix the underlying contention and risks making behavior less predictable (see section 7, matrix point 7).

---

## 6. Recommendation

Ship **Option A first**. It is the cheapest fix in the whole set, it is not a hypothesis (the missing guard is a directly-read code fact, not inferred from OS documentation), it directly matches the reported symptom, and it is independent of resolving exactly which acoustic sub-mechanism (interruption-cycling stitching, hardware-format contention, or Bluetooth HFP downgrade) is responsible for the garbling. It requires `backend-api` (this repository's `flutter-mobile` agent cannot touch `MindSync/app/`).

Pair it with **Option B** on a similar timeline: cheap, low-risk, and prevents the most common version of this scenario (telehealth call already running when the user opens MindSync) before it happens at all.

Hold **Option C** until after the device-verification experiments in section 3 are actually run. Building a live-detection heuristic before confirming which failure signature (clean interruption gaps vs continuous contention vs Bluetooth downgrade) actually occurs risks tuning it against the wrong signal, the same mistake that produced the original CS-14 bug this report cites as internal precedent (an unverified assumption about how two concurrent captures would behave, discovered only through real device/QA testing).

Do not pursue Option D.

Before any of the above is scoped as a build task, run the four device experiments in section 3. They are cheap (a phone, a second phone or laptop to place the telehealth call, and about an hour), and they will tell us definitively whether the primary iOS mechanism is interruption-cycling (favors Option C's live banner, tuned around interruption frequency) or hardware-format contention (favors a different mitigation entirely, e.g. detecting and warning on an unexpected sample-rate mismatch rather than on interruption count), and whether Android needs a separate investigation track given its documented different behavior.

---

## 7. Seven-point matrix

1. **Platforms, iOS vs Android:** Different documented mechanisms, not assumed to be shared. iOS: a single-owner, interruption-based model where the losing app's session is fully deactivated when a competing non-mixable session activates (Apple, *Handling Audio Interruptions*). Android since Android 10: a "silence the loser" model, not an interruption model, the losing app keeps running but receives zero-filled/silent buffers, with explicit priority rules favoring privileged/foreground/voice-communication-source apps (`source.android.com/docs/core/audio/concurrent`). This means the same scenario is expected to *look different* on the two platforms: garbling/stitching artifacts are the iOS-shaped failure, near-silence is the Android-shaped one. Android is entirely unverified for this report (the field report is iPhone-only).

2. **Audio session setup today:** iOS category `.playAndRecord`, mode `.spokenAudio`, options `allowBluetooth | defaultToSpeaker | duckOthers`, configured via the `audio_session` package immediately before `AudioRecorder.start()` (`record_session_cubit.dart:274-286`, mirrored identically in `voice_quick_capture_cubit.dart:45-51` and `debrief_capture_cubit.dart:403-410`, confirming the audio-session configuration is consistent across MindSync's own capture flows). This is a non-mixable category by default (no `mixWithOthers`), so when another app takes the microphone, MindSync's session is deactivated and an interruption is delivered; the app already handles `begin`/`end` of that interruption by pausing and (for the v2 pipeline) always auto-resuming. What is not handled: detecting *before* recording starts that another app already holds the session, and distinguishing "a single clean interruption" from "repeated contention throughout the recording."

3. **Active VoIP call in the background, what we actually receive:** Not confirmed on-device (requires the experiment in section 3). Two credible, non-exclusive candidates from OS documentation: (a) clean interruption cycling, MindSync's recording is legitimately paused and resumed multiple times, producing a stitched recording with audible seams; (b) direct hardware/format contention when the competing app does not use CallKit's cleaner arbitration path, where Apple's own developer forums document the OS refusing a requested sample rate "when another software already had control of the audio session on the device," which would produce genuinely distorted (not merely gapped) audio. Both are plausible explanations of "too garbled."

4. **Bluetooth and headsets:** Checked via documentation, not on-device. If the call (or the recording) is routed through a Bluetooth headset, the device is very likely operating in the Hands-Free Profile (HFP), which is capped at 8 kHz mono narrowband audio unless the headset additionally supports the newer mSBC/Wideband Speech extension (HFP 1.6+). MindSync requests 16 kHz mono for its own recording regardless of route (`_recorder.start(RecordConfig(... sampleRate: 16000 ...))`, `record_session_cubit.dart:344-350`, and `CrashSafeRecorder`'s PCM stream, `crash_safe_recorder.dart:66-72`). A Bluetooth-routed call layers a real, independent quality ceiling (8 kHz narrowband, lossy compression) on top of whatever the app-contention mechanism does, and is a plausible compounding factor in "too garbled," not the sole cause on its own since [użytkowniczka V]'s device details do not confirm Bluetooth was in use.

5. **Signal parameters:** MindSync records 16 kHz mono. v1 path: WAV on iOS (chosen specifically because certain iOS versions silently produce empty/28-byte files with the hardware AAC encoder, see project memory `pattern-ios-wav-recorder`) or AAC-LC 64 kbps on Android; v2 path (the current default, `_usePipelineV2 = true`): raw PCM 16-bit mono at 16 kHz, assembled into a WAV after stop. There is no code-level fallback to a lower-quality "telephony mode" on MindSync's side; if a degraded mode is observed, it is being imposed on the shared hardware by the OS during contention (candidate 3b above), not requested by MindSync's own configuration.

6. **System processing (echo cancellation, noise suppression, AGC):** MindSync's own recorder (`record` / `AVAudioRecorder`, no `AVAudioEngine` voice-processing tap) does not itself invoke iOS's voice-processing I/O unit, so MindSync is not applying AEC/NS/AGC to its own capture. However, a telehealth app running concurrently very likely *does* enable voice-processing (VoIP/video-call apps almost universally do, precisely for echo cancellation on the call's own audio). Apple's voice-processing I/O unit is documented to affect audio session behavior at a level broader than just the app that enabled it in some configurations (see the general resource-contention findings in section 1), which is a plausible contributor to the observed distortion but not confirmed without a device test; flagged as "needs device verification," not "checked, no effect."

7. **OS limits, hard restriction vs our own misconfiguration:** The core restriction, that iOS and Android do not allow two arbitrary third-party apps full-quality simultaneous microphone access, is a hard, documented, intentional OS restriction, not something fixable at the app layer (see Option D, rejected). What is within MindSync's control and is a configuration/product gap rather than an OS limit: no pre-flight detection of a competing session, no live warning during a detected contention event, a session category/mode tuned only for the solo-room-mic use case, no route-change reaction beyond logging, and, independently, the confirmed backend gap in section 1 Part B that lets a degraded result reach the user silently as "success" instead of a clear failure.

---

## Appendix: evidence used

**Business/spec documents**
- `Business_requirements/MS_3/v3.10/MSV3.10 - User Feedback Fix.md` (CS-01 spec, the task source)
- `Business_requirements/MS_3/v3.2/fixes/phases/20_PHASE_B_FE_VOICE.md` (CS-02 iOS voice pipeline history, referenced for the AVAudioSession/record-package pattern and known encoder quirks)

**Frontend code (Flutter, `mindsync-frontend/mindsync_app/`)**
- `lib/screens/fab_flows/cubit/record_session_cubit.dart` (full read, 1905 lines): session-recording lifecycle, iOS AVAudioSession configuration (`_configureIosAudioSessionForBackground`, lines 274-334), v1 recorder config (lines 336-354), v2 pipeline (`_startRecordingV2`, `_stopRecordingV2`, `resumeSessionV2`, lines 1296-1840), interruption handling (lines 292-318), route-change logging only (lines 320-333)
- `lib/services/recording_pipeline_v2/crash_safe_recorder.dart` (full read): PCM streaming recorder used by the default v2 pipeline, `RecordConfig(encoder: pcm16bits, sampleRate: 16000, numChannels: 1)`, no `iosConfig`/`manageAudioSession` override (relies on the cubit's separate `audio_session` configuration)
- `lib/screens/workspace/cubit/voice_quick_capture_cubit.dart` (grep + targeted read): confirms identical iOS audio-session configuration to `RecordSessionCubit`
- `lib/screens/debrief_capture/cubit/debrief_capture_cubit.dart` (targeted read, header doc + audio-session block): confirms identical iOS audio-session configuration; header doc states "the `record` package (AudioRecorder) is the SOLE microphone owner" as an explicit design rule for this cubit
- `lib/screens/health_check/cubit/health_check_flow_cubit.dart` (targeted read, lines 260-340 and 720-780): **CS-14 fix and its root-cause doc comment**, the key internal precedent for this investigation; documents a previously real, previously fixed dual-microphone-capture contention bug in this exact codebase (WebRTC + AudioRecorder), with an explicit statement that concurrent captures degrade "whichever one loses to near-silence" on both iOS and Android
- `pubspec.yaml`: `record: ^5.1.3`, `audio_session: ^0.1.25`
- `l10n/app_en.arb` (grepped): `recording_placementTip` (line 1639), confirming the feature's own onboarding copy describes room-mic capture of an in-person conversation, not capture of a call the phone itself is making
- `ios/Runner/Info.plist`: `UIBackgroundModes` includes `audio` (background recording capability)
- `android/app/src/main/AndroidManifest.xml`: `RECORD_AUDIO`, `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_MICROPHONE`, `MODIFY_AUDIO_SETTINGS` permissions confirmed

**Backend code (`MindSync/app/`, read-only)**
- `app/services/stt_service.py` (full read): confirms session recordings always use AssemblyAI directly and never the Whisper short-form fallback used by voice notes
- `app/tasks/session_recording.py` (targeted read, lines 1-130 and 390-510, plus a broader grep pass): `process_session_recording` (AssemblyAI path, no empty-transcript guard, lines 429-461) vs `process_session_recording_whisper` (explicit empty-transcript guard that fails the job, lines 774-775). This asymmetry is the confirmed backend gap in section 1 Part B.
- `app/services/assemblyai_service.py` (grep): confirmed no confidence/quality score is exposed or consulted anywhere in the session-recording path

**Agent memory (historical context, not re-verified against current code except where cross-checked above)**
- `.claude/agent-memory/flutter-mobile/recording_pipeline_history.md`
- `.claude/agent-memory/flutter-mobile/ios_voice_note_fallback.md`
- `mindsync-frontend/.claude/agent-memory/flutter-mobile/feedback_record_package_ios_audio_session.md` (documents the `record`/`record_darwin` `manageAudioSession` default-off quirk and the proven `audio_session`-package pattern MindSync uses)
- `MindSync/.claude/agent-memory/flutter-mobile/pattern_ios_wav_recorder.md` (documents the iOS hardware AAC encoder quirk behind the WAV-on-iOS choice, and explicitly notes the `record` package has "no phone call management")

**External sources (web research, current as of 2026-09-01)**
- Apple, *Handling Audio Interruptions*: https://developer.apple.com/library/archive/documentation/Audio/Conceptual/AudioSessionProgrammingGuide/HandlingAudioInterruptions/HandlingAudioInterruptions.html
- Apple, `AVAudioSession.interruptionNotification`: https://developer.apple.com/documentation/avfaudio/avaudiosession/interruptionnotification?language=objc
- Apple Developer Forums, sample-rate forced by another app already controlling the session: https://developer.apple.com/forums/thread/798906
- Apple, WWDC 2025 session 251, *Enhance your app's audio recording capabilities*: https://developer.apple.com/videos/play/wwdc2025/251/
- Apple Developer Forums, background recording requires foreground start, then the `audio` background mode allows continuation: https://developer.apple.com/forums/thread/770556
- Medium, AVAudioSession conflicts and resource-contention discussion: https://medium.com/@mi9nxi/haptic-feedback-and-avaudiosession-conflicts-in-ios-troubleshooting-recording-issues-666fae35bfc6
- Android, official concurrent capture policy documentation: https://source.android.com/docs/core/audio/concurrent
- Android Police, consumer-facing summary of the Android 10 concurrent-microphone-access change: https://www.androidpolice.com/2019/09/12/android-10-allows-multiple-apps-to-access-your-microphone-at-once/
- XDA Forums, real-world report of Android silencing AudioRecord sources during active calls: https://xdaforums.com/t/android-hal-silences-all-audiorecord-sources-during-active-calls-is-session-ownership-the-only-solution.4786798/
- Android Authority, aptX Voice / Bluetooth call quality background (HFP narrowband vs wideband): https://www.androidauthority.com/aptx-voice-bluetooth-call-quality-1056511/
- `record` Flutter plugin repository: https://github.com/llfbandit/record
