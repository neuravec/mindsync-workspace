2 conversations, estimated cost USD 0.04 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| smoke-v3-mini | gpt-realtime-mini | none | fresh | 1 | 0/1 | 1/1 | 1/1 | n/a | n/a | 0/1 | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 | 1.00 | 2.4 | 0.58 | 0.70 | 8.9 | 246 | 68/177/0 | 0 | 0 | 0 | 0.0304 |
| smoke-v3-text | gpt-5.4-mini | none | fresh | 1 | n/a | n/a | n/a | n/a | n/a | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0.25 | 2.2 | n/a | n/a | n/a | 61 | n/a | 0 | 0 | 0 | 0.0052 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| smoke-v3-mini | R1 | fresh | 1 | FAIL | pass | pass | n/a | n/a | FAIL | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | chciałabyś, czułaś, jakbyś czuła | none | none |
| smoke-v3-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | Jakbyś już była, chciałabyś, chciałaś, wzięłaś, zgodziłaś | none | none |

### Transcripts

#### smoke-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.7 s to first audio, 4.1 s spoken): Cześć Ania, cieszę się, że jesteś. Jak się czujesz dzisiaj?
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.51 s to first audio, 9.95 s spoken): Brzmi, jakby ta myśl o jutrze pojawiała się zanim jeszcze zacznie się dzień. Myślisz, że chodzi o konkretne zadania, które cię czekają? Albo o to, jak się w to wszystko wpasowuje?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.61 s to first audio, 9.4 s spoken): Rozumiem, to brzmi, jakby cię to zaskakiwało i czułaś, że jest to przytłaczające od samego początku. Czy może to jest związane z tym, co się dzieje jutro u ciebie w pracy?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.53 s to first audio, 9.8 s spoken): To brzmi, jakbyś czuła się przytłoczona tym, że nie udało się od razu postawić granicy. Może to jest coś, na czym chciałabyś się skupić, żeby lepiej poradzić sobie następnym razem?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.53 s to first audio, 11.05 s spoken): To, co myślę, to że warto zastanowić się, co dokładnie chcesz przekazać. Możesz powoli sprecyzować, co cię obciąża, i dać sobie prawo do priorytetyzowania. Jak ci się wydaje?

#### smoke-v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela u ciebie znowu robi się ciężka, zanim tydzień w ogóle się zacznie. Brzmi to tak, jakby sam poniedziałek nie był jeszcze problemem, a bardziej to, co twoja głowa już do niego dokleja. Jeśli chcesz, mogę też powiedzieć, co widzę w tym powtarzającym się układzie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi bardziej jak ciężar niż jedna konkretna myśl. Jakbyś już była zmęczona samym czekaniem na to, co jutro przyniesie.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Czyli nie chodzi tylko o jutro, ale też o to, że znowu wzięłaś na siebie coś, czego nie chciałaś. Myślę, że najbardziej boli tu chyba nie sam projekt, tylko to, że zgodziłaś się wbrew sobie i teraz musisz to nieść przez cały weekend.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To już najlepiej omówić z twoją terapeutką. Co chciałabyś jej powiedzieć o tym szefie i o tym, jak trudno ci odmówić?
