# PHASE B — Frontend: Voice input (MSV3.2 Fix.1) — run in repo `mindsync-frontend/`

## SYSTEM INSTRUCTIONS (read fully before any tool call)

You are a fresh Claude Code session acting as the team lead for the VOICE slice of the MSV3.2 Fix.1
batch. Project rules come from `CLAUDE.md` (auto-loaded). Delegate implementation to `flutter-mobile`
(and `qa-testing` at the end); keep the agent count lean.

- Repo: `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend` — branch **dev**. App code in `mindsync_app/`.
  Do not touch the backend repo (if you find a backend root cause for CS-02, STOP on that sub-item and
  record it in STATUS.md for PHASE A / the operator).
- **Commit locally, stage only files you touched, NEVER push** (push to dev triggers Codemagic → TestFlight — operator's call).
- May run in parallel with PHASE A (backend). No other FE session may run at the same time.
- l10n: every new/changed string in PL + ENG (all ARB locales get at least the EN value); run gen-l10n;
  run build_runner after model changes; **commit generated code**.
- Read `00_MASTER_PLAN.md` (decisions log). When done, APPEND your report to `STATUS.md`.
- Test baseline: 30 FE failures pre-exist. `flutter analyze` must introduce no new errors.

## Context you should know (from project memory)
- Voice notes v2 (2026-07-04): prep/debrief/between notes go stop → Whisper transcription → user edits →
  accept; there is a recovery pointer; there was a fix for empty M4A files on iOS.
- MSV3.2 batch (2026-07-06) included an iOS mic fix (AVAudioSession) that still required QA on a real
  iPhone. Session recording v2 is default. An older triage note: freezes on stale builds ≤130 — the
  current dev branch is far past that, but keep build-version sanity in mind when reasoning about repros.
- The pufferfish Lottie asset is ALREADY committed: `mindsync_app/assets/lottie/pufferfish_error_v2.json`
  (package `lottie: ^3.3.1` already in pubspec; `assets/lottie/` already registered). The source zip
  `Business_requirements\MS_3\Lottie animations for Flutter pufferfish.zip` also contains a v1 JSON and a
  design-system reference (`_ds/...: colors_and_type.css`, README) — use it as styling reference for the card.

## Spec items (verbatim scope — implement exactly)

### CS-01 · CHANGE · Record error card — full redesign + pufferfish Lottie
Shown whenever a voice recording fails, in ALL voice-input flows (one shared component). Lead: grep the
current error-card widget / "Ups!" strings.
UI anatomy (top to bottom):
1. Top: card title + X to close the window
2. Middle: Lottie animation — pufferfish (existing asset; loop + autoplay). **Coral Pink circle removed entirely.**
3. Below: title — PL „Ups!" / ENG „Yieks!" (intentional spelling, verbatim) + subtext with error-type
   information — a DISTINCT string per error type (e.g. mic permission / nothing heard / upload failed;
   enumerate the failure types the recording flow can actually raise from code).
4. Bottom: primary button PL „Ponów próbę" / ENG „Try again"; below it SECONDARY button PL „Porzuć" /
   ENG „Discard" (restore — currently missing; must be a ghost-style secondary BUTTON, not a text link).
Logic: X → discard recording, close, no confirm → previous screen. „Ponów próbę" → restart recording in
the same flow, card dismissed. „Porzuć" → identical to X.
Do NOT touch: happy-path recording UI; permission-request flow; other modal states.
Done when: error card in every voice flow matches anatomy 1–4; each error type shows its own subtext;
all three exits behave per logic; no Coral Pink circle rendered; builds pass Android + iOS.

### CS-02 · FIX · iOS recording upload fails everywhere
On iOS, attempting a voice recording in ANY functionality immediately errors that the recording can't be
uploaded. Manual text input works. Android works. Diagnose from code (leads, not conclusions: permissions /
audio codec / AVAudioSession config / empty-M4A regression / upload pipeline / content-type) and fix at root.
Do NOT touch the Android voice path or manual text input.
Done when: a voice note records and processes on iOS in every voice-enabled feature, including the weekly
check-in / therapy-relationship card; Android unchanged. (Real-device iPhone QA cannot be done in this
session — implement, verify by code-trace + tests, and flag device QA in STATUS.md.)

### CS-04 · FIX · Remove the transcription-promise line
Recording screen helper text „Your transcript will appear here after you stop recording." — delete ONLY
that exact string and its PL sibling of the same key. Nothing else on the screen changes.
Done when: grep for the string returns no live references; screen renders without it in PL and ENG.

## Definition of done (Phase B)
- All three items done per their "Done when"; shared error card verified reachable from every voice flow.
- `flutter analyze` clean of new errors; targeted widget/cubit tests added; full `flutter test` — no new
  failures vs the 30-failure baseline.
- Commits local on dev (generated code committed). STATUS.md report appended, including: enumerated error
  types + their subtext strings, iOS root cause found for CS-02, and remaining device-QA items.

## Code anchors (planner-provided; verify before use)
All paths under `mindsync_app/`.

**CS-01 — the error card ALREADY partially exists**: `lib/widgets/voice_error_card.dart` —
`class VoiceErrorCard` L44, `enum VoiceErrorKind{micPermission,noAudioHeard,processingFailed}` L12;
already renders `assets/lottie/pufferfish_error_v2.json` (L94) **plus the Coral Pink circle (remove)**;
retry = `l10n.capture_tryAgainButton` → `onRetry` L117; discard = `l10n.voiceError_discardButton` „Porzuć"
→ `onDiscard` L133 (currently a TEXT button → restyle as ghost secondary BUTTON). The card deliberately has
no title/X — hosts provide them; spec anatomy requires card title + X at the top: decide whether to add
them to the shared widget or verify EVERY host renders them (spec wants one shared component).
Host flows (each maps state→kind via `_voiceErrorKindFor*`): `lib/screens/fab_flows/record_session_flow.dart`,
`lib/screens/debrief_capture/debrief_capture_screen.dart`,
`lib/screens/workspace/widgets/voice_or_text_capture_sheet.dart`,
`lib/screens/workspace/cubit/voice_quick_capture_state.dart`.
Existing per-error ARB keys (`l10n/app_pl.arb` L1670–1673): `voiceError_micPermissionMessage`,
`voiceError_noAudioMessage`, `voiceError_processingFailedMessage`, `voiceError_discardButton`; generic:
`common_somethingWentWrong`, `recording_somethingWentWrong` (L1519). Spec requires title PL „Ups!" /
ENG „Yieks!" (verbatim) + a distinct subtext per failure type — extend `VoiceErrorKind` if the pipeline
raises more types (e.g. upload failed vs processing failed).

**CS-04** — key `capture_recordingTranscriptHint`: EN `l10n/app_en.arb:1409`, PL `l10n/app_pl.arb:1301`
(„Transkrypcja pojawi się tutaj po zakończeniu nagrywania."). Usage:
`lib/screens/debrief_capture/debrief_capture_screen.dart`. Do not confuse with
`capture_stageTranscribingLabel` / `recording_stageTranscribing` (stay).

**CS-02 — voice pipeline map**: recorder `lib/services/recording_pipeline_v2/crash_safe_recorder.dart`
(package `record`, `startStream(RecordConfig(encoder: pcm16bits…))` L66; the `record` plugin manages
AVAudioSession natively — no Dart-side session config; iOS native under `ios/Runner/`). Support:
`chunked_upload_manager.dart`, `background_upload_cubit.dart`, `wav_builder.dart`,
`lib/services/foreground_recording_service.dart`, `recording_recovery_service.dart`.
Upload/transcribe API: `lib/api/api_managers/audio_v2_manager.dart` (POST `/audio-v2/transcribe`
multipart L40, POST `/audio-v2/realtime-session` L12) and `lib/api/api_managers/recording_manager.dart`
(chunked initiate/chunk/complete). Voice-notes v2 flow (stop→Whisper→edit→accept) + iOS empty-M4A history:
see memory notes `project_voice_notes_v2_whisper_review_2026_07_04` and the AVAudioSession fix in
`project_msv3_2_workspace_batch_2026_07_06`. Phase A audits the BE side (STATUS.md will carry findings).

**Lottie**: fluttergen accessors `lib/gen/assets.gen.dart` (`$AssetsLottieGen` L315); example usages
`lib/widgets/lottie_overlay.dart`, `lib/utils/lottie_helpers.dart`. Run `fluttergen` if you add assets.
