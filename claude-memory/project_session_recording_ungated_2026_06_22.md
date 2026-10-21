---
name: project_session_recording_ungated_2026_06_22
description: "Nagrywanie sesji (75-min) nie przeżywało zabicia appki — crash-safe v2 był DORMANT za flagą recording_pipeline_v2, której NIGDY nie stworzono w PostHog. Odpięte od flagi + 2 bugi. COMMITTED+PUSHED."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6fd6219a-b2a2-4256-b8db-111da9997e78
---

Nagrywanie SESJI (75-min, min 10-min, `record_session_cubit.dart` + `lib/services/recording_pipeline_v2/` + splash recovery) — INNE niż notatki głosowe ([[project_voice_note_too_short_ios_fix_2026_06_22]]). Nie przeżywało zabicia aplikacji: przerwanie w trakcie traciło wszystko, brak promptu o wznowieniu przy relaunchu.

**Przyczyna główna:** cały crash-safe pipeline v2 (`CrashSafeRecorder` → segmenty PCM + `RecordingManifest` + splash cold-start recovery z arkuszem 4-opcyjnym: Kontynuuj / Zakończ i przetwórz / Zapisz / Odrzuć) był W PEŁNI ZBUDOWANY ale DORMANT — bramkowany flagą PostHog `recording_pipeline_v2`, której user **NIGDY nie stworzył w PostHog**. `isFeatureEnabled('recording_pipeline_v2')` dla nieistniejącej flagi → false → `_usePipelineV2=false` → zawsze ścieżka v1 (zwykły plik, ZERO zapisu w trakcie) → nie ma czego wznawiać. (Notatki głosowe mają OSOBNY, zawsze-włączony recovery przez pliki `.autosave` — stąd user widział „przechowana" tam, ale nie w sesji.)

**Decyzja usera:** PostHog feature flags = niepotrzebne tarcie dla jego workflow (front i tak idzie na TestFlight→prod). Odpiąć od flagi. Świadomy kompromis: traci zdalny prod kill-switch (mityguje walidacja TestFlight + istniejący fallback single-shot upload na `GcsUnavailableException`).

**Naprawa (frontend-only, 4 pliki; backend już gotowy — GCS set, chunked endpoints live, UploadSession fix v505):**
- `record_session_cubit.dart`: `_usePipelineV2=true` na stałe, usunięte odpytywanie PostHog. + **BUG FIX**: `_startRecordingV2.onSegmentCompleted` NIE dopisywał `segmentPath` do `_activeSession.segmentPaths` (tylko totalBytes) → po zabiciu appki manifest miał `segmentPaths: []` (recovery ratował się tylko diskScanOrphans). Naprawione na wzór `resumeSessionV2`.
- `splash_screen.dart`: `_checkAndOfferRecordingRecoveryDispatch` zawsze odpala v2 recovery (foldery PCM) + v1 prefs-check (legacy pending-upload), bez flagi.
- `recording_manifest.dart`: **BUG FIX (regresja przejściowa)** — `diskScanOrphans` łapał stare pliki płaskie v1 (`pending_upload_*`, `session_recording_*`) → (a) podwójny prompt vs v1 prefs-check, (b) LAWINA starych okien recovery przy 1. uruchomieniu po update (każde przerwane nagranie v1 zostawia osierocony `session_recording_*`, a `_cleanupStaleRecordingFiles` WYŁĄCZONY), (c) „Kontynuuj" na pliku v1 WAV → korupcja (traktowany jak surowy PCM, podwójny nagłówek WAV). Teraz skanuje TYLKO foldery sesji v2 (.pcm). Legalny pending-upload v1 nadal ratuje v1 prefs-path.

**Status: COMMITTED+PUSHED 2026-06-22** — commit `05db043` na `origin/dev` (rebase na auto-version bump Codemagica `fb465c2 "Pre-release updates"` — push voice-note triggerował auto-versioning; rebase czysty, zero przecięcia). 4 pliki, JAWNIE stage'owane. `flutter analyze` 0 błędów, **60/60** testów `recording_pipeline_v2`. → Codemagic→TestFlight.

**Why:** User uznał za krytyczne, że 50-min sesja terapii ma przeżyć wyłączenie telefonu/appki/internetu — to baseline, nie eksperyment za flagą.

**How to apply:** **v2 NIGDY nie działał na żywo** (flaga nie istniała) — to PIERWSZA aktywacja. Zostaje QA na urządzeniu (TestFlight) 3 scenariuszy PRZED promocją do App Store: (1) zabicie appki w trakcie → splash recovery → „Kontynuuj" → dograj → Stop → ma złożyć CAŁOŚĆ (pre-kill+post-resume) i wysłać; (2) Stop ≥10min → chunked upload → przetwarzanie → gotowe; (3) brak internetu → stan błędu/wstrzymania (nie ciche zniknięcie) → włącz sieć → wznawia. Ekran Debug Logs (ikona robaka na ekranie nagrywania) dla diagnostyki on-device. Flaga `recording_pipeline_v2` jest teraz martwa dla ścieżki nagrywania — NIE wprowadzaj ponownie zależności od flagi. v1 zostawione jako dead code/fallback (łatwy revert). Patrz [[project_recording_pipeline_v2_phase_a]], [[project_general_fixes_2026_06_20]], [[project_session_rec_recovery_fix_2026_06_21]], [[feedback_concurrent_session_git_hygiene]], [[feedback_memory_write_after_commit]].
