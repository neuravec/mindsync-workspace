---
name: project-msv33-cs11-cs13-batch-2026-08-14
description: "MSV3.3 CS-11 (backend generation half, topics-to-questions across 4 AI cards) + CS-13 (prep card mood section rebuild) — data-analytics track, COMMITTED-pending (not committed as of last check)"
metadata: 
  node_type: memory
  type: project
  originSessionId: b9676365-4ed7-41a2-8c69-40415833f008
  modified: 2026-08-14T17:40:42.371Z
---

Backend repo (`MindSync/`), branch main. Concurrent with a backend-api agent
(schema half: `SessionDebrief.therapist_questions` / `SessionRecording.
therapist_questions`, migration `ll3m4n5o6p7q` = new head) and an unrelated
CS-10 recording-duration fix agent (touched `app/tasks/session_recording.py`).

## What shipped (data-analytics files)

- `app/services/openai_service.py`: `SessionCardResult.open_threads` and
  `RecordingSummaryResult.topics_with_timestamps` deprecated (always `[]`
  for new cards, code backstop + prompt instruction); both gained
  `therapist_questions: List[str]` (cap 3, code backstop). `EnhancedPrepCardResult
  .suggested_agenda` deprecated (force `[]`); `.emotional_temperature`
  deprecated (force `[]`) — CS-13 rebuilds this section via a NEW, separate
  method `generate_prep_card_mood_section(symptom_histories, recent_debriefs,
  between_session_notes, ...)` that reuses `generate_symptom_description()`
  (the exact Mood Trend pipeline) per tracked symptom, returning
  `SymptomMoodItemOutput{symptom_name, description}` — no scores, no
  onboarding data (structurally impossible: the method has no such param).
  `AgendaSuggestionOutput.kind` narrowed `Literal["topic","question"]` →
  `Literal["question"]` (schema-enforced, not just prompt). `generate_recording_summary`
  was ALSO canonicalized (dropped `settings.SESSION_RECORDING_SUMMARY_PROMPT`
  override, mirroring the CS-11/FIX.03 precedent) so the new Questions
  section can't be shadowed by a stale Heroku env var.
- `app/crud/crud.py`: `gather_prep_card_context` gained `symptom_score_histories`
  key — per tracked symptom, `{symptom_name, score_history_text}` windowed
  to the period since `last_session_date` (falls back to full history if the
  window is empty). Feeds `generate_prep_card_mood_section` directly.
- `app/tasks/triage_proposals.py`: stopped emitting `kind="topic"` candidates
  from `open_threads`/`suggested_agenda`/`topics_with_timestamps`/
  between-session `agenda_suggestions` non-"question" items. Debrief and
  recording's new `therapist_questions` now route as `kind="question"`
  (mirrors prep card's existing `therapist_questions` route). Historical
  topic data on old cards is untouched — this only stops NEW candidate
  creation on resync.
- `app/api/v1/endpoints/debriefs.py` + `session_recordings.py`: full
  decode/response wiring for `therapist_questions` (`_debrief_to_response`,
  `_recording_to_response`); debrief ALSO gets the persist half
  (`_process_debrief_ai`, isolated separately-committed step, mirrors the
  action_items/breakthroughs pattern elsewhere).
- `app/api/v1/endpoints/prep_cards.py` + `app/tasks/prep_card_auto_generate.py`:
  both call `generate_prep_card_mood_section` and persist into the
  EXISTING `emotional_temperature` column with the NEW shape (no
  model/migration change — it was already an opaque encrypted-JSON blob).

## Two flagged gaps NOT fixed (out of file grant — reported to lead)

1. **`app/tasks/session_recording.py::_save_summary_sections`** needs one
   line: `recording.therapist_questions = encode(json.dumps(summary.
   therapist_questions)) if summary.therapist_questions else None`
   (mirror the existing `topics_with_timestamps` line right next to it).
   This file was NOT in this task's file grant (owned by whoever is doing
   the CS-10 duration fix concurrently) and is where the recording
   pipeline's generation→persist actually happens — `session_recordings.py`
   only has the read/decode side. Until this line lands, `therapist_questions`
   is generated correctly but never reaches the DB for recordings (debrief's
   round trip IS complete — same file owns both halves there).
2. **`app/schemas/schemas.py::EmotionalTemperatureItem`** requires
   `current_score: int` (not Optional). The CS-13 rebuild persists
   `{symptom_name, description}` (no score) into the same
   `SessionPrepCard.emotional_temperature` column — `EmotionalTemperatureItem(**e)`
   will raise on the new shape, and `_prep_card_to_response`'s existing
   broad except swallows it to `None`. Content is generated/persisted
   correctly now (no regeneration needed later) but won't reach the API
   response until backend-api updates this schema class (pure Pydantic
   change, no migration — the column is just an encrypted JSON blob).
   `prep_card_widget.dart:1260` also needs a Flutter-side rebuild (currently
   renders `current_score`/`trend` with a trend icon; borrows
   `_PrepSection.unresolvedTopics` as a placeholder header enum since there
   was never a dedicated section for this one) — flutter-mobile work,
   sequenced after the schema fix.

## Tests

New file `app/tests/test_msv33_cs11_cs13_generation.py` (23 tests, all
green) covers: deprecated-fields-empty + question-cap backstops for
debrief/recording, `_debrief_to_response`/`_recording_to_response` decode
round trip (the specific thing a coordinator message flagged as easy to
miss — persistence isn't proof the client sees it), triage candidate
kind-filtering for all four cards, `AgendaSuggestionOutput` kind rejection,
mood-section generation (per-symptom, skips incomplete entries, never
fabricates, structurally can't see Focus Area data), and
`gather_prep_card_context`'s new `symptom_score_histories` key against a
real SQLite-backed DB fixture.

Also had to update 3 pre-existing test files whose assertions encoded the
now-superseded OLD topic-generation behavior: `test_between_sessions.py`
(2 tests: `kind="topic"` used to be valid, now rejected), `test_msv32_fix2_cards.py`
(3 tests: debrief prompt section count 5→6, "never fabricate one" count
3→2 since open_threads is now unconditionally-empty rather than
never-fabricate, and the old "topics capped at 3" wording is gone). All
fixed to assert the new CS-11 contract instead of deleting coverage.

Targeted suite run (not full 8.5-min suite, per task instructions): 487
passed / 0 failed across every file touched + every consumer test file
found via grep (debriefs, session_recordings, between_sessions, prep_cards,
prep_card_overhaul, prep_card_auto_generate x2, triage_proposals,
triage_extraction_hooks, recording_summary_prompt, msv32_fix2_cards,
cs11_therapist_questions_migration [backend-api's migration test],
msv33_backend_migrations, plus the new file).

[[feedback_stale_read_after_compaction]]
