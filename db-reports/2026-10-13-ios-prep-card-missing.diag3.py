import json, hashlib
from sqlalchemy import text, event
from app.db.session import engine, SessionLocal
from app.services import orca_memory

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
        print("ERR", type(e).__name__, str(e)[:300])
        return []

def H(uid):
    return hashlib.sha256(uid.encode()).hexdigest()[:8]

R = orca_memory._redis()
print("read_only", q("SHOW transaction_read_only"))
print("=== iOS-B: REFLECT threads whose last message is 2026-10-05 08:25..08:40 UTC ===")
rows = q("SELECT cv.id, cv.user_id, cv.created_at, cv.status::text, cv.entry_origin, max(m.created_at), count(*) FILTER (WHERE m.role::text='USER') FROM conversations cv JOIN messages m ON m.conversation_id=cv.id WHERE cv.conversation_type::text='REFLECT' GROUP BY 1,2,3,4,5 HAVING max(m.created_at) BETWEEN '2026-10-05 08:25' AND '2026-10-05 08:40' ORDER BY 6 LIMIT 20")
for r in rows:
    uid = r[1]
    u = q("SELECT u.created_at, u.first_conversation_claimed_at, up.device_type, t.trial_platform, up.currently_in_therapy IS NOT NULL, c.onboarding_completed FROM users u LEFT JOIN user_profile up ON up.user_id=u.id LEFT JOIN user_subscription_trial t ON t.user_id=u.id LEFT JOIN user_therapy_context c ON c.user_id=u.id WHERE u.id=:u", u=uid)
    cons = q("SELECT consent_type, granted_at, withdrawn_at, coalesce(source,'') FROM consent_records WHERE user_id=:u ORDER BY granted_at", u=uid)
    cards = q("SELECT id, created_at, input_type::text, coalesce(generation_type,''), processing_status::text, deleted_at IS NOT NULL FROM session_prep_cards WHERE user_id=:u AND created_at >= '2026-10-01' ORDER BY created_at", u=uid)
    ck = R.ttl(orca_memory.prep_card_claim_key(r[0])) if R is not None else None
    print(json.dumps({"cid": r[0], "h": H(uid), "t_created": str(r[2])[:19], "status": r[3], "origin": r[4], "last_msg": str(r[5])[:19], "user_msgs": r[6],
        "user": [str(x)[:19] for x in u[0]] if u else None, "consents": [(c[0], str(c[1])[:19], str(c[2])[:19] if c[2] else None, c[3]) for c in cons],
        "cards": [(c[0], str(c[1])[:19], c[2], c[3], c[4], c[5]) for c in cards], "claim_ttl": ck}, ensure_ascii=True))
db.close()
