---
name: character-ke-ux-fixes-2026-10-18
description: Character KD v2 (KE) UX review fixes a11fd4a on feat/character-kd2-v3 (pushed to origin only) - radar scaled as one piece, KE4 words + optional contexts, one-scroll KE4, FittedBox stage names, Not yet column; gen_l10n select trick and measuring-under-Material gotcha
metadata:
  type: project
---

UX review round (8 findings) on the KE screens is commit a11fd4a on `feat/character-kd2-v3` (worktree `mindsync-frontend-wt-character-kd2`), pushed to origin only. Builds on FE3 052960d / 57d2f78 and fa10f22.

**Why:** the UX reviewer rendered KE1-KE4 at 360 px and 1.3x text (scratchpad `teams/character/ux-review/shots`, re-rendered after the fix in `ux-review/shots_after`); boards are drawn only at 390.

**How to apply (integration / follow-ups):**
- Still open, outside the client: `pending_stages[].contexts` (optional, up to 3 paraphrases) is parsed and rendered but NOT in API.md 2.1 yet; the board's specific Orca line ("You held that line without a long explanation.") would need a server field too. Board notes for Darek: hidden-idea text #335357, KE2 chip "visual 40, target 48".
- `captureKeParityShot(..., textScale:)` exists now; 360 px and 1.3x parity shots live next to the board ones.

Recipes that worked:
- Spelled-out numbers in ARB: gen_l10n plural only accepts =0/=1/=2/zero/one/two/few/many/other, so use `{n, select, one{..} two{..} ... nine{..} other{{count} ..}}` with a Dart `numberCase(int)` mapper; per-language phrases keep grammar (PL locative "dwóch różnych tygodniach").
- "Pinned bottom when it fits, follows content when not" without IntrinsicHeight (LayoutBuilder children cannot do intrinsics): `LayoutBuilder -> SingleChildScrollView -> ConstrainedBox(minHeight: viewport) -> Column(mainAxisAlignment: spaceBetween)`.
- Fixed-coordinate painter on narrow screens: compute label extents, size the canvas to them, wrap in `Center(FittedBox(scaleDown))`; tests must derive expected sizes from `horizontalExtent` because the wide test font widens the canvas.
- Shared value column ("Not yet" vs "1"): measure the text under the same Material as the rows. Measuring above it picked a DefaultTextStyle without the 0.25 letterSpacing and the columns drifted 1.75 px.

Related: [[character-ke-fe3-2026-10-18]], [[character-ke-fe2-2026-10-18]]
