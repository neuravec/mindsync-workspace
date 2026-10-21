---
name: project-ke-backfill-sizing-2026-10-19
description: KE (Character KD v2) at v574 - alembic ke_a7c3e9f1b2d4, 7 ke_* tables empty; PROFILING opt-in cohort only 10 users (records come only from the Settings toggle); 42% of 90d Reflect threads lack conversation_summaries (pre-October gap) so KE cannot see them
metadata:
  type: project
---

Prod snapshot 2026-10-19 (report: db-reports/2026-10-19-ke-backfill-sizing.md):
- alembic_version = ke_a7c3e9f1b2d4; ke_user_state/paths/skills/tools/hard/moments/ideas all 0 rows. All KE flags are unset in Heroku config; code defaults apply (ENABLED False, EXTRACTION False, REQUIRE_PROFILING_OPT_IN True, DAILY_CALL_CAP 60).
- consent_records PROFILING: 29 rows from 11 users ever, 10 currently active (9 also have ARTICLE9_HEALTH active). ARTICLE9_HEALTH is active for 99 users. Onboarding never writes PROFILING, so in opt-in mode KE reaches roughly 10 accounts, probably mostly internal ones.
- 90-day KE-readable entries: opt-in cohort 232; not-withdrawn cohort (1971 users) 377 entries from 62 users.
- Reflect threads with USER messages but no conversation_summaries row: Jul 6/6, Aug 27/29, Sep 20/32, Oct 0/58. These are long threads too, and KE reads only conversation_summaries.
- users.last_login is NULL for about 93% of users, so it is useless as an activity signal. Use USER messages instead.
- inputtypeenum now has both 'auto' and 'AUTO'.
- Premium follows `_therapy_helpers.is_user_premium`: is_active plus an end_date guard, with the sign-up trial ending at 00:00 of end_date. On 2026-10-19 that was 22 users: purchase 8, starter_pack 1, signup_trial 10, promo 2, NULL legacy 1. Only 3 of them have PROFILING active, and 11 have ART9. 6 rows have is_active=true but are past their end_date (the guard excludes them). In the 90-day window, premium users have 187 KE entries from 12 people; premium plus PROFILING have 151 from 3 people.

**Why:** the operator is planning the KE backfill. These numbers decide whether the opt-in gate makes a backfill pointless.
**How to apply:** re-verify the counts before reuse, since consent and summaries change quickly. When anyone sizes KE or any PROFILING-gated feature, start from "the opt-in cohort is tiny". Related: [[project-onboarding-field-save-bug-2026-06-29]]
