---
name: write-project-memory-after-commit-not-after-intent-to-commit
description: "Memory zapisany \"IMPLEMENTED, pending deploy\" gdy realnie kod nie był nawet committed → memory rozjeżdża się z rzeczywistością. F1-F5 onboarding fix 2026-04-29 jako case study."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dc69bc9d-1cbe-403f-a209-03b7adc35779
---

**Rule**: Project memory o stanie implementacji ("IMPLEMENTED", "READY TO DEPLOY", "SHIPPED") wolno pisać DOPIERO po weryfikacji że artefakty są w git i na disku. Sama deklaracja agenta "I implemented X" lub user mówi "OK ship it" nie wystarczy.

**Why**: 2026-04-29 zapisałem `project_onboarding_reopen_fix_2026_04_29.md` ze statusem "IMPLEMENTED, pending deploy" — pakiet F1-F5 z 55 testów. 28 dni później (2026-05-27) próbując wrócić do tematu okazało się że:
- `lib/widgets/onboarding_error_view.dart` — nie istnieje
- `test/screens/therapy_onboarding/onboarding_views_cta_visibility_test.dart` — nie istnieje
- F1 splash retry overlay — brak `_resolveError`, `_retryResolve`, `splash_resolve_failed` w kodzie
- F4 UID-scoped SharedPrefs — brak `u_{uid}_therapyOnboardingCompleted`, `_migrateOnboardingKey`
- F5 `if (!keyboardOpen)` antywzorzec — WCIĄŻ obecny w 3 views
- Tylko `TherapyOnboardingError` state class faktycznie wylądował

Praca zaginęła między agent runs, między pull/rebase, lub w bufferze edytora. User zapytany "co planowaliśmy z onboardingiem" — moja memory dała mu pewność że coś jest IMPLEMENTED gdy realnie nie było.

**How to apply**:
1. Po zakończeniu implementacji przez agenta, ZANIM zapiszę memory: `git status` + `git log -1` + spot-check kluczowych plików per `Read`/`Grep`.
2. Status w memory używaj poziomów: PLANNED → IN_PROGRESS → COMMITTED (in git, locally) → MERGED (in dev/main) → DEPLOYED (in prod).
3. Jeśli agent kończy bez commit'a, status = IN_PROGRESS. Memory zapisz, ale wyraźnie zaznacz że pliki są tylko w worktree.
4. Dla feature memory: link do commit SHA jeśli istnieje, nie tylko nazwa branchy.
5. Project memory o "deployment readiness" pisz po `git log dev | head` weryfikacji że relevant commits są na branch.

**Trade-off**: zapisanie memory zaraz po sesji ma wartość (kontekst świeży). Niech będzie — ale ze statusem PLANNED/IN_PROGRESS, nie IMPLEMENTED. Status promote'uj dopiero gdy widzisz dowód.
