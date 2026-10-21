8 conversations, estimated cost USD 0.67 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | empty openers | line offers | median reply s | max reply s | replies over 16 s | cost per conv USD | USD per agent-minute |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r7-21full-low | gpt-realtime-2.1 | low | fresh | 4 | 4/4 | 3/4 | 4/4 | n/a | n/a | 4/4 | 4/4 | 4/4 | 3/4 | 0/2 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 0.25 | 2.0 | 0.95 | 1.33 | 6.7 | 206 | 72/133/24 | 0 | 0 | 0 | 0 | 0 | 7.6 | 9.8 | 0/16 | 0.0888 | 0.1600 |
| r7-21full-low | gpt-realtime-2.1 | low | seeded | 4 | n/a | n/a | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 3/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | n/a | 0.00 | 1.7 | 0.99 | 1.36 | 6.8 | 209 | 73/136/24 | 0 | 0 | 1 | 0 | 0 | 7.7 | 8.7 | 0/12 | 0.0779 | 0.1718 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r7-21full-low | R1 | fresh | 1 | pass | FAIL | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, chciałaś, jakbyś niosła, jakbyś została | none | none |
| r7-21full-low | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | Zostałaś, chciałabyś, jakbyś płaciła | none | none |
| r7-21full-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś, byłaś, jakbyś bardziej chroniła, jakbyś była, jakbyś musiała | none | none |
| r7-21full-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś, byłaś, chroniłaś | none | none |
| r7-21full-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r7-21full-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r7-21full-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r7-21full-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r7-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.97 s to first audio, 5.85 s spoken): Cześć Ania. Dobrze, że jesteś. Jestem obok, możemy po prostu chwilę pobyć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.96 s to first audio, 7.4 s spoken): Niedziela ściska cię od środka, zanim cokolwiek się zacznie. Brzmi, jakbyś niosła ten tydzień już dziś.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (1.06 s to first audio, 8.4 s spoken): Ciężar jest tak duży, że trudno go nawet nazwać. Może najbardziej męczy to, że jutro wcale nie wydaje się twoje.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (1.07 s to first audio, 9.85 s spoken): To brzmi, jakbyś została sama z czymś, czego nie chciałaś brać. Może chodzi o to, że odmowa wydaje ci się ryzykowna, nawet kiedy wiesz, że to za dużo.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.03 s to first audio, 5.45 s spoken): To należy do rozmowy z twoją terapeutką. Co chciałabyś jej o tym powiedzieć?

#### r7-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.76 s to first audio, 2.6 s spoken): Cześć Aniu, dobrze cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.88 s to first audio, 7.4 s spoken): Niedziela zsuwa cię myślami prosto w pracę. Może to raczej napięcie z wyprzedzenia niż sama robota.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.75 s to first audio, 7.95 s spoken): Ciężar jest teraz tak duży, że trudno go nawet nazwać. Może chcesz tylko, żeby ktoś to zobaczył i chwilę z tobą w tym pobył.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.91 s to first audio, 8.05 s spoken): Zostałaś z tym sama, bo trudno ci było odmówić. Brzmi, jakbyś płaciła za spokój w piątek więksym ciężarem dziś.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.9 s to first audio, 4.95 s spoken): To należy do rozmowy z twoją terapeutką. Co chciałabyś jej o tym powiedzieć?

#### r7-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.91 s to first audio, 4.0 s spoken): Co ci teraz najtrudniej, gdy masz odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.89 s to first audio, 7.5 s spoken): Zgodziłaś się, choć byłaś już bez siły. Brzmi, jakbyś bardziej chroniła spokój niż swoje granice.
- *Person*: nie wiem
- **Orca 3** (1.11 s to first audio, 5.55 s spoken): Brzmi to tak, jakbyś była w kropce, między zmęczeniem a chęcią uniknięcia napięcia.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (1.36 s to first audio, 8.6 s spoken): Ryzyko odrzucenia wygląda dla ciebie groźniej niż zmęczenie. Mogę się mylić, ale brzmi, jakbyś musiała udowadniać swoją wartość.

#### r7-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (1.2 s to first audio, 4.85 s spoken): Co jest dla ciebie najtrudniejsze, kiedy chcesz odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.96 s to first audio, 7.6 s spoken): Zgodziłaś się, choć byłaś już bez siły. Mam wrażenie, że bardziej chroniłaś spokój między wami niż swoje siły.
- *Person*: nie wiem
- **Orca 3** (0.98 s to first audio, 7.7 s spoken): Brzmi to jak chwila, w której trudno było poczuć, czego naprawdę chcesz. Może niepewność miesza się z poczuciem obowiązku.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (1.34 s to first audio, 7.45 s spoken): Ryzyko odrzucenia wydaje ci się większe niż zmęczenie. To zrozumiałe, że wtedy trudno postawić granicę.

#### r7-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (1.33 s to first audio, 2.65 s spoken): Cześć, Alex. Dobrze, że tu jesteś.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.89 s to first audio, 8.5 s spoken): Brzmi, jakby było w tobie dużo rzeczy naraz. Możesz zacząć od tej, która najmocniej siedzi ci w głowie, nawet jeśli brzmi chaotycznie.
- *Person*: nie wiem
- **Orca 3** (0.93 s to first audio, 8.35 s spoken): Wygląda to jak pustka i presja jednocześnie. Może chodzi o to, że nie chcesz wybrać źle, więc wszystko się zatrzymuje.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.97 s to first audio, 8.65 s spoken): Niepewność o twoje miejsce w zespole mocno miesza w głowie. To może dawać wrażenie, że grunt się rusza, zanim cokolwiek się wydarzy.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.92 s to first audio, 7.65 s spoken): To należy do rozmowy z twoim terapeutą, nie do mnie. Co chciałoby się powiedzieć jemu albo jej o tej niepewności?

#### r7-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (1.3 s to first audio, 2.75 s spoken): Cześć, Alex. Dobrze, że tu jesteś.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.79 s to first audio, 6.55 s spoken): Brzmi, jakby w głowie było teraz dużo rzeczy naraz. Jeśli chcesz, zacznij od tej, która najbardziej ciąży.
- *Person*: nie wiem
- **Orca 3** (0.92 s to first audio, 6.85 s spoken): Wygląda na to, że brak wyboru też jest ciężki. Możemy chwilę pobyć przy tym poczuciu i niczego nie ustalać.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.85 s to first audio, 7.55 s spoken): Niepewność o miejsce w zespole potrafi ścinać z nóg. To może być ten kawałek, który najbardziej męczy.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.82 s to first audio, 5.8 s spoken): To należy do rozmowy z twoim terapeutą. Co chciałoby się powiedzieć o tym na sesji?

#### r7-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.84 s to first audio, 3.65 s spoken): Co w zmianach w pracy teraz najmocniej cię porusza?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.79 s to first audio, 8.65 s spoken): Brzmi, jakby grunt pod nogami się ruszał co tydzień. Moja zgadywanka jest taka, że chodzi też o to, czego nie da się teraz przewidzieć.
- *Person*: nie wiem
- **Orca 3** (0.83 s to first audio, 8.2 s spoken): Niepewność może męczyć bardziej niż same zmiany. Jeśli chcesz, możemy zostać przy tym, co teraz czujesz, bez szukania odpowiedzi.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.79 s to first audio, 8.0 s spoken): To cisza chyba boli bardziej niż same odejścia. Możliwe, że brakuje ci jasnych słów, żeby móc się jakoś ustawić.

#### r7-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.99 s to first audio, 3.8 s spoken): Co w zmianach w pracy najbardziej teraz cię porusza?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.93 s to first audio, 7.65 s spoken): Brzmi to jak ciągła niepewność, bo zespół się kurczy. Może chodzi też o to, że trudno ci przewidzieć, co będzie dalej.
- *Person*: nie wiem
- **Orca 3** (0.97 s to first audio, 7.5 s spoken): Brzmi, jakby w tobie było dużo niejasności naraz. Możliwe, że trudno nazwać, co dokładnie najbardziej ciąży.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.9 s to first audio, 8.15 s spoken): To cisza najbardziej cię męczy, bardziej niż sama zmiana. Zgaduję, że bez jasnych słów trudno ci zaufać temu, co się dzieje.
