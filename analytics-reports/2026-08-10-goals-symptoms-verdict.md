# B4 – Cele i Symptomy: wypromować czy wygasić

Data: 2026-08-10. Autor: ui-ux-designer (audyt read-only, kod + PostHog). Zakres: zadanie B4 z `2026-08-10-posthog-audit-taskplan.md`.

## Werdykt w skrócie

| Obszar | Werdykt | Uzasadnienie w jednym zdaniu |
|---|---|---|
| **Cele (Goals)** | **WYGASIĆ** (miękko – bez utraty danych) | Mimo dedykowanej kampanii push kierującej nowych userów wprost do ekranu tworzenia celu, konwersja jest śladowa (16 osób w ~3,5 miesiąca) i status celów przestał się zmieniać całkowicie od 23.07 – to nie jest problem odkrywalności, tylko brak potrzeby. |
| **Symptomy (Symptoms)** | **WYPROMOWAĆ (lekko)** – dokończyć, nie budować od nowa | Karta jest już najlepiej wypromowanym miejscem w apce (3. karta na Home, zero dodatkowych tapnięć) i jako jedyna z dwóch ma ciągłe, żywe użycie (zdarzenie odpaliło dziś), ale połowa zbudowanej funkcji (sugestie objawów) nie ma żadnego UI od redesignu Stats – to tania (~1–2h) dokończka, nie nowy projekt. |

Poniżej pełne dowody per obszar.

---

## 1. Cele (Goals)

### 1.1 Odkrywalność w kodzie

Ścieżka do celu z ekranu głównego: **bottom-nav → zakładka "Workspace" (4. z 5 ikon, etykieta `nav_workspace`) → scroll w dół do modułu 5 z 6** (`lib/screens/workspace/workspace_screen.dart`, kolejność: Agenda → Wątki tematyczne → Do zrobienia → Wątki → Realizacje → **Cele** → Relacja terapeutyczna). To 1 tap + spory scroll, nie 1 tap + widoczność bez przewijania.

Dodatkowo sama zakładka Workspace nie jest domyślną (Home jest domyślna) i ma świeże zdarzenie `workspace_opened` (żyje od 2026-08-04) pokazujące, że w ostatnich 14 dniach otworzyło ją tylko 18 osób – przy 91 aktywnych userach appki w tym samym oknie to ok. 20%. Sam fakt dotarcia do zakładki, w której żyją Cele, jest więc już wąskim gardłem.

Nowym userom funkcja JEST komunikowana – i to aktywnie: `MindSync/app/services/moments/account_setup_nudge_generator.py` (CS-07, wdrożone 2026-07-24) wysyła **do 4 pushy** w ciągu pierwszych 96h od rejestracji, każdy z deep-linkiem `/main-page/tab/workspace?section=goals&setup=true`, który po stronie klienta (`ms_routes.dart` + `goals_module_section.dart:openAddGoalSheet`) otwiera od razu arkusz dodawania celu. Seria zatrzymuje się, jak tylko user ma choćby jeden `UserGoal` w dowolnym stanie. To znaczy: **odkrywalność nie jest tu wąskim gardłem tak jak w innych obszarach audytu (np. therapy_schedule) – jest wręcz aktywnie forsowana z backendu.**

### 1.2 Dane (pełna historia, nie tylko 14d)

Zapytania HogQL przez `scripts/posthog_query.py`, projekt 141170 EU. Uwaga metodologiczna: `goal_created`, `goal_status_changed` i zdarzenia symptomów są emitowane **serwerowo** (`posthog_capture` w endpointach FastAPI, `$lib=posthog-python`), więc filtr `$lib='posthog-flutter'` z briefu ich wycina do zera – nie ma to sensu dla tych zdarzeń (klient nigdy nie ustawia tej właściwości dla eventów wysyłanych z backendu). Poniższe liczby są bez tego filtra; nie da się w HogQL odsiać testflight/emulator dla eventów bez klienckich property, więc traktuj to jako lekką górną granicę.

| Event | Zdarzenia (całość) | Unikalne osoby (całość) | Pierwsze wystąpienie | Ostatnie wystąpienie |
|---|---|---|---|---|
| `goal_created` | 29 | **16** | 2026-05-01 | 2026-08-07 |
| `goal_status_changed` | 21 | **6** | 2026-04-28 | **2026-07-23** (martwe od 18 dni) |

Dla porównania: `total_app_people_alltime` (dowolny event kliencki, `$lib=posthog-flutter`) = **854 osoby**. 16 osób, które kiedykolwiek stworzyły cel, to **1,9% wszystkich userów appki w całej historii**.

Trend tygodniowy `goal_created`: 1–4 zdarzenia/tydzień, z lukami (żadnego zdarzenia w kilku tygodniach), **zero w ostatnim pełnym tygodniu (08-09)**. Żadnego wybicia po starcie kampanii push 24.07 – jeśli push faktycznie dociera (patrz zastrzeżenie niżej), to i tak nie konwertuje.

### 1.3 Sanity-check techniczny

Nie znaleziono wzorca 422 jak w `therapy_schedule`. Endpoint `PUT /api/v1/goals/{id}/status` (`goals.py:440`) waliduje poprawnie i emituje `goal_status_changed` w bloku `try/except: pass` (błąd PostHog nigdy nie zablokuje zapisu – dobry wzorzec). Zapis samego celu (`POST /api/v1/goals/`) też wygląda poprawnie po stronie klienta (`goal_manager.dart:createGoal`).

Znaleziono za to **martwy kod, który pokazuje, że nawet zespół produktowy przestał kończyć pracę nad tym obszarem**:
- `GoalTrackingCubit.trackGoalViewed()` (`goal_tracking_cubit.dart:32`) – zdefiniowana metoda emisji `goal_viewed`, **zero wywołań w całym `lib/`**. Nigdy nie podpięta pod żaden tap.
- `GoalManager.getSuggestions()` (`goal_manager.dart:97`, `GET /api/v1/goals/suggestions` – sugestie celu na podstawie śledzonych symptomów) – model, DTO i endpoint istnieją, **żaden widget go nie wywołuje**. Cały most Symptomy→Cele, który mógłby podnosić konwersję, jest zbudowany po stronie API i nieużywany.
- Nie udało się w tej sesji potwierdzić z PostHog, czy `ACCOUNT_SETUP_NUDGE` faktycznie dociera jako push (property `moment_type` nie jest wypełniana na `moment.opened`/`moment.acted`, więc bez joina do prod DB nie da się rozbić po typie momentu). **Zalecenie do backend-api/data-analytics**: krótka weryfikacja w prod DB (tabela `notification_moment`, `moment_type='ACCOUNT_SETUP_NUDGE'`), żeby odróżnić "push wysłany, zignorowany" od "push nigdy nie wyszedł" – wynik nie zmienia werdyktu (patrz 1.4), ale wpływa na to, czy warto jeszcze próbować promować kanałem push przed wygaszeniem UI.

### 1.4 Werdykt: WYGASIĆ (miękko)

Uzasadnienie:
1. **To nie jest problem odkrywalności.** Feature ma dedykowaną, 4-dotknięciową kampanię push wskazującą wprost na arkusz tworzenia celu – a mimo to konwersja jest śladowa i płaska (16 osób / 854 w całej historii, zero w ostatnim tygodniu).
2. **Status celów jest martwy od 18 dni** (`goal_status_changed` = 0 od 23.07) – nawet ci nieliczni, którzy stworzyli cel, przestali go finalizować (oznaczać jako osiągnięty/porzucony).
3. **Koszt utrzymania jest nieproporcjonalny do ruchu.** Feature ma pełny stos: model + migracje, AI-generowaną narrację (regenerowaną przy każdym create/edit/status-change – koszt OpenAI per akcja), RAG/embeddingi, dziennik narracji, archiwum, reorder, share, polling po utworzeniu. Był re-inwestowany w kolejnych batchach (Fix.1 CS-07 przeniesienie do Workspace, Fix.1 CS-20/21/22 refresh/archiwum/przycisk dodawania) bez odpowiadającego wzrostu użycia.
4. Nawet własne, już zbudowane rozszerzenia (`trackGoalViewed`, sugestie celu z symptomów) nigdy nie zostały dokończone – sygnał, że priorytet dla tego obszaru już spadł do zera w praktyce, tylko formalnie nie została podjęta decyzja.

**Co zrobić (spec dla flutter-mobile, gdy operator zatwierdzi):**
- Usunąć z `GoalsModuleSection` (`goals_module_section.dart`) wejście solicitujące NOWE tworzenie celu: przycisk `WorkspaceAddGhostButton` ("+ Dodaj cel") oraz pusty stan `stats_setGoals` zachęcający do założenia pierwszego celu. **Nie usuwać** renderowania istniejących aktywnych celów – 16 osób, które już mają cel, nie powinno dostać nagle pustki (żadnej utraty danych/funkcji dla obecnych właścicieli celów).
- Wyłączyć `AccountSetupNudgeGenerator` po stronie backend-api (właściciel `app/tasks/gamification.py`/`app/services/moments/` wg mapy własności) – przestać zapraszać nowych userów do funkcji, którą wygaszamy.
- Wycofać deep-link `?setup=true` / akcję `goal_setup` w `ms_routes.dart` i `main_nav_cubit.dart` razem z powyższym (albo zostawić jako no-op, żeby stare, już wysłane powiadomienia nie failowały – decyzja integration-devops).
- Analytics (przy okazji C1): usunąć nigdy-niewywoływaną `trackGoalViewed`/`goal_viewed`; `goal_created`/`goal_status_changed` zostają jako telemetria dla istniejących właścicieli celów, nie trzeba ich wycinać z kodu.
- **Nie kasować** danych: tabela celów, `GoalDetailScreen` (deep-link `/workspace/goals/:id`) i historia narracji zostają nietknięte – to tylko wygaszenie kanału POZYSKANIA nowych celów, nie danych.

---

## 2. Symptomy (Symptoms)

### 2.1 Odkrywalność w kodzie

Symptomy żyją jako `UnifiedSymptomModule` (`lib/screens/stats_tab/widgets/unified_symptom_module.dart`) osadzony w karcie `MoodTrendCard` na **zakładce Home (domyślna, index 0)**, jako **3. karta od góry** (`mainTabDefaultWidgetOrder = ['next_session', 'homework_today', 'mood_trend', ...]`, `main_tab_cubit.dart:34`) – zaraz po karcie następnej sesji i "co dziś". Nagłówek na ekranie to wprost **"Trend objawów · 7 dni"**. Zero dodatkowych tapnięć od uruchomienia appki; to najlepiej wypromowane miejsce, jakie w ogóle mogłoby dostać.

Jedyne ryzyko: karta jest w `mainTabDefaultWidgetOrder`, czyli **user może ją ukryć** w trybie edycji layoutu Home (`_EditModeBody`) – to jego świadomy wybór, nie problem produktu.

Zarządzanie symptomami (dodawanie/usuwanie/zmiana widoczności) jest też dostępne w Ustawieniach (`settings/widgets/symptoms_section.dart`), ale tam znaleziono **realny bug UX**: tekst `settings_manageInStats` = *"Zarządzaj śledzeniem w zakładce Statystyki"* (`app_pl.arb:415`) odsyła do **zakładki, która nie istnieje od czasu redesignu Workspace** (`ms_routes.dart` komentarz: "tab index 3 used to be Stats... Index 3 is now Workspace, not Stats"). To myląca, martwa wskazówka nawigacyjna – niska szkodliwość (Settings i tak pozwala zarządzać na miejscu), ale warto poprawić przy okazji (patrz sekcja 3).

### 2.2 Dane (pełna historia)

| Event | Zdarzenia (całość) | Unikalne osoby (całość) | Pierwsze wystąpienie | Ostatnie wystąpienie |
|---|---|---|---|---|
| `symptom_scored` | **445** | **36** | 2026-04-27 | **2026-08-10 (dziś)** |
| `symptom_created` | 38 | 16 | 2026-04-30 | 2026-08-10 (dziś) |
| `symptom_archived` | 9 | 4 | 2026-05-23 | 2026-08-07 |
| `symptom_suggestion_accepted` | 7 | 4 | 2026-04-27 | **2026-05-18 (martwe od 84 dni)** |
| `symptom_suggestion_dismissed` | 1 | 1 | 2026-05-13 | **2026-05-13 (martwe od 89 dni)** |

`symptom_scored` ma **ciągłą, cotygodniową obecność od kwietnia do dziś** (1–6 unikalnych osób/tydzień, żaden tydzień bez aktywności) – jedyny z ośmiu ocenianych w tym zadaniu eventów (cele+symptomy), który wciąż żyje w dniu audytu. 36 osób na 854 w całej historii to wciąż mało w liczbach bezwzględnych (4,2%), ale trzeba to zestawić z tym, że ocena objawu wymaga świadomego wysiłku (przesunięcie suwaka przy każdym symptomie), nie samego dotarcia na ekran – i mimo to trzyma się stabilnie bez żadnej dedykowanej kampanii push (w przeciwieństwie do Celów, gdzie promocja jest, a konwersji nie ma).

### 2.3 Sanity-check techniczny – kluczowe znalezisko

`symptom_suggestion_accepted`/`_dismissed` ucichły w połowie maja nie przez błąd typu 422, tylko przez **martwe UI po redesignie Stats**:

- `SymptomTrackingCubit` (`symptom_tracking_cubit.dart`) ma **w pełni zaimplementowaną** logikę: `pendingSuggestions` w stanie, `acceptSuggestion()`/`dismissSuggestion()` z optymistycznym update i rollbackiem na błąd, `trackSuggestionShown()`.
- **Żaden widget w całym `lib/` nie czyta `state.pendingSuggestions`** ani nie wywołuje `acceptSuggestion`/`dismissSuggestion`/`trackSuggestionShown` (potwierdzone grepem – zero trafień poza cubitem/stanem/freezed). `UnifiedSymptomModule` i `symptom_management_sheet.dart` nie mają żadnego elementu UI dla sugestii.
- Backend (`symptoms.py:394-451`, `GET/POST /symptoms/suggestions/...`) działa i emituje eventy poprawnie – **to nie backend jest martwy, tylko front nigdy nie dostał widgetu**, najpewniej ucięty przy przenosinach Stats → Main/Workspace (ten sam wzorzec co martwe sugestie celów w sekcji 1.3 – rozłączenie backend/frontend w tym samym redesignie).

To znaczy: **połowa gotowej pracy leży nieużywana za darmo** – cubit, endpoints, modele są kompletne, brakuje tylko renderowania.

### 2.4 Werdykt: WYPROMOWAĆ (lekko – dokończyć, nie budować od nowa)

Uzasadnienie:
1. Karta już zajmuje najlepsze możliwe miejsce (Home, pozycja 3, zero tapnięć) i jest jedynym z badanych obszarów z żywym, ciągłym użyciem sięgającym dnia dzisiejszego.
2. Bariera nie jest w dotarciu, tylko w wysiłku ocenienia symptomu ręcznie (suwak) – gotowe sugestie AI (`symptom_suggestion_*`) to dokładnie mechanizm obniżający ten wysiłek (jeden tap zamiast przesuwania suwaka), i jest w 90% zbudowany.
3. Koszt dokończenia jest niski: brakuje tylko widgetu renderującego `pendingSuggestions` – logika stanu, wywołania API i tracking już istnieją.

**Spec dla flutter-mobile (konkretne miejsce wejścia):**
- Nowy mały widget `_SymptomSuggestionsRow` (lub podobny) w `unified_symptom_module.dart`, renderowany **wewnątrz białej karty, nad pierwszym wierszem symptomu** (ten sam slot, w którym dziś siedzi `header` z AI-podsumowaniem `MoodTrendCard` – analogiczny wzorzec do FIX.03) – widoczny tylko, gdy `state.pendingSuggestions.isNotEmpty`, żeby pusty stan nie dodawał szumu.
- Layout: 1 chip/rząd na sugestię, tekst typu *"Zauważyliśmy więcej wzmianek o zmęczeniu – dodać ocenę?"* + dwa małe przyciski: ✓ (wywołuje już istniejące `cubit.acceptSuggestion(id)`) i ✕ (`cubit.dismissSuggestion(id)`). Wywołać `cubit.trackSuggestionShown(id)` raz przy pierwszym renderze chipa (już zaimplementowana metoda, tylko niewywoływana).
- Touch target min. 48×48dp na oba przyciski (WCAG 2.5.5), kolorystyka spójna z resztą modułu (`_lagoon`/`_deepOcean`, bez czerwieni – to zgodne z zasadami mental-health UX tego projektu).
- Szacowany nakład: ~1–2h flutter-mobile (jeden nowy widget, zero zmian w cubicie/API/modelach).
- Przy okazji: poprawić `settings_manageInStats` (i odpowiedniki w innych 6 językach) – zmienić na wskazanie właściwego miejsca (np. "Zarządzaj śledzeniem na ekranie głównym") albo usunąć linię, skoro Ustawienia i tak pozwalają zarządzać bezpośrednio na miejscu.

---

## 3. Wspólne ustalenie: `$screen_name` nie jest wiarygodnym sygnałem dla żadnej zakładki

Dowód z briefu ("w top 20 $screen_name nie ma ekranów celów ani symptomów") jest prawdziwy, ale **mylący jako miara niskiego zainteresowania konkretnie tymi dwoma obszarami**. Sprawdzone w PostHog: top `$screen_name` to `mainPage` (6270/250), `splash`, `auth`, `settings`, `therapyOnboarding`, `recordSessionFlow`, `afterTherapyFlow`, `signUp`, `betweenSessionsFlow`, `healthCheckFlow`, `account`, `subscription`, `prepTherapyFlow`, `mainPageTab` (177/11), `audioChat`... **Żadna z pięciu zakładek dolnej nawigacji (Home, Timeline, Reflect, Workspace, Character) nie ma własnego `$screen_name`** – wszystkie żyją jako dzieci jednego `PageView` pod pojedynczą trasą `go_router` `/main-page` (`main_page_body.dart`), więc `PosthogObserver` (podpięty do `GoRouter`) nigdy ich nie odróżnia. To ta sama luka, która dotyczy Timeline (który i tak ma dobre użycie per inne zadania audytu) – nie jest to sygnał specyficzny dla Cele/Symptomy.

**Rekomendacja poboczna (do C1/backend-api+flutter-mobile, nie blokuje werdyktu B4):** rozważyć ręczną emisję `$screen`/custom eventu przy każdej zmianie taba w `MainNavCubit` (już są tam trigery typu `therapy_tab_opened` i nowy `workspace_opened` – wystarczy dodać brakujące dla pozostałych tabów), żeby przyszłe audyty tego typu miały twardszy sygnał niż wnioskowanie z eventów domenowych.

---

## Podsumowanie dla operatora

- **Cele: WYGASIĆ.** Odkrywalność nie jest winna – jest aktywna kampania push, a konwersja i tak jest płaska i status celów jest martwy od 18 dni. Usunąć kanał pozyskania nowych celów (przycisk dodawania + push-nudge), zostawić istniejących 16 właścicieli celów bez zmian.
- **Symptomy: WYPROMOWAĆ, ale tanio.** Nie przenosić, nie przebudowywać – dokończyć już zbudowaną (backend+cubit) funkcję sugestii jednym nowym widgetem w `unified_symptom_module.dart` (~1-2h pracy flutter-mobile), plus poprawić martwy odnośnik do "zakładki Statystyki" w Ustawieniach.
- Otwarte pytanie do backend-api/data-analytics (nie blokuje werdyktu): potwierdzić w prod DB, czy `ACCOUNT_SETUP_NUDGE` faktycznie wysyła pushe (tabela `notification_moment`), żeby mieć pewność, że niska konwersja Celów to "zignorowany push", a nie "push, który nigdy nie wyszedł" – wynik nie zmienia decyzji o wygaszeniu UI, ale wpływa na to, czy backend-api powinien też wyłączyć generator, czy zostawić go jako martwy kod niskiego ryzyka.

Ścieżka raportu: `C:\Users\mikol\Notebooks\MindSync\Heroku\analytics-reports\2026-08-10-goals-symptoms-verdict.md`
