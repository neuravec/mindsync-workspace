---
name: project_post_release_review_2026_08_16
description: "Przegląd 4 dni po release 12.08 — release techniczny OK, ale ADD_THERAPY_DATE zalewa 98,5% bazy, crash firebase_analytics u każdego, paywall_shown martwy, DAU w PostHog zawyżone przez eventy server-side"
metadata: 
  node_type: memory
  type: project
  originSessionId: e01f33cc-3e18-48ac-ad1a-fe294806ffcd
  modified: 2026-08-16T09:12:49.802Z
---

Przegląd post-release (2026-08-16, okno 12–15.08) wdrożenia z 12.08 (BE Heroku v528–531 z 10–11.08, FE build 2.0.77 z `d41dec4`). Raport: `analytics-reports/2026-08-16-post-release-review-12-08.md`. ClickUp: parent [86cb5tvn8](https://app.clickup.com/t/86cb5tvn8) + 6 subtasków (86cb5tvv1, 86cb5tvv6, 86cb5tvva, 86cb5tvvw, 86cb5tvvz, 86cb5tvw1), każdy z work-orderem w komentarzu. **AUDIT ONLY — żadna poprawka nie została zaimplementowana.**

**Werdykt:** technicznie OK, biznesowo niemierzalne (38 unikalnych klientów w 4 dni; adopcja 2.0.77 = 29 osób).

**Pułapka pomiarowa, którą trzeba pamiętać przy KAŻDEJ analizie PostHog od 11.08:** DAU skoczyło z ~20 na ~1750, bo naprawa `init_posthog` w workerze (`177c026`) sprawiła, że joby emitują `moment.scheduled`/`moment.sent` dla całej bazy jako `$lib=posthog-python`. **Realna aktywność = filtr `properties.$lib = 'posthog-flutter'`** (11–17 dziennie, bez zmian przed/po). Dashboardy z `scripts/posthog_build_dashboards.py` powstały PRZED skokiem i nie mają tego filtru. Patrz [[reference_posthog_dashboards]], [[reference_posthog_access_method]].

**Potwierdzone naprawy:** pętla retry Reflect 403 (1870 błędów/tydzień od 1 usera → 0), api_error ~570/dobę → ~255/dobę, tagowanie `is_expected` działa (949 spodziewanych vs 96 realnych, tylko 1 prawdziwa 5xx = ClientDisconnect).

**4 znaleziska:**
1. **ADD_THERAPY_DATE = 99,1% całego ruchu powiadomień** — 10 522 momentów / 1786 z 1813 userów w 6 dni; opened 22 (0,21%), acted 5. 1647 userów bez tokena FCM (praca w próżnię), 139 z tokenem dostaje ~6 pushy w 6 dni. Generator (`app/services/moments/add_therapy_date_generator.py`) jest `register_deterministic` → iteruje po każdym userze, dedup tylko per dzień lokalny, zero cooldownu. **Koszt AI NIE jest problemem** (tylko 66 z 10 692 momentów `is_ai_generated`, reszta to statyczne `_FALLBACK`).
2. **Zgłoszenie operatora „mam datę, a i tak przychodzi" — potwierdzone, ale mechanizm inny niż zepsuty warunek.** W ostatnich 48h **0 userów z ważną przyszłą datą** dostało nudge, więc `compute_next_session_date() is None` działa poprawnie. Problem: 6 z 8 userów ma `custom_therapy_sessions` **w przeszłości** — data była, minęła, nikt nie prosi o kolejną, a komunikat brzmi „nie ustawiłeś sesji". Brak gałęzi „data minęła" w `app/utils/therapy_schedule_utils.py`. **W CAŁEJ bazie tylko 12 osób kiedykolwiek ustawiło jakąkolwiek datę** (4 recurring, 8 custom, 2 z `next_session_date`, 1 w przyszłości).
3. **Crash `FirebaseAnalytics.logEvent`** (`firebase_analytics.dart:121`, `PlatformDispatcher`, handled=false) — 83 ze 111 wyjątków, 13 z 14 dotkniętych userów, 34% aktywnych klientów. Brak baseline'u sprzed 11.08 (error tracking wszedł dopiero z tym release'em, `5b3ecae`), więc nie wiadomo czy regresja. Dane w Firebase mogą być dziurawe. Uwaga przy analizie: `$exception_type`/`$exception_message` są PUSTE — treść siedzi w `$exception_list`.
4. **`paywall_shown` martwy** — 1 event w historii (16.08, `trigger_feature=settings`), przy 10 `subscription_screen_opened`/5 userów. `trial_started` (server-side, `991cb9a`) = 0, ale przy tej skali może to być prawda, nie bug — rozstrzygnąć przez `subscription_receipts` w prod DB.

**Pomniejsze defekty danych:** `next_session_date` zwietrzałe (3 userów ma schedule + NULL; liczone tylko przy zapisie w `crud.update_therapy_schedule`); `notification_moments.push_delivered` bezwartościowe (`server_default=true`, nigdy nie weryfikowane — `true` dla 8969 momentów przy 144 userach z tokenem); `moment.expired` (~20/dzień) trafia zawsze na jeden `person_id` (job nie przekazuje `distinct_id`).

Dostęp do prod DB przez `heroku run` — **działa `Get-Content skrypt.py | heroku run --no-tty -a mindsync python` z PowerShella**; wariant z PTY (`heroku run ... < skrypt.py` z basha) wisi bez outputu i wymaga ręcznego `heroku ps:stop`. Heroku CLI w tej sesji **nie odpowiada z narzędzia Bash** (timeouty nawet na `heroku --version`) — używać PowerShella. Uzupełnia [[reference_database_administrator_agent]].
