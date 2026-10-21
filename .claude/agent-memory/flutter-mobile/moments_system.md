---
name: moments-system
description: Notification Moments / Insights dispatch architecture (Phase 2, May 2026) — renderers, trigger hooks, rate limiting, and widget test gotchas
metadata:
  type: project
---

## Moments System Phase 2 (May 2026)

- `InsightDispatcher`: `lib/widgets/moments/renderers/insight_dispatcher.dart` — routes by `InsightType`; enforces 30s rate limit via `cubit.canShowContent()`; `celebrateTease` only marks shown (inline rendered via BlocBuilder); `reveal` → `RevealToastRenderer.show()`; others → debugPrint no-op
- `RevealToastRenderer`: `lib/widgets/moments/renderers/reveal_toast_renderer.dart` — calls `cubit.showInsight(id)` BEFORE rendering; `direction=='down' ? '↓' : '↑'`; `isPositive ? 🎉 : 💪`; `abs(delta)`; falls back to `insight.title`/`insight.body` when payload keys missing
- `CelebrateTeaseRenderer`: `lib/widgets/moments/renderers/celebrate_tease_renderer.dart` — StatelessWidget, wraps `InlineNoticeBanner`; `_iconForMilestone`: `streak_month→emoji_events, streak_three→celebration, _→water`; `ctaRoute==null → onCta=null`
- `MomentsCubit.onTrigger(type, ctx)`: awaits `triggerDetection` then `getPendingInsights` then `copyWith(pendingInsights:...)` if loaded, else fresh `loaded()`; fire-and-forget in callers via `unawaited()`
- Trigger hooks: `debrief_save` / `note_added` in `DebriefCaptureCubit._uploadRecording()` + `submitText()`; `symptom_logged` in `SymptomTrackingCubit.updateScore()`; `stats_tab_opened` / `therapy_tab_opened` in `main_page_body.dart` `BlocListener<MainNavCubit>` tab index 3/1
- `MomentsCubit.onTrigger` does NOT emit when new state equals current state (Freezed equality) — seed tests with non-empty state so the → empty transition is observable
- (NOTE Jul 2026: since fixed via `unknownEnumValue` — see [[notification_cadence_v3_hardening]] — an unrecognized backend `moment_type` used to throw here and tank the whole `loadOnAppOpen` via `Future.wait`)

## Widget-test gotchas specific to this system

- Widget tests with `context.go()`: use `MaterialApp.router` with a `GoRouter` that has stub routes — plain `MaterialApp` throws `No GoRouter found in context` on CTA tap
- `MomentBottomSheet` minHeight = 40% screen — use `tester.view.physicalSize = Size(800, 1400)` **and** `tester.view.devicePixelRatio = 1.0` for CTA tap tests (the default 3.0 ratio shrinks the logical viewport enough to push a secondary CTA below a primary one out of hit-testable bounds); add `addTearDown(tester.view.reset)`
- `InlineNoticeBanner`: `Icons.close` appears TWICE (Dismissible background + `_BannerContent` GestureDetector) — use `find.byIcon(Icons.close).first` to target the dismiss button; use `pumpAndSettle()` to complete 300ms entrance animation before tapping
- `MomentDeepLinkScreen` shows an indeterminate `CircularProgressIndicator` for every status except `expired`, including while a sheet is open on top of it (`dispatching`) — `pumpAndSettle()` never terminates in that state; use bounded `tester.pump(duration)` loops instead once a sheet may be open. Full writeup: [[notification_cadence_v3_hardening]]
