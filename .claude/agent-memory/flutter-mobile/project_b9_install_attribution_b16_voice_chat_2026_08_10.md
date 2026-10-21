---
name: project-b9-install-attribution-b16-voice-chat-2026-08-10
description: B9 install-attribution implementation (Play Install Referrer) + B16 voice-chat regression check on build 2.0.76 (verdict + git divergence discovery)
metadata:
  type: project
---

## B9: Install attribution (Play Install Referrer)

Implemented `lib/services/install_attribution_service.dart` — Android Play
Install Referrer read once per install, `$set_once` person properties +
`app_install_attributed` event. Committed dev `498071b` (NOT pushed).

**Package note**: `android_play_install_referrer` (the package named in most
tutorials/older task specs) is DISCONTINUED on pub.dev — replaced by
`play_install_referrer` (same author, same API shape:
`PlayInstallReferrer.installReferrer` static getter returning
`ReferrerDetails.installReferrer` raw string). Always check
`pub.dev/api/packages/<name>` for `isDiscontinued`/`replacedBy` before
pinning a referrer/attribution package — this class of package churns.

**PostHog person-properties-without-identify() pattern**: to set `$set_once`
person properties on the pre-login ANONYMOUS distinct ID (e.g. at app
startup before any user is identified), do NOT try to call
`PostHogService.identify()` — it requires a `distinctId` and is meant for
post-auth. Instead, nest `r'$set_once': {...}` (raw string — `$` triggers
Dart interpolation otherwise) inside the `properties` map passed to the
existing `PostHogService.capture()` wrapper. PostHog merges these into
whatever the current distinct ID's person profile is; when the user later
authenticates and `identify()` is called, PostHog's own anonymous-ID merge
links the pre-login person properties into the identified profile. No new
PostHogService method was needed — this only works because `capture()`
already does a thin passthrough of `properties` to `Posthog().capture()`.

**Testability pattern for platform-gated code**: `Platform.isAndroid`/
`isIOS` are FALSE in `flutter test` (Dart VM host, e.g. Windows) — you
cannot exercise an `if (Platform.isAndroid) { ... }` branch's contents via
the public entrypoint from a test running on a non-Android host. Split the
platform dispatch (thin, untested) from the actual logic behind it
(injectable, fully tested): `resolveAndroidAttribution(Future<String?>
Function() fetchReferrerRaw)` is a `@visibleForTesting static` method the
platform switch delegates to, letting tests simulate success/exception/null
without a real platform channel or host-OS Android detection.

**One-time-flag ordering bug caught by tests**: an early `if (alreadyCaptured)
return;` INSIDE a `try { ... } finally { markCaptured() }` block still runs
the `finally` on the early-return path — silently re-marking (and, in a
different shape of bug, re-firing) on every launch after the first, not just
once. Fix: read-and-decide the skip BEFORE entering the try/finally that
does the actual work + marks the flag. A `verifyNever(() =>
prefs.markInstallAttributionCaptured())` test on the already-captured path
is what caught this — mocktail's failure message in that case ("Unexpected
calls: ...") lists ALL unverified calls on that mock, which was initially
confusing (looked like `hasCapturedInstallAttribution()` itself was the
problem) until tracing back to which mock the second `verifyNever` in the
test was actually checking.

## B16: Voice-chat "regression" on build 2.0.76 — NOT a regression

Report `analytics-reports/2026-08-10-voice-chat-assessment.md` (F6) flagged
zero `voice_chat_started` on build 2.0.76 (31 active users) as needing a
code check before trusting it as signal. Traced via git tags:
`app_2.0.75` = `b43de4c`, `app_2.0.76` = `5208340`. `git diff --stat
app_2.0.75 app_2.0.76` touches 38 files, NONE of which are
`reflect_tab_screen.dart` (the premium mic gate at `:619`),
`audio_chat_cubit.dart`, `realtime_api.dart`, or `connectivity_service.dart`
— the entire voice-chat entry path is byte-for-byte unchanged between the
two builds. **Verdict: noise from low n (16 active premium subs), not a
regression. No fix applied, per task instructions ("SPRAWDŹ" with no
regression found = document and close").**

**Git divergence discovered while doing this (not fixed, flagged only)**:
`origin/dev` HEAD is `5208340` (`app_2.0.76`, "Pre-release updates",
authored by the Codemagic bot). The local `dev` branch's un-pushed commit
chain does NOT build on top of that commit — `git merge-base app_2.0.76
HEAD` returns `7b5f8c5` (the PARENT of `5208340`), i.e. local history
branched at the same point `5208340` did, and diverged. `git
merge-base --is-ancestor app_2.0.76 HEAD` returns false. Concretely: local
`pubspec.yaml` still reads `2.0.75+148` and local git log never received
the version-bump/CHANGELOG commit that produced the `2.0.76` tag. This
means when the ~15+ locally-committed-not-pushed batches (see main project
MEMORY.md index) eventually get pushed, there will be a real (if likely
trivial — the divergent commit only touches `CHANGELOG.md` +
`pubspec.yaml`) merge/rebase to reconcile, not a fast-forward. Worth a
heads-up to `integration-devops` before the next push, not an immediate
action.
