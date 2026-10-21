# Design conformance and logic audit: subscription + onboarding redesign (2026-10-02)

Auditor: ui-ux-designer (read-only). Scope: FE-A to FE-E, uncommitted working tree on `feat/subscription-onboarding-redesign` in `mindsync-frontend/`.
Sources of truth: `SPEC.md`, `copy-en.md` (wins over mockup text), `screens/*.dc.html`.
Method: code and test reading only. No tests were run, no code was changed. All paths are relative to `mindsync-frontend/mindsync_app/` unless stated.

## Summary

- Screens audited: 23 screens or variants. 13 MATCH, 10 MINOR DEVIATION, 0 MAJOR DEVIATION.
- Findings: 0 Blocker, 3 High, 18 Medium, 24 Low.
- Copy: 367 of 384 copy-en rows are identical in `app_en.arb`. Every mismatch is an allowed reuse or an accepted variant (section A.0). The five operator VERBATIM strings match character for character and are rendered unmodified. No key is missing in de, es, fr, nb, pl or sv. No U+2014 or U+2013 in any redesign key in any locale, and none in non-comment Dart code of the touched screens.
- The three High findings:
  1. The name typed on the name screen never reaches Build and Reveal (email users get no name, Google and Apple users get their account name instead of their chosen nickname).
  2. After a purchase on the post-onboarding offer, the Welcome screen's primary action ("Open After therapy") and its three start cards jump to Home and abandon the flow, so paying users skip the reminders pre-prompt and First step.
  3. Notification and moment entry points open Before therapy, After therapy and Between Sessions without the 0-left paywall gate.

---

## Part A. Conformance

### A.0 Copy diff (mechanical, copy-en.md vs `lib/l10n/app_en.arb`)

| Item | Result |
|---|---|
| Identical rows | 367 of 384 (excluding "(do not add)" rows, which correctly do not exist as keys) |
| `subscription_headlineLimit` | Implemented as an ICU `select` per feature; each branch equals the copy-en sentence with the right feature name, plus `other{Use Premium as often as you need.}`. Accepted (better for translation). |
| `auth_termsConfirmation` | Trailing space added before the link widget. Accepted. |
| `onboarding_progressStep` | Not created; existing `onboarding_stepOfTotal` ("{current} of {total}") reused, as copy-en allows. |
| `onboarding_disclaimerReadMore` | Not created; the full live disclaimer is shown inline in the card (lead decision). Accepted. |
| `postOnboarding_restore`, `_planAnnual`, `_planMonthly`, `_badgeBestValue`, `_terms`, `_privacy` | Not created; the offer reuses `subscription_*` keys with identical text. Accepted. |
| `reveal_firstReadMissing` | Not created; the block is hidden instead, which copy-en allows. |
| `home_rowReflect`, `home_rowRecord` | Not created; optional per copy-en (no new Home rows were built). |
| `usage_lastUsedHabit` | Not created and not implemented (Low finding L15). |
| VERBATIM strings | `firstStep_optionReflect`, `firstStep_optionBetweenSessions`, `firstStep_optionHealthCheck`, `firstStep_voiceNoteExplainer`, `postOnboarding_offerStarterBody`, `onboarding_capturePastSession`: all identical; rendered without trim or case transform (`lib/screens/wow/views/first_step_view.dart:53-55,123-133`, `post_onboarding_offer_view.dart:155`). |
| Range hyphens and consent | `auth_ageBand1824` = "18-24", `onboarding_1to6months` = "1-6 months", `onboarding_art9ConsentCheckbox` = comma version. Correct. |
| Locales | All 6 non-English arb files contain every English key. Only `push_exampleMeta` (format only), `subscription_eyebrow` and `premium_eyebrow` (brand name) equal English; sv also `onboarding_actDescription`. Fine. |
| Banned names in redesign keys | None. Older, out-of-scope strings still contain them: "debrief" in `stats_healthCheckEmpty`, `character_sessionDebriefs`, `settings_therapyFocusInfo`, `settings_frustrationInfo`, `info_therapyTabBody`; "progress snapshots" in `walkthrough_statsBody` (app tour); "full export access" in `settings_premiumDescription` (key is unused in Dart, so not visible). See L22. |
| Leftover old copy | "Success!" (`auth_success`) and "DIVE IN" (`onboarding_diveIn`) survive only in the unused `lib/l10n/parts/part_auth_onboarding.json`; nothing reads them. Deleted widgets (welcome_view, onboarding_welcome_splash, feature_list, subscription_selector, subscription_button, subscription_bottom_info, the three trial popups) have no remaining references. |

### A.1 Conformance table

| Screen (mockup) | Implementation | Structure and states | Copy | Actions | Tokens | Accessibility | Mental-health UX | Verdict |
|---|---|---|---|---|---|---|---|---|
| OB01Welcome | `lib/screens/welcome/welcome_body.dart` | Dark deepOcean, tinted logo (60-70), headline, subline, Get started, I already have an account, legal links (104-111). Same order. | Match | Get started -> auth sign-up (30), log in (35), analytics kept | MsColors | Buttons 56/52 dp with Semantics(button), links min 44 (182), headline is a header, 11.5:1 contrast | Calm | MATCH |
| OB02Account | `lib/screens/auth/auth_body.dart` | Back, title, subline, platform social first (238), "or with email", email, password, terms checkbox, Create account, footer toggle | Match, no privacy claim (lead decision) | Wired | Raw hex at 20 and 293 | Password visibility toggle has no Semantics label (280-299, pre-existing); terms error in red (381) | OK | MINOR DEVIATION |
| OB03Personalise | `lib/screens/sign_up/personalise_view.dart`, `widgets/gender_pronouns_selector.dart` | Name main field, age chips, gender and pronouns, hint, Continue. Gender and pronouns are dropdowns, not the mockup chip rows; "Prefer not to say" is last, mockup has it first (48-52). Self-describe kept. | Match | Empty name sent as null | OK | Name TextField has no label or hint (126-147, M14); hardcoded English semantics labels (selector 134, 204); age chips selected semantics, 44 dp | Optional fields marked | MINOR DEVIATION |
| OB04Legal (DIVE IN merged) | `therapy_onboarding/views/onboarding_legal_gate_view.dart` | Logo, greeting with name or neutral fallback (132-134), subtitle, card with full live disclaimer (186-193), both checkboxes, privacy link, language row (252), sticky Agree and continue | Match, consent wording live | Gated on both boxes (283) | OK | Checkbox tiles checked semantics, 44 dp, liveRegion hint | OK | MATCH |
| OB05Challenges | `views/onboarding_challenges_view.dart` | Chips + Add your own, CTA with ICU count (63-65), disabled at 0 | Match | Wired | OK | Chips 48 dp, selected semantics; unselected chip border 1.38:1 (same as mockup) | OK | MINOR DEVIATION (counter "1 of 5" where mockup shows "1 of 7", see M5) |
| OB06Intensity | `views/onboarding_intensity_view.dart`, `widgets/severity_slider_row.dart` | Card per area, big value, 1-10 slider, end labels | Match | Untouched default 5 (227) | OK | Slider label and value (378-384); inactive track 1.17:1 | OK | MATCH |
| OB07Journey | `views/onboarding_journey_view.dart` | Art.9 consent first, answers only after consent (257), duration chips and goal + crisis banner only for the two Yes answers (265-300) | Match | Continue / Skip | OK | Radio group semantics, checkbox semantics | Neutral skip, crisis banner kept | MATCH |
| OB08Modality | `views/onboarding_modality_view.dart` | 9 cards, "I'm not sure" exclusive, Other with text field. Selections not seeded from the cubit after back or resume (41, L4) | Match | Continue disabled when empty, Skip | OK | Toggled semantics | OK | MINOR DEVIATION |
| OB09Schedule | `views/onboarding_schedule_view.dart` | Weekday row, time, frequency incl. custom calendar (221-228), next-session line, "I don't have a date yet" | Match | Wired | Raw red 0xFFC94040 in custom calendar (653, 959, pre-existing) | Weekday buttons about 39 dp wide on 360 dp phones (140-165, L3); display honors 12/24 h (41-48) but `lib/widgets/ms_time_picker.dart:69,86` takes 24 h input only (L2) | OK | MINOR DEVIATION |
| OB10Companion | `views/onboarding_companion_view.dart` | AnimatedOrca, name, 5 styles, live sample bubble with name / no-name (172-180), color picker kept (184-219), change-anytime line | Match incl. fixed coach sample | Name required (107) | OK | Color circles 48 dp radio semantics; AnimatedOrca ignores disableAnimations (`lib/widgets/animated_orca.dart:255`, L7) | OK | MINOR DEVIATION |
| OB11Source | `views/onboarding_lead_source_view.dart` | 6 radio cards, Somewhere else text field, Set up my app, I'd rather not say | Match | Wired | OK | Radio semantics | Non-shaming skip | MATCH (analytics issue M16) |
| PersonalBuild | `lib/screens/wow/views/personal_build_view.dart` | Four steps (25-42), first-week step replaces reminders when no schedule (30-39), neutral title when name empty (62) | Match | n/a | Tokens | Reduced motion stops halo and spinner (142-150, 207, 237); live region re-reads all rows every second (79, L19) | Calm | MATCH (but name never arrives, H1) |
| PersonalReveal | `views/personal_reveal_view.dart` | Header, focus areas with 5-bar intensity and a11y label (252-255, 274-277), week strip in-therapy vs first week (317-352), first read loading / ready / hidden (64-77), tone card, sticky CTA. First-week plan has 2 rows while Build promises a check-in (L18); first-read block collapses at deadline while reading (L20) | Match | Let's start | Tokens | Reduced motion on loading (492-499) | Graceful absence | MINOR DEVIATION |
| PostOnboarding offer | `views/post_onboarding_offer_view.dart` | Close X 44 dp with `postOnboarding_closeA11y` (274-290), Restore 44 dp (298), starter + Annual + Monthly radio cards (391-396), CTA and billing per selection (106-119), skip 44 dp (223-237). Annual badge shows "Save N%" when computable instead of copy-en "Best value" (166, accepted, matches paywall). Plan group has no group label (L17). Starter card can be missing (M6). Trial copy can be untrue (M1). | Match incl. VERBATIM starter body | Wired | Tokens | Unselected radio ring 1.79:1 (419, L13) | Honest billing lines, but see M1 | MINOR DEVIATION |
| OB15Push | `views/push_preprompt_view.dart` | Title/subtitle variants (89, 95), two example cards from real moments: prep + post-session, or check-in + Reflect (43-73) | Match | Turn on / Not now, both 44 dp+ (123-142) | Tokens | OK | No pressure | MATCH |
| FlowFirstStep | `views/first_step_view.dart` | Trial chip (70-80), capture card only in therapy (95-108), three VERBATIM options 60 dp+ (109-116), explainer with dot (123-133), Take me to the app 48 dp (141-157) | Match, VERBATIM intact | Wired (see B.3) | Tokens | Option tiles wrap the tap target in a button label without merging (210, 261): device QA | OK | MINOR DEVIATION (stale trial chip after purchase, M18) |
| Main paywall, generic | `lib/screens/subscription/subscription_body.dart`, `widgets/*` | Close X left, Restore right (`paywall_header.dart:90-122`), eyebrow, headline, subline (130-141), plan radio cards (body 329), cancel line (339), table (351), starter + promo (358-360), legal (366), sticky CTA + billing (375-386) | Match | All wired (body 286-301, 321-322; `starter_pack_card.dart:238-240`; `paywall_promo_section.dart:320-348`) | Raw hex in `subscription_style.dart:452-458` (L10) | Close X 44 dp + Semantics label; plan cards checked / inMutuallyExclusiveGroup (`plan_selector.dart:329-333`); eyebrow 4.47:1 (L11); table rows not labeled per column for screen readers (L12) | Weekly summary and trends "Included" in both columns; no export promise; honest billing | MATCH |
| Main paywall, limit | `paywall_context.dart:37-45,99-105` | Chip above eyebrow, per-feature headline; accepts `session_recording` and `session_recordings` | Match | Same | Same | Chip has icon + text | No shaming | MATCH |
| Main paywall, trial (running / ended) | `paywall_header.dart:24-31`, `paywall_context.dart:107-120` | Chip + headline variants | Match | Same | Same | Same | Honest | MATCH (day count, see M9) |
| Welcome (after purchase) | `premium_welcome_screen.dart` | Check icon, title, subtitle, 3 start cards, Open After therapy, Back to home (76-170); routes exist | Match | Back blocked -> Home (61-66). Start points ignore the offer flow (H2) | Tokens | 48 dp targets, number badges excluded from semantics | Calm | MINOR DEVIATION |
| Premium active, store | `widgets/premium_view.dart:158-289` | Plan card, App Store / Google Play line (119), Manage (68-85), hint, included list, Restore, legal | Match | Manage opens store page | OK | OK | OK | MATCH |
| Premium active, trial / promo / starter_pack | `premium_view.dart:123-146`, `premium_status.dart:42-79` | Variant cards; Choose a plan / See plans switch to paywall in place (`subscription_screen.dart:96-99`) | Match | Wired | OK | OK | Honest; stale comment at `premium_status.dart:14-17` (L14) | MATCH |
| CountersStates | `lib/screens/usage/usage_feature.dart:68-91`, `widgets/usage_chip.dart:17-32` | Hidden (premium / unknown / error), Unlimited in trial, N of M left, Last one this month / 1 free this month / Last one left, 0 left · Premium | Match | 0 opens paywall | Hex not MsColors (53-71, L10) | State always in text; 12 sp text; no own Semantics (read as part of parent button) | OK | MATCH |
| CountersHome | `main_tab/main_tab_screen.dart:1105,1190,1254,1344-1373`, `widgets/ms_fab.dart:272`, `getting_started_card.dart:166`, `timeline_capture_bridge_card.dart:168`, reset line `main_tab_screen.dart:527` | Chips on real entry points. Chip inline in a single-row 44 dp button instead of stacked under the label in a 64 dp tile (L9). No new Reflect / Record rows (optional). | Match | Gated (B.5) | Hex | Truncation risk at large text | OK | MINOR DEVIATION |
| CountersReflect | `reflect_tab/widgets/reflect_usage_indicator.dart:30-151`, `reflect_tab_screen.dart:778-797` | Header chip, left line, none-left panel replacing input | Match | Keep talking -> paywall | Hex panel (111-112) | OK | "Your conversation stays saved" | MATCH |
| Trial bar (CurHome) | `lib/screens/usage/widgets/trial_bar.dart:24-133` | Text + determinate progress + See plans (`trial_banner`) | Match incl. "last day" plural | Whole bar ~68 dp, Semantics(button) | Hex accent (15) | Determinate progress, no motion issue | Calm | MATCH |
| FlowTrialReminder | `lib/screens/usage/widgets/trial_reminder_sheet.dart:44-140` | Eyebrow, title (header semantics), subtitle, three stats, free limits, Keep Premium, Not now 48 dp | Match | Wired | Hex eyebrow (87) | Eyebrow forced to uppercase (86, L16) | "Everything you saved stays saved" | MATCH |

---

## Part B. Logic walkthrough

Legend: WORKS / RISK / BROKEN. "Test" names the covering test or says "no test".

### B.1 Sign-up paths

| Path | Status | Evidence | Test |
|---|---|---|---|
| Email sign-up: Personalise -> register -> CheckEmail -> onboarding | WORKS | `auth_body.dart:150`, `sign_up_cubit.dart:155-250,306-315`, `sign_up_screen.dart:47-48` | `sign_up_success_removal_test` "email path: CheckEmail -> completed -> onboarding, no Success screen" |
| Apple / Google new account | WORKS (happy path), RISK (error path) | 404 -> needsRegistration (`auth_cubit.dart:300-311,400-411`), `registerForGoogleAndApple` (`sign_up_cubit.dart:257-300`) has no try/finally: backend error leaves a spinner forever (pre-existing, M15) | "social path: personalise -> completed -> onboarding immediately"; error path no test |
| Existing account, email log-in | WORKS | `auth_cubit.dart:217-221` -> `resolveForExistingAccount` | `auth_cubit_email_login_destination_test` (completed / not completed / 404 / 5xx) |
| Existing account, Apple / Google | WORKS | `auth_cubit.dart:285-289,385-389` | `post_login_destination_resolver_test` group `resolveForExistingAccount()` |
| Resolver | WORKS | `lib/services/post_login_destination_resolver.dart:43-71`: completed -> Home, not completed -> onboarding, 5xx -> Home (existing account) or retry (splash), `profile_not_created` 404 -> onboarding without sign-out (splash 221-234) | resolver test, 9 cases |
| No "Success" screen | WORKS | `welcome_view.dart` deleted, no route; dead widget `lib/screens/auth/widgets/welcome_bottom_button.dart` and unused parts JSON remain (L21) | `sign_up_success_removal_test` |

### B.2 Onboarding

| Item | Status | Evidence | Test |
|---|---|---|---|
| 7-step path | WORKS | `therapy_onboarding_state.dart:62-114`, `saveJourneyAndAdvance` (`therapy_onboarding_cubit.dart:497-548`) | `therapy_onboarding_cubit_branching_test` "in therapy: onboarding_step 4..." |
| 5-step path (not in therapy, or no Art.9 consent) | WORKS | Visibility needs consent AND a yes answer (state 75-78); 3 -> 6 | "not in therapy: onboarding_step 6...", "no consent (status null)...", "a yes answer without Art.9 consent does not count" |
| Back across the skip | WORKS in-app; RISK for system back | `previousScreenBefore` (state 108-113, cubit 704-715). No PopScope in the flow, so Android system / predictive back is not mapped to step back (pre-existing) | "not in therapy: back from companion lands on the journey"; system back no test |
| Changing the answer no -> yes | WORKS | Steps return | "changing the answer back to in therapy brings the steps back" |
| Changing the answer yes -> no after schedule saved | RISK | Steps disappear, but saved schedule (prefs + backend sync, cubit 719-743) and `therapy_modalities` (585) stay, so prep reminders continue (M4) | Test only checks the step list |
| Resume after kill, steps 0-5 | WORKS | `resumedIntoTherapySteps` keeps 7 steps (cubit 202) | "saved step $step resumes on that (visible) step", "resumed on step 4..." |
| Resume after kill at step 6, in-therapy user | BROKEN | `currentlyInTherapy` not restored (`loadExistingContext` 191-204): counter "4 of 5", back skips schedule, `completedCurrentlyInTherapy` / `completedNextSession` null (794-803) so Build / Reveal / Push / First step show not-in-therapy variants and no capture card (M3) | Only not-in-therapy resume tested |
| Resume at step 7 | WORKS (acceptable) | Step 7 never saved, resumes on companion | n/a |
| Resume into a skipped step | WORKS (impossible) | | covered |
| Progress counter | RISK | Steps 1-3 show "n of 5" for everyone; in-therapy users see total jump to 7 at the journey step. Test named "step 1 shows 1 of 7" asserts "1 of 5" (`onboarding_redesign_views_test.dart:119-125`) (M5) | misnamed test |
| Consent writes once (GDPR + 16+) | WORKS | Emits saving before first await (cubit 259), gate view empty while saving, back clamps at 1, idempotent upsert on retry | "both boxes required; consent accepted exactly once" |
| Art.9 grant once | RISK (Low) | No in-flight guard (journey view 343-389), double tap can grant twice (L8) | no test |
| Art.9 status load race | RISK | `loadArt9HealthConsentStatus` (cubit 436-445) emits a stale `copyWith` after await and can roll `currentScreen` back to 3 after a quick Skip (M17) | no test |
| `_stepNames` and `onboarding_step` stable | WORKS | cubit 78-87 unchanged; `total_steps` added from step 3 | branching tests |
| Time format by device locale | RISK | Display honors 12/24 h; picker is 24 h input only (L2) | no 12 h test |

### B.3 Post-onboarding

| Item | Status | Evidence | Test |
|---|---|---|---|
| Build cap / timeouts | WORKS | 4 ticks of 1 s (`wow_cubit.dart:128-135`), profile call capped at 5 s (140, 158) | `wow_cubit_test` "never hangs...", "a profile call that never answers is capped..." |
| User name on Build / Reveal | BROKEN | `advanceToLeadSource` reads `_resolveGreetingName()` from the pending profile JSON (cubit 805, 211-234), which `_flushPendingProfile` cleared at consent (cubit 275; `users_manager.dart:386-395`). Falls back to Firebase displayName (H1) | no test; fixtures inject the name (`wow_test_helpers.dart:119`) |
| Reveal first read ready / late / absent | WORKS | Poll every 3 s, 8 s per call, 25 s deadline (`wow_cubit.dart:181-211`); failed or empty patterns hides the block | cubit "ready", "absent" x2, "late"; screen "first read absent", "first read late" |
| Reveal in therapy vs not | WORKS (given correct input) | `wow_screen_params.dart:48`; focus-area join max two (`post_onboarding_format.dart:44-49`); 1-10 -> 5 bars (format 13), default 5 -> 3 bars | screen Reveal tests, helpers "intensity 1-10 maps..." |
| Offer skip reasons | WORKS | Order (`wow_cubit.dart:264-282`): not just onboarded, profile unavailable, already premium (purchase / starter / null source), already seen, products unavailable (4 s cap). Promo users still see it. | cubit "Offer decision" (6 tests), screen "store products missing" |
| Offer without an active sign-up trial | RISK | No check that the trial is active, so "Your first 4 days of Premium are on us" can be shown to promo users, re-onboarded or expired accounts (M1) | no test |
| Starter unavailable, plans loaded | WORKS | Card hidden, Annual preselected (offer view 38-40) | screen "starter unavailable..." |
| Starter loads after offer shown | RISK | Read once (offer view 35-41), later arrival stored without rebuild (92); decision waits only for subscription products (`wow_screen.dart:94-100`) (M6) | no test |
| Purchase success -> Welcome -> reminders | RISK / BROKEN for primary CTA | "Back to home" and system back continue the flow (`wow_screen.dart:124-137`, `premium_welcome_screen.dart:61-65`). "Open After therapy" and the 3 cards go Home (29-32, 43-57, 151) and abandon the flow (H2) | screen test covers starter + "Back to home" only |
| Store cancel stays | WORKS | `subscription_cubit.dart:341-353`; starter cancel reloads product (starter cubit 138-140) | no screen test |
| Purchase / restore error on offer | RISK | Error state yields no plans (offer view 44-45, 84-89); failed restore never reloads products (`subscription_cubit.dart:229`): cards vanish, Annual CTA dead (M7) | no test |
| Starter purchase seen by both listeners | RISK | Subscription listener does not ignore `ms_starter_package` (`subscription_cubit.dart:135,233-312`), races starter verification, may log `purchased_annual` (`wow_screen.dart:111-116`) and fire a second `subscription_purchase_completed` (M2) | no test |
| Offer once per account | WORKS | Per-uid flag (`push_prompt_policy.dart:75-96`), marked on show (`wow_cubit.dart:251`); flow only runs after onboarding completion | cubit "shown ... once per account" |
| `paywall_shown` with `post_onboarding` | WORKS | Deferred until the offer step appears (`wow_screen.dart:69-79,190-192`; `subscription_cubit.dart:75-85,119-128`) | screen "...paywall_shown revealed"; cubit "deferred paywall" |
| `post_onboarding_offer_result` | WORKS | skipped (close_x / continue_free), purchased_starter / _annual / _monthly, plus extra `restored`; once | cubit "Offer actions" |
| Reminders accept / OS decline / Not now | WORKS | `wow_cubit.dart:386-408`; `push_prompt_result` accepted / declined / not_now | cubit 3 tests; screen "Not now skips the OS" |
| Reminders already decided | WORKS | Granted or permanently denied skips the pre-prompt (350-354); Android "never asked" vs "said no" (`push_permission_gateway.dart:35-43`) | cubit "already granted/denied", "status unreadable" |
| No cold OS prompt on Home for new-flow accounts | WORKS same session; RISK later | Home checks policy (`main_page_body.dart:88`, `fcm_token_service.dart:29-32`). "In flow" flag is in memory, "answered" flag per uid per device: kill mid-flow, reinstall or second device brings the cold prompt back (intended per code comments) | cubit "defers the cold push prompt..."; `fcm_cold_prompt_policy_test` |
| Existing accounts unchanged | WORKS | No flags set, old request runs | no direct test |
| First step targets | WORKS | Capture (in therapy only) -> After therapy over Home; Reflect -> tab 2; Between Sessions and health check -> their flows; Take me to the app -> Home (`wow_screen.dart:141-167`, `ms_routes.dart:81-87`) | screen tests for capture, take-me-to-app, Reflect tab |
| App tour not auto-opened | WORKS | Suppressed when Reveal viewed (`wow_cubit.dart:222`, `app_tour_cubit.dart:46-50`); kill during Build means tour auto-opens next launch | `app_tour_suppression_test` (4) |
| App killed mid-flow | WORKS, degraded | Next launch -> Home (onboarding complete). Offer and pre-prompt lost, cold prompt returns, offer never shown twice, nobody stuck | no test |
| Back / predictive back | WORKS | System back blocked for the whole flow (`wow_screen.dart:172`); explicit exits only | no test |
| Reveal CTA busy wait | RISK (Low) | Up to about 7 s (4 s offer decision + 3 s permission check) (276, 342) | no test |

### B.4 Subscription

| Item | Status | Evidence | Test |
|---|---|---|---|
| `premium_gate_<feature>` -> limit variant with right chip | WORKS | `paywall_context.dart:37-45,99-105` | `paywall_context_test` "premium_gate_$gate -> limit chip"; body tests "limit: chip names...", "limit: Reflect chip quotes the 15" |
| Unknown gate (`reflect_voice`, `monthly_audit`) | WORKS | Falls back to generic (104); voice-mode headline reads generic (L23) | "a gate without a chip ... falls back to generic" |
| `trial_ended_popup` / `trial_banner` | WORKS | 107-120, `calendarDaysUntil` 127-136 | "trial_ended_popup -> ended", "trial_banner with a running trial", "after the trial lapsed" |
| Generic otherwise | WORKS | 122 | "everything else -> generic" |
| Annual preselected, plan switch -> CTA + billing line | WORKS | `plan_selector.dart:39`, body 263, 286-290, 376-383 | "annual is preselected...", "switching to monthly changes CTA and billing line" |
| Save % and fallback | WORKS | `plan_selector.dart:44-52,100` | "falls back to Best value when only one plan loaded" |
| No store products | RISK | Full paywall with disabled CTA and no explanation (body 379-385) (M8) | no test |
| Starter hidden on product error | WORKS | `starter_pack_card.dart:19-26` | "hidden when the product failed to load" |
| Starter purchase error | RISK | Card disappears silently, flickers on cancel (M7) | no test |
| Promo | WORKS | Same SettingsCubit calls + `refreshSubscriptionInfo` (promo section 320-326); user then stays on the purchase paywall (L24) | "collapsed by default...applies through SettingsCubit", "a verified code refreshes..." |
| Restore | WORKS | Lands on Premium view (`subscription_screen.dart:80`); failed restore shows English-only ErrorView (cubit 229, L6) | "Restore in the header calls restorePurchases once", "a completed restore stays..." |
| Restore of an expired store subscription | RISK | `justCompleted` forces Premium view with source purchase (`subscription_screen.dart:154,198`) | no test; device QA |
| Premium-active variant by `premium_source` | WORKS | `premium_status.dart:42-79`: purchase, null, starter_pack always; signup_trial and promo from drawer / settings | `subscription_screen_gate_test` (4 sources + unknown) |
| After-purchase Welcome | WORKS (outside offer) | `subscription_screen.dart:74-94` | "a completed purchase replaces the paywall with the Welcome screen" |
| Store cancel | WORKS for `canceled`; RISK if store reports an error (error flash, plan resets to Annual, cubit 329-340, L5) | | cubit analytics test only |
| Analytics kept | WORKS | paywall_shown once (cubit 91-112), product selected (149-160), purchase and restore events kept. `paywall_dismissed` fires only from Premium view back (`premium_view.dart:88`), not from the paywall X (note for the PostHog audit) | cubit analytics groups |

### B.5 Trial and usage

| Item | Status | Evidence | Test |
|---|---|---|---|
| Usage states | WORKS | `usage_feature.dart:68-91`; free with null / 0 limit hidden; overuse clamped | `usage_model_and_cubit_test` "resolveUsageChip" |
| Gate at 0 opens paywall and returns | WORKS | `usage_gate.dart:36-57` (push, await, refresh, stay) | "at 0: logs, opens the paywall..." |
| In-app entry points gated | WORKS | Home cards via `therapy_flow_launcher.dart:81-90` (callers `main_tab_screen.dart:395,427,445`), FAB (`main_page_body.dart:632-690`), Getting started (`getting_started_card.dart:57`), timeline bridge (`timeline_capture_bridge_card.dart:93`), Reflect new conversation (`reflect_tab_screen.dart:897-909`) | "TherapyFlowLauncher (all Home / FAB / timeline entry points)"; Reflect new-thread gate and Getting started: no test |
| Notification / moment entry points | BROKEN (vs spec) | `lib/main.dart:185,301`, `lib/utils/notification_route_resolver.dart:50-52`, `widgets/moments/renderers/post_session_reflection_sheet.dart:99-102,169-174` open flows without the gate; backend silently saves `plain_text` (H3) | no test |
| Reading never gated | WORKS | View-unfinished runs before gate (`therapy_flow_launcher.dart:48-76`); Reflect threads open, only input becomes the limit panel. Side effect: at 0, a latest `plain_text` entry triggers the "unfinished note" dialog first | partial |
| Usage 404 / 5xx / timeout / bad JSON | WORKS | `usage_cubit.dart:59-70` -> unavailable, chips hidden, gate passes; parser throws only when `plan` missing (`user_usage.dart:51-78`) | "-> unavailable, every chip hidden, nothing gated", "an error after a good load..." |
| Reflect clamp at 0, limit from API | WORKS | `reflect_usage_indicator.dart:30-32`; unclamped `remainingMessages` in `reflect_chat_cubit.dart:264,447` is unused by UI | "limit and used come from /reflect/usage, clamped at 0" |
| Trial bar days math around 00:00 UTC | WORKS (math), RISK (copy) | `trial_timing.dart:25-39`, calendar days in device zone, 0 on end day, hidden after, never negative. East of UTC "last day" almost never shows and the bar says "1 day left" on the real last day. Three different formulas and two end-date sources across paywall chip, trial bar and First-step chip (M9) | "trialDaysLeft / isTrialReminderDay across time zones" |
| Day-3 sheet once | WORKS | One day left, once per uid, flag written before show (`trial_popup_manager.dart:57,98,140`); first open on day 4 shows nothing. Eyebrow "Day 3 of 4" is off by one in UTC+ zones (L1). "Keep Premium" reuses `trial_banner` (L25) | "day-3 sheet: ... once per account", "Not now closes without a paywall" |
| Trial-ended paywall once, recent sign-up trials only | WORKS (logic), RISK (product) | `trial_timing.dart:52-65`: free plan, inactive, `premium_source == signup_trial`, ended within 30 days; once per uid. On release every trial that ended in the last 30 days gets it (M11); flag in SharedPreferences, reinstall shows it again | "trial ended: paywall, within 30 days only", "never for buyers, promo, active or premium-plan accounts" |
| Startup popup order | WORKS in code, RISK on device | `main_page_body.dart:85-117` awaits trial popup then moments queue; skipped while tour pending or after post-onboarding flow. `FCMTokenService.initialize()` (82) runs in parallel, OS dialog can overlap the sheet for legacy users; cold start from a notification can stack the paywall on the deep-linked flow (M13) | manager tested alone; MainPageBody order no test |
| Sign-out resets usage | WORKS for drawer sign-out; RISK elsewhere | `main_page_cubit.dart:81`. Account deletion (`settings_cubit.dart:861-873`) and splash 404 sign-out (`splash_screen.dart:242`) do not reset; `reset()` keeps `_inFlight` (`usage_cubit.dart:54,82-85`); `TrialPopupManager._handledThisSession` (52) never reset (M12) | cubit "reset (sign-out) drops the previous account"; wiring no test |
| Refresh after each gated action | RISK | `UsageGate.afterUse` refreshes right after the flow pops (`usage_gate.dart:62-87`) while the FAB handler waits 2 s for the commit (`main_page_body.dart:692-693`) and recordings upload in background: chip stale, "last free" note skipped, next tap opens the flow instead of the paywall (M10) | "last one -> zero shows the note once" (mocked timing) |

### B.6 Cross-checks

| Check | Status | Evidence |
|---|---|---|
| Backend error misread as a user state | WORKS | Usage error never becomes "free, 0 left"; trial-ended decision needs a successful usage load; resolver 5xx -> Home for existing accounts, retry on splash; `profile_not_created` 404 is the only onboarding trigger. Only weak spot: an empty store response looks like a dead paywall (M8) |
| Dead routes / unreachable screens | WORKS | `/premium-welcome` wired. Dead file `lib/screens/auth/widgets/welcome_bottom_button.dart`; unused `lib/l10n/parts/*.json` with old copy (L21). Older unreferenced route constants predate this batch |
| Missing locale keys | WORKS | none missing in 6 locales |
| Hardcoded limits / prices | WORKS | No prices in Dart. Constants `kSignupTrialDays = 4` and the 30-day window (`trial_timing.dart:7,12`). Limit numbers live in arb strings by lead decision. Hardcoded English: cubit error strings (`subscription_cubit.dart:229,326,339,422`), onboarding snackbars (cubit 209, 289, 396, 425, 530, 546), semantics labels (`gender_pronouns_selector.dart:134,204`), orca fallback "Orca" (`therapy_onboarding_screen.dart:95`, `ms_routes.dart:524`) |

---

## Part C. Findings (sorted by severity)

### Blocker

None.

### High

| ID | What | Where | Why it matters | Suggested fix | Owner |
|---|---|---|---|---|---|
| H1 | Name typed on the name screen never reaches Build and Reveal | `therapy_onboarding_cubit.dart:805` reads `_resolveGreetingName()` (211-234) from pending profile JSON that `_flushPendingProfile` cleared at consent (275; `users_manager.dart:386-395`) | Email users see "Your MindSync is ready." with no name right after being greeted by name; Google / Apple users see their account first name instead of the nickname they chose (can be a legal or dead name, a sensitive identity issue) | Use `state.greetingName` (held since screen 0); on resume fall back to profile `full_name`; add a cubit test across consent -> companion | flutter-mobile |
| H2 | Welcome after an offer purchase exits the post-onboarding flow | `premium_welcome_screen.dart:29-32,43-57,151` vs `wow_screen.dart:124-142` | Paying new users skip the reminders pre-prompt and First step, no `push_prompt_result` is logged, and the cold OS prompt fires next launch. Breaks SPEC FE-D "purchase success -> Welcome -> continue" | In flow mode (when `onBackHome` is set) route every action through the caller (for example `onContinue(route)` resumed after reminders), or show a single Continue | flutter-mobile |
| H3 | Notification and moment entry points skip the 0-left gate | `lib/main.dart:185,301`, `lib/utils/notification_route_resolver.dart:50-52`, `post_session_reflection_sheet.dart:99-102,169-174` | A Free user at 0 who taps the prep reminder (which the new pre-prompt promotes) saves an entry that silently gets no AI summary; feels broken and breaks "0 left opens the paywall" | Route these through `UsageGate.allowOrPaywall` with push / moment trigger context; add tests | flutter-mobile |

### Medium

| ID | What | Where | Why it matters | Suggested fix | Owner |
|---|---|---|---|---|---|
| M1 | Offer can claim "4 days of Premium are on us" with no active trial | `wow_cubit.dart:264-282`; offer copy and close a11y label | Dishonest billing line for promo users, re-onboarded or expired accounts | Require an active sign-up trial (trial days left not null); otherwise skip with a new reason or neutral copy | flutter-mobile |
| M2 | Starter purchase handled by both purchase listeners | `subscription_cubit.dart:135,233-312`; `subscription_screen.dart:105-115`; `wow_screen.dart:111-116` | Subscription verify races the one-time verify (possible wrong `premium_source` / end date), duplicate `subscription_purchase_completed`, `purchased_annual` logged for a starter buy | Subscription listener ignores products it did not load (`ms_starter_package`); backend-api confirms what subscription verify does with a starter receipt | flutter-mobile (+ backend-api check) |
| M3 | Resume at step 6 loses the in-therapy answer | `therapy_onboarding_cubit.dart:191-204,794-803` | Counter "4 of 5", back skips schedule, post-onboarding shows not-in-therapy variants, no capture card, saved session ignored | Restore `currentlyInTherapy` from profile (or prefs) on resume, derive next session from saved schedule; add test | flutter-mobile (backend-api only if the field is missing from the API) |
| M4 | Switching to "not in therapy" after the schedule step keeps schedule and modalities | `therapy_onboarding_cubit.dart:719-743,585` | Prep reminders ("Your session is tomorrow") reach someone who just said they are not in therapy | Clear prefs schedule and sync an empty schedule (optionally clear modalities) when the answer turns non-therapy, or defer the write to completion; add test | flutter-mobile |
| M5 | Progress total grows from 5 to 7 at step 3; misnamed test | `therapy_onboarding_state.dart:75-86`; `onboarding_redesign_views_test.dart:119-125` | Moving goalpost exactly for the users with the longer flow; mockups show "1 of 7" | Default to 7 until the branch is known (total only shrinks), or hide "of N" before step 3; rename the test | flutter-mobile |
| M6 | Starter card can be missing on the offer | `post_onboarding_offer_view.dart:35-41,92`; `wow_screen.dart:94-100` | On a slow network the operator's main offer is absent or pops in unselected later | Rebuild on starter arrival, preselect if untouched; include starter in the offer-decision wait | flutter-mobile |
| M7 | Purchase / restore errors silent; plan and starter cards vanish | Offer view 44-45, 84-89; `subscription_cubit.dart:229`; `starter_pack_card.dart:19-26` | After a failed restore the Annual CTA is dead; a failed starter purchase removes the cheaper option without a word | Keep last loaded plans in view; show an empathetic inline error ("Something went wrong. Let's try again.") for both purchase types | flutter-mobile |
| M8 | Empty store response shows a dead paywall | `subscription_body.dart:379-385` | Full paywall with a disabled CTA and no explanation | Calm "store unavailable" state with retry | flutter-mobile |
| M9 | Trial day counts disagree across screens | `paywall_context.dart:118`, `trial_timing.dart:25-38`, `wow_cubit.dart:144` via `premium_status.dart:130-143` | In US time zones right after sign-up First step says "4 days left" while Home says "3 days left" | One helper, one source (`usage.trialEndsAt`, calendar days) | flutter-mobile |
| M10 | Usage refresh runs before the save lands | `usage_gate.dart:62-79`; `main_page_body.dart:685-693` | Chip stays "1 left", "last free" note skipped, next tap opens the flow and saves a plain-text entry | Refresh again after the existing 2 s commit delay; for recordings refresh on upload completion | flutter-mobile |
| M11 | Trial-ended paywall reaches trials that ended up to 30 days before the update | `trial_timing.dart:12` | Surprise paywall for existing users, against "existing users are not notified about the limit change" | Operator decision: shrink the window (for example 3 days) or require the trial to have ended after this build was installed | flutter-mobile (after operator decision) |
| M12 | Stale state across accounts in one process | `settings_cubit.dart:861-873`, `splash_screen.dart:242`, `usage_cubit.dart:82`, `trial_popup_manager.dart:52` | After delete + new sign-up, old chips or a wrong gate briefly show; trial popups suppressed until restart | One "session cleared" hook resetting UsageCubit (incl. `_inFlight`) and TrialPopupManager | flutter-mobile |
| M13 | Startup popups can collide | `main_page_body.dart:82,104-110` | Trial-ended paywall stacks on a deep-linked flow; legacy users get the OS push dialog over the day-3 sheet | Skip trial popups on notification / deep-link opens; await the FCM permission step before popups | flutter-mobile |
| M14 | Name field has no accessible label | `personalise_view.dart:126-147` | Main field of the screen announced as an unlabeled text box | `InputDecoration(labelText: l10n.auth_nameFieldLabel)` or `Semantics(label:)` | flutter-mobile |
| M15 | `registerForGoogleAndApple` has no error handling (pre-existing) | `sign_up_cubit.dart:257-300` | Backend error leaves an endless spinner in the most fragile flow | Mirror `register()`: try/finally, `signupFailed` event, empathetic message | flutter-mobile |
| M16 | Lead source "Somewhere else" sends free text to PostHog (pre-existing) | `onboarding_lead_source_view.dart:57-63,86,119-122,132` | Conflicts with SPEC 6.3 "no free text in events"; user may type personal data | Send `text_length` only, once, on completion | flutter-mobile |
| M17 | Art.9 status load race can revert the screen | `therapy_onboarding_cubit.dart:436-445` | After a quick Skip the user is pulled back to the journey step | Re-read `state` after await and patch only `art9HealthConsentActive` | flutter-mobile |
| M18 | First-step trial chip stale after purchase on the offer | `wow_cubit.dart:143-150`; `first_step_view.dart:70-80` | A user who just paid sees "Premium trial · 4 days left" | Clear trial days left in purchase and restore handlers | flutter-mobile |

### Low

| ID | What | Where | Suggested fix | Owner |
|---|---|---|---|---|
| L1 | "Day 3 of 4" eyebrow off by one in UTC+ zones; "last day" rarely shown east of UTC | `trial_timing.dart:25-43`, `trial_reminder_sheet.dart` | Compute from days since sign-up or drop the number | flutter-mobile |
| L2 | Time picker 24 h input only | `lib/widgets/ms_time_picker.dart:69,86` | Follow `MediaQuery.alwaysUse24HourFormat` | flutter-mobile |
| L3 | Weekday buttons under 44 dp wide on 360 dp screens | `onboarding_schedule_view.dart:140-165` | Reduce gap or allow scroll | flutter-mobile |
| L4 | Modality selections not seeded after back or resume | `onboarding_modality_view.dart:41` | Seed `_selected` from cubit | flutter-mobile |
| L5 | Store cancel reported as error flashes error screen and resets plan | `subscription_cubit.dart:329-340` | Treat cancel-like errors as `canceled` | flutter-mobile |
| L6 | Hardcoded English error strings and snackbars, error red tone | `subscription_cubit.dart:229,326,339,422`; onboarding cubit 209, 289, 396, 425, 530, 546 | Localize; warm amber; inline with retry | flutter-mobile |
| L7 | AnimatedOrca ignores reduced motion | `lib/widgets/animated_orca.dart:255` | Respect `MediaQuery.disableAnimations` | flutter-mobile |
| L8 | Art.9 grant can fire twice on double tap | `onboarding_journey_view.dart:343-389` | In-flight guard | flutter-mobile |
| L9 | Home chips inline in a 44 dp single-row button instead of stacked | `main_tab_screen.dart:1344-1373` | Chip on a second line, 56-64 dp min height | flutter-mobile |
| L10 | Raw hex instead of MsColors | `subscription_style.dart:452-458`, `usage_chip.dart:53-71`, `trial_bar.dart:15,92,114`, `trial_reminder_sheet.dart:87`, `reflect_usage_indicator.dart:111-112`, `auth_body.dart:20,293`, `terms_of_service_checkbox.dart:28` | Promote to tokens | flutter-mobile |
| L11 | Contrast slightly short: paywall eyebrow 4.47:1; unselected radio ring / card border under 3:1 | `paywall_header.dart`, `plan_selector.dart:339,430` | Darken one step | flutter-mobile |
| L12 | Comparison table rows not labeled per column for screen readers | `premium_comparison_table.dart:98` | `Semantics(label: "Free: 1 a month. Premium: Unlimited.")` | flutter-mobile |
| L13 | Offer unselected radio ring 1.79:1 | `post_onboarding_offer_view.dart:419` | Use textSecondary | flutter-mobile |
| L14 | Stale comment says backend does not send `starter_pack` | `premium_status.dart:14-17` | Update comment | flutter-mobile |
| L15 | `usage_lastUsedHabit` not implemented | n/a | Build the habit note or drop the string from copy | flutter-mobile |
| L16 | Trial reminder eyebrow forced uppercase | `trial_reminder_sheet.dart:86` | Sentence case | flutter-mobile |
| L17 | Offer plan group has no group label | offer view | Wrap with `Semantics(label: ...)` | flutter-mobile |
| L18 | Reveal first-week plan has 2 rows, Build promises "Reflect, Between Sessions and a check-in" | `personal_reveal_view.dart:338-351`; `personal_build_view.dart:39` | Add the check-in row or adjust the Build string | flutter-mobile |
| L19 | Build live region re-reads all rows every second | `personal_build_view.dart:79` | Live region on the active row only | flutter-mobile |
| L20 | First-read block collapses at the deadline while the user may be reading | `personal_reveal_view.dart:67` | Keep the loading line or fade to the "appears in Character" line | flutter-mobile |
| L21 | Dead code and stale strings | `lib/screens/auth/widgets/welcome_bottom_button.dart`, `lib/l10n/parts/*.json` ("Success!", "DIVE IN"), duplicate next-session logic (`onboarding_schedule_view.dart:53-91` vs `onboarding_next_session.dart`) | Delete | flutter-mobile |
| L22 | Banned names remain in older strings outside the redesign | `app_en.arb`: `stats_healthCheckEmpty`, `character_sessionDebriefs`, `settings_therapyFocusInfo`, `settings_frustrationInfo`, `info_therapyTabBody`, `walkthrough_statsBody` ("progress snapshots"), unused `settings_premiumDescription` ("full export access") | Copy pass with brand-voice-manager; delete the unused key | flutter-mobile |
| L23 | `reflect_voice` and `monthly_audit` gates show the generic headline | `paywall_context.dart:104` | Copy decision (brand-voice-manager) | flutter-mobile |
| L24 | After a promo is accepted the user stays on the purchase paywall | `paywall_promo_section.dart:323-325`; `premium_status.dart:52-54` | Switch to the Premium (promo) view on success | flutter-mobile |
| L25 | Day-3 sheet "Keep Premium" reuses `trial_banner` trigger | `trial_popup_manager.dart:176-178` | Separate `trial_reminder_sheet` trigger mapped to the trial variant | flutter-mobile |

Smaller polish notes without their own ID: password visibility toggle without Semantics (`auth_body.dart:280-299`), hardcoded English semantics labels (`gender_pronouns_selector.dart:134,204`), orca fallback "Orca" in English (`therapy_onboarding_screen.dart:95`, `ms_routes.dart:524`), gender / pronouns as dropdowns with "Prefer not to say" last (`gender_pronouns_selector.dart:48-52`), 12-13 sp secondary lines on the offer and Build, custom session weeks away shown as weekday only on Build / Reveal, Reveal CTA busy up to about 7 s.

Missing tests worth adding (qa-testing or flutter-mobile): name propagation to Build / Reveal (H1), Welcome actions in flow mode (H2), notification entry gating (H3), resume at step 6 in therapy (M3), answer change clears schedule (M4), Reflect new-conversation gate, Getting started gate, sign-out / delete reset wiring, MainPageBody startup order, starter purchase single-handling (M2), offer error states (M7).

---

## Needs device QA (cannot be judged from code)

1. Starter purchase on the paywall and on the offer, iOS and Android: exactly one backend verify, one `purchase_completed`, Welcome once, logged `result` value, server `premium_source` and end date (M2).
2. Store cancel and payment failure for every offer and paywall option: spinner clears, cards stay, message shown (M7, L5).
3. iOS Restore on an account whose only subscription expired: does the screen wrongly say "Active"?
4. Welcome after an offer purchase: system back, Back to home, each start point; Android 14+ predictive back (H2).
5. Android system back and predictive back on every onboarding step (no PopScope).
6. Kill the app on onboarding steps 1, 3, 4, 5, 6 for both paths: counter, back target, post-onboarding variant (M3).
7. Name shown on Build / Reveal for email, Apple and Google sign-up, where the account name differs from the typed nickname (H1).
8. Reminders on iOS (not asked, provisional, denied) and Android 12 vs 13+ (never asked, denied once, permanently denied); after Not now and after a mid-flow kill, does Home cold-prompt next launch.
9. Slow network on the offer: does the starter card appear (M6). Slow network on the journey step with an immediate Skip (M17).
10. Trial bar, paywall chip, First-step chip and day-3 sheet with the device in UTC-7, UTC+2 and UTC+9 around trial end, incl. the bar hiding at 00:00 UTC (M9, L1).
11. Cold start from a push notification for a just-ended trial: paywall must not stack on the flow (M13). Legacy account with no push decision on a trial day: OS dialog vs sheet.
12. Free user at 0 tapping a prep or post-session notification (H3); after the last free recording, when the chip reaches 0 (M10).
13. Account delete, then new sign-up in the same process: no stale chips, popups still eligible (M12).
14. TalkBack and VoiceOver: Personalise name field and dropdowns, Art.9 checkbox, weekday row, offer and paywall radio groups, comparison table, First-step option tiles (label vs button merge), intensity bars, Build announcement noise.
15. Text at 130-200%: Home chips, sticky paywall CTA (fixed 56 dp, one line), comparison table fixed columns (84 / 96 dp), weekday row, Personalise dropdown row.
16. Reduced motion: Build, Reveal loading, AnimatedOrca on companion, screen transitions.
17. 12 h vs 24 h device setting and a Sunday-first locale on the schedule picker, week strip and reminder example timestamps.
18. Language auto-switch on the agreements screen for a non-English device on first run.
