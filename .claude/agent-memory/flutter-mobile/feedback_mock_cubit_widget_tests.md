---
name: feedback-mock-cubit-widget-tests
description: How to correctly mock Cubits in widget tests using bloc_test + mocktail
metadata:
  type: feedback
---

When writing widget tests for BlocBuilder-based widgets, `MockCubit<S>` from `bloc_test` requires:

1. Import `bloc_test/bloc_test.dart` in the widget test file (NOT just `flutter_bloc` or `mocktail`).
2. Stub ALL three: `state`, `stream`, and any public methods called by the widget.
3. Use a `_setUpMock()` helper pattern:

```dart
import 'package:bloc_test/bloc_test.dart';
// ...
class MockMyFeatureCubit extends MockCubit<MyFeatureState>
    implements MyFeatureCubit {}

void _setUpMock(MockMyFeatureCubit cubit, MyFeatureState state) {
  when(() => cubit.state).thenReturn(state);
  when(() => cubit.stream).thenAnswer((_) => Stream.value(state));
  when(() => cubit.loadData()).thenAnswer((_) async {});
  when(() => cubit.refresh()).thenAnswer((_) async {});
}
```

**Why:** Without the `bloc_test` import, `MockCubit` is not found. Without stubbing `.stream`, BlocBuilder throws at runtime. Without stubbing public methods, `_setUpMock` pattern fails because the mock doesn't know about them.

**How to apply:** Every new widget test that uses a MockCubit must follow this pattern. If you forget, the compiler error will say "Type 'MockCubit' not found."
