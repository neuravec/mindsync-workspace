# MSV3.2 Fix.1 — STATUS board

## NEXT STEPS (execution plan — binding for the lead session, incl. after /clear)
1. ~~Phases A–G~~ ALL DONE 2026-07-17. ~~Compat fix (G §3 gating item)~~ DONE same day, operator-ordered: BE `646bda1` + FE `a99fc01` (see PHASE G ADDENDUM at the bottom).
2. **VERDICT: GO.** Batch complete, all suites at baseline, no gating items left.
3. Operator deploy sequence in PHASE G §7 (BE main = **7 commits** + `alembic upgrade head` together — 2 migrations pending, `xx/yy/zz` already ON prod; then FE dev = **11 commits** → Codemagic) and the device-QA checklist in §6.


> Every phase session APPENDS its section here when done (do not edit other phases' sections).
> Next-wave sessions read this file FIRST.

## Template (copy for your phase)

```
## PHASE <X> — <name> — <DONE | PARTIAL | BLOCKED> — <date>
- Session commits (repo + hash + one-liner):
- Items completed (spec IDs):
- Items NOT completed / deviations + why:
- API contract deviations (must also be reflected in API_CONTRACT_Fix1.md):
- New migrations (id, chained from, applied on prod? NO):
- Test results (before → after vs baseline 21 BE / 30 FE):
- Manual QA still needed (device/platform):
- Notes for next phases:
```

---
<!-- Phase reports below -->

## PHASE B — FE Voice — DONE — 2026-07-17
- Commits: mindsync-frontend/dev `716f33b` (local, NOT pushed). Full report: `STATUS_B.md`.
- CS-01 error card redesigned (pufferfish, no Coral Pink, „Ups!/Yieks!", 5 VoiceErrorKind subtexts, ghost „Porzuć"); CS-02 iOS root cause = empty AAC/M4A from HW encoder → WAV-on-iOS in debrief + quick-capture cubits + real content-type in transcribe multipart; CS-04 transcript-promise line removed from all 7 ARBs.
- Tests: 1090 pass / 30 fail = baseline. Device QA needed (list in STATUS_B.md); trade-off flagged: iOS notes >~13 min may hit 25 MB transcribe cap (WAV).

## PHASE A — slice A1 (workspace core) — DONE — 2026-07-17
- Commits: MindSync/main `4c5759d`, `b1f29f7`, `3cd6682`, `3b0a93b` (local, NOT pushed). Migration **aa2b3c4d5e6f** (chained from zz6a7b8c9d0e, idempotent, NOT applied on prod). Full report: `STATUS_A1.md`; contract: `API_CONTRACT_Fix1_A1.md`.
- Lifecycle+archives (agenda/todo/thread/topics), triage chip toggle endpoints + `thread` kind, NEW TopicQuestionItem module, agenda add-to-agenda→idempotent toggle + realization agenda-pin toggle (FIX.05), thread archive view + reopen-at-capacity queues instead of 409, todos `repeat_freq` + TodoCompletion log with LAZY rollover (no cron), NEW `GET /therapy-tracking/session-state` for CS-09.
- Tests: 4382 pass / 21 fail = baseline. Deviation: Goals lifecycle NOT done (file ownership) → gap-closing slice A3 spawned.

## PHASE A — slice A2 (AI/summaries/notifications) — DONE — 2026-07-17
- Commits: MindSync/main `c878e9f` (local, NOT pushed). Full report: `STATUS_A2.md`; contract: `API_CONTRACT_Fix1_A2.md`.
- Summaries raw-500 root cause fixed (prep phase outside try/except → structured error envelope; removed `default` from structured-output schema); auto-generation already cron-wired (audited, no change). Mood Trend: prompt rewrite (qualitative, banned patterns), `last_updated_at`, AI-summary bootstrap on first score. Goals refresh audited OK + regression test. Notification type→payload table complete; `recording_id` added to session-recording push; 2 dead notification paths documented. Therapy relationship: `should_show_main_prompt` added. A13 audit: backend does NOT reject iOS uploads (confirms Phase B diagnosis).
- Tests: 4371 pass / 21 fail = baseline. `import app.main` clean.

## PHASE A — slice A3 (goals lifecycle gap-close) — DONE — 2026-07-17
- Commits: MindSync/main `2554187` (local, NOT pushed). Migration **bb3c4d5e6f70** (adds `user_goals.achieved_at`, chained from aa2b3c4d5e6f → NEW single head). Full report: `STATUS_A3.md`; contract: `API_CONTRACT_Fix1_A3.md`.
- `achieved_at` stamped on ACHIEVED/cleared otherwise; NEW `GET /goals/archive` (Zakończone cele, newest-first, updated_at fallback for legacy rows); NEW `DELETE /goals/{id}` hard delete; close/restore via existing `PUT /{id}/status` (deliberate, documented). CS-20/CS-22 untouched.
- Tests: 4422 pass / 21 fail = baseline (36 new).
- **⚠ DEPLOY-ORDER FLAG:** unlike the new Workspace tables, `user_goals` is a LIVE prod table — `bb3c4d5e6f70` must run TOGETHER with the deploy or the whole Goals feature 500s on `UndefinedColumn`.
- Backend (slices A1+A2+A3) is now COMPLETE. Alembic chain: … → zz6a7b8c9d0e → aa2b3c4d5e6f → **bb3c4d5e6f70 = HEAD**; none applied on prod.

## PHASE C — FE Main screen — DONE — 2026-07-17
- Commits: mindsync-frontend/dev `914ddc3` (local, NOT pushed; dev now ahead by 2: B `716f33b` + C). Full report: `STATUS_C.md`.
- CS-08 root cause = `sanitizeMainTabWidgetOrder` dropped new module ids for users with pre-existing saved layouts (why iOS "failed") → now reconciles: spec order default, missing modules injected at spec position, user reorder of seen modules preserved. CS-10 homework 2→3 oldest-open (`/todos/today?limit=3`). CS-11 score input restored (slider → POST /symptoms/{id}/scores) + relative last-scored dates. FIX.03 AI summary inside Mood Trend (no bullets), empty-state box deleted (7 locales). FIX.04 `refreshHealthCheck()` on flow return. 1.2 CS-01 reminder „open" → pushes fresh check-in + dismisses.
- Documented deltas (deliberate, for Phase G audit): CS-09 state machine stays CLIENT-side (verified correct + tested; `GET /therapy-tracking/session-state` = fast-follow because schedule syncs to BE are fire-and-forget); FIX.04 keeps session-anchored gate instead of `should_show_main_prompt` (would change when the prompt shows).
- Tests: 1093 pass / 30 fail = baseline; analyze clean. Device QA list in STATUS_C.md (note: 1.2 CS-01 moment generation needs the moment-types enum migration applied on prod).

## PHASE D — FE Workspace core — DONE — 2026-07-17
- Commits: mindsync-frontend/dev `861a805` (58 files, +5092/−646; local, NOT pushed; dev ahead by 3: B+C+D). Full report: `STATUS_D.md`.
- Shipped: shared widgets (P1 `lib/screens/workspace/widgets/voice_or_text_capture_sheet.dart` incl. prefilled-edit + todos repeat control; P2 `workspace_archive_view.dart` + FE badge store `lib/utils/workspace_archive_badge_store.dart` [has threads/goals keys ready]; P3 `workspace_expandable_list.dart`; 3-dot menu + delete-confirm `workspace_item_menu.dart`); rename Pracownia/Workspace (nav_workspace + workspace_title, 7 locales; nav_therapy untouched); lifecycle §1 wired; Agenda (tags, archive both surfaces, 3-dot menu, +Dodaj temat); NEW module Tematy i pytania (CS-05 full); Do zrobienia (checkbox-only close, Zrobione archive replaces counter, repeats via edit sheet, P3, +Dodaj zadanie, no due-dates; /todos/today untouched).
- Deliberate deviations (Phase G audit): Agenda list stays top-3+see-all (P3 not required by spec there); todos keep server FIFO inside P3; agenda odklik machinery kept in cubit for Phase-F triage; GET /todos/{id}/completions unconsumed (no UI specced).
- Tests: 1120 pass / 30 fail = baseline; analyze clean. Device QA in STATUS_D.md. Deploy note: new module/repeats/edit-delete need migration `aa2b3c4d5e6f` applied WITH the deploy.

## PHASE E — FE Workspace modules — DONE — 2026-07-17
- Commits: mindsync-frontend/dev `67a932d` (local, NOT pushed; dev ahead by 4: B+C+D+E). Full report: `STATUS_E.md` (incl. Phase-F hooks + device-QA matrix).
- Wątki: add-to-agenda = idempotent pin TOGGLE (dead button + duplicates fixed); card cleanup (archive button gone, swipe/chevron close); P3 list; „5 z N aktywnych" only >5; „+ Dodaj wątek" P1; „Domknięte wątki" P2 + badge; ≥5 nudge (thread still added). Realizations: pin state DERIVED from agenda active list via new `/agenda-pin` — deleting agenda item clears pin by construction (FIX.05). Goals: ↻ refresh (loading, failure keeps text + retry toast) left of „Zakończone cele" P2; single „+ Dodaj cel"; achievedAt + GET /goals/archive wired. Therapy Relationship: bottom clipping fixed (nav-aware padding); colors bound to stored relationship_state (orange removed; safety_escalation = red + warning icon); P3 list, contrast 6.2:1 (AA ✓, needed darker primary[700] control color).
- Deviations documented in STATUS_E.md (reopen-409 cubit-level; ThreadsFullScreen unlinked; goal delete wired-not-surfaced; refresh re-list ~3s). No contract mismatches.
- Tests: 1125 pass / 30 fail = baseline; analyze 0 errors; 13 l10n keys × 7 locales.
- **WAVE COMPLETE.** Remaining: Phase F (as 3 split worktree agents + integrator per NEXT STEPS above) → Phase G.

## PHASE F — FE triage chips + notification deep-links + Timeline summaries — DONE — 2026-07-17
- Session commits: mindsync-frontend/dev `03c8f49` (F2) + `14fda1a` (F1) + `087e8f7` (F3) + merges `e57e713`/`3e5e939`/`019031b` (local, NOT pushed; dev ahead of origin by 10). Ran as 3 parallel worktree agents + integrator (worktrees removed, branches deleted). Full report: `STATUS_F.md`.
- Items completed: 1.2 CS-03+CS-10 (TriageSection rewritten rows→grouped chips, order Tematy·Pytania·Wątki·Action pointy·Odkrycie, server-driven 3-state chips via `POST /triage/{id}/toggle`, closed→restore, old-card triage OK, per-kind cubit refresh); 1.1 CS-06 (resolver extended to full §9 table — only real gap was `session_recording_ready`→ exact card via new `/therapy/recording/:id`, legacy fallback to Timeline tab; 11 moment types already correct); 1.1 CS-21 FE (in-card error state + retry; `ApiException` exposes A2 error envelope; cubit smart-routes retry→`POST /retry/{id}` because re-`/generate` after failure would DUPLICATE the row — traced in BE).
- Deviations (for Phase G audit): F1 skips `AgendaCubit` refresh on chip tap (no toggle outcome touches Agenda); legacy `submitTriage` batch API left unused-but-present; FAILED monthly audits excluded from timeline listing (BE asymmetry) so visible-card retry reachable only for weekly today.
- API contract deviations: none (F1 verified §2 against BE schemas directly; F2 none; F3's `/retry` routing is contract-compliant usage, nuance documented).
- New migrations: none (FE-only). Requires BE A1/A2/A3 deployed+migrated (chips/modules/envelope).
- Tests: post-merge full suite **1161 pass / 30 fail = exact baseline** (failing set verified pre-existing); analyze 0 errors; 9 new l10n keys × 7 ARBs (gen-l10n validated byte-identical post-merge).
- Manual QA still needed: consolidated list in `STATUS_F.md` (chips on 4 card types + restore + offline revert; F2 type×app-state matrix incl. real prod push with `recording_id`; F3 failure/retry weekly+monthly; PL spot-checks).
- Notes for next phases: Windows CRLF churn gotcha documented in STATUS_F.md; `thread`-kind chips need data-analytics to emit thread proposals (gap from STATUS_A1/E).

## PHASE G — Final QA + deploy checklist — DONE — 2026-07-17
Executed as 5 parallel read-only agents (G1 suites+offline safety / G2 done-when audit+grep gates / G3 contract check / G4 security / G5 prod migration state). No code changed, no commits, nothing pushed.

### 1. Test suites (G1)
- BE `python -m pytest app/tests/`: **4422 pass / 21 fail = exact baseline** (all 21 in the pre-documented categories). New failures: none.
- FE: `flutter analyze` 0 errors (142 pre-existing infos); `flutter test` **1161 pass / 30 fail = exact baseline** (1:1 map to the known baseline files). New failures: none.
- Offline boot-safety: boot-critical router tree `app.api.v1.api` imports cleanly (325 routes). Raw `import app.main` fails ONLY on local Windows (firebase cert path — known documented gap, covered by `test_fix1_goals_lifecycle.py::TestPostgresDDLCompiles`).
- DDL: both new migrations compile with the postgresql dialect, both fully IDEMPOTENT (`_column_exists`/`_table_exists`/`_index_exists` guards), zero `Enum(PyEnum)`. Alembic: all 67 version files parsed → **single head `bb3c4d5e6f70`**, expected chain confirmed.

### 2. Done-when audit (G2) — 38/39 PASS, 1 FAIL, 0 blockers
- 39 unique spec items (41 minus 2 duplicates). **PASS 38** (6 carry NEEDS-DEVICE-QA sub-notes for clauses unprovable statically: CS-02, CS-06, CS-09, CS-11, CS-23, 1.2 CS-01). All documented C/D/E/F deviations judged **ACCEPTABLE** against literal Done-when text.
- **FAIL (1): 1.1 CS-21 monthly branch** — `crud.py:4147-4157` `_fetch_monthly_audits_for_timeline` excludes FAILED rows from the Timeline listing (weekly does not), so a persisted monthly failure shows no card/error/retry on revisit. Pre-existing BE behavior, NOT introduced by this batch, not a crash. **Fast-follow: remove the `!= FAILED` filter to mirror weekly** (owner: data-analytics).
- New tech-debt findings: dead unreachable `ThreadDetailScreen` (`/workspace/threads/:id`) still carries the old 3-action design incl. an „Odklik" button (zero navigation call sites — cleanup ticket); dead ARB keys `workspace_goalAddCta`, `workspace_odklik(Done)`.
- **Grep gates: 7/7 PASS** (transcript hint, „Odkliknij", tab naming, empty-state strings, double-plus, Coral Pink, due-date UI).

### 3. Cross-layer contract check (G3) — no FE↔BE mismatch; ONE backward-compat regression
- Every contract section with an FE consumer **MATCHES** exactly (paths, fields, nullability, error envelopes incl. A2 `{"detail":{error_code,retryable,summary_id|audit_id}}`, triage 3-state `chip_state`, `PinToggleResponse`).
- Failure-mode rule PASS: only a definitive 404 is ever treated as "new user" (`api_error_utils.dart::isDefinitive404`, doc-commented); all new cubits route errors to distinct error states — no path maps a BE error to onboarding.
- Unconsumed-by-design (non-blocking, documented): `GET /todos/{id}/completions`, `DELETE /threads/{id}`, `DELETE /goals/{id}` (manager wired, no UI — follow-up ticket), `GET /therapy-tracking/session-state` + `should_show_main_prompt` (deliberate Phase C deferrals; note: BE's ~30h `debrief_cta` recency window therefore not live — FE's client-side trigger has no upper bound).
- **⚠ BACKWARD-COMPAT REGRESSION (verified against production `origin/dev` `12ffa71`):** `PUT /workspace/threads/{id}/add-to-agenda` response changed `AgendaItemResponse` → `PinToggleResponse`. The A1 contract claimed "no live consumer" — WRONG: Workspace already shipped pre-Fix.1. Old installed builds parse the response with `AgendaItemModel.fromJson` (non-nullable `text/sourceType/status/createdAt`) → throws on the new shape. Blast radius: the thread "Dodaj do agendy" action silently breaks for users on pre-Fix.1 builds after BE deploy, until they update the app (no crash-loop, no data loss). Old builds live for weeks per project convention. **Operator decision required — see GO/NO-GO.**
- Minor nits: CS-17 counter definition (BE `count` includes queued threads, FE recomputes excluding them — product call); stale 409-catch comments in threads cubit.

### 4. Security pass (G4) — NOT deploy-blocking
- **0 Critical / 0 High.** Horizontal-privilege-escalation audit PASS on every new/changed endpoint (all lookups user-scoped at CRUD, 404-not-403). No mass-assignment. GDPR: all new tables CASCADE on user delete (model + DDL), new free-text encrypted (Fernet), `recording_id` push owner-scoped.
- **MED-001**: `GET /dashboard/mood-trend` returns raw `str(e)` in `detail` (only deviation from the envelope pattern) → fix to generic message + server-side log (data-analytics).
- **MED-002**: no cooldown on `/retry` while FAILED → denial-of-wallet loop on OpenAI; add 15–30s per-user cooldown (data-analytics).
- **LOW-001/002**: defense-in-depth `user_id` filters missing on two internal lookups (`touch_agenda_item` thread lookup; `_resolve_chip_state` realization lookup) — not currently exploitable (backend-api).

### 5. Prod migration state (G5, read-only via one-off dyno, stopped after)
- Prod `alembic_version` = **`zz6a7b8c9d0e`**; schema agrees exactly (no partial drift). **`xx…`/`yy…`/`zz…` (MSV3.2 batch) are ALREADY APPLIED on prod** — corrects earlier assumption. The moment-types enum needed by 1.2 CS-01 QA is therefore already live.
- **PENDING (what `alembic upgrade head` will run): 1) `aa2b3c4d5e6f`, 2) `bb3c4d5e6f70`.** Both additive-only, idempotent, no native enums. `user_goals` = 84 rows, nullable ADD COLUMN only. Report: `db-reports/msv3_2_fix1_phaseG_migration_state_2026-07-17.md`.

### 6. Consolidated manual device-QA checklist (operator)
1. **CS-02** iOS voice end-to-end on a REAL iPhone: session recording, debrief/prep/between notes, weekly check-in; WAV path; note >~13-min notes vs 25 MB transcribe cap.
2. **CS-08/CS-10** Main order on a physical iPhone, esp. an account with a pre-existing saved layout; homework shows 3 oldest-open.
3. **CS-06** notification matrix: 11 moment types + `session_recording`(+`recording_id`) + `admin_broadcast` × {cold start, backgrounded, foreground} — land on the exact card; recording deep-link against a REAL prod push.
4. **CS-23** Therapy Relationship bottom clipping: small + large device, Android gesture-nav + iOS home indicator.
5. **CS-09** live transitions: day-boundary flip, "session starting now", debrief CTA after session.
6. **CS-11** live LLM narrative spot-check (no point-deltas/history-recital); score slider posts and relative date updates.
7. **1.2 CS-01** reminder „open" → fresh check-in + dismiss (enum already on prod ✓).
8. **F1 chips**: each chip kind creates/withdraws/restores in the right module on all 4 card types; old Timeline card reopen; airplane-mode mid-tap revert; narrow-device wrap. (`thread` chips need data-analytics to emit thread proposals — known gap.)
9. **F3**: weekly + monthly Generate Now failure → in-card banner + retry; FAILED weekly card in-card retry; PL spot-check of new strings.
10. **Phase D/E spot-checks**: Pracownia rename everywhere; archives P2 + badges; threads „5 z N" + nudge; goals ↻ + „Zakończone cele"; TR colors incl. `safety_escalation` red+warning.

### 7. Deploy checklist (operator — do NOT execute out of order)
1. ~~DECIDE the add-to-agenda compat item~~ RESOLVED: compat fix executed (see PHASE G ADDENDUM — BE `646bda1` + FE `a99fc01`).
2. Backend: `git push` origin main (**7 commits**: 4c5759d, b1f29f7, 3cd6682, 3b0a93b, c878e9f, 2554187, 646bda1) + deploy to Heroku **together with** `heroku run alembic upgrade head --app mindsync` (2 pending migrations; no release phase — deploy ≠ migrate). Verify: `heroku run alembic current --app mindsync` → `bb3c4d5e6f70`; watch logs for H10.
3. Frontend: push dev (**11 commits**) → Codemagic → TestFlight/Play internal.
4. Fast-follows (non-gating, file tickets): CS-21 monthly FAILED filter; MED-001; MED-002; LOW-001/002; delete dead `ThreadDetailScreen` + dead ARB keys; surface `DELETE /goals/{id}` in UI or drop it; adopt `GET /therapy-tracking/session-state` + `should_show_main_prompt` (incl. debrief-CTA upper bound); CS-17 counter definition; thread-kind AI extraction (data-analytics).

### 8. VERDICT: **CONDITIONAL GO** → resolved to **GO** by the addendum below
Suites at exact baselines, 0 security blockers, 38/39 done-when PASS, contracts match, migrations safe and verified against live prod. **The single gating item was the §3 backward-compat regression on `PUT /threads/{id}/add-to-agenda`** — operator chose the compat fix (executed same day, see addendum).

## PHASE G ADDENDUM — add-to-agenda compat fix — DONE — 2026-07-17 (operator-ordered)
- **BE commit `646bda1`** (MindSync/main, now **7 ahead** of origin): `PUT /workspace/threads/{id}/add-to-agenda` restored as LEGACY-COMPAT — ADD-only, idempotent (repeat call returns the same item, no duplicates), returns full `AgendaItemResponse` → old builds keep working. Toggle semantics moved to NEW `PUT /workspace/threads/{id}/agenda-pin` returning `PinToggleResponse` (mirrors realizations). New CRUD helper `get_or_create_agenda_pin`; user scoping unchanged (404-not-403). Tests: targeted 121 pass; full suite **4426 pass / 21 fail = baseline** (+4 new tests); boot-check clean. Contract doc §3c corrected (the wrong "no live consumer" claim removed).
- **FE commit `a99fc01`** (mindsync-frontend/dev, now **11 ahead** of origin): `toggleThreadAgendaPin()` repointed to new `workspaceThreadAgendaPin` endpoint constant; `PinToggleResponse` parsing unchanged; old constant annotated legacy-compat-only, zero remaining new-code call sites (grep-verified). Analyze 0 errors; full suite **1161 pass / 30 fail = baseline**; pin-toggle tests (CS-14/CS-19) pass.
- Net effect: old installed builds hit the old route and get the shape they parse; the new app uses the new toggle route. No semantics change for the new code; the Fix.1 no-duplicates improvement retained on both routes.
- Device QA: nothing new beyond §6 — verify thread pin/unpin against the deployed backend once live.
