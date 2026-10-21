---
name: notification-service-patterns
description: DND/timezone helpers, FeatureEnum drift, notification-preferences null-fix, consent soft-gates in users.py
metadata:
  type: reference
---

## Notification DND + Query Optimization (Tasks 2.4 + 2.7)
- `is_do_not_disturb(local_dt, dnd_start=22, dnd_end=8)` accepts custom hours
  - Wrap-around (start > end): active when hour >= start OR hour < end
  - Non-wrapping (start < end): active when start <= hour < end; start == end = full 24h DND
- All DND call sites in notification_service.py read `dnd_start_hour`/`dnd_end_hour` from `notif_prefs`
- Index `ix_user_preferences_time_zone` added via migration `a0b1c2d3e4f5`
- Note (2026-07-03): `get_users_eligible_for_notification` in crud.py was REMOVED as part of Notification Cadence v3 cleanup — see [[notification_cadence_v3]]. Do not reference it as a live pattern anymore.

## FeatureEnum / featureenum Enum Drift (prod incident 2026-06-21)
- `FeatureEnum` in models.py and `featureenum` Postgres type must stay in sync — any new `track_usage("NEW_LABEL")` call needs both a FeatureEnum member AND a migration
- Pattern for new labels: one migration using `ALTER TYPE featureenum ADD VALUE IF NOT EXISTS 'LABEL'` (see uu1v2w3x4y5z); FeatureEnum gets matching member; test with test_featureenum_hero_insight.py pattern
- `log_token_usage` is fire-and-forget (try/except Exception at top level), so a missing label kills only the INSERT, not the calling job — BUT it still poisons the Postgres session in the dyno until closed
- Migration test pattern: import alembic migrations via `importlib.util.spec_from_file_location` NOT `import_module("alembic.versions.*")` — the latter fails because `from alembic import op` needs Alembic runtime context; OR use source-text assertions (see TestMigrationSource in test_featureenum_hero_insight.py). See also [[offline_verification]] for a fuller offline recipe (SQLite real-run + Postgres as_sql render).

## Notification Preferences 500 Bug (fixed on disk, not deployed, 2026-06-29)
- Root cause: `_load_json_prefs()` did `result.update(stored)` — stored JSON blob can have null for non-Optional fields (`dnd_start_hour: int`, etc.) → Pydantic v2 ValidationError → HTTP 500
- Fix: null-sanitization loop after `result.update(stored)` restores typed defaults for any key where `result.get(key) is None`
- Secondary: type-guard on `notification_interests` in get/update — if stored as non-list (bad migration), falls back to default list
- Files: `app/crud/crud.py` (`_load_json_prefs`, `get_notification_preferences`, `update_notification_preferences`)
- Tests: `app/tests/test_notif_prefs_null_fix.py` (21 tests)

## PUT /users/profile — Partial Update Safety (2026-06-29, on disk, not deployed)
- `payload = profile_data.model_dump(exclude_unset=True)` — exclude_unset prevents Pydantic from filling unset Optional fields with None and silently clearing DB values
- POST still uses `profile_data.dict()` (full dict needed for CREATE); exclude_unset only in PUT
- Test: `TestPutProfileExcludeUnset` in `app/tests/test_age_band.py` — patch `app.crud.crud.update_user_profile` to capture payload; assert missing fields absent

## Art.9 Soft-Gate for currently_in_therapy (2026-06-29, on disk, not deployed)
- Old behavior: `raise HTTPException(403)` when CIT arrived without Art.9 consent → blocked ALL fields including gender for 99.5% of users
- New behavior: silently `del payload["currently_in_therapy"]` when no consent; other fields proceed; 200 returned
- POST gate: after `profile_data.dict()`, check `profile_data_dict.get("currently_in_therapy") is not None and not is_consent_active(...)`
- PUT gate: after `model_dump(exclude_unset=True)`, check `"currently_in_therapy" in payload and payload["currently_in_therapy"] is not None and not is_consent_active(...)`
- Explicit null (clearing CIT) is always allowed — data minimization, no consent check
- Privacy: VALUE is never logged or sent to PostHog; field NAME only appears in `updated_fields` if consent active
- Tests: `TestCurrentlyInTherapySoftGate` in `app/tests/test_consent.py` (8 tests); 2 old 403 tests updated to 200
- Consent helper: `is_consent_active(db, user_id, "ARTICLE9_HEALTH")` imported from `app.crud.consent`; for patching use `"app.api.v1.endpoints.users.is_consent_active"`
