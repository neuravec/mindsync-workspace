---
name: known-bugs-2026-02-23
description: Analytics/summaries audit findings from 2026-02-23 — TTS_MODEL config bug, key-order bugs, N+1 queries, missing else branches.
metadata:
  type: project
---

Audit findings (status as of 2026-02-23, verify still-present before relying on):

- CRIT: `settings.TTS_MODEL` does not exist -- config has `TTS_HD`. Fix in `openai_service.py` line 165.
- CRIT: `generate_yearly_summaries` uses `replace_dict_keys` with positional zip on GPT JSON -- key order not guaranteed.
- CRIT: `generate_monthly_summaries` crashes if user has no UserPreferences.
- CRIT: `rq_queue` imported AFTER use in `summaries.py` line 499.
- CRIT: `emotional_intensity` endpoints missing `return` before early-exit schema construction.
- HIGH: `get_time_scope()` has no else branch -- `UnboundLocalError` for any n_days not in {7,30,90}.
- HIGH: `BEHAVIOR_EMOTION_COMPOSITION` calls `compute_emotion_composition` instead of `compute_behavior_emotion_composition`.
- HIGH: `generate_monthly_charts_for_all_users` uses current month dates, not previous month.
- HIGH: N+1 queries in emotion pie/composition/behavioral functions.
- HIGH: Day-by-day loop queries in timeline/profile functions.
- OBS: Actual summary jobs live in `app/services/periodic_summary.py` and `app/services/chart_explanations.py`, NOT in `app/tasks/`.
