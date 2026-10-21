---
name: project_post_release_fix_batch_2026_08_16
description: "Batch naprawczy po przeglądzie post-release: DEPLOYED Heroku v536 + 2 migracje (head nn5o6p7q8r9s), FE pushed dev; 2 realne bugi płatnicze naprawione; device-QA płatności BLOKUJE promocję do produkcji"
metadata: 
  node_type: memory
  type: project
  originSessionId: e01f33cc-3e18-48ac-ad1a-fe294806ffcd
  modified: 2026-08-16T13:03:26.329Z
---

Batch naprawczy wynikający z [[project_post_release_review_2026_08_16]]. **DEPLOYED** 2026-08-16. Runbook: `analytics-reports/2026-08-16-deploy-runbook.md`. ClickUp: parent [86cb5tvn8](https://app.clickup.com/t/86cb5tvn8), 8 subtasków.

**Stan:** BE Heroku **v536** = `a3a4086` (origin/main), migracje **nn5o6p7q8r9s = HEAD** (łańcuch: ll3m4n5o6p7q → mm4n5o6p7q8r → nn5o6p7q8r9s). FE PUSHED `dev` = `1ff3f42` → Codemagic → TestFlight/Play internal (**NIE promowane do produkcji**). Dashboardy PostHog zastosowane (`--update --retire-dead`), zweryfikowane: DAU pokazuje 11–17 zamiast ~1750. QA GO (0 regresji: BE 5235 pass/21 fail vs baseline 5153/21; FE 1865/28 vs 1837/28), security GO po naprawie HIGH-001.

**Największe znalezisko – 2 realne bugi płatnicze (FE):** (1) `completePurchase()` wołane PRZED wysłaniem paragonu na backend → zerwana sieć/kill apki = transakcja domknięta w sklepie, zero śladu na serwerze, user płaci i nie dostaje premium; (2) `markAsSubscribed`/`markAsOneTimePurchased` akceptowały tylko `PurchaseStatus.purchased` i po cichu no-opowały na `.restored` → **każde użycie „przywróć zakupy" w historii apki nie wysłało paragonu**. Oba naprawione (verify-before-complete + 1 retry 2s + transakcja zostaje pending przy porażce). To tłumaczy rozjazd „5 zakupów wg PostHog vs 1 paragon w DB".

**HIGH-001 (security, naprawione):** endpointy weryfikacji nie sprawdzały, czy transakcja nie jest już przypisana do innego usera → jeden opłacony zakup mógł dać premium dowolnej liczbie kont przez „przywróć zakupy". Fix: `subscription_receipts.platform_transaction_id` (Apple `original_transaction_id` – był parsowany i wyrzucany!, Google `purchase_token` a NIE `order_id`, który rotuje przy odnowieniu). **Świadomie BEZ constraintu UNIQUE** – ten sam user może legalnie mieć kilka VERIFIED wierszy (brak dedup-before-insert = LOW-002), więc constraint na kolumnie blokowałby zwykłe ponowne wysłanie. Prod przed fixem: Apple `order_id` 100% NULL (53/53), Google 67 wierszy zbackfillowanych.

**Decyzje operatora 2026-08-16:** Family Sharing najpewniej wyłączony → guard zostaje w najprostszej formie (**gdyby kiedyś włączyć, wrócić – Apple zwraca ten sam `original_transaction_id` każdemu członkowi rodziny**). Zmiana konta = odrzucana tak samo jak replay, obsługa przez support, [ticket backlog 86cb5v395](https://app.clickup.com/t/86cb5v395).

**Backend – reszta:** `CooldownGiveUpThrottle` mixin (7d cooldown, give-up po 3 zignorowanych, skip gdy brak tokena FCM **I** `activated_at IS NULL` – szerszy skip skasowałby kartę in-app, bo `GET /moments/upcoming` je pokazuje); rozdzielenie „nigdy nie ustawił daty" vs „data minęła" (`compute_most_recent_past_session_date` + `_FALLBACK_PASSED` w 7 językach); `push_delivered` liczone przez rekoncyliację z `notification_logs.moment_id` (stara wersja: `send_fcm_to_all_user_tokens()` NIGDY nie rzuca przy błędzie tokena, więc try/except był no-opem); `moment.expired` z prawdziwym `distinct_id`.

## Wnioski procesowe (ważne na przyszłość)

**Migracji NIE DA SIĘ uruchomić przed deployem kodu** – pliki migracji jadą w slugu. `heroku run alembic upgrade head` przy starym slugu kończy się sukcesem i NIC nie robi (head = stara rewizja). Zawsze weryfikuj `alembic current` po fakcie. Kolejność musi być: push → deploy → natychmiast migracja. Tryb konserwacji odrzucony jako gorszy (blokuje całą apkę wszystkim vs wąskie okno na 2 endpointach płatniczych przy ~0 zakupów dziennie).

**NIGDY `bind.commit()` w migracji.** `nn5o6p7q8r9s` miało je „dla SQLite" → na Postgresie (transactional DDL, Alembic trzyma całość w jednej transakcji) DDL się zapisał, ale **stamp `alembic_version` przepadł** – `current` pokazywał `mm4n5o6p7q8r` mimo wykonania obu. Prawdziwy bug był w harnessie testowym (nie commitował własnego połączenia po `module.upgrade()`), nie w migracji. Fix `a3a4086` usuwa commit całkowicie + test AST skanujący wszystkie migracje pod kątem `.commit()` (z pominięciem docstringów). Naprawa self-heal: idempotentna migracja re-run + poprawny stamp, bez ręcznego `alembic stamp` (który i tak blokuje klasyfikator uprawnień).

**Heroku CLI nie odpowiada z narzędzia Bash** (timeout nawet na `--version`) – używać PowerShella, `$env:HEROKU_DISABLE_AUTOUPDATE=1`, i `Get-Content skrypt.py | heroku run --no-tty -a mindsync python` (self-exiting, bez ręcznego `ps:stop`). Patrz [[reference_database_administrator_agent]].

## NIEZWERYFIKOWANE – sprawdzić 2026-08-17

1. **Czy throttling ADD_THERAPY_DATE zadziałał.** Deploy o 12:44 UTC, generator odpala o 18:00 czasu lokalnego usera. Baseline dzienny: 12.08=1525, 13.08=1784, 14.08=1785, 15.08=1669. Oczekiwane po fixie: spadek o rząd wielkości. **16.08 (256) NIE jest dowodem** – to głównie sprzed deployu.
2. **Czy `notification_logs.moment_id` się wypełnia.** Po migracji (12:52 UTC) nie powstał ANI JEDEN log – brak wysyłek z tokenem w tym oknie. Zero z 19 logów ma `moment_id`, ale wszystkie pochodzą sprzed migracji, więc to spójne, nie defekt. Wymaga potwierdzenia na świeżych danych.
3. **Device-QA ścieżki płatniczej – BLOKUJE promocję buildu do produkcji.** Prawdziwy zakup, prawdziwe przywracanie, zakup jednorazowy, kill apki w trakcie potwierdzania, próba przywrócenia cudzego zakupu na drugim koncie.

## Follow-upy (tickety/backlog)

Nasłuch transakcji przy starcie apki; dedup paragonów (LOW-002) odblokowujący constraint; throttling dla `REFLECTION_INVITATION`/`THERAPY_RELATIONSHIP_CHECKIN` (~1750 kandydatów/tydz., ~98% wygasa niewysłanych); proaktywna propozycja terminu po sesji; **event przy nieudanym `loadSubscriptionsProducts()` – dziś cichy potencjalny bloker sprzedaży** (5 userów otworzyło ekran subskrypcji, ~0 `paywall_shown`); rename 5 insightów `[awaiting deploy]`; martwy `onboarding_legal_gate_abandoned` (0 od zawsze); **5 dashboardów PostHog nie budowanych skryptem nadal pokazuje ~1750** (m.in. domyślny `My App Dashboard` 568994 – najpewniej to tam ktoś zobaczy złą liczbę).
