---
name: project-first-week-guidance-design-2026-10-07
description: "Design 07.10: tryb pierwszego tygodnia na Home (stała karta Today + plan z onboardingu), canvas BXroyzGRcFpcDKp6bhXxq9 v4, SPEC DRAFT design-specs/2026-10-07-first-week-home/; czeka na 7 decyzji operatora"
metadata:
  node_type: memory
  type: project
  originSessionId: 67eeb13c-b0a0-4799-a633-a474eb81f78c
  modified: 2026-10-11T22:05:42.009Z
---

Operator 2026-10-07 uznał onboarding, pierwszą rozmowę i ekrany subskrypcji za zamknięty flow. Po wejściu na Home nowa osoba jest zagubiona, więc zlecił /design: jak jest teraz i jak proponujemy. Potem polecił iterować, „póki nie będzie przeświadczenia, że propozycja jest idealna”.

Canvas: https://claude.ai/artifact/BXroyzGRcFpcDKp6bhXxq9 (typ Design, v4, 18 ekranów, notatki PL). Pliki robocze w scratchpadzie sesji 67eeb13c (first-week-canvas/, iteration-notes). SPEC (EN, DRAFT): design-specs/2026-10-07-first-week-home/SPEC.md. Audyt bezpieczeństwa (GO z warunkami H-1..H-4) leży w tym samym folderze: audit-security-design.md.

Iteracje:
- v1: ścieżka 7 kroków z check-inem w dniu 0. Odrzucona, bo dublowała suwaki intensywności z onboardingu.
- v2: dzień 0 bez zadania, warianty, wariant spokojny.
- v3: jawne stany kroków, karta świadoma limitów Free, wspólny szkielet B/C.
- v4: ten sam komponent dla tonu spokojnego, alternatywy z agendą Workspace, reguły dat.
- Recenzje: ui-ux-designer w 3 rundach (ostatnia: blisko, 5 drobnych poprawek, wdrożone) i security-guardian. Re-review SPEC zlecony.

Kluczowe ustalenia (dowody):
- PostHog, n=42, 01.09-06.10: powrót w dniach 1-7 to 9 z 30. 19 z 42 osób kończy onboarding między 18:00 a 3:00. W tygodniu 1 wysyłamy masę pushy bez wspólnego limitu: weekly summary 35 z 42, check-in relacji 18 (także osobom spoza terapii), monthly summary 9.
- Kod:
  - „Saved to your Timeline” i „Orca will check in later in the week” to obietnice bez pokrycia.
  - „Add a check-in” prowadzi do Workspace.
  - Strefy czasowe zapisane jako UTC+2, nie IANA.
  - Push piszą AI; nie ma Android PRIVATE; tekst push trafia do logów.
  - PUT therapy-schedule nie ma bramki Art. 9.
- Prod DB: skrypt db-reports/2026-10-07-first-week-design-aggregates.py nieuruchomiony, bo Heroku CLI jest wylogowane (operator: `heroku login`).

Projekt v4:
- Dzień 0 bez zadania. Przypomnienie w kontekście, domyślnie wyłączone.
- Warianty:
  - A: sesja w tygodniu 1.
  - B/C (prawdopodobnie większość): d1 rozmowa, d3 notatka, d4 check-in, d6 rozmowa, d7 recap.
- Wariant spokojny po kryzysie: te same karty i zdarzenia, do początku dnia 3. Flaga tylko w zaszyfrowanym Redis.
- Max 1 push dziennie ze wszystkich generatorów, z neutralną treścią.
- Kroki tygodnia 1 poza limitami Free (ledger, sufity). Od dnia 8 karta zna limity i nigdy nie prowadzi prosto w paywall.
- Pomiar: same akcje, bez właściwości kroku (Art. 9).

**Decyzje operatora 2026-10-08 (SPEC §13, wiążące):** 1 tak; 2 NIE ma zwolnienia z limitów (trial 4 dni = Premium, potem zwykłe limity Free; karta świadoma limitów od końca triala, nie od dnia 8); 3 arkusz z dnia 3 pokazuje ponownie ofertę z onboardingu (starter 2 tyg.); 4 pytanie dnia 1 zawsze z pamięci (zgoda na pamięć obejmuje całą apkę, bez prawnika i flagi), bez pierwszej rozmowy albo bez notatki pamięci: pytanie generyczne, nie z setupu; 5-7 tak; 8 (403 Art. 9 na harmonogram) najpierw policzyć. Operator zatwierdził dowiezienie do TestFlight i prodowego backendu, z raportem przed każdym pushem i migracją. Build ruszył 2026-10-08 na gałęziach `feat/first-week-home` (BE od main 0c7d275, FE od 5ec58ed z prep-card).

**Stan buildu 2026-10-08 (lead):**
- Dokumenty: `API_CONTRACT.md` (z §14.1 rozstrzygnięciami leada), `COPY.md` (287 stringów + 29 pushy), `audit-security-wp0-backend.md` w folderze specu.
- WP-0 BE (push privacy H-4 `push_copy.py`, cap 1/dzień <8 dni `push_cadence.py`, IANA tz + fixy LMT/DST, M-1 `moment_privacy.py`) WYPCHNIĘTE na origin/main 8eb8d3f (tag lokalny `wp0-be-release`), bez migracji. Pełna suita: 9 faili = baseline (identyczne na 0c7d275).
- WP-0 FE na FE `feat/first-week-home` 6777c74 (fe0a 98fe273 + fe0b 6777c74, flutter_timezone 4.1.1), NIE wypchnięte; czeka aż BE tz na prodzie.
- WP-1 BE: gałęzie fw/be1-schema (m318a1b2c3d4), fw/be1-engine, fw/be1-tone; integracja na fw/be1-int w toku. FE data layer fw/fe1-data w toku.
- Blokery operatora: `heroku login` (m317 + m318 + liczby Art. 9), decyzje A-D (oferta dnia 3 w tonie łagodnym, zdanie „second therapy session”, helpline, typ produktu startera).
- Worktree'y: `Heroku/MindSync-wt-fw-*`, `Heroku/mindsync-frontend-wt-fw-*`; agenty zapisują pamięć względem cwd, przenosić z `design-specs/**/.claude/`.

**Stan 2026-10-11 (lead):** BE `feat/first-week-home` = a021da9 (WP-1..4 scalone, pełna suita = 9 baseline, boot przed migracją OK), NIE wypchnięte; w toku fw/be5-reminder (generator FIRST_WEEK_STEP + wyciszenia tygodnia 1) i audyt security WP-1..4. FE `feat/first-week-home` = 2ea8800 (Home, karta planu, karty boczne, przypomnienie dnia 0, check-in, pytanie Orki); w toku fw/fe3-session (arkusz sesji + zgoda Art. 9) i fw/fe7-recap. Zostaje: E4 arkusz dnia 3 + fix gubionego `new_thread` przy Home -> Reflect. Decyzje A-D przyjęte domyślnie wg rekomendacji leada.
Później 11.10: BE = 874a31d (be5 przypomnienia + wyciszenia + znacznik klienta `fw:client:{uid}`, be6 poprawki audytu security; 1 test do poprawy po scaleniu: sweep recap wymaga znacznika). FE = bed441f (wszystkie ekrany + arkusz dnia 3 + fix `new_thread`). Audyt UX: B-1 + M-1..M-6, poprawki w toku (fw/fe8-ux-home, fw/fe9-ux-session, BE fw/be7-plan-fields: `today.session_date`, limity Free w rytmie planu, CTA check-in przy 0 wiadomości, drop dla prep). Znalezione przy okazji, sprzed tej pracy: niemiecki ARB z mojibake (~106 linii na dev), `navigatorKey` niepodpięty (toasty Settings po angielsku). Dla prawnika przed sklepem: COPY.md 14.8 (tekst zgody Art. 9 na terminy sesji).
**Stan końcowy 11.10 (lead):** BE gotowy do pusha = `d0d2940` na `feat/first-week-home` (worktree MindSync-wt-fw-integration; pełna suita 11041 pass / 9 baseline; security GO z warunkami x2). Push na main ZABLOKOWAŁ klasyfikator auto mode [Production Deploy], także przygotowanie gałęzi release2. Operator ma pushować sam albo dodać regułę. Druga paczka BE niescalona: `fw/be12-copy` (zawiera be10: D-L1, purge momentów, I-8..I-10, fr pytanie, krótsze tytuły pushy) + `fw/be11-env` (.env.example); wymaga scalenia + pełnej suity. FE gotowy = `f3cc3bb` na `feat/first-week-home` (worktree mindsync-frontend-wt-fw-int), FF nad origin/dev 6f2c168, 21 commitów; push na dev = TestFlight (spodziewany 2.0.109), potem `ART9_SCHEDULE_GATE_MIN_APP_VERSION`. Runbook: design-specs/2026-10-07-first-week-home/DEPLOY_RUNBOOK.md. Pułapka: rollback kodu po pojawieniu się wierszy FIRST_WEEK_STEP zatrzymuje dostarczanie pushy (stary SQLEnum) — fix forward.
**Decyzje operatora 11.10 wieczorem:** luki PostHog do DOPISANIA (nie akceptacja), naprawić nagłówek Home po „Not sure yet”, bez posta na Instagram; po naprawie push na oba repo (zgoda jawna), operator robi `heroku login`, lead puszcza migracje. Lead scalił drugą paczkę BE na `feat/first-week-home` = 7e281ff (bez nowej migracji); w toku fw/fe11-hero, fw/fe12-events, pełna suita BE.
**WDROŻONE BE 11.10 20:36:** push 7e281ff na main (qa GO: 11121 pass, 9 baseline) = Heroku v571 (rollback target v570); `alembic upgrade head` m316->m317->m318a1b2c3d4 (head) puścił lead po `heroku login` operatora (klasyfikator przepuścił przy jawnej zgodzie). Trasy first-week odpowiadają 403 bez tokenu. Błąd „nagłówek pokazuje przesuniętą sesję” NIE istniał (hero pierwszego tygodnia bez sesji, COPY 1); fe11 naprawił za to skipped_dates w lokalnej matematyce MainTabCubit i tytuł prep z `session_date`; FE int = f202e1a, czeka na fe12 (zdarzenia PostHog). Przy okazji: prod `posthog_service.identify()` rzuca TypeError `set_once` (sprzed tej pracy).
**FE 11.10 wieczorem:** qa pełna suita na fa8985c (fe11 + fe12 zdarzenia) = GO, 4440 testów, 26 faili identycznych z origin/dev 6f2c168 (record_session_appbar_close wisi, therapy_card_detail_screen_error bez Routera, ui/reflect_tab, save_feedback_indicator). Potem FF do 2ff6e92 (fe13: poprawki security E-M1 zgody Art. 9 tylko z karty bocznej bez właściwości, E-L1 bez `drop`, E-L2 `resetFirstWeekForAccountChange()` przed resetem PostHog). Audyt: design-specs/2026-10-07-first-week-home/audit-security-events-2026-10-11.md. Delta qa na 2ff6e92 = GO (1731 pass, 0 fail, analyze bez zmian). **FE WYPCHNIĘTE 12.10: 2ff6e92 na origin/dev** (FF z 6f2c168) = Codemagic, oczekiwany tag app_2.0.109. Otwarte po pushu: `ART9_SCHEDULE_GATE_MIN_APP_VERSION` (krok operatora), weryfikacja zdarzeń w PostHog po TestFlight, splash 404 nie woła `PostHogService.reset()` (sprzed tej pracy, drobne), posthog `identify()` TypeError `set_once` na BE.

**Why:** retencja przegrywa w dniach 1-7, patrz analytics-reports/2026-10-03-retencja-subskrypcje-priorytety.md. Powiązane: [[project-first-conversation-voice-v2-2026-10-05]], [[project-usage-trend-paywall-diagnosis-2026-09-25]].
**How to apply:** przed budową operator decyduje SPEC §12 (7 punktów). WP-0 (czerwona kartka: naprawy, wspólny limit pushy, neutralne treści, IANA) można zacząć niezależnie. Security-guardian sprawdza kod przed deployem.
