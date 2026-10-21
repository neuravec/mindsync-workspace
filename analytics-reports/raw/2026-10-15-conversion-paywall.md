# Konwersja paywall -> zakup, 60 dni: surowy wyciąg z PostHog

- **Data**: 2026-10-15 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okno**: 2026-08-16 00:00 UTC -> 2026-10-15 ~18:00 UTC (60 dni). Podział: PRZED = 08-16..10-02 (48 dni), PO = 10-03..10-15 (13 dni, redesign subskrypcji + onboardingu, poprawka monthly iOS).
- **Pytanie**: lejek paywall -> wybór planu -> start zakupu -> wynik, per trigger_feature / platforma / plan, przed i po 03.10; trial -> płatny; błędy; restore; czas do paywalla i zakupu.
- **Prawda o przychodzie**: Postgres `subscription_receipts` + App Store / Google Play (przez `database-administrator`). PostHog pokazuje zachowanie, nie pieniądze.

## Weryfikacja zdarzeń (60 dni, kto emituje)

| zdarzenie | strona ($lib) | płynie? | uwagi |
|---|---|---|---|
| `paywall_shown` | klient | tak (82 zd.) | ma `trigger_feature`, `plans_shown`, `hours_since_signup` |
| `subscription_screen_opened` | klient | tak (226) | brak triggera przed 2.0.97, użyty jako szerszy proxy "widział paywall" |
| `subscription_product_selected` | klient | tak (114) | `subscription_type`, `selection_source` (od 03.10: default/user/cta) |
| `subscription_purchase_started` | klient | tak (47) | |
| `subscription_purchase_pending` | klient | tak od 03.10 (8, tylko tester) | |
| `subscription_purchase_completed` | klient ORAZ backend | tak | backend (`posthog-python`) zawiera odnowienia i re-weryfikacje; liczono po osobie, klient = akt zakupu |
| `subscription_purchase_failed` | klient | tak (28) | `failure_reason`: pending / store_error / user_cancelled |
| `subscription_verification_failed` | klient + backend | tak (621) | 1-2 osoby, pętle |
| `subscription_restore_*` | klient | tak od 03.10 | `restore_failed` nigdy nie wystąpił |
| `trial_started` | backend | tak od 2026-10-03 09:22 | 54 osoby |
| `trial_ended` | backend | **prawie nie** (2 zd.) | oba `outcome=converted`; brak zdarzeń dla trialów zakończonych bez zakupu |
| `post_onboarding_offer_shown/_result/_not_shown` | klient | tak od 03-09.10 | |
| `paywall_load_failed` | klient | tak (51) | 2 osoby, obie testowe/automaty |

**Filtr testerów** (osoba wykluczona, jeśli w oknie miała którekolwiek): `$is_testflight=true`, `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')` lub `$is_emulator=true`, >=12 różnych `$app_version`, >=3x `onboarding_completed`. Wynik: 351 osób "realnych", 37 wykluczonych (w tym 31 botów Play bez paywalla).

## Wyniki

### Baza i zasięg paywalla (realni użytkownicy, klient)

| okres | aktywni w aplikacji | widzieli paywall (shown lub screen_opened) | zasięg |
|---|---|---|---|
| PRZED (48 d) | 260 | 15 | 5,8% |
| PO (13 d) | 134 | 20 | 14,9% |

### (1) Lejek per okres (osoby, realni użytkownicy)

| krok | PRZED | PO |
|---|---|---|
| widział paywall (dowolny) | 15 | 20 |
| w tym `paywall_shown` | 10 | 20 |
| wybrał plan (`product_selected`) | 12 | 14 |
| start zakupu | n<5 | n<5 |
| zakup ukończony (klient) | n<5 | n<5 |
| zakup ukończony (klient lub backend) | 6 | 6 |
| porzucił (`paywall_dismissed`) | n<5 | 8 |
| nieudany zakup | n<5 | 0 |

Uwaga: "wybrał plan" w PO jest zawyżone, bo 14 osób to automatyczne preselekcje yearly (`selection_source=default`). Świadomy wybór (`user`): monthly 6 osób, yearly n<5.

### Per platforma (realni, osoby, klient)

| okres | OS | widzieli paywall | wybrali | start | zakup |
|---|---|---|---|---|---|
| PRZED | Android | 10 | 7 | n<5 | n<5 |
| PRZED | iOS | 5 | 5 | n<5 | n<5 |
| PO | Android | 19 | 13 | n<5 | n<5 |
| PO | iOS | n<5 | n<5 | 0 | 0 |

### Per plan (realni, osoby, klient)

| okres | OS | plan | wybrali | start | zakup | błąd |
|---|---|---|---|---|---|---|
| PRZED | Android | yearly | 7 | 0 | 0 | 0 |
| PRZED | Android | monthly | n<5 | n<5 | n<5 | 0 |
| PRZED | iOS | yearly | 5 | n<5 | 0 | n<5 |
| PRZED | iOS | monthly | n<5 | n<5 | n<5 | n<5 |
| PO | Android | yearly | 12 (głównie preselekcja) | 0 | 0 | 0 |
| PO | Android | monthly | n<5 | n<5 | n<5 | 0 |
| PO | iOS | yearly | n<5 | 0 | 0 | 0 |

Wniosek mechaniczny: w 60 dniach **żaden realny użytkownik nie kupił planu rocznego** wg PostHog; wszystkie ukończone zakupy klienta to monthly (plus 1 starter pack, `one_time_purchase_completed`).

### (6) Bramki: które się pokazują, które sprzedają (realni, `paywall_shown`, 60 d)

| trigger_feature | zdarzenia | osoby widziały | wybrały plan | zakup |
|---|---|---|---|---|
| post_onboarding | 12 | 12 | n<5 | 0 |
| drawer_menu | 14 | 9 | 0 | 0 |
| post_onboarding_all_plans | n<5 | n<5 | n<5 | n<5 (>=1) |
| trial_banner | 5 | n<5 | n<5 | 0 |
| trial_ended_popup | n<5 | n<5 | n<5 | 0 |
| premium_gate_after_therapy | 1 | n<5 | n<5 | n<5 (>=1) |
| trial_reminder | 1 | n<5 | n<5 | n<5 (>=1) |
| premium_gate_reflect_voice | n<5 | n<5 | n<5 | 0 |
| premium_gate_habits / _monthly_audit / _session_recording / _reflect_messages / settings | po 1 | n<5 | <=n<5 | 0 |
| (brak triggera, zdarzenia sprzed 2.0.97) | | | 13 | n<5 (>=1) |

Najczęściej pokazywane: `post_onboarding` (12 osób, sprzedaż 0 w kroku 1; sprzedaż przychodzi dopiero w kroku 2 `post_onboarding_all_plans`) i `drawer_menu` (9 osób, 0 wyborów planu). Bramki premium w funkcjach (`premium_gate_*`) u realnych użytkowników prawie się nie pokazują (po 1 osobie), co jest zgodne z tym, że 4-dniowy trial wciąż ukrywa limity u nowych.

### Oferta po onboardingu (od 03.10, realni)

| wynik `post_onboarding_offer_result` | osoby |
|---|---|
| `post_onboarding_offer_shown` (krok 1 na ekranie) | 8 |
| continued_to_plans (krok 1 -> krok 2) | n<5 |
| closed_plans (krok 2 zamknięty) | n<5 |
| skipped | n<5 |
| closed_offer (krok 1 zamknięty) | n<5 |
| purchased_starter | n<5 |

### (2) Trial -> płatny (backend `trial_started`, od 03.10)

| trial | platforma | dł. | trial powinien być zakończony (start > 5 d temu) | osoby | kupiły po starcie trialu |
|---|---|---|---|---|---|
| signup | android | 4 d | tak | 14 | n<5 |
| signup | android | 4 d | nie | 19 | n<5 |
| signup | ios | 4 d | tak | 10 | 0 |
| signup | ios | 4 d | nie | 11 | 0 |

Razem 54 triale (33 Android, 21 iOS), konwersja trial -> płatny w PostHog: n<5 (wszystko Android); na iOS 0 z 10 zakończonych. `trial_ended` wystąpiło tylko 2 razy (oba `converted`), więc wygaśnięcia bez zakupu w ogóle nie są emitowane.

Dodatkowo: iOS App Store (nie-TestFlight) po 03.10 to głównie 2.0.100 (8 osób), z czego 0 widziało paywall i 0 ukończyło onboarding w tym oknie. Zasięg paywalla na iOS w PO to n<5.

### (3) Błędy i anulowania (60 d)

| zdarzenie | przyczyna | okres | realni: zd. / osoby | testerzy: zd. / osoby |
|---|---|---|---|---|
| purchase_failed | pending (sprzed poprawki, iOS sheet liczony jako błąd) | PRZED | 3 / n<5 | 0 |
| purchase_failed | store_error | PRZED | 2 / n<5 | 0 |
| purchase_failed | store_error | PO | 0 | 12 / n<5 |
| purchase_failed | user_cancelled | PO | 0 | 8 / n<5 |
| purchase_failed | pending | PO | 0 | 3 / n<5 |
| verification_failed (backend) | apple_status_21002 | PRZED+PO | 62 / n<5 (1 osoba w pętli) | 0 |
| verification_failed | expired | PO | 0 | 478 / n<5 (1 osoba w pętli) |
| paywall_load_failed | (brak kodu) | PO | 0 | 51 / n<5 (automat Play) |

Po 03.10 realni użytkownicy nie mają ani jednego `subscription_purchase_failed`. Anulowania (`user_cancelled`) widać tylko u testerów. Reszta błędów to pętle pojedynczych osób, nie wzorzec.

### (4) Restore purchases (od 03.10)

| zdarzenie | realni | testerzy |
|---|---|---|
| restore_started | 0 | n<5 |
| restore_completed | 0 | n<5 (16 zd., 1 osoba) |
| restore_empty | 0 | n<5 |
| restore_failed | 0 | 0 |

Restore używają wyłącznie testerzy.

### (5) Czas do pierwszego paywalla i do zakupu (realni + testerzy razem, pierwszy kontakt od ingestu 2026-04-22)

| nowi w oknie | czas od pierwszego zdarzenia do 1. paywalla | osoby | kupujący |
|---|---|---|---|
| tak | < 1 h | 17 | n<5 |
| tak | 1-24 h | n<5 | n<5 |
| tak | 1-7 d | n<5 | 0 |
| tak | 7-30 d | n<5 | 0 |
| nie (starsze konta) | 1-7 d | n<5 | 0 |
| nie | 7-30 d | n<5 | n<5 |
| nie | 30 d+ | 8 | n<5 |

Kupujący (zakup klienta) nowi w oknie: n<5, wszyscy kupili w ciągu 3 dni od pierwszego zdarzenia. Kupujący ze starszych kont: n<5, kupowali po 35-163 dniach od pierwszego zdarzenia.

Właściwość `hours_since_signup` na `paywall_shown`: `post_onboarding` mediana 0,1 h, `trial_banner` 4,3 h, `trial_ended_popup` 299 h, `drawer_menu` 14 708 h (stare konta; wartość liczona od rejestracji konta, nie instalacji).

## Zastrzeżenia

- **Próba jest za mała na wnioski o stopach konwersji.** 60 dni = 6 realnych osób z ukończonym zakupem (wg klienta lub backendu), większość komórek n<5. Stopy procentowe per trigger/plan nie mają sensu statystycznego.
- **Podwójna emisja zakupu.** `subscription_purchase_completed` leci z klienta i z backendu. Backend obejmuje odnowienia sandbox (Apple premium_m_01, 81 zd. / 3 osoby, cykl 24 h TestFlight) i **186 zdarzeń z backendu z `$os=Windows`** (SKU `com.mindsync.premium`, 3 osoby, 08-19..10-14). To wygląda na lokalny/testowy backend piszący do produkcyjnego PostHoga; nie liczyć jako zakupy. Android przez backend: 7 zd. / n<5 osób (zgodne z klientem).
- `subscription_receipt_received` = 588 zdarzeń / 8 osób: pętle weryfikacji, nie popyt.
- `trial_ended` nie raportuje wygaśnięć bez zakupu, więc "trial -> nie kupił" da się wyznaczyć tylko jako brak zakupu po starcie.
- `trigger_feature` na `subscription_product_selected/started/completed` istnieje dopiero od 2.0.97; zdarzenia PRZED mają NULL.
- Filtr testerów jest heurystyką; Android nie ma `$is_testflight`, a testowe zakupy Play (license testers) mogą przejść jako realne.
- Ingest od 2026-04-22: czas "od instalacji" to czas od pierwszego zdarzenia w PostHog.
- Prywatność: nie wybierano `user_id`, `error_message`, kwot ani ID osób.

## Zapytania (HogQL, dosłownie, kluczowe)

```sql
-- filtr testerów (CTE t, używany w każdym zapytaniu)
WITH t AS (
  SELECT person_id FROM events WHERE timestamp >= toDateTime('2026-08-16') AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
  HAVING countIf(properties.$is_testflight = true) > 0 OR countIf(properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro') OR properties.$is_emulator = true) > 0
     OR count(DISTINCT properties.$app_version) >= 12 OR countIf(event = 'onboarding_completed') >= 3
)
-- lejek per okres
SELECT period, testers, countIf(shown) AS u_paywall_shown, countIf(opened) AS u_screen_opened, countIf(shown OR opened) AS u_any_paywall,
  countIf(sel) AS u_selected, countIf(st) AS u_started, countIf(pend) AS u_pending,
  countIf(comp_c) AS u_completed_client, countIf(comp_b) AS u_completed_backend, countIf(comp_c OR comp_b) AS u_completed_any,
  countIf(fail) AS u_failed, countIf(vfail) AS u_verif_failed, countIf(dism) AS u_dismissed
FROM (
  SELECT person_id, if(timestamp < toDateTime('2026-10-03'), '1_pre', '2_post') AS period,
    person_id IN (SELECT person_id FROM t) AS testers,
    countIf(event='paywall_shown')>0 AS shown, countIf(event='subscription_screen_opened')>0 AS opened,
    countIf(event='subscription_product_selected')>0 AS sel, countIf(event='subscription_purchase_started')>0 AS st,
    countIf(event='subscription_purchase_pending')>0 AS pend,
    countIf(event='subscription_purchase_completed' AND properties.$lib='posthog-flutter')>0 AS comp_c,
    countIf(event='subscription_purchase_completed' AND properties.$lib='posthog-python')>0 AS comp_b,
    countIf(event='subscription_purchase_failed')>0 AS fail, countIf(event='subscription_verification_failed')>0 AS vfail,
    countIf(event='paywall_dismissed')>0 AS dism
  FROM events WHERE timestamp >= toDateTime('2026-08-16') AND event IN ('paywall_shown','subscription_screen_opened','subscription_product_selected','subscription_purchase_started','subscription_purchase_pending','subscription_purchase_completed','subscription_purchase_failed','subscription_verification_failed','paywall_dismissed')
  GROUP BY person_id, period
) GROUP BY period, testers

-- per trigger
SELECT properties.trigger_feature AS trig, person_id IN (SELECT person_id FROM t) AS testers,
  countIf(event='paywall_shown') AS ev_shown, count(DISTINCT if(event='paywall_shown', person_id, NULL)) AS u_shown,
  count(DISTINCT if(event='subscription_product_selected', person_id, NULL)) AS u_sel,
  count(DISTINCT if(event='subscription_purchase_started', person_id, NULL)) AS u_started,
  count(DISTINCT if(event='subscription_purchase_completed', person_id, NULL)) AS u_completed,
  count(DISTINCT if(event='subscription_purchase_failed', person_id, NULL)) AS u_failed,
  count(DISTINCT if(event='paywall_dismissed', person_id, NULL)) AS u_dismissed
FROM events WHERE timestamp >= toDateTime('2026-08-16') AND properties.$lib='posthog-flutter'
  AND event IN ('paywall_shown','subscription_product_selected','subscription_purchase_started','subscription_purchase_completed','subscription_purchase_failed','paywall_dismissed')
GROUP BY trig, testers

-- trial -> płatny
WITH ts AS (SELECT person_id, min(timestamp) AS t0, any(properties.trial_type) AS ttype, any(properties.platform) AS plat, any(properties.trial_length_days) AS len
  FROM events WHERE event = 'trial_started' AND timestamp >= toDateTime('2026-10-01') GROUP BY person_id),
pc AS (SELECT person_id, min(timestamp) AS tp FROM events WHERE event = 'subscription_purchase_completed' AND timestamp >= toDateTime('2026-10-01') GROUP BY person_id)
SELECT ttype, plat, len, ts.t0 < now() - INTERVAL 5 DAY AS trial_should_be_over, count() AS trial_users, countIf(pc.tp > ts.t0) AS bought_after_trial_start
FROM ts LEFT JOIN pc ON pc.person_id = ts.person_id GROUP BY ttype, plat, len, trial_should_be_over

-- błędy
SELECT event, properties.$lib AS lib, properties.failure_reason AS reason, if(timestamp < toDateTime('2026-10-03'), 'pre', 'post') AS period,
  person_id IN (SELECT person_id FROM t) AS testers, count() AS ev, count(DISTINCT person_id) AS users
FROM events WHERE timestamp >= toDateTime('2026-08-16') AND event IN ('subscription_purchase_failed','subscription_verification_failed','paywall_load_failed')
GROUP BY event, lib, reason, period, testers

-- selekcja planu
SELECT if(timestamp < toDateTime('2026-10-03'), 'pre', 'post') AS period, properties.subscription_type AS plan, properties.selection_source AS src, count() AS ev, count(DISTINCT person_id) AS users
FROM events WHERE event='subscription_product_selected' AND timestamp >= toDateTime('2026-08-16') AND coalesce(properties.$is_testflight,false) != true
GROUP BY period, plan, src

-- źródła backendowych zakupów
SELECT event, properties.$os AS os, properties.platform AS plat, properties.product_sku AS sku, count() AS ev, count(DISTINCT person_id) AS users, min(timestamp), max(timestamp)
FROM events WHERE timestamp >= toDateTime('2026-08-16') AND properties.$lib='posthog-python' AND event IN ('subscription_purchase_completed','subscription_receipt_received','trial_started')
GROUP BY event, os, plat, sku
```

Pozostałe zapytania (restore/offer, czas do paywalla, `hours_since_signup`, zasięg wg wersji iOS, baza aktywnych) mają ten sam wzór; pliki SQL w scratchpadzie sesji.
