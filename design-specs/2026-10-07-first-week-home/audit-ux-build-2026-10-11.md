# First-week Home: UX, accessibility and mental-health review of the build

Date: 2026-10-11. Reviewer: ui-ux-designer (read-only).
Code: `mindsync-frontend-wt-fw-int/mindsync_app`, branch `feat/first-week-home` at `27dafa4`. All paths below are relative to `mindsync_app/` unless they start with `MindSync-wt-fw-integration/` (backend worktree, branch `feat/first-week-home` at `a021da9`, read only to confirm what the client receives).
Design sources: `canvas/*.dc.html` (v4), `SPEC.md` sections 6 and 13, `COPY.md`, `API_CONTRACT.md` section 14 (14.1 and 14.2).
Out of scope: the day-3 trial sheet (built on another branch).
Method: code reading against the boards and the spec, WCAG contrast computed from `lib/resources/ms_colors.dart`, layout at large text estimated from Figtree advance widths (about 0.52 to 0.55 em per character). No tests were run and no code was changed.

## Verdict

**Ready for TestFlight after the listed Blocker and Major fixes.** The structure, states, tokens and tone handling follow the canvas closely and most of the build is careful work. One binding rule is broken (a Today card leads straight into the paywall when Free Reflect messages are used up), the session sheet's "Not sure yet" and the Art. 9 consent step need another pass, and the Home rows break at large text sizes. M-4 has a TestFlight-safe option now and a lawyer-dependent option before the store release.

## Findings

Severity: **Blocker** (breaks a binding rule or misleads the person in a way that must not reach testers), **Major** (fix before TestFlight), **Minor** (fix before store release), **Polish**.

| ID | Severity | Screen | File:line | What is wrong | Exact fix (owner) |
|---|---|---|---|---|---|
| B-1 | Blocker | Home, Today card `rest` and `open` | `lib/screens/first_week/first_week_copy.dart:254-275, 529-556`; backend `MindSync-wt-fw-integration/app/services/first_week/plan_engine.py:1305-1313, 1365-1372`; paywall at `lib/screens/reflect_tab/reflect_tab_screen.dart:971-977` | On Free with 0 Reflect messages left, `rest` and `open` still show "Talk with {orcaName}" next to the line "Reflect messages: 0 of 15 left until Nov 1". The server always sends `/main-page/tab/reflect?new=true` for these states, and Reflect's new-thread path at zero pushes the paywall. The card invites an action it says is used up and then lands in the paywall, which SPEC 3.8 and 13.2 forbid ("never straight into the paywall"). The client's `restBodyNoMessages` and check-in branch exist but are unreachable because the server never sends the check-in route. `open` (hidden plan) lasts beyond week 1, so this repeats daily. | backend-api: in `plan_engine.py`, for `rest` and `open`, when `is_free` and `reflect_messages` left is 0, send `cta_route = "/first-week/check-in"` (already allowlisted). flutter-mobile: in `_openTalk`, when the target is check-in: `rest` keeps `firstWeek_restTitle` with body `firstWeek_restBodyNoMessages` (gentle: `firstWeek_quotaTalkBodyGentle`); `open` uses title `firstWeek_quotaTalkTitle(resetDate)` and body `firstWeek_quotaTalkBody` (gentle: `firstWeek_quotaTalkBodyGentle`); CTA `firstWeek_ctaQuickCheckIn`; keep the quota line and "See Premium" (standard only). All strings exist; no new copy. Interim if the backend cannot ship together: derive the check-in target on the client from `today.quota` (`reflect_messages`, `left == 0`); `/first-week/check-in` is a fixed client target, not a server-invented route. integration-devops: update API_CONTRACT 1.3 note on `rest`/`open`. Add a widget test per state and tone. |
| M-1 | Major | Mirror; session sheet "nothing to capture" result | `lib/screens/first_week/check_in/widgets/check_in_mirror_view.dart:253-333`; `lib/screens/first_week/check_in/quick_check_in_screen.dart:118-124`; `lib/screens/first_week/session_sheet/session_sheet.dart:72-77`; `lib/screens/first_week/session_sheet/show_session_sheet.dart:112-113` | Same loop one step later. The quota-out card's free alternative is the check-in; the B/C mirror then offers "Talk with {orcaName}", which at 0 messages opens the paywall. The "It didn't happen" result also offers "Talk with {orcaName}" and its body says "{orcaName} is here". | flutter-mobile: one helper, `reflectMessagesExhausted()` (Free plan and `reflect_messages` left 0, from `UsageCubit` or `plan.today.quota`). When true: the mirror hides the B/C next-step card (the recap line and "Back to home" stay; the A agenda card is unaffected); the "didn't happen" result hides the "Talk with {orcaName}" button and uses a body without the last sentence. brand-voice-manager: new key `firstWeekSession_didntBodyNoTalk`, proposed "Your plan skips this step, and your usual schedule stays as it is." |
| M-2 | Major | Home Today card, quota line, day-0 reminder row, plan card header, mirror rows | `lib/screens/first_week/widgets/today_card.dart:323-353, 590-616`; `lib/screens/first_week/widgets/day0_reminder_row.dart:153-206`; `lib/screens/first_week/widgets/plan_card.dart:378-408`; `lib/screens/first_week/check_in/widgets/check_in_mirror_view.dart:176-222` | Text and buttons share one horizontal row with no breakpoint. Card inner width at 320 dp is 248 dp. At text scale 1.3 on 320 dp, "Not today" takes about 127 dp and the CTA label gets about 77 dp, so "Start Before therapy" breaks inside "therapy". The reminder label gets about 77 dp, so "tomorrow" breaks mid-word. At 2.0 on a 375 dp phone, the CTA label gets about 85 dp for 34 sp text and words break letter by letter. Mirror area names and the plan title ("Your first week" next to "See the week") break the same way at 2.0. The session sheet, recap and rhythm have 320 dp at 1.3 tests; the Home parts have none. | flutter-mobile: stack when `MediaQuery.textScalerOf(context).scale(16) > 20` or the row's `maxWidth < 300` (`LayoutBuilder`). Dark card: CTA full width (min 52), then "Not today" as a full-width `TextButton` (min 48), centred. Quota row: the line on its own, "See Premium" below it, start-aligned. Reminder row: label on its own line, then `Row(time button, Spacer, Switch)`. Plan header: title, then the toggle start-aligned below. Mirror row: area name on its own line, then the two columns. Tests: Today card (every state), plan card, side card, reminder row and mirror at 320x640 with `TextScaler.linear(1.3)` and 375x812 with `2.0`: no exception, CTA width at least 160 dp, every tap target at least 48 dp. |
| M-3 | Major | Session sheet, "Not sure yet" | `lib/screens/first_week/session_sheet/session_sheet_cubit.dart:190-196`; `lib/screens/first_week/session_sheet/session_sheet.dart:319-345` | Two issues. (1) From "Session moved?" (prep) and from the side card, "Not sure yet" closes the sheet with no write and no message. The person gets no confirmation, and the prep card keeps saying "Get ready for tomorrow's session" right after they said the session moved; tomorrow's `after` card will say "After your session today" for a session that is not happening. (2) "Not sure yet" sits as a half-width twin of the time button, so it reads as "not sure about the time". A person who picked a day and tapped it would believe the date was saved without a time. | See section "M-3 detail" for the behaviour and copy. flutter-mobile: move "Not sure yet" below "Update my plan" as a full-width `TextButton` (min 48) and make the time button full width with a leading clock icon. backend-api (preferred, small): let `POST /first-week/today/drop` also accept an open `prep` step and drop that session's `after` step in the same call, schedule untouched. brand-voice-manager: the new strings listed in the detail section. |
| M-4 | Major | Art. 9 consent step in the session sheet | `lib/widgets/art9_consent/art9_consent_step.dart:64-146`; `lib/screens/first_week/session_sheet/session_sheet.dart:67-71` | Reusing the onboarding text is not clear here. The person tapped "Add sessions" (or tried to move a session) and gets "Personalise to your therapy", which reads as a detour, not as the permission the action needs. The checkbox says "use my therapy status", but this flow stores session dates and times, and since API_CONTRACT 14.1 item 5 it also sets the in-therapy status. Neither is named, so the consent is less informed than Art. 9 expects. "Continue" and "Cancel" do not say what happens, and nothing says where to withdraw (Settings, Privacy & Data, "Use therapy treatment data"). | See section "M-4 detail". Before TestFlight (no legal text change): a context lead-in above the reused block, plus context button labels and a decline toast. Before store release: lawyer and security-guardian confirm whether the onboarding text covers storing session times; if not, a context-specific consent text. Owners: brand-voice-manager (copy), flutter-mobile (props for lead-in and labels on `Art9ConsentStep`), lead (lawyer). |
| M-5 | Major | Side card B/C into the session sheet | `lib/screens/first_week/widgets/side_card.dart:61-67`; `lib/screens/first_week/session_sheet/session_sheet_state.dart:80`; `lib/screens/first_week/session_sheet/session_sheet.dart:268-310` | API_CONTRACT 2 says B "Add session time" opens the existing `SessionSetupScreen`; the build opens the move-a-session sheet for both B and C. For adding sessions it has the wrong defaults. The scope starts on "Just this once", so a C person adding a weekly therapy gets one session and an empty plan after it. The hint "Your usual schedule stays the same." refers to a schedule they do not have. There is no frequency choice (every 2 weeks, monthly), and a B person on a biweekly off-week can add a one-off on top of their recurring day. | Lead decides between two options. A (contract): after the consent step, open `SessionSetupScreen` for both cards; consent is now active, so its PUT passes. B (keep the sheet): for the `addSession` entry, default the scope to "From now on" and use add-specific hints, `firstWeekSession_addOnceHint` "Only this date is added." and `firstWeekSession_addAlwaysHint` "Every week on this day and time." (brand-voice-manager), and add an "Every week / Every 2 weeks" choice (backend-api must accept a frequency on `POST /therapy-schedule/change`). |
| M-6 | Major | Plan card "Hide this plan" | `lib/screens/first_week/widgets/plan_card.dart:342-350, 530-535` | One tap hides the plan for good (no unhide in v1, 14.1 item 12), with no confirmation and no Undo. The muted text button sits right under the rows, where a mis-tap is easy, and the snackbar does not say it is permanent. Respecting the choice is right; losing the plan through a slip is not. | flutter-mobile: deferred commit, as the recap's "Not right" does. Show `firstWeek_planHiddenSnackbar` with an Undo action (`firstWeek_undo`) for 5 s, hide the card locally at once, and send `POST /plan/hide` when the snackbar closes, unless Undo was tapped. Log `first_week_plan_hidden` after the server accepts. No confirmation dialog: the Undo is enough and does not nag. |
| m-1 | Minor | Home first load | `lib/screens/main_tab/main_tab_screen.dart:223-271, 677-683` | While the first plan request runs, Home builds the legacy body (Getting started card, empty next-session card, legacy modules) with only a Today skeleton on top, then swaps to first-week mode when the plan arrives. If the plan takes longer than the legacy cards' 300 ms entrance delay, a new person sees the old cluttered Home on day 0 and then a layout jump. | flutter-mobile: during the first fetch of an app session, render a neutral body (hero, Today skeleton, plan-card skeleton, no legacy cards). Fall back to legacy only after 204 or failure. To spare existing accounts the skeleton, cache a per-uid bool "had a plan last time" (no tone) and use it to pick the initial body. Verify on device with network throttling. |
| m-2 | Minor | Home cards, reduced motion | `lib/screens/main_tab/main_tab_screen.dart:321-325, 734-788` | `_AnimatedCard` (fade plus slide) ignores `disableAnimations`, and because `animKey` changes on every Home tab visit, the whole first-week block re-animates each time. | flutter-mobile: skip the controller when `MediaQuery.disableAnimationsOf(context)`; animate the first-week block only on its first build, not on tab revisits. |
| m-3 | Minor | Today card semantics | `lib/screens/first_week/widgets/today_card.dart:224-230, 414-420`; `lib/screens/first_week/first_week_copy.dart:238, 247, 496, 547` | Light cards use "Today" as both the container label and the visible eyebrow, so a screen reader says "Today, Today, You're set for today". | flutter-mobile: wrap the light-card eyebrow in `ExcludeSemantics` when it equals `firstWeek_todayA11y`. |
| m-4 | Minor | Plan card chips | `lib/screens/first_week/widgets/plan_card.dart:464-493` | Done chips are read as "Setup", "First talk" with no "done"; only the decorative tick shows it. | flutter-mobile: `Semantics(label: '$chip, ${s.firstWeek_whenDone}', excludeSemantics: true)` on each chip. |
| m-5 | Minor | Day-0 reminder row | `lib/screens/first_week/widgets/day0_reminder_row.dart:153-205` | The switch repeats the visible label as its own label, so "Remind me tomorrow" is read twice. | flutter-mobile: `MergeSemantics` around the label `Text` and the `Switch`, and drop the explicit `Semantics(label:)`. |
| m-6 | Minor | Quick check-in | `lib/screens/first_week/check_in/widgets/check_in_area_card.dart:56, 96-99, 152-173`; `lib/screens/first_week/check_in/quick_check_in_screen.dart:225` | At 320 dp each score button is 44.8 dp wide (256 dp less four 8 dp gaps, over five), below the 48 dp standard. | flutter-mobile: when `maxWidth < 280` inside the card, use card padding 8 and no extra right padding (or 6 dp gaps). The 48 dp height and 8 dp vertical gap stay. |
| m-7 | Minor | Mirror in gentle tone | `lib/screens/first_week/check_in/widgets/check_in_mirror_view.dart:185-207` | The recap drops setup values in gentle tone (no deltas, SPEC 3.6), but the mirror still puts setup next to today right after a crisis flag. | flutter-mobile: read the tone from `FirstWeekCubit.plan` (memory only) and show the Today column only, with the same widget keys. brand-voice-manager: new a11y key `firstWeekMirror_rowA11yTodayOnly`, "{area}: {todayScore} today". |
| m-8 | Minor | Rhythm sheet from "Change my rhythm" | `lib/screens/first_week/rhythm/first_week_rhythm_sheet.dart:29-36, 176-185` | No Free limit lines, while COPY 10.2 says "same list, same limit lines". A Free person can switch on "A voice note on Fridays" without seeing "On Free: 3 a month". | flutter-mobile: build the lines from `UsageCubit` (`plan == free` plus each feature's `free_limit`, API_CONTRACT 9), or backend-api adds `on_free` and `free_limits` to the plan's `rhythm` block (additive). |
| m-9 | Minor | Recap errors | `lib/screens/first_week/recap/recap_screen.dart:137-140` | 503, 5xx and offline leave with a toast; API_CONTRACT 11.2 asks for an error state with retry. The person tapped "See my week" and is bounced straight back. | flutter-mobile: in-screen error state (`error_somethingWentWrong` plus `common_retry`, 48 dp) for non-404 failures; 404 keeps the silent return. |
| m-10 | Minor | Follow-up at 0 messages | `lib/screens/first_week/follow_up/follow_up_screen.dart:127-137, 324-333` | On Free with 0 messages, the primary "Write to {orcaName}" opens the paywall. This is rare, because the Today card is `quota_out` by then, but it can happen within a day. | flutter-mobile: at zero, the primary button becomes `firstWeek_ctaQuickCheckIn` and opens `/first-week/check-in`; keep the usage line, and keep "Talk by voice" with its badge as the Premium path. |
| m-11 | Minor | Quick check-in empty and error states | `lib/screens/first_week/check_in/quick_check_in_screen.dart:243-250, 339-376` | Empty: "No focus areas yet" with no reason and no way on. Load error: "Something went wrong" (no "try again" tone). | brand-voice-manager: empty body `firstWeekCheckIn_emptyBody`, "You didn't pick any focus areas in setup. You can add some in Mood & symptom trends." flutter-mobile: a secondary button opening the trends module, and the error text `error_somethingWentWrong` ("Something went wrong. Please try again."). |
| m-12 | Minor | Home hero (pre-existing, now the first-week top) | `lib/screens/main_tab/main_tab_screen.dart:946-966` | The greeting is a `RichText`, which does not follow the system text size (its `textScaler` defaults to no scaling). | flutter-mobile: `Text.rich`, or `textScaler: MediaQuery.textScalerOf(context)`. |
| m-13 | Minor | Side card dismiss; recap "I'll find my own way" | `lib/screens/first_week/widgets/side_card.dart:69-72, 109-115`; `lib/screens/first_week/recap/recap_screen.dart:331-343` | Both are permanent and have no Undo. The side card is C's main way into sessions from Home. | flutter-mobile: the same deferred commit with Undo as M-6. |
| p-1 | Polish | Light Today card CTA | `lib/screens/first_week/widgets/today_card.dart:481-491` | `#DBF0ED` on white is 1.19:1, so the button shape almost disappears (the label is 11.53:1, so it passes). Same as the canvas. | `MsColors.primary[100]` fill plus a 1 dp `MsColors.lagoonBlue` border, or keep the fill and add a `primary[500]` border. |
| p-2 | Polish | Time buttons | `day0_reminder_row.dart:175-188`, `session_sheet.dart:359-379`, `first_week_rhythm_list.dart:95-108` | The `#BBE4DE` border on white is 1.38:1; the button boundary misses 3:1 (WCAG 1.4.11). | Border `MsColors.primary[500]` (3.60:1). |
| p-3 | Polish | Spinners | `session_sheet.dart:119-128, 225-234`; `follow_up_actions.dart:46-52` | `CircularProgressIndicator` ignores reduced motion. | Use the hourglass-icon pattern at `main_tab_screen.dart:1623` when `disableAnimations`. |
| p-4 | Polish | Consent step | `art9_consent_step.dart:126-132` | "Continue" is disabled with no hint why. | A 14 sp helper under the checkbox while unticked, e.g. "Tick the box to continue." (brand-voice-manager). |
| p-5 | Polish | Follow-up back button | `follow_up_screen.dart:116-119, 346-363` | While a start is running, back does nothing and shows no disabled state. | Grey the icon and set `enabled: false` in its semantics while `starting`. |
| p-6 | Polish | Dead code | `lib/screens/first_week/first_week_placeholder_screen.dart` | No longer referenced. | Delete. |
| p-7 | Polish | Quota `prep` CTA | `first_week_cta_launcher.dart` (agenda push) | "Add to my agenda" opens the agenda list; the person still has to find the add field. | Open the agenda with its add input focused, if the screen supports an argument for that. |

## M-3 detail: "Not sure yet"

Current behaviour, by entry:

| Entry | What "Not sure yet" does now | Problem |
|---|---|---|
| "It didn't happen" then "It moved to another day" | Drops the `after` step, then "Okay, no date for now / Your plan skips this step for now..." | Correct and true. Keep. |
| "Session moved?" on `prep` | Closes, no write, no message | Silent, and the Today card and tomorrow's `after` card keep claiming a session the person just said moved. |
| Side card B/C (`addSession`) | Closes, no write, no message | Silent. The COPY result text would be false here, so not showing it is right, but some confirmation is needed. |

Proposed behaviour and copy (brand-voice-manager finalises the wording; zero U+2014 and U+2013):

1. **"Session moved?" then "Not sure yet".**
   - Preferred (backend-api, small): `POST /first-week/today/drop` also accepts an open `prep` step and drops the matching `after` step in the same call; the schedule is untouched (same rule as today's drop). Then show the result view:
     - title: reuse `firstWeekSession_notSureTitle`, "Okay, no date for now";
     - body: new `firstWeekSession_notSureMovedBody`, "The steps for this session are off your plan. When you know the new day, add it in Settings, under Therapy Schedule, and your plan will follow.";
     - primary: `premiumWelcome_backHome`.
     - `session_sheet_completed` fires once, after the server accepts the drop (as for the `after` drop).
   - Fallback if the backend change does not make this release (no write):
     - same title;
     - body: new `firstWeekSession_notSureKeepBody`, "Nothing in your plan changes yet. If today's step doesn't fit, tap Not today. When you know the new day, add it in Settings, under Therapy Schedule.";
     - primary: `premiumWelcome_backHome`; no event.
2. **Side card then "Not sure yet".** No write, and do not dismiss the side card. Close the sheet and show `MsMessage.showInfo` with new `firstWeekSession_notSureAddToast`, "Okay. This card stays on Home for when you know." No event.
3. **Placement (all entries).** Time button full width (leading clock icon, label `{time}`, a11y `firstWeekSession_timeA11y` unchanged). Then "Update my plan" (primary). Then "Not sure yet" as a full-width `TextButton`, min 48 dp, `SubStyle.ink`. This sets the exit apart from the time and keeps it secondary.

```
┌──────────────────────────────────┐
│ When is your next session?       │
│ [ Just this once | From now on ] │
│ Your usual schedule stays ...    │
│ [Fri 10] [Sat 11] [Sun 12]       │
│ [Mon 13] [Tue 14] [Wed 15]       │
│ [Thu 16] [Fri 17] [Sat 18]       │
│ [ (clock) 5:00 PM              ] │  full width, 48 dp
│ [ Update my plan               ] │  primary, 56 dp
│        Not sure yet              │  text button, 48 dp
└──────────────────────────────────┘
```

## M-4 detail: the consent step in this context

Is reusing `onboarding_art9Consent*` plus "Continue"/"Cancel" clear here? Not fully:

- In onboarding the row sits in a list of personalisation choices, where "Personalise to your therapy" fits. Here it interrupts a concrete action ("Add sessions", "Update my plan"), and the title does not connect to it.
- The checkbox names "my therapy status". This flow stores session dates and times, and since 14.1 item 5 it also sets the in-therapy status. Settings describes the same consent as "therapy status" (`settings_useTherapyDataSubtitle`), so session times are named nowhere.
- "Continue" does not say it grants the permission, and "Cancel" does not say nothing was saved.

Before TestFlight (keeps the legal text unchanged):

- flutter-mobile: optional `lead`, `acceptLabel` and `declineLabel` parameters on `Art9ConsentStep`, used only by the session sheet. The Settings sheet keeps its current labels.
- brand-voice-manager, new keys:
  - `firstWeekSession_consentLead`, above the title, 16 sp, `SubStyle.ink`: "To save session times, MindSync needs your permission first."
  - `firstWeekSession_consentAllow`, primary: "Allow and continue".
  - `firstWeekSession_consentNotNow`, secondary: "Not now".
  - `firstWeekSession_consentWithdrawNote`, 14 sp under the checkbox: "You can withdraw this any time in Settings, under Privacy & Data."
  - `firstWeekSession_consentDeclinedToast`, info toast after "Not now": "Okay, nothing was saved."

Before store release (lead with the lawyer and security-guardian): confirm whether the onboarding text covers storing session times and the automatic in-therapy status. If it does not, use one context-specific text everywhere a schedule is written. Proposed:

- title: "Save your session times?"
- body: "Session days and times are health information. MindSync stores them only with your permission, to plan short steps before and after each session."
- checkbox: "Yes, MindSync may store my session times and that I'm in therapy."

## M-2 detail: rows at large text

The rule for every horizontal row of text plus button on first-week Home:

```dart
final stacked = MediaQuery.textScalerOf(context).scale(16) > 20 // > 1.25x
    || constraints.maxWidth < 300;                              // LayoutBuilder
```

Stacked Today card (dark):

```
┌──────────────────────────────┐
│ Today · about 3 min          │
│ Orca has a question for you  │
│ Answer in a few words or ... │
│ [      See the question     ]│  full width, min 52
│          Not today           │  full-width TextButton, min 48
│ Session moved?               │  link slot unchanged
└──────────────────────────────┘
```

## Contrast (WCAG 2.1, computed from `MsColors`)

| Pair | Ratio | Result |
|---|---|---|
| Dark card title `#FFFFFF` on `#113237` | 13.68 | AA |
| Dark body, quota line, "Not today" `#DBF0ED` on `#113237` | 11.53 | AA |
| Dark eyebrow `#AAE5E2` on `#113237` | 9.78 | AA |
| Links and "See Premium" `#FFC88A` on `#113237` | 9.04 | AA |
| CTA label `#113237` on `#FFC88A` | 9.04 | AA |
| Chip `#113237` on `#AAE5E2` | 9.78 | AA |
| "Not today" disabled (50%) | 4.06 | disabled, exempt |
| Light body `#5A7A73` on white | 4.70 | AA |
| Light eyebrow, Undo `#26767B` on white | 5.30 | AA |
| Next-box label `#26767B` on `#F2FBFA` | 5.04 | AA |
| Plan "Today" `#A06008` on white | 5.03 | AA |
| Plan chip `#1F4C50` on `#F2FBFA` | 9.04 | AA |
| Side card close icon `#5A7A73` on `#F2FBFA` | 4.47 | passes 3:1 for icons |
| Upcoming ring `#339499` on white | 3.60 | passes 3:1 |
| Light CTA fill `#DBF0ED` on white | 1.19 | boundary only, see p-1 |
| Time-button border `#BBE4DE` on white | 1.38 | below 3:1, see p-2 |

Information is never carried by colour alone: plan rows say "Done", "Today" or the day; the quota state is a sentence; the deferred state has its own title. The app has no dark theme (no `darkTheme` anywhere in `lib/`), so dark mode does not apply.

## Matches the design

- Order and content of first-week Home follow SPEC 6: hero, Today card, plan card, the shipped trial bar, B/C side card, "More when you're ready". Getting started, the next-session card, Therapy Relationship and the legacy modules are hidden (`first_week_home_cards.dart`, `main_tab_screen.dart:298-334`).
- The dark card is used for `today` and `quota_out`, the light card for `day0`, `deferred`, `done`, `rest` and `open`, as on `Main.dc.html`. Tokens match the board: radius 24, padding 20, CTA `#FFC88A` 52 dp radius 16, eyebrow `#AAE5E2`, body `#DBF0ED`, white light card with an `#DBF0ED` border.
- Copy keys are in the right places: the talk card says "{orcaName} has a question for you" / "See the question" (COPY decision 1); prep picks today or tomorrow from the session date; the B note title is copy only; chips follow the 2.1 rules; done reads "Next: {stepTitle}, tomorrow."; there is no "Included in your first week" anywhere.
- Plan card: collapsed chips plus one "Next" line, hidden on day 0 and in `done` (14.2 item 7), and shown on day 0. Expanded rows have text status, no counter and no progress bar. "Hide this plan" or "Change my rhythm" sits at the bottom. The expanded state is stored locally without tone.
- Gentle tone keeps the same widgets, keys and routes. It changes the hero subtitle, eyebrows, titles, bodies and the "When you're ready:" lead, puts the helpline in the link slot (session links stay on prep and after), hides the day-0 reminder row and hides "See Premium".
- No guilt or streak pressure: none of the banned words appear, "Not today" turns into "Okay, it'll wait" with Undo, dropped steps disappear silently, and there is no counter.
- `quota_out` cards put the free alternative first, show the line with the real limit and the UTC reset date, keep "See Premium" secondary, and hide it in gentle tone.
- Day-0 reminder row: off by default, the OS prompt only after an explicit toggle, a denied state with "Open Settings" and a recheck on resume, the late-night label and the privacy note.
- Quick check-in follows the board: a 5 by 2 grid of 48 dp buttons with 8 dp gaps, no preselected value, per-area Skip and "Skipped · Undo", "Also rate {area}", fieldset-style semantics, a static skeleton and a retry. The mirror shows numbers only, "Not set", the A agenda card with the privacy line, and the recap line on days 1 to 6.
- Follow-up: label, question and hint per variant; voice-open and voice-locked layouts; the memory footer only when quoted; the helpline only in gentle tone; a 404 returns silently and other failures return with a toast (14.2 item 6); a skeleton while loading.
- Session sheet: the COPY 6 ask view (decision 2), a real radio group for the scope with a live hint, 9 dated chips at 56 dp in a 3 by 3 grid, consent first for C, 403 leads to consent and one retry, and declining writes nothing. It is a modal, not a route.
- Recap: null sections are not built; gentle tone shows "Latest" only; "Not right" is a deferred delete with Undo; rhythm limit lines show on Free only; "Done" replaces "Keep this rhythm" when everything is off.
- Touch targets are at least 48 dp everywhere except the check-in score buttons at 320 dp (m-6). `MsTimePicker`, `MsMessage` toasts, `SubPrimaryButton` and the bottom-sheet shape are reused consistently. Replay masking wraps Home, the follow-up, the check-in and the recap.

## Not covered

- Behaviour on device (Figtree metrics, TalkBack and VoiceOver order) was reasoned from code, not observed. flutter-mobile should confirm M-2 and m-1 on a 320 dp emulator at 130% and 200% text.
- The day-3 trial sheet was not reviewed.
