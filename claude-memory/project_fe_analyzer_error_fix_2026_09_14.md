---
name: project_fe_analyzer_error_fix_2026_09_14
description: FE "nie kompiluje sie" 2026-09-14 = jedyny error analizatora w tescie (stale sync mock addCustomSession); fix d3ba054 PUSHED dev 2026-09-15
metadata:
  type: project
---

**Co:** Operator zglosil 2026-09-14, ze frontend "sie nie kompiluje". Diagnoza: lib/ kompilowal sie normalnie; jedyny error-level issue analizatora byl w `test/screens/main_tab/widgets/session_setup_screen_test.dart` (mock `addCustomSession` odpowiadal synchronicznie, a od 41ffb03 / MSV3.11 CS-10 metoda zwraca Future<void> -> `body_might_complete_normally`). IDE swiecilo na czerwono 11 dni, release build nietkniety.

**Stan:** commit d3ba054 (fix w 1 linii, test-only) PUSHED na origin/dev 2026-09-15 (cbe89e7..d3ba054). `flutter analyze` 2026-09-15: 137 uwag, 0 error. Sesja z 14.09 padla przed zapisem pamieci, stan odtworzony z git.

**Why:** Czerwone IDE przez error w tescie wyglada jak brak kompilacji – zanim szukasz problemu w lib/, filtruj `flutter analyze` po `error •`.

**How to apply:** Przy zgloszeniu "nie kompiluje sie" najpierw `flutter analyze | grep "error •"`, potem `flutter build`/`git status`. Zobacz [[feedback_stale_read_after_compaction]] i [[reference_frontend_ci_git_topology]] (push dev = TestFlight).
