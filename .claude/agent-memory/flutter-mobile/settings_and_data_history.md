---
name: settings-and-data-history
description: Settings notification field cleanup, save-feedback UX pattern, MainTabCubit data loading, and therapy schedule persistence/sync
metadata:
  type: project
---

## SettingsState Notification Field Cleanup (Faza 4, May 2026)

- REMOVED from SettingsLoadedState: notifTherapyReminder, notifBetweenSessions, notifWeeklySummary, notifMonthlyAudit, notifStreaks, notifMilestones, notifPostSessionNudge, postSessionNudgeDelayMinutes, notifHealthCheck, healthCheckReminderFrequency, notifSymptomTracking, notifMidWeekCheckIn, notifPreSessionCheckIn
- KEPT: notifOsEnabled (OS permission banner), dndStartHour/dndEndHour (quiet hours), notificationEnabled/notificationInterests (V2 master controls)
- REMOVED from SettingsCubit: toggleNotification(String,bool), updatePostSessionNudgeDelay(), updateHealthCheckReminderFrequency()
- REMOVED from notifications_section.dart: NotifToggleLegacy class
- REMOVED (Jun 2026): notificationIntensity field from SettingsLoadedState, setNotificationIntensity() from SettingsCubit, _IntensityPicker widget from notifications_section.dart, notifSettings_intensity*/notifSettings_recommended ARB keys from all 7 ARBs — backend removing notification_intensity field in parallel
- DELETE /api/v1/users/fcm_token does NOT exist in backend — FCM token cleanup at logout is not implemented (N/A for Faza 4)
- settings_cubit_delete_account_test.dart has 7 pre-existing failures (GetIt registration missing SymptomManager etc.) — unrelated to Faza 4

## Settings Save Feedback Pattern (SC02, Mar 2026)

- `MsMessage.showSaved(text)` — 1500ms toast with green check. Used after all cubit saves.
- `SaveFeedbackIndicator` widget — inline animated checkmark used in `_NotifToggle` rows.
- Text fields (orca name) use `FocusNode` blur to fire backend sync + toast — NOT on every keystroke.
- Pattern: `updateX()` updates local state only; `saveX()` or blur handler updates state + backend + toast.
- `SettingsCubit.saveOrcaName(name)` — called on blur from `_OrcaNameField` in character_section.
- `TherapyBackgroundSection` — session duration dropdown; `updateTherapyDuration` fires on every dropdown change.
- `CharacterSection` no longer includes `_OrcaNameField` (removed in Settings V2 — orca naming is onboarding-only now).
- Frustration chips/text REMOVED from onboarding Journey step (Jun 2026) — therapist guidance: negatively-framed questions not at start. ARB keys preserved. Backend fields nullable, not sent from Journey view anymore.

## MainTabCubit Data Loading (Phase 10)

- `MainTabCubit` loads `latestPrepCard` + `latestDebrief` concurrently after initial state emission
- `hasTherapySchedule` read from `SharedPreferencesManager.hasTherapySchedule()` on init
- Card widgets receive data from `MainTabLoadedState` fields

## Therapy Schedule Persistence & Sync

- Schedule saved to SharedPreferences as JSON string (key: `therapyScheduleJson`)
- Frequency saved as String (key: `therapyFrequency`, default `'weekly'`); custom interval as int (key: `customIntervalDays`)
- `SettingsCubit` persists + fire-and-forget syncs to `PUT /api/v1/users/therapy-schedule` via `UsersManager.syncTherapySchedule`
- Endpoint: `Endpoints.therapySchedule`
- `nextSessionAnchorDate` (String, ISO-8601) used by `MainTabCubit._computeNextCustomSession` for custom-interval scheduling
