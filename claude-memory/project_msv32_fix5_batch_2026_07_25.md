---
name: project-msv32-fix5-batch-2026-07-25
description: "MSV3.2 Fix 5 (QA 24.07) — 4 itemy FE-only COMMITTED dev 095abe7, NIE pushed; root cause iOS save = sync WAV+SHA na UI isolate"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2ede2d04-2022-49dc-8f89-c7b0c8d0923b
  modified: 2026-07-25T06:44:34.974Z
---

# MSV3.2 Fix 5 batch (2026-07-25)

4 itemy ze spec `Business_requirements/MS_3/v3.2.ios/MSV3.2_Fix5.md` — **FE-only, COMMITTED lokalnie dev `095abe7`, NIE pushed. BEZ migracji, backend nietknięty.**

- **CS-01** Threads pill wrap: 2 bugi — (a) shared `threads_section.dart` miał maxLines:2+ellipsis (usunięte), (b) legacy fallback Prep (`unresolvedTopics`/`newDevelopments`) renderował w `Wrap` BEZ ograniczenia szerokości → Column+Flexible. After Therapy ma WŁASNY duplikat `_TopicChip` (`session_card_widget.dart`) — poprawiony osobno, w tym ścieżka share/export. Topics&Questions pille świadomie nietknięte.
- **CS-02** root cause iOS flaky save: składanie WAV (`List<int>.addAll` → ~1GB heap na 75-min sesji) + SHA-256 (pure Dart) SYNCHRONICZNIE na UI isolate → freeze + memory-kill. Fix: `WavBuilder.assembleFromSegments` (pre-sized Uint8List) + `computeFileSha256` przez `compute()`. Cross-platform, bez Platform.isIOS.
- **CS-03** Yieks: x/discard → nowe `discardRecording()` (plik + bookkeeping v1 RecoveryService + v2 Manifest); **scope zawężony po QA HIGH finding**: AppBar-X kasuje TYLKO przy `_isVoiceInputError` — inne błędy (np. `error_networkRecordingSaved` po udanym nagraniu) zachowują nagranie (safe `_safeExit`).
- **CS-04** Recording Found: "Keep it" było NO-OP (martwy loop) → teraz `_handOffToBackgroundUpload` (ten sam pipeline co Finish&Process).

QA: suita 1461 pass / 30 fail = dokładnie baseline, analyze 0 błędów. Werdykt GO po fixie scope'u.

**Otwarte:** (1) device-QA na iPhone wymagane: 10× zapis z rzędu, airplane-mode, x/discard bez pop-outu, Keep-it, Share karty z długim tytułem wątku (ścieżka export bez testów automatycznych!), Android regression check. (2) NIEfiksowane, do decyzji Darka: `CrashSafeRecorder.stop()` bez wewnętrznego timeoutu na natywnym stop — możliwy drugorzędny wkład w CS-02. (3) Testy opcjonalne NA DYSKU, NIEcommitowane (sesja przerwana wyłączeniem komputera): `test/screens/fab_flows/record_session_appbar_close_test.dart` (wiring AppBar-X Yieks vs non-Yieks; run: 2 z 4 testów FAIL — trace wskazuje unhandled async z dart:isolate, prawdopodobnie fire-and-forget discardRecording() po teardownie widgetu; do debugu) i `test/screens/therapy_capture/widgets/prep_card_share_content_test.dart` (share path przez publiczne widgety; prawdopodobnie 2 pass, niepotwierdzone które). NIE commitować bez zielonego runu. Zgłoszony blocker testowalności: legacy fallback share w prep_card_widget (prywatne _buildTopicChip/_buildDevelopmentPill) i cała ścieżka share w session_card_widget (prywatny _TopicChip) — wymaga małego seamu w lib/ (ekstrakcja do publicznych widgetów albo @visibleForTesting). (4) Niecommitowane pliki agent-memory flutter-mobile w tree.

Deploy: tylko push FE dev → Codemagic/TestFlight. Powiązane: [[project-msv32-fix4-batch-2026-07-24]].
