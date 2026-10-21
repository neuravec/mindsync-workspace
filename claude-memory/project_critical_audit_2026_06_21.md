---
name: project_critical_audit_2026_06_21
description: Global backend+frontend prod-critical audit 2026-06-21 + full code-by-code verification 2026-06-22; report AUDIT_CRITICAL_2026_06_21.md; 55/66 confirmed real, 5 already-fixed, 6 refuted
metadata: 
  node_type: memory
  type: project
  originSessionId: 1ae85807-4619-458b-934d-edd52e6f767d
---

Kompleksowy audyt backendu+frontendu pod krytyczne błędy funkcjonalności (cel: poprawne działanie dla WSZYSTKICH userów na prod). Workflow `mindsync-prod-critical-audit` run `wf_3bad8a4c-b2a`, 21 audytorów → 66 surowych znalezisk.

**WERYFIKACJA KOD-PO-KODZIE 2026-06-22** (workflow `mindsync-audit-verify-all` run `wf_d1bca273-d32`, 66 sceptyków czytało AKTUALNY kod, każdy werdykt cytuje file:line): **55/66 potwierdzone realne** (zrewidowane wagi: 3 critical, 18 high, 26 medium, 8 low), **5 JUŻ NAPRAWIONE na dysku**, **6 obalone**. Werdykty z dowodami: `_audit_verdicts_full.json` + `_audit_verify/F##.json` (repo-root).

**Pełny raport (ZAKTUALIZOWANY o weryfikację): `C:/Users/mikol/Notebooks/MindSync/Heroku/AUDIT_CRITICAL_2026_06_21.md`** — każde znalezisko F01–F66 ze statusem + file:line + fix + kolejność napraw. ŹRÓDŁO PRAWDY, czytaj przed naprawą.

Status: **NAPRAWY W TOKU** (paczkami 2-3; każda: web-research→propozycja→akceptacja→fix+testy→oznaczenie w raporcie sekcja „Fix log"). Nic nie wdrożone (backend root nie-git → edycje plików bez commita; „pending deploy").
**Paczka 1 ZROBIONA 2026-06-22** (on disk, testy zielone, NIEwdrożone): F01 `/conversations/all`+`.filter(user_id)`; F14 backend `users.py:799` `bool(is_active)`; F15 `users.py:805-806` re-raise HTTPException+generyczne 500 bez wycieku `str(e)`. Test `app/tests/test_audit_batch1_fixes.py` 4/4. (Pre-existing unrelated red: test_onboarding_v2::test_preserves_therapy_data — mock, nie moja zmiana.)
**Paczka 2 ZROBIONA 2026-06-22** (frontend, on disk, NIEwdrożone, repo git mindsync-frontend NIE commitowane): F66/F63 `user_info.dart:37` `as bool? ?? false`; F62/F38/F55 `auth_cubit` Google+Apple rozróżnia 404 (nowy user) od transient (rethrow→outer catch błąd, user zostaje zalogowany, NIE onboardowany) — nowy `lib/utils/api_error_utils.dart` `isDefinitive404()`. Email-login (auth_cubit:161-163) już OK, nietknięty. Testy `test/api/user_info_test.dart` 4/4 + `test/utils/api_error_utils_test.dart` 6/6, `flutter analyze` 0. **TIER 0 RDZEŃ ZAMKNIĘTY** (Paczki 1+2, pending deploy). Side-effect: parse-error envelope (F40) też nie udaje „nowego usera"; jawny guard `result['profile']==null` (F40 medium) opcjonalnie później. Następne kandydatki: F01 zrobione; F45/F46 restore, F59 home-spinner, F50/F53 recording.

**🔴 CRITICAL realne (3):** F01 GET /conversations/all leak (conversations.py:122-127); F45 Restore Purchases no-op (subscription_bottom_info.dart:45-48); F62 auth_cubit Google/Apple dumps istniejących OAuth-userów do rejestracji.

**TIER 0 „backend error→onboarding/sign-out" — CZĘŚCIOWO naprawiony:** splash JUŻ rozróżnia 404 vs transient (F30/F31 fixed), ale ścieżka Google/Apple sign-in NADAL podatna (F62 crit, F38/F55 high) + root null-cast: backend users.py:799 zwraca subscription_is_active bez bool() (null gdy brak wiersza sub), FE user_info.dart:37 twardy `as bool` → TypeError (F14/F63/F66); backend owija 404+transient w 400 (users.py:805-806, F15). Fix oba końce + 404-discrimination w auth_cubit (wzór już w therapy_context_manager + naprawionym splashu).

**🟠 HIGH realne (18):** F06 schedule-driven moments zjadają budżet notyfikacji; F14/F15/F38/F55/F66 Tier 0; F18 clinician archived 404 (route shadow); F19 brief enqueuje nieistniejący task→wisi; F20 invite Apple-relay fail+self-cancel; F36 batch-joby bez db.rollback() zatruwają partię; F44 notification_moments.payload JSON-model/TEXT-migracja→500 na PROD (nie SQLite); F46 restore nie do backendu; F47 completePurchase przed weryfikacją; F50 recording v2 OOM ~1.4GB (record_session_cubit:1076-1083); F53 iOS interruptions gubią audio v2; F57 onboarding blank dead-end; F59 home wieczny spinner (main_page_cubit:71-78); F65 MomentType enum bez RE_ENGAGEMENT/unknownValue.

**🛠️ JUŻ NAPRAWIONE na dysku (potwierdzone, NIE ruszać):** F30/F31 splash 404-discrimination; F32 async /complete (worker Whisper/GCS, koniec H12); F51 resume-after-crash union (D6); F52 finish&process→BackgroundUploadCubit (D4).

**❌ OBALONE (NIE ścigać):** F09 legacy crony martwe/niezaschedulowane (nie w scheduler/lifespan/Procfile); F11 score'y append-only; F28 prompt nie free-text (4 stałe <200); F35 brak copy-move (storage_key direct); F54 matcher widzi tylko czysty `HTTP error: <code>`; F56 backend POST/subscription ignoruje status z body + guard → NIE nadpisuje premium.

Motywy: Tier 0 (OAuth path otwarty), deploy≠migrate (F44/F07/F61), SQLite≠Postgres (F44), brak transient-vs-permanent na FE (typed ApiException), money-path bez trwałości (F45-48), recording v2 (F50/F53 zostają).

Powiązane: [[project_postgres_enum_drift]], [[feedback_no_live_api_experiments]], [[project_voice_note_dataloss_fix_2026_06_19]], [[project_general_fixes_2026_06_20]], [[project_session_rec_recovery_fix_2026_06_21]], [[reference_frontend_ci_git_topology]].
