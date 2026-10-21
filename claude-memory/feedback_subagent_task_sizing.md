---
name: feedback-subagent-task-sizing
description: "Nie dawaj subagentom zadań >45-60 min — dziel na małe taski i puszczaj kilku agentów równolegle (worktree) z krokiem integracji, albo task-by-task"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5541cd49-a520-473a-99d6-c1a653b80bb4
---

Operator (2026-07-17, batch MSV3.2 Fix.1): faza E jako JEDEN agent flutter trwała >1h07 — „takie wielkie zadania zwiększają ryzyko usterek. Powinieneś dzielić na zadania i puszczać np. kilku flutter agentów równolegle i potem ew. integracja. Albo task by task."

**Why:** długi pojedynczy agent = rozmyty kontekst pod koniec pracy, większe ryzyko błędów i długi feedback loop; małe zadania są tańsze w weryfikacji i retry.

**How to apply:** przy orkiestracji faz implementacyjnych celuj w taski ~20–40 min na agenta. Gdy taski są rozłączne plikowo tylko częściowo (np. wspólne ARB/l10n/generated we Flutterze) — używaj `isolation: "worktree"` w tool-u Agent i po zakończeniu zrób krok integracyjny (merge do dev, rozwiązanie konfliktów ARB, re-run gen-l10n/build_runner, analyze + testy). Gdy zależności są sekwencyjne — task-by-task, każdy agent z wąskim scope i własnym raportem. Duży „fazowy" agent tylko wyjątkowo. Related: [[feedback-concurrent-session-git-hygiene]], [[project-msv32-fix1-phase-plan-2026-07-17]].
