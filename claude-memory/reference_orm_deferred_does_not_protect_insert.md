---
name: reference-orm-deferred-does-not-protect-insert
description: Odroczenie kolumny w SQLAlchemy chroni tylko SELECT, nie INSERT ani Query.count(); wlasciwym narzedziem na okno deploy-przed-migracja jest exclude_properties
metadata:
  type: reference
---

Przy dodawaniu kolumny do goracej tabeli na Heroku (deploy natychmiastowy, migracja RECZNA i pozniejsza)
odruch "zadeklaruje kolumne jako `deferred()`, wiec stary schemat jej nie zobaczy" jest BLEDNY i przeszedl
przez trzy zadania implementacyjne, zanim wylapaly go dwa niezalezne przeglady.

Zweryfikowane wykonaniem na tabeli, ktorej fizycznie brakuje kolumny:

- domyslny SELECT encji: PRZECHODZI, odroczenie dziala
- `Query(Encja).count()`: PADA, bo owija pelny zestaw kolumn mappera w podzapytanie
- ORM INSERT: PADA, bo jednostka pracy nazywa kazda zmapowana kolumne, dopisujac jawne NULL

Skutek na MindSync bylby taki: 500 na tworzeniu watku Reflect, 500 na tworzeniu rozmowy w dzienniku
(niepowiazana funkcja) i 500 na obu trasach `session_data`. Czyli wylaczone zakladanie rozmow w calej
aplikacji, nie "bezwladna funkcja".

DZIALAJACE rozwiazanie: kolumna zostaje na `__table__` (wiec `create_all` i testy dzialaja), ale znika
z mappera:

    __mapper_args__ = {"exclude_properties": ["modality", "seed_source", "seed_label"]}

Wtedy INSERT i `count()` przechodza, a pada tylko jawny odczyt Core w oslonietym helperze, czyli tam,
gdzie ma degradowac. Dostep wylacznie przez helpery z `try` + `db.rollback()` + zwrot falsy.

Dwie pulapki obok:
- `Encja(nowa_kolumna="x")` NIE rzuca wyjatku. Konstruktor deklaratywny przypisuje, atrybut nie jest
  instrumentowany, wartosc po cichu znika. Atrapy testowe ustawione w ten sposob przechodza, nie
  sprawdzajac niczego.
- `hasattr(Encja, "nowa_kolumna")` nadal zwraca True. Sprawdzac nieobecnosc w `__mapper__.columns`,
  nie `hasattr`.

Wzor testu, ktory to pilnuje: `app/tests/test_reflect_entry_pre_migration.py` w repo MindSync.
Usuwa kolumny instrukcja ALTER, potwierdza ze znikly, dopiero potem przepuszcza prawdziwe zadania HTTP.
Zostaje w pakiecie na stale. Patrz [[feedback-claim-not-verified-until-state-reproduced]].
