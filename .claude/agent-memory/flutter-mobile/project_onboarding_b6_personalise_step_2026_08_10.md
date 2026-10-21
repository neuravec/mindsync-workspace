---
name: project-onboarding-b6-personalise-step-2026-08-10
description: PostHog audit B6 - PersonaliseView (SignUpCubit) was the missing 9th onboarding step; fixed with step_index -1 to avoid renumbering TherapyOnboardingCubit's 0-7 range
metadata:
  type: project
---

Root cause of the "9th onboarding step never emits step_name" audit finding
(analytics-reports/2026-08-10-posthog-audit-taskplan.md, task B6): the
onboarding funnel is split across TWO cubits that were never unified under
one instrumentation contract.

- `TherapyOnboardingCubit` (lib/screens/therapy_onboarding/cubit/) owns 8
  steps and already tracked all of them: legal_gate=0, challenges=1,
  intensity=2, journey=3, modality=4, schedule=5, companion=6,
  lead_source=7 (`_stepNames`, `_trackStepViewed`/`_trackStepCompleted`).
- `SignUpCubit` (lib/screens/sign_up/cubit/) owns a step that runs BEFORE
  all of the above: `PersonaliseView` (lib/screens/sign_up/personalise_view.dart)
  collects name/age_band/gender/pronouns, shown as SignUpCubit's initial
  state, before the Firebase account is even created. It never emitted
  onboarding_step_viewed/completed because nobody wired it into
  TherapyOnboardingCubit's list — it's architecturally a different cubit.

Fix: added the same two-event contract (step_name/step_index/
duration_seconds) to SignUpCubit — `_trackPersonaliseViewed()` fires from
the constructor (personalise() is always the initial state), and
`_trackPersonaliseCompleted()` fires as the first statement in both
`register()` and `registerForGoogleAndApple()`.

**Numbering decision** (matters for anyone touching onboarding step indices
again): used `step_index: -1` for personalise instead of renumbering
TherapyOnboardingCubit's 0-7 range. Renumbering would have required shifting
every existing index (legal_gate 0->1 ... lead_source 7->8), which silently
corrupts any PostHog dashboard/funnel already built against those indices
(old and new data would collide under the same index with different
meanings). -1 sorts correctly before 0 in any index-ordered funnel view and
needs zero changes downstream. Left a cross-reference comment in both files
so a future reader of TherapyOnboardingCubit's `_stepNames` list knows step
-1 exists elsewhere.

**Test gotcha confirmed reusable**: `SignUpCubit.register()`/
`registerForGoogleAndApple()` call `BotToast.showLoading()` as their second
analytics-adjacent statement, which throws `AssertionError` outside a pumped
BotToast widget tree (same pattern already established in
test/screens/settings/cubit/settings_cubit_delete_account_test.dart). Because
`_trackPersonaliseCompleted()` is literally the FIRST statement in both
methods, tests can call the method, expect the AssertionError via
`expectLater(..., throwsA(isA<AssertionError>()))`, and still assert on the
PostHog capture that already fired before the throw — no need for a full
widget-tree pump or deep Firebase/User mocking. See
test/screens/sign_up/personalise_step_analytics_test.dart.

Commit: ff3087c (mindsync-frontend, branch dev, NOT pushed — 13 pre-existing
local commits ahead of origin/dev before this one, per project memory
project_msv32_fix5_batch_2026_07_25.md-adjacent batches).
