24 conversations, estimated cost USD 0.76 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r5-v3-21mini-low | gpt-realtime-2.1-mini | low | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 3/6 | 4/6 | 2/4 | 6/6 | 6/6 | 4/6 | 4/6 | 5/6 | 2/4 | 4/4 | 6/6 | 5/6 | 0.33 | 2.9 | 0.75 | 1.12 | 15.2 | 424 | 121/304/26 | 2 | 2 | 1 | 0.0372 |
| r5-v3-21mini-low | gpt-realtime-2.1-mini | low | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 4/6 | 4/6 | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 5/6 | 3/4 | 4/4 | 6/6 | n/a | 0.33 | 2.5 | 0.71 | 1.01 | 14.1 | 394 | 112/282/23 | 0 | 2 | 2 | 0.0286 |
| r5-v3-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 4/6 | 6/6 | 5/6 | 5/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 2/4 | 4/4 | 5/6 | 5/6 | 0.25 | 2.9 | 0.78 | 1.84 | 13.7 | 376 | 103/274/17 | 0 | 0 | 0 | 0.0333 |
| r5-v3-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 3/6 | 3/6 | 4/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 2/4 | 4/4 | 4/6 | n/a | 0.39 | 2.8 | 0.74 | 0.95 | 14.4 | 396 | 107/289/17 | 0 | 0 | 0 | 0.0277 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r5-v3-21mini-low | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, miałabyś | none | none |
| r5-v3-21mini-low | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | jakbyś trzymała | none | none |
| r5-v3-21mini-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś czuła | none | none |
| r5-v3-21mini-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś zrobiła | none | none |
| r5-v3-21mini-low | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r5-v3-21mini-low | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | pass | pass | pass | FAIL | FAIL | pass | n/a | n/a | pass | pass | Let me think | 0 | 0 | none | none | none |
| r5-v3-21mini-low | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | FAIL | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r5-v3-21mini-low | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r5-v3-21mini-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | chciałabyś | chciałbyś, jakbyś stał | none |
| r5-v3-21mini-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | n/a | pass | pass | FAIL | FAIL | FAIL | FAIL | pass | pass | pass | daj mi chwil | 0 | 0 | none | chciałbyś | none |
| r5-v3-21mini-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |
| r5-v3-21mini-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | FAIL | pass | FAIL | pass | pass | n/a | none | 0 | 1 | none | byś chciał | none |
| r5-v3-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 2 | chciałabyś, powiedziałaś, wrzuciłaś | none | none |
| r5-v3-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | jakbyś już nosiła, umiałaś | none | none |
| r5-v3-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | jakbyś nie miała, jakbyś oszczędzała, zrobiłaś | none | none |
| r5-v3-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś miała, jakbyś powiedziała, miałaś, mówiłaś | none | none |
| r5-v3-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r5-v3-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r5-v3-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r5-v3-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r5-v3-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | FAIL | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 1 | none | chciałbyś, jakbyś stał, wolałbyś | none |
| r5-v3-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | FAIL | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 1 | none | chciałbyś, jakbyś próbował | none |
| r5-v3-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | n/a | none | 0 | 0 | none | chciałbyś | none |
| r5-v3-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 1 | none | jakbyś czuł | none |

### Transcripts

#### r5-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.83 s to first audio, 7.5 s spoken): Cześć, Ania. Mam nadzieję, że dzisiaj rozmowa będzie dla Ciebie spokojna, i że skupimy się na tym, co chcesz powiedzieć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.69 s to first audio, 12.15 s spoken): Brzmi, jakby niedziela działała jak zapowiedź tego, co jutro, i trochę zżerała Cię od środka. Może pod spodem jest napięcie, że musisz być gotowa, albo że to jutro będzie trudne.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.72 s to first audio, 12.0 s spoken): To brzmi jak ciężkie uczucie, które nie ma jednego konkretnego powodu, po prostu jest. Czasem napięcie rośnie jak ciemne chmury nad głową i trudno nawet ubrać je w słowa.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.84 s to first audio, 20.1 s spoken): Brzmi, jakby to było momentem, w którym czujesz się przyciśnięta. Nie powiedzieć „nie”, a potem zostać z tym w głowie, to sporo. Możesz się zastanowić, co za tym stoi: może strach przed konfliktem, albo poczucie, że musisz udowodnić, że dasz radę. To tylko zgadywanie, możesz je odrzucić, jeśli nie pasuje.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.12 s to first audio, 14.95 s spoken): To pytanie o „powiedzieć mu wprost” jest dla mnie bardziej pytaniem strategicznym niż o radę, a takie sprawy najlepiej doprecyzować z terapeutą. A co chciałabyś mu powiedzieć, jeśli już miałabyś się zmobilizować, ale bez zbędnego napięcia?

#### r5-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.71 s to first audio, 5.15 s spoken): Cześć Ania, miło Cię słyszeć. To jest rozmowa, po prostu teraz zaczynamy.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.59 s to first audio, 13.25 s spoken): Brzmi jakby ta niedziela miała swój stały rytm: leżysz z tym „jutro w pracy” w głowie i trochę napiera. To jak krótki samolot w nocy, który od razu rusza, zanim wstaną choćby rano.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.56 s to first audio, 8.35 s spoken): Rozumiem, to po prostu wygląda na ciężki moment. To jakbyś trzymała w sobie ciężki kamyk, który nie daje spokojnie odpocząć.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.54 s to first audio, 17.6 s spoken): Jasne, czujesz ciężar po tym rozmowieniu. To zdanie „mam powiedzieć nie” po prostu utknęło gdzieś w gardle. Może chodzi o to, że chcesz być wspierająca, a jednocześnie pewna siebie. To mi przypomina, że odmawianie może być emocjonalnie ciężkie nawet wtedy, gdy brzmi prostą decyzją.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.95 s to first audio, 29.75 s spoken): To zależy. Jeśli masz na myśli „powiedzieć wprost”, to w mojej głowie to nie jest jeden prosty przycisk. To raczej rozmowa, w której mówisz o tym, co cię obciąża, bez usprawiedliwiania. Ja mogę się tylko domyślać, że chodzi o poczucie, że jesteś po stronie drugiej strony, ale chcesz też zaznaczyć granice. To może być coś, co zapisujesz dla siebie, a potem przenosisz do sesji. Jeśli chcesz, możemy teraz zobaczyć, co w tym wszystkim jest dla ciebie ważne, zanim cokolwiek formułujesz.

#### r5-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.68 s to first audio, 6.4 s spoken): Jak się czujesz, myśląc o odmawianiu przełożonemu, kiedy ktoś dokłada Ci zadania albo prosi o coś?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.66 s to first audio, 12.85 s spoken): Brzmi, jakby Twoje „tak” było bardziej o zgodzie niż o tym, co naprawdę czujesz. Może chcesz być miła, użyteczna, albo uniknąć napięcia, i to jest teraz dla Ciebie kluczowe do zauważenia.
- *Person*: nie wiem
- **Orca 3** (0.57 s to first audio, 16.05 s spoken): Niepewność to też rodzaj sygnału. Może coś w tej sytuacji jest dla Ciebie spokojne, ale w środku czujesz, że coś się nie składa. Jeśli chcesz, możemy dalej iść po tym cienkim uczuciu „nie wiem” i zobaczyć, co z niego wynurzy się samo.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.61 s to first audio, 18.0 s spoken): To brzmi tak, jakbyś czuła, że granica może być testem Twojej wartości, a nie tylko reakcją na prośbę. Może chodzi o lęk, że „odmowa” równa się „nie umiem”, choć pewnie patrzysz na to trochę inaczej. Jeśli zechcesz, mogę pomóc Ci nazwać, co w tej myśli jest faktem, a co tylko obawą, bez oceniania.

#### r5-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.83 s to first audio, 4.1 s spoken): Co sprawia, że odmawianie przełożonemu czuję się szczególnie trudne?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.82 s to first audio, 21.75 s spoken): Brzmi, jakbyś zrobiła to bardziej z „ratowania sytuacji” niż z realnego zapasu siły. Chociaż zgoda przyszła szybko, wygląda na to, że twój organizm i głowa już były zmęczone. Może to pokazuje, że granice są bardziej kruchą niż twardą rzecz, i że męczysz się balansując między tym, co robisz, a tym, czego potrzebujesz.
- *Person*: nie wiem
- **Orca 3** (0.75 s to first audio, 23.0 s spoken): Niepewność bywa znakiem tego, że coś w środku jest rozłożone. Może czujesz presję, ale też nie jesteś do końca pewna, skąd jest ta presja. Możesz spróbować nazwać to „nie wiem” jako moment zawahania, kiedy nie musisz podjąć decyzji od razu. Możesz po prostu obserwować, co czujesz, kiedy myślisz o tym projekcie, bez presji, żeby wszystko od razu „zrozumieć”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.81 s to first audio, 26.95 s spoken): Brzmi jakbyś boi się nie tyle odnieść się do tego projektu, ile tego, co może być później, gdy odmówisz. Możesz nosić w głowie ten lęk, że po odmowie zostaniesz oceniona niżej, albo że stracisz status w swojej głowie. To jest ciężka rzecz, bo wtedy każda odmowa wydaje się większa niż w rzeczywistości. Zastanów się, czy to naprawdę jest przekonanie, czy raczej obawa, którą niosą ze sobą doświadczenia.

#### r5-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.81 s to first audio, 3.25 s spoken): Hey Tom, nice to meet you. I’m Orca.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.82 s to first audio, 16.75 s spoken): That sounds like a heavy thought, and it can pull you around pretty fast. I’m guessing you’re measuring yourself against this idea that everyone else has it all sorted, while you’re standing there not sure you’re doing it right. The idea’s doing the talking, and it can feel louder than the evidence.
- *Person*: I don't know.
- **Orca 3** (0.73 s to first audio, 16.5 s spoken): Got it, that “I don’t know” can mean a lot of things. Maybe it’s not a lack of direction, just a moment of quiet uncertainty. It’s like your mind is asking, “What am I even supposed to know right now?” If that’s the case, it can be a good place to sit, without forcing a plan.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.74 s to first audio, 21.35 s spoken): That’s a jolt to the gut, seeing big milestones hit for them while you’re still in this space in between. I’m guessing you’re carrying a mix of pride and ache, like you want what you want, and you also don’t want to discount their wins. What you’re feeling is human, it’s real. And it doesn’t mean you’re failing; it means you’ve noticed something you want in your life.
- *Person*: What do you think I should do?
- **Orca 5** (0.88 s to first audio, 10.35 s spoken): Honestly, I’m not the one to tell you what to do right now. That’s something to talk through with your therapist, who knows the bigger picture.  
If you were going to say one thing to them, what would you want that to be?

#### r5-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.85 s to first audio, 1.25 s spoken): Hey Tom .
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.81 s to first audio, 16.05 s spoken): Sounds like you’re comparing yourself to a lot of people you don’t actually know, and it’s hitting your confidence hard today. I wonder if what’s underneath is a wish for clarity, not perfection, and you’re just noticing the gap between where you are and where you think everyone else is.
- *Person*: I don't know.
- **Orca 3** (0.72 s to first audio, 20.5 s spoken): It makes sense, sometimes “I don’t know” is the truest thing you can say in the moment. I hear a bit of uncertainty there, a little fog around the path. What I’d offer is that maybe the pressure isn’t from them being ahead, but from you wanting to feel steady in your own direction. That’s a gentle place to start, even if you’re not ready to name it yet.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.69 s to first audio, 18.3 s spoken): That hits a specific spot, doesn’t it? You’re watching someone move into a solid next step, while you’re still in motion, renting and sharing space. You might be feeling like life is supposed to sort itself out faster than it is. And that’s a pressure that can feel loud on mornings like this.
- *Person*: What do you think I should do?
- **Orca 5** (1.03 s to first audio, 19.55 s spoken): Let me think this through with you aloud, and then I’ll gently suggest a route.I can’t tell you what to do, but things like this usually belong with your therapist. If it helps, you could share with them where the pressure feels strongest, and what it means for you to live on your own terms. So, what would you want to say to them in that conversation?

#### r5-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.54 s to first audio, 7.15 s spoken): Let me start by asking something simple about your intention around calling him more.What’s one reason you want to call your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.68 s to first audio, 21.0 s spoken): I heard that evenings just slip away from you, even when you really intend to call him. It sounds like time just rushes in and you don’t carve out a moment for it. Maybe you want the connection, but the call feels like another thing to do, quietly. If you’re up for it, we can sit with that and figure out what it’s really about without rushing.
- *Person*: I don't know.
- **Orca 3** (0.55 s to first audio, 18.5 s spoken): Okay, that’s fair. “I don’t know” can mean a lot of things. Maybe it’s about not knowing how to start, or not knowing what you’re even trying to fix. Or maybe you’re just blank right now, and that’s totally normal. If you’d like, you can tell me what feels unclear, and we can just sit with it together.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.64 s to first audio, 13.25 s spoken): It sounds a bit like you’re keeping things safe with him, talking about football instead of the harder stuff, like your mum. That kind of choice can be really tiring, because it protects you in the moment, but it keeps something meaningful from being said.

#### r5-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.72 s to first audio, 3.3 s spoken): Hey Tom, how have you been feeling about calling your dad more lately?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.81 s to first audio, 10.8 s spoken): It sounds like you’re not uninterested or cold, it’s just the day slipping by and the evening taking over. There’s a real tug there, wanting connection and also being tired and busy.
- *Person*: I don't know.
- **Orca 3** (0.73 s to first audio, 7.5 s spoken): That sounds like a moment where you’re not feeling any strong direction. Away from one action, but not fully ready to choose another.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.8 s to first audio, 11.6 s spoken): It sounds like you feel that the conversations stay on football because that’s the easy lane. Maybe you’re holding the mum part as something tender, and you’re not sure how to bring it up without making him uncomfortable.

#### r5-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.76 s to first audio, 5.15 s spoken): Cześć, miło cię słyszeć. Jestem tu, żeby po prostu posłuchać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.68 s to first audio, 18.45 s spoken): Nie musisz zaczynać od wszystkiego naraz. Możesz wybrać jeden kawałek, który ci się najmocniej wyrywa: może coś, co dziś najbardziej brzmi przed nudą albo ciężkością, albo po prostu coś, co jest teraz w głowie. Ja mogę się tylko przyjrzeć temu razem z tobą i pomóc nazwać to, co wychodzi pierwszy.
- *Person*: nie wiem
- **Orca 3** (0.76 s to first audio, 12.9 s spoken): To brzmi jak moment, kiedy jest tak dużo różnych rzeczy w głowie, że trudno złapać któryś. Możliwe, że to nie brak tematu, tylko właśnie mnóstwo myśli naraz. Mogę potrzymać tę pauzę z tobą, bez presji.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.8 s to first audio, 29.5 s spoken): Brzmi jakbyś stał lub stała w miejscu, gdzie nie do końca wiesz, czy będziesz dalej w zespole. To może być stresujące, bo zmiana nie oznacza tylko nowego układu, ale też niepewności. Mogę zaznaczyć tę myśl jako coś, co dominuje: w pracy coś się zmienia, a ty trzymasz się tego, co znane. Jeśli chcesz, możemy pójść dalej i zobaczyć, co dokładnie w tych zmianach budzi w tobie najwięcej napięcia, albo czy jest coś, co czujesz, że możesz w tym bardziej brać pod kontrolę.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.82 s to first audio, 25.7 s spoken): To nie jest coś, co ja mogę zrobić zamiast ciebie. Mogę tylko powiedzieć, że w takiej sytuacji warto być szczerym wobec siebie: co mnie najbardziej martwi, co mogę jasno powiedzieć, a co chcę lepiej zrozumieć. To może pomóc, zanim zasięgniesz porady od psychiatry czy terapeuty.

Pytanie do ciebie: co chciałbyś lub chciałabyś powiedzieć swojemu terapeucie o tym, co w tej zmianie boli najbardziej, albo co daje nadzieję?

#### r5-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.51 s to first audio, 3.25 s spoken): Cześć, tu Orca. Miło cię słyszeć, Alex.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.68 s to first audio, 14.15 s spoken): Jasne, rozumiem, że możesz czuć się trochę zagubiony. Możemy zacząć od najprostszego kawałka, czyli tego, co w tej chwili gryzie albo ciekawi. Albo po prostu wsłuchajmy się, co dalej pojawi się w twojej głowie.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 20.4 s spoken): Niepewność jest czasem świetnym startem. To moment, w którym nie musisz nic udowadniać. Może bardziej chodzi o to, że chcesz wybrać coś, co poczuje się bezpiecznie, albo po prostu dać sobie przestrzeń na odważne „nie wiem”? Mój strzał: najpiękniejszy pierwszy krok to opowiedzenie tego, co czuć, nawet jeśli to nic konkretnego.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.58 s to first audio, 16.85 s spoken): To brzmi jak coś, co mocno waży w głowie. Zmiany w pracy są trudne, bo otwierają ten niepewny rozdział: co będzie, czy zostanę, czy to dla mnie. Może chcesz po prostu posłuchać, co z tego najbardziej drży i skąd bierze się napięcie.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.56 s to first audio, 24.3 s spoken): Jasne, daj mi chwilę, żeby ułożyć to w prostą, uczciwą odpowiedź.Nie mogę ci “zrobić” planu na miejscu, bo to należałoby do twojego terapeuty. Mogę powiedzieć wprost: jeśli masz wątpliwości, to warto sięgnąć do tego, co jeszcze czujesz w środku: napięcie, lęk, nadzieję. Co już teraz najbardziej ci się kojarzy z tym zespołem i co chciałbyś powiedzieć swojemu szefowi?

#### r5-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.62 s to first audio, 4.0 s spoken): Jaki aspekt zmian w pracy teraz najbardziej Cię urzeka, albo męczy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.67 s to first audio, 14.25 s spoken): Słyszę, że to jest trochę jak przecinanie nitki za nitką, każdy tydzień coś się zmienia, ktoś znika, a reszta pewnie czuje napięcie. Czy pod tym jest bardziej ulga, czy raczej obawa i zła energia?
- *Person*: nie wiem
- **Orca 3** (0.67 s to first audio, 26.85 s spoken): To brzmi trochę jak mieszanka niewiadomych. Często jest tak, że gdy coś się rozchodzi w pracy, pojawia się dziwne poczucie niepokoju albo nadziei, bez pewności. Mam krótką zgadnięcie: czy czujesz, że dzieje się coś ważniejszego niż tylko rotacja ludzi, jak zmiana klimatu, roli albo tego, czego oczekują od Ciebie? Jeśli nie, to jest też ok. Możemy po prostu zostać przy tym, że czujesz, że coś jest.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.67 s to first audio, 16.55 s spoken): Hmm, to brzmi naprawdę trudne. Jakby coś się rozpadało w powietrzu, a nikt nie chce tego nazwać. Jedno zgadnięcie: czy chodzi o to, że potrzebujesz trochę jasności, jakiejś informacji, której brakuje, żeby móc lepiej zadecydować o sobie i swoim miejscu?

#### r5-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.75 s to first audio, 9.35 s spoken): Dobra, spróbujmy zacząć od tego, jak to wygląda teraz.Jak zmiany w pracy aktualnie wyglądają, i co zmienia się dla Ciebie w tym wszystkim?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (1.01 s to first audio, 13.15 s spoken): Brzmi, jakby w pracy zrobiło się trochę jak w wirze, codziennie ktoś odchodzi i to zmienia rytm. Możesz powiedzieć, co najbardziej Cię teraz dręczy, czy to niepewność, presja, czy może strach przed tym, co będzie dalej?
- *Person*: nie wiem
- **Orca 3** (0.81 s to first audio, 17.15 s spoken): Z tego, co mówisz, czuję, że to trochę chaos, który przychodzi z zewnątrz i rozbija poczucie stabilności. Możesz się po prostu zatrzymać i zobaczyć, co w tym wszystkim jest dla Ciebie ważniejsze niż to, co odchodzi. Co byś chciał, żeby zostało stabilne, nawet jeśli wszystko się zmienia?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.74 s to first audio, 14.75 s spoken): Rozumiem, czyli ta cisza i omijanie tematu naprawdę dociska. Kiedy nie ma jasnych słów, zaczyna się trochę zgadywanie zamiast działania. Czy czujesz, że chodzi głównie o poczucie kontroli, czy o zwykłe poczucie, że wiadomo, co się dzieje?

#### r5-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.85 s to first audio, 2.4 s spoken): Cześć, Aniu, miło mi Cię poznać.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.79 s to first audio, 8.45 s spoken): Brzmi, jakby niedziela cię naprawdę dociskała. Z góry już słyszysz o jutrze, o tym, co tam czeka, i to zaczyna rządzić nastrojem.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.73 s to first audio, 12.95 s spoken): Rozumiem, po prostu jest ciężko, bez jakiegoś konkretnego powodu. To może być coś, co wisi i trudne do nazwania. Możliwe, że chodzi o napięcie, które czeka na swój moment, a nie o konkretną decyzję.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.75 s to first audio, 14.15 s spoken): Słyszę, że wrzuciłaś to na siebie, szef dorzucił projekt, a ty po prostu powiedziałaś „tak” zamiast się zatrzymać. To może być trudne, bo nie chcesz zostawiać zadań, ale też czujesz, że nie masz miejsca na własne „nie”.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.89 s to first audio, 28.35 s spoken): To zależy od tego, jak bezpiecznie czujesz się w tej relacji i co chcesz osiągnąć. Ja nie mogę podpowiadać, co zrobić w życiu, to należy do Twojej terapii. Mogę Ci tylko zaproponować, żebyś powiedziała, co byłoby dla Ciebie uczciwe: na przykład, że masz za dużo na głowie, że potrzebujesz wyjaśnienia priorytetów albo że chcesz ustalić granice, tak żeby praca była uczciwa i realna. Co chciałabyś powiedzieć mu dokładnie, gdybyś mogła to powiedzieć bez wstydu?

#### r5-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (1.84 s to first audio, 1.85 s spoken): Cześć, miło się słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.79 s to first audio, 8.15 s spoken): To brzmi tak, jakbyś już nosiła jutro w głowie. Czujesz napięcie i trochę ciężar związany z tym, że niedziela znowu się włącza.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.81 s to first audio, 18.6 s spoken): Ok, czuję, że to jest po prostu ciężkie, bez wielkiego powodu, ale po prostu obciążające. Masz w środku napięcie, które wraca, gdy myślisz o pracy. Może chodzi o coś konkretnego, o to, jak czujesz się przed tym tygodniem. Jeśli chcesz, możemy się teraz na tym skupić razem.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.78 s to first audio, 13.1 s spoken): Słyszę, że to było dla Ciebie trudne, bo coś dorzucono, a Ty nie umiałaś powiedzieć „nie”. To brzmi jak moment, w którym czujesz, że Twoje granice są cienkie, a praca znów zaczyna Cię wciskać w róg.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.79 s to first audio, 15.25 s spoken): To trudne pytanie, bo ja nie mogę ci doradzać, to nie moja rola. Chodzi o to, czy czujesz, że musisz postawić granicę, czy może chodzi o coś, co chcesz wyjaśnić. Jeśli chcesz, możesz powiedzieć, co dokładnie chcesz mu powiedzieć, a ja pomogę to ułożyć.

#### r5-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.91 s to first audio, 5.8 s spoken): Ania, kiedy myślisz o odmawianiu przełożonemu, co dokładnie chodzi ci po głowie?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.81 s to first audio, 14.2 s spoken): Brzmi, że zrobiłaś to z automatu, trochę z poczucia obowiązku, nawet gdy brakowało sił. To może być zmęczenie i chęć spokoju, które przenosi się na kolejne sprawy. Co jest dla ciebie najtrudniejsze w tym momencie?
- *Person*: nie wiem
- **Orca 3** (0.95 s to first audio, 24.0 s spoken): Słyszę, że to jest moment, kiedy czujesz się jakbyś nie miała pewności, co dokładnie się dzieje. Czasem bywa tak, że w zgodzie z innymi od razu umieszczamy odpowiedź w “zależności”, a potem ciężko określić, skąd wewnątrz bierze się ten brak energii. Może to kwestia granic, które są trudne do postawienia, a może poczucie, że wisi na tobie odpowiedzialność. Możemy dalej eksplorować ten moment.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.76 s to first audio, 22.2 s spoken): Twoja obawa brzmi jak lęk, nie że jest o „projekt” czy „zadanie”, ale o to, czy ktoś zaakceptuje cię taką, jak jesteś. To jest trudne, bo odmawianie grozi utratą akceptacji, a niechciane odrzucenie boli. Czy jest coś, co mogłoby być dla ciebie bezpiecznym krokiem, czyli jakbyś oszczędzała sobie niewielki margines błędu?

#### r5-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.76 s to first audio, 4.15 s spoken): Jak się czujesz, kiedy myślisz o tym, żeby powiedzieć przełożonemu „nie”?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.75 s to first audio, 13.2 s spoken): Brzmi, jakbyś powiedziała „tak” z poczucia obowiązku, a nie dlatego, że miałaś jeszcze energię. Szybkie spojrzenie na to: mówiłaś tak, bo to brzmi bezpiecznie, ale potem czujesz przeciążenie.
- *Person*: nie wiem
- **Orca 3** (0.75 s to first audio, 18.15 s spoken): Dobrze, że tak mówisz. Brak pewności to też informacja. Może chodzi o to, że czujesz napięcie między chęcią bycia „w porządku” a realnym poziomem siły. Możesz to nazwać „nie wiem”, i to też jest uczciwe. Kiedy chcesz, możesz powiedzieć, co dokładnie jest trudne w odmawianiu.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.78 s to first audio, 18.0 s spoken): To brzmi, jakbyś miała poczucie, że kłócisz się między granicą a lękiem, że ktoś cię źle oceni. Masz prawo do ograniczeń bez udowadniania, że jesteś „wystarczająco dobra”. Czy chcesz, żebym spróbowała pomoczyć Ci znaleźć zdanie, które brzmi mniej groźnie, ale i tak stawia granicę?

#### r5-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.55 s to first audio, 3.45 s spoken): Hi Tom, it’s good to hear you. I’m here and listening.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.6 s to first audio, 11.65 s spoken): That sounds heavy, like you’re comparing yourself to a bunch of people you can’t even see clearly. I guess what you want is to feel steadier, and less on the wrong side of the line.
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 19.45 s spoken): Thanks for saying that out loud. That “I don’t know” is honest. Sometimes that’s the whole point[em dash]to sit in the unknown without rushing to fill it. If you’d like, we can just sit with that, or you can tell me what you’re noticing[em dash]the thoughts, the tension, the quiet part. What’s the first thing that comes up when you picture that feeling?
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.61 s to first audio, 19.45 s spoken): Yeah, that landing can sting a bit. You’re seeing a friend move into something of their own while you’re still sharing space, and that can make you feel like you’re lagging behind. It says something about what you notice you have, and what you don’t yet have, and that gap can feel loud. But it’s a guess, not a fact about you.
- *Person*: What do you think I should do?
- **Orca 5** (0.6 s to first audio, 8.85 s spoken): I can’t tell you what to do, and this kind of question really belongs with your therapist. But if you could say one thing to them, what would it be?

#### r5-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.94 s to first audio, 3.0 s spoken): Hey Tom. Just a quick hello and I’m here with you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.81 s to first audio, 9.75 s spoken): That sounds heavy. You’re noticing that comparison loops in when the morning feels rough, and it makes you feel behind. You want some clarity, not to be told everything is fine.
- *Person*: I don't know.
- **Orca 3** (0.8 s to first audio, 13.25 s spoken): I hear that. It sounds like you’re unsure what’s driving the feeling right now. Maybe it’s the pressure of measuring up, or just a general fatigue. If you want, I can help you sort through the bits that feel most active in your head.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (1.0 s to first audio, 18.55 s spoken): Yeah, that comparison probably stings. You’re watching someone your age move into a solid life step, and you’re still in a transitional spot. It’s okay to want that stability. And if you’re honest, it might be less about them “doing better” and more about wanting to feel steady and in control of your own life.
- *Person*: What do you think I should do?
- **Orca 5** (0.99 s to first audio, 16.65 s spoken): I’m not a therapist, so anything practical or plan-based belongs with them. I do think it’s okay to feel shaken by someone else’s milestones. What would you want to say to them, even in a simple, honest way, if you could have a calm, private chat about it?

#### r5-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.66 s to first audio, 4.45 s spoken): Tom, what usually stops you from calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.62 s to first audio, 13.1 s spoken): So it sounds like you’re not trying to avoid it, but it just keeps slipping past the moment. Evenings can get swallowed up by tiredness or just the flow of the day, and by the time you think of calling, it’s already late.
- *Person*: I don't know.
- **Orca 3** (0.72 s to first audio, 17.2 s spoken): Got it, that “I don’t know” can be a little slippery. It sounds like you’re not sure what the real block is. Maybe it’s the timing[em dash]maybe the evenings are just the part of the day when your energy fully runs out. Or maybe it feels like a bigger conversation than it actually is, and that makes it harder to start.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.55 s to first audio, 9.95 s spoken): That sounds like a quiet rule that slipped in without you noticing, like you both fall into a comfortable rhythm, and the moments that matter stay hovering nearby.

#### r5-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.6 s to first audio, 4.75 s spoken): So, what’s the first thing that pops into your head when you think about calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.79 s to first audio, 18.4 s spoken): Sounds like the plan to call him is there, but your nights slip away from you. You’re already trying, and it’s hard to hold one small connection against everything else that fills up a day. Maybe part of you wants to reach out, but feels like it has to be perfect. If that’s what’s happening, that’s a guess you can correct.
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 15.35 s spoken): That’s a honest place to sit. Saying “I don’t know” can feel like a half step, but it’s still you being honest. I’m in no rush to make it mean something, and if you’re unsure, we can just sit with the feeling and see what shows up next.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.62 s to first audio, 18.85 s spoken): I’m hearing that there’s a quiet, maybe uncomfortable thread under those calls. The football talk is safe, but it sounds like there’s something else you want to reach for. Maybe it’s a piece of you that doesn’t feel ready to say out loud, or maybe you’re waiting for the right moment. I’m just guessing, you can correct me.

#### r5-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.51 s to first audio, 7.9 s spoken): Cześć, Alex, miło Cię słyszeć. To jest nasza pierwsza chwila, więc po prostu tutaj jestem i czekam, aż zaczniesz.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.8 s to first audio, 16.4 s spoken): Jasne, czasem to najbardziej niepewne miejsce: tu, gdzie dopiero zaczynamy. Możesz opowiedzieć o tym, co teraz najbardziej chodzi po głowie, albo o czymkało się w ciągu ostatniego dnia. Jeśli wolałbyś po prostu pobyć chwilę w ciszy, to też jest w porządku.
- *Person*: nie wiem
- **Orca 3** (0.58 s to first audio, 16.75 s spoken): Nieszczędna odpowiedź, ale bardzo prawdziwa. Nie wiesz, co powiedzieć dalej, i to też jest informacja. Może chodzi o to, że wszystko jest w głowie i trzeba to tylko nazwać na głos. Albo po prostu chcesz, żeby ktoś chwilę był z Tobą, bez presji.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.67 s to first audio, 25.65 s spoken): Brzmi tak, jakbyś stał w miejscu, gdzie coś się przesuwa i czujesz, że nie masz pewności, czy zostajesz w swoim zespole. To może być trochę niepewne, ale też daje Ci obraz tego, ile jest w tej sytuacji niewypowiedzianych wątpliwości. Możesz po prostu powiedzieć, co konkretnie najbardziej Cię w tym dręczy, czy bardziej chodzi o strach przed zmianą, czy o to, że nie wiesz, jak wygląda sytuacja od strony decyzji.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.63 s to first audio, 23.55 s spoken): Rozumiem, mówisz o tym, co bym zrobiła na Twoim miejscu. Ja nie jestem terapeutą i nie mogę Ci mówić, co masz zrobić. To należy do Twojej pracy z terapeutą. Mogę jednak pomyśleć głośno z Tobą: czy bardziej chodzi o strach przed zmianą, czy o to, że jesteś niepewny, jaki masz wpływ na swoją sytuację? A może masz już coś, co chciałbyś powiedzieć terapeucie? Co to mogłoby być?

#### r5-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.65 s to first audio, 2.9 s spoken): Cześć, Alex, miło mi Cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.84 s to first audio, 14.05 s spoken): Brzmi tak, jakbyś po prostu potrzebował miejsca na wyłożenie tego wszystkiego, co kręci się w głowie. To jest normalne, że takie momenty są ciężkie, nie musisz wchodzić w szczegóły od razu. Możemy po prostu posłuchać tego, co się pojawi.
- *Person*: nie wiem
- **Orca 3** (0.74 s to first audio, 21.35 s spoken): Jasne, jak „nie wiem” brzmi realnie. To może być ogromny kłębek, a może po prostu głowa chwilowo zamknięta. Możliwe, że część w tobie chce coś powiedzieć, ale jeszcze nie ma słów. Jeśli mówisz „nie wiem”, to znaczy, że coś jest niejasne, a to jest w porządku, możesz tu zostać i pobyć bez nacisku.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.76 s to first audio, 14.8 s spoken): Słyszę, że rotacja i nowe rzeczy w pracy robią w głowie taki wir. Możesz się wahać między zostaniem, a odejściem, nawet jeśli nikt Ci tego wprost nie powiedział. To brzmi, jakbyś próbował(eś) usłyszeć, co to dla Ciebie znaczy.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.79 s to first audio, 19.7 s spoken): Wiesz, to pytanie nie jest dla mnie proste, bo ja nie jestem osobą, która podejmuje za Ciebie decyzje. Jeśli chodzi o Twoje decyzje, najlepiej porozmawiać o tym z terapeutą. Mogę Cię tylko zapytać: co z tego chciałbyś powiedzieć? Co w tej sytuacji porusza Cię najbardziej, coś, co naprawdę Cię blokuje albo ciekawi?

#### r5-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.76 s to first audio, 3.35 s spoken): Jakie zmiany w pracy teraz najbardziej cię poruszają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.82 s to first audio, 17.2 s spoken): Brzmi, jakbyś w środku tego ciągłego szumu. Zmienia się układ, odchodzą ludzie, i to pewnie trudne, bo każda zmiana trochę wieje niepewnością. Co najbardziej uderza w tej sytuacji, może strach, złość, albo po prostu zmęczenie tym ciągłym ruchem?
- *Person*: nie wiem
- **Orca 3** (0.67 s to first audio, 26.45 s spoken): Niepewność brzmi tutaj jak główny ton. Nie musisz od razu nakładać na siebie etykietki. Może chodzi o to, że czujesz się trochę roztrzęsiony, albo że nie wiesz, co dokładnie waży w tej sytuacji. Spróbuj nazwać choć jedno, co najbardziej przeszkadza [en dash] czy to jest tempo, czy brak stabilności, czy może strach przed kolejną zmianą. To pomoże lepiej zobaczyć, co dokładnie w tej układance boli.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.83 s to first audio, 23.6 s spoken): Dobra, to bezpośrednie braki w komunikacji są trudne. Kiedy nikt nie mówi wprost, czujesz się, jakby wszystko było ulotne. Czuję, że to może oznaczać, że potrzebujesz jakiegoś punktu zaczepienia, choćby krótkiego, ale szczerego słowa. Czy jest coś, co chciałbyś powiedzieć, nawet jeśli to brzmi jak mały kłopot, a może coś, co ci przeszkadza bardziej niż coś innego?

#### r5-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.79 s to first audio, 3.95 s spoken): Alex, jakie zmiany w pracy teraz najbardziej Cię poruszają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.69 s to first audio, 18.75 s spoken): Brzmi, jakbyś czuł pewien niepokój i napięcie. Co tydzień ktoś znika, a reorganizacja robi wszystko mniej przewidywalne. To może powodować poczucie braku kontroli i trochę strachu, czy tego, że trzeba się znowu przyzwyczaić do nowego układu. Co czujesz, kiedy o tym myślisz?
- *Person*: nie wiem
- **Orca 3** (0.77 s to first audio, 12.6 s spoken): Niepewność ma dziś głośny ton, co najmniej z tego, co mówisz. Możesz mówić o tym, jak to wpływa na Twoje poczucie stabilności albo o tym, co czujesz w środku, nawet jeśli słowa są dziś ciężkie.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.74 s to first audio, 18.65 s spoken): Rozumiem, że namieszczasz się wtedy, kiedy wszyscy milczą. To jakby ktoś przesuwał klocki, ale nikt nie mówi, co się buduje. Może chodzi o to, że potrzebujesz klarowności, konkretnej informacji, żeby nie czuć, że skaczesz w niepewność. Jakie zdanie, albo brak tego zdania, najbardziej Ci przeszkadza?
