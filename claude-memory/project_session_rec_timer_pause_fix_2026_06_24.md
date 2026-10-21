---
name: project_session_rec_timer_pause_fix_2026_06_24
description: Session-recording (v2) elapsed timer froze in iOS background + Pause hung/unresponsive — fixed with wall-clock elapsed + UI-first guarded pause
metadata: 
  node_type: memory
  type: project
  originSessionId: 82521988-96d2-4ac9-87ba-1aa0c095df19
---

Session recording (crash-safe pipeline v2, `record_session_cubit.dart`) — audio capture worked (10+ min saved), but TWO timer bugs on iOS, confirmed from device logs. See [[project_session_rec_stale_build_triage_2026_06_23]] and [[project_session_recording_ungated_2026_06_22]].

**Bug A — elapsed timer froze in background ("zegar szwankuje").** `_startElapsedTimer` did `_elapsed += 1s` per `Timer.periodic` tick; iOS suspends Dart timers when backgrounded → undercount. Log proof: 22 min real recording → counter only reached 608s (~10 min). Code already half-knew this ("Fix 5" stop-gate uses `max(pcmBytes/32000, _elapsed)`) but the DISPLAYED timer still used the freezable counter.

**Bug B — Pause hung / app unresponsive.** `pauseRecording()` v2 did `await _crashSafeRecorder.pause()` (→ `record` pkg `_recorder.pause()`, hangs on iOS streaming) BEFORE cancelling the timer + emitting `isPaused:true`. So UI never flipped, timer kept ticking, user spammed Pause → **21 calls in 10s** in the log (elapsed advancing 608→618 = `.cancel()` after the await never reached).

**Fix (frontend-only, IMPLEMENTED on disk, NOT committed):**
- `record_session_cubit.dart`: new fields `_recordingStartedAt` / `_accumulatedPaused` / `_pausedAt`; pure `@visibleForTesting static Duration computeElapsed({startedAt, now, accumulatedPaused, pausedAt})` (`now−start−accumPaused−inProgressPause`, clamp≥0). `_startElapsedTimer` now SETS `_elapsed=computeElapsed(...)` each tick (timer only drives 1Hz refresh). `_startRecordingV2` anchors `_recordingStartedAt=now`; `resumeSessionV2` anchors `now−(PCM-estimated elapsed)` so recovery continues from the right point. `didChangeAppLifecycleState(resumed)` snaps `_elapsed` immediately (observer already registered for existing pollStatusNow). pause/resume v2: idempotency guard (already-paused→return) + UI-first (cancel/restart timer, set/fold `_pausedAt`↔`_accumulatedPaused`, emit) THEN `unawaited(pause()/resume())`. v1 branches untouched.
- `crash_safe_recorder.dart`: `pause()/resume()` keep setting `_isPaused` first (which already gates PCM byte-writes = real guarantee), then `await _recorder.pause/resume().timeout(2s, onTimeout:(){})`.
- Untouched: capture, AVAudioSession/background, foreground service, health-check-never-in-v2 guards, stop 5s-timeout + segment assembly, "Fix 5", `_isStopping`.
- 27/27 tests (`test/screens/fab_flows/record_session_elapsed_pause_test.dart` +11), analyze clean. Verified by lead reading the diff (pause accumulation no double-count, recovery anchor, foreground snap).

**Known minor (non-prod):** v1 `startRecording` path doesn't set `_recordingStartedAt` → if `_usePipelineV2` ever flipped false (debug-only; hardcoded true), v1 timer would read 0. Dead code in prod; 1-line fix available if wanted.

**Remaining:** on-device iOS QA — (1) background 10+ min → foreground snaps to correct elapsed; (2) single Pause tap stops timer+flips instantly, re-tap idempotent, Resume continues from correct time; (3) server length = non-paused time. Then commit 3 files (2 lib + 1 test) → dev → TestFlight.
