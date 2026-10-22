---
name: project-loops-comms-process-2026-10-21
description: "Programy maili Loops P1-P9 + holdout + webhook do PostHog: WDROŻONE i WŁĄCZONE 22.10 (BE v580 + m321e4c5a6b7, workflowy Active); otwarte weryfikacja pierwszych zdarzeń, M-3 prawnik"
metadata:
  node_type: memory
  type: project
  originSessionId: 806b2eae-f552-4d9b-b485-ad2d9da6085c
  modified: 2026-10-21T22:19:18.301Z
---

21.10 Mikołaj zlecił proces komunikacji Loops (doc dla Darka https://claude.ai/artifact/D62cGuX3Muu9SaFFg49ajU, makiety https://claude.ai/artifact/CAFirna19ZHZ59J95Yo9b7), a potem "wykonaj end2end całość i włącz na loops". Kontrakt: `email/lifecycle-2026-10/SPEC.md` (w workspace), copy w `copy/`, ID wszystkiego w Loops w `loops-build.json`.

Stan 22.10 ok. 00:20 (+0200), wdrożył Claude na polecenie Mikołaja:
- Backend: `feat/loops-lifecycle` ff do main 13a5e6e, Heroku v580, migracja m321e4c5a6b7 uruchomiona (3 tabele). QA GO (zero nowych faili vs main), security DEPLOY OK (`security-reports/2026-10-21-loops-lifecycle.md`).
- Heroku config: EMAIL_LINK_SECRET, LOOPS_WEBHOOK_SECRET (z panelu Loops), LOOPS_LIFECYCLE_ENABLED=true. LOOPS_EXCLUDED_EMAILS puste.
- Loops: webhook na `/api/v1/webhooks/loops` włączony (Contacts, Email sending, Email events), test event 200. Aktywne: P1, P2, P3a, P3b, P3b cisza, P4, P5 Wygaśnięcie, P6a, P6b, P9. P5 Rezygnacja zostaje Draft (subscriptionCancelled niewykrywalne bez App Store Server Notifications / Google RTDN). Wstrzymane stare: Onboarding mailing list, INACTIVE SURVEY 2 WEEKS, No Note Reminder, Survey + Calendly (dzień 2 kolidował z P3a). Freebie PDF zostaje Active. P7 to szkic kampanii, każdy numer ręcznie (Monika, /blog-write).
- Joby: `mindsync_hourly_email_lifecycle_trial_ending` (:25), `mindsync_daily_email_lifecycle` (10:00 UTC).

22.10 rano (sprawdzenie): webhooki działały (3746 odbiorów, 115 kontaktów dopasowanych do kont, 45 ze zgodą), Loops wysłał P1 x1, P3b x2, P3b cisza x1, ale do PostHog nie doszło żadne `email_opened`: zadania RQ lifecycle nie wołały `flush_posthog()` (work horse kończy się os._exit). Poprawka 6a9f856 (v581, 08:34 +0200), pierwsze `email_opened` w PostHog potwierdzone. Zdarzenia sprzed poprawki (ok. 21.10 22:00 do 22.10 06:34 UTC, w tym otwarcia kampanii z 21.10) w PostHog przepadły, stan otwarć jest w `email_contact_state`. Każde nowe zadanie RQ z capture PostHog musi kończyć się flush_posthog w finally.

Otwarte: M-3 (podstawa prawna marketingu, Art. 9) do prawnika, backlog Low L-2/L-4/L-5/L-7/L-8, skrzynki darek@ i monika@ muszą przyjmować odpowiedzi.

**Why:** pętla komunikacji stała na braku zdarzeń z aplikacji; teraz zdarzenia płyną, a holdout 10% pozwala zmierzyć efekt (powrót w 72 h).
**How to apply:** awaryjnie wyłączyć `heroku config:set LOOPS_LIFECYCLE_ENABLED=false -a mindsync` (zero zapisów do Loops). Nie wznawiać starych workflowów bez decyzji, bo dublują P1/P2/P6. Powiązane: [[reference-loops-access-2026-10-21]], [[feedback-chrome-tool-js-only-env]], [[project-email-new-look-2026-10-21]].
