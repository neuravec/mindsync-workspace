---
name: project-first-week-followup-fix-2026-10-22
description: "Naprawa follow-up 404, fałszywego first_week_plan_failed, 401 w tle i rage clicków po wydaniu 2.0.117; WDROŻONE 23.10: BE v585 (cfddb06), FE 30a1bc1 na dev"
metadata:
  node_type: memory
  type: project
  originSessionId: e638dcd8-2c46-4beb-ba6a-ae3a728012be
  modified: 2026-10-23T05:24:48.927Z
---

22-23.10.2026, Mikołaj zlecił naprawę 3 błędów z przeglądu PostHog po wydaniu 2.0.117 (Android b188 od 19.10, iOS b184, w App Store jako "2.0.56", od 20.10 18:24 UTC).

Przyczyny (dowód: PostHog + prod DB + archiwum logów Papertrail):
1. follow_up 404: `/first-week/steps` daje krokowi talk CTA follow_up od dnia 0, a resolver follow-up (stary plan_engine) w dniu 0 zawsze nie ma kroku. Fix BE: pytanie ogólne, `quoted:false`, gdy steps oferuje follow-up. FE: przy 404 otwiera nowy wątek Reflect, nowe zdarzenie `follow_up_unavailable`.
2. first_week_plan_failed u konta bez first week: serwer dawał 204 w 8 ms (logi), a klient po zerwanym połączeniu keep-alive nadpisywał "brak planu" błędem. Fix FE: 204 zostaje "none" mimo późniejszej porażki; GET plan/steps ponawiany raz po martwym gnieździe. Hipoteza 401 okazała się fałszywa dla tego konta.
3. iOS 401 w tle: zegar Main odpytywał w tle z wygasłym tokenem. Fix FE: jedno ponowienie po 401 z odświeżeniem tokena przypiętym do uid (security FE-M1 zamknięte), zegar staje w tle, blokada wielokrotnego tapu w TherapyFlowLauncher.
Do zdarzeń doszły `failure_reason` i `http_status`.

Raporty: `db-reports/2026-10-22-first-week-followup-404.md`, `security-reports/2026-10-22-first-week-followup-auth-retry.md`, raw `analytics-reports/raw/2026-10-22-*` (fix-timelines zawiera UID-y, nie commitować).

Logi: Papertrail to teraz SolarWinds Observability; wejście przez SSO dodatku (`heroku addons:open papertrail`, wymaga zalogowanego Heroku w Chrome); wyszukiwarka sięga kilka godzin, godzinowe archiwa JSON ok. 2 dni (pole `logmsg`). Token z `heroku config` API odrzuca (403).

**Why:** stan wdrożenia i otwarte punkty do weryfikacji.
**How to apply:** po buildzie TestFlight/sklepie posthog-data-extractor ma potwierdzić: `follow_up_failed` not_found spada do 0, pojawia się `reflect_session_started` seed_source=first_week_followup z nowego Main, `first_week_plan_failed` ma `failure_reason`. Backlog: FE-L2 (ponowienie bez responseType), flaky izolacja testów BE w jednym procesie. Zob. [[project-release-2-0-117-review-2026-10-21]].
