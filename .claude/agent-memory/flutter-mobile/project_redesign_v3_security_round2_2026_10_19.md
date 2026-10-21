---
name: redesign-v3-security-round2
description: Redesign v3 integration security round 2 fixes (2026-10-19, pushed 56814cd on integration/redesign-v3) - KE 409 ideas_paused silent reload, After card progress mask, first-week seen store positions + removal, DioClient debug-only log; open items for other owners
metadata:
  type: project
---

Four FE commits on integration/redesign-v3 (77e1bf6, 3194e13, 1d580c5, 56814cd), pushed to origin only.

- KE idea act 409 (`ideas_paused`, crisis window): no event at all, no saveFailedTick, optimistic idea reverted, quiet reload (`KeSheetCubit.load(quiet: true, track: false)`; KE3 also `_reloadIdea()` that only takes over idea + next session date). KE3 `_supportRow` now uses `context.select` on KeSheetCubit (it was `read`, so a sheet reload never rebuilt KE3).
- After card `TherapyProgressPanel`: line + point labels in one `PostHogMaskWidget` (`chartMaskKey`, `lineKey`); locked placeholder stays unmasked.
- `McWeekSeenStore` now stores 1-based positions (`Set<int>`); McWeekCubit converts at the boundary with the current plan, in-memory logic still keys. Old key-format entry reads as null (silent re-seed). Removal: sign-out via `resetFirstWeekForAccountChange` (uid read synchronously before Firebase sign-out), deletion via `AccountDeviceErasure` (deletion's reset runs after `user.delete()`, currentUser is null there).
- `DioClient._handleError`: one kDebugMode line with `DioClient.routeTemplate(uri)` (digit segments to `{id}`, v1 kept). Test overrides the global `debugPrint` and restores it.

**Why:** security round 2 findings; card-type properties to PostHog/Firebase left to operator + lawyer (M-3 bundle).

**How to apply:** open items not mine: android:allowBackup/dataExtractionRules in AndroidManifest (integration-devops), backend 422 handler echoing exc.body (backend-api), and RecordingDebugLog still debugPrints multipart request headers (Bearer token) and session-recording error bodies in release (same class, unfixed). Edit tool keeps CRLF; Write writes LF, convert with Python bytes. See [[redesign-v3-review-fixes]].
