from app.db.session import SessionLocal
from sqlalchemy import text
db = SessionLocal()
print("ACTIVE_NULL:", db.execute(text("SELECT id, user_id, subscription_type, start_date, end_date, (end_date - start_date) AS span FROM user_subscription WHERE granted_via IS NULL AND is_active = true ORDER BY start_date")).fetchall())
print("TESTER_USERS:", db.execute(text("SELECT id, email, created_at FROM users WHERE email ILIKE '%[tester A]%'")).fetchall())
print("SIGNUP_TRIAL_ANY:", db.execute(text("SELECT COUNT(*) FROM user_subscription WHERE granted_via = 'signup_trial'")).fetchall())
db.close()
print("DONE")
