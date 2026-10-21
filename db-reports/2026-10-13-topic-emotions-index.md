# conversation_topic_emotions: czy jest indeks pod `conversation_id IN (...)`

Data: 2026-10-13. Prod Postgres (Azure) przez `heroku run --no-tty -a mindsync python` (run.7109, zakończył się sam). Tylko SELECT, EXPLAIN bez ANALYZE, transakcja READ ONLY, rollback.

Kontekst: Reflect v3.1 progress snapshot (`reflect_progress.py`, `_emotion_window`, linie 365-394) robi 2 zapytania na okno czasowe, 2 okna na cache miss (6 h cache w Redis per user).

## Fakty

Kolumny (information_schema): `id int NOT NULL`, `conversation_id int`, `topic_id int`, `emotion_id int`, `layer int`, `value int` (wszystkie poza id nullable). Zgodne z modelem.

Indeksy na `conversation_topic_emotions`:

| indeks | definicja |
|---|---|
| conversation_topic_emotions_pkey | UNIQUE btree (id) |
| ix_conversation_topic_emotions_id | btree (id), duplikat PK |

**Brak jakiegokolwiek indeksu na `conversation_id`, `layer`, `emotion_id`, `topic_id`.** Klucze obce na conversation_id i topic_id nie są zaindeksowane.

Rozmiar i statystyki:

| tabela | reltuples | heap | indeksy | razem | strony |
|---|---|---|---|---|---|
| conversation_topic_emotions | 469 523 (n_live_tup 479 273) | 24 MB | 21 MB | 46 MB | 3 004 |
| conversations | 1 849 | 384 kB | 224 kB | 648 kB | 47 |
| emotions | 124 | 8 kB | 32 kB | 72 kB | 1 |

- Rozkład `layer`: 1 = 26 944, 2 = 157 074, 3 = 295 255. Warstwa 1 to ok. 5,6% wierszy.
- 1 276 rozmów ma wiersze, średnio ok. 376 wierszy na rozmowę (ok. 21 w warstwie 1).
- pg_stat: `seq_scan = 12 420`, `idx_scan = 1 000` na tej tabeli. Seq scany już dziś dominują.
- `conversations`: indeksy tylko na id i uuid, brak na `user_id`.

## EXPLAIN (60 najnowszych rozmów jednego aktywnego użytkownika, identyfikatory pominięte)

Zapytanie z zadania (`emotion_id, count(*) ... layer = 1 GROUP BY emotion_id`):
```
Finalize GroupAggregate (cost=9059.97..9082.84)
  -> Gather Merge, Workers Planned: 1
     -> Parallel Seq Scan on conversation_topic_emotions (rows=776)
        Filter: (layer = 1) AND (conversation_id = ANY(<60 ids>))
```

Zapytanie z serwisu (JOIN emotions, sum/count distinct, `value > 0`):
```
GroupAggregate (cost=9736.56..9756.75)
  -> Hash Join (cte.emotion_id = em.id)
     -> Parallel Seq Scan on conversation_topic_emotions cte
        Filter: (value > 0) AND (layer = 1) AND (conversation_id = ANY(<60 ids>))
     -> Hash -> Seq Scan on emotions (124 wiersze)
```

Drugie zapytanie z serwisu (`count(DISTINCT conversation_id)`): też Parallel Seq Scan, koszt ok. 9 750.

Lookup id rozmów (`conversations WHERE user_id AND created_at ... LIMIT 60`): Seq Scan na 1 849 wierszach, koszt 95. Pomijalne.

JOIN z `emotions` nie jest problemem (124 wiersze, hash w pamięci). Problemem jest wyłącznie pełny skan `conversation_topic_emotions`.

## Interpretacja

Security miało rację: każde z 4 zapytań na cache miss to pełny skan ok. 3 000 stron (24 MB) po to, żeby znaleźć kilkaset wierszy z ok. 470 tys. Na dziś to rząd kilkudziesięciu ms na zapytanie (tabela mieści się w cache), więc nie jest to awaria, ale koszt rośnie liniowo z tabelą (ok. 376 wierszy na każdą nową rozmowę), a 6 h cache tylko rozkłada go w czasie, nie usuwa. Przy równoległych missach (np. po wdrożeniu, gdy cache jest pusty) skany idą jednocześnie i zabierają workery równoległe.

Dodatkowo, niezależnie od Reflect: brak indeksu na FK `conversation_id` (i `topic_id`) znaczy, że `ON DELETE CASCADE` przy usuwaniu rozmowy lub konta robi seq scan tej tabeli na każdą usuwaną rozmowę. To dotyczy ścieżki usuwania konta.

## Rekomendacja

Migracja jest uzasadniona: tani indeks (szacunkowo 10-15 MB), duży zysk selektywności, zero zmian w zapytaniach. Właściciel: **backend-api** (model + `app/alembic/`). Ja niczego nie tworzę.

Specyfikacja:
- `CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_cte_conversation_id_layer ON conversation_topic_emotions (conversation_id, layer);`
- `CONCURRENTLY` wymaga wykonania poza transakcją: w Alembic przez `with op.get_context().autocommit_block():`. Idempotentnie (`IF NOT EXISTS` lub guard przez inspector). Bez `bind.commit()` w migracji.
- Opcjonalnie wariant pokrywający `(conversation_id, layer) INCLUDE (emotion_id, value)`, który da index-only scan. Przy tej skali zwykły dwukolumnowy wystarczy.
- Model: `Index("ix_cte_conversation_id_layer", "conversation_id", "layer")` w `__table_args__`, żeby `create_all` i migracja się zgadzały.
- Down: `DROP INDEX CONCURRENTLY IF EXISTS ix_cte_conversation_id_layer`.
- Przy okazji (osobna decyzja): `ix_conversation_topic_emotions_id` dubluje PK i tylko kosztuje przy zapisie; indeks na `topic_id` pomógłby kaskadzie z `conversation_topics`. Indeks `conversations (user_id, created_at)` na razie niepotrzebny (1 849 wierszy).

Ryzyko wdrożenia: brak wpływu na boot, brak zmiany kontraktu. Indeks zwiększa koszt zapisu ok. 376 wierszy na rozmowę o jeden btree insert na wiersz, co jest pomijalne. Po migracji warto powtórzyć EXPLAIN i oczekiwać `Bitmap Index Scan on ix_cte_conversation_id_layer`.
