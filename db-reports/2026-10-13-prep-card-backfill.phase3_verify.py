# Phase 3 (READ ONLY): outcome per backfilled thread. Run: heroku run --no-tty -a mindsync python < this_file
import hashlib
from sqlalchemy import text, event
from rq.job import Job
from app.db.session import engine, SessionLocal
from app.core.redis import redis_client
from app.services import orca_memory

JOBS = {28812: "6894d383-5e94-46da-b160-1d3ed0293cd2", 28876: "7d9799e2-6465-4992-9ac6-bf87760afb0d",
        29044: "d1524aba-35b0-4ae0-93a5-d155acece43f", 29173: "10a55569-b777-44e4-96fc-16e910117a8d"}

engine.dispose()

@event.listens_for(engine, "connect")
def _ro(dbapi_conn, rec):
    cur = dbapi_conn.cursor()
    cur.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY")
    cur.execute("SET statement_timeout = 30000")
    cur.close()
    dbapi_conn.commit()

db = SessionLocal()
R = orca_memory._redis()
for cid, jid in JOBS.items():
    uid = db.execute(text("SELECT user_id FROM conversations WHERE id=:c"), {"c": cid}).scalar()
    db.rollback()
    h = hashlib.sha256(uid.encode()).hexdigest()[:8]
    last = db.execute(text("SELECT max(created_at) FROM messages WHERE conversation_id=:c"), {"c": cid}).scalar()
    cards = db.execute(text("SELECT id, created_at, processing_status::text, session_date IS NOT NULL, week_in_brief IS NOT NULL, deleted_at IS NOT NULL FROM session_prep_cards WHERE user_id=:u AND input_type::text='AUTO' AND created_at >= :s ORDER BY id"), {"u": uid, "s": last}).fetchall()
    db.rollback()
    try:
        j = Job.fetch(jid, connection=redis_client)
        st, res = j.get_status(), j.return_value()
        exc = (j.exc_info or "").strip().splitlines()[-1][:80] if j.exc_info else None
    except Exception as e:
        st, res, exc = "fetch_err", None, type(e).__name__
    print(cid, h, "job", st, "result", "skipped" if res in ("skipped:crisis", "skipped:short", "skipped:not_in_therapy") else res, "exc", exc,
          "claim", bool(R.exists(orca_memory.prep_card_claim_key(cid))) if R is not None else None,
          "cards", [(c[0], str(c[1])[:19], c[2], "has_date=%s" % c[3], "has_brief=%s" % c[4], "deleted=%s" % c[5]) for c in cards])
db.close()
print("DONE_SENTINEL")
