# Security and privacy design review: first week mode on Home: 2026-10-07

Auditor: security-guardian (read-only). Pre-implementation review of a DESIGN. No code exists yet, so every finding below is a requirement the SPEC must carry before any agent starts building. GDPR Art. 9 focus.

Sources read:

- Design canvas `first-week-canvas/project/`: `canvas.json` (all notes, in particular n_measure, n_push, n_plan, n_quota, n_edge, n_legal, n_build, n_decide), `Main.dc.html` (Home logic, full script), `FollowUp.dc.html`, `Push.dc.html`, `WeekOne.dc.html`, `CheckIn.dc.html`, `CheckInDone.dc.html`, `TrialDay3.dc.html`, `SessionCheck.dc.html`, `HomeCalm.dc.html`.
- Prior audits: `design-specs/2026-10-02-subscription-onboarding/audit-security.md` (H-1, M-3 and its re-verification), `design-specs/2026-10-03-first-voice-conversation/audit-security.md` (H-1 crisis to PostHog, H-2, M-1 to M-6, backfill B-H1).
- Backend code the design reuses: `app/services/orca_memory.py` (recap cache, crisis scan, memory gates), `app/services/first_conversation.py` (`user_is_in_therapy`, exemption window), `app/crud/reflect_entry.py` (`claim_first_conversation`), `app/crud/crud.py` (`reset_therapy_onboarding`), `app/api/v1/endpoints/users.py` (`PUT /users/therapy-schedule`, account deletion), `app/api/v1/endpoints/consent.py` (Art. 9 withdrawal), `app/services/notification_service.py` (FCM send), `app/services/moment_text_generator.py`, `app/services/moments/therapy_prep_generator.py`, `app/services/notification_observability.py`, `app/services/notification_orchestrator.py`, `app/tasks/notification_orchestrator_job.py`, `app/models/models.py` (`NotificationLog`), `app/models/notification_moment.py`, `app/api/v1/endpoints/audio_v2.py`.
- Frontend code the design reuses: `lib/core/analytics/posthog_service.dart` (session replay), `lib/navigation/ms_routes.dart` (`PosthogObserver`), `lib/main.dart` (notification channels and foreground display), `lib/utils/notification_telemetry.dart`, `lib/screens/wow/views/offer_step_view.dart` (calm helpline precedent), `test/support/reflect_analytics_guard.dart`, `lib/l10n/app_en.arb` (push examples, age gate).
- `analytics-reports/raw/2026-10-07-post-onboarding-home-behavior.md` (how moment events are used per person today).
- California SB 243 summaries (sources at the end). The official bill page refused automated access, so the SB 243 points are from secondary summaries and need the lawyer's confirmation.

## Executive summary

The design is privacy-aware in intent: it already removes step types and variants from analytics, keeps check-in scores out of PostHog, makes lock-screen copy neutral by default, gives the crisis path the same events as the normal path, and gates memory quotes on consent. That intent is right. But the concrete contracts do not yet deliver it, and four places would leak Art. 9 data or a crisis indicator if built as drawn:

1. **H-1: the calm (crisis) cohort is still observable.** "Same events" covers only the today card. Elements that are hidden in calm (the B/C side card, the reminder offer, "Not today"), the follow-up screen's label, the backend `moment.*` events with `moment_type`, the day-3 sheet timing, session replay layouts and route names can each single out a person who disclosed suicidal ideation, the same class as the 2026-10-03 H-1.
2. **H-2: the calm flag needs a storage design.** It must not become a plaintext column, a log line, a job result or a client cache. It must cover the model-only crisis signal that today expires after 24 h.
3. **H-3: an Art. 9 consent bypass.** Variant C includes people without Art. 9 consent. Its "Seeing a therapist? Add sessions" card writes a therapy schedule through `PUT /users/therapy-schedule`, which has no Art. 9 check. The plan then switches the person to variant A.
4. **H-4: lock-screen copy is not neutral today, and the plan reuses those generators.** Push titles and bodies are AI-written per user, the prompt allows therapy wording, the static fallback says "therapy session", and no Android visibility is set. Push text is also written to logs and to a plaintext table.

The Medium items: `has_step` combined with the day number is itself a therapy-status proxy (A vs B/C). The follow-up question needs a legal basis, storage and deletion contract. The Free-limit exemption needs a write-once anchor and a per-step ledger. The plan endpoint needs a minimisation and degradation contract. The calm trigger ignores crisis after day 0. SB 243 likely applies. Pre-existing backend moment events also put therapy status and mood dips on identified PostHog persons.

**Verdict: GO to spec with conditions.** Nothing here needs a redesign of the product idea. All four High items are design requirements that must be written into the SPEC (section "Conditions for GO" below) before implementation starts. Implementation that ships without them is a deployment block. security-guardian re-reviews the SPEC text for H-1 to H-4, then the code before deploy.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 4 |
| Medium | 7 |
| Low | 7 |
| Info | 4 |

---

## Critical findings

None. No code exists, and nothing in the design exposes one user's data to another user.

---

## High findings

### H-1: The calm (crisis) cohort can be singled out through surfaces the event contract does not cover

- **Severity:** High. Crisis indicators are rank 3 in the threat model. The 2026-10-03 H-1 set the bar: the calm branch must not be distinguishable per person in PostHog. The design's n_measure says "Wariant spokojny wysyła dokładnie to samo", but that is only true for the three today-card events. The design itself makes several elements conditional on calm.
- **Where the design differs between calm and normal (from `Main.dc.html` and `FollowUp.dc.html`):**
  1. **Side card** ("When is your next session?" / "Seeing a therapist?"): `showSideCard: branch !== 'schedule' && !calm`. Any impression event on it (the mandatory PostHog step will push implementers to add `first_week_side_card_viewed`) is absent for B/C people in calm. B/C membership is already visible from the onboarding funnel (prior M-3), so "B/C, Home viewed on day 0, no side-card impression" means calm, deterministically.
  2. **Reminder offer on day 0:** `showReminder` only in mode `day0`, never in `calm0`. If `reminder_optin_result` (or any impression) fires on view or on leaving, its absence marks calm.
  3. **"Not today"** does not exist in calm, so `today_card_deferred` can never fire on days 0 to 2. Weak alone, but it adds to the others.
  4. **Follow-up screen:** three labels (`From your first talk`, `From your setup`, `Whenever you're ready`). A `follow_up_viewed {source: recap | setup | calm}` property, or three route names, is a direct crisis flag.
  5. **Backend moment events (existing, see M-5):** `posthog_track_moment` sends `moment.scheduled`, `moment.sent` and `moment.expired` per identified person with `moment_type` (`notification_orchestrator.py:780`, `notification_orchestrator_job.py:216` and `:435`). If calm suppresses THERAPY_PREP, POST_SESSION_REFLECTION or the new plan-step type for someone who would otherwise get it, the missing `moment.scheduled` is visible. Every other suppression reason (step done, "Not today", plan hidden, two ignored, cap taken by a higher type) is itself visible in PostHog, so calm is the one unexplained gap.
  6. **Client push telemetry:** `notification_telemetry.dart:21-45` copies `moment_type` from the FCM data payload into `notification_received` and `notification_opened` when present.
  7. **Day-3 trial sheet:** n_idea says calm lasts 72 h, but the mockup ends it at `day <= 2`. With day 1 at least 12 h after onboarding, plan day 3 starts about 57 h after an evening onboarding, inside a 72 h window. If calm suppresses the sheet, "step done on day 3, no sheet" marks calm.
  8. **Session replay:** `posthog_service.dart:109-112` records every session with texts and images masked. Layout is not masked: the calm Home has no switch, an extra support row and no side card. A replay viewer can see the difference.
  9. **Route names:** `PosthogObserver` (`ms_routes.dart:302`) turns route names into `$screen`. A separate route for the calm follow-up or the calm Home would be a `$screen` crisis flag.
- **Required changes (owner flutter-mobile unless noted):**
  1. **Rule for the SPEC:** no impression event on any element whose visibility depends on tone. Elements that differ by tone may only carry user-initiated action events, with no property that encodes tone, source or branch. Concretely: no side-card impression event (a tap event without `kind` is allowed); `reminder_optin_result` fires only after an explicit toggle (on) and the OS result, never on view or leave; one follow-up event at most (for example `follow_up_started` on the first send), with no `source`, `label` or `recap` property.
  2. Same route name and the same widget keys for both tones on Home and on the follow-up. Tone is state, never a route or a route argument.
  3. The helpline link in calm reuses the `_CalmContinuation` precedent (`offer_step_view.dart:262-282`): external browser, no event, no helper that captures one.
  4. Wrap the Today card and the follow-up prompt area in `PostHogMaskWidget` for both tones, so replays show the same masked block. If that cannot hide the layout difference, exclude Home and the follow-up screen from replay for every account in its first 8 days. Do NOT turn replay off only for calm accounts, because that would itself be the flag.
  5. Calm boundary: end calm at the start of plan day 3 (04:00 local), as the mockup does, and drop "72 h" from the spec. The day-3 sheet then never sees calm. If the lead keeps a pure 72 h window, the day-3 sheet must ignore tone.
  6. Backend (backend-api): calm suppresses only the new plan-step reminder, which is opt-in and default off, and which calm people are never offered. Session reminders the person set up (THERAPY_PREP, POST_SESSION_REFLECTION, THERAPY_APPOINTMENT) keep running in neutral copy (H-4). If the lead wants calm to silence those too, `posthog_track_moment` must send nothing per person for every account younger than 8 days, uniformly. The plan-step type must never send per-person moment events: measure it in aggregate from `notification_logs`.
  7. Backend (backend-api): no `moment_type` in the FCM data payload of plan-step pushes (keeps item 6 of the description closed).
  8. Extend `test/support/reflect_analytics_guard.dart`: forbidden keys `tone`, `calm`, `variant`, `branch`, `plan_variant`, `has_step`, `step_type`, `step_key`, `step_kind`, `side_card`, `follow_up_source`, `recap_source`; forbidden values `calm`, `gentle`, `ready`/`fallback` as a follow-up source. Add a test that renders Home and the follow-up in both tones and asserts identical event names and identical property key sets.
- **Operator acceptance:** like the 2026-10-03 H-1, these are funnel gaps under the CLAUDE.md PostHog rule. The lead must list them and the operator must accept them explicitly.

### H-2: The calm flag needs a storage design that never creates a readable crisis marker

- **Severity:** High as a requirement. A plaintext crisis marker in Postgres, logs or job results was rated High in the backfill review (B-H1, per-user crisis counts in the worker log). The design asks for a 72 h flag where today only a 24 h Redis cache exists.
- **What exists:** the recap result, crisis bit included, is Fernet-encrypted in Redis for `RECAP_STORE_TTL_SECONDS = 24 * 3600` (`orca_memory.py:704`). The keyword crisis signal can be recomputed at any time from the stored turns (`thread_has_crisis_language`, `orca_memory.py:1124`), and the cached answer is already rescanned on every read (`:1651-1658`). The model-only signal (a paraphrase the keywords miss, `:1729-1736`) exists only in the cached recap and disappears after 24 h. A plan that reads only the recap would switch a model-flagged person back to the normal tone on day 1.
- **Required design (owner backend-api for storage, data-analytics for the recap write):**
  1. **Where:** a per-user Redis key that exists for EVERY account in its first week, not only for calm accounts, for example `fw:state:{uid}`. The value is Fernet-encrypted JSON (`{"tone": "standard" | "gentle", "tone_until": ...}`) with one TTL for everyone (end of plan day 2 plus a margin). Key existence then reveals nothing. Write it in the same code path as the recap, from `scanned_crisis or model_crisis`.
  2. **Never in Postgres in plaintext.** No `calm_until`, `crisis_flag` or `tone` column. database-administrator and growth-analyst run SELECTs on prod and write reports; backups outlive the 72 h. If Redis loss is a concern, the floor is the keyword rescan of the first-conversation thread (and of later threads, see M-6). It already fails toward calm for keyword crises. Accept that a Redis loss drops the model-only signal, and record that trade-off in the SPEC.
  3. **Retention:** the TTL is the retention. No copy anywhere else. Delete the key on account deletion (add it to the step 7f block in `users.py:1895`, next to the recap cache) and on deletion of the first-conversation thread (next to `forget_recap`).
  4. **Who reads it:** one helper, `first_week_tone(db, user_id) -> "standard" | "gentle"`, used only by the plan endpoint (web) and the plan-step generator (worker). No admin, broadcast, clinician-portal or export path may call it.
  5. **The plan engine must not persist tone.** If plan state is stored (deferred steps, hidden plan, rhythm), tone is not part of it. A server-side response cache, if any, must not hold tone longer than 60 s and must be encrypted.
  6. **No tone in logs, job arguments or job results.** The orchestrator logs `reason` with the user id (`notification_observability.py:40-47`). A calm skip must use the same generic reason string as other ineligibility (for example `not_eligible`). Never `calm`, `crisis` or `gentle`. RQ jobs take ids only and return counts that do not split by tone.
  7. **Client:** tone is held in memory (Cubit state) only. It is never written to SharedPreferences, never logged with Fimber, never put into an exception message. Freezed `toString` output with tone must not reach `$exception` (the sanitiser should strip state dumps).
  8. **Naming:** the response field is `tone` with values `standard` / `gentle`, never `crisis` or `calm`, so a careless log or analytics property is less obviously a crisis flag, and the guard in H-1 item 8 catches it anyway.

### H-3: Variant C can collect Art. 9 therapy data without Art. 9 consent

- **Severity:** High. Processing special-category data without the explicit consent the app itself relies on (Art. 9(2)(a)).
- **Design:** C covers "not in therapy OR no Art. 9 consent" (n_plan, n_legal: "bez zgody zawsze C"). C shows "Seeing a therapist? Add your sessions", and "Dodanie terminu przełącza na A".
- **Code fact:** `PUT /users/therapy-schedule` (`users.py:1570`) stores the schedule with no `ARTICLE9_HEALTH` check. Compare `users.py:394-401` and `:1178-1186`, where `currently_in_therapy` is silently dropped without consent. Art. 9 withdrawal (`consent.py:231-280`) clears `currently_in_therapy` but leaves the schedule. `user_is_in_therapy` (`first_conversation.py:623`) is consent-gated, but a schedule read is not.
- **Failure scenario:** a person declined the Art. 9 checkbox in onboarding. On day 2 they tap "Add sessions" on the C card and enter Thursday 17:00. The schedule is stored, the plan reads it, switches to A, sends "Before therapy" steps and session-named pushes. The person never gave explicit consent for therapy data.
- **Required changes:**
  1. flutter-mobile: the C card's "Add sessions" opens the Art. 9 consent step first, with the same wording as onboarding. Declining closes the flow and stores nothing. The B card (already consented) goes straight to the schedule.
  2. backend-api: `PUT /users/therapy-schedule` returns 403 `art9_consent_required` (or drops the schedule like the profile field) when `ARTICLE9_HEALTH` is not active. Test it.
  3. backend-api: the plan engine decides A or B only through one helper that requires active Art. 9 consent for BOTH the status and the schedule (extend `user_is_in_therapy`, or add `therapy_schedule_if_consented`). Without consent: C, and no session dates in the response.
  4. backend-api (pre-existing, same fix): THERAPY_PREP, POST_SESSION_REFLECTION and THERAPY_APPOINTMENT must not fire when Art. 9 is withdrawn. On withdrawal, consider clearing the schedule as the profile field is cleared (lead and lawyer decide, since the schedule may also serve plain calendar reminders).

### H-4: Lock-screen copy is AI-written per user, can name therapy and distress, and Android visibility is unset

- **Severity:** High. A lock screen is readable by anyone near the phone. "Your session is coming up: prepare for your therapy session" discloses therapy attendance (Art. 9) to third parties. The design reuses these generators and promises "it never shows what you talked about" (`Main.dc.html` reminder note).
- **Code facts:**
  - `moment_text_generator.py:44-70`: push title and body are generated per user ("personalised notification copy for a mental health therapy companion app"). Rule 2 allows therapy wording for therapy moments. The CRISIS SAFETY section steers copy toward distress references.
  - `therapy_prep_generator.py:446-449`: the static fallback is "Take a few minutes to prepare for your therapy session."
  - `notification_service.py:119-127`: the FCM message has no `android` block, so no `visibility`. `main.dart:1175-1184`: the foreground local notification has no `visibility` either.
  - `notification_service.py:131`: `logger.info(f"[FCM] Sending to {token[:20]}...: {title} | {body}")` writes push text to Heroku logs. `NotificationLog.title/body` (`models.py:2011-2012`) and `NotificationMoment.push_title/push_body` (`notification_moment.py:186-187`) store it in plaintext.
- **Required changes (owner backend-api, generators and FCM; flutter-mobile, client):**
  1. **Lock-screen fields come from a static, server-side allowlist** of neutral strings per moment type, in all 7 locales (the `neutral` set in `Push.dc.html` is a good base). The model never writes `push_title` or `push_body`. AI copy, if kept, goes only to `in_app_headline` / `in_app_body`, shown after unlock. This applies to every generator and every account, not only the first week, as n_push already says.
  2. **Neutral means:** no therapy, session, therapist, symptom, mood, focus-area, emotion or crisis words, no companion-memory quotes, no names. "A 2-minute step for tomorrow" passes. "Your session is tomorrow" does not.
  3. **"Details" opt-in:** a server-side per-user setting, default off, explained with a real preview, revocable. Even with details on: no memory quotes, no focus areas, no mood or symptom words, nothing crisis-related. "Your session is tomorrow" is the maximum.
  4. **Android:** `"android": {"notification": {"visibility": "PRIVATE"}}` on every FCM message, and `visibility: NotificationVisibility.private` in `AndroidNotificationDetails` for foreground display. iOS has no per-message equivalent, so neutral copy is the only protection there.
  5. **Data payload:** a generic route (`/home`) for plan-step pushes, no `moment_type`, no step kind (see H-1 item 7).
  6. **Logs and tables:** log notification type and moment id only, never title or body. Store a template key instead of text in `notification_logs`, or encrypt the columns (see M-5).
  7. Tests: every generator's push fields match the allowlist; the FCM payload carries `visibility: PRIVATE`; no log line contains a push body.

---

## Medium findings

### M-1: `has_step` together with the day number is a therapy-status proxy (A vs B/C)

- **Location:** n_measure, `today_card_viewed / tapped / deferred {has_step, days_since_signup}`; plan skeletons in n_plan and `Main.dc.html`.
- **Description:** B and C share one fixed skeleton: steps on days 1, 3, 4, 6, 7 and rest on days 2 and 5. A follows the session: prep the day before, capture on the session day, check-in on day 5, recap on day 7, so A has steps on days B/C never do and rests on days B/C always have a step. The "moves once" rule adds noise but does not remove the signal: a B/C day 4 always has the check-in, so `has_step=false` on day 4 can only be A (or a hidden plan, which has its own event). Dropping `days_since_signup` does not help, because PostHog can rebuild the day from `onboarding_completed` and the event timestamp. Inferred data counts as Art. 9 data (CJEU C-184/20, as in prior M-3).
- **Related proxies the SPEC must avoid:** a `cta` or `kind` property on the check-in mirror ("Add to session notes" vs "Talk with Orca"); a side-card `kind`; B's "Note something for therapy" built on a different feature or route than C's "Leave a voice note" (for example `betweenSessionsFlow` for B), which would separate B from C through `$screen`.
- **Required changes (flutter-mobile):** drop `has_step`. Today-card events carry no properties, or only `plan_active` (false after "Hide this plan"; does not depend on variant or tone). `days_since_signup` may stay, because it carries no variant. B and C use the same voice-note feature, screen and events; "for therapy" is copy only. The check-in mirror CTA is one event without `cta`. The variant split stays server-side, in aggregate, with groups below 10 suppressed, after the lawyer's decision, and never by tone (n_measure already says this for variants).

### M-2: The follow-up question needs a legal basis, storage, deletion and crisis contract

- **Design:** the question is generated at recap time from the first conversation, stored for up to about 7 days, quoted on day 1 ("You mentioned sleep has been rough lately..."), with a setup-based fallback and a calm variant.
- **Legal basis:** this is memory-derived personalisation of Art. 9 content kept beyond the conversation, the same processing class as Orca memory. It must use exactly the memory gate: `memory_extraction_gate(...) == allowed` at generation and `not profiling_withdrawn(...)` at display (`orca_memory.py:454-491`). Do not write a new interpretation of "PROFILING consent". If the lawyer later decides memory needs an explicit PROFILING grant, both change together. Add the follow-up to the pending privacy-policy update (memory, bio patterns, suppression hashes).
- **Source:** derive it ONLY from a memory item that was actually written. Never from the recap items: the recap runs even when memory is blocked (recap-only prompt), so a recap-derived quote kept for 7 days would bypass the memory gate and the 24 h recap retention.
- **Storage (owner backend-api for the model and migration, data-analytics for generation):** a small table, for example `first_week_follow_ups(user_id FK users ON DELETE CASCADE, memory_item_id FK user_memory_items ON DELETE CASCADE, conversation_id FK conversations ON DELETE CASCADE, question_ciphertext Text (Fernet, same key as messages), created_at, expires_at)`, String columns only, no PG enum, no ORM relationship back to User (the hero_insights nullify lesson), guarded reads that degrade to "no follow-up" before migration. A daily purge hard-deletes expired rows. Alternative: one nullable encrypted column on `conversations` plus the memory item id, excluded from the mapper (the pattern `orca_memory.py:56-59` already proposes).
- **Deletion:** the FKs give "Forget this" on the quoted item, "Forget everything", PROFILING withdrawal (which purges memory), thread deletion and account deletion. Also delete explicitly in `forget_memory_after_profiling_withdrawal` as belt and braces. Test the account-deletion ORM path. The WeekOne "Not right" button must call the existing hard-delete endpoint (`DELETE /users/memory/{id}`, which also writes the suppression hash), not a new soft hide.
- **Crisis:** (a) generate nothing when the recap says crisis, by scan or by model; (b) at display, rescan the question and the item text with `contains_crisis_language`, check tone (H-2), check every Reflect thread since the first-week anchor with `thread_has_crisis_language` (M-6), and confirm the item still exists; (c) any failed check shows the calm question with no quote.
- **Exposure:** quote only in-app on the follow-up screen. The Home card and every push, including "details", say "a question from your first talk" without quoting. Render as plain text, no linkify (stored prompt injection stays single-user, as prior L-6).
- **Day-7 recap, same rules:** "Orca noticed" comes from the summary pipeline and is not memory-gated or crisis-screened today. Screen it with the crisis guard. If the week had any crisis flag, use the quiet variant without "Orca noticed". "You mentioned" lists live memory items only.

### M-3: The Free-limit exemption needs a write-once anchor and a per-step ledger

- **Design:** first-week steps do not count toward Free limits, the day-1 conversation has its own 10-message ceiling (n_quota, decision 2). "Ponowny onboarding: plan nie startuje od nowa."
- **Abuse vectors:**
  1. Onboarding rerun or thread deletion restarting the week. The 2026-10-03 M-1 showed that "once per account" decided by live rows can be reset. `reset_therapy_onboarding` (`crud.py:782`) only resets `UserTherapyContext`, which is good, but the anchor must not live there.
  2. Variant flipping: adding, moving ("Just this once", "From now on") or removing sessions to create new exempt Before/After therapy steps. Custom sessions on several days of week 1 would create several exempt prep and capture steps.
  3. Time-zone changes moving the 04:00 day boundaries to fit an extra "day".
  4. Parallel requests (prior M-2) and delete-then-recreate (prior M-1, R-1).
  5. A client claiming "this is my first-week step".
  6. Voice: realtime key minting still has no entitlement or rate limit (prior M-6, `audio_v2.py:211`, still open).
- **Required design (backend-api):**
  1. Anchor: a write-once `users.first_week_started_at`, set by a conditional UPDATE (`WHERE first_week_started_at IS NULL`) at the first `onboarding_completed`. Never reset by Reset onboarding, thread deletion or schedule changes. Existing accounts stay NULL, so no plan and no exemption (matches n_edge v1). Do not reuse `first_conversation_claimed_at`: a skipped first conversation is claimed on day 1, which would shift the week.
  2. Window: exemptions apply only while `now < first_week_started_at + 8 days` in UTC, whatever the time zone.
  3. Ledger: `first_week_allowances(user_id FK CASCADE, step_key String(32), consumed_at, UNIQUE(user_id, step_key))`. Consume with `INSERT ... ON CONFLICT DO NOTHING RETURNING`, before the AI call. Exempt only when the insert won. Deleting the created note never refunds.
  4. Hard cap per account: Before therapy 1, After therapy 1, voice note 1, follow-up talk 10 user messages, day-6 talk 10 user messages, check-in always free (no ledger). Talk messages are counted against a server-side claim, as for the first conversation, so deleting the thread or opening a second one gains nothing.
  5. The server decides the step: the create endpoint computes "today's open step for this user" itself. No request field can mark something as a first-week step.
  6. Text only after the trial. No voice exemption until prior M-6 is fixed.
  7. Fail closed: if the anchor or ledger cannot be read (before migration, any error), count normally. "Included in your first week" copy comes from the server response for that step, never hard-coded, so a degraded backend never promises a free step and then charges it.
  8. Accepted risk, unchanged: delete account and re-register gives a new UID, a new trial and a new first week (prior I-4). Do not add device fingerprinting to close it.

### M-4: The plan endpoint needs a minimisation, scoping and degradation contract

- **Variant and session dates in the response:** acceptable. Session dates are the person's own data, already shown in the app, and gated by H-3 item 3. But do not send a `variant` label (`A/B/C`, `in_therapy`, `branch`): the client needs steps, not the label, and a label is the field most likely to leak into analytics. Send `steps[]` (`key` from a fixed enum, `date`, `state`, `exempt`, `quota_left`), `tone` (H-2), side-card key, today-card copy keys.
- **Never in the plan response:** the follow-up question text (fetched only when the follow-up screen opens), memory text, check-in scores, suppression reasons, anything about other users.
- **Auth and scoping:** `Depends(deps.get_current_user)`, no user id in path, query or body. Every read filtered by the token user. Step states come from existence and timestamps only: the endpoint decrypts no content and calls no model.
- **Writes** ("Not today", hide plan, rhythm, session moved): Pydantic with `extra="forbid"`, enum fields, and no settable `variant`, `tone`, `day`, `first_week_started_at`, `exempt` or `done`. "Done" is only ever derived from a real result (n_plan already says so).
- **Headers:** `Cache-Control: no-store` on the plan and follow-up responses. The client never persists them; offline means today's legacy Home, as n_edge says.
- **Degradation:** before migration, any new table or column read returns 503 `first_week_unavailable`, never 500, and never at import or boot (no `Enum(PyEnum)`, String plus constants; see CLAUDE.md H10). The new moment type needs `ALTER TYPE ... ADD VALUE IF NOT EXISTS` in an autocommit block, with the UPPERCASE label prod uses, and the generator must skip itself when the label is missing, rolling back its own per-user transaction. Client: any non-200 or timeout gives the legacy Home without card or plan. It never routes to onboarding or the paywall (CLAUDE.md rule 6) and never shows first-week copy.
- **Logging:** user id and counts only. No variant, tone or session date. The existing `update_therapy_schedule` log line with `next_session_date` is L-4.

### M-5 (pre-existing): Backend moment events put therapy status and mood dips on identified PostHog persons

- **Location:** `notification_orchestrator.py:780` (`moment.scheduled` with `moment_type`), `notification_orchestrator_job.py:216` (`moment.expired`) and `:435` (`moment.sent`), through `posthog_track_moment` (`notification_observability.py:75`). Types include THERAPY_PREP, POST_SESSION_REFLECTION, THERAPY_APPOINTMENT, THERAPY_RELATIONSHIP_CHECKIN and MOOD_DIP_ALERT (registered, `mood_dip_alert_generator.py:512`). The 2026-10-07 raw extract uses them per person.
- **Description:** THERAPY_PREP on a person says "has a therapy schedule". MOOD_DIP_ALERT says "the system detected a mood dip for this person": a derived health signal on an identified profile at a third-party processor. Prior audits covered client proxies (M-3, M-4), not these backend events. The push text is also logged (`notification_service.py:131`) and stored in plaintext (`NotificationLog.title/body`, no purge; `NotificationMoment.push_title/push_body`, 90 days). With AI copy and the "details" opt-in, those columns can hold therapy or distress wording.
- **Required changes (backend-api):** replace `moment_type` in per-person events with a neutral bucket (`session_related` / `engagement` / `summary`, with mood dip folded into `engagement`), or move moment analytics to server-side aggregates from `notification_logs`. Add the event mapping to the lawyer bundle with prior M-3. Remove title and body from the FCM info log. Store a template key in `notification_logs` instead of the text, and add a retention purge. Not introduced by this design, but the design's own goal "bez wzrostu wyłączeń powiadomień" can be measured from aggregates.

### M-6: Calm is triggered only by the first conversation; a crisis later in week 1 keeps the plan pushing

- **Description:** a person who discloses crisis in a Reflect thread on day 3 still gets "Your step for today is ready" pushes, step cards and the day-3 sheet. Text Reflect already flags crisis (`crisis_detected` from `contains_crisis_language`, prior L-3 fixed), and the recap or analysis scan covers voice.
- **Required change (backend-api, data-analytics):** compute tone from every Reflect thread since `first_week_started_at` (keyword rescan plus the model signal when a recap or extraction ran), with the same storage rules as H-2 and the same event neutrality as H-1. A later crisis switches the person to the gentle tone until the end of the following plan day 2 equivalent (lead to set the length), reminders stop, the follow-up quote and "Orca noticed" disappear.

### M-7: California SB 243 likely applies, and the calm path should be built to support it

- **Applicability (lawyer to confirm):** SB 243 (in force since 2026-01-01) covers a "companion chatbot": an AI system with adaptive, human-like responses that can meet a user's social needs, shows anthropomorphic features and can sustain a relationship across multiple interactions. Orca is a named companion with memory, and this design adds a feature whose whole purpose is to "pick up where you left off". That strengthens the case that MindSync is in scope for California users.
- **Duties as summarised (verify with counsel):** a protocol that prevents suicidal-ideation and self-harm content and refers users to crisis services (hotline or crisis text line) when they express suicidal ideation, published on the operator's website; clear AI disclosure where a reasonable person could think they talk to a human; a disclosure that companion chatbots may not be suitable for some minors; for users the operator knows are minors, AI disclosure, a break reminder at least every 3 hours of continuous use and measures against sexual content; annual reports to the Office of Suicide Prevention from 2027-07-01 on crisis referrals issued and the protocols, with no personal information; private right of action of at least USD 1,000 per violation.
- **What this means for the design:**
  1. The calm Home's helpline link is a good follow-on. It is not the referral the law asks for: that must happen in the conversation, at the moment of disclosure. Verify the voice path shows an on-screen referral when crisis is detected mid-call (the text path does since prior L-3).
  2. Build a server-side aggregate counter of referral notifications shown (in-chat banner, calm screen, calm Home): daily counts with no user id, not in PostHog. This supports the 2027 report without repeating the 2026-10-03 H-1.
  3. Publish the crisis protocol on mindsync.app (operator, after the lawyer).
  4. Add an explicit "Orca is an AI" line where the first conversation starts, and the minors-suitability disclosure, if counsel confirms scope.

---

## Low findings

- **L-1: Push pre-prompt examples promise non-neutral pushes.** `app_en.arb:2216-2221` ("Your session is tomorrow", "Check in on {focusAreas} today"). In-app only, so not a leak, but the consent screen shows copy that H-4 forbids, which misleads the choice. **Owner flutter-mobile**, 7 locales, already in n_fix item 6.
- **L-2: Android channel description names therapy.** `main.dart:885-899` ("Session Reminders", "Reminders to capture your therapy sessions") is visible in system settings to anyone holding the phone. **Owner flutter-mobile:** "Reminders" / "Reminders you set up in MindSync".
- **L-3: Rhythm and recurring reminders.** The day-7 rhythm creates recurring pushes (Mondays check-in, Wednesdays talk, before and after sessions). They fall under H-4 and the daily cap. `rhythm_selected` carries `count` only, never option keys ("before_after_session" is a therapy proxy). **Owner flutter-mobile, backend-api.**
- **L-4 (pre-existing): session date in logs.** `update_therapy_schedule` logs `next=%s` with the user id (`users.py`, around line 1620). **Owner backend-api:** log the frequency only.
- **L-5: Redis transport.** The tone key (H-2) and the follow-up path rely on Redis. Values are Fernet-encrypted, but confirm `REDISGREEN_URL` uses `rediss://`. **Owner integration-devops.**
- **L-6: Age gate vs age bands.** The gate is "16 or older" (`app_en.arb:82`) while age bands start at 18-24 (`schemas.py:66`). A 16- or 17-year-old must skip the band or misreport. For GDPR Art. 8 the 16 threshold works in most member states (some go to 13 to 15). For SB 243, if the operator ever "knows" a California user is a minor, the minor duties in M-7 apply. **Owner lead and lawyer:** either an 18+ gate, or a 16-17 band plus the SB 243 minor measures.
- **L-7: Check-in scores into session notes.** "Add to session notes" on the check-in mirror copies symptom scores into a note that a linked clinician can see when linking returns (prior I-8, CS-11 hidden today). The person decides, which is fine, but the confirmation should say who can see session notes. **Owner flutter-mobile.**

## Info

- **I-1: Good choices to keep:** scores never sent to PostHog; "done" only from a real result; no plan for existing accounts (no retroactive processing of history); "You mentioned" and the memory footer only with memory consent; reminders default off; one push per day; the Free card never leads straight into the paywall; step types and variants already left out of events.
- **I-2: `reminder_optin_result`, `first_week_plan_toggled`, `first_week_plan_hidden`, `first_week_recap_viewed` and `quick_checkin_completed(areas_count, skipped_count)` are acceptable as proposed,** with the H-1 rule on `reminder_optin_result` (action only).
- **I-3:** No HTTP cache or logging interceptor exists in the client (checked `pubspec.yaml`), and no crash reporter other than the PostHog `$exception` sanitiser. Keep it that way for the plan and follow-up responses.
- **I-4:** The "Not today", hidden plan and rhythm state belong to a plan-state table with `ON DELETE CASCADE`, String columns, and no tone (H-2 item 5). Data export still does not exist. When it is built, include plan state and the follow-up question.

---

## Rulings on the seven questions

1. **Analytics.** Today-card events with `has_step` and `days_since_signup` single out variant A (M-1), and several calm-dependent surfaces can single out the crisis cohort (H-1). Safe set below.
2. **Calm flag.** Redis only, one encrypted per-user first-week key for everyone, TTL to the end of plan day 2, deleted with the account and the first thread, read through one helper by the plan endpoint and the plan-step generator only. The plan engine must not persist it. Never in Postgres in plaintext, logs, job results, PostHog or client storage (H-2). Same events for calm and normal: only after the H-1 changes.
3. **Follow-up question.** Same gate as Orca memory, derived only from a written memory item, Fernet-encrypted, FK cascades to the item, thread and account, hard purge after 7 days, crisis rescan and tone check before showing, in-app only (M-2).
4. **Lock screen.** Static neutral allowlist for every generator's push fields, AI copy only in-app, details opt-in limited as in H-4, Android `visibility: PRIVATE` in FCM and local notifications, no content in logs or data payload (H-4, M-5).
5. **Plan endpoint.** Session dates acceptable, variant label not, follow-up text not, `no-store`, token-only scoping, `extra="forbid"`, 503 that degrades to the legacy Home and never to onboarding, exemption fails closed (M-4, M-3).
6. **Free-limit exemption.** Write-once `first_week_started_at`, UTC 8-day window, unique per-step ledger consumed before the AI call, per-account caps, server decides the step, text only after the trial (M-3).
7. **Other.** SB 243 likely applies: in-conversation referral, aggregate referral counter, published protocol, AI disclosure (M-7). Age gate mismatch (L-6). Consent order: the Art. 9 step must come before any therapy schedule entry from the C card (H-3). The memory notice already precedes memory. PostHog identify already follows consent. Push permission comes after the first conversation and is never offered in calm.

### Safe event set (client)

| Event | Allowed properties | Notes |
|---|---|---|
| `today_card_viewed` | none, or `plan_active` (bool) | No `has_step`. `days_since_signup` optional. Same in both tones. |
| `today_card_tapped` | none, or `plan_active` | No step kind or destination. |
| `today_card_deferred` | none | Only exists where "Not today" exists. Acceptable because it is user-initiated. |
| `first_week_plan_toggled` | `expanded` (bool) | As proposed. |
| `first_week_plan_hidden` | none | As proposed. |
| `first_week_recap_viewed` | none | No quiet/full flag. |
| `rhythm_selected` | `count` (int) | Never option keys. |
| `reminder_optin_result` | `result`: `on` / `off` / `denied_settings` | Only after an explicit user action and the OS result. |
| `quick_checkin_completed` | `areas_count`, `skipped_count` | No scores, no area names. |
| `follow_up_started` (optional) | none | No `source`, no label. |
| side card | tap event only, no `kind`, no impression | H-1. |
| helpline link | no event | H-1, precedent `offer_step_view.dart`. |
| `getting_started_card_tapped`, `fab_flow_selected` | as in the 2026-10-07 raw extract | `option` / `flow` values such as `after_therapy` are therapy proxies: put them in the lawyer bundle with prior M-3, or send a count only. |

Backend: no per-person `moment.*` events for the plan-step type. Existing types follow M-5.

---

## GDPR compliance status (design scope)

| Requirement | Status | Notes |
|---|---|---|
| Right to erasure | Conditional | Follow-up and tone deletion paths are specified in M-2 and H-2. They must be built and tested, including the account-deletion ORM path. |
| Data minimisation | Conditional | No variant label in the response, no question text in the plan, no `has_step` (M-1, M-4). |
| Right to portability | Not available | Unchanged. No export exists. |
| Consent for processing | Fail as drawn | C card writes Art. 9 data without consent (H-3). The follow-up uses the memory gate (M-2). Analytics proxies remain in the lawyer bundle (prior M-3, M-5). |
| Data encryption at rest | Conditional | Follow-up and tone Fernet-encrypted (M-2, H-2). Push text in plaintext tables (M-5). |
| Retention policy | Conditional | Tone ends with plan day 2, follow-up after 7 days with a hard purge, `notification_logs` needs a purge (M-5). |
| Transparency | Partial | The follow-up and day-7 recap join the pending privacy-policy update. Push examples must match the real copy (L-1). SB 243 disclosures (M-7). |

## Horizontal privilege escalation (planned endpoints)

| Endpoint (planned) | Requirement |
|---|---|
| `GET` first-week plan | Token user only, no parameters that name a user, no decryption, no model call, `no-store`. |
| `GET` follow-up question | Token user only. The row is selected by `user_id`, never by an id from the client. 404 alike for missing and foreign rows. |
| `POST` defer / hide / rhythm / session moved | Token user only, `extra="forbid"`, enums, no server-owned fields settable. Session moved needs active Art. 9 (H-3). |
| Create endpoints with exemption | Exemption decided server-side from the token user's ledger and anchor (M-3). |
| `PUT /users/therapy-schedule` (existing) | Already token-scoped. Add the Art. 9 check (H-3). |

## Conditions for GO (must be written into the SPEC before implementation)

1. H-1: the calm-neutral event rule, the safe event set above, same routes and keys for both tones, replay masking, calm ending at plan day 3, no per-person moment events for the plan-step type, extended analytics guard and test. Owners: flutter-mobile, backend-api. Operator accepts the funnel gaps.
2. H-2: Redis-only encrypted per-user first-week state for every first-week account, TTL, deletion hooks, one reader helper, no persistence in the plan engine, generic log reasons, no client persistence. Owners: backend-api, data-analytics, flutter-mobile.
3. H-3: Art. 9 consent step before the C card's schedule entry, consent check in `PUT /users/therapy-schedule`, consent-gated schedule reads in the plan engine and session generators. Owners: flutter-mobile, backend-api.
4. H-4: static neutral push allowlist for all generators, limited details opt-in, Android `PRIVATE` visibility in FCM and local notifications, no push text in logs, generic data payload. Owners: backend-api, flutter-mobile. This is a precondition for sending any plan-step reminder.
5. M-1 to M-4 written into the SPEC with their owners (flutter-mobile; data-analytics and backend-api; backend-api; backend-api and flutter-mobile).
6. M-6 and M-7 decided by the lead, M-7 with the lawyer, before the production store release. M-5 joins the lawyer bundle with prior M-3.
7. Before deploy: security-guardian re-reviews the code against H-1 to H-4 and M-1 to M-4. qa-testing runs the guard tests. After TestFlight: posthog-data-extractor confirms that no event from the new version carries the forbidden keys, and that calm and normal sessions show the same event names.

Low items L-1 to L-7 go to the backlog, except L-1 and L-2 which are cheap and fit the same flutter-mobile batch.

## Remediation priority list

1. **Into the SPEC now (blocking the build):** H-1, H-2, H-3, H-4.
2. **Into the SPEC now (this build):** M-1, M-2, M-3, M-4.
3. **Lead and lawyer, before the store release:** M-5, M-6, M-7, L-6.
4. **Backlog or same batch if cheap:** L-1 to L-5, L-7.

## Sources (SB 243)

- [Future of Privacy Forum: Understanding the New Wave of Chatbot Legislation: California SB 243 and Beyond](https://fpf.org/blog/understanding-the-new-wave-of-chatbot-legislation-california-sb-243-and-beyond/)
- [ETO AGORA: California SB-243 (Companion chatbots)](https://agora.eto.tech/instrument/2732)
- [CASRAI: California SB 243 Companion Chatbot Law](https://casrai.org/guides/california-sb-243-companion-chatbot-law)
- Official bill text (not machine-readable in this session, lawyer to read): leginfo.legislature.ca.gov, bill 202520260SB243.

---

## SPEC re-review 2026-10-07

Scope: `SPEC.md` (DRAFT, 2026-10-07) in this folder, sections 3.6, 3.7, 3.9, 4, 5, 6, 8 and 9, checked against H-1 to H-4, M-1 to M-4 and M-6. Read-only. SPEC.md was not edited.

### Status per condition

| ID | Status | What is missing (exact SPEC change) |
|---|---|---|
| H-1 | **FAIL (4 text gaps)** | (a) Day-3 sheet and tone are undefined. With a later flag (M-6) gentle tone can cover plan day 3, and "step done, no `trial_reminder_sheet_shown`" would mark the person. Add to 3.6 Effect: "Tone never changes whether the day-3 sheet shows; in gentle tone it shows with gentle copy and fires the same event." In section 4: "`trial_sheet_eligible` never depends on tone." (b) Section 4 `copy_key` values such as `today.talk.gentle` put tone into a second field, and the guard matches values exactly, so a logged `copy_key` slips through. Change to: "`copy_key` is tone-agnostic (`today.talk`); the client picks the gentle string from `tone`. Copy keys are never widget keys, routes, log text or event values." (c) Section 6 Replay is conditional and leaves out the recap, whose layout loses "Orca noticed" and the deltas after a flag. Replace with: "Wrap the whole first-week Home body, the follow-up screen and the day-7 recap in one `PostHogMaskWidget` for every account in its first 8 days." (d) Section 8 `session_sheet_result`: see ruling 3. |
| H-2 | PASS | Optional clarifications in 3.6: "TTL = anchor + 9 days for every account (covers week 1 plus a later gentle window)" and "a missing key is rebuilt once from a keyword rescan and rewritten; never rescanned on every request". |
| H-3 | PASS | Add to section 5 so the generator owner sees it: "`THERAPY_PREP`, `POST_SESSION_REFLECTION` and `THERAPY_APPOINTMENT` read the schedule only through the consent-gated helper (3.2)." Info for integration-devops: today's builds call `PUT /users/therapy-schedule` without a consent step, so existing users without active Art. 9 consent will get 403. Check the count on prod and handle the 403 in the client (consent step), so nobody silently loses a schedule edit. |
| H-4 | PASS | None. |
| M-1 | PASS | `has_step` gone, one `note` feature for B and C, no `cta` or side-card `kind`. |
| M-2 | PASS with 1 addition | Add to 3.9: "Quoted, setup-fallback and gentle questions start the thread with the same `seed_source` and the same start events; no event or property says which question was shown." |
| M-3 | PASS | None. |
| M-4 | PASS with 2 additions | Add to section 4: "`GET /first-week/plan` decrypts no message and calls no model; step states come from existence and timestamps; tone comes only from `first_week_tone`." Add to section 6: "The client navigates only to `cta_route` values on a fixed allowlist; anything else falls back to Home." |
| M-6 | **FAIL (1 text gap)** | 3.6 names the trigger but not where the key is written. Add: "Every crisis detection point writes `fw:state`: `POST /reflect/{id}/message` when `crisis_detected`, `/end` and `/recap` (scan or model), and the analysis extraction's crisis result. `tone_until` only moves later, never earlier." |

### Rulings on the lead's questions

1. **No reminder row in gentle tone: acceptable.** Conditions: no impression event (already in section 8), the replay mask from H-1 (c), and the row is never offered later on a day or under a condition that only formerly gentle accounts reach. Those accounts enable reminders in Settings only.
2. **`copy_key` containing "gentle": acceptable on the wire,** because `tone` is already there and the transport is the person's own TLS session. Not recommended: it doubles the places where tone can leak. Use tone-agnostic keys (H-1 (b)). If the keys stay, the guard must reject any string value containing `gentle` or `calm` as a substring.
3. **`session_sheet_result`: reduce.** The `result` values describe therapy attendance and routine (a session that did not happen, a permanent move). That is the same reasoning as prior M-3 point 3 (`frequency`, `session_count`). Use a propertyless `session_sheet_completed`, or drop the event. Read the outcome split server-side in aggregate from schedule changes and debriefs. The sheet's existence is still a therapy proxy, so it stays in the lawyer bundle with prior M-3.
4. **Muting by account age only: no privacy concern.** It is uniform, not health-derived, and it removes two therapy- or mood-named pushes from new accounts. Keep it independent of tone and variant. Residual (M-5): the in-app MOOD_DIP_ALERT still produces `moment.scheduled {moment_type: MOOD_DIP_ALERT}` on the PostHog person. Recommended, not blocking: no per-person `moment.*` events for accounts younger than 8 days.
5. **API sketch:** no M-4 violation beyond the two additions above and H-1 (a) and (b). `support_link`, `side_card`, step keys and dates on the wire are acceptable.

### Verdict

**Acceptable to hand to implementing agents once the operator decides section 12, after the text changes for H-1 (a) to (d) and M-6.** They are short edits to 3.6, 4, 6 and 8. No new design work is needed. The H-3 note for section 5 and the M-2 and M-4 additions should go in during the same edit. A re-read of the changed lines is enough. A full re-review is not needed.

**Gap-fix check 2026-10-07: PASS.** I re-read the changed lines in SPEC.md sections 3.6, 3.9, 4, 5, 6 and 8. H-1 (a) to (d), M-6, and the H-2, H-3, M-2 and M-4 additions are all present as worded above. Nothing from H-1 to H-4, M-1 to M-4 or M-6 is open. The SPEC is ready for the implementing agents once the operator decides section 12. Before deploy I still review the code. One note for QA: the new substring rule rejects any value containing "calm" or "gentle". Run it against the existing event values first, so a legitimate value is not rejected by accident.
