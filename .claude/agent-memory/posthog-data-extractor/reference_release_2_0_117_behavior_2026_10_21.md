---
name: reference-release-2-0-117-behavior-2026-10-21
description: Redesign store build 2.0.117 (first seen 2026-10-19 18:13 UTC), tester-exclusion recipe for it, new Main/cards/Character events flowing, voice_chat_started 0 on all 2.0.113+ builds, $rageclick iOS-only with no screen name
metadata:
  type: reference
---

Verified 2026-10-21 (extract `analytics-reports/raw/2026-10-21-release-behavior.md`).

- **Build map**: 2.0.113-2.0.116 = tester builds of the redesign (10-19 06:51..18:00, TestFlight + few Android); **2.0.117 = store build** (Android build 188, iOS 184, `$is_testflight=false`). 2.0.110 = previous Android store build (main old-version cohort 10-14..10-20).
- **Tester exclusion used**: person with any `$is_testflight=true`, build 2.0.111-2.0.116, emulator or bot device in 30d (25 persons). Android-only testers who never ran a tester build slip through.
- **Adoption after ~47 h**: 7 real persons on 2.0.117, only 3 existing accounts (rest new installs). Before/after on same people impossible; re-run around 2026-10-28.
- **Flowing on new builds**: `main_viewed` (props mode, dot_tiles), `main_tile_viewed/_tapped` (tile_id: todo, focus, session, relationship, habits, affirmation, observations, agenda, first_week), `main_sheet_closed` (method x/scrim/swipe/back/action, duration_s), `main_sheet_action`, `main_week_*`, `card_*`, `period_card_extras_viewed`, `timeline_filter_*`, `skill_*`, `companion_opened`, `skill_moment_*`. Gone: `today_card_*`, `side_card_*`, `$screen` mainPageTab/firstWeekTrends/firstWeekHabits/reflectModeChoice.
- **Never on 2.0.113-117 (incl. testers)**: `voice_chat_started`, `voice_chat_ended`, `mic_permission_result`; code still emits it (audio_chat_cubit, live_chat_cubit). Flagged to flutter-mobile for device check. First conversation on 2.0.117 went text (n=1).
- **Sheet closes**: swipe-down only 7% of closes; 53% close < 2 s but nearly all testers.
- **`$rageclick`**: iOS only (native SDK autocapture), `$screen_name` always "Flutter". No `$dead_click` event exists.
- Gotcha: `last` is a reserved word in HogQL, alias as `last_ts`. Bash heredoc with Python f-strings containing `$` and quotes failed; write generator scripts with the Write tool instead.
