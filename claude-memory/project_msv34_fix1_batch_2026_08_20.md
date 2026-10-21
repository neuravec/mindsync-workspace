---
name: project-msv34-fix1-batch-2026-08-20
description: "MSV3.4 Fix.1 (7 itemów) + kolejność celów + fix zagłodzenia kolejki RQ - stan COMMITTED-pending, nic nie pushed"
metadata: 
  node_type: memory
  type: project
  originSessionId: b135de76-b7fb-4f2d-b294-9ab7c227a0a4
  modified: 2026-08-20T10:48:51.737Z
---

Batch z 2026-08-20. **Wszystko w working tree, NIC nie zacommitowane ani nie pushed.**

## MSV3.4 Fix.1 - 7 itemów zaimplementowanych
Spec: `Business_requirements/MS_3/v3.4/fix/MSV3.4 Fix.1.md`. Baseline specu był nieaktualny (skompilowany dla FE `f11f72e` / BE `8dd329d`, a MSV3.3.Fix.1 już wszedł: FE `96468f6`, BE `a817b77` = Heroku v542) - wszystkie numery linii przesunięte, `prep_card_widget.dart` urósł 1500→1951.

- CS-01/CS-02: wspólna kontrolka `SectionEditButton` 48 dp w wierszu nagłówka + tytuły 14/w700/ls0.3. **Efekt uboczny**: ołówki w `weekly_summary_widget.dart` też rosną (wspólny widget, nieuniknione bez flagi).
- CS-03: `pixelRatio` liczony per capture (pomiar layoutu offscreen), `compute()`, błąd widoczny + telemetria, `sharePositionOrigin`.
- CS-04: Discord `pVWS39kpg`.
- CS-05/CS-06: rollback+logi w obu blokach swallow, cel na górze, archived→Active z historią.
- CS-07: znalazł REALNY defekt - toasty w `settings_cubit.dart` hardcoded EN (cubit nie ma BuildContext); fix przez `navigatorKey.currentContext`.

**Bez migracji** - deploy code-only. Alembic head bez zmian (`pp7q8r9s0t1u`).

## Sprzeczności w specu wykryte przy implementacji
- CS-03: "floor 2.0" i "cap 8192 px" wykluczają się dla przypadku podanego w samym specu (~5000 logicznych px → potrzeba ~1.6). Rozstrzygnięte na korzyść capa (kompletność > ostrość).
- CS-05/CS-06: spec twierdził, że "poisoned session" to wspólna przyczyna. **Prod tego nie potwierdził** (zero trafień po 15.08). Realne: archived-skip + czwarty, nienazwany mechanizm - bramka `if stored_focus and stored_ratings` cicho pomijała sync gdy ratings=NULL.

## Nadpisania specu przez operatora
- **Każdy nowy cel na górze listy, także ręczny "+ Add goal"** - spec mówił wprost "do NOT touch the manual add path's ordering". Przy okazji wyszło, że ręczny cel JUŻ wcześniej skakał na dół po refetchu (klient prependował optymistycznie, serwer appendował) - to była realna, nieznana wcześniej regresja.
- Wybrano `_reserve_prepend_slots` (renumeracja) zamiast dryfu w ujemne `display_order`.

## Zagłodzenie kolejki RQ (osobny temat, ten sam batch)
Objaw: "Generate Now" weekly summary wisi na "Generating". **NIE był to stary build** (pierwsza diagnoza z samego kodu była błędna - agent nie miał dostępu do proda).

Prawdziwy mechanizm z proda (`db-reports/2026-08-20-weekly-summary-generate-now-stuck.md`): restart po v542 o 08:09:31 UTC odpalił pierwszą udaną masówkę dla ~1800 userów → ~2000 jobów w jedynej kolejce `default`; jeden `rq worker` bez współbieżności; tap o 09:16:14 nigdy nie pobrany, sweep ubił go o 09:38:49. Osierocony job dalej w kolejce.

Fix: kolejka `high` + `enqueue_interactive()` w `app/core/rq_queue.py` (fallback gdy brak workera na `high`), Procfile `rq worker --url $REDISGREEN_URL high default`.
**CO-DEPLOY: kod i Procfile MUSZĄ pojechać razem** - sam kod bez Procfile = joby w kolejce, której nikt nie drenuje (gorzej niż przed fixem). Jadą w tym samym slugu, więc jeden deploy jest atomowy.

**Ograniczenie**: RQ priorytetyzuje NASTĘPNY job, nie wywłaszcza trwającego. Tap w trakcie wielkiego joba crona dalej czeka.

## Decyzje operatora 2026-08-20
- **Nie skalować workerów** (zostaje 1, wszystkie dyna Basic). Obserwujemy przy następnym backfillu.
- **Chunkowanie godzinnego crona = osobny follow-up**, nie w tym batchu (cron DOPIERO zaczął działać: 145/145 weekly, 1752/1752 monthly).

## Follow-upy niezrobione
- 565 nigdy niedrenowanych wpisów `FailedJobRegistry` od 2026-07-03; zero referencji do `FailedJobRegistry` w całym kodzie. Nowa kolejka `high` będzie miała własny rejestr - sprzątanie musi objąć obie.
- Toasty poza Drawer/Settings dalej hardcoded EN (Moja terapia, Stats, Character).
- Chunkowanie crona (patrz wyżej).

## Wymaga QA na urządzeniu (nie da się zamknąć bez sprzętu)
CS-03 (fizyczny iPhone, najlepiej starszy + iPad), CS-07 (screenshoty EN/PL), CS-01 (komfort tapnięcia), działanie nowego linku Discord.

Patrz też: [[feedback-prod-evidence-before-code-only-diagnosis]]

## Runda 2 - "zaadresuj pozostale elementy" (ten sam dzien)

### Discord: link dziala, ale ZNOWU wygasa
Zweryfikowane przez Discord API: stary `ZWqzxdsr` = 404; nowy `pVWS39kpg` = wazny, guild "MindSync - Community", **ale expiry 2026-09-18 21:12:58 UTC**. Spec ostrzegal, ze zaproszenie ma byc "never expire" - dostarczony link tego nie ma, wiec bug wroci w polowie wrzesnia. Do decyzji operatora: bezterminowe zaproszenie + ewentualne przeniesienie linku na backend (dzis hardcoded => kazda wymiana = release apki przez TestFlight/Play).

### FailedJobRegistry: 565 to w 98% smieci, nie awarie
Charakterystyka z proda (`db-reports/2026-08-20-failedjobregistry-565-characterization.md`):
- **490 (87%)** = `deactivate_expired_subscriptions` z naprawionego 2026-08-10 buga duplikatow crona; wszystkie maja `status: finished` - ONE SIE UDALY.
- **~60** = funkcje USUNIETE przy Notification Cadence v3 (2026-07-03); nigdy nie wystartuja.
- **11 (2%)** na zywym kodzie, z czego **3** realne trwale straty: `run_conversation_analysis` (2026-03-02 SIGTERM) + `regenerate_goal_narratives` x2 (2026-07-25, dwa work-horse kills pod rzad = realny problem pojemnosci).
- OOM: 39/565 (6.9%) `Work-horse terminated unexpectedly`. Na zywym kodzie: 3 work-horse kills vs **ZERO** wyjatkow aplikacyjnych - kazda realna awaria jest infrastrukturalna.
- `mindsych_hourly_monthly_therapy_audit` failuje kosmetycznie: cale cialo joba w blanket `except Exception` bez re-raise, wiec do RQ dociera tylko work-horse kill; 1752 wierszy juz wtedy zapisane, self-heal na kolejnym ticku.

**GOTCHA (najwazniejsze): RQ NIE usuwa ID joba z `FailedJobRegistry`, gdy job z tym samym ID pozniej sie POWIEDZIE.** Udowodnione: te same ID siedza jednoczesnie w `FailedJobRegistry` i `FinishedJobRegistry`. Obecnosc w rejestrze != awaria. Monitoring liczacy surowe wpisy dalby ~554 falszywych alarmow pierwszego dnia i zostalby zignorowany.

### Zbudowany monitor
`app/tasks/rq_failed_job_monitor.py` + `setup_daily_rq_failed_job_monitor()` (03:15 UTC, offset od trzech jobow o 03:00), obie kolejki. Filtruje przez `status` + `FinishedJobRegistry`; wpisy po usunietych funkcjach i juz-udane czysci bez wzgledu na wiek; retencja **14 dni** tylko dla realnych awarii na rozwiazywalnym kodzie. Rozdziela `work_horse_killed` od `application_exception`.
`app/main.py` = +1 wywolanie w lifespanie. **Blok 23 wywolan `setup_*` NIE ma try/except** - nowy job nie pogarsza sytuacji (identyczny profil ryzyka co 22 pozostale), ale to istniejaca krucha sciezka bootu, warta osobnego follow-upu.

### Lokalizacja toastow - dokonczona
21 nowych kluczy x 7 jezykow + podpiete istniejace-ale-nieuzywane. Ustalenie: follow-up o "toastach symptomow w Stats" byl oparty na nieporozumieniu - metody `addSymptom/removeSymptom/renameSymptom/saveOrcaName` w `SettingsCubit` sa MARTWE (Stats uzywa `SymptomTrackingCubit`, ktory toasta nie pokazuje wcale).
**Test-straznik** w `test/l10n_completeness_test.dart`: skanuje zrodla `lib/` za `MsMessage.show*`/`BotToast.showText` z surowym literalem. Zweryfikowany przez wstrzykniecie prawdziwego naruszenia - wykryl je z `plik:linia`.

### Weryfikacja runda 2
`flutter analyze lib` 0 bledow; ARB parity 1772 klucze x 7; FE 87/87 + 17/17; BE 110/110 (monitor + scheduler idempotency + lifespan orchestrator). Em-dashe dodane przez nasz diff: **0** (jeden wszedl do komentarza, usuniety recznie).
