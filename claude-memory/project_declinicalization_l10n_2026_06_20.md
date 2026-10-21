---
name: project_declinicalization_l10n_2026_06_20
description: MDR de-clinicalization wording + legal fixes shipped to FE dev; concurrent-tree contamination handled; what was excluded
metadata: 
  node_type: memory
  type: project
  originSessionId: 67f1e7a4-aa2e-46e5-8ee4-c5312e494e7b
---

De-clinicalization / medical-wording + legal fixes from handoff `translation_fixes/MINDSY_1.DOC` (a .docx despite the .DOC extension). Source extracted to `translation_fixes/MINDSY_1_md.txt`; full verified change spec at `translation_fixes/CHANGES_SPEC.md`.

**SHIPPED** — commit `f2a2433` (merge `1b15a1a`) PUSHED to `origin/dev` 2026-06-20. Localization layer ONLY: EN + PL value changes across app_en/pl.arb (~150 keys), 8 new soft-topic preset keys in all 7 ARBs, regenerated `lib/l10n/generated`, `lib/utils/symptom_presets.dart` (17 clinical presets incl. Suicidal Ideation / Panic attacks → 8 soft topics: Low mood, Unease, Overwhelm, Worries, Stress, Sleep, Loss, Focus), + `add_symptom_sheet_test.dart` string update. `flutter analyze` 0 errors. Other 5 langs (de/fr/nb/sv/es) got ONLY the 8 preset keys; their reframed *values* are a deferred follow-up (doc Part XIV). Disclaimer / Terms "No Medical Advice" / crisis strings left UNTOUCHED.

**⚠ LEGAL FLAG (blocks release):** `onboarding_gdprConsent` reworded "mental health-related data" → "wellbeing and reflection data". De-clinicalizes UX but may weaken the **Art. 9 GDPR** special-category basis. Needs lawyer sign-off BEFORE production release. Pushing to `dev` triggers Codemagic auto-versioning (saw tag `app_2.0.50` + incoming "Pre-release updates" bump) — hold the actual store release until legal confirms. Related: [[project_onboarding_profiling_plan_2026_05_27]] (pre-existing GDPR/Art.9 work).

**ALSO SHIPPED — doc-requested feature changes** (commit `6541248` on dev, after user said "podejmuj decyzje, chcę gotowca"): removed notification intensity/frequency controls (Part XIII — `settings_cubit/state/freezed`, `notifications_section.dart`; the 5 restored `notifSettings_intensity*`/`_recommended` ARB strings are now unused-but-harmless) and removed onboarding journey "frustration" chips/text (screen #5 — `onboarding_journey_view.dart`, `therapy_onboarding_cubit.dart`; backend frustration_chips/text stay nullable). 9 files, tests updated, validated 0 analyze errors in an isolated worktree.

**Concurrent-session gotcha (the hard part):** a SECOND session was live the whole time doing the voice-note fix ([[project_voice_note_dataloss_fix_2026_06_19]]) — it committed `6491660` and **switched the shared checkout to branch `fix/voice-note-dataloss` mid-work**. My feature commit accidentally landed on THEIR branch on top of their voice commit. Recovery without disturbing their live WIP: `git worktree add <tmp> dev` → `cherry-pick` my commit onto dev → analyze → push dev → remove worktree; then `git reset --soft 6491660` + `git restore --source=6491660 -- <my 9 files>` to peel my stray commit off their branch (touching only my 9 files, never their voice files). Their working tree (audio_chat/debrief_capture/splash/recording_pipeline_v2 + ~17 new voice-recovery l10n keys/regen, all uncommitted) left fully intact.

Lessons: (1) on a shared tree another session may touch, NEVER bulk `git add .` — classify every file (git key-set diff per ARB, mtime, diff content) and stage only yours by explicit pathspec; (2) a concurrent session can switch the branch under you — re-check `git branch --show-current` before every commit; (3) to move a misplaced commit off a live-contended branch, use an isolated worktree for the cherry-pick + push, never `checkout`/`reset --hard` the shared tree. See [[feedback_memory_write_after_commit]].
