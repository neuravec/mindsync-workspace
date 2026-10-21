# Runbook wdrożenia – batch post-release 2026-08-16

**Stan wyjściowy produkcji:** Heroku v534 = commit `4bb9b2c`, alembic na `ll3m4n5o6p7q`.
**Do wdrożenia:** backend `main` 7 commitów naprzód (HEAD `2d827fb`), frontend `dev` 3 commity naprzód (HEAD `1ff3f42`). Nic nie jest wypchnięte.

**Weryfikacja:** QA GO, zero regresji w obu repo. Security GO po naprawie jednego znaleziska High.

| Repo | Baseline | Po zmianach | Regresje |
|---|---|---|---|
| Backend | 5153 pass / 21 fail | 5235 pass / 21 fail | **0** |
| Frontend | 1837 pass / 28 fail | 1865 pass / 28 fail | **0** |

`flutter analyze`: 0 błędów, w tym 0 jakichkolwiek uwag w 5 zmienionych plikach.

---

## ⚠️ Kolejność jest krytyczna: migracje PRZED kodem

To nie jest preferencja, tylko wymóg. QA zweryfikowało obie strony empirycznie.

**Dlaczego migracje mogą pójść pierwsze:** obie są czysto addytywne (nullowalne kolumny + indeksy). Kod działający teraz na produkcji (`4bb9b2c`) ich nie zna i nie dotyka. Sprawdzone testem: brak jakiegokolwiek efektu.

**Dlaczego odwrotna kolejność jest groźna:**

- `mm4n5o6p7q8r` (kolumna w logach powiadomień) – zapis logu wysyłki leci na nieistniejącą kolumnę. Sam push nadal dociera, ale sesja bazy zostaje w stanie wymagającym wycofania, przez co kolejne zapytanie też pada i w logach pojawiają się mylące komunikaty o nieudanej wysyłce. Degradacja, nie katastrofa.
- `nn5o6p7q8r9s` (identyfikator transakcji przy paragonach) – **znacznie gorzej**. SQLAlchemy dokłada nową kolumnę do zapytania wstawiającego nawet wtedy, gdy kod jej jawnie nie ustawia. Pierwszy zapis w obu endpointach płatniczych pada **zanim** dojdzie do weryfikacji w Apple/Google i **poza** obsługą błędów. Efekt: żaden paragon nie zostaje zapisany, żadne zdarzenie audytowe się nie zapala, a **każda próba zakupu dostaje surowy błąd 500 przez cały czas trwania okna**.

---

## Sekwencja

### Krok 1 – migracje na produkcji (najpierw, przy kodzie v534)

```bash
heroku run --no-tty -a mindsync alembic upgrade head
```

Zastosuje po kolei `mm4n5o6p7q8r` i `nn5o6p7q8r9s`. Obie idempotentne.

**Weryfikacja przed przejściem dalej:**
```bash
heroku run --no-tty -a mindsync alembic current    # oczekiwane: nn5o6p7q8r9s (head)
```
Aplikacja musi w tym momencie działać normalnie. Jeśli nie – zatrzymaj się, nie pushuj kodu.

### Krok 2 – backend

```bash
cd C:/Users/mikol/Notebooks/MindSync/Heroku/MindSync
git push origin main
```

Push = **natychmiastowy deploy** na Heroku, bez fazy release. Poczekaj aż wstanie i sprawdź, czy dyno web nie wpadło w pętlę restartów.

**Weryfikacja po ~15 minutach:** powiadomienia typu „dodaj datę terapii" powinny przestać być planowane dla całej bazy. Baseline sprzed zmiany jest w `db-reports/2026-08-16-trial-emission-and-notification-baselines.md`.

### Krok 3 – frontend

```bash
cd C:/Users/mikol/Notebooks/MindSync/Heroku/mindsync-frontend
git push origin dev
```

Push = build Codemagic → **TestFlight i Play internal**, nie produkcja. Promocja do produkcji jest ręczna, więc ten krok jest bezpieczny i stanowi jednocześnie nośnik dla testów na urządzeniu z kroku 4.

### Krok 4 – testy na urządzeniu (BLOKUJĄCE dla promocji do produkcji)

Ścieżka płatnicza została przebudowana i testy automatyczne działają na atrapach sklepu. Przed promocją buildu do produkcji trzeba przejść na fizycznym urządzeniu:

- [ ] prawdziwy zakup subskrypcji (sandbox) – kończy się przyznaniem premium
- [ ] prawdziwe przywracanie zakupów – po raz pierwszy w historii aplikacji faktycznie wysyła paragon
- [ ] zakup jednorazowy (starter pack)
- [ ] jeśli wykonalne: zabicie aplikacji w trakcie potwierdzania zakupu, następnie ponowne wejście na ekran subskrypcji – transakcja powinna zostać dostarczona ponownie, nie przepaść
- [ ] próba przywrócenia cudzego zakupu na drugim koncie – powinna zostać odrzucona
- [ ] sprawdzenie, czy crash analityki zniknął ze zgłoszeń

### Krok 5 – dashboardy PostHog (niezależne, można w dowolnym momencie)

```bash
cd C:/Users/mikol/Notebooks/MindSync/Heroku
python scripts/posthog_build_dashboards.py --dry-run              # najpierw przejrzeć
python scripts/posthog_build_dashboards.py --update --retire-dead
```

`--update` jest **obowiązkowe** – bez niego skrypt pomija istniejące i nic nie poprawia. Nigdy `--force` (duplikuje).

**Uwaga:** przebudowa z 10.08 nigdy nie została zastosowana, więc to jedno uruchomienie wprowadzi **dwie zmiany naraz** – filtr ruchu serwerowego i całą zaległą przebudowę (zmiany nazw, ~30 nowych insightów). Spodziewaj się dużego diffu.

**Weryfikacja:** kafelek „DAU (any navigation)" powinien pokazywać 11–17, nie ~1750.

---

## Czego ten runbook NIE naprawia

**Pięć dashboardów nie jest budowanych skryptem** i pozostanie z zawyżonymi liczbami: `My App Dashboard` (568994, zawiera domyślne kafelki PostHoga „Daily active users" – najbardziej prawdopodobne miejsce, gdzie ktoś zobaczy 1750), `MindSync — Master Dashboard` (619341), `MindSync - Conversions & Engagement` (606008) i dwa dotyczące strony WWW. Wymagają ręcznej edycji w interfejsie PostHoga.

---

## Wycofanie

- **Backend:** `heroku rollback v534`. Migracji **nie** trzeba cofać – obie są addytywne i stary kod ich nie widzi.
- **Frontend:** nie promować buildu do produkcji. Nic nie trafia do użytkowników bez ręcznej promocji.
- **Dashboardy:** skrypt jest idempotentny, ale nie ma automatycznego cofnięcia. `--dry-run` przed właściwym uruchomieniem to jedyne zabezpieczenie.

---

## Follow-upy (nie w tym wdrożeniu)

1. Nasłuch transakcji zakupowych podpięty przy starcie aplikacji – pełna odporność na przerwany zakup
2. Odsiewanie duplikatów paragonów przy zapisie (LOW-002), które odblokuje ograniczenie unikalności w bazie
3. Limity dla generatorów `REFLECTION_INVITATION` i `THERAPY_RELATIONSHIP_CHECKIN` – ten sam mechanizm, ~98% ich momentów wygasa niewysłanych
4. Proaktywna propozycja kolejnego terminu po odbytej sesji
5. Zdarzenie przy nieudanym pobraniu produktów ze sklepu – dziś cichy potencjalny bloker sprzedaży
6. Zmiana nazw pięciu insightów oznaczonych `[awaiting deploy]`, których zdarzenia już działają
7. Martwe zdarzenie porzucenia bramki prawnej w onboardingu (0 wystąpień od zawsze)
8. Przeniesienie subskrypcji na inne konto – [ticket w backlogu](https://app.clickup.com/t/86cb5v395)
