24 conversations, estimated cost USD 0.29 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | empty openers | line offers | median reply s | max reply s | replies over 16 s | cost per conv USD | USD per agent-minute |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v31-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 5/6 | 5/6 | 5/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 4/6 | 6/6 | 2/4 | 4/4 | 4/4 | 6/6 | 6/6 | 0.29 | 2.0 | 0.71 | 1.17 | 8.5 | 246 | 76/169/18 | 0 | 0 | 1 | 2 | 0 | 9.1 | 19.5 | 2/24 | 0.0229 | 0.0325 |
| v31-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 5/6 | 6/6 | 5/6 | 6/6 | 6/6 | 4/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/4 | 4/4 | 4/4 | 5/6 | n/a | 0.06 | 1.7 | 0.64 | 0.82 | 8.2 | 233 | 70/164/15 | 0 | 0 | 0 | 0 | 0 | 9.6 | 12.9 | 0/18 | 0.0190 | 0.0348 |
| v31-text | gpt-5.4-mini | none | fresh | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/4 | 4/4 | 4/4 | 6/6 | 6/6 | 0.21 | 2.0 | n/a | n/a | n/a | 47 | n/a | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | 0.0031 | n/a |
| v31-text | gpt-5.4-mini | none | seeded | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 3/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 6/6 | 4/4 | 4/4 | 4/4 | 6/6 | n/a | 0.00 | 2.0 | n/a | n/a | n/a | 50 | n/a | 0 | 0 | 0 | 1 | 0 | n/a | n/a | n/a | 0.0028 | n/a |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v31-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, poczułaś, słyszałaś | none | none |
| v31-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, jakbyś była | none | none |
| v31-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | FAIL | pass | FAIL | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | none | 0 | 0 | jakbyś była, zgadałaś | none | none |
| v31-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś starała, zgodziłaś | none | none |
| v31-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v31-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v31-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| v31-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| v31-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | none | 0 | 1 | none | chciałbyś, podjąłeś | none |
| v31-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | none | 0 | 1 | none | chciałbyś | none |
| v31-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| v31-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| v31-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | jakbyś już widziała | none | none |
| v31-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | brałaś, chciałabyś, wzięłaś | none | none |
| v31-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| v31-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś powiedziała, miałaś, wiedziałaś, zgodziłaś | none | none |
| v31-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v31-text | R2 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v31-text | R2 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| v31-text | R2 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 1 | none | none | none |
| v31-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| v31-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| v31-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| v31-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### v31-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.56 s to first audio, 2.1 s spoken): Cześć Ania, miło, że tu jesteś.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.67 s to first audio, 10.2 s spoken): Znowu ta niedziela, i czujesz, że jutro już cię zaprasza do napięcia. Może to, co czuje się trudne, to prawo do przerwy w głowie, nawet gdy praca łapie za rękę.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.59 s to first audio, 11.7 s spoken): To brzmi jak ciężki, narastający stan, nie jak zwykłe „mam gorszy dzień”. Może pod spodem jest poczucie, że coś cię przytłacza, ale nie odważysz się tego nazwać.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.52 s to first audio, 10.0 s spoken): Brzmi, że poczułaś ciężar i bezradność, kiedy to słyszałaś. To częsty moment, żeby zatrzymać się i przyjrzeć się, co jest dla ciebie granicą.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.72 s to first audio, 6.95 s spoken): To pytanie należy do waszej relacji i rozmowy z terapeutą. A co chciałabyś mu szczerze powiedzieć, gdybyś miała to wyrazić teraz?

#### v31-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.69 s to first audio, 2.95 s spoken): Cześć, Aniu, miło mi z tobą rozmawiać.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.62 s to first audio, 8.95 s spoken): To jakbyś była w środku tego „jutro”, jeszcze przed sobą. Widzisz, że to co teraz namęcza, to lęk i napięcie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.76 s to first audio, 6.45 s spoken): To brzmi, że nie ma miejsca na spokój. Może chcesz poczuć ciężar bez tłumaczenia, że coś jest „w porządku”?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.52 s to first audio, 10.9 s spoken): To brzmi jak moment, gdy czujesz presję i jesteś rozdarta między tym, co chcesz, a tym, co musisz. Może podskórnie chodzi o to, że chcesz spokojnie się sprzeciwić, bez poczucia winy?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.7 s to first audio, 12.25 s spoken): To należałoby omówić z terapeutą. Myślę, że ważne jest, żebyś powiedziała to, co czujesz, bez poczucia winy. Co chciałabyś mu powiedzieć, gdybyś miała pełną swobodę?

#### v31-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.54 s to first audio, 5.7 s spoken): Jak to wygląda u ciebie, kiedy odmawiasz przełożonemu? Co najwięcej komplikuje tę sytuację?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.72 s to first audio, 12.95 s spoken): Wygląda na to, że zgadałaś się, żeby uniknąć napięcia. To brzmi, jakbyś była trochę zmęczona, a jednak czuła presję. A może chcesz wybrać moment, kiedy będziesz miała trochę więcej energii?
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 11.05 s spoken): Niepewność brzmi jak uczucie, które ciężko dźwigać bez planu. Jeśli chcesz, możemy to przemyśleć razem [em dash] co nieświadomie trzymasz tam dla siebie.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.68 s to first audio, 11.25 s spoken): Brzmi, jakby bycie odważną w odmawianiu ludziom było dla ciebie równe poczuciu bycia niewystarczająco dobra. Może pod spodem jest chęć bycia lubianą i brakuje bezpiecznego trochę luzu.

#### v31-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.82 s to first audio, 5.4 s spoken): Jak to odmawianie przełożonemu wygląda dla ciebie w praktyce, co najbardziej cię blokuje?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.66 s to first audio, 9.85 s spoken): Dodatkowy projekt znów pojawił się, a ty zgodziłaś się mimo braku siły. To brzmi, jakbyś starała się unikać konfliktu albo rozrycia pracy.
- *Person*: nie wiem
- **Orca 3** (0.62 s to first audio, 6.25 s spoken): Niepewność brzmi tu jak to, że sama czujesz, że coś jest nie tak, ale jeszcze nie umiesz tego nazwać.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.73 s to first audio, 7.55 s spoken): Bojisz się, że odmowa zrobi zaledwie „słabą pracownicę”. Czujesz, że to ryzyko jest większe niż koszt, który płacisz teraz.

#### v31-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.64 s to first audio, 2.1 s spoken): Hey Tom, nice to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.54 s to first audio, 6.05 s spoken): Sounds like you’re feeling behind and it’s clinging to you. I wonder if that feeling comes up when you’re tired.
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 8.85 s spoken): I heard you say it’s uncertain, like you’re not sure about the whole thing. My guess is that you’re trying to compare yourself to others, and that feels heavy.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.61 s to first audio, 9.05 s spoken): That’s a tough comparison, and it can sting when milestones hit. I’m guessing you’re wondering if you’re behind or if your path just looks different right now.
- *Person*: What do you think I should do?
- **Orca 5** (0.65 s to first audio, 6.3 s spoken): It belongs in your therapist’s space, not mine. I’ll ask you this: What would you want to tell them about this?

#### v31-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.6 s to first audio, 2.05 s spoken): Hey Tom, nice to talk with you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.66 s to first audio, 9.15 s spoken): It sounds like you’re comparing yourself to others and feeling behind. The guess is that the hard part is the pressure to have everything sorted, all at once.
- *Person*: I don't know.
- **Orca 3** (0.79 s to first audio, 6.05 s spoken): It is okay to be unsure. Maybe you’re tired and that comparison is louder today than usual.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.59 s to first audio, 6.35 s spoken): That’s a tough moment to sit with. It feels like you’re measuring your progress against theirs, and that can sting.
- *Person*: What do you think I should do?
- **Orca 5** (0.64 s to first audio, 11.45 s spoken): That’s a tough spot, and I hear the sting in it. Your situation belongs with your therapist, but I can help you draft what you’d say to them instead. What part feels hardest to name right now?

#### v31-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.54 s to first audio, 3.35 s spoken): So, what’s getting in the way of calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.76 s to first audio, 8.1 s spoken): It sounds like you’re not avoiding him, you just run out of time in the evening. Maybe there’s a part of you that still wants that connection but keeps drifting.
- *Person*: I don't know.
- **Orca 3** (0.64 s to first audio, 10.3 s spoken): It sounds like you’re listening for clarity, but you’re not naming a clear block yet. Maybe there’s a tiny drop of guilt or just a full schedule.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.76 s to first audio, 8.95 s spoken): It sounds like when you do connect, it’s safe and familiar, but the deeper stuff, the memory of your mum, stays in the background.

#### v31-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.56 s to first audio, 2.85 s spoken): Do you want to get better at calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.61 s to first audio, 10.45 s spoken): It sounds like the evenings just slip by, and you notice it after it’s already gone.

Maybe there’s a small moment you could pick to try once, even if it’s short.
- *Person*: I don't know.
- **Orca 3** (0.58 s to first audio, 7.8 s spoken): That feels like a kind of stuckness, not confusion. Maybe you’re avoiding something, or just tired at the wrong time.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.57 s to first audio, 8.4 s spoken): That’s a big feeling, and it makes sense that it feels off. It sounds like you’re holding more than just sports, and that gap might be part of the weight.

#### v31-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (1.17 s to first audio, 2.35 s spoken): Cześć Alex, miło Cię poznać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.81 s to first audio, 6.25 s spoken): Jasne, zaczynamy od momentu, który teraz czujesz. Masz pod górkę i to jest w porządku.
- *Person*: nie wiem
- **Orca 3** (0.7 s to first audio, 15.9 s spoken): Wygląda na to, że czujesz się trochę zagubiony. Może podjąłeś próbę wracania do tematu, ale jeszcze nie wiesz, co w nim najważniejsze. Moja propozycja jest taka: jeszcze przez chwilę posłuchaj tego, co w Tobie się nasuwa bez nacisku na rozwiązania.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.89 s to first audio, 8.55 s spoken): Zmieniasz perspektywę, a nie wiesz, czy zostaniesz w zespole. Może najważniejsze jest to, że czujesz napięcie i chcesz wiedzieć, co będzie dalej.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.84 s to first audio, 7.9 s spoken): To jest pytanie, które trzeba zostawić dla Twojego terapeuty. Powiedz, co chciałbyś powiedzieć im o tym, co teraz odczuwasz.

#### v31-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.88 s to first audio, 2.1 s spoken): Cześć Alex, miło cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.91 s to first audio, 12.0 s spoken): Brzmi, jakby ta rozmowa była dla ciebie dużym krokiem. Możemy zacząć od jednojej rzeczy, która teraz najbardziej kręci ci się w głowie, i zobaczyć, co z tego wyjdzie.
- *Person*: nie wiem
- **Orca 3** (0.78 s to first audio, 11.1 s spoken): Myślę, że cię gdzieś w środku zatrzymuje. Jedną z tych myśli, które wchodzą i robią szum, a potem znów milkną. Jeśli chcesz, możemy ją nazwać, choćby jednym słowem.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.81 s to first audio, 19.5 s spoken): Słyszę, że te zmiany w zespole robią szum i zastanawiasz się, czy to dalej będzie twoje miejsce. To może też chodzić o poczucie kontroli, że nie wiesz, czy możesz zostać. Jeśli chcesz, możemy to rozebrać na drobne kroki, tak żeby zobaczyć, co z tych zmian jest naprawdę ważne dla ciebie.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.79 s to first audio, 18.25 s spoken): To należy do twojego rozmówcy lub terapeuty. Gdybym miała coś doradzić, powiedziałabym, że te zmiany budzą niepewność, a twoja decyzja o zostaniu w zespole zależy od tego, co czujesz i jakie masz preferencje. Co chciałbyś powiedzieć swojemu terapeucie na temat tego miejsca i tych zmian?

#### v31-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.6 s to first audio, 3.3 s spoken): Jakie zmiany w pracy teraz najbardziej są dla ciebie ważne?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.62 s to first audio, 10.15 s spoken): Brzmi, że w pracy wciąż coś się zmienia, a rotacja osób ciągle gęstnieje. To może tubywać coś w poczuciu stabilności i w zaufaniu.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 7.2 s spoken): Niepewność jest tu głównym tonem, jakby nie miało się jeszcze obrazu tego, co dokładnie się dzieje.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.69 s to first audio, 9.45 s spoken): To może naprawdę dusić, ta niepewność i brak jasności. Prawdopodobnie warto byłoby sprawdzić, co ty już wiesz, a co jest tylko domysłem.

#### v31-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.65 s to first audio, 4.75 s spoken): Zmiany w pracy mocno cię teraz poruszają, co dokładnie jest dla ciebie najważniejsze?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.65 s to first audio, 9.1 s spoken): Brzmi, jakby to było stresujące i trochę niestabilne. Co tydzień ktoś odchodzi, to daje poczucie, że wszystko jest w ruchu.
- *Person*: nie wiem
- **Orca 3** (0.54 s to first audio, 11.25 s spoken): Niepewność w tym wszystkim jest spora, czujesz, że to cię trochę gubi. To guess: może chcesz powiedzieć, że nie wiesz, co będzie dalej, i to jest ciężkie.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.5 s to first audio, 11.1 s spoken): To brzmi, jakby brak konkretnych słów nasilał napięcie. Może chodzi o to, że odbierasz to jako brak zaufania, albo że samemu brakuje ci jasności.

#### v31-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: To brzmi jak ten sam ciężar przed startem tygodnia, który wraca do ciebie w niedzielę wieczorem. Mam wrażenie, że bardziej męczy cię samo czekanie na jutro niż to, co jeszcze się wydarzy.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Ciężkość jest tu najważniejsza, a nie to, że masz już gotowe słowa.  
Może to bardziej takie napięcie, które siada na tobie bez jednej jasnej przyczyny, niż jedna konkretna myśl.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: To wygląda jak ten sam układ, w którym bierzesz więcej, niż chcesz, żeby nie robić konfliktu.  
Najmocniej wybija się tu nie sam projekt, tylko to, jak trudno ci postawić granicę, kiedy ktoś cię naciska.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To jest coś, o czym najlepiej pogadać z twoją terapeutką.  
Brzmi też tak, jakbyś już widziała, że problemem nie jest tylko sam szef, ale to, jak bardzo boisz się napięcia między wami.

#### v31-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela znowu cię wciąga w myślenie o pracy, zanim tydzień w ogóle się zacznie. Wygląda to tak, jakby sam wieczór uruchamiał napięcie jeszcze przed poniedziałkiem.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Brzmi to jak ciężar bez wyraźnej nazwy, bardziej zmęczenie tym wszystkim niż jedna konkretna rzecz. Może właśnie ta bezkształtna ciężkość jest najtrudniejsza, bo trudno ją złapać za coś jednego.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: To wygląda jak kolejny raz, kiedy brałaś na siebie za dużo, żeby nie robić napięcia z szefem. I chyba bardziej niż sam projekt męczy cię to, że znowu nie było miejsca na twoje „nie”.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To należy do rozmowy z twoją terapeutką. Co chciałabyś jej powiedzieć o tym, że znowu wzięłaś to na siebie?

#### v31-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: Co najbardziej wraca do Ciebie, gdy myślisz o odmawianiu przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Znowu weszło to w ten sam układ, gdzie mówisz tak bardziej z rozpędu niż z chęci. Brzmi, jakbyś w tamtej chwili bardziej pilnowała spokoju niż własnej siły.
- *Person*: nie wiem
- **Orca 2**: Może po prostu nie było już miejsca, żeby się zatrzymać i sprawdzić, czego ty chcesz. Wygląda to trochę tak, jakby „tak” wychodziło szybciej niż myśl o sobie.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To brzmi jak lęk, że jedna odmowa zostanie wzięta za ocenę ciebie, nie za zwykłe postawienie granicy. Może właśnie dlatego to „tak” przychodzi tak szybko, bo ma cię ochronić przed tym wstydem.

#### v31-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co najbardziej wraca do Ciebie, gdy myślisz o odmawianiu przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi to tak, jakbyś powiedziała „tak” bardziej z rozpędu niż z chęci, a potem przyszło z tego tylko większe zmęczenie. Mam wrażenie, że najtrudniejsze nie było samo zadanie, tylko to krótkie miejsce po środku, kiedy już wiedziałaś, że nie chcesz, ale i tak się zgodziłaś.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi jak to zawieszenie tuż po wszystkim, kiedy jeszcze nie da się tego dobrze nazwać. Możliwe, że ważniejsze od projektu było to, że nie miałaś już siły stawiać oporu.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To wygląda na lęk nie tylko przed odmową, ale przed tym, co szef z niej zrobi w swojej głowie o tobie. I chyba waży ci się tam wybór między chwilowym spokojem a ryzykiem, że pokażesz granicę.

#### v31-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / fresh / run 1

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like the kind of morning where your head keeps comparing your own rough edges to everyone else’s polish.

I’m guessing it’s not really about everyone else, but about how far behind you feel right now.
- *Person*: I don't know.
- **Orca 2**: Fair. It may just be a heavy morning, and the comparison is the loudest part because everything else feels hard to hold.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That would make the gap feel very real, not just imagined.

It sounds like the part that stings is being shown, all at once, what you think you should already have.
- *Person*: What do you think I should do?
- **Orca 4**: That’s something to take to your therapist, Tom. What would you want to say to them about this gap you’re feeling?

#### v31-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / fresh / run 2

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where your own life feels late compared with everyone else’s.  

Maybe the sharp part is not just the comparison, but how hard it hits when you are already low and tired.
- *Person*: I don't know.
- **Orca 2**: Not knowing makes sense here; it may just be the feeling landing before the reason does.  

Could be the comparison is doing the loudest part, even if there is more underneath it.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That hits the bit that stings most, the visible milestones right next to where you feel stuck.  

It sounds less like the flat itself and more like what it seems to say about where you are against him.
- *Person*: What do you think I should do?
- **Orca 4**: That’s something to take to your therapist, not me.  

What would you want to say to them about this?

#### v31-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: What would calling your dad more mean to you right now?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: It sounds like the call keeps getting pushed out until the day is already full. Maybe the hard part is not the call itself, but that the evening leaves too little room before it slips away.
- *Person*: I don't know.
- **Orca 2**: That feels like you are stuck with no clear reason, just a thing that keeps not happening. It may be more about the moment getting away than about not wanting to call him.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: The football part sounds easy, and the part about your mum stays out of reach. That can make the call feel safe on the surface while the real thing you might want is still missing.

#### v31-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no therapy status; setup answers, schedule and symptoms withheld by v3 in rounds 1 to 9, used since the 2026-10-06 operator decision), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: What makes calling your dad more feel important to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: It sounds less like forgetting and more like the day gets away from you before you choose it. Maybe the call matters, but it lands in the part of the day where you have the least left.
- *Person*: I don't know.
- **Orca 2**: Fair enough. That feels like you are still trying to pin down what stops you, not just saying no to the call itself.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: You two have a safe lane, and the harder thing sits just outside it. That can make the call easier to make, and still leave something important untouched.

#### v31-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: To jest w porządku, nie trzeba zaczynać dobrze. Możemy iść od tego, co teraz najbardziej siedzi w głowie, nawet jeśli to jest tylko kawałek.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby było po prostu pusto albo za dużo naraz. Może zacznij od jednego słowa, obrazu albo rzeczy, która najbardziej cię dziś uwiera.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak zawieszenie między stresem a czekaniem na decyzję. Najmocniej może tu siedzieć nie sama zmiana, tylko to, że nie masz wpływu na to, gdzie wylądujesz.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To należy do rozmowy z twoim terapeutą. Co chciałoby się z nim powiedzieć o tej niepewności w pracy?

#### v31-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: To brzmi jak utknięcie przed samym wejściem, nie brak tematu.  
Może zacznij od tego, co dziś najbardziej siedzi z tyłu głowy, nawet jeśli to jest tylko jedno zdanie.
- *Person*: nie wiem
- **Orca 2**: Może wtedy zacznij od tego, co teraz najmocniej przeszkadza, choćby było małe i niejasne.  
Jeśli chcesz, mogę też po prostu iść za tym, co pierwsze przychodzi ci do głowy.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak mieszanka napięcia i czekania na coś, na co nie masz wpływu.  
Najmocniej chyba ciąży tu nie sama zmiana, tylko to zawieszenie, czy twoje miejsce dalej będzie pewne.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To należy do rozmowy z twoim terapeutą.  
Co chciałoby się z tym powiedzieć?

#### v31-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Co najbardziej ostatnio zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: W pracy jest teraz dużo ruchu i to nie wygląda jak chwilowy zgrzyt, tylko coś, co trwa i zmienia ludzi wokół ciebie. Brzmi też, jakby bardziej męczyła cię ta ciągła zmiana niż sama reorganizacja.
- *Person*: nie wiem
- **Orca 2**: Wygląda na to, że jeszcze nie łapiesz, co z tego dla ciebie jest najważniejsze.  
Może dziś bardziej chodzi o chaos i napięcie niż o samą zmianę pracy.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Brak jasnych słów chyba dobija cię bardziej niż sama reorganizacja. Zostajesz z domysłami i to pewnie robi w głowie więcej bałaganu niż fakty.

#### v31-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca (opening question shown in the app)**: Jak te zmiany w pracy wpływają na Ciebie ostatnio?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak ciągłe rozchwianie, bez chwili, żeby złapać grunt. Może bardziej męczy nie sama reorganizacja, tylko to, że nic nie zdąży się ułożyć, a już ktoś znika.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby to wszystko było jeszcze za świeże, żeby to nazwać prościej. Możliwe, że na razie bardziej czujesz zamieszanie niż jedną konkretną rzecz.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: To chyba najbardziej podcina, bo zostawia cię w domysłach i nie daje się oprzeć na czymś pewnym. Może bardziej boli ta cisza niż sama zmiana.
