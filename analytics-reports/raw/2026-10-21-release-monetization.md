# Monetyzacja po wydaniu 2.0.117 (redesign): surowy wyciąg z PostHog

- **Data**: 2026-10-21 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okna** (UTC, liczone od chwili zapytania ok. 2026-10-21 17:00): OSTATNIE 48 h = 10-19 ~17:00 -> 10-21 ~17:00; POPRZEDNI TYDZIEŃ = 10-12 ~17:00 -> 10-19 ~17:00 (7 dni).
- **Pytanie**: paywall (per trigger, platforma, wersja, per osoba), lejek paywall -> start -> wynik, trial, restore, błędy zakupu, bramki limitów premium na nowej wersji.
- **Nowa wersja**: `2.0.117`, pierwsze zdarzenie 2026-10-19 18:13 UTC (Android), iOS 20:44 UTC (`$is_testflight=false`, czyli App Store). 2.0.113-2.0.116 z 19.10 to buildy przejściowe (głównie testerzy).
- **Prawda o kupujących i przychodzie**: Postgres `subscription_receipts` + App Store / Google Play (`database-administrator`). PostHog pokazuje zachowanie, nie pieniądze.

## Weryfikacja zdarzeń (14 dni)

| zdarzenie | strona | płynie? | ostatnie | uwagi |
|---|---|---|---|---|
| `paywall_shown` | klient | tak, 48 zd. / 29 os. | 10-21 16:43 | `trigger_feature`, `plans_shown`, `hours_since_signup` na 100% zdarzeń |
| `subscription_screen_opened` | klient | tak, 74 / 24 | 10-21 | |
| `subscription_product_selected` | klient | tak, 46 / 21 | 10-21 | `selection_source` (default/user) |
| `subscription_purchase_started` | klient | tak, 19 / 7 | 10-20 07:10 | |
| `subscription_purchase_completed` | klient 6/6 ORAZ backend 53/8 | tak | 10-18 | backend zawiera 6 zd. z `$os=Windows` (lokalny/testowy backend, SKU `com.mindsync.premium`), wykluczone |
| `subscription_purchase_failed` | klient | **0 zdarzeń w 14 dni** | | |
| `subscription_purchase_pending` | klient | 1 / 1 | 10-08 | |
| `one_time_purchase_completed` | backend | 1 / 1 | 10-12 | ten sam zakup klient raportuje jako `subscription_purchase_completed` z `product_id=ms_starter_package` |
| `paywall_dismissed` | klient | tak, 26 / 16 | 10-21 | `dismiss_method`, `purchase_attempted`, `selected_plan`, `dwell_ms` |
| `trial_started` | backend | tak, 63 / 63 | 10-21 16:18 | brak `$app_version`/`$os` klienta, jest `platform` |
| `trial_ended` | backend | prawie nie, 3 zd. | 10-18 | wszystkie `converted`; wygaśnięć bez zakupu brak |
| `subscription_restore_*` | klient | 2 started + 2 empty, 1 os. | 10-20 | |
| `paywall_load_failed` | klient | 29 / 2 | 10-20 | `reason`: products_not_found / store_unavailable |
| `usage_limit_panel_shown` | klient | 6 / 3 | 10-18 | `feature` |
| `habit_limit_reached` | klient | 2 / 2 | 10-19 | |
| `reflect_limit_hit` | klient + backend | 5 / 2 | 10-08 | |
| `api_error` (403) | backend | tak | | bez `$app_version` (zdarzenie serwerowe), podział tylko po endpointcie |
| `paywall_shown` brak? | | nie dotyczy | | nazwa istnieje i płynie |

**Filtr testerów** (jak w baseline 10-15, okno 21 d): osoba wykluczona, jeśli miała `$is_testflight=true`, `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')` lub `$is_emulator=true`, >=12 różnych `$app_version`, >=3x `onboarding_completed`.

## Wyniki

### Baza: aktywni w kliencie (osoby)

| okno | OS | realni, stara wersja | realni, 2.0.117 | testerzy |
|---|---|---|---|---|
| poprz. 7 d | Android | 44 | 0 | 11 |
| poprz. 7 d | iOS | 9 | 0 | n<5 |
| ost. 48 h | Android | 10 | 5 | 6 |
| ost. 48 h | iOS | 0 | n<5 (2) | n<5 |

Realnych osób na 2.0.117 jest 7 (5 Android, 2 iOS). Wszystko poniżej jest anegdotą, nie statystyką.

### (1) Paywall: pokazania per trigger (`paywall_shown`)

| okno | trigger_feature | realni zd. / os. | testerzy zd. / os. |
|---|---|---|---|
| poprz. 7 d | trial_ended_popup | 5 / 5 | 0 |
| poprz. 7 d | post_onboarding | n<5 | 0 |
| poprz. 7 d | post_onboarding_all_plans | n<5 | n<5 |
| poprz. 7 d | premium_gate_reflect_voice | n<5 (1 os.) | n<5 |
| poprz. 7 d | drawer_menu, premium_gate_after_therapy, trial_banner | po 1 os. | n<5 |
| ost. 48 h | post_onboarding_all_plans, post_onboarding, trial_ended_popup | po 1 os. | |
| ost. 48 h | drawer_menu, premium_gate_between_sessions | | po 1 os. |

Per osoba: poprz. 7 d 13 realnych osób z `paywall_shown` (Android 10, iOS 3) na 54 aktywnych = 24%. Ost. 48 h 3 osoby na 17 = 18%. Baseline PO (03-15.10): zasięg 14,9% (szersza definicja, 13 dni), więc bez zmiany kierunku.

### (1b) Paywall per platforma i wersja (realni)

| okno | OS | wersja | zd. | os. |
|---|---|---|---|---|
| poprz. 7 d | Android | 2.0.110 | 10 | 7 |
| poprz. 7 d | Android | 2.0.100 / 2.0.107 / 2.0.111 | 4 | n<5 |
| poprz. 7 d | iOS | 2.0.106 / 2.0.110 | 3 | n<5 |
| ost. 48 h | Android | 2.0.110 | 1 | 1 |
| ost. 48 h | Android | **2.0.117** | 1 | 1 |
| ost. 48 h | iOS | **2.0.117** | 1 | 1 |

Paywall na 2.0.117 renderuje się na obu platformach (po 1 realnej osobie), ale nikt na 2.0.117 nie rozpoczął zakupu.

### (2) Lejek per osoba (realni)

| krok | poprz. 7 d Android | poprz. 7 d iOS | ost. 48 h Android | ost. 48 h iOS |
|---|---|---|---|---|
| `paywall_shown` | 10 | n<5 (3) | n<5 (2) | n<5 (1) |
| `subscription_screen_opened` | 8 | n<5 | n<5 | n<5 |
| wybór planu świadomy (`selection_source=user`) | n<5 (3) | 0 | 0 | 0 |
| `purchase_started` | n<5 (3) | 0 | 0 | 0 |
| zakup ukończony (zdeduplikowany, patrz niżej) | n<5 (3) | 0 | 0 | 0 |
| `purchase_failed` | 0 | 0 | 0 | 0 |
| `paywall_dismissed` | 5 | n<5 (3) | n<5 | n<5 |
| restore | 0 | 0 | 0 | 0 |

**Deduplikacja zakupów (klient vs backend).** Jeden fakt = jeden zakup: klient `subscription_purchase_completed` (`server_confirmed=true`) sparowany w tej samej godzinie z backendem (`posthog-python`, `$os=Linux`, `platform=google`). Wykluczone: backend z `$os=Windows` (6 zd. / 3 os., Apple sandbox SKU, lokalny backend). Wynik w 9 dniach: **3 zakupy, wszystkie Android, wszystkie na starej wersji**:

| dzień (UTC) | produkt | trigger | wersja | klient | backend |
|---|---|---|---|---|---|
| 10-12 | ms_starter_package (jednorazowy) | post_onboarding_all_plans | 2.0.107 | `subscription_purchase_completed` (błędna nazwa dla jednorazowego) | `one_time_purchase_completed` |
| 10-14 | premium_m_01 | premium_gate_after_therapy | 2.0.110 | tak | tak |
| 10-18 | premium_m_01 | trial_banner | 2.0.110 | tak | tak (+ `trial_ended converted`) |

Ost. 48 h: **0 startów, 0 zakupów, 0 błędów u realnych użytkowników na jakiejkolwiek wersji.** iOS: 0 zakupów w całych 9 dniach (baseline: 0 na iOS od 03.10).

### (2b) Porzucenia paywalla (`paywall_dismissed`, wszyscy)

| okno | trigger | metoda | próbował kupić | plan zaznaczony | os. | mediana czasu |
|---|---|---|---|---|---|---|
| poprz. 7 d | trial_ended_popup | close_x | nie | annual | 5 | 3,0 s |
| poprz. 7 d | post_onboarding_all_plans | close_x | nie | annual | n<5 | 26,7 s |
| poprz. 7 d | drawer_menu / trial_banner / premium_gate_reflect_voice | close_x | nie | annual | n<5 | 2-7 s |
| poprz. 7 d | trial_banner | close_x | tak | monthly | 1 | 33,9 s |
| ost. 48 h | post_onboarding_all_plans | close_x | nie | annual | 1 | 120,9 s |
| ost. 48 h | trial_ended_popup | close_x | nie | annual | 1 | 18,2 s |

Popup po końcu trialu zamykany średnio po 3 s (5 z 5 osób), bez próby zakupu.

### (2c) Oferta po onboardingu (`post_onboarding_offer_result`, wszyscy)

| okno | wynik | OS | os. |
|---|---|---|---|
| poprz. 7 d | continued_to_plans | iOS 3, Android 1 | |
| poprz. 7 d | closed_plans | iOS | 3 |
| poprz. 7 d | purchased_starter | Android | 1 |
| poprz. 7 d | closed_offer / skipped / skipped_ineligible | Android | po 1 |
| ost. 48 h | continued_to_plans -> closed_plans | iOS | 1 |
| ost. 48 h | closed_offer, skipped_ineligible | Android | po 1 |

Na 2.0.117: 2 realne osoby ukończyły onboarding (obie iOS), 1 widziała ofertę. Android 2.0.117: 9 osób, 0 ukończonych onboardingów w tym oknie.

### (2d) Trial (`trial_started`, backend)

| okno | platforma | os. | na dobę |
|---|---|---|---|
| poprz. 7 d | ios | 17 | 2,4 |
| poprz. 7 d | android | 11 | 1,6 |
| ost. 48 h | ios | n<5 (4) | 2,0 |
| ost. 48 h | android | n<5 (2) | 1,0 |

Wszystkie `signup`, 4 dni. Tempo bez wyraźnej zmiany (4/dobę -> 3/dobę; przy tej skali to szum). `trial_ended`: 3 zdarzenia w 14 d, wszystkie `converted`, Google; wygaśnięcia bez zakupu dalej nie są emitowane.

### (2e) Błędy zakupu i ładowania

| okno | zdarzenie | powód | OS | zd. / os. | kto |
|---|---|---|---|---|---|
| poprz. 7 d | verification_failed + stale_transaction_finished | expired | iOS | 9+9+9 / 1 | 1 osoba w pętli (klient+backend, ten sam fakt potrójnie) |
| poprz. 7 d | verification_failed | apple_status_21002 | Windows (backend) | 2 / 1 | lokalny backend |
| poprz. 7 d | paywall_load_failed | products_not_found / store_unavailable | Android | 15 / 2 | tester OnePlus8Pro + emulator |
| ost. 48 h | paywall_load_failed | products_not_found (5x na **2.0.117**) / store_unavailable | Android | 10 / 1 | tester OnePlus8Pro |
| 14 d | `subscription_purchase_failed` | | | **0** | |

Osobny sygnał: 10-20 07:10 tester (Android 2.0.111, OnePlus8Pro) zrobił 8x `subscription_purchase_started` (7 monthly, 1 yearly) plus restore -> `restore_empty`, i **żaden z 8 startów nie ma zdarzenia wyniku w ciągu 1 h** (ani completed, ani failed, ani pending). W 30 d takich "startów bez wyniku" było też po 1 na Android 2.0.100/2.0.105/2.0.106/2.0.110. Albo zamknięcie arkusza Google Play nie emituje `failed/user_cancelled`, albo flow się zawiesza.

### (3) Bramki limitów premium

| okno | zdarzenie | wersja | zd. / os. |
|---|---|---|---|
| poprz. 7 d | usage_limit_panel_shown (`feature=reflect_messages`) | Android 2.0.110 | 2 / 1 |
| ost. 48 h | habit_limit_reached | Android 2.0.115 | 1 / 1 |
| ost. 48 h | premium_view_shown | Android 2.0.117 | 1 / 1 |
| 9 d | reflect_limit_hit | | 0 |
| 9 d | `paywall_shown` z `premium_gate_*` | | poprz. 7 d: n<5 realnych; ost. 48 h: 1 tester (`premium_gate_between_sessions`) |
| ost. 48 h | `api_error` 403/402/429 | | **0** |
| poprz. 7 d | `api_error` 403 | | 24 zd., najwięcej `get_user_profile_and_subscription` 14 / 2 os.; reszta po 1 (live-session, character_card, ke/sheet, period_card) |

Co robią po trafieniu w limit (14 d, kolejne 24 h): `usage_limit_panel_shown` 3 os. -> 3 paywall -> 2 start -> 1 zakup; `habit_limit_reached` 2 -> 2 paywall -> 1 start -> 0; `reflect_limit_hit` 2 -> 2 paywall -> 2 start -> 1 zakup. Na 2.0.117 nikt realny nie trafił w limit.

## Porównanie z baseline (2026-10-15, okres PO 03-15.10)

| miara | baseline PO (13 d) | poprz. 7 d | ost. 48 h |
|---|---|---|---|
| zakupy ukończone (realni, zdedup.) | 6 os. | 3 (Android) | 0 |
| zakupy iOS | 0 | 0 | 0 |
| `purchase_failed` realni | 0 | 0 | 0 |
| triale / dobę | 54 / 13 d = 4,2 | 4,0 | 3,0 |
| zakupy roczne | 0 | 0 | 0 |

## Zastrzeżenia

- **Za mało danych na jakikolwiek wniosek o konwersji na 2.0.117**: 7 realnych osób, 2 widziały paywall, 0 startów zakupu. "Zakup działa na 2.0.117" jest **niezweryfikowane** na obu platformach, nie "zepsute".
- **Android 2.0.117 na urządzeniu testera daje `products_not_found`** (5x). To typowe dla buildu spoza Play (sideload / debug signing), ale trzeba to wykluczyć instalacją z Play na koncie license testera.
- k-anonimowość: wszystkie segmenty mają n<25. Zgodnie z konwencją baseline podaję liczby 5-24 jawnie i n<5 jako "n<5" (z wartością w nawiasie tam, gdzie to zachowanie zakupowe, nie dane zdrowotne). Zero danych zdrowotnych, treści, ID.
- Podwójna emisja zakupu (klient + backend); backend z `$os=Windows` to lokalny backend piszący do prod PostHoga. Jednorazowy starter pack klient raportuje jako `subscription_purchase_completed`.
- `trial_ended` nie raportuje wygaśnięć; brak zdarzeń anulowania/wygaśnięcia subskrypcji.
- `api_error` nie ma wersji aplikacji, więc 403 nie da się przypisać do 2.0.117.
- Filtr testerów jest heurystyką (Android bez `$is_testflight`; Play license testers mogą przejść jako realni).
- Wersje 2.0.113-2.0.116 z 19.10 to głównie testerzy; "nowa wersja" = tylko 2.0.117.

## Zapytania (HogQL, dosłownie)

Pliki źródłowe: `main.sql`, `b2.sql` w scratchpadzie sesji. Kluczowe:

```sql
-- filtr testerów (CTE t)
WITH t AS (SELECT person_id FROM events WHERE timestamp > now() - INTERVAL 21 DAY AND properties.$lib='posthog-flutter' GROUP BY person_id
 HAVING countIf(properties.$is_testflight = true) > 0 OR countIf(properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro') OR properties.$is_emulator = true) > 0 OR count(DISTINCT properties.$app_version) >= 12 OR countIf(event = 'onboarding_completed') >= 3)

-- paywall per trigger
SELECT if(timestamp > now() - INTERVAL 48 HOUR,'2_last48h','1_prev7d') w, person_id IN (SELECT person_id FROM t) testers, properties.trigger_feature trig, count() ev, count(DISTINCT person_id) users
FROM events WHERE event='paywall_shown' AND timestamp > now() - INTERVAL 9 DAY GROUP BY w, testers, trig ORDER BY w, testers, users DESC LIMIT 60

-- lejek per osoba
SELECT w, testers, os, countIf(shown) u_shown, countIf(opened) u_screen, countIf(sel_user) u_sel_user, countIf(sel) u_sel_any, countIf(st) u_started, countIf(pend) u_pending,
 countIf(comp_c) u_comp_client, countIf(comp_b) u_comp_backend, countIf(comp_c OR comp_b) u_comp_any, countIf(fail) u_failed, countIf(dism) u_dismissed, countIf(dism_att) u_dism_after_attempt,
 countIf(rest) u_restore, countIf(trial) u_trial_started, countIf(otp) u_one_time
FROM (SELECT person_id, if(timestamp > now() - INTERVAL 48 HOUR,'2_last48h','1_prev7d') w, person_id IN (SELECT person_id FROM t) testers,
  any(if(properties.$lib='posthog-flutter', properties.$os, NULL)) os,
  countIf(event='paywall_shown')>0 shown, countIf(event='subscription_screen_opened')>0 opened,
  countIf(event='subscription_product_selected' AND properties.selection_source='user')>0 sel_user,
  countIf(event='subscription_product_selected')>0 sel, countIf(event='subscription_purchase_started')>0 st, countIf(event='subscription_purchase_pending')>0 pend,
  countIf(event='subscription_purchase_completed' AND properties.$lib='posthog-flutter')>0 comp_c,
  countIf(event='subscription_purchase_completed' AND properties.$lib='posthog-python' AND properties.$os!='Windows')>0 comp_b,
  countIf(event='subscription_purchase_failed')>0 fail, countIf(event='paywall_dismissed')>0 dism,
  countIf(event='paywall_dismissed' AND properties.purchase_attempted=true)>0 dism_att,
  countIf(event LIKE 'subscription_restore_%')>0 rest, countIf(event='trial_started')>0 trial, countIf(event='one_time_purchase_completed')>0 otp
 FROM events WHERE timestamp > now() - INTERVAL 9 DAY AND event IN ('paywall_shown','subscription_screen_opened','subscription_product_selected','subscription_purchase_started','subscription_purchase_pending','subscription_purchase_completed','subscription_purchase_failed','paywall_dismissed','subscription_restore_started','subscription_restore_completed','subscription_restore_empty','subscription_restore_failed','trial_started','one_time_purchase_completed')
 GROUP BY person_id, w)
GROUP BY w, testers, os ORDER BY w, testers, os

-- błędy
SELECT if(timestamp > now() - INTERVAL 48 HOUR,'2_last48h','1_prev7d') w, event, properties.$lib lib, properties.$os os, properties.failure_reason fr, properties.reason r, properties.error_code ec, count() c, count(DISTINCT person_id) users
FROM events WHERE timestamp > now() - INTERVAL 9 DAY AND event IN ('subscription_purchase_failed','subscription_verification_failed','paywall_load_failed','subscription_stale_transaction_finished','subscription_restore_failed')
GROUP BY w, event, lib, os, fr, r, ec ORDER BY w, c DESC LIMIT 40

-- 403 po endpointach
SELECT if(timestamp > now() - INTERVAL 48 HOUR,'2_last48h','1_prev7d') w, properties.status_code sc, properties.endpoint ep, properties.error_class ec, count() c, count(DISTINCT person_id) users
FROM events WHERE event='api_error' AND timestamp > now() - INTERVAL 9 DAY AND toString(properties.status_code) IN ('402','403','429')
GROUP BY w, sc, ep, ec ORDER BY w, c DESC LIMIT 40

-- limit -> co dalej w 24 h
SELECT l.event lim, count(DISTINCT l.person_id) users,
 count(DISTINCT if(n.event='paywall_shown', l.person_id, NULL)) then_paywall,
 count(DISTINCT if(n.event='subscription_purchase_started', l.person_id, NULL)) then_started,
 count(DISTINCT if(n.event='subscription_purchase_completed', l.person_id, NULL)) then_bought
FROM (SELECT person_id, event, min(timestamp) ts FROM events WHERE timestamp > now() - INTERVAL 14 DAY AND event IN ('usage_limit_panel_shown','habit_limit_reached','reflect_limit_hit') GROUP BY person_id, event) l
LEFT JOIN (SELECT person_id, event, timestamp FROM events WHERE timestamp > now() - INTERVAL 14 DAY AND properties.$lib='posthog-flutter') n ON n.person_id = l.person_id AND n.timestamp > l.ts AND n.timestamp < l.ts + INTERVAL 24 HOUR
GROUP BY lim

-- starty bez wyniku w 1 h (30 d)
SELECT s.os, s.ver, count() starts, countIf(o.n_out = 0) starts_no_outcome_1h, count(DISTINCT s.person_id) users
FROM (SELECT person_id, timestamp ts, properties.$os os, properties.$app_version ver FROM events WHERE event='subscription_purchase_started' AND timestamp > now() - INTERVAL 30 DAY) s
LEFT JOIN (
  SELECT st.person_id pid, st.ts sts, countIf(e.timestamp >= st.ts AND e.timestamp <= st.ts + INTERVAL 1 HOUR) n_out
  FROM (SELECT person_id, timestamp ts FROM events WHERE event='subscription_purchase_started' AND timestamp > now() - INTERVAL 30 DAY) st
  JOIN (SELECT person_id, timestamp FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND event IN ('subscription_purchase_completed','subscription_purchase_failed','subscription_purchase_pending','one_time_purchase_completed') AND properties.$lib='posthog-flutter') e ON e.person_id = st.person_id
  GROUP BY pid, sts) o ON o.pid = s.person_id AND o.sts = s.ts
GROUP BY s.os, s.ver ORDER BY s.ver LIMIT 30
```
