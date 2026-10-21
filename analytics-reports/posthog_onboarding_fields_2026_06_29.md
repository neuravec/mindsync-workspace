# Onboarding — czy userzy uzupełniają dodatkowe pola profilujące? — Business Insight Report

- **Data**: 2026-06-29
- **Analityk**: growth-analyst
- **Pytanie biznesowe**: Czy w danych widać, że użytkownicy faktycznie UZUPEŁNIAJĄ dodatkowe pola dodane do onboardingu (age band, inclusive gender, currently_in_therapy + withdrawal, challenges/interests, journey free-text, lead source)? Cel pól = zebrać WIĘCEJ danych o userze — czy jest realizowany?
- **Okno danych**: 40–60 dni (pola żyją od ~2026-05-29). Before/after 27.06 marginalny — pola NIE są nowe w update'cie 2.0.60.
- **Źródła**: PostHog (proj. 141170, EU) — HogQL read-only przez REST query API (`POSTHOG_PERSONAL_API_KEY` z `MindSync/.env`, wartość nigdy nie wypisana). Model `MindSync/app/models/models.py` (`UserProfile`, `ConsentRecord`). **Postgres `user_profile` NIE odpytany — brak sterownika PG w tej sesji** (patrz Rekomendacje — to definitywne źródło prawdy o wypełnieniu wartości).
- **Confidence**: Wniosek dla `lead_source` i „gdzie lądują dane" = **High**. Per-field VALUE fill-rate = **nierozstrzygalny z PostHog** (wymaga Postgres). Small-n jak zwykle (realnie ~70–120 userów w onboardingu w oknie).

> Towarzyszy raportowi `analytics-reports/posthog_post_update_2026_06_29.md` (post-update health check). Ten plik odpowiada wyłącznie na pytanie o uzupełnianie pól.

---

## TL;DR

- **Rdzeń onboardingu jest uzupełniany dobrze.** 8 kroków (`legal_gate → challenges → intensity → journey → modality → schedule → companion → lead_source`). Step-to-step retention 88–99% dla 7 pierwszych kroków; ~71 z ~106 wchodzących kończy core (companion) = ~67%.
- **`lead_source` jest praktycznie NIE wypełniany przez userów.** Krok `lead_source` osiąga tylko **7 userów**, jawny wybór (`onboarding_lead_source_selected`) = **6 userów**, wariant „inne" (free-text) = **1 user** — mimo że pole figuruje w payloadzie zapisu profilu dla **93 userów** (prawdopodobnie domyślny null). Cel „zbieramy lead source od userów" = **NIEzrealizowany w aplikacji**. (Realne źródło pozyskania i tak jest łapane automatycznie z UTM/install-referrer: `utm_source/campaign/medium`, `fbclid`, `gclid` na personach.)
- **Czy dane LĄDUJĄ: tak — ale do POSTGRES, nie do PostHog.** `profile_updated` odpala dla **148 userów/45d** z payloadem `[age, age_band, currently_in_therapy, full_name, gender, lead_source, pronouns]` (7-field flow żyje od 2026-05-29). To dowodzi, że formularz zbiera te pola i pisze je do bazy.
- **PostHog jest CELOWO ślepy na 2 wrażliwe pola.** Model: `currently_in_therapy` = „Article 9 health data, write-gated by ARTICLE9_HEALTH consent"; `lead_source` = „NOT sent to PostHog (re-identification risk)". Na personach PostHog ledwie lądują `gender`/`age_band` (po kilka), a `currently_in_therapy`/`lead_source`/`pronouns`/`age` — **wcale (by design)**. → **wypełnienia tych pól NIE da się zweryfikować z PostHog**; to nie błąd, to prywatność.
- **GAP nadrzędny**: PostHog potwierdza, że pole było CZĘŚCIĄ ZAPISU, ale nie czy WARTOŚĆ jest niepusta. Dla `currently_in_therapy` (opcjonalne, Art.9 + withdrawal) i `lead_source` to różnica między „zebrane" a „puste". **Definitywna odpowiedź = jeden read-only SELECT na Postgres `user_profile`** (zob. Rekomendacje) — dziś niewykonany (brak sterownika PG).
- **Inne gapy**: `therapy_context_updated.updated_section` = **null dla wszystkich 808 eventów** (nie wiemy która sekcja); wybrane WARTOŚCI challenges/intensity/modality/schedule nie są zbierane (tylko completion kroku); journey free-text content nie jest zbierany (dobrze dla prywatności, ale fill-rate nieznany); brak eventu zgody Art.9/withdrawal → consent-rate niemierzalny w PostHog.
- **Before/after 27.06**: pola dodano ~05-29 (Wave 1/3/4), ~miesiąc PRZED buildem 2.0.60. 7-field payload nadal odpala po 27.06 (10 ev). Brak zmiany przypisywalnej do update'u; nowy build = głównie testerzy.

---

## Czy to w ogóle MIERZYMY? (mapa pole → sygnał w PostHog)

| Pole (gdzie w onboardingu) | Sygnał w PostHog | Co wiemy | Werdykt |
|---|---|---|---|
| **challenges / interests** (krok 1) | `onboarding_step_completed` step_name=challenges — **91 userów** (94% wchodzących); wybrane wartości NIE zbierane | krok przechodzi prawie każdy | **Wypełniane** (completion); treść niemierzalna |
| **intensity** (krok 2) | step completed **87**; wartość nie zbierana | — | Wypełniane (completion) |
| **journey free-text** (krok 3) | step completed **84**; **treść free-text NIE zbierana** (jedyny event z tekstem to lead_source_other, 1 user) | krok przechodzi większość, ale czy TEKST wpisany — nieznane | **Krok zaliczony; realny fill free-textu UNKNOWN** (prawdopodobnie wysoki skip) |
| modality / schedule / companion (4/5/6) | step completed 82 / 81 / **71**; wartości nie zbierane | — | Wypełniane (completion) |
| **age + gender** (profil) | w `profile_updated.updated_fields` dla **93** (7-field) + 90 (stary 4-field); `gender` na ~kilku personach | prawdopodobnie wymagane pickery | **Zbierane na poziomie zapisu** (~wszyscy profilujący) |
| **age_band** (Wave 1, profil) | w updated_fields dla **93** (od 05-29); `age_band` na ~kilku personach | tylko nowy flow | **Zbierane (write-level)**; VALUE-fill → Postgres |
| **currently_in_therapy** (Wave 3, Art.9, consent-gated) | w updated_fields dla 93; **NIE na personach (by design)**; brak eventu zgody | write zależy od zgody ARTICLE9_HEALTH | **Zbierane TYLKO jeśli zgoda**; value + consent-rate → **Postgres** |
| **lead_source** (Wave 4) | jawny wybór `onboarding_lead_source_selected` = **6 userów**; krok osiąga 7; w payloadzie 93 (null default); **NIE na personach (by design)** | UTM łapie pozyskanie automatycznie | **NIE wypełniane przez userów w aplikacji** (~6) |
| **withdrawal** (Art.9 cofnięcie zgody) | **brak jakiegokolwiek eventu** | — | **Niemierzalne w PostHog** (tylko `consent_records`) |

---

## Lejek kroków onboardingu (distinct users, ~40d)

| # | step_name | viewed (users) | completed (users) | step→step retention |
|--:|---|--:|--:|--:|
| 0 | legal_gate | 106 | 97 | — |
| 1 | challenges | 97 | 91 | 94% |
| 2 | intensity | 91 | 87 | 96% |
| 3 | journey | 87 | 84 | 97% |
| 4 | modality | 84 | 82 | 98% |
| 5 | schedule | 82 | 81 | 99% |
| 6 | companion | 81 | 71 | 88% |
| 7 | **lead_source** | **7** | **7** | **10%** ⬅ urwisko |

`onboarding_completed` ≈ 71 userów (45d). **Czytanie**: core onboarding (0–6) jest zdrowy — drop step-po-stepie 1–12%. Jedyne urwisko to `lead_source` (krok 7): osiąga go tylko 7/71 finiszerów. Pole żyje od 05-29 (nie jest świeże), więc to nie „za wcześnie" — to strukturalny brak zasięgu/skip tego kroku.

---

## Sygnał vs Szum vs Gap

**Sygnał (wiarygodne):**
- `lead_source` zbierany od userów w aplikacji = ~6 osób → cel niezrealizowany (High confidence — 3 niezależne eventy zgodne: step 7, selected 6, other 1).
- Core onboarding (challenges/intensity/journey-step/modality/schedule/companion) kończony przez 67–86% wchodzących → pola „przechodzą".
- `profile_updated` 7-field payload żyje od 05-29 i odpala dla ~93 userów → pipeline zapisu działa, dane idą do bazy.

**Szum (nie nadinterpretować):**
- Liczby personowe z PostHog (`total_persons` zwracało raz 102, raz ~1469 zależnie od metody) — **tabela `persons` w tym API jest niewiarygodna ilościowo**; nie liczyć z niej fill-rate. Wiarygodne = `JSONExtractKeysAndValues`/`profile_updated`.
- before/after 27.06 dla tych pól (10 ev po) — pola sprzed update'u, brak sygnału.

**Gap instrumentacji (ważne — część jest BY DESIGN/prywatność, nie bug):**
- `currently_in_therapy` & `lead_source` **celowo nie wysyłane do PostHog** (Art.9 / re-identyfikacja) → value-fill niemierzalny w PostHog. ⇒ definitywna odpowiedź TYLKO z Postgres.
- `therapy_context_updated.updated_section` = null (808/808) → nie wiadomo która sekcja.
- Wartości wyborów (challenges/intensity/modality/schedule/companion) niezbierane → brak rozkładów.
- journey free-text fill-rate niemierzalny (treść niezbierana — słusznie).
- Brak eventu zgody Art.9 / withdrawal → consent & withdrawal rate niemierzalne w PostHog.
- **Drobny privacy-smell**: `onboarding_lead_source_other_text` niesie `first_50_chars` realnego tekstu (1 user) — łamie zasadę „żadnego free-textu" z planu; niska wrażliwość („skąd o nas wiesz"), ale do usunięcia/zhashowania.

---

## Rekomendacje (priorytet = impact × confidence × effort)

1. **Rozstrzygnij value-fill jednym read-only SELECT na Postgres** (definitywna prawda, której PostHog nie da). Owner: growth-analyst (gdy dostępny sterownik) / `backend-api`. Zapytanie:
   ```sql
   SELECT count(*) AS profiles,
          count(age_band)             AS age_band_filled,
          count(currently_in_therapy) AS cit_filled,
          count(lead_source)          AS lead_source_filled,
          count(gender)               AS gender_filled,
          count(age)                  AS age_filled
   FROM user_profile;
   -- + consent: SELECT consent_type, count(*) FILTER (WHERE withdrawn_at IS NULL) AS active,
   --            count(*) FILTER (WHERE withdrawn_at IS NOT NULL) AS withdrawn
   --     FROM consent_records WHERE consent_type IN ('ARTICLE9_HEALTH','PROFILING') GROUP BY 1;
   ```
   Miara sukcesu celu „więcej danych": `cit_filled/profiles` i `lead_source_filled/profiles` — jeśli niskie, cel niezrealizowany mimo że pole „jest w formularzu".
2. **Napraw zasięg kroku `lead_source` albo go usuń.** Skoro UTM/install-referrer już łapie pozyskanie automatycznie (utm_*/fbclid/gclid na personach), in-app `lead_source` (6 userów) jest redundantny i prawie martwy. Decyzja: albo przesunąć krok wyżej/uczynić obowiązkowym (jeśli potrzebny self-reported channel), albo wyciąć i polegać na UTM. Owner: `ui-ux-designer` (audyt pozycji kroku) → `flutter-mobile`. Miara: `lead_source_selected` userzy / onboarding_completed z 10% → cel.
3. **Dodaj measurable-bez-treści sygnał wypełnienia pól** (privacy-safe): emit `onboarding_field_filled` z `field_name` + `filled:boolean` (BEZ wartości) dla age_band/gender/currently_in_therapy/journey/lead_source. Owner: `flutter-mobile`. Miara: per-field fill-rate widoczny w PostHog bez łamania prywatności i bez Postgres.
4. **Wypełnij `therapy_context_updated.updated_section`** (background/goals/focus_areas) — dziś null. Owner: `backend-api`/`data-analytics` (`users.py`). Miara: 0 null `updated_section`.
5. **Dodaj boolean event zgody Art.9** (`article9_consent_changed` z `granted:bool`, `source`) — bez treści. Owner: `flutter-mobile`+`backend-api`. Miara: consent-grant i withdrawal rate mierzalne; pozwala policzyć ile userów w ogóle MOŻE wypełnić `currently_in_therapy`.
6. **Usuń/zhashuj `first_50_chars`** z `onboarding_lead_source_other_text`. Owner: `flutter-mobile`. Miara: 0 free-textu w properties (privacy audit clean).

---

## Data Caveats & Confidence
- **PostHog mierzy „pole było w zapisie", nie „wartość niepusta".** Dla pól opcjonalnych (currently_in_therapy, lead_source) to różnica krytyczna → Postgres jest rozstrzygający; tu niewykonany (brak sterownika PG: psycopg2/asyncpg/pg8000 nieobecne; SQLAlchemy 2.0.47 jest, ale bez DBAPI).
- **`persons` table count niewiarygodny** w tym query API (różne wyniki różnymi metodami). Fill-rate liczony z `profile_updated.updated_fields` + `JSONHas`/key-extraction, nie z `properties.X != ''` (ten predykat zwraca true dla brakujących kluczy — zweryfikowane, daje fałszywe 100%).
- **Small-n**: ~70–120 userów w onboardingu w oknie; wszystko kierunkowe.
- **Pola sprzed update'u** (Wave 1/3/4 ~05-06…05-29) → before/after 27.06 nieinformatywny dla tego pytania.
- **By-design ≠ bug**: brak currently_in_therapy/lead_source w PostHog jest intencjonalny (Art.9 consent, re-identyfikacja) — komentarze w `models.py`.

## Appendix — kluczowe zapytania (HogQL, read-only)
```sql
-- Kroki: viewed vs completed po step_name/index (40d)
SELECT event, properties.step_index AS i, properties.step_name AS s,
       count() AS cnt, count(DISTINCT person_id) AS users
FROM events WHERE timestamp >= now()-INTERVAL 40 DAY
  AND event IN ('onboarding_step_viewed','onboarding_step_completed')
GROUP BY event,i,s ORDER BY i,event;

-- Payload zapisu profilu: które pola, kiedy, ilu userów
SELECT properties.updated_fields AS f, min(timestamp) first, max(timestamp) last,
       countIf(timestamp<toDateTime('2026-06-27 00:00:00')) before, count(DISTINCT person_id) users
FROM events WHERE event='profile_updated' AND timestamp>=now()-INTERVAL 60 DAY GROUP BY f;

-- lead_source: jawny wybór vs free-text
SELECT event, count() cnt, count(DISTINCT person_id) users, min(timestamp) first, max(timestamp) last
FROM events WHERE timestamp>=now()-INTERVAL 45 DAY AND event LIKE '%lead_source%' GROUP BY event;

-- Co ląduje na personach (wiarygodnie): JSONExtractKeysAndValues, NIE properties.x!=''
SELECT key, count() FROM (SELECT JSONExtractKeysAndValues(properties,'String') kv FROM persons LIMIT 600)
ARRAY JOIN (kv).1 AS key, (kv).2 AS value WHERE key NOT LIKE '$%' AND value!='' GROUP BY key ORDER BY 2 DESC;

-- therapy_context_updated.updated_section (=null wszędzie)
SELECT properties.updated_section AS sec, count() FROM events
WHERE event='therapy_context_updated' AND timestamp>=now()-INTERVAL 40 DAY GROUP BY sec;
```

---

## ⚑ DEFINITYWNE POTWIERDZENIE Z PROD POSTGRES (2026-06-29)

Read-only SELECT odpalony na prod (przez jednorazowy dyno Heroku — lokalna maszyna nie rozwiązuje hosta Azure DB). To rozstrzyga to, czego PostHog nie mógł: czy WARTOŚCI są niepuste.

**`user_profile` — fill-count (n = 1718 profili all-time):**

| Pole | Niepuste | % wszystkich profili | Status |
|---|---:|---:|---|
| `gender` | **1336** | 77.8% | ✅ wypełniane (ale to pole LEGACY, nie z ostatnich dodatków) |
| `age` | 17 | 1.0% | ❌ prawie puste |
| `age_band` (Wave 1) | **3** | 0.17% | ❌ martwe |
| `currently_in_therapy` (Wave 3, Art.9) | **0** | 0.0% | ❌ ZERO — nikt |
| `lead_source` (Wave 4) | **5** | 0.29% | ❌ martwe (zgodne z PostHog ~6) |

Rozkłady: `lead_source` → friend 2 / social_media 2 / other 1 (reszta 1713 null). `age_band` → 25-34: 2, 18-24: 1. `currently_in_therapy` → wszystkie 1718 null.

**`consent_records`:** `ARTICLE9_HEALTH` = 9 aktywnych / 2 wycofane / 11 total; `PROFILING` = 1 / 0 / 1.

**Interpretacja (rozstrzygająca):**
- **Cel „zbierać więcej danych o userze" NIE jest realizowany.** Wszystkie pola dodane w ostatnich falach (age_band, currently_in_therapy, lead_source, age) są w prod praktycznie puste (0–17 na 1718).
- **Smoking gun — `age_band`**: PostHog pokazywał `age_band` w payloadzie `profile_updated` dla ~93 userów, a w bazie niepuste = **3**. To potwierdza gap, który zgłosił PostHog-raport: **klucz jest w zapisie, ale wartość przychodzi null**. To sygnał BUGA (input nie bindowany / nie persystowany), nie tylko „userzy pomijają".
- **`currently_in_therapy` = 0 mimo 9 aktywnych zgód ARTICLE9_HEALTH** — userzy wyrażają zgodę na dane zdrowotne, ale status terapii nigdy nie zostaje zapisany. Drugi sygnał buga/skipu.
- **Caveat denominatora:** 1718 to populacja all-time; większość profili powstała PRZED dodaniem pól (~2026-05-29), więc null dla nowych pól jest po części „z definicji". Uczciwy mianownik to świeże rejestracje (~93 z payloadem 7-pól). Ale nawet względem tego mianownika liczby 0/3/5 = bliskie zera ⇒ wniosek się trzyma: **realna kolekcja tych pól ≈ 0**.
- **`gender` (77.8%)** to jedyne dobrze wypełnione pole, bo istnieje od dawna (legacy) — nie należy do „dodatkowych danych, które dodaliśmy".

**Następny krok (rekomendacja):** zdiagnozować, czemu `age_band`/`currently_in_therapy` mają klucz w payloadzie, a wartość null — to różnica między „formularz jest" a „dane lądują". Kandydat na buga w warstwie zapisu profilu (FE binding lub BE persist). Patrz [[project_onboarding_extra_fields_unfilled_2026_06_29]].
