# MindSync — Production-Critical Functionality Audit

> **Cel:** poprawne działanie aplikacji dla **wszystkich** użytkowników na produkcji.
> **Audyt:** 2026-06-21 — 21 audytorów high-effort przeczytało realny kod → 66 surowych znalezisk.
> **Weryfikacja kod-po-kodzie:** 2026-06-22 — **każde z 66 znalezisk** sprawdzone przez niezależnego sceptyka czytającego AKTUALNY kod na dysku (workflow `wf_d1bca273-d32`, 66 agentów, 4.3M tokenów, każdy werdykt cytuje konkretne linie).

## Wynik weryfikacji (2026-06-22)

| Status | Liczba | Co znaczy |
|---|---|---|
| ✅ **CONFIRMED / PARTLY** (realne) | **55 / 66** | bug obecny w kodzie + osiągalny przez realnego usera |
| 🛠️ **ALREADY FIXED on disk** | 5 | ostatnie fixy już to naprawiły (sceptyk potwierdził w kodzie) |
| ❌ **REFUTED** (nierealne) | 6 | premisa fałszywa / nieosiągalne / niefunkcjonalne |

**55 realnych wg ZWERYFIKOWANEJ wagi:** 🔴 **3 critical** · 🟠 **18 high** · 🟡 **26 medium** · ⚪ **8 low**.

Każde znalezisko ma ID `F01`–`F66` (pełny opis + dowód: `_audit_verify/F##.json` + `_audit_verdicts_full.json`). Wagi poniżej to **zrewidowane** wagi po weryfikacji (część audytorów przeszacowała w obie strony).

## 🔧 Fix log (postęp napraw)

> Kadencja: web-research najlepszych praktyk → propozycja (problem+rozwiązanie) → akceptacja → naprawa+testy → oznaczenie tutaj. Backend root (Heroku) nie jest repo git → edycje plików, bez commita; status „pending deploy" = na dysku + testy zielone, niewdrożone.

| Data | ID | Status | Zmiana | Testy |
|---|---|---|---|---|
| 2026-06-22 | **F01** | ✅ FIXED (pending deploy) | `conversations.py:127` — dodany `.filter(Conversation.user_id == current_user_id)` | `test_audit_batch1_fixes.py` 4/4 |
| 2026-06-22 | **F14** | ✅ FIXED (pending deploy) | `users.py:799` — `bool(is_active)` (nigdy null) | ↑ |
| 2026-06-22 | **F15** | ✅ FIXED (pending deploy) | `users.py:805-806` — re-raise `HTTPException`, generyczne 500 bez wycieku `str(e)`, log z tracebackiem | ↑ |
| 2026-06-22 | **F66 / F63** | ✅ FIXED (pending deploy) | `user_info.dart:37` — `as bool? ?? false` (null→false, brak crashu) | `test/api/user_info_test.dart` 4/4 |
| 2026-06-22 | **F62 / F38 / F55** | ✅ FIXED (pending deploy) | `auth_cubit.dart` Google+Apple: nowy util `isDefinitive404` → tylko 404 = nowy user; transient → `rethrow` (outer catch pokazuje błąd, user zostaje zalogowany, nie onboardowany). Nowy `lib/utils/api_error_utils.dart` | `test/utils/api_error_utils_test.dart` 6/6 + `flutter analyze` 0 |

**Tier 0 — rdzeń ZAMKNIĘTY (Paczki 1+2, pending deploy):** backend zwraca realny bool + poprawne 404/500 (F14/F15); FE parsuje null-safe (F66/F63) i rozróżnia 404 vs transient w OAuth (F62/F38/F55). Splash był już naprawiony (F30/F31). Efekt uboczny: parse-error envelope (F40) też nie udaje już „nowego usera". Pozostaje opcjonalnie jawny guard `result['profile']==null` (F40, medium) — do rozważenia w późniejszej paczce.

---

## TL;DR — kolejność napraw

1. **TIER 0 — „backend error → onboarding/sign-out" (F62 crit, F14/F38/F55/F66 high, F15/F40/F63 med).** Splash JUŻ naprawiony (404-discrimination), ale **ścieżka Google/Apple sign-in nadal wyrzuca istniejących userów do rejestracji** + backend nadal zwraca null `subscription_is_active` i owija wszystko w 400. Najwyższy priorytet.
2. **F01 (crit) — `GET /conversations/all` leak** konwersacji wszystkich userów. Jedna linia fixu.
3. **F45/F46 (crit/high) — Restore Purchases martwy + restore nie trafia do backendu.** Płacący po reinstalacji bez premium + ryzyko odrzucenia w App Store.
4. **F59 (high) — home wieczny spinner** bez retry przy przejściowym błędzie.
5. **F50 (high) — recording v2 OOM** na długiej sesji (utrata nagrania); **F53 (high) — iOS interruptions** gubią audio. (F51/F52 recovery JUŻ naprawione.)
6. **Backend prod-only:** F44 (JSON/TEXT 500), F36 (batch-joby bez rollback), F18/F19/F20 (clinician), F06 (notyfikacje).

---

## TIER 0 — „backend error czytany jako nowy user → onboarding/sign-out"

**Status: ✅ RDZEŃ ZAMKNIĘTY (Paczki 1+2, 2026-06-22, pending deploy).** Splash (F30/F31) był już fixed; w tej sesji: backend `bool()`+poprawne 404/500 (F14/F15), FE null-safe parse (F66/F63), OAuth 404-discrimination (F62/F38/F55). Zostaje opcjonalny jawny guard `result['profile']==null` (F40, medium).

**Wciąż podatne (zweryfikowane w kodzie):**
- **F62 🔴 CONFIRMED critical** — `auth_cubit.dart:228/241-251 (Google), 307/320-330 (Apple)`: bare `catch(e)` po `getUserProfile()` routuje KAŻDY wyjątek do `singUpRoute, isUserFromGoogleOrApple:'true'`. Backend `users.py:805-806` owija nawet własne 404 w `HTTPException(400, str(e))`, więc klient nie może rozróżnić. Istniejący OAuth-user podczas blipu → rejestracja.
- **F38 / F55 🟠 high** — ta sama ścieżka Google/Apple (potwierdzona; splash-połowa F38 już fixed, OAuth-połowa NIE).
- **F14 / F63 / F66 · ✅ FIXED 2026-06-22** — `users.py:799` → `bool(is_active)` (Paczka 1) + `user_info.dart:37` → `as bool? ?? false` (Paczka 2). Crash parsowania wyeliminowany na obu końcach.
- **F15 🟡 medium** — `users.py:805-806` konwertuje 404 i transient na 400 + wycieka `str(e)`.

**Już niegroźne:** **F56 ❌ REFUTED** — re-rejestracja NIE nadpisuje subskrypcji: backend `POST /subscription` ignoruje pola statusu z body, a `_create_initial_subscription` ma guard istnienia (`# nie nadpisuj`). Więc misrouting nie kasuje premium (sama utrata sesji/UX zostaje).

**Fix (oba końce):** backend — `bool(is_active)`, nie owijać 404/HTTPException w 400, nie wyciekać `str(e)`; FE — `as bool? ?? false` + w `auth_cubit` rozróżniać 404 (→rejestracja) od 5xx/timeout/parse (→retry, keep signed-in). Wzór już istnieje w `therapy_context_manager.getTherapyContext()` (sprawdza `statusCode==404`) i w naprawionym splashu — skopiować do auth_cubit.

---

## ✅ CONFIRMED — 🔴 CRITICAL (3)

- **F01 · ✅ FIXED 2026-06-22 · `GET /conversations/all` zwraca konwersacje WSZYSTKICH userów** — `conversations.py:122-127`: `return db.query(models.Conversation).all()` bez filtra; `current_user_id` wstrzyknięty, nieużyty (każdy inny handler filtruje). Każdy zalogowany user dostaje id+status konwersacji wszystkich (cross-tenant, GDPR). **Fix wprowadzony:** dodany `.filter(models.Conversation.user_id == current_user_id)` (test: `/all` zwraca tylko własne). *(podniesione z high → critical: broken authorization)*
- **F45 · Restore Purchases to no-op** — `subscription_bottom_info.dart:45-48` `onTap: () {}`; `restorePurchases()` (`subscription_cubit.dart:119`) zaimplementowane, ale **nigdzie nie wołane**. Subskrybent po reinstalacji/nowym urządzeniu nie odzyska premium; gwarantowane odrzucenie App Store (Guideline 3.1.1). **Fix:** wpiąć onTap.
- **F62 · ✅ FIXED 2026-06-22 · Backend error podczas getUserProfile() wyrzuca OAuth-userów do rejestracji** — `auth_cubit` Google+Apple rozróżnia teraz 404 (nowy user) od transient (rethrow→błąd, user zostaje). Backend F15 też przestał owijać 404 w 400. Patrz Tier 0.

## ✅ CONFIRMED — 🟠 HIGH (18)

- **F14 · ✅ FIXED 2026-06-22 (backend half) · Null `subscription_is_active` → crash → onboarding** — Tier 0 (root). Backend: `users.py:799` → `bool(is_active)` (nigdy null). Frontend null-safe parse (F66/F63) zostaje do Paczki 2.
- **F15 · ✅ FIXED 2026-06-22 · GET subscription owija 404+transient w 400 + wyciek `str(e)`** — `users.py:805-806` → re-raise `HTTPException`, generyczne 500 bez `str(e)`, log z tracebackiem (test: brak profilu → 404 nie 400).
- **F06 · Schedule-driven moments zjadają dzienny budżet notyfikacji** — `crud/notification_moment.py:442-450` (`count_moments_scheduled_today` bez filtra typu) gating `notification_orchestrator.py:274-281`. THERAPY_PREP/POST_SESSION_REFLECTION wpadają w licznik → `rate_limit_hit` blokuje MOOD_DIP/STREAK/PATTERN/RE_ENGAGEMENT dla userów z harmonogramem. Sprzeczne z docstringiem („bypass this cap entirely"). **Fix:** wykluczyć typy schedule-driven z count.
- **F18 · `GET /clinician/patients/archived` zawsze 404 (route shadowing)** — `api.py:251-281` includuje `clinician` (z `/patients/{user_id}`) przed `clinician_v2` (z literalnym `/patients/archived`) → `archived` łapie się jako `user_id`. Sekcja „Archived patients" martwa. **Fix:** literalna trasa przed parametryczną.
- **F19 · Refresh brief enqueuje nieistniejący task RQ → brief wisi „processing" na zawsze** — `clinician_v2.py:639-643` enqueuje `'app.tasks.clinician_brief.generate_brief_job'`; moduł nie istnieje (grep = 1 trafienie, samo enqueue). `.enqueue()` po stringu się udaje (202), worker rzuca ModuleNotFoundError; sync-fallback nieosiągalny. **Fix:** utworzyć task / zmienić target; worker ustawia `failed` na błędzie.
- **F20 · Redempcja zaproszenia pada dla Apple private-relay + auto-kasuje invite po 5** — `clinician.py:340-353` wymusza `patient_email == firebase_email`; relay/inny mail → reject + `record_redeem_failure` → po 5 `cancel_invite`. **Fix:** wiązanie maila doradcze, nie liczyć „nie da się zweryfikować" do licznika.
- **F36 · Batch-joby AI bez `db.rollback()` przy błędzie usera → jeden commit-error zatruwa resztę partii** — `weekly_therapy_summary.py:56-69` (+ monthly_audit, period_snapshots, hero_insight, notification_orchestrator) jedna współdzielona `SessionLocal()`, per-user `except` bez rollbacku; bare commity w `crud.py:1538-1541,1581-1584`. Trigger: transient Azure PG drop / enum DataError → `PendingRollbackError` dla wszystkich kolejnych. **Fix:** rollback per-user / świeża transakcja per user.
- **F44 · `notification_moments.payload` JSON-w-modelu / TEXT-w-migracji → 500 na PROD** — `models/notification_moment.py:130,136` `Column(JSON)` (generyczny) vs migracja `hh8i9j0k1l2m:153-165` `sa.Text()`. Sceptyk potwierdził: na psycopg2 generyczny JSON na kolumnie TEXT (OID 25) zwraca `str` → Pydantic `dict[str,Any]` → ResponseValidationError 500. Bije TYLKO na bazie z migracji (prod), nie na create_all/SQLite (testy zielone). `app_insights_shown.payload` tak samo. **Fix:** uzgodnić model z migracją (ALTER ... USING ::json albo json.loads na odczycie).
- **F46 · Przywrócone subskrypcje nie trafiają do backendu** — `subscription_repository.dart:16-19` early-return gdy `status != purchased` (więc `restored` nie POST-uje), a cubit emituje sukces → krótkie fałszywe „premium". Po naprawie F45 restore i tak nie nada premium. **Fix:** akceptować `purchased` i `restored` przed POST. *(narrowed crit→high: dziś główny trigger martwy przez F45)*
- **F47 · `completePurchase()` przed weryfikacją backendu → receipt tracony** — `subscription_cubit.dart:151-182` (+ starter_package): finalizacja transakcji PRZED POST; jeśli `markAsSubscribed` rzuci (network/5xx/token) → store nie odtworzy, brak kolejki → user obciążony bez premium. **Fix:** POST+sukces przed `completePurchase()`.
- **F50 · Recording v2 OOM — całe nagranie do `List<int>` ~1.15 GB → app ubita, nagranie tracone** — `record_session_cubit.dart:1076-1083` (normalna ścieżka Stop): `assembledPcm.addAll(...)` + `Uint8List.fromList` + `buildWav` → peak ~1.4 GB dla 75 min (jetsam iOS / low-RAM Android). Catch tylko emituje błąd, WAV nie zapisany. Helper streamingowy `WavBuilder` istnieje, nieużyty. **Fix:** strumieniowa asamblacja segmentów do WAV.
- **F53 · iOS interruptions (telefon/Siri) nieobsłużone w v2 → ciche gubienie audio** — `record_session_cubit.dart:186-193` v2 returnuje przed `_configureAndStartRecorder` (gdzie żyje cały AVAudioSession + interruption listener). Gated flagą `recording_pipeline_v2`. **Fix:** skonfigurować AVAudioSession + interruptionEventStream pause/resume w v2.
- **F38 · ✅ FIXED 2026-06-22 · OAuth sign-in dumps istniejących userów do rejestracji** — Tier 0 (OAuth-połowa naprawiona: `isDefinitive404` w `auth_cubit`).
- **F55 · ✅ FIXED 2026-06-22 · Google/Apple bez 404-discrimination** — Tier 0 (jw.).
- **F57 · Onboarding — nieodwracalny pusty ekran przy transient błędzie therapy-context** — `therapy_onboarding_screen.dart` builder bez gałęzi `TherapyOnboardingError`; po Dive-In legal-gate renderuje `SizedBox.shrink` → blank, bez retry → force-kill → pętla. **Fix:** gałąź Error z „Try again".
- **F59 · Home wieczny spinner gdy startowy fetch profilu rzuci** — `main_page_cubit.dart:71-78` `carouselCheck()` bez try/catch → zostaje w `MainPageLoadingState`, brak emisji error/retry. Trigger przy deploy≠migrate (nie-zmigrowana kolumna 500-i `/users/`) lub słaby zasięg. **Fix:** try/catch → `emit(error)` + guard `result['profile']==null`.
- **F65 · MomentType enum (FE) bez `RE_ENGAGEMENT`/`unknownValue` → moments+insights padają dla nieaktywnych userów** — backend ma 9. wartość (`notification_moment.py:52`), FE 8 bez fallbacku (`$enumDecode` → ArgumentError). `/moments/upcoming` nie filtruje typu → gdy aktywny RE_ENGAGEMENT, `loadOnAppOpen` zawsze error (Future.wait kolapsuje cały emit). Łamie additive-only. **Fix:** dodać `reEngagement` + `@JsonKey(unknownEnumValue:)` (też MomentStatus, AppInsight enums).
- **F66 · ✅ FIXED 2026-06-22 · `UserInfo.fromJson` twardy `as bool` na nullable** — `user_info.dart:37` → `as bool? ?? false`. Tier 0 (parsing).

## ✅ CONFIRMED — 🟡 MEDIUM (26)

- **F02 · end-conversation 500 zamiast 404** — `conversations.py:242` deref przed None-guard (245); generic handler → 500. Trigger: double-tap/retry „Stop" na pustej (auto-skasowanej) notatce. **Fix:** guard 404 nad sprawdzeniem statusu. *(high→med: zły status-code na error-edge)*
- **F04 · promo-code 500 gdy brak wiersza subskrypcji** — `users.py:696-720` deref `sub.end_date` na None, brak try/except. **Fix:** `if sub is None:`. *(high→med: warunkowa osiągalność)*
- **F05 · `get_current_user` blokujący `verify_id_token` na event loopie** — `deps.py:23-35` `async def` woła sync `auth.verify_id_token`; single uvicorn worker → episodyczne serializowanie requestów przy odświeżaniu cache certów. Latency/scalability (nie crash). **Fix:** `run_in_threadpool` lub plain `def`. *(uwaga: 1. run uznał za nie-bug; tu potwierdzony jako realny medium)*
- **F07 · Moment INSERT cicho pada gdy prod-enum bez RE_ENGAGEMENT (niezmigrowany)** — `notification_moment.py:150-157` łapie DataError→None. Zawężone: THERAPY_PREP był w oryginalnym enumie, tylko RE_ENGAGEMENT realnie nowy; błąd jest **głośno** logowany (`logger.exception`). Operator-gated (deploy≠migrate). **Fix:** potwierdzić mm3n4o5p6q7r na prod / String(n)+stałe.
- **F10 · Weekly off-by-one (double-liczy następną niedzielę)** — `periodic_summary.py:190` `+timedelta(days=1)` na już-end-of-day. **Fix:** `<= week_end`.
- **F12 · Therapy-tracking data_hash ignoruje kierunki trendu + audit context** — `crud.py:4707-4717`; najsilniejszy trigger to nowy MonthlyAudit movement bez nowych captures (hash bez zmian). **Fix:** dodać `symptom_trend_summary`/`latest_audit_movement` do hash.
- **F13 · On-demand `/generate` `/refresh` sync OpenAI bez timeoutu → H12/zagłodzenie wątków** — `monthly_audits.py:359-370`, weekly, snapshots; klient 600s default + retry×5 z sleep; single worker. **Fix:** krótki timeout + enqueue do RQ.
- **F16 · Apple receipt: brak retry na transient 21002/21005 + permanentny FAILED** — `subscription_service.py:99-112`. **HEADLINE 21008 BŁĘDNY** (21008 zwraca tylko sandbox; 21007 TestFlight/review JUŻ obsłużony). Realny problem: transient/permanent-FAILED bez kolejki. **Fix:** retry/kolejka na transient, nie permanentny FAIL.
- **F17 · Receipt verify w pełni sync bez timeoutu → blip permanentnie FAILED** — `users.py:446-506`, `subscription_service.py` `requests.post`/`execute()` bez timeoutu. (Część „raises 500" nieścisła — zwraca 200+FAILED.) **Fix:** timeouty + PENDING+retry zamiast FAILED.
- **F21 · `mark_session_done` silent no-op** — `models/clinician.py:174-187` brak kolumny `status`, `hasattr` False, endpoint zwraca `done`. **Fix:** zmapować kolumny + migracja.
- **F22 · `/auth/verify` wydaje JWT przy pustym/krótkim `CLINICIAN_JWT_SECRET` → lockout + spalony magic-link** — `config.py:248` default `''`; verify nie ma guardu (a `get_current_clinician` ma `<32→503`). **Fix:** ten sam guard w send/verify.
- **F23 · Mood Trend nigdy nie zawiera dziś** — `chart_service.py:514` `created_at <= end_date` (date→północ). **Fix:** `< end_date + 1 day`.
- **F24 · `carousel_check` unbounded — 1 query/dzień bez capa** — `dashboard.py:62-95`. **Fix:** grouped distinct-date query + cap zakresu.
- **F27 · Achievement nigdy nie nadaje XP** — `goals.py:334` (create) zużywa `xp_awarded`; `goals.py:429-430` (ACHIEVED) short-circuit. (Dodatkowo legacy `award_xp` i tak nie przyznaje punktów leveling.) **Fix:** osobna flaga `achieved_xp_awarded`.
- **F33 · Whisper fallback nie zdekoduje m4a (brak ffmpeg/Aptfile)** — `wav_chunker.py:276-307` pydub→None→single-shot Whisper→fail >25 MB. **Fix:** Aptfile `ffmpeg` + heroku-community/apt.
- **F34 · Free-tier recording bypass przez równoległe `/upload/initiate`** — `session_recordings.py:308-315` limit tylko przy initiate z COMPLETED; `/complete` nie re-sprawdza. **Fix:** re-check w `/complete` + liczyć PENDING/IN_PROGRESS.
- **F37 · Recording recovery PENDING+commit PRZED enqueue → ping-pong bez inkrementacji attempt** — `recording_recovery.py:102-105`. **Fix:** `enqueue_failed=True` do sukcesu enqueue / inkrementować attempt.
- **F39 · 403 interceptor re-wysyła skonsumowany multipart + dubluje premium-requesty + gubi query** — `dio_client.dart:58-71` retry na każdy 403 (premium-gate to 403), bez force-refresh. **Fix:** retry tylko 401; `getToken(true)`; nie retry FormData; re-pass query.
- **F40 · `getUserProfile()` deref `result['profile']` + twarde casty** — `users_manager.dart:54-59`. **Fix:** typed `NotRegistered` vs transient; tolerancyjny fromJson. *(med: główny returning-user path to splash, już fixed; OAuth-path zostaje)*
- **F43 · Voice realtime-session bez wydłużonego timeoutu (20s/30s) → po cold-starcie voice nie startuje** — `dio_settings.dart:18-19`, łańcuch 2 callów. **Fix:** dłuższy timeout + 1 retry.
- **F48 · Brak app-level listenera `purchaseStream` → zakupy finalizujące się po zamknięciu paywalla gubione** — `subscription_cubit.dart:140-147,235-239` (close cancels). Ask-to-Buy/deferred/wolna walidacja. **Fix:** globalny listener w `main.dart`.
- **F49 · `subscription_cubit` emit `LoadedProducts` przez niesprawdzony `as` cast** — `:101-103,167-169,203-205`; CastError gdy event streamu w innym stanie (np. canceled-branch :203 niezguardowany). **Fix:** `if (s is LoadedProductsState)`.
- **F58 · Rejestracja: spinner wisi wiecznie gdy create-call rzuci** — `sign_up_cubit.dart:81` showLoading bez try/catch przed `closeAllLoading` (132); fire-and-forget z PersonaliseView. Dla email konto Firebase już utworzone → retry „email already in use". **Fix:** try/finally z `closeAllLoading` + obsługa user==null.
- **F61 · `get_users_eligible_for_notification` `KeyError('1,2')` (`str.format` na klamrach regexa)** — `crud.py:528-540`. Reprodukowalne; **firnęło w prod 2026-05-06**, ale callerzy gated `notification_legacy_jobs_enabled` (default False) → dziś nieosiągalne, fatal po re-włączeniu flagi. **Fix:** bound parameter zamiast `.format()`.
- **F63 · ✅ FIXED 2026-06-22 · `UserInfo.fromJson` nullable `subscription_is_active` jako non-null** — `user_info.dart:37` → `as bool? ?? false` (z F66). Tier 0 (parsing).
- **F64 · Dio 403 premium-gate traktowany jak token-expiry → re-upload multipart** — `dio_client.dart:58-72`; degraded (nie silent). **Fix:** retry tylko 401 / rozróżnić premium-403.

## ✅ CONFIRMED — ⚪ LOW (8, realne ale drobne)

- **F03** · end_redis no-op subtraction (`:285`) + overwrite `created_at` (`:262`) — telemetry-only, guarded try/except; bucketowanie dzienne praktycznie bez wpływu.
- **F08** · `deliver_due_moments` proceeds-without-lock przy błędzie Redis — duplikaty blokowane przez atomic claim + UNIQUE; tylko koszt; design świadomy.
- **F25** · EmotionPie empty-state zawsze 400 (typo `desription` + brak `AI_description`) — FE degraduje do noData(), więc tylko log 400. **Fix:** `description=...`, `AI_description=""`.
- **F26** · Dashboard `Query(default=dt_date.today())` zamrożony na boot — żywa apka wysyła `date` jawnie; dyna cyklują dziennie. Wąskie.
- **F29** · `_suggestion_rate_limit` dict bez eviction — entry ~kilkadziesiąt bajtów, potrzeba setek tysięcy distinct non-EN userów. **Fix:** TTL/purge.
- **F41** · `DioClient.post/put/patch` bez `is Map` → TypeError tylko na sukces-200 z nie-obiektowym body (FastAPI zwraca obiekty). **Fix:** mirror `getMap`.
- **F42** · Chunked-upload substring-match kodów — poor practice, ale (jak F54) matcher widzi tylko czysty `HTTP error: <code>`, nie offsety. Niskie ryzyko. **Fix:** branch po int statusie.
- **F60** · Stats sections czyta `StatsOverviewCubit` synchronicznie raz → stale empty-first layout (race). Kosmetyczne, naprawia się przy re-entry. **Fix:** BlocSelector.

---

## 🛠️ ALREADY FIXED on disk (5) — zweryfikowane że NAPRAWIONE

> Sceptyk czytał aktualny kod i potwierdził, że bug już nie istnieje (ostatnie fixy z pamięci).

- **F30** (splash sign-out na każdy błąd) — naprawione: `splash_screen.dart:38-45` `_isDefinitive404`; tylko 404 → welcome, 5xx/timeout/parse → retry overlay (dokładnie suggested_fix).
- **F31** (splash empty-cache → onboarding) — naprawione: `_resolvePostLoginDestination` (~514) propaguje wyjątki getTherapyContext; 404 vs transient rozróżnione, transient → retry zamiast onboardingu.
- **F32** (chunked `/complete` AAI sync 25s → 503) — naprawione: `/complete` tworzy recording z `storage_key` i enqueuje `process_session_recording_whisper` (job_timeout=1800) z pustym AAI URL — worker robi GCS/Whisper. Sync upload tylko w single-shot `/upload` dla małych plików.
- **F51** (resume-after-crash gubi audio sprzed crashu) — naprawione (D6): `resumeSessionV2` seeduje `segmentPaths` starymi segmentami; `_stopRecordingV2` składa unię old+new.
- **F52** (`Finish & process` dead-end) — naprawione (D4): deleguje do `BackgroundUploadCubit.processEntry` → `_resolveWavPath` składa `.pcm` w WAV i uploaduje; martwy `.wav`-only return usunięty.

## ❌ REFUTED (6) — obalone, NIE ścigać

- **F09** (legacy crony abortują wszystkich userów) — **martwe/niezaschedulowane:** `generate_monthly/daily/yearly_summaries` nie są w `rq_scheduler_setup.py`, lifespanie ani Procfile; jedyny caller to standalone skrypt wołający daily-wariant (już None-guarded). Aktywny pipeline okresowy to inne (per-user izolowane) joby. Defekt w kodzie istnieje, ale nieosiągalny w prod.
- **F11** (hero-insight hash ignoruje wartości score) — **INVALID:** SymptomScore append-only; „korekta" = nowy wiersz → zmienia point-count → hash się zmienia.
- **F28** (health_check prompt VARCHAR(200) → 500) — **nieosiągalne:** pole nie jest free-text, klient wysyła 4 krótkie stałe localized stringi (<200). Tylko custom-klient mógłby.
- **F35** (osierocone audio GCS przy failed move) — **premisa nieaktualna:** brak copy-move; assembled blob jest `storage_key` i kasowany przez privacy-cleanup po transkrypcji.
- **F54** (chunked substring-match misfire na offsetach) — **obalone:** `_handleError` wrapuje w `Exception('HTTP error: <code> <terse msg>')`; offsety/Content-Range nie trafiają do stringu, więc transient 500 nie zostanie wzięty za 409/404.
- **F56** (re-rejestracja nadpisuje subskrypcję na inactive) — **INVALID:** backend `POST /subscription` ignoruje status z body, `_create_initial_subscription` ma guard istnienia (`# nie nadpisuj`). Premium NIE jest kasowane.

---

## Motywy przekrojowe (po weryfikacji)

1. **Tier 0 „backend error = nowy user"** — splash naprawiony, **OAuth sign-in path + null-cast w kontrakcie profilu nadal otwarte**. Najgroźniejsze, sprzęga się z deploy≠migrate.
2. **deploy≠migrate (Heroku bez release phase)** — F44 (JSON/TEXT 500), F07 (enum drift), F61 (latent za flagą). Migracje ręczne → additive + boot-resilient.
3. **SQLite testy ≠ Postgres** — F44 (JSON readback), F28-class (VARCHAR overflow). Dodać offline check na dialekcie `postgresql`.
4. **Brak transient-vs-permanent na FE** — generyczny `Exception('HTTP error: ...')` gubi statusy (źródło Tier 0, F39, F40, F64). Rozwiązanie: typed `ApiException(statusCode)`.
5. **Money path bez trwałości** — F45/F46/F47/F48: martwy restore, restore-nie-do-backendu, complete-przed-weryfikacją, brak globalnego listenera.
6. **Recording v2** — F50 (OOM) i F53 (interruptions) zostają; F51/F52/F32 już naprawione. Gated flagą `recording_pipeline_v2`.
7. **Batch-joby na współdzielonej sesji bez rollbacku** (F36) — jeden błąd kasuje run dla reszty.

## Rekomendowana kolejność napraw

**Faza 1 — deploy-blockery (przed kolejnym release):**
1. Tier 0 OAuth path + null-cast (F62, F14, F66, F63, F15, F38, F55, F40) — backend `bool()`+nie-owijać-404, FE null-safe + 404-discrimination w auth_cubit. `integration-devops` koordynuje `backend-api`+`flutter-mobile`.
2. F01 `/conversations/all` filtr user_id — `backend-api`.
3. F59 home-spinner try/catch+retry — `flutter-mobile`.
4. F45+F46 restore (wpiąć + akceptować `restored`) — `flutter-mobile`.

**Faza 2 — wysokie ryzyko / utrata danych:**
5. F50 recording OOM (streaming WAV) + F53 iOS interruptions — `flutter-mobile` (gate flagą).
6. F36 batch-joby `db.rollback()` — `backend-api`+`data-analytics`.
7. F44 notification_moments JSON/TEXT — `backend-api` (migracja idempotentna).
8. F47 completePurchase ordering + F48 global purchase listener — `flutter-mobile`.
9. F06 schedule-driven budget — `data-analytics`. F02/F04 guardy — `backend-api`.

**Faza 3 — high/medium pozostałe:** F18/F19/F20/F22 clinician → `backend-api`; F39/F65/F49/F57/F58 → `flutter-mobile`; F23/F24/F25/F13/F33/F34/F37 → `data-analytics`/`backend-api`; F16/F17 receipts → `backend-api`+`flutter-mobile`; reszta MEDIUM/LOW wg listy.

**Przed deployem:** `qa-testing` (suite + offline Postgres DDL check), `security-guardian` dla F01 i Tier 0.

---

## Appendix

- **Audyt:** workflow `mindsync-prod-critical-audit` run `wf_3bad8a4c-b2a` (21 audytorów, 2026-06-21).
- **Weryfikacja:** workflow `mindsync-audit-verify-all` run `wf_d1bca273-d32` (66 sceptyków kod-po-kodzie, 2026-06-22). Werdykty: confirmed=38, partly_confirmed=18, refuted=10, cannot_verify=0; już-naprawione=5.
- **Artefakty (repo-root, do re-weryfikacji):** `_audit_verify/F01.json`–`F66.json` (pełne znaleziska), `_audit_verdicts_full.json` (werdykty z dowodami file:line), `_audit_verdicts_digest.md` (skrót).
- **Nie audytowano:** therapist-deck (osobny projekt), pełny l10n (slice fe-l10n: 0 błędów funkcjonalnych), testy/coverage, czysty performance.
