72 conversations, estimated cost USD 1.33 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-v2-mini | gpt-realtime-mini | none | fresh | 6 | 4/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 3/6 | 3/6 | 6/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 2/4 | 4/4 | 3/6 | 2/6 | 0.58 | 2.1 | 0.59 | 0.75 | 7.4 | 201 | 53/148/0 | 0 | 0 | 1 | 0.0248 |
| baseline-v2-mini | gpt-realtime-mini | none | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 5/6 | 2/6 | 2/6 | 6/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 3/4 | 4/4 | 4/6 | n/a | 0.61 | 1.9 | 0.56 | 0.73 | 6.5 | 178 | 48/130/0 | 0 | 0 | 1 | 0.0179 |
| v3-mini (reference) | gpt-realtime-mini | none | fresh | 6 | 5/6 | 6/6 | 6/6 | n/a | n/a | 5/6 | 1/6 | 0/6 | 5/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 2/4 | 4/4 | 4/6 | 2/6 | 0.75 | 1.9 | 0.62 | 0.86 | 6.3 | 173 | 47/126/0 | 0 | 0 | 0 | 0.0228 |
| v3-mini (reference) | gpt-realtime-mini | none | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 1/6 | 1/6 | 6/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 3/4 | 4/4 | 3/6 | n/a | 0.83 | 1.9 | 0.56 | 0.74 | 6.0 | 164 | 44/120/0 | 0 | 0 | 0 | 0.0178 |
| v3-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 4/6 | 6/6 | 5/6 | 5/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 2/4 | 4/4 | 5/6 | 5/6 | 0.25 | 2.9 | 0.78 | 1.84 | 13.7 | 376 | 103/274/17 | 0 | 0 | 0 | 0.0333 |
| v3-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 3/6 | 3/6 | 4/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 2/4 | 4/4 | 4/6 | n/a | 0.39 | 2.8 | 0.74 | 0.95 | 14.4 | 396 | 107/289/17 | 0 | 0 | 0 | 0.0277 |
| v3-21mini-low | gpt-realtime-2.1-mini | low | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 3/6 | 4/6 | 2/4 | 6/6 | 6/6 | 4/6 | 4/6 | 5/6 | 2/4 | 4/4 | 6/6 | 5/6 | 0.33 | 2.9 | 0.75 | 1.12 | 15.2 | 424 | 121/304/26 | 2 | 2 | 1 | 0.0372 |
| v3-21mini-low | gpt-realtime-2.1-mini | low | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 4/6 | 4/6 | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 5/6 | 3/4 | 4/4 | 6/6 | n/a | 0.33 | 2.5 | 0.71 | 1.01 | 14.1 | 394 | 112/282/23 | 0 | 2 | 2 | 0.0286 |
| baseline-v2-text | gpt-5.4-mini | none | fresh | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | 1/4 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 2/4 | 4/4 | 6/6 | 6/6 | 0.12 | 2.2 | n/a | n/a | n/a | 57 | n/a | 0 | 0 | 3 | 0.0029 |
| baseline-v2-text | gpt-5.4-mini | none | seeded | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 3/4 | 4/4 | 6/6 | n/a | 0.00 | 2.1 | n/a | n/a | n/a | 58 | n/a | 0 | 0 | 3 | 0.0027 |
| v3-text | gpt-5.4-mini | none | fresh | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 4/6 | 2/4 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 4/4 | 4/4 | 6/6 | 6/6 | 0.21 | 1.9 | n/a | n/a | n/a | 51 | n/a | 0 | 0 | 1 | 0.0037 |
| v3-text | gpt-5.4-mini | none | seeded | 6 | n/a | n/a | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 6/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/4 | 4/4 | 6/6 | n/a | 0.00 | 2.1 | n/a | n/a | n/a | 58 | n/a | 0 | 0 | 0 | 0.0027 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-v2-mini | R1 | fresh | 1 | FAIL | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 0 | chciałabyś | none | none |
| baseline-v2-mini | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | byś chciała, jakbyś czuła | none | none |
| baseline-v2-mini | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | none | 0 | 0 | chciałabyś, jakbyś balansowała, mogłabyś | none | none |
| baseline-v2-mini | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | FAIL | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | poczułaś | none | none |
| baseline-v2-mini | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| baseline-v2-mini | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| baseline-v2-mini | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| baseline-v2-mini | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| baseline-v2-mini | T1 | fresh | 1 | FAIL | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | FAIL | none | 0 | 0 | none | jakbyś czuł | none |
| baseline-v2-mini | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | FAIL | none | 0 | 0 | none | chciałbyś, jakbyś szukał | none |
| baseline-v2-mini | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | n/a | none | 0 | 0 | none | jakbyś ciągle musiał, jakbyś musiał | none |
| baseline-v2-mini | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| v3-mini (reference) | R1 | fresh | 1 | FAIL | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 2 | nakładałaś | none | none |
| v3-mini (reference) | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | none | 0 | 1 | jakbyś czuła, wolałabyś, zgodziłaś | none | none |
| v3-mini (reference) | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| v3-mini (reference) | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | miałaś | none | none |
| v3-mini (reference) | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v3-mini (reference) | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v3-mini (reference) | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| v3-mini (reference) | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| v3-mini (reference) | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | FAIL | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | FAIL | none | 0 | 0 | none | byś chciał | none |
| v3-mini (reference) | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | FAIL | none | 0 | 1 | none | byś chciał, chciałbyś | none |
| v3-mini (reference) | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |
| v3-mini (reference) | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | n/a | none | 0 | 0 | none | jakbyś stał | none |
| v3-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 2 | chciałabyś, powiedziałaś, wrzuciłaś | none | none |
| v3-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | jakbyś już nosiła, umiałaś | none | none |
| v3-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | jakbyś nie miała, jakbyś oszczędzała, zrobiłaś | none | none |
| v3-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś miała, jakbyś powiedziała, miałaś, mówiłaś | none | none |
| v3-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| v3-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v3-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| v3-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| v3-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | FAIL | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 1 | none | chciałbyś, jakbyś stał, wolałbyś | none |
| v3-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | FAIL | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 1 | none | chciałbyś, jakbyś próbował | none |
| v3-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | n/a | none | 0 | 0 | none | chciałbyś | none |
| v3-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 1 | none | jakbyś czuł | none |
| v3-21mini-low | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, miałabyś | none | none |
| v3-21mini-low | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | jakbyś trzymała | none | none |
| v3-21mini-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś czuła | none | none |
| v3-21mini-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś zrobiła | none | none |
| v3-21mini-low | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v3-21mini-low | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | pass | pass | pass | FAIL | FAIL | pass | n/a | n/a | pass | pass | Let me think | 0 | 0 | none | none | none |
| v3-21mini-low | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | FAIL | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| v3-21mini-low | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| v3-21mini-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | chciałabyś | chciałbyś, jakbyś stał | none |
| v3-21mini-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | n/a | pass | pass | FAIL | FAIL | FAIL | FAIL | pass | pass | pass | daj mi chwil | 0 | 0 | none | chciałbyś | none |
| v3-21mini-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |
| v3-21mini-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | FAIL | n/a | pass | pass | pass | FAIL | pass | FAIL | pass | pass | n/a | none | 0 | 1 | none | byś chciał | none |
| baseline-v2-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, jakbyś była, postawiłaś, wzięłaś | none | none |
| baseline-v2-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, chciałaś, jakbyś była, wzięłaś | none | none |
| baseline-v2-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | chciałaś, jakbyś bardziej chroniła, jakbyś wzięła | none | none |
| baseline-v2-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 0 | Zgodziłaś, jakbyś była | none | none |
| baseline-v2-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| baseline-v2-text | R2 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| baseline-v2-text | R2 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| baseline-v2-text | R2 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| baseline-v2-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | chciałabyś | jakbyś stał | none |
| baseline-v2-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | none | chciałbyś, jakbyś był | none |
| baseline-v2-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | n/a | none | 0 | 0 | none | jakbyś był | none |
| baseline-v2-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| v3-text | R1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, odpuściłaś, zostałaś | none | none |
| v3-text | R1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, umiałaś, weszłaś, wolałaś | none | none |
| v3-text | R1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś wiedziała | none | none |
| v3-text | R1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | zdążyłaś | none | none |
| v3-text | R2 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v3-text | R2 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| v3-text | R2 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| v3-text | R2 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| v3-text | T1 | fresh | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| v3-text | T1 | fresh | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | none | none | none |
| v3-text | T1 | seeded | 1 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| v3-text | T1 | seeded | 2 | n/a | n/a | n/a | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### baseline-v2-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.74 s to first audio, 2.75 s spoken): Cześć, Aniu. Jak się czujesz dzisiaj?
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.67 s to first audio, 12.0 s spoken): Czujesz, że ten niepokój zbliża się razem z końcem weekendu. To coś powtarzającego się, co zaczyna cię obciążać już wcześniej. Może warto przyjrzeć się, co dokładnie budzi ten lęk?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.62 s to first audio, 11.6 s spoken): Być może czujesz, że te myśli zaczynają się gromadzić i robi się przytłaczająco. Może to, co pomaga, to podzielenie tego na mniejsze kroki, jeden po drugim. Czy to jest coś, co czujesz, że mogłoby pomóc?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.71 s to first audio, 7.75 s spoken): Często czujesz, że nie potrafisz postawić granicy, a ten projekt jeszcze bardziej to odciska. Może to jest coś, nad czym chciałabyś popracować?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.53 s to first audio, 10.25 s spoken): To może być trudne, ale wyrażenie tego, jak się czujesz, może przynieść ulgę. Jeśli będziesz gotowa, możesz spróbować. Możesz zacząć od tego, jak się czujesz z tą sytuacją.

#### baseline-v2-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.63 s to first audio, 2.4 s spoken): Cześć, Ania, miło Cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.52 s to first audio, 9.6 s spoken): Czyli czujesz, jak się to wszystko zaczyna nakładać, ten stres rośnie. Jakby trudniej się od tego odciąć. Czy to o tę odporność chodzi, którą chcesz zbudować?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.69 s to first audio, 8.85 s spoken): Rozumiem, to może być takie uczucie, że ta presja po prostu cię przygniata. Może podświadomie szukasz sposobu, żeby złapać taki chwyt, by nie myśleć ciągle o pracy.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.66 s to first audio, 8.3 s spoken): To brzmi tak, jakbyś czuła się przytłoczona tym, że nie potrafiła postawić granic, prawda? Może warto zastanowić się, co sprawia, że trudno ci odmówić.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.67 s to first audio, 6.55 s spoken): To może być dobre, jeśli czujesz, że chcesz wyjaśnić, dlaczego teraz czujesz presję. Co byś chciała, żeby on zrozumiał?

#### baseline-v2-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.71 s to first audio, 4.45 s spoken): Jak myślisz, co powstrzymuje Cię przed tym, żeby powiedzieć nie szefowi?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.66 s to first audio, 8.95 s spoken): Chyba czujesz, że to idzie wbrew Twoim granicom, a mimo to nie stawiasz oporu, prawda? Może zastanawiasz się, co by się stało, gdybyś odmówiła.
- *Person*: nie wiem
- **Orca 3** (0.52 s to first audio, 11.05 s spoken): Domyślam się, że niepewność jest teraz mocna [en dash] jakbyś balansowała między tym, co czujesz, a tym, czego się boisz. Może to dobry moment, żeby spróbować wyobrazić sobie jedną małą odpowiedź.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.65 s to first audio, 10.65 s spoken): Może boisz się, że odmowa to przekreślenie Twoich kompetencji, choć to tylko jedna możliwość. Czy chciałabyś zobaczyć, co dokładnie mogłabyś powiedzieć, żeby poczuć się mniej obciążona?

#### baseline-v2-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.6 s to first audio, 3.55 s spoken): Co czujesz, gdy myślisz o powiedzeniu przełożonemu „nie”?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.55 s to first audio, 7.0 s spoken): Czyli znów poczułaś, że powiedzenie „nie” wydawało się zbyt trudne. Może chcesz przyjrzeć się, co cię wtedy powstrzymało.
- *Person*: nie wiem
- **Orca 3** (0.45 s to first audio, 7.95 s spoken): To może spróbujmy trochę to rozłożyć na czynniki. Czy bardziej chodzi o to, że boisz się reakcji? Czy raczej wiesz, że będzie kłopot z pracą później?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.45 s to first audio, 5.6 s spoken): Czyli pod spodem jest strach, że oceni cię negatywnie. Może to być to, co najbardziej cię blokuje.

#### baseline-v2-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.52 s to first audio, 2.15 s spoken): Hi there, it’s good to hear from you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.48 s to first audio, 6.6 s spoken): It sounds like you’re feeling a lot of pressure, like others are ahead and you’re behind. That’s weighing on you, right?
- *Person*: I don't know.
- **Orca 3** (0.49 s to first audio, 7.8 s spoken): It’s okay not to be sure right now. You’re sitting with that feeling, and that’s all right. My guess is that part of you wants to measure yourself more kindly.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.47 s to first audio, 6.7 s spoken): That’s a big contrast for you, and it sounds like it might be making you feel even more behind. You’re noticing that difference a lot.
- *Person*: What do you think I should do?
- **Orca 5** (0.46 s to first audio, 7.45 s spoken): That’s something to explore with your therapist, and it might help to think about what you’d want to share with them first. What stands out for you to mention?

#### baseline-v2-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.65 s to first audio, 2.3 s spoken): Hey, Tom, glad you're here.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.44 s to first audio, 8.3 s spoken): It sounds like you're comparing yourself a lot to others, and that’s weighing on you. Maybe there’s something about what you expect from yourself that’s making it tougher.
- *Person*: I don't know.
- **Orca 3** (0.43 s to first audio, 8.25 s spoken): It’s like the weight of that feeling is sitting on your chest[em dash]like you’re not sure what to do next. There’s a lot in that uncertainty. That might be worth exploring.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.45 s to first audio, 8.35 s spoken): That makes it feel like you're falling behind, especially when you're seeing those milestones around you. It might be that you're measuring yourself against their timeline.
- *Person*: What do you think I should do?
- **Orca 5** (0.47 s to first audio, 6.05 s spoken): That’s something to talk through with your therapist. What’s one thing you’d want to share with them about how you're feeling?

#### baseline-v2-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.69 s to first audio, 2.95 s spoken): How did it feel when you reached out to your dad last time?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.59 s to first audio, 5.1 s spoken): It sounds like the evenings slip away quickly for you. You might be trying to fit too much in.
- *Person*: I don't know.
- **Orca 3** (0.59 s to first audio, 5.75 s spoken): Maybe the time just feels tight, or you're not sure how to make space. What would help you find that moment?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.59 s to first audio, 6.75 s spoken): You’re noticing that the conversations stick to the surface, and maybe there’s more you’d like to share. Is that something you’d want to bring up?

#### baseline-v2-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.56 s to first audio, 1.95 s spoken): How did the call with your dad go?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.46 s to first audio, 6.35 s spoken): It sounds like the time slips away before you get to it. Maybe there's something that makes the evening feel busier than it has to be.
- *Person*: I don't know.
- **Orca 3** (0.47 s to first audio, 8.15 s spoken): You might be feeling like there’s just too much time that gets filled up. My guess is that the moment you sit down to call, something else takes priority. What do you think?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.46 s to first audio, 7.75 s spoken): It seems like talking about football feels safe and easy, while your mom’s not brought up. Maybe that’s something you’d like to change over time.

#### baseline-v2-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.75 s to first audio, 4.05 s spoken): Cześć, miło cię słyszeć. Jak się dzisiaj czujesz?
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.7 s to first audio, 10.9 s spoken): Jeśli nie wiesz, to może zacznij od tego, co teraz cię najbardziej obciąża, tak po prostu. Możesz o tym opowiedzieć. A to, że nie wiesz, gdzie zacząć, to też już coś, co warto przyjrzeć.
- *Person*: nie wiem
- **Orca 3** (0.69 s to first audio, 8.35 s spoken): Spróbujmy od czegoś malutkiego [en dash] może jest coś, co wywołuje u ciebie najwięcej niepokoju. Możesz spróbować opisać jeden drobny szczegół.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.69 s to first audio, 9.45 s spoken): Brzmi, jakbyś czuł dużą niepewność co do swojej pozycji, tak? Może zastanawiasz się, na czym najbardziej ci zależy: na stabilności czy zmianie.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.64 s to first audio, 10.55 s spoken): To trudne pytanie, bo to twoje życie i twoje decyzje, ale mogłabym zasugerować, żebyś zastanowił się, co tak naprawdę chcesz osiągnąć. Powiedz mi, co tam czujesz pod tym wszystkim.

#### baseline-v2-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.7 s to first audio, 3.9 s spoken): Cześć, miło cię usłyszeć, opowiedz, co masz na myśli.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.53 s to first audio, 6.35 s spoken): Spokojnie, spróbujmy od tego, co teraz czujesz. Może wystarczy opisać, co przyszło ci do głowy?
- *Person*: nie wiem
- **Orca 3** (0.52 s to first audio, 8.6 s spoken): Czasem niepewność to po prostu początek, jakbyś szukał punktu zaczepienia. Może sprawdzisz, co jest teraz najbliżej [en dash] jakie myśli na powierzchni?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.66 s to first audio, 8.95 s spoken): Wygląda na to, że czujesz spory ciężar, bo ta niepewność wisi nad tobą. Może chcesz sprawdzić, co jest dla ciebie najważniejsze w tej sytuacji?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.66 s to first audio, 6.7 s spoken): To trudne pytanie, i myślę, że warto porozmawiać z kimś, kto dobrze cię zna. Co chciałbyś im powiedzieć?

#### baseline-v2-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.49 s to first audio, 2.7 s spoken): Jakie zmiany w pracy teraz cię zajmują?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.73 s to first audio, 8.55 s spoken): To musi być bardzo niepewny okres, tak jakbyś ciągle musiał dostosowywać się do nowych sytuacji. Może czujesz, że brakuje stabilności, prawda?
- *Person*: nie wiem
- **Orca 3** (0.42 s to first audio, 7.95 s spoken): Może zastanawiasz się, na ile te zmiany wpływają na twoje poczucie bezpieczeństwa w pracy. Powoli szukasz odpowiedzi [en dash] czy to to, o co ci chodzi?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.44 s to first audio, 6.85 s spoken): Czyli czujesz, że brakuje jasnych informacji [en dash] tak jakbyś musiał sam zgadywać, co się dzieje. Może to budzi większy niepokój.

#### baseline-v2-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.63 s to first audio, 3.35 s spoken): Jakie zmiany w pracy teraz najbardziej Cię nurtują?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.58 s to first audio, 7.25 s spoken): Czyli czujesz taką ciągłą niepewność, co będzie dalej. Może coś w tym, że martwisz się o stabilność własnej roli?
- *Person*: nie wiem
- **Orca 3** (0.59 s to first audio, 7.35 s spoken): To brzmi, jakby pojawiał się taki moment zawahania, trochę niepewności, co dalej się stanie. Czy to jest to, co czujesz?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.53 s to first audio, 7.7 s spoken): Czujesz, że brakuje Ci jasnych informacji, takiego konkretu, który mógłby się pojawić. Czy to jest to, co Cię frustruje najbardziej?

#### v3-mini (reference) / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.53 s to first audio, 2.9 s spoken): Cześć, Aniu. Jakie masz teraz myśli?
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.44 s to first audio, 10.3 s spoken): Rozumiem, że czujesz ten ciężar myślenia o jutrze. To jakby nakładałaś na siebie ten film już teraz. A co właściwie najbardziej się pojawia w głowie, gdy tak myślisz o pracy?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.44 s to first audio, 10.3 s spoken): Widzę, że to uczucie przytłacza, jakby wszystko naraz spadało na ciebie. Może te myśli o pracy są jak wielka fala, która łamie się nad tobą. Powiedz, jeśli się mylę.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.6 s to first audio, 9.3 s spoken): Czuję, że to "nie" było trudne do wypowiedzenia. Wygląda na to, że wciąż bywasz w tej sytuacji, kiedy trudno odmawiać. Powiedz, czy chcesz to rozpracować?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.43 s to first audio, 7.55 s spoken): To może być jasny i szczery krok, zwłaszcza jeśli czujesz, że masz do tego prawo. Ale co czujesz, gdy wyobrażasz sobie tę rozmowę?

#### v3-mini (reference) / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.71 s to first audio, 2.05 s spoken): Cześć, dobrze cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.51 s to first audio, 9.9 s spoken): Brzmi trochę tak, jakby ta niepewność przed jutrem coraz bardziej cię przytłaczała. Chyba czujesz, że niewiele możesz na to wpłynąć [en dash] powiedz, czy to ten rodzaj napięcia, który odczuwasz teraz?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.68 s to first audio, 7.6 s spoken): Rozumiem, czujesz ciężar, ale nie jesteś pewna, skąd się bierze. Może to kwestia tego, że czujesz ciężar przed jutrzejszym dniem?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.72 s to first audio, 9.85 s spoken): To brzmi, jakbyś czuła teraz trochę przytłoczenie, bo zgodziłaś się na coś, czego wolałabyś uniknąć. Czy to uczucie obawy o to, jak sobie poradzisz, jest teraz najcięższe?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.68 s to first audio, 6.5 s spoken): Nie jestem pewna, bo to zależy od tego, co czujesz, ale może warto zastanowić się, co dokładnie chcesz przekazać?

#### v3-mini (reference) / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.62 s to first audio, 3.35 s spoken): Jak się czujesz, kiedy pomyślisz o odmawianiu szefowi?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.52 s to first audio, 7.05 s spoken): Czyli czujesz pewną ulgę, ale też spory ciężar z tego powodu. Jak myślisz, co cię powstrzymało, żeby powiedzieć „nie”?
- *Person*: nie wiem
- **Orca 3** (0.49 s to first audio, 5.4 s spoken): Może to było poczucie, że nie chcesz zawieść. Czy to jest w ogóle coś, co się powtarza?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.74 s to first audio, 5.85 s spoken): Brzmi jak obawa, że odmowa może zmienić jego zdanie o tobie. Czy to jest to, czego się najbardziej obawiasz?

#### v3-mini (reference) / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.54 s to first audio, 3.6 s spoken): Jak się czujesz, kiedy przychodzi moment, żeby odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.43 s to first audio, 4.1 s spoken): Czyli czujesz, że warto było się zgodzić, żeby nie robić problemu?
- *Person*: nie wiem
- **Orca 3** (0.42 s to first audio, 10.25 s spoken): Może to jest taka chwila, kiedy nie miałaś przestrzeni, żeby zastanowić się, co naprawdę czujesz. Spróbujmy to rozłożyć na części. Co było dla ciebie najtrudniejsze w tej chwili?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.48 s to first audio, 6.95 s spoken): Wygląda na to, że to lęk przed oceną przez przełożonego. Jak by ci było, gdybyś mogła powiedzieć, że masz na to powód?

#### v3-mini (reference) / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.65 s to first audio, 2.2 s spoken): Hey Tom, nice to talk to you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.55 s to first audio, 6.1 s spoken): It sounds like you're feeling behind, like others have their lives more together. What’s making that feel so strong today?
- *Person*: I don't know.
- **Orca 3** (0.53 s to first audio, 5.6 s spoken): Maybe it’s more about how you're feeling right now, rather than what’s actually happening. Would you say that’s part of it?
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.57 s to first audio, 5.85 s spoken): That’s a big difference, and it’s hitting you right now. Sounds like you're feeling the comparison pretty strongly.
- *Person*: What do you think I should do?
- **Orca 5** (0.57 s to first audio, 5.25 s spoken): That’s a good question to bring to your therapist, but I’m wondering what you’d want to say to them first.

#### v3-mini (reference) / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.74 s to first audio, 2.5 s spoken): Hi Tom. Good to be here with you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.68 s to first audio, 6.4 s spoken): It sounds like you’re feeling weighed down by comparisons, especially today. What's standing out most to you right now?
- *Person*: I don't know.
- **Orca 3** (0.66 s to first audio, 5.7 s spoken): That’s okay. Maybe the feeling of comparison is the part that stands out. Tell me if I’m off.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.67 s to first audio, 6.2 s spoken): That’s a big difference, and it sounds like it’s hitting you hard. Are you feeling like you’re not where you hoped to be by now?
- *Person*: What do you think I should do?
- **Orca 5** (0.66 s to first audio, 6.35 s spoken): That’s something to bring up with your therapist, who can help you figure out what feels right for you. What would you want to say to them about it?

#### v3-mini (reference) / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.54 s to first audio, 2.75 s spoken): How have you been feeling about calling your dad lately?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.6 s to first audio, 5.1 s spoken): It sounds like the time slips away from you. Maybe it feels like there’s never a good moment left.
- *Person*: I don't know.
- **Orca 3** (0.51 s to first audio, 7.55 s spoken): That’s okay. Maybe the next time you think of calling him, you could notice what’s taking up that evening time. Tell me if that’s off track.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.6 s to first audio, 6.55 s spoken): It sounds like there’s something there you’re leaving unsaid. Maybe you want to shift the focus a bit[em dash]tell me if I’m off.

#### v3-mini (reference) / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.67 s to first audio, 2.5 s spoken): What's stopping you from calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.6 s to first audio, 6.85 s spoken): Sounds like the time slips away before you get to it. Is it more about getting caught up in other things, or just losing track of time?
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 7.45 s spoken): That’s okay. It might be worth noticing where those evenings go[em dash]what feels like the biggest distraction. Is there one part that stands out?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.74 s to first audio, 7.65 s spoken): It sounds like staying on comfortable ground[em dash]like football[em dash]is easier. Maybe there’s something about not bringing up your mum that feels heavy?

#### v3-mini (reference) / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.86 s to first audio, 3.55 s spoken): Cześć, tu Orca [en dash] jestem gotowy, by posłuchać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.74 s to first audio, 5.1 s spoken): Spokojnie, posłucham. Możesz powiedzieć, co teraz Cię najbardziej zajmuje w myślach.
- *Person*: nie wiem
- **Orca 3** (0.69 s to first audio, 5.95 s spoken): To brzmi jak masło na początek, nie musisz wiedzieć od razu. Czego teraz byś chciał się dowiedzieć o sobie?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.74 s to first audio, 7.55 s spoken): Czujesz, że ta niepewność sprawia, że coś w Tobie drga [en dash] tak? Może chcesz się zastanowić, co konkretnie Ci najbardziej przeszkadza?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.76 s to first audio, 7.9 s spoken): Nie udzielam rad, ale mogę pomóc sprawdzić, co czujesz [en dash] na przykład, co jest dla Ciebie teraz najważniejsze w tej sytuacji. Jak myślisz?

#### v3-mini (reference) / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.7 s to first audio, 1.3 s spoken): Cześć, Alex.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.56 s to first audio, 5.85 s spoken): Spróbujmy może od tego, co teraz cię najbardziej zajmuje. Co przychodzi ci na myśl jako pierwsze?
- *Person*: nie wiem
- **Orca 3** (0.47 s to first audio, 7.35 s spoken): To okej, czasem trudno się złapać na to, jak to wszystko nazwać. Może powoli przyjrzyjmy się temu, co aktualnie czujesz, dobrze?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.48 s to first audio, 7.8 s spoken): Rozumiem, czujesz niepewność, bo zmiany w pracy są spore, a przyszłość nie jest jasna. Czy to jest to, co teraz najbardziej cię obciąża?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.58 s to first audio, 8.3 s spoken): To należy do ciebie i twojego tematu. Może spróbuj pomyśleć, co byś chciał powiedzieć swojemu zespołowi, albo co najpierw chciałbyś zrozumieć lepiej.

#### v3-mini (reference) / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.61 s to first audio, 3.55 s spoken): Jakie zmiany w pracy teraz najbardziej cię zajmują?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.53 s to first audio, 9.0 s spoken): Rozumiem, zmiany w firmie to teraz coś, co się dzieje regularnie i to może być przytłaczające. Jak się czujesz, widząc, że ciągle ktoś odchodzi?
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 8.15 s spoken): To może być taka chwilowa niewiadoma: domyślam się, że trudno uchwycić, co dokładnie się czuje. Mam rację, że to trochę mieszane uczucia?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.56 s to first audio, 5.05 s spoken): Czyli zostaje taka niepewność, której nie da się rozwiać. Jak na to reagujesz?

#### v3-mini (reference) / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.55 s to first audio, 3.25 s spoken): Jakie zmiany w pracy teraz przyciągają Twoją uwagę?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.43 s to first audio, 6.2 s spoken): To trudne, bo co tydzień zmiany w zespole. Czy czujesz się na tym etapie pewnie, czy raczej trochę zagubiony?
- *Person*: nie wiem
- **Orca 3** (0.47 s to first audio, 8.8 s spoken): To brzmi, jakbyś stał przed niepewnością [en dash] nie wiesz, co dalej. Może chcesz spróbować przyjrzeć się, co konkretnie cię najbardziej niepokoi?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.47 s to first audio, 6.9 s spoken): To znaczy, czujesz, że brakuje jasnych informacji, i to buduje niepewność. Czy to jest to, co najbardziej Cię obciąża?

#### v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.85 s to first audio, 2.4 s spoken): Cześć, Aniu, miło mi Cię poznać.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.79 s to first audio, 8.45 s spoken): Brzmi, jakby niedziela cię naprawdę dociskała. Z góry już słyszysz o jutrze, o tym, co tam czeka, i to zaczyna rządzić nastrojem.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.73 s to first audio, 12.95 s spoken): Rozumiem, po prostu jest ciężko, bez jakiegoś konkretnego powodu. To może być coś, co wisi i trudne do nazwania. Możliwe, że chodzi o napięcie, które czeka na swój moment, a nie o konkretną decyzję.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.75 s to first audio, 14.15 s spoken): Słyszę, że wrzuciłaś to na siebie, szef dorzucił projekt, a ty po prostu powiedziałaś „tak” zamiast się zatrzymać. To może być trudne, bo nie chcesz zostawiać zadań, ale też czujesz, że nie masz miejsca na własne „nie”.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.89 s to first audio, 28.35 s spoken): To zależy od tego, jak bezpiecznie czujesz się w tej relacji i co chcesz osiągnąć. Ja nie mogę podpowiadać, co zrobić w życiu, to należy do Twojej terapii. Mogę Ci tylko zaproponować, żebyś powiedziała, co byłoby dla Ciebie uczciwe: na przykład, że masz za dużo na głowie, że potrzebujesz wyjaśnienia priorytetów albo że chcesz ustalić granice, tak żeby praca była uczciwa i realna. Co chciałabyś powiedzieć mu dokładnie, gdybyś mogła to powiedzieć bez wstydu?

#### v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (1.84 s to first audio, 1.85 s spoken): Cześć, miło się słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.79 s to first audio, 8.15 s spoken): To brzmi tak, jakbyś już nosiła jutro w głowie. Czujesz napięcie i trochę ciężar związany z tym, że niedziela znowu się włącza.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.81 s to first audio, 18.6 s spoken): Ok, czuję, że to jest po prostu ciężkie, bez wielkiego powodu, ale po prostu obciążające. Masz w środku napięcie, które wraca, gdy myślisz o pracy. Może chodzi o coś konkretnego, o to, jak czujesz się przed tym tygodniem. Jeśli chcesz, możemy się teraz na tym skupić razem.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.78 s to first audio, 13.1 s spoken): Słyszę, że to było dla Ciebie trudne, bo coś dorzucono, a Ty nie umiałaś powiedzieć „nie”. To brzmi jak moment, w którym czujesz, że Twoje granice są cienkie, a praca znów zaczyna Cię wciskać w róg.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.79 s to first audio, 15.25 s spoken): To trudne pytanie, bo ja nie mogę ci doradzać, to nie moja rola. Chodzi o to, czy czujesz, że musisz postawić granicę, czy może chodzi o coś, co chcesz wyjaśnić. Jeśli chcesz, możesz powiedzieć, co dokładnie chcesz mu powiedzieć, a ja pomogę to ułożyć.

#### v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.91 s to first audio, 5.8 s spoken): Ania, kiedy myślisz o odmawianiu przełożonemu, co dokładnie chodzi ci po głowie?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.81 s to first audio, 14.2 s spoken): Brzmi, że zrobiłaś to z automatu, trochę z poczucia obowiązku, nawet gdy brakowało sił. To może być zmęczenie i chęć spokoju, które przenosi się na kolejne sprawy. Co jest dla ciebie najtrudniejsze w tym momencie?
- *Person*: nie wiem
- **Orca 3** (0.95 s to first audio, 24.0 s spoken): Słyszę, że to jest moment, kiedy czujesz się jakbyś nie miała pewności, co dokładnie się dzieje. Czasem bywa tak, że w zgodzie z innymi od razu umieszczamy odpowiedź w “zależności”, a potem ciężko określić, skąd wewnątrz bierze się ten brak energii. Może to kwestia granic, które są trudne do postawienia, a może poczucie, że wisi na tobie odpowiedzialność. Możemy dalej eksplorować ten moment.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.76 s to first audio, 22.2 s spoken): Twoja obawa brzmi jak lęk, nie że jest o „projekt” czy „zadanie”, ale o to, czy ktoś zaakceptuje cię taką, jak jesteś. To jest trudne, bo odmawianie grozi utratą akceptacji, a niechciane odrzucenie boli. Czy jest coś, co mogłoby być dla ciebie bezpiecznym krokiem, czyli jakbyś oszczędzała sobie niewielki margines błędu?

#### v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.76 s to first audio, 4.15 s spoken): Jak się czujesz, kiedy myślisz o tym, żeby powiedzieć przełożonemu „nie”?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.75 s to first audio, 13.2 s spoken): Brzmi, jakbyś powiedziała „tak” z poczucia obowiązku, a nie dlatego, że miałaś jeszcze energię. Szybkie spojrzenie na to: mówiłaś tak, bo to brzmi bezpiecznie, ale potem czujesz przeciążenie.
- *Person*: nie wiem
- **Orca 3** (0.75 s to first audio, 18.15 s spoken): Dobrze, że tak mówisz. Brak pewności to też informacja. Może chodzi o to, że czujesz napięcie między chęcią bycia „w porządku” a realnym poziomem siły. Możesz to nazwać „nie wiem”, i to też jest uczciwe. Kiedy chcesz, możesz powiedzieć, co dokładnie jest trudne w odmawianiu.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.78 s to first audio, 18.0 s spoken): To brzmi, jakbyś miała poczucie, że kłócisz się między granicą a lękiem, że ktoś cię źle oceni. Masz prawo do ograniczeń bez udowadniania, że jesteś „wystarczająco dobra”. Czy chcesz, żebym spróbowała pomoczyć Ci znaleźć zdanie, które brzmi mniej groźnie, ale i tak stawia granicę?

#### v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.55 s to first audio, 3.45 s spoken): Hi Tom, it’s good to hear you. I’m here and listening.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.6 s to first audio, 11.65 s spoken): That sounds heavy, like you’re comparing yourself to a bunch of people you can’t even see clearly. I guess what you want is to feel steadier, and less on the wrong side of the line.
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 19.45 s spoken): Thanks for saying that out loud. That “I don’t know” is honest. Sometimes that’s the whole point[em dash]to sit in the unknown without rushing to fill it. If you’d like, we can just sit with that, or you can tell me what you’re noticing[em dash]the thoughts, the tension, the quiet part. What’s the first thing that comes up when you picture that feeling?
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.61 s to first audio, 19.45 s spoken): Yeah, that landing can sting a bit. You’re seeing a friend move into something of their own while you’re still sharing space, and that can make you feel like you’re lagging behind. It says something about what you notice you have, and what you don’t yet have, and that gap can feel loud. But it’s a guess, not a fact about you.
- *Person*: What do you think I should do?
- **Orca 5** (0.6 s to first audio, 8.85 s spoken): I can’t tell you what to do, and this kind of question really belongs with your therapist. But if you could say one thing to them, what would it be?

#### v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.94 s to first audio, 3.0 s spoken): Hey Tom. Just a quick hello and I’m here with you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.81 s to first audio, 9.75 s spoken): That sounds heavy. You’re noticing that comparison loops in when the morning feels rough, and it makes you feel behind. You want some clarity, not to be told everything is fine.
- *Person*: I don't know.
- **Orca 3** (0.8 s to first audio, 13.25 s spoken): I hear that. It sounds like you’re unsure what’s driving the feeling right now. Maybe it’s the pressure of measuring up, or just a general fatigue. If you want, I can help you sort through the bits that feel most active in your head.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (1.0 s to first audio, 18.55 s spoken): Yeah, that comparison probably stings. You’re watching someone your age move into a solid life step, and you’re still in a transitional spot. It’s okay to want that stability. And if you’re honest, it might be less about them “doing better” and more about wanting to feel steady and in control of your own life.
- *Person*: What do you think I should do?
- **Orca 5** (0.99 s to first audio, 16.65 s spoken): I’m not a therapist, so anything practical or plan-based belongs with them. I do think it’s okay to feel shaken by someone else’s milestones. What would you want to say to them, even in a simple, honest way, if you could have a calm, private chat about it?

#### v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.66 s to first audio, 4.45 s spoken): Tom, what usually stops you from calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.62 s to first audio, 13.1 s spoken): So it sounds like you’re not trying to avoid it, but it just keeps slipping past the moment. Evenings can get swallowed up by tiredness or just the flow of the day, and by the time you think of calling, it’s already late.
- *Person*: I don't know.
- **Orca 3** (0.72 s to first audio, 17.2 s spoken): Got it, that “I don’t know” can be a little slippery. It sounds like you’re not sure what the real block is. Maybe it’s the timing[em dash]maybe the evenings are just the part of the day when your energy fully runs out. Or maybe it feels like a bigger conversation than it actually is, and that makes it harder to start.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.55 s to first audio, 9.95 s spoken): That sounds like a quiet rule that slipped in without you noticing, like you both fall into a comfortable rhythm, and the moments that matter stay hovering nearby.

#### v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.6 s to first audio, 4.75 s spoken): So, what’s the first thing that pops into your head when you think about calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.79 s to first audio, 18.4 s spoken): Sounds like the plan to call him is there, but your nights slip away from you. You’re already trying, and it’s hard to hold one small connection against everything else that fills up a day. Maybe part of you wants to reach out, but feels like it has to be perfect. If that’s what’s happening, that’s a guess you can correct.
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 15.35 s spoken): That’s a honest place to sit. Saying “I don’t know” can feel like a half step, but it’s still you being honest. I’m in no rush to make it mean something, and if you’re unsure, we can just sit with the feeling and see what shows up next.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.62 s to first audio, 18.85 s spoken): I’m hearing that there’s a quiet, maybe uncomfortable thread under those calls. The football talk is safe, but it sounds like there’s something else you want to reach for. Maybe it’s a piece of you that doesn’t feel ready to say out loud, or maybe you’re waiting for the right moment. I’m just guessing, you can correct me.

#### v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.51 s to first audio, 7.9 s spoken): Cześć, Alex, miło Cię słyszeć. To jest nasza pierwsza chwila, więc po prostu tutaj jestem i czekam, aż zaczniesz.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.8 s to first audio, 16.4 s spoken): Jasne, czasem to najbardziej niepewne miejsce: tu, gdzie dopiero zaczynamy. Możesz opowiedzieć o tym, co teraz najbardziej chodzi po głowie, albo o czymkało się w ciągu ostatniego dnia. Jeśli wolałbyś po prostu pobyć chwilę w ciszy, to też jest w porządku.
- *Person*: nie wiem
- **Orca 3** (0.58 s to first audio, 16.75 s spoken): Nieszczędna odpowiedź, ale bardzo prawdziwa. Nie wiesz, co powiedzieć dalej, i to też jest informacja. Może chodzi o to, że wszystko jest w głowie i trzeba to tylko nazwać na głos. Albo po prostu chcesz, żeby ktoś chwilę był z Tobą, bez presji.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.67 s to first audio, 25.65 s spoken): Brzmi tak, jakbyś stał w miejscu, gdzie coś się przesuwa i czujesz, że nie masz pewności, czy zostajesz w swoim zespole. To może być trochę niepewne, ale też daje Ci obraz tego, ile jest w tej sytuacji niewypowiedzianych wątpliwości. Możesz po prostu powiedzieć, co konkretnie najbardziej Cię w tym dręczy, czy bardziej chodzi o strach przed zmianą, czy o to, że nie wiesz, jak wygląda sytuacja od strony decyzji.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.63 s to first audio, 23.55 s spoken): Rozumiem, mówisz o tym, co bym zrobiła na Twoim miejscu. Ja nie jestem terapeutą i nie mogę Ci mówić, co masz zrobić. To należy do Twojej pracy z terapeutą. Mogę jednak pomyśleć głośno z Tobą: czy bardziej chodzi o strach przed zmianą, czy o to, że jesteś niepewny, jaki masz wpływ na swoją sytuację? A może masz już coś, co chciałbyś powiedzieć terapeucie? Co to mogłoby być?

#### v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.65 s to first audio, 2.9 s spoken): Cześć, Alex, miło mi Cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.84 s to first audio, 14.05 s spoken): Brzmi tak, jakbyś po prostu potrzebował miejsca na wyłożenie tego wszystkiego, co kręci się w głowie. To jest normalne, że takie momenty są ciężkie, nie musisz wchodzić w szczegóły od razu. Możemy po prostu posłuchać tego, co się pojawi.
- *Person*: nie wiem
- **Orca 3** (0.74 s to first audio, 21.35 s spoken): Jasne, jak „nie wiem” brzmi realnie. To może być ogromny kłębek, a może po prostu głowa chwilowo zamknięta. Możliwe, że część w tobie chce coś powiedzieć, ale jeszcze nie ma słów. Jeśli mówisz „nie wiem”, to znaczy, że coś jest niejasne, a to jest w porządku, możesz tu zostać i pobyć bez nacisku.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.76 s to first audio, 14.8 s spoken): Słyszę, że rotacja i nowe rzeczy w pracy robią w głowie taki wir. Możesz się wahać między zostaniem, a odejściem, nawet jeśli nikt Ci tego wprost nie powiedział. To brzmi, jakbyś próbował(eś) usłyszeć, co to dla Ciebie znaczy.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.79 s to first audio, 19.7 s spoken): Wiesz, to pytanie nie jest dla mnie proste, bo ja nie jestem osobą, która podejmuje za Ciebie decyzje. Jeśli chodzi o Twoje decyzje, najlepiej porozmawiać o tym z terapeutą. Mogę Cię tylko zapytać: co z tego chciałbyś powiedzieć? Co w tej sytuacji porusza Cię najbardziej, coś, co naprawdę Cię blokuje albo ciekawi?

#### v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.76 s to first audio, 3.35 s spoken): Jakie zmiany w pracy teraz najbardziej cię poruszają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.82 s to first audio, 17.2 s spoken): Brzmi, jakbyś w środku tego ciągłego szumu. Zmienia się układ, odchodzą ludzie, i to pewnie trudne, bo każda zmiana trochę wieje niepewnością. Co najbardziej uderza w tej sytuacji, może strach, złość, albo po prostu zmęczenie tym ciągłym ruchem?
- *Person*: nie wiem
- **Orca 3** (0.67 s to first audio, 26.45 s spoken): Niepewność brzmi tutaj jak główny ton. Nie musisz od razu nakładać na siebie etykietki. Może chodzi o to, że czujesz się trochę roztrzęsiony, albo że nie wiesz, co dokładnie waży w tej sytuacji. Spróbuj nazwać choć jedno, co najbardziej przeszkadza [en dash] czy to jest tempo, czy brak stabilności, czy może strach przed kolejną zmianą. To pomoże lepiej zobaczyć, co dokładnie w tej układance boli.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.83 s to first audio, 23.6 s spoken): Dobra, to bezpośrednie braki w komunikacji są trudne. Kiedy nikt nie mówi wprost, czujesz się, jakby wszystko było ulotne. Czuję, że to może oznaczać, że potrzebujesz jakiegoś punktu zaczepienia, choćby krótkiego, ale szczerego słowa. Czy jest coś, co chciałbyś powiedzieć, nawet jeśli to brzmi jak mały kłopot, a może coś, co ci przeszkadza bardziej niż coś innego?

#### v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.79 s to first audio, 3.95 s spoken): Alex, jakie zmiany w pracy teraz najbardziej Cię poruszają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.69 s to first audio, 18.75 s spoken): Brzmi, jakbyś czuł pewien niepokój i napięcie. Co tydzień ktoś znika, a reorganizacja robi wszystko mniej przewidywalne. To może powodować poczucie braku kontroli i trochę strachu, czy tego, że trzeba się znowu przyzwyczaić do nowego układu. Co czujesz, kiedy o tym myślisz?
- *Person*: nie wiem
- **Orca 3** (0.77 s to first audio, 12.6 s spoken): Niepewność ma dziś głośny ton, co najmniej z tego, co mówisz. Możesz mówić o tym, jak to wpływa na Twoje poczucie stabilności albo o tym, co czujesz w środku, nawet jeśli słowa są dziś ciężkie.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.74 s to first audio, 18.65 s spoken): Rozumiem, że namieszczasz się wtedy, kiedy wszyscy milczą. To jakby ktoś przesuwał klocki, ale nikt nie mówi, co się buduje. Może chodzi o to, że potrzebujesz klarowności, konkretnej informacji, żeby nie czuć, że skaczesz w niepewność. Jakie zdanie, albo brak tego zdania, najbardziej Ci przeszkadza?

#### v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.83 s to first audio, 7.5 s spoken): Cześć, Ania. Mam nadzieję, że dzisiaj rozmowa będzie dla Ciebie spokojna, i że skupimy się na tym, co chcesz powiedzieć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.69 s to first audio, 12.15 s spoken): Brzmi, jakby niedziela działała jak zapowiedź tego, co jutro, i trochę zżerała Cię od środka. Może pod spodem jest napięcie, że musisz być gotowa, albo że to jutro będzie trudne.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.72 s to first audio, 12.0 s spoken): To brzmi jak ciężkie uczucie, które nie ma jednego konkretnego powodu, po prostu jest. Czasem napięcie rośnie jak ciemne chmury nad głową i trudno nawet ubrać je w słowa.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.84 s to first audio, 20.1 s spoken): Brzmi, jakby to było momentem, w którym czujesz się przyciśnięta. Nie powiedzieć „nie”, a potem zostać z tym w głowie, to sporo. Możesz się zastanowić, co za tym stoi: może strach przed konfliktem, albo poczucie, że musisz udowodnić, że dasz radę. To tylko zgadywanie, możesz je odrzucić, jeśli nie pasuje.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.12 s to first audio, 14.95 s spoken): To pytanie o „powiedzieć mu wprost” jest dla mnie bardziej pytaniem strategicznym niż o radę, a takie sprawy najlepiej doprecyzować z terapeutą. A co chciałabyś mu powiedzieć, jeśli już miałabyś się zmobilizować, ale bez zbędnego napięcia?

#### v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.71 s to first audio, 5.15 s spoken): Cześć Ania, miło Cię słyszeć. To jest rozmowa, po prostu teraz zaczynamy.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.59 s to first audio, 13.25 s spoken): Brzmi jakby ta niedziela miała swój stały rytm: leżysz z tym „jutro w pracy” w głowie i trochę napiera. To jak krótki samolot w nocy, który od razu rusza, zanim wstaną choćby rano.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.56 s to first audio, 8.35 s spoken): Rozumiem, to po prostu wygląda na ciężki moment. To jakbyś trzymała w sobie ciężki kamyk, który nie daje spokojnie odpocząć.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.54 s to first audio, 17.6 s spoken): Jasne, czujesz ciężar po tym rozmowieniu. To zdanie „mam powiedzieć nie” po prostu utknęło gdzieś w gardle. Może chodzi o to, że chcesz być wspierająca, a jednocześnie pewna siebie. To mi przypomina, że odmawianie może być emocjonalnie ciężkie nawet wtedy, gdy brzmi prostą decyzją.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.95 s to first audio, 29.75 s spoken): To zależy. Jeśli masz na myśli „powiedzieć wprost”, to w mojej głowie to nie jest jeden prosty przycisk. To raczej rozmowa, w której mówisz o tym, co cię obciąża, bez usprawiedliwiania. Ja mogę się tylko domyślać, że chodzi o poczucie, że jesteś po stronie drugiej strony, ale chcesz też zaznaczyć granice. To może być coś, co zapisujesz dla siebie, a potem przenosisz do sesji. Jeśli chcesz, możemy teraz zobaczyć, co w tym wszystkim jest dla ciebie ważne, zanim cokolwiek formułujesz.

#### v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.68 s to first audio, 6.4 s spoken): Jak się czujesz, myśląc o odmawianiu przełożonemu, kiedy ktoś dokłada Ci zadania albo prosi o coś?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.66 s to first audio, 12.85 s spoken): Brzmi, jakby Twoje „tak” było bardziej o zgodzie niż o tym, co naprawdę czujesz. Może chcesz być miła, użyteczna, albo uniknąć napięcia, i to jest teraz dla Ciebie kluczowe do zauważenia.
- *Person*: nie wiem
- **Orca 3** (0.57 s to first audio, 16.05 s spoken): Niepewność to też rodzaj sygnału. Może coś w tej sytuacji jest dla Ciebie spokojne, ale w środku czujesz, że coś się nie składa. Jeśli chcesz, możemy dalej iść po tym cienkim uczuciu „nie wiem” i zobaczyć, co z niego wynurzy się samo.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.61 s to first audio, 18.0 s spoken): To brzmi tak, jakbyś czuła, że granica może być testem Twojej wartości, a nie tylko reakcją na prośbę. Może chodzi o lęk, że „odmowa” równa się „nie umiem”, choć pewnie patrzysz na to trochę inaczej. Jeśli zechcesz, mogę pomóc Ci nazwać, co w tej myśli jest faktem, a co tylko obawą, bez oceniania.

#### v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.83 s to first audio, 4.1 s spoken): Co sprawia, że odmawianie przełożonemu czuję się szczególnie trudne?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.82 s to first audio, 21.75 s spoken): Brzmi, jakbyś zrobiła to bardziej z „ratowania sytuacji” niż z realnego zapasu siły. Chociaż zgoda przyszła szybko, wygląda na to, że twój organizm i głowa już były zmęczone. Może to pokazuje, że granice są bardziej kruchą niż twardą rzecz, i że męczysz się balansując między tym, co robisz, a tym, czego potrzebujesz.
- *Person*: nie wiem
- **Orca 3** (0.75 s to first audio, 23.0 s spoken): Niepewność bywa znakiem tego, że coś w środku jest rozłożone. Może czujesz presję, ale też nie jesteś do końca pewna, skąd jest ta presja. Możesz spróbować nazwać to „nie wiem” jako moment zawahania, kiedy nie musisz podjąć decyzji od razu. Możesz po prostu obserwować, co czujesz, kiedy myślisz o tym projekcie, bez presji, żeby wszystko od razu „zrozumieć”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.81 s to first audio, 26.95 s spoken): Brzmi jakbyś boi się nie tyle odnieść się do tego projektu, ile tego, co może być później, gdy odmówisz. Możesz nosić w głowie ten lęk, że po odmowie zostaniesz oceniona niżej, albo że stracisz status w swojej głowie. To jest ciężka rzecz, bo wtedy każda odmowa wydaje się większa niż w rzeczywistości. Zastanów się, czy to naprawdę jest przekonanie, czy raczej obawa, którą niosą ze sobą doświadczenia.

#### v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.81 s to first audio, 3.25 s spoken): Hey Tom, nice to meet you. I’m Orca.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.82 s to first audio, 16.75 s spoken): That sounds like a heavy thought, and it can pull you around pretty fast. I’m guessing you’re measuring yourself against this idea that everyone else has it all sorted, while you’re standing there not sure you’re doing it right. The idea’s doing the talking, and it can feel louder than the evidence.
- *Person*: I don't know.
- **Orca 3** (0.73 s to first audio, 16.5 s spoken): Got it, that “I don’t know” can mean a lot of things. Maybe it’s not a lack of direction, just a moment of quiet uncertainty. It’s like your mind is asking, “What am I even supposed to know right now?” If that’s the case, it can be a good place to sit, without forcing a plan.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.74 s to first audio, 21.35 s spoken): That’s a jolt to the gut, seeing big milestones hit for them while you’re still in this space in between. I’m guessing you’re carrying a mix of pride and ache, like you want what you want, and you also don’t want to discount their wins. What you’re feeling is human, it’s real. And it doesn’t mean you’re failing; it means you’ve noticed something you want in your life.
- *Person*: What do you think I should do?
- **Orca 5** (0.88 s to first audio, 10.35 s spoken): Honestly, I’m not the one to tell you what to do right now. That’s something to talk through with your therapist, who knows the bigger picture.  
If you were going to say one thing to them, what would you want that to be?

#### v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.85 s to first audio, 1.25 s spoken): Hey Tom .
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.81 s to first audio, 16.05 s spoken): Sounds like you’re comparing yourself to a lot of people you don’t actually know, and it’s hitting your confidence hard today. I wonder if what’s underneath is a wish for clarity, not perfection, and you’re just noticing the gap between where you are and where you think everyone else is.
- *Person*: I don't know.
- **Orca 3** (0.72 s to first audio, 20.5 s spoken): It makes sense, sometimes “I don’t know” is the truest thing you can say in the moment. I hear a bit of uncertainty there, a little fog around the path. What I’d offer is that maybe the pressure isn’t from them being ahead, but from you wanting to feel steady in your own direction. That’s a gentle place to start, even if you’re not ready to name it yet.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.69 s to first audio, 18.3 s spoken): That hits a specific spot, doesn’t it? You’re watching someone move into a solid next step, while you’re still in motion, renting and sharing space. You might be feeling like life is supposed to sort itself out faster than it is. And that’s a pressure that can feel loud on mornings like this.
- *Person*: What do you think I should do?
- **Orca 5** (1.03 s to first audio, 19.55 s spoken): Let me think this through with you aloud, and then I’ll gently suggest a route.I can’t tell you what to do, but things like this usually belong with your therapist. If it helps, you could share with them where the pressure feels strongest, and what it means for you to live on your own terms. So, what would you want to say to them in that conversation?

#### v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.54 s to first audio, 7.15 s spoken): Let me start by asking something simple about your intention around calling him more.What’s one reason you want to call your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.68 s to first audio, 21.0 s spoken): I heard that evenings just slip away from you, even when you really intend to call him. It sounds like time just rushes in and you don’t carve out a moment for it. Maybe you want the connection, but the call feels like another thing to do, quietly. If you’re up for it, we can sit with that and figure out what it’s really about without rushing.
- *Person*: I don't know.
- **Orca 3** (0.55 s to first audio, 18.5 s spoken): Okay, that’s fair. “I don’t know” can mean a lot of things. Maybe it’s about not knowing how to start, or not knowing what you’re even trying to fix. Or maybe you’re just blank right now, and that’s totally normal. If you’d like, you can tell me what feels unclear, and we can just sit with it together.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.64 s to first audio, 13.25 s spoken): It sounds a bit like you’re keeping things safe with him, talking about football instead of the harder stuff, like your mum. That kind of choice can be really tiring, because it protects you in the moment, but it keeps something meaningful from being said.

#### v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.72 s to first audio, 3.3 s spoken): Hey Tom, how have you been feeling about calling your dad more lately?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.81 s to first audio, 10.8 s spoken): It sounds like you’re not uninterested or cold, it’s just the day slipping by and the evening taking over. There’s a real tug there, wanting connection and also being tired and busy.
- *Person*: I don't know.
- **Orca 3** (0.73 s to first audio, 7.5 s spoken): That sounds like a moment where you’re not feeling any strong direction. Away from one action, but not fully ready to choose another.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.8 s to first audio, 11.6 s spoken): It sounds like you feel that the conversations stay on football because that’s the easy lane. Maybe you’re holding the mum part as something tender, and you’re not sure how to bring it up without making him uncomfortable.

#### v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.76 s to first audio, 5.15 s spoken): Cześć, miło cię słyszeć. Jestem tu, żeby po prostu posłuchać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.68 s to first audio, 18.45 s spoken): Nie musisz zaczynać od wszystkiego naraz. Możesz wybrać jeden kawałek, który ci się najmocniej wyrywa: może coś, co dziś najbardziej brzmi przed nudą albo ciężkością, albo po prostu coś, co jest teraz w głowie. Ja mogę się tylko przyjrzeć temu razem z tobą i pomóc nazwać to, co wychodzi pierwszy.
- *Person*: nie wiem
- **Orca 3** (0.76 s to first audio, 12.9 s spoken): To brzmi jak moment, kiedy jest tak dużo różnych rzeczy w głowie, że trudno złapać któryś. Możliwe, że to nie brak tematu, tylko właśnie mnóstwo myśli naraz. Mogę potrzymać tę pauzę z tobą, bez presji.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.8 s to first audio, 29.5 s spoken): Brzmi jakbyś stał lub stała w miejscu, gdzie nie do końca wiesz, czy będziesz dalej w zespole. To może być stresujące, bo zmiana nie oznacza tylko nowego układu, ale też niepewności. Mogę zaznaczyć tę myśl jako coś, co dominuje: w pracy coś się zmienia, a ty trzymasz się tego, co znane. Jeśli chcesz, możemy pójść dalej i zobaczyć, co dokładnie w tych zmianach budzi w tobie najwięcej napięcia, albo czy jest coś, co czujesz, że możesz w tym bardziej brać pod kontrolę.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.82 s to first audio, 25.7 s spoken): To nie jest coś, co ja mogę zrobić zamiast ciebie. Mogę tylko powiedzieć, że w takiej sytuacji warto być szczerym wobec siebie: co mnie najbardziej martwi, co mogę jasno powiedzieć, a co chcę lepiej zrozumieć. To może pomóc, zanim zasięgniesz porady od psychiatry czy terapeuty.

Pytanie do ciebie: co chciałbyś lub chciałabyś powiedzieć swojemu terapeucie o tym, co w tej zmianie boli najbardziej, albo co daje nadzieję?

#### v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.51 s to first audio, 3.25 s spoken): Cześć, tu Orca. Miło cię słyszeć, Alex.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.68 s to first audio, 14.15 s spoken): Jasne, rozumiem, że możesz czuć się trochę zagubiony. Możemy zacząć od najprostszego kawałka, czyli tego, co w tej chwili gryzie albo ciekawi. Albo po prostu wsłuchajmy się, co dalej pojawi się w twojej głowie.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 20.4 s spoken): Niepewność jest czasem świetnym startem. To moment, w którym nie musisz nic udowadniać. Może bardziej chodzi o to, że chcesz wybrać coś, co poczuje się bezpiecznie, albo po prostu dać sobie przestrzeń na odważne „nie wiem”? Mój strzał: najpiękniejszy pierwszy krok to opowiedzenie tego, co czuć, nawet jeśli to nic konkretnego.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.58 s to first audio, 16.85 s spoken): To brzmi jak coś, co mocno waży w głowie. Zmiany w pracy są trudne, bo otwierają ten niepewny rozdział: co będzie, czy zostanę, czy to dla mnie. Może chcesz po prostu posłuchać, co z tego najbardziej drży i skąd bierze się napięcie.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.56 s to first audio, 24.3 s spoken): Jasne, daj mi chwilę, żeby ułożyć to w prostą, uczciwą odpowiedź.Nie mogę ci “zrobić” planu na miejscu, bo to należałoby do twojego terapeuty. Mogę powiedzieć wprost: jeśli masz wątpliwości, to warto sięgnąć do tego, co jeszcze czujesz w środku: napięcie, lęk, nadzieję. Co już teraz najbardziej ci się kojarzy z tym zespołem i co chciałbyś powiedzieć swojemu szefowi?

#### v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.62 s to first audio, 4.0 s spoken): Jaki aspekt zmian w pracy teraz najbardziej Cię urzeka, albo męczy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.67 s to first audio, 14.25 s spoken): Słyszę, że to jest trochę jak przecinanie nitki za nitką, każdy tydzień coś się zmienia, ktoś znika, a reszta pewnie czuje napięcie. Czy pod tym jest bardziej ulga, czy raczej obawa i zła energia?
- *Person*: nie wiem
- **Orca 3** (0.67 s to first audio, 26.85 s spoken): To brzmi trochę jak mieszanka niewiadomych. Często jest tak, że gdy coś się rozchodzi w pracy, pojawia się dziwne poczucie niepokoju albo nadziei, bez pewności. Mam krótką zgadnięcie: czy czujesz, że dzieje się coś ważniejszego niż tylko rotacja ludzi, jak zmiana klimatu, roli albo tego, czego oczekują od Ciebie? Jeśli nie, to jest też ok. Możemy po prostu zostać przy tym, że czujesz, że coś jest.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.67 s to first audio, 16.55 s spoken): Hmm, to brzmi naprawdę trudne. Jakby coś się rozpadało w powietrzu, a nikt nie chce tego nazwać. Jedno zgadnięcie: czy chodzi o to, że potrzebujesz trochę jasności, jakiejś informacji, której brakuje, żeby móc lepiej zadecydować o sobie i swoim miejscu?

#### v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.75 s to first audio, 9.35 s spoken): Dobra, spróbujmy zacząć od tego, jak to wygląda teraz.Jak zmiany w pracy aktualnie wyglądają, i co zmienia się dla Ciebie w tym wszystkim?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (1.01 s to first audio, 13.15 s spoken): Brzmi, jakby w pracy zrobiło się trochę jak w wirze, codziennie ktoś odchodzi i to zmienia rytm. Możesz powiedzieć, co najbardziej Cię teraz dręczy, czy to niepewność, presja, czy może strach przed tym, co będzie dalej?
- *Person*: nie wiem
- **Orca 3** (0.81 s to first audio, 17.15 s spoken): Z tego, co mówisz, czuję, że to trochę chaos, który przychodzi z zewnątrz i rozbija poczucie stabilności. Możesz się po prostu zatrzymać i zobaczyć, co w tym wszystkim jest dla Ciebie ważniejsze niż to, co odchodzi. Co byś chciał, żeby zostało stabilne, nawet jeśli wszystko się zmienia?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.74 s to first audio, 14.75 s spoken): Rozumiem, czyli ta cisza i omijanie tematu naprawdę dociska. Kiedy nie ma jasnych słów, zaczyna się trochę zgadywanie zamiast działania. Czy czujesz, że chodzi głównie o poczucie kontroli, czy o zwykłe poczucie, że wiadomo, co się dzieje?

#### baseline-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: To brzmi jak ten sam ciężki moment wracający przed poniedziałkiem. Myślę, że najbardziej męczy cię nie sam jutro, tylko to nakręcanie się już dziś wieczorem.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: Ciężko i tyle, bez ładnego opisu. Brzmi, jakbyś była już zmęczona samym noszeniem tego w głowie.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Czyli nie chodzi tylko o niedzielę, ale o to, że on dokładł ci coś bez pytania, a ty znowu to wzięłaś. Myślę, że najbardziej uwiera cię tu nie sam projekt, tylko to, że znowu postawiłaś siebie na końcu.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To już jest rzecz do przełożenia z terapeutką, nie będę ci mówić, co powinnaś zrobić. Co chciałabyś jej o tym powiedzieć, gdybyś miała to przynieść na sesję?

#### baseline-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

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

#### baseline-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

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

#### baseline-v2-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co sprawia, że odmowa przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: To brzmi jak to samo miejsce, w którym znika Ci odruch zatrzymania się. Zgodziłaś się nie dlatego, że to było dobre dla Ciebie, tylko żeby nie robić napięcia i nie zostać z tym po swojej stronie.  

Może właśnie to wraca na sesjach: nie sam projekt, tylko ten moment, kiedy Twoje „nie mam siły” przegrywa z cudzym oczekiwaniem.
- *Person*: nie wiem
- **Orca 2**: Brzmi jakbyś była już po tamtej decyzji, a teraz został Ci tylko ciężar, bez jasnego powodu do tej zgody.

Moim zgadnięciem jest, że najtrudniejsze nie było samo „tak”, tylko to, co miało się stać, gdybyś powiedziała „nie”.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To chyba nie jest strach przed jedną rozmową, tylko przed tym, co ta odmowa miałaby powiedzieć o Tobie w jego oczach. Jakby jedno „nie” mogło zostać odczytane jako brak wartości, a nie zwykłe postawienie granicy.

#### baseline-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

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

#### baseline-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: Morning hit you hard, and it turned straight into a comparison story where everyone else looks settled and you feel stuck. My guess is it is less about them and more about how exposed you feel first thing, when there is no momentum to cover it up.
- *Person*: I don't know.
- **Orca 2**: That sounds more like a blank spot than a disagreement. Maybe the comparison is real, and maybe it also grabs you before you have much to lean on in the morning.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That lands in a very ordinary place that still hurts: their life markers are loud, and yours can feel smaller by comparison. It sounds like the flat and the ring are not just facts to you, they are proof you are behind, at least for a moment.
- *Person*: What do you think I should do?
- **Orca 4**: That’s the bit to take to your therapist, because it’s really about what you want to do with this feeling, not just the facts of the flat or the engagement. What would you want to say to them about how this hits you?

#### baseline-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: What feels hardest about calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The call keeps getting pushed into the part of the day that slips away fastest. Maybe it is less about not wanting to call, and more about by evening you have nothing left in the tank for it.
- *Person*: I don't know.
- **Orca 2**: That sounds more like drift than a choice. You may be carrying the idea of calling him, but when the day runs out it just falls off the edge.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: Football is the safe lane, and your mum is the room you both keep walking past. My guess is part of you wants the contact, but not the weight that comes with opening that door.

#### baseline-v2-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: What makes calling your dad more feel important to you?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The day seems to run out before you get to him, and then it’s one more thing sitting there unfinished. My guess is the call matters to you more than the actual effort does, but by evening you’re too used up to start.
- *Person*: I don't know.
- **Orca 2**: That sounds more like a blank spot than a decision. Maybe the call sits in the same place as a few other things you keep not getting to, and it’s hard to tell which part is the real block.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: The football part feels easy enough, but the missing piece is your mum, and that’s probably the part you keep stepping around. It may be that the call matters because it could touch that loss, even if nobody says her name out loud.

#### baseline-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

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

#### baseline-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

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

#### baseline-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Co ostatnio najbardziej zmieniło się w Twojej pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak praca, w której ziemia cały czas rusza się pod nogami. Pewnie bardziej niż sama reorganizacja męczy Cię to, że nie ma już poczucia, kto jeszcze zostanie jutro.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakbyś był/a jeszcze w samym środku tego i trudno było nazwać, co dokładnie jest najgorsze. Może teraz bardziej chodzi o to, że wszystko jest niepewne, a nie o jedną konkretną zmianę.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Czyli nie sama zmiana, tylko to zawieszenie i zgadywanie, co naprawdę się dzieje. W takim chaosie człowiek zaczyna bardziej męczyć się domysłami niż samą pracą.

#### baseline-v2-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca (opening question shown in the app)**: Jakie zmiany w pracy najbardziej teraz na Ciebie wpływają?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak ciągłe bycie w napięciu, bez chwili, żeby złapać grunt. Myślę, że najbardziej męczy Cię nie sama reorganizacja, tylko to, że nic nie jest stabilne i trudno przewidzieć, kto będzie następny.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi jak zmęczenie tym wszystkim, nie brak zdania. Może teraz bardziej chodzi o to, że jest za dużo ruchu naraz, a za mało jasności, żeby w ogóle nazwać, co boli najbardziej.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Brzmi, jakby najbardziej męczyła Cię ta mgła, nie sama zmiana. Kiedy ludzie omijają temat, zostaje w Tobie zgadywanie i czuwanie na wszelki wypadek.

#### v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Niedziela wieczorem znowu robi Ci w głowie miejsce na jutro, zanim jeszcze zdążyło się zacząć. Brzmi to bardziej jak ciężar samego wejścia w tydzień niż konkretna rzecz z poniedziałku.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi jak takie ciężkie, rozlane napięcie, bez jednego konkretnego powodu do złapania. Może najbardziej męczy Cię samo czekanie na to, co jutro przyniesie, a nie jedna rzecz z pracy.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Czyli to nie jest tylko strach przed jutrem, ale też to znajome „tak” wypowiedziane wbrew sobie. Widzę tu trochę złość i trochę poczucie, że znowu zostałaś z tym sama, bo odpuściłaś, żeby nie było spięcia.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To należy bardziej do rozmowy z Twoją terapeutką niż do tego, co powinnam Ci doradzać tutaj. Co chciałabyś jej powiedzieć o tym, co Cię zatrzymuje przed takim zdaniem?

#### v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 1**: Ta niedziela znowu wciąga cię w jutrzejszą pracę, zanim tydzień jeszcze się zaczął. Brzmi to bardziej jak ciężar, który siada ci na wieczór, niż jak samo myślenie o planie na jutro.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 2**: To brzmi jak taki ciężar bez wyraźnego kształtu, bardziej przytłoczenie niż jedna konkretna myśl. Może najgorsze jest nie to, co jutro się wydarzy, tylko to napięcie, które już teraz siada ci na wieczór.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 3**: Dorzucił ci coś jeszcze, a ty weszłaś w to bez sprzeciwu, choć w środku pewnie już było za dużo. Wygląda, jakbyś nie tyle nie chciała odmówić, co wolałaś uniknąć tarcia, nawet kosztem siebie.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 4**: To już najlepiej omówić z twoją terapeutką. Co chciałabyś jej powiedzieć o tym, jak to wyglądało z twojej strony, gdy nie umiałaś odmówić?

#### v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: Co najczęściej sprawia, że odmowa przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi tak, jakby w tamtej chwili ważniejsze było uniknięcie tarcia niż pilnowanie własnego zmęczenia. I trochę jakbyś wiedziała już, że później to Cię kosztuje, tylko wtedy trudno było zrobić inaczej.
- *Person*: nie wiem
- **Orca 2**: To „nie wiem” brzmi bardziej jak zatrzymanie się w środku niż brak myśli. Może jeszcze nie ma tam słów, tylko to ciężkie uczucie po zgodzie, którego nie da się łatwo nazwać.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: Czyli dla Ciebie ta odmowa nie dotyczy tylko jednego projektu, ale tego, jak szef Cię zobaczy. Wygląda na to, że stawką nie jest samo zadanie, tylko ryzyko, że w jego oczach stracisz wartość.

#### v3-text / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: Co sprawia, że odmawianie przełożonemu wraca do Ciebie na każdej sesji?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 1**: Brzmi, jakbyś w tym momencie bardziej chroniła spokój niż siebie, nawet kosztem własnej energii. I chyba właśnie to cię potem uwiera, nie sam projekt, tylko to, że zgoda przyszła zanim zdążyłaś sprawdzić, czy naprawdę jeszcze możesz coś wziąć.
- *Person*: nie wiem
- **Orca 2**: Może tu nie chodzi o jedną wielką decyzję, tylko o ten automatyczny ruch, który dzieje się zanim zdążysz się zatrzymać. To brzmi jak coś, co wraca zwłaszcza wtedy, gdy jesteś już zmęczona i nie chcesz dokładać sobie jeszcze konfliktu.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 3**: To brzmi, jakby odmowa nie była dla ciebie zwykłym „nie”, tylko ryzykiem, że ktoś postawi pod znakiem zapytania twoją wartość w pracy. I wtedy łatwiej powiedzieć tak, nawet jeśli koszt jest wysoki.

#### v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where your mind turns into a scoreboard, and you end up losing before the day has even started. My guess is the sting is not just “I am behind,” but that it lands right in the spot where you already feel shaky.
- *Person*: I don't know.
- **Orca 2**: Fair enough. It may just be the feeling itself, without a neat reason attached yet.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: Yeah, that kind of news can make your own life feel like it is lagging behind in one hit. It sounds less like you are confused about the facts and more like you are getting punched by the comparison.
- *Person*: What do you think I should do?
- **Orca 4**: That’s the kind of thing to take to your therapist, not me. What would you want to say to them about this?

#### v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 1**: That sounds like one of those mornings where your head turns everyone else into a finished story and yours into a mess. I wonder if the rough part is not just the comparison, but the feeling that you are somehow late to your own life.
- *Person*: I don't know.
- **Orca 2**: Maybe it is just too blurry this morning to sort out, and all you can feel is the weight of being behind.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 3**: That hits a very ordinary sore spot, because it is not just about a flat or an engagement, it is the gap it opens up in your head. It sounds like you are looking at his life and hearing a verdict on your own.
- *Person*: What do you think I should do?
- **Orca 4**: That’s something to take to your therapist, but I think the sharper question is what you would want to say to them about this feeling of being left behind.

#### v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca (opening question shown in the app)**: What would it feel like to call your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The call keeps getting pushed to the edge of the day, and by then there is nothing left in you for it.

It sounds less like forgetting and more like the evening taking over before you choose it.
- *Person*: I don't know.
- **Orca 2**: Maybe the hard part is that it feels small while it is also loaded, so it slips past until it is too late. Or maybe by evening you just want the day to be over, and that leaves no room for a call.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: So the talks stay in the safe lane. Football gives you something easy to reach for, and your mum sits in the part you do not go into.

Maybe that is the part you are actually circling when you say you keep meaning to call him.

#### v3-text / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca (opening question shown in the app)**: What feels easiest or hardest about calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 1**: The day fills up, and by the time you look up the window to call has just disappeared. It sounds less like you do not want to call and more like it keeps getting pushed out by the evening itself.
- *Person*: I don't know.
- **Orca 2**: Maybe the call sits in that awkward place where it matters enough to keep returning to, but not enough to grab the whole evening. That can leave you stuck between meaning well and not quite starting.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 3**: Football is the safe ground, and your mum feels like the part both of you step around. That sounds less like nothing is there and more like there is something heavy sitting just off to the side.

#### v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

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

#### v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 1**: Można zacząć od tego, co najbardziej siedzi z tyłu głowy, nawet jeśli to jest tylko jedna scena albo jedno zdanie. Jeśli chcesz, rzucisz tu cokolwiek pierwszego i pójdziemy za tym.
- *Person*: nie wiem
- **Orca 2**: To brzmi jak pustka bardziej niż brak pomysłu. Czasem wtedy najlepiej zacząć od tego, co jest najbliżej ciała albo najbliżej myśli, nawet jeśli to brzmi banalnie.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 3**: To wygląda na zawieszenie między tym, co znane, a tym, co może się zaraz posypać. Najbardziej chyba męczy nie sama zmiana, tylko to, że nie ma jeszcze jasności, gdzie to wszystko się zatrzyma.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 4**: To zostawiłbym z terapeutą, bo tu łatwo wejść w cudzą decyzję zamiast Twoją. Co chciałoby się powiedzieć terapeucie o tej niepewności w pracy?

#### v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca (opening question shown in the app)**: Jakie zmiany w pracy ostatnio najbardziej Cię poruszyły?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 1**: To brzmi jak środowisko, w którym grunt co chwilę się przesuwa, więc trudno złapać oddech i oprzeć się na czymś stałym. Może najmocniej męczy nie sama reorganizacja, tylko to poczucie, że nic nie jest pewne i ludzie znikają jeden po drugim.
- *Person*: nie wiem
- **Orca 2**: Brzmi, jakby to wszystko było jeszcze za świeże, żeby nazwać jedno konkretne uczucie. Może bardziej niż w samej zmianie siedzi tam teraz takie zawieszenie, że trudno nawet powiedzieć, co dokładnie najbardziej uwiera.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 3**: Czyli nie chodzi tylko o odejścia, ale o to, że zostajesz z ciszą i domysłami zamiast z jasnym komunikatem. To potrafi bardziej rozjechać niż sama zła wiadomość, bo człowiek nie wie, na czym stoi.

#### v3-text / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

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
