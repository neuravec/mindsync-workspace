import json, hashlib, datetime as dt
from collections import defaultdict, Counter
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

P("=== A. read-only + migration state ===")
P("read_only", q("SHOW transaction_read_only"))
P("alembic", q("SELECT version_num FROM alembic_version"))
P("inputtypeenum", [r[0] for r in q("SELECT e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid WHERE t.typname='inputtypeenum' ORDER BY e.enumsortorder")])
P("featureenum MOOD_TREND", q("SELECT count(*) FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid WHERE t.typname='featureenum' AND e.enumlabel='MOOD_TREND'"))
P("cast AUTO", q("SELECT CAST('AUTO' AS inputtypeenum)::text"))
P("now", q("SELECT now()"))
P("cols", q("SELECT table_name, column_name FROM information_schema.columns WHERE (table_name='conversations' AND column_name IN ('entry_origin','modality')) OR (table_name='users' AND column_name='first_conversation_claimed_at') OR (table_name='user_profile' AND column_name='device_type') OR (table_name='user_subscription_trial' AND column_name='trial_platform')"))

P("=== B. prep cards since 2026-10-01 by day/type/status ===")
for r in q("SELECT date_trunc('day', created_at)::date, input_type::text, coalesce(generation_type,'(null)'), processing_status::text, count(*) FROM session_prep_cards WHERE created_at >= '2026-10-01' GROUP BY 1,2,3,4 ORDER BY 1,2,3,4"):
    P(" ", *r)
P("AUTO all-time", q("SELECT processing_status::text, count(*) FROM session_prep_cards WHERE input_type::text IN ('AUTO','auto') GROUP BY 1"))

# Redis
from app.services import orca_memory, first_conversation
from app.tasks import first_conversation_prep_card as fcp
R = None
try:
    R = orca_memory._redis()
except Exception as e:
    P("redis err", type(e).__name__)
P("redis", R is not None)

def rttl(key):
    if R is None:
        return None
    try:
        return R.ttl(key)
    except Exception:
        return None

CUT = dt.datetime(2026, 10, 11, 20, 40, tzinfo=dt.timezone.utc)
users = q("SELECT u.id, u.created_at, u.first_conversation_claimed_at FROM users u WHERE u.created_at >= '2026-10-01' ORDER BY u.created_at LIMIT 3000")
P("cohort users", len(users))

def aware(v):
    if v is None:
        return None
    return v if v.tzinfo else v.replace(tzinfo=dt.timezone.utc)

recs = []
for uid, created, claimed in users:
    r = {"h": H(uid), "created": aware(created), "claimed": aware(claimed)}
    r["win"] = "post_fix" if aware(created) >= CUT else "pre_fix"
    pr = q("SELECT device_type, currently_in_therapy IS NOT NULL, age_band IS NOT NULL FROM user_profile WHERE user_id=:u", u=uid)
    r["has_profile"] = bool(pr)
    r["device_type"] = pr[0][0] if pr else None
    r["cit_filled"] = bool(pr and pr[0][1])
    tr = q("SELECT trial_platform FROM user_subscription_trial WHERE user_id=:u", u=uid)
    r["trial_platform"] = tr[0][0] if tr else None
    rc = q("SELECT DISTINCT platform FROM subscription_receipts WHERE user_id=:u", u=uid)
    r["receipt_platform"] = ",".join(sorted(x[0] for x in rc)) or None
    r["fcm"] = q("SELECT count(*) FROM user_fcm_token WHERE user_id=:u", u=uid)[0][0]
    utc = q("SELECT onboarding_completed, onboarding_step, gdpr_consent_at IS NOT NULL, updated_at FROM user_therapy_context WHERE user_id=:u", u=uid)
    r["onb_done"] = bool(utc and utc[0][0])
    r["onb_step"] = utc[0][1] if utc else None
    r["onb_updated"] = aware(utc[0][3]) if utc else None
    cons = q("SELECT consent_type, max(granted_at), bool_or(withdrawn_at IS NULL) FROM consent_records WHERE user_id=:u GROUP BY 1", u=uid)
    r["consents"] = {c[0]: (aware(c[1]), c[2]) for c in cons}
    r["art9"] = "ARTICLE9_HEALTH" in r["consents"]
    try:
        r["in_therapy"] = first_conversation.user_is_in_therapy(db, uid)[0]
        db.rollback()
    except Exception as e:
        db.rollback()
        r["in_therapy"] = None
    th = q("SELECT c.id, c.created_at, c.status::text, c.conversation_type::text, c.modality, (SELECT count(*) FROM messages m WHERE m.conversation_id=c.id AND m.role::text='USER'), (SELECT count(*) FROM messages m WHERE m.conversation_id=c.id), (SELECT max(m.created_at) FROM messages m WHERE m.conversation_id=c.id) FROM conversations c WHERE c.user_id=:u AND c.entry_origin='onboarding_first_conversation' ORDER BY c.created_at", u=uid)
    r["threads"] = []
    for t in th:
        cid = t[0]
        d = {"cid": cid, "created": aware(t[1]), "status": t[2], "ctype": t[3], "modality": t[4], "user_msgs": t[5], "msgs": t[6], "last_msg": aware(t[7])}
        d["claim_ttl"] = rttl(orca_memory.prep_card_claim_key(cid))
        d["analysis_ttl"] = rttl("reflect:analysis_job:%d" % cid)
        try:
            v = orca_memory._load_cached_recap(cid)
        except Exception:
            v = None
        d["recap"] = (v.status, v.saved_line_kind, bool(v.crisis)) if v else None
        try:
            prof = first_conversation.load_recap_profile(db, uid)
            tx = orca_memory.load_transcript(db, cid, prof.companion_name)
            db.rollback()
            d["tx_turns"] = tx.user_turns
            d["tx_floor"] = tx.meets_recap_floor()
            d["tx_crisis"] = bool(tx.crisis_language)
        except Exception as e:
            db.rollback()
            d["tx_turns"] = None
            d["tx_floor"] = None
            d["tx_crisis"] = None
            d["tx_err"] = type(e).__name__
        since = d["last_msg"] or d["created"]
        cards = q("SELECT id, created_at, processing_status::text, input_type::text, coalesce(generation_type,''), deleted_at IS NOT NULL, session_date IS NOT NULL FROM session_prep_cards WHERE user_id=:u AND created_at >= :s ORDER BY created_at", u=uid, s=since)
        d["cards"] = [(c[0], aware(c[1]), c[2], c[3], c[4], c[5], c[6]) for c in cards]
        d["recap_tok"] = q("SELECT min(created_at), count(*) FROM token_usage_log WHERE user_id=:u AND operation ILIKE '%first_conversation_recap%' AND created_at >= :s", u=uid, s=d["created"])[0]
        d["prep_tok"] = q("SELECT min(created_at), count(*) FROM token_usage_log WHERE user_id=:u AND feature::text='PREP_CARD' AND created_at >= :s", u=uid, s=d["created"])[0]
        d["sum_rows"] = q("SELECT count(*) FROM conversation_summaries WHERE conversation_id=:c", c=cid)[0][0]
        r["threads"].append(d)
    r["other_convs"] = q("SELECT count(*) FROM conversations WHERE user_id=:u AND (entry_origin IS DISTINCT FROM 'onboarding_first_conversation')", u=uid)[0][0]
    r["any_cards"] = q("SELECT count(*) FROM session_prep_cards WHERE user_id=:u", u=uid)[0][0]
    recs.append(r)

def plat(r):
    dtp = r["device_type"]
    tp = (r["trial_platform"] or "").lower()
    rp = (r["receipt_platform"] or "")
    if dtp:
        return dtp
    if tp in ("ios", "apple"):
        return "ios"
    if tp in ("android", "google"):
        return "android"
    if rp == "apple":
        return "ios"
    if rp == "google":
        return "android"
    return "unknown"

P("=== C. platform signal agreement ===")
agree = Counter()
for r in recs:
    agree[(r["device_type"], r["trial_platform"], r["receipt_platform"])] += 1
for k, v in agree.most_common(20):
    P(" ", k, v)

def thr(r):
    return r["threads"][-1] if r["threads"] else None

STEPS = [
    ("users", lambda r, t: True),
    ("has_profile", lambda r, t: r["has_profile"]),
    ("onb_completed", lambda r, t: r["onb_done"]),
    ("gdpr_consent_row", lambda r, t: "GDPR" in r["consents"]),
    ("art9_consent_row", lambda r, t: r["art9"]),
    ("cit_filled", lambda r, t: r["cit_filled"]),
    ("in_therapy_gate", lambda r, t: r["in_therapy"] is True),
    ("fc_thread", lambda r, t: t is not None),
    ("fc_REFLECT", lambda r, t: t is not None and t["ctype"] == "REFLECT"),
    ("fc_FINISHED", lambda r, t: t is not None and t["status"] == "FINISHED"),
    ("fc_user_msgs>0", lambda r, t: t is not None and (t["user_msgs"] or 0) > 0),
    ("fc_floor_ok", lambda r, t: t is not None and t["tx_floor"] is True),
    ("fc_recap_tok", lambda r, t: t is not None and t["recap_tok"][1] > 0),
    ("fc_summary_row(analysis ran)", lambda r, t: t is not None and t["sum_rows"] > 0),
    ("IT+FINISHED+floor", lambda r, t: t is not None and r["in_therapy"] is True and t["status"] == "FINISHED" and t["tx_floor"] is True),
    ("claim_key_present", lambda r, t: t is not None and (t["claim_ttl"] or -2) > 0),
    ("prep_tok_logged", lambda r, t: t is not None and t["prep_tok"][1] > 0),
    ("AUTO_card_row", lambda r, t: t is not None and any(c[3] in ("AUTO", "auto") for c in t["cards"])),
    ("AUTO_card_COMPLETED", lambda r, t: t is not None and any(c[3] in ("AUTO", "auto") and c[2] == "COMPLETED" for c in t["cards"])),
]

P("=== D. funnel per window x platform (latest marked thread per user) ===")
groups = defaultdict(list)
for r in recs:
    groups[(r["win"], plat(r))].append(r)
for key in sorted(groups):
    rs = groups[key]
    P("--", key, "n=%d" % len(rs))
    for name, f in STEPS:
        P("   %-30s %d" % (name, sum(1 for r in rs if f(r, thr(r)))))

P("=== D2. health-gate aggregate on IT+FINISHED threads (no per-user) ===")
for key in sorted(groups):
    rs = [r for r in groups[key] if thr(r) and r["in_therapy"] is True and thr(r)["status"] == "FINISHED"]
    c = Counter()
    for r in rs:
        t = thr(r)
        if t["tx_crisis"] or (t["recap"] and t["recap"][2]):
            c["crisis"] += 1
        elif not t["tx_floor"]:
            c["short"] += 1
        else:
            c["passes_health_gates"] += 1
        c["recap_kind=" + str(t["recap"][1] if t["recap"] else None)] += 1
    P("--", key, dict(c))

P("=== D3. thread status/type/modality/user_msgs buckets per platform ===")
for key in sorted(groups):
    c = Counter()
    for r in groups[key]:
        t = thr(r)
        if t is None:
            c["no_thread"] += 1
            continue
        um = t["user_msgs"] or 0
        b = "0" if um == 0 else ("1" if um == 1 else ("2-4" if um < 5 else "5+"))
        c["%s/%s/%s/um=%s" % (t["ctype"], t["status"], t["modality"], b)] += 1
    P("--", key, dict(c))

P("=== D4. multiple marked threads per user ===")
P(Counter((r["win"], plat(r), len(r["threads"])) for r in recs))

def fmt(v):
    if isinstance(v, dt.datetime):
        return v.strftime("%m-%d %H:%M:%S")
    return v

P("=== E. per-user samples (post_fix first, then pre_fix), hash only ===")
for win in ("post_fix", "pre_fix"):
    for pl in ("ios", "android", "unknown"):
        rs = [r for r in groups.get((win, pl), []) if r["threads"]]
        P("--", win, pl, "with_thread=%d" % len(rs))
        for r in rs[-12:]:
            t = thr(r)
            dur = (t["last_msg"] - t["created"]).total_seconds() if t["last_msg"] else None
            P(json.dumps({
                "h": r["h"], "created": fmt(r["created"]), "dev": r["device_type"], "trial_pf": r["trial_platform"], "rcpt": r["receipt_platform"],
                "onb": r["onb_done"], "onb_upd": fmt(r["onb_updated"]), "gdpr": "GDPR" in r["consents"], "art9": r["art9"], "cit_filled": r["cit_filled"],
                "claimed": fmt(r["claimed"]), "nthreads": len(r["threads"]), "cid": t["cid"], "t_created": fmt(t["created"]), "status": t["status"],
                "ctype": t["ctype"], "modality": t["modality"], "user_msgs": t["user_msgs"], "msgs": t["msgs"], "dur_s": dur, "last_msg": fmt(t["last_msg"]),
                "floor": t["tx_floor"], "recap_status": t["recap"][0] if t["recap"] else None, "recap_kind": t["recap"][1] if t["recap"] else None,
                "recap_tok": [fmt(t["recap_tok"][0]), t["recap_tok"][1]], "sum_rows": t["sum_rows"], "analysis_ttl": t["analysis_ttl"], "claim_ttl": t["claim_ttl"],
                "prep_tok": [fmt(t["prep_tok"][0]), t["prep_tok"][1]], "cards": [(c[0], fmt(c[1]), c[2], c[3], c[4], c[5], c[6]) for c in t["cards"]],
                "any_cards": r["any_cards"], "other_convs": r["other_convs"],
            }, default=str, ensure_ascii=True))

db.close()
