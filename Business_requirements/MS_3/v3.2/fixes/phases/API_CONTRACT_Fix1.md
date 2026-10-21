# MSV3.2 Fix.1 — API contract (BE ↔ FE) — INDEX

> The contract is FINAL and lives in the fragment files below (written by the backend
> implementation agents). FE phases (C/D/E/F) MUST read the relevant fragments before wiring
> any API call. If reality differs from a fragment, STOP wiring that piece and record the
> mismatch in your STATUS_<phase>.md instead of guessing.

| Sections | File | Author slice |
|----------|------|--------------|
| §1 lifecycle/archives (agenda, todos, threads, topics&questions) · §2 triage chips (`GET /workspace/triage/{type}/{id}/chips`, `POST /workspace/triage/{id}/toggle`) · §3 agenda feeds/tags/pin-sync + thread statuses · §4 todos repeats (`repeat_freq` + `TodoCompletion` log, lazy rollover) + homework/today · §10 session schedule + **NEW `GET /therapy-tracking/session-state`** (CS-09 state machine, server-computed) | `API_CONTRACT_Fix1_A1.md` | A1 (commits 4c5759d, b1f29f7, 3cd6682, 3b0a93b; migration **aa2b3c4d5e6f**) |
| §5 symptoms/mood-trend (score input, `last_updated_at`, narrative rules, AI-summary bootstrap) · §6 weekly/monthly summaries (error envelope `error_code`/`message`/`retryable`; auto-gen already cron-wired) · §7 goals refresh · §8 therapy relationship (ratings; **`should_show_main_prompt`**) · §9 FULL notification type→payload table | `API_CONTRACT_Fix1_A2.md` | A2 (commit c878e9f) |
| §7-addendum: Goals lifecycle (complete/archive „Zakończone cele"/restore/delete) | `API_CONTRACT_Fix1_A3.md` | A3 (gap-closing slice; see STATUS_A3.md) |

Notes:
- Goals lifecycle was a gap between A1/A2 ownership — closed by slice A3; if `API_CONTRACT_Fix1_A3.md`
  is missing, A3 is still running: Phase E must wait for it before wiring CS-21.
- Archive badge counts ("closed since archive last opened") are FE-computed unless a fragment says otherwise.
- Migration head after this batch: check `alembic/versions` (A1 added `aa2b3c4d5e6f` on top of `zz6a7b8c9d0e`;
  A3 may add another). NONE applied on prod — operator runs `alembic upgrade head` at deploy time.
