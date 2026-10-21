---
name: Broadcast push notification
description: How to send push notifications to all users via admin broadcast endpoint
type: reference
---

## Admin Broadcast Push Notification

**Endpoint:** `POST /api/v1/admin/broadcast`
**Auth:** `X-Admin-Key` header (same key as admin_usage)
**Returns:** 202 Accepted immediately — RQ worker sends in background

**Files:**
- Endpoint: `app/api/v1/endpoints/admin_broadcast.py`
- RQ task: `app/tasks/broadcast.py`
- Registered in: `app/api/v1/api.py` under prefix `/admin`

**Usage:**
```bash
curl -X POST https://mindsync-829f3f05ed43.herokuapp.com/api/v1/admin/broadcast \
  -H "X-Admin-Key: <ADMIN_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"title":"...","body":"...","data":{"route":"/settings"}}'
```

**Behavior:**
- Sends FCM push to ALL registered tokens (skips DND)
- `data` field is optional — can include deep-link route
- RQ worker gets OAuth token once, sends all, logs progress every 100 tokens
- Invalid/expired tokens auto-cleaned from `user_fcm_token` table
- `job_timeout=600` (10 min max)
- Check delivery results in Heroku worker logs

**Production URL:** `https://mindsync-829f3f05ed43.herokuapp.com`
