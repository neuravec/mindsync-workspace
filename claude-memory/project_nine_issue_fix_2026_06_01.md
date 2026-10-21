---
name: project-nine-issue-fix-2026-06-01
description: "2026-06-01 batch fix of 9 reported app bugs (onboarding/registration UI, reactive state, notifications, weekly/monthly summaries). IMPLEMENTED on disk, NOT committed/deployed."
metadata: 
  node_type: memory
  type: project
  originSessionId: 94b6bc39-12b3-4989-a285-b47b82295a02
---

2026-06-01 — fixed 9 user-reported bugs in one orchestrated pass. Status: IMPLEMENTED on disk (repo is NOT a git repo — no commit). NOT deployed. See [[feedback-memory-write-after-commit]].

**The 9 fixes (all additive, verified):**
1. Registration `personalise_view.dart`: nickname border teal-when-filled (driven from MsInput.enabledBorder call-site, ms_input.dart untouched); removed the 160px resting spacer in `gender_pronouns_selector.dart`; added back button → `context.go(MsRoutes.authRoute)`; replaced `MsSilverScrollView`+Padding(100) with `SafeArea`+`SingleChildScrollView` (fixes top-heading overflow on small iPhones).
2a. Onboarding keyboard cramping: `scrollPadding: EdgeInsets.only(bottom:120)` on all onboarding TextFields + `Scrollable.ensureVisible` on journey multiline fields; challenges view now hides header on keyboardOpen.
2b. Back stuck at card 4: added `TherapyOnboardingCubit.goToPreviousScreen()` (clamp at 1, legal-gate screen 0 stays irreversible); back-button delegates to cubit (was a stateless off-by-one `jumpToPage`).
2c. Time picker numeric keypad dead: ROOT CAUSE = global unfocus `GestureDetector` in `mind_sync_app.dart` stole focus from showTimePicker EditableText. Fixed to skip unfocus when focused widget is EditableText; added `initialEntryMode: TimePickerEntryMode.input`.
2d. Orca-name field closed after 1 char: dropped per-keystroke `setOrcaName` emit + `buildWhen` so BlocBuilder doesn't rebuild the field; name read on submit. `onboarding_companion_view.dart`.
3. Symptom add auto-advanced: removed `Navigator.pop()` in `symptom_tracking_section.dart` `_addSymptom()`; now resets form + stays open.
4. Lead-source "Other" needed 2 taps: added inline confirm IconButton reading controller directly (`onboarding_lead_source_view.dart`); the bottom CTA was `keyboardOpen`-gated so first tap only dismissed keyboard.
5. Inactive users got NO push: ROOT CAUSE = `RE_ENGAGEMENT` mapped to "REFLECTIONS" interest category, filtered out when user deselects the Reflections chip. Fix = `_INTEREST_FILTER_EXEMPT = {RE_ENGAGEMENT, THERAPY_PREP, POST_SESSION_REFLECTION}` in `notification_orchestrator.py`; re-engagement now gated only by `re_engagement_push` + master toggle.
6. No notification before/after a therapy session: legacy pre/post-session jobs are flag-disabled (hard cutover) and the orchestrator had no pre-session generator + its post-session one required a saved debrief. Fix in the moments framework: NEW `therapy_prep_generator.py` (THERAPY_PREP, schedule_driven, ~2h before next session); reworked `post_session_reflection_generator.py` to be schedule-driven (fires after session even with NO debrief; suppressed only if a debrief exists). Added a window-independent "Pass 2" in `run_daily` over all users with a therapy_schedule (bypasses the 10-19 window + daily cap for schedule-driven types). No new pref column (gated on notification_enabled + has-schedule; reuses post_session_nudge_delay_minutes).
7. UI stale until restart: ROOT CAUSE = `MainPageCubit` registered as GetIt **factory** (sl<>() ≠ provider instance) + non-reactive `.read()` consumers. Fix: factory→`registerLazySingleton` + `BlocProvider.value` in main.dart; greeting/drawer now `BlocBuilder<MainPageCubit>`; `settings_cubit.saveOrcaName/updateToneArchetype` now also call `sl<CharacterTabCubit>().loadCharacterCard()`. KNOWN residual: `MainPageCubit.signOut()` (file not edited) doesn't reset state → brief stale-name flash on re-login; recommend `userInfo=null; emit(loading)` there.
8. End-of-onboarding "save previous session" assumed therapy: `wow_screen.dart` now branches on `currentlyInTherapy` — yes_regular/yes_occasional → keep "Capture a past session"; null/not_right_now/never_been → 3-action menu (Reflect / Quick note / Track how you feel). Plumbed `currentlyInTherapy` through WowScreenParams + cubit cache. 4 new ARB keys × 7 langs.
9. Weekly/Monthly therapy summaries empty: feature was ALREADY built end-to-end; gap = over-strict cron gating (weekly hour==22 + therapy-day/Sun; monthly day==1 hour==6) + no on-demand creation. Fix: NEW `POST /api/v1/weekly-summaries/generate` + `POST /api/v1/monthly-audits/generate` (idempotent, reuse /retry logic; monthly free = activity-only no-AI, NO 403; /retry still 403s free); relaxed gating (weekly hour>=22, monthly day in 1..3) keeping dedup; FE "Generate now" CTA in empty states (`therapy_tab_screen.dart` + cubit `generateForFilter` + manager `generateLatest`).

**Migration:** NEW `qq7r8s9t0u1v_add_therapy_prep_moment_type.py`, down_revision `pp6q7r8s9t0u`, idempotent (ALTER TYPE ... ADD VALUE IF NOT EXISTS). New single head = `qq7r8s9t0u1v`.

**Verification:** flutter analyze 0 errors; build_runner + gen-l10n clean; 36/36 change-set Flutter tests + 56/56 new backend tests pass; the one regression (test_dedup_key_generators TestPostSessionReflectionDedupKey, obsolete debrief-keyed assertion) updated to schedule-driven format → 11/11 pass. Pre-existing red suite documented separately, see [[reference-pre-existing-test-baseline-2026-06-01]].

**OPERATOR FOLLOW-UPS (human-only):**
- Run `alembic upgrade head` on Heroku PROD manually (deploy ≠ migrate, no release phase). New head `qq7r8s9t0u1v`.
- Verify prod `moment_type_enum` contains THERAPY_PREP, POST_SESSION_REFLECTION, RE_ENGAGEMENT (UPPERCASE labels).
- Do NOT set `notification_legacy_jobs_enabled=True` (would double-send alongside the orchestrator).
- No migration needed for the summaries endpoints (reuse existing tables).
