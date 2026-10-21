24 conversations, estimated cost USD 0.57 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | empty openers | line offers | median reply s | max reply s | replies over 16 s | cost per conv USD | USD per agent-minute |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r6-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 5/6 | 3/6 | 2/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 1/6 | 6/6 | 2/4 | 4/4 | 2/4 | 5/6 | 4/6 | 0.29 | 2.1 | 0.67 | 0.88 | 9.8 | 278 | 82/196/17 | 0 | 0 | 0 | 10 | 0 | 10.5 | 18.6 | 3/24 | 0.0261 | 0.0319 |
| r6-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 1/6 | 6/6 | 3/4 | 4/4 | 4/4 | 5/6 | n/a | 0.06 | 1.9 | 0.69 | 0.96 | 9.9 | 279 | 82/198/18 | 0 | 0 | 0 | 8 | 0 | 11.5 | 17.6 | 2/18 | 0.0213 | 0.0323 |
| r6-21mini-low | gpt-realtime-2.1-mini | low | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | 4/4 | 6/6 | 6/6 | 4/6 | 3/6 | 5/6 | 0/6 | 6/6 | 2/4 | 4/4 | 3/4 | 6/6 | 6/6 | 0.12 | 2.2 | 0.74 | 1.09 | 10.6 | 309 | 98/212/29 | 2 | 3 | 1 | 8 | 0 | 11.1 | 24.6 | 4/24 | 0.0280 | 0.0317 |
| r6-21mini-low | gpt-realtime-2.1-mini | low | seeded | 6 | n/a | n/a | n/a | 5/6 | 6/6 | 5/6 | 6/6 | 6/6 | 4/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 1/6 | 6/6 | 4/4 | 4/4 | 4/4 | 6/6 | n/a | 0.06 | 1.9 | 0.76 | 1.08 | 9.4 | 273 | 85/188/24 | 0 | 0 | 0 | 5 | 0 | 10.6 | 15.7 | 0/18 | 0.0203 | 0.0325 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r6-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | FAIL | pass | FAIL | none | 0 | 2 | chciałabyś, czułaś | none | none |
| r6-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | none | 0 | 3 | byś to ujęła, jakbyś wracała, mogłabyś, umiałaś | none | none |
| r6-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | Jakbyś musiała, byłaś, jakbyś usłyszała | none | none |
| r6-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | n/a | none | 0 | 1 | none | none | none |
| r6-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r6-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | FAIL | pass | n/a | n/a | n/a | pass | pass | none | 0 | 1 | none | none | none |
| r6-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r6-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 2 | none | none | none |
| r6-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | none | 0 | 3 | byś chciała | none | none |
| r6-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | FAIL | pass | pass | none | 0 | 1 | none | chciałbyś | none |
| r6-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | n/a | none | 0 | 2 | none | jakbyś miał, stałeś | none |
| r6-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | n/a | none | 0 | 2 | none | none | none |
| r6-21mini-low | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | pass | pass | none | 0 | 1 | none | none | none |
| r6-21mini-low | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | none | 0 | 2 | chciałabyś, chciałaś, jakbyś już była, jakbyś miała | none | none |
| r6-21mini-low | R1 | seeded | 1 | n/a | n/a | n/a | FAIL | pass | FAIL | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | zrobiłaś | none | none |
| r6-21mini-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | jakbyś czuła, powiedziałaś | none | none |
| r6-21mini-low | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | n/a | n/a | n/a | pass | pass | none | 0 | 1 | none | none | none |
| r6-21mini-low | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | FAIL | FAIL | pass | n/a | n/a | n/a | pass | pass | let me think | 0 | 1 | none | none | none |
| r6-21mini-low | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r6-21mini-low | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 1 | none | none | none |
| r6-21mini-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | FAIL | pass | pass | none | 0 | 1 | chciałabyś | none | none |
| r6-21mini-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | FAIL | FAIL | pass | FAIL | pass | FAIL | pass | pass | pass | pass | Daj mi chwil | 0 | 2 | none | nazwałeś | none |
| r6-21mini-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |
| r6-21mini-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |

### Transcripts

#### r6-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.59 s to first audio, 5.45 s spoken): Cześć, Ania. Miło Cię słyszeć, mam nadzieję, że jesteś gotowa na krótką rozmowę.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.71 s to first audio, 8.4 s spoken): Brzmi, jakby ta niedziela miała już w sobie jutro w pracy, ciężkie. To jest ciężkie, kiedy głowa pyta o to, co będzie jutro.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.63 s to first audio, 6.45 s spoken): Słyszę, że to cię przygniata po prostu. To nie tylko plan, ale cały ciężar, który niesiesz.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.62 s to first audio, 9.85 s spoken): Słyszę, że znowu coś dorzucono i czułaś, że nie można było tego zatrzymać. To brzmi jak poczucie bezradności, że musisz się zgodzić, choć czujesz, że nie chcesz.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.74 s to first audio, 14.75 s spoken): To zależy, ale mówiąc zgodnie z tym, co widzisz, może to być ważne powiedzieć wyraźnie. Ja nie mogę dawać porad, ale twoje poczucie może wskazywać, że chcesz postawić granicę bez poczucia winy. Co chciałabyś mu powiedzieć?

#### r6-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.73 s to first audio, 2.8 s spoken): Cześć, miło mi z Tobą spędzić ten czas.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.63 s to first audio, 9.35 s spoken): Brzmi jakbyś wracała do jutra, zanim w ogóle zakończysz ten wieczór. To może być moment, kiedy niepokój już wyprzedza to, co jest teraz.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.67 s to first audio, 9.7 s spoken): Rozumiem, ciężko jest bez konkretnego powodu, po prostu czujesz ciężar. Może chodzi o przeciążenie, a może o poczucie, że musisz coś domknąć w głowie.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.65 s to first audio, 9.55 s spoken): Słyszę, że szef znowu przyłożył Ci coś do głowy, a Ty nie umiałaś powiedzieć „nie”. Może to było bardziej o poczuciu, że musisz sprostać, niż o samym projekcie.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.67 s to first audio, 13.8 s spoken): Jasne, mogłabyś, ale to decyzja, która należy do Ciebie, a ja nie mogę Ci niczego narzucać. Jeśli już chcesz to powiedzieć, to jak byś to ujęła? To Twoje słowa, więc daj mi je, a ja posłucham.

#### r6-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.79 s to first audio, 4.95 s spoken): Jakie momenty, czyli co dokładnie, najbardziej utrudniają ci odmawiać przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.65 s to first audio, 13.15 s spoken): Brzmi, jakbyś usłyszała prośbę, a potem od razu zrobiła miejsce, nawet gdy byłaś już zmęczona. Czasem odmawianie nie jest o złej decyzji, tylko o tym, że potrzebujesz granicy dla siebie.
- *Person*: nie wiem
- **Orca 3** (0.65 s to first audio, 7.2 s spoken): Nie musisz wiedzieć od razu. Może czujesz, że sięgasz po zgodę z lęku albo z obowiązku, a nie z tego, co naprawdę chcesz.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.59 s to first audio, 8.2 s spoken): Słyszę, że to nie samo odmówienie boli, tylko strach przed oceną. Jakbyś musiała udowadniać swoją wartość, kiedy mówisz „nie”.

#### r6-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.76 s to first audio, 3.6 s spoken): Co jest dla Ciebie najtrudniejsze w odmawianiu przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.72 s to first audio, 12.35 s spoken): To brzmi jak moment, kiedy chcesz być po prostu dobra dla innych, a Twoja siła już jest wyczerpana. Może pod spodem jest presja, że trzeba się zgodzić, bo inaczej pojawi się konflikt.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 17.05 s spoken): Wygląda, że to naprawdę trudne, kiedy czujesz się w kropce, niepewna, czy Twoja decyzja to odwaga, czy ucieczka. I może właśnie to „nie wiem” jest sygnałem, że chcesz sięgnąć po to, co Twoje [em dash] granice, tempo, a nie tylko „łagodność wobec innych”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.57 s to first audio, 15.3 s spoken): Rozumiem ten lęk, że odmowa może wyglądać jak brak kompetencji. Chyba chodzi o to, że chcesz być wiarygodna i potrzebujesz, żeby ktoś to zobaczył. Może jednak to Twoje granice są ważne, choć też trudno je powiedzieć głośno.

#### r6-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.84 s to first audio, 4.7 s spoken): Hi Tom, nice to meet you. Just a quick hello, and I’m here if you want to talk.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.77 s to first audio, 7.55 s spoken): That sounds really heavy this morning. I heard you feeling like others have a clearer path, and you’re comparing yourself to that.
- *Person*: I don't know.
- **Orca 3** (0.83 s to first audio, 11.8 s spoken): That “I don’t know” feels like a small pause, but it can also be a real place of confusion. Maybe you’re noticing that you want something more defined, but you don’t have the words yet.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.73 s to first audio, 11.45 s spoken): I heard a bit of comparison there[em dash]watching people hit those big life milestones while you’re still in a shared place. And maybe it hits you in the gut because you want a clearer, steadier path too.
- *Person*: What do you think I should do?
- **Orca 5** (0.88 s to first audio, 10.8 s spoken): That’s a fair question, and it feels like you’re measuring yourself against others. I can’t tell you what to do, that’s for your therapist, but what do you think you’d want to say to them about this?

#### r6-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.77 s to first audio, 6.55 s spoken): Hey Tom, it’s good to hear your voice. You can start with whatever’s on your mind, and we’ll go from there.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.56 s to first audio, 14.45 s spoken): That feeling sounds heavy in the moment. You’re comparing yourself to people you don’t really know, and that can get loud when you’re tired. I’d guess you’re wrestling with wanting to be on track, and also feeling like you’re not allowed to admit you’re unsure.
- *Person*: I don't know.
- **Orca 3** (0.58 s to first audio, 7.9 s spoken): I hear you, not knowing can feel uneasy, and sometimes it’s the quiet part that says, “I’m not sure who I am yet.”
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.55 s to first audio, 18.55 s spoken): I heard the comparison hit a nerve there. It sounds like you’re watching what other people have and feeling like you haven’t caught up, even though your path is different. What’s the part you’re hoping that flatmate phase really represents for you, is it stability, being seen, or just a sense of direction?
- *Person*: What do you think I should do?
- **Orca 5** (0.58 s to first audio, 14.8 s spoken): What I’d do really belongs with your therapist, honestly. You’ve got a couple of things pulling at you, and I’m not sure I’m the right person to decide for you. One thing I’m curious about: what would you want to say to them about wanting stability, or about feeling behind?

#### r6-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.63 s to first audio, 4.25 s spoken): Tom, what’s one thing that usually makes it harder to call your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.68 s to first audio, 10.5 s spoken): Sounds like the moment slips away before you notice it. It could be that your evening feels full, or heavy, or maybe you’re not seeing a small window of time to call.
- *Person*: I don't know.
- **Orca 3** (0.61 s to first audio, 8.3 s spoken): Sounds like you’re not sure what’s going on, and that’s okay. One guess is that the evening feels fuzzy and you miss the cue to pick up the phone.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.59 s to first audio, 14.75 s spoken): You’re noticing that when you talk to him, the only real connection is football, not the shared family story. And it makes sense if that feels like a small piece of the relationship. Maybe you’re trying to protect the mood or avoid a heavier conversation.

#### r6-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.65 s to first audio, 3.1 s spoken): Tom, what keeps you from calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.63 s to first audio, 10.1 s spoken): I hear that the intention is there, but the time just slips by. Maybe it’s not that you don’t care, but that the day gets hijacked and you just don’t have the energy left.
- *Person*: I don't know.
- **Orca 3** (0.62 s to first audio, 9.5 s spoken): Got it, sometimes being unsure is part of the process. I’m guessing you’re weighing your energy, your stress, and your guilt, all at once, and that’s heavy.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.61 s to first audio, 10.75 s spoken): That sounds like a smiley kind of routine you’ve got, but it might feel like you’re avoiding the part that actually matters. I’m guessing you’d like a way to talk about her without it being heavy, if that’s true.

#### r6-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.64 s to first audio, 2.35 s spoken): Cześć, miło mi cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.63 s to first audio, 10.5 s spoken): Jasne, czujesz się trochę zagubiony i zaczęcie o czymkolwiek jest trudne. Możesz po prostu powiedzieć, co jest teraz najważniejsze, a resztę dopiero doprecyzować.
- *Person*: nie wiem
- **Orca 3** (0.57 s to first audio, 7.1 s spoken): Rozumiem, po prostu nie wiesz. To czasem już dużo. Spróbuj powiedzieć, co najmniej trochę ciąży w głowie.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.73 s to first audio, 16.4 s spoken): Słyszę, że w pracy dzieje się sporo i czujesz niepewność, czy zostaniesz w zespole. To brzmi jak coś, co może mocno obciążać głowę.

Myślę, że może chodzi o to, że zmiana jest nieprzewidywalna, a ty nie chcesz wchodzić w coś, co może skończyć się rozczarowaniem.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.67 s to first audio, 17.4 s spoken): To jest jedna z tych rzeczy, które zwykle lepiej zostawić dla twojego terapeuty. Mogę tylko powiedzieć, że to pytanie pokazuje strach przed rozczarowaniem i niepewność wobec przyszłości. A ty, co byś chciała powiedzieć terapeucie o tej sytuacji, gdybyś miała chwilę?

#### r6-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.57 s to first audio, 1.25 s spoken): Cześć, Alex.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.58 s to first audio, 10.6 s spoken): Rozumiem, że czujesz trochę niepewności, jak zacząć. Możesz po prostu powiedzieć ten najmniejszy kawałek, który teraz jest w głowie, a ja pomogę to uporządkować.
- *Person*: nie wiem
- **Orca 3** (0.58 s to first audio, 9.85 s spoken): Możesz powiedzieć po prostu, co teraz najmocniej cię dręczy. Jeśli wcale nie wiesz, to też spoko, bo to może oznaczać, że szukasz i wszystko jeszcze się układa.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.59 s to first audio, 9.8 s spoken): Hmmm, słyszysz, że to cię dręczy, i to zresztą całkiem zaufanie. Tylko ta niepewność co do przyszłości w zespole daje ci dziś do myślenia.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.76 s to first audio, 10.5 s spoken): Na Twoim miejscu nie jestem w stanie doradzić, to już należy do terapeuty. Mogę tylko zapytać: co chciałbyś, żeby powiedział Twojemu terapeucie?

#### r6-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.8 s to first audio, 5.2 s spoken): Alex, co najbardziej w zmianach w pracy teraz cię porusza lub martwi?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.96 s to first audio, 10.1 s spoken): Słyszę, że jest tam sporo naruszania stałeś ciągłymi odejściami. To może wywoływać napięcie i poczucie braku kontroli. Możesz powiedzieć, co najbardziej dokucza ci w tej sytuacji?
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 12.3 s spoken): To brzmi tak, jakbyś miał dużo na głowie, ale jeszcze nie złapał tego, co najbardziej wkurza, albo co najbardziej boli. Może to jest właśnie to poczucie, że wszystko się sypie bez pytania.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.63 s to first audio, 17.65 s spoken): Słyszę, że najbardziej wkurza brak jasności i tego, że nikt nie mówi wprost. To może być ciężkie, bo wszystko dzieje się półkrokiem. Może chcesz, żeby to było bardziej widoczne, albo żeby ktoś w końcu powiedział, czego potrebuje, albo co się dokładnie dzieje.

#### r6-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.92 s to first audio, 2.95 s spoken): Co najbardziej się wstrzymuje przy tych zmianach w pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.79 s to first audio, 13.8 s spoken): Słyszę, że to jest dla ciebie naprawdę ciężkie, bo co tydzień ktoś znika. Ten rytm odchodzeń mógł stworzyć poczucie niepewności i braku stabilności, nawet jeśli wszystko było wcześniej w miarę ułożone.
- *Person*: nie wiem
- **Orca 3** (0.79 s to first audio, 9.6 s spoken): Nie musisz wiedzieć od razu. Myślę, że możesz być po prostu zmęczony tym ciągłym ruchem, brakiem przewidywalności i powoli tracisz poczucie kontroli.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.76 s to first audio, 12.55 s spoken): Słyszę, że brak jasności cię męczy, bo nie wiesz, co jest faktem, a co plotką. To możliwe, że chcesz po prostu, żeby ktoś powiedział wprost, co się zmienia i czego można oczekiwać.

#### r6-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.72 s to first audio, 1.75 s spoken): Cześć, Ania.Cześć, Ania.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.86 s to first audio, 10.05 s spoken): Jasne, to brzmi jakby ten tydzień już cię doganiał. Możesz odprężyć się teraz, a potem zobaczysz, co faktycznie jest jutro na tapecie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.73 s to first audio, 9.95 s spoken): Wygląda, jakby ciężkość nie była tylko jutro, tylko jest teraz w środku. Może to poczucie, że musisz być gotowa na cały tydzień naraz.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.77 s to first audio, 9.75 s spoken): To brzmi jak moment, w którym czujesz, że coś przytłacza. Wygląda na to, że chcesz ustawić granicę, ale nie chcesz stracić relacji, albo spokoju.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.0 s to first audio, 16.9 s spoken): Nie, nie wiem za ciebie, to jest dla twojej terapii. Mogę tylko powiedzieć, że bycie szczerym jest ważne, jeśli masz na myśli granicę, którą chcesz postawić. Jeśli jednak to niesie więcej napięcia niż pożytku, to może lepiej najpierw skonsultować to z terapeutą, dla większej klarowności.

#### r6-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.91 s to first audio, 3.25 s spoken): Cześć, Ania, miło jest z tobą chwilę porozmawiać.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.61 s to first audio, 7.15 s spoken): Słyszę, że ta niedziela znów zepchnęła cię w myślenie o pracy. To jakbyś już była tam głową, zanim jutro się zacznie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.6 s to first audio, 10.9 s spoken): Rozumiem, że to po prostu ciężki moment, nie ma w tym nic rozdmuchanego. W takiej chwili czasem wystarczy po prostu nazwać, że to boli, i nic więcej.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.67 s to first audio, 12.4 s spoken): To brzmi, jakbyś miała trudne zderzenie: pracę chciałaś pokazać, a w środku zostawał opór. Możliwe, że chodzi o to, żeby nie krzywdzić siebie, a jednocześnie zaznaczyć granicę.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.09 s to first audio, 15.05 s spoken): To zależy, czy czujesz się na tyle bezpiecznie, żeby to powiedzieć wprost, i czy to w ogóle przyniesie ci ulgę. Uważam, że takie rzeczy warto omawiać z terapeutką, a ty możesz zdecydować, co chcesz mu powiedzieć. A co ty chciałabyś mu przekazać?

#### r6-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.81 s to first audio, 6.35 s spoken): Jak wygląda odmawianie przełożonemu w twojej głowie? Gdzie najczęściej siada strach albo poczucie winy?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.83 s to first audio, 12.0 s spoken): Słyszę, że mimo zmęczenia, zrobiłaś tak, by nie robić fali. To brzmi jak chęć dogadać się za wszelką cenę. Może w środku chcesz spokoju i zgody, a niekoniecznie kolejnego zadania?
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 11.5 s spoken): Niepewność jest tu częścią tego. Gdy nie wiesz, co dokładnie czujesz, dobrze jest po prostu zauważyć, że coś w tobie się opiera i daje to czas, by lepiej to usłyszeć.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.72 s to first audio, 8.75 s spoken): Brzmi, jakbyś cały czas ważyła swoje granice, żeby nie stracić czyjejś opinii. To ciężkie, gdy strach mówi głośniej niż chęć.

#### r6-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.69 s to first audio, 4.25 s spoken): Co najczęściej blokuje cię, kiedy próbujesz odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.66 s to first audio, 15.6 s spoken): Brzmi, jakbyś czuła albo brak siły, albo napięcie, a mimo to powiedziałaś tak, żeby nie konfrontować sytuacji. Może chodzi o to, że chcesz być ruchliwa i pomocna, a odmawianie wydaje się trudne i kosztowne emocjonalnie.
- *Person*: nie wiem
- **Orca 3** (0.57 s to first audio, 7.95 s spoken): W porządku, nie musisz wiedzieć od razu. To, że mówisz „nie wiem”, pokazuje, że jesteś w środku tego napięcia i próbujesz to zrozumieć.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.61 s to first audio, 15.7 s spoken): Rozumiem, to brzmi jak lęk przed tym, że odmówienie to odrzucenie. Często rodzi się tam myśl, że warto się zgodzić, bo inaczej “nie pasujesz”. To może być ciężka historia o byciu wystarczająco dobrym, nie tylko o samym projekcie.

#### r6-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.92 s to first audio, 1.65 s spoken): Hey Tom, nice to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.75 s to first audio, 11.2 s spoken): That sounds heavy, like you feel behind them and compare yourself to them. Sometimes the thing you’re really wrestling with isn’t being wrong, it’s noticing you’re still figuring your own path out.
- *Person*: I don't know.
- **Orca 3** (0.73 s to first audio, 8.9 s spoken): I hear you, it feels like there’s a lot happening with no clear answer. Maybe you’re juggling comparison and uncertainty at the same time.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.72 s to first audio, 19.3 s spoken): I heard that it hurt, seeing big steps like getting engaged and buying a place while you’re still renting with flatmates. It really makes you compare fast. I wonder if you’re sitting with a mix of pride for them, jealousy, and worry for yourself. That’s a lot to carry alone.
- *Person*: What do you think I should do?
- **Orca 5** (0.87 s to first audio, 9.6 s spoken): I can’t tell you exactly what to do, that’s really for your therapist. But I’m curious what you’d want to say to them about this, and what feels most important.

#### r6-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.61 s to first audio, 3.65 s spoken): Hi Tom, it’s nice to hear from you. I’m here to listen.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.57 s to first audio, 10.25 s spoken): It sounds like you’re comparing yourself to others, and it feels heavy. That’s a tough spot, and I’m guessing you’re hoping to have your own direction, not just their success.
- *Person*: I don't know.
- **Orca 3** (0.64 s to first audio, 9.0 s spoken): I hear the uncertainty and that “I don’t know” feeling. Maybe you’re noticing something missing in the picture you’re holding, and you’re not sure what belongs there next.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.57 s to first audio, 12.6 s spoken): That must sting a bit, and it’s hard when others’ steps feel louder than your own. My guess is that you’re not jealous of them, but tired of feeling like you’re behind, and wondering what your own next step even is.
- *Person*: What do you think I should do?
- **Orca 5** (0.72 s to first audio, 24.6 s spoken): Okay, let me think about how to respond in a gentle, practical way.I can’t give you a do or don’t list, but I can share what I’d say honestly: this is a personal snapshot, not a measure of who you are. It belongs with your therapist, and you can say what matters to you about it when you talk with them. What would you want to say to your therapist about this feeling, or the comparison?

#### r6-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.83 s to first audio, 3.75 s spoken): Tom, what feels like the hardest part of calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.78 s to first audio, 11.15 s spoken): It sounds like you want to reach out, but evenings slip away before you can. Maybe there’s something quietly pulling you off track, like the tiredness or the day’s noise.
- *Person*: I don't know.
- **Orca 3** (0.8 s to first audio, 8.85 s spoken): It sounds like you’re feeling unsure, like the whole thing feels a bit foggy. Maybe you’re feeling the weight of other stuff too, and it’s just showing up as “I don’t know.”
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.7 s to first audio, 13.8 s spoken): That sounds like a real pattern: you meet him there, but the deeper stuff stays off the table. Maybe, just maybe, you want that part to be part of the relationship, even if it feels awkward or messy to start.

#### r6-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.67 s to first audio, 4.55 s spoken): What’s one small thing that makes calling your dad feel easier or harder?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.6 s to first audio, 10.7 s spoken): Sounds like the evenings slip by before you get to it. Maybe you’re not avoiding the call so much as you’re running out of time and you want that connection to feel on your terms, not rushed.
- *Person*: I don't know.
- **Orca 3** (0.63 s to first audio, 10.1 s spoken): That’s honest. You’re not sure yet, and that’s okay. It might be worth noticing what really blocks the moment, whether it’s energy, timing, or something else.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.54 s to first audio, 11.05 s spoken): I hear a pattern there, like you connect through football and skip that more vulnerable stuff. It’s a guess, but maybe talking about your mum feels more emotional than you want to carry in that setting.

#### r6-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.93 s to first audio, 2.9 s spoken): Cześć, Alex, miło mi Cię poznać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.69 s to first audio, 8.4 s spoken): To brzmi jak moment zawahania. Może chcesz po prostu wybrać coś, co teraz cię najbardziej drapie, a resztę dopłyniesz po drodze.
- *Person*: nie wiem
- **Orca 3** (0.87 s to first audio, 13.2 s spoken): Hmm, czuję, że to może być bardziej o poczuciu braku kierunku niż o braku słów. Może to jest moment, w którym trzeba się tylko zatrzymać i posłuchać, co samo się wyłoni, bez pośpiechu.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.75 s to first audio, 10.65 s spoken): Słyszę, że czujesz niepewność, jakby zmiany w pracy przesuwały grunt pod Tobą. Możesz to zobaczyć jako sygnał, że coś się klaruje, nawet jeśli jeszcze nie widzisz gdzie dokładnie.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.85 s to first audio, 9.7 s spoken): Jestem maszyną i nie mogę Ci powiedzieć, co zrobić, bo to jest coś dla Twojej terapii. Mogę tylko zapytać, co chciałabyś powiedzieć Twojemu terapeucie.

#### r6-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.65 s to first audio, 4.0 s spoken): Cześć, Alex, miło Cię słyszeć. Powiedz, kiedy chcesz zacząć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.62 s to first audio, 13.55 s spoken): Brzmi, że czujesz trochę pustą zerwę i chcesz tylko znaleźć właściwy początek. Możesz mi powiedzieć, co najmniej przeszkadza albo co trochę drapie, a potem zobaczymy, co z tego ułożyć.
- *Person*: nie wiem
- **Orca 3** (0.57 s to first audio, 15.2 s spoken): Brzmi, że naprawdę nie jesteś tego pewniony. To może być sygnał, że gdzieś w środku masz sporo myśli, ale jeszcze nie nazwałeś ich po kolei. Mogę tylko zgadywać, co jest ważne, i próbować doprecyzować to razem z Tobą.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.62 s to first audio, 11.25 s spoken): Słyszę, że te zmiany w zespole to dla Ciebie niewiadoma. Masz w głowie pytanie o miejsce, które może się zmienić. Brzmi to jak moment, kiedy czujesz lekką niepewność.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.64 s to first audio, 21.0 s spoken): Jasne, pomyślmy o tym spokojnie. Daj mi chwilę, żeby się nad tym zastanowić.To pytanie leży bardziej u Twojego terapeuty niż u mnie. To, co zrobiłbym na Twoim miejscu, nie jest dla mnie właściwą odpowiedzią, ale mogę powiedzieć, że dobrze byłoby sprawdzić, co chcesz powiedzieć terapeucie. Co chcesz im przekazać?

#### r6-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (1.05 s to first audio, 5.65 s spoken): Co najbardziej w tych zmianach w pracy, daje ci do myślenia, na co chcesz zwrócić uwagę?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.82 s to first audio, 9.9 s spoken): Słyszę, że to dla ciebie chwiejne i trochę niepewne, co teraz się dzieje. Ktoś odchodzi, a reorganizacja może zrywać poczucie stabilności w pracy.
- *Person*: nie wiem
- **Orca 3** (0.85 s to first audio, 9.75 s spoken): Niepewność jest spora, ale też pokazuje, że coś w tym wszystkim jest niezgadzone. Może to chodzi o to, że tracisz poczucie kontroli, a nie samo odejście.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.79 s to first audio, 8.35 s spoken): Słyszysz, że to bez słów robi większy ciężar niż same zmiany. Brak jasności bywa irytujący, bo trudno przewidzieć, co będzie dalej.

#### r6-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.99 s to first audio, 5.5 s spoken): Alex, co teraz w pracy wygląda dla Ciebie jak największa zmiana, którą odczuwasz?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (1.08 s to first audio, 10.5 s spoken): Brzmi, jakby reorganizacja i częste odejścia robią teraz dużo zamieszania. Może chodzi o to, że czujesz niepewność i rosnącą presję, choć nikt wprost tego nie mówi.
- *Person*: nie wiem
- **Orca 3** (0.82 s to first audio, 11.8 s spoken): Niepewność wisi w powietrzu, a ty możesz nawet nie umieć nazwać, co dokładnie boli. To może być mieszanka strachu, złości i zmęczenia, które trudne jest poukładać szybko.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.75 s to first audio, 8.0 s spoken): Słyszę, że brakuje Ci informacji, a to bardzo frustrujące. Czasem cisza jest gorsza niż same trudne wieści.
