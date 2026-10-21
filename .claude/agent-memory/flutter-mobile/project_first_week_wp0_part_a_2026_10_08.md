---
name: first-week-wp0-part-a-2026-10-08
description: First-week Home WP-0 part A (commit 98fe273 on fw/fe0a-home, local only) - recap "Saved in Reflect", check-in route to Mood trend, neutral Home tap events, ARB editing gotchas (CRLF, Write tool turns \u escapes into real dashes, DE mojibake)
metadata:
  type: project
---

WP-0 part A shipped as commit 98fe273 on branch `fw/fe0a-home` (worktree `mindsync-frontend-wt-fw-fe0a`, from `feat/first-week-home` 5ec58ed). Not pushed as of 2026-10-08.

Decisions worth remembering:
- Tap events on therapy-flavoured choices carry NO option identity: `getting_started_card_tapped` has no properties, `fab_flow_selected` only `tab_name`. A fixed position index was rejected as a renamed therapy proxy (security audit 2026-10-07 "count only"). **Why:** the lead suggested "index or neutral enum"; an index maps 1:1 to the flow. **How to apply:** for any future tap event on a menu whose options name therapy, send where the tap came from, never which option.
- The first conversation is a Reflect thread; `GET /reflect/threads` lists every REFLECT conversation, and the client hides only the persisted fresh-empty thread. The Timeline (TherapyTimelineItem) never lists conversations. So "Saved in Reflect" is true, "Saved to your Timeline" is not.
- "Add a check-in" = `MainNavCubit.selectTab(0, scrollTo: MsRoutes.mainMoodTrendsSection)`; rating lives only in `UnifiedSymptomModule` inside the Home Mood trend card. Health check flow is the Therapy Relationship check-in, not area rating.
- COPY.md (brand-voice-manager) can land mid-task; re-check for it before committing copy.

Gotchas:
- ARB files in a worktree are CRLF (core.autocrlf=true). A Python edit that splits on "\n" leaves mixed endings; detect the newline first.
- The Write tool turns `—` inside file content into the real character. Write dash escapes in Dart sources via a bytes-level script, then scan.
- `app_de.arb` has ~140 lines of double-encoded mojibake (e.g. "fĂĽhlst", "â€”"). Write new DE strings as proper UTF-8; fix old ones only where touched.

Related: [[posthog-integration]], [[l10n-and-prefs]]
