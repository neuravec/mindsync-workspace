---
name: project-redesign-v3-push-link-reminder-copy-2026-10-19
description: 3564e03+2da882b+e50e705 pushed on integration/redesign-v3-final; ?section=first_week_plan opens the plan sheet (source push), reminder copy; 230 px text column, measure recipe
metadata:
  type: project
---

Pre-release fixes on integration/redesign-v3-final, pushed (b9817a9..e50e705).

- 3564e03: backend step reminder push opens `/main-page/tab/main?section=first_week_plan` (`MsRoutes.mainFirstWeekPlanSection`). `McMainScreen._openWeekPlanFromLink` awaits `week.load()` (shares the in-flight load) when status != loaded, then opens only if `showTile`; a `_weekLink` counter makes each link open at most once; post-frame guard drops it on another tab or while a pop-out is up. Analytics source is now enum `McWeekPlanSource {tile, popup, push}` (mc_analytics.dart) checked against `mainWeekSources`.
- 2da882b: `mc_weekReminderBody` reworded in 7 langs; e50e705: EN changed to "A daily nudge until your steps are done" (one line, lead asked to avoid the widow).

**Why:** the contract test forbids any String param except `action` in `McAnalytics.week*` signatures, so a new source must be an enum, not a String. The reminder row text column is only 230 px at 390 (Figtree 13): old EN fit at 228.3, the new EN needs 245 and wraps; "A daily nudge until your steps are done" (225.7) would fit. All other 6 languages already wrapped.

**How to apply:**
- Copy-fit questions: temp `@Tags(['marketing'])` test in test/main_parity_shots calling `captureMainShot(..., prepare:)`, read `RenderParagraph.constraints.maxWidth` (import flutter/rendering.dart), then `TextPainter` per candidate. Run with `--tags marketing --run-skipped`, delete after.
- A deep link that needs async data: await the cubit's shared load, re-check mounted/link token/tab, open post-frame.

Related: [[project-redesign-v3-final-2026-10-19]], [[project-main-mc-v3-fe6-2026-10-18]]
