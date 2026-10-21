---
name: feedback-agents-stop-on-background-jobs
description: "Subagenty kończą turę \"czekając\" na run_in_background (analyze/test) i nigdy nie dostają wyniku – w promptach zakazuj background jobs i wymagaj commitu+raportu w tej samej turze; pełny flutter test tylko per katalog"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 10c5e5c1-4e6d-4f4b-a3e0-6d7562a0b2be
  modified: 2026-09-02T09:52:36.066Z
---

Obserwacja z MSV3.11 (2026-09-02): 6 z 9 subagentów (Flutter i backend) zatrzymało turę z komunikatem "czekam na background flutter analyze/pytest" – zatrzymany subagent NIE dostaje notyfikacji o zakończeniu zadania w tle, więc lead musiał każdego wznawiać SendMessage'em (czasem 3 razy), tracąc po 10-20 min na agenta.

**Why:** run_in_background w subagencie + "poczekam" = martwy punkt; tylko lead dostaje task-notification. Dodatkowo na tej maszynie (16 GB, kilka worktree'ów Flutter równolegle) pełny `flutter test` jednym poleceniem zawiesza się / OOM (osierocone `flutter_tester`/`dart` po 3-4 GB), a `flutter analyze` trwa 1-3 min.

**How to apply:**
- W każdym prompcie subagenta: "nigdy nie kończ tury z wiszącym run_in_background; analyze/testy w pierwszym planie z timeout do 10 min; commit i raport w tej samej turze".
- Flutter: testy per katalog/plik, `--concurrency=2`, nigdy dwa procesy flutter naraz; przed retry ubij osierocone procesy starsze niż 20 min. Pełną suitę zostaw Codemagic / qa-testing per katalog.
- Backend: pełna suita ~10-24 min (zależnie od obciążenia) – lead może ją puścić w tle sam (dostaje notyfikację), agent nie.
- Gdy agent zatrzyma się na "czekam": wznów jednym SendMessage z twardą listą kroków i "end your turn only with the final report".

Related: [[feedback-subagent-task-sizing]], [[project-msv311-threads-reflect-grace-batch-2026-09-02]].
