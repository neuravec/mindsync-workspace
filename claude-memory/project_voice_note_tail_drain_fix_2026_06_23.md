---
name: project_voice_note_tail_drain_fix_2026_06_23
description: "Voice-note \"nothing recorded\" on immediate-Save after long monologue — fixed by replacing 1.2s settle with 8s smart bounded tail-drain (Path B only)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 82521988-96d2-4ac9-87ba-1aa0c095df19
---

Voice-note (głosówka) recording with Realtime API kept losing the note when the user spoke **long and continuously** then tapped Save **immediately**: UI said "nothing recorded" even though they talked a lot. Talk→pause→wait-for-text→Save worked fine. All 3 capture flows (debrief/prep-card/between-session) share ONE cubit `DebriefCaptureCubit`, so one fix covers all three. See [[ios-voice-note-fallback]] and [[project_voice_note_too_short_ios_fix_2026_06_22]].

**Root cause:** On iOS WebRTC wins AVAudioSession → M4A near-empty → every iOS note uses Path B (live transcript = only content). The end-of-recording grace (`_kStopSettleMs=1200ms`, `_settleTranscription()`) was too short AND exited on the FIRST chunk. With `semantic_vad`, a transcript chunk only arrives after the server detects end-of-speech AND transcribes the segment. A long continuous monologue = one uncommitted VAD segment; at Stop the transcript is empty, and the server needs ~0.5–1s (silence detect) + 1–3s (transcribe tail) = 2–5s. The 1.2s settle bailed first → empty transcript → noAudio/tooShort.

**Fix (frontend-only, `lib/screens/debrief_capture/cubit/debrief_capture_cubit.dart`):**
- Path B now calls new `_drainTailTranscript()` (NOT `_settleTranscription`); Path A (real M4A/Android upload) UNCHANGED, still 1.2s cosmetic settle.
- `_drainTailTranscript`: Stopwatch + 250ms-slice loop, re-arms `_finalTranscriptDrain` each slice so a landing chunk wakes it immediately. Constants `_kTailDrainMaxMs=8000` (hard cap, always terminates), `_kTailDrainQuietMs=1500` (exit once content quiet this long). Keeps waiting while transcript still empty (cap not hit) — this is the actual fix for the long-monologue case.
- Pure testable helper `shouldKeepDrainingTail({transcriptLen, elapsedMs, msSinceLastGrowth})` mirrors `decideStopOutcome` pattern.
- `decideStopOutcome` signature+logic byte-identical (untouched). UI already shows `processing(captured)` before the drain, so the up-to-8s wait is invisible.
- Teardown safe: `_cleanupTranscription` completes any in-flight drain so `close()` can't hang; loop nulls only its own completer ref.

**Status:** IMPLEMENTED on disk, NOT committed/pushed (left in working tree per [[feedback_concurrent_session_git_hygiene]]). 31/31 tests (17 existing decision + 14 new drain-logic), analyze clean. **Remaining:** on-device iOS QA of 3 scenarios (long-continuous→immediate Save saves; pause→Save still fast ~1.5s; talk-then-wait path unregressed), then commit only the 2 files to dev → Codemagic/TestFlight.
