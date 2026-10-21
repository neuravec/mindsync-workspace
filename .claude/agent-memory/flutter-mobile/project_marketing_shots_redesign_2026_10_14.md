---
name: project-marketing-shots-redesign-2026-10-14
description: Marketing shots of the 5c27b2c redesign (cards, Timeline, Workspace v2, KD sheet/star/new skill) on branch feat/marketing-shots-redesign (629bffe, local); harness gotchas and UI bugs found
metadata:
  type: project
---

8 shots committed on feat/marketing-shots-redesign (worktree mindsync-frontend-wt-mshots, 629bffe, not pushed); PNGs + _manifest.json entries in social/images/app-shots (frontend_commit 5c27b2c).

- Redesigned cards: TherapyCardDetailScreen needs a Router (BackButtonListener), so shots rebuild its `_buildCardScaffold` chrome (`cardDetailChrome` in redesign_demo_data.dart).
- Tall captures: resize `tester.view` inside `beforeCapture`; when also calling `patchNullFontFamilies`, pumpAndSettle AFTER the resize first, else the MediaQuery rebuild drops the patch. Workspace module buttons (WorkspaceFilledButton) are null-family labels.
- KD screens: use `settle: false` + pump; char demo data reuses test/screens/character_tab/sheet/sheet_fixtures.dart helpers.
- Bugs found (reported, not fixed): health_check_section.dart check-in subtitle swaps args (generated `stats_checkInNumberDate(date, number)`), hard-codes DateFormat 'pl' ("#30 wrz" in EN) and the ARB copy has an em dash; Workspace "Therapy Relationship" header wraps mid-word ("Relations/hip") because Flexible title + Spacer split free space.

**Why:** operator wanted real redesign screens for an IG feature post.
**How to apply:** reuse the two demo-data files for further redesign shots. Related: [[marketing-shots-first-conversation-2026-10-05]].
