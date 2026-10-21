---
name: project-timeline-capture-bridge-2026-08-10
description: Timeline "All" empty-state capture-bridge CTA (design-specs/2026-08-10-timeline-capture-bridge.md) — implementation gotchas worth remembering
metadata:
  type: project
---

Implemented per `design-specs/2026-08-10-timeline-capture-bridge.md`
(ui-ux-designer). New `TimelineCaptureBridgeCard` widget
(`lib/screens/therapy_tab/widgets/timeline_capture_bridge_card.dart`) wired
additively into `_EmptyStateState.build()` in `therapy_tab_screen.dart`.
Committed locally on `dev` at `3ae6a18` (parent `8300710`), NOT pushed.

**Why:** activation-definition growth-analyst report flagged Timeline's
"All" empty state as passive-text-only despite 46 users/14d reach — highest-
precision, zero-plumbing place to intercept zero-capture users.

**How to apply / gotchas for next time:**

1. **Render guard must exclude generating/premiumLocked/generateFailed
   variants, not just filter+hasItemsInOtherFilter.** `_EmptyState` has
   `isGenerating`/`isPremiumLocked`/`isGenerateFailed` flags independent of
   `filter`. A guard of just `filter == all && !hasItemsInOtherFilter` would
   theoretically also fire during those variants if they ever carried
   `filter == all` (they don't today — on-demand generation only exists for
   Weekly/Monthly — but the spec's SS4 "Not applicable" row requires the
   exclusion defensively). Caught this only by writing the screen-level
   render-condition test matrix, not by re-reading the spec.

2. **GoRouter identity gotcha in widget tests.** Building a fresh
   `GoRouter(...)` object inside a `_harness()` helper called on every
   `pumpWidget()` breaks "fires once across rebuilds" tests: a new
   `RouterConfig` object identity forces `MaterialApp.router` to reset its
   Router/Navigator, which unmounts+remounts the subtree (a real new
   `State`, not a rebuild) — so `initState`-guarded analytics correctly fire
   again, and the test fails for the wrong reason. Fix: build the
   `GoRouter` ONCE per test (`final router = _router(...)`) and reuse the
   same instance across both `pumpWidget()` calls; only the outer
   `MaterialApp.router` wrapper widget should be rebuilt. Plain
   `MaterialApp(home: ...)` harnesses (no router) don't have this problem —
   see `getting_started_card_activation_test.dart`.

3. **`use_build_context_synchronously` lint: prefer bare `mounted` over
   `context.mounted`.** For a `context.read<Cubit>()` call after an awaited
   async gap inside a `State`, `if (!context.mounted) return;` (early
   return, matching `TherapyFlowLauncher`'s own style) still got flagged as
   "guarded by an unrelated 'mounted' check" — an analyzer quirk. Switching
   to the State's own `if (!mounted) return;` field check cleared it. Try
   plain `mounted` first when this lint won't clear with `context.mounted`.

4. **gen-l10n toolchain check is worth doing, but wasn't the actual
   problem here.** Ran `gen-l10n` once via system Flutter 3.41.1 first
   (huge ~1000-line-per-file diff on every locale's generated output —
   looked alarming). Suspected a formatter-version mismatch vs the
   project's pinned FVM Flutter 3.27.0 and re-ran via
   `.fvm/flutter_sdk/bin/flutter gen-l10n` to check — it produced a
   BYTE-IDENTICAL result to the system-Flutter output already committed.
   The large diff was real but pre-existing drift in the repo (confirmed
   via `git log` on the generated file — several prior commits, e.g.
   `4a20b19`, `88dbc17`, also touch the full generated file whenever ARB
   keys change), not something this task introduced incorrectly. Lesson:
   don't assume a large gen-l10n diff is a toolchain mistake — verify with
   the FVM SDK before "fixing" anything, but expect whole-file diffs on any
   ARB key change to be normal in this repo.

5. **New PreferenceKey pattern reused verbatim**: `timelineCaptureBridgeDismissed`
   follows the `hasCapturedBefore`/`swipeDeleteHintShown` exact shape (bool,
   `hasDismissedX()` + `markXDismissed()` pair on `SharedPreferencesManager`).

See also [[architecture]], [[l10n_and_prefs]].
