---
name: e2e_local
description: Run MindSync's local end-to-end correctness checks — a manually-invoked, extensible suite that verifies a change has not broken critical user flows. Each "aspect" is one self-contained check; new aspects are added over time. Use when the user types "/e2e_local", "e2e local", "run e2e checks", "run the local e2e suite", or asks to verify a change has not broken account deletion (the first aspect). This skill is invoked manually by the user — never run it proactively.
---

# e2e_local — Local End-to-End Correctness Suite

A manually-invoked, **extensible** set of checks that confirm a change has not
silently broken a critical MindSync flow. Run it after implementing or reviewing
a change, before handing work off, or before a deploy.

The suite is organized into **aspects**. Each aspect is an independent check with
a clear PASS/FAIL. The user grows this list over time — when asked to "add a
check to e2e_local", append a new `## Aspect N` section below and (where useful)
a script under `scripts/`.

## How to run

Run **every** aspect below unless the user names a specific one, then print a
single consolidated report:

```
e2e_local results
─────────────────
[PASS] Aspect 1 — Account Deletion Integrity
...
Overall: PASS  (N/N aspects passed)
```

Commands are run from the backend dir (`MindSync/`) unless noted. On Windows use
PowerShell; the equivalent POSIX command is shown where it differs. If any
aspect FAILS, surface the exact failing output and the responsible file/owner —
do **not** summarize it away.

---

## Aspect 1 — Account Deletion Integrity

**What it protects:** `DELETE /api/v1/users/settings/account`
(`app/api/v1/endpoints/users.py::delete_own_account`). The endpoint erases a user
with a single `db.delete(user); db.commit()` and relies entirely on the database
`ON DELETE CASCADE` to remove every child row. If any User child is misconfigured,
that one statement raises `IntegrityError` → HTTP 500, and the Flutter client
(`SettingsCubit.deleteAccount` → generic `catch`) shows "An unexpected error
occurred" — i.e. **account deletion silently fails**. Because this is GDPR Art. 17
(right to erasure), a regression here is both a UX bug and a compliance bug.

Two invariants must always hold (a single broken model column or relationship
breaks them):

1. **DB cascade** — every `*.user_id → users.id` foreign key declares
   `ondelete='CASCADE'` (or, intentionally, `'SET NULL'` for audit/retention
   tables like `token_usage_log`).
2. **No ORM nullify** — every User-side one-to-many relationship is delete-safe:
   it carries `passive_deletes=True`/`'all'` **or** a delete cascade. Otherwise
   SQLAlchemy emits `UPDATE child SET user_id = NULL` before the DB can cascade,
   violating the NOT NULL column. (Footgun: a plain `backref="x"` **string**
   does NOT receive the `relationship()`-level `passive_deletes`; the flags must
   go *inside* `backref(...)`. This is exactly the `hero_insights` bug this
   aspect was created to catch.)

### Check 1a — static cascade-safety audit (fast, no DB)

Run the audit script. It inspects the live SQLAlchemy metadata and fails if any
`user_id` FK lacks an ON DELETE action or any User one-to-many can nullify:

```powershell
# from repo root
python .claude/skills/e2e_local/scripts/check_account_deletion.py
```

Exit 0 = PASS. Exit 1 = a code change would break account deletion (the script
prints the offending table/column or relationship and the fix). Exit 2 = harness
error (could not import models — fix that first).

### Check 1b — dynamic regression tests (real ORM delete)

Run the delete-account test suites. `test_delete_account_cascade.py` deletes a
**populated** user through the production ORM path (`db.delete(user)`) against an
in-memory SQLite DB with FK enforcement, so a real nullify/cascade gap surfaces
as a failure (e.g. `TestDeleteAccountOrmPathBackrefTables`):

```powershell
# from MindSync/
python -m pytest app/tests/test_delete_account.py app/tests/test_delete_account_cascade.py -q
```

PASS = all green.

### Check 1c — manual review of the diff (when reviewing a change)

If a diff is in scope, confirm none of these were broken:

- **New model with a `user_id` FK** → must declare `ForeignKey("users.id",
  ondelete="CASCADE")` (or `SET NULL` for audit tables) **and** its DB migration
  must include the same `ondelete` (Heroku migrations are manual — `deploy ≠
  migrate`; a fresh-vs-prod FK drift will not show locally). If it adds a
  User-side collection, wire it with `passive_deletes=True` + a delete cascade —
  via `back_populates` on an explicit `User` relationship, or via
  `backref("name", cascade="all, delete-orphan", passive_deletes=True)` (never a
  bare `backref="name"` string).
- **Endpoint** still does the single `db.delete(user); db.commit()`; all
  third-party cleanup (Redis/PostHog/Loops/AssemblyAI/Firebase) stays **after**
  the commit and stays exception-wrapped (the DB erasure is the legal contract).
- **Frontend** `UsersManager.deleteAccount()` still treats HTTP 404 as success
  (idempotent), and `SettingsCubit.deleteAccount()` still calls the backend
  **before** `firebaseUser.delete()` and reauthenticates before deleting.

**Aspect 1 PASS** ⇔ 1a exit 0 **and** 1b all green (1c has no findings when a diff
is in scope).

---

## Adding a new aspect

When the user says "add X to e2e_local":

1. Append a new `## Aspect N — <name>` section using the shape above: a short
   "what it protects", the concrete check command(s), and the PASS condition.
2. If the check is non-trivial, add a deterministic script under
   `scripts/` (self-locating like `check_account_deletion.py`, exit 0/1/2) and
   call it from the section.
3. Keep each aspect independent so the suite degrades gracefully — one failing
   aspect must not block the others from running or reporting.
