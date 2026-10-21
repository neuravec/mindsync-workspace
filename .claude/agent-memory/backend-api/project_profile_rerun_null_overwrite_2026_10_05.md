---
name: project-profile-rerun-null-overwrite-2026-10-05
description: POST/PUT /users/profile write contract after the onboarding re-run wipe fix (POST existing row = no write, PUT identity null ignored / "" clears); upsert_user_preferences reset trap
metadata:
  type: project
---

Commit `0f74b96` on branch `fix/profile-rerun-null-overwrite` (worktree `Heroku/MindSync-wt-profile`, from origin/main d1d93d0), NOT pushed, no migration.

Contract (lives in `app/services/user_profile_writes.py`):
- POST /users/profile, row exists: 200 + stored row, NO write at all (not even empty slots). flutter-mobile asked for this explicitly (FE 1277c02): fill-only merge would refill a name the user deliberately cleared with the Firebase displayName on a re-run. Race on the unique key: IntegrityError caught, rollback, same path.
- PUT /users/profile, full_name/pronouns/gender/age_band only: explicit null ignored, "" or whitespace clears (stored NULL). `UserProfileUpdate` schema accepts "" for gender/age_band. Every other field keeps explicit-null-clears (currently_in_therapy Art.9 path).

**Why:** Settings "Reset onboarding" re-ran the consent flush with no local JSON; POST 500 then PUT nulls wiped name+gender in prod (2 testers), companion lost first name and Polish grammatical gender.

**How to apply:**
- Never call `crud.upsert_user_preferences` with the POST defaults on an existing user: it OVERWRITES ai_language/time_zone to English/UTC (not create-only). The old POST only escaped this because it 500'd first.
- Accepted trade-off: an existing row with an empty name plus a pending sign-up JSON (rare cross-device case) is no longer repaired by POST; PostHog `profile_updated.unfilled_empty_fields` measures it.
- Full suite no longer fits one 10-min foreground call (7180 tests, ~13 min): split `ls app/tests/test_*.py` with `split -n l/4` and run 4 groups. See [[test-baseline-pytest-history]].
