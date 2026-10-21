24 conversations, estimated cost USD 0.90 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r1-v3-21mini-low | gpt-realtime-2.1-mini | low | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 5/6 | 6/6 | 3/4 | 6/6 | 6/6 | 6/6 | 4/6 | 2/6 | 2/4 | 4/4 | 6/6 | 3/6 | 0.25 | 4.1 | 0.86 | 2.36 | 18.9 | 522 | 143/379/29 | 2 | 2 | 7 | 0.0440 |
| r1-v3-21mini-low | gpt-realtime-2.1-mini | low | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | 5/6 | 5/6 | n/a | 6/6 | 6/6 | 5/6 | 5/6 | 3/6 | 3/4 | 4/4 | 4/6 | n/a | 0.11 | 3.2 | 0.72 | 1.20 | 17.6 | 485 | 133/352/28 | 1 | 1 | 3 | 0.0337 |
| r1-v3-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 5/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 4/6 | 5/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 2/6 | 2/4 | 4/4 | 5/6 | 5/6 | 0.33 | 3.6 | 0.69 | 0.97 | 17.4 | 474 | 126/348/18 | 0 | 0 | 4 | 0.0415 |
| r1-v3-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 4/6 | 3/6 | n/a | 6/6 | 6/6 | 5/6 | 5/6 | 5/6 | 3/4 | 4/4 | 4/6 | n/a | 0.33 | 2.9 | 0.72 | 0.87 | 16.1 | 437 | 116/321/19 | 1 | 1 | 2 | 0.0310 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r1-v3-21mini-low | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | Jakbyś trzymała, poczułaś, przyjęłaś | none | none |
| r1-v3-21mini-low | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | FAIL | none | 0 | 1 | Zajęłaś, chciałabyś, jakbyś wróciła | none | none |
| r1-v3-21mini-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | byłaś, potrzebowałaś, powiedziałaś, zrobiłaś | none | none |
| r1-v3-21mini-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | FAIL | pass | pass | FAIL | n/a | none | 0 | 0 | jakbyś była, jakbyś wolała | none | none |
| r1-v3-21mini-low | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v3-21mini-low | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v3-21mini-low | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r1-v3-21mini-low | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | FAIL | FAIL | pass | n/a | n/a | pass | n/a | let me think | 0 | 0 | none | none | none |
| r1-v3-21mini-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | n/a | pass | pass | pass | pass | FAIL | FAIL | pass | pass | pass | none | 0 | 1 | none | chciałbyś | none |
| r1-v3-21mini-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | FAIL | pass | FAIL | pass | pass | FAIL | none | 0 | 2 | none | chciałbyś, jakbyś czekał | none |
| r1-v3-21mini-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |
| r1-v3-21mini-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 1 | none | jakbyś był | none |
| r1-v3-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | FAIL | pass | pass | pass | FAIL | none | 0 | 0 | jakbyś dostała, jakbyś już była, umiałaś | none | none |
| r1-v3-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 1 | chciałabyś, jakbyś już czuła, miałaś | none | none |
| r1-v3-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | FAIL | FAIL | pass | pass | pass | pass | n/a | daj mi chwil | 0 | 0 | chciałabyś, miałaś, zrobiłaś | none | none |
| r1-v3-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś zgodziła | none | none |
| r1-v3-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v3-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v3-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r1-v3-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r1-v3-21mini-minimal | T1 | fresh | 1 | pass | FAIL | pass | n/a | n/a | pass | pass | FAIL | pass | n/a | pass | pass | pass | pass | FAIL | FAIL | pass | FAIL | pass | none | 0 | 1 | none | byś chciał | none |
| r1-v3-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | none | Jakbyś mógł, napisałeś | none |
| r1-v3-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v3-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 1 | none | jakbyś był, jakbyś musiał | none |

### Transcripts

#### r1-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (2.36 s to first audio, 6.05 s spoken): Cześć, Aniko. Miło mi Cię usłyszeć, jest tu dla Ciebie spokojne miejsce, na przemyślenia i rozmowę.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.84 s to first audio, 21.8 s spoken): To wygląda na spiralę: niedziela, spokój, ale już w głowie kręci się jutro. Jakbyś trzymała w dłoniach plan dnia, który jeszcze nie zaczął się, a już siedzi Ci na barkach. Może chcesz, żebym pomogła ułożyć to trochę lżej? Albo przynajmniej nazwać, co najbardziej wyostrza to napięcie, zanim przejdziemy dalej.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.79 s to first audio, 24.25 s spoken): Może to właśnie tyle: ciężko. I to nie jest mały kłopot, tylko coś, co narasta, kiedy głowa już odlicza świat. Jest tu miejsce, żeby z tym zostać, bez pośpiechu, bez prób przyklejania etykiet. Jeśli chcesz, mogę powiedzieć coś prostego o tym, co słyszę, jako oddech, który pomaga, albo po prostu chwilę ciszy, żebyś mogła zobaczyć, co w tym jest naprawdę.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (1.08 s to first audio, 25.95 s spoken): Słyszę, że to było dla Ciebie momentem, kiedy poczułaś, że musisz przyjąć coś, co jest wygodne dla innych, ale męczy Ciebie. To nie jest brak siły, to raczej odruch, który chroni relację. Czyli chęć dogadania się, spokoju, bez konfliktu. Możemy teraz wejść w to, co w Twojej głowie krąży: co z tego jest faktyczną priorytetem, a co jest taką miękką potrzebą bycia w porządku wobec innych.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.3 s to first audio, 25.7 s spoken): Nie, nie powinno być to automatyczna decyzja. To może być odpowiedź, która brzmi szczerze, ale trzeba ją dobrze dobrać. To znaczy, warto powiedzieć wprost, że przyjęłaś projekt z poczucia presji, a nie dlatego, że jest to dla Ciebie idealne. To może być pierwsza szczery rozmowa, która zmienia sposób, w jaki później będziecie rozmawiać. Wiem, że to niewygodne, ale czasem to jest właśnie ta prawda, która daje przestrzeń.

#### r1-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.74 s to first audio, 8.15 s spoken): Cześć Ania, miło mi Cię poznać. Dopóki nie powiesz, o czym chcesz dziś pomyśleć, zostaję tu spokojnie z Tobą.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.9 s to first audio, 23.05 s spoken): Słyszę, że ta niedziela jest jak pętla. Myślisz o pracy jutro, zanim w ogóle się zaczęło. Zajęłaś się już tym przedłużeniem, które ciągle krąży w głowie. Moja zgadywanka jest taka, że to nie tylko jutro Cię martwi, ale to, że jesteś zmęczona już teraz. Jeśli chcesz, możemy jeszcze na chwilę zatrzymać się przy tym, co przed Twoją głową.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.76 s to first audio, 20.7 s spoken): Brzmi, jakby było ciężko, czasem nawet wtedy, kiedy nie ma konkretnie czego nazwać. To taki moment, w którym wszystko jest po prostu trudne. Może teraz nie trzeba nic rozbierać, tylko zauważyć, że to jest po prostu ciężki czas. Jeśli chcesz, możemy zostać przy tym uczuciu, bez oceniania, i po prostu posłuchać, co ono mówi.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.79 s to first audio, 30.4 s spoken): Brzmi, jakbyś wróciła z poczuciem, że nic nie mówisz tylko sobie, a potem wchodzi kolejny projekt. I może pojawia się taki podskórny konflikt: chcesz być pomocna, ale też chcesz mieć granicę. Moja zgadywanka: to nie jest tylko „nie chcę”, tylko „boję się konsekwencji”. Jeśli to prawda, możemy zostać przy tym. Nie musisz od razu mówić „nie” pięknie. Możesz po prostu zrobić przerwę, powiedzieć „muszę to przemyśleć”, a potem znaleźć swoje miejsce w rozmowie.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.06 s to first audio, 26.9 s spoken): To, że chcesz powiedzieć to wprost, może być bardzo pomocne. Ale też pamiętaj, że mówienie „nie” nie musi być od razu idealne. It’s okay to say, „muszę się nad tym zastanowić” albo „może inaczej rozplanować”. Jeśli chodzi o to, czy powiedzieć wprost, to zależy od tego, co czujesz w środku. Jeśli chcesz, możesz mi powiedzieć, co dokładnie chciałabyś mu powiedzieć. Co byłoby dla Ciebie najuczciwsze?

#### r1-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.85 s to first audio, 4.7 s spoken): Jak często czujesz, że musisz się wyłamać i powiedzieć „nie” przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.71 s to first audio, 22.25 s spoken): Brzmi, że w piątek znowu zrobiłaś to, co zwykle: powiedziałaś tak, choć sama byłaś wykończona. To może oznaczać, że ważne było dla ciebie bycie w porządku albo spokój między wami, zamiast tego, co naprawdę potrzebowałaś powiedzieć. Może to też pokazuje, że czujesz dyskomfort z powodu granic, ale jeszcze chwytasz się tego, co jest bezpieczne w danym momencie.
- *Person*: nie wiem
- **Orca 3** (0.66 s to first audio, 18.8 s spoken): To „nie wiem” brzmi jak moment, w którym trochę odpuszczasz sobie. To może być też coś między: trochę niedowierzanie, trochę zmęczenie, trochę poczucie, że potrzebujesz czasu. Mogę to traktować jako wskazówkę, że coś w tej sytuacji jest ciężkie i może potrzebujesz więcej przestrzeni, żeby to przemyśleć.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.59 s to first audio, 18.55 s spoken): Rozumiem, że to nie dotyczy tylko samego projektu, ale tego, czy dojrzysz do własnych granic. Masz lęk, że odmawianie to kapitulacja albo że ktoś uzna cię za słabszą. Ale to nie jest to samo, co być bezradną, to właśnie chwytanie się granic, choćby miało być niewygodne.

#### r1-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.67 s to first audio, 4.55 s spoken): Ania, co dokładnie sprawia Ci trudność w odmawianiu przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.64 s to first audio, 18.8 s spoken): Brzmi, jakbyś wolała nie robić, ale zgodziła się, żeby nie narazić się na konflikt, albo żeby po prostu ulżyć sobie w tej chwili. To może być też taki moment, gdzie Twoja niechęć stała się większa niż realna gotowość. Co myślisz o tym [en dash] to był pierwszy impuls, a potem chęć przetrwać?
- *Person*: nie wiem
- **Orca 3** (0.61 s to first audio, 22.85 s spoken): To brzmi jakbyś była trochę „w środku” [em dash] nie masz pewności, ale też nie chcesz się wypychać. Moja zgadywanka: może chodzi o to, że wiesz, że to nie będzie łatwe, ale też nie chcesz wchodzić w sytuację napięcia czy kłótni. Jeśli chcesz, możesz powiedzieć, co przychodzi Ci do głowy teraz, a ja tylko pomogę to wypowiedzieć [em dash] bez ocen, bez pędzenia i bez presji.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.62 s to first audio, 20.1 s spoken): Mam wrażenie, że pod spodem jest strach przed odrzuceniem, przed tym, że ktoś pomyśli: „ona nie podoła”. To brzmi jak głos, który broni Cię, choć robi to w sposób, który kosztuje Cię siły. Możemy to ułożyć, ale bez nacisku: co byłoby dla Ciebie w tej sytuacji najmniej bolesnym sposobem powiedzenia „nie”?

#### r1-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.95 s to first audio, 5.55 s spoken): Hey Tom, it’s good to hear your voice. I’m here, and we can start whenever you’re ready.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.66 s to first audio, 19.55 s spoken): That sounds really heavy, like your brain is comparing everyone else and coming up short. It’s a common trap, especially when the day feels like it’s supposed to have a clear plan. You’re not wrong for feeling this way, just tired and trying to measure yourself while you’re tired. I wonder what part of it really hit you hardest today.
- *Person*: I don't know.
- **Orca 3** (0.88 s to first audio, 20.1 s spoken): Got it, that’s honest. Sometimes when you’re not sure, it means your mind is juggling a few things at once and none of them feel fair on their own. My guess is that this might be about feeling behind, or uncertain, and you’re trying to find a way to measure yourself without comparing too much. If that’s not right, we can tweak it and go from there.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.86 s to first audio, 16.65 s spoken): That’s a real sting, seeing milestones you haven’t hit yet, and feeling stuck in limbo. It’s like your life is being measured through someone else’s timeline. My guess is you’re not just jealous. You’re noticing you want a clearer shape to your own path.
- *Person*: What do you think I should do?
- **Orca 5** (0.83 s to first audio, 25.75 s spoken): Let me talk this through with you, and keep it simple and grounded.I can’t tell you what to do. What I think is it’s a prompt to slow down and focus on what’s actually in your hands, like your housing, your money, your rhythm. Those things matter. It’s better to bring this up with your therapist and ask them to help you sort it, because they can weigh your big picture. What would you want to say to them about this?

#### r1-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.64 s to first audio, 3.65 s spoken): Hey Tom, glad you’re here. Take your time, I’m listening.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.59 s to first audio, 25.65 s spoken): It sounds like you’re carrying a lot of comparison today, and it’s draining. You might be weighing where you’re supposed to be against where you actually are. And maybe you’re hoping that you’ll catch up, but that pressure makes everything feel heavier than it is.

We can just sit with that for now. You don’t have to prove anything. If you want, we can talk about one small thing you did recently that felt steady.
- *Person*: I don't know.
- **Orca 3** (0.53 s to first audio, 19.25 s spoken): That’s fair. Sometimes when things feel that muddy, it’s hard to grab onto anything specific. My guess is this: you’re not empty or missing everything. You’re just tired and comparing your insides to other people’s outsides. If something small comes up, you can share it. If not, we can just sit with the heaviness for a second.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.59 s to first audio, 23.05 s spoken): Yeah, that one hits. The milestone, the buying, the life moving, and you’re still in a more crowded setup. It can sting, and it’s okay to admit that. My guess is that what you’re noticing isn’t just the flat. It’s the feeling of being behind, and maybe wanting a sense of stability you can count on. If that’s right, we can explore it together without rushing.
- *Person*: What do you think I should do?
- **Orca 5** (0.77 s to first audio, 20.1 s spoken): I can’t give a clear plan for you to follow. Big life stuff like this belongs with your therapist. But what I can offer is this: you’re noticing a mix of jealousy and longing, and it can feel like pressure when others move ahead. If you want, you can say what you’d like to explain to your therapist, or how you want them to respond when this comes up.

#### r1-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (1.02 s to first audio, 4.65 s spoken): Tom, what’s one small step you’ve been thinking about to call your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.69 s to first audio, 23.35 s spoken): That sounds like a familiar trap: the day slips by, and then evenings suddenly feel gone. And it’s not laziness, it’s just how your energy and time end up.

You might be noticing that evenings are when you’d like quieter time, and calling feels like it would add to it. It’s okay to try something tiny, like a two-minute call, or even a text first. But only if that feels doable.
- *Person*: I don't know.
- **Orca 3** (0.81 s to first audio, 22.35 s spoken): I heard you, and it sounds like it feels a bit tangled. Maybe you’re not unsure of what you want to say, but more unsure of how it’ll feel once it’s said, or when to make time for it.

My guess is, you’re not avoiding it completely, just waiting for the right moment[em dash]and that moment keeps moving. Tell me if that sounds close, or if you want to share what’s making it feel unclear.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.76 s to first audio, 30.2 s spoken): Okay, I heard that. It sounds like the relationship is doing a light version, and the deeper part, your mum, doesn’t get space. That might be weighing on you[em dash]you want more of him, but the conversation keeps sitting on safe topics. And that’s okay to say out loud.

If it feels heavy, you could try a single line like, “I’ve been thinking about mum a lot lately,” before shifting to football or whatever comes next. It keeps the door open without forcing a big moment right away.

#### r1-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.77 s to first audio, 8.65 s spoken): Nice, let me think about that for a moment.So, what makes “calling your dad more” feel important to you right now?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (1.2 s to first audio, 22.35 s spoken): It sounds like you mean to reach out, but the evening just gets away from you. A lot of things compete for attention in that time, and it’s easy to miss the moment you wanted to call. There’s probably a mix of wanting to connect and feeling pressed by time or other things. If you want, we can talk through one small step you could try with the next evening, so it feels a bit lighter.
- *Person*: I don't know.
- **Orca 3** (0.76 s to first audio, 19.6 s spoken): That’s fair. Keep it really simple. Try picking a specific day, like Tuesday, and aim for one call, even if it’s short. Once it’s planned, something in the schedule takes the pressure off. You don’t have to get through a whole evening routine. Just make one call on purpose, and let it be enough.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.75 s to first audio, 17.15 s spoken): That’s interesting, and a bit lonely too. It sounds like the call is more about light conversation, like football, and the space for the harder stuff doesn’t have room yet. Maybe your dad’s feeling okay with just a small, steady chat can be a way in, without trying to cover everything.

#### r1-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.79 s to first audio, 5.7 s spoken): Cześć, Alex. Miło cię słyszeć, mam nadzieję, że któryś z tych tematów da ci chwilę oddechu.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.99 s to first audio, 15.5 s spoken): Świetnie, to może zacznijmy od tego, co cię dziś najmocniej przyciąga myśli. Jeśli to chaos, to już jest znak. Możemy go trochę uporządkować. Albo możesz powiedzieć, co jest najmniejszym zmartwieniem teraz. Cokolwiek wybierzesz, to jest start.
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 15.2 s spoken): Brzmi, jakbyś po prostu czuł lekką pustkę i nie wiedział, co z nią zrobić. Moja zgadywanka: może to nie brak tematu, tylko brak miejsca na to, co już się dzieje. Jeśli to prawda, możemy spróbować po prostu nazwać uczucie, nawet jednym słowem.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.75 s to first audio, 25.85 s spoken): Widzę, że to dla ciebie naprawdę istotne. W pracy kręci się dużo, a ty czujesz, że nie masz pewności, czy zostaniesz w zespole. To zwykłe, że tak się czujesz, gdy sytuacja jest niejasna. Myślę, że pod spodem może być strach przed utratą stabilności i też pragnienie spokoju w tym, co niepewne. Jeśli chcesz, wyłóżmy to na spokojnie, po jednym kroku. Co dla ciebie jest teraz największą wątpliwością?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.9 s to first audio, 26.6 s spoken): Jasne, tylko pamiętam, że nie jestem terapeutką ani doradcą zawodowym. To, co mogę zaproponować, to w sensie myślenia: możesz sprawdzić, co jest kontrolowane, a co tylko przewidywane. To jest różnica, która pomaga trochę ugruntować ruch. A jeśli chcesz, możemy to przerzucić na rozmowę z terapeutką, bo to właśnie tam taki plan i granice są najpewniejsze. Co chciałbyś powiedzieć im na ten temat o swojej niepewności?

#### r1-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.9 s to first audio, 1.9 s spoken): Cześć, miło cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.77 s to first audio, 16.4 s spoken): Brzmi, że chcesz po prostu móc zacząć, a niekoniecznie od razu wiedzieć, gdzie iść. Możemy po prostu zacząć od tego, co dziś w głowie, nawet jeśli to tylko ogólny szkic. W pierwszej kolejności słucham, co samo się pojawi, bez zmuszania do planu.
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 21.0 s spoken): Myślę, że kiedy mówisz „nie wiem”, chodzi o to, że wybór jest dla ciebie ciężki, nie że brak ci wszystkiego. To może być moment, gdy chcesz przede wszystkim poczuć, co jest dla ciebie właściwe, zanim podejmiesz decyzję. Jeśli tylko to, co przychodzi do głowy brzmi zaufalnie, możemy się zatrzymać i pozwolić tym myślom przepłynąć.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.7 s to first audio, 19.05 s spoken): Rozumiem, że to niepewność, też sporo napięcia. To wygląda tak, jakbyś czekał na coś, co rozstrzygnie sprawę, ale trochę się też obawiał. Może chodzi o to, że zostać w zespole to byłoby dla ciebie stabilne, a odchodzić też trochę kusi. Mogę pomóc Ci to uporządkować, jeśli zechcesz.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.71 s to first audio, 28.55 s spoken): Rozumiem, że to trudne pytanie. Pozwól, że ułożę w głowie prostą odpowiedź.Nie mogę doradzać konkretnych decyzji, bo to nie jest moje miejsce. Mogę powiedzieć uczciwie: jeśli czujesz, że niepewność o zespół jest ciężka, warto mieć plan B. Albo wypytać o rolę i perspektywę, albo przygotować się na zmianę. To wszystko. A jeśli chcesz, mogę pomóc Ci sformułować, co chciałbyś powiedzieć w rozmowie z szefem czy z zespołem. Czego chciałbyś się dowiedzieć wprost?

#### r1-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.66 s to first audio, 3.75 s spoken): Jakie zmiany w pracy teraz najbardziej dają Ci do myślenia?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.66 s to first audio, 17.7 s spoken): Słyszę, że to jest dla Ciebie mocno niepewne i trochę wytrąca z rytmu. Co tydzień ktoś znika, to pewnie budzi napięcie i pyytanie, kto będzie następny. To jest sytuacja, która potrafi trochę przytłoczyć, bo masz wrażenie, że wszystko jest w ruchu i nie jest stabilne.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 23.7 s spoken): Niepewność to w tej chwili to, co czujesz najmocniej. Kiedy nie widzisz jasnego kierunku, umysł może się rozpraszać i podłączać do wielu scenariuszy naraz. Może warto pamiętać o jednym przydatnym fakcie: to nie jest jedno konkretne zadanie dla Ciebie, tylko cała fala zmian. Możesz zrobić krok po kroku: przyjrzeć się, co jest pod kontrolą, a co tylko przechodzi obok.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.67 s to first audio, 27.15 s spoken): To brzmi bardzo męcząco. Ta cisza, kiedy nikt nic nie mówi wprost, potrafi być gorsza niż konkretna informacja. Czujesz, że wszystko jest zawieszone, a ty nie dostajesz nawet wskazówki, co dalej.

Moja zgadujka to: może chodzi o to, że masz potrzebę jasności i poczucia, że ktoś stoi za decyzjami. Jeśli to tak, to możesz powiedzieć, co konkretnie u Ciebie najbardziej bolące, albo co chciałoby się, żeby ktoś wypowiedział.

#### r1-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.66 s to first audio, 3.8 s spoken): Alex, jakiej zmiany w pracy najbardziej się teraz spodziewasz?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.64 s to first audio, 21.2 s spoken): Brzmi, jakbyś był w miejscu, gdzie wszystko się przesuwa, a ludzie odchodzą, więc to co zwykle stabilne, nagle staje się niepewne. Może chodzi o to, że ta rotacja zmienia poczucie bezpieczeństwa i trochę zaburza rytm dnia. Jeśli chcesz, możemy po prostu popatrzeć, co z tego najbardziej wpływa na twoje samopoczucie.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 19.7 s spoken): Zrozumiałem, że czujesz się trochę przytłoczony i jeszcze nie do końca wiesz, co dokładnie robi na Ciebie największe wrażenie. To jest zwykłe. Kiedy wszystko się zmienia, człowiek potrzebuje chwili, żeby to przetrawić. Czyli może skupić się na tym, co uczucie podpowiada, a nie na tym, co jest „poprawne”. Z czasem może to stać się bardziej oczywiste.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.78 s to first audio, 26.15 s spoken): Rozumiem, że brak jasnych komunikatów jest dla Ciebie męczący. Niepewność bywa gorsza niż konkret. Kiedy nic nie jest powiedziane wprost, trudno ocenić, co jest stabilne, a co się zmienia. Mogę Ci zaproponować jedno: spróbuj nazwać ten moment, kiedy czujesz, że docierasz do ściany, nawet jeśli nie jest to „problem”, a raczej wrażenie. To może pomóc uchwycić, co dokładnie jest dla Ciebie trudne.

#### r1-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.67 s to first audio, 1.75 s spoken): Cześć, miło Cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.8 s to first audio, 26.95 s spoken): Jesteś już w tym miejscu, gdzie niedzielne wieczory zaczynają brzmieć „jutro” i trochę ściska w środku. Masz świeżo w głowie to, co będzie jutro, i to samo podejrzanie wraca. To jakbyś już była w tym stole jutro, zanim jeszcze nadeszło. Może zamiast próbować zmieniać wszystko naraz, warto coś drobnego, na przykład zatrzymać się na moment i pozwolić sobie zauważyć, co w tym „jutro” jest naprawdę ciężkie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.75 s to first audio, 25.2 s spoken): To brzmi jak ciężar bez uchwytu, taki moment, kiedy po prostu czujesz, że nie masz czym odciągnąć myśli. Moja zgadywanka: może najbardziej męczy samo bycie w stanie gotowości, sprawdzanie, czy wszystko jest ok, zanim jeszcze zacznie się tydzień. Możesz to poczuć jako ogólny ciężar, bez konkretnego kształtu, i to też jest ok. Czasem wystarczy powiedzieć: „jest ciężko, ale jestem tu i słyszę to”.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.82 s to first audio, 21.55 s spoken): Brzmi, jakbyś dostała coś dodatkowego, a w środku zostało poczucie, że nie wolno Ci tego odłożyć. Nie umiałaś powiedzieć nie, albo nie była przestrzeń na to. To może być długotrwałe zmęczenie, kiedy trzeba się dopasować. A jeśli chcesz, możemy teraz wziąć to spokojnie na tapetę. Jakie jest to „nie”, które wydaje Ci się najtrudniejsze teraz?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.76 s to first audio, 24.85 s spoken): Szczerze? Jeśli czujesz, że jest to kwestia granicy, to mówić wprost może być sensowne. Nie po to, by kłócić się, tylko po to, żeby wyrazić, co jest dla Ciebie do dźwignięcia. Możesz powiedzieć: „Nie dam rady tego przyjąć bez przekroczenia swoich zobowiązań”. Jeśli masz w głowie lęk albo poczucie winy, to też ważne, ale niech to nie przesłoni tego, że Twoje zdanie liczy się tak samo, jak czyjeś oczekiwania.

#### r1-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.76 s to first audio, 2.55 s spoken): Cześć, Ania, miło Cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.73 s to first audio, 14.2 s spoken): Świetnie, że to mówisz. Brzmi, jakbyś już czuła ten ciężar, zanim jeszcze zacznie się wszystko na nowo. Ten moment, kiedy cały tydzień w pracy już siedzi w głowie, a nie w następnym tygodniu, tylko w niedzieli.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.68 s to first audio, 33.35 s spoken): Rozumiem, to po prostu bywa ciężkie, bez żadnego dodatkowego planu. Czujesz, że to narasta i wciąga cię, i trudno jest złapać oddech. Moja zgroza jest taka, że to, co ciężkie, może być mniej zwyczajne niż weekend. Może pod spodem jest napięcie z pracy, z tego, że chcesz dobrze wypaść, albo po prostu zmęczenie. Ale teraz, teraz po prostu to czujesz. Jeśli chcesz, możemy to spokojnie przyjrzeć się krok po kroku, bez pośpiechu, i zobaczyć, co jest pierwsze do odłamania.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.77 s to first audio, 22.35 s spoken): Brzmi, jakby decyzja, która pojawiła się w ostatni moment, była dla Ciebie obciążeniem. To nie tylko kwestia projektu, ale też tego, że nie chcesz eskalacji ani konfliktu, więc mówisz „tak”, choć czujesz, że nie masz przestrzeni. Czasem to właśnie ten moment bywa ciężki, bo chcesz być użyteczna, a jednocześnie brakuje Ci miejsca na własne granice.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.78 s to first audio, 30.85 s spoken): To zależy od tego, co dokładnie chcesz powiedzieć. Jeśli chodzi o to, że masz teraz za dużo i potrzebujesz przestrzeni, to ucz się mówić, że nie, po prostu. Ja nie jestem terapeutą, więc nie będę Ci mówiła, co masz zrobić, ale myślę, że szczerość może być uczciwa, a oszczędna, jeśli chcesz, żeby szef zrozumiał: że masz limit, że pracujesz nad tym, co masz, i że nie możesz dorzucać kolejnej rzeczy.

Co chciałabyś mu powiedzieć, gdyby miałaś zamiast odpowiedzi „tak”, powiedzieć „nie”, wprost i spokojnie?

#### r1-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.55 s to first audio, 4.4 s spoken): Ania, co jest dla ciebie teraz najtrudniejsze przy odmawianiu przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.84 s to first audio, 10.2 s spoken): Brzmi, jakby w tej sytuacji też zrobiłaś to głównie po to, żeby nie robić kłopotu, a nie dlatego, że miałaś na to rzeczywiście energię. Czy to zgodzi się z tym, co czujesz?
- *Person*: nie wiem
- **Orca 3** (0.59 s to first audio, 20.35 s spoken): Okej, daj mi chwilę, żeby to spokojnie przemyśleć razem.Jasne, może być Ci trudno wskazać, co dokładnie Cię w tym zaskoczyło. Może to była mieszanka zmęczenia, strachu przed konfliktem i chęci utrzymać dobrą relację. Widzę, że jest tam coś między poczuciem winy a brakiem siły. Jeśli tam coś jest, to pewnie właśnie to.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.86 s to first audio, 21.75 s spoken): To brzmi jak stary strach, który wchodzi w rolę opinii o sobie. Gdy się wahasz, pojawia się myśl, że odmawianie to niedomaganie, a nie granica. To jest bardzo ludzka obawa. Chcę ją nazwać spokojnie, nie oceniając. Czy chciałabyś spróbować zobaczyć to inaczej, na przykład tak, że odmowa nie jest porażką, tylko decyzją?

#### r1-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.78 s to first audio, 4.1 s spoken): Ania, co u Ciebie najbardziej gryzie w odmawianiu przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.85 s to first audio, 17.65 s spoken): Brzmi, jakbyś zgodziła się na coś nie tylko z braku siły, ale z chęci uniknąć kłótni albo napięcia. To często robi różnicę: bierzesz na siebie dodatkowy ciężar, żeby sytuacja była spokojniejsza. Czy da się to podejść inaczej, tak żeby Twoja energia miała szansę przetrwać?
- *Person*: nie wiem
- **Orca 3** (0.76 s to first audio, 21.0 s spoken): Niepewność to bardzo ludzka rzecz, zwłaszcza kiedy te rozmowy są trudne. Mogę zgadnąć, że chodzi o to, że chcesz być uprzejma i widziana jako pomocna, ale Twoje zasoby są ograniczone i to też jest ważne. Co by było dla Ciebie bardziej wspierające: samo postawienie granicy, czy przygotowanie zdania, które będzie mówiło „nie” bez zbędnego objaśniania?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.77 s to first audio, 32.7 s spoken): To brzmi jak naprawdę ciężki ciężar, kiedy jesteś uważana za „niepowinno” czy „nie nadaje się”, tylko dlatego, że chcesz postawić granicę. To uczucie, że odmawiając, tracisz swoją wartość, może gościć często. W takim strachu jest trochę Twojej troski: chcesz być dobrze postrzegana, ale jednocześnie czujesz, że Twoje granice są w konflikcie. Jeśli chcesz, możemy spróbować zobaczyć, co będzie dla Ciebie wsparciem: łagodna odmowa, albo jednak powiedzenie swojego zdania.

#### r1-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.57 s to first audio, 1.65 s spoken): Hey Tom, nice to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.53 s to first audio, 14.35 s spoken): That sounds heavy. When you say rough, I hear a mix of pressure and comparison. It’s like you’re holding the feeling that you’re behind in a race you didn’t even sign up for. And maybe a little part of you wants to be doing it right, not just doing it.
- *Person*: I don't know.
- **Orca 3** (0.49 s to first audio, 14.95 s spoken): You’re not sure yet, and that’s okay. I’m guessing you’re tired of sorting what’s theirs and what’s yours, and that part feels confusing. Sometimes the hard part is just sitting with the “I don’t know” without needing to solve it immediately.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.55 s to first audio, 16.9 s spoken): That’s a sharp comparison to bump into. It sounds like you’re noticing where you feel you’re at versus where they are, and it’s landing hard. My guess is you’re wanting stability and a clear next step, and seeing the engagement and flat makes that want feel sharper. Tell me if that’s off.
- *Person*: What do you think I should do?
- **Orca 5** (0.57 s to first audio, 15.55 s spoken): That’s a big question. I can’t give you a strict “do this” plan here. I’m a machine, and I can’t replace the deeper guidance you get from your therapist. But I can help you shape what you want to say about this. So, what would you tell them is the hardest part of this for you?

#### r1-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.87 s to first audio, 1.95 s spoken): Hey Tom, it’s good to hear from you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.69 s to first audio, 15.6 s spoken): Yeah, that feeling is heavy. It sounds like you’re measuring yourself against everyone else’s timeline, and when you’re tired, it feels louder. I’m guessing you want to feel like you’re on your own path, not rushed or behind. If that’s close, we can keep going with it.
- *Person*: I don't know.
- **Orca 3** (0.71 s to first audio, 16.95 s spoken): Fair. Sometimes the “I don’t know” says more than we think. It can mean you’re tired, or you’ve been comparing yourself a lot, or you’re just unsure what you really want. If I’m wrong, let me know. If I’m close, then maybe today is just a day of noticing and not deciding.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.69 s to first audio, 19.9 s spoken): That’s a sharp contrast, and it can hit hard. It sounds like you’re comparing your situation to theirs and feeling like you’re being judged by it. My guess is you want to feel steady and okay with where you are right now, without feeling like you’re in a race. If that’s close, we can sit with it. If it’s far off, we can adjust.
- *Person*: What do you think I should do?
- **Orca 5** (0.97 s to first audio, 14.8 s spoken): That’s a fair question. I can’t guide you on what to do, but what you do with this matters for your own clarity.

If this is something you’d bring to your therapist, what would you want to say to them about the comparison, the pressure, or the quiet jealousy that shows up when that happens?

#### r1-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.6 s to first audio, 3.9 s spoken): What makes calling your dad more feel important to you right now?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.65 s to first audio, 13.3 s spoken): Oh, yeah, that happens a lot [em dash] the day just eats the time. It sounds like you really mean to, but nights get away from you. Maybe the missing piece is a bit of a plan, like a small window you protect for it.
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 13.05 s spoken): Sounds like you’re not sure what to do next, and that leaves you floating a bit. Maybe it’s not a big decision, just a gentle structure you could try tomorrow, like a short call before or after dinner.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.55 s to first audio, 16.15 s spoken): That suggests there’s something heavy behind the football chatter. Maybe you’re trying to keep it light because the grief is hard to sit with, or the story of your mum feels too big for a quick call. And maybe football is safe because it’s familiar, easy, and doesn’t ask much.

#### r1-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.54 s to first audio, 4.2 s spoken): What’s the first thing that comes to mind when you think about calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.6 s to first audio, 15.9 s spoken): I hear that you really want to connect with him, but the day slips away from you before you can make the call. Maybe there’s a moment earlier in the day that feels more reachable than the evening. If that’s right, we can explore that later, and you can decide how it sounds to you.
- *Person*: I don't know.
- **Orca 3** (0.59 s to first audio, 19.95 s spoken): That “I don’t know” feels like a blank spot, not a failure. My guess is you’re not resisting him, you’re just not sure where to put the effort in a day that already feels full. It might help to notice the one thing that makes calling harder[em dash]like being tired, or feeling like you have to sound a certain way[em dash]and we can start there.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.65 s to first audio, 23.05 s spoken): Yeah, that sounds like a pattern: the call turns into football and stays there, and the mum can feel like a shadow in the room. My guess is part of you might be protecting both sides[em dash]him and yourself[em dash]from feeling like you have to carry a lot at once. We can just sit with that for a moment, no need to fix it. If you want, we can talk about what that feels like when you pick up the phone, later.

#### r1-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.58 s to first audio, 4.5 s spoken): Cześć, Alex! Miło Cię słyszeć. Zaczynamy od tego, co chcesz powiedzieć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.53 s to first audio, 15.5 s spoken): Gotowe to. Nie musisz od razu wiedzieć, od czego zacząć. Czasem wystarczy powiedzieć po prostu, co teraz spada na myśl. Może to drobna rzecz, albo coś, co wisi w głowie. Jeśli chcesz, mów po prostu [en dash] ja będę słuchać i pomagać Ci ułożyć to w głowie.
- *Person*: nie wiem
- **Orca 3** (0.61 s to first audio, 22.15 s spoken): Słyszę, że jesteś w takim miejscu, gdzie wszystko jest w głowie i nie wiesz na czym zaczepić. To ok, że jest niejasne. Wiesz, co mnie tamu potencjalnie chodzi po głowie? Może to, że nie chcesz narzucać sobie tematu, albo że brak pomysłu to sygnał zmęczenia albo napięcia. Daj mi znać, czy to jest coś, co czujesz, czy może coś zupełnie innego.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.56 s to first audio, 21.9 s spoken): Brzmi, jakby to było ciężkie, bo czujesz, że Twoje miejsce w zespole nie jest pewne. Możesz to opisać jako napięcie między nadzieją, a obawą. Moja zgadywanka: zastanawiasz się, czy wolisz zostać i przetrwać, czy zrobić krok dalej, mimo że nie wiesz, jak będzie. Jeśli to brzmi blisko tego, możesz powiedzieć, a ja potrafię to poukładać.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.59 s to first audio, 22.2 s spoken): Hmm, na miejscu tej osoby zrobiłabym tak, żeby być jak najuczciwsza wobec siebie i dla reszty zespołu. Ale nie jestem człowiekiem na twoich realiach, więc ciężko mi narzucać swoje decyzje orzecznicze. To, co mogę zrobić, to pomóc Ci zobaczyć, czego naprawdę chcesz, i przefiltrować to przez realia. Co byś chciał, żebyś powiedział swojej terapeutce w tej sprawie?

#### r1-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.66 s to first audio, 2.35 s spoken): Cześć, Alex, miło cię usłyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.7 s to first audio, 16.85 s spoken): Hej, dzięki, że napisałeś. Możemy zaczynać od czegokolwiek, co akurat chodzi po głowie. Jeśli chcesz, możemy po prostu nazwać to, co sprawia, że zaczynasz się zastanawiać, nawet jeśli jest to „nie wiem”. A potem spróbujemy to dobrze przyjrzeć się temu, co utkwiło w głowie.
- *Person*: nie wiem
- **Orca 3** (0.67 s to first audio, 23.1 s spoken): Nie wiem, brzmisz, jakby było ci trudno znaleźć punkt, od którego pójść dalej. Może to po prostu myślenie się krąży, bez wyraźnego ukierunkowania. To też jest wskazówka, że potrzebujesz przestrzeni, żeby coś wyłoniło się samo, bez nacisku. Jeśli chcesz, mogę pomóc ci przeramować to „nie wiem” w prostą rzecz do namysłu, a potem zobaczymy, co z tego wyjdzie.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.84 s to first audio, 21.15 s spoken): Z tego, co mówisz, brzmi, że teraz to poczucie zmiany w pracy jest dla Ciebie trochę niepewne, a myśl o zostaniu w zespole wisi w powietrzu. To może oznaczać, że czujesz się trochę zawieszony między nadzieją a obawą. Jeśli masz ochotę, możesz spróbować powiedzieć, co jest dla Ciebie teraz najtrudniejsze w tym wszystkim.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.74 s to first audio, 36.3 s spoken): Jasne, ale nie mogę ci doradzać tak konkretnie, bo nie jestem terapeutą. To, co mogę zrobić, to pomóc ci posłuchać siebie, co tu jest dla ciebie ważne, a potem możesz to wykorzystać w rozmowie z terapeutą albo z kimś zaufanym.

Gdybym miała zgadywać, to możliwe, że chodzi o to, czy wolisz stabilność, czy jednak nowe możliwości, nawet jeśli są trudne. Ale to tylko zgadanie, możesz to wypchnąć albo zostawić.

Jakbyś mógł/mogła powiedzieć tylko jedno zdanie o tym, czego chcesz się więcej dowiedzieć, albo czym się teraz najbardziej martwisz, co to byłoby?

#### r1-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.75 s to first audio, 7.15 s spoken): Jakie zmiany w pracy ostatnio najbardziej Cię poruszają, albo co w tym temacie kręci Cię teraz najmocniej?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.87 s to first audio, 26.15 s spoken): Brzmi, że to jest dla Ciebie jako fala, raz ktoś odchodzi, raz coś się zmienia i to trochę osłabia poczucie stabilności. Czujesz, że to wpływa na Twoje poczucie bezpieczeństwa albo na to, jak patrzysz na swoją rolę? 
Jako sugestię wrzucam, że może w tym wszystkim najbardziej brakuje poczucia, że wiesz, co jest stałe, co zależy od Ciebie, a co jest poza Twoją kontrolą.
- *Person*: nie wiem
- **Orca 3** (0.74 s to first audio, 18.65 s spoken): Nie jesteś w stanie wskazać jednej rzeczy, która to wszystko spaja. To normalne, kiedy wydarzenia są w ruchu. Masz już start, ale jeszcze nie masz całej mapy. Jeśli chcesz, możesz podać choćby jedną rzecz, którą widzisz wyraźnie, a wtedy spróbuję ją doprecyzować, bez nacisku.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.85 s to first audio, 16.65 s spoken): To znaczy, że brakuje jasnych słów i czujesz, że wszystko jest w zawietrzu. Gdy nikt nie mówi wprost, trudno też wiedzieć, co jest prawdą, co się zmienia, a co może zostać. To może być właśnie coś, co wzmacnia niepokój, bo brakuje kierunku.

#### r1-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.79 s to first audio, 3.35 s spoken): Co w tych zmianach w pracy teraz najbardziej Cię porusza?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.81 s to first audio, 17.55 s spoken): Brzmi, jakbyś był w takim miejscu, gdzie wszystko się przesuwa, a ludzie odchodzą bez końca. To pewnie robi wrażenie, że jesteś ciągle w ruchu, trochę jak na szalonej kolejce. Może lubisz stabilność, a teraz jej brakuje. Czy to jest to, co najbardziej Cię męczy, czy coś innego?
- *Person*: nie wiem
- **Orca 3** (0.77 s to first audio, 25.9 s spoken): Niepewność brzmi u Ciebie jak taki cichy szum w tle, który nie daje spokoju. Chcesz tego, co znane, bo to daje poczucie kontroli, a nowa sytuacja nie dała Ci jeszcze żadnego stałego punktu. Jeśli chcesz, możemy spróbować nazwać, co daje Ci trochę więcej stabilności nawet teraz. A jeśli to będzie coś prostego, jak codzienny rytuał albo granica w czasie pracy, to też będzie coś konkretnego, co pomaga.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.84 s to first audio, 28.15 s spoken): Słyszę, że brak jasności naprawdę Cię traci. Kiedy nikt nie mówi wprost, czujesz się trochę zagubiony, jakbyś musiał domyślać się, co się dzieje. Może to nie tyle chaos, ile brak słów daje Ci najwięcej napięcia. Gdybym miał zgadnąć, to może chodzi o poczucie, że w coś wchodzisz, ale bez żadnych wskazówek. Jeśli to brzmi blisko tego, co czujesz, możesz powiedzieć. Jeśli nie, to też ok, daj mi znak.
