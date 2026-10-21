# KE (Character KD v2) backfill sizing, prod, 2026-10-19

**Question.** Before backfilling existing users into the new Character pipeline (KE, Heroku v574, migration `ke_a7c3e9f1b2d4`), how many people does it reach and how many entries would it read?

**Access.** Three read-only runs on `--no-tty` one-off dynos (run.6364, run.1554, run.1191). Every query ran in its own `SET TRANSACTION READ ONLY` transaction with a 90 s statement timeout and was rolled back. No DML or DDL was run, and no dynos were left running. This report contains counts only.

**k-anonymity.** The opt-in cohort has 10 people, which is under the 25-person threshold. Its per-person distribution (median, p90, max, buckets, per-source user counts) is therefore suppressed (n<25, suppressed). The totals and threshold counts below are enough for sizing.

## 1. Migration and tables

| Check | Result |
|---|---|
| `alembic_version` | `ke_a7c3e9f1b2d4` |
| `ke_*` tables present | 7/7: ke_user_state, ke_paths, ke_skills, ke_tools, ke_hard, ke_moments, ke_ideas |
| Row counts | 0 in every table |
| Late columns `ke_user_state.activated_at`, `last_opened_at` | present (timestamptz) |
| Effective settings inside the dyno | `CHARACTER_KE_ENABLED=False`, `CHARACTER_KE_EXTRACTION_ENABLED=False`, `CHARACTER_KE_REQUIRE_PROFILING_OPT_IN=True`, `KE_DAILY_CALL_CAP=60`, `KE_SWEEP_MAX_USERS=200`, `KE_SWEEP_RECENT_OPEN_DAYS=30`, `CHARACTER_KE_USER_IDS` has 0 entries |

None of these flags are set as Heroku config vars, so every value comes from code defaults. The tables are also built by `create_all` at boot, which is why the `alembic_version` row is the actual proof that the migration ran.

## 2. Consent (latest record per type, matching `app/crud/consent.py`)

Semantics: the latest row per (user_id, consent_type) ordered by `granted_at DESC` (with `id DESC` as a tiebreak; there are 0 tied pairs). A record is active when `withdrawn_at IS NULL`.

| Metric | Users |
|---|---|
| All users | 1972 |
| **PROFILING active (latest record granted)** | **10** |
| PROFILING withdrawn | 1 |
| PROFILING, no record at all | 1961 |
| **PROFILING active AND ARTICLE9_HEALTH active** | **9** |
| ARTICLE9_HEALTH active (all users) | 99 |
| Not withdrawn PROFILING (cohort if the opt-in flag were off) | 1971, of which 99 have Art. 9 active |

PROFILING history: 29 rows from 11 people, first grant in June 2026. Rows are written only by the Settings toggle, never by onboarding (see the `is_profiling_consent_withdrawn` docstring). In practice the opt-in cohort is "people who went into Settings and flipped the switch", and it probably includes the team's own test accounts. **Under the current default (`REQUIRE_PROFILING_OPT_IN=True`), a backfill reaches 10 accounts.**

## 3. Entries KE would read

Sources and filters follow `app/services/ke/extract.py`:

| cursor key | table | filter used here |
|---|---|---|
| reflect_talk | conversation_summaries JOIN conversations | summary_long or summary_short non-empty (all conversation types) |
| note | between_session_notes | deleted_at null, input_type not auto, summary/significance non-empty, or a typed note with raw_text that is not pending |
| after_therapy (Art. 9) | session_debriefs | deleted_at null, input_type not auto, snapshot/insights/threads non-empty |
| session (Art. 9) | session_recordings | deleted_at null, overview/insights/actions non-empty |
| realization | realizations | deleted_at null, is_auto_detected = false |
| todo_done | todo_completions JOIN todo_items | text non-empty; a repeating item skipped if completed within the previous 6 days; therapist homework counts as Art. 9 |

"Readable" means usable AND (not Art. 9, or the person's ARTICLE9_HEALTH is active). The 90-day window matches `BACKFILL_DAYS=90`. Crisis-language entries, which get no model call, cannot be counted because the text is encrypted. Treat the figures as an upper bound on extraction calls.

### Opt-in cohort (10 people, the current default)

| | all time | last 90 days |
|---|---|---|
| People with at least 1 readable entry | 7 | 6 |
| Total readable entries | 530 | **232** |
| Median / p90 / max per person | n<25, suppressed | n<25, suppressed |
| People with more than 15 entries (more than one job of `ENTRIES_PER_JOB=15`) | | 4 |
| People with more than 60 entries (more than one day at `KE_DAILY_CALL_CAP=60`) | | 2, each finishes within 2 days |

Readable entries by source over 90 days (all time in brackets): reflect_talk 24 (242), note 64 (97), after_therapy 30 (63), session 22 (30), realization 19 (19), todo_done 73 (79). The all-time reflect_talk figure is mostly legacy JOURNAL summaries, none of them in the last 90 days.

### Broader cohort if the opt-in flag were switched off (1971 people, no PROFILING withdrawal)

| | all time | last 90 days |
|---|---|---|
| People with at least 1 readable entry | 558 | 62 |
| Total readable entries | 2011 | **377** |
| Median / p90 / max per person (people with at least 1 entry) | 1 / 4.3 / 262 | 1 / 10 / 71 |
| People with more than 15 / more than 60 entries in 90 days | | 5 / 2 |
| Distribution in 90 days | | 0: 1909, 1-5: 49, 6 or more: 13 |

Without Art. 9 consent, 57 after-therapy cards, 2 sessions and 1 homework item (all time) would be skipped for good.

## 4. Active in the last 30 days

| Definition | Opt-in (10) | Broad (1971) |
|---|---|---|
| Sent a USER message | 6 | 37 |
| Has a readable KE entry | 6 | 37 |
| Started a conversation | 5 | 45 |
| `users.last_login` within 30 days | 8 | 136 (unreliable: 1834 of 1971 are NULL) |

## 5. Operator account

Matched by exact email, `+alias` and gmail dotless forms: **1 account** (created 2024-12-20). The UID was returned to the lead in the session and is deliberately not written here because reports are committed. Sign in with Apple private-relay accounts cannot be matched by email.

## Findings and handoffs

1. **The opt-in gate leaves the backfill with almost nobody to process.** It reaches 10 people and about 232 extraction calls for the 90-day window, roughly the same order as a single heavy user's history. Turning the flag off widens the cohort to 1971 people, but only 62 of them have anything in the window (377 calls). This is a product and legal decision for the operator (the open M-5 question), not a data problem.
2. **Reflect talks with no summary are invisible to KE (data-analytics).** Of 125 Reflect threads in the last 90 days that contain user messages, 53 (42%) have no `conversation_summaries` row. All 53 are still ACTIVE and have been idle for more than 7 days. They are not trivially short: 35 have 4 or more user messages and 20 have 10 or more. The gap is historical: July 6/6, August 27/29, September 20/32 and October 0/58 have no summary. KE reads only `conversation_summaries` (it deliberately ignores `reflect_summary_cards`), so these talks never reach the map. If they should count, `data-analytics` (owner of the summary jobs) should backfill summaries for those threads **before** the KE backfill runs, since the KE cursor will not revisit older rows.
3. **Activation gate.** The sweep only processes people with `ke_user_state.activated_at` set (they opened the tab). The table is empty, so a backfill has to create state rows or enqueue jobs directly. Owner: `backend-api`.
4. **Enum note.** `inputtypeenum` on prod now has both `auto` and `AUTO` (plus VOICE and TEXT). KE lowercases the value, so it is unaffected. Raw SQL must compare `lower(input_type::text)`.
5. **QA allowlist.** With `REQUIRE_PROFILING_OPT_IN=True`, an account on `CHARACTER_KE_USER_IDS` still sees the lock unless its latest PROFILING record is active. Before testing, flip the Settings toggle on the QA account.

## Addendum: premium users only (same day, run.7115)

**Definition used, exactly the gate in `app/api/v1/endpoints/_therapy_helpers.py::is_user_premium`.** It is called by about 20 endpoints and tasks (reflect, debriefs, session_recordings, stats and others). `GET /users/usage` (`resolve_plan`) also calls it. A user is premium when a `user_subscription` row has `is_active = true` AND one of:

- `end_date IS NULL`;
- `end_date > today (UTC)`;
- `end_date = today` AND `granted_via` is NULL or anything other than `signup_trial`. Paid access lasts through the expiry day; the sign-up trial ends at 00:00 UTC of `end_date`.

`subscription_type` is not checked. All 22 premium rows are PREMIUM anyway. The source split is `granted_via`, which is also what PostHog receives as `premium_source`. KE itself has no premium check.

`user_subscription` has 1968 rows, one per user. 28 have `is_active=true`, but 6 of those are past their `end_date`, so the gate correctly excludes them. `end_date` is a DATE on prod.

### Premium now, by source

| granted_via | Users | With a VERIFIED receipt | PROFILING active | ART9 active | Both |
|---|---|---|---|---|---|
| purchase | 8 | 8 | 3 | 6 | 3 |
| starter_pack | 1 | 1 | 0 | 0 | 0 |
| signup_trial | 10 | 0 | 0 | 3 | 0 |
| promo | 2 | 0 | 0 | 2 | 0 |
| NULL (legacy, no receipt) | 1 | 0 | 0 | 0 | 0 |
| **Total** | **22** | 9 | **3** | **11** | 3 |

- **Paid:** 9 (purchase plus starter_pack, all with a verified receipt).
- **Trial:** 10.
- **Promo or granted:** 3 (promo plus the legacy row).

Receipts have no environment column, so "paid" may include TestFlight or sandbox purchases.

No premium user has a withdrawn PROFILING record.

### KE-readable entries in the last 90 days (same source rules as above)

| Cohort | Users | With at least 1 entry | Entries, 90 days | Entries, all time | More than 15 / more than 60 entries |
|---|---|---|---|---|---|
| Premium, no PROFILING requirement | 22 | **12** | **187** | 268 | 3 / 1 |
| Premium with PROFILING active (current opt-in default) | 3 | **3** | **151** | 228 | 3 / 1 |

- Median and p90: the group with entries is 12 people in the first row and 3 in the second, both under 25, so these are suppressed.
- "No PROFILING requirement" gives the same result as "PROFILING not withdrawn", because no premium user has withdrawn.
- The single account over 60 entries finishes within 2 days at the daily cap of 60.
- Premium entries by plan source (90 days): purchase 8 users / 177 entries, signup_trial 2 / 2, promo 1 / 6, starter_pack 1 / 2, legacy 0 / 0. Paying users account for almost the whole volume.
- Premium entries by KE source (90 days): note 57, todo_done 47, reflect_talk 24, session 24, after_therapy 22, realization 13.

### The 53 Reflect threads without a summary

The count is unchanged at 53 threads, owned by 30 people. **17 threads belong to people who are premium now** (5 people): 16 purchase and 1 promo. Of those 17, 9 belong to the premium users with PROFILING active. Across all plans, 14 of the 53 belong to people with PROFILING active. Premium status is as of today, not as of when each thread was written.

**Takeaway.** "Premium plus PROFILING" is 3 people and 151 calls. "Premium regardless of PROFILING" is 12 people with content and 187 calls. Either way the backfill is small. The largest single gap in coverage is the 17 premium-owned Reflect talks that have no summary for KE to read.
