# Metrics hygiene: C2 (web vs app split) + C3 (internal traffic filter) + C7 (bot traffic filter) – 2026-08-10

- **Author**: integration-devops
- **Source tasks**: `analytics-reports/2026-08-10-posthog-audit-taskplan.md` §C2, §C3; C7 continuation from `analytics-reports/2026-08-10-anonymous-users-analysis.md` (growth-analyst, finding F1)
- **Scope**: verify and document the default filters that should be applied to every "active users" style query (web-vs-app split, internal/test traffic, and – added in this update – automated bot traffic); pull (or arrange the pull of) historical GA4 web traffic before it goes behind the consent gate; record the filters in agent memory and wire the confirmed ones into `scripts/posthog_build_dashboards.py`. No dashboards were run against production (`--update` was not invoked) and nothing in PostHog was mutated.
- **Access used**: `python scripts/posthog_query.py` directly (read-only REST/HogQL, project 141170 EU, credentials from `MindSync/.env`). All numbers below are freshly queried 2026-08-10, independent of the growth-analyst report run earlier the same day.

## C2 – separate marketing-site traffic from app metrics

### Canonical filter – verified on fresh data

- **App metrics**: `properties.$lib = 'posthog-flutter'`
- **Marketing-site metrics**: `properties.$lib = 'web'`
- **Backend-emitted events**: `properties.$lib = 'posthog-python'` (never carries `$os`/`$app_version`/`$is_testflight`/`$is_emulator` – see C3)

This matches the filter growth-analyst already established and documented in `.claude/agent-memory/growth-analyst/reference_posthog_web_vs_app_split.md` (the "web vs app split" trap, and the 2026-07-25 cookie-consent gate that cut tracked web traffic ~84%). This task re-verifies it two weeks later with an independent query.

### Before / after (14d vs prior 14d, 2026-08-10)

| `$lib` | events 14d | users 14d | events prior 14d | users prior 14d |
|---|---|---|---|---|
| `posthog-flutter` (app) | 6,307 | 94 | 6,231 | 81 |
| `web` (marketing site) | 143 | 28 | 893 | 176 |
| `posthog-python` (backend) | 7,576 | 67 | 1,734 | 40 |

App traffic is flat-to-growing (81 → 94 users), web traffic is down ~84% period over period – consistent with the consent-gate finding in `analytics-reports/2026-08-10-acquisition-collapse.md`. Any "active users" number that does not split by `$lib` is still overweighting a shrinking, consent-biased web sample; user counts drift a few points between runs (documented person-merge behaviour, not a bug) so treat the ratios, not the absolute counts, as load-bearing.

**Coverage check**: `properties.$lib` is present on 100% of events (`countIf(NOT JSONHas(properties,'$lib')) = 0` of 14,026 events in the 14d window). Safe to filter on unconditionally – no fallback/default-value handling needed.

### GA4 historical pull (task step C2.2)

**Status: NOT DONE from this session – requires the operator.**

Checked every access path available in this environment before concluding that:
- `MindSync/.env` – no `GA4`/`GOOGLE_ANALYTICS`/`GOOGLE_APPLICATION_CREDENTIALS`/service-account keys of any kind (full key list checked; only Azure AD, OpenAI, Firebase, PostHog, Loops, AssemblyAI, Play Console are present).
- No `gcloud` CLI available in this environment.
- No Google service-account JSON, OAuth client secret, or GA4 config file anywhere in the repo (`client_secret*`, `*ga4*`, `*google*credential*`, `*service-account*` all searched, nothing found).
- The `seo-google` skill (which has a GA4 Data API command, `/seo google ga4`) is **not configured**: its expected config file `~/.config/claude-seo/google-api.json` does not exist, and its `scripts/` directory (referenced by the skill's own instructions, e.g. `scripts/google_auth.py`) is not present in this installation – the skill has never been set up with credentials for this Google account.

Per the task instruction, this was not forced (no ad-hoc OAuth flow was attempted). **This is an operator step, and it is time-sensitive**: task S6 (consent-gate fix, `security-reports/2026-08-10-consent-gate-ruling.md`) will move GA4 behind the consent banner once executed, after which GA4 will suffer the same ~84%-undercounting problem PostHog web tracking already has. The pull must happen before S6 ships.

**Exact instruction for the operator:**

1. Log into Google Analytics (the account that owns property `G-DWNVZNWCT5`, `www.mindsync.app`).
2. Go to Reports → Life cycle → Acquisition (or Explore → free-form exploration) for the property.
3. Export **daily** aggregates from the earliest available date (property creation, likely well before this project's PostHog ingest start of 2026-04-22) through today (2026-08-10), with these dimensions/metrics:
   - Dimension: Date (daily grain – do not use the default weekly/monthly rollup)
   - Dimension: Default channel group (or Session source/medium) – needed to distinguish organic/direct/referral/paid, matching what growth-analyst already found in PostHog (`$direct` and `www.google.com` dominant, near-zero paid)
   - Metrics: Users (or Total users), Sessions, Views (pageviews), Engagement rate (optional but useful)
4. Export as CSV (GA4 UI export, or via Explore → export to Sheets/CSV – no API access is required for a one-time manual pull).
5. Save the export at `analytics-reports/raw/ga4-history-export.md` (or `.csv` alongside a short `.md` note) with:
   - The exact date range pulled
   - The property ID confirmation (`G-DWNVZNWCT5`)
   - A one-line note on which channel-group taxonomy was used, so a future analyst doesn't need to guess
6. Once saved, ping growth-analyst or integration-devops to fold it into `analytics-reports/2026-08-10-acquisition-collapse.md` (hypothesis H5, currently OPEN – "was any real website traffic lost, not just tracking") and to close out task C2 fully.

This step is independent of, and should happen **before**, the S6 consent-gate fix (task plan explicitly flags this ordering).

## C3 – filter out internal/test traffic

### Volume verified (14d, 2026-08-10)

Within `properties.$lib = 'posthog-flutter'` (6,307 events / 94 users, 14d):

| flag | events | distinct users |
|---|---|---|
| `$is_testflight = true` | 693 | 3 |
| `$is_emulator = true` | 165 | 3 |
| either true (union) | 858 | 6 (the two 3-user sets do not overlap) |

858 of 14,026 total-project events (all `$lib` values) = **~6.1%**, matching the task-plan's "ok. 6%" estimate almost exactly. As a share of app-only volume it is higher: 858/6,307 = **13.6%**.

### Reliability – the two flags are NOT equally trustworthy

- **`$is_emulator`**: present on **100%** of `posthog-flutter` events (6,307/6,307). Fully reliable – safe to filter on directly.
- **`$is_testflight`**: present on only **~22–25%** of `posthog-flutter` events on the two current builds (2.0.76: 731/3,028 = 24.1%; 2.0.75: 685/3,005 = 22.8%), higher on the older still-active 2.0.60 (127/188 = 67.6%), and **completely absent** on legacy builds 2.0.44/2.0.36 (property didn't exist yet). Coverage is roughly uniform across event *types* at a given app version (e.g. on `$screen` 469/1,876 = 25%, on `tab_switched` 393/1,770 = 22%) – this looks like a timing/async gap in when the Flutter client attaches the property within a session, not an omission on specific event types. Root cause not diagnosed here (would need flutter-mobile to check the analytics-init code path).
- **Practical consequence**: a query gated on `$is_testflight = true` **under-counts** actual TestFlight-origin traffic – only about 1 in 4 of those events are tagged on the current build. **Report the 693-event / 13.6% figure as a floor, not a precise measurement.**
- Both flags are **client-only**: `posthog-python` (backend) and `web` events never carry either key (0/0 confirmed for both in this check). A backend-triggered event from an internal account cannot be excluded by these flags.

### Default exclusion clause (documented in agent memory per task instruction)

```
properties.$is_testflight != true AND properties.$is_emulator != true
```

**NULL-safety verified explicitly** (this matters because a related HogQL gotcha – `properties.X != ''` silently drops rows where the key is missing – is already documented for string-presence checks in `posthog-data-extractor`'s memory): `countIf(properties.$is_testflight != true)` returned exactly the same count (5,614) as the explicit `countIf(NOT JSONHas(...) OR ... = false)` form, over the same 6,307-event flutter set. A boolean `!= true` comparison against a *missing* key does **not** silently exclude the row here – so the exclusion clause above is safe to use as-is, no `JSONHas` guard required. (Re-check this if the ClickHouse/HogQL version ever changes – it is an engine-behaviour observation, not a documented guarantee.)

### `internal_user` person property – assessed, not implemented

Per the task, this was evaluated only:

- **Would help**: it is person-level, not per-event, so one `$set`/identify call at login covers every subsequent event for that person for the rest of their history – closing exactly the gap `$is_testflight`'s partial coverage leaves open. It would also be the *only* way to exclude backend-emitted (`posthog-python`) activity from a known internal account, since the two existing flags are client-only. The 6 already-known internal person_ids (3 testflight-flagged, 3 emulator-flagged, no overlap) are a natural seed list.
- **Would cost**: requires an actual code change (backend-api or data-analytics territory: an allowlist – email domain or explicit admin flag on the `users` table – plumbed through to the PostHog `$set`/`identify` call) and ongoing maintenance (staleness risk when team membership changes, same class of problem as any allowlist).
- **Recommendation**: not blocking. The two existing flags plus reporting the "floor, not precise" caveat above are sufficient for now; revisit if internal traffic keeps producing false alarms in growth reporting.

## C7 – exclude automated (bot) traffic

Follow-up to growth-analyst's `analytics-reports/2026-08-10-anonymous-users-analysis.md`
finding F1: 151 of the 430 "never authenticated" app-first persons in the 2026-05-01..07-26
cohort sit on exactly two device models (`OnePlus8Pro`, `Pixel 6 Pro`) with a behavioral
signature (one session per app-store build, rotating locale on a fixed US IP, ~223s
sessions, reaching the auth screen more often than real users but almost never converting)
that matches Google Play's pre-launch report device farm, though this is not independently
confirmed (see below). Growth-analyst's report proposed this as a query-time filter
(R1 step 2) pending an operator check of Play Console.

### Signature verification – independent re-check, 2026-08-10

Re-ran the person-level breakdown for the same 05-01..07-26 window and cohort
(`properties.$lib='posthog-flutter' AND properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')`,
159 distinct persons total – slightly above growth-analyst's 151 because their number was
already net of other exclusions):

| check | result |
|---|---|
| persons with zero `user_registered`/`user_logged_in` AND zero screens beyond `splash`/`auth`/`signUp`/`forgotPassword` | **154 / 159 (96.9%)** – unambiguous bot |
| persons reaching a post-auth screen (`mainPage`) in a single ~5-15s session, one `$app_version`, without ever firing a login/register event first | 3 / 159 – distinct sub-pattern, still excluded as bot, flagged below as a possible client bug |
| persons with genuine multi-session engagement | 2 / 159 – see below, neither is a reason to loosen the filter |

**Both engaged persons examined individually, because this is exactly the "does the
signature accidentally sweep up real humans" check the task asked for:**

1. One person: 25 distinct `$app_version`s, 76 `user_logged_in` events, 1,716 non-gate-screen
   events, active 2026-05-02 through **2026-08-04**, rotating across 6 countries/locales
   (IN, UA, RO, KZ, SA, US). This is not a plausible organic new user – it is either an
   internal QA/test device manually smoke-testing each release build, or a credentialed
   automation script. The very pattern that flags the rest of the cohort as bot (one
   session per build, locale rotation on device-model-consistent hardware) applies here
   too, just with real login credentials attached. **Correctly excluded from a "new
   organic user" cohort either way** – no narrowing needed on this account.
2. One person: 300 events, exactly 1 `$app_version`, 1 login, single country/locale (CA /
   en-US), 12-day window. This is the most plausible genuine real owner of one of these two
   phone models. It is the "marginal collateral damage" growth-analyst's own report already
   flagged and accepted (OnePlus has ~1-2% Android market share). **At most 1/159 (0.6%)
   sampled persons is a plausible false positive.**

**Verdict: signature confirmed, no narrowing required for the dashboard-hygiene use case.**
$device_model alone (without an added `$geoip_country_code='US'` or `$is_emulator=false`
condition) already gives ~99% precision on this sample; adding more conditions would only
reduce recall against a source that self-selects for hardware, not geography (the earlier
report already showed geo/locale rotation is *part of* the bot signature, not a filter to
apply on top of it).

**Two things this re-check surfaces that were not in the source report:**

- **Correction – this traffic did NOT stop on 2026-07-26.** The source report frames R1 as
  cleanup for "mostly historical series" because no new `OnePlus8Pro` persons appeared after
  the week of 07-26. Re-verification found fresh bot-pattern-consistent `Pixel 6 Pro`
  sessions on **2026-08-05** (new person, 12 events, single build) and **2026-08-10 – the
  same day as this check** (new person, 3 events, single build), both matching the pure-bot
  signature exactly (one `$app_version`, zero non-gate screens, minutes-long session).
  **This is a standing exclusion needed for current and future dashboards, not a one-time
  backfill.**
- **Possible separate bug (not this agent's file to fix, flagging for flutter-mobile):** the
  3 "reaches `mainPage` without logging in" sessions above are each 4-7 events over a few
  seconds, single build, and otherwise match the bot signature – most likely still
  automated traffic hitting a client-side auth-state edge case rather than evidence of a
  real account, but worth a look if it recurs at higher volume.
- **Source of the traffic remains unconfirmed.** Neither `OnePlus 8 Pro` nor `Pixel 6 Pro`
  appear in the public Firebase Test Lab device catalog (per the source report, checked Feb
  2026), so the Google Play pre-launch report attribution is a working hypothesis, not a
  fact. Confirming it requires a human to open Play Console → Testing → Pre-launch report
  and check the device list for May-July runs – an operator step, unchanged from the source
  report's own instruction, not something this session can do.

### Filter added

`scripts/posthog_build_dashboards.py`: added `BOT_DEVICE_MODEL_FILTER` (`properties.$device_model
NOT IN ('OnePlus8Pro', 'Pixel 6 Pro')`, PostHog `is_not` operator) to `CLIENT_HYGIENE_FILTERS`
alongside the existing `$lib`/`$is_testflight`/`$is_emulator` filters (module docstring item 1,
and the "Hygiene filters" block above `event_series()`). It is applied automatically to every
`event_series(..., client=True)` call – i.e. every Flutter-emitted series on all 9 dashboards
picks it up the next time the script is run with `--update`. Nothing was executed against
PostHog in this session; the script change is unrun, matching how the C2/C3 filters were
handled (rebuild is task C4, operator-run).

### Deliverable status vs DONE_WHEN

C7 DONE_WHEN (verify signature, add filter to the dashboard-build script, update
posthog-data-extractor memory + this report): **done.** Signature confirmed at ~99% precision
with no narrowing required; filter wired into `scripts/posthog_build_dashboards.py`
(unrun); `.claude/agent-memory/posthog-data-extractor/reference_default_exclusion_filters.md`
updated with a new section 3 + its MEMORY.md index line. Play Console source confirmation
remains an operator step, same as the source report already stated.

## What was written to agent memory

- **New file** (this session's earlier C2/C3 pass): `.claude/agent-memory/posthog-data-extractor/reference_default_exclusion_filters.md` – full canonical filters (C2's `$lib` split and C3's internal-traffic exclusion), the fresh verification numbers above, the `$is_testflight` coverage caveat, the NULL-safety verification, and the `internal_user` assessment. Links to (does not duplicate) growth-analyst's existing `reference_posthog_web_vs_app_split.md`, which already owns the full web-vs-app mechanism/history.
- **Updated** (C7 pass): same file – added section 3 (bot-traffic filter, signature verification, the two-person deep-dive, the "still active today" correction, and the unresolved-source caveat).
- **Updated**: `.claude/agent-memory/posthog-data-extractor/MEMORY.md` – added a one-line pointer under a new "Default filters" section at the top of the index, ahead of the Access section, so it's the first thing read before any app-metrics query; extended in the C7 pass with the `$device_model` filter, its precision, and the "still active" caveat.
- **Updated**: `.claude/agent-memory/integration-devops/MEMORY.md` – recorded that direct `posthog_query.py` access works from this agent too, the GA4-access-absence finding (so it isn't re-investigated from scratch next time), and a pointer to this report.
- `growth-analyst`'s memory file was deliberately **not edited** (out of ownership; its content on the `$lib` mechanism and consent-gate history is already correct and current – this task only added the C3-specific material and fresh C2 numbers elsewhere, per the "don't duplicate, only supplement" instruction).

## Deliverable status vs DONE_WHEN

- C2 DONE_WHEN ("dashboards show app actives without web traffic, and the historical www series from GA4 is pulled and archived"): **filter confirmed and documented** (dashboard application itself is task C4, operator-run, out of scope here); **GA4 pull NOT done** – operator action required, instructions above, time-sensitive ahead of S6.
- C3 DONE_WHEN ("dashboards and default queries exclude internal traffic, and the rule is recorded in agent memory"): **filter confirmed, documented, and written to posthog-data-extractor's memory** (dashboard application is C4); `internal_user` option assessed per instruction, not implemented.
