# iOS: brak karty "Before therapy" po onboardingu na nowym koncie (2026-10-13)

**Autor:** database-administrator (tylko odczyt)
**Stan danych:** 2026-10-13 15:49 UTC, prod Postgres (alembic `m318a1b2c3d4`), RedisGreen
**Dostęp:** trzy dyna one-off (`run.7835`, `run.3206` i trzecie, wszystkie `--no-tty`, zakończyły się same; `heroku ps` po każdym pokazał zero dyn `run.*`). Każde połączenie wymuszone jako read-only przy connect (`SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY`, sprawdzone `transaction_read_only=on`). Redis: tylko `GET`/`TTL`. Zero DML, zero DDL, zero zapisów w Redis, zero zmian w kodzie aplikacji.
**Skrypty:** `2026-10-13-ios-prep-card-missing.diag1.py` (lejek per platforma, próbki), `.diag2.py` (tygodniowo, zgody, kontrast Android), `.diag3.py` (identyfikacja iOS-B). Uruchamiane przez chunkowany runner `exec(compile(...))`.

## TL;DR

**Platforma nie jest przyczyną. Przyczyną jest brak zgody ARTICLE9_HEALTH w chwili zakończenia pierwszej rozmowy.** Na iOS żadne nowe konto nie ma tej zgody, więc karta nigdy nie powstaje.

1. Fix enuma działa: `inputtypeenum` = `VOICE, TEXT, auto, AUTO`, `CAST('AUTO')` przechodzi, head `m318a1b2c3d4`. Od fixu powstały dwie karty AUTO (pierwsze w historii prod), obie COMPLETED, obie konta Android.
2. Bramka, która blokuje: `first_conversation.user_is_in_therapy` wymaga jednocześnie `user_profile.currently_in_therapy IN ('yes_regular','yes_occasional')` **oraz** aktywnego rekordu `consent_records` typu `ARTICLE9_HEALTH`. Jest sprawdzana dwa razy: w `POST /reflect/{id}/end` (`should_enqueue`, przed enqueue) i w samym jobie. Bez zgody Art. 9 job **nie jest nawet enqueue'owany**, więc nie ma claimu w Redis, nie ma wiersza karty, nie ma logu `[FC-PREP]` i nie ma eventu PostHog (zdarzenia zdrowotne celowo nie emitują nic).
3. Dodatkowo `PUT/POST profile` po cichu usuwa `currently_in_therapy` z payloadu, gdy brak aktywnej zgody Art. 9 (`users.py:433-443`, `1254+`). Czyli odpowiedź "jestem w terapii" z onboardingu jest gubiona, a późniejsze udzielenie zgody na Home jej nie przywraca.
4. iOS: 0 z 18 kont utworzonych od 2026-10-01 ma jakikolwiek rekord `ARTICLE9_HEALTH` i 0 ma wypełnione `currently_in_therapy`. Android: 11 z 28 ma rekord Art. 9 (źródło `onboarding_art9`). Od 2026-08-01 nie ma ani jednego rekordu Art. 9 u konta rozpoznanego jako iOS.
5. Android bez zgody Art. 9 zachowuje się identycznie jak iOS: zakończona rozmowa, recap `ready`, brak karty (3 przypadki wskazane przez leada, potwierdzone wierszami).

Wniosek: punkt rozbieżności to **zapis zgody Art. 9 (i co za tym idzie statusu terapii) w onboardingu na iOS**, nie generator karty. Z bazy nie da się rozstrzygnąć, czy iOS w ogóle nie pokazuje ekranu zgody Art. 9 w onboardingu, czy pokazuje go dopiero na Home (PostHog leada: iOS-A odrzucił Art. 9 na Home o 13:57:10, czyli już po `/end` o 13:54:59). To pytanie do `flutter-mobile`.

## 1. Stan migracji i enuma

| Sprawdzenie | Wynik |
|---|---|
| `alembic_version` | `m318a1b2c3d4` |
| `inputtypeenum` | `VOICE, TEXT, auto, AUTO` |
| `SELECT CAST('AUTO' AS inputtypeenum)` | ok |
| `featureenum` zawiera `MOOD_TREND` | tak |
| Karty `input_type='AUTO'` all-time | 2, obie COMPLETED: id 3466 (2026-10-12 10:50:15, Android, AND-1, karta z pierwszej rozmowy) i id 3499 (2026-10-13 15:30:16, Android, godzina :30 wskazuje na cron) |

## 2. Lejek per platforma

Platforma: `user_profile.device_type` (ustawiane wyłącznie przez `POST /users/subscription`, stary flow), w drugiej kolejności `user_subscription_trial.trial_platform` (nowy flow), potem `subscription_receipts.platform`. Mieszanka sygnałów od 2026-10-05 jest czysta: `(ios, ios)` 15, `(NULL, ios)` 2, `(NULL, android)` 28, brak sygnału 12. Do konta `unknown` nie trafił żaden wątek pierwszej rozmowy. Wątek = ostatni oznaczony `entry_origin='onboarding_first_conversation'`.

Uwaga k-anonimowość: wszystkie segmenty mają n<25. Liczby kroków niezdrowotnych podaję, bo to diagnoza błędu zapisu. Wynik bramki "w terapii" dla Androida jest pominięty (n<25, suppressed); dla iOS wynosi 0 z konstrukcji, bo bez zgody Art. 9 wartość nie może się zapisać.

### Konta utworzone po fixie (od 2026-10-11 20:40 UTC)

| Krok | iOS (n=4) | Android (n=4) |
|---|---|---|
| profil istnieje | 4 | 4 |
| `onboarding_completed` | 1 | 4 |
| rekord `ARTICLE9_HEALTH` | **0** | 1 |
| `currently_in_therapy` wypełnione | **0** | 1 |
| wątek pierwszej rozmowy | 1 | 3 |
| wątek FINISHED (`/end` doszedł) | 1 | 3 |
| wypowiedzi użytkownika > 0 | 1 | 2 |
| próg recapu spełniony | 1 | 2 |
| recap wygenerowany (`token_usage_log`) | 1 | 2 |
| analiza przebiegła (`conversation_summaries`) | 1 | 2 |
| claim `reflect:first_conversation:prep_card:<cid>` w Redis | **0** | 1 |
| wywołania modelu PREP_CARD | 0 | 1 |
| wiersz karty AUTO | **0** | 1 |
| karta COMPLETED | 0 | 1 |

### Konta z 2026-10-01 do 2026-10-11 20:40 UTC

| Krok | iOS (n=14) | Android (n=24) |
|---|---|---|
| profil istnieje | 14 | 18 |
| `onboarding_completed` | **0** | 17 |
| rekord `ARTICLE9_HEALTH` | 0 | 10 |
| `currently_in_therapy` wypełnione | 0 | 7 |
| wątek pierwszej rozmowy | 0 | 9 |
| wątek FINISHED | 0 | 7 |
| karta AUTO | 0 | 0 (przed fixem enuma każdy INSERT AUTO padał) |

### Tygodniowo od 2026-08-01, rekord Art. 9 u kont iOS

Każdy tydzień: 0 (łącznie 38 kont iOS). U Androida i kont bez sygnału platformy rekordy `onboarding_art9` pojawiają się co tydzień. Rekordy Art. 9 zapisane od 2026-10-01 (wg platformy autora): Android 12, bez sygnału 10, iOS 0.

## 3. Gdzie iOS się rozjeżdża (oparte na wierszach)

Kolejne kroki po stronie serwera przechodzą na iOS tak samo jak na Androidzie: onboarding zapisany, wątek utworzony, rozmowa głosowa zapisana (49 wiadomości), `/end` przestawił wątek na FINISHED (klucz `reflect:analysis_job:29173` w Redis, zapis ok. 13:55), recap wygenerowany o 13:55:02 ze statusem `ready`, analiza zakończona. Rozjazd jest **przed** jobem karty:

| Hipoteza z briefu | Werdykt | Dowód |
|---|---|---|
| rozmowa nigdy nie zamknięta (klient nie woła `/end`) | nie | wątek 29173 FINISHED, klucz analizy w Redis |
| rozmowa za krótka, odrzucona przez progi | nie | 30 wypowiedzi, 16,5 min, próg spełniony, recap `ready` |
| job padł | nie, job nie wystartował | brak claimu w Redis (TTL -2), zero wywołań PREP_CARD, zero wierszy karty, `should_enqueue` zwraca False |
| karta powstała, ale klient patrzy na inny wątek | nie | brak jakiegokolwiek wiersza `session_prep_cards` dla konta |
| **brak zgody Art. 9 i statusu terapii w chwili `/end`** | **tak** | `consent_records` puste, `currently_in_therapy` NULL, recap zwrócił `saved_line_kind=check_in`, a nie `before_therapy_card` |

Ważne: recap iOS-A sam nie obiecał karty (`check_in`). Jeśli ekran na iOS mimo to pokazał obietnicę karty albo zaczął odpytywać `prep-cards/latest` (404 przez godziny według PostHog), to klient nie słucha `saved_line_kind` z recapu. Do sprawdzenia przez `flutter-mobile`.

## 4. Przypadki wskazane przez leada (dopasowane po czasie UTC)

Identyfikator to prefiks sha256 z UID, nigdy surowy UID.

| Przypadek | Konto | Wątek | Zgoda Art. 9 | `currently_in_therapy` | Recap | Claim / job | Karta | Werdykt |
|---|---|---|---|---|---|---|---|---|
| iOS-A, iOS 2.0.110 | `c64f4452`, utw. 10-13 13:36:31 | 29173, utw. 13:38:19, ostatnia wiad. 13:54:50, FINISHED, voice, 30 wypowiedzi | **brak rekordu** (odmowa na Home o 13:57:10 nie tworzy wiersza) | NULL | `ready`, `check_in`, 13:55:02 | brak claimu, 0 PREP_CARD | brak | zablokowany przez bramkę Art. 9 w `/end` |
| iOS-B, iOS 2.0.97 | `225a543d`, stare konto (2024-12-20), claim 10-05 08:32:10 | 28546, utw. 08:32:10, ostatnia wiad. 08:34:52, FINISHED, 7 wypowiedzi | aktywna od 2026-05-29 (`onboarding_art9`) | wypełnione | cache wygasł | brak claimu | brak | **inna przyczyna: rozmowa zakończona 10-05, a job karty istnieje dopiero od v567 (10-07 15:50Z) i i tak padał na enumie do 10-11**. Nie jest to błąd iOS i nie naprawi się sam (brak retro generowania) |
| AND-1 (sukces), Android 2.0.109 | `c9fe676e`, utw. 10-12 10:46:03 | 29074, ostatnia wiad. 10:49:51, FINISHED, voice, 5 wypowiedzi | aktywna (`onboarding_art9`) + PROFILING | wypełnione | recap 10:49:59 | claim jest (TTL ok. 28,8 dnia), 3 wywołania PREP_CARD od 10:50:18 | **3466 AUTO COMPLETED 10:50:15** | ścieżka działa |
| Android bez Art. 9 | `a202f60c`, utw. 10-11 05:27 | 29008, ostatnia wiad. 05:40:09, FINISHED, text, 13 wypowiedzi | brak | NULL | recap 05:40:18 | brak claimu | tylko późniejsza ręczna TEXT (10-11 19:19) | ta sama blokada co iOS |
| Android bez Art. 9 | `5e303f4a`, utw. 10-09 23:08 | 28848, ostatnia wiad. 23:19:51, FINISHED, voice, 28 wypowiedzi | brak | NULL | recap 23:20:04 | brak claimu | brak | ta sama blokada |
| Android bez Art. 9 | `a53dde31`, utw. 10-12 18:01 | 29108, ostatnia wiad. 18:16:42, FINISHED, voice, 29 wypowiedzi | brak | NULL | `ready`, `check_in`, 18:16:52 | brak claimu | brak | ta sama blokada |

Dodatkowe przypadki kontrastowe (Android, Art. 9 obecne, rozmowa przed fixem enuma): `55a4accc` (wątek 29009), `2ca31ea2` (29044), `8995db41` (28876). Gate Art. 9 przechodził, ale INSERT AUTO padał na enumie (przed `m317`), a claim był oddawany (brak klucza w Redis), więc kart AUTO brak. To już naprawione i nie dotyczy iOS.

## 5. Odpowiedź na pytania leada

1. **Czy job ruszył dla iOS?** Nie. Brak claimu w Redis, zero wierszy `session_prep_cards` (żadnego statusu, także FAILED ani usuniętych), zero wywołań PREP_CARD w `token_usage_log`. Logi: bufor `heroku logs -n 1500` sięga dopiero 15:45:39 UTC, więc linie z 13:55 wypadły; ale przy braku enqueue linii `[FC-PREP]` i tak by nie było.
2. **Czy kod prod gate'uje na Art. 9?** Tak, potwierdzone w `MindSync-wt-fw-integration` (HEAD `7e281ff`): `app/services/first_conversation.py:95-96` (`_IN_THERAPY_STATUSES = {"yes_regular","yes_occasional"}`, `_ARTICLE9_CONSENT = "ARTICLE9_HEALTH"`), `user_is_in_therapy` w linii 623 wymaga obu. Wołane w `app/tasks/first_conversation_prep_card.py:232` (`should_enqueue`, używane w `app/api/v1/endpoints/reflect.py:1872-1875` przed enqueue) oraz w linii 276 (sam job). Recap używa tej samej funkcji do `saved_line_kind`.
3. **Dlaczego eventy PostHog nigdy nie dotarły:** `prep_card_auto_generated` z `source=first_conversation` powinien był przyjść raz (AND-1, 10-12 10:50). Brak eventu dla iOS jest oczekiwany (job nie ruszył, a wynik "nie w terapii" celowo nie emituje nic). Brak eventu dla AND-1 to osobna rzecz do sprawdzenia przez `posthog-data-extractor` (event jest person-less, losowy `distinct_id`, więc nie da się go wyszukać po osobie, tylko po `source` i czasie).

## 6. Obserwacje poboczne

1. **16 z 18 kont iOS od 2026-10-01 nie ma w ogóle wiersza `user_therapy_context`** (nie przeszły ekranu zgód onboardingu V2), mają `device_type='ios'` ustawione przez `POST /users/subscription` i w większości zero rozmów; część jednak rozmawia (np. `73e70d51`: 2 rozmowy, 140 wiadomości) bez wiersza onboardingu. Wygląda to na starszy build App Store, który nie przechodzi nowego onboardingu. Na Androidzie nowy flow (trial_platform, brak device_type) dominuje od 2026-09-28. Do potwierdzenia przez PostHog (`$app_version` per `$os`).
2. **Zgoda Art. 9 udzielona później nie leczy wątku.** `currently_in_therapy` zostało wyrzucone przy zapisie profilu, a `/end` już minął. Nawet gdyby iOS pytał o Art. 9 na Home i użytkownik się zgodził, karta z pierwszej rozmowy nie powstanie bez ponownego zapisu statusu terapii i ręcznego enqueue.
3. `device_type` jest ustawiane tylko w `POST /users/subscription` i domyślnie przyjmuje `ios`, gdy brak flagi `is_ios`. Do analiz platformy pewniejsze jest `trial_platform`.
4. Rekordy GDPR nie są zapisywane w `consent_records` (0 wszędzie); zgoda GDPR żyje w `user_therapy_context.gdpr_consent_at`. Zgodne z obecnym kodem, odnotowuję dla porządku.

## 7. Czego prod nie powie

- Czy iOS 2.0.110 w ogóle pokazuje ekran zgody Art. 9 i pytanie o terapię w onboardingu, czy odpowiedź była "nie w terapii". Bez zgody Art. 9 wartość nie zapisuje się w żadnym wariancie, więc baza nie odróżni "nie pytano" od "odpowiedź odrzucona przez gate".
- Dokładne czasy `/end` dla iOS-A: klucz analizy w Redis daje ok. 13:55, PostHog leada mówi 13:54:59.

## Przekazania

| Do | Co |
|---|---|
| flutter-mobile | Sprawdzić w buildzie iOS 2.0.110, czy onboarding wysyła `POST` zgody `ARTICLE9_HEALTH` (source `onboarding_art9`) przed zapisem profilu z `currently_in_therapy`, tak jak Android. Według PostHog iOS pyta o Art. 9 dopiero na Home, po zakończeniu rozmowy. Sprawdzić też, czy klient po recapie z `saved_line_kind=check_in` nie powinien przestać czekać na kartę (404 na `prep-cards/latest` przez godziny). |
| backend-api (opcjonalnie, decyzja produktowa) | Rozważyć ponowienie enqueue karty, gdy zgoda Art. 9 i status terapii pojawią się po `/end` pierwszej rozmowy (np. przy zapisie zgody, w oknie kilku godzin od `/end`). Dziś taka zgoda nie ma wpływu na wątek. |
| posthog-data-extractor | `$app_version` per `$os` dla kont bez wiersza onboardingu (pkt 6.1); czy `prep_card_auto_generated` `source=first_conversation` dotarł ok. 2026-10-12 10:50Z (AND-1). |
| operator | iOS-B (wątek 28546) i wątki Android z Art. 9 sprzed fixu enuma nie dostaną karty samoistnie. Jeśli potrzebne, pojedynczy enqueue `generate_first_conversation_prep_card` per wątek (bez DML; claimów brak, więc nic nie trzeba kasować). |
