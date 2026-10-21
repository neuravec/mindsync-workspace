---
name: project-redesign-v3-health-check-flow-mask-2026-10-19
description: b9817a9 on integration/redesign-v3-final (pushed); whole HealthCheckFlowScreen masked for replay, test recipe, CRLF reindent recipe
metadata:
  type: project
---

Security finding (High) after 4654c19: the health check FLOW screen was not masked, only the stats tile and result card. maskAllTexts hides digits but not the selected 1-5 circle (grows 48 to 56 px, fills), and safety/heard/direction always come in that order, so replay leaked scores. Fixed in b9817a9 (pushed to origin integration/redesign-v3-final): `HealthCheckFlowScreen.maskKey` on one PostHogMaskWidget around SafeArea/BlocBuilder in `_HealthCheckFlowBody`.

**Why:** replay is on for every user; any masked summary surface is moot if the input screen that produced it is not masked. Check the entry flow, not just the tile.

**How to apply:**
- When masking a summary/tile, follow its tap target and mask the screen it opens too (pattern: quick_check_in_screen.dart, mc_main_screen.dart).
- Test recipe: `test/screens/health_check/widgets/health_check_flow_mask_test.dart` emits each state on the screen's own cubit (`tester.element(find.byType(Scaffold)).read<Cubit>()`, two pumps), taps a circle, asserts mask is ancestor of every circle and `getRect(mask) == getRect(Scaffold)`. Proved non-vacuous by swapping the mask for KeyedSubtree (all 10 fail).
- Wrapping a big CRLF build block without the Edit tool: python binary read, split on `\r\n`, prefix two spaces to the inner range, rejoin. `git diff -w` then shows only the wrapper lines.
- Git Bash `$TMPDIR` is `C:/Users/mikol/AppData/Local/Temp`, NOT the session scratchpad; clean up backups there.

Related: [[project-redesign-v3-final-2026-10-19]]
