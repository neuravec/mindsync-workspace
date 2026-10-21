---
name: reference-fe-dev-push-via-worktree
description: How to push a frontend feature branch to mindsync-frontend dev without touching a busy working tree (detached worktree, merge, analyze/test, push), plus the Codemagic bot commit that makes a merge almost always necessary
metadata:
  type: reference
---

Pushing a frontend branch to `dev` (push = Codemagic, then TestFlight and Play internal) while another agent is using the main working tree:

- **Expect a merge, not a fast-forward.** Codemagic `app-create-version` pushes a "Pre-release updates" commit (pubspec version + CHANGELOG, author Codemagic Bot) to `dev` after every push and tags it `app_X.Y.Z`. A feature branch cut from `dev` is therefore almost never a descendant of `origin/dev`. The bot commit only touches `mindsync_app/pubspec.yaml` and `CHANGELOG.md`, so the merge is clean unless the branch also edits those.
- **Recipe that leaves the main tree alone:** `git worktree add --detach <scratchpad>/fd origin/dev` (short dir name: scratchpad path is ~118 chars and the longest tracked path is ~110, Windows MAX_PATH 260), `git -C <wt> merge --no-ff <branch>`, then in `<wt>/mindsync_app`: `flutter pub get`, `flutter analyze`, targeted `flutter test <dirs>`; re-`fetch` right before pushing and push only if `origin/dev` is still an ancestor (`git -C <wt> push origin HEAD:dev`); then `git worktree remove --force <wt>` (force because `pub get` regenerates the desktop plugin registrants, which differ from the committed ones; never commit them).
- **Gotcha:** `git -C <worktree> config X` writes to the SHARED repo `.git/config`, not to the worktree. Use `git -c core.longpaths=true ...` per command instead, or unset afterwards.
- **Analyzer output format on Flutter 3.41.1** is `error - msg - file:line - code` (hyphen), not `error • ...`. Filtering on `error •` silently finds nothing. Count with `grep -cE '^\s*error (•|-) '`.
- **`flutter analyze` can hang** (seen 2026-10-05 while other agents ran flutter in the main tree): the CLI sits on "Analyzing mindsync_app..." and the analysis server's `dartvm.exe` child is idle (near-zero CPU delta). Normal runtime is 40 to 75 seconds. Always wrap it as `timeout 300 flutter analyze` (and `timeout 560 flutter test ...`) so a hang can't hit the 600 s tool cap and get auto-backgrounded. To recover, kill only your own tree: `cmd.exe /c flutter.bat analyze` → `dart.exe ... flutter_tools.snapshot analyze` → `dartvm.exe` → `dart.exe analysis_server.dart.snapshot` → `dartvm.exe`; leave the VS Code `dart.exe language-server` alone.
- Flutter SDK: global `/c/Users/mikol/flutter` is 3.41.1 and matches `mindsync_app/.fvmrc`; the `.fvm/flutter_sdk` symlink still points at 3.27.0 and is stale, so do not use it.

First used 2026-10-05 for the first-voice-conversation batch, see [[project-first-voice-conversation-fe-deploy-2026-10-05]].
