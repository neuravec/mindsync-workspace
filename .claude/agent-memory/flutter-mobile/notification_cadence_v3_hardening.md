---
name: notification-cadence-v3-hardening
description: Notification Moments enum hardening (unknownEnumValue) + pumpAndSettle gotcha discovered while testing it (2026-07-03)
metadata:
  type: project
---

## What changed (2026-07-03, on disk, NOT committed)

Backend added 2 new `moment_type` values (`DAILY_CHECK_IN`, `SESSION_MORNING_OF`) and revealed
a 3rd the client never modeled (`RE_ENGAGEMENT`, live backend-side since May 2026). Before this
batch, `MomentType` in `lib/api/models/moments/notification_moment_model.dart` had no
`unknownEnumValue`, so any moment_type the client didn't recognize threw inside `$enumDecode`.

Blast radius: `NotificationMomentsManager.getUpcoming()`/`getMomentById()` call
`NotificationMomentModel.fromJson()` directly inside a try/catch that only swallows 404 —
an enum-decode `ArgumentError` was rethrown, and `MomentsCubit.loadOnAppOpen()`'s
`Future.wait([getUpcoming(), getPendingInsights()])` treated it as a hard failure, landing the
*entire* app-open load in `MomentsState.error` — including unrelated `pendingInsights`. A single
unmapped enum from the backend blows up an unrelated data path via a shared `Future.wait`.

Fix pattern (reusable for ANY backend-enum-typed Freezed model):
1. Add a sentinel enum value, e.g. `unknown('UNKNOWN')`.
2. On the model field: `@JsonKey(unknownEnumValue: MomentType.unknown) required MomentType momentType,`.
3. Generated code changes from `$enumDecode(map, json['x'])` to
   `$enumDecode(map, json['x'], unknownValue: MomentType.unknown)` — never throws again.
4. Anywhere there's an exhaustive `switch` over the enum (here: `MomentDeepLinkScreen._dispatchByType`),
   route `unknown` (and any other undedicated type) to the existing generic fallback renderer
   (`MomentBottomSheet` via `_showGenericSheet`) — never a dead-end case.
5. `if`-based dispatch (e.g. `main_page_body.dart._showMomentSheet`, which only special-cases
   `postSessionReflection` and falls through to generic otherwise) needs NO change — already safe
   by construction. Exhaustive `switch` is the only place at risk.

Apply this same pattern to any other backend-driven enum model in this codebase before it bites
again (e.g. if `InsightType`/`FormFactor` in `app_insight_model.dart` ever get new backend values).

## Test gotcha: pumpAndSettle() + indeterminate spinner = timeout

`MomentDeepLinkScreen.build()` shows a `CircularProgressIndicator` (indeterminate) for **every**
`_DeepLinkStatus` except `expired` — including `dispatching`, i.e. while a modal bottom sheet is
open on top of it. An indeterminate spinner never lets "no more scheduled frames" become true, so
`tester.pumpAndSettle()` times out (10s) any time a test interacts with a moment that dispatches
to a sheet (as opposed to the `expired`/pure-spinner-then-nothing paths the pre-existing tests
exercised). Symptom: `pumpAndSettle timed out` thrown from inside the assertion-adjacent tool call,
before your own `expect()` lines ever run.

Fix: use bounded `tester.pump(duration)` in a loop instead of `pumpAndSettle()` for any test that
opens/interacts with a sheet from this screen:
```dart
Future<void> pumpFrames(WidgetTester tester,
    {int times = 10, Duration step = const Duration(milliseconds: 100)}) async {
  for (var i = 0; i < times; i++) {
    await tester.pump(step);
  }
}
```
This is a pre-existing latent quirk in the screen (harmless in prod — the sheet visually covers
the spinner — but wastes a frame budget while a sheet is open). Out of scope to "fix" the widget
for this task; the test workaround is the correct scope-preserving move.

Also hit: default test `devicePixelRatio` is 3.0. Setting only `tester.view.physicalSize` without
also pinning `tester.view.devicePixelRatio = 1.0` shrinks the logical viewport (e.g. 800x1400
physical → ~266x466 logical), which can push a secondary CTA (stacked below a primary CTA in a
Column) outside hit-testable bounds even though `find.text()` still finds it in the tree. Always
set both together in tests that tap buttons inside `MomentBottomSheet`/similar sheets:
```dart
tester.view.physicalSize = const Size(800, 1400);
tester.view.devicePixelRatio = 1.0;
addTearDown(tester.view.reset);
```

## Files touched
- `lib/api/models/moments/notification_moment_model.dart` (+ `.freezed.dart`/`.g.dart` regenerated)
- `lib/screens/moments/moment_deep_link_screen.dart` (switch cases only — `main_page_body.dart`
  needed no change, see above)
- Tests: new `test/api/models/moments/notification_moment_model_test.dart`; additions to
  `test/api/notification_moments_manager_test.dart`, `test/bloc/moments/moments_cubit_test.dart`,
  `test/screens/moments/moment_deep_link_screen_test.dart`
- Left uncommitted on `dev` per task instructions — lead coordinates commit after QA.
