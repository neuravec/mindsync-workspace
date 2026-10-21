"""
Build / update the PostHog dashboards for MindSync.

##########################################################################
# READ THIS BEFORE ADDING OR EDITING ANY INSIGHT: the $lib convention.
##########################################################################
Every event in this project carries a `$lib` property naming the SDK that sent
it. There are exactly three values, and they are three different populations:

    $lib = 'posthog-flutter'  -> the mobile app. THE ONLY SOURCE THAT MEANS
                                 "a human used MindSync".
    $lib = 'posthog-python'   -> the backend: API handlers, RQ worker, cron
                                 jobs. A person_id here means "the server did
                                 something ABOUT this user", not "this user
                                 did something".
    $lib = 'web'              -> the Webflow marketing site (www.mindsync.app).
                                 Real humans, but visitors, not app users.

WHY THIS MATTERS (the 2026-08-16 fix, analytics-reports/2026-08-16-post-release-review-12-08.md §2):
On 2026-08-11 backend commit 177c026 repaired a missing PostHog init in the RQ
worker dyno. Background jobs started emitting server-side events for the first
time ever – mostly moment.scheduled / moment.sent, fired for essentially the
WHOLE user base every single day. PostHog counts the person_id on those events
as an active user, so unfiltered "daily active users" jumped from ~20 to ~1750
overnight while the real number never moved (12–17 humans/day). Anyone reading
an unfiltered dashboard is off by two orders of magnitude.

THE RULES:
 1. Any insight that is meant to read as HUMAN APP USAGE – DAU/WAU/MAU,
    retention, stickiness, lifecycle, activation, onboarding/monetization
    funnels, feature adoption, anything counting distinct users – must pin
    $lib = 'posthog-flutter'. In this script that is source=SOURCE_APP, which
    is the DEFAULT, so you get it for free unless you opt out.
 2. NEVER write a blanket "$lib != 'posthog-python'" instead. That still lets
    Webflow ('web') traffic into app metrics. Pin the source you want; do not
    subtract the one you don't.
 3. Opting out is an explicit, justified decision, not a shrug. Pick the
    accurate source:
      SOURCE_BACKEND – the event only ever fires server-side (api_error,
                       user_activated, weekly_summary_generated, moment.*).
      SOURCE_WEB     – marketing-site event ($pageview, $web_vitals,
                       app_store_click).
      SOURCE_ANY     – VERIFIED dual-sourced: the same logical action fires
                       from BOTH the app and the backend, so pinning either
                       one would undercount (today: consent_granted,
                       subscription_purchase_completed). Only use this after
                       running the check below; "I'm not sure" is not a reason.
 4. Before assigning a source to a new event, verify it – do not guess from
    the file it lives in:
        python scripts/posthog_query.py --sql "SELECT event, properties.\\$lib,
          count() FROM events WHERE timestamp > now() - INTERVAL 90 DAY
          GROUP BY 1,2 ORDER BY 3 DESC"
    Guessing has already burned this project twice: notification_received
    reads like a backend event and is 100% client; consent_revoked reads like
    a client event and is 100% backend.
 5. Server-side behaviour is not noise to be discarded – it is its own signal.
    It lives on the "Backend & Jobs (server-side)" dashboard built by
    build_backend_jobs(), where person counts are explicitly labelled as
    "users the server acted on", never as active users.
##########################################################################

--------------------------------------------------------------------------
2026-08-16 FIX (measurement bug: dashboards reporting ~130x too many users).
  - `event_series(client=True/False)` became `event_series(source=...)`.
    The old boolean had one true meaning and three false ones: client=False
    was used for backend-only, web-only AND dual-sourced events alike, so it
    silently degraded to "no $lib filter at all". That escape hatch is how an
    unfiltered series gets written by accident. The four sources are now named
    and each applies a positive pin (except SOURCE_ANY, which is deliberate).
  - Same change on retention(target_source=/returning_source=), lifecycle(source=)
    and stickiness(source=). The `client=` kwarg is GONE, not deprecated, so a
    stale call site raises TypeError instead of silently going unfiltered.
  - CLIENT_HYGIENE_FILTERS renamed APP_HYGIENE_FILTERS (same contents).
  - BUG FIXED: "App store deep-link clicks" (Monetization) was pinned to
    $lib='posthog-flutter', but app_store_click is a WEB event – verified 85
    events / 180d, 100% $lib='web', 0 posthog-flutter. That insight has been
    reading a hard zero since the hygiene filters were written. Now SOURCE_WEB.
  - NEW dashboard: "Backend & Jobs (server-side)" – moment pipeline, job
    output, server-side failures. Keeps the signal that caused the false DAU
    spike visible and correctly named instead of just filtering it away.
  Source classifications in this file were re-verified against live PostHog on
  2026-08-16 (90d window, event x $lib matrix); only 4 events in the whole
  project are dual-sourced, 2 of which this script uses.
--------------------------------------------------------------------------

--------------------------------------------------------------------------
2026-08-10 REBUILD (task C4, analytics-reports/2026-08-10-posthog-audit-taskplan.md).
Full rationale + per-dashboard diff: analytics-reports/2026-08-10-dashboards-rebuild-plan.md.
This is a REBUILD of the original 2026-04-23 script, not a fresh file. Summary of
what changed and why:

1. Hygiene filters (tasks C2/C3/C7, analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md).
   Every client-emitted (Flutter) event series now carries, by default:
     - properties.$lib = 'posthog-flutter'   (excludes the marketing-site / web SDK)
     - properties.$is_testflight != true      (excludes internal TestFlight testers)
     - properties.$is_emulator != true        (excludes emulator/simulator traffic)
     - properties.$device_model NOT IN ('OnePlus8Pro', 'Pixel 6 Pro')  (task C7 --
       excludes automated/bot traffic, most likely Google Play's pre-launch report
       device farm; see BOT_DEVICE_MODEL_FILTER below and the C7 section of the
       C2/C3 report for the verification query and confidence caveats)
   (NOTE, 2026-08-16: the API described in this 2026-08-10 section — the
   CLIENT_HYGIENE_FILTERS name and the client=True/False kwarg — was superseded
   by APP_HYGIENE_FILTERS and source=SOURCE_*. The reasoning below still holds
   verbatim; only the spelling changed. See the 2026-08-16 section above.)
   See APP_HYGIENE_FILTERS below. Backend-emitted (posthog-python) events never
   carry $lib='posthog-flutter' or the three test/emulator/bot flags at all (client-only
   properties -- see the C2/C3 report), so the filter is applied per-series via
   event_series(..., client=True/False) rather than once globally -- a query that
   mixes a client series with a backend series (e.g. the Reflect engagement pair)
   would otherwise zero out the backend side.
   CAVEAT: this uses the PostHog UI "is_not" property-filter operator, which is
   assumed (not independently verified against the raw HogQL `!=` NULL-safety
   check documented in the C2/C3 report) to have the same NULL-safe behavior.
   Operator should spot-check one insight's number against a raw
   `scripts/posthog_query.py --sql` count after running with --update.

   IMPORTANT correction made mid-rebuild (flagged by a parallel B7 finding):
   client vs. backend origin was NOT assumed from filenames/comments -- every
   event used in this script was checked with a fresh
   `SELECT event, properties.$lib, count() ... GROUP BY event, lib` query on
   2026-08-10 before its client=True/False was assigned. That check surfaced:
     - notification_received is CLIENT-only (100% posthog-flutter) -- an earlier
       draft misclassified it as backend from a doc-comment in
       notification_orchestrator_job.py that only *names* the client event.
     - Some events are DUAL-SOURCED (fire from both the client and the backend
       for the same logical action) and therefore use client=False (NO $lib
       filter at all, so neither side is dropped) even though they read like
       ordinary client events: subscription_purchase_completed (5
       posthog-flutter + 3 posthog-python /90d) and consent_granted (16
       posthog-flutter + 18 posthog-python /90d).
     - consent_revoked is the mirror case: BACKEND-ONLY (0 posthog-flutter),
       so it also needs client=False, but for the opposite reason (a
       $lib=posthog-flutter filter would silently zero it, not double-count it).
   See analytics-reports/2026-08-10-dashboards-rebuild-plan.md for the full
   per-insight table of which filter variant each one uses and why.

2. Rename: notification_interest_toggled -> notification_row_toggled (FE commit
   4a20b19, 2026-07-24). Schema also changed: category/selected -> key/value.
   The old insight "Notification preference changes" (which actually referenced
   an even earlier dead event, notification_preference_changed -- silent since
   2026-05-21) is retired; a new insight "Notification row toggles (key/value)"
   replaces it on the Account Health dashboard, breakdown by `key` not
   `preference_type`.

3. Reflect engagement semantics corrected. reflect_session_started AND
   reflect_session_ended are BOTH backend-emitted (app/api/v1/endpoints/reflect.py)
   and mark the THREAD's lifecycle -- reflect_session_ended only fires on the
   explicit "End Reflection" action (finalizes the thread, enqueues paid OpenAI
   analysis), so in production it undercounts real usage ~12x versus
   reflect_session_started. reflect_ui_session_ended is a separate, CLIENT-emitted
   event (added 2026-08-10) that measures actual on-screen engagement across every
   exit path. Engagement dashboards pair reflect_session_started (backend) with
   reflect_ui_session_ended (client) -- never reflect_session_ended alone.

4. api_error quality split (S1 fix, backend commit 7696f40, app/main.py). Every
   api_error event now carries `is_expected` (bool) distinguishing designed 4xx
   behavior (empty states, premium/limit gates) from real failures. NOTE: as of
   this rebuild the fix is committed but NOT deployed to Heroku -- is_expected is
   NULL on 100% of api_error events in the live 14d window (verified via
   posthog_query.py, 2026-08-10). The "real failures only" insight will read empty
   until the operator deploys that commit; see the rebuild-plan report.

5. New events covered (added across several 2026-08-04..2026-08-10 batches; many
   are also NOT YET DEPLOYED -- see the rebuild-plan report for the exact
   populated-vs-empty-until-deploy list): workspace_opened, app_tour_*, consent_*,
   signup_*, account_screen_opened/account_deletion_*, quick_capture_*,
   prep_capture_*, voice_transcription_*, reflect_ui_session_ended,
   notification_permission_*, paywall_shown, subscription_restore_*,
   summary_viewed, weekly_summary_generated, monthly_audit_generated,
   user_activated, recording_abandoned, realization_detected.

6. Insights on events with zero volume and no committed instrumentation plan are
   marked "[awaiting instrumentation]" in their description rather than silently
   included or silently dropped (task C1 is still in progress) -- see
   AWAITING_DEPLOY_NOTE usages below for events that DO have code but aren't live
   in prod yet (a different, more solvable state than "awaiting instrumentation").

Reality as of 2026-04-23 (ORIGINAL, superseded by the above): project started
ingesting 2026-04-22 -> only ~2 days of data; 22 custom events flowing.
--------------------------------------------------------------------------

Usage:
    POSTHOG_PERSONAL_API_KEY=phx_... POSTHOG_PROJECT_ID=141170 \\
        python scripts/posthog_build_dashboards.py [--dry-run] [--force] [--update] [--retire-dead]

    --dry-run       Print actions without POSTing/PATCHing anything.
    --force         Create insights even if one with the same name exists (duplicates).
    --update        PATCH the query+description of insights that already exist by name,
                     instead of skipping them. THIS is what actually propagates the
                     2026-08-10 hygiene-filter / rename / new-series changes onto the
                     live 638505-638513 dashboards built by the original 2026-04-23 run.
                     Without --update, re-running this script against the existing
                     dashboards is a no-op (idempotent skip-if-exists), same as before.
    --retire-dead   Soft-delete the specific named insights in RETIRED_INSIGHTS below
                     (superseded-by-rename insights only -- see item 2 above). Separate
                     opt-in flag because deletion is more destructive than update.

Idempotency: by default, skips any dashboard/insight whose exact name already exists.
--update changes the insight branch of that to "PATCH instead of skip". --force always
creates a new one regardless (duplicates). Dashboards are never duplicated by --force.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

PERSONAL_API_KEY = os.environ.get("POSTHOG_PERSONAL_API_KEY")
PROJECT_ID = os.environ.get("POSTHOG_PROJECT_ID")
HOST = os.environ.get("POSTHOG_HOST", "https://eu.i.posthog.com")
# UI host is different from the ingestion host — eu.i.posthog.com serves the API,
# eu.posthog.com serves the web UI where dashboards render.
UI_HOST = HOST.replace("://eu.i.", "://eu.").replace("://us.i.", "://us.")

if not PERSONAL_API_KEY or not PROJECT_ID:
    print("ERROR: set POSTHOG_PERSONAL_API_KEY and POSTHOG_PROJECT_ID env vars.", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {PERSONAL_API_KEY}",
    "Content-Type": "application/json",
}

DRY_RUN = False
FORCE = False
UPDATE = False
RETIRE_DEAD = False


def _req(method: str, path: str, body=None):
    url = f"{HOST}/api/projects/{PROJECT_ID}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = resp.read().decode("utf-8")
            return json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} on {method} {path}: {body_text}", file=sys.stderr)
        raise


def find_dashboard_by_name(name: str):
    q = urllib.parse.urlencode({"search": name, "limit": 50})
    res = _req("GET", f"/dashboards/?{q}")
    for d in res.get("results", []):
        if d.get("name") == name and not d.get("deleted"):
            return d
    return None


def create_dashboard(name: str, description: str, tags=None) -> int:
    existing = find_dashboard_by_name(name)
    if existing and not FORCE:
        print(f"[=] dashboard {existing['id']}  {name}  (exists — skipping)")
        return existing["id"]
    if DRY_RUN:
        print(f"[dry] would create dashboard: {name}")
        return -1
    body = {"name": name, "description": description, "pinned": False}
    if tags:
        body["tags"] = tags
    res = _req("POST", "/dashboards/", body)
    print(f"[+] dashboard {res['id']}  {name}")
    return res["id"]


# dashboard_id -> {insight_name: insight_id}, populated lazily.
_dashboard_insight_cache: dict[int, dict[str, int]] = {}


def _get_existing_insights(dashboard_id: int) -> dict[str, int]:
    """Return {name: insight_id} for non-deleted insights already attached to the
    dashboard. Caches per dashboard to avoid refetching on every insight call."""
    if dashboard_id in _dashboard_insight_cache:
        return _dashboard_insight_cache[dashboard_id]
    res = _req("GET", f"/dashboards/{dashboard_id}/")
    mapping: dict[str, int] = {}
    for tile in res.get("tiles") or []:
        insight = tile.get("insight") or {}
        name = insight.get("name")
        if name and not insight.get("deleted"):
            mapping[name] = insight["id"]
    _dashboard_insight_cache[dashboard_id] = mapping
    return mapping


def create_insight(dashboard_id: int, name: str, description: str, query: dict) -> int:
    """Create, update, or skip an insight by name, depending on flags:
      - name doesn't exist yet            -> create (unless --dry-run)
      - name exists, --update passed      -> PATCH query+description in place
      - name exists, --update NOT passed  -> skip (original 2026-04-23 behavior)
      - --force                           -> always create a new one (duplicate)
    """
    if dashboard_id == -1:
        print(f"    [dry] insight: {name}")
        return -1

    existing = _get_existing_insights(dashboard_id) if not FORCE else {}
    if name in existing:
        insight_id = existing[name]
        if UPDATE:
            if DRY_RUN:
                print(f"    [dry] would UPDATE insight {insight_id}  {name}")
                return insight_id
            _req("PATCH", f"/insights/{insight_id}/", {"description": description, "query": query})
            print(f"    [~] updated insight {insight_id}  {name}")
            return insight_id
        if DRY_RUN:
            print(f"    [dry] [=] skip (pass --update to refresh): {name}")
            return -1
        print(f"    [=] insight  {name}  (exists — skipping; pass --update to refresh query/description)")
        return -1

    if DRY_RUN:
        print(f"    [dry] [+] create: {name}")
        return -1
    body = {
        "name": name,
        "description": description,
        "query": query,
        "dashboards": [dashboard_id],
        "saved": True,
    }
    res = _req("POST", "/insights/", body)
    _dashboard_insight_cache.setdefault(dashboard_id, {})[name] = res["id"]
    print(f"    + insight {res['id']}  {name}")
    return res["id"]


# ---------------------------------------------------------------------------
# Retired insights (task C4, item 2 / item 6) — superseded by a differently-
# named replacement insight elsewhere in this same script, or dropped with no
# replacement because the underlying event has been dead a long time with no
# instrumentation plan attached to it. Only acted on when --retire-dead is
# passed (opt-in, separate from the default create/update pass).
# ---------------------------------------------------------------------------

RETIRED_INSIGHTS: dict[str, list[str]] = {
    # Referenced notification_preference_changed, dead since 2026-05-21 (silently
    # superseded twice: -> notification_interest_toggled -> notification_row_toggled).
    # Replaced by "Notification row toggles (key/value)" in build_account_health().
    "Account Health": ["Notification preference changes"],
    # Claimed "(9 steps)" but only 8 step_index values (0..7) have ever flowed
    # (task B6 — the 9th step is a real, still-open instrumentation gap, not a
    # renumbering). Replaced by "Onboarding funnel (8 of 9 known steps — see B6)".
    "Onboarding Health": ["Onboarding funnel (9 steps)"],
}


def retire_dead_insights() -> None:
    for dash_name, insight_names in RETIRED_INSIGHTS.items():
        d = find_dashboard_by_name(dash_name)
        if not d:
            print(f"[!] retire: dashboard not found: {dash_name}", file=sys.stderr)
            continue
        res = _req("GET", f"/dashboards/{d['id']}/")
        for tile in res.get("tiles") or []:
            insight = tile.get("insight") or {}
            if insight.get("name") in insight_names and not insight.get("deleted"):
                if DRY_RUN:
                    print(f"    [dry] would retire insight {insight['id']}  {insight['name']}")
                    continue
                _req("PATCH", f"/insights/{insight['id']}/", {"deleted": True})
                print(f"    [-] retired insight {insight['id']}  {insight['name']}")


# ---------------------------------------------------------------------------
# Hygiene filters (tasks C2/C3/C7) - see module docstring item 1.
# ---------------------------------------------------------------------------

APP_LIB_FILTER = {"type": "event", "key": "$lib", "operator": "exact", "value": ["posthog-flutter"]}
NOT_TESTFLIGHT_FILTER = {"type": "event", "key": "$is_testflight", "operator": "is_not", "value": [True]}
NOT_EMULATOR_FILTER = {"type": "event", "key": "$is_emulator", "operator": "is_not", "value": [True]}
# Task C7 (analytics-reports/2026-08-10-anonymous-users-analysis.md, finding F1;
# verified independently in analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md
# section C7). $device_model IN ('OnePlus8Pro', 'Pixel 6 Pro') matches automated,
# most-likely Google Play pre-launch-report traffic -- source not 100% confirmed,
# Play Console cross-check is an operator step (see report). Confirmed still active
# as of 2026-08-10 (today), not purely historical -- do not treat as a one-time
# backfill filter. ~99% precision on the 05-01..07-26 sample (154/159 persons pure
# bot; 5 borderline, of which at most 1 looks like a plausible genuine phone owner --
# accepted as marginal collateral, same call the source report already made).
BOT_DEVICE_MODEL_FILTER = {"type": "event", "key": "$device_model", "operator": "is_not",
                            "value": ["OnePlus8Pro", "Pixel 6 Pro"]}
APP_HYGIENE_FILTERS = [APP_LIB_FILTER, NOT_TESTFLIGHT_FILTER, NOT_EMULATOR_FILTER, BOT_DEVICE_MODEL_FILTER]

# --- $lib source pins (2026-08-16) -----------------------------------------
# See the "$lib convention" block at the top of this file. Each source applies a
# POSITIVE pin on $lib. We deliberately do NOT offer a "not posthog-python"
# filter: excluding the backend would still leave Webflow ('web') traffic inside
# app metrics, which is the same class of bug one layer down.
BACKEND_LIB_FILTER = {"type": "event", "key": "$lib", "operator": "exact", "value": ["posthog-python"]}
WEB_LIB_FILTER = {"type": "event", "key": "$lib", "operator": "exact", "value": ["web"]}

SOURCE_APP = "app"          # $lib='posthog-flutter' + testflight/emulator/bot hygiene. DEFAULT.
SOURCE_BACKEND = "backend"  # $lib='posthog-python'  – server-side only events.
SOURCE_WEB = "web"          # $lib='web'             – Webflow marketing site.
SOURCE_ANY = "any"          # NO $lib pin – ONLY for verified dual-sourced events.

_SOURCE_FILTERS: dict[str, list] = {
    SOURCE_APP: APP_HYGIENE_FILTERS,
    SOURCE_BACKEND: [BACKEND_LIB_FILTER],
    SOURCE_WEB: [WEB_LIB_FILTER],
    SOURCE_ANY: [],
}


def source_filters(source: str) -> list:
    """Return the $lib property filters for a source. Unknown source = hard error.

    Failing loudly matters here: a typo'd source that quietly fell through to
    "no filter" would reintroduce the exact bug this convention exists to stop.
    """
    if source not in _SOURCE_FILTERS:
        raise ValueError(
            f"unknown source {source!r}; expected one of "
            f"{sorted(_SOURCE_FILTERS)} – see the $lib convention block at the top of this file"
        )
    return list(_SOURCE_FILTERS[source])

# Appended to the NAME of insights whose underlying event has code shipped but
# is not yet deployed to Heroku prod / released to app stores (verified empty via
# posthog_query.py on 2026-08-10) — kept short so it doesn't dominate the tile
# title in the PostHog UI. Each such insight's own description additionally
# explains its specific deploy dependency; the full per-event verification table
# (which events, what volume, what commit) lives in
# analytics-reports/2026-08-10-dashboards-rebuild-plan.md, not duplicated here.
AWAITING_DEPLOY_NOTE = " [awaiting deploy]"

# ---------------------------------------------------------------------------
# Query builders
# ---------------------------------------------------------------------------


def event_series(event: str, math: str = "total", math_property: str | None = None,
                 properties: list | None = None, name: str | None = None,
                 source: str = SOURCE_APP):
    """Build one EventsNode series, pinned to a single $lib source.

    source=SOURCE_APP (default) applies APP_HYGIENE_FILTERS ($lib=posthog-flutter,
    excl. testflight/emulator/bot-device-model) — the correct choice for anything
    that is supposed to read as human app usage.

    Pass SOURCE_BACKEND for server-side-only events, SOURCE_WEB for marketing-site
    events, and SOURCE_ANY *only* for events verified to fire from both the app and
    the backend for the same logical action. See the $lib convention block at the
    top of this file; do not add a new SOURCE_ANY series without running the
    event x $lib verification query it documents.
    """
    node = {"kind": "EventsNode", "event": event, "name": name or event, "math": math}
    if math_property:
        node["math_property"] = math_property
    combined: list = source_filters(source)
    if properties:
        combined.extend(properties)
    if combined:
        node["properties"] = combined
    return node


def trends(series: list, date_from: str = "-14d", interval: str = "day",
           breakdown: dict | None = None, display: str = "ActionsLineGraph",
           formula: str | None = None):
    trends_filter: dict = {"display": display}
    if formula:
        trends_filter["formula"] = formula
    source = {
        "kind": "TrendsQuery",
        "series": series,
        "dateRange": {"date_from": date_from},
        "interval": interval,
        "trendsFilter": trends_filter,
    }
    if breakdown:
        source["breakdownFilter"] = breakdown
    return {"kind": "InsightVizNode", "source": source}


def funnel(series: list, date_from: str = "-14d",
           window_interval: int = 7, window_unit: str = "day",
           order_type: str = "ordered"):
    source = {
        "kind": "FunnelsQuery",
        "series": series,
        "dateRange": {"date_from": date_from},
        "funnelsFilter": {
            "funnelWindowInterval": window_interval,
            "funnelWindowIntervalUnit": window_unit,
            "funnelOrderType": order_type,
        },
    }
    return {"kind": "InsightVizNode", "source": source}


def retention(target_event: str, returning_event: str, period: str = "Day",
              total_intervals: int = 7, date_from: str = "-14d",
              target_source: str = SOURCE_APP, returning_source: str = SOURCE_APP):
    """Retention cohort. Both entities default to SOURCE_APP.

    Retention is a pure "did this human come back" question, so an unpinned
    entity is almost always a bug: a backend job touching a user every day would
    make that user look perfectly retained forever.
    """
    def _entity(event: str, source: str) -> dict:
        entity: dict = {"id": event, "name": event, "type": "events"}
        filters = source_filters(source)
        if filters:
            entity["properties"] = filters
        return entity

    return {
        "kind": "InsightVizNode",
        "source": {
            "kind": "RetentionQuery",
            "dateRange": {"date_from": date_from},
            "retentionFilter": {
                "period": period,
                "totalIntervals": total_intervals,
                "retentionType": "retention_first_time",
                "targetEntity": _entity(target_event, target_source),
                "returningEntity": _entity(returning_event, returning_source),
            },
        },
    }


def lifecycle(event: str, date_from: str = "-14d", interval: str = "day",
              source: str = SOURCE_APP):
    """New/returning/resurrecting/dormant. Defaults to SOURCE_APP — a lifecycle
    built on a backend event describes the job schedule, not the user."""
    return {
        "kind": "InsightVizNode",
        "source": {
            "kind": "LifecycleQuery",
            "series": [event_series(event, math="total", source=source)],
            "dateRange": {"date_from": date_from},
            "interval": interval,
            "lifecycleFilter": {"toggledLifecycles": ["new", "returning", "resurrecting", "dormant"]},
        },
    }


def stickiness(event: str, date_from: str = "-14d", source: str = SOURCE_APP):
    """Days-active-per-user. Defaults to SOURCE_APP; a daily backend job would
    otherwise report the entire user base as maximally sticky."""
    return {
        "kind": "InsightVizNode",
        "source": {
            "kind": "StickinessQuery",
            "series": [event_series(event, math="dau", source=source)],
            "dateRange": {"date_from": date_from},
            "interval": "day",
            "stickinessFilter": {},
        },
    }


# Helper: property filter for step_index (numeric!)
def step_index_filter(i: int) -> list:
    return [{"type": "event", "key": "step_index", "operator": "exact", "value": [i]}]


def is_expected_filter(expected: bool) -> list:
    return [{"type": "event", "key": "is_expected", "operator": "exact", "value": [expected]}]


# ---------------------------------------------------------------------------
# Dashboards
# ---------------------------------------------------------------------------


def build_onboarding() -> int:
    d = create_dashboard(
        "Onboarding Health",
        "Funnel completion, drop-off by step, duration per step. "
        "Uses onboarding_started -> onboarding_step_completed(step_index 0..7) -> onboarding_completed. "
        "8 of the specced 9 steps currently emit step_index — step 9 is a known gap (task B6).",
        tags=["onboarding"],
    )

    # 2026-08-10: audit (task B6) found 8 flowing step_index values (0..7), not 7
    # (0..6) as the original script assumed — range(8) below, and the insight is
    # renamed (old "(9 steps)" name retired via RETIRED_INSIGHTS, --retire-dead).
    step_series = [event_series("onboarding_started", name="Started")]
    for i in range(8):
        step_series.append({
            "kind": "EventsNode",
            "event": "onboarding_step_completed",
            "name": f"Step {i} completed",
            "math": "total",
            "properties": APP_HYGIENE_FILTERS + step_index_filter(i),
        })
    step_series.append(event_series("onboarding_completed", name="Completed"))
    create_insight(d, "Onboarding funnel (8 of 9 known steps — see B6)",
                   "Started -> each step_index (0..7) -> Completed. Window: 1 day. "
                   "Ordered (not strict) because step_viewed fires between step_completed emissions. "
                   "Spec describes 9 steps; only 8 step_index values have ever been observed — "
                   "task B6 tracks finding and instrumenting the missing one.",
                   funnel(step_series, date_from="-14d", window_interval=1, window_unit="day",
                          order_type="ordered"))

    create_insight(d, "Completions vs starts (daily counts, not cohort)",
                   "Two parallel DAU series. A/B is a rough ratio of daily completers to daily starters — "
                   "not a cohort conversion rate (use the funnel for that).",
                   trends(
                       [
                           event_series("onboarding_completed", math="dau", name="Completed"),
                           event_series("onboarding_started", math="dau", name="Started"),
                       ],
                       date_from="-14d", interval="day", formula="A/B"))

    create_insight(d, "Onboarding started (daily)",
                   "Unique users starting the flow.",
                   trends([event_series("onboarding_started", math="dau")],
                          date_from="-14d", interval="day"))

    create_insight(d, "Step views — distribution by step_name",
                   "Where users linger. Count of onboarding_step_viewed by step_name.",
                   trends([event_series("onboarding_step_viewed", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "step_name"},
                          display="ActionsBar"))

    create_insight(d, "Median duration per step (seconds)",
                   "Median of duration_seconds on onboarding_step_completed, bucketed by step_name.",
                   trends([event_series("onboarding_step_completed",
                                        math="median", math_property="duration_seconds")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "step_name"},
                          display="ActionsBar"))

    create_insight(d, "Started by auth provider",
                   "2026-08-10: switched from the user_logged_in proxy to the direct signal — "
                   "breakdown of signup_method_selected by `method` (apple/google/email), now that "
                   "the signup_* funnel is instrumented (2026-08-05 batch).",
                   trends([event_series("signup_method_selected", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "method"},
                          display="ActionsBar"))

    create_insight(d, "Total onboarding duration (median seconds)",
                   "Median of total_duration_seconds on onboarding_completed.",
                   trends([event_series("onboarding_completed",
                                        math="median", math_property="total_duration_seconds")],
                          date_from="-14d", interval="day"))

    # Legal Gate Funnel — added 2026-04-24 (legal_gate_bug fix, T3b)
    create_insight(d, "Legal Gate Funnel — gate-ready vs abandoned",
                   "Post-fix baseline for legal gate completion friction. "
                   "A = onboarding_legal_gate_gate_ready (user reached checkboxed consent screen). "
                   "B = onboarding_legal_gate_abandoned (left without consenting). "
                   "Formula B/A tracks users who reached the consent screen but left without consenting — "
                   "scroll-gate removed; residual abandonment reflects checkbox friction only. "
                   "Window: last 14 days.",
                   trends(
                       [
                           event_series("onboarding_legal_gate_gate_ready",
                                        math="total", name="Gate ready (A)"),
                           event_series("onboarding_legal_gate_abandoned",
                                        math="total", name="Abandoned (B)"),
                       ],
                       date_from="-14d", interval="day", formula="B/A"))

    create_insight(d, "Legal Gate — abandoned by viewport_width",
                   "Breakdown of onboarding_legal_gate_abandoned by viewport_width. "
                   "Identifies viewport widths where consent abandonment concentrates — "
                   "narrow viewports (e.g., iPhone SE 320pt) may signal residual layout friction.",
                   trends([event_series("onboarding_legal_gate_abandoned", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "viewport_width"},
                          display="ActionsBar"))

    create_insight(d, "Legal Gate — abandoned by text_scale_factor",
                   "Breakdown of onboarding_legal_gate_abandoned by text_scale_factor. "
                   "Identifies iOS Dynamic Type / Android font scale values where abandonment concentrates — "
                   "accessibility regression signal post-fix.",
                   trends([event_series("onboarding_legal_gate_abandoned", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "text_scale_factor"},
                          display="ActionsBar"))

    # New 2026-08-10: pre-onboarding signup + consent steps (2026-08-05 batch).
    create_insight(d, "Signup + consent funnel (pre-onboarding)",
                   "New pre-onboarding steps instrumented 2026-08-05: account creation and the "
                   "consent screen, both upstream of onboarding_started. "
                   "signup_started -> signup_method_selected -> consent_screen_viewed -> consent_granted. "
                   "consent_granted is DUAL-SOURCED — verified (event,$lib,count): 16 posthog-flutter "
                   "+ 18 posthog-python in the last 90d (client fires on local grant, backend confirms "
                   "server-side) — so it carries NO $lib filter here (SOURCE_ANY) to avoid dropping "
                   "either side. Re-verified 2026-08-16: 26 posthog-flutter + 32 posthog-python /90d, "
                   "still genuinely dual-sourced. Window: 1 day.",
                   funnel([
                       event_series("signup_started", name="Signup started"),
                       event_series("signup_method_selected", name="Method selected"),
                       event_series("consent_screen_viewed", name="Consent screen viewed"),
                       event_series("consent_granted", name="Consent granted (client+backend)",
                                    source=SOURCE_ANY),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "Signup failures",
                   "Daily count of signup_failed — auth/registration errors during signup.",
                   trends([event_series("signup_failed", math="total")],
                          date_from="-14d", interval="day"))

    return d


def build_activation() -> int:
    d = create_dashboard(
        "Activation & Time-to-Value",
        "How quickly new users reach first capture. "
        "Note: backend *_created events not yet emitted — *_started (frontend intent) used as proxy.",
        tags=["activation"],
    )

    create_insight(d, "Onboarding -> debrief (7d)",
                   "Funnel: completed onboarding -> started first debrief within a week.",
                   funnel([
                       event_series("onboarding_completed", name="Onboarded"),
                       event_series("debrief_started", name="Started debrief"),
                   ], date_from="-14d", window_interval=7, window_unit="day"))

    create_insight(d, "Onboarding -> prep card (7d)",
                   "Funnel: completed onboarding -> started a prep card.",
                   funnel([
                       event_series("onboarding_completed", name="Onboarded"),
                       event_series("prep_card_started", name="Started prep"),
                   ], date_from="-14d", window_interval=7, window_unit="day"))

    create_insight(d, "Onboarding -> between-session (7d)",
                   "Funnel: completed onboarding -> started a between-session note.",
                   funnel([
                       event_series("onboarding_completed", name="Onboarded"),
                       event_series("between_session_started", name="Started between-session"),
                   ], date_from="-14d", window_interval=7, window_unit="day"))

    create_insight(d, "Active users — DAU",
                   "Unique users triggering any tab navigation or capture event.",
                   trends([
                       event_series("tab_switched", math="dau", name="DAU (tab_switched)"),
                       event_series("user_logged_in", math="dau", name="DAU (logins)"),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "Lifecycle (daily)",
                   "New / Returning / Resurrecting / Dormant based on any app navigation.",
                   lifecycle("tab_switched", date_from="-14d", interval="day"))

    # New 2026-08-10: app tour (product tour after signup, 2026-08-04 batch).
    create_insight(d, "App tour funnel",
                   "New (2026-08-04): app_tour_started -> app_tour_step_viewed -> app_tour_completed, "
                   "vs. app_tour_skipped as the drop-off path. Window: 1 day.",
                   funnel([
                       event_series("app_tour_started", name="Tour started"),
                       event_series("app_tour_step_viewed", name="Step viewed"),
                       event_series("app_tour_completed", name="Tour completed"),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "App tour skip rate",
                   "app_tour_skipped vs app_tour_started (formula B/A = skip rate).",
                   trends([
                       event_series("app_tour_started", math="total", name="Started (A)"),
                       event_series("app_tour_skipped", math="total", name="Skipped (B)"),
                   ], date_from="-14d", interval="day", formula="B/A"))

    # New 2026-08-10: user_activated is backend-derived (posthog_service.py) —
    # see growth-analyst's analytics-reports/2026-08-10-activation-definition.md,
    # which explicitly recommends AGAINST a client-only activation event and
    # instead derives it backend-side from 9 qualifying artifact-creation events.
    create_insight(d, "User activated (backend-derived) — daily",
                   "DAU of the backend-derived user_activated event (at-most-once per user, fired on "
                   "the FIRST qualifying artifact write — debrief/prep/between-session/etc). "
                   "See analytics-reports/2026-08-10-activation-definition.md for the definition and "
                   "why this is computed server-side rather than as a client event.",
                   trends([event_series("user_activated", math="dau", source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day"))

    create_insight(d, "Activation — within 24h vs later",
                   "Breakdown of user_activated by is_within_24h. Growth-analyst found first-write-"
                   "within-24h correlates with 3.41x retention.",
                   trends([event_series("user_activated", math="total", source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "is_within_24h"},
                          display="ActionsPie"))

    return d


def build_engagement() -> int:
    d = create_dashboard(
        "Core Engagement",
        "Active users, stickiness, feature usage, short-window retention. "
        "Retention windows kept small (project started ingesting 2026-04-22).",
        tags=["engagement"],
    )

    create_insight(d, "DAU (any navigation)",
                   "Users firing tab_switched — any in-app action.",
                   trends([event_series("tab_switched", math="dau", name="DAU")],
                          date_from="-14d", interval="day"))

    create_insight(d, "Stickiness — tab_switched",
                   "How many days in the period each user is active.",
                   stickiness("tab_switched", date_from="-14d"))

    create_insight(d, "Daily unique users per feature",
                   "DAU per feature entry point. 2026-08-10: added workspace_opened, "
                   "quick_capture_started and prep_capture_started — these run alongside (not yet "
                   "replacing) the original prep_card_started/debrief_started/between_session_started "
                   "capture events; both sets are live simultaneously as of this rebuild, worth "
                   "watching to see which becomes canonical (see rebuild-plan report).",
                   trends([
                       event_series("debrief_started", math="dau", name="Debrief"),
                       event_series("prep_card_started", math="dau", name="Prep (legacy)"),
                       event_series("between_session_started", math="dau", name="Between-session"),
                       event_series("recording_upload_started", math="dau", name="Recording"),
                       event_series("voice_chat_started", math="dau", name="Voice chat"),
                       event_series("character_card_viewed", math="dau", name="Character"),
                       event_series("timeline_viewed", math="dau", name="Timeline"),
                       event_series("workspace_opened", math="dau", name="Workspace"),
                       event_series("quick_capture_started", math="dau", name="Quick capture"),
                       event_series("prep_capture_started", math="dau", name="Prep capture (new)"),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "Retention — post-onboarding (daily, 7 days)",
                   "How many users return on D1..D7 after onboarding_started.",
                   retention("onboarding_started", "tab_switched",
                             period="Day", total_intervals=7, date_from="-14d"))

    create_insight(d, "Retention — debrief users (daily, 7 days)",
                   "Do users who start a debrief keep coming back?",
                   retention("debrief_started", "tab_switched",
                             period="Day", total_intervals=7, date_from="-14d"))

    create_insight(d, "Tab distribution",
                   "Which tabs users open (breakdown by tab_name).",
                   trends([event_series("tab_switched", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "tab_name"},
                          display="ActionsPie"))
    return d


def build_therapy_loop() -> int:
    d = create_dashboard(
        "Therapy Loop Health",
        "Does a user close prep -> (external session) -> debrief each week? Plus Reflect chat "
        "engagement (backend session pair, corrected 2026-08-10 — see module docstring item 3).",
        tags=["therapy"],
    )

    create_insight(d, "Prep -> debrief funnel (7d window)",
                   "prep_card_started -> debrief_started within 7 days.",
                   funnel([
                       event_series("prep_card_started", name="Prep started"),
                       event_series("debrief_started", name="Debrief started"),
                   ], date_from="-14d", window_interval=7, window_unit="day"))

    create_insight(d, "Daily capture activity",
                   "Each capture type per day.",
                   trends([
                       event_series("prep_card_started", math="dau", name="Prep"),
                       event_series("debrief_started", math="dau", name="Debrief"),
                       event_series("between_session_started", math="dau", name="Between-session"),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "Debrief input modality",
                   "Voice vs text on debrief_started.",
                   trends([event_series("debrief_started", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "input_type"},
                          display="ActionsBar"))

    create_insight(d, "Prep card input modality",
                   "Voice vs text on prep_card_started.",
                   trends([event_series("prep_card_started", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "input_type"},
                          display="ActionsBar"))

    create_insight(d, "Recording uploads by duration bucket",
                   "Short vs medium vs long session recordings.",
                   trends([event_series("recording_upload_started", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "duration_bucket"},
                          display="ActionsBar"))

    # --- New 2026-08-10: Reflect chat engagement, corrected semantics ---------
    # reflect_session_started is backend-emitted (reflect.py POST /start); pair it
    # with the CLIENT reflect_ui_session_ended (real on-screen engagement), never
    # with backend reflect_session_ended (rare, explicit thread finalization only —
    # see module docstring item 3 / analytics_events.dart's reflectUiSessionEnded doc).
    create_insight(d, "Reflect engagement funnel (session started -> ui session ended)" + AWAITING_DEPLOY_NOTE,
                   "reflect_session_started (backend, thread opened, verified LIVE — 158 events/90d, "
                   "100% posthog-python) -> reflect_ui_session_ended (client, actual on-screen "
                   "engagement close, verified 0 events/90d as of this rebuild — code exists but is "
                   "not yet live in prod). Do NOT substitute backend reflect_session_ended here — "
                   "that only fires on explicit thread finalization and undercounts real usage ~12x "
                   "(11 events/90d vs 158 reflect_session_started). This funnel will show 0% "
                   "conversion until reflect_ui_session_ended deploys. Window: 1 day.",
                   funnel([
                       event_series("reflect_session_started", name="Session started",
                                    source=SOURCE_BACKEND),
                       event_series("reflect_ui_session_ended", name="UI session ended",
                                    source=SOURCE_APP),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "Reflect UI session duration (median seconds)" + AWAITING_DEPLOY_NOTE,
                   "Median duration_seconds on reflect_ui_session_ended — how long a Reflect "
                   "engagement actually lasts on screen.",
                   trends([event_series("reflect_ui_session_ended",
                                        math="median", math_property="duration_seconds")],
                          date_from="-14d", interval="day"))

    create_insight(d, "Reflect UI session end reason" + AWAITING_DEPLOY_NOTE,
                   "Breakdown of reflect_ui_session_ended by end_reason (navigated_away / "
                   "backgrounded / thread_switched / user_ended / limit_reached).",
                   trends([event_series("reflect_ui_session_ended", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "end_reason"},
                          display="ActionsBar"))

    create_insight(d, "Reflect messages per session (median)" + AWAITING_DEPLOY_NOTE,
                   "Median messages_sent on reflect_ui_session_ended — depth of a Reflect "
                   "engagement, not just its duration.",
                   trends([event_series("reflect_ui_session_ended",
                                        math="median", math_property="messages_sent")],
                          date_from="-14d", interval="day"))

    # --- New 2026-08-10: summary/audit generated-vs-viewed (task B3) ------------
    # weekly_summary_generated / monthly_audit_generated: backend-only
    # (app/services/posthog_service.py), verified 0 posthog-flutter presence in
    # code. summary_viewed: client-only (therapy_tab_cubit.dart trackSummaryViewed).
    # Both sides verified 0 live events in the last 90d as of this rebuild (code
    # committed, not yet deployed) — AWAITING_DEPLOY_NOTE on all three insights.
    create_insight(d, "Summary/audit generated (backend, weekly vs monthly)" + AWAITING_DEPLOY_NOTE,
                   "weekly_summary_generated / monthly_audit_generated — backend-emitted "
                   "(posthog_service.py), fired once per successful creation on both the hourly-cron "
                   "auto path and the manual Generate Now/Retry path (is_regeneration property "
                   "distinguishes them). No $lib filter — backend event, never carries "
                   "$lib=posthog-flutter.",
                   trends([
                       event_series("weekly_summary_generated", math="total", name="Weekly",
                                    source=SOURCE_BACKEND),
                       event_series("monthly_audit_generated", math="total", name="Monthly",
                                    source=SOURCE_BACKEND),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "Summary viewed (client, by period_type)" + AWAITING_DEPLOY_NOTE,
                   "summary_viewed — client-emitted, fired at most once per (period_type, "
                   "period_start) per visit to the Therapy tab. Breakdown by period_type "
                   "(weekly/monthly) is the read half of the generated-vs-read pair task B3 asked for.",
                   trends([event_series("summary_viewed", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "period_type"},
                          display="ActionsBar"))

    create_insight(d, "Summary generated-vs-viewed ratio — weekly" + AWAITING_DEPLOY_NOTE,
                   "Formula B/A = weekly summaries actually opened per weekly summary generated. "
                   "A = weekly_summary_generated (backend, SOURCE_BACKEND). B = summary_viewed filtered "
                   "to period_type=weekly (app, SOURCE_APP). This is the core B3 metric — "
                   "'is anyone reading the summaries we generate.' The two sides are deliberately "
                   "pinned to different $lib sources: A is job output, B is human reading.",
                   trends([
                       event_series("weekly_summary_generated", math="total", name="Generated (A)",
                                    source=SOURCE_BACKEND),
                       event_series("summary_viewed", math="total", name="Viewed weekly (B)",
                                    properties=[{"type": "event", "key": "period_type",
                                                 "operator": "exact", "value": ["weekly"]}]),
                   ], date_from="-14d", interval="day", formula="B/A"))

    # --- New 2026-08-10: realization detection (task B5, backend, 1 event ever) --
    create_insight(d, "Realization detected (daily count)" + " [B5: fired once in project history — "
                   "backend investigating whether the detector is not running, threshold is too high, "
                   "or the emission point is unreachable; see task B5]",
                   "realization_detected (backend, app/api/v1/endpoints/realizations.py). Fired exactly "
                   "once since project start as of this rebuild — kept on the dashboard (not retired) "
                   "because there is an active investigation (task B5), not a dead/abandoned feature.",
                   trends([event_series("realization_detected", math="total", source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day"))

    return d


def build_monetization() -> int:
    d = create_dashboard(
        "Monetization",
        "Subscription intent funnel, now including the paywall entry point and restore flow "
        "(2026-08-10 monetization funnel fix batch).",
        tags=["monetization"],
    )

    create_insight(d, "Subscription screen -> product selected",
                   "Funnel within 1 day. subscription_purchase_completed is backend-verified "
                   "(receipt verification), not yet added here as a funnel step — see "
                   "'Purchases completed' below for its own trend.",
                   funnel([
                       event_series("subscription_screen_opened", name="Screen opened"),
                       event_series("subscription_product_selected", name="Product selected"),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "Paywall -> screen -> product selected" + AWAITING_DEPLOY_NOTE,
                   "Full funnel including the paywall entry point: paywall_shown -> "
                   "subscription_screen_opened -> subscription_product_selected. paywall_shown "
                   "(guarded, once-per-screen-instance emission, 2026-08-10 batch) is not yet live in "
                   "prod. NOTE: paywall_dismissed (same batch) already shows a handful of events with "
                   "zero matching paywall_shown — flag to data-analytics as a possible guard/emission "
                   "bug once paywall_shown deploys and the asymmetry persists. Window: 1 day.",
                   funnel([
                       event_series("paywall_shown", name="Paywall shown"),
                       event_series("subscription_screen_opened", name="Screen opened"),
                       event_series("subscription_product_selected", name="Product selected"),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "Paywall shown by trigger_feature" + AWAITING_DEPLOY_NOTE,
                   "Breakdown of paywall_shown by trigger_feature — which gated feature actually "
                   "drives paywall views, once live.",
                   trends([event_series("paywall_shown", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "trigger_feature"},
                          display="ActionsBar"))

    create_insight(d, "Subscription screen opens by source",
                   "Where does the user enter the subscription flow (settings/onboarding/paywall).",
                   trends([event_series("subscription_screen_opened", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "source"},
                          display="ActionsBar"))

    create_insight(d, "Products selected",
                   "Breakdown by product_id.",
                   trends([event_series("subscription_product_selected", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "product_id"},
                          display="ActionsBar"))

    create_insight(d, "Monthly vs yearly selection",
                   "Breakdown of subscription_product_selected by subscription_type.",
                   trends([event_series("subscription_product_selected", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "subscription_type"},
                          display="ActionsPie"))

    create_insight(d, "App store deep-link clicks",
                   "app_store_click events — intent to install/purchase via the external store. "
                   "BUG FIXED 2026-08-16: this is a WEB event from the Webflow marketing site, NOT "
                   "an in-app event – verified 85 events / 180d, 100% $lib='web', zero "
                   "posthog-flutter, last seen 2026-08-10. It was previously pinned to "
                   "$lib='posthog-flutter' and therefore rendered a permanent hard zero. Now "
                   "SOURCE_WEB. Read it as marketing-site conversion intent, not app engagement, "
                   "and do not merge it into app funnels.",
                   trends([event_series("app_store_click", math="total", source=SOURCE_WEB)],
                          date_from="-14d", interval="day"))

    create_insight(d, "Purchase attempts (started / completed / failed)",
                   "subscription_purchase_started/failed are client-only (verified 100% "
                   "posthog-flutter). subscription_purchase_completed is DUAL-SOURCED — verified "
                   "(event,$lib,count): 5 posthog-flutter (optimistic client-side fire) + 3 "
                   "posthog-python (receipt-verification confirmation) in the last 90d — so its "
                   "series intentionally carries NO $lib filter (SOURCE_ANY) to avoid undercounting "
                   "by dropping either side; the other two series keep the default app hygiene "
                   "filter since they are single-sourced. Re-verified 2026-08-16: 6 posthog-flutter "
                   "+ 7 posthog-python /90d, still dual-sourced.",
                   trends([
                       event_series("subscription_purchase_started", math="total", name="Started"),
                       event_series("subscription_purchase_completed", math="total",
                                    name="Completed (client+backend, unfiltered by $lib)",
                                    source=SOURCE_ANY),
                       event_series("subscription_purchase_failed", math="total", name="Failed"),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "Restore attempts (started / completed / failed)" + AWAITING_DEPLOY_NOTE,
                   "subscription_restore_started/completed/failed — restore-purchase flow, new in "
                   "the 2026-08-10 batch (58d097b). Restores that silently fail are a common source "
                   "of one-star reviews; watch the failed/started ratio once this is live.",
                   trends([
                       event_series("subscription_restore_started", math="total", name="Started"),
                       event_series("subscription_restore_completed", math="total", name="Completed"),
                       event_series("subscription_restore_failed", math="total", name="Failed"),
                   ], date_from="-14d", interval="day"))

    return d


def build_feature_adoption() -> int:
    d = create_dashboard(
        "Feature Adoption Matrix",
        "Daily unique users per feature and interaction depth.",
        tags=["features"],
    )

    create_insight(d, "Feature reach — DAU",
                   "Daily unique users per feature entry point. 2026-08-10: added workspace_opened, "
                   "quick_capture_started, prep_capture_started, voice_transcription_started.",
                   trends([
                       event_series("debrief_started", math="dau", name="Debrief"),
                       event_series("prep_card_started", math="dau", name="Prep"),
                       event_series("between_session_started", math="dau", name="Between"),
                       event_series("voice_chat_started", math="dau", name="Voice chat"),
                       event_series("recording_upload_started", math="dau", name="Recording"),
                       event_series("timeline_viewed", math="dau", name="Timeline"),
                       event_series("character_card_viewed", math="dau", name="Character"),
                       event_series("bio_refreshed", math="dau", name="Bio refresh"),
                       event_series("workspace_opened", math="dau", name="Workspace"),
                       event_series("quick_capture_started", math="dau", name="Quick capture"),
                       event_series("prep_capture_started", math="dau", name="Prep capture (new)"),
                       event_series("voice_transcription_started", math="dau", name="Voice transcription"),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "Feature depth — total events",
                   "Total events per feature (not unique users) — higher = deeper use per user.",
                   trends([
                       event_series("debrief_started", math="total", name="Debrief"),
                       event_series("prep_card_started", math="total", name="Prep"),
                       event_series("between_session_started", math="total", name="Between"),
                       event_series("voice_chat_started", math="total", name="Voice"),
                       event_series("recording_upload_started", math="total", name="Recording"),
                       event_series("timeline_viewed", math="total", name="Timeline"),
                       event_series("character_card_viewed", math="total", name="Character"),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "Timeline filter usage",
                   "How users slice the therapy timeline.",
                   trends([event_series("timeline_filter_changed", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "filter_type"},
                          display="ActionsBar"))

    create_insight(d, "Input modality across captures",
                   "Voice vs text share per capture event.",
                   trends([
                       event_series("debrief_started", math="total", name="Debrief"),
                       event_series("prep_card_started", math="total", name="Prep"),
                       event_series("between_session_started", math="total", name="Between"),
                   ], date_from="-14d", interval="day",
                       breakdown={"breakdown_type": "event", "breakdown": "input_type"}))

    create_insight(d, "Quick capture funnel",
                   "New (2026-08-05): quick_capture_started -> quick_capture_submitted, vs "
                   "quick_capture_abandoned as the drop-off path. Window: 1 day.",
                   funnel([
                       event_series("quick_capture_started", name="Started"),
                       event_series("quick_capture_submitted", name="Submitted"),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "Prep capture funnel (new)",
                   "New (2026-08-05): prep_capture_started -> prep_capture_submitted, vs "
                   "prep_capture_abandoned. See 'Daily unique users per feature' (Core Engagement) "
                   "for the open question of how this relates to the legacy prep_card_started path. "
                   "Window: 1 day.",
                   funnel([
                       event_series("prep_capture_started", name="Started"),
                       event_series("prep_capture_submitted", name="Submitted"),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "Voice transcription — started vs completed vs failed",
                   "New (2026-08-05, part of the AssemblyAI STT batch): voice_transcription_started/"
                   "completed/failed for quick/prep capture voice input.",
                   trends([
                       event_series("voice_transcription_started", math="total", name="Started"),
                       event_series("voice_transcription_completed", math="total", name="Completed"),
                       event_series("voice_transcription_failed", math="total", name="Failed"),
                   ], date_from="-14d", interval="day"))

    return d


def build_health_quality() -> int:
    d = create_dashboard(
        "Health & Quality",
        "Marketing site ($web_vitals from www.mindsync.app) + mobile capture reliability + "
        "backend error quality (api_error, corrected 2026-08-10 — see module docstring item 4).",
        tags=["quality"],
    )

    # $pageview / $web_vitals are only ever emitted by the web SDK ($lib='web').
    # 2026-08-16: upgraded from "no filter" to a positive SOURCE_WEB pin. These are
    # DAU-shaped numbers on a shared events table, so leaving them unpinned meant
    # any future same-named server or app event would silently inflate them.
    create_insight(d, "[Marketing site] Pageviews (daily)",
                   "$pageview from www.mindsync.app web SDK. Pinned $lib='web'. These are site "
                   "visitors, NOT app users – never add this series to an app DAU chart.",
                   trends([event_series("$pageview", math="dau", source=SOURCE_WEB)],
                          date_from="-14d", interval="day"))

    create_insight(d, "[Marketing site] LCP p75",
                   "Largest Contentful Paint, 75th percentile.",
                   trends([event_series("$web_vitals", math="p75",
                                        math_property="$web_vitals_LCP_value", source=SOURCE_WEB)],
                          date_from="-14d", interval="day"))

    create_insight(d, "[Marketing site] INP p75",
                   "Interaction to Next Paint, 75th percentile.",
                   trends([event_series("$web_vitals", math="p75",
                                        math_property="$web_vitals_INP_value", source=SOURCE_WEB)],
                          date_from="-14d", interval="day"))

    create_insight(d, "[Marketing site] CLS p75",
                   "Cumulative Layout Shift, 75th percentile.",
                   trends([event_series("$web_vitals", math="p75",
                                        math_property="$web_vitals_CLS_value", source=SOURCE_WEB)],
                          date_from="-14d", interval="day"))

    create_insight(d, "[Mobile] Recording upload volume",
                   "Daily recording_upload_started by duration_bucket. "
                   "Compare to recording_upload_completed once that event flows.",
                   trends([event_series("recording_upload_started", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "duration_bucket"},
                          display="ActionsBar"))

    create_insight(d, "[Mobile] Voice chat starts",
                   "Daily count of voice_chat_started — proxy for voice feature health. n is very "
                   "low (1 event / 1 user in the last 14d as of this rebuild) — see task B7 "
                   "(is voice chat worth further investment).",
                   trends([event_series("voice_chat_started", math="total")],
                          date_from="-14d", interval="day"))

    create_insight(d, "[Mobile] Recording abandoned by reason",
                   "New (2026-08-10): recording_abandoned closes the gap where several exit paths "
                   "after recording_started fired zero analytics. Breakdown by `reason` "
                   "(permission_denied / user_discarded / etc).",
                   trends([event_series("recording_abandoned", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "reason"},
                          display="ActionsBar"))

    # --- New 2026-08-10: api_error quality split (task S1, backend commit 7696f40) ---
    create_insight(d, "[Backend] API errors — total volume by endpoint",
                   "All api_error events (4xx+5xx), including designed empty-state / limit-gate "
                   "responses — this is the RAW volume, not the quality signal. See 'API errors — "
                   "real failures only' below for the filtered view. Backend-emitted, no $lib filter.",
                   trends([event_series("api_error", math="total", source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "endpoint"},
                          display="ActionsBar"))

    create_insight(d, "[Backend] API errors — expected vs real (is_expected split)"
                   + AWAITING_DEPLOY_NOTE,
                   "Trend split by the `is_expected` property added in the S1 fix (backend commit "
                   "7696f40, app/main.py) — distinguishes designed 4xx behavior from genuine "
                   "failures. NOT YET DEPLOYED to Heroku as of this rebuild: is_expected is NULL on "
                   "100% of api_error events in the live 14d window (verified 2026-08-10). Deploy the "
                   "commit to populate this split.",
                   trends([event_series("api_error", math="total", source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "is_expected"},
                          display="ActionsBar"))

    create_insight(d, "[Backend] API errors — real failures only (is_expected=false) by endpoint"
                   + AWAITING_DEPLOY_NOTE,
                   "THE quality signal — pre-S1 this dashboard drowned ~20 real failures per 14 days "
                   "under ~4500 expected-empty-state/limit-gate events. Reads empty until the S1 "
                   "commit (7696f40) is deployed to Heroku.",
                   trends([event_series("api_error", math="total", source=SOURCE_BACKEND,
                                        properties=is_expected_filter(False))],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "endpoint"},
                          display="ActionsBar"))

    return d


def build_gamification() -> int:
    d = create_dashboard(
        "Gamification Impact",
        "Character tab engagement, orca naming/color, user/orca level distribution. "
        "NOTE (task B4, SPRAWDŹ/still open): goals and symptoms are practically unused — 4 events / "
        "2 users (goals) and 47 events / 7 users (symptoms) in 14d, vs 46 users on timeline — and "
        "neither screen appears in the top-20 $screen_name ranking. No product decision has been made "
        "yet (promote vs sunset), so no insights for those areas are added here until B4 resolves.",
        tags=["gamification"],
    )

    create_insight(d, "Character card views (daily)",
                   "DAU on character_card_viewed.",
                   trends([event_series("character_card_viewed", math="dau")],
                          date_from="-14d", interval="day"))

    create_insight(d, "Orca color changes",
                   "Breakdown by chosen color.",
                   trends([event_series("orca_color_changed", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "color"},
                          display="ActionsPie"))

    create_insight(d, "Bio refresh frequency",
                   "How often users regenerate the personal bio.",
                   trends([event_series("bio_refreshed", math="total")],
                          date_from="-14d", interval="day"))

    create_insight(d, "User level distribution",
                   "Character card views broken down by user_level.",
                   trends([event_series("character_card_viewed", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "user_level"},
                          display="ActionsBar"))

    create_insight(d, "Orca level distribution",
                   "Character card views broken down by orca_level.",
                   trends([event_series("character_card_viewed", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "orca_level"},
                          display="ActionsBar"))

    create_insight(d, "Retention — character tab engagers (daily, 7 days)",
                   "Return rate of users who view the character card.",
                   retention("character_card_viewed", "tab_switched",
                             period="Day", total_intervals=7, date_from="-14d"))
    return d


def build_account_health() -> int:
    d = create_dashboard(
        "Account Health",
        "Login patterns, settings engagement, account lifecycle (signup through deletion), "
        "consent grants/revocations.",
        tags=["account"],
    )

    create_insight(d, "Daily logins",
                   "DAU of user_logged_in.",
                   trends([event_series("user_logged_in", math="dau")],
                          date_from="-14d", interval="day"))

    create_insight(d, "Logins by auth provider",
                   "google vs apple vs email split.",
                   trends([event_series("user_logged_in", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "auth_provider"},
                          display="ActionsPie"))

    create_insight(d, "Logout volume",
                   "Daily user_logged_out count. High logout without re-login = churn signal.",
                   trends([event_series("user_logged_out", math="total")],
                          date_from="-14d", interval="day"))

    # 2026-08-10: replaces the retired "Notification preference changes" insight,
    # which referenced notification_preference_changed — dead since 2026-05-21,
    # renamed twice since (-> notification_interest_toggled -> notification_row_toggled,
    # FE commit 4a20b19). Schema also changed: category/selected -> key/value.
    create_insight(d, "Notification row toggles (key/value)",
                   "Users toggling individual notification rows in Settings. Breakdown by `key` "
                   "(the notification type, e.g. daily_check_in) — replaces the old preference_type "
                   "breakdown, which used a schema (category/selected) that no longer exists. See "
                   "'Notification preference changes' (retired via --retire-dead) for the superseded "
                   "insight this replaces.",
                   trends([event_series("notification_row_toggled", math="total")],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "key"},
                          display="ActionsBar"))

    create_insight(d, "Login lifecycle",
                   "Lifecycle of user_logged_in: new / returning / resurrecting / dormant.",
                   lifecycle("user_logged_in", date_from="-14d", interval="day"))

    create_insight(d, "Notifications received (daily)",
                   "FCM delivery volume. CORRECTED 2026-08-10: this is CLIENT-emitted "
                   "(FirebaseMessaging.onMessage / onBackgroundMessage in main.dart), not backend — "
                   "verified via a fresh (event,$lib,count) query, 100% posthog-flutter. An earlier "
                   "draft of this rebuild misclassified it as backend from a doc-comment reference in "
                   "notification_orchestrator_job.py that only *names* this client event, and would "
                   "have silently zeroed this insight by pairing the wrong client flag with the "
                   "$lib=posthog-flutter filter. Pair with notification_opened to measure open rate.",
                   trends([event_series("notification_received", math="total")],
                          date_from="-14d", interval="day"))

    create_insight(d, "Notification permission funnel",
                   "New (2026-08-04): notification_permission_prompted -> "
                   "notification_permission_granted, vs notification_permission_denied as the "
                   "drop-off path. Window: 1 day.",
                   funnel([
                       event_series("notification_permission_prompted", name="Prompted"),
                       event_series("notification_permission_granted", name="Granted"),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "Account screen opens (daily)",
                   "New (2026-08-06): DAU on account_screen_opened.",
                   trends([event_series("account_screen_opened", math="dau")],
                          date_from="-14d", interval="day"))

    create_insight(d, "Account deletion funnel",
                   "New (2026-08-09): account_deletion_started -> account_deletion_confirmed, vs "
                   "account_deletion_cancelled as the drop-off/retention-save path. Window: 1 day.",
                   funnel([
                       event_series("account_deletion_started", name="Started"),
                       event_series("account_deletion_confirmed", name="Confirmed"),
                   ], date_from="-14d", window_interval=1, window_unit="day"))

    create_insight(d, "Consent grants vs revokes",
                   "New (2026-08-04): consent_granted vs consent_revoked daily counts. A rising "
                   "revoke line without a matching grant spike is a churn/trust signal. "
                   "consent_granted is DUAL-SOURCED (client+backend, see the Onboarding dashboard's "
                   "Signup + consent funnel for the verified split) so it carries no $lib filter here "
                   "either (SOURCE_ANY; re-verified 2026-08-16: 26 flutter + 32 python /90d). "
                   "consent_revoked is BACKEND-ONLY — verified 100% posthog-python, 0 posthog-flutter "
                   "in the last 90d (revocation only happens through a server-confirmed settings "
                   "action) – so it is pinned SOURCE_BACKEND, the opposite reason: a "
                   "$lib=posthog-flutter filter would have zeroed it completely.",
                   trends([
                       event_series("consent_granted", math="total", name="Granted (client+backend)",
                                    source=SOURCE_ANY),
                       event_series("consent_revoked", math="total", name="Revoked (backend-only)",
                                    source=SOURCE_BACKEND),
                   ], date_from="-14d", interval="day"))

    return d


def build_backend_jobs() -> int:
    """Server-side activity: the notification/moment pipeline, job output, backend failures.

    Added 2026-08-16 alongside the $lib fix. The point is NOT to hide the backend
    events that broke the DAU numbers – it is to give them a home where they are
    labelled honestly. On this dashboard a person count means "users the server
    acted on", which is a legitimate and important number (it is how the
    ADD_THERAPY_DATE blast was found); it just is not, and must never be read as,
    an active-user count.

    Every series here is source=SOURCE_BACKEND ($lib='posthog-python').
    """
    d = create_dashboard(
        "Backend & Jobs (server-side)",
        "SERVER-SIDE ONLY ($lib='posthog-python'): RQ worker, cron jobs and API handlers. "
        "Person counts on this dashboard mean 'users the backend did something ABOUT', "
        "NOT active users – a job that touches the whole base scores ~1800 people while real "
        "app usage is a dozen a day. For human activity use Core Engagement / Activation, "
        "which are pinned to $lib='posthog-flutter'. Context: background jobs only started "
        "reporting to PostHog on 2026-08-11 (backend 177c026 fixed a missing worker init), "
        "so there is NO history before that date – a flat line to the left is missing "
        "instrumentation, not silence.",
        tags=["backend", "jobs", "server-side"],
    )

    create_insight(d, "[Jobs] Moment pipeline – scheduled / sent / opened / acted",
                   "The notification funnel as event volume. scheduled = orchestrator wrote a "
                   "moment to the DB; sent = push fired; opened/acted = the human reacted. The gap "
                   "between sent and opened is the health of the whole notification product "
                   "(2026-08 baseline: ~0.2% open rate).",
                   trends([
                       event_series("moment.scheduled", math="total", name="Scheduled",
                                    source=SOURCE_BACKEND),
                       event_series("moment.sent", math="total", name="Sent",
                                    source=SOURCE_BACKEND),
                       event_series("moment.opened", math="total", name="Opened",
                                    source=SOURCE_BACKEND),
                       event_series("moment.acted", math="total", name="Acted",
                                    source=SOURCE_BACKEND),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "[Jobs] Moments scheduled by moment_type",
                   "Which notification type the orchestrator actually picks. This is the insight "
                   "that exposes cadence degeneration: the MSV3.2.2 spec called for two varied "
                   "slots a day, and in the 2026-08 window ADD_THERAPY_DATE alone was 99% of all "
                   "moments. A single dominant bar here means the scoring is collapsing onto one "
                   "generator.",
                   trends([event_series("moment.scheduled", math="total", source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "moment_type"},
                          display="ActionsBar"))

    create_insight(d, "[Jobs] Pushes sent – real delivery vs into the void (has_token)",
                   "Breakdown of moment.sent by has_token. has_token=false means the user has no "
                   "FCM token, so the push had nowhere to go and the worker did the work for "
                   "nothing – 9705 of 10522 moments in the 10–16.08 window. Watch this ratio: it "
                   "is both a wasted-compute measure and a reality check on how many people the "
                   "notification system can actually reach (139 users, not 1786).",
                   trends([event_series("moment.sent", math="total", source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "has_token"},
                          display="ActionsBar"))

    create_insight(d, "[Jobs] Moment open rate (opened / sent)",
                   "Formula B/A. The single number that says whether notifications are worth "
                   "sending at all. 2026-08 baseline: ~0.002 (0.2%).",
                   trends([
                       event_series("moment.sent", math="total", name="Sent (A)",
                                    source=SOURCE_BACKEND),
                       event_series("moment.opened", math="total", name="Opened (B)",
                                    source=SOURCE_BACKEND),
                   ], date_from="-14d", interval="day", formula="B/A"))

    create_insight(d, "[Jobs] Users the notification job touched (NOT active users)",
                   "Distinct person_id on moment.scheduled – i.e. how much of the user base the "
                   "orchestrator wrote a moment for on a given day (~1750 of ~1813). THIS IS THE "
                   "NUMBER THAT BROKE THE DASHBOARDS: before 2026-08-16 it leaked into unfiltered "
                   "'daily active users' tiles and made ~13 real humans look like ~1750. It is kept "
                   "here, deliberately and under an unambiguous name, because reach-of-job is a "
                   "real operational metric – just not an engagement one.",
                   trends([event_series("moment.scheduled", math="dau", name="Users touched by job",
                                        source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day"))

    create_insight(d, "[Jobs] Moments expired (batch purge volume)",
                   "Sum of expired_count on moment.expired – moments that timed out unread, "
                   "aggregated per batch run. NOTE: this event is emitted by the purge job WITHOUT "
                   "a per-user distinct_id, so all of it lands on one anonymous person profile "
                   "(1 person / 109 events). Read the VOLUME, never the user count. Fixing the "
                   "distinct_id is an open backend item (post-release review §7/§8).",
                   trends([event_series("moment.expired", math="sum", math_property="expired_count",
                                        source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day"))

    create_insight(d, "[Jobs] Content generation output (summaries / audits / insights)",
                   "What the scheduled jobs actually produced. Pair with 'Summary viewed' on "
                   "Therapy Loop Health to see whether generated content is ever read.",
                   trends([
                       event_series("weekly_summary_generated", math="total", name="Weekly summaries",
                                    source=SOURCE_BACKEND),
                       event_series("monthly_audit_generated", math="total", name="Monthly audits",
                                    source=SOURCE_BACKEND),
                       event_series("inapp_insight.generated", math="total", name="In-app insights",
                                    source=SOURCE_BACKEND),
                       event_series("prep_card_auto_generated", math="total", name="Auto prep cards",
                                    source=SOURCE_BACKEND),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "[Backend] Server-side artifact writes (DB-confirmed)",
                   "Backend-confirmed creations – the server's own record of what got persisted, as "
                   "opposed to the client's *_started intent events. A divergence between an app "
                   "'*_started' line and its backend '*_created' line is a save-path bug.",
                   trends([
                       event_series("debrief_created", math="total", name="Debriefs",
                                    source=SOURCE_BACKEND),
                       event_series("prep_card_created", math="total", name="Prep cards",
                                    source=SOURCE_BACKEND),
                       event_series("between_session_created", math="total", name="Between-session",
                                    source=SOURCE_BACKEND),
                       event_series("goal_created", math="total", name="Goals",
                                    source=SOURCE_BACKEND),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "[Backend] Recording pipeline – processing started / completed / failed",
                   "Server-side transcription/processing outcomes. A failed line that tracks the "
                   "started line means the pipeline, not the phone, is the problem. Beware "
                   "single-user skew: on 2026-08-14 one user produced 105 upload-completed events.",
                   trends([
                       event_series("recording_processing_started", math="total", name="Started",
                                    source=SOURCE_BACKEND),
                       event_series("recording_processing_completed", math="total", name="Completed",
                                    source=SOURCE_BACKEND),
                       event_series("recording_processing_failed", math="total", name="Failed",
                                    source=SOURCE_BACKEND),
                   ], date_from="-14d", interval="day"))

    create_insight(d, "[Backend] Real failures by endpoint (is_expected=false)",
                   "api_error with is_expected=false – genuine failures only, excluding the designed "
                   "404/empty-state and premium-gate responses that make up the bulk of raw volume "
                   "(949 of 1045 in the 12–16.08 window were expected). The is_expected tag is LIVE "
                   "as of 2026-08-16 (1294 tagged events), so unlike the twin insight on Health & "
                   "Quality this one is populated. Duplicated here on purpose: this dashboard is "
                   "where someone looks when the question is 'is the server broken'.",
                   trends([event_series("api_error", math="total", source=SOURCE_BACKEND,
                                        properties=is_expected_filter(False))],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "endpoint"},
                          display="ActionsBar"))

    create_insight(d, "[Backend] Failures by status_code",
                   "api_error broken down by status_code – separates 4xx client-contract problems "
                   "from 5xx server faults. 5xx is the page-me line (2026-08 baseline: one genuine "
                   "5xx in four days).",
                   trends([event_series("api_error", math="total", source=SOURCE_BACKEND)],
                          date_from="-14d", interval="day",
                          breakdown={"breakdown_type": "event", "breakdown": "status_code"},
                          display="ActionsBar"))

    create_insight(d, "[Backend] Account lifecycle (registered / activated / deleted)",
                   "Server-side truth for account lifecycle. user_registered and account_deleted are "
                   "backend-only; user_activated is the backend-derived first-qualifying-write signal "
                   "(see analytics-reports/2026-08-10-activation-definition.md). These ARE real "
                   "per-user actions – they just happen to be recorded server-side, which is why "
                   "they sit here rather than on an app-usage dashboard.",
                   trends([
                       event_series("user_registered", math="total", name="Registered",
                                    source=SOURCE_BACKEND),
                       event_series("user_activated", math="total", name="Activated",
                                    source=SOURCE_BACKEND),
                       event_series("account_deleted", math="total", name="Deleted",
                                    source=SOURCE_BACKEND),
                   ], date_from="-14d", interval="day"))

    return d


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    global DRY_RUN, FORCE, UPDATE, RETIRE_DEAD
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print actions without posting")
    parser.add_argument("--force", action="store_true", help="Create dashboards/insights even if one with the same name exists (duplicates)")
    parser.add_argument("--update", action="store_true", help="PATCH existing insights (by name) with the new query/description instead of skipping them")
    parser.add_argument("--retire-dead", action="store_true", help="Soft-delete insights superseded by a rename (see RETIRED_INSIGHTS)")
    args = parser.parse_args()
    DRY_RUN = args.dry_run
    FORCE = args.force
    UPDATE = args.update
    RETIRE_DEAD = args.retire_dead

    builders = [
        build_onboarding,
        build_activation,
        build_engagement,
        build_therapy_loop,
        build_monetization,
        build_feature_adoption,
        build_health_quality,
        build_gamification,
        build_account_health,
        build_backend_jobs,
    ]
    created = []
    for b in builders:
        try:
            dash_id = b()
            created.append((b.__name__, dash_id))
            time.sleep(0.5)
        except Exception as e:
            print(f"[!] {b.__name__} failed: {e}", file=sys.stderr)

    if RETIRE_DEAD:
        print("\n=== RETIRING SUPERSEDED INSIGHTS ===")
        retire_dead_insights()

    print("\n=== DONE ===")
    for name, did in created:
        if did == -1:
            print(f"  {name}: (dry-run)")
        else:
            print(f"  {name}: {UI_HOST}/project/{PROJECT_ID}/dashboard/{did}")


if __name__ == "__main__":
    main()
