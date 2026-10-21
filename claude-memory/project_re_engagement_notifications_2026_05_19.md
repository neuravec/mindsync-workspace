---
name: project-re-engagement-notifications-2026-05-19
description: "Re-engagement push generator for inactive users — backend only, no frontend toggle, not deployed"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4fb4e0d-7e23-439f-9f79-f09b69f097e8
---

Re-engagement ("we miss you") push notification generator — fills the gap where inactive users got NOTHING (all 4 existing Notification Moments generators require recent activity; investigation 2026-05-19 confirmed no re-engagement / dormant-user path existed).

**Status:** backend SHIPPED in code, NOT deployed. Frontend deliberately skipped.

**Why backend-only:** user decided against a dedicated settings toggle. The `re_engagement_push` preference exists on the backend (default `true`, subordinate to the master `notification_enabled` toggle) but has NO UI — users can only disable it via the master notification toggle. Flutter changes were built then fully reverted.

**How it works:**
- `ReEngagementGenerator` in `app/services/moments/re_engagement_generator.py`, registered with the notification orchestrator alongside the 4 existing generators.
- Inactivity = `today_local - last_activity_date` where last_activity is the max across conversations/debriefs/between-session notes/recordings/symptoms/realizations/reflections (`crud.get_last_activity_datetime()`).
- Escalation (self-healing thresholds, NOT strict equality — fixed same day): push #1 fires when `days_inactive >= 3 AND sent_count == 0`; push #2 when `days_inactive >= 7 AND sent_count == 1`; stop at `sent_count >= 2`. `>=` (not `==`) so a missed orchestrator day self-heals on day 4/5/6/7. Push number / content path driven by `sent_count`, not raw days. Window = "since last_activity_date" so it resets automatically when the user returns. State derived by counting non-terminal `RE_ENGAGEMENT` moments in `notification_moments` table after last_activity — no new table.
- Cold path (0 conversations / no history): templated onboarding-flavored fallback strings, no LLM. Warm path (has data): LLM-personalized (gpt, user `ai_language`), lock-screen-safe (no clinical terms), templated fallback on AI failure.
- Respects all universal gates: 10–19h local window, FCM token presence, master toggle, daily budget.

**Artifacts:** migration `mm3n4o5p6q7r` (down_revision `ll2m3n4o5p6q`) — adds `re_engagement_push` bool to `user_preferences` + `RE_ENGAGEMENT` to `moment_type_enum`. New `MomentTypeEnum.RE_ENGAGEMENT` mapped to `REFLECTIONS` category. Config: `RE_ENGAGEMENT_PROMPT` + 8 fallback string constants (all have baked-in defaults, no .env change). 106 tests in `test_re_engagement_generator.py`, all pass.

**To deploy:** apply migration `mm3n4o5p6q7r`, then deploy backend. See [[reference_broadcast_push]] for verifying the FCM pipeline independently.
