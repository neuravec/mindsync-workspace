24 conversations, estimated cost USD 0.64 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r4-v3-mini | gpt-realtime-mini | none | fresh | 6 | 5/6 | 5/6 | 6/6 | n/a | n/a | 5/6 | 3/6 | 1/6 | 4/6 | 2/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 2/4 | 4/4 | 3/6 | 3/6 | 0.71 | 1.9 | 0.66 | 0.92 | 6.1 | 170 | 47/123/0 | 0 | 0 | 0 | 0.0214 |
| r4-v3-mini | gpt-realtime-mini | none | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 2/6 | 2/6 | 5/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 2/4 | 4/4 | 4/6 | n/a | 0.78 | 1.9 | 0.61 | 0.98 | 6.3 | 171 | 45/125/0 | 0 | 0 | 0 | 0.0177 |
| r4-v3-21mini-low | gpt-realtime-2.1-mini | low | fresh | 6 | 6/6 | 3/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 3/4 | 6/6 | 6/6 | 3/6 | 2/6 | 5/6 | 2/4 | 4/4 | 6/6 | 4/6 | 0.17 | 3.2 | 0.70 | 1.23 | 15.1 | 429 | 126/302/29 | 4 | 4 | 2 | 0.0369 |
| r4-v3-21mini-low | gpt-realtime-2.1-mini | low | seeded | 6 | n/a | n/a | n/a | 5/6 | 6/6 | 5/6 | 4/6 | 4/6 | 5/6 | n/a | 6/6 | 6/6 | 5/6 | 5/6 | 5/6 | 3/4 | 4/4 | 6/6 | n/a | 0.22 | 3.1 | 0.68 | 0.91 | 16.1 | 446 | 123/323/25 | 1 | 1 | 3 | 0.0304 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r4-v3-mini | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | none | 0 | 1 | none | none | none |
| r4-v3-mini | R1 | fresh | 2 | FAIL | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | Mówiłaś, chciałabyś | none | none |
| r4-v3-mini | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś czuła, miałaś, mogłabyś | none | none |
| r4-v3-mini | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś czuła, jakbyś starała | none | none |
| r4-v3-mini | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r4-v3-mini | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r4-v3-mini | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r4-v3-mini | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r4-v3-mini | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | none | 0 | 1 | none | byś chciał | none |
| r4-v3-mini | T1 | fresh | 2 | pass | FAIL | pass | n/a | n/a | FAIL | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | FAIL | none | 0 | 0 | none | chciałbyś, jakbyś czuł | none |
| r4-v3-mini | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | n/a | none | 0 | 0 | none | jakbyś czuł | none |
| r4-v3-mini | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 1 | none | Jakbyś miał | none |
| r4-v3-21mini-low | R1 | fresh | 1 | pass | FAIL | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | Daj mi chwil | 0 | 0 | chciałabyś, jakbyś czekała, zaczęłaś | none | none |
| r4-v3-21mini-low | R1 | fresh | 2 | pass | FAIL | pass | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | Daj mi chwil | 0 | 0 | chciałabyś, jakbyś już czuła | none | none |
| r4-v3-21mini-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | FAIL | FAIL | pass | pass | pass | pass | n/a | Daj mi chwil | 0 | 1 | jakbyś się zmuszała | none | none |
| r4-v3-21mini-low | R1 | seeded | 2 | n/a | n/a | n/a | FAIL | pass | FAIL | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | powiedziałaś | none | none |
| r4-v3-21mini-low | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r4-v3-21mini-low | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | pass | n/a | n/a | pass | pass | let me think | 0 | 0 | none | none | none |
| r4-v3-21mini-low | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r4-v3-21mini-low | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 1 | none | none | none |
| r4-v3-21mini-low | T1 | fresh | 1 | pass | FAIL | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | FAIL | pass | FAIL | pass | pass | FAIL | none | 0 | 0 | none | odezwałeś | none |
| r4-v3-21mini-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | FAIL | none | 0 | 0 | none | jakbyś był, jakbyś trzymał | none |
| r4-v3-21mini-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |
| r4-v3-21mini-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 0 | jakbyś stała | none | none |

### Transcripts

#### r4-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.85 s to first audio, 2.1 s spoken): Cześć, miło słyszeć Cię.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.5 s to first audio, 9.45 s spoken): Czuję, że to cię mocno obciąża [en dash] jakby te myśli o pracy już się zaczynały wkradać w wieczór. Może coś jest w tym, jak wyobrażasz sobie początek dnia jutrzejszego?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.51 s to first audio, 6.8 s spoken): Wygląda na to, że ciąży ci ta niepewność jutra. Może to z tego wynika, że nie masz jeszcze planu, jak sobie z tym poradzić.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.68 s to first audio, 6.05 s spoken): Słyszę, że czujesz ciężar z powodu tego, co się dzieje w pracy. Czy to jest to, co najbardziej cię teraz obciąża?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.5 s to first audio, 8.1 s spoken): To może być warto spróbować, ale najpierw warto poczuć, co dokładnie chcesz przekazać. Możesz spróbować zastanowić się, co konkretnie chcesz powiedzieć.

#### r4-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.92 s to first audio, 3.0 s spoken): Cześć, Aniu. Czym chciałabyś się teraz zająć?
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.67 s to first audio, 8.2 s spoken): Czuję, że to cię mocno obciąża, jakby ciężar pracy już teraz cię doganiał. Jak ci się wydaje, czego najbardziej się obawiasz jutro?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.72 s to first audio, 8.45 s spoken): Mówiłaś, że jest ciężko, i może to o to, że te myśli już się zaczynają wkradać. Powiedz, co w tym wszystkim czuje się najtrudniejsze?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.68 s to first audio, 10.65 s spoken): Rozumiem, czujesz, że teraz czujesz to obciążenie, które przyszło nagle. Możliwe, że boisz się, co będzie, jeśli nie wyrazisz sprzeciwu. Tylko czy to prawda, że boisz się konsekwencji?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.67 s to first audio, 7.55 s spoken): To zależy, bo ważne jest, żebyś poczuła, że masz na to przestrzeń i sposób, który ci pasuje. Chcesz spróbować to ująć łagodnie?

#### r4-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.82 s to first audio, 4.0 s spoken): Co teraz czujesz, gdy myślisz o odmawianiu przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.62 s to first audio, 6.25 s spoken): To brzmi tak, jakbyś czuła, że nie miałaś miejsca, żeby powiedzieć nie. Jakie emocje się w tobie wtedy pojawiły?
- *Person*: nie wiem
- **Orca 3** (0.51 s to first audio, 7.45 s spoken): Może to jest coś, co czujesz bardziej w ciele niż w słowach. Czy mogłabyś powiedzieć, gdzie dokładnie czujesz ten ciężar?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.5 s to first audio, 8.1 s spoken): Obawiasz się, że odmowa może sprawić, że zobaczy Cię w innym świetle. Może podłożem jest lęk przed oceną. Jak myślisz?

#### r4-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.51 s to first audio, 3.9 s spoken): Co zazwyczaj powstrzymuje Cię, żeby powiedzieć „nie” przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.48 s to first audio, 10.4 s spoken): Brzmi jakbyś czuła się przytłoczona i trochę nie miała siły wypowiedzieć tego „nie”. To tak, jakbyś starała się nie obarczać innych, nawet kosztem siebie. Czy to na pewno tak?
- *Person*: nie wiem
- **Orca 3** (0.43 s to first audio, 7.55 s spoken): Ok, to może to jest chwila, żeby zastanowić się, co czujesz pod tym. Możesz spróbować opisać chwilę, gdy przyszło to pierwsze „tak”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.43 s to first audio, 6.15 s spoken): Czyli pod spodem jest lęk przed oceną, że nie będziesz wystarczająco dobra. To ważne, żeby to zauważyć.

#### r4-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.67 s to first audio, 2.35 s spoken): Hi Tom, good to have you here.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.68 s to first audio, 5.45 s spoken): It sounds like you’re feeling a lot of pressure, especially when comparing. There's a weight to that feeling.
- *Person*: I don't know.
- **Orca 3** (0.64 s to first audio, 7.0 s spoken): It sounds like you’re not entirely sure where that thought is coming from. Maybe there’s something specific you’re comparing yourself to?
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.52 s to first audio, 4.25 s spoken): That sounds like it’s hitting hard, especially when you feel the difference so clearly.
- *Person*: What do you think I should do?
- **Orca 5** (0.66 s to first audio, 7.5 s spoken): That’s something to explore with your therapist, and it might help to ask yourself what feels most important to you right now. What would you want to say to them?

#### r4-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.85 s to first audio, 2.35 s spoken): Hi Tom, good to connect with you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.67 s to first audio, 6.6 s spoken): That feeling of being behind, like everyone else knows what they're doing, really weighs on you. There’s a lot in that.
- *Person*: I don't know.
- **Orca 3** (0.52 s to first audio, 6.05 s spoken): It sounds like you're unsure where that feeling is coming from. Maybe there’s something deeper you’re not sure about.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.69 s to first audio, 4.85 s spoken): That’s a big difference, and it makes sense that it’s sticking with you, especially when you compare.
- *Person*: What do you think I should do?
- **Orca 5** (0.63 s to first audio, 6.35 s spoken): That’s something that’s best to explore with your therapist. But I’m curious[em dash]what’s one thing you wish you could say to them about how you feel?

#### r4-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.78 s to first audio, 2.5 s spoken): What’s on your mind about calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.67 s to first audio, 4.6 s spoken): It sounds like the time just slips away, and you end up running out of moments.
- *Person*: I don't know.
- **Orca 3** (0.77 s to first audio, 8.15 s spoken): That's okay. We can stay with that a bit. Maybe there's something about the evening slipping away[em dash]like what’s happening before it feels like it’s gone?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.98 s to first audio, 7.25 s spoken): So it’s easier to talk about football than to go deeper into how he’s feeling about your mum. That’s something you both might be avoiding.

#### r4-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.64 s to first audio, 3.25 s spoken): What’s been stopping you from calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.43 s to first audio, 7.95 s spoken): It sounds like your evenings slip away quickly. Maybe there’s something about how the timing of your day is set. Would it help to set a reminder earlier?
- *Person*: I don't know.
- **Orca 3** (0.44 s to first audio, 6.05 s spoken): That’s okay. It’s worth noticing that the time just slips by. What do you think makes it hard to start the call?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.43 s to first audio, 4.4 s spoken): So it feels like you're missing that deeper connection. Is that what you’re noticing?

#### r4-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.72 s to first audio, 2.8 s spoken): Cześć, Alex. Czekam, co chcesz powiedzieć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.66 s to first audio, 4.7 s spoken): Czyli czujesz, że jest trochę pustki, coś się pojawia, ale trudno wskazać?
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 5.0 s spoken): Spróbujmy to rozłożyć na kawałki. Czy coś konkretnie zaczęło Cię niepokoić?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.74 s to first audio, 7.05 s spoken): Widzę, że to jest spory ciężar [en dash] niepewność, czy zostaniesz w zespole. To jest coś, co teraz bardzo Cię obciąża, prawda?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.59 s to first audio, 5.2 s spoken): To pytanie pasuje do rozmowy z terapeutą. A teraz, co byś chciał powiedzieć swojemu zespołowi?

#### r4-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.76 s to first audio, 4.8 s spoken): Cześć, Alex. Już cię słyszę. Możesz zacząć, kiedy będziesz gotowy.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.6 s to first audio, 7.25 s spoken): Jasne, odczuwasz, że jest kilka rzeczy naraz do przemyślenia, tak? Może chcesz zacząć od tego, co cię teraz najbardziej obciąża?
- *Person*: nie wiem
- **Orca 3** (0.66 s to first audio, 5.9 s spoken): To w porządku, możemy po prostu posłuchać chwilę, zobaczyć, co się pojawi. Czego chcesz w tej chwili?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.6 s to first audio, 8.35 s spoken): Brzmi, jakbyś czuł się trochę niepewnie, nie wiedząc, jak potoczą się te zmiany. Czy to jest ten moment, w którym myślisz o tym, co chcesz zrobić dalej?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.58 s to first audio, 9.95 s spoken): Ja nie jestem w stanie podjąć za ciebie decyzji, ale warto może zastanowić się, jakie masz fakty, co czujesz i co chciałbyś, żeby się stało. Co chciałbyś powiedzieć swojemu zespołowi?

#### r4-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.75 s to first audio, 3.5 s spoken): Co aktualnie czujesz, myśląc o tych zmianach w pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.65 s to first audio, 6.5 s spoken): Brzmi, jakbyś czuł sporo niepewności, bo zmiany są bardzo częste. Jak na to reagujesz, odkąd to trwa?
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 8.35 s spoken): Może jest coś, co czujesz, choć trudno to nazwać [en dash] mogę spróbować to dopasować. Jak myślisz, co mogłoby być najbliżej tego, co się dzieje w Tobie?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.69 s to first audio, 8.05 s spoken): Czyli czujesz większe napięcie przez tę niejasność. Może warto spróbować zastanowić się, czego potrzebujesz, żeby poczuć się pewniej?

#### r4-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.68 s to first audio, 3.2 s spoken): Co teraz najbardziej cię w tych zmianach w pracy zajmuje?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.61 s to first audio, 5.3 s spoken): Widzę, że to jest spory stres, bo ciągle ktoś odchodzi. Jak to na ciebie wpływa?
- *Person*: nie wiem
- **Orca 3** (0.53 s to first audio, 8.2 s spoken): Może coś w tym jest, bo nie czujesz jasno, co się w tym momencie dzieje dla ciebie. Czy chcesz porozmawiać o tym, co być może najbardziej cię niepokoi?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.56 s to first audio, 9.4 s spoken): Czyli to, co najbardziej uderza, to ta niepewność i brak jasnych informacji. Jakbyś miał spróbować nazwać to, co czujesz z tą niepewnością, co by to było?

#### r4-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.57 s to first audio, 5.4 s spoken): Cześć, Ania. Miło mi się z Tobą spotkać.Cześć, Ania. Miło mi się z Tobą spotkać.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.69 s to first audio, 16.3 s spoken): Brzmi, że niedziela otwiera drzwi do pracy, nawet gdy jeszcze jej nie zaczęłaś. Możliwe, że chodzi o napięcie przed listą zadań i o to, co będzie miała przynieść. A może to moment, kiedy trochę się wyciszasz, zanim znów zacznie się wir.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.63 s to first audio, 22.65 s spoken): To brzmi jak takie ciężkie zawahanie, jakby dzień już wchodził w drzwi, a ty po prostu jesteś w środku tego ciężaru. Daj mi chwilę, myślę, że to może być poczucie odpowiedzialności albo nadziei, że dasz radę być idealna. Nie próbuj teraz niczego naprawiać, po prostu zauważ, że jest ciężko, i jakbyś czekała, aż to trochę opadnie.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.6 s to first audio, 11.3 s spoken): To brzmi, jakbyś w piątek dostała coś na głowę, a potem został Ci brak słowa „stop”. To też brzmi jak coś, co męczy Cię nawet po pracy, bo zostało niedopowiedziane.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.98 s to first audio, 17.75 s spoken): Wiesz, to nie jest decyzja, którą mogę za Ciebie podjąć. To raczej temat dla Twojego terapeuty. Mogę za to pomóc Ci ułożyć słowa, które chciałabyś mu powiedzieć, albo nawet pomyśleć, co patrzy na Ciebie z tyłu głowy, gdy mówisz o granicach. Powiedz mi, czy chcesz, żebym sformułowała coś prostego.

#### r4-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.69 s to first audio, 7.15 s spoken): Cześć, Ania. Miło, że zaczynasz. Jestem tu, żeby posłuchać, jak mówisz i pomóc rozłożyć myśli na spokojnie.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.62 s to first audio, 9.75 s spoken): Brzmi, jakbyś już czuła się w tym momencie wprowadzona w wir jutra. A może to też chęć, żeby teraz na chwilę być tutaj, zanim zacznie się dzień w pracy.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.63 s to first audio, 11.75 s spoken): Myślę, że to ciężkość, która nie ma jednego konkretnego powodu, a raczej narasta z wielu drobnych rzeczy na raz. Możesz sobie tylko uświadomić, że to jest teraz, i że to mija.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.64 s to first audio, 25.0 s spoken): To jest frustrujące, kiedy ktoś dodaje kolejna rzecz, a ty czujesz się jednocześnie zobowiązana i trochę bez litości dla siebie. Możesz się domyślać, że to poczucie, że odmawianie kogoś może kosztować relację albo utratę dobrej opinii. Jeśli chcesz, możemy spróbować skupić się tylko na jednym zdaniu, co było trudne i co było ważne, i zastawić klocki, bez planu całej rozmowy.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.23 s to first audio, 26.45 s spoken): Daj mi chwilę, żeby ułożyć to spokojnie i powiedzieć, co naprawdę o tym myślę.Myślę, że wprost jest uczciwe. To może brzmieć trochę twardo, ale też daje jasność. Oczywiście ważna jest forma i moment, ale nie sam akt mówienia. Czuję, że to temat, który najlepiej omówić z terapeutą, bo to pomaga dobrać słowa do Twojej sytuacji. Co chciałabyś mu powiedzieć, gdybyś miała wybór?

#### r4-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.67 s to first audio, 5.35 s spoken): Ania, kiedy próbujesz odmówić przełożonemu, co jest dla ciebie najtrudniejsze?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.61 s to first audio, 12.15 s spoken): Brzmi, jakbyś się zmuszała, nawet kiedy czujesz, że brakuje siły. To może być ta część pracy, gdzie grasz rolę „spokojnej” albo „elastycznej”, a potem czujesz, że dźwigasz wszystko sama.
- *Person*: nie wiem
- **Orca 3** (0.75 s to first audio, 25.85 s spoken): Zrozumiałam, że jesteś trochę zagubiona. Daj mi chwilę, żeby to spokojnie ująć.To brzmi trochę jak „nie mam pewności, co dokładnie czuję i co z tego wynika”. Czasem to niepewność jest właśnie sygnałem, że coś w tej decyzji boli, nawet jeśli nie umiesz jeszcze nazwać tego wprost. Może jesteś właśnie w środku tego momentu, gdzie chcesz spróbować inaczej, ale nie wiesz, co to by było.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.64 s to first audio, 14.35 s spoken): Rozumiem, to brzmi jak strach przed oceną i odrzuceniem, skoro jeden brak zgody może brzmieć „nie nadajesz się”. To uczucie może pojawić się nawet wtedy, gdy w głębi serca jesteś zmęczona i chcesz granic.

#### r4-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.74 s to first audio, 7.75 s spoken): Ania, jak to teraz brzmi, kiedy mówisz o odmawianiu przełożonemu? Co robi różnicę, gdy próbujesz powiedzieć „nie”?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.65 s to first audio, 28.85 s spoken): Brzmi, jakbyś już w środku czuła, że nie dasz rady, ale dalej powiedziałaś „tak”. To musi być męczące, kiedy ciało mówi „dość”, a głos w głowie mówi „nie mogę zawieść”.

Moją zgadką jest, że chodzi też o to, że chcesz być słyszalna, ale boisz się, że zadręczysz coś albo stracisz zaufanie. Jeśli to trafia, to słucham, co z tego czujesz, i możemy po prostu zatrzymać się nad tą granicą: co jest dla ciebie ważne, a co już jest ponad twoje siły.
- *Person*: nie wiem
- **Orca 3** (0.75 s to first audio, 10.5 s spoken): To jest okej. Nie wiesz, więc weźmy to po kawałku. Możesz tu zostać w tym „nie wiem” bez presji. Czasem sam moment zastanowienia się jest granicą, której potrzebujesz.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.79 s to first audio, 25.05 s spoken): Rozumiem ten lęk, jakby odmowa była testem, czy się nadajesz. Twoja myśl sugeruje, że odmowa mogłaby być końcem, a nie początkiem innego układu. Może chodzi o poczucie bezpieczeństwa, o to, że chcesz być pewna, że jesteś warta zaufania, nawet gdy masz dość. Jeśli chcesz, możemy na razie popatrzeć, co w tej myśli jest granicą, a co jest opowieścią, którą masz podjąć.

#### r4-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.85 s to first audio, 4.05 s spoken): Hey Tom, nice you’re here. Just a quick hello, and I’ll wait for you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.77 s to first audio, 12.0 s spoken): That sounds heavy. It feels like you’re measuring yourself against everybody else, and that weight shows up on rough mornings like this. And it makes you feel like you’re behind in a big way, even if it’s just a pattern you’re noticing today.
- *Person*: I don't know.
- **Orca 3** (0.77 s to first audio, 11.8 s spoken): Got you. You’re not sure what to say next, and that’s okay. My guess is you’re tired of putting yourself under that spotlight, and you’re just looking for a little space to think out loud without being judged.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.72 s to first audio, 15.0 s spoken): That’s a sharp comparison point. You’re noticing the milestone they hit, and you’re still in a different situation, which can feel like a direct measure. My guess is you’re holding both things at once: their good news, and your own worry that you’re behind.
- *Person*: What do you think I should do?
- **Orca 5** (0.82 s to first audio, 11.4 s spoken): Honestly, this kind of tug-of-war is really common. I can’t tell you what to do, though. That’s something for you and your therapist to untangle together. What feels most important to say to them right now?

#### r4-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.7 s to first audio, 2.1 s spoken): Hey Tom, nice to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.68 s to first audio, 11.1 s spoken): That sounds heavy, like you’re measuring yourself against others, and coming up short. It’s a common feeling, not a fact about you right now, and it can really sting when it shows up in the morning.
- *Person*: I don't know.
- **Orca 3** (0.59 s to first audio, 15.05 s spoken): You’re not sure what to make of this feeling yet, and that can be confusing. Maybe you’re holding a bunch of worries and comparisons without knowing where to place them. If it helps, you can just say what’s closest to the surface, and we’ll go from there.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.63 s to first audio, 17.9 s spoken): Oof, that hits. It sounds like you’re comparing your life to theirs, and it feels like you’re coming up short. Still renting, sharing space, and watching someone move ahead can really sting, and it can make you wonder if you’re falling behind. But you’ve got your own pace and your own priorities, even if they’re different.
- *Person*: What do you think I should do?
- **Orca 5** (0.61 s to first audio, 22.35 s spoken): Okay, let me think this through with you for a moment.I can’t tell you what to do, that’s a job for your therapist and your own judgment. But I can share a thought: noticing the comparison pop up is already helpful. It’s not a sign you’re failing, it’s a signal you’re paying attention to what matters to you.

If you want, tell me what you’d actually want to say to someone like your therapist or a close friend about this.

#### r4-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.58 s to first audio, 3.45 s spoken): What’s it like when you think about calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.76 s to first audio, 22.7 s spoken): Sounds like you’ve got good intentions, but the timing just keeps slipping away. Evenings can be sneaky like that, full of little demands and distractions. My guess is that your heart wants to connect, but your evenings feel like a blur that drains the window between intention and action. Would you want to share what the evening looks like on a typical day?
- *Person*: I don't know.
- **Orca 3** (0.72 s to first audio, 19.45 s spoken): Thanks for saying that, really. It sounds like you’re not sure what the evenings mean for you, and you probably haven’t had enough space to notice. My guess is it’s not just the time, but the mental load, the “I’ll do it later” feeling kicking in. If you’re not sure, let’s just sit with that. We can sort through it together, piece by piece.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.91 s to first audio, 19.2 s spoken): You’re noticing a pattern: when you do talk, the conversation stays around football, and you haven’t felt like you can bring up your mum. My guess is that it’s not just the topic, but the emotional weight, and maybe you’re worried it’ll be heavy or feel awkward. Would you want to share what part of that feels most uncomfortable for you?

#### r4-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.46 s to first audio, 3.95 s spoken): Hey Tom, what gets in the way when you try to call your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.61 s to first audio, 18.45 s spoken): It sounds like you’ve got a plan in mind, but the evenings slip by before you can act on it. Maybe there’s a part of you that wants to reach out, but the moment it feels like a busy night, it just slips away. I’m curious about what nights feel hardest. Are they the busiest, or do they just feel more like a blur?
- *Person*: I don't know.
- **Orca 3** (0.55 s to first audio, 22.95 s spoken): Yeah, that’s really fair. It feels like you’re not sure what the main blocker is yet. Sometimes it’s the weight of the day, or the effort of making the call, and sometimes it’s just the timing being off. One thing that might help is paying attention to which part is hardest when you’re trying to call. Is it choosing to do it, finding the time, or just getting started?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.66 s to first audio, 20.1 s spoken): That makes sense. It sounds like the chat is safe and familiar, but it stays on the surface. I’d guess that you want to connect, but the emotional part feels heavier, like if you mention your mum, you’re opening something you’re not sure how to hold. If that’s right, we can leave it there for now. You don’t have to fix it; just noticing it is a big step.

#### r4-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.74 s to first audio, 5.2 s spoken): Cześć, Alex. Miło, że się odezwałeś. Jestem tu i gotowy, żeby słuchać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.58 s to first audio, 19.3 s spoken): Okej, słyszę, że jesteś trochę w rozterce i nie wiesz, od czego zacząć. To całkiem normalne. Możemy to zrobić na spokojnie. Powiedz, co w tej chwili jest najmocniejsze w Twoich myślach, a ja pomogę Ci to uporządkować. Jak pojawi się jasność, zobaczymy dalej.
- *Person*: nie wiem
- **Orca 3** (0.59 s to first audio, 28.35 s spoken): Myślę, że kiedy ktoś mówi „nie wiem”, czasem chodzi o to, że wiele rzeczy naraz robi hałas w głowie. Może to być duże coś, ale też małe, niezauważone. Mogę tylko zgadnąć, że szukasz kierunku i trochę tablicy, na której można rozłożyć to, co teraz ważne. Powiedz, czy to raczej coś, co cię dręczy, czy coś, co czeka na swoją kolej. jeśli chcesz, możemy zacząć od tego „cicho dręczącego” i zobaczyć, co wyłoni się jako pierwsze.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.49 s to first audio, 24.4 s spoken): To brzmi jak coś, co trzyma Cię w napięciu. Zmiany w pracy potrafią być głuche, ale też widać je w codziennym stresie. Może chodzi o pytanie, czy jesteś częścią tego, co dopiero się układa, czy już w innej stronie? Mogę tylko zgadnąć, że chcesz wiedzieć, czy zostać i gdzie, więc być może warto zacząć od tego, co możesz kontrolować tu i teraz, a potem zobaczyć, co przyniesie kolejne dni.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.75 s to first audio, 33.0 s spoken): Jasne, zwięźle: nie mogę udzielać Ci konkretnych porad, ale mogę powiedzieć, co, moim zdaniem, widzę pod tym wszystkim. Masz w głosie sporo niepewności, a też jakby pragnienie stabilności, czyli wiedzieć, gdzie się stoi i że kolejne zmiany nie są dla Ciebie szokiem. To mogłoby wskazywać, że pod powierzchnią niepewności jest chęć poczucia kontroli i spokoju. Mogę się mylić, więc jeśli chcesz, możesz powiedzieć, co dokładnie leży w tej niepewności, a ja pomogę to rozświetlić, ale tego planu nie narzucę.

#### r4-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.6 s to first audio, 3.2 s spoken): Cześć, Alex. Miło, że zaczynamy tę rozmowę.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.63 s to first audio, 12.65 s spoken): Jednym sposobem jest wybrać ten moment, który najmocniej cię rozgrzewa albo trochę wkurza. Nie musisz ogarniać wszystkiego naraz. Możemy zacząć od tego, co jest teraz najbardziej obecne w głowie.
- *Person*: nie wiem
- **Orca 3** (0.59 s to first audio, 17.8 s spoken): W porządku, to też jest wystarczająco dużo, żeby coś nazwać. Mogę zgadnąć, że to nie chaos, tylko uczucie, że nie chcesz wybrać, bo wszystko wydaje się ważne naraz. Jeśli to przeczucie jest blisko tego, spróbujmy zacząć od jednego drobnego szczegółu, tego co dziś trochę ciąży.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.6 s to first audio, 13.0 s spoken): Brzmi tak, jakbyś był, albo była, w miejscu, gdzie czujesz, że nie masz kontroli nad tym, co się dzieje wokół. Zmiany są na wierzchu, a ty trzymasz kciuki, żebyś został w zespole. To jest dużo napięcia naraz.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.89 s to first audio, 20.1 s spoken): Nie mogę ci powiedzieć, co masz zrobić, bo to nie jest moja rola. Mogę ci jednak powiedzieć, że to, co brzmi, jakbyś trzymał, trzymała w dłoni, to poczucie, że musisz wziąć odpowiedzialność za coś, na co nie masz wpływu. To może być prawdziwe. A co należałoby powiedzieć naszym wspólnym rozmówcom, czyli twojemu terapeucie albo zespołowi?

#### r4-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.75 s to first audio, 3.75 s spoken): Jakie zmiany w pracy teraz dają Ci najwięcej do myślenia?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.85 s to first audio, 23.75 s spoken): Brzmi, że ta zmienność w pracy zaczyna być przytłaczająca. Odejścia ludzi mogą robić wrażenie, że coś się osłabia, a nie że idzie do przodu. Kiedy ludzie się zmieniają, zostaje trochę niepewności i pytanie, co dalej. Jeśli chcesz, mogę zostawić to jako punkt do przemyślenia, albo możesz po prostu powiedzieć, co z tego teraz jest dla Ciebie najtrudniejsze.
- *Person*: nie wiem
- **Orca 3** (0.77 s to first audio, 22.0 s spoken): To normalne, że nie masz teraz pewności. Czasem w takich sytuacjach człowiek stoi w środku zmiany i dopiero później układa sobie to w głowie. Może to, co teraz trudne, to brak stałej, albo poczucie, że nie masz kontroli. Jeśli chcesz, mogę pomyśleć z Tobą o tym, gdzie w tym wszystkim jest coś, co chcesz utrzymać, nawet w małej skali.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.68 s to first audio, 22.95 s spoken): Rozumiem, że to najbardziej ciężkie. Kiedy nikt nie mówi wprost, pojawia się ta dziwna mieszanka nadziei i strachu, że coś jest nie tak, ale nikt tego nie nazwie. To może być właśnie to, co najbardziej dręczy, ta niepewność. Jeśli chcesz, możemy dalej posłuchać, co tam pod spodem leży: co Cię męczy, a co w tej sytuacji kurczy siły.

#### r4-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.6 s to first audio, 4.35 s spoken): Jakie zmiany w pracy są teraz najbardziej słyszalne dla Ciebie?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.56 s to first audio, 10.85 s spoken): Brzmi jak dużo ruchu i niepewności, kiedy ciągle ktoś znika z zespołu. To sali, żeby trzymać się razem i patrzeć, co z tego wszystkiego dla Ciebie wynika.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 21.0 s spoken): Brzmi jak trochę rozbicie, jakbyś stała, czy stał wśród ruchu, który nie daje wyobrażenia, dokąd to idzie. To normalne, że przy takiej „niewiadomej” pojawiają się wątpliwości i chęć schowania się w cień. Możesz zostać przy tym na chwileczkę, a potem zobaczymy, co z tego kawałka da się nazwać.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.55 s to first audio, 18.55 s spoken): To brzmi jak taki cień zawieszony nad wszystkim. Ruchy są, ale nikt nie mówi tego wprost. To może być frustrujące, bo nie wiesz, co jest prawdą, co jest planem, a co tylko domysłami. I choć to nierealne, to w pewnym sensie możesz się zastanawiać, czy coś przeoczajesz.
