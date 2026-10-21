# PostHog coverage audit: subscription + onboarding redesign (2026-10-02)

Scope: closing stage 6.3 of `SPEC.md`, per CLAUDE.md "PostHog Instrumentation (Mandatory final step)".
Audited: uncommitted working trees on `feat/subscription-onboarding-redesign` in `mindsync-frontend/` and `MindSync/`.
Method: static read of every call site (no device run, no PostHog query). Read-only: no app code was changed.

## 0. How to read this

- Events reach PostHog through `AnalyticsEvents.logEvent` (`lib/core/analytics/analytics_events.dart:1576`), which forwards every event to `PostHogService.capture` and to Firebase Analytics. Backend events go through `app/services/posthog_service.py:96` (`capture`).
- Screen views: `PosthogObserver` is attached to the GoRouter (`lib/navigation/ms_routes.dart:292`), so every named GoRoute emits `$screen`. Steps that live inside one route (onboarding PageView, the whole `/wow` flow, Check email inside `/sign-up`, log-in vs sign-up mode inside `/auth`) get no `$screen` and depend on custom events.
- Status values:
  - **OK**: the event exists, fires once, carries usable properties. A missing test does not change the status; it is shown as `NONE` in the test column and collected in gap G22.
  - **GAP**: no event, or the event cannot answer the question it is there for.
  - **DUPLICATE**: the same fact is emitted twice (client and backend, two cubits, a rebuild) or an event fires when the thing did not happen.
  - **PRIVACY**: user-written text, a health detail, or a consent problem.
- Paths are relative to `mindsync-frontend/mindsync_app/lib/` (client) and `MindSync/app/` (backend). Tests are relative to `mindsync_app/test/` and `MindSync/app/tests/`.
- Three findings below describe behaviour of the purchase stream that was derived from the plugin source in the pub cache (`in_app_purchase_storekit 0.4.11+1`, `in_app_purchase_android 0.5.0`), not reproduced on a device. They are marked "code-derived".

## 1. Coverage table

| # | Surface | User action / fact | Event | Key properties | Where it fires | Side | Test | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Welcome | Screen viewed | `$screen` (welcome) | `$screen_name` | navigation/ms_routes.dart:292, :315 | client | NONE | OK |
| 2 | Welcome | Tap "Get started" | `welcome_cta_tapped` | `cta=sign_up` | screens/welcome/welcome_body.dart:29 | client | NONE | OK |
| 3 | Welcome | Tap "I already have an account" | `welcome_cta_tapped` | `cta=log_in` | screens/welcome/welcome_body.dart:34 | client | NONE | OK |
| 4 | Welcome | Tap Terms / Privacy | none | | screens/welcome/welcome_body.dart:186 | client | NONE | GAP |
| 5 | Account | Screen viewed | `$screen` (auth) | mode not carried (inferred from row 2 or 3) | navigation/ms_routes.dart:334 | client | NONE | OK |
| 6 | Account | Switch between "Create account" and "Log in" | none | | screens/auth/auth_body.dart:80; widgets/animated_widgets/animated_bottom_widgets.dart:45 | client | NONE | GAP |
| 7 | Account | Tap Apple / Google button | none at the tap | | screens/auth/widgets/animated_widgets/animated_google_apple_widgets.dart:79, :91 | client | NONE | GAP |
| 8 | Account | Tap "Create account" with a valid email and password | none (next signal is `$screen` signUp) | | screens/auth/auth_body.dart:150 | client | NONE | GAP |
| 9 | Account | Validation error (email, password, terms checkbox) | none | | screens/auth/auth_body.dart:137-149, :252-311 | client | NONE | GAP |
| 10 | Account | Log in success, email | `user_logged_in` | `auth_provider=email`, `platform` | screens/auth/cubit/auth_cubit.dart:197, :210 | client | NONE | OK |
| 11 | Account | Log in success, Google / Apple (existing account) | `user_logged_in` | `auth_provider=google/apple`, `platform` | screens/auth/cubit/auth_cubit.dart:278, :378 | client | NONE | OK |
| 12 | Account | Log in failure (wrong credentials, unverified email redirect, social cancel or error) | none | | screens/auth/cubit/auth_cubit.dart:166, :176, :320, :419 | client | NONE | GAP |
| 13 | Account | Forgot password | `password_reset_requested`, `password_reset_failed` | none | screens/forgot_password/cubit/forgot_password_cubit.dart:16, :24 | client | NONE | OK |
| 14 | Account (backend) | Account row created | `user_registered` | `auth_provider` | api/v1/endpoints/users.py:298 | backend | NONE | OK |
| 15 | Name | Screen viewed | `onboarding_step_viewed` (+ `$screen` signUp) | `step_index=-1`, `step_name=personalise` | screens/sign_up/cubit/sign_up_cubit.dart:79 | client | screens/sign_up/personalise_step_analytics_test.dart | OK |
| 16 | Name | Viewed event when the screen opens straight on Check email (returning unverified user) | `onboarding_step_viewed` fires from the cubit constructor although the name screen is never shown | same | screens/sign_up/cubit/sign_up_cubit.dart:26-27; sign_up_screen.dart:41 | client | NONE | DUPLICATE |
| 17 | Name | Tap "Continue" | `onboarding_step_completed`, `signup_started`, `signup_method_selected` | `step_index=-1`, `duration_seconds`; `method=email/oauth` | screens/sign_up/cubit/sign_up_cubit.dart:100, :165-169, :267-271 | client | personalise_step_analytics_test.dart (step only) | OK |
| 18 | Name | Registration failed, email path | `signup_failed` | `error_type=register_failed/login_failed/no_current_user/backend_provisioning_failed` | screens/sign_up/cubit/sign_up_cubit.dart:177-241 | client | NONE | OK |
| 19 | Name | Registration failed, Google / Apple path | none (no try/catch, the exception escapes) | | screens/sign_up/cubit/sign_up_cubit.dart:257-300 | client | NONE | GAP |
| 20 | Name | Optional fields filled (age range, gender, pronouns) | `profile_updated` + person properties `age_band`, `gender` | `updated_fields` (names only), `is_first_save` | api/v1/endpoints/users.py:396, :417; screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart:329 | backend + client identify | core/analytics/posthog_identify_demographics_test.dart | OK |
| 21 | Check email | Screen viewed | none (state inside the signUp route) | | screens/sign_up/sign_up_screen.dart:60 | client | NONE | GAP |
| 22 | Check email | Resend email | none | | screens/sign_up/cubit/sign_up_cubit.dart:317 | client | NONE | GAP |
| 23 | Check email | Email verified (auto-advance) | none | | screens/sign_up/cubit/sign_up_cubit.dart:310-312 | client | NONE | GAP |
| 24 | Check email | Sign out / leave | none | | screens/sign_up/check_email_view.dart:43 | client | NONE | GAP |
| 25 | Agreements | Screen viewed | `onboarding_started`, `onboarding_step_viewed`, `consent_screen_viewed` (+ `$screen` therapyOnboarding) | `source=fresh/reset`; `step_index=0`, `step_name=legal_gate`; `consent_type=gdpr` | screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart:139, :143, :186; views/onboarding_legal_gate_view.dart:62 | client | screens/therapy_onboarding/therapy_onboarding_cubit_branching_test.dart (step viewed) | OK |
| 26 | Agreements | Screen NOT viewed: user resumes on step 1-7, or onboarding is already complete | `consent_screen_viewed` always fires, and `onboarding_legal_gate_abandoned` fires on resume, because the gate is now PageView page 0 and is built before the jump | as row 25 / row 30 | screens/therapy_onboarding/views/onboarding_legal_gate_view.dart:60-84, :97-104; therapy_onboarding_screen.dart:57-66, :76-83 | client | NONE | DUPLICATE |
| 27 | Agreements | Both checkboxes ticked | `onboarding_legal_gate_gate_ready` | `time_since_step_viewed_seconds`, `viewport_width`, `viewport_height`, `text_scale_factor`, `locale` | screens/therapy_onboarding/views/onboarding_legal_gate_view.dart:114 | client | NONE | OK |
| 28 | Agreements | Tap "Continue" (consent saved) | `consent_granted`, `onboarding_step_completed`, PostHog identify | `consent_type=gdpr`; `step_index=0`, `duration_seconds` | screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart:272-282, :329 | client | screens/sign_up/onboarding_gdpr_sequencing_test.dart (identify order) | OK |
| 29 | Agreements | Consent save failed | none | | screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart:287 | client | NONE | GAP |
| 30 | Agreements | Left without both boxes ticked | `onboarding_legal_gate_abandoned` | `time_on_screen_seconds`, `gdpr_checked`, `age_checked`, viewport | screens/therapy_onboarding/views/onboarding_legal_gate_view.dart:73 | client | NONE | OK |
| 31 | Agreements | Open privacy policy | none | | screens/therapy_onboarding/views/onboarding_legal_gate_view.dart:218 | client | NONE | GAP |
| 32 | Agreements | Change language | none | | screens/therapy_onboarding/views/onboarding_legal_gate_view.dart:330-379 | client | NONE | GAP |
| 33 | Step 1 focus areas | Viewed, "Continue" | `onboarding_step_viewed`, `onboarding_step_completed` | `step_index=1`, `step_name=challenges`, `duration_seconds` | screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart:282, :388 | client | therapy_onboarding_cubit_branching_test.dart | OK |
| 34 | Step 1 focus areas | Select chips, add own focus area | none, and no counts on the completed event | | screens/therapy_onboarding/views/onboarding_challenges_view.dart:41, :81-104 | client | NONE | GAP |
| 35 | Step 2 intensity | Viewed, "Continue" | step events | `step_index=2`, `step_name=intensity` | cubit:389, :416 | client | therapy_onboarding_cubit_branching_test.dart | OK |
| 36 | Step 3 therapy status | Viewed, "Continue" | step events | `step_index=3`, `step_name=journey`, `total_steps=7/5` | cubit:417, :536-537 | client | therapy_onboarding_cubit_branching_test.dart | OK |
| 37 | Step 3 therapy status | Tick / untick Art.9 consent | `consent_granted`, `consent_revoked` | `consent_type=ARTICLE9_HEALTH`, `consent_id` | api/v1/endpoints/consent.py:186, :245 | backend | NONE | OK |
| 38 | Step 3 therapy status | Tap "Skip" | `onboarding_step_completed`, identical to "Continue" | no skip flag | cubit:552-566 | client | NONE | GAP |
| 39 | Step 4 therapy type | Viewed, "Continue" | step events | `step_index=4`, `step_name=modality`, `total_steps=7` | cubit:589-590 | client | therapy_onboarding_cubit_branching_test.dart | OK |
| 40 | Step 4 therapy type | Tap "Skip" | `onboarding_step_completed`, no skip flag | | cubit:603-612 | client | NONE | GAP |
| 41 | Step 5 next session | Viewed, "Continue" | step events | `step_index=5`, `step_name=schedule`, `total_steps=7` | cubit:747-748 | client | therapy_onboarding_cubit_branching_test.dart | OK |
| 42 | Step 5 next session | Tap "I don't have a date yet" | `onboarding_step_completed`, no skip flag | | cubit:758-767 | client | NONE | GAP |
| 43 | Step 5 next session | Weekday, time, frequency, custom calendar add / remove | none, and no counts on the completed event | | screens/therapy_onboarding/views/onboarding_schedule_view.dart:150-226 | client | NONE | GAP |
| 44 | Step 6 companion | Viewed, "Continue" | step events (orca name never sent) | `step_index=6`, `step_name=companion` | cubit:819-820 | client | therapy_onboarding_cubit_branching_test.dart | OK |
| 45 | Step 6 companion | Pick talk style, color | none, and no enum on the completed event | | screens/therapy_onboarding/views/onboarding_companion_view.dart:168, :198 | client | NONE | GAP |
| 46 | Step 7 lead source | Viewed, "Set up my app" | `onboarding_lead_source_selected`, `onboarding_step_completed`, `onboarding_completed` | `source_value` (enum); `step_index=7`; `total_duration_seconds`, `total_steps` | cubit:869, :928-938 | client | screens/therapy_onboarding/onboarding_lead_source_view_wave4_test.dart (lead source only) | OK |
| 47 | Step 7 lead source | Tap "Skip" | `onboarding_step_completed` + `onboarding_completed`, no skip flag | | cubit:902-905 | client | NONE | GAP |
| 48 | Step 7 lead source | Type the "Other" answer | `onboarding_lead_source_other_text` | `text_length`, **`first_50_chars` (user-written text)** | screens/therapy_onboarding/views/onboarding_lead_source_view.dart:57 | client | NONE | PRIVACY |
| 49 | Step 7 lead source | Confirm the "Other" answer | same event fires up to 4 times for one answer (`onSubmitted`, `onEditingComplete`, check icon, primary button) | | screens/therapy_onboarding/views/onboarding_lead_source_view.dart:89, :120-134 | client | NONE | DUPLICATE |
| 50 | 5-step branch | Steps 4 and 5 are not shown | no events for index 4 and 5; `total_steps=5` on steps 3, 6, 7 and on `onboarding_completed` | `total_steps` | cubit:92-99, :507, :559 | client | therapy_onboarding_cubit_branching_test.dart | OK |
| 51 | Any step | Back arrow | `onboarding_step_back`, then `onboarding_step_viewed` for the target | `from_step`, `to_step` | cubit:709-713 | client | NONE | OK |
| 52 | Any step | Save failed (snackbar), or the context failed to load | none | | cubit:205-210, :394, :422, :543, :595, :750 | client | NONE | GAP |
| 53 | Resume | Onboarding reopened after an app kill | `onboarding_started`, `onboarding_step_viewed` | `source=reset`, step index | cubit:178-190 | client | therapy_onboarding_cubit_branching_test.dart | OK |
| 54 | Build | Screen viewed (also the only `$screen` of the whole flow: wow) | `post_onboarding_build_viewed` | `in_therapy`, `has_schedule`, `focus_area_count`, `reduced_motion` | screens/wow/cubit/wow_cubit.dart:116 | client | screens/wow/wow_cubit_test.dart | OK |
| 55 | Build | Finished | `post_onboarding_build_finished` | `duration_ms`, `first_read_ready`, `profile_loaded` | screens/wow/cubit/wow_cubit.dart:162 | client | wow_cubit_test.dart | OK |
| 56 | Reveal | Screen viewed | `personal_reveal_viewed` | `in_therapy`, `has_schedule`, `focus_area_count`, `first_read_shown` | screens/wow/cubit/wow_cubit.dart:223 | client | wow_cubit_test.dart, wow_screen_test.dart | OK |
| 57 | Reveal | Tap "Let's start" | `personal_reveal_cta_tapped` | `first_read_shown`, `dwell_ms` | screens/wow/cubit/wow_cubit.dart:240 | client | wow_cubit_test.dart | OK |
| 58 | Offer | Not shown | `post_onboarding_offer_not_shown` | `reason=not_just_onboarded/status_unavailable/already_premium/already_seen/products_unavailable` | screens/wow/cubit/wow_cubit.dart:256 | client | wow_cubit_test.dart, wow_screen_test.dart | OK |
| 59 | Offer | Shown | `subscription_screen_opened`, `paywall_shown` | `trigger_feature=post_onboarding`, `plans_shown` (starter pack not counted), `hours_since_signup`, `user_id` | screens/subscription/cubit/subscription_cubit.dart:56, :108 via screens/wow/wow_screen.dart:192 | client | screens/subscription/cubit/subscription_cubit_analytics_test.dart, wow_screen_test.dart | OK |
| 60 | Offer | Change option | `post_onboarding_offer_option_selected` | `option=starter/annual/monthly` | screens/wow/cubit/wow_cubit.dart:291 | client | wow_cubit_test.dart, wow_screen_test.dart | OK |
| 61 | Offer | Tap the purchase button | `subscription_product_selected`, `subscription_purchase_started` | `product_id`, `product_price`, `currency_code`, `subscription_type` or `product_type=starter_package` | subscription_cubit.dart:150, :164; screens/main_page/daily_page/cubit/starter_package_cubit.dart:40, :64; wow/views/post_onboarding_offer_view.dart:53-71 | client | NONE for purchase_started | OK |
| 62 | Offer | Purchase success | `subscription_purchase_completed` (client), `post_onboarding_offer_result` | `result=purchased_starter/purchased_annual/purchased_monthly`, `option_selected`, `dwell_ms` | subscription_cubit.dart:298; starter_package_cubit.dart:184; wow_cubit.dart:301 | client | wow_cubit_test.dart, wow_screen_test.dart | OK |
| 63 | Offer | Starter pack purchased while SubscriptionCubit is also listening (code-derived) | SubscriptionCubit has no product filter on the broadcast purchase stream, so it also handles the starter transaction: extra `POST /subscription_data`, then either a phantom `subscription_verification_failed` or a second `subscription_purchase_completed`, and `post_onboarding_offer_result` can be logged as `purchased_annual` if that cubit answers first | | subscription_cubit.dart:242-328; wow/wow_screen.dart:108-120; starter_package_cubit.dart:143 | client + backend | NONE | DUPLICATE |
| 64 | Offer | Skip (X or "Continue with my free 4 days") | `post_onboarding_offer_result` | `result=skipped`, `skip_method=close_x/continue_free`, `option_selected`, `dwell_ms` | screens/wow/cubit/wow_cubit.dart:313 | client | wow_cubit_test.dart, wow_screen_test.dart | OK |
| 65 | Offer | Restore | `subscription_restore_started/completed/failed`, `post_onboarding_offer_result` | `result=restored` | subscription_cubit.dart:214-228, :298; wow_cubit.dart:326 | client | subscription_cubit_analytics_test.dart | OK |
| 66 | Offer | Tap Terms / Privacy | none | | screens/wow/views/post_onboarding_offer_view.dart:183 | client | NONE | GAP |
| 67 | Reminders pre-prompt | Screen viewed | `push_prompt_viewed` | `variant=in_therapy/no_therapy` | screens/wow/cubit/wow_cubit.dart:366 | client | wow_cubit_test.dart | OK |
| 68 | Reminders pre-prompt | "Turn on reminders" + OS dialog answer | `notification_permission_prompted`, `notification_permission_granted/denied`, `push_prompt_result` | `result=accepted/declined`, `variant` | services/fcm_token_service.dart:75, :85, :88; wow_cubit.dart:398 | client | wow_cubit_test.dart (result only) | OK |
| 69 | Reminders pre-prompt | "Not now" | `push_prompt_result` | `result=not_now`, `variant` | screens/wow/cubit/wow_cubit.dart:406 | client | wow_cubit_test.dart | OK |
| 70 | Reminders pre-prompt | Not shown (already decided, or status unknown) | `push_prompt_result` | `result=skipped_already_decided/skipped_unavailable`, `os_status` | screens/wow/cubit/wow_cubit.dart:353, :358 | client | wow_cubit_test.dart | OK |
| 71 | First step | Screen viewed | `first_capture_prompt_shown` | `entry_point=post_onboarding`, `prompt_variant`, `capture_types_offered`, `trial_chip_shown`, `hours_since_signup` | screens/wow/cubit/wow_cubit.dart:429 | client | wow_cubit_test.dart | OK |
| 72 | First step | Pick an option | `first_capture_prompt_option_tapped` | `choice=debrief/reflect/between_session/health_check`, `prompt_variant`, `dwell_ms` | screens/wow/cubit/wow_cubit.dart:448 | client | wow_cubit_test.dart, wow_screen_test.dart | OK |
| 73 | First step | "Take me to the app" | `first_capture_prompt_dismissed` | `choice=take_me_to_app`, `dismiss_method`, `dwell_ms` | screens/wow/cubit/wow_cubit.dart:463 | client | wow_cubit_test.dart, wow_screen_test.dart | OK |
| 74 | Home trial bar | Viewed (once per app session) | `trial_bar_viewed` | `days_left` | screens/usage/widgets/trial_bar.dart:57 | client | screens/usage/trial_visibility_test.dart | OK |
| 75 | Home trial bar | Tap "See plans" | `trial_bar_tapped`, then `paywall_shown` | `days_left`; `trigger_feature=trial_banner` | screens/usage/widgets/trial_bar.dart:61-62 | client | trial_visibility_test.dart | OK |
| 76 | Usage chips | Chip visible in each state (N of M left, last one, 0 left, Unlimited in trial) | none | | screens/usage/widgets/usage_chip.dart; screens/usage/cubit/usage_cubit.dart | client | NONE | GAP |
| 77 | Usage chips | Tap an entry at zero (Before therapy, After therapy, Between Sessions, recording) | `usage_chip_tapped_at_zero`, then `paywall_shown` | `feature`, `entry_point=fab/home_card/getting_started/timeline_bridge`; `trigger_feature=premium_gate_<feature>` | screens/usage/usage_gate.dart:44-49 | client | screens/usage/usage_chip_and_gate_test.dart | OK |
| 78 | Usage chips | Recording gate: two trigger values for one feature | `premium_gate_session_recordings` (FAB gate) vs `premium_gate_session_recording` (in-flow gate) | `trigger_feature` | screens/usage/usage_gate.dart:57; screens/fab_flows/record_session_flow.dart:246 | client | NONE | DUPLICATE |
| 79 | Usage chips | Last free use note shown | `usage_last_free_note_shown` | `feature` | screens/usage/usage_gate.dart:83; screens/reflect_tab/reflect_tab_screen.dart:249 | client | usage_chip_and_gate_test.dart | OK |
| 80 | Usage chips | Usage failed to load (chips hidden) | `usage_load_failed` | `error_class=http_404/http_4xx/http_5xx/network/parse` | screens/usage/cubit/usage_cubit.dart:75 | client | screens/usage/usage_model_and_cubit_test.dart | OK |
| 81 | Usage (backend) | Entry saved at the limit without AI | `debrief_created`, `prep_card_created`, `between_session_created` | `ai_processed=false`, `processing_status=plain_text` | api/v1/endpoints/debriefs.py:485; prep_cards.py:646; between_sessions.py:463 | backend | NONE | OK |
| 82 | Usage (backend) | `GET /users/usage` called | none (read endpoint, failure is visible through row 80) | | api/v1/endpoints/users.py:1045 | backend | test_subscription_onboarding_redesign.py (contract) | OK |
| 83 | Reflect | New conversation tapped at zero | `reflect_new_thread_tapped`, `usage_chip_tapped_at_zero`, then `paywall_shown` | `feature=reflect_messages`, `entry_point=reflect_new`; `trigger_feature=premium_gate_reflect_messages` | screens/reflect_tab/reflect_tab_screen.dart:895-908 | client | NONE | OK |
| 84 | Reflect | Message refused at the limit | `reflect_limit_hit` on the client AND `reflect_limit_hit` on the backend | client: none; backend: `thread_id`, `messages_used` bucket | screens/reflect_tab/cubit/reflect_chat_cubit.dart:594; api/v1/endpoints/reflect.py:939 | client + backend | NONE | DUPLICATE |
| 85 | Reflect limit panel | Panel viewed | none | | screens/reflect_tab/widgets/reflect_usage_indicator.dart:101-108 | client | NONE | GAP |
| 86 | Reflect limit panel | Tap the Premium button | only the resulting `paywall_shown` | `trigger_feature=premium_gate_reflect_messages` | screens/reflect_tab/widgets/reflect_usage_indicator.dart:144 | client | NONE | GAP |
| 87 | Day-3 sheet | Shown | `trial_reminder_sheet_shown` | `days_left`, `therapy_entries_count`, `recordings_count`, `reflect_messages_count` | managers/trial_popup_manager.dart:161 | client | trial_visibility_test.dart | OK |
| 88 | Day-3 sheet | "Keep Premium", "Not now", swipe away | `trial_reminder_sheet_result` | `result=keep_premium/not_now/dismissed` | managers/trial_popup_manager.dart:171 | client | trial_visibility_test.dart | OK |
| 89 | Day-3 sheet | Paywall opened by "Keep Premium" | `paywall_shown` with `trigger_feature=trial_banner`, the same value as the Home bar | `trigger_feature` | managers/trial_popup_manager.dart:176-178 | client | trial_visibility_test.dart | GAP |
| 90 | Trial-ended paywall | Shown on the first open after the trial ended | `subscription_screen_opened`, `paywall_shown` | `trigger_feature=trial_ended_popup` | managers/trial_popup_manager.dart:149-151 | client | trial_visibility_test.dart, screens/subscription/paywall_context_test.dart | OK |
| 91 | Paywall | Viewed, every variant (+ `$screen` subscription) | `subscription_screen_opened`, `paywall_shown` | `trigger_feature`, `plans_shown`, `hours_since_signup`, `user_id` (variant is derivable from `trigger_feature`) | screens/subscription/cubit/subscription_cubit.dart:56, :108 | client | subscription_cubit_analytics_test.dart, screens/subscription/subscription_screen_test.dart | OK |
| 92 | Paywall | Store products failed to load (error view) | none | | screens/subscription/cubit/subscription_cubit.dart:144 | client | NONE | GAP |
| 93 | Paywall | Select a plan | `subscription_product_selected` fires for the preselected plan on every mount (again after each failed purchase reload) and then per tap; nothing separates the automatic one from a tap | `product_id`, `product_title`, `product_price`, `currency_code`, `subscription_type` | screens/subscription/subscription_body.dart:52, :72-76; subscription_cubit.dart:150 | client | screens/subscription/subscription_body_test.dart | DUPLICATE |
| 94 | Paywall | Purchase start | `subscription_purchase_started` | product props | screens/subscription/cubit/subscription_cubit.dart:164 | client | NONE | OK |
| 95 | Paywall | Purchase success | `subscription_purchase_completed` on the client AND on the backend, same name | client: `product_id`, `subscription_type`, `server_confirmed`; backend: `platform`, `product_sku`, `purchase_kind` | subscription_cubit.dart:298; api/v1/endpoints/users.py:563 | client + backend | subscription_cubit_analytics_test.dart; test_subscription_data_resubmission.py | DUPLICATE |
| 96 | Paywall | Purchase success claimed although the backend recorded FAILED | client `subscription_purchase_completed` with `server_confirmed=true`: the backend answers HTTP 200 with `status=FAILED`, and the client never reads `status` | | providers/subscription/subscription_repository.dart:13-45, :47-77; api/v1/endpoints/users.py:591-607 | client | NONE | GAP |
| 97 | Paywall | Purchase cancel / store error (code-derived) | `subscription_purchase_failed` on Android. On iOS (StoreKit 1) a cancelled or failed transaction has `pendingCompletePurchase=true`, so the cubit completes it silently and logs nothing | `failure_reason=user_cancelled/store_error/pending/unknown` | subscription_cubit.dart:244-258, :329-368; starter_package_cubit.dart:144-155 | client | subscription_cubit_analytics_test.dart (fixture with `pendingCompletePurchase=false` only) | GAP |
| 98 | Paywall | Receipt verification failed | `subscription_verification_failed` on the client AND on the backend, same name | client: `product_id`, error class; backend: `failure_reason`, `product_sku` | subscription_cubit.dart:280; starter_package_cubit.dart:166; api/v1/endpoints/users.py:592, :611 | client + backend | subscription_cubit_analytics_test.dart; test_subscription_cross_account_guard.py | DUPLICATE |
| 99 | Paywall | Starter card "Try it" | `subscription_purchase_started/completed/failed` | `product_type=starter_package` (failed events carry no `failure_reason`) | screens/main_page/daily_page/cubit/starter_package_cubit.dart:64-241; screens/subscription/widgets/starter_pack_card.dart:87 | client | screens/main_page/daily_page/cubit/starter_package_cubit_test.dart | OK |
| 100 | Paywall | Expand "Have a promo code?" | none | | screens/subscription/widgets/paywall_promo_section.dart:69 | client | NONE | GAP |
| 101 | Paywall | Promo code applied or refused | `promo_code_applied` (the code itself is never sent) | `success`, `failure_reason=not_found/inactive/expired/global_limit_reached/...` | api/v1/endpoints/users.py:834 | backend | NONE | OK |
| 102 | Paywall | Restore | `subscription_restore_started/completed/failed` (nothing to restore gives no outcome event; several restored transactions give several completed events) | `product_id`, `server_confirmed` | subscription_cubit.dart:214-228, :298 | client | subscription_cubit_analytics_test.dart | OK |
| 103 | Paywall | Close X / system back | none | | screens/subscription/subscription_body.dart:107 | client | NONE | GAP |
| 104 | Paywall, premium view | Tap Terms / Privacy | none | | screens/subscription/widgets/subscription_legal_links.dart:44 | client | NONE | GAP |
| 105 | Paywall, offer | Product select, purchase, restore and verification events carry no `trigger_feature` | all `subscription_*` events except `subscription_screen_opened` | | subscription_cubit.dart:150-421; starter_package_cubit.dart:40-247 | client | NONE | GAP |
| 106 | Premium-active view | Viewed | `subscription_screen_opened` (`paywall_shown` suppressed) | `trigger_feature`; no variant (store / trial / promo / starter) | subscription_cubit.dart:56, :92 | client | subscription_cubit_analytics_test.dart | GAP |
| 107 | Premium-active view | Tap "Manage subscription" | none | | screens/subscription/widgets/premium_view.dart:68 | client | NONE | GAP |
| 108 | Premium-active view | Tap "Choose a plan" / "See plans" | `paywall_shown` | `trigger_feature` of the entry (drawer_menu) | screens/subscription/subscription_screen.dart:96-98; subscription_cubit.dart:119 | client | subscription_cubit_analytics_test.dart | OK |
| 109 | Premium-active view | Restore | `subscription_restore_started/completed/failed` | | screens/subscription/widgets/premium_view.dart:274 | client | subscription_cubit_analytics_test.dart | OK |
| 110 | Premium-active view | Back | `paywall_dismissed`: the only place this event fires, on a screen where no paywall was shown | none | screens/subscription/widgets/premium_view.dart:88 | client | NONE | GAP |
| 111 | Welcome (after purchase) | Screen viewed | `$screen` (premiumWelcome) only from the paywall; from the offer it is a nameless `MaterialPageRoute`, so nothing | | screens/subscription/subscription_screen.dart:93; screens/wow/wow_screen.dart:130-142 | client | NONE | GAP |
| 112 | Welcome (after purchase) | "Open After therapy", three start cards, "Back to home", system back | none | | screens/subscription/premium_welcome_screen.dart:43-57, :151, :163 | client | NONE | GAP |
| 113 | Backend fact | Sign-up trial started | `trial_started` | `days`, `platform`, `trial_type=signup`, `trial_length_days`, `product_id=signup_trial` | api/v1/endpoints/users.py:451; services/posthog_service.py:925 | backend | test_subscription_onboarding_redesign.py | OK |
| 114 | Backend fact | Trial ended without purchase | `trial_ended` | `outcome=expired`, `platform`, `product_id`, `trial_type` | services/subscription_service.py:281; services/posthog_service.py:968 | backend | test_subscription_onboarding_redesign.py, test_trial_lifecycle_events.py | OK |
| 115 | Backend fact | Trial ended by a purchase (subscription or starter pack) | `trial_ended` | `outcome=converted`, `product_id` of the purchase, `trial_type` | api/v1/endpoints/users.py:586, :780 | backend | test_starter_pack_premium_source.py, test_trial_lifecycle_events.py | OK |
| 116 | Backend fact | `trial_ended` for accounts that never accepted the agreements | emitted by the hourly job with `distinct_id` = Firebase UID; `trial_started` is recorded at `POST /users/subscription`, which runs before the consent screen | | services/subscription_service.py:281; api/v1/endpoints/users.py:451 | backend | NONE | PRIVACY |
| 117 | Backend fact | One-time purchase (starter pack) | `one_time_receipt_received`, `one_time_purchase_completed`, `one_time_verification_failed` | `platform`, `product_sku`, `purchase_kind=one_time`, `failure_reason` | api/v1/endpoints/users.py:675, :753, :768, :786 | backend | test_subscription_cross_account_guard.py (failure), test_starter_pack_premium_source.py | OK |
| 118 | Backend fact | Subscription receipt received | `subscription_receipt_received` | `platform`, `product_sku`, `purchase_kind=subscription` | api/v1/endpoints/users.py:501 | backend | NONE | OK |
| 119 | Person properties | Plan (free / trial / premium) | `subscription_tier` has three writers and three vocabularies, none of them says trial | client `free/premium`; backend `basic/premium`; backend `free/premium_monthly` | screens/auth/cubit/auth_cubit.dart:98, :120; api/v1/endpoints/users.py:331-344; services/posthog_service.py:284-340 | client + backend | core/analytics/posthog_identify_behavioral_test.dart; test_behavioral_posthog.py | GAP |
| 120 | Person properties | Identify after consent | PostHog identify at consent (new user) and after the profile fetch (returning user) | `platform`, `language`, `gender` (enum), `age_band`, `country` | screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart:272, :329; screens/auth/cubit/auth_cubit.dart:68; screens/splash/splash_screen.dart:597 | client | screens/sign_up/onboarding_gdpr_sequencing_test.dart, core/analytics/posthog_identify_demographics_test.dart | OK |

Totals: 120 rows. OK 69, GAP 40, DUPLICATE 9, PRIVACY 2 (counted mechanically from the Status column).

## 2. Funnel analysis

Linking properties available today: `step_index` + `step_name` + `total_steps` (onboarding), `trigger_feature` (only on `subscription_screen_opened` and `paywall_shown`), `feature` + `entry_point` (usage gate), `variant` (reminders), `prompt_variant` + `choice` (first step), `result` (offer, reminders, day-3 sheet), `outcome` + `trial_type` (backend trial). Everything else is linked by person and time order. Backend events use the `X-PostHog-Distinct-ID` header (`lib/api/dio_client.dart:41`), so they land on the same person as the client events; the hourly job uses the Firebase UID, which is the same person once the client has identified.

### (a) Welcome -> account -> 7 steps -> Build -> Reveal -> offer skipped -> reminders accepted -> first step -> Home

1. `$screen` welcome
2. `welcome_cta_tapped` {cta: sign_up}
3. `$screen` auth
4. (hole) which button was used on the account screen, and any validation error: no event (rows 7-9)
5. `$screen` signUp + `onboarding_step_viewed` {step_index: -1, step_name: personalise}
6. `onboarding_step_completed` {step_index: -1} + `signup_started` + `signup_method_selected` {method}
7. backend `user_registered` {auth_provider}, backend `trial_started` {trial_type: signup, days: 4}
8. (hole, email path only) Check email screen, resend, verified: no event (rows 21-24)
9. `$screen` therapyOnboarding + `onboarding_started` {source: fresh} + `consent_screen_viewed` + `onboarding_step_viewed` {step_index: 0}
10. `onboarding_legal_gate_gate_ready`, `consent_granted` {consent_type: gdpr}, identify, `onboarding_step_completed` {step_index: 0}
11. `onboarding_step_viewed` / `onboarding_step_completed` for step_index 1 to 7, with `total_steps: 7` from step 3 on; backend `consent_granted` {consent_type: ARTICLE9_HEALTH} at step 3
12. `onboarding_lead_source_selected` {source_value}, `onboarding_completed` {total_duration_seconds, total_steps: 7}
13. `$screen` wow + `post_onboarding_build_viewed` {in_therapy: true, has_schedule}
14. `post_onboarding_build_finished`
15. `personal_reveal_viewed`, `personal_reveal_cta_tapped`
16. `subscription_screen_opened` + `paywall_shown` {trigger_feature: post_onboarding}
17. `post_onboarding_offer_result` {result: skipped, skip_method}
18. `push_prompt_viewed` {variant}
19. `notification_permission_prompted`, `notification_permission_granted`, `push_prompt_result` {result: accepted}
20. `first_capture_prompt_shown` {entry_point: post_onboarding}
21. `first_capture_prompt_option_tapped` {choice} or `first_capture_prompt_dismissed` {choice: take_me_to_app}
22. `$screen` mainPage

Verdict: reconstructable from Welcome to Home. Two holes, both before the account exists: the account screen (step 4) and Check email (step 8). The link between steps is `step_index` inside onboarding and plain event order elsewhere. Skips inside onboarding are invisible (rows 38, 40, 42, 47): a skipped step looks like a completed one.

### (b) Same, 5-step branch, starter pack bought on the offer

Steps 1 to 10 as in (a). Then:

11. step_index 1, 2, 3, then 6 and 7. `total_steps: 5` appears on the step 3 completed event and on every later event. No event for index 4 or 5.
12. `onboarding_completed` {total_steps: 5}
13. `post_onboarding_build_viewed` {in_therapy: false, has_schedule: false}, `post_onboarding_build_finished`, `personal_reveal_viewed`, `personal_reveal_cta_tapped`
14. `subscription_screen_opened` + `paywall_shown` {trigger_feature: post_onboarding}
15. `subscription_product_selected` {product_type: starter_package}, `subscription_purchase_started` {product_type: starter_package} (no `post_onboarding_offer_option_selected`, the starter pack is preselected)
16. backend `one_time_receipt_received`, `one_time_purchase_completed`, `trial_ended` {outcome: converted, trial_type: signup, product_id: ms_starter_package}
17. client `subscription_purchase_completed` {product_type: starter_package, server_confirmed: true}
18. `post_onboarding_offer_result` {result: purchased_starter, option_selected: starter}
19. (hole) after-purchase Welcome: no view event from the offer, no button event (rows 111, 112)
20. `push_prompt_viewed` and onward as in (a)

Verdict: reconstructable, with one hole (step 19) and one accuracy risk. The risk is row 63: SubscriptionCubit also reacts to the starter transaction, so this journey can contain a phantom `subscription_verification_failed` (Android) or a second `subscription_purchase_completed` plus `result: purchased_annual` instead of `purchased_starter` (iOS). The 5 vs 7 branch is identified by `total_steps`; a user who resumes after a kill directly on step 6 has no `total_steps` at all (accepted, see section 6).

### (c) Trial user: trial bar -> paywall -> annual purchase -> Welcome -> Home

1. `trial_bar_viewed` {days_left}
2. `trial_bar_tapped` {days_left}
3. `$screen` subscription + `subscription_screen_opened` + `paywall_shown` {trigger_feature: trial_banner, plans_shown}
4. `subscription_product_selected` {subscription_type: yearly} (automatic, the preselected plan)
5. `subscription_purchase_started` {subscription_type: yearly}
6. backend `subscription_receipt_received`, `subscription_purchase_completed`, `trial_ended` {outcome: converted, trial_type: signup}
7. client `subscription_purchase_completed` {subscription_type: yearly, server_confirmed: true}
8. `$screen` premiumWelcome
9. (hole) which Welcome button was used: no event (row 112)
10. `$screen` mainPage

Verdict: reconstructable. `trigger_feature` exists only on step 3, so the purchase is attributed to the trial bar by order within the session, not by a property (row 105). Step 6 and step 7 are the same fact under the same name (row 95): an insight that does not filter by `$lib` counts this purchase twice.

### (d) Free user hits zero on After therapy -> paywall -> dismiss

1. `usage_chip_tapped_at_zero` {feature: after_therapy, entry_point}
2. `$screen` subscription + `subscription_screen_opened` + `paywall_shown` {trigger_feature: premium_gate_after_therapy}
3. `subscription_product_selected` (automatic)
4. (hole) dismiss: no event (row 103)

Verdict: NOT reconstructable to the end. The "did nothing" branch is the absence of a purchase event followed by another `$screen`. `paywall_dismissed` exists in the taxonomy but only fires from the premium-active view (row 110). Also unknown before step 1: how many free users saw the chip at 1 or 0 at all (row 76).

### (e) Trial expires unconverted: day-3 sheet -> "Not now" -> trial ended -> trial-ended paywall -> monthly purchase

1. `trial_reminder_sheet_shown` {days_left: 1, therapy_entries_count, recordings_count, reflect_messages_count}
2. `trial_reminder_sheet_result` {result: not_now}
3. backend `trial_ended` {outcome: expired, trial_type: signup} (hourly job)
4. next open: `$screen` subscription + `subscription_screen_opened` + `paywall_shown` {trigger_feature: trial_ended_popup}
5. `subscription_product_selected` {yearly} (automatic), then `subscription_product_selected` {monthly} (tap)
6. `subscription_purchase_started` {subscription_type: monthly}
7. backend `subscription_receipt_received`, `subscription_purchase_completed` (no second `trial_ended`: the trial was already closed as expired, which is correct and reads as a win-back)
8. client `subscription_purchase_completed` {subscription_type: monthly}
9. `$screen` premiumWelcome

Verdict: reconstructable. Two caveats. If the user had tapped "Keep Premium" in step 2, the paywall would carry `trigger_feature: trial_banner` and be indistinguishable from a Home bar tap except by the preceding sheet event (row 89). On iOS a cancel at step 6 leaves no event (row 97).

## 3. Checks

**Does every paywall entry carry `trigger_feature`?** Yes for the entry itself. Every push goes through `MsRoutes.subscriptionRouteWithTrigger` (`navigation/ms_routes.dart:237`) and an external link falls back to `deep_link` (`:229`). Values in use: `post_onboarding`, `trial_banner`, `trial_ended_popup`, `drawer_menu`, `premium_gate_before_therapy`, `premium_gate_after_therapy`, `premium_gate_between_sessions`, `premium_gate_reflect_messages`, `premium_gate_session_recordings`, `premium_gate_session_recording`, `premium_gate_habits`, `premium_gate_reflect_voice`, `premium_gate_monthly_audit`, `deep_link`. Three problems: the day-3 sheet reuses `trial_banner` (row 89), the recording feature has two spellings (row 78), and no event after `paywall_shown` carries the trigger (row 105). `settings` and `onboarding` are defined but have no call site.

**Same fact on client and backend?** Yes, four cases, all older than this batch but all on this batch's main path:
- `subscription_purchase_completed`: client (`subscription_cubit.dart:298`) and backend (`users.py:563`), same name.
- `subscription_verification_failed`: client (`subscription_cubit.dart:280`, `starter_package_cubit.dart:166`) and backend (`users.py:592`, `:611`), same name.
- `reflect_limit_hit`: client (`reflect_chat_cubit.dart:594`) and backend (`reflect.py:939`), same name.
- Starter pack purchase: client `subscription_purchase_completed` {product_type: starter_package} and backend `one_time_purchase_completed`, different names, same fact.
`trial_started` / `trial_ended` are backend-only, as the spec requires. `consent_granted` is used by both sides but for different consent types (client `gdpr`, backend `PROFILING` / `ARTICLE9_HEALTH`), so it is not a duplicate.

**Events that can fire twice for one action?**
- Row 63: both store cubits alive on the offer and on the paywall; SubscriptionCubit does not filter by product id while StarterPackageCubit does (`starter_package_cubit.dart:143`). Both cubits already coexisted on the old subscription screen, but the starter pack is now the preselected option of the offer, so the exposure is much larger.
- Row 93: `subscription_product_selected` on mount and after every reload.
- Row 49: `onboarding_lead_source_other_text` up to four times.
- Row 26: `consent_screen_viewed` and `onboarding_legal_gate_abandoned` on resume. This one is new in this batch: before the redesign PageView page 0 was the "DIVE IN" splash and the gate was page 1.
- Row 16: `onboarding_step_viewed` (personalise) when the screen opens on Check email.
- Row 102: a restore that returns several past transactions logs several `subscription_restore_completed`.
- Guarded correctly (once): `paywall_shown`, `subscription_screen_opened`, `post_onboarding_*`, `personal_reveal_viewed`, `push_prompt_*`, `first_capture_prompt_shown` in the flow, `trial_bar_viewed`, `usage_load_failed`, `post_onboarding_offer_result`.

**Identify after consent, after the sign-up changes?** The client side is intact. New users are identified in `acceptConsent` (`therapy_onboarding_cubit.dart:272`) before the pending profile is flushed; returning users after a successful profile fetch (`auth_cubit.dart:208`, `:276`, `:376`, `splash_screen.dart:597`). Removing the "Success!" screen and routing existing social accounts through `PostLoginDestinationResolver` did not move any identify call. Events before consent (`welcome_cta_tapped`, `signup_*`, personalise step) stay anonymous and merge on identify. Two notes on the backend: `user_registered`, its identify call and now `trial_started` run before consent, keyed to the anonymous id from the header and to the Firebase UID when the header is missing; and the hourly job emits `trial_ended` with the UID for accounts that never consented (row 116).

**Plan cohorts (free / trial / premium)?** Not possible today (row 119). `subscription_tier` is written as `free/premium` by the client at login, `basic/premium` by `POST /users/`, and `free/premium_monthly` by `refresh_behavioral_properties` (its `premium_annual` branch is unreachable). A trial user is `premium` or `premium_monthly`, a starter-pack user too. Event-based workaround until fixed: trial = `trial_started` {trial_type: signup} without a later `trial_ended`.

**Screen-view mechanism for the new routes and steps?** `$screen` covers the routes welcome, auth, signUp, therapyOnboarding, wow, subscription, premiumWelcome, mainPage. The single `/wow` route emits one `$screen`; its five steps are covered by `post_onboarding_build_viewed`, `personal_reveal_viewed`, `paywall_shown` {post_onboarding}, `push_prompt_viewed`, `first_capture_prompt_shown`. Not covered by anything: Check email (row 21), the after-purchase Welcome when opened from the offer (row 111), the Reflect limit panel (row 85), the paywall error view (row 92).

## 4. Privacy

Properties that can contain user-written text or a health detail:

| Property | Event | Verdict |
|---|---|---|
| `first_50_chars` | `onboarding_lead_source_other_text` | **Violation.** Raw user text, sent to PostHog and to Firebase Analytics. Row 48. |
| `total_steps` (7 vs 5) | onboarding step events, `onboarding_completed` | Proxy for "currently in therapy". It is only 7 when Art.9 consent is active, so it is emitted after the consent that covers this data. Operator awareness needed, see section 6. |
| `in_therapy`, `has_schedule`, `variant=in_therapy`, `prompt_variant=therapy_cta` | `post_onboarding_build_viewed`, `personal_reveal_viewed`, `push_prompt_*`, `first_capture_prompt_*` | Same health detail, as a boolean. Same reasoning and same decision as above. |
| `distinct_id` = Firebase UID without consent | backend `trial_ended` {expired} | Consent problem, not text. Row 116. |

Checked and clean:
- Full name, greeting name: never in an event. Guarded by `screens/wow/wow_cubit_test.dart:420`.
- Orca name: stays in `WowScreenParams` and the backend call, never in an event.
- Focus area names (including custom ones): only `focus_area_count`.
- Goal text, therapy duration, modality "Other" text: sent to the backend only.
- Gender self-describe: the free-text field is not wired into the value; `gender` is mapped to the enum before it reaches identify.
- Promo code: `promo_code_applied` carries `success` and `failure_reason` only.
- Email: not in any event or person property.
- `product_title`: store metadata, not user text.
- `user_id` (Firebase UID) is added as an event property by `withUserParams` on the `subscription_*` events. It duplicates the distinct id and is not free text.
- Session replay is on with `maskAllTexts` and `maskAllImages` (`core/analytics/posthog_service.dart:109-112`), which covers the new inputs (name, custom focus area, goal, orca name, promo code).

## 5. Gaps to close (work order)

Ordered by damage to the funnel. Each item: event, properties, file, test.

### flutter-mobile

**G1. Paywall close is invisible (rows 103, 110). Blocks journey (d).**
- Event: `paywall_dismissed` (existing name). Properties: `trigger_feature`, `selected_plan` (annual/monthly), `purchase_attempted` (bool), `dwell_ms`, `dismiss_method` (close_x/system_back).
- Fire from a new `SubscriptionCubit.trackPaywallDismissedOnce()`, called by the close X in `screens/subscription/subscription_body.dart:107` and by a `PopScope` on the same widget. Only when `paywall_shown` was logged and no purchase completed.
- Stop firing `paywall_dismissed` from `screens/subscription/widgets/premium_view.dart:88`; replace with `premium_view_closed` (see G12).
- Test: `test/screens/subscription/cubit/subscription_cubit_analytics_test.dart` (once, with trigger, not after a purchase) and `test/screens/subscription/subscription_body_test.dart` (X and system back).

**G2. SubscriptionCubit handles starter-pack transactions (row 63).**
- In `screens/subscription/cubit/subscription_cubit.dart:243`, skip every `PurchaseDetails` whose `productID` is `starterPackProductId` (or is not one of the loaded subscription product ids). No event, no state change, no `completePurchase`.
- Test: `subscription_cubit_analytics_test.dart`: a `purchased` starter transaction on the stream produces no event, no `markAsSubscribed` call and no `PurchaseSuccessfulState`. `test/screens/wow/wow_screen_test.dart`: a starter purchase logs `post_onboarding_offer_result` {result: purchased_starter} exactly once.
- Ask `posthog-data-extractor` whether production already shows `subscription_purchase_completed` with `product_id = ms_starter_package` and `subscription_type = unknown`; that confirms or refutes the code-derived reading.

**G3. Cancel and store error are silent on iOS (row 97).**
- In the `!isPurchased && !isRestored` branch (`subscription_cubit.dart:248-258`, `starter_package_cubit.dart:148-155`) log `subscription_purchase_failed` before completing: `failure_reason` = `user_cancelled` for `PurchaseStatus.canceled`, otherwise `_classifyFailureReason(error)`. Add `failure_reason` to every failed event in `StarterPackageCubit` (it has none today).
- Test: `subscription_cubit_analytics_test.dart` and `test/screens/main_page/daily_page/cubit/starter_package_cubit_test.dart` with a fixture that has `pendingCompletePurchase: true` and `status: canceled` / `error`; assert exactly one failed event.

**G4. `server_confirmed` is not actually confirmed (row 96).**
- `providers/subscription/subscription_repository.dart`: `markAsSubscribed` and `markAsOneTimePurchased` must throw when the response `status` is not `VERIFIED`. The cubits then take their existing verification-failed path.
- Test: a repository or cubit test with a stubbed `{status: FAILED}` response: no `subscription_purchase_completed`, one `subscription_verification_failed`, no `completePurchase`.
- This is also a logic defect (the user would see the Welcome screen without Premium), so report it to the lead beyond analytics.

**G5. Purchase events have no `trigger_feature` (row 105).**
- Add `trigger_feature` to `subscription_product_selected`, `subscription_purchase_started/completed/failed`, `subscription_restore_*`, `subscription_verification_failed` in `subscription_cubit.dart`. Give `StarterPackageCubit` a `configureContext(triggerFeature)` called from `subscription_screen.dart:114` and `wow_screen.dart:80`, and add the property to its events.
- Test: extend `subscription_cubit_analytics_test.dart` ("carries the trigger_feature configured via configurePaywallContext" for each event) and `starter_package_cubit_test.dart`.

**G6. Spurious consent-screen events on resume (row 26).**
- `screens/therapy_onboarding/views/onboarding_legal_gate_view.dart`: fire `consent_screen_viewed` once, the first time the state is `TherapyOnboardingLoaded` with `currentScreen == 0`, not in `initState`. Set `_loadedStateSeen` only in that same case, so `onboarding_legal_gate_abandoned` cannot fire for a user who was never on the gate.
- Test: `test/screens/therapy_onboarding/onboarding_legal_gate_view_test.dart`: with a loaded state at `currentScreen: 3` (and with `completed`), pump and dispose; assert neither event fired. With `currentScreen: 0`, assert `consent_screen_viewed` once.

**G7. Free text in `onboarding_lead_source_other_text` (rows 48, 49).**
- Remove `first_50_chars`. Keep `text_length`. Fire once, from the primary button path only (`onboarding_lead_source_view.dart:89`); drop the calls in `onSubmitted`, `onEditingComplete` and the check icon.
- Test: `test/screens/therapy_onboarding/onboarding_lead_source_view_wave4_test.dart`: the event has exactly the key `text_length`, no property value equals the typed text, and it fires once.

**G8. Day-3 sheet shares the Home bar trigger (row 89).**
- New constant `triggerFeatureTrialReminder = 'trial_reminder'` in `core/analytics/analytics_events.dart`; use it in `managers/trial_popup_manager.dart:177`; map it to the trial variant in `screens/subscription/paywall_context.dart:111`.
- Test: `test/screens/usage/trial_visibility_test.dart` (the pushed route) and `test/screens/subscription/paywall_context_test.dart` (variant).

**G9. Skips look like completions (rows 38, 40, 42, 47).**
- Add `outcome` (`saved`/`skipped`) to `onboarding_step_completed` for step_index 3, 4, 5, 7 in `therapy_onboarding_cubit.dart` (`skipJourney`, `skipModality`, `skipSchedule`, `skipLeadSource` pass `skipped`).
- Test: `test/screens/therapy_onboarding/therapy_onboarding_cubit_branching_test.dart`: one case per skip method.

**G10. Account screen is blind (rows 6-9, 12, 19).**
- `auth_method_tapped` {`mode`: sign_up/log_in, `method`: email/google/apple} in `screens/auth/auth_body.dart:137` (after validation passes) and in `animated_google_apple_widgets.dart:79`, `:91`.
- `auth_validation_failed` {`mode`, `reason`: email_empty/email_invalid/password_empty/password_short/terms_not_accepted} in `auth_body.dart` `_handlePrimaryCtaTap`.
- `auth_mode_switched` {`to`: sign_up/log_in} in `auth_body.dart:80`.
- `login_failed` {`method`, `error_type`: invalid_credentials/email_not_verified/cancelled/network/unknown} in `screens/auth/cubit/auth_cubit.dart:166`, `:176`, `:320`, `:419`.
- `signup_failed` {`error_type`: backend_provisioning_failed, `method`: oauth} around the body of `registerForGoogleAndApple` (`sign_up_cubit.dart:257`), with a try/finally that closes the loading overlay.
- Test: `test/screens/auth/auth_body_test.dart` (tap, validation, switch) and a new `test/screens/auth/auth_cubit_analytics_test.dart`; `test/screens/sign_up/sign_up_cubit_gdpr_test.dart` for the oauth failure.

**G11. Check email is blind (rows 16, 21-24).**
- `signup_email_verification_viewed` (when `SignUpCheckEmailState` is first shown), `signup_email_verification_resent` {`success`}, `signup_email_verified` {`wait_seconds`}, `signup_email_verification_abandoned` (sign out), all in `screens/sign_up/cubit/sign_up_cubit.dart` (`loadCheckEmailScreen`, `checkIfUserIsRegistered`, `resendVerificationEmail`, `checkEmailVerification`, `signOut`).
- Move `_trackPersonaliseViewed()` out of the constructor so it does not fire when `checkIfUserIsRegistered(true)` opens the screen on Check email.
- Test: `test/screens/sign_up/personalise_step_analytics_test.dart` (no personalise event in the registered case) plus a new group for the four events.

**G12. Premium-active view and after-purchase Welcome (rows 106, 107, 110-112).**
- `premium_view_shown` {`variant`: store/trial/promo/starter, `trigger_feature`} in `screens/subscription/widgets/premium_view.dart` `initState`; `premium_manage_tapped` {`variant`} at `:68`; `premium_view_closed` at `:88`.
- `premium_welcome_viewed` {`entry`: paywall/post_onboarding_offer} and `premium_welcome_action` {`action`: open_after_therapy/start_after/start_record/start_monthly/back_home/system_back} in `screens/subscription/premium_welcome_screen.dart` (convert to a StatefulWidget for the view event; `entry` from `onBackHome != null`).
- Test: `test/screens/subscription/premium_view_test.dart`, `test/screens/subscription/premium_welcome_screen_test.dart`.

**G13. Usage chip states are not observable (row 76).**
- `usage_snapshot`, once per app session after the first successful load in `screens/usage/cubit/usage_cubit.dart` `_load`. Properties: `plan`, `before_therapy_left`, `after_therapy_left`, `between_sessions_left`, `reflect_messages_left`, `session_recordings_left`, `features_at_zero` (count). Numbers only.
- Test: `test/screens/usage/usage_model_and_cubit_test.dart`: fires once across two loads; values for free, trial, premium.

**G14. Reflect limit panel (rows 85, 86).**
- `usage_limit_panel_shown` {`feature`: reflect_messages} once per thread visit, and `usage_chip_tapped_at_zero` {`feature`: reflect_messages, `entry_point`: reflect_limit_panel} on the button at `screens/reflect_tab/widgets/reflect_usage_indicator.dart:144`. New constant `usageEntryPointReflectLimitPanel`.
- Test: a widget test for `reflect_usage_indicator.dart` (none exists for these events).

**G15. `subscription_product_selected` auto-fires (row 93).**
- Add `selection_source` (`default`/`user`/`cta`) in `subscription_body.dart:52`, `:72` and `post_onboarding_offer_view.dart:61`, `:69`.
- Test: `test/screens/subscription/subscription_body_test.dart`.

**G16. Recording trigger has two spellings (row 78).**
- Keep the shipped value `premium_gate_session_recording`. Give `UsageFeature` a `triggerKey` (equal to `apiKey` except `session_recording`) and use it in `usage_gate.dart:57`.
- Test: `test/screens/usage/usage_chip_and_gate_test.dart`.

**G17. Small additions.**
- `paywall_load_failed` {`trigger_feature`, `error_type`} in `subscription_cubit.dart:144` (row 92). Test in `subscription_cubit_analytics_test.dart`.
- `paywall_promo_expanded` {`trigger_feature`} in `paywall_promo_section.dart:69` (row 100). Test: a widget test for the promo section.
- `legal_link_opened` {`surface`: welcome/agreements/offer/paywall/premium_view, `link`: terms/privacy} in `welcome_body.dart:186`, `onboarding_legal_gate_view.dart:88`, `subscription_legal_links.dart:44` (rows 4, 31, 66, 104). Test: one widget test per surface.
- Counts on step completion (rows 34, 43, 45): `focus_area_count`, `custom_focus_area_count` (step 1); `frequency` (enum), `session_count`, `custom_session_count` (step 5); `archetype` (enum), `orca_color` (enum) (step 6). Never names. Test in `therapy_onboarding_cubit_branching_test.dart`.
- `onboarding_step_save_failed` {`step_index`, `step_name`} in each `catch` of `therapy_onboarding_cubit.dart`, `onboarding_load_failed` at `:205` (rows 29, 52). Test in the same file.
- `onboarding_language_changed` {`to`} at `onboarding_legal_gate_view.dart:330` (row 32).
- `source` (`pre_prompt`/`cold_prompt`) on `notification_permission_*` in `services/fcm_token_service.dart:75-88`.

**G18. Stop writing `subscription_tier` from the client** once G20 ships (`screens/auth/cubit/auth_cubit.dart:92-126`). Update `test/core/analytics/posthog_identify_behavioral_test.dart`.

### backend-api

**G19. Decide the owner of the purchase fact (rows 95, 98; operator decision needed).**
- Recommended: the backend owns "money arrived" (`subscription_purchase_completed`, `one_time_purchase_completed`, `subscription_verification_failed`), because it is the only side that knows. The client keeps `subscription_purchase_started`, `subscription_purchase_failed` and a new `purchase_flow_finished` {`result`, `trigger_feature`, `product_type`} for the UI outcome, and stops emitting the two shared names. Existing insights must be re-pointed in the same release.
- Until that ships: every insight on these two events must filter `$lib`.
- Backend part: add a test that pins `subscription_purchase_completed` and `one_time_purchase_completed` properties (`test_subscription_data_resubmission.py`, `test_starter_pack_premium_source.py`), since they become the only source.

**G20. One plan person property (row 119).**
- New person properties `plan` (`free`/`trial`/`premium`) and `premium_source` (`signup_trial`/`purchase`/`starter_pack`/`promo`), set with `$set` on `trial_started`, `trial_ended` (both outcomes), `subscription_purchase_completed`, `one_time_purchase_completed`, `promo_code_applied` (success), and inside `refresh_behavioral_properties`, all through `plan_usage_service.resolve_plan` so the property and `GET /users/usage` cannot disagree. Leave `subscription_tier` as is for old dashboards, but fix the unreachable `premium_annual` branch or drop it.
- Files: `app/services/posthog_service.py` (`capture_signup_trial_started`, `capture_trial_ended`, `refresh_behavioral_properties`), `app/api/v1/endpoints/users.py` (`_capture_payment_event` call sites).
- Test: `app/tests/test_subscription_onboarding_redesign.py` (assert `$set.plan` on each event), `app/tests/test_behavioral_posthog.py`.

**G21. `trial_ended` without consent (row 116; security-guardian decision in stage 6.4).**
- Option A: in `deactivate_expired_subscriptions` (`app/services/subscription_service.py:279-285`) skip the PostHog emission (still close the trial row) when the user has no `gdpr_consent_at` in the therapy context.
- Option B: accept, on the ground that the event carries no personal data beyond a pseudonymous id.
- Test for A: `app/tests/test_trial_lifecycle_events.py`: no capture for a user without consent, the DB row is still closed.

### qa-testing

**G22. Tests for events that exist but are asserted nowhere** (test column `NONE` on an OK row): `welcome_cta_tapped`, `user_logged_in`, `signup_started`, `signup_method_selected`, `signup_failed`, `onboarding_started`, `onboarding_completed`, `onboarding_step_back`, `consent_screen_viewed`, `consent_granted`, `onboarding_legal_gate_gate_ready`, `onboarding_legal_gate_abandoned`, `subscription_purchase_started`, `notification_permission_*`, Reflect path of `usage_chip_tapped_at_zero`; backend `user_registered`, `promo_code_applied`, `subscription_receipt_received`, `ai_processed` on the three created events, backend `consent_granted` for Art.9. Extend the wow privacy guard pattern (`wow_cubit_test.dart:420`) to onboarding: no event property equals a typed name, focus area, goal or orca name.

## 6. Accepted as is (with reason)

Each of these needs the operator's explicit acceptance under the CLAUDE.md rule.

1. **Post-onboarding flow has no step index.** The five steps use five different event names in a fixed order, which gives the same funnel as a step index would. Adding `flow_step_index` is cosmetic.
2. **`total_steps` is absent on steps 0 to 2 and when resuming directly on step 6.** The branch is unknown before step 3 by design; the resume case is rare and `onboarding_completed` still lacks it only then.
3. **`total_steps` and `in_therapy` reveal the therapy status.** They are booleans or enums, emitted only after the Art.9 consent that covers this data, and the funnel split by branch is the point of the redesign. Flag to security-guardian in stage 6.4.
4. **`signup_method_selected` says `oauth`, not google or apple.** The platform person property and backend `user_registered.auth_provider` give the exact provider. G10 adds the exact value at the tap.
5. **`notification_permission_granted` and `push_prompt_result` {accepted} overlap.** The first is the OS answer from every entry point (including the cold prompt for existing users), the second is the pre-prompt funnel step with the `not_now` and skipped branches. Count grants from `notification_permission_granted` only.
6. **`consent_granted` is emitted by both sides** for different consent types (`gdpr` on the client, `PROFILING` and `ARTICLE9_HEALTH` on the backend). Different facts; always filter by `consent_type`. The value casing differs and stays, the names are shipped.
7. **`GET /users/usage` has no backend event.** A read endpoint called on every Home load; failure is visible through the client `usage_load_failed`.
8. **`onboarding_step_completed` (personalise), `signup_started`, `signup_method_selected` repeat on a retried registration.** Documented behaviour, consistent with the rest of the step tracking; use unique users per step.
9. **Restore with nothing to restore produces no outcome event.** The store sends nothing in that case; inferring it needs a timeout. Low value.
10. **Offer abandoned by killing the app** leaves `paywall_shown` {post_onboarding} without `post_onboarding_offer_result`. That absence is the "did nothing" branch for this one screen and is acceptable because back is blocked and the only other exits are logged.
11. **`plans_shown` does not count the starter pack.** The starter product loads separately; `post_onboarding_offer_not_shown` {products_unavailable} covers the case that matters.
12. **Backend `reflect_limit_hit.messages_used` bucket `<10`** can no longer occur with a limit of 15. Harmless.
13. **Trial popup suppressed** (app tour pending, flow ran this session, usage unavailable) logs nothing. The popup shows on a later open and is logged then.
14. **`user_registered` and `trial_started` are emitted before the agreements screen**, on the anonymous id from the request header. No demographic or health data; existing design. Include in the stage 6.4 security review together with G21.

## 7. Recommended PostHog-side setup after release

Nothing below was created. First step after release: `posthog-data-extractor` confirms each new event actually flows (name, properties, `$lib`) before any number is reported. Always filter client events by `$lib = 'posthog-flutter'` (project note: DAU is inflated otherwise).

**Funnels**
1. Acquisition to first value: `$screen` welcome -> `welcome_cta_tapped` {sign_up} -> `onboarding_step_viewed` {-1} -> `user_registered` -> `consent_granted` {gdpr} -> `onboarding_completed` -> `personal_reveal_viewed` -> `first_capture_prompt_shown` -> `first_capture_prompt_option_tapped`. Breakdown: platform, `auth_provider`.
2. Onboarding steps: `onboarding_step_viewed` by `step_index` -1 to 7, two saved versions filtered on `total_steps` 7 and 5. Add the `outcome` breakdown once G9 ships.
3. Post-onboarding offer: `personal_reveal_cta_tapped` -> `paywall_shown` {post_onboarding} -> `subscription_purchase_started` -> `post_onboarding_offer_result`, broken down by `result`. Second insight: `post_onboarding_offer_not_shown` by `reason`.
4. Reminders: `push_prompt_viewed` -> `push_prompt_result`, by `result` and `variant`.
5. Paywall by entry: `paywall_shown` -> `subscription_purchase_started` -> backend `subscription_purchase_completed` or `one_time_purchase_completed`, breakdown `trigger_feature` (first-step attribution until G5 ships). Add `paywall_dismissed` as the exit step after G1.
6. Limit to purchase: `usage_chip_tapped_at_zero` -> `paywall_shown` -> purchase completed, breakdown `feature` and `entry_point`.
7. Trial lifecycle: `trial_started` {signup} -> `trial_bar_tapped` or `trial_reminder_sheet_shown` -> `trial_ended`, breakdown `outcome`. Win-back: `trial_ended` {expired} -> `paywall_shown` {trial_ended_popup} -> purchase completed.

**Trends and tables**
8. Day-3 sheet: `trial_reminder_sheet_result` by `result`; distribution of `therapy_entries_count`, `recordings_count`, `reflect_messages_count` for converters vs non-converters.
9. Free-limit pressure: `usage_last_free_note_shown` and `usage_chip_tapped_at_zero` per feature per week; after G13, share of free users with `features_at_zero > 0`.
10. Plain-text saves: backend `debrief_created`, `prep_card_created`, `between_session_created` with `ai_processed = false`, as the server-side count of limit hits.
11. Health: `usage_load_failed` by `error_class`, `subscription_verification_failed` (backend) by `failure_reason`, `subscription_purchase_failed` by `failure_reason` and platform (expect iOS near zero until G3 ships, which is the symptom of the bug).
12. First-step choice: `first_capture_prompt_option_tapped` by `choice` against day-1 and day-7 return.

**Cohorts** (after G20): `plan = trial`, `plan = free` with `trial_ended` {expired}, `plan = premium` by `premium_source`. Until then build them from events as described in section 3.

**One-off checks for `posthog-data-extractor`**
- G2 evidence: `subscription_purchase_completed` where `product_id = 'ms_starter_package'` and `subscription_type = 'unknown'`.
- G3 evidence: `subscription_purchase_failed` with `failure_reason = 'user_cancelled'` split by `$os`.
- G4 evidence: client `subscription_purchase_completed` without a backend `subscription_purchase_completed` for the same person within one minute.
