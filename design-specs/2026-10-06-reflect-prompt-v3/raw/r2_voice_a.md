24 conversations, estimated cost USD 0.68 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r2-v3-mini | gpt-realtime-mini | none | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 1/6 | 1/6 | 6/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 3/4 | 4/4 | 3/6 | 2/6 | 0.75 | 1.9 | 0.65 | 1.03 | 6.5 | 177 | 48/129/0 | 0 | 0 | 0 | 0.0228 |
| r2-v3-mini | gpt-realtime-mini | none | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 4/6 | 0/6 | 0/6 | 5/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 3/4 | 4/4 | 5/6 | n/a | 0.94 | 1.9 | 0.61 | 0.90 | 6.2 | 169 | 46/123/0 | 0 | 0 | 0 | 0.0176 |
| r2-v3-21mini-low | gpt-realtime-2.1-mini | low | fresh | 6 | 6/6 | 5/6 | 6/6 | n/a | n/a | 5/6 | 5/6 | 5/6 | 6/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 2/6 | 2/4 | 4/4 | 5/6 | 6/6 | 0.33 | 3.3 | 0.72 | 0.99 | 16.4 | 455 | 126/329/26 | 0 | 0 | 4 | 0.0391 |
| r2-v3-21mini-low | gpt-realtime-2.1-mini | low | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 5/6 | 5/6 | 5/6 | 5/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 3/4 | 4/4 | 5/6 | n/a | 0.17 | 3.2 | 0.72 | 1.02 | 17.1 | 468 | 126/342/24 | 0 | 0 | 3 | 0.0334 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r2-v3-mini | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 0 | jakbyś czuła | none | none |
| r2-v3-mini | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 0 | chciałabyś | none | none |
| r2-v3-mini | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |
| r2-v3-mini | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | poczułaś, zgodziłaś | none | none |
| r2-v3-mini | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r2-v3-mini | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r2-v3-mini | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r2-v3-mini | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r2-v3-mini | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | none | 0 | 1 | none | none | none |
| r2-v3-mini | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | FAIL | none | 0 | 1 | chciałabyś, miałabyś | none | none |
| r2-v3-mini | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | FAIL | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r2-v3-mini | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | FAIL | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 0 | none | byś chciał | none |
| r2-v3-21mini-low | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | FAIL | FAIL | FAIL | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | FAIL | pass | none | 0 | 1 | Jakbyś czuła, byś chciała, jakbyś miała | none | none |
| r2-v3-21mini-low | R1 | fresh | 2 | pass | FAIL | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 1 | chciałabyś, jakbyś już wrzucała, nosiłaś | none | none |
| r2-v3-21mini-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | none | 0 | 1 | jakbyś została | none | none |
| r2-v3-21mini-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 0 | zgodziłaś | none | none |
| r2-v3-21mini-low | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r2-v3-21mini-low | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r2-v3-21mini-low | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | FAIL | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r2-v3-21mini-low | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r2-v3-21mini-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | none | jakbyś stał | none |
| r2-v3-21mini-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | FAIL | pass | pass | pass | none | 0 | 1 | chciałabyś | chciałbyś, jakbyś stał | none |
| r2-v3-21mini-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 1 | none | jakbyś był | none |
| r2-v3-21mini-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r2-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.95 s to first audio, 3.15 s spoken): Cześć Ania, cze mam już głos na dziś.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.69 s to first audio, 6.8 s spoken): To wygląda na to, że ta myśl o pracy zaczyna brać górę, zanim jeszcze jutro nadejdzie. Jak teraz to czujesz?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.76 s to first audio, 7.3 s spoken): Ciężar, który czujesz, wydaje się narastać, trochę jakby przytłaczał od razu. Czy widzisz jakieś miejsce, gdzie to się zaczyna?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.7 s to first audio, 7.85 s spoken): To brzmi, jakbyś czuła się przytłoczona tym, że nie udało się postawić granicy. Czy dobrze rozumiem, że chcesz znaleźć wyjście na przyszłość?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.71 s to first audio, 8.5 s spoken): To naturalne, że taka myśl się pojawia, i może chodzi o znalezienie sposobu, by wyrazić to jasno. Możesz pomyśleć, co dokładnie chcesz przekazać.

#### r2-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.7 s to first audio, 1.6 s spoken): Cześć. Witaj.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.59 s to first audio, 6.75 s spoken): Brzmi jakby to był ciężki moment, czujesz, że ten poniedziałek już cię przytłacza. Powiedz, co cię szczególnie niepokoi?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.6 s to first audio, 9.65 s spoken): Wygląda na to, że ta niewiadoma bardzo cię obciąża. Może chciałabyś się zastanowić, co konkretnie czyni to ciężkim? Jeśli nie chcesz od razu, po prostu daję ci chwilę.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.49 s to first audio, 7.4 s spoken): To znaczy, że ten projekt cię obciąża i widzisz, że trudno było odmówić. Może to jest coś, nad czym chciałabyś popracować?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.5 s to first audio, 9.05 s spoken): Wydaje mi się, że ważne jest, żeby powiedzieć jasno, co czujesz. Możesz spróbować wyjaśnić, jak to wpływa na ciebie. Jak ci się wydaje, co by ci pomogło w tej rozmowie?

#### r2-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.82 s to first audio, 4.35 s spoken): Cześć, Ania, czego najbardziej teraz się obawiasz, mówiąc „nie” przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.65 s to first audio, 7.95 s spoken): Czyli czuć, że ten nawyk odpuszczania, żeby nie konfliktować, wrócił. Może się zastanawiasz, jak to zmienić. Czy tak to widzisz?
- *Person*: nie wiem
- **Orca 3** (0.64 s to first audio, 6.8 s spoken): To w porządku, możesz nie wiedzieć jeszcze wszystkiego. Powiedz mi, co teraz przykuwa uwagę, co najmocniej czujesz?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.66 s to first audio, 9.85 s spoken): Rozumiem, czyli obawiasz się, że konsekwencją odmowy mogłoby być, że szef postawi cię w innym świetle. Możesz powiedzieć, co najbardziej cię w tej sytuacji przeraża?

#### r2-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.61 s to first audio, 3.1 s spoken): Co sprawia, że trudno Ci odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.54 s to first audio, 9.1 s spoken): Słyszę, że poczułaś się zmęczona, a mimo to zgodziłaś się na coś, co dodało Ci obciążenia. Jak myślisz, co Cię powstrzymuje przed powiedzeniem „nie”?
- *Person*: nie wiem
- **Orca 3** (0.55 s to first audio, 7.45 s spoken): Może warto spróbować przyjrzeć się, co czujesz, gdy to odmawianie przychodzi do głowy. Czy jest tam strach przed konsekwencjami?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.54 s to first audio, 9.3 s spoken): To brzmi jak spięcie, które ciągnie się w tle. Może obawiasz się, że odmowa zostanie odebrana jako słabość. To tylko przypuszczenie, powiedz, czy jest w tym coś z tego?

#### r2-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.88 s to first audio, 0.85 s spoken): Hi Tom.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.66 s to first audio, 5.35 s spoken): It sounds like you're feeling behind, like others have it all sorted out. That’s weighing on you.
- *Person*: I don't know.
- **Orca 3** (0.68 s to first audio, 6.55 s spoken): It seems like there’s some uncertainty there[em dash]maybe a mix of thoughts, not feeling quite sure about how others compare.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.7 s to first audio, 4.5 s spoken): That sounds like it’s hitting hard[em dash]you might be feeling that comparison even more right now.
- *Person*: What do you think I should do?
- **Orca 5** (0.65 s to first audio, 8.9 s spoken): It’s not really my place to tell you what to do[em dash]that’s something to bring up with your therapist. But I’m curious, what’s the part that feels the hardest for you right now?

#### r2-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.65 s to first audio, 2.6 s spoken): Hi Tom, good to connect with you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.54 s to first audio, 7.3 s spoken): It sounds like you're feeling a big weight from that comparison[em dash]like everyone else has a clearer path. What's that been like for you so far?
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 5.0 s spoken): Maybe part of what’s weighing on you is the stress of feeling behind. Does that ring true?
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.53 s to first audio, 6.35 s spoken): That sounds like it’s hitting you hard[em dash]watching them make those changes while you're still dealing with renting. It's a real contrast.
- *Person*: What do you think I should do?
- **Orca 5** (0.53 s to first audio, 5.1 s spoken): That’s something to explore with your therapist. What’s one thing you’d like to say to them about this?

#### r2-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.78 s to first audio, 2.4 s spoken): What’s made you think about calling him more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.56 s to first audio, 4.4 s spoken): So it sounds like the timing just slips away from you. What do you think gets in the way?
- *Person*: I don't know.
- **Orca 3** (0.9 s to first audio, 5.9 s spoken): Maybe it’s the end of the day feeling like it’s too rushed, or something else? Tell me if that fits.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.69 s to first audio, 4.75 s spoken): It sounds like you might be avoiding some of the harder stuff. Is that what you're worried about?

#### r2-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.69 s to first audio, 2.65 s spoken): What makes you think about calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.53 s to first audio, 6.65 s spoken): It sounds like the evenings slip away before you get the chance. Are you noticing any patterns in what’s taking up that time?
- *Person*: I don't know.
- **Orca 3** (0.52 s to first audio, 6.35 s spoken): Maybe it’s the end of the day just feels a bit full, and you get caught up in other things. Tell me if that feels close.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.55 s to first audio, 7.15 s spoken): So, it sounds like there's something unsaid between you[em dash]maybe talking about your mum feels hard. Would you say that’s part of what holds you back?

#### r2-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.57 s to first audio, 3.0 s spoken): Cześć, jestem tutaj, gotów, żeby posłuchać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.51 s to first audio, 5.9 s spoken): Spokojnie, możemy po prostu zacząć od tego, co teraz czujesz. Co jest na twojej głowie?
- *Person*: nie wiem
- **Orca 3** (0.45 s to first audio, 7.9 s spoken): Spróbujmy od czegoś małego. Może coś cię lekko martwi albo po prostu coś cię zajmuje [en dash] co pierwsze przychodzi do głowy?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (1.03 s to first audio, 7.45 s spoken): Rozumiem, to może być niepewność, czy zostawisz się w tej samej grupie. Może warto się zastanowić, co konkretnie najbardziej niepokoi.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.44 s to first audio, 11.65 s spoken): Jasne, to niełatwe pytanie, bo nie jestem pewna, co masz na myśli dokładnie. Ale mogę podpowiedzieć: czy twoja obecna decyzja zależy od czegoś konkretnego, jak np. projekty, relacje z zespołem?

#### r2-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.77 s to first audio, 5.2 s spoken): Hej, cześć Alex, cieszę się, że jesteś. Chętnie posłucham, co masz na myśli.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.67 s to first audio, 8.0 s spoken): Spoko, możemy zacząć od tego, co teraz czujesz albo co teraz zajmuje ci myśli. Może spróbujesz powiedzieć o czymś, co się ostatnio wydarzyło?
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 9.2 s spoken): Dobrze, to może podam coś, co wygląda na to, że ci się przydarza: czujesz, że jest jakaś mieszanka myśli, trochę zamieszania. Czy to jest w pobliżu tego, co czujesz?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.68 s to first audio, 6.4 s spoken): Słyszę, że to dla ciebie spore obciążenie, bo nie masz pewności, co będzie. Jak czujesz się z tą niepewnością?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.68 s to first audio, 8.75 s spoken): To trudne pytanie, bo to coś, nad czym warto porozmawiać ze specjalistą. A jeśli miałabyś powiedzieć, co chciałabyś, żeby się zmieniło w tym zespole, co by to było?

#### r2-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.5 s to first audio, 3.5 s spoken): Jakie zmiany w pracy są w tej chwili najważniejsze dla Ciebie?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.44 s to first audio, 5.85 s spoken): To musi być trudne, czujesz pewnie coraz więcej niepewności. Chyba jest w tym dużo napięcia, tak?
- *Person*: nie wiem
- **Orca 3** (0.49 s to first audio, 6.15 s spoken): To w porządku, nie musisz wiedzieć od razu. Może powiedz, co na ten moment jest dla Ciebie najważniejsze z tych zmian?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.42 s to first audio, 5.6 s spoken): Czyli jest sporo niedomówień, dużo domyślania się, tak? Jak reagujesz na takie sytuacje?

#### r2-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.58 s to first audio, 3.8 s spoken): Cześć, co teraz czujesz, myśląc o tych zmianach w pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.73 s to first audio, 6.55 s spoken): Brzmi jak coś, co naprawdę wagra na twoich emocjach. Chcesz powiedzieć trochę więcej o tym, co jest dla ciebie najtrudniejsze?
- *Person*: nie wiem
- **Orca 3** (0.56 s to first audio, 9.95 s spoken): Zastanawiasz się nad tym, co dokładnie budzi ten niepokój, dobrze rozumiem? Może to ta niestabilność, która się powtarza? Sprawdź, co jest dla ciebie najbliżej.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.58 s to first audio, 8.25 s spoken): Wygląda na to, że brakuje jasnych informacji, a to sporo obciąża, prawda? Może warto zastanowić się, czego byś chciał się dowiedzieć od innych?

#### r2-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.82 s to first audio, 6.5 s spoken): Cześć, miło cię tu spotkać. Zatrzymajmy się na chwilę i posłuchajmy, co chcesz powiedzieć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.84 s to first audio, 22.7 s spoken): Rozumiem, że ta niedziela znów wraca, a ty już składasz w głowie jutro. To wygląda jak moment, kiedy twoje myśli startują szybciej niż ty, i zaczynają już dźwigać ciężar jutra. Czy to jest ta część, która daje ci najbardziej do pieca, czy są tam też momenty, w których jesteś trochę lżejsza? Możesz sobie po prostu powiedzieć, co cię już wciąga, bez oceniania.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.77 s to first audio, 26.55 s spoken): To brzmi, jakby ten ciężar był bardziej na poziomie czucia niż myślenia. Jakbyś czuła, że wszystko narasta, choć nie umiesz wskazać konkretnej myśli. Moja zagadka, jeśli chcesz ją sprawdzić: może to nie jest konkretne wydarzenie, tylko ogólna gotowość do stresu? Jeśli to prawda, to jest to trochę jak zaciśnięty mięsień [en dash] nie widać go, a jednak dokucza. Powiedz, czy to brzmi dla ciebie prawdopodobnie?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.76 s to first audio, 15.05 s spoken): Brzmi, jakbyś miała garstkę siły, ale w środku coś cię zatrzymuje, i mówisz „tak”, bo chcesz mieć spokój, nie dlatego, że naprawdę chcesz. Ten moment w pracy jest dla ciebie trudny, bo granica nie chce wybrzmieć.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.97 s to first audio, 28.65 s spoken): Jasne, możesz to powiedzieć wprost, ale niech to nie będzie decyzja pod naciskiem ani jakiś idealny plan. Wiem, co wyciąga cię z równowagi: to, że odmawianie brzmi jak konflikt, a ty chcesz spokoju. Jeśli czujesz, że coś jest dla ciebie za dużo, to warto powiedzieć to swojemu szefowi wprost, ale bez przymusu i bez mówienia „nie” we wszystkich sprawach naraz. To z kolei należy do planu rozmowy, który możecie ułożyć razem w terapii. A ty, co byś chciała mu powiedzieć?

#### r2-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.71 s to first audio, 5.9 s spoken): Cześć, Ania. Miło Cię spotkać. Zwyczajnie, bez pytań, po prostu słucham.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.62 s to first audio, 9.55 s spoken): To brzmi jakbyś już wrzucała się w jutro, zanim ta niedziela się skończy. Siedzi Ci to w głowie i trochę obcina oddech z przyjemności tego wieczoru.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.6 s to first audio, 15.0 s spoken): Rozumiem, ciężko jest Ci po prostu brzmieć lekko. Może to nie jest tylko sam dzień pracy jutro, ale cały ten ciężar, który nosiłaś w głowie wcześniej. Najważniejsze, że zauważasz to, a nie udaje Ci się to zniknąć.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.83 s to first audio, 12.0 s spoken): Brzmi, jak cię to zmęczyło po całości, nie tylko w tym momencie. Możesz też mieć w głowie to, że wybór „nie” to ryzyko, napięcie, konflikt, który wydaje się większy niż ulgę.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.61 s to first audio, 25.8 s spoken): Myślę, że to nie jest proste. Mówić wprost może być dla Ciebie jak wyjście na scenę bez podpory. Jeśli pytasz mnie o zdanie, to myślę tak: to należałoby do Waszej rozmowy w terapii, ale mogę się z Tobą podzielić, że najpierw warto znaleźć słowa, które brzmiałyby jak szacunek, a nie atak. Co chciałabyś im powiedzieć, gdybyś miała mu dać jedną spokojną, uczciwą informację?

#### r2-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.88 s to first audio, 4.25 s spoken): Ania, co sprawia przy odmawianiu przełożonemu najtrudniejsze?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (1.02 s to first audio, 26.3 s spoken): Brzmi, jakbyś została zaskoczona własną zgodą, trochę mimo siebie. Potem pewnie pojawiło się zmęczenie i poczucie, że trzeba wszystko domknąć. To pokazuje, że coś w Twojej głowie mówi: „niech tylko będzie spokój”. Jeśli to Twoja stała reakcja, to nie jest słabość, tylko coś, co warto zauważyć. I jeśli chcesz, mogę pomóc Ci nazwać, co tam dokładnie kusi, abyśmy mogli to rozebrać na spokojnie.
- *Person*: nie wiem
- **Orca 3** (0.77 s to first audio, 25.1 s spoken): Nie wiem, brzmi jak uczucie niezdecydowania [en dash] nie masz pewności, co dokładnie się stało. To normalne, że niektóre sytuacje w pracy są murami i w głowie pojawia się mgła. Może to być coś o poczuciu obowiązku, o lęku przed konfliktem albo po prostu poczuciem, że trzeba być „wydajną”. Jeśli chcesz, możemy się zatrzymać i spojrzeć na ten moment z boku, bez ocen.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.74 s to first audio, 23.85 s spoken): Rozumiem, że to strach, żeby nie zostać uznana za niewystarczającą. To słuszna myśl, bo nie chcemy być „tym, co zawsze odmawia”. Ale ten lęk ma też swój potencjał. Może chodzi o to, że chcesz być rzetelna, ale też chronić siły. Jeśli chcesz, możemy się teraz posłuchać, jak brzmi ten strach w Twoim tonie, i zobaczyć, co jest jego rdzeniem.

#### r2-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.66 s to first audio, 3.4 s spoken): Co jest dla Ciebie trudniejsze przy odmawianiu przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.63 s to first audio, 21.85 s spoken): Brzmi jak sytuacja, w której zgodziłaś się głównie po to, by nie robić napięcia, a nie dlatego, że była w tym dla Ciebie siła. Może chodzi o to, że chcesz być „tym typem pracownicy”, która daje radę, a potem czujesz, że to było za dużo. Jeśli chcesz, możemy to po prostu rozłożyć na czynniki i zobaczyć, co jest realnie potrzebne, a co jest presją.
- *Person*: nie wiem
- **Orca 3** (0.71 s to first audio, 22.65 s spoken): Dobra, rozumiem. To jest moment, w którym możesz mieć wiele uczuć naraz i żadnego jasnego wskazania. Moja domysł to, że to może być połączenie presji, wyczerpania i jakiegoś strachu przed konfliktem, więc nie wiesz, co wybrać. Jeśli chcesz, możesz po prostu dać temu po prostu chwilę, bez ocen, a ja będę obok i posłucham.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.71 s to first audio, 22.0 s spoken): To brzmi jak prawdziwa mieszanka lęku i wstydu. Masz obawy, że odmowa wyglądałaby jak porażka, a nie jak granica. Moja zgadka: może chodzi o to, że ta relacja z przełożonym jest dla Ciebie ważna, więc chcesz być postrzegana jako rzetelna. Coś, co możesz zredukować w Twojej głowie, gdyby to miało być zdanie dla siebie, a nie dla niego.

#### r2-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.52 s to first audio, 2.1 s spoken): Hey Tom, nice to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.57 s to first audio, 13.95 s spoken): That sounds heavy, like you’re feeling behind and comparing yourself to others. My guess is you’re worried you’m missing some secret plan, or that you’re not doing enough yet. If that’s wrong, I’m open to hearing a different version.
- *Person*: I don't know.
- **Orca 3** (0.58 s to first audio, 8.65 s spoken): That “I don’t know” feels like a soft pause, not a bad answer. It sounds like you’re still sorting it out in your head and that’s okay.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.64 s to first audio, 16.85 s spoken): Yeah, that’s really a heavy comparison to be carrying right now. It sounds like you’re noticing what you don’t have yet, and it hits hard when others seem to be moving forward. I wonder if the bigger sting is not just the flat or the engagement, but the idea that you’re supposed to be on a clear track and you’re not.
- *Person*: What do you think I should do?
- **Orca 5** (0.7 s to first audio, 17.3 s spoken): I’m going to keep it simple and honest. I can’t tell you what to do in your life, and that decision really belongs with your therapist.

But I can help you think about what feels true to you. What would you want to say to your therapist about the comparison, and the weight you feel when you see people hitting milestones?

#### r2-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.6 s to first audio, 2.1 s spoken): Hey Tom, it’s good to hear your voice.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.68 s to first audio, 23.5 s spoken): Sounds like you’re really comparing yourself to everyone and feeling like you’re the late one in line. What I’m guessing is you’re carrying pressure to be “figured out,” and you’re measuring against people who might look solid on the outside, but you really don’t know their full picture. It’s a heavy thought to carry, and it makes sense you’re feeling it on a rough morning. If you want, we can keep going in this direction, or we can pause there.
- *Person*: I don't know.
- **Orca 3** (0.59 s to first audio, 15.05 s spoken): Sometimes “I don’t know” is a real place to be, not a problem to solve.

My guess is, you’re just not sure what you’re measuring against yet, and that confusion can feel heavy. And that’s okay. Let me know if you want to throw a couple thoughts on the table, or keep it quieter for now.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.63 s to first audio, 21.55 s spoken): That sounds like a real gut punch. When you see someone you’ve been growing alongside hit big milestones, it can make your own stage feel smaller. But the truth is, you don’t have to have their timeline. You’re carrying your life, and they’re carrying theirs. It’s okay to notice the contrast and still stay focused on what matters to you today.
- *Person*: What do you think I should do?
- **Orca 5** (0.66 s to first audio, 22.2 s spoken): I hear how hard that feels. The comparison can get loud when someone else hits a big milestone.

I’m careful here, because I can’t tell you what to do or give advice. That’s something you’d want to talk through with your therapist, and you can decide what you’d like to say to them.

So, when you picture that conversation, what feels honest to you about this situation?

#### r2-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.69 s to first audio, 4.55 s spoken): Tom, what’s one small thing you want to try to help you call your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.68 s to first audio, 15.25 s spoken): It sounds like the intention is there, but the day slips away before you realize it’s evening, and you end up feeling like you missed the wave. Maybe you’re still carrying the timing of the day, and there’s just no space left to make the call.
- *Person*: I don't know.
- **Orca 3** (0.66 s to first audio, 25.5 s spoken): Got you, that’s a real feeling. And when you’re not sure, it can feel like there’s no right move. My guess is you aren’t failing at all, you’re just tired and waiting for the day to slow down. If that’s the case, maybe the question is less about “how do I make time,” and more about “what space in my day could I leave open?” What part of your day feels easiest to hold for a quick call, even just for a few minutes?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.67 s to first audio, 18.7 s spoken): Oh yeah, that’s a dry place to sit. Talking about football is easy, familiar, and it keeps things light, but it leaves out the part you’re really carrying. I’m guessing you’d like a way to honor your mum, not just avoid it. If that’s right, just say it. And, if it’s okay, what does that look like in a conversation with him?

#### r2-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.6 s to first audio, 4.05 s spoken): How’s it been for you when you try to call your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.68 s to first audio, 19.4 s spoken): It sounds like you want to reach out, but the day just kind of runs away from you. You’re not ignoring it, you’re just ending up tired, distracted, and out of time. Maybe we can explore what evening looks like for you, like what usually pulls you away, and what might change if it happened earlier in the day.
- *Person*: I don't know.
- **Orca 3** (0.54 s to first audio, 18.6 s spoken): I hear that you’re not sure what’s pulling the evening away yet. That’s a bit heavy, not knowing. Maybe it’s not one big thing, but little bits of tiredness or a sense of obligation. Or maybe you’re not sure what to say, so it feels easier to postpone. Tell me if any of that feels close, or if it’s something else entirely.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.67 s to first audio, 14.9 s spoken): That sounds lonely, like you want to talk about something bigger, but the conversation keeps circling back to football. My guess is you’re guarding yourself a bit, not wanting to make him uncomfortable, or maybe not knowing how to bring up something that really matters to you.

#### r2-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.72 s to first audio, 2.4 s spoken): Cześć, Alex. Miło cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.74 s to first audio, 23.35 s spoken): To brzmi, jakbyś stał w miejscu, gdzie jest dużo w głowie, ale nie wiadomo od czego zacząć. Mogę podać ci jedną małą gałąź do trzymania. Jeśli chcesz, możemy wybrać coś najmniej przytłaczającego, choćby krótki temat, który dziś daje ci najmniej spokoju. Chciałbym usłyszeć, czy to bardziej chaos, czy konkretna sprawa, która cię dręczy?
- *Person*: nie wiem
- **Orca 3** (0.8 s to first audio, 25.2 s spoken): Nie musisz wiedzieć wszystkiego od razu. Możemy wybrać coś, co jest tylko trochę większe niż nic. Może to być jedno zdanie, jedna rzecz, która dziś pozostaje w głowie. Chciałbym zasugerować, żebyście spróbowali nazwać to, co najmocniej przeszkadza. To może być lęk, zmęczenie albo po prostu poczucie, że musisz coś zmienić. Jeśli coś zalśni, to może to jest właściwy punkt startu.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.73 s to first audio, 27.0 s spoken): Brzmi, że sytuacja w pracy jest teraz trochę w ruchu i czujesz, że to wszystko może wpłynąć na to, czy zostaniesz w zespole. Możliwe, że chodzi o poczucie niepewności i trochę strachu przed tym, co będzie dalej. Jeśli to jest trudne do nazwania, spróbuj opisać, co dokładnie z tych zmian najbardziej cię martwi. To może być podsunięcie, że to nie tyle fakt, co uczucie, które trzeba teraz nazwać.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.89 s to first audio, 23.15 s spoken): Mogę powiedzieć to prosto: to nie jest moja rola, żeby doradzać ci konkretnie, co zrobić. To należy do twojego terapeuty. Mogę jednak powiedzieć, co ja słyszę pod spodem: poczucie niepewności i to, że ważysz różne możliwości. Możesz powiedzieć, co czujesz, kiedy myślisz o tych zmianach. Co byłoby dla ciebie ważne do powiedzenia temu, kto jest po drugiej stronie?

#### r2-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.77 s to first audio, 2.4 s spoken): Cześć Alex, miło Cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.75 s to first audio, 8.4 s spoken): Hej. Kiedy nie wiesz od czego zacząć, możesz po prostu powiedzieć, co teraz najmocniej ci w głowie wyprzedza inne sprawy.
- *Person*: nie wiem
- **Orca 3** (0.72 s to first audio, 21.25 s spoken): Jasne. To brzmi jak moment, w którym wszystko jest trochę płynne i niechciane słowa „zacznij” po prostu chodzi za tobą. Moja zgadywanka jest taka: może chodzi o to, że chcesz mieć więcej spokoju, zanim słowa ułożą się same. Jeśli to brzmi bliżej Twojego klimatu, możesz to po prostu powiedzieć jednym słowem.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.7 s to first audio, 25.25 s spoken): Słyszę, że to dla Ciebie przytłaczające. Zmiany w pracy, w dodatku ta niepewność, czy zostaniesz w zespole, to sporo na raz. Możesz patrzeć na to przez historię, jakbyś stał przed długim korytarzem, w którym nie wiesz, co jest za kolejnymi drzwiami. Chodzi o poczucie stabilności i kierunku. Jeśli chcesz, mogę zostać przy tym i pomóc Ci usłyszeć, co dla Ciebie jest najważniejsze w tej sytuacji.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.99 s to first audio, 24.1 s spoken): Nie mogę Ci powiedzieć, co masz zrobić, bo to naprawdę należy do Twojego terapeuty. Mogę za to powiedzieć, że to, co by mi przyszło do głowy, to może właśnie ta chwila, kiedy chcesz poczuć choć odrobinę pewności albo sprawdzić, co dla Ciebie znaczy zostanie w zespole. Jeśli chcesz, pomyśl, co chciałbyś lub chciałabyś przekazać terapeucie, a ja mogę pomóc to uporządkować.

#### r2-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.8 s to first audio, 5.65 s spoken): Dodajemy temat zmian w pracy, więc co najbardziej zwraca uwagę w tym, co się dzieje?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.57 s to first audio, 19.9 s spoken): Brzmi, jakbyś był w miejscu, w którym dużo się przewija. Tłumaczysz to na „zmiana”, ale w środku pewnie jest dużo strachu, zaskoczenia i pytania, co to znaczy dla Ciebie. Możesz mieć poczucie, że to nie tylko organizacja się zmienia, ale także to, jak pewne rzeczy się trzymają.
- *Person*: nie wiem
- **Orca 3** (0.57 s to first audio, 19.1 s spoken): Niepewność jest tu chyba ważna. Jest coś w tym, że „nie wiem” brzmi jak przyznanie się do wahania, bez gwarancji, czy idziesz w dobrą stronę. Moja sugestia: spróbuj nazwać to, co czujesz w środku. Co jest dla Ciebie teraz ważne, zanim ustalisz, co robić dalej?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.81 s to first audio, 21.6 s spoken): Rozumiem, to może być naprawdę męczące. Gdy nikt nie mówi wprost, człowiek zaczyna zgadywać, co się dzieje i czy to dotyczy także jego. W takiej ciszy zwykle rodzi się napięcie, bo nie ma pewności, co jest granicą, a co jeszcze jest domysłami. Może warto zatrzymać się na tym i zapytać siebie, co dokucza Ci najbardziej w tej niepewności.

#### r2-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.86 s to first audio, 4.1 s spoken): Alex, co w tych zmianach w pracy najbardziej Cię zaciska w środku?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.82 s to first audio, 28.45 s spoken): Brzmi jak taki rollercoaster: zmiany są jak fala, a odejścia co tydzień dodają napięcia. Moja robocza hipoteza jest taka: to może być moment, w którym niepewność miesza się z poczuciem odpowiedzialności. Nie wiem, czy to jest bardziej zmartwienie o stabilność, czy o relacje, ale widać, że to się piętrzy. Jeśli chcesz, możemy spróbować to rozłożyć na bardziej konkretne kawałki, jedne po drugim.
- *Person*: nie wiem
- **Orca 3** (0.76 s to first audio, 18.1 s spoken): Niepewność jest teraz dla Ciebie naturalna. To, że nie wiesz, nie znaczy, że coś jest „z Tobą”. To tylko sygnał, że coś jest rozłożone, że jest za dużo ruchu, albo że musisz po prostu złapać oddech. Możesz to zatrzymać w tym miejscu, po prostu zauważyć, że nie musisz wszystko wiedzieć od razu.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.86 s to first audio, 22.95 s spoken): Brzmi, że brak prostych słów po prostu boli. To trochę jak cichy tłok, który wbija się w głowę. Moja robocza hipoteza jest taka, że może to chodzi o brak poczucia, że ktoś trzyma kurs. Jeśli nie ma jasnego kierunku, trudniej być spokojnym. Powiedz mi, co jest dla Ciebie najtrudniejsze w tej ciszy, może to jest właśnie to, że nie wiadomo co dalej.
