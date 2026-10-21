---
name: intl version pinning policy
description: Flutter intl package pinning depends on the Flutter SDK version. The 0.19.0 lock applied to Flutter 3.27. Flutter 3.41 (Xcode 26 migration, 2026-04-30) requires intl 0.20.x. Always match flutter_localizations.
type: feedback
originSessionId: 7cc72544-c49f-4ef3-b741-6a113123dcde
---
Flutter `intl` package version is dictated by the Flutter SDK's `flutter_localizations` package. Do not bump or downgrade `intl` outside the version that the active Flutter SDK pins.

**Why:** This has burned us twice. (1) On Flutter 3.27.0 (fvm-pinned), `flutter_localizations` pinned `intl 0.19.0` exactly — agents running system Flutter (which pinned a different version) "fixed" the constraint and broke `pub get`. (2) During the Xcode 26 / Flutter 3.41.1 migration on 2026-04-30, the rule had to be retired: Flutter 3.41 ships `intl 0.20.2`, and keeping `^0.19.0` would have failed `pub get`. The lesson: pinning is FLOOR-DEPENDENT, not absolute.

**How to apply:**
- The current correct pin is `intl: ^0.20.2` (Flutter 3.41.1, since 2026-04-30).
- An inline comment in `mindsync-frontend/mindsync_app/pubspec.yaml` next to the `intl:` line documents this — trust the comment over outdated memory.
- When bumping the Flutter SDK in `.fvmrc`, immediately verify the intl pin matches what `flutter pub deps` resolves; update both pubspec.yaml and the inline comment.
- Always use the project's pinned Flutter (`fvm flutter` on macOS, system Flutter 3.41.1 matches on Windows). Never bump intl to satisfy a system-installed Flutter that disagrees with `.fvmrc`.
