---
name: project-workspace-wa1-v2-redesign-2026-10-13
description: Workspace tab WA1 v2 redesign (branch feat/workspace-redesign, commit 1e1c441, local only) - palette, module order, workspace_item_action event, gotchas hit
metadata:
  type: project
---

WA1 v2 Workspace redesign committed locally on feat/workspace-redesign (1e1c441, worktree mindsync-frontend-wt-workspace-redesign), not pushed.

- Order: agenda, todo, questions, goals, threads, realizations, therapy_relationship (`kWorkspaceModuleOrder` in workspace_screen.dart). Colours live in `WorkspacePalette` (workspace/widgets/workspace_palette.dart), deliberately NOT in MsColors to avoid merge collisions with the parallel "Karty" redesign.
- New event `workspace_item_action` {section_name, action} (closed sets in AnalyticsEvents); `WorkspaceItemMenu.sectionName` logs every entry except Delete (callers log delete after confirm).
- Product rule from reviewer notes: change UI, not content/functions; "Orca saved for you" and single add entry were rejected.

**Why:** operator wants several agent teams merged next day; low-churn diffs matter.
**How to apply:** NEVER run `dart format` on existing files in this repo: the codebase is not formatter-clean, one run rewrote ~40 untouched files (had to restore and re-apply edits via scripts). Whole-screen widget tests need a tall `tester.view.physicalSize` because the Workspace SliverList builds lazily; `find.byKey` on a StatelessWidget key is not a Container (use descendant with matchRoot). Stub manager calls with never-completing `Completer().future` to avoid unhandled async errors from fire-and-forget cubit calls. Related: [[project-account-scoped-reset-2026-10-12]].
