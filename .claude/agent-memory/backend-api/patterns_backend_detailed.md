---
name: patterns-backend-detailed
description: Long-form backend patterns and test gotchas moved out of MEMORY.md (check-and-set, chain-tip tests, psycopg2 date coercion, object_session on MagicMock, migration graph parsing)
metadata:
  type: reference
---

## Migration chain history (pre 2026-10)
- ww3x4y5z0a1b (Cadence v3 moment types) -> vv2w3x4y5z0a (upload_chunks) -> uu1v2w3x4y5z -> tt0u1v2w3x4y -> ...
- MSV3.2 batch: xx4y5z6a7b8c (workspace, 8 tables) -> yy5z6a7b8c9d (moment types enum) -> zz6a7b8c9d0e (agenda.kind)
- ... -> ff7182a3b4c5 (MSV3.2.2, 9 moment_type_enum labels) -> gg8h9i0j1k2l (users.activated_at) -> hh9i0j1k2l3m (B12) -> ii0j1k2l3m4n (B18) -> jj -> kk -> ll -> mm -> nn5o6p7q8r9s (platform_transaction_id) -> oo6p7q8r9s0t (granted_via) -> pp7q8r9s0t1u (corrective re-backfill, 2026-08-18) -> ... -> m318 -> m319 -> m320c4a5r6d7 -> ke_a7c3e9f1b2d4 (integration/redesign-v3).
- A programmatic down_revision-graph parser must handle tuple-form `down_revision = ('a','b')` from merge migrations like 5cafadce1513, or it falsely reports multiple heads. Prefer `py -3.12 -m alembic heads`.

## Atomic check-and-set "exactly once"
`db.query(Model).filter(Model.id==x, Model.flag_col.is_(None)).update({"flag_col": now}, synchronize_session="fetch")` then `db.commit()`; treat `rowcount==1` as "this call won", anything else as "already done/failed". Race-safe via DB row locking regardless of which Session/transaction issues it; the WHERE clause prevents double-fire, not transaction boundaries. See [[project_activation_user_activated_2026_08_10]].

## Migration chain-tip tests
Files like `test_workspace_fix4_migration.py` assert "X is currently the head" (`children == []`). Adding a migration on top of X makes that false (real regression signal). Update it to assert the new migration is X's one known successor, following the precedent in that file's docstring. Recurred 2026-08-10 (B12 broke gg8h9i0j1k2l's test, unnoticed). Targeted runs never catch this; run the full suite after landing a migration.

## object_session on MagicMock
`sqlalchemy.orm.object_session(x)` on a `MagicMock` does NOT raise: MagicMock auto-creates `_sa_instance_state`, so it returns a nested MagicMock. Use a real `declarative_base()` mini-model + in-memory SQLite for tests needing genuine behavior.

## psycopg2 date coercion (prod incident 2026-08-18)
`_coerce_datetime` in oo6p7q8r9s0t's backfill handled `datetime` and ISO `str` but not `datetime.date`; psycopg2 returns plain `date` for prod `user_subscription.start_date/end_date` (schema drift), and `date` is not a `datetime`, so every row coerced to None. SQLite round-trips return `str` and are structurally blind to this. Rule: extract row-processing into a pure function and unit-test it with real `date(2026, 1, 1)` objects. See [[project_granted_via_paywall_fix_2026_08_17]].

## Backward-compat lesson
Before changing an endpoint's response shape, grep the Flutter repo too (`lib/api/`, `lib/screens/**/cubit/`). Old shipped builds never show up in a backend-only grep.

## Extend the shared helper
When N endpoints funnel through one shared service function and a requirement applies "at every call site", put it in the shared function instead of editing N endpoint files.

## Workspace agenda pin helpers
`toggle_agenda_pin` (toggle, archives on repeat) vs `get_or_create_agenda_pin` (ADD-only, for legacy routes). Both derive pin state from `get_active_agenda_item_for_source`. See [[msv32-fix1-gfix-2026-07-17]].

## Full-suite baseline history
2026-09-02: 21-22 failures (custom-therapy-sessions x2, first-impression x1, notification-improvements x4, onboarding-v2 x1, symptom-suggestions x1, therapy-frequency x5, voice-fixes x5, walkthrough x1, therapy_tracking_fix1_a12 x1). 2026-10-05: 9 failures, suite split into 4 groups (>10 min). Drift from `test_temp.db` leftover/order noise (test_consent, test_workspace_fix1_a1_migration, test_timeline, test_notification_worker_registration). Log: [test_baseline_pytest_history.md](test_baseline_pytest_history.md).
