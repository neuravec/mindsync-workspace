---
name: Xcode 26 / Flutter 3.41.1 migration (ITMS-90725)
description: 2026-04-30 — migration decisions, audits, and rationale for the Apple iOS 26 SDK gate. Branch chore/xcode26-flutter341 in mindsync-frontend.
type: project
originSessionId: 7cc72544-c49f-4ef3-b741-6a113123dcde
---
**Why:** Apple ITMS-90725 — od 2026-04-28 wszystkie iOS app submissions wymagają build z iOS 26 SDK (Xcode 26+). Build SDK requirement, nie deployment target — ALE pluginy (głównie `flutter_webrtc 1.x`) wymuszają deployment target bump.

**How to apply:** Następna release MUSI iść z brancha `chore/xcode26-flutter341` (lub mergniętego do dev). Stary toolchain (Flutter 3.27 / Xcode 16) jest one-way doorem — Apple odrzuci builds zbudowane starym SDK po deadline.

## Decyzje (które warto pamiętać przy rotacji kodu)

- **flutter_webrtc exact pin (no caret) + dependency_override** — 0.x→1.x był major API rewrite. Przyszły `flutter pub upgrade --major-versions` przepisuje caret/exact tak samo, dlatego zabezpieczenie jest w `dependency_overrides` (jedyne co `--major-versions` szanuje). Nie podnosić bez explicit voice-pipeline regression testu na realnym device.
- **UIScene migration NIE robiona ręcznie** — Flutter 3.41 auto-migrates przy pierwszym `flutter run` na macOS. Zweryfikowano że `AppDelegate.swift` jest minimalny (brak custom Firebase init / FCM handlers / deep-link handlers w Swift). firebase_messaging plugin sam swizzles nawet z `FirebaseAppDelegateProxyEnabled=false`.
- **pubspec version NIE bumpowany ręcznie** — humm release CLI bumpuje na tag push. Codemagic również nadpisuje build number z `app-store-connect get-latest-testflight-build-number + 1` (iOS) i Play API equivalent (Android). Pubspec build number jest cosmetic.
- **Backend nie ruszany** — IAP używa legacy `verifyReceipt` API spójnie z `in_app_purchase` plugin (też legacy). Migracja do App Store Server API to osobny ticket, nie blocker dla ITMS-90725.
- **Codemagic Xcode 26.4** — najnowsza dostępna; jeśli regression w image, fallback na 26.0 (jedna linia `xcode_ver` w codemagic.yaml). Test build NIE robić z brancha — `publishing:` nie ma gate, wyśle do TestFlight/Play niezależnie od `submit_as_draft`.

## Co zostało zaadresowane przez 5 rund Devils-Advocate review

- CRIT: test trigger app-release z brancha publikuje do TF/Play → plan zmieniony, user testuje normalnym humm flow (merge → tag → app-release)
- CRIT: pubspec build number race (3 sources of truth: pubspec, ASC API, Play API) → skip manual bump, document że pubspec jest cosmetic
- CRIT: Generated.xcconfig stale fvm path → mitigated, plik jest gitignored (`ios/.gitignore`), CI regeneruje świeżo
- CRIT: Podfile post_install nie wymuszało deployment target na Pod targetach → decyzja: explicit per-config loop w `post_install` ustawia `IPHONEOS_DEPLOYMENT_TARGET` jeśli pod's spec minimum jest niższe niż app's deployment target. Bez tego pluginy z lower spec minimum (np. flutter_webrtc declaruje 13.0) silnie ściągają deployment target Pod targetu poniżej app target → ITMS-90725 wraca przy upload (dynamic framework MinimumOSVersion mismatch). Towarzyszący `require 'rubygems/version'` u góry Podfile to defensive: CocoaPods' embedded Ruby na niektórych obrazach Codemagic nie autoload'uje `Gem::Version`; bez require porównanie wersji w post_install crashuje z `NameError`. Jeśli ktoś usunie require myśląc że to "unused", CI break na fresh image. Jeśli usunie cały loop, deployment targety pluginów silnie ściągną się w dół.
- HIGH: l10n.yaml synthetic-package usunięte przeze mnie omyłkowo → przywrócone (forward-compatible setting; ~90 ekranów używa explicit import path)
- HIGH: webrtc caret pin → exact pin + dependency_override
- HIGH: intl pinning rule retired → memory zaktualizowane (feedback file + index lines)
- MED: AppFrameworkInfo.plist regen ryzyko przy `flutter create .` → udokumentowane jako fragile

## Test plan dla usera (po stronie macOS)

1. `fvm install 3.41.1 && fvm flutter pub get && cd ios && pod install`
2. Open `Runner.xcworkspace` w Xcode 26 → smoke build iOS 26 simulator + iOS 16 device
3. Smoke flows w priorytecie:
   - **Voice realtime** (HIGH RISK, flutter_webrtc 1.x major rewrite)
   - Cold-start auth (Apple SignIn + Google)
   - FCM cold-start nudge tap (deep-link)
   - IAP sandbox purchase
   - 75-min recording session (Whisper fallback)
4. Po pozytywnym smoke: merge → dev → humm tag → `app-release` → TestFlight → 24h soak → App Store submission

## Rollback path

Voice pipeline regression: rewrite `dependency_overrides` na `flutter_webrtc: 0.12.7`, ale UWAGA — to wymaga też cofnięcia deployment target (16.0 wymuszone przez 1.x; 0.12.x toleruje 14.0). Inne plugin downgrade'y mogą nie być potrzebne. Hotfix na starym toolchain jest niemożliwy (Apple gate); fix-forward jest jedyną drogą.

## Powiązane follow-ups (inne tickety)

- Whisper chunking (single-shot 25MB limit nadal aktywny przy 75-min sesji)
- App Store Server API migration zamiast verifyReceipt
- humm CLI SHA pinning (memory: codemagic_setup follow-up)
- AppFrameworkInfo.plist CI guard (assertion że MinimumOSVersion zostaje na bieżącym poziomie)
- flutter_webrtc CI version assertion (defense-in-depth dla dependency_override)
