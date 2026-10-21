# MindSync: opis w sklepach na następne wydanie (EN-US)

Status: **AKCEPT brand-voice-manager 2026-10-19 po poprawkach; czeka na decyzje operatora (sekcja D)**.

Copy jest po angielsku (pisownia US), notatki po polsku. Każde pole przeszło humanizer w trybie
embedded z próbką głosu `docs/blog/voice-sample-monika.md`. Znaki liczyłem mechanicznie na plikach
roboczych (koniec linii LF = 1 znak, bez końcowego entera). Tekst do wklejenia jest w blokach kodu,
dokładnie tak, jak ma trafić do App Store Connect i Play Console.

Skąd fakty: `mindsync-frontend-wt-store-shots/mindsync_app/lib/l10n/app_en.arb` (nowy Main,
Character, pierwsza rozmowa, What Orca remembers, limity Free), `blog/app-features.json` (tylko
`live`), polityka prywatności mindsync.app z 25.07.2026 (szyfrowanie, kasowanie audio, brak reklam),
strona mindsync.app/about (historia założyciela). Statystyka: Jensen-Doss i in. 2018 (sekcja D).

Kiedy wgrywać: razem z wersją sklepową, która ma nowy Main i Character (tak jak screeny w
`store/copy.md` §4). Promotional text w App Store można podmienić później bez wydania.

---

## A. App Store

### A1. Name (limit 30)

```
MindSync: Therapy Journal
```
25 / 30 znaków. Dwukropek jako separator, łącznik tylko w wyrazach złożonych. Słowa kluczowe
z nazwy bez zmian.

Operator może zostawić obecne `MindSync - Therapy Journal` (26 / 30), jeśli nie chce zmiany nazwy
w review.

### A2. Subtitle (limit 30)

Rekomendacja:
```
Keep more from every session
```
28 / 30 znaków.

Wariant zachowawczy (obecny): `The smarter way to do therapy` (29 / 30). Jeśli zostaje, w keywords
zamień `summary` na `session` (patrz A5).

### A3. Promotional text (limit 170)

```
See your therapy week on one screen: next session, agenda, to-dos and habits. A new Character tab shows your strengths growing from what you write and say.
```
155 / 170 znaków.

### A4. Description (limit 4000)

```
You pay for therapy every week. Then a friend asks what you talked about, and all you have is a feeling and maybe one word.

MindSync helps you keep it. After a session, talk or type for a few minutes. The app turns it into a card with the topics, questions, to-dos and realizations from that hour. The day before your next session, a Before therapy card sums up what came up since last time, so you walk in knowing where to start.

YOUR THERAPY WEEK AT A GLANCE

Main is your home screen. Eight tiles show what's waiting right now: your next session, Therapy Agenda, to-dos, the last seven days of your habits, Focus Areas, therapy relationship, weekly observations and a daily affirmation.

New here? Main gives you a first-week plan: eight small steps of a few minutes each, with no fixed days. Finish one and the next one opens. A daily reminder is optional.

SEE YOUR STRENGTHS GROW

Change is hard to see from the inside. Character shows it, built from your notes, your talks with Orca and your sessions. Six strengths (Courage, Insight, Honesty, Resilience, Kindness and Commitment) grow each time they show up in what you share. Opening the app doesn't count.

Your map lists the feelings you're working on and the skills you're building around each one, and your level rises as those skills grow. If a moment doesn't sound like you, tap Not quite and it stops counting.

MEET ORCA

Orca is MindSync's AI therapy assistant for the days between sessions. It isn't a therapist and doesn't replace yours. Its job is to help you remember and prepare.

Right after sign-up, Orca asks three short questions, by voice or in writing, and sums up what it heard. Your first Before therapy card starts from that summary. When something comes up midweek, talk it through with Orca in Reflect, and tap any past talk to read it again. In Settings, What Orca remembers lists every note Orca keeps, and you can delete any of them.

EVERYTHING BETWEEN SESSIONS IN ONE PLACE

MindSync picks out topics, questions, to-dos and realizations from what you write and record. The app suggests, you decide. Workspace holds your Agenda, To-do, Questions, Goals, Threads (themes that keep coming back), Realizations and check-ins on your therapy relationship. Timeline keeps every entry in order, with filters at the top.

WHY IT MATTERS

MindSync exists because its founder spent 10 years and $130,000 on therapy and couldn't tell if it was working.

In a survey published in 2018, Jensen-Doss and colleagues asked 504 US mental health clinicians about tracking progress. Overall, they liked the idea, but only 13.9% used a standard questionnaire at least once a month (Administration and Policy in Mental Health). MindSync gives you your own record to bring to your next session.

WHAT YOU GET

Session recording with a summary of topics, questions and to-dos (ask your therapist first)
Between Sessions voice notes, transcribed for you
Focus Areas: rate sleep, worry or anything else you track from 1 to 10, and read the trend in plain words
Habits to keep, or to stay free of
Goals with a short written update on where you stand
Weekly and monthly summaries
Reminders you can switch on and off one by one

PRIVACY

Your data is encrypted in transit and at rest (AES-256). MindSync deletes the audio from voice notes and recordings once the transcript exists. There are no ads, and MindSync never sells your data.

FREE TO START

You get 4 days of Premium free, and nothing is charged automatically. After that, the Free plan includes a limited number of cards, notes and Reflect messages each month, plus a small number of session recordings. Premium keeps every feature unlimited and includes voice talks with Orca.

MindSync isn't a crisis service. In the US, call or text 988 any time. If you might be in danger, call your local emergency number.

Terms of Use (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
Privacy Policy: https://mindsync.app/privacy-policy
```
3974 / 4000 znaków.

### A5. Keywords (limit 100, bez spacji po przecinkach)

```
notes,prep,counseling,mood,tracker,mental,health,diary,anxiety,symptom,reflection,recorder,summary
```
98 / 100 znaków. Bez słów z nazwy i podtytułu (mindsync, therapy, journal, keep, more, from, every,
session). Apple łączy słowa z nazwy, podtytułu i keywords, więc `notes` daje "therapy notes",
`prep` daje "therapy prep", `recorder` daje "therapy session recorder", `symptom` + `tracker` daje
"symptom tracker".

Świadomie pominięte: `ai` (w parze z "therapy" z nazwy dałoby dopasowanie do "ai therapy", a tej
ramy zabrania brand-instagram.md §4.1), `therapist` (dopasowanie do "ai therapist" i do osób, które
szukają terapeuty, a nie narzędzia), `cbt` (apka nie prowadzi CBT, Apple 2.3.7 zabrania mylących
słów kluczowych).

### A6. What's New (limit 4000)

```
Main, a new home screen. Eight tiles show your next session, Therapy Agenda, to-dos, the last seven days of your habits, Focus Areas, therapy relationship, weekly observations and a daily affirmation. Tap one to open it in full.

A first-week plan on Main: eight small steps with no fixed days. Finish one and the next one opens. A daily reminder is optional.

Character, rebuilt. Six strengths grow from what you write and say, your skills sit on a map under the feelings they help with, and your level rises as those skills grow. Tap Not quite to remove a moment that doesn't fit.

Right after sign-up, there's now a first conversation with Orca, MindSync's AI therapy assistant for the days between sessions. Orca isn't a therapist. It asks three short questions, by voice or in writing, and your first Before therapy card starts from its summary.

What Orca remembers, in Settings: read every note Orca keeps and delete any of them.

Also: redesigned cards and Workspace, filters at the top of Timeline, and past Reflect talks you can open and read.
```
1053 / 4000 znaków. Pominięte celowo: silnik głosowy Live (tylko podgląd w Settings), ekrany zgód
i wszystko za flagą.

---

## B. Google Play

### B1. Title (limit 30)

```
MindSync: Therapy Journal
```
25 / 30 znaków. Ta sama nazwa co w App Store (obecnie na Play: "MindSync - Smarter Therapy").

### B2. Short description (limit 80)

```
Remember what you talk about in therapy and walk into the next session ready.
```
77 / 80 znaków.

Wariant: `Notes after therapy, prep before the next session, and patterns in between.` (75 / 80).

### B3. Full description (limit 4000)

Nagłówki sekcji są tu zdaniami, a nie WERSALIKAMI: Play podaje "ALL CAPS although not part of brand
name" jako przykład naruszenia zasad metadanych. Poza nagłówkami i linkami na końcu treść jest
identyczna z A4. Linii z ceną nie ma, bo Play sam pokazuje cenę.

```
You pay for therapy every week. Then a friend asks what you talked about, and all you have is a feeling and maybe one word.

MindSync helps you keep it. After a session, talk or type for a few minutes. The app turns it into a card with the topics, questions, to-dos and realizations from that hour. The day before your next session, a Before therapy card sums up what came up since last time, so you walk in knowing where to start.

Your therapy week at a glance

Main is your home screen. Eight tiles show what's waiting right now: your next session, Therapy Agenda, to-dos, the last seven days of your habits, Focus Areas, therapy relationship, weekly observations and a daily affirmation.

New here? Main gives you a first-week plan: eight small steps of a few minutes each, with no fixed days. Finish one and the next one opens. A daily reminder is optional.

See your strengths grow

Change is hard to see from the inside. Character shows it, built from your notes, your talks with Orca and your sessions. Six strengths (Courage, Insight, Honesty, Resilience, Kindness and Commitment) grow each time they show up in what you share. Opening the app doesn't count.

Your map lists the feelings you're working on and the skills you're building around each one, and your level rises as those skills grow. If a moment doesn't sound like you, tap Not quite and it stops counting.

Meet Orca

Orca is MindSync's AI therapy assistant for the days between sessions. It isn't a therapist and doesn't replace yours. Its job is to help you remember and prepare.

Right after sign-up, Orca asks three short questions, by voice or in writing, and sums up what it heard. Your first Before therapy card starts from that summary. When something comes up midweek, talk it through with Orca in Reflect, and tap any past talk to read it again. In Settings, What Orca remembers lists every note Orca keeps, and you can delete any of them.

Everything between sessions in one place

MindSync picks out topics, questions, to-dos and realizations from what you write and record. The app suggests, you decide. Workspace holds your Agenda, To-do, Questions, Goals, Threads (themes that keep coming back), Realizations and check-ins on your therapy relationship. Timeline keeps every entry in order, with filters at the top.

Why it matters

MindSync exists because its founder spent 10 years and $130,000 on therapy and couldn't tell if it was working.

In a survey published in 2018, Jensen-Doss and colleagues asked 504 US mental health clinicians about tracking progress. Overall, they liked the idea, but only 13.9% used a standard questionnaire at least once a month (Administration and Policy in Mental Health). MindSync gives you your own record to bring to your next session.

What you get

Session recording with a summary of topics, questions and to-dos (ask your therapist first)
Between Sessions voice notes, transcribed for you
Focus Areas: rate sleep, worry or anything else you track from 1 to 10, and read the trend in plain words
Habits to keep, or to stay free of
Goals with a short written update on where you stand
Weekly and monthly summaries
Reminders you can switch on and off one by one

Privacy

Your data is encrypted in transit and at rest (AES-256). MindSync deletes the audio from voice notes and recordings once the transcript exists. There are no ads, and MindSync never sells your data.

Free to start

You get 4 days of Premium free, and nothing is charged automatically. After that, the Free plan includes a limited number of cards, notes and Reflect messages each month, plus a small number of session recordings. Premium keeps every feature unlimited and includes voice talks with Orca.

MindSync isn't a crisis service. In the US, call or text 988 any time. If you might be in danger, call your local emergency number.
```
3834 / 4000 znaków.

### B4. Release notes (limit 500)

```
Main is a new home screen with your next session, agenda, to-dos and habits.
A first-week plan with eight small steps. Finish one and the next one opens.
Character, rebuilt: six strengths that grow from what you write and say, and a map of your skills.
After sign-up, you have a first talk with Orca, your AI therapy assistant between sessions. Orca isn't a therapist.
What Orca remembers, in Settings: read and delete Orca's notes.
Redesigned cards and Workspace, plus filters on Timeline.
```
490 / 500 znaków.

---

## C. Co się zmieniło i dlaczego

| Pole | Obecnie | Teraz | Dlaczego |
|---|---|---|---|
| AS name | MindSync - Therapy Journal | MindSync: Therapy Journal | Dwukropek jako separator, łącznik tylko w wyrazach złożonych (reguła typograficzna). Te same słowa kluczowe ("therapy" + "journal"). Operator może zostawić starą nazwę, jeśli nie chce zmiany nazwy w review. |
| AS subtitle | The smarter way to do therapy | Keep more from every session | Konkretna korzyść zamiast ogólnika. To druga linia pozycjonowania marki, więc głos się zgadza. "session" dochodzi jako nowe słowo indeksowane ("therapy" jest już w nazwie). "Smarter therapy" da się czytać jako obietnicę lepszej terapii (YMYL). |
| AS promotional text | brak danych | tydzień terapii na jednym ekranie + nowa zakładka Character | Linia nad opisem, zmienia się bez wydania. Wersja po akcepcie zaczyna od tego, co użytkownik zobaczy, a nie od nazwy ekranu "Main", której nowa osoba jeszcze nie zna. Po kilku tygodniach warto ją podmienić na stały komunikat. |
| AS description | hook "$200... forgotten half", sekcja "NEW: YOUR WORKSPACE", testimoniale, 65%/80%, "2,000+", "Try it free. Full access. No credit card." | hook o płaceniu i zapominaniu bez niesprawdzalnych liczb; sekcje Main, Character, Orca, Workspace; źródłowa statystyka; prywatność z polityki; uczciwy opis Free i Premium; zdanie kryzysowe z 988; link do Privacy Policy | Hook został, ale "$200" i "half" nie miały źródła, więc obraz zastąpiło rozpoznanie w stylu Moniki (zdanie z naszego wpisu o zapamiętywaniu sesji). Workspace nie jest już nowością, nowością są Main i Character. Orca nazwana zgodnie z §4.1 (AI therapy assistant, między sesjami, nie terapeuta). Opis Free i Premium wymaga Apple 2.3.2 (czytelnik musi wiedzieć, co jest płatne), a "Full access. No credit card." nie zgadzało się z apką: trial ma 4 dni, potem Free z limitami. Usunięte bez źródła: 65%, 80%, 2,000+, testimoniale, "3-5 minutes", "Not a chatbot that agrees with everything". Badanie Jensen-Doss podane uczciwie wobec terapeutów: oceniali monitorowanie postępów dobrze, a mimo to rzadko go używali (tak mówi abstrakt). Zdanie kryzysowe ma 988, bo listing jest na USA. |
| AS keywords | brak danych | 13 słów, 98 znaków | Bez powtórek z nazwy i podtytułu, frazy pod intencje osób w terapii (notatki, przygotowanie, nastrój, objawy, nagranie sesji). Wykluczenia opisane w A5. |
| AS What's New | "New Activation flow, better conversation, UI fixes" | lista realnych zmian zwykłymi zdaniami | "Activation flow" to żargon zespołu. Czytelnik ma wiedzieć, co zobaczy po aktualizacji. Akapit o pierwszej rozmowie mówi wprost, że Orca nie jest terapeutą (Orca jest tam tematem, więc §4.1 tego wymaga). |
| Play title | MindSync - Smarter Therapy | MindSync: Therapy Journal | Jedna nazwa w obu sklepach, z dwukropkiem jako separatorem. "Journal" to fraza kategorii, której ludzie szukają. "Smarter Therapy" to ten sam problem YMYL co subtitle. |
| Play short description | brak danych | Remember what you talk about in therapy... | Główny ból (zapominanie) i korzyść (przygotowanie) w jednym zdaniu, z frazami "therapy" i "session". Bez "New", "Best", ceny i wezwań do pobrania. |
| Play full description | jak AS + "ALSO NEW", "PDFs you can share with your therapist", "$12.99/month. The cost of 10 minutes of therapy. For 167 hours of support", "GDPR compliant", testimonial "Darek" | treść identyczna z AS, nagłówki zdaniami, bez linii z ceną i bez linków EULA | Linia z ceną wypadła, bo Play sam pokazuje cenę, a opis ma być taki sam jak w App Store. Play podaje jako naruszenia: WERSALIKI poza nazwą marki i nieprzypisane albo anonimowe opinie. Eksportu PDF nie ma w arb, a udostępnianie terapeucie ma status `planned`, więc obie obietnice wypadły. Porównanie "10 minutes of therapy" nie ma źródła, a "167 hours of support" sugeruje usługę wsparcia. "GDPR compliant" to twierdzenie prawne, a kwestie zgód (prawnik M-3, bramka ART9) są otwarte. |
| Play release notes | brak danych | 6 linii o realnych zmianach | Krótka wersja A6 w limicie 500 znaków. Pierwsza linia mówi, co jest na nowym ekranie; linia o Orce zawiera "Orca isn't a therapist". |

---

## D. Otwarte punkty dla operatora

**Wgranie blokuje tylko D5.** Pozostałe otwarte punkty to decyzje albo usprawnienia, które mogą
przyjść później. Zamknięte: D4, D7, D8, D11.

1. **Statystyki 65% i 80%.**
   - "65% of long-term therapy patients can't tell if it's working": nie znalazłem żadnego źródła
     (wyszukiwanie zwróciło tylko badanie Consumer Reports z 1995 roku, które mówi co innego).
     **Usunięte.**
   - "80% of therapists don't track outcomes": zastąpione liczbą ze źródła. Jensen-Doss i in.,
     "Monitoring treatment progress and providing feedback is viewed favorably but rarely used in
     practice", *Administration and Policy in Mental Health and Mental Health Services Research*
     45(1), 48-61, 2018, https://doi.org/10.1007/s10488-016-0763-0. Ogólnokrajowa ankieta 504
     klinicystów z USA (terapeuci AMHCA, pracownicy socjalni NASW, terapeuci par i rodzin AAMFT):
     13.9% używało standardowego kwestionariusza postępów co najmniej raz w miesiącu, 61.5% nigdy.
     Pełny tekst: https://pmc.ncbi.nlm.nih.gov/articles/PMC5495625/. Uwaga: artykuł wyszedł online
     w 2016 roku, numer czasopisma jest z 2018, stąd "published in 2018". Zdanie "Overall, they
     liked the idea" opiera się na abstrakcie, według którego klinicyści oceniali monitorowanie
     postępów i informację zwrotną ogólnie przychylnie.
2. **"2,000+ people already use MindSync".** Brak źródła danych. To samo zdanie stoi na
   mindsync.app/about ("2,000+ people already know"), ale bez liczby z bazy. Do potwierdzenia przez
   `database-administrator` (liczba kont) z rozróżnieniem kont i aktywnych użytkowników: "use"
   sugeruje aktywnych. Jeśli liczba się potwierdzi dla kont, bezpieczne brzmienie to
   "More than 2,000 people have signed up for MindSync." Do tego czasu zdanie zostaje poza opisem.
3. **Testimoniale.** W tym opisie nie ma żadnego. Żeby wrócić, każdy musi spełnić trzy warunki:
   prawdziwa osoba, która używała apki; zapisana zgoda na publikację; brak niejawnej relacji
   z firmą. Podstawa: reguła FTC 16 CFR Part 465 (w mocy od 21.10.2024), która zakazuje fałszywych
   opinii i opinii osób z wewnątrz firmy bez ujawnienia relacji, oraz zasady metadanych Play, które
   zakazują opinii nieprzypisanych i anonimowych w opisie. Konkretnie:
   - **Darek** ("This app helped me see the patterns..."): jeśli to Darek z zespołu MindSync,
     opinia bez ujawnienia relacji łamie zasadę FTC o opiniach insiderów. Nie przywracać.
   - **Kate, therapist** (wersja App Store): "they have data to share" obiecuje udostępnianie
     terapeucie, które ma status `planned`. Treści opinii nie edytujemy, więc tej wersji nie da się
     użyć. Wersja z Play ("We spend the session working, not recapping") jest do przywrócenia, jeśli
     spełnia trzy warunki wyżej.
   - **Martha**: do przywrócenia po potwierdzeniu trzech warunków. Samo imię to na Play granica
     "attributed"; bezpieczniej imię i inicjał nazwiska albo miasto, tak jak na slajdzie 9.
   - Slajd 9 w App Store (Rachel K., Austin, TX) to osobna sprawa, opisana w `store/copy.md` §4.
4. **ZAMKNIĘTE: cena.** Linia z ceną wypadła z opisu Play: Play sam pokazuje cenę, a opis jest
   taki sam jak w App Store. W żadnym sklepie nie ma cen w opisie. Stare porównanie "The cost of
   10 minutes of therapy" też zostaje usunięte.
5. **BLOKUJE WGRANIE: polityka prywatności.** Zdania o szyfrowaniu (AES-256), kasowaniu audio,
   braku reklam i niesprzedawaniu danych pochodzą z polityki prywatności z 25.07.2026. Na tej
   samej stronie (mindsync.app/privacy-policy) wisi jednak stara, niedatowana wersja v1 z innymi
   warunkami (m.in. przechowywanie do roku). Opis w sklepie odsyła do tej strony, więc **v1 musi
   zniknąć z mindsync.app/privacy-policy przed wgraniem opisu**. Przy okazji niech
   `integration-devops` potwierdzi, że szyfrowanie AES-256 w spoczynku dotyczy faktycznego dostawcy
   bazy (w komentarzach kodu jest Heroku Postgres na EBS, w CLAUDE.md Azure).
6. **"GDPR compliant"** usunięte z Play: to twierdzenie prawne, a sprawy zgód (prawnik M-3, bramka
   ART9) są otwarte. Wraca dopiero po zielonym świetle od prawnika.
7. **ZAMKNIĘTE: historia założyciela.** "10 years and $130,000" ma źródło na mindsync.app/about
   ("MindSync exists because one person spent 10 years in therapy and $130,000 and couldn't tell
   if it was working."), a to, że chodzi o założyciela, potwierdza brand doc §1 (założona przez
   klienta terapii, który wydał na nią około 130 tys. USD w ciągu 10 lat). "its founder" zostaje.
8. **ZAMKNIĘTE: plan pierwszego tygodnia ma osiem kroków.** Dziesięć definicji w arb
   (`mc_wkSetup`, `Talk`, `Session`, `Note`, `Checkin`, `Agenda`, `Habit`, `Recap`, `Talk2`,
   `Question`) to pula, z której apka składa plan: kroki na pozycjach 3 i 6 zależą od tego, czy
   osoba chodzi na terapię. Użytkownik zawsze widzi osiem, więc "eight small steps" zostaje.
9. **Limity Free.** W opisie nie ma liczb (1 Before therapy, 1 After therapy, 3 Between Sessions,
   15 wiadomości Reflect miesięcznie, 2 nagrania łącznie), bo backend podaje je dynamicznie
   (`GET /users/usage`) i mogą się zmienić bez wydania. "4 days of Premium" jest w tekstach apki na
   sztywno; jeśli długość triala się zmieni, opis trzeba poprawić.
10. **Słowa kluczowe bez danych o wolumenie.** Ahrefs Keywords Explorer nie wchodzi w obecny plan
    Ahrefs, więc wolumenów nie dało się sprawdzić. Lista do sprawdzenia, gdy będzie dostęp
    (Keywords Explorer albo inne narzędzie ASO, US): "therapy notes", "therapy journal", "therapy prep",
    "session notes", "mood tracker", "symptom tracker", "counseling journal", "therapy recorder".
    Słowa z niskim wolumenem podmienić na kolejne z listy kandydatów: `psychology`, `selfcare`,
    `wellbeing`, `emotions`, `habit`.
11. **ZAMKNIĘTE: kryzys.** 988 dopisane w obu opisach: "MindSync isn't a crisis service. In the
    US, call or text 988 any time. If you might be in danger, call your local emergency number."
12. **Katalog funkcji.** `blog/app-features.json` nie ma Main, Habits, planu pierwszego tygodnia,
    Character v2 ani What Orca remembers (to samo zgłasza `store/copy.md` §4). Fakty o nich wziąłem
    z arb. Katalog trzeba zaktualizować, zanim blog i IG zaczną używać tych nazw.

---

## Kontrole przed akceptem

- [x] Humanizer na każdym polu, próbka głosu Moniki (otwarcie od rozpoznania, jedna puenta
  "Change is hard to see from the inside." wzięta z tekstu apki, badanie opowiedziane z rokiem).
- [x] Zero U+2014 i U+2013 w całym pliku (sprawdzone mechanicznie po zapisie).
- [x] Fakty tylko z arb (worktree store-shots), katalogu (`live`), polityki prywatności i /about.
- [x] YMYL: brak obietnic skuteczności terapii, diagnoz i leczenia; Orca nazwana według §4.1,
  w parze z "between sessions" i "isn't a therapist"; zdanie o kryzysie z 988.
- [x] Poprawki brand-voice-manager z 2026-10-19 wprowadzone (A1, A3, A4, A6, B1, B3, B4), każdy
  zmieniony fragment przeszedł humanizer, a każde zmienione pole policzone mechanicznie od nowa.
- [x] Play: brak "New", "Best", "#1", rankingów, cen w tytule, wezwań typu "Download now",
  anonimowych opinii i WERSALIKÓW w nagłówkach.
- [x] App Store: brak cen, opis tego, co jest płatne (2.3.2), link do EULA.
- [x] Pominięte: silnik Live, ekrany zgód, funkcje za flagą, udostępnianie terapeucie (`planned`).
