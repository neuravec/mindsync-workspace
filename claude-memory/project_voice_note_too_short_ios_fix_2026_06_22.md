---
name: project_voice_note_too_short_ios_fix_2026_06_22
description: "Voice notes (between/prep/debrief) falsely \"too short\" on iOS — REGRESJA z fixu 06-19; naprawione przez wybór źródła treści (transkrypt jako fallback). COMMITTED+PUSHED."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6fd6219a-b2a2-4256-b8db-111da9997e78
---

Notatki głosowe (między sesjami / przygotowanie / po terapii) — wszystkie 3 to JEDEN wspólny `DebriefCaptureCubit` (`CaptureFlowType.debrief|prepCard|betweenSession`) + live transkrypcja przez WebRTC Realtime API. Na iOS po realnym (długim) nagraniu klik Zapisz dawał „za krótka" (`error_recordingTooBrief`) **automatem na KAŻDYM nagraniu**.

**Przyczyna główna (skorygowana diagnoza):** to REGRESJA wprowadzona przez [[project_voice_note_dataloss_fix_2026_06_19]]. Na iOS równoległa sesja WebRTC `getUserMedia` (live transkrypt) **wygrywa walkę o współdzieloną AVAudioSession** i zagładza pakiet `record` → plik M4A zostaje pusty (~28 bajtów ftyp). Live transkrypt DZIAŁA (user potwierdził: tekst się pojawia), ale plik audio jest pusty. Fix z 06-19 przełączył werdykt „za krótka" na **liczony z rozmiaru pliku** — więc skoro M4A na iOS jest zawsze pusty, „za krótka" leciało zawsze. Fix 06-19 leczył objaw (zła diagnoza: zakładał że plik jest OK, a tylko gating po transkrypcie był zły). Stary (działający) przepływ przed 06-19 wysyłał **tekst z live transkryptu** — to jedyne, co realnie łapie dźwięk na iOS.

**Naprawa (frontend-only, zachowuje live transkrypt, zero zmian backendu):** w `lib/screens/debrief_capture/cubit/debrief_capture_cubit.dart`:
- `decideStopOutcome` wybiera ŹRÓDŁO TREŚCI (priorytet): realny M4A ≥ kMinUsefulBytes(2048) → upload głosowy (Android, serwer Whisper); inaczej niepusty transkrypt (≥5 znaków) → `transcriptFallback` = wyślij przez ISTNIEJĄCY endpoint tekstowy (`createText*`, iOS); inaczej null/0-bajt → `noAudio`; inaczej → `tooShort`. Komunikat zmieniony na uczciwy `error_noAudioHeard`.
- **Transkrypt wygrywa nad null/0-bajtowym/małym plikiem** (`hasTranscript` sprawdzany PRZED noAudio/tooShort) — nigdy nie gubi wypowiedzi usera.
- **Settle-before-decide:** w gałęzi bez audio czeka na bounded `_settleTranscription()` (≤_kStopSettleMs=1200ms) PRZED werdyktem, żeby ostatni fragment VAD zdążył dojść (domyka stary edge case „Stop tuż po ostatnim zdaniu").
- `_submitTextContent(String)` wydzielony z `submitText`, reużyty w fallbacku (zachowane triggery MomentsCubit).

**Status: COMMITTED+PUSHED 2026-06-22** — commit `2e64e36` na `origin/dev` (repo `mindsync-frontend/`, branch dev → Codemagic→TestFlight). 17/17 testów `debrief_capture_decision_test.dart` (zweryfikowane osobiście, nie tylko agent), `flutter analyze` czysty. Staged JAWNIE tylko 2 pliki (cubit+test). **Zostaje: QA na urządzeniu iOS (TestFlight)** — potwierdzić że długie nagranie z widocznym transkryptem zapisuje się jako notatka.

**Why:** Krytyczny bug — userzy w aplikacji zdrowia psychicznego mówili 5 min i tracili notatkę. Drugi raz „naprawiany" (06-19 źle), więc diagnoza musiała być twarda, kod-po-kodzie, a nie ufanie pamięci.

**How to apply:** Notatki głosowe na iOS zapisują teraz treść z **live transkryptu** (gpt-4o-mini-transcribe), nie z serwerowego Whispera na pełnym audio — świadomy kompromis (audio na iOS i tak puste). Gdyby kiedyś chcieć serwerowy Whisper na iOS → trzeba rozwiązać kontencję o AVAudioSession (zrezygnować z równoległego WebRTC na iOS) — wtedy wraca decyzja UX o live transkrypcie. Residua (nieblokujące): (1) nieudany upload fallbacku tekstowego (błąd sieci) nie retainuje transkryptu do retry jak głosowy `uploadFailed`; (2) martwy klucz ARB `error_recordingTooBrief`. Pakiet `record` używa `AudioEncoder.aacLc` na iOS (NIE WAV jak `record_session_cubit`) — celowo nietknięte, bo plik i tak pusty (WebRTC wygrywa); WAV miałby sens dopiero gdyby `record` był jedynym właścicielem mikrofonu. Patrz [[feedback_memory_write_after_commit]], [[feedback_concurrent_session_git_hygiene]].
