# MSV3.2 Fix.1 — API contract, slice A2 (data-analytics)

> Companion to `API_CONTRACT_Fix1.md` (PHASE A's main contract file, which this
> agent was told NOT to edit). Covers the FINAL implemented shapes for the
> sections owned by this slice: §5 (symptoms/mood trend), §6 (summaries),
> §7 (goals), §8 (therapy relationship), §9 (notifications). FE phases (C, F)
> should read this file for these sections instead of the `TBD` placeholders
> in the main contract file.
>
> Repo: `MindSync/`, branch `main`, commit `c878e9f` (local, NOT pushed).

---

## §5. Mood Trend / Symptoms

### `GET /api/v1/symptoms/` — list (existing, unchanged shape + 1 new field)
Query: `visible_only: bool = false`
Response: `List[SymptomCardResponse]`
```jsonc
{
  "id": 1,
  "name": "Anxiety",
  "is_custom": false,
  "display_order": 0,
  "is_visible": true,
  "current_score": 6,
  "ai_description": "It eased a little this week.",
  "ai_description_generated_at": "2026-03-05T08:00:00Z",
  "last_updated_at": "2026-03-05T07:55:00Z",   // NEW — most recent SymptomScore.created_at, null if no scores
  "scores_count": 12,
  "scores": [ { "id": 1, "score": 6, "created_at": "2026-03-05T07:55:00Z" }, ... ]
}
```
`SymptomResponse` (returned by create/update/get-by-id) gained the same
`last_updated_at` field.

### `GET /api/v1/symptoms/trend` — Main tab widget (existing, + 1 new field)
Response: `SymptomTrendResponse { symptoms: SymptomTrendItem[] }`
```jsonc
{
  "id": 1, "name": "Anxiety", "current_score": 6, "direction": "down",
  "sparkline_scores": [7, 7, 6, 6],
  "last_updated_at": "2026-03-05T07:55:00Z"   // NEW
}
```

### `POST /api/v1/symptoms/{id}/scores` — add/update score (AUDITED, unchanged, confirmed working)
Request: `{ "score": 1-10 }` → 201 `SymptomScoreResponse`.
**Backend audit result: no bug found.** `crud.add_symptom_score` has no
gating on `is_visible`, no unique constraint blocking repeated scores same
day, router is mounted at `/symptoms` (defensive try/import in `api.py`,
confirmed importable). The reported "can't add new scores" is very likely a
**FE wiring gap**: the old Stats screen called this endpoint; confirm the
new Main-screen Mood Trend widget actually calls it (symptom `id` is present
in both `/symptoms/` and `/symptoms/trend` responses, so nothing new is
needed to wire it). **Action for Phase C**: verify/wire tap-to-score against
this pre-existing endpoint; report back if a genuine backend gap is found on
manual test — none found by code trace.

Side effect (NEW, MSV3.2Fix.1 A8): on a user's **first-ever** symptom score
(no `MoodTrendSummary` row yet for the user), enqueues an event-driven Mood
Trend AI Summary generation (see §5 AI Summary below) instead of waiting for
the next daily batch tick. No behavior change for users who already have a
summary — steady-state cadence is still the daily batch.

### Per-symptom narrative — CONTENT rewritten (mechanics/timing unchanged)
Same field (`ai_description` on `/symptoms/*`), same trigger mechanics
(`POST /symptoms/{id}/refresh-description`, `POST /symptoms/refresh-all-descriptions`,
stale-check via `last_score_id_at_generation`). **Content only** changed:
- Banned (regression-tested): point deltas between two specific dates/scores,
  reciting score history as a list/timeline, any add-a-note/journal/"keep
  tracking to see what's linked" suggestion.
- Required: qualitative magnitude wording ("rose sharply", "eased a little",
  "held steady"...), grounded in the score trend **and** recent app-activity
  context (session topics / between-session note topics, last 30 days) when
  available — new `_gather_recent_activity_context()` helper in
  `symptoms.py`, feeds an extra `"Recent app activity (context only): ..."`
  block into the AI input when non-empty.
- PL+ENG: driven by the existing `"Language:"` line in the AI input (system
  prompt now explicitly instructs the model to respect it, including for the
  two low-data fallback lines).

### AI Summary of all symptom change (`GET /api/v1/dashboard/mood-trend`, unchanged shape)
```jsonc
{
  "bullets": ["...", "...", "...", "...", "..."],   // <=5, no bullets *within* each string
  "summary_generated_at": "2026-03-05T08:00:12Z",
  "last_entry_date": "2026-03-05",
  "days_since_last_entry": 0,
  "needs_update_prompt": false                       // true when days_since_last_entry >= 3
}
```
Generation mechanics unchanged (daily batch at each user's local 8am,
`app/tasks/mood_trend.py`), **plus** the new first-time bootstrap described
above (`regenerate_mood_trend_summary_for_user`, event-driven, RQ
fire-and-forget from `add_score`, bypasses the local-hour gate for that one
call only). `needs_update_prompt` and `days_since_last_entry` are already
live-computed every request (no caching) — FIX.03's reported staleness
("Nie dodałeś od kilku dni notatki" never disappearing) is a **FE-only
box** per spec (explicitly slated for deletion, not relocation) — nothing
in this endpoint's data was ever stale; only the now-defunct standalone box
was.

---

## §6. Timeline weekly & monthly summaries

### Root cause of the reported "Generate Now" raw 500
Two contributing issues, fixed together:
1. **Confirmed by code trace**: in both `weekly_summaries.py` and
   `monthly_audits.py`, the entire data-gathering + PROCESSING-row-creation
   "prep" phase of `/generate` and `/retry` ran **outside any try/except**.
   Any exception there (bad window math, a decode failure deep in
   `crud.gather_weekly_summary_data`, a transient DB hiccup) reached the
   client as a genuinely raw, bodyless 500 — this is the literal, reproducible
   bug matching "throws an on-screen error 500."
2. **Plausible, defensively fixed**: `WeeklyTherapySummaryResult.limited_data`
   and `MonthlyTherapyAuditResult.limited_data` carried a bare Python
   `default=False`. OpenAI's structured-output strict JSON schema mode
   (`openai_client.beta.chat.completions.parse()`) is documented to reject
   schemas with unsupported keywords, and Pydantic renders a field default as
   a `"default"` key in the schema `to_strict_json_schema()` produces. This
   could never be caught by CI (tests mock the AI call directly, bypassing
   real schema validation). Fixed by making the field required — the AI
   already always sets it per the prompt's own instructions, so zero
   behavior change, pure risk removal. Regression-locked in
   `test_fix1_summaries_error_envelope.py` (`to_strict_json_schema()` on both
   models now asserted to never contain a `"default"` key anywhere).

**We could not reproduce against the live OpenAI API** (project rule: no
live API experiments) — item (1) is the concrete, code-provable fix; item
(2) is a real, low-risk hazard removed defensively. If "Generate Now" still
errors after this fix ships, the structured envelope below will now at
least surface the real error server-side (full traceback in logs via
`exc_info=True`) instead of a bodyless 500 — please forward the
`error_code` if it recurs.

### `POST /api/v1/weekly-summaries/generate` (unchanged happy-path response shape)
Success: 200 `WeeklyTherapySummaryResponse` (unchanged).
**Error envelope (NEW — was a bare-string `detail` before, now structured):**
```jsonc
// HTTP 500
{
  "detail": {
    "error_code": "weekly_summary_prepare_failed" | "weekly_summary_generation_failed",
    "message": "Could not prepare your weekly summary right now. Please try again." | "AI generation failed. Please try again later.",
    "retryable": true,
    "summary_id": 42          // present only for *_generation_failed (row exists, marked FAILED)
  }
}
```
Retry semantics: `prepare_failed` → no row was created, safe to call
`/generate` again. `generation_failed` → the row exists with
`processing_status: "FAILED"`; call `POST /weekly-summaries/{summary_id}/retry`
(same envelope shape on failure; `error_code: "weekly_summary_retry_prepare_failed"`
for a prep-phase failure during retry).

### `POST /api/v1/monthly-audits/generate` / `/{id}/retry` — same pattern
Error envelope identical shape, `error_code` values:
`monthly_audit_prepare_failed`, `monthly_audit_generation_failed`,
`monthly_audit_retry_prepare_failed`. `audit_id` present for
`*_generation_failed`.

### Content: "is my approach working / better-worse-neutral"
- **Weekly**: `at_a_glance` now explicitly closes with a plain-language
  verdict (e.g. "Overall this points toward things feeling a bit easier than
  last week"), instructed via the system prompt — no new field, still one
  string.
- **Monthly**: `movement_assessment` + `movement_type` (`visible`/`mixed`/
  `limited`) already covered this — audited, unchanged.

### Auto-generation at period end
**Already implemented before this batch** — confirmed by code trace, not
re-implemented:
- `app/core/rq_scheduler_setup.py::setup_hourly_weekly_therapy_summary()` —
  hourly cron, generates for users whose local hour is >=22 the evening
  before a therapy day (idempotent per-window, `<2h` dedup guard).
- `app/core/rq_scheduler_setup.py::setup_monthly_therapy_audit()` — hourly
  cron, generates on days 1-3 at local hour 6 (idempotent per report-period).
- Both registered from `app/main.py` lifespan (`setup_hourly_weekly_therapy_summary()`
  and `setup_monthly_therapy_audit()` calls, verified present in source).
- "Generate Now" stays as the manual trigger, unchanged.

---

## §7. Goals — narrative ad-hoc refresh

### `POST /api/v1/goals/{id}/refresh` (AUDITED, already implemented, unchanged)
Response: 200 `GoalResponse` (current state, returned **immediately** —
regeneration is async via RQ, same pipeline `regenerate_goal_narratives`
uses for every other trigger).
- **Cache hit** (context `data_hash` unchanged AND `processing_status ==
  COMPLETED`): returns the current goal as-is, no AI call, no enqueue.
- **Cache miss**: enqueues `regenerate_goal_narratives(user_id,
  "manual_refresh", goal_id)`, returns current (stale) state immediately —
  FE should show a loading state on the narrative area per spec, then
  re-fetch (poll `GET /goals/{id}` or re-list) to pick up the new narrative.
- **Failure semantics (regression-locked in
  `test_fix1_goals_notifications_therapy_relationship.py`)**: on AI failure
  (including after the internal one retry), `regenerate_goal_narratives`
  calls `crud.update_goal_narrative` with **only**
  `{"processing_status": "FAILED"}` — the `ai_narrative` key is never
  included, so the previously-stored narrative is never overwritten. FE
  contract: poll and if `processing_status == "FAILED"`, show a toast with a
  retry action that re-calls `POST /{id}/refresh`.
- 404 if the goal doesn't exist / isn't owned by the user.

No code changes were needed for A9 — audit + regression test only.

---

## §8. Therapy Relationship

### Per-check-in rating values (AUDITED, already exposed, unchanged)
Every `HealthCheckResponse` (from `/submit*`, `/latest`, `/history`,
`/{id}`) already carries:
```jsonc
{
  "relationship_state": "green" | "amber" | "red" | "safety_escalation",
  "state_label": "Feeling connected",   // human-readable, language-aware
  ...
}
```
**Color mapping for FE**: spec's "red/yellow/green" maps to
`red` → red, `amber` → **yellow** (spec's wording, backend's field value is
literally `"amber"` — do not expect a `"yellow"` string from the API),
`green` → green. `safety_escalation` is a 4th state (crisis pre-scan or
`safety_score == 1`) — FE should render it as the most urgent visual
treatment (e.g. red + a distinct icon/badge), not conflate it with plain
`red`. Scoring/color computation itself (`compute_relationship_state` in
crud.py) is **unaudited/untouched** per spec ("already works").

**Module-level icon on the Workspace overview** = the `relationship_state`
of the **latest** check-in — use `GET /health-check/latest` (404 if none
yet; treat as "no rating yet" state, not an error).

### `GET /api/v1/health-check/status` — Main prompt gating (1 field ADDED)
```jsonc
{
  "is_due": false,
  "next_due_date": "2026-03-15T00:00:00Z",
  "total_completed": 3,
  "days_until_due": 10,
  "first_check_in_available": false,
  "banner_dismissed": true,
  "current_streak": 2,
  "longest_streak": 2,
  "should_show_main_prompt": false   // NEW — see below
}
```
**`should_show_main_prompt`** (NEW field, Main's CS-08 conditional module
should gate on this, not on `is_due`/`banner_dismissed` directly):
`is_due AND NOT banner_dismissed`, computed **live** on every request from
the latest COMPLETED `TherapyHealthCheck` — no caching layer anywhere in
this chain.

**Audit finding (FIX.04 "doesn't dismiss after completion")**: no backend
caching/staleness bug found. `is_due` and `banner_dismissed` (via
`crud.compute_health_check_due_date` / `crud.is_banner_suppressed`) both
recompute from scratch on every call, reading the latest COMPLETED
check-in's `created_at`. Submitting **any** check-in
(`/submit`, `/submit-voice`, `/quick-check`, `/quick-check-voice`) always
ends with `processing_status = COMPLETED` (even on AI failure, which falls
back to a canned observation rather than leaving the row stuck) — so the
very next `GET /health-check/status` call is guaranteed to return
`should_show_main_prompt: false`.

**Recommendation for Phase C**: after a successful submission response,
either (a) optimistically hide the prompt client-side immediately, or (b)
re-fetch `GET /health-check/status` right after submit succeeds — do **not**
rely on a cached/stale copy of the status fetched before submission. If the
prompt is still observed not to dismiss after this is wired correctly,
it is very likely the **CS-02 iOS voice bug** for `submit-voice` /
`quick-check-voice` specifically (transcription failing silently before a
COMPLETED row is ever created) — not a status-endpoint bug; see §A13 notes
in `STATUS_A2.md`.

---

## §9. Notification deep-link payloads — full type → payload table

**Delivery mechanism note**: two independent send paths exist. (1) The
**Notification Moments framework** (`app/tasks/notification_orchestrator_job.py::deliver_due_moments`,
runs every 15 min) is the primary, currently-live path — 11 of 13
`MomentTypeEnum` values have an active generator registered. (2) A handful
of **direct `send_fcm_to_all_user_tokens` calls** outside the moments
framework, audited individually below.

### (1) Notification Moments framework — ALL types, uniform payload
Every moment, regardless of `moment_type`, is delivered with:
```jsonc
{
  "type": "notification_moment",
  "moment_id": "123",
  "deep_link_route": "<generator-specific, legacy — kept for backward compat>",
  "route": "/moment/123"   // <- FE resolver reads this; always wins over deep_link_route
}
```
This was fixed in a prior commit (`12543e3`, before this A2 slice) —
audited here, confirmed correct, not re-touched. `/moment/{id}` is a
dedicated deep-link screen that resolves further internally by
`moment_type`. Active generator types (registered, will actually fire):

| `moment_type` | Generator file | In-app `payload.primary_cta.route` (pre-delivery-override) |
|---|---|---|
| `DAILY_CHECK_IN` | `moments/daily_check_in_generator.py` | variant-dependent (`self._cta_route`) |
| `REFLECTION_INVITATION` | `moments/reflection_invitation_generator.py` | variant-dependent |
| `SESSION_MORNING_OF` | `moments/session_morning_of_generator.py` | `/therapy/prep-card/{id}` or `/fab/prepare-therapy` |
| `THERAPY_PREP` | `moments/therapy_prep_generator.py` | `/therapy/prep-card/{id}` or `/fab/prepare-therapy` |
| `POST_SESSION_REFLECTION` | `moments/post_session_reflection_generator.py` | `/therapy/between-sessions/new` |
| `RE_ENGAGEMENT` | `moments/re_engagement_generator.py` | `/main-page` |
| `MOOD_DIP_ALERT` | `moments/mood_dip_alert_generator.py` | `/exercises/breathing/quick` or `/symptoms/log` |
| `PATTERN_INSIGHT` | `moments/pattern_insight_generator.py` | variant-dependent |
| `STREAK_CELEBRATION` | `moments/streak_celebration_generator.py` | `/character/streaks` |
| `MOOD_UPDATE_REQUEST` | `moments/mood_update_request_generator.py` | `/main-page` |
| `THERAPY_RELATIONSHIP_CHECKIN` | `moments/therapy_relationship_checkin_generator.py` | `/health-check` |

(The `payload.primary_cta.route` column only matters for any in-app
surfaces that read the stored `payload` directly, e.g. `/moments/upcoming`
polling or a moment-detail sheet's own CTA button — the **push tap** always
uses the delivery-time override `route: "/moment/{id}"` above, regardless of
this column.)

| `moment_type` (no active generator — DEAD, do not build FE handling around them) |
|---|
| `WEEKLY_RECAP` — enum value exists, no generator registered |
| `ACHIEVEMENT_UNLOCK` — enum value exists, no generator registered |

### (2) Direct-send paths (outside the moments framework)

| Source | `notification_type` | `data` payload | Status |
|---|---|---|---|
| `app/tasks/session_recording.py::_post_success_jobs` | `session_recording` | `{"route": "session_recording_ready", "type": "session_recording", "recording_id": "<id>"}` | **LIVE.** `"session_recording_ready"` is a short-code the FE resolver (`notification_route_resolver.dart`) explicitly maps to the Timeline tab (`MsRoutes.mainPageTherapyTabRoute`) — correct, audited, unchanged. `recording_id` added this batch (additive) so a future FE revision can deep-link to the exact card instead of just the tab. |
| `app/api/v1/endpoints/admin_broadcast.py` → `app/tasks/broadcast.py::execute_broadcast` | n/a (operator-controlled) | Whatever `data` dict the admin operator supplies in the `POST /admin/broadcast` request body (optional, freeform) | **LIVE**, admin-triggered only. No fixed route by design — this is a marketing/announcement tool. Contract: if the operator wants tap-through routing, they must include a `route` key resolvable by the FE resolver (a full path, e.g. `/main-page`) in the request; omitting it means the tap opens the app with no deep-link (FE default fallback). Not a bug. |
| `app/services/notification_service.py::notify_summary_notification` (called from `app/services/periodic_summary.py` daily/weekly/monthly/yearly summary jobs) | `summary_ready` | `{"route": "/main-page", "type": "summary_ready"}` | **DEAD / UNSCHEDULED.** `periodic_summary.py`'s `generate_daily_summaries` etc. are only invoked from `app/run_daily_summaries.py`, a standalone script not referenced by the Heroku `Procfile` (`web`/`worker`/`scheduler` only) nor by `app/core/rq_scheduler_setup.py`. Zero production reachability confirmed by grep. Generic `/main-page` routing here genuinely matches the CS-06 "Now (wrong)" complaint pattern, but has zero current user impact — **left unfixed, flagged here** in case this code path is ever resurrected; do not build FE handling assuming it fires. |
| `app/services/notification_service.py::_process_first_nudges` / `_process_followup_nudges` (post-session nudge) | `post_session_nudge` / `post_session_nudge_followup` | `{"route": "/fab/after-therapy", "type": "post_session_nudge", "therapist_name": "...", "session_date": "..."}` | **DEAD / SUPERSEDED.** The hourly cron entry point that called these (`notify_post_session_nudge`) was removed in Notification Cadence v3 (2026-07-03), superseded by `POST_SESSION_REFLECTION` in the moments framework (see table above). Confirmed by an explicit comment left in `app/tests/test_post_session_nudge.py`. The two functions still exist and are still unit-tested directly, but are not reachable from any scheduler entry point. Route shape (`/fab/after-therapy`) was already specific/correct, not generic — no action needed even if resurrected. |

### FE resolver contract reference (read from the FE repo, unchanged by this batch)
`lib/utils/notification_route_resolver.dart::resolveNotificationRoute(data)`:
reads `data['route']`, falls back to `data['deep_link_route']`. Recognizes
short-codes `prep_card` (+`prep_card_id`), `prep_card_create`, `moment`
(+`moment_id`), `session_recording_ready`; anything else is treated as an
already-full path and returned as-is. `null`/missing → FE falls back to its
own default (Main).

---

## Deviations from `API_CONTRACT_Fix1.md`'s §5-§9 skeleton
None structurally — all additions are purely additive fields/behaviors on
existing endpoints; no endpoint paths, methods, or existing field
types/names changed. See `STATUS_A2.md` for the full items-done list, schema
requests (none needed), and A13 audit findings for PHASE B.
