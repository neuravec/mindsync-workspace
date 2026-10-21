# PHASE F — Frontend: Triage chips · Notification deep-links · Timeline summaries — repo `mindsync-frontend/`

## SYSTEM INSTRUCTIONS (read fully before any tool call)

You are a fresh Claude Code session acting as the team lead for the final integration slice of the MSV3.2
Fix.1 batch. Project rules from `CLAUDE.md`. Delegate to `flutter-mobile` (+ `qa-testing`).

- Repo: `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend` — branch **dev**. App code in `mindsync_app/`.
- **Commit locally, stage only files you touched, NEVER push.** No other FE session at the same time.
- REQUIRES: Phases A, D, E finished. Read `STATUS.md` and `API_CONTRACT_Fix1.md` (§2 chips, §9
  notification table) FIRST. Contract mismatch → stop that piece, log in STATUS.md.
- l10n PL + ENG; gen-l10n + build_runner; commit generated code. Baselines: 30 FE failures; analyze clean.
- Binding decision (master plan #1): **1.2 CS-03 chips supersede 1.1 CS-07 bookmark mechanics.** Surviving
  1.1 CS-07 intent: all four card types feed Workspace; nothing disappears from cards; triage works on any
  later Timeline reopen. Keep the existing „Odkrycie" chip group → Realizations (decision #2).

## Item 1 — Triage chips on output cards (1.2 CS-03 + CS-10; replaces 1.1 CS-07 mechanics)
Location: bottom section of ALL four generated output cards: after-therapy, prep, between-sessions note,
recording. Global guardrail: do NOT touch card body content/generation above the chip section — triage
only APPENDS a chip section at the bottom.
UI anatomy: chips grouped by type, order: **Tematy · Pytania · Wątki · Action pointy** (+ existing
Odkrycie group); group header only when non-empty; each chip = candidate text, UNSELECTED by default —
AI never pre-selects. If extraction returned nothing, hide the whole section.
Logic:
- Chip (unselected) → tap → selected + INSTANTLY sent to target module: Temat/Pytanie → „Tematy i pytania"
  (Phase D module); Wątek → Wątki; Action point → Do zrobienia (no due-date UI — author decision).
- Chip (selected) → tap → deselected + withdrawn from the target module.
- Chip whose item was CLOSED in its module → closed state on the card; tap → restores it to the module's
  active list (P2 restore).
- Unselected chips never disappear — they stay on the Timeline card and can be sent later. State persists
  forever (server-side per contract §2).
Done when: on all four card types, tapping a chip of each type creates the item in the correct module
instantly; second tap withdraws it; unselected chips persist; closed items restorable from the card;
reopening an old card from Timeline still allows triage.

## Item 2 — Notification deep-links (1.1 CS-06)
Every notification must navigate directly to the input/output card it refers to — not to Main. Implement
payload → route mapping covering EVERY notification type that exists after this batch (the full type table
is in `API_CONTRACT_Fix1.md` §9, produced by Phase A from the codebase). Cover BOTH app states: cold start
AND backgrounded. Do NOT touch scheduling/content.
Done when: tapping each type in each app state lands on the exact card; the manual test matrix
(type × app state) is written into STATUS.md and the commit message.

## Item 3 — Timeline weekly & monthly summaries UI (1.1 CS-21 FE part)
BE fixed in Phase A (no raw 500; auto-generation at period end; error envelope with retry). FE:
- Auto-generated weekly/monthly cards appear in their Timeline views per period.
- „Generate Now" stays as manual trigger; generates/regenerates the current period's card.
- Generation failure → in-app ERROR STATE on the card with retry via „Generate Now" — never a raw 500/
  exception toast.
Do NOT touch other Timeline views or existing cards.
Done when: cards render for finished periods; Generate Now works without errors; failure shows the in-card
error state with working retry.

## Definition of done (Phase F)
- Items 1–3 per their Done-when; cubit/widget tests for chip state transitions (unselected/selected/closed)
  and the route resolver (unit tests for every type in the §9 table).
- `flutter analyze` no new errors; `flutter test` no new failures vs baseline (30).
- Commits local on dev (generated code committed). STATUS.md report appended (incl. the notification test
  matrix and anything left for device QA).

## Code anchors (planner-provided; verify before use)
All paths under `mindsync_app/` unless noted.

**Triage** — shared `lib/widgets/triage_section.dart` (`TriageSection` L35 — currently full-width tappable
BOOKMARK rows; redesign to chips per anatomy above; „Odkrycie" group L282 → Realizations). Embedded in:
`lib/screens/debrief_capture/widgets/session_card_widget.dart` (TriageSection at L944),
`lib/screens/therapy_capture/widgets/prep_card_widget.dart` (L570),
`lib/screens/therapy_tab/widgets/between_session_note_widget.dart` (L618),
`lib/screens/therapy_tab/widgets/recording_summary_widget.dart` (L486); card detail
`lib/screens/therapy_tab/therapy_card_detail_screen.dart`. Models
`lib/api/models/workspace/triage_proposal_model.dart`, `triage_submit_response_model.dart`. BE: triage
submit `workspace.py` L847; `TriageProposalKind` gets a new thread kind from Phase A (contract §2) —
verify before wiring Wątki chips.

**Notifications** — `lib/main.dart`: local-notif tap `onDidReceiveNotificationResponse` L689 (payload
jsonDecode → `_resolveNotificationRoute` → `_handleNotificationRoute` L43 `sl<GoRouter>().go`); FCM
`onMessageOpenedApp.listen` L877 (background); `getInitialMessage` L894 (cold start →
`pendingNotificationRoute` L34 consumed by splash); foreground `onMessage.listen` L758 branches on
`message.data['type']`; payload encode on send L950. Route logic (unit-testable):
`lib/utils/notification_route_resolver.dart` — `resolveNotificationRoute` L36 (reads `route`, legacy
`deep_link_route`; existing cases: prep_card, moment→`/moment/{id}`, session_recording_ready),
`prepCardRouteFromData` L62. Extend the resolver to the full §9 table.

**Timeline** — `lib/screens/therapy_tab/therapy_tab_screen.dart` + `cubit/therapy_tab_cubit.dart`:
`generateForFilter(TherapyFilter)` L141 → `_weeklySummaryManager.generateLatest()` L165 /
`_monthlyAuditManager.generateLatest()` L167 (analytics event `timeline_generate_now` L153). Managers:
`lib/api/api_managers/weekly_summary_manager.dart`, `monthly_audit_manager.dart`, `timeline_manager.dart`.
Widgets: `lib/screens/therapy_tab/widgets/weekly_summary_widget.dart`, `monthly_audit_widget.dart`.