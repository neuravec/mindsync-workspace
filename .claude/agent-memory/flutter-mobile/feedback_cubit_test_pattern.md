---
name: feedback-cubit-test-pattern
description: Use bloc_test blocTest helper for cubit tests — manual stream.listen misses synchronous emissions
metadata:
  type: feedback
---

Always use `bloc_test`'s `blocTest<CubitType, StateType>()` for cubit state transition tests. DO NOT use manual `stream.listen` + `await cubit.method()` patterns.

**Why:** Cubit's `emit()` fires synchronously, but Dart streams deliver events asynchronously. A stream listener set up before calling the method may still miss the first `emit(loading)` due to event loop timing. `blocTest` wraps this correctly with `seed:`, `act:`, `expect:`, and `verify:` hooks.

**How to apply:** Every new cubit test file should `import 'package:bloc_test/bloc_test.dart';` and use `blocTest(...)` for state sequence assertions. For GetIt-dependent cubits (field initializer calls `sl()`), register a stub singleton in `setUp()` and call `await GetIt.instance.reset()` in `tearDown()`. Use `seed:` to set initial state instead of calling a previous method in act.

**GetIt stub registration pattern:**
```dart
setUp(() async {
  SharedPreferences.setMockInitialValues({});
  manager = MockManager();
  final sl = GetIt.instance;
  if (!sl.isRegistered<Manager>()) {
    sl.registerSingleton<Manager>(manager);
  }
});
tearDown(() async => GetIt.instance.reset());
```

Related: [[feedback-testing]]
