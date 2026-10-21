# Audyt bezpieczeństwa i prywatności: release/2026-10-15-posthog-notif-errors

Data: 2026-10-15. Audytor: security-guardian (tylko odczyt, bez zmian w kodzie).
Zakres: `git -C MindSync-wt-rel-1015 diff d79c509..deea7c0` (13 commitów, 48 plików) plus sprawa śledzonego pliku `.env`.

## Werdykt

**Kod tego release'u: brak znalezisk Critical i High. Z perspektywy kodu wdrożenie NIE jest blokowane.**

Osobno: **SEC-ENV-001 (Critical, istniejące wcześniej, poza diffem)**. Repozytorium backendu śledzi w git plik `.env` z produkcyjnymi sekretami oraz dwa pliki JSON z kluczami prywatnymi kont serwisowych Google. Release niczego w tym nie zmienia (diff nie dotyka `.env`), więc wstrzymanie wdrożenia nie zmniejszy ekspozycji. Rotacja musi jednak ruszyć niezależnie i pilnie (plan niżej). Rekomendacja: wdrażać release, a rotację sekretów traktować jako osobny incydent z najwyższym priorytetem.

| ID | Severity | Temat | Bloker release'u |
|----|----------|-------|------------------|
| SEC-ENV-001 | Critical (istniejące) | `.env` i klucze kont serwisowych w git i w slugu Heroku | Nie (poza diffem), ale pilna rotacja |
| MED-001 | Medium | `summary_generation_skipped` z crona bez bramki zgody G21 | Nie |
| LOW-001 | Low | Dedup receiptów Google: odnowienie z tym samym `purchase_token` w oknie 300 s nie przedłuża dostępu | Nie |
| LOW-002 | Low | `delete_person` (GDPR) cicho pomijany poza Heroku | Nie |
| LOW-003 | Low | Klucze Redis z UID po usunięciu konta (TTL do 64 dni) | Nie |
| INFO-001..005 | Info | Potwierdzenia poprawności (cross-account, H-1, M-1, H-4, HIGH-001) | Nie |

---

## SEC-ENV-001: produkcyjne sekrety śledzone w git (Critical, istniejące)

- **Lokalizacja**: `MindSync/.env` (śledzony, `git ls-files .env` zwraca plik), `MindSync/app/firebase_dummy_credentials.json`, `MindSync/app/mindsync-8f534-839e8464e684.json`.
- **Stan**: `.gitignore` nie zawiera `.env` (jest tylko `.venv*`). Plik ma 70 commitów w historii, pierwszy z 2024-10-29. Nie ma `.slugignore`, więc `.env` trafia do każdego sluga Heroku (potwierdza to komentarz w `posthog_service.posthog_sending_allowed`). `.dockerignore` wyklucza `.env*`, więc obraz Dockera jest czysty.
- **Nazwy kluczy w `.env` z niepustą wartością, wyglądającą na prawdziwą** (wartości nie były wyświetlane): `OPENAI_API_KEY`, `ASSEMBLYAI_API_KEY`, `APPLE_SHARED_SECRET`, `LOOPS_API_KEY`, `POSTHOG_API_KEY`, `POSTHOG_PERSONAL_API_KEY`, `DATABASE_URL`, `CLIENT_ID`, `CLIENT_SECRET`, `CLIENT_SECRET_ID`, `TENANT_ID` (Azure AD), `FIREBASE_CREDENTIALS` i `PLAY_CONSOLE_JSON` (ścieżki do plików JSON). Pozostałe nazwy: `ALLOWED_HOSTS`, `DATABASE_NAME`, `ENTRAUSERNAME`, `HOSTNAME`, `USERNAME`, `SSL_MODE`, `PORT`, `PWD`, `POSTHOG_ENABLED`, `POSTHOG_HOST`, `POSTHOG_PROJECT_ID`, `OPENAI_ENDPOINT`, modele GPT/Whisper/TTS, `DIRECTOR_ENABLED`, `REALTIME_*` oraz prompty (`SYSTEM_MESSAGE`, `*_PROMPT`, `*_SHORT`, `*_LONG`).
- **Pliki JSON**: oba to `service_account` projektu `mindsync-8f534` z polem `private_key` (1704 znaki). Plik nazwany `firebase_dummy_credentials.json` NIE jest atrapą: to prawdziwe konto serwisowe produkcyjnego projektu, na które wskazuje `FIREBASE_CREDENTIALS`. Drugi (`mindsync-8f534-839e...json`, w git od 2025-03-08) to konto Play Console (`PLAY_CONSOLE_JSON`).
- **Repo GitHub** `neuravec/MindSync`: anonimowe zapytanie do API zwraca 404, czyli repo jest prywatne (albo niewidoczne). To ogranicza, ale nie usuwa ryzyka.
- **Wpływ (scenariusze)**: każdy, kto ma lub kiedykolwiek miał dostęp do repo (współpracownicy, forki, kopie na laptopach, worktree, środowiska sesji chmurowych agentów, integracje CI z odczytem repo) albo do sluga Heroku, dostaje:
  - konto serwisowe Firebase Admin: tworzenie custom tokenów i logowanie jako dowolny użytkownik, czyli odczyt rozmów terapeutycznych, nastrojów i sygnałów kryzysowych każdej osoby przez API; wysyłka pushy FCM do wszystkich użytkowników;
  - `DATABASE_URL` plus sekret aplikacji Azure AD: potencjalnie bezpośredni dostęp do produkcyjnego Postgresa (łagodzi to tylko brak publicznego DNS hosta);
  - klucz OpenAI (koszty, nadużycia), Play Console (dane zakupów, zwroty), Apple shared secret, Loops (lista mailingowa, wysyłka maili w imieniu MindSync), PostHog personal key (odczyt i usuwanie danych analitycznych).
  To de facto pełny dostęp do danych zdrowia psychicznego (art. 9 RODO). Każdy wyciek repo to naruszenie wymagające zgłoszenia do UODO w 72 h.
- **Skutek uboczny już zaobserwowany**: ten sam `.env` lokalnie włączał wysyłkę do produkcyjnego PostHoga (186 fałszywych zakupów, zdarzenia testowe). Release łata objaw (bramka `DYNO`), przyczyną jest śledzony `.env`. Lokalny backend z tym plikiem łączy się też z produkcyjną bazą.
- **Właściciel**: `integration-devops` (sekrety, Heroku config vars, `.gitignore`, `.slugignore`), operator (konsole dostawców), `backend-api` (usunięcie fallbacku na `.env` w prod, jeśli kod go wymaga).

### Plan naprawy (do wykonania przez operatora i integration-devops, nie wykonano)

1. **Inwentaryzacja Heroku (przed rotacją)**: `heroku config -a mindsync` i porównanie NAZW z listą powyżej. Każdy klucz obecny tylko w `.env`, a nie w config vars, trzeba najpierw dodać do config vars. Inaczej usunięcie `.env` ze sluga wyłączy go na prodzie (ryzyko H10, por. CLAUDE.md "Change Safety"). Szczególnie: prompty i `FIREBASE_CREDENTIALS`/`PLAY_CONSOLE_JSON` jako ścieżki do plików. Te dwa trzeba zamienić na config var z treścią JSON (lub base64) albo plik budowany przy starcie z config var.
2. **Rotacja, w kolejności ryzyka**:
   1. Konta serwisowe Google `mindsync-8f534` (Firebase Admin i Play): wygenerować nowe klucze, wgrać do config vars, wdrożyć, potem USUNĄĆ stare klucze w IAM (samo usunięcie pliku z repo nic nie daje). Rozważyć Workload Identity lub zawężenie ról.
   2. Sekret aplikacji Azure AD (`CLIENT_SECRET`) i hasło/poświadczenia z `DATABASE_URL`; sprawdzić logi logowań Entra ID i Azure Postgres pod kątem obcych IP.
   3. `OPENAI_API_KEY`, `ASSEMBLYAI_API_KEY`, `LOOPS_API_KEY`, `POSTHOG_PERSONAL_API_KEY`, `APPLE_SHARED_SECRET` (App Store Connect pozwala wygenerować nowy).
   4. `POSTHOG_API_KEY` (project key): z założenia publiczny (jest też w aplikacji mobilnej), rotacja opcjonalna; ważniejszy jest personal key z pkt 3.
   Po każdej rotacji: deploy, smoke test, dopiero wtedy unieważnienie starego klucza.
3. **Usunięcie z repo (stan bieżący)**: `git rm --cached .env app/firebase_dummy_credentials.json app/mindsync-8f534-839e8464e684.json`, dopisać `.env`, `*.json` z kluczami kont serwisowych do `.gitignore`, dodać `.slugignore` z `.env`. Zostawić `.env.example` bez wartości. Lokalnie deweloperzy dostają osobny `.env` z kluczami dev/staging, nie prod.
4. **Historia**: przepisanie historii (`git filter-repo --path .env --path app/firebase_dummy_credentials.json --path app/mindsync-8f534-839e8464e684.json --invert-paths`) dopiero PO rotacji, bo rotacja jest właściwym zabezpieczeniem, a przepisanie historii tylko ogranicza dalsze rozprzestrzenianie. Wymaga force-push na `origin` i skoordynowania wszystkich klonów oraz worktree (stash i branche są współdzielone przez równoległe sesje). Repo Heroku: po przepisaniu `git push heroku main --force` albo `heroku repo:reset`; stare slugi pozostają w historii release'ów Heroku, więc rotacja i tak jest konieczna.
5. **Zapobieganie**: pre-commit hook z gitleaks/detect-secrets, GitHub secret scanning i push protection, przegląd dostępu do repo i do aplikacji Heroku.
6. **RODO**: udokumentować incydent w rejestrze naruszeń (art. 33 ust. 5). Jeśli w logach dostawców widać użycie kluczy przez nieznane podmioty, ocena zgłoszenia do UODO w 72 h.

---

## MED-001: `summary_generation_skipped` z crona bez bramki zgody (G21)

- **Lokalizacja**: `app/services/summary_generation_gate.py`, `record_generation_skip` i `_capture` (wywołanie `posthog_service.capture(distinct_id=user_id, ...)`); wołane z `_process_user` w `app/tasks/weekly_therapy_summary.py` i `app/tasks/monthly_therapy_audit.py`.
- **Opis**: zdarzenie idzie z cogodzinnego crona na identyfikowaną osobę (UID jako `distinct_id`), dla każdej osoby nieaktywnej od 14 dni (komentarz w kodzie mówi o ok. 1100-1700 osobach). Reguła G21 (`capture_trial_ended(require_consent=True)`, `capture_store_renewal`, `capture_subscription_expired`) mówi: zdarzenia emitowane przez joby w tle tylko dla osób z `has_accepted_agreements`. Tutaj tej bramki brak.
- **Scenariusz**: konto z `UserPreferences`, które nie przeszło ekranu zgód (półutworzone konto, por. `profile_not_created`), albo osoba, która nigdy nie otworzyła aplikacji po aktualizacji. Cron tworzy jej osobę w PostHog (capture bez `$process_person_profile: False`) i zapisuje sygnał zachowania "nie używa aplikacji od 14 dni". To metadane użycia, nie dane zdrowotne, stąd Medium, a nie High. Jest to jednak przetwarzanie analityczne bez podstawy, którą projekt sam przyjął.
- **Naprawa**: w `record_generation_skip` przed `_capture` dodać `has_accepted_agreements(db, user_id)` (funkcja wymaga sesji, więc przekazać `db` z `_process_user`) albo wysyłać zdarzenie person-less (`personless_distinct_id()` + `personless(...)`), skoro do pomiaru wystarczy licznik per `period_type`/`reason`. Dopisać test: osoba bez `gdpr_consent_at` nie generuje zdarzenia.
- **Uwaga funkcjonalna**: zdarzenia z crona idą z forkowanego work horse RQ; bez `flush_posthog()` na końcu joba część z nich może nie dotrzeć (ten sam problem, który release naprawił w `tasks/subscriptions.py`).
- **Właściciel**: `data-analytics` (`summary_generation_gate.py`, taski summaries).

---

## LOW-001: dedup receiptów a odnowienia Google z tym samym tokenem

- **Lokalizacja**: `app/services/receipt_dedup.py` (`find_recent_verified_duplicate`), `app/api/v1/endpoints/users.py` (`create_subscription`).
- **Opis**: dla Google kluczem jest `purchase_token`, który pozostaje taki sam przez wszystkie odnowienia subskrypcji. Odpowiedź z dedupu nie wywołuje Google i nie woła `_activate_user_subscription`.
- **Scenariusz**: receipt zweryfikowany o T (stary `expiryTime`), sklep odnawia subskrypcję, klient przesyła ten sam token o T+2 min. Dostaje `VERIFIED` bez przedłużenia `end_date`. Jeśli klient po `VERIFIED` uzna transakcję za zamkniętą i nie wyśle jej ponownie, dostęp zależy od cogodzinnej re-weryfikacji (R1 w `deactivate_expired_subscriptions`), która ma limit na przebieg (`MAX_REVERIFICATIONS_PER_RUN`). Okno 300 s wokół momentu odnowienia jest wąskie, więc prawdopodobieństwo jest niskie; skutek to utrata dostępu przez płacącą osobę, nie eskalacja uprawnień.
- **Naprawa (opcjonalna)**: dla Google pomijać dedup, gdy `user_subscription.end_date` jest już w przeszłości lub wypada w ciągu doby, albo dodać do klucza `order_id` (zmienia się przy każdym odnowieniu, sufiks `..N`). Dla Apple ryzyka nie ma: odnowienie zmienia bajty app receipt.
- **Właściciel**: `backend-api`.

## LOW-002: `delete_person` (GDPR) cicho pomijany poza Heroku

- **Lokalizacja**: `app/services/posthog_service.py`, `delete_person` (bramka zmieniona z `POSTHOG_ENABLED` na `posthog_sending_allowed`).
- **Ocena prod**: worker RQ działa w dynie Heroku (`worker.1`), a Heroku ustawia `DYNO` w każdym dynie, także `run.N` i `scheduler.1`. **Na produkcji usunięcia GDPR działają jak dotąd.**
- **Ryzyko**: usunięcie to nie jest "wysyłanie danych", a bramka je obejmuje. Jeśli backend kiedyś ruszy poza Heroku (w repo jest `Dockerfile`) albo operator uruchomi skrypt usuwania lokalnie, usunięcie z PostHoga zostanie pominięte bez żadnego logu. Osoba zostaje w PostHogu mimo żądania art. 17.
- **Naprawa**: w gałęzi pominięcia dodać `logger.warning("PostHog person deletion skipped: ...")`, a najlepiej warunkować `delete_person` tylko obecnością `POSTHOG_PERSONAL_API_KEY` i `POSTHOG_PROJECT_ID` (conftest i tak je czyści, więc testy nie wyślą żądania). Dopisać test, że w środowisku z `DYNO` usunięcie wysyła żądanie.
- **Właściciel**: `backend-api`.

## LOW-003: klucze Redis z UID po usunięciu konta

- **Lokalizacja**: `summary_generation_gate.py`: `summary_gate:skip:{period}:{uid}:{period_end}` (TTL 64 dni), `summary_gate:inactive:{uid}` (3 h), `summary_gate:on_return:...` (1 h).
- **Opis**: po usunięciu konta klucze z UID i informacją "nieaktywny w okresie X" zostają w Redis do wygaśnięcia TTL. Dane są pseudonimowe, a retencja ograniczona, więc ryzyko jest niskie. Warto jednak dopisać `SCAN summary_gate:*:{uid}*` z `DEL` do ścieżki usuwania konta albo skrócić TTL markera skip.
- **Właściciel**: `data-analytics` (klucze) + `backend-api` (ścieżka usuwania konta).

---

## Weryfikacja punktów z zakresu (Info, bez znalezisk)

### 1. Dedup weryfikacji receiptów
- **Cross-account**: zapytanie `get_latest_verified_receipts` filtruje po `user_id == current_user_id` (UID z tokenu Firebase), platformie, SKU i `status == "VERIFIED"`. Wiersz innego użytkownika nigdy nie pasuje. Zduplikowana odpowiedź dotyczy wiersza, który wcześniej przeszedł `find_cross_account_receipt`. Atakujący z cudzym `purchase_token`/receiptem nie trafia w dedup (brak własnego wiersza VERIFIED) i przechodzi pełną ścieżkę ze strażnikiem HIGH-001. **Brak możliwości przejęcia cudzej subskrypcji.**
- **Przedłużenie dostępu bez weryfikacji**: gałąź dedupu nie wywołuje `_activate_user_subscription`, nie tworzy wiersza i nie zmienia `end_date`. Zwraca tylko `VERIFIED` i id starego wiersza. **Brak przedłużenia dostępu.** Drobna uwaga: odpowiedź nie sprawdza stanu dostępu w chwili zapytania (np. zwrot w ciągu 5 min). Bramki premium czytają jednak DB, więc odpowiedź niczego nie przyznaje.
- **H-1**: cache'owany jest wyłącznie sukces. Porażki (w tym `apple_status_21002`, retryable) zawsze idą do sklepu. `verification_outcome(True, None)` daje `retryable=False`, co dla zweryfikowanej transakcji jest poprawne: to ten sam payload, który już raz był VERIFIED, więc klient może bezpiecznie ją zakończyć. **Polityka H-1 zachowana.**
- Puste `base64_receipt`/`purchase_token` nigdy nie pasują; `RECEIPT_DEDUP_WINDOW_SECONDS=0` wyłącza mechanizm. Log zawiera tylko id wiersza, UID i platformę. Zdarzenie `subscription_receipt_received{deduplicated}` ma tylko enumy i SKU.

### 2. Zdarzenia PostHog
- `subscription_purchase_completed` / `subscription_renewed` / `subscription_expired`: właściwości to enumy, booleany i SKU (`platform`, `product_sku`, `subscription_type`, `is_sandbox`, `premium_source`, `previous_premium_source`, `source`, `was_lapsed`, `reason`, `had_store_receipt`). Bez kwot, identyfikatorów transakcji i tekstu. Zdarzenia z joba (`capture_store_renewal`, `capture_subscription_expired`) mają bramkę `has_accepted_agreements` (G21). Zdarzenie ze ścieżki żądania jej nie ma, tak samo jak dotychczasowe zdarzenia płatności (akcja aktywnego użytkownika). `flush_posthog()` w `finally` nie zmienia logiki joba.
- `moment.opened`: `get_moment_by_id(..., user_id=current_user_id)`, więc zakres jest ograniczony do właściciela. `moment_type` dodawany tylko gdy `not is_health_revealing_moment_type`; typy zdrowotne, konta z pierwszego tygodnia i nieznany wiek konta idą person-less przez `posthog_track_moment`, a `personless_moment_properties` odrzuca `moment_id`, `source`, `was_pushed`. `source` z query jest na liście dozwolonych (`push`/`in_app`, inaczej `unknown`). **M-1 zachowane.**
- `moment.skipped`: `skip_reason` to enum (`inactive_14d`, `summary_not_found`, `inactive_period`). Dotyczy tylko typów "summary ready", które nie są zdrowotne. Wysyłka idzie przez `posthog_track_moment`, więc obowiązują reguły person-less. Dedup raz dziennie na proces.
- `text_source`/`template_variant`: enum i indeks wariantu ze stałej puli. Dopisane do allowlisty `PERSONLESS_MOMENT_EVENT_PROPERTIES` zgodnie z opisem; nie niosą danych o osobie.
- `api_error`: `app_version` dopasowany do `^\d{1,4}(\.\d{1,4}){0,3}$`, `platform` z `{ios, android}`, więc sfałszowany nagłówek nie wprowadzi tekstu. `detail` jest tylko porównywany przy klasyfikacji `is_expected`, nie trafia do zdarzenia.
- `summary_generation_on_return_enqueued`/`_skipped`: tylko `period_type` i `reason`. Zgoda: patrz MED-001.

### 3. Bramka `DYNO`
- `posthog_sending_allowed`: wymaga `POSTHOG_ENABLED` oraz `DYNO` albo `POSTHOG_ALLOW_OUTSIDE_HEROKU is True`. Porównanie `is True` zamyka bramkę dla wartości niebędących booleanem. `conftest.py` twardo ustawia `POSTHOG_ENABLED=false` i czyści oba klucze. Prod: web, worker i scheduler mają `DYNO`, więc wysyłka i `delete_person` działają (zastrzeżenie w LOW-002).

### 4. Generowanie podsumowań przy powrocie
- **Zakres danych**: wszystkie cztery endpointy biorą `current_user_id` z `deps.get_current_user`; `maybe_enqueue_on_return` przyjmuje tylko ten UID. Nie ma parametru pozwalającego wskazać inne konto. **Brak eskalacji poziomej.**
- **HIGH-001**: `enqueue_interactive(job, user_id, ...)`, czyli argumenty to wyłącznie ID. Job ponownie czyta użytkownika, a po usunięciu konta zwraca `skipped`.
- **Nadużycie kosztów**: `SET NX` z TTL 1 h na (okres, osoba, period_end), więc maksymalnie 2 joby na godzinę na osobę (tydzień i miesiąc). Tylko ostatni zakończony okres, brak backfillu (konto utworzone po `period_end` jest odrzucane, więc farma nowych kont nic nie wymusi). Gdy wiersz istnieje (dowolny status), nic nie jest kolejkowane. Przy niedostępnym Redis `_claim` zwraca False, czyli nic nie jest kolejkowane (fail closed). Job korzysta z tego samego `_process_user` co cron (zasady premium, first-week, dedup per okres, UNIQUE w monthly). Ryzyko kosztowe jest akceptowalne.
- Odpowiedzi endpointów bez zmian; enqueue nie podnosi wyjątków.

### 5. Warianty tekstów in-app
- `moment_text_variants.py`: stałe pule w 7 językach, bez placeholderów i bez nazw objawów. `MoodDipAlertGenerator._fallback_text` nie wstawia już `symptom_name`, co jest poprawą prywatności względem wcześniejszego tekstu ("Your {symptom} levels have been elevated"). Rotacja: hash SHA-256 (UID, typ) + dzień; odczyt ostatniego wariantu zawężony do `user_id`.
- **H-4**: `deliver_due_moments` nadal bierze tekst ekranu blokady z `push_copy` (`template_key_for_moment`). Warianty trafiają tylko do wiersza momentu i arkusza w aplikacji. Zachowane.

### Pozostałe (istniejące wcześniej, poza zakresem)
- `dashboard.py` `get_call_to_action` i `moments.py` nadal mają `HTTPException(400, detail=str(e))` dla nieoczekiwanych wyjątków, co może ujawniać treść wyjątku klientowi. Release poprawił tylko przypadek 404. Low, backlog (`data-analytics` dla dashboard, `backend-api` dla moments).

---

## RODO: status dla zakresu release'u

| Wymóg | Status | Uwagi |
|-------|--------|-------|
| Prawo do usunięcia | OK (prod) | `delete_person` działa w dynach Heroku; LOW-002 i LOW-003 do poprawy |
| Minimalizacja danych | OK | Nowe zdarzenia zawierają tylko enumy, booleany, SKU i indeksy; MOOD_DIP bez objawu |
| Zgoda na przetwarzanie | Częściowo | MED-001: zdarzenie z crona bez G21 |
| Szyfrowanie / poufność sekretów | NIE | SEC-ENV-001 |
| Retencja | OK | Klucze Redis z TTL; brak nowych tabel |

## Audyt eskalacji poziomej (endpointy w diffie)

| Endpoint | Zakres do zalogowanego usera |
|----------|------------------------------|
| POST `/users/subscription_data` (dedup) | Tak (`current_user_id` w zapytaniu) |
| POST `/moments/{id}/opened` | Tak (`get_moment_by_id(..., user_id)`, `mark_moment_status(..., user_id)`) |
| GET `/weekly-summaries/`, `/weekly-summaries/latest` | Tak |
| GET `/monthly-audits/`, `/monthly-audits/latest` | Tak |
| GET `/dashboard/calltoaction` | Bez zmian w zakresie (tylko re-raise HTTPException) |

## Priorytety

1. **Natychmiast, niezależnie od release'u**: SEC-ENV-001, czyli inwentaryzacja config vars, rotacja kont serwisowych Google, Azure/DB, OpenAI i pozostałych, potem usunięcie z repo i historii (integration-devops + operator).
2. **Bieżący sprint**: MED-001 (data-analytics).
3. **Backlog**: LOW-001 (backend-api), LOW-002 (backend-api), LOW-003 (data-analytics + backend-api), `detail=str(e)`.

Wdrożenie kodu release'u: **dozwolone** (brak Critical/High w diffie).
