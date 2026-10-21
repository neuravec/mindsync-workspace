# Cięcie kosztów powiadomień – lista zadań

Zlecone: 2026-09-13. Kontekst: `analytics-reports/2026-09-12-diagnoza-retencja-monetyzacja.md`.
Cel biznesowy: obniżyć rachunek za AI (112,13 USD/30d, z czego >=82% to powiadomienia)
bez pogorszenia doświadczenia płacących użytkowników.

## Stan

| # | Zadanie | Agent | Status |
|---|---------|-------|--------|
| 1 | Bramka premium na generowaniu AI w powiadomieniach (end-to-end) | backend-api | ZROBIONE, niescommitowane |
| 2 | Audyt modelu i optymalizacja procesu generacji dla płacących | data-analytics | ZROBIONE |
| 3 | Weryfikacja konfiguracji modeli na Heroku (prod) | data-analytics (w ramach #2) | ZROBIONE |
| 6 | Naprawa buga re-engagement (EXPIRED pomijany, render 2457:1) | backend-api | ZROBIONE, niescommitowane |
| 7 | Diagnoza wygasania pushy | backend-api | ZROBIONE, teza o niedostarczaniu OBALONA |
| 8 | Pominac render dla odbiorcow bez tokenu FCM | backend-api | ZROBIONE |
| 4 | Weryfikacja OBU zmian razem przed deployem | qa-testing | ZROBIONE, werdykt GO |
| 5 | Deploy wszystkich trzech zmian razem | lead | WDROZONE: Heroku v549, 3/3 dyna up, zero bledow |
| 9 | Pomiar efektu po 7 dniach (koszt AI + open rate AI vs szablon) | do zlecenia ~2026-09-20 | CZEKA |

## Ustalenia z rekonesansu (2026-09-13)

- Centralny generator: `app/services/moment_text_generator.py:164`, model `settings.GPT_MODEL_41_MINI`.
- Lokalny `.env`: GPT_MODEL, GPT_MODEL_MINI, GPT_MODEL_41_MINI, GPT_MODEL_41 = `gpt-5.4-mini`. Prod do potwierdzenia.
- Osiem call-site'ów AI w ścieżce powiadomień (7 generatorów momentów + `notification_service.generate_nudge_text`).
- Każdy generator ma już zlokalizowany fallback na sztywnych szablonach, bez treści AI.
- Tylko 2 z 8 call-site'ów mają `track_usage("NOTIFICATION")` – raportowany koszt jest zaniżony.

## Decyzje operatora

- 2026-09-13: wdrazamy JEDNYM deployem dopiero po dorobieniu #8 (pomijanie kont bez tokenu FCM),
  zamiast wdrazac #1 i #6 od razu. Swiadomie tracimy kilka dni oszczednosci na rzecz czystszego wdrozenia.

- Użytkownicy bez premium: ZERO generowania AI w powiadomieniach, wyłącznie sztywne szablony.
- Użytkownicy premium: zostaje AI, ale proces ma zostać zoptymalizowany.

## Otwarte pytania

- Realna cena planu `premium_m_01` (brak w bazie, do odczytu z App Store Connect / Play Console).
- Czy `conversation_*` to urwana instrumentacja czy wycofany model interakcji.
- Habit Tracker bez instrumentacji PostHog.

## Wynik audytu (#2, 2026-09-13)

- Model na prodzie: `gpt-5.4-mini`, potwierdzone niezależnie z bazy (100% ze 105 567 wywołań NOTIFICATION w 30 dni). Zero dryfu.
- `heroku config` nie pokazuje zmiennych GPT_MODEL*, bo te ustawienia zyja w sledzonym gitem `MindSync/.env`, ktory jedzie w slugu. Zweryfikowano zgodnosc HEAD 072a25b2 z release'em v548.
- KOREKTA: wszystkie 8 call-site'ow ma poprawny `track_usage("NOTIFICATION")`. Wczesniejsze ustalenie o 2 z 8 bylo artefaktem grepa lamanego przez wielolinijkowe wywolania. Koszt NIE byl zanizony.
- GLOWNE ZNALEZISKO: `re_engagement_text_warm` to 86% kosztu (78,08 z 90,91 USD). Stosunek wywolan AI do zapisanych powiadomien 2457:1 (90 899 renderow, 37 rekordow, 7 otwarc).
- Przyczyna: `_count_re_engagement_moments_since()` w `re_engagement_generator.py:376-415` pomija status EXPIRED przy liczeniu juz wyslanych, wiec orchestrator renderuje AI od nowa co godzine dla tego samego wygaslego kandydata.
- 73% kosztu (66,73 USD) generuja uzytkownicy z WYGASLYM premium. Bramka musi filtrowac po `is_active=true`. Przekazane do #1.
- Aktywnych premium jest 11, nie 18. Po bramce koszt powiadomien AI: 1-2 USD/mies.
- Prompt ~580 tokenow wejscia / ~96 wyjscia, ~70% to tresc stala. Za krotkie na prompt caching (prog OpenAI ~1024 tok.).
- `GPT_MODEL_41_MINI` jest wspoldzielony przez 13 plikow, w tym zywa rozmowe. Zmiana modelu wymaga dedykowanej zmiennej, nie globalnego przelacznika.
- Wniosek: optymalizacja modelu i promptu to przy tej skali walka o grosze. Priorytet to bramka i bug re-engagement.

## Wynik #1 – bramka premium (2026-09-13, w drzewie roboczym, niescommitowane)

- Bramka w jednym miejscu: `is_ai_notification_eligible(db, user_id)` na wejsciu `generate_moment_text()`,
  rzuca `AIGenerationNotEligibleError` zamiast wolac model. Wszystkie 7 generatorow juz lapalo wyjatek
  i wracalo do szablonu, wiec zero zmian logiki w generatorach.
- Druga sciezka `_generate_nudge_text` w `notification_service.py` zabramkowana osobno, przed dociaganiem
  kontekstu, wiec darmowy uzytkownik oszczedza tez zapytania do bazy.
- Fail-closed przy braku sesji `db`. Powiadomienie zawsze wychodzi, tylko z szablonu.
- KOREKTA `is_active` okazala sie niepotrzebna: `is_user_premium()` juz wymaga `is_active=True` ORAZ
  (`end_date IS NULL` LUB `end_date > NOW()`), nigdy nie patrzy na `subscription_type`. Dopisano 2 testy
  odtwarzajace przypadek z audytu (wygasly trial PREMIUM oraz spozniony cron dezaktywacji) – oba odrzucone.
- Bramka odrzuca 1163 uzytkownikow z wygaslym trialem PREMIUM i 648 uzytkownikow BASIC.
- BEZ MIGRACJI. Pole `NotificationMoment.is_ai_generated` juz istnieje i juz leci do PostHog w
  `moment.scheduled` / `moment.sent`, wiec porownanie open rate AI vs szablon to gotowe zapytanie.
- Testy: 5776 passed, 14 failed – dokladny podzbior znanego baseline'u, zero regresji.
  Nowy `test_notification_ai_premium_gate.py` (23 testy) + zaktualizowany `test_moment_text_generator.py` (23) zielone.
- Szacunek: wyciecie ~3700-3800 wywolan AI dziennie, spadek kosztu o ~99%, z ~3,2-3,3 USD/dzien do ~0,03-0,10 USD/dzien.
  To ekstrapolacja, nie pomiar – do weryfikacji po wdrozeniu.

## Wynik #6 i #7 (2026-09-13, w drzewie roboczym, niescommitowane)

- Bug potwierdzony. Miejsce renderu: `NotificationOrchestrator.select_moment_for_user`, krok 6.4
  (`notification_orchestrator.py` ~705-736). Przyczyna w generatorze:
  `_count_re_engagement_moments_since` (`re_engagement_generator.py` ~376-425) wykluczala EXPIRED i DISMISSED.
- Petla: push wygasa -> licznik wysylek cofa sie z 1 na 0 -> push_number wraca na 1 -> identyczny dedup_key
  (bo `last_activity_date` nieaktywnego uzytkownika sie nie zmienia) -> platny render AI -> odrzut przez
  UNIQUE(user_id, dedup_key). Co godzine, bez konca.
- Historia pliku: wykluczenie istnieje od pierwszego commita `aded542e` (2026-05-20). Wada od poczatku,
  nie regresja. Intencja "druga szansa" nigdy nie byla ograniczona i byla sprzeczna z docstringiem klasy.
- Naprawa: licznik monotoniczny (liczy wszystkie statusy). Kadencja 3 -> 7 -> stop nietknieta, zabezpieczona testem.
- Testy: 5790 passed, 14 failed = caly baseline, zero regresji. 11 nowych testow na prawdziwej sesji SQLite.
- Bez migracji, bez zmiany kontraktu z Flutterem, import w workerze RQ potwierdzony.

## KOREKTA tezy o wygasaniu (#7)

Teza "81% pushy wygasa niedostarczonych" jest OBALONA. Kwerenda prod (30 dni, EXPIRED/AI/RE_ENGAGEMENT):
- 100% (30/30) mialo `sent_at IS NOT NULL`. Zero siedzialo w PENDING do wygasniecia.
- 73% (22/30) mialo `push_delivered=True`. Push doszedl, uzytkownik zignorowal.
- 27% (8/30) `push_delivered=False`, bo 38% adresatow nie ma ZADNEGO tokenu FCM.
- Kontrola systemowa (7 dni, wszystkie typy): 2% niepodjetych, 0% dla RE_ENGAGEMENT.
  Wyklucza to zaglodzenie kolejki RQ (MSV3.3.Fix.1) jako przyczyne.
- EXPIRED znaczy "minal expires_at", nie "niedostarczony".
- WNIOSEK: open rate 1,4% mierzy realne niezaangazowanie, nie problem dostarczalnosci.
- Auto-czyszczenie martwych tokenow DZIALA (wlasna implementacja w `notification_service.py`:
  `send_fcm_message_v1` wykrywa token_invalid, `send_fcm_to_all_user_tokens` wola `crud.remove_fcm_token`).
  Nie wysylamy w kolko na martwy token.

## Wynik #4 – weryfikacja laczona (2026-09-13). WERDYKT: GO

- Pelny zestaw dwukrotnie: 5790 passed / 14 failed, potem 5801 passed / 14 failed (po dodaniu nowych testow).
  Czerwone to dokladnie te same 14 z baseline'u. Zero regresji z obu zmian.
- Nowy plik `app/tests/test_notification_ai_gate_re_engagement_integration.py`, 11 testow integracyjnych na styk A i B.
- DOWOD KONTRFAKTYCZNY (najwazniejsze): qa podmienilo w pamieci procesu stara, buggy wersje licznika
  i przepuscilo te sama symulacje 240 tyknien godzinowych (10 dni trwale nieaktywnego uzytkownika,
  kazdy zapisany moment natychmiast EXPIRED):
    * STARA wersja, darmowy: 168 renderow na 240 tyknien, 1 zapisany wiersz (reszta odrzucona przez UNIQUE).
    * STARA wersja, premium: 168 renderow I 168 REALNYCH wywolan OpenAI.
    * NOWA wersja, oba: <=2 rendery, <=2 wywolania OpenAI, dokladnie push #1 (dzien 3) i push #2 (dzien 7), potem stop.
  To potwierdza mechanizm z audytu i dowodzi, ze test nie jest tautologia – zlapie regres, gdyby fix sie cofnal.
- Strażnik na przyszlosc: statyczny skan AST wszystkich plikow w `moments/` i `insights/` pilnuje,
  ze kazde wywolanie `generate_moment_text(...)` ma jawny `db=`. Pominiecie oznaczaloby cichy fail-closed
  (premium dostaje szablon i nikt tego nie zauwaza).
- Zweryfikowano recznie wszystkie 7 miejsc przekazujacych `db=db`.
- `AIGenerationNotEligibleError` pochlaniany przez wszystkie 7 generatorow (`except Exception`), nie przecieka wyzej.
- Licznik monotoniczny NIE przechyla sie w druga strone: dokladnie 2 momenty na 240 tyknien, nigdy wiecej.
- Boot-safety potwierdzone: import zmienionych modulow czysty, ReEngagementGenerator nadal zarejestrowany.
- Zawezenie zakresu zaznaczone uczciwie: testy multi-tick steruja jednym generatorem, bez konkurencji
  wielu generatorow w rundzie scoringowej. Niezwiazane z zadna z dwoch zmian.

## Wynik #8 – ghost recipients (2026-09-13)

- KRYTYCZNE PYTANIE ROZSTRZYGNIETE: karta in-app DOCIERA do uzytkownika bez tokenu FCM.
  Dowod: `GET /moments/upcoming` (`app/api/v1/endpoints/moments.py`) wolane przy kazdym otwarciu apki,
  niezaleznie od stanu pusha; pod spodem `get_pending_or_sent_moment_for_user`
  (`app/crud/notification_moment.py`), ktorego docstring (CS-20, MSV3.3) opisuje go wprost jako
  kanal zapasowy in-app dla przypadku "SENT ale push_delivered=False".
- DLATEGO nie pominieto generowania w calosci. Uzyto wezszej bramki:
  `CooldownGiveUpThrottle.has_no_push_target()` (gotowy mechanizm, juz uzywany przez AddTherapyDateGenerator).
  Blokuje tylko gdy JEDNOCZESNIE brak tokenu FCM I `activated_at IS NULL`.
  Adresat re-engagement, ktory byl aktywny i ucichl, ma activated_at z przeszlosci, wiec jego karta przezywa.
- Bramka w `is_eligible()` (Gate 2, po tanim toggle, przed droższymi zapytaniami) ORAZ jako pierwszy krok
  w `generate()` (zabezpieczenie na wyscig usuniecia tokenu).
- Kadencja 3/7/stop nietknieta, wlasny mechanizm generatora. `is_throttled()` NIE uzywane.
- Kolizja z testami #4: fixture `_insert_user()` tworzyl usera z `activated_at=None` i bez tokenu,
  czyli dokladnie odcinana populacje. Naprawione jednolinijkowo w fixture, bez ruszania asercji.
- Testy: 5807 passed, 14 failed = caly baseline, zero spoza listy.
- Zasieg WEZSZY niz 38%, bo wymaga tez `activated_at IS NULL`. Twarda liczba dzienna do policzenia
  przez database-administrator, jesli operator bedzie chcial.
- PROPOZYCJA NIEZAIMPLEMENTOWANA: ten sam gate dla innych typow momentow. REFLECTION_INVITATION
  i THERAPY_RELATIONSHIP_CHECKIN swiadomie go NIE przyjely (wlasne docstringi). Do decyzji operatora.

## Deploy

- Commit `bc6ee9c` na main, 13 plikow, 1694 insertions. Wypchniety 2026-09-13.
- Do commita weszly WYLACZNIE pliki tej zmiany. Poza commitem swiadomie zostawiono:
  pliki `.claude/agent-memory/` z tej i wczesniejszych sesji oraz katalog `db-reports/`.
- BEZ MIGRACJI. Nie trzeba `alembic upgrade head`.

## Deploy potwierdzony (2026-09-13 11:46 CEST)

- Heroku **v549** = Deploy `bc6ee9ce`. Poprzedni release v548 byl z 2026-09-03.
- Wszystkie trzy dyna UP: web.1, worker.1, scheduler.1. Zero H10, zero Traceback, zero ImportError w logach.
- Web dyno przeszlo pelny lifespan: `rq_scheduler_setup` zarejestrowal wszystkie joby (upload finalizer,
  weekly goal narrative, mood trend, weekly observations, RQ failed-job monitor).
- Worker nasluchuje na `high, default` w poprawnej kolejnosci priorytetow.
- BEZ migracji, wiec `alembic upgrade head` nie byl potrzebny.
