# Nadrobienie kart "Before therapy" z pierwszej rozmowy (2026-10-13)

**Autor:** database-administrator
**Zgoda operatora:** "Ręcznie nadrób na starych" (2026-10-13). Zakres zgody: wyłącznie enqueue `generate_first_conversation_prep_card` raz na kwalifikujący się wątek. Zero DML i DDL z mojej strony, zero kasowania claimów, zero innych zapisów.
**Kod:** prod `7e281ff` (`MindSync-wt-fw-integration`), alembic `m318a1b2c3d4`.
**Dyna:** `run.7062` (faza 1), `run.1725` (enqueue), `run.6329` (weryfikacja), wszystkie `--no-tty`, zakończyły się same; `heroku ps` po każdym: zero dyn `run.*`. Połączenia DB wymuszone jako read-only (`transaction_read_only=on`).
**Skrypty obok raportu:** `2026-10-13-prep-card-backfill.phase1.py` (kandydaci, tylko odczyt), `.phase2_enqueue.py` (enqueue), `.phase3_verify.py` (wynik, tylko odczyt).

## TL;DR

- Wszystkich wątków pierwszej rozmowy w statusie FINISHED: 23 (ACTIVE: 2).
- Po bramce "w terapii" (aktywna zgoda ARTICLE9_HEALTH i `currently_in_therapy` yes_regular/yes_occasional), bez karty AUTO po zakończeniu wątku i bez claimu w Redis: **7 wątków, 4 osoby**.
- Enqueue na kolejce `default`: **4 wątki** (jeden na osobę, uzasadnienie niżej). **Wszystkie 4 karty COMPLETED** w ciągu minuty (16:51:57 do 16:52:36 UTC), joby `FINISHED`, wynik `created`, claim ustawiony.
- iOS-B (`225a543d`, wątek 28546) **nie dostał karty: bramka "w terapii" go odrzuca** (nadal brak aktywnej zgody Art. 9 albo statusu terapii). Nie obchodziłem bramki.

## 1. Kandydaci (faza 1, tylko odczyt)

Kryteria takie same jak w jobie: wątek `entry_origin='onboarding_first_conversation'`, REFLECT, FINISHED; `first_conversation.user_is_in_therapy` = True; brak karty `generation_type='auto'`, `input_type=AUTO`, status COMPLETED lub PROCESSING, utworzonej od ostatniej wypowiedzi wątku; brak klucza `reflect:first_conversation:prep_card:<cid>`. Konto istnieje (JOIN do `users`; usunięcie konta kasuje wątki kaskadowo).

| Wątek | Osoba (sha) | Koniec wątku (UTC) | Platforma | Bramka treści | Decyzja |
|---|---|---|---|---|---|
| 28584 | `63a0d3a4` | 2026-10-05 16:17 | Android (google) | odmowa | bez enqueue, job by pominął |
| 28679 | `63a0d3a4` | 2026-10-07 14:34 | Android (google) | ok | bez enqueue, patrz pkt 2 |
| 28777 | `63a0d3a4` | 2026-10-08 17:12 | Android (google) | odmowa | bez enqueue, job by pominął |
| 28812 | `63a0d3a4` | 2026-10-09 12:25 | Android (google) | ok | **enqueue** |
| 28876 | `8995db41` | 2026-10-10 13:20 | Android | ok | **enqueue** |
| 29044 | `2ca31ea2` | 2026-10-11 18:23 | Android | ok | **enqueue** |
| 29173 | `c64f4452` | 2026-10-13 13:54 | iOS | ok | **enqueue** |

"Bramka treści" to te same sprawdzenia co w jobie: skan kryzysowy wypowiedzi, próg recapu (min. 2 wypowiedzi i 10 słów) oraz werdykt recapu z cache, jeśli jest. Celowo nie rozróżniam per wątek, czy chodzi o kryzys, czy o za krótką rozmowę (job też loguje to jako zwykłe "skipped").

Poza kandydatami (dla porządku): 14 wątków odpada na bramce "w terapii" (w tym 6 wątków iOS-B `225a543d`: 28546, 28612, 28613, 28649, 28650, 28744), 1 wątek ma już kartę (29074, karta 3466 z 2026-10-12), 2 wątki mają claim (29074 i 28711, patrz pkt 4).

## 2. Dlaczego jeden enqueue na osobę, a nie na każdy wątek

Osoba `63a0d3a4` ma pięć wątków pierwszej rozmowy (powtórzony onboarding), z czego dwa przechodzą bramkę treści (28679 i 28812). Job uznaje za "kartę tego wątku" każdą kartę AUTO utworzoną po ostatniej wypowiedzi wątku (`_existing_card`). Karta zrobiona dziś jest nowsza niż każdy z tych wątków, więc pierwszy wykonany job blokuje wszystkie pozostałe wątki tej osoby (`skipped:existing_card`). Enqueue wszystkich dałby dokładnie jedną kartę, a jej treść zależałaby od kolejności. Wybrałem najnowszy wątek przechodzący bramki (28812), bo to on odpowiada obietnicy z recapu ("starts from this"). Wątki 28584 i 28777 job i tak by pominął na bramce treści. Limit 2 karty na 24 h nie miał tu znaczenia.

## 3. Wynik (faza 3, tylko odczyt, ok. 16:55 UTC)

| Wątek | Osoba (sha) | Job RQ | Wynik joba | Karta | Status | Data sesji | Claim |
|---|---|---|---|---|---|---|---|
| 28812 | `63a0d3a4` | `6894d383` FINISHED | created | 3500, 16:51:57 | COMPLETED | brak (brak harmonogramu) | jest |
| 28876 | `8995db41` | `7d9799e2` FINISHED | created | 3501, 16:52:15 | COMPLETED | jest | jest |
| 29044 | `2ca31ea2` | `d1524aba` FINISHED | created | 3502, 16:52:27 | COMPLETED | jest | jest |
| 29173 | `c64f4452` | `10a55569` FINISHED | created | 3503, 16:52:36 | COMPLETED | jest | jest |

Logi workera: cztery linie `[FC-PREP] thread <cid>: created`, zero błędów. Kolejka `default` była pusta przed enqueue, więc joby ruszyły od razu. Każda karta wywołała `prep_card_auto_generated` (`source=first_conversation`, person-less), czyli w PostHog widać 4 dodatkowe zdarzenia z 16:51 do 16:52 UTC, które nie pochodzą z `/end`.

## 4. Uwagi

1. **Werdykt modelu recapu był niedostępny dla starych wątków.** Cache recapu żyje 24 h, więc dla 28812, 28876 i 29044 job miał tylko skan słów kluczowych (tak działa w projekcie, gdy cache wygasł: `recap_verdict` zwraca None). Dla 29173 werdykt był w cache. To nie jest obejście bramki, ale ochrona kryzysowa dla nadrobionych kart była słabsza niż dla kart robionych zaraz po `/end`.
2. **29173 (`c64f4452`, iOS) wygląda na konto iOS-A** z raportu `2026-10-13-ios-prep-card-missing.md` (koniec 13:54:50, `/end` w PostHog 13:54:59). W chwili `/end` nie było w terapii, więc recap nie obiecywał karty. Teraz przechodzi bramkę (zgoda Art. 9 i status terapii pojawiły się później), więc spełniał kryteria zadania i kartę dostał. Jeśli operator chciał nadrabiać wyłącznie wątki sprzed fixu enuma, to ten jeden jest poza tym zamiarem; karta jest zwykłą kartą AUTO i użytkownik może ją usunąć.
3. **Wątek 28711 (`63a0d3a4`) ma claim bez żadnej karty** (claim z ok. 2026-10-07 18:45 UTC, TTL do ok. 2026-11-06). Kod oddaje claim, gdy wiersz karty nie powstał, więc to wygląda na przeciek claimu sprzed fixu enuma (stary kod albo przerwany job). Nie ruszałem go (zakaz kasowania claimów). Bez znaczenia dla tej osoby, bo ma już kartę 3500.
4. **iOS-B (`225a543d`)**: wszystkie 6 wątków odpada na bramce "w terapii". Karta powstanie tylko, jeśli ta osoba udzieli zgody Art. 9 i zapisze status terapii; wtedy wystarczy pojedynczy enqueue najnowszego wątku (28744 ma pustą treść, więc realnie 28650).
5. Logi workera RQ wypisują argumenty joba, w tym Firebase UID (`generate_first_conversation_prep_card(cid, '<uid>')`). Dotyczy to też zwykłej ścieżki `/end` i każdego joba z UID w argumentach; do rozważenia przez `backend-api` / `security-guardian`, nie wynik tego backfillu.

## Przekazania

| Do | Co |
|---|---|
| lead / operator | Potwierdzić, że karta dla 29173 (`c64f4452`, iOS, wątek z dziś) jest OK (pkt 4.2). |
| backend-api | Opcjonalnie: ponowienie enqueue karty, gdy zgoda Art. 9 i status terapii pojawią się po `/end` (to samo co w raporcie iOS); zbadać przeciek claimu 28711 (pkt 4.3), jeśli może się powtórzyć na obecnym kodzie. |
| posthog-data-extractor | Odliczyć 4 zdarzenia `prep_card_auto_generated` z 2026-10-13 16:51 do 16:52 UTC przy liczeniu kart z `/end`. |
