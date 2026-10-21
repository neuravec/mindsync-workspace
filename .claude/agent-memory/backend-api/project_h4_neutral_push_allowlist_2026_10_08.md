---
name: project_h4_neutral_push_allowlist_2026_10_08
description: H-4 push privacy (first-week-home WP-0): send-time neutral allowlist, push_title column is in-app copy now, notification_logs.title = template key, Write tool turns unicode escapes into literal chars
metadata:
  type: project
---

Commit `280c478` on branch `fw/be0-push` (worktree MindSync-wt-fw-be0-push, base `feat/first-week-home` 0c7d275), NOT pushed as of 2026-10-08. No migration.

Design decisions that are not obvious from the code:
- The lock-screen copy is resolved at SEND time (`deliver_due_moments` -> `send_templated_push`), not at moment creation. Reason: the Flutter in-app moment sheet renders `pushTitle`/`pushBody` from GET /moments/upcoming (main_page_body.dart, moment_deep_link_screen.dart), so overwriting the row would have killed the AI in-app copy. `NotificationMoment.push_title/push_body` therefore now mean "in-app copy"; FCM never sees them. Also covers PENDING rows created before deploy.
- `notification_logs.title` stores the push_copy template key, `body` is NULL. Chosen over a new column to avoid a migration. Old rows keep text until the 30-day cleanup.
- English copy = brand-voice-manager's COPY.md section 11 verbatim (29 keys, checked by script against the markdown table). Other 6 locales were my translations; non-EN strings avoid the feature name "Reflect" (localized differently per ARB) and gendered forms (PL/FR/ES).
- THERAPY_PREP fires at T-24h and T-3h; delivery picks `therapy_prep_same_day` when dedup_key ends with ":T-3h".
- AST guard test fails if anything outside notification_service calls `send_fcm_to_all_user_tokens`/`send_fcm_message_v1`; new push paths must use `send_templated_push` plus a new PUSH_COPY key.

Residuals flagged to lead: moment rows and PostSessionNudge still store AI text in plaintext (M-5 encryption); Flutter foreground `body.hashCode` id collides when neutral bodies repeat; local AndroidNotificationDetails visibility is flutter-mobile's.

Tool gotcha: the Write tool and heredoc tool inputs convert `—`-style escapes into the literal character. To keep a file free of U+2014/U+2013, write escapes with `chr(92) + 'u2014'` from a Python script, then grep with `grep -cP "[\x{2013}\x{2014}]"`.

Related: [[notification_service_patterns]], [[offline-verification]]
