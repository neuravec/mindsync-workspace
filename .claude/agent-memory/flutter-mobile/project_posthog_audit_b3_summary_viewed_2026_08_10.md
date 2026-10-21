---
name: project-posthog-audit-b3-summary-viewed-2026-08-10
description: B3 task (PostHog audit) — Timeline summary_viewed read-receipt, resumed after a session pad; found already ~complete when picked back up
metadata:
  type: project
---

Resumed a pad-interrupted session's work on B3 from `analytics-reports/2026-08-10-posthog-audit-taskplan.md`:
client-side `summary_viewed` event pairing with the backend's `weekly_summary_generated`/
`monthly_audit_generated` (data-analytics, commit e16f657).

On review, the interrupted session's working tree was already functionally complete and
well-tested (30 new tests, all passing) — verification-only, no code gaps to fill:
- `AnalyticsEvents.logSummaryViewed` + closed-vocabulary constants (period_type/period_start/source)
  in `lib/core/analytics/analytics_events.dart`.
- `TherapyTabCubit.trackSummaryViewed`/`resetSummaryViewedGuard` replaced the OLD
  `trackSummaryViewed(summaryType, summaryId)`/`trackMonthlyAuditViewed` methods, which were
  dead code (defined, zero call sites) — confirmed via grep before treating the replacement as safe.
- `viewSource` param threaded through `WeeklySummaryWidget`/`MonthlyAuditWidget`/
  `TherapyCardDetailScreen`, defaulting to `detail_screen`; Timeline list passes `timeline_list`,
  the two deep-link GoRoutes in `ms_routes.dart` pass `deep_link`.
- Guard reset wired via `_TherapyTabBodyState` subscribing to `sl<MainNavCubit>().stream` and
  calling `resetSummaryViewedGuard()` on tab-away (best-effort try/catch — degrades gracefully
  when `MainNavCubit` isn't registered, e.g. isolated widget tests).

**Committed**: dev branch, commit `5735309`, 13 files (7 lib + 6 test), NOT pushed.

**Found unrelated in working tree, correctly left unstaged**:
`lib/api/models/workspace/triage_proposal_model.freezed.dart` was modified (doc-comment
whitespace/em-dash cleanup) but its non-generated sibling `triage_proposal_model.dart` showed
*zero* diff vs HEAD — meaning the source's comment change was already committed previously and
only the generated file was stale/out-of-sync in this working tree. Unrelated to B3; left
uncommitted and reported rather than bundled in. Lesson: when a `.freezed.dart` diff shows up
during a stage-only-my-files pass, always diff its non-generated source sibling too — if the
source has no diff, the freezed file is stale build_runner output from *some other* prior change,
not a byproduct of the current one.

Also present but out of scope (other agents' files, left alone):
`.claude/agent-memory/data-analytics/*` (modified + new), `.claude/agent-memory/growth-analyst/`.
