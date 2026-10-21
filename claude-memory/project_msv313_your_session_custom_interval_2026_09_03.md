---
name: project_msv313_your_session_custom_interval_2026_09_03
description: "MSV3.13 (spec Darka nazwany MSV3.12, przemianowany bo numer zajęty) – CS-01 FIX Your Session card zacina się po After Therapy (root cause: sufit 48h w debriefMatchesSession), CS-02 DELETE custom_interval_days end-to-end; DEPLOYED 2026-09-03 Heroku v548 + migracja m313a1b2c3d4 na prodzie, FE dev 997025e → Codemagic; dowód z proda: wiersz Darka, tz 'UTC+2' nie-IANA; device-QA otwarte"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f3e4af0-4683-4679-90a3-1c668e42026b
  modified: 2026-09-03T07:27:42.559Z
---

# MSV3.13 "Your Session flow + Custom frequency cleanup" (spec Darka 02.09.2026) – status: DEPLOYED (2026-09-03), device-QA OTWARTE

Spec .docx od Darka nosił numer MSV3.12, ale MSV3.12 = Habit Tracker (wdrożony 2026-09-02), więc batch nazwany **MSV3.13** (flagged for veto). Materiały: `Business_requirements/MS_3/v3.13/` (spec .md, `STATUS.md` = tablica fal + checklist deployu + device-QA, `CS01_DIAGNOSIS.md`, `CONTRACT_REVIEW_MSV313.md` GO, `QA_REPORT_FE_MSV313.md`), `db-reports/2026-09-03-msv313-your-session-prod-evidence.md` (tylko plan zapytań, patrz blokada niżej).

## Gdzie jest kod (evidence)
- BE repo MindSync, gałąź `msv3.13` w worktree `Heroku/wt-msv313-be` (base main `f4e27e8` = prod v547): `3d4af04` CS-02 (32 pliki, migracja `m313a1b2c3d4` down_revision `m312a4b5c6d7`, idempotentny DROP COLUMN `user_preferences.custom_interval_days`), `48ffdbc` CS-01 (`_debrief_matches_session` bez sufitu 48h), `072a25b` em-dash fix w teście = HEAD. Pełna suita: 5757 pass / 14 fail = baseline (nowy baseline BE = 14, bo 7 testów walidacji custom przepisano).
- FE repo mindsync-frontend, gałąź `msv3.13` w worktree `Heroku/wt-msv313-fe` (base dev `73e5314`): `3fa50c7` CS-02 (38 plików, ARB ×7, freezed), `733444a` CS-01 (`debriefMatchesSession` + nowy test `next_session_action_late_debrief_cs01_test.dart`), `e2d827b` em-dash fix w teście = HEAD. Worktree ma 224 pliki "modified" tylko przez CRLF po build_runner – ignorować.

## Root cause CS-01 (zweryfikowany, integration-devops)
Łańcuch 7 stanów w `computeNextSessionAction` (main_tab_cubit.dart) był poprawny. Bramka `debriefMatchesSession` akceptowała debrief tylko z tego samego dnia lokalnego albo utworzony ≤48h po sesji, a `sessionDate` debriefu = `DateTime.now()` przy zapisie (debrief_capture_cubit.dart:917; przez `TherapyFlowLauncher` nie idzie żadna tożsamość sesji). After Therapy wypełniony po >48h nigdy nie „liczył się", `hasDebrief` false, karta wiecznie `debriefCta`. Istniejące testy po obu stronach certyfikowały sufit 48h jako zamierzony – dlatego przeżył MSV3.2 Fix2 i Fix3. Nowa reguła (FE i BE identyczna): ten sam dzień lokalny LUB utworzony w/po chwili sesji, bez górnej granicy; ściśle przed sesją innego dnia = brak. Konsekwencja: debrief wypełniony po tym, jak minęła już KOLEJNA sesja, liczy się dla najnowszej. `GET /therapy-tracking/session-state` = martwy kod dla klienta (0 wywołań w FE), wyrównany dla spójności. `prepCardMatchesNextSession` (lustrzane okno 48h PRZED sesją) nietknięte – potencjalny bliźniaczy bug, oflagowany.

## CS-02 semantyka
frequency=custom: next = najbliższa przyszła data z `custom_therapy_sessions`, brak = None; last = najbliższa przeszła w oknie lookback (custom = 31 dni jak dotąd). Guard `is_custom_interval_only` z CS-11 usunięty w 6 generatorach + session-state (custom bez wpisów i bez dat = `no_therapy_set`, teraz poprawnie). Pydantic `extra=ignore` → stary build wysyłający `custom_interval_days` w PUT = 200 i ignorowane (test). Parked z MSV3.11 „prep_card_auto_generate.py ta sama luka custom-interval" = bezprzedmiotowe.

## Deploy (WYKONANY 2026-09-03 na polecenie operatora "pushuj wszystko i uruchom migracje")
BE: `git push origin msv3.13:main` (ff f4e27e8..072a25b, z PowerShella) → Heroku **v548** 09:51 +0200 → snapshot read-only → `heroku run --no-tty -a mindsync "alembic upgrade head"` = m312a4b5c6d7 -> **m313a1b2c3d4 = HEAD na prodzie**; logi 0 Traceback/UndefinedColumn/H1x/5xx. FE: origin/dev odjechał o commit Codemagic (8f79cf8 "Pre-release updates"), więc merge --no-ff w ODŁĄCZONYM worktree (`git worktree add --detach … origin/dev`, `reset --hard` z `core.autocrlf=false` bo świeży checkout pokazuje 7 "dirty" plików przez CRLF) → push HEAD:dev = **997025e** → Codemagic/TestFlight. Worktree'y i gałęzie msv3.13 usunięte. Heroku CLI wymagało `heroku login` operatora (sesja wygasła; `heroku auth:whoami` jako pierwszy test).

## Dowód z proda (snapshot leada przed migracją)
`custom_interval_days` miało tylko 2 userów (obaj custom, obaj z przyszłą datą ręczną); frequency=custom łącznie 29. Wiersz Darka `<UID-1>`: custom, interwał 6, **tz `'UTC+2'` (nie-IANA)**, next_session_date `2026-09-04 18:00+00`, sesje ręczne …, 08-26 18:00 "[terapeutka]", 09-04 18:00 "[terapeutka]" → po fixie (nowy build!) karta = "Prepare" na 04.09 (<72h, stan 5 pominięty). Stary build zostanie zacięty do aktualizacji. DBA (dowód z proda): debrief Darka za 26.08 istnieje (id 3104, session_date 2026-09-02 18:23, ~7 dni po sesji) = scenariusz sufitu 48h potwierdzony; z wdrożonymi funkcjami stan = prep_cta. **POTWIERDZONY osobny bug:** `time_zone='UTC+2'` parsowane gołym `pytz.timezone()` (therapy_tracking.py:302, crud.get_therapy_schedule_with_frequency) → fallback UTC → 2h skew w next_session_date; `app/utils/time_utils.parse_timezone()` obsługuje offsety, ale nie jest tam używany → follow-up backend-api (LOW-002). 5 userów ma next_session_date >7 dni przeterminowane przy harmonogramie (self-heal tylko na GET). `heroku run python -`: `DATABASE_URL` ma schemat `postgres://` (SQLAlchemy 2 go nie przyjmuje) – używaj `from app.db.session import engine`.

Powiązane: [[project_msv311_threads_reflect_grace_batch_2026_09_02]], [[project_msv312_habit_tracker_2026_09_02]], [[reference_backend_autodeploy_on_push]], [[feedback_concurrent_session_git_hygiene]], [[feedback_agents_stop_on_background_jobs]], [[feedback_prod_evidence_before_code_only_diagnosis]].
