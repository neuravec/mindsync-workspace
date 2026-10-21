---
name: project-release-2-0-117-review-2026-10-21
description: "Przegląd PostHog + prod po wydaniu 2.0.117 (redesign) w sklepach, 21.10: stabilnie, n=7, głos 0 startów, stary build iOS bez ART9"
metadata:
  type: project
---

21.10.2026 (Mikołaj zlecił): 6 agentów posthog-data-extractor (adopcja, błędy, onboarding, zachowanie, monetyzacja, aktywność) + database-administrator. Raport: `analytics-reports/2026-10-21-release-2-0-117-review.md`, raw `analytics-reports/raw/2026-10-21-release-*.md`, `db-reports/2026-10-21-ios-google-signup-stuck.md`.

Stan: 2.0.117 (Android b188 od 20.10 02:12, iOS b184 od 21.10 07:49 UTC realnie); 7 realnych osób; 0 wyjątków Darta, 0 nowych sygnatur. Otwarte: 0 voice_chat_started na 2.0.113-117 (test na urządzeniu), zakup na 2.0.117 niezweryfikowany, stary build iOS (prawdopodobnie iOS<16) zakłada ~30 kont/2,5 tyg. bez onboardingu i ART9 (9 rozmawia bez zgody), Main odpytuje /health-check/latest ~52x/os/7d, 5xx backendu nie trafiają do PostHog, iOS bez notification_opened. Onboarding 10-19.10: 83% ukończenia, rozmowa w 24h 62%. DAU spada od początku października, wydanie bez skoku.

**Why:** baseline dla powtórek i lista otwartych problemów po wydaniu.
**How to apply:** powtórki 23.10 (48h po mailu Loops) i 28.10 z tymi samymi filtrami (wykluczenie testerów po osobie, 92 osoby). Lejki licz bez kont legacy. Zob. [[project-posthog-multi-angle-2026-10-15]], [[project-email-new-look-2026-10-21]].
