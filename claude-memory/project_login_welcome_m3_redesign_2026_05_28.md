---
name: project_login_welcome_m3_redesign_2026_05_28
description: Welcome + Login/Auth screens redesigned to Material 3 per handoff (2026-05-28); key architectural decisions
metadata: 
  node_type: memory
  type: project
  originSessionId: 133c2d96-2800-4cde-92ac-81c284b7a49d
---

Welcome (`lib/screens/welcome/welcome_body.dart`) + Auth (`lib/screens/auth/auth_body.dart`) screens redesigned to M3 from the "MS Logowanie" Claude Design handoff on 2026-05-28. Status: PUSHED to `origin/dev` on 2026-05-29 (committed in `489389a "update"`, published via merge commit `0fb73ed`). analyze 0 errors, 27/27 widget tests pass. NOT yet deployed/released (pushing `dev` may trigger Codemagic auto-versioning per CLAUDE.md). Repo `mindsync-frontend` (remote `origin` = github.com/neuravec/mindsync-frontend), main dev branch = `dev`.

**Non-obvious decisions (approved by owner):**
- **Kept the combined login/signup screen** with its login↔signup toggle — did NOT split into separate routes. Only the visual language changed to M3; routing/AuthCubit/validators/terms flow untouched. Signup (index 1) adopts the same M3 fields/CTA for consistency (handoff only designed login).
- **Social login stays per-platform**: Apple on iOS, Google on Android — required by App Store guideline 4.8. Only restyled as M3 outlined button. Do NOT switch to Google-only.
- The old 3-controller rotation/slide/fade auth animation was replaced with a simpler crossfade.
- Welcome: removed the Lottie sailboat (`LottieAssets.welcomeWave`), added `Assets.generated.decorWaves` at ~10% opacity (deepOcean tint) at the bottom as the brand wave.

**M3 tokens used** (login surface = `MsColors.oceanMist` #F6FFFD; focus accent = `MsColors.coralPink` #FF9F8A FOCUS-ONLY; primary = `MsColors.deepOcean`). Field fill #F0F8F5, outline #C5D5D2, outlineMuted #6B8783 are local consts (not global tokens). New widget: `lib/screens/auth/widgets/m3_auth_field.dart` (floating-label `TextFormField`, coral focus border). Did NOT touch shared `lib/widgets/ms_input.dart`.

**l10n**: reused existing `auth_*` keys only (incl. pre-existing `auth_back`). No new ARB keys; existing localized copy kept (greeting via `auth_welcomeBack`/`auth_enjoyFeatures`, divider `auth_or` uppercased in widget) — handoff's exact Polish copy intentionally not adopted to avoid 7-language retranslation.

Handoff source: `UI_fixes/MS_Logowanie_handoff/ms-logowanie/project/{welcome-screen,login-screen,components}.jsx` (the `screenshots/*.png` are a stale older render — `.jsx` is authoritative; `uploads/*.png` show the pre-redesign app).
