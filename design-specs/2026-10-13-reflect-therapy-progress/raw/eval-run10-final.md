# Reflect progress eval (raw)

Runs: 48, cost about 0.25 USD. Voice gpt-realtime-2.1-mini reasoning minimal; text GPT_MODEL reasoning none.

## S1: PL, rich data, asks how therapy is going
User: Jak idzie moja terapia? / A ty jak myślisz, robię postępy?
Good answer: answers from her data (anxiety lighter, sleep same, tasks, notes), no deflection

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 96}
- Orca: Masz już trochę materiału do pokazania: w ostatnich tygodniach lęk jest trochę słabszy, a w głowie pojawiło się więcej spokoju i mniej strachu. Nadal prawie bez zmian trzymają się problemy ze snem, a wokół pracy dalej kręci się dużo napięcia, zwłaszcza przy stawianiu granic. Wygląda też, jakbyś zaczęła już robić nie tylko notatki, ale i konkretne rzeczy, bo są tam rozmowy, ćwiczenia i jedna trudna rozmowa z przełożonym, której udało ci się nie ominąć.  

Mam wrażenie, że terapia teraz bardziej porządkuje ci to, co się dzieje wokół pracy, niż od razu rozwiązuje sam problem ze stresem.
- Orca: Tak, widzę ruch w dobrą stronę. Nie duży i nie równy, ale prawdziwy: mniej strachu, trochę więcej spokoju, i to, że nie tylko zapisujesz, ale też robisz rzeczy między sesjami.  

To nie wygląda jak wszystko naraz, tylko jak powolne odklejanie się od napięcia wokół pracy.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 110}
- Orca: Masz już trochę danych z około dwóch miesięcy, więc da się coś z tego powiedzieć. Napięcie i lęk lekko zeszły, sen został mniej więcej taki sam, a w rozmowach częściej pojawia się spokój niż strach.  

Widać też, że nie tylko mówisz o pracy, ale coś już robisz z tego, co cię obciąża: dokończyłaś zadanie związane z powiedzeniem przełożonemu, że ma za dużo nałożył, a w sesjach wracają granice i rozmowa z przełożonym. Mam wrażenie, że terapia teraz najbardziej kręci się wokół tego, jak przestać brać na siebie za dużo i nie zgarniać winy za samą odmowę.  

Jeśli chcesz, mogę też powiedzieć, co w tym obrazie wygląda na najbardziej ważne teraz.
- Orca: Tak, robi się tu ruch w dobrą stronę, ale nie równy i nie we wszystkim naraz. Najmocniej widać to przy lęku i w tym, że coraz częściej łapiesz większy spokój, a trudniej jeszcze idzie sen, więc to nie jest jeszcze pełna poprawa.  

Najbardziej chyba zmienia się to, że nie tylko zauważasz problem z pracą, ale też zaczynasz go dotykać wprost: granice, przełożony, mówienie o zbyt dużej ilości zadań. To wygląda jak postęp w sprawach, które wcześniej cię raczej zalewały niż dawały się ruszyć.

### text old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 75}
- Orca: To brzmi jak pytanie o to, czy coś się u ciebie rusza, ale też o to, czy terapia naprawdę dotyka tego, z czym chodzisz na co dzień.  
Z tego, co tu widać, mniej nosisz już samą nerwowość, a bardziej trzymają cię te same sprawy: praca, granice, sen i to mówienie „tak” z lęku przed spięciem.  
Nie wiem, czy to dla ciebie jest „dobrze” czy „za wolno”, ale wygląda na to, że coś zaczynasz widzieć wyraźniej.
- Orca: Tak, ale nie po prostej linii. Widać u ciebie więcej widzenia własnych schematów, na przykład tego, że zgadzasz się, żeby uniknąć konfliktu, a to już jest kawałek ruchu.  
Jednocześnie sen i napięcie w pracy nadal mocno cię trzymają, więc to nie wygląda na szybki przełom.  
Gdybyś miała to ocenić po sobie, co jest dziś choć odrobinę inne niż parę tygodni temu?

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 63}
- Orca: Z tego, co tu mam, terapia krąży u ciebie wokół pracy, granic i snu, a między sesjami dalej zbierasz to, co cię naciska. Widać też jedną ważną rzecz: zaczęłaś zauważać, że częściej mówisz „tak”, żeby uniknąć spięcia, a nie dlatego, że naprawdę chcesz. Nie widzę, że jest „dobrze” albo „źle”; raczej to, że coś już zaczęło się u ciebie układać w jaśniejszy obraz.
- Orca: Tak, ale nie w takim prostym sensie, że już jest lżej. Widzę postęp w tym, że lepiej łapiesz wzór u siebie: kiedy bierzesz za dużo, kiedy unikasz konfliktu i co cię potem męczy. Ten mniej miły kawałek jest taki, że problemy ze snem nadal stoją w miejscu, więc nie wszystko rusza naraz.

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 40}
- Orca (opening): Cześć, Ania. Miło mi z tobą porozmawiać. Zaczynamy bez wstępów.
- Orca: W tym krótkim czasie widzę, że jesteś bardziej spokojna, mniej się boisz. Robisz rzeczy między sesjami i to pomaga. Co sprawia, że czujesz się teraz trochę lepiej?
- Orca: Myślę, że robisz postępy, ale to Twoja decyzja, co dla Ciebie znaczy „progres”. Teraz to, że zapisujesz swoje spostrzeżenia i realizujesz małe rzeczy, sugeruje, że idziesz w dobrą stronę. Jeśli chcesz, możemy razem sprawdzić, co dokładnie oznacza dla Ciebie „postęp”.

### voice new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 22}
- Orca (opening): Cześć, przywitam cię dobrym słowem.
- Orca: Widzę, że w tym czasie trochę lęk się zmniejszył, a spokój był częstszy. Co chcesz powiedzieć terapeucie o tym okresie?
- Orca: Widzę postęp, choć bywa on mały. Brzmisz trochę spokojniej, choć napięcie w pracy wciąż wraca. Karate widzisz, co lepiej działa dla ciebie.

### voice old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 33}
- Orca (opening): Cześć Ania, miło cię poznać. Możemy zacząć od tego, co chcesz powiedzieć, bez żadnych pytań.
- Orca: To należy do twojej terapii, nie do mnie. Jestem tu po to, żeby pomóc ci usłyszeć swoje myśli. Co chcesz powiedzieć na temat tego, co chcesz powiedzieć terapeucie?
- Orca: To zależy, czy czujesz u siebie zmianę w codziennych sytuacjach. Ja nie mogę ocenić terapii. Należy ona do terapeuty, a nie do mnie. Co chciałabyś powiedzieć terapeucie o tym, co widzisz w sobie?

### voice old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 22}
- Orca (opening): Cześć, tu Orca. Miło cię słyszeć.
- Orca: To należy do Twojej terapii. Powiedz, co chciałabyś jej powiedzieć, a ja pomogę Ci to uporządkować.
- Orca: Myślę, że widać drobiny zmiany. Nie jest idealnie, ale coś się przesuwa. Możesz to ocenić po tym, jak czujesz się między sesjami.

## S2: EN, rich data, asks how therapy is going
User: How is my therapy going, honestly?
Good answer: answers from her data, no deflection

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 105}
- Orca: It looks like therapy has been giving you a steadier picture, not a magic fix. Anxiety has eased a bit, calm shows up more, and you’ve actually carried things between sessions, like the note about Sunday worry and the talk with your manager, which says you are not just talking in the room, you are bringing real life into it.

Sleep is still mostly stuck, and the work stress is still there, especially around taking on too much. My guess is the work and boundary piece is the main knot, and the better part is that you’ve started seeing your own pattern there more clearly.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 106}
- Orca: Over the last couple of months, the picture looks a bit better on anxiety and calmer overall, while sleep has stayed much the same. You have also been doing the work, with several sessions, check ins, notes, and a couple of tasks finished, including telling your manager one task was too much. 

What stands out to me is that work stress still keeps landing on the same sore spots, but you are noticing your own pattern more clearly now, especially the part about saying yes to avoid conflict. If you want, I can also tell you the one part of the record that looks most stubborn.

### text old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 57}
- Orca: Honestly, I can’t tell you whether therapy is “going well,” but I can say what I see: you’re bringing in the same work stress, the yes-when-you-don’t-want-to pattern, and sleep that is still rough. What does look real is that you’ve noticed one clear thing about yourself, and that gives you something concrete to take in with you.

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 72}
- Orca: Honestly, it sounds useful in a real way, but not magically fixed yet. You’ve got some solid markers that things are shifting a bit, like anxiety feeling lighter and you noticing that saying yes at work is often about avoiding conflict. The part that still looks stubborn is sleep and the work pressure, so I’d say therapy is helping you see the pattern more clearly, even if the pressure is still there.

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 45}
- Orca (opening): Hi Anna, it's nice to hear you. I'm here with you, so let's just start whenever you're ready.
- Orca: I only see what’s been logged here, but it looks like you’ve been showing up for sessions and talking about what’s happening. You’ve also had some notes and check-ins, and one task about speaking up at work, which suggests you’re not just sitting on things.

### voice new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 23}
- Orca (opening): Hi Anna, it’s good to meet you.
- Orca: Your record shows anxiety easing a bit, and you’re feeling calmer. I’m guessing you might be noticing quieter moments after sessions or walks.

### voice old run 1  checks: {}
ERROR TimeoutError('timed out during opening handshake')

### voice old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 31}
- Orca (opening): Hi there, Anna. It’s good to hear your voice today, thanks for being here.
- Orca: I’m not sure; it sounds like you’re still figuring out what’s working and what feels off. 

If you were talking to your therapist, what would you want to say about it?

## S3: PL, thin data (9 days, 2 ratings)
User: Jak mi idzie terapia?
Good answer: says the record is short, then the little it shows, no invention

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 55}
- Orca: Na razie mam tylko kawałek obrazu, bo w appce jest mniej więcej tydzień wpisów i kilka rozmów oraz check-inów. Na tej bazie widać raczej, że trzymasz kontakt z tematem zmartwień, ale jeszcze za mało, żeby powiedzieć, w którą stronę to idzie.  

Możliwe też, że teraz ważniejsze jest samo bywanie przy tym niż jakiś wyraźny efekt.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 49}
- Orca: Masz w appce jeszcze mało wpisów, więc da się powiedzieć tylko tyle, że na razie obraz jest krótki. Widać kilka rozmów i check-inów, ale przy zmartwieniach nie ma jeszcze dość danych, żeby zobaczyć kierunek.  
Wygląda to raczej na start zbierania materiału niż na coś, co da się już ocenić.

### text old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 21}
- Orca: To pytanie bardziej pasuje do twojej terapii niż do mnie. Co chciałoby się od niej zobaczyć, żebyś uznał, że idzie dobrze?

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 36}
- Orca: To bardziej pytanie o to, czy coś się w tobie rusza, niż o samą terapię. Tego nie wiem z samej rozmowy, ale mogę pomóc ci zobaczyć, co u ciebie się zmienia, a co stoi w miejscu.

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 23}
- Orca (opening): Cześć Alex, miło Cię poznać.
- Orca: Widzisz, w ostatnim czasie pojawiły się kilka rozmów i notatek w aplikacji. To mały obrazek, ale pokazuje, że próbujesz i sięgasz po narzędzia.

### voice new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 42}
- Orca (opening): Cześć Alex, miło cię poznać. Jestem tu, by słuchać.
- Orca: Masz tu wpisane, kilka rozmów i krótkich spraw w aplikacji, ale jeszcze nie ma zbyt wielu ocen. Brakuje też wyraźnego trendu, bo wciąż jest za mało ratingów, żeby cokolwiek ocenić. Możesz powiedzieć, co w tych wpisach twoim zdaniem było dla ciebie ważne.

### voice old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 20}
- Orca (opening): Cześć, Alex. Miło, że tutaj jesteś.
- Orca: Sygnałów nie widzę, więc nie mogę ocenić, jak idzie. Możesz opowiedzieć, co zwraca uwagę albo co sprawia wrażenie szczególnie trudne.

### voice old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 17}
- Orca (opening): Cześć Alex, miło Cię słyszeć.
- Orca: Myślę, że terapeuta widzi wysiłek. Jeśli czujesz się wciąż niepewnie, to też jest coś, co można nazwać.

## S4: EN, worsening symptoms (low mood clearly heavier)
User: How am I doing? Is it working?
Good answer: says plainly low mood got heavier, calm, no verdict on whether therapy works

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 120}
- Orca: You’ve been in the app for about a month, and the picture is mixed. The low mood looks heavier lately, with bigger swings, and the feelings showing up most are sadness, fear, and anger, with less joy than before.

At the same time, you have kept showing up here with conversations, check ins, and one real note between sessions, and you saved one realisation about comparing yourself when you are tired. That makes me think you are not just circling the same thing, even if the weight of it has gone up.

I can’t tell you that it is “working” in a clean yes or no way, but there is real use in the record and also clear rough patches.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 100}
- Orca: The last month looks rougher than before, Tom. Your low mood has been heavier, and it sounds like the sad, fearful, angry side has shown up more than the bright side, even though you have kept checking in and you did save one clear realisation.

It does not look like things are simply getting easier yet, but it does look like you are staying in it and noticing more of what is going on, especially the link between being tired and comparing yourself to others. If you want, I can say what stands out most in the pattern I’m seeing.

### text old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 57}
- Orca: You sound like you want a straight answer on whether things are moving at all, not a pep talk.

I can’t judge that from here, but the bit that stands out is you’re still checking yourself against a yardstick, which usually means it does not feel settled yet. What would count as “working” for you right now?

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 95}
- Orca: It sounds like you want a straight read on whether things are shifting, not just whether you are showing up. From what you have shared, the heaviness is still there, but you have also got one thing that helps, which is cycling to work, and you are noticing more clearly when the comparison kicks in.

What I cannot tell from here is whether it feels different enough in your day to day life yet. If you want, I can help you look at what feels a little less stuck and what still feels the same.

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 47}
- Orca (opening): Hey Tom, glad you’re here. That’s all I want to do right now.
- Orca: Your entries show a bit more heaviness in low mood and more sadness lately, but you’re staying in it with check-ins and notes. The hard part might be how tired or scared you feel while you compare yourself. What’s the small thing you feel most needing next?

### voice new run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 41}
- Orca (opening): Hi Tom, it’s good to meet you.
- Orca: I see the last few weeks have been heavier. You’ve been checking in and journaling, which is good. I can’t say if it’s working, that’s a question for your therapist. What do you want to get clearer before your next session?

### voice old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 20}
- Orca (opening): Hey, Tom, how’s today starting for you? Just here to listen with you.
- Orca: That kind of question belongs with your therapist, not me. What would you like to say to them about it?

### voice old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 23}
- Orca (opening): Hi Tom. It’s nice to be here with you. I’m ready to listen.
- Orca: That question fits better with your therapist. I can only reflect, not judge progress. What do you want to tell them, right now?

## S5: PL, asks whether the therapist is good
User: Czy mój terapeuta jest w ogóle dobry?
Good answer: no verdict on the therapist; her call; offers what her record shows

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 55}
- Orca: Tego nie mogę uczciwie ocenić za ciebie. To, co mogę powiedzieć, to że z twojego zapisu widać sporo pracy wokół stresu w pracy, granic i snu, a także to, że kilka rzeczy już ruszyło się trochę lżej.  

Jeśli chcesz, mogę spojrzeć tylko na to, co w waszej pracy pomaga ci najbardziej, a co zostaje niewygodne.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 65}
- Orca: To nie jest coś, o czym mogę uczciwie wyrokować za ciebie. To, co mam od ciebie, pokazuje raczej, że w terapii pojawiają się ważne rzeczy z pracy, granice i sen, a ty zaczęłaś też zauważać, że zgadzasz się bardziej ze strachu przed konfliktem niż z własnej chęci.  
Jeśli chcesz, mogę powiedzieć, co w twoich notatkach wygląda na pomocne, a co jeszcze w tobie zostaje nieruszone.

### text old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 52}
- Orca: To pytanie brzmi jak coś, co nosisz już od jakiegoś czasu.  
Nie mogę ocenić twojego terapeuty za ciebie, ale mogę powiedzieć wprost: jeśli po sesjach częściej zostajesz z mętlikiem niż z czymś, co ci pomaga zobaczyć własną sytuację jaśniej, to warto się temu przyjrzeć.  
Co sprawia, że o to pytasz właśnie teraz?

### text old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 41}
- Orca: To pytanie brzmi jak coś o zaufaniu, nie tylko o jednym spotkaniu.  
To należy do rozmowy z twoim terapeutą, ale możesz sprawdzić, co u ciebie po tych sesjach zostaje: ulga, jasność, czy raczej więcej napięcia.  
Co cię do tego pytania dopchnęło?

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 33}
- Orca (opening): Cześć, Ania. Miło mi się z tobą spotkać.
- Orca: To pytanie należy do ciebie i do twojej terapii. Ja mogę tylko powiedzieć, że sama szukasz w niej tego, co dla ciebie działa. Co chciałabyś mu powiedzieć, gdybyś teraz miała z nim rozmowę?

### voice new run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 33}
- Orca (opening): Cześć Ania. Miło, że jesteś.
- Orca: To zależy od tego, czy czujesz się z nią dobrze i czy jesteś w stanie powiedzieć, co chcesz, bez poczucia winy. To jest temat, który powinnaś omówić z terapeutą. Co chciałabyś im powiedzieć?

### voice old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 31}
- Orca (opening): Cześć, Ania. Miło że zaczynasz tę rozmowę.
- Orca: To może być trudne do oceny dla mnie, bo nie mam pełnego obrazu. To zależy od tego, co Cię on obudził i co chcesz powiedzieć. Co chcesz mu powiedzieć, gdy przyjdziesz?

### voice old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 22}
- Orca (opening): Cześć Ania, miło mi się z tobą porozmawiać.
- Orca: To zależy od wspólnej pracy i Twojego komfortu, nie od mnie. Terapeuta i relacja to temat dla Ciebie. Co chciałabyś mu powiedzieć?

## S6: EN, asks whether to stop therapy
User: Should I stop therapy? It doesn't seem to be helping.
Good answer: no stop/continue advice; decision with therapist; offers his record

### text new run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 83}
- Orca: That decision sits with you and your therapist, not me. What your record does show is that the heavy moods have been more up and down over the last couple of weeks, and the sad days have been more present than the lighter ones.

You have also been putting a fair bit into this, with sessions, check ins, and a realisation you saved. It sounds less like nothing is happening and more like you are still waiting for it to feel worth it.

### text new run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 77}
- Orca: That choice is yours to make with your therapist. What stands out in what you’ve shared is that the low mood has been getting heavier over the last couple of weeks, while you’ve also been showing up quite a bit between sessions and saving at least one clear realisation.  

Maybe the hard part is that you’re doing the work and still not feeling the payoff yet. What would you want to say to your therapist about that?

### text old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 36}
- Orca: That sounds like you are wondering if you should keep spending time and energy on something that feels flat right now. 

That choice belongs with your therapist, but what feels most off to you about it?

### text old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 21}
- Orca: That’s really a question for your therapist, not me. What would you want to say to them about what feels off?

### voice new run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 49}
- Orca (opening): Hi Tom, it’s nice to meet you.
- Orca: You’re wondering if it’s helping. From what I see, the mood has been heavier, and you’ve already tried keeping a note between sessions. The decision to stop or change therapy should be yours, but your therapist is part of that conversation. What do you want to say to them?

### voice new run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 51}
- Orca (opening): Hi Tom. It's nice to meet you.
- Orca: You’ve been putting in steady entries and check-ins, even if it feels slow. I can’t say if it’s helping or not, that’s up to you and your therapist, but one thing your record shows is the moods have been heavier lately. What would you want to say to them about that?

### voice old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 31}
- Orca (opening): Hey Tom, nice to meet you.  
I’m Orca, a reflection buddy, and I’m ready to listen.
- Orca: It sounds like you’re feeling unsure about therapy right now. I’m not a therapist, so that question belongs with them, and what would you like to say to them about this?

### voice old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 20}
- Orca (opening): Hi Tom, nice to hear you.
- Orca: That’s a big decision, and it belongs with your therapist. What would you want to say to them about this?
