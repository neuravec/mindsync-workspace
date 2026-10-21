---
name: project-wp0-time-zones-2026-10-08
description: WP-0 time zones (first-week-home): one grammar in time_utils, parse_timezone stays pytz, resolve_tzinfo/local_date_at for new code, old-build offset artifacts UTC0-5 / UTC+010, branch fw/be0-tz commit 8739bb4 (not pushed)
metadata:
  type: project
---

WP-0 backend time zones, branch `fw/be0-tz` (off `feat/first-week-home`), commit `8739bb4`, NOT pushed (2026-10-08).

- `parse_timezone` MUST keep returning pytz-compatible objects: ~10 call sites use `.localize()` (time_utils itself, moment_hooks, periodic_summary, therapy_schedule_utils `_localize_naive`) and tests assert `tz == pytz.UTC` / `str(tz) == "Europe/Berlin"`. Zoneinfo validation + a zoneinfo-returning twin `resolve_tzinfo` share one grammar (`_resolve_spec`). New code (WP-1 plan engine) should use `resolve_tzinfo` / `local_date_at(day_starts_at_hour=4)`.
- **Why:** returning ZoneInfo from parse_timezone would break `.localize` across jobs and the two parallel notification branches.
- Old Flutter formats (settings_cubit changeSelectedLanguage builds `'UTC' + sign + '0' + hours`): negative offsets come out `UTC0-5`, +10..+14 as `UTC+010`. The validator added 2026-04-01 rejected both with 422, so those users' language change failed and reverted; before April they were stored and misread (UTC0-5 -> UTC, UTC+010 -> +1). Sync on app start sends `UTC+2` / `UTC-5` / `UTC+0`; storage normalizes to that same form so old builds do not re-PUT every launch.
- Follow-up commit `619d6c1` (same branch, not pushed): fixed every pytz `.replace(tzinfo=zone)` site (LMT offset, +01:24 Warsaw / -04:56 New York): `get_day_range_utc`, periodic_summary weekly SUN/MON, therapy_tracking `_debrief_matches_session` naive branch; plus the offset-carry pattern (field `.replace(hour=0/day=1)` on a pytz-aware now) in `get_recent_range_utc` and periodic_summary monthly. periodic_summary jobs are NOT scheduled (manual `app/run_daily_summaries.py` only).
- Last 3 offset-carry sites fixed in `68d62fa` on `fw/be0-tz2` (off merged `feat/first-week-home` 0f54bf0, not pushed) via new `time_utils.local_wall_time(reference, day, hour, minute)`: notification_service DND end (live via orchestrator `_adjust_for_dnd`), `_next_session_datetime_for_entry` (no prod caller), weekly_observations Monday midnight (latent: no tz zone changes DST on a Monday morning, scanned 2025-2027). tasks/* still do not pass `user_id` to parse_timezone.
- **How to apply:** when touching tz code, go through `app.utils.time_utils`; never `pytz.timezone(prefs.time_zone)` directly, never `.replace(tzinfo=pytz_zone)`, never `.replace(hour=...)` on a pytz-aware value to reach another day: use `local_wall_time` or `resolve_tzinfo`. Related: [[notification_service_patterns]].
