# CS-21 – Notification audit checklist

Required deliverable for MSV3.3 CS-21: *"A written checklist enumerates every notification with its trigger condition and target destination, and each entry is verified on a device build on both platforms."*

Compiled 2026-08-14 from a read-only code audit of `MindSync/app/services/moments/`, `moment_hooks.py`, `notification_routes.py`, `services/insights/`, and the Flutter router `lib/navigation/ms_routes.dart`.

**Status legend for the device column:** `[ ]` = not yet verified on device · `[A]` = verified Android · `[i]` = verified iOS.
Every row needs all three checks: **fires when its condition is truly met (and never otherwise)**, **deep-links to its target card**, **no in-app duplicate** (CS-20).

---

## A · Moment generators – real pushes via `NotificationMoment` + FCM

16 live generators. Pass 1 = scored, Pass 2 = schedule-driven, Pass 3 = deterministic.

| # | Moment type | Trigger condition | Toggle key | Copy source | Deep link | Route exists? | Device |
|---|---|---|---|---|---|---|---|
| 1 | `THERAPY_APPOINTMENT` | T−24h and T−3h before next session (Pass 2) | `therapy_appointment` | static fallback | `/main-page/tab/workspace?section=agenda` | yes | `[ ]` |
| 2 | `ADD_THERAPY_DATE` | local hour == 18 AND `compute_next_session_date()` is None (Pass 3) | `add_therapy_date` | static fallback | `/settings?section=therapy_schedule` | yes | `[ ]` |
| 3 | `POST_SESSION_REFLECTION` | session ended ≤26h ago AND no debrief exists; delivered at start+75min (Pass 2) | `after_therapy` | AI + fallback | `/fab/after-therapy` | yes | `[ ]` |
| 4 | `THERAPY_PREP` | T−24h/T−3h slot due AND no prep card for that session (Pass 2) | `prepare_for_therapy` | AI + fallback | `/fab/prepare-therapy` | yes | `[ ]` |
| 5 | `BETWEEN_SESSIONS_NOTE` | hour==18, last+next session known, `days_to_next > 3`, debrief exists, no note this cycle (Pass 3) | `between_sessions` | static fallback | `/fab/between-sessions?new=true` | yes ⚠ query param ignored – builder takes no args | `[ ]` |
| 6 | `RECORD_SESSION` | session start −8 min; skipped if session already started (Pass 2) | `record_session` | static fallback | `/fab/record-session` | yes | `[ ]` |
| 7 | `HOMEWORK_REMINDER` | hour==18 exactly 3 days before session AND ≥1 OPEN todo with origin THERAPIST (Pass 3) | `homework` | static fallback | `/main-page/tab/workspace?section=todo` | yes | `[ ]` |
| 8 | `MOOD_UPDATE_REQUEST` | hour==18 AND ≥3 days since last SymptomScore; repeats every 3d; never-logged users excluded (Pass 3) | `mood_trends` | AI + fallback | `/main-page/tab/main?section=mood_trends` | yes | `[ ]` |
| 9 | `REFLECTION_INVITATION` | Sunday hour==18 AND no REFLECT conversation this Mon–Sun week (Pass 3) | `reflect` | `reflection_invitation_generic` | `/main-page/tab/reflect?new=true` | yes | `[ ]` |
| 10 | `GOALS_WEEKLY` | event hook – weekly goal-narrative regen completes; night rule 21:00–08:00 defers to next 08:00 | `goals` | `goals_weekly_ready` | `/main-page/tab/workspace?section=goals` | yes | `[ ]` |
| 11 | `THERAPY_RELATIONSHIP_CHECKIN` | Sunday hour==18 AND no `TherapyHealthCheck` this Mon–Sun week (Pass 3) | `therapy_relationship` | AI + fallback | `/health-check` | yes | `[ ]` |
| 12 | `WEEKLY_SUMMARY_READY` | event hook – a `WeeklyTherapySummary` row is created | `weekly_summary` | `weekly_summary_ready` | `/therapy/weekly-summary/{id}` | yes | `[ ]` |
| 13 | `MONTHLY_SUMMARY_READY` | event hook – a `MonthlyTherapyAudit` row is created | `monthly_summary` | `monthly_audit_ready` | `/therapy/monthly-audit/{id}` | yes | `[ ]` |
| 14 | `ACCOUNT_SETUP_NUDGE` | created_at +24/48/72/96h AND user still has zero `UserGoal` (Pass 3) | **none** (system) | `account_setup_nudge` | `/main-page/tab/workspace?section=goals&setup=true` | yes | `[ ]` |
| 15 | `MOOD_DIP_ALERT` | ≥3 consecutive scores ≥7 on a negative-keyword symptom; suppressed if all ≥9; 1 per symptom / 5 days (Pass 1, base 8.0) | none (interest category) | AI + fallback | `/main-page/tab/main?section=mood_trends` (hardcoded) | yes | `[ ]` |
| 16 | `RE_ENGAGEMENT` | `days_inactive ≥3` (push 1) / `≥7` (push 2); max 2 per inactivity window (Pass 1, base 6.0) | `re_engagement_push` | AI + warm/cold fallbacks | `/main-page` (hardcoded) | yes | `[ ]` |

**All 14 routes in the backend `MOMENT_ROUTES` table resolve in the Flutter router.** No dead moment deep links.

### Retired enum members – no generator, kept only for historical rows
`STREAK_CELEBRATION` · `PATTERN_INSIGHT` · `DAILY_CHECK_IN` · `SESSION_MORNING_OF` · `WEEKLY_RECAP` · `ACHIEVEMENT_UNLOCK`

---

## B · Non-moment push paths

| Path | Trigger | Copy | Route | Notes | Device |
|---|---|---|---|---|---|
| `session_recording` | recording summary finishes processing | hardcoded EN, not localized ⚠ | `/therapy/recording/{id}` | resolves | `[ ]` |
| `summary_ready` | legacy `PeriodicSummary` generation | localized | `/main-page` | ☠ **DEAD** – not registered in any scheduler setup; only entrypoint is a standalone script not in the Procfile | n/a |
| `post_session_nudge` / `_followup` | – | localized | `/fab/after-therapy` | ☠ **DEAD** – `_process_first_nudges` / `_process_followup_nudges` have no callers | n/a |
| `admin_broadcast` | operator-triggered | operator-supplied | passthrough | live, manual only | `[ ]` |

---

## C · In-app insights (no push; rendered in-app)

| Insight | Trigger | Form factor | CTA route | Route exists? | Device |
|---|---|---|---|---|---|
| `NOTICE` | `APP_OPENED` | inline banner | `/stats` | ❌ **DEAD → "Page Not Found"** – this is the CS-19 bug | `[ ]` |
| `REVEAL` | `STATS_TAB_OPENED` | toast | `/stats/symptoms/{id}` | ❌ **DEAD** | `[ ]` |
| `CELEBRATE_TEASE` | multiple | inline banner | `/character/streaks` | ❌ **DEAD** | `[ ]` |
| `RECOVERY_MOMENT` | `STATS_TAB_OPENED`, `APP_OPENED` | bottom sheet | `/stats/symptoms/{id}/history` or `/stats` | ❌ **DEAD** | `[ ]` |
| `COMPARATIVE` | `DEBRIEF_SAVED`, `NOTE_ADDED` | toast | `/stats` | ❌ **DEAD** | `[ ]` |
| `PATTERN` | – | – | – | no detector registered; the Flutter sheet is unreachable | n/a |

⚠ `STATS_TAB_OPENED` is **no longer fired by the client** (removed with the Workspace tab), so `REVEAL` can never fire and `RECOVERY_MOMENT` only fires via `APP_OPENED`.

### Consolidated dead routes – all reachable from a notification/insight surface

| Dead path | Source | Surface | Severity |
|---|---|---|---|
| `/stats` | `notice_insight_detector.py`, `comparative_insight_detector.py`, `recovery_moment_insight_detector.py` | in-app insight CTA | the CS-19 bug |
| `/stats/symptoms/{id}` | `reveal_insight_detector.py` | in-app insight CTA | `REVEAL` can no longer fire (its trigger was removed) |
| `/stats/symptoms/{id}/history` | `recovery_moment_insight_detector.py` | in-app insight CTA | reachable via `APP_OPENED` |
| `/character/streaks` | `celebrate_tease_insight_detector.py` | in-app insight CTA | reachable |
| **`/exercises/breathing/quick`** | **`mood_dip_alert_generator.py:~190-196`** | **`primary_cta.route` on a LIVE push** | **worst of the five – a real push whose primary CTA dead-ends** |

The fifth was found late, during the CS-21 implementation pass. It matters more than the other four: `MOOD_DIP_ALERT` is a live Pass 1 scored generator, so this is a push a real user receives. Its `deep_link_route` (`/main-page/tab/main?section=mood_trends`) is fine – only the CTA payload is dead. **The 14 `MOMENT_ROUTES` deep links were all verified routable; the CTA payload fields had never been checked.** A full generator-by-generator CTA audit is in progress.

**Residual risk, unresolvable from source:** the retired `STREAK_CELEBRATION` and `PATTERN_INSIGHT` generators have been deleted (only stale `.pyc` remain), so their CTA routes cannot be read. Surviving unexpired historical moment rows from before their retirement could still surface a dead CTA.

CS-21 requires that "Page Not Found" must never be reachable from a notification. **All five must be neutralised** – client-side (no dead button renders) and server-side (stop emitting them).

---

## D · Cross-cutting defects found by the audit

1. **CS-18 – custom session dates are invisible, two independent bugs.**
   (a) The date is *deleted on save*: the backend nulls `custom_therapy_sessions` whenever `frequency != "custom"`, and the Flutter one-off flow never sets frequency (it defaults to `weekly`).
   (b) Even if stored, the resolver only consults custom sessions inside the `frequency == "custom"` branch. A user with a one-off date and no recurring entries resolves to `next_session = None`.
   This propagates to **10 other consumers** of `compute_next_session_date`, so it is not only the "no next session" push that is wrong.

2. **CS-20 – in-app duplication is by design and must be reversed.** Push and in-app read the *same* moment row; `get_pending_or_sent_moment_for_user` filters `status IN (PENDING, SENT)` and explicitly orders SENT *before* PENDING, so the already-pushed row is the preferred in-app card. Narrowing the filter to PENDING stops duplication while leaving the whole mechanism intact for undelivered moments (e.g. `no_token` users).

3. **Flutter moment enum gap.** The client knows only 12 `MomentType` values and is missing all 9 added in MSV3.2.2, so they decode to `unknown` and always fall back to the generic sheet instead of their typed renderer.

4. **`session_recording` push copy is hardcoded English**, unlike every other path which goes through `notification_texts.py`.

---

## E · Sign-off

| Check | Status |
|---|---|
| Every notification enumerated with trigger + destination | done (this document) |
| Every deep link verified to resolve in the router | done – 14/14 moment routes resolve; 4 insight routes dead |
| Dead routes neutralised | pending implementation |
| No in-app duplicate of a pushed message (CS-20) | pending implementation |
| Each entry verified on an Android device build | pending |
| Each entry verified on an iOS device build | pending |
