---
name: project-stt-assemblyai-posthog-cleanup-batch-2026-08-04
description: "Batch 2026-08-04 — AssemblyAI-primary STT (short-form notes), ~50 nowych eventów PostHog FE+BE, legacy cleanup BE+FE; KOREKTA 2026-08-10: COMMITTED (bf02d88+a7e5b98) i WDROŻONE na Heroku v528/v529"
metadata: 
  node_type: memory
  type: project
  originSessionId: d529b774-3b11-47a6-8a5d-a6a1a021d170
  modified: 2026-08-04T05:57:11.409Z
---

Batch 2026-08-04 (3 zadania + research), status: ~~UNCOMMITTED~~ **KOREKTA 2026-08-10 (ustalone przy B10 audytu PostHog)**: batch ZOSTAŁ scommitowany (BE: bf02d88 "phog + whisper" + a7e5b98 "lops fix") i jest WDROŻONY na Heroku (v528/v529, potwierdzone heroku releases). UWAGA: `ASSEMBLYAI_API_KEY` NIE jest ustawiony w konfigu Heroku – short-form degraduje bezpiecznie do Whispera, ale legacy single-shot ścieżka nagrań sesji (bez guarda) dostałaby 401; decyzja operatora: ustawić klucz albo wygasić legacy path. Nagrania sesji (chunked) NIGDY nie używają AssemblyAI – zawsze Whisper, stąd diarization_failed=true jest projektowe.

1. **STT**: prep/debrief/between/check-in już od voice notes v2 NIE używały realtimeAPI (Whisper). Zmiana = nowy `app/services/stt_service.py::transcribe_short_form` — AssemblyAI primary (upload→submit→poll, bez diaryzacji) + fallback Whisper; kontrakt `TranscribeResponse{text,model}` bez zmian → zero zmian FE. Revert env-varem `STT_PRIMARY_PROVIDER=whisper`; `STT_ASSEMBLYAI_POLL_TIMEOUT_SECONDS=90`. GDPR: delete_transcript_job enqueue na sukcesie ORAZ na błędzie po submit (fix HIGH-001 z security review). Realtime zostaje tylko w audio chat/reflect.
2. **PostHog**: ~50 eventów FE (workspace, notes, chat, prep capture, lejek voice_transcription_*, signup, consent, account deletion, app tour, journey, paywall_dismissed, notification_permission_*...) w analytics_events.dart + cubity; BE consent_granted/revoked w consent.py. Pominięte (brak UI): note_saved/deleted, journey_day_opened, summary_record_shared, streak_screen_viewed.
3. **Cleanup**: usunięte BE: legacy PUT add-to-agenda (+get_or_create_agenda_pin), triage batch GET/submit (+schematy, enum CONSUMED zostawiony), martwe helpery GCS w session_recordings, health-check submit-voice/quick-check-voice/transcription-session, user_loops_maintenance.py. FE: martwe endpointy/metody (workspace triage, health-check voice, thoughtAudioPath branch), model triage_submit_response. NIE ruszone (żywe/krytyczne): v1 /session-recordings/upload (fallback 503!), notification_interests lazy-migracja, legacy pola prep-card/summary (historyczne rowy), teksty B1/B2 (testy je assertują), alias schedulera RQ. **[[reference-legacy-realtime-key]]: LEGACY_REALTIME_KEY=True nadal w configu — rekomendacja: flip na False na Heroku po potwierdzeniu Androida, potem usunąć kod.**

Testy: BE pełna suita 20 fail = baseline (0 nowych), stt 94/94; FE analyze 144 (=baseline-1), testy touched 129+19 pass. Security: GO po fixie HIGH-001; MED-001 (usunięcie add-to-agenda łamie pre-Fix.1-G buildy) = świadoma decyzja operatora.

Deploy: bez migracji (HEAD zostaje ff7182a3b4c5), code-only; wymagane env na Heroku: nic nowego obowiązkowego (ASSEMBLYAI_API_KEY już jest).

Korekty operatora 2026-08-04: user_loops_maintenance.py PRZYWRÓCONY (wrapper CLI; właściwy sync Loops = tasks/loops_sync.py + cron + /admin/loops/sync, nietknięte). **GPT_AGENT_MODEL zmieniony na Heroku: gpt-realtime-2 → gpt-realtime-mini (v527, 2026-08-04)** — czysta zmiana config vara, kod pomija reasoning dla nie-realtime-2; rollback: config:set z powrotem. Wymagany test głosowy PL.

Research realtime-alternatyw (2026-08): rekomendacja Faza 1 = gpt-realtime-mini ($10/$20 za 1M audio vs $32/$64) + higiena prompt-cache (~65–75% taniej, drop-in); Faza 2 = Gemini Live 3.1 Flash native audio przez LiveKit Agents (~75–85%, WebSocket-only, brak session.update mid-session, Vertex EU dla danych zdrowotnych). Odrzucone: Nova Sonic (brak PL), Hume (PL/US-only), Vapi/Retell/11Labs (nie tańsze).
