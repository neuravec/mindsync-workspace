# Audyt modelu i procesu generacji powiadomień AI (płacący użytkownicy)

**Data:** 2026-09-13
**Autor:** data-analytics (read-only, zero edycji kodu)
**Okno danych:** ostatnie 30 dni, prod Postgres (`token_usage_log`, `notification_moments`), zapytania przez `database-administrator` (Heroku one-off dyno, wyłącznie SELECT)
**Kontekst:** operator tnie generowanie AI dla użytkowników bez premium (robi to `backend-api`). To jest druga połowa: dla tych, którzy AI zostaną, sprawdzić czym generujemy i czy da się taniej lub lepiej.

## Streszczenie (dla niecierpliwych)

- Model na produkcji: **`gpt-5.4-mini`** dla 100% z 105 567 wywołań NOTIFICATION w 30 dni. Potwierdzone bezpośrednio z bazy (nie przez `heroku config` – patrz pkt 1).
- Nagłówek operatora ($91,96 / 82% / 1826 kont) **potwierdzony dokładnie** (zmierzone: $90,91 / 82,0% / 1822 konta – różnica to szum ruchomego 30-dniowego okna, dzień 09-13 jest niepełny).
- **Wszystkie 8 call-site'ów AI w ścieżce powiadomień MAJĄ poprawny `track_usage("NOTIFICATION", ...)`** – ustalenie z briefu ("tylko 2 z 8") było artefaktem grepa łamanego przez wielolinijkowe wywołania. Błędna atrybucja (feature=SYSTEM/operation=unknown) to $0,005 z $90,91 – pomijalne.
- **Największe pojedyncze znalezisko audytu:** operacja `re_engagement_text_warm` to 86% kosztu ($78,08 z $90,91), a stosunek wywołań AI do faktycznie zapisanych powiadomień tego typu wynosi **~2457:1** (90 899 renderów AI → 37 zapisanych rekordów → tylko 7 kiedykolwiek dotarło/otworzono/kliknięto). To zdiagnozowany, żywy bug w `re_engagement_generator.py`, nie kwestia doboru modelu ani promptu. Szacowana oszczędność z samej naprawy: **rzędu $75-78/miesiąc**, effort niski-średni.
- Po wdrożeniu bramki premium (7 płacących + 18 kont premium, target ~25 kont): realny koszt NOTIFICATION AI spada do rzędu **$1-2/miesiąc** (ekstrapolacja z faktycznie zmierzonych $0,75/30dni dla 11 obecnie aktywnych-premium userów). To potwierdza intuicję operatora: przy tej skali dalsza optymalizacja modelu/promptu to walka o grosze – **z jednym wyjątkiem: naprawa buga re-engagement, bo on nie zniknie sam z bramką premium i psuje też koszt dla tych, którzy zostają.**
- Drugorzędne, ale tanie do naprawienia: model `gpt-5.4-mini` jest 5-7,5x droższy niż `gpt-4o-mini` przy identycznym zadaniu (2-3 zdania push copy), a komentarze w kodzie ciągle mówią "GPT-4o-mini" – to sugeruje regresję kosztową przy zmianie configu, nie świadomą decyzję.

---

## 1. Jaki model faktycznie chodzi na produkcji

**`heroku config -a mindsync` NIE pokazuje żadnej zmiennej `GPT_MODEL*`.** To nie jest błąd CLI (CLI działa, zalogowane poprawnie, dyno `web`/`worker`/`scheduler` widoczne i `up`) – to architektura configu tego projektu:

- `app/core/config.py:13-38` deklaruje `GPT_MODEL`, `GPT_MODEL_MINI`, `GPT_MODEL_41_MINI`, `GPT_MODEL_41` jako pola **bez wartości domyślnej** (`GPT_MODEL: str`, nie `Optional`) – więc muszą być ustawione skądś, inaczej `Settings()` nie wystartuje.
- `class Config: env_file = ".env"` (`config.py`, koniec pliku) – Pydantic Settings czyta te wartości z pliku `.env`.
- Plik `MindSync/.env` jest **śledzony przez git** (`git ls-files` go zwraca, nie jest w `.gitignore`) i jedzie w slugu Heroku razem z kodem. `heroku config` pokazuje tylko zmienne ustawione jako Config Vars na Heroku (24 sztuki – DATABASE_URL, REDISGREEN_URL, POSTHOG_*, SMTP_*, itd.) – GPT_MODEL* nie są tam ustawione, bo nie muszą być, żyją w `.env`.
- Zweryfikowałem, że to faktycznie ten `.env`, który jest wdrożony: `git status --porcelain -- .env` czysty (brak niezacommitowanych zmian), lokalny `HEAD` = `072a25b2`, a `heroku releases -a mindsync` pokazuje bieżący release **v548 = "Deploy 072a25b2"** – dokładnie ten sam commit.
- Lokalny `.env`: `GPT_MODEL`, `GPT_MODEL_MINI`, `GPT_MODEL_41_MINI`, `GPT_MODEL_41` wszystkie ustawione na `gpt-5.4-mini`.

**Niezależna weryfikacja z bazy (silniejszy dowód niż czytanie plików):** `token_usage_log` dla `feature='NOTIFICATION'`, 30 dni: **105 567 z 105 567 wierszy (100%) mają `model='gpt-5.4-mini'`.** Zero dryfu, zero starych/błądzących wartości. To jest ostateczne potwierdzenie – model configu i model faktycznie wysyłany do OpenAI są zgodne.

**Efekt uboczny tego ustalenia (na marginesie, nie mój obszar, zgłaszam do rozważenia):** `.env` zawiera też prawdziwe sekrety produkcyjne (klucz OpenAI, dane dostępowe do bazy, klucz szyfrowania wiadomości, sekret Apple, itd.) i jest zcommitowany do repo, a nie zarządzany przez `heroku config:set`. To oznacza, że każdy audyt "sprawdź `heroku config`" da niepełny obraz configu tej aplikacji – wart odnotowania dla `security-guardian`/`integration-devops`, poza zakresem tego audytu. Nie drukowałem i nie zapisuję tu żadnej wartości sekretu.

---

## 2. Gdzie realnie wycieka koszt

### 2.1 Korekta ustalenia z briefu: 8/8 call-site'ów, nie 2/8

Sprawdziłem każdy z 8 miejsc, gdzie `app/services/moment_text_generator.py`'s `generate_moment_text()` lub bezpośrednie `gpt_structured()` są wywoływane w ścieżce powiadomień:

| # | Plik:linia | operation | track_usage("NOTIFICATION", ...) |
|---|---|---|---|
| 1 | `moments/mood_dip_alert_generator.py:412-420` | `mood_dip_alert_text` | ✅ |
| 2 | `moments/mood_update_request_generator.py:287-295` | `mood_update_request_text` | ✅ |
| 3 | `moments/post_session_reflection_generator.py:536-544` | `post_session_reflection_text` | ✅ |
| 4 | `moments/re_engagement_generator.py:561-569` | `re_engagement_text_warm` | ✅ |
| 5 | `moments/therapy_prep_generator.py:416-424` | `therapy_prep_text` | ✅ |
| 6 | `moments/therapy_relationship_checkin_generator.py:313-321` | `therapy_relationship_checkin_text` | ✅ |
| 7 | `insights/recovery_moment_insight_detector.py:295-305` | `recovery_moment_insight_text` | ✅ |
| 8 | `notification_service.py:476-482` (`_generate_nudge_text`) | `generate_nudge_text` | ✅ (ale zobacz 2.2 – martwy kod) |

Wszystkie 8 poprawnie tagują `feature="NOTIFICATION"`. Baza to potwierdza z dwóch stron: (a) `feature='SYSTEM' OR operation='unknown'` w 30 dni = **2 wiersze, $0,005341** – pomijalne; (b) przeszukanie wszystkich innych features pod kątem `operation ILIKE '%notif%'/'%moment%'/'%push%'` = **0 wierszy**. Nic z tego kosztu nie ukrywa się pod inną etykietą.

Ustalenie "tylko 2 mają track_usage" z briefu było artefaktem greppowania `track_usage("NOTIFICATION")` jako literału w jednej linii – w kodzie wywołanie jest łamane (`track_usage(\n    "NOTIFICATION", "operation_name", ...)`), więc prosty grep łapał tylko 2 przypadki, które akurat mieściły się w jednej linii (`re_engagement_generator.py:561`, `notification_service.py:476`). To dobra wiadomość: instrumentacja kosztowa jest kompletna, nie trzeba nic doszywać.

**Kontekst historyczny (znalazłem po drodze, warto znać):** ta instrumentacja to efekt audytu z 2026-08-10 (`analytics-reports/2026-08-10-system-ai-cost-audit.md`), który zastał dokładnie te same 7 call-site'ów (1-7 powyżej) BEZ `track_usage` w ogóle – cały koszt lądował pod `feature=SYSTEM, operation=unknown` ($134,23/60dni). Ten sam audyt znalazł też architektoniczny bug ("generate-before-select waste", ~22:1) w `notification_orchestrator.py` i naprawił go tego samego dnia (fix "A14": `render_content=False/True` split – orchestrator buduje kandydatów bez płacenia za AI, a renderuje realny tekst tylko dla zwycięzcy scoringu). **Zweryfikowałem, że fix A14 nadal jest w kodzie i wygląda poprawnie** (`notification_orchestrator.py:640-741`).

### 2.2 Operacja `generate_nudge_text` to martwy kod

`notification_service.py:373-376`, komentarz wprost: *"The former `notify_post_session_nudge()` cron entry point was removed (Cadence v3, 2026-07-03) — superseded by `PostSessionReflectionGenerator`... these helpers are kept as they are still independently unit-tested"*. Sprawdziłem: `_process_first_nudges` (linia 561) i `_process_followup_nudges` (linia 715), jedyne funkcje wołające `_generate_nudge_text()`, **nie mają żadnego callera poza własnym plikiem** – zgrepowałem każdy import z `notification_service.py` w `app/tasks/`, `app/core/rq_scheduler_setup.py`, `app/api/v1/endpoints/` – tylko `get_access_token`, `send_fcm_to_all_user_tokens`, `get_user_fcm_tokens` są gdziekolwiek importowane, nigdy `_process_*_nudges`. Ta operacja jest nieosiągalna na produkcji od 2026-07-03 (ponad 2 miesiące). Baza to potwierdza pośrednio: nie pojawia się w ogóle w rozbiciu po `operation` dla 30 dni (patrz tabela 2.3 – tylko 6 operacji, nie 8). **Zero kosztu, zero do zrobienia tutaj** – ale kod wart odnotowania jako kandydat do usunięcia (nie moja decyzja/plik do edycji poza tym audytem).

### 2.3 Rozbicie kosztu po operacji (30 dni, prod)

| operation | wywołań (n) | koszt USD | % kosztu NOTIFICATION | koszt/wywołanie |
|---|---:|---:|---:|---:|
| **`re_engagement_text_warm`** | **90 899** | **$78,077917** | **85,9%** | $0,000859 |
| `mood_update_request_text` | 9 350 | $8,192507 | 9,0% | $0,000876 |
| `therapy_relationship_checkin_text` | 5 169 | $4,503098 | 5,0% | $0,000871 |
| `post_session_reflection_text` | 69 | $0,062477 | 0,07% | $0,000905 |
| `therapy_prep_text` | 69 | $0,059835 | 0,07% | $0,000867 |
| `mood_dip_alert_text` | 11 | $0,009929 | 0,01% | $0,000903 |
| `generate_nudge_text` | 0 (martwy kod, patrz 2.2) | $0 | – | – |
| **Razem NOTIFICATION** | **105 567** | **$90,905763** | 100% | – |

Koszt pojedynczego wywołania jest **bardzo jednolity** między typami (~$0,00086-0,00091) – różnice w koszcie całkowitym to niemal wyłącznie kwestia **wolumenu wywołań**, nie różnic w rozmiarze promptu między typami momentów.

### 2.4 Właściwe źródło wycieku: bug w `re_engagement_generator.py`, nie model ani prompt

To jest **jedyne znalezisko w tym audycie warte natychmiastowej naprawy przed jakąkolwiek zmianą modelu**. Dociekłem mechanizmu na podstawie kodu + drugiego zapytania do prod bazy porównującego wywołania AI z faktycznie zapisanymi rekordami:

**Liczby:** 90 899 wywołań AI (koszt $78,08) → **37 zapisanych** rekordów `notification_moments` typu `RE_ENGAGEMENT` z `is_ai_generated=true` (24 unikalnych userów) → z tych 37: **30 wygasło (EXPIRED) niewysłanych**, 5 SENT, 1 OPENED, 1 ACTED. Realnie użytecznych wyników: 7 z 37.

- **Stosunek marnotrawstwa: ~2457:1** (90 899 / 37) – ostrzejszy wariant licząc tylko to, co faktycznie dotarło/zaangażowało (SENT+OPENED+ACTED=7): **~12 986:1**.
- Rozkład dzienny renderów AI jest płaski (~3 200-3 850/dzień, stabilnie), a rozkład zapisanych momentów RE_ENGAGEMENT to 1-3/dzień z 10 dniami na zero w 30-dniowym oknie – kompletnie oderwane od siebie liczby, co samo w sobie jest sygnałem, że coś płaci za AI bez związku z tym, co faktycznie trafia do użytkownika.

**Mechanizm (zlokalizowany na poziomie linii kodu):**
1. `re_engagement_generator.py:60-81` – limit projektowy to **maksymalnie 2 AI-generowane push'e na epizod nieaktywności** (`_MAX_RE_ENGAGEMENT_SENDS = 2`, push #1 od dnia 3, push #2 od dnia 7).
2. `re_engagement_generator.py:288-296` – `dedup_key = f"RE_ENGAGEMENT:{user_id}:{last_activity_str}:push{push_number}"`, egzekwowany twardym `UNIQUE(user_id, dedup_key)` constraintem w tabeli `notification_moments` (`notification_moment.py:154`).
3. `re_engagement_generator.py:376-415` (`_count_re_engagement_moments_since`) – **celowo** liczy tylko statusy `PENDING/SENT/OPENED/ACTED` jako "już wysłane"; `EXPIRED` i `DISMISSED` są jawnie wykluczone (docstring: *"they represent delivery that did not result in engagement"*).
4. **Efekt uboczny:** gdy push #1 wygasa niewysłany (co dzieje się w **81% przypadków** – 30 z 37), `sent_count` wraca do 0 na następnym ticku. Użytkownik znów wygląda na "eligible" dla push #1. Orchestrator (mimo działającego fixu A14) na każdym hourly-tickcie od nowa **renderuje i PŁACI za AI** dla tego samego `dedup_key`, po czym `_persist_moment` (`notification_orchestrator.py:756-778`) po cichu odrzuca zapis jako duplikat (constraint z pkt. 2) – orchestrator ma nawet licznik na tę sytuację (`_duplicate_persist_skips`), więc mechanizm jest znany/obserwowany, ale nie zaadresowany na poziomie kosztu.

To jest **osobny bug od tego, co naprawił fix A14 z 08-10** (A14 naprawił "generuj dla każdego kandydata w rundzie scoringu"; ten bug to "generuj od nowa na każdym tickcie dla tego samego, już wygasłego kandydata"). Dwa różne mechanizmy w tym samym podsystemie.

**Dlaczego aż 81% wygasa?** Nie badałem tego głębiej (poza zakresem tego audytu, dotyczy warstwy doręczania push, nie generacji AI) – ale sensowna hipoteza: RE_ENGAGEMENT z definicji celuje w userów nieaktywnych 3+ dni, czyli dokładnie tę populację, która najbardziej prawdopodobnie ma martwy/nieważny token FCM albo już odinstalowała appkę. To nie tłumaczy samego mechanizmu marnotrawstwa (błąd jest w logice eligibility, nie w doręczaniu), ale tłumaczy, czemu tak duża część kwalifikujących się userów kończy w EXPIRED zamiast SENT.

**Rekomendowana naprawa (zarys, nie mój plik do edycji w tym zadaniu – `backend-api` nie jest tu właścicielem, to plik `data-analytics`, ale to osobne zadanie od tego audytu):** `_count_re_engagement_moments_since` powinno liczyć **istnienie `dedup_key` per push_number** niezależnie od statusu (albo: sprawdzać `notification_moments` z tym samym `dedup_key` bez filtra statusu przed w ogóle wejściem w rendering), zamiast filtrować po statusie. Jeśli push wygasł niewysłany, to osobny problem (do zbadania w warstwie doręczania) – nie powód, żeby płacić za AI drugi/setny raz za tę samą treść, która i tak trafi w tę samą ścianę.

**Sugestia z audytu bazy (nie zweryfikowana przeze mnie w tym przebiegu):** warto sprawdzić, czy ten sam wzorzec (expire → reset eligibility → re-render → dedup-discard) występuje też w pozostałych 5 generatorach scoringowych (`mood_update_request`, `therapy_relationship_checkin`, `post_session_reflection`, `therapy_prep`, `mood_dip_alert`) – ich koszt jest już dziś dużo mniejszy ($8,19/$4,50/$0,06/$0,06/$0,01), ale jeśli mają tę samą logikę "wyklucz EXPIRED z liczenia", to samo źródło marnotrawstwa może tam rosnąć w przyszłości.

---

## 3. Ile tokenów zjada jedno wywołanie

Z bazy (30 dni, per operacja – liczby bardzo spójne między typami):

| operation | avg prompt_tokens | avg completion_tokens | avg cached_tokens |
|---|---:|---:|---:|
| re_engagement_text_warm | 574,4 | 95,1 | 0 |
| mood_update_request_text | 583,0 | 97,5 | 0 |
| therapy_relationship_checkin_text | 580,0 | 96,9 | 0 |
| post_session_reflection_text | 610,7 | 99,4 | 0 |
| therapy_prep_text | 594,1 | 93,7 | 0 |
| mood_dip_alert_text | 618,6 | 97,5 | 0 |

**`cached_tokens = 0` na 100% wierszy, zero wyjątków przez 30 dni** – żadne cachowanie promptów nie jest dziś aktywne (co odpowiada wprost na część pytania 5).

**Ile z tego to prompt systemowy powtarzany za każdym razem?** Zmierzyłem `_DEFAULT_MOMENT_TEXT_GENERATOR_PROMPT` (`moment_text_generator.py:43-69`) na **1420 znaków ≈ 355 tokenów** (szacunek znaki/4), plus `_FORMATTING_SUFFIX` (`openai_service.py:26-31`, doklejany do KAŻDEGO promptu systemowego w całej aplikacji) ≈ 250 znaków ≈ 65 tokenów. To daje **~420 tokenów identycznego, stałego tekstu na każde wywołanie**, wobec zmierzonych ~580-620 tokenów `prompt_tokens` łącznie. **Czyli ok. 68-72% promptu wejściowego to sztywna treść, identyczna niezależnie od użytkownika, typu momentu czy kontekstu.** Reszta (~150-200 tokenów) to zmienna część promptu systemowego (interpolacja `{orca_name}`, `{tone_archetype}`, `{moment_type}`, `{context_summary}`, `{language}`) plus narzut schematu JSON dla structured output (`response_format=pydantic_structure`, liczony przez OpenAI jako część `prompt_tokens`).

Sprawdziłem `ai_context` budowany przez generatory – jest wszędzie mały (3-4 pola tekstowe, np. `mood_dip_alert_generator.py:161-169`: `symptom_name`, `scores_last_14d`, `recent_avg_score`, `pattern_hint`; `therapy_prep_generator.py:408-412`: `session_date`, `hours_until_session`, `reminder_kind`; `mood_update_request_generator.py` i `therapy_relationship_checkin_generator.py` przekazują wręcz jednopolowy dict inline). To potwierdza: zmienność między wywołaniami jest mała, dominuje stały koszt promptu.

**Czy opłaca się prompt caching (OpenAI):** przy ~580 tokenach łącznego promptu i typowym progu automatycznego cache'owania OpenAI w okolicach ~1024 tokenów, ten prompt jest **za krótki, żeby cache w ogóle się włączył** – nawet gdyby przestawić kolejność (stała treść na początku, zmienna na końcu), cały prompt nie przekracza progu. Dodatkowo obecna kolejność w `_DEFAULT_MOMENT_TEXT_GENERATOR_PROMPT` wstawia `{orca_name}` już w drugim zdaniu ("The user's companion is a virtual Orca named {orca_name}") – więc nawet krótki wspólny prefiks łamie się na personalizacji od razu, zanim cokolwiek mogłoby się cache'ować. **Wniosek: prompt caching (w obecnej architekturze OpenAI) nie da tu żadnej realnej oszczędności, niezależnie od przeróbek promptu** – wolumen tokenów jest za mały, żeby próg cache'owania miał znaczenie.

---

## 4. Czy prompt jest przerośnięty

Tak, częściowo – 68-72% promptu to stała treść (patrz pkt 3), a output to 2-3 zdania na ekran blokady (`push_title` ≤50 znaków, `push_body` ≤110 znaków, `in_app_headline` ≤80, `in_app_body` ≤300 – limity z `moment_text_generator.py:82-101`).

Co konkretnie można wyciąć bez utraty jakości (`moment_text_generator.py:43-69`):
- **Opisy 5 archetypów tonu** ("realist: direct, grounded, no fluff... coach: motivating... friend: warm, casual... sage: thoughtful, reflective... explorer: curious, inviting") – to ~130 znaków opisu dla WSZYSTKICH 5 tonów, mimo że dla danego wywołania liczy się tylko JEDEN z nich (`{tone_archetype}` wybiera jeden). Można to zredukować do jednozdaniowego opisu tylko wybranego tonu, interpolowanego zamiast całej listy – oszczędność ~25-30 tokenów/wywołanie bez utraty informacji (model i tak dostaje tylko instrukcję dla właściwego tonu).
- **7 ponumerowanych zasad formatowania** (punkty 1-7) – częściowo redundantne z `_FORMATTING_SUFFIX`, który już zakazuje em-dash i każe dzielić długi tekst na akapity. Limity znaków (punkty 3-6) można skondensować do jednej linijki z czterema liczbami zamiast czterech pełnych zdań.
- **Blok CRISIS SAFETY** (`moment_text_generator.py:62-68`) – to jedyna część, której **nie wolno** ciąć ani skracać ponad rozsądek – to zabezpieczenie na wypadek podwyższonego distress u użytkownika, kosztuje ~230 znaków ≈ 55-60 tokenów, i jest to koszt, który warto ponosić.

**Szacunek:** skrócenie punktów 1 i 2 powyżej mogłoby zejść z ~355 tokenów stałej treści do ~220-250 tokenów, czyli ~100-130 tokenów mniej na wywołanie (przy zachowaniu CRISIS SAFETY w całości). Przy obecnym wolumenie (105 567 wywołań/30dni) i cenie inputu `gpt-5.4-mini` ($0,75/1M), to ~$0,08-0,10/miesiąc oszczędności – **dosłownie grosze**, bo input jest tani względem output w tym modelu. Warte zrobienia przy okazji innej zmiany w tym pliku, nie jako samodzielna akcja – efekt dolarowy jest znikomy w porównaniu do punktu 2.4.

`notification_service.py`'s `NUDGE_PROMPT_DEFAULT`/`NUDGE_FOLLOWUP_PROMPT_DEFAULT` (linie 369-401, `POST_SESSION_NUDGE_PROMPT`/`POST_SESSION_NUDGE_FOLLOWUP_PROMPT` w configu) są już krótkie i celne (~100 słów) – ale to i tak martwy kod (pkt 2.2), więc nieistotne kosztowo.

**Znalezisko przy okazji:** `RE_ENGAGEMENT_PROMPT` w `app/core/config.py:261-278` (osobny, dłuższy prompt specyficzny dla re-engagement, z własnymi zasadami np. "NEVER use clinical terms... NEVER be guilt-inducing") **nie jest nigdzie używany w kodzie** – `re_engagement_generator.py`'s WARM path woła generyczne `generate_moment_text()` z generycznym `MOMENT_TEXT_GENERATOR_PROMPT`, nie z tym dedykowanym promptem. To martwa konfiguracja (prawdopodobnie pozostałość wcześniejszej implementacji) – zero kosztu, ale warta odnotowania jako dług techniczny/dezorientująca dla kogoś czytającego config.

---

## 5. Czy da się batchować lub cache'ować

| Opcja | Szacowana oszczędność | Koszt wdrożenia | Ocena |
|---|---|---|---|
| **Prompt caching (OpenAI automatyczny)** | ~$0 | – | Prompt (~580 tok.) jest poniżej progu, przy którym OpenAI w ogóle zaczyna cache'ować (~1024 tok.). `cached_tokens=0` na 100% wierszy potwierdza, że nic się nie cache'uje dziś. Reorganizacja promptu (stałe na początku) nie pomoże – wolumen wciąż za mały. **Nie warto.** |
| **Batch API (OpenAI, -50%)** | Teoretycznie ~$45/miesiąc na obecnym wolumenie, ALE patrz zastrzeżenie | Średni-wysoki (redesign) | Orchestrator to cron hourly (`rq_scheduler_setup.py:317-349`, `"0 * * * *"`), a decyzja "kto wygrywa slot" zależy od świeżego stanu (dismissal counts, action rates, eligibility) w momencie ticka – Batch API ma SLA 24h, co jest niezgodne z tym, że wynik scoringu musi być aktualny w chwili wysyłki. Częściowo pasowałoby do typów z długim naturalnym oknem (re-engagement day 3/7), ale scoring i tak dzieje się per-tick, nie per-batch. **Realistycznie: nie opłaca się przy obecnej architekturze "score then render synchronously"** bez większego refaktoru. Gdyby #2.4 zostało naprawione i wolumen spadł do faktycznie ~kilkuset wywołań/miesiąc, korzyść z batcha i tak byłaby $ kilka/miesiąc – nie warto ryzyka refaktoru. |
| **Deduplikacja identycznych kontekstów / cache treści per (typ, ton, język)** | Nie do oszacowania rzetelnie przed naprawą #2.4 | Niski-średni | Konteksty są już dziś małe i w większości generyczne (`mood_update_request`, `therapy_relationship_checkin` mają praktycznie tylko `reminder_kind` jako zmienną) – dobry kandydat na cache Redis keyowany `(moment_type, tone_archetype, language)` z TTL rzędu 24-72h, bo wiele userów dzieli te same wartości tych trzech pól. Ale: (a) to nie adresuje głównego problemu (2.4), (b) po naprawie #2.4 legalny wolumen prawdopodobnie spadnie na tyle (patrz pkt 7), że efekt dolarowy będzie w granicach $1-3/miesiąc. **Niski priorytet, rozważyć dopiero po #2.4.** |
| **Naprawa #2.4 (nie jest "cache" sensu stricto, ale to realna redukcja wywołań)** | ~$75-78/miesiąc | Niski-średni | Patrz pkt 2.4 i 8. To jedyna pozycja w tej sekcji z realnym, dużym zwrotem. |

---

## 6. Czy model jest dobrany do zadania

Zadanie: 2-3 zdania push copy, structured output, `reasoning_effort="none"` już ustawiony na każdym wywołaniu (`openai_service.py:3634/3640/3687` – `extra_body={"reasoning_effort": "none"}` na WSZYSTKICH wywołaniach `gpt_function`/`gpt_structured`, nie tylko notification). To już wyłącza "podatek za rozumowanie" modeli z rodziny GPT-5 – dobra, tania decyzja, którą ktoś już podjął.

**Aktualne ceny OpenAI (sprawdzone 2026-09-13, `developers.openai.com/api/docs/pricing`, per 1M tokenów):**

| Model | Input | Cached input | Output |
|---|---:|---:|---:|
| `gpt-5.4-mini` (obecny) | $0,75 | $0,075 | $4,50 |
| `gpt-4.1-mini` | $0,40 | $0,10 | $1,60 |
| `gpt-5-mini` | $0,25 | $0,025 | $2,00 |
| `gpt-4.1-nano` | $0,10 | $0,025 | $0,40 |
| `gpt-4o-mini` | $0,15 | $0,075 | $0,60 |
| `gpt-5-nano` | $0,05 | $0,005 | $0,40 |

Komentarz w `moment_text_generator.py:10-11` mówi wprost: *"Uses GPT-4o-mini (GPT_MODEL_41_MINI) for cost efficiency"* – ale `GPT_MODEL_41_MINI` w rzeczywistości wskazuje na `gpt-5.4-mini`, nie na `gpt-4o-mini`. Przy zmierzonych ~580 tok. input / ~95 tok. output na wywołanie, koszt per-wywołanie pod różnymi modelami (przeliczone z rzeczywistych tokenów, bez cache):

| Model | Koszt/wywołanie | vs. `gpt-5.4-mini` |
|---|---:|---:|
| `gpt-5.4-mini` (obecny, zmierzony) | $0,000859 | 1,0x (bazowy) |
| `gpt-5-mini` | $0,000334 | 2,6x taniej |
| `gpt-4.1-mini` | $0,000388 | 2,2x taniej |
| `gpt-4o-mini` | $0,000143 | **6,0x taniej** |
| `gpt-4.1-nano` | $0,0000954 | 9,0x taniej |
| `gpt-5-nano` | $0,0000667 | **12,9x taniej** |

To nie jest hipoteza – komentarz kodu literalnie zakłada model, który jest 6x tańszy niż to, co faktycznie leci do OpenAI. Wygląda na to, że globalna zmienna `GPT_MODEL_41_MINI` (używana w **13 różnych plikach**, nie tylko w powiadomieniach – `conversations.py`, `reflect.py`, `chart_explanations.py`, `clinician_ai.py`, `mental_health_card.py`, `profile_service.py`, `thread_matching.py`, `voice_director.py`, `thread_context.py`, plus te 2 tutaj) została w pewnym momencie przestawiona na `gpt-5.4-mini` globalnie (prawdopodobnie decyzja jakościowa dla rozmów na żywo / bardziej wymagających zadań), a powiadomienia "pojechały w pakiecie" bez osobnej rewizji, mimo że ich zadanie (2-3 zdania, structured output, zero rozumowania) nie wymaga tej samej klasy modelu co np. `voice_director.py` (żywa rozmowa) czy `conversations.py`.

**Rekomendacja:** dla samego zadania "2-3 zdania push copy" `gpt-4o-mini` lub `gpt-5-nano` powinny dać porównywalną jakość przy 6-13x niższym koszcie – ale **zmiana `GPT_MODEL_41_MINI` globalnie jest ryzykowna** (dotyka 11 innych, niepowiadomieniowych ścieżek, w tym rozmowę na żywo – `voice_director.py`, `conversations.py`). Właściwa droga: **nowa, dedykowana zmienna configu** (np. `GPT_MODEL_NOTIFICATION`) używana wyłącznie w `moment_text_generator.py:164` i `notification_service.py:481`, domyślnie ustawiona na tańszy model, bez ruszania pozostałych 11 plików. To zmiana w `app/core/config.py`, który należy do `backend-api` – wymaga koordynacji, nie mogę tego zrobić sama.

**Uwaga techniczna dla implementującego:** `reasoning_effort` w `extra_body` (`openai_service.py:3634/3640/3687`) to parametr specyficzny dla rodziny modeli z rozumowaniem (o-series/GPT-5). `gpt-4o-mini` **nie jest** modelem rozumującym – przekazanie mu nieznanego parametru w `extra_body` może zwrócić 400 "Unsupported parameter" (nie zweryfikowałem tego empirycznie na żywym API – zaznaczam wprost, że to do sprawdzenia przed wdrożeniem, nie pewnik). Jeśli firma zdecyduje się na `gpt-4o-mini`, `reasoning_effort` trzeba usunąć z tej ścieżki wywołania (albo uwarunkować per-model). `gpt-5-nano`/`gpt-5-mini` powinny akceptować ten sam parametr co `gpt-5.4-mini` (ta sama rodzina), więc dla nich zmiana jest bezpieczniejsza pod tym kątem.

**Czy warto podnieść jakość dla tych, co zostają (po bramce premium)?** Przy docelowej populacji ~25 kont i koszcie rzędu $1-2/miesiąc (pkt 7), różnica między `gpt-5.4-mini` a np. droższym `gpt-4.1` albo Claude Haiku 4.5 ($1,00/$5,00 za 1M tokenów u Anthropic, porównywalne z `gpt-5.4-mini`) to dosłownie centy miesięcznie. **Tutaj nie ma dylematu koszt/jakość – można spokojnie zostawić obecny model (albo nawet podnieść) dla tej małej grupy, bo wolumen czyni to nieistotnym finansowo.** Przejście na zupełnie inny provider (Anthropic) wymagałoby osobnej integracji SDK i nie jest uzasadnione przy tej skali kosztu.

---

## 7. Ile realnie zostanie po cięciu (bramka premium)

Zapytałem bazę wprost, ile dziś kosztuje NOTIFICATION dla userów z aktywnym premium (`user_subscription.subscription_type='PREMIUM' AND is_active=true`) vs reszta:

| segment | koszt/30dni | unikalnych userów |
|---|---:|---:|
| **premium aktywny (`is_active=true`)** | **$0,751024** | **11** |
| PREMIUM, ale `is_active=false` (wygasłe) | $66,733110 | 1 163 |
| BASIC (nigdy premium) | $23,420767 | 648 |

**Kluczowe, niezależne od tego audytu znalezisko z zapytania do bazy** (warte przekazania do `backend-api` przy wdrażaniu bramki): dominującym źródłem kosztu **nie są** userzy bez premium – to **1163 userów z WYGASŁYM premium** (73,4% kosztu, $66,73), prawie 3x więcej niż nigdy-nieupgradowani BASIC (25,8%, $23,42). **Bramka musi sprawdzać `is_active=true`, nie sam fakt posiadania `subscription_type='PREMIUM'`** – inaczej ~73% dzisiejszego kosztu przetrwa wdrożenie, bo ci userzy formalnie "mają" typ subskrypcji PREMIUM w rekordzie, tylko nieaktywny.

**Operator podał docelowo 7 aktywnych płacących + 18 kont premium (~25 kont)** – to więcej niż 11 zmierzonych dziś jako `is_active=true`. Rozbieżność prawdopodobnie wynika z innej definicji "premium" po stronie operatora (np. licząc też trialujących albo inny status) niż `subscription_type='PREMIUM' AND is_active=true` w bazie – **nie da się tego rozstrzygnąć bez doprecyzowania z operatorem/`backend-api`, jaka dokładnie kolumna/warunek definiuje "kto zostaje po bramce".**

**Ekstrapolacja (najlepsza dostępna, oznaczona jako szacunek):** średni koszt na aktywnego-premium usera to $0,751024/11 ≈ **$0,068/user/30dni** (nieco wyżej niż średnia calej populacji $0,0499/user – ci userzy nie są tańsi niż przeciętny). Przy 25 docelowych kontach: **25 × $0,068 ≈ $1,71/30dni**, czyli **rzędu $1-2/miesiąc**.

**Wniosek:** tak, po wdrożeniu bramki premium dalsza optymalizacja modelu/promptu przestaje mieć znaczenie finansowe – to faktycznie "walka o grosze" przy tej skali. **Wyjątek: bug z pkt 2.4 nie zniknie sam z bramką.** Nawet w 25-osobowej populacji, jeśli którykolwiek z tych userów pójdzie w 3+ dniową nieaktywność i trafi w tę samą pętlę EXPIRED→reset→re-render, koszt na tę osobę może wystrzelić nieproporcjonalnie (choć przy tak małej populacji absolutny pułap strat jest i tak niski, rzędu pojedynczych dolarów miesięcznie nawet w najgorszym przypadku – to nie jest już problem biznesowy, ale wciąż warto naprawić bug, bo koszt naprawy jest niski, a "płacimy za coś bez sensu" nie przestaje być prawdą tylko dlatego, że kwota jest mała).

---

## 8. Rekomendacja końcowa (posortowana wg stosunku oszczędność/wysiłek)

| # | Rekomendacja | Oszczędność | Wysiłek | Kto | Priorytet |
|---|---|---|---|---|---|
| 1 | **Napraw `_count_re_engagement_moments_since` (pkt 2.4)** – licz istnienie `dedup_key` niezależnie od statusu EXPIRED/DISMISSED, nie tylko statusy "żywe" | **~$75-78/miesiąc** | Niski-średni (1 plik, logika już rozumiana, warto dorzucić test regresyjny na "expired push nie generuje nowego AI-calla") | `data-analytics` | **ZRÓB TERAZ** |
| 2 | Zbadaj, czy ten sam wzorzec (EXPIRED wykluczone z liczenia) występuje w pozostałych 5 generatorach scoringowych | Nieznana, ale rosnąca w czasie jeśli nie sprawdzone | Niski (przegląd kodu, ~30-60 min) | `data-analytics` | Zrób przy okazji #1 |
| 3 | Zbadaj, czemu 81% RE_ENGAGEMENT push'y wygasa niewysłanych (warstwa doręczania, nie generacji) | Pośrednia (mniej "eligible" cykli = mniej wywołań AI nawet bez fixu #1) | Średni (wymaga logów FCM/delivery, może inny właściciel) | `backend-api`/`integration-devops` | Warto, osobne zadanie |
| 4 | Dedykowany `GPT_MODEL_NOTIFICATION` config zamiast dzielenia `GPT_MODEL_41_MINI` z 11 innymi funkcjami, ustawiony na `gpt-4o-mini` lub `gpt-5-nano` (6-13x taniej per-wywołanie) | Przed bramką premium: rzędu $65-80/miesiąc PRZY OBECNYM wolumenie (ale ten wolumen w większości zniknie po #1); po bramce: centy/miesiąc | Niski-średni (nowe pole w `config.py` – wymaga `backend-api`; plus weryfikacja `reasoning_effort` z modelem docelowym) | `backend-api` (config) + `data-analytics` (call sites) | Zrób, ale DOPIERO po #1 i po bramce premium – inaczej optymalizujesz koszt, który i tak zniknie |
| 5 | Skróć stałą treść promptu systemowego (opisy tonów, zasady formatowania) w `moment_text_generator.py` | ~$0,08-0,10/miesiąc przy obecnym wolumenie; jeszcze mniej po #1 | Niski (edycja jednego stringa) | `data-analytics` | Nie warte osobnego zadania – zrób przy okazji następnej zmiany tego pliku |
| 6 | Cache treści per (moment_type, tone, language) z krótkim TTL | Nie do oszacowania rzetelnie przed #1; prawdopodobnie $1-3/miesiąc po #1 | Niski-średni | `data-analytics` | Niewarte zachodu przy tej skali |
| 7 | Prompt caching OpenAI (natywny) | ~$0 | – | – | **Nie rób** – prompt za krótki, żeby przekroczyć próg cache'owania |
| 8 | Batch API | Niepewna, prawdopodobnie ujemna netto przy uwzględnieniu ryzyka refaktoru | Wysoki | – | **Nie rób** – niezgodne z architekturą "score then render per-tick"; nawet po #1 wolumen będzie za mały, żeby uzasadnić refaktor |
| 9 | Usuń martwy kod `generate_nudge_text`/`_process_*_nudges` (pkt 2.2) | $0 (już nie kosztuje) | Niski | `data-analytics`/`backend-api` | Porządek, nie priorytet kosztowy |

**Jednym zdaniem:** 86% kosztu powiadomień AI to nie kwestia modelu ani promptu – to bug w logice re-engagement, który płaci za render AI za każdym razem, gdy poprzedni push wygasł niedostarczony (co dzieje się w 4 na 5 przypadków). Napraw to jedno (pkt 2.4), a rozmowa o modelu/promptowym cięciu staje się w większości nieaktualna, bo wolumen i tak spadnie o rząd wielkości niezależnie od bramki premium. Po bramce premium reszta tematu to faktycznie grosze ($1-2/miesiąc), z zastrzeżeniem, że #1 warto zrobić i tak, bo bug nie zniknie sam.

---

## Zastrzeżenia i czego nie ustaliłem

- **Rozbieżność 7+18 kont operatora vs 11 zmierzonych `is_active=true`** – nie wiem, jaka dokładnie definicja "premium" ma obowiązywać po stronie bramki; do doprecyzowania z operatorem/`backend-api` przed finalnym ustaleniem budżetu na `is_active` (pkt 7).
- **Nie zweryfikowałem empirycznie**, czy `gpt-4o-mini`/`gpt-5-nano` faktycznie akceptują `extra_body={"reasoning_effort": "none"}` bez błędu 400 – oznaczone wprost w pkt 6 jako "do sprawdzenia przed wdrożeniem".
- **Nie zbadałem**, czemu konkretnie 81% RE_ENGAGEMENT push'y wygasa (pkt 2.4/pkt 8 #3) – to wymaga logów warstwy doręczania FCM, poza zakresem tego audytu kosztowego.
- **Nie sprawdziłem** pozostałych 5 generatorów scoringowych pod kątem tego samego wzorca EXPIRED-wykluczenia (pkt 8 #2) – ich koszt jest dziś mały, więc nie było to priorytetem w tym przebiegu, ale mogą rosnąć.
- Liczby kosztowe pochodzą z ruchomego 30-dniowego okna zapytanego 2026-09-13 ~07:55 UTC; dzień 09-13 był niepełny (~8h) w chwili pomiaru – stąd $90,91 zmierzone vs $91,96 podane w briefie (różnica ~1,1%, w granicach szumu, nie problem z danymi – potwierdzone przez `database-administrator`).
- Ceny OpenAI (pkt 6) pobrane z `developers.openai.com/api/docs/pricing` w dniu audytu (2026-09-13) – ceny modeli AI zmieniają się często, warto zweryfikować ponownie przed wdrożeniem jeśli minie więcej niż kilka tygodni.
