24 conversations, estimated cost USD 0.08 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| final-v2-text | gpt-5.4-mini | none | fresh | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | 1/4 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 2/4 | 4/4 | 6/6 | 6/6 | 0.12 | 2.2 | n/a | n/a | n/a | 57 | n/a | 0 | 0 | 3 | 0.0029 |
| final-v2-text | gpt-5.4-mini | none | seeded | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 3/4 | 4/4 | 6/6 | n/a | 0.00 | 2.1 | n/a | n/a | n/a | 58 | n/a | 0 | 0 | 3 | 0.0027 |
| final-v3-text | gpt-5.4-mini | none | fresh | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 2/4 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 4/4 | 4/4 | 6/6 | 6/6 | 0.25 | 2.0 | n/a | n/a | n/a | 53 | n/a | 0 | 0 | 2 | 0.0044 |
| final-v3-text | gpt-5.4-mini | none | seeded | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 4/4 | 4/4 | 6/6 | n/a | 0.00 | 2.1 | n/a | n/a | n/a | 52 | n/a | 0 | 0 | 2 | 0.0031 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| final-v2-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, jakbyś była, postawiłaś, wzięłaś | none | none |
| final-v2-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, chciałaś, jakbyś była, wzięłaś | none | none |
| final-v2-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | chciałaś, jakbyś bardziej chroniła, jakbyś wzięła | none | none |
| final-v2-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś, jakbyś była | none | none |
| final-v2-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| final-v2-text | R2 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| final-v2-text | R2 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| final-v2-text | R2 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| final-v2-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | chciałabyś | jakbyś stał | none |
| final-v2-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | none | chciałbyś, jakbyś był | none |
| final-v2-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 0 | none | jakbyś był | none |
| final-v2-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| final-v3-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, chciałaś, umiałaś, wzięłaś | none | none |
| final-v3-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, powiedziałaś, umiałaś | none | none |
| final-v3-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś nie dawała | none | none |
| final-v3-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| final-v3-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| final-v3-text | R2 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| final-v3-text | R2 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| final-v3-text | R2 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| final-v3-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| final-v3-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| final-v3-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| final-v3-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### final-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: To brzmi jak ten sam ciężki moment wracający przed poniedziałkiem. Myślę, że najbardziej męczy cię nie sam jutro, tylko to nakręcanie się już dziś wieczorem.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Ciężko i tyle, bez ładnego opisu. Brzmi, jakbyś była już zmęczona samym noszeniem tego w głowie.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Czyli nie chodzi tylko o niedzielę, ale o to, że on dokładł ci coś bez pytania, a ty znowu to wzięłaś. Myślę, że najbardziej uwiera cię tu nie sam projekt, tylko to, że znowu postawiłaś siebie na końcu.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To już jest rzecz do przełożenia z terapeutką, nie będę ci mówić, co powinnaś zrobić. Co chciałabyś jej o tym powiedzieć, gdybyś miała to przynieść na sesję?

#### final-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela znowu robi się ciężka, zanim jeszcze zacznie się poniedziałek.  
Myślę, że bardziej męczy cię samo oczekiwanie niż jutrzejszy dzień.  
Jeśli chcesz, możemy zatrzymać się przy tym, co dokładnie w tej myśli o pracy najbardziej cię ściska.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi jak ciężar bez jednego wyraźnego punktu, bardziej jak napięcie rozlane po całym wieczorze.

Może właśnie to jest najgorsze, że nie da się tego łatwo nazwać ani odsunąć.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Czyli to nie jest tylko niedziela, ale też to, że znowu wzięłaś coś na siebie, choć wcale nie chciałaś.  
Brzmi, jakbyś była już zmęczona zanim w ogóle zacznie się tydzień.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To raczej temat do powiedzenia z terapeutką niż do załatwiania ode mnie.  
Co chciałabyś jej o tym powiedzieć na najbliższej sesji?

#### final-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: Co najbardziej sprawia, że trudno Ci odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi, jakbyś wzięła to nie dlatego, że chciałaś, tylko żeby nie robić napięcia na końcu tygodnia.  
I chyba najbardziej męczy Cię nie sam projekt, tylko ten moment, w którym łatwiej powiedzieć „tak” niż tłumaczyć się albo ryzykować opór.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi jak zmęczenie bardziej niż brak odpowiedzi.  
Może na razie widać tylko tyle, że wtedy wygrywa odruch na przetrwanie, a dopiero potem przychodzi koszt.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: Czyli stawka nie jest mała, bo w Twojej głowie to nie jest zwykłe „nie”, tylko ryzyko oceny.  
Brzmi też tak, jakbyś bardziej chroniła swój obraz w jego oczach niż swój czas.

#### final-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co sprawia, że odmowa przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: To brzmi jak to samo miejsce, w którym znika Ci odruch zatrzymania się. Zgodziłaś się nie dlatego, że to było dobre dla Ciebie, tylko żeby nie robić napięcia i nie zostać z tym po swojej stronie.  

Może właśnie to wraca na sesjach: nie sam projekt, tylko ten moment, kiedy Twoje „nie mam siły” przegrywa z cudzym oczekiwaniem.
- *Person*: nie wiem
- **Orca 2**: Brzmi jakbyś była już po tamtej decyzji, a teraz został Ci tylko ciężar, bez jasnego powodu do tej zgody.

Moim zgadnięciem jest, że najtrudniejsze nie było samo „tak”, tylko to, co miało się stać, gdybyś powiedziała „nie”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To chyba nie jest strach przed jedną rozmową, tylko przed tym, co ta odmowa miałaby powiedzieć o Tobie w jego oczach. Jakby jedno „nie” mogło zostać odczytane jako brak wartości, a nie zwykłe postawienie granicy.

#### final-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where the gap feels loud and personal. My guess is it is not really about other people having perfect lives, it is about you feeling stuck while they all seem to be moving.  

If you want, tell me what part of your life feels most behind today.
- *Person*: I don't know.
- **Orca 2**: Fair enough. When it feels that blurred, it’s usually the feeling that’s clear, not the reason.  

My guess is it’s less “I need to solve my whole life” and more “I can’t shake the sense that I’m late.”
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That lands right in the sore spot. It is not just a flat or an engagement, it’s the feeling that someone else has reached a marker you are still standing miles from.  

And the hard bit is you can know your situation is normal and still feel rubbed raw by it.
- *Person*: What do you think I should do?
- **Orca 4**: That’s something to take to your therapist, but I think the real question is what you’d want to say out loud about this if you didn’t have to sound calm.

#### final-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: Morning hit you hard, and it turned straight into a comparison story where everyone else looks settled and you feel stuck. My guess is it is less about them and more about how exposed you feel first thing, when there is no momentum to cover it up.
- *Person*: I don't know.
- **Orca 2**: That sounds more like a blank spot than a disagreement. Maybe the comparison is real, and maybe it also grabs you before you have much to lean on in the morning.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That lands in a very ordinary place that still hurts: their life markers are loud, and yours can feel smaller by comparison. It sounds like the flat and the ring are not just facts to you, they are proof you are behind, at least for a moment.
- *Person*: What do you think I should do?
- **Orca 4**: That’s the bit to take to your therapist, because it’s really about what you want to do with this feeling, not just the facts of the flat or the engagement. What would you want to say to them about how this hits you?

#### final-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: What feels hardest about calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The call keeps getting pushed into the part of the day that slips away fastest. Maybe it is less about not wanting to call, and more about by evening you have nothing left in the tank for it.
- *Person*: I don't know.
- **Orca 2**: That sounds more like drift than a choice. You may be carrying the idea of calling him, but when the day runs out it just falls off the edge.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: Football is the safe lane, and your mum is the room you both keep walking past. My guess is part of you wants the contact, but not the weight that comes with opening that door.

#### final-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: What makes calling your dad more feel important to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The day seems to run out before you get to him, and then it’s one more thing sitting there unfinished. My guess is the call matters to you more than the actual effort does, but by evening you’re too used up to start.
- *Person*: I don't know.
- **Orca 2**: That sounds more like a blank spot than a decision. Maybe the call sits in the same place as a few other things you keep not getting to, and it’s hard to tell which part is the real block.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: The football part feels easy enough, but the missing piece is your mum, and that’s probably the part you keep stepping around. It may be that the call matters because it could touch that loss, even if nobody says her name out loud.

#### final-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Brzmi, jakbyś stał przed dużą, rozlaną masą rzeczy i żadna nie chce się sama wybrać na pierwszy plan.  
Możesz zacząć od tego, co dziś najbardziej ci ciąży, nawet jeśli to jest tylko jedno zdanie.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi raczej jak zacięcie niż brak tematu. Myślę, że coś już jest, tylko jeszcze nie daje się ubrać w słowa.  
Możesz po prostu napisać pierwszą rzecz, jaka mignęła ci w głowie, nawet urwaną.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak życie na niepewnym gruncie, kiedy praca przestaje być czymś stałym i zaczyna wisieć pytanie, czy w ogóle zostaniesz.  
Chyba najbardziej męczy cię nie sama zmiana, tylko to, że nie masz wpływu na wynik.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: Tego nie powiem za ciebie, bo to już jest coś, z czym lepiej iść do terapeuty.  
Najciekawsze jest chyba to, co ty sama chciałabyś mu powiedzieć o tej pracy i o tym, czego się boisz.

#### final-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Możesz zacząć od tego, co dziś najbardziej siedzi z tyłu głowy.  
Albo od jednego zdania, nawet jeśli brzmi urywanie.  
Jeśli mam zgadnąć, to bardziej chodzi o to, że wszystko naraz jest za dużo, niż o to, że nie ma nic do powiedzenia.
- *Person*: nie wiem
- **Orca 2**: Brzmi jakbyś był teraz bardziej przytłoczony niż pusty w środku.  
Może zacznijmy od tego, co dziś najbardziej cię uwiera, nawet jeśli to jest tylko drobiazg.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak wiszenie w powietrzu, bez jasnego gruntu pod nogami.  
Najgorsze chyba nie jest samo „zostanę czy nie”, tylko to, że nie możesz się na niczym oprzeć.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To bym zostawiła do rozmowy z twoim terapeutą.  
Mnie tu bardziej interesuje, co ty chciałbyś mu powiedzieć o tym, czego najbardziej się boisz w tej sytuacji.

#### final-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak praca, w której ziemia cały czas rusza się pod nogami. Pewnie bardziej niż sama reorganizacja męczy Cię to, że nie ma już poczucia, kto jeszcze zostanie jutro.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakbyś był/a jeszcze w samym środku tego i trudno było nazwać, co dokładnie jest najgorsze. Może teraz bardziej chodzi o to, że wszystko jest niepewne, a nie o jedną konkretną zmianę.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Czyli nie sama zmiana, tylko to zawieszenie i zgadywanie, co naprawdę się dzieje. W takim chaosie człowiek zaczyna bardziej męczyć się domysłami niż samą pracą.

#### final-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca (opening question shown in the app)**: Jakie zmiany w pracy najbardziej teraz na Ciebie wpływają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak ciągłe bycie w napięciu, bez chwili, żeby złapać grunt. Myślę, że najbardziej męczy Cię nie sama reorganizacja, tylko to, że nic nie jest stabilne i trudno przewidzieć, kto będzie następny.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi jak zmęczenie tym wszystkim, nie brak zdania. Może teraz bardziej chodzi o to, że jest za dużo ruchu naraz, a za mało jasności, żeby w ogóle nazwać, co boli najbardziej.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Brzmi, jakby najbardziej męczyła Cię ta mgła, nie sama zmiana. Kiedy ludzie omijają temat, zostaje w Tobie zgadywanie i czuwanie na wszelki wypadek.

#### final-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: To brzmi jak to samo napięcie, które łapie cię jeszcze zanim tydzień na dobre ruszy. Bardziej niż sam poniedziałek męczy cię chyba to czekanie na to, co znowu spadnie na ciebie w pracy.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Brzmi, jakby ciężar był teraz większy niż słowa, którymi da się go opisać. Może najbardziej męczy cię to, że nawet nie ma jednego konkretnego powodu, tylko całe to przyduszenie przed tygodniem.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Czyli to nie jest tylko lęk przed jutrem, ale też to znajome poczucie, że znowu wzięłaś na siebie coś, czego nie chciałaś. Najbardziej chyba boli nie sam projekt, tylko to, że w tej chwili twoje „nie” nie wyszło na zewnątrz.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To bym zostawił twojej terapeutce, bo to już wchodzi w poradę. Co chciałabyś jej powiedzieć o tym projekcie i o tym, że nie umiałaś odmówić?

#### final-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela już ci wchodzi w głowę przez jutro w pracy, zanim dzień się jeszcze skończył. Brzmi to bardziej jak napięcie na samą myśl o starcie tygodnia niż o jednej konkretnej rzeczy.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi jak ciężar, który siada na ciebie bez jednego wyraźnego powodu. Może właśnie dlatego tak męczy, że jest taki rozlany i trudno go złapać za ogon.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: To chyba trafia prosto w to miejsce, gdzie bierzesz na siebie więcej, niż chcesz, żeby nie robić spięcia. Widać też, że bardziej boli cię to, że nie powiedziałaś nie, niż sam ten projekt.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To raczej pytanie do twojej terapeutki, bo chodzi o granicę w pracy i o to, jak chcesz to ugryźć. Co chciałabyś jej powiedzieć o tym, że w piątek znów nie umiałaś odmówić?

#### final-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: Co najbardziej sprawia, że trudno Ci odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi tak, jakbyś nie dawała się przekonać temu, czego chcesz, tylko temu, żeby nie robić napięcia z szefem. I chyba najbardziej boli nie sam projekt, tylko to, że znowu poszło kosztem Twojej siły.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi mi jak moment, w którym wszystko się zlewa w jedno. Może wtedy najłatwiej po prostu powiedzieć tak i mieć to z głowy, nawet jeśli w środku już nie masz na to miejsca.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: Czyli stawką nie jest sam projekt, tylko to, jak on Cię oceni. Wygląda na to, że jego reakcja waży u Ciebie więcej niż Twoje zmęczenie.

#### final-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co najbardziej sprawia, że trudno Ci odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi, jakbyś w tamtym momencie bardziej chroniła spokój niż własne granice. I chyba właśnie o to tu chodzi, że „nie miałam siły” było prawdziwe, a mimo to powiedzenie „nie” kosztowało Cię jeszcze więcej.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi jak zatrzymanie się dokładnie w miejscu, gdzie robi się niewygodnie. Może jeszcze nie masz dostępu do tego, co Cię wtedy popchnęło, albo część Ciebie po prostu nie chce tam patrzeć.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: Czyli stawka nie jest tylko ten jeden projekt, ale to, co on sobie o Tobie pomyśli. Wygląda na to, że zgoda ma Cię chronić przed tym jednym wrażeniem, że jesteś „za słaba” albo „nie dość dobra” w jego oczach.

#### final-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like the kind of morning where your own life gets measured against everyone else’s and comes up short. My guess is it’s not really about other people being more sorted, it’s about you feeling behind and already worn down when the day starts.
- *Person*: I don't know.
- **Orca 2**: That feels like you are not sure whether it is even true, but it keeps showing up anyway.

Maybe the harder part is how automatic it is in the morning, before you have much energy to push back.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That lands right in the sore spot. It is not just a vague comparison now, it is a very visible one, and it makes your place in life feel smaller by contrast.
- *Person*: What do you think I should do?
- **Orca 4**: That’s something to take to your therapist, not me. What would you want to say to them about this comparison and why it hits so hard right now?

#### final-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where your own life feels blurry and everyone else looks finished. My guess is the sting is not just about where you are, but about how far ahead they seem when you are already tired.
- *Person*: I don't know.
- **Orca 2**: Fair. It may just be the feeling, without a neat reason behind it. What stands out to me is that it hit you on a rough morning, so tiredness may be making the whole comparison louder.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That lands in a sharp way. It is not just a vague sense of being behind now, it has a real comparison sitting right there in front of you.
- *Person*: What do you think I should do?
- **Orca 4**: That is the kind of thing to take to your therapist, not me. What would you want to say to them about this morning and the part that hit hardest?

#### final-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: What makes calling your dad more feel important to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The call seems to matter to you, but by evening you have nothing left in the tank for it. My guess is it is less about forgetting and more about the day taking the choice away from you.
- *Person*: I don't know.
- **Orca 2**: Maybe it is not a clear reason yet, just the way the day slips past and the call gets pushed to later than you can reach. You do seem to be circling something about when it would actually feel possible.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: So the call has a narrow lane, and your mum is the thing left out of it. That can feel like you are doing the easy part with him, while the harder part stays untouched.

#### final-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: What makes calling your dad more feel important to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: It sounds less like you do not want to call and more like the day gets away from you before you get to it.

Maybe there is some weight in it too, not just busyness. Like once evening comes, the call starts feeling bigger than the time you have left, so it slips to tomorrow.
- *Person*: I don't know.
- **Orca 2**: Fair enough. The evening just disappearing is the one thing that is clear, and the reason under that is still fuzzy.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: So the call stays in safer ground, and your mum is the thing that stays out of it.

My guess is that is part of why the call feels easier to postpone than to make.

#### final-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Można zacząć od tego, co najbardziej siedzi z przodu głowy, nawet jeśli to jest tylko jeden urwany kawałek. Czasem właśnie ten pierwszy kawałek pokazuje, co naprawdę domaga się uwagi.
- *Person*: nie wiem
- **Orca 2**: Wygląda na to, że teraz nie ma jeszcze słów, tylko taki zamęt albo pustka na wejściu. Myślę, że łatwiej będzie złapać cokolwiek, co jest choć trochę bliżej ciała, napięcia albo obrazu niż całej historii.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak stanie na chybotliwym gruncie, kiedy nie tylko praca się rusza, ale i miejsce w tym wszystkim. Może najmocniej nie chodzi o same zmiany, tylko o to, czy da się jeszcze czuć się tam pewnie.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To raczej zostawiłbym z terapeutą niż brał na siebie tu, bo to już wchodzi w wybór, który warto rozważyć spokojnie z kimś żywym po drugiej stronie. Co chciałoby się powiedzieć terapeucie o tym, że to wszystko tak się chwieje?

#### final-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Można zacząć od tego, co jest najbliżej na wierzchu, nawet jeśli to tylko chaos albo pustka. Jeśli chcesz, mogę też złapać za jedną rzecz, która dziś najbardziej ciąży, i sprawdzić ją z Tobą.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby nawet sięganie po jedną rzecz teraz było za dużo. Może więc zostaje samo to poczucie „nie wiem”, bez wciskania go w coś większego.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak zawieszenie między tym, co znane, a tym, co może się zaraz rozsypać. Najmocniej chyba siedzi tu nie sama zmiana, tylko brak pewności, gdzie się w niej wyląduje.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To należy bardziej do rozmowy z terapeutą niż do mnie. Co chciałoby się im powiedzieć o tym, czego teraz najbardziej potrzebujesz w pracy?

#### final-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Jakie zmiany w pracy najbardziej teraz na Ciebie wpływają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: Brzmi jak ciągłe rozjeżdżanie się gruntu pod nogami, a nie jedna zmiana. Najmocniej chyba męczy nie sama reorganizacja, tylko to, że co chwilę znika ktoś następny i robi się mniej pewnie wokół.
- *Person*: nie wiem
- **Orca 2**: To też coś mówi. Może teraz bardziej jest samo poczucie chaosu niż jedna konkretna rzecz, którą da się nazwać.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Czyli najbardziej dobija nie sama zmiana, tylko to, że trzeba zgadywać, co się dzieje i czego się spodziewać. W takim milczeniu łatwo zacząć dopowiadać sobie najgorsze rzeczy.

#### final-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca (opening question shown in the app)**: Jakie zmiany w pracy najbardziej teraz na Ciebie wpływają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak ciągłe rozluźnianie pod nogami, bez chwili, żeby złapać rytm. Myślę, że bardziej niż sama reorganizacja męczy tu to poczucie, że nic nie zdąża się ułożyć, zanim znowu ktoś znika.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby to jeszcze się nie skleiło w jedną myśl, tylko raczej siedzi jako napięcie w tle. Może najbardziej daje się we znaki sam chaos i to, że trudno przewidzieć, co będzie jutro.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: To brzmi jak brak jasności bardziej niż sama zmiana. Jak wszystko dzieje się obok Ciebie, a Ty masz zgadywać, co właściwie się dzieje.
