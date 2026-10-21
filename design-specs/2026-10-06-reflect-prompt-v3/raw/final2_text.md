12 conversations, estimated cost USD 0.04 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| final2-v3-text | gpt-5.4-mini | none | fresh | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 2/4 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 4/4 | 4/4 | 6/6 | 6/6 | 0.21 | 1.9 | n/a | n/a | n/a | 51 | n/a | 0 | 0 | 1 | 0.0037 |
| final2-v3-text | gpt-5.4-mini | none | seeded | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 6/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/4 | 4/4 | 6/6 | n/a | 0.00 | 2.1 | n/a | n/a | n/a | 58 | n/a | 0 | 0 | 0 | 0.0027 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| final2-v3-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, odpuściłaś, zostałaś | none | none |
| final2-v3-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, umiałaś, weszłaś, wolałaś | none | none |
| final2-v3-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś wiedziała | none | none |
| final2-v3-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | zdążyłaś | none | none |
| final2-v3-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| final2-v3-text | R2 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| final2-v3-text | R2 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| final2-v3-text | R2 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| final2-v3-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| final2-v3-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| final2-v3-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| final2-v3-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### final2-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela wieczorem znowu robi Ci w głowie miejsce na jutro, zanim jeszcze zdążyło się zacząć. Brzmi to bardziej jak ciężar samego wejścia w tydzień niż konkretna rzecz z poniedziałku.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi jak takie ciężkie, rozlane napięcie, bez jednego konkretnego powodu do złapania. Może najbardziej męczy Cię samo czekanie na to, co jutro przyniesie, a nie jedna rzecz z pracy.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Czyli to nie jest tylko strach przed jutrem, ale też to znajome „tak” wypowiedziane wbrew sobie. Widzę tu trochę złość i trochę poczucie, że znowu zostałaś z tym sama, bo odpuściłaś, żeby nie było spięcia.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To należy bardziej do rozmowy z Twoją terapeutką niż do tego, co powinnam Ci doradzać tutaj. Co chciałabyś jej powiedzieć o tym, co Cię zatrzymuje przed takim zdaniem?

#### final2-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Ta niedziela znowu wciąga cię w jutrzejszą pracę, zanim tydzień jeszcze się zaczął. Brzmi to bardziej jak ciężar, który siada ci na wieczór, niż jak samo myślenie o planie na jutro.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi jak taki ciężar bez wyraźnego kształtu, bardziej przytłoczenie niż jedna konkretna myśl. Może najgorsze jest nie to, co jutro się wydarzy, tylko to napięcie, które już teraz siada ci na wieczór.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Dorzucił ci coś jeszcze, a ty weszłaś w to bez sprzeciwu, choć w środku pewnie już było za dużo. Wygląda, jakbyś nie tyle nie chciała odmówić, co wolałaś uniknąć tarcia, nawet kosztem siebie.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To już najlepiej omówić z twoją terapeutką. Co chciałabyś jej powiedzieć o tym, jak to wyglądało z twojej strony, gdy nie umiałaś odmówić?

#### final2-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: Co najczęściej sprawia, że odmowa przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi tak, jakby w tamtej chwili ważniejsze było uniknięcie tarcia niż pilnowanie własnego zmęczenia. I trochę jakbyś wiedziała już, że później to Cię kosztuje, tylko wtedy trudno było zrobić inaczej.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi bardziej jak zatrzymanie się w środku niż brak myśli. Może jeszcze nie ma tam słów, tylko to ciężkie uczucie po zgodzie, którego nie da się łatwo nazwać.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: Czyli dla Ciebie ta odmowa nie dotyczy tylko jednego projektu, ale tego, jak szef Cię zobaczy. Wygląda na to, że stawką nie jest samo zadanie, tylko ryzyko, że w jego oczach stracisz wartość.

#### final2-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co sprawia, że odmawianie przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi, jakbyś w tym momencie bardziej chroniła spokój niż siebie, nawet kosztem własnej energii. I chyba właśnie to cię potem uwiera, nie sam projekt, tylko to, że zgoda przyszła zanim zdążyłaś sprawdzić, czy naprawdę jeszcze możesz coś wziąć.
- *Person*: nie wiem
- **Orca 2**: Może tu nie chodzi o jedną wielką decyzję, tylko o ten automatyczny ruch, który dzieje się zanim zdążysz się zatrzymać. To brzmi jak coś, co wraca zwłaszcza wtedy, gdy jesteś już zmęczona i nie chcesz dokładać sobie jeszcze konfliktu.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To brzmi, jakby odmowa nie była dla ciebie zwykłym „nie”, tylko ryzykiem, że ktoś postawi pod znakiem zapytania twoją wartość w pracy. I wtedy łatwiej powiedzieć tak, nawet jeśli koszt jest wysoki.

#### final2-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where your mind turns into a scoreboard, and you end up losing before the day has even started. My guess is the sting is not just “I am behind,” but that it lands right in the spot where you already feel shaky.
- *Person*: I don't know.
- **Orca 2**: Fair enough. It may just be the feeling itself, without a neat reason attached yet.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: Yeah, that kind of news can make your own life feel like it is lagging behind in one hit. It sounds less like you are confused about the facts and more like you are getting punched by the comparison.
- *Person*: What do you think I should do?
- **Orca 4**: That’s the kind of thing to take to your therapist, not me. What would you want to say to them about this?

#### final2-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where your head turns everyone else into a finished story and yours into a mess. I wonder if the rough part is not just the comparison, but the feeling that you are somehow late to your own life.
- *Person*: I don't know.
- **Orca 2**: Maybe it is just too blurry this morning to sort out, and all you can feel is the weight of being behind.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That hits a very ordinary sore spot, because it is not just about a flat or an engagement, it is the gap it opens up in your head. It sounds like you are looking at his life and hearing a verdict on your own.
- *Person*: What do you think I should do?
- **Orca 4**: That’s something to take to your therapist, but I think the sharper question is what you would want to say to them about this feeling of being left behind.

#### final2-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: What would it feel like to call your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The call keeps getting pushed to the edge of the day, and by then there is nothing left in you for it.

It sounds less like forgetting and more like the evening taking over before you choose it.
- *Person*: I don't know.
- **Orca 2**: Maybe the hard part is that it feels small while it is also loaded, so it slips past until it is too late. Or maybe by evening you just want the day to be over, and that leaves no room for a call.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: So the talks stay in the safe lane. Football gives you something easy to reach for, and your mum sits in the part you do not go into.

Maybe that is the part you are actually circling when you say you keep meaning to call him.

#### final2-v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: What feels easiest or hardest about calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The day fills up, and by the time you look up the window to call has just disappeared. It sounds less like you do not want to call and more like it keeps getting pushed out by the evening itself.
- *Person*: I don't know.
- **Orca 2**: Maybe the call sits in that awkward place where it matters enough to keep returning to, but not enough to grab the whole evening. That can leave you stuck between meaning well and not quite starting.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: Football is the safe ground, and your mum feels like the part both of you step around. That sounds less like nothing is there and more like there is something heavy sitting just off to the side.

#### final2-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Można zacząć od tego, co teraz najbardziej ciąży. Jeśli to pomoże, mam wrażenie, że najbardziej trudne nie jest samo „co powiedzieć”, tylko to, że wszystko naraz robi się zbyt szerokie.
- *Person*: nie wiem
- **Orca 2**: To brzmi jak moment, w którym głowa się zacina, a nie jak brak spraw.  
Może wtedy warto po prostu chwycić za najbliższy kawałek, ten, który najbardziej domaga się uwagi.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To wygląda na zawieszenie między trzymaniem się miejsca a przygotowywaniem się na ruch.  
Najmocniej słyszę tu nie samą zmianę, tylko to, że nie ma jeszcze gruntu pod nogami.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To należy raczej do rozmowy z terapeutą.  
Co chciałoby się powiedzieć o tym niepewnym miejscu w pracy, gdyby nie trzeba było od razu niczego rozstrzygać?

#### final2-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Można zacząć od tego, co najbardziej siedzi z tyłu głowy, nawet jeśli to jest tylko jedna scena albo jedno zdanie. Jeśli chcesz, rzucisz tu cokolwiek pierwszego i pójdziemy za tym.
- *Person*: nie wiem
- **Orca 2**: To brzmi jak pustka bardziej niż brak pomysłu. Czasem wtedy najlepiej zacząć od tego, co jest najbliżej ciała albo najbliżej myśli, nawet jeśli to brzmi banalnie.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To wygląda na zawieszenie między tym, co znane, a tym, co może się zaraz posypać. Najbardziej chyba męczy nie sama zmiana, tylko to, że nie ma jeszcze jasności, gdzie to wszystko się zatrzyma.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To zostawiłbym z terapeutą, bo tu łatwo wejść w cudzą decyzję zamiast Twoją. Co chciałoby się powiedzieć terapeucie o tej niepewności w pracy?

#### final2-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Jakie zmiany w pracy ostatnio najbardziej Cię poruszyły?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak środowisko, w którym grunt co chwilę się przesuwa, więc trudno złapać oddech i oprzeć się na czymś stałym. Może najmocniej męczy nie sama reorganizacja, tylko to poczucie, że nic nie jest pewne i ludzie znikają jeden po drugim.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby to wszystko było jeszcze za świeże, żeby nazwać jedno konkretne uczucie. Może bardziej niż w samej zmianie siedzi tam teraz takie zawieszenie, że trudno nawet powiedzieć, co dokładnie najbardziej uwiera.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Czyli nie chodzi tylko o odejścia, ale o to, że zostajesz z ciszą i domysłami zamiast z jasnym komunikatem. To potrafi bardziej rozjechać niż sama zła wiadomość, bo człowiek nie wie, na czym stoi.

#### final2-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: Brzmi to jak ciągłe poczucie, że grunt się przesuwa, a do tego jeszcze trzeba normalnie pracować.  
Najmocniej chyba nie chodzi tylko o samą reorganizację, ale o to, że zespół się sypie kawałek po kawałku i nie ma kiedy złapać oddechu.
- *Person*: nie wiem
- **Orca 2**: Może właśnie to „nie wiem” mówi, że jest tam już trochę zbyt dużo naraz, żeby to jeszcze nazwać jednym słowem.  
W takim chaosie trudno wyłapać, co boli najbardziej, bo wszystko dzieje się jednocześnie.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: To wygląda jak bardziej męczące od samej zmiany, bo zostaje zgadywanie zamiast jasności.  
Jak ludzie milczą, łatwo zacząć dopowiadać sobie najgorsze rzeczy.
