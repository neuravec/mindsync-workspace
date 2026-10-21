# CS-01 Notification Audit — every push the backend can send, post-MSV3.2.2

**Author:** backend-api · **Date:** 2026-07-24 · **Spec:** MSV3.2.2 (Notifications & Settings Fix 1)

This is the CS-01 "audit every notification the app can send" deliverable. It
lists every push-capable code path in the backend as of this batch, its
trigger, schedule, controlling toggle, FCM tap route, and status. Anything
marked **NEEDS DAREK'S CONFIRMATION** is a live survivor outside the CS-03
13-row set whose target was NOT invented — per the spec's instruction, these
are flagged rather than guessed.

## A. The CS-03 13-notification set (all row numbers per the spec's list order)

| # | Type / MomentTypeEnum | Trigger | Schedule | Toggle (notification_toggles key) | FCM route | Status |
|---|---|---|---|---|---|---|
| 1 | `THERAPY_APPOINTMENT` | Next session known | T-24h and T-3h before start (Pass 2, schedule-driven) | `therapy_appointment` | `/main-page/tab/workspace?section=agenda` | spec-defined |
| 2 | `ADD_THERAPY_DATE` | No next session known | Daily at shared hour (18:00 local) while true (Pass 3) | `add_therapy_date` | `/settings?section=therapy_schedule` | spec-defined |
| 3 | `POST_SESSION_REFLECTION` | Session ended, no debrief yet | Fixed 75 min after session start (Pass 2) | `after_therapy` | `/fab/after-therapy` | spec-defined |
| 4 | `THERAPY_PREP` | Next session known, no prep card yet | T-24h and T-3h before start (Pass 2) | `prepare_for_therapy` | `/fab/prepare-therapy` | spec-defined |
| 5 | `BETWEEN_SESSIONS_NOTE` | Debrief done, next session > 3 days away, no note this cycle | Daily at shared hour while window active (Pass 3) | `between_sessions` | `/fab/between-sessions?new=true` | spec-defined |
| 6 | `RECORD_SESSION` | Next session known | ~8 min before start, delivered in the [-8,-3] min window (Pass 2 + 5-min delivery cadence) | `record_session` | `/fab/record-session` | spec-defined |
| 7 | `HOMEWORK_REMINDER` | Open therapist to-do exists | Exactly 3 days before session, at shared hour (Pass 3) | `homework` | `/main-page/tab/workspace?section=todo` | spec-defined |
| 8 | `MOOD_UPDATE_REQUEST` | No SymptomScore in 3+ days (rolling) | Shared hour, every 3 further stale days (Pass 3) | `mood_trends` | `/main-page/tab/main?section=mood_trends` | spec-defined |
| 9 | `REFLECTION_INVITATION` | No REFLECT conversation this Mon-Sun week | Sunday at shared hour (Pass 3) | `reflect` | `/main-page/tab/reflect?new=true` | spec-defined |
| 10 | `GOALS_WEEKLY` | Weekly goal-narrative regen completes | Event-anchored (goal_narrative.py hook) + night rule | `goals` | `/main-page/tab/workspace?section=goals` | spec-defined |
| 11 | `THERAPY_RELATIONSHIP_CHECKIN` | No TherapyHealthCheck this Mon-Sun week | Sunday at shared hour (Pass 3) | `therapy_relationship` | `/health-check` | spec-defined |
| 12 | `WEEKLY_SUMMARY_READY` | WeeklyTherapySummary card created | Event-anchored (weekly_therapy_summary.py hook) + night rule | `weekly_summary` | `/therapy/weekly-summary/{id}` | spec-defined |
| 13 | `MONTHLY_SUMMARY_READY` | MonthlyTherapyAudit created | Event-anchored (monthly_therapy_audit.py hook) + night rule | `monthly_summary` | `/therapy/monthly-audit/{id}` | spec-defined |

## B. System notification (not in the CS-02 toggle list)

| Type / MomentTypeEnum | Trigger | Schedule | Toggle | FCM route | Status |
|---|---|---|---|---|---|
| `ACCOUNT_SETUP_NUDGE` (CS-07) | Account created, no UserGoal yet | t+24h/48h/72h/96h, up to 4 touches (Pass 3), only-future | none (master `notification_enabled` only) | `/main-page/tab/workspace?section=goals&setup=true` | spec-defined |

## C. Survivors outside the CS-03/CS-07 set (kept, unchanged sending logic)

| Type / MomentTypeEnum | Trigger | Toggle | FCM route | Status |
|---|---|---|---|---|
| `MOOD_DIP_ALERT` | Sustained symptom-score dip pattern (Pass 1, scored) | none (interest-filter exempt was already narrowed; no CS-03 row) | `/main-page/tab/main?section=mood_trends` (CS-01 retarget — was the `/main-page` placeholder) | **kept-needs-Darek-confirmation** — this row has no CS-03 analogue; route content-matches Mood Trend but was never explicitly named in this spec |
| `RE_ENGAGEMENT` | 3+ days inactive (Pass 1, scored, own `re_engagement_push` toggle) | `re_engagement_push` (separate legacy column, not a CS-03 toggle) | `/main-page` | **kept-needs-Darek-confirmation** — explicitly flagged by the lead's brief; `/main-page` is a generic landing, not an input-card anchor |
| `session_recording_ready` (direct FCM, not a NotificationMoment) | Session recording finishes processing | none | short-code `session_recording_ready`, resolved client-side to the Timeline tab (`lib/utils/notification_route_resolver.dart`) | spec-defined / kept — CS-01 explicitly named this an already-correct mapping (MSV3.2Fix.1 A10); unchanged |

## D. Historical-only moment types (enum members kept, no generator produces them)

| Type / MomentTypeEnum | Why retired | Status |
|---|---|---|
| `PATTERN_INSIGHT` | CS-04 — Insights push deleted | deleted (generator removed 2026-07-24); enum kept for historical rows |
| `STREAK_CELEBRATION` | CS-04 — Streaks push deleted | deleted (generator removed 2026-07-24); enum kept for historical rows |
| `DAILY_CHECK_IN` | Retired baseline-fallback cadence, superseded by the CS-03 deterministic set | deleted (generator removed 2026-07-24); enum kept for historical rows |
| `SESSION_MORNING_OF` | Superseded by `THERAPY_APPOINTMENT` (row 1) and `RECORD_SESSION` (row 6) | deleted (generator removed 2026-07-24); enum kept for historical rows |
| `WEEKLY_RECAP`, `ACHIEVEMENT_UNLOCK` | Never had a live generator (pre-existing, before this batch) | dead-code (enum members with no producer; unrelated to this batch) |

## E. Dead code — no scheduler/worker path reaches these (audit-only, not touched)

| Function | Location | Why it never fires in prod |
|---|---|---|
| `notify_summary_notification` | `app/services/notification_service.py` | Called only from `app/services/periodic_summary.py`, which is called only from `app/run_daily_summaries.py` — a standalone script not registered in `app/core/rq_scheduler_setup.py` or listed in the `Procfile`. Dead in the deployed web/worker/scheduler dynos. |
| `_process_first_nudges`, `_process_followup_nudges` | `app/services/notification_service.py` | Zero callers anywhere in the codebase (grep-verified). Pre-existing dead code, unrelated to this batch; left in place per the lead's "delete only if trivially safe" guidance — removal is a separate cleanup, not required for this spec. |

## F. CS-01 payload contract (applies to every NotificationMoment-based push above)

`app/tasks/notification_orchestrator_job.py::deliver_due_moments` sends FCM `data`:

```json
{
  "type": "notification_moment",
  "moment_id": "<str(moment.id)>",
  "deep_link_route": "<moment.deep_link_route>",
  "route": "<moment.deep_link_route>"
}
```

`route` now carries the REAL target for every moment type (rows 1-13, CS-07,
and the survivors in section C) — the previous `/moment/{id}` generic-sheet
indirection is retired app-wide, not only for the new rows. `deep_link_route`
is kept alongside `route` (identical value) for backward compatibility with
any other reader of this payload (e.g. the in-app `/moments/upcoming` poll).

Route strings are centralised in `app/services/notification_routes.py`
(`MOMENT_ROUTES` dict + `route_for()` helper) — see that module for the full
list and the CS-01 anchor each maps to.

## Items flagged NEEDS DAREK'S CONFIRMATION (per CS-01: "stop, list it, confirm before inventing")

1. **`RE_ENGAGEMENT`** — route stays `/main-page` (a generic landing, not an
   input-card anchor). This row predates MSV3.2.2, is not part of the CS-03
   13-row set, and the lead's brief explicitly called it out as needing
   Darek's target confirmation rather than a guessed retarget.
2. **`MOOD_DIP_ALERT`** — retargeted to
   `/main-page/tab/main?section=mood_trends` on a content-matching basis
   (same anchor as CS-03 row 8) since it has no CS-03 row of its own. Flagged
   for veto per the lead's brief.

## Flagged-for-veto decisions from this batch (see full report to the lead for detail)

- Row 6 delivery-cadence tradeoff: `deliver_due_moments` cron tightened from
  `*/15` to `*/5` (roughly triples delivery-job invocation volume) so
  RECORD_SESSION's tight [-8,-3] min window reliably lands before session
  start.
- Row 6's exception to the strict only-future rule: a target already past
  (but session not yet started) clamps to "now" instead of being dropped.
- Row 10's night-rule extension: the spec defines the 21:00-08:00 delay rule
  for rows 12/13 only; applied here to row 10 too since the weekly goal job
  runs at a fixed UTC hour (Sun 04:00) that can land at any local hour.
- CS-06 interpretation scope: DND/quiet-hours retirement applied to the
  CS-03 13-row set (Pass 2/Pass 3) only. Pass 1 survivors (`MOOD_DIP_ALERT`,
  `RE_ENGAGEMENT`) keep their existing `_adjust_for_dnd` call, since their
  logic is explicitly "kept, unchanged" per the spec's disposition list.
- `notification_toggles` master-off behaviour: turning `notification_enabled`
  off does NOT clear the stored per-row `notification_toggles` (unlike the
  legacy JSON boolean pattern, which zeros every legacy key). This preserves
  the user's row-level choices across a temporary opt-out/opt-in cycle — a
  considered improvement over the legacy pattern, not spec-mandated either
  way.
