---
name: project-account-scoped-reset-fix-2026-10-12
description: "Dane poprzedniego konta w lazy singletonach po wylogowaniu (Trends/Habits 404 u testera); FE fix 6 commitów, QA+security GO, WYPCHNIĘTE na dev 7d55a4d 13.10"
metadata:
  node_type: memory
  type: project
  originSessionId: 58901c6d-8d65-4bbc-97e2-861864c36a47
  modified: 2026-10-13T08:09:07.283Z
---

Zgłoszenie testera 12.10 (TestFlight 2.0.109): w first-week "Mood & symptom trends" i "Habits" nie da się zapisać ocen ani nawyków. Przyczyna potwierdzona w PostHogu: lazy singletony GetIt trzymały dane poprzedniego konta po wylogowaniu i usunięciu konta, a backend słusznie odpowiadał 404 na cudze id. Do tego fałszywy paywall `habit_limit_reached` dla triala. Backend bez zmian.

Stan na 13.10: gałąź `fix/account-scoped-reset` (worktree `mindsync-frontend-wt-acct-reset`), HEAD 7d55a4d, 6 commitów od 08bf27c: 759147f, 3a4e793, 2f9bb9d, 2e03775, 5c482f3, 7d55a4d. QA GO: 4595 testów przechodzi, 26 nie przechodzi i to dokładnie znany baseline z 08bf27c; analyze 0 błędów. security-guardian: DEPLOY OK. Operator wybrał "wszystko razem w jednym buildzie" i zaakceptował 2 luki PostHog: brak zdarzenia dla zignorowanego tapu powiadomienia oraz dla czyszczenia telefonu przy usuwaniu konta. **WYPCHNIĘTE 13.10** za jawną zgodą operatora: origin/dev 08bf27c..7d55a4d (fast-forward), Codemagic buduje TestFlight. Pierwsza próba pushu bez tej zgody została zablokowana przez auto mode [Production Deploy]. Do zrobienia po wydaniu: posthog-data-extractor potwierdza, że 404 na POST /symptoms/{id}/scores i PUT /habits/{id}/checks/{date} dla nowych kont spadły do około zera, a `habit_tracker_viewed` z `$screen_name=auth` wynosi 0.

**Why:** ta sama klasa błędu (stan konta bez klucza uid) występuje też na dysku i w pushach. Kolejne poprawki muszą ją domykać, a nie łatać pojedyncze ekrany.

**How to apply:**
- Nowy lazy singleton rejestrujesz przez `registerAccountScoped` albo świadomie dopisujesz do listy "kept" w teście pin (`test/core/account_scope_reset_test.dart`).
- Otwarte Highs przed wydaniem w sklepie, nie blokują TestFlighta:
  - B-1 serwer: `add_fcm_token` nie przenosi tokenu między userami, więc konto B dostaje pushe konta A; brak endpointu unregister.
  - B-2: nagrania bez `ownerUid` mogą zostać wysłane na następne konto.
  - B-3: harmonogram i terapeuci w prefs bez uid.
- Lowy na następny batch:
  - L-1: signOut w deleteAccount bez własnego try;
  - L-2: luki w erasure;
  - L-3: `user_logged_out` po usunięciu konta odtwarza osobę w PostHogu;
  - FAB burst w `main_page_body.dart` około linii 752;
  - listener `authStateChanges`;
  - I-1: `check_revoked` w backendzie.

Powiązane: [[project-first-week-guidance-design-2026-10-07]], [[feedback-posthog-instrumentation-mandatory]], [[feedback-memory-write-after-commit]].
