---
name: half-created-account-lockout-fix-2026-08-18
description: "Fix lockoutu \"konto bez profilu\" (czarny ekran + We couldn't find your profile); BE c1334e8 + FE 2e91ac0 COMMITTED lokalnie NIE pushed; kontrakt 404 detail profile_not_created/user_not_found"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b152f61-9524-414a-a470-3abc86b59d4b
  modified: 2026-08-18T09:48:48.501Z
---

# Lockout "half-created account" – diagnoza i fix (2026-08-18)

**Bug (zgłoszony przez testerkę, e-mail signup):** rejestracja e-mail tworzy konto Firebase + wiersz `users` + subskrypcję, ale `user_profile` powstaje DOPIERO po zgodzie RODO w therapy-onboardingu (odroczenie z commitu FE `2156b03`, patrz [[onboarding-profiling-plan]]). Użytkownik, który wypadł z flow między weryfikacją maila a legal gate, był trwale zablokowany:
1. login → `auth_cubit` połykał 404 (`catch (_) {}`) → `/main-page` → `MainPageCubit.carouselCheck()` bez try/catch → wieczny `loading()` → gołe `Center(CircularProgressIndicator())` bez Scaffolda = **czarny ekran**; cubit to lazy singleton, więc zaklinowany do zabicia procesu;
2. cold start → splash traktował KAŻDE 404 z `get_user_profile_and_subscription` jako "brak konta" (fix `7043175` zawęził eviction do 404, ale endpoint jest rootowany od `UserProfile`, więc 404 dostaje też user bez profilu) → toast "We couldn't find your profile" + signOut;
3. re-rejestracja → Firebase `email-already-in-use` → "A user with this email already exists" (string CZYSTO kliencki, `firebase_error_mapper.dart`, NIE z backendu). Pułapka bez wyjścia.

**Fix (DEPLOYED/PUSHED 2026-08-18 ~12:40):** BE `c1334e8` PUSHED → **Heroku v540 DEPLOYED** (dyna up, bez migracji). FE commit przebazowany na bot-bump Codemagic (`6e9adf4`, tagi 2.0.80/2.0.81) → **`45d1474` PUSHED na dev** → Codemagic/TestFlight. (Pierwotny lokalny hash FE: 2e91ac0.)
- **BE `c1334e8` (main):** 404 z `get_user_profile_and_subscription` rozróżnia teraz detail: `"profile_not_created"` (users row jest, profilu brak) vs `"user_not_found"` (brak users row). Additive-only, bez migracji, 200 bez zmian. To **stały kontrakt cross-layer** – nie zmieniać stringów.
- **FE `2e91ac0` (dev):** (a) `carouselCheck()` łapie błędy → `MainPageState.error` + retry w `ErrorView` (nowy opcjonalny `onRetry`); (b) splash i email-login przy `profile_not_created` kierują do `/therapy-onboarding` (bez signOut) – każde inne 404 = stare zachowanie (bezpieczne ze starym backendem); (c) try/finally na BotToast w register/login; (d) `flushPendingProfile` tworzy minimalny profil (displayName lub pusty) gdy brak pending JSON – domyka pętlę po reinstalu; backend `UserProfileCreate` ma wszystkie pola Optional, więc 422 nie grozi.

**Review integration-devops: GO.** Macierz wersji zweryfikowana (nowy klient + stary backend = legacy evict, stary klient + nowy backend = bez zmian). Testy: BE pełna suita = baseline (21 failed / 5305 passed); FE touched testy 47/47, analyze czysty.

**Deploy:** najpierw push BE main (auto-deploy Heroku, bez migracji), potem push FE dev (Codemagic→TestFlight). Monitoring po deployu: spike `logError` z ErrorView jako kanarek resztkowego loopa 404.

**Follow-up parity Google/Apple: ZROBIONE** – FE commit **`5d2244b`** **PUSHED na dev 2026-08-18 ~13:3x** (→ Codemagic/TestFlight). Nowy enum `SocialSignInProfileFailure` + `resolveSocialSignInProfileFailure()` w `api_error_utils.dart`; obie gałęzie social w `auth_cubit.dart` switchują: profile_not_created → `/therapy-onboarding` (bez signOut), user_not_found/legacy → singUpRoute jak dotąd, transient → rethrow. Testy targeted 42/42, analyze 0 issues; pełna suita nie re-runowana w tej sesji (CPU thrash od równoległych flutter test – baseline 26 fail z sesji 45d1474 aktualny). Push = decyzja operatora (kolejny build Codemagic).

**Konto testerki:** decyzją operatora NIE naprawiane (olewamy).
