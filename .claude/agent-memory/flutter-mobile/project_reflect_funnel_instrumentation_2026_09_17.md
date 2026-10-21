---
name: reflect-funnel-instrumentation-2026-09-17
description: FE-4 Reflect entry funnel PostHog consolidation, the structural privacy guard pattern that replaces "no leaks" comments with assertions, and the contract-vs-shipped decisions taken along the way
metadata:
  type: project
---

FE-4 of the Reflect entry batch (`TASKS-reflect-entry.md`). Commit `7f9f897` on `dev`,
local only, not pushed.

## What this batch established, reusable beyond Reflect

**The structural privacy guard.** `mindsync_app/test/support/reflect_analytics_guard.dart`
is the pattern worth copying for any feature that emits analytics in this product. It takes
the captured `(event, properties)` pairs and asserts four things rather than one:

1. no fixture string appears in any property value (the obvious check);
2. every string value is in an explicit allowed vocabulary;
3. every value is a primitive, or a list of primitives (objects get stringified on the way
   to PostHog, which is exactly how a model carrying a label leaks);
4. no string exceeds 40 characters.

**Why:** 2 to 4 are what catch content nobody thought to put in the fixture list. A guard
that only greps for known fixtures passes happily on a free-text field that happens not to
match one. Checks 2 and 4 both fail on it.

**How to apply:** drive every emitting path with distinctive fixture content, collect the
property maps through a mocked `PostHogService` in GetIt, call the guard, and pass
`expectedEvents` so it cannot pass vacuously. Then prove it is not vacuous by temporarily
adding a probe property and watching it go red. Four probes were used here (a seed label, a
whole Freezed model, a long sentence, a short unseen string); each failed on a different
assertion.

**Gotcha when building the allowed-value set:** it is a `const Set<String>`, so two
constants with the same literal value (`reflectEntryPointModeChoice` and
`reflectStageModeChoice` are both `'mode_choice'`; `reflectModalityUnknown` and the voice
`'unknown'` reason) are a compile error, not a duplicate entry. Leave one out with a
comment saying which and why.

## Decisions taken, with the reasoning

- **`premium_gate_reflect_voice` beat the contract's `reflect_voice`.** The contract said
  `trigger_feature=reflect_voice`, but `ReflectTabScreen._showVoiceUpsell` has pushed
  `premiumGateTrigger('reflect_voice')` since before this batch (present in `d3ba054`), so
  that value may already be flowing in production. The new entry screen was unified onto
  the shipped value rather than the contract's, because two buckets for the same wall would
  break the paywall question the contract itself asks. Renaming a possibly-live value is
  the thing to avoid.
- **A locked voice tap fires BOTH `reflect_mode_selected` and `reflect_voice_locked_tapped`.**
  Not one instead of the other. They answer different questions. A mode-choice conversion
  funnel has to exclude `mode=voice AND is_premium=false` to avoid counting a selection that
  can never proceed.
- **`reflect_ui_session_ended` deliberately does NOT carry `seed_source`.**
  `GET /reflect/threads` does not return a thread's seed, so a resumed thread could not
  report one and the property would understate exactly the seeded sessions the question is
  about. The answer is a PostHog join on `thread_id` between the backend's
  `reflect_session_started` (which has `seed_source`) and `reflect_ui_session_ended`.
- **`entry_point=notification` is declared but never emitted.** The REFLECTION_INVITATION
  push and an in-app deep link both resolve to `/main-page/tab/reflect?new=true`, so the
  client cannot tell them apart. Splitting them needs the notification handler to tag
  `MainNavCubit.pendingAction`, which is a deep-link-contract change. Join on
  `notification_opened` in the same session until then.

## Test techniques that worked here

- **Proving attribution across a route boundary.** `test/navigation/ms_routes_reflect_entry_extra_test.dart`
  calls the REAL `MsRoutes.router.configuration` route builders with a synthetic
  `GoRouterState(..., extra: ...)` and reads the returned widget's fields. Constructing the
  screen directly proves nothing about the `extra` hand-off, and the two halves can drift
  while every event still fires, just attributed to the default. Same trick as the B17 and
  CS-08 tests.
- **Proving an event does not double-fire on rebuild.** `tester.binding.setSurfaceSize(...)`
  then back to `null` rebuilds the subtree without recreating the `State`, which is exactly
  how a `build`-time capture double-counts.
- **`tester.pageBack()` needs an AppBar back button.** A stubbed paywall route with a bare
  `Scaffold(body: Text(...))` has none; use `tester.binding.handlePopRoute()`.
- **mocktail's `verify(...).captured` drains what it returns.** Call the capture helper once
  per test and hold the list, or the second call comes back with only the new events.
- **`test/ui` and `test/screens` pre-existing failures as of `5ff4ab4`:** 18 in `test/ui`
  (13 `test/ui/reflect_tab` visual + 5 `test/ui/settings/widgets/save_feedback_indicator_test.dart`)
  and 12 in `test/screens` (6 `therapy_tab/therapy_card_detail_screen_error_test.dart`,
  3 `wow/wow_screen_adaptive_cta_test.dart`, 2 `fab_flows/record_session_appbar_close_test.dart`,
  1 `therapy_onboarding/onboarding_lead_source_view_wave4_test.dart`). Measured in a
  `git worktree` at the base commit, not assumed.
