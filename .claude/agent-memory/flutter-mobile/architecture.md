---
name: architecture
description: Core project structure, BLoC/Freezed conventions, navigation architecture, DI patterns, and FVM/build tooling on Windows
metadata:
  type: project
---

## Project Structure Notes

- All screens are under `lib/screens/` (NOT `lib/ui/screens/` as the system prompt says)
- All models are under `lib/api/models/` (NOT `lib/data/models/`)
- All API managers are under `lib/api/api_managers/`
- Service locator: `lib/core/service_locator.dart` — GetIt instance as `sl`
- Navigation: go_router via `lib/navigation/ms_routes.dart`

## Architecture Notes

- BLoC pattern: Cubit subclasses that extend `MsCubit<State>` (custom base class in `lib/core/app_cubit/ms_cubit.dart`)
- Freezed models: `abstract class` with `@freezed` — NOT plain `class` (Freezed 3.x requirement)
- `MainPageCubit.userInfo` is a raw field (not inside state) — populated by `carouselCheck()` on init
- Freezed 3.x sealed classes: NO `.when()`/`.maybeWhen()` — use Dart 3 `switch` expressions instead

## New Navigation Architecture (Feb 2026)

- `MainPageBody` uses `PageView` (swipeable) with 5 tabs via `MainNavCubit`
- 5 tabs: MainTab, TherapyTab, ReflectTab, StatsTab, CharacterTab
- `MsFab` is a `Positioned` overlay in the root Stack, bottom-right above BottomNavigationBar
- `MainNavCubit` is `lazySingleton`; tab cubits (MainTabCubit, TherapyTabCubit, StatsTabCubit, CharacterTabCubit) are `registerFactory`
- `ReflectChatCubit` is `lazySingleton` (replaced ReflectConversationsCubit, provided at MainPageScreen level for persistence)
- `MainTabCubit` uses `SharedPreferencesManager` for widget order persistence

## Preserved Files (NOT deleted from daily_page/)

Phase 7 deletes the daily_page screens but these cubit/widget files must be KEPT (still referenced):
- `lib/screens/main_page/daily_page/cubit/` — all 4 cubits (DailyPageCubit, BackgroundTaskCubit, StarterPackageCubit + states)
- `lib/screens/main_page/daily_page/widgets/trial_ended_popup.dart`
- `lib/screens/main_page/daily_page/widgets/free_trial_welcome_popup.dart`
- `lib/screens/main_page/daily_page/widgets/trial_start_popup.dart`
- `lib/screens/main_page/daily_page/widgets/daily_description_text.dart`
- `lib/screens/main_page/daily_page/widgets/journey_strip.dart`
- `lib/screens/main_page/daily_page/widgets/post_conversation_insight_modal.dart`
- `lib/screens/main_page/analytics_page/cubit/` — AnalyticsCubit + state + mode (still in service_locator)
- `lib/screens/main_page/summaries_page/cubit/` — SummariesCubit + state + mode (still in service_locator)
- `lib/screens/summary_records/cubit/` — SummaryRecordsCubit + state (still in service_locator)

## MsFab Pattern

- `MsFab` takes `onFlowSelected: ValueChanged<FabFlowType>` and `onExpandedChanged: ValueChanged<bool>?`
- `onExpandedChanged` wires to `MainPageBodyState._isFabExpanded` for the full-screen dim overlay
- Pulse animation on first launch via `SharedPreferencesManager.hasSeenFabFirstLaunch()`

## Freezed Model Rules

- ALWAYS use `abstract class Foo with _$Foo` — plain `class` breaks Freezed 3.x mixin resolution
- Sealed union states: `@freezed sealed class` — generates concrete classes only, no `.when()`
- Data models with `fromJson`: `@freezed abstract class` + `factory X.fromJson(...)` + `part X.g.dart`
- After any model change: run `fvm flutter pub run build_runner build --delete-conflicting-outputs`
- Backend-driven enum fields: add an `unknown` sentinel value + `@JsonKey(unknownEnumValue: X.unknown)` on the field — see [[notification_cadence_v3_hardening]] for the full pattern and why it matters (prevents one unmapped backend enum value from throwing and tanking unrelated data via a shared `Future.wait`)

## firebase_auth UserInfo Conflict

`firebase_auth` exports a `UserInfo` class that conflicts with `mindsync_app/api/models/users/user_info.dart`.
Fix: `import 'package:firebase_auth/firebase_auth.dart' hide UserInfo;`

## flutter analyze via fvm on Windows

- Must call via `cmd //c "cd <project> && fvm flutter analyze"` — direct bash call exits 1 always
- "No issues found!" in output = clean even if exit code = 1 from cmd wrapper
- Always run `build_runner` before `analyze` if any `part` directives point to generated files

## FVM on Windows (updated Mar 2026)

- FVM not in PATH; use `.fvm/flutter_sdk/bin/flutter` directly
- For flutter analyze via cmd: `cmd //c "C:\...\..fvm\flutter_sdk\bin\flutter analyze"`
- intl version: FVM Flutter 3.27.0 requires intl ^0.19.0; system Flutter 3.41.1 requires ^0.20.2 — always use FVM (but see [[feedback_intl_version_pinning]] in the user's memory — pin currently ^0.20.2 since the Apr 2026 Xcode 26 migration)
- build_runner via FVM: `.fvm/flutter_sdk/bin/flutter pub run build_runner build --delete-conflicting-outputs`
- pubspec.yaml SDK constraint is `>=3.11.0` — FVM 3.27.0 (Dart 3.6.0) cannot resolve it; use system Flutter 3.41.1 (Dart 3.11.0) for build_runner + analyze (system Flutter is on PATH as plain `flutter`, confirmed working 2026-07-03)
