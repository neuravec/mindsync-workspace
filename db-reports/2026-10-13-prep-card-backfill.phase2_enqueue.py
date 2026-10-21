# Phase 2: enqueue generate_first_conversation_prep_card once per selected thread on "default".
# Operator approval 2026-10-13 ("Recznie nadrob na starych"). DB is opened READ ONLY here;
# the only write is the RQ enqueue itself. Every gate is re-checked right before each enqueue
# and the job checks every gate again on the worker.
# Run: heroku run --no-tty -a mindsync python < this_file
import time, hashlib
from sqlalchemy import text, event
from app.db.session import engine, SessionLocal
from app.services import orca_memory, first_conversation
from app.core.rq_queue import rq_queue
from app.tasks.first_conversation_prep_card import generate_first_conversation_prep_card, JOB_TIMEOUT_SECONDS

THREADS = [28812, 28876, 29044, 29173]

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
print("queue", rq_queue.name, "len_before", len(rq_queue), "redis", R is not None)

for cid in THREADS:
    row = db.execute(text("SELECT user_id, status::text, entry_origin FROM conversations WHERE id=:c"), {"c": cid}).first()
    db.rollback()
    if row is None or row[1] != "FINISHED" or row[2] != "onboarding_first_conversation":
        print(cid, "SKIP thread_state")
        continue
    uid = row[0]
    h = hashlib.sha256(uid.encode()).hexdigest()[:8]
    in_th, _s = first_conversation.user_is_in_therapy(db, uid)
    db.rollback()
    last = db.execute(text("SELECT max(created_at) FROM messages WHERE conversation_id=:c"), {"c": cid}).scalar()
    db.rollback()
    n_cards = db.execute(text("SELECT count(*) FROM session_prep_cards WHERE user_id=:u AND generation_type='auto' AND input_type::text='AUTO' AND processing_status::text IN ('COMPLETED','PROCESSING') AND created_at >= :s"), {"u": uid, "s": last}).scalar()
    db.rollback()
    claim = R.exists(orca_memory.prep_card_claim_key(cid)) if R is not None else None
    if not in_th or n_cards or claim:
        print(cid, h, "SKIP recheck", "in_therapy=%s cards=%s claim=%s" % (in_th, n_cards, claim))
        continue
    job = rq_queue.enqueue(generate_first_conversation_prep_card, cid, uid, job_timeout=JOB_TIMEOUT_SECONDS)
    print(cid, h, "ENQUEUED job", job.id)
    time.sleep(5)

print("len_after", len(rq_queue))
db.close()
print("DONE_SENTINEL")
