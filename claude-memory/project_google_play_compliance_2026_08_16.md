---
name: project_google_play_compliance_2026_08_16
description: "Google Play compliance batch (Billing 8, targetSdk 36, 16 KB pages) — FE-only, zweryfikowany na AAB/APK, stan na 2026-08-16"
metadata: 
  node_type: memory
  type: project
  originSessionId: d866557a-887c-4926-8c2d-ec908f40c831
  modified: 2026-08-16T10:00:08.056Z
---

Ticket ClickUp **86c9b65rj** „Google Play Updates 14.08.2026" – trzy wymogi Play (deadline Billing + targetSdk **31.08.2026**, 16 KB **01.02.2027**). Zrobione **tylko we froncie**, backend bez zmian.

**Status: PUSHED** – commit `913f985` na `origin/dev` (rebase na auto-commit Codemagic `fff99de`, wersja **2.0.79+152**), więc Codemagic sam zbuduje release. Ticket ClickUp przestawiony na **in testing** (w tej liście NIE MA statusu „review": Open / to do / in progress / in testing / blocked / completed / Closed).

**Zmiany (6 plików, gałąź `dev`, wszystkie w `mindsync_app/`):**
- `pubspec.yaml` – `in_app_purchase` ^3.2.1 → **^3.3.0**, dodane jawnie `in_app_purchase_storekit: ^0.4.0`
- `android/settings.gradle` – AGP **8.4.2 → 8.11.1**
- `android/gradle/wrapper/gradle-wrapper.properties` – Gradle **8.6 → 8.14**
- `android/app/build.gradle` – usunięty pin `com.android.billingclient:billing:7.0.0` (to on trzymał starą wersję mimo nowszej w pluginie)
- `lib/core/service_locator.dart` – `enableStoreKit1()` na starcie (iOS/macOS)

**Dlaczego pin StoreKit 1:** `in_app_purchase_storekit` 0.4.0 zrobił StoreKit 2 domyślnym, przez co `serverVerificationData` zmienia się z paragonu Apple na token JWS. Backend (`app/services/subscription_service.py`) waliduje legacy `verifyReceipt` → bez pinu każdy zakup na iOS byłby pobrany i odrzucony przy weryfikacji. Wywołanie MUSI być przed pierwszym dotknięciem `InAppPurchase.instance` (to ono robi `registerPlatform()`, które czyta flagę i buduje obserwatora transakcji; późniejsza zmiana zostawia niezainicjowany `_sk1transactionObserver` i `purchaseStream` rzuca). Migracja backendu na App Store Server API = osobny temat, `enableStoreKit1` jest już `@Deprecated`.

**Weryfikacja na realnym artefakcie (nie deklaratywnie):**
- Billing: `gradlew :app:dependencies --configuration releaseRuntimeClasspath` → `com.android.billingclient:billing:**8.0.0**`
- targetSdk: scalony manifest → `android:targetSdkVersion="36"` (`minSdkVersion=24`)
- 16 KB: wszystkie 64-bitowe `.so` w AAB mają LOAD align ≥ 16384 (llvm-readelf z NDK 28.2), `extractNativeLibs="false"`, a `zipalign -c -P 16 -v 4` na release APK → „Verification successful"

**Ważne fakty do zapamiętania:**
- Flutter 3.41.1 sam z siebie daje compileSdk/targetSdk **36** i ndkVersion 28.2 (`flutter_tools/.../FlutterExtension.kt`); Play flagował 35, bo dotyczy to **release'u produkcyjnego**, a Codemagic publikuje wyłącznie na **internal** – promocja do production jest ręczna w Play Console i bez niej wymogi Play nadal będą raportowane jako niespełnione.
- AGP 8.11.1 + Gradle 8.14 to kombinacja, którą Flutter 3.41.1 generuje dla nowych projektów (`gradle_utils.dart`: `templateAndroidGradlePluginVersion`, `templateDefaultGradleVersion`) – najlepiej przetestowana para dla tego SDK.
- `in_app_purchase_android` zatrzymuje się na **0.5.0** na Flutterze 3.41.1 (0.5.2 nie jest „resolvable"); 0.5.0 i tak niesie billing 8.0.0, więc wymóg spełniony.
- Baseline testów: `test/screens/fab_flows/record_session_appbar_close_test.dart` failuje (asercja `discardRecording()`, linia 188) **i wisi na drugim teście** – potwierdzone w izolowanym worktree na czystym `origin/dev`, to stan zastany. Patrz [[reference_pre_existing_test_baseline_2026_06_01]].
- Uwaga na osierocone procesy: ubicie zadania w tle zostawia proces `flutter_tools`, na którym blokuje się każdy kolejny `flutter test` (zero CPU, wisi w nieskończoność). Ubić dart.exe z `flutter_tools` w command line przed ponowną próbą.
- targetSdk 36 = Android 16 ignoruje blokadę orientacji na ekranach ≥600dp → na tabletach/foldables apka może się obracać mimo `SystemChrome.setPreferredOrientations`. Do sprawdzenia w QA, nie blokuje wydania.

Powiązane: [[reference_frontend_ci_git_topology]], [[feedback_concurrent_session_git_hygiene]].
