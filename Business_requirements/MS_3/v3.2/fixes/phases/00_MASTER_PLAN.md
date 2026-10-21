# MSV3.2 Fix.1 — Master Plan (phases for parallel Claude Code sessions)

> **How to use (operator):** open a NEW Claude Code session in `C:\Users\mikol\Notebooks\MindSync\Heroku`
> (CLAUDE.md + project memory load automatically) and prompt it with:
> `Przeczytaj i wykonaj w całości plik "Business_requirements\MS_3\v3.2\fixes\phases\<PHASE_FILE>.md"`
> Each phase file is self-contained: it embeds its spec items verbatim, code anchors, rules and done-criteria.

## Scope

End-to-end implementation of:
1. `MSV3.2Fix.1.1 - Change Spec.docx` — 16 items (voice, notifications, triage, Main, Workspace, Timeline)
2. `Update MSV3.2Fix.1.2 - Workspace Feature.docx` — 25 items (Workspace hub: chips, archives, add-sheets, modules)
3. Pufferfish Lottie animation (asset `assets/lottie/pufferfish_error_v2.json` — **already committed** in the FE repo)

Full extracted spec texts (reference): `SPEC_Fix1.1_full_text.txt`, `SPEC_Fix1.2_full_text.txt` (same folder).

## Wave schedule (parallelism matrix)

| Wave | Sessions run in parallel | Repo(s) | Why safe |
|------|--------------------------|---------|----------|
| 1 | **PHASE A (backend)** ∥ **PHASE B (FE voice)** | MindSync/ ∥ mindsync-frontend/ | different git repos, zero file overlap |
| 2 | **PHASE C (FE Main)** (A may still be running) | mindsync-frontend/ | only one FE session at a time |
| 3 | **PHASE D (FE Workspace core)** — requires A finished (API contract) | mindsync-frontend/ | sequential FE |
| 4 | **PHASE E (FE Workspace modules)** — requires D (shared P1/P2/P3 widgets) | mindsync-frontend/ | sequential FE |
| 5 | **PHASE F (FE triage + notifications + Timeline)** — requires A, D, E | mindsync-frontend/ | sequential FE |
| 6 | **PHASE G (final QA + deploy checklist)** | both (read/test only) | after everything |

**HARD RULE: never run two FE sessions at once.** They collide on ARB/l10n files, generated code
(build_runner, gen-l10n) and shared cubits/repos. The BE session (A) may overlap any single FE session.

## Phase files

| File | Scope (item IDs) |
|------|------------------|
| `10_PHASE_A_BACKEND.md` | BE for: 1.1 CS-06(payload), CS-07/1.2 CS-03+CS-04(persistence), CS-11, FIX.03(gen), CS-21; 1.2 CS-05(data), CS-15(AI), CS-20(refresh), CS-24(values); todos repeats (1.1 FIX.01); pin sync (FIX.05/CS-19); check-in state (FIX.04); migrations |
| `20_PHASE_B_FE_VOICE.md` | 1.1 CS-01 (error card + pufferfish), CS-02 (iOS upload), CS-04 (transcript line) |
| `30_PHASE_C_FE_MAIN.md` | 1.1 CS-08, CS-09, CS-10, CS-11(UI), FIX.03(UI), FIX.04; 1.2 CS-01 (reminder open button) |
| `40_PHASE_D_FE_WORKSPACE_CORE.md` | shared P1/P2/P3 widgets; rename (1.1 CS-20 + 1.2 CS-02); 1.2 CS-04; Agenda (1.2 CS-06..CS-09, 1.1 FIX.02); Tematy i pytania (1.2 CS-05); Do zrobienia (1.1 FIX.01 + 1.2 CS-11..CS-13) |
| `50_PHASE_E_FE_WORKSPACE_MODULES.md` | Wątki (1.2 CS-14..CS-18); Realizations (1.2 CS-19 + 1.1 FIX.05); Goals (1.2 CS-20..CS-22); Therapy Relationship (1.2 CS-23..CS-25) |
| `60_PHASE_F_FE_TRIAGE_NOTIF_TIMELINE.md` | triage chips (1.2 CS-03 + CS-10, supersedes 1.1 CS-07 mechanics); notification deep-links (1.1 CS-06); Timeline summaries UI (1.1 CS-21 FE) |
| `70_PHASE_G_FINAL_QA.md` | full test suites, manual matrices, Done-when audit, deploy checklist |

## Global decisions log (binding for every phase — do not re-litigate)

1. **Fix.1.2 (2026-07-13) supersedes Fix.1.1 (2026-07-07) wherever they conflict.** Concretely:
   - Triage UI = **chip section appended at the bottom of output cards, grouped Tematy · Pytania · Wątki · Action pointy** (1.2 CS-03) — NOT per-item bookmark icons (1.1 CS-07). 1.1 CS-07's surviving intent: all 4 card types feed Workspace, nothing is lost from cards, triage works on later Timeline reopen.
   - Tematy/pytania route to the NEW module **„Tematy i pytania"** (1.2 CS-05) — NOT directly to Agenda. Agenda is user-curated via „Dodaj do agendy"/pin only (1.2 CS-06).
   - Agenda closed topics = **P2 archive „Twoje zakończone tematy"** (1.2 CS-07) — supersedes 1.1 FIX.02's inline "DONE section" idea. If the Agenda renders on more than one surface, the archive entry point exists on each surface, same data.
   - Do zrobienia: Done = **P2 archive „Zrobione"** (1.2 CS-11) — supersedes 1.1 FIX.01's inline „Pokaż zakończone" section. Row affordance = **3-dot menu** („Edytuj nazwę", red „Usuń") per 1.2 CS-12 — supersedes 1.1 FIX.01's pencil icon. **Repeats (1.1 FIX.01) survive**: repeat controls (Powtarzaj: Codziennie/Tygodniowo/Miesięcznie) live INSIDE the edit sheet (P1 prefilled, extended for todos).
2. If the code already contains a triage group for realizations/„Odkrycie" (shipped in MSV3.2 batch), keep it as an additional chip group routed to Realizations §4 (1.1 CS-07 mapping); the four 1.2 groups are mandatory.
3. Rename appears in both specs (1.1 CS-20 = 1.2 CS-02): one change — tab + section header + every string naming the section → PL **„Pracownia"** / ENG **„Workspace"**. Never rename copy where terapia/therapy means the therapy concept (e.g. „Therapy Relationship").
4. Red **„Usuń"** in any 3-dot menu = confirm dialog → permanent delete, NEVER archives.
5. Every new user-facing string ships **PL + ENG** (all 7 ARB locales must at least get the EN fallback value; PL and EN verbatim from spec).
6. Shared patterns P1 (add-entry bottom sheet with „Nagraj" STT), P2 (archive with badge + Przywróć), P3 (expand/collapse 5→+10) are **single shared widgets** built once in PHASE D and reused everywhere.
7. Do NOT touch: generated content of output cards above the chip section; check-in scoring/color-mapping logic; Agenda checkbox close behavior; Timeline history/ordering.

## Git & safety rules (every session, non-negotiable)

- Backend repo `MindSync/` → branch **main**. Frontend repo `mindsync-frontend/` → branch **dev**. Verify with `git status -sb` BEFORE committing.
- **Commit locally. NEVER push. NEVER run migrations against prod.** The operator pushes and runs `heroku run alembic upgrade head --app mindsync` after PHASE G. (FE push to dev triggers Codemagic → TestFlight — operator's call.)
- Stage ONLY files you touched (never `git add .` / `git add -A`).
- Migration chain: current single head = `zz6a7b8c9d0e` (agenda.kind). Any new migration must set `down_revision` to the CURRENT single head (verify — an earlier phase may have added one; check `alembic heads` equivalent by reading files). Migrations must be idempotent (prod drift). NEVER SQLAlchemy `Enum(PyEnum)` with inconsistent labels — use `String(n)` + constants.
- **Deploy ≠ migrate**: the 3 MSV3.2 migrations (`xx…`, `yy…`, `zz…`) may not yet be applied on prod. Do not assume prod schema; do not design code that crashes at boot if a table is missing (per CLAUDE.md Change Safety rules).
- SQLite tests ≠ Postgres: for any model/DDL change, compile DDL with the `postgresql` dialect offline or import the app.
- Pre-existing test baseline (2026-07-03): **21 BE + 30 FE failures are baseline, not your regression.** Record numbers before/after.
- Flutter: run `build_runner` after model changes and `gen-l10n` after ARB changes; **commit generated code**.
- Full CLAUDE.md "Change Safety & Impact Recon" applies to every change.

## Coordination files (same folder)

- `API_CONTRACT_Fix1.md` — PHASE A fills this in (final request/response shapes). FE phases D/E/F MUST read it before wiring API calls and MUST report any mismatch in STATUS.md instead of guessing.
- `STATUS.md` — every phase appends its report section when done (template inside). The next wave's session reads it first.

## Definition of done (whole batch)

Every item's own "Done when" from the two specs holds; both builds pass; `flutter analyze` no new errors; BE pytest no new failures vs baseline; PHASE G checklist signed off; STATUS.md complete with commits listed; deploy checklist ready for the operator.
