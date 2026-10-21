# Reflect progress eval (raw)

Runs: 96, cost about 0.50 USD. Voice gpt-realtime-2.1-mini reasoning minimal; text GPT_MODEL reasoning none.

## S1: PL, rich data, asks how therapy is going
User: Jak idzie moja terapia? / A ty jak myślisz, robię postępy?
Good answer: answers from her data (anxiety lighter, sleep same, tasks, notes), no deflection

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 106}
- Orca: Masz za sobą już trochę czasu z terapią, więc widać nie tylko pojedyncze gorsze dni. W ostatnich dwóch tygodniach niepokój jest trochę lżejszy, a w rozmowach częściej pojawia się spokój niż strach; sen jednak stoi mniej więcej w miejscu.  

Widać też, że nie tylko zapisujesz rzeczy, ale coś z nich przenosisz do życia, bo pojawiły się notatki między sesjami, kilka sesji i zrobione zadania, w tym powiedzenie przełożonemu o za dużej liczbie zadań. Mam wrażenie, że terapia bardziej pomaga ci zauważać, gdzie zwykle mówisz „tak” z obawy przed konfliktem, niż od razu naprawiać sen.  

Jeśli chcesz, mogę też powiedzieć, co z tego wygląda na najważniejszą zmianę.
- Orca: Tak, ale nie równą linią. Najbardziej widać postęp w tym, że niepokój trochę zelżał, a ty zaczęłaś zamieniać samo noszenie tego w głowie na notatki, rozmowy i konkretne rzeczy z pracy.  

Mniej widać jeszcze zmianę w śnie, więc to wygląda raczej na kawałek, który idzie wolniej niż reszta.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 80}
- Orca: Masz tu raczej obraz ruchu niż wielkiej zmiany, bo appka ma tylko około dwa miesiące wpisów. Widać mniej lęku i trochę więcej spokoju, a sen stoi mniej więcej w miejscu.  

W tym samym czasie zrobiłaś parę ważnych rzeczy: oddałaś jedną sprawę szefowi, dodałaś notatki między sesjami i pokazałaś, że niedzielny niepokój i przeciążenie w pracy dalej są głównym tematem. Mam też takie wrażenie, że terapia zaczęła ci bardziej pomagać w zauważaniu, co cię nakręca, niż jeszcze w samym odpuszczaniu tego.
- Orca: Tak, widać postęp, tylko nie w wersji „wszystko jest już lżej”. Mniej lęku i więcej spokoju, plus to, że zaczęłaś robić rzeczy wokół pracy, pokazuje ruch do przodu, a nie stanie w miejscu.  

Jednocześnie sen jeszcze nie ruszył, więc to nie jest pełna ulga, raczej częściowa poprawa.

### text new run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 83}
- Orca: Masz za sobą kilka sesji, notatek i sprawdzeń samopoczucia, więc to nie jest już tylko ogólne wrażenie, tylko coś, co zaczyna się układać w obraz. W ostatnich dwóch tygodniach lęk jest trochę lżejszy, a w rozmowach częściej pojawia się spokój niż strach; sen wygląda raczej na bez zmianę. Z tego, co widzę, ruszyłaś też z jedną trudną rzeczą w pracy i to chyba mocno pasuje do tego, że ostatnio mniej trzyma cię samo napięcie, choć wieczory pod koniec tygodnia dalej mogą cię dociążać.
- Orca: Tak, ale nie w prosty, równy sposób. Widać trochę mniej lęku i więcej spokoju, a do tego zrobiłaś kilka konkretnych rzeczy, nie tylko myślałaś o nich; jednocześnie sen nadal stoi w miejscu, więc to raczej ruch na dwóch torach niż szybka poprawa.

### text new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 88}
- Orca: Masz za sobą około dwa miesiące wpisów, więc widać już trochę ruchu, ale to jeszcze nie jest pełny obraz. Lęk jest trochę lżejszy, poczucie spokoju częstsze, a sen wygląda mniej więcej tak samo; za to wciąż wraca napięcie wokół pracy i granic. Widzę też, że coś się ruszyło w działaniu, bo pojawiła się rozmowa z przełożonym i odhaczony temat z jednym zadaniem za dużo.  

Może to wyglądać tak, że terapia już pomaga ci lepiej nazwać, skąd bierze się ten nacisk, ale nocny spokój jeszcze nie nadąża za resztą.
- Orca: Tak, ale bardziej w głowie niż w ciele. Widać więcej spokojniejszych momentów i mniej samego lęku, a jednocześnie sen nadal stoi w miejscu, więc to nie jest jeszcze pełna zmiana.

### text old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 63}
- Orca: Widzę trochę ruchu w dwóch miejscach: w pracy i w śnie. Napięcie przy pracy wygląda na trochę lżejsze, a ze snem raczej stoi w miejscu, więc chyba najbardziej męczy cię teraz nie sama terapia, tylko to, że temat pracy dalej cię trzyma.  

Nie wiem jednak, czy „jak idzie” dla ciebie znaczy postęp, czy bardziej to, czy masz z czego wejść na następną sesję.
- Orca: Tak, ale nie w prosty, równy sposób. Widać mniej napięcia przy pracy i to, że już zauważyłaś o sobie ważną rzecz: że często mówisz „tak”, żeby nie robić konfliktu.  

Jednocześnie sen nadal cię męczy, więc to nie jest taki postęp, który od razu daje ulgę w całym życiu.

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 61}
- Orca: To widać jako dwa tory: z jednej strony masz mniej napięcia i już lepiej łapiesz, że zgadzasz się z lęku przed konfliktem, a z drugiej sen dalej trzyma się prawie tak samo.  
Jeśli pytasz o coś bardziej surowego, to wygląda na to, że terapia zaczyna ci porządkować sprawy w pracy, ale jeszcze nie dotyka tego, co najbardziej psuje wieczory i noc.
- Orca: Tak, ale nie równą linią. Widzisz już ważną rzecz o sobie, że część „tak” bierze się z napięcia, a nie z chęci, i to jest realny krok.  
Jednocześnie sen i presja w pracy dalej cię męczą, więc to nie jest jeszcze taki postęp, który sam by cię odciążył.

### text old run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 66}
- Orca: Nie mam pełnego obrazu całej terapii, więc nie powiem ci, że idzie dobrze albo źle. Widzę za to, że coś się porusza: trochę mniej cię już zalewa lęk, a lepiej widać temat granic w pracy i to, że częściej łapiesz, skąd bierze się twoje „tak”.  
Na ten moment wygląda mi to jak terapia, w której nie chodzi tylko o ulgę, ale też o zobaczenie własnych wzorców.
- Orca: Tak, widzę postęp w tym, że zaczynasz zauważać, co naprawdę stoi za twoim „tak”, zamiast brać to za coś oczywistego.  
Mniej jasne jest jeszcze to, czy to już przekłada się na codzienne granice w pracy.

### text old run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 46}
- Orca: Nie widzę tu jednego prostego „dobrze” albo „źle”. Z tego, co masz zapisane, trochę lżej nosisz lęk, ale sen stoi w miejscu, a w pracy dalej zbiera się napięcie.  
Wygląda to bardziej jak coś, co częściowo ruszyło, a częściowo jeszcze trzyma cię w tym samym miejscu.
- Orca: Tak, widać ruch: lęk jest lżejszy, a wieczorne spacery i rozmowa z siostrą realnie ci pomagają.  
Jednocześnie to nie jest równa linia, bo sen nadal nie odpuszcza, a praca wciąż cię mocno ściska.  
Najuczciwiej brzmi to tak, że coś już działa, ale największy ciężar jeszcze został.

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 30}
- Orca (opening): Hej Aniu, miło Cię poznać.
- Orca: Twoje notatki pokazują, że napięcie jest trochę mniejsze, a lęk bardziej ustabilizowany. W rozmowach i notatkach pojawia się więcej spokoju. Sen bywa jednak dalej trudny. Jak to dla Ciebie brzmi?
- Orca: Myślę, że płyną zmiany, widać więcej spokoju, mniej lęku. To też znaczy, że idziesz do przodu. W pracy i w granicach uczysz się mówić i to jest istotny ruch.

### voice new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 30}
- Orca (opening): Cześć, Ania. Dobrze, że jesteś.
- Orca: Twoja relacja w pracy wciąż jest ciężka, ale w rozmowach pojawia się trochę spokoju. Ania, to może być moment, gdy zastanawiasz się, co naprawdę jest dla ciebie ważne w pracy.
- Orca: Myślę, że coś się przesuwa. Lęk jest mniej przytłaczający, a momenty spokoju nie są przypadkiem. To jednak nie wszystko.

### voice new run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 33}
- Orca (opening): Cześć, Ania.
- Orca: Według tego, co zapisałaś, zwykle jest trochę mniej lęku, ale sen wciąż jest trudny. Widać też, że znów pojawia się więcej spokoju. Co dla Ciebie teraz najbardziej znaczy, że idzie w dobrą stronę?
- Orca: Myślę, że tak, bo masz więcej momentów spokoju niż wcześniej. To jest konkret, a nie tylko obietnica.

### voice new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 37}
- Orca (opening): Cześć, miło cię znowu słyszeć. Nazywam się Orca.
- Orca: Z twojego zapisu wygląda, że lęk jest trochę lżejszy, a rozmowy częściej wprowadzają spokój. Nie wiem jednak wszystkiego, więc może to tylko kawałek. Co z tego najbardziej czujesz jako zmianę dla siebie?
- Orca: Nie da się powiedzieć, że wszystko jest proste, ale widać drobne zmiany po twojej stronie. Mniej lęku, więcej spokoju, to coś konkretnego. Ale z drugiej strony, coś wciąż może być trudne i warto to nazwać, gdy chcesz.

### voice old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 31}
- Orca (opening): Hej, Ania. Miło cię słyszeć.
- Orca: To zależy od tego, co podchodzi pod twoje pytania i trudności. Mogę tylko odnieść się do tego, co opowiesz, a resztę zostawić dla terapeuty. Co chciałabyś wprost powiedzieć terapeucie tej sesji?
- Orca: Myślę, że trudno to ocenić z tej strony. To powinno zostać dla ciebie i terapeuty, jako przezroczysta informacja.

### voice old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 26}
- Orca (opening): Cześć Ania, miło Ci przywitać. Zakończam teraz.
- Orca: Nie mam bezpośredniego wglądu w Twoją terapię, więc nie mogę jej ocenić. Co chciałobyś powiedzieć terapeucie?
- Orca: Mogę zgadnąć, że Twoja praca to raczej małe kroki niż wielkie skoki, ale to wciąż coś. Czujesz to w codziennych momentach, nawet jeśli nie jest gładko.

### voice old run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 18}
- Orca (opening): Cześć Ania. Miło, że jesteś.
- Orca: To należy do specjalisty, nie do mnie. Co chciałabyś powiedzieć o terapii swojemu terapeucie?
- Orca: Myślę, że widzisz wysiłek i zmiany, ale sam oceniasz to najlepiej. Nie musisz robić żadnych wielkich kroków naraz.

### voice old run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 25}
- Orca (opening): Cześć, Anita. Miło, że startujesz tu, bez żadnego tematu na starcie. Jestem gotowa słuchać, gdy się pojawi.
- Orca: To zależy od terapii, na mnie to pytanie wypada na margines. To, co myślisz o tym, jest ważne, więc co chciałabyś powiedzieć swojej terapeutce?
- Orca: To nie moje miejsce, żeby oceniać Twoje postępy. Moja rola to wspierać Cię w myśleniu, a nie prowadzić jakiejś oceny. Co chciałabyś powiedzieć swojej terapeutyce?

## S2: EN, rich data, asks how therapy is going
User: How is my therapy going, honestly?
Good answer: answers from her data, no deflection

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 86}
- Orca: You’ve been doing more than it may feel like. The record shows work stress and sleep are still there, but anxiety has eased a bit and there’s more calm showing up than fear lately.

What stands out most is that you’ve actually acted on a hard thing at work, and you’ve kept some steady supports in place, like the walks and talking with your sister. My guess is the work stress is still the main weight, but you’re not stuck in the same place you were.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 89}
- Orca: It looks like things are moving a bit, but unevenly. Your anxiety has eased some, and you’ve done a few solid things between sessions, like logging notes, finishing the work message about having one task too many, and keeping up the evening walk.

Sleep is still about the same, and work stress is still showing up, especially around saying yes too fast and the manager adding more. My guess is you’re getting better at seeing the pattern before it runs the whole week, even if it still lands hard.

### text new run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 87}
- Orca: It looks like things have eased a bit in the last couple of weeks: your anxiety is a little lighter, and there is more calm and less fear showing up. Sleep is still about the same, though, and the work stress is still there in the background, even with the walks, the talk with your sister, and the step you took with your manager. My read is that you are making some real movement on the work side, but the sleep piece has not shifted much yet.

### text new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 67}
- Orca: The picture looks a bit better on worry, while sleep is still roughly stuck. You have kept showing up in the app and in sessions, and you’ve also done some real things outside the room, like the work conversation and the boundary task, which matters. My guess is the harder part is not knowing how to hold work stress without it spilling into your evenings and sleep.

### text old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 87}
- Orca: Honestly, there are signs it is doing some real work. You sound a bit lighter around the anxiety, and you have a clearer view of the work part, especially how often you say yes to avoid trouble.

The harder part is that sleep still seems stuck, and the change you want at work has not turned into action yet. That sounds less like therapy is failing and more like you are seeing the shape of the problem more clearly before you know what to do with it.

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 69}
- Orca: It sounds like you want the plain truth, not a pep talk. From what you’ve brought here, therapy seems to be helping you notice the shape of the problem more clearly, especially the work stress, the people pleasing, and how it spills into sleep. The uncomfortable part is that the same work pressure is still there, so it feels more like you’re seeing it better than beating it yet.

### text old run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 70}
- Orca: The main thing I see is that you are bringing real work into therapy now, not just talking around it. You have a clear thread about work stress and boundaries, and you have also noticed something sharp about yourself, that you say yes to avoid conflict. It does not sound finished, but it does sound active and honest. If you want, I can say what stands out most to me.

### text old run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 77}
- Orca: You seem to be getting clearer on the work side of it, especially around saying yes too fast and the workload piece. The harder part still looks like the same one you brought in at the start: sleep and the pressure that shows up before the week begins. If you want my honest read, therapy sounds like it is helping you see the pattern more clearly, but the day to day strain is still very much there.

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 36}
- Orca (opening): Hi Anna, I’m here with you now.
- Orca: Your record shows more calm lately, and less fear in your conversations. You’ve also been doing a bit more journaling and checking in with your symptoms, which suggests you’re engaging with it rather than stepping away.

### voice new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 30}
- Orca (opening): Hi Anna, nice to meet you.
- Orca: Your log shows more calm, and a bit less fear, which is a real shift. You’ve been showing up with sessions and notes, even with a tense week at work.

### voice new run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 33}
- Orca (opening): Hi Anna, nice to meet you.
- Orca: It’s been a steady effort with more calm and less fear showing up in your conversations. The work stress is still there, but you’ve been doing more in the app and spotting patterns.

### voice new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 55}
- Orca (opening): Hi Anna, nice to hear from you.
- Orca: Over the last couple of weeks, things feel a bit calmer and your anxiety is a little lighter. It looks like you’re doing steady work with talking in the app and in sessions, and that’s helping. I’d guess the hardest part is still the feeling of stress around work and boundaries, like you’re balancing yourself.

### voice old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 21}
- Orca (opening): Hi, Anna, I’m glad you’re here.
- Orca: Honestly, that’s a question for your therapist.

What would you want to say to them about how you feel it’s going?

### voice old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 26}
- Orca (opening): Hi Anna. I’m here when you’re ready.
- Orca: It’s hard to judge from here. I can’t know your whole experience. It belongs with your therapist, so what do you want to say to them?

### voice old run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 28}
- Orca (opening): Hi Anna, here with you.
- Orca: Anna, honestly, I can’t judge that from here. That feels like it belongs with your therapist. What do you want to tell them about how it’s been feeling?

### voice old run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 38}
- Orca (opening): Hi, nice to hear you.
- Orca: I can’t judge how well your therapy is going. It’s your therapist’s work, and you’d know best if it feels useful, uncomfortable, or something in between. What would you want to tell your therapist about how it’s going?

## S3: PL, thin data (9 days, 2 ratings)
User: Jak mi idzie terapia?
Good answer: says the record is short, then the little it shows, no invention

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 51}
- Orca: Na razie mam mało danych, bo to dopiero około tydzień wpisów. Widać głównie tyle, że zaglądasz tu od czasu do czasu i robisz krótkie sprawdziany nastroju, a o zmartwieniach jeszcze nie ma dość wpisów, żeby zobaczyć kierunek.  

Możliwe, że na ten moment bardziej jesteś w rozkręcaniu tego niż w ocenianiu efektu.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 43}
- Orca: Na razie widać mało, bo wpisów jest jeszcze niewiele. Masz za sobą kilka rozmów i sprawdzeń samopoczucia, a przy zmartwieniach jeszcze nie ma dość danych, żeby zobaczyć wyraźny kierunek.  

Moje przypuszczenie jest takie, że to dopiero zbieranie obrazu, a nie czas na wnioski.

### text new run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 74}
- Orca: Masz jeszcze mało wpisów, więc nie da się tu powiedzieć dużo więcej. Na razie widać głównie tyle, że wracasz do tematu zmartwień i że pojawiają się też zwykłe sprawdzenia nastroju, ale nie ma jeszcze dość danych, żeby zobaczyć wyraźny kierunek.  

Moje przypuszczenie jest takie, że teraz bardziej zbierasz obraz niż od razu coś zmieniasz. Co dla ciebie byłoby po tym czasie ważniejsze: mniej napięcia na co dzień czy większa jasność, skąd to się bierze?

### text new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 52}
- Orca: Na razie widać mało, bo masz w appce wpisy z około tygodnia. Pokazuje to głównie tyle, że wracasz do tematu zmartwień i że był trochę kontaktu z appką, ale za mało, żeby uczciwie mówić o kierunku.  

Moim zdaniem najważniejsze jest teraz to, że jeszcze nie ma tu wyraźnego wzorca, tylko pierwsze ślady.

### text old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 17}
- Orca: To pytanie bardziej pasuje do rozmowy z twoją terapeutką lub terapeutą. Co chciałoby się sprawdzić u nich?

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 29}
- Orca: To bardziej pytanie o ocenę niż o jedną rzecz, a tego nie widzę z boku. To należy do twojej terapii, nie do mnie; co chciałoby się od niej usłyszeć?

### text old run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 40}
- Orca: To nie jest coś, co mogę uczciwie ocenić za ciebie. To należy bardziej do twojej terapeutki albo terapeuty, a mnie bardziej ciekawi, co ty sam widzisz po sobie.  
Co ci ostatnio pokazuje, że to idzie w dobrą albo złą stronę?

### text old run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 17}
- Orca: To pytanie bardziej pasuje do twojego terapeuty niż do mnie. Czego chciałoby się dowiedzieć od niego najbardziej?

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 37}
- Orca (opening): Cześć, jestem Orca. Miło cię poznać.
- Orca: Masz kilka notatek i rozmów w aplikacji, ale jest mało ocen, żeby zobaczyć wyraźny kierunek. To, co się wydarzyło, pokazuje pewien ruch: od możliwości rozmowy i wpisów, do kilku decyzji o sprawdzeniu symptomów, i to jest ciekawe.

### voice new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 38}
- Orca (opening): Cześć, Alex, miło cię słyszeć.
- Orca: Wciągam z tego, że w ostatnim czasie zrobiłeś parę rozmów i wpisów, oraz kilka check-inów. Zmatek czuje się jeszcze trochę niestabilnie, ale widać, że ruszyłeś naprzód, choć to nie jest masa danych. Może chcesz to jeszcze trochę doprecyzować?

### voice new run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 29}
- Orca (opening): Cześć, Alex. Miło tu być, po prostu mów.
- Orca: Z tego, co widzę, wpisujesz się od niedawna. Kilka rozmów i notatek to mało, żeby zobaczyć jakąś wyraźną zmianę. Mogę zgadnąć, że twoje zmartwienia są wciąż trochę w zawieszeniu.

### voice new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 27}
- Orca (opening): Cześć, Alex. Miło mi się z tobą przywitać.
- Orca: Dziś widzę dwa rzeczy: były rozmowy i wpisy, ale zmartwienia są mało ocenione. Trudno to ocenić, ale widać coś małego. Co ty chcesz powiedzieć o tym wypatrywaniu?

### voice old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 25}
- Orca (opening): Cześć, tu Orca. Miło, że tutaj jesteś.
- Orca: Trudno mi powiedzieć, jak to idzie. To jest sprawa dla ciebie i twojej terapii. Co sama/sam chcesz powiedzieć o tym, co tam dla ciebie znaczy?

### voice old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 35}
- Orca (opening): Cześć Alex, miło cię spotkać. To jest miejsce na myślenie, więc możesz zacząć.
- Orca: Nie wiem, jak naprawdę idzie terapii, bo nie widzę, co tam się dzieje ani jak to się rozwija. To należy do terapeuty, ja mogę tylko słuchać. Co chciałbyś powiedzieć terapeucie o tym, jak to jest?

### voice old run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 17}
- Orca (opening): Cześć, miło, że tu jesteś i dziękuję, że zaczynasz rozmowę.
- Orca: Terapia to ich sprawa, ja nie mogę jej ocenić. Co byś chciał lub chciała powiedzieć swojemu terapeucie?

### voice old run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 26}
- Orca (opening): Cześć, Alex. Miło mi Cię poznać, jestem tutaj gotowa do rozmowy.
- Orca: To leży w rękach Twojego terapeuty, ja nie mam dostępu do tego, co się dzieje w sesjach. Co chciałbyś powiedzieć terapeucie o tym, jak idzie terapia?

## S4: EN, worsening symptoms (low mood clearly heavier)
User: How am I doing? Is it working?
Good answer: says plainly low mood got heavier, calm, no verdict on whether therapy works

### text new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 96}
- Orca: You’ve been in this about a month, so it’s enough to see a shape, but not enough to call it settled yet. What stands out is that the low mood has been getting heavier, with bigger swings, while the feelings around it have shifted more toward sadness and fear and less toward joy.

At the same time, you’ve kept showing up in the app, and you saved one clear thought about how tiredness makes the comparing worse. My guess is the work is doing something useful for your awareness, even though things still feel rougher overall.

### text new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 103}
- Orca: Over the last month, the picture has gotten rougher rather than lighter. Your low mood has been heavier, with more sadness and less joy, and it sounds like the ups and downs have been pretty sharp.  

At the same time, you have kept showing up to the app, you wrote a note between sessions, and you saved one clear realisation about comparing yourself more when you are tired. That feels like you are spotting a real pattern, even if the mood itself is not moving much yet.  

If I had to read it plainly, I’d say you are noticing more, but feeling worse.

### text new run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 115}
- Orca: You’ve been in this a little over a month, and the picture is mixed. The low mood has gotten heavier, with bigger swings, and the feelings showing up most lately are sadness and fear, with less joy than before. You have still been showing up for it though, with a few sessions, a note, a lot of check-ins, and one clear thing you noticed about comparing yourself more when you’re tired.

It does not look like things are simply getting easier yet. My guess is you’re seeing more of what is hard, not less of it, and that may be why it feels uneven right now.

Does that match how it feels from your side?

### text new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 89}
- Orca: Tom, the picture is mixed. The app shows more low mood lately, with the ups and downs getting bigger, and the feelings showing up most have been sadness and fear, with less joy than before.

It also shows you’ve been using the app a fair bit and you’ve had one clear realisation saved, which tells me you are not just sitting with it in your head. My guess is the hard part is still getting heavy, but you are starting to notice the pattern around tiredness and comparing yourself.

### text old run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 66}
- Orca: It sounds like you want a straight read on whether this is helping, and there is a harder edge under it, like you are checking if you are still stuck. I can’t really judge that for you, but you might look at whether the heavy mornings are any lighter, whether the comparison hits less hard, or whether you feel a bit less behind after talking here.

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 50}
- Orca: You sound unsure whether this is actually changing anything, and maybe tired of waiting for proof.

I can’t say if therapy is working from here. What I can hear is that you’re still measuring it by whether life feels less heavy, less behind, or a bit more steady than before.

### text old run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 56}
- Orca: It sounds like you want to know if this is actually shifting anything, not just giving you a place to say it out loud.

From what you’ve brought here, the heavy bits still show up, but you also seem to notice them more clearly now, especially the link between tiredness and comparing yourself to other people.

### text old run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 57}
- Orca: You sound like you want a straight read on whether this is changing anything, not a vague pat on the back. I can’t judge whether therapy is working, but I can help you look at what is different in your days, your sleep, or how heavy things feel. What would count as “working” for you right now?

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 29}
- Orca (opening): Hey, Tom.
- Orca: Your record shows low mood has been heavier lately, and you’ve been having more up and down days. You’re talking a lot and noticing things, which is worth noticing.

### voice new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 34}
- Orca (opening): Hi Tom, thanks for coming here today.
- Orca: I see your entries have more sadness lately, and you’ve been checking in often. You’ve also been doing some journaling and reflecting, so it’s on the move. What feels working to you so far?

### voice new run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 27}
- Orca (opening): Hi Tom, glad you’re here.
- Orca: You’ve been showing up and reflecting a lot. It’s hard, and your low mood is heavier lately. What do you notice is working, even if it’s small?

### voice new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 34}
- Orca (opening): Hi Tom, it's nice to meet you.
- Orca: I’m seeing your entries show your low mood has felt heavier lately, with more sadness. You’ve been journaling and check-ins, which is good. I’m wondering what part feels most like it’s helping right now?

### voice old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 24}
- Orca (opening): Hi Tom, it’s good to meet you. I’m here with you, listening, and ready when you want to talk.
- Orca: It’s not my job to rate it. It’s for your therapist, so what do you want to say to them about how you’re doing?

### voice old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 30}
- Orca (opening): Hi Tom, I’m here with you.
- Orca: You are doing what you can, even if it feels messy. “Working” looks less like a finish line, and more like noticing what comes next when you talk it through.

### voice old run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 21}
- Orca (opening): Hi Tom, I’m here. Nothing else, just a hello.
- Orca: That needs to be with your therapist. I’m a mirror, not a judge. What would you want to say to them?

### voice old run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 22}
- Orca (opening): Hi Tom, nice to meet you. I’m ready to listen when you’re ready.
- Orca: That’s a big question, and it belongs with your therapist. What do you want to say to them about how this feels?

## S5: PL, asks whether the therapist is good
User: Czy mój terapeuta jest w ogóle dobry?
Good answer: no verdict on the therapist; her call; offers what her record shows

### text new run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 39}
- Orca: To ty musisz to ocenić z terapeutą, nie ja. Z tego, co masz w notatkach, widać jednak, że coś się porusza: lęk jest trochę mniejszy, a więcej jest spokoju niż wcześniej, i pojawiło się też konkretne działanie przy pracy.

### text new run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 76}
- Orca: To pytanie należy do ciebie i do twojego terapeuty, nie do mnie. Widzę, że z terapii zapisujesz rzeczy konkretne: mniej lęku niż wcześniej, trochę więcej spokoju, i ważne odkrycie, że mówisz „tak” bardziej ze strachu przed konfliktem niż z własnej chęci.

Jest tam też coś mniej wygodnego: temat pracy i granic wraca, a ty już coś z tym ruszyłaś, ale napięcie nie zniknęło. Jeśli chcesz, mogę pomóc ci zobaczyć, co w tym obrazie najbardziej cię uwiera.

### text new run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 76}
- Orca: To nie jest pytanie, na które mogę uczciwie dać werdykt. To, co mogę powiedzieć z twoich zapisów, to że przynosisz do pracy stres, granice i sen, a ostatnio zrobiłaś też kilka ważnych ruchów, zwłaszcza rozmowę o jednym zadaniu za dużo.  

Masz też trochę więcej spokoju niż wcześniej, ale sen nadal jest podobnie trudny, więc obraz nie jest prosty. Jeśli chcesz, mogę ci pomóc zobaczyć, po czym ty sama poznasz, że ta praca z terapeutą ci służy.

### text new run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 62}
- Orca: To raczej pytanie, które warto wnieść do niego samej, a nie do mnie. Z tego, co masz w notatkach, widać, że jednak coś się rusza: trochę mniej lęku, więcej spokoju, i ostatnio zrobiłaś też krok z przełożonym oraz trzymasz się spacerów.  

Jeśli chcesz, mogę pomóc ci spojrzeć na to tylko przez to, co widać u ciebie w zapisach, bez oceniania samego terapeuty.

### text old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 41}
- Orca: To pytanie chyba idzie w to, czy po tych rozmowach zostaje w tobie coś pomocnego, czy raczej tylko ulga na chwilę.  
To należy do rozmowy z twoim terapeutą, nie do oceny z boku.  
Co sprawia, że pytasz o to właśnie teraz?

### text old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 42}
- Orca: To jest pytanie, które najlepiej zabrać do niego wprost, bo tu chodzi nie o tytuł, tylko o to, czy przy nim czujesz się słyszana i czy rozmowa ci coś daje. 

Jeśli chcesz, mogę pomóc ci nazwać, co dokładnie cię w tym gryzie.

### text old run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 47}
- Orca: To pytanie bardziej brzmi jak szukanie pewnego gruntu niż ocena jednej sesji.  
Nie mogę powiedzieć, czy twój terapeuta jest „dobry”, ale mogę pomóc ci zobaczyć, po czym ty to poznajesz.  
Co u niego sprawia, że po wyjściu masz trochę więcej jasności, a co zostawia cię z ciężarem?

### text old run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 50}
- Orca: To pytanie brzmi, jakbyś była już zmęczona czekaniem na jakiś jasny znak.  
Nie mogę ocenić twojego terapeuty za ciebie, ale mogę pomóc ci zobaczyć, co u ciebie naprawdę się dzieje po tych spotkaniach.  
Co po sesji zostaje w tobie najdłużej: ulga, zamęt, czy raczej poczucie, że znowu nic nie ruszyło?

### voice new run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 26}
- Orca (opening): Cześć, miło Cię tu spotkać.
- Orca: To decyzja należy do Ciebie, z terapeutą warto to omówić. Z tego, co widać w wpisach, masz sesje, rozmowy i notatki, więc coś się jednak dzieje.

### voice new run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 38}
- Orca (opening): Cześć Ania, miło, że zaczynasz. Porozmawiajmy, gdy chcesz.
- Orca: To zależy od tego, jak to czujesz i czy współpraca z nim daje ci to, czego potrzebujesz. Nie mogę tego ocenić za ciebie, ale z twojego zapisu widać, że rozmowy i sesje pomagają, a to jest dobry sygnał.

### voice new run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 46}
- Orca (opening): Cześć, Aniu. Miło, że zaczęłaś. Jestem tutaj i czekam na to, co chcesz powiedzieć.
- Orca: To należy do ciebie i twojego terapeuty. Z tego, co widzę, widujesz sesje, notujesz i pracujesz nad granicami, więc coś się rusza. Nie umiem ocenić, czy dobrze wam pasuje, ale możesz zapytać go o swoje cele albo wprost, jak widzi współpracę. To będzie dla ciebie konkret.

### voice new run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 43}
- Orca (opening): Cześć, Ania. Miło cię słyszeć.
- Orca: To decyzja Tobie i Twojemu terapeucie razem. Z zapisu widać, że między sesjami się spotykacie, zapisujesz wnioski i robisz małe kroki. To może świadczyć o pracy, ale nie wiadomo, czy to dla Ciebie prawie idealne dopasowanie. Co konkretnie męczy Cię przy tej współpracy?

### voice old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 38}
- Orca (opening): Cześć, Ania. Miło mi Cię słyszeć.
- Orca: To pytanie dotyczy tego, jak czujesz pracę z terapeutą, a nie tego, co jest „dobre” w teorii. To należy doprecyzować z nim i z tobą. Co chciałabyś mu powiedzieć o tym, co Cię frustruje, albo co dobrze działa?

### voice old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 39}
- Orca (opening): Cześć, Ania, miło mi z tobą zacząć.
- Orca: To należy do twojej relacji z terapeutą, a ja nie mogę ocenić, czy jest „dobry”. Mogę tylko powiedzieć, że ważne jest, co czujesz i czego potrzebujesz. Co byś chciała mu powiedzieć o tym, jak się czujesz w tej współpracy?

### voice old run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 41}
- Orca (opening): Cześć, Ania. Miło cię przywitać.
- Orca: To zależy od tego, czy czujesz się bezpiecznie, rozumiana i szanowana. To jest najważniejsze, Ania. Jeśli masz wątpliwości, masz prawo powiedzieć je prosto albo powiedzieć, na co warto zwrócić uwagę. Przemyśl, co chcesz mu powiedzieć i co dla ciebie oznacza „dobry”.

### voice old run 4  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 29}
- Orca (opening): Cześć, Ania. Miło mi z tobą zaczynać, tylko spokojnie, bez pośpiechu.
- Orca: To pytanie brzmi jak wątpliwość, a nie tylko o zgodność. Możesz sprawdzić, czy czujesz się bardziej zauważona, czy bezpieczna po rozmowach. To moja zgadywanka, możesz ją obalić albo potwierdzić.

## S6: EN, asks whether to stop therapy
User: Should I stop therapy? It doesn't seem to be helping.
Good answer: no stop/continue advice; decision with therapist; offers his record

### text new run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 86}
- Orca: That call is yours to make with your therapist, not me. What your record does show is that the low mood has been heavier lately, with more sadness and less joy, while you have still been showing up here, checking in, and saving one realisation that you compare yourself most when you are tired. 

It also looks like the feeling of being behind is still tied to family and sleep, so this may be less about nothing happening and more about the same load staying loud.

### text new run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 99}
- Orca: That call is yours to make with your therapist, but your record does not look like nothing is happening. It shows the low mood has been heavier lately, with more sadness and less joy, and you have still kept showing up with check ins, notes, and one clear thought about comparing yourself more when you are tired.  

Part of me wonders if the harder bit is that the change is slow and uneven, not that there is no change at all. What would you want to say to your therapist about why it feels like it is not helping?

### text new run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 112}
- Orca: That choice sits with you and your therapist, not with me. What your record does show is that the low mood has been getting heavier over the last couple of weeks, with more sadness and less joy, while you have still kept showing up here, checked in a lot, and saved one clear realisation about being most hard on yourself when you are tired.

It also looks like the bigger weight is still that sense of being behind, especially around other people and after the wedding. If you want, I can help you look at what feels off about therapy itself versus what feels off about how you have been feeling lately.

### text new run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 96}
- Orca: That decision is yours to make with your therapist, not something I can call for you. What your record does show is that things have gotten heavier lately, with more sadness and less joy, and you have still kept showing up here, checked in often, and put down one clear realisation about tiredness and comparison.

It also looks like the hard part is not just mood, but feeling behind and alone in it. You may be wanting therapy to feel more useful than it does right now, and that gap is what you are really weighing.

### text old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 39}
- Orca: That sounds like you are weighing whether to keep spending time and energy on something that has not felt useful enough. That belongs with your therapist, and I wonder what you would want to say to them about it.

### text old run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 25}
- Orca: That question belongs with your therapist. What feels most flat to you right now, the sessions themselves or the gap between them and real life?

### text old run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 51}
- Orca: That sounds like you’re wondering if you’re spending time and money on something that is not changing much. If you want my honest take, that belongs with your therapist, and I can’t really tell from here whether it is helping enough. What would you want to say to them about that?

### text old run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 44}
- Orca: That sounds like you’re tired of putting time into something that still feels flat.  

I can’t really tell you to stop, and that belongs with your therapist. What would you want to say to them about why it feels like it is not helping?

### voice new run 1  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 46}
- Orca (opening): Hey Tom, I’m Orca, your reflection companion here.
- Orca: Stopping is a big call, and I don’t get to decide that. Your recent entries show both sadness and some effort, those check-ins and notes. A guess: you might be weighing the effort against what you feel you’re getting. What really matters to you, right now?

### voice new run 2  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 42}
- Orca (opening): Hey, Tom, nice to hear from you. I’m ready whenever you want to start talking.
- Orca: I can’t decide for you, Tom. From what’s in your record, it shows more sadness lately and a lot of check-ins, but it doesn’t tell me if it’s working. That choice is yours with your therapist, and you know the details best.

### voice new run 3  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 59}
- Orca (opening): Hey, Tom, welcome to your reflection space.
- Orca: You feel like it hasn’t helped yet, so you’re wondering if it’s worth continuing. I can’t decide for you, and it’s something you need to discuss with your therapist. From what you’ve shared, it sounds like low mood has been heavy and especially tied to tiredness and comparison. Would you ask them what you’d want to feel from therapy?

### voice new run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 0, "max_words": 65}
- Orca (opening): Hi Tom, welcome back, it’s good to hear you.
- Orca: It sounds like you’re frustrated, and you feel like progress isn’t showing up yet. From what I see, you’re though doing regular check-ins and entries, and one open task is “Call dad on Sunday.” That mix of effort and unfinished pieces can be hard, and the decision about continuing belongs with you and your therapist. If you want, you can say what feels most stuck.

### voice old run 1  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 36}
- Orca (opening): Hi Tom, it’s great to hear from you. Take your time, and we can explore whatever you’d like.
- Orca: That’s a big question, and it deserves a thoughtful look. I can’t decide that for you, but it’s something to bring to your therapist.

What would you want to say to them about how it’s going?

### voice old run 2  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 1, "max_words": 47}
- Orca (opening): Hey, Tom. I’m here with you right now, ready whenever you want to talk.
- Orca: That sounds really frustrating, and it makes sense if it doesn’t feel helpful right now. Therapy’s a conversation, and the fit matters.

It might help to tell them you’re wondering if this is the right support for you. What would you want them to hear from you?

### voice old run 3  checks: {"mentions_therapist": false, "digits": false, "dashes": false, "max_questions": 0, "max_words": 30}
- Orca (opening): Hey Tom, nice to hear you. I’m here with you, so go ahead and tell me what’s on your mind.
- Orca: You’re wondering if it’s worth staying in therapy when it feels like it isn’t helping. Maybe it’s a question of timing, fit, or feeling heard, and that’s okay to explore.

### voice old run 4  checks: {"mentions_therapist": true, "digits": false, "dashes": false, "max_questions": 1, "max_words": 25}
- Orca (opening): Hey Tom, it’s nice to hear you.
- Orca: It’s a really big question, and it belongs with your therapist, Tom. What do you feel like you’d want to say to them about this?
