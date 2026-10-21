---
name: project-loops-comms-process-2026-10-21
description: "Propozycja procesu komunikacji mailowej Loops end-to-end z pętlą feedbacku (21.10); doc dla Darka, czeka na 7 decyzji, nic nie wdrożone"
metadata:
  node_type: memory
  type: project
  originSessionId: 806b2eae-f552-4d9b-b485-ad2d9da6085c
  modified: 2026-10-21T16:41:50.585Z
---

21.10 Mikołaj poprosił o pełny proces komunikacji przez Loops z pętlą feedbacku, oparty na stanie obecnym i niezależnym researchu, w dokumencie dla Darka. Doc (Claude Docs): https://claude.ai/artifact/D62cGuX3Muu9SaFFg49ajU. Udostępnić Darkowi musi Mikołaj przyciskiem Share, Claude tego nie zrobi.

Stan na 21.10 (odczyt Loops API i kodu):
- Backend nie wysyła do Loops żadnych zdarzeń (`loops_client.py` nie ma sendEvent). Działa tylko nocny sync ok. 40 cech (`tasks/loops_sync.py`).
- Żadnej zgody marketingowej: typ MARKETING jest w modelu, ale nikt go nie zbiera ani nie sprawdza.
- Działające automaty: 10-mailowy onboarding, ankieta po 13 dniach nieaktywności (licznik liczy od rejestracji, więc poszła do ok. 1740 osób), Survey+Calendly, No Note Reminder (temat nie pasuje do treści). Szkice nigdy nie włączone: Win-back 3/7/14, First-value, Trial ending.
- 10 ostatnich kampanii: łącznie 24 kliknięcia na ok. 1700 wysyłek każda, 80-93 soft bounce co wysyłkę.

Propozycja: 9 programów (6 wyzwalanych zdarzeniami), metryka główna = powrót do aplikacji w 72 h względem holdoutu 10% (`email_holdout`), webhooki Loops do PostHog, wspólna skrzynka na odpowiedzi z tagami, retro po 7 dniach. Plan: Porządki, Pomiar, Automaty, Rytm (ok. 7 tygodni, terminy proponowane).

**Why:** obecne wysyłki nie dają mierzalnego efektu, a cała pętla stoi na braku zdarzeń z aplikacji.
**How to apply:** nie wdrażać nic przed decyzjami Darka z sekcji "Decyzje dla Darka". Faza 1 to zmiany w backendzie i FE, więc obowiązuje recon zmian i instrumentacja PostHog. Powiązane: [[reference-loops-access-2026-10-21]], [[project-email-new-look-2026-10-21]].
