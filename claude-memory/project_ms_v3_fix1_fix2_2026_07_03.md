---
name: project_ms_v3_fix1_fix2_2026_07_03
description: "MS v3 fix1 (13 CS) + Fix.2 (restore Goals w Stats) — FE PUSHED dev, BE COMMITTED lokalnie (push→operator)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e80f5da0-e4ed-44bb-bc57-8758873b6b93
---

Batch 2026-07-03 wg speców `Business_requirements/MS_3/ms v3 fix1.md` + `MSV#.1_Fix.2 .md`. Pełny raport: `Business_requirements/MS_3/RAPORT_wykonania_fix1_fix2_2026-07-03.md`.

- **FE PUSHED `origin/dev`**: `293d5b6` (fix1: renamy PL/EN, TherapyFlowLauncher, AddSessionSheet na pustym kafelku sesji, view_source z Main, persystencja pustego wątku Reflect + reconcile-on-load, toLocal() w reflect_thread_tile, checkmarkColor chipa, usunięty voice fast-path → zawsze submit-voice/Whisper, „Twoje odpowiedzi" bez zwijania, „Prep cards") + `83054e3` (Goals restore w Stats z `3464457^`, trim: usunięty tylko `_GoalRelatedDataRow`; Main bez Goals; TreatmentGoals nietknięte). Codemagic → TestFlight + Play internal (auto-rollout od c26353c).
- **BE COMMITTED lokalnie na `main`**: `e7d729c` (CS-10: HEALTH_CHECK_PROMPT + opis `observation` + fallbacki 7 jęz. → 4 akapity; sekcja porównania score'ów tylko przy historii; prompt-only, env-override na Heroku potwierdzony NIEustawiony) + `a4d661f` (LEGACY_CLEANUP_MS3.md: wiersz D-01 /goals/* ANULOWANY). Push na main DENIED przez klasyfikator → **operator: `git push origin main` + `git push heroku main`** (bez migracji; Heroku było na v515=Cadence v3, więc deploy = tylko CS-10).
- QA GO: BE 4055 pass/23 fail (pre-existing/flaky, stash-A/B), FE 944 pass/30 fail (=baseline), analyze 0 err.

**Kluczowe ustalenia techniczne** (do reuse): CS-11+CS-12 to jeden widget (`HealthCheckResultCard` obsługuje pełny i quick check-in); „Therapy Relationship" = subsystem health-check (`/api/v1/health-check`, NIE conversations); backend zawsze zwracał pełny transkrypt w `open_ended_response` przy submit-voice; lazy-create wątku Reflect nadal odrzucony (voice mode); goals data layer sesji terapii = SharedPreferences + mirror PUT /users/therapy-schedule.

**RE-FIX po TestFlight QA (2026-07-04, PUSHED dev `a5fd523`):** CS-07 wróciło — root cause: backend stempluje `last_message_at` przy TWORZENIU wątku Reflect (sortowanie), więc warunek reconcile `lastMessageAt==null` był nieosiągalny; pustość = tylko `lastMessagePreview==null`. + sąsiedni bug: wiadomości GŁOSOWE (AudioChatCubit→ReflectManager bezpośrednio) nie czyściły flagi fresh-empty → exit mógł skasować wątek z treścią; fix w refreshMessages(). CS-05 wróciło — GettingStartedCard zasłaniał pusty kafelek sesji; teraz kafelek promowany nad Getting-Started (`shouldPromoteNextSessionCard`) + AddSessionSheet ZASTĄPIONY pełnoekranowym hub-and-spoke `SessionSetupScreen` (wzorzec PersonaPicker).

Powiązane: [[project_ms3_batch_2026_07_02]], [[reference_pre_existing_test_baseline_2026_06_01]], [[feedback_concurrent_session_git_hygiene]]
