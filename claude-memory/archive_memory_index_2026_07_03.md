# MindSync Project Memory

## References
- [Business agents track + growth-analyst](project_business_agents_track_2026_06_28.md) — new business-agent track started 2026-06-28; growth-analyst (Opus, read-only PostHog+Postgres+revenue → reports in analytics-reports/) for churn/monetization/retention "why" questions
- [competitive-strategist agent](project_competitive_strategist_agent_2026_06_28.md) — 2nd business agent (2026-06-28); Opus, read-only competitor/market intel (Ahrefs+app-store reviews+web) → light-pivot strategy reports in competitive-reports/; framing: mature product + ~3-4 subs ⇒ fix positioning/distribution not features
- [Broadcast push notification](reference_broadcast_push.md) — POST /admin/broadcast, RQ worker, auto-cleans invalid tokens
- [PostHog integration](reference_posthog_integration.md) — Flutter + FastAPI analytics, session replay, feature flags, config
- [PostHog access method](reference_posthog_access_method.md) — MCP OAuth NIE działa w tym env (invalid_scope→No OAuth flow); fallback: read-only HogQL przez REST query API z POSTHOG_PERSONAL_API_KEY z MindSync/.env (proj 141170 EU); $app_version tylko na client-eventach
- [Play Console access + Android internal testing](reference_play_console_access.md) — dev/app IDs, opt-in link, tester list "MindSync Internal", submit_as_draft flip c26353c (2026-07-03); NO Android-only path (app-release = iOS+Android)
- [database-administrator agent](reference_database_administrator_agent.md) — nowy agent (2026-06-29) do prod Postgres: read-only audyty/diagnostyka, drift schematu/enumów, stan migracji; KLUCZOWE: Azure DB nieosiągalny lokalnie (brak DNS) → dostęp przez `heroku run -a mindsync python < REPL-safe_script.py` → `heroku ps:stop run.NNNN`; nie owns modeli/migracji (backend-api)
- [Post-update analysis 2026-06-29](project_post_update_analysis_2026_06_29.md) — update 2.0.60 (27.06) niemierzalny po 2d (publiczność na 2.0.44, nowy build=testerzy, brak granicy before/after); nic się nie pali; 🔴 recording v2 funnel gap (tylko chunked_upload_completed); re-run ~07-07 z app_version split
- [Onboarding extra fields UNFILLED 2026-06-29](project_onboarding_extra_fields_unfilled_2026_06_29.md) — prod Postgres dowód: age_band 3/1718, currently_in_therapy 0, lead_source 5 (gender 77.8% ale legacy); 🔴 smoking gun: age_band w payloadzie dla ~93 ale null w bazie = kandydat na buga zapisu profilu (FE/BE); jak odpytać prod: heroku run python < REPL-safe script
- [PostHog dashboards](reference_posthog_dashboards.md) — 9 dashboards + 50 insights provisioned 2026-04-23, idempotent script at scripts/posthog_build_dashboards.py
- [PostHog GDPR person delete](reference_posthog_gdpr_delete.md) — POST /persons/bulk_delete/ (NIE DELETE /persons/?distinct_id=, ten 403); enqueue do RQ żeby nie blokować request thread
- [Next Wave plan v3](reference_next_wave_plan_v3.md) — 5 WOW funkcji + PR #0 notification budget, zatwierdzony 2026-04-21 po 3 rundach DA
- [Codemagic CI/CD setup](reference_codemagic_setup.md) — stan setupu Codemagic, co user musi zrobić w UI, follow-ups (humm SHA pin, ASC rename)
- [Frontend CI/git topology](reference_frontend_ci_git_topology.md) — repo frontu = mindsync-frontend/ (NIE root Heroku); dev=główny branch→push triggeruje Codemagic→TestFlight; CI odpala tylko `flutter pub get` (commituj codegen freezed/g.dart/l10n); synthetic-package:false → ARB bez gen-l10n = stale S class blokuje testy; FE-only wydania niezależne od backendu, stare apki żyją tygodniami → backend additive-only
- [Xcode 26 / Flutter 3.41.1 migration](project_xcode26_migration_2026_04_30.md) — ITMS-90725 fix; branch chore/xcode26-flutter341; deploy target 16.0
- [gpt-realtime-2 migration 2026-05-12](project_gpt_realtime_2_migration_2026_05_12.md) — drop-in swap; cost-neutral; PR-2 (whisper STT) REJECTED as 5.67× more expensive
- [Voice config backend-driven 2026-05-12](project_voice_config_backend_driven_2026_05_12.md) — backend returns client_session_config blob; FE consumes; reasoning_effort conditional for gpt-realtime-2+; fixed AppCubit registerFactory bug
- [Notification Moments redesign 2026-05-14](project_notification_moments_redesign_2026_05_14.md) — 2 systemy (push moments + in-app pop-upy), hybrid AI/templated, hard cutover legacy, Faza 2 start: 1 push + 2 pop-upy; P0 bugi już naprawione
- [Notification Moments SHIPPED 2026-05-15](project_notification_moments_shipped_2026_05_15.md) — wszystkie 4 fazy w prod, ~695 testów, orchestrator/detector framework, 4 push generators + 5 detectors, adaptive scoring, Settings V2 (master+intensity+6 interests)
- [Clinician portal integration 2026-05-15](project_clinician_portal_integration_2026_05_15.md) — therapist-deck spięty end-to-end z app; admin endpoint do tworzenia kont; deployment operator-gated (env vary + Loops + migracja)
- [Therapist Deck V2 2026-05-18](project_therapist_deck_v2_2026_05_18.md) — full-stack rozbudowa portalu (Pulpit, briefy, cele, notatki sesji/głosowe, złota nić); migracja kk1l2m3n4o5p; 2 Critical naprawione; nie wdrożone
- [Character tab redesign 2026-05-18](project_character_tab_redesign_2026_05_18.md) — Pet Hero/Bio/Activity cards z handoffu; single orca level; activity_breakdown + orca_points_in_current_level backend (additive); 41 testów; a11y blockery naprawione; nie wdrożone
- [Stats tab redesign 2026-05-18](project_stats_tab_redesign_2026_05_18.md) — Hero Insight + unified symptom module + single Premium Surface; migracja ll2m3n4o5p6q; GET/POST /stats/* endpoints; hourly hero_insight job; nie wdrożone
- [Re-engagement notifications 2026-05-19](project_re_engagement_notifications_2026_05_19.md) — push dla nieaktywnych userów (3d→7d→stop, progi >=); backend only, brak UI toggle; migracja mm3n4o5p6q7r; cold/warm path; nie wdrożone
- [Scheduler cleanup 2026-05-19](project_scheduler_cleanup_2026_05_19.md) — prod RQ miał 531 jobów (498 dup + 8 ghost); Redis posprzątany NA ŻYWO → 26; idempotency fix w kodzie (clear_all_scheduled_jobs) niewdrożony
- [Personal Bio cost optimization 2026-05-19](project_personal_bio_cost_optimization_2026_05_19.md) — najdroższa operacja AI; data_hash cache + split sekcji + 90d okno + restyle + cooldown; migracja nn4o5p6q7r8s; nie wdrożone
- [Reflect v1.1 redesign 2026-05-23](project_reflect_v1_1_2026_05_23.md) — pixel-perfect DESIGN.md v4 + DOCX produktowe; mint borders, sand sent-from-suggestion z "teraz", FAB pill, DZISIAJ mint chip, status dot always-on; nowy ReflectVoiceBody (flat canvas, blue orb 280dp); auto-title 3→2 + end-trigger + max(0,…) clamp; 8 ARB keys w 7 lang; 74/74 testów; nie wdrożone
- [Onboarding profiling plan 2026-05-27](project_onboarding_profiling_plan_2026_05_27.md) — PLANNED. 4 wave'y: W1 GDPR fix + age band + inclusive gender (5 opt), W2 challenges reframe + behavioral PostHog, W3 Art.9 currently_in_therapy + withdrawal, W4 lead source backend-only. Główne odkrycie: PersonaliseView zbiera gender PRZED Legal Gate = pre-existing GDPR violation.
- [consent_records drift fix 2026-05-29](project_consent_records_drift_fix_2026_05_29.md) — prod alembic DuplicateTable consent_records; migracja pp6q7r8s9t0u uczyniona IDEMPOTENTNĄ (inspector guards), commit 76a5b26 na backend main; migracje na Heroku RĘCZNE (brak release phase) → deploy ≠ migrate.
- [Nine-issue batch fix 2026-06-01](project_nine_issue_fix_2026_06_01.md) — 9 bugów (rejestracja/onboarding UI, reactive state factory→singleton, RE_ENGAGEMENT interest-filter exempt, schedule-driven pre/post-session moments, weekly/monthly on-demand generate); migracja qq7r8s9t0u1v; IMPLEMENTED on disk (brak git), nie wdrożone; operator musi odpalić alembic na Heroku
- [Pre-existing test baseline 2026-06-01](reference_pre_existing_test_baseline_2026_06_01.md) — ~85 testów RED przed jakąkolwiek nową pracą (legacy notif disabled + stale reflect-tab tokens + ConsentManager GetIt gap); nie myl z regresją
- [Onboarding+Home fixes 2026-06-02](project_onboarding_home_fixes_2026_06_02.md) — 5 TestFlight fixów (intensity "Optional" label out, hub-and-spoke FullScreenTextEditor dla journey free-text, custom MsTimePicker numeryczny zamiast natywnego showTimePicker x4, name-empty self-heal: deferred-flush był silent plain-POST → teraz UPSERT+strict-uid+self-heal). Frontend-only, 202/202 testów, analyze 0 err; IMPLEMENTED on disk (brak git), nie wdrożone. Istniejące konta NIE auto-recover (legacy pending bez uid odrzucony dla GDPR) → re-register/re-enter w Account.
- [Login/Welcome M3 redesign 2026-05-28](project_login_welcome_m3_redesign_2026_05_28.md) — PUSHED na origin/dev 2026-05-29 (merge 0fb73ed, redesign w 489389a; 27/27 testów). Welcome+Auth na M3 wg handoffu; ZACHOWANY combined login/signup switcher (nie rozdzielono), social per-platforma (Apple iOS/Google Android, App Store 4.8), nowy m3_auth_field.dart, reused l10n keys; nie wdrożone (push dev może triggerować Codemagic auto-versioning).
- [Voice-note data-loss fix 2026-06-19](project_voice_note_dataloss_fix_2026_06_19.md) — KRYTYCZNY: notatka 3-min ginęła jako "too short" gdy user klikał Stop za szybko (live transcript kasował M4A). Fix frontend-only: zawsze upload pełnego M4A (serwer transkrybuje), too-short z rozmiaru pliku nie z transcriptu, M4A nigdy nie kasowany przed potwierdzonym save, close() finalizuje+backup; +settle-grace 1.2s; +Reflect endCall drain 2.5s final-turn. gen-l10n odblokował testy. analyze 0 err, 19/19 testów. MERGED do dev + PUSHED 2026-06-21: fix commit 6491660 → merge f2d7845 na origin/dev (Codemagic→TestFlight triggered); merge diff = dokładnie 8 plików (concurrent tree — NIGDY git add ., merge robiony w izolowanym worktree). dev = główny branch (origin HEAD). Repo frontu = mindsync-frontend/ (nie root Heroku). Zostaje: QA na urządzeniu/TestFlight, potem sklepy.
- [De-clinicalization l10n+features SHIPPED 2026-06-20](project_declinicalization_l10n_2026_06_20.md) — MDR wording+legal z MINDSY_1.DOC, PUSHED origin/dev: f2a2433 (EN+PL ARB ~150 kluczy + 8 soft presetów Suicidal Ideation/Panic→Low mood/… + regen) + 6541248 (feature: usunięte notif intensity controls + journey frustration chips). gdprConsent "mental health"→"wellbeing" ⚠ prawnik przed release. GOTCHA: 2. sesja (voice [[project_recording_pipeline_v2_phase_a]]) przełączyła branch na fix/voice-note-dataloss W TRAKCIE → mój feature-commit wpadł na ich branch; recovery: isolated worktree cherry-pick→push dev + reset --soft/restore tylko moich 9 plików. NIGDY bulk git add . / sprawdzaj branch przed commitem.
- [Recording pipeline v2 Phase A 2026-06-20](project_recording_pipeline_v2_phase_a.md) — crash-safe PCM segments + WAV assembly + 4-option cold-start recovery; PostHog flag gated; 38 tests; IMPLEMENTED on disk (no git commit yet)
- [General fixes batch 2026-06-20](project_general_fixes_2026_06_20.md) — 3 topics, COMMITTED+PUSHED 2026-06-21: (1) remove notif Intensity FE+BE (orchestrator fixed cap), (2) frustration block out of onboarding Journey, (3) crash-safe recording overhaul Phases A–C + Whisper chunking (GCS durable, resumable chunked upload, reprocess/safety-net, PostHog flag recording_pipeline_v2; runbook). Backend main=commit dcc779d (migrations rr/ss/tt, HEAD=tt0u1v2w3x4y); frontend dev=commit 0e01298 (Topic3 FE; clean cherry-pick); Topic1/2 FE already on dev via 6541248. Rollout (operator-gated): GCS_BUCKET_NAME=mindsync-8f534.firebasestorage.app SET 2026-06-21; NEXT = run `alembic upgrade head` on Heroku + deploy; Tier 2 via PostHog flag recording_pipeline_v2→TestFlight (Standard-2X dyno before ramp).
- [UploadSession boot-crash 2026-06-21](project_upload_session_boot_crash_2026_06_21.md) — H10 crash-loop from status Enum-vs-String + create_all@boot (dcc779d/v501); fix 523946c deployed v505 (verified clean boot). +2 follow-ups SHIPPED 2026-06-21: featureenum HERO_INSIGHT (3222d48→v506, migration uu1v2w3x4y5z run, label verified) + FE splash 503≠onboarding (7043175 on dev→TestFlight)
- [Global critical audit 2026-06-21 + verify 2026-06-22](project_critical_audit_2026_06_21.md) — 66 znalezisk, WSZYSTKIE zweryfikowane kod-po-kodzie: 55 realnych (3 crit F01/F45/F62, 18 high, 26 med, 8 low), 5 JUŻ naprawione na dysku (F30/F31/F32/F51/F52), 6 obalone (F09/F11/F28/F35/F54/F56 NIE ścigać); raport repo-root AUDIT_CRITICAL_2026_06_21.md (F01–F66 ze statusem+fix); AUDIT ONLY nic nie naprawione; Tier 0 OAuth path NADAL otwarty (splash już fixed)
- [Session-rec recovery+comms fix 2026-06-21](project_session_rec_recovery_fix_2026_06_21.md) — cold-start recovery gubił nagranie + zero feedbacku (scen. app-kill/phone-off). BE: async /complete (koniec H12) + nowy safety-net job finalize_complete_upload_sessions (≤15min, idempotent with_for_update) — NO migration. FE: long-lived BackgroundUploadCubit (przeżywa nawigację, fix push-then-go) + pełna lokalizowana warstwa komunikacji (banner progress/saved/offline/failed+retry, 11 ARB×7lang). Security PASS, contract PASS, 4 scenariusze "no silent-loss". **DEPLOYED 2026-06-21** (verified live 06-22): BE v507 (125735c) zdrowy 11h, safety-net `mindsync_upload_finalizer` mieli co 15min "Job OK" na prodzie; FE 6f29e07 na origin/dev (+0a055bb bump)→TestFlight. "up" commity czysto izolowały TYLKO nasze pliki (osobny workstream users.py/auth zostawiony uncommitted). Zostaje: QA na urządzeniu 4 scenariuszy. Runbook MindSync/docs/RUNBOOK_recording_pipeline_fix.md
- [Voice-note "too short" iOS fix 2026-06-22](project_voice_note_too_short_ios_fix_2026_06_22.md) — REGRESJA z fixu 06-19: na iOS WebRTC wygrywa AVAudioSession→M4A pusty→werdykt liczony z rozmiaru pliku dawał "za krótka" ZAWSZE (nawet długie nagranie z widocznym transkryptem). Fix: decideStopOutcome wybiera źródło treści (realny M4A→upload głosowy/Android; inaczej live transkrypt→endpoint tekstowy/iOS; transkrypt wygrywa nad null/0-bajt/małym plikiem; settle-before-decide na ogon VAD). Frontend-only, zachowany live transkrypt, zero backendu. 17/17 testów. COMMITTED+PUSHED `2e64e36` origin/dev→Codemagic/TestFlight; zostaje QA na urządzeniu iOS.
- [Session recording un-gated (crash-safe v2 default) 2026-06-22](project_session_recording_ungated_2026_06_22.md) — nagrywanie SESJI (75-min) nie przeżywało zabicia appki: crash-safe v2 (PCM segments+manifest+splash recovery) był DORMANT za flagą `recording_pipeline_v2`, której NIGDY nie stworzono w PostHog → zawsze v1 (zero zapisu w trakcie). Odpięte od flagi (v2 domyślny, release pipeline=gate, single-shot fallback=net) + 2 bugi: segmentPaths nie dopisywane do manifestu w trakcie; diskScanOrphans łapał stare pliki v1 (podwójny prompt+lawina osieroconych okien+korupcja na „Kontynuuj"). 4 pliki, 60/60 testów, analyze czysty. COMMITTED+PUSHED `05db043` origin/dev (rebase na auto-bump Codemagica `fb465c2`)→TestFlight. v2 PIERWSZY raz na żywo — QA 3 scenariuszy (zabicie/Stop-upload/brak netu) przed App Store. Notatki głosowe niezależne (osobny .autosave recovery). FOLLOW-UPS: nav-fix `record_session_flow.dart` `_safeExit` (X nie wychodził z ekranu resume/processing bo `go()` = unpoppable root) — NIEZACOMMITOWANY frontend, batch.
- [Recording chunks → Postgres (nie GCS) 2026-06-22](project_recording_chunks_postgres_2026_06_22.md) — upload nagrania padał `503 Failed to store chunk to durable storage` bo Firebase Storage = płatny plan (bucket nie provisionowany). User: składuj w Postgresie. Chunki w `upload_chunks` (Fernet-encrypted, transient), te same endpointy → klient bez zmian; migracja `vv2w3x4y5z0a` (idempotentna, bezpieczne typy); worker streamuje do temp-pliku→AssemblyAI→kasuje; retencja 7 dni (Phase 2 hard purge); security 0 Critical/High (+3 findingi naprawione: total_bytes cap 200MB, temp-file cleanup, encode_service boot guard); route fix push→/main-page. 120 testów. backend `main` `8a64d86`+`c2daecf`(origin/main)+`a3b1049`(local, route key P2), NIE deployed — operator-gated: `git push heroku main` + `heroku run alembic upgrade head --app mindsync` (⚠ shared tree: deploy obejmie też współbieżne „up" commity 5a7d3b5 conversations/users z innej sesji).
- [Session-recording processing/nav/deep-link fixes 2026-06-22](project_recording_chunks_postgres_2026_06_22.md) — FRONTEND batch PUSHED `cf8ffa2` origin/dev→TestFlight (5 fixów z testów na urządzeniu): (1) zacięte „Transcribing" na zawsze — root cause z LOGÓW: iOS zamraża dartowe `Timer.periodic` w tle, więc nagranie kończone w tle nigdy nie domykało ekranu → fix: poll od razu + re-poll na app-resume (WidgetsBindingObserver w cubicie, removeObserver w close/completed/failed), interwał 20s→10s; (2) honest „Processing…" zamiast zawsze-„Transcribing" (klamrowanie indexOf→0); (3) nav dead-end: `_safeExit` (canPop?pop:go(main)) na ekranie resume+processing — INNA SESJA zacommitowała identyczny fix jako „up" e3d562d, rebase scalił czysto; (4) P2 deep-link push→therapy timeline (`/main-page/tab/:tab`+MainNavCubit.selectTab, route key `session_recording_ready`); case-insensitive status (defensywny, nie był przyczyną). 10/10 testów poll-resume (agent NIE odpalił testów — padały na GetIt DioColient, złapałem własnym runem). Repo frontu shared tree — rebase na auto-bump Codemagica + cudzy „up". (5) BACKGROUND RECORDING regresja z un-gatingu v2: `CrashSafeRecorder` NIE konfigurował `AVAudioSession` (v1 `_configureAndStartRecorder` ustawiał `playAndRecord`+allowBluetooth/defaultToSpeaker/duckOthers/spokenAudio) → iOS usypiał appkę przy screen-lock/app-switch → pauza. Info.plist już miał `audio` UIBackgroundMode. Fix `27807da`→rebase `4af9db5` origin/dev→TestFlight: wydzielony `_configureIosAudioSessionForBackground()` wołany w OBU wejściach v2 (`_startRecordingV2`+`resumeSessionV2`) przed `_crashSafeRecorder.start()`; v1 deleguje; interruptions (telefon) pauzują/wznawiają v2 przez istniejące handlery. 5-min segment-roll: stop/restart silnika NIE deaktywuje sesji (do potwierdzenia on-device). analyze 0, 10/10 testów. ZOSTAJE: QA tła na urządzeniu. (6) KRYTYCZNY z logów `c08243a`→TestFlight: po pauzie→wznowieniu Save WISIAŁ + audio gubione, bo v2 odpalał ZASZŁY health-check v1: `resumeRecording` startował `_startHealthCheckTimer`, `_performHealthCheck` monitorował `_recordingPath` (nieużywany WAV v1 = 0 bajtów w v2, bo PCM idzie do segmentów) → fałszywy „dead" → `_attemptRecorderRestart` restartował CUBIT'owy `_recorder` v1 (inny instance niż w CrashSafeRecorder) → walka o iOS audio HW → PCM zagłodzone → `_stopRecordingV2` wisiał na `stop()`. Fix: (a) v2 nigdy nie odpala health-check/restart v1 (usunięte z resume + guard `if(_usePipelineV2)return` w obu); (b) `stop().timeout(5s)` + składanie z trwałych segmentów PCM (manifest+disk scan) → Save zawsze kończy; (c) `_isStopping` guard (3× tap robił 3 stopy); (d) interruption auto-resume w v2 (było tylko pause/duck → zostawało spauzowane); (e) próg 10min = max(PCM-bytes/32000, _elapsed) bo Dart timer zamarza w tle. 15/15 testów. PCM crash-safe = nagranie z nieudanego testu odzyskiwalne przez splash recovery przy next launch.
- [Voice-note tail-drain fix 2026-06-23](project_voice_note_tail_drain_fix_2026_06_23.md) — głosówka (debrief/prep/between, jeden cubit) gubiła notatkę gdy user gadał długo CIĄGIEM i od razu klikał Save ("nothing recorded"); talk→pauza→czekaj-na-tekst→Save działało. Root cause: end-of-rec grace `_kStopSettleMs=1200ms` za krótki + wychodził na PIERWSZYM chunku; iOS M4A pusty (WebRTC wins AVAudioSession) więc transcript=jedyna treść, a semantic_vad transkrybuje ogon 2–5s. Fix frontend-only (Path B only): nowy `_drainTailTranscript()` smart bounded (8s hard cap / 1.5s quiet-after-growth, CZEKA gdy transcript pusty), pure `shouldKeepDrainingTail`; Path A (M4A/Android upload) + `decideStopOutcome` nietknięte; spinner już widoczny więc czekanie niewidoczne. 31/31 testów, analyze clean. IMPLEMENTED on disk, NIE committed — zostaje QA iOS 3 scen. + commit 2 plików.
- [Session-rec stale-build triage 2026-06-23](project_session_rec_stale_build_triage_2026_06_23.md) — zgłoszenie freeze/hang/„czas od 0" nagrywania SESJI = STARA paczka TestFlight (≤2.0.57/130), NIE bug w kodzie. Logi `health check: file size = 0 bytes`→`attempting recorder restart`→`stopRecordingV2 stopping` ×4 = v1-health-check-restart-w-v2, już naprawiony przez `c08243a`; fizycznie niemożliwy na origin/dev (guard `if(_usePipelineV2)return` przed logiem L868, stop timeout 5s L1158, per-segment manifest L1100-1114). PIERWSZA paczka z fixem = **2.0.58 (131)**. Triage rule: freeze nagrywania sesji → najpierw sprawdź numer builda; ≤130=stale→131. Codemagic auto-version: `git show <c>:mindsync_app/pubspec.yaml|grep ^version:`.
- [Session-rec timer+pause fix 2026-06-24](project_session_rec_timer_pause_fix_2026_06_24.md) — v2 nagrywanie sesji: (A) licznik zamarzał w tle (iOS suspenduje Dart `Timer.periodic`; 22min realnie→608s) bo `_elapsed+=1s` co tyk; (B) Pauza wisiała/UI nie reagował (await natywnego `_recorder.pause()` PRZED cancel+emit → 21 tapnięć w 10s w logu). Fix frontend-only: wall-clock `computeElapsed(now−start−pauzy)` + anchor `_recordingStartedAt` (recovery: now−PCM-estimate) + foreground snap w `didChangeAppLifecycleState`; pauza/resume UI-first + idempotency guard + `unawaited(pause/resume)`; `CrashSafeRecorder` `.timeout(2s)` (flaga `_isPaused` i tak odcina audio). Nietknięte: capture/AVAudioSession/foreground/health-check/stop/Fix5/v1. 27/27 testów, analyze clean, lead zweryfikował diff. IMPLEMENTED on disk, NIE committed; zostaje QA iOS 3 scen. Drobiazg: v1 path nie ustawia `_recordingStartedAt` (martwy kod, prod=v2).

- [MS_3 batch 33 poprawek + TestFlight-first strategy 2026-07-02](project_ms3_batch_2026_07_02.md) - FE 3464457 dev->TestFlight + BE 4c2579a origin/main PUSHED; Heroku deploy PENDING approval; strategia docs/RELEASE_STRATEGY_TESTFLIGHT_FIRST.md + LEGACY_CLEANUP_MS3.md (Faza 2 rejestr); flagi: brak UI logowania objawow, /me/goals mismatch
- [Notification Cadence v3 2026-07-03](project_notification_cadence_v3_2026_07_03.md) — framework momentów NIGDY nie wysłał pusha (rejestracja generatorów tylko w web dyno → worker=pusty rejestr); fix wiring + sloty 2/dzień (DAILY_CHECK_IN/REFLECTION_INVITATION baseline) + SESSION_MORNING_OF + fix time_zone + wycięte legacy (7 setup_*, flaga, 7 notify_*); migracja ww3x4y5z0a1b; FE 895713d PUSHED dev; BE 2621868 COMMITTED lokalnie (push origin/main DENIED przez classifier) → operator: push + heroku deploy + alembic

## Process & Feedback
- [Concurrent-session git hygiene](feedback_concurrent_session_git_hygiene.md) — wiele sesji agentów w JEDNYM drzewie git frontu; sprawdzaj branch przed commitem (`git rev-parse --abbrev-ref HEAD`), staguj TYLKO swoje pliki jawnie (NIGDY `git add .`/`-a`), `git diff --cached --name-only` przed commitem; merge/build w izolowanym `git worktree` żeby nie ruszać cudzej niezacommitowanej pracy. Bity 2× (voice-note + de-clin).
- [Account deletion fix + e2e_local skill 2026-06-08](project_account_deletion_fix_2026_06_08.md) — hero_insights backref nullify 500'd deletion; code-only fix; new manually-invoked e2e_local skill statically audits User-FK cascade safety
- [Chrome tool = JS-only in this env](feedback_chrome_tool_js_only_env.md) — claude-in-chrome screenshot/read_page/clicks all timeout on document_idle (even example.com); drive pages via javascript_tool only; synthetic clicks do routing but NOT trusted-gesture dialogs
- [No live API experiments](feedback_no_live_api_experiments.md) — test API migrations offline before production
- [Voice pipeline status](project_voice_pipeline_status.md) — current state of voice features (2026-03-26)
- [intl version pinning](feedback_intl_version_pinning.md) — match flutter_localizations of active SDK; current pin ^0.20.2 (Flutter 3.41.1, since 2026-04-30 Xcode 26 migration)
- [Whisper fallback needs 75-min update](project_whisper_session_recording_update.md) — session recording raised to 75 min 2026-04-22, Whisper fallback still single-shot (25MB limit), needs chunking in future session
- [Legal gate iPhone 17 bug](project_legal_gate_bug_2026_04_24.md) — scroll-gate blokuje Continue na małych viewportach; plan: remove gate (Fix 1)
- [Postgres enum drift](project_postgres_enum_drift.md) — prod ma UPPERCASE labels, migracje deklarują lowercase; raw SQL musi używać uppercase, fresh DB jest złamany
- [FastAPI exception handler gotcha](feedback_fastapi_exception_handler.md) — `@app.exception_handler(Exception)` NIE łapie HTTPException/RequestValidationError; rejestruj dedykowane handlery + zasady PostHog dla `endpoint` property
- [Memory write after commit, not before](feedback_memory_write_after_commit.md) — F1-F5 onboarding fix 2026-04-29: memory said "IMPLEMENTED" gdy realnie 0 plików w git. Status: PLANNED/IN_PROGRESS/COMMITTED/MERGED/DEPLOYED — promote po dowodzie, nie po zamiarze.

## Project Structure
- Backend: `MindSync/app/` — FastAPI, Python 3.12.2, SQLAlchemy (sync), Pydantic v2, RQ/RQ-Scheduler
- Frontend: `mindsync-frontend/mindsync_app/lib/` — Flutter 3.41.1, BLoC/Cubit, Freezed, GetIt, Dio
- Alembic migrations: `MindSync/alembic/versions/`
- Latest migration chain (VERIFIED single head 2026-06-25): ... → `qq7r8s9t0u1v` (THERAPY_PREP, 2026-06-01) → rr/ss/tt (general_fixes 06-20) → `uu1v2w3x4y5z` (featureenum HERO_INSIGHT) → `vv2w3x4y5z0a` (add `upload_chunks` table — recording chunks→Postgres) = **HEAD**. Backend `MindSync/` IS its own git repo (branch `main`, HEAD a3b1049). Heroku migracje RĘCZNE (deploy≠migrate, brak release phase): `heroku run alembic upgrade head --app mindsync`; weryfikacja `alembic current`→`vv2w3x4y5z0a`. Bez tej migracji ZAPIS NAGRANIA pada (brak `upload_chunks` → „503/coś poszło nie tak"). Head-detection gotcha: pliki mieszają `revision = "x"` i `revision: str = "x"` — licz oba style. Migration files: `MindSync/alembic/versions/`.
- Prod DB drift: prefer IDEMPOTENT migrations (inspector existence guards) — prod has orphaned tables/enum drift. Migrations MANUAL on Heroku (no `release` phase in Procfile) — deploy ≠ migrate.
- Migration gotcha: new migrations MUST set `down_revision` to the current single head, not an old already-merged revision (caused multiple-heads error 2026-05-19, fixed by re-parenting `ll2m3n4o5p6q`)

## Key Patterns
- SQLAlchemy: **synchronous** sessions throughout (SessionLocal, not AsyncSession)
- Auth: Firebase token via `deps.get_current_user` — NO dummy bypass (removed)
- Premium gate: returns HTTP 403 (not 401) for non-premium users
- RQ jobs: registered in `rq_scheduler_setup.py`, called from `main.py` lifespan
- Flutter models: Freezed + json_serializable — run `build_runner` after model changes
- Flutter `intl` package: pinned by flutter_localizations of active Flutter SDK (current ^0.20.2 for Flutter 3.41.1) — see feedback_intl_version_pinning.md
- Flutter state: Cubit (not full BLoC with events) — initial → loading → loaded/error

## Features Implemented (2026-03-05)
### Full App Localization — 7 Languages
- Framework: `flutter gen-l10n` with output class `S`, `synthetic-package: false`, output in `lib/l10n/generated/`
- Config: `mindsync_app/l10n.yaml`
- Languages: English (en), German (de), French (fr), Norwegian Bokmål (nb), Swedish (sv), Spanish (es), Polish (pl)
- ARB files: `lib/l10n/app_{en,de,fr,nb,sv,es,pl}.arb` — 929 string keys each
- Generated: `lib/l10n/generated/app_localizations.dart` (S class, 929 getters/methods)
- New files: `lib/core/locale/supported_locale.dart` (7-entry enum: code, nativeName, backendName), `locale_cubit.dart` (Cubit<Locale>, persists to SharedPreferences), `l10n_extensions.dart` (context.l10n shortcut)
- `SupportedLocale` replaces old `Language` class entirely — used in settings_state.dart (Freezed), settings_cubit.dart, language_selection.dart, settings_body.dart
- `LocaleCubit` registered as lazySingleton in service_locator, provided at top-level MultiBlocProvider in main.dart
- `mind_sync_app.dart`: wrapped with `BlocBuilder<LocaleCubit, Locale>`, S.delegate added, locale property set
- `preference_keys.dart`: added `appLocaleCode` (String)
- `shared_preferences_manager.dart`: added `getLocaleCode()` / `saveLocaleCode()`
- Single language setting controls both UI locale AND backend `ai_language` (via `SupportedLocale.backendName`)
- `intl` upgraded to `^0.20.2` for flutter_localizations compatibility
- String extraction: ~90 Dart files modified, all hardcoded English replaced with `S.of(context).key`
- ARB key convention: camelCase with domain prefix (settings_, mainTab_, therapy_, capture_, healthCheck_, recording_, stats_, character_, subscription_, auth_, onboarding_, chat_, account_, legal_, notes_, walkthrough_, app_, common_, nav_)
- Cubit error messages (BotToast without BuildContext) left as English — future work
- Legal body text (Privacy Policy, Terms of Service paragraphs) left as English — requires professional translation
- `ms_common_strings.dart` static consts left unchanged, ARB entries added as `common_*` for future migration
- flutter analyze: 0 errors
- No backend changes required


### 7/30/90 Day Snapshots (Batch 5, Feature #15)
- Migration `u1p2q3r4s5t6`: creates `period_snapshots` table with UniqueConstraint(user_id, period_type)
- Model: `PeriodSnapshot` — period_type (7d/30d/90d), session_count, realization_count, top_topics (encrypted JSON), symptom_directions (encrypted JSON), overall_symptom_direction (7d), relationship_trend (encrypted, 90d), narrative (encrypted AI), is_activated, limited_data, data_hash, data_window_start/end, processing_status
- Schemas: SnapshotTopicItem, SnapshotSymptomDirection, PeriodSnapshotResponse (premium_locked computed at endpoint), AllSnapshotsResponse
- CRUD: create/get/get_by_type/get_all/update/upsert_period_snapshot, compute_snapshot_metrics (session count from debriefs, realization count, top topics from debriefs+notes+recordings+conv_topics, symptom directions with overall for 7d, relationship trend from health checks for 90d, activation thresholds, data_hash SHA-256)
- Activation thresholds: 7d=any data point, 30d=7 days of tracking, 90d=30 days of tracking
- AI: SnapshotNarrativeResult, generate_snapshot_narrative() via gpt_structured (GPT_MODEL_41_MINI), 3 distinct focus prompts (7d=this week, 30d=trends, 90d=arcs), under 50 words
- Config: PERIOD_SNAPSHOT_PROMPT
- Background job: `app/tasks/period_snapshots.py` — hourly cron, 10 PM local, therapy schedule alignment via _should_generate_today, data_hash cache skip, upsert pattern (one row per user per period), retry once on AI failure
- Endpoints: `/api/v1/snapshots/` (3: GET all, GET /{period}, POST /{period}/refresh) — refresh uses data_hash cache
- Premium gating: 7d=free, 30d/90d=premium (403 on refresh, narrative=None + premium_locked=True on GET)
- Rolling windows: always last 7/30/90 days from now, no history archive, overwritten on each refresh
- Flutter: 4 Freezed models (SnapshotTopicItem, SnapshotSymptomDirection, PeriodSnapshotModel, AllSnapshotsResponse), SnapshotManager (3 methods)
- Flutter: SnapshotsCubit (lazy singleton, loadSnapshots + refreshSnapshot per period), SnapshotsState (loading/loaded/error)
- Flutter: SnapshotsSection rewrite — 3 vertically stacked _SnapshotCard widgets, collapsible (collapsed=metrics, expanded=+narrative), color hierarchy (7d=aquaBreeze, 30d=#5BA4CF, 90d=deepOcean), premium lock banner, inactive/empty states, share as JPG via CardShareUtil
- Flutter: ShareCardConfig.snapshot() factory added
- Tests: 77 backend tests (all pass) — schemas, CRUD, compute_snapshot_metrics (22 tests: activation, directions, topics, hashing, limited_data), endpoints, premium gating, background job, AI
- 100% additive, existing flows untouched

## Features Implemented (2026-03-04)
### Character Tab (Batch 5, Feature #18)
- Migration `s9n0o1p2q3r4`: creates `personal_bios` + `user_leveling` tables, adds `orca_name` to `user_preferences`, migrates tone archetypes (supportive→friend, direct→realist, gentle→sage, analytical→explorer, encouraging→coach)
- Models: `PersonalBio` (5 encrypted sections: progress/patterns/drivers/style/outlook, tone_archetype_used, processing_status), `UserLeveling` (dual-track points, 5 activity counters)
- Schemas: PersonalBioResponse, LevelingResponse, InteractionStatsPeriod/Response, CharacterCardResponse, OrcaNameUpdate, ToneArchetypeUpdate
- CRUD: compute_level, points_to_next_level, get_orca_visual_stage, award_user_track_points, award_orca_track_points (daily symptom cap 3), compute_orca_happiness (0/1/2/3 days → 0.0/0.33/0.67/1.0), get_weekly_interaction_stats, backfill_user_leveling (lazy on first visit), personal bio CRUD
- Leveling: 10 levels each track, thresholds [0,11,31,61,101,161,241,341,461,601], ocean-themed titles
- Point hooks: debrief=3, recording=3 (user track); between_session_note=1, reflect=2, symptom=1, realization=2 (orca track) — fire-and-forget try/except in 6 endpoint files
- Endpoints: `/api/v1/gamification/` (4: GET character_card, PUT orca_name, PUT tone_archetype, POST character_card/refresh_bio)
- AI: PersonalBioResult, generate_personal_bio() via gpt_structured (GPT_MODEL_41_MINI), crisis safety override, previous bio continuity
- Background job: `app/tasks/personal_bio.py` — hourly cron, 10 PM local, therapy schedule, 6h duplicate guard, 14-day data window, retry once
- Config: PERSONAL_BIO_PROMPT
- Flutter: 4 Freezed models (CharacterCard/PersonalBio/Leveling/InteractionStats), CharacterManager (4 methods)
- Flutter: CharacterTabCubit rewrite (typed state with CharacterCardModel), level-up detection via SharedPreferences
- Flutter: 5 widget sections (OrcaCompanionSection, DualLevelingSection, PersonalBioSection, InteractionStatsSection, BioShareView)
- Flutter: AnimatedOrca enhanced with stage (baby/juvenile/adult → scale) + happiness (0-1 → animation intensity + sparkle glow)
- Flutter: Settings character_section.dart — orca name field + 5 archetype cards (realist/coach/friend/sage/explorer)
- Flutter: Onboarding "Meet Your Companion" step (4th page) — baby orca, name field, archetype picker, skippable
- Flutter: Bio JPG export via BrandedShareWrapper pattern
- Tests: 97 backend tests (all pass) — schemas, CRUD, endpoints, AI, background job, archetype migration, leveling thresholds
- Flutter analyze: 0 errors/warnings
- 100% additive, existing flows untouched

## Features Implemented (2026-03-03)
### Therapy Tracking Signal (Batch 5, Feature #11)
- Migration `q7l8m9n0o1p2`: creates `therapy_tracking_signals` table, adds `THERAPY_TRACKING` to `RAGSourceEnum`
- Model: `TherapyTrackingSignal` — signal (green/amber/red), label, explanation (encrypted, premium-only), data_window_start/end, data_hash, limited_data, is_early_signal, is_stale, input_summary (encrypted), processing_status
- Schemas: `TherapyTrackingSignalResponse` with `premium_locked` (computed at endpoint, not stored)
- CRUD: create/get/get_latest/update + `compute_therapy_tracking_inputs()` (gathers 4 categories: symptom trends, realizations, topics, capture counts + data_hash) + `compute_deterministic_signal()` (pure scoring: max 13 points → green ≥9, amber ≥5, red <5)
- AI: `TherapyTrackingSignalResult`, `generate_therapy_tracking_explanation()` via `gpt_structured()` with `GPT_MODEL_41_MINI` — AI only generates explanation text, signal is deterministic
- Config: `THERAPY_TRACKING_SIGNAL_PROMPT`
- Background job: `app/tasks/therapy_tracking_signal.py` — hourly cron, 10 PM local check, therapy schedule logic (_should_generate_today), data_hash cache (skip if unchanged), retry once on AI failure, error isolation per user
- Endpoints: `/api/v1/therapy-tracking/` (3: GET latest, GET /{id}, POST /refresh) — refresh uses data_hash cache to skip AI when data unchanged
- Premium gating: free users see signal+label, explanation=None + premium_locked=True
- No FCM notification (weekly summary is sufficient), no RAG indexing (derived signal)
- Flutter: `TherapyTrackingModel` (Freezed), `TherapyTrackingManager` (3 methods: getLatestSignal, getSignal, refreshSignal)
- Flutter: `TherapyTrackingSection` in Stats tab — colored circle + label, explanation (premium) or lock banner (free), refresh button, info bottom sheet (GREEN/AMBER/RED explanations), badges (early/stale/limited), shimmer loading
- Flutter: `TherapyTrackingCompactWidget` in Main tab — dot + label + chevron, tap → Stats tab
- Flutter: StatsTabCubit + MainTabCubit updated with therapyTrackingSignal state + parallel fetch
- Tests: 48 tests in test_therapy_tracking_signal.py (all pass) — schemas, CRUD, deterministic scoring, background job, endpoints, AI
- 100% additive, existing flows untouched

## Features Implemented (2026-03-02)
### Therapy Timeline (Filtered Feed)
- Migration `n4i5j6k7l8m9`: adds `deleted_at` to `session_debriefs` + `between_session_notes`
- CRUD: `soft_delete_session_debrief/between_session_note`, `restore_*`, `get_deleted_timeline_items`, `purge_expired_soft_deletes`, `get_timeline_page` (cursor pagination across 5 types)
- All existing list/count/context functions now filter `deleted_at IS NULL`
- Schemas: `TimelineItem`, `TimelineResponse`, `DeletedItemsResponse`; `DebriefResponse`/`BetweenSessionNoteResponse` gain `deleted_at`
- Endpoint: `/api/v1/timeline/` (GET paginated, GET deleted, POST delete, POST restore) — registered in api.py
- Background job: `purge_expired_soft_deletes` hourly at :30, cleans rows + RAG docs older than 24h
- Tests: 51 tests in test_timeline.py (all pass)
- Flutter: `TimelineItemModel`/`TimelineResponse`/`DeletedItemsResponse` (Freezed), `TimelineManager` (4 methods)
- Flutter: TherapyTabCubit refactored — single `TimelineManager.getTimeline()` replaces 5-manager parallel fetch, cursor pagination via `loadMore()`, soft-delete/restore methods
- Flutter: 8 filter chips in `Wrap` (Monthly disabled "Coming soon"), dot rail with colored dots + vertical line, date grouping headers
- Flutter: Unified `_TimelineCard` for all 5 types, long-press delete (debrief/between_session only), tap → detail via per-type manager fetch
- Flutter: `RecentlyDeletedScreen` with muted cards, countdown, restore button
- Flutter: Per-filter empty states with warm messaging, `_NewEntryPill` animated indicator
- Flutter: Infinite scroll (ScrollController, 200px threshold, batches of 20)
- `intl` upgraded to ^0.20.2 for flutter_localizations compatibility
- build_runner: 136 outputs, flutter analyze: 0 errors/warnings
- 100% additive, existing flows untouched

### Post-Session Nudge Notifications (Batch 2, Feature #16)
- Migration `l2g3h4i5j6k7`: creates `post_session_nudges` table with UniqueConstraint(user_id, session_date)
- Model: `PostSessionNudge` — id, user_id, session_date, first_nudge_text, followup_nudge_text, first_nudge_sent_at, followup_sent_at, suppressed, created_at
- Schemas: Updated `NotificationPreferencesUpdate/Response` with `post_session_nudge` (bool, default True) + `post_session_nudge_delay_minutes` (int, default 30, validated 15/30/60)
- Schemas: Added `therapist_name: Optional[str] = None` to `TherapyScheduleEntry`
- CRUD: create/get/update post_session_nudge, has_debrief_for_session (suppression check)
- AI: `NudgeNotification` Pydantic structure, `_generate_nudge_text()` in notification_service.py — uses gpt_structured with GPT_MODEL_41_MINI, context: therapy_context + pronouns + open_threads + therapist_name
- Config: `POST_SESSION_NUDGE_PROMPT`, `POST_SESSION_NUDGE_FOLLOWUP_PROMPT`
- Fallbacks: `FALLBACK_NUDGE_FIRST`, `FALLBACK_NUDGE_FOLLOWUP` — used when AI fails or no context
- Background job: `notify_post_session_nudge()` — hourly cron, two phases: (1) first nudges for sessions in last 26h, (2) follow-ups for nudges sent 23-25h ago
- Timing: session_start + 60min (assumed duration) + user_delay (15/30/60, default 30) = nudge fire time
- Suppression: checks `has_debrief_for_session()` before both first nudge and follow-up
- Max 2 notifications per session (UniqueConstraint + followup_sent_at check)
- FCM: `send_fcm_message_v1` extended with optional `data` payload for deep-linking
- Scheduler: `setup_hourly_post_session_nudge()` in rq_scheduler_setup.py, registered in main.py lifespan
- Free for all users (no premium gate, no UserSubscription join)
- Flutter: `notifPostSessionNudge` + `postSessionNudgeDelayMinutes` in settings state
- Flutter: Toggle + `_PostSessionNudgeDelayPicker` (AnimatedCrossFade, 3 segmented buttons) in notifications_section.dart
- Flutter: Deep-link routing — `_handleNotificationRoute()` via GoRouter for background/cold-start notifications
- Flutter: `pendingNotificationRoute` for cold-start deep-links, consumed in splash_screen.dart after auth
- Flutter: `_showInAppNudgeBanner()` — BotToast banner with "Later"/"Capture" buttons, 5s auto-dismiss
- Flutter: Android `session_reminders` notification channel
- Flutter: Analytics events: `notificationNudgeTapped`, `notificationNudgeDismissed`
- Flutter: OS notification permission detection via FirebaseMessaging.getNotificationSettings(), amber warning banner + per-toggle warning icon, lifecycle observer auto-rechecks on resume
- Model: `therapist_name` column on PostSessionNudge for follow-up personalization
- AI context: session day/time passed to prompt, tone archetype guidance in both prompt templates
- FCM data payload: includes therapist_name + session_date for deep-link context
- Tests: 42 tests in test_post_session_nudge.py (all pass) — timing, schemas, AI, suppression, follow-up, DND, error isolation, FCM payload, archetype prompts
- 100% additive, existing flows untouched

### Between Sessions Notes
- Migration `k1f2g3h4i5j6`: creates `between_session_notes` table, adds `BETWEEN_SESSION` to `RAGSourceEnum`
- Model: `BetweenSessionNote` — id, user_id, input_type (VOICE/TEXT), raw_text (encrypted), topic (encrypted), summary (encrypted), emotional_tone_internal (encrypted, NEVER exposed in API), guiding_questions (plain JSON), processing_status, created_at, updated_at, xp_awarded
- Schemas: BetweenSessionNoteCreateText, BetweenSessionNoteUpdate (topic+summary only, raw_text NOT editable), BetweenSessionNoteResponse (NO emotional_tone_internal)
- CRUD: 6 new functions (create/get/list/latest/update/recent_for_context) + updated count_ai_notes_this_month (shared limit), has_user_activity_since, gather_weekly_summary_data
- Endpoints: `/api/v1/between-sessions/` (8: guiding-questions, create text, voice, list, latest, get, update, retry)
- AI: `BetweenSessionNoteResult(topic, summary, emotional_tone_internal)`, `generate_between_session_guiding_questions()` (GPT_MODEL_41_MINI), `generate_between_session_note()` (GPT_MODEL, receives recent_topic_labels for label consistency)
- Config: `BETWEEN_SESSION_GUIDING_QUESTIONS_PROMPT`, `BETWEEN_SESSION_NOTE_PROMPT`
- RAG: `index_between_session_to_rag()` — COMPLETED combines topic+summary+emotional_tone, PLAIN_TEXT indexes raw_text; backfill updated
- Helpers: `get_recent_between_session_dicts()`, `get_recent_topic_labels()` in _therapy_helpers.py
- Router: registered in api.py with try/except ImportError pattern
- Flutter: `BetweenSessionModel` + `BetweenSessionGuidingQuestionsResponse` (Freezed), `BetweenSessionManager` (8 methods), endpoints in dio_settings, DI registered
- Flutter: `CaptureFlowConfig.betweenSession()` — "Capture a Thought" title, reuses generic TherapyCaptureScreen + DebriefCaptureCubit
- Flutter: DebriefCaptureCubit extended with betweenSession cases (loadGuidingQuestions, submitText, submitVoice, retry)
- Flutter: `TimelineBetweenSession` variant in therapy_timeline_item, 5-way parallel fetch in therapy_tab_cubit, `TherapyFilter.between` works
- Flutter: `_BetweenSessionTimelineCard` — amber/orange theme, lightbulb icon, "Between Sessions" badge
- Flutter: `BetweenSessionNoteWidget` — topic (editable), summary (editable), transcript (collapsible, read-only), share as JPG, processing/failed/plain_text states
- Flutter: `between_sessions_flow.dart` replaced placeholder with full capture flow
- Free tier: shared AI note limit (debriefs + prep cards + between-session notes), plain text fallback with RAG indexing
- Tests: 47 tests in test_between_sessions.py (all pass) — security, schemas, AI functions, response helpers
- 100% additive, existing flows untouched

### Self-Assessed Symptom Tracking (Batch 3, Feature #8)
- Migration `j0e1f2g3h4i5`: creates `user_symptoms` table + `symptom_scores` table, adds `SYMPTOM_TRACKING` to `RAGSourceEnum`
- Model: `UserSymptom` — id, user_id, name, is_custom, display_order, ai_description (encrypted), ai_description_generated_at, last_score_id_at_generation, created_at, updated_at. UniqueConstraint(user_id, name)
- Model: `SymptomScore` — id, symptom_id (FK CASCADE), user_id (FK CASCADE), score (1-10), created_at. Indexed on (symptom_id, created_at) and (user_id, created_at)
- Schemas: SymptomCreate, SymptomUpdate, SymptomScoreCreate/Response, SymptomResponse, SymptomCardResponse, SymptomTrendItem/Response, SymptomDescriptionRefreshResponse, SymptomReorderRequest
- CRUD: create/get/list/update/delete symptoms, add_score, get_scores, get_latest, reorder, description staleness check, count_today (gamification cap), sync_from_onboarding, trend_data, scores_in_window
- Endpoints: `/api/v1/symptoms/` (11 endpoints: list, create, update, delete, add score, get scores, refresh-description, refresh-all-descriptions, trend, share-data, reorder)
- AI: `generate_symptom_description()` in openai_service.py — uses gpt_function with GPT_MODEL_41_MINI, factual one-sentence descriptions, no diagnosis/interpretation
- Config: `SYMPTOM_DESCRIPTION_PROMPT`, `SYMPTOM_INTERACTION_POINTS_DAILY_CAP=3`
- RAG: `index_symptom_data_to_rag()` in rag_indexing.py — aggregates all user symptoms as single RAG doc (source_id=0), backfill updated
- Weekly summary: `gather_weekly_summary_data()` enriched with `symptom_scores` key, `has_user_activity_since()` includes symptom scores
- Onboarding hook: `PUT /users/therapy-context` now calls `sync_symptoms_from_onboarding()` to create UserSymptom + SymptomScore records from focus_areas + severity_ratings
- Description caching: `is_symptom_description_stale()` checks last_score_id_at_generation vs latest score — avoids unnecessary AI calls
- Gamification: count_symptom_scores_today counts user-wide, capped at 3/day (XP award hook ready but not wired to user_xp table)
- Flutter: 5 Freezed models in `lib/api/models/symptom/` (SymptomModel, SymptomCardModel, SymptomScoreModel, SymptomTrendModel/Response, SymptomDescriptionRefresh)
- Flutter: `SymptomManager` (11 API methods), `SymptomTrackingCubit` (loadSymptoms, updateScore, refreshDescription, refreshAllDescriptions, addSymptom, removeSymptom, renameSymptom, getShareData)
- Flutter: `SymptomTrackingSection` — full symptom cards with sliders (1-10, auto-save on release), Syncfusion LineSeries charts (fixed Y 1-10, teal accent, dot markers, tooltips), AI description (gray italic + per-card refresh), 90-day default + "Show all" toggle, single-dot ScatterSeries for 1 data point
- Flutter: `SymptomTrendWidget` — Main tab compact view with name/score/direction arrow/CustomPainter sparkline, hidden when empty, navigates to Stats
- Flutter: `SymptomsSection` — Settings: preset chips (Depression/Anxiety/Relationships/Trauma/Self-esteem/Burnout/Grief) + "Other" free-text, X delete with micro-confirmation, inline rename, backend-synced via SymptomManager
- Flutter: `SymptomShareView` — offscreen widget for JPG export: all symptoms stacked, charts + AI descriptions, "Self-assessed data from MindSync" footer, date header
- Free for all users (no premium gate), 100% additive, existing flows untouched
- Deferred: offline score queue (cloud-first), XP awarding (cap counting ready)

### Session Recording + AI Summary
- Migration `i9d0e1f2g3h4`: creates `session_recordings` table, adds `recording_consent_given` to `user_preferences`, adds `SESSION_RECORDING` to `RAGSourceEnum`
- Model: `SessionRecording` — 7 encrypted summary sections (overview, topics_with_timestamps, therapist_observations, patient_insights, action_items, emotional_arc, unresolved_topics) + fallback fields (diarization_failed, key_moments, audio_quality_warning) + transcript_text (encrypted, NEVER exposed)
- Schemas: `RecordingTopicTimestamp`, `SessionRecordingResponse`, `RecordingStatusResponse`, `RecordingTrialResponse`
- CRUD: create/get/list/latest/update/count_completed + consent helpers
- Endpoints: `/api/v1/session-recordings/` (7: upload, trial-status, status/{id}, list, latest, get/{id}, retry/{id}) + `GET/PUT /users/recording-consent`
- AssemblyAI service: `app/services/assemblyai_service.py` — upload, submit transcription with diarization, poll, format, quality check, delete
- Background job: `app/tasks/session_recording.py` — on-demand RQ job (30min timeout): transcribe → summarize → encrypt → notify → RAG index → delete audio
- AI: `RecordingSummaryResult` + `generate_recording_summary()` in openai_service.py — diarization-aware (7 sections if reliable, key_moments fallback if not)
- RAG: `index_session_recording_to_rag()` in rag_indexing.py, backfill updated
- Config: `ASSEMBLYAI_API_KEY`, `SESSION_RECORDING_SUMMARY_PROMPT`, `FREE_TIER_RECORDING_LIMIT=2`
- Weekly summary integration: `gather_weekly_summary_data()` and `has_user_activity_since()` include recordings
- Flutter: `RecordingModel`/`RecordingStatusModel`/`RecordingTrialModel` (Freezed), `RecordingManager` (8 API methods + consent), endpoints in `dio_settings.dart`, DI registered
- Flutter: `RecordSessionCubit` (11 states: loading→consentWall→quickConfirm→ready→recording→tooShort/uploading→processing→completed/premiumRequired/error)
- Flutter: `RecordSessionFlow` — full-screen recording flow with consent wall, active recording (timer+pause+wakelock), upload progress, processing stages, premium upsell
- Flutter: `TimelineRecording` sealed class variant, cubit fetches 4 types in parallel, `TherapyFilter.recordings` filter, `_RecordingTimelineCard` (teal theme, mic icon)
- Flutter: `RecordingSummaryWidget` — 7-section read-only card, diarization fallback, audio quality warning, share as JPG, retry for failed
- Free tier: 2 completed recordings lifetime, then premium only. 10+ min minimum duration
- Privacy: audio auto-deleted from AssemblyAI after processing, transcript never exposed in API

## Features Implemented (2026-03-01)
### Weekly Therapy Summary (Batch 4, Feature #5)
- Migration `h8c9d0e1f2g3`: creates `weekly_therapy_summaries` table, adds `notification_preferences` column to `user_preferences`, adds `WEEKLY_THERAPY_SUMMARY` to `RAGSourceEnum`
- Model: `WeeklyTherapySummary` — 5 encrypted sections (at_a_glance, themes_and_patterns, symptom_shifts, key_insights, open_threads) + limited_data flag + data_window_start/end + processing_status
- Schemas: `ThemeItem(theme, explanation)`, `WeeklyTherapySummaryResponse`, `WeeklyTherapySummaryUpdate`, `NotificationPreferencesUpdate/Response`
- CRUD: create/get/list/latest/update for summaries, `has_user_activity_since()`, `gather_weekly_summary_data()`, notification prefs CRUD
- Endpoints: `/api/v1/weekly-summaries/` (5: list, latest, get, update, retry) + `GET/PUT /users/notification-preferences`
- AI: `WeeklyTherapySummaryResult` Pydantic model, `WEEKLY_THERAPY_SUMMARY_PROMPT`, `generate_weekly_therapy_summary()` via `gpt_structured()`
- Background job: `app/tasks/weekly_therapy_summary.py` — hourly cron, 10 PM local check, therapy schedule parsing, Sunday fallback, zero-activity skip, duplicate guard (2h), FCM notification (respects `weekly_summary` preference), RAG indexing (fire-and-forget)
- RAG: `index_weekly_therapy_summary_to_rag()` in `rag_indexing.py`, backfill updated
- Config: `WEEKLY_THERAPY_SUMMARY_PROMPT` in `config.py`
- Flutter: `WeeklySummaryModel`/`ThemeItem` (Freezed), `WeeklySummaryManager` (5 methods), endpoints in `dio_settings.dart`, DI in `service_locator.dart`
- Flutter: `TimelineWeeklySummary` sealed class variant, cubit fetches 3 types in parallel, `TherapyFilter.summaries` works, `_WeeklySummaryTimelineCard` green card in timeline
- Flutter: `WeeklySummaryWidget` — 5 editable sections (text editor, list editor, theme-pair editor), share as JPG, limited data banner, processing/failed/retry states
- Flutter: Notification prefs persistence — `settings_cubit.dart` loads from backend on init, fire-and-forget sync on toggle
- Free for all users (no premium gate), edits overwrite original (no version history)
- Chart removal deferred to separate task

### AI Reflection Chat (Reflect Tab Rebuild)
- Migration `g7b8c9d0e1f2`: adds `ConversationTypeEnum` (JOURNAL/REFLECT), `RAGSourceEnum`, `rag_documents` table, 4 new `conversations` columns
- New models: `RAGDocument` (encrypted chunks + 1536-dim embeddings), `ConversationTypeEnum`, `RAGSourceEnum`
- New columns on `Conversation`: `conversation_type` (server_default="JOURNAL"), `title`, `last_message_preview`, `last_message_at`
- Config: `REFLECT_SYSTEM_MESSAGE`, `REFLECT_STARTERS_PROMPT`, `REFLECT_AUTO_TITLE_PROMPT`, `REFLECT_MONTHLY_MESSAGE_LIMIT=30`, `REFLECT_NUDGE_MINUTES=15`
- CRUD: `count_reflect_messages_this_month`, `find_similar_rag_documents`, `find_similar_combined`, `get_reflect_threads`, `upsert_rag_document`
- Endpoints: `/api/v1/reflect/*` (10 endpoints: start, starters, usage, threads, message, messages, end, session_data, audio user/agent)
- Schemas: `ReflectThreadListItem`, `ReflectThreadListResponse`, `ReflectSendMessage`, `ReflectMessageResponse`, `ReflectStartersResponse`, `ReflectUsageResponse`
- AI: `generate_reflect_starters()`, `generate_reflect_auto_title()` in openai_service.py (GPT_MODEL_41_MINI)
- RAG indexing: `app/tasks/rag_indexing.py` — 5 indexing functions + `backfill_rag_documents()`
- RAG hooks: fire-and-forget enqueues in debriefs.py, prep_cards.py, conversation_analysis.py, periodic_summary.py (daily/weekly/monthly/yearly)
- Background job: `auto_title_reflect_thread()` in `app/tasks/reflect.py` — after 3rd user message
- `close_all_notes.py`: filters out REFLECT conversations from nightly auto-close
- Free tier: 30 USER messages/month, premium gate on voice mode (session_data)
- Token windowing: 50k threshold → rolling summary + last 8 messages
- Flutter: ReflectChatCubit (4 states: threadsLoading, threadsLoaded, chatActive, error)
- Flutter: ReflectManager (10 API methods), 3 Freezed models (ReflectThread, ReflectMessageResponse, ReflectUsage)
- Flutter: ReflectTabScreen rewrite — two-view (thread list ↔ chat), 6 widgets
- Flutter: DI updated — ReflectChatCubit replaces ReflectConversationsCubit
- Production safety: 100% additive, all new columns nullable or server_default, existing JOURNAL flow untouched

## Features Implemented (2026-02-22 to 2026-02-28) — See `features_feb.md` for full details
- **Pre-Session Prep Card** (Feb 28): migration `f6a7b8c9d0e1`, `/api/v1/prep-cards/*` (8 endpoints), `count_ai_notes_this_month` shared limit, `CaptureFlowConfig` pattern
- **Therapy Context Onboarding** (Feb 26): migration `d4e5f6a7b8c9`, `user_therapy_context` table, `{THERAPY_CONTEXT}` in system prompt
- **Therapy Companion + Character Card 2.0** (Feb 22): `therapy_sessions`/`user_xp`/`user_character_stats` tables, XP system, `/api/v1/therapy/*`

## Security Notes
- `TherapySessionResponse` does NOT include `user_id` (GDPR data minimisation)
- Therapeutic alliance reasoning text is NOT logged (only score at DEBUG level)
- Character stats debug log does NOT include stat values
- `scheduled_at` validated: max 1 year past, 2 years future

## Flutter Contract Notes
- session_state enum: UPCOMING | PREP | DEBRIEF | PAST (4 values)
- emotion direction: "up" | "down" | "neutral" (3 values)
- emotional_delta: up to 4 items
- In locked card state: xp IS populated, radar_stats/therapeutic_alliance/emotional_delta/computed_at are null
- DELETE /therapy/sessions/{id} returns 204 No Content — no body parsing
