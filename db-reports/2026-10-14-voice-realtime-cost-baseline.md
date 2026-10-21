# Baseline użycia i kosztu rozmów głosowych Realtime (2026-10-14)

Autor: database-administrator. Tryb: wyłącznie SELECT w transakcji READ ONLY, dwa przebiegi przez `heroku run --no-tty -a mindsync python` (run.2847, run.9550). Oba dyno zakończyły się same, `heroku ps` nie pokazuje pozostałych `run.*`. Alembic na prodzie: `m320c4a5r6d7`.

Cel: realny baseline minut i kosztu głosu Realtime do porównania z GPT-Live-1 ($0,05 za minutę sesji, billing co sekundę, tokeny modelu backendu liczone osobno).

## 1. Najważniejsze ustalenie: koszt tokenów Realtime nie istnieje w bazie

- `token_usage_log` dostaje dla głosu tylko jeden wiersz na wydany klucz efemeryczny (`operation='create_realtime_session'`, `api_type='REALTIME'`): `prompt_tokens=0`, `completion_tokens=0`, `cost_usd=0`, `user_id=NULL` (endpoint `/audio_v2/realtime-session` nie ustawia kontekstu użytkownika). Komentarz w `openai_audio_service.py` mówi, że tokeny per tura loguje klient po sesji. Tak się nie dzieje: Flutter sumuje `response.done -> usage` (`RealtimeUsage`), ale wysyła sumę tylko do PostHoga, w evencie `first_conversation_ended` (`input_tokens`, `output_tokens`, `cached_tokens`), i tylko dla pierwszej rozmowy. Zwykły Reflect głosowy nie raportuje tokenów nigdzie.
- Nie ma podziału audio/tekst nigdzie (ani w bazie, ani w PostHogu). Klient czyta tylko `input_tokens`, `output_tokens` i `input_token_details.cached_tokens`.
- Ścieżka legacy (`LEGACY_REALTIME_KEY`, `POST /v1/realtime/sessions` w `reflect.py` i `conversations.py`) wydaje klucze bez żadnego wpisu w logu, więc liczba kluczy w logu jest zaniżona.
- Wniosek: kosztu na sesję i na minutę dla obecnego Realtime z bazy policzyć się nie da. Nie podaję takiej liczby.

## 2. Cennik w `model_pricing` (REALTIME, aktywne wiersze)

| model | in / 1M | out / 1M | cached / 1M | od |
|---|---|---|---|---|
| gpt-realtime-1.5 | 10 | 20 | 0,30 | 2026-04-06 |
| gpt-realtime-2 | 32 | 64 | 0,40 | 2026-05-12 |
| gpt-realtime-2.1 | 32 | 64 | 0,40 | 2026-10-05 |
| gpt-realtime-2.1-mini | 10 | 20 | 0,30 | 2026-10-05 |
| gpt-4o-mini-transcribe-2025-12-15 (STT) | | | | $0,003/min |

Uwagi: (a) brak wiersza dla `gpt-realtime-mini`, którego prod używał od sierpnia do 2026-10-05 (50 kluczy w 90 dniach); (b) jedna stawka na wejście i jedna na wyjście, czyli stawka audio; tokeny tekstowe (instrukcje, kontekst, wstrzyknięcia) są w rzeczywistości tańsze, więc gdyby tokeny były logowane, ten wzór zawyżałby koszt; (c) nie weryfikowałem stawek z bieżącym cennikiem OpenAI, to zadanie dla kogoś z dostępem do sieci.

## 3. Klucze Realtime wydane (log mintów, bez powiązania z użytkownikiem)

| model | 30 dni | 90 dni | uwaga |
|---|---|---|---|
| gpt-realtime-mini | 38 | 50 | zwykły Reflect głosowy do 2026-10-05 |
| gpt-realtime-2.1-mini | 41 | 41 | zwykły Reflect głosowy od 2026-10-06 |
| gpt-realtime-2.1 | 18 | 18 | pierwsza rozmowa (override od 2026-10-05) |
| gpt-realtime-2 | 0 | 5 | |
| razem | 97 | 114 | plus nielogowane klucze legacy |

Historia miesięczna: maj 24, czerwiec 9, lipiec 19, sierpień 6, wrzesień 37, październik (do 14.10) 66 kluczy. Klucz to nie sesja: retry przy błędzie override, ponowne połączenia i otwarcia bez słowa też wydają klucz.

## 4. Sesje i czas trwania (wyprowadzone z timestampów)

Metoda. Jawnego czasu sesji nie ma w żadnej tabeli. Sesję wyznaczam jako ciąg zdarzeń z przerwą nie większą niż 10 minut:
- **Reflect głosowy (zwykły)**: wiersze `token_usage_log` z `operation='director_embed_user_text'`. Director odpala się na każdą wypowiedź użytkownika w Reflect głosowym, nie w pierwszej rozmowie (`reflect.py`, `audio/user_message_add`). Grupowanie per użytkownik. Czas = pierwsza do ostatniej wypowiedzi użytkownika.
- **Pierwsza rozmowa**: wiadomości (`messages`, użytkownik i agent) w wątkach `entry_origin='onboarding_first_conversation'` z `modality='voice'`, grupowanie per wątek.
- Błąd metody: zaniżenie o czas od połączenia do pierwszej wypowiedzi, o ostatnią odpowiedź agenta (Reflect) i o czas do tapnięcia End; szacuję 0,3-1 min na sesję. Sesje bez żadnej wypowiedzi są niewidoczne. Sesje z jedną wypowiedzią mają czas 0. Kolumna `modality` istnieje od 2026-09-18, więc pomiar z `messages` obejmuje tylko ostatni miesiąc.

| segment | okno | sesje | użytk. | sesje/użytk. | p50 min | p75 | p90 | p99 | średnia | suma min |
|---|---|---|---|---|---|---|---|---|---|---|
| Reflect głosowy | 90 d | 144 | 31 | 4,6 | 1,53 | 5,95 | 18,15 | 80,3 | 6,55 | 943,2 |
| Reflect głosowy | 30 d | 67 | 14 (n<25) | 4,8 | rozkład ukryty | | | | | 276,7 |
| Pierwsza rozmowa | 30 d = 90 d (start 03.10) | 19 | 10 (n<25) | 1,9 | rozkład ukryty | | | | | 78,9 |
| Rozmowa głosowa w dzienniku (JOURNAL) | 30 d / 90 d | 19 / 26 seedów sesji | 6 (n<25) | | niemierzalne | | | | | niemierzalne |

Rozkład czasu dla puli z `messages` z 30 dni (Reflect i pierwsza rozmowa łącznie, 51 sesji, 15 użytkowników, poniżej progu k=25, więc tylko kubełki): poniżej 1 min 10 sesji, 1-3 min 26, 3-10 min 9, 10-20 min 5, 20-40 min 1.

JOURNAL: wiadomości głosowe dziennika nie są niczym oznaczone, jedyny ślad to `embed_voice_session_seed` (pobranie kontekstu przed sesją), więc liczę wyłącznie otwarcia, bez minut.

## 5. Free / trial / premium

Wszyscy użytkownicy głosu w oknie mają wiersz PREMIUM w `user_subscription` (`granted_via` = `signup_trial`, `purchase` albo `starter_pack`, część już nieaktywna). Głos jest więc w praktyce funkcją premium/trialu. Każda grupa ma poniżej 25 użytkowników, więc podział minut i kosztu na płacącego jest ukryty (n<25, suppressed). Stan subskrypcji to migawka z dziś, nie z chwili sesji.

## 6. GPT-Live-1 przy $0,05/min (tylko warstwa głosowa)

| scenariusz | minuty | koszt GPT-Live-1 |
|---|---|---|
| 30 d, dolna granica (Reflect 276,7 + pierwsza rozmowa 78,9) | 355,6 | $17,78 |
| 30 d, z narzutem 0,5 min na sesję (86 sesji) | ok. 399 | ok. $19,95 |
| 90 d (Reflect 943,2 + pierwsza rozmowa 78,9) | 1022,1 | $51,11 (średnio ok. $17/mies.) |

Bez minut dziennika głosowego (niemierzalne, rzędu 19 otwarć w 30 dni). GPT-Live liczy czas połączenia, także ciszę, więc otwarcia bez wypowiedzi (różnica między 97 kluczami a ok. 86 sesjami z treścią) dołożą minuty, których ta metoda nie widzi.

**Backend liczony osobno.** Dzisiejszy backend głosu (director: embeddingi i decyzje, embeddingi wypowiedzi, seedy RAG) kosztował dla użytkowników głosu w 30 dniach: REALTIME_VOICE $0,0004, RAG_INDEXING $0,001; cała funkcja REFLECT tych użytkowników (razem z tekstem) $1,14. Łączny koszt AI w `token_usage_log` za 30 dni: $25,99 (bez Realtime, który jest tam zerowy). Przy GPT-Live dojdą tokeny modelu backendu, który prowadzi rozmowę; tego z bazy nie da się oszacować.

## 7. Proxy dla brakującego kosztu Realtime (propozycje)

1. **Prawda finansowa teraz**: panel Usage/Costs w OpenAI, filtr po modelach `gpt-realtime-mini`, `gpt-realtime-2.1-mini`, `gpt-realtime-2.1` za te same 30 dni; podzielić przez 355,6 min, aby dostać realne $/min do zestawienia z $0,05.
2. **Pierwsza rozmowa**: `posthog-data-extractor` może zsumować `input_tokens`, `output_tokens`, `cached_tokens` i `duration_s` z `first_conversation_ended` (bez podziału audio/tekst).
3. **Trwała naprawa (właściciele: `flutter-mobile` + `backend-api`)**: po sesji klient wysyła do backendu sumę `RealtimeUsage` z rozbiciem `input_token_details` (`audio_tokens`, `text_tokens`, `cached_tokens_details`) i `output_token_details`, plus czas połączenia w sekundach i `conversation_id`; backend zapisuje to przez `log_token_usage(api_type='REALTIME', user_id_override=...)`. `backend-api`: dodać wiersz `model_pricing` dla `gpt-realtime-mini`, rozważyć osobne stawki audio i tekst oraz ustawić `user_id` na wierszu mintu.

## Zapytania

Skrypty w scratchpadzie sesji (`q1.py`, `q2.py`), kluczowe fragmenty:

```sql
-- klucze per model
SELECT model, sum(CASE WHEN created_at >= now()-interval '30 days' THEN 1 ELSE 0 END), count(*)
FROM token_usage_log WHERE api_type::text='REALTIME' AND created_at >= now()-interval '90 days' GROUP BY 1;

-- sesje Reflect głosowego z directora (przerwa > 10 min = nowa sesja)
WITH d AS (SELECT user_id uid, created_at t FROM token_usage_log
           WHERE operation='director_embed_user_text' AND user_id IS NOT NULL AND created_at >= now()-interval '90 days'),
g AS (SELECT *, CASE WHEN lag(t) OVER w IS NULL OR t - lag(t) OVER w > interval '10 minutes' THEN 1 ELSE 0 END brk
      FROM d WINDOW w AS (PARTITION BY uid ORDER BY t)),
s AS (SELECT *, sum(brk) OVER (PARTITION BY uid ORDER BY t ROWS UNBOUNDED PRECEDING) sg FROM g),
seg AS (SELECT uid, sg, min(t) st, count(*) n, extract(epoch FROM max(t)-min(t)) sec FROM s GROUP BY 1,2)
SELECT count(*), count(DISTINCT uid), percentile_cont(0.5) WITHIN GROUP (ORDER BY sec/60), sum(sec/60) FROM seg;

-- pierwsza rozmowa: to samo na messages JOIN conversations
-- WHERE modality='voice' AND entry_origin='onboarding_first_conversation', partycja per conversation_id
```

Prywatność: same agregaty, bez treści, bez identyfikatorów. Segmenty poniżej 25 użytkowników mają ukryty rozkład; sumy minut podane jako wielkości operacyjne całej populacji głosu.
