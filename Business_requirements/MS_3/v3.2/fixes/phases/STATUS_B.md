# MSV3.2 Fix.1 — PHASE B (FE voice) — STATUS

## PHASE B — Frontend: Voice input — DONE — 2026-07-17

- **Session commits** (repo `mindsync-frontend`, branch `dev`, **committed locally, NOT pushed**):
  - `716f33b` — "MSV3.2Fix.1 B: voice error card redesign, iOS recording upload fix, drop transcript hint" (23 files, +438 / −178). Single commit covering CS-01 + CS-02 + CS-04 (they share the ARB + generated-l10n files, so splitting would fragment those).

- **Items completed (spec IDs):** CS-01, CS-02 (FE portion), CS-04 — all three per their "Done when".

- **Items NOT completed / deviations + why:** none outstanding. Deviations noted below (all intentional):
  - CS-01 anatomy #1 ("card title + X at top") is **host-provided, not baked into the shared card**. All four real hosts already render a title + close (X) whose close = discard + pop with no confirmation, exactly matching the spec's "X → discard, close, no confirm". Baking a second X into the shared widget would double the X in every host and force touching each host's close/permission logic, which the guardrails forbid. The shared card owns anatomy #2 (Lottie), #3 (headline + subtext) and #4 (primary + ghost buttons); #1 is verified present + consistent on every host (Record = AppBar X; Debrief/Prep/Between = `_buildHeader` X; Workspace sheet = header-row IconButton X).
  - CS-01 primary button uses a **new** key `voiceError_retryButton` (PL „Ponów próbę" / EN „Try again") rather than the shared `capture_tryAgainButton` (PL „Spróbuj ponownie") — the spec text for this button is verbatim „Ponów próbę", which differs from the existing shared string, and reusing it would have changed other screens.

- **API contract deviations (API_CONTRACT_Fix1.md):** none. No request/response shape changed. `POST /api/v1/audio-v2/transcribe` is unchanged; we only fixed the multipart `filename`/`content-type` the client sends (see CS-02). Backend already accepts wav (`audio_v2.py`: "Accepts m4a, mp3, mp4, wav, webm").

- **New migrations:** none (FE-only phase).

- **Test results (FE baseline 30 failures):**
  - Full `flutter test`: **1090 pass / 30 fail** → unchanged vs the 30-failure baseline (zero new failures, zero regressions).
  - `flutter analyze` on all touched files: **no new errors** (1 pre-existing `info`/`prefer_const_constructors` at `record_session_flow.dart:1129`, in code I did not touch).
  - `test/widgets/voice_error_card_test.dart` rewritten for the new anatomy: **14 tests, all green** (headline present, no Coral Pink circle, ghost `OutlinedButton` discard, distinct subtext per kind ×5, retry/discard callbacks, PL wiring).
  - `l10n_completeness_test.dart` + `debrief_capture_cubit_test.dart` + `debrief_capture_decision_test.dart`: all pass (ARB parity intact; CS-02 recorder change did not break the debrief state machine).

---

## CS-01 — enumerated error types + their subtext strings

The shared `lib/widgets/voice_error_card.dart` `VoiceErrorKind` enum now has **5** kinds (was 3). Each renders a DISTINCT subtext under the „Ups!"/„Yieks!" headline. The two new kinds (`couldNotStart`, `interrupted`) are real distinctions the pipeline already raised but that previously collapsed into `processingFailed` with one generic string.

| Kind | Raised by (message → kind mapping) | EN subtext | PL subtext |
|------|-----------------------------------|-----------|-----------|
| `micPermission` | `error_microphoneRequired` / `error_microphoneRequiredShort` | "Microphone permission is required to record. Check your settings and try again." | „Aby nagrywać, potrzebujemy dostępu do mikrofonu. Sprawdź ustawienia i spróbuj ponownie." |
| `noAudioHeard` | `error_recordingNoAudio`, `error_recordingFailedSilently`, `error_noAudioDetected`, `error_noAudioHeard`, `CaptureErrorType.noAudio`/`.tooShort`, empty-transcript | "We couldn't hear anything. Check your microphone and try again." | „Nic nie słyszeliśmy. Sprawdź mikrofon i spróbuj ponownie." |
| `couldNotStart` (NEW) | `error_couldNotStartRecording` (recorder failed to start) | "We couldn't start the recording. Please try again." | „Nie udało się rozpocząć nagrywania. Spróbuj ponownie." |
| `interrupted` (NEW) | `error_recordingInterrupted` (cut off mid-recording) | "Your recording was interrupted before we could finish. Please try again." | „Nagrywanie zostało przerwane, zanim się zakończyło. Spróbuj ponownie." |
| `processingFailed` | any other recording-phase failure (generic fallback) | "Something went wrong while processing your recording. Please try again." | „Coś poszło nie tak podczas przetwarzania nagrania. Spróbuj ponownie." |

Fixed strings (same across all kinds):
- Headline `voiceError_title`: EN „Yieks!" / PL „Ups!" (verbatim, intentional spelling).
- Primary button `voiceError_retryButton`: EN „Try again" / PL „Ponów próbę".
- Secondary ghost button `voiceError_discardButton`: EN „Discard" / PL „Porzuć".

New ARB keys added to all 7 locales (`voiceError_title`, `voiceError_retryButton`, `voiceError_couldNotStartMessage`, `voiceError_interruptedMessage`); PL + EN verbatim, EN fallback value for de/es/fr/nb/sv per the batch rule. `flutter gen-l10n` was run; generated code committed.

**Scope note — what the card does NOT cover:** "upload failed" and "Whisper transcription failed" are intentionally NOT `VoiceErrorKind`s. In the Debrief/Prep/Between flow those are separate states (`DebriefCaptureTranscriptionFailed`, `DebriefCaptureUploadFailed`) with their own dedicated recovery screens offering keep-for-later / delete / retry — richer than this card, and flagged "other modal states" by the guardrails, so left untouched. In the Record-session flow, upload/network/processing failures still route to that flow's `_ErrorView` (unchanged). This is documented so it is not mistaken for a gap.

---

## CS-02 — iOS "recording can't be uploaded": root cause + fix

**Root cause (FE, iOS-specific, high confidence — code evidence in-repo):**
The session-recording flow (`RecordSessionCubit.startRecording`, lines ~201–207) works on iOS *because it deliberately records WAV on iOS*, with this exact rationale in code:

> "Use WAV on iOS — the hardware AAC encoder on certain iOS versions silently fails to write audio frames, producing a 28-byte ftyp-only file. WAV bypasses the hardware encoder and reliably captures audio. On Android, AAC works correctly…"

But the two **note** flows — `DebriefCaptureCubit` (debrief / prep-card / between-session, incl. the therapy-relationship & weekly check-in voice notes) and `VoiceQuickCaptureCubit` (Workspace agenda/to-do quick-capture) — recorded **`AudioEncoder.aacLc` → `.m4a` on ALL platforms including iOS**. On the affected iOS versions the HW AAC encoder writes no audio frames, so the `.m4a` is empty / ftyp-only. That file then either trips the `kMinUsefulBytes` corruption guard, or is uploaded to `POST /audio-v2/transcribe` where Whisper cannot decode it and the endpoint 500s ("Audio transcription failed") — surfacing to the user as "the recording can't be uploaded". Manual text input works (it skips the file entirely); Android works (AAC is fine there). The MSV3.2 AVAudioSession fix addressed a *different* iOS failure (session not in `.playAndRecord`) and did not touch the encoder, so it could not fix this.

**Fix (FE, this commit):**
1. `DebriefCaptureCubit.startRecording` and `VoiceQuickCaptureCubit.startRecording`: choose encoder/extension by platform — `AudioEncoder.wav` + `.wav` on iOS, `AudioEncoder.aacLc` + `.m4a` on Android — mirroring the proven `RecordSessionCubit` workaround. Android voice path is untouched.
2. `AudioV2Manager.transcribe`: derive the multipart `filename` (`recording.$ext`) and `content-type` (`audio/wav` for wav, else `audio/mp4`) from the actual file extension, instead of the hard-coded `recording.m4a`. Whisper sniffs format primarily from the filename, so an iOS WAV must be labelled `recording.wav` or transcription fails. Mirrors the existing `RecordingManager.uploadRecording` pattern (`DioMediaType`).

The `kMinUsefulBytes = 2048` corruption guard still holds for WAV (44-byte header + PCM; a real ≥0.1 s note is far larger, a header-only WAV is correctly rejected). The recovery-pointer / autosave logic is extension-agnostic (prefix + `.autosave` suffix match; full path incl. extension stored in the pointer), so it keeps working with `.wav`.

**Known trade-off (device-QA item, not a blocker):** WAV at 16 kHz mono 16-bit ≈ 32 KB/s ≈ 1.9 MB/min, so an iOS note longer than ~13 min exceeds the transcribe endpoint's 25 MB cap (→ HTTP 413). The note flows cap recording at 15 min, so only 13–15 min iOS notes are affected — strictly better than the current state where *every* iOS note fails. Notes are typically short; flagged below for QA / possible follow-up (e.g. iOS-note cap of 13 min, or client-side downsample) if long iOS notes prove common.

**Backend note for PHASE A / A13 audit:** no backend change is required for this fix — the endpoint already accepts wav and does not validate content-type. If A13's server-side logs still show iOS transcription 500s AFTER this build ships, capture the OpenAI error detail (the endpoint currently collapses everything to a generic 500 "Audio transcription failed"); a more specific 4xx/detail on decode failure would speed future triage, but that is a nice-to-have, not part of CS-02.

---

## Manual QA still needed (physical iPhone — cannot be done in this session)

1. **CS-02 core:** on a real iPhone, record a voice note in EACH flow and confirm it transcribes + saves (no "can't upload"):
   - Debrief (After-Therapy), Prep-card, Between-session.
   - Weekly check-in voice note and Therapy-relationship card voice note (spec explicitly calls these out).
   - Workspace quick-capture ("Nagraj") for Agenda and To-do.
   - Session recording (should be unchanged — regression check only).
2. **CS-02 encoder:** confirm the produced iOS file is a non-trivial `.wav` (not a 28-byte stub) and that amplitude/level indicators animate during recording.
3. **CS-02 long-note edge:** record a ~14-min iOS note and confirm behaviour at the 25 MB / 13-min boundary (expected: works up to ~13 min; may 413 beyond). Decide whether an iOS-note cap or downsample is warranted.
4. **CS-01 layout on device:** verify the redesigned card (no coral circle, „Ups!"/„Yieks!" headline, primary + ghost buttons) renders without clipping on a small iPhone (SE) inside the Workspace bottom sheet (now `height: 440`, card scrolls internally) and in the full-screen hosts; verify PL strings render fully.
5. **CS-01 exits on device:** X (host), „Ponów próbę" (re-records same flow), and „Porzuć" (discard + close, no confirm) all behave per spec in each of the four hosts.
6. **CS-04:** confirm the recording screen no longer shows the "Your transcript will appear here…" line in PL and EN.

## Notes for next phases
- No shared cubit/model signatures changed; `VoiceErrorKind` gained two values (all `switch`es over it updated). Other FE phases can reuse `VoiceErrorCard` as-is.
- No `.freezed.dart` / build_runner regen was needed (no Freezed/JSON model changed) — only `flutter gen-l10n` for the new/removed ARB keys; generated l10n committed.
