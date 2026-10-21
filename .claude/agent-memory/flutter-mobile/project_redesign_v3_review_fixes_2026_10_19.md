---
name: project-redesign-v3-review-fixes-2026-10-19
description: Integration review fixes on integration/redesign-v3 (9f18f4b..856fb44 pushed) - KE replay masks + KeIdeaSlot, therapy-value folding in KeAnalytics, Main flow_opened, MsCardLineChart mask; PostHog mask internals, fold-not-bucket rule, build-wrap trick
metadata:
  type: project
---

Four review findings fixed on `integration/redesign-v3` (worktree mindsync-frontend-wt-integration-v3), pushed 2026-10-19 as 9f18f4b, a06355b, f72207b, 856fb44. Builds on [[project-redesign-v3-integration-2026-10-19]] and [[project-main-mc-v3-review-fixes-2026-10-19]].

- KE replay (H-1): `KeReplayMask` (tab body, KE2, KE3, KE4) + `showKeSheet`/`KeSheetRoute` (Rename, About) in `ke/widgets/ke_replay_mask.dart`. `KeIdeaSlot`: support row fills the room of an invisible sizer copy of the idea (no callbacks). Test `ke_replay_mask_test.dart` (12/13 fail with masks removed).
- KE analytics: therapy-only values folded into a value everyone has (using_therapy->connecting, session/after_therapy->note, from_therapy->used_method, homework->consolidate), tool origin dropped. Backend `skill_stage_reached` still sends raw anchor: open for backend-api.
- Main: session + relationship sheet buttons send `flow_opened` (`mainTherapyFlowActions` never sent).
- MsCardLineChart wrapped in PostHogMaskWidget (`maskKey`).

**Why:** the same traps return in every privacy review round.
**How to apply:**
- posthog_flutter 5.23 masks by walking onstage elements: PostHogMaskWidget, Text/RenderParagraph, RenderEditable, RenderImage. CustomPaint/Canvas text is NEVER masked by maskAllTexts; any painter with user data needs a PostHogMaskWidget.
- Never fold a therapy value into `other` or a new bucket that holds only therapy values: the bucket itself becomes the marker. Fold into a common existing value and pin "each folded bucket also holds a non-therapy value" in a test.
- To wrap a whole screen without re-indenting (no dart format on existing files): `build(ctx) => Mask(child: _buildPage(ctx));` and rename the old build.
- Long Python edit scripts via bash heredoc failed ("unexpected EOF looking for matching `'`"); write them with the Write tool instead.
- KE4 route: pump(1 s) after push, not 400 ms (companion animates, no pumpAndSettle).
