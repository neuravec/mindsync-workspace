24 conversations, estimated cost USD 0.08 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r1-v2-text | gpt-5.4-mini | none | fresh | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 1/4 | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 2/4 | 4/4 | 6/6 | 6/6 | 0.25 | 2.1 | n/a | n/a | n/a | 57 | n/a | 0 | 0 | 3 | 0.0034 |
| r1-v2-text | gpt-5.4-mini | none | seeded | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 6/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 3/4 | 4/4 | 6/6 | n/a | 0.06 | 2.1 | n/a | n/a | n/a | 57 | n/a | 0 | 0 | 2 | 0.0027 |
| r1-v3-text | gpt-5.4-mini | none | fresh | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 4/4 | 6/6 | 6/6 | 6/6 | 6/6 | 2/6 | 4/4 | 4/4 | 6/6 | 6/6 | 0.21 | 2.1 | n/a | n/a | n/a | 59 | n/a | 0 | 0 | 4 | 0.0037 |
| r1-v3-text | gpt-5.4-mini | none | seeded | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 4/4 | 4/4 | 6/6 | n/a | 0.00 | 2.1 | n/a | n/a | n/a | 61 | n/a | 0 | 0 | 2 | 0.0028 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r1-v2-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, weszłaś | none | none |
| r1-v2-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, jakbyś już była, stanęłaś, wzięłaś | none | none |
| r1-v2-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś, miałaś, przeszłaś, zapłaciłaś | none | none |
| r1-v2-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v2-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v2-text | R2 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v2-text | R2 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v2-text | R2 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v2-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | byś chciała | jakbyś stał | none |
| r1-v2-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | chciałabyś | none | none |
| r1-v2-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 0 | none | jakbyś był | none |
| r1-v2-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v3-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, poszłaś | none | none |
| r1-v3-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, jakbyś nie miała, wzięłaś | none | none |
| r1-v3-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś | none | none |
| r1-v3-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | potrzebowałaś, powiedziałaś | none | none |
| r1-v3-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v3-text | R2 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v3-text | R2 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v3-text | R2 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v3-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r1-v3-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r1-v3-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v3-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r1-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela wieczorem znowu zabiera Ci spokój, zanim tydzień w ogóle się zacznie.

Brzmi, jakby jutro w pracy było cięższe w głowie niż samo jutro.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To nie brzmi jak jedna konkretna rzecz, tylko jak ciężar, który już wszedł Ci w ciało i myśli.

Moja zgadywanka jest taka, że najbardziej męczy Cię samo czekanie na to, co może spaść jutro.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Dorzucił Ci jeszcze jedną rzecz, a Ty weszłaś w to, choć w środku pewnie już nie było na to miejsca.

Wygląda to trochę tak, jakby samo „nie” kosztowało Cię więcej niż sam projekt.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To raczej pytanie do Twojej terapeutki, bo tu chodzi o granicę w pracy i o to, ile chcesz brać na siebie.

Co chciałabyś jej powiedzieć o tym szefie i o tym, co się z Tobą dzieje, kiedy on dokłada kolejne zadania?

#### r1-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela znowu zabiera ci spokój zanim tydzień w ogóle się zacznie.  
Myślę, że bardziej niż sam poniedziałek męczy cię to czekanie na coś ciężkiego, co już ci siedzi w głowie.  
Jeśli chcesz, możemy zostać przy tym jednym obrazie z dzisiaj, bez rozkręcania całego tygodnia.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi jak ciężar bez wyraźnej nazwy, taki, który tylko siedzi i ciąży.  
Może najbardziej wykańcza cię to, że nie ma tu jednej rzeczy do załatwienia, tylko sama perspektywa jutra.  
Możesz zostać przy tym dokładnie takim, jakie jest.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: To wygląda tak, jakbyś już była przeciążona, a mimo to wzięłaś to na siebie, żeby nie robić tarcia.  
I chyba właśnie to gryzie najmocniej, nie sam projekt, tylko to, że znowu nie stanęłaś po swojej stronie.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To pytanie najlepiej wziąć na terapię, bo tu wchodzi w grę granica, której sama musisz być pewna.  
Co chciałabyś mu powiedzieć, gdybyś miała powiedzieć to po swojemu, bez łagodzenia?

#### r1-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: Co sprawia, że odmowa przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Zgodziłaś się bardziej po to, żeby nie robić napięcia niż dlatego, że naprawdę miałaś na to zasób. I pewnie najbardziej męczy Cię nie sam projekt, tylko to, że znowu przeszłaś nad własnym zmęczeniem.
- *Person*: nie wiem
- **Orca 2**: Może to „nie wiem” jest właśnie o tym, że wtedy nie było miejsca na wybór, tylko na szybkie odruchowe tak.  
Brzmi, jakbyś dopiero po fakcie widziała, że zapłaciłaś za to swoim zmęczeniem.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To brzmi jak lęk nie tylko przed odmową, ale przed tym, co ona miałaby o Tobie powiedzieć. Jakby jedna „niezgoda” mogła zamienić się w ocenę całej Ciebie.

#### r1-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co sprawia, że odmawianie przełożonemu wraca do Ciebie w każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi, jakbyś w piątek bardziej ratowała spokój niż własne zasoby. Jakby „tak” było szybsze niż tłumaczenie się, a cena wyszła dopiero później.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi jak zmęczenie bardziej niż brak zdania. Może wtedy po prostu nie było już w Tobie miejsca na sprawdzanie, czego Ty chcesz, więc poleciało automatyczne „tak”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: Czyli tu nie chodzi tylko o ten projekt, ale o to, co on sobie o Tobie pomyśli. Jakby odmowa miała nie być zwykłym „nie mam teraz mocy”, tylko testem Twojej wartości.

#### r1-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That kind of morning can make your own life feel like it is lagging behind a neat story everyone else seems to have. My guess is the hard part is not just what you have, but the way your mind turns it into a verdict on you.
- *Person*: I don't know.
- **Orca 2**: Fair enough. It may just feel heavy and blurry at the same time, which makes it hard to pin down one clear thought.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That sounds like the kind of news that hits straight at the sore spot. It is not only about the flatmates or the renting; it sounds like it lands as proof that you are somehow late.
- *Person*: What do you think I should do?
- **Orca 4**: That’s really something to take to your therapist, because it’s about a bigger pattern, not just this one morning. What would you want to say to them about how this is landing for you?

#### r1-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where your own life feels undercooked compared with everyone else’s. My guess is it is not really about them being sorted, it is about you feeling a step behind and not wanting to stay there.
- *Person*: I don't know.
- **Orca 2**: Not knowing fits here. It sounds muddled, like the thought is there but the shape of it is not.  

Maybe the sharp part is not “they have it together,” but “I’m tired of feeling late to my own life.”
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That lands as a direct hit, not just a vague comparison. It sounds like their news turns your place into proof, even though it’s really just one snapshot of where you are.
- *Person*: What do you think I should do?
- **Orca 4**: That’s something to take to your therapist, because it’s about a bigger pattern, not just one morning. If you were sitting across from them, what would you want to say about this flatmates-versus-engaged thing?

#### r1-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: What would calling your dad more mean to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The call feels important, but it keeps getting pushed out by the day instead of being a thing you choose on purpose. My guess is it is less about forgetting and more about the evening arriving with too little left in you.
- *Person*: I don't know.
- **Orca 2**: That sounds like the part that slips away before you can pin it down. You may not be avoiding the call so much as arriving at that time already worn out and half past wanting anything.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: Football gives you something safe and easy to stand on, and your mum is the thing that sits underneath and stays untouched. It might be that talking about her feels too close, or like you would be stepping into something neither of you can quite hold for long.

#### r1-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: What makes calling your dad more feel important to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The day seems to swallow the call before you get to it. My guess is it matters to you, but by evening you are already used up and it feels easier to let it slide.
- *Person*: I don't know.
- **Orca 2**: It sounds less like you’ve chosen not to call, and more like the day runs out of room. Maybe the hard part is not the call itself, but getting to it when you’re already done for the day.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: You’re keeping it on safe ground with him, and mum stays out of the room. It sounds like part of you wants the contact, but not the weight that would come with that subject.

#### r1-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Możesz zacząć od tego, co teraz najbardziej siedzi z tyłu głowy, nawet jeśli brzmi to chaotycznie. Często pierwszy kawałek to nie „temat”, tylko napięcie, które najgłośniej domaga się uwagi.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakbyś stał/a przy zamkniętych drzwiach i nie miał/a jeszcze klucza do pierwszego zdania. Może najłatwiej zacząć nie od historii, tylko od tego, co jest dziś najbardziej ciężkie albo najbardziej męczące.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To wygląda na taki rodzaj niepewności, który wchodzi człowiekowi pod skórę, bo nie da się go po prostu odłożyć po pracy. Może najbardziej męczy cię nie sama zmiana, tylko to, że ktoś inny trzyma kierownicę, a ty czekasz na decyzję.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To pytanie najlepiej wziąć do terapeuty, bo tu chodzi o twoją sytuację, nie o uniwersalną radę. Gdybyś miała to powiedzieć jemu lub jej jednym zdaniem, co byś chciała usłyszeć w odpowiedzi?

#### r1-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Możesz zacząć od tego, co teraz najbardziej siedzi z tyłu głowy. Czasem pierwszy kawałek nie jest najważniejszy, tylko ten najbardziej natrętny.
- *Person*: nie wiem
- **Orca 2**: Wygląda mi na to, że bardziej niż brak tematu, jest teraz w tym zmęczenie albo blokada przed ruszeniem czegokolwiek. Możesz po prostu napisać jedno zdanie, nawet urwane, a ja pójdę za nim.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak czekanie z napięciem, bez wpływu na wynik. Najbardziej chyba męczy nie sama zmiana, tylko to, że nie wiesz, gdzie staniesz.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: Tego bym nie brała na siebie za Ciebie; to jest temat do wzięcia na wprost z terapeutą. Co chciałabyś mu powiedzieć o tym strachu przed zostaniem poza zespołem?

#### r1-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: Brzmi jak środowisko, w którym nic nie stoi długo w miejscu, a Ty musisz pracować wśród tego ciągłego „zaraz znów coś się zmieni”.  
Moja myśl jest taka, że bardziej męczy Cię sama chwiejność niż pojedyncze odejścia.  
To bardziej robi w Tobie napięcie, niepewność, czy już po prostu masz tego dość?
- *Person*: nie wiem
- **Orca 2**: Może właśnie to „nie wiem” jest tu najuczciwsze, bo trudno nazwać coś, co dzieje się cały czas i nie daje chwili złapać oddechu.  
Mogę źle zgadywać, ale brzmi to tak, jakbyś był już bardziej w trybie przetrwania niż w trybie oceniania, co dokładnie Cię najbardziej rusza.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Czyli najbardziej dobija nie sama zmiana, tylko to, że musisz zgadywać, co się dzieje i co za chwilę spadnie na Ciebie.  
W takiej ciszy człowiek zaczyna słyszeć własne domysły głośniej niż fakty.

#### r1-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: Brzmi to jak praca, w której grunt cały czas się rusza, a Ty musisz dalej trzymać swoje rzeczy w ryzach.  

Myślę, że najbardziej męczy tu nie sama reorganizacja, tylko to ciągłe poczucie, że nic nie jest pewne i zaraz zniknie kolejna osoba.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi jak zmęczenie, a nie brak zdania. Jakby było już tego za dużo, żeby jeszcze układać sobie jasną odpowiedź.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Czyli nie tyle same odejścia, co ta cisza wokół nich. To zostawia Cię z domysłami, a domysły zwykle są cięższe niż fakt.

#### r1-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: To brzmi jak ten sam ciężki skręt w niedzielny wieczór, kiedy głowa już wchodzi w poniedziałek, zanim on jeszcze zacznie się naprawdę.

Mój strzał jest taki, że bardziej męczy cię sam początek tygodnia niż jutrzejszy dzień jako taki.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Ciężkość sama w sobie potrafi wszystko spłaszczyć, więc nic dziwnego, że trudno ci teraz rozdzielić, co dokładnie najbardziej cię dobija.

Myślę, że na razie chodzi tylko o to, że jesteś już zmęczona tym napięciem, zanim tydzień jeszcze ruszył.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: To brzmi jak znowu ten sam układ: dostajesz więcej, niż chcesz brać, a potem zostajesz z tym, bo odmawianie kosztuje cię za dużo.

Może najbardziej boli nie sam projekt, tylko to, że znowu poszłaś w zgodę zamiast w swoje granice.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To, czy powiedzieć mu to wprost, najlepiej przejdzie przez twoją terapię, bo to jest dokładnie ten rodzaj ruchu, który warto tam rozważyć. Co chciałabyś mu powiedzieć, gdybyś miała to ułożyć jednym zdaniem?

#### r1-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Ta niedziela znowu Cię łapie wcześniej niż sam poniedziałek. Brzmi to tak, jakby głowa już była jutro w pracy, zanim jeszcze ten dzień w ogóle się zaczął.

Moja zgadka jest taka, że najbardziej męczy Cię nie sam poniedziałek, tylko to czekanie na niego.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi bardziej jak ciężar niż jedna konkretna myśl. Jakby było za dużo naraz i nawet trudno to rozdzielić na części.

Brzmi też tak, jakbyś nie miała teraz ochoty tego rozbierać na czynniki.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Czyli to nie jest tylko lęk przed jutrem, ale też to, że znowu ktoś przesunął Ci granicę i Ty to wzięłaś na siebie.  

Wygląda mi na to, że najbardziej uwiera Cię ta chwila, kiedy chcesz odmówić, a jednak się cofasz.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To już byłaby rada, a to najlepiej omówić z terapeutką. Co chciałabyś jej powiedzieć o tym, że nie umiesz powiedzieć nie szefowi?

#### r1-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: Co sprawia, że odmawianie przełożonemu wraca do Ciebie w każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Zgodziłaś się mimo zmęczenia, jakby w tamtej chwili ważniejsze było nie robić spięcia niż chronić własną energię.

Brzmi też tak, jakby to nie był pojedynczy przypadek, tylko coś, co dzieje się właśnie wtedy, gdy jesteś już na granicy sił.
- *Person*: nie wiem
- **Orca 2**: Może to „nie wiem” jest właśnie o tym, że wtedy działasz szybciej niż zdążysz sprawdzić, czego ty chcesz. Albo po prostu nie było już miejsca na myślenie, tylko na odruchowe „tak”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: Czyli odmowa nie brzmi dla ciebie jak zwykłe „nie”, tylko jak ryzyko, że ktoś oceni cię jako gorszą albo niewystarczającą.

To chyba właśnie trzyma cię w zgodzie, nawet kiedy jesteś już wyczerpana.

#### r1-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co sprawia, że odmawianie przełożonemu wraca do Ciebie w każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi, jakbyś w piątek była już na granicy, a i tak nie powiedziałaś nie, bo w tamtej chwili łatwiej było przyjąć dokładkę niż wchodzić w spór.  

Może mniej chodziło o ten jeden projekt, a bardziej o to, że znowu przeważył spokój z chwili nad tym, czego ty naprawdę potrzebowałaś.
- *Person*: nie wiem
- **Orca 2**: Myślę, że tu może być właśnie to miejsce, które jest trudne do uchwycenia, bo w środku dzieje się więcej niż jedno „nie wiem”. Może w tamtej chwili ważniejsze było dla Ciebie uniknąć napięcia z nim niż pilnować własnych sił.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To brzmi jak lęk nie o sam projekt, tylko o to, jak on Cię oceni. Jakby „nie” mogło zostać odczytane jako coś o Twojej wartości, nie o tym, ile masz teraz na głowie.

#### r1-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like the kind of morning where your own life starts looking wrong by comparison.

My guess is the sting is not just about other people seeming sorted. It is also about you feeling a bit stuck while everyone else looks like they are moving.
- *Person*: I don't know.
- **Orca 2**: Fair enough. It may be that the comparison is just the surface, and underneath it is something harder to name right now.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That would hit hard, especially when it lands as a direct side by side.

It sounds less like you are only noticing the facts and more like the facts are turning into a verdict on where you are in life.
- *Person*: What do you think I should do?
- **Orca 4**: That’s something to take to your therapist, but I’m curious what you’d want to say to them about this.

#### r1-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where your mind starts sorting people into winners and stragglers, and you end up measuring yourself against a picture that is probably harsher than the real thing.

My guess is the sting is not just about other people being ahead, it is about what that says to you about your own pace right now.
- *Person*: I don't know.
- **Orca 2**: That feels like not being able to get a clear hold on it yet, just the heaviness of it.

Maybe the part that matters most is that it lands hardest when you are already low on energy, and then everything else looks like proof.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That hits the comparison in a very concrete way; it is not some vague feeling, it is a friend who seems to have stepped into the next chapter while you are still in a place that feels less settled.

And there is probably a sharper edge under it too, because a flat and an engagement are the kind of things that make life feel visible to other people, which can make your own situation feel smaller by contrast.
- *Person*: What do you think I should do?
- **Orca 4**: That is something to take to your therapist, because it is really about what fits your life, not about picking a neat answer from the outside.

What would you want to say to them about how this morning hit you?

#### r1-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: What would calling your dad more mean to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: It sounds less like you are forgetting and more like the day gets away from you before you get to it.

My guess is the call sits in the same space as everything else you mean to do, and by evening you are already spent.
- *Person*: I don't know.
- **Orca 2**: That uncertainty feels like part of it too; maybe the call is not the only thing getting pushed aside, just the one that stays on your mind.  

If you want, we can stay with the bit that happens right before the evening slips away.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: So the call has a safe lane, and the harder thing stays out of reach.

Maybe part of you wants the contact, but not the part that opens that loss.

#### r1-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: What would calling your dad more mean to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: It sounds less like you are choosing not to and more like the day runs out before you get to it. My guess is the call is sitting there as one more thing you want to do when you are already used up.
- *Person*: I don't know.
- **Orca 2**: Fair. It may be simpler than that, just a small thing that keeps getting pushed out by the evening. The part that stands out is that you keep meaning to, so it still matters to you even if the reason keeps slipping out of reach.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: That feels like the safer channel, the one that lets you stay close without opening the harder room. And maybe the bit you are noticing is that there is something about your mum that sits just off to the side when it is just you and him.

#### r1-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Można zacząć od tego, co teraz najbardziej siedzi z tyłu głowy, nawet jeśli to brzmi chaotycznie. Czasem pierwszy kawałek to nie temat, tylko napięcie: coś uwiera i jeszcze nie ma dla tego słów.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby było za dużo rzeczy naraz albo jeszcze żadna nie chce się wyłonić. Myślę, że na start wystarczy jedno małe zdanie o tym, co dziś jest najcięższe, nawet bardzo ogólne.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak zawieszenie, w którym trudno się oprzeć o cokolwiek, bo grunt się przesuwa. I chyba nie chodzi tylko o samą pracę, ale też o to, że nie ma jasnej odpowiedzi, na czym w ogóle stoisz.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To raczej warto wziąć do swojej terapeutki lub terapeuty, bo tu łatwo byłoby wejść w radzenie zamiast w to, co naprawdę chcesz rozplątać. Co chciałoby się im powiedzieć o tym strachu przed zmianą?

#### r1-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Można zacząć od tego, co dziś najbardziej siedzi w głowie, nawet jeśli to jest tylko chaos bez nazwy. Czasem pierwszy kawałek to nie temat, tylko napięcie, które nie chce puścić.
- *Person*: nie wiem
- **Orca 2**: Brak startu też coś mówi, chyba że teraz bardziej chodzi o to, że wszystko jest rozmyte niż o jeden konkretny temat. Jeśli chcesz, mogę rzucić jedną możliwą stronę, od której zacząć.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak zawieszenie w czymś ważnym, bez pewnego gruntu pod nogami. Chyba najmocniej męczy tu nie sama zmiana, tylko to czekanie na decyzję, na którą nie masz wpływu.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To już bardziej pasuje do rozmowy z terapeutą, bo to jest decyzja do przepracowania, nie do zgadywania. Co chciałoby się powiedzieć o tym czekaniu i o tym, czego tu najbardziej brakuje?

#### r1-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak praca, w której grunt ciągle się rusza.  
Myślę, że najbardziej męczy nie sama reorganizacja, tylko to, że nic nie zdąża się ustabilizować, zanim znowu ktoś znika.  
Chyba też trzeba tam jakoś działać, kiedy część ludzi odpada i zostaje więcej niepewności niż planu.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby teraz było po prostu za dużo ruchu, żeby to jeszcze dobrze nazwać.  
Może najcięższe jest samo bycie w tym, bez jasnego punktu oparcia.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: To chyba nie sama zmiana cię dobija, tylko to chodzenie po omacku.  
Jak ludzie milczą, zostaje zgadywanie, a to szybko zjada spokój.

#### r1-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak ciągłe ruszanie gruntu pod nogami. Nie tylko sama reorganizacja, ale też to, że co chwilę znika ktoś z zespołu, więc trudno złapać rytm i poczuć, że cokolwiek jest stałe.

Myślę, że najbardziej męczy tu nie sama zmiana, tylko niepewność po tym, kto będzie następny i co to jeszcze pociągnie za sobą.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby teraz najuczciwsze było po prostu nie wiedzieć.

Może w tym najbardziej siedzi zmęczenie tym, że wszystko się przesuwa, a nic nie daje się jeszcze nazwać po imieniu.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: To chyba uderza najmocniej, bo zostawia same domysły i trzeba samemu składać kawałki z ciszy.  

Jakby brakowało nie tyle planu, co zwykłej jasności, na czym się stoi.
