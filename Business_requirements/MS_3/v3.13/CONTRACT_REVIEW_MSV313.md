# MSV3.13 Contract Review – CS-02 (`custom_interval_days` removal) + CS-01 (debrief-match rule)

Read-only review. No code changed, nothing pushed, Heroku untouched.

Backend reviewed: `wt-msv313-be` branch `msv3.13`, base `f4e27e8` (prod v547). At review time the branch had **two** commits:
- `3d4af04` – CS-02 (custom_interval_days removal end-to-end)
- `48ffdbc` – CS-01 backend (debrief-match 48h ceiling removed), landed while this review was in progress

Frontend reviewed: `wt-msv313-fe` branch `msv3.13`, base `73e5314` (dev), commits:
- `3fa50c7` – CS-02 (Flutter)
- `733444a` – CS-01 (Flutter)

Both branches were fully committed by the time this report was written, so all six review points below are based on the complete CS-01 + CS-02 diff on both sides.

## 1. GET/PUT `/api/v1/users/therapy-schedule` contract

**MATCH.**

Backend `TherapyScheduleResponse` (`app/schemas/schemas.py:1023-1046`, msv3.13):
```
schedule: List[TherapyScheduleEntry]
frequency: str = "weekly"
next_session_date: Optional[datetime] = None
next_session_at: Optional[datetime] = None
next_session_timezone: Optional[str] = None
custom_sessions: Optional[List[CustomTherapySession]] = None
```
`custom_interval_days` is gone from this class and from `TherapyScheduleUpdate` (`schemas.py:981-1020`).

Frontend `TherapyScheduleResponse` (`lib/api/models/settings/therapy_schedule_response.dart`, msv3.13) carries the identical six fields (`schedule`, `frequency`, `customSessions`/`custom_sessions`, `nextSessionDate`/`next_session_date`, `nextSessionAt`/`next_session_at`, `nextSessionTimezone`/`next_session_timezone`) and no `customIntervalDays` field (removed from the `@freezed` factory, `.freezed.dart`, and `.g.dart` – `wt-msv313-fe` diff `73e5314..msv3.13` on that file family).

`UsersManager.syncTherapySchedule` (`lib/api/api_managers/users_manager.dart:231-244`) dropped the `customIntervalDays` parameter and no longer puts `custom_interval_days` in the PUT body; every remaining field (`schedule`, `frequency`, `custom_sessions`) is unchanged. Endpoint side: `app/api/v1/endpoints/users.py:1418-1524` (GET/PUT) constructs the response with the same six fields on both handlers, and the PUT handler no longer reads or forwards `data.custom_interval_days` to `crud.update_therapy_schedule`.

Repo-wide grep confirms no live reference to `custom_interval_days` / `customIntervalDays` remains in either `app/` (outside tests and the two migration files, one historical add, one the new drop) or `lib/` (outside one stale comment in `onboarding_schedule_view.dart:123`, which renders nothing).

## 2. Old-build compatibility, both directions

**MATCH on all four sub-cases.**

**(a) OLD Flutter build PUTs `custom_interval_days` against the NEW backend.** `TherapyScheduleUpdate` has no `model_config` (default Pydantic v2 `extra="ignore"`), confirmed with a live interpreter check (`M.model_validate({'a':1,'b':2})` → extra key silently dropped, no error). Directly tested: `app/tests/test_therapy_frequency.py::test_put_with_legacy_custom_interval_days_key_is_ignored` (line 774) PUTs `{"custom_interval_days": 14, ...}`, asserts `resp.status_code == 200`, `"custom_interval_days" not in body`, and that the key was never forwarded to `crud.update_therapy_schedule`.

**(b) OLD Flutter build reads the NEW GET response (key absent).** Old FE model reads `(json['custom_interval_days'] as num?)?.toInt()`; a missing Dart map key returns `null`, so this parses to `null` on the existing nullable `int? customIntervalDays` field – no exception. Traced further: old `SettingsCubit._applySyncResponse` (`73e5314:lib/screens/settings/cubit/settings_cubit.dart:142`) calls `saveCustomIntervalDays(response.customIntervalDays)` → `null` → old `SharedPreferencesManager.saveCustomIntervalDays(null)` (`73e5314` version) calls `removeValue`, self-healing the stale local cache the next time the user saves any schedule change from an old build. Separately, old `MainTabCubit._refreshNextSessionFromBackend` (`73e5314:lib/screens/main_tab/cubit/main_tab_cubit.dart:709-727`) unconditionally overlays `nextSessionDateTime` with the backend's `effectiveNextSessionAt` on load/resume/1-minute timer regardless of local interval state, so even an old build that never touches Settings gets the corrected (now-null-for-interval-only-users) value promptly.

**(c) NEW Flutter build against the OLD backend (rollout window, response still contains the key).** `json_serializable`'s generated `fromJson` (`therapy_schedule_response.g.dart`) reads only the six named keys off the map; an extra `custom_interval_days` key present in the JSON is simply never accessed – no error. Directly tested: `test/api/models/settings/therapy_schedule_response_test.dart`, new case `'a response still carrying the legacy custom_interval_days key parses cleanly and ignores it'`. `users_manager_therapy_schedule_test.dart` adds `'the PUT body never contains a custom_interval_days key'`, locking the removal in at the wire level.

**Old build in Custom mode with a stored interval and no manual dates, post-deploy.** Backend `compute_next_session_date`'s custom branch (`app/utils/therapy_schedule_utils.py:118-129`, msv3.13) returns `None` when `custom_sessions` is empty – no interval fallback exists any more. That `None` propagates through `get_therapy_schedule_with_frequency` into `next_session_date`/`next_session_at` = `null` in the GET response. Per (b) above, both the old FE's local interval-based computation (self-healed to inert) and the periodic backend overlay converge on "no next session known" – `emptyHub`/set-therapy state, not an error. No crash path was found on either side for this configuration.

## 3. Deploy sequencing for the column drop

**Confirmed safe; sequence for STATUS.md:**

1. `models.UserPreferences` (`app/models/models.py:220-224`) no longer declares `custom_interval_days`. SQLAlchemy simply never selects or writes a column it doesn't know about — a live table still carrying the column is harmless (verified by reading every SELECT/INSERT/UPDATE path touched by this diff: `crud.py`'s `update_therapy_schedule` and `get_therapy_schedule_with_frequency`, `users.py`'s GET/PUT handlers — none reference the column post-diff).
2. `Base.metadata.create_all(bind=engine)` (`app/main.py`, boot-critical per CLAUDE.md) only creates missing tables/columns from the model; it never drops a column absent from the model but present in the live table. So deploying the new code before the migration leaves a harmless orphan column — no boot risk, no 500s.
3. The migration itself (`alembic/versions/m313a1b2c3d4_drop_custom_interval_days.py`) is idempotent: guarded by a live `sa.inspect(...).get_columns()` check on both `upgrade()` and `downgrade()`, mirroring the precedent in `c9x0y1z2a3b4` and `m312a4b5c6d7`. `down_revision = "m312a4b5c6d7"`, which matches the current confirmed prod alembic head — single linear chain, no branching.
4. Required order: **push code first, run `alembic upgrade head` second** (matches `STATUS.md`'s existing note and the migration's own docstring). Reversed order (migrate before deploying the old code) is not applicable here since the OLD code never depended on this column either after this diff is what's live — but the project's standing "deploy ≠ migrate" rule is still the operative one: migrate only after the new slug is live, never before.
5. No other pending migration sits between `m312a4b5c6d7` and `m313a1b2c3d4` on this branch — single-step migration, safe to run once as part of this batch's deploy.

## 4. Every other backend consumer of the schedule

**MATCH — all resolve from manual dates only; weekly/biweekly untouched.**

Grepped and diffed every file named in the task:

- `app/services/moments/add_therapy_date_generator.py`, `homework_reminder_generator.py`, `post_session_reflection_generator.py`, `record_session_generator.py`, `therapy_appointment_generator.py`, `therapy_prep_generator.py` — each only drops the `custom_interval_days=...` keyword argument from its `compute_next_session_date`/`compute_last_session_datetime` call; no other line changed in any of these six files' compute logic.
- `app/services/moments/between_sessions_note_generator.py` — same removal, plus `_lookback_hours_for_cadence(frequency, custom_interval_days)` → `_lookback_hours_for_cadence(frequency)`, hardcoding the custom-mode lookback to `(30 * 24.0) + 24.0` hours. This is the exact value the old formula `(custom_interval_days or 30) * 24.0 + 24.0` always produced once the field stopped existing (it was already `None` for every remaining custom user) — byte-identical outcome, not a behavior change.
- `app/services/notification_service.py`, `app/tasks/prep_card_auto_generate.py`, `app/tasks/weekly_observations.py` — same pattern, parameter dropped, no logic touched.
- `app/api/v1/endpoints/therapy_tracking.py` (`get_session_cycle_state`, `_lookback_hours_for_cadence`) — the CS-11 exception `is_custom_interval_only = frequency == "custom" and custom_interval_days is not None` is removed; a custom user with empty `schedule` and empty `custom_sessions` now correctly resolves to `no_therapy_set` (there is no third "interval-only" configuration left to except). `_lookback_hours_for_cadence` here mirrors the same hardcoded `(30*24)+24` as the moment generator's local copy.
- `app/utils/therapy_schedule_utils.py::should_generate_for_therapy_day` — the custom branch now checks only `custom_sessions` for tomorrow's date; the old `if anchor_date is not None and custom_interval_days: ...` fallback block is deleted outright, not merely defaulted.

**Weekly/biweekly diff check (byte-identical):** `git diff` on `therapy_schedule_utils.py`, `crud.py`, and all consumer files touches only lines containing `custom_interval_days`/`anchor_date`-for-custom or their surrounding docstrings/comments. No line inside a weekly- or biweekly-specific branch (`_next_weekly_occurrence`, `_last_weekly_occurrence`, the biweekly week-parity math, `compute_next_session_date`'s non-custom path) was touched by either commit. Confirmed by reading the full diff of `therapy_schedule_utils.py` and `crud.py::update_therapy_schedule`/`get_therapy_schedule_with_frequency` top to bottom.

## 5. CS-01 rule parity

**MATCH — landed on both sides during this review, rules are identical.**

At the start of this review only the Flutter CS-01 commit (`733444a`) existed; the backend commit (`48ffdbc`, "fix(therapy-tracking): remove 48h ceiling from debrief-match (MSV3.13 CS-01)") landed on `wt-msv313-be`'s `msv3.13` branch partway through this review and has been reviewed in full.

Flutter `debriefMatchesSession` (`lib/screens/main_tab/cubit/main_tab_cubit.dart:132-158`, msv3.13):
```
same local calendar day  OR  !debrief.createdAt.isBefore(sessionDateTime)
```
Backend `_debrief_matches_session` (`app/api/v1/endpoints/therapy_tracking.py:191-224`, msv3.13):
```
same local calendar day  OR  debrief_utc >= session_utc
```
Both: no upper time bound; a debrief strictly before the session on a different day still does not match (explicit negative test on each side). `_session_has_matching_debrief`'s DB query window end was widened from a fixed post-session ceiling to `datetime.now(timezone.utc)`, consistent with the new unbounded rule. `crud.py` has zero changes in the CS-01 backend commit (`has_debrief_for_session`, the separate ±12h function used by `post_session_reflection_generator.py`/`notification_service.py`, is untouched, confirmed by diff).

Test coverage is parallel on both sides: 49h, 60h/3 days, 6 days (Darek's exact repro), and 30 days late all assert a match; 1h-before-the-session-on-a-different-day still asserts no match. FE: `next_session_action_test.dart` + new `next_session_action_late_debrief_cs01_test.dart`. BE: `test_therapy_tracking_fix1_a12.py::TestDebriefLenientMatching`.

Note per the diagnosis and both commits' own messages: the backend endpoint this touches (`GET /therapy-tracking/session-state`) has zero callers in `mindsync-frontend/` today — this is a consistency fix for dead code, not the user-visible fix. The user-visible fix is entirely the Flutter-side `debriefMatchesSession` change, already landed and reviewed under point 1's response-model check (no contract field changed by CS-01 on either side — confirmed, `SessionCycleStateResponse`'s shape is untouched by `48ffdbc`).

## 6. Out-of-scope / "Do NOT touch" check

**Nothing found beyond spec scope.** Checked against the spec's explicit guardrails:

- Weekly/Biweekly frequency modes and logic: untouched (point 4 above).
- Custom calendar picker and its saved dates (`custom_therapy_sessions`, `CustomCalendarView`): not present in either diff; `therapy_frequency_selector.dart`'s diff only deletes the `_CustomIntervalInput` widget and its wiring, leaving `const CustomCalendarView()` exactly as it was.
- Therapists section: no file under that area appears in either diff.
- Notification types, copy, or lead times: no string/copy/timing constant changed in `notification_service.py`, the six moment generators, or any ARB/localization file beyond the deletion of the four `settings_customIntervalDays*` keys (which is the removed feature's own strings, not a notification).
- Countdown formats: `main_tab_cubit.dart`'s CS-01 diff touches only `debriefMatchesSession`; `betweenSessionsPrepWindow`, the 72h retarget logic, and all display/formatting code are untouched (confirmed via the full diff of that file — the only two functions changed are `debriefMatchesSession` and the two `_computeNextSession`/`_computeLastSession` custom branches for CS-02, which only remove the interval fallback, not the calendar-based computation or return shape).
- Capture flows themselves (`debrief_capture_cubit.dart`, `TherapyFlowLauncher`): not present in either branch's diff — confirmed by `git diff --stat` on both repos, neither file is listed.

One item worth flagging for the lead, not a mismatch: `PreferenceKey.customIntervalDays` was removed from the Dart `enum PreferenceKey` (`lib/services/preference_keys.dart`). This is safe — `PreferenceKeyExtension.key` returns `name` (the identifier string), not `.index`, so removing an entry mid-enum does not shift any other key's storage identity. Verified by reading the extension directly.

## Verdict

**GO.**

No mismatches found across the API contract, both old-build compatibility directions, backend consumer sweep, CS-01 rule parity, or scope-boundary check. The two open items are process, not code:

1. **CS-01 backend commit `48ffdbc` landed mid-review** — STATUS.md's wave table still shows this row as `IN_PROGRESS`/`PLANNED` in places; it is in fact done and reviewed clean. Recommend the lead update STATUS.md's wave 2 row for "CS-01 fix BE" to COMMITTED before wave 3 (qa-testing) starts, so QA runs against the final two-commit branch state, not a partial one.
2. **Deploy sequence for this batch** (backend): push `msv3.13` → `heroku run alembic upgrade head` (single-step, `m312a4b5c6d7` → `m313a1b2c3d4`) → verify. Frontend deploys independently once QA passes; no cross-dependency beyond the already-noted "CS-02 before CS-01" landing order, which both branches already satisfy.
