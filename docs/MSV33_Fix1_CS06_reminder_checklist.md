# MSV3.3.Fix.1 CS-06 – In-app reminder routing checklist

Backend half completed 2026-08-19 (backend-api). This is the written
checklist the spec's `Done when` demands: every reminder type × surface ×
trigger × destination, ticked on a device build once the frontend half (a
`flutter-mobile` task, tracked separately) lands.

**Location note:** this file lives at the shared `Heroku/docs/` level (newly
created) rather than inside either repo's own `docs/` folder
(`MindSync/docs/`, `mindsync-frontend/docs/`) because it spans both repos and
both platforms. A related but superseded artifact exists at
`mindsync-frontend/docs/CS-06_manual_test_matrix.md` – that one is the
MSV3.2 CS-06 "does it deep-link at all" matrix (references `PATTERN_INSIGHT`
/ `STREAK_CELEBRATION`, both retired types); this document supersedes it for
the reminder-routing question. That older file is left as-is (not owned by
this batch).

**Scope of this pass:** backend only (routes, payload CTA fields,
`push_delivered` exposure). The frontend half – wiring `InsightDispatcher`
for bottom-sheet insights, removing/using the dead renderers, adding the
`pushDelivered` field to the client moment model and gating on it instead of
`status`, and implementing the `?section=` anchors on the Main/Workspace/
Character tabs – is a separate `flutter-mobile` task. Rows below are marked
**BE done** or **FE pending** accordingly. The "Device ✓" column stays empty
for the operator until both halves ship and are verified on a physical
build.

---

## 1. Notification moments (`GET /moments/upcoming`, generic bottom sheet unless noted)

These 14 rows resolve via `app/services/notification_routes.py` (`MOMENT_ROUTES` + `route_for()`) except MOOD_DIP_ALERT and RE_ENGAGEMENT, which build their route inline in their own generator (they predate the CS-03 13-row canonical set).

| # | Type | Trigger | Destination | Backend status | Device ✓ |
|---|---|---|---|---|---|
| 1 | THERAPY_APPOINTMENT | day-precision scheduled | `/main-page/tab/workspace?section=agenda` | Unchanged – verified already resolves | ☐ |
| 2 | ADD_THERAPY_DATE | day-precision scheduled, throttled | `/settings?section=therapy_schedule` (client redirects to `/my-therapy`) | Unchanged – verified already resolves; throttle untouched | ☐ |
| 3 | POST_SESSION_REFLECTION | after session ends | `/fab/after-therapy` | Unchanged – verified already resolves | ☐ |
| 4 | THERAPY_PREP | T-24h / T-3h before session | `/fab/prepare-therapy` | Unchanged – verified already resolves | ☐ |
| 5 | BETWEEN_SESSIONS_NOTE | daily, shared hour, window active | `/fab/between-sessions` | **CHANGED**: dropped inert `?new=true` (client never read it – composer always opens blank) | ☐ |
| 6 | RECORD_SESSION | day-precision scheduled | `/fab/record-session` | Unchanged – verified already resolves | ☐ |
| 7 | HOMEWORK_REMINDER | day-precision scheduled | `/main-page/tab/workspace?section=todo` | Unchanged – verified already resolves | ☐ |
| 8 | MOOD_UPDATE_REQUEST | day-precision scheduled | `/main-page/tab/main?section=mood_trends` | Unchanged – verified already resolves | ☐ |
| 9 | REFLECTION_INVITATION | day-precision scheduled | `/main-page/tab/reflect?new=true` (functional param – starts a new thread) | Unchanged – verified already resolves | ☐ |
| 10 | GOALS_WEEKLY | weekly hook | `/main-page/tab/workspace?section=goals` | Unchanged – verified already resolves | ☐ |
| 11 | THERAPY_RELATIONSHIP_CHECKIN | day-precision scheduled | `/health-check` | Unchanged – verified already resolves | ☐ |
| 12 | WEEKLY_SUMMARY_READY | weekly summary hook | `/therapy/weekly-summary/{id}` | Unchanged – verified already resolves | ☐ |
| 13 | MONTHLY_SUMMARY_READY | monthly audit hook | `/therapy/monthly-audit/{id}` | Unchanged – verified already resolves | ☐ |
| 14 | ACCOUNT_SETUP_NUDGE | CS-07 system nudge | `/main-page/tab/workspace?section=goals&setup=true` | Unchanged – verified already resolves | ☐ |
| 15 | MOOD_DIP_ALERT | symptom pattern (push) **+** in-app sheet | `/main-page/tab/main?section=mood_trends` – **same destination for both entries now** | **CHANGED**: `payload.primary_cta.route` was `None` (push-entry and in-app-entry diverged); now matches `deep_link_route`. Label changed from "90s breathing" to "Log today's mood" (no breathing feature exists). Secondary CTA relabelled "Not now" (was "Quick log mood", now redundant with primary) | ✅ **FE done** (2026-08-19) — `mood_dip_alert_sheet.dart` (push-tap entry): fallback route changed `MsRoutes.betweenSessionsFlowRoute` → new `MsRoutes.mainTabMoodTrendsRoute` constant; fallback label changed `moments_breathingExercise` → new `moments_logTodaysMood` ARB key (7 locales, English text shipped everywhere per project convention); payload route now gated through `MsRoutes.isRoutable` before being trusted. In-app entry (`main_page_body.dart`'s generic sheet) needed no code change — it already reads `moment.deepLinkRoute` directly, now backend-set to the same anchor. Device ☐ |
| 16 | RE_ENGAGEMENT | 3d / 7d inactivity (push) **+** in-app sheet | `/fab/between-sessions` | **CHANGED**: was `/main-page` (bare home tab – the "dead end wearing a button" pattern). Now opens the lightest capture flow to get a lapsed user back in | ✅ **FE done** — no code change needed; renders via the same generic in-app sheet as row 15, which now also skips rendering entirely if a future moment ever arrives with an unroutable route (see §"Don't-render" rule below). Device ☐ |

## 2. App insights (`GET /insights/pending`)

| # | Type | Surface | Destination | Backend status | Device ✓ |
|---|---|---|---|---|---|
| 17 | RECOVERY_MOMENT | bottom sheet | `/main-page/tab/main?section=mood_trends` | **CHANGED**: `cta_route`/`cta_label` and `payload.primary_cta.route` were all `None`; now set. Talks about a symptom recovering → Mood Trend | ✅ **FE done** (2026-08-19) — see "Frontend implementation" below, §Dispatcher decision. Wired (not removed): `RecoveryMomentSheet` now renders via a direct switch in `main_page_body.dart`'s `FormFactor.bottomSheet` case, gated on `MsRoutes.isRoutable(insight.ctaRoute)`. Device ☐ |
| 18 | REVEAL | toast | `/main-page/tab/main?section=mood_trends` | **CHANGED**: was `None`/`None`. Reports a week-over-week symptom change → Mood Trend | ✅ **FE done** — no code change needed; `RevealToastRenderer` already gated the tap action via `MsRoutes.isRoutable`, so the backend route fix alone makes it tappable. Device ☐ |
| 19 | COMPARATIVE | toast | `/main-page/tab/main?section=mood_trends` | **CHANGED**: was `/main-page/tab/workspace` (bare tab). Compares entry counts across periods – a mood/tracking signal → Mood Trend | ✅ **FE done** — no code change needed, same reasoning as REVEAL (`ComparativeToastRenderer` already isRoutable-gated). Device ☐ |
| 20 | NOTICE | inline banner | `/main-page/tab/workspace?section={anchor}` – see kind→anchor mapping below | **CHANGED**: was `/main-page/tab/workspace` (bare tab, no section) | ✅ **FE done** — no code change needed; the banner-rendering code in `main_page_body.dart`'s `build()` already gates its CTA via `MsRoutes.isRoutable`. `notice_banner_renderer.dart` (a separate, never-called renderer with a hardcoded no-CTA-ever behaviour that would have been WRONG under this fix) was removed — see Dispatcher decision below. Device ☐ |
| 21 | CELEBRATE_TEASE | inline banner | `/main-page/tab/character?section={anchor}` – see anchor mapping below | **CHANGED**: was `/main-page/tab/character` (bare tab, no section) | ✅ **FE done** (2026-08-19) — `character_tab_screen.dart` now implements the `?section=` anchor (`character.streaks`, wrapping `PetHeroCard`) via the same `SectionAnchorRegistry`/`MainNavCubit.scrollTarget` pattern as Workspace/Main; `level` is deliberately left unregistered (no live producer yet) — `SectionAnchorRegistry.scrollTo` already no-ops safely for it. See "Frontend implementation" below, §Character tab anchor, for why `streaks` anchors to `PetHeroCard` rather than a dedicated streak widget. Device ☐ |

### NOTICE kind → Workspace anchor mapping

Implemented in `app/services/insights/notice_insight_detector.py::_anchor_for_observation_type`. This detector currently only ever produces two observation-type prefixes, and neither concerns agenda/todo content specifically – both fall back to the spec's documented default (`goals`):

| `observation_type` prefix | Anchor | Why |
|---|---|---|
| `best_time_*` (e.g. `best_time_morning`) | `goals` (fallback) | Describes *when* the user journals – a general usage pattern, not agenda/todo content |
| `most_active_day_*` (e.g. `most_active_day_3`) | `goals` (fallback) | Same – a usage-rhythm observation, not tied to one Workspace module |
| `agenda*` (reserved, not currently produced) | `agenda` | Ready for a future notice kind that genuinely concerns upcoming sessions |
| `todo*` (reserved, not currently produced) | `todo` | Ready for a future notice kind that genuinely concerns homework/todo items |
| anything else unmapped | `goals` | Spec's explicit fallback: "a notice kind with no matching section → Workspace → Goals" |

### CELEBRATE_TEASE milestone → Character anchor mapping

Implemented in `app/services/insights/celebrate_tease_insight_detector.py::_anchor_for_milestone_type`:

| `milestone_type` prefix | Anchor | Status |
|---|---|---|
| `streak*` (`streak_three`, `streak_week`, `streak_month` – the only values this detector currently produces) | `streaks` | **Live today** – every CELEBRATE_TEASE candidate resolves here |
| `level*` (reserved, not currently produced by any generator) | `level` | Ready for a future level-up celebration reusing this same detector/anchor scheme |
| anything else unmapped | `streaks` | Conservative default matching current behaviour |

flutter-mobile implements the Character-tab `?section=` anchors under these exact names (`streaks`, `level`).

### BETWEEN_SESSIONS_NOTE `?new=true` decision

**Dropped.** The Flutter route builder (`ms_routes.dart:548-551`, verified while grounding this item) never read the `new` query param – the between-sessions note composer always opens a blank note regardless of how it was reached. The param was inert weight on the URL, not a functional flag, so `MOMENT_ROUTES["BETWEEN_SESSIONS_NOTE"]` and `RE_ENGAGEMENT`'s hardcoded route (which now points at the same flow) both omit it. Contrast with `REFLECTION_INVITATION`'s `?new=true`, which IS read by the client (`action: 'new_thread'`) and is correctly left in place.

---

## 3. `push_delivered` exposure (client double gate, spec item (i))

- `NotificationMomentResponse` (`app/schemas/notification_moment.py`) now carries `push_delivered: bool` – **additive**, non-nullable, matching the DB column.
- Backend keep-logic in `app.crud.notification_moment.get_pending_or_sent_moment_for_user` is **unchanged**: a `SENT` moment with `push_delivered=False` was already being kept for the in-app channel (CS-20 / 16.08 work) – this item only exposes the field so the client can act on it.
- ✅ **FE done** (2026-08-19): `pushDelivered` (nullable `bool?`, NOT `@Default(false)`) added to `NotificationMomentModel`; `shouldAutoShowMomentSheet` now branches on it — `null` (old-backend response, field absent) falls back to the exact pre-CS-06 gate (`status != SENT`); a real value shows whenever `!pushDelivered`. See "Frontend implementation" below, §push_delivered gate, for why nullable (not defaulted) was required for true backward compatibility.

## 4. `route_for()` fallback removal (spec item (iii))

- `app/services/notification_routes.py::route_for()` no longer returns `"/main-page"` for an unmapped `moment_type` – it returns `None` and logs a structured warning (`[NOTIFICATION_ROUTES] route_for: no route mapped for moment_type=...`).
- Every currently-registered generator that calls `route_for()` always passes a literal `MomentTypeEnum` member that IS a key in `MOMENT_ROUTES` (verified by grep – all 12 call sites across `app/services/moments/*.py` and `app/services/moment_hooks.py` pass one of the 14 mapped types). `None` is therefore not expected on any live path today; the change exists so a future typo/omission fails loudly (logged) instead of shipping a dead-end route.
- `app/tasks/notification_orchestrator_job.py::deliver_due_moments` already writes `moment.deep_link_route or ""` into the FCM payload – no crash risk if a future caller does hit `None` before persisting (though `deep_link_route` is `NOT NULL` in the DB, so a generator that received `None` from `route_for()` and did not guard against it would fail moment creation, not delivery; this is flagged for awareness, not fixed here – out of this item's scope per the task's file list, and no live call site is affected).
- ✅ **FE done** (2026-08-19): the generic NotificationMoment bottom sheet (`main_page_body.dart::_showMomentSheet`) and its cold-start-deep-link twin (`moment_deep_link_screen.dart::_showGenericSheet`) both now check `MsRoutes.isRoutable(moment.deepLinkRoute)` **before** showing anything — an unroutable moment is skipped entirely (logged, not rendered), instead of falling back to an "Open" button pointing at `/main-page`. See "Frontend implementation" below, §Don't-render rule.

---

## Recon summary (Change Safety, CLAUDE.md)

- **Consumers grepped**: `cta_route`/`primary_cta`/`deep_link_route`/`push_delivered` across the Flutter codebase (`mindsync-frontend/mindsync_app/lib/`) – confirmed `push_delivered`/`pushDelivered` had **zero** existing references (additive is safe) and located every renderer/route-resolver file that reads the fields this batch changed (`recovery_moment_sheet.dart`, `reveal_toast_renderer.dart`, `comparative_toast_renderer.dart`, `notice_banner_renderer.dart` / `inline_notice_banner.dart`, `celebrate_tease_renderer.dart`, `mood_dip_alert_sheet.dart`, `moments_cubit.dart`, `ms_routes.dart`) – none edited (flutter-mobile's file ownership).
- **Boot-critical check**: `import app.main` under the test harness's env bootstrap (`app/tests/conftest.py`) with RQ mocked – all modified modules (`notification_routes`, all 5 insight detectors, `mood_dip_alert_generator`, `re_engagement_generator`, `between_sessions_note_generator`) imported cleanly and every generator/detector registered without error (confirmed via the orchestrator's own `[ORCH] Registered ...` / `[DETECTOR] Registered ...` log lines). Import subsequently hit an unrelated, pre-existing local-environment limitation (`firebase_admin` rejecting the dummy JSON credential string used by local env vars) that is not reachable through the pytest harness proper – confirmed separately via `app/tests/test_deploy_before_migrate_session_poisoning.py`, which imports the full app stack under pytest and passed.
- **Response-shape change**: `push_delivered` addition to `NotificationMomentResponse` is additive only (new field, nothing renamed/removed).
- **Migration**: none required – `push_delivered` already exists as a DB column (migration `mm4n5o6p7q8r`, 16.08 work); this batch only exposes it in the Pydantic response schema.

## Test results

Targeted files (363 tests): `test_notification_routes.py` (new), `test_recovery_moment_insight_detector.py`, `test_reveal_insight_detector.py`, `test_comparative_insight_detector.py`, `test_notice_insight_detector.py`, `test_celebrate_tease_insight_detector.py`, `test_mood_dip_alert_generator.py`, `test_re_engagement_generator.py`, `test_cs06_payload_fixes.py`, `test_moments_endpoints.py`, `test_moments_endpoints_get_by_id.py`, `test_msv322_new_generators.py` – **all pass**.

Broader sweep (`-k "notification or moment or insight"`, 1038 selected): **1038 passed**, 4 pre-existing failures unrelated to this change (`test_notification_improvements.py::TestBetweenSessionsPlaceholder` ×3 – checks `app.crud.crud._DEFAULT_NOTIFICATION_PREFS`/source comments, a file this batch never touches; `TestNotificationTimezoneIndexMigration::test_migration_creates_index` – a migration-state check, also untouched). These match the project's known pre-existing RED baseline, not a regression from this batch.

---

# Frontend implementation (flutter-mobile, 2026-08-19)

Client half of CS-06. Every row marked "FE pending" above is now "FE done" —
device ticks (✓) stay empty for the operator's physical-build pass; this
section is the reasoning + verification-in-code trail behind each one.

## push_delivered gate

`lib/api/models/moments/notification_moment_model.dart` — added
`bool? pushDelivered` as an **additive, nullable** field (deliberately NOT
`@Default(false)`). The nullability is load-bearing: a response from a
backend that predates this field parses the key as absent → `null`, which
must be told apart from an explicit `false` sent by an up-to-date backend.
`@Default(false)` would have collapsed both cases to `false` and silently
changed behaviour for anyone still talking to an old backend during a
staged rollout.

`lib/screens/moments/cubit/moments_cubit.dart::shouldAutoShowMomentSheet`:
```dart
bool shouldAutoShowMomentSheet(NotificationMomentModel moment) {
  final delivered = moment.pushDelivered;
  if (delivered == null) {
    return moment.status != MomentStatus.sent; // pre-CS-06 gate, unchanged
  }
  return !delivered;
}
```
`null` → old CS-20 behaviour exactly; a real value → the new CS-06 gate
(show whenever the push channel did NOT already reach the user, regardless
of `status` — this is what makes a `SENT`-but-`push_delivered=false` moment,
which the backend deliberately keeps around for exactly this reason, show
up as an in-app card for a user with no working FCM token).

Tests: `test/bloc/moments/moments_cubit_test.dart` (new group "CS-06 —
shouldAutoShowMomentSheet (pushDelivered gate)" — false/true/null-fallback,
all 6 `MomentStatus` values crossed with each); `test/api/models/moments/
notification_moment_model_test.dart` (new group "pushDelivered — CS-06
additive field" — parses true/false/absent, round-trips through `toJson`).

## Don't-render rule

Two call sites render a **generic** NotificationMoment sheet (as opposed to
a typed renderer like `MoodDipAlertSheet`), and both previously fell back to
`/main-page` when the route was empty/dead. Both now skip rendering
entirely instead:

- `lib/screens/main_page/main_page_body.dart::_showMomentSheet` — the
  in-app auto-popup path (`_loadMomentsOnOpen`). Computes
  `MsRoutes.isRoutable(moment.deepLinkRoute)` **before** calling
  `MomentBottomSheet.show`; if false (and the moment isn't the
  hardcoded-route check-in reminder, which is exempt), logs and returns
  with nothing shown. Safe to skip silently: the caller already marked the
  moment `opened` before invoking this method, so it won't be re-offered on
  the next app open.
- `lib/screens/moments/moment_deep_link_screen.dart::_showGenericSheet` —
  the cold-start push-tap path (`/moment/:id`). Same gate, same skip. The
  caller (`_resolve`) still does its unconditional
  `context.go(MsRoutes.mainPageRoute)` afterward — identical to what
  happens once any shown sheet resolves — so a stale/dead deep-link tap
  silently lands the user on Main without ever showing a dead button.

The `FormFactor.bottomSheet` case for **app insights** (in
`_loadMomentsOnOpen`) gets the equivalent gate on `insight.ctaRoute`,
folded into the dispatcher rewrite below (same file, same method).

Toasts and inline banners (REVEAL/COMPARATIVE/NOTICE/CELEBRATE_TEASE) were
deliberately **left as graceful-degrade-not-skip**: they already hide just
the CTA button (not the whole toast/banner) when the route is unroutable —
that's pre-existing CS-19/CS-21 behaviour, not the "Open → /main-page"
anti-pattern this item targets, and in practice the backend now always
sends a real route for all 4 of these types, so the distinction is
defense-in-depth only. Bottom sheets are the one surface whose entire
purpose is the primary action, so they're held to the stricter "don't
render at all" standard; a passive toast/banner still conveys useful
information even without a working tap target.

Tests: `test/screens/moments/moment_deep_link_screen_test.dart` (new tests
in the "generic sheet fallback" group — a `/stats`-routed and an
empty-routed moment both render nothing and still land on `Main Page`);
`test/navigation/ms_routes_cs01_deep_link_test.dart` (new group
"MsRoutes.isRoutable — CS-06 reminder destination routes" — every
target-table destination string is asserted routable).

## Dispatcher / dead-renderer decision (spec item ii)

Grepped every call site of `RecoveryMomentSheet`, `PatternInsightSheet`, and
`NoticeBannerRenderer` before touching anything. Finding: **all three were
100% unreachable in production**, not just the two the spec text named —
`InsightDispatcher.dispatch()` is only ever invoked for
`FormFactor.toast` insights (`main_page_body.dart`'s
`case FormFactor.toast:`); its `pattern`/`recoveryMoment`/`notice`/
`celebrateTease` switch cases existed but nothing ever called `dispatch()`
with one of those. `CELEBRATE_TEASE` and `NOTICE` insights DO render today,
just via separate, direct code in `MainPageBody.build()`'s inline-banner
list — `CelebrateTeaseRenderer` for the former, and inline generic
`InlineNoticeBanner` construction (NOT `NoticeBannerRenderer`) for the
latter.

Decision, per renderer:

- **`RecoveryMomentSheet` (wired, not removed).** RECOVERY_MOMENT is a live
  insight type with a real, invested hero visualization (symptom
  before/after comparison bars + warm orca) and 4 passing widget tests.
  `main_page_body.dart`'s `FormFactor.bottomSheet` case now switches on
  `insight.insightType` and calls `RecoveryMomentSheet.show(context,
  insight)` directly (not through `InsightDispatcher` — that dispatcher
  doesn't own the surrounding `_momentSheetShowing`/`mounted`/CS-17
  `pauseMomentQueue()` bookkeeping this call needs, and duplicating that
  logic inside the dispatcher for one caller wasn't worth it). Per
  `feedback_pause_on_navigate_pattern.md` (this agent's own memory,
  originally written for CS-17): the caller only needs to check `!mounted`
  after the `await` and call `pauseMomentQueue()` — it does NOT need
  `RecoveryMomentSheet` itself to know about the queue, so wiring it in was
  a same-file, low-risk change, not a re-architecture.
- **`PatternInsightSheet` (wired for symmetry, currently unreachable at
  runtime).** PATTERN is not produced by any of the 5 currently-registered
  insight detectors (reveal/recovery_moment/notice/comparative/
  celebrate_tease) — it predates the CS-03 canonical 5-detector set. It is
  now reachable (same switch, same file) rather than deleted, matching this
  codebase's established "keep dead-but-future-ready code, documented"
  convention (see the CS-20 comment in `moments_cubit.dart` for
  precedent). If PATTERN is ever formally retired, delete
  `pattern_insight_sheet.dart` + its test + this switch case together.
- **`NoticeBannerRenderer` (removed).** Unlike the two above, this one was
  not just unreachable — it was **actively wrong** under the new contract.
  Its own doc comment says "NOTICE insights are informational — no CTA
  label", and its implementation hardcodes `ctaLabel: null, onCta: null`,
  ignoring `insight.ctaRoute`/`ctaLabel` entirely. But NOTICE now HAS a real
  `cta_route` from the backend (a Workspace anchor) that should be
  tappable — the ALREADY-LIVE inline banner code in `main_page_body.dart`
  handles this correctly (reads `insight.ctaRoute`/`ctaLabel`, gates via
  `MsRoutes.isRoutable`). Keeping the dead, outdated class around risked a
  future maintainer "fixing" the wrong file. Deleted `notice_banner_renderer
  .dart` and its test (`notice_banner_renderer_test.dart`).

`InsightDispatcher.dispatch()` was simplified to match reality: its switch
now only has real cases for `reveal`/`comparative` (its only two actual
callers, both toast); every other `InsightType` falls into one
documented, logged catch-all branch. The class's doc comment now states
outright that `dispatch()` is toast-only and points to where each other
form factor actually renders.

Tests: `test/widgets/moments/renderers/insight_dispatcher_test.dart` (new
group — pattern/notice/celebrateTease/recoveryMoment delivered as a toast
log and complete without throwing); `test/widgets/moments/renderers/
recovery_moment_sheet_test.dart` (new group "CS-06 route safety net" — the
payload's `primary_cta.route` is now ALSO gated through
`MsRoutes.isRoutable`, falling back to `insight.ctaRoute`, which the caller
in `main_page_body.dart` already verified routable before showing the sheet
at all — defense in depth, not the primary gate).

## Character tab anchor

`lib/screens/character_tab/character_tab_screen.dart` now implements the
`?section=` anchor infrastructure Workspace (`workspace_screen.dart:174,
191,202`) and Main (`main_tab_screen.dart:443`) already use:
`SectionAnchorRegistry`/`SectionAnchor` + a `scrollTarget` `ValueNotifier`
listener on `MainNavCubit`, added to `_CharacterTabScreenState` (the
existing stateful shell that already owns `CharacterTabCubit`, rather than
converting the stateless `_CharacterTabBody` to stateful).

**Which widget does `character.streaks` wrap, and why:** grepped the whole
Character tab for "streak" — zero hits. There is no dedicated streak-count
widget on this tab today (the gamification streak UI CLAUDE.md describes —
counter, calendar, freeze indicator — has not been built yet; that's a
separate, much larger feature, out of this routing-fix item's scope). Of
the tab's 3 existing cards (`PetHeroCard`, `BioCard`, `ActivityCard`),
`PetHeroCard` was chosen as the `character.streaks` anchor target: it's the
tab's hero element, already carries a "Level-Up" celebration badge, and is
the closest thing to a celebration-adjacent landing spot that exists today
— landing there beats a bare tab. This is flagged as a decision, not a
discovery: **if a dedicated streak-count widget is ever built, move the
`SectionAnchor` onto it** — the id `'character.streaks'` is the stable
contract the backend/other renderers depend on, not the `PetHeroCard`
wrapping.

`level` (the milestone-type prefix reserved for a future level-up
celebration) is deliberately left **unregistered** — no `SectionAnchor` id
`'character.level'` exists anywhere. `SectionAnchorRegistry.scrollTo`
already no-ops safely for any id with no matching anchor (verified by the
pre-existing "graceful no-ops" tests in `section_anchor_test.dart`), so this
satisfies the spec's "no-op-safe reserved value" requirement with zero
extra code — registering it prematurely against a widget with no real
level-up content would have been a worse anchor target than no anchor at
all.

Tests: `test/utils/section_anchor_test.dart` (new group
"SectionAnchorRegistry.scrollTo — character.streaks (CS-06)" — happy path +
the `level` no-op, mirroring the file's existing `workspace.todo`
pattern); `test/navigation/ms_routes_cs01_deep_link_test.dart` (new group —
`parseTabDeepLinkParams({'section': 'streaks'})` and `{'section': 'level'}`
both parse correctly; this parsing is tab-agnostic shared code, already
covered for Workspace/Main sections, extended here for Character).

## Files changed

- `lib/api/models/moments/notification_moment_model.dart` (+ regenerated
  `.freezed.dart`/`.g.dart`) — `pushDelivered` field
- `lib/screens/moments/cubit/moments_cubit.dart` — gate rewrite
- `lib/navigation/ms_routes.dart` — `mainTabMoodTrendsRoute` constant
- `lib/widgets/moments/renderers/mood_dip_alert_sheet.dart` — route/label
  fix, `isRoutable` gate
- `lib/widgets/moments/renderers/recovery_moment_sheet.dart` — `isRoutable`
  safety net on the payload route
- `lib/widgets/moments/renderers/insight_dispatcher.dart` — simplified to
  toast-only, dead branches removed
- `lib/widgets/moments/renderers/notice_banner_renderer.dart` — **deleted**
  (+ its test)
- `lib/screens/main_page/main_page_body.dart` — don't-render gate on the
  generic moment sheet; bottom-sheet insight case now dispatches to
  `RecoveryMomentSheet`/`PatternInsightSheet` directly
- `lib/screens/moments/moment_deep_link_screen.dart` — matching don't-render
  gate on its own generic-sheet fallback
- `lib/screens/character_tab/character_tab_screen.dart` — `character.streaks`
  section anchor
- `lib/l10n/app_{en,pl,de,fr,es,nb,sv}.arb` (+ regenerated
  `l10n/generated/*`) — new `moments_logTodaysMood` key (English text in
  all 7 locales per project convention; soft-warned, not hard-failed, by
  `l10n_completeness_test.dart`)
- Tests: `test/bloc/moments/moments_cubit_test.dart`,
  `test/api/models/moments/notification_moment_model_test.dart`,
  `test/screens/moments/moment_deep_link_screen_test.dart`,
  `test/navigation/ms_routes_cs01_deep_link_test.dart`,
  `test/utils/section_anchor_test.dart`,
  `test/widgets/moments/renderers/mood_dip_alert_sheet_test.dart`,
  `test/widgets/moments/renderers/recovery_moment_sheet_test.dart`,
  `test/widgets/moments/renderers/insight_dispatcher_test.dart`,
  `test/widgets/moments/renderers/notice_banner_renderer_test.dart`
  (**deleted**, tested a removed class)

## Frontend test results

_Filled in after the full targeted run — see the commit this section's edit
lands in._
