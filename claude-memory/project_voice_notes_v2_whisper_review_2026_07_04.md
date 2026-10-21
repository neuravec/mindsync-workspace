---
name: project_voice_notes_v2_whisper_review_2026_07_04
description: "Głosówki notatek (prep/debrief/between) przerobione na record→stop→Whisper→edytowalny przegląd→akceptacja; FE PUSHED dev 22cb141, BE 31ddac3 lokalnie (push→operator)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e80f5da0-e4ed-44bb-bc57-8758873b6b93
---

Batch 2026-07-04 (zlecenie Mikołaja, v3): likwidacja live realtime-transkrypcji w notatkach terapeutycznych na rzecz pełnego Whispera po Stop + kroku przeglądu/edycji transkryptu przed przetworzeniem.

- **FE PUSHED `origin/dev` `22cb141`** (29 plików, +3601/−1363): `DebriefCaptureCubit/State/Screen` przepisane — usunięte całe WebRTC (PC/DC/drain/settle; `StopDecision.transcriptFallback` i `shouldKeepDrainingTail` skasowane); **recorder jedynym właścicielem mikrofonu → naprawia iOS AVAudioSession contention (puste M4A)**. Nowe stany: `transcribing` / `transcriptReview` (edytowalny, pre-filled) / `transcriptionFailed` (Retry / Keep-for-later / Delete — audio NIGDY nie kasowane po błędzie). Akceptacja → istniejące endpointy TEKSTOWE (`createText*`, parity pól + triggery MomentsCubit). Audio kasowane WYŁĄCZNIE po potwierdzonym zapisie. Recovery cross-process: pointer `captureRecoveryPointerJson` w SharedPreferences {flowType, audioPath, stage recorded|transcribed, transcript}, `.autosave` co 60s zostaje; banner recovery zlokalizowany (Kontynuuj/Usuń); fail submitu tekstu zachowuje edytowany transkrypt do retry (naprawiony stary residual). 31 nowych kluczy l10n ×7; martwe `error_recordingTooBrief`+`capture_connectingLabel` usunięte. Nowy `AudioV2Manager.transcribe()` + model `TranscriptionResult`.
- **BE `31ddac3` + chore `dad9bb5` COMMITTED lokalnie na `main`** (push=operator): `/audio-v2/transcribe` przyjmuje opcjonalne multipart `feature` (PREP_CARD|DEBRIEF|BETWEEN_SESSION, whitelist lokalny set) → `track_usage(feature,"transcribe_voice_note",user_id)`; brak/nieznane = zachowanie jak dotąd. Endpoint ISTNIAŁ już na prodzie (v515) — **TestFlight działa bez deployu BE** (stary FastAPI ignoruje niezadeklarowane pola form).
- QA GO: BE 4065/21 fail (=baseline; 2 consent-flaki akurat przeszły), FE 1078/30 (=baseline), analyze 0 err, kontrakt FE↔BE zgodny, health_check/reflect/fab_flows/recording_pipeline_v2 zero diff. Uwaga QA: `flutter test` na tej maszynie potrafi CICHO zgubić raport ~15 plików — licz pliki vs katalog, nie ufaj samemu tally.
- **Nietknięte celowo**: `health_check_flow_cubit` (ma własny DUPLIKAT WebRTC — zostaje live), reflect/audio_chat (konwersacje realtime), record_session/recording_pipeline_v2, `RealtimeAPIManager`, `getTranscriptionSession`, endpointy `createVoice*` (nieużywane przez nowy flow, żyją dla starych buildów).
- Wcześniejsze fixy głosówek stają się historią: [[project_voice_note_dataloss_fix_2026_06_19]], [[project_voice_note_too_short_ios_fix_2026_06_22]], [[project_voice_note_tail_drain_fix_2026_06_23]] — ich mechanizmy (drain/settle/transcriptFallback) już nie istnieją w notatkach.

Powiązane: [[project_ms_v3_fix1_fix2_2026_07_03]], [[reference_pre_existing_test_baseline_2026_06_01]]
