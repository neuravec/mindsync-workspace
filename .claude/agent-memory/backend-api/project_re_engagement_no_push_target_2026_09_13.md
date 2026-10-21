---
name: project-re-engagement-no-push-target-2026-09-13
description: ReEngagementGenerator now skips users with no FCM token AND never-activated, reusing CooldownGiveUpThrottle.has_no_push_target(); documents the in-app-card critical-question resolution and a fixture-collision gotcha with a sibling integration test file.
metadata:
  type: project
---

Task (2026-09-13, follow-up to [[project_notification_ai_premium_gate_2026_09_13]] and the
data-analytics 38%-no-token prod finding): `app/services/moments/re_engagement_generator.py`
now mixes in `CooldownGiveUpThrottle` (app/services/notification_orchestrator.py) SOLELY for
`has_no_push_target()` — NOT `is_throttled()`, since RE_ENGAGEMENT already has its own
3-day/7-day/stop cadence via `_count_re_engagement_moments_since` that must stay untouched.
Checked as Gate 2 in `is_eligible()` (right after the cheap in-memory toggle check, before the
last-activity/moment-count queries) and again as the first check in `generate()` (race guard,
before any context-building or AI-call work).

**Critical question resolved with code evidence, not guessed**: does a no-FCM-token user who
opens the app see the in-app moment card? YES — `GET /moments/upcoming`
(`app/api/v1/endpoints/moments.py` -> `get_pending_or_sent_moment_for_user` in
`app/crud/notification_moment.py`) is explicitly documented (CS-20, MSV3.3) as the in-app
fallback for exactly the "SENT but push_delivered=False" case a missing token produces — it is
called on every app open regardless of push state. This is WHY `has_no_push_target()` is not a
blanket "no token -> skip": it only fires when the user has BOTH no token AND
`User.activated_at IS NULL` (never fired a single qualifying therapy-loop event — see
`models.User.activated_at`), i.e. no token and no credible sign they'll ever open the app to see
a card either. A user who was previously active (the actual RE_ENGAGEMENT target population)
almost always has `activated_at` set from before they went quiet, so their in-app card survives
even with zero current tokens.

**Fixture-collision gotcha (found the hard way, cost one fix-forward round)**: adding this gate
broke 6/6 tests in the sibling, already-uncommitted
`app/tests/test_notification_ai_gate_re_engagement_integration.py` (change A+B interaction
tests from a parallel task) because its `_insert_user()` helper creates a real `models.User`
with `activated_at=None` and never registers an FCM token — exactly the population my new gate
skips. Existing tests in `test_re_engagement_generator.py` itself were UNAFFECTED because their
`_make_user()` returns a bare `MagicMock()`, and `getattr(mock, "activated_at", None) is not
None` is `True` for an unconfigured MagicMock attribute (auto-created child mock, never `None`)
— so MagicMock-based fixtures silently "pass" this gate by accident, while real-SQLAlchemy-model
fixtures do not. **Rule for next time**: whenever adding an `activated_at`/token-style gate,
grep test files for BOTH `MagicMock()` user fixtures (safe by accident) AND real
`models.User(...)` insert helpers used by OTHER, unrelated test files that exercise the same
generator (NOT safe — will need `activated_at` set explicitly). Fixed here by adding
`activated_at=_NOW - timedelta(days=365)` to that file's shared `_insert_user()` helper only
(one line, one place, zero assertions touched) — mirrors the exact precedent already established
in `test_msv322_new_generators.py::TestAddTherapyDateGenerator.setup_method` when
`has_no_push_target()` was first introduced for `AddTherapyDateGenerator`.

Full suite after the fix: 5807 passed, 14 failed — identical to the documented baseline (see
MEMORY.md "Test Patterns" baseline note), zero new reds, +6 vs. the 5801 baseline (my 6 new
tests in `test_re_engagement_generator.py`).

Considered-but-declined widening: REFLECTION_INVITATION and THERAPY_RELATIONSHIP_CHECKIN
deliberately did NOT adopt `has_no_push_target()` (per their own module docstrings) to avoid
reducing reach beyond what their existing give-up-after-unengaged throttle already targets —
flagged as a possible future candidate but explicitly NOT implemented here without a separate
operator decision, per the task's own scope guard.
