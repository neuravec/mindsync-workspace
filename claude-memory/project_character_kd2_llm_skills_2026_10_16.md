---
name: project-character-kd2-llm-skills-2026-10-16
description: "Character KD v2: karta postaci, mapa i umiejętności generowane przez LLM z treści (emocje, wpisy, terapia) zamiast z aktywności; propozycja w artefakcie 16.10, NIE wdrożona"
metadata:
  node_type: memory
  type: project
  originSessionId: 3db298d3-320b-4d06-a645-197780005c6a
  modified: 2026-10-17T07:55:07.277Z
---

16.10 operator zlecił zmianę logiki zakładki Character: umiejętności, drzewko (mapa), statystyki i rekomendacje mają wynikać z tego, o czym osoba mówiła, pisała i co poruszała na terapii, a nie z aktywności w apce. W trakcie dopisał: drzewko i skille generowane dynamicznie przez LLM na bazie odkrywania własnych emocji.

Stan: propozycja w artefakcie https://claude.ai/artifact/1T46tjjRbva5YaEL2M5hRF, strona Character, rząd „Kierunek KD v2” (plansze KESheet, KEMap, KESkill, KEStep, KEEarly + KELogic i KELLM dla zespołu, notatki n_kd2_*). KD v1 (wdrożone 14.10, logika z liczników w app/services/character_sheet.py) zostało jako punkt odniesienia. Nic nie zaimplementowane.

Kluczowe decyzje projektu v2: „LLM nazywa i grupuje, kod liczy” (etapy Discovered/Practicing/Growing/Yours, mocne strony i poziom liczy kod z momentów z dowodami); promienie = rodziny emocji nazwane słowami osoby; każda umiejętność ma ukrytą kotwicę z ram DBT/ACT/CBT/samowspółczucie (bezpieczeństwo + analityka bez treści); mocne strony zostają stałym zestawem 6 (do potwierdzenia); Orka dalej rośnie z aktywności.

Iteracja 16.10 (uwagi operatora, wersja 68): główna karta ma zostać w układzie v1 (bohater z radarem, wejście w mapę, zakładki Stats, Skills, Tools), BEZ podziału na okresy 30 dni / 3 miesiące / cały czas i BEZ osobnej sekcji „Light ideas for this week”. Pomysły żyją w zakładce Skills przy wybranej umiejętności, obok „Next” (reguła etapu liczona kodem: co przybliża kolejny etap i poziom), max 3 aktywne, z „Why this” i „Not now”. Operator: „Poza tym wszystko OK”.

Iteracja 2 (16.10, wersja 69): usunięty „Simple view” (operator: bez sensownej funkcji) i podpis pod kartą; teksty UI po humanizerze; jasna paleta operatora zamiast ciemnych kart (zob. [[feedback-artifact-design-rules-darek]]). Tools = metody radzenia sobie, których osoba faktycznie UŻYŁA, wyłapane z treści (z terapii albo własne), z „For: ścieżka”, źródłem i ostatnim użyciem; metoda tylko zaproponowana przez terapeutę zostaje pomysłem przy umiejętności, dopóki nie zostanie użyta.

Iteracja 3 (17.10, wersja 71): operator: „chujowo kolorystycznie”. Plansze KE przepisane na paletę aplikacji (MsColors) z kolorami tylko jako akcent, mapa jednokolorowa z nazwami emocji na promieniach, „Not now” w nagłówku pomysłu. Wysokości: KE1 1490 (inne zakładki przewijają się w ramce), KE2 1586, KE3 1764, KE4 844, KE5 1420.

**Why:** v1 liczy aktywność, a operator chce karty o człowieku i jego pracy z emocjami.
**How to apply:** przy wdrożeniu najpierw sama ekstrakcja momentów za wyłącznikiem i zestaw jakości offline, potem UI; blokery: prawnik PROFILING i security-guardian (model czyta treść). Otwarte pytania w notatce n_kd2_open. Powiązane: [[project-redesign-cards-workspace-character-2026-10-13]].
