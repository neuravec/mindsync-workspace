# First-week design aggregates (prod Postgres), 2026-10-07

**Status: NOT EXECUTED. Results pending.** No numbers in this file come from prod yet.

**Blocker:** the Heroku CLI on the operator machine (`heroku/11.11.0 win32-x64`) is not authenticated. `heroku auth:whoami` returns `not logged in`, then `Invalid credentials provided`. Without a valid CLI session there is no way to start the one-off dyno, and the Azure DB host is not reachable from outside Heroku/Azure. The agent did not try to work around this (credential files were not inspected).

**To unblock (operator, about 2 minutes):**

1. `heroku login` in an interactive terminal.
2. Run the ready script (read-only, bounded, self-exiting with `--no-tty`):
   - Git Bash: `heroku run -a mindsync --no-tty python < db-reports/2026-10-07-first-week-design-aggregates.py > first-week.out 2>&1`
   - PowerShell (no `<` redirect there): `Get-Content -Raw db-reports\2026-10-07-first-week-design-aggregates.py | heroku run -a mindsync --no-tty python > first-week.out`
3. Re-spawn `database-administrator` with the output file, or with "rerun the 2026-10-07 first-week script", to interpret it and fill in the Results section.

Script: `db-reports/2026-10-07-first-week-design-aggregates.py` (65 SQL statements, all `SELECT` or catalog reads).

## Safety and privacy built into the script

- First statements: `SET TRANSACTION READ ONLY` and `SET LOCAL statement_timeout = 60000`. No `commit()`; the script ends with `db.rollback()` and `db.close()`.
- Each query runs through a helper that catches errors, prints only the first line of the error (no DETAIL line, so no data fragments), rolls back and re-arms read-only mode. One bad query cannot abort the rest.
- k-anonymity is applied in the script output itself: every column prefixed `u_` (user counts, and item or rating counts that could map to a few users) prints `<5` when the value is 1 to 4. Zero stays 0.
- Nothing per user is selected: no ids, emails, names, goal text, custom focus-area labels or therapy status per person. Emails are only used inside SQL to flag test-looking accounts and are never returned. Custom focus-area labels are excluded from the label ranking (`is_custom = 'false'` only).
- Offline validation done before handing over: every statement parsed with `pglast` (libpg_query, the real Postgres grammar), SQLAlchemy compile showed zero accidental bind parameters, and every script line compiles as a single REPL statement.

## Population definition

There is **no `onboarding_completed_at` column** anywhere. The onboarding state lives in `user_therapy_context` (one row per user): `onboarding_completed` (bool), `created_at` (row creation, the first onboarding PUT) and `updated_at` (`onupdate=now()`, bumped by every later PUT to `/users/therapy-context`).

- **Completed onboarding:** `user_therapy_context.onboarding_completed = true`.
- **Completion time `t_done`:** `updated_at` when it is within 3 hours of `created_at`, otherwise `created_at`. Reason: the same PUT endpoint is reused later (Settings writes `therapy_duration` through it), so a large gap means a later edit, not a slow onboarding. The script prints the `updated_at - created_at` gap distribution (`s1_gap_start_to_update_90`) so this rule can be checked, plus the median minutes from start to the first starter bio (`personal_bios`, enqueued on completion) as an independent completion signal.
- **Windows:** `t_done >= now() - 90 days` and `t_done >= now() - 30 days`.
- **Caveats:** Reset onboarding keeps the original `created_at` and clears `focus_areas`, `severity_ratings` and `goals_text` until the user redoes it. A user who started more than 90 days ago and later edited the row is anchored on the old `created_at` and falls out of the window.
- **Test accounts:** there is **no reliable marker** in the schema (no `is_test` flag; TestFlight subscriptions look like real ones). The script excludes a heuristic set (email matching `test%`, `%+test%`, `%test@%`, `%tester%`, `%@mindsync.%`, `%@example.%`) and reports how many were excluded (`u_testish90`, `u_testish30`). Team members on personal addresses are not caught.

## Method per question

| # | Question | Source and method |
|---|---|---|
| 1 | Focus areas per user, custom use, top 10 | `user_therapy_context.focus_areas` JSON `[{"name","is_custom"}]`: array length bucketed 0..5, 6+, median and mean. Custom = element with `is_custom = true` (users and total custom areas). Top 10 = preset labels only, distinct users. Cross-check: `user_symptoms` rows created between `t_start - 1 min` and `t_done + 1 h`. |
| 2 | Onboarding intensity | `user_therapy_context.severity_ratings` JSON `{name: score}`. **Scale 1 to 10** (slider `min 1, max 10, divisions 9`; backend accepts only 1..10). Rating-level min, median, max, mean and a 1..10 histogram; per-user mean and max medians. Cross-check: first `symptom_scores` row per symptom in the onboarding window. |
| 3 | Therapy status | `user_profile.currently_in_therapy` (`yes_regular`, `yes_occasional`, `not_right_now`, `never_been`, null). It is only written when ARTICLE9_HEALTH consent is active, so null is split by active Art.9 consent (`q3_status_vs_art9_*`). |
| 4 | Schedule and days to next session | `user_preferences.therapy_schedule` (recurring, `day_of_week` 0=Mon..6=Sun, `time_of_day` HH:MM) and `custom_therapy_sessions` (calendar dates). Schedule set = either array non-empty. Days to next = smallest gap from `t_done` in the user's local time to the next recurring weekday occurrence (same weekday counts as 0 if the session time is still ahead that day, else 7) or the next custom date after `t_done`. Buckets 0..7, `gt7`, `none_future`. Run for in-therapy users (`yes_regular` or `yes_occasional`) and for everyone with a schedule. Frequency split printed too. |
| 5 | goals_text non-empty | Count of `goals_text` with non-blank content (content never read out). Cross-check: `user_goals` rows created in the onboarding window. |
| 6 | Push token | Any row in `user_fcm_token`, plus "oldest surviving token created within 1 day of `t_done`". |
| 7 | Hour of completion | `t_done` converted with `user_preferences.time_zone` when it is a valid IANA name (checked against `pg_timezone_names`), else UTC; 3-hour buckets. A UTC-only version and the count of fallbacks are printed. |
| 8 | First 7 days (30d cohort) | Window `t_start - 1 min` to `t_done + 7 days`. Score after onboarding = any `symptom_scores` row more than 5 minutes after the user's first score in the window (or after `t_done` if they had none). Reflect = `conversations` with type REFLECT and `last_message_at` set; reported as any, excluding `entry_origin = 'onboarding_first_conversation'`, and 2 or more threads; first-conversation threads counted separately. Debrief, prep card (user-made only: not `generation_type = 'auto'` and not input type AUTO; any prep card also shown) and between-sessions note counted separately and combined. Split by whether the user already has a full 7-day window (`ROLLUP` row = total). |
| 9 | Memory items in first 24 h | `user_memory_items` created between `t_start - 1 min` and `t_done + 24 h`: per-user count distribution and median (all users and users with at least 1), category and source distribution. Run for the whole 30d cohort and for the sub-cohort onboarded after the first memory item ever existed. Global first-day-per-source table included to date the feature. |

## Caveats to read alongside the numbers (known from code, before any data)

- **Therapy status may be almost empty.** The 2026-06-29 audit found `currently_in_therapy` filled for 0 users even with Art.9 consent. If that has not changed, Q3 and the in-therapy half of Q4 will be mostly null and not usable as asked; the Art.9 split will show whether that is a consent gap or a save gap.
- **Schedules are rare and undated.** The 2026-09-02 audit found a non-empty `therapy_schedule` for 12 of 1810 users. `user_preferences` has no `updated_at`, so the script cannot tell whether a schedule was entered during onboarding or weeks later; the days-to-next figure uses whatever schedule exists today. Biweekly parity is ignored, so for biweekly users the true gap can be 7 days longer.
- **Push tokens are a lower bound.** Invalid tokens are deleted automatically; coverage was 7.6% of users in September.
- **Memory items are new.** `user_memory_items` exists since early October (migration m315), so most of the 30d cohort onboarded before it existed; the all-30d median will be 0 by construction. Use the since-launch sub-cohort. Items are hard-deleted on "Forget everything" and when their source is deleted.
- **First conversation is new too.** `entry_origin` only marks onboarding first conversations from early October. For users onboarded before that, "any Reflect thread" already means "beyond the first conversation".
- **Time zones:** non-IANA stored values (for example `UTC+2`) fall back to UTC; the script reports how many.

## Results

Pending the run above. Each section of the output is headed `=== <query name> ===` and maps to the table rows by prefix (`s0`/`s1` schema and cohort, `q1`..`q9` the questions).
