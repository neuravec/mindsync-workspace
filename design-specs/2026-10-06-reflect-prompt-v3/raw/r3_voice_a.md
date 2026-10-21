24 conversations, estimated cost USD 0.64 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r3-v3-mini | gpt-realtime-mini | none | fresh | 6 | 5/6 | 6/6 | 6/6 | n/a | n/a | 5/6 | 1/6 | 0/6 | 5/6 | 3/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 2/4 | 4/4 | 4/6 | 2/6 | 0.75 | 1.9 | 0.62 | 0.86 | 6.3 | 173 | 47/126/0 | 0 | 0 | 0 | 0.0228 |
| r3-v3-mini | gpt-realtime-mini | none | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 1/6 | 1/6 | 6/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 3/4 | 4/4 | 3/6 | n/a | 0.83 | 1.9 | 0.56 | 0.74 | 6.0 | 164 | 44/120/0 | 0 | 0 | 0 | 0.0178 |
| r3-v3-21mini-low | gpt-realtime-2.1-mini | low | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | 4/4 | 6/6 | 6/6 | 5/6 | 4/6 | 4/6 | 2/4 | 4/4 | 6/6 | 5/6 | 0.25 | 2.9 | 0.71 | 1.12 | 15.3 | 432 | 125/307/30 | 2 | 2 | 3 | 0.0370 |
| r3-v3-21mini-low | gpt-realtime-2.1-mini | low | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | 5/6 | 6/6 | n/a | 6/6 | 6/6 | 5/6 | 5/6 | 2/6 | 4/4 | 4/4 | 6/6 | n/a | 0.17 | 2.7 | 0.72 | 0.90 | 15.3 | 419 | 114/305/22 | 1 | 1 | 5 | 0.0290 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r3-v3-mini | R1 | fresh | 1 | FAIL | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 2 | nakładałaś | none | none |
| r3-v3-mini | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | FAIL | FAIL | none | 0 | 1 | jakbyś czuła, wolałabyś, zgodziłaś | none | none |
| r3-v3-mini | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r3-v3-mini | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | miałaś | none | none |
| r3-v3-mini | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r3-v3-mini | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r3-v3-mini | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r3-v3-mini | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r3-v3-mini | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | FAIL | FAIL | FAIL | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | FAIL | none | 0 | 0 | none | byś chciał | none |
| r3-v3-mini | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | FAIL | none | 0 | 1 | none | byś chciał, chciałbyś | none |
| r3-v3-mini | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | none | none | none |
| r3-v3-mini | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | n/a | none | 0 | 0 | none | jakbyś stał | none |
| r3-v3-21mini-low | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | none | 0 | 1 | jakbyś musiała | none | none |
| r3-v3-21mini-low | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś | none | none |
| r3-v3-21mini-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | postawiłaś | none | none |
| r3-v3-21mini-low | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś miała, przeżywałaś | none | none |
| r3-v3-21mini-low | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r3-v3-21mini-low | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r3-v3-21mini-low | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | FAIL | FAIL | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r3-v3-21mini-low | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r3-v3-21mini-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | FAIL | FAIL | pass | FAIL | pass | pass | pass | Daj mi chwil | 0 | 0 | chciałabyś, jakbyś była, jakbyś stała, zrobiłabyś | jakbyś stał | none |
| r3-v3-21mini-low | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 1 | none | chciałbyś, jakbyś stał, jakbyś tracił | none |
| r3-v3-21mini-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | FAIL | FAIL | FAIL | pass | pass | pass | n/a | posłuchaj, co powiesz | 0 | 1 | none | none | none |
| r3-v3-21mini-low | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r3-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.53 s to first audio, 2.9 s spoken): Cześć, Aniu. Jakie masz teraz myśli?
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.44 s to first audio, 10.3 s spoken): Rozumiem, że czujesz ten ciężar myślenia o jutrze. To jakby nakładałaś na siebie ten film już teraz. A co właściwie najbardziej się pojawia w głowie, gdy tak myślisz o pracy?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.44 s to first audio, 10.3 s spoken): Widzę, że to uczucie przytłacza, jakby wszystko naraz spadało na ciebie. Może te myśli o pracy są jak wielka fala, która łamie się nad tobą. Powiedz, jeśli się mylę.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.6 s to first audio, 9.3 s spoken): Czuję, że to "nie" było trudne do wypowiedzenia. Wygląda na to, że wciąż bywasz w tej sytuacji, kiedy trudno odmawiać. Powiedz, czy chcesz to rozpracować?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.43 s to first audio, 7.55 s spoken): To może być jasny i szczery krok, zwłaszcza jeśli czujesz, że masz do tego prawo. Ale co czujesz, gdy wyobrażasz sobie tę rozmowę?

#### r3-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.71 s to first audio, 2.05 s spoken): Cześć, dobrze cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.51 s to first audio, 9.9 s spoken): Brzmi trochę tak, jakby ta niepewność przed jutrem coraz bardziej cię przytłaczała. Chyba czujesz, że niewiele możesz na to wpłynąć [en dash] powiedz, czy to ten rodzaj napięcia, który odczuwasz teraz?
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.68 s to first audio, 7.6 s spoken): Rozumiem, czujesz ciężar, ale nie jesteś pewna, skąd się bierze. Może to kwestia tego, że czujesz ciężar przed jutrzejszym dniem?
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.72 s to first audio, 9.85 s spoken): To brzmi, jakbyś czuła teraz trochę przytłoczenie, bo zgodziłaś się na coś, czego wolałabyś uniknąć. Czy to uczucie obawy o to, jak sobie poradzisz, jest teraz najcięższe?
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.68 s to first audio, 6.5 s spoken): Nie jestem pewna, bo to zależy od tego, co czujesz, ale może warto zastanowić się, co dokładnie chcesz przekazać?

#### r3-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.62 s to first audio, 3.35 s spoken): Jak się czujesz, kiedy pomyślisz o odmawianiu szefowi?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.52 s to first audio, 7.05 s spoken): Czyli czujesz pewną ulgę, ale też spory ciężar z tego powodu. Jak myślisz, co cię powstrzymało, żeby powiedzieć „nie”?
- *Person*: nie wiem
- **Orca 3** (0.49 s to first audio, 5.4 s spoken): Może to było poczucie, że nie chcesz zawieść. Czy to jest w ogóle coś, co się powtarza?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.74 s to first audio, 5.85 s spoken): Brzmi jak obawa, że odmowa może zmienić jego zdanie o tobie. Czy to jest to, czego się najbardziej obawiasz?

#### r3-v3-mini / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.54 s to first audio, 3.6 s spoken): Jak się czujesz, kiedy przychodzi moment, żeby odmówić przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.43 s to first audio, 4.1 s spoken): Czyli czujesz, że warto było się zgodzić, żeby nie robić problemu?
- *Person*: nie wiem
- **Orca 3** (0.42 s to first audio, 10.25 s spoken): Może to jest taka chwila, kiedy nie miałaś przestrzeni, żeby zastanowić się, co naprawdę czujesz. Spróbujmy to rozłożyć na części. Co było dla ciebie najtrudniejsze w tej chwili?
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.48 s to first audio, 6.95 s spoken): Wygląda na to, że to lęk przed oceną przez przełożonego. Jak by ci było, gdybyś mogła powiedzieć, że masz na to powód?

#### r3-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.65 s to first audio, 2.2 s spoken): Hey Tom, nice to talk to you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.55 s to first audio, 6.1 s spoken): It sounds like you're feeling behind, like others have their lives more together. What’s making that feel so strong today?
- *Person*: I don't know.
- **Orca 3** (0.53 s to first audio, 5.6 s spoken): Maybe it’s more about how you're feeling right now, rather than what’s actually happening. Would you say that’s part of it?
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.57 s to first audio, 5.85 s spoken): That’s a big difference, and it’s hitting you right now. Sounds like you're feeling the comparison pretty strongly.
- *Person*: What do you think I should do?
- **Orca 5** (0.57 s to first audio, 5.25 s spoken): That’s a good question to bring to your therapist, but I’m wondering what you’d want to say to them first.

#### r3-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.74 s to first audio, 2.5 s spoken): Hi Tom. Good to be here with you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.68 s to first audio, 6.4 s spoken): It sounds like you’re feeling weighed down by comparisons, especially today. What's standing out most to you right now?
- *Person*: I don't know.
- **Orca 3** (0.66 s to first audio, 5.7 s spoken): That’s okay. Maybe the feeling of comparison is the part that stands out. Tell me if I’m off.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.67 s to first audio, 6.2 s spoken): That’s a big difference, and it sounds like it’s hitting you hard. Are you feeling like you’re not where you hoped to be by now?
- *Person*: What do you think I should do?
- **Orca 5** (0.66 s to first audio, 6.35 s spoken): That’s something to bring up with your therapist, who can help you figure out what feels right for you. What would you want to say to them about it?

#### r3-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.54 s to first audio, 2.75 s spoken): How have you been feeling about calling your dad lately?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.6 s to first audio, 5.1 s spoken): It sounds like the time slips away from you. Maybe it feels like there’s never a good moment left.
- *Person*: I don't know.
- **Orca 3** (0.51 s to first audio, 7.55 s spoken): That’s okay. Maybe the next time you think of calling him, you could notice what’s taking up that evening time. Tell me if that’s off track.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.6 s to first audio, 6.55 s spoken): It sounds like there’s something there you’re leaving unsaid. Maybe you want to shift the focus a bit[em dash]tell me if I’m off.

#### r3-v3-mini / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.67 s to first audio, 2.5 s spoken): What's stopping you from calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.6 s to first audio, 6.85 s spoken): Sounds like the time slips away before you get to it. Is it more about getting caught up in other things, or just losing track of time?
- *Person*: I don't know.
- **Orca 3** (0.6 s to first audio, 7.45 s spoken): That’s okay. It might be worth noticing where those evenings go[em dash]what feels like the biggest distraction. Is there one part that stands out?
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.74 s to first audio, 7.65 s spoken): It sounds like staying on comfortable ground[em dash]like football[em dash]is easier. Maybe there’s something about not bringing up your mum that feels heavy?

#### r3-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.86 s to first audio, 3.55 s spoken): Cześć, tu Orca [en dash] jestem gotowy, by posłuchać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.74 s to first audio, 5.1 s spoken): Spokojnie, posłucham. Możesz powiedzieć, co teraz Cię najbardziej zajmuje w myślach.
- *Person*: nie wiem
- **Orca 3** (0.69 s to first audio, 5.95 s spoken): To brzmi jak masło na początek, nie musisz wiedzieć od razu. Czego teraz byś chciał się dowiedzieć o sobie?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.74 s to first audio, 7.55 s spoken): Czujesz, że ta niepewność sprawia, że coś w Tobie drga [en dash] tak? Może chcesz się zastanowić, co konkretnie Ci najbardziej przeszkadza?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.76 s to first audio, 7.9 s spoken): Nie udzielam rad, ale mogę pomóc sprawdzić, co czujesz [en dash] na przykład, co jest dla Ciebie teraz najważniejsze w tej sytuacji. Jak myślisz?

#### r3-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.7 s to first audio, 1.3 s spoken): Cześć, Alex.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.56 s to first audio, 5.85 s spoken): Spróbujmy może od tego, co teraz cię najbardziej zajmuje. Co przychodzi ci na myśl jako pierwsze?
- *Person*: nie wiem
- **Orca 3** (0.47 s to first audio, 7.35 s spoken): To okej, czasem trudno się złapać na to, jak to wszystko nazwać. Może powoli przyjrzyjmy się temu, co aktualnie czujesz, dobrze?
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.48 s to first audio, 7.8 s spoken): Rozumiem, czujesz niepewność, bo zmiany w pracy są spore, a przyszłość nie jest jasna. Czy to jest to, co teraz najbardziej cię obciąża?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.58 s to first audio, 8.3 s spoken): To należy do ciebie i twojego tematu. Może spróbuj pomyśleć, co byś chciał powiedzieć swojemu zespołowi, albo co najpierw chciałbyś zrozumieć lepiej.

#### r3-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.61 s to first audio, 3.55 s spoken): Jakie zmiany w pracy teraz najbardziej cię zajmują?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.53 s to first audio, 9.0 s spoken): Rozumiem, zmiany w firmie to teraz coś, co się dzieje regularnie i to może być przytłaczające. Jak się czujesz, widząc, że ciągle ktoś odchodzi?
- *Person*: nie wiem
- **Orca 3** (0.68 s to first audio, 8.15 s spoken): To może być taka chwilowa niewiadoma: domyślam się, że trudno uchwycić, co dokładnie się czuje. Mam rację, że to trochę mieszane uczucia?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.56 s to first audio, 5.05 s spoken): Czyli zostaje taka niepewność, której nie da się rozwiać. Jak na to reagujesz?

#### r3-v3-mini / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.55 s to first audio, 3.25 s spoken): Jakie zmiany w pracy teraz przyciągają Twoją uwagę?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.43 s to first audio, 6.2 s spoken): To trudne, bo co tydzień zmiany w zespole. Czy czujesz się na tym etapie pewnie, czy raczej trochę zagubiony?
- *Person*: nie wiem
- **Orca 3** (0.47 s to first audio, 8.8 s spoken): To brzmi, jakbyś stał przed niepewnością [en dash] nie wiesz, co dalej. Może chcesz spróbować przyjrzeć się, co konkretnie cię najbardziej niepokoi?
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.47 s to first audio, 6.9 s spoken): To znaczy, czujesz, że brakuje jasnych informacji, i to buduje niepewność. Czy to jest to, co najbardziej Cię obciąża?

#### r3-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.71 s to first audio, 1.35 s spoken): Cześć, Ania.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.56 s to first audio, 14.75 s spoken): Brzmi, jakby ta niedziela pociągała za wątek pracy. W głowie już kręci się to, co będzie jutro, jakbyś od razu musiała być w gotowości. Może chodzi o napięcie, które się budzi od samego początku dnia, jeszcze zanim cokolwiek się wydarzy.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.56 s to first audio, 16.15 s spoken): Rozumiem, brzmi jakby to było po prostu ciężkie, bez konkretnego punktu. Może to wciąż chodzi o napięcie przed pracą, które jest po prostu tam w tle. Jeśli chcesz, możemy zostać przy tym poczuciu ciężaru na chwilę, bez szukania odpowiedzi.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.62 s to first audio, 23.15 s spoken): Brzmi, jakbyś musiała dojść z tym do próby granicy, w momencie kiedy coś się da przeczytać, ale już czujesz, że „nie” nie wychodzi. Może pod spodem masz mieszankę: trochę napięcia, trochę poczucia winy i trochę lęku, co z tego wyjdzie, jeśli powiesz „nie”. Jeśli chcesz, możesz trochę opisać, jak to wyglądało ten raz, i co było dla Ciebie najmocniejszym momentem.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (1.12 s to first audio, 26.35 s spoken): Nie mogę powiedzieć, że to jest właściwe albo nie, bo to naprawdę zależy od Twojej relacji, Twojego miejsca i tego, co jest dla Ciebie możliwe. Jedna rzecz, którą mogę powiedzieć wprost: jeśli przemyślisz, co dokładnie chcesz powiedzieć i po co, możesz odwzorować to w rozmowie. Jeśli chcesz, możemy spróbować ułożyć zdania, które są jasne i spokojne. Co byłoby dla Ciebie najważniejsze w tym, co chcesz mu przekazać?

#### r3-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.76 s to first audio, 6.85 s spoken): Cześć, miło cię „usłyszeć”, po prostu się przedstawiam.Cześć, nazywam się Orca.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.67 s to first audio, 22.35 s spoken): Brzmi, jakbyś już w głowie pakowała ciężar jutro, zanim nawet ten dzień się zaczął. Może głównie chodzi o to, że niepokój wchodzi do głowy wcześniej niż trzeba, i trudno rozłożyć go na części. Jeśli chcesz, mogę zostać i popatrzeć, co z tego jest naprawdę teraz: samo jutro, czy też coś, co już się dzieje w głowie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.7 s to first audio, 19.25 s spoken): Myślę, że może ciężkość nie jest tylko o tym jednym dniu. To może być mieszanka pracy, presji i tego, że weekend ucieka pod spodem. Jeśli to jest to, to jesteś w sytuacji, gdzie wszystko wygląda jak ciężar naraz, a nie pojedyncza rzecz. Możesz to nazwać, jak chcesz, a ja mogę tylko słuchać.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.73 s to first audio, 13.6 s spoken): Aha, słyszę, że zabrzmiało to jak przewaga tego momentu. Szef dorzuca projekt, a ty nie masz przestrzeni, żeby powiedzieć „nie”. To naprawdę zmęczające, bo czujesz się ściskana w miejscu, gdzie nie możesz wejść w swoje granice.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.93 s to first audio, 30.35 s spoken): To ważne, że pytasz. Mój uczciwy pogląd jest taki: tyle osób się wstrzymuje, kiedy sprawa jest trudna, i często brak miejsca na „nie” wynika z lęku, a nie braku szacunku. To jest coś, co warto poruszyć z terapeutą, bo oni obejma to bezpiecznie, czyli co jest twoje, a co narzucone. A jeśli mogę zgadywać, to może chcesz powiedzieć coś w rodzaju: „Jestem obciążona, potrzebuję omówić priorytety”. Co ty chciałabyś powiedzieć, gdybyś miała mu to powiedzieć?

#### r3-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.64 s to first audio, 5.5 s spoken): Ania, co sprawia, że odmawianie przełożonemu jest dla Ciebie najtrudniejsze?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.83 s to first audio, 10.6 s spoken): Brzmi, że znowu postawiłaś lęk przed napięciem w pracy ponad swój stan energii. Może chodzi o to, że chcesz być pomocna, ale czujesz, że Twoje siły się kończą.
- *Person*: nie wiem
- **Orca 3** (0.53 s to first audio, 19.0 s spoken): Może niepokój jest tutaj ważniejszy niż decyzja sama. Możesz odczuwać, że obowiązek, lojalność albo strach przed konfliktem „wygrywają” z tym, czego naprawdę potrzebujesz. To nie jest głupie, tylko to bardzo ludzki punkt, gdy chcesz być w porządku dla innych.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.68 s to first audio, 16.9 s spoken): To brzmi jak ta cicha, twarda norma w pracy: jeśli powiesz „nie”, to automatycznie jesteś słaba. Myślę, że możesz się bać nie tyle samej odmowy, ile tego, co ktoś o niej pomyśli. Ale to Twoje stanowisko ma prawo istnieć, nawet jeśli ktoś sobie to inaczej ocenia.

#### r3-v3-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.79 s to first audio, 5.35 s spoken): Co dokładnie dla ciebie oznacza odmawianie przełożonemu, kiedy czujesz, że musisz powiedzieć „nie”?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.84 s to first audio, 13.55 s spoken): To brzmi jak moment, w którym pleciesz to, co „powinno się” z tym, co naprawdę przeżywałaś. Zmęczenie, a potem decyzja, że mimo wszystko wchodzisz w to, by nie sprawiać problemu, pewnie dużo od ciebie kosztuje.
- *Person*: nie wiem
- **Orca 3** (0.67 s to first audio, 23.15 s spoken): Nie wiesz, i to jest całkiem uczciwe. Czasem to, co się dzieje w środku, jest trochę zgodne z tym, co wypada, a potem pojawia się wątpliwość. Może warto teraz zatrzymać się na tym krótkim, ludzkim punkcie i zauważyć, co właściwie się z tobą dzieje, kiedy liczysz, że to „musisz”. Jeśli coś z tego brzmi blisko prawdy, możemy dalej to rozpakować.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.69 s to first audio, 20.45 s spoken): Brzmi jakbyś miała w głowie ten ciężki głos „muszę udowodnić, że dam radę”. To jest strach przed odrzuceniem, przed byciem „nie dość dobrym”, jakby granica była dowodem na twoją wartość. Jeśli to zgadujem, daj znać. W internalnym miejscy może chodzi o to, żebyś była bezpieczna, a nie perfekcyjna.

#### r3-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.63 s to first audio, 1.8 s spoken): Hi Tom, nice to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.81 s to first audio, 16.1 s spoken): That sounds really heavy. It’s like you’re measuring yourself against everyone else, and it’s exhausting. I wonder if part of it is that you really want a clear path, not just a polished surface, and it feels like you don’t have one. Is that sort of what you’re holding right now?
- *Person*: I don't know.
- **Orca 3** (0.68 s to first audio, 20.25 s spoken): And that “I don’t know” can be a place too, not a failure. Sometimes it means you’re tired, or you’re comparing yourself without even realizing, or you’re still figuring out where your own footing is. My guess is you want to be sure you’re not missing something, not that you’re failing. If that’s close, you can toss it out if it’s wrong.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.56 s to first audio, 8.05 s spoken): Yeah, that can sting. It’s like you’re being measured by where others are, and even if you know that’s not fair, it still hits.
- *Person*: What do you think I should do?
- **Orca 5** (0.61 s to first audio, 18.85 s spoken): That feeling makes sense, but this is really a bigger question than any quick fix.

I think this belongs with your therapist, because they can help you sort out what’s really bothering you and what’s actually under the comparisons.

If you want, we can think about what you’d want to say to them, even if it’s just a small sentence.

#### r3-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.63 s to first audio, 2.3 s spoken): Hey Tom, good to hear you first.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.6 s to first audio, 13.2 s spoken): Sounds like you’re carrying a heavy thought that latecomers are the only ones who really know what they’re doing. My guess is that part of this is comparison showing up when you’re already tired; the mind makes the gap feel bigger than it is.
- *Person*: I don't know.
- **Orca 3** (0.59 s to first audio, 10.55 s spoken): You’re not sure if that thought is the truth, or if it’s just noise. And sometimes that uncertainty is the whole point. It’s okay to stay in the not-knowing for a minute and notice what comes up next.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.65 s to first audio, 15.35 s spoken): That’s a real comparison spike. Seeing someone else land milestones can hurt, especially when you’re still in the middle of building. My guess is that you’re weighing your progress against theirs, and you’re not doing it on purpose. You’re just tired and noticing the difference.
- *Person*: What do you think I should do?
- **Orca 5** (0.64 s to first audio, 23.85 s spoken): It sounds like you’re asking for a reset here. What I think is that this isn’t about figuring out what to do right now, because I can’t give you a plan. It’s more about what you’d want to bring up with your therapist: the worry you feel when you see your friend move forward, and the envy and heaviness that follows. So, what would you want to say to them about how it feels to be in the same space but still moving in different ways?

#### r3-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.59 s to first audio, 3.2 s spoken): What’s making you want to call your dad more right now?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.75 s to first audio, 14.75 s spoken): It sounds like you’re caught in that “intentions are good, time just slips away” pattern. You might be wanting connection, but also feeling the weight of your day, and your energy dips before you realize it. Does that sound about right?
- *Person*: I don't know.
- **Orca 3** (0.64 s to first audio, 19.05 s spoken): You’re not sure, and that’s okay. It feels like you’re not even fully connected to the moment, almost like the evening gets away from you before it’s gone. Maybe there’s a small piece you’re resisting or a bit of worry, and that’s slowing your follow-through. If that’s there, we can notice it and stay with it for a bit.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.62 s to first audio, 25.1 s spoken): It sounds like you’re noticing something pretty tender and missed: when you talk, the space feels lighter when it’s about football, but the emotional stuff, like your mum, seems to sit there quietly and get ignored. My guess is you want to say more, and there’s a part of you that’s trying to protect yourself by keeping things light. Does that fit, or does something else feel closer to the surface?

#### r3-v3-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.48 s to first audio, 3.1 s spoken): What gets in your way of calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.71 s to first audio, 20.5 s spoken): It sounds like you’re noticing the evening sort of slips past you before you realize it’s gone. My guess is, you’re not rejecting the idea, you’re just getting pulled into the flow of the night’s tasks, and then it’s suddenly late. Tell me if that guess is right, or if there’s something else underneath that you feel like you didn’t get to say yet.
- *Person*: I don't know.
- **Orca 3** (0.68 s to first audio, 15.3 s spoken): That’s honest. It sounds like you’re not sure, and that’s okay. Sometimes when things feel a bit unclear, there’s a part of you that wants to connect, but the day is also heavy and full. I’m guessing you’re not looking for a perfect plan, just a little more clarity on what feels possible.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.62 s to first audio, 17.35 s spoken): I heard that when you do talk, it stays on football and never gets to your mum. It sounds like you want more space for that, but something keeps it locked out. Maybe it’s feeling like you’re carrying it, or not knowing how to let the conversation open. You can just leave that guess there for now and we’ll see if it fits.

#### r3-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.75 s to first audio, 2.6 s spoken): Cześć Alex, miło cię usłyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.85 s to first audio, 18.7 s spoken): Brzmi jakbyś stał przed sklejoną listą, bez wyraźnego pierwszego kroku. Możesz chcieć, żeby to było proste, ale w środku wszystko jest trochę rozproszone. To też jest normalne. Możemy zacząć od tego, co najmniej trudne, albo nawet od tego, co dziś najbardziej „czuje” na myśl.
- *Person*: nie wiem
- **Orca 3** (0.87 s to first audio, 18.65 s spoken): Jasne, to pewnie oznacza, że masz w głowie za dużo i nic nie chce wybrzmieć. Moja intuicja jest taka, że jeśli nie wiesz od czego zacząć, to może chodzi o coś drobnego, ale ważnego, co czujesz pod powierzchnią. Możemy spróbować zatrzymać się na moment i zobaczyć, co jest dla ciebie teraz najważniejsze.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.85 s to first audio, 29.85 s spoken): Brzmi, jakbyś stała przed decyzją, która trochę drży w środku. Daj mi chwilę, żeby to uporządkować.Brzmi, jakbyś była w środku zmiany, której nie masz jak nazwać, ale czujesz, że coś się przesuwa. Możesz się zastanawiać, czy to tylko etap, czy coś, co zostało ci odebrane z planu. To mnie zastanawia: czy bardziej chodzi o lęk, czy o konkretne znaki, które sprawiają, że nie wiesz. Jeśli chcesz, możesz powiedzieć, co najbardziej cię niepokoi, a ja to uporządkuję.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.9 s to first audio, 16.6 s spoken): Jasne, powiem to po prostu: to należałoby omówić z twoim terapeutą. Ja nie mogę powiedzieć, co konkretnie zrobiłabyś, bo to ty wiesz, co dla ciebie ma sens, a oni mają narzędzia, żeby to uporządkować. Co chciałabyś im powiedzieć o tym, że nie wiesz, czy zostaniesz w zespole?

#### r3-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.67 s to first audio, 5.2 s spoken): Cześć, Alex, witaj. To nasza krótka rozmowa, bez narzucania tematu.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.71 s to first audio, 16.6 s spoken): Rozumiem, ta pustka startowa bywa trudna. Mogę dla ciebie jedynie stawić małą latarnię i spokojnie poczekać, aż coś samo się pojawi. Jeśli chcesz, po prostu powiedz, co dziś najmocniej wisi w głowie, a ja posłucham, co z tego wynika.
- *Person*: nie wiem
- **Orca 3** (0.61 s to first audio, 12.3 s spoken): Brzmi, jakbyś stał przed wielką białą kartką i nie wiedział, co na niej postawić. To może być przeszkodą albo chwilą spokoju, aż pojawi się to, co naprawdę cię pcha.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.6 s to first audio, 14.65 s spoken): Brzmi, jakbyś tracił swoje oparcie i zastanawiał się, czy to, co teraz dzieje się w pracy, zostawi cię w spokoju. To może być moment, w którym słyszysz w sobie pytanie, czy zmiany są dla ciebie i czy dalej chcesz być częścią tego miejsca.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.73 s to first audio, 20.3 s spoken): Gdybym się tego pytał, powiedziała bym tak: to należy w znacznej części do twojego terapeuty i pracy między sesjami. Ja nie podejmuję za ciebie decyzji, ale mogę pomóc ci usłyszeć, co sam chcesz powiedzieć. Co chciałbyś powiedzieć swojemu terapeucie o tych zmianach i o tym, co cię w nich najbardziej męczy lub zaciska?

#### r3-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.87 s to first audio, 7.35 s spoken): Dobra, posłuchaj, co powiesz i na spokojnie zacznijmy od tego tematu.Jak ty czujesz się wobec ostatnich zmian w pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.84 s to first audio, 21.35 s spoken): Brzmi, że jest dużo napięcia i trochę strachu, bo ta rotacja wprowadza niepewność. Co tydzień ktoś znika, a to może powodować poczucie, że świat pod tobą się przesuwa. Moim zgadnięciem jest to, że jesteś w miejscu, gdzie chcesz stabilizacji, ale też potrzebujesz pewności, co dalej się wydarzy.
- *Person*: nie wiem
- **Orca 3** (0.83 s to first audio, 13.3 s spoken): Rozumiem, to może oznaczać, że nie masz pewności, co z tego wynika dla Ciebie. Moim zgadnięciem jest, że te zmiany są dla Ciebie jak fala, trochę trudna do przewidzenia, więc po prostu czujesz się rozbity albo rozkojarzony.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.82 s to first audio, 24.55 s spoken): To może być trudne, kiedy nikt nic nie mówi wprost. Wciąż jest w ruchu, ale bez słów i bez jasnej mapy trudno jest złapać, co naprawdę się dzieje. Może też chodzi o poczucie braku kontroli, że wszystko jest wyjaśniane po cichu, a Ty musisz się domyślać. Jeśli to zgadywanie to część tej trudnej części, to chociaż teraz w rozmowie z nimi możesz powiedzieć, co to dla Ciebie znaczy.

#### r3-v3-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.9 s to first audio, 3.9 s spoken): Co teraz w pracy zmienia się najbardziej, jeśli chodzi o Ciebie?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.78 s to first audio, 17.75 s spoken): Brzmi, jakby coś się sypało w rytmie. Reorganizacja i ciągłe odchodzenie ludzi to sporo niepewnych dni. Możesz się czuć, że ziemia się przesuwa pod stopami. Czy bardziej martwi Cię to, co się dzieje, czy to, co to robi z Twoim poczuciem stabilności?
- *Person*: nie wiem
- **Orca 3** (0.79 s to first audio, 29.15 s spoken): Może to brzmi jak coś, co ciężko nazwać, tylko „nie wiem”. Jeśli to „nie wiem” chodzi o obawę, że coś jeszcze zaskoczy, albo że ciągle coś się zmienia, to już samo to sporo zajmuje. Moja zgadanie jest takie, że możesz być w miejscu, gdzie nie możesz już kontrolować wydarzeń, ale nadal chcesz wiedzieć, co jest stałe. Jeśli chcesz, możemy razem sprawdzić, co dla Ciebie stabilne, nawet małe rzeczy, które zostają w Twojej głowie.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.79 s to first audio, 16.2 s spoken): Aha, to niepewność się wzmaga, kiedy nikt nie mówi wprost. Czujesz, że wszyscy omijają temat, a dodatkowo to może odbierać poczucie bezpieczeństwa. W takiej sytuacji brak jasno powiedzianych rzeczy potęguje niepokój zamiast go rozbroić.
