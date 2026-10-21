---
name: project-personal-bio-cost-optimization-2026-05-19
description: Personal Bio (Character tab) — cost optimization of the most expensive AI op; data_hash cache + partial regen + cooldown
metadata: 
  node_type: memory
  type: project
  originSessionId: 4d1e275a-e90c-47fb-bc5f-246565f44f9e
---

Personal Bio generation (Character tab) was the single most expensive OpenAI operation in the app, per cost analysis. Root cause: `generate_personal_bio()` re-sent a full 365-day window of therapy data as input tokens on EVERY call, regenerated all 5 sections at once, and had no content-based cache (only a 6h time guard).

Optimization pack A–E shipped 2026-05-19 (100% additive, not deployed):
- **A — data_hash cache**: migration `nn4o5p6q7r8s` added `recent_data_hash` + `history_data_hash` columns to `personal_bios`. `crud.compute_bio_data_hash(data)` = stable SHA-256. If both hashes match latest COMPLETED bio → skip AI entirely. Same pattern as Therapy Tracking Signal / Period Snapshots.
- **B — section split**: if only recent (14d) data changed → call new `openai_service.generate_bio_progress_section(...) -> str` (cheap, 14d input only) for Progress, carry over Patterns/Drivers/Style/Outlook from previous bio. Full `generate_personal_bio` only when history hash changed.
- **C — history window**: 365d → 90d in `app/tasks/personal_bio.py`.
- **E — restyle on tone change**: `generate_single_personal_bio(user_id, reason="tone_change")` calls new `openai_service.restyle_personal_bio(previous_bio, tone, ...) -> PersonalBioResult` — rewrites existing 5 sections in new tone, sends NO therapy data. Falls back to full gen if no prior COMPLETED bio.
- **D — refresh cooldown**: `POST /gamification/character_card/refresh_bio` returns existing bio (200) if last COMPLETED bio < 24h old, no PENDING record, no enqueue.

Two new prompts in openai_service.py: `BIO_PROGRESS_SECTION_PROMPT`, `RESTYLE_BIO_PROMPT` (both with `settings.` override fallback). New Pydantic model `BioProgressResult`.

Tests: `app/tests/test_personal_bio_cache.py` (backend-api, 63 combined pass) + 19 in test_character_tab.py (data-analytics). Pre-existing unrelated failures: 4× `TestShouldGenerateToday`.

See [[reference-next-wave-plan-v3]]; relates to [[project-character-tab-redesign-2026-05-18]].
