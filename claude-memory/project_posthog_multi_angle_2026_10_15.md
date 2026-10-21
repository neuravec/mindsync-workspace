---
name: project-posthog-multi-angle-2026-10-15
description: "Analiza PostHog z 8 kątów (15.10.2026) + synteza growth-analyst; baseline lejka, P1 higieny danych, terminy powtórki"
metadata:
  node_type: memory
  type: project
  originSessionId: a633f018-aec3-4994-a197-2b7114d8f765
  modified: 2026-10-15T18:44:31.334Z
---

15.10.2026: 8 agentów posthog-data-extractor (zmiany, błędy, pozyskanie, onboarding, retencja, konwersja, churn, funkcje/głos) + synteza growth-analyst w `analytics-reports/2026-10-15-posthog-multi-angle.md` (raw w `analytics-reports/raw/2026-10-15-*.md`).

Baseline: 296 nowych/60d, onboarding ukończony 24%, R14 10%; MAU ścisłe ~80; rdzeń 12-15 powracających/tydz. Redesign 03.10: onboarding 47%->74%, rozmowa w 24h 14%->42%; retencji jeszcze nie ocenić. Zmiany 09-15.10 tylko na TestFlight. Kupujący: tylko Postgres jest prawdą.

**Why:** punkt odniesienia dla kolejnych pomiarów i lista P1 higieny danych (podwójne zakupy klient+backend, dev backend z Windows pisze do prod PostHog, brak zdarzeń wygaśnięcia/anulowania, rozbita tożsamość 26%, brak first_week_plan_shown, pushe podsumowań do całej bazy, FirebaseAuthException Android).

**How to apply:** powtórki 10-17 (aktywacja 7d), 10-29 (R14 od 03.10), 11-02 (D30), 14 dni po wejściu 2.0.109+ do sklepu. Równoległe agenty: każdy w osobnym podkatalogu scratchpada (nadpisywały sobie pliki). Zob. [[feedback_posthog_instrumentation_mandatory]].
