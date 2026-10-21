# First voice conversation after an onboarding re-run: prod evidence for the generic opener

- **Date:** 2026-10-05, queried about 16:20 UTC
- **Requested by:** lead, after the operator re-ran onboarding on an account that had already had its first conversation and Orca opened with a generic greeting instead of the survey-based script
- **Approved scope (operator, 2026-10-05):** decrypt only Orca's (the agent's) lines, never the user's words, plus presence flags showing whether the survey data was in the database. No DML, no DDL.
- **Access:** three Heroku one-off dynos on `mindsync` (`run.5264`, `run.6394`, `run.9203`) with the script piped over stdin (`heroku run --no-tty`). Each dyno exited on EOF, and `heroku ps` showed no one-off dyno afterwards. The Heroku CLI session was invalid, so the CLI was given the `_netrc` token as `HEROKU_API_KEY` (the value was never printed).
- **Safety:** every query ran in its own transaction opened with `SET TRANSACTION READ ONLY` and `SET LOCAL statement_timeout = 15000`, followed by `rollback()`. There was no `commit()`, no DML and no DDL. System prompts (message 0) were never decrypted. User messages were never decrypted either: their size comes from the length of the Fernet envelope alone, which gives a range accurate to within 16 bytes. Orca lines were decrypted inside the dyno, and the dyno masked the user's name, focus areas, survey chips and therapist names before printing. Anything the dyno missed (see the privacy note) was redacted by hand before writing this report.
- **Identifiers:** accounts appear as the first 10 hex characters of `sha256(user_id)`. Conversations appear as labels (A1, B3, ...) and their database ids are deliberately left out.

## Verdict

**Prod confirms the code analysis.** On account `225a543db2` the first-conversation claim was taken at 08:32:10 UTC by a marked thread, and Orca opened that thread with the survey script. Onboarding was later re-run and finished at 15:33:52 / 15:34:14 UTC with 3 focus areas, 3 severity ratings and an active ARTICLE9_HEALTH consent. Eight seconds later a voice Reflect thread was created with `entry_origin = NULL`, no seed and the claim already taken. Its first Orca line was a generic greeting that mentioned none of the survey. Two more ordinary voice threads from earlier that day open with a bare greeting and no question, which is exactly what the `OPENING GREETING` block asks for.

This is **working as designed** (spec 4.2 plus security audit M-1: one first conversation per account, and the claim is never reset). It is not a persistence bug: the survey data was saved, but the ordinary-thread path does not use it for the opener. Whether a re-run *should* get a survey-aware opener is a product decision (section 7).

## 1. How the code routes a re-run (reference, read on 2026-10-05)

- `POST /reflect/start` with `entry="onboarding_first_conversation"` (`app/api/v1/endpoints/reflect.py`, `start_reflect_thread`): an ACTIVE marked thread is resumed. Otherwise a new marked thread is created **only** when the account has no marked thread at all **and** wins `claim_first_conversation` (`UPDATE users SET first_conversation_claimed_at = now WHERE ... IS NULL`). Every other case (a FINISHED or deleted marked thread, a claim already taken) clears the seed fields and falls through to an **ordinary** Reflect thread.
- The voice `session_data` route appends `reflect_entry.build_voice_greeting_instruction()` ("Greet them in one sentence ... Ask no question. Mention nothing you know about them") whenever the thread has no USER message and no seed. That is what an ordinary, unseeded re-run thread gets.
- Orca's lines are stored as `messages.role = 'SYSTEM'` rows after message 0, and message 0 is the system prompt (the same convention `reflect.py` uses, `messages_db[1:]`, SYSTEM becomes assistant). The `AGENT` role was 0 in every thread checked.

## 2. Schema and migration state

| check | result |
|---|---|
| `alembic_version` | `m316a1b2c3d4` |
| `users.first_conversation_claimed_at` | present, `timestamp with time zone` |
| `conversations.entry_origin` | present, `character varying` |
| `conversations.created_at`, `messages.created_at` | `timestamp without time zone` (the app writes UTC wall time; known drift, see the CS-07 notes) |
| `user_therapy_context` | has `created_at`, `updated_at`, `onboarding_step`, `onboarding_completed` and the consent timestamps |
| `user_profile` | no `updated_at`, so a change to `full_name` or `gender` cannot be timed |

## 3. Step 1: which accounts are re-run candidates

| metric | value |
|---|---|
| accounts with `first_conversation_claimed_at` set (all-time) | **3**, all claimed on 2026-10-05 between 08:32:10 and 16:14:41 UTC |
| marked threads (`entry_origin IS NOT NULL`) in prod | 2, on 2 accounts |
| claimed accounts with at least 1 Reflect thread since 2026-10-03 | 3 |
| **claimed accounts with more than 1 Reflect thread since 2026-10-03** | **2** |

| account | claimed_at (UTC) | Reflect threads since 10-03 | first | last |
|---|---|---|---|---|
| `63a0d3a464` | 2026-10-05 16:14:41 | 3 | 10-03 10:05:13 | 10-05 16:14:41 |
| `225a543db2` | 2026-10-05 08:32:10 | 6 | 10-03 07:52:30 | 10-05 15:34:22 |

Both are internal test accounts, which matches the 3 claims all happening on the day of the test. The third claimed account (`34b6e9317a`) has only one Reflect thread since 10-03, so it is not a candidate. It shows a separate anomaly, described in section 6.

## 4. Per account: threads, Orca's first two lines, user turns as metadata only

Normalization in the quotes below: curly apostrophes are written straight, a long dash in the model's output is written as `[dash]`, and line breaks as `/`. Masks: `[FIRST_NAME]`, `[FOCUS_AREA]`, `[COMPANION_NAME]` (the user-chosen Orca name). "Withheld" means the Orca line paraphrases what the user said, so it stays out of this report even though it is Orca's text.

### Account `225a543db2` (the re-run case)

Timeline on 2026-10-05 (UTC): claim 08:32:10, then onboarding re-completed (consents 15:33:52, survey saved 15:34:14), then thread B6 at 15:34:22.

| label | created (UTC) | status | entry_origin | modality / seed | claim before thread | msgs (user / Orca) |
|---|---|---|---|---|---|---|
| B1 | 10-03 07:52:30 | FINISHED | NULL (ordinary) | voice / none | no (feature not live yet) | 16 (8 / 7) |
| B2 | 10-03 12:09:42 | ACTIVE | NULL (ordinary) | voice / none | no | 2 (0 / 1) |
| **B3** | **10-05 08:32:10** | FINISHED | **onboarding_first_conversation** | voice / none | claimed by this thread | 22 (7 / 14) |
| B4 | 10-05 13:16:19 | FINISHED | NULL (ordinary) | voice / none | yes | 6 (2 / 3) |
| B5 | 10-05 13:17:25 | FINISHED | NULL (ordinary) | voice / none | yes | 8 (3 / 4) |
| **B6** | **10-05 15:34:22** | FINISHED | **NULL (ordinary)** | voice / none | yes | 6 (2 / 3) |

Orca's lines:

| label | Orca line 1 | Orca line 2 | question in line 1 | survey content in line 1 |
|---|---|---|---|---|
| B1 | "Hi, it's good to connect with you[dash]whatever's on your mind, I'm here to talk." | "Sure, let's do that. What's been on your mind lately?" | no | no |
| B2 | "Hi, it's good to hear your voice[dash]how are you feeling about starting today?" | (none) | yes | no |
| **B3** | "Hi, I'm [COMPANION_NAME]. You mentioned that [FOCUS_AREA] is the thing that weighs on you most. How has it shown up for you this week?" | "Hi [FIRST_NAME], nice to meet you. / If it helps, start anywhere. Maybe [FOCUS_AREA] showed up as too many tasks, or that tight feeling that follows you through the day. What did it look like for you this week?" | yes | **yes** (survey script) |
| B4 | "Hi, it's good to connect with you. I'm here when you're ready." | withheld | **no** | **no** |
| B5 | "Hi, it's good to hear from you." | "Hi there, let's take it step by step[dash]what's on your mind right now?" | **no** | **no** |
| **B6** | "Hi, glad you're here[dash]what's on your mind today?" | withheld | yes (generic) | **no** |

User turns (metadata only): in B4, B5 and B6 the first user turn arrived 4 to 10 s after Orca's line 1, and each was 0 to 31 bytes, which fits a short spoken reply.

### Account `63a0d3a464` (not a post-claim re-run)

| label | created (UTC) | status | entry_origin | modality / seed | claim before thread | msgs (user / Orca) |
|---|---|---|---|---|---|---|
| A1 | 10-03 10:05:13 | ACTIVE | NULL (ordinary) | text / prep_card | no | 5 (2 / 2) |
| A2 | 10-03 12:12:56 | ACTIVE | NULL (ordinary) | voice / between_session | no | 13 (5 / 7) |
| **A3** | **10-05 16:14:41** | FINISHED | **onboarding_first_conversation** | voice / none | claimed by this thread | 17 (8 / 8) |

| label | Orca line 1 | Orca line 2 | survey content in line 1 |
|---|---|---|---|
| A1 | withheld (text thread, the user wrote first; Orca reflects their turn, no question) | withheld | no |
| A2 | withheld (one question about the seeded between-session topic) | withheld (same question rephrased) | no (seeded topic instead) |
| **A3** | "Hi, I'm [COMPANION_NAME]. How has [FOCUS_AREA] shown up for you this week, the" (cut off) | "Hi, I'm [COMPANION_NAME]. You named [FOCUS_AREA] as the thing weighing on you most. How has it shown up for you this week?" | **yes** (survey script) |

A1 and A2 were created before the feature existed and are ordinary seeded threads, not re-runs. A3 is this account's first and only claim, and its opener is the survey script.

## 5. Survey data presence flags (state at query time, about 16:20 UTC)

| flag | `225a543db2` | `63a0d3a464` |
|---|---|---|
| `user_therapy_context.focus_areas` non-empty | **yes, 3 areas** | no (0) |
| `severity_ratings` present | **yes, 3 keys** | no |
| `user_profile.full_name` present | no | no |
| `user_profile.gender` present | no | no |
| `currently_in_therapy` present | yes | yes |
| ARTICLE9_HEALTH consent active (latest row by `granted_at`, `withdrawn_at IS NULL`) | yes (granted 2026-05-29) | yes (granted 2026-08-17) |
| `onboarding_completed` / step | true / 6 | **false / 1** |
| consents re-given (disclaimer, GDPR, age) | 2026-10-05 15:33:52 | 2026-10-05 16:18:16 |
| `user_therapy_context.updated_at` | 2026-10-05 15:34:14 | 2026-10-05 16:18:17 |
| Orca memory items (live) | 12 | 12 |

Reading it:

- `225a543db2`: the survey was saved at 15:34:14, **8 s before B6 was created**. Survey data was present when the re-run thread started, and the thread did not use it.
- `63a0d3a464`: focus areas and severities are empty **now** because onboarding was reset at 16:18:16 (`crud.reset_therapy_onboarding` clears `focus_areas` and `severity_ratings` together and sets step 1). At 16:14:51 the data was there, because Orca quoted a focus area in A3. That re-run is unfinished (step 1). When it finishes and the conversation starts, it will take the same ordinary-thread path as B6, since the claim is already taken and A3 is FINISHED.

## 6. Conclusions per account

| account | re-run got an ordinary thread (entry_origin NULL) while survey data existed? | Orca's first line a bare greeting with no survey question? |
|---|---|---|
| **`225a543db2`** | **Yes.** B6 (15:34:22) came 8 s after the re-run saved 3 focus areas, 3 severities and an active Art. 9 consent. The claim had been taken at 08:32:10 by B3 (FINISHED). B4 and B5 (13:16, 13:17) are also ordinary and post-claim, but the DB cannot show whether they came from the onboarding entry or the regular Reflect entry, because both write `entry_origin = NULL`. | **Yes, no survey content in any of the three.** B4 and B5 are bare greetings with no question, exactly as the `OPENING GREETING` block asks. B6 adds a generic "what's on your mind today?", so the model partly ignored "Ask no question", but it still mentions nothing from the survey. The same account's marked thread B3 did open with the survey script, so the script itself works. |
| `63a0d3a464` | **No re-run yet.** Its first claim at 16:14:41 produced marked thread A3, and the two older threads predate the feature. An onboarding re-run started at 16:18:16 and is at step 1, with no thread since. | No. A3 opened with the survey script (line 1 was cut off, then repeated in full). |

Other findings:

1. **Claim without a surviving marked thread: `34b6e9317a`.** Its claim was taken at 15:18:39 UTC, 28 s after onboarding completed (15:18:11). There is **no** marked thread for it and **no** Reflect thread created after 14:01:55 (that earlier thread is a text thread seeded from between_session). The thread made at claim time was therefore either hard-deleted (`DELETE /reflect/{id}` removes the row) or never created after the claim committed. The code accepts that outcome by design ("any failure after it means an ordinary thread later"). The Heroku log buffer only reaches back to 16:05:46 UTC, so the logs cannot decide between the two. The one first-conversation start in the buffer (A3, 16:14:41) logged normally. Any later onboarding re-run on this account also gets an ordinary thread.
2. **The greeting block was followed in 2 of 3 cases:** B6 asked a question despite "Ask no question". This is low priority and belongs to the prompt owner.
3. **The name source is unclear.** Line 2 of B3 greeted the user by first name at 08:32, but `user_profile.full_name` is NULL now on both accounts (and so is `gender`). `first_conversation.load_context` takes the first name only from `user_profile.full_name`. So either `full_name` was set at 08:32 and cleared later (there is no `updated_at` on `user_profile` to prove it), or the name reached the voice prompt another way, for example from the 12 live Orca memory items. Telling which would mean decrypting the prompt, which is outside the approved scope. It is worth a check by `backend-api`: if an onboarding re-run writes `full_name` or `gender` as NULL, that is a save-path bug signal of the same kind as the 2026-06-29 `age_band` finding.

## 7. Handoffs

- **Product decision, then `backend-api` (owner of `reflect.py` / `reflect_entry`):** the current behavior is the spec'd once-per-account rule (M-1). If an onboarding re-run should still open on the survey, two shapes keep M-1 intact (no second exemption):
  - (a) when `entry="onboarding_first_conversation"` falls back to an ordinary thread, seed the voice opener from the top focus area, the same way `build_voice_opening_instruction(seed)` works, instead of using `build_voice_greeting_instruction()`;
  - (b) expose the outcome in `ReflectStartResponse` (for example the effective `entry_origin`), so `flutter-mobile` can change the onboarding step's copy for an account that already had its first conversation.

  Either change needs `security-guardian` to confirm the exemption semantics are unchanged.
- **QA / testers:** the first-conversation script **cannot be re-tested on a claimed account**. Use a fresh account. Resetting `users.first_conversation_claimed_at` on a tester account is a prod UPDATE and needs explicit operator approval. It was not done.
- **Optional, `posthog-data-extractor`:** for `34b6e9317a`, check `reflect_session_started` with `entry_origin = onboarding_first_conversation` around 15:18:39 UTC, plus any thread-delete signal. That would tell whether the marked thread was deleted or never created.

## 8. Exact queries (all read-only, `:u` / `:c` bound in the dyno, never printed)

```sql
SELECT version_num FROM alembic_version;
SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=:t ORDER BY ordinal_position;
SELECT count(*) FILTER (WHERE first_conversation_claimed_at IS NOT NULL), min(first_conversation_claimed_at), max(first_conversation_claimed_at) FROM users;
SELECT count(*), count(DISTINCT user_id) FROM conversations WHERE entry_origin IS NOT NULL;
-- step 1
SELECT u.id, u.first_conversation_claimed_at, count(c.id), min(c.created_at), max(c.created_at)
FROM users u JOIN conversations c ON c.user_id = u.id
WHERE u.first_conversation_claimed_at IS NOT NULL AND c.conversation_type::text = 'REFLECT' AND c.created_at >= '2026-10-03'
GROUP BY u.id, u.first_conversation_claimed_at HAVING count(c.id) > 1 ORDER BY max(c.created_at) DESC;
-- per account (top 5)
SELECT full_name, gender::text, currently_in_therapy FROM user_profile WHERE user_id=:u;            -- presence only
SELECT focus_areas, severity_ratings, frustration_chips, created_at, updated_at FROM user_therapy_context WHERE user_id=:u;  -- counts only
SELECT granted_at, withdrawn_at FROM consent_records WHERE user_id=:u AND consent_type::text='ARTICLE9_HEALTH' ORDER BY granted_at DESC LIMIT 1;
SELECT custom_therapy_sessions FROM user_preferences WHERE user_id=:u;                             -- therapist names used only as a mask
SELECT id, created_at, status::text FROM conversations WHERE user_id=:u AND entry_origin IS NOT NULL ORDER BY created_at;
SELECT id, created_at, status::text, entry_origin, last_message_at, modality, seed_source FROM conversations
 WHERE user_id=:u AND conversation_type::text='REFLECT' AND created_at >= '2026-10-03' ORDER BY created_at ASC LIMIT 12;
SELECT count(*), count(*) FILTER (WHERE role::text='USER'), count(*) FILTER (WHERE role::text='SYSTEM'), count(*) FILTER (WHERE role::text='AGENT') FROM messages WHERE conversation_id=:c;
SELECT id, role::text, created_at, content FROM messages WHERE conversation_id=:c ORDER BY created_at ASC, id ASC LIMIT 12;
-- index 0 SYSTEM = prompt, never decrypted; USER = envelope size only; first 2 SYSTEM rows after index 0 = Orca, decrypted + masked
SELECT onboarding_completed, onboarding_step, medical_disclaimer_accepted_at, gdpr_consent_at, age_verified_at, updated_at FROM user_therapy_context WHERE user_id=:u;
SELECT count(*) FILTER (WHERE deleted_at IS NULL), count(*) FROM user_memory_items WHERE user_id=:u;
-- claimed accounts without a marked thread
SELECT u.id, u.first_conversation_claimed_at FROM users u WHERE u.first_conversation_claimed_at IS NOT NULL
 AND NOT EXISTS (SELECT 1 FROM conversations c WHERE c.user_id=u.id AND c.entry_origin IS NOT NULL) LIMIT 5;
```

Privacy note: the dyno-side mask uses the values stored *now*. Because of the 16:18 reset on `63a0d3a464` and the NULL `full_name` on `225a543db2`, a focus-area word and a first name came through unmasked in the raw dyno output. Both were redacted by hand above. The raw output files were deleted from the session scratchpad after this report was written.

## 9. Addendum (queried about 16:33 UTC): are `full_name` and `gender` saved for new users?

- **Asked by:** lead. Prompt v2 of the first voice conversation greets by first name (`user_profile.full_name`) and will use `gender` / `pronouns` for Polish grammar, and section 6 found both NULL on the two tester accounts.
- **Access and safety:** two more one-off dynos (`run.1102`, `run.6109`), same recipe and guards as above (`SET TRANSACTION READ ONLY`, 15 s timeout, rollback, no commit, no DML or DDL). Both exited on EOF, and `heroku ps` showed no one-off dyno afterwards. Output was aggregate counts only, with no ids, names or emails.
- **k-anonymity:** every weekly bucket and the "since 2026-10-01" window have fewer than 25 users, so counts are shown in 2-week buckets of 25 or more. Segments still under 25 are marked suppressed.
- **Onboarding flag:** `user_therapy_context.onboarding_completed`. "No row" means the user never reached the legal gate. The profile is only created after GDPR consent, so those users are expected to have no profile.

### 9.1 Fill counts by signup date

| signup window | users | profile row | full_name non-empty | gender | pronouns | age_band |
|---|---|---|---|---|---|---|
| 09-01 to 09-13 | 25 | 24 | 22 | 19 | 16 | 20 |
| 09-14 to 09-27 | 28 | 24 | 14 | 15 | 11 | 13 |
| 09-28 to 10-05 | 26 | 20 | 15 | 15 | 15 | 16 |
| **all since 09-01** | **79** | **68** | **51** (75% of rows) | **49** (72%) | 42 (62%) | 49 (72%) |
| since 09-01, onboarding completed | 42 | 42 | 33 (79%) | 34 (81%) | 28 (67%) | 37 (88%) |
| since 09-01, not completed or no context row | 37 | 26 | 18 | 15 | 14 | 12 |
| since 10-01 only | 20 | suppressed (n<25), same picture as the 09-28 bucket: most rows have a name and gender | | | | |
| all-time | 1912 | 1878 | 1302 (69%) | 1456 (78%) | 1339 (71%) | 119 (field added in July) |

Further cuts:

- `full_name` stored as an empty string: 0 since 09-01, 10 all-time. Those 10 are heavily over-represented in accounts whose GDPR consent timestamp is more than a day after signup, a rough proxy for an onboarding re-run (that segment has n<25, so the exact split is suppressed).
- All 11 signups since 09-01 that have no profile row are users who never reached the legal gate. That is expected, not a loss.
- By month (users, share of profile rows with a name / gender): 03: 63% / 71%, 04: 77% / 86%, 05: 79% / 84%, 06: 65% / 71%, 07: 70% / 76%, 08: 70% / 86%, 09: 78% / 70%. Nothing broke in September or October. Since July, `age_band` is roughly 70% filled for new users, so the 2026-06-29 finding (3 of 1718) is fixed for new signups.
- By email class, all-time: Apple "hide my email" accounts (n=64) have a name on only 48% of profile rows and gender on 55%, against 68% / 77% for gmail and 82% / 85% for other domains. Since 09-01 this split is under 25 for Apple, so it is suppressed.
- Duplicate or orphan rows: none (0 duplicate `user_id` in `user_profile` or `user_therapy_context`, 0 orphan profiles).

### 9.2 Value sets

- `gender` is the native PG enum `genderenum` with labels `MALE`, `FEMALE`, `OTHER`, and there is no drift. All-time distribution: MALE 722, FEMALE 701, OTHER 33, NULL 422.
- `pronouns` is a `varchar` that holds **display labels in the UI language**, not a normalized code. Values: She/Her 655, He/His 598, They/Them 35, NULL 539, plus Ona/Jej, On/Jego, Sie/Ihr, Er/Sein, Hon/Henne, Han/Hans, Hun/Henne, He/Him and he/him (each fewer than 25, 34 rows in total). Another 5 distinct values (17 rows) do not have the `x/y` shape and were not printed. There are no empty strings. For Polish grammar, `gender` is the cleaner input. `pronouns` would need a normalization map ("He/His", "He/Him", "On/Jego" and "Er/Sein" all mean masculine).

### 9.3 The two tester accounts

`user_profile` has **no audit column** (no `updated_at` and no `created_at`). Instead I timed the row's last write from the age of its Postgres `xmin` (the transaction id of the last write), bracketed by the nearest `messages.created_at` rows on either side and by the same user's `user_therapy_context` row. This gives the time of the **last** write only, not what it changed.

| | `225a543db2` | `63a0d3a464` |
|---|---|---|
| `full_name` | NULL | **empty string** (not NULL) |
| `gender` / `pronouns` / `age_band` | NULL / NULL / NULL | NULL / NULL / NULL |
| `currently_in_therapy` | present | present |
| profile row last written | **2026-10-05 about 15:34:14 UTC**: 2 transactions before the `user_therapy_context` write stamped 15:34:14, 86 transactions before the first message at 15:34:22 | **2026-10-03 between 10:07:01 and 12:09:43 UTC** |
| relation to the re-run | **written after the 08:32 named greeting, during the re-run** (consents 15:33:52, survey 15:34:14) | **not touched** by the 10-05 re-run (consents 16:18:16). A3 at 16:14 did not greet by name, which is consistent with an empty name stored since 10-03 |

`consent_records` has no GDPR rows at all, because GDPR consent lives only in the `user_therapy_context` timestamps, which a re-run overwrites. So earlier re-runs cannot be dated from the DB.

### 9.4 Reading it

1. **The first-time save works for most users.** Of the users who completed onboarding since 09-01, 79% have a name and 81% have gender, in line with the all-time rates. The roughly 20% gap cannot be split into "skipped" and "lost" from the DB. PostHog `profile_updated.updated_fields` (key present with a NULL value) can tell those apart.
2. **An onboarding re-run can wipe the profile, and both tester accounts show it.** The code path, read on 2026-10-05:
   - A re-run calls `TherapyOnboardingCubit.acceptConsent`, which runs `_flushPendingProfile`. The pending JSON was cleared after the first onboarding, so `UsersManager.flushPendingProfile` builds `Profile(fullName: <Firebase displayName>, pronouns: null, gender: null)`.
   - `POST /users/profile` then fails with a 500 UniqueViolation (the known note), and the client falls back to `PUT`.
   - The generated `Profile.toJson` always emits `full_name`, `pronouns`, `gender` and `age_band`, even when they are null. Only `currently_in_therapy` is `includeIfNull: false`.
   - The backend's `model_dump(exclude_unset=True)` keeps keys that were sent with an explicit null, so the PUT sets `gender`, `pronouns` and `age_band` to NULL and replaces `full_name` with the displayName. That is NULL or empty for email/password accounts.

   The prod fingerprint matches this exactly: on both accounts the four always-sent keys are NULL or empty and `currently_in_therapy` survived. `225a543db2` was rewritten during its re-run, after Orca had greeted it by name at 08:32. `first_conversation.load_context` reads the name only from `user_profile.full_name`, so the name was almost certainly present at 08:32.
3. **The blast radius is small so far.** Only 5 profiles all-time have `currently_in_therapy` present with `gender`, `pronouns` and `age_band` all NULL. All 5 also have no name, 2 of them are the tester accounts, and 1 signed up since 09-01. This is a lower bound, because the fingerprint only catches users who had answered the Art. 9 question (59 profiles in all).
4. **Implication for prompt v2:** expect no name for about 1 in 4 users and no gender for about 1 in 4 to 5. The prompt needs a neutral fallback in Polish. Testers who re-run onboarding will lose name and gender (and the voice greeting will look broken) until the wipe is fixed.

### 9.5 Handoffs

- **`flutter-mobile`** (`lib/api/api_managers/users_manager.dart`, `lib/api/models/users/profile.dart`): the fallback in `flushPendingProfile` when there is no pending JSON must not send null keys. Either skip it when a profile row already exists, or send only non-null fields (for example `includeIfNull: false` on the PUT path), and never send `full_name` when displayName is null or empty.
- **`backend-api`** (`app/api/v1/endpoints/users.py`):
  - On `PUT /users/profile`, decide whether an explicit null may clear `full_name`, `gender`, `pronouns` and `age_band`. The explicit-null clear for `currently_in_therapy` is deliberate (data minimisation) and should stay.
  - Make `POST /users/profile` idempotent (an upsert, or a 409 instead of a 500).
  - Consider adding `updated_at` to `user_profile` in a migration, so the next investigation does not need the `xmin` workaround.
- **`posthog-data-extractor`:** count backend `profile_updated` events with `is_first_save = false` whose `updated_fields` is exactly `[age_band, full_name, gender, pronouns]`, which is the fallback-PUT signature. Also check the two tester accounts at about 15:33 to 15:34 and 16:18 UTC on 10-05. That would size the wipe across all users, and it would also separate "skipped" from "lost" in point 1.

### 9.6 Exact queries (read-only)

```sql
SELECT column_name, udt_name FROM information_schema.columns WHERE table_schema='public' AND table_name=:t ORDER BY ordinal_position;
SELECT t.typname, e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid WHERE t.typname='genderenum' ORDER BY e.enumsortorder;
-- fill counts; {g} = week / onboarding / day / month / email class / re-run proxy, :since = 2026-09-01 | 2026-10-01 | 2026-03-01 | all-time
WITH p AS (SELECT DISTINCT ON (user_id) user_id, full_name, gender, pronouns, age_band FROM user_profile ORDER BY user_id, id DESC),
t AS (SELECT DISTINCT ON (user_id) user_id, onboarding_completed, gdpr_consent_at FROM user_therapy_context ORDER BY user_id),
base AS (SELECT u.created_at, (p.user_id IS NOT NULL) has_p, (nullif(btrim(p.full_name),'') IS NOT NULL) fn,
  (p.full_name IS NOT NULL AND btrim(p.full_name)='') fn_empty, (p.gender IS NOT NULL) g, (nullif(btrim(p.pronouns),'') IS NOT NULL) pr,
  (p.age_band IS NOT NULL) ab, CASE WHEN t.user_id IS NULL THEN 'no_utc_row' WHEN t.onboarding_completed THEN 'completed' ELSE 'not_completed' END onb,
  CASE WHEN u.email ILIKE '%@privaterelay.appleid.com' THEN 'apple_relay' WHEN u.email ILIKE '%@gmail.com' THEN 'gmail' ELSE 'other' END mail,
  (t.gdpr_consent_at > u.created_at + interval '1 day') late_consent
  FROM users u LEFT JOIN p ON p.user_id=u.id LEFT JOIN t ON t.user_id=u.id WHERE u.created_at >= :since)
SELECT {g}, count(*), count(*) FILTER (WHERE has_p), count(*) FILTER (WHERE fn), count(*) FILTER (WHERE fn_empty),
  count(*) FILTER (WHERE g), count(*) FILTER (WHERE pr), count(*) FILTER (WHERE ab) FROM base GROUP BY 1 ORDER BY 1;
SELECT coalesce(gender::text,'(null)'), count(*) FROM user_profile GROUP BY 1 ORDER BY 2 DESC;
SELECT CASE WHEN pronouns IS NULL THEN '(null)' WHEN btrim(pronouns)='' THEN '(empty)' ELSE btrim(pronouns) END, count(*)
  FROM user_profile GROUP BY 1 ORDER BY 2 DESC LIMIT 40;   -- printed only if the value matches ^[letters]{1,8}(/[letters]{1,8}){1,2}$
-- testers (:u bound in the dyno, matched by sha256 prefix among claimed accounts)
SELECT p.full_name IS NULL, btrim(p.full_name)='', p.gender IS NULL, p.pronouns IS NULL, p.age_band IS NULL, p.currently_in_therapy IS NULL, age(p.xmin)
  FROM user_profile p WHERE p.user_id=:u;
SELECT age(t.xmin), t.updated_at, t.gdpr_consent_at FROM user_therapy_context t WHERE t.user_id=:u;
SELECT m.created_at, age(m.xmin) - :a FROM messages m WHERE m.created_at >= '2026-09-15' AND age(m.xmin) > :a ORDER BY age(m.xmin) ASC LIMIT 4;   -- just before
SELECT m.created_at, age(m.xmin) - :a FROM messages m WHERE m.created_at >= '2026-09-15' AND age(m.xmin) < :a ORDER BY age(m.xmin) DESC LIMIT 4;  -- just after
SELECT consent_type::text, granted_at, withdrawn_at, source FROM consent_records WHERE user_id=:u AND granted_at >= '2026-10-03';
-- wipe fingerprint
SELECT count(*), count(*) FILTER (WHERE p.full_name IS NULL OR btrim(p.full_name)=''), count(*) FILTER (WHERE u.created_at >= '2026-09-01')
  FROM user_profile p JOIN users u ON u.id=p.user_id
 WHERE p.currently_in_therapy IS NOT NULL AND p.gender IS NULL AND p.pronouns IS NULL AND p.age_band IS NULL;
```
