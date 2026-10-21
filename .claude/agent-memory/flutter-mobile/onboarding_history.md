---
name: onboarding-history
description: Splash-resolve retry logic, legal gate scroll-gate removal, and the May 2026 login/welcome/onboarding visual polish pass
metadata:
  type: project
---

## Splash Retry + Onboarding Error Fixes (Apr 2026, F1-F4)

- F1: `_resolvePostLoginDestination()` returns `String?` — null means error, retry overlay shown
- F1: Retry logic: 2 attempts, delays `[300ms, 600ms]`; DioException 404 → onboarding (not error); other failures → `_resolveError=true` + error overlay with "Try Again" button
- F1: PostHog event `AnalyticsEvents.splashResolveFailed = 'splash_resolve_failed'`
- F2: `TherapyOnboardingError` case added to `BlocConsumer.listener` in `therapy_onboarding_screen.dart` — logs `onboarding_load_error` to PostHog
- F3: `onboarding_legal_gate_view.dart` builder: `TherapyOnboardingLoading` → `CircularProgressIndicator`; `TherapyOnboardingError` → `OnboardingErrorView` (retry calls `loadExistingContext()`); saving → `SizedBox.expand()`; loaded → full UI
- F3: `OnboardingErrorView` widget at `lib/widgets/onboarding_error_view.dart` — reusable, takes `onRetry: VoidCallback`
- F4: `hasCompletedTherapyOnboarding({String? uid})` — UID-scoped key `u_{uid}_therapyOnboardingCompleted`; uid=null → false
- F4: One-shot migration in `_migrateOnboardingKey(uid)` — guarded by `onboardingUidMigrationDone` bool key; copies legacy `therapyOnboardingCompleted` if true, removes it, sets sentinel
- F4: New PreferenceKey: `onboardingUidMigrationDone` (bool)
- F4: All 3 callers updated with uid: splash_screen, therapy_onboarding_cubit, settings_cubit
- L10n: 4 new keys added to all 7 ARBs + generated files: `onboarding_loadError`, `onboarding_loadErrorRetry`, `splash_resolveError`, `splash_resolveErrorRetry`

## Legal Gate Fix (Apr 2026)

- `disclaimerScrolled` field + `setDisclaimerScrolled()` method REMOVED from `TherapyOnboardingState`/`TherapyOnboardingCubit`
- `canContinue = gdprChecked && ageChecked` — scroll-gate eliminated (GDPR/EDPB/HIG/M3 don't require it)
- `onboarding_legal_gate_view.dart` rewritten: outer `Column { header + _LanguageBanner + Expanded(SingleChildScrollView) + helper text + button + SafeArea bottom }` — button sticky, no scroll controller
- Disclaimer is a plain `Container` block (no inner Expanded/Scrollbar/ScrollController), expands to content height
- Helper text `onboarding_consentRequired` shown when `!canContinue`, wrapped in `Semantics(liveRegion: true)`
- Accessibility: `_CheckboxTile` wrapped in `Semantics(container,checked,label,onTap,excludeSemantics:true)`; info icon in `ExcludeSemantics`; privacy link `GestureDetector` → `Semantics(button)+InkWell`; "Change" `GestureDetector` → `TextButton(padding:zero,minimumSize:zero,shrinkWrap)`
- ARB: `onboarding_changeLanguage` translated in 6 non-EN locales; new key `onboarding_consentRequired` in all 7 ARBs

## Login/Welcome/Onboarding Polish (May 2026, Poprawki 1-11)

- M3AuthField focus color: `_kFocusColor = Color(0xFF78D0D0)` (primary[300] aqua/mint) — NOT coralPink; red/coral focus border looks like validation error
- Auth screen (login/signup): `MsAppScaffold(backgroundColor: MsColors.oceanMist)` + Container(color:oceanMist) — both required for uniform bottom background
- Back arrow in auth: `Icons.arrow_back_rounded` — use rounded variant throughout auth screens
- Lock icon: use `Assets.svg.lockFilled` for password-hidden state; `Assets.svg.lockOpen` for visible state
- TermsOfServiceCheckbox: rewritten to use AnimatedContainer (same as RememberMeCheckbox) — no more material Checkbox with coralPink activeColor; deepOcean fill, 180ms animation
- WelcomMainButton: Material+InkWell+Ink(decoration) pattern for press ripple — GestureDetector+Container has no splash
- Onboarding CTAs: ALL onboarding step buttons (legal gate, challenges, intensity, journey, modality, schedule, companion, lead source) → `MsColors.coralPink` bg + `MsColors.deepOcean` text. Auth buttons stay dark-green/teal.
- Final onboarding button text: `onboarding_done` key ("Gotowe"/"Done") on LeadSourceView (step 7/7)
- `OnboardingModalityView`: added `'other'` option (index 8) + free-text TextField; `_buildSelectedList()` encodes custom text as `'other:CustomText'`; `dispose()` required for `_otherController`
- Keyboard dismiss on screen transition: `FocusManager.instance.primaryFocus?.unfocus()` in `_jumpToScreen()` — centralized in TherapyOnboardingScreen
- Time picker: `showTimePicker` REPLACED everywhere by [[ms_time_picker]] `MsTimePicker.show(ctx, initialTime:)` — 4 replaced sites: `onboarding_schedule_view.dart` (2×), `therapy_schedule_section.dart` (1×), `custom_calendar_view.dart` (1×)
- `TimePickerThemeData` in `AppTheme.theme` is now unused but harmless — do NOT remove it (may be referenced elsewhere)
- PersonaliseView: added `focusedBorder: primary[500]` to name MsInput (4.1); gender/pronouns dropdown: `(isExpanded || value != null)` condition for teal border (4.2); SizedBox(height: 160) → SizedBox(height: 24) before button (4.3)
- Journey screen keyboard: when keyboard open, hide progress indicator + title + bottom buttons via `if (!keyboardOpen)` wrapping the header section
- Companion screen: `autofocus: false` (was true), extra `SizedBox(height: 8)` before TextField, `contentPadding: EdgeInsets.fromLTRB(16,20,16,10)` to prevent floating label clipping
- Widget test pattern for scrollable list items: `await tester.binding.setSurfaceSize(Size(400, 2400))` + `scrollUntilVisible(finder, 100)` + `warnIfMissed: false` for tap on items near bottom
