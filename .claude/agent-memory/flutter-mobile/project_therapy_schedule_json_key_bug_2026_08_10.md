---
name: project-therapy-schedule-json-key-bug-2026-08-10
description: Root cause + fix for therapy_schedule persisting as "[]" for 100% of prod users — Freezed model missing @JsonKey snake_case mapping
metadata:
  type: project
---

Diagnosed and fixed (2026-08-10, dev commit 0ec26e9, local only, not pushed): `TherapyScheduleEntry`
(`lib/api/models/settings/therapy_schedule_entry.dart`) had no `@JsonKey` annotations, so `toJson()`
emitted camelCase `dayOfWeek`/`timeOfDay`. The backend's Pydantic `TherapyScheduleEntry` schema
(`app/schemas/schemas.py`) requires snake_case `day_of_week`/`time_of_day` (both required, non-optional).
Every `PUT /users/therapy-schedule` with a non-empty schedule 422'd on FastAPI request validation —
before `update_therapy_schedule`'s endpoint body even ran — and `UsersManager.syncTherapySchedule`'s
`catch (_) {}` best-effort wrapper swallowed it silently. An empty schedule (`[]`) has no items to
validate, so it always succeeded — which is why the DB column was "[]" for 100% of users who had ever
touched the schedule UI (add-then-remove-to-empty, or any call with an empty starting list succeeds;
every call with real entries always failed).

**Why:** No error surfaced anywhere (fire-and-forget sync, no toast/log on failure), so this was invisible
until `database-administrator` found the prod fill-rate anomaly (task #34, 2026-08-10).

**The tell that pinpointed it:** `CustomTherapySession` (a sibling model, `custom_therapy_session.dart`)
already had correct `@JsonKey(name: 'time_of_day')` / `@JsonKey(name: 'therapist_name')` annotations, and
its `custom_therapy_sessions` column *did* persist correctly for 6/138 users. Diffing the two models
(the task's own suggested method) found the missing annotations on `TherapyScheduleEntry` instantly.

**Fix:** Added `@JsonKey(name: 'day_of_week')` / `@JsonKey(name: 'time_of_day')` to `TherapyScheduleEntry`,
ran `build_runner`, committed regenerated `.freezed.dart`/`.g.dart`. Left `therapistId` unmapped/unmapped
to backend's `therapist_name` on purpose — it's a local-only `TherapistModel.id` (a client-generated id,
not a display name); mapping it would silently corrupt the backend's `therapist_name` field wherever it's
displayed (character-tab bio, prep-card "session with X"). Pydantic v2's default `extra='ignore'` behavior
means the unmapped `therapistId` key is harmlessly dropped server-side rather than erroring.

**How to apply:** Any new Freezed model whose JSON goes to this FastAPI backend MUST carry explicit
`@JsonKey(name: 'snake_case_field')` for every field — Dart/Freezed defaults to the Dart field's own
camelCase name with no auto-conversion, and this backend's Pydantic schemas have no camelCase
`alias_generator` (verified: only `model_config = ConfigDict(from_attributes=True)`, no aliasing). A
silent 422 swallowed by a `try/catch(_) {}` "best-effort" API call is a standing landmine pattern in this
codebase (see `UsersManager` — several sync methods use it) — when investigating "field never seems to
save" bugs, check for this pattern first, and diff against a sibling model that demonstrably *does* work.

See also [[patterns]] for other DioClient/API gotchas.
