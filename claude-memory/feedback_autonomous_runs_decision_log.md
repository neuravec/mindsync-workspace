---
name: feedback-autonomous-runs-decision-log
description: Przy długich wdrożeniach operator chce pełnej autonomii; decyzje podejmuję sam i na końcu spisuję je w raporcie
metadata:
  node_type: memory
  type: feedback
  originSessionId: b6586333-3dd5-492d-905d-2c19866da247
  modified: 2026-10-13T19:48:12.923Z
---

Gdy operator zleca długą pracę (np. wdrożenie e2e przez zespoły agentów) i mówi „ma być autonomicznie do końca”, nie zatrzymuję się na pytania. Każdą potrzebną decyzję podejmuję sam (najbezpieczniejsza rozsądna opcja, odwracalna, za flagą gdy ryzykowna) i zapisuję ją, a na końcu daję listę: decyzja, dlaczego, jak cofnąć.

**Why:** operator 2026-10-13: „Jeśli gdzieś będzie potrzebna jakaś decyzja to podejmuj sam i na koniec spisz jakie były podjęte. Ma być autonomicznie do końca.”

**How to apply:** dalej obowiązują twarde granice (bez pusha, deployu, migracji na prod, usuwania danych) chyba że operator wprost na nie pozwolił; to nie są „decyzje do podjęcia samemu”, tylko rzeczy do zostawienia gotowych dla operatora. Zob. [[project-redesign-cards-workspace-character-2026-10-13]].
