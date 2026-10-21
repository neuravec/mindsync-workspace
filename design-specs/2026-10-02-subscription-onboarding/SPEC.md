# Subscription + onboarding redesign: implementation spec (2026-10-02)

Approved by the operator on 2026-10-02 ("jest ok, implementuj end2end").
Design canvas: https://claude.ai/artifact/6ajEsLgFccV8oZkvEwP2Cp
Screen sources (HTML mockups, one per screen): `screens/*.dc.html` in this folder.
Final English copy: `copy-en.md` in this folder (written by brand-voice-manager; when it exists it WINS over the text inside the mockups).

The mockups are the visual and structural direction. They are not pixel contracts. Use the app's existing tokens (`MsColors`, `MsStyles`, Figtree) and existing widgets where they fit.

## 0. Ground rules for every implementing agent

1. No commit, no push, no deploy. Work on branch `feat/subscription-onboarding-redesign` (create it from the current branch if it does not exist). Backend repo = `MindSync/` (push to main auto-deploys to Heroku, so never push). Frontend repo = `mindsync-frontend/` (push to dev triggers TestFlight, so never push).
2. Do not touch unrelated dirty files (`mindsync_app/test/marketing_shots/*`, `.claude/agent-memory/*`, `test_temp.db`).
3. CLAUDE.md "Change Safety & Impact Recon" applies. Report the blast radius in your final message.
4. Sign-up and onboarding are the most fragile flows in the app (see past incidents: half-created account lockout, legal gate bug, H10). Keep every existing data write, consent call, analytics event and cubit contract working. Restyle and re-sequence views; do not rewrite persistence.
5. Do not drop existing data fields that a mockup happens to omit: therapy duration chips, goal text + crisis banner, orca color picker, custom session calendar, "add your own" focus area, self-describe gender, language change on the agreements screen.
6. Typography rule for all user-facing text and docs: never use the em dash (U+2014) or en dash (U+2013). Rewrite the sentence instead.
7. Feature names are fixed: "Before therapy", "After therapy", "Between Sessions", "Reflect", "Mood & symptom trends", "Weekly therapy summary", "Monthly therapy summary", "Therapy Relationship", "Character". Never "debrief", "progress snapshots", "therapy tracking", "AI goal narratives".
8. The orca visual is the logo mark (`assets/svg/logo.svg`, same shape as `orcs_new.svg` / `AnimatedOrca`). Use the existing `AnimatedOrca` or the logo tinted; do not add new illustration assets.
9. Tests are mandatory in the same task. Flutter: run `flutter test` per directory only (full suite OOMs), filter analyze output by `error •`. Known pre-existing failures are not regressions (baseline: 21 BE + 30 FE).
10. l10n: every new string goes to `app_en.arb` and all other locale arb files (7 languages total), then `flutter gen-l10n`; generated files are committed with the change later.

## 1. Product decisions (settled)

- Trial: every new account keeps the server-granted 4-day Premium trial, no card (`_create_initial_subscription(db, uid, 4)`). Not changed.
- Post-onboarding offer = option A: server trial stays, the offer screen sells (a) starter pack "Extend to 2 weeks" for $5 (`ms_starter_package`, one-time, preselected), (b) Annual, (c) Monthly. Skippable. Option B (store trial) is NOT built.
- New Free limits per calendar month (reset on the 1st, same month window the backend uses today):
  - Before therapy: 1
  - After therapy: 1
  - Between Sessions: 3
  - Reflect messages: 15 (was 30)
  - Session recordings: 2 in total (unchanged)
  - Habits: 1 active (unchanged)
- Existing users are NOT notified about the limit change (operator decision).
- Usage counters are shown to Free users on each limited feature; trial shows "Unlimited in trial"; Premium shows nothing. At 0 the entry opens the paywall.
- Goal progress story, Therapy Relationship, Weekly therapy summary, Mood & symptom trends are NOT premium differentiators (not gated in the app). They must not appear as "Premium only".
- "Full data export" must not be promised anywhere (feature does not exist).
- Operator-mandated copy, keep verbatim:
  - First-step buttons: "Talk with {orcaName} about your therapy & wellbeing" (Reflect), "Get a summary of how you feel with Between Sessions" (Between Sessions), "Check the health of your Therapy Relationship" (health check). "Capture a past session" stays.
  - Explainer under the buttons, with a dot: "Leaving a short voice note will let us analyze what's going on and give you helpful tips on your therapy progress."
  - Starter card on the offer: "Extend your four-day tryout to two weeks, just for five dollars. Most of our users feel like they got a second therapy session in that time."

## 2. Backend (backend-api) : contract

### 2.1 Per-feature free limits
Today `count_ai_notes_this_month` (crud) is one shared pool of 5 for debriefs + prep cards + between-session notes, checked via `_therapy_helpers`. Split into per-type counting and per-type limits in `app/core/config.py`:
`FREE_TIER_MONTHLY_PREP_LIMIT=1`, `FREE_TIER_MONTHLY_DEBRIEF_LIMIT=1`, `FREE_TIER_MONTHLY_BETWEEN_SESSIONS_LIMIT=3`, `REFLECT_MONTHLY_MESSAGE_LIMIT=15`.
Check `.env` (tracked in git, shipped in the slug) and Heroku-config assumptions for overrides of these keys. Gate semantics stay: the last allowed use succeeds, the next attempt gets the existing 403. Trial and premium users are unlimited as today. Auto-generated prep cards (`prep_card_auto_generate`) must keep their current eligibility rules; say in the report whether an auto card consumes the Before therapy allowance and keep whatever is least surprising (recommended: auto cards for free users are not generated today, so nothing changes).

### 2.2 `GET /api/v1/users/usage` (new, auth required, own data only)
```json
{
  "plan": "free",                 // "premium" | "trial" | "free"
  "trial_ends_at": null,          // ISO 8601 UTC when plan == "trial", else null
  "resets_at": "2026-11-01T00:00:00Z",
  "features": {
    "before_therapy":    {"used": 0,  "limit": 1,  "period": "month"},
    "after_therapy":     {"used": 1,  "limit": 1,  "period": "month"},
    "between_sessions":  {"used": 1,  "limit": 3,  "period": "month"},
    "reflect_messages":  {"used": 3,  "limit": 15, "period": "month"},
    "session_recordings":{"used": 1,  "limit": 2,  "period": "lifetime"},
    "habits":            {"used": 1,  "limit": 1,  "period": "active"}
  }
}
```
`limit` is `null` for trial and premium. `plan == "trial"` means premium granted by the sign-up trial (see `UserSubscription.granted_via` / `premium_source`), `"premium"` means store purchase, promo, or starter pack. `used` must use exactly the same counting functions as the gates, so the chip and the 403 never disagree. Cheap queries only (this is called on Home load).

### 2.3 Trial analytics
PostHog events from the backend: `trial_started` when the initial subscription is created (props: days, platform), `trial_ended` when the hourly expiry job deactivates a sign-up trial that did not convert. Idempotent, no duplicates on retries.

### 2.4 Starter pack semantics
Verify what `POST /users/one_time_purchase` grants for `ms_starter_package`. Target: Premium until `purchase_time + 14 days`, never shorter than the access the user already has. Bought on day 0 of the trial it yields about two weeks total. If the current behavior differs, fix it with tests; if it already matches, just add the missing test.

No DB migration is expected. If you find you need one, stop and report.

## 3. Frontend (flutter-mobile) : work packages, in this order

### FE-A Subscription screens (`lib/screens/subscription/`)
Mockups: `Main` (paywall, variants via entry context), `PaywallLimit`, `PaywallTrial`, `Welcome` (after purchase), `Premium` (active, manage), reference `BeforePaywall` / `BeforePremium` = today.
- Header: close X (left), Restore (right). Eyebrow "MindSync Premium", headline + subline depend on entry context derived from the existing `trigger_feature`: `premium_gate_*` → "limit" variant with a chip naming the exhausted feature; `trial_ended_popup` / `trial_banner` → "trial" variant; everything else → generic.
- Plan selector: Annual (preselected, "Save N%" badge computed from store prices as today, fallback "Best value") and Monthly, as radio cards. No struck-through anchor price.
- "Cancel anytime in your store account." line.
- Comparison table "What Premium changes": rows Before therapy 1 a month / Unlimited; After therapy 1 a month / Unlimited; Between Sessions 3 a month / Unlimited; Session recordings 2 in total / Unlimited; Reflect messages 15 a month / Unlimited; Reflect voice mode Locked / Included; Habit tracker 1 habit / Unlimited; Monthly therapy summary Activity only / Full summary; Weekly therapy summary Included / Included; Mood & symptom trends Included / Included. Footnote: "Free limits reset on the 1st of every month. You always see how many you have left."
- Starter pack as a quiet dashed card ("Not ready to commit? Try 14 days of Premium for {price}." + "Try it"), hidden when the product fails to load. Promo code collapsed behind "Have a promo code?" (same SettingsCubit calls as today).
- Sticky bottom bar: CTA "Continue with Annual" / "Continue with Monthly", busy state, billing line "Billed {price} once a year. Renews automatically, cancel anytime." / monthly equivalent.
- After a successful purchase: `Welcome` screen (three starting points, primary "Open After therapy", secondary "Back to home").
- Premium active view: plan card (plan name, renewal / trial end / promo end date, billed through store), "Manage subscription" (opens store subscription management), included list (Unlimited Before therapy & After therapy, Unlimited session recordings, Unlimited Reflect messages, Reflect voice mode, Unlimited habits, Full monthly therapy summary), Restore, legal links. Variants by `premium_source`: store, sign-up trial ("Choose a plan"), promo ("See plans").
- Keep all existing analytics (paywall_shown, product selected, purchase events, restore).

### FE-B Welcome, account, name (`lib/screens/welcome`, `auth`, `sign_up`)
Mockups: `OB01Welcome`, `OB02Account`, `OB03Personalise`.
- Welcome: dark background, logo, headline + subline, "Get started" (sign-up), "I already have an account" (log in), legal links.
- Account: platform social button first (Apple on iOS, Google on Android), then email + password + age/terms checkbox, "Create account".
- Name screen: name is the main field; age range, gender, pronouns optional below. Enforce nothing new server-side; if the name is empty the app falls back to a neutral greeting.
- Remove the "Success!" screen (4 s wait, wrong "log in page" copy): go straight to therapy onboarding after account creation (email path still passes through CheckEmail).
- Fix: Google/Apple sign-in of an EXISTING account must run the same onboarding-completed check as the splash (today it jumps to the main page).
- Do not change what is sent to the backend at sign-up.

### FE-C Therapy onboarding (`lib/screens/therapy_onboarding/`)
Mockups: `OB04Legal` … `OB11Source`.
- The "DIVE IN" splash is merged into the agreements screen (greeting with the user's name + what is coming). Agreements keep both checkboxes, the disclaimer card, privacy link and language change; consent writes are unchanged.
- Steps 1-7 restyled with the new copy: focus areas (chips + add your own, button shows the count), intensity (sliders 1-10 with big value), therapy status (Art.9 consent first; options only after consent; duration chips and goal only for yes_regular / yes_occasional), therapy type, next session (weekday row, time, frequency incl. existing custom calendar, "next session" confirmation line), companion (name, talk style with a live sample line per archetype, color picker kept), lead source ("Set up my app").
- Branching: when the user is not in therapy (not_right_now / never_been) or did not give Art.9 consent, skip "therapy type" and "next session"; the progress indicator then counts 5 steps instead of 7. `onboarding_step` values and step analytics names (`_stepNames`) stay stable for dashboards; skipped steps simply are not viewed.
- Time formatting follows the device locale (12 h / 24 h).

### FE-D After onboarding (`lib/screens/wow/` and new screens)
Mockups: `PersonalBuild`, `PersonalReveal`, `PostOnboarding` (offer), `OB15Push`, `FlowFirstStep`.
Sequence after the last onboarding step: Build (about 4 s, four steps ticking, replaces the Wow spinner; it still waits for the same API calls the Wow screen makes) → Reveal ("{name}, your MindSync is ready.": focus areas with intensity bars (map 1-10 to 5 bars), "Your week with MindSync" strip + three plan rows from the saved schedule, "{orcaName}'s first read on you" from the starter bio "patterns" section with a soft loading state and graceful absence, talk style; CTA "Let's start") → Offer (only when: just finished onboarding, not premium from a store purchase, store products loaded; otherwise skipped; shown once per account; `paywall_shown` with `trigger_feature = post_onboarding`; purchase success → FE-A Welcome screen → continue) → Reminders pre-prompt (two example notifications, "Turn on reminders" triggers the OS permission request that today fires cold on the main page; "Not now" skips; the main page must no longer auto-prompt for new users, existing users keep current behavior) → First step (trial chip, "Capture a past session" for users in therapy, the three operator-mandated buttons, the voice-note explainer, "Take me to the app").
- Not in therapy / no schedule: the Reveal week strip becomes "Your first week" with Reflect, Between Sessions and a check-in.
- The reminders example for after a session must describe a notification that really exists in the notification moments; if there is none, use an existing one (for example the prep reminder plus a check-in reminder) and say so in the report.
- The 7-slide app tour no longer opens automatically for accounts that went through this flow (still available from Settings).
- New events: `personal_reveal_viewed`, `post_onboarding_offer_result` (purchased_starter / purchased_annual / purchased_monthly / skipped), `push_prompt_result` (accepted / declined / not_now). Keep `first_capture_prompt_*` events on the first-step screen.

### FE-E Trial visibility and usage counters
Mockups: `CountersHome`, `CountersReflect`, `CountersStates`, `FlowHomeTrial`, `FlowTrialReminder`.
- API client + repository + cubit for `GET /users/usage` (section 2.2). Refresh on Home load and after each gated action.
- Chips per `CountersStates`: "N of M left", "Last one this month" / "1 free this month", "0 left · Premium" (tap opens paywall with `premium_gate_<feature>`), "Unlimited in trial", hidden for premium. Place them on the real entry points of Before therapy, After therapy, Between Sessions, Reflect, session recording. Reflect keeps its existing indicator, restyled, with the 15 limit coming from the API (no hardcoded 30).
- Home trial bar during the sign-up trial: "Premium trial: N days left" + progress + "See plans" → paywall (`trigger_feature = trial_banner`).
- Day 3 of the trial, first app open: bottom sheet "Your Premium trial ends tomorrow" with usage numbers and the Free limits, "Keep Premium" → paywall, "Not now". Once.
- First open after the trial ended without purchase: paywall in the "trial" variant (`trigger_feature = trial_ended_popup`), once. Wire through the existing `TrialPopupManager` (today nothing calls it); remove or adapt its dead paths.
- A backend error or missing usage data must degrade to "no chips", never to a blocked feature or a wrong paywall.

## 4. Order and ownership
1. brand-voice-manager: `copy-en.md` (all screens, humanized, keeps operator-mandated strings).
2. backend-api: section 2 (parallel with 1).
3. flutter-mobile: FE-A → FE-B → FE-C → FE-D → FE-E, one after another (shared arb files).
4. qa-testing: full regression of both repos; security-guardian: review of `GET /users/usage` and the offer/trial paths before any deploy.
5. Deploy only on explicit operator approval. Backend first (no migration expected), then frontend to dev (TestFlight).

## 5. Backend facts after implementation (2026-10-02, for FE-D / FE-E)

- `GET /api/v1/users/usage` exists exactly as in 2.2. `plan`: `free` | `trial` (premium with `granted_via == "signup_trial"`) | `premium` (purchase, promo, starter pack, legacy). `trial_ends_at` = subscription `end_date` at 00:00 UTC. Errors return 500 `usage_unavailable`; the client must degrade to "no chips".
- At the limit the create endpoints for After therapy, Before therapy and Between Sessions do NOT return 403. They save the entry as `processing_status: "plain_text"` (no AI summary). The 403s exist only on `/retry` and prep `/auto-generate`. Reflect returns 403 `monthly_limit_reached`. So the paywall at 0 is a CLIENT gate: when the chip shows 0, tapping the entry opens the paywall (`premium_gate_<feature>`) instead of the flow (operator decision: "after the counters hit zero the paywall appears"). Closing the paywall returns the user to where they were. Reading existing entries is never gated.
- Auto-generated Before therapy cards (trial/premium only) do not count toward the free allowance.
- Reflect: `/reflect/usage` now reports limit 15. `messagesLimit - messagesUsed` can be negative for users who already used more than 15 this month: clamp to 0 in the UI.
- Starter pack: server forces 14 days from purchase for `ms_starter_package` and never shortens existing access.
- `trial_started` / `trial_ended` are emitted by the backend; do not duplicate them on the client.
- `premium_source` can now be `"starter_pack"` (verified `ms_starter_package` purchase that sets or extends access; also relabels kept `signup_trial` / `promo` access, because a payer is never labelled as trial or promo). A later store subscription overwrites it with `"purchase"`. `/users/usage` reports `plan = "premium"` for it.
- Deploy note: client builds already in users' hands (dev a9856205 and older) show the paywall instead of the premium view to a `starter_pack` user on the subscription screen (`premiumSource == 'purchase' || null`). Access is unaffected (server-side gates). Accepted: it works as an upsell until the new client ships.

## 6. Closing stages (operator request 2026-10-02, after FE-E)

1. Design conformance: every implemented screen is compared with its mockup and `copy-en.md` (structure, states, copy, branches). Deviations are listed and either fixed or accepted.
2. Logic verification: full flow walkthrough in code and tests (sign-up paths, 5-step and 7-step onboarding, offer branches, reminders, first step, trial bar, day-3 sheet, trial-ended paywall, counters at N / 1 / 0, error degradation), plus full regression of both repos.
3. PostHog coverage audit per the new CLAUDE.md rule "PostHog Instrumentation (Mandatory final step)": one coverage table for the whole batch (surface | user action | event | properties | file). Every gap gets an event, a test, and the funnel must be reconstructable from Welcome to purchase / skip. No free text in events.
4. Security review of `GET /users/usage`, the offer and trial paths.
