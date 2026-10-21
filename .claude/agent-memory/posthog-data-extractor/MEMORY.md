# posthog-data-extractor – memory

## Default filters (read before any app-metrics query)
- [Default exclusion filters](reference_default_exclusion_filters.md) – `$lib='posthog-flutter'` for app; `$is_testflight`/`$is_emulator != true`; `$is_testflight` 100% iOS/iPadOS, 0% Android (structural, not a bug); `$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')` excludes bot traffic, still active
- [reflect_* lib trap + voice-chat B7 baselines](reference_voice_chat_and_backend_lib_trap_2026_08_10.md) – `reflect_session_started/_message_sent/_ended` are backend (`posthog-python`), not `posthog-flutter`; `$session_id` is top-level not `properties.$session_id`; `subscription_screen_opened` has no trigger property
- [moment.* notification family + 2026-09-12 baselines](reference_moment_notification_family_and_2026_09_12_baselines.md) – backend-touched population ~14x larger than active app users, never report as "active users"; `moment.sent`/`moment.opened` = sent-vs-opened; Habit Tracker zero instrumentation; D30 retention 0.8%
- [Reflect entry mode-picker pull 2026-09-25](reference_reflect_entry_picker_2026_09_25.md) – picker events flowing since ship date 2026-09-18 on `$app_version` 2.0.91+; partial rollout (~46/127-150 30d users); `end_reason=voice_interrupted` not observed yet; single-user skew 112/115 events one day; reconfirms lib trap + legacy conversation_* dead
- [Post-onboarding offer + tester classification 2026-10-03](reference_post_onboarding_offer_and_test_accounts_2026_10_03.md): no `offer_shown` event, use `paywall_shown` trigger `post_onboarding`; flow on 2.0.97+; tester/automation-account heuristics for fresh builds; `subscription_screen_opened` now carries `trigger_feature` on 2.0.97+
- [Post-onboarding Home behaviour 2026-10-07](reference_post_onboarding_home_2026_10_07.md): landing = first `$screen` mainPage; GettingStartedCard/FAB taps uninstrumented; `moment.opened` has no type (join on moment_id); week-1 baselines
- [Blog -> app attribution 2026-10-07](reference_blog_attribution_2026_10_07.md): `install_source=blog` 0 so far; google-play = Play default; web PostHog consent-gated; `blog_store_click` never seen
- [First conversation -> prep card 2026-10-13](reference_first_conversation_prep_card_2026_10_13.md): backend job telemetry person-less and never arrived; proxies = prep-cards/latest 404 polling + backend ART9 consent
- [Churn signals 2026-10-15](reference_churn_signals_2026_10_15.md): 14d-silence churn def + baselines; re-engagement 2.8% return; no cancel/expire events; scratchpad shared, use unique names
- [Tab usage + PageView pass-through 2026-10-13](reference_tab_usage_pageview_passthrough_2026_10_13.md): `tab_switched` inflated for middle tabs, use settled opens (>=3s); `character_card_viewed` is a load not an open; Character baselines
- [Retention baselines 2026-10-15](reference_retention_baselines_2026_10_15.md): broad vs strict "active" (broad MAU ~3x strict), D1/D7/D30, lifecycle, array retention pattern; shared scratchpad overwrites
- [Oct 2026 release impact 2026-10-15](reference_release_impact_oct_2026_10_15.md): build->feature map (2.0.100/2.0.107 store, 2.0.109-112 testers only), new events flowing vs never seen, weekly baselines
- [Acquisition cube + new-user definition 2026-10-15](reference_acquisition_cube_2026_10_15.md): new = first flutter event since 04-22; one-query cube + local slicing; 60d baselines; blog installs still 0
- [Errors + stability 2026-10-15](reference_errors_stability_2026_10_15.md): error-event catalog, single-user loop traps, profile-404 = first-launch path, real-error share 21%

- [Paywall conversion taxonomy 2026-10-15](reference_conversion_paywall_2026_10_15.md): purchase_completed emitted client+backend; Windows-backend test pollution; trial_ended only on conversion; 60d baselines
- [Onboarding + activation 2026-10-15](reference_onboarding_activation_2026_10_15.md): step_index -1..7, completion 47%->74%, first_week_plan no exposure event, aha=debrief; shared scratchpad

## Access (verified 2026-08-10)
- Transport is ALWAYS `python scripts/posthog_query.py` (stdlib REST runner, read-only). MCP/OAuth is known-broken here – never try it.
- Project: PostHog EU Cloud, `POSTHOG_PROJECT_ID=141170`, host `https://eu.i.posthog.com`. Creds in `MindSync/.env` (`POSTHOG_PERSONAL_API_KEY`) – names only, never values.
- `--check` confirms reachability. Batch many queries into one `.sql` with `-- @@ label` sections and run once (`--sql-file`). On Windows prefer `--sql-file` over `--sql`.
- HTTP 400 responses carry a `detail` field naming the exact error – read it instead of retrying.
- A self-JOIN of `events` with an unbounded CTE can exceed the runner's 120s timeout even at modest volume. Fix: bound EVERY CTE with `timestamp >=/< toDateTime(...)`, and pass `--timeout 240`+ for 2+ joined CTEs. Isolate a heavy query in its own `--sql-file` call.
- (2026-10-07) `/query/` now enforces `max_execution_time = 10` s server-side (504). `--timeout` cannot lift it. Workaround: materialize a small population as a scratchpad-only `person_id IN (...)` list (delete after, never commit). Runner now keeps going past a failed `-- @@` section.

## HogQL gotchas (each one cost a failed query)
- `timestamp` is `DateTime64(6,'UTC')` → `windowFunnel` needs `toDateTime(timestamp)`. `toDate`/`toStartOfWeek`/`min`/`max` accept it raw.
- User counts: `count(DISTINCT person_id)`, NOT `distinct_id` (overcounts).
- Property access `properties.$os` works; missing values are `NULL` **or** `''` → filter both.
- `$app_version`, `$os`, `$screen*` are client-only – backend events never carry them.
- `$session_id` is a **top-level field**, not `properties.$session_id`. Works as a window-function partition key.
- Enumerate keys: `arrayJoin(JSONExtractKeys(toString(properties)))`.
- **Don't assume a feature's whole event-name family shares one `$lib`.** `reflect_session_started`/`_message_sent`/`_ended` are backend (`posthog-python`); the newer `reflect_mode_*`/`reflect_entry_*` picker events ARE client (`posthog-flutter`). Same trap caught the whole `moment.*` family. Always check `properties.$lib` per-event before filtering. See [[reference_voice_chat_and_backend_lib_trap_2026_08_10]], [[reference_reflect_entry_picker_2026_09_25]].
- **A low aggregate coverage % for a property can be a platform-mix artifact.** Always break a suspicious coverage number down by `$os` before concluding it's an instrumentation defect – see [[reference_default_exclusion_filters]].
- **A naive `GROUP BY properties.$os` + `count(DISTINCT person_id)` double-counts** people whose events mix a real value and null. Fix: aggregate to one row per person first (`any(properties.$os)` in a `GROUP BY person_id` subquery), then group that.
- `--props <event> --days N` overstates "users" vs a direct `count(DISTINCT person_id)` query. Use `--props` only to confirm a key exists; get counts via explicit HogQL.
- Reusable: "new users per day" = `SELECT person_id, min(timestamp) first_ts FROM events WHERE timestamp > toDateTime('2026-04-22') GROUP BY person_id`, then bucket on `first_ts`.
- Reusable: feature-breadth histogram = `multiIf(event IN (...), 'category', ...)` per event → `count(DISTINCT feature)` per person → bucket. Category map in `analytics-reports/raw/2026-08-10-engagement-14d.md`.
- Reusable: current-vs-prior trend in ONE query = `countIf(timestamp > now() - INTERVAL 14 DAY)` + `count(DISTINCT if(cond, person_id, NULL))`, repeated for prior window, `GROUP BY event`.
- Reusable: skew check = `SELECT person_id, count() FROM events WHERE event=... AND <window> GROUP BY person_id ORDER BY count() DESC LIMIT 10` (whole window) or with `toDate(timestamp)='YYYY-MM-DD'` for a single suspicious day. Caught a 112/115-event single-person one-day spike 2026-09-25 (null `$app_version` on Windows = backend/test client tell) – see [[reference_reflect_entry_picker_2026_09_25]]. For a full event sweep: `SELECT event, sum(cnt) total, max(cnt) top1 FROM (SELECT event, person_id, count() cnt FROM events WHERE <window> GROUP BY event, person_id) GROUP BY event HAVING total>=10 AND top1*1.0/total > 0.6`.
- Reusable: "did X ever happen per person" = per-person boolean flags (`countIf(event='A')>0 AS has_a` in a `GROUP BY person_id` subquery), then `countIf(has_a AND has_b)` outer.
- Reusable: "never fired, ever" = one `GROUP BY event` query with `timestamp > now() - INTERVAL 365 DAY` over a candidate list; events absent never fired. Better: pull the full `event_definitions` catalog once (`--events`, ~150-180 names) and grep locally – also shows a new feature's exact first-seen ship date via clustered `created_at`.
- Reusable: per-person retention inside a post-signup window = CTE chain `first_seen` → `flags` → `cohort` (join) → `per_person` (join back to events, bounded `BETWEEN first_ts AND first_ts + INTERVAL N DAY`) → outer `GROUP BY cohort_name`. Needs every CTE time-bound (see timeout gotcha). Worked example: [[reference_voice_chat_and_backend_lib_trap_2026_08_10]].
- Reusable: right-censoring-safe D1/D7/D30 retention = three SEPARATE queries, each with its own cohort-eligibility cutoff (`first_ts < now() - INTERVAL {1,7,30} DAY`), not one shared cutoff.

## Baselines (2026-08-10 14d unless noted; see [[reference_moment_notification_family_and_2026_09_12_baselines]] for 2026-09-12 30d baselines which supersede several items)
- Total events 14d ≈ 13,679, DAU 3-20/day. New users 14d = 90.
- WAU by week: 07-05 113 (clamped) · 07-12 123 · 07-19 155 · 07-26 68 · 08-02 67 · 08-09 19 (partial). Stickiness (complete weeks): 17-21%.
- Retention new-cohort (n=90, 14d): 18.9% returned any later day.
- Total distinct users 14d = 127 vs prior 14d = 266 – roughly halved as of 2026-08-10; check this before treating any trend as a quality signal vs a traffic signal.
- Platform split 14d (app-only events): Android 76 / iOS 15 / iPadOS 1.
- App versions: moved from 2.0.75/76 (Aug) to 2.0.85-2.0.94 by 2026-09-25 (largest 30d cohort: 2.0.89, 57 users, first 09-03) – re-check current versions each pull, list moves every 1-2 weeks.
- Top events 14d: `api_error` 4507/60u · `reflect_limit_hit` 1870/**1-user skew** · `$screen` 1838/89u · `tab_switched` 1689/35u · `timeline_viewed` 510/46u · `reflect_message_sent` 432/15u · onboarding events ~250-270/33u each · `character_card_viewed` 162/33u · `workspace_opened` 124/16u.
- Onboarding funnel 14d: 8 steps (9th `personalise` by 09-12). 33 viewed → 27 completed (82%). Longest dwell: `companion` step, 46s.
- Therapy-loop stage users 14d: prep 6, recording 16, debrief 17, between_session 11 – no summary-view event exists.
- Voice chat B7 lifetime (08-10): 11 users/65 events, last fired 08-04 – see [[reference_voice_chat_and_backend_lib_trap_2026_08_10]].
- `$is_testflight` coverage: 100% iOS/iPadOS, 0% Android (structural). See `analytics-reports/raw/2026-08-10-testflight-coverage-os-split.md`.
- Full raw pulls (chronological): `2026-08-10-engagement-14d.md`, `2026-08-10-errors-quality-14d.md`, `2026-08-10-voice-chat-b7.md`, `2026-08-10-testflight-coverage-os-split.md`, `2026-09-12-usage-retention-monetization-extract.md`, `2026-09-25-reflect-mode-picker-post-deploy.md` (all under `analytics-reports/raw/`).

## Instrumentation gaps (see [[reference_moment_notification_family_and_2026_09_12_baselines]] for 2026-09-12 corrections)
- `paywall_shown`: absent until 2026-08-16, still thin (1-10 events/day at most). `trial_started`/`trial_ended`: confirmed absent, re-checked 2026-09-12. `subscription_purchase_completed`: fires but very thin (single digits/month) – never treat PostHog purchase counts as revenue truth, cross-check Postgres `subscription_receipts` via `database-administrator`. `paywall_shown.properties.trigger_feature` values seen as of 2026-09-25: `drawer_menu`, `premium_gate_session_recording`, `premium_gate_reflect_messages` – no value yet for the new Reflect voice-lock trigger.
- No event for "summary viewed/generated (daily)" (only weekly/monthly_audit exist) or gamification/streaks/achievements (still "planned" per CLAUDE.md). Habit Tracker (shipped 09-02) has zero instrumentation, confirmed 09-12.
- `subscription_screen_opened` has NO trigger/source property anywhere in its history – use `paywall_shown.properties.trigger_feature` instead for trigger breakdowns.
- `voice_transcription_failed`: never fired until 2026-08-10, now fires (first 08-20).
- Ingest started **2026-04-22** – retention/cohort windows clamp against it.
- `api_error` is MindSync's largest event by far. Root cause (decomposed 08-10, reconfirmed 09-12): mostly `is_expected=True` 404s on `…/latest` endpoints (empty-state pattern, not a crash). Real remainder concentrates on `/users/get_user_profile_and_subscript…` and `/users/therapy-context` 404s (~30-38 users/30d) – flagged to `backend-api`. Full breakdown: `errors_quality_gaps_2026_08_10.md` (topic file).
- Notification-toggle event rename (08-10): `notification_interest_toggled`/`notification_banner_tapped`/`notification_master_toggled` went silent, `notification_row_toggled` appeared – likely rename not regression, reconfirmed still silent as of 08-10 deep pull. `timeline_generate_now` and `inapp_insight.*` also silent for 2+ weeks as of 08-10.
- Recording pipeline backend events (`recording_processing_started/completed/failed`): never fired until 08-10, now fire (first 08-12) – re-verify completion RATE if this recurs.
- `conversation_started`/`_message_sent`/`_ended` (legacy chat, distinct from Reflect): went silent 2026-08-11, **reconfirmed permanently dead in 2026-09-25 recheck** – fully superseded by `reflect_*`, no longer an open question.
- Reflect entry redesign (shipped 09-18, see [[reference_reflect_entry_picker_2026_09_25]]): new `end_reason=voice_interrupted` on `reflect_ui_session_ended` not observed as of 09-25 (1 week post-ship) – open question for `flutter-mobile`/`backend-api`.
- See topic file `errors_quality_gaps_2026_08_10.md` for the full 40-event never-fired/went-silent/thin-signal list checked against code (several corrected above as of 09-12/09-25 – treat that file as historical).
- [Feature usage + voice 2026-10-15](reference_feature_usage_voice_2026_10_15.md): 30d reach baselines (257 active); GPT-Live-1 events 1 TF tester; to-do no events; moment_id join needs toString
