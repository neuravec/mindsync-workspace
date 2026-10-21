# First voice conversation: UX, accessibility and mental-health review

Date: 2026-10-03. Reviewer: ui-ux-designer (read-only).
Scope: branch `feat/first-voice-conversation` in `mindsync-frontend/` (commits 2d8398e, c8492a5, f1a9644) against `SPEC.md` and the approved screens in `screens/` (Option B = `OfferStarterFirst` + `AllPlans`).
Files read: `lib/screens/first_conversation/**`, `lib/screens/wow/{wow_screen.dart, cubit/wow_cubit.dart, cubit/wow_state.dart, views/offer_step_view.dart, views/personal_reveal_view.dart}`, `lib/screens/subscription/{subscription_screen.dart, widgets/prices_failed_card.dart, widgets/paywall_header.dart, widgets/subscription_style.dart}`, `lib/screens/orca_memory/**`, `lib/screens/settings/settings_body.dart`, `lib/screens/audio_chat/{voice_tokens.dart, widgets/voice_shell.dart}`, `lib/l10n/app_en.arb`, `app_pl.arb` (plus the other 5 locales for the shared strings). All paths below are relative to `mindsync-frontend/mindsync_app/`.

## Verdict: GO with fixes

The build is faithful to the approved design in layout, hierarchy and copy almost everywhere, the copy is warm and dash-free, reduced motion is respected, and every state the spec asks for exists. It is not ready for the stores yet. Seven High items must land first: a gap in the crisis gate, the wait after End (empty in text mode), the missing close X on step 1, invalidating copy when the recap fails, a price that gets cut off on the purchase CTA, the hard-coded "five dollars" next to a store price, and the calm screen's support line. None of them is a Blocker for an internal TestFlight build. H1 (crisis gate) should still land before any external tester sees the flow.

## Fix list for flutter-mobile (prioritized)

| ID | Sev | Where | Problem | Exact fix |
|---|---|---|---|---|
| H1 | High | `lib/screens/first_conversation/cubit/first_conversation_cubit.dart:742` and `:746` | The "no offer after a crisis" gate reads only `recap.crisis`. If the text reply already flagged crisis (`state.crisisDetected`) but `/recap` fails or times out, the flow shows a priced offer right after a crisis conversation. | Line 742: `crisis: recap.crisis \|\| state.crisisDetected,`. Line 746 (catch): `result = handoff.copyWith(recapStatus: FirstConversationRecapStatus.failed, crisis: state.crisisDetected);`. Add a cubit test: text crisis + recap throws -> `handoff.crisis == true` -> `OfferMode.calm`. Backend flag for the lead: see "Backend capability" below (voice has no client-side crisis signal). |
| H2 | High | `lib/screens/first_conversation/views/first_conversation_view.dart:44-45`, `first_conversation_text_view.dart:59-73`, `first_conversation_voice_view.dart:33-35, 152, 189-203` | After End the person waits on the conversation screen for the final transcript, `/end`, `/recap` and the offer decision (typically a few seconds, worst case about 45-49 s). Text mode shows nothing at all, only greyed controls. Voice shows "Saving what you said" while the timer keeps ticking and the mute/keyboard buttons look live. | Add a `FirstConversationClosingView` for `ending` and `ended` in both modes (spec in section 4). Freeze and hide the timer, hide the phase indicator and the three controls, show the staged copy with a live region. |
| H3 | High | `lib/screens/wow/views/offer_step_view.dart:309-326` (header row), `:38-39` (doc), `lib/screens/wow/cubit/wow_cubit.dart` (new method), `lib/screens/wow/wow_screen.dart:276-283` | Step 1 has no close X. The approved `Paywall.dc.html` header (used by `OfferStarterFirst`) has one (`aria-label="Close and continue with the free trial"`). The only way forward is "Continue", and it opens a second paywall. Android system back does nothing on this step. | Restore the 44x44 X at the left of the header row for `starter`, `continueOnly` and `pricesFailed` (not `recapOnly`/`calm`). Semantics label = restored key `postOnboarding_closeA11y` ("Close and continue with the free trial", it exists in git at f27c589). Wire it to a new `WowCubit.closeOffer()` that logs `post_onboarding_offer_result` `result: closed_offer`, `offer_step: 1`, then `_goToPushOrFinish()`. Map system back on `offer` and `plans` to the same close actions. Reasoning in section 3. |
| H4 | High | `lib/screens/wow/views/offer_step_view.dart:384-390`, `app_*.arb` | `failed` (LLM error/timeout) and `ready` without items reuse "You kept it short, and that's fine." Someone who talked for 20 minutes would be told they kept it short, at the moment they most need to feel heard. | Branch on status: `short` keeps `postOnboarding_recapShort`. `failed` and `ready` without items use a new key `postOnboarding_recapFailed`: "Your conversation is saved. {orcaName} will pick up from here next time." (7 locales). |
| H5 | High | `lib/screens/subscription/widgets/subscription_style.dart:91-120` (`SubPrimaryButton`) | The button has a fixed `height: 56` and a one-line `TextOverflow.ellipsis` label. At default size, "Prolonger à 2 semaines pour 5,49 €" (FR) and "Przedłuż do 2 tygodni za 21,99 zł" (PL) already need about 300-320 dp against about 272 dp available on a 360 dp phone, so the price is cut off on a purchase button. At 200% text it happens in English too (WCAG 1.4.4). | Replace `SizedBox(height: 56)` with `ConstrainedBox(constraints: BoxConstraints(minHeight: 56))`, give the label `maxLines: 2, textAlign: TextAlign.center` without ellipsis, and add vertical padding 12. This is a shared widget, so re-run the paywall and onboarding widget tests. |
| H6 | High | `lib/l10n/app_en.arb:2182` (+ 6 locales), rendered at `offer_step_view.dart:629` | The body says "just for five dollars" in every locale, while the card shows the localized store price (for example 21,99 zł). A spoken price that disagrees with the charged price is misleading and a store-review risk. The string predates this batch, but it is now the main card of step 1. | EN: "Extend your four-day tryout to two weeks for just {price}. Most of our users feel like they got a second therapy session in that time." The second sentence stays verbatim. Add the `{price}` placeholder in all 7 locales and pass `starterProduct.price`. Needs the operator's OK because it is approved copy. |
| H7 | High | `lib/screens/wow/views/offer_step_view.dart:229-275`, keys `postOnboarding_calm*` | The calm screen is safe and non-alarming, but the support line goes straight from "someone you trust" to "emergency number". It skips crisis lines and, for people in therapy, their therapist, and it reads like body text instead of a findable support element. | Copy and layout in section 2. Same keys plus `postOnboarding_calmSupportTitle` and an in-therapy variant. |
| M1 | Medium | `lib/screens/first_conversation/cubit/first_conversation_cubit.dart:151-172` (`start`) | "Start talking", OS dialog, deny: the person lands in a text chat with no explanation. | In `start()`, after `_enterText()` when `entryPoint == firstConversationEntryMicDenied`, call `_notify(FirstConversationNotice.micNeeded)`. When permanently denied, add a `SnackBarAction` "Open settings" (`openAppSettings()`). |
| M2 | Medium | `lib/screens/first_conversation/views/first_conversation_text_view.dart:383-405` | The crisis line uses `error[50]` red and a warning triangle. That is alarming on a first conversation and goes against the calm palette. | Use the calm pattern of `therapy_onboarding/widgets/crisis_banner.dart`: `MsColors.primary[50]` fill, `primary[200]` border, `Icons.favorite_border_rounded` in `deepOcean`, ink text 14sp. Wrap it in `Semantics(liveRegion: true, container: true)`. |
| M3 | Medium | `lib/screens/audio_chat/widgets/voice_shell.dart:622-638` (`VoiceWordFadeText`) | Every transcript word is its own `Text`, so TalkBack/VoiceOver step through the transcript one word at a time. | Wrap it: `Semantics(label: widget.text, child: ExcludeSemantics(child: Wrap(...)))`. |
| M4 | Medium | `lib/screens/first_conversation/views/first_conversation_voice_view.dart:250-281`, `first_conversation_text_view.dart:245-266` | The phase indicator is read twice ("Opening question 1 of 3" from the bar, then "Getting to know you · 1 of 3 · This week") and phase changes are never announced. | Make it one node: `Semantics(container: true, liveRegion: true, label: <the visible phaseOpening string>, child: ExcludeSemantics(child: Column(bar, text)))`. Same for the open pill. |
| M5 | Medium | `lib/screens/audio_chat/widgets/voice_shell.dart:657-680` (`VoiceCircleButton`) | A disabled button (connecting, saving) looks and announces exactly like an active one. The mute toggle has no toggled state. | `Semantics(button: true, enabled: onPressed != null, toggled: <optional bool>, ...)`. Draw the icon at 40% opacity when `onPressed == null`. Add an optional `toggled` param, used by mute: `toggled: muted`. |
| M6 | Medium | `lib/screens/orca_memory/orca_memory_screen.dart:256-261`, `cubit/orca_memory_cubit.dart` (`deleteItem`) | A single delete is a hard delete with no confirmation and no undo. The card just disappears, and screen-reader users get no feedback and lose focus. | Keep it one tap, but defer the delete: hide the item, show `SnackBar("Note deleted", action: "Undo")` for 5 s, and call DELETE when the bar closes without Undo (or on dispose). Fire `orca_memory_item_deleted` on commit only and `orca_memory_delete_undone` (category) on Undo. The SnackBar text gives screen-reader feedback. |
| M7 | Medium | `lib/screens/orca_memory/orca_memory_screen.dart:142-145` | `SubStyle.muted` (#5A7A73) on the aquaBreeze page (#DBF0ED) is 3.96:1 for 14sp text. That fails 4.5:1. | Use `SubStyle.inkSoft` (#1E4043, 9.47:1). |
| M8 | Medium | `orca_memory_screen.dart:140`, keys `orcaMemory_*` | It does not say where the notes are used, and they are Art. 9 data. | Under the intro add `orcaMemory_usedFor`: "{orcaName} uses these notes in your conversations, your Before therapy cards and your Personal Bio." (wording matches SPEC 3.2). |
| M9 | Medium | `lib/screens/first_conversation/views/first_conversation_voice_view.dart:184-206` | The bottom row has 64 + End pill (44 dp padding each side) + 64 with no flex. With DE "Beenden" or FR "Terminer" at a 1.3x text scale on a 360 dp phone, the row overflows. | Wrap `VoiceEndButton` in `Flexible`, reduce its horizontal padding to 32 (design: 34), and put the label in `FittedBox(fit: BoxFit.scaleDown)`. |
| M10 | Medium | `lib/screens/subscription/widgets/prices_failed_card.dart:77-88` | `SizedBox(height: 44)` around "Mit meinen 4 kostenlosen Tagen weitermachen" (DE wraps to 2 lines) clips the text. | `ConstrainedBox(constraints: BoxConstraints(minHeight: 44))` plus `textAlign: TextAlign.center`. |
| M11 | Medium | `lib/screens/first_conversation/views/first_conversation_text_view.dart:315-381` | Bubbles do not say who is speaking, and the typing bubble is silent. | `_Bubble`: `Semantics(label: fromUser ? s.firstConversation_youSaidA11y(text) : s.firstConversation_orcaSaidA11y(orcaName, text), excludeSemantics: true)` (new keys "You: {text}", "{orcaName}: {text}"). `_TypingBubble`: `Semantics(liveRegion: true, label: s.firstConversation_orcaWritingA11y(orcaName))` ("{orcaName} is writing"). |
| L1 | Low | `lib/screens/subscription/widgets/paywall_header.dart:100` | The step 2 X is read as just "Close". Design: "Close and continue with the free trial". | For `PaywallVariant.onboarding` use `postOnboarding_closeA11y`. |
| L2 | Low | `lib/screens/first_conversation/views/first_conversation_voice_view.dart:237-243` | Mint text on the open pill is 4.42:1 over the gradient's inner stop (13sp). The design value is inherited. | Pill fill `VoiceTokens.mint.withValues(alpha: 0.10)` and text `VoiceTokens.onDark`, or keep the mint text with no fill. |
| L3 | Low | `lib/screens/first_conversation/views/first_conversation_voice_view.dart:285-323` | The "Orca remembers" chips are 4 separate screen-reader stops. | Wrap the `Wrap` in `MergeSemantics`. |
| L4 | Low | `lib/screens/first_conversation/views/first_conversation_voice_view.dart:35` | A silent reconnect mid-call shows "Connecting…". | New key `firstConversation_reconnecting`: "One moment, reconnecting…". |
| L5 | Low | `lib/screens/wow/cubit/wow_cubit.dart:518-523` | After the calm screen the flow asks for notification permission at once. A permission ask right after a hard disclosure feels transactional. | On `OfferMode.calm`, skip the pre-prompt: `PushPromptPolicy.clearSessionDeferral()` so the main page asks later, then `_finish()`. Log `push_prompt_result` `result: skipped_calm`. Operator decision. |
| L6 | Low | `lib/screens/wow/views/offer_step_view.dart:530` | After "Skip for now" (start failed, no conversation), benefit 1 reads "Talk like this whenever you need it". | When `recapStatus == none`, use a new key: "Talk with {orcaName} whenever you need it". |
| L7 | Low | `lib/screens/first_conversation/views/first_conversation_view.dart:86-96` | The text-mode start is a bare spinner (up to 20 s). | Add the orca mark and the line "Getting {orcaName} ready…" under it, centered, with liveRegion. |
| L8 | Low | `lib/screens/orca_memory/orca_memory_screen.dart` | Polish details. | Hide `orcaMemory_permanentNote` when the list is empty. Show the source per note ("From your first conversation", "From Reflect", using `item.source`). After "Forget everything" show the SnackBar "All notes deleted". Use skeleton cards instead of the spinner while loading. |
| L9 | Low | `lib/screens/first_conversation/views/first_conversation_voice_view.dart:41-45` | The design shows the person's words in italics while Orca is listening. | `fontStyle: FontStyle.italic` on the transcript when `ui == listening`. |
| L10 | Low | `SubStyle.muted` = `MsColors.textSecondary` #5A7A73 | The design's muted text is #3D5C60 (7.25:1 on white). The implementation sits at 4.70:1 on white and 4.62:1 on oceanMist: it passes, but barely. | Optional token alignment: `SubStyle.muted = Color(0xFF3D5C60)` (affects the paywall too, so do it as a separate small change). |
| L11 | Low | `app_pl.arb` (`reveal_talkCta`, `firstConversation_title`, `reveal_nextHeading`) | Custom companion names cannot be declined: "Porozmawiaj z Orca" should be "z Orcą". | Prefer nominative phrasing in PL, e.g. `reveal_talkCta`: "Zacznij rozmowę", `firstConversation_title`: "Pierwsza rozmowa · {orcaName}". |
| L12 | Low | `lib/l10n/app_en.arb` `reveal_nextTitle`, `reveal_talkHint` | "A 3-minute voice conversation" next to "As long as you like. You end it." on the intro. Design-approved, but the two set different expectations. | Optional: "About 3 minutes to start · You can stop anytime". |

## 1. Fidelity to the approved screens

| Screen / state | Status | Notes |
|---|---|---|
| 1 Reveal (`Main`) | Matches | Single CTA "Talk with {orcaName}" with mic icon and hint, the "Next: meet" card, week plan and tone card removed, focus footnote removed, first-read footnote updated. |
| 2 Intro (`VoiceIntro`) | Matches | Back 48 dp, ringed mark, title, lead (filled/general), 3 topics + "Then, talk about anything", privacy line with lock, "Start talking" with mic, mic hint, "Type instead". Topic variants for therapy, not in therapy and skipped are all correct. Gap: denying the mic gets no explanation (M1). |
| 3a-3d Voice phases (`VoiceLive`, `VoiceListening`, `VoiceWrapUp`, `VoiceOpen`) | Matches | Title + timer, 3 segments + "Getting to know you · n of 3 · topic", open pill, orb, state label, transcript, chips, mute/End/keyboard. Small differences: no italics on the person's words (L9), End pill padding 44 vs 34 (M9). |
| 3y Answers skipped (`VoiceNoAnswers`) | Matches | General topics, chips hidden. |
| 2x Text (`TypeFallback`) | Matches | Header with Voice pill and progress, "remembers" line under the first agent bubble, composer, "Finish for now". The Voice pill is 40 dp tall visually, but its tap target is padded to 48 (Material default, no global shrinkWrap). |
| 3x Connection lost (`VoiceError`) | Matches | Copy and both actions match. |
| Start failed (no design) | Acceptable | Calm card with "Try again" and "Skip for now". See L6 for what follows. |
| 4B step 1 recap: ready / short | Matches, one copy bug | Bullets, saved line by `saved_line_kind`, headline variants. `failed` wrongly reuses the short copy (H4). |
| 4B step 1 recap: writing | Built but effectively unreachable | `WowCubit.firstConversationFinished` waits up to 45 s for the recap before it shows step 1, and the recap itself gives up after about 40 s, so step 1 always gets the final status. The wait the design meant to cover with this state now happens on the conversation screen (H2, section 4). |
| 4B step 1 starter + Continue (`OfferStarterFirst`) | Matches except the X | Restore, benefits, starter card, legal links, CTA with price, billing line, outlined "Continue". The header's close X from the approved screen is missing (H3). Price copy issue (H6). |
| 4x Prices failed (`PaywallPricesFailed`) | Matches except the X | Card copy, "Try again", "Continue with my free 4 days". Hiding Restore here is reasonable (the store is unreachable). |
| 4B step 2 (`AllPlans`, entry onboarding) | Matches | Chip "Your free 4 days are on. Close to keep them." with the generic headline and subline. The flow's own prices-failed state has no header, which is acceptable. X label (L1). |
| Recap-only | Matches the spec | Dark header, recap card, "Continue", no prices, no Restore. |
| Calm (no design, lead decision) | Good base, copy to strengthen | Section 2. |

## 2. Calm screen after a crisis conversation

What works: there is no offer, no recap (good: replaying crisis content as "What Orca heard" could hurt), no red, no alarm language. The screen never says "we detected" anything, there are no numbers, the background is dark and quiet, and "Continue" is the only action. The body line "Take all the time you need. {orcaName} is here whenever you want to talk again." is right.

What to change:

1. The headline thanks the person for "talking with Orca", which puts the app at the center. It should acknowledge the person's courage without naming what was flagged.
2. The support line jumps from "someone you trust" to "your local emergency number" and leaves out the middle step that matters most: a crisis line, and the person's own therapist when they are in therapy. The existing in-chat banner already names crisis lines.
3. It is styled as one more paragraph. It should be a soft, findable card, not a warning.

Proposed copy (EN, no helpline numbers):

| Key | Copy |
|---|---|
| `postOnboarding_calmHeadline` | "Thank you for opening up." |
| `postOnboarding_calmHeadlineNamed` (new) | "Thank you for opening up, {name}." |
| `postOnboarding_calmBody` | unchanged: "Take all the time you need. {orcaName} is here whenever you want to talk again." |
| `postOnboarding_calmSupportTitle` (new) | "You don't have to carry it alone." |
| `postOnboarding_calmSupport` (not in therapy) | "If things feel like too much right now, reach out to someone you trust or a crisis line where you live. If you might be in danger, call your local emergency number." |
| `postOnboarding_calmSupportTherapy` (new, in therapy) | "If things feel like too much right now, reach out to someone you trust, your therapist, or a crisis line where you live. If you might be in danger, call your local emergency number." |
| `postOnboarding_calmHelplineLink` (new, optional) | "Find a helpline near you" opens `https://findahelpline.com` (international directory, so the app states no numbers). Needs operator and legal OK. The existing onboarding banner links to 988lifeline.org, which only covers the US. |

PL suggestion (gender-neutral; past-tense forms like "otworzyłeś" must be avoided): headline "Dziękujemy za Twoją szczerość.", support title "Wsparcie jest blisko.", support "Jeśli teraz jest Ci za ciężko, odezwij się do kogoś, komu ufasz, albo do telefonu zaufania w Twoim kraju. Jeśli grozi Ci niebezpieczeństwo, zadzwoń pod lokalny numer alarmowy." The in-therapy variant adds "do swojego terapeuty". The other locales get faithful translations.

Layout:

```
┌──────────────────────────────────┐
│ (56dp top)                       │
│ [Orca mark 48]                   │
│ Thank you for opening up, Ana.   │  26sp/800, white, header
│                                  │
│ Take all the time you need. Orca │  16sp/1.45, aquaBreeze
│ is here whenever you want to     │
│ talk again.                      │
│ ┌──────────────────────────────┐ │  support card: fill white 8%,
│ │ ♡  You don't have to carry   │ │  border aquaBreeze 30%, radius 16,
│ │    it alone.                 │ │  padding 16; heart icon mint 20dp
│ │    If things feel like too   │ │  title 16sp/700 white,
│ │    much right now, ...       │ │  body 15sp/1.45 aquaBreeze
│ │    Find a helpline near you  │ │  optional link, underlined, min 44dp
│ └──────────────────────────────┘ │
├──────────────────────────────────┤
│ [ Continue ]                     │  white bottom bar, as now
└──────────────────────────────────┘
```

Flutter notes: `Semantics(container: true)` on the card, so it is read as one unit after the body. Do not use a live region here, because the screen is already the focus target. Keep `Icons.favorite_border_rounded`, never a warning icon. The link uses `url_launcher` with `LaunchMode.externalApplication`. See L5 for skipping the reminder ask after this screen.

## 3. No close X on step 1: decision

Recommendation: restore the X, as on the approved screen (H3).

- Fidelity: the approved `Paywall.dc.html` header, which `OfferStarterFirst` renders with `layout="starterFirst"`, has the X with `aria-label="Close and continue with the free trial"`. Dropping it was an implementation decision, not part of what the operator approved.
- Ethics: the person has just opened up to Orca. If the only visible way on is "Continue", and "Continue" opens a second, bigger paywall, the flow turns into two sales screens in a row before they can leave. That is not a trap, because step 2 has an X, but in the most vulnerable moment of the flow it feels like one. The button label adds to it: "Continue" usually means "go on into the app".
- Android: system back is blocked on this step (`PopScope(canPop: false)`, and `backToReveal` is a no-op here). Without an X, there is no dismiss gesture at all.
- Store review: a hard-to-dismiss paywall in onboarding is a frequent reason reviewers push back. A visible X on each paywall screen removes that risk at no cost.
- Funnel: an X does not take the "see all plans" path away. "Continue" stays the outlined secondary action, exactly as approved. If the lead wants to measure the cost, `post_onboarding_offer_result` with `result: closed_offer` and `offer_step: 1` (new enum value, plus its test) shows how many people leave at step 1 instead of at step 2. Today that leak is hidden inside `closed_plans`, so the funnel reads worse than it is.

If the lead still decides against the X, the minimum honest version is to rename "Continue" to "See all plans" and add the design's "Continue with my free 4 days" text link under it. That is a copy change the operator would need to approve.

## 4. What the person sees between End and step 1

Today: End, then `ending` (waiting up to 5 s for the final transcript), then `ended` with the recap still running. After that comes `/end` (cap 20 s), then `/recap` (cap 20 s), then the profile read and the product probe (cap 4 s), and only then step 1. The typical wait is a few seconds. The worst case is about 45-49 s. The whole time the conversation screen stays up:

- Voice: the orb, the label "Saving what you said", a timer that keeps counting (it looks as if the call is still running), the phase indicator, End greyed out, and mute and keyboard buttons that look active but do nothing.
- Text: the chat with a disabled field and a disabled "Finish for now", with no label at all. This is the main problem: nothing tells the person their End was registered.

Proposal: `FirstConversationClosingView`, shown for `ending` and `ended` in both modes until the offer step replaces it.

```
┌──────────────────────────────────┐
│ First conversation with Orca     │  title only: timer stopped and hidden,
│                                  │  phase indicator hidden
│                                  │
│          ( calm orb )            │  VoiceOrb(calm) on the dark gradient
│                                  │  (text mode: _RingedMark on oceanMist)
│      Saving what you said        │  stage A: status line, 15sp/600
│                                  │
│   ▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭              │  stage B: 3 soft lines (as in
│   ▭▭▭▭▭▭▭▭▭▭▭▭                  │  _RecapWriting), 12dp, radius 6,
│   ▭▭▭▭▭▭▭▭▭▭▭▭▭▭                │  white 12% (dark) / #E3F2EF (light)
│                                  │
│   This can take a few more       │  stage C (after 12 s): 15sp/1.45,
│   seconds. Everything you said   │  muted on the ground
│   is already saved.              │
│                                  │
│   (64dp empty band, no buttons)  │  keeps the layout from jumping
└──────────────────────────────────┘
```

Stages and copy:

| Stage | When | Status line |
|---|---|---|
| A | `view == ending` | existing `firstConversation_saving`: "Saving what you said" |
| B | `view == ended` and `handoff.recapStatus == writing` (and after the recap lands, until the offer step shows) | existing `postOnboarding_recapWriting`: "{orcaName} is writing up what it heard…" plus the 3 lines |
| C | 12 s after End, added under B | new `firstConversation_closingSlow`: "This can take a few more seconds. Everything you said is already saved." |

Flutter notes:

- In `FirstConversationView` (`first_conversation_view.dart:44-45`), route `ending` and `ended` to the new view for both `voiceMode` values, and drop the `saving` branch from the voice view. The new view reads `voiceMode` for its ground.
- Stage C runs on a local `Timer` started in `initState`, which needs no cubit change. The status line sits in `Semantics(liveRegion: true)`, so each stage is announced once. Exclude the skeleton lines from semantics.
- Orb motion follows `disableAnimations` (already supported). No spinner.
- No escape button: the hard cap is about 49 s, and an early exit would have to skip the offer anyway, because nothing priced may show before the crisis flag is known.
- PostHog: no new event is needed. `first_conversation_recap_result.latency_ms` already measures this wait.

## 5. "What Orca remembers"

| Aspect | Assessment |
|---|---|
| Clarity | Good. The title, the intro ("short notes ... so the next one can pick up where you left off") and the permanence note are plain and warm. Missing: where the notes are used (M8). |
| Trust | Category pills and a saved date help. Show the source too ("From your first conversation") (L8). The permanence note is right. Fix its contrast (M7). |
| Delete one | One tap, hard delete, no undo, no feedback, focus lost (M6). A confirmation dialog per note would be too much friction. A 5 s undo with a deferred commit is the right balance. |
| Forget everything | Good: in-app sheet, honest copy ("This can't be undone, and later conversations will start without them."), a safe "Keep my notes" option, and a cancel event. Red for the destructive action is acceptable here (platform convention), and the sheet's button is 56 dp. Add the "All notes deleted" confirmation (L8). |
| Empty | Good copy: "Nothing here yet" / "After you talk with {orcaName}, the things worth remembering will show up here." Hide the permanence note in this state (L8). |
| Unavailable (503/404) | Calm and final, never an error loop: "Not available yet" / "... There's nothing you need to do." Good. |
| Error | "This didn't load" / "Check your connection and try again." + "Try again". Good. |
| Loading | Spinner. Skeleton cards would be calmer (L8). |
| Targets | Back 48, delete 48, Forget 52, sheet 56/48. All pass. |

## 6. Accessibility

Contrast (WCAG 2.1, computed on the actual tokens):

| Pair | Ratio | Result |
|---|---|---|
| Transcript (white 92%) on gradient #1B584B / #0F3D33 | 7.30 / 10.46 | Pass |
| State and phase label mint #A6E8D8 on #1B584B | 5.96 | Pass |
| Mint on the open pill (14% mint over #1B584B) | 4.42 | Fail by a little at 13sp (L2) |
| Timer and chip label (white 70%) on #1B584B | 4.99 | Pass |
| Chip text white on 12% chip | 6.04 | Pass |
| Ink on disabled End (55% white) | 4.82 | Pass |
| Muted #5A7A73 on white / oceanMist | 4.70 / 4.62 | Pass, barely (L10) |
| Muted #5A7A73 on aquaBreeze (memory page) | 3.96 | Fail (M7) |
| Accent #26767B eyebrow on white / category pill on tint | 5.30 / 5.04 | Pass |
| Starter body #421F06 / terms #844B0F on sandBeige | 13.03 / 6.23 | Pass |
| Calm body aquaBreeze on deepOcean | 11.53 | Pass |
| Text field border #BBE4DE on white (non-text) | 1.35 | Below 3:1. Design-inherited; the hint text identifies the field. Low, no action required. |

Touch targets: every interactive element is at least 44 dp (most are 48 or more). The Voice pill in text mode is 40 dp visually but has a padded 48 dp target. The step 1 X, once restored (H3), must be 44 x 44 as in the design.

Semantics labels on icon buttons: mute/unmute, switch to text, send, back and delete are all labelled. Gaps: disabled state not exposed (M5), duplicate phase reading (M4), a word-by-word transcript (M3), speakers missing in text bubbles (M11), the generic step 2 close label (L1).

Screen-reader order on the voice screen (after M3, M4 and L3): title (header) -> timer -> phase (one node, live region) -> state label -> transcript (one node) -> "Orca remembers: ..." (one node) -> Mute -> End -> Switch to text. This order is logical. Do not make the speaking/listening label a live region: with VoiceOver on, it would talk over Orca. Only the closing stages (H2) and phase changes (M4) are announced.

Text scaling: there is no global clamp, so system sizes apply in full. Problems: the CTA truncates (H5), the End row overflows (M9), the prices-failed link clips (M10). Every other screen scrolls and handles 200%.

Reduced motion: the orb, the word fade, the step `AnimatedSwitcher` and the recap switcher all honor `disableAnimations`. Pass.

## 7. Copy rules

- U+2014 / U+2013: zero hits in all lines added by the 3 commits (`lib/` and `test/`, generated files included) and zero hits in the values of every new key in all 7 locales. Pass.
- The verbatim sentence "Most of our users feel like they got a second therapy session" is present in `postOnboarding_offerStarterBody` (`app_en.arb:2182`) and rendered on step 1 (`offer_step_view.dart:629`). Pass. The DE/ES/FR/NB/SV/PL translations are faithful. The "five dollars" part of the same string must change (H6). The verbatim sentence does not.
- Tone (EN): warm, short, human, no clinical words, no shame. Errors are calm ("That didn't send. Please try again.", "That didn't go through. Please try again in a moment."). The exceptions are H4 (invalidating copy on a failed recap) and H7 (the calm support line).
- Tone (PL): natural and consistently informal (Ty), capitalized Ty forms, no gendered verbs in the new strings. Notes: `postOnboarding_calmHeadline` "Dziękujemy za tę rozmowę." reads as a corporate "we" (replaced by the section 2 proposal), and companion-name declension (L11). `postOnboarding_recapEyebrow` "Co {orcaName} zapamiętuje" sidesteps the gendered past tense of "heard". That was a good choice.

## PostHog coverage for the proposed changes (for the closing table)

| Surface | Action | Event | Key properties | Where |
|---|---|---|---|---|
| Step 1 | close X (H3) | `post_onboarding_offer_result` | `result: closed_offer`, `offer_step: 1`, `dwell_ms` | `wow_cubit.dart` new `closeOffer()` |
| Calm | helpline link (H7, optional) | `support_resource_tapped` (new) | `surface: post_onboarding_calm` | `offer_step_view.dart` |
| Calm | reminders skipped (L5, optional) | `push_prompt_result` | `result: skipped_calm`, `variant` | `wow_cubit.dart` |
| Memory | undo delete (M6) | `orca_memory_delete_undone` (new) | `category` | `orca_memory_cubit.dart` |
| Closing view (H2) | none needed | covered by `first_conversation_recap_result.latency_ms` | | |

No free text: the undo and link events carry enums only.

## Backend capability to flag to the lead

Voice has no client-side crisis signal. If `/recap` fails or times out after a voice conversation that touched crisis content, the client cannot know, and the offer shows. Ask data-analytics (BE-B1 owner) to (a) return `crisis` from `/reflect/{id}/end` as well, or (b) have `/recap` return `crisis` even with `status: failed`, computed from the stored message-level flags without the LLM call. The client would then read it in the `/end` call in `_finishThread` (`first_conversation_cubit.dart:721`).
