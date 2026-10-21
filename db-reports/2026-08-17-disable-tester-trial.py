from app.db.session import SessionLocal
from sqlalchemy import text
UID = "<UID-3>"
db = SessionLocal()
before = db.execute(text("SELECT id, user_id, subscription_type, start_date, end_date, is_active FROM user_subscription WHERE user_id = :u"), {"u": UID}).fetchall()
print("BEFORE:", before)
res = db.execute(text("UPDATE user_subscription SET is_active = false WHERE id = 31285 AND user_id = :u AND is_active = true"), {"u": UID})
print("rows updated:", res.rowcount)
db.commit()
after = db.execute(text("SELECT id, user_id, subscription_type, start_date, end_date, is_active FROM user_subscription WHERE user_id = :u"), {"u": UID}).fetchall()
print("AFTER:", after)
db.close()
print("DONE")
