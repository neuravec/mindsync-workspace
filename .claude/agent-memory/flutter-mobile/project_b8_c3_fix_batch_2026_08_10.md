---
name: b8-c3-fix-batch-2026-08-10
description: B8-fix (SettingsScreen persistent back button) + C3-fix ($is_testflight coverage misdiagnosis corrected) — 2026-08-10, both committed locally on dev, not pushed
metadata:
  type: project
---

## B8-fix — SettingsScreen persistent back button (commit 768eac3, dev, local only)

Source: rage-click audit `analytics-reports/2026-08-10-rageclick-audit.md` (33
`$rageclick` events/14d, one user 3 separate days). Root cause: `SettingsHeader`
(back button) only existed inside `SettingsBody`, i.e. only in
`SettingsLoadedState`. `SettingsCubit.init()` does several sequential +
parallel network calls, so `SettingsLoadingState` (bare
`Center(CircularProgressIndicator())`, no `NoDataState`/`ErrorState` either)
could sit on screen long enough for users to rage-tap where the button was
about to appear.

**Fix**: `lib/screens/settings/settings_screen.dart` now wraps the whole
`switch(state)` in a single `MsAppScaffold` + `SafeArea` +
`Padding(left:20,right:20,top:30)` + `Column([SettingsHeader(), Expanded(switch)])`
— header renders once, for all 4 states. `lib/screens/settings/settings_body.dart`
lost its own `MsAppScaffold`/`SafeArea`/header/outer padding (now just
`GestureDetector` + `SingleChildScrollView` + `Padding(bottom:30)` — the
`bottom:30` is the only remnant of the old `symmetric(20,30)`, since
horizontal:20/top:30 now come from the parent). This reproduces the
loaded-state layout pixel-for-pixel while giving loading/no-data/error a
background + header they never had before (intentional — that's the fix).

**Test**: `test/screens/settings/settings_screen_test.dart` — mocks
`SettingsCubit` via GetIt singleton (screen reads it via `sl<SettingsCubit>()`
in `initState`, not `context.read`/`BlocProvider(create:)` — same pattern as
[[msv32-f3-timeline-summary-error-state]]'s `TherapyTabScreen` gotcha). Pushes
the screen on a real minimal `GoRouter` (needed because `SettingsHeader`'s
back button calls go_router's `context.pop()`). Covers all 4 states.

**New widget-test gotcha found**: `pumpAndSettle()` after tapping "back"
ALSO times out while `SettingsLoadingState`'s indeterminate spinner is still
on screen mid-pop-transition (not just on the initial push) — the outgoing
route's widget subtree (with its perpetually-animating spinner) stays
mounted until the pop transition itself finishes, and `pumpAndSettle()` loops
on that. Fix: never use `pumpAndSettle()` anywhere this widget might be
onscreen, not even after navigation actions — use a bounded pump loop
instead (`for (var i=0;i<10;i++) await tester.pump(Duration(milliseconds:100))`;
a single `pump()+pump(400ms)` was NOT enough, root cause not fully
pinned down but the loop reliably works). Extends the existing
"pumpAndSettle+indeterminate-spinner" note in [[notification-cadence-v3-hardening]].

**Incidental fix (same commit)**: widget-testing the loaded state surfaced a
real, pre-existing, unrelated 1.8px `RenderFlex` overflow in
`lib/screens/settings/widgets/premium_banner.dart` — the "Subscribe" CTA
`Container` was a fixed `width: 206` too narrow for its `Text` + arrow icon
in English locale. Confirmed pre-existing (reproduces identically on
`git stash` of just my 3 changed files) and width-independent (fixed
container, unrelated to screen size or my restructuring). Widened to 212.
Flagged as incidental/out-of-scope in the commit message rather than folded
silently into the B8-fix narrative.

## C3-fix — `$is_testflight` coverage "gap" was a misdiagnosis (commit d3955a6, dev, local only)

Source: `analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md` (integration-devops)
flagged `$is_testflight` at ~22-25% property coverage on `posthog-flutter`
events vs. ~100% for `$is_emulator`, hypothesizing an async super-property
registration race in the Flutter client, and asked flutter-mobile to find the
root cause.

**Finding**: `lib/core/analytics/posthog_service.dart` (the only PostHog
touchpoint in `lib/`) never sets either property — both are computed
entirely inside the native PostHog iOS/Android SDKs (pulled in transitively
via `posthog_flutter`'s `pubspec.lock` entry, no vendored source to
patch). There is no Dart-level hook to await/control that native
computation (`Posthog()`'s public API has `register()`/`unregister()` for
super properties but no "static context ready" signal).

**Decisive check** (spawned `posthog-data-extractor`, raw extract at
`analytics-reports/raw/2026-08-10-testflight-coverage-os-split.md`):
`$is_testflight` coverage is **100.00%** on iOS/iPadOS, both aggregate and
per-session (15 sampled sessions, zero mixed-coverage sessions), zero
exceptions in the 14d window. The reported ~22-25% aggregate is pure
platform-mix arithmetic: iOS+iPadOS = 24.5% of all `posthog-flutter` traffic,
Android is ~75% and structurally can never carry `$is_testflight` (TestFlight
doesn't exist there) — not a timing gap, not missing instrumentation.

**Outcome**: no code fix applies. Documented the corrected root cause as a
doc comment in `PostHogService` (so it isn't re-flagged as a client bug next
time someone reads the raw coverage %) and added
`test/core/analytics/posthog_service_init_gating_test.dart` — a regression
test for the one thing this file's code DOES control (init() gates
capture/identify/reset/etc. behind `_initialized`, so nothing in this app
can emit an event through this wrapper before `Posthog().setup()` runs).
Any future query gating on `$is_testflight` must also scope
`$os IN ('iOS','iPadOS')` or it will misread normal Android traffic as a
coverage gap — that's the actual, correct fix, and it lives in the querying
layer (posthog-data-extractor/growth-analyst), not in app code.
