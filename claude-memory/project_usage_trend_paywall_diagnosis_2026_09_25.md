---
name: project-usage-trend-paywall-diagnosis-2026-09-25
description: "Diagnoza 25.09 - MAU spada (211->111 maj->wrz), paywall prawie niewidoczny, auto-trial 4d ukrywa bramki, gotowe popupy triala nigdy nie wolane; raport growth-analyst"
metadata:
  node_type: memory
  type: project
  originSessionId: 7668fffa-d4eb-47c7-9605-a84f1b1336d5
  modified: 2026-09-25T11:43:29.674Z
---

Raport `analytics-reports/2026-09-25-usage-trend-and-paywall-exposure.md` (growth-analyst, PostHog + kod; prod DB NIE odpytany, bo odmowa uprawnien, skrypt w scratchpadzie sesji).

- Teza operatora "uzycie rosnie" = w wiekszosci FALSZ: MAU 211 (maj) -> 111 (wrz), nowi 213 -> 101; rosnie tylko intensywnosc na osobe. Skok eventow/osob w PostHogu od sierpnia to joby backendu, nie ludzie.
- Paywall: 16 wyswietlen w calej historii, 5/127 aktywnych w 30d.
- Glowna przyczyna: auto-trial 4 dni dla kazdego konta (`_create_initial_subscription(uid, 4)`, `signup_trial`) wylacza bramki i paywall, a 71% userow nie wraca od 4. dnia. `TrialPopupManager` (powitanie, oferta $5/14d, trial-ended -> paywall) istnieje, ale nic go nie wola. Darmowi nie dobijaja do limitow, wiec zaostrzanie limitow nie pomoze.
- Luki w pomiarze: brak `trial_started`/`trial_ended`, `subscription_tier` pusty u ~72%.

Pomiar ekranu wyboru glos/tekst (18.09): sesje 9->27/tydz, te same 7 osob; `reflect_mode_selected` 125 vs 44 wyswietlen (podejrzenie wielokrotnego odpalania); `voice_interrupted` zero razy. Raw: `analytics-reports/raw/2026-09-25-reflect-mode-picker-post-deploy.md`.

**Why:** baza pod decyzje o paywallu i trialu.
**How to apply:** przed zmiana paywalla/trialu czytaj ten raport; ponowny odczyt retencji 2026-10-25. Powiazane: [[project-reflect-entry-batch-2026-09-18]], [[project-trial-paywall-block-fix-2026-08-18]].
