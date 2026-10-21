---
name: project-character-tab-redesign-2026-05-18
description: "Character (Postać) tab full UI redesign — Pet Hero / Bio / Activity cards, shipped 2026-05-18"
metadata: 
  node_type: memory
  type: project
  originSessionId: de2aeab2-04a0-48ec-9696-40044a940aec
---

Character tab redesigned from the "MindSync Bio" handoff (UI_fixes/MindSync_Bio_handoff). Done 2026-05-18.

**Product decisions (user-confirmed):** single level shown = orca/pet track only (user track dropped from this screen, backend still has both); no "See all activity" link.

**Backend (additive, no migration):**
- `CharacterCardResponse.activity_breakdown`: list of 5 `ActivityBreakdownItem{key,count,xp}` — keys symptom_checkins/reflect_conversations/between_session_notes/session_summaries/prep_cards. xp = count × real per-occurrence award constant from crud.py `ORCA_TRACK_POINTS`/`USER_TRACK_POINTS` (1/2/1/3/3). symptom has 3/day cap so xp is an intentional approximation.
- `LevelingResponse.orca_points_in_current_level` + `user_points_in_current_level` — exact in-bracket XP (crud helper `points_in_current_level`); fixes the wrong `total % remaining` progress-bar math (orca thresholds are non-uniform).

**Frontend:** new widgets `pet_hero_card.dart`, `bio_card.dart`, `activity_card.dart`, `mimik_orca.dart`; new Freezed `ActivityBreakdownItem`. Old `dual_leveling_section/interaction_stats_section/orca_companion_section/personal_bio_section.dart` DELETED. Mood badge derived frontend-side from `orcaHappiness` (≥0.85 Thriving / ≥0.6 Resting / ≥0.3 Settling / else Sleepy). Bio share/refresh moved into a kebab menu. `refreshBio()` polls (5×3s) instead of blind delay. 41 character-tab tests pass; build done after [[project-clinician-portal-integration-2026-05-15]]-era work.

Reviewed by ui-ux-designer: 5 Critical/High accessibility blockers (48dp touch targets, shimmer-not-spinner loading, screen-reader semantics) — all fixed. Not yet deployed.
