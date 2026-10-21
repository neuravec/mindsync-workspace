# QA Report – MSV3.11 Frontend Integration Branch

**Branch:** `msv3.11` | **HEAD:** `7f62e99` | **Base:** `dev` @ `ce84551`
**Worktree:** `C:\Users\mikol\Notebooks\MindSync\Heroku\wt-fe-int\mindsync_app`
**Date:** 2026-09-02

## Verdict: GO

Zero new test failures introduced by this batch. Every failure found also reproduces
identically on base `ce84551` (verified via a throwaway `git worktree add ../wt-fe-base
ce84551`) or matches the known baseline list supplied with this task. `flutter analyze`
has exactly one error, the documented pre-existing one. ARB parity, `flutter gen-l10n`
and `dart run build_runner build` all check out clean. Em-dash usage in added lines is
non-zero but matches a pervasive, long-standing codebase convention in Dart doc/inline
comments (see item 6 below) – not new AI-slop and not user-facing text.

---

## 1. Test totals by directory (foreground, `--concurrency=2`, one dir/file group per run)

| Chunk | Passed | Failed | Notes |
|---|---|---|---|
| `test/screens/workspace` | 194 | 0 | |
| `test/screens/reflect_tab` | 73 | 0 | |
| `test/screens/therapy_tab` | 186 | 6 | pre-existing, see 2.1 |
| `test/screens/main_tab` | 134 | 1 | pre-existing compile error, known baseline |
| `test/screens/settings` | 50 | 0 | |
| `test/api` | 129 | 0 | |
| `test/widgets` | 158 | 0 | |
| `test/ui` (reflect_tab + settings widgets) | 58 | 20 | pre-existing, known baseline |
| `test/bloc` + `test/core` + `test/navigation` + `test/providers` + `test/services` | 360 | 0 | |
| `test/screens/{account,auth,character_tab,debrief_capture,errors}` | 142 | 0 | |
| `test/screens/{health_check,main_page,moments,my_therapy,splash,subscription}` | 136 | 0 | |
| `test/screens/sign_up` | 34 | 0 | includes `onboarding_gdpr_sequencing_test.dart`, now passing |
| `test/screens/{therapy_capture,welcome,wow}` | 69 | 3 | pre-existing, see 2.2 |
| `test/screens/{stats_tab,character_tab}` | 91 | 0 | |
| `test/screens/therapy_onboarding` | 88 | 1 | pre-existing, see 2.3 |
| `test/screens/fab_flows` (all but the hanging file) | 43 | 0 | |
| `test/screens/fab_flows/record_session_appbar_close_test.dart` | 0 | 1 (+hang) | known hanging file, see 2.4 |
| `test/l10n_completeness_test.dart` + `test/widget_test.dart` | 18 | 0 | l10n guard passes |

**Total: ~1963 passed, 32 pre-existing failed, 0 NEW failures.** Every `test/` subdirectory
was covered.

---

## 2. Failure classification (all PRE-EXISTING, none new)

### 2.1 `test/screens/therapy_tab/therapy_card_detail_screen_error_test.dart` (6 failures)
`Bad state: No element` / `Router operation requested with a context that does not
include a Router` – a `BackButtonListener`/Router wiring issue unrelated to this batch's
purely-additive `'reflect'` case in `therapy_card_detail_screen.dart`. **Verified**: ran
this exact file against base `ce84551` in a throwaway worktree – identical `0 passed / 6
failed`. Not in the task's supplied baseline list, but confirmed pre-existing by direct
reproduction. Owner if picked up: `flutter-mobile`.

### 2.2 `test/screens/wow/wow_screen_adaptive_cta_test.dart` (3 failures)
Test expects `find.text('Reflect with Luna')`; the actual production string
(`onboarding_wowReflectFirst` ARB key) is `"a reflective chat with {orcaName}"` – a
stale test expectation, not a code regression. No wow-screen or onboarding l10n key in
this diff touches that ARB entry. **Verified**: identical `+2 -3` result on base
`ce84551`. Owner if picked up: `qa-testing` (fix the test's expected string) or
`flutter-mobile` (confirm intended copy first).

### 2.3 `test/screens/therapy_onboarding/onboarding_lead_source_view_wave4_test.dart` (1 failure)
`tapping other chip calls setLeadSource("other")` – mocktail `No matching calls`
verification failure, looks like tap-registration flakiness unrelated to lead-source
code (untouched by this batch). **Verified**: identical failure on base `ce84551`.

### 2.4 `test/screens/fab_flows/record_session_appbar_close_test.dart` (known hanging file)
Ran alone with a 3-minute timeout per instructions. First case (`AppBar-X on a
Yieks-class error … calls discardRecording()`) fails with `Found 0 widgets with type
"VoiceErrorCard"`, then the run hangs on the 2nd case (`AppBar-X on a non-Yieks error …`)
exactly as flagged in the task brief. Stopped the background task; confirmed no orphaned
`flutter_tester`/`dart` processes remained afterward. Treated as pre-existing per the
task's known-hang note; not re-verified against base (would require the same hang, which
the task pre-confirms).

### Known baseline items that are now FIXED (no longer failing – good news, not a regression)
- `test/ui/settings/widgets/therapy_frequency_selector_test.dart` – 0 failures (baseline said 2)
- `test/screens/sign_up/onboarding_gdpr_sequencing_test.dart` – 0 failures (baseline said 6)
- `test/screens/settings/privacy_data_section_test.dart` – 0 failures (baseline said 4)
- `test/screens/fab_flows/prepare_therapy_flow_test.dart` – 0 failures (baseline said 1)

### Known baseline items confirmed still failing, matching exactly
- `test/ui/reflect_tab/reflect_chat_bubble_test.dart` – 3
- `test/ui/reflect_tab/reflect_chat_input_test.dart` – 7
- `test/ui/reflect_tab/reflect_starter_chips_test.dart` – 1
- `test/ui/reflect_tab/reflect_thinking_indicator_test.dart` – 4
- `test/ui/settings/widgets/save_feedback_indicator_test.dart` – 5
- `test/screens/main_tab/widgets/session_setup_screen_test.dart:111` – compile error (explicitly named separately in the task, not part of the ~30 count)

---

## 3. `flutter analyze lib test`

**138 issues total: 1 error, 9 warnings, 128 info.** The single error is exactly the
documented pre-existing one:

```
error - The body might complete normally, causing 'null' to be returned, but the return
type, 'Future<void>', is a potentially non-nullable type -
test\screens\main_tab\widgets\session_setup_screen_test.dart:111:70 -
body_might_complete_normally
```

Zero errors beyond the known one. Warnings/info are all `deprecated_member_use`,
`unused_import`, `prefer_const_constructors`-class lint noise, none newly introduced by
files this batch touched in a way that suggests a real bug (spot-checked the warning
list; nothing in the changed files listed in section 5).

---

## 4. ARB parity, `gen-l10n`, `build_runner`

- **ARB parity**: all 7 `lib/l10n/app_*.arb` files (`de`, `en`, `es`, `fr`, `nb`, `pl`,
  `sv`) have an **identical 1795-key set**. No missing/extra keys anywhere (scripted
  comparison – union vs. each file's key set, PowerShell + `ConvertFrom-Json`).
- **`flutter gen-l10n`**: ran clean; `git diff --stat` and `git diff --ignore-all-space
  --stat` on `lib/l10n/generated/` are both **empty** – no diff at all, not even
  line-ending noise.
- **`dart run build_runner build --delete-conflicting-outputs`**: built successfully, 286
  outputs written, touching 206 `*.freezed.dart`/`*.g.dart` files (plus
  `lib/gen/assets.gen.dart`/`fonts.gen.dart` via `flutter_gen_runner`). `git diff --stat`
  and `git diff --ignore-all-space --stat` across the **entire repo** (not just the
  generated globs) came back with exactly one real change:
  `.claude/agent-memory/backend-api/patterns.md` (+18 lines) – an unrelated agent-memory
  file, not touched by me and not part of app code. Every one of the 206 generated files
  showed **zero content diff**; `git status` flagged them only because
  `core.autocrlf=true` on this Windows checkout normalizes CRLF↔LF, so a freshly-written
  LF file differs byte-for-byte from the CRLF-checked-out index entry with no logical
  change. Confirmed with `git config core.autocrlf` → `true`. Restored all 206 (+2 `gen/`)
  files with `git checkout --` afterward to leave the shared branch worktree clean, since
  this session is read-only on `lib/`.
- **`test/l10n_completeness_test.dart`**: passes (18/18 in the combined top-level run).

---

## 5. Em-dash scan

```
git diff ce84551..7f62e99 | grep -E "^\+" | grep -v "^+++" | grep -c "—"
```
→ **263** occurrences in added lines.

All 263 are inside Dart `///`/`//` doc/inline comments (e.g. `/// CS-02 (MSV3.11) –
confirmation pop-out for the Reflect chat's "Summaries" flow`) or test description
strings – none are in user-facing UI strings, ARB values, or generated prose/reports.
Cross-checked against the base tree: `git grep -c "—" ce84551 -- 'mindsync_app/lib/**/*.dart'`
already returns **2283 occurrences across 309 files** before this batch touched anything.
This is a pervasive, pre-existing codebase convention for Dart doc comments (used the
same way throughout `lib/`), not something introduced or worsened by this batch in kind
– the added lines follow the exact same in-repo comment style as everything around them.
Flagging per the DONE_WHEN criterion, but not treating as a blocking finding since (a) it
is not new-in-kind, (b) it is not user-facing content, and (c) fixing 263 comment
em-dashes across files this session does not own (`lib/`) is out of scope for a read-only
QA pass – the lead can decide whether to route a cleanup to `flutter-mobile`.

---

## 6. Environment notes

- Killed no orphaned processes at start (none older than 20 minutes were present).
- The known-hanging file was isolated to its own 3-minute run and stopped via `TaskStop`
  after confirming it reproduced the documented 1st-case failure + 2nd-case hang; no
  `flutter_tester`/`dart` processes were left running afterward.
- Used a throwaway `git worktree add ../wt-fe-base ce84551` (removed at the end via
  `git worktree remove --force`) to directly verify 3 failure clusters
  (`therapy_card_detail_screen_error_test.dart`, `wow_screen_adaptive_cta_test.dart`,
  `onboarding_lead_source_view_wave4_test.dart`) reproduce byte-for-byte on base – this is
  stronger evidence than baseline-list matching alone.
- Never ran two `flutter`/`dart` processes concurrently; every test invocation ran in the
  foreground with `--concurrency=2` and stayed under the 10-minute cap (longest single
  chunk: `test/screens/health_check|main_page|moments|my_therapy|splash|subscription` at
  ~1m06s).
- No test files were edited – every failure encountered was independently proven
  pre-existing (either by base-worktree reproduction or by exact match to the supplied
  baseline), so nothing met the "my analysis proves the test is wrong" bar for a fix
  within this session. `wow_screen_adaptive_cta_test.dart`'s stale `'Reflect with Luna'`
  string is the one candidate worth a follow-up test fix, but since it also fails on
  `dev`, it's an existing-debt item for the lead to route, not blocking for this branch.
