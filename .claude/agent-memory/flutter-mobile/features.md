# Flutter Mobile Features Reference

Detailed notes on implemented features. MEMORY.md has a concise index; this file has full details.

## Treatment Goals (Patient Read-Only View) — May 2026

- Model: `TreatmentGoalModel` (Freezed abstract) + `LocalizedString(pl, en)` at `lib/api/models/treatment_goal/treatment_goal_model.dart`
- Manager: `TreatmentGoalsManager.getMyGoals()` calls `GET /api/v1/me/goals` via `DioClient.getListMap()` — endpoint in `Endpoints.myTreatmentGoals`
- Cubit: `TreatmentGoalsCubit` (lazySingleton) — states: initial/loading/loaded(goals)/error; `firstActiveGoalTitle(localeCode)` helper for anchor widget
- UI: `TreatmentGoalsSection` — Stats tab, below GoalsSection; renders nothing on initial/error/empty; status dot + bilingual title + progress bar (only when progress>0 and not done); silent error isolation
- UI: `TreatmentGoalAnchorWidget` — Main tab compass card; reads from `TreatmentGoalsCubit` lazySingleton; self-suppresses when no active (progress/idle) goals; taps → `sl<MainNavCubit>().selectTab(3)`
- Registration: `TreatmentGoalsManager` as `registerFactory`, `TreatmentGoalsCubit` as `registerLazySingleton` (calls `loadGoals()` on creation)
- Main tab: `'treatment_goal_anchor'` key added to `mainTabDefaultWidgetOrder` in `MainTabCubit`; provided via `MultiBlocProvider` in `MainTabScreen`
- L10n: 8 ARB keys added across all 7 languages: `treatmentGoals_sectionTitle/sectionSubtitle/statusIdle/statusProgress/statusDone/statusPaused/progressLabel(percent)/anchorLabel`
- Testability pattern: `TreatmentGoalsSection(cubit: ...)` optional param bypasses GetIt in widget tests — the cubit is passed directly, avoiding `sl()` call in test environment
- Tests: 11 BLoC tests (`test/bloc/treatment_goals_cubit_test.dart`) + 20 widget tests (`test/screens/stats_tab/treatment_goals_section_test.dart`), all pass
- Status colors: progress=`#2E7D32`, done=`#1565C0`, paused=`#E65100`, idle=`MsColors.neutral[500]`

## Generic Capture Flow Pattern (Feb/Mar 2026)

- `DebriefCaptureScreen` accepts `CaptureFlowConfig` — drives debrief, prep-card, and between-session flows
- `CaptureFlowConfig.debrief()` / `.prepCard()` / `.betweenSession()` named constructors set all strings
- `DebriefCaptureCubit` takes `CaptureFlowType flowType` — switches API manager per flow type (3 managers)
- Cubit is created directly in `BlocProvider.create` (NOT via GetIt) since it needs runtime params
- Complete state holds nullable `DebriefModel?`, `PrepCardModel?`, and `BetweenSessionModel?` — screen switches widget
- Config lives at `lib/screens/therapy_capture/capture_flow_config.dart`
- PrepCardModel at `lib/api/models/prep_card/prep_card_model.dart`
- PrepCardManager at `lib/api/api_managers/prep_card_manager.dart`
- PrepCardWidget at `lib/screens/therapy_capture/widgets/prep_card_widget.dart`
- PrepCardMainTabWidget at `lib/screens/therapy_capture/widgets/prep_card_main_tab_widget.dart`
- Main tab `therapy_prep` slot now uses `PrepCardMainTabWidget` instead of placeholder

## Therapy Timeline Pattern (Phase 9, Feb/Mar 2026)

- `TherapyTimelineItem` sealed class: `TimelineDebrief`, `TimelinePrepCard`, `TimelineWeeklySummary`, `TimelineRecording`, `TimelineBetweenSession` variants
- Model at `lib/screens/therapy_tab/models/therapy_timeline_item.dart`
- Extension `TherapyTimelineItemDate` provides `.createdAt` accessor across variants
- `TherapyTabCubit` fetches debriefs + prep cards + weekly summaries + recordings + between notes in parallel using Dart 3 record destructuring
- State keeps `allItems` (unfiltered) + `items` (filtered) — filter is applied client-side
- `TherapyFilter` enum: all, debrief, preparation, between, recordings, summaries, realizations
- Detail screen pushed via `Navigator.of(context).push(MaterialPageRoute(...))` — no go_router route needed
- Debrief badge: teal `primary[50]` background; Prep badge: purple `Color(0xFFF3EEFB)` background
- Between Sessions badge: amber `Color(0xFFFFF8E1)` background, `Color(0xFFE65100)` text, lightbulb icon

## Reflect Chat Feature (Mar 2026)

- `ReflectChatCubit` replaces `ReflectConversationsCubit` — old files DELETED (Mar 2026 cleanup)
- `ReflectManager` at `lib/api/api_managers/reflect_manager.dart` — all 10 API methods
- Freezed models: `ReflectThread`, `ReflectMessageResponse`, `ReflectUsage` at `lib/api/models/reflect/`
- State: `ReflectChatState` sealed class with 4 variants: threadsLoading, threadsLoaded, chatActive, error
- `getThreads()` returns Dart 3 record `({List<ReflectThread> threads, bool hasMore})`
- Two-view screen: thread list (threadsLoaded) and chat (chatActive) in one ReflectTabScreen
- Widgets at `lib/screens/reflect_tab/widgets/`: chat_bubble, chat_input, starter_chips, thinking_indicator, thread_tile, usage_indicator
- Voice mode: `AudioChatScreen` accepts `isReflect` flag; `AudioChatCubit.initialize()` has `{isReflect, reflectThreadId}` named params
- `chatActive` state has `showNudge` field for 15-min inactivity nudge

## Session Recording Feature (Mar 2026)

- `RecordingModel`, `RecordingStatusModel`, `RecordingTrialModel` at `lib/api/models/recording/recording_model.dart`
- `RecordingManager` at `lib/api/api_managers/recording_manager.dart` — 8 methods (upload, trial, status, list, latest, get, retry, consent get/set)
- `RecordSessionCubit` at `lib/screens/fab_flows/cubit/record_session_cubit.dart` — extends `MsCubit`
- `RecordSessionState` sealed class: loading, consentWall, quickConfirm, ready, recording, tooShort, uploading, processing, completed, premiumRequired, error
- Route: `MsRoutes.recordSessionFlowRoute` = `/fab/record-session`
- Dependencies: `record: ^5.1.3`, `wakelock_plus: ^1.2.10`

## Self-Assessed Symptom Tracking Feature (Mar 2026)

- 5 Freezed models at `lib/api/models/symptom/`
- `SymptomManager` at `lib/api/api_managers/symptom_manager.dart` — 11 API methods
- `SymptomTrackingCubit` at `lib/screens/stats_tab/cubit/symptom_tracking_cubit.dart` — self-contained BlocProvider in SymptomTrackingSection
- Stats tab: SymptomTrackingSection with slider cards, SfCartesianChart (LineSeries + ScatterSeries for single point), AI descriptions
- Main tab: SymptomTrendWidget with CustomPainter sparklines, direction arrows
- Settings: SymptomsSection rewritten — backend-synced via SettingsCubit.addSymptom/removeSymptom/renameSymptom with SymptomManager
- SettingsState.symptoms changed from `List<String>` to `List<SymptomModel>` (breaking change)
- DioClient limitation: no postList method. refreshAllDescriptions uses try/catch around postEmpty

## Between Sessions Notes Feature (Mar 2026)

- `BetweenSessionModel` + `BetweenSessionGuidingQuestionsResponse` at `lib/api/models/between_session/between_session_model.dart`
- `BetweenSessionManager` at `lib/api/api_managers/between_session_manager.dart` — 8 methods
- Reuses generic `DebriefCaptureCubit` with `CaptureFlowType.betweenSession` — no separate cubit needed
- FAB flow: `BetweenSessionsFlowScreen` wraps `DebriefCaptureScreen(config: CaptureFlowConfig.betweenSession())`
- `BetweenSessionNoteWidget` at `lib/screens/therapy_tab/widgets/between_session_note_widget.dart`
- Theme: amber/orange — badge `Color(0xFFFFF8E1)`, text `Color(0xFFE65100)`, border `Color(0xFFFFE0B2)`, icon `Color(0xFFFFA000)`

## Post-Session Nudge Notifications (Mar 2026)

- Settings: `notifPostSessionNudge` (bool) + `postSessionNudgeDelayMinutes` (int, 15/30/60)
- Deep-link routing: `_handleNotificationRoute(route)` via `sl<GoRouter>().go(route)`
- Cold-start: `pendingNotificationRoute` global in main.dart, consumed by splash_screen
- Foreground nudge: `_showInAppNudgeBanner()` via BotToast — 8s auto-dismiss
- Two Android channels: `high_importance_channel` + `session_reminders`

## Realizations Collection Feature (Mar 2026)

- See `realizations.md` for full details
- `RealizationManager` at `lib/api/api_managers/realization_manager.dart` — 6 methods
- Gold theme: `Color(0xFFD4A017)`, badges, timeline filter, detail widget, long-press mark

## Monthly Therapy Audit Report (Mar 2026)

- 3 Freezed models at `lib/api/models/monthly_audit/monthly_audit_model.dart`
- `MonthlyAuditManager` at `lib/api/api_managers/monthly_audit_manager.dart` — 4 methods
- Endpoints: monthlyAudits, monthlyAuditLatest, monthlyAudit(id), monthlyAuditRetry(id)
- Dark blue theme: dot `Color(0xFF1565C0)`, badgeBg `Color(0xFFE3F2FD)`, badgeText `Color(0xFF0D47A1)`
- Detail: `MonthlyAuditWidget` — READ-ONLY, premium gated (Activity Summary free, other 5 sections locked)
- Settings: `notifMonthlyAudit` (bool) in NotificationsSection

## Therapy Tracking Signal (Mar 2026)

- `TherapyTrackingModel` at `lib/api/models/therapy_tracking/therapy_tracking_model.dart`
- `TherapyTrackingManager` at `lib/api/api_managers/therapy_tracking_manager.dart` — 3 methods
- Stats tab: `TherapyTrackingSection` — full card with signal dot, label, explanation, premium lock
- Main tab: `TherapyTrackingCompactWidget` — compact card with dot + label + chevron
- Signal values: "green" (#4CAF50), "amber" (#FF9800), "red" (#F44336)

## Goal Tracker Feature (Mar 2026)

- 3 Freezed models at `lib/api/models/goal/`
- `GoalManager` at `lib/api/api_managers/goal_manager.dart` — 8 methods
- `GoalTrackingCubit` at `lib/screens/stats_tab/cubit/goal_tracking_cubit.dart` — lazySingleton
- Stats tab: `GoalsSection` — active goal cards with popup menu, achieved/dropped sections, add bottom sheet (5 active limit)
- Main tab: `GoalProgressWidget` — compact card with flag icons + goal text

## Character Tab Feature (Mar 2026)

- 4 Freezed models at `lib/api/models/character/`
- `CharacterManager` at `lib/api/api_managers/character_manager.dart` — 4 methods
- Endpoints: characterCard, characterRefreshBio, orcaName, toneArchetype (all under `/api/v1/gamification/`)
- `CharacterTabCubit` registered as `registerFactory`, uses typed CharacterCardModel
- Level-up detection: SharedPreferences keys `characterLastUserLevel` (int), `characterLastOrcaLevel` (int)
- 5 widget files at `lib/screens/character_tab/widgets/`
- AnimatedOrca: `stage` (baby/juvenile/adult) and `happiness` (0-1) params
- Settings: `CharacterSection` — 5 archetypes (realist/coach/friend/sage/explorer), orca name TextField

## Therapy Health Check Feature (Mar 2026)

- 3 Freezed models at `lib/api/models/health_check/health_check_model.dart`
- `HealthCheckManager` at `lib/api/api_managers/health_check_manager.dart` — 6 methods
- `HealthCheckFlowCubit` — 9 states (loading through detail/error)
- Full-screen flow: `HealthCheckFlowScreen` accepts optional `existingCheckId`
- Stats tab: `HealthCheckSection` — 4 sub-views (empty, firstCheckIn CTA, due, latest)
- Main tab: `HealthCheckBannerWidget` — dismissible banner card
- Timeline: indigo theme (`Color(0xFFE8EAF6)` bg, `Color(0xFF3949AB)` text)
- `createdAt` is `DateTime?` — do NOT wrap in `DateTime.parse()`
- `Future.catchError((_) => null)` fails on non-nullable return — use try/catch

## 7/30/90 Day Snapshots Feature (Mar 2026)

- 4 Freezed models at `lib/api/models/snapshot/snapshot_model.dart`
- `SnapshotManager` at `lib/api/api_managers/snapshot_manager.dart` — 3 methods
- `SnapshotsCubit` at `lib/screens/stats_tab/cubit/snapshots_cubit.dart` — lazySingleton
- Stats tab: `SnapshotsSection` — 3 stacked expandable cards (7d/30d/90d)
- Color scheme: 7d=aquaBreeze, 30d=Color(0xFF5BA4CF), 90d=deepOcean
- shimmer package NOT available — use Container placeholders + CircularProgressIndicator
- `withOpacity()` deprecated — use `withValues(alpha: X)`

## Contextual In-App Walkthrough Feature (#19, Mar 2026)

- `WalkthroughStateModel` at `lib/api/models/walkthrough/walkthrough_state_model.dart`
- `WalkthroughManager` at `lib/api/api_managers/walkthrough_manager.dart` — 3 methods
- `WalkthroughCubit` at `lib/screens/walkthrough/cubit/` — lazySingleton
- 3 overlay widgets: welcome_overlay, tooltip_overlay (spotlight cutout), level_up
- `WalkthroughContent` — 25 static tooltip texts + 5 welcome greetings, `[orca_name]` placeholder
- Local cache: `walkthrough_completed` bool (raw key, not PreferenceKey enum)
- Settings: `resetAllTutorials()` also calls `sl<WalkthroughCubit>().resetTour()`

## Onboarding V2 (Mar 2026)

- 7-page PageView: [WelcomeSplash, LegalGate, Challenges, Intensity, Journey, Modality, Companion]
- `TherapyOnboardingCubit` at `lib/screens/therapy_onboarding/cubit/` — uses `TherapyContextRepository`, `SharedPreferencesManager`, `CharacterManager`
- State fields: `currentScreen` (0-5), `orcaName`, `selectedArchetype`, `consentGiven`, `disclaimerScrolled`, `gdprChecked`, `ageChecked`
- Key methods: `loadExistingContext()`, `acceptConsent()`, `saveChallengesAndAdvance()`, `saveIntensityAndAdvance()`, `saveJourneyAndAdvance()`/`skipJourney()`, `saveModalityAndAdvance()`/`skipModality()`, `completeOnboarding(name, archetype)`
- `TherapyContextModel` has 5 consent fields: `consentGiven`, `medicalDisclaimerAcceptedAt`, `gdprConsentAt`, `ageVerifiedAt`, `consentVersion`
- Reset: `TherapyContextManager.resetOnboarding()` + `SharedPreferencesManager.clearTherapyOnboardingCompleted()`
- Settings: "Reset onboarding" button with confirmation dialog, navigates to `MsRoutes.therapyOnboardingRoute`
- Old `/onboarding` route REMOVED from ms_routes.dart (was image-slides onboarding)
- Reuses existing widgets: `FocusAreaChip`, `SeveritySliderRow`, `CrisisBanner`, `AnimatedOrca`
- `OnboardingProgressIndicator` replaces old `OnboardingProgressDots` — "X of 5" linear bar
- Companion view: 5 archetypes (friend/realist/sage/explorer/coach) + name field, same pattern as settings CharacterSection
- `completeOnboarding()` does fire-and-forget CharacterManager calls (updateOrcaName, updateToneArchetype)
- Deleted old files: onboarding_screen.dart, welcome_view, duration_view, frustration_goals_view, focus_areas_view, severity_view, complete_view, progress_dots
