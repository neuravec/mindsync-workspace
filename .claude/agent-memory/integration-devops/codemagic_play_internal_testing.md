---
name: codemagic-play-internal-testing
description: Google Play internal testing track now auto-rolls-out (submit_as_draft flipped false) 2026-07-03 — TestFlight-parity for Android beta testing
metadata:
  type: project
---

`mindsync-frontend/codemagic.yaml` `app-release` workflow's `publishing.google_play.submit_as_draft` was flipped from `true` to `false` on 2026-07-03 (commit `c26353c` on `dev`, pushed to `origin/dev`).

**Why:** User wants to beta-test Android like iOS TestFlight, via Google Play Internal testing. Previously every build landed as a draft requiring manual rollout in Play Console — the internal track was stuck at an old version code (55) while the app's latest was ~530, because nobody was manually promoting drafts. Play Console internal-testing track + tester list ("MindSync Internal") were already verified Active before the flip.

**How to apply:** From this point forward, every successful `app-release` build auto-delivers to Play internal testing — no manual "roll out" click needed in Play Console. If asked to debug "testers aren't getting new Android builds," check Codemagic build success first, not the draft-rollout step (it no longer exists in the flow).

**Safety verified before flip (still valid — re-check if `codemagic.yaml` triggering design ever changes):**
- `app-release` has **no** `triggering:` block (dispatch-only) — confirmed by grep, only `pr-builder` and `app-create-version` have `triggering:`. This is the documented anti-duplicate-build design (see comment block ~lines 389-419 in codemagic.yaml): API-trigger from `app-create-version`'s "Auto-trigger app-release via Codemagic API" step checks for an existing build for the tag before POSTing, so only one `app-release` build fires per release tag → no version-code collision risk from concurrent builds.
- Android build number is fetched fresh from Play itself and incremented (`google-play get-latest-build-number` + 1, codemagic.yaml ~line 442) — strictly monotonic version codes regardless of draft/non-draft.
- Google Play internal testing does not require release notes/changelog as mandatory, and does not go through Google review — non-draft submit publishes immediately to the tester list.

See [[reference_codemagic_setup]] and [[reference_frontend_ci_git_topology]] for the surrounding CI/CD context (shared git tree, dev = main branch, humm version-bump flow).
