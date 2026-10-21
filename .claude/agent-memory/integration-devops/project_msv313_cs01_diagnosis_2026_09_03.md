---
name: project-msv313-cs01-diagnosis-2026-09-03
description: MSV3.13 CS-01 "Your Session card stuck after After Therapy" root cause and fix-plan location
metadata:
  type: project
---

Root cause found (2026-09-03, read-only diagnosis, BE main f4e27e8 / FE dev 73e5314): the
CS-09 state chain in `main_tab_cubit.dart` (`computeNextSessionAction`) is implemented
correctly. The actual defect is one layer upstream: `debriefMatchesSession`
(main_tab_cubit.dart:~132) only counts an After Therapy submission as "done" for the missed
session if it lands on the same calendar day as the session or within 48h after it. The
debrief's `sessionDate` is stamped `DateTime.now()` at submission time
(`debrief_capture_cubit.dart:917`, `_submitTextContent`), never the actual session's date
(`TherapyFlowLauncher` passes no session-identifying data into the capture flow at all).
Once a user debriefs more than 48h after the session (the realistic case for a therapy app),
the match fails permanently and the card is stuck on "Session has ended" forever, no matter
how many times "After Therapy" is completed. `lastSessionDateTime`'s own lookup is unbounded
(never expires), so nothing ever un-sticks it except a correct match.

An identical rule (`_debrief_matches_session`, `_DEBRIEF_MATCH_WINDOW_HOURS = 48.0`,
`app/api/v1/endpoints/therapy_tracking.py:170`) is duplicated on the backend's
`GET /therapy-tracking/session-state` endpoint, but that endpoint is dead code as far as the
Main card is concerned: confirmed via repo-wide grep, the Flutter client never calls it.

Both codebases' existing tests assert the 48h ceiling as *intended* behavior
(`next_session_action_test.dart:114` "created more than 48h after the session does not
match"; `test_therapy_tracking_fix1_a12.py::test_debrief_beyond_48h_and_different_day_does_not_match`)
- which is why this survived two earlier "fix" rounds (MSV3.2 Fix 2 CS-09, MSV3.2 Fix 3)
without being caught: the bug was certified as correct by the test suite itself.

**Why this matters beyond this one ticket:** this is the second time in this project a
same-day-or-N-hour matching heuristic between an independently-timestamped record and a
scheduled event has turned into a silent permanent-stuck-state bug (see also
`prepCardMatchesNextSession` in the same file, main_tab_cubit.dart:77-95, which has the
*same* structural risk on the forward-looking "match a prep card to an upcoming session"
side - flagged but explicitly out of scope for CS-01, not yet a reported bug). Any future
"X must have happened for/about session Y" check in this codebase should key off an actual
session identifier (id or exact scheduled datetime), not a recency window against a
submission timestamp, if the real event can plausibly happen later than the window allows.

Full report with state-machine tables, ranked root causes, CLAUDE.md-format fix work orders
for backend-api and flutter-mobile, a unit test matrix, and device-QA repro/verification
steps: `Business_requirements/MS_3/v3.13/CS01_DIAGNOSIS.md`.

Sequencing note from the spec: CS-01 is soft-blocked by CS-02 (`custom_interval_days`
removal, in progress in parallel on `wt-msv313-be`/`wt-msv313-fe`) - land CS-02 first so the
debrief-match fix is validated against the final (interval-free) custom-schedule model.

See also [[reference_backend_autodeploy_on_push]] for deploy sequencing once fixes land, and
the MSV3.11 CS-10 history (`Business_requirements/MS_3/v3.11/STATUS.md`) for why the tile's
GET-based refresh plumbing (timer, resume hook, post-submit refresh) was already fixed and is
*not* part of this defect - all of it was independently re-verified as correct during this
diagnosis.
