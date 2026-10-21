---
name: project_post_update_analysis_2026_06_29
description: PostHog post-update read 2026-06-29 — update 2.0.60 unmeasurable after 2d; recording v2 funnel gap; re-run ~07-07
metadata: 
  node_type: memory
  type: project
  originSessionId: 265b85f9-0735-4283-8ab9-5c8b981d47b2
---

growth-analyst report 2026-06-29: `analytics-reports/posthog_post_update_2026_06_29.md`. Question: effect of the 2026-06-27 app update (build **2.0.60+133**).

**Headline:** update is effectively **unmeasurable after 2 days** — public is still on **2.0.44** (App Store, 257 users/30d); new build is ~8–9 DAU, mostly the same testers; new build first appeared in telemetry **06-23/24 (TestFlight), before 06-27**, so there is NO clean before/after calendar boundary. The 06-21…25 "DAU 40–54" spike was **internal QA**, not market. **Nothing on fire, no rollback warranted, but also no proof of improvement.**

**Positives (directional):** `503 .../chunk` "store chunk" 12→0 (the chunks→Postgres migration error) and voice `500`s gone — partly confounded by lower usage post-QA.

**Red flags (none from the update):** `/users/notification-preferences` **500** is PRE-EXISTING (→ backend-api fix); `api_error` is ~80% benign expected-404s on `/latest` (Health dashboard is noisy → don't log expected 404 as error).

**🔴 Critical gap:** session-recording **v2 funnel cannot be built from PostHog** — only `recording_chunked_upload_completed` flows; no start/stop/upload/processing/saved/failed. So "is recording more stable now" is NON-OBSERVABLE. Missing business events too: `paywall_shown`, `conversation_*`, `level_up`, `account_deleted`.

**Next:** re-run ~**2026-07-07** with split by `app_version` (2.0.44 vs 2.0.60) once new-build adoption ≥25/segment. Access via [[reference_posthog_access_method]]. All numbers small-n (~3–13 public DAU), directional only.
