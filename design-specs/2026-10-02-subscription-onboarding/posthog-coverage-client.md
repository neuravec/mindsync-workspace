# PostHog coverage, client side: subscription + onboarding redesign (FE-FIX-2, 2026-10-02)

Scope: every client surface of the 2026-10-02 batch, after FE-FIX-1 and FE-FIX-2, on branch `feat/subscription-onboarding-redesign` (uncommitted). Backend events are listed only where a client funnel step depends on them.

Paths: `lib/...` and `test/...` are relative to `mindsync-frontend/mindsync_app/`. Event and property names are constants in `lib/core/analytics/analytics_events.dart`. Every event below goes through `AnalyticsEvents.logEvent` (PostHog + Firebase). Shared recorder for new tests: `test/support/posthog_capture.dart`.

Privacy rule applied to the whole table: counts, enums, booleans and durations only. No typed text (name, email, password, custom focus area, goal, orca name, lead source "Other", promo code), no therapy status property (`in_therapy`, `has_schedule` removed per security M-3), no error messages (error class names only).

## 1. Coverage table

| surface | user action | event name | key properties | where it fires (file) | test |
|---|---|---|---|---|---|
| Welcome | Screen viewed | `$screen` (welcome) | `$screen_name` | navigation/ms_routes.dart (PosthogObserver) | navigation tests (observer) |
| Welcome | Tap "Get started" | `welcome_cta_tapped` | `cta=sign_up` | screens/welcome/welcome_body.dart | test/screens/welcome/welcome_body_test.dart |
| Welcome | Tap "I already have an account" | `welcome_cta_tapped` | `cta=log_in` | screens/welcome/welcome_body.dart | test/screens/welcome/welcome_body_test.dart |
| Welcome | Tap Terms / Privacy | `legal_link_opened` | `surface=welcome`, `link=terms/privacy` | screens/welcome/welcome_body.dart | test/screens/welcome/welcome_body_test.dart |
| Account | Screen viewed | `$screen` (auth) | mode from `welcome_cta_tapped` | navigation/ms_routes.dart | navigation tests |
| Account | Switch Create account / Log in | `auth_mode_switched` | `to=sign_up/log_in` | screens/auth/auth_body.dart | test/screens/auth/auth_body_test.dart |
| Account | Tap Apple / Google | `auth_method_tapped` | `mode`, `method=apple/google` | screens/auth/widgets/animated_widgets/animated_google_apple_widgets.dart | test/screens/auth/auth_body_test.dart |
| Account | Tap the primary CTA with a valid form | `auth_method_tapped` | `mode`, `method=email` | screens/auth/auth_body.dart | test/screens/auth/auth_body_test.dart |
| Account | Validation error | `auth_validation_failed` | `mode`, `reason=email_empty/email_invalid/password_empty/password_short/terms_not_accepted` | screens/auth/auth_body.dart | test/screens/auth/auth_body_test.dart |
| Account | Log in success (email, Google, Apple) | `user_logged_in` | `auth_provider`, `platform` | screens/auth/cubit/auth_cubit.dart | test/screens/auth/auth_cubit_analytics_test.dart (email) |
| Account | Log in failure | `login_failed` | `method=email/google/apple`, `error_type=invalid_credentials/email_not_verified/cancelled/network/unknown` | screens/auth/cubit/auth_cubit.dart, managers/auth_manager.dart, managers/auth_failure_type.dart | test/screens/auth/auth_cubit_analytics_test.dart (email paths + classifier) |
| Account | Forgot password | `password_reset_requested`, `password_reset_failed` | none | screens/forgot_password/cubit/forgot_password_cubit.dart (unchanged) | none (pre-existing, outside this batch) |
| Name | Screen viewed (only when the name step is really shown) | `onboarding_step_viewed` (+ `$screen` signUp) | `step_index=-1`, `step_name=personalise` | screens/sign_up/cubit/sign_up_cubit.dart (`checkIfUserIsRegistered(false)`) | test/screens/sign_up/personalise_step_analytics_test.dart |
| Name | Tap Continue | `onboarding_step_completed`, `signup_started`, `signup_method_selected` | `step_index=-1`, `duration_seconds`; `method=email/oauth` | screens/sign_up/cubit/sign_up_cubit.dart | test/screens/sign_up/sign_up_analytics_fe_fix2_test.dart, personalise_step_analytics_test.dart |
| Name | Registration failed (email and OAuth) | `signup_failed` | `error_type=register_failed/login_failed/no_current_user/backend_provisioning_failed`, `method=email/oauth` | screens/sign_up/cubit/sign_up_cubit.dart | test/screens/sign_up/sign_up_analytics_fe_fix2_test.dart |
| Name | Optional age, gender, pronouns | person properties via identify after consent; backend `profile_updated` | `age_band`, `gender` (enum) | screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart | test/core/analytics/posthog_identify_demographics_test.dart |
| Check email | Screen viewed | `signup_email_verification_viewed` | `entry=after_signup/unverified_login` | screens/sign_up/cubit/sign_up_cubit.dart | test/screens/sign_up/personalise_step_analytics_test.dart, sign_up_analytics_fe_fix2_test.dart |
| Check email | Resend | `signup_email_verification_resent` | `success` | screens/sign_up/cubit/sign_up_cubit.dart | test/screens/sign_up/sign_up_analytics_fe_fix2_test.dart |
| Check email | Email verified (auto-advance) | `signup_email_verified` | `wait_seconds` | screens/sign_up/cubit/sign_up_cubit.dart | test/screens/sign_up/sign_up_analytics_fe_fix2_test.dart |
| Check email | Sign out / leave | `signup_email_verification_abandoned` | `wait_seconds` | screens/sign_up/cubit/sign_up_cubit.dart | test/screens/sign_up/sign_up_analytics_fe_fix2_test.dart |
| Agreements | Screen viewed | `onboarding_started`, `consent_screen_viewed`, `onboarding_step_viewed` | `source=fresh/reset`; `consent_type=gdpr`; `step_index=0` | therapy_onboarding_cubit.dart; views/onboarding_legal_gate_view.dart | test/screens/therapy_onboarding/therapy_onboarding_analytics_fe_fix2_test.dart, onboarding_legal_gate_view_test.dart |
| Agreements | Both boxes ticked | `onboarding_legal_gate_gate_ready` | `time_since_step_viewed_seconds`, viewport | views/onboarding_legal_gate_view.dart | test/screens/therapy_onboarding/onboarding_legal_gate_view_test.dart |
| Agreements | Continue (consent saved) | `consent_granted`, `onboarding_step_completed`, identify | `consent_type=gdpr`; `step_index=0` | therapy_onboarding_cubit.dart | test/screens/therapy_onboarding/therapy_onboarding_analytics_fe_fix2_test.dart |
| Agreements | Consent save failed | `onboarding_step_save_failed` | `step_index=0`, `step_name`, `error_type` | therapy_onboarding_cubit.dart | test/screens/therapy_onboarding/therapy_onboarding_analytics_fe_fix2_test.dart |
| Agreements | Left without both boxes | `onboarding_legal_gate_abandoned` | `time_on_screen_seconds`, `gdpr_checked`, `age_checked`, viewport | views/onboarding_legal_gate_view.dart | test/screens/therapy_onboarding/onboarding_legal_gate_view_test.dart |
| Agreements | Open privacy policy | `legal_link_opened` | `surface=agreements`, `link=privacy` | views/onboarding_legal_gate_view.dart | test/screens/therapy_onboarding/onboarding_legal_gate_view_test.dart |
| Agreements | Change language | `onboarding_language_changed` | `to` (language code) | views/onboarding_legal_gate_view.dart | test/screens/therapy_onboarding/onboarding_legal_gate_view_test.dart |
| Step 1 focus areas | Viewed, Continue | `onboarding_step_viewed`, `onboarding_step_completed` | `step_index=1`, `focus_area_count`, `custom_focus_area_count` | therapy_onboarding_cubit.dart | test/screens/therapy_onboarding/therapy_onboarding_analytics_fe_fix2_test.dart |
| Step 2 intensity | Viewed, Continue | step events | `step_index=2` | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Step 3 therapy status | Continue / Skip | `onboarding_step_completed` | `step_index=3`, `outcome=saved/skipped`, `total_steps=7/5` | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Step 3 therapy status | Art.9 consent tick / untick | backend `consent_granted` / `consent_revoked` | `consent_type=ARTICLE9_HEALTH` | backend consent.py (unchanged) | backend |
| Step 4 therapy type | Continue / Skip | `onboarding_step_completed` | `step_index=4`, `outcome` | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Step 5 next session | Continue / "I don't have a date yet" | `onboarding_step_completed` | `step_index=5`, `outcome` only (schedule details removed, security M-3) | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Step 6 companion | Continue | `onboarding_step_completed` | `step_index=6`, `archetype` (enum), `orca_color` (enum); orca name never sent | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Step 7 lead source | Set up my app / Skip | `onboarding_lead_source_selected`, `onboarding_step_completed`, `onboarding_completed` | `source_value` (enum); `outcome`; `total_duration_seconds`, `total_steps` | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Step 7 lead source | Type "Other" | `onboarding_lead_source_other_text` | `text_length` only, once | views/onboarding_lead_source_view.dart (FE-FIX-1) | test/screens/therapy_onboarding/onboarding_lead_source_view_wave4_test.dart |
| Any step | Back arrow | `onboarding_step_back`, then `onboarding_step_viewed` | `from_step`, `to_step` | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Any step | Save failed | `onboarding_step_save_failed` | `step_index`, `step_name`, `error_type` | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Onboarding | Context failed to load | `onboarding_load_failed` | `error_type` | therapy_onboarding_cubit.dart | therapy_onboarding_analytics_fe_fix2_test.dart |
| Build | Viewed / finished | `post_onboarding_build_viewed`, `post_onboarding_build_finished` | `focus_area_count`, `reduced_motion`; `duration_ms`, `first_read_ready`, `profile_loaded` | screens/wow/cubit/wow_cubit.dart | test/screens/wow/wow_cubit_test.dart |
| Reveal | Viewed / Let's start | `personal_reveal_viewed`, `personal_reveal_cta_tapped` | `focus_area_count`, `first_read_shown`; `dwell_ms` | wow_cubit.dart | wow_cubit_test.dart |
| Offer | Not shown | `post_onboarding_offer_not_shown` | `reason` | wow_cubit.dart | wow_cubit_test.dart |
| Offer | Shown | `subscription_screen_opened`, `paywall_shown` | `trigger_feature=post_onboarding`, `plans_shown` | subscription_cubit.dart via wow_screen.dart | subscription_cubit_analytics_test.dart, wow_screen_test.dart |
| Offer | Change option | `post_onboarding_offer_option_selected` | `option` | wow_cubit.dart | wow_cubit_test.dart, wow_screen_test.dart |
| Offer | Tap the purchase button | `subscription_product_selected`, `subscription_purchase_started` | `selection_source=cta`, `trigger_feature=post_onboarding`, product props | views/post_onboarding_offer_view.dart, subscription_cubit.dart, starter_package_cubit.dart | wow_screen_test.dart, starter_package_cubit_test.dart |
| Offer | Purchase success / fail / verification fail | `subscription_purchase_completed/failed`, `subscription_verification_failed`, `post_onboarding_offer_result` | `trigger_feature`, `failure_reason`, `result` | subscription_cubit.dart, starter_package_cubit.dart, wow_cubit.dart | subscription_cubit_analytics_test.dart, starter_package_cubit_test.dart, wow_cubit_test.dart |
| Offer | Skip (X / Continue free) | `post_onboarding_offer_result` | `result=skipped`, `skip_method` | wow_cubit.dart | wow_cubit_test.dart |
| Offer | Restore | `subscription_restore_*`, `post_onboarding_offer_result` | `trigger_feature`, `result=restored` | subscription_cubit.dart, wow_cubit.dart | subscription_cubit_analytics_test.dart |
| Offer | Tap Terms / Privacy | `legal_link_opened` | `surface=offer`, `link` | views/post_onboarding_offer_view.dart | test/screens/wow/wow_screen_test.dart |
| Reminders pre-prompt | Viewed | `push_prompt_viewed` | `variant=session_reminders/checkin_reminders` | wow_cubit.dart | wow_cubit_test.dart |
| Reminders pre-prompt | Turn on + OS answer | `notification_permission_prompted`, `notification_permission_granted/denied`, `push_prompt_result` | `source=pre_prompt`; `result`, `variant` | services/fcm_token_service.dart, services/push_permission_gateway.dart, wow_cubit.dart | test/services/fcm_cold_prompt_policy_test.dart, wow_cubit_test.dart |
| Reminders pre-prompt | Not now / not shown | `push_prompt_result` | `result=not_now/skipped_*`, `os_status` | wow_cubit.dart | wow_cubit_test.dart |
| Main page (existing users) | OS cold prompt | `notification_permission_*` | `source=cold_prompt` | services/fcm_token_service.dart | test/services/fcm_cold_prompt_policy_test.dart |
| First step | Viewed / option / Take me to the app | `first_capture_prompt_shown`, `first_capture_prompt_option_tapped`, `first_capture_prompt_dismissed` | `prompt_variant`, `capture_types_offered_count` (int), `choice`, `dwell_ms` | wow_cubit.dart | wow_cubit_test.dart, wow_screen_test.dart |
| Home trial bar | Viewed / See plans | `trial_bar_viewed`, `trial_bar_tapped`, then `paywall_shown` | `days_left`; `trigger_feature=trial_banner` | screens/usage/widgets/trial_bar.dart | test/screens/usage/trial_visibility_test.dart |
| Usage chips | What the chips show (impressions) | `usage_snapshot` (once per app session) | `plan`, `<feature>_left` (int, -1 unlimited), `features_at_zero` | screens/usage/cubit/usage_cubit.dart | test/screens/usage/usage_model_and_cubit_test.dart |
| Usage chips | Tap an in-app entry at 0 | `usage_chip_tapped_at_zero`, then `paywall_shown` | `feature`, `entry_point=fab/home_card/getting_started/timeline_bridge`; `trigger_feature=premium_gate_<feature>` | screens/usage/usage_gate.dart | test/screens/usage/usage_chip_and_gate_test.dart |
| Usage chips | External entry at 0 (push, cold start, moment CTA) | `usage_chip_tapped_at_zero` | `entry_point=notification/moment` | screens/usage/usage_gate.dart, main.dart, splash_screen.dart | test/screens/usage/usage_external_entry_gate_test.dart |
| Usage chips | Recording gate trigger | `paywall_shown` | `trigger_feature=premium_gate_session_recording` (one spelling) | screens/usage/usage_feature.dart, usage_gate.dart | test/screens/usage/usage_external_entry_gate_test.dart |
| Usage chips | Last free use note | `usage_last_free_note_shown` | `feature` | screens/usage/usage_gate.dart | usage_chip_and_gate_test.dart |
| Usage chips | Load failed | `usage_load_failed` | `error_class` | screens/usage/cubit/usage_cubit.dart | usage_model_and_cubit_test.dart |
| Reflect | New conversation at 0 | `reflect_new_thread_tapped`, `usage_chip_tapped_at_zero`, `paywall_shown` | `entry_point=reflect_new`; `trigger_feature=premium_gate_reflect_messages` | screens/reflect_tab/reflect_tab_screen.dart | test/screens/usage/usage_chip_and_gate_test.dart (shared helper) |
| Reflect limit panel | Panel shown | `usage_limit_panel_shown` | `feature=reflect_messages` | screens/reflect_tab/widgets/reflect_usage_indicator.dart | test/screens/usage/usage_chip_and_gate_test.dart |
| Reflect limit panel | Tap Premium | `usage_chip_tapped_at_zero`, `paywall_shown` | `entry_point=reflect_limit_panel` | reflect_usage_indicator.dart | test/screens/usage/usage_chip_and_gate_test.dart |
| Day-3 sheet | Shown / result | `trial_reminder_sheet_shown`, `trial_reminder_sheet_result` | counts; `result` | managers/trial_popup_manager.dart | test/screens/usage/trial_visibility_test.dart |
| Day-3 sheet | Keep Premium opens the paywall | `paywall_shown` | `trigger_feature=trial_reminder` (trial variant) | managers/trial_popup_manager.dart, screens/subscription/paywall_context.dart | trial_visibility_test.dart, paywall_context_test.dart |
| Trial-ended paywall | Shown | `subscription_screen_opened`, `paywall_shown` | `trigger_feature=trial_ended_popup` | managers/trial_popup_manager.dart | trial_visibility_test.dart |
| Paywall | Viewed | `subscription_screen_opened`, `paywall_shown` | `trigger_feature`, `plans_shown`, `hours_since_signup` | subscription_cubit.dart | subscription_cubit_analytics_test.dart |
| Paywall | Products failed to load | `paywall_load_failed` | `trigger_feature`, `error_type` | subscription_cubit.dart | subscription_cubit_analytics_test.dart |
| Paywall | Plan reported on mount / tapped | `subscription_product_selected` | `selection_source=default/user`, `trigger_feature`, product props | subscription_body.dart, subscription_cubit.dart | subscription_body_test.dart, subscription_cubit_analytics_test.dart |
| Paywall | Purchase start / success / fail | `subscription_purchase_started/completed/failed` | `trigger_feature`, `failure_reason`, `server_confirmed` | subscription_cubit.dart | subscription_cubit_analytics_test.dart |
| Paywall | Receipt not verified | `subscription_verification_failed` | `trigger_feature` | subscription_cubit.dart, starter_package_cubit.dart | subscription_cubit_analytics_test.dart, starter_package_cubit_test.dart |
| Paywall | Starter card "Try it" (success / fail) | `subscription_product_selected/purchase_*` | `product_type=starter_package`, `trigger_feature`, `failure_reason`; failure keeps the card and shows the inline line | starter_package_cubit.dart, starter_pack_card.dart, subscription_screen.dart | starter_package_cubit_test.dart, subscription_body_test.dart |
| Paywall | Expand promo | `paywall_promo_expanded` | `trigger_feature` (code never sent) | widgets/paywall_promo_section.dart | subscription_body_test.dart |
| Paywall | Promo applied / refused | backend `promo_code_applied` | `success`, `failure_reason` | backend users.py | backend |
| Paywall | Restore | `subscription_restore_started/completed/failed` | `trigger_feature` | subscription_cubit.dart | subscription_cubit_analytics_test.dart |
| Paywall | Close X / system back | `paywall_dismissed` (once) | `trigger_feature`, `selected_plan`, `purchase_attempted`, `dwell_ms`, `dismiss_method=close_x/system_back` | subscription_body.dart, subscription_cubit.dart | subscription_body_test.dart, subscription_cubit_analytics_test.dart |
| Paywall | Tap Terms / Privacy | `legal_link_opened` | `surface=paywall`, `link` | widgets/subscription_legal_links.dart | subscription_body_test.dart |
| Premium-active view | Viewed | `premium_view_shown` (`paywall_shown` suppressed) | `variant=store/trial/promo/starter`, `trigger_feature` | widgets/premium_view.dart | test/screens/subscription/premium_view_test.dart |
| Premium-active view | Manage subscription | `premium_manage_tapped` | `variant`, `trigger_feature` | widgets/premium_view.dart | premium_view_test.dart |
| Premium-active view | Choose a plan / See plans | `paywall_shown` | `trigger_feature` of the entry | subscription_screen.dart, subscription_cubit.dart | subscription_cubit_analytics_test.dart |
| Premium-active view | Restore | `subscription_restore_*` | `trigger_feature` | widgets/premium_view.dart | subscription_cubit_analytics_test.dart |
| Premium-active view | Back / system back | `premium_view_closed` (no longer `paywall_dismissed`) | `variant`, `trigger_feature`, `dismiss_method` | widgets/premium_view.dart | premium_view_test.dart |
| Premium-active view | Terms / Privacy | `legal_link_opened` | `surface=premium_view`, `link` | widgets/premium_view.dart | premium_view_test.dart |
| Welcome to Premium | Viewed (from paywall and from the offer) | `premium_welcome_viewed` | `entry=paywall/post_onboarding_offer` | screens/subscription/premium_welcome_screen.dart | test/screens/subscription/premium_welcome_screen_test.dart |
| Welcome to Premium | Any exit | `premium_welcome_action` (once) | `action=open_after_therapy/start_after/start_record/start_monthly/back_home/continue/system_back`, `entry` | premium_welcome_screen.dart | premium_welcome_screen_test.dart |
| Backend facts | Account, trial, purchase truth | `user_registered`, `trial_started`, `trial_ended`, `subscription_receipt_received`, backend `subscription_purchase_completed`, `one_time_*`, `promo_code_applied`, person properties `plan`, `premium_source` | as in audit section 1 | backend | backend tests |

## 2. Funnels (section 2 of the audit), after FE-FIX-2

| journey | linking property | where it is tested |
|---|---|---|
| (a) Welcome to Home, 7 steps | Welcome and Account: event order (`welcome_cta_tapped`, `auth_method_tapped`, `auth_validation_failed`); Name and Check email: `step_index=-1`, `signup_*`, `signup_email_verification_*`; onboarding: `step_index` + `total_steps` + `outcome`; post-onboarding: fixed event order | per surface: welcome_body_test, auth_body_test, sign_up_analytics_fe_fix2_test; onboarding journey (a) in therapy_onboarding_analytics_fe_fix2_test; Build to First step in wow_cubit_test (privacy + full funnel test) |
| (b) 5 steps, starter pack bought on the offer | `total_steps=5`, `outcome=skipped`; offer events with `trigger_feature=post_onboarding`, `product_type=starter_package`, `selection_source=cta`; `premium_welcome_viewed` `entry=post_onboarding_offer` | therapy_onboarding_analytics_fe_fix2_test (journey b), starter_package_cubit_test (G5), wow_screen_test (starter success, offer result), premium_welcome_screen_test |
| (c) Trial bar to annual purchase to Welcome | `trigger_feature=trial_banner` on every paywall event | trial_visibility_test (bar), subscription_cubit_analytics_test "FE-FIX-2 funnels (c)", premium_welcome_screen_test |
| (d) Zero on After therapy to paywall to dismiss | `feature=after_therapy` then `trigger_feature=premium_gate_after_therapy`; exit `paywall_dismissed` | subscription_cubit_analytics_test "FE-FIX-2 funnels (d)", subscription_body_test (X, system back) |
| (e) Day-3 sheet, trial ended, trial-ended paywall, monthly | `trigger_feature=trial_ended_popup` (or `trial_reminder` after Keep Premium); iOS cancel now visible as `subscription_purchase_failed` | trial_visibility_test (sheet), subscription_cubit_analytics_test "FE-FIX-2 funnels (e)" |

Not testable as one unit-level script: journey (a) and the first part of (b) cross five routes, each with its own cubit (WelcomeBody, AuthBody/AuthCubit, SignUpCubit, TherapyOnboardingCubit, WowCubit), so they are asserted per segment with the linking properties above. Google / Apple log-in and sign-in call platform plugins (GoogleSignIn, SignInWithApple) and are covered through the shared `logLoginFailed` / `authErrorTypeFor` helpers. Backend steps of every journey are outside the client tests.

## 3. Gap list G1..G22

| id | status | note |
|---|---|---|
| G1 | DONE | `paywall_dismissed` from the X and system back, once, never after a completed purchase, never without `paywall_shown`; premium view uses `premium_view_closed` |
| G2 | ALREADY DONE (FE-FIX-1) | verified by the existing "G2" test |
| G3 | ALREADY DONE (FE-FIX-1) | verified by the existing "G3" tests |
| G4 | ALREADY DONE (FE-FIX-1) | verified by the existing "G4" tests |
| G5 | DONE | `trigger_feature` on every SubscriptionCubit event; StarterPackageCubit `configureContext` from the paywall and the offer |
| G6 | ALREADY DONE (FE-FIX-1) | existing "G6" tests; gate-ready / abandoned now asserted too |
| G7 | ALREADY DONE (FE-FIX-1) | existing lead source test |
| G8 | DONE | `trial_reminder` trigger, mapped to the trial variant |
| G9 | DONE | `outcome` saved / skipped on steps 3, 4, 5, 7 |
| G10 | DONE | `auth_method_tapped`, `auth_validation_failed`, `auth_mode_switched`, `login_failed`; OAuth `signup_failed` aligned (`error_type` + `method`) |
| G11 | DONE | four Check email events; personalise viewed no longer fires when the screen opens on Check email |
| G12 | DONE | premium view shown / manage / closed; Welcome viewed / action incl. flow-mode `continue` |
| G13 | DONE | `usage_snapshot` once per app session, numbers only (plus the `plan` enum) |
| G14 | DONE | `usage_limit_panel_shown` + `usage_chip_tapped_at_zero` (`reflect_limit_panel`) |
| G15 | DONE | `selection_source` default / user / cta |
| G16 | DONE | one spelling `premium_gate_session_recording` (`UsageFeature.triggerKey`) |
| G17 | DONE | `paywall_load_failed`, `paywall_promo_expanded`, `legal_link_opened` on five surfaces, counts / enums on step completion, `onboarding_step_save_failed`, `onboarding_load_failed`, `onboarding_language_changed`, `source` on `notification_permission_*` |
| G18 | NOT DONE (lead decision) | client `subscription_tier` writer left as is this release; backend owns `plan` / `premium_source` |
| G19 | NOT DONE (lead decision) | purchase event ownership unchanged; insights on `subscription_purchase_completed` / `subscription_verification_failed` must filter `$lib` |
| G20 | NOT CLIENT | backend (person properties `plan`, `premium_source`) |
| G21 | NOT CLIENT | backend / security decision |
| G22 | DONE (client part) | assertions added for every listed client event; privacy guard extended to auth (email, password), sign-up (typed name), onboarding (name, custom focus area, goal, orca name, therapy-status keys) and wow (therapy-status keys) |

## 4. Still uncovered, needs explicit operator acceptance

1. Check email left by back or app kill (not by Sign out) has no event; the absence of `signup_email_verified` after `signup_email_verification_viewed` is the "did nothing" branch.
2. `reflect_limit_hit` is still emitted by both client and backend (audit row 84); ownership unchanged under G19.
3. A restore that returns several past transactions still logs several `subscription_restore_completed` (audit row 102); a restore with nothing to restore logs no outcome.
4. Content-descriptive values still correlate with therapy status: `prompt_variant=therapy_cta/core_action_menu` (kept as shipped), `capture_types_offered_count` (4 vs 3), `push_prompt_viewed.variant=session_reminders/checkin_reminders` and `total_steps=7/5`. No property names the status or describes the therapy: after the M-3 re-verification the step 5 schedule properties were removed and the post-onboarding `capture_types_offered` list was replaced by a count. The older activation surfaces (Getting started card, Timeline bridge card) still send a fixed `capture_types_offered` list that does not depend on the user; they are outside this batch.
5. `usage_snapshot` carries `plan` as an event property (free / trial / premium / unknown); it is not written as a person property, so it does not duplicate the backend `plan` person property.
6. Google / Apple `login_failed` call sites are not exercised end to end in tests (platform plugins); the shared helpers are.
7. The Reflect "new conversation at 0" path is asserted through the shared `UsageGate.logTappedAtZero` helper and `reflectAtZero`, not by pumping the whole Reflect tab.
8. After release, `posthog-data-extractor` must confirm that every new event above actually flows before any number is reported.
