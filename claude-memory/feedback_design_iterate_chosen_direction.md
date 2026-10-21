---
name: feedback-design-iterate-chosen-direction
description: "Po wyborze kierunku designu dopracowywać i iterować go aż będzie idealny, zamiast zostawiać jedną wersję"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b6586333-3dd5-492d-905d-2c19866da247
  modified: 2026-10-13T18:57:44.322Z
---

Gdy w artefakcie designu (np. canvas "MindSync: karty, Workspace, Character", https://claude.ai/artifact/1T46tjjRbva5YaEL2M5hRF) operator albo zespół wybierze kierunek, nie kończę na jednej poprawce. Wybrany kierunek dopracowuję i iteruję (kolejne wersje plansz, stany brzegowe, spójność z resztą apki, uwagi z komentarzy), aż będzie idealny.

**Why:** operator powiedział 2026-10-13, po wyborze kierunku A dla kart Before/After: "jak kierunek będzie wybrany to masz dopracowywać i iterować póki nie będzie idealnie".

**How to apply:** po decyzji o kierunku (w komentarzu z END albo w rozmowie) sam proponuję i robię kolejne iteracje tego kierunku: brakujące plansze (np. After w tej samej wersji co Before, stany pusty/ładowanie/błąd/limited data/plain_text/failed), dopasowanie do realnej zawartości i funkcji z kodu, spójność tokenów. Odrzucone kierunki zostawiam na kanwie z notatką, nie rozwijam ich. Komentarze bez END dalej traktuję jako szkice (zob. monitor komentarzy).

Widoczność pracy: operator chce, żeby ludzie widzieli, że jeszcze pracuję. Nowych komentarzy w artefakcie nie da się zakładać (ArtifactComments tylko czyta, odpowiada i zamyka wątki przekazane do Claude'a), więc przy każdej iteracji aktualizuję niebieską kartkę statusu na kanwie („CLAUDE PRACUJE”, godzina, gotowe / teraz / następnie), a w wątkach przekazanych do Claude'a odpisuję krótko, co zmieniłem.

Kartka statusu musi być zawsze prawdziwa (operator 2026-10-13: „pilnuj statusu, bo zespół nie wie, co się dzieje”). „CLAUDE PRACUJE” tylko gdy faktycznie coś robię; po skończeniu tury zmieniam na „GOTOWE DO PRZEGLĄDU” z listą: zrobione, otwarte, na co czekam. Aktualizuję ją w tym samym publishu co zmiany w planszach, z godziną.
