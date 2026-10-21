---
name: project_session_rec_stale_build_triage_2026_06_23
description: Session-recording freeze/hang/loss bug report 2026-06-23 was a STALE TestFlight build (≤2.0.57/130) — fix c08243a first ships in build 2.0.58 (131)
metadata: 
  node_type: memory
  type: project
  originSessionId: 82521988-96d2-4ac9-87ba-1aa0c095df19
---

User reported (2026-06-23) session recording (75-min, crash-safe v2) bug: turn off internet mid-recording → app hung; after recovery prompt "Continue" the mic animates but **timer frozen**; after app kill "Continue" starts from 0 / no audio recovered. Logs showed:
```
health check: file size = 0 bytes (prev=0)
health check: file not growing for 30s — attempting restart
attempting recorder restart (attempt 1/2)
stopRecordingV2() — stopping CrashSafeRecorder   (×4 over 4 min, elapsed frozen, no completion)
resumeSessionV2() — estimated elapsed from existing PCM: 0s (0 bytes)
```

**Diagnosis: NOT a current-code bug — it's the v1-health-check-restart-in-v2 cascade already fixed by `c08243a` (see [[project_recording_chunks_postgres_2026_06_22]] item 6). The user's TestFlight build predates that fix.** Proven impossible on current code: `record_session_cubit.dart` v2 never starts the health-check timer (startRecording v2 returns L206; resume v2 skips it L365-377), and `_performHealthCheck` has `if(_usePipelineV2)return;` BEFORE the `health check: file size` log (L868) — so that log line cannot be produced by current code. Current code also has `stop().timeout(5s)` (L1158) + per-segment manifest append (L1100-1114), so stop can't hang and kill-recovery finds audio.

**Build-number mapping (frontend repo `mindsync-frontend`, git):**
- `2.0.56 (129)` = `4af9db5` background-recording fix, NO c08243a (background/screen-off works for user ✓, proves they're ≥129)
- `2.0.57 (130)` = `2289134` pre-release, still NO c08243a
- **`2.0.58 (131)` = first build WITH `c08243a`** (`7a4b9de` pre-release after the fix). On origin/dev (HEAD=99c8ccb, local==origin, clean).

**Resolution: tell user to install TestFlight build 2.0.58 (131)+ and re-test 3 scenarios (background / internet-off / app-kill recovery). No new code.** TestFlight's "needs internet" alert is TestFlight-only (absent in App Store production) — that specific audio interruption won't hit real users. If symptoms persist on 131 → residual bug, get logs.

**Triage rule:** session-recording freeze/hang/"time from 0" reports → FIRST check installed build number. ≤2.0.57(130) = stale, ship 131. Codemagic auto-versions on dev push ("Pre-release updates" commits = a build was cut); `git show <commit>:mindsync_app/pubspec.yaml | grep ^version:` maps commit→build.
