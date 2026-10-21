---
name: design-handoff-prototype
description: Single-file HTML clickable prototype at design-handoff/current-app-mockup.html — 12 screens, 1713 lines, built 2026-05-18
metadata:
  type: project
---

Static HTML prototype at `C:\Users\mikol\Notebooks\MindSync\Heroku\design-handoff\current-app-mockup.html`.

**Why:** Design handoff artifact for external designer showing current app state.

**How to apply:** When designer asks for updates, edit that file. Each screen is a `<div class="screen" id="screen-XXX">` inside `#screens` div. JS `show(id)` switches visibility.

Screens included:
1. welcome — lagoon-blue bg, logo SVG, Log In / Sign Up buttons
2. auth — lagoon-blue, email+password form, Google/Apple social
3. home — aqua-breeze, hero greeting, next session card, symptom trend chart, realization widget
4. therapy — timeline with filter chips, 5 item types (debrief/prep/realization/between-session/recording)
5. stats — symptom SVG polyline chart, therapy signal, snapshots (7/30/90d), goals progress bars
6. character — orca SVG, dual leveling bars, personal bio sections, interaction stats
7. chat — bubbles (user=deep-ocean, ai=white), typing indicator, mic button navigates to audiochat
8. audiochat — waveform bars, end-call button navigates back to chat
9. settings — collapsible groups (App/Voice/Therapy/Notifications/Character/Account), premium banner
10. subscription — feature list, plan selector (annual/monthly), CTA button
11. onboarding — progress dots, challenge chips, sand-beige theme
12. debrief — guiding questions, text area, voice button, submit CTA

Bottom nav shown on screens: home, therapy, chat, stats, character.
FAB shown on same screens.
