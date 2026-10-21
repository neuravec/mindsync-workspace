---
name: reference_frontend_ci_git_topology
description: Frontend git repo = mindsync-frontend/ (not root); dev=main branch→Codemagic→TestFlight; CI runs only pub get (commit codegen); synthetic-package:false l10n quirk
metadata: 
  node_type: memory
  type: reference
  originSessionId: a765e70c-b2e6-4699-8dfa-2b4c166df0cd
---

Topology + CI facts for the MindSync **frontend** (Flutter), needed for any commit/build/deploy work.

- **Git repo root = `mindsync-frontend/`** (the Flutter app is in `mindsync-frontend/mindsync_app/`). It is NOT the `Heroku/` container root — the harness/env reports "Is a git repository: false" because it inspects the root. Backend (`MindSync/`, FastAPI) is a SEPARATE repo + deploy (Heroku).
- **`dev` is the main branch** (`git remote show origin` → HEAD branch: dev; `origin/HEAD -> origin/dev`). All work flows through `dev`; recent features were pushed straight to `origin/dev`. Codemagic **auto-versions on push to `dev`** → TestFlight build in ~30 min. Codemagic also has a PR builder on `dev` PRs.
- **Codemagic build runs only `flutter pub get`** — NOT `flutter gen-l10n`, NOT `build_runner` (verified in codemagic.yaml). Therefore generated files MUST be committed current: `*.freezed.dart` / `*.g.dart` after model changes, and `lib/l10n/generated/*` after ARB changes. Do not rely on CI to regenerate them.
- **l10n: `synthetic-package: false`** → the generated `S` class lives committed in `lib/l10n/generated/` and is NOT auto-regenerated. Editing `*.arb` without running `flutter gen-l10n` leaves the generated class stale → "getter '…' isn't defined for the type 'S'" compile errors (e.g. `symptom_presets.dart`) that block ALL `flutter test` (verified: local `flutter test` does NOT auto-regenerate; it failed until `flutter gen-l10n` was run). Fix: `flutter gen-l10n`.
- **Deploy coupling:** frontend-only fixes ship INDEPENDENTLY of backend (no backend deploy → zero risk to current prod users on old apps). Conversely, old app versions stay live for WEEKS (store review 1-2 days + slow user updates), so any backend change must be backward-compatible (additive only: no removed/renamed/retyped fields the old app uses, no new required request fields, no tightened validation). "Wait for the frontend" is not a viable strategy.

Concurrent-session hazards in this single shared working tree: [[feedback_concurrent_session_git_hygiene]]. Codemagic UI setup details: [[reference_codemagic_setup]].
