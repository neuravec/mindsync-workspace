# Security review: WP-0 backend (first-week Home), pre-deploy, 2026-10-08

Auditor: security-guardian (read-only). No code, git or prod changes were made.

Scope: `git diff 0c7d275..68d62fa` on branch `feat/first-week-home` in `MindSync-wt-fw-integration` (36 files, +5207 / -195). Question: may this diff go to production on its own, before any frontend change?

Sources read:

- The whole diff, plus the new files in full: `app/services/push_copy.py`, `app/services/push_cadence.py`, `app/crud/user_activity.py`, and the guard and test lists in `app/tests/test_push_privacy_h4.py` and `app/tests/test_first_week_push_cadence.py`.
- Code around the diff: `app/tasks/notification_orchestrator_job.py` (`deliver_due_moments`, expiry), `app/services/notification_orchestrator.py` (Pass 1 to 3), `app/services/notification_observability.py`, `app/services/posthog_service.py` (person-less helper), `app/services/first_conversation.py` (`user_is_in_therapy`), `app/crud/therapy_schedule_context.py`, `app/api/v1/endpoints/moments.py`, `app/crud/notification_moment.py` (retention), `app/crud/crud.py` and `app/core/rq_scheduler_setup.py` (log cleanup), `app/services/moment_text_generator.py`.
- Client code the backend change interacts with (frontend checkout `fix/first-conversation-prep-card-arrival`): `lib/utils/notification_telemetry.dart`, `lib/main.dart` (`FirebaseShowNotificationHelper`), `lib/screens/main_page/main_page_body.dart`.
- `SPEC.md` sections 5, 7, 9, 13 and the lead scoping notes; `audit-security-design.md` (H-4, M-5); `COPY.md` section 11.

Verification run: the targeted suites on Python 3.12 / SQLite, with pytest cache and bytecode off and the test database in the scratchpad, so the worktree stayed clean: `test_push_privacy_h4.py`, `test_first_week_push_cadence.py`, `test_time_zone_wp0.py`, `test_time_zone_wp0_dst_sites.py`, `test_time_zone_wp0_pytz_attach.py`. Result: 1757 passed. I did not run the full suite (qa-testing owns that).

## Executive summary

**Verdict: GO with conditions.**

The H-4 work does what it claims. Every live push now takes its lock-screen title and body from a static, neutral allowlist in 7 locales. Every FCM message carries Android `visibility: PRIVATE`. Push text is gone from the application logs and from `notification_logs`, and a structural test blocks new raw sends. The daily cap is the single gate in front of every `create_moment` call. It touches only accounts younger than 8 days and fails closed for them. The time-zone work validates strictly, never logs the stored value, and the new `time_zone_saved` event carries a format enum only. No endpoint was added, no cross-user read is possible, there is no raw SQL and no migration.

One regression needs a decision before deploy (M-1). The new in-therapy gate on the Sunday check-in is right in itself, but it turns that type's existing per-person PostHog events into a clean "in therapy, with Art. 9 consent" flag on identified people. That conflicts with the person-less rule the 2026-10-07 prep-card review put into `posthog_service.py`. The fix is small and backend-only.

The cap's reservation look-ahead reads the therapy schedule without the Art. 9 gate (M-2). For WP-0 that is acceptable: it reads exactly what today's ungated session generators read and changes only whether a neutral push is allowed. It must move behind the same gate in the same WP-1 commit that gates the generators.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 3 (M-1 new, needs a decision before deploy; M-2 WP-1 condition; M-3 pre-existing) |
| Low | 6 |
| Info | 6 |

## Claims verified

| # | Claim | Result | Evidence |
|---|---|---|---|
| 1 | Neutral static copy for all 22 `MomentTypeEnum` values and the non-moment pushes, 7 locales | Verified | `push_copy.py:161-426`, maps `:437-472`. Tests enforce coverage, length and the word ban per locale (`test_push_privacy_h4.py:117-213`). I read every string; none names therapy, sessions, mood, symptoms, crisis, people or quotes. |
| 2 | `send_templated_push` is the single entry point | Verified for live code | Callers: `deliver_due_moments` (`notification_orchestrator_job.py:395`), recording ready (`session_recording.py:222`), and three legacy senders that are not scheduled (L-5). Only other FCM talker: the operator broadcast (`broadcast.py:61`), out of the allowlist by design. |
| 3 | Android `PRIVATE` on every FCM message | Verified | `build_fcm_message` (`notification_service.py:75-106`) is used by `send_fcm_message_v1` (`:173`) and `broadcast.py:61`. What PRIVATE does and does not hide: L-3. |
| 4 | No push title or body in logs | Verified | `notification_service.py:177-180`; `moment_text_generator.py:277-281` logs lengths only. A grep found no other log line with push or nudge text. FCM error bodies are logged but do not echo the message text. |
| 5 | `notification_logs.title` holds the template key, `body` is NULL | Verified | `notification_service.py:231-241`. Older rows keep their text until the existing 30-day purge (I-4). |
| 6 | AI copy stays on the moment row for in-app display only | Verified | Delivery resolves the template by type (`notification_orchestrator_job.py:395-400`). The row text is shown only after unlock (`main_page_body.dart:306-309`, `moment_deep_link_screen.dart:203-204`). Plaintext at rest remains: M-3. |
| 7 | `therapist_name` removed from the nudge payload | Verified | `notification_service.py:843-855`, `:928-938`. Both senders are dead code today (L-5). |
| 8 | AST guard forbids raw FCM sender calls | Verified, with gaps | `test_push_privacy_h4.py:651-717`. Gaps: L-2. |
| 9 | One-push-per-local-day cap for accounts under 8 days, with priority and displacement | Verified | `push_cadence.enforce_daily_push_cap`, called before every moment write: `moment_hooks._create` (`:147-157`), orchestrator Pass 1 (`:760`), Pass 2 (`:1080`), Pass 3 (`:1199`). `create_moment` has no other callers. Older accounts return before any query (`push_cadence.py:253-254`); an error in week 1 refuses (`:266-272`). |
| 10 | Therapy Relationship check-in only with in-therapy status and active ARTICLE9_HEALTH consent | Verified | `therapy_relationship_checkin_generator.py:151-153`, `:180-182`, `:272-283` via `first_conversation.user_is_in_therapy` (`first_conversation.py:623-641`), which requires both and answers False on any read error. Tests cover withdrawn and missing consent (`test_first_week_push_cadence.py:879-896`). |
| 11 | Summary-ready pushes skipped for new or inactive accounts | Verified | `moment_hooks._summary_ready_skip_reason`. The summary record is read by id AND `user_id`. `user_activity.py` checks existence only and logs only the surface label and user id. |
| 12 | `parse_timezone` accepts IANA and legacy offsets; 422 `invalid_time_zone` | Verified | `schemas.py:166-190`, `time_utils.py:297-379`. An unparseable stored value logs kind and length, never the value (`time_utils.py:274-288`). |
| 13 | `time_zone_saved` with property `format` only | Verified | `users.py:1345-1361`, `:1380-1381`. Values `iana` / `utc_offset`, no zone, sent only after a successful save. |
| 14 | DST and LMT fixes | Verified at the cited sites | No security impact beyond correct delivery times. |

## Critical findings

None.

## High findings

None. Checked: no new endpoint; `PUT /users/preferences` is unchanged apart from the event and still scoped to the token user; every new read filters by the token user or by the job's own user id (`get_moments_scheduled_between`, `moment_exists_with_dedup_key`, the summary record lookup, `has_user_activity_between`); no raw SQL; no migration; no new data sent to OpenAI; no crisis or tone input anywhere in the diff.

## Medium findings

### M-1 (new, decide before deploy): the in-therapy gate turns the check-in's per-person events into an in-therapy flag in PostHog

- **Severity:** Medium. This is an Art. 9 inference on an identified analytics profile. It belongs to the same class as design-audit M-5, but this diff makes it worse, and it breaks the person-less rule at `posthog_service.py:135-159` ("events whose mere existence says something about a person's health (they fire only for people in therapy ...) must not be joinable to that person").
- **Location:** the gate at `therapy_relationship_checkin_generator.py:151-153` and `:180-182`, plus the unchanged emitters that now carry it:
  - backend `moment.scheduled` with `moment_type` (`notification_orchestrator.py:1210-1216`, Pass 3);
  - backend `moment.expired` (`notification_orchestrator_job.py:216-228`) and `moment.sent` (`:441-449`);
  - `moment_type` in the FCM data payload (`notification_orchestrator_job.py:431`), which the client copies into `notification_received` and `notification_opened` (frontend `lib/utils/notification_telemetry.dart:21-45`).
- **Description:** before WP-0 the Sunday check-in reached everyone who passed the time and throttle checks (18 of 42 new accounts were not in therapy), so `moment_type: THERAPY_RELATIONSHIP_CHECKIN` on a person said little. Now it is created only for `currently_in_therapy` in {`yes_regular`, `yes_occasional`} with active Art. 9 consent. Every week each of these people gets `moment.scheduled`, then `moment.sent` or `moment.expired`, plus the client's `notification_received` / `notification_opened`, all with that type, on their identified PostHog person. That includes people in therapy who never entered a schedule, so no THERAPY_PREP event flagged them before.
- **Failure scenario:** posthog-data-extractor or growth-analyst runs a person-level breakdown of `moment.scheduled` by `moment_type` (the 2026-10-07 raw extract already used these events per person). The THERAPY_RELATIONSHIP_CHECKIN cohort is now exactly "in therapy and consented", joinable to email through `identify`, and it ends up in any export or report.
- **Remediation (backend-api; small, backend-only, no client release needed):**
  1. In `posthog_track_moment` (`notification_observability.py:75-90`), send `moment.*` person-less for a fixed set of health-revealing types: `distinct_id=personless_distinct_id()`, `properties=personless({...})`, and without `moment_id` (a per-person `moment.opened {moment_id}` from `moments.py:148` would otherwise re-join it). The minimum set is THERAPY_RELATIONSHIP_CHECKIN. Recommended: also THERAPY_PREP, POST_SESSION_REFLECTION, THERAPY_APPOINTMENT, RECORD_SESSION, BETWEEN_SESSIONS_NOTE, HOMEWORK_REMINDER, ADD_THERAPY_DATE and MOOD_DIP_ALERT, which closes design-audit M-5 for those types in the same change.
  2. In `deliver_due_moments`, leave `moment_type` out of the FCM data payload for the same set. The client already handles a missing key and then sends no property (`notification_telemetry.dart:17-24`).
  3. Tests: for those types, capture gets a non-user distinct id and `$process_person_profile: False` with no `moment_id`, and the data payload has no `moment_type`.
- **Deploy condition:** fix before deploy (preferred, about an hour of work), or the operator accepts in writing that the check-in type joins the M-5 lawyer bundle, with the fix scheduled before WP-1 ships. Funnel cost: the per-person check-in funnel goes away; aggregate counts stay in PostHog, and `notification_logs` keeps one template key per send server-side.

### M-2 (WP-1 condition, acceptable for WP-0): the cap's reservation look-ahead reads the therapy schedule without the Art. 9 gate

- **Location:** `push_cadence.py:421-483` (`_anticipated_session_rank`; reads `therapy_schedule` at `:442`, and custom sessions, frequency and anchor date at `:496-499`).
- **Ruling for WP-0: acceptable.**
  1. It reads exactly what the Pass 2 generators read today, also without the gate. THERAPY_PREP and POST_SESSION_REFLECTION have no consent check (design-audit H-3 item 4, scheduled for WP-1).
  2. Its only output is allow or refuse for a push whose text is now neutral.
  3. It writes nothing, logs no schedule value and emits no event.
  4. It runs only for accounts younger than 8 days and honours the same toggles as the generators.
  So it does not widen the processing that happens today.
- **Why it cannot stay like this:** once WP-1 makes the session generators read the schedule only through the consent-gated helper, an ungated look-ahead would keep processing a schedule after Art. 9 withdrawal (Art. 7(3)). It would also reserve days for pushes that never come, so a person who withdrew consent in week 1 would get fewer pushes on their former session days.
- **WP-1 condition (backend-api):** the look-ahead calls the same consent-gated schedule helper as THERAPY_PREP, POST_SESSION_REFLECTION and THERAPY_APPOINTMENT, in the same commit. Add a test: withdrawn consent means no reservation. The docstring at `push_cadence.py:436-440` already says this; it needs to be a test, not only a comment.

### M-3 (pre-existing, known follow-up of design M-5): AI copy is still generated from health context and stored in plaintext, and the moment purge never runs

- **Location:** `models/notification_moment.py:186-191` (`push_title`, `push_body`, plus the in-app text in the payload), `moment_text_generator.py:51-79` (prompt context: debrief highlights, mood data, a crisis-safety section), `crud/notification_moment.py:934` (`purge_old_terminal_moments`).
- **Description:** after WP-0 this text never reaches a lock screen. It is still written per user by OpenAI from health context and stored unencrypted. Because a delivered push suppresses the in-app fallback (CS-20), most AI `push_title` / `push_body` values are now never shown to anyone (processing without a use, Art. 5(1)(c)). Also new in this review: `purge_old_terminal_moments` (90-day retention) has no caller anywhere in `app/` (no scheduler entry, no task), so these rows are kept without limit.
- **Remediation (backend-api, data-analytics; not blocking WP-0, which only reduces exposure):** schedule the terminal-moment purge in `rq_scheduler_setup.py` (cheap, do it soon); stop asking the model for `push_title` / `push_body`; keep and encrypt only the in-app text that a surface actually shows; keep the item in the M-5 lawyer bundle.

## Low findings

- **L-1: the cap's log line reveals session days, and L-4 now prints more dates.** `push_cadence.py:274-282` logs user id, moment type, local date and reason at INFO for every week-1 decision. `reason=reserved_for_higher_priority day=2026-10-09` means "a session-related push is expected for this person on that date". That is the same class as the pre-existing L-4 line `users.py:1726` (`next=%s`). WP-0 widens L-4 slightly: the time-zone fix in `crud.py:1545-1552` now computes a real `next_session_date` for legacy-offset users, so that line prints a date for them too. **Owner backend-api:** log the reservation as a generic `not_eligible` (or drop `day` when the reason is a reservation), and log only the frequency in `update_therapy_schedule`.
- **L-2: the AST guard matches names only.** `test_push_privacy_h4.py:651-706` looks for calls named `send_fcm_to_all_user_tokens` / `send_fcm_message_v1` and for files that contain the literal `fcm.googleapis.com`. It misses an import alias (`import ... as _send`), `getattr`, a URL built from a setting, and `firebase_admin.messaging`. **Owner qa-testing:** also fail on any import of the raw senders outside `notification_service.py` (check `ast.ImportFrom` names and aliases), on any `firebase_admin.messaging` import, and on `messages:send` anywhere outside the two known files.
- **L-3: PRIVATE is defense in depth, not the control.** Android conceals a `PRIVATE` notification only when the user's lock-screen setting hides sensitive content; with "show all content" the text is shown. iOS has no per-message equivalent. The neutral copy is the real protection, and it holds. The client's foreground local notification (`main.dart:1170-1184`) still has no `visibility` (flutter-mobile H-4 item 4); low risk now that the text is neutral. Reword the comment at `notification_service.py:68-72` so nobody relies on PRIVATE alone.
- **L-4: Pass 1 probes the cap at one time and persists at another.** `notification_orchestrator.py:758-823`: the cap is checked at the scored winner's DND-adjusted time. If the rendered winner comes back with a different suggested time on a different local day, that day was never checked, and two pushes can land on it. Displacement also commits before render and persist, so a later persist failure leaves the day with no push. Functional, not a leak, and rare. **Owner backend-api:** re-run the cap when `winner.suggested_scheduled_at != cap_probe_raw`.
- **L-5: dead legacy senders sit outside the cap.** `notify_summary_notification` (`notification_service.py:452`), `_process_first_nudges` (`:717`) and `_process_followup_nudges` (`:875`) have no scheduler entry and do not run today. They bypass the cap and still put `route: /fab/after-therapy` and `session_date` in the data payload (`:847-849`, `:932-934`). **Owner backend-api:** delete them, or route them through `moment_hooks._create` if they are ever revived.
- **L-6: timing residual.** Neutral copy hides the content, not the rhythm. POST_SESSION_REFLECTION at session start + 75 min and THERAPY_PREP at T-24h / T-3h still form a weekly pattern that someone who often sees the phone can notice. This was accepted by design (SPEC 5). Mention it in the privacy notice next to the push description.

## Info

- **I-1: `time_zone_saved` is safe as built.** It carries only `format` (`iana` / `utc_offset`) and no zone, and it fires after a successful save. It reveals the app build's age, not health. Privacy-notice note: an IANA name such as `Europe/Warsaw` is a finer location signal than `UTC+2`. Storing it is justified for DST-correct reminders. It must stay out of PostHog and prompts, and today it does: prompts use only the schedule `summary` sentence (`first_conversation.py:986`, `therapy_schedule_context.py:185-200`), which contains no zone.
- **I-2: validation is stricter on what is stored and more tolerant of what old builds send.** Everything the old validator accepted is still accepted, so existing clients get no new 422s. The fallback log never contains the value (`time_utils.py:274-288`).
- **I-3: boot and deploy safety.** No migration, no Procfile or requirements change, and the model edits are comments only. `push_copy` imports nothing from the app; `push_cadence` imports the enum at module level and loads everything else inside its functions. A deploy is a push; no `alembic upgrade` step is needed.
- **I-4: correction to my design audit M-5.** `notification_logs` does have a 30-day purge (`crud.py:9409`, scheduled at `rq_scheduler_setup.py:420`). Rows written before this deploy, which still hold AI or static therapy text, disappear within 30 days. `notification_moments` rows keep their text with no limit (M-3).
- **I-5: H-1 (crisis cohort) is untouched.** Neither the cap nor the summary skip reads tone, a crisis flag or the recap. Their inputs are account age, activity existence, schedule and toggles. No safety or crisis message depends on a push, so a refused push in week 1 removes no safety path.
- **I-6: moment endpoints are user-scoped.** The `moment_id` in the data payload is safe to keep: `get_moment_by_id` filters by the token user (`crud/notification_moment.py:160-172`).

## Answers to the lead's focus questions

1. **Health data on the lock screen, in logs, PostHog or FCM payloads.** Lock screen: fixed. Logs: fixed for push text; schedule derivatives remain in two INFO lines (L-1). `notification_logs`: fixed. FCM title and body: fixed. FCM data payload: still carries `moment_type` (and for the dead nudge senders a therapy route), which is not shown but reaches PostHog through client telemetry (M-1, design M-5). PostHog: one regression (M-1), nothing else new.
2. **Any push path that bypasses the allowlist or PRIVATE.** None among the live paths. The operator broadcast skips the allowlist by design but gets PRIVATE. The dead legacy senders use the allowlist but skip the cap (L-5).
3. **Can the cap or the summary suppression single out therapy status or crisis (H-1)?** Crisis: no (I-5). Summary suppression: no; it depends on age and activity only and emits no per-person event. The cap: it adds no event and no property. Its visible traces (a lower-ranked moment missing on a session day, or a `moment.scheduled` that is displaced without any follow-up event) only sit next to THERAPY_PREP and POST_SESSION_REFLECTION events that already name the type per person (design M-5), so they add no new inference today. Once the session types go person-less (M-1 recommended set), a dangling `moment.scheduled` of a displaced moment becomes the only per-person trace of a session day. The SPEC 5 recommendation closes that uniformly: no per-person `moment.*` events at all for accounts younger than 8 days. That rule depends on account age, not on health, so it is not itself a flag. Put it in WP-1.
4. **Consent in the check-in and the look-ahead.** The check-in is correct and fails closed (claim 10). The look-ahead is ungated, acceptable for WP-0, and must be gated with the generators in WP-1 (M-2).
5. **`time_zone_saved`.** Acceptable (I-1).
6. **Log lines with user data.** Push text is gone. What remains: user id together with moment type, local date and reason (L-1); the pre-existing `next=` date (L-4 of the design audit); a 20-character FCM token prefix on invalid-token removal (pre-existing, not usable alone).
7. **Plaintext AI copy on moment rows (M-5).** Still there, now never on a lock screen. The purge that should bound it never runs (M-3).

## GDPR status (WP-0 scope)

| Requirement | Status | Notes |
|---|---|---|
| Right to erasure | Unchanged, pass | No new table or column. `notification_logs` and `notification_moments` cascade from `users` (`models.py:172-176`, `notification_moment.py:159-163`). |
| Data minimisation | Improved, one regression | Lock screen, logs and `notification_logs` no longer carry text; `therapist_name` left the payload. Regression: M-1. Open: M-3. |
| Consent for processing | Pass, with a WP-1 condition | Check-in now consent-gated. Look-ahead ungated like the generators (M-2). |
| Encryption at rest | Unchanged | Plaintext AI copy on moment rows (M-3). |
| Retention | Partial | `notification_logs` 30 days (I-4). `notification_moments` purge defined but never scheduled (M-3). |
| Transparency | Notes for the privacy notice | Time zone as an approximate location (I-1); push timing (L-6). |
| Right to portability | Not available | Unchanged, no export exists. |

## Horizontal privilege escalation (new or changed reads)

| Read | Scoping |
|---|---|
| `get_moments_scheduled_between` | `user_id` filter. Internal only, not reachable from a request. |
| `moment_exists_with_dedup_key` | `user_id` filter. Internal only. |
| `displace_pending_moment` | By id; ids come only from the user-filtered occupant list. Internal only. |
| `_summary_ready_skip_reason` record lookup | Record id AND `user_id`; a mismatched id gives `summary_not_found` and no push. |
| `has_user_activity_between` | Every query filters by `user_id` (directly or via the parent conversation or habit). |
| `PUT /users/preferences` | Token user only; unchanged apart from the event. |

## Pre-existing, out of scope: `.env` is tracked in the backend repository

The backend repository tracks `.env` (`git ls-files` lists it; it is also in every worktree on this machine and in the Heroku slug). I listed only the variable names and did not read any value. The names cover the Azure AD client secret and database credentials, the OpenAI, AssemblyAI and Loops API keys, the Apple shared secret, the Play Console service JSON, the PostHog personal API key, and the Firebase service-account credentials. If those values are real, anyone who can read the GitHub repository, any clone or backup of it, or any agent session that opens the file can read the production mental-health database, read every person-level PostHog event, and use the Firebase service account to send arbitrary push text to every user's device. That last point bypasses this whole H-4 allowlist. Deleting the file in a new commit does not remove it from history: only rotating each credential does. The operator should decide on rotation and on moving the values to Heroku config vars; no remediation is part of this review.

## Conditions for deploying this diff on its own

1. **M-1:** fix before deploy (preferred), or the operator's written acceptance with a fix date before WP-1 ships.
2. **qa-testing** runs the full backend suite before the push (I ran only the targeted WP-0 suites, 1757 passed).
3. **After deploy, read-only checks:** database-administrator samples new `notification_logs` rows (title is a template key, body NULL) and confirms no new row holds text; a Heroku log sample shows `[FCM] Sending` lines with type, moment id and template only; posthog-data-extractor confirms `time_zone_saved` carries only `format`.
4. **Carried into WP-1, not blocking WP-0:** M-2 (gate the look-ahead together with the session generators); the SPEC 5 plan-step rules (data payload `route: /home`, no `moment_type`, no per-person events); the recommended uniform rule of no per-person `moment.*` for accounts under 8 days (answer 3); L-1 and L-4.

No Critical or High finding is open, so this report does not block deployment once condition 1 is met.

## Remediation priority

1. **Before deploy:** M-1 (backend-api), or operator acceptance.
2. **With WP-1:** M-2, L-1, L-4 (backend-api); SPEC 5 plan-step payload and event rules.
3. **This sprint:** M-3 purge scheduling (backend-api), L-2 (qa-testing), L-3 comment and client visibility (backend-api, flutter-mobile).
4. **Backlog:** M-3 AI-copy minimisation and encryption, L-5, L-6 (privacy notice).
5. **Operator:** decision on rotating the credentials in the tracked `.env`.
