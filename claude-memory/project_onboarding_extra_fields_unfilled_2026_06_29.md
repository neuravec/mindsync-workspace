---
name: project_onboarding_extra_fields_unfilled_2026_06_29
description: age_band ~empty in prod — root cause = destructive partial-PUT overwrite (BE no exclude_unset) + Account null-send; fixed on disk
metadata: 
  node_type: memory
  type: project
  originSessionId: 265b85f9-0735-4283-8ab9-5c8b981d47b2
---

Prod Postgres (2026-06-29, via heroku-dyno read-only): extra onboarding fields ~empty. `user_profile` n=1718: `age_band` 3, `currently_in_therapy` 0, `lead_source` 5, `gender` 1336 (77.8%). 30-day cohort (feature present throughout): age_band 2/79. Investigated via growth-analyst (PostHog) + [[reference_database_administrator_agent]] (DB) + flutter-mobile (FE trace) + backend-api (BE trace).

**ROOT CAUSE (refined — earlier "FE/BE save bug" hunch was too coarse):**
1. **PRIMARY — destructive partial-overwrite on backend.** `PUT /users/profile` used `profile_data.dict()` (NO `exclude_unset`) → Pydantic filled absent fields as None → crud `setattr` wiped them. `therapy_onboarding_cubit` calls `updateUserProfile({'lead_source'})` and `({'currently_in_therapy'})` as **single-field** updates → under old code these NULLED full_name/pronouns/gender/age_band/age. So age_band got wiped during therapy onboarding.
2. **SECONDARY — Account screen null-send.** `account_body.dart` built `Profile` without ageBand → sent `age_band:null` → re-cleared it (via same setattr). gender survived because account/auth paths re-sent gender WITH a value while age_band went null.
3. Onboarding SEND path is CORRECT (flutter verified end-to-end: personalise_view→sign_up_cubit→flushPendingProfile→Profile.toJson all carry age_band). The `if(ageBand!=null)` at therapy_onboarding_cubit ~L234 is the PostHog identify call, NOT the save path.
4. Residual genuine optional-skip (chip selector) is some fraction — measure post-deploy.

**FIXES (on disk, NOT committed/deployed — operator-gated):**
- BE: `users.py:863` → `model_dump(exclude_unset=True)`; 3 callers verified safe, explicit null still clears. +8 tests.
- FE: `account_body.dart` now sends ageBand. +test.
- **Verify after deploy:** re-run DBA on 30-day post-fix cohort (~2 weeks out). Fill rises → bug was the driver (done). Stays ~2.5% → genuine UX/optional-skip → product decision (make age_band prominent/less skippable, or drop like lead_source).

`lead_source` is DIFFERENT: persists when chosen (5 DB ≈ 6 PostHog picks) → low fill is behavioral, not a bug.

**`currently_in_therapy` (Art.9) — UNBLOCKED this session (on disk, not deployed; security-cleared):** FE added `currentlyInTherapy` to `Profile` with `@JsonKey(includeIfNull:false)` (null → key omitted, no klobber) + gated send on `art9HealthConsentActive`; consent capture already exists (`_Art9ConsentBanner` in onboarding_journey_view). BE replaced the `403` with a **soft-gate**: field present+non-null without active ARTICLE9_HEALTH consent → silently dropped (2xx, other fields saved); explicit null passthrough (data-min clear); uses `is_consent_active`. security-guardian audit = **CLEAR TO DEPLOY**, GDPR Art.9/7(3)/17 PASS, withdrawal→purge ALREADY implemented (`DELETE /consent/art9_health` clears value + sets withdrawn_at; FE+account-deletion cascade), zero leak to PostHog/OpenAI/Loops. 4 Low backlog: withdrawal 2-commit non-atomicity; GET `UserProfileResponse` carries field (always null, latent future-exposure); withdrawal source hardcoded; grant non-idempotent. DB schema drift bonus: prod has `country`,`about` columns absent from models.py. See [[project_post_update_analysis_2026_06_29]].
