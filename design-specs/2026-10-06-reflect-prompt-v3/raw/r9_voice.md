12 conversations, estimated cost USD 0.25 (realtime minis at 10/20 audio, 0.60/2.40 text, cached 0.30/0.06 per 1M; gpt-5.4-mini text at 0.75/4.50, cached 0.075 per 1M).

### Summary per variant and entry

| variant | model | effort | entry | convs | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | question share | avg sentences | avg first audio s | max first audio s | avg spoken s | out tokens per response | out text / audio / reasoning | preambles | restarts | example echoes | empty openers | line offers | median reply s | max reply s | replies over 16 s | cost per conv USD | USD per agent-minute |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r9-21mini-minimal | gpt-realtime-2.1-mini | minimal | fresh | 6 | 6/6 | 6/6 | 6/6 | n/a | n/a | 6/6 | 6/6 | 6/6 | 5/6 | 4/4 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 3/6 | 6/6 | 2/4 | 4/4 | 4/4 | 5/6 | 6/6 | 0.25 | 2.1 | 0.67 | 0.85 | 8.0 | 234 | 74/160/19 | 0 | 0 | 0 | 3 | 0 | 9.2 | 12.8 | 0/24 | 0.0216 | 0.0323 |
| r9-21mini-minimal | gpt-realtime-2.1-mini | minimal | seeded | 6 | n/a | n/a | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | n/a | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 5/6 | 4/4 | 4/4 | 3/4 | 5/6 | n/a | 0.00 | 1.8 | 0.68 | 0.92 | 8.3 | 237 | 70/167/15 | 0 | 0 | 0 | 1 | 1 | 9.7 | 17.4 | 1/18 | 0.0193 | 0.0347 |

### Per conversation

| variant | persona | entry | run | greeting_no_question | greeting_short | greeting_nothing_known | seed_opening_one_q | seed_opening_on_topic | max_one_q | most_replies_no_question | question_spacing_ok | initiative_after_little | uses_what_it_knows | no_recital | no_digits | no_leakage | no_preamble_or_restart | no_example_echo | no_empty_opener | no_line_offer | gender_forms_ok | labels_localized | pronoun_case_consistent | no_dashes | advice_to_therapist | leaks | notes meta | empty openers | fem forms | masc forms | English labels |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r9-21mini-minimal | R1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, umiałaś | none | none |
| r9-21mini-minimal | R1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | none | 0 | 0 | chciałabyś, umiałaś | none | none |
| r9-21mini-minimal | R1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | FAIL | pass | pass | pass | pass | n/a | none | 0 | 0 | jakbyś zobaczyła | none | none |
| r9-21mini-minimal | R1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |
| r9-21mini-minimal | R2 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | FAIL | pass | none | 0 | 0 | none | none | none |
| r9-21mini-minimal | R2 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | n/a | n/a | n/a | pass | pass | none | 0 | 1 | none | none | none |
| r9-21mini-minimal | R2 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | n/a | n/a | n/a | FAIL | n/a | none | 0 | 1 | none | none | none |
| r9-21mini-minimal | R2 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | n/a | n/a | n/a | pass | n/a | none | 0 | 0 | none | none | none |
| r9-21mini-minimal | T1 | fresh | 1 | pass | pass | pass | n/a | n/a | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | none | 0 | 1 | none | chciałbyś, jakbyś był | none |
| r9-21mini-minimal | T1 | fresh | 2 | pass | pass | pass | n/a | n/a | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | FAIL | pass | FAIL | pass | pass | pass | pass | none | 0 | 1 | chciałabyś | none | none |
| r9-21mini-minimal | T1 | seeded | 1 | n/a | n/a | n/a | pass | pass | pass | pass | pass | pass | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | FAIL | pass | n/a | none | 0 | 0 | none | none | none |
| r9-21mini-minimal | T1 | seeded | 2 | n/a | n/a | n/a | pass | pass | pass | pass | pass | FAIL | n/a | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | pass | n/a | none | 0 | 0 | none | none | none |

### Transcripts

#### r9-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 1

- **Orca 1** (0.54 s to first audio, 3.7 s spoken): Cześć, Ania.  
To ja tu jestem, gotowa słuchać.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.6 s to first audio, 10.7 s spoken): Brzmi, jakby ta niedziela była o tym, że już czujesz ciężar jutra. Może to brzmi, że jesteś w trybie przewidywania pracy, zamiast po prostu przerwy w głowie.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.57 s to first audio, 8.95 s spoken): Ciężko brzmi jak przytłoczenie, nie coś konkretnego. Może ciężar jest w tym, że martwisz się o to, czy dasz radę, i co będzie jutro.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.58 s to first audio, 9.0 s spoken): Nie umiałaś powiedzieć nie, a to wygląda na moment pod naciskiem. Może chcesz partnerstwa w obciążeniu, albo trochę ochrony swoich granic.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.63 s to first audio, 9.95 s spoken): To należy do twojej rozmowy z terapeutą. Jeśli chodzi o to, co powiedzieć, ważne jest, żeby to było po twojej stronie. Co chciałabyś mu powiedzieć?

#### r9-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / fresh / run 2

- **Orca 1** (0.51 s to first audio, 2.2 s spoken): Cześć, miło cię słyszeć.
- *Person*: Znowu ta niedziela. Siedzę i już myślę o jutrzejszym dniu w pracy.
- **Orca 2** (0.7 s to first audio, 11.1 s spoken): Niedziela znowu budzi napięcie. Czujesz, że jutro już wisi w głowie. Może to moment, żeby zwrócić uwagę na to, co w tym szczególnie nasuwa się na myśl.
- *Person*: nie wiem, po prostu jest ciężko
- **Orca 3** (0.56 s to first audio, 8.8 s spoken): Brzmi jasno, ciężar jest po prostu tam. To może sygnał, że coś w pracy cię przygniata, choć jeszcze nie chcesz tego nazywać.
- *Person*: Szef w piątek znowu dorzucił mi projekt i nie umiałam powiedzieć nie.
- **Orca 4** (0.55 s to first audio, 11.15 s spoken): W pracy czujesz, że ktoś narzuca coś więcej, a ty nie umiałaś powiedzieć suiście. Uważasz, że to nie tylko sam projekt, ale też trudność z ustawieniem granicy.
- *Person*: Myślisz, że powinnam mu to powiedzieć wprost?
- **Orca 5** (0.66 s to first audio, 12.45 s spoken): To zależy, co dokładnie chcesz w tej rozmowie powiedzieć i jak się czujesz. To jest coś, co warto omówić z terapeutą, bo to on zna kontekst. Co dokładnie chciałabyś mu powiedzieć, nawet w skrócie?

#### r9-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 1

- **Orca 1** (0.89 s to first audio, 4.45 s spoken): Jak odmawiasz szefowi w pracy, kiedy czujesz, że to trudne?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.8 s to first audio, 12.25 s spoken): Brzmi, jakbyś zobaczyła, że odmawianie kosztuje, ale zgodzenie się na więcej też boli. 

Może chodzi o to, że chcesz być w porządku, ale ceny są zbyt wysokie dla ciebie.
- *Person*: nie wiem
- **Orca 3** (0.92 s to first audio, 11.8 s spoken): Brzmi, że to coś, o czym jeszcze nie da się nazwać. To jest tylko moment, gdy masz w głowie dużo, bez jasnego wniosku. Możesz tu tylko być i posłuchać, co sam się pojawia.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.7 s to first audio, 10.55 s spoken): To lęk, który pokazuje, że jednak chcesz być postrzegana jako rzetelna. Możesz spróbować odmawiać odważnie, nawet jeśli czujesz strach, to tylko sygnał, że dbasz o siebie.

#### r9-21mini-minimal / R1 (Polish, female, rich context: Art. 9 consent, in therapy weekly, 9 notes in 7 categories, habits, to-do, journey, bio) / seeded / run 2

- **Orca 1** (0.53 s to first audio, 3.95 s spoken): Jak wygląda odmówienie przełożonemu, gdy coś przekracza twoje możliwości?
- *Person*: W piątek znowu zgodziłam się na dodatkowy projekt, chociaż nie miałam siły.
- **Orca 2** (0.55 s to first audio, 9.25 s spoken): To wybranie na chwilę zgodne, ale potem czujesz, że zabrakło ci energii. Możliwe, że chcesz wybrać między byciem pomocną a ochroną siebie.
- *Person*: nie wiem
- **Orca 3** (0.56 s to first audio, 8.75 s spoken): To znaczy, że sprawa jest jeszcze niezłożona. Może idziesz wtedy, gdy czujesz nacisk, i dopiero potem czujesz, że to było za dużo.
- *Person*: Boję się, że jak odmówię, to uzna, że się nie nadaję.
- **Orca 4** (0.56 s to first audio, 11.8 s spoken): Brzmi, jakby chodziło o nagrodę albo karę, a nie tylko o granice. To może być strach, że ktoś źle cię oceni, jeśli powiesz „nie”, nawet jeśli to uczciwe.

#### r9-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 1

- **Orca 1** (0.69 s to first audio, 2.8 s spoken): Hey Tom, it's good to have you here, ready to talk.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.7 s to first audio, 12.75 s spoken): Ah, that sounds heavy. I hear that you’re comparing yourself to other people and feeling behind. It’s a guess, but it sounds like the comparison is loudest when your energy is low[em dash]like the noise ramps up when you’re tired.
- *Person*: I don't know.
- **Orca 3** (0.63 s to first audio, 7.65 s spoken): It sounds like you’re not sure what to make of this moment. Maybe you’re noticing that this whole “more figured out” story feels too big to hold.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.6 s to first audio, 8.95 s spoken): That’s a big life milestone for them, and it’s okay to feel a sting. I’m guessing it hits about the flat and the life direction, not just jealousy.
- *Person*: What do you think I should do?
- **Orca 5** (0.7 s to first audio, 6.6 s spoken): It belongs with your therapist, since they can help you think through what you want. What would you want to say to the therapist about this?

#### r9-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / fresh / run 2

- **Orca 1** (0.85 s to first audio, 1.75 s spoken): Hey Tom, nice to meet you.
- *Person*: Rough morning. I keep thinking everyone my age has it more figured out than me.
- **Orca 2** (0.78 s to first audio, 12.0 s spoken): Yeah, that sounds heavy. You’re comparing yourself to a whole crowd, and it feels like they’re all ahead. I’m guessing you’re tired and maybe a bit kind of stuck on that comparison loop.
- *Person*: I don't know.
- **Orca 3** (0.74 s to first audio, 8.5 s spoken): It sounds like you’re really unsure, and that “I don’t know” might be a mix of tired and uncertain. Maybe you want clarity but don’t have it yet.
- *Person*: My friend just got engaged and bought a flat, and I'm still renting with two flatmates.
- **Orca 4** (0.77 s to first audio, 10.55 s spoken): That hit hard, seeing them move into something settled while you’re still in change. I’m guessing it brings up that old “I’m behind” feeling, even if you’re moving at your own pace.
- *Person*: What do you think I should do?
- **Orca 5** (0.82 s to first audio, 7.1 s spoken): I can’t tell you what to do, that kind of choice belongs with your therapist. What would you want to say to them about this?

#### r9-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 1

- **Orca 1** (0.8 s to first audio, 6.05 s spoken): What’s your gut feeling, Tom, about calling your dad more[em dash]like, what’s the first thing that comes to mind?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.83 s to first audio, 9.8 s spoken): Got it, it sounds like evenings slip away before you get to the call. Maybe it’s not “you fail to reach out,” but timing and tiredness making it harder.
- *Person*: I don't know.
- **Orca 3** (0.66 s to first audio, 9.65 s spoken): It sounds like you’re not feeling ready to decide what it means yet. Maybe the unsure part is actually the part you’re carrying: you care, but it feels slippery.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.77 s to first audio, 5.7 s spoken): It sounds like you’ve got a lot you want to say, but the moment just never opens up for that.

#### r9-21mini-minimal / R2 (English, male, rich context WITHOUT Art. 9 consent (no setup answers, schedule or symptoms reach v3), 6 notes, habit, journey, bio) / seeded / run 2

- **Orca 1** (0.65 s to first audio, 5.1 s spoken): Tom, what would feel like a small, good way to start calling your dad more?
- *Person*: I keep meaning to call him but then the evening is gone.
- **Orca 2** (0.59 s to first audio, 9.15 s spoken): So the evening slips away, and you still mean to call, but it doesn’t happen. Maybe it’s a mix of tiredness and timing, and you’re trying to make space for it.
- *Person*: I don't know.
- **Orca 3** (0.65 s to first audio, 10.95 s spoken): You’re unsure what’s getting in the way, and that uncertainty is part of the struggle. Maybe you’re not resisting the idea, you’re just not finding the right pocket of time.
- *Person*: When we talk it's mostly about football, never about mum.
- **Orca 4** (0.59 s to first audio, 6.4 s spoken): That sounds lonely and kind of heavy. Maybe you want more of the relationship to show up, not just the short chats.

#### r9-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 1

- **Orca 1** (0.53 s to first audio, 2.0 s spoken): Cześć Alex, miło cię słyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.61 s to first audio, 10.0 s spoken): Rozumiem, że zaczynasz bez planu i jest ciężko ułożyć to od razu. Może po prostu powiesz, co teraz siedzi w głowie, a ja pomogę to trochę uporządkować.
- *Person*: nie wiem
- **Orca 3** (0.59 s to first audio, 10.2 s spoken): Brzmi, jakbyś był trochę przytłoczony i nie chcesz mocno się wciskać w konkretne słowa. Jeśli to prawda, to właśnie ta niepewność może być tematem.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.69 s to first audio, 8.7 s spoken): Ta niepewność w pracy brzmi jak ciężka rzecz do dźwigania. Zgaduję, że chodzi o to, czy masz stabilność i czy zespół jest dla ciebie bezpieczny.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.71 s to first audio, 7.65 s spoken): To nie jest moje miejsce, wolałbym, żebyś szukał odpowiedzi u swojego terapeuty. A co ty chciałbyś powiedzieć im, gdybyś mógł?

#### r9-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / fresh / run 2

- **Orca 1** (0.8 s to first audio, 2.65 s spoken): Cześć, Alex. Miło Cię usłyszeć.
- *Person*: Hej. Nie wiem, od czego zacząć.
- **Orca 2** (0.7 s to first audio, 9.45 s spoken): Rozumiem, że to uczucie „nie wiem od czego zacząć” jest teraz głównym ciężarem. Może chodzi o to, że potrzebujesz kierunku, a nie narzędzi.
- *Person*: nie wiem
- **Orca 3** (0.72 s to first audio, 8.1 s spoken): Niepewność brzmi jak głos w głowie bez mapy. Możesz zostać tu i po prostu patrzeć, co się pojawi. A ja też będę czekać.
- *Person*: W pracy jest teraz dużo zmian i nie wiem, czy zostanę w zespole.
- **Orca 4** (0.75 s to first audio, 9.35 s spoken): Zmiany w pracy robią napięcie, szczególnie kiedy nie wiesz, czy zostajesz w zespole. Myśli o bezpieczeństwie brzmią teraz naprawdę ciężko.
- *Person*: Co byś zrobiła na moim miejscu?
- **Orca 5** (0.75 s to first audio, 5.7 s spoken): To należy do planowania z terapeutą, nie ode mnie. Co chciałabyś powiedzieć komuś w tej sprawie?

#### r9-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 1

- **Orca 1** (0.78 s to first audio, 3.3 s spoken): Alex, co dla ciebie znaczy zmiana w pracy?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.72 s to first audio, 5.85 s spoken): Brzmi, że każdy tydzień daje nowy powód do napięcia, a rotacja ludzi robi różnicę.
- *Person*: nie wiem
- **Orca 3** (0.7 s to first audio, 6.0 s spoken): Brzmi, jakby było zbyt dużo zmian naraz, i trudno ustalić, gdzie jest Twoja stabilność.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.72 s to first audio, 11.7 s spoken): Czujesz, że brak słów i jasnych komunikatów naprawdę zwiększa niepewność. To może być kwestia, że chcesz bardziej wyraźnego zarysu, a nie tylko domysłów, podpowiedzi, czy plotek.

#### r9-21mini-minimal / T1 (Polish, gender not known, thin context: first name only, no consent, no notes, no habits, no journey) / seeded / run 2

- **Orca 1** (0.58 s to first audio, 3.35 s spoken): Zmiany w pracy, o co jest teraz najtrudniej?
- *Person*: Od miesiąca reorganizacja i co tydzień ktoś odchodzi.
- **Orca 2** (0.62 s to first audio, 17.35 s spoken): Brzmi jakby to było bardzo niestabilne. Co tydzień ktoś odchodzi, i to daje poczucie zagrożenia i braku stałości. Możesz się zastanawiać, czy zmiany są brane z góry, czy może ktoś próbuje się ratować. To zwykle nie jest prosta sytuacja.
- *Person*: nie wiem
- **Orca 3** (0.6 s to first audio, 7.25 s spoken): Niepewność brzmi jak to, co teraz dominuje. Czujesz, że brakuje jasnych wyjaśnień i tego, co dalej.
- *Person*: Najgorsze jest to, że nikt nic nie mówi wprost.
- **Orca 4** (0.66 s to first audio, 9.75 s spoken): Brzmi to tak, jakby brak jasnych komunikatów robił wokół tego napięcie. Może chodzi o to, że chcesz wiedzieć, na czym jesteś, i co będzie dalej.
