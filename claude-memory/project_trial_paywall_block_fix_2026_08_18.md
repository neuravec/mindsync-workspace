---
name: project-trial-paywall-block-fix-2026-08-18
description: "Bug \"trial blokuje zakup\" naprawiony e2e; kolumna granted_via + premium_source; BE DEPLOYED v539, FE PUSHED dev; lekcja psycopg2 datetime.date w backfillu"
metadata: 
  node_type: memory
  type: project
  originSessionId: 66a32afe-aab9-47d6-b2ab-e622a7e9ca76
  modified: 2026-08-18T07:02:48.655Z
---

# Trial blokował zakup subskrypcji – fix granted_via/premium_source (2026-08-17/18)

**Incydent:** tester ([e-mail testera]) na nowym koncie Android nie mógł kupić suba – "już masz premium". Przyczyna: automatyczny 4-dniowy grant przy rejestracji (`_create_initial_subscription(days=4)`, users.py) zapisuje `is_active=True/PREMIUM` identycznie jak płatna subskrypcja; `subscription_screen.dart` gate `if (isPremium || starterPurchased) return PremiumView()` (bez przycisku kupna). Blokada czysto frontowa – backend nigdy nie odrzucał zakupu. Dotyczyło KAŻDEGO nowego usera przez pierwsze 4 dni (w dniu incydentu 8/13 "premium" = trial bez paragonu). Cross-account replay (HIGH-001) wykluczony.

**Fix (DEPLOYED/PUSHED 2026-08-18):**
- BE: kolumna `user_subscription.granted_via` VARCHAR(20) NULL + stałe `SubscriptionGrantedViaEnum` (signup_trial|promo|purchase, wzór String+stałe). Writerzy: initial grant→signup_trial; promo→promo TYLKO gdy != purchase (purchase nigdy nie degradowany!); `_activate_user_subscription` i `activate_user_access_until`→purchase bezwarunkowo. `GET /get_user_profile_and_subscription` zwraca addytywne `premium_source` (dodane też do `UserProfileResponseWithTrial` w schemas – response_model wycina niezadeklarowane klucze!).
- FE: `UserInfo.premiumSource` (model RĘCZNY – bez build_runnera), gate przez `shouldForcePremiumView()`: PremiumView tylko gdy `subscriptionIsActive && (premiumSource=='purchase' || null)`. NULL = legacy-safe (zachowanie jak dawniej). Trial/promo widzą paywall; `paywall_shown` przestał być tłumiony dla triali. Refresh po zakupie już istniał (`PremiumView.initState→refreshSubscriptionInfo`).
- Deploy split 2 commity (migracja osobno od modelu!): a31c954 (migracja oo6p7q8r9s0t) → alembic upgrade → 91638ce (kod) → 97ef3b0 (migracja korygująca pp7q8r9s0t1u). Heroku v537–v539. FE: dev `05f5dfd` (po rebase na Codemagic "Pre-release updates") → TestFlight/Play internal.
- Migracje: **pp7q8r9s0t1u = HEAD** (po nn5o6p7q8r9s → oo6p7q8r9s0t).
- Prod zweryfikowane: 5 purchase aktywne / 1 promo / 8 signup_trial / 1 NULL celowy (id=298: ręczny 730-dniowy grant PREMIUM bez paragonu, 2024-12→2026-12 – guard kształtu 4 dni słusznie go pominął).

**Incydent wtórny (lekcja):** backfill pass 3 pierwszej migracji zrobił no-op na prodzie – `_coerce_datetime` nie obsługiwał `datetime.date` (psycopg2 zwraca date dla kolumn date; SQLite zwraca stringi ISO, więc testy przeszły). Naprawione migracją korygującą + fix in-place. **Testy migracji czytających kolumny date muszą być karmione obiektami `datetime.date`, nie stringami.** Patrz też [[feedback-no-live-api-experiments]], [[project-postgres-enum-drift]].

**Ryzyko wdrożeniowe tej klasy zmian:** dodanie kolumny do modelu `UserSubscription` = każdy pełnoencyjny ORM SELECT jej wymaga → deploy przed migracją wywala `is_user_premium()` (całą warstwę premium), nie jedną funkcję. Stąd split na 2 commity/deploye.

**Otwarte:**
- Stare buildy FE nadal blokują zakup w trialu do czasu aktualizacji apki (czytają tylko subscription_is_active).
- Tester SKASOWAŁ konto (users nie ma konta testera) – po ponownej rejestracji na starym buildzie trzeba mu zgasić `is_active` na NOWYM UID (skrypt-wzór: db-reports/2026-08-17-disable-tester-trial.py), na nowym buildzie zadziała samo.
- Osobny ticket-kandydat: `itemAlreadyOwned` z Google Play pokazuje generyczne "Failed to complete the purchase" bez wyjaśnienia.
- `PUT /subscription` – martwy endpoint pozwalający ustawić is_active bez paragonu (udokumentowane ryzyko rezydualne, komentarz w kodzie).
- Heroku one-off `python < script` na Windows: odpalać przez `cmd /c "... < plik"`, skrypt MUSI być REPL-safe (bez pętli for/bloków – tylko jednolinijkowce), dyna potrafią wisnąć → `heroku ps:stop run.NNNN`.
