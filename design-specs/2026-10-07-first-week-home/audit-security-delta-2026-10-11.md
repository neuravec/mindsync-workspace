# Security review: first-week backend delta a021da9..5843db4, pre-deploy, 2026-10-11

Auditor: security-guardian (read-only). No code, git, Heroku or prod changes were made. This file is the only write.

Scope: `git diff a021da9..5843db4` on branch `feat/first-week-home` in `MindSync-wt-fw-integration` (46 files, +6224 / -317; 40 non-test files). Three merged branches: `fw/be5-reminder` (29bac2f), `fw/be6-sec` (273dfa3), `fw/be7-plan-fields` (8849d65). Question: may 5843db4 go to production, followed by `alembic upgrade head` (m317a1b2c3d4, then m318a1b2c3d4)? Test-only commits by qa-testing after 5843db4 (6bd0e3e at the time of writing) were ignored, as instructed. The migrations themselves did not change in this delta.

Baseline: `audit-security-wp1-4-backend.md` (a021da9), `audit-security-wp0-backend.md` (8eb8d3f), `audit-security-design.md` (H-1 to H-4, M-1 to M-7). Contract: `API_CONTRACT.md` sections 0, 1.2, 2, 7.3, 10, 14.1 and 14.2 (items 8, 9 and 12).

Code read in full: `services/first_week/{client_marker,reminder,free_limits}.py`, `services/moments/first_week_step_generator.py`, every changed hunk in `push_cadence.py`, `notification_orchestrator_job.py`, `notification_service.py`, `moment_hooks.py`, `crud/notification_moment.py`, `crud/guarded_columns.py`, `push_copy.py`, `notification_routes.py`, `follow_up.py`, `recap.py`, `tone.py`, `reflect_prompt.py`, `plan_engine.py`, `plan_loader.py`, `plan_service.py`, `crud/first_week.py`, `therapy_schedule_service.py`, `_first_week_http.py`, `users.py`, `main.py`, `api_error_classification.py`, `schemas/first_week.py`, `tasks/{first_week_follow_up,prep_card_auto_generate,weekly_therapy_summary}.py`. Context read outside the diff: `moment_privacy.py`, `notification_observability.py`, the Pass 3 loop in `notification_orchestrator.py`, `moments.py` endpoints, `NotificationMomentResponse`, `orca_memory._chat_completion` and memory extraction, `usage_tracking.track_usage` / `log_token_usage`, `therapy_consent.consented_schedule_inputs`, the follow-up display path, the voice and text follow-up start in `reflect.py`, account deletion step 7h.

Verification run (Python 3.12, SQLite; test DB and bytecode in the scratchpad; worktree left clean): `test_first_week_security_fixes`, `test_first_week_step_reminder`, `test_first_week_plan_fields` (316 passed); `test_first_week_push_cadence`, `test_moment_privacy`, `test_push_privacy_h4`, `test_first_week_follow_up`, `test_first_week_recap`, `test_schedule_art9_gate`, `test_prep_card_auto_generate_diagnosis`, `test_prep_card_auto_generate_posthog`, `test_cs06_payload_fixes`, `test_first_week_seams`, `test_first_week_plan_engine` (2478 passed); `test_first_week_api`, `test_first_week_api_boot`, `test_first_week_tone`, `test_therapy_consent` (258 passed). Total 3052 passed, 0 failed. I did not run the full suite (qa-testing owns that).

## Verdict

**GO with conditions** for pushing 5843db4 and running m317 then m318.

No Critical, High or Medium finding in the delta. Every previous finding the lead listed is closed as specified, except L-7 (bounded, rate limit still open) and M-2 (a configuration action that belongs to the frontend release). M-3 is fixed in code, so m317 no longer waits for an operator decision.

The delta keeps the earlier contracts: no tone, step or variant in a response beyond the contract, in a log line, in a PostHog event or in a push payload; plan-step pushes use neutral allowlist copy, carry `route: /main-page` and no `moment_type`, and keep Android `PRIVATE`; every new schedule read goes through the Art. 9 gate; no new route, no user id from the client, no horizontal escalation.

One new Low finding (D-L1): suppressing the plan-step reminder in gentle tone, which the design accepted, leaves a trace in Postgres and in INFO logs that a determined prod reader could turn into a per-person, per-day tone estimate by recomputing the plan. It does not block. One part of it (the cap reservation) has a cheap fix that also keeps a person in crisis from getting a different push in the freed slot.

| Severity | New in this delta | Previous findings still open |
|---|---|---|
| Critical | 0 | 0 |
| High | 0 | 0 |
| Medium | 0 | 2 (WP-1..4 M-2 configuration; WP-0 M-3 purge caller) |
| Low | 1 (D-L1) | WP-1..4 L-7 (partial); WP-0 L-2, L-5, L-6 |
| Info | 11 | |

## Findings table (new in this delta)

| ID | Sev | Title | Location | Failure scenario | Owner | Blocks |
|---|---|---|---|---|---|---|
| D-L1 | Low | Tone-gated plan-step reminder leaves a reconstructable trace in Postgres and INFO logs | `services/first_week/reminder.py:271-276`, `:320-329`; `services/push_cadence.py:799-831` (rank-3 reservation), `:938-1001` (delivery drop); `tasks/notification_orchestrator_job.py:412-419`; `services/moments/first_week_step_generator.py:182`; `services/notification_service.py:243`; `services/notification_orchestrator.py:1242` | A prod reader with the repository recomputes each reminder-enabled account's plan per day with the pure plan engine (plan state, reminder time, results, consented schedule and time zone are all in Postgres) and compares it with the `FIRST_WEEK_STEP` rows. After the computable reasons are ruled out (step done before the reminder time, deferred, rest, quota out, two ignored, cap rank, notifications off), an open-step day with no row, a row dropped at delivery with `cancelled_reason = not_eligible` and no explaining result or plan change, or a rank-4 push admitted on a day the reminder would have reserved, points to gentle tone on that day. | lead (accept and record), backend-api (reservation fix, WP-0 M-3 purge) | No |

Info items (no action required for this push unless noted): I-1 to I-11 below.

---

## D-L1: Tone-gated plan-step reminder leaves a reconstructable trace

- **What the code does (correct per SPEC 5 and design H-1 item 6):** the reminder is created only when the tone reads `standard`, failing closed (`reminder.py:271-276`, `tone.first_week_tone(..., on_unavailable="gentle")`). It is re-checked at delivery and dropped when the tone turned gentle in between (`push_cadence.delivery_decision`, `:938-1001`; the job retires it PENDING to EXPIRED with `cancelled_reason = "not_eligible"`, `notification_orchestrator_job.py:412-419`). The cap reserves the day for an expected reminder only when the same rules, tone included, say it will be sent (`_plan_step_expected_on`, `push_cadence.py:799-831`).
- **What is uniform (good):** every skip logs the same `[PLAN_STEP] user=%s outcome=not_eligible` line (`reminder.py:140-142`) whatever the reason, on rest days and done days too; every drop stores the same `not_eligible` reason as the week-1 mute drops; no `moment.*` event for this type is per person (`moment_privacy`, plan-step type in the health-revealing set); the FCM payload has no `moment_type`; the template key never reaches a log (`log_safe_template_key`).
- **What is not:** the existence of a `FIRST_WEEK_STEP` row (and its `notification_logs` row) on a day, an EXPIRED drop within the hour after creation, and a rank-4 push being refused or admitted on a reminder day all depend on tone. The INFO lines `[ORCH] user=... selected=FIRST_WEEK_STEP` and `[PLAN_STEP] user=... outcome=not_eligible` carry the same information as the rows. `notification_moments` has no purge (WP-0 M-3 still open), so the rows stay.
- **Why Low and not Medium (documented reasoning):** the trace exists only for accounts that opted in to the reminder (default off; calm accounts are never offered it on day 0) and whose tone turned gentle afterwards (design M-6 later crisis). Reading it needs a full plan recomputation per account and day from at least six tables plus the engine code, and every other suppression reason must be excluded, several of which (step done earlier in the day, deferred, quota out) are themselves only visible by the same recomputation. Compare WP-1..4 H-1 (one `length()` filter, rated High) and M-1 (one join over `token_usage_log` for every new signup, rated Medium). The design (H-1 item 6) explicitly accepted tone suppressing this reminder; it considered PostHog only.
- **Remediation:**
  1. backend-api: in `_plan_step_expected_on`, evaluate the reservation WITHOUT rule 5 (tone): reserve the day whenever reminders are on, the plan is active, the step is open at the reminder time and the last two were not ignored. The rank-4 refusal then no longer depends on tone, and a person in crisis keeps a quiet day instead of receiving a STREAK_CELEBRATION, ACHIEVEMENT_UNLOCK, DAILY_CHECK_IN or similar push in the slot the reminder left. Generation and delivery keep the tone gate. Test: same `DailyCapDecision` for a rank-4 push in both tones.
  2. backend-api: schedule `purge_old_terminal_moments` (WP-0 M-3). That bounds the row trace to the 90-day retention.
  3. lead: record the acceptance next to SPEC 5 and in the lawyer bundle, and add one rule to the `database-administrator` and `growth-analyst` agent definitions: never recompute first-week plans or tone per person from prod; plan-step reminders are analysed in aggregate only, groups below 10 suppressed.
- **Timeline:** this sprint. Not blocking.

---

## Fix verification table (every previous finding)

### WP-1..4 audit (a021da9)

| ID | Finding | Fix in the delta | Verified | Status |
|---|---|---|---|---|
| H-1 | Calm follow-up question recoverable from ciphertext length | One mapping `_FIXED_QUESTIONS`; `_GENERIC_QUESTIONS` and `_CALM_QUESTIONS` are the same object (`follow_up.py:191-203`); `_generic` and `_calm` return byte-identical strings | The two cases are the same string in all 7 languages, so stored message, preview and message 0 have equal lengths by construction; `TestStoredThreadIsTheSameForGenericAndCalm` (7 languages, text and voice) passes. Residual: quoted vs fixed stays distinguishable, accepted in the previous report as noise (crisis mixed with no memory item, gate says no, skipped first talk, `talk2`) | **Closed** |
| M-1 | Model-call traces split by the crisis flag | Follow-up model call with `user_id=None` (`follow_up.py:614`); recap "noticed" inside `track_usage(..., user_id=None)` (`recap.py:989`); `stored 1 follow-up` at DEBUG (`crud/first_week.py:939`); store failure and recap generation failure at DEBUG | `_chat_completion` passes `user_id_override=None` and opens its own context with None in the worker thread, so `log_token_usage` writes NULL (`orca_memory.py:623-641`, `usage_tracking.py:214`); the recap pipeline takes no user id; job INFO lines identical for crisis and non-crisis (tests `test_the_job_logs_the_same_lines_for_a_crisis_account`, `..._for_a_flagged_week`, `..._usage_row_without_the_user`). Residual: the `first_week_follow_ups` row (7 days, the feature itself) and memory extraction (I-7) | **Closed** as specified |
| M-2 | Art. 9 gate on `PUT /users/therapy-schedule` off by default | No code change; contract 14.2 item 8 now records the default (gate nobody until the operator sets the minimum version), so contract and code agree | `config.py:291-292` unchanged; neither variable is in `.env.example` | **Open** (configuration). Condition for the consent-step frontend build, not for this push |
| M-3 | m317 revives the hourly AUTO prep-card cron without the Art. 9 gate | `consented_schedule_inputs(db, user, prefs=prefs)` before any schedule computation or model call; skip without consent; skipped dates honoured (`prep_card_auto_generate.py:141-148`, `:171-185`) | Counts only in the DONE line (`skipped_no_consent=%d`), no per-user line; tests `TestAutoPrepCardNeedsArt9` (never consented, withdrawn, just-this-once skip) pass | **Closed**. m317 needs no further operator decision |
| L-1 | Log lines that encode the variant or a missed session | Drop and side-card dismiss log one neutral DEBUG line (`plan_service.py:544`, `:568`); schedule change and PUT refusal at DEBUG (`therapy_schedule_service.py`, `users.py`) | `TestNeutralLogLines` passes. Remaining first-week INFO lines: started, deferred, undid a deferral, hid the plan, rhythm count, reminder changed, recap served, job finished. Only "deferred today's step" is a weak standard-tone marker on days 0 to 2 (I-8) | **Closed** |
| L-2 | Per-person `api_error` on the schedule routes | PUT 403 `art9_consent_required` sent person-less (`api_error_classification.py:78-89`, `main.py:261`); the change route answers every error itself and sends only a person-less 500 (`_first_week_http.py:109-159`) | Exact match on route template, status and detail; `TestPersonlessClassification`, `test_booted_app_api_error_and_no_store` pass. Residual: the PUT's 400 and body-422 errors still go per person (pre-existing, I-9) | **Closed** for the cases named |
| L-3 | Quoted question copied into the stored system prompt | Text OPENING TURN is the constant `FOLLOW_UP_TEXT_OPENING_NOTE` (`reflect_prompt.py:421`, `:448`); `build_stored_prompt` always builds in text mode | Message 0 is identical for every follow-up thread whatever the question; the voice prompt with the question is built per session and not stored (`reflect.py:2196-2251`); tests `TestStoredPromptCarriesNoQuestion` pass | **Closed** |
| L-4 | `step_moves` kept forever | `prune_step_moves` (`crud/first_week.py:782`) run by the existing daily 04:40 UTC purge job; retention `STEP_MOVES_RETENTION_DAYS` = 28 + 7 + 1 = 36 days (`plan_loader.py:73`) | Keyset batches, conditional `UPDATE ... WHERE step_moves = :old` (a person's own write wins), `updated_at` untouched, counts-only log, Postgres compile test, "pruning never changes a plan" test. The new prep-drop writes a future `after` record; it is kept until its own date plus 36 days | **Closed** |
| L-5 | No `no-store` on framework errors of the change route; 422 echoes the body | `ScheduleChangeRoute` via `route_class_override` (`users.py:1941-1947`); FastAPI keeps the route class through both `include_router` levels | Auth 401/403, handler 403/422/503, body 422 (`_plain_errors`: loc, msg, type only, no input), unexpected 500 (class and innermost file:line logged, never the message, which could hold session dates) all carry `no-store`; booted-app test passes | **Closed** |
| L-6 | Recap job re-enqueued on `high` after uncounted failures | Every non-done outcome is counted, the 15-minute marker is kept until TTL after a failure, `_claim_pending` refuses at `MAX_GENERATION_FAILURES = 3` (`recap.py:364-383`, `:1000-1035`) | Neither the request path nor the hourly sweep queues again after the cap; tests pass | **Closed** |
| L-7 | No rate limit; follow-up GET decrypts and scans up to 50 threads | `DISPLAY_SCAN_MAX_THREADS = 20`; the scan runs only on the quoted `talk` path after the cheaper checks pass (`follow_up.py:827-845`, `:886-899`) | Over the cap the fixed question is served (fail closed) | **Mitigated**. Per-user rate limit still absent (pre-existing, backlog, integration-devops and backend-api) |
| L-8 | Processing before a consumer exists; first weekly card suppressed for old builds | First-week client marker gates the memory-write follow-up trigger (`follow_up.py:658-665`), the hourly recap sweep (`recap.py:1165-1184`, `:1221`), the first calendar-week card suppression (`weekly_therapy_summary.py:387`), the ADD_THERAPY_DATE mute and the first WEEKLY_SUMMARY_READY mute (`push_cadence.py`) | Old builds never call `GET /first-week/plan`, so they never get the marker; every marker failure falls back to the old behaviour. Left for old builds: the anchor and the tone key (Redis, keyword scan, no model call), and the seven always-muted types (a product choice that sends fewer pushes, no privacy concern) | **Closed** |
| I-4 | Follow-up claim key not deleted on account deletion | Unchanged; the delta adds `fw:followup:req:{uid}` (`follow_up.py:688-737`, value "1", TTL 1 h), same class | No content | Accepted (I-5 below) |
| I-10 | No data export | Unchanged | | Open (pre-existing) |
| I-12 | Redis TLS for `REDISGREEN_URL` unverified | Unchanged; the marker adds one more dependency | | Open (integration-devops) |

### WP-0 audit (8eb8d3f) leftovers

| ID | Finding | Status after this delta |
|---|---|---|
| M-3 | AI copy in plaintext; `purge_old_terminal_moments` has no caller | **Open.** Still no caller (`crud/notification_moment.py:1041`). Plan-step rows now add to the table and to D-L1. Schedule it this sprint (backend-api). |
| L-2 | AST guard matches names only | **Open** (qa-testing). Not touched in this delta. |
| L-5 | Dead legacy senders outside the cap | **Partially addressed.** `notify_summary_notification` now asks the week-1 gate (`notification_service.py:474-481`) but still bypasses the daily cap; `_process_first_nudges` and `_process_followup_nudges` unchanged. `periodic_summary.py` still references the summary sender; it has no scheduler entry. |
| L-6 | Timing residual, privacy notice | **Open** (operator). Add the plan-step reminder (daily, at the person's chosen time, neutral copy) to the notice text. |
| Pre-existing | `.env` tracked in the backend repository | **Unchanged** (`git ls-files` still lists it; I did not open it). Operator decision on rotation stands. |

---

## Answers to the lead's checks

1. **H-1 / H-2 / H-3 / H-4 / M-1 across the delta.**
   - Responses: the plan adds `today.session_date`, `rhythm.available[].free_limits` and `rhythm.on_free` only. No variant label, no tone beyond `tone` and `support_link`. `PlanResult.drop_refs` is `repr=False` and never serialised.
   - Logs: the reminder logs user id plus `not_eligible` only; `ReminderSettings` and `DueReminder` keep time zone, time, state, dedup key and template key out of `repr`; FCM send logs `template=plan_step` for every step family; drop logs `moment id, user, outcome=not_eligible`; exceptions are logged by class. Pre-existing lines that print exception text are I-10.
   - Events: no new identified PostHog event in the delta. `moment.scheduled`, `moment.sent`, `moment.expired` and the opened, dismissed and acted events for `FIRST_WEEK_STEP` are person-less (`moment_privacy.is_health_revealing_moment_type`); a dropped moment emits nothing; a week-1 muted type is refused before it is written, so nothing downstream runs; the in-app-only MOOD_DIP_ALERT emits no `moment.sent`.
   - Push payloads: plan-step data is `{type, moment_id, deep_link_route: /main-page, route: /main-page}`, no `moment_type`, no step. Copy comes from the allowlist (`push_copy.py:166-213`, neutral in all 7 languages, no therapy, session or mood words). Android `visibility: PRIVATE` is set on every message (`notification_service.py:78`, `:105`).
   - Tone storage (H-2): still only the padded, encrypted Redis key. Readers are the plan service, the follow-up display and the reminder module (generator, cap look-ahead and delivery check); no admin, broadcast, clinician or export path calls it.
2. **The client marker** (`fw:client:{uid}`, value `"1"`, TTL 21 days, refreshed at most daily).
   - Content: no tone, step, variant or health fact; it says the build has the first-week Home.
   - Cross-user: written only from `GET /first-week/plan` with the token uid (`plan_service.py:352-388`, after the response); no endpoint reads or returns it; a crafted request can only mark the caller.
   - Failure modes: every Redis problem reads as "no marker" (`client_marker.py:165-180`), which gives the old-build behaviour: pushes are not muted (neutral copy anyway), the first weekly card is not suppressed, and no follow-up generation or recap sweep runs (less processing). Nothing raises into a request or job; logs carry user id and exception class only.
   - Deletion: `forget_first_week_client` in account deletion step 7h (`users.py:2213-2223`); on a Redis outage it expires within 21 days, like the other first-week keys.
   - Export: not needed for portability (a technical flag, not data the person provided). List it in the Art. 15 / records-of-processing inventory next to the other first-week Redis keys (I-1).
3. **Mute and reminder paths, "ignored" detection.** No per-person `moment.*` event for `FIRST_WEEK_STEP` on any path (point 1). "Ignored" reads only existing data: `sent_at`, `opened_at`, `acted_at`, `push_delivered` of the person's own plan-step rows (`crud/notification_moment.py:324-353`), the plan state's `updated_at` and `recap_opened_at`, and the existing result-timestamp statements (`first_week_reads.get_result_instants`), all filtered by user id, no content decrypted. A failed read fails closed (no reminder). The mute list is independent of tone and variant, so it adds no tone channel; the reminder's own tone gate is D-L1.
4. **`session_date`.** Set only in the `today` and `quota_out` branches for `prep` and `after` (`plan_engine.py:1167-1186`, `:1439`, `:1449`), which are exactly the cards whose `links` already show the session sheet; `None` everywhere else. The key is always serialised (`Optional[date]` with no default, no `exclude_none` on the first-week routers). It reveals nothing the card's `step`, `copy_key` and `links` do not already reveal, and design M-4 accepted session dates in the plan response. It appears in no log line (grep over `services/first_week`, the first-week endpoints, `therapy_schedule_service.py` and the schemas finds no logging of `session_date`, `session_at` or `replaces_date`). Client condition in "Conditions" item 5.
5. **Consent gating of every new schedule read.** Reminder eligibility, the cap look-ahead and the delivery re-check all compute the plan through `plan_loader.load_plan`, which reads status and schedule only via `therapy_schedule_if_consented` (`plan_loader.py:231-253`); `prep` and `after` get no plan-step reminder at all. The prep drop and its `after` ref come from the same gated plan; without consent there is no prep step and the route answers 409. `session_date` comes from the gated slot's `session_at`. The change route's new local biweekly anchor (`therapy_schedule_service.py:259-272`) runs inside a route that is always Art. 9 gated. The AUTO prep-card cron is now gated (M-3).
6. **Auth and horizontal escalation.** No new route. `POST /users/therapy-schedule/change` keeps `Depends(deps.get_current_user)`; the route class catches the auth `HTTPException` and answers it with `no-store`, never a 200. `POST /first-week/today/drop` still takes an empty `extra="forbid"` body; the refs are computed server-side from the caller's plan. `GET /moments/upcoming` now excludes `FIRST_WEEK_STEP` by text comparison (safe before m318); `GET /moments/{id}` can return the caller's own plan-step moment (owner-scoped, neutral copy, no `scoring_signals`). The reminder account list (`get_reminder_enabled_user_ids`) is a server-side filter only.
7. **Open items.** See the two verification tables. M-2 stays a configuration condition for the frontend; L-8 is closed by the marker; WP-0 M-3, L-2, L-5 and L-6 remain open.

## Horizontal privilege escalation (changed behaviour)

| Route / read | Scoping | Result |
|---|---|---|
| `GET /first-week/plan` (marker write, follow-up request, `session_date`, rhythm limits) | Token uid only; background task uses `loaded.user_id` | Pass |
| `POST /first-week/today/drop` (prep plus its after) | Token uid; row lock on the caller's plan state; refs from the caller's gated plan | Pass |
| `POST /users/therapy-schedule/change` (new route class, local biweekly anchor) | Token uid; `FOR UPDATE` on the caller's preferences | Pass |
| `GET /moments/upcoming`, `GET /moments/{id}` | `user_id` filter unchanged; plan-step type excluded from the in-app channel | Pass |
| Plan-step generator, cap look-ahead, delivery check | Per-user reads filtered by the moment's or account's user id | Pass |

## GDPR status (delta)

| Requirement | Status | Notes |
|---|---|---|
| Right to erasure | Pass | Marker deleted in step 7h; plan-step moments and `notification_logs` rows cascade with the user (FK `ON DELETE CASCADE`); `fw:followup:req` holds no content and lives 1 h (I-5). |
| Data minimisation | Improved | H-1, M-1, L-3, L-4, L-8 closed. Open: D-L1, I-7. |
| Consent for processing | Improved | M-3 closed; every new schedule read is gated. Open: M-2 configuration. |
| Retention | Improved | `step_moves` 36 days. Open: moment purge (WP-0 M-3), `notification_logs` and `token_usage_log` have no purge. |
| Right to portability | Not available | Unchanged (pre-existing). |
| Transparency | Notes | Privacy notice: plan-step reminders and their timing (WP-0 L-6), the follow-up question and the day-7 observation (previous report). |

## Info

- **I-1:** The marker is personal data of the most technical kind (client capability). Add `fw:client`, `fw:followup:req`, `fw:state`, `fw:recap*` and the follow-up claim to the records-of-processing inventory with their TTLs.
- **I-2:** `notification_logs.title` and `scoring_signals.push_template_key` keep the step family per person (`plan_step_note` and `plan_step_talk2` occur only in B and C plans). This is the aggregate measurement source the design asked for (H-1 item 6, H-4 item 6), and A versus B/C is already derivable from the stored schedule and consent rows. It falls under the existing lack of a `notification_logs` purge (design M-5).
- **I-3:** The plan-step lock-screen copy differs by step family ("Your step for today is ready", "A 1-minute step is ready", "30 seconds for you"). None of it names therapy, sessions or mood, so a bystander learns nothing.
- **I-4:** In gentle tone the reminder is not sent and, today, the reserved slot goes to the next rank-4 push. Fix 1 of D-L1 also keeps that day quiet for a person in crisis; this is a UX decision for the lead as well as a privacy fix.
- **I-5:** `fw:followup:req:{uid}` is not deleted on account deletion (value "1", TTL 1 h). Same class as the accepted WP-1..4 I-4.
- **I-6:** The follow-up display reads tone with the default fallback (`standard`) while the reminder fails closed. On a Redis outage a model-only crisis signal is lost for the quote decision; the keyword rescans still run. This is the trade-off design H-2 item 2 accepted. Unchanged by the delta.
- **I-7:** Memory extraction still writes `token_usage_log` with the user id on the non-crisis path and skips the call on a keyword crisis (`orca_memory.py:2689-2730`). Pre-existing, M-1 class; the previous report suggested fixing it in the same change. Backlog for data-analytics.
- **I-8:** `[FirstWeek] user %s deferred today's step` (`plan_service.py:481`, pre-existing) can appear on days 0 to 2 only when the client showed "Not today", which calm Home does not. Weak, positive-only standard-tone marker (design H-1 item 3 class). Moving it to DEBUG would cost nothing.
- **I-9:** `PUT /users/therapy-schedule` 400 (bad weekday or time, `users.py:1771-1786`) and its body-422 still send `api_error` with the person's id: "tried to save a therapy schedule". Pre-existing and rare; extending `PERSONLESS_API_ERRORS` to every status of `/api/v1/users/therapy-schedule` would close it.
- **I-10:** Two pre-existing `[PUSH_CAP]` warnings print the exception text (`push_cadence.py:593`, `:633`). A SQLAlchemy error string can carry bound parameters, for example a THERAPY_PREP dedup key that holds a session date. Log the class name only, as the new code does.
- **I-11:** The recap job's INFO outcome `failed` comes almost only from the model path, which flagged weeks never reach, so a `failed` line is a positive non-crisis hint. Failures are rare and capped at 3. Acceptable; noted for completeness.

## Conditions for this deploy

1. **qa-testing** runs the full backend suite on the commit that is actually pushed (5843db4 plus its test-only commits). I ran 18 targeted suites: 3052 passed, 0 failed.
2. **Deploy equals migrate:** run `heroku run alembic upgrade head` (m317, then m318) right after the push. M-3 is fixed in this code, so m317 needs no further operator decision. The gap before m318 is safe: the plan-step generator skips itself with one INFO line per run, the in-app exclusion compares text (no enum literal bound), and no `FIRST_WEEK_STEP` row can exist before the label does.
3. **Read-only checks afterwards:** `alembic current` is m318a1b2c3d4; the `[PLAN_STEP] plan-step reminders skipped this run` line stops after the migration; no 500 on `GET /moments/upcoming`; the next hourly `[AUTO-GEN] ... DONE` line carries `skipped_no_consent=`; no 500 on `POST /users/therapy-schedule/change`; `GET /first-week/plan` for an old account returns 204.
4. **Before the frontend build with the consent step reaches TestFlight (M-2):** the operator sets `ART9_SCHEDULE_GATE_MIN_APP_VERSION` to that build's version (or `ART9_SCHEDULE_GATE_ALL_CLIENTS=true`); integration-devops adds both variables to `.env.example`.
5. **For the frontend release (flutter-mobile):** `session_date` never goes into a PostHog event, a log line or persisted storage (add `session_date` and `replaces_date` to the forbidden keys of `reflect_analytics_guard.dart`); the plan-step push's `moment_id` must not be attached to an identified event that would re-join the person-less `moment.*` stream.
6. **This sprint, not blocking:** D-L1 fixes 1 and 2 (backend-api), D-L1 item 3 (lead), WP-0 M-3 purge scheduling (backend-api), I-8 and I-10 (backend-api).

No Critical and no High finding. This report does not block pushing 5843db4 or running m317 and m318.

## Remediation priority

1. **Now (this push):** nothing blocking.
2. **Before the consent-step frontend build:** M-2 configuration (operator, integration-devops); frontend condition 5 (flutter-mobile).
3. **This sprint:** D-L1 reservation fix and moment purge (backend-api); D-L1 acceptance and agent rule (lead); I-8, I-9, I-10 (backend-api).
4. **Backlog:** L-7 rate limit (integration-devops, backend-api); I-7 memory-extraction usage rows (data-analytics); WP-0 L-2 (qa-testing) and L-5 (backend-api); data export; Redis TLS check (integration-devops).
5. **Lead or lawyer:** D-L1 acceptance, WP-0 L-6 privacy notice, `.env` rotation decision (operator).
