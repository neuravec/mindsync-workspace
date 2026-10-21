# PostHog dashboards rebuild plan (task C4) – 2026-08-10

- **Author**: integration-devops
- **Source task**: `analytics-reports/2026-08-10-posthog-audit-taskplan.md` §C4
- **Depends on**: C2/C3 filters (`analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md`, already applied here), S1 api_error fix (committed, **not deployed** – see below)
- **Scope of this session**: update `scripts/posthog_build_dashboards.py` (code + insight definitions) and write this plan. **The script was NOT run against production PostHog.** Running it – i.e. actually mutating the 9 live dashboards – is an operator decision, per the task owner note ("operator uruchamia skrypt, nie agent"). Verification of event names/volumes was done read-only via `scripts/posthog_query.py`.
- **Access used**: `python scripts/posthog_query.py --sql ...` (read-only HogQL, project 141170 EU) for every volume/`$lib` claim below, all queried fresh on 2026-08-10. `python scripts/posthog_build_dashboards.py --dry-run [--update] [--retire-dead]` was run against the real 9 dashboards (638505–638513) to confirm the script executes cleanly end-to-end – dry-run only issues GET requests (dashboard/insight existence checks), it does not create, update, or delete anything.

## Why a rebuild, and why it needed a mid-task correction

The 9 dashboards and ~50 insights were built 2026-04-23 against a taxonomy that has since drifted heavily: renames, a schema change on one event, several client vs. backend re-splits, and roughly a dozen new event families added across five batches between 2026-08-04 and 2026-08-10 – most of which are **committed but not yet deployed to Heroku / released to app stores**, so they read as zero-volume even though the code exists.

Mid-task, a parallel finding (task B7) flagged that several events read as "client" from filenames/comments alone are actually backend-emitted (`posthog-python`), and that a naive global `$lib = 'posthog-flutter'` filter would silently zero them. That correction was applied: **every event used in this script was independently verified with a fresh `SELECT event, properties.$lib, count() ... GROUP BY event, lib` query before its filter was assigned** – not inferred from where the event name appeared in the codebase. That check surfaced two further complications beyond the reflect_*/api_error/user_activated/summary_*/realization_detected set already known from the taskplan metadata:

- **`notification_received` is client-only** (100% `posthog-flutter`, verified). An earlier draft of this rebuild had it as backend, from a doc-comment in `notification_orchestrator_job.py` that only *names* the client event – not an actual capture call. Fixed.
- **Two events are dual-sourced** – fired independently by both the client and the backend for the same logical action: `subscription_purchase_completed` (5 `posthog-flutter` + 3 `posthog-python` / 90d) and `consent_granted` (16 `posthog-flutter` + 18 `posthog-python` / 90d). Both use `client=False` (no `$lib` filter at all) so neither side is dropped, rather than either of the single-source variants.
- **`consent_revoked` is the mirror case** – backend-only (0 `posthog-flutter` of 4 events / 90d) – also needs `client=False`, but because a `$lib='posthog-flutter'` filter would have zeroed it, not because it needed to include both sides.

## How the filter is applied (per-series, not global)

`scripts/posthog_build_dashboards.py` now has `event_series(event, ..., client=True)`. `client=True` (default) appends the three hygiene filters (`$lib='posthog-flutter'`, `$is_testflight != true`, `$is_emulator != true`) to that one series. `client=False` appends nothing. This is deliberately **per-series**, not a single filter on the whole query, because several insights mix a client series with a backend series in the same funnel/trend (e.g. Reflect engagement: backend `reflect_session_started` paired with client `reflect_ui_session_ended`) – a query-level filter would have zeroed the backend half.

**Caveat carried into the script's docstring**: the exclusion uses the PostHog UI "is_not" property-filter operator. Its NULL-safety was *assumed* to match the raw HogQL `!=` NULL-safety already verified in `analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md` – that assumption was not independently re-verified through the UI operator itself. **Operator action after running with `--update`: spot-check one insight's number against the equivalent raw `posthog_query.py --sql` count.**

### Verified `$lib` per event (fresh queries, 2026-08-10, 90d window)

| Event | `$lib` | Filter used | Why |
|---|---|---|---|
| `subscription_purchase_completed` | 5 flutter + 3 python | `client=False` (no filter) | dual-sourced, would undercount either way |
| `consent_granted` | 16 flutter + 18 python | `client=False` (no filter) | dual-sourced |
| `consent_revoked` | 0 flutter / 4 python | `client=False` (no filter) | backend-only; a flutter filter would zero it |
| `notification_received` | 35/35 flutter | `client=True` (default) | client-only — corrected mid-task, see above |
| `reflect_session_started`, `reflect_session_ended` | 100% python | `client=False` | backend (`app/api/v1/endpoints/reflect.py`) |
| `api_error` | 100% python | `client=False` | backend (`app/main.py`) |
| `realization_detected` | 100% python (1/1) | `client=False` | backend (`app/api/v1/endpoints/realizations.py`) |
| `user_activated`, `weekly_summary_generated`, `monthly_audit_generated` | 0 events yet; code is backend-only (`app/services/posthog_service.py`), no matching Flutter emitter found | `client=False` | backend by code inspection (no live data to verify $lib directly — see AWAITING DEPLOY below) |
| `reflect_ui_session_ended`, `notification_row_toggled`, `signup_*`, `consent_screen_viewed`, `account_*`, `app_tour_*`, `workspace_opened`, `quick_capture_*`, `prep_capture_*`, `voice_transcription_*`, `notification_permission_*`, `paywall_shown`, `subscription_restore_*`, `summary_viewed` | 100% flutter (where volume exists) | `client=True` (default) | client-only, verified |
| `$pageview`, `$web_vitals` | web SDK (`$lib='web'`) | `client=False` (no filter, not a hygiene-filter case) | marketing site, not app traffic — a `posthog-flutter` filter would zero these entirely |

## Per-dashboard changes

### Onboarding Health (638505)
- **Fixed**: main funnel used `range(7)` (steps 0–6); audit found 8 flowing `step_index` values (0–7). Updated to `range(8)`. Insight renamed "Onboarding funnel (9 steps)" → "Onboarding funnel (8 of 9 known steps — see B6)" (old name **retired**, `--retire-dead`) because the "(9 steps)" claim was never true — 9 is the *spec*, 8 is what has ever fired; the 9th step is an open gap (task B6), not fixed here.
- **Updated**: "Started by auth provider" switched from the `user_logged_in` proxy to the direct `signup_method_selected` breakdown by `method`, now that signup is instrumented.
- **Added**: "Signup + consent funnel (pre-onboarding)" (signup_started → signup_method_selected → consent_screen_viewed → consent_granted, `consent_granted` unfiltered per dual-source note above), "Signup failures" (signup_failed trend).
- Hygiene filters applied to all pre-existing insights via `--update`.

### Activation & Time-to-Value (638506)
- **Added**: "App tour funnel" and "App tour skip rate" (new 2026-08-04 instrumentation). "User activated (backend-derived) — daily" and "Activation — within 24h vs later" using the backend `user_activated` event (see growth-analyst's `analytics-reports/2026-08-10-activation-definition.md`, which explicitly recommends the backend-derived metric over a client event — **not yet deployed, will read empty**).

### Core Engagement (638507)
- **Updated**: "Daily unique users per feature" gained `workspace_opened`, `quick_capture_started`, `prep_capture_started` alongside the original capture events. **Open question flagged in the insight description, not resolved here**: `prep_card_started` (legacy, 9 events/14d) and `prep_capture_started` (new, 4 events/14d) are both live simultaneously — unclear whether `prep_capture_*` is meant to replace `prep_card_*` or is a distinct "quick" variant. Worth a data-analytics/flutter-mobile follow-up, not decided by this rebuild.
- All other insights unchanged in structure, hygiene filters applied via `--update`.

### Therapy Loop Health (638508)
- **Corrected semantics (the headline C4 item)**: added "Reflect engagement funnel (session started → ui session ended)" pairing backend `reflect_session_started` (live, 158 events/90d) with client `reflect_ui_session_ended` (0 events/90d — code exists, not deployed). Explicitly does **not** use backend `reflect_session_ended` (11 events/90d vs 158 `reflect_session_started` — only fires on explicit thread finalization, undercounts ~12x). Added duration/end_reason/messages_sent insights on `reflect_ui_session_ended`, all marked `[awaiting deploy]`.
- **Added**: "Summary/audit generated (backend, weekly vs monthly)", "Summary viewed (client, by period_type)", "Summary generated-vs-viewed ratio — weekly" (task B3's core ask — is anyone reading what gets generated). All three **awaiting deploy** (0 events/90d on both the backend and client side, verified).
- **Added, kept with TODO marker per task C4 item 6** (not retired — active investigation, task B5): "Realization detected (daily count)" — `realization_detected` fired exactly once in project history; name/description flag this explicitly rather than hiding it or silently including it as if it were healthy.

### Monetization (638509)
- **Added**: "Paywall → screen → product selected" and "Paywall shown by trigger_feature" (both **awaiting deploy** — `paywall_shown` is 0/90d). Description flags a curiosity worth escalating to data-analytics: `paywall_dismissed` (same batch) already has 5 events/4 users with **zero** matching `paywall_shown` — either a guard bug or an artifact of the deploy gap; re-check once `paywall_shown` goes live and the asymmetry persists.
- **Added**: "Purchase attempts (started/completed/failed)" — `subscription_purchase_completed` uses the dual-source unfiltered variant (see table above). "Restore attempts (started/completed/failed)" — **awaiting deploy**, `subscription_restore_*` is 0/90d.

### Feature Adoption Matrix (638510)
- **Added**: "Feature reach — DAU" gained `workspace_opened`, `quick_capture_started`, `prep_capture_started`, `voice_transcription_started`. New standalone insights: "Quick capture funnel", "Prep capture funnel (new)", "Voice transcription — started vs completed vs failed" (2026-08-05 AssemblyAI batch).

### Health & Quality (638511)
- **Corrected**: marketing-site insights (`$pageview`, `$web_vitals`) explicitly use `client=False` (they're `$lib='web'`, not `posthog-flutter` — applying the app hygiene filter would have zeroed them, a different failure mode than the C2/C3 filters were designed to prevent but the same root cause).
- **Added**: "[Mobile] Recording abandoned by reason" (`recording_abandoned`, live, 2026-08-10 batch). "[Backend] API errors — total volume by endpoint" (unfiltered, the old undifferentiated signal, still useful). "[Backend] API errors — expected vs real (`is_expected` split)" and "[Backend] API errors — real failures only (`is_expected=false`) by endpoint" — **THE** S1 quality fix, but **not yet deployed**: `is_expected` is `NULL` on 100% of the 4,611 `api_error` events in the live 14d window (verified 2026-08-10, four separate days checked). These two insights will read empty/undifferentiated until the S1 backend commit (7696f40) is deployed to Heroku — flagged `[awaiting deploy]`.

### Gamification Impact (638512)
- Structurally unchanged (all its events — `character_card_viewed`, `orca_color_changed`, `bio_refreshed` — are still live and client-only). Dashboard description now documents task B4's finding (goals/symptoms near-unused, no product decision made yet) as context, without adding speculative insights for an undecided feature area.

### Account Health (638513)
- **Retired** (`--retire-dead`): "Notification preference changes" — referenced `notification_preference_changed`, silent since 2026-05-21 and renamed twice since (`notification_interest_toggled`, silent since 2026-07-17, → `notification_row_toggled`, live since 2026-08-04, FE commit 4a20b19). Schema also changed `category/selected` → `key/value`.
- **Added** (replacement): "Notification row toggles (key/value)" — breakdown by `key`, matching the new schema.
- **Added**: "Notification permission funnel" (`notification_permission_prompted` → `granted`, live 2026-08-04 batch), "Account screen opens (daily)", "Account deletion funnel" (`account_deletion_started` → `confirmed`), "Consent grants vs revokes" (both series `client=False` per the dual-source/backend-only table above).
- **Fixed**: "Notifications received (daily)" was implicitly backend in the original script's framing; verified 100% `posthog-flutter` — kept as a default (client-filtered) series, description corrected to explain the origin and the mid-task misclassification that was caught and fixed.

## What will read empty until the operator deploys/ships something

Verified via `posthog_query.py`, 90-day window, 2026-08-10 — all `[awaiting deploy]`-tagged insights above:

| Event(s) | Volume (90d) | Blocked on |
|---|---|---|
| `is_expected` property on `api_error` | 0 of 4,611 events tagged | Deploy backend commit 7696f40 (S1) to Heroku |
| `reflect_ui_session_ended` | 0 | Deploy/release the 2026-08-10 client batch (commit ~5b3af7d) |
| `paywall_shown`, `subscription_restore_started/completed/failed` | 0 | Deploy/release the 2026-08-10 monetization-funnel-fix batch |
| `summary_viewed`, `weekly_summary_generated`, `monthly_audit_generated` | 0 | Deploy/release the summary-instrumentation batch (FE ~5735309 / BE e16f657) |
| `user_activated` | 0 | Deploy the backend activation-instrumentation batch (2026-08-10) |

Everything else referenced in this rebuild (`workspace_opened` 142/18u, `notification_permission_prompted` 60/20u, `consent_granted` 34/19u, `account_screen_opened` 28/7u, `reflect_session_started` 24/16u/14d, `app_tour_started` 18/12u, `signup_started` 17/15u, `voice_transcription_started` 8/3u, `app_tour_completed` 8/8u, `account_deletion_started` 5/2u, `consent_revoked` 4/2u, `prep_capture_started` 4/3u, `notification_row_toggled` 4/1u, `quick_capture_started` 3/2u, `realization_detected` 1/1u, `signup_failed` 1/1u — all 14d) is already live and will populate immediately.

## Retired insights (require `--retire-dead` to actually remove)

| Dashboard | Insight name | Reason |
|---|---|---|
| Account Health | Notification preference changes | Referenced a doubly-superseded dead event; replaced by "Notification row toggles (key/value)" |
| Onboarding Health | Onboarding funnel (9 steps) | Factually wrong step count; replaced by "Onboarding funnel (8 of 9 known steps — see B6)" |

No other original insight referenced a dead event — all 22 events from the original 2026-04-23 build are still flowing (verified fresh, including the previously-borderline `onboarding_legal_gate_abandoned`, which is genuinely near-zero by design, not dead).

## Operator instructions

1. **Read this report and the script's updated module docstring** (`scripts/posthog_build_dashboards.py`) before running anything.
2. Recommended sequence, from the repo root, with `POSTHOG_PERSONAL_API_KEY` / `POSTHOG_PROJECT_ID` set (or sourced from `MindSync/.env`):
   ```
   # 1. Dry run first — read-only, confirms exactly what would change.
   python scripts/posthog_build_dashboards.py --dry-run --update --retire-dead

   # 2. Review the output. Then run for real:
   python scripts/posthog_build_dashboards.py --update

   # 3. Separately (deletion is opt-in on purpose):
   python scripts/posthog_build_dashboards.py --retire-dead
   ```
   `--update` is required to actually propagate the new queries onto the 44 pre-existing insights that keep their original name (hygiene filters, the auth-provider swap, etc.) — without it the script's original skip-if-exists behavior means re-running it is a no-op against the live dashboards, same as before this rebuild.
3. **Spot-check the `is_not` operator caveat**: after running with `--update`, pick one hygiene-filtered insight (e.g. "DAU (any navigation)" on Core Engagement) and compare its number in the PostHog UI against `python scripts/posthog_query.py --sql "SELECT uniq(distinct_id) FROM events WHERE event='tab_switched' AND properties.\$lib='posthog-flutter' AND properties.\$is_testflight != true AND properties.\$is_emulator != true AND timestamp > now() - INTERVAL 14 DAY"`. They should match; if not, the UI "is_not" operator diverges from the verified NULL-safe HogQL `!=` and every hygiene-filtered insight needs re-checking.
4. This rebuild does **not** address task S6 (consent-gate fix) or task C2's GA4 pull — both are separate, still-open operator actions tracked elsewhere (`analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md`, `security-reports/2026-08-10-consent-gate-ruling.md`).
5. Revisit the `[awaiting deploy]`-tagged insights after each of the five pending batches ships, to confirm they actually populate as expected (not just that the query is syntactically valid).

## Deliverable status vs. DONE_WHEN

Task C4 DONE_WHEN: "dashboards odzwierciedlają eventy, które faktycznie lecą, mają filtr ruchu wewnętrznego i web (C2, C3), a insighty na nieistniejące eventy są usunięte lub oznaczone jako oczekujące na instrumentację."

- **Script updated** to reflect live taxonomy, with C2/C3 hygiene filters applied per-series (verified client/backend/dual-source per event, not assumed) — done, not run.
- **Dead-event insights**: 2 retired (via opt-in `--retire-dead`), all others confirmed still live.
- **Zero-volume insights**: distinguished as `[awaiting deploy]` (code exists, deploy pending — 5 batches, listed above) rather than "awaiting instrumentation" (task C1, still in progress) — one exception, `realization_detected`, kept with an explicit investigation-in-progress marker (task B5) rather than either label, since it has both code AND a deploy AND a known-broken behavior.
- **Not done here** (explicitly out of scope, operator/other-task-owned): actually running the script against production PostHog; task C1's full sweep of ~40 dead events (only the ones touching these 9 dashboards were handled); GA4 pull (C2.2).
