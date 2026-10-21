---
name: Legal gate onboarding bug (iPhone 17 + Dynamic Type) — FIXED 2026-04-24
description: Krytyczny bug — scroll-gate blokujący Continue na iPhone SE/17 + Dynamic Type. Fix 1 (remove scroll-gate) wdrożony 2026-04-24. Single PR, 19 widget tests passing, backend unchanged, telemetria + dashboard deployed.
type: project
originSessionId: e0b13d6c-6237-4c1a-b9b2-0e064e58c61f
---

**STATUS 2026-04-24: IMPLEMENTED (pending user deploy).**
- T1 view refactor — `disclaimerScrolled` usunięty ze state+cubit, scroll-gate wywalony, a11y uplift (Semantics na checkboxach, TextButton na "Change", Semantics(button) na privacy link)
- T2 6 ARB locales przetłumaczone ("Change" → Zmień/Ändern/Modifier/Cambiar/Ändra/Endre) + nowy klucz `onboarding_consentRequired` w 7 ARB
- T3 PostHog events `onboarding_legal_gate_gate_ready` + `onboarding_legal_gate_abandoned` (BlocListener + dispose), helper `_deviceModel()` via `dart:io Platform` (fallback — brak device_info_plus w pubspec, TODO comment). `AnalyticsEvents.onboardingLegalGateReady`/`.onboardingLegalGateAbandoned` stałe dodane. Dashboard "Onboarding Health" — 3 nowe insighty w `scripts/posthog_build_dashboards.py:278-310`
- T4 widget tests — 19 testów w `test/screens/therapy_onboarding/onboarding_legal_gate_view_test.dart`, anti-regression guard "ElevatedButton NOT in SingleChildScrollView"
- T5 backend verified read-only — zero zmian server-side, double-guard (splash:165/179 + cubit:113) confirmed functional
- flutter analyze: 0 new issues. Grep `disclaimerScrolled` w lib/: 1 hit (docstring only, martwy symbol).

**Rollback:** single `git revert` — zero DB migrations, zero backend coupling.

---
Ekran `lib/screens/therapy_onboarding/views/onboarding_legal_gate_view.dart` ma 3-warunkowy gate (`disclaimerScrolled && gdprChecked && ageChecked`). Disclaimer card w `Expanded > Expanded > SingleChildScrollView` zapada się do ~10-80px na iPhone SE/17 + iOS Dynamic Type. Dwa failure modes kompromitujące scroll-gate: (a) `maxScrollExtent==0` gdy content fits → listener nigdy nie odpala, (b) viewport tak mały że fizycznie nie da się scrollować. Wybrany fix: **Fix 1 — REMOVE scroll-gate**. Alternatywy: Fix 2 (`addPostFrameCallback` auto-mark gdy maxScrollExtent<=0, odrzucony jako evidentially dishonest + nie fixuje CRIT-01), Fix 3 (modal "expand to read", bardziej legalnie defensywny ale większy refaktor). Analiza 2026-04-24: flutter-mobile + ui-ux-designer + 2× devils-advocate rounds.

**Why:** Bug blokuje konwersję na pierwszym ekranie. GDPR Art.7 + EDPB 05/2020 NIE wymagają scroll-gate (weryfikowane — dark pattern w większości analiz). Apple App Store Review 5.1.1 nie specyfikuje scroll. MindSync NIE jest medical device (MDR Class I nie stosuje się), consent timestamps (`medical_disclaimer_accepted_at`, `gdpr_consent_at`, `age_verified_at`, `consent_version`) są pełnoprawnym dowodem informed consent bez scroll affordance.

**How to apply:**
- **Idempotentność**: zweryfikuj DOUBLE-GUARD na istniejących userach — (1) splash `hasCompletedTherapyOnboarding()` w SharedPreferences, (2) cubit `loadExistingContext()` w `therapy_onboarding_cubit.dart:79-143` sprawdza backend `context.consentGiven` → emituje `TherapyOnboardingCompleted` i navigacja do `MsRoutes.wowRoute`. OBA muszą być zachowane. Jeśli frontend flag zostanie wyczyszczony (reinstall/logout) a backend ma `consentGiven=true`, cubit short-circuituje — ekran się nie pokaże.
- **Bundle bezwzględnie wymagany**: (1) `onboarding_changeLanguage` fix we wszystkich 6 non-en ARB (de="Ändern", fr="Modifier", es="Cambiar", sv="Ändra", nb="Endre", pl="Zmień") — `app_en.arb` już OK, (2) PostHog events `onboarding_legal_gate_gate_ready` (fired when `canContinue` first true, with `time_since_step_viewed_seconds + device_model + text_scale_factor`) + `onboarding_legal_gate_abandoned` (fired from dispose gdy `consent_given==false`) — bez tego nie mierzysz skuteczności fixa, (3) widget test przy `textScaleFactor: 1.0/2.0/3.0` + `Size(320,568)` iPhone SE weryfikujący że Kontynuuj jest reachable + tappable po checkboxach, (4) build_runner PRZED commitem — Freezed state regen wymagany jeśli usuwasz `disclaimerScrolled` field (lub zostaw jako dead-code no-op dla safety), (5) backend `users.py` PUT `/therapy-context` — NIE wymaga pola `scrolled_to_bottom`, consent fields wystarczą, bez zmian server-side.
- **A11y uplift w tym samym PR**: Semantics(checked/label) na `_CheckboxTile` z `excludeSemantics:true`, `Semantics(button:true)` na "Change" language link, `Semantics(button:true)` na privacy link, `ExcludeSemantics` na dekoracyjnej `Icon(info_outline_rounded)`, `Semantics(liveRegion:true)` na helper text pod przyciskiem żeby VoiceOver ogłosił "Kontynuuj jest teraz dostępny".
- **Rollback plan**: single-PR `git revert` — brak migracji DB, brak coupling backend, zero-risk. Nie używać Firebase Remote Config feature flag na tym kroku (overkill, bug jest deterministyczny).
- **Zależne bugi do ticketu osobnego** (nie blockery): `OnboardingScheduleView` `TableCalendar height:400` na iPhone SE AX5 — cramped ale reachable przez `SingleChildScrollView` outer; `CircularProgressIndicator` saving overlay (UX: za anxious, replace z `LinearProgressIndicator`).
- **Telemetryczny success metric**: drop-off na `onboarding_step_completed` z `step_index=0` per device_model (iPhone SE/17) + text_scale_factor pre vs post release.

**Orphaned analytics**: sprawdź czy PostHog ma historyczny event `onboarding_legal_gate_scrolled` — po fixie stanie się dead; oznaczyć w dashboardzie jako deprecated.
