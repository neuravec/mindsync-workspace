---
name: project-deeplink-back-blackscreen-fix-2026-08-20
description: Fix czarnego ekranu po "wstecz" na karcie otwartej z notyfikacji (FE-only, PUSHED dev 1c34b95, 2026-08-20)
metadata:
  type: project
---

Zgłoszenie 2026-08-20: tap w notyfikację poprawnie otwiera np. podsumowanie miesięczne, ale "wstecz" na karcie daje **czarny ekran**. Miało wracać do Timeline.

**Root cause (mechanizm, nieoczywisty):** `_handleNotificationRoute()` w `main.dart` robi `router.go(route)`, a `go()` **zastępuje cały stos**. Wszystkie cele notyfikacji (`/therapy/monthly-audit/:id`, `/therapy/weekly-summary/:id`, `/therapy/prep-card/:id`, `/therapy/recording/:id`, `/health-check`, `/workspace/...`) to **top-level GoRoute'y**, więc na stosie zostaje jedna strona. `Navigator.pop()` opróżniał Navigatora = czarny ekran. Ekrany używające `context.pop()` (settings/my-therapy) zamiast tego rzucały wyjątek.

**Druga pułapka, warta zapamiętania:** przy jednostronicowym stosie `PopScope` NIE wystarcza na sprzętowy back. W go_router 14.6 `GoRouterDelegate.popRoute()` kończy na `_findCurrentNavigator() == null` i **nigdy nie woła `maybePop()`**, więc `PopScope` nie jest w ogóle konsultowany, a naciśnięcie leci do `SystemNavigator` (wyjście z apki). Trzeba przechwycić wyżej: `BackButtonListener`.

**Rozwiązanie:** nowy `lib/utils/safe_back.dart` – `msSafeBack(context, fallbackRoute:, result:)` + `msCanPop(context)`. Popuje gdy jest co popować (zwykła nawigacja in-app; `result` zachowany, bo Timeline robi `Navigator.push` i czeka na `view_source`), inaczej `go()` na fallback. Świadomie na `Navigator`, nie na go_routerowym `context.canPop()` – karty są in-app pushowane imperatywnie `MaterialPageRoute`, czego lista matchy go_routera nie widzi.

Objęte ekrany (każdy, na który notyfikacja może wejść jako root stosu): karta Timeline (fallback = zakładka Timeline `/main-page/tab/therapy`), health-check (14 X-ów), workspace thread/goal detail + agenda/todo/realizations, nagłówki settings i my-therapy. Agenda/todo/realizations/goal-detail dostały **jawny** back – automatyczny `AppBar` chowa się gdy nie ma czego popować, czyli deep-link nie miał wyjścia w ogóle.

**Status:** FE-only, **PUSHED dev `1c34b95`** (fix `08605e6` + typografia), po rebase na Codemagic bump `429d606`. Backend BEZ ZMIAN (payloady `/therapy/monthly-audit/{id}` z `notification_routes.py` były poprawne) – repo MindSync czyste i równe origin/main. Bez migracji.

Testy: 6 nowych (deep-link root → fallback, in-app → pop z resultem, sprzętowy back). `flutter analyze` bez nowych uwag. 2 czerwone testy (`record_session_appbar_close`, `debrief_capture_cubit`) to **baseline** – zweryfikowane przez stash: identyczne `+24 -2` bez moich zmian, patrz [[reference-pre-existing-test-baseline-2026-06-01]].

Device-QA warte zrobienia: tap w pusha z podsumowaniem, potem back **i** gest systemowy, na iPhone i Androidzie.
