# Final English copy: subscription + onboarding redesign (2026-10-02)

Owner: brand-voice-manager. Status: approved for implementation, post-humanizer.
This file wins over any text inside the HTML mockups (SPEC.md, header).

How to read it:

- One section per screen, in flow order. `key` is the proposed arb key. "existing key" in the note means the key is already in `app_en.arb` and only its English text changes (other locales need a fresh translation). "unchanged" means keep the live string as it is.
- Placeholders are ICU and arb-ready. Plurals are written in full ICU form.
- "VERBATIM" marks operator-mandated text. Do not edit it, not even punctuation.
- Weekday names, weekday letters, dates and times come from `intl` (`DateFormat`) in the device locale, never from arb strings. `{time}` is already formatted (12 h or 24 h per device), `{date}` is a medium date such as "Nov 1".
- Prices (`{price}`, `{annualPrice}`, `{monthlyPrice}`) are the store's localized price strings, never hard-coded.
- No em dash and no en dash anywhere, including number ranges (use a plain hyphen: "18-24").
- Style: sentence case everywhere, US spelling, "MindSync" and "the app", straight apostrophes.

## OB01Welcome

| key | text | note |
|---|---|---|
| welcome_title | Get more out of every therapy session. | |
| welcome_subtitle | Prepare before, capture after, and see how things change between sessions. | |
| welcome_getStarted | Get started | |
| welcome_haveAccount | I already have an account | |
| welcome_terms | Terms of Service | |
| welcome_privacy | Privacy Policy | |

## OB02Account

| key | text | note |
|---|---|---|
| auth_createAccountTitle | Create your account | |
| auth_createAccountSubtitle | A few questions next, then the app is set up for you. | LEAD DECISION: no privacy claim on this screen (not verified against AI processing and sharing). |
| auth_continueWithApple | Continue with Apple | unchanged, existing key |
| auth_continueWithGoogle | Continue with Google | unchanged, existing key |
| auth_orWithEmail | or with email | |
| auth_email | Email | unchanged, existing key |
| auth_passwordLabel | Password (6+ characters) | |
| auth_termsConfirmation | I confirm I'm of legal age and agree to the | existing key, text tidied, hard line break removed. Followed by the link below. Keeps the live legal meaning; see open question about 16 vs 18. |
| auth_termsOfServiceLink | Terms of Service | unchanged, existing key |
| auth_createAccountButton | Create account | |
| auth_haveAccountPrompt | Have an account? | |
| auth_logIn | Log in | unchanged, existing key |

## OB03Personalise

| key | text | note |
|---|---|---|
| auth_whatShouldWeCallYou | What should we call you? | unchanged, existing key |
| auth_nameFieldLabel | Your name or nickname | |
| auth_ageBandLabel | Your age range | unchanged, existing key |
| auth_optionalSuffix | (optional) | Shown after "Your age range". |
| auth_ageBand1824 | 18-24 | existing key, the live text uses an en dash: replace with a hyphen |
| auth_ageBand2534 | 25-34 | existing key, same fix |
| auth_ageBand3544 | 35-44 | existing key, same fix |
| auth_ageBand4554 | 45-54 | existing key, same fix |
| auth_ageBand55plus | 55+ | unchanged, existing key |
| auth_preferNotToSay | Prefer not to say | unchanged, existing key |
| auth_genderOptionalLabel | Gender (optional) | |
| auth_genderPreferNotToSay | Prefer not to say | existing key, new text (live text is "I don't want to tell") |
| auth_genderWoman | Woman | unchanged, existing key |
| auth_genderMan | Man | unchanged, existing key |
| auth_genderNonBinary | Non-binary | unchanged, existing key |
| auth_genderSelfDescribe | Self-describe | unchanged, existing key |
| auth_genderSelfDescribeHint | Describe your gender | unchanged, existing key |
| auth_pronounsOptionalLabel | Pronouns (optional) | |
| auth_pronounsTheyThem | They/Them | unchanged, existing key |
| auth_pronounsSheHer | She/Her | unchanged, existing key |
| auth_pronounsHeHis | He/Him | existing key, fixes "He/His" |
| auth_pronounsOther | Other | unchanged, existing key |
| auth_nameUsageHint | MindSync uses your name and pronouns when it talks to you. You can change them later in Settings. | The orca has no name yet at this step, so the line names MindSync. |
| auth_continue | Continue | |

## OB04Legal

| key | text | note |
|---|---|---|
| onboarding_legalTitle | Hi {name}. A few short questions, then your app is ready. | {name} = name from the previous screen. "A few" because the count is 5 or 7 depending on answers. |
| onboarding_legalTitleNoName | Hi there. A few short questions, then your app is ready. | When the name is empty. |
| onboarding_legalSubtitle | First, two things to read and agree to. | |
| onboarding_disclaimerCardTitle | MindSync is not a medical device | |
| onboarding_disclaimerCardBody | (do not add) | LEAD DECISION: the card body shows the full live `onboarding_disclaimerText` unchanged (legally reviewed). No shortened version. |
| onboarding_disclaimerReadMore | Read more | Opens the full disclaimer (existing `onboarding_disclaimerText`, unchanged). |
| onboarding_gdprConsent | I consent to MindSync processing my wellbeing and reflection data as described in our Privacy Policy | unchanged, existing key. Consent wording stays as reviewed; do not swap in the mockup text. |
| onboarding_ageConfirmation | I confirm I am 16 years of age or older | unchanged, existing key |
| onboarding_languageRow | Language: {language} | {language} = current language name. |
| onboarding_changeLanguage | Change | unchanged, existing key |
| onboarding_agreeAndContinue | Agree and continue | |
| onboarding_consentRequired | Check the boxes to continue | unchanged, existing key |

## OB05Challenges

| key | text | note |
|---|---|---|
| onboarding_progressStep | {current} of {total} | Shared by all steps. Same as existing `onboarding_stepOfTotal`, reuse it if you prefer. |
| onboarding_challengesTitle | What do you want to keep an eye on? | existing key, new text |
| onboarding_challengesSubtitle | Pick at least one. You'll see how each one changes over time. | |
| symptomPresetLowMood etc. | Low mood, Unease, Overwhelm, Worries, Stress, Sleep, Loss, Focus | unchanged. Use the existing `symptomPreset*` labels and values; no new keys. |
| onboarding_addYourOwn | Add your own | unchanged, existing key (the "+" is an icon) |
| onboarding_typeYourChallenge | e.g. tension, motivation | unchanged, existing key |
| onboarding_challengesContinue | {count, plural, =1{Continue with 1 area} other{Continue with {count} areas}} | {count} = areas picked |
| onboarding_challengesPickOne | Pick at least one | Disabled button state. |

## OB06Intensity

| key | text | note |
|---|---|---|
| onboarding_intensityTitle | How strong is each one right now? | existing key, new text |
| onboarding_intensitySubtitle | 1 is barely there, 10 is overwhelming. This is your starting point. | existing key, new text |
| onboarding_intensityLow | Barely there | |
| onboarding_intensityHigh | Overwhelming | |
| onboarding_continue | Continue | unchanged, existing key. Shared primary button for steps 2-6. |

## OB07Journey

| key | text | note |
|---|---|---|
| onboarding_currentlyInTherapyTitle | Are you in therapy right now? | existing key, new text |
| onboarding_inTherapySubtitle | If you are, MindSync helps you prepare before each session and capture what happened after. | |
| onboarding_art9ConsentCheckboxTitle | (do not add) | LEAD DECISION: consent wording stays live. Keep `onboarding_art9ConsentTitle`, `onboarding_art9ConsentBody` as they are; `onboarding_art9ConsentCheckbox` becomes "Yes, use my therapy status to personalise my experience" (only the dash replaced by a comma, in all languages). |
| onboarding_art9ConsentCheckboxBody | (do not add) | See row above. |
| onboarding_art9ConsentRequired | Consent could not be saved. Please try again. | unchanged, existing key |
| onboarding_currentlyInTherapyYesRegular | Yes, regularly | existing key, removes the dash |
| onboarding_currentlyInTherapyYesOccasional | Yes, now and then | existing key, removes the dash |
| onboarding_currentlyInTherapyNotRightNow | Not right now | unchanged, existing key |
| onboarding_currentlyInTherapyNeverBeen | I've never been | existing key, new text |
| onboarding_howLongInTherapy | How long have you been in therapy? | unchanged, existing key. Shown only for the two "Yes" answers. |
| onboarding_justStarted | Just started | unchanged, existing key |
| onboarding_1to6months | 1-6 months | existing key, live text has an en dash: replace with a hyphen |
| onboarding_6to12months | 6-12 months | existing key, same fix |
| onboarding_1plusYears | 1+ years | unchanged, existing key |
| onboarding_3plusYears | 3+ years | unchanged, existing key |
| onboarding_therapyGoalLabel | What do you want from therapy? | Followed by `auth_optionalSuffix`. |
| onboarding_therapyGoalHint | e.g. feel calmer at work | |
| onboarding_crisisNotAlone | You're not alone | unchanged, existing key (crisis banner) |
| onboarding_crisisSupport | If you're struggling, support is available. The 988 Suicide & Crisis Lifeline offers free, confidential help 24/7. | unchanged, existing key |
| onboarding_crisisLink | Visit 988lifeline.org | unchanged, existing key |
| onboarding_skip | Skip | Shared secondary button for steps 3-4. |

## OB08Modality

| key | text | note |
|---|---|---|
| onboarding_modalityTitle | What kind of therapy is it? | existing key, new text |
| onboarding_modalitySubtitle | Pick all that fit. MindSync shapes its questions around them. | existing key, new text. The orca is named later (step 6), so no {orcaName} here. |
| onboarding_cbt | CBT | unchanged, existing key |
| onboarding_cbtDescription | Cognitive Behavioral Therapy | unchanged, existing key |
| onboarding_dbt | DBT | unchanged, existing key |
| onboarding_dbtDescription | Dialectical Behavior Therapy | unchanged, existing key |
| onboarding_emdr | EMDR | unchanged, existing key |
| onboarding_emdrDescription | Working through difficult memories | existing key, new text |
| onboarding_psychodynamic | Psychodynamic | unchanged, existing key |
| onboarding_psychodynamicDescription | How past experiences shape today | existing key, new text |
| onboarding_act | ACT | unchanged, existing key |
| onboarding_actDescription | Acceptance and Commitment Therapy | unchanged, existing key |
| onboarding_somatic | Somatic | unchanged, existing key |
| onboarding_somaticDescription | Body-centered work on stress and tension | existing key, new text (US spelling) |
| onboarding_talkTherapy | Talk therapy | existing key, new text |
| onboarding_talkTherapyDescription | General conversation-based therapy | existing key, new text |
| onboarding_notSure | I'm not sure | unchanged, existing key |
| onboarding_notSureDescription | The app adapts to you | existing key, new text |
| onboarding_other | Other | unchanged, existing key |
| onboarding_otherDescription | Integrative, Gestalt or something else | existing key, new text |
| onboarding_otherHint | Describe your approach (optional) | unchanged, existing key |

## OB09Schedule

| key | text | note |
|---|---|---|
| onboarding_scheduleTitle | When is your next session? | existing key, new text |
| onboarding_scheduleSubtitle | We'll remind you the day before, so you have time to prepare with Before therapy. | existing key, new text. Matches the real T-24h prep reminder; the card itself is not created automatically. |
| onboarding_scheduleTimeLabel | Time | |
| onboarding_scheduleFrequencyLabel | How often | |
| onboarding_frequencyWeekly | Weekly | |
| onboarding_frequencyBiweekly | Every 2 weeks | |
| onboarding_frequencyCustom | Custom | Opens the existing custom calendar. |
| onboarding_scheduleNextSession | Next session: {weekday} at {time}. We'll remind you the day before. | {weekday} = full weekday name, {time} = formatted time |
| onboarding_scheduleNoDate | I don't have a date yet | |

## OB10Companion

| key | text | note |
|---|---|---|
| onboarding_companionTitle | Meet your orca. You talk with it between sessions. | existing key, new text |
| onboarding_nameYourOrca | Give it a name | existing key, new text |
| onboarding_orcaNameHint | e.g. Luna, Wave | existing key, new text |
| onboarding_talkStyleQuestion | How should {orcaName} talk to you? | {orcaName} = typed name |
| onboarding_talkStyleQuestionNoName | How should your orca talk to you? | When the name field is empty. |
| onboarding_theRealist | The Realist | unchanged, existing key |
| onboarding_realistDescription | Straight talk. No sugar coating. | unchanged, existing key |
| onboarding_theCoach | The Coach | unchanged, existing key |
| onboarding_coachDescription | Motivating. Focused on next steps. | existing key, new text |
| onboarding_theFriend | The Friend | unchanged, existing key |
| onboarding_friendDescription | Warm, casual, honest. | existing key, new text |
| onboarding_theSage | The Sage | unchanged, existing key |
| onboarding_sageDescription | Reflective. Sees the bigger picture. | existing key, new text |
| onboarding_theExplorer | The Explorer | unchanged, existing key |
| onboarding_explorerDescription | Curious and a bit playful. | existing key, new text |
| onboarding_sampleLabel | {orcaName} would say | Label above the sample bubble. |
| onboarding_sampleLabelNoName | Your orca would say | |
| onboarding_sampleRealist | Last week was hard. Let's look at what actually happened. | The UI adds the quotation marks. |
| onboarding_sampleCoach | You showed up. What's one thing to try before your next session? | Mockup said "before Thursday"; a fixed weekday reads wrong for most users. |
| onboarding_sampleFriend | That sounds like a heavy week. Want to talk it through? | |
| onboarding_sampleSage | What does this week tell you about what matters to you? | |
| onboarding_sampleExplorer | Interesting. What do you think was going on underneath? | |
| onboarding_chooseColor | Pick a color | unchanged, existing key (color picker stays) |
| onboarding_changeAnytime | You can change this anytime in Settings. | unchanged, existing key |

## OB11Source

| key | text | note |
|---|---|---|
| onboarding_leadSourceTitle | Last one. How did you hear about MindSync? | existing key, new text |
| onboarding_leadSourceSubtitle | It helps us reach more people like you. | existing key, new text |
| onboarding_leadSourceTherapist | My therapist or doctor | existing key, new text. Stored values stay the same. |
| onboarding_leadSourceFriend | A friend | existing key, new text |
| onboarding_leadSourceSocialMedia | Instagram, TikTok or Reddit | existing key, new text |
| onboarding_leadSourceAppStore | App Store or Google Play | existing key, new text |
| onboarding_leadSourceBlog | A blog or website | existing key, new text |
| onboarding_leadSourceOther | Somewhere else | existing key, new text |
| onboarding_leadSourceOtherHint | Tell us more (optional) | unchanged, existing key |
| onboarding_setUpMyApp | Set up my app | |
| onboarding_leadSourceSkip | I'd rather not say | unchanged, existing key |

## PersonalBuild

Approved earlier today. Text is kept; only placeholders and plural forms were added so the strings work in arb.

| key | text | note |
|---|---|---|
| build_title | {orcaName} is setting up your app, {name} | |
| build_titleNoName | {orcaName} is setting up your app | When the user's name is empty. |
| build_subtitle | Based on the answers you just gave. | |
| build_stepAreasTitle | Saving your focus areas | |
| build_stepAreasBody | {count, plural, =1{1 area and how heavy it feels} other{{count} areas and how heavy each one feels}} | |
| build_stepRemindersTitle | Setting reminders for your sessions | In therapy with a saved session. |
| build_stepRemindersBody | Next session {weekday} at {time} | Mockup showed "Sessions on Thursdays at 6:00 PM"; plural weekdays do not localize, so this form is used. |
| build_stepFirstWeekTitle | Planning your first week | Replaces the reminders step when the user is not in therapy or has no session date. |
| build_stepFirstWeekBody | Reflect, Between Sessions and a check-in | |
| build_stepToneTitle | Setting how {orcaName} talks to you | |
| build_stepToneRealist | Talks like a realist | One string per archetype (articles differ). |
| build_stepToneCoach | Talks like a coach | |
| build_stepToneFriend | Talks like a friend | |
| build_stepToneSage | Talks like a sage | |
| build_stepToneExplorer | Talks like an explorer | |
| build_stepFirstReadTitle | Writing {orcaName}'s first read on you | |
| build_stepFirstReadBody | Based only on what you told us | |

## PersonalReveal

Approved earlier today. Text kept; placeholders, plural forms and the not-in-therapy variant added.

| key | text | note |
|---|---|---|
| reveal_eyebrow | Your setup | |
| reveal_title | {name}, your MindSync is ready. | |
| reveal_titleNoName | Your MindSync is ready. | |
| reveal_subtitle | Everything below comes from your answers. | |
| reveal_focusAreasHeading | Your focus areas | |
| reveal_intensityA11y | Intensity {level} of 5 | Screen-reader label for the bars. {level} = 1-5 |
| reveal_focusAreasFootnote | Tracked in Mood & symptom trends, starting today. | |
| reveal_weekHeading | Your week with MindSync | In therapy with a saved session. |
| reveal_firstWeekHeading | Your first week | Not in therapy, or no session date. |
| reveal_planDayBeforeWhen | {weekday}, the day before | {weekday} = day before the session |
| reveal_planDayBeforeWhat | Reminder to prepare with Before therapy | LEAD DECISION: true for every plan (auto-generated cards exist only for trial/premium). |
| reveal_planSessionWhen | {weekday} {time}, your session | |
| reveal_planSessionWhat | Record the session or write After therapy notes | |
| reveal_planCheckInWhen | Between sessions | LEAD DECISION: no fixed check-in days exist, so no day names here; the week strip marks only the session day and the day before. |
| reveal_planCheckInWhat | Quick check-in on {focusAreas} | Extra placeholder: up to two focus area names joined with "and". |
| reveal_firstWeekReflectWhen | Today | |
| reveal_firstWeekReflectWhat | Talk with {orcaName} in Reflect | |
| reveal_firstWeekNoteWhen | Any day | |
| reveal_firstWeekNoteWhat | Leave a short voice note in Between Sessions | |
| reveal_firstReadHeading | {orcaName}'s first read on you | |
| reveal_firstReadLoading | {orcaName} is still writing this. It will show up here in a moment. | Soft loading state. |
| reveal_firstReadFootnote | More accurate with each session you add. Full version in Character. | |
| reveal_firstReadMissing | Your first read will appear in Character. | When the starter bio is not available; or hide the block. |
| reveal_toneHeading | How {orcaName} talks to you | |
| reveal_toneRealist | Like a realist | Description below it = `onboarding_realistDescription` |
| reveal_toneCoach | Like a coach | Description = `onboarding_coachDescription` |
| reveal_toneFriend | Like a friend | Description = `onboarding_friendDescription` |
| reveal_toneSage | Like a sage | Description = `onboarding_sageDescription` |
| reveal_toneExplorer | Like an explorer | Description = `onboarding_explorerDescription` |
| reveal_cta | Let's start | |

## PostOnboarding (offer)

| key | text | note |
|---|---|---|
| postOnboarding_closeA11y | Close and continue with the free trial | Screen-reader label for the X. The trial is already running. |
| postOnboarding_restore | Restore | |
| postOnboarding_profileReady | Your profile is ready | |
| postOnboarding_title | Your first 4 days of Premium are on us. | |
| postOnboarding_subtitle | No card needed. When the 4 days are up, you move to Free unless you pick a plan. | |
| postOnboarding_offerHeading | Want more time with Premium? | |
| postOnboarding_offerStarterTitle | Extend to 2 weeks | |
| postOnboarding_offerStarterBody | Extend your four-day tryout to two weeks, just for five dollars. Most of our users feel like they got a second therapy session in that time. | VERBATIM by operator |
| postOnboarding_offerStarterTerms | One-time payment · no renewal | |
| postOnboarding_planAnnual | Annual | |
| postOnboarding_planAnnualSub | Billed once a year | Replaces "Premium for good", which reads as "forever". |
| postOnboarding_badgeBestValue | Best value | |
| postOnboarding_planMonthly | Monthly | |
| postOnboarding_planMonthlySub | Billed every month | |
| postOnboarding_ctaStarter | Extend to 2 weeks for {price} | {price} = starter price |
| postOnboarding_ctaAnnual | Continue with Annual | Same wording as the paywall. |
| postOnboarding_ctaMonthly | Continue with Monthly | |
| postOnboarding_billingStarter | One payment of {price}. Premium for 2 weeks from today, then you move to Free. Nothing renews. | |
| postOnboarding_billingAnnual | Billed {price} today, then once a year. Cancel anytime in your store settings. | |
| postOnboarding_billingMonthly | Billed {price} today, then every month. Cancel anytime in your store settings. | |
| postOnboarding_skip | Continue with my free 4 days | Was "Start with my free 4 days"; the trial has already started. |
| postOnboarding_terms | Terms of Service | |
| postOnboarding_privacy | Privacy Policy | |

## OB15Push

| key | text | note |
|---|---|---|
| push_title | Want a reminder before your session? | In therapy with a saved session. |
| push_subtitle | We remind you before and after your sessions. You can turn each type off in Settings. | |
| push_titleNoTherapy | Want a reminder to check in? | Not in therapy, or no session date. |
| push_subtitleNoTherapy | A short nudge for check-ins and Reflect. You can turn each type off in Settings. | |
| push_exampleMeta | MindSync · {weekday}, {time} | Timestamp line on each example card. |
| push_examplePrepTitle | Your session is tomorrow | Real moment: THERAPY_PREP, sent 24 h before. |
| push_examplePrepBody | Take a few minutes to pick what you want to bring up. | |
| push_examplePostTitle | How did your session go? | Real moment: POST_SESSION_REFLECTION. |
| push_examplePostBody | Note one thing in After therapy while it's fresh. | |
| push_exampleCheckInTitle | Quick check-in | Not-in-therapy example 1. Real moment: MOOD_UPDATE_REQUEST. |
| push_exampleCheckInBody | How are {focusAreas} today? It takes a minute. | Same {focusAreas} as on the Reveal screen. |
| push_exampleReflectTitle | {orcaName} has a question for you | Not-in-therapy example 2. Real moment: REFLECTION_INVITATION. |
| push_exampleReflectBody | Open Reflect when you have five minutes. | |
| push_turnOn | Turn on reminders | |
| push_notNow | Not now | |

## FlowFirstStep

| key | text | note |
|---|---|---|
| firstStep_trialChip | {days, plural, =1{Premium trial · 1 day left} other{Premium trial · {days} days left}} | |
| onboarding_wowChooseFirstStep | I'd like to start with: | unchanged, existing key |
| onboarding_capturePastSession | Capture a past session | unchanged, existing key. VERBATIM by operator. |
| firstStep_captureSub | After therapy, while it's fresh | |
| firstStep_or | or | |
| firstStep_optionReflect | Talk with {orcaName} about your therapy & wellbeing | VERBATIM by operator |
| firstStep_optionBetweenSessions | Get a summary of how you feel with Between Sessions | VERBATIM by operator |
| firstStep_optionHealthCheck | Check the health of your Therapy Relationship | VERBATIM by operator |
| firstStep_voiceNoteExplainer | Leaving a short voice note will let us analyze what's going on and give you helpful tips on your therapy progress. | VERBATIM by operator. Shown with the dot bullet. |
| onboarding_takeMeToApp | Take me to the app | unchanged, existing key |

## CurHome (trial bar only)

| key | text | note |
|---|---|---|
| home_trialBar | {days, plural, =0{Premium trial: last day} =1{Premium trial: 1 day left} other{Premium trial: {days} days left}} | {days} = whole days left |
| home_trialBarCta | See plans | Opens the paywall, trigger_feature = trial_banner |

## FlowTrialReminder

| key | text | note |
|---|---|---|
| trialReminder_eyebrow | Day 3 of 4 | |
| trialReminder_title | Your Premium trial ends tomorrow | |
| trialReminder_subtitle | Here's what you've used so far. Everything you saved stays saved either way. | |
| trialReminder_statSessions | Before and After therapy | Label under the number. |
| trialReminder_statRecordings | Recordings | |
| trialReminder_statReflect | Reflect messages | |
| trialReminder_freeLimits | From tomorrow on Free: 1 Before therapy, 1 After therapy, 3 Between Sessions and 15 Reflect messages a month, plus 2 session recordings in total. | If the limits ever become config-driven, switch to {limit} placeholders. |
| trialReminder_keepPremium | Keep Premium | Opens the paywall |
| trialReminder_notNow | Not now | |

## Main (paywall)

| key | text | note |
|---|---|---|
| subscription_closeA11y | Close | |
| subscription_restore | Restore | unchanged, existing key |
| subscription_eyebrow | MindSync Premium | |
| subscription_headlineGeneric | Prepare for and capture every session. | Variant: generic |
| subscription_sublineGeneric | Unlimited Before therapy, After therapy, Between Sessions, Reflect and recordings, plus your full monthly therapy summary. | Variant: generic. About 115 characters; the table covers habits. |
| subscription_chipLimitBefore | You've used your free Before therapy this month | Variant: limit. trigger premium_gate for Before therapy |
| subscription_chipLimitAfter | You've used your free After therapy this month | Variant: limit |
| subscription_chipLimitBetween | You've used all {limit} Between Sessions this month | Variant: limit. {limit} = 3 today |
| subscription_chipLimitReflect | You've used your {limit} free Reflect messages this month | Variant: limit. {limit} = 15 today |
| subscription_chipLimitRecordings | You've used your {limit} free session recordings | Variant: limit. Lifetime limit, so no "this month". |
| subscription_chipLimitHabits | {limit, plural, =1{Free includes 1 active habit} other{Free includes {limit} active habits}} | Variant: limit |
| subscription_headlineLimit | Use {feature} as often as you need. | Variant: limit. {feature} = the feature name in the chip ("Before therapy", "After therapy", "Between Sessions", "Reflect", "session recordings", "the habit tracker") |
| subscription_sublineLimit | Everything you've saved stays saved. Premium removes the free limits on every feature. | Variant: limit |
| subscription_chipTrialActive | {days, plural, =0{Your free trial ends today} =1{Your free trial ends tomorrow} other{Your free trial ends in {days} days}} | Variant: trial, opened from the trial bar |
| subscription_chipTrialEnded | Your free trial has ended | Variant: trial, opened by trial_ended_popup |
| subscription_headlineTrialActive | Keep Premium after your trial. | Variant: trial, trial still running |
| subscription_headlineTrialEnded | Pick up where your trial left off. | Variant: trial, trial ended |
| subscription_sublineTrial | Your recordings, notes and summaries stay saved either way. Premium keeps every feature unlimited. | Variant: trial, both cases |
| subscription_planAnnual | Annual | |
| subscription_planMonthly | Monthly | |
| subscription_savePercent | Save {percent}% | existing key, new text (sentence case; the badge style can uppercase it) |
| subscription_badgeBestValue | Best value | Fallback badge when the saving cannot be computed. |
| subscription_planAnnualSub | About {monthlyPrice} a month | {monthlyPrice} = annual price divided by 12, store currency |
| subscription_planMonthlySub | Billed every month | |
| subscription_perYear | per year | existing key, new text |
| subscription_perMonth | per month | existing key, new text |
| subscription_cancelAnytimeStore | Cancel anytime in your store account. | Dropped "No questions asked." |
| subscription_tableTitle | What Premium changes | |
| subscription_tableFree | Free | |
| subscription_tablePremium | Premium | |
| subscription_rowBefore | Before therapy | |
| subscription_rowAfter | After therapy | |
| subscription_rowBetween | Between Sessions | |
| subscription_rowRecordings | Session recordings | |
| subscription_rowReflect | Reflect messages | |
| subscription_rowVoice | Reflect voice mode | |
| subscription_rowHabits | Habit tracker | |
| subscription_rowMonthly | Monthly therapy summary | |
| subscription_rowWeekly | Weekly therapy summary | |
| subscription_rowTrends | Mood & symptom trends | |
| subscription_valueOneAMonth | 1 a month | Free column: Before therapy, After therapy |
| subscription_valueThreeAMonth | 3 a month | Free column: Between Sessions |
| subscription_valueTwoTotal | 2 in total | Free column: Session recordings |
| subscription_valueFifteenAMonth | 15 a month | Free column: Reflect messages |
| subscription_valueOneHabit | 1 habit | Free column: Habit tracker |
| subscription_valueActivityOnly | Activity only | Free column: Monthly therapy summary |
| subscription_valueLocked | Locked | Free column: Reflect voice mode |
| subscription_valueIncluded | Included | Both columns where it applies |
| subscription_valueUnlimited | Unlimited | Premium column |
| subscription_valueFullSummary | Full summary | Premium column: Monthly therapy summary |
| subscription_tableFootnote | Free limits reset on the 1st of every month. You always see how many you have left. | Session recordings are a lifetime limit; the footnote is still true for the monthly rows. |
| subscription_starterTitle | Not ready to commit? | |
| subscription_starterBody | Try 14 days of Premium for {price}. | |
| subscription_starterCta | Try it | |
| subscription_promoToggle | Have a promo code? | |
| subscription_promoLabel | Promo code | |
| subscription_promoHint | Enter code | Mockup used a sample code; avoid showing a code that may not exist. |
| subscription_promoApply | Apply | Promo success and error messages: unchanged, existing settings_promo* strings. |
| subscription_ctaAnnual | Continue with Annual | |
| subscription_ctaMonthly | Continue with Monthly | |
| subscription_ctaBusy | Opening the store... | |
| subscription_billingAnnual | Billed {price} once a year. Renews automatically, cancel anytime. | {price} = annual price |
| subscription_billingMonthly | Billed {price} every month. Renews automatically, cancel anytime. | {price} = monthly price |
| subscription_termsOfService | Terms of Service | unchanged, existing key |
| subscription_privacyPolicy | Privacy Policy | existing key, capital P to match the other screens |

## Welcome (after purchase)

| key | text | note |
|---|---|---|
| premiumWelcome_title | Welcome to Premium | |
| premiumWelcome_subtitle | Your limits are off. Here are three places to start. | |
| premiumWelcome_afterTitle | After therapy | |
| premiumWelcome_afterBody | Write down what came up in your last session while it's fresh. | |
| premiumWelcome_recordTitle | Record your next session | |
| premiumWelcome_recordBody | Recordings are unlimited now, so you can save every session. | |
| premiumWelcome_monthlyTitle | Your monthly therapy summary | |
| premiumWelcome_monthlyBody | Read the full summary at the end of each month. | Mockup promised "the last month", which is empty for new users. |
| premiumWelcome_openAfter | Open After therapy | |
| premiumWelcome_backHome | Back to home | |

## Premium (active view)

| key | text | note |
|---|---|---|
| premium_title | Your subscription | |
| premium_eyebrow | MindSync Premium | |
| premium_badgeActive | Active | Variant: store (and starter pack) |
| premium_planAnnual | Annual plan | Variant: store |
| premium_planMonthly | Monthly plan | Variant: store |
| premium_renewsOn | Renews on {date} | Variant: store |
| premium_billedAppStore | Billed through the App Store | Variant: store, iOS |
| premium_billedGooglePlay | Billed through Google Play | Variant: store, Android |
| premium_manage | Manage subscription | Variant: store |
| premium_manageHint | Opens your store account, where you can switch plans or cancel. You keep Premium until the end of the paid period. | Variant: store |
| premium_badgeTrial | Free trial | Variant: trial |
| premium_planTrial | Premium trial | Variant: trial |
| premium_trialEndsOn | Trial ends on {date} | Variant: trial |
| premium_trialNoCharge | Nothing is charged automatically | Variant: trial |
| premium_choosePlan | Choose a plan | Variant: trial |
| premium_trialHint | Pick a plan before the trial ends to keep Before therapy, After therapy and recordings unlimited. | Variant: trial |
| premium_badgePromo | Promo code | Variant: promo |
| premium_planPromo | Premium via promo code | Variant: promo |
| premium_accessUntil | Access until {date} | Variant: promo and starter pack |
| premium_noPayment | No payment on file | Variant: promo |
| premium_seePlans | See plans | Variant: promo and starter pack |
| premium_promoHint | Your promo access ends on the date above. You can pick a plan anytime. | Variant: promo |
| premium_planStarter | 2 weeks of Premium | Variant: starter pack (not in the mockup; the starter pack is a fourth source) |
| premium_starterOneTime | One-time payment, nothing renews | Variant: starter pack |
| premium_starterHint | Your access ends on the date above. You can pick a plan anytime. | Variant: starter pack |
| premium_includedTitle | Included in your plan | |
| premium_featBeforeAfter | Unlimited Before therapy & After therapy | |
| premium_featRecordings | Unlimited session recordings | |
| premium_featReflect | Unlimited Reflect messages | |
| premium_featVoice | Reflect voice mode | |
| premium_featHabits | Unlimited habits | |
| premium_featMonthly | Full monthly therapy summary | |
| premium_restorePurchases | Restore purchases | |
| premium_terms | Terms of Service | |
| premium_privacy | Privacy Policy | |

## CountersHome

| key | text | note |
|---|---|---|
| usage_chipLeft | {left} of {limit} left | {left} >= 2. Monthly and lifetime limits. |
| usage_chipLastMonthly | Last one this month | {left} = 1, monthly limit above 1 (Between Sessions, Reflect) |
| usage_chipLastLifetime | Last one left | {left} = 1, session recordings (lifetime) |
| usage_chipOneFree | 1 free this month | Limit of 1 (Before therapy, After therapy) |
| usage_chipNoneLeft | 0 left · Premium | Tap opens the paywall with premium_gate_<feature> |
| usage_chipTrial | Unlimited in trial | |
| usage_resetsOn | Free limits reset on {date} | Free users only. {date} = resets_at |
| home_rowReflect | Talk with {orcaName} in Reflect | Home entry label from the mockup; use only if this row is new. |
| home_rowRecord | Record a session | Same |

## CountersReflect

| key | text | note |
|---|---|---|
| usage_reflectLeftLine | {left, plural, =1{1 of {limit} free messages left this month} other{{left} of {limit} free messages left this month}} | Under the input. {limit} comes from the API (15 today, no hardcoded 30). |
| usage_reflectNoneTitle | You've used your {limit} free messages this month. | |
| usage_reflectNoneBody | Your conversation stays saved. Free messages come back on {date}. | |
| usage_reflectNoneCta | Keep talking with Premium | |

The Reflect header chip uses `usage_chipLeft` and `usage_chipNoneLeft`. The input placeholder ("Write to {orcaName}...") is the existing string, unchanged.

## CountersStates (chip labels and the limit note)

Chip labels are the `usage_chip*` keys from CountersHome. The one extra string is the short note shown after the user saves their last free use:

| key | text | note |
|---|---|---|
| usage_lastUsedMonthly | That was your last free {feature} this month. It resets on {date}. | {feature} = "Before therapy", "After therapy", "Between Sessions" or "Reflect message" |
| usage_lastUsedRecording | That was your last free session recording. | Lifetime limit, no reset date. |
| usage_lastUsedHabit | Free includes 1 active habit. | Shown when the user adds their first habit and is on Free. |


## Lead decisions on open questions (2026-10-02)

- Age wording: keep the live "legal age" checkbox at sign-up and the live 16+ checkbox on the agreements screen. The 16 vs 18 mismatch is flagged to the operator, not changed here.
- Privacy consent checkbox and 16+ checkbox: live wording, unchanged.
- Limit numbers inside strings (paywall table, trial reminder) are hardcoded on purpose; if limits change, update the strings.
- Everything marked "(do not add)" above must not become an arb key.
