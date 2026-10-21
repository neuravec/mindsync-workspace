---
name: default-exclusion-filters
description: Canonical WHERE-clause filters to run BY DEFAULT on any "app metrics" pull - exclude marketing-site traffic ($lib), internal/test traffic ($is_testflight, $is_emulator), and automated bot traffic ($device_model). Read before any DAU/WAU/actives/funnel query.
metadata:
  type: reference
---

# Default exclusion filters for app-metrics queries

Two traffic classes contaminate almost every naive `count(DISTINCT person_id)` /
`count()` query against `events` in project 141170 and should be excluded (or at
minimum reported alongside the unfiltered number) unless the question is
specifically about web traffic or internal QA activity.

## 1. Marketing-site (web) traffic - filter by `$lib`

Full mechanism, history and the 2026-07-25 consent-gate context already live in
`growth-analyst`'s [[posthog-web-vs-app-split]]
(`.claude/agent-memory/growth-analyst/reference_posthog_web_vs_app_split.md`) -
read that first, this section only adds fresh verification numbers.

**Canonical filter for "app" metrics**: `properties.$lib = 'posthog-flutter'`.
**Canonical filter for "web" metrics**: `properties.$lib = 'web'`. Backend-emitted
events use `properties.$lib = 'posthog-python'` (no `$os`/`$app_version`, never
`$is_testflight`/`$is_emulator` either - see below).

Re-verified 2026-08-10 (fresh, independent of the growth-analyst report run
earlier the same day - numbers drift a few users between runs, see person-merge
caveat in [[posthog-web-vs-app-split]]):

| lib | events (14d) | users (14d) | events (prior 14d) | users (prior 14d) |
|---|---|---|---|---|
| posthog-flutter (app) | 6,307 | 94 | 6,231 | 81 |
| web (marketing site) | 143 | 28 | 893 | 176 |
| posthog-python (backend) | 7,576 | 67 | 1,734 | 40 |

Confirms the post-2026-07-25 consent-gate pattern holds two weeks later: web
volume down ~84% period over period, app volume up. `properties.$lib` coverage
is 100% - `countIf(NOT JSONHas(properties,'$lib'))` over the same 14d window = 0
of 14,026 events. Safe to filter on unconditionally, no fallback needed.

## 2. Internal/test traffic - filter by `$is_testflight` / `$is_emulator`

**Default exclusion clause**: `properties.$is_testflight != true AND properties.$is_emulator != true`.

Verified 2026-08-10, `properties.$lib = 'posthog-flutter'` scope, 14d window
(6,307 events / 94 users total):

| flag | events | distinct users |
|---|---|---|
| `$is_testflight = true` | 693 | 3 |
| `$is_emulator = true` | 165 | 3 |
| either true (union) | 858 | 6 (no overlap between the two 3-user sets) |

858 / 14,026 total-project events = ~6.1% of all-project volume, matching the
task-plan's "ok. 6%" estimate. As a share of app-only volume it is 858/6,307 = 13.6%.

**Reliability - asymmetric coverage between the two flags, but `$is_testflight`
IS reliable once you condition on OS (root-caused 2026-08-10, see below):**
- `$is_emulator`: present on 100% of `posthog-flutter` events (6,307/6,307). Fully
  reliable, all platforms.
- `$is_testflight`: present on only ~22-25% of `posthog-flutter` events in the
  RAW aggregate on current builds (2.0.76: 731/3,028 = 24.1%; 2.0.75: 685/3,005 =
  22.8%). **This aggregate number is misleading on its own** - it is NOT a
  coverage gap or async timing bug. Root cause confirmed 2026-08-10
  (`analytics-reports/raw/2026-08-10-testflight-coverage-os-split.md`, spawned
  by flutter-mobile for C3-fix): coverage is **100.00% on iOS/iPadOS and 0% on
  Android** (TestFlight doesn't exist on Android - the property is structurally
  inapplicable, not missing). Checked at both aggregate level (1532/1532 iOS
  events, 16 users) and per-session level (15 sampled iOS sessions, 36-252
  events each, zero mixed sessions - every session is either all-present or
  the concept doesn't apply). iOS+iPadOS = ~24.5% of all `posthog-flutter`
  events in the 14d window, which is *exactly* the "~24% aggregate coverage"
  number - fully explained by platform mix. The 2.0.60 anomaly (127/188 =
  67.6%) and absence on 2.0.44/2.0.36 (0%) are separate, real historical facts
  (older builds truly predate the property) but are NOT evidence of a
  per-event race - do not re-open that hypothesis without new session-level
  counter-evidence.
- **Practical consequence - CORRECTED**: `$is_testflight = true` is a reliable,
  complete signal **on iOS**, not a floor/undercount. On Android it is simply
  never applicable (0% is the correct, expected value, not missing data). When
  gating a query on `$is_testflight`, restrict to `properties.$os IN ('iOS',
  'iPadOS')` first if you want the true testflight population - do not apply
  the flag project-wide and read a low aggregate rate as a data-quality problem.
- `$is_testflight`/`$is_emulator` are **client-only properties** - `posthog-python`
  (backend) and `web` events never carry either key (both 0/0 in the 2026-08-10
  check). A backend-emitted event cannot be excluded this way; if internal
  backend-triggered activity needs excluding, it has to go through a different
  signal (e.g. a known internal user_id list) - see the `internal_user` option below.

**NULL-safety of the `!=` filter (verified, do not assume the general HogQL
`!=` gotcha applies here):** `countIf(properties.$is_testflight != true)` on the
flutter-only 14d set returned exactly the same count (5,614) as the explicit
`countIf(NOT JSONHas(...) OR ... = false)` form. Unlike the documented
`properties.X != ''` presence gotcha in [[posthog-access-fallback]], a boolean
`!= true` comparison against a MISSING key behaves as "not true" here (does not
silently drop rows), so `$is_testflight != true AND $is_emulator != true` is
safe to use directly as a default exclusion clause without an explicit
`JSONHas` guard. Re-verify this if HogQL/ClickHouse version changes.

### `internal_user` person-property option (evaluated, not implemented)

Task C3 asked to *assess* (not build) tagging known team accounts with an
`internal_user` person property as a more reliable alternative/supplement to
the two flags above. Assessment, for whoever picks this up (backend-api or
data-analytics would own the emission point):

- **Pro**: person-level (not per-event), so it would not suffer the
  `$is_testflight` per-platform-inapplicability above - one `$set`/identify call
  covers every subsequent event for that person, and it would also cover
  backend-emitted (`posthog-python`) events for that same person_id, closing
  the gap the two client-only flags cannot close.
  Also covers non-TestFlight, non-emulator internal use (e.g. a team member's
  personal production device/account), which today has no signal at all.
  Six person_ids are already known-internal today (3 testflight + 3 emulator,
  no overlap) - a natural seed list, though not owned/maintained by this agent.
- **Con / cost**: needs a maintained allowlist (email domain, UID list, or an
  explicit admin flag in the `users` table) plumbed through to the PostHog
  `$set`/`identify` call - an actual code change in backend-api/data-analytics
  territory, not a query-time filter. Risk of staleness (someone leaves the
  team, account isn't untagged) is the same class of problem as any allowlist.
- **Recommendation**: worth doing if internal traffic keeps being a source of
  false alarms in growth reporting, but the two existing flags plus reporting
  the "$is_testflight is iOS-only" caveat above is sufficient for now. Not blocking.

## 3. Automated/bot traffic - filter by `$device_model` (task C7, 2026-08-10)

Source: `analytics-reports/2026-08-10-anonymous-users-analysis.md` (growth-analyst,
finding F1). Independently re-verified by integration-devops 2026-08-10, see
`analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md` section C7 for the queries.

**Default exclusion clause**: `properties.$device_model NOT IN ('OnePlus8Pro', 'Pixel 6 Pro')`,
scoped to `properties.$lib = 'posthog-flutter'` (client-only property, same as
`$is_testflight`/`$is_emulator` - `posthog-python` and `web` events never carry it).

**Signature and precision (re-verified independently, 05-01..07-26 window, 159 persons
total on these two device models):**
- 154/159 (96.9%) are unambiguous bot: zero `user_registered`/`user_logged_in`, zero
  screens beyond `splash`/`auth`/`signUp`/`forgotPassword`.
- 3/159 are a distinct sub-pattern worth a flutter-mobile look: single ~5-15s session,
  one `$app_version`, reaches `mainPage` (a post-auth screen) WITHOUT ever firing
  `user_logged_in`/`user_registered` first. Possibly a client-side auth-state race/bug
  transiently rendering `mainPage`, not evidence of a real account - still excluded as
  bot for hygiene purposes, but flagged as a possible separate bug.
- 2/159 have genuine engagement and should NOT be read as proof the filter is unsafe:
  - One person (25 `$app_version`s, 76 `user_logged_in` events, 1716 non-gate-screen
    events, active 2026-05-02..08-04, rotating across 6 countries/locales) is almost
    certainly an internal QA/test device or a credentialed automation script, not an
    organic new user - the very pattern (one session per build, locale rotation) that
    flags the rest of the cohort as non-human also applies here, just with real
    credentials attached. Excluding it from growth "new user" cohorts is correct
    regardless of whether it is literally a device-farm bot.
  - One person (300 events, 1 `$app_version`, 1 login, single country/locale, 12-day
    window) is the most plausible genuine real owner of the phone model - this is the
    "marginal collateral damage" the source report already accepted (OnePlus has
    ~1-2% Android market share). **No narrowing needed**: at most 1/159 (0.6%) sampled
    persons is a plausible false-positive under the blunt device-model filter.
- **Verdict: signature confirmed at the precision needed for dashboard hygiene.** Do
  not narrow further (e.g. by requiring `$geoip_country_code='US'` too) unless a future
  audit finds a materially higher false-positive rate - the current one is negligible.

**Source of the traffic - still NOT independently confirmed.** The behavioral profile
(one session per app-store build, locale rotation, fixed US IP, ~223s sessions, reaches
`auth` more often than humans but never converts) matches Google Play's documented
pre-launch report device farm, but neither `OnePlus 8 Pro` nor `Pixel 6 Pro` appear in
the public Firebase Test Lab device catalog (checked Feb 2026). Confirming this requires
a human to open Play Console > Testing > Pre-launch report and check the device list -
an operator step, not something an agent session can do. Treat the "Google pre-launch
report" attribution as a working hypothesis, not a fact, until that check happens.

**CORRECTION to the source report's timing claim - this traffic is ONGOING, not purely
historical.** The source report states the traffic "stopped after 2026-07-19" (zero
*new* `OnePlus8Pro` persons since the week of 07-26). Re-verification on 2026-08-10
found bot-pattern-consistent events on `Pixel 6 Pro` as recently as **2026-08-05** (a
new person, 12 events, single session) and **2026-08-10 - the same day as this
verification** (a new person, 3 events, single session), both fully matching the pure-bot
signature (single app_version, zero non-gate screens). **Do not treat this filter as a
one-time backfill for old dashboard series - it is a standing exclusion needed for
current and future queries too.**

See also [[posthog-web-vs-app-split]], [[posthog-access-fallback]],
[[posthog-flowing-events-baselines]].
