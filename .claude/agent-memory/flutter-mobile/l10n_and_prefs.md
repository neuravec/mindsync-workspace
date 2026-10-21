---
name: l10n-and-prefs
description: SharedPreferences key/type pattern, l10n infrastructure setup, and Polish localization date/locale fixes
metadata:
  type: project
---

## SharedPreferences Pattern

- Keys in `lib/services/preference_keys.dart` (enum `PreferenceKey` + extension with `type` getter)
- New keys need both enum value AND a case in the `type` switch — `bool`/`String`/`int`/`List<String>` supported
- Methods in `lib/services/shared_preferences_manager.dart` call `_sharedPreferencesService`
- Keys added over time: `mainTabWidgetOrder` (List<String>), `fabFirstLaunchSeen` (bool), `therapyScheduleJson` (String), `appLocaleCode` (String), `therapyFrequency` (String), `customIntervalDays` (int), `nextSessionAnchorDate` (String), `premiumBannerDismissedAt` (String, ms epoch), `therapistsJson` (String, JSON array), `customSessionsJson` (String, JSON array), `onboardingUidMigrationDone` (bool)

## Localization (L10n) Infrastructure (Mar 2026)

- Config: `l10n.yaml` in project root — output class `S`, output dir `lib/l10n/generated/`, `synthetic-package: false`
- ARB template: `lib/l10n/app_en.arb`
- `SupportedLocale` enum: `lib/core/locale/supported_locale.dart` — 7 locales (en/de/fr/nb/sv/es/pl)
- `LocaleCubit`: `lib/core/locale/locale_cubit.dart` — lazySingleton, persists to SharedPreferences, syncs from backend
- `l10n_extensions.dart`: `context.l10n` convenience extension
- `LocaleCubit` registered in service_locator, provided via `BlocProvider` in main.dart, consumed by `BlocBuilder` in mind_sync_app.dart
- `S.delegate` added to `localizationsDelegates` in MaterialApp.router
- Old `Language` class removed from `language_selection.dart`; replaced by `SupportedLocale` across settings_state, settings_cubit, settings_body
- `pubspec.yaml` has `generate: true` under `flutter:` section
- gen-l10n cannot run cleanly due to a pre-existing Polish ARB syntax error in `stats_scoresCount` plural (`=4` is invalid); generated file is stale but harmless — extra abstract methods don't cause compile errors
- ARB files cleaned of walkthrough_/settings_resetTutorials keys (Mar 2026) and all zombie notification-toggle keys (May 2026 Faza 4 — see [[settings_and_data_history]])

## Polish Localization Fixes (May 2026)

- `Intl.defaultLocale` must be set in ALL 3 paths of `LocaleCubit`: `_initialLocale()`, `changeLocale()`, `syncFromBackend()` — without this, `DateFormat()` without explicit locale uses en-US regardless of app language
- `DateFormat.Hm()` preferred over `DateFormat('HH:mm')` — locale-aware 24h time; also respects `Intl.defaultLocale`
- New ARB keys require `flutter gen-l10n` before `flutter analyze` — stale generated `S` class causes `undefined_getter` errors
- Unicode escape sequences (`—`, `ś`, etc.) in ARB values prevent multi-line Edit tool matches — edit such keys individually
- All 7 ARB files (en/de/fr/nb/sv/es/pl) must stay in sync — missing keys cause `flutter gen-l10n` untranslated warnings
- `FittedBox(fit: BoxFit.scaleDown, child: Row(...))` — overflow-safe pattern for large headline text in Row
- Subscription comparison/tier/feature keys and symptom preset keys (`symptomPresetEnergyMotivation`, `symptomPresetSuicidalIdeation`) added to all 7 ARBs in this pass
- ARB key removal on Windows: use `grep -v "pattern" file > tmp && mv tmp file` (Python 3 not in PATH)
