# MindSync — De-clinicalization & legal wording fixes (EN + PL)

Source: `translation_fixes/MINDSY_1.DOC` (extracted to `MINDSY_1_md.txt`).
Scope of THIS task: **EN (`app_en.arb`) + PL (`app_pl.arb`)** value changes, plus the
symptom-preset reframe (`lib/utils/symptom_presets.dart` + new ARB keys in all 7 langs).
Other 5 languages (de/fr/nb/sv/es) for the reframed *values* are a deferred follow-up
(doc Part XIV). Only the **8 new preset keys** are added to all 7 ARBs.

Guiding philosophy (doc Part XI cheat sheet — apply everywhere, incl. residual strings):
- symptom → check-in / focus area / how you're feeling
- severity / score(1–10) → intensity / rating
- monitor / track symptoms → notice over time / reflect / check in
- assessment / health check → reflection / check-in / summary / recap
- baseline → starting point
- signal / movement (R/A/G) → summary / what stood out
- audit → recap / review
- diagnose / treat / condition (affirmative) → ONLY inside the negating disclaimer
- patient → you / speaker
- improving / worsening / declining → feeling better / feeling tougher / steady

Trigger words to purge from affirmative user-facing copy (keep ONLY in the negating
disclaimer / Terms "No Medical Advice"): diagnose, treat, monitor, assess(ment),
symptom, severity, baseline, health check.

Paths:
- `mindsync_app/lib/l10n/app_en.arb`
- `mindsync_app/lib/l10n/app_pl.arb`
- `mindsync_app/lib/utils/symptom_presets.dart`
- ARB files for de/fr/nb/sv/es (ONLY for the 8 new preset keys)

Legend per item: KEY — new EN — new PL. "(keep)" = leave unchanged (listed for completeness).
"[JUDGMENT]" = compose per intent; exact wording at implementer's discretion within philosophy.

---

## PART II — Stats / Symptoms → Check-ins  [HIGH]

- `info_statsTabBody`
  EN: `Track your therapy journey — see how your check-ins change over time, revisit past check-ins, set goals, and see periodic snapshots of your progress.`
  PL: `Śledź swoją drogę w terapii — zobacz, jak Twoje check-iny zmieniają się w czasie, wracaj do wcześniejszych check-inów, ustawiaj cele i oglądaj okresowe podsumowania postępów.`
- `stats_symptomTracking` → EN `Wellbeing check-ins` / PL `Check-iny samopoczucia`
- `mainTab_therapyTracking` → EN `Wellbeing check-ins` / PL `Check-iny samopoczucia`
- `character_symptomCheckins` → EN `Wellbeing check-ins` / PL `Check-iny samopoczucia`
- Symptom-tracking reminder setting (FIND actual keys — search "reminder" / "symptom score";
  doc names them settings_notifSymptomTracking / *Desc but those exact keys may differ):
  - title → EN `Check-in reminders` / PL `Przypomnienia o check-inie`
  - desc  → EN `Weekly reminder to note how you're feeling` / PL `Cotygodniowe przypomnienie, żeby zapisać, jak się czujesz`
- `stats_howTrackerWorksBody`
  EN: `Note how you're feeling each day on a 1–10 scale.\n\nAfter 5 entries, you'll see a trend chart.\n\nA simple way to notice your own patterns.`
  PL: `Codziennie zaznaczaj, jak się czujesz, w skali 1–10.\n\nPo 5 wpisach zobaczysz wykres trendu.\n\nTo prosty sposób, żeby dostrzec własne wzorce.`
- `symptomTracking_initialSeverity` → EN `Starting intensity` / PL `Początkowa intensywność`
- `symptomTracking_mild` → EN `Light` / PL `Łagodnie`
- `symptomTracking_severe` → EN `Intense` / PL `Intensywnie`
- `symptomTracking_emptyTitle` → EN `Check in on how you're feeling over time` / PL `Sprawdzaj, jak się czujesz, w czasie`
- `settings_symptomsHelpText`
  EN: `These are the things you check in on in Stats. You can adjust intensity anytime from the Stats tab.`
  PL: `To rzeczy, które obserwujesz w zakładce Statystyki. Intensywność możesz dostosować w każdej chwili.`
- `mainTab_symptomTrend` → EN `Mood trend` / PL `Trend nastroju`
- `therapy_auditSymptomTrends` → EN `Mood trend` / PL `Trend nastroju`
- `therapy_weeklySummarySymptomShifts` → EN `Mood trend` / PL `Trend nastroju`
- `settings_symptomsSection` → EN `Focus areas` / PL `Obszary uwagi`
- `settings_profileGroup` → EN `Focus areas` / PL `Obszary uwagi`
- `stats_symptoms` → EN `Focus areas` / PL `Obszary uwagi`
- `stats_symptomsLabel` (residual) → EN `Focus areas: {value}` / PL `Obszary uwagi: {value}`
- `stats_logScore` → EN `Note` / PL `Zapisz`
- `stats_scoreLabel` → EN `Rating` / PL `Ocena`
- `stats_setFirstScore` → EN `Add your first check-in to start.` / PL `Dodaj swój pierwszy check-in, aby zacząć.`
- `symptomSuggestion_improving` → EN `Feeling better` / PL `Lepiej Ci`
- `symptomSuggestion_worsening` → EN `Feeling tougher` / PL `Trudniej Ci`
- `symptomSuggestion_updateTo` → EN `Set to {score}` / PL `Ustaw na {score}`
- `symptomSuggestion_newInsight` → (keep) `New insight` / `Nowe spostrzeżenie`
- `symptomSuggestion_basedOn` → (keep) `Based on your {triggerType}` / `Na podstawie Twojego {triggerType}`

Also sweep `app_en.arb` + `app_pl.arb` for any OTHER user-facing string still containing
"symptom"/"severity" in an affirmative sense and reframe per cheat sheet (e.g. signal/info
descriptions in Part III). Do NOT touch placeholder names or the negating disclaimer.

## PART III — Therapy Health Check → check-in / summary  [HIGH]

- `stats_therapyHealthCheck` → EN `Therapy check-in` / PL `Check-in terapii`
- `healthCheck_title` → EN `Therapy check-in` / PL `Check-in terapii`
- `fab_healthCheck` → EN `Therapy check-in` / PL `Check-in terapii`
- `therapy_typeHealthCheck` → EN `Therapy check-in` / PL `Check-in terapii`
- `stats_infoSheetDescription`
  EN: `This summary reflects your own check-ins, tagged realizations, session topics, and app engagement over the past 4 weeks. It shows what stood out — not what your therapy is worth.`
  PL: `To podsumowanie odzwierciedla Twoje własne check-iny, oznaczone spostrzeżenia, tematy sesji i aktywność w aplikacji z ostatnich 4 tygodni. Pokazuje, co się wyróżniło — a nie ile warta jest Twoja terapia.`
- `healthCheck_firstCheckInBaseline`
  EN: `This is your first relationship check-in. It's a starting point you can look back on.`
  PL: `To Twój pierwszy check-in relacji. To punkt wyjścia, do którego możesz wrócić.`
- `healthCheck_firstCheckInBody`
  EN: `You just captured your first session. Let's check in on how your therapeutic relationship feels — a starting point you can look back on.`
  PL: `Masz za sobą pierwszą sesję. Sprawdźmy, jak czujesz się w relacji terapeutycznej — to punkt wyjścia, do którego możesz wrócić.`
- Signal R/A/G group [JUDGMENT — drop traffic-light "signal/movement" framing, use neutral
  "what stood out" summary language; keep the three states distinct but non-clinical]:
  - `stats_earlySignal` → EN `What stood out` / PL `Co się wyróżniło`
  - `stats_refreshSignal` → EN `Refresh` / PL `Odśwież`
  - `stats_signalGreenLabel` (`Movement visible`) → EN `Things are moving` / PL `Widać ruch`
  - `stats_signalAmberLabel` (`Mixed signals`) → EN `A mixed stretch` / PL `Różnie bywało`
  - `stats_signalRedLabel` (`Limited movement`) → EN `A quieter stretch` / PL `Spokojniejszy okres`
  - `stats_signalGreenDescription` / `stats_signalAmberDescription` / `stats_signalRedDescription`
    → reframe per cheat sheet: drop "symptom scores", "signal"; speak of check-ins/what stood out. [JUDGMENT]
- `therapy_auditMovementAssessment` → EN `Looking back` / PL `Spojrzenie wstecz`
- `therapy_auditMovementVisible` / `therapy_auditMovementMixed` / `therapy_auditMovementLimited`
  [JUDGMENT — same neutral reframes as the signal labels above; keep distinct]
- `healthCheck_observation` → EN `Reflection` / PL `Refleksja`
- `healthCheck_safetyLabel` → EN `Safety` / PL `Poczucie bezpieczeństwa`
- `healthCheck_heardLabel` → EN `Heard and understood` / PL `Poczucie wysłuchania`
- `healthCheck_directionLabel` → EN `Direction` / PL `Kierunek`
- `healthCheck_processingResults` → EN `Putting your check-in together…` / PL `Składamy Twój check-in…`
- KEEP: `healthCheck_safetyEscalation*` (crisis/safety) — DO NOT TOUCH.

## PART IV — Settings & notifications: "Monthly audit" → "Monthly recap"  [MEDIUM]

Reframe the whole monthly-audit family. Search all keys containing "audit"/"Monthly audit"
and apply EN `recap`/`review`, PL `podsumowanie`/`przegląd`:
- `therapy_typeMonthly` (find), monthly-audit notification setting (find) → EN `Monthly recap` / PL `Miesięczne podsumowanie`
- `therapy_badgeMonthlyAudit` (`Monthly Audit`) → EN `Monthly recap` / PL `Miesięczne podsumowanie`
- `therapy_generatingMonthlyAudit` → EN `Generating monthly recap...` / PL `Tworzymy miesięczne podsumowanie...`
- `therapy_emptyMonthlyTitle` (`No monthly audits yet.`) → EN `No monthly recaps yet.` / PL `Brak miesięcznych podsumowań.`
- `therapy_auditFirstAuditBanner` → reframe "audit"→"recap", "baseline"→"starting point" [JUDGMENT]
- `therapy_auditLimitedDataBanner`, `therapy_auditProcessing`, `therapy_auditFailed`,
  `therapy_auditPremiumTitle` (and any `therapy_auditPremium*`) → "audit"→"recap"/"review" [JUDGMENT]
- NOTE (out of scope, do NOT implement): doc asks to remove notification frequency/intensity
  controls — that is a feature change, not wording.

## PART V — Session prep & trends  [MEDIUM]

- `prep_emotionalTemperature` → EN `Your mood this week` / PL `Twój nastrój w tym tygodniu`
- `therapy_recordingEmotionalArc` → EN `How the conversation flowed` / PL `Jak płynęła rozmowa`
- `prep_patternAlerts` → EN `Things to notice` / PL `Na co zwrócić uwagę`
- `prep_wasPreviousScore` → (keep) EN `was {score}/10` / PL `było {score}/10`
- `stats_improving` → EN `Brighter` / PL `Lżej`
- `stats_declining` → EN `Heavier` / PL `Ciężej`
- `stats_steady` → EN `Steady` / PL `Bez zmian`
- `therapy_auditBreakthroughs` → (keep) EN `Breakthroughs` / PL `Przełomy`
- `therapy_typeRealization` → (keep) EN `Realization` / PL `Spostrzeżenie`
- `therapy_emptyRealizations` → (keep wording; ensure PL says "Spostrzeżenia")

## PART VI — Recordings & clinical roles  [MEDIUM]

- `account_psychiatrist` → EN `Mental health professional` / PL `Specjalista zdrowia psychicznego`
- `therapy_recordingPatientInsights` → EN `Your insights` / PL `Twoje spostrzeżenia`
- `therapy_recordingTherapistObservations` → EN `Other speaker` / PL `Druga osoba`
- `account_therapist` / `account_addTherapist` / `account_role` / `settings_assignTherapist`
  → (keep) Therapist / Terapeuta — low risk, no change.

## PART VII — Onboarding therapy-approach descriptions  [MEDIUM]

Keep acronyms (CBT/DBT/EMDR/ACT). Soften the most clinical descriptions:
- `onboarding_emdrDescription` (`Eye Movement Desensitization and Reprocessing`)
  → EN `A guided approach for working through difficult memories` / PL `Metoda pomagająca przepracować trudne wspomnienia`
- `onboarding_somaticDescription` (`Body-based trauma and stress processing`)
  → EN `A body-centred approach to stress and tension` / PL `Podejście do stresu i napięcia oparte na ciele`
- Others (cbt/dbt/act/psychodynamic descriptions): keep as-is.

## PART VIII — Legal / disclaimer / consent

- `onboarding_medicalDisclaimer` → EN `How to use MindSync` / PL `Jak korzystać z MindSync`
- `onboarding_gdprConsent`
  EN: `I consent to MindSync processing my wellbeing and reflection data as described in our Privacy Policy`
  PL: `Wyrażam zgodę na przetwarzanie moich danych dotyczących dobrostanu i refleksji przez MindSync zgodnie z Polityką Prywatności`
- KEEP UNCHANGED (do NOT touch): `onboarding_disclaimerText`, `about_*`,
  Terms of Service "No Medical Advice", all crisis strings
  (`onboarding_crisis*`, `chat_crisisBanner`), `healthCheck_safetyEscalation*`.
- ⚠️ LEGAL FLAG: new `onboarding_gdprConsent` wording + Art. 9 GDPR basis must be
  confirmed by a lawyer before deploy (doc Part VIII). Privacy-policy age inconsistency
  (16+ vs 18+) is a separate legal item — not a wording change here.

## PART I — Onboarding copy (only items that map to real keys)

- `onboarding_welcomeSplashTitle` / `onboarding_welcomeSplashSubtitle` → (keep, already approved)
- `onboarding_challengesTitle` (`What do you want\nmore of?`)
  → EN `What would you like to work on?` / PL `Nad czym chcesz pracować?`
- `onboarding_selectAllThatApply`
  → EN `Choose at least one thing you'd like to keep an eye on.` / PL `Wybierz przynajmniej 1 rzecz, którą chcesz obserwować.`
- `onboarding_intensityTitle` (`How intense does each\nfeel right now?`)
  → EN `How are you feeling today?` / PL `Jak się dziś czujesz?`
- `onboarding_intensitySubtitle` (`No right answers. Just where you are today.`)
  → EN `Mark how strong each one feels right now.` / PL `Zaznacz, jak mocno teraz to czujesz.`
- `onboarding_intensityScale` → (keep)
- `onboarding_modalityTitle` (`Do you know what type\nof therapy you're in?`)
  → EN `Choose your therapy approach` / PL `Wybierz nurt terapii`
- `onboarding_modalitySubtitle`
  → EN `If you like, the app will adapt to the therapy approach you choose.` / PL `Jeśli chcesz, aplikacja dostosuje się do wybranego przez Ciebie nurtu terapeutycznego.`
- `onboarding_notSureDescription` (`That's okay — MindSync will adapt`)
  → EN `Let it flow. The app will adapt to you.` / PL `Niech się potoczy. Aplikacja dostosuje się do Ciebie.`
- `onboarding_scheduleTitle` (`When do you usually have therapy?`)
  → EN `Add when your therapy takes place.` / PL `Wpisz, kiedy masz terapię.`
- `onboarding_scheduleSubtitle`
  → EN `If you're in therapy, save your next session and the app will help you remember and prepare.` / PL `Jeśli jesteś w terapii, zapisz, kiedy masz najbliższą sesję. Aplikacja pomoże Ci pamiętać i się przygotować.`
- `onboarding_leadSourceTitle` (`How did you find MindSync?` / `Jak znalazłeś/aś MindSync?`)
  → EN `How did you hear about MindSync?` / PL `Skąd znasz MindSync?`  (gender-neutral PL)
- Screen #5 ("Your therapy matters") [JUDGMENT — map by meaning]:
  - title key for the therapy-journey/frustration screen → EN `Your therapy matters` / PL `Twoja terapia ma znaczenie`
    (e.g. `onboarding_journeyTitle`); add/adjust subtitle → EN `Fill this in if you're in therapy. MindSync will adapt to you and your therapy.` / PL `Uzupełnij, jeśli jesteś w terapii. MindSync dopasuje się do Ciebie i Twojej terapii.`
  - `onboarding_biggestFrustration` → EN `What frustrates you about your therapy?` / PL `Co Cię frustruje w Twojej terapii?`
  - `onboarding_goalsTitle` (`What do you hope to get from therapy?`)
    → EN `What's the goal of your therapy?` / PL `Jaki jest cel Twojej terapii?`
- Screen #10 final step [JUDGMENT — map to wow* keys]:
  - `onboarding_wowChooseFirstStep` → EN `I'd like to start with:` / PL `Chcę zacząć od:`
  - `onboarding_wowReflectFirst` → EN `a reflective chat with {orcaName}` / PL `refleksyjnej rozmowy z {orcaName}`
  - `onboarding_wowQuickNote` → EN `writing down what's on my mind today` / PL `zapisania tego, co mi dziś siedzi w głowie`
  - `onboarding_wowTrackFeeling` → EN `a quick check-in` / PL `krótkiego check-inu`
- Custom-field hint: where a clinical example is shown, use a neutral one
  (`onboarding_typeYourChallenge` or equivalent hint) → EN `e.g. tension, motivation` / PL `np. napięcie, motywacja`.

## PRESETS — symptom presets reframe (de-clinicalize the default chips)  [HIGH]

File: `lib/utils/symptom_presets.dart`. Replace the 17-item clinical list with the 8 soft
topics from the doc. New list (value sent to backend, label = localized):

```
('Low mood',  symptomPresetLowMood)
('Unease',    symptomPresetUnease)
('Overwhelm', symptomPresetOverwhelm)
('Worries',   symptomPresetWorries)
('Stress',    symptomPresetStress)
('Sleep',     symptomPresetSleepTopic)
('Loss',      symptomPresetLoss)
('Focus',     symptomPresetFocus)
```

Add these 8 NEW ARB keys to ALL 7 ARB files (en/pl real; de/fr/nb/sv/es translate these
8 simple words using existing files as style reference). EN / PL labels:
- symptomPresetLowMood: `Low mood` / `niski nastrój`
- symptomPresetUnease: `Unease` / `niepokój`
- symptomPresetOverwhelm: `Overwhelm` / `przytłoczenie`
- symptomPresetWorries: `Worries` / `zmartwienia`
- symptomPresetStress: `Stress` / `stres`
- symptomPresetSleepTopic: `Sleep` / `sen`
- symptomPresetLoss: `Loss` / `strata`
- symptomPresetFocus: `Focus` / `koncentracja`

- Leave the OLD `symptomPreset*` keys in the ARBs (unused — harmless; `localizedSymptomName`
  falls back to the raw stored value for legacy entries, so existing user data still displays).
- ⚠️ BACKEND NOTE (do NOT change backend; coordinate later): new chips send new backend
  `value`s (`Low mood`, …). Existing stored clinical values (`Depression`, …) keep displaying
  via fallback. No data migration here; flag for backend/analytics coordination.

## OUT OF SCOPE (report, do not implement — not wording/legal)

- UX/visual: intensity-slider redesign, add emoji/icons to topics, empty-state designs,
  picture/quote layout on final screen.
- Feature: remove notification frequency/intensity controls; "Prepare for therapy"
  activation redirect (screen #10 logic); "not in therapy / skip" new options.
- External input needed: Moni's comment text, Darek's plans CSV, therapist consultation,
  onboarding screen-numbering reconciliation (Part XIV).
- Off-repo: store listing copy, backend AI prompts (Part X).
- Legal review items: gdprConsent basis + privacy-policy age (16 vs 18) → lawyer.

## VALIDATION

1. `flutter gen-l10n` (or `flutter pub run build_runner build --delete-conflicting-outputs`)
   → regenerate `lib/l10n/generated/`. Must succeed.
2. `flutter analyze` → 0 errors.
3. `flutter test` → report results; fix only tests that assert changed strings.
4. Confirm no affirmative trigger words remain in en/pl (grep: symptom, severity, baseline,
   "health check", monitor, assess) outside the negating disclaimer / Terms.
