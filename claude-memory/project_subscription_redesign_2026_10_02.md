---
name: project-subscription-redesign-2026-10-02
description: Redesign subskrypcji + onboardingu + liczniki limitow; WDROZONE 2026-10-03 (BE main f5ea34d = Heroku, FE dev 02f8d0b = TestFlight), bez migracji; otwarte device-QA + prawnik przed sklepami; spec + raporty w design-specs/2026-10-02-subscription-onboarding/
metadata:
  node_type: memory
  type: project
  originSessionId: 11ef1d1a-7b6d-4b0b-b417-08a34feccc91
  modified: 2026-10-02T22:30:09.195Z
---

Operator zatwierdzil 2026-10-02 projekt z canvasu https://claude.ai/artifact/6ajEsLgFccV8oZkvEwP2Cp i kazal wdrazac end2end. Zrodlo prawdy: `design-specs/2026-10-02-subscription-onboarding/` (SPEC.md, copy-en.md, screens/, audit-design-logic.md, audit-posthog.md, audit-security.md, posthog-coverage-client.md, qa-regression.md).

Stan 2026-10-03: WDROZONE na polecenie operatora: BE commit f5ea34d na main (PUSHED = deploy Heroku, bez migracji), FE commit 02f8d0b + merge 69825df na dev (PUSHED = TestFlight przez Codemagic). Wczesniej branch `feat/subscription-onboarding-redesign`. QA GO: BE 6088/6097 (9 fail = baseline main), FE 2821/2847 (26 fail = baseline dev), analyze 0 errors. Security: 0 crit, H-1/H-2 FIXED; M-3 (korelaty statusu terapii w eventach PostHog: total_steps, prompt_variant) = PARTIAL, wymaga prawnika PRZED wydaniem do sklepow, nie przed TestFlight. Device-QA i prawnik (M-3) nadal otwarte przed wydaniem do sklepow.

Decyzje: trial serwerowy 4 dni zostaje; oferta po onboardingu = starter $5 "Extend to 2 weeks" (domyslnie) + Annual + Monthly, tylko przy aktywnym trialu, raz na konto; limity Free/mies.: Before 1, After 1, Between Sessions 3, Reflect 15, nagrania 2 lacznie, habity 1; paywall przy 0 = bramka kliencka (BE zapisuje plain_text), takze z powiadomien; logo = Orka; zdanie "Most of our users feel like they got a second therapy session" VERBATIM; ownership eventow zakupu BEZ zmian (filtrowac $lib); trial_ended tylko po zgodzie (hourly job), trial_started przed zgoda zaakceptowane; premium_source "starter_pack" nowe (stare buildy pokaza paywall takim userom = OK); paywall trial-ended takze dla triali zakonczonych <=30 dni przed updatem.

Deploy: BE push main = natychmiastowy deploy, bez migracji; FE push dev = TestFlight. Backlog: usage ledger (M-1, migracja), lock M-2, rate limit, refundy sklepowe, 19 Low z audytu designu, 16 vs 18 lat w copy, device-QA (zakupy, push dialogi, tz).

**Why:** paywall widzialo 5/127 aktywnych, trial konczyl sie po cichu, zero ekranu personalizacji ([[project-usage-trend-paywall-diagnosis-2026-09-25]]).
**How to apply:** przed commitem/pushem wymagana zgoda operatora; po deployu posthog-data-extractor potwierdza, ze nowe eventy plyna. Nazwy funkcji wg [[feedback-feature-truth-from-frontend]]; reguła PostHog [[feedback-posthog-instrumentation-mandatory]].
