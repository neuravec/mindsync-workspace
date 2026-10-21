## PHASE A2 (data-analytics slice: A7, A8, A9, A10, A11, A13) — DONE — 2026-07-17

- Session commits (repo `MindSync/`, branch `main`, NOT pushed):
  - `c878e9f` — "MSV3.2Fix.1 A2: fix summaries raw-500, rewrite symptom narrative, expose therapy-relationship/notification contract fields" (15 files: 4 endpoint files, config.py, schemas.py, openai_service.py, 2 task files, 6 test files — 3 new, 3 minimal collateral fixes to pre-existing tests)

- Items completed (spec IDs):
  - **A7** (1.1 CS-21) — DONE. Fixed the raw-500: wrapped the previously-unguarded
    data-gather + row-creation "prep" phase of `/generate` and `/retry` (both
    `weekly_summaries.py` and `monthly_audits.py`) in try/except, always
    returning a structured error envelope (`error_code`/`message`/`retryable`,
    plus `summary_id`/`audit_id` when a row exists to retry). Also removed a
    plausible OpenAI structured-output schema hazard (bare Python
    `default=False` on both AI result models' `limited_data` field — now
    required, zero behavior change). Weekly prompt now explicitly answers
    "is my therapy approach working / better-worse-neutral" inside "This Week
    at a Glance"; monthly's Movement Assessment already covered this
    (audited). Auto-generation at period end audited and confirmed
    **already implemented** before this slice (`setup_hourly_weekly_therapy_summary`
    / `setup_monthly_therapy_audit`, hourly crons registered from
    `app/main.py` lifespan) — not re-implemented, just verified.
  - **A8** (1.1 CS-11 + FIX.03) — DONE.
    (a) Symptom score input audited — `POST /symptoms/{id}/scores` found
    fully functional, no backend bug. Flagged as likely FE gap.
    (b) Narrative content rewritten (`SYMPTOM_DESCRIPTION_PROMPT` in
    `config.py`, kept byte-identical in `openai_service.py`'s fallback copy)
    — bans point-deltas/history-recitals/add-a-note-suggestions, requires
    qualitative wording grounded in the user's own app data (new
    `_gather_recent_activity_context` helper feeds recent session/note
    topics into the prompt input).
    (c) `last_updated_at` added to `SymptomResponse`, `SymptomCardResponse`,
    `SymptomTrendItem`.
    (d) AI Summary "must actually generate" — added a one-time,
    cost-bounded event-driven bootstrap (`regenerate_mood_trend_summary_for_user`
    in `mood_trend.py`) fired only on a user's first-ever symptom score
    (no existing `MoodTrendSummary` row), so a new user no longer waits up
    to 24h for the daily-batch tick to see any summary. Steady-state daily
    cadence/cost for existing users is untouched.
  - **A9** (1.2 CS-20) — DONE (audit only). `POST /goals/{id}/refresh`
    already existed and already implements correct failure semantics
    (previous narrative preserved, row marked FAILED on AI failure). No code
    change needed; added a regression-lock test.
  - **A10** (1.1 CS-06) — DONE. Full live-notification-type enumeration in
    `API_CONTRACT_Fix1_A2.md` §9. Moments framework (11 active generator
    types) already routes every push through `/moment/{id}` — a prior fix
    (commit `12543e3`, before this slice), audited and confirmed correct,
    not re-touched. Added `recording_id` to the session-recording-ready
    payload (additive). Found and documented two **dead/unscheduled** code
    paths that still contain the generic-`/main-page`-route anti-pattern
    (`periodic_summary.py`'s daily/weekly/monthly/yearly jobs — never
    referenced by the Heroku Procfile or the scheduler setup module; and
    the post-session-nudge direct-send functions — superseded by the
    moments framework's `POST_SESSION_REFLECTION` generator in Notification
    Cadence v3) — left unfixed since they have zero production reachability,
    flagged in case either is ever resurrected.
  - **A11** (1.2 CS-24 + 1.1 FIX.04) — DONE. Per-check-in
    `relationship_state`/`state_label` audited — already exposed on every
    `HealthCheckResponse`; scoring/color logic untouched per spec. Added
    `should_show_main_prompt` to `HealthCheckStatusResponse`
    (`is_due AND NOT banner_dismissed`, live-computed every call). Audited
    the FIX.04 "doesn't dismiss" report and found **no backend
    caching/staleness bug** — both `is_due` and `banner_dismissed` already
    recompute from scratch on every request from the latest COMPLETED
    check-in; every submission path always ends COMPLETED (even on AI
    failure, which falls back to a canned observation). Documented the most
    likely explanations (FE not re-fetching status after submit; or, for
    voice submissions specifically, the CS-02 iOS transcription bug
    preventing a COMPLETED row from ever being created) for Phase C.
  - **A13** (1.1 CS-02 support) — DONE (read-only audit). See findings below.

- Items NOT completed / deviations + why: none. All six items delivered;
  A9/A11(part)/A10(moments part) turned out to already be implemented by
  prior work and are documented as audits rather than re-implementations —
  reported explicitly rather than silently marking done with no diff.

- API contract deviations (also reflected in `API_CONTRACT_Fix1_A2.md`):
  none structural — every change is an additive field or content-only
  rewrite; no endpoint path/method/existing-field changed shape.

- New migrations: **none**. No schema changes were required for any of A7,
  A8, A9, A10, A11, A13 — everything fits existing columns/tables. (A6's
  `TodoItem` recurrence-fields gap and A2/A3's storage-model gaps mentioned
  in `10_PHASE_A_BACKEND.md`'s "known gaps" section belong to the concurrent
  A1 agent's scope, not this slice.)

- Test results (before → after vs baseline 21 BE / 30 FE):
  - Targeted new/changed test files: all green
    (`test_fix1_summaries_error_envelope.py` 14/14,
    `test_fix1_mood_trend_symptoms.py` 17/17,
    `test_fix1_goals_notifications_therapy_relationship.py` 12/12,
    `test_symptom_description_prompt.py` rewritten + green,
    `test_symptom_analytics.py` / `test_monthly_therapy_audit.py` one-line
    collateral fixes + green).
  - Full suite (`python -m pytest app/tests/ -q`): **21 failed, 4371 passed**
    — identical failure count to the documented 2026-07-03 baseline (21 BE).
    None of the 21 failing tests touch any file this slice modified
    (spot-checked by name against `git diff --stat`). Re-run after the
    concurrent A1 agent's uncommitted Workspace/therapy_tracking changes
    were present on disk (not committed by me) — same count, so no
    cross-agent interference observed at test-run time.
  - Boot safety: `python -c "import app.main"` verified clean (with `rq`
    mocked in `sys.modules` to work around the unrelated, pre-existing
    Windows-only `multiprocessing` fork-context limitation that also affects
    every existing test file via their `_ensure_rq_importable()` helper —
    not present on Heroku/Linux).

- Manual QA still needed (device/platform):
  - A8(a): manually verify on-device (Android + iOS) that Main's Mood Trend
    widget actually calls `POST /symptoms/{id}/scores` when a score is
    entered — this agent found no backend bug, so if scores still can't be
    added after Phase C's UI work, the issue is very likely still FE-side
    (or a genuinely new finding to report back).
  - A11: manually verify the weekly check-in prompt dismisses on Main
    immediately after a text/quick submission (should already work per the
    live-computation audit) vs. after a voice submission (may still be
    blocked by the CS-02 iOS bug until Phase B's fix lands — re-test after
    that ships).
  - A7: since this agent could not hit the live OpenAI API (no live
    experiments per project rules), **please manually smoke-test "Generate
    Now"** on weekly and monthly summaries against a real account after
    deploy, and check Heroku logs for the new `exc_info=True` tracebacks if
    it still errors — the structured envelope will now at least surface the
    real `error_code` client-side instead of a bodyless 500.

- Notes for next phases (Phase C, D/E, F):
  - **API_CONTRACT_Fix1_A2.md** has the full, final shapes for §5-§9 —
    read it before wiring any of: symptoms/mood-trend, weekly/monthly
    summary error handling, goals refresh, therapy-relationship values +
    Main prompt gating, and the notification type→payload table.
  - Phase C (Main): use `should_show_main_prompt` from
    `GET /health-check/status` to gate the CS-08 "Therapy relationship
    prompt" module — re-fetch status right after a successful check-in
    submission rather than relying on a pre-submission cached copy.
  - Phase F (notifications): the moments-framework `/moment/{id}` routing
    is already correct for all 11 active generator types — no FE work
    needed there beyond confirming the resolver handles it (it already
    does, per `notification_route_resolver.dart`, audited read-only).
    `session_recording_ready` also already resolves correctly to the
    Timeline tab; `recording_id` is now available in the payload if a
    future precision-routing pass wants it.
  - Phase F (Timeline summaries UI): build against the new structured error
    envelope in §6 of `API_CONTRACT_Fix1_A2.md` — `detail` is now always a
    dict with `error_code`/`message`/`retryable` on failure, never a bare
    string.

---

### A13 audit findings — for PHASE B (FE voice, iOS upload fix)

Scope: audited `app/api/v1/endpoints/audio_v2.py` and
`app/api/v1/endpoints/session_recordings.py` (both single-shot `/upload` and
chunked `/upload/initiate` + `/upload/{id}/chunk` + `/upload/{id}/complete`)
for anything that would reject iOS uploads specifically. **Read-only — no
code changes made**, per the phase assignment (PHASE B owns the fix).

**No content-type/MIME whitelist rejection found anywhere.**
- `audio_v2.py::/transcribe` — no content-type check at all; accepts any
  `UploadFile` regardless of extension/MIME.
- `session_recordings.py::ChunkedUploadInitiateRequest.content_type` — plain
  `str = "audio/m4a"` default, **no pattern/regex/whitelist constraint** —
  any string iOS sends (e.g. `audio/mp4`, `audio/x-m4a`, `audio/aac`) is
  accepted as-is.
- `session_recordings.py::/upload` (legacy single-shot) — `audio.content_type`
  is only used as a **fallback label** passed to durable GCS storage
  (`audio.content_type or "audio/m4a"`), never validated/rejected against a
  whitelist.

**Zero-byte / undersized handling — deliberate, not a bug, but worth knowing:**
- All three upload surfaces explicitly reject `len(bytes) == 0` with a clear
  400 ("Empty audio file" / "Empty chunk body") rather than silently
  accepting and failing downstream — this is correct defensive behavior,
  not the source of a silent iOS failure.
- The legacy single-shot `/upload` **additionally** rejects anything under
  50 KB (`"Audio file too small (...). The recording may not have saved
  correctly."`) — this is a **deliberate anti-corruption guard sized for
  full therapy-session recordings** (~4.8 MB expected for 10 min at 64kbps
  AAC-LC), not iOS-specific — it would equally reject a too-short Android
  recording. The chunked path's `/complete` endpoint applies the identical
  50 KB floor against the client-declared `total_bytes`. **If any
  *shorter, legitimate* voice-note feature (not full session recordings)
  reuses either of these code paths, this floor would reject valid short
  notes on both platforms equally** — worth checking Phase B's target
  feature isn't accidentally routed through the session-recording upload
  path if it's meant to support sub-6-second notes.
- **Session state**: chunk upload requires `status == IN_PROGRESS` (409
  otherwise), rejects out-of-order chunks with a clear 409 + resume offset
  (not a silent drop), and `/complete` is idempotent (safe to call twice).
  Nothing here looks platform-specific.

**Conclusion**: this agent's backend-side audit found **no server-side
gate that would explain "ANY iOS voice recording immediately errors that
it can't be uploaded"** while Android and manual text work fine. Given the
symptom is "immediate" (fails before/during upload, not after), and no
content-type or size gate on the backend would trigger differently for iOS
vs Android given identical bytes, the root cause is most likely **client-side**
(iOS audio session / recording format producing a file the client itself
can't attach correctly, or a request-construction difference on iOS — e.g.
missing `Content-Range` header, wrong multipart boundary, or the file never
actually being captured before the upload call fires). Recommend Phase B
instrument the exact HTTP request iOS sends (headers + body size) at the
point of failure and compare directly against a working Android request to
the same endpoint — the backend audit did not find anything to fix on this
side.
