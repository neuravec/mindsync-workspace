---
name: project-ios-google-legacy-client-2026-10-21
description: "iOS + Google stuck" accounts (PostHog-invisible, 0 onboarding) are an OLD app build signature, not a sign-in bug or bots; legacy shape = device_type set + no user_therapy_context
metadata:
  type: project
---

2026-10-21 diagnosis (report `db-reports/2026-10-21-ios-google-signup-stuck.md`): 30/34 iOS+gmail accounts 04-21.10 have "legacy shape": `user_profile.device_type` written at signup (client older than 2026-05-27 GDPR deferral), no `user_therapy_context`, age_band 0, zero consent_records, conversations only type JOURNAL (current clients: REFLECT), no PostHog SDK (added 2026-04-22). Real people (no bursts, Central-Asia tz UTC+5/+6, hand-filled name/gender, 9/30 chat). The 4 current-shape iOS+Google accounts onboarded 4/4. Legacy iOS grows since Aug (7, 13, 31/month); Android legacy faded out in July. Likely old iPhones on iOS 13-15 getting last compatible build (deploy target 13 -> 16 on 2026-04-30); not provable from DB.

**Why:** DB has no auth_provider and no app_version column; backend defaults missing `is_ios` to iOS, so platform attribution is shaky.

**How to apply:** For any onboarding/activation funnel from prod, split or exclude legacy shape (`p.device_type IS NOT NULL AND tc.id IS NULL`). Provider proxy = email domain. Open handoffs: server-side ART9 gate (legacy users chat with no consent), app_version capture, force-update decision.

Related: [[reference-dyno-script-per-query-txn]]
