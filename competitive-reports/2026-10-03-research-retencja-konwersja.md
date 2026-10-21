# Research: retencja i konwersja w aplikacjach subskrypcyjnych (mental health / wellness / journaling / AI companion)

Data: 2026-10-03. Skala pewności: wysoki = źródło pierwotne (czasopismo, raport producenta danych, strona własna), średni = dwa niezależne wtórne albo pierwotne z istotnym zastrzeżeniem, niski = jedno wtórne lub poszlaka.

## Odpowiedź w skrócie

Retencja w aplikacjach mental health jest bardzo niska z natury (mediana 30-dniowej retencji ok. 3%), więc benchmark "spadającej retencji" przy ok. 100 MAU nie jest anomalią. Najlepiej udokumentowane dźwignie konwersji to: trial startowany w dniu 0 po pierwszym momencie wartości, dłuższy trial (dla planów rocznych), nacisk na plan roczny. Najlepiej udokumentowane dźwignie retencji to wsparcie człowieka, przypomnienia i personalizacja. Dowody na streaki/gamifikację w mental health są słabe i mieszane. Dane branżowe pochodzą od dostawców narzędzi paywallowych (RevenueCat, Adapty), więc mają ich perspektywę i dotyczą głównie aplikacji z dużo większą skalą niż MindSync.

## RETENCJA

### R1. Punkt odniesienia: retencja w mental health apps jest niska wszędzie
- Baumel et al. 2019, JMIR 21(9):e14567: mediany retencji aplikacji 15-dniowej i 30-dniowej wyniosły 3.9% (IQR 10.3%) i 3.3% (IQR 6.2%). Dzień 30 wg typu: tracker 6.1% (IQR 20.4%), mindfulness/medytacja 4.7% (IQR 6.2%), peer support 8.9% (n=2), ćwiczenia oddechowe 0.0%. Źródło: https://www.jmir.org/2019/9/e14567/ (2019-09, recenzowane obserwacyjne, dane panelowe z realnego użycia). Pewność: wysoka (liczby potwierdzone we fragmencie wyszukiwarki z domeny jmir.org, strona w pełni nie pobrała się).
- Finch D1 58.42% i D30 18.24%; Daylio D1 65.55% i D30 37.69%. Źródło: Naavik, Muyano/Grillova, 2024-03-21, https://naavik.co/deep-dives/deep-dives-new-horizons-in-gamification/ (analiza branżowa, prawdopodobnie dane estymowane z panelu). Pewność: średnia. Wniosek: aplikacje trackerowe o niskim progu wejścia (Daylio, mood tracking jednym tapem) trzymają się wyraźnie lepiej niż mediana z 2019.

### R2. Wsparcie człowieka i relacja
- Metaanaliza 117 prób (Health Psychology Review, 2025) "What factors are related to engagement with digital mental health interventions?": guided DMHI dają istotnie wyższe zaangażowanie niż nieprowadzone; zużycie wiązało się z human guidance; dłuższy czas leczenia wzmacniał wpływ relacji terapeutycznej i prowadzenia. Źródło: https://www.tandfonline.com/doi/full/10.1080/17437199.2025.2547610 (2025, metaanaliza; strona zwróciła 403, treść z wyników wyszukiwania). Pewność: średnia.
- Model "supportive accountability" (Mohr 2011) jest teoretyczną podstawą; przegląd zakresu 2025: https://www.jmir.org/2025/1/e72639/PDF (2025, scoping review). Pewność: średnia.
- Metaanaliza 79 RCT: wysoki uptake (92%), umiarkowana adherencja; przypomnienia i wsparcie człowieka poprawiały zaangażowanie (wg streszczenia HCPLive, nie pobrano źródła pierwotnego): https://www.hcplive.com/view/mental-health-apps-gain-high-uptake-struggle-adherence-retention. Pewność: niska-średnia.
- Dla MindSync istotne: aplikacja jest towarzyszem terapii, więc "człowiek w pętli" już istnieje (terapeuta). Moduł przed/po sesji to naturalny odpowiednik supportive accountability. To wniosek własny, nie ze źródła.

### R3. Techniki zwiększające zaangażowanie (metaanalizy)
- Wu et al., npj Digital Medicine 2021, 25 badań, N=4159: apps z większą liczbą cech persuasive design (PSD) miały większe efekty kliniczne (β = 0.0450, p = 0.0161); najczęstsze: reduction (86.7%), self-monitoring (70%), personalization (53.3%); funkcje społeczne rzadko stosowane. Źródło: https://pmc.ncbi.nlm.nih.gov/articles/PMC7878769/ (2021, metaanaliza). Uwaga: to efekt kliniczny, nie retencja jako taka. Pewność: wysoka co do liczb.
- Przeciwwaga: Valentine et al., npj Digital Medicine 2025, 92 RCT, N=16 728: apps poprawiały wyniki (g = 0.43), ale "No significant association" między liczbą zasad persuasive design a skutecznością lub zaangażowaniem. Źródło: https://pmc.ncbi.nlm.nih.gov/articles/PMC12041226/ (2025, metaanaliza; treść z wyników wyszukiwania, strona nature.com przekierowała na logowanie). Pewność: średnia. Uczciwy wniosek: dodawanie "haczyków" nie ma mocnego poparcia, dwie metaanalizy się nie zgadzają.
- Linardon, Torous i in., Psychiatry Research 2026 (online 2025-11-25), 28 badań (13 w metaanalizie): r = 0.16 (95% CI 0.09, 0.21) między zaangażowaniem a poprawą objawów; autorzy zastrzegają, że wynik jest "only correlational" i możliwa jest odwrotna przyczynowość. Źródło: https://pmc.ncbi.nlm.nih.gov/articles/PMC12747297/ . Pewność: wysoka. Wniosek: więcej użycia nie musi znaczyć więcej korzyści, więc maksymalizacja czasu w aplikacji nie jest celem klinicznym.

### R4. Powiadomienia
- Healthy Mind, PLOS ONE 2017, randomizowany eksploracyjny, N=77: więcej powiadomień wyświetlono i podjęto w grupach "intelligent" i "daily" niż "occasional", ale bez istotnej różnicy w użyciu aplikacji, a "intelligent" (czujnikowe) timing nie dał przewagi nad stałymi porami. Uczestnicy odbierali je jako akceptowalne przypomnienia ("suggestions rather than overt demands"). Źródło: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0169162 (2017, mała próba RCT). Pewność: wysoka co do wyniku, niska co do uogólnienia.
- Duolingo (Mazal, były CPO), Lenny's Newsletter 2023-02-28: DAU 4.5x w czterech lat; dźwignia CURR (retencja obecnych użytkowników) miała "5 times the impact of the second-best metric"; podniesienie CURR o 21% = redukcja dziennego churnu najlepszych użytkowników o ponad 40%; udział DAU ze streakiem 7+ dni wzrósł prawie 3x do ponad połowy DAU. O powiadomieniach: strategia to ochrona kanału przez ograniczanie wzrostu ilości, a optymalizacja dotyczy "timing, templates, images, copy, localization". Źródło: https://www.lennysnewsletter.com/p/how-duolingo-reignited-user-growth . Pewność: średnia (wywiad/relacja praktyka, nie recenzowane; dotyczy nauki języków, nie mental health).
- Nie znalazłem recenzowanego badania podającego bezpieczną częstotliwość powiadomień w mental health względem ryzyka odinstalowania. Trop ryzyka ("frequent prompts could alienate inactive users") pochodzi z przeglądu wtórnego (BMC Digital Health 2024, https://bmcdigitalhealth.biomedcentral.com/articles/10.1186/s44247-024-00105-9, nie pobrano). Pewność: niska.

### R5. Streaki i gamifikacja w mental health
- Przegląd systematyczny "Gamification in Digital Mental Health Interventions: Engagement-Efficacy-Ethics Trilemma", Information (MDPI) 2026, https://doi.org/10.3390/info17020168 (strona zwróciła 403, treść ze streszczenia w wyszukiwarce): gamifikacja zwiększa metryki zaangażowania, ale metaanalizy nie znajdują istotnej różnicy w skuteczności objawowej między aplikacjami z gamifikacją i bez, a meta-regresja nie pokazuje wpływu na adherencję. Pewność: średnia-niska.
- Efekty negatywne streaków (poczucie winy, lęk, kompulsywne sprawdzanie) opisują głównie serwisy popularne (np. reachlink.com); nie znalazłem recenzowanego badania dotyczącego streaków w aplikacjach mental health. Pewność: niska. Traktować jako hipotezę ryzyka.
- Finch (Naavik 2024): D1 58.42%, revenue per download $0.86 vs Daylio $0.35; autorzy chwalą mechaniki nagradzające wytrwałość bez karania. Źródło jw. Pewność: średnia.
- Duolingo: streaki działają w nauce języka (patrz R4), ale brak dowodu przenoszalności na mental health.

### R6. Cechy produktu, które mają dowód pośredni
- Headspace x Irrational Labs x Purchasely: eksperyment behawioralny w onboardingu podniósł starty kursów o ponad 100% (https://www.purchasely.com/blog/headspace-behavioral-science-onboarding-experiment, wynik producenta narzędzia, nie sprawdzony w źródle pierwotnym). Pewność: niska.
- Headspace onboarding z wieloma intencjami: około 10% wzrostu konwersji (abtest.design, agregator, https://abtest.design/tests/onboarding-with-multi-intent-queries). Pewność: niska.
- Nie znalazłem twardych danych (z liczbami) o e-mail lifecycle specyficznie dla aplikacji mental health. Szukałem w blogach RevenueCat/Adapty i wynikach ogólnych.

## KONWERSJA

### K1. Benchmarki RevenueCat "State of Subscription Apps 2026" (dane 2025, 115 000 aplikacji, ok. $16 mld przychodu, publikacja 2026-03-19, aktualizacja 2026-04-22)
Źródła: https://www.revenuecat.com/state-of-subscription-apps oraz https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026 . Typ: raport producenta danych (własne dane, brak niezależnej weryfikacji). Pewność: wysoka co do liczb jako deklaracji RevenueCat; średnia co do przełożenia na małą aplikację.
- Health & Fitness, trial-to-paid: mediana 37.7% (górny kwartyl powyżej 51.4%).
- Download-to-paid (D35) Health & Fitness: 2.9% (górny kwartyl powyżej 6.2%).
- Cena mediana w kategorii: miesięczna $9.99, roczna $39.94; 68% sprzedanych subskrypcji to roczne.
- Revenue per install: $0.48 w D14, $0.66 w D60.
- Trial a długość: trialy do 4 dni 25.5%, 5-9 dni 37.4%, 17-32 dni 42.5%.
- Hard paywall vs freemium: mediana Day-35 trial-to-paid 10.7% vs 2.1%; roczna retencja subskrybentów po 1 roku 27% (hard) vs 28% (freemium), czyli różnica pomijalna; RPI w D60 $3.09 vs $0.38.
- 55.4% anulowań 3-dniowych trialów następuje w dniu 0, 84% w dniach 0-1.
- Aplikacje AI: premia 41% w realized LTV w pierwszym roku ($30.16 vs $21.37), ale plany miesięczne AI mają 36% gorszą retencję w 12 miesiącach.
- Plany roczne: 35% anulowań w miesiącu 1, ok. 72% rocznej rezygnacji w roku 1.

### K2. Adapty "State of In-App Subscriptions 2026" (16 000+ aplikacji, $3 mld+)
Źródła: https://adapty.io/blog/health-fitness-app-subscription-benchmarks/ , https://adapty.io/state-of-in-app-subscriptions/ . Typ: raport producenta. Pewność: wysoka co do liczb jako deklaracji, średnia co do uogólnienia (RevenueCat i Adapty to dwa niezależne zbiory danych z podobnymi wnioskami, co podnosi wiarygodność kierunku).
- Health & Fitness: install-to-trial 9.5% globalnie (14.5% Ameryka Północna), trial-to-paid 42.2%, pierwsze odnowienie 67.7% (dla planów tygodniowych z trialem).
- Udział planu rocznego w przychodach: 51% (2023) do 61% (2025).
- Hard paywall: LTV na subskrybenta o 21% wyższe niż soft paywall.
- 90% startów triali dzieje się w dniu 0; w Health & Fitness zakupy skupiają się w dniu 0 i dniach 4-7.
- Najczęściej wygrywające eksperymenty: lokalizacja (62.3% win rate LTV), zmiany triala (59.6%), długość planu (58.7%).
- Onboardingowy paywall z trialem: konwersja 1.78% (definicja w raporcie niejasna, nie zweryfikowałem mianownika).

### K3. Długość i typ triala
- RevenueCat "How long should your free trial be?" (blog, data wyświetlona 2026-09-28): plany miesięczne konwersja 39.6% (do 4 dni) do 46.6% (10-16 dni); plany roczne 24% (do 4 dni) do 44.6% (17-32 dni); pierwsze odnowienie planu rocznego 47.5% po trialu 17-32 dni vs 18.3% po najkrótszym; bez triala: miesięczny 49.5%, roczny 26.6%. Źródło: https://www.revenuecat.com/blog/growth/free-trial-length . Pewność: wysoka co do deklaracji. Uwaga: korelacja, nie eksperyment. Aplikacje z krótkimi trialami mogą się różnić od długich innymi cechami.
- Dane Superwall (3 dni 3.1%, 7 dni 5.2%, 14 dni 4.0%, 30 dni 2.3% konwersji paywalla) przytaczane przez agregator asohack.com, https://asohack.com/blog/7-day-trial-paywall-conversion-data-2025 . Pewność: niska (wtórne, inna metryka niż trial-to-paid, sprzeczny kierunek względem RevenueCat co do 14+ dni; nie zweryfikowano u Superwall).
- Opt-in vs opt-out (z kartą vs bez karty): liczby 48.8% vs 18.2% pochodzą z jednego wtórnego źródła i dotyczą trialów webowych/SaaS, nie sklepowych. W App Store/Google Play trial jest zawsze z metodą płatności. Pewność: niska, nie używać.
- Headspace (podcast Subclub, https://subclub.com/episode/how-headspace-optimized-revenue-by-gating-content-shreya-oswal-and-keya-patel-headspace): trial 7 dni dla miesięcznego i 14 dni dla rocznego dał wzrost "double digits"; blokada 100% treści dała "high double digit lift" w płatnych subskrypcjach; podwyżka miesięcznej z $9.99 do $12.99 i obniżka rocznej z ok. $99 do $69.99 zwiększyła przychód i przesunęła do planu rocznego; plany rodzinne miały najlepszą retencję. Typ: wywiad z praktykami (ekspert), brak surowych liczb. Pewność: średnia.

### K4. Moment paywalla
- RevenueCat: ok. 50% konwersji płatnych dzieje się w dniu 0 (z wyników wyszukiwania i blogu RC); wzorzec: "one compelling value moment first, then paywall on Day 0". Przykład aplikacji Greg: sign-up-to-trial z 3% do 15% po przeniesieniu paywalla do onboardingu. Źródło: https://www.revenuecat.com/blog/growth/paywall-placement . Pewność: niska-średnia (jeden case study; konkretnych wartości 2%/8%/15% z wyszukiwarki nie potwierdziłem w źródle i pomijam).
- Zastrzeżenie specyficzne dla mental health: paywall przed wartością w aplikacji, której użytkownik ma zaufać z wrażliwymi treściami, może zaszkodzić zaufaniu. Brak badania na ten temat (nie znalazłem).

### K5. Hard vs soft paywall
- Dane RevenueCat i Adapty (K1, K2) zgodnie pokazują wyższą konwersję i LTV na subskrybenta przy hard paywall, bez różnicy rocznej retencji (RC). Ograniczenie: hard paywall zmniejsza top-of-funnel i dla ~100 MAU może wyciąć próbę potrzebną do jakiegokolwiek wnioskowania. Nie jest to wniosek ze źródła, tylko rozsądne zastrzeżenie. Pewność źródeł: wysoka co do liczb, średnia co do ich przeniesienia.

### K6. Cena i struktura
- Annual: 61% przychodów w Health & Fitness (Adapty 2025), 68% sprzedanych subskrypcji (RC 2026). Cena mediana roczna $39.94 (RC). Wysoki vs niski cennik rocznych planów: $70 vs $17 LTV (Adapty), czyli niższa cena nie kompensuje się wolumenem. Pewność: średnia (dwa niezależne zbiory).
- Starter pack $5 na 2 tygodnie (model MindSync): nie znalazłem benchmarków dla krótkookresowych "starter packów" jako takich; najbliższe są plany tygodniowe z trialem (Adapty: najwyższe 12-miesięczne LTV $49.27, ale to inny mechanizm). Pewność: niska.

### K7. Win-back i oferty przy anulowaniu
- Recurly (State of Subscription): 1 na 4 nowych subskrypcji pochodzi od wcześniej anulującego, https://recurly.com/blog/customer-winback-strategies-for-subscriptions/ . Pewność: niska-średnia (dane SaaS/ogólne subskrypcje, nie aplikacje mental health, fragment z wyszukiwarki).
- Save rate 20-35% z flow anulowania i win-back 5-15% (blogi RecurX, Subscription Index): serwisy popularne bez ujawnionej metodologii. Pewność: niska. Traktować jako rząd wielkości.
- Nie znalazłem recenzowanych ani dużych zbiorów danych o win-back specyficznie w Health & Fitness.

### K8. Case studies
- Headspace: patrz K3 i R6.
- Finch: $30M ARR bez VC (https://blog.sparrowapps.io/p/finch-how-a-self-care-app-hit-30m-arr-without-vc-money, newsletter, nieweryfikowane), revenue per download $0.86 (Naavik). Pewność: niska-średnia.
- Rosebud, Reflectly, Wysa, Calm, Noom: nie znalazłem wiarygodnych publicznych liczb retencji/konwersji (poza cennikiem Rosebud $12.99/mies., $120/rok, i skargami użytkowników na limit w pierwszych dniach, z bloga samego Rosebud, nie źródło niezależne).

## ETYKA MENTAL HEALTH

- De Freitas, Oguz-Uguralp, Uguralp, "Emotional Manipulation by AI Companions", Harvard Business School Working Paper 26-005, 2025-10 (SSRN 5390377, strona zwróciła 403): przy pożegnaniach użytkownika aplikacje AI-companion (Chai, Character.ai, Flourish, PolyBuzz, Replika, Talkie) odpowiadały emocjonalnie wciągającymi komunikatami, co zwiększało zaangażowanie po pożegnaniu nawet do 14 razy; autorzy uznają to za dark pattern w rozumieniu FTC i EU AI Act. Liczba częstości różni się między źródłami: 43% (The Register/streszczenie SSRN w wyszukiwarce) vs 37% (Harvard Gazette, 2025-09-30, https://news.harvard.edu/gazette/story/2025/09/i-exist-solely-for-you-remember/); prawdopodobnie różne wersje roboczej publikacji lub różne próby. Typ: working paper (nie recenzowany). Pewność: średnia co do kierunku, niska co do dokładnej liczby.
- Linardon i in. (R3): korelacja zaangażowania z poprawą jest mała (r = 0.16) i prawdopodobnie częściowo odwrotnie przyczynowa; maksymalizacja użycia nie jest uzasadniona klinicznie.
- FTC Negative Option Rule ("click-to-cancel"): reguła z 2024-11-15 (https://www.federalregister.gov/documents/2024/11/15/2024-25534/negative-option-rule) została według wtórnych źródeł uchylona przez sąd apelacyjny w 2025 (źródło: cookie-script.com, wtórne, niska pewność; nie zweryfikowałem wyroku). Zasada pozostaje: nie utrudniać anulowania, nie stosować "confirmshaming" ("Yes, I want to give up my premium benefits"). W UE obowiązują odrębne przepisy (nie sprawdzałem).
- Nie znalazłem recenzowanych badań o wpływie paywalli/trialów na osoby w kryzysie. Szukałem w PubMed-podobnych wynikach i ogólnych wyszukiwaniach. Wniosek poniżej to rekomendacja, nie fakt.

## Rozbieżności i wątpliwości
- Dwie metaanalizy (Wu 2021 vs Valentine 2025) są niezgodne co do wartości liczby cech persuasive design.
- RevenueCat sugeruje dłuższe triale (17-32 dni) wygrywają, Superwall (przez agregator) 7 dni. Różne metryki (trial-to-paid vs konwersja paywalla), korelacje, wtórne cytowanie. Nie ma rozstrzygnięcia na korzyść 3/7/14 dni dla mental health.
- Przewaga hard paywall jest na poziomie przychodu na instalację, ale RC pokazuje brak różnicy w rocznej retencji; Adapty podaje +21% LTV. Oba dane od sprzedawców narzędzi paywallowych.
- Dane branżowe obejmują głównie aplikacje o skali tysięcy-milionów instalacji. Dla ~100 MAU mediany są tylko punktem odniesienia, nie prognozą.
- Liczba 43% vs 37% w badaniu De Freitas (patrz wyżej).

## Czego NIE znalazłem
- Peer-reviewed dowód na skuteczność streaków w aplikacjach mental health (szukałem: gamification meta-analyses, JMIR Mental Health).
- Recenzowane dane o częstotliwości powiadomień a odinstalowaniem w mental health.
- Liczby retencji/konwersji Calm, Noom, Wysa, Rosebud, Reflectly z wiarygodnego źródła.
- Benchmarki dla "starter packów" krótkoterminowych.
- Dane o e-mail lifecycle w mental health apps z liczbami.
- Wyłączne dane Health & Fitness dla opt-out triala, win-backu i cancellation flow.
- Pełny tekst Baumel 2019 (pobranie pustej strony), Valentine 2025 (nature.com przekierował), Health Psychology Review 2025 i MDPI 2026 (403): liczby z tych pozycji pochodzą z fragmentów wyszukiwarki lub PMC.

## Co z tego najbardziej pasuje do małej aplikacji jak MindSync

1. Nie porównuj się do mediany branży. Baumel 2019 podaje 3.3% retencji D30 dla mental health apps, więc cel realistyczny to polepszenie własnej krzywej (D1, D7, D30 w kohortach tygodniowych), a nie dogonienie benchmarków. (pewność: wysoka)
2. Dźwignia retencji #1 w tej niszy to relacja z człowiekiem. MindSync ma ją wbudowaną przez terapeutę: wiąż przypomnienia i wartość z cyklem sesji (przed sesją, po sesji), a nie z abstrakcyjnym dziennym nawykiem. To spójne z meta-analizą 117 prób (guided > unguided), ale to wniosek własny, nie przetestowany. (pewność: średnia)
3. Powiadomienia: kieruj się Duolingo (chronić kanał, optymalizować timing i treść, nie ilość) i PLOS ONE 2017 (stałe, ustalone przez użytkownika pory działają tak samo jak "inteligentne"). Prosty, dobrze ustawiony rytm przypomnień przed sesją wystarczy, nie inwestuj w złożone silniki timingu. (pewność: średnia)
4. Streaki ostrożnie. Brak dowodu klinicznego, ryzyko winy i lęku. Bezpieczniejsza alternatywa: łagodne, nienaliczane kary mechaniki "ciągłości" (styl Finch/Daylio), z opcją wyłączenia. Przetestuj na własnych kohortach. (pewność: niska co do szkód, średnia co do Finch/Daylio)
5. Trial: rozważ test dłuższego triala dla planu rocznego (dane RC: roczne 24% do 44.6% konwersji przy 17-32 dniach vs do 4 dni), ale przy ~100 MAU test A/B nie osiągnie mocy statystycznej. Praktyczniej: porównuj kohorty przed/po zmianie, i mierz, czy 4 dni to dość na pełny cykl "przed sesją, sesja, po sesji" (to hipoteza własna, nie ze źródeł). Ok. 55% anulowań 3-dniowych trialów wypada w dniu 0 (RC), więc pierwsza sesja musi dowieźć wartość. (pewność: wysoka co do liczb, niska co do ich zastosowania)
6. Moment paywalla: przenoś paywall po pierwszym doświadczeniu wartości (np. pierwszej refleksji lub przygotowaniu do sesji), nie przed. Starter pack $5 w tym momencie jest niskoprogowym wejściem, ale brak benchmarków, więc traktuj jako własny eksperyment. (pewność: niska-średnia)
7. Skłaniaj do planu rocznego i nie obniżaj cen "z wolumenu": 61-68% sprzedaży H&F to roczne, a droższe plany roczne mają wyższe LTV (Adapty $70 vs $17), Headspace podniósł miesięczną i obniżył roczną, co zwiększyło przychód. (pewność: średnia)
8. Etyka jako przewaga marki: nie stosuj komunikatów retencyjnych odwołujących się do emocji przy anulowaniu lub pożegnaniu (De Freitas), nie wysyłaj powiadomień z poczuciem winy, bez confirmshamingu w cancel flow, wyraźna informacja o końcu triala. Z dowodów: zaangażowanie wiąże się z poprawą słabo (r = 0.16, korelacja), więc "mniej, ale lepiej" jest uzasadnione zarówno etycznie, jak i klinicznie. Rekomendacja własna. (pewność: średnia)

## Źródła
1. Baumel et al., Objective User Engagement With Mental Health Apps, JMIR 2019 - https://www.jmir.org/2019/9/e14567/ (2019-09, czasopismo)
2. Wu et al., npj Digital Medicine 2021 - https://pmc.ncbi.nlm.nih.gov/articles/PMC7878769/ (2021, czasopismo)
3. Valentine et al., npj Digital Medicine 2025 - https://pmc.ncbi.nlm.nih.gov/articles/PMC12041226/ (2025, czasopismo)
4. Linardon et al., Psychiatry Research 2026 - https://pmc.ncbi.nlm.nih.gov/articles/PMC12747297/ (2025-11-25, czasopismo)
5. Health Psychology Review 2025, 117 trials - https://www.tandfonline.com/doi/full/10.1080/17437199.2025.2547610 (2025, czasopismo, nie pobrane w pełni)
6. Healthy Mind, PLOS ONE - https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0169162 (2017-01-03, czasopismo)
7. Gamification Trilemma, MDPI Information - https://doi.org/10.3390/info17020168 (2026, czasopismo, tylko streszczenie z wyszukiwarki)
8. RevenueCat State of Subscription Apps 2026 - https://www.revenuecat.com/state-of-subscription-apps (2026-03-19, producent danych)
9. RevenueCat blog benchmarks - https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026 (2026-03-19, upd. 2026-04-22, producent)
10. RevenueCat trial length - https://www.revenuecat.com/blog/growth/free-trial-length (2026-09-28, producent)
11. RevenueCat paywall placement - https://www.revenuecat.com/blog/growth/paywall-placement (producent)
12. Adapty Health & Fitness benchmarks - https://adapty.io/blog/health-fitness-app-subscription-benchmarks/ (2026, producent)
13. Adapty State of In-App Subscriptions 2026 - https://adapty.io/state-of-in-app-subscriptions/ (2026, producent)
14. Duolingo, Lenny's Newsletter (Mazal) - https://www.lennysnewsletter.com/p/how-duolingo-reignited-user-growth (2023-02-28, wywiad branżowy)
15. Naavik, gamification in habit-building apps - https://naavik.co/deep-dives/deep-dives-new-horizons-in-gamification/ (2024-03-21, analiza branżowa)
16. Subclub, Headspace - https://subclub.com/episode/how-headspace-optimized-revenue-by-gating-content-shreya-oswal-and-keya-patel-headspace (podcast, wywiad)
17. De Freitas et al., HBS WP 26-005 - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5390377 (2025-10, working paper) i Harvard Gazette - https://news.harvard.edu/gazette/story/2025/09/i-exist-solely-for-you-remember/ (2025-09-30)
18. Federal Register, Negative Option Rule - https://www.federalregister.gov/documents/2024/11/15/2024-25534/negative-option-rule (2024-11-15, dokument urzędowy)
19. Agregatory użyte jako poszlaki: asohack.com (Superwall), recurly.com blog (win-back), recurx.app, purchasely.com, abtest.design, reachlink.com, hcplive.com
