---
name: project-testflight-sub-renewal-audit-2026-08-18
description: "Audyt 'sub na 2 dni' (tester): to TestFlight – od XII 2024 suby w TF odnawiają się co 24h (max 6x); backend zapisał wiernie expiry Apple; + 4 rezydualne ryzyka (brak server-side renewal trackingu, start_date leftover, TypeError date-vs-datetime, DATE drift)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 52cac8cb-04cc-46bd-86ef-098cf7d7073a
  modified: 2026-08-19T05:39:33.172Z
---

# Audyt "premium na 2 dni po zakupie miesięcznym" ([e-mail testera], 2026-08-18)

**Werdykt: NIE bug backendu.** Zakup poszedł przez **TestFlight (sandbox Apple)** – od grudnia 2024 auto-renewable suby w TestFlight odnawiają się **co 24 h niezależnie od okresu** (max 6 odnowień w tygodniu, potem auto-cancel). Apple zwróciło `expires_date ≈ zakup + 24h`, backend zapisał to 1:1 (`_activate_user_subscription` zawsze ustawia `end_date = expiry ze sklepu`, nigdy sam nie liczy miesiąca). Produkcyjny zakup dostanie realny miesiąc.

Dowody (db-reports/2026-08-18-tester-purchase-dates-audit.md): konto utworzone 2026-08-17 20:41 (trial 08-17→08-21); jedyny paragon apple `premium_m_01` VERIFIED 2026-08-18 08:25 UTC, `platform_transaction_id=2000001223046972` (**prefix 2000000… = sandbox/TestFlight**); zero promo; `end_date=2026-08-19` = +24h. **Rozpoznawanie zakupów testowych: sandbox txn id zaczyna się od 2000000/2000001.**

Wyjaśnienia pól:
- `start_date` po zakupie NIE jest datą zakupu – aktywacja ustawia start tylko gdy NULL, więc zostaje leftover z signup-triala (kosmetyka).
- `had_trial` NIE wpływa na daty/długość – to flaga "skonsumował trial SKLEPOWY" (is_trial_period / paymentState==2 albo one-time purchase); signup 4-dniowy grant celowo jej nie ustawia. Konsumenci: popupy FE + Loops.
- `granted_via='purchase'` ustawia bezwarunkowo `_activate_user_subscription` (i backfill oo/pp dla istniejących wierszy) – poprawne.

**Rezydualne ryzyka (nie naprawione, kandydaci na tickety):**
1. **Brak server-side renewal trackingu** – brak App Store Server Notifications i pollingu; `end_date` przedłuża się TYLKO gdy klient ponownie wyśle paragon, a purchaseStream jest armowany wyłącznie na ekranie paywalla (nie przy starcie apki). W prodzie po końcu okresu hourly `deactivate_expired_subscriptions` zgasi premium płacącemu, dopóki nie wejdzie w paywall/restore.
2. `users.py:302` i `:1477` porównują `sub.end_date > utc_now()` a prod ma kolumny **DATE** → TypeError połykany przez try/except, mislabel `subscription_tier` w PostHog (fix-wzorzec: `crud.safe_to_datetime`, użyty w promo :805).
3. Drift: `models.py` deklaruje DateTime(timezone=True), prod ma `date` dla `user_subscription.start_date/end_date` (klasa [[project-postgres-enum-drift]]).
4. Promo endpoint (users.py:820-823) nadpisuje `start_date/end_date` bezwarunkowo gdy extend_days > pozostałe dni – może skrócić/przestawić daty purchaserowi (granted_via chroniony, daty nie).

U testerki: TF odnowi sub co 24h do ~08-24, ale nasz end_date sam się nie przedłuży – hourly job zgasi is_active po 08-19 (+grace). To oczekiwane w TestFlight, nie regresja fixu v539. Patrz też [[project-trial-paywall-block-fix-2026-08-18]].

**UPDATE 2026-08-19 – wszystkie 4 ryzyka NAPRAWIONE, DEPLOYED: push 2026-08-19 → Heroku **v541**, dyna web/worker/scheduler up, boot czysty. Bez migracji – deploy code-only.**
- R1: `deactivate_expired_subscriptions` re-weryfikuje najnowszy VERIFIED paragon przed zgaszeniem; odnowienie → `_activate_user_subscription`; cap 50/run, transient→retry z twardym capem 3 dni po end_date; **guard HIGH-002**: Apple renewal akceptowany TYLKO gdy `original_transaction_id == receipt.platform_transaction_id` (blob verifyReceipt jest per Apple ID – bez guardu lapsed user mógłby jechać na cudzej płatności; legacy NULL txid = odmowa); timeout=15 na Apple requests.post i kliencie Google (AuthorizedHttp+httplib2). Nowy `crud.get_latest_verified_receipt`. rq_scheduler_setup nietknięty.
- R3: model start/end_date → `Date` (prod = źródło prawdy; tabela predates alembic), pisarze `.date()`, czytelnicy przez `safe_to_datetime`.
- R2: TypeError w users.py:302/:1477 naprawione (subscription_tier w PostHog już nie kłamie).
- R4: promo nie resetuje `start_date`; purchase = addytywnie `max(now,end)+dni`; trial = stare zasady.
- Suita: 5327 pass / 21 fail = identycznie z baseline HEAD (zweryfikowane worktree'em na czystym c1334e8); +22 nowe testy. Security review: GO po fixie HIGH-002/MED-001.
- **Pułapka procesowa: nie odpalać pełnej suity równolegle z agentem edytującym kod – pytest importuje pliki w trakcie i daje fantomowe faile** (41 vs realne 21).
- Backlog (Low, nie zrobione): cancellation_date/refund check w weryfikatorach; timeout w `verify_apple_one_time_product`; App Store Server Notifications V2 + RTDN jako docelowe; FE: purchaseStream armowany tylko na paywallu.
