---
name: project-account-scoped-reset-2026-10-12
description: Account-change reset of GetIt lazy singletons (759147f on fix/account-scoped-reset, local, not pushed); registerAccountScoped registry, sign-out window hazards, kept-singleton list, test gotchas
metadata:
  type: project
---

Fix for TestFlight 2.0.109 stale-account bug (next account saw/wrote previous account's focus areas and habits, 404s on score/check writes). Commit 759147f on branch fix/account-scoped-reset in worktree mindsync-frontend-wt-acct-reset (from origin/dev 08bf27c), NOT pushed as of 2026-10-12; lead pushes after QA + security review.

**Design (lib/core/account_scope_reset.dart):**
- `registerAccountScoped<T>(create, dispose:)` in service_locator = account-scoped (20 types); plain `registerLazySingleton` = app-scoped. The split is pinned by a source-parsing test (test/core/account_scope_reset_test.dart) with a reason per kept type, so a new lazy singleton forces a decision.
- `resetAccountScopedState()` = MainPageCubit.clearForAccountChange + SettingsCubit.clearForAccountChange (callers of signOut/deleteAccount: cleared, never closed) + UsageCubit.reset + resetFirstWeekForAccountChange + close/forget all registry entries. Before PostHog reset.
- `dropAccountScopedStateOfOtherAccounts()` in MainPageScreen.initState: safety net, drops instances whose creation uid != current uid.

**Why non-obvious:**
- Sign-out window: `selectTab(0)` while the main page is still mounted fires tab listeners (MainTabScreen reload, TherapyTab guard) that call `sl<X>()` and REBUILD dropped cubits with the old token; this is what put `habit_tracker_viewed` on the auth screen. Fix: post-frame `selectTab(0, track: false)` after `emit(loading)` tears the page down. In the delete path, MainPageCubit loading emission tears down the offstage Home before card rebuilds.
- get_it 7.7.0 has NO `checkLazySingletonInstanceExists`; `resetLazySingleton` is async but nulls the instance synchronously (dispose errors surface as future errors). Registry tracks `live` + owner uid itself.
- bloc_test MockCubit does NOT stub `isClosed` (mocktail TypeError) - never guard widget code on `context.read<X>().isClosed` where tests use MockCubit.
- BackgroundUploadCubit captured TherapyTabCubit at construction; now takes `therapyTabCubitResolver` (only if live). TherapyTabCubit is still built eagerly at splash (preserved).

**Open questions / observed, not fixed:** BackgroundUploadCubit, BackgroundTaskCubit, ConversationsManager kept (in-flight uploads/jobs of the old account); splash definitive-404 has no PostHog reset (pre-existing); MainTabScreen tab listener loads HabitsCubit (fires habit_tracker_viewed) on Home visits even in first-week mode where the card is not shown; SettingsCubit.init reads device-level prefs (schedule) not keyed by account; reflect_ui_session_ended never fires for a sign-out mid-session.

Related: [[project-first-week-wp0-part-a-2026-10-08]], [[feedback-cubit-test-pattern]]
