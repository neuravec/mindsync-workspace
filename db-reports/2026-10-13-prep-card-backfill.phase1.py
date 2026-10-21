# Phase 1 (READ ONLY): candidate first-conversation threads for the prep card backfill.
# Run: heroku run --no-tty -a mindsync python < this_file
# Prints only sha prefixes, thread ids, timestamps, enums and booleans. No content, no UIDs.
import json, hashlib
from sqlalchemy import text, event
from app.db.session import engine, SessionLocal
from app.services import orca_memory, first_conversation
from app.tasks import first_conversation_prep_card as fc

engine.dispose()

@event.listens_for(engine, "connect")
def _ro(dbapi_conn, rec):
    cur = dbapi_conn.cursor()
    cur.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY")
    cur.execute("SET statement_timeout = 30000")
    cur.close()
    dbapi_conn.commit()

db = SessionLocal()

def q(sql, **p):
    try:
        rows = db.execute(text(sql), p).fetchall()
        db.rollback()
        return rows
    except Exception as e:
        db.rollback()
        print("ERR", type(e).__name__)
        return []

def H(uid):
    return hashlib.sha256(uid.encode()).hexdigest()[:8]

R = orca_memory._redis()
print("read_only", q("SHOW transaction_read_only"), "redis", R is not None, "cap", fc.daily_cap())
print("alembic", q("SELECT version_num FROM alembic_version"))
print("threads_by_status", [(r[0], r[1]) for r in q("SELECT status::text, count(*) FROM conversations WHERE entry_origin='onboarding_first_conversation' GROUP BY 1 ORDER BY 1")])

rows = q("""SELECT cv.id, cv.user_id, cv.created_at, cv.conversation_type::text
FROM conversations cv JOIN users u ON u.id=cv.user_id
WHERE cv.entry_origin='onboarding_first_conversation' AND cv.status::text='FINISHED'
ORDER BY cv.id LIMIT 500""")
print("finished_threads", len(rows))

out = []
for cid, uid, created, ctype in rows:
    rec = {"cid": cid, "h": H(uid), "created": str(created)[:19], "type": ctype}
    in_th, _st = first_conversation.user_is_in_therapy(db, uid)
    db.rollback()
    rec["in_therapy"] = bool(in_th)
    plat = q("SELECT coalesce(t.trial_platform, up.device_type, (SELECT platform FROM subscription_receipts sr WHERE sr.user_id=:u ORDER BY sr.id DESC LIMIT 1), 'unknown') FROM users u LEFT JOIN user_profile up ON up.user_id=u.id LEFT JOIN user_subscription_trial t ON t.user_id=u.id WHERE u.id=:u", u=uid)
    rec["platform"] = str(plat[0][0]) if plat else "unknown"
    try:
        prof = first_conversation.load_recap_profile(db, uid)
        tr = orca_memory.load_transcript(db, cid, prof.companion_name)
        db.rollback()
        last = fc._last_turn_at(tr)
        since = last or created
        rec["ended"] = str(since)[:19]
        content_ok = (not tr.crisis_language) and tr.user_turns > 0 and tr.meets_recap_floor()
        v = orca_memory.recap_verdict(cid, wait=False)
        rec["recap_cached"] = v is not None
        if v is not None and (v.crisis or v.status == orca_memory.RECAP_STATUS_SHORT):
            content_ok = False
        rec["content_gate_ok"] = bool(content_ok)
    except Exception as e:
        db.rollback()
        rec["transcript_err"] = type(e).__name__
        since = created
        rec["ended"] = str(created)[:19]
    cards = q("SELECT id, created_at, processing_status::text, deleted_at IS NOT NULL FROM session_prep_cards WHERE user_id=:u AND generation_type='auto' AND input_type::text='AUTO' AND created_at >= :s ORDER BY id", u=uid, s=since)
    rec["auto_cards_since"] = [(c[0], str(c[1])[:19], c[2], c[3]) for c in cards]
    rec["blocking_card"] = any(c[2] in ("COMPLETED", "PROCESSING") for c in cards)
    rec["claim_ttl"] = R.ttl(orca_memory.prep_card_claim_key(cid)) if R is not None else None
    out.append(rec)

for rec in out:
    print(json.dumps(rec, ensure_ascii=True))

cand = [r for r in out if r["in_therapy"] and not r["blocking_card"] and (r["claim_ttl"] is None or r["claim_ttl"] == -2)]
print("=== CANDIDATES (in therapy, no blocking card, no claim):", len(cand))
for r in cand:
    print("CAND", r["cid"], r["h"], r["ended"], r["platform"], "content_ok=%s" % r.get("content_gate_ok"), "recap_cached=%s" % r.get("recap_cached"))
print("not_in_therapy", sum(1 for r in out if not r["in_therapy"]), "blocked_by_card", sum(1 for r in out if r["blocking_card"]), "claimed", sum(1 for r in out if r["claim_ttl"] is not None and r["claim_ttl"] != -2))
db.close()
print("DONE_SENTINEL")
