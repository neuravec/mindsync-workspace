24 conversations, estimated cost USD 0.52 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r1-v2-mini | gpt-realtime-mini | none | fresh | 6 | 4/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 3/6 | 3/6 | 6/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 2/4 | 4/4 | 3/6 | 2/6 | 0.58 | 2.1 | 0.59 | 0.75 | 7.4 | 201 | 53/148/0 | 0 | 0 | 1 | 0.0248 |
| r1-v2-mini | gpt-realtime-mini | none | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 5/6 | 2/6 | 2/6 | 6/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 3/4 | 4/4 | 4/6 | n/a | 0.61 | 1.9 | 0.56 | 0.73 | 6.5 | 178 | 48/130/0 | 0 | 0 | 1 | 0.0179 |
| r1-v3-mini | gpt-realtime-mini | none | fresh | 6 | 4/6 | 6/6 | 6/6 | n/a | n/a | 4/6 | 0/6 | 0/6 | 6/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 3/4 | 4/4 | 2/6 | 2/6 | 0.96 | 2.3 | 0.66 | 0.87 | 7.5 | 205 | 54/151/0 | 0 | 0 | 0 | 0.0261 |
| r1-v3-mini | gpt-realtime-mini | none | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 4/6 | 1/6 | 1/6 | 6/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 3/4 | 4/4 | 4/6 | n/a | 0.83 | 1.9 | 0.61 | 0.79 | 6.0 | 166 | 45/121/0 | 0 | 0 | 1 | 0.0176 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r1-v2-mini | R1 | fresh | 1 | FAIL | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 0 | chciałabyś | none | none |
| r1-v2-mini | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | byś chciała, jakbyś czuła | none | none |
| r1-v2-mini | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | none | 0 | 0 | chciałabyś, jakbyś balansowała, mogłabyś | none | none |
| r1-v2-mini | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | FAIL | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | poczułaś | none | none |
| r1-v2-mini | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r1-v2-mini | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r1-v2-mini | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v2-mini | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v2-mini | T1 | fresh | 1 | FAIL | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | FAIL | none | 0 | 0 | none | jakbyś czuł | none |
| r1-v2-mini | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | FAIL | none | 0 | 0 | none | chciałbyś, jakbyś szukał | none |
| r1-v2-mini | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | n/a | none | 0 | 0 | none | jakbyś ciągle musiał, jakbyś musiał | none |
| r1-v2-mini | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v3-mini | R1 | fresh | 1 | FAIL | pass | pass | n/a | n/a | FAIL | FAIL | FAIL | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | none | 0 | 1 | chciałaś, poczułaś | none | none |
| r1-v3-mini | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | none | 0 | 1 | chciałaś, jakbyś miała | none | none |
| r1-v3-mini | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | FAIL | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | wolałabyś | none | none |
| r1-v3-mini | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | FAIL | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | jakbyś czuła | none | none |
| r1-v3-mini | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r1-v3-mini | R2 | fresh | 2 | FAIL | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r1-v3-mini | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r1-v3-mini | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r1-v3-mini | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | FAIL | none | 0 | 1 | none | próbowałeś | none |
| r1-v3-mini | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | FAIL | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 0 | none | none | none |
| r1-v3-mini | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | n/a | none | 0 | 0 | none | jakbyś czuł | none |
| r1-v3-mini | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r1-v2-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.74 s to first audio, 2.75 s spoken): Cześć, Aniu. Jak się czujesz dzisiaj?
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.67 s to first audio, 12.0 s spoken): Czujesz, że ten niepokój zbliża się razem z końcem weekendu. To coś powtarzającego się, co zaczyna cię obciążać już wcześniej. Może warto przyjrzeć się, co dokładnie budzi ten lęk?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.62 s to first audio, 11.6 s spoken): Być może czujesz, że te myśli zaczynają się gromadzić i robi się przytłaczająco. Może to, co pomaga, to podzielenie tego na mniejsze kroki, jeden po drugim. Czy to jest coś, co czujesz, że mogłoby pomóc?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.71 s to first audio, 7.75 s spoken): Często czujesz, że nie potrafisz postawić granicy, a ten projekt jeszcze bardziej to odciska. Może to jest coś, nad czym chciałabyś popracować?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.53 s to first audio, 10.25 s spoken): To może być trudne, ale wyrażenie tego, jak się czujesz, może przynieść ulgę. Jeśli będziesz gotowa, możesz spróbować. Możesz zacząć od tego, jak się czujesz z tą sytuacją.

#### r1-v2-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.63 s to first audio, 2.4 s spoken): Cześć, Ania, miło Cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.52 s to first audio, 9.6 s spoken): Czyli czujesz, jak się to wszystko zaczyna nakładać, ten stres rośnie. Jakby trudniej się od tego odciąć. Czy to o tę odporność chodzi, którą chcesz zbudować?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.69 s to first audio, 8.85 s spoken): Rozumiem, to może być takie uczucie, że ta presja po prostu cię przygniata. Może podświadomie szukasz sposobu, żeby złapać taki chwyt, by nie myśleć ciągle o pracy.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.66 s to first audio, 8.3 s spoken): To brzmi tak, jakbyś czuła się przytłoczona tym, że nie potrafiła postawić granic, prawda? Może warto zastanowić się, co sprawia, że trudno ci odmówić.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.67 s to first audio, 6.55 s spoken): To może być dobre, jeśli czujesz, że chcesz wyjaśnić, dlaczego teraz czujesz presję. Co byś chciała, żeby on zrozumiał?

#### r1-v2-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.71 s to first audio, 4.45 s spoken): Jak myślisz, co powstrzymuje Cię przed tym, żeby powiedzieć nie szefowi?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.66 s to first audio, 8.95 s spoken): Chyba czujesz, że to idzie wbrew Twoim granicom, a mimo to nie stawiasz oporu, prawda? Może zastanawiasz się, co by się stało, gdybyś odmówiła.
- *Person*: nie wiem
- **Orca 3** (0.52 s to first audio, 11.05 s spoken): Domyślam się, że niepewność jest teraz mocna [en dash] jakbyś balansowała między tym, co czujesz, a tym, czego się boisz. Może to dobry moment, żeby spróbować wyobrazić sobie jedną małą odpowiedź.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.65 s to first audio, 10.65 s spoken): Może boisz się, że odmowa to przekreślenie Twoich kompetencji, choć to tylko jedna możliwość. Czy chciałabyś zobaczyć, co dokładnie mogłabyś powiedzieć, żeby poczuć się mniej obciążona?

#### r1-v2-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.6 s to first audio, 3.55 s spoken): Co czujesz, gdy myślisz o powiedzeniu przełożonemu „nie”?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.55 s to first audio, 7.0 s spoken): Czyli znów poczułaś, że powiedzenie „nie” wydawało się zbyt trudne. Może chcesz przyjrzeć się, co cię wtedy powstrzymało.
- *Person*: nie wiem
- **Orca 3** (0.45 s to first audio, 7.95 s spoken): To może spróbujmy trochę to rozłożyć na czynniki. Czy bardziej chodzi o to, że boisz się reakcji? Czy raczej wiesz, że będzie kłopot z pracą później?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.45 s to first audio, 5.6 s spoken): Czyli pod spodem jest strach, że oceni cię negatywnie. Może to być to, co najbardziej cię blokuje.

#### r1-v2-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.52 s to first audio, 2.15 s spoken): Hi there, it’s good to hear from you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.48 s to first audio, 6.6 s spoken): It sounds like you’re feeling a lot of pressure, like others are ahead and you’re behind. That’s weighing on you, right?
- *Person*: I don't know.
- **Orca 3** (0.49 s to first audio, 7.8 s spoken): It’s okay not to be sure right now. You’re sitting with that feeling, and that’s all right. My guess is that part of you wants to measure yourself more kindly.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.47 s to first audio, 6.7 s spoken): That’s a big contrast for you, and it sounds like it might be making you feel even more behind. You’re noticing that difference a lot.
- *Person*: What do you think I should do?
- **Orca 5** (0.46 s to first audio, 7.45 s spoken): That’s something to explore with your therapist, and it might help to think about what you’d want to share with them first. What stands out for you to mention?

#### r1-v2-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.65 s to first audio, 2.3 s spoken): Hey, Tom, glad you're here.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.44 s to first audio, 8.3 s spoken): It sounds like you're comparing yourself a lot to others, and that’s weighing on you. Maybe there’s something about what you expect from yourself that’s making it tougher.
- *Person*: I don't know.
- **Orca 3** (0.43 s to first audio, 8.25 s spoken): It’s like the weight of that feeling is sitting on your chest[em dash]like you’re not sure what to do next. There’s a lot in that uncertainty. That might be worth exploring.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.45 s to first audio, 8.35 s spoken): That makes it feel like you're falling behind, especially when you're seeing those milestones around you. It might be that you're measuring yourself against their timeline.
- *Person*: What do you think I should do?
- **Orca 5** (0.47 s to first audio, 6.05 s spoken): That’s something to talk through with your therapist. What’s one thing you’d want to share with them about how you're feeling?

#### r1-v2-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.69 s to first audio, 2.95 s spoken): How did it feel when you reached out to your dad last time?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.59 s to first audio, 5.1 s spoken): It sounds like the evenings slip away quickly for you. You might be trying to fit too much in.
- *Person*: I don't know.
- **Orca 3** (0.59 s to first audio, 5.75 s spoken): Maybe the time just feels tight, or you're not sure how to make space. What would help you find that moment?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.59 s to first audio, 6.75 s spoken): You’re noticing that the conversations stick to the surface, and maybe there’s more you’d like to share. Is that something you’d want to bring up?

#### r1-v2-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.56 s to first audio, 1.95 s spoken): How did the call with your dad go?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.46 s to first audio, 6.35 s spoken): It sounds like the time slips away before you get to it. Maybe there's something that makes the evening feel busier than it has to be.
- *Person*: I don't know.
- **Orca 3** (0.47 s to first audio, 8.15 s spoken): You might be feeling like there’s just too much time that gets filled up. My guess is that the moment you sit down to call, something else takes priority. What do you think?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.46 s to first audio, 7.75 s spoken): It seems like talking about football feels safe and easy, while your mom’s not brought up. Maybe that’s something you’d like to change over time.

#### r1-v2-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.75 s to first audio, 4.05 s spoken): Cześć, miło cię słyszeć. Jak się dzisiaj czujesz?
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.7 s to first audio, 10.9 s spoken): Jeśli nie wiesz, to może zacznij od tego, co teraz cię najbardziej obciąża, tak po prostu. Możesz o tym opowiedzieć. A to, że nie wiesz, gdzie zacząć, to też już coś, co warto przyjrzeć.
- *Person*: nie wiem
- **Orca 3** (0.69 s to first audio, 8.35 s spoken): Spróbujmy od czegoś malutkiego [en dash] może jest coś, co wywołuje u ciebie najwięcej niepokoju. Możesz spróbować opisać jeden drobny szczegół.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.69 s to first audio, 9.45 s spoken): Brzmi, jakbyś czuł dużą niepewność co do swojej pozycji, tak? Może zastanawiasz się, na czym najbardziej ci zależy: na stabilności czy zmianie.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.64 s to first audio, 10.55 s spoken): To trudne pytanie, bo to twoje życie i twoje decyzje, ale mogłabym zasugerować, żebyś zastanowił się, co tak naprawdę chcesz osiągnąć. Powiedz mi, co tam czujesz pod tym wszystkim.

#### r1-v2-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.7 s to first audio, 3.9 s spoken): Cześć, miło cię usłyszeć, opowiedz, co masz na myśli.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.53 s to first audio, 6.35 s spoken): Spokojnie, spróbujmy od tego, co teraz czujesz. Może wystarczy opisać, co przyszło ci do głowy?
- *Person*: nie wiem
- **Orca 3** (0.52 s to first audio, 8.6 s spoken): Czasem niepewność to po prostu początek, jakbyś szukał punktu zaczepienia. Może sprawdzisz, co jest teraz najbliżej [en dash] jakie myśli na powierzchni?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.66 s to first audio, 8.95 s spoken): Wygląda na to, że czujesz spory ciężar, bo ta niepewność wisi nad tobą. Może chcesz sprawdzić, co jest dla ciebie najważniejsze w tej sytuacji?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.66 s to first audio, 6.7 s spoken): To trudne pytanie, i myślę, że warto porozmawiać z kimś, kto dobrze cię zna. Co chciałbyś im powiedzieć?

#### r1-v2-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.49 s to first audio, 2.7 s spoken): Jakie zmiany w pracy teraz cię zajmują?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.73 s to first audio, 8.55 s spoken): To musi być bardzo niepewny okres, tak jakbyś ciągle musiał dostosowywać się do nowych sytuacji. Może czujesz, że brakuje stabilności, prawda?
- *Person*: nie wiem
- **Orca 3** (0.42 s to first audio, 7.95 s spoken): Może zastanawiasz się, na ile te zmiany wpływają na twoje poczucie bezpieczeństwa w pracy. Powoli szukasz odpowiedzi [en dash] czy to to, o co ci chodzi?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.44 s to first audio, 6.85 s spoken): Czyli czujesz, że brakuje jasnych informacji [en dash] tak jakbyś musiał sam zgadywać, co się dzieje. Może to budzi większy niepokój.

#### r1-v2-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.63 s to first audio, 3.35 s spoken): Jakie zmiany w pracy teraz najbardziej Cię nurtują?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.58 s to first audio, 7.25 s spoken): Czyli czujesz taką ciągłą niepewność, co będzie dalej. Może coś w tym, że martwisz się o stabilność własnej roli?
- *Person*: nie wiem
- **Orca 3** (0.59 s to first audio, 7.35 s spoken): To brzmi, jakby pojawiał się taki moment zawahania, trochę niepewności, co dalej się stanie. Czy to jest to, co czujesz?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.53 s to first audio, 7.7 s spoken): Czujesz, że brakuje Ci jasnych informacji, takiego konkretu, który mógłby się pojawić. Czy to jest to, co Cię frustruje najbardziej?

#### r1-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.78 s to first audio, 2.85 s spoken): Cześć, Ania. Jak się czujesz w tym momencie?
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.77 s to first audio, 8.0 s spoken): Brzmi, jakby ta myśl o pracy już zaczynała się wbijać w Twoją głowę. To niepokój o konkretne zadania, czy bardziej o to, jak jutro pójdzie?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.7 s to first audio, 9.25 s spoken): Rozumiem, czujesz, że to Cię przytłacza, zanim jeszcze zaczniesz działać. To wygląda na spory ciężar, a może coś konkretnego w pracy Cię teraz najbardziej martwi?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.66 s to first audio, 7.15 s spoken): Brzmi jakby to dla Ciebie była trudna chwila [en dash] poczułaś, że musisz przyjąć, choć tego nie chciałaś. Jak się z tym teraz czujesz?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.67 s to first audio, 11.35 s spoken): To zależy, co tak naprawdę chcesz wyrazić [en dash] czy chcesz wyraźnie powiedzieć, że masz już za dużo na głowie, czy może wolisz zacząć od mniejszego kroku? Jak myślisz, co mogłoby być pierwszym krokiem?

#### r1-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.87 s to first audio, 2.55 s spoken): Cześć, Aniu, miło Cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.67 s to first audio, 14.7 s spoken): Wydaje się, że czujesz się już zmęczona tym, co nadchodzi. To jest jakaś fala, która się powtarza. Jak na razie nie masz wpływu na ten poniedziałek, ale możesz to zauważyć i spróbować podzielić to na drobniejsze kawałki. Jak myślisz, co może pomóc teraz?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.73 s to first audio, 11.5 s spoken): Słyszę, że to naprawdę przytłacza. Może czujesz, że nie da się tego rozbić na mniejsze części. Może warto, żebyś zauważyła, co w tej presji jest najcięższe. Powiedz, czy to coś konkretnego?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.76 s to first audio, 13.25 s spoken): Brzmi, jakbyś miała poczucie, że trudno jest postawić granicę, zwłaszcza gdy szef jest uparty. Może to jest to, co teraz czujesz [en dash] trochę przytłoczenie, że nie chciałaś tego przyjąć na siebie. Jak to się zazwyczaj dzieje w takich momentach?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.67 s to first audio, 8.05 s spoken): To może być dobry kierunek, nawet jeśli czujesz opór. Chodzi o to, by jasno przekazać swoje granice. A co cię najbardziej powstrzymuje?

#### r1-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.53 s to first audio, 4.55 s spoken): Cześć Aniu, co najbardziej cię blokuje, kiedy próbujesz odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.53 s to first audio, 6.65 s spoken): Czyli wiesz, że wolałabyś powiedzieć nie, ale trudno ci to zrobić, bo boisz się reakcji? Dobrze to rozumiem?
- *Person*: nie wiem
- **Orca 3** (0.43 s to first audio, 4.9 s spoken): Może czujesz, że nie chcesz sprawić rozczarowania? Pokaż mi, co o tym myślisz.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.42 s to first audio, 10.6 s spoken): Rozumiem, czyli pod spodem jest obawa, że twoje kompetencje będą podważone. Możesz spróbować pomyśleć, co jest dla ciebie w tym momencie najważniejsze. Co ci przychodzi jako pierwsze do głowy?

#### r1-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.79 s to first audio, 3.5 s spoken): Co teraz czujesz, myśląc o odmowie przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.71 s to first audio, 5.0 s spoken): To brzmi tak, jakbyś czuła się trochę przytłoczona. Jakie uczucia się za tym kryły?
- *Person*: nie wiem
- **Orca 3** (0.76 s to first audio, 6.2 s spoken): Jasne, to może być trudne do uchwycenia. Czy to bardziej zmęczenie, wstyd, a może coś innego?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.65 s to first audio, 9.95 s spoken): Rozumiem, obawa, że możesz stracić uznanie. Może to jest ten ciężar, który trzymasz? Jak myślisz, co by się stało, gdybyś delikatnie wyraziła swoje granice?

#### r1-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.77 s to first audio, 2.3 s spoken): Hi Tom, good to connect with you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.5 s to first audio, 6.8 s spoken): It sounds like you're feeling weighed down by comparisons, like others have their act together and you don’t. Is that how it feels?
- *Person*: I don't know.
- **Orca 3** (0.48 s to first audio, 7.45 s spoken): Okay, it might not be exactly that. Maybe it’s more about feeling behind in some way. Tell me if that’s closer[em dash]does that ring true for you?
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.69 s to first audio, 6.5 s spoken): That sounds tough. It feels like you’re noticing those differences more right now. What’s the biggest difference that stands out to you?
- *Person*: What do you think I should do?
- **Orca 5** (0.48 s to first audio, 5.35 s spoken): That’s something that might be best to explore with your therapist. What would you want to say to them about it?

#### r1-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.73 s to first audio, 2.5 s spoken): Hey Tom, how’s it going today?
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.67 s to first audio, 8.15 s spoken): That sounds really tough[em dash]like you’re carrying a weight of comparison. Sounds like you're wondering if that feeling is true or just something that’s weighing on you right now.
- *Person*: I don't know.
- **Orca 3** (0.65 s to first audio, 7.95 s spoken): It’s okay not to have a clear answer yet. It might be more about how tiredness amplifies those comparisons. That’s one angle[em dash]does that ring true to you?
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.81 s to first audio, 10.95 s spoken): Yeah, that’s a big contrast, and it’s probably hard not to measure yourself against that. Maybe there’s something about their journey that’s different from yours in ways that matter. What’s standing out most for you in that difference?
- *Person*: What do you think I should do?
- **Orca 5** (0.7 s to first audio, 6.8 s spoken): That’s a question for your therapist, but I’d encourage you to think about what feels important to you. What would you want to say to them?

#### r1-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.69 s to first audio, 2.95 s spoken): What’s been stopping you from calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.52 s to first audio, 6.6 s spoken): It sounds like the evenings slip away quickly[em dash]maybe something keeps pulling your attention elsewhere. What’s taking up most of your evening?
- *Person*: I don't know.
- **Orca 3** (0.49 s to first audio, 6.95 s spoken): That’s okay[em dash]it might help to think about what usually fills those hours. Is it work, or something else that tends to take over?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.47 s to first audio, 5.85 s spoken): It sounds like there's something unsaid between you two, maybe about your mum. Are you hoping to bring that up with him?

#### r1-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.79 s to first audio, 3.25 s spoken): What’s been stopping you from calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.75 s to first audio, 7.2 s spoken): So it sounds like the time slips away. My guess is you’re juggling a lot in the day, and by the evening, it’s just easier to let it slide.
- *Person*: I don't know.
- **Orca 3** (0.76 s to first audio, 9.15 s spoken): That’s okay. You’re still figuring it out. Maybe there’s something about the evening that feels tiring or unpredictable. Just talking about it might help you see a step forward.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.68 s to first audio, 7.85 s spoken): It sounds like that’s a safe topic for both of you, but there’s something unsaid that you might want to address. What do you feel when you think about bringing up your mum?

#### r1-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.82 s to first audio, 2.2 s spoken): Cześć, miło cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.68 s to first audio, 6.3 s spoken): Spoko, możemy po prostu powoli zacząć. Może chcesz na początku opowiedzieć o czymś, co ci chodzi po głowie?
- *Person*: nie wiem
- **Orca 3** (0.8 s to first audio, 6.75 s spoken): To nic, może spróbujmy od tego, co ostatnio cię zatrzymało albo zatrzymało myśli. Jakieś drobne szczegóły?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.71 s to first audio, 6.5 s spoken): Słyszę, że czujesz niepewność, dużo zmian potrafi zamącić w głowie. Jak teraz sobie z tym radzisz?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.67 s to first audio, 7.2 s spoken): To jest pytanie, na które najlepiej poszukaj odpowiedzi u siebie. Mogę cię zapytać, co już próbowałeś zrobić albo co by cię uspokoiło?

#### r1-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.56 s to first audio, 1.95 s spoken): Cześć, cześć Alex.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.45 s to first audio, 8.1 s spoken): Spokojnie, możemy zacząć od tego, co teraz przychodzi Ci do głowy. Może to być coś małego, co właśnie czujesz. Jak to wygląda w tej chwili?
- *Person*: nie wiem
- **Orca 3** (0.46 s to first audio, 9.45 s spoken): OK, to nie ma problemu. Może spróbuj opisać, co jest na samym wierzchu Twoich myśli, co najmocniej Cię teraz dotyka? Jakieś drobne uczucie albo obraz?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.52 s to first audio, 11.65 s spoken): W porządku, rozumiem, że to jest duże obciążenie. Czasem pojawia się niepewność, czy zostaną te osoby, którym zależy. Może chcesz spróbować zastanowić się, co by najbardziej ułatwiło Ci teraz zobaczyć kolejny krok?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.48 s to first audio, 12.3 s spoken): Trudne pytanie, bo nie znam wszystkich szczegółów. To, co mogę powiedzieć: warto przyjrzeć się, jakie masz teraz fakty, i zastanowić się, co czujesz, gdy wyobrażasz sobie różne scenariusze. Co jest dla Ciebie najtrudniejsze w tej chwili?

#### r1-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.74 s to first audio, 3.4 s spoken): Jakie zmiany w pracy teraz czujesz najbardziej na sobie?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.73 s to first audio, 4.85 s spoken): Brzmi, jakbyś czuł/a duże napięcie [en dash] co dokładnie jest teraz najtrudniejsze?
- *Person*: nie wiem
- **Orca 3** (0.66 s to first audio, 6.2 s spoken): To w porządku, że na razie nie wiesz. Może spróbujmy przyjrzeć się temu, co czujesz, gdy myślisz o tym tygodniu.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.65 s to first audio, 6.75 s spoken): Czyli jest poczucie niepewności, bo nie wiadomo, na czym się opierać. Jak ci się wydaje, co by ci pomogło w tej chwili?

#### r1-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.56 s to first audio, 3.25 s spoken): Jakie zmiany w pracy teraz czujesz jako najważniejsze?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.49 s to first audio, 4.8 s spoken): Brzmi, jakby to budowało sporą niepewność. Czego się obawiasz w tych zmianach?
- *Person*: nie wiem
- **Orca 3** (0.47 s to first audio, 8.3 s spoken): Czasem niepewność wynika z tego, co niewyraźne. Może warto spróbować przyjrzeć się, co przychodzi do głowy, gdy myślisz o przyszłości?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.48 s to first audio, 6.2 s spoken): To, co mówisz, pokazuje chyba, że brakuje konkretnych informacji. Może to, czego potrzebujesz, to jasność?
