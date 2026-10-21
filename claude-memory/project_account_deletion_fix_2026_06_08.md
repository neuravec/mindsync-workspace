---
name: project_account_deletion_fix_2026_06_08
description: Account deletion 500-ed for active users — User.hero_insights backref nullify bug; fixed + new e2e_local skill guards it
metadata: 
  node_type: memory
  type: project
  originSessionId: f81eaf6b-0865-48d5-8df2-2e83502147e0
---

Account deletion (`DELETE /api/v1/users/settings/account`) failed in the app for
essentially every active user. Root cause was a SQLAlchemy footgun in
`app/models/hero_insight.py`: the relationship used a plain string
`backref="hero_insights"` with `passive_deletes=True` passed as a `relationship()`
kwarg. That kwarg applies to `HeroInsight.user` (many-to-one), NOT to the
auto-created `User.hero_insights` collection, which kept unsafe defaults
(passive_deletes=False, no delete cascade). So `db.delete(user); db.commit()`
(the endpoint's single cascade-delete) emitted `UPDATE hero_insights SET
user_id = NULL` → NOT NULL violation → `IntegrityError` → HTTP 500 → Flutter
showed "An unexpected error occurred". The hourly hero_insight job populates one
row per active user, so most users hit it.

**Fix:** pass the flags *inside* `backref(...)`:
`backref("hero_insights", cascade="all, delete-orphan", passive_deletes=True)`.
hero_insights.user_id already had DB `ON DELETE CASCADE` (model + migration
`ll2m3n4o5p6q`), so the DB cascade does the work — NO migration needed, code-only.

Key learning: the 3 backref children in models.py (periodic_summaries,
subscription_receipts, rag_documents) were ALREADY correct because they pass
passive_deletes *inside* `backref(...)`. Verified the real endpoint path with an
echo-SQL diag: with passive_deletes wired correctly, `db.delete(user)` emits only
`DELETE FROM users` (no nullify). The stale "ORM cascade gap" comments in
`test_delete_account_cascade.py` predate the passive_deletes additions and are
misleading — don't trust them, verify with the audit below.

**Also did:** added `cascade="all, delete-orphan"` to those 3 backrefs for
consistency (harmless, they were safe); added ORM-path regression tests
(`TestDeleteAccountOrmPathBackrefTables`, incl. the hero_insights reproducer that
goes RED without the fix) to `app/tests/test_delete_account_cascade.py`.

**New skill `e2e_local`** (`.claude/skills/e2e_local/`, manually invoked, extensible
— user adds aspects over time). Aspect 1 = Account Deletion Integrity:
- `scripts/check_account_deletion.py` — static cascade-safety audit over live
  SQLAlchemy metadata: every `user_id→users.id` FK must have ondelete CASCADE/SET
  NULL, and every User one-to-many must have passive_deletes/delete-cascade.
  Exit 0/1/2. THIS is what caught hero_insights. Self-locating; bootstraps env via
  `app/tests/conftest.py`. Run from repo root.
- runs the delete-account pytest suites + a diff review checklist.

**Status:** IMPLEMENTED on disk + verified (delete suite 30 passed, hero_insight
48 passed, audit exit 0, mappers configure). NOT committed (repo not git per
harness), NOT deployed. See [[feedback_memory_write_after_commit]].

Env note: Grep/Glob tools were broken this session (uv_spawn/ripgrep missing);
used PowerShell Select-String. Backend tests run from `MindSync/` with system
python 3.14 + pytest 9 (`python -m pytest app/tests/...`).
