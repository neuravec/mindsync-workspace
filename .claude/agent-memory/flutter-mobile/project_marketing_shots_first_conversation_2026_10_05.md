---
name: marketing-shots-first-conversation-2026-10-05
description: Marketing shots for first-conversation + Orca memory (2026-10-05); null-family button label fix, full-length capture trick, intro notice-below-fold finding
metadata:
  type: project
---

Added 5 marketing shots (untracked, as the whole test/marketing_shots folder is): first_conversation_intro/voice/open/recap, orca_memory, plus helper `marketing_text_patch.dart`.

Non-obvious findings:
- **Null-family button labels**: `FilledButton/OutlinedButton.styleFrom(textStyle: TextStyle(...))` is NOT merged with the theme (ButtonStyleButton = widget ?? theme ?? default), so `SubPrimaryButton` ("Start talking", "Continue"), the Orca-memory "Forget everything" button and similar render Ahem blocks in shots, and on a real device they use the PLATFORM font (SF Pro/Roboto), not Figtree. Registering Figtree under ~14 default family names (Roboto, sans-serif, Segoe UI, .SF UI Text...) does NOT help (`--use-test-fonts`, fallback disabled). Shot-side fix: `patchNullFontFamilies(tester)` in `beforeCapture` rewrites RenderParagraph root spans with null family. Real fix = explicit fontFamily in lib (flagged, not done).
- **Full-length capture**: set `tester.view.physicalSize` taller inside `beforeCapture` (captureShot re-settles and resets the view). The first `maxScrollExtent` is a lazy SliverList ESTIMATE (overshot ~130px). Trim to the last widget's real bottom in a second pass. render.py scales by width and crops from the bottom, so tall PNGs are fine.
- **Timer-started fade animations** (VoiceWordFadeText, VoiceOrb rings) need stepped `pump(50ms)` frames. One long pump leaves them at value 0.
- **UX finding (estimated, not device-verified)**: the intro's memory "notice at collection" (security M-5) overflows the 393x852 frame even with ZERO safe-area insets (34px with "Sunday anxiety" as the top area). On a real iPhone 15/16 (~93pt insets) it sits fully below the fold. FIXED 2026-10-05 in 4daf29f: the notice moved into the pinned footer above "Start talking", see [[intro-memory-notice-pinned-2026-10-05]]; the intro shot comment about "Sleep vs Sunday anxiety" is now outdated.

**Why:** the operator wants real app screens for Instagram. Pipeline: `python scripts/social/app-shots.py run --name <shot>`.
**How to apply:** reuse `marketing_text_patch.dart` for any shot with a CTA button; reuse the orca_memory full-length pattern for long lists. Related: [[posthog-integration]].
