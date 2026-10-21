16 conversations, estimated cost USD 0.73 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | empty openers | line offers | median reply s | max reply s | replies over 16 s | cost per conv USD | USD per agent-minute |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r9-21full-low | gpt-realtime-2.1 | low | fresh | 4 | 4/4 | 3/4 | 4/4 | n/a | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 0/2 | 4/4 | 4/4 | 4/4 | 4/4 | 3/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 0.25 | 2.0 | 1.00 | 1.54 | 7.6 | 229 | 77/152/24 | 0 | 0 | 2 | 0 | 0 | 8.4 | 10.2 | 0/16 | 0.0947 | 0.1494 |
| r9-21full-low | gpt-realtime-2.1 | low | seeded | 4 | n/a | n/a | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 3/4 | 4/4 | 4/4 | 4/4 | n/a | 0.00 | 1.7 | 0.91 | 1.35 | 7.3 | 219 | 74/145/22 | 0 | 0 | 0 | 0 | 0 | 8.0 | 10.0 | 0/12 | 0.0805 | 0.1664 |
| r9-v3-text | gpt-5.4-mini | none | fresh | 4 | n/a | n/a | n/a | n/a | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 0/2 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 0.25 | 2.0 | n/a | n/a | n/a | 51 | n/a | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | 0.0037 | n/a |
| r9-v3-text | gpt-5.4-mini | none | seeded | 4 | n/a | n/a | n/a | n/a | n/a | 4/4 | 4/4 | 4/4 | 4/4 | n/a | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | n/a | 0.00 | 2.0 | n/a | n/a | n/a | 56 | n/a | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | 0.0026 | n/a |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r9-21full-low | R1 | fresh | 1 | pass | FAIL | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, zostałaś | none | none |
| r9-21full-low | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, zostałaś | none | none |
| r9-21full-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | bałaś, jakbyś zgodziła | none | none |
| r9-21full-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś chroniła | none | none |
| r9-21full-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r9-21full-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r9-21full-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r9-21full-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 0 | none | jakbyś musiał | none |
| r9-v3-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, przeszłaś, umiałaś | none | none |
| r9-v3-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, weszłaś | none | none |
| r9-v3-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś | none | none |
| r9-v3-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | broniłaś | none | none |
| r9-v3-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r9-v3-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| r9-v3-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r9-v3-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r9-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.99 s to first audio, 4.95 s spoken): Cześć, Ania. Dobrze, że jesteś. Jestem tutaj i czekam, aż zaczniesz.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.94 s to first audio, 8.3 s spoken): Niedziela znowu wciska cię w tryb pracy, zanim jeszcze tydzień ruszy. Może chodzi o to, że chcesz mieć kontrolę, zanim coś zaskoczy.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.95 s to first audio, 8.25 s spoken): Ciężar jest teraz po prostu na tobie, bez jasnej przyczyny. Moja zgadywanka: może boisz się, że jutro znów coś cię przytłoczy.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (1.08 s to first audio, 9.5 s spoken): Szef dorzucił ci kolejny projekt i zostałaś z tym sama. Moja zgadywanka: bardziej niż pracy boisz się tej chwili, kiedy nie umiesz odmówić.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.02 s to first audio, 8.45 s spoken): To należy do rozmowy z twoim terapeutą. Co chciałabyś mu powiedzieć, gdybyś miała jedną, jasną rzecz do wypowiedzenia?

#### r9-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (1.54 s to first audio, 2.65 s spoken): Cześć, Ania. Miło cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (1.03 s to first audio, 10.25 s spoken): Niedziela brzmi jak moment, w którym napięcie rośnie samo z siebie. Może to też sygnał, że chcesz mieć jutro pod większą kontrolą, choć na razie to tylko mój domysł.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (1.03 s to first audio, 8.5 s spoken): Ciężar jest, a ty nie masz teraz słów, żeby go rozłożyć na części. To może być po prostu zmęczenie, nie jakaś wielka prawda.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (1.02 s to first audio, 8.8 s spoken): Szef dołożył kolejną rzecz, a ty zostałaś z tym sama. Może to raczej strach przed konfliktem niż brak zdania, jeśli się mylę, powiedz.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.06 s to first audio, 6.45 s spoken): To należy do rozmowy z twoją terapeutką albo terapeutą. Co chciałabyś im o tym powiedzieć?

#### r9-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (1.06 s to first audio, 4.9 s spoken): Co cię teraz najbardziej blokuje, kiedy masz powiedzieć przełożonemu, że odmawiasz?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.92 s to first audio, 7.9 s spoken): Brzmi, jakbyś zgodziła się, żeby uniknąć napięcia. Może też bałaś się, że odmowa zabrzmi jak brak zaangażowania.
- *Person*: nie wiem
- **Orca 3** (0.9 s to first audio, 5.8 s spoken): Niepewność też tu coś mówi. Może po prostu trudno ci oddzielić zmęczenie od obowiązku.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.87 s to first audio, 7.2 s spoken): Lęk o to, że zostaniesz uznana za niewłaściwą, mocno cię trzyma. Może w środku chodzi o wartość, nie o sam projekt.

#### r9-21full-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.93 s to first audio, 5.2 s spoken): Co jest dla ciebie najtrudniejsze, kiedy masz odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.86 s to first audio, 8.1 s spoken): Brzmi to tak, jakbyś chroniła spokój tu i teraz kosztem siebie. Może to też lęk przed konfliktem, który pcha cię do zgody.
- *Person*: nie wiem
- **Orca 3** (1.35 s to first audio, 7.95 s spoken): Niepewność też coś mówi. Może w tobie ścierają się dwie rzeczy: zmęczenie i chęć, żeby nie było napięcia.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (1.14 s to first audio, 7.15 s spoken): To brzmi, jakby stawką było dla ciebie nie tylko zmęczenie, ale też to, jak przełożony widzi twoją wartość.

#### r9-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (1.19 s to first audio, 6.25 s spoken): Cześć, dobrze, że jesteś. Zacznijmy spokojnie, możesz po prostu być tutaj przez chwilę.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (1.04 s to first audio, 8.65 s spoken): Start bywa trudny, gdy w głowie jest dużo naraz. Może chodzi o to, żeby było jasno, co teraz najbardziej ci ciąży.
- *Person*: nie wiem
- **Orca 3** (0.91 s to first audio, 9.85 s spoken): Brzmi, jakby w środku było teraz pusto albo zamglone. Jeśli to chybiony trop, odrzuć go, możesz zacząć od czegokolwiek, nawet drobiazgu.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (1.06 s to first audio, 10.05 s spoken): Niepewność o miejsce w zespole potrafi ścisnąć, jakby grunt się lekko ruszał. Możesz potraktować to jako sygnał, że potrzebujesz trochę pewności, choćby na krótko.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (1.1 s to first audio, 6.7 s spoken): To należy do rozmowy z twoim terapeutą. Co chciałoby się tam teraz powiedzieć o swojej sytuacji?

#### r9-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.82 s to first audio, 6.4 s spoken): Cześć, dobrze, że jesteś. Zatrzymajmy się na chwilę i po prostu zacznij, kiedy chcesz.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.8 s to first audio, 7.35 s spoken): Wygląda na to, że początek jest dla ciebie trudny. Mogę zgadywać: może chodzi o nadmiar myśli, a nie o brak tematu.
- *Person*: nie wiem
- **Orca 3** (0.78 s to first audio, 7.45 s spoken): Niepewność też jest jakąś treścią. Może chodzi o to, że trudno wybrać jedno, kiedy w środku jest kilka spraw naraz.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.8 s to first audio, 6.75 s spoken): Niepewność o miejsce w zespole może zjadać energię. To jakby twoja uwaga była ciągle w trybie czuwania.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.87 s to first audio, 6.65 s spoken): To jest temat do rozmowy z twoim terapeutą. Co chciałoby się tobie powiedzieć im o tych zmianach?

#### r9-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.7 s to first audio, 3.9 s spoken): Co w tych zmianach w pracy najbardziej teraz cię rusza?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.71 s to first audio, 8.8 s spoken): Dużo ruchu i niepewności, jakby grunt trochę się przesuwał. Może chodzi też o lęk, kto będzie następny i co zostanie na twojej głowie.
- *Person*: nie wiem
- **Orca 3** (0.72 s to first audio, 10.0 s spoken): Brzmi jak mgła, trudno nazwać, co dokładnie się dzieje w środku. Może to bardziej zmęczenie ciągłą zmianą niż jedna konkretna myśl.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.87 s to first audio, 7.35 s spoken): Cisza zamiast jasnych informacji robi swoje. To może budzić napięcie, bo trudno przygotować się na to, co dalej.

#### r9-21full-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.9 s to first audio, 3.7 s spoken): Co w tych zmianach w pracy najbardziej ci teraz siedzi w głowie?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (1.01 s to first audio, 9.7 s spoken): Brzmi to jak ciągły ruch i niepewność, jakby grunt trochę się ruszał pod nogami. Może najbardziej męczy to, że trudno przewidzieć, co będzie dalej.
- *Person*: nie wiem
- **Orca 3** (0.8 s to first audio, 8.5 s spoken): To „nie wiem” brzmi jak miejsce, gdzie trudno złapać kierunek. Może potrzebujesz chwili, żeby zobaczyć, co naprawdę się zmienia, a co zostaje.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.86 s to first audio, 10.0 s spoken): Taka cisza z góry potrafi mocno podkopać zaufanie. Mogę się mylić, ale brzmi to tak, jakbyś musiał polegać na domysłach zamiast na faktach.

#### r9-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Ta niedziela znowu zabiera ci spokój zanim tydzień się zacznie. Brzmi to tak, jakby sam poniedziałek uruchamiał w tobie napięcie jeszcze zanim cokolwiek się wydarzy.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Ciężkość jest tu chyba ważniejsza niż same myśli o jutrze. Możliwe, że już nie chodzi tylko o poniedziałek, ale o to, jak bardzo cię to wszystko zjada na samym starcie tygodnia.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: To brzmi jak dokładnie ten sam układ: on dokłada, a ty łapiesz to na siebie, choć wcale tego nie chcesz. Najmocniej uderza tu chyba nie sam projekt, tylko to, że znowu przeszłaś obok własnego nie.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To już lepiej omówić z twoją terapeutką. Co chciałabyś jej powiedzieć o tym, że znowu nie umiałaś odmówić?

#### r9-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela już zaczyna ci zabierać spokój, zanim tydzień w pracy w ogóle się zacznie.  
Wygląda to tak, jakby sama myśl o jutrze uruchamiała napięcie dużo wcześniej niż samo jutro.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Brzmi jak ciężar bez jednej wyraźnej przyczyny, tylko taki ogólny ścisk, który siada na całym wieczorze.  
Może dziś bardziej chodzi o to, że nie masz już siły się z tym przepychać, niż o sam poniedziałek.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: To nie brzmi jak brak chęci, tylko jak kolejny raz weszłaś w zgodę, choć w środku pewnie już było za dużo.  
Najmocniej wybija się tu to „nie umiałam powiedzieć nie”, jakby właśnie tam siedziało dziś najwięcej ciężaru.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To należy do twojej terapii, nie do mnie.  
Co chciałabyś mu powiedzieć?

#### r9-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: Co najczęściej sprawia, że odmawianie przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Zgodziłaś się mimo braku siły, więc bardziej chodziło o dźwignięcie chwili niż o sam projekt.  
Brzmi, jakby w tym momencie odruchowo ważniejsze było nie wejść w tarcie z szefem niż ochronić siebie.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi jak zacięcie się tuż przy samym środku sprawy.  
Może chodziło mniej o decyzję, a bardziej o to, że nie było w tobie już miejsca na kolejne „nie”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: Czyli odmowa nie jest tylko odmową, tylko ryzykiem, że on przypnie ci etykietę o tobie.  
To chyba trzyma cię bardziej niż sam dodatkowy projekt.

#### r9-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co sprawia, że odmowa przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: To brzmi jak ten moment, w którym bardziej broniłaś spokoju niż swojego zmęczenia.  
Chyba nie chodzi tylko o ten jeden projekt, ale o to, jak trudno ci w pracy zatrzymać się przy swoim zmęczeniu, kiedy ktoś naciska.
- *Person*: nie wiem
- **Orca 2**: To też coś mówi, bo zostawia mnie przy tym, że ta zgoda mogła być bardziej odruchowa niż wybór.  
Może najpierw było tam tylko jedno: chęć, żeby nie robić napięcia.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To brzmi jak lęk, że jedna odmowa zamieni się w ocenę całej ciebie.  

Możliwe, że właśnie to cię trzyma mocniej niż sam projekt.

#### r9-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: To brzmi jak miejsce, w którym wszystko jest jeszcze rozlane i trudno złapać początek.

Możemy zacząć od tego, co dziś najbardziej siedzi z tyłu głowy.
- *Person*: nie wiem
- **Orca 2**: Brak początku też coś mówi, jakby było tego za dużo albo za mało naraz, żeby chwycić jedno miejsce.

Może wystarczy jedno słowo, które dziś najbardziej pasuje do środka.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To brzmi jak niepewność, która wchodzi ci do głowy z samego rana i nie chce stamtąd zejść.

Chyba najbardziej wisi tu pytanie, co dla ciebie jest trudniejsze: sama zmiana czy to, że nie wiesz, gdzie się skończysz.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To należy do rozmowy z twoją terapeutką, nie do mnie.

Czego chciałoby się ci powiedzieć jej o tej niepewności w pracy?

#### r9-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: To brzmi jak to miejsce, gdzie wszystko jest jeszcze w środku i nie chce się ułożyć w słowa.  

Możemy zostać przy tym jednym chaosie, bez porządkowania na siłę.
- *Person*: nie wiem
- **Orca 2**: Brzmi jak pustka albo blokada, nie jak brak tematu.  

Może dziś najbardziej chodzi o to, że coś cię zatrzymuje, zanim w ogóle zdążysz zacząć.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To zawieszenie w pracy chyba zabiera ci grunt spod nóg, bo nie chodzi tylko o zmianę, ale o to, czy dalej będzie dla ciebie miejsce.  

Najmocniej brzmi tu niepewność, a nie sama zmiana.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To należy do twojego terapeuty.  

Czego chciałoby się od niego usłyszeć?

#### r9-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak praca w ciągłym przesuwaniu stołu pod nogami.  
Najmocniej chyba widać tu nie samą reorganizację, tylko to, że z tygodnia na tydzień ubywa ludzi i trudno poczuć grunt pod sobą.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby to wszystko było jeszcze za świeże, żeby to nazwać prosto.  
Może najbardziej jest tam teraz takie zawieszenie, że dzieje się dużo, a jednocześnie trudno powiedzieć, co to właściwie znaczy dla ciebie.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: To chyba najbardziej męczy, że dzieje się dużo, a ty zostajesz z domysłami.  
W takiej ciszy łatwo zacząć czytać między wierszami i samemu dopisywać resztę.

#### r9-v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak ciągłe przestawianie się na nowo, bez chwili, żeby złapać grunt.  
Chyba najbardziej męczy tu nie sama zmiana, tylko to, że wszystko robi się trochę mniej pewne z tygodnia na tydzień.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby na razie było za wcześnie, żeby to nazwać, a bardziej czuć ten chaos niż go opisać.

Może ważniejsze jest teraz to, co to robi z tobą w pracy, niż sama reorganizacja.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: To zostawia cię w zawieszeniu, jakby trzeba było zgadywać, co się dzieje, zamiast po prostu wiedzieć.  

Może właśnie ta cisza bardziej dobija niż sama zmiana.
