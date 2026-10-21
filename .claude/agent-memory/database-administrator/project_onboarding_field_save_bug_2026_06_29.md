---
name: project_onboarding_field_save_bug_2026_06_29
description: Quantitative DB proof that age_band / currently_in_therapy / lead_source fields never persist despite the same save flow writing gender correctly — field-specific bug, not row-specific
metadata:
  type: project
---

Diagnosed 2026-06-29 via dyno run.9157 on prod (1718 user_profile rows).

**Finding: definitively field-specific, not row-specific.**
Among the 1336 users where `gender IS NOT NULL` (save flow provably reached DB):
- age_band IS NOT NULL: 3 (0.22%)
- currently_in_therapy IS NOT NULL: 0 (0.00%)
- lead_source IS NOT NULL: 5 total all-time, but none overlap with the 3 age_band-filled rows

**Freshness confirmed (not a legacy data problem):**
- Last 90 days: 247 gender-filled users, 3 age_band filled (1.2%), 0 cit
- Last 30 days: 58 gender-filled users, 2 age_band filled, 0 cit
All 3 non-null age_band rows are recent (within 90d of migration ~2026-05-27).

**Consent gate is not the blocker:**
5 users with active ARTICLE9_HEALTH consent (`withdrawn_at IS NULL`): cit_not_null=0, age_band_not_null=0.
Consent rows write correctly; what's downstream of consent doesn't write the value.

**Q4 spot-check (3 age_band outliers):**
- 18-24: n=1 (gender=true, cit=false, lead_source=false)
- 25-34: n=2 (gender=true, cit=false, lead_source=false)
Even the rows with age_band still have no cit or lead_source. Likely test/admin accounts or a brief partial-fix window.

**Why:** Three fields (`age_band`, `currently_in_therapy`, `lead_source`) are missing from the save path — most likely absent from the Pydantic `UserProfileUpdate` schema OR from the CRUD update dict — added as Wave 1/3/4 columns in migration ~2026-05-27 but never wired into the update path.

**How to apply:** When asked about onboarding profile completeness or these specific fields, cite these counts. Direct `backend-api` to grep for `age_band` in `app/crud/` and `app/schemas/` — if it only appears in the model definition, the bug is at the persist layer. Direct `flutter-mobile` to confirm the payload includes these fields in the PATCH/PUT body.
