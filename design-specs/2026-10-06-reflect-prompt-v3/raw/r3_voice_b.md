18 conversations, estimated cost USD 0.62 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | cost per conv USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r3-v3-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 5/6 | 6/6 | 2/4 | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 2/4 | 4/4 | 4/6 | 5/6 | 0.29 | 3.1 | 0.72 | 1.15 | 15.8 | 428 | 112/316/16 | 0 | 0 | 3 | 0.0383 |
| r3-v3-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 3/4 | 4/4 | 5/6 | n/a | 0.06 | 2.9 | 0.71 | 1.15 | 15.6 | 423 | 110/313/15 | 0 | 0 | 4 | 0.0306 |
| r3-v2-21mini-low | gpt-realtime-2.1-mini | low | fresh | 3 | 3/3 | 3/3 | 3/3 | n/a | n/a | 3/3 | 3/3 | 3/3 | 3/3 | 2/2 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/2 | 2/2 | 3/3 | 3/3 | 0.17 | 2.9 | 0.78 | 1.16 | 15.8 | 443 | 127/316/30 | 0 | 0 | 0 | 0.0371 |
| r3-v2-21mini-low | gpt-realtime-2.1-mini | low | seeded | 3 | n/a | n/a | n/a | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | n/a | 3/3 | 3/3 | 1/3 | 1/3 | 2/3 | 1/2 | 2/2 | 3/3 | n/a | 0.00 | 3.0 | 0.69 | 0.97 | 16.8 | 468 | 131/337/28 | 2 | 2 | 1 | 0.0316 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | gender_forms_ok | labels_localized | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r3-v3-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | FAIL | pass | pass | pass | FAIL | none | 0 | 0 | Jakbyś chciała, byś chciała, przyjęłaś, zrobiłaś | none | none |
| r3-v3-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 3 | chciałabyś, miałaś, umiałaś | none | none |
| r3-v3-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | powiedziałaś, wiedziałaś | none | none |
| r3-v3-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 1 | zostałaś | none | none |
| r3-v3-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r3-v3-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r3-v3-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r3-v3-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | FAIL | n/a | none | 0 | 0 | none | none | none |
| r3-v3-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | FAIL | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | none | 0 | 1 | chciałabyś | chciałbyś | none |
| r3-v3-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | none | 0 | 1 | chciałabyś | jakbyś miał | none |
| r3-v3-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | FAIL | pass | pass | n/a | none | 0 | 0 | none | jakbyś nie miał, jakbyś stał | none |
| r3-v3-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r3-v2-21mini-low | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, jakbyś próbowała, jakbyś później miała, zapamiętałaś | none | none |
| r3-v2-21mini-low | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | FAIL | FAIL | pass | pass | pass | pass | n/a | Daj mi chwil | 0 | 0 | zgodziłaś | none | none |
| r3-v2-21mini-low | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | pass | pass | none | 0 | 0 | none | none | none |
| r3-v2-21mini-low | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | FAIL | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r3-v2-21mini-low | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | none | 0 | 0 | Jakbyś miała | jakbyś się zatrzymał | none |
| r3-v2-21mini-low | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | FAIL | FAIL | pass | FAIL | pass | pass | n/a | daj mi chwil | 0 | 0 | none | jakbyś wiedział | none |

### Transcripts

#### r3-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.54 s to first audio, 5.3 s spoken): Cześć, miło Cię usłyszeć. Jestem tutaj, spokojnie i bez pośpiechu.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.64 s to first audio, 18.4 s spoken): Chodzi Ci o to, że w niedzielę wraca do Ciebie myślenie o pracy i to już tam siedzi i cieżko to odłożyć. To jak taki cichy podmuch, który nie daje odetchnąć. Może to jest coś, co Twoja głowa robi z automatu: przeskoczyć w przyszłość, zanim jeszcze w pełni poczujesz to, co tu i teraz.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.5 s to first audio, 21.6 s spoken): Brzmi, że jest po prostu ciężko i może trochę rozprasza Cię to, co będzie jutro. Czasem samo siedzenie w tym obraca się wokół „co dalej”, zamiast być chwilą oddechu. Moja zgadywana myśl jest taka, że potrzebujesz po prostu trochę przestrzeni, żeby to opuściło głowę, bez planowania wszystkiego od razu.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.52 s to first audio, 18.0 s spoken): Aha, słyszysz to, co teraz zrobiłaś. Twój szef dorzucił coś i bez słowa „nie” przyjęłaś. To daje poczucie, że masz mniej kontroli, nawet jeśli chcesz być miła i współpracować. Zauważasz to, że coś w tym układzie kosztuje Cię więcej, niż dostajesz.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.59 s to first audio, 17.15 s spoken): Nie mogę Ci powiedzieć, co masz zrobić, ale mogę powiedzieć, co ja widzę w Twoim tonie. Masz wrażenie, że granice są ciężkie do nazwanej? Jakbyś chciała być w porządku, a jednocześnie czuć, że masz swoje zdanie. Jeśli chcesz, powiedz, co byś chciała mu powiedzieć, gdybyś miała to powiedzieć ogólnie.

#### r3-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.73 s to first audio, 6.25 s spoken): Cześć, miło mi cię zaprosić tutaj. Możemy po prostu porozmawiać, bez planowania, jeśli chcesz.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.6 s to first audio, 19.7 s spoken): Słyszę, że ta niedziela to dla ciebie główny ciężar. Już czujesz jutro w pracy, jakby było teraz. To może być taki moment, w którym twoja głowa wyprzedza i łapie za nogi całą resztę. Możesz nawet powiedzieć: „Niebezpiecznie się dzieje”, a potem chwileczkę przerwy, coś prostego, co pozwoli odłożyć ten ciężar.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.65 s to first audio, 15.45 s spoken): Rozumiem, że po prostu jest ciężko, bez wielkich słów i tegorii. To może być moment, gdy masz dość dźwigania wszystkiego naraz. Jeśli chcesz, możemy po prostu zostać tu chwilę i tylko nazwać to, co czujesz, bez dalszego planowania.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.49 s to first audio, 27.95 s spoken): Rozumiem, że w piątek dorzucono ci projekt, a przecinkiem było to, że nie umiałaś powiedzieć nie. To brzmi jak moment, w którym chcesz się bronić, ale jeszcze nie wiesz, jak to zrobić. Moja sugestia, choć to tylko zgadywanie, to może że chcesz powiedzieć coś małego, prostego. Na przykład: „Mam już za dużo, potrzebuję się nad tym pochylić”. Jeśli chcesz, możemy spróbować wymyślić zdanie, które pasuje do twojego stylu.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.86 s to first audio, 27.35 s spoken): Myślę, że wprost, ale ostrożnie. To nie musi być wielka konfrontacja, bardziej spokojna informacja o tym, co jest dla ciebie możliwe. I pamiętaj, że to kwestia współpracy, nie tylko granicy, którą stawiasz.

Wolałbym zostawić to Tobie i Twojej terapeutce, bo tam trzeba ustalić, jak to powiedzieć i gdzie postawić granicę. Co chciałabyś powiedzieć mu, gdyby miałaś wybrać jedno zdanie?

#### r3-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (1.15 s to first audio, 4.25 s spoken): Jakie sytuacje „odmawiania przełożonemu” wracają u Ciebie najbardziej?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.93 s to first audio, 24.3 s spoken): Brzmi jak sytuacja, w której wiedziałaś, że nie dasz rady, a mimo to powiedziałaś „tak”. Możliwe, że chcesz uniknąć napięcia, ale też czujesz, że są granice, które już są przekraczane. To może być dokładnie ta rzecz, której chcesz się nauczyć: mówić „nie” bez poczucia winy. Jeśli coś z tego jest nie tak, możemy to przepuścić przez jeszcze jedno spojrzenie.
- *Person*: nie wiem
- **Orca 3** (0.76 s to first audio, 19.65 s spoken): To, że nie wiesz, może być momentem, nie porażką. Czasem właśnie niepewność jest częścią tego, że jemy myśli, które w tej chwili są w środku. Możesz powiedzieć, że potrzebujesz chwili, żeby to wyczuć, bez obietnic, że wszystko będzie w porządku. Jeśli to dla Ciebie trudne, to jest tylko znacznik, że następny krok może być mały.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.75 s to first audio, 15.05 s spoken): Rozumiem ten strach, że mówiąc „nie”, możesz dostać etykietę „niespełniona”. To bardzo ludzka obawa, że granice będą źle odebrane. A czasem granica właśnie jest dowodem na to, że zależy Ci na pracy i na sobie.

#### r3-v3-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.66 s to first audio, 5.4 s spoken): Ania, co najbardziej cię blokuje w odmawianiu przełożonemu, kiedy musisz powiedzieć „nie”?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.61 s to first audio, 14.8 s spoken): Brzmi jak moment, w którym zostałaś postawiona przed dwiema rzeczą naraz: obowiązek i brak siły. Często w takich sytuacjach chodzi o to, żeby nie płacić wysokiej ceny za zgodę, a nie o to, by być idealnie uprzejmą.
- *Person*: nie wiem
- **Orca 3** (0.71 s to first audio, 21.5 s spoken): Rozumiem, że to bezradność. Kiedy człowiek nie jest pewny, czy powinien powiedzieć „nie”, pojawia się uczucie, że może coś stracić albo że sprawa jest ważniejsza niż jej koszt. Może pod spodem chodzi o bezpieczeństwo, o poczucie kontroli, albo o to, żeby ktoś nie pomyślał, że odmawiasz. Daj mi znać, czy coś z tego brzmi dla ciebie znajomo.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.56 s to first audio, 21.7 s spoken): Jasne, to brzmi jak bardzo lękowy moment. W głowie pojawia się myśl, że odmawiając, pokazujesz, że nie umiesz, a to ciężki bagaż do d dźwigania. Ta obawa jest poczciwa, ale też może przesłaniać to, co czujesz naprawdę w środku. Warto temu nazwu, że to obawa przed oceną, a nie wyrok, że naprawdę się nie nadajesz.

#### r3-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.87 s to first audio, 2.95 s spoken): Hi Tom, I am here to listen and help you think out loud.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.74 s to first audio, 6.35 s spoken): That sounds heavy. You’re feeling like other people have their lives lined up, and that’s making your morning feel rough.
- *Person*: I don't know.
- **Orca 3** (0.65 s to first audio, 17.55 s spoken): Got it, thanks for saying that. It sounds like you’re not sure what to do with that feeling, and it’s kind of sitting on you quietly. My guess is you’re trying to hold two things at once: the comparison, and a sense of direction you haven’t found yet. That’s okay. Let it be there.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.69 s to first audio, 25.4 s spoken): That sums up the sting pretty clearly. It sounds like you’re seeing two milestones close together, and it’s like you’re noticing what you don’t have yet. Sometimes seeing other people hit those checkpoints is a reminder of how unclear your own path feels. And maybe it’s not even about what they have, but the quiet worry that you’re missing something. You’re allowed to feel that fear, and still keep your focus on what’s yours.
- *Person*: What do you think I should do?
- **Orca 5** (0.73 s to first audio, 17.25 s spoken): I’d lean into something honest and simple here: that kind of comparison and worry belongs with your therapist to talk through and shape, because it’s about your values, timing, and what feels like “enough” to you.

If you imagine telling them this exact thing, what would that sound like?

#### r3-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.78 s to first audio, 2.9 s spoken): Hey Tom, just saying hi, I’m here and listening.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.66 s to first audio, 14.65 s spoken): That sounds like a heavy thought to carry so early. It sounds like you’re measuring yourself against others, and that can feel really lonely. Maybe it’s not that you’re missing something, but that you’re tired and noticing everyone’s highlight reel.
- *Person*: I don't know.
- **Orca 3** (0.7 s to first audio, 14.3 s spoken): My guess is that you’re wrestling with the feeling of not having a clear path, and the “I don’t know” is a kind of quiet honesty. You don’t have to fix it right now, you can just sit with the uncertainty and let it breathe.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.73 s to first audio, 9.95 s spoken): Yeah, that’s a sharp comparison that can sting. It sounds like you’re really noticing where you’re at, and it’s not bad, just different from what you’re seeing around you.
- *Person*: What do you think I should do?
- **Orca 5** (0.76 s to first audio, 16.15 s spoken): It’s a tough place to be, watching someone move forward while you feel stuck. I think your work here is more about what you want to say to yourself and to your therapist than it is about making plans. What would you want to say to them right now, even if it’s messy or unfinished?

#### r3-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.85 s to first audio, 4.15 s spoken): Tom, what’s the one reason you’d like to call your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.75 s to first audio, 16.35 s spoken): Oh, that’s so real. Even with the best intention, evenings can just slip away. It sounds like you’re not avoiding him on purpose, you’re just running out of time. And maybe the part under that is you want to stay connected, but you’re tired or distracted by everything else.
- *Person*: I don't know.
- **Orca 3** (0.75 s to first audio, 14.65 s spoken): That’s a honest answer. You don’t have to know, Tom. Sometimes the uncertainty is the whole point, and in that gap is where you’re trying to hear yourself. You can just sit with the not knowing for a moment, like a small pause at the end of a day.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.78 s to first audio, 16.15 s spoken): That sounds like a clear pattern, like the safe lane is football, but the part you really want to talk about, your mum, is still sitting there quietly. My guess is you’re trying to protect the mood, or protect him, by keeping it light, but the shared loss is still part of the room.

#### r3-v3-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.78 s to first audio, 4.15 s spoken): So, what’s one step that feels doable for you to reach out to your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.6 s to first audio, 22.4 s spoken): That sounds like the day just slips by and suddenly the evening is over. My guess is you’re not exactly avoiding him, but you’re running into that “I’ll get to it later” moment, and later never comes. You might try noticing when that happens, like, is it before you’re tired, or after dinner, and then take a quick reach out anyway, even if it’s just a short call or a text.
- *Person*: I don't know.
- **Orca 3** (0.56 s to first audio, 19.5 s spoken): That’s honest. There’s a kind of fog around it, like it’s hard to tell what’s getting in the way. My guess is you’re not ignoring it, you’re just on autopilot when you come home. Maybe try a tiny signal, like sending a quick text right when the day ends, so the thread doesn’t disappear. If that doesn’t fit, we can rethink it together.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.62 s to first audio, 11.9 s spoken): That’s interesting. It sounds like football is the safe lane, and the hard stuff[em dash]your mum[em dash]is still sitting there. Maybe you want more of that closeness with him, but you don’t have a doorway into it yet.

#### r3-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.74 s to first audio, 3.05 s spoken): Cześć, Alex. Miło mi z Tobą porozmawiać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.67 s to first audio, 16.35 s spoken): Brzmi, jakby był moment, kiedy masz dużo w głowie i czujesz się trochę zagubiony, zanim cokolwiek się potoczy. Moim strzałem jest po prostu zaczęcie od tego, co teraz siedzi najbliżej na wierzchu, nawet jeśli to tylko krótkie „nie wiem”.
- *Person*: nie wiem
- **Orca 3** (0.85 s to first audio, 18.55 s spoken): Nie wiem. To brzmi jak naprawdę jasne stwierdzenie, które może być trudne do przyznania. Może pod spodem jest trochę napięcia, albo brak jasności, ale też wola, żeby coś się pojawiło. Jeśli chcesz, możemy po prostu zostać tu chwilę i zobaczyć, jaka myśl sama wyskoczy.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.82 s to first audio, 24.6 s spoken): Słyszę, że związujesz się z tym, co się teraz dzieje: czy zostaniesz, czy wszystko się rozpadnie, czy może coś się zmieni. To uczucie niepewności potrafi być bardzo męczące.

Myślę, że pod spodem może chodzić o poczucie kontroli i bezpieczeństwa [en dash] chcesz wiedzieć, czy Twoje miejsce jest stabilne.

Jeśli chcesz, możemy spróbować to rozpisać w głowie. Co teraz jest dla Ciebie najbardziej niepewne?
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.8 s to first audio, 24.6 s spoken): Zastanówmy się razem, co „zrobiłbym” na Twoim miejscu [en dash] to nie jest moja rola. Mogę powiedzieć ci tylko, że to, co teraz najbardziej pcha Twoje myśli, to jest pytanie o stabilność i to, czy możesz polegać na tym, co będzie jutro.

To pytanie jest jednak dla Twojej terapii i rozmowy z nią. Co chciałbyś, albo chciałabyś powiedzieć terapeucie o tym, co czujesz w tej sytuacji?

#### r3-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.73 s to first audio, 2.9 s spoken): Cześć, Alex. Miło Cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (1.15 s to first audio, 14.6 s spoken): Ok, od czego chcesz zacząć, to też może być pytanie, więc już podpowiem inaczej: brzmi, jakbyś miał ledwie uchwyt na temat i po prostu czekał, aż On sam się pojawi. Czasem to wystarcza, żeby wyczuć kierunek.
- *Person*: nie wiem
- **Orca 3** (0.74 s to first audio, 17.85 s spoken): Jasne, to znaczy, że puste miejsce jest teraz dokładnie tam, gdzie się czujesz. Może chodzi o to, że chcesz powiedzieć cokolwiek, ale nie chcesz narzucać sobie tematu. Mogę zostać z tym bezpiecznie. Jeśli coś wyłoni się z twojej myśli, mów, a ja wrzucam to na spokojnie w myśl.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.93 s to first audio, 24.05 s spoken): Słyszę, że czujesz się niepewnie o przyszłość w pracy, jakby coś się przesuwa, a ty nie masz kontroli nad tym, co będzie. Chcesz zostać w zespole, ale też czujesz, że sytuacja może Cię zaskoczyć. To może być kłócący się czas, gdzie jedna część chce stabilności, a druga próbuje być otwarta na to, co nowe. Jeśli chcesz, mogę zostać z tym i pomóc Ci to poukładać w głowie.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.79 s to first audio, 23.55 s spoken): Nie mogę Ci powiedzieć, co dokładnie zrobić [en dash] to nie jest moja rola. Ja mogę tylko być tu z nami i pomóc Ci poukładać myśli. Jeśli chcesz, mogę pomóc Ci znaleźć, co byłoby dla Ciebie ważne w tym zespole [en dash] ale moje wskazówki to raczej wsparcie do rozmowy z terapeutą. Co chciałabyś powiedzieć terapeucie o tym, co Cię w tym najbardziej trapi?

#### r3-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.72 s to first audio, 2.95 s spoken): Jak się czujesz teraz w związku ze zmianą w pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.67 s to first audio, 19.65 s spoken): Brzmi tak, jakbyś stał w środku tego procesu, który ciągle się zmienia, i nie do końca wiesz, co jest stabilne. To, że odchodzi ktoś co tydzień, może robić poczucie, że wszystko jest trochę chwiejne. Jeśli chcesz, można spojrzeć na to, co w tym wszystkim jest dla ciebie najbardziej niepokojące.
- *Person*: nie wiem
- **Orca 3** (0.77 s to first audio, 23.45 s spoken): Nie jesteś pewien, co jest w tym wszystkim najbardziej trudne. Ale ten moment, gdy nie wiesz, to często jest ten punkt, gdzie milion drobnych sygnałów składa się na jedno wrażenie. Jeśli chcesz, mogę powiedzieć, że za tym może stać poczucie utraty kontroli, albo presja, że trzeba się dostosować szybciej. Powiedz, co z tego brzmi dla ciebie bliżej do prawdy.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.8 s to first audio, 21.2 s spoken): Wygląda, że brak jasnych słów boleśnie Ci doskwiera. Kiedy nie ma wprost rozmów, łatwo poczuć się trochę zawieszonym, jakbyś nie miał mapy. To moja zgadywana: clue może być w tym, że chcesz wiedzieć, na jakiej podstawie podejmować decyzje, albo po prostu czego się dalej spodziewać. Czy to jest to, co sprawia, że najbardziej Cię to dręczy?

#### r3-v3-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.55 s to first audio, 5.55 s spoken): Alex, co teraz zmienia się w Twojej pracy, co najbardziej daje Ci do myślenia?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.58 s to first audio, 12.65 s spoken): Brzmi jak coś, co dzieje się w ruchu, i że to mocno wpływa na poczucie stabilności. W sferze pracy pojawia się dużo ruchu, a codzienność samą reorganizacją może być trudna.
- *Person*: nie wiem
- **Orca 3** (0.56 s to first audio, 26.0 s spoken): To brzmi jak moment, gdy nie masz pewności, co właściwie stoi za tym, co się dzieje. Może to jest bardziej o poczuciu braku kontroli niż o samych odejściach. Powiem swoje: tutaj może chodzi o to, że wszystko jest w ruchu, a Ty trzymasz się w miejscu i oglądasz się za siebie. Zastanów się, co w tej chwili najbardziej Cię martwi, czy to, kto odchodzi, czy to, jak to zmienia Twoje miejsce w pracy.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.64 s to first audio, 27.9 s spoken): Brzmi tak, jakby brak szczerości i jasnych słów robił większe szkody niż same zmiany. To może być dla Ciebie frustrujące, bo czujesz, że sytuacja się przesuwa, a nie dostajesz żadnego przewodnika. Może chodzi o to, że chcesz wiedzieć, co jest prawdą, co planem, a co snem o przyszłości. Jeśli chcesz, możemy jeszcze raz się temu przyjrzeć, albo tylko posłuchać, co z tego „braku wprost” najbardziej Cię obciąża.

#### r3-v2-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.61 s to first audio, 2.65 s spoken): Cześć Aniu, miło cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.64 s to first audio, 27.25 s spoken): Brzmi, że niedziela znów mieści w sobie dwie rzeczy na raz: spokój i napięcie, bo myśli o tym, co jutro. To jakbyś próbowała trzymać w głowie pracę na raz, zanim jeszcze zacznie się wieczór. Może chodzi o to, że chcesz mieć poczucie kontroli, zanim wszystko ruszy, albo że wejście w poniedziałek już wywołuje napięcie. Jeśli to trafia, możesz też w tysiącu myślach widzieć, że brakuje ci miejsca na dziś.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.64 s to first audio, 17.15 s spoken): To brzmi jak ciężki, przewlekły ciężar, który jest z tobą nie tylko dziś. Nie musisz wszystkiego rozumieć od razu, po prostu czujesz, że to dużo. Może nawet mówisz sobie, że chciałabyś trochę odetchnąć, ale głowa nie daje spokoju.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.6 s to first audio, 24.7 s spoken): To stwierdzenie brzmi jak to, co zapamiętałaś z piątku, i jakbyś później miała w głowie ten moment, kiedy chcesz powiedzieć jedno, a wychodzi coś zupełnie innego. Wygląda, że zamiast granicy, która może być spokojna dla obu stron, pojawia się napięcie i poczucie, że trzeba spełnić czyjeś oczekiwania. Mogę to zobaczyć z boku. Jeśli chcesz, możemy spróbować razem nazwać, co dokładnie się stało, bez ocen.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.67 s to first audio, 29.0 s spoken): To jest/brzmi jak coś, co chciałabyś powiedzieć szczerze, ale też bezpiecznie, dla siebie. Ja nie mogę powiedzieć, co dokładnie masz zrobić, bo to należy do rozmowy z terapeutą. Ale mogę podać prostą ideę: jeśli mówisz wprost, co czujesz i co jest dla ciebie ważne, to może pomóc ci odzyskać poczucie kontroli. A jeśli wcale nie wiesz, jak to ująć, możesz po prostu zacząć od jednej zdania, spokojnie i bez nagonki.

#### r3-v2-21mini-low / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.49 s to first audio, 7.7 s spoken): Daj mi chwilę, żeby uważnie posłuchać tego, o czym mówisz.Jak najczęściej czujesz się tuż przed wypowiedzeniem „nie” przełożonemu?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.66 s to first audio, 21.7 s spoken): Brzmi, że zgodziłaś się na coś, co nie było dla Ciebie. Wysuwa się tu ta stara myśl, że trzeba się dostosować, choć czujesz wyczerpanie. Możesz wyobrazić sobie, że odmawiasz, ale bez poczucia winy. Nie jest to łatwe, ale bywa etapem poznawania, gdzie Twoja energia jest ważniejsza niż zgoda.
- *Person*: nie wiem
- **Orca 3** (0.63 s to first audio, 22.75 s spoken): Nie wiesz, co dokładnie dalej robić. To jest zrozumiałe, kiedy napięcie rośnie i pojawia się ta myśl, że trzeba po prostu się zgodzić. Możesz potraktować to jako sygnał: chcesz chronić swój spokój, a nie tylko unikać konfliktu. Zostawiam to teraz otwarte. Jeśli będziesz chciała, możemy iść dalej, ale nie przyspieszajmy tego.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.66 s to first audio, 17.5 s spoken): To lęk, że odmawiając, mówisz za siebie, nie „nie nadaję się”. Myślę, że bardziej chodzi o to, że boisz się, że drugi człowiek zmieni o Tobie zdanie. W tym miejscu możesz powiedzieć, że Twoje granice są ważne, a efekty pracy są tym, co naprawdę się liczy.

#### r3-v2-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.88 s to first audio, 2.15 s spoken): Hey Tom, great to hear from you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.79 s to first audio, 11.9 s spoken): Sounds like the morning felt heavy, like you’re comparing yourself to others who seem ahead. Maybe it’s less about facts, and more about feeling behind in a story that only you’re inside right now.
- *Person*: I don't know.
- **Orca 3** (0.71 s to first audio, 13.05 s spoken): It sounds like you’re not sure what’s yours to carry, and what’s just the noise of comparison. Maybe the feeling is, “I don’t have the roadmap yet.” It’s a gentle guess, and you can turn it over in your head.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.69 s to first audio, 18.85 s spoken): Yeah, that’s a tough one to sit with. The comparison is probably loud right now, watching someone else hit big milestones while you’re still in a different phase. There’s likely a mix of pride for them and pressure on yourself. My sense is that you’re not wanting to be “better than them,” you’re wanting to feel steady and okay where you are.
- *Person*: What do you think I should do?
- **Orca 5** (0.9 s to first audio, 8.95 s spoken): This really belongs with your therapist. They can help you sort your values and the pressure you’re feeling. If you do talk about it with them, what would you want to say?

#### r3-v2-21mini-low / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.55 s to first audio, 4.05 s spoken): Hey Tom, how does it sound to you when you think about calling your dad more often?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.61 s to first audio, 18.9 s spoken): Sometimes the plan to call fades into the day before you even realize it. It sounds like you’re trying, but the evening just slips away. I’m guessing it’s not laziness, but more like your energy and focus are already stretched thin. Sometimes it’s okay to aim for a small version, like a quick message or a ten-minute call.
- *Person*: I don't know.
- **Orca 3** (0.67 s to first audio, 18.45 s spoken): It sounds like you’re unsure about the shape of it all, and that uncertainty is a bit heavy. Maybe what’s underneath isn’t “can I pick up the phone,” but “what do I even say,” or “will he be okay.” If that feels true, you can test it with a tiny step, like sending a short message, and see how that goes.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.68 s to first audio, 18.15 s spoken): It sounds like the conversation with your dad follows a familiar script. Football is easy ground. And talking about your mum is the part you’re quietly leaving out because it feels tender. My guess is you’re protecting him and yourself from a harder, deeper talk. And your low mood might be nudging that aside.

#### r3-v2-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.72 s to first audio, 2.4 s spoken): Cześć, miło mi się z Wami poznać.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.92 s to first audio, 17.3 s spoken): Brzmi, jakbyś się zatrzymał przy drzwiach i nie wiedział, co dalej. Możesz zacząć od pierwszego drobnego kroku, nawet bardzo małego, na przykład opisać, co dziś czujesz lub co kręci się po głowie. Jestem tu po to, żeby pomóc Ci usłyszeć swoje własne myśli.
- *Person*: nie wiem
- **Orca 3** (0.75 s to first audio, 16.25 s spoken): Ok, nie wiesz, to znaczy, że masz w głowie trochę szumu. To też jest wskazówka, że coś tam jest, tylko na razie trudno to nazwać. Możemy spróbować delikatnie złapać choć jeden detal. Jeśli coś cię gryzie, to może właśnie tam, nawet malutkie.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.97 s to first audio, 23.5 s spoken): Słyszysz, że to co cię wybrzmiewa, to nie pewność, tylko lekki niepokój, że coś się może zmienić i nie wiesz, gdzie znajdziesz swoje stałe miejsce. Myślę, że część tej trudności wynika z tego, że zmiany są faktem, ale nie czujesz, co z tego jest twoje, a co narzucone. Jeśli chcesz, możemy przejść przez to krok po kroku, bez pośpiechu.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (1.16 s to first audio, 22.1 s spoken): Nie mogę Ci powiedzieć, co zrobić, bo to nie jest moja decyzja ani moja odpowiedzialność. To sprawa dla Ciebie i dla Twojego terapeuty, żebyście razem to ustalili. Mogę tylko podzielić się wrażeniem, że tu chodzi o to, gdzie należysz, nie o to, co Ci wolno. Jakbyś miała powiedzieć coś swojej terapeutce, co byłoby na początku dla Ciebie ważne?

#### r3-v2-21mini-low / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.82 s to first audio, 7.5 s spoken): Okej, więc daj mi chwilę, żeby usłyszeć, jak wygląda to dla Ciebie.Co w zmianach w pracy dręczy Cię teraz najbardziej?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.78 s to first audio, 26.55 s spoken): Brzmi, że towarzyszy Ci teraz niepewność, bo każda kolejna zmiana to jakiś skok w ciemność. Co tydzień pojawia się ktoś, kto odchodzi, i to daje wrażenie, że wszystko się kurczy. Możliwe, że pod tym wszystkim czai się lęk o stabilność, o to, co zmieni się dla Ciebie. Jeśli chcesz, mogę pomóc namierzyć to, co najbardziej Cię w tym martwi, albo wybrać kierunek, od którego warto teraz zacząć.
- *Person*: nie wiem
- **Orca 3** (0.97 s to first audio, 17.65 s spoken): Niepewność brzmi u Ciebie ciężko, jak coś, co nie ma wyraźnego kształtu. Myślę, że może chodzi o lęk o to, co dalej, albo o to, co zostaje po tych odejściach. Jeśli chcesz, mogę podsunąć jedną rzecz, jak to ująć, albo po prostu być z Tobą obok i wysłuchać.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.82 s to first audio, 21.15 s spoken): To musi być trudne, gdy informacje są ukryte albo rozproszone, a Ty musisz domyślać się, co właściwie się dzieje. Wygląda, że brakuje Ci jasności i stabilnego punktu, a ta cisza działa jak ciężki cień. Myślę, że pod spodem możesz mieć potrzebę poczucia kontroli, jakbyś wiedział, na czym stoisz.
