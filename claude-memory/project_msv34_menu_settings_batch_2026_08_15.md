---
name: project-msv34-menu-settings-batch-2026-08-15
description: "MSV3.4 (menu boczne, Ustawienia, onboarding→Goals) — 16 itemów CS-01..CS-16, decyzje operatora i ustalenia recon-u"
metadata: 
  node_type: memory
  type: project
  originSessionId: ee6fd84f-fbfd-49e0-9973-e352078eae3f
  modified: 2026-08-15T17:28:21.275Z
---

Batch **MSV3.4** ruszył 2026-08-15. Spec Darka z 2026-08-07, 16 itemów CS-01..CS-16, zero open questions po stronie autora.
Źródło w repo: `Business_requirements/MSV3.4/MSV3.4_Settings_spec_2026-08-07.pdf` + wyekstrahowany `.md` (PDF przyszedł od operatora; Google Drive doca **nie da się** odczytać konektorem — udostępnienie nie dotarło na `mikolaj.jesion@gmail.com`, pliki są najpewniej na Workspace @mindsync.com).
ClickUp: `86caym3tr` w liście **Tech Tasks** `901508860552` (NIE w Features!), status "to do". Seria: MSV3.3 `86caym253` → MSV3.4 → MSV3.5 `86c9b63kv`.

## Ustalenia recon-u, które unieważniają założenia speca

- **Guardrail speca jest nieaktualny.** Spec zakłada, że MSV3.3 nie wszedł. Wszedł — BE `971f182`, FE `ff20f2a`, oba repo czyste i zsynchronizowane z originem. Zgodnie z instrukcją samego speca **CS-02 i CS-03 = tylko weryfikacja**:
  - CS-02 (ikona „i" na Main + kasacja Edit Layout) **JUŻ ZROBIONE** — `Icons.info_outline` w `main_tab_screen.dart:824`, `grep Icons.tune` = 0, persistence layoutu skasowana, backend nigdy nie miał pola.
  - CS-03 (ołówek w Mood Trend) **JUŻ ZROBIONE** — `Icons.edit_outlined` size 24 w `unified_symptom_module.dart:135-142`.
- **CS-04 tańsze niż wygląda**: `SymptomTrackingCubit.addSymptom()` i `POST /api/v1/symptoms/` istniały z **zerem wywołań z UI**. „+Add new" = podpięcie gotowego kabla, zero backendu.
- **MSV3.4 nie wymaga ŻADNEJ migracji.** Deploy code-only. Head zostaje `ll3m4n5o6p7q`.
- **CS-08 grozi zepsuciem pushy**: backend wysyła deep link `/settings?section=therapy_schedule` (`notification_routes.py:50`, moment ADD_THERAPY_DATE). Trasy backendowej NIE wolno zmienić (stare buildy żyją tygodniami) → przekierowanie musi powstać w routerze frontu.
- **CS-11**: „Share my check-ins with my therapist" **nie istnieje** w kodzie. Wejście do panelu terapeuty jest na ekranie **Konto** (`account_body.dart:187-191`), nie w Settings. Ukrycie UI nie wymaga zmian backendu.
- Drawer (`drawer_menu.dart`) ma 11 pozycji i **żadnej lewej** — nie ma czego flagować wg guardrailu. Brakuje „Moja terapia".

## Decyzje operatora (2026-08-15) — nadpisują literę speca

1. **CS-10 / Privacy & Data — NIE usuwać backendu.** Za sekcją stoi `consent_records` (ślad audytowy RODO, model wprost mówi „rows are NEVER deleted") + `is_consent_active()` jest **bramką zapisu Art. 9** w `POST/PUT /users/profile`. Decyzja: **oba przełączniki zgód przenieść na ekran Konto**, sekcja znika z Settings, backend nietknięty. Zachowuje wykonalność Art. 7(3) RODO.
2. **CS-01 — dopisywać cel BEZ limitu 5.** Dziś `sync_goals_from_onboarding` (crud.py:6691) no-opuje, gdy user ma ≥1 aktywny cel, więc Done-when speca („powtórny onboarding dokłada drugą kartę") nie przechodzi. Limit 5 z `crud.create_goal:5274` zdjęty. UWAGA: prompty AI były projektowane pod maks. 5 celów — bound trzeba trzymać na poziomie promptu, nie bazy.
3. **CS-07 — zostawić re-auth** tuż przed faktycznym skasowaniem konta, wbrew „no password re-entry" ze speca. Uwaga: re-auth NIE jest tu wymogiem technicznym — konto Firebase kasuje backend joba `firebase_delete_user` przez Admin SDK (`users.py:1437-1444`), klient nie woła `user.delete()`, więc `requires-recent-login` nie wystąpi. To czysta decyzja bezpieczeństwa.
4. **CS-13 rozszerzony**: poza `support@mindsync.app` → `hello@mindsync.app` (4 miejsca w 2 plikach Dart) poprawiamy też osobny bug — `support@mindsync.**com**` (zła domena) w kluczu `recording_consentSheetBody` w 7 plikach ARB.

## Status: WSZYSTKIE 16 ITEMÓW **PUSHED** (2026-08-15)
BE `4bb9b2c` → origin/main. FE `1c20e54` → origin/dev (rebase na bota Codemagic `beeecfe`, wersja 2.0.78+151; push na dev = build Codemagic → TestFlight/Play internal).
**Backend ZDEPLOYOWANY automatycznie: Heroku v534 „Deploy 4bb9b2c8"**, ~30 s po pushu na origin/main – patrz [[reference-backend-autodeploy-on-push]] (push = deploy, nie ma osobnego kroku). Po deployu web/worker/scheduler `up`, zero H10/crashy/tracebacków w 300 liniach logów.
**Migracja NIE była potrzebna** – zmiany BE to czysta logika Pythona, zero DDL; head zostaje `ll3m4n5o6p7q`, deploy code-only. Gdyby batch RUSZAŁ schemat, ta automatyka byłaby pułapką: kod poszedłby na prod przed migracją.
Drzewo robocze: BE 4 pliki zmienione (`_therapy_helpers.py`, `users.py`, `crud/crud.py`, `tests/test_goals.py`), **0 migracji**. FE 39 zmienionych / 6 usuniętych / 16 nowych.
- Testy FE (sweep po dotkniętych katalogach): 436 pass / 7 fail — wszystkie 7 pre-existing w `test/ui/settings/widgets/{save_feedback_indicator,therapy_frequency_selector}_test.dart`, żaden z tych plików ani testowanych widgetów nie występuje w `git status`.
- Testy BE: 5154 pass / 20 fail — skład 1:1 z baseline. `test_onboarding_v2::TestResetTherapyOnboarding::test_preserves_therapy_data` **zweryfikowany na czystym worktree HEAD 971f182 → pada też bez naszych zmian**.
- `flutter analyze`: 131 issues, **0 errors**, identycznie jak baseline.

## Znalezione bugi POZA zakresem (kandydaci do MSV3.5)
- **`_CustomIntervalInput` (`therapy_frequency_selector.dart:134`) jest martwym kodem** — zadeklarowany, nigdy nie instancjonowany. Skutek: wybór częstotliwości „Custom" NIE pokazuje pola „Every N days". To źródło 2 z 7 czerwonych testów FE. Uwaga: CS-08 przeniósł ten selektor do nowego huba „Moja terapia", więc bug jest teraz w świeżo wyeksponowanym miejscu.
- 30 kluczy PL ma angielski fallback (`l10n_completeness_test` ostrzega, nie failuje). Część zasadna („Premium", „Trauma"), część nie: `workspace_agendaTitle`="Agenda", `prep_emotionalTemperature`="Your Mood This Week", `therapy_auditBreakthroughs`="Realizations & breakthroughs".

## Odstępstwa od speca (świadome, wszystkie zaraportowane)
- CS-02/CS-03 **pominięte** — guardrail speca, MSV3.3 wszedł.
- CS-01: trigger tworzenia celu został na **kroku 4 onboardingu**, nie na `onboarding_completed` (bo `_markOnboardingComplete` nie wysyła `goals_text`; przeniesienie zgubiłoby cel przy porzuconym onboardingu). **Czeka na werdykt operatora.**
- CS-01: przy zdejmowaniu capa dodano `.limit(10)` w `_therapy_helpers.get_active_goal_dicts` — funkcja NIE miała limitu i karmi realtime AI (`voice_director`) oraz prep-cards. Bez tego zdjęcie capa = nieograniczony prompt.
- CS-14: wykrywanie stłumienia dialogu przez `AppLifecycleState` w oknie ~700 ms (spec sam oznaczył to „compiler call, flagged for veto"). **Wymaga QA na fizycznym urządzeniu.**
- `lib/gen/assets.gen.dart` edytowany ręcznie (brak `fluttergen` w env) — getter + wpis w `values`, pozycja alfabetyczna zgodna z generatorem; `pubspec.yaml:177` rejestruje cały katalog `assets/svg/`, więc pubspec nie wymagał zmian.

## Wymagane przed wypuszczeniem
Device-QA na iPhone i Androidzie (spec: „After each item, run the app on Android and iOS"), ze szczególnym naciskiem na CS-14 (natywny dialog recenzji) i CS-16 (brak zawieszonego spinnera przy wylogowaniu).
Powiązane: [[feedback-subagent-task-sizing]], [[feedback-memory-write-after-commit]], [[project-postgres-enum-drift]]
