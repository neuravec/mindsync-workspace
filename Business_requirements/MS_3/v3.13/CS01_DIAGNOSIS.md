# MSV3.13 CS-01 Diagnosis – "Your Session" card stuck after After Therapy

Read-only investigation. No code was changed. Backend head `f4e27e8` (MindSync, main, = prod Heroku v547). Flutter head `73e5314` (mindsync-frontend/mindsync_app, dev). All findings below are VERIFIED by reading the actual code paths end to end and, where noted, the existing test suite that encodes the current behavior as intended. No part of this report relies on inference alone.

## 1. Top-line answer

The Main card's state machine (`computeNextSessionAction` in `lib/screens/main_tab/cubit/main_tab_cubit.dart`) is already faithful to the CS-09 target chain and correctly returns to the "no next session known" / set-therapy state once a session's After Therapy note is recognized. The bug is one gate upstream of that: **the function that decides whether a submitted After Therapy note counts as "done" for the most recent session refuses to match it once more than 48 hours have passed** (or the note is written on a different calendar day than the fallback rule allows). Darek submitted After Therapy roughly six days after the 26 August session. The note was saved successfully, but the matching check rejected it, so the card kept re-deriving "session happened, no after-therapy note yet" forever, no matter how many times he completed the flow.

The identical rule, with the identical 48-hour ceiling, is duplicated on the backend in an endpoint the Flutter client does not currently call at all (`GET /therapy-tracking/session-state`). That backend copy is covered by its own test suite, which explicitly asserts the 48-hour cutoff as intended behavior today. It has no bearing on Darek's bug (the client never reads it) but should get the same fix so it does not become a second, contradictory copy of the same logic later.

## 2. State machine as actually implemented today

### Client-side (drives the Main card – this is the ONLY implementation the app uses)

All of this lives in `main_tab_cubit.dart`; the backend's parallel implementation (section 2b) is never consulted.

| State | Function / line | Condition | Card shown |
|---|---|---|---|
| Priority 0 – session happened, no debrief | `computeNextSessionAction`, main_tab_cubit.dart:216-221 | `lastSessionDateTime != null && !lastSessionDateTime.isAfter(now)` AND `!hasDebrief` | `sessionHappened` ("Session has ended…" / "After Therapy") |
| 1 – no next session known | main_tab_cubit.dart:223-225 | `nextSessionDateTime == null` (only reached once `hasDebrief` is true, or there was no past session at all) | `emptyHub` (set-therapy prompt) |
| 3/6 – prep already exists | main_tab_cubit.dart:231-233 | `matchingPrepCard != null` | `populated` ("View prep card") |
| 5 – Between Sessions | main_tab_cubit.dart:235-241 | `hasDebrief` true, `nextSessionDateTime` known, `now` more than 72h (`betweenSessionsPrepWindow`, line 153) before it | `betweenSessions` |
| 2/6 – Prepare | main_tab_cubit.dart:243 | fallback: next session known, no prep yet, within 72h or no debrief-gate applies | `populated` ("Prepare") |

`hasDebrief` (main_tab_cubit.dart:216-221) is computed as:
```
hasDebrief = latestDebrief != null && debriefMatchesSession(latestDebrief, lastSessionDateTime);
```
`debriefMatchesSession` (main_tab_cubit.dart:132-144) is the actual gate – see root cause below.

Inputs to this state machine and where they come from:
- `lastSessionDateTime` – **local-only**, from `_computeLastSession`/`_computeLastCalendarSession` (main_tab_cubit.dart:872-961), reading SharedPreferences (`custom_therapy_sessions`, schedule, frequency). This lookup is **unbounded** – it always finds the most recent past occurrence, however long ago, with no time-window cutoff. The backend's confirmed `next_session_date` is explicitly **not** overlaid onto this field (main_tab_cubit.dart:702-708, "the backend contract has no 'last session' field at all… there is nothing to overlay").
- `nextSessionDateTime` – local compute first, then **overlaid with the backend's confirmed value** from `GET /users/therapy-schedule` on load, on the 1-minute timer, and on app resume (`_refreshNextSessionFromBackend`, main_tab_cubit.dart:680-727). Verified: a `null` backend value legitimately overwrites a stale local non-null one.
- `latestDebrief` – `DebriefManager.getLatestDebrief()` → `GET /debriefs/latest` → `crud.get_latest_session_debrief` (MindSync/app/crud/crud.py:1092-1102), ordered by `session_date DESC`. Refreshed via `refreshDebrief()` (main_tab_cubit.dart:585-595), called from: the module's "After Therapy" button after the flow returns (main_tab_screen.dart:429), the FAB flow after it returns (main_page_body.dart:648), the capture cubit itself the instant the debrief is created server-side, from both the debrief and prep branches' success paths (`debrief_capture_cubit.dart:940`, unconditional – fires regardless of which entry point launched the flow), and the 1-minute `_onSessionClockTick` (main_tab_cubit.dart:467-471) as a self-healing retry. **All the wiring that could plausibly cause a "forgot to refresh" bug is present and redundant; this is not the defect.**
- Recomputation is pull-based but frequent enough to be effectively live: 1-minute timer, app-resume hook (`didChangeAppLifecycleState`, main_tab_cubit.dart:447-451), and the four direct post-submit calls above. `computeNextSessionAction`/`resolveNextSessionCardVariant` are pure functions re-evaluated on every rebuild from current cubit state (main_tab_screen.dart:350-356, 923-927) – there is no stale-cache/memoization bug here either.

### Server-side (built, tested, but currently unused by the client – dead code w.r.t. the Main card)

`GET /therapy-tracking/session-state` (`app/api/v1/endpoints/therapy_tracking.py:243-357`) implements an independently-written, more elaborate version of the same chain:

| State | Condition (get_session_cycle_state, lines 340-347) |
|---|---|
| `no_therapy_set` | no schedule, no custom sessions, and not a custom-interval-only config (line 276) |
| `debrief_cta` | a session occurred within `_DEBRIEF_CTA_RECENCY_WINDOW_HOURS` = 30h (line 153) AND no matching debrief |
| `prep_cta` | no prep card matches the current window |
| `between_sessions` | prep done AND debrief done |
| `scheduled` | prep done, debrief not done, but the 30h recency window has already lapsed (this is the fallback state nothing in the spec names – see §3.4) |

Verified with a repo-wide grep: **zero references** to `/therapy-tracking/session-state`, `SessionCycleStateResponse`, or `session_cycle_state` anywhere in `mindsync-frontend/`. This endpoint is only exercised by its own backend test file (`app/tests/test_therapy_tracking_fix1_a12.py`). It has no effect on what Darek sees.

Backend `next_session_date` computation is separately confirmed **correct** for CS-01's needs: `crud.get_therapy_schedule_with_frequency` (crud.py:1475-1617) recomputes `next_session_date` fresh on every `GET /users/therapy-schedule` call and self-heals the persisted column to `None` once every `custom_therapy_sessions` entry has passed with nothing future added (crud.py:1527-1608, explicit comment block citing this exact "custom sessions in the past with no replacement" case). `therapy_schedule_utils.compute_next_session_date`'s custom branch (lines 122-135) returns `None` correctly when `custom_sessions` yields nothing future and `custom_interval_days` is `None`. This part of the chain needs no fix.

## 3. Root causes, ranked

### 3.1 PRIMARY – debrief-match window rejects a late After Therapy submission (BOTH – FE is what matters, BE has an identical dead-code copy)

**VERIFIED**, including via the existing test suite that encodes it as intended:

- Frontend: `debriefMatchesSession` (main_tab_cubit.dart:132-144) returns true only if the debrief's `sessionDate` falls on the same calendar day as the session, **or** was created within 48 hours after it. `SessionDebrief.session_date` is stamped to `DateTime.now()` at submission time, not the actual missed session's time (`debrief_capture_cubit.dart:917`, `sessionDate: DateTime.now()`) – confirmed via `TherapyFlowLauncher.launch` (`lib/utils/therapy_flow_launcher.dart`), which passes no session-identifying data to the capture flow at all.
- The test file itself documents the 48h ceiling as deliberate: `test/screens/main_tab/cubit/next_session_action_test.dart:114-120`, test name `'created more than 48h after the session does not match'`, asserting `isFalse`.
- Backend duplicate: `_debrief_matches_session` (`app/api/v1/endpoints/therapy_tracking.py:173-200`), `_DEBRIEF_MATCH_WINDOW_HOURS = 48.0` (line 170), same same-day-or-48h rule, exercised by `app/tests/test_therapy_tracking_fix1_a12.py::TestDebriefLenientMatching::test_debrief_beyond_48h_and_different_day_does_not_match` (lines 447-461), which submits a debrief 3 days after a session and asserts `debrief_done is False` – i.e., today's backend test suite explicitly certifies the same defect as correct.
- Because `lastSessionDateTime` has **no matching time limit** on the client (it is found by an unbounded backward scan, main_tab_cubit.dart:872-961), the card keeps re-deriving "this session happened and needs a debrief" indefinitely – there is nothing that ever makes the stale session "expire" on its own. The only way out of `debriefCta` is a debrief that matches, and once 48 hours have elapsed nothing the user does in the After Therapy flow can ever satisfy that match. This is a genuine dead end, exactly matching "a week after the session date it still sits in the same state."

This single defect fully explains Darek's repro: Aug 26 18:00 session, After Therapy completed ~01.09 (≈6 days later, both a different calendar day and outside 48h) → `debriefMatchesSession` false → `hasDebrief` false forever → `computeNextSessionAction` returns `debriefCta` on every recomputation, regardless of how many times "After Therapy" is completed, regardless of whether a future session exists.

### 3.2 Confirmed NOT broken (regression risk only, no fix needed)

- The 72-hour Between-Sessions→Prepare retarget (`betweenSessionsPrepWindow`, main_tab_cubit.dart:153, 235-241) – correct as written; covered by existing passing tests (state 5/6 boundary cases).
- The 5→1 fallback ("no next session known" wins even when `hasDebrief` is true) – main_tab_cubit.dart:223-225 already does exactly what the spec asks; covered by an existing passing test (`next_session_action_test.dart`, "state 5->1: one-off session, after-therapy done, no next session known -> noNextSessionKnown").
- Backend `next_session_date` self-heal to `None` for a past-only custom session (crud.py:1527-1608) – already fixed in MSV3.11 CS-10, verified still in place.
- Refresh wiring from both the module button and the FAB – both call `refreshDebrief()`/`refreshPrepCard()` through multiple redundant paths (§2). Not the defect.
- DST-safe date math (`_localize_naive`, therapy_schedule_utils.py:61-83) – already fixed, unrelated to this bug, should not regress.

### 3.3 Secondary, out of scope for this fix (flag only)

- `prepCardMatchesNextSession` (main_tab_cubit.dart:77-95) uses a structurally similar but *forward-looking* same-day-or-48h-before window for matching a prep card to an upcoming session. It carries the same theoretical class of risk (a prep card created very early, more than 48h before a far-out session, on a different calendar day, could fail to register) but this is not what Darek reported, is not implicated by the "After Therapy" symptom, and the spec explicitly excludes "the After Therapy and Between Sessions capture flows themselves" and asks for a minimal fix. Not included in the work orders below; worth a future look if a symmetric bug report ever surfaces for "Prepare".
- The backend's `get_session_cycle_state` endpoint is fully-built, tested, dead code from the client's perspective. Wiring the client to consume it instead of maintaining a parallel local implementation would be a legitimate long-term simplification, but it is a redesign, not a minimal fix, and the spec explicitly forbids redesigning the state chain. Not recommended for this batch.

### 3.4 Observation, not a defect blocking CS-01

The backend's own `scheduled` fallback state (therapy_tracking.py:346-347, reached once the 30h recency window lapses with no matching debrief and prep is done) has no equivalent named state in the spec's 7-state chain and no client consumer to notice. Harmless today given the endpoint is unused; flag for whoever eventually wires the client to this endpoint.

## 4. Fix work orders

```
TASK: Remove the 48-hour/same-day ceiling from the After-Therapy debrief-match check so a late submission unsticks the "Your Session" card
AGENT: flutter-mobile
FILES: lib/screens/main_tab/cubit/main_tab_cubit.dart (debriefMatchesSession, ~line 124-144), test/screens/main_tab/cubit/next_session_action_test.dart (debriefMatchesSession group, ~line 95-157)
DEPENDS_ON: msv3.13 CS-02 (flutter-mobile, custom_interval_days removal) landing first, per the spec's "Blocked by" note – confirm _computeNextSession/_computeLastSession's custom-interval fallback branches (main_tab_cubit.dart:739-741, 880-882) are already gone before starting, so this fix is validated against the final schedule model.
DONE_WHEN:
  - debriefMatchesSession(debrief, sessionDateTime) returns true whenever debrief.sessionDate (compared in local time) is at or after sessionDateTime, with no upper time bound, and still returns false when the debrief's sessionDate is strictly before sessionDateTime (a stale earlier debrief must never satisfy a later occurrence).
  - The existing test 'created more than 48h after the session does not match' is changed to assert isTrue (or replaced/renamed to reflect the new rule), and a new case covers a debrief several days late (e.g. 6 days, mirroring Darek's report) still asserting isTrue. The 'created before the session does not match' case is kept and still asserts isFalse. The same-day and 'session starting right now' edge cases already covered stay green unmodified.
  - Darek's exact repro passes in a widget/cubit test: a past custom one-off session with no future date, After Therapy submitted 1h / 30h / 6 days / 30 days later, in every case computeNextSessionAction flips off sessionHappened/debriefCta to either betweenSessions (future session known) or noNextSessionKnown (none known) on the very next recomputation.
  - flutter analyze clean; full next_session_action_test.dart group green; manually verified on Android + iOS per the device-QA steps in section 6 below.
  - No other CS-09 state, button label, countdown format, or the capture flows themselves (debrief_capture_cubit.dart, TherapyFlowLauncher) are touched.
CONTEXT: Root cause is documented in section 3.1 above. SessionDebrief.session_date is stamped DateTime.now() at submission (debrief_capture_cubit.dart:917) rather than tied to the actual missed session's date – there is no session-identifying key passed through TherapyFlowLauncher.launch, and the spec forbids changing the capture flow's entry points beyond what's needed, so the fix belongs in the matching predicate, not in threading a session id through the flow. lastSessionDateTime's own lookup is already unbounded (main_tab_cubit.dart:872-961) so no change is needed there. Do not touch prepCardMatchesNextSession (main_tab_cubit.dart:77-95) – different, forward-looking match, out of this item's scope per section 3.3.
```

```
TASK: Apply the identical debrief-match fix to the backend's parallel (currently client-unused) CS-09 session-state endpoint, for consistency
AGENT: backend-api
FILES: app/api/v1/endpoints/therapy_tracking.py (_debrief_matches_session, ~line 173-200), app/tests/test_therapy_tracking_fix1_a12.py (TestDebriefLenientMatching class, ~line 405-461)
DEPENDS_ON: none functionally (this endpoint is not on the path the Main card uses today – see section 2b). Coordinate merge order only with msv3.13 CS-02 backend (custom_interval_days removal) since both touch the therapy-schedule file family; no logical dependency between the two changes.
DONE_WHEN:
  - _debrief_matches_session(debrief, session_local, user_tz) returns True whenever the debrief's session_date, converted to the user's local timezone, is at or after session_local, with no 48-hour ceiling, and False when it is strictly before session_local.
  - test_debrief_beyond_48h_and_different_day_does_not_match is updated to assert debrief_done is True (rename to reflect the corrected behavior) and a new case covers a debrief several days/weeks late still resolving away from debrief_cta.
  - The rest of TestDebriefLenientMatching and the full test_therapy_tracking_fix1_a12.py file still pass.
  - GET/PUT /users/therapy-schedule and get_therapy_schedule_with_frequency's next_session_date self-heal are confirmed unchanged and still correct (already verified in section 2b – no code change needed there).
  - Grep confirms has_debrief_for_session (the separate, older +/-12h-window function used by post_session_reflection_generator.py and notification_service.py) is untouched – this fix only changes _debrief_matches_session / _session_has_matching_debrief, which are exclusively local to therapy_tracking.py.
CONTEXT: This endpoint is dead code as far as Main's card is concerned (grep across mindsync-frontend/ for "session-state" / "SessionCycleStateResponse" returns nothing) so this task is not required to satisfy CS-01's device-observable done_when criteria on its own. It exists to prevent the backend from carrying an already-diagnosed bug forward as "tested, correct behavior" (see test_debrief_beyond_48h_and_different_day_does_not_match, which currently asserts the bug as intended) in case a future change wires the client to this endpoint instead of the local implementation.
```

## 5. Unit-level test matrix

| # | Scenario | FE (next_session_action_test.dart) | BE (test_therapy_tracking_fix1_a12.py) |
|---|---|---|---|
| 1 | After Therapy done, next session known, > 72h away | existing, passing – regression only | existing, passing – regression only |
| 2 | After Therapy done, next session known, < 72h away (skip Between Sessions) | existing, passing – regression only | existing, passing – regression only |
| 3 | After Therapy done, no next session known at all | existing, passing – regression only | n/a (endpoint has no equivalent consumer, but keep the state's own test green) |
| 4 | Debrief submitted 0h / 1h / 30h / 47h / 49h / 3 days / 6 days / 30 days after the session | new cases at 49h/3d/6d/30d must now assert match=true; 0h/1h/30h/47h already pass | same set, mirrored in TestDebriefLenientMatching |
| 5 | Debrief submitted 1h before the session (negative offset) | keep asserting false – guards a stale earlier debrief from wrongly satisfying a later occurrence | keep asserting false, same guard |
| 6 | Session starting exactly at "now" | existing, passing – regression only | n/a, not endpoint-specific |
| 7 | Day boundary: session 23:50, debrief 6 days later crossing several midnights | extend the existing day-boundary test past 48h | extend similarly if a day-boundary case is added |
| 8 | DST spring-forward / fall-back occurrence math | existing coverage – regression check only, unrelated to this fix | existing coverage – regression check only |
| 9 | All three frequency modes (weekly, biweekly, custom-manual-dates) across a session boundary, After Therapy submitted late in each | one parametrized case per mode – the matching function is frequency-agnostic, so this is primarily a regression guard that no mode-specific branch reintroduces a window | same, one case per mode against get_session_cycle_state |
| 10 | Debrief submitted via the FAB vs via the module | confirm MainTabCubit state updates after both entry points (already redundantly wired – see section 2 – this is a regression check, not a new fix) | n/a (backend has no entry-point distinction) |

## 6. Device tester steps

1. On an account with a custom one-off therapy session dated in the past (with a therapist name), confirm Main shows "Session has ended" with that date/time and therapist name, button "After Therapy" – this reproduces Darek's starting screenshot.
2. Before the fix ships: wait (or advance) more than 48 hours past that session's time, tap "After Therapy" from the module, complete the flow. Confirm the card is still stuck on "Session has ended" – this reproduces the bug and should be the last time it's reproducible.
3. After the fix ships, repeat step 2's submission (fresh past session, more than 48 hours late, from the module) and confirm the card flips within about a minute (the periodic session-clock tick) to "Between Sessions" if a future session is on the calendar, or to the set-therapy prompt if none is – without switching tabs, backgrounding, or reopening the app.
4. Repeat once submitting "After Therapy" from the FAB instead of the module, on a separate past session.
5. Repeat for weekly and for biweekly frequency: let a scheduled occurrence pass, wait more than 48 hours, submit After Therapy late, confirm the same flip.
6. Confirm "Between Sessions" holds until exactly 3 days before the next known session, then flips to "Prepare" with the countdown showing the next session's own date and time (not the previous session's hour).
7. Repeat once with the app force-quit and reopened between submission and the check, and once with the app merely backgrounded and resumed, to confirm both the app-resume hook and the 1-minute timer pick up the change.
8. Verify all of the above on both Android and iOS, per the spec's done-when requirement.
