---
name: test-baseline-pytest-history
description: Full chronological history of `python -m pytest app/tests/ -q` full-suite failure counts/composition, used to distinguish a real regression from known pre-existing baseline or transient SQLite-leftover-state flakiness
metadata:
  type: project
---

## How to use this file
Before treating a red full-suite test as your regression, check whether its
name/file already appears below. If the CURRENT run's failure list matches a
past composition (same test names), it's baseline, not a regression — confirm
quickly via `git stash` + run just that test in isolation, don't re-diagnose
from scratch. Composition drifts day to day (transient SQLite `test_temp.db`
leftover-state/order sensitivity is a real, recurring, non-regression noise
source — same handful of files repeatedly implicated: `test_consent.py`,
`test_workspace_fix1_a1_migration.py`, `test_timeline.py`, `test_notification_
worker_registration.py`) — always re-run rather than trust any single historical
number as gospel. The "core" baseline composition has been stable since
2026-08-17 at: custom-therapy-sessions×2, first-impression×1,
notification-improvements×4, onboarding-v2×1, symptom-suggestions×1,
therapy-frequency×5 (TherapyScheduleUpdate validation-drift group), voice-fixes×5,
walkthrough×1, plus therapy_tracking_fix1_a12's date-relative flake×1 = 21.

## Chronological log (most recent first)
- **2026-10-05 (profile re-run fix, commit `0f74b96`, base origin/main d1d93d0)**: 9
  failed + 7171 passed, run as 4 file groups (suite now exceeds a 10-min foreground
  call). Baseline shrank to 9: first-impression x1, notification-improvements x4,
  onboarding-v2 x1 (`TestResetTherapyOnboarding::test_preserves_therapy_data`,
  confirmed failing on origin/main without the change), symptom-suggestions x1,
  therapy-frequency x1 (`test_year_boundary_dec_to_jan_known_limitation`),
  walkthrough x1.
- **2026-09-02 (MSV3.11 CS-10, commit `5f7211b`)**: 22 failed + 5539 passed — the
  21-core baseline exactly, plus 1 confirmed order-dependent flake
  (`test_notification_worker_registration.py::test_importing_job_module_alone_
  registers_everything`, green alone/as-file both before and after via `git stash`).
- **2026-09-01 (MSV3.10 CS-02, commit `7dddf38`)**: 21 failed + 5519 passed — exact
  21-core baseline, zero new. An intermediate run (only the secondary-hardening
  commit `37532c0` applied) showed 25 failed with 4 extra in
  `test_timeline.py::TestExistingFunctionsExcludeSoftDeleted` — vanished on re-run,
  confirmed transient leftover-state noise.
- **2026-08-17 (granted_via paywall fix, commit `91638ce`)**: 21 failed + 5281
  passed — first appearance of the `therapy_tracking_fix1_a12` date-relative flake
  on top of the prior 20-failure composition; operator independently confirmed "21
  BE fail sprzed prac to znany baseline" the same day.
- **2026-08-10 (task B18, after fixing migration chain-tip tests, commit
  `69cc599`)**: 20 failed + 5007 passed — clean baseline, no consent/
  workspace-fix1-a1 flakiness this run.
- **2026-08-10 (C1-BE telemetry, commit `177c026`)**: 20 failed + 5022 passed —
  same clean 20-failure composition.
- **2026-08-10 (after prep-card/logging fix, commit `64ad4f3`)**: 28 failed + 4889
  passed — 8 EXTRA vs the 20-baseline (consent×2, workspace-fix1-a1-migration×6).
  Confirmed NOT a regression: ran both files in total isolation (no other test
  files loaded) and got the identical failures — SQLite leftover-state/order
  sensitivity, not caused by that session's changes.
- **2026-08-10 (earlier same day, after activation check-and-set commit)**: 20
  pre-existing failures + 4876 passed — first appearance of the stable 20-failure
  composition (custom-therapy-sessions×2, first-impression×1,
  notification-improvements×4, onboarding-v2×1, symptom-suggestions×1,
  therapy-frequency×5, voice-fixes×5, walkthrough×1). A 21st failure this run
  (`test_workspace_fix4_migration.py::test_new_head_has_no_known_successor`) WAS a
  real regression (adding a migration on top of an old head broke a chain-tip
  assertion) — fixed same commit. See the migration chain-tip-test lesson in
  MEMORY.md's Key Patterns.
- **2026-07-17**: 21 failures, 4426 passed (up from 4422 baseline after 4 net-new
  tests). Grew to 28 by early 2026-08-10 per a same-day check (see above) before
  settling back to 20 later that day.
