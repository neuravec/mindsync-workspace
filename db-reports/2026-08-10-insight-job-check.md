# inapp_insight.generated silence since 2026-07-23 — RQ + Postgres check

Data: 2026-08-10. Autor: database-administrator. Handoff z: `analytics-reports/2026-08-10-c1-dead-instrumentation-review.md`, sekcja Backend, punkt 1 (`inapp_insight.generated`).

## Pytanie

PostHog pokazuje `inapp_insight.generated` odpalone 4x/3 os. między 2026-06-29 a 2026-07-23, potem 18+ dni ciszy, mimo że `.shown`/`.acted` rosną dalej. Hipoteza z handoffu: job detektora insightów pada albo przestał być schedulowany.

## Metoda (read-only)

Przez `heroku run -a mindsync python < skrypt.py` (run.9861, zakończył się sam po EOF na stdin — brak dyno do zatrzymania, `heroku ps -a mindsync` nie pokazuje żadnego `run.*`).

1. Prod Redis: `FinishedJobRegistry` / `FailedJobRegistry` / `ScheduledJobRegistry` / `StartedJobRegistry` na kolejce `default`, przefiltrowane po `func_name` zawierającym `run_insight_detection`.
2. Prod Postgres (SELECT-only, `SET statement_timeout = 15000`): `app_insights_shown` (tabela docelowa detektora — `app/models/app_insight_shown.py`) — overview, rozkład dzienny 45 dni, rozkład po `insight_type`, liczniki `shown_at`/`dismissed_at`/`acted_at`/`dedup_key` po 2026-07-23.

## Ważne ustalenie wstępne: to NIE jest job schedulowany

`run_insight_detection` (`app/tasks/notification_orchestrator_job.py:432`) nie jest zarejestrowany w `rq_scheduler_setup.py` — nie ma cronu/`ScheduledJobRegistry` do sprawdzenia. Jest enqueue'owany **on-demand** z `POST /insights/trigger` (`app/api/v1/endpoints/app_insights.py:96`, `rq_queue.enqueue(...)`) za każdym razem, gdy klient zgłasza jeden z 6 triggerów (`app_opened`, `debrief_saved`, `stats_tab_opened`, `therapy_tab_opened`, `note_added`, `symptom_logged`). `ScheduledJobRegistry` sprawdzony i pusty (0), zgodnie z oczekiwaniem — to nie błąd.

## Wyniki

### RQ registries (kolejka `default`)

| Registry | Total w kolejce | Trafienia `run_insight_detection` |
|---|---|---|
| ScheduledJobRegistry | 0 | 0 |
| StartedJobRegistry (stuck?) | 0 | 0 |
| FinishedJobRegistry | 5630 | 0 (patrz zastrzeżenie niżej) |
| FailedJobRegistry | 572 (sprawdzono pierwsze 500) | **0** |

Aktualna długość kolejki `default`: 0 (brak zaległości).

**Zastrzeżenie o FinishedJobRegistry:** RQ nie ustawia `result_ttl` przy tym `enqueue()` (`app/api/v1/endpoints/app_insights.py:96-101`), więc obowiązuje domyślne ~500 s. Wpisy starsze niż kilka minut są fizycznie usuwane z tego rejestru — **nie da się nim odtworzyć historii sprzed 07-23 ani nawet sprzed godziny**. `fin_match_count=0` jest więc nieinformacyjny w obu kierunkach (nie potwierdza ani nie wyklucza niedawnych udanych uruchomień) i nie jest dowodem na nic.

**FailedJobRegistry jest za to wiarygodny:** domyślny `failure_ttl` to ~1 rok, czyli obejmuje całe okno od powstania feature'u (`b298b1d`, 2026-05-15) po dziś. Wśród 572 nieudanych jobów w tej kolejce (próbka 500) **zero** dotyczy `run_insight_detection` — brak `NoDetectorsRegisteredError`, brak żadnego innego wyjątku dla tej funkcji, kiedykolwiek. Lista unikalnych `func_name` w próbce niepowodzeń: `daily_pipeline`, `weekly_MON_pipeline`, `yearly_pipeline`, `close_open_conversations_and_analyze`, `run_conversation_analysis`, `notify_inactivity_reminder`, `notify_journal_reminder`, `update_all_user_profiles`, `deactivate_expired_subscriptions` — inne, niepowiązane joby (część to legacy `notify_*`, oczekiwane stare wpisy sprzed usunięcia w ramach Cadence v3).

**Werdykt RQ: job nigdy nie padł.** Guardrail `NoDetectorsRegisteredError` (dodany 2026-07-03) nigdy się nie odpalił dla tej funkcji.

### Postgres — `app_insights_shown` (prawda gruntu)

```
total=15 | earliest=2026-07-04 11:38:04+00 | latest=2026-08-10 15:10:07+00 | after_0723=10
```

Rozkład dzienny (ostatnie 45 dni, wszystkie wiersze w tym oknie):

| Dzień (UTC) | Liczba |
|---|---|
| 2026-07-04 | 1 |
| 2026-07-05 | 1 |
| 2026-07-07 | 1 |
| 2026-07-13 | 1 |
| 2026-07-20 | 1 |
| **2026-07-24** | **1** |
| 2026-07-27 | 1 |
| 2026-07-29 | 2 |
| 2026-08-03 | 1 |
| 2026-08-05 | 2 |
| 2026-08-07 | 1 |
| 2026-08-08 | 1 |
| **2026-08-10** | **1** (dziś, 15:10 UTC — ok. 4h przed tym sprawdzeniem) |

Rozkład po `insight_type` (all-time): **`NOTICE` = 15, wszystkie pozostałe 0** (`REVEAL`, `PATTERN`, `CELEBRATE_TEASE`, `RECOVERY_MOMENT`, `COMPARATIVE` nigdy nie wyprodukowały wiersza — osobna obserwacja, patrz niżej).

Po 2026-07-23: `shown_after=9`, `dismissed_after=0`, `acted_after=4`, `distinct_dedup_after=10` (10 wygenerowanych wierszy po 07-23, wszystkie unikalne `dedup_key` — brak duplikatów/kolizji).

**Werdykt DB: generacja insightów (zapis wiersza do `app_insights_shown`) NIE ustała 07-23. Działa nieprzerwanie, ostatni wiersz powstał dziś.** Hipoteza "job padł" lub "przestał być triggerowany" jest **odrzucona przez dane**.

## Rozstrzygnięcie: to bug instrumentacji, nie generacji — i ma już (nieukończoną) łatkę

Skoro wiersze w DB powstają dalej, a `.generated` w PostHog milczy, rozjazd musi siedzieć między `_persist_insight()` a wywołaniem `posthog_track_insight()` — dokładnie w miejscu, gdzie kod woła `app.services.posthog_service.capture()` (`in_app_insight_detector.py:225-230` → `notification_observability.posthog_track_insight` → `_posthog_capture` → `posthog_service.capture()`).

Sprawdziłem `app/services/posthog_service.py:117-118`:

```python
def capture(...):
    if _client is None:
        return
```

`_client` to singleton modułu, ustawiany WYŁĄCZNIE przez `init_posthog()`. Jedyne miejsce, które historycznie je wołało, to `app/main.py` (lifespan startupu web dyno). `run_insight_detection` żyje w `app/tasks/notification_orchestrator_job.py` i wykonuje się w procesie `worker` dyno (`rq worker --url $REDISGREEN_URL`, bez własnego bootstrapu) — **ten proces nigdy nie uruchamia lifespanu `app/main.py`, więc `_client` w nim jest `None`, a każde wywołanie `capture()` cicho nic nie robi (return na pierwszej linii, brak wyjątku, brak logu powyżej DEBUG).**

To NIE moja hipoteza — to już zdiagnozowany dziś (2026-08-10) przez backend-api dokładnie ten sam mechanizm dla siostrzanych regresji z tego samego audytu C1 (`recording_processing_started/completed/failed`, `prep_card_auto_generated`). W drzewie roboczym repo (`MindSync/`, branch `main`, **NIEZACOMMITOWANE** — `git status --short` pokazuje `M app/tasks/__init__.py` + `M app/api/v1/endpoints/prep_cards.py` + `M app/tasks/prep_card_auto_generate.py`) leży już poprawka:

```python
# app/tasks/__init__.py (working tree diff, uncommitted)
from app.services.posthog_service import init_posthog
...
init_posthog()
```

Docstring commitu-w-drodze wprost mówi: *"EVERY posthog_capture(...) call made from ANY app/tasks/* module ... was being silently swallowed in production — correct call site, correct event shape, zero events delivered, and no error anywhere to reveal why."* Ponieważ `app.tasks.notification_orchestrator_job` jest submodułem pakietu `app.tasks`, Python zawsze najpierw importuje `app/tasks/__init__.py` — więc ta łatka, gdy zostanie zcommitowana i wdrożona, zamyka lukę **również** dla `inapp_insight.generated`, nie tylko dla dwóch eventów, dla których została napisana.

### Uczciwe zastrzeżenie — nie wszystko się domyka

Sama teoria "`_client` zawsze `None` w workerze" przewiduje **zero** zdarzeń `.generated` od zawsze (feature od `b298b1d`, 2026-05-15), a PostHog pokazał 4 udane zdarzenia między 06-29 a 07-23. Sprawdziłem historię plików, które mogłyby to tłumaczyć zmianą w czasie — `Procfile` (bez zmian od 2025), `posthog_service.py` (bez zmian 05-28→dziś), `app/tasks/__init__.py` (nie zawierał żadnego initu procesowego przed dzisiejszym `64ad4f3`/`configure_logging()`, `init_posthog()` wciąż niezcommitowane) — żadna nie tłumaczy, dlaczego działało 06-29→07-23 a potem przestało. Możliwe wyjaśnienia (niezweryfikowane w tym zadaniu, poza zakresem read-only DB/Redis): losowa kolejność forka RQ-workera w jakimś oknie faktycznie miała `app.main` w pamięci procesu z innego powodu; albo te 4 zdarzenia w PostHog mają inne pochodzenie niż zakładano. **Nie fabrykuję pewności tam, gdzie dane jej nie dają** — ale to nie zmienia głównego werdyktu: dziś, prospektywnie, generacja żyje (DB), job nie pada (RQ), a emisja `.generated` jest zgodna z tym samym `_client is None` mechanizmem, który backend-api już naprawia dla dwóch sąsiednich eventów w tym samym pliku.

## Werdykt

**Działa-ale-bez-eventu**, nie "job padł" i nie "niescheduled" (bo nigdy nie miał być schedulowany). Detekcja insightów jest żywa i tworzy wiersze w `app_insights_shown` nieprzerwanie do dziś (2026-08-10 15:10 UTC). `FailedJobRegistry` (retencja ~1 rok) nie ma ani jednego niepowodzenia tej funkcji. Cisza w PostHog dla `.generated` od 07-23 jest spójna z tym samym silent-no-op `_client is None` w procesie `worker`, który backend-api zdiagnozował dziś dla `recording_processing_*` i `prep_card_auto_generated` — i dla którego istnieje już (niezcommitowana) łatka w `app/tasks/__init__.py`.

## Dodatkowe znalezisko (poboczne, do wiadomości)

Wszystkie 15 wierszy `app_insights_shown` w historii to `insight_type=NOTICE` — pozostałe 5 typów (`REVEAL`, `PATTERN`, `CELEBRATE_TEASE`, `RECOVERY_MOMENT`, `COMPARATIVE`) nigdy nie wyprodukowały wiersza. Zgodne z hipotezą już postawioną w C1 (detektor `REVEAL` zależy od triggera `stats_tab_opened`, który pochodzi z martwego ekranu Stats/`AnalyticsCubit`). Nie badałem tego dalej — poza zakresem tego zadania, ale warto to złączyć z resztą audytu detektorów, jeśli ktoś będzie dalej ciągnął temat eligibility.

## Handoff

**backend-api**: przy commitowaniu łatki `app/tasks/__init__.py` (`init_posthog()`) — potwierdzić w code review, że zamyka też `inapp_insight.generated`, nie tylko dwa eventy z C1. Rekomendacja: dodać do test planu tej łatki asercję/log potwierdzający `posthog_service._client is not None` w kontekście importu `app.tasks.notification_orchestrator_job` (symulacja procesu workera), żeby regresja tego typu nie wróciła cicho. Po wdrożeniu: `posthog-data-extractor` powinien zweryfikować, że `inapp_insight.generated` faktycznie znów płynie w PostHog (wolumen > 0 w oknie po deployu) — to jedyny sposób potwierdzenia end-to-end, bo prod DB i RQ nie mówią nic o tym, czy event faktycznie dotarł do PostHog.

## Query'e (do powtórzenia)

```sql
-- overview
SELECT count(*) AS total, min(generated_at) AS earliest, max(generated_at) AS latest,
       count(*) FILTER (WHERE generated_at > '2026-07-23') AS after_0723
FROM app_insights_shown;

-- dzienny rozkład
SELECT date_trunc('day', generated_at)::date AS d, count(*)
FROM app_insights_shown
WHERE generated_at > now() - interval '45 days'
GROUP BY 1 ORDER BY 1;

-- po typie
SELECT insight_type, count(*), max(generated_at)
FROM app_insights_shown GROUP BY 1 ORDER BY 2 DESC;

-- interakcje po 07-23
SELECT count(*) FILTER (WHERE shown_at > '2026-07-23') AS shown_after,
       count(*) FILTER (WHERE dismissed_at > '2026-07-23') AS dismissed_after,
       count(*) FILTER (WHERE acted_at > '2026-07-23') AS acted_after,
       count(distinct dedup_key) FILTER (WHERE generated_at > '2026-07-23') AS distinct_dedup_after
FROM app_insights_shown;
```

Skrypt RQ (REPL-safe, uruchomiony przez `heroku run -a mindsync python < skrypt.py`, run.9861, dyno zakończył się sam po EOF na stdin): `FinishedJobRegistry`/`FailedJobRegistry`/`ScheduledJobRegistry`/`StartedJobRegistry` na `app.core.rq_queue.rq_queue`, filtr po `func_name` zawierającym `run_insight_detection`.
