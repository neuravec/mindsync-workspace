---
name: project-cards-v3-fe4-review-fixes-2026-10-18
description: Cards v3 FE4 review fixes pushed (c82bf87 font + 6705fe0) on feat/cards-v3; FE already reads requested backend fields realization/therapist_name; board inline-span line box; escape traps in Bash heredocs and the Edit tool
metadata:
  type: project
---

FE4 fixed 12 frontend review findings on cards v3 and pushed `feat/cards-v3` (c82bf87 font family, identical to workspace 9e2d0cc so the merge is clean; 6705fe0 the rest). Builds on [[project-cards-v3-fe3-2026-10-18]].

**Why:** the screens had to match the artifact boards 1:1; reviewer flagged duplicate summary/realization, missing quotes, AA Cancel, Timeline Weekly/Monthly stack, line heights.

**How to apply:**
- Pending backend (FE already parses, nullable): `realization` on Between and Reflect responses (gold block shows only when it differs from the summary), `therapist_name` on debrief and recording ("Session with {name}" eyebrow, none when null), Monthly goals as {goal, status} pairs (FE splits "goal: status" meanwhile). Listed in teams/cards/API.md. Do not re-add a filler eyebrow or the summary-as-quote.
- Timeline Weekly/Monthly chips now read the `/timeline/` feed (state has no weeklySummaries/monthlyAudits); rows under those chips open the card with summary_viewed source=timeline_list, All keeps detail_screen.
- Board CSS: an inline span alone in a block div gets the parent's 16px strut (line box 19.2), a flex-column child gets 12*1.2. Summary label = 19.2/12; other labels 1.2. MsCardPage/Timeline set DefaultTextStyle height 1.2.
- Escape traps: Bash heredoc collapses `\\` to `\` before Python sees it (Dart regex `\b` became byte 0x08); the Edit tool turns `“` into the literal character. Write a .py file with the Write tool (keeps `\\`) or build backslashes with chr(92); scan with `grep -rlP "\x08"`.
- ButtonStyle.textStyle without the theme label style has a null family (platform font on device, black bars in shots): use Theme.of(context).textTheme.labelLarge?.copyWith(...).
- Pre-existing failure, not ours: test/screens/fab_flows/record_session_appbar_close_test.dart (fails on d775f64 too).
- Open for the lead/operator: header Edit on Recording, Reflect, structured Weekly, Monthly, Realization (D3 vs boards).
