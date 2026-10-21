#!/usr/bin/env python
"""e2e_local — Account Deletion Integrity (static cascade-safety audit).

WHY THIS EXISTS
---------------
Account deletion (DELETE /api/v1/users/settings/account) erases a user with a
SINGLE ``db.delete(user); db.commit()`` and relies entirely on the database's
FK ``ON DELETE CASCADE`` to remove every child row.  Two invariants must hold or
that one statement 500s — and the Flutter client surfaces it as a generic
"An unexpected error occurred", i.e. the account silently fails to delete:

  INVARIANT 1 (DB cascade): every ``*.user_id -> users.id`` foreign key declares
      ``ondelete='CASCADE'`` (or, intentionally, ``'SET NULL'`` for audit tables
      like ``token_usage_log``).  A bare FK (ondelete=None) makes Postgres reject
      the parent DELETE while child rows exist -> 500.

  INVARIANT 2 (no ORM nullify): every User-side one-to-many relationship is
      delete-safe — it has ``passive_deletes=True`` / ``'all'`` OR a delete
      cascade.  Otherwise SQLAlchemy emits ``UPDATE child SET user_id = NULL``
      before the DB can cascade, which violates the NOT NULL column -> 500.

This script statically verifies BOTH invariants against the live SQLAlchemy
model metadata, so any code change that adds a User child table without a
cascade, or wires a User relationship without passive_deletes, fails CI/this
check BEFORE it can break account deletion in production.

It does NOT touch a real database — it inspects ``Base.metadata`` and the User
mapper only.  Dynamic end-to-end coverage (actually deleting a populated user)
lives in ``app/tests/test_delete_account_cascade.py``, which the skill also runs.

USAGE
-----
    python .claude/skills/e2e_local/scripts/check_account_deletion.py

Exit code 0 = all invariants hold.  Exit code 1 = at least one violation that
would break account deletion (details printed).  Exit code 2 = harness/import
error (could not load the models).
"""

from __future__ import annotations

import pathlib
import sys

# --------------------------------------------------------------------------- #
# Locate the backend and reuse the test-suite env bootstrap so model imports
# (which read config at import time) succeed without real credentials.
# --------------------------------------------------------------------------- #
_HERE = pathlib.Path(__file__).resolve()
# scripts -> e2e_local -> skills -> .claude -> <repo root>
_REPO = _HERE.parents[4]
_BACKEND = _REPO / "MindSync"

if not _BACKEND.is_dir():
    print(f"[e2e_local] ERROR: backend dir not found at {_BACKEND}", file=sys.stderr)
    raise SystemExit(2)

sys.path.insert(0, str(_BACKEND))
sys.path.insert(0, str(_BACKEND / "app" / "tests"))

try:
    import conftest  # noqa: F401  — module-level side effects set env + SQLite shim
except Exception as exc:  # pragma: no cover - harness failure
    print(f"[e2e_local] ERROR: could not bootstrap test env: {exc}", file=sys.stderr)
    raise SystemExit(2)

try:
    # Importing the package runs app/models/__init__.py which registers the bulk
    # of the mappers. clinician_v2 is loaded on-demand by its endpoints, so pull
    # it in explicitly to audit those user_id FKs too.
    import app.models  # noqa: F401
    from app.models import clinician_v2  # noqa: F401
    from app.db.session import Base
    from app.models.models import User
    from sqlalchemy.orm import class_mapper
    from sqlalchemy.orm.interfaces import ONETOMANY, MANYTOMANY
except Exception as exc:  # pragma: no cover - harness failure
    print(f"[e2e_local] ERROR: could not import models: {exc}", file=sys.stderr)
    raise SystemExit(2)


_ACCEPTABLE_ONDELETE = {"CASCADE", "SET NULL", "SET DEFAULT"}


def audit_foreign_keys() -> tuple[list[str], list[str]]:
    """INVARIANT 1 — every FK to users.id has an ON DELETE action.

    Returns (violations, info_setnull).
    """
    violations: list[str] = []
    info_setnull: list[str] = []

    for table in Base.metadata.sorted_tables:
        for fk in table.foreign_keys:
            target = fk.target_fullname.lower()  # e.g. "users.id"
            if target != "users.id":
                continue
            ondelete = (fk.ondelete or "").upper()
            col = fk.parent.name
            if ondelete not in _ACCEPTABLE_ONDELETE:
                violations.append(
                    f"{table.name}.{col} -> users.id has ondelete={fk.ondelete!r} "
                    f"(must be CASCADE, or SET NULL for audit-only tables)"
                )
            elif ondelete in {"SET NULL", "SET DEFAULT"}:
                info_setnull.append(f"{table.name}.{col} -> users.id ({ondelete})")
    return violations, info_setnull


def audit_user_relationships() -> list[str]:
    """INVARIANT 2 — every User one-to-many is delete-safe (no SET NULL nullify)."""
    violations: list[str] = []
    mapper = class_mapper(User)

    for rel in mapper.relationships:
        # Only collections hanging off User can trigger the pre-delete nullify.
        if rel.direction not in (ONETOMANY, MANYTOMANY):
            continue

        passive = rel.passive_deletes  # True | False | 'all'
        cascade = rel.cascade
        delete_safe = (passive in (True, "all")) or bool(cascade.delete)

        if not delete_safe:
            target = rel.mapper.class_.__name__
            violations.append(
                f"User.{rel.key} -> {target}: one-to-many without passive_deletes "
                f"or delete cascade (cascade={set(cascade)}, passive_deletes={passive!r}). "
                f"SQLAlchemy will SET NULL the child user_id on account delete -> 500."
            )
    return violations


def main() -> int:
    print("=" * 72)
    print("e2e_local :: Account Deletion Integrity (static cascade-safety audit)")
    print("=" * 72)

    fk_violations, fk_setnull = audit_foreign_keys()
    rel_violations = audit_user_relationships()

    # Count audited surface for transparency.
    user_fk_tables = {
        t.name
        for t in Base.metadata.sorted_tables
        for fk in t.foreign_keys
        if fk.target_fullname.lower() == "users.id"
    }
    one_to_many = [
        r.key
        for r in class_mapper(User).relationships
        if r.direction in (ONETOMANY, MANYTOMANY)
    ]
    print(f"Audited {len(user_fk_tables)} tables with a user_id FK and "
          f"{len(one_to_many)} User one-to-many relationships.\n")

    if fk_setnull:
        print("Intentional SET NULL FKs (audit/retention tables — OK):")
        for line in sorted(fk_setnull):
            print(f"  - {line}")
        print()

    problems = fk_violations + rel_violations
    if not problems:
        print("PASS — every user_id FK cascades and no User relationship nullifies.")
        print("       A single db.delete(user) will erase the account cleanly.")
        return 0

    print("FAIL — these would break account deletion:\n")
    if fk_violations:
        print("  INVARIANT 1 (DB cascade) violations:")
        for v in fk_violations:
            print(f"    * {v}")
        print()
    if rel_violations:
        print("  INVARIANT 2 (ORM nullify) violations:")
        for v in rel_violations:
            print(f"    * {v}")
        print()
    print("Fix: add ondelete='CASCADE' to the FK (backend-api owns the migration), "
          "and/or passive_deletes=True + cascade='all, delete-orphan' on the User "
          "relationship. Then re-run this check and the delete-account test suite.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
