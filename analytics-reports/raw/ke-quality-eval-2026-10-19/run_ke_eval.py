"""Thin wrapper around scripts/ke_quality_eval.py (worktree v574, unmodified) for the 2026-10-19 gate run.

Why a wrapper: at v574 the eval script seeds a user and calls process_user()
directly, but the pipeline now has four gates the script never opens, so an
unmodified run returns an empty map for every story ("0 problems", a false pass):
  1. CHARACTER_KE_EXTRACTION_ENABLED / CHARACTER_KE_ENABLED default False (status "off");
  2. ke_user_state.activated_at is only set by sheet.record_open() (GET /sheet),
     never by the script (status "inactive");
  3. CHARACTER_KE_REQUIRE_PROFILING_OPT_IN (default True) needs an ACTIVE PROFILING
     consent record (status "consent");
  4. therapy content (after_therapy, session, homework to-dos) is read only with an
     active ARTICLE9_HEALTH consent.
The wrapper opens exactly these gates the way a consenting user who opened the tab
would, and adds richer output (all moments per entry, skills' in_your_words, ideas,
pending stage-ups, token split). Everything else is the script's own code.

Safety: DB_URL is still assigned by the script's _bootstrap_env() before any app
import (fresh SQLite in %TEMP%); the wrapper asserts the engine is SQLite before the
first story. PostHog and Redis stay off. Only the OpenAI model is called.

Usage (any cwd):
  python run_ke_eval.py --weeks 2 --story S01 S02 --json out.json [--no-art9] [--dry]
"""

from __future__ import annotations

import os
import sys
from datetime import timedelta
from pathlib import Path

WT = Path(r"C:/Users/mikol/Notebooks/MindSync/Heroku/MindSync-wt-integration-v3-final")
sys.path.insert(0, str(WT / "scripts"))

NO_ART9 = "--no-art9" in sys.argv
if NO_ART9:
    sys.argv.remove("--no-art9")

# Gate 1: KE on for everyone, extraction on (the 2026-10-19 rollout state).
os.environ["CHARACTER_KE_ENABLED"] = "true"
os.environ["CHARACTER_KE_EXTRACTION_ENABLED"] = "true"
os.environ.pop("CHARACTER_KE_USER_IDS", None)
# Prod default for the model: KE_LLM_MODEL empty -> GPT_MODEL_MINI.
os.environ["KE_LLM_MODEL"] = ""

import ke_quality_eval as E  # noqa: E402  (module import only; no app import yet)

_orig_bootstrap = E._bootstrap_env
_orig_run_story = E.run_story
_orig_summary = E._summary
_PREPARED: set[str] = set()
TOKENS: list[dict] = []
PRICE = {"prompt": 0.75, "cached": 0.075, "completion": 4.50}  # gpt-5.4-mini USD per 1M (model_pricing seed)


def _cost(rows: list[dict]) -> dict:
    p = sum(r["prompt"] for r in rows)
    k = sum(r["cached"] for r in rows)
    c = sum(r["completion"] for r in rows)
    usd = ((p - k) * PRICE["prompt"] + k * PRICE["cached"] + c * PRICE["completion"]) / 1e6
    return {"calls": len(rows), "prompt": p, "cached": k, "completion": c, "usd": round(usd, 5)}


def _install_gates() -> None:
    # token_usage_log.id is BigInteger: on SQLite that is not a rowid alias, so every usage
    # insert fails (NOT NULL id) and the script's own _usage() reads nothing. Compile it as
    # INTEGER for this temp DB only, so the run's tokens are recorded.
    from sqlalchemy import BigInteger
    from sqlalchemy.ext.compiler import compiles

    @compiles(BigInteger, "sqlite")
    def _bigint_sqlite(type_, compiler, **kw):  # noqa: ANN001
        return "INTEGER"

    # Exact token accounting: the real logger opens a second SQLite session while the job's
    # session holds the write lock, so ~30% of inserts fail with "database is locked" (and
    # each waits 5 s). Record every call in memory instead (same numbers the logger gets).
    import app.services.openai_service as OS
    from app.services import usage_tracking as UT

    def _record(api_type, model, prompt_tokens=None, completion_tokens=None, total_tokens=None,
                cached_tokens=0, is_estimate=False, feature_override=None, operation_override=None,
                user_id_override=None):
        ctx = UT._usage_context.get()
        TOKENS.append({
            "user_id": user_id_override or (ctx.user_id if ctx else None),
            "operation": operation_override or (ctx.operation if ctx else "unknown"),
            "api_type": api_type, "model": model, "prompt": int(prompt_tokens or 0),
            "completion": int(completion_tokens or 0), "cached": int(cached_tokens or 0),
        })

    OS.log_token_usage = _record

    import app.tasks.ke as T
    from app.db.session import engine
    from app.models.models import ConsentRecord
    from app.services.ke.sheet import record_open

    assert engine.url.get_backend_name() == "sqlite", f"refusing to run on {engine.url.get_backend_name()}"
    real = T.process_user

    def process_user(db, user_id, *, now=None, **kw):
        if user_id not in _PREPARED:
            types = ["PROFILING"] + ([] if NO_ART9 else ["ARTICLE9_HEALTH"])
            for ct in types:  # gates 3 and 4: consent granted before the first open
                db.add(ConsentRecord(user_id=user_id, consent_type=ct,
                                     granted_at=(now or E.NOW) - timedelta(days=1), source="ke_eval"))
            db.commit()
            record_open(db, user_id, now=now)  # gate 2: first open of the tab
            _PREPARED.add(user_id)
        return real(db, user_id, now=now, **kw)

    T.process_user = process_user


def _bootstrap_env():
    db = _orig_bootstrap()
    _install_gates()
    return db


def _summary(sheet: dict) -> dict:
    out = _orig_summary(sheet)
    out["pending_stages"] = [f'skill {p["skill_id"]} -> {p["stage"]}' for p in sheet.get("pending_stages", [])]
    out["idea_count"] = len(sheet.get("ideas", []))
    return out


def _dec(value):
    from app.services.encode_service import decode

    if not isinstance(value, str) or not value:
        return value
    try:
        return decode(value)
    except Exception:
        return value


def _usage_split(db, uid: str) -> dict:
    from sqlalchemy import func

    from app.models.models import TokenUsageLog

    rows = (
        db.query(TokenUsageLog.operation, TokenUsageLog.model, func.count(TokenUsageLog.id),
                 func.sum(TokenUsageLog.prompt_tokens), func.sum(TokenUsageLog.completion_tokens),
                 func.sum(TokenUsageLog.cached_tokens))
        .filter(TokenUsageLog.user_id == uid)
        .group_by(TokenUsageLog.operation, TokenUsageLog.model)
        .all()
    )
    return {f"{op}|{model}": {"calls": int(n), "prompt": int(p or 0), "completion": int(c or 0), "cached": int(k or 0)}
            for op, model, n, p, c, k in rows}


def run_story(story: dict, weeks: int) -> dict:
    result = _orig_run_story(story, weeks)
    from app.db.session import SessionLocal
    from app.models.ke import KeHard, KeIdea, KeMoment, KePath, KeSkill, KeTool, KeUserState

    uid = f"eval_{story['id']}"
    db = SessionLocal()
    try:
        moments = []
        for m in db.query(KeMoment).filter(KeMoment.user_id == uid).order_by(KeMoment.source_at, KeMoment.id):
            sa = m.source_at if m.source_at.tzinfo else m.source_at.replace(tzinfo=E.NOW.tzinfo)
            moments.append({
                "days_ago": round((E.NOW - sa).total_seconds() / 86400), "source_kind": m.source_kind,
                "family": m.emotion_family, "kind": m.kind, "anchor": m.anchor, "strengths": m.strengths,
                "confidence": m.confidence, "hard_situation": m.hard_situation, "text": _dec(m.text),
                "attached": {"path": m.path_id, "skill": m.skill_id, "tool": m.tool_id, "hard": m.hard_id},
            })
        result["moments"] = moments
        result["skills_full"] = [
            {"id": s.id, "path_id": s.path_id, "anchor": s.anchor, "icon": s.icon, "name": _dec(s.name),
             "in_your_words": _dec(s.in_your_words)}
            for s in db.query(KeSkill).filter(KeSkill.user_id == uid).order_by(KeSkill.id)
        ]
        result["paths_full"] = [
            {"id": p.id, "family": p.emotion_family, "name": _dec(p.name), "focus": _dec(p.focus),
             "merged_into": p.merged_into_id}
            for p in db.query(KePath).filter(KePath.user_id == uid).order_by(KePath.id)
        ]
        result["tools_full"] = [
            {"id": t.id, "name": _dec(t.name), "what": _dec(getattr(t, "what", None)), "origin": t.origin,
             "origin_note": _dec(getattr(t, "origin_note", None))}
            for t in db.query(KeTool).filter(KeTool.user_id == uid).order_by(KeTool.id)
        ]
        result["hard_full"] = [
            {"id": h.id, "label": _dec(h.label), "context": _dec(getattr(h, "context", None))}
            for h in db.query(KeHard).filter(KeHard.user_id == uid).order_by(KeHard.id)
        ]
        result["ideas_full"] = [
            {"id": i.id, "path_id": i.path_id, "skill_id": i.skill_id, "text": _dec(i.text), "why": _dec(i.why),
             "reason": i.reason, "cta": i.cta, "state": i.state, "created_at": str(i.created_at)}
            for i in db.query(KeIdea).filter(KeIdea.user_id == uid).order_by(KeIdea.id)
        ]
        st = db.query(KeUserState).filter(KeUserState.user_id == uid).first()
        result["state"] = {"latest_entry_crisis": getattr(st, "latest_entry_crisis", None),
                           "initial_sync_done": getattr(st, "initial_sync_done", None),
                           "source_counts": getattr(st, "source_counts", None)} if st else None
        mine = [r for r in TOKENS if r["user_id"] == uid]
        result["usage_split"] = {op: _cost([r for r in mine if r["operation"] == op])
                                 for op in sorted({r["operation"] for r in mine})}
        result["usage_split"]["total"] = _cost(mine)
        result["models_used"] = sorted({r["model"] for r in mine})
        result["art9_granted"] = not NO_ART9
    finally:
        db.close()
    for key in ("moments", "skills_full", "ideas_full"):
        print(f"  {key}:")
        for row in result[key]:
            print(f"     {row}")
    print(f"  state: {result['state']}")
    print(f"  usage_split: {result['usage_split']}")
    return result


E._bootstrap_env = _bootstrap_env
E._summary = _summary
E.run_story = run_story

if __name__ == "__main__":
    code = E.main()
    print(f"TOKENS TOTAL: {_cost(TOKENS)}  by op: "
          f"{ {op: _cost([r for r in TOKENS if r['operation'] == op]) for op in sorted({r['operation'] for r in TOKENS})} }")
    if "--json" in sys.argv:
        import json

        out = Path(sys.argv[sys.argv.index("--json") + 1]).with_suffix(".tokens.json")
        out.write_text(json.dumps(TOKENS, indent=1), encoding="utf-8")
    sys.exit(code)
