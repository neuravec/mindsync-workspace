# MSV3.12 Habit Tracker – API contract (lead-authored, v1, 2026-09-02)

Single source of truth for backend-api (implements) and flutter-mobile (consumes).
integration-devops verifies both sides against THIS file after implementation.
If backend-api must deviate, it edits this file AND reports the deviation to the lead.

Router prefix: `/api/v1/habits`. Auth: `get_current_user` (Firebase). Every row is scoped
to the caller. Cross-user or missing habit → 404 (never 403, matching the workspace precedent).

## Domain rules (server is the source of truth, client never recomputes)

- `type` is `"good" | "bad"`. Storage: `String(8)` column + Python constants (UploadSession pattern).
  NEVER a SQLAlchemy `Enum(PyEnum)`.
- A check row = success for that habit on that calendar day. Presence is the only state.
  For a bad habit a check means "stayed free of it today". No failure states exist anywhere.
- Day boundary = user's local midnight. Timezone source: `UserPreferences.time_zone`
  (fallback UTC). Reuse `app/utils/time_utils.py` (`get_todo_period_start_utc`,
  `get_calendar_week_range_utc`, `get_calendar_month_range_utc`, naive-vs-aware guards).
- Week = the user's preference-aligned week: `UserProfile.first_day_of_week`
  (default Monday). Same source `crud.workspace.get_user_period_context` already reads.
- Future dates are rejected server-side. Backdated writes are allowed (Edit mode corrects
  history). Backdating floor: 366 days before today. No floor at habit creation date
  (a habit created on Thursday may be back-filled for Mon-Wed; Darek: retro weeks pay XP).
- `current_streak` = consecutive checked days ending today, or ending yesterday if today
  is still unchecked (an unchecked today does not break the streak until the day ends).
  0 when neither today nor yesterday is checked.
- `month_summary` = `{checked, elapsed, month}` for the month of the window. `elapsed` =
  days from the 1st through today inclusive for the current month; = month length for a
  past month. Darek's example: "21/27 days".
- `week_complete` = all 7 days of the window's week are checked (week window). For the
  month window it refers to the current preference-aligned week containing `today`.
- Free tier cap: free account = 1 active habit, premium = unlimited. Count cap, refillable
  after delete. Premium check: `_therapy_helpers.is_user_premium(db, user_id)`.
- XP: when a habit-week becomes 7/7, award +10 XP on the ORCA track
  (`crud.award_orca_track_points`, the track the Character tab's PetHeroCard shows).
  Idempotent per (habit, week_start) via a ledger table `habit_week_awards`
  (unique `(habit_id, week_start)`, `xp_awarded` bool as the `xp_flag` source record).
  Un-checking a day later never claws XP back; re-completing never re-awards.
  Deleting a habit cascades checks + ledger rows; XP already in `user_leveling` stays.

## Shapes

```jsonc
// HabitResponse
{
  "id": 12,
  "name": "Drink water",              // 1..80 chars, trimmed
  "type": "good",                     // "good" | "bad"
  "sort_order": 0,
  "created_at": "2026-08-20T10:11:12+00:00",
  "checks": ["2026-08-24", "2026-08-25", "2026-08-27"],  // ISO dates INSIDE the window only, ascending
  "current_streak": 6,
  "month_summary": { "checked": 21, "elapsed": 27, "month": "2026-08" },
  "week_complete": false
}
```

```jsonc
// WindowInfo
{
  "kind": "week",                     // "week" | "month"
  "start": "2026-08-24",              // first day of the window (user tz, ISO date)
  "end": "2026-08-30",                // last day of the window (inclusive)
  "today": "2026-08-27",              // today in the user's tz
  "week_start_day": "monday",         // "monday" | "sunday" (user preference, default monday)
  "timezone": "Europe/Warsaw"
}
```

```jsonc
// LimitsInfo
{ "max_active": 1, "active_count": 1, "is_premium": false, "can_add": false }
// max_active is null for premium (unlimited)
```

## Endpoints

### GET /habits?window=week|month&anchor=YYYY-MM-DD
- `window` default `week`. `anchor` default = today (user tz); any date inside the wanted period.
- A window whose start is after today's period → `400 {"detail": "future_window"}`.
- 200:
```jsonc
{ "window": WindowInfo, "habits": [HabitResponse, ...], "limits": LimitsInfo }
```
- `habits` sorted by `sort_order` asc, then `id` asc. Archived habits are never returned.

### POST /habits
- Body `{ "name": "Drink water", "type": "good" }`
- 201 → `HabitResponse` (week window of today). New habit gets `sort_order` = max + 1.
- Free user already at cap → `403 {"detail": "premium_required"}`.
  backend-api: verify the exact `detail` string the app's other premium gates return
  and use THAT string; note it in this file if it differs.
- Empty / too long name, bad type → 422.

### PATCH /habits/{habit_id}
- Body `{ "name"?: string, "type"?: "good"|"bad" }` (at least one field)
- 200 → `HabitResponse` (week window of today).

### PUT /habits/reorder
- Body `{ "habit_ids": [12, 7, 3] }` – must be exactly the set of the caller's active habit ids, else 422.
- 200 → `{ "habits": [HabitResponse, ...] }` in the new order (week window of today).

### DELETE /habits/{habit_id}
- 204. Hard delete, cascades checks and week-award ledger rows.

### PUT /habits/{habit_id}/checks/{date}
- `date` = `YYYY-MM-DD` in the user's tz. Body `{ "checked": true|false }`. Idempotent PUT
  (explicit target state, not a toggle, so a double tap cannot flip twice).
- `date` after today → `400 {"detail": "future_date"}`.
  `date` older than 366 days → `400 {"detail": "date_too_old"}`.
- 200:
```jsonc
{
  "habit": HabitResponse,          // week window CONTAINING `date`
  "week_completed_now": true,      // true only on the transition to 7/7 in this call
  "xp_awarded": 10                 // 10 on the first-ever completion of that habit-week, else 0
}
```
- Setting the same value again → 200, `week_completed_now=false`, `xp_awarded=0`.

## Error summary
| Status | detail | When |
|---|---|---|
| 401 | (auth) | no / bad Firebase token |
| 403 | `premium_required` | free user creates a 2nd active habit |
| 404 | `habit_not_found` | habit missing or owned by another user |
| 400 | `future_date` / `future_window` / `date_too_old` | date rules above |
| 422 | (pydantic) | validation |

## AI context feed (CS-01 item 6)
- `crud.fetch_habit_context_for_prompt(db, user_id) -> str` (backend-api): compact text with
  each active habit (name, type, current streak, checks in the last 30 days as "N/30",
  full weeks completed). Empty string when the user has no habits. Never raises (log + "").
- Wired next to `fetch_todo_repeat_context_for_prompt` in `app/api/v1/endpoints/reflect.py`
  (backend-api) and into the session-preparation / weekly / monthly report prompt paths in
  `app/services/openai_service.py` (data-analytics, follow-up task).

## Frontend consumption notes (flutter-mobile)
- Weekly view: `GET /habits?window=week` on card load and after every mutation response
  (the mutation responses already carry the fresh `HabitResponse`, so a refetch is optional).
- Monthly view: `GET /habits?window=month&anchor=<first of month>`; paging back = anchor
  of the previous month; never page to a month after `window.today`'s month.
- Gate "+ Add habit" on `limits.can_add` BEFORE opening the sheet (no sheet flash);
  `can_add == false` → open the subscription screen.
- Show the "+10 XP" chip only when `xp_awarded > 0`; the mint wash when `week_completed_now`.
