from app.db.session import SessionLocal
from sqlalchemy import text
db = SessionLocal()
print("DIST:", db.execute(text("SELECT granted_via, is_active, COUNT(*) FROM user_subscription GROUP BY granted_via, is_active ORDER BY granted_via, is_active")).fetchall())
print("ROW298:", db.execute(text("SELECT id, granted_via, is_active FROM user_subscription WHERE id = 298")).fetchall())
print("ALEMBIC:", db.execute(text("SELECT version_num FROM alembic_version")).fetchall())
db.close()
print("VERIFY_DONE")
