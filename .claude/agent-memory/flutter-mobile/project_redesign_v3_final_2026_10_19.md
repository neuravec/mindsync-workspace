---
name: redesign-v3-final-2026-10-19
description: integration/redesign-v3-final (4654c19, 9989177, 1f57e4f pushed to origin only) - health check replay mask, recording logs without token/bodies, first-week reminder opt-in on MC v3 Main; open items and layout traps
metadata:
  type: project
---

Three commits on `integration/redesign-v3-final` (worktree mindsync-frontend-wt-integration-v3-final, base origin/integration/redesign-v3 56814cd), pushed to origin only. Builds on [[redesign-v3-security-round2]].

- HealthCheckSection is one PostHogMaskWidget (`maskKey`) in every state; HealthCheckResultCard too (`maskKey`), it paints the state in circle, banner and share pill.
- RecordingDebugLog: console print only in kDebugMode, buffer kept (the record-session app bar shows a bug icon "Debug logs" viewer in RELEASE builds, people can copy it), every entry redacted (Authorization, Bearer, JWT). DioClient: `failureLogLine` and `multipartRequestLogLine` (route template only), source-guard test scans log calls for headers/.data/.message.
- Reminder on Main: `McWeekCubit.setReminder(enabled, source)` -> PUT /first-week/reminder {"enabled": bool}, optimistic, permission via PushPermissionGateway (denied status = blocked, no dialog), `_pendingReminder` survives a load landing mid-save. Row `McWeekReminderRow` in the plan sheet; pop-out `McStepPopupData.onRemind`. `reminder_optin_result` now {result, source, enabled} for every sender (old Home row sends first_week_home); guard maps updated.
- Gentle tone: backend sends no step reminder (fails closed), so the row is Visibility(maintainSize) there (sheet height parity, H-1) and the pop-out has no button.

**Why:** release-blocking review items from the operator (2026-10-19).

**How to apply:**
- Open, not done: health check FLOW question views (score buttons) are still unmasked; the "Debug logs" bug icon ships to all users in release.
- M3 Switch with shrinkWrap is still 60x40; measure copy with a TextPainter in a temporary `@Tags(['marketing'])` test that loads Figtree before tuning row paddings.
- A `for d in ...; flutter test` loop over 4 big dirs passes 600 s: run at most 3 per command.
