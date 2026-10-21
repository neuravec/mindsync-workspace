# Flutter Mobile Patterns

## DioClient 404 Handling

`DioClient._handleError` wraps `DioException` as `Exception('HTTP error: 404 ...')`.
When catching 404 in API managers:
```dart
} catch (e) {
  final msg = e.toString();
  if (msg.contains('HTTP error: 404')) return null;
  rethrow;
}
```
The `on DioException` branch won't fire because DioClient re-throws as plain Exception.

## fl_chart 0.68.0 API

**LineChart animation**: `duration:` and `curve:` (ImplicitlyAnimatedWidget params).
NOT `swapAnimationDuration`/`swapAnimationCurve` (those are BarChart-only aliases).
```dart
LineChart(duration: const Duration(milliseconds: 600), curve: Curves.easeInOutCubic, data)
BarChart(data, swapAnimationDuration: ..., swapAnimationCurve: ...)
```
**clamp() returns num not double**: use `raw < 1 ? 1.0 : raw` not `.clamp(1, 999)`.

## EmotionColors Utility

`lib/screens/main_page/charts/emotion_colors.dart`:
- `getColor(emotion)` — color for any emotion name (normalizes via `_normalize`)
- `getEmoji(emotion)` — emoji string
- `getDisplayName(emotion)` — capitalized key
- `getLabelWithEmoji(emotion)` — "Joy 😊" style for legends
- `getRandomColor(index)` — palette for non-emotion-keyed data

## TrialPopupManager Flow (Android)

1. New user, `subscriptionIsActive: true, !hadTrial` → `FreeTrialWelcomePopup`
2. Build-time block: `!subscriptionIsActive && !hadTrial` → `TrialStartPopup.showBlocking()`
3. `!subscriptionIsActive && !hadTrial`, not blocked → `TrialStartPopup.show()`
4. After purchase: `subscriptionIsActive: true, hadTrial: true` → `FreeTrialBanner`
5. Paid plan, 1-6 days left → `PaidPlanCounterBanner` (amber, "Renew" button)

## UserInfo.hadTrial Semantics

- `hadTrial: false` = brand new user, never started trial
- `hadTrial: true` = user has initiated/is in/has completed trial
- Starter-pack buyers: `hadTrial: true` AND `subscriptionIsActive: true` AND `subscriptionEndDate != null`

## Code Review Checklist

1. `mounted` guard required in every `Future.delayed` callback before `context.*`
2. `postFrameCallback` inside `BlocBuilder.build()` fires on every rebuild — guard with static flag
3. `inDays` truncates — use `(duration.inSeconds / 86400).ceil()` for day counters
4. Double-popup risk: guard `_maybeShowPopups` with early-return when `_isAndroidTrialExpired` is true
5. BuildContext across async gaps: capture `Navigator.of(context)` before `await`

## Dart Patterns

**Private static methods same-file access:**
- Private static methods on private class (e.g. `_TrialStartPopupState._buildStep`) are library-private
- Accessible anywhere in same file: `_TrialStartPopupState._buildStep(...)`

**Freezed 3.x sealed switch:**
```dart
// Use switch, not .when()
switch (state) {
  LoadedState(:final data) => Widget(data),
  LoadingState() => CircularProgressIndicator(),
  ErrorState(:final message) => Text(message),
}
```

## Dependency Notes

- `intl` must be `^0.19.0` — Flutter SDK pins to 0.19.0 via flutter_localizations
- Use `.withValues(alpha: x)` not `.withOpacity(x)` — latter is deprecated in Flutter
