---
name: shared-widget-full-screen-text-editor
description: FullScreenTextEditor — hub-and-spoke modal text editor used to prevent keyboard crowding on long-form text fields
metadata:
  type: project
---

# FullScreenTextEditor

File: `lib/widgets/full_screen_text_editor.dart`

## Purpose

Opens a full-screen Scaffold for text editing so the keyboard never crowds inline
text fields on complex scrollable screens. Pattern: tappable display field → push →
user edits → Confirm pops with new text (or X discards).

## API

```dart
FullScreenTextEditor.open(
  context,
  title: 'Section title',       // shown in top bar next to X
  initialText: controller.text,
  hintText: 'Optional hint',
  maxLength: 300,                // null = unlimited; shows counter when set
  footerBuilder: (text) => [...],// widgets inserted above the Confirm button
)
// returns Future<String?> — null means user dismissed (X); non-null means Confirm
```

## Key implementation details

- `maxLines: null, expands: true` — TextField fills the Expanded area above footer
- `buildCounter` returns null (custom counter shown below the field instead)
- Auto-focuses the field via `WidgetsBinding.instance.addPostFrameCallback` in initState
- `MaxLengthEnforcement.enforced` prevents paste-overflow
- `footerBuilder` receives the live text value — suitable for reactive widgets like CrisisBanner
- Background: `MsColors.oceanMist`; Confirm button: `coralPink` bg + `deepOcean` text
- L10n keys used: `S.of(context).common_cancel` (tooltip), `S.of(context).common_confirm` (button)

## Usage pattern in onboarding_journey_view.dart

```dart
Widget _tapToEditField({required String title, required TextEditingController controller, required String hint, required int maxLength}) {
  final value = controller.text.trim();
  return GestureDetector(
    onTap: () async {
      final result = await FullScreenTextEditor.open(context, title: title, initialText: controller.text, hintText: hint, maxLength: maxLength,
        footerBuilder: (text) => [CrisisBanner(visible: _crisisRegex.hasMatch(text))]);
      if (result != null) { controller.text = result; setState(() {}); }
    },
    child: Container(/* tappable pill display */),
  );
}
```

Setting `controller.text = result` triggers the existing `_onTextChanged` listener — crisis detection still works.

## Related

- [[shared-widget-ms-tab-top-bar]]
- Used in: `lib/screens/therapy_onboarding/views/onboarding_journey_view.dart` (frustration free-text + goals fields)
