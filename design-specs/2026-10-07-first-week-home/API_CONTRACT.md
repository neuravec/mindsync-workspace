# First-week Home: API contract (v1, 2026-10-08)

Owner: integration-devops. Status: VERIFIED against code, ready for parallel build by backend-api, data-analytics and flutter-mobile. Open questions at the end (section 14) need the lead or the operator; none of them blocks starting WP-1 or WP-2.

- Source of truth: `SPEC.md` in this folder. **Section 13 (operator decisions 2026-10-08) overrides earlier sections.** Security conditions: `audit-security-design.md` (H-1 to H-4, M-1 to M-4, M-6).
- Verified against: backend `MindSync` on `main` at `0c7d275` (branch `feat/first-week-home` has no commits yet), frontend `mindsync-frontend` at `5ec58ed` (`fix/first-conversation-prep-card-arrival`, the base of `feat/first-week-home`). Every existing endpoint, route, schema and event cited below was read in code; `file:line` refers to those commits.
- Dropped by 13.2 and absent from this contract: `today.exempt`, the `first_week_allowances` ledger, every "Included in your first week" string, any server logic that decides a step is exempt from Free limits.

Contents: 0 Conventions. 1 `GET /first-week/plan`. 2 `cta_route` allowlist. 3 `GET /first-week/follow-up`. 4 Mutations. 5 Day-7 recap. 6 Quick check-in and mirror. 7 Therapy schedule (Art. 9 gate, one-off session, version gate). 8 `POST /reflect/start`. 9 Additive change to `GET /users/usage`. 10 PostHog emission sides. 11 Impact and failure modes. 12 Deploy order and rollback. 13 Verified references. 14 Open questions.

---

## 0. Conventions (apply to every new endpoint)

| Topic | Rule |
|---|---|
| Base path | New router `app/api/v1/endpoints/first_week.py`, registered in `app/api/v1/api.py` at prefix `/first-week` with the same guarded `try: import ... except ImportError` pattern every optional router uses (`api.py:42-52` for symptoms). Mounted under `settings.API_V1_STR` (`main.py:332`), so full paths are `/api/v1/first-week/...`. An import failure removes the router (client sees 404, degrades to legacy Home) instead of crash-looping the dyno. |
| Auth | `Depends(deps.get_current_user)` (`deps.py:23-35`). No user id in path, query or body; every read and write is filtered by the token uid. Invalid or expired token: `401 {"detail": "Invalid or expired authentication token."}`. Missing `Authorization` header: FastAPI 0.111 `HTTPBearer` answers `403 {"detail": "Not authenticated"}` (`requirements.txt:34`). No first-week endpoint uses 403 for anything else. |
| Request bodies | Pydantic v2 models with `model_config = ConfigDict(extra="forbid")`, `Literal` enums, explicit bounds. Endpoints without a body declare an empty forbid model as an optional body: no body or `{}` is accepted, any key gives 422. Never settable anywhere: `variant`, `tone`, `day`/`plan_day`, `done`, `exempt`, `first_week_started_at`, any user id. |
| Error body | FastAPI shape. 4xx/5xx other than 422: `{"detail": "<snake_case_code>"}` with a fixed code string (codes listed per endpoint). 422: FastAPI's list form `{"detail": [{"loc": [...], "msg": "...", "type": "..."}]}`. First-week endpoints never return the splash contract strings `profile_not_created` or `user_not_found` (`users.py:1096-1119`), so no first-week error can route the client to onboarding or sign-out. |
| Degradation | Before `alembic upgrade head`, and for any unexpected server error inside these endpoints: `503 {"detail": "first_week_unavailable"}`. Never 500, never an error at import or boot. New columns are `String(n)` with Python constants, never `Enum(PyEnum)`; new tables and the new `users.first_week_started_at` column are read through guarded helpers (CLAUDE.md H10 rule). `first_week_started_at` goes into the `User` mapper's `exclude_properties` next to `first_conversation_claimed_at` (`models.py:243-249`): a mapped-but-missing column would break every user INSERT (registration) in the deploy-before-migrate window, and `deferred` does not protect INSERTs. |
| Caching | Every response of every new `/first-week/*` endpoint (sections 1, 3, 4, 5 and 6.1) carries `Cache-Control: no-store` (success and error). The client never writes these payloads to disk (no SharedPreferences, no file cache); in-memory Cubit state only. Also on `POST /users/therapy-schedule/change` (section 7). |
| Dates and times | `date` fields: `"YYYY-MM-DD"`, the calendar date in the user's IANA time zone (`user_preferences.time_zone`, UTC fallback; WP-0 fixes `UTC+2` style values). Local instants (`next_session_at`, `next_boundary_at`): ISO 8601 with the user's local offset, same convention as `TherapyScheduleResponse.next_session_at` (`schemas.py:1046-1070`). Usage instants (`quota.resets_at`): ISO 8601 UTC with `Z`, serialized with the same `_iso_utc_z` helper as `/users/usage` (`plan_usage.py:21-27`). Times of day: `"HH:MM"`, 24 h, `00:00` to `23:59`. |
| Nulls | Pydantic v2 serializes `Optional` fields as JSON `null`; keys are always present. |
| Forward compatibility | The client parses tolerantly (pattern of `UserUsage.fromJson`, `user_usage.dart:51-78`): an unknown value in `steps[]`, `links`, `side_card` or `rhythm` options is skipped; an unknown `today.state`, `today.step` or `today.copy_key` means "cannot render honestly" and the client falls back to the legacy Home for that load. |
| Logging | Backend logs user id and counts only. Never tone, variant, step keys, session dates, question text, memory text or scores. |
| Analytics | No first-week endpoint emits a PostHog event. Section 10 lists which side emits each fact. No response field name or value is ever copied into an event (`tone`, `copy_key`, `step`, `side_card`, `support_link`, `links`, `quoted` are all on the guard list, SPEC 8). |
| Tone neutrality (H-1, H-2) | Every response has the same keys, the same enums and the same status codes in both tones. Only the value of `tone` and of `support_link` differ. `copy_key` values are tone-agnostic; the client picks the gentle string from `tone`. |

---

## 1. `GET /api/v1/first-week/plan`

Read-only. Decrypts no message and calls no model; step states come from row existence and timestamps; tone comes only from `first_week_tone(db, user_id)` (Redis, H-2); variant comes only from the consent-gated helper (SPEC 3.2). The response never contains a variant label, the follow-up text, memory text, scores or suppression reasons.

### 1.1 Status codes

| Code | Body | When | Client |
|---|---|---|---|
| 200 | `FirstWeekPlanResponse` | `users.first_week_started_at` is set. This includes a hidden plan (`plan_active: false`) and every day after week 1. | First-week Home. |
| 204 | empty | `first_week_started_at` IS NULL (every account created before release, onboarding not completed yet, or the users row missing). | Legacy Home, unchanged. |
| 401 / 403 | see section 0 | Auth. | Existing auth handling, then legacy Home. |
| 404 | FastAPI default | Backend without the router (older deploy, import failure). | Legacy Home. |
| 503 | `{"detail": "first_week_unavailable"}` | Migration not run, Redis or DB failure, any unexpected error. | Legacy Home. |

Deviation from SPEC 4 text, on purpose: SPEC 4 says 204 also "when the plan is hidden and no rhythm exists", but SPEC 3.3 ("the Today card stays with an open Talk with Orca" after "Hide this plan") and 13.1 ("permanent Today card") require a Today card for hidden plans. A hidden plan therefore returns 200 with `plan_active: false`. 204 means only "no anchor". Lead to confirm (section 14, Q1).

Client: a 204 body is empty and has no JSON content type, so `DioClient.getMap` / `getMapOrNull` would throw "Unexpected response format" (`dio_client.dart:141-186`). The plan call must check `statusCode == 204` before parsing (a small `getMapWithStatus` helper in `DioClient` is the expected approach). Client timeout for this one call: 6 s, then legacy Home (same budget as `TrialPopupManager`, `trial_popup_manager.dart:136`).

### 1.2 `FirstWeekPlanResponse`

| Field | Type | Meaning |
|---|---|---|
| `plan_day` | int >= 0 | Number of local 04:00 boundaries crossed since the anchor, in the user's time zone. Day 0 is the onboarding day. |
| `phase` | `"first_week"` \| `"rhythm"` | `first_week` for plan days 0 to 7, `rhythm` from plan day 8. Drives plan card title ("Your first week" / "This week") and its bottom link ("Hide this plan" / "Change my rhythm"). |
| `plan_active` | bool | `false` after `POST /plan/hide` (or "I'll find my own way" on the recap). Plan card hidden, plan reminders stop, Today card in state `open`. Also the only property allowed on `today_card_viewed` / `today_card_tapped`. |
| `tone` | `"standard"` \| `"gentle"` | From `first_week_tone` only. Client holds it in memory (Cubit) only. |
| `first_talk` | `"done"` \| `"skipped"` | `done` when the onboarding first-conversation thread (`entry_origin = onboarding_first_conversation`) has at least one user message. Drives the day-0 copy, the "First talk" chip in the plan card, and the `talk` step copy. |
| `next_session_at` | datetime (local offset) \| null | Next session, read only through the consent-gated helper (`therapy_schedule_if_consented`). Null without active ARTICLE9_HEALTH consent even when a legacy schedule exists. The client reads it for the prep card title (fallback after `today.session_date`), the mirror variant and the session sheet's initial time and `replaces_date` fallback. The first-week Home hero shows no session at all (COPY 1) and does not read it (lead correction 2026-10-11). It is not adjusted for a prep step dropped through "Not sure yet". |
| `next_boundary_at` | datetime (local offset) | The next local 04:00. The client refetches the plan on resume when `now >= next_boundary_at`. |
| `today` | `TodayCard` | Always present on 200. See 1.3. |
| `steps` | list of `PlanStep` | Plan card rows, ordered by date. Empty when `plan_active` is false. See 1.4. |
| `side_card` | `"add_session_time"` \| `"add_sessions"` \| null | B: "When is your next session?". C: "Seeing a therapist?". Null in phase `rhythm`, after dismissal, and for A. Same in both tones (SPEC 3.4). |
| `reminder` | `{"state": "on" \| "off", "time": "HH:MM"}` | Plan-step reminder setting. Default `off`; default time = anchor local time rounded down to the half hour, clamped to `08:00`..`21:00` (backend-api may refine, Q13). Returned unchanged in gentle tone; the client hides the day-0 reminder row in gentle tone and the server sends no plan-step reminders while gentle (SPEC 3.6). |
| `rhythm` | `Rhythm` \| null | Null before plan day 7. From day 7 on: `{"chosen": [RhythmOption] \| null, "available": [{"option": RhythmOption, "preselected": bool}], "time": "HH:MM"}`. `chosen` is null until `PUT /rhythm` (or until the preselected set auto-applies on day 9, SPEC 3.5). Used by "Change my rhythm". |
| `trial_sheet_eligible` | bool | See 1.6. Never depends on tone. |
| `starter_offer_eligible` | bool | See 1.6. Always `false` when `trial_sheet_eligible` is `false`. |

`TodayCard`:

| Field | Type | Meaning |
|---|---|---|
| `step` | `StepKey` \| null | The step the card is about. Null for `day0`, `open`, `rest`. |
| `state` | `TodayState` | See 1.3. |
| `copy_key` | `TodayCopyKey` | Tone-agnostic copy selector (enum in 1.5). Never a widget key, route, log text or event value. |
| `cta_route` | allowlisted route \| null | Section 2. Null when the card has no primary CTA (`day0`, `deferred`, `done`). |
| `links` | list of `"session_moved"` \| `"didnt_happen"` | Link slot. `session_moved` only on `prep`, `didnt_happen` only on `after`, in states `today` and `quota_out`. Both open the session sheet (section 7.3). |
| `support_link` | bool | `true` exactly when `tone == "gentle"`. Helpline link in the link slot, external browser, no event (`_CalmContinuation` precedent, H-1 item 3). |
| `quota` | `Quota` \| null | See 1.5. Non-null only when the account is on Free (`resolve_plan` returns `free`, `plan_usage_service.py:85-96`) and the card's action uses a limited feature. |

`PlanStep`:

| Field | Type | Meaning |
|---|---|---|
| `step` | `StepKey` | |
| `date` | date \| null | Local date the step is planned for. For a `deferred` step: the day it moved to, or null when it has nowhere to go (it then disappears at the next boundary, "dropped silently"). |
| `state` | `"done"` \| `"today"` \| `"upcoming"` \| `"deferred"` \| `"quota_out"` | `dropped` exists only server-side; dropped steps are omitted, never sent. |
| `copy_key` | `StepCopyKey` | Row title selector (enum in 1.5). |

Window of `steps[]`: phase `first_week` = plan days 1 to 7 (day 0 is rendered by the client from `first_talk`: "Setup" is always done, "First talk" only when `first_talk == "done"`). Phase `rhythm` = rhythm steps dated from 2 days before today through 6 days after today, plus the `recap` step while it falls inside that window.

### 1.3 Today card states (server derivation, first match wins)

| # | Condition | `state` | `step` | `copy_key` | `cta_route` |
|---|---|---|---|---|---|
| 1 | `plan_day == 0` | `day0` | null | `today.day0`, or `today.day0_late` when the anchor's local time is 00:00 to 03:59 ("After some sleep") | null |
| 2 | `plan_active == false` | `open` | null | `today.open` | `/main-page/tab/reflect?new=true` |
| 3 | Today's step done today | `done` | that step | `today.done` | null |
| 4 | Today's step deferred today | `deferred` | that step | `today.deferred` | null |
| 5 | Today's step open, account on Free, its feature has `left == 0` (`prep`, `after`, `note`, `talk`, `talk2`) | `quota_out` | that step | `today.<x>_quota_out` | see section 2 |
| 6 | Today's step open | `today` | that step | per step, see 1.5 | see section 2 |
| 7 | No step today | `rest` | null | `today.rest` | `/main-page/tab/reflect?new=true` |

`done` comes only from a real result on the step's day (SPEC 3.3): `talk`/`talk2` a Reflect thread with at least one user message, `prep` a prep card, `after` a debrief, `note` a between-session note, `checkin` at least one new symptom score, `recap` the first 200 of `GET /first-week/recap`. Never from elapsed time.

States `open` and `rest` carry `quota` for `reflect_messages` when on Free, so the client can show the "Reflect messages: 0 of 15 left until {date}" line; the state itself does not change (their CTA opens the ordinary Reflect flow, which already has its limit panel).

### 1.4 Step keys and plan rules

`StepKey` (fixed enum, `String(32)` column server-side, never a PG enum): `talk`, `talk2`, `prep`, `after`, `note`, `checkin`, `recap`. Plan layout, priorities, the one move, "Not today" and the session rules are exactly SPEC 3.3. Rhythm mapping from plan day 8: `before_after_session` produces `prep` (day before each session) and `after` (session day); `checkin_monday` produces `checkin`; `talk_wednesday` produces `talk2`; `voice_note_friday` produces `note`.

### 1.5 Enums

| Enum | Values |
|---|---|
| `TodayState` | `day0`, `today`, `deferred`, `done`, `rest`, `quota_out`, `open` |
| `StepState` (wire) | `done`, `today`, `upcoming`, `deferred`, `quota_out` (server-only: `dropped`) |
| `TodayCopyKey` | `today.day0`, `today.day0_late`, `today.first_talk` (`talk` when `first_talk == "skipped"`), `today.talk`, `today.talk2`, `today.rhythm_talk` (`talk2` in phase `rhythm`), `today.prep`, `today.after`, `today.note`, `today.note_therapy` (B's "Note something for therapy": copy only, same feature, screen, route and events as `note`), `today.checkin`, `today.recap`, `today.deferred`, `today.done`, `today.rest`, `today.open`, `today.prep_quota_out`, `today.after_quota_out`, `today.note_quota_out`, `today.talk_quota_out` (also for `talk2`) |
| `StepCopyKey` | `step.first_talk`, `step.talk`, `step.talk2`, `step.rhythm_talk`, `step.prep`, `step.after`, `step.note`, `step.note_therapy`, `step.checkin`, `step.recap` |
| `Link` | `session_moved`, `didnt_happen` |
| `SideCard` | `add_session_time` (B), `add_sessions` (C) |
| `ReminderState` | `on`, `off` |
| `Tone` | `standard`, `gentle` |
| `RhythmOption` | `before_after_session` (A only), `checkin_monday`, `talk_wednesday`, `voice_note_friday` |
| `QuotaFeature` | `before_therapy`, `after_therapy`, `between_sessions`, `reflect_messages` (the `FeatureUsageMap` keys, `plan_usage.py:43-51`) |

Step to quota feature: `prep` -> `before_therapy`, `after` -> `after_therapy`, `note` -> `between_sessions`, `talk`/`talk2` -> `reflect_messages`, `checkin` and `recap` -> none (always free).

### 1.6 `Quota` (from the real `GET /users/usage`)

Verified source: `GET /api/v1/users/usage` (`users.py:1159-1177`), schema `UserUsageResponse` (`plan_usage.py:30-66`), built by `plan_usage_service.get_user_usage` (`plan_usage_service.py:141-185`). Today's real limits and counters:

| Feature key | Free limit (source) | Counter (same one the gate uses) | Period / reset |
|---|---|---|---|
| `before_therapy` | 1, `FREE_TIER_MONTHLY_PREP_LIMIT` (`config.py:189`) | `crud.count_prep_cards_this_month` via `count_ai_feature_usage_this_month` (`_therapy_helpers.py:85-98`) | `month`, resets 00:00 UTC on the 1st (`plan_usage_service.py:56-66`) |
| `after_therapy` | 1, `FREE_TIER_MONTHLY_DEBRIEF_LIMIT` (`config.py:188`) | `crud.count_debriefs_this_month` | `month` |
| `between_sessions` | 3, `FREE_TIER_MONTHLY_BETWEEN_SESSIONS_LIMIT` (`config.py:190`) | `crud.count_between_session_notes_this_month` | `month` |
| `reflect_messages` | 15, `REFLECT_MONTHLY_MESSAGE_LIMIT` (`config.py:201`) | `first_conversation.count_billable_reflect_messages_this_month` (`plan_usage_service.py:118-138`) | `month` |
| `session_recordings` | 2, `FREE_TIER_RECORDING_LIMIT` (`config.py:266`) | `crud.count_completed_recordings` | `lifetime` |
| `habits` | 1, `FREE_TIER_MAX_ACTIVE_HABITS` (`crud/habit.py:46`) | `habit_crud.count_active_habits` | `active` |

`limit` is null for `trial` and `premium` (`plan_usage_service.py:147-150`); none of these settings is overridden in `.env` (checked) or, per the config comment, in Heroku. At the limit, prep, after and note creates still save but without AI processing (plain text), and guiding questions fall back to static defaults (`between_sessions.py:350-356`, `debriefs.py:398-403`); Reflect messages are refused with `403 monthly_limit_reached` (`reflect.py:1255`).

`Quota` object (computed by calling the same `get_user_usage` inside the plan endpoint, so the card and every chip in the app can never disagree):

```json
{
  "feature": "reflect_messages",
  "used": 15,
  "limit": 15,
  "left": 0,
  "period": "month",
  "resets_at": "2026-11-01T00:00:00Z",
  "resets_on": "2026-11-01"
}
```

- `left = max(0, limit - used)`. `resets_on` is the UTC calendar date of `resets_at`: the client prints it as is ("until Nov 1") and must not convert `resets_at` to local time, which would print "Oct 31" in the Americas.
- Chip "1 free this month": client shows it when `feature` is `before_therapy` or `after_therapy` and `left == 1`.
- If `get_user_usage` fails inside the plan endpoint: `quota: null`, state as if not on Free, `trial_sheet_eligible: false`, `starter_offer_eligible: false` (fail closed: no chip, no sheet, never a paywall).
- Numbers in copy (quota lines, rhythm list, day-3 sheet) always come from these fields or from `free_limit` (section 9), never from strings.

### 1.7 Day-3 trial sheet and the starter offer

How eligibility is decided today (verified):
- Day-3 sheet: client only. `TrialPopupManager.decide` (`trial_popup_manager.dart:101-121`) shows it when `/users/usage` says `plan == trial` and `trialDaysLeft == 1` (`trial_timing.dart:58-65`, device time zone) and the local flag `ms_trial_reminder_seen_{uid}` is not set (`trial_popup_manager.dart:72`).
- Post-onboarding starter offer: client only. `WowCubit._offerSkipReason` (`wow_cubit.dart:395-413`): just completed onboarding, not a rerun, profile loaded, not already premium via purchase/starter/legacy, active sign-up trial, local flag `PostOnboardingOfferMemory.wasShown(uid)` (`push_prompt_policy.dart:77`). Then the store: the starter is shown only if the product query returns `ms_starter_package` (`wow_cubit.dart:424-437`, `purchases_data_provider.dart:127-139`), and it is bought with `buyNonConsumable` (`purchases_data_provider.dart:110-121`).
- Server: no eligibility endpoint and no "already bought the starter" check. It only verifies the receipt, grants `granted_via = starter_pack` for 14 days (`users.py:824-836`, `config.py:269-270`) and rejects a transaction bound to another account (`users.py:801-815`).
- Answer: today the client decides eligibility and the store decides whether the purchase can happen.

New rule (13.3), server decides the account side, store decides availability:

`trial_sheet_eligible = true` iff all of:
1. `resolve_plan(...) == "trial"` (an active `signup_trial` grant; any purchase, promo or starter makes it `premium`, `plan_usage_service.py:85-96`);
2. the user-local calendar date (stored IANA zone) is the day before the local date of `trial_ends_at` (same rule as `trialCalendarDaysLeft == 1`, computed server-side so the plan and the sheet use one clock);
3. `today.state` is `done`, `rest` or `open` (shown after today's step is done, or on the next open on a rest day, SPEC 6).

`starter_offer_eligible = true` iff `trial_sheet_eligible` and the account has no `subscription_receipts` row with `product_sku == settings.STARTER_PACK_PRODUCT_SKU` and `status == "VERIFIED"` (`models.py:768-780`).

Client:
- For accounts with a plan (200), `trial_sheet_eligible` replaces `isTrialReminderDay` in `TrialPopupManager`; the once-per-account flag `ms_trial_reminder_seen_{uid}` still applies, and the sheet may also open when Home refetches the plan after the step screen closes (not only on app open). Accounts with 204 keep today's logic unchanged.
- Starter on the sheet only when `starter_offer_eligible` is true AND `getStarterPackageProduct()` returns a product; otherwise the regular "Keep Premium" path. The store has the last word (an Apple ID or Play account that already owns the non-consumable cannot buy it again; a transaction bound to another MindSync account is rejected server-side).
- Sheet copy "Writing stays on Free, up to N messages a month": N = `features.reflect_messages.free_limit` from `/users/usage` (section 9). During the trial `limit` is null, which is why `free_limit` is needed.

### 1.8 Examples

B/C account, plan day 3 (`note`), still on trial, standard tone:

```json
{
  "plan_day": 3,
  "phase": "first_week",
  "plan_active": true,
  "tone": "standard",
  "first_talk": "done",
  "next_session_at": null,
  "next_boundary_at": "2026-10-12T04:00:00+02:00",
  "today": {
    "step": "note",
    "state": "today",
    "copy_key": "today.note",
    "cta_route": "/fab/between-sessions",
    "links": [],
    "support_link": false,
    "quota": null
  },
  "steps": [
    {"step": "talk", "date": "2026-10-09", "state": "done", "copy_key": "step.talk"},
    {"step": "note", "date": "2026-10-11", "state": "today", "copy_key": "step.note"},
    {"step": "checkin", "date": "2026-10-12", "state": "upcoming", "copy_key": "step.checkin"},
    {"step": "talk2", "date": "2026-10-14", "state": "upcoming", "copy_key": "step.talk2"},
    {"step": "recap", "date": "2026-10-15", "state": "upcoming", "copy_key": "step.recap"}
  ],
  "side_card": "add_sessions",
  "reminder": {"state": "on", "time": "19:00"},
  "rhythm": null,
  "trial_sheet_eligible": false,
  "starter_offer_eligible": false
}
```

(Trial ends 2026-10-12, so 10-11 is the sheet day; `trial_sheet_eligible` turns `true` once the note is saved and the plan is refetched.)

A account, plan day 2 (`prep`, session on day 3), gentle tone:

```json
{
  "plan_day": 2,
  "phase": "first_week",
  "plan_active": true,
  "tone": "gentle",
  "first_talk": "done",
  "next_session_at": "2026-10-11T17:00:00+02:00",
  "next_boundary_at": "2026-10-11T04:00:00+02:00",
  "today": {
    "step": "prep",
    "state": "today",
    "copy_key": "today.prep",
    "cta_route": "/fab/prepare-therapy",
    "links": ["session_moved"],
    "support_link": true,
    "quota": null
  },
  "steps": [
    {"step": "talk", "date": "2026-10-09", "state": "done", "copy_key": "step.talk"},
    {"step": "prep", "date": "2026-10-10", "state": "today", "copy_key": "step.prep"},
    {"step": "after", "date": "2026-10-11", "state": "upcoming", "copy_key": "step.after"},
    {"step": "checkin", "date": "2026-10-13", "state": "upcoming", "copy_key": "step.checkin"},
    {"step": "recap", "date": "2026-10-15", "state": "upcoming", "copy_key": "step.recap"}
  ],
  "side_card": null,
  "reminder": {"state": "off", "time": "19:00"},
  "rhythm": null,
  "trial_sheet_eligible": false,
  "starter_offer_eligible": false
}
```

Free account, plan day 6 (`talk2`), Reflect messages used up (only `today` shown):

```json
{
  "step": "talk2",
  "state": "quota_out",
  "copy_key": "today.talk_quota_out",
  "cta_route": "/first-week/check-in",
  "links": [],
  "support_link": false,
  "quota": {"feature": "reflect_messages", "used": 15, "limit": 15, "left": 0, "period": "month", "resets_at": "2026-11-01T00:00:00Z", "resets_on": "2026-11-01"}
}
```

Hidden plan (`plan_active: false`, `steps: []`), Free with messages left:

```json
{
  "step": null,
  "state": "open",
  "copy_key": "today.open",
  "cta_route": "/main-page/tab/reflect?new=true",
  "links": [],
  "support_link": false,
  "quota": {"feature": "reflect_messages", "used": 4, "limit": 15, "left": 11, "period": "month", "resets_at": "2026-11-01T00:00:00Z", "resets_on": "2026-11-01"}
}
```

Day 0 after a late-night onboarding: `"today": {"step": null, "state": "day0", "copy_key": "today.day0_late", "cta_route": null, "links": [], "support_link": false, "quota": null}`.

Phase `rhythm`, plan day 9, A on Free with the monthly prep still available: `today` = `{"step": "prep", "state": "today", "copy_key": "today.prep", "cta_route": "/fab/prepare-therapy", "links": ["session_moved"], "support_link": false, "quota": {"feature": "before_therapy", "used": 0, "limit": 1, "left": 1, ...}}` (client shows the "1 free this month" chip), `rhythm.chosen = ["before_after_session", "checkin_monday"]`.

---

## 2. `cta_route` allowlist

The client navigates only to these exact strings (path plus query, compared literally). Anything else, including null and any value a future backend invents, means "stay on Home" (no navigation, no error UI). This is in addition to `MsRoutes.isRoutable` (`ms_routes.dart:288-292`), which is a denylist and is not enough here.

| `cta_route` | Used for | Status | Verified |
|---|---|---|---|
| `/first-week/follow-up` | `talk`, `talk2`, rhythm talk (state `today`) | NEW route, flutter-mobile adds it | Not in `ms_routes.dart` today |
| `/first-week/check-in` | `checkin` (state `today`); `talk`/`talk2`/`note` in state `quota_out` | NEW route | Not in `ms_routes.dart` today |
| `/first-week/recap` | `recap` (state `today`) | NEW route | Not in `ms_routes.dart` today |
| `/fab/prepare-therapy` | `prep` (state `today`) | Existing | `ms_routes.dart:87`, GoRoute `:616-620` |
| `/fab/after-therapy` | `after` (state `today`) | Existing | `ms_routes.dart:86`, GoRoute `:607-615` (optional `extra.isFirstCapture`) |
| `/fab/between-sessions` | `note` for B and C alike (state `today`) | Existing | `ms_routes.dart:88`, GoRoute `:621-625` |
| `/workspace/agenda` | `prep` and `after` in state `quota_out` ("Add to my agenda", "Save a takeaway"); the screen already has an add flow (`agenda_full_screen.dart:108`) | Existing | `ms_routes.dart:298`, GoRoute `:723-727` |
| `/main-page/tab/reflect?new=true` | states `rest` and `open` ("Talk with Orca") | Existing | `ms_routes.dart:126-131`, `parseTabDeepLinkParams` `:183-196`, GoRoute `:401-422` |

Fallback = Home (`/main-page`, `ms_routes.dart:56`, GoRoute `:380-384`).

Rules for the new routes (H-1 items 2 and 9): one route per screen for every tone, step and source; no route arguments that carry tone, step, variant or question source (the follow-up screen asks `GET /first-week/follow-up` itself); each GoRoute sets `name` so `PosthogObserver` (`ms_routes.dart:311`) records a stable `$screen`. The check-in mirror is a state of `/first-week/check-in`, not a route.

Not routes (open in place as modal sheets, so they produce no `$screen` that could act as a therapy proxy): the session sheet (from `links`), the rhythm list ("Change my rhythm"), the day-3 trial sheet (existing `trial_reminder_sheet.dart`). Side cards use fixed client flows: B "Add session time" opens the existing `SessionSetupScreen` (`main_tab/widgets/session_setup_screen.dart`, writes through `SettingsCubit.addTherapySession` / `addCustomSession` at `:213` and `:228`); C "Add sessions" opens the Art. 9 consent step first (section 7.1).

Correction to SPEC 5 (push payload): the plan-step push must use `route: "/main-page"`. `/home` is not a GoRoute; the resolver passes unknown full paths through unchanged (`notification_route_resolver.dart:44-67`) and GoRouter would show `RouteNotFoundScreen` (`ms_routes.dart:316`).

---

## 3. `GET /api/v1/first-week/follow-up`

Returns the question for today's open talk step. For `talk` it is the day-1 follow-up (13.4); for `talk2` and rhythm talks it is a generic weekly question. The server selects the row by the token uid only; there is no id parameter.

| Code | Body | When |
|---|---|---|
| 200 | `{"question": "<plain text, max 300 chars>", "quoted": true \| false}` | `today.step` is `talk` or `talk2` and `today.state == "today"`. |
| 404 | `{"detail": "not_found"}` | No anchor, no open talk step today, or anything else (missing and foreign alike). |
| 503 | `{"detail": "first_week_unavailable"}` | Unexpected failure. |

Question source (13.4 overrides SPEC 3.9 and 6):
- `quoted: true`: generated by data-analytics from a memory item actually written from the onboarding first conversation, with `memory_extraction_gate(...) == "allowed"` at generation (`orca_memory.py:475`) and `not profiling_withdrawn(...)` at display (`orca_memory.py:455`); stored Fernet-encrypted in `first_week_follow_ups` (SPEC 3.9 storage, FK cascades, 7-day purge).
- `quoted: false`: generic question written by brand-voice-manager (server-side allowlist, 7 locales, user's `ai_language`), never built from setup answers. Used when the first conversation was skipped, no memory item came out of it, a gate says no, the follow-up table is missing (before migration), for `talk2` and rhythm talks, and for every crisis case.
- Display-time checks before returning a quoted question (M-2): `contains_crisis_language` on question and item (`orca_memory.py:337`), tone is `standard`, `thread_has_crisis_language` over Reflect threads since the anchor (`orca_memory.py:1424`), the memory item still exists. Any failure: a calm question with `quoted: false`.
- No field says which of these produced the question (no `source`, no `label`). The client shows the memory footer (link to the existing `/orca-memory`, `ms_routes.dart:71`, GoRoute `:510-516`) only when `quoted` is true. Render as plain text, no linkify.

Client: any non-200 closes the follow-up screen into the ordinary new-thread flow (`/main-page/tab/reflect?new=true`). Home and pushes never quote the question; they say "a question from your first talk" (copy must stay true when the question is generic, Q15).

---

## 4. Mutations

Every mutation: `Depends(get_current_user)`, empty or `extra="forbid"` body, `Cache-Control: no-store`, idempotent where stated, and on success **200 with the full `FirstWeekPlanResponse`** so the client re-renders without a second GET. (A 204 here would break the existing helpers: `DioClient.post`/`postEmpty`/`put` return `response.data` typed as a map, `dio_client.dart:193-256`, and `delete` returns nothing, `:321-334`.) Common errors: `404 {"detail": "first_week_inactive"}` when the account has no anchor, `503 first_week_unavailable`, 422 for validation.

| Endpoint | Body | Semantics | Extra errors |
|---|---|---|---|
| `POST /api/v1/first-week/today/defer` | none | "Not today". Today's open step becomes `deferred`, no reminder today, the step moves once to its next free day (or is dropped at the next boundary when there is none). Counts as its one move. Idempotent when already deferred today. | `409 {"detail": "nothing_to_defer"}` when today's state is not `today` or `quota_out` |
| `POST /api/v1/first-week/today/defer/undo` | none | Undo within the same plan day: the step returns to `today` on today's date. No-op 200 when nothing was deferred today. POST (not DELETE) so the client gets the plan back through `postEmpty`. | none |
| `POST /api/v1/first-week/today/drop` | none | "It didn't happen" (and "It moved" + "Not sure yet") from the `after` card: drops today's `after` step silently; the schedule is not touched. Idempotent. | `409 {"detail": "nothing_to_drop"}` when today's step is not an open `after` |
| `POST /api/v1/first-week/plan/hide` | none | "Hide this plan" and "I'll find my own way". `plan_active` becomes false, plan reminders stop, Today card `open`. Idempotent. No unhide endpoint in v1 (Q12). | none |
| `POST /api/v1/first-week/side-card/dismiss` | none | `side_card` becomes null for good. Idempotent (200 even when there was none). | none |
| `PUT /api/v1/first-week/rhythm` | `{"options": [RhythmOption, ...], "time": "HH:MM"}` | "Keep this rhythm" / "Change my rhythm". `options`: 0 to 4 unique values, each must be in this account's `rhythm.available`. `time` also becomes the reminder time. Allowed from plan day 7. | `422` for unknown, duplicate or unavailable options (`before_after_session` without a consented schedule) and before plan day 7 |
| `PUT /api/v1/first-week/reminder` | `{"enabled": bool, "time": "HH:MM"}` (`time` optional, keeps the current one) | Plan-step reminder on/off. Allowed in both tones; the server simply sends nothing while tone is gentle. Call only after the OS permission result (`FcmPushPermissionGateway`): granted -> `enabled: true`; denied -> no call, show "Open Settings". | none |

All bodies: `extra="forbid"`; nothing in SPEC 4's forbidden list is settable.

---

## 5. Day-7 recap: `GET /api/v1/first-week/recap`

Built on `gather_weekly_summary_data` (`crud.py:2441`) and `assemble_weekly_summary_sections` (`openai_service.py:1128`) over the signup-anchored window [anchor, start of plan day 8). The endpoint never waits on a model: "Orca noticed" is prepared by a background job from plan day 7 and is `null` until it exists.

| Code | Body | When |
|---|---|---|
| 200 | `FirstWeekRecapResponse` | Anchor set and `7 <= plan_day <= 14` (window end: Q12). The **first 200 marks the `recap` step done** ("opened", SPEC 3.3). The client fetches it only when the recap screen opens, never as a prefetch. |
| 404 | `{"detail": "recap_not_available"}` | No anchor, before plan day 7, after the window. |
| 503 | `{"detail": "first_week_unavailable"}` | |

```json
{
  "quiet": false,
  "did": ["first_talk", "talk", "prep", "after", "checkin"],
  "where": [
    {"symptom_id": 12, "name": "Stress", "setup_score": 8, "latest_score": 6},
    {"symptom_id": 15, "name": "Sleep", "setup_score": 7, "latest_score": 7},
    {"symptom_id": 18, "name": "Focus", "setup_score": null, "latest_score": 4}
  ],
  "noticed": {"text": "Sleep came up in both of your talks this week.", "in_timeline": true},
  "mentioned": [
    {"memory_item_id": 41, "text": "Sleep has been rough lately"},
    {"memory_item_id": 44, "text": "Walks help you clear your head"}
  ],
  "rhythm": {
    "available": [
      {"option": "before_after_session", "preselected": true},
      {"option": "checkin_monday", "preselected": true},
      {"option": "talk_wednesday", "preselected": false}
    ],
    "chosen": null,
    "time": "19:00"
  }
}
```

| Section | Rule |
|---|---|
| `quiet` | Server decides (proposal: fewer than 2 done steps in plan days 1 to 7). Quiet: `where` and `noticed` are null, `rhythm.available` holds exactly one option with `preselected: false`, no empty sections. |
| `did` | Done items only, ordered by date: `first_talk` (when done) plus done `StepKey`s. No modality, no counts. May be empty; the client then shows the subtitle only. |
| `where` | "Setup" next to "Latest", numbers only. Rows only for setup areas with a check-in in the window; `setup_score: null` renders "Not set" (source of that null: Q2). Null when there is no check-in, in a quiet week, and whenever any crisis flag occurred in the week (SPEC 3.6: no deltas). |
| `noticed` | Crisis-screened (`contains_crisis_language`). Null when not ready yet, in a quiet week, or when any flag occurred in the week. `in_timeline` is true only if the same text really is in a Weekly summary card on the Timeline (no false claims, lesson of WP-0 fix 2). |
| `mentioned` | Up to 3 live memory items created in the window, newest first. Null when empty or when the memory gate blocks (`profiling_withdrawn`, `memory_extraction_gate`). |
| `rhythm` | Same shape as in the plan (section 1.2). Free-limit labels come from `/users/usage` `free_limit` (section 9). |

Actions on the recap:
- "Keep this rhythm": `PUT /first-week/rhythm`. "I'll find my own way": `POST /first-week/plan/hide`.
- "Not right" on a mentioned item: the existing hard delete `DELETE /api/v1/users/memory/{item_id}` (`users.py:2055-2074`): `204` on success, `404 {"detail": "memory_item_not_found"}` when it is not the caller's or already gone (client treats as done), `503 {"detail": "memory_unavailable"}` (client keeps the item, shows the error toast). The client uses the same deferred delete as "What Orca remembers": the call is sent after the 5 s Undo window or when the screen closes, and Undo inside the window sends nothing (existing events, section 10).

---

## 6. Quick check-in and mirror

### 6.1 `GET /api/v1/first-week/checkin-baseline` (NEW)

Why new instead of composing `GET /users/therapy-context` + `GET /symptoms/`: the setup values live in `user_therapy_context.severity_ratings` keyed by area name, the symptom ids live in `user_symptoms`, and matching them by name on the client breaks after a rename or a Reset onboarding (which clears `severity_ratings`, `crud.py:782-809`). The recap needs the same join server-side anyway.

| Code | Body | When |
|---|---|---|
| 200 | see below | Anchor set (also after week 1, for the Monday check-in). |
| 404 | `{"detail": "first_week_inactive"}` | No anchor. |
| 503 | `{"detail": "first_week_unavailable"}` | |

```json
{
  "areas": [
    {"symptom_id": 12, "name": "Stress", "setup_score": 8, "latest_score": null, "latest_at": null},
    {"symptom_id": 15, "name": "Sleep", "setup_score": 7, "latest_score": 7, "latest_at": "2026-10-12T19:04:11+00:00"},
    {"symptom_id": 18, "name": "Focus", "setup_score": null, "latest_score": null, "latest_at": null}
  ]
}
```

- `areas`: the visible symptoms that came from the onboarding focus areas, ordered by `setup_score` descending, nulls last. The client asks the first 3 and offers "Also rate {area}" for the rest.
- `setup_score`: 1 to 10, or null for "Not set" (an area left at the untouched default 5 in onboarding, see Q2). `latest_score`/`latest_at`: newest score after the anchor, or null.
- `name` is the person's own label: shown on their screen only, never in analytics or logs.

### 6.2 Saving: existing `POST /api/v1/symptoms/{symptom_id}/scores`

Verified (`symptoms.py:556-648`, router prefix `/symptoms` `api.py:42-52`):
- Request `SymptomScoreCreate` (`schemas.py:1533-1535`): `{"score": int}` with `ge=1, le=10`. Scale 1..10 confirmed. Not `extra="forbid"` (extra keys ignored).
- `201` `SymptomScoreResponse` (`schemas.py:1538-1544`): `{"id": int, "score": int, "created_at": datetime}`.
- `404 {"detail": "not_found"}` when the symptom is not the caller's. 422 out of range.
- One call per rated area. Partial failure: keep the saved ones, mirror shows only saved values, retry the rest. The `checkin` step is done once at least one score saved on the step's day.

### 6.3 Mirror

Rendered from the baseline (6.1) plus the scores just saved; no extra endpoint. Next-step card:
- A: "Bring this to your next session?" uses the existing `POST /api/v1/workspace/agenda` (`workspace.py:467-518`) with `{"text": "<composed by the client from the numbers, in the user's locale, max 1000 chars>", "kind": "topic"}` (`AgendaItemCreate`, `schemas/workspace.py:29-75`): `201 AgendaItemResponse`. The text is encrypted at rest (`encode`). Only the person sees agenda items today (no clinician route reads them); the confirmation line still says who can see them (L-7).
- B/C: "Talk with Orca" -> `/main-page/tab/reflect?new=true`.
- One event, `checkin_next_step_tapped`, without a `cta` property (M-1).

---

## 7. Therapy schedule

### 7.1 `PUT /api/v1/users/therapy-schedule` (existing, behavior changes)

Verified: `users.py:1645-1730`, body `TherapyScheduleUpdate` (`schemas.py:1004-1044`): `schedule` optional (null = untouched), `frequency` default `"weekly"`, `custom_sessions` optional (null = untouched); single writer `crud.update_therapy_schedule` (`crud.py:1435-1600`). Today it stores without any ARTICLE9_HEALTH check.

New rule (H-3, 13.8):

| Request | Without active ARTICLE9_HEALTH consent |
|---|---|
| Any write that leaves schedule data stored: non-empty `schedule`, non-empty `custom_sessions`, or a frequency change while entries exist | `403 {"detail": "art9_consent_required"}`, nothing written |
| A full clear (every provided list is empty and nothing remains stored) | Allowed. Removing health data never needs consent (the onboarding "not in therapy" clear, `therapy_onboarding_cubit.dart:701-710`, may run without consent) |

Consent check: `consent_crud.is_consent_active(db, uid, "ARTICLE9_HEALTH")` (`crud/consent.py:134`), the same one `user_is_in_therapy` uses (`first_conversation.py:623-641`).

Version gate (13.8 branch "not small"): config var `ART9_SCHEDULE_GATE_MIN_APP_VERSION` (unset = the 403 applies to every client, the "small number" branch). When set, the 403 applies only to requests whose `X-App-Version` (7.4) is greater than or equal to it; requests without the header, or with an unparseable or older value, keep today's behavior until those builds age out. The lead records the branch in SPEC 13.8 after database-administrator's count. `POST /therapy-schedule/change` (7.3) is always gated (only new builds call it).

Client handling (new builds):
- Send therapy-schedule writes with `retryOn403: false`. `DioClient.put` has no such option today (`dio_client.dart:241-256`), so the shared interceptor would refresh the token and resend once (`dio_client.dart:59-79`); flutter-mobile adds the parameter.
- On `403 art9_consent_required`: open the Art. 9 consent step (same wording as onboarding). Accept: `POST /api/v1/users/consent/art9_health` (`consent.py:191-219`, 200 `ConsentRecordResponse`), then retry the write once. Decline: store nothing, and roll back the optimistic local cache (`SettingsCubit` writes SharedPreferences before the PUT, `settings_cubit.dart:89` and `:278`), so Home never shows a session the server does not have.
- Any other 403 (`Not authenticated`) keeps today's auth handling.
- C side card: consent step first, then the session setup. Whether that flow must also set `currently_in_therapy` for the plan to become A: Q5.

Also drop the session date from the update log line (`users.py:1699-1705`, L-4).

### 7.2 Additive change to `GET`/`PUT` response

`TherapyScheduleResponse` (`schemas.py:1046-1070`) gains `skipped_dates: List[str]` (`"YYYY-MM-DD"`, recurring occurrences cancelled "just this once", default `[]`). Old clients ignore it. `next_session_date` / `next_session_at` honor skips and one-offs.

### 7.3 `POST /api/v1/users/therapy-schedule/change` (NEW, session sheet)

Why a new endpoint instead of the PUT: the PUT replaces whole lists sent from a local cache and defaults `frequency` to `"weekly"` when omitted; that class of bug already wiped real schedules twice (MSV3.11 CS-10, MSV3.10 CS-02, documented at `schemas.py:1004-1026` and `crud.py:1500-1543`). This endpoint is a server-side read-modify-write under a row lock on `user_preferences`.

Request (`extra="forbid"`):

```json
{"kind": "once", "date": "2026-10-12", "time_of_day": "17:00", "replaces_date": "2026-10-11"}
```

| Field | Type | Rule |
|---|---|---|
| `kind` | `"once"` \| `"from_now_on"` | Sheet scope "Just this once" / "From now on". |
| `date` | date | New session date, from today through today + 8 (local). |
| `time_of_day` | `"HH:MM"` | |
| `replaces_date` | date \| null | The session being moved (the `prep`/`after` step's session date). Null = an additional session. |

Semantics:
- `once`: append `{date, time_of_day}` to `custom_therapy_sessions` (dedupe). If `replaces_date` is a recurring occurrence, add it to `skipped_dates`; if it is a custom session, remove that one. `therapy_schedule` and `therapy_frequency` are never touched. (A one-off alone, without the skip, would leave a phantom session on the old date and fire its prep and after steps.)
- `from_now_on`: weekly/biweekly: the recurring entry matching `replaces_date`'s weekday and time moves to `date`'s weekday and `time_of_day`; other entries untouched; the biweekly anchor is recomputed so `date` is an on-week. Frequency `custom`: same as `once`. `replaces_date` null: add a recurring entry.
- Response: `200 TherapyScheduleResponse` (with `skipped_dates`). The client then refetches the plan (or uses it on the next Home load).
- Errors: `403 {"detail": "art9_consent_required"}`; `422` (bad format, date out of range, `{"detail": "replaces_date_not_a_session"}` when `replaces_date` matches no known session); `503 {"detail": "schedule_change_unavailable"}` while the `skipped_dates` column does not exist yet; any other unexpected failure is a 500 as in the rest of `users.py`. The client shows the existing error toast for 5xx.
- Storage of `skipped_dates`: new nullable `Text` column on `user_preferences` (JSON list), migration by backend-api, read through a guarded helper (excluded from the mapper like the `conversations` entry-flow columns, `models.py:583-591`), so `GET`/`PUT /therapy-schedule` keep working before the migration and simply report `skipped_dates: []`.

"It didn't happen" and "Not sure yet" never call this route; they call `POST /first-week/today/drop` (section 4) and leave the schedule as it is.

### 7.4 App version header (needed for the gate; none exists today)

Verified: the Dio client sends only `Authorization`, `X-PostHog-Distinct-ID` (`dio_client.dart:30-45`) and `Content-Type`/`Accept` (`dio_settings.dart:13-16`). No version header anywhere in `lib/` or `app/`.

| Header | Value | Use |
|---|---|---|
| `X-App-Version` | `PackageInfo.version`, e.g. `2.0.109` (pubspec `version:` name, `pubspec.yaml:19`; the same on both platforms) | The gate compares it as a numeric `major.minor.patch` tuple. |
| `X-App-Build` | `PackageInfo.buildNumber` | Informational only. Not comparable across platforms: Android and iOS numbers are derived separately (`codemagic.yaml:442-477`). |
| `X-App-Platform` | `ios` \| `android` | Informational. |

Client: read `PackageInfo.fromPlatform()` once (already a dependency, `pubspec.yaml:69`), cache it, and add the headers in the existing `onRequest` interceptor next to `X-PostHog-Distinct-ID` so they survive the 403 retry path (which copies `requestOptions.headers`). Backend: parse leniently (`^\d+\.\d+\.\d+$`, otherwise treated as absent); no user id in any log line that prints it.

---

## 8. `POST /api/v1/reflect/start` with `seed_source = "first_week_followup"`

Verified today:
- Route `reflect.py:790-968`, body `ReflectStartWithEntryRequest` (`schemas/reflect_first_conversation.py:20-29`) extending `ReflectStartRequest` (`schemas.py:1078-1094`): every field optional, `mode: "text" | "voice"`, `seed_source: Literal["prep_card", "recording", "between_session"]`, `seed_id: int`, `seed_label: str (<= 200)`, `entry: Literal["onboarding_first_conversation"]`. Not `extra="forbid"`.
- `ReflectSeedSource` enum (`models.py:469-478`) has the same three values; `conversations.seed_source` is `String(24)` (`models.py:562`), so `first_week_followup` (19 chars) fits without DDL.
- Response `ReflectStartResponse` (`schemas.py:1097-1105`): `{"conversation_id": int, "opening_question": str | null}`.
- Backend event `reflect_session_started` carries `seed_source` (`reflect.py:942-962`).

Change (additive):
- `ReflectStartRequest.seed_source` Literal and `ReflectSeedSource` gain `"first_week_followup"`. With it, `seed_id` and `seed_label` are ignored (the question is never taken from the client).
- The server resolves today's follow-up exactly as `GET /first-week/follow-up` (section 3, same display-time checks). Text mode: the question is persisted as Orca's first message the way the first conversation does it (`_persist_opening_message`, `reflect.py:523-548`), so `GET /reflect/{id}/messages` (`reflect.py:1467-1493`) returns it on resume, and `opening_question` in the response is that same text (the client renders it as the first bubble and does not render it twice). Voice mode: `opening_question: null`, `session_data` composes it live.
- The thread is an ordinary REFLECT thread (`seed_source = "first_week_followup"`, `seed_label` NULL); every user message counts against `reflect_messages` as usual (no exemption, 13.2).
- Quoted, generic and gentle questions all start with the same `seed_source`, the same `has_opening_question` (true for text, false for voice) and the same events (H-1, M-2).
- No open talk step today: an ordinary thread with no seed, 200 (never an error).
- SHOULD: within one plan day, an ACTIVE `first_week_followup` thread with no user message yet is returned instead of creating a second one (double tap).
- Ordering: a new client sending this value to an older backend gets 422 (Literal). Backend deploys first; the client still retries once without `seed_source` on 422.

---

## 9. Additive change to `GET /api/v1/users/usage`

Every `FeatureUsage` (`plan_usage.py:30-40`) gains `free_limit: int`, the Free number from the same settings (section 1.6 table), filled for every plan, including `trial` and `premium` where `limit` stays null.

```json
"reflect_messages": {"used": 3, "limit": null, "period": "month", "free_limit": 15}
```

Needed because the day-3 sheet runs during the trial (`limit` is null then) and the recap rhythm labels can be shown to trial or premium accounts, yet both must print the real Free numbers. Safe for every shipped client: `UserUsage.fromJson` reads only `used`, `limit`, `period` per feature and ignores other keys (`user_usage.dart:56-71`).

---

## 10. PostHog: which side emits what

Rule: each fact once, on one side. First-week endpoints emit nothing. Nothing below carries tone, variant, step, side card kind, question source or scores.

| Fact | Event | Side | Properties | Where |
|---|---|---|---|---|
| Today card seen | `today_card_viewed` | client | none or `plan_active` | Today card (new) |
| Today card CTA | `today_card_tapped` | client | none or `plan_active` | Today card |
| "Not today" | `today_card_deferred` | client | none | Today card |
| Plan card expand/collapse | `first_week_plan_toggled` | client | `expanded` | plan card |
| Hide plan / "I'll find my own way" | `first_week_plan_hidden` | client | none | plan card, recap |
| Side card CTA | `side_card_tapped` | client | none (no `kind`, no impression event) | side card |
| Side card dismiss | `side_card_dismissed` | client | none | side card |
| Reminder toggle result | `reminder_optin_result` | client | `result`: `on`/`off`/`denied_settings`, only after an explicit toggle and the OS result | day-0 card |
| Check-in saved | `quick_checkin_completed` | client | `areas_count`, `skipped_count` | check-in screen |
| Each score saved | existing `symptom_scored` | backend (`symptoms.py:631-641`) | `symptom_id`, `score_bucket` (pre-existing, see Q9) | do not add a client duplicate |
| Mirror next step | `checkin_next_step_tapped` | client | none (no `cta`) | mirror |
| Agenda item from mirror or quota card | none | none | none | `POST /workspace/agenda` emits nothing today |
| Follow-up thread created | existing `reflect_session_started` | backend (`reflect.py:942-962`) | `seed_source: "first_week_followup"` (same value for every question kind), `mode`, `has_opening_question`, etc. | do not add a client duplicate |
| Follow-up first message | `follow_up_started` | client | none | follow-up screen |
| Each Reflect message | existing `reflect_message_submitted` (client) and `reflect_message_sent` (backend, `reflect.py:1438`) | unchanged | as today | not touched by this feature |
| Prep / After / note created (step completion) | existing `prep_card_created`, `debrief_created`, `between_session_created` | backend | as today | no new event for "step done" |
| Session sheet completed | `session_sheet_completed` | client | none (outcome only in server-side aggregates) | session sheet |
| Schedule changed from the sheet | none per person | none | none | the sheet must NOT fire the existing client `therapy_schedule_updated` (`settings_cubit.dart:636-639`) |
| Art. 9 consent from the C card | existing `consent_granted {consent_type: ARTICLE9_HEALTH}` | backend only (`consent.py:212-218`) | as today | the client fires `consent_granted` only for `gdpr` (`therapy_onboarding_cubit.dart:387-389`); keep it that way |
| Day-3 sheet shown | existing `trial_reminder_sheet_shown` | client | as today (do not add `starter_shown`, Q6) | `trial_reminder_sheet.dart` |
| Day-3 sheet outcome | existing `trial_reminder_sheet_result` | client | `result`: existing values plus new `starter` (starter CTA tapped) | same |
| Starter offer opened from the sheet | existing `paywall_shown` / `subscription_screen_opened` | client | `trigger_feature: "trial_reminder_starter"` (new value, Q11) | via `subscriptionRouteWithTrigger` (`ms_routes.dart:252-253`) |
| "See Premium" on a quota card | existing `paywall_shown` | client | `trigger_feature: "today_card"` (new value, no step encoded) | Today card |
| Purchase completed | existing purchase events | unchanged | as today (`one_time_purchase_completed` backend `users.py:868` for the starter) | not touched |
| Recap opened | `first_week_recap_viewed` | client | none | recap |
| Rhythm kept | `rhythm_selected` | client | `count` (never option keys) | recap, rhythm sheet |
| "Not right" on recap | existing `orca_memory_item_deleted` / `orca_memory_delete_undone` / `orca_memory_action_failed` | client (`analytics_events.dart:851-867`) | as today | recap |
| Helpline link | none | none | none | gentle tone only |
| Plan-step reminder sent/opened | no per-person `moment.*` event; aggregate from `notification_logs` | backend | none | push payload has no `moment_type` |

### 10.1 Gap events added 2026-10-11 (operator approved implementing the gaps; shapes after `audit-security-events-2026-10-11.md`)

All client side, all enforced by the analytics guard with exact key and value sets. `status_class` is `unavailable` (503) or `error` (anything else, offline included); the follow-up also allows `not_found`, `first_week_action_failed` also allows `conflict` (409).

| Fact | Event | Properties |
|---|---|---|
| Undo inside the 5 s window: hide plan, recap own-way | `first_week_plan_hide_undone` | none |
| Undo inside the 5 s window: side card dismiss | `side_card_dismiss_undone` | none |
| Reminder time changed while on | `reminder_time_changed` | none (never the time) |
| "Open Settings" in the denied state | `reminder_open_settings_tapped` | none |
| Art. 9 step shown / declined, side card path only | `art9_consent_step_shown`, `art9_consent_declined` | none. Session sheet and Settings send nothing (the backend 403 is person-less by design, security E-M1); granting stays the backend `consent_granted` |
| Session sheet opened / closed with nothing accepted | `session_sheet_opened`, `session_sheet_dismissed` | none (never the entry) |
| Follow-up left without starting / failed / Quick check-in at 0 messages | `follow_up_dismissed`, `follow_up_failed`, `follow_up_check_in_tapped` | `status_class` on failed only |
| Recap left without action / failed / Retry | `first_week_recap_dismissed`, `first_week_recap_failed`, `first_week_recap_retry_tapped` | `status_class` on failed only (404 stays silent) |
| Check-in empty-state trends / abandoned | `checkin_empty_trends_tapped`, `quick_checkin_abandoned` | `areas_count`, `rated_count` on abandoned |
| Check-in baseline failed / Retry | `quick_checkin_load_failed`, `quick_checkin_retry_tapped` | `status_class` on failed (404 is `first_week_inactive`, silent) |
| Plan failed, Home fell back to legacy (once per process, never for 204) | `first_week_plan_failed` | `status_class` |
| A first-week mutation failed | `first_week_action_failed` | `action` (`defer`, `defer_undo`, `hide_plan`, `dismiss_side_card`, `set_reminder`, `set_rhythm`; never `drop`, security E-L1), `status_class` |

No event by design: schedule-change failures and the drop outcome (therapy proxy, server aggregates only), the rhythm sheet closed without saving (derivable from `rhythm_sheet_opened` without `rhythm_selected`), the check-in empty-state "Back to home" (`$screen`), offline failures of calls that are not first-week, the gentle-tone helpline link.

---

## 11. Impact on existing consumers and failure modes

### 11.1 Endpoints whose behavior changes

**`PUT /users/therapy-schedule` (403 without consent).** Flutter writers, all through `UsersManager.syncTherapySchedule` (`users_manager.dart:231-279`, `_dioClient.put`):
- `SettingsCubit._persistAndSyncSchedule` (`settings_cubit.dart:86-102`) from `addTherapySession` (`:569`) and `removeTherapySession` (`:584`), called by `therapy_schedule_section.dart:43,180` (Settings and My therapy, `/my-therapy` `ms_routes.dart:74`) and by Home's `session_setup_screen.dart:213`.
- `SettingsCubit._syncScheduleMetadata` (`settings_cubit.dart:110-121`) from `addCustomSession` (`:272`), `removeCustomSession` (`:289`), `updateTherapyFrequency` (`:626`), called by `custom_calendar_view.dart:109,141,269`, `therapy_frequency_selector.dart:45` and `session_setup_screen.dart:228`.
- `TherapyOnboardingCubit._clearSavedSchedule` (`therapy_onboarding_cubit.dart:701-710`): a full clear, stays allowed.
- `TherapyOnboardingCubit.saveScheduleAndAdvance` (`therapy_onboarding_cubit.dart:885-910`): the schedule screen is only reachable with Art. 9 consent (`therapy_onboarding_state.dart`, `therapyStepsVisible` requires `art9HealthConsentActive`), so unaffected.

What an old build does on the new 403 (no consent step): the interceptor resends once, `syncTherapySchedule` returns null, the user sees "Something went wrong" (`settings_cubit.dart:129-135`), and SharedPreferences keep the unsaved schedule, so Home's next-session card (read from prefs, `main_tab_cubit.dart:449-452`) shows a session the server does not have and no prep or after reminder fires. That is the cost the 13.8 count decides on; the version gate (7.1) avoids it for old builds. The backend has a single schedule writer (`crud.py:1497,1541`), so no backend job is affected by the 403.

**`POST /reflect/start` (new `seed_source` value).** Flutter callers `ReflectManager.startThread` (`reflect_manager.dart:16-21`, used by `reflect_chat_cubit.dart:269`) and `startThreadWithEntry` (`reflect_manager.dart:54-75`, used by `reflect_chat_cubit.dart:319` and `first_conversation_cubit.dart:296`) never send the new value: no change for them. PostHog insights that enumerate `reflect_session_started.seed_source` need the new value.

**`GET /users/usage` (additive `free_limit`).** Read only through `UsageManager.getUsage` (`usage_manager.dart:18-21`) into the tolerant `UserUsage.fromJson`; consumers via `UsageCubit`: `trial_popup_manager.dart`, `usage_gate.dart`, `trial_bar.dart`, `usage_chip.dart`, `reflect_usage_indicator.dart`, `reflect_tab_screen.dart`, `main_tab_screen.dart`, `main_page_cubit.dart`, `settings_cubit.dart`, `splash_screen.dart`. No change in behavior. `usage_snapshot` event unchanged.

**`GET /users/therapy-schedule` (additive `skipped_dates`).** Parsed by `TherapyScheduleResponse.fromJson` in `users_manager.dart:284-296` (unknown keys ignored by json_serializable). Next-session values now honor skips.

**Backend readers.** THERAPY_PREP, POST_SESSION_REFLECTION and THERAPY_APPOINTMENT must read the schedule through the consent-gated helper and honor `skipped_dates` (SPEC 5, backend-api).

### 11.2 Failure modes (client), SPEC 6 "Loading"

Hard rule: no first-week failure ever routes to onboarding, the paywall, sign-out or first-week copy.

| Situation | Client behavior |
|---|---|
| Plan: 204 | Legacy Home (no Today card, no plan card), exactly today's Home. |
| Plan: 401/403/404/5xx/503, timeout (6 s), offline, unparseable body, unknown `today.state`/`today.step`/`copy_key` | Legacy Home for this load; refetch on next resume. Never cached. |
| Plan: unknown `cta_route` | Card renders, CTA stays on Home. |
| Mutation fails (any non-200) | Keep the plan on screen, existing error toast (`MsMessage.showError`); on 409 refetch the plan. |
| Follow-up: non-200 | Ordinary new Reflect thread flow. |
| `reflect/start` with the new seed: 422 | Retry once without `seed_source`. |
| Check-in: one score fails | Keep the saved ones, offer retry; 404 for an area: skip it. |
| Recap: 404 | Back to Home. 503: error state with retry. |
| Memory delete: 404 | Treat as deleted. 503: keep the item, toast, `orca_memory_action_failed`. |
| Schedule write: `403 art9_consent_required` | Consent step; decline = store nothing and roll back the local cache. Any other 403: existing auth path. |
| Schedule change route: `503 schedule_change_unavailable` | Error toast, sheet stays open, nothing changed locally. |
| `/users/usage` fails | No chips, no quota lines, no day-3 sheet (fail closed), as today. |

---

## 12. Deploy order and rollback

1. Backend first (`feat/first-week-home` -> `main` auto-deploys), then `heroku run alembic upgrade head --app mindsync` immediately. Between the two, every first-week read answers 503 and the app shows the legacy Home; the new schedule-change route answers 503; boot is unaffected (guarded router import, String columns, guarded reads).
2. Verify on prod before any client ships: `GET /first-week/plan` with an old account returns 204; `/users/usage` carries `free_limit`; `PUT /users/therapy-schedule` gate matches the branch chosen in 13.8.
3. Frontend to `dev` (TestFlight) only after step 2. A frontend build against a backend without the router sees 404 and shows the legacy Home.
4. Config: `ART9_SCHEDULE_GATE_MIN_APP_VERSION` only if the version-gated branch is chosen (integration-devops adds it to `.env.example` and Heroku config).
5. Rollback: backend `git revert` + push (no down-migration needed: the new columns and tables are additive and unread by old code); the shipped client then gets 404 on first-week routes and shows the legacy Home. To switch off the Art. 9 gate without a deploy in the version-gated branch, set `ART9_SCHEDULE_GATE_MIN_APP_VERSION` to a version no build has (for example `99.0.0`).

---

## 13. Verified references (existing code this contract relies on)

| Item | Location |
|---|---|
| Router registration, guarded imports | `MindSync/app/api/v1/api.py:13,21,42-52,321`; mount `app/main.py:332` |
| Auth dependency, 401 detail | `app/api/deps.py:23-35`; FastAPI 0.111.0 `requirements.txt:34` |
| `GET /users/usage` | `app/api/v1/endpoints/users.py:1159-1177`; `app/schemas/plan_usage.py:30-66`; `app/services/plan_usage_service.py:56-185` |
| Free limits and gates | `app/core/config.py:188-190,201,266,269-270`; `app/crud/habit.py:46`; `app/api/v1/endpoints/_therapy_helpers.py:29-123` |
| Reflect limit 403, voice premium 403 | `app/api/v1/endpoints/reflect.py:1255,1911` |
| Therapy schedule GET/PUT, schemas, CRUD | `users.py:1620-1730`; `app/schemas/schemas.py:977-1070`; `app/crud/crud.py:1435-1600` |
| Consent endpoints and check | `app/api/v1/endpoints/consent.py:191-219,284-310`; `app/crud/consent.py:134`; `app/services/first_conversation.py:623-641` |
| Reflect start, seed enum, opening persistence, messages | `reflect.py:523-548,790-968,1467-1493`; `app/schemas/schemas.py:1078-1105`; `app/schemas/reflect_first_conversation.py:20-29`; `app/models/models.py:469-478,562` |
| Symptom scores | `app/api/v1/endpoints/symptoms.py:31,454-466,556-648`; `schemas.py:1533-1544,1567-1580` |
| Onboarding severity sync | `users.py:1440-1530`; `crud.py:3759-3816`; `crud.py:782-809` (reset) |
| Memory delete | `users.py:2055-2074`; `app/schemas/user_memory.py:30-52` |
| Memory and crisis helpers | `app/services/orca_memory.py:337,455,475,1424` |
| Weekly summary helpers | `crud.py:2441`; `app/services/openai_service.py:1128` |
| Workspace agenda create | `app/api/v1/endpoints/workspace.py:467-518`; `app/schemas/workspace.py:29-92` |
| Starter grant, receipts, cross-account guard | `users.py:801-836,868`; `app/models/models.py:768-780`; `app/services/subscription_service.py:44` |
| Push route table | `app/services/notification_routes.py` (`MOMENT_ROUTES`) |
| Flutter routes | `mindsync_app/lib/navigation/ms_routes.dart:56,71,74,86-88,126-131,183-196,252-253,288-292,298,309-319,380-384,401-422,510-516,607-625,723-727` |
| Push route resolver | `lib/utils/notification_route_resolver.dart:44-67` |
| Dio client and headers | `lib/api/dio_client.dart:27-83,141-186,193-256,321-350`; `lib/api/dio_settings.dart/dio_settings.dart:13-16` |
| Endpoint constants | `lib/api/dio_settings.dart/endpoints.dart:18,23-24,105,160,243,296,308` |
| Usage client | `lib/api/api_managers/usage_manager.dart:18-21`; `lib/api/models/users/user_usage.dart:51-78` |
| Trial sheet decision | `lib/managers/trial_popup_manager.dart:72,101-121,136`; `lib/screens/usage/trial_timing.dart:58-65` |
| Post-onboarding offer decision | `lib/screens/wow/cubit/wow_cubit.dart:395-437`; `lib/screens/wow/cubit/wow_state.dart:44-55`; `lib/services/push_prompt_policy.dart:77`; `lib/providers/purchases_data_provider.dart:110-139` |
| Schedule writers (client) | `lib/api/api_managers/users_manager.dart:231-296`; `lib/screens/settings/cubit/settings_cubit.dart:86-135,272-300,569-644`; `lib/screens/therapy_onboarding/cubit/therapy_onboarding_cubit.dart:701-710,885-910`; `lib/screens/main_tab/widgets/session_setup_screen.dart:213,228` |
| Reflect start (client) | `lib/api/api_managers/reflect_manager.dart:16-21,54-75` |
| Onboarding untouched default 5 | `lib/screens/therapy_onboarding/views/onboarding_intensity_view.dart:12,32-35` |
| Analytics constants | `lib/core/analytics/analytics_events.dart:494,499,506-525,851-867,915-919,957` |
| Agenda screen add flow | `lib/screens/workspace/agenda/agenda_full_screen.dart:108` |
| App version and build numbering | `mindsync_app/pubspec.yaml:19,69`; `mindsync-frontend/codemagic.yaml:442-477` |

---

## 14. Open questions (lead or operator)

1. **204 vs hidden plan.** This contract returns 204 only when there is no anchor; a hidden plan returns 200 with `plan_active: false` and an `open` Today card (SPEC 3.3, 13.1). SPEC 4's "hidden and no rhythm -> 204" would remove the Today card in week 1. Lead: confirm.
2. **"Not set" has no data source today.** Onboarding saves every untouched area as 5 (`onboarding_intensity_view.dart:12,32-35`), so the backend cannot tell an untouched 5 from a chosen 5. Recommended: onboarding stops sending untouched areas in `severity_ratings` (backend readers already use `.get()`: `crud.py:836-841`, `first_conversation.py:586-599`, `openai_service.py:4590-4600,8069`; the symptom is then created without a first score, `crud.py:3793-3815`), and `setup_score` is null for them. Alternative: an additive `severity_untouched` list. Lead with flutter-mobile and backend-api; also check the personal reveal screen, which reads the local ratings.
3. **Art. 9 gate branch (13.8).** Needs database-administrator's count of schedule edits without active consent (30 and 90 days). Small: unset `ART9_SCHEDULE_GATE_MIN_APP_VERSION`. Not small: set it to the first build with the consent step. The header (7.4) ships in that build either way.
4. **"Just this once" needs a skip store.** Today there is no way to cancel one recurring occurrence. This contract adds `skipped_dates` (new nullable column on `user_preferences`, migration by backend-api) and the narrow `POST /therapy-schedule/change`. Lead: confirm the new route instead of reusing the PUT.
5. **C side card and variant A.** SPEC 3.2 needs `currently_in_therapy` in (`yes_regular`, `yes_occasional`) for A. After Art. 9 consent from the C card, either the flow also asks and saves the therapy status (`PUT /users/profile`), or the engine treats a consented schedule as "in therapy". Lead/operator decide.
6. **Gentle tone and the starter offer.** SPEC 3.6 keeps the day-3 sheet in gentle tone and 13.3 now puts the starter offer on it; the 2026-10-03 lead decision says a crisis-flagged conversation shows no offer. If `starter_offer_eligible` becomes false in gentle tone, it must stay invisible in analytics (no `starter_shown` on `trial_reminder_sheet_shown`; the starter `paywall_shown` fires only on a tap). Operator decides.
7. **`note` when Free voice notes are used up.** SPEC 3.8 defines prep, after and talk only. Proposal used here: `today.note_quota_out` with CTA `/first-week/check-in` (same for B and C). brand-voice/ui-ux to confirm.
8. **Store setup of `ms_starter_package`.** Confirm it is a non-consumable on both stores. If it is consumable on Google Play, the store does not stop a second purchase; only the server check (same account) does.
9. **Pre-existing: scores reach PostHog.** `symptom_scored` sends `score_bucket` per person (`symptoms.py:31,631-641`), which contradicts audit I-1 ("scores never sent to PostHog"); the quick check-in will multiply it (up to 3 per check-in). security-guardian to rule before the WP-4 release.
10. **SPEC 5 correction.** Plan-step push `route` must be `/main-page`, not `/home` (section 2). backend-api to apply; no decision needed unless the lead prefers a new `/home` alias route in Flutter.
11. **New `trigger_feature` values.** This contract uses `trial_reminder_starter` (follows `post_onboarding` / `post_onboarding_all_plans`; the sheet's existing "Keep Premium" stays `trial_reminder`) and `today_card` for "See Premium" on quota cards. The operator's example was `trial_day3_sheet`. Confirm names before WP-2.
12. **Recap window and unhide.** Recap available plan days 7 to 14; no "show the plan again" path after hiding. Confirm both.
13. **Default reminder time.** Proposal: anchor local time rounded down to the half hour, clamped to 08:00 to 21:00, never earlier than 12 hours after the anchor for day 1 (SPEC 3.1). backend-api/ui-ux confirm.
14. **Version header and the PUT default.** Independent of this feature, consider making `TherapyScheduleUpdate.frequency` optional (null = untouched) so an omitted frequency stops resetting it to `weekly`. Not required here because the session sheet uses the new route.
15. **Home copy for the follow-up.** Home and pushes say "a question from your first talk", but a generic question (no memory item, skipped first talk) is not from the first talk. brand-voice-manager: one string that stays true for both (the `copy_key` is deliberately the same).

### 14.1 Lead resolutions, 2026-10-08 (binding for the build)

1. **Confirmed.** 204 only without an anchor. A hidden plan answers 200 with `plan_active: false` and an `open` Today card.
2. **Accepted.** Onboarding stops sending untouched areas in `severity_ratings`; `setup_score` is null for them ("Not set"). flutter-mobile runs recon on every reader of the local ratings (personal reveal screen included) and backend-api confirms every server reader tolerates a missing key. Existing accounts keep their stored values.
3. **Pending** the database-administrator count. Until then build both branches behind config. Default before the numbers arrive: a request WITHOUT `X-App-Version` (every build shipped today) is not gated; a request WITH it (builds that ship the consent step) is gated. `ART9_SCHEDULE_GATE_ALL_CLIENTS=true` switches to "gate everyone" without a deploy.
4. **Confirmed.** New `POST /users/therapy-schedule/change` plus the `skipped_dates` column. The recurring schedule is never overwritten by "Just this once".
5. **Lead decision.** When a schedule write succeeds with active ARTICLE9_HEALTH consent and `currently_in_therapy` is not already `yes_regular` or `yes_occasional`, the backend sets it: `yes_regular` for a recurring schedule, `yes_occasional` for a one-off session only. No extra question in the flow.
6. **Pending operator.** Provisional build rule: the day-3 sheet is shown in both tones (same `trial_reminder_sheet_shown`, no tone-dependent property); in gentle tone `starter_offer_eligible` is false; the sheet emits no offer impression event in either tone (starter `paywall_shown` only after a tap).
7. **Confirmed.** `today.note_quota_out` with CTA `/first-week/check-in` for B and C.
8. **Pending operator** (store console). backend-api keeps the same-account server check either way.
9. **Deferred to security-guardian** before the WP-4 release. The client `quick_checkin_completed` carries counts only.
10. **Confirmed.** Plan-step push route is `/main-page`.
11. **Confirmed.** `trial_reminder_starter` and `today_card`.
12. **Confirmed for v1.** Recap on plan days 7 to 14; no unhide path.
13. **Confirmed.** Default reminder time as proposed.
14. **Optional.** backend-api may make `frequency` optional in the same PR if the change is additive and tested; not required.
15. **Resolved in COPY.md:** "{orcaName} has a question for you" on Home and in-app; pushes use the neutral allowlist.

### 14.2 Additions after the build, 2026-10-11 (binding)

1. **Recap rhythm Free limits (section 5).** Each `rhythm.available[]` item gains `free_limits: [{"feature": QuotaFeature, "limit": int}]` with the real Free limits from settings, and `rhythm` gains `on_free: bool` (false when the plan cannot be read). The client prints the limit lines only when `on_free` is true. Additive.
2. **Recap codes.** 404 `{"detail": "recap_not_available"}` when there is no anchor or the plan day is outside 7 to 14. After any gentle-tone flag in the week, `where` and `noticed` are null (keys present).
3. **Schedule change 503.** `POST /users/therapy-schedule/change` answers 503 `{"detail": "schedule_change_unavailable"}` before migration m318 (as in 7.3), not `first_week_unavailable`.
4. **`resets_on`** stays the UTC calendar date of `resets_at` (section 1.6), because the counters reset at 00:00 UTC on the 1st.
5. **Mirror agenda text.** The client composes the agenda item from `firstWeek_checkInTitle` plus one line per rated area ("{area}: {setup} in setup, {today} today"), area labels included; it is the person's own encrypted agenda.
6. **Follow-up errors (sections 3 and 11.2).** A non-200 from `GET /first-week/follow-up` no longer opens the ordinary new-thread flow. The screen returns to Home: silently on 404, with the existing error toast on 503 and 5xx. Nothing routes to onboarding or sign-out.
7. **Plan card on day 0 and in the done state (SPEC 6).** The card is shown whenever `plan_active` is true. "Hidden on day 0 and in the done state" applies to the collapsed card's "Next" line only, as in the canvas (`hasNext` is false for `day0` and `done`).
8. **Art. 9 gate default (overrides 14.1 item 3 and the "unset" sentence in 7.1).** The WP-0 build already sends `X-App-Version` without any consent step, so the header alone cannot mean "gate me". With `ART9_SCHEDULE_GATE_MIN_APP_VERSION` unset and `ART9_SCHEDULE_GATE_ALL_CLIENTS` false, `PUT /users/therapy-schedule` gates nobody. After the first build with the consent step reaches TestFlight, the operator sets the minimum version to that build's version name. `POST /users/therapy-schedule/change` stays always gated.
9. **Follow-up question text (security audit WP-1..4, H-1).** The generic and calm cases use one fixed question per language ("How are you doing right now?"), so the stored length cannot tell them apart.
10. **Side cards add sessions through the existing setup screen (UX review M-5).** As section 2 already says, "Add session time" (B) and "Add sessions" (C) open `SessionSetupScreen`, after the Art. 9 consent step when consent is not active. They do not open the move-a-session sheet. Recurring schedules and every-two-weeks rhythms are then set up with the screen's own choices. The session sheet stays reserved for "Session moved?" and "It didn't happen".
11. **Free accounts with no Reflect messages left (UX review B-1).** On Free with the `reflect_messages` quota used up, the `rest` and `open` Today cards send `cta_route` `/first-week/check-in`, as `today.note_quota_out` already does. No first-week card ever leads to a paywall.
12. **`today.session_date` (sections 1.2 and 7.3).** Every Today card carries `session_date` (`"YYYY-MM-DD"` or null). It is non-null exactly when `today.links` is not empty (`prep` and `after` in `today` or `quota_out`), and equals the local start date of the session the step was built from. The client sends it as `replaces_date`. The change route reads the biweekly anchor in the user's zone, as the plan engine does.
13. **Rhythm Free limits in the plan (sections 1.2 and 14.2 item 1).** The plan's `rhythm` block carries the same `available[].free_limits` and `on_free` as the recap.
14. **`POST /first-week/today/drop` (section 4).** It also accepts an open `prep` step ("Session moved?" then "Not sure yet"): it drops the prep step and the not-done `after` step of the same session in one call. The schedule is never touched; repeat calls are no-ops; every other card answers `409 nothing_to_drop`.
