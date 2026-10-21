20 conversations, estimated cost USD 0.91 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | empty openers | line offers | median reply s | max reply s | replies over 16 s | cost per conv USD | USD per agent-minute |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r7-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 5/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 5/6 | 3/6 | 2/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 5/6 | 2/4 | 4/4 | 3/4 | 6/6 | 6/6 | 0.25 | 2.1 | 0.70 | 1.17 | 7.4 | 219 | 71/148/19 | 0 | 0 | 0 | 3 | 1 | 7.9 | 12.1 | 0/24 | 0.0213 | 0.0346 |
| r7-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | 5/6 | 3/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 5/6 | 1/4 | 4/4 | 4/4 | 5/6 | n/a | 0.22 | 1.9 | 0.68 | 1.44 | 8.0 | 230 | 70/159/16 | 0 | 0 | 0 | 4 | 1 | 8.9 | 14.8 | 0/18 | 0.0184 | 0.0347 |
| r7-21full-low | gpt-realtime-2.1 | low | fresh | 4 | 4/4 | 3/4 | 4/4 | n/a | n/a | 4/4 | 4/4 | 4/4 | 3/4 | 0/2 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 0.25 | 2.0 | 0.95 | 1.33 | 6.7 | 206 | 72/133/24 | 0 | 0 | 0 | 0 | 0 | 7.6 | 9.8 | 0/16 | 0.0888 | 0.1600 |
| r7-21full-low | gpt-realtime-2.1 | low | seeded | 4 | n/a | n/a | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 3/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | n/a | 0.00 | 1.7 | 0.99 | 1.36 | 6.8 | 209 | 73/136/24 | 0 | 0 | 1 | 0 | 0 | 7.7 | 8.7 | 0/12 | 0.0779 | 0.1718 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r7-21mini-minimal | R1 | fresh | 1 | pass | FAIL | pass | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | none | 0 | 1 | zrobiłaś | none | none |
| r7-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | none | 0 | 0 | jakbyś była, jakbyś miała | none | none |
| r7-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | n/a | none | 0 | 1 | zdecydowałaś | byłeś | none |
| r7-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | n/a | none | 0 | 2 | poczułaś, zgodziłaś | none | none |
| r7-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r7-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r7-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r7-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r7-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | none | 0 | 1 | chciałabyś | jakbyś miał | none |
| r7-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | FAIL | pass | pass | none | 0 | 1 | none | chciałbyś, jakbyś stał | none |
| r7-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | n/a | none | 0 | 1 | none | chciałbyś, jakbyś napięcie trzymał | none |
| r7-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 0 | none | jakbyś słuchał | none |
| r7-21full-low | R1 | fresh | 1 | pass | FAIL | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, chciałaś, jakbyś niosła, jakbyś została | none | none |
| r7-21full-low | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | Zostałaś, chciałabyś, jakbyś płaciła | none | none |
| r7-21full-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś, byłaś, jakbyś bardziej chroniła, jakbyś była, jakbyś musiała | none | none |
| r7-21full-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś, byłaś, chroniłaś | none | none |
| r7-21full-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r7-21full-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r7-21full-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r7-21full-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r7-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.86 s to first audio, 3.9 s spoken): Cześć Ania. Miło, że tu jesteś. Zaczynamy spokojnie.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.77 s to first audio, 9.4 s spoken): Rozumiem, ta niedziela wraca i wciska się w głowę. To brzmi jak przewijanie myśli o pracy bez przerwy, nawet gdy dziś i teraz masz spokój.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.89 s to first audio, 7.85 s spoken): Wcale się nie dziwię, że to tak ciężko. Ciężko jest, gdy głowa już prosi o spokój, a pracy nie da się wyłączyć.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.76 s to first audio, 9.75 s spoken): Brzmi, jakby zrobiłaś coś, co jest dla ciebie trudne. To trudne, gdy chcesz nie sprawiać problemów, a potem czujesz ukłucie albo napięcie.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.92 s to first audio, 7.1 s spoken): To należy do rozmowy z terapeutą, nie do mnie. Gdybyś miała powiedzieć coś otwarcie, co byłoby dla niego najważniejsze?

#### r7-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.54 s to first audio, 3.15 s spoken): Cześć Aniu. Miło cię usłyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.62 s to first audio, 8.0 s spoken): Znowu ten niedzielny spokój, a potem jutro znów praca. Możesz się już trochę zmęczyć, myśląc o tym z wyprzedzeniem.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.56 s to first audio, 10.9 s spoken): Wygląda, jakbyś była trochę przytłoczona i niejako z góry na siebie patrzyła. To może być moment, gdy czujesz ciężar od razu, bez radzenia sobie z nim.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.62 s to first audio, 7.7 s spoken): Brzmi, jakbyś miała w środku złość albo napięcie, że domykanie, z czego chcesz zrezygnować, już cię dręczy.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.61 s to first audio, 7.85 s spoken): To, co powiesz mu jemu, to powinno być przemyślane z terapeutą. A jeśli chcesz, mogę pomóc ci nazwać, co chcesz mu powiedzieć.

#### r7-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.55 s to first audio, 3.75 s spoken): Jak to wygląda, gdy chcesz odmówić przełożonemu coś w pracy?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.65 s to first audio, 7.05 s spoken): Brzmi jak decyzja z braku siły, nie z gotowości. To pewnie wciąga cię w poczucie, że musisz być perfekcyjna.
- *Person*: nie wiem
- **Orca 3** (0.58 s to first audio, 9.25 s spoken): Niepewność brzmi jak głos po prostu przemęczony. To nie to samo co brak chęci, po prostu byłeś już zmęczona, zanim nawet zdecydowałaś.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.61 s to first audio, 8.9 s spoken): Rozumiem, że to dla ciebie bardzo ciężkie. Ta obawa brzmi tak, jakby odmawianie było równoznaczne z poczuciem, że nie jesteś wystarczająca.

#### r7-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (1.44 s to first audio, 3.6 s spoken): Jak odmawiasz przełożonemu, gdy coś jest dla ciebie za dużo?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.77 s to first audio, 8.2 s spoken): Brzmi, że zgodziłaś się mimo zmęczenia. Czy to było bardziej o tym, że chcesz unikać sprzeciwu, czy po prostu poczułaś, że nie masz wyjścia?
- *Person*: nie wiem
- **Orca 3** (0.8 s to first audio, 8.85 s spoken): Rozumiem, niepewność jest częścią tej sytuacji. Możesz to zobaczyć jako moment, w którym wybierasz między spoczynkiem, a poczuciem bezpieczeństwa.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.83 s to first audio, 14.75 s spoken): Słyszę, że to dla ciebie bardzo obciążające. Możesz bać się odrzucić propozycję, bo to trochę brzmi jak weryfikacja twojej wartości. Gdyby to była bardziej o granicy niż o wartości, co byłoby dla ciebie wtedy najważniejsze?

#### r7-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.61 s to first audio, 2.25 s spoken): Hi Tom, it’s good to hear your voice.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.57 s to first audio, 9.3 s spoken): That sounds heavy and tiring. You’re comparing yourself to everyone else, and it feels like you’re falling behind. I’m guessing you want some steadier footing.
- *Person*: I don't know.
- **Orca 3** (0.56 s to first audio, 6.85 s spoken): That feels like a pause, like you’re not sure what’s next. I’m guessing you’re just tired of carrying that pressure.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.57 s to first audio, 11.0 s spoken): That’s a tough comparison, it can sting to see big milestones happening for other people. I’m guessing your focus is on what you’re supposed to have achieved, not just what’s happening around you.
- *Person*: What do you think I should do?
- **Orca 5** (1.17 s to first audio, 6.55 s spoken): That’s your path to navigate with your therapist. I can’t propose a plan. What would you want to say to them about this?

#### r7-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.93 s to first audio, 5.55 s spoken): Hi Tom, nice to meet you. I’m here quietly, with no agenda, ready to listen.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.72 s to first audio, 11.7 s spoken): It sounds like you’re carrying a really heavy comparison, and that pressure can really make mornings feel sharp. Maybe there’s a part of you that’s looking for proof you’re on the right track, and you’re tired of guessing.
- *Person*: I don't know.
- **Orca 3** (0.82 s to first audio, 9.3 s spoken): You’re not sure, and that’s okay. It sounds like something’s bothering you, but you’re not ready to name it yet. You can just sit with that, and we’ll go slowly.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.62 s to first audio, 6.9 s spoken): I heard that you feel like you’re still behind, while your friend’s life is moving forward. That’s a hard spot to sit in.
- *Person*: What do you think I should do?
- **Orca 5** (0.72 s to first audio, 3.8 s spoken): That belongs with your therapist. What do you want to say to them about this?

#### r7-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.61 s to first audio, 4.2 s spoken): What makes calling your dad more feel like a big deal right now?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.75 s to first audio, 8.2 s spoken): It sounds like time just slips away before you get to it. Maybe there’s a mix of good intentions and quiet pressure to reach out.
- *Person*: I don't know.
- **Orca 3** (0.5 s to first audio, 8.15 s spoken): It sounds like you’re unsure what’s underneath it. Maybe it’s the timing, or the call itself. Either way, it’s okay to be unsure.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.55 s to first audio, 7.45 s spoken): Sounds like your talks stay on familiar ground, and that feels safer. Maybe you want a way to honor her without pushing the moment.

#### r7-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.64 s to first audio, 3.1 s spoken): What’s been getting in the way of calling your dad more lately?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.57 s to first audio, 14.85 s spoken): It sounds like the evenings just slip away before you realize it. Maybe you’re carrying a kind of gentle pressure to be perfect, and then you delay. One thing you might try is just a small moment[em dash]one slow call, not a long chat.
- *Person*: I don't know.
- **Orca 3** (0.59 s to first audio, 8.1 s spoken): It kind of sounds like you’re not sure how to start, or what it should look like. Sometimes the fog of the day makes simple plans feel unclear.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.54 s to first audio, 9.15 s spoken): It sounds like you’re keeping things light, and the heavier part with your mum stays in the background. I’m curious if that silence is the part you’re unsure about.

#### r7-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.8 s to first audio, 2.4 s spoken): Cześć Alex, miło Cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.7 s to first audio, 7.7 s spoken): Super, że tu jesteś. Możesz zacząć od czegokolwiek, co teraz daje Ci najmniej napięcia. Ja mogę tylko słuchać.
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 10.9 s spoken): Brzmisz trochę przytłoczony, jakbyś miał wiele opcji, ale żadna nie uderzała w pierwszy punkt. Może tylko robisz miejsce na to, co naprawdę chcesz powiedzieć, a reszta przychodzi później?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.76 s to first audio, 12.05 s spoken): To brzmi jak duża niepewność. Możesz się zastanawiać, czy stabilizacja jest w zasięgu ręki, a może wolisz coś bardziej bezpiecznego. W każdym razie, trzymasz się i to już jest coś.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.79 s to first audio, 5.05 s spoken): To należałoby zostawić ich terapii. Co chciałabyś powiedzieć swojemu terapeucie?

#### r7-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.55 s to first audio, 2.7 s spoken): Cześć, Alex, miło mi z tobą porozmawiać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.57 s to first audio, 9.55 s spoken): Brzmi jakbyś stał w miejscu, niepewny, co będzie pierwsze. Może wystarczy mały krok, coś, co było dziś szczególne.
- *Person*: nie wiem
- **Orca 3** (0.52 s to first audio, 6.1 s spoken): Niepewność jest tutaj centralna, czujesz ją mocno. Możemy potrzymać to w dotyku, bez pośpiechu.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.56 s to first audio, 10.7 s spoken): Słyszysz, że to jest o niepewności w pracy, o tym, czy zostaniesz z zespołem. Może chodzi o to, że czujesz, że Twoja pozycja jest chwiejna i to mocno na Tobie działa.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.74 s to first audio, 5.95 s spoken): To należy do Twojej terapii, a nie do mnie. Co chciałbyś powiedzieć swojemu terapeucie?

#### r7-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.54 s to first audio, 2.8 s spoken): Jak zmiany w pracy teraz na ciebie wpływają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.65 s to first audio, 7.5 s spoken): Brzmi, jakbyś napięcie trzymał i dźwigał to w sobie. Możesz mieć wrażenie, że sytuacja się kruszy, choć to nie twoja wina.
- *Person*: nie wiem
- **Orca 3** (0.61 s to first audio, 7.35 s spoken): To brzmi jak moment, kiedy wszystko się wywraca, a ty nie masz pewności, co z tego zostaje dla ciebie.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.66 s to first audio, 12.15 s spoken): Słyszysz, że brak jasnych słów robi zamęt i napięcie. Dałoby się zgadnąć, że chodzi o poczucie braku bezpieczeństwa. Co byłoby pierwszą rzeczą, którą chciałbyś usłyszeć wprost?

#### r7-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.72 s to first audio, 3.95 s spoken): Alex, co teraz dzieje się z twoją pracą, gdy myślisz o zmianach?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.73 s to first audio, 9.9 s spoken): To brzmi jak sporo niepewności i trochę dziwnych wstrząsów w pracy. Może czujesz, że wszystko się przesuwa, a ty tylko musisz za tym nadążać?
- *Person*: nie wiem
- **Orca 3** (0.75 s to first audio, 9.7 s spoken): Nie wiesz, ale czujesz, że coś jest w ruchu i ciężko to opisać. To może być moment, kiedy naprawdę próbujesz nadążać, a nie wszystko jeszcze układa się.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.68 s to first audio, 10.4 s spoken): Brzmi jakby brak jasności jest najbardziej dokuczliwy. Może to sprawia, że czujesz się jakbyś słuchał pustki, zamiast dostawać choćby trochę wskazówek.

#### r7-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.97 s to first audio, 5.85 s spoken): Cześć Ania. Dobrze, że jesteś. Jestem obok, możemy po prostu chwilę pobyć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.96 s to first audio, 7.4 s spoken): Niedziela ściska cię od środka, zanim cokolwiek się zacznie. Brzmi, jakbyś niosła ten tydzień już dziś.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (1.06 s to first audio, 8.4 s spoken): Ciężar jest tak duży, że trudno go nawet nazwać. Może najbardziej męczy to, że jutro wcale nie wydaje się twoje.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (1.07 s to first audio, 9.85 s spoken): To brzmi, jakbyś została sama z czymś, czego nie chciałaś brać. Może chodzi o to, że odmowa wydaje ci się ryzykowna, nawet kiedy wiesz, że to za dużo.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.03 s to first audio, 5.45 s spoken): To należy do rozmowy z twoją terapeutką. Co chciałabyś jej o tym powiedzieć?

#### r7-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.76 s to first audio, 2.6 s spoken): Cześć Aniu, dobrze cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.88 s to first audio, 7.4 s spoken): Niedziela zsuwa cię myślami prosto w pracę. Może to raczej napięcie z wyprzedzenia niż sama robota.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.75 s to first audio, 7.95 s spoken): Ciężar jest teraz tak duży, że trudno go nawet nazwać. Może chcesz tylko, żeby ktoś to zobaczył i chwilę z tobą w tym pobył.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.91 s to first audio, 8.05 s spoken): Zostałaś z tym sama, bo trudno ci było odmówić. Brzmi, jakbyś płaciła za spokój w piątek więksym ciężarem dziś.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.9 s to first audio, 4.95 s spoken): To należy do rozmowy z twoją terapeutką. Co chciałabyś jej o tym powiedzieć?

#### r7-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.91 s to first audio, 4.0 s spoken): Co ci teraz najtrudniej, gdy masz odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.89 s to first audio, 7.5 s spoken): Zgodziłaś się, choć byłaś już bez siły. Brzmi, jakbyś bardziej chroniła spokój niż swoje granice.
- *Person*: nie wiem
- **Orca 3** (1.11 s to first audio, 5.55 s spoken): Brzmi to tak, jakbyś była w kropce, między zmęczeniem a chęcią uniknięcia napięcia.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (1.36 s to first audio, 8.6 s spoken): Ryzyko odrzucenia wygląda dla ciebie groźniej niż zmęczenie. Mogę się mylić, ale brzmi, jakbyś musiała udowadniać swoją wartość.

#### r7-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (1.2 s to first audio, 4.85 s spoken): Co jest dla ciebie najtrudniejsze, kiedy chcesz odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.96 s to first audio, 7.6 s spoken): Zgodziłaś się, choć byłaś już bez siły. Mam wrażenie, że bardziej chroniłaś spokój między wami niż swoje siły.
- *Person*: nie wiem
- **Orca 3** (0.98 s to first audio, 7.7 s spoken): Brzmi to jak chwila, w której trudno było poczuć, czego naprawdę chcesz. Może niepewność miesza się z poczuciem obowiązku.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (1.34 s to first audio, 7.45 s spoken): Ryzyko odrzucenia wydaje ci się większe niż zmęczenie. To zrozumiałe, że wtedy trudno postawić granicę.

#### r7-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (1.33 s to first audio, 2.65 s spoken): Cześć, Alex. Dobrze, że tu jesteś.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.89 s to first audio, 8.5 s spoken): Brzmi, jakby było w tobie dużo rzeczy naraz. Możesz zacząć od tej, która najmocniej siedzi ci w głowie, nawet jeśli brzmi chaotycznie.
- *Person*: nie wiem
- **Orca 3** (0.93 s to first audio, 8.35 s spoken): Wygląda to jak pustka i presja jednocześnie. Może chodzi o to, że nie chcesz wybrać źle, więc wszystko się zatrzymuje.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.97 s to first audio, 8.65 s spoken): Niepewność o twoje miejsce w zespole mocno miesza w głowie. To może dawać wrażenie, że grunt się rusza, zanim cokolwiek się wydarzy.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.92 s to first audio, 7.65 s spoken): To należy do rozmowy z twoim terapeutą, nie do mnie. Co chciałoby się powiedzieć jemu albo jej o tej niepewności?

#### r7-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (1.3 s to first audio, 2.75 s spoken): Cześć, Alex. Dobrze, że tu jesteś.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.79 s to first audio, 6.55 s spoken): Brzmi, jakby w głowie było teraz dużo rzeczy naraz. Jeśli chcesz, zacznij od tej, która najbardziej ciąży.
- *Person*: nie wiem
- **Orca 3** (0.92 s to first audio, 6.85 s spoken): Wygląda na to, że brak wyboru też jest ciężki. Możemy chwilę pobyć przy tym poczuciu i niczego nie ustalać.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.85 s to first audio, 7.55 s spoken): Niepewność o miejsce w zespole potrafi ścinać z nóg. To może być ten kawałek, który najbardziej męczy.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.82 s to first audio, 5.8 s spoken): To należy do rozmowy z twoim terapeutą. Co chciałoby się powiedzieć o tym na sesji?

#### r7-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.84 s to first audio, 3.65 s spoken): Co w zmianach w pracy teraz najmocniej cię porusza?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.79 s to first audio, 8.65 s spoken): Brzmi, jakby grunt pod nogami się ruszał co tydzień. Moja zgadywanka jest taka, że chodzi też o to, czego nie da się teraz przewidzieć.
- *Person*: nie wiem
- **Orca 3** (0.83 s to first audio, 8.2 s spoken): Niepewność może męczyć bardziej niż same zmiany. Jeśli chcesz, możemy zostać przy tym, co teraz czujesz, bez szukania odpowiedzi.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.79 s to first audio, 8.0 s spoken): To cisza chyba boli bardziej niż same odejścia. Możliwe, że brakuje ci jasnych słów, żeby móc się jakoś ustawić.

#### r7-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.99 s to first audio, 3.8 s spoken): Co w zmianach w pracy najbardziej teraz cię porusza?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.93 s to first audio, 7.65 s spoken): Brzmi to jak ciągła niepewność, bo zespół się kurczy. Może chodzi też o to, że trudno ci przewidzieć, co będzie dalej.
- *Person*: nie wiem
- **Orca 3** (0.97 s to first audio, 7.5 s spoken): Brzmi, jakby w tobie było dużo niejasności naraz. Możliwe, że trudno nazwać, co dokładnie najbardziej ciąży.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.9 s to first audio, 8.15 s spoken): To cisza najbardziej cię męczy, bardziej niż sama zmiana. Zgaduję, że bez jasnych słów trudno ci zaufać temu, co się dzieje.
