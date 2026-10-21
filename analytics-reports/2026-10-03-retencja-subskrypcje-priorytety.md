# Retencja i subskrypcje: co w produkcie poprawić najpierw. Raport priorytetów

- **Data**: 2026-10-03
- **Analityk**: growth-analyst
- **Pytanie biznesowe**: które elementy aplikacji, oglądane jak przez użytkownika i potwierdzone danymi, najbardziej ograniczają retencję (powrót w dniach 1-30) i liczbę subskrypcji, oraz co zmienić w jakiej kolejności.
- **Metryki sukcesu**: powrót nowego zarejestrowanego użytkownika w dniach 1-7 (dziś 20-30%) i D1 (dziś 12-16% dla kohort sierpień/wrzesień); dla monetyzacji odsetek kohorty, który zobaczył ofertę, i zakupy na 100 rejestracji.
- **Okno danych**: kohorty rejestracji 2026-06-01 do 2026-09-25; zdarzenia z ostatnich 30-60 dni do 2026-10-03 12:00 UTC.
- **Źródła**: PostHog (projekt 141170, HogQL read-only przez `scripts/posthog_query.py`), kod frontu `mindsync-frontend/mindsync_app/lib/` (nazwy funkcji i bramek), kod backendu `MindSync/app/` (generatory powiadomień, podsumowania), wcześniejsze raporty: `2026-09-12-diagnoza-retencja-monetyzacja.md`, `2026-09-25-usage-trend-and-paywall-exposure.md`, `2026-08-10-activation-definition.md`, `2026-09-13-audyt-modelu-powiadomien.md`, spec `design-specs/2026-10-02-subscription-onboarding/SPEC.md`. Prod Postgres nie był odpytywany (nie było to konieczne; prawda przychodowa z raportu DB z 2026-09-12).
- **Pewność**: **średnia**. Kierunek ustaleń o retencji jest spójny z trzema wcześniejszymi raportami i z kodem. Większość liczników na poziomie funkcji ma n poniżej 25, więc są kierunkowe. Redesign subskrypcji wszedł dziś, więc jego skuteczności nie da się jeszcze ocenić.

Konwencja: **[DOWÓD]** = liczba z PostHoga albo plik:linia; **[HIPOTEZA]** = wyjaśnienie przyczyny, które trzeba potwierdzić testem. Wszystkie liczby użytkowników to osoby z klienta (`$lib='posthog-flutter'`), bez farmy urządzeń (`OnePlus8Pro`, `Pixel 6 Pro`). Segmenty poniżej 25 osób są podane tylko kierunkowo.

---

## Streszczenie

- **Retencja przegrywa w dniach 2-7, nie w onboardingu i nie na paywallu.** 80% nowych zarejestrowanych (215 z 270) w pierwszej dobie nie robi ani zapisu terapii, ani Reflect, i z nich wraca 14%. Ci, którzy zrobili zapis, wracają w 44%, a ci po Reflect w 38%. Ekran pierwszego kroku wdrożony dziś celuje dokładnie w ten moment, więc trzeba go zmierzyć, zanim zbuduje się coś nowego.
- **Kanał push jest spalony na podsumowaniach dla martwych kont.** W 30 dni wysłano 8 798 powiadomień do 1 841 osób, z czego 97% to "Weekly/Monthly summary ready" bez progu aktywności (`MindSync/app/tasks/weekly_therapy_summary.py:44`, `:394`). Otwarto je 4 razy. Tylko 33% nowych użytkowników dostaje w pierwszym tygodniu jakiekolwiek powiadomienie zachęcające do działania. Zgoda na push nie jest problemem (81 z 100 pytanych się zgodziło), problemem jest treść i rytm.
- **Ekran główny jest zbudowany wokół sesji terapii i nie zmienia się dla osób, które nie są w terapii.** Pierwsza karta to "Next session", a pusty stan brzmi "No upcoming sessions scheduled." (`main_tab_cubit.dart:53`, `app_en.arb:637`). W kodzie ekranu głównego nie ma żadnego odwołania do statusu terapii. Trzy najczęstsze błędy w aplikacji to zaprojektowane 404 pustych stanów (`/prep-cards/latest` 50 osób, 1 128 razy).
- **Monetyzacja: jedyną ofertą, jaką widzi większość, jest ta zaraz po onboardingu, a dziś obie próby jej pokazania skończyły się pominięciem** (`post_onboarding_offer_not_shown`, reason `already_premium`, 2 z 2, w tym 1 TestFlight). Do tego `paywall_load_failed` 6 razy. Próba jest za mała, żeby to nazwać błędem, ale trzeba to sprawdzić w tym tygodniu, bo od tej jednej oferty zależy cały nowy lejek.
- **Uwaga na nowe liczby:** od 2026-09-20 liczba nowych osób w apce skoczyła z ~21 do 72 na tydzień (Android, tanie urządzenia, Wybrzeże Kości Słoniowej, Algieria, Iran, Irak, Pakistan), a odsetek, który zakłada konto, spadł z 64% do 28%. MAU 30d wynosi przez to 203, a nie ~111. Każdy odczyt retencji z najbliższych tygodni trzeba dzielić na ten ruch i resztę, inaczej redesign dostanie niezasłużoną ocenę.

---

## Kluczowe metryki

| Metryka | Wartość | Trend | Benchmark | Ocena |
|---|---|---|---|---|
| D1 kohorty zarejestrowanych (cze / lip / sie / wrz) | 7,6% / 7,7% / 12,2% / 16,3% (n=105/52/74/43) | ▲ | 26-35% health & fitness (raport 09-25) | daleko poniżej, poprawa |
| Powrót w dniach 1-7 (cze / lip / sie / wrz) | 20,0% / 25,0% / 29,7% / 25,6% | ▲ słabo | brak | niski |
| Powrót w dniach 8-30 (cze / lip / sie) | 17,1% / 13,5% / 29,7% | ▲ | D30 ~3-4% rynek (raport 09-25) | sierpień nietypowo dobry, n=74 |
| Nowi bez zapisu i bez Reflect w 1. dobie | 79,6% (215/270) | brak | brak | główny wyciek |
| Zgoda na push (60d) | 81 zgód / 100 zapytań | brak | brak | dobra |
| Powiadomienia "summary ready" w puli 30d | 97,0% (8 532/8 798) | brak | brak | kanał spalony |
| Otwarcia `moment.opened` 30d | 17 zdarzeń, 12 osób | brak | brak | ~0 |
| Nowi z pushem zachęcającym w 1. tygodniu | 32,5% (41/126) | brak | brak | za mało |
| `inapp_insight.shown` od 2026-08-24 | 0 | ▼ | brak | warstwa nagrody nie działa |
| Nowe osoby/tydz. (09-06 / 09-13 / 09-20 / 09-27) | 22 / 21 / 39 / 72 | ▲ | brak | zmiana miksu, nie wzrost |
| Odsetek nowych, którzy założyli konto | 64% / 57% / 38% / 28% | ▼ | brak | ruch niskiej intencji |
| Użytkownicy Reflect ponad 15 wiadomości/mies. (wrz) | 8 z 17 (n<25) | brak | brak | jedyny limit, który wiąże |
| Retencja płacących (DB, 09-12) | 7/37 = 18,9% | brak | brak | płacący też odchodzą |

---

## Część A. Retencja (uszeregowane wg wpływu)

### R1. Brak powodu do powrotu w dniach 2-7: push idzie do martwych kont, a nowi go nie dostają · Wpływ: Krytyczny · Pewność: wysoka (mechanizm), średnia (wielkość efektu)

- **[DOWÓD]** 30 dni: `moment.sent` = 8 798 zdarzeń do 1 841 osób. `WEEKLY_SUMMARY_READY` 6 794 (1 825 osób, 4 otwarcia), `MONTHLY_SUMMARY_READY` 1 738 (0 otwarć). Zachęty do działania to margines: `REFLECTION_INVITATION` 59, `THERAPY_RELATIONSHIP_CHECKIN` 57, `RE_ENGAGEMENT` 40, `MOOD_UPDATE_REQUEST` 8, `DAILY_CHECK_IN` 1. Do 65 osób z MAU trafiło tylko 406 wysyłek (4,6% puli). Zapytania: `moments_by_type_30d`, `moments_to_active_users_30d` (Załącznik, Q3).
- **[DOWÓD]** Tygodniowe podsumowanie nie ma progu aktywności: "No minimum-activity gate: every user with an elapsed period gets a card" (`MindSync/app/tasks/weekly_therapy_summary.py:44` i `:394`), a hook pusha strzela po każdej karcie (`MindSync/app/services/moment_hooks.py:223-232`).
- **[DOWÓD]** Nowi użytkownicy 2026-08-15 do 09-25 (n=126): 41 (32,5%) dostało w pierwszych 7 dniach jakiekolwiek powiadomienie inne niż podsumowanie (Q4).
- **[DOWÓD]** Zgoda nie jest wąskim gardłem: 81 `notification_permission_granted` na 100 `notification_permission_prompted` w 60 dniach. Sama zgoda w 1. dobie nie podnosi powrotu (17,9%, 7/39, n<25), czyli dziś push nie niesie żadnej wartości.
- **[HIPOTEZA]** Użytkownik, który w dniu 0 zrobił coś raz, nie dostaje w dniach 1-6 nic, co odwołuje się do tego, co powiedział w onboardingu (obszary, intensywność, plan sesji). Pierwszy kontakt to w praktyce "Your weekly summary is ready" po tygodniu, często nad pustą kartą. To uczy ignorowania powiadomień, a dla 1 800 uśpionych kont to sygnał do odinstalowania.
- **Zmiana**:
  1. Wyłączyć push "summary ready" (i generowanie karty) dla kont bez żadnej aktywności w danym okresie. Raport 09-12 rekomendował to jako A2 ze względu na koszt, tu jest drugi powód: retencja i reputacja kanału.
  2. Zbudować sekwencję pierwszego tygodnia dla nowych: dzień 1, 2, 4 i 6, każda z jednym konkretnym, krótkim działaniem dopasowanym do obszaru wybranego w onboardingu (30-sekundowy check-in, jedno pytanie do Reflect, "przygotuj się do czwartkowej sesji" gdy jest plan). Szablony wystarczą, AI nie jest potrzebne (open rate AI vs szablon nadal niezmierzony).
- **Wysiłek**: M (backend `data-analytics` dla generatorów i progu; `ui-ux-designer` dla treści i rytmu, ważne dla grupy wrażliwej: łagodnie, z łatwym wyciszeniem).
- **Pomiar**: powrót w dniach 1-7 kohorty zarejestrowanych (cel: z ~25% do 35%), `moment.opened` / `moment.sent` per `moment_type` dla nowych w 1. tygodniu, odsetek wyłączeń powiadomień (`notification_master_toggled`) jako zabezpieczenie. Okno: 2 kohorty miesięczne.

### R2. Pierwsza doba: 80% nowych nie robi niczego wartościowego · Wpływ: Krytyczny · Pewność: wysoka (korelacja), przyczynowość niepotwierdzona

- **[DOWÓD]** Kohorta zarejestrowanych 2026-06-01 do 09-23, n=270, powrót w dniach 1-7 (Q2):

| Działanie w 1. dobie | n | Wróciło d1-7 | % |
|---|---|---|---|
| Wszyscy | 270 | 54 | 20,0% |
| Zapis terapii (After/Before therapy, Between Sessions, nagranie, quick capture) | 34 | 15 | 44,1% (n<25 licznik) |
| Brak zapisu | 236 | 39 | 16,5% |
| Reflect | 37 | 14 | 37,8% |
| Check-in (`symptom_scored` / `health_check_completed`) | 35 | 13 | 37,1% |
| Ukończony onboarding | 120 | 35 | 29,2% |
| Ani zapis, ani Reflect | 215 | 30 | 14,0% |

- **[DOWÓD]** Tylko 120 z 270 (44%) kończy onboarding w 1. dobie (część to logowania na nowym urządzeniu, więc to dolna granica). Przed redesignem `first_capture_prompt_shown` 88 osób, `first_capture_prompt_dismissed` 20 (60 dni).
- **[DOWÓD]** Po zapisie użytkownik od razu widzi kartę z wynikiem AI (`debrief_capture_screen.dart:935-1013`), więc gdy "aha" nastąpi, jest dowiezione. Problem jest w tym, żeby do niego doszło.
- **[HIPOTEZA]** Ekran pierwszego kroku daje 4-5 równorzędnych opcji plus "Take me to the app" (`lib/screens/wow/views/first_step_view.dart:99-145`). Przy tej grupie (zmęczenie, niepewność, co powiedzieć) wybór między czterema drogami i wyjście awaryjne obok wygrywa wyjście.
- **Zmiana**: najpierw zmierzyć to, co weszło dziś (ten ekran jest właściwą odpowiedzią). Potem, jeśli odsetek zapisu w 1. dobie nie przekroczy 25%: jedno główne wezwanie dopasowane do statusu terapii (w terapii: "Capture a past session"; poza terapią: 30-sekundowy check-in albo jedno pytanie Reflect), reszta zwinięta. Test 50/50 na fladze.
- **Wysiłek**: S (pomiar), M (wariant ekranu).
- **Pomiar**: odsetek zarejestrowanych z zapisem lub Reflect w 24 h (dziś 20,4%; cel 30%), `first_capture_prompt_option_tapped` / `first_capture_prompt_shown`, powrót d1-7 w obu ramionach.

### R3. Ekran główny nie pasuje do osób spoza terapii i wita pustymi stanami · Wpływ: Wysoki · Pewność: średnia

- **[DOWÓD]** Kolejność kart jest stała: `next_session`, `habits`, `mood_trend`, `health_check_banner`, `weekly_observations`, `affirmation` (`lib/screens/main_tab/cubit/main_tab_cubit.dart:53-60`). Ekran główny nie czyta statusu terapii (zero trafień `inTherapy` / `currently_in_therapy` w `lib/screens/main_tab/`). Pusty stan pierwszej karty: "No upcoming sessions scheduled." (`lib/l10n/app_en.arb:637`).
- **[DOWÓD]** Najczęstsze 404 w 30 dniach to puste stany: `/prep-cards/latest` 50 osób (1 128 razy), `/debriefs/latest` 49 (994), `/health-check/latest` 47 (789). Karty "Mood & symptom trends" i "Weekly observations" przy braku danych renderują nic (`mood_trend_card.dart` `SizedBox.shrink`, `weekly_observations_card.dart:43`), więc nowy użytkownik widzi głównie pusty kalendarz sesji i kartę "Getting started".
- **[DOWÓD]** Onboarding od dziś rozgałęzia się dla osób spoza terapii (5 kroków zamiast 7, SPEC FE-C), a ekran Reveal ma wariant "Your first week". Ekran główny tego rozgałęzienia nie kontynuuje.
- **[HIPOTEZA]** Osoba, która nie chodzi na terapię albo dopiero szuka terapeuty, widzi aplikację o czymś, czego nie ma, i nie ma tam dla niej codziennej czynności. Tego nie da się dziś potwierdzić liczbą, bo statusu terapii świadomie nie wysyłamy do PostHoga (Art. 9). `total_steps` (5 vs 7) z nowego onboardingu da agregatowy podział, ale wymaga decyzji prawnika (M-3 z audytu bezpieczeństwa).
- **Zmiana**: wariant ekranu głównego dla "poza terapią / bez planu sesji": na górze dzisiejsza czynność (check-in, pytanie Reflect, nawyk), karta sesji niżej jako "Masz terapeutę? Dodaj sesję". Dla wszystkich: pusty stan zamiast "nic" pokazuje, co pojawi się po pierwszym zapisie.
- **Wysiłek**: M (`ui-ux-designer` spec, `flutter-mobile`).
- **Pomiar**: D7 nowych z gałęzi 5-krokowej vs 7-krokowej (po zgodzie prawnika na agregat), odsetek nowych z jakimkolwiek działaniem w dniach 1-3.

### R4. Nie ma lekkiej codziennej pętli ani nagrody, która by ją domykała · Wpływ: Wysoki · Pewność: średnia

- **[DOWÓD]** Zasięg funkcji w 30 dniach (osoby): `timeline_viewed` 63, `workspace_opened` 44, `character_card_viewed` 43, `bio_viewed` 40, `habit_tracker_viewed` 35, `reflect_session_started` 26, `goal_created` 15, `health_check_completed` 15, `summary_viewed` 14, `symptom_scored` 13, `between_session_created` 12, `debrief_created` 11, **`habit_check_toggled` 7**, `prep_card_created` 7, `recording_upload_completed` 1 (Q9). Ludzie najczęściej oglądają siebie (oś czasu, bio, postać), a rzadko coś robią.
- **[DOWÓD]** Warstwa nagrody praktycznie nie istnieje: `inapp_insight.shown` 0 od 2026-08-24, `inapp_insight.generated` 4 we wrześniu (2 osoby), `realization_viewed` we wrześniu 2 osoby (Q12).
- **[DOWÓD]** Check-in w 1. dobie koreluje z powrotem równie mocno jak Reflect (37,1% vs 20,0% średnio, n=35), a jest najtańszą czynnością w aplikacji.
- **[HIPOTEZA]** Pętla (wyzwalacz, działanie, nagroda, inwestycja) istnieje tylko wokół sesji terapii, która zdarza się raz na 1-2 tygodnie. Codzienne elementy (afirmacja, nawyk) nie mają nagrody, która pokazuje postęp, więc nie tworzą nawyku. To ten sam "frequency mismatch" co w raporcie 09-12, teraz widoczny w kodzie ekranu głównego.
- **Zmiana**: jedna codzienna czynność 30-sekundowa (check-in nastroju albo odhaczenie nawyku) z natychmiastowym lustrem ("3 dni z rzędu, nastrój w tym tygodniu wyżej niż w poprzednim") i licznikiem dni na ekranie głównym. Osobno: zdecydować, czy pipeline `inapp_insight` naprawić, czy wyłączyć (generuje, nie pokazuje).
- **Wysiłek**: M.
- **Pomiar**: osoby z aktywnością w co najmniej 3 różnych dniach tygodnia (WAU 3+ dni), DAU/MAU (dziś ~8,6%), `habit_check_toggled` i `symptom_scored` na aktywnego.

### R5. Zmiana źródła ruchu zafałszuje każdą ocenę zmian · Wpływ: Wysoki dla decyzji (nie dla użytkowników) · Pewność: wysoka

- **[DOWÓD]** Nowe osoby w apce na tydzień: 22 / 21 / 39 / 72 (tygodnie od 09-06), z kontem 14 / 12 / 15 / 20, czyli odsetek rejestracji 64% → 28%. Od 09-20 kraje: US 15, CI 9, DZ 7, IR 7, IQ 6, PK 6, SA 4, DE 4 i kilkanaście innych; urządzenia głównie Samsung A0x, Tecno, Infinix, itel; prawie wyłącznie Android (68 z 72 w ostatnim tygodniu). `install_source` = `google-play` 141 osób, zero UTM (Q5-Q7).
- **[HIPOTEZA]** To organiczna ekspozycja w Google Play na nowych rynkach (zmiana listingu, nowe frazy albo efekt bloga), nie kampania. Ten ruch ma niską intencję (aplikacja jest po angielsku i dla osób w terapii), więc obniży D1 i konwersję niezależnie od jakości redesignu.
- **Zmiana**: (1) w każdym odczycie retencji i lejka od 2026-09-20 dzielić na "rynki dotychczasowe" i "nowa fala"; (2) sprawdzić w Play Console, skąd przyszły instalacje (wyszukiwanie, frazy, kraje) i czy listing nie wymaga zawężenia krajów albo języka.
- **Wysiłek**: S (`posthog-data-extractor` segment, `integration-devops` Play Console).
- **Pomiar**: odsetek rejestracji per kraj, D1 per segment.

---

## Część B. Monetyzacja (uszeregowane wg wpływu)

Kontekst, którego nie należy zgubić: retencja płacących to 7/37 = 18,9% (DB, 09-12), a 71% zarejestrowanych odchodzi przed końcem 4-dniowego triala (raport 09-25). Każda zmiana w monetyzacji mnoży to, co dowiezie retencja.

### M1. Oferta po onboardingu to jedyna oferta, którą zobaczy większość, a dziś 2 z 2 pokazań zostały pominięte · Wpływ: Krytyczny · Pewność: niska (n=2), ryzyko wysokie

- **[DOWÓD]** 2026-10-03: `post_onboarding_offer_not_shown` 2 zdarzenia, 2 osoby, `reason = already_premium` (1 to TestFlight). `paywall_load_failed` 6 zdarzeń u 1 osoby (`trigger_feature` `drawer_menu` 5, `premium_gate_habits` 1, `error_type` `_Exception`). `usage_load_failed` 5 zdarzeń u 2 osób (Q10, Q11).
- **[DOWÓD]** Warunek pominięcia: aktywna subskrypcja i `premiumSource` równe `null`, `purchase` albo `starterPack` (`lib/screens/wow/cubit/wow_cubit.dart:268-272`). Backend dla triala ustawia `granted_via = signup_trial` (`MindSync/app/api/v1/endpoints/users.py:161`), więc w teorii nowy użytkownik ofertę dostanie. `null` zdarza się, gdy nie ma wiersza subskrypcji albo pochodzi sprzed migracji (`users.py:1092-1095`). Brak produktów ze sklepu też po cichu pomija ofertę (`products_unavailable`, `wow_cubit.dart:280-286`).
- **[HIPOTEZA]** Dwa dzisiejsze przypadki to najpewniej konta testowe z wcześniejszym zakupem. Gdyby jednak u prawdziwych nowych kont przychodziło `null` albo produkty nie ładowały się na części Androidów, nowy lejek byłby pusty od pierwszego dnia, a nikt by tego nie zauważył, bo pominięcie nie jest błędem.
- **Zmiana**: w ciągu 7 dni od wydania sprawdzić odsetek `post_onboarding_offer_*` (pokazana / pominięta wg `reason`) wśród osób z `onboarding_completed`, z podziałem na platformę. Cel: oferta pokazana co najmniej 85% kończących onboarding z aktywnym trialem. Rozbić `paywall_load_failed` na platformę i typ błędu.
- **Wysiłek**: S (`posthog-data-extractor`; poprawki ewentualnie `flutter-mobile`).
- **Pomiar**: jak wyżej, plus `post_onboarding_offer_result` wg wyniku.

### M2. Najczęściej oglądane miejsca nie sprzedają niczego, a premium jest opisane jako większe limity · Wpływ: Wysoki · Pewność: średnia

- **[DOWÓD]** Najczęściej odwiedzane powierzchnie to oś czasu (63 osoby/30d), workspace (44), karta postaci (43), bio (40). Rekomendacja 3 z raportu 09-25 (CTA na miękkich blokadach: narracja celów, sugerowane pytania w health check, migawki 30/90 dni) nie weszła do zakresu redesignu (SPEC FE-A..FE-E jej nie obejmuje).
- **[DOWÓD]** Tabela porównawcza na paywallu to w 8 z 10 wierszy ilości ("1 a month / Unlimited", "2 in total / Unlimited"), a 2 wiersze to "Included / Included" (SPEC FE-A, `SPEC.md:83`). Retained free users mają średnio 1,7 aktywnego dnia w miesiącu i do limitów nie dochodzą (raport 09-25).
- **[HIPOTEZA]** Ktoś, kto nie dochodzi do limitu, nie ma w tabeli nic do kupienia. Premium sprzedaje się lepiej jako wynik ("pełny miesięczny obraz Twojej terapii", "rozmowa głosowa", "karta przygotowania gotowa przed każdą sesją") niż jako licznik.
- **Zmiana**: (1) CTA z `trigger_feature = premium_gate_<funkcja>` na istniejących miękkich blokadach i na końcu bio / osi czasu ("zobacz pełny obraz miesiąca"); (2) nagłówek paywalla i 3 pierwsze wiersze tabeli przepisać na wyniki, limity zostawić niżej. Test A/B tekstu.
- **Wysiłek**: M (`ui-ux-designer`, `brand-voice-manager` copy, `flutter-mobile`).
- **Pomiar**: odsetek MAU z co najmniej jednym `paywall_shown` w 30 dniach (dziś 3,9%), `paywall_shown` → `subscription_purchase_started` per `trigger_feature`.

### M3. Reflect to jedyny limit, który realnie wiąże, i jednocześnie najsilniejsza czynność retencyjna · Wpływ: Wysoki · Pewność: niska (n<25)

- **[DOWÓD]** Wrzesień: 17 osób wysłało `reflect_message_submitted`, 8 z nich ponad 15 wiadomości (5 ponad 30). Sierpień: 11 osób, 5 ponad 15 (Q8). Nowy limit to 15 wiadomości miesięcznie (było 30, SPEC §1). Reflect w 1. dobie: powrót 37,8% vs 17,2%.
- **[HIPOTEZA]** Po końcu triala limit 15 wiadomości to jedna rozmowa. To dobre miejsce na paywall, bo ludzie faktycznie tam dochodzą. Ryzyko: odcina też czynność, która najmocniej koreluje z powrotem, więc może obniżyć retencję wolnych użytkowników, z których część kupiłaby później.
- **Zmiana**: przy wyczerpaniu limitu Reflect pokazać, co rozmowa już dała (podsumowanie wątku jest generowane, `reflect_summary_generated`), i dopiero wtedy ofertę, w tym starter pack. Na kolejne kohorty: flaga 15 vs 30 z pomiarem D30 i zakupów na 100 rejestracji.
- **Wysiłek**: S (komunikat), M (test).
- **Pomiar**: `paywall_shown` z `premium_gate_reflect_messages` → zakup, D30 obu ramion.

### M4. Płacący odchodzą, a nie wiemy dlaczego · Wpływ: Wysoki · Pewność: wysoka (fakt), brak danych o przyczynie

- **[DOWÓD]** 7/37 kont kiedykolwiek płacących ma dziś premium (18,9%, DB 09-12). Nie ma zdarzenia z powodem rezygnacji. Od dziś płynie `premium_manage_tapped` (wyjście do zarządzania subskrypcją w sklepie).
- **[HIPOTEZA]** Płacący dostają te same funkcje co wcześniej, tylko bez limitów, a te same luki z R1 i R4 (brak codziennej pętli, push o pustych podsumowaniach) dotyczą ich tak samo.
- **Zmiana**: (1) po `premium_manage_tapped` jedno pytanie "co nie zadziałało" (enum, bez wolnego tekstu); (2) dla płacących miesięcznie po 2. odnowieniu propozycja rocznego; (3) przy nieudanym odnowieniu (Google grace period / Apple billing retry) push z prośbą o aktualizację płatności.
- **Wysiłek**: S-M (`flutter-mobile`, `backend-api` dla statusów odnowień).
- **Pomiar**: retencja płacących miesiąc do miesiąca z `subscription_receipts`, rozkład powodów.

### M5. Nie znamy ceny ani przychodu na użytkownika · Wpływ: Średni (blokuje decyzje cenowe) · Pewność: wysoka

- **[DOWÓD]** `subscription_receipts` nie ma kwoty ani waluty (raport 09-12). Dzisiejsze `subscription_purchase_completed` część zdarzeń ma `product_id` null i system Linux/Windows (zdarzenia z backendu albo testów), więc liczenie zakupów z PostHoga bez filtra `$lib` daje fałszywy wynik (Q11).
- **Zmiana**: dopisać cenę i walutę (z obiektu produktu sklepu) do `subscription_purchase_completed` po stronie klienta; ceny Monthly/Annual/starter odczytać z App Store Connect i Play Console i zapisać w raporcie bazowym.
- **Wysiłek**: S (`flutter-mobile`, `integration-devops`).
- **Pomiar**: przychód na 100 rejestracji, udział Annual.

### M6. Trial krótszy niż cykl terapii (otwarte z 09-25) · Wpływ: Średni · Pewność: średnia

- **[DOWÓD]** Trial serwerowy 4 dni zostaje (SPEC §1); starter $5 na 2 tygodnie jest płatnym przedłużeniem. Cykl sesji to 1-2 tygodnie (raport 09-12).
- **Zmiana**: niczego nie zmieniać przez pierwsze 4 tygodnie po redesignie; potem, jeśli starter kupuje mniej niż 3% osób, które zobaczyły ofertę, test 7-dniowego triala (rekomendacja 2 z 09-25).
- **Wysiłek**: M. **Pomiar**: `post_onboarding_offer_result` = `purchased_starter`, zakupy na 100 rejestracji.

---

## Rekomendacje w kolejności (wpływ × pewność × wysiłek)

| # | Działanie | Obszar | Wysiłek | Właściciel | Oczekiwany efekt | Jak mierzymy |
|---|---|---|---|---|---|---|
| 1 | Sprawdzić, czy oferta po onboardingu się pokazuje (reason, platforma) i co z `paywall_load_failed` | Monetyzacja | S | `posthog-data-extractor` → `flutter-mobile` | oferta dla ≥85% kończących onboarding | `post_onboarding_offer_*` / `onboarding_completed`, 7 dni |
| 2 | Dzielić wszystkie odczyty od 09-20 na "nowa fala" i resztę; Play Console: skąd instalacje | Pomiar | S | `posthog-data-extractor`, `integration-devops` | poprawna ocena redesignu | D1 per segment |
| 3 | Zatrzymać push i generowanie "summary ready" dla kont bez aktywności w okresie | Retencja | S-M | `data-analytics` | mniej szumu, koszt w dół, mniej odinstalowań | `moment.sent` per typ, wyłączenia powiadomień |
| 4 | Sekwencja pierwszego tygodnia (dni 1, 2, 4, 6), szablony dopasowane do onboardingu | Retencja | M | `ui-ux-designer` → `data-analytics` | powrót d1-7 z ~25% do 35% | kohorta zarejestrowanych, 2 miesiące |
| 5 | Zmierzyć ekran pierwszego kroku; jeśli zapis w 24 h <25%, wariant z jednym głównym wezwaniem | Retencja | S/M | `flutter-mobile` | zapis lub Reflect w 24 h z 20% do 30% | `first_capture_prompt_*`, kohorta |
| 6 | Ekran główny w wariancie "poza terapią" i puste stany z obietnicą | Retencja | M | `ui-ux-designer` → `flutter-mobile` | wyższe D7 gałęzi 5-krokowej | D7 per gałąź (agregat, po zgodzie prawnika) |
| 7 | Codzienna 30-sekundowa czynność z lustrem postępu i licznikiem dni; decyzja o `inapp_insight` | Retencja | M | `ui-ux-designer`, `flutter-mobile`, `data-analytics` | DAU/MAU z 8,6% do 12% | WAU 3+ dni |
| 8 | CTA na miękkich blokadach i bio/osi czasu; paywall opisany wynikami, nie limitami | Monetyzacja | M | `ui-ux-designer`, `brand-voice-manager`, `flutter-mobile` | zasięg paywalla z 3,9% MAU do >15% | `paywall_shown` per `trigger_feature` |
| 9 | Limit Reflect: komunikat z wartością rozmowy, potem test 15 vs 30 | Monetyzacja/retencja | S/M | `flutter-mobile`, `backend-api` | konwersja bez spadku D30 | zakupy/100 rej., D30 |
| 10 | Powód rezygnacji (enum), upsell rocznego, odzyskiwanie nieudanych odnowień | Monetyzacja | S-M | `flutter-mobile`, `backend-api` | retencja płacących z 19% w górę | `subscription_receipts` m/m |
| 11 | Cena i waluta w zdarzeniu zakupu; ceny ze sklepów do baseline | Pomiar | S | `flutter-mobile`, `integration-devops` | przychód na rejestrację liczony | zdarzenie z ceną |

Kolejność ma sens: punkty 1-2 decydują, czy w ogóle da się ocenić to, co weszło dziś. Punkty 3-7 to retencja, czyli główne ograniczenie. Punkty 8-11 mają sens dopiero, gdy jest kogo konwertować.

---

## Segmenty i kohorty

| Kohorta zarejestrowanych (pierwsze otwarcie aplikacji) | n | D1 | Powrót d1-7 | Powrót d4-30 | Powrót d8-30 |
|---|---|---|---|---|---|
| Czerwiec 2026 | 105 | 8 (7,6%) | 21 (20,0%) | 21 (20,0%) | 18 (17,1%) |
| Lipiec 2026 | 52 | 4 (7,7%) | 13 (25,0%) | 12 (23,1%) | 7 (13,5%) |
| Sierpień 2026 | 74 | 9 (12,2%) | 22 (29,7%) | 23 (31,1%) | 22 (29,7%) |
| Wrzesień 2026 (do 09-25) | 43 | 7 (16,3%) | 11 (25,6%) | okno niepełne | okno niepełne |

Liczniki poniżej 25 są kierunkowe. Poprawa D1 w sierpniu i wrześniu zgadza się z raportem 09-25 i nadal nie jest istotna statystycznie.

---

## Zastrzeżenia do danych

- **Korelacja to nie przyczyna.** Wyższy powrót po zapisie albo Reflect w 1. dobie może wynikać z tego, że wracają ludzie z większą motywacją. Dlatego rekomendacje 4-7 mają testy, a nie tylko wdrożenie.
- **Redesign wszedł 2026-10-03.** Dzisiejsze zdarzenia (`trial_started` 1, `personal_reveal_viewed` 2, `push_prompt_result` 2, oferta 2) to w dużej części testy. Nic z redesignu nie jest tu oceniane, oprócz ryzyka w M1.
- **MAU 30d = 203** jest zawyżone przez nową falę z Google Play (R5). Wcześniejsze raporty liczyły ~111-127.
- **Kohorta "zarejestrowanych"** to osoby z pierwszym zdarzeniem klienta w oknie i z jakimkolwiek zdarzeniem backendu albo `user_registered` / `user_logged_in`. Część to ponowne logowania na nowym urządzeniu, co zaniża ukończenie onboardingu w 1. dobie.
- **Statusu terapii nie mierzymy** (Art. 9, świadoma decyzja). Teza R3 o osobach spoza terapii jest hipotezą z kodu, nie z danych.
- **Open rate AI vs szablon** jest nadal niezmierzony: `moment.sent` nie ma właściwości `is_ai_generated`, ma ją tylko `moment.scheduled` (369 AI, 968 szablon w 30 dniach).
- **Prawda przychodowa** (7/37, 2 paragony w 30 dniach) pochodzi z raportu DB z 2026-09-12 i nie była odświeżana.
- Benchmarki (D1 26-35%, D30 3-4%) pochodzą z raportów 09-12 i 09-25; nowego researchu zewnętrznego nie robiłem (robi go równolegle inny agent).

---

## Luki w instrumentacji, które blokują ocenę

1. `is_ai_generated` na `moment.sent` / `moment.opened` (backend, `data-analytics`), żeby porównać AI z szablonem.
2. Cena i waluta na `subscription_purchase_completed` (klient, `flutter-mobile`).
3. Powód rezygnacji po `premium_manage_tapped`, jako enum (klient, `flutter-mobile`).
4. Decyzja prawnika o agregacie `total_steps` (5 vs 7) do podziału retencji na gałęzie onboardingu (M-3 z audytu bezpieczeństwa).
5. `moment_type` na `moment.opened` (dziś trzeba łączyć po `moment_id`).

---

## Załącznik: zapytania (HogQL, read-only)

Filtr bazowy we wszystkich zapytaniach klienta: `properties.$lib = 'posthog-flutter' AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')`.

**Q1 kohorty miesięczne** i **Q2 działania 1. doby**: kohorta = `min(timestamp)` zdarzeń klienta per `person_id`, przecięta z osobami mającymi `user_registered` / `user_logged_in` albo dowolne zdarzenie `$lib='posthog-python'`. Q2 ustawia flagi `max(e.timestamp < t0 + INTERVAL 24 HOUR AND e.event IN (...))` dla grup: Reflect (`reflect_message_submitted`, `reflect_message_sent`, `reflect_session_started`), zapis (`debrief_created`, `prep_card_created`, `between_session_created`, `recording_upload_completed`, `recording_saved`, `quick_capture_submitted`), check-in (`symptom_scored`, `health_check_completed`), push (`notification_permission_granted`), onboarding (`onboarding_completed`); powrót = dowolne zdarzenie klienta w `[t0+24h, t0+8d)`.

**Q3 powiadomienia 30d**:
```sql
SELECT s.mt AS moment_type, count() AS sent, uniq(s.pid) AS users,
  countIf(o.mid IS NOT NULL AND toString(o.mid) != '') AS opened
FROM (SELECT properties.moment_type AS mt, toString(properties.moment_id) AS mid, person_id AS pid
      FROM events WHERE event='moment.sent' AND timestamp >= now() - INTERVAL 30 DAY) s
LEFT JOIN (SELECT DISTINCT toString(properties.moment_id) AS mid FROM events
      WHERE event IN ('moment.opened','moment.acted') AND timestamp >= now() - INTERVAL 30 DAY) o
ON o.mid = s.mid GROUP BY moment_type ORDER BY sent DESC
```

**Q4 push w 1. tygodniu nowych**: nowi z `t0` w [2026-08-15, 2026-09-26), `moment.sent` w `[t0, t0+7d)`, bez `WEEKLY_SUMMARY_READY` / `MONTHLY_SUMMARY_READY`.

**Q5-Q7 zmiana ruchu**: nowe osoby per `toStartOfWeek(t0)` i `$os`; `$device_model`, `$geoip_country_code` z pierwszego zdarzenia (kraje z n≥3); `app_install_attributed` per `install_source` i `utm_*`.

**Q8 Reflect**: `count()` zdarzeń `reflect_message_submitted` per osoba i miesiąc od 2026-08-15, dalej tylko rozkład (identyfikatory osób nie są raportowane).

**Q9 zasięg funkcji i 404**: `uniq(person_id)` per zdarzenie w 30 dniach; `api_error` ze `status_code = 404` per `endpoint`.

**Q10-Q11 dzień wydania**: zdarzenia redesignu od 2026-10-03 00:00 UTC z `$is_testflight`; `reason`, `error_type`, `trigger_feature` dla `post_onboarding_offer_not_shown` i `paywall_load_failed`; `product_id` i `$os` dla `subscription_purchase_completed`.

**Q12 nagrody**: `inapp_insight.*`, `realization_detected`, `realization_viewed` per miesiąc od czerwca.
