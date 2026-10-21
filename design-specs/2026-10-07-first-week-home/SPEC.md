# First-week Home: implementation spec (APPROVED FOR BUILD 2026-10-08, see section 13)

Status: APPROVED FOR BUILD on 2026-10-08. **Section 13 holds the operator decisions and overrides every earlier section where they differ.** Earlier status: DRAFT. Waiting for operator decisions (section 12). security-guardian re-reviewed this text on 2026-10-07 (H-2, H-3, H-4, M-1 to M-4 PASS; the H-1 and M-6 text gaps it listed are closed in this version, see the "SPEC re-review" section of `audit-security-design.md`).

- Design canvas (v4): https://claude.ai/artifact/BXroyzGRcFpcDKp6bhXxq9 (boards `Main.dc.html` and importers for Home, plus step screens; Polish rationale notes on the canvas).
- Security design review: `audit-security-design.md` in this folder (GO to spec with conditions H-1 to H-4).
- Evidence: `analytics-reports/2026-10-03-retencja-subskrypcje-priorytety.md`, `analytics-reports/raw/2026-10-07-post-onboarding-home-behavior.md`, `competitive-reports/2026-10-03-research-retencja-konwersja.md`. Prod DB aggregates script ready but not run: `db-reports/2026-10-07-first-week-design-aggregates.py`.
- Copy in the mockups is the direction. brand-voice-manager finalises English copy; all 7 locales.

## 0. Ground rules

1. CLAUDE.md "Change Safety and Impact Recon" applies to every package. Backend push to main deploys immediately; migrations are manual. Frontend push to dev ships to TestFlight. No push without operator approval.
2. Typography: never U+2014 or U+2013 in any user-facing string or doc. Rewrite the sentence.
3. Feature names are fixed: "Before therapy", "After therapy", "Between Sessions", "Reflect", "Mood & symptom trends", "Weekly therapy summary", "Therapy Relationship", "Character".
4. Tests in the same task. PostHog coverage table (section 8) is part of done.
5. Use `MsColors` / `MsStyles` tokens and existing widgets. Body text 16, touch targets 48, sentence case labels.

## 1. Goal and success measures

New accounts land on Home after onboarding (first conversation, recap, offer, reminders pre-prompt) and see a cluttered Home built around therapy sessions, with nothing that continues the first conversation. Return in days 1-7 is about 30% (9 of 30, Sep 1 to Oct 6), fewer than 5 of 32 are active on 3 separate days in week 1, and 71% do not come back from day 4 (end of the 4-day trial).

Goal: a Home that always shows one small, honest next step, starting with a first week built from the person's onboarding answers and first conversation.

Measures (before/after cohorts; about 20 genuine signups a week is too few for an A/B test; split the Google Play "new wave" traffic from 2026-09-20 out of every read):
- return in days 1-7: from about 30% to 40%;
- people active on 3 or more separate days in week 1: up;
- notification disable rate: not up.

## 2. Scope

In: accounts whose first `onboarding_completed` happens after release (they get `users.first_week_started_at`, section 3.1).
Out (v1): existing accounts (anchor stays NULL: no plan, no exemption, Home unchanged), onboarding reruns (never restart the plan), web.

## 3. Plan engine (backend-api; data-analytics for the follow-up and recap content)

### 3.1 Anchor and days

- `users.first_week_started_at`: nullable timestamp, write-once via conditional UPDATE `WHERE first_week_started_at IS NULL` at the first `onboarding_completed`. Never reset by Reset onboarding, thread deletion or schedule edits. Do not reuse `first_conversation_claimed_at`.
- Plan day index: number of local 04:00 boundaries crossed since the anchor, in the user's IANA time zone. Day 0 is the onboarding day. The day-1 reminder never fires earlier than 12 hours after the anchor.
- Examples: onboarding Mon 19:00, day 1 = Tue, reminder Tue 19:00. Mon 23:30, day 1 = Tue. Tue 01:30 is still Monday's plan day; day 1 = Tue from 04:00; the day-0 card says "After some sleep" instead of "Tomorrow".
- Prerequisite: time zones stored as IANA names. Today the app sends `UTC+2` and `pytz` falls back to UTC in schedule endpoints; negative offsets are saved wrongly by `settings_cubit.dart:459-466`. Fix in package WP-0.
- Week 1 = plan days 0 to 7. From plan day 8 the plan comes from the rhythm (3.5).

### 3.2 Variant (never sent to the client as a label)

Decided only through one helper that requires active `ARTICLE9_HEALTH` consent for both therapy status and schedule (extend `user_is_in_therapy` or add `therapy_schedule_if_consented`).

- A: in therapy (`yes_regular` / `yes_occasional`), consent active, a session falls on plan days 1 to 6.
- B: in therapy, consent active, no session in days 1 to 6 (no schedule, or biweekly off-week).
- C: everything else (not in therapy, unknown, no consent).
- Adding a session (consent required, H-3) recomputes the plan; B or C may become A.

### 3.3 Steps

Step keys (fixed enum, String column, never a PG enum): `talk`, `talk2`, `prep`, `after`, `note`, `checkin`, `recap`.

| Variant | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Day 6 | Day 7 |
|---|---|---|---|---|---|---|---|
| A (session on day S) | `talk` | `prep` on S-1 | `after` on S | | `checkin` (first free day from 5) | | `recap` |
| B and C | `talk` | rest | `note` | `checkin` | rest | `talk2` | `recap` |

Rules:
- One step per day. Priority when two compete for a day: session steps, then `talk`, then `checkin`. If the session is on day 1, `prep` moves to the morning of day 1 and `talk` moves to day 2.
- B and C use the same feature, screen and route for `note` (Between Sessions voice note); B's title "Note something for therapy" is copy only.
- If the first conversation was skipped, `talk` becomes "Your first talk with Orca" and day 0 does not claim it happened.
- Day 0 has no step.

States: `done`, `today`, `upcoming`, `deferred`, `dropped`, `quota_out`.
- `done` only from a real result: `talk`/`talk2` a Reflect thread with at least one user message on that step's day; `prep` a prep card; `after` a debrief; `note` a between-session note; `checkin` at least one new symptom score; `recap` the recap endpoint was opened. Never from elapsed time.
- An undone step moves once to the next free day, then is dropped silently. No "missed" wording anywhere.
- "Not today": `deferred`, no reminder that day, card shows "Okay, it'll wait" with Undo. Counts as the one move.
- "Hide this plan": plan card and plan reminders stop; the Today card stays with an open "Talk with Orca". Same for "I'll find my own way" on the recap.
- "Session moved?" (on `prep`) and "It didn't happen" (on `after`) open the session sheet: dated chips for the next 8 days, "Just this once" or "From now on", "Not sure yet". "Just this once" must not overwrite the recurring schedule (MSV3.11 lesson: a PUT once wiped schedules). "It didn't happen" drops `after` and keeps the schedule.

### 3.4 Side cards

- B: "When is your next session?" with "Add session time" (consent is already active).
- C: "Seeing a therapist?" with "Add sessions", which opens the Art. 9 consent step first when consent is not active. Declining stores nothing (H-3).
- Both dismissable; dismissal stored server-side in plan state. Visible in both tones.

### 3.5 Rhythm (plan day 8 onward)

Chosen on the recap. Options with Free limits shown next to each switch; 1 or 2 preselected:
- A: "Before and after each session" (on; "On Free: 1 of each a month; other weeks, add points to your agenda"), "Quick check-in on Mondays" (on; always free), "A talk with Orca on Wednesdays" (off; writing free up to 15 messages a month).
- B and C: "Quick check-in on Mondays" (on), "A talk with Orca on Wednesdays" (on), "A voice note on Fridays" (off; 3 a month on Free).
If the recap is never opened, the preselected options apply from day 9. "Change my rhythm" reopens the list.

### 3.6 Tone (calm variant)

- Trigger: crisis in the first conversation (keyword scan or model signal) or in any Reflect thread since the anchor (M-6).
- Duration: from the flag until the start (04:00 local) of the plan day 3 days later; for a day-0 flag that is the start of plan day 3.
- Storage (H-2): one Fernet-encrypted Redis key per first-week account, for every first-week account, e.g. `fw:state:{uid}`, value `{"tone": "standard"|"gentle", "tone_until": ...}`, TTL = anchor + 9 days for every account. Deleted on account deletion and on deletion of the first-conversation thread. Read only through `first_week_tone(db, user_id)` by the plan endpoint and the plan-step generator. Never in Postgres, logs, RQ args or results, PostHog, or client storage. A missing key is rebuilt once from a keyword rescan and rewritten, never rescanned on every request. Redis loss: the model-only signal may be lost (accepted trade-off).
- Writers (M-6): every crisis detection point writes `fw:state`: `POST /reflect/{id}/message` when `crisis_detected`, `/end` and `/recap` (scan or model), and the analysis extraction's crisis result. `tone_until` only ever moves later.
- Effect: same plan, same cards, same routes, same widget keys, same events. Gentle copy (chosen on the client from `tone`), a helpline link in the card's link slot (external browser, no event), no plan-step reminders, no reminder offer on day 0 (matches today's calm screen; formerly gentle accounts are never shown the offer later by a rule only they reach, they enable reminders in Settings), follow-up without quote, no "Orca noticed" and no deltas in the recap if any flag occurred in the week. Session steps stay, with gentle copy. Session reminders the person set up keep running in neutral copy.
- Tone never changes whether the day-3 trial sheet shows; in gentle tone it shows with gentle copy and fires the same event.

### 3.7 Free-limit exemption (decision 2; M-3)

- Window: `now < first_week_started_at + 8 days` in UTC.
- Ledger: `first_week_allowances(user_id FK users ON DELETE CASCADE, step_key String(32), consumed_at, UNIQUE(user_id, step_key))`, consumed with `INSERT ... ON CONFLICT DO NOTHING RETURNING` before any AI call; deleting the created item never refunds.
- Caps per account: Before therapy 1, After therapy 1, voice note 1, `talk` 10 user messages, `talk2` 10 user messages (server-side claim, as for the first conversation), check-in always free.
- The server decides whether a create request is today's first-week step. No request field can claim it.
- Text only after the trial (voice minting is still ungated, prior M-6).
- Fail closed: if anchor or ledger cannot be read, count normally. "Included in your first week" copy comes from the server response for that step only.

### 3.8 Quota-aware Today card (plan day 8 onward, Free only)

- One use left: chip "1 free this month".
- None left, never straight into the paywall:
  - `prep`: "Add to my agenda" (Workspace agenda, free) + line "Before therapy: 0 of 1 left until {reset date}" + "See Premium".
  - `after`: "Save a takeaway" to the agenda, then an optional check-in + line "After therapy: 0 of 1 left until {date}".
  - `talk`/`talk2`: title "Talks resume {date}", CTA "Quick check-in" + line "Reflect messages: 0 of 15 left until {date}".
- Data from the existing `GET /users/usage`. Missing usage data: no chip, normal card.

### 3.9 Follow-up question (M-2; data-analytics generates, backend-api stores)

- Gate: exactly the memory gate (`memory_extraction_gate(...) == allowed` at generation, `not profiling_withdrawn(...)` at display).
- Source: only a memory item that was actually written from the first conversation. Never from recap items. Without a memory item: the setup fallback ("Stress was the strongest of the things you picked. What has it been like since?").
- Storage: `first_week_follow_ups(user_id FK CASCADE, memory_item_id FK user_memory_items CASCADE, conversation_id FK conversations CASCADE, question_ciphertext Text Fernet, created_at, expires_at)`, String columns, no ORM back-relationship to User, daily purge after 7 days; also deleted in `forget_memory_after_profiling_withdrawal`. Reads degrade to "no follow-up" before migration.
- Crisis: generate nothing when the recap flags crisis. At display rescan question and item with `contains_crisis_language`, check tone, rescan Reflect threads since the anchor, confirm the item exists. Any failure: calm question, no quote.
- Exposure: quoted only inside the follow-up screen. Home and pushes say "a question from your first talk". Plain text, no linkify.
- Reflect: new `seed_source = "first_week_followup"` on `POST /reflect/start`; the opening question is persisted as Orca's first message (like the first conversation), voice composes it live. Quoted, setup-fallback and gentle questions all start the thread with the same `seed_source` and the same start events.

### 3.10 Day-7 recap

- Signup-anchored window (anchor to day 7), built on `gather_weekly_summary_data` + `assemble_weekly_summary_sections`. Suppress the first calendar-week "Weekly summary ready" card and push for accounts younger than 8 days.
- Sections: What you did (done steps only), Where things are (setup value next to the latest check-in, numbers only, no bars, no verdicts; areas left at the untouched default 5 in onboarding show "Not set"), Orca noticed (crisis-screened; hidden if any flag in the week), You mentioned (live memory items only, with "Not right" calling `DELETE /users/memory/{id}`; hidden without memory consent), rhythm (3.5).
- Quiet week variant: only what happened, no empty sections, one optional rhythm suggestion.

## 4. API (backend-api; contract verified by integration-devops before frontend work)

All endpoints: `Depends(deps.get_current_user)`, no user id in path, query or body, Pydantic v2 with `extra="forbid"`, enum fields, `Cache-Control: no-store`. Before migration any new table read returns 503 `first_week_unavailable`, never 500, never at import or boot (String columns, no `Enum(PyEnum)`).

- `GET /api/v1/first-week/plan`
  - 204 when the account has no anchor or the plan is hidden and no rhythm exists.
  - 200 body (shape, names final in the contract review):
    ```json
    {
      "plan_day": 3,
      "tone": "standard",
      "today": {
        "step": "note",
        "state": "today",
        "copy_key": "today.note",
        "cta_route": "/fab/between-sessions",
        "links": ["session_moved"],
        "support_link": false,
        "exempt": true,
        "quota": null
      },
      "steps": [{"step": "talk", "date": "2026-10-08", "state": "done"}],
      "side_card": "add_session_time",
      "reminder": {"state": "off", "time": "19:00"},
      "trial_sheet_eligible": false
    }
    ```
  - Never in the response: a variant label, the follow-up text, memory text, scores, suppression reasons.
  - `copy_key` is tone-agnostic (`today.talk`, `today.note`); the client picks the gentle string from `tone`. Copy keys are never widget keys, routes, log text or event values.
  - `trial_sheet_eligible` never depends on tone.
  - The endpoint decrypts no message and calls no model; tone comes only from `first_week_tone`.
- `GET /api/v1/first-week/follow-up`: `{ "question": "...", "quoted": true }` or 404 (missing and foreign alike). `no-store`.
- `POST /api/v1/first-week/today/defer`, `POST /api/v1/first-week/plan/hide`, `POST /api/v1/first-week/side-card/dismiss`, `PUT /api/v1/first-week/rhythm` (`{"options": ["checkin_monday", ...], "time": "19:00"}`), `PUT /api/v1/first-week/reminder` (`{"enabled": true, "time": "19:00"}`). No settable `variant`, `tone`, `day`, `done`, `exempt` or anchor.
- `PUT /users/therapy-schedule` (existing): 403 `art9_consent_required` without active consent; add "just this once" support (one-off custom session) without touching the recurring schedule. Impact (integration-devops): current builds edit schedules with no consent step, so existing users without Art. 9 consent will start getting 403. Count them on prod first (database-administrator), and ship the client handling (403 opens the consent step) in the same release.
- Logging: user id and counts only.

## 5. Notifications (backend-api)

Owner of the daily cap: one function every pass and hook calls before creating a push.

- At most 1 push per user per local day across all generators.
- Priority when several compete: 1) `POST_SESSION_REFLECTION` (start + 75 min); 2) `THERAPY_PREP` at the person's chosen time the day before (the T-3h variant only when the session is on plan day 1); 3) the new plan-step type at the chosen time; 4) everything else.
- Muted for accounts younger than 8 days: `MOOD_UPDATE_REQUEST`, `RE_ENGAGEMENT`, `ACCOUNT_SETUP_NUDGE`, `REFLECTION_INVITATION`, `THERAPY_RELATIONSHIP_CHECKIN`, `GOALS_WEEKLY`, first `WEEKLY_SUMMARY_READY`, `MONTHLY_SUMMARY_READY`, `ADD_THERAPY_DATE` (the B side card replaces it), `MOOD_DIP_ALERT` push (in-app only).
- Plan-step reminder: new `MomentTypeEnum` value via `ALTER TYPE ... ADD VALUE IF NOT EXISTS` in an autocommit block with the UPPERCASE label prod uses; the generator skips itself if the label is missing. Sent only if the reminder is enabled, today's step is open, not deferred, plan not hidden, tone standard, and the last two plan reminders were not ignored. A skip logs the generic reason `not_eligible`.
- Copy (H-4), for every generator and every account, not only week 1: a static server-side allowlist of neutral title/body per type in 7 locales, e.g. "Your step for today is ready" / "About 3 minutes, whenever suits you"; "A 2-minute step for tomorrow"; "30 seconds for you". No therapy, session, therapist, symptom, mood, focus area, emotion or crisis words, no memory quotes, no names. AI copy only in-app. "Details on lock screen": server-side setting, default off, real preview; even then nothing beyond "Your session is tomorrow".
- Android `visibility: PRIVATE` in every FCM message and in local `AndroidNotificationDetails`. Data payload for plan steps: generic route `/home`, no `moment_type`, no step.
- Never log push title or body (`notification_service.py:131`); store a template key in `notification_logs`.
- No per-person `moment.*` PostHog events for the plan-step type; measure from `notification_logs` in aggregate. Recommended (not blocking): no per-person `moment.*` events at all for accounts younger than 8 days (an in-app MOOD_DIP_ALERT still sends `moment.scheduled` with `moment_type` today, M-5).
- `THERAPY_PREP`, `POST_SESSION_REFLECTION` and `THERAPY_APPOINTMENT` read the schedule only through the consent-gated helper (3.2).
- Muting by account age is independent of tone and variant.

## 6. Frontend (flutter-mobile)

Home (`lib/screens/main_tab/`), using the existing conditional-card pattern in `_buildCards`:
- Order in first-week mode: hero (greeting, subtitle without topics), Today card, plan card, trial bar (shipped style, below the plan), side card (B/C), "More when you're ready" (Mood & symptom trends, Habits). Hidden in first-week mode: GettingStartedCard, next-session card (session steps replace it), TherapyRelationshipPromptCard.
- Today card states: day-0 done ("You're set for today", next step, reminder row when OS permission is undecided; "Notifications are off for MindSync" + "Open Settings" when denied; none in gentle tone), today (dark card, duration eyebrow, CTA, "Not today", link slot for "Session moved?" / "It didn't happen" / helpline), waiting, done, rest, quota_out. Tone is Cubit state in memory only; same widget keys for both tones.
- Plan card: collapsed by default (done chips, one "Next" line, hidden on day 0 and in done state), "See the week" expands (static rows: done, today, upcoming; no counter, no progress bar), "Hide this plan" at the bottom; expanded state remembered locally (not tone).
- Loading: card skeleton. Non-200, timeout or offline: legacy Home without card and plan; never onboarding, paywall or first-week copy.
- Replay: wrap the whole first-week Home body, the follow-up screen and the day-7 recap in one `PostHogMaskWidget` for every account in its first 8 days.
- Navigation: the client navigates only to `cta_route` values on a fixed allowlist; anything else falls back to Home.

Screens:
- Quick check-in: areas picked in setup, top 3 by setup intensity (+ "Also rate {area}" for the rest), 1-10 as a 5x2 grid of 48 px buttons with 8 px gaps, no preselected value, "Barely there" / "Overwhelming" labels, per-area Skip; saves one score per rated area via `POST /api/v1/symptoms/{id}/scores`.
- Mirror: setup value next to today, numbers only, no bars, no verdict words; "Not set" for untouched defaults; next-step card: A "Bring this to your next session?" (adds to session notes, with a line saying who can see session notes, L-7), B/C "Talk with Orca"; one event without a `cta` property.
- Follow-up (Reflect): label, question, hint; voice and "Write instead" during trial; after trial "Write to Orca" primary, "Talk by voice" with Premium badge; memory footer only when the question is quoted. Same route for every source and tone.
- Session sheet: entry from `after` ("Did your session happen today?") or from `prep` ("When is your next session?").
- Day-3 trial sheet (`trial_reminder_sheet.dart`): shown only after today's step is done (or on the next open on a rest day), never to starter or premium buyers, no starter offer (the post-onboarding offer stays one-time), copy "Your first week continues on Free." / "After tomorrow, talking with Orca by voice is part of Premium. Writing stays on Free, up to 15 messages a month."
- Recap (day 7) and rhythm list.
- Reminder opt-in on day 0 uses `FcmPushPermissionGateway`: toggle on triggers the OS prompt (iOS still undetermined after "Not now"); denied leads to `openAppSettings`.

## 7. Independent fixes (WP-0, can ship before the decisions)

1. "Add a check-in" on GettingStartedCard opens Workspace, where no check-in exists.
2. Recap "Saved to your Timeline" is false; change the copy (or save a summary card).
3. Recap "{orca} will check in on this later in the week" has no backing; remove until the follow-up ships.
4. Mood trend: hardcoded Polish placeholder rows and a dead link to a removed Settings section.
5. Em dash in the Home subtitle "No session this week ... catch your thoughts".
6. Push pre-prompt examples name focus areas and sessions (`app_en.arb:2216-2221`); Android channel description names therapy (`main.dart:885-899`).
7. `THERAPY_RELATIONSHIP_CHECKIN` reaches people not in therapy (18 of 42 new accounts in week 1).
8. Monthly and weekly "summary ready" pushes reach new and inactive accounts.
9. No shared daily push cap.
10. Time zones `UTC+2` instead of IANA; negative offsets saved wrongly.
11. Missing events `getting_started_card_tapped` and `fab_flow_selected` (send counts or neutral values only; `after_therapy` as a value is a therapy proxy, see audit).
12. Push text written by AI per user, "therapy session" fallback copy, no Android `PRIVATE`, push text in logs (H-4).

## 8. PostHog coverage (client; safe set from the audit)

Rule (H-1): no impression event on any element whose visibility depends on tone; tone-dependent elements carry only user-initiated action events with no property that encodes tone, source, step or branch.

| Surface | User action | Event | Properties | Where |
|---|---|---|---|---|
| Today card | sees it | `today_card_viewed` | none, or `plan_active` | main_tab Today card |
| Today card | taps CTA | `today_card_tapped` | none, or `plan_active` | Today card |
| Today card | "Not today" | `today_card_deferred` | none | Today card |
| Plan card | expand / collapse | `first_week_plan_toggled` | `expanded` | plan card |
| Plan card | hide plan | `first_week_plan_hidden` | none | plan card |
| Side card | taps CTA | `side_card_tapped` | none | side card |
| Side card | dismiss | `side_card_dismissed` | none | side card |
| Reminder row | toggles on, OS result | `reminder_optin_result` | `result`: on / off / denied_settings | day-0 card (only after an explicit toggle) |
| Quick check-in | saves | `quick_checkin_completed` | `areas_count`, `skipped_count` | check-in screen |
| Mirror | taps next step | `checkin_next_step_tapped` | none | mirror |
| Follow-up | first message sent | `follow_up_started` | none | follow-up screen |
| Session sheet | completes the sheet | `session_sheet_completed` | none (outcome split only server-side, in aggregate) | session sheet (exists only with a session: lawyer bundle with prior M-3) |
| Day-3 trial sheet | shown | existing `trial_reminder_sheet_shown` | as today | same in both tones |
| Recap | opens | `first_week_recap_viewed` | none | recap |
| Recap | keeps rhythm | `rhythm_selected` | `count` | recap |
| Recap | "Not right" | existing memory delete event | as today | recap |
| Helpline link | taps | no event | none | gentle tone only |

Step completion is measured by existing feature events. Backend: no per-person events for the plan-step reminder. Extend `test/support/reflect_analytics_guard.dart` with forbidden keys `tone`, `calm`, `variant`, `branch`, `plan_variant`, `has_step`, `step_type`, `step_key`, `step_kind`, `side_card`, `follow_up_source`, `recap_source`, and any string value containing `calm` or `gentle`; add a test that renders Home, the follow-up and the recap in both tones and asserts identical event names and property key sets. qa-testing first runs the extended guard against all existing event values, so no legitimate value containing those substrings is rejected by accident. After TestFlight, posthog-data-extractor confirms no new event carries forbidden keys. Operator accepts these funnel gaps (decision 5).

## 9. Security conditions (from the audit; must hold before build and deploy)

- H-1 analytics neutrality (sections 3.6, 6, 8).
- H-2 tone storage (3.6).
- H-3 Art. 9 before any schedule write from the C card; 403 in `PUT /users/therapy-schedule`; consent-gated schedule reads in the plan and in session generators (3.2, 3.4, 4).
- H-4 neutral push allowlist, Android PRIVATE, no push text in logs (5). Precondition for sending any plan-step reminder.
- M-2 follow-up (3.9), M-3 exemption (3.7), M-4 endpoint contract (4), M-6 later crisis (3.6).
- M-5 and M-7 (SB 243), L-6 (age gate 16+ vs bands from 18): lawyer before store release.
- Before deploy: security-guardian reviews the code against H-1 to H-4 and M-1 to M-4; qa-testing runs the guard tests.

## 10. Work packages and order

1. WP-0 independent fixes (section 7): flutter-mobile, backend-api, data-analytics. Includes the shared daily cap, neutral push allowlist, Android PRIVATE and IANA time zones.
2. WP-1 backend: anchor + migration, plan endpoint, plan state table (`ON DELETE CASCADE`, String columns, no tone), tone helper, Art. 9 gate on schedule, exemption ledger, plan-step moment type + mute list. Deploy with `alembic upgrade head` immediately after push; boot must survive the gap.
3. WP-2 frontend: Home first-week mode, Today card, plan card, side cards, reminder opt-in, session sheet, day-3 sheet changes, guard tests.
4. WP-3: follow-up question (data-analytics + backend-api) and follow-up screen (flutter-mobile).
5. WP-4: quick check-in, mirror, day-7 recap, rhythm.
6. Reviews: integration-devops contract check before WP-2; security-guardian before deploy; qa-testing before every push; ui-ux-designer on the built screens; brand-voice-manager on copy.

## 11. Edge cases (summary)

First conversation skipped; OS permission denied; plan hidden; starter or premium from day 0 (no trial bar, chips or day-3 sheet); existing users (no plan); onboarding rerun (no restart); offline / 503 (legacy Home); late-night onboarding; session on day 1; biweekly; crisis later in week 1; recap never opened; quota out on each limited step.

## 12. Operator decisions (recommendations in brackets)

1. First-week mode on Home with a permanent Today card. [yes]
2. First-week steps outside Free limits with the caps in 3.7. [yes; otherwise copy shows the live counter]
3. The 2-week starter stays one-time, post-onboarding only. [yes]
4. Follow-up question only from a saved memory item; setup fallback otherwise. [yes, after the lawyer]
5. Accept the reduced analytics (actions only, no step properties). [yes]
6. Order: WP-0 first, then WP-1 and WP-2, then WP-3, then WP-4. [yes]
7. Run the prod aggregates script after `heroku login` to size A, B and C. [yes]

## 13. Operator decisions, 2026-10-08 (binding; they override sections 0 to 12)

1. **First-week mode on Home with a permanent Today card: YES.** Sections 3, 4 and 6 stand.
2. **NO first-week exemption from Free limits.** The 4-day trial is Premium, so there are no limits while it runs. After the trial the account is on Free with exactly the same limits every Free account has in the app today. Consequences:
   - Drop section 3.7 entirely: no `first_week_allowances` table, no ledger, no caps, no "server decides the step is exempt" logic.
   - Drop `today.exempt` from the API and the "Included in your first week" copy everywhere (FollowUp locked state, any chip).
   - Section 3.8 (quota-aware Today card) applies **whenever the account is on Free** (trial ended, no premium, no active starter), including plan days 4 to 7, not only from plan day 8. Same rule: never straight into the paywall; free alternative + "0 of N left until {date}" + "See Premium". Data from the existing `GET /users/usage`; the numbers shown are the real Free limits read from the app/backend, never hardcoded in copy.
   - Day-3 sheet copy ("Your first week continues on Free. After tomorrow, talking with Orca by voice is part of Premium. Writing stays on Free, up to N messages a month.") stays, with N taken from the real Free limit.
3. **The day-3 trial sheet shows the post-onboarding offer again** (the same offer the person saw after onboarding, the 2-week starter), instead of "no starter offer". Overrides section 6 ("no starter offer") and decision 12.3. Shown once, on the day-3 sheet only; never to people who already bought the starter or Premium; only if the store still lets this account redeem that offer (if not eligible, the sheet shows the regular "Keep Premium" path). Same `trial_reminder_sheet_shown` event, plus the existing paywall/offer events with the existing `trigger_feature` convention (a new `trigger_feature` value for this entry point, e.g. `trial_day3_sheet`).
4. **Follow-up question on day 1 comes from memory, always.** The consent people give covers using memory across the whole app, so there is no lawyer gate and no feature flag. Rules:
   - If the person had the onboarding first conversation and a memory item was written from it: the question is generated from that memory item (section 3.9 storage, crisis and exposure rules stay).
   - If the person skipped the first conversation, or no memory item came out of it, or the existing technical guards (`memory_extraction_gate`, `profiling_withdrawn`) say no: a **generic question** that quotes nothing and is not built from setup answers (brand-voice-manager writes it, e.g. "How have the last few days been?"). This replaces the "setup fallback" in sections 3.9 and 6 and the `fallback` state on the FollowUp board.
   - Crisis handling unchanged: calm question, no quote.
5. **Reduced analytics accepted: YES** (sections 3.6, 8 and H-1 stand).
6. **Order: YES.** WP-0 first, then WP-1 + WP-2, then WP-3, then WP-4. WP-0 may ship as its own release.
7. **Prod aggregates: YES**, after the operator runs `heroku login`.
8. **Art. 9 gate on `PUT /users/therapy-schedule` (H-3): YES, sized first.** database-administrator counts accounts that edit a schedule without active ARTICLE9_HEALTH consent (last 30 and 90 days). If the number is small, the 403 applies to every client; if not, the 403 applies only to app builds that ship the consent step (version check), and old builds keep today's behaviour until they age out. The lead picks the branch from the numbers and records it here.

Delivery: the operator approved carrying this through to TestFlight (push to `dev`) and the production backend (push to `main` + `alembic upgrade head`). The lead still reports to the operator right before every push and every prod migration.

Lead scoping notes (2026-10-08):
- The "at most 1 push per local day" cap (section 5) applies to accounts in their first 8 days. Older accounts keep the Cadence v3 slots; changing their cadence is out of scope.
- The neutral static push allowlist (H-4) applies to every generator and every account, as section 5 says.
- "Details on lock screen" (section 5) is out of scope for v1: every push is neutral, there is no setting.
- Code branches: backend `feat/first-week-home` (from `main` 0c7d275), frontend `feat/first-week-home` (from `fix/first-conversation-prep-card-arrival` 5ec58ed, which is not on `dev` yet and ships with this work).
