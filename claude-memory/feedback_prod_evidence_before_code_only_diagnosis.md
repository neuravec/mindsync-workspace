---
name: feedback-prod-evidence-before-code-only-diagnosis
description: Przy objawie zgłoszonym z produkcji nie zamykaj diagnozy na podstawie samego kodu - najpierw dowód z proda
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b135de76-b7fb-4f2d-b294-9ab7c227a0a4
  modified: 2026-08-20T10:49:11.570Z
---

Przy objawie zgłoszonym z produkcji ("X nie działa na urządzeniu") **równolegle z analizą kodu odpal `database-administrator` po dowód z proda**, i nie prezentuj wniosku z samego kodu jako rozstrzygnięcia.

**Why:** 2026-08-20, "weekly summary wisi na Generating". Agent analizujący wyłącznie kod zbudował spójną, szczegółową i całkowicie błędną historię: że to stary build klienta, bo backendowy fix v542 dopiero co odsłonił latentny bug FE z cichym poddaniem się po 71 s. Historia była wewnętrznie logiczna i miała poparcie w komentarzach w kodzie. Dane z proda pokazały co innego: job **nigdy nie został pobrany z kolejki** (jeden worker RQ, ~2000 zaległych jobów po pierwszej udanej masówce), a sweep ubił go po 22 minutach. Zdążyłem przekazać operatorowi błędną diagnozę i poprosić go o numer builda, zanim przyszły dane z proda - czyli wysłałem go w ślepy zaułek.

**How to apply:** Objaw z proda = spawnuj `database-administrator` (stan DB, `heroku ps`, logi) RÓWNOLEGLE z agentem od kodu, od razu, nie po. Zanim powiesz operatorowi "to prawdopodobnie X", sprawdź, czy X opiera się na obserwacji z produkcji, czy tylko na wnioskowaniu z kodu - i jeśli to drugie, powiedz to wprost albo poczekaj. Agent bez dostępu do proda nie może odróżnić "job padł" od "job nigdy nie wystartował". Uwaga na retencję logów Heroku: bywa ~1 h (chatter workera wypycha linie web dyno), więc brak błędu w logach NIE jest dowodem, że błędu nie było.

Patrz też: [[project-msv34-fix1-batch-2026-08-20]], [[feedback_no_live_api_experiments]]
