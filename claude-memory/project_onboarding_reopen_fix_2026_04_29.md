---
name: Onboarding reopen fix (F1-F5) — IMPLEMENTED 2026-04-29
description: Pakiet 5 fixów onboardingu po user report "stary layout po reopen". Splash silent catch, brak listenera TherapyOnboardingError, SizedBox.shrink na legal gate, SharedPrefs nie user-scoped, companion screen CTA hides on keyboard. 55 testów pass.
type: project
originSessionId: 0365e4b6-84bc-434e-b2a7-38f9f743811f
---
**STATUS 2026-04-29: IMPLEMENTED, pending deploy.** Branch `dev`, niecommitowane (24 modified + 5 nowych plików).

## Co user zgłosił
Po fixie legal_gate scroll-gate (2026-04-24) userzy logowali się OK pierwszy raz, ale po zamknięciu i ponownym otwarciu apki widzieli onboarding znowu, ze "starym layoutem" i nieklikalnym Continue.

## Root cause (zweryfikowane przez PostHog 2026-04-29)
- 11/15 userów ukończyło onboarding od 2026-04-24, 4/15 utknęło
- 2 utknęło na 2.0.35 (stary build z scroll-gate) → CRIT-2 stale build
- 1 user (`019dd41f...`) na 2.0.36 przeszedł 6 ekranów ale utknął na **companion screen step 6** — bo CTA znikał gdy klawiatura była otwarta
- Backend timeout/network failure → splash silent catch fallthrough → user widzi onboarding zamiast retry
- Brak listenera `TherapyOnboardingError` → puste WelcomeSplash gdy backend padł
- Legal gate `SizedBox.shrink()` na non-Loaded → pusta strona z app barem (wygląda jak "stary layout")
- SharedPreferences `hasCompletedTherapyOnboarding()` nie user-scoped → multi-account leak

## Fixy zaimplementowane (single PR, atomic)

### F1 — Splash retry + error overlay (`lib/screens/splash/splash_screen.dart`)
- `_resolvePostLoginDestination()` zwraca `Future<String?>` (null = error)
- 2 attempts: natychmiastowy + retry po 300ms
- DioException 404 → onboarding (legitimate new user, no retry)
- Inne błędy po 2 próbach → `setState(_resolveError = true)`, return null
- `_retryResolve()` — user-triggered retry w error overlay
- PostHog: `splash_resolve_failed` (error_type, attempt, is_final)
- Error overlay: `Icons.wifi_off_rounded` + "Try Again" button

### F2 — Listener TherapyOnboardingError (`lib/screens/therapy_onboarding/therapy_onboarding_screen.dart`)
- Nowy case `else if (state is TherapyOnboardingError)` w `BlocConsumer.listener`
- PostHog: `onboarding_load_error` (error_type='load_failed', NIGDY raw message — mental health privacy)

### F3 — Legal gate error view (`lib/screens/therapy_onboarding/views/onboarding_legal_gate_view.dart`)
- Loading → `CircularProgressIndicator(color: deepOcean)`
- Error → `OnboardingErrorView(onRetry: cubit.loadExistingContext)` (nowy widget `lib/widgets/onboarding_error_view.dart`)
- Saving/inne → `SizedBox.expand()`

### F4 — Per-UID SharedPrefs + migracja (`lib/services/shared_preferences_manager.dart`, `lib/services/preference_keys.dart`)
- Klucz: `u_{uid}_therapyOnboardingCompleted` (raw string przez `SharedPreferencesService.prefs`)
- Metody przyjmują `{String? uid}` — `null` → zawsze false/no-op
- Jednorazowa migracja `_migrateOnboardingKey()`: legacy klucz `therapyOnboardingCompleted` → UID-scoped, sentinel `onboardingUidMigrationDone` blokuje powtórzenie
- 3 call-sites zaktualizowane: splash, therapy_onboarding_cubit, settings_cubit

### F5 — Companion screen + uniwersalny anti-regression (`lib/screens/therapy_onboarding/views/onboarding_companion_view.dart`, `cubit`, `state`)
- **CRIT-1**: usunięty `if (!keyboardOpen) ...` wrapper wokół CTA + `autofocus: true` z TextField. CTA teraz sticky footer poza scroll area (wzorzec legal_gate).
- **CRIT-2**: Cubit ma nowy `goBack()` decrementuje `currentScreen`. Back button w `therapy_onboarding_screen.dart` wywołuje `cubit.goBack()` przed `_pageController.jumpToPage`.
- **HIGH-1**: `selectedArchetype` default zmieniony z `''` na `'friend'` w state (Freezed regen via build_runner).
- **HIGH-3**: Progress indicator `currentStep: 6, totalSteps: 6` → `5, 5` (uniknięcie false complete signal).
- **MED-3**: `completeOnboarding` capture state PRZED `emit(saving())` → catch używa snapshot.copyWith(errorMessage:...) zamiast fresh `loaded(currentScreen: 6)`. Zachowuje orcaName + archetype.
- **Bonus**: ten sam `if (!keyboardOpen)` antywzorzec usunięty też z `onboarding_challenges_view.dart` i `onboarding_journey_view.dart`.

### Universal anti-regression test
- `test/screens/therapy_onboarding/onboarding_views_cta_visibility_test.dart` — regex scan plików `views/*.dart`, fail jeśli ktokolwiek wprowadzi `if (!keyboardOpen)` lub `if (keyboardOpen)` warunek.
- Cel: chronić przed regresją tej klasy buga po raz trzeci.

## Test coverage
- 21 legal_gate (2 nowe F3) ✅
- 13 cubit (qa-testing — error path, toggle, goBack, success paths) ✅
- 4 anti-regression CTA visibility ✅
- 7 splash error overlay (qa-testing — harness pattern, brak Firebase mock) ✅
- 10 SharedPreferencesManager (UID isolation, migracja, sentinel) ✅
- **TOTAL: 55/55 PASS**, `flutter analyze`: 0 errors (60 pre-existing info)

## Lokalizacje
- 4 nowe ARB klucze w 7 językach (en/de/fr/nb/sv/es/pl): error UI, retry button
- gen-l10n nadal nie uruchamia się czysto (pre-existing PL ARB `=4` syntax issue) — klucze dodane ręcznie w 7 generated files

## Co user musi zrobić
1. Code review zmian (24 modified, 5 nowych plików — `git diff`)
2. Commit jako single PR
3. Deploy via Codemagic do TestFlight + Play
4. Monitor PostHog `splash_resolve_failed` + `onboarding_load_error` w pierwszych 24h po deploy
5. Po 7 dniach: analiza % userów wciąż na 2.0.35 → decyzja czy wymagać forced update

## Risks / open items
- **Brak widget testu pełnego `SplashScreen`** — `FirebaseAuth.instance.authStateChanges()` jest static call w `initState`, nieczy testowalny bez DI refactoru. Pokryte przez harness pattern (overlay-only) + cubit + prefs unit tests.
- **Migration fire-and-forget** w `_migrateOnboardingKey` — idempotentna, OK marginalne ryzyko podwójnego setBool(true).
- **Splash error overlay BEZ "Retrying…" indicator** — UX cosmetics, follow-up.
- **Companion screen MED-1 (Semantics), MED-2 (color picker touch targets), LOW-1 (skip button), LOW-2 (orca happiness reactivity)** — out of scope tego PR, follow-up UX polish.

## Powiązane memory
- `project_legal_gate_bug_2026_04_24.md` — poprzedni fix tej samej klasy buga (5 dni wcześniej)
- `feedback_intl_version_pinning.md` — fvm Flutter 3.27.0 wymagany (system Flutter wymaga intl ^0.20.2 ≠ pubspec ^0.19.0)

## Lessons learned (do future feedback memory if relevant)
- Anti-regression testy na konkretne wzorce kodu (regex scan) > tylko widget testy. Jeden plik chroni 3 views.
- "User mówi STARY LAYOUT" = empty widget tree (`SizedBox.shrink()`) wygląda dla usera identycznie jak "old layout pre-fix".
- Backend network errors w splash flow MUSZĄ pokazywać retry, nigdy fallthrough do onboarding (mental health compliance + user trust).
