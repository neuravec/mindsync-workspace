---
name: project-msv322-notifications-batch-2026-07-24
description: "MSV3.2.2 Notifications & Settings Fix 1 — 7 itemów e2e COMMITTED (BE a918322+b76204c, FE c1e2696+4a20b19, NIE pushed); migracja ff7182a3b4c5 = HEAD; lista decyzji do veta Darka"
metadata: 
  node_type: memory
  type: project
  originSessionId: b6485ab0-4fa9-4177-97d2-f54f46bfcf22
  modified: 2026-07-24T19:03:26.373Z
---

# MSV3.2.2 Notifications & Settings Fix 1 (spec 23-24.07.2026, impl. 2026-07-24)

Spec: `Business_requirements/MS_3/v3.22/MSV3.2.2.md` (7 itemów; CS-06 NIE ma własnej sekcji w pliku — zdefiniowany przez Summary: "whole Quiet hours section leave the app" + referencje w CS-01/CS-02).

## Status: COMMITTED lokalnie, NIE pushed
- **BE `main`**: `a918322` (cały batch) + `b76204c` (fix DST po cross-review). Migracja **`ff7182a3b4c5` = nowy HEAD** (down_revision ee6f7182a3b4; 9 etykiet `moment_type_enum` przez ALTER TYPE ADD VALUE IF NOT EXISTS, autocommit, dialect-guarded, idempotentna).
- **FE `dev`**: `c1e2696` (CS-01 deep linki) + `4a20b19` (CS-02/04/05/06 ekran ustawień).
- QA: pytest 21 fail/4797 pass, flutter 1436 pass/30 fail = baseline, 0 nowych. Reviews: data-analytics GO (High DST naprawiony w b76204c), integration-devops GO (kontrakt 6/6).

## Architektura
- **Toggle model**: `notification_toggles` — 13 booli w istniejącym blobie JSON `notification_preferences` (BEZ nowej kolumny). Klucze w kolejności listy: therapy_appointment, add_therapy_date, after_therapy, prepare_for_therapy, between_sessions, record_session, homework, mood_trends, reflect, goals, therapy_relationship, weekly_summary, monthly_summary. Lazy-migracja z `notification_interests` przy odczycie; PUT starych interests mapuje na togle (WEEKLY_SUMMARIES→oba summary); stare klucze (interests, dnd_*) nadal zwracane/przyjmowane (additive-only).
- **Orchestrator Pass 3 "deterministic"** (`register_deterministic()`, per-generator `toggle_key`): bez scoringu/slotów/daily-cap/DND. Pass 1 zostały tylko MOOD_DIP_ALERT + RE_ENGAGEMENT.
- Wiersze event-anchored: hooki w `app/services/moment_hooks.py` (night rule 21:00–08:00→08:00 lokalnie, DST-safe przez `tz.localize(naive)` wg wzorca time_utils) wołane z weekly_therapy_summary.py / monthly_therapy_audit.py / goal_narrative.py (tylko weekly_scheduled). Dedup_key = DB-enforced idempotencja.
- **Routes w JEDNYM module**: `app/services/notification_routes.py` (MOMENT_ROUTES 14 wpisów + `DAY_PRECISION_SEND_HOUR=18` + `route_for()`). FCM data: `{type: notification_moment, moment_id, route=deep_link_route}` — route niesie REALNY cel (koniec indirection /moment/{id}).
- **FE scroll-to-section (greenfield)**: `lib/utils/section_anchor.dart` — `SectionAnchor(id)` + `SectionAnchorRegistry.scrollTo` (poll do 3s na async content); `MainNavCubit.selectTab(scrollTo/action)` + bezpośrednie listenery notifierów w initState (Cubit deduplikuje emity — sam BlocListener nie odpali na tym samym tabie); `?section=/new=/setup=` parsowane w ms_routes helperami. Nowy route `/therapy/weekly-summary/:id`.
- CS-04: usunięte generatory pattern_insight, streak_celebration + (decyzja lead, flagged) session_morning_of i daily_check_in. Enum members zostają (historia). In-app insight detectors NIEtknięte (osobny feature).
- CS-07: ACCOUNT_SETUP_NUDGE t+24/48/72/96h od User.created_at, tylko gdy brak UserGoal, dedup setup_nudge_1..4, bez toggla (respektuje master), route goals&setup=true.
- Deleted FE: chipy "What interests you?", Quiet hours UI (updateDndHours, dnd state), 14 kluczy ARB; dodane 28 kluczy (header+13×title/subtext, 7 języków). Banner OS-warning na MsColors.alert[50/200/700/800/900].
- Audyt CS-01: `Business_requirements/MS_3/v3.22/CS01_NOTIFICATION_AUDIT.md` (poza repo git).

## Do veta / potwierdzenia Darka (przed lub tuż po deployu)
1. **RE_ENGAGEMENT** — żyje, tap → `/main-page` (generyczny). BRAK zdefiniowanego celu w spec — wymaga decyzji Darka (CS-01 "stop, list it").
2. **MOOD_DIP_ALERT** — przekierowany na `/main-page/tab/main?section=mood_trends` (dopasowanie treściowe, wymyślone przez nas — do akceptacji).
3. Usunięcie session_morning_of + daily_check_in (zastąpione wierszami 1/2/4/6 — interpretacja).
4. Wiersz 6: cron dostawy `deliver_due_moments` */15→**\*/5** + scheduling na start−8min (okno dostawy [−8,−3] zamiast literalnych 3 min).
5. Night rule rozszerzona na wiersz 10 (Goals; job leci ~04:00 UTC — bez tego push o 5 rano).
6. CS-06 backend: DND martwe dla nowych ścieżek (klucze dnd_* w API zostają, inertne).
7. periodic_summary `summary_ready` (→/main-page) — odpalane tylko zewnętrznym schedulerem, nie ruszone, w audycie.
8. Nudge CS-07 respektuje master toggle (spec mówi "always active").

## Deploy checklist
1. Push BE `main` + NATYCHMIAST `heroku run alembic upgrade head --app mindsync` (pending: aa, bb, cc, dd, ee, **ff** — wszystkie addytywne; nowe enum labels wymagane ZANIM powstanie pierwszy moment nowego typu).
2. Push FE `dev` (Codemagic → TestFlight/Play internal).
3. Znane wąskie ryzyko: stare buildy po tapie w push "Weekly summary" → domyślna strona błędu GoRoutera (jedyny nowy route; samo-gaśnie z aktualizacjami). Rekomendowany follow-up: app-wide errorBuilder w GoRouter (hardening).
4. Device-QA na iPhone+Android: tap-testy 14 anchorów cold+warm start, 13 toggli persist, banner żółty, brak Quiet hours. FE screeny Workspace/Main/Reflect nie mają widget-testów (wzorzec repo) — scroll wymaga manualnego QA.
5. Wiersze 12/13 zaczną strzelać dopiero gdy Fix4 CS-03 generuje karty (strukturalnie gwarantowane — push tylko po COMPLETED karcie).

Powiązane: [[project-msv32-fix4-batch-2026-07-24]], [[project-notification-cadence-v3-2026-07-03]], [[feedback-no-live-api-experiments]], [[project-postgres-enum-drift]]
