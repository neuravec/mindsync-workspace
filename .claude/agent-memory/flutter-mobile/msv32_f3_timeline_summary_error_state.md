---
name: msv32-f3-timeline-summary-error-state
description: MSV3.2 Fix.1 F3 — weekly/monthly summary in-card generation-error state + retry, ApiException pattern, widget-test GetIt gotcha
metadata:
  type: project
---

## What shipped (2026-07-17, commit 087e8f7 on `msv32-f3-timeline`, NOT pushed — worktree `.worktrees/f3`)

CS-21 FE part. Backend (Phase A2) wraps `/weekly-summaries/generate|retry` and
`/monthly-audits/generate|retry` prep-phase failures in a structured envelope:
`{"detail": {"error_code", "message", "retryable", "summary_id"|"audit_id"}}`
instead of a raw bodyless 500. FE now surfaces this as an in-card friendly
error with working retry in two places, never a full-screen error/toast:

1. **Empty-state "Generate Now" CTA** (`TherapyTabGenerateFailedState`, new
   state) — friendly banner (mapped from `error_code`, generic fallback for
   network/unrecognized errors) above the SAME "Generate now" button, reused
   as retry.
2. **An already-visible FAILED weekly/monthly card** in the loaded timeline —
   `_SummaryRetryFailedRow` (local StatefulWidget, mirrors the existing
   `_RealizationUntagButton` nested-GestureDetector-inside-tappable-card
   pattern) replaces the old plain "Processing failed" text for these two
   types only; other FAILED card types untouched.

## `ApiException` — new reusable pattern for structured backend errors

`DioClient._handleError` previously did `throw Exception('HTTP error: $code $msg')`,
discarding `err.response?.data` entirely — no caller could ever read a
backend error envelope's `error_code`/extra fields, only the stringified
message. Added `lib/api/api_exception.dart`:
```dart
class ApiException implements Exception {
  final int? statusCode;
  final dynamic responseData;
  Map<String, dynamic>? get errorDetail { // parses {"detail": {...}} }
  String toString() => _message; // EXACT same "HTTP error: $code $msg" format
}
```
`_handleError` now throws this instead. **Purely additive** — `toString()`
format is byte-identical to before, so every existing `e.toString().contains('404')`
/`'403'` check across the codebase (`api_error_utils.dart`,
`weekly_summary_manager.dart`, `monthly_audit_manager.dart`,
`therapy_context_manager.dart`) keeps working unchanged. Use `e is ApiException`
+ `.errorDetail` going forward whenever a manager/cubit needs more than a
status code from a failure (e.g. any other `*_failed` envelope pattern).

## Retry-endpoint-vs-generate-endpoint nuance (backend code-trace finding)

`POST /weekly-summaries/generate` (and monthly's equivalent) is **NOT**
idempotent-safe as a retry after a `*_generation_failed` envelope (row
created, `summary_id` present): it computes a NEW window from
`latest_summary.data_window_end` regardless of whether that latest row is
FAILED, and creates ANOTHER row — repeated taps would accumulate multiple
FAILED rows with shifting windows instead of retrying the same one. Only
`*_prepare_failed` (no row created) is safe to retry via `/generate` again.
`TherapyTabCubit.generateForFilter` now branches on this: if the current
state is `TherapyTabGenerateFailedState` for the same filter with a non-null
`retryRowId`, it calls `/retry/{id}`; otherwise `/generate`. Same asymmetry
exists for monthly (`monthly_audits.py`) — verify before assuming any
`/generate` endpoint elsewhere in this app is retry-safe.

## Backend timeline listing asymmetry (crud.py, read-only finding, not fixed)

`_fetch_monthly_audits_for_timeline` explicitly excludes
`processing_status == FAILED` rows ("per spec") — a failed monthly audit
NEVER appears as a card in the timeline, only surfaces via the live
exception at generation time. `_fetch_weekly_summaries_for_timeline` has NO
such filter — a FAILED weekly summary DOES appear as a card. This means the
"already-visible FAILED card retry" scenario is reachable for weekly but
provably unreachable for monthly today; the FE handles both symmetrically
anyway (defensive/future-proof), but don't be surprised if a FAILED
monthly_audit card is never observed in manual QA — that's expected.

## Widget-test gotcha: screen whose root reads its Cubit via `sl<>()`, not `context.read`

`TherapyTabScreen.build()` does `BlocProvider.value(value: sl<TherapyTabCubit>(), ...)`
— the mock must be registered into GetIt (`sl.registerSingleton<TherapyTabCubit>(mock)`,
NOT `registerFactory`, since `_TimelineList`'s `RefreshIndicator.onRefresh` calls
`sl<TherapyTabCubit>()` a SECOND time and both call sites must resolve the
same mock instance) — a `BlocProvider.value` in the test's own widget tree
does nothing here. Closest existing precedent:
`test/screens/main_tab/widgets/session_setup_screen_test.dart`. Also needed:
mock `SharedPreferencesManager` via `sl.registerFactory` (screen's `initState`
calls `hasSeenSwipeDeleteHint()`). `SvgPicture.asset` needs no special
handling in this repo's test env (real asset bundle, `flutter_svg` parses
raw bytes at test time) — confirmed by running `reflect_chat_input_test.dart`.
`Lottie.asset` is fine too as long as you avoid `pumpAndSettle()` on states
that render one (it loops forever) — use bounded `tester.pump(duration)`
instead, per `test/widgets/voice_error_card_test.dart`'s convention.

## Bug this widget test caught (would have shipped broken otherwise)

First cut gated the empty-state error banner on `generateErrorCode != null`.
That's wrong: a network/unrecognized error has `errorCode == null` but is
STILL a failure that must show the generic-fallback banner. Widget test
"an unrecognized/network error shows the generic fallback copy" failed
(found 0 widgets) and caught it immediately. Fixed by adding a separate
`isGenerateFailed` bool to `_EmptyState`, independent of the nullable
`generateErrorCode` used only for message *mapping*. Lesson: when a nullable
field doubles as both "is there a value" and "should the value's own null
case still show something," those are two different booleans — don't
collapse them into one null-check.

## Windows build_runner + git core.autocrlf gotcha (broadly applicable, not F3-specific)

Running `flutter pub run build_runner build --delete-conflicting-outputs`
regenerates ALL ~700+ managed `.freezed.dart`/`.g.dart` files project-wide
(not just ones touched), and with `core.autocrlf=true` this makes
`git status` show HUNDREDS of unrelated files as modified — but the diffs
are 100% line-ending noise (`git diff --ignore-all-space --stat -- <path>`
shows nothing). **Always verify with `--ignore-all-space` before staging**
after any build_runner run in this repo, and `git checkout --` the
line-ending-only files before committing — never trust `git status` alone
to mean "these are my changes." A `git checkout --` across ~200+ files can
time out (>2min) and leave a stale `.git/worktrees/<name>/index.lock`; if no
other git process is actually running (check `tasklist`/`Get-Process git`),
it's safe to `rm` that lock — it's scoped to that one worktree's own index,
not shared with sibling worktrees.
