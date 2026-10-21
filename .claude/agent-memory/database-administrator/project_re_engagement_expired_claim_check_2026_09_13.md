---
name: re-engagement-expired-claim-check
description: Follow-up to the RE_ENGAGEMENT AI-render-waste bug — every EXPIRED moment in the 30d window WAS claimed/attempted; queue-timing ruled out as root cause
metadata:
  type: project
---

Follow-up query for backend-api (2026-09-13), answering what its own prior report
(`db-reports/2026-09-13-re-engagement-ai-render-waste.md` — referenced by backend-api
but not present in this checkout/session at query time, so treat as backend-api's
working doc, not independently re-verified here) left open: were the 81% EXPIRED
RE_ENGAGEMENT moments ever actually claimed for delivery, or did they sit in PENDING
untouched until the sweep?

**Result: all 30/30 were claimed** (`sent_at IS NOT NULL`, 30d window, moment_type=
RE_ENGAGEMENT, is_ai_generated=true, status=EXPIRED). Zero never-claimed rows. Of the
30 claimed: 22 (73%) reached `push_delivered=true` (delivered, then ignored within the
48h expiry window — user-disengagement, not a bug); 8 (27%) claimed but never delivered.
21 distinct users behind the 30 rows; 8/21 (38%) have zero rows in `user_fcm_token`
right now — consistent with (not row-joined/proven identical to) the 8 not-delivered
claims, i.e. plausibly explained by "no push token to send to," not a delivery-pipeline
failure.

**Systemic sanity check (7d, ALL moment_types, status=EXPIRED): 148/151 (98%) were
claimed, only 3 (2%) never-claimed.** This rules out the RQ `high`/`default`
queue-contention pattern ([[project_msv33_fix1_batch_2026_08_19]]) as the driver here —
`deliver_due_moments`'s 5-minute claim step is working fine fleet-wide. The
AI-render-waste bug is NOT a delivery-timing/queue problem.

**Implication for backend-api's root-cause / fix:** the waste is upstream of delivery —
re-opening AI-generation eligibility for users who are either (a) lapsed/uninstalled
with no FCM token at all, or (b) consistently ignoring RE_ENGAGEMENT pushes that DO
arrive. A queue/timing fix won't touch this; an eligibility/targeting fix (skip
AI-regeneration for zero-token users, or after N consecutive ignored RE_ENGAGEMENT
sends) would.

See also [[project_notification_moments_worker_registration_bug_2026_07_03]] for the
unrelated (already-fixed) worker-registration gap in this same table.
