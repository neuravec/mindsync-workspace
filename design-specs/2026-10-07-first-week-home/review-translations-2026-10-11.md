# First-week Home: review of the non-English strings

Date: 2026-10-11. Reviewer: brand-voice-manager (read only; no app file edited).

Sources:
- `mindsync-frontend-wt-fw-int/mindsync_app/lib/l10n/app_{en,de,es,fr,nb,pl,sv}.arb`, branch `feat/first-week-home` (cd68adc per the brief; read as on disk while merges were still landing, so line numbers may shift).
- `MindSync-wt-fw-integration/app/services/push_copy.py`, `app/services/first_week/follow_up.py` (`_CALM_QUESTIONS` points to `_FIXED_QUESTIONS`), `app/tests/test_push_privacy_h4.py`.
- `COPY.md` sections 0 to 14 (EN source of truth), `docs/blog/brand-mindsync.md` (tone).

Severity:
- **must-fix** before TestFlight: wrong or stale meaning against the current EN, broken placeholder, therapy word on a lock screen, dash, server and client disagreeing.
- **nice-to-have**: naturalness, consistency, length.

Length method: visible characters, `{orcaName}` counted as "Orca". A button or chip gets a text row only when it is over 130% of the EN length and over the COPY "Max", and a shorter natural string exists. Where no shorter string keeps the meaning, it goes to a "layout check" line instead (flutter-mobile confirms it wraps to 2 lines and never ellipsizes, COPY rule 3).

No proposed string contains U+2014 or U+2013 (mechanical scan of this file done). Where a current value contains a dash, it is written here as [em dash] or [en dash].

## Summary

| Locale | must-fix (asked scope) | nice-to-have rows | Related must-fix (section 5) |
|---|---|---|---|
| de | 11 | 21 | 12 remaining dash lines |
| es | 0 | 12 | therapist consent button (dash) |
| fr | 1 | 9 | therapist consent button (dash) |
| nb | 0 | 7 | therapist consent button (dash) |
| pl | 0 | 10 | therapist consent button (dash) |
| sv | 0 | 5 (10 keys) | therapist consent button (dash) |
| en | | | therapist consent button (dash) |

Push allowlist: neutral in all 7 languages, 0 must-fix. Fixed follow-up question: 1 must-fix (fr, counted above).

Top issues:
1. **Nine of the 38 German strings translate the old, clinical EN** (before the June de-clinicalization): "Genauigkeit" (accuracy), "Bewertung" (assessment), "Symptomwerte", "verfolge Symptome", "Überwache Symptomtrends", "legt deine Basis fest" (sets your baseline), "Audit". Today's rewrite removed the dashes but kept the stale meaning. The same stale wording sits in es, fr, nb and sv (section 5.3).
2. **German consent screen is now mixed language.** `therapists_consentConfirmButton` is German ("Zustimmen und verbinden", meaning matches) while every other string on that consent screen is still English in `app_de.arb`. Ship one language per screen (section 1, row 10, and 5.1).
3. **French follow-up question: server and ARB differ.** Server "Comment tu te sens en ce moment ?", ARB "Comment ça va, là, maintenant ?". COPY 14.5 requires them to be equal.
4. **German recap heading has the wrong meaning.** "{orcaName} ist aufgefallen" reads "Orca stood out". Needs "Das ist {orcaName} aufgefallen".
5. **Spanish recap chip collides with the Weekly summary.** "Resumen semanal" is also the Weekly summary badge, which week-1 accounts do not get yet.
6. **Swedish "röstmeddelande"** (voice message, voicemail) for a note to self suggests it is sent to someone. Use "röstanteckning".
7. **Register:** recommend informal (du, tu) everywhere; de has only 15 formal lines, fr 106 (section 4).

---

## 1. German: the 38 strings rewritten today

All 38 are dash-free and every placeholder is intact (`{number}`, `{date}`, `{start}`, `{end}`, `{sourceLabel}`, `{orcaName}`). Register is du throughout.

Fine as they are (15): `settings_frustrationInfo`, `settings_therapyFocusInfo`, `stats_checkInNumberDate`, `stats_heroInsightDataWindow`, `character_bioStillGenerating`, `therapy_realizationFromSource`, `recording_uploadingBackgroundNote`, `prep_questionFlowSkip`, `tour_slide2_subcopy`, `tour_slide3_body`, `tour_slide5_body`, `tour_slide5_orcaLevelBody`, `walkthrough_reflectBody`, `info_characterTabBody`, `info_reflectTabBody`.

Should change (23):

| # | Key | Current | Proposed | Reason | Severity |
|---|---|---|---|---|---|
| 1 | `stats_earlySignalBadge` | Fruehes Signal: Genauigkeit verbessert sich mit mehr Daten | Noch am Anfang. Mit mehr Check-ins wird das klarer. | Translates the old EN ("accuracy improves with more data"). Current EN: "Early days, this gets clearer with more check-ins". "Genauigkeit" claims a measured accuracy, which the EN removed. Also "Fruehes" without umlaut. | must-fix |
| 2 | `stats_infoSheetDescription` | Diese Bewertung basiert auf deinen selbst angegebenen Symptomwerten, markierten Erkenntnissen, Sitzungsthemen und App-Nutzung der letzten 4 Wochen. Sie zeigt, was die Daten nahelegen, nicht, was die Therapie wert ist. | Diese Übersicht beruht auf deinen eigenen Check-ins, markierten Erkenntnissen, Sitzungsthemen und deiner App-Nutzung der letzten 4 Wochen. Sie zeigt, was auffällt, nicht, was deine Therapie wert ist. | Old EN. Current EN says "summary", "your own check-ins", "what stood out". "Bewertung" (assessment) and "Symptomwerte" are the clinical words the EN dropped. | must-fix |
| 3 | `character_bioEmptyCoach` | Deine Geschichte beginnt diese Woche! Halte eine Sitzung fest, schreibe eine Notiz, verfolge ein Symptom, und ich habe dein erstes Profil am Sonntag bereit. | Deine Geschichte beginnt diese Woche! Halte eine Sitzung fest, schreib eine Notiz oder mach einen Check-in, und bis Sonntag ist dein erstes Porträt fertig. | "verfolge ein Symptom" is the old "track a symptom"; current EN "add a check-in". "Porträt" matches the heading right above it (`character_bioEmptyTitle` "Dein Porträt entsteht"). | must-fix |
| 4 | `therapy_auditFirstAuditBanner` | Das ist dein erstes monatliches Audit. Es legt deine Basis fest. | Das ist dein erstes monatliches Audit, ein Startpunkt, auf den du später zurückschauen kannst. | "legt deine Basis fest" is the old "sets your baseline"; current EN "a starting point you can look back on". "Audit" stays for now so the banner matches the badge on the same screen; rename the whole de "Audit" family to "Monatsrückblick" in one go (5.3), then this becomes "Das ist dein erster Monatsrückblick, ein Startpunkt, auf den du später zurückschauen kannst." | must-fix |
| 5 | `healthCheck_firstCheckInBody` | Du hast gerade deine erste Sitzung festgehalten. Lass uns schauen, wie sich deine therapeutische Beziehung anfuehlt. Das legt deine Basis fest. | Du hast gerade deine erste Sitzung festgehalten. Lass uns schauen, wie sich deine therapeutische Beziehung anfühlt. Das ist ein Startpunkt, auf den du später zurückschauen kannst. | Same stale "baseline" as row 4; "anfuehlt". | must-fix |
| 6 | `tour_slide4_statsBody` | Sieh, wie sich deine Symptome und Stimmung entwickeln. Muster zeigen sich im Laufe der Zeit. Schaue wöchentlich nach. | Sieh, wie sich deine Check-ins und deine Stimmung entwickeln. Muster zeigen sich mit der Zeit, also mach einmal pro Woche einen Check-in. | "Symptome" is the old EN; current EN "check-ins". "Schaue wöchentlich nach" means "look weekly", the EN says "check in weekly". | must-fix |
| 7 | `tour_slide5_yourLevelBody` | Du erhältst XP bei jeder Interaktion: Gespräche, Notizen, Reflexionen und Symptom-Check-ins. | Du bekommst XP, wann immer du die App nutzt: Gespräche, Notizen, Reflexionen und Check-ins. | EN lists "check-ins", no "symptom". | must-fix |
| 8 | `info_mainTabBody` | Deine tägliche Übersicht: Sieh bevorstehende Sitzungen, verfolge Symptome, halte Gedanken fest und überprüfe deinen Therapiefortschritt. | Deine tägliche Übersicht: Sieh dir anstehende Sitzungen an, schau, wie es dir geht, halte Gedanken fest und behalte deinen Therapiefortschritt im Blick. | "verfolge Symptome" is the old EN; current EN "check in on how you're feeling". | must-fix |
| 9 | `info_statsTabBody` | Verfolge deine Therapiereise: Überwache Symptomtrends, überprüfe Gesundheits-Check-ins, setze Ziele und sieh periodische Snapshots deines Fortschritts. | Behalte deine Therapie im Blick: Sieh, wie sich deine Check-ins mit der Zeit verändern, schau dir frühere Check-ins an, setz dir Ziele und sieh regelmäßige Momentaufnahmen deines Fortschritts. | Old EN ("monitor symptom trends", "health check-ins"); current EN "see how your check-ins change over time, revisit past check-ins". Also drops "Therapiereise" (journey is on the no-use list for this feature). | must-fix |
| 10 | `therapists_consentConfirmButton` | Zustimmen und verbinden | For TestFlight: the dash-free EN string, "Allow and connect" (5.1). After the screen is translated: "Erlauben und verbinden". | Meaning check: "Zustimmen und verbinden" = "consent and connect". It matches the EN action exactly; only the first-person "I" is gone, which is the normal German button form. The problem is the screen around it: `therapists_consentHeading`, `therapists_consentIntro`, `therapists_consentItem1` to `6`, `therapists_consentReadOnly`, `therapists_consentRevocable` and the success strings are all still English in `app_de.arb`. A German user would give consent to share health data on an English screen with a German button. Keep the screen in one language; translate the whole `therapists_*` block as one task, with the lawyer, before the store release. "Erlauben und verbinden" then mirrors "Erlauben und weiter" from 14.1. | must-fix |
| 11 | `chat_emptyThreadsTitle` | Das ist dein Raum zum Nachdenken.\nIch bin hier, um zuzuhoeren und zu reflektieren, nicht um zu beraten. | Das ist dein Raum, um laut nachzudenken.\nIch bin hier, um zuzuhören und mitzudenken, nicht um dir Ratschläge zu geben. | "think out loud" lost "laut"; "zuzuhoeren" without umlaut. | nice-to-have |
| 12 | `chat_takeYourTime` | Lass dir Zeit, oder speichere diesen Thread und komm spaeter zurueck. | Lass dir Zeit. Oder speichere diesen Thread und komm später zurück. | Umlauts; the comma before "oder" reads stiff. | nice-to-have |
| 13 | `character_bioEmptyRealist` | Noch keine Daten. Nutze die App diese Woche: Ich brauche Material, bevor ich dein Profil schreiben kann. | Noch keine Daten. Nutze die App diese Woche, ich brauche erst etwas Material für dein Porträt. | "Profil" while the heading says "Porträt" (three words for one thing: Profil, Porträt, Bio). | nice-to-have |
| 14 | `character_bioEmptyExplorer` | Interessant, ein leeres Blatt! Lass es uns fuellen. Nutze die App diese Woche und ich erstelle dein erstes Profil aus dem, was ich entdecke. | Interessant, ein leeres Blatt! Lass es uns füllen. Nutze die App diese Woche, dann schreibe ich aus dem, was ich entdecke, dein erstes Porträt. | Umlaut; "Porträt" as in row 13. | nice-to-have |
| 15 | `character_bioFailed` | Konnte gerade nicht laden. Tippe zum erneuten Versuchen. | Laden hat gerade nicht geklappt. Tippe, um es noch einmal zu versuchen. | Subjectless first sentence; "zum erneuten Versuchen" is stiff. | nice-to-have |
| 16 | `capture_processingWait` | Das dauert normalerweise ein paar Sekunden. Du kannst diesen Bildschirm schliessen. Deine Karte ist bereit, wenn du zurueckkommst. | Das dauert meist nur ein paar Sekunden. Du kannst diesen Bildschirm schließen. Deine Karte ist fertig, wenn du zurückkommst. | "schliessen", "zurueckkommst"; a card is "fertig", not "bereit". | nice-to-have |
| 17 | `recording_privacyBody` | (as on disk; four words without umlauts: voellig, praesent, Gespraechen, eingeschraenkt) | MindSync nutzt KI, um deine Sitzungen zu transkribieren und zusammenzufassen, damit du ganz präsent sein kannst. Sobald die Zusammenfassung erstellt ist, speichern wir deine Audiodateien nicht mehr.\n\nTherapie ist aber ein privater Raum. Weil das Aufnehmen von Gesprächen ohne Erlaubnis in vielen Regionen gesetzlich eingeschränkt ist und Vertrauen die Grundlage der Therapie ist, brauchst du für dieses Tool die Erlaubnis deiner Therapeutin oder deines Therapeuten. | Umlauts; "deines Therapeuten" is masculine only, while the de file pairs both forms elsewhere (`workspace_todoSupportCopy`). Meaning unchanged. Consent-adjacent text, so it goes to the lawyer with 14.8. | nice-to-have |
| 18 | `recording_healthWarning` | Aufnahmeproblem erkannt, wird behoben... | Aufnahmeproblem erkannt. Wir versuchen, es zu beheben... | EN says "attempting to fix"; "wird behoben" promises the fix. | nice-to-have |
| 19 | `recording_tooShortBody` | Aufnahmen unter 10 Minuten werden nicht verarbeitet: Sie sind zu kurz, um eine nuetzliche Zusammenfassung zu erstellen. Diese Aufnahme wurde nicht gespeichert und zaehlt nicht fuer deine kostenlose Testversion. | Aufnahmen unter 10 Minuten werden nicht verarbeitet, weil sie für eine nützliche Zusammenfassung zu kurz sind. Diese Aufnahme wurde nicht gespeichert und wird nicht auf deine kostenlose Testversion angerechnet. | After the colon the capital "Sie sind zu kurz" reads as formal "You are too short". Three missing umlauts. | nice-to-have |
| 20 | `recording_uploadPausedOffline` | Upload pausiert, warte auf Verbindung | Upload pausiert, bis du wieder online bist | "warte" reads as an order to the person ("wait for a connection"). | nice-to-have |
| 21 | `tour_slide1_body` | Ich bin dein Begleiter hier. Wir werden deine Therapiereise gemeinsam unterstützen, einen kleinen Schritt nach dem anderen. | Ich bin hier an deiner Seite und begleite dich durch deine Therapie, Schritt für Schritt. | "Therapiereise" is a calque of "journey"; the sentence is long for a tour slide. | nice-to-have |
| 22 | `walkthrough_characterBody` | Du und {orcaName} leveln beide auf. Dein Level spiegelt dein Engagement wider: Notizen, Reflexionen, Check-ins. {orcaName}s Level wächst, wenn die App Einblicke über dich aufbaut. | Du und {orcaName} steigt beide im Level auf. Dein Level zeigt, wie aktiv du bist: Notizen, Reflexionen, Check-ins. Das Level von {orcaName} wächst, je mehr Einblicke die App über dich sammelt. | "{orcaName}s" glues a genitive s onto a name the person chooses (wrong for names ending in s, x, z). "Du und X" takes the ihr form ("steigt"). | nice-to-have |
| 23 | `info_therapyTabBody` | Dein Therapie-Zeitstrahl: Durchsuche Sitzungsprotokolle, Vorbereitungskarten, Notizen, Aufzeichnungen und Wochenzusammenfassungen. Nutze Filter, um das Gesuchte zu finden. | Dein Therapie-Zeitstrahl: Blättere durch Einträge aus Nach der Therapie, Vorbereitungskarten, Notizen, Aufnahmen und Wochenzusammenfassungen. Mit Filtern findest du schnell, was du suchst. | "Sitzungsprotokolle" (session minutes) sounds clinical; the app calls these "Nach der Therapie" and recordings "Aufnahmen". | nice-to-have |

Umlauts: the agent that rewrote these kept the ASCII spelling (ae, oe, ue, ss) the strings had on `dev`. That is pre-existing, not a regression, and app_de.arb has at least 169 such lines (5.4). Rows above fix it only where the string changes anyway.

---

## 2. First-week, offer, terms and billing strings (de, es, fr, nb, pl, sv)

Checked against COPY sections 1 to 14, every `firstWeek_*` key in the six files.

- **Placeholders:** intact in every key of all six locales, including the ICU plurals (`trialDay3FreeBody`, `trialDay3FreeLimitsAll`, `recapOptTalkLimit`). pl declines the plural correctly ("do 15 wiadomości"); fr uses `one` where EN uses `=1`, which is correct for French.
- **No gendered forms for the person:** de, nb, sv have none by grammar. pl avoids gendered past tense on purpose ("wybrano", "za Tobą", "co mówisz", "{orcaName} będzie mieć"), es and fr avoid gendered adjectives ("Bienvenue" instead of "Ravi(e)"). Clean.
- **No clinical claims, no guilt or pressure:** clean in all six. Gentle strings stay gentle.
- **Terminology** matches the shipped labels:

| EN | de | es | fr | nb | pl | sv |
|---|---|---|---|---|---|---|
| Before therapy | Therapie vorbereiten | Antes de la terapia | Avant la thérapie | Før terapien | Przed terapią | Före terapin |
| After therapy | Nach der Therapie | Después de la terapia | Après la thérapie | Etter terapien | Po terapii | Efter terapin |
| Between Sessions | Zwischen Sitzungen | Entre sesiones | Entre les séances | Mellom øktene | Między sesjami | Mellan sessionerna |
| Reflect | Reflektieren | Reflexionar | Réflexion (nav label is "Reflexion", see 5.4) | Reflekter | Refleksja | Reflektera |
| check-in | Check-in | check-in | check-in | innsjekk | check-in | incheckning |
| Premium, Free | kept | kept | kept | kept | kept | kept |

- **Offer, terms and billing** (`postOnboarding_offerStarterBody`, `postOnboarding_offerStarterTerms`, `postOnboarding_billingStarter`): all six locales match COPY 14.7 word for word, including the approved German fix ("Einmalzahlung · kein Abo", "Kein Abo."). No change.

### de

| Key | Current | Proposed | Reason | Severity |
|---|---|---|---|---|
| `firstWeek_recapNoticedHeading` | {orcaName} ist aufgefallen | Das ist {orcaName} aufgefallen | As a standalone heading it reads "Orca stood out". The dative frame makes it "Orca noticed". 24 characters with "Orca", max 24. | must-fix |
| `firstWeek_todayCheckInBodyGentle` | Bewerte nur, was sich gerade okay anfühlt. Du kannst jeden Punkt überspringen. | Bewerte nur, was du gerade bewerten magst. Du kannst jeden Punkt überspringen. | Lost "to rate": now reads "rate only what feels okay right now", i.e. only the areas that are fine. EN means "only what you are okay rating". Gentle tone, worth doing. | nice-to-have |
| `firstWeek_trialDay3OfferBody` | Einmalig {price}. Premium für 2 Wochen ab heute, danach wechselst du zu Free. Nichts verlängert sich. | Einmalig {price}. Premium für 2 Wochen ab heute, danach wechselst du zu Free. Kein Abo. | Same "verlängern" ambiguity the lead fixed in 14.7; keeps the two offer screens on one wording for the same SKU. | nice-to-have |
| `firstWeek_checkInSavedTo` | Gespeichert in Stimmungs- und Symptomverläufe. | Gespeichert unter Stimmungs- und Symptomverläufe. | "in" needs the dative ("-verläufen"); "unter" plus the screen name reads as a place in the app. | nice-to-have |
| `firstWeek_checkInEmptyBody` | Dieser Check-in ist für die Schwerpunkte aus deiner Einrichtung. In Stimmungs- und Symptomverläufe kannst du jederzeit Schwerpunkte hinzufügen und bewerten. | Dieser Check-in ist für die Schwerpunkte aus deiner Einrichtung. Unter Stimmungs- und Symptomverläufe kannst du jederzeit Schwerpunkte hinzufügen und bewerten. | Same case problem. | nice-to-have |
| `firstWeek_followUpVoiceCta` | Per Stimme sprechen | Sprachgespräch | "speak by voice" is a tautology. | nice-to-have |
| `firstWeek_todayPrepCtaGentle` | Therapie vorbereiten öffnen | Therapie vorbereiten | 27 characters, 142% of EN, max 20. The feature name already reads as a calm action. | nice-to-have |

Layout check, no text change: `firstWeek_todayAfterCta` (25, 132%, max 20), `firstWeek_todayAfterCtaGentle` (24, 133%, max 20), `firstWeek_checkInSkippedUndo` (25, 179%, max 16), `firstWeek_chipPrep` (20, 143%, max 16), `firstWeek_openSettings` (20, 154%, max 16), `firstWeek_checkInSkip` (12, max 10), `firstWeek_undo` (10, max 8), `firstWeek_seePremium` (15, max 14).

### es

| Key | Current | Proposed | Reason | Severity |
|---|---|---|---|---|
| `firstWeek_todayPrepCta` | Empezar Antes de la terapia | Preparar la terapia | 27 characters, 135% of EN, max 20. "Preparar la terapia" is the shipped quick-capture label (`fab_prepareTherapy`), so the person already knows it. | nice-to-have |
| `firstWeek_quotaAfterCta` | Guardar una idea clave | Guardar idea clave | 22 characters, 147%, max 20. | nice-to-have |
| `firstWeek_chipRecap` | Resumen semanal | Repaso semanal | Identical to the Weekly summary badge (`therapy_badgeWeeklySummary` "Resumen semanal"), a feature week-1 accounts do not get yet. "repaso" is what the recap body, row meta and mirror line already say. | nice-to-have |
| `firstWeek_todayRecapTitle` | El resumen de tu primera semana está listo | El repaso de tu primera semana está listo | Same collision. | nice-to-have |
| `firstWeek_waitingRecapTitle` | El resumen está casi listo | El repaso está casi listo | Same collision. | nice-to-have |
| `firstWeek_ctaTalk` | Habla con {orcaName} | Hablar con {orcaName} | Every other es button is an infinitive (Ver la pregunta, Empezar check-in, Guardar check-in). | nice-to-have |
| `firstWeek_followUpWriteCta` | Escribe a {orcaName} | Escribir a {orcaName} | Same. | nice-to-have |
| `firstWeek_checkInSaveFailed` | No se ha guardado. Inténtalo de nuevo. | No se guardó. Inténtalo de nuevo. | The only Spain-style perfect in a file that uses the simple past (usaste, guardaste, dijiste), which also reads better for US Spanish speakers. | nice-to-have |
| `firstWeek_recapOwnWay` | Iré a mi manera | Lo haré a mi manera | "Iré" is "I will go"; EN means "I'll do it my way". | nice-to-have |

Layout check: `firstWeek_todayAfterCta` (29, 153%), `firstWeek_todayPrepCtaGentle` (25, 132%), `firstWeek_todayAfterCtaGentle` (27, 150%), `firstWeek_chipPrep` (19, 136%, max 16), `firstWeek_chipAfter` (21, 162%, max 16).

### fr

| Key | Current | Proposed | Reason | Severity |
|---|---|---|---|---|
| `firstWeek_followUpQuestionCalm` | Comment ça va, là, maintenant ? | Comment ça va en ce moment ? | Must equal the server string; see section 3. | must-fix (counted in section 3) |
| `firstWeek_todayCheckInCta` | Commencer le check-in | Faire le check-in | 21 characters, 150%, max 20. | nice-to-have |
| `firstWeek_checkInSave` | Enregistrer le check-in | Enregistrer | 23 characters, 177%, max 20; the screen title already says "Check-in rapide". | nice-to-have |
| `firstWeek_sessionUpdate` | Mettre à jour mon plan | Mettre à jour | 22 characters, 157%, max 20; the sheet is about the plan. | nice-to-have |
| `firstWeek_trialDay3FreeBody` | À partir d'après-demain, parler à voix haute avec {orcaName} fait partie de Premium. L'écrit reste dans Free, jusqu'à {limit, plural, one{{limit} message} other{{limit} messages}} par mois. | À partir d'après-demain, parler à voix haute avec {orcaName} fait partie de Premium. Écrire reste possible en Free, jusqu'à {limit, plural, one{{limit} message} other{{limit} messages}} par mois. | "dans Free" while every other fr string says "en Free"; "L'écrit" is stiff. | nice-to-have |
| `firstWeek_recapOptTalkLimit` | L'écrit est gratuit, jusqu'à {limit, plural, one{{limit} message} other{{limit} messages}} par mois | Écrire est gratuit, jusqu'à {limit, plural, one{{limit} message} other{{limit} messages}} par mois | Same. | nice-to-have |

Layout check: `firstWeek_todayAfterCtaGentle` (24, 133%), `firstWeek_openSettings` (19, 146%, max 16), `firstWeek_ctaTalkShort` (18, 138%, max 16), `firstWeek_chipAfter` (17, 131%, max 16).

### nb

| Key | Current | Proposed | Reason | Severity |
|---|---|---|---|---|
| `firstWeek_sessionDidntBody` | Planen din hopper over dette steget, og den vanlige planen din forblir som den er. Hvis du heller vil snakke om uken, er {orcaName} her. | Planen din hopper over dette steget, og de faste tidspunktene dine er uendret. Hvis du heller vil snakke om uken, er {orcaName} her. | "planen" names two things in one sentence (the week plan and the usual schedule), so the second half can read "your plan stays as it is". | nice-to-have |
| `firstWeek_sessionDidntBodyNoTalk` | Planen din hopper over dette steget, og den vanlige planen din forblir som den er. | Planen din hopper over dette steget, og de faste tidspunktene dine er uendret. | Same. COPY 14.2 requires it to equal the first sentence above: change both, and the 14.2 table. | nice-to-have |
| `firstWeek_sessionScopeOnceHint` | Den vanlige planen din forblir den samme. | De faste tidspunktene dine forblir de samme. | Same ambiguity, next to "Oppdater planen min". | nice-to-have |
| `firstWeek_todayAfterBody` | Når den er over, holder det med noen få ord. Helst mens det fortsatt er friskt. | Når den er over, holder det med noen få ord. Helst mens det er ferskt i minnet. | "friskt" alone reads "healthy"; matches the push copy ("ferskt i minnet"). | nice-to-have |
| `firstWeek_followUpVoiceCta` | Snakk med stemmen | Bruk stemmen | "talk with the voice" is unidiomatic. | nice-to-have |

Layout check: `firstWeek_checkInSkippedUndo` (19, 136%, max 16), `firstWeek_openSettings` (18, 138%, max 16).

### pl

| Key | Current | Proposed | Reason | Severity |
|---|---|---|---|---|
| `firstWeek_recapNotRight` | Nieprawda | To nie tak | "Nieprawda" ("that's false") sounds like an accusation; the button corrects Orca's note, not the person. | nice-to-have |
| `firstWeek_restBody` | Tak ma być. Jeśli coś się wydarzy, {orcaName} jest tu. | Tak ma być. Jeśli coś się pojawi, {orcaName} jest tu. | "coś się wydarzy" sounds like an incident; EN "comes up" is a thought or a need. | nice-to-have |
| `firstWeek_day0Body` | Konfiguracja i pierwsza rozmowa z {orcaName} za Tobą. Jak na pierwszy dzień, to dużo. | Konfiguracja i pierwsza rozmowa z {orcaName} za Tobą. Jak na pierwszy dzień, w zupełności wystarczy. | "to dużo" can read "that's a lot"; EN "plenty" means "enough", reassuring. | nice-to-have |
| `firstWeek_trialDay3Subtitle` | Wszystko, co zapisano, zostaje zapisane bez względu na wybór. | Wszystko, co masz zapisane, zostaje, cokolwiek wybierzesz. | Impersonal "zapisano" plus "zapisane" twice reads like a system log. "masz zapisane" stays gender-neutral. | nice-to-have |
| `firstWeek_trialDay3SubtitleGentle` | Nic z tego, co zapisano, nie zniknie, a {orcaName} będzie tu też w wersji Free. Dziś nie musisz niczego decydować. | Nic z tego, co masz zapisane, nie zniknie, a {orcaName} będzie tu też w wersji Free. Dziś nie musisz o niczym decydować. | Same; "decydować" takes "o czymś". | nice-to-have |
| `firstWeek_todayCheckInBody` | Oceń to, co wybrano na starcie, i zobacz dzisiejszy wynik obok punktu wyjścia. | Oceń obszary wybrane na starcie i zobacz dzisiejszy wynik obok punktu wyjścia. | Impersonal "wybrano"; still gender-neutral. | nice-to-have |
| `firstWeek_sessionMovedTitleNow` | Kiedy teraz jest sesja? | Na kiedy przeniesiono sesję? | Unnatural word order; the entry is "It moved to another day". | nice-to-have |
| `firstWeek_mirrorPrivacyLine` | Widzisz to tylko Ty, chyba że to udostępnisz albo połączysz terapeutę w MindSync. | Widzisz to tylko Ty, chyba że to udostępnisz albo połączysz się z terapeutą w MindSync. | "połączyć terapeutę" is unidiomatic; the app says "Połącz się z terapeutą" (`therapists_emptyTitle`). 87 characters, max 90. | nice-to-have |

Layout check: `firstWeek_openSettings` (17, 131%, max 16), marginal.

### sv

| Key | Current | Proposed | Reason | Severity |
|---|---|---|---|---|
| `firstWeek_todayNoteTitle`, `firstWeek_todayNoteCta`, `firstWeek_todayNoteTitleGentle`, `firstWeek_chipNote`, `firstWeek_didNote`, `firstWeek_recapOptNote` | Lämna ett röstmeddelande / Spela in röstmeddelande / Ett röstmeddelande, om det hjälper / Röstmeddelande / Ett röstmeddelande / Ett röstmeddelande på fredagar | Lämna en röstanteckning / Spela in röstanteckning / En röstanteckning, om det hjälper / Röstanteckning / En röstanteckning / En röstanteckning på fredagar | "röstmeddelande" is a voice message or voicemail, something sent to someone. In a therapy app that can read as "this goes to my therapist". It is a note to self that Orca summarizes. Change `reveal_firstWeekNoteWhat` too, so the app has one term. Lengths unchanged or shorter. | nice-to-have (recommended) |
| `firstWeek_todayCheckInBodyGentle` | Betygsätt bara det som känns okej. Du kan hoppa över vilket som helst. | Betygsätt bara det som känns okej att betygsätta. Du kan hoppa över vilket som helst. | Lost "to rate", same as de. | nice-to-have |
| `firstWeek_todayAfterBody` | När den är över räcker några ord. Helst medan det är färskt. | När den är över räcker några ord. Helst medan det är färskt i minnet. | Idiom; matches the push copy. | nice-to-have |
| `firstWeek_followUpVoiceCta` | Prata med rösten | Använd rösten | Unidiomatic, same as nb. | nice-to-have |

Layout check: `firstWeek_openSettings` (19, 146%, max 16).

Note for COPY: `firstWeek_openSettings` is over its max of 16 in de, fr, nb, pl and sv with the standard OS wording. Raise the max to 20 or confirm the wrap.

nb, pl and sv also put a "summary" word into the recap title ("Oppsummeringen", "Podsumowanie", "Sammanfattningen"), but none is identical to their Weekly summary label, so no change there.

---

## 3. Push allowlist (`push_copy.py`) and the fixed follow-up question

### 3.1 Neutrality on the lock screen

**Pass in all 7 languages, 0 must-fix.** 29 template keys x 7 languages = 203 title and body pairs read. No therapy, session, therapist, appointment, symptom, mood, feeling, emotion, stress, anxiety or crisis word, direct or indirect. Beyond the test's ban list I also checked German Termin and fühl, French rendez-vous, séance and sens, Spanish cita and sient, Norwegian time, timer and føl, Swedish mår and besök, Polish czuj, wizyt and samopoczucie: none occur. No names, no quotes, no placeholders. `MOOD_DIP_ALERT` stays neutral in every language ("A moment for you"). Good detail: nb `therapy_prep_same_day` avoids "timer", which also means "appointments".

### 3.2 Naturalness and length

The test allows translations 50 and 75 characters, but iOS and Android show a push title on one line and cut it, so titles over the EN max of 40 lose their end.

| Key | Lang | Field | Current | Proposed | Reason | Severity |
|---|---|---|---|---|---|---|
| `plan_step_recap` | de | title | Deine erste Woche ist bereit für einen Rückblick (48) | Deine erste Woche im Rückblick (30) | Length. | nice-to-have |
| `plan_step_recap` | fr | title | Ta première semaine est prête à être revue (42) | Le récap de ta première semaine (31) | Length; "récap" is the in-app word. | nice-to-have |
| `plan_step_recap` | es | title | Tu primera semana está lista para repasarla (43) | Un repaso de tu primera semana (30) | Length. | nice-to-have |
| `plan_step_recap` | nb | title | Den første uken din er klar til å se tilbake på (47) | Et tilbakeblikk på den første uken (34) | Length. | nice-to-have |
| `plan_step_recap` | sv | title | Din första vecka är redo att blicka tillbaka på (47) | En tillbakablick på din första vecka (36) | Length. | nice-to-have |
| `plan_step_recap` | pl | title | Możesz spojrzeć wstecz na swój pierwszy tydzień (47) | Twój pierwszy tydzień w skrócie (31) | Length. | nice-to-have |
| `therapy_appointment` | de | title | Eine Erinnerung, die du für heute gesetzt hast (46) | Deine Erinnerung für heute (26) | Length; "eine Erinnerung setzen" is an anglicism. | nice-to-have |
| `therapy_appointment` | fr | title | Un rappel que tu as prévu pour aujourd'hui (42) | Ton rappel pour aujourd'hui (27) | Length. | nice-to-have |
| `plan_step_checkin` | fr | body | Un petit point rapide est prêt. | Un check-in rapide est prêt. | The screen it opens is called "Check-in rapide"; "petit ... rapide" says small twice. | nice-to-have |
| `mood_update_request` | fr | body | Un petit point rapide t'attend dans MindSync. | Un check-in rapide t'attend dans MindSync. | Same. | nice-to-have |
| `therapy_prep` | es | body | Cualquier momento de hoy vale. | Cualquier momento de hoy está bien. | "vale" is Spain-only; the es ARB is neutral Spanish, which suits the US market. | nice-to-have |
| `reflection_invitation` | es | body | Escribe unas líneas, si te apetece. | Escribe unas líneas, si quieres. | Same; "si quieres" is what the ARB uses. | nice-to-have |
| `therapy_prep_same_day` | nb | body | Best gjort så snart du kan i dag. | Helst snart, når det passer deg. | "så snart du kan" adds urgency the EN does not have; "Best gjort" is a calque. Still avoids "timer". | nice-to-have |
| `goals_weekly` | pl | title | Nowości z tego tygodnia są gotowe | Twój cotygodniowy przegląd jest gotowy | "Nowości" reads like app news. 38 characters. | nice-to-have |

Every proposed string passes the test's ban list and length limits.

### 3.3 Fixed follow-up question (`_FIXED_QUESTIONS`, used as `_CALM_QUESTIONS` and `_GENERIC_QUESTIONS`)

| Language | Server (`follow_up.py:191-199`) | ARB `firstWeek_followUpQuestionCalm` | Verdict |
|---|---|---|---|
| English | How are you doing right now? | same | OK |
| German | Wie geht es dir gerade? | same | OK |
| Spanish | ¿Cómo estás ahora mismo? | same | OK |
| Norwegian | Hvordan har du det akkurat nå? | same | OK |
| Swedish | Hur mår du just nu? | same | OK |
| Polish | Jak się teraz czujesz? | same | OK (in-app only; natural and gentle) |
| French | Comment tu te sens en ce moment ? | Comment ça va, là, maintenant ? | **must-fix: mismatch** |

French fix: set both the server string and the ARB value to **"Comment ça va en ce moment ?"**, and update COPY 14.5. COPY 14.5 requires the server string to equal the ARB value: the server's string is stored as Orca's first message, so today the thread and the client show two different questions. The proposed text drops "te sens" (the EN deliberately says "doing", not "feeling") and the spoken "là, maintenant". Minimal alternative if the lead wants no ARB change: set the server string to the ARB value. All seven are neutral, informal, gender-free and dash-free; the single string per language keeps the H-1 property.

### 3.4 Suggestion for qa-testing (`test_push_privacy_h4.py`)

The ban list bans "stress" and "feel" for English only, and misses common indirect words. Add: de "termin", "fühl", "psych", "stress"; fr "rendez-vous", "ressen", "psy", "stress"; es "cita", "sient", "psic", "estrés"; nb "føl", "psyk", "stress"; sv "mår" (whole word), "besök", "känn", "psyk", "stress"; pl "czuj", "psych", "samopoczu", "stres". None of them occurs in today's copy; the list guards future edits.

---

## 4. Register: recommendation for the lead

Counts across the whole ARB (lines containing the form):

| Locale | Informal | Formal | Where the formal lines are |
|---|---|---|---|
| de | 554 lines with du, dich, dir, dein (106 of them first week) | 15 lines with Sie, Ihr (third-person "sie" and the pronoun label "Sie/Ihr" excluded) | `auth_genderSelfDescribeHint`, `auth_ageBandLabel`, `legal_sharingPersonalInfo`, `settings_noCustomSessions`, `recording_recoveryBody`, `recording_v2_recoveryBody`, `treatmentGoals_sectionSubtitle`, `onboarding_art9ConsentTitle`, `onboarding_art9ConsentBody`, `onboarding_art9ConsentRequired`, `onboarding_leadSourceOtherHint`, `settings_personalisationProfilingSubtitle`, `settings_useTherapyDataSubtitle`, `settings_confirmWithdrawProfiling`, `settings_confirmWithdrawArt9` |
| fr | about 491 lines with tu, te, toi, ton, ta, tes, t' (111 first week; onboarding and auth 49) | 106 lines with vous, votre, vos (onboarding and auth only 6) | Spread over about 20 areas: auth, legal, settings, main tab, stats, character, recording, prep, errors, the info tabs (`info_*TabBody`), Art. 9 consent and the settings consent toggles, workspace |
| es | tú throughout | 0 usted | |
| pl | Ty (capitalized) throughout | 0 Pan, Pani | |
| nb, sv | du throughout | 0 (sv "Ni" once, plural "you both") | |

So the premise needs one correction: onboarding is mostly informal in both de and fr. The formal lines are pockets, mainly the consent and legal texts in de, and scattered older batches in fr.

**Recommendation: informal everywhere (du, tu), the consent texts included, once the lawyer says yes (COPY 14.8 item 7).**

Reasons:
1. It is already the app's register: de 554 to 15, fr about 491 to 106; es, nb, pl and sv have no formal address at all.
2. The voice is a companion speaking in the first person in Monika's warm, direct style. "Sie" or "vous" from Orca reads cold, and it shows up exactly where trust matters most: consent, and recovery after a failed recording.
3. One consent record, one register. `firstWeek_sessionConsent*` (du) and `onboarding_art9Consent*` (Sie) grant the same ARTICLE9_HEALTH consent (14.8 item 1); two registers make them look like two documents.
4. The informal pronoun does not weaken consent. GDPR asks for clear and plain language (Art. 7(2), Art. 12(1)), not a formal pronoun. The lawyer confirms.

Order: de first (15 strings, one short task; do the three `onboarding_art9*` and four settings consent strings in the same lawyer review as 14.1), fr second (106 lines, a separate sweep that can go with the fr accent fix in 5.4).

---

## 5. Related findings outside the asked scope

### 5.1 `therapists_consentConfirmButton` in every locale

EN is "I consent [em dash] connect". es, fr, nb and sv carry the same English string, dash included; pl is "Wyrażam zgodę [em dash] połącz". The whole `therapists_*` consent block is still English in de, es, fr, nb and sv (only pl is translated), and the de copy of `therapists_consentItem1` is an old EN text ("Your symptom tracking scores and trends"; EN now "Your wellbeing check-ins and trends").

| Locale | Proposed now | Severity |
|---|---|---|
| en | Allow and connect | must-fix (dash) |
| de, es, fr, nb, sv | Allow and connect (same as EN until the block is translated; for de see section 1, row 10) | must-fix (dash; de also mixed language) |
| pl | Zezwól i połącz | must-fix (dash) |

"Allow and connect" mirrors "Allow and continue" from COPY 14.1. If the lawyer wants the word "consent" on the button: "I consent and connect". Then translate the whole `therapists_*` block in all five locales as one task, with the lawyer, before the store release.

### 5.2 Dashes still in `app_de.arb` (12 lines, outside the 38)

| Key | Current | Proposed |
|---|---|---|
| `mainTab_homeworkEmpty` | Gerade keine Aufgaben [em dash] schau später wieder vorbei | Gerade keine Aufgaben. Schau später wieder vorbei. |
| `capture_transcribingLongEstimate` | Deine {minutes}-minütige Aufnahme wird verarbeitet [em dash] das dauert meist etwa {seconds} Sekunden… | Deine {minutes}-minütige Aufnahme wird verarbeitet. Das dauert meist etwa {seconds} Sekunden… |
| `prep_moodTrackedFallback` | Diese Woche erfasst [en dash] Details im Stimmungsverlauf. | Diese Woche erfasst. Details findest du im Stimmungsverlauf. |
| `error_textSubmitFailedRetry` | Beim Speichern deiner Notiz ist etwas schiefgelaufen. Dein Text ist sicher [em dash] tippe auf Wiederholen, um es erneut zu versuchen. | Beim Speichern deiner Notiz ist etwas schiefgelaufen. Dein Text ist sicher. Tippe auf Wiederholen, um es noch einmal zu versuchen. |
| `recording_bg_uploadFailed` | Upload fehlgeschlagen [en dash] wird beim nächsten Öffnen wiederholt | Upload fehlgeschlagen, neuer Versuch beim nächsten Öffnen |
| `recording_bg_uploadSaved` | Gespeichert [en dash] Zusammenfassung wird vorbereitet… | Gespeichert. Zusammenfassung wird vorbereitet… |
| `recording_v2_recoverySaveSubtitle` | Audiodatei exportieren [en dash] keine Zusammenfassung wird erstellt | Audiodatei exportieren, ohne Zusammenfassung |
| `recording_resumedBanner` | Fortgesetzt [en dash] {duration} Audio erhalten | Fortgesetzt: {duration} Audio erhalten |
| `info_workspaceTabBody` | Hier verwaltest du deine Therapie zwischen den Sitzungen: die Agenda für die nächste Sitzung, Aufgaben, offene Themen, Erkenntnisse, Ziele und deine Beziehung zu deinem Therapeuten [em dash] alles an einem Ort. | Hier verwaltest du deine Therapie zwischen den Sitzungen: die Agenda für die nächste Sitzung, Aufgaben, offene Themen, Erkenntnisse, Ziele und deine therapeutische Beziehung. Alles an einem Ort. |
| `workspace_threadCapacityMessage` | Du hast bereits 5 aktive Themen. Schließe eins ab oder blende eins aus, um Platz zu machen [em dash] das neue Thema wartet in der Warteschlange. | Du hast bereits 5 aktive Themen. Schließe eins ab oder blende eins aus, um Platz zu machen. Das neue Thema wartet so lange in der Warteschlange. |
| `triage_saveFailed` | Konnte nicht gespeichert werden [em dash] bitte erneut versuchen | Konnte nicht gespeichert werden. Bitte versuch es noch einmal. |
| `workspace_todoSupportCopy` | Hausaufgaben von deiner Therapeutin/deinem Therapeuten und KI-Action-Points [em dash] an einem Ort. | Hausaufgaben von deiner Therapeutin oder deinem Therapeuten und KI-Action-Points, an einem Ort. |

Placeholders kept (`{minutes}`, `{seconds}`, `{duration}`). Every dash line is must-fix by our rule; I list these because the brief aimed at a dash-free de file. Other files still hold lines with a dash: en 52, es 50, fr 50, nb 50, pl 51, sv 50 (the full sweep from COPY decision 15).

### 5.3 The June de-clinicalization reached only en and pl

de, es, fr, nb and sv still carry the old clinical wording in the same keys. Examples: `stats_earlySignalBadge` ("accuracy improves with more data" in all five), `therapy_auditFirstAuditBanner` ("baseline" in all five), `tour_slide4_statsBody` ("symptoms" in all five), `info_statsTabBody`. In de the whole "Audit" family is stale too: `therapy_emptyMonthlyTitle`, `therapy_generatingMonthlyAudit`, `therapy_monthlyNoPeriodYetMessage`, `therapy_badgeMonthlyAudit`, `therapy_auditLimitedDataBanner`, `therapy_auditProcessing`, `therapy_auditFailed`, `therapy_auditPremiumTitle`, `therapy_auditPremiumSubtitle` ("Symptomtrends ... Fortschrittsbewertung"), `therapy_auditIsRegenerating` (EN: "monthly recap"; de proposal "Monatsrückblick"). Recommendation: one sweep per locale that diffs every key against the current EN. The nine must-fix rows in section 1 are the part today's rewrite touched.

### 5.4 Spelling debt in legacy strings

- de: at least 169 lines spell umlauts in ASCII (ae, oe, ue, ss), including visible labels such as `therapy_typeWeekly` "Woechentlich".
- es, fr, nb: missing accents in legacy strings ("Senal", "precision", "auditoria", "linea"; fr `nav_reflect` "Reflexion" while first week says "Réflexion", `auth_ageBandLabel` "Votre tranche d'age", `therapy_badgeWeeklySummary` "Resume hebdomadaire"; nb "noyaktigheten", "forste", "manedlige").
- sv: `tour_slide4_statsBody` "din humör" should be "ditt humör".

The first-week strings themselves are clean. One spelling pass per locale is a separate task.

### 5.5 Retired key still present

`firstWeek_followUpQuestionGeneric` is still in all 7 ARB files and has no reader under `lib/` outside `l10n` (checked 2026-10-11). It can be deleted now (COPY 14.5).
