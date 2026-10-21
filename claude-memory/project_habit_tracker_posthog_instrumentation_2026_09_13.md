---
name: project-habit-tracker-posthog-instrumentation-2026-09-13
description: "Instrumentacja PostHog dla Habit Trackera – 5 zdarzeń, kontrakt i zasada prywatności; PUSHED dev cbe89e7"
metadata: 
  node_type: memory
  type: project
  originSessionId: f2d2ea51-45eb-41a9-b25a-e5b820d1faa8
  modified: 2026-09-13T11:17:36.785Z
---

2026-09-13: **PUSHED na dev `cbe89e7`** (repo `mindsync-frontend`), build Codemagic → TestFlight. FE-only, zero zmian backendu i kontraktu API.

Powód: Habit Tracker wdrożony 2026-09-02 miał ZERO instrumentacji PostHog, a jest jedyną funkcją produktu z dzienną pętlą powrotu, czyli jedynym kandydatem na naprawę retencji (D30 = 0,8%). Patrz [[project-diagnoza-retencja-monetyzacja-2026-09-12]].

**Kontrakt 5 zdarzeń** (do weryfikacji w PostHogu po dotarciu buildu do testerów):

| Zdarzenie | Parametry |
|---|---|
| `habit_tracker_viewed` | `surface` (`card`\|`month_view`), `active_habit_count`, `is_premium` |
| `habit_created` | `habit_type`, `active_habit_count_after`, `is_premium` |
| `habit_check_toggled` | `checked`, `is_today`, `days_offset`, `habit_type` |
| `habit_deleted` | `habit_type`, `active_habit_count_after`, `habit_age_days` |
| `habit_limit_reached` | `trigger` (`ui_blocked`\|`api_403`) |

**Decyzje projektowe warte zapamiętania:**
- `habit_check_toggled` odpala się WYŁĄCZNIE po potwierdzeniu przez serwer, nigdy na optymistycznym emit. Inaczej mierzylibyśmy intencje i liczby byłyby zawyżone.
- `is_today` + `days_offset` rozdzielają realny dzienny nawyk od uzupełniania tygodnia wstecz. W surowych licznikach wyglądają identycznie, a to zupełnie inne przypadki.
- `HabitModel.type` to swobodny `String`, nie enum. `AnalyticsEvents.habitTypeForAnalytics()` mapuje nieznane wartości na `"other"` zamiast wysyłać surowy tekst użytkownika.
- Odrzucone: `habit_updated`, `habit_reordered`, `habit_month_navigated` – nie odpowiadają na żadne pytanie biznesowe; wejście w widok miesięczny pokrywa już `habit_tracker_viewed`.

**Lejek do paywalla jest kompletny:** `subscription_screen_opened.trigger_feature` JUŻ niósł `premium_gate_habits` dla obu ścieżek limitu, więc po dodaniu `habit_limit_reached` da się złożyć pełną ścieżkę od próby dodania drugiego nawyku do zakupu. Darmowy limit to 1 aktywny nawyk (`FREE_TIER_MAX_ACTIVE_HABITS`), 403 `premium_required`.

**ZASADA PRYWATNOŚCI (twarda):** nazwa nawyku NIGDY nie trafia do PostHoga – w aplikacji mental-health to dane wrażliwe najwyższej kategorii. Pilnuje tego dedykowany test, który przepuszcza 5 zdarzeń z nazwą „Take my antidepressants at 8pm" i skanuje każdy ładunek wraz z kluczami. Ten test ma łapać regresy w przyszłości, nie usuwać go.

Analityka jest exception-safe: testy z mockiem PostHog rzucającym na każde wywołanie potwierdzają, że akcje nawyków kończą się poprawnie.

**NASTĘPNY KROK:** gdy build dotrze do testerów, zweryfikować że każde z 5 zdarzeń REALNIE płynie, ZANIM policzy się z nich cokolwiek. Zero może znaczyć „nikt nie używa" albo „zdarzenie się nie wysyła", a to przeciwne decyzje. Zadanie dla `posthog-data-extractor`.
