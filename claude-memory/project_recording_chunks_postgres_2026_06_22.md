---
name: project_recording_chunks_postgres_2026_06_22
description: "Chunked upload nagrań sesji składuje chunki w POSTGRESIE (transient, Fernet), NIE w GCS — Firebase Storage wymaga płatnego planu. 7-dniowa retencja. COMMITTED LOCAL, czeka na deploy."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6fd6219a-b2a2-4256-b8db-111da9997e78
---

Po włączeniu crash-safe v2 ([[project_session_recording_ungated_2026_06_22]]) upload nagrania sesji padał na `503 {detail: Failed to store chunk to durable storage}`. Przyczyna: **Firebase Storage / GCS wymaga płatnego planu** — bucket `mindsync-8f534.firebasestorage.app` nigdy nie był provisionowany (operator ustawił tylko env var `GCS_BUCKET_NAME`, ale nie utworzył bucketa → zapis 404/fail). Nazwa bucketa była POPRAWNA (potwierdzona w GoogleService-Info.plist/google-services.json/firebase_options.dart), autoryzacja OK (ten sam `FIREBASE_CREDENTIALS` co Firebase Admin) — padał sam zapis do nieistniejącego bucketa.

**Decyzja usera:** nie płacić za Firebase Storage; składować w Postgresie (transient). Audio jest przejściowe — wartością jest transkrypt (tekst). „Tylko lokalnie na kliencie" odrzucone (audio MUSI dojść do AssemblyAI po transkrypt).

**Rozwiązanie (backend-only, klient bez zmian — te same endpointy):**
- Nowa tabela `upload_chunks` (migracja `vv2w3x4y5z0a`, down_revision `uu1v2w3x4y5z`): id, upload_session_id (FK→upload_sessions ON DELETE CASCADE), byte_offset (BigInteger), data (Text = Fernet(base64(bytes))), created_at. Idempotentna (has_table guard), TYLKO bezpieczne typy (String/BigInteger/Text/DateTime, ZERO Enuma — unik pułapki H10). Model `UploadChunk` w `models.py`.
- `session_recordings.py`: `_store_chunk_to_pg`/`_assemble_chunks_from_pg`/`_delete_upload_session_chunks` + `_encode_chunk`/`_decode_chunk` (Fernet). Usunięty gate `_require_gcs_or_503` z initiate/chunk/complete (Postgres zawsze dostępny). Stare GCS helpery zostawione jako dead code. Single-shot `/upload` nadal używa `recording_storage` (best-effort, działa bez GCS).
- Worker (`session_recording.py`): składa chunki **streamem do NamedTemporaryFile** (NIE 140MB do RAM) → AssemblyAI/Whisper → kasuje chunki po transkrypcji.
- **Retencja 7 dni (wymóg usera):** `cleanup_abandoned_upload_sessions` (godzinny job, min 50) = Phase 1 (sesje IN_PROGRESS >7d → ABORTED + kasuj chunki) + Phase 2 NOWE (`crud.delete_stale_upload_chunks` — bulk DELETE KAŻDEGO chunka >7d niezależnie od statusu sesji, domyka osierocone chunki po COMPLETED). Cutoff tz-aware, DB-agnostyczny. Audio nigdy nie żyje >7 dni; transkrypt zostaje.

**Security review (security-guardian): 0 Critical/High, deploy NIE zablokowany.** Zweryfikowane: horizontal-priv (`get_upload_session(id, current_user_id)` filtruje po id I user_id; session_id = UUID v4 → cudza sesja 404), szyfrowanie (Fernet/MESSAGE_ENCRYPTION_KEY, brak plaintextu), GDPR erasure (User DELETE → CASCADE → upload_sessions → upload_chunks), retencja (3 mechanizmy, brak ścieżki >7d), chunki nigdy w odpowiedzi API. Naprawione 3 findingi: MED-001 (`total_bytes` cap `MAX_RECORDING_BYTES`=200MB + 413 na oversized chunk), MED-002 (temp-plik z odszyfrowanym audio kasowany na KAŻDEJ ścieżce błędu), LOW-001 (jawny RuntimeError gdy brak MESSAGE_ENCRYPTION_KEY — diagnozowalny boot zamiast kryptycznego crash-loop). 120 testów (mój własny run).

**+ Route fix push (commit `c2daecf`):** FCM po zakończeniu nagrania („Your session recording summary is ready.") deep-linkował do `/fab/after-therapy` (ekran nagrywania notatki!) zamiast podsumowania → zmienione na `/main-page` (jak `summary_ready`). `_post_success_jobs` odpala TYLKO na ścieżce COMPLETED (AssemblyAI i Whisper).

**Status (2026-06-22): COMMITTED, NIE deployed.** Backend `main`: `8a64d86` (storage+retencja+security, 12 plików) + `c2daecf` (route push→/main-page) JUŻ na origin/main (wypchnęła współbieżna sesja) + `a3b1049` (route key→`session_recording_ready`, P2) LOKALNIE na wierzchu. Repo backendu = `MindSync/` (remoty `heroku` git.heroku.com/mindsync.git + `origin` github neuravec/MindSync). **Deploy operator-gated** (mój `git push origin main` ZABLOKOWANY przez classifier — default branch wymaga zgody usera): `git push heroku main` + `heroku run alembic upgrade head --app mindsync` (OBOWIĄZKOWE — brak release phase; create_all też utworzy tabelę jako siatka, ale odpal migrację dla spójności rewizji) + verify logs + opc. `heroku config:unset GCS_BUCKET_NAME`. ⚠️ GOTCHA: shared git tree — origin/main ma interleaved współbieżne commity „up" (5a7d3b5 = conversations.py/users.py/audit-test z innej sesji; 0c7a111/125735c/5a7d3b5 = inne workstreamy). `git push heroku main` wdroży je RAZEM z moimi — flag dla usera. P2 wymaga OBU: FE route handler (cf8ffa2 na dev) + BE route key (a3b1049); stare buildy degradują na main-page.

**Powiązany pending (FRONTEND, osobny tor):** nav-fix `record_session_flow.dart` (`_safeExit`: pop jak canPop, inaczej `go(mainPage)`) — naprawia uwięziony X na ekranie resume ORAZ processing — na dysku, NIEZACOMMITOWANY, batch; pchnąć na `dev`→TestFlight gdy user skończy rundę testów. Patrz [[feedback_concurrent_session_git_hygiene]], [[feedback_memory_write_after_commit]].
