# First-week Home: final English copy

Status: FINAL EN for build, 2026-10-08. Owner: brand-voice-manager. Section 14 (additions after the UX review, with translations) added 2026-10-11; sections 6, 8 and 13 aligned with it.
Built from: `SPEC.md` (section 13 is binding), the canvas v4 direction copy (`canvas/*.dc.html`), `canvas/canvas.json` notes and `audit-security-design.md` (H-1 to H-4, M-1, M-2, L-1, L-2, L-7).

Translators: translate the "EN" column only. Keep every `{placeholder}` exactly as written. The "Notes" column is for you and for the implementing agents.

## 0. Conventions

**Placeholders**

| Placeholder | Meaning |
|---|---|
| `{orcaName}` | The companion's name. Default "Orca", the person can rename it, up to 20 characters (`onboarding_companion_view.dart:150`). Same placeholder as the existing ARB strings. Never hardcode "Orca". |
| `{limit}` | The Free limit for that feature, from `GET /users/usage` (`features.<key>.limit`). Never type the number into a string. |
| `{prepLimit}`, `{afterLimit}`, `{betweenLimit}`, `{reflectLimit}`, `{recordingLimit}` | Per-feature limits, used where one string needs more than one. Same source. |
| `{resetDate}` | Local short date of `resets_at` from `GET /users/usage` ("Nov 1"). Use the same formatter as the shipped `usage_resetsOn`. |
| `{weekday}` | Localized weekday name ("Thursday"). |
| `{date}` | Localized date for accessibility labels ("October 10"). |
| `{time}` | Localized time ("7:00 pm"). |
| `{area}` | One focus area from setup. Only inside the check-in, mirror and recap screens. |
| `{setupScore}`, `{todayScore}`, `{latestScore}`, `{score}` | Whole numbers 1 to 10. |
| `{stepTitle}` | One of the plan row titles from section 4. |
| `{price}` | Store-formatted price. |

**Rules for every string in this file**

1. Keys. Client strings are ARB keys with the prefixes `firstWeek_`, `firstWeekCheckIn_`, `firstWeekMirror_`, `firstWeekFollowUp_`, `firstWeekSession_`, `trialDay3_`, `firstWeekRecap_`, `firstWeekRhythm_`. Push strings are server template keys for the static allowlist (section 11). "Reuse" means: use the existing key, do not create a duplicate.
2. Tone. A key ending in `Gentle` is the gentle-tone version of the same key without the suffix. The client picks it from `tone` (Cubit state, memory only). Same widget, same widget key, same route, same events (SPEC 3.6, H-1). Rows marked "standard only" never render in gentle tone. Anything without a `Gentle` row uses the same text in both tones.
3. Max. Maximum visible characters, measured with the default name "Orca". A string that contains `{orcaName}` must be allowed to wrap one more line. Never truncate or ellipsize.
4. Style. Sentence case. Straight apostrophes. The middle dot (·) is allowed as a separator in eyebrows and metadata, as the app already does. Digits for durations and counts in UI ("3 min", "30 sec"). Zero U+2014 and zero U+2013 (this file passes the mechanical scan).
5. Fixed names keep their capitals: Before therapy, After therapy, Between Sessions, Reflect, Mood & symptom trends, Weekly therapy summary, Therapy Relationship, Character, Premium, Free. Added 2026-10-11: My Therapy, Therapy Schedule, Account, Privacy & Data (real locations in 14.0).
6. Never on Home and never in a push: anything the person said, focus-area names, crisis words. The phrase "Included in your first week" does not exist anywhere (SPEC 13.2).
7. Words we do not use anywhere in this feature: missed, streak, behind, fail, catch up, don't lose, last chance, journey.

## Free limits (verified in code, 2026-10-08)

| Feature | `/users/usage` key | Free limit | Period | Source |
|---|---|---|---|---|
| Before therapy (`prep`) | `before_therapy` | 1 | calendar month, UTC, resets on the 1st | `MindSync/app/core/config.py:189` `FREE_TIER_MONTHLY_PREP_LIMIT`, read in `app/api/v1/endpoints/_therapy_helpers.py:105-106` |
| After therapy (`after`) | `after_therapy` | 1 | month | `config.py:188` `FREE_TIER_MONTHLY_DEBRIEF_LIMIT`, `_therapy_helpers.py:103-104` |
| Between Sessions (`note`) | `between_sessions` | 3 | month | `config.py:190` `FREE_TIER_MONTHLY_BETWEEN_SESSIONS_LIMIT`, `_therapy_helpers.py:107-108` |
| Reflect messages (writing to Orca, `talk`, `talk2`) | `reflect_messages` | 15 | month | `config.py:201` `REFLECT_MONTHLY_MESSAGE_LIMIT` |
| Session recordings | `session_recordings` | 2 | lifetime | `config.py:266` `FREE_TIER_RECORDING_LIMIT` |
| Habits | `habits` | 1 active | active | `MindSync/app/crud/habit.py:46` `FREE_TIER_MAX_ACTIVE_HABITS` |
| Quick check-in (symptom scores) | none | unlimited | | `MindSync/app/api/v1/endpoints/symptoms.py:5` ("FREE for all users") |
| Talking with Orca by voice | none | Premium only (client gate) | | `app_en.arb:3108` `firstConversation_voicePremiumNote`; backend key minting is still ungated (SPEC 3.7, prior M-6) |

The payload is built in `MindSync/app/services/plan_usage_service.py:141-185`; `resets_at` is 00:00 UTC on the 1st of next month (`plan_usage_service.py:56-66`). The values are not overridden in `MindSync/.env` (no matching key; comment at `config.py:187`). Trial and Premium return `limit: null`, so no chip and no quota state. The starter pack gives 14 days of Premium from the purchase (`config.py:270`, `subscription_service.py:822-828`).

Note on `{resetDate}`: in US time zones, 00:00 UTC on the 1st is the evening of the last day of the month. Use the exact date logic of the shipped `usage_resetsOn`, so the app never shows two different reset dates.

## 1. Home hero subtitle (first-week mode)

Body 16, two lines. No topics and no therapy words in any state.

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeek_heroSubtitleDay0` | Good to meet you. Here's how your first week looks. | 70 | Plan day 0 |
| `firstWeek_heroSubtitleWeek` | One small thing a day. The rest can wait. | 70 | Plan days 1 to 6, rest days included |
| `firstWeek_heroSubtitleDay7` | One week with {orcaName} today. | 70 | Plan day 7 |
| `firstWeek_heroSubtitleRhythm` | Your rhythm is set. Change it whenever you like. | 70 | Plan day 8 on |
| `firstWeek_heroSubtitleOwnPace` | Your own pace from here. | 70 | After "Hide this plan" or "I'll find my own way" |
| `firstWeek_heroSubtitleGentle` | Take your time. Nothing here is urgent. | 70 | Gentle, replaces every subtitle above |

**1b. "More when you're ready" block** (bottom of first-week Home, SPEC 6)

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeek_moreHeading` | More when you're ready | 30 | |
| `firstWeek_moreTrendsMetaSetup` | Your focus areas from setup | 36 | Under "Mood & symptom trends" (existing title) before the first check-in |
| `firstWeek_moreTrendsMetaLatest` | Setup and your latest check-in | 36 | After the first check-in |
| `firstWeek_moreHabitsMeta` | Track one small thing each day | 36 | Under "Habits" (existing title) |

## 2. Today card

### 2.1 Shared elements

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeek_todayA11y` | Today | | Section label for screen readers |
| `firstWeek_notToday` | Not today | 12 | Both tones |
| `firstWeek_undo` | Undo | 8 | |
| `firstWeek_sessionMovedLink` | Session moved? | 20 | Link slot on `prep` |
| `firstWeek_didntHappenLink` | It didn't happen | 20 | Link slot on `after` |
| reuse `postOnboarding_calmHelplineLink` | Find a helpline near you | | Gentle only. A11y: reuse `postOnboarding_calmHelplineLinkA11y`. External browser, no event. |
| `firstWeek_ctaTalk` | Talk with {orcaName} | 20 | Shared CTA |
| `firstWeek_ctaTalkShort` | Start talking | 16 | Optional fallback when the name makes the CTA wrap next to "Not today" (names over 10 characters). Allowing a 2-line button is also fine. |
| `firstWeek_ctaQuickCheckIn` | Quick check-in | 18 | |
| `firstWeek_seePremium` | See Premium | 14 | Quota line. Standard only (decision 7). |
| reuse `usage_chipOneFree` | 1 free this month | 18 | Chip when one use is left and the limit is 1 |
| reuse `usage_chipLastMonthly` | Last one this month | 20 | Chip when one use is left and the limit is above 1 (Between Sessions) |

Eyebrows (14, one line, shares the row with a chip):

| Key | EN | Max | Used on |
|---|---|---|---|
| `firstWeek_eyebrow3Min` | Today · about 3 min | 26 | `talk`, `talk2` |
| `firstWeek_eyebrow2Min` | Today · 2 min | 26 | `prep` |
| `firstWeek_eyebrow1Min` | Today · 1 min | 26 | `note` |
| `firstWeek_eyebrow30Sec` | Today · 30 sec | 26 | `checkin` |
| `firstWeek_eyebrowRead2Min` | Today · 2 min read | 26 | `recap` |
| `firstWeek_eyebrowAfterSession` | Today · after your session | 26 | `after` |
| `firstWeek_eyebrowIfItHelpsGentle` | Today · only if it helps | 26 | Gentle `prep`, `after`, `note`, `checkin` |
| `firstWeek_eyebrowIfYouWantGentle` | Today · only if you want | 26 | Gentle `talk`, `talk2`, `recap` |

### 2.2 State "today" (dark card), per step

Title 24 bold, 2 lines (max 44). Body 16, 3 lines (max 120). CTA 17 bold next to "Not today" (max 20).

| Step | Element | Key | EN | Notes |
|---|---|---|---|---|
| `talk` | title | `firstWeek_todayTalkTitle` | {orcaName} has a question for you | First conversation happened. True for the memory question and the generic one (decision 1). |
| `talk` | body | `firstWeek_todayTalkBody` | Answer in a few words or a few paragraphs, whatever comes. | |
| `talk` | CTA | `firstWeek_todayTalkCta` | See the question | Opens the follow-up screen |
| `talk` (first talk skipped) | title | `firstWeek_todayFirstTalkTitle` | Your first talk with {orcaName} | SPEC 3.3 |
| `talk` (first talk skipped) | body | `firstWeek_todayFirstTalkBody` | Whenever you're ready. Start with whatever is on your mind, out loud or in writing. | Plan days 1-2 are always inside the trial, so voice is available |
| `talk` (first talk skipped) | CTA | `firstWeek_ctaTalk` | Talk with {orcaName} | |
| `talk2` | title | `firstWeek_todayTalk2Title` | A short talk with {orcaName} | |
| `talk2` | body | `firstWeek_todayTalk2Body` | How has the week been so far? {orcaName} will listen. | No voice promise: day 6 is after the trial |
| `talk2` | CTA | `firstWeek_ctaTalk` | Talk with {orcaName} | |
| `prep` | title | `firstWeek_todayPrepTitleTomorrow` | Get ready for tomorrow's session | Day before the session |
| `prep` | title | `firstWeek_todayPrepTitleToday` | Get ready for today's session | Session on plan day 1, card in the morning |
| `prep` | body | `firstWeek_todayPrepBody` | What do you want to bring up? Note it now, and it'll be ready to read right before you start. | Works for in-person and online sessions |
| `prep` | CTA | `firstWeek_todayPrepCta` | Start Before therapy | 20 |
| `prep` | link | `firstWeek_sessionMovedLink` | Session moved? | |
| `after` | title | `firstWeek_todayAfterTitle` | After your session today | Reads right before and after the session |
| `after` | body | `firstWeek_todayAfterBody` | When it's over, a few words are enough. Best while it's still fresh. | |
| `after` | CTA | `firstWeek_todayAfterCta` | Start After therapy | |
| `after` | link | `firstWeek_didntHappenLink` | It didn't happen | |
| `note` (C) | title | `firstWeek_todayNoteTitle` | Leave a voice note | |
| `note` (B) | title | `firstWeek_todayNoteTitleTherapy` | Note something for therapy | Copy only; same feature, screen, route and events as C (M-1) |
| `note` (C) | body | `firstWeek_todayNoteBody` | Say how your week is going. {orcaName} turns it into a short summary. | |
| `note` (B) | body | `firstWeek_todayNoteBodyTherapy` | Say what happened this week that you might want to bring up. {orcaName} turns it into a short summary. | |
| `note` | CTA | `firstWeek_todayNoteCta` | Record a voice note | |
| `checkin` | title | `firstWeek_todayCheckInTitle` | Quick check-in | |
| `checkin` | body | `firstWeek_todayCheckInBody` | Rate the things you picked in setup, then see today next to where you started. | |
| `checkin` | CTA | `firstWeek_todayCheckInCta` | Start check-in | |
| `recap` | title | `firstWeek_todayRecapTitle` | Your first week is ready | |
| `recap` | body | `firstWeek_todayRecapBody` | A short look back, plus a rhythm for the weeks ahead if you want one. | True even when "Orca noticed" is hidden |
| `recap` | CTA | `firstWeek_todayRecapCta` | See my week | |
| rhythm `talk` (day 8 on) | title | `firstWeek_todayRhythmTalkTitle` | Your talk with {orcaName} | Wednesday option. Other rhythm steps reuse the `checkin`, `note`, `prep`, `after` rows above. |
| rhythm `talk` | body | `firstWeek_todayRhythmTalkBody` | A few minutes about your week. | |

Gentle "today" (same CTA destination as standard for every step; the gentle `checkin` card still opens the check-in):

| Step | Element | Key | EN |
|---|---|---|---|
| `talk`, first talk, `talk2`, rhythm `talk` | title | `firstWeek_todayTalkTitleGentle` | {orcaName} is here when you're ready |
| same | body | `firstWeek_todayTalkBodyGentle` | You don't need to prepare anything. If you'd like to talk, {orcaName} will listen. |
| same | CTA | `firstWeek_ctaTalk` | Talk with {orcaName} |
| `prep` | title | `firstWeek_todayPrepTitleTomorrowGentle` | Tomorrow's session |
| `prep` | title | `firstWeek_todayPrepTitleTodayGentle` | Today's session |
| `prep` | body | `firstWeek_todayPrepBodyGentle` | If it helps, note what you'd like your therapist to know. A few words are enough. |
| `prep` | CTA | `firstWeek_todayPrepCtaGentle` | Open Before therapy |
| `after` | title | `firstWeek_todayAfterTitleGentle` | After today's session |
| `after` | body | `firstWeek_todayAfterBodyGentle` | If you feel up to it, keep a few words about it. It can also wait. |
| `after` | CTA | `firstWeek_todayAfterCtaGentle` | Open After therapy |
| `note` (B and C) | title | `firstWeek_todayNoteTitleGentle` | A voice note, if it helps |
| `note` | body | `firstWeek_todayNoteBodyGentle` | Say whatever is on your mind, or leave it for another day. |
| `checkin` | title | `firstWeek_todayCheckInTitleGentle` | A quick check-in, if you want |
| `checkin` | body | `firstWeek_todayCheckInBodyGentle` | Rate only what feels okay to rate. You can skip any of them. |
| `recap` | title | `firstWeek_todayRecapTitleGentle` | Your first week |
| `recap` | body | `firstWeek_todayRecapBodyGentle` | A short look back, whenever you want it. |

Gentle `note`, `checkin` and `recap` keep their standard CTA strings. Gentle cards carry the helpline link in the link slot; on `prep` and `after` the session links stay available as well.

### 2.3 Other states (light card)

| State | Element | Key | EN | Max | Notes |
|---|---|---|---|---|---|
| deferred | title | `firstWeek_deferredTitle` | Okay, it'll wait | 44 | After "Not today" |
| deferred | body | `firstWeek_deferredBody` | No reminder today. If there's room later this week, it'll come back. | 120 | Honest about "moves once, then dropped" |
| deferred | action | `firstWeek_undo` | Undo | 8 | |
| deferred | title | `firstWeek_deferredTitleGentle` | Okay, it can wait | 44 | |
| deferred | body | `firstWeek_deferredBodyGentle` | Nothing else is planned for today. {orcaName} is here if you want to talk. | 120 | |
| waiting | title | `firstWeek_waitingTitle` | Almost ready | 44 | Today's step exists but its content is not ready yet. Both tones. See decision 16. |
| waiting | body | `firstWeek_waitingBody` | {orcaName} is still getting today's step ready. Check back in a few minutes. | 120 | |
| waiting (`recap`) | title | `firstWeek_waitingRecapTitle` | Your first week is almost ready | 44 | Recap still being built |
| waiting (`recap`) | body | `firstWeek_waitingRecapBody` | {orcaName} is putting it together. Check back in a little while. | 120 | |
| done | title | `firstWeek_doneTitle` | Done for today | 44 | Both tones |
| done | body | `firstWeek_doneNextTomorrow` | Next: {stepTitle}, tomorrow. | 120 | |
| done | body | `firstWeek_doneNextOnDay` | Next: {stepTitle}, on {weekday}. | 120 | |
| done | body | `firstWeek_doneNothingNext` | That's everything planned for this week. | 120 | |
| done | body | `firstWeek_doneBodyGentle` | That's enough for today. {orcaName} is here if you want to talk. | 120 | Plus helpline |
| rest | title | `firstWeek_restTitle` | Nothing planned today | 44 | Both tones |
| rest | body | `firstWeek_restBody` | That's on purpose. If something comes up, {orcaName} is here. | 120 | CTA `firstWeek_ctaTalk` |
| rest | body | `firstWeek_restBodyNoMessages` | That's on purpose. A quick check-in is free any day. | 120 | Free with 0 Reflect messages left; CTA `firstWeek_ctaQuickCheckIn` |
| rest | body | `firstWeek_restBodyGentle` | Take your time. {orcaName} is here if you want to talk. | 120 | Plus helpline |
| plan hidden | title | `firstWeek_hiddenTitle` | {orcaName} is here when you want to talk | 44 | After "Hide this plan" or "I'll find my own way". CTA `firstWeek_ctaTalk`. Gentle: use the gentle `talk` title and body. |
| plan hidden | body | `firstWeek_hiddenBody` | Talk about whatever is on your mind, whenever it suits you. | 120 | |

### 2.4 Quota out (SPEC 3.8 as amended by 13.2)

Applies whenever the account is on Free (trial over, no Premium, no active starter), plan days 4 to 7 included, and the feature has `used >= limit`. Never straight into the paywall: free alternative first, then the quota line and "See Premium". No usage data means no chip and the normal card. The quota line is 14 and may wrap to 2 lines (max 52). Bodies carry no number on purpose: the line under them shows it, and they stay correct for any limit.

| Step | Element | Key | EN |
|---|---|---|---|
| `prep` | title | (unchanged `prep` title) | Get ready for tomorrow's session |
| `prep` | body | `firstWeek_quotaPrepBody` | You've used this month's free Before therapy. Your agenda is still free, so you can add what you want to bring up. |
| `prep` | CTA | `firstWeek_quotaPrepCta` | Add to my agenda |
| `prep` | line | `firstWeek_quotaPrepLine` | Before therapy: 0 of {limit} left until {resetDate} |
| `prep` | body (gentle) | `firstWeek_quotaPrepBodyGentle` | You've used this month's free Before therapy. If it helps, add a few words to your agenda instead. |
| `after` | title | (unchanged `after` title) | After your session today |
| `after` | body | `firstWeek_quotaAfterBody` | You've used this month's free After therapy. Save one takeaway to your agenda, then do a quick check-in if you like. |
| `after` | CTA | `firstWeek_quotaAfterCta` | Save a takeaway |
| `after` | line | `firstWeek_quotaAfterLine` | After therapy: 0 of {limit} left until {resetDate} |
| `after` | body (gentle) | `firstWeek_quotaAfterBodyGentle` | You've used this month's free After therapy. If you want, save one takeaway to your agenda. It can also wait. |
| `talk`, `talk2`, rhythm `talk` | title | `firstWeek_quotaTalkTitle` | Free messages are back on {resetDate} |
| same | body | `firstWeek_quotaTalkBody` | You've used this month's free messages. A quick check-in is free any day. |
| same | CTA | `firstWeek_ctaQuickCheckIn` | Quick check-in |
| same | line | `firstWeek_quotaTalkLine` | Reflect messages: 0 of {limit} left until {resetDate} |
| same | body (gentle) | `firstWeek_quotaTalkBodyGentle` | You've used this month's free messages. A quick check-in is always free, if you want one. |
| `note` | title | `firstWeek_quotaNoteTitle` | Free notes are back on {resetDate} |
| `note` | body | `firstWeek_quotaNoteBody` | You've used this month's free Between Sessions notes. A quick check-in is free any day. |
| `note` | CTA | `firstWeek_ctaQuickCheckIn` | Quick check-in |
| `note` | line | `firstWeek_quotaNoteLine` | Between Sessions: 0 of {limit} left until {resetDate} |
| `note` | body (gentle) | `firstWeek_quotaNoteBodyGentle` | You've used this month's free Between Sessions notes. A quick check-in is always free, if you want one. |

One use left: show the chip from 2.1 (`usage_chipOneFree` or `usage_chipLastMonthly`) and the normal card. In gentle tone: the eyebrow is the gentle one from 2.1; `prep` and `after` keep their gentle titles from 2.2; `talk` and `note` keep the factual quota titles above ("Free messages are back on {resetDate}", "Free notes are back on {resetDate}"), because their CTA is the check-in, not a talk; the bodies are the gentle ones above.

## 3. Day-0 card (light card, plan day 0)

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeek_day0Title` | You're set for today | 44 | Standard only |
| `firstWeek_day0Body` | Setup and your first talk with {orcaName} are done. That's plenty for day one. | 120 | First conversation happened |
| `firstWeek_day0BodySkipped` | Setup is done. Your first talk with {orcaName} can wait until you're ready. | 120 | First conversation skipped; day 0 never claims it happened |
| `firstWeek_day0NextLabelTomorrow` | Tomorrow | 20 | Label of the next-step box |
| `firstWeek_day0NextLabelAfterSleep` | After some sleep | 20 | Onboarding between 00:00 and 04:00 local (still plan day 0) |
| `firstWeek_day0NextTalk` | {orcaName} will have a question for you. About 3 minutes. | 80 | Day-1 step `talk` |
| `firstWeek_day0NextFirstTalk` | Your first talk with {orcaName}, whenever you're ready. About 3 minutes. | 80 | First conversation skipped |
| `firstWeek_day0NextPrep` | Get ready for your session. About 2 minutes. | 80 | Session on plan day 1 (prep moves to that morning) |
| `firstWeek_reminderToggleTomorrow` | Remind me tomorrow | 24 | Standard only; OS permission undecided |
| `firstWeek_reminderToggleLaterToday` | Remind me later today | 24 | Late-night onboarding |
| `firstWeek_reminderTimeA11y` | Reminder time, {time}. Change time | | The visible button shows `{time}` only |
| `firstWeek_reminderNoteOff` | One reminder a day at most. It never shows what you said or wrote. | 90 | Under the switch while off |
| `firstWeek_reminderNoteOn` | Your phone will ask you to allow notifications. One reminder a day at most, and it never shows what you said or wrote. | 130 | After toggling on, before the OS answer |
| `firstWeek_reminderSet` | Reminder on for {time}. Never more than one a day. | 70 | OS permission granted |
| `firstWeek_notificationsOff` | Notifications are off for MindSync on this phone. | 60 | OS permission denied; standard only |
| `firstWeek_openSettings` | Open Settings | 16 | Opens the OS app settings |
| `firstWeek_day0TitleGentle` | Take the rest of today easy | 44 | Gentle |
| `firstWeek_day0BodyGentle` | There's nothing else to do today. {orcaName} is here whenever you want to talk. | 120 | Gentle |
| `firstWeek_day0NextGentle` | {orcaName} will be here, whenever you want to talk. | 80 | Gentle next-step box text, with the same two labels; plus helpline link |

The reminder row, the granted line and the denied row never render in gentle tone (SPEC 3.6), and they are never offered later by a rule only formerly gentle accounts reach.

## 4. Plan card

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeek_planTitle` | Your first week | 24 | Plan days 0 to 7 |
| `firstWeek_planTitleRhythm` | This week | 24 | Day 8 on |
| `firstWeek_planExpand` | See the week | 16 | |
| `firstWeek_planCollapse` | Show less | 16 | |
| `firstWeek_planNextLead` | Next: | 8 | Collapsed line: lead, then `{stepTitle}` in bold, then ` · {when}` |
| `firstWeek_planNextLeadGentle` | When you're ready: | 20 | Gentle |
| `firstWeek_whenDone` | Done | 10 | Row status |
| `firstWeek_whenToday` | Today | 10 | |
| `firstWeek_whenTomorrow` | Tomorrow | 10 | Other days: short localized weekday, no string |
| `firstWeek_planHide` | Hide this plan | 20 | Bottom of the expanded card, week 1 |
| `firstWeek_planChangeRhythm` | Change my rhythm | 20 | Same slot, day 8 on |
| `firstWeek_planHiddenSnackbar` | Plan hidden. Its reminders are off too. | 50 | After "Hide this plan" |

Rows (title 16, max 32; meta 14, max 30). These titles are also the `{stepTitle}` values.

| Step | Title key | Title EN | Meta key | Meta EN |
|---|---|---|---|---|
| setup (day 0) | `firstWeek_rowSetupTitle` | Set up MindSync | `firstWeek_rowSetupMeta` | Your starting point is saved |
| first talk (day 0) | `firstWeek_rowFirstTalkTitle` | First talk with {orcaName} | `firstWeek_rowFirstTalkMeta` | On your first day |
| `talk` | `firstWeek_rowTalkTitle` | Follow-up talk | `firstWeek_rowAbout3Min` | About 3 min |
| `talk` (first talk skipped) | reuse `firstWeek_rowFirstTalkTitle` | First talk with {orcaName} | `firstWeek_rowAbout3Min` | About 3 min |
| `prep` | `firstWeek_rowPrepTitle` | Get ready for your session | `firstWeek_rowPrepMeta` | Before therapy · 2 min |
| `after` | `firstWeek_rowAfterTitle` | After your session | `firstWeek_rowAfterMeta` | After therapy · 2 min |
| `note` (C) | reuse `firstWeek_todayNoteTitle` | Leave a voice note | `firstWeek_rowNoteMeta` | Between Sessions · 1 min |
| `note` (B) | reuse `firstWeek_todayNoteTitleTherapy` | Note something for therapy | `firstWeek_rowNoteMeta` | Between Sessions · 1 min |
| `checkin` | reuse `firstWeek_todayCheckInTitle` | Quick check-in | `firstWeek_rowCheckInMeta` | 30 sec |
| `talk2` | reuse `firstWeek_todayTalk2Title` | A short talk with {orcaName} | `firstWeek_rowAbout3Min` | About 3 min |
| `recap` | `firstWeek_rowRecapTitle` | Your first week | `firstWeek_rowRecapMeta` | A look back · 2 min |
| rhythm `talk` | reuse `firstWeek_ctaTalk` | Talk with {orcaName} | `firstWeek_rowRhythmTalkMeta` | Wednesdays · about 3 min |
| rhythm `checkin` | reuse `firstWeek_todayCheckInTitle` | Quick check-in | `firstWeek_rowRhythmCheckInMeta` | Mondays · 30 sec |
| rhythm `note` | reuse `firstWeek_todayNoteTitle` | Leave a voice note | `firstWeek_rowRhythmNoteMeta` | Fridays · 1 min |
| rhythm `prep`, `after` | same as week 1 | | same as week 1 | |

Done chips (14, max 16):

| Step | Key | EN |
|---|---|---|
| setup | `firstWeek_chipSetup` | Setup |
| first talk | `firstWeek_chipFirstTalk` | First talk |
| `talk` | `firstWeek_chipFollowUp` | Follow-up |
| `prep` | `firstWeek_chipPrep` | Before therapy |
| `after` | `firstWeek_chipAfter` | After therapy |
| `note` | `firstWeek_chipNote` | Voice note |
| `checkin` | `firstWeek_chipCheckIn` | Check-in |
| `talk2` | `firstWeek_chipTalk2` | Short talk |
| `recap` | `firstWeek_chipRecap` | Week recap |

## 5. Side cards (B and C, both tones)

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeek_sideNextSessionTitle` | When is your next session? | 32 | B |
| `firstWeek_sideNextSessionBody` | Add the day and time, and your plan will include a short step before and after it. | 110 | B; consent already active |
| `firstWeek_sideNextSessionCta` | Add session time | 20 | B; opens the schedule directly |
| `firstWeek_sideTherapistTitle` | Seeing a therapist? | 32 | C |
| `firstWeek_sideTherapistBody` | Add your session times, and your plan will include a short step before and after each one. | 110 | C |
| `firstWeek_sideTherapistCta` | Add sessions | 20 | C; opens the Art. 9 consent step first when consent is not active (H-3). Declining stores nothing. |
| `firstWeek_sideDismissA11y` | Hide this card | | Close icon label |

## 6. Session sheet

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeekSession_askTitle` | What happened with today's session? | 44 | Entry from "It didn't happen" on `after` (decision 2) |
| `firstWeekSession_askBody` | Sessions move. Your plan will follow. | 80 | |
| `firstWeekSession_optionMoved` | It moved to another day | 32 | Opens the date view |
| `firstWeekSession_optionDidntHappen` | It didn't happen this time | 32 | Drops `after`, keeps the schedule |
| `firstWeekSession_optionHappened` | It happened after all | 32 | Text button; opens After therapy |
| `firstWeekSession_movedTitleNext` | When is your next session? | 44 | Entry from "Session moved?" on `prep` |
| `firstWeekSession_movedTitleNow` | When is the session now? | 44 | Entry from "It moved to another day" |
| `firstWeekSession_scopeA11y` | Apply this change to | | Radio group label |
| `firstWeekSession_scopeOnce` | Just this once | 16 | |
| `firstWeekSession_scopeOnceHint` | Your usual schedule stays the same. | 60 | Shown under the segment while selected. "Just this once" must never overwrite the recurring schedule. |
| `firstWeekSession_scopeAlways` | From now on | 16 | |
| `firstWeekSession_scopeAlwaysHint` | This becomes your usual day and time. | 60 | |
| `firstWeekSession_dayA11y` | {weekday}, {date} | | Dated chips for the next 8 days; the visible chip is the short weekday and the day number, no string |
| `firstWeekSession_timeA11y` | Session time, {time}. Change time | | Visible button shows `{time}` |
| `firstWeekSession_notSure` | Not sure yet | 16 | |
| `firstWeekSession_update` | Update my plan | 20 | Primary |
| `firstWeekSession_updatedSnackbar` | Plan updated. | 30 | |
| `firstWeekSession_notSureTitle` | Okay, no date for now | 44 | After "Not sure yet" |
| `firstWeekSession_notSureBody` | Your plan skips the steps for this session. When you know the new date, add it in My Therapy, under Therapy Schedule. | 120 | Revised 2026-10-11 (14.3). The schedule lives in My Therapy (`myTherapy_title`, `myTherapy_scheduleSectionTitle`), not in Settings; the old text also said "for now", but dropped steps do not come back. |
| `firstWeekSession_didntTitle` | Okay, nothing to capture today | 44 | |
| `firstWeekSession_didntBody` | Your plan skips this step, and your usual schedule stays as it is. If you'd like to talk about the week instead, {orcaName} is here. | 140 | Secondary CTA `firstWeek_ctaTalk`. On Free with 0 Reflect messages left: `firstWeekSession_didntBodyNoTalk` (14.2) and no talk button. |
| reuse `premiumWelcome_backHome` | Back to home | | Primary on the two result views |

Additions after the UX review (the Art. 9 consent step in this sheet, `didntBodyNoTalk`, "Not sure yet"): section 14.

## 7. Quick check-in and mirror

### 7.1 Quick check-in

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeekCheckIn_title` | Quick check-in | 24 | Top bar |
| `firstWeekCheckIn_durationChip` | 30 sec | 8 | |
| `firstWeekCheckIn_closeA11y` | Close | | |
| `firstWeekCheckIn_heading` | How strong is each one today? | 44 | Mirrors onboarding (`onboarding_intensityTitle`) |
| `firstWeekCheckIn_subheading` | 1 is barely there, 10 is overwhelming. | 60 | |
| reuse `onboarding_intensityLow` / `onboarding_intensityHigh` | Barely there / Overwhelming | 14 each | Scale end labels |
| `firstWeekCheckIn_areaA11y` | {area}, from 1, barely there, to 10, overwhelming | | Fieldset legend |
| `firstWeekCheckIn_skip` | Skip | 10 | Per area |
| `firstWeekCheckIn_skippedUndo` | Skipped · Undo | 16 | Same button after skipping |
| `firstWeekCheckIn_alsoRate` | Also rate {area} | 32 | Areas beyond the top 3 |
| `firstWeekCheckIn_save` | Save check-in | 20 | Disabled until one area has a value |
| `firstWeekCheckIn_savedTo` | Saved to Mood & symptom trends. | 40 | Under the button |
| `firstWeekCheckIn_saveFailed` | That didn't save. Please try again. | 50 | |

### 7.2 Mirror (after saving)

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeekMirror_title` | Check-in saved | 30 | |
| `firstWeekMirror_subtitle` | Here it is next to where you started in setup. | 70 | |
| `firstWeekMirror_colSetup` | Setup | 8 | Column label |
| `firstWeekMirror_colToday` | Today | 8 | |
| `firstWeekMirror_notSet` | Not set | 10 | Areas left at the untouched default in onboarding; also used in the recap |
| `firstWeekMirror_rowA11y` | {area}: {setupScore} in setup, {todayScore} today | | Numbers only, no verdict |
| `firstWeekMirror_rowA11yNotSet` | {area}: not set in setup, {todayScore} today | | |
| `firstWeekMirror_nextTitleSession` | Bring this to your next session? | 44 | Variant A |
| `firstWeekMirror_nextBodySession` | Add today's numbers to your agenda. You decide what to say about them. | 100 | Variant A (decision 10) |
| `firstWeekMirror_nextCtaSession` | Add to my agenda | 20 | Variant A; confirmation reuses `workspace_topicsAddedToAgenda` ("Added to agenda") |
| `firstWeekMirror_privacyLine` | Only you see this, unless you share it or connect a therapist in MindSync. | 90 | Variant A, under the CTA (L-7) |
| `firstWeekMirror_nextTitleTalk` | Want to talk any of this over? | 44 | Variants B and C |
| `firstWeekMirror_nextBodyTalk` | {orcaName} can go through it with you, at your pace. | 100 | B and C; CTA `firstWeek_ctaTalk` |
| `firstWeekMirror_recapLine` | You'll see this again in your first-week look back. | 70 | Only on plan days 1 to 6 with an active plan |
| reuse `premiumWelcome_backHome` | Back to home | | |

One event for the next-step card, without a `cta` property (M-1).

## 8. Follow-up screen (Reflect, day 1)

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeekFollowUp_header` | Reflect | 16 | Top bar |
| `firstWeekFollowUp_backA11y` | Back | | |
| `firstWeekFollowUp_labelMemory` | From your first talk | 30 | Memory question (`quoted: true`) |
| `firstWeekFollowUp_hintMemory` | {orcaName} is picking up from something you said. Answer as much or as little as you like. | 110 | Memory question |
| `firstWeekFollowUp_labelGeneric` | A question for today | 30 | Generic question (`quoted: false`, standard tone) |
| `firstWeekFollowUp_questionGeneric` | RETIRED 2026-10-11 (was "How have the last few days been?") | | Retired: generic and calm now share one fixed question per language, so the stored first message cannot tell the two cases apart (API_CONTRACT 14.2 item 9, security H-1). The generic case uses `firstWeekFollowUp_questionCalm`. See 14.5. |
| `firstWeekFollowUp_hintGeneric` | Start wherever you like. A few words are enough. | 110 | |
| `firstWeekFollowUp_labelCalm` | Whenever you're ready | 30 | Gentle tone, crisis guard hit, or any failed display check |
| `firstWeekFollowUp_questionCalm` | How are you doing right now? | 60 | Calm question, no quote. Since 2026-10-11 also the generic question (14.5). Persisted as Orca's first message: the server's fixed string per language must equal this key's ARB value. |
| `firstWeekFollowUp_hintCalm` | Say as much or as little as you want. {orcaName} will listen. | 110 | Plus helpline link (gentle tone only) |
| `firstWeekFollowUp_micA11y` | Talk with {orcaName}, about 3 minutes | | During the trial |
| `firstWeekFollowUp_tapToTalk` | Tap to talk · about 3 minutes | 36 | During the trial |
| `firstWeekFollowUp_writeInstead` | Write instead | 20 | During the trial |
| `firstWeekFollowUp_writeCta` | Write to {orcaName} | 24 | After the trial, on Free: primary |
| `firstWeekFollowUp_voiceCta` | Talk by voice | 20 | After the trial, on Free: secondary, with badge |
| `firstWeekFollowUp_premiumBadge` | Premium | 10 | Badge on "Talk by voice" |
| reuse `usage_reflectLeftLine` | {left} of {limit} free messages left this month | | Optional line under the buttons on Free. Replaces the removed "Included in your first week". At 0 left the existing Reflect "none left" state applies. |
| `firstWeekFollowUp_memoryFooter` | This question comes from a note {orcaName} kept from your first talk. You can see or delete it in Settings, under What {orcaName} remembers. | 160 | Only when `quoted: true` |

The question text itself comes from the server. Same route, same seed source and same events for all three question types (SPEC 3.9).

**Brief for the generated memory question (data-analytics prompt, not a client string)**

- One question, at most 110 characters, second person, plain text.
- Open with a short paraphrase of the memory item in the person's own everyday words, then ask about the time since. Pattern from the canvas: "You mentioned sleep has been rough lately. How have the last few nights been?"
- No diagnosis or clinical labels, no advice, no "why" questions, no assumption that things got better or worse, no names of other people, no quotes longer than a few words.
- No em dash, no en dash, no emoji. Crisis rules from SPEC 3.9 unchanged.

## 9. Day-3 trial sheet

Shown once, after today's step is done (or on the next open on a rest day), never to starter or Premium buyers. Same `trial_reminder_sheet_shown` event in every version; the offer uses the existing paywall and offer events with the new `trigger_feature` value (SPEC 13.3).

| Key | EN | Max | Notes |
|---|---|---|---|
| reuse `trialReminder_eyebrow` | Day 3 of 4 | | |
| reuse `trialReminder_title` | Your Premium trial ends tomorrow | | Standard |
| `trialDay3_subtitle` | Everything you saved stays saved either way. | 70 | Standard |
| `trialDay3_didHeading` | Your first days | 24 | Items: the `firstWeek_did*` strings from section 10, done steps only |
| `trialDay3_freeTitle` | Your first week continues on Free. | 44 | |
| `trialDay3_freeBody` | After tomorrow, talking with {orcaName} by voice is part of Premium. Writing stays on Free, up to {limit} messages a month. | 140 | `{limit}` = `reflect_messages` limit |
| `trialDay3_freeLimitsAll` | Each month on Free: {prepLimit} Before therapy, {afterLimit} After therapy, {betweenLimit} Between Sessions and {reflectLimit} Reflect messages. Session recordings: {recordingLimit} in total. | 200 | Optional small print. Replaces the hardcoded numbers in `trialReminder_freeLimits` (`app_en.arb:2932`). |

Offer block, only when the store still lets this account redeem the starter pack:

| Key | EN | Max | Notes |
|---|---|---|---|
| `trialDay3_offerTitle` | 2 weeks of Premium, one payment | 36 | Same starter SKU as after onboarding |
| `trialDay3_offerBody` | {price} once. Premium for 2 weeks from today, then you move to Free. Nothing renews. | 110 | True on day 3: the pack runs 14 days from the purchase |
| `trialDay3_offerCta` | Get 2 weeks for {price} | 26 | Primary |
| `trialDay3_seeAllPlans` | See all plans | 20 | Secondary text button; opens the regular paywall |
| reuse `trialReminder_notNow` | Not now | | |

Not eligible for the offer (already redeemed, store says no, or prices failed to load):

| Key | EN | Notes |
|---|---|---|
| reuse `trialReminder_keepPremium` | Keep Premium | Primary, opens the regular paywall |
| reuse `trialReminder_notNow` | Not now | |

Gentle tone (the sheet still shows when eligible, H-1; only the top changes, the offer stays factual):

| Key | EN | Max |
|---|---|---|
| `trialDay3_titleGentle` | Your trial ends tomorrow | 44 |
| `trialDay3_subtitleGentle` | Nothing you saved goes away, and {orcaName} is still here on Free. You don't need to decide anything today. | 130 |

## 10. Day-7 recap and rhythm

### 10.1 Recap

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeekRecap_closeA11y` | Close | | |
| `firstWeekRecap_title` | Your first week with {orcaName} | 44 | |
| `firstWeekRecap_subtitle` | Here's what this week looked like. | 70 | Full week |
| `firstWeekRecap_subtitleQuiet` | A quiet week is fine. Here's what happened, and {orcaName} is here whenever you want to talk. | 120 | Quiet week, and also the subtitle in gentle tone |
| `firstWeekRecap_didHeading` | What you did | 24 | Done steps only |
| `firstWeekRecap_whereHeading` | Where things are | 24 | Hidden when there is no check-in |
| `firstWeekRecap_setupValue` | Setup {score} | 12 | |
| `firstWeekRecap_latestValue` | Latest {score} | 12 | |
| reuse `firstWeekMirror_notSet` | Not set | | Untouched default areas |
| `firstWeekRecap_rowA11y` | {area}: {setupScore} in setup, {latestScore} at the latest check-in | | |
| `firstWeekRecap_rowA11yNotSet` | {area}: not set in setup, {latestScore} at the latest check-in | | |
| `firstWeekRecap_rowA11yLatestOnly` | {area}: {latestScore} at the latest check-in | | Gentle or any flag in the week: show "Latest" only, no setup value next to it (no deltas, SPEC 3.6) |
| `firstWeekRecap_noticedHeading` | {orcaName} noticed | 24 | Hidden after any flag in the week. Body is generated (one or two sentences, an observation without a verdict, crisis-screened). |
| `firstWeekRecap_mentionedHeading` | You mentioned | 24 | Live memory items only; hidden without memory consent |
| `firstWeekRecap_notRight` | Not right | 12 | Calls `DELETE /users/memory/{id}` |
| `firstWeekRecap_removed` | Removed. {orcaName} won't use this note anymore. | 60 | Replaces the item text after deletion |
| `firstWeekRecap_undo` | Undo | 8 | Only if the client delays the DELETE (decision 8) |
| `firstWeekRecap_seeAllMemory` | See all in What {orcaName} remembers | 44 | |

"What you did" items (also used on the day-3 sheet; 16, max 40):

| Step | Key | EN |
|---|---|---|
| first talk | `firstWeek_didFirstTalk` | Had your first talk with {orcaName} |
| `talk` | `firstWeek_didTalk` | Followed up with {orcaName} |
| `talk` (first talk skipped) | reuse `firstWeek_didFirstTalk` | Had your first talk with {orcaName} |
| `prep` | `firstWeek_didPrep` | Got ready for your session |
| `after` | `firstWeek_didAfter` | Saved notes after your session |
| `note` | `firstWeek_didNote` | Left a voice note |
| `checkin` | `firstWeek_didCheckIn` | Did a quick check-in |
| `talk2` | `firstWeek_didTalk2` | Had a short talk with {orcaName} |

### 10.2 Rhythm

| Key | EN | Max | Notes |
|---|---|---|---|
| `firstWeekRecap_rhythmHeading` | Your rhythm from here | 30 | |
| `firstWeekRecap_rhythmHint` | Based on your week. Keep what fits, and change it any time. | 80 | Full week |
| `firstWeekRecap_rhythmHintQuiet` | Only if it helps. You can change this any time. | 80 | Quiet week: one suggestion, off by default |
| `firstWeekRecap_optBeforeAfter` | Before and after each session | 34 | A; on by default |
| `firstWeekRecap_optBeforeAfterLimit` | On Free: {limit} of each a month. Your agenda is always free. | 80 | `{limit}` = Before therapy limit. Use only while the Before and After limits are equal (both 1 today). |
| `firstWeekRecap_optBeforeAfterLimitSplit` | On Free: {prepLimit} Before therapy and {afterLimit} After therapy a month. Your agenda is always free. | 100 | Fallback if the two limits ever differ |
| `firstWeekRecap_optCheckIn` | Quick check-in on Mondays | 34 | All variants; on by default |
| `firstWeekRecap_optCheckInLimit` | Always free | 80 | |
| `firstWeekRecap_optTalk` | A talk with {orcaName} on Wednesdays | 34 | A: off by default; B and C: on |
| `firstWeekRecap_optTalkLimit` | Writing is free, up to {limit} messages a month | 80 | `reflect_messages` limit (15 today; if it can ever be 1, convert to an ICU plural) |
| `firstWeekRecap_optNote` | A voice note on Fridays | 34 | B and C; off by default |
| `firstWeekRecap_optNoteLimit` | On Free: {limit} a month | 80 | `between_sessions` limit |
| `firstWeekRecap_reminderTime` | Reminders at {time} | 24 | A11y: reuse `firstWeek_reminderTimeA11y` |
| `firstWeekRecap_keep` | Keep this rhythm | 24 | Primary |
| `firstWeekRecap_keepNone` | Done | 24 | Primary label when every option is off |
| `firstWeekRecap_ownWay` | I'll find my own way | 24 | Secondary; same effect as "Hide this plan" |
| `firstWeekRecap_savedSnackbar` | Rhythm saved. | 30 | |
| `firstWeekRecap_ownWaySnackbar` | Okay. {orcaName} is here whenever you want to talk. | 60 | |
| `firstWeekRhythm_title` | Your rhythm | 24 | Screen opened from "Change my rhythm" (same list, same limit lines) |
| `firstWeekRhythm_save` | Save my rhythm | 24 | |

Limit lines show only while the account is on Free. Hide them for Premium and an active starter pack.

## 11. Push allowlist (H-4): lock-screen text for every push type

Applies to every generator and every account, not only week 1 (SPEC 5, lead note 13). The model never writes `push_title` or `push_body`; AI copy stays in-app. Store the template key in `notification_logs`, never the text. Plan-step pushes route to `/home` with no `moment_type` and no step.

Ban list, checked on every line below: therapy, session, therapist, appointment, symptom, mood, feel or feeling, focus area, emotion, stress, anxiety, any crisis word, any name (the companion's name included), any quote or paraphrase of what the person said. Title max 40, body max 60.

| Push type | Status in code | Template key | Title | Body |
|---|---|---|---|---|
| New plan-step type, step `talk` | new (SPEC 5) | `plan_step_talk` | Your step for today is ready | About 3 minutes, whenever it suits you. |
| New plan-step type, step `talk2` and rhythm talk | new | `plan_step_talk2` | Today's step is ready | A few minutes, whenever you have them. |
| New plan-step type, step `note` and rhythm note | new | `plan_step_note` | A 1-minute step is ready | Open MindSync when you have a moment. |
| New plan-step type, step `checkin` and rhythm check-in | new | `plan_step_checkin` | 30 seconds for you | A quick check-in is ready. |
| New plan-step type, step `recap` | new | `plan_step_recap` | Your first week is ready to look back on | Two minutes, whenever you like. |
| `THERAPY_PREP` (day before, at the chosen time) | live generator | `therapy_prep` | A 2-minute step for tomorrow | Any time today works. |
| `THERAPY_PREP` (T-3h variant, session on plan day 1) | live generator | `therapy_prep_same_day` | A 2-minute step for today | Best done in the next few hours. |
| `POST_SESSION_REFLECTION` | live generator | `post_session_reflection` | A 2-minute step is ready | Best done while it's fresh. |
| `THERAPY_APPOINTMENT` | live generator | `therapy_appointment` | A reminder you set for today | Open MindSync for the details. |
| `RECORD_SESSION` | live generator | `record_session` | Your reminder for now | Open MindSync when you're ready to start. |
| `ADD_THERAPY_DATE` | live generator (muted under 8 days) | `add_therapy_date` | Add a date in MindSync | It takes a few seconds. |
| `BETWEEN_SESSIONS_NOTE` | live generator | `between_sessions_note` | One minute for a quick note | Say or type whatever is on your mind. |
| `HOMEWORK_REMINDER` | live generator | `homework_reminder` | A to-do is waiting | Open MindSync to see it. |
| `GOALS_WEEKLY` | live hook (`moment_hooks.py:189`, muted under 8 days) | `goals_weekly` | Your weekly update is ready | Take a look when you have a minute. |
| `WEEKLY_SUMMARY_READY` | live hook (`moment_hooks.py:250`) | `weekly_summary_ready` | Your week in MindSync | A short summary is ready to read. |
| `MONTHLY_SUMMARY_READY` | live hook (`moment_hooks.py:313`, today sends "monthly therapy audit") | `monthly_summary_ready` | Your month in MindSync | A summary is ready for when you have a few minutes. |
| `ACCOUNT_SETUP_NUDGE` | live generator (muted under 8 days) | `account_setup_nudge` | Finish setting up MindSync | It takes about a minute. |
| `MOOD_UPDATE_REQUEST` | live generator (muted under 8 days) | `mood_update_request` | Got 30 seconds? | A quick check-in is ready in MindSync. |
| `THERAPY_RELATIONSHIP_CHECKIN` | live generator (muted under 8 days) | `therapy_relationship_checkin` | A short question for you | Two minutes, whenever it suits you. |
| `MOOD_DIP_ALERT` | live generator (in-app only under 8 days) | `mood_dip_alert` | A moment for you | Open MindSync when you have a minute. |
| `REFLECTION_INVITATION` | live generator (muted under 8 days) | `reflection_invitation` | A few minutes for you | Write a few lines in Reflect, if you like. |
| `RE_ENGAGEMENT` | live generator (muted under 8 days) | `re_engagement` | Whenever you're ready | Everything you saved is right where you left it. |
| `WEEKLY_RECAP` | enum only, no producer found | `weekly_recap` | Your week, in short | Open MindSync for a quick look back. |
| `ACHIEVEMENT_UNLOCK` | enum only, no producer found | `achievement_unlock` | A small milestone | It's waiting for you in MindSync. |
| `STREAK_CELEBRATION` | retired (enum comment) | `generic` | Something new in MindSync | Open the app when you have a moment. |
| `PATTERN_INSIGHT` | retired | `generic` | Something new in MindSync | Open the app when you have a moment. |
| `DAILY_CHECK_IN` | retired | `generic` | Something new in MindSync | Open the app when you have a moment. |
| `SESSION_MORNING_OF` | retired | `generic` | Something new in MindSync | Open the app when you have a moment. |
| Any type missing from this table | default | `generic` | Something new in MindSync | Open the app when you have a moment. |

Pushes outside `MomentTypeEnum`:

| Sender | Status in code | Template key | Title | Body |
|---|---|---|---|---|
| `notify_summary_notification` (Daily, Weekly, Monthly, Yearly; `notification_service.py:312`, called from `periodic_summary.py`) | callers not registered in `rq_scheduler_setup.py` today | `summary_ready` | Your summary is ready | Open MindSync to read it. |
| Session recording summary ready (`tasks/session_recording.py:220`) | live | `recording_summary_ready` | Your notes are ready | They're in MindSync whenever you want them. |
| Post-session nudge, first (`notification_service.py:683`) | not registered in the scheduler today | `post_session_nudge` | Two minutes, if you have them | Best done while it's fresh. |
| Post-session nudge, follow-up (`notification_service.py:766`) | not registered today | `post_session_nudge_followup` | A short step is still open | A few words are enough, whenever you're ready. |
| `health_check_reminder` text (`notification_texts.py:37`) | no caller outside tests | reuse `therapy_relationship_checkin` | A short question for you | Two minutes, whenever it suits you. |
| `symptom_tracking_reminder` text (`notification_texts.py:71`) | no caller outside tests | reuse `mood_update_request` | Got 30 seconds? | A quick check-in is ready in MindSync. |
| `reflection_invitation_session_today` text (`notification_texts.py:405`) | REFLECTION_INVITATION variant | reuse `reflection_invitation` | A few minutes for you | Write a few lines in Reflect, if you like. |
| `daily_check_in_*` texts (`notification_texts.py:208-297`) | retired with DAILY_CHECK_IN | reuse `generic` | Something new in MindSync | Open the app when you have a moment. |
| `/admin/broadcast` | operator-written | none | | The operator writes these by hand; the same ban list applies. |

## 12. WP-0 replacements (can ship before the feature)

### 12.1 Push pre-prompt examples (`app_en.arb:2220-2241`, L-1)

The examples must show the real lock-screen text from section 11. Update all 7 locales.

| Key | Current EN | New EN | Notes |
|---|---|---|---|
| `push_examplePrepTitle` | Your session is tomorrow | A 2-minute step for tomorrow | = `therapy_prep` |
| `push_examplePrepBody` | Take a few minutes to pick what you want to bring up. | Any time today works. | |
| `push_examplePostTitle` | How did your session go? | A 2-minute step is ready | = `post_session_reflection` |
| `push_examplePostBody` | Note one thing in After therapy while it's fresh. | Best done while it's fresh. | |
| `push_exampleCheckInTitle` | Quick check-in | Got 30 seconds? | = `mood_update_request` |
| `push_exampleCheckInBody` | Check in on {focusAreas} today. It takes a minute. | A quick check-in is ready in MindSync. | Drop the `{focusAreas}` placeholder and its `@` metadata; update the call site |
| `push_exampleReflectTitle` | {orcaName} has a question for you | A few minutes for you | = `reflection_invitation`. Drop the `{orcaName}` placeholder (no names on the lock screen); update the call site |
| `push_exampleReflectBody` | Open Reflect when you have five minutes. | Write a few lines in Reflect, if you like. | |
| `push_examplesPrivacyNote` (new) | | Reminders never show what you said or wrote. | Optional line under the examples. Ship only together with the live allowlist. |

`push_title`, `push_subtitle`, `push_titleNoTherapy` and `push_subtitleNoTherapy` are in-app and can stay.

### 12.2 Android notification channels (`mindsync_app/lib/main.dart:885-899`, L-2)

Keep the channel IDs. Re-creating a channel with the same ID updates its name and description.

| Channel ID | Field | Current | New |
|---|---|---|---|
| `high_importance_channel` | name | High Importance Notifications | General |
| `high_importance_channel` | description | General notifications from MindSync | Updates from MindSync |
| `session_reminders` | name | Session Reminders | Reminders |
| `session_reminders` | description | Reminders to capture your therapy sessions | Reminders you set up in MindSync |

### 12.3 First-conversation recap lines (`app_en.arb:3026-3029`, chosen in `offer_step_view.dart:600-608`)

The first conversation is a Reflect thread, and `GET /reflect` lists every Reflect thread with no origin filter (`crud.py:1917-1935`), so "Saved in Reflect" is true. The Timeline does not show it.

| Key | Current EN | New EN | Notes |
|---|---|---|---|
| `postOnboarding_savedBeforeTherapyDay` | Saved to your Timeline. Your Before therapy card for {weekday} starts from this. | Saved in Reflect. Your Before therapy card for {weekday} starts from this. | The card promise is backed by `saved_line_kind` |
| `postOnboarding_savedBeforeTherapy` | Saved to your Timeline. Your next Before therapy card starts from this. | Saved in Reflect. Your next Before therapy card starts from this. | |
| `postOnboarding_savedCheckIn` | Saved to your Timeline. {orcaName} will check in on this later in the week. | Saved in Reflect. You can come back to it any time. | WP-0 version: promises nothing that does not exist yet |
| `postOnboarding_savedFollowUp` (new, WP-3) | | Saved in Reflect. After some sleep, {orcaName} will have a question for you. | Use instead of `savedCheckIn` only after WP-3 ships, and only for accounts with a first-week anchor (not reruns, not existing accounts). "After some sleep" stays true for evening and late-night onboarding alike. |

Also: the docstring at `MindSync/app/tasks/first_conversation_prep_card.py:6` quotes the old line (comment only), and `test/screens/wow/offer_step_view_test.dart:138, 155, 176, 193` assert the old strings (qa-testing updates them).

### 12.4 Legacy Home strings with dashes (WP-0 item 5, outside first-week mode)

The shipped strings join two phrases with an em dash. The "Current EN" column writes that character as [em dash], so this file stays dash-free.

| Key | Current EN | New EN |
|---|---|---|
| `mainTab_heroSubtitleNoSession` (`app_en.arb:687`) | No session this week [em dash] catch your thoughts | No session this week. Note what's on your mind. |
| `mainTab_heroSubtitleSessionSoon` (`app_en.arb:685`) | Therapy session soon [em dash] ready? | Your session is coming up. Ready? |
| `mainTab_checkinCtaNever` (`app_en.arb:697`) | No check-in yet [em dash] tap to start | No check-in yet. Tap to start. |

## 13. Copy decisions taken in this file (for the lead and the operator)

1. The `talk` Today card says "{orcaName} has a question for you", not "A question from your first talk". The plan endpoint does not tell the client whether the question is quoted, and the generic question (SPEC 13.4) is not from the first talk, so the old line would be false for part of the cohort.
2. The session sheet opened from "It didn't happen" asks "What happened with today's session?" with "It moved", "It didn't happen this time" and "It happened after all", instead of re-asking "Did your session happen today?" right after the person said it didn't.
3. SPEC 3.8 does not define `note` at quota. Free alternative here: Quick check-in, the same for B and C (one route, M-1).
4. The day-3 offer has its own wording around the same starter SKU and price. Not reused from the post-onboarding screen: "Extend your trial to 2 weeks" is inaccurate on day 3 (the pack runs 14 days from purchase), and `postOnboarding_offerStarterBody` (`app_en.arb:2186`) says "Most of our users feel like they got a second therapy session in that time", which compares the app with therapy (YMYL) and hardcodes "five dollars" while the CTA uses `{price}`. Recommendation: remove that sentence from the post-onboarding screen too.
5. In gentle tone the day-3 sheet still shows the offer when eligible (H-1 requires `trial_sheet_eligible` to ignore tone). The gentle top line takes the pressure off: "You don't need to decide anything today." Operator to confirm this is acceptable.
6. Quota bodies carry no number; the "0 of {limit} left until {resetDate}" line does. This keeps them right for any limit and avoids plural problems in 7 locales.
7. "See Premium" on the quota line is hidden in gentle tone. It is a user-initiated element, which H-1 allows to differ; security-guardian to confirm.
8. "Not right" on the recap hard-deletes the memory item. Show `firstWeekRecap_undo` only if the client waits a few seconds before calling DELETE; otherwise no Undo.
9. Dropped from "Orca noticed": "This is also in your weekly summary in Timeline." Not verified, and the first calendar-week summary is suppressed for accounts younger than 8 days.
10. Mirror A: the app has no feature called "session notes", so the CTA is "Add to my agenda" (Workspace, next-session agenda). Privacy line per L-7: "Only you see this, unless you share it or connect a therapist in MindSync." Connected therapists can read check-in scores (clinician portal), so the line stays conditional.
11. Rhythm limit lines appear only on Free; hidden for Premium and an active starter.
12. Generic follow-up question: the operator's example "How have the last few days been?" is kept. It works for skipped first talks, for day 1 or day 2, and quotes nothing. Superseded 2026-10-11: the generic case now asks "How are you doing right now?", the same fixed string as the calm case (API_CONTRACT 14.2 item 9; section 14.5).
13. `trialReminder_freeLimits` (`app_en.arb:2932`) hardcodes 1, 1, 3, 15 and 2. Replace with `trialDay3_freeLimitsAll` and real values.
14. Helpline: the app's calm screen uses findahelpline.com ("Find a helpline near you"); reused here for consistency. The Instagram standard names 988 for the US; a US-specific "Call or text 988" line is an operator decision.
15. `app_en.arb` has 55 lines with an em or en dash. Section 12.4 fixes the three on Home; a full ARB sweep is a separate task.
16. "Waiting" is read here as "today's step exists but is not ready yet" (for example the recap is still being built). The canvas used "waiting" for the deferred state; that one is "Okay, it'll wait" in 2.3.

## 14. Additions after the UX review, 2026-10-11

Sources: `audit-ux-build-2026-10-11.md` (M-1, M-3, M-4, M-6, m-7, m-11, m-13, p-4) and `API_CONTRACT.md` 14.1 item 5 and 14.2 items 8 to 11.

Key names in this section are the **ARB names**. The ARB folds the COPY prefixes into `firstWeek_`: COPY `firstWeekSession_x` is ARB `firstWeek_sessionX`, `firstWeekMirror_x` is `firstWeek_mirrorX`, `firstWeekCheckIn_x` is `firstWeek_checkInX`, `firstWeekFollowUp_x` is `firstWeek_followUpX`. The COPY alias is given in brackets where a section above refers to it.

"Chars" is the visible length of the EN string: `{orcaName}` counted as "Orca" (rule 3), other placeholders counted as written. Rules 1 to 7 of section 0 apply. Translations use the house register: second person, informal (du, tú, tu, du, ty, du), no gendered forms; Polish keeps the app's capital "Twój/Twoich".

### 14.0 Where things live in the build (checked 2026-10-11)

| Name in copy | Real path in the app | ARB labels |
|---|---|---|
| Therapy Schedule | Menu, My Therapy, Therapy Schedule (`my_therapy_screen.dart`). The Settings screen has no schedule section; `settings_therapyScheduleSection` is in the ARB but no screen renders it. | `myTherapy_title`, `myTherapy_scheduleSectionTitle` |
| Privacy & Data, toggle "Use therapy treatment data" | Menu, Account (the top row with the person's name; screen title "Account"), Privacy & Data (`account_body.dart:200`). Not in Settings. | `account_title`, `settings_privacyDataSection`, `settings_useTherapyDataToggle` |
| What {orcaName} remembers | Settings (as written in section 8, correct) | `settings_orcaMemory` |

So the audit's "Settings, under Therapy Schedule" and "Settings, Privacy & Data" are corrected below, and `firstWeekSession_notSureBody` (section 6) is revised in 14.3.

Localized labels used in the strings below: My Therapy = Meine Therapie / Mi terapia / Ma thérapie / Min terapi / Moja terapia / Min terapi. Therapy Schedule = Therapieplan / Horario de terapia / Planning de thérapie / Terapiplan / Harmonogram terapii / Terapischema. Account = Konto / Cuenta / Compte / Konto / Konto / Konto. Privacy & Data = Datenschutz & Daten / Privacidad y Datos / Confidentialité & Données / Personvern og data / Prywatność i dane / Integritet & Data. The French ARB spells `myTherapy_title` "Ma therapie" and the section "Planning de therapie" without accents; the strings here use the correct accents, and the French labels should be fixed to match (14.9).

### 14.1 Art. 9 consent step in context (M-4, p-4)

**Where it shows.** Every place where a therapy-schedule write can come back as `403 art9_consent_required`: the session sheet ("Update my plan"), the C side card "Add sessions" before `SessionSetupScreen` (API_CONTRACT 14.2 item 10), and the schedule editors that write through `SettingsCubit` (My Therapy, Home's session setup). One text in all of them, both tones, same widget keys (H-1).

**What changes.** Onboarding keeps its own title, body and checkbox ("Personalise to your therapy"). Here the step says what is stored (the dates and times of sessions, plus the in-therapy status the server now sets on a consented schedule write, API_CONTRACT 14.1 item 5) and why. It promises nothing beyond what the product does: no "only", and no purpose we have not verified.

**Order on screen** (flutter-mobile: props on `Art9ConsentStep` for lead, title, body, note, checkbox, helper and the two labels):

1. lead, 2. title (header semantics), 3. body, 4. withdraw note, 5. checkbox, 6. helper (only while unticked), 7. primary button, 8. secondary button.

The withdraw note goes above the checkbox on purpose: GDPR Art. 7(3) says the person is told about withdrawal before giving consent.

| ARB key (COPY alias) | EN | Chars | Max | Notes |
|---|---|---|---|---|
| `firstWeek_sessionConsentLead` (`firstWeekSession_consentLead`) | To save session times, MindSync needs your permission first. | 60 | 80 | 16 sp, `SubStyle.ink`, above the title. Connects the step to the action the person just took. |
| `firstWeek_sessionConsentTitle` (`firstWeekSession_consentTitle`) | Session times are health information | 36 | 44 | Replaces `onboarding_art9ConsentTitle` here. 24 sp bold, 2 lines. States the reason for asking, does not repeat the lead. |
| `firstWeek_sessionConsentBody` (`firstWeekSession_consentBody`) | If you allow it, MindSync saves the dates and times of your sessions and notes that you're in therapy. That way your plan and reminders can fit around them. | 156 | 170 | Replaces `onboarding_art9ConsentBody` here. "notes that you're in therapy" = the status set on a consented write (14.1 item 5). |
| `firstWeek_sessionConsentWithdrawNote` (`firstWeekSession_consentWithdrawNote`) | You can change your mind any time in Account, under Privacy & Data. | 67 | 90 | 14 sp. Real path, see 14.0 (not Settings). |
| `firstWeek_sessionConsentCheckbox` (`firstWeekSession_consentCheckbox`) | Yes, MindSync may save and use my session times and therapy status | 66 | 80 | Context-specific, replaces `onboarding_art9ConsentCheckbox` here (that one names neither session times nor storage). No final period, as in onboarding. Also the checkbox's a11y label. |
| `firstWeek_sessionConsentHelper` (`firstWeekSession_consentHelper`) | Check the box to continue. | 26 | 40 | p-4. 14 sp, under the checkbox, only while it is unticked. US "check", not "tick". |
| `firstWeek_sessionConsentAllow` (`firstWeekSession_consentAllow`) | Allow and continue | 18 | 24 | Primary, disabled until ticked. Replaces `onboarding_continue` here. |
| `firstWeek_sessionConsentNotNow` (`firstWeekSession_consentNotNow`) | Not now | 7 | 16 | Secondary text button. Replaces `common_cancel` here. Writes nothing; in the editors it also rolls back the optimistic cache (API_CONTRACT 7.1). |
| `firstWeek_sessionConsentDeclinedToast` (`firstWeekSession_consentDeclinedToast`) | Okay, nothing was saved. | 24 | 40 | `MsMessage.showInfo` after "Not now", in every context (the editors show nothing on decline today). The side card stays. |

Unchanged: `onboarding_art9ConsentRequired` ("Consent could not be saved. Please try again.") stays the error when the consent request fails.

Translations:

| ARB key | de | es | fr |
|---|---|---|---|
| `firstWeek_sessionConsentLead` | Um Sitzungstermine zu speichern, braucht MindSync zuerst deine Erlaubnis. | Para guardar los horarios de tus sesiones, MindSync necesita antes tu permiso. | Pour enregistrer les horaires de tes séances, MindSync a d'abord besoin de ton accord. |
| `firstWeek_sessionConsentTitle` | Sitzungstermine sind Gesundheitsdaten | Los horarios de sesión son datos de salud | Les horaires de séance sont des données de santé |
| `firstWeek_sessionConsentBody` | Wenn du es erlaubst, speichert MindSync Datum und Uhrzeit deiner Sitzungen und vermerkt, dass du in Therapie bist. So können sich dein Plan und deine Erinnerungen danach richten. | Si lo permites, MindSync guarda la fecha y la hora de tus sesiones y anota que estás en terapia. Así tu plan y tus recordatorios pueden adaptarse a ellas. | Si tu l'autorises, MindSync enregistre la date et l'heure de tes séances et note que tu suis une thérapie. Ton plan et tes rappels peuvent ainsi s'organiser autour d'elles. |
| `firstWeek_sessionConsentWithdrawNote` | Du kannst es dir jederzeit anders überlegen, unter Konto im Bereich Datenschutz & Daten. | Puedes cambiar de opinión cuando quieras en Cuenta, en Privacidad y Datos. | Tu peux changer d'avis à tout moment dans Compte, sous Confidentialité & Données. |
| `firstWeek_sessionConsentCheckbox` | Ja, MindSync darf meine Sitzungstermine und meinen Therapiestatus speichern und nutzen | Sí, MindSync puede guardar y usar los horarios de mis sesiones y mi estado terapéutico | Oui, MindSync peut enregistrer et utiliser les horaires de mes séances et mon statut thérapeutique |
| `firstWeek_sessionConsentHelper` | Setz ein Häkchen, um fortzufahren. | Marca la casilla para continuar. | Coche la case pour continuer. |
| `firstWeek_sessionConsentAllow` | Erlauben und weiter | Permitir y continuar | Autoriser et continuer |
| `firstWeek_sessionConsentNotNow` | Jetzt nicht | Ahora no | Pas maintenant |
| `firstWeek_sessionConsentDeclinedToast` | Okay, es wurde nichts gespeichert. | De acuerdo, no se guardó nada. | D'accord, rien n'a été enregistré. |

| ARB key | nb | pl | sv |
|---|---|---|---|
| `firstWeek_sessionConsentLead` | For å lagre tidspunktene for timene dine trenger MindSync tillatelsen din først. | Żeby zapisać terminy sesji, MindSync potrzebuje najpierw Twojej zgody. | För att spara sessionstider behöver MindSync ditt tillstånd först. |
| `firstWeek_sessionConsentTitle` | Timene dine er helseopplysninger | Terminy sesji to dane dotyczące zdrowia | Sessionstider är hälsouppgifter |
| `firstWeek_sessionConsentBody` | Hvis du tillater det, lagrer MindSync dato og klokkeslett for timene dine og noterer at du går i terapi. Da kan planen og påminnelsene dine tilpasses timene. | Jeśli się zgodzisz, MindSync zapisze daty i godziny Twoich sesji oraz zanotuje, że jesteś w terapii. Dzięki temu plan i przypomnienia dopasują się do Twoich sesji. | Om du tillåter det sparar MindSync datum och tid för dina sessioner och noterar att du går i terapi. Då kan din plan och dina påminnelser anpassas efter dem. |
| `firstWeek_sessionConsentWithdrawNote` | Du kan ombestemme deg når som helst under Konto, Personvern og data. | Możesz zmienić zdanie w każdej chwili w Koncie, w sekcji Prywatność i dane. | Du kan ändra dig när som helst under Konto, Integritet & Data. |
| `firstWeek_sessionConsentCheckbox` | Ja, MindSync får lagre og bruke tidspunktene for timene mine og terapistatusen min | Tak, MindSync może zapisywać i wykorzystywać terminy moich sesji oraz mój status terapeutyczny | Ja, MindSync får spara och använda mina sessionstider och min terapistatus |
| `firstWeek_sessionConsentHelper` | Kryss av i boksen for å fortsette. | Zaznacz pole, aby kontynuować. | Kryssa i rutan för att fortsätta. |
| `firstWeek_sessionConsentAllow` | Tillat og fortsett | Zezwól i kontynuuj | Tillåt och fortsätt |
| `firstWeek_sessionConsentNotNow` | Ikke nå | Nie teraz | Inte nu |
| `firstWeek_sessionConsentDeclinedToast` | Greit, ingenting ble lagret. | Dobrze, nic nie zostało zapisane. | Okej, inget sparades. |

Terminology follows the shipped first-week strings: Sitzung (de), sesión (es), séance (fr), time (nb, "appointment"), sesja (pl), session (sv); "estado terapéutico", "statut thérapeutique", "terapistatus", "status terapeutyczny" as in the Settings consent toggle.

### 14.2 Session sheet: "It didn't happen" with no Reflect messages left (M-1)

| ARB key (COPY alias) | EN | Chars | Max | Notes |
|---|---|---|---|---|
| `firstWeek_sessionDidntBodyNoTalk` (`firstWeekSession_didntBodyNoTalk`) | Your plan skips this step, and your usual schedule stays as it is. | 66 | 140 | Use instead of `firstWeek_sessionDidntBody` when `reflectMessagesExhausted()` is true (Free and `reflect_messages` left 0); the "Talk with {orcaName}" button is hidden then. Same title (`firstWeek_sessionDidntTitle`) and primary (`premiumWelcome_backHome`). It points nowhere on purpose: no talk, no paywall. |

| ARB key | de | es | fr |
|---|---|---|---|
| `firstWeek_sessionDidntBodyNoTalk` | Dein Plan lässt diesen Schritt aus, und dein üblicher Zeitplan bleibt, wie er ist. | Tu plan se salta este paso y tu horario habitual se queda como está. | Ton plan saute cette étape, et ton planning habituel reste tel quel. |

| ARB key | nb | pl | sv |
|---|---|---|---|
| `firstWeek_sessionDidntBodyNoTalk` | Planen din hopper over dette steget, og den vanlige planen din forblir som den er. | Plan pomija ten krok, a Twój stały harmonogram zostaje bez zmian. | Din plan hoppar över det här steget, och ditt vanliga schema är oförändrat. |

These are the first sentences of the shipped `firstWeek_sessionDidntBody` translations, so both versions read the same.

### 14.3 "Not sure yet" (M-3)

**From "Session moved?" on `prep`.** The server now drops today's `prep` step and that session's `after` step, schedule untouched, then the sheet shows the existing result view. The old body did not fit: it said "this step" (two steps go), "for now" (dropped steps do not come back) and "in Settings" (the schedule is in My Therapy). One revised body now fits both entries that drop steps: this one, and "It didn't happen", then "It moved to another day", then "Not sure yet" (which drops `after`). Same key, new text, all 7 locales change.

**From the side card.** No write, the card stays, a short toast.

| ARB key (COPY alias) | EN | Chars | Max | Notes |
|---|---|---|---|---|
| `firstWeek_sessionNotSureTitle` (unchanged) | Okay, no date for now | 21 | 44 | Fits both entries. |
| `firstWeek_sessionNotSureBody` (`firstWeekSession_notSureBody`), **revised text, same key** | Your plan skips the steps for this session. When you know the new date, add it in My Therapy, under Therapy Schedule. | 117 | 120 | Primary `premiumWelcome_backHome`. `session_sheet_completed` fires once, after the server accepts the drop. |
| `firstWeek_sessionNotSureAddToast` (`firstWeekSession_notSureAddToast`) | Okay, nothing changed. The card stays here for later. | 53 | 60 | `MsMessage.showInfo` after the sheet closes; no write, no dismiss, no event. No therapy words and one string for B and C (the card kind is a therapy proxy). **Probably unused:** under API_CONTRACT 14.2 item 10 the side cards open `SessionSetupScreen`, which has no "Not sure yet". Add the key only if flutter-mobile keeps a no-write exit on that path. |

| ARB key | de | es | fr |
|---|---|---|---|
| `firstWeek_sessionNotSureBody` | Dein Plan lässt die Schritte für diese Sitzung aus. Wenn du den neuen Termin kennst, trag ihn in Meine Therapie unter Therapieplan ein. | Tu plan se salta los pasos de esta sesión. Cuando sepas la nueva fecha, añádela en Mi terapia, en Horario de terapia. | Ton plan saute les étapes de cette séance. Quand tu connaîtras la nouvelle date, ajoute-la dans Ma thérapie, sous Planning de thérapie. |
| `firstWeek_sessionNotSureAddToast` | Okay, es hat sich nichts geändert. Die Karte bleibt für später hier. | De acuerdo, no cambió nada. La tarjeta se queda aquí para más tarde. | D'accord, rien n'a changé. La carte reste ici pour plus tard. |

| ARB key | nb | pl | sv |
|---|---|---|---|
| `firstWeek_sessionNotSureBody` | Planen din hopper over stegene for denne timen. Når du vet den nye datoen, legger du den inn under Min terapi, Terapiplan. | Plan pomija kroki dla tej sesji. Gdy poznasz nowy termin, dodaj go w Mojej terapii, w sekcji Harmonogram terapii. | Din plan hoppar över stegen för den här sessionen. När du vet det nya datumet lägger du till det under Min terapi, Terapischema. |
| `firstWeek_sessionNotSureAddToast` | Greit, ingenting er endret. Kortet blir liggende her til senere. | Dobrze, nic się nie zmieniło. Karta zostaje tu na później. | Okej, inget har ändrats. Kortet ligger kvar här till senare. |

Not written, on purpose: the audit's `notSureMovedBody` and `notSureKeepBody` (the revised body covers both entries, and the no-write fallback is moot now that the server drops the steps), and `addOnceHint` / `addAlwaysHint` (M-5 is settled by API_CONTRACT 14.2 item 10: adding sessions goes through `SessionSetupScreen`).

### 14.4 Undo snackbars (M-6, m-13)

All three use a 5 s snackbar with a deferred commit and the action `firstWeek_undo` ("Undo"). `firstWeek_recapUndo` stays on the recap's "Not right".

| Surface | Message key | EN | Chars | Status |
|---|---|---|---|---|
| "Hide this plan" | `firstWeek_planHiddenSnackbar` | Plan hidden. Its reminders are off too. | 39 | Existing key covers it. No new copy. |
| Recap "I'll find my own way" | `firstWeek_recapOwnWaySnackbar` | Okay. {orcaName} is here whenever you want to talk. | 45 with "Orca" | Existing key covers it. No new copy. |
| Side card close (B and C) | `firstWeek_sideDismissedSnackbar` (new) | Okay, this card won't show again. | 33 (max 40) | New. True as written: dismissal is permanent (`side_card` null for good, API_CONTRACT 4), so "for now" would be false. No therapy words; reads the same for B and C. |

| ARB key | de | es | fr | nb | pl | sv |
|---|---|---|---|---|---|---|
| `firstWeek_sideDismissedSnackbar` | Okay, diese Karte wird nicht mehr angezeigt. | De acuerdo, esta tarjeta no volverá a aparecer. | D'accord, cette carte ne s'affichera plus. | Greit, dette kortet vises ikke igjen. | Dobrze, ta karta już się nie pojawi. | Okej, det här kortet visas inte igen. |

### 14.5 Follow-up question (section 8 aligned with API_CONTRACT 14.2 item 9)

- `firstWeekFollowUp_questionGeneric` (ARB `firstWeek_followUpQuestionGeneric`) is **retired**. Reason: generic and calm now share one fixed question per language, so the stored first message cannot show which case it was (security H-1).
- Both cases use `firstWeekFollowUp_questionCalm` (ARB `firstWeek_followUpQuestionCalm`), "How are you doing right now?". Labels and hints stay per case; "A question for today" plus "Start wherever you like. A few words are enough." still read well with it.
- The server's fixed string per language must equal the shipped ARB values: de "Wie geht es dir gerade?", es "¿Cómo estás ahora mismo?", fr "Comment ça va, là, maintenant ?", nb "Hvordan har du det akkurat nå?", pl "Jak się teraz czujesz?", sv "Hur mår du just nu?".
- flutter-mobile: remove every reader of `firstWeek_followUpQuestionGeneric`, then delete the key from all 7 ARB files. Section 13 decision 12 is superseded.

### 14.6 Other copy the review asks for (m-7, m-11)

| ARB key (COPY alias) | EN | Chars | Max | Notes |
|---|---|---|---|---|
| `firstWeek_mirrorRowA11yTodayOnly` (`firstWeekMirror_rowA11yTodayOnly`) | {area}: {todayScore} today | | | m-7. Mirror row label in gentle tone, when only the Today column shows. |
| `firstWeek_checkInEmptyBody` (`firstWeekCheckIn_emptyBody`) | This check-in is for the focus areas you picked in setup. You can add and rate focus areas any time in Mood & symptom trends. | 125 | 130 | m-11. Under the existing empty title (`stats_noSymptomsTitle`, "No focus areas yet"); a secondary button opens Mood & symptom trends. Changed from the audit's "You can add some in Mood & symptom trends": areas added there do not appear in this check-in (API_CONTRACT 6.1 returns setup areas only), so that line would promise something false. |

| ARB key | de | es | fr |
|---|---|---|---|
| `firstWeek_mirrorRowA11yTodayOnly` | {area}: {todayScore} heute | {area}: {todayScore} hoy | {area} : {todayScore} aujourd'hui |
| `firstWeek_checkInEmptyBody` | Dieser Check-in ist für die Schwerpunkte aus deiner Einrichtung. In Stimmungs- und Symptomverläufe kannst du jederzeit Schwerpunkte hinzufügen und bewerten. | Este check-in es para las áreas de enfoque que elegiste al inicio. Puedes añadir y valorar áreas de enfoque cuando quieras en Tendencias de ánimo y síntomas. | Ce check-in porte sur les axes choisis au départ. Tu peux ajouter et évaluer des axes à tout moment dans Tendances de l'humeur et des symptômes. |

| ARB key | nb | pl | sv |
|---|---|---|---|
| `firstWeek_mirrorRowA11yTodayOnly` | {area}: {todayScore} i dag | {area}: {todayScore} dziś | {area}: {todayScore} i dag |
| `firstWeek_checkInEmptyBody` | Denne innsjekken er for fokusområdene du valgte i oppsettet. Du kan legge til og vurdere fokusområder når som helst i Trender for humør og symptomer. | Ten check-in dotyczy obszarów wybranych na starcie. Obszary możesz dodawać i oceniać w każdej chwili w Trendach nastroju i objawów. | Den här incheckningen gäller fokusområdena du valde vid starten. Du kan lägga till och skatta fokusområden när som helst i Trender för humör och symtom. |

### 14.7 Starter offer strings: proposal, needs lead OK

Context: the post-onboarding offer screen (`offer_step_view.dart:785-899`) shows, top to bottom: card title "Extend your trial to 2 weeks" with the price, the body, the terms tag, the CTA "Extend to 2 weeks for {price}", then the billing line. Since decision B the body ends with "One payment, nothing renews.", so the card says the payment terms twice in a row (body, then tag) and a third time under the button.

Proposal: each fact once per block. The card carries the offer and a short terms tag; the line under the button carries the full billing terms, where a buyer looks before tapping. Only the body changes (and two German fixes, below).

| Key | EN now | EN proposed | Chars |
|---|---|---|---|
| `postOnboarding_offerStarterBody` | Extend your four-day trial to two weeks for {price}. One payment, nothing renews. | 2 weeks of Premium from today instead of 4 days, for {price}. | 61 |
| `postOnboarding_offerStarterTerms` | One-time payment · no renewal | unchanged | 29 |
| `postOnboarding_billingStarter` | One payment of {price}. Premium for 2 weeks from today, then you move to Free. Nothing renews. | unchanged | 94 |

The new body adds what the title does not say ("from today", "instead of 4 days"), keeps `{price}`, and uses digits like the title and CTA (rule 4). True at the moment of the offer: the starter gives 14 days of Premium from the purchase, and this screen shows on day 0 of the 4-day trial.

| Key | de | es | fr | nb | pl | sv |
|---|---|---|---|---|---|---|
| `postOnboarding_offerStarterBody` | 2 Wochen Premium ab heute statt nur 4 Tagen, für {price}. | 2 semanas de Premium desde hoy en lugar de 4 días, por {price}. | 2 semaines de Premium dès aujourd'hui au lieu de 4 jours, pour {price}. | 2 uker med Premium fra i dag i stedet for 4 dager, for {price}. | 2 tygodnie Premium od dziś zamiast 4 dni, za {price}. | 2 veckor med Premium från i dag i stället för 4 dagar, för {price}. |
| `postOnboarding_offerStarterTerms` | **Einmalzahlung · kein Abo** (fix) | unchanged | unchanged | unchanged | unchanged | unchanged |
| `postOnboarding_billingStarter` | **Eine Zahlung von {price}. Premium für 2 Wochen ab heute, danach wechselst du zu Free. Kein Abo.** (fix) | unchanged | unchanged | unchanged | unchanged | unchanged |

German fix, needed even without this proposal: "verlängern" means both "extend" and "renew". The title, body and CTA say "Verlängere / verlängern" (extend) while the tag says "keine Verlängerung" and the billing line "Nichts verlängert sich" (no renewal), so the screen reads "extend your trial, no extension". "Kein Abo" removes the clash.

Review of the six translations flutter-mobile wrote for the current body, if the lead keeps it:

| Locale | Verdict | Fix |
|---|---|---|
| de | Contradiction (above): "Verlängere ... nichts verlängert sich". | Verlängere deine viertägige Testphase für {price} auf zwei Wochen. Eine Zahlung, kein Abo. |
| es | Correct; "no se renueva nada" is a bit stiff. | Amplía tu prueba de cuatro días a dos semanas por {price}. Un solo pago, sin renovación. |
| fr | Ambiguous: "Prolonge ton essai de quatre jours" can read as "extend your trial by four days". | Passe ton essai de quatre jours à deux semaines pour {price}. Un seul paiement, sans renouvellement. |
| nb | Correct, natural. | none |
| pl | Correct, natural. | none |
| sv | Correct, natural. | none |

### 14.8 For the lawyer (and security-guardian) before the store release

The consent text in 14.1 is honest and promises nothing the product does not do, but it is legal text. These need a yes or a fix:

1. **Two texts, one consent.** Onboarding and the schedule contexts now grant the same ARTICLE9_HEALTH record with different wording ("therapy status to personalise" versus "session times and therapy status"). Confirm one record can rest on either text, and that the record stores which text and where it was shown. Today every editor passes `source: 'settings'` (`settings_cubit.dart:226`), even from Home's session setup.
2. **Are the purposes complete?** The body names the plan, reminders and the in-therapy status. If session dates or the in-therapy status also reach the AI provider in prompts, a connected therapist, or summaries, the text must say so. Backend owners confirm the full list of uses first.
3. **Automatic in-therapy status** (API_CONTRACT 14.1 item 5): disclosed in the body and the checkbox. Confirm that inferring and storing it from a schedule write is acceptable.
4. **What withdrawal does.** The withdraw note sends people to Account, Privacy & Data, "Use therapy treatment data". Its confirm dialog says it "will remove your therapy status"; nothing says what happens to stored session times. Confirm whether they are deleted or kept after withdrawal, then update `settings_confirmWithdrawArt9` and `settings_useTherapyDataSubtitle` to name session times. The new copy deliberately says "change your mind" and promises no deletion.
5. **"Health information".** Correct for the EU (data showing someone receives psychotherapy). For US users, state consumer-health-data laws (for example Washington's My Health My Data Act) may require specific consent elements. Confirm the wording is enough for the US market.
6. **German consent text is garbled.** `onboarding_art9ConsentBody` in `app_de.arb` (and the generated `app_localizations_de.dart:6162`) shows mojibake ("DafĂĽr benĂ¶tigen ... ausdrĂĽckliche"). German users see a broken consent text in onboarding. 137 lines of `app_de.arb` have the same encoding damage. Fix before any store release (flutter-mobile).
7. **Register.** Onboarding consent texts in de and fr use formal "Sie"/"vous"; the new texts use "du"/"tu" like the rest of first week. If the lawyer wants formal legal text, both sets should match.
8. **Analytics residual (added 2026-10-11, `audit-security-events-2026-10-11.md`).** `session_sheet_opened`, `session_sheet_dismissed` and `session_sheet_completed` carry no properties, but they fire only for people who move or report on a therapy session with active Art. 9 consent, so their presence in PostHog is a therapy proxy. Confirm this is covered by the consent and the privacy notice.
9. **Firebase Analytics as a recipient.** `AnalyticsEvents.logEvent` forwards every client event to Firebase Analytics in release builds, not only to PostHog. The privacy notice and the processor list must name it.

### 14.9 Notes for flutter-mobile

- New ARB keys (EN plus 6 locales from the tables above): `firstWeek_sessionConsentLead`, `firstWeek_sessionConsentTitle`, `firstWeek_sessionConsentBody`, `firstWeek_sessionConsentWithdrawNote`, `firstWeek_sessionConsentCheckbox`, `firstWeek_sessionConsentHelper`, `firstWeek_sessionConsentAllow`, `firstWeek_sessionConsentNotNow`, `firstWeek_sessionConsentDeclinedToast`, `firstWeek_sessionDidntBodyNoTalk`, `firstWeek_sideDismissedSnackbar`, `firstWeek_mirrorRowA11yTodayOnly`, `firstWeek_checkInEmptyBody`, and, only if the path exists, `firstWeek_sessionNotSureAddToast`.
- Changed text: `firstWeek_sessionNotSureBody` (all 7 locales).
- Retire: `firstWeek_followUpQuestionGeneric`.
- Placeholders: `firstWeek_mirrorRowA11yTodayOnly` takes `{area}` (String) and `{todayScore}` (int), like `firstWeek_mirrorRowA11y`. No other new key has a placeholder.
- The consent keys are also used outside first week (My Therapy editor). The `firstWeek_` prefix follows this brief; rename to a neutral prefix later if you prefer, the text stays.
- French labels: fix `myTherapy_title` ("Ma thérapie"), `myTherapy_scheduleSectionTitle` and `settings_therapyScheduleSection` ("Planning de thérapie") so the strings in 14.3 match the screen.
- The drawer's top row shows the person's name, not "Account" (it falls back to "Account" when there is no name). The withdraw note says "Account" because that is the screen title; ui-ux-designer may want a visible "Account" label on that row.
- Zero U+2014 and zero U+2013 in every string of this section (mechanical scan done on this file).

### 14.10 Lead decisions on section 14 (2026-10-11)

- 14.7 is approved: the shorter starter body, the German terms and billing fix ("Einmalzahlung · kein Abo", "Kein Abo.") and the French body fix ship in this build.
- `firstWeek_sessionNotSureAddToast` is not added: the side cards open `SessionSetupScreen` (API_CONTRACT 14.2 item 10), which has no "Not sure yet".
- The German ARB mojibake (pre-existing on `dev`, about 106 lines) is repaired in this build.
- 14.5, French: the fixed follow-up question is now "Comment ça va en ce moment ?" on the server (`follow_up.py`) and in the ARB (`firstWeek_followUpQuestionCalm`), per the translation review of 2026-10-11.
- Push titles for `plan_step_recap` in de, fr, es, nb, sv and pl are the shorter strings from `review-translations-2026-10-11.md` section 3.
