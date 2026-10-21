# CS-06 — Deep-Link Every Notification to Its Card

Status: **ANALYSIS / CONTRACT — not implemented.** No app code was changed to produce this document. This is the contract `backend-api`, `data-analytics`, and `flutter-mobile` implement in the next wave, verified by `integration-devops` (this agent) before ship.

Author: integration-devops · Date: 2026-07-06 · Spec ref: MSV3.2 CS-06 (p.5), CS-11 (p.7-8), CS-12 (p.8), CS-07/Workspace feature brief.

All findings below were verified by reading the current code on 2026-07-06 (not from memory/prior-session notes, which were used only as a starting hypothesis and cross-checked). File:line references are exact as of that read.

---

## 1. Executive summary

**Root cause of "notifications open the app generically":** the backend's Notification Moments framework (9 live push generators covering 9 of MindSync's ~11 notification types) already computes a correct, type-specific deep-link path per notification (`deep_link_route` column on `notification_moments`) — but the FCM delivery job puts that value under the JSON key `"deep_link_route"`, while the Flutter client's single route-resolution function, `_resolveNotificationRoute()` in `lib/main.dart:58`, only ever reads the key `"route"`. Because the moments payload has no `"route"` key, **every tap on a moments-framework push (cold start, background, and — on Android — the locally-re-shown notification) resolves to `null` and silently does nothing**, leaving the user wherever the app already was (normally Main). This is not a platform quirk or a cold-start timing bug — it is a plain key-name mismatch between two payload conventions that evolved independently, and it is the single highest-leverage fix in this contract.

A second, independent family of notifications (`notify_summary_notification` for daily/weekly/monthly/yearly summaries, and admin broadcast) already uses the `"route"` key the client reads — but always points at `/main-page`, which is the literal "generic" behavior CS-06 was filed against.

A third finding: `TherapyPrepGenerator` (`app/services/moments/therapy_prep_generator.py:187`) sets `deep_link_route="prep_card_create"` — a bare alias string, not a real GoRouter path — but THERAPY_PREP moments are dispatched through the *generic* bottom sheet (`_showGenericSheet` in `moment_deep_link_screen.dart:144`), whose CTA calls `context.go(moment.deepLinkRoute)` directly with **no route-alias resolution and no try/catch**. This is a live latent bug: tapping "open" on a THERAPY_PREP moment's sheet passes an invalid path to GoRouter.

A fourth finding, forward-looking: `MoodDipAlertGenerator` (`app/services/moments/mood_dip_alert_generator.py:202`) hardcodes `deep_link_route=f"/stats/symptoms/{symptom_id}/history"`. CS-21 deletes the Stats screen this wave. If CS-11/CS-21 land without updating this generator, MOOD_DIP_ALERT pushes will deep-link into a route that no longer exists.

None of this requires new infrastructure. The moments framework, its DB-backed route field, its FCM delivery job, its GoRouter deep-link screen, and its per-type renderer dispatch are all already built and already handle **unknown enum values gracefully** (`@JsonKey(unknownEnumValue: MomentType.unknown)` in `notification_moment_model.dart:58`) — which is exactly the forward/backward-compatibility property CS-06 needs for old clients. The fix is: (1) make every FCM send-site populate one universal `route` key with a real, resolvable path, (2) fix the two concrete route bugs above, (3) add two new moment types for CS-11/CS-12, and (4) close a foreground/iOS display gap. Section 4 is the implementation plan; Section 3 is the payload contract itself.

---

## 2. Notification inventory (current state, verified in code)

### 2.1 Notification Moments framework — `app/services/moments/*`, delivered by `app/tasks/notification_orchestrator_job.py::deliver_due_moments()`

All 9 generators are registered at module scope in `app/services/moments/__init__.py` (imported at module scope by `notification_orchestrator_job.py`, per the Cadence v3 fix — confirmed still in place). Every FCM send for these 9 types goes through **one call site**: `notification_orchestrator_job.py:336-347`:

```python
send_fcm_to_all_user_tokens(
    db, moment.user_id, title=moment.push_title, body=moment.push_body,
    data={
        "type": "notification_moment",
        "moment_id": str(moment.id),
        "deep_link_route": moment.deep_link_route or "",
    },
    notification_type="notification_moment",
)
```

Note: **no `"route"` key.** This is the payload the FE currently receives for all 9 types below.

| # | Moment type (enum) | Generator file | Cadence / trigger | `deep_link_route` value set today | Category |
|---|---|---|---|---|---|
| 1 | `POST_SESSION_REFLECTION` | `post_session_reflection_generator.py:206` | ~26h after a session, dedup per session datetime | `"/therapy/between-sessions/new"` | REFLECTIONS |
| 2 | `MOOD_DIP_ALERT` | `mood_dip_alert_generator.py:202` | 3 high symptom scores in a row, dedup per symptom/day | `f"/stats/symptoms/{symptom_id}/history"` — **⚠ points at Stats, deleted by CS-21** | MOOD_TRENDS |
| 3 | `STREAK_CELEBRATION` | `streak_celebration_generator.py:143` | streak milestone (3/7/30/100/365), dedup per milestone | `"/character/streaks"` | STREAKS |
| 4 | `PATTERN_INSIGHT` | `pattern_insight_generator.py:148-151,188` | recurring topic 3+ in 14d, dedup per ISO week | `f"/insights/pattern/{topic_id}"` or `"/insights/patterns"` | INSIGHTS |
| 5 | `THERAPY_PREP` | `therapy_prep_generator.py:187` | scheduled before a session | **`"prep_card_create"`** — ⚠ not a real path, see §1 finding 3 | THERAPY_PREP |
| 6 | `REFLECTION_INVITATION` | `reflection_invitation_generator.py:258-268` | Cadence v3 baseline slot (10-13/18-21 local), dedup per local day | `"/fab/between-sessions"` (variant `session_today`) or `"/main-page/tab/reflect"` (generic) | REFLECTIONS |
| 7 | `DAILY_CHECK_IN` | `daily_check_in_generator.py:272-286` | Cadence v3 baseline slot, dedup per local day | `"/settings"` (schedule_nudge), `"/main-page"` (streak_status / generic) — **not in `MOMENT_TYPE_TO_CATEGORY`** (minor pre-existing gap, not in CS-06 scope) | (unmapped) |
| 8 | `SESSION_MORNING_OF` | `session_morning_of_generator.py:167-170,207` | 2-3.5h before a scheduled session, dedup per session local date | `f"/therapy/prep-card/{existing_prep_id}"` if a prep card already exists, else `"/fab/prepare-therapy"` | (unmapped) |
| 9 | `RE_ENGAGEMENT` | `re_engagement_generator.py:277` | inactivity ≥3d (push #1) / ≥7d (push #2), self-healing day count | `"/home"` — **⚠ not a registered route; `MsRoutes` has no `/home`, only `mainPageRoute = "/main-page"`** | REFLECTIONS |
| 10 | `WEEKLY_RECAP` | *(no generator file — enum member only)* | — | — | WEEKLY_SUMMARIES |
| 11 | `ACHIEVEMENT_UNLOCK` | *(no generator file — enum member only)* | — | — | STREAKS |

Full current enum (`app/models/notification_moment.py:51-61`): `POST_SESSION_REFLECTION, MOOD_DIP_ALERT, STREAK_CELEBRATION, PATTERN_INSIGHT, THERAPY_PREP, REFLECTION_INVITATION, WEEKLY_RECAP, ACHIEVEMENT_UNLOCK, RE_ENGAGEMENT, DAILY_CHECK_IN, SESSION_MORNING_OF`.

**Current tap behavior for all 9 live types:** none navigate anywhere (see §1). If/once the `route` key is added (Section 4), the *existing, already-shipped* dispatch in `moment_deep_link_screen.dart` takes over: 4 types get a rich contextual bottom sheet with AI content (`PostSessionReflectionSheet`, `MoodDipAlertSheet`, `StreakCelebrationSheet`, `MomentPatternInsightSheet`) whose own CTA then navigates to `moment.deepLinkRoute`; the other 5 (+2 reserved, +`unknown`) fall through to a bare generic sheet (`_showGenericSheet`) whose CTA does the same.

### 2.2 Legacy / non-moments FCM sends — `app/services/notification_service.py`, `app/tasks/broadcast.py`

| Send site | Status | Payload (`data=`) | Current tap behavior |
|---|---|---|---|
| `notify_summary_notification()` (`notification_service.py:301-311`), called from `app/services/periodic_summary.py:171,268,486,620` for Daily/Weekly/Monthly/Yearly summary generation | **LIVE** — fires on every summary generation | `{"route": "/main-page", "type": "summary_ready"}` | Navigates to Main (uses the `route` key the client *does* read) — this is the literal "generic" behavior CS-06 was filed against. All 4 summary cadences point at the same place regardless of which summary or period. |
| `_process_first_nudges()` / `_process_followup_nudges()` (`notification_service.py:533-816`) | **DEAD** — no scheduler entry calls these; docstring at `notification_service.py:362-366` confirms superseded by `PostSessionReflectionGenerator`, Cadence v3 cleanup 2026-07-03. Only referenced by `app/tests/test_post_session_nudge.py`. | `{"route": "/fab/after-therapy", "type": "post_session_nudge", "therapist_name":..., "session_date":...}` | N/A — not fired in production. **Do not resurrect without migrating to the unified schema in Section 3.** |
| `POST /api/v1/admin/broadcast` → `app/tasks/broadcast.py::execute_broadcast()` | LIVE, operator-triggered only | Arbitrary caller-supplied `data` dict (optional), no fixed schema | Whatever the operator puts in `data.route`; not a "notification type" in the CS-06 sense (ops tool). Should stay schema-agnostic but MUST be compatible with the client's route resolution if the operator wants a deep link — i.e., the operator should pass `{"route": "/some/real/path"}`. |

### 2.3 New types added by this batch (CS-11, CS-12) — **no existing generator; net-new**

| Type | Spec requirement | Existing backend hooks found | Gap |
|---|---|---|---|
| **CS-11 mood-update request** — fires after 3 days without a new mood/symptom entry | None. `MoodDipAlertGenerator` is a *symptom-score-dip* detector (3 high scores in a row), not a staleness/inactivity detector — different trigger condition entirely, do not conflate. `ReEngagementGenerator` (`re_engagement_generator.py`) is the closest **pattern** to model from: it already computes `days_inactive` from `crud.get_last_activity_datetime()` with a self-healing `>=` threshold and a `RE_ENGAGEMENT` dedup-key convention keyed on the inactivity window. Symptom/mood entry points exist at `app/api/v1/endpoints/symptoms.py`. | Needs: (a) new `MomentTypeEnum.MOOD_UPDATE_REQUEST` member (native PG enum → Alembic `ALTER TYPE ... ADD VALUE IF NOT EXISTS`, backend-api owns), (b) a new generator computing days-since-last-symptom/mood-entry (NOT reusing `MoodDipAlertGenerator`), (c) a `deep_link_route` pointing at the mood/symptom entry input card (route TBD — depends on where CS-11's "in-app prośba o update" input control lives on the new Main Mood Trend module; flutter-mobile defines this route once the module exists), (d) registration in `app/services/moments/__init__.py` + `notification_categories.py` (suggest category `MOOD_TRENDS`, shared with `MOOD_DIP_ALERT`). |
| **CS-12 therapy-relationship check-in reminder** — fires 1 day after each session, deep-links to the check-in | The check-in feature itself is **fully built**: `TherapyHealthCheck` model (`app/models/models.py:1317-1369`), `/api/v1/health-check/*` endpoints (`app/api/v1/endpoints/health_check.py`, registered at prefix `/health-check` in `app/api/v1/api.py:131-136`) — `GET /status` already returns `is_due` (via `crud.is_health_check_due` / `compute_health_check_due_date`, `crud.py:6331-6379`) which is exactly what CS-12's "Main slot 4 prompt visible until check-in done" needs, no new backend work required for that part. The *day-after-session push* is what's missing — no generator fires relative to "session ended + 24h" for this purpose today. Closest pattern to model from: `PostSessionReflectionGenerator`'s session-timing/dedup approach (dedup keyed on session datetime, ~26h-after timing window) and `SessionMorningOfGenerator`'s schedule-derived session-datetime computation. | Needs: (a) new `MomentTypeEnum.THERAPY_RELATIONSHIP_CHECKIN` member, (b) new generator firing once per session occurrence (dedup keyed on session datetime, mirroring `PostSessionReflectionGenerator`), (c) `deep_link_route` = the health-check submit flow route (`MsRoutes.healthCheckFlowRoute` = `/health-check`, confirmed registered in `lib/navigation/ms_routes.dart:70` — reuse as-is, no new FE route needed), (d) registration + category `THERAPY_PREP`-adjacent or new `THERAPY_RELATIONSHIP` category. **Open question for backend-api/product:** `compute_health_check_due_date` cadence is biweekly (<6 completed) / monthly (≥6 completed) — the spec text says "weekly therapy check-in" for the Main-prompt gating (CS-08/CS-12) and Workspace brief also says "weekly". This is a pre-existing cadence that predates this spec and does not match "weekly" literally; flag to product/backend-api, do not silently change it as part of CS-06. The push notification itself is unconditional (fires every session, independent of `is_due`), so this mismatch only affects the Main-prompt visibility gate, not the notification. |

---

## 3. Frontend current-state audit (verified in code)

### 3.1 The four FCM/local-notification entry points — all converge on one function

| Entry point | File:line | Behavior |
|---|---|---|
| Cold start (terminated → tapped) | `FirebaseMessaging.instance.getInitialMessage()` — `main.dart:897-904` | Resolves route via `_resolveNotificationRoute()`; stores it in the module-level `pendingNotificationRoute` string; **consumed later** by `splash_screen.dart:191-198` after auth completes, via `context.go(deepLink)` — **not wrapped in try/catch**, unlike the background path below. |
| Background (app backgrounded, OS notification tapped) | `FirebaseMessaging.onMessageOpenedApp.listen(...)` — `main.dart:880-894` | Resolves route via `_resolveNotificationRoute()`, then `_handleNotificationRoute(route)` (`main.dart:42-49`), which calls `sl<GoRouter>().go(route)` **inside a try/catch that silently no-ops on failure**. |
| Foreground (app open, message arrives) | `FirebaseMessaging.onMessage.listen(...)` — `main.dart:781-877` | Dispatches on `message.data['type']` to one of 8 hardcoded in-app-banner branches (`post_session_nudge*`, `health_check`, `prep_card_notification`, `journal_reminder`/`inactivity_reminder`, `symptom_tracking`, `weekly_summary`/`summary_ready`, `monthly_audit`, `mid_week_check_in`/`pre_session_check_in`, `session_recording`). **`type == "notification_moment"` is not one of them** → falls to the `else` branch → `FirebaseShowNotificationHelper().showNotification(message)` (`main.dart:930-977`), which is **gated `if (Platform.isAndroid)`** — on iOS, a moments-framework push arriving in the foreground produces **no visible UI at all** today (confirmed gap, not present in prior memory). |
| Local-notification tap (Android only — the re-shown notification from the foreground branch above) | `flutterLocalNotificationsPlugin.initialize(..., onDidReceiveNotificationResponse: ...)` — `main.dart:710-725` | Decodes the `payload` JSON string (which is `jsonEncode(message.data)` verbatim, set at `main.dart:953`) and calls the **same** `_resolveNotificationRoute()` → `_handleNotificationRoute()`. Same key-mismatch bug as background/cold-start. |

**Key finding: there is exactly one route-resolution function to fix**, `_resolveNotificationRoute()` (`main.dart:58-81`):

```dart
String? _resolveNotificationRoute(Map<String, dynamic> data) {
  final route = data['route'] as String?;
  if (route == null || route.isEmpty) return null;
  switch (route) {
    case 'prep_card': return _prepCardRoute(data) ?? MsRoutes.prepTherapyFlowRoute;
    case 'prep_card_create': return MsRoutes.prepTherapyFlowRoute;
    case 'moment':
      final rawId = data['moment_id'] as String?;
      final id = rawId != null ? int.tryParse(rawId) : null;
      return id != null ? '/moment/$id' : MsRoutes.mainPageRoute;
    case 'session_recording_ready': return MsRoutes.mainPageTherapyTabRoute;
    default: return route; // already a full path
  }
}
```

It reads **only** `data['route']`. It has a `case 'moment':` branch that would correctly build `/moment/$id` — but no backend send-site ever sets `route: 'moment'`, so this branch is currently unreachable dead code.

### 3.2 The `/moment/:id` deep-link screen — already fully built, already correct

`lib/screens/moments/moment_deep_link_screen.dart` (route `momentDetailRoute = '/moment/:id'`, `ms_routes.dart:80`) is a complete, working implementation: fetches the moment by ID (`GET /api/v1/moments/{id}`, HIGH-10 fix — not the generic "oldest active moment" endpoint), shows an explicit expired-state UI on 404, marks the moment `opened`, and dispatches to a type-specific rich renderer for 4 types or a generic sheet (`_showGenericSheet`, line 144-172) for everything else (including `unknown`). The generic sheet's primary CTA does:

```dart
final targetRoute = moment.deepLinkRoute.isNotEmpty ? moment.deepLinkRoute : MsRoutes.mainPageRoute;
onPrimaryCta: () { unawaited(cubit.markMomentActed(moment.id)); context.go(targetRoute); }
```

This is **not wrapped in try/catch** — an invalid `deepLinkRoute` string (see THERAPY_PREP's `"prep_card_create"` bug) will propagate whatever GoRouter does with an unmatched/malformed path.

**Conclusion: this screen and its dispatch logic need zero changes.** The only broken link is upstream — the FCM payload never causes the client to navigate to `/moment/$id` in the first place.

### 3.3 Route table (relevant entries), confirmed in `lib/navigation/ms_routes.dart`

```
mainPageRoute            = '/main-page'
mainPageTherapyTabRoute  = '/main-page/tab/therapy'
'/main-page/tab/:tab'    (generic tab-param route, line 160 — 'reflect' is a valid :tab value)
afterTherapyFlowRoute    = '/fab/after-therapy'
prepTherapyFlowRoute     = '/fab/prepare-therapy'
betweenSessionsFlowRoute = '/fab/between-sessions'
recordSessionFlowRoute   = '/fab/record-session'
healthCheckFlowRoute     = '/health-check'
prepCardDetailRoute      = '/therapy/prep-card/:id'
monthlyAuditDetailRoute  = '/therapy/monthly-audit/:id'
momentDetailRoute        = '/moment/:id'
settingsRoute            = '/settings'
```

No `/home` route exists — `RE_ENGAGEMENT`'s `deep_link_route="/home"` (§2.1 row 9) does not match anything; it will hit GoRouter's unmatched-route behavior. No `/stats/...`, `/workspace/...`, or `/insights/...` routes exist yet either — `MOOD_DIP_ALERT`'s `/stats/symptoms/{id}/history` and `PATTERN_INSIGHT`'s `/insights/pattern/{topic_id}` / `/insights/patterns` are **also currently unmatched** (Stats/Insights screens were not in scope to verify their route registration in detail here, but no matching path literal was found in `ms_routes.dart` — flutter-mobile must confirm before this wave ships, see Section 6 open items).

### 3.4 Current bottom nav (pre-Workspace-build state, for reference)

`main_page_body.dart` confirms today's tab pages: `TherapyTabScreen`, `ReflectTabScreen`, `StatsTabScreen`, `CharacterTabScreen` (plus Main itself). Per the Workspace feature brief: the tab currently named "Therapy" (Timeline content) will be renamed "Timeline"; the tab in the current "Stats" position will be replaced with Workspace content and labeled "Therapy". **Neither rename nor the Workspace screens exist in code yet** (confirmed — no `workspace` or `timeline` route/screen files found). This contract's route matrix (Section 5) includes forward-looking Workspace/Timeline route names as **placeholders for backend-api/flutter-mobile to bind in the wave that actually builds Workspace** — CS-06 itself must not block on Workspace existing (per spec: "Workspace build itself is handled outside this spec").

### 3.5 Package versions (`pubspec.yaml`)

`go_router: ^14.6.0`, `firebase_messaging: ^16.0.0`, `flutter_local_notifications: ^19.5.0`. iOS: `UIBackgroundModes` includes `remote-notification` (`Info.plist:49-53`, correct for background data messages). Android: `MainActivity` uses `launchMode="singleTop"` (`AndroidManifest.xml:22`). No custom `UNUserNotificationCenterDelegate` found in `AppDelegate.swift` — relies on FlutterFire's default self-registration; verify this still shows alerts while foregrounded on iOS (see pitfall in Section 4.4).

---

## 4. The contract: unified payload → route schema

### 4.1 Design principles (why this shape)

1. **One universal key wins:** every FCM send site — moments delivery, summary notifications, the two new CS-11/CS-12 generators, and (optionally) admin broadcast — MUST set a top-level `route` string equal to a real, currently-registered GoRouter path (with any IDs already interpolated, e.g. `/therapy/prep-card/123`). This is the ONLY key `_resolveNotificationRoute()` needs to read, and it already does. No new parsing logic, no new schema version negotiation.
2. **Additive, not replacing:** `type`, `moment_id`, `deep_link_route` stay exactly as they are today (other code — the in-app `/moments/upcoming` poll, `NotificationMomentResponse`, `MomentsCubit` — reads `deep_link_route` from the **API response**, not from the FCM payload; leaving it in the FCM data too costs nothing and avoids a second migration).
3. **FCM data values are always strings.** Confirmed both send implementations (`notification_service.py:125`, `broadcast.py:66`) already do `{k: str(v) for k, v in data.items()}` — the schema below assumes every value is a string; nested structures are not supported by FCM's data payload and must not be added.
4. **Old client / new payload:** an app build predating this fix reads `data['route']`. If a future payload's `route` points at a screen the old build doesn't have (e.g. a Workspace path added in a later wave), `_handleNotificationRoute`'s try/catch (background/local-tap path) degrades silently to "no navigation" — safe. The **cold-start path does not have this try/catch** (`splash_screen.dart:194`) — Section 4.4 requires adding one, both for old-client safety and because it's the same silent-degrade contract the background path already has.
5. **New client / old payload:** a payload that lacks `route` entirely (e.g. hitting a build lag where backend ships first) falls through today's `default: return route` only if `route` itself is present; if `route` is completely absent, `_resolveNotificationRoute` already returns `null` at line 60 and the app just opens to whatever it opens to by default (Main) — this is the existing, acceptable fallback and requires no change.
6. **Unknown moment types degrade for free.** `@JsonKey(unknownEnumValue: MomentType.unknown)` (`notification_moment_model.dart:58`) means an old client tapping a `MOOD_UPDATE_REQUEST` or `THERAPY_RELATIONSHIP_CHECKIN` push (new enum members it doesn't know) still parses the moment successfully as `MomentType.unknown`, still reaches `/moment/{id}` (once §4.2's fix ships), still shows the generic sheet, and still navigates via `deep_link_route`/`route`. **No Dart enum update is required for CS-06 to work end-to-end for the two new types** — updating the Dart `MomentType` enum is only needed if/when flutter-mobile wants a *dedicated* renderer for them instead of the generic sheet.

### 4.2 The fix, precisely

**Backend — one-line addition at the single moments delivery call site**, `app/tasks/notification_orchestrator_job.py:341-345`:

```python
data={
    "type": "notification_moment",
    "moment_id": str(moment.id),
    "deep_link_route": moment.deep_link_route or "",
    "route": f"/moment/{moment.id}",   # NEW — the only key the client route-resolver reads
},
```

This alone fixes cold start, background, and Android local-notification tap for **all 9 live moment types simultaneously**, because it routes every moment push through the already-correct, already-shipped `/moment/:id` screen. No per-generator route strings need to change for the *first hop* to work.

**Frontend — defense in depth**, add a branch to `_resolveNotificationRoute()` in `main.dart` so a payload missing `route` (e.g. from an already-in-flight/queued moment sent by an un-migrated worker during rollout) still resolves correctly:

```dart
case 'moment': // already present, currently unreachable — becomes reachable
  ...
default:
  if (data['type'] == 'notification_moment' && data['moment_id'] != null) {
    return '/moment/${data['moment_id']}';
  }
  return route;
```

This makes the two fixes independent and order-agnostic during rollout (see Section 6 sequencing).

**Two concrete bug fixes bundled into this same change:**

- `therapy_prep_generator.py:187` — change `deep_link_route="prep_card_create"` to `MsRoutes`-equivalent real path. Mirror `SessionMorningOfGenerator`'s pattern: if an in-progress prep card already exists for the upcoming session, `f"/therapy/prep-card/{prep_card_id}"`; otherwise `"/fab/prepare-therapy"`.
- `re_engagement_generator.py:277` — change `deep_link_route="/home"` to `"/main-page"` (the actual registered route; `/home` does not exist).

**One coordination item, not a CS-06 code change:** `mood_dip_alert_generator.py:202`'s `f"/stats/symptoms/{symptom_id}/history"` must be updated in lockstep with whichever wave ships CS-11 (Mood Trend moves to Main) and CS-21 (Stats deleted) — flag to backend-api now so it isn't forgotten; do not fix it in this wave since the destination route doesn't exist yet either way.

### 4.3 Payload → route matrix (every type that will exist after this batch)

All `route` values below are the values the corresponding backend code should send. Columns: Type · Trigger · `type` value · `route` value (FCM) · First-hop destination · Second-hop (sheet CTA) destination, where applicable.

| Type | Trigger | `type` | `route` (FCM) | First hop | Second hop (if generic/rich sheet) |
|---|---|---|---|---|---|
| POST_SESSION_REFLECTION | ~26h after session | `notification_moment` | `/moment/{id}` | `/moment/{id}` → rich sheet (has AI content) | CTA → `/therapy/between-sessions/new` |
| MOOD_DIP_ALERT | 3 high scores in a row | `notification_moment` | `/moment/{id}` | `/moment/{id}` → rich sheet | CTA → `deep_link_route` (Stats today; **must be repointed when CS-11/CS-21 ship** — see §4.2) |
| STREAK_CELEBRATION | streak milestone | `notification_moment` | `/moment/{id}` | `/moment/{id}` → rich sheet | CTA → `/character/streaks` |
| PATTERN_INSIGHT | recurring topic | `notification_moment` | `/moment/{id}` | `/moment/{id}` → rich sheet | CTA → `/insights/pattern/{id}` or `/insights/patterns` (flutter-mobile: confirm these routes are actually registered — not found in `ms_routes.dart` during this audit) |
| THERAPY_PREP | before session | `notification_moment` | `/moment/{id}` | `/moment/{id}` → generic sheet | CTA → `/therapy/prep-card/{id}` or `/fab/prepare-therapy` (fixed per §4.2) |
| REFLECTION_INVITATION | Cadence v3 slot | `notification_moment` | `/moment/{id}` | `/moment/{id}` → generic sheet | CTA → `/fab/between-sessions` or `/main-page/tab/reflect` |
| DAILY_CHECK_IN | Cadence v3 slot | `notification_moment` | `/moment/{id}` | `/moment/{id}` → generic sheet | CTA → `/settings` or `/main-page` |
| SESSION_MORNING_OF | 2-3.5h before session | `notification_moment` | `/moment/{id}` | `/moment/{id}` → generic sheet | CTA → `/therapy/prep-card/{id}` or `/fab/prepare-therapy` |
| RE_ENGAGEMENT | inactivity 3d/7d | `notification_moment` | `/moment/{id}` | `/moment/{id}` → generic sheet | CTA → `/main-page` (fixed per §4.2) |
| WEEKLY_RECAP *(reserved, no generator)* | — | `notification_moment` | `/moment/{id}` | generic sheet | CTA → TBD when a generator ships |
| ACHIEVEMENT_UNLOCK *(reserved, no generator)* | — | `notification_moment` | `/moment/{id}` | generic sheet | CTA → TBD when a generator ships |
| **MOOD_UPDATE_REQUEST** *(NEW — CS-11)* | 3 days without new mood/symptom entry | `notification_moment` | `/moment/{id}` | `/moment/{id}` → generic sheet (or new dedicated sheet if flutter-mobile chooses) | CTA → Main Mood Trend module's entry control (route TBD — owned by whoever builds the CS-11 Main module; must be a real path by the time this generator ships) |
| **THERAPY_RELATIONSHIP_CHECKIN** *(NEW — CS-12)* | 1 day after each session | `notification_moment` | `/moment/{id}` | `/moment/{id}` → generic sheet | CTA → `/health-check` (`MsRoutes.healthCheckFlowRoute`, already registered — no new FE route needed) |
| Daily/Weekly/Monthly/Yearly summary ready | summary generation completes | `summary_ready` | **change from `/main-page` to the specific summary/output-card route** (e.g. `/main-page/tab/therapy` + surfacing the new summary in Timeline, or a dedicated summary-detail route if one exists — flutter-mobile to confirm/define; at minimum land on the tab that contains the summary, not bare Main) | direct (no sheet) | — |
| Admin broadcast | operator-triggered | caller-defined, recommend `broadcast` | operator-supplied; must be a real path if a deep link is wanted | direct | — |
| *(Future — Workspace, not this wave)* Agenda item / Do zrobienia / Wątki / Realizations / Goals card references in a triaged-output-card notification | — | — | placeholder convention: `/workspace/agenda`, `/workspace/todo`, `/workspace/threads/{id}`, `/workspace/realizations`, `/workspace/goals/{id}` | — | for whichever wave builds Workspace to bind |
| *(Future — Timeline, renamed from Therapy tab)* | — | — | existing `/main-page/tab/therapy`, `/therapy/prep-card/:id`, `/therapy/monthly-audit/:id` patterns are unaffected by the rename — no route changes needed for CS-06 | — | — |

### 4.4 Cold start / background / foreground notes (Flutter, both platforms) + known pitfalls

- **Cold start (terminated):** `getInitialMessage()` fires once, before `runApp()`. The resolved route is stashed in `pendingNotificationRoute` and consumed by the splash screen *after* auth completes (`splash_screen.dart:191-198`) — this ordering is already correct and required (you cannot `context.go()` before the router/auth state exists). **Pitfall found:** this consumption site calls `context.go(deepLink)` with no try/catch, unlike the background path's `_handleNotificationRoute`. **Add the same try/catch here** so an old client receiving a not-yet-registered route degrades silently instead of throwing during the splash → main-page transition. This is a required part of this wave, not optional polish — it's the backward-compatibility guarantee Section 4.1 point 4 depends on.
- **Background (app suspended, OS tray notification tapped):** `onMessageOpenedApp` — already correctly wired, already has the safe try/catch. No changes needed beyond the payload/route fix itself.
- **Foreground (app open when message arrives):** two sub-paths, both need attention:
  - Add a `type == 'notification_moment'` branch to the `onMessage.listen` dispatcher (`main.dart:781-869`, alongside the other 8 branches) that shows an in-app banner (BotToast, consistent with the existing pattern) using `push_title`/`push_body`, with tap-through calling `_handleNotificationRoute('/moment/${data['moment_id']}')`. This closes the **iOS foreground gap** identified in §3.1 (currently: nothing is shown on iOS for a foreground moments push, since `FirebaseShowNotificationHelper` is Android-gated).
  - Verify iOS foreground presentation: no `UNUserNotificationCenterDelegate` override was found in `AppDelegate.swift`. If FlutterFire's default foreground presentation options do not include `.alert`, an OS-level banner will not show even for the *notification* (title/body) part of the payload while foregrounded on iOS — separate from the in-app-banner fix above but worth a physical-device check per platform (this is the exact kind of thing the CS-06 risk note in the spec calls out — "deep-linking with cold start on Flutter is fiddly; test both platforms").
- **Android-specific:** `launchMode="singleTop"` on `MainActivity` means a tapped notification while the app is already running in the background reuses the existing Activity instance (correct, required for `onMessageOpenedApp` to fire instead of a fresh cold start). No change needed, just confirming it's already correct — do not let a future manifest edit regress this.
- **iOS-specific:** APNs data payload has a combined size cap around 4KB; the schema in Section 4.3 stays well under this (a handful of short string keys) — no risk today, but do not add large free-text fields (e.g. full AI observation text) to the FCM `data` payload itself. Rich content stays server-side, fetched via `GET /moments/{id}` by the deep-link screen, exactly as already designed — do not be tempted to shortcut this by stuffing content into the push payload.
- **Both platforms:** confirm `/insights/pattern/:id`, `/insights/patterns`, and any Workspace/summary-detail routes referenced in Section 4.3 are actually registered in `ms_routes.dart` before the corresponding generator ships pointing at them — this audit found `PATTERN_INSIGHT`'s routes are not currently present in the route table checked.

---

## 5. Implementation plan (file:function level)

### Backend (`backend-api` for migrations/models, `data-analytics` for generator logic — coordinate per CLAUDE.md's shared-file rules)

1. `app/tasks/notification_orchestrator_job.py:341-345` — add `"route": f"/moment/{moment.id}"` to the `deliver_due_moments()` FCM data dict. **Single highest-leverage change in this contract.**
2. `app/services/moments/therapy_prep_generator.py:187` — fix `deep_link_route` from `"prep_card_create"` to a real path (existing prep card vs. new, mirroring `session_morning_of_generator.py:167-170`).
3. `app/services/moments/re_engagement_generator.py:277` — fix `deep_link_route` from `"/home"` to `"/main-page"`.
4. `app/services/notification_service.py::notify_summary_notification()` (line 301-311) — change `data={"route": "/main-page", ...}` to route at the specific summary/output card per summary_type; requires `periodic_summary.py`'s 4 call sites (lines 171, 268, 486, 620) to pass through enough context (e.g. summary ID or period) for the route to be built. Coordinate with `data-analytics` (this file is jointly relevant — `notification_service.py` itself is not explicitly listed in either agent's ownership table in CLAUDE.md; confirm ownership with the lead before editing, per the "shared files require coordination" rule).
5. **New: MOOD_UPDATE_REQUEST generator (CS-11).** New file `app/services/moments/mood_update_request_generator.py` modeled on `re_engagement_generator.py`'s day-counting pattern, but scoped to last symptom/mood-entry timestamp (not general activity). Add `MomentTypeEnum.MOOD_UPDATE_REQUEST` to `app/models/notification_moment.py`, an Alembic migration (`backend-api` owns) doing `ALTER TYPE moment_type_enum ADD VALUE IF NOT EXISTS 'MOOD_UPDATE_REQUEST'` in an autocommit block (per the project's established enum-migration convention), register in `app/services/moments/__init__.py`, add category mapping in `notification_categories.py` (suggest `MOOD_TRENDS`, shared with `MOOD_DIP_ALERT`).
6. **New: THERAPY_RELATIONSHIP_CHECKIN generator (CS-12).** New file `app/services/moments/therapy_relationship_checkin_generator.py` modeled on `post_session_reflection_generator.py`'s session-timing/dedup pattern (fire once per session occurrence, ~24h after), `deep_link_route = MsRoutes.healthCheckFlowRoute` equivalent (`"/health-check"`). Same migration/registration steps as #5, new enum member `THERAPY_RELATIONSHIP_CHECKIN`.
7. Flag to product/backend-api (do not silently resolve): the "weekly" cadence language in CS-12/Workspace-brief vs. `compute_health_check_due_date`'s actual biweekly/monthly cadence (`crud.py:6331-6379`).

### Frontend (`flutter-mobile`)

1. `lib/main.dart::_resolveNotificationRoute()` (line 58) — add the `type == 'notification_moment'` fallback branch (Section 4.2). Zero risk to existing branches; purely additive.
2. `lib/main.dart` — add a `notification_moment` branch to the `onMessage.listen` foreground dispatcher (line ~781-869) showing an in-app banner with tap-through to `/moment/{moment_id}`, closing the iOS foreground gap (Section 4.4).
3. `lib/screens/splash/splash_screen.dart:191-198` — wrap the cold-start `context.go(deepLink)` call in the same try/catch pattern already used by `_handleNotificationRoute()` in `main.dart:42-49`.
4. Confirm (or register) GoRouter paths referenced by `PATTERN_INSIGHT` (`/insights/pattern/:id`, `/insights/patterns`) — this audit could not confirm these exist; if they don't, either register them or have `pattern_insight_generator.py` fall back to an existing route until they do.
5. When CS-11's Main Mood Trend module and CS-12's health-check flow are touched by their respective feature work, confirm the exact CTA route each generator should target (Section 4.3 rows for MOOD_UPDATE_REQUEST / THERAPY_RELATIONSHIP_CHECKIN) and relay it back to backend-api/data-analytics — `/health-check` is already known and requires no new route.
6. No Dart `MomentType` enum changes are required for CS-06 itself (Section 4.1 point 6) — only if a dedicated (non-generic) renderer is wanted for the two new types, which is out of scope here.

### Sequencing (per CLAUDE.md's deployment rule: backend first when dependent)

1. Ship backend fixes #1-3 (Section 5, backend list) first — they are pure additive/corrective changes to existing live code, safe to deploy standalone, and immediately fix the core bug for old AND new app builds (old builds already read `route`; they just weren't receiving one).
2. Ship frontend fixes #1-3 (defense-in-depth + iOS foreground gap + splash try/catch) in the next TestFlight/Play build — order-independent relative to step 1 because of the belt-and-suspenders design (Section 4.1 point 4-5), but both should land in the same wave to close the iOS-foreground and cold-start-crash gaps together.
3. CS-11 and CS-12 generators (backend items #5-6) ship together with their respective Main-module/health-check-flow frontend work — these are net-new notification types, so there is no backward-compat ordering constraint beyond "don't send a push whose CTA route doesn't exist yet on any live client," per Section 4.1 point 4's safe-degrade guarantee.
4. The `MOOD_DIP_ALERT` Stats-route fix is **not** part of this wave — track it as a required follow-up item tied to whichever PR actually deletes the Stats screen (CS-21) or moves Mood Trend to Main (CS-11's UI half). Do not let CS-21 ship without it — it would silently 404-equivalent an existing, currently-shipped notification type.

---

## 6. Manual test matrix (required in the PR per spec DONE_WHEN)

Test every notification type × (cold start / background / foreground) × (iOS / Android). "Lands correctly" = first hop reaches `/moment/{id}` (or the direct route for non-moment types) and, where a second-hop CTA exists, the CTA reaches the exact card/screen referenced by the push.

| Type | Cold start iOS | Cold start Android | Background iOS | Background Android | Foreground iOS | Foreground Android |
|---|---|---|---|---|---|---|
| POST_SESSION_REFLECTION | ☐ | ☐ | ☐ | ☐ | ☐ (new banner branch) | ☐ |
| MOOD_DIP_ALERT | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| STREAK_CELEBRATION | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| PATTERN_INSIGHT | ☐ (confirm route registered first) | ☐ | ☐ | ☐ | ☐ | ☐ |
| THERAPY_PREP | ☐ (verify fixed route, not `prep_card_create`) | ☐ | ☐ | ☐ | ☐ | ☐ |
| REFLECTION_INVITATION | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| DAILY_CHECK_IN | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| SESSION_MORNING_OF | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| RE_ENGAGEMENT | ☐ (verify fixed `/main-page`, not `/home`) | ☐ | ☐ | ☐ | ☐ | ☐ |
| MOOD_UPDATE_REQUEST (CS-11, new) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| THERAPY_RELATIONSHIP_CHECKIN (CS-12, new) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| Daily/Weekly/Monthly/Yearly summary ready | ☐ (verify lands on specific summary, not bare Main) | ☐ | ☐ | ☐ | ☐ | ☐ |
| Admin broadcast (with a `route` payload) | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

Additional required checks (not per-type, but per the risk note in the spec — "cold start on Flutter is fiddly"):
- ☐ Old app build (pre-fix) receiving a NEW payload (post-fix backend) — confirm silent, non-crashing degrade on both cold start and background, both platforms (validates Section 4.1 point 4 and the splash-screen try/catch fix).
- ☐ New app build receiving an OLD-shape payload (e.g. a moment already enqueued by a not-yet-restarted worker during rollout) — confirm the frontend fallback branch (Section 4.2, `type == 'notification_moment'` without `route`) still resolves correctly.
- ☐ Tapping a notification whose target route requires auth/onboarding state not yet loaded (cold start racing auth) — confirm `pendingNotificationRoute` consumption in `splash_screen.dart` still gates correctly behind auth completion.
- ☐ iOS foreground presentation — confirm OS-level banner actually shows for a data-only or notification+data moments push while the app is foregrounded (separate from the new in-app-banner branch); check `AppDelegate.swift` foreground presentation options if not.

---

## 7. Open items requiring a decision before/during implementation

1. **PATTERN_INSIGHT routes** (`/insights/pattern/:id`, `/insights/patterns`) — not found registered in `ms_routes.dart` during this audit. flutter-mobile must confirm these exist (perhaps under a different path convention) or register them before this type is exercised in the test matrix.
2. **MOOD_DIP_ALERT's Stats-pointing route** — must be repointed as part of CS-11/CS-21, tracked as a dependency, not fixed in this wave (destination doesn't exist yet).
3. **CS-11's exact Mood Trend entry-point route** — depends on the CS-11 Main-module implementation; the generator's `deep_link_route` cannot be finalized until that route exists. Backend generator can ship with a placeholder pointing at `/main-page` and be updated in the same PR that ships the Main module, or the two can ship together.
4. **CS-12 cadence wording mismatch** ("weekly" in spec vs. biweekly/monthly in `compute_health_check_due_date`) — needs a product/backend-api decision; does not block the notification itself (which is unconditional per-session), only affects the Main-prompt visibility gate's actual cadence.
5. **`notify_summary_notification`'s new target route** — "the specific summary/output-card route" needs a concrete answer from data-analytics/flutter-mobile: does a summary-detail screen exist, or should this simply land on the Timeline tab filtered/scrolled to the relevant summary? This audit did not find a dedicated summary-detail route and did not attempt to invent one.
6. **Ownership of `app/services/notification_service.py` for the summary-route fix** — not explicitly assigned in CLAUDE.md's file ownership table between `backend-api` and `data-analytics`; the lead should assign this explicitly before work starts, per the "shared files require coordination through the lead" rule.
