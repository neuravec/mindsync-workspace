---
name: project-main-tab-redesign-2026-10-14
description: "Propozycje redesignu zakładki Main (MA Next step, MB Today, MC Compact hub) na stronie \"Main\" artefaktu designu; czeka na wybór kierunku"
metadata:
  node_type: memory
  type: project
  originSessionId: b6586333-3dd5-492d-905d-2c19866da247
  modified: 2026-10-14T18:35:21.018Z
---

14.10 operator poprosił o przemyślane propozycje redesignu zakładki Main. Strona "Main" w artefakcie https://claude.ai/artifact/1T46tjjRbva5YaEL2M5hRF (wersja 62): plansze Teraz (MNow, MNowFirstWeek, MNowAfterSession, MNowEmpty) oraz MA/MB/MC Home+States (klikalne). Źródła: audyt `scratchpad/cards/main-audit.md`, opis kierunków `scratchpad/cards/main-proposals.md` (sesja b6586333), dane `analytics-reports/raw/2026-10-14-main-tab-usage.md`. Skrypt dodający stronę: `scratchpad/cards/add_main.py`.

Rekomendacja: MA "Next step" (karta według stanu sesji, bez backendu, wysiłek M) z dodatkami z MB i MC. MB wymaga backendu planu po dniu 7 (L).

Naprawy niezależne od redesignu (flutter-mobile, czekają na zgodę): odwrócony trend obszarów (isPositive=false w unified_symptom_module.dart), podtytuł po sesji, "No session this week" bez terapeuty, myślnik w info_mainTabBody, ok. 11 zapytań na wejście, kontrast, martwy getting_started_card_tapped.

**Why:** Main ma słabe użycie (5% pierwszych akcji z Main, 35% sesji bez akcji, 45 osób/30 dni).
**How to apply:** po wyborze kierunku iterować wybrany (zob. [[feedback-design-iterate-chosen-direction]]); nowe wydarzenia PostHog z notatki n_m_measure są częścią zakresu.
