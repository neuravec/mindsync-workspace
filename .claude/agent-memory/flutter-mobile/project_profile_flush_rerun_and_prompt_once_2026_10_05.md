---
name: project-profile-flush-rerun-and-prompt-once-2026-10-05
description: fix/first-conversation-voice-v2-fe (NOT pushed) - 1277c02 re-run profile wipe + prompt once, 71947ef stale wow test, fc74a5e calm Premium voice gate + Reflect limit; 185d62a (paywall-return branch) purchase pops back + close ends open thread + sticky pause
metadata:
  type: project
---

Commit 1277c02 on `fix/first-conversation-voice-v2-fe` (frontend repo, from origin/dev 113543f), NOT pushed (2026-10-05).

Contracts later work must keep:
- `UsersManager.flushPendingProfile` no-JSON branch is CREATE-ONLY (`_upsertProfile(updateExisting: false)`): a failed POST never falls back to PUT. Reset onboarding re-runs the consent step with the sign-up JSON already cleared, so that branch runs while the row exists.
- Flush bodies drop null keys (`_profileBodyWithoutNulls`). `Profile.toJson()` ALWAYS emits `full_name/pronouns/gender/age_band` (only `currently_in_therapy` is includeIfNull:false), and backend PUT /users/profile is `exclude_unset`: any PUT built from a `Profile` with nulls erases saved values. Account screen (`account_body.dart` Save) still sends a full Profile: a cleared name goes out as `"full_name": ""`, never null; gender/pronouns/age band are resent as held (no UI to clear them).
- Backend POST /users/profile "idempotent" change (backend-api, parallel) must stay create-if-missing; if it ever merges fields into an existing row, the no-JSON branch's Firebase displayName would overwrite a chosen name again.
- `VoiceSessionOptions.sendSystemMessageItem` (default true). First conversation sets false (start, reconnect, renewal): prompt only in `session.update` instructions + key mint. Plain Reflect voice (`audio_chat_screen.dart`, the only other `initialize` caller) unchanged.

Gotchas seen:
- `.fvm/flutter_sdk` is still Flutter 3.27 / Dart 3.6 and fails `pub get` (pubspec needs SDK >=3.11). Use system `flutter` (C:\Users\mikol\flutter, 3.41.1) for test/analyze.
- Pre-existing red test, not from this change: `test/screens/wow/wow_screen_test.dart:357` still expects the text subtitle "First conversation · 1 of 3 · This week" that 0704af6 (no phases) removed.

fc74a5e (2026-10-05), first conversation for a Free account past its exemption (exemption is per account, 48 h from first claim; re-run always gets the scripted conversation since BE 5ee8701):
- `session_data` 403 = premium gate (`FirstConversationCubit.isGateRefusal`: 403 and detail != "Not authenticated"; invalid token is a 401). No reconnect: text, `voiceLocked`, inline `FirstConversationVoicePremiumNote` + "See Premium". mode_switched/started carry `premium_required`. The realtime mint has no premium gate.
- `/message` 403 = monthly limit: `limitReached`, `ReflectLimitPanel` (new params `entryPoint`, `onSeePlans`, `showCta`), Finish still ends. Client never logs `reflect_limit_hit` here (backend owns it; the Reflect tab still logs it client-side too: pre-existing double emit, flagged).
- Plans entries go through `FirstConversationCubit.openPaywall`, given by WowScreen (`_openConversationPaywall`, standard `/subscription?trigger=` route). WowScreen's preloaded SubscriptionCubit listens to the purchase stream all conversation long and every listener processes every purchase, so it calls `suspendPurchaseUpdates()`/`resumePurchaseUpdates()` around the push. Never open a second paywall over /wow without that.
- Plans entries hidden after a text crisis reply (H-1). A purchase there ends on Premium welcome then Home (standard paywall), the recap is not shown.
- `firstConversationCubitFactory` now takes `(profile, onStarting, openPaywall)`.
- 185d62a on `fix/first-conversation-paywall-return` (worktree `mindsync-frontend-wt-paywall`, NOT pushed), integration-devops F1/F2: `pushReplacement` (paywall -> Premium welcome) never completes the awaited `context.push` on go_router 14.6, so the conversation's paywall uses `subscriptionRouteWithTrigger(..., returnAfterPurchase: true)` (`after_purchase=back`) and pops back after a purchase (other entry points keep the welcome). `FirstConversationCubit.close()` ends an open thread with user turns (`/end` fire-and-forget, `first_conversation_ended` reason `screen_closed`; End is reason `user`). SubscriptionCubit pause is sticky (a load finishing while paused listens only on resume).
- Widget-test gotcha: after a go_router pop/go, pump ~1 s before tapping under the old route or verifying dispose effects; `pumpUntilFound` returns mid-transition.

**Why:** prod showed NULL full_name/gender on re-run tester accounts; the duplicate prompt was billed on every realtime response.
**How to apply:** never PUT a whole `Profile` from a background/self-heal path; build bodies without nulls. Related: [[project-first-voice-conversation-fe1]], [[feedback-realtime-function-call-no-name]].
