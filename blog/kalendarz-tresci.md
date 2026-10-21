# Kalendarz treści bloga MindSync – mapa klastrów (szkielet)

> Stan: SZKIELET po adaptacji 2026-08-25. Klastry = propozycja lidera na bazie
> pozycjonowania marki i istniejących landingów; **kolejność i wybór tematów wewnątrz
> klastra dyktują dane** (GSC gdy się odblokują – patrz `scripts/gsc/gsc.config.json` –
> a do tego czasu research konkurencji przez `seo-content-writer` + Ahrefs).
> Każda partia tematów przechodzi KROK 0 (bramka pokrycia) przed briefami.

## Klastry topical authority (propozycja startowa)

1. **Getting more from therapy** (pillar; partner landingu /pre-order/tracking-therapy-effectiveness)
   – how to prepare for a session, is therapy working, what to talk about, therapy homework,
   why you forget what happened in session. Kategoria: MindSync Tips / Therapy.
2. **Between sessions** (serce produktu)
   – nervous system regulation (JEST live – rozbudowa, nie duplikat), between-session
   tracking, journaling vs voice notes, building a check-in habit.
3. **Understanding your patterns** (partner /pre-order/understand-behavioural-patterns)
   – triggers, mood patterns, emotional granularity, why mood tracking works/fails.
4. **Therapy logistics & decisions**
   – how to choose a therapist, cost of therapy, online vs in-person, when to consider
   therapy (partner /freebie – uwaga: ebook jest PL), red flags.
5. **Modern life & mental health** (szeroki wellbeing, top-of-funnel)
   – digital burnout (JEST live – rozbudowa), sleep, work stress, doomscrolling.
6. **Data & measurement in mental health** (różnicujący nas klaster)
   – measuring therapy outcomes, what to share with your therapist, mood data privacy.
7. **For therapists** (B2B, sporadycznie; partner clinician portalu)
   – between-session data in practice, patient engagement, measurement-based care.
   ⚠ ZAMROŻONY do odsłonięcia portalu w apce: wejście patient-side ukryte w MSV3.4 (CS-11),
   `therapist-sharing` w katalogu = planned. Nie obiecujemy udostępniania terapeucie w treści.

## Zasady kalendarza

- Drip: **1 wpis dziennie** (Task Scheduler po testach publikatora); `planowana_data`
  bez kolizji i dziur – pilnuje `blog-queue-gate.py`.
- Wpis „partner" landingu linkuje do niego frazowym anchorem (duet wpis ↔ landing).
- Pętla striking-distance: raz w miesiącu `scripts/gsc/blog-tematy.py` → sekcja 1
  (pozycje 4-20) = zadania rozbudowy ISTNIEJĄCYCH wpisów, priorytet przed nowymi.

## Dziennik partii

| Partia | Data | Tematy | Status |
|---|---|---|---|
| Partia 1 (rekomendacja) | 2026-08-25 | wg `seo/blog/gsc-analiza-2026-08-25.md` §4: 1× how-to-use MindSync (jedyny temat z popytem w GSC), 1× rozbudowa nervous-system (striking distance poz. 14.7), 2× duety pod /pre-order/track-interventions i /tracking-therapy-effectiveness, reszta z klastrów 1-3 z researchu konkurencji | do zlecenia (KROK 0 przed briefami) |
| Partia 1 – ETAP A (lista tematów) | 2026-08-25 | 9 pozycji: 01 how-to-use MindSync · 02 ROZBUDOWA nervous-system · 03 duet track-interventions (which coping skills work) · 04 duet tracking-therapy-effectiveness (is therapy working) · 05 prepare for a session · 06 remember what you talk about in therapy · 07 PILLAR between sessions · 08 emotional triggers · 09 why mood tracking stops working. Pliki: `blog/queue/_preflight-partia1.json`, `blog/queue/_partia1-notatki-fraz.md` | KROK 0: **9× OK, 0 RYZYKO, 0 BRAK** |
| Partia 1 – ETAP B (briefy) | 2026-08-25 | 9 briefów w `blog/queue/_batch-partia1-briefs.md`; drip 2026-08-27..09-03 (kolejność publikacji podporządkowana linkowaniu: pillar 07 na końcu), 02 = edycja itemu w CMS bez daty dripu; Ahrefs niedostępny (brak wolumenów, research SERP) | do pisania przez `blog-writer` |
| Partia 2 (tematy + briefy) | 2026-09-03 | 10 pozycji, drip 2026-09-04..09-13, klastry 4/2/5/6 (klaster 7 zamrożony): 01 how to choose a therapist (HUB kl. 4) · 02 when your therapist is not the right fit · 03 is therapy worth the money · 05 journaling vs voice notes (HUB metody) · 04 how to do therapy homework · 06 racing thoughts at night (HUB kl. 5) · 07 sunday scaries · 08 how to stop doomscrolling · 09 tracking mood on antidepressants (duet /pre-order/mood-on-antidepressants) · 10 are mental health apps private. Pliki: `blog/queue/_preflight-partia2.json`, `blog/queue/_batch-partia2-briefs.md` | KROK 0: **10× OK, 0 RYZYKO, 0 BRAK**; briefy gotowe do pisania przez `blog-writer` |
| Partia 4 (tematy + briefy, pierwsza stylem Moniki) | 2026-09-25 | 3 pozycje, drip 2026-09-26..09-28, klastry 5/3/3: 01 early signs of burnout (`early-signs-of-burnout`, kl. 5) · 02 how to stop people pleasing (`how-to-stop-people-pleasing`, kl. 3, duet /pre-order/understand-behavioural-patterns) · 03 anxious attachment style (`anxious-attachment-style`, kl. 3); rezerwy bez briefów: loneliness, adult play. Linki w partii tylko wstecz, zero LINK-LATER. Pliki: `blog/queue/_preflight-partia4.json`, `blog/queue/_batch-partia4-briefs.md` | KROK 0: **5× OK, 0 RYZYKO, 0 BRAK** (policzone ręcznie wg logiki skryptu, do potwierdzenia jednym uruchomieniem); GSC nieuruchomiony, frazy z SERP; briefy gotowe do `blog-write` |
| Partia 5 (tematy + briefy, druga stylem Moniki) | 2026-09-28 | 7 pozycji, drip 2026-09-29..10-05, klastry 5/3/4/3/5/3/1 (żaden klaster dwa dni z rzędu): 01 morning anxiety (`morning-anxiety`, kl. 5) · 02 how to stop overthinking (`how-to-stop-overthinking`, kl. 3) · 03 online vs in-person therapy (`online-vs-in-person-therapy`, kl. 4, pierwszy wpis klastra o formacie) · 04 avoidant attachment style (`avoidant-attachment-style`, kl. 3, duet z anxious) · 05 benefits of play for adults (`play-for-adults`, kl. 5, rozwinięcie newslettera #17) · 06 same argument over and over (`same-argument-over-and-over`, kl. 3, duet /pre-order/understand-behavioural-patterns) · 07 when to stop therapy (`when-to-stop-therapy`, kl. 1, duet /pre-order/tracking-therapy-effectiveness); rezerwy bez briefów: loneliness in adulthood, imposter syndrome. Linki w partii tylko wstecz, zero LINK-LATER. Pliki: `blog/queue/_preflight-partia5.json`, `blog/queue/_batch-partia5-briefs.md` | KROK 0: **9× OK, 0 RYZYKO, 0 BRAK** (policzone ręcznie wg logiki skryptu, do potwierdzenia jednym uruchomieniem); GSC uruchomiony 09-28: 0 luk, frazy z SERP bez wolumenów; briefy gotowe do `blog-write` |
