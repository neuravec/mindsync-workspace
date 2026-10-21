6 conversations, estimated cost USD 0.07 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | empty openers | line offers | median reply s | max reply s | replies over 16 s | cost per conv USD | USD per agent-minute |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v31-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 3 | 3/3 | 3/3 | 3/3 | n/a | n/a | 3/3 | 3/3 | 3/3 | 2/3 | 1/2 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 1/2 | 2/2 | 2/2 | 3/3 | 2/3 | 0.17 | 1.8 | 0.78 | 1.37 | 7.6 | 223 | 71/151/18 | 0 | 0 | 1 | 0 | 0 | 9.2 | 13.9 | 0/12 | 0.0213 | 0.0338 |
| v31-text | gpt-5.4-mini | none | fresh | 3 | n/a | n/a | n/a | n/a | n/a | 3/3 | 3/3 | 3/3 | 1/3 | 2/2 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/2 | 2/2 | 2/2 | 3/3 | 3/3 | 0.25 | 2.1 | n/a | n/a | n/a | 47 | n/a | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | 0.0034 | n/a |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v31-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | jakbyś dostała, jakbyś już niosła, weszłaś | none | none |
| v31-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v31-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | FAIL | none | 0 | 0 | jakbyś stała | chciałbyś | none |
| v31-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, chciałaś, wzięłaś | none | none |
| v31-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v31-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |

### Transcripts

#### v31-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.99 s to first audio, 2.1 s spoken): Cześć, miło cię poznać.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (1.37 s to first audio, 8.75 s spoken): To brzmi, że niedziele znów wracają pod ciszę, gdy myślisz o pracy. Wygląda, jakbyś już niosła jutro w głowie, zanim jeszcze przyjdzie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.96 s to first audio, 11.75 s spoken): To brzmi jak napięcie, które jest w tobie teraz, bez konkretnego powodu. Może chodzi o to, że czujesz się zmęczona i niepewna? To tylko zgadywanka, weszłaś w nią bez planu.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (1.1 s to first audio, 5.65 s spoken): Brzmi, jakbyś dostała kolejną dawkę presji i wolała odpuścić niż powiedzieć, że nie.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.86 s to first audio, 11.25 s spoken): To brzmi, że chcesz postawić granicę, ale czujesz, że to może być trudne dla mnie. Jeśli dasz, to warto skonsultować z terapeutą, a potem zobaczyć, co chcesz mu powiedzieć.

#### v31-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.56 s to first audio, 2.75 s spoken): Hi, Tom. It’s nice to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.75 s to first audio, 9.75 s spoken): Those thoughts can feel loud when the morning is heavy. You’re noticing a comparison, and it sounds like you want to feel more steady about where you’re at.
- *Person*: I don't know.
- **Orca 3** (0.54 s to first audio, 5.65 s spoken): It sounds like you’re feeling unsure about where you stand, and that can be a bit unsettling.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.67 s to first audio, 10.2 s spoken): It sounds like you’re comparing your life to others’, and it feels like you’re behind. I guess part of that is the doubt that can sneak in when you’re tired, not just the situation itself.
- *Person*: What do you think I should do?
- **Orca 5** (0.68 s to first audio, 9.7 s spoken): It’s your choice, and that’s the most important part. I can’t tell you exactly what to do, but I’d be curious what you’d want to say to your therapist about this.

#### v31-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.55 s to first audio, 5.05 s spoken): Cześć, miło cię słyszeć. Jestem tu, by towarzyszyć ci w rozmowie.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.81 s to first audio, 6.0 s spoken): To zaczynamy od tego, co na teraz jest najcięższe. Możesz powiedzieć, co najmocniej cię przytłacza.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 5.4 s spoken): Spokojnie, niepewność jest teraz tym, co już czujesz i można ją po prostu nazwać.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.58 s to first audio, 13.95 s spoken): Brzmi, jakbyś stała w miejscu, gdzie dużo się przesuwa, a ty łapiesz oddech i zastanawiasz się, co zrobić dalej. Może chodzi o poczucie stabilności, o to, że nie wiesz, czy zostać, czy ruszyć dalej.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.66 s to first audio, 5.5 s spoken): To należałoby powiedzieć twojemu terapeucie, a nie mi. Co chciałbyś powiedzieć im odnośnie tych zmian?

#### v31-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Ta niedziela znowu cię przyciska, i myśli już uciekają do jutra w pracy. Brzmi to jak ten sam ciężar, który wraca jeszcze zanim tydzień naprawdę się zacznie.  
Może najbardziej nie chodzi o sam poniedziałek, tylko o to, że wiesz, co on zwykle ze sobą przynosi.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Po prostu jest ciężko, bez jednego jasnego powodu do złapania.  
Może teraz bardziej chodzi o zmęczenie tym, że to wraca, niż o samą pracę.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: To wygląda jak kolejny raz, gdy wzięłaś coś na siebie, choć w środku tego nie chciałaś.  
Najbardziej wybrzmiewa tu chyba nie sam projekt, tylko to, jak trudno ci postawić granicę bez poczucia winy.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To należy do ciebie i do tego, co chciałabyś powiedzieć potem na terapii.  
Co chciałabyś mu przekazać?

#### v31-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / fresh / run 1

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like the kind of morning where your mind goes straight to measuring yourself against everyone else, and it lands hard. I’m guessing the rough part is not just the thought, but the feeling of being late to your own life.
- *Person*: I don't know.
- **Orca 2**: That sounds more like you’re not sure what the real bite is yet, just that something feels off. It may be the comparison itself, or the way it hits when you already feel tired.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That would make the gap feel very concrete, not just in your head. It sounds like the hard part is seeing someone close to you hit the markers you keep comparing yourself to, while your own life still feels unfinished.
- *Person*: What do you think I should do?
- **Orca 4**: That belongs with your therapist, not me. What would you want to say to them about this?

#### v31-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Możesz zacząć od tego, co dziś najbardziej siedzi w głowie. Czasem pierwszy kawałek nie musi być ważny, wystarczy, że jest prawdziwy.
- *Person*: nie wiem
- **Orca 2**: Wygląda na to, że teraz jest bardziej pustka niż jedna konkretna rzecz. Jeśli chcesz, możemy zacząć od tego, co jest najbliżej: ciało, myśli albo coś, co wydarzyło się dziś.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak bycie w zawieszeniu, bez jasnego gruntu pod nogami. Chyba najcięższe jest tu nie samo to, co się zmienia, tylko brak pewności, gdzie ty w tym wszystkim stoisz.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To należy omówić z twoim terapeutą. Co chciałoby się tam powiedzieć?
