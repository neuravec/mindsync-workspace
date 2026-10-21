---
name: project-gpt-live-1-voice-engine-2026-10-15
description: GPT-Live-1 jako drugi silnik głosowy (Preview) obok Classic realtime; WDROŻONE BE v573 i FE 6821717 na dev 15.10
metadata:
  node_type: memory
  type: project
  originSessionId: 411d28c9-cb2c-48c4-9433-4ef95b60476b
  modified: 2026-10-15T01:55:36.013Z
---

Silnik Live (gpt-live-1, $0,05/min) równolegle do Classic (gpt-realtime-2.1 / 2.1-mini). Przełącznik "Voice engine" w Settings pod "Selected voice", Classic domyślny, Live oznaczony "Preview", zapis per uid lokalnie.

Stan (dowód z 2026-10-15): BE d79c509 wypchnięty na main, Heroku v573, boot czysty, POST /api/v1/audio-v2/live-session i /live-session/{id}/end odpowiadają 403 bez tokenu. FE 6821717 wypchnięty na dev (TestFlight). Branch feat/gpt-live-1 w obu repo, worktree MindSync-live i mindsync-frontend-live. Bez migracji.

Kill switch: Config Var VOICE_LIVE_ENABLED=False wyłącza Live bez deployu (backend zwraca engine=realtime, klient spada na Classic).

Otwarte: pełne flutter analyze nie przeszło lokalnie (brak RAM), Codemagic nie analizuje pusha na dev; device QA (timing tur, opener, moderacja, PL/DE); ewaluacja SAFETY na Live przed szerszym ruchem; tier konta OpenAI; koszt zależy od wywołania /end przez klienta (sideband = trwała naprawa); weryfikacja eventów PostHog po release przez posthog-data-extractor.

Raporty: docs/voice/gpt-live-1-*-2026-10-14.md, db-reports/2026-10-14-voice-realtime-cost-baseline.md. Powiązane: [[project-first-conversation-voice-v2-2026-10-05]].
