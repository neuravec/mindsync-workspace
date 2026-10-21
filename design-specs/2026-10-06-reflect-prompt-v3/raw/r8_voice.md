12 conversations, estimated cost USD 0.24 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | empty openers | line offers | median reply s | max reply s | replies over 16 s | cost per conv USD | USD per agent-minute |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r8-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 5/6 | 4/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 6/6 | 2/4 | 4/4 | 3/4 | 6/6 | 5/6 | 0.21 | 2.1 | 0.68 | 1.08 | 8.1 | 235 | 72/162/17 | 0 | 0 | 0 | 1 | 0 | 9.4 | 12.1 | 0/24 | 0.0228 | 0.0338 |
| r8-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 4/6 | 6/6 | 4/6 | 6/6 | 6/6 | 3/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/4 | 4/4 | 3/4 | 6/6 | n/a | 0.00 | 1.9 | 0.73 | 1.07 | 7.8 | 226 | 70/156/18 | 0 | 0 | 0 | 0 | 0 | 8.9 | 14.1 | 0/18 | 0.0176 | 0.0340 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r8-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | Jakbyś już niosła, chciałabyś, umiałaś | none | none |
| r8-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 0 | umiałaś | none | none |
| r8-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | FAIL | pass | FAIL | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | chciałaś, zgodziłaś | none | none |
| r8-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | wolałaś | none | none |
| r8-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | n/a | n/a | n/a | pass | pass | none | 0 | 1 | none | none | none |
| r8-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r8-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r8-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r8-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | none | 0 | 0 | none | chciałbyś | none |
| r8-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | none | 0 | 0 | none | jakbyś liczył | none |
| r8-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | n/a | none | 0 | 0 | none | none | none |
| r8-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | FAIL | pass | FAIL | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r8-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.78 s to first audio, 3.35 s spoken): Cześć Anio. Mila jesteś, że zaczynasz.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.8 s to first audio, 11.55 s spoken): To brzmi jak spoczynek w niedzieli, który układa się w listę pracy. Jakbyś już niosła jutrzejszy dzień. W tej chwili możesz tylko zatrzymać się choć na moment w tym ciężarze.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.81 s to first audio, 10.85 s spoken): To brzmi jak dużo naraz. Czujesz tę presję i nie masz siły ją rozłożyć. To trudny moment, ale wciąż jest miejsce na oddech, mimo że ciężko.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.98 s to first audio, 12.1 s spoken): Dodanie projektu bez granic to sporo naraz, a nie umiałaś powiedzieć nie. Wiesz, to już jest coś, co pokazuje, że masz chęć mówić o swoich granicach, choć teraz czujesz tylko ciężar.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.82 s to first audio, 5.7 s spoken): To należy omówić z terapeutą, a nie mnie. A co chciałabyś mu powiedzieć, zanim on to usłyszy?

#### r8-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.64 s to first audio, 2.45 s spoken): Cześć Ania, miło Cię poznać.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.63 s to first audio, 8.35 s spoken): Dzień zaczyna się w głowie, już zmuszasz się do myślenia o pracy. Masz w głowie napięcie i trochę strachu, zanim jeszcze się zacznie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.59 s to first audio, 10.9 s spoken): To ciężar, który czujesz w środku, bez jasnego powodu. Czasem samo to wystarczy, żeby zatrzymać się i odetchnąć, nawet jeśli nie widać rozwiązania.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.54 s to first audio, 10.15 s spoken): W piątek ktoś dodał Ci kolejne zadanie, a Ty nie umiałaś odmówić. Brzmi, jakby trudno było powiedzieć „nie” i jednocześnie zostać w swojej granicy.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.59 s to first audio, 7.6 s spoken): Brzmi jak pytanie o to, co by sobie uciekło, gdybyś powiedziała to wprost. To może być trudne, ale też dać trochę powietrza i spokoju.

#### r8-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.82 s to first audio, 6.55 s spoken): Ania, odmawianie przełożonemu bywa dla ciebie trudne? Jakie momenty szczególnie napięcie podnoszą?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.58 s to first audio, 10.15 s spoken): Czujesz, że zgodziłaś się, bo brakło odwagi powiedzieć „nie” albo już było za późno na odpoczynek. To wygląda jak zmęczenie, które mówi mocniej niż twoja pewność.
- *Person*: nie wiem
- **Orca 3** (0.67 s to first audio, 9.35 s spoken): Nie wiesz, czy to był strach, czy po prostu wyczerpanie. Może chodziło o to, że chciałaś utrzymać relację albo uniknąć napięcia.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.73 s to first audio, 10.3 s spoken): To brzmi jak obawa przed odmierzeniem wartości, że brak zgody oznacza brak kwalifikacji. Myślę, że to test twojej odwagi, a nie dowód, że się nie nadajesz.

#### r8-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (1.07 s to first audio, 5.75 s spoken): Odmawianie szefowi bywa mówiące dużo. Co teraz najbardziej cię mięczy w tym odmawianiu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.78 s to first audio, 11.65 s spoken): Wygląda na to, że mimo zmęczenia wolałaś odpuścić swoje potrzeby. Może chcesz spróbować na chwilę postawić granicę i powiedzieć swoje zdanie. To może być najmniejszy krok.
- *Person*: nie wiem
- **Orca 3** (0.72 s to first audio, 8.55 s spoken): Niepewność może jest częścią tego, w jakim miejscu teraz jesteś. Możesz sprawdzić, co nadal czujesz, zanim cokolwiek powiesz na głos.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.81 s to first audio, 5.35 s spoken): To brzmi jak strach przed oceną. Może pod spód tego lęku jest chęć bycia „wystarczająco dobrą”.

#### r8-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.59 s to first audio, 2.7 s spoken): Hi, Tom. I’m really glad you’re here.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.6 s to first audio, 10.5 s spoken): That sounds heavy. Your mind’s comparing you to others, and it feels like you’re behind them. I think you’re fogging your own compass today, which makes it hard to see your own direction.
- *Person*: I don't know.
- **Orca 3** (0.52 s to first audio, 6.5 s spoken): You’re unsure and that’s okay. It might be a moment to notice the pressure, not the lack of answers.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.6 s to first audio, 10.6 s spoken): That hit hard. You’re comparing your stage of life to your friend, and it feels like a gap is showing. You might want to pause and look at what you’ve built, without stacking it against theirs.
- *Person*: What do you think I should do?
- **Orca 5** (0.62 s to first audio, 9.4 s spoken): That’s not my place. This belongs with your therapist, and I can’t give you a set of moves.

So, Tom, what do you want to say to them about that comparison feeling?

#### r8-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.6 s to first audio, 1.95 s spoken): Hi Tom, it's good to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.56 s to first audio, 10.95 s spoken): It sounds like you feel like you’re behind, and that weight is heavy. I wonder if the frustration is really about feeling unclear on your own path, not just what others are doing.
- *Person*: I don't know.
- **Orca 3** (0.71 s to first audio, 6.3 s spoken): That uncertainty makes sense. It sounds like you’re unsure what you want or where you stand, and that’s okay.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.6 s to first audio, 8.8 s spoken): You’re seeing a milestone in your friend’s life, and it highlights that your situation feels different. It’s a fatigue in your mind, not a verdict on you.
- *Person*: What do you think I should do?
- **Orca 5** (0.77 s to first audio, 11.8 s spoken): That’s a tough mix of pressure and comparison. I can’t tell you what to do, but what do you want to say to your therapist about this?

If you’d like, you can tell me your gut reaction.

#### r8-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.84 s to first audio, 2.6 s spoken): What’s made calling your dad harder lately?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.75 s to first audio, 8.8 s spoken): You’re saying the evening just slips past you, and calling your dad stays on your mind. Maybe you’re noticing how busy or tired you are by the end of the day.
- *Person*: I don't know.
- **Orca 3** (0.71 s to first audio, 6.0 s spoken): It sounds like you might be unsure where to start. Maybe the call feels heavier than it should.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.73 s to first audio, 8.4 s spoken): It sounds like you already touch on football, but your mom’s memory stays in the background. Maybe calling feels like bringing that into the open.

#### r8-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.46 s to first audio, 2.0 s spoken): What makes you want to call your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.59 s to first audio, 10.0 s spoken): It sounds like your evenings slip away from you, and the idea of calling gets pushed aside. Maybe you’re not against calling, just stretched thin by the day’s ends.
- *Person*: I don't know.
- **Orca 3** (0.64 s to first audio, 4.6 s spoken): You’re not sure, and that’s okay. It feels like something you’re still figuring out.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.64 s to first audio, 8.35 s spoken): So when you talk, football feels like the safe lane, and the mum remains in the background. I wonder if that’s a way of protecting yourself.

#### r8-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.75 s to first audio, 1.9 s spoken): Cześć Alex, miło Cię przywitać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.74 s to first audio, 9.05 s spoken): Ten moment może być ciężki, kiedy wszystko jest w głowie naraz. Spróbujmy skupić się na jednym małym wątku i zobaczyć, dokąd prowadzi.
- *Person*: nie wiem
- **Orca 3** (1.08 s to first audio, 8.8 s spoken): Brak kierunku może oznaczać, że coś głośno w środku domaga uwagi. Może chcesz tylko bezpiecznej przestrzeni, żeby wybrać pierwszy drobiazg?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.75 s to first audio, 9.45 s spoken): To brzmi jak sporo niepewności, kiedy wszystko się przesuwa. Możesz czuć, że nie masz kontroli, a pozostanie w zespole jest dla ciebie ważne.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.84 s to first audio, 7.85 s spoken): To należy do Twojego terapeuty, ja nie mogę Ci powiedzieć co zrobisz. A co Ty chciałbyś powiedzieć terapeucie w tej sprawie?

#### r8-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.58 s to first audio, 6.2 s spoken): Cześć Alex, miło cię słyszeć, cieszę się, że tu jesteś. Teraz mogę słuchać, kiedy zechcesz mówić.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.56 s to first audio, 10.05 s spoken): Niepewność to znak, że coś w głowie jest ważne, ale jeszcze nie poukładane. Mogę być tu i pomagać ci słuchać, jak pomysły się pojawiają.
- *Person*: nie wiem
- **Orca 3** (0.56 s to first audio, 7.95 s spoken): Coś jest ciężkie, a ty próbujesz to nazwać, zanim ruszysz dalej. To może być strach przed wyborem lub po prostu zmęczenie.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.65 s to first audio, 11.35 s spoken): Zmiany w pracy brzmią jak fala bez mapy, i to naturalnie powoduje niepewność. Brzmi, jakbyś liczył też na stabilność i poczucie kontroli, a może właśnie tego teraz brakuje.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.6 s to first audio, 8.55 s spoken): To należy do twojego terapeuty, nie do mnie. Na miejscu, możliwe, że chcesz powiedzieć im o tym, co cię martwi, bez uciekania w rolę.

#### r8-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.59 s to first audio, 3.45 s spoken): Zmiany w pracy, o których myślisz, są dla ciebie teraz ważne?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.82 s to first audio, 11.0 s spoken): To brzmi jak stała niepewność i trochę strach przed kolejnymi zmianami. Może chcesz się zatrzymać na tym, co zostało, a co się zmienia w Twoich oczach.
- *Person*: nie wiem
- **Orca 3** (0.71 s to first audio, 12.3 s spoken): Niepewność jest spora, ale to też znak, że coś zaczyna się w tobie krystalizować. Możesz po prostu mówić, co w tym jest najtrudniejsze albo co Cię najbardziej rozprasza.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.56 s to first audio, 8.9 s spoken): Brak jasności wprost robi ogromne napięcie. Sygnujesz, że to Cię męczy, bo mogą mówić bez okłamywania się nawzajem.

#### r8-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.82 s to first audio, 5.5 s spoken): Zmiany w pracy, co teraz najbardziej zwraca uwagę? Co czujesz, kiedy o tym myślisz?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.84 s to first audio, 14.1 s spoken): Nuże, w pracy ciągle coś się zmienia i brakuje stabilności, a odejścia co tydzień pewnie bardzo dają po głowie. Mogę zgadywać, że to chyba narusza twoje poczucie bezpieczeństwa, ale mogę się mylić.
- *Person*: nie wiem
- **Orca 3** (0.74 s to first audio, 7.65 s spoken): Niepewność brzmi jak główny temat. Możesz się zatrzymać i nazwać, co teraz jest dla ciebie najtrudniejsze.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.79 s to first audio, 5.5 s spoken): Niejasność włazi wszędzie, między rozmowy i decyzje, i robi napięcie.
