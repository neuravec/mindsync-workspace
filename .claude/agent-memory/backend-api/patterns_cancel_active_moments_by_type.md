---
name: patterns-cancel-active-moments-by-type
description: How to cancel/invalidate an already-generated NotificationMoment when its trigger condition is resolved by a later write, and a MagicMock truthiness gotcha hit while testing it
metadata:
  type: project
---

## The pattern
`NotificationMoment` (app/models/notification_moment.py) has no `CANCELLED`
status -- only PENDING/SENT/OPENED/DISMISSED/ACTED/EXPIRED, and adding a new
native-Postgres-enum value needs a migration. When a generator's trigger
condition can be resolved by a later write (e.g. ADD_THERAPY_DATE's "no known
session" condition, resolved by saving a session date -- see
[[project_msv310_cs02_add_therapy_date_investigation_2026_09_01]]), the
established fix shape is: reuse `EXPIRED` (it already means "will never be
delivered" and is already excluded from both `get_moments_due_for_delivery`
(PENDING-only) and `get_pending_or_sent_moment_for_user` (excludes EXPIRED)),
set `push_delivered=False` (matches `_expire_stale_moments_impl`'s convention
for "never genuinely delivered"), and add a `scoring_signals["cancelled_reason"]`
marker to distinguish from a genuine timeout-expiry for observability --
`scoring_signals` is a plain JSON column (not MutableDict), so REASSIGN the
dict (`moment.scoring_signals = {**existing, "key": val}`), don't mutate a
fetched dict in place, or SQLAlchemy won't detect the change on flush.

Scope the query to PENDING **or** (SENT with `push_delivered is False`) --
the two channels a not-yet-genuinely-delivered moment can still reach a user
through (push retry via `deliver_due_moments`, and the in-app fallback via
`get_pending_or_sent_moment_for_user`). A SENT moment with
`push_delivered=True` already reached the user; leave it alone.

Call the cancel function from the ONE write path that resolves the condition
(grep for every production writer of the relevant columns first to confirm
there's exactly one -- there was for `therapy_schedule`/`custom_therapy_sessions`,
both isolated to `crud.update_therapy_schedule`). Gate the call on the
resolved condition actually being "now satisfied" (e.g. `next_dt is not
None`) so the opposite case (clearing/removing the condition) is a strict
no-op and existing moments keep being governed by their normal
cooldown/eligibility rule, per whatever spec is driving the change.

## MagicMock gotcha hit while testing this
A query result (`db.query(...).filter(...).all()`) is a real Python `list` in
production, where `not rows` and `len(rows) == 0` are equivalent. Against a
**fully-mocked** `db = MagicMock()` fixture (a legitimate, already-established
pattern in this codebase, e.g. `test_therapy_frequency.py`'s
`_make_db_and_prefs`), `.all()` returns an auto-created `MagicMock`, whose
default `__bool__` is `True` even though its default `__len__` is `0` --
`bool(MagicMock())` is `True`, `len(MagicMock())` is `0`. A guard written as
`if not rows: return 0` does NOT short-circuit against that mock (since
`bool()` wins over `__len__` for truthiness), so the function falls through
to an extra, unintended `db.commit()` call -- broke an existing test asserting
`db.commit.assert_called_once()` on `crud.update_therapy_schedule`
(unrelated code path that happened to share the same generic `db` mock).
Fix: write the guard as `if len(rows) == 0:` explicitly -- correct for real
lists (no behavior change in production) AND correct against this mock shape
(since `len()` IS configured to 0 by default). **Prefer `len(x) == 0` over
`not x` for any query-result guard that might ever run against a
fully-mocked `db` in this codebase's test suite.**
