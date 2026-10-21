---
name: feature-history-2026-05
description: Treatment Goals (patient read-only) and account-deletion flow implementations from May 2026
metadata:
  type: project
---

## Treatment Goals — Patient Read-Only (May 2026)

- Model: `TreatmentGoalModel` + `LocalizedString(pl,en)` at `lib/api/models/treatment_goal/treatment_goal_model.dart`
- Endpoint: `GET /api/v1/me/goals` → `Endpoints.myTreatmentGoals`; manager at `lib/api/api_managers/treatment_goals_manager.dart`
- Cubit: `TreatmentGoalsCubit` lazySingleton; `firstActiveGoalTitle(localeCode)` for anchor
- UI: `TreatmentGoalsSection` (Stats tab, below GoalsSection) — silent error isolation; status dot + progress bar
- UI: `TreatmentGoalAnchorWidget` (Main tab) — self-suppresses when no active goals; tap → Stats tab index 3
- Testability: `TreatmentGoalsSection(cubit: ...)` optional param bypasses GetIt in widget tests
- L10n: 8 keys added to all 7 ARBs (`treatmentGoals_*`); gen-l10n run with Flutter 3.41.1
- Tests: 11 BLoC tests + 20 widget tests, all pass
- NOTE (Jul 2026 project memory flagged): `/me/goals` response mismatch reported in MS_3 batch — verify contract still holds before further work here

## Delete Account Flow (May 2026)

- Live path: `DangerZoneSection` → reauth in widget → `SettingsCubit.deleteAccount()` (no BuildContext)
- Operation order: backend DELETE → `user.delete()` → analytics/PostHog reset → `signOut()` → `sl<GoRouter>().go(welcomeRoute)`
- `UsersManager.deleteAccount()` swallows 404 (idempotent retry path — backend row already gone)
- `SettingsCubit` constructor accepts optional `UsersManager?` + `FirebaseAuth?` for test injection (`??sl()` fallback)
- Password dialog is `_PasswordReauthDialog` StatefulWidget (owns controller lifecycle — no leak on back-dismiss)
- Validate empty password BEFORE `Navigator.pop()` so toast fires while context is still mounted
- ARB keys `error_requiresRecentLogin` + `error_emptyPassword` added but used as literals (gen-l10n stale)
- `AccountCubit.deleteAccount()` removed (was dead code — no callers); `AccountCubit` still alive for profile editing
- Tests: `test/screens/settings/cubit/settings_cubit_delete_account_test.dart` — 6 tests, no GetIt required
