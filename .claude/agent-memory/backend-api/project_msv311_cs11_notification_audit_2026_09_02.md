---
name: project-msv311-cs11-notification-audit-2026-09-02
description: MSV3.11 CS-11 notification-logic audit + fixes -- custom-interval-only schedule bug found in 7 call sites, CooldownGiveUpThrottle added to 2 weekly generators, homework self-heal bypass fixed
metadata:
  type: project
---

## What happened
CS-11 (run after CS-10 per spec order) required a full audit of all 16
notification types + fixing daily/weekly cycle defects the audit found.
Branch `msv3.11-cs11` (worktree `wt-be-cs11`), base commit `5f7211b`
(CS-10), final commit `f97d0f9`. Audit report at
`Business_requirements/MS_3/v3.11/CS11_NOTIFICATION_AUDIT.md` (outside the
git repo, same convention as the MSV3.2.2 CS-01 audit).

## The big finding: custom-interval-only schedule invisibility (7 call sites)
CS-18 (an earlier fix) added a guard of the shape
`if not schedule and not custom_sessions: return None` to stop bailing
when a user relies purely on calendar-picked `custom_therapy_sessions`.
But `frequency=="custom"` actually has a THIRD valid shape this guard
never considered: interval-only (`custom_interval_days` + `next_session_date`
anchor, no recurring entries, no calendar picks) -- which legitimately has
BOTH `schedule` and `custom_sessions` empty. `compute_next_session_date`/
`compute_last_session_datetime` (`app/utils/therapy_schedule_utils.py`)
already branch on `frequency=="custom"` FIRST and resolve this case fine --
the bug was purely in 7 *local* copy-pasted guards sitting in front of
those shared functions, never reached them. Grep signature to find this
class of bug again: `if not schedule and not custom_sessions`.

Fixed (removed the guard entirely -- the compute functions already return
None safely for genuinely-empty schedules of any frequency, verified by
reading their source before deleting each guard):
- `app/api/v1/endpoints/therapy_tracking.py` `/session-state` (extended,
  not deleted -- the guard also decides the `no_therapy_set` response, so
  it became `if not schedule and not custom_sessions and not
  (frequency=="custom" and custom_interval_days is not None)`)
- `therapy_appointment_generator.py`, `therapy_prep_generator.py`,
  `record_session_generator.py`, `post_session_reflection_generator.py`,
  `homework_reminder_generator.py`, `between_sessions_note_generator.py`

**NOT fixed (out of FILES scope, same bug pattern, flagged for follow-up):**
`app/tasks/prep_card_auto_generate.py:134` (SessionPrepCard auto-gen, not
a notification generator, not one of the two named CS-10 leftovers).

## CooldownGiveUpThrottle rollout to REFLECTION_INVITATION + THERAPY_RELATIONSHIP_CHECKIN
Fresh DBA prod pull (`db-reports/2026-09-02-msv311-prod-evidence.md` §E)
confirmed the exact "iterate every user, ~99.97% expire unsent" shape
CooldownGiveUpThrottle (`notification_orchestrator.py`, landed 2026-08-16
for ADD_THERAPY_DATE, commit `de8d538`) was written to fix. Adopted the
mixin on both weekly generators -- `give_up_after_unengaged=3` is the real
fix (stops after 3 consecutive un-opened/un-acted Sundays); `cooldown_days=7`
is mostly redundant documentation since the Sunday-only eligibility check
+ ISO-week dedup already cap this at once/week.

**Deliberately did NOT adopt `has_no_push_target`** on these two (unlike
ADD_THERAPY_DATE) -- it gates on `activated_at is None AND no FCM token`,
and the existing test fixtures for both generators (real-SQLite-session
style in `test_msv32_notification_generators.py` and MagicMock-style in
`test_reflection_invitation_generator.py`) don't set `activated_at`, so
adding it would have broken ~20 existing eligibility tests for a guard the
spec didn't explicitly ask for. Judgment call: give-up mechanism targets
the exact evidenced shape; reach-reduction via has_no_push_target is a
separate, bigger decision out of scope for "fix the cycle."

**Test gotcha discovered**: `test_reflection_invitation_generator.py`
used `db = MagicMock()` for ALL its tests (unlike the sibling
THERAPY_RELATIONSHIP_CHECKIN test file, which already used a real
in-memory SQLite session). Adding `is_throttled()` (queries
`NotificationMoment` via `db.query(...)`) broke every existing test in
that file, because MagicMock's query chain returns non-comparable
MagicMock objects and `is_throttled` fails closed on the exception
(logged as `[THROTTLE] is_throttled query failed... '<' not supported
between instances of 'MagicMock' and 'datetime.timedelta'`), i.e. eligible
became False everywhere silently. Fixed by adding `is_throttled=False` to
the existing `patch.multiple(...)` helpers (`_mock_no_reflect_this_week`)
rather than converting the whole file to real-SQLite. New throttle-specific
tests use a NEW class with a real SQLite session in the same file (mixed
convention within one file is fine, matches the mixed pattern already used
elsewhere in this codebase).

## HOMEWORK_REMINDER self-heal bypass (CS-08 sanity check)
`_has_open_homework` queried `TodoItem.status == "open"` directly,
bypassing `ws_crud.sweep_repeating_todos` -- since homework items
(origin=therapist) can carry `repeat_freq` like any Workspace to-do
(CS-05/06/07, same MSV3.11 round), a repeating homework item past its
period but not yet opened in-app still looked DONE. Fixed by calling
`ws_crud.sweep_repeating_todos(db, user_id)` first, matching every other
read path. **Important scope note**: my branch (`msv3.11-cs11`, based on
`msv3.11-cs10`) does NOT include the `msv3.11-cs07` branch's rewrite of
`sweep_repeating_todos`/`_maybe_reopen_repeating_todo` (calendar-boundary
reset) -- that CS-07 work is on a SEPARATE, not-yet-merged branch. My fix
calls the CURRENT (pre-CS-07, fixed-offset `_REPEAT_INTERVAL_DAYS`)
implementation, which has the same 2-arg `sweep_repeating_todos(db,
user_id)` signature the eventual CS-07 rewrite keeps -- confirmed
forward-compatible by reading the CS-07 diff (`git diff main..msv3.11-cs07
-- app/`) as reference material only, not as code actually present in my
tree. **Gotcha for whoever merges CS-07 later**: don't assume a sibling
branch's diff you read for context is already in your own tree -- verify
with a direct grep of the actual file before writing code that depends on
it.

## HOMEWORK_REMINDER route (CS-08) -- no change needed
Verified read-only against `mindsync-frontend`:
`moment_deep_link_screen.dart` dispatches every MSV3.2.2 deterministic
type (including homeworkReminder) through the generic renderer, which
navigates via `moment.deepLinkRoute` -- the backend-supplied string,
verbatim. `ms_routes.dart` (~line 145) confirms `section=todo` is already
a recognized Workspace `scrollTo` anchor. Backend's
`route_for(HOMEWORK_REMINDER)` was already
`/main-page/tab/workspace?section=todo` (unchanged since MSV3.2.2) -- CS-08
did not require any backend route change, only the sanity check on trigger
conditions above.

## Dead code confirmed (CS-10 leftover b, resolved by clarification not fix)
`_process_first_nudges`/`_process_followup_nudges` in
`notification_service.py`: zero callers anywhere in `app/` (grep-verified),
and `settings.notification_legacy_jobs_enabled` -- which the CS-10 handoff
described these as "gated by, default False" -- **does not exist on
Settings at all** (fully removed 2026-07-03 per Notification Cadence v3,
confirmed via `test_legacy_cutover.py`'s own assertion). This sharpens the
original handoff: not merely defaulted off, genuinely unreachable dead code
in every deployed process. Left untouched (established project convention:
"delete only if trivially safe... removal is a separate cleanup").

## Process notes
- Full `app/tests/` run took 634.79s (10:34) on this box -- much slower
  than the earlier CS-10 run reported (that was likely a smaller/warmer
  run). If timing this again, budget ~11 minutes, not the ~7 minutes a
  partial/touched-files run suggests.
- **Background-task pitfall confirmed**: a `run_in_background`-promoted
  Bash task (auto-promoted after exceeding the per-call timeout, not an
  explicit `run_in_background: true` call) got silently `[killed]` after a
  long wait with no output -- lost an entire ~10-minute pytest run. The
  fix: always start a long test run with EXPLICIT `run_in_background:
  true` from the first call (not relying on auto-promotion), and prefer
  writing output straight to a file (`> log 2>&1`) over piping through
  `tail` (which buffers until the pipe's writer closes, so `tail`-fed logs
  show ZERO lines until the whole command finishes -- not useful for
  progress checks). A `Monitor` tool call with a polling shell loop
  (`until grep -qE "passed|failed|error" logfile; do sleep 30; done`) is
  the right tool for "notify me when this long test run finishes" --
  cheaper than repeated manual `Bash`/`Read` polling and doesn't compete
  with the running suite for shell/process resources the way a burst of
  ad-hoc polling commands does.
- See also [[test_baseline_pytest_history]] -- the 21-failure baseline
  held exactly, item-for-item, on this integrated branch
  (cs07+cs10+cs01+cs02 base per the coordinator's message) after this
  task's changes.

## Commit
Branch `msv3.11-cs11` (worktree `wt-be-cs11`), commit `f97d0f9`, NOT
pushed. No migration (no schema changes, no new moment types).
