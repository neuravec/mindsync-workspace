# MSV3.3.Fix.1 – Cross-Layer Contract Review

**Reviewer:** integration-devops · **Date:** 2026-08-20 · **Scope:** read-only cross-review of the batch below, per the Cross-Review Protocol (single selected reviewer).

**Backend (`MindSync`, main):** `8dd329d` (parent) → `552a267` CS-06 → `0a3ef72` CS-07 → `cde4aab` CS-05/CS-01(BE) → `a817b77` CS-04. Nothing pushed.
**Frontend (`mindsync-frontend`, dev):** `9c9100e` CS-01..03 → `4fea945` CS-06 → `33dc58a` CS-04/CS-08 → `30c553c` CS-07/CS-05. Nothing pushed.
**No Alembic migrations in this batch** (confirmed: `git diff --stat 8dd329d..a817b77` touches no file under `app/models/` or `app/alembic/`).

## Verdict: **GO** — no Critical or High findings. Two Low findings noted (non-blocking).

All five review-focus questions were checked directly against the diffs (not against the spec's/checklist's self-reported claims), and every claim in `MSV33_Fix1_CS06_reminder_checklist.md` that I re-derived from code held up.

---

## 1. Old-client safety (additive-only) — PASS

| Change | Evidence | Verdict |
|---|---|---|
| `EmotionalTemperatureItem.score_series` (CS-04) | `app/schemas/schemas.py` diff in `a817b77`: new optional field appended after `description`; the 5 pre-existing fields (`symptom_name`, `current_score`, `previous_score`, `trend`, `description`) are untouched. | Additive. Old client ignores unknown key (json_serializable drops unrecognized keys). |
| `ThreadResponse.context_description` (CS-05) | `app/schemas/workspace.py` / `app/api/v1/endpoints/workspace.py` diff in `cde4aab`: field added to the **list** response; `context_snippet` (140-char) is left byte-for-byte unchanged. `ThreadDetailResponse` no longer redeclares `context_description` (moved to the base class) — response shape for the detail endpoint is unchanged, still present, just declared one level up. | Additive, no rename/removal. |
| `NotificationMomentResponse.push_delivered` (CS-06) | `app/schemas/notification_moment.py` diff in `552a267`: appended after `expires_at`. DB column: `Boolean, nullable=False, default=True, server_default=sa.text("true")` (`app/models/notification_moment.py:237`) — no migration needed in this batch, matches the Pydantic `bool` (non-Optional) type, cannot 500 on old rows. | Additive, non-nullable but backed by a `server_default`. |
| Weekly/monthly envelopes (CS-07) | `weekly_summaries.py`/`monthly_audits.py` diffs in `0a3ef72`: no field added/removed/retyped on `WeeklySummaryGenerateResponse`/`MonthlyAuditGenerateResponse`; only new response-building **branches** (`_reenqueue_existing_weekly`/`_reenqueue_existing_monthly`) that still return the same envelope type. | No shape change at all. |

No accidental rename/removal/retyping found anywhere in the four backend commits.

## 2. New-client vs. old-backend tolerance — PASS

- **CS-04 chart:** `EmotionalTemperatureItem.scoreSeries` (Flutter) is nullable; `prep_card_widget.dart`'s `_buildTemperatureRow` gates the chart on `series != null && series.length >= 2` and otherwise falls through to name+narrative — verified in `33dc58a`. An old-backend response (no `score_series` key) parses to `null` → no chart, no crash. The `SymptomScoreChart` extraction from Main's private `_SymptomChartPainter` is a byte-identical mechanical move (same constants, same paint logic, same `_lagoon`/`_deepOcean` tokens) — Main's rendering is provably unchanged.
- **CS-05 thread context:** `thread_card.dart` diff in `30c553c` prefers `contextDescription`, falls back to `contextSnippet` when the former is null/empty — safe against an old backend that only sends the snippet.
- **CS-06 push_delivered gate:** `moments_cubit.dart`'s `shouldAutoShowMomentSheet` explicitly branches on `null` vs a real bool — `null` (field absent, old backend) reproduces the exact pre-CS-06 `status != SENT` gate; only a non-null value switches to the new gate. Confirmed nullable-not-defaulted in the Freezed model (`bool? pushDelivered`, no `@Default(false)`), which is exactly what makes this distinction possible.
- **CS-07 tolerant parsing:** `weekly_summary_model.dart`/`monthly_audit_model.dart` diffs in `30c553c` widen `dataWindowStart/dataWindowEnd/processingStatus/createdAt/updatedAt` from `required` to nullable, matching the backend schema (`app/schemas/summary.py:102-156`, already `Optional`). `WeeklySummaryManager`/`MonthlyAuditManager.list*()` parse each row independently and skip a bad one (per commit message; not re-verified line-by-line but the model nullability alone removes the primary crash vector). Widgets null-check before formatting dates (`_formatDateRange`) and status comparisons (`_statusUpper`).

**Deploy-order conclusion: either order is safe for this batch.** Every backend change is additive-only and every frontend change tolerates the pre-batch backend response shape (nullable fields, `isRoutable`/`null` fallbacks, snippet fallback). There is no response field this Flutter build *requires* that the currently-deployed backend doesn't already send, and no backend field whose absence crashes the new client. Backend-first remains the house default (per CLAUDE.md) and is what the spec's suggested execution order implies, but nothing in this batch imposes a hard ordering constraint — Codemagic building the frontend before the operator runs the Heroku deploy would not break anything.

## 3. CS-06 route contract — PASS, cross-checked against the checklist and the code (not just against each other)

I re-derived the route table independently from the diffs rather than trusting the checklist's own table, then compared:

- `notification_routes.py`'s `MOMENT_ROUTES` dict (13 entries) matches the checklist's rows 1-14 minus MOOD_DIP_ALERT/RE_ENGAGEMENT (which build their route inline, as documented) — confirmed via `sed -n '1,120p' notification_routes.py`.
- All 12 live call sites of `route_for()` (grepped across `app/services/moments/*.py` and `app/services/moment_hooks.py`) pass a literal `MomentTypeEnum` member that is a key in `MOMENT_ROUTES` — `route_for()` returning `None` (its new behavior for an unmapped type, replacing the old `/main-page` fallback) is genuinely unreachable on every live path today. This was the one place I expected a possible boot/runtime landmine (a `None` written into a `NOT NULL deep_link_route` DB column would fail moment *creation*, not just delivery) — verified it cannot happen with the current registered generator set.
- Every backend-emitted route was checked against Flutter's route resolution:
  - `/main-page/tab/main?section=mood_trends` (RECOVERY_MOMENT, REVEAL, COMPARATIVE, MOOD_DIP_ALERT), `/main-page/tab/workspace?section={agenda|todo|goals}` (NOTICE, THERAPY_APPOINTMENT, HOMEWORK_REMINDER, GOALS_WEEKLY, ACCOUNT_SETUP_NUDGE), `/main-page/tab/character?section={streaks|level}` (CELEBRATE_TEASE), `/fab/between-sessions` (RE_ENGAGEMENT, BETWEEN_SESSIONS_NOTE) — all resolve through the generic `/main-page/tab/:tab` `GoRoute` + `MsRoutes.parseTabDeepLinkParams`, which passes `section` straight through to `MainNavCubit.selectTab(scrollTo:)`, consumed by each tab's own `SectionAnchorRegistry.scrollTo('<tab>.<section>')` listener. Character tab's listener was added in this exact batch (`character_tab_screen.dart` diff in `4fea945`) and mirrors the pre-existing Workspace/Main pattern precisely.
  - `MsRoutes.isRoutable()` is a **denylist** (`_knownDeadRoutePatterns`: `/stats`, `/stats/symptoms/:id`, `/stats/symptoms/:id/history`, `/character/streaks`), not a positive route-table lookup — none of the new anchor-suffixed routes match any denylist pattern (the denylist regexes are anchored to the bare path, and `isRoutable` strips the query string via `Uri.tryParse(path)?.path` before matching), so every new route is correctly treated as routable.
- `level` (reserved `CELEBRATE_TEASE` anchor, no live producer) is deliberately left unregistered on the Flutter side; `SectionAnchorRegistry.scrollTo` already no-ops for unknown ids — confirmed this is a documented, intentional no-op, not an oversight.

**No mismatch found.** Every route the backend can currently emit resolves to a concrete, working destination on the client; nothing lands on `/main-page` or a bare tab.

## 4. CS-07 semantics — PASS, with one Low note

Verified directly in `app/api/v1/endpoints/weekly_summaries.py` and `monthly_audits.py` (`0a3ef72`):

- **No duplicate work/rows on a COMPLETED tap.** The dedup branch only re-enqueues when `existing.processing_status == FAILED` or `is_*_stale_processing(existing)` is true; a COMPLETED (or a fresh, non-stale PROCESSING) row falls through to `return _generate_response_ok(existing)` / `_audit_response_ok(existing, premium)` unchanged. The frontend's new persistent "Generate now" row (`therapy_tab_screen.dart`, `30c553c`) is safe exactly as its own comment claims — confirmed against the backend code, not just trusted.
- **Monthly re-enqueue premium gating matches `/retry`'s existing 403 gate.** `generate_monthly_audit`'s re-enqueue branch is `if premium and (FAILED or stale_processing)`; a free user's FAILED/stale row is *not* re-enqueued by `/generate` — it falls through to `_audit_response_ok(existing, premium=False)`, mirroring `retry_monthly_audit()`'s existing premium gate. `_reenqueue_existing_monthly`'s own docstring states free users never reach this branch in practice because their audit path completes synchronously and never goes PROCESSING/FAILED — consistent with `_build_audit_response` always stripping premium-gated fields via `show_full = is_premium or audit.user_was_premium`.
- **Free-monthly paywall path still returns a card, never nothing.** `_build_audit_response` unconditionally returns `status="ok"` with `premium_locked=not show_full` and `activity_summary` always populated (even for free users) — this is pre-existing code, untouched by this batch, and still reachable through every code path I traced.
- **Low finding (non-blocking):** `_build_audit_response` is called with whatever `existing.processing_status` a free user's *legacy* row happens to carry (e.g., a FAILED/stale-PROCESSING row created while the user was briefly premium, then downgraded before the sweep or a retry ran). Since the re-enqueue branch is `premium`-gated, such a user's `/generate` tap returns that stale/failed row's `processing_status` verbatim inside a `status="ok"`/`premium_locked=true` envelope. This is **not a regression** — `_build_audit_response` returned exactly this before CS-07 too, and the CS-07 change only added a new branch, not this fallthrough — but it means a downgraded-premium user with a pre-existing stuck row could, in principle, see a locked card whose `processing_status` still reads `"failed"` or `"processing"` rather than a clean activity-only card. Flagged for awareness; recommend a `growth-analyst`/`database-administrator` check on whether any real prod user is in this state before treating it as worth a follow-up ticket. Does not block this deploy.

## 5. Boot safety — PASS

- No new SQLAlchemy models, no `Enum(PyEnum)` additions, no migration files in this batch (confirmed by commit-range diff stat).
- All new Pydantic models (`ScoreSeriesItem`, `ScoreSeriesPointOutput`) are plain `BaseModel` subclasses with no import-time side effects.
- All new module-level constants (`_ANCHOR_FOR_MILESTONE_TYPE_PREFIX`, `_ANCHOR_FOR_OBSERVATION_PREFIX`, `STALE_PROCESSING_THRESHOLD_MINUTES`, `logger = logging.getLogger(...)` in `notification_routes.py`) are inert literals/standard logger construction — nothing reachable from import or FastAPI lifespan that could crash-loop the web dyno.
- The stale-PROCESSING sweep (`sweep_stale_processing_weekly_summaries`/`_monthly_audits`) is correctly wired into each hourly cron's entry point (`generate_weekly_therapy_summaries`, confirmed at `app/tasks/weekly_therapy_summary.py:246-253`) and is itself wrapped in its own try/except so a sweep failure can't abort that tick's generation loop.
- `_collect_symptom_score_series`'s `datetime.utcnow() - timedelta(days=90)` cutoff is a SQLAlchemy filter pushed down to SQL (`SymptomScore.created_at >= cutoff_dt`), not a Python-side datetime comparison — this is **not** the same bug class as the CS-07 naive/aware `TypeError` (that bug was two Python `datetime` objects being compared directly in application code); confirmed this new code cannot hit the same failure mode.
- Checklist's own boot-import check (`app/tests/conftest.py` env bootstrap, all 5 detectors + 2 generators + `notification_routes` imported and registered cleanly) is consistent with what the diffs show — no reason to doubt it.

---

## Additional verification beyond the five focus points

- **CS-06 bookkeeping regression check:** the `main_page_body.dart` diff removes the old unconditional `await cubit.showInsight(insight.id)` call from the bottom-sheet branch. I verified this is *not* a lost side-effect — `RecoveryMomentSheet.show()` and `PatternInsightSheet.show()` (both in `4fea945`) each independently call `cubit.showInsight(insight.id)` and `cubit.recordBottomSheetShown()` internally (grepped and confirmed), so the dedup/analytics bookkeeping the old code performed is preserved, just relocated into the renderers as the commit message claims.
- **CS-01 (Main → Mood Trend sheet) and CS-08 (Custom interval field):** file-scope-contained (`symptom_management_sheet.dart`, `symptom_presets.dart`, `therapy_frequency_selector.dart`), no API contract or model changes — confirmed out of scope for cross-layer risk, matches the spec's own Low-risk rating.

## Findings summary

| # | Severity | Area | Finding |
|---|---|---|---|
| 1 | Low | CS-07 / monthly free-tier | A free user with a pre-existing FAILED/stale-PROCESSING monthly row from a prior premium period can see that `processing_status` echoed inside an otherwise-correctly-locked card envelope. Pre-existing behavior, not a regression from this batch. No action required before deploy; worth a prod data check if it recurs in a support report. |
| 2 | Low | Documentation | This review's own file lives at the shared `Heroku/docs/` level per the task instruction — same location convention already established by `MSV33_Fix1_CS06_reminder_checklist.md`; noting only so it's not mistaken for stray placement. |

**No Critical or High findings.** Nothing here blocks deployment.

## Deploy-order recommendation

- **Either order is safe** (see §2). Backend-first remains the recommended default per house convention and is what the spec's suggested execution order (§"Suggested execution order") implies, but this batch's additive/tolerant design means a Codemagic build shipping before the operator runs `git push heroku main` + verifies would not break anything, and vice versa.
- **Standard sequencing still applies:** deploy backend, verify (no migration to run — this batch adds none), then push frontend. Rollback is a plain revert on either side independently, since neither side depends on the other having landed.
- **Recommend `qa-testing` run before deploy** per CLAUDE.md's mandatory pre-deployment gate (not run as part of this review — this review was contract-focused only). Backend commit messages report 5362/5392 passing (30 pre-existing failures, none touching changed files); frontend commit messages report per-suite green runs but no consolidated full-suite number was quoted in the commits I reviewed — worth confirming with `qa-testing` before push.
