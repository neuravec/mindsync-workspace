---
name: project-notification-ai-cost-cut-2026-09-13
description: "Cięcie kosztów AI powiadomień – bramka premium + naprawa pętli renderowania re-engagement, DEPLOYED v549"
metadata: 
  node_type: memory
  type: project
  originSessionId: f2d2ea51-45eb-41a9-b25a-e5b820d1faa8
  modified: 2026-09-13T09:47:21.926Z
---

2026-09-13: commit `bc6ee9c` na main, **DEPLOYED Heroku v549**, wszystkie 3 dyna up, zero błędów bootu, BEZ migracji.

Trzy zmiany w jednym deployu, wszystkie w `MindSync/app/services/`:

1. **Bramka premium na AI** – `is_ai_notification_eligible(db, user_id)` na wejściu `generate_moment_text()`, rzuca `AIGenerationNotEligibleError`. Wszystkie 7 generatorów już łapało wyjątek i wracało do zlokalizowanego szablonu, więc zero zmian logiki w generatorach. Druga ścieżka `_generate_nudge_text` w `notification_service.py` zabramkowana osobno. Fail-closed przy braku `db`.
2. **Naprawa pętli re-engagement** – `_count_re_engagement_moments_since()` wykluczała EXPIRED i DISMISSED, więc po wygaśnięciu pusha licznik cofał się z 1 na 0, `push_number` wracał na 1, `dedup_key` był identyczny (bo `last_activity_date` nieaktywnego usera się nie zmienia) i orchestrator płacił za render AI co godzinę, bez końca. Wada od pierwszego commita `aded542e` (2026-05-20), nie regresja. Licznik jest teraz monotoniczny.
3. **Pomijanie martwych kont** – `ReEngagementGenerator` używa `CooldownGiveUpThrottle.has_no_push_target()` (tylko tej metody, nigdy `is_throttled()`), blokuje gdy JEDNOCZEŚNIE brak tokenu FCM I `activated_at IS NULL`.

**Liczby wyjściowe:** koszt AI 112,13 USD/30d, z czego 90,91 USD to NOTIFICATION, a 78,08 USD (86%) sama operacja `re_engagement_text_warm`. Dowód kontrfaktyczny qa: 240 tyknięć godzinowych dawało **168 renderów** przed naprawą wobec **≤2** po. Oczekiwany spadek ~99%, do 1-2 USD/mies. To ekstrapolacja, nie pomiar.

**Model:** `gpt-5.4-mini` na prodzie, potwierdzone z bazy (100% ze 105 567 wywołań). `heroku config` NIE pokazuje zmiennych `GPT_MODEL*`, bo żyją w śledzonym gitem `MindSync/.env` jadącym w slugu. `GPT_MODEL_41_MINI` jest współdzielony przez 13 plików, w tym żywą rozmowę, więc zmiana modelu wymaga dedykowanej zmiennej, nie globalnego przełącznika. Prompt ~580 tok. wejścia / ~96 wyjścia, za krótki na prompt caching (próg ~1024).

**Obalona teza:** „81% pushy wygasa niedostarczonych" jest FAŁSZYWE. Kwerenda prod: 100% miało `sent_at`, 73% `push_delivered=True`. EXPIRED znaczy „minął `expires_at`", nie „niedostarczony". Open rate 1,4% mierzy realne niezaangażowanie, nie problem dostarczalności. Auto-czyszczenie martwych tokenów DZIAŁA (własna implementacja w `notification_service.py`, nie ta z `broadcast.py`).

**Karta in-app dociera do usera bez tokenu FCM** – `GET /moments/upcoming` wołane przy każdym otwarciu apki niezależnie od pusha; `get_pending_or_sent_moment_for_user` to świadomy kanał zapasowy dla „SENT ale push_delivered=False" (CS-20, MSV3.3). Dlatego NIE wolno pomijać generowania dla wszystkich bez tokenu.

**Pomiar do zrobienia ~2026-09-20:** pole `is_ai_generated` już leci do PostHoga w `moment.scheduled`/`moment.sent`, więc porównanie open rate AI vs szablon to gotowe zapytanie, bez migracji. Jeśli AI nie miało przewagi, można zostawić szablony także dla płacących.

Kontekst biznesowy i pełna diagnoza: [[project-diagnoza-retencja-monetyzacja-2026-09-12]]. Lista zadań: `TASKS-notification-cost-cut.md`.
