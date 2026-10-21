---
name: reflect-v31-therapy-progress-2026-10-13
description: Reflect v3.1 (branch feat/reflect-therapy-progress, NOT pushed 2026-10-13): progress questions answered from user data + PROGRESS SNAPSHOT; voice-mini and eval gotchas learned
metadata:
  type: project
---

Operator 2026-10-13: Reflect said "that's for you and your therapist" when asked how therapy is going. Fix = reflect-v3.1: section HOW THEY ARE DOING in `reflect_prompt.py`, LIMITS line softened to "no verdict on therapy/method/therapist", new deterministic `app/services/reflect_progress.py` (PROGRESS SNAPSHOT block in WHAT YOU KNOW ABOUT THEM, ~13 queries per text turn / voice session / /start event). Eval in `design-specs/2026-10-13-reflect-therapy-progress/eval.md`.

**Why:** operator wants a useful answer from the user's own record; verdict on therapy stays banned.

**How to apply / non-obvious lessons:**
- Root cause was TWO lines, not one: LIMITS "Never judge their therapist or say whether their therapy is working" AND the advice rule ("belongs with their therapist, then ask what they'd say to them"). gpt-realtime-2.1-mini files "should I stop therapy?" under the advice rule unless it is explicitly excluded there; even then voice needed a line in EVERY SPOKEN TURN (end of prompt) to stop deflecting.
- Adding a "answer from their data" section made the model talk progress inside a crisis message and state 112 (assumes country, breaks SAFETY). Fixed by a carve-out bullet referencing SAFETY "rule by rule, its rule on phone numbers included" without editing the approved SAFETY text. Any future data-forward section needs the same carve-out + an S7-style crisis eval.
- Security round (commit 7f8f5b6): wording in a data-forward section that MENTIONS phone numbers or tells the model to ask "are you safe" made gpt-5.4-mini state 112 in 4-6/24 crisis replies (old 0/24). Ablation proved it; final gate says only "nothing from the record, stay with them". Never paraphrase SAFETY rules elsewhere in the prompt. Prompt-only gating did not stop PL passive ideation from citing the record (8/8 -> 4/8); a deterministic snapshot drop on the text path (`message_signals_distress(data.text)`) got it to 0/8. Measure crisis with 24 text runs (cheap, ~0.05 USD), 8 is too noisy.
- Model called a 2-month record "thin" until the thin criterion was made concrete (< ~2 weeks or few entries).
- Voice eval: Python 3.12 has websockets 12 (`additional_headers` TypeError) -> run `scripts/reflect_eval.py` / `reflect_progress_eval.py` with `py -3.14`. Unit tests on `py -3.12`.
- `conversation_topic_emotions` has no user column and possibly no index on conversation_id (unverified on prod): the emotion aggregate is cached 6h in Redis via `orca_memory._redis_call` (timeouts + back-off). Ask database-administrator to check `pg_indexes` before trusting latency.
- Git Bash heredoc in this environment can turn `\\n` in a Python heredoc into a real newline: write edit scripts with the Write tool.
- Open (operator): voice PL "is my therapist good?" still deflects without data (2/2); voice progress answers ~37 words vs 20-word rule.

Related: [[project-reflect-prompt-rewrite-2026-09-18]], [[release_2026_07_01_lista_poprawek]]
