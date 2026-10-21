import json, hashlib, datetime as dt
from collections import Counter
from sqlalchemy import text, event
from app.db.session import engine, SessionLocal

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

def P(*a):
    print(*a, flush=True)

P("read_only", q("SHOW transaction_read_only"))
PLAT = "CASE WHEN up.device_type IS NOT NULL THEN up.device_type WHEN lower(t.trial_platform) IN ('ios','apple') THEN 'ios' WHEN lower(t.trial_platform) IN ('android','google') THEN 'android' ELSE 'unknown' END"
BASE = "FROM users u LEFT JOIN user_profile up ON up.user_id=u.id LEFT JOIN user_subscription_trial t ON t.user_id=u.id LEFT JOIN user_therapy_context c ON c.user_id=u.id"

P("=== F1. weekly by platform since 2026-08-01: users, onb_completed, art9 row, cit filled, marked thread ===")
for r in q("SELECT date_trunc('week', u.created_at)::date AS wk, " + PLAT + " AS pf, count(*), count(*) FILTER (WHERE c.onboarding_completed), count(*) FILTER (WHERE EXISTS (SELECT 1 FROM consent_records cr WHERE cr.user_id=u.id AND cr.consent_type='ARTICLE9_HEALTH')), count(up.currently_in_therapy), count(up.age_band), count(up.lead_source), count(*) FILTER (WHERE EXISTS (SELECT 1 FROM conversations cv WHERE cv.user_id=u.id AND cv.entry_origin='onboarding_first_conversation')), count(c.id) " + BASE + " WHERE u.created_at >= '2026-08-01' GROUP BY 1,2 ORDER BY 1,2"):
    P(" ", *r)

P("=== F2. platform signal mix since 2026-09-15 (device_type set only by POST /subscription; trial_platform from trial row) ===")
for r in q("SELECT date_trunc('week', u.created_at)::date, up.device_type, t.trial_platform, count(*) " + BASE + " WHERE u.created_at >= '2026-09-15' GROUP BY 1,2,3 ORDER BY 1,2,3"):
    P(" ", *r)

P("=== F3. consent_type mix since 2026-10-01 by platform ===")
for r in q("SELECT " + PLAT + ", cr.consent_type, coalesce(cr.source,'(null)'), count(DISTINCT u.id) " + BASE + " JOIN consent_records cr ON cr.user_id=u.id WHERE u.created_at >= '2026-10-01' GROUP BY 1,2,3 ORDER BY 1,2,3"):
    P(" ", *r)

P("=== F4. ART9 rows written by anyone since 2026-10-01, by platform of writer ===")
for r in q("SELECT date_trunc('day', cr.granted_at)::date, " + PLAT + ", count(*) FROM consent_records cr JOIN users u ON u.id=cr.user_id LEFT JOIN user_profile up ON up.user_id=u.id LEFT JOIN user_subscription_trial t ON t.user_id=u.id WHERE cr.consent_type='ARTICLE9_HEALTH' AND cr.granted_at >= '2026-10-01' GROUP BY 1,2 ORDER BY 1,2"):
    P(" ", *r)

P("=== F5. new-flow iOS users (trial_platform ios, created >= 2026-10-01): field presence, no values ===")
rows = q("SELECT u.id, u.created_at, up.device_type, up.age_band IS NOT NULL, up.gender IS NOT NULL, up.lead_source IS NOT NULL, up.currently_in_therapy IS NOT NULL, up.full_name IS NOT NULL, up.pronouns IS NOT NULL, c.onboarding_completed, c.onboarding_step, c.medical_disclaimer_accepted_at, c.gdpr_consent_at, c.age_verified_at, c.consent_version, c.focus_areas IS NOT NULL, c.updated_at, u.first_conversation_claimed_at " + BASE + " WHERE u.created_at >= '2026-10-01' AND (lower(t.trial_platform) IN ('ios','apple') OR up.device_type='ios') ORDER BY u.created_at")
for r in rows:
    uid = r[0]
    cons = q("SELECT consent_type, granted_at, withdrawn_at IS NULL, coalesce(source,''), consent_version FROM consent_records WHERE user_id=:u ORDER BY granted_at", u=uid)
    pref = q("SELECT time_zone IS NOT NULL, therapy_frequency, next_session_date IS NOT NULL FROM user_preferences WHERE user_id=:u", u=uid)
    sub = q("SELECT subscription_type::text, is_active, start_date FROM user_subscription WHERE user_id=:u", u=uid)
    nconv = q("SELECT count(*) FROM conversations WHERE user_id=:u", u=uid)[0][0]
    nmsg = q("SELECT count(*) FROM messages m JOIN conversations cv ON cv.id=m.conversation_id WHERE cv.user_id=:u", u=uid)[0][0]
    P(json.dumps({"h": H(uid), "created": str(r[1])[:19], "dev": r[2], "age_band": r[3], "gender": r[4], "lead": r[5], "cit": r[6], "name": r[7], "pron": r[8],
        "onb_done": r[9], "onb_step": r[10], "disclaimer": str(r[11])[:19] if r[11] else None, "gdpr_at": str(r[12])[:19] if r[12] else None, "age_at": str(r[13])[:19] if r[13] else None,
        "cver": r[14], "focus": r[15], "ctx_upd": str(r[16])[:19] if r[16] else None, "claimed": str(r[17])[:19] if r[17] else None,
        "consents": [(c[0], str(c[1])[:19], c[2], c[3], c[4]) for c in cons], "prefs": [tuple(p) for p in pref], "sub": [tuple(map(str, s)) for s in sub], "nconv": nconv, "nmsg": nmsg}, ensure_ascii=True))

P("=== F6. same presence profile, new-flow Android since 2026-10-11 (contrast) ===")
rows = q("SELECT u.id, u.created_at, up.age_band IS NOT NULL, up.gender IS NOT NULL, up.lead_source IS NOT NULL, up.currently_in_therapy IS NOT NULL, c.onboarding_completed, c.onboarding_step, c.gdpr_consent_at IS NOT NULL, c.consent_version " + BASE + " WHERE u.created_at >= '2026-10-11' AND lower(t.trial_platform)='android' ORDER BY u.created_at")
for r in rows:
    cons = q("SELECT consent_type, coalesce(source,''), consent_version FROM consent_records WHERE user_id=:u ORDER BY granted_at", u=r[0])
    P(json.dumps({"h": H(r[0]), "created": str(r[1])[:19], "age_band": r[2], "gender": r[3], "lead": r[4], "cit": r[5], "onb_done": r[6], "onb_step": r[7], "gdpr_at": r[8], "cver": r[9], "consents": [tuple(c) for c in cons]}, ensure_ascii=True))

P("=== F7. AUTO cards all-time with creator platform ===")
for r in q("SELECT s.id, s.created_at, s.processing_status::text, " + PLAT + " FROM session_prep_cards s JOIN users u ON u.id=s.user_id LEFT JOIN user_profile up ON up.user_id=u.id LEFT JOIN user_subscription_trial t ON t.user_id=u.id WHERE s.input_type::text='AUTO' ORDER BY s.created_at"):
    P(" ", *r)

P("=== F8. all marked first-conversation threads since 2026-10-11 20:40 (any account age) by platform ===")
for r in q("SELECT " + PLAT + ", cv.status::text, count(*), count(*) FILTER (WHERE u.created_at < '2026-10-11 20:40+00') " + BASE + " JOIN conversations cv ON cv.user_id=u.id WHERE cv.entry_origin='onboarding_first_conversation' AND cv.created_at >= '2026-10-11 20:40+00' GROUP BY 1,2 ORDER BY 1,2"):
    P(" ", *r)

db.close()
