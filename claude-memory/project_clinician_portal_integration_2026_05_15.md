---
name: clinician-portal-integration-2026-05-15
description: "Therapist-deck portal wired end-to-end to the MindSync app's invite-code feature; deployment is operator-gated"
metadata: 
  node_type: memory
  type: project
  originSessionId: 61b59d96-4399-46f7-84e8-3a5671426022
---

# Clinician portal integration — wired end-to-end 2026-05-15

The therapist-deck clinician portal (`Heroku/therapist-deck/`, Next.js 16 BFF) is now connected
end-to-end to the MindSync backend and mobile app's "redeem therapist invite code" feature.

**Why:** the feature was ~90% built across all three sides but disconnected — the portal's write
path was mock (InviteModal generated codes with `Math.random()`), and no Clinician row could be
created so portal login was impossible.

**What shipped this session:**
- Backend: `POST/GET /api/v1/admin/clinicians` (X-Admin-Key) to provision clinics + clinician
  accounts; `sharingSince` field added to clinician `PatientResponse`. 88 clinician tests pass.
- Portal: real server actions (`src/app/(authed)/patients/actions.ts`) for issue/cancel invite,
  revoke patient, create session; InviteModal + patient shells rewired off mock data; `server-only`
  added as a direct dependency.
- Flutter side was already complete (consent code entry, redeem cubit, manager, routes, DI).

**How to apply:**
- Deployment is OPERATOR-GATED — not done. Before the portal works: set Heroku config vars
  `CLINICIAN_JWT_SECRET` (≥32 chars), `LOOPS_CLINICIAN_MAGIC_TEMPLATE_ID`, `CLINICIAN_PORTAL_URL`,
  `ADMIN_API_KEY`; create the Loops transactional template (data vars `magic_url`, `full_name`,
  `expires_minutes`); run `alembic upgrade head` (migration `jj0k1l2m3n4o`); set
  `MINDSYNC_API_BASE_URL` in Vercel; create the first clinician via the admin curl.
- Known backlog (non-blocking, from reviews): admin `GET` list is unpaginated; no startup warning
  if `ADMIN_API_KEY` unset; patient-list table uses `role="button"` on `<tr>` (a11y).

See [[reference_codemagic_setup]] for CI context.
