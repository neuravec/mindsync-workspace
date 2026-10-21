# Partia 1 – briefy wpisów (ETAP B)

> Data: 2026-08-25. Autor briefów: `seo-content-writer`. Wykonawca prozy: `blog-writer`
> (+ `humanizer`, akcept `brand-voice-manager`, schema od `seo-tech-lead`).
> **Treść po ANGIELSKU.** Format pliku kolejki: `blog/queue/_format.md`.
> Głos marki i zakazy: `docs/blog/brand-mindsync.md`.
>
> **Status danych:** bramka KROK 0 przeszła 9× OK / 0 RYZYKO / 0 BRAK
> (`blog/queue/_preflight-partia1.json`). **Ahrefs niedostępny** („Insufficient plan" na
> Keywords Explorer API), więc w tej partii **nie ma wolumenów ani KD**. Frazy główne
> pozycji 02-09 pochodzą z researchu SERP (kto rankuje + jaka luka), nie z narzędzia
> słów kluczowych. Jedyna fraza z twardą liczbą to `how to use mindsync app`
> (GSC: 37 wyświetleń, poz. 3.5, 0 kliknięć). Po miesiącu dripu weryfikacja przez
> `scripts/gsc/blog-partia-frazy.py` i korekta H2/FAQ.
> Frazy poboczne i luki konkurencyjne w rozwinięciu: `blog/queue/_partia1-notatki-fraz.md`.

## Zasady wspólne dla wszystkich 9 briefów (nie powtarzam ich w każdym)

1. **Zakaz em-dash (U+2014)** w tytule, meta, zajawce i treści. Półpauza „–" ze spacjami
   albo przebudowa zdania. Bramka dripu odrzuca wpis z em-dash.
2. **YMYL:** zero diagnozowania, zero obietnic wyleczenia, zero zniechęcania do leków
   i terapii. MindSync uzupełnia terapię, nie zastępuje. Zero tematów kryzysowych.
3. **Funkcje `planned` nie istnieją w treści:** `therapist-sharing` (portal ukryty,
   MSV3.4 CS-11) i `streaks` (brak UI). Nie sugerujemy wysyłania czegokolwiek terapeucie
   z apki, nawet jeśli landing `/pre-order/*` to obiecuje. Nie obiecujemy serii i odznak.
4. **Zero cen w treści** (od cennika jest `/membership`). Zero wymyślonych zrzutów ekranu
   i zero wymyślonych nazw przycisków. Jeśli sekcja wymaga nazwy ekranu, której nie ma
   w `blog/app-features.json`, autor zostawia znacznik `[VERIFY-UI: ...]` dla operatora
   zamiast zgadywać.
5. **Karty:** maksymalnie 3 na wpis (1-2 `[FEATURE:]` inline + ewentualnie jeden blok
   `[FEATURES:]` przed FAQ). Powód w karcie to jedno zdanie prozą, po angielsku.
6. **FAQ:** nagłówek H2 dokładnie `Frequently asked questions`, pytania w H3, w brzmieniu
   naturalnego zapytania (małą literą w środku zdania tak jak ludzie piszą w Google,
   ale zapis zdaniowy z wielkiej litery). 4-5 pytań. Odpowiedź 40-70 słów.
7. **Badania:** każda liczba ma nazwisko, rok i czasopismo. Autor **weryfikuje źródło
   pierwotne** przed użyciem. Jeśli nie da się potwierdzić autorów, roku i liczby, twierdzenie
   wypada z tekstu (nie parafrazujemy blogów konkurencji jako źródeł). Linkujemy do publikacji
   albo do rekordu PubMed/PMC, nie do wtórnych blogów.
8. **Struktura:** lead 40-60 słów (scena z życia, nie definicja), sekcje merytoryczne,
   sekcja praktyczna, karty, FAQ. Bez sekcji „Conclusion" i bez waty. Długość: 1100-1600 słów
   (pillar 07: 1500-1900).
9. **Slug wpisu** = pole `seo_url`; URL publiczny to `https://mindsync.app/journal/<slug>`.
10. **Linkowanie do wpisów z tej samej partii tylko wtedy, gdy tamten wpis jest już
    opublikowany** (patrz kolejność dat niżej). Linki „w przód" dopina `webflow-publisher`
    przy publikacji późniejszego wpisu albo zostają jako `[LINK-LATER: slug]` w komentarzu
    briefu, nigdy jako surowy `[LINK: ...]` w treści (bramka dripu odrzuca).

## Kolejność publikacji i daty

Kolejność jest podporządkowana linkowaniu wewnętrznemu: pillar 07 idzie **na końcu**,
żeby mógł linkować w dół do już opublikowanych wpisów, a wpisy wspierające publikują się
wcześniej. Jeśli koordynator woli kolejność numeryczną 01-09, wystarczy przestawić
`planowana_data` w plikach kolejki, treść na tym nie ucierpi (poza linkami w dół w 07).

| data | # | slug (`seo_url`) | kategoria | `kolor` |
|---|---|---|---|---|
| 2026-08-27 | 01 | `how-to-use-mindsync` | MindSync Tips | `#339499` |
| 2026-08-28 | 05 | `how-to-prepare-for-a-therapy-session` | MindSync Tips | `#1f3d38` |
| 2026-08-29 | 06 | `how-to-remember-what-you-talk-about-in-therapy` | Therapy | `#3c67a5` |
| 2026-08-30 | 04 | `how-to-know-if-therapy-is-working` | Therapy | `#e8af0a` |
| 2026-08-31 | 03 | `which-coping-skills-actually-work` | Therapy | `#339499` |
| 2026-09-01 | 08 | `how-to-identify-emotional-triggers` | Therapy | `#ff9f8a` |
| 2026-09-02 | 09 | `why-mood-tracking-stops-working` | Therapy | `#3c67a5` |
| 2026-09-03 | 07 | `what-to-do-between-therapy-sessions` | Therapy | `#1f3d38` |
| bez daty | 02 | `regulate-nervous-system-between-therapy-sessions` (ISTNIEJE) | Therapy | bez zmian |

2026-09-04 zostaje wolne jako bufor (poślizg akceptu albo hero). Rozbudowa 02 nie ma daty
dripu: to **edycja istniejącego itemu w CMS**, nie nowy wpis w kolejce. Sugerowane okno
wykonania: 2026-08-28..08-30, bo wpisy 05, 06 i 07 linkują do niej jako do materiału
o regulacji.

---

# 01. How to use MindSync (getting started)

**1. Meta**
- `seo_url`: `how-to-use-mindsync`
- kategoria: `MindSync Tips` | `kolor`: `#339499` | `planowana_data`: **2026-08-27**
- `tagi`: `["mindsync-tips", "getting-started"]`
- tytuł roboczy: „How to Use MindSync: Your First Week, Step by Step"
- meta_title (≤60 zn.): „How to Use MindSync: Your First Week | MindSync"
- meta_description: obietnica konkretu (co robisz w dniu 1, co w dniu sesji, co po tygodniu).
- **Uwaga publikatorska:** to pierwszy wpis dripu, służy też jako test
  `scripts/webflow/blog-publish.ps1`. Hero musi leżeć na dysku przed 2026-08-27.

**2. Frazy i intencja**
- główna: `how to use mindsync app` (GSC: 37 wyświetleń, poz. 3.5, **0 kliknięć**)
- poboczne: `how does mindsync work`, `mindsync app`, `mindsync ai journal`,
  `record therapy session app`, `therapy journaling app`, `mindsync app download`,
  `is mindsync free`
- intencja: nawigacyjno-instruktażowa. Człowiek albo już pobrał apkę i nie wie, od czego
  zacząć, albo rozważa pobranie i chce zobaczyć, jak to wygląda w praktyce. Dziś ten klik
  ląduje na homepage i się odbija (0 kliknięć przy poz. 3.5 to sygnał, że snippet nie
  odpowiada na pytanie).

**3. Struktura**
- H1: How to Use MindSync: Your First Week, Step by Step
- Lead: scena – pobrałeś apkę w dniu, w którym miałeś sesję, i nie wiesz, czy zacząć
  od nagrywania, czy od pisania.
- H2: What MindSync is for (and what it is not)
  - jedno zdanie definicyjne (GEO), jedno zdanie o granicy: to nie jest terapeuta ani
    zamiennik terapii
- H2: Day one: the ten minutes that set everything up
  - H3: Pick the two or three things you are actually working on
  - H3: Do your first check-in
- H2: Your first session with the app
  - H3: Before: the prep card
  - H3: During: recording (and asking your therapist first)
  - H3: After: the debrief while it is still fresh
- H2: The week between sessions
  - H3: Voice notes when something comes up
  - H3: Homework that lands on your home screen
- H2: What you get after two weeks (trends, weekly summary, timeline)
- H2: Getting the app
  - dwa zwykłe linki tekstowe (App Store, Google Play). **Nie** wstawiamy bloku badge,
    on jest raz w szablonie wpisu.
- H2: Frequently asked questions
  - H3: What is MindSync used for?
  - H3: Is MindSync free?
  - H3: Can I record my therapy session with MindSync?
  - H3: Does MindSync work without a therapist?
  - H3: Do I have to journal every day for it to be useful?

**4. Karty funkcji** (id z werdyktów: session-recording, session-prep, voice-notes,
check-ins, summaries)
- inline po sekcji „Your first session with the app":
  `[FEATURE: session-recording | Record the session with your therapist's permission and get the transcript, the takeaways and the questions they asked you.]`
- inline po sekcji „The week between sessions":
  `[FEATURE: voice-notes | Say it out loud when it happens: the note is transcribed and waiting for you before the next session.]`
- blok przed FAQ:
  `[FEATURES: What to set up in the first week || session-prep | A prep card so you never open a session with a blank mind. || check-ins | A one minute rating of what you are working on, which quietly becomes your trend line. || summaries | A weekly summary that turns scattered notes into a readable story.]`

**5. Linkowanie wewnętrzne**
- `/features` anchorem „see everything the app does"
- `/faq` anchorem „how your data is stored and who can see it"
- `/membership` anchorem „what the free trial includes" (bez cen w tekście)
- `/audience` anchorem „who MindSync is built for"
- Linki do 05 i 06 dopina `webflow-publisher` po ich publikacji (`[LINK-LATER: 05, 06]`).

**6. GEO (fragmenty cytowalne)**
- Definicja, 40-55 słów, tuż pod H2 „What MindSync is for": „MindSync is a mobile app that
  helps people in therapy keep more from every session. It records sessions with your
  therapist's permission, captures voice notes between them, tracks how you are doing on a
  simple scale, and turns all of it into weekly summaries and trends."
- Odpowiedź krokowa, 50-70 słów, pod „Day one": ponumerowana sekwencja pierwszych trzech
  kroków, tak żeby dała się zacytować w całości.

**7. Hero**
- Wariant „codzienny moment" (`hero-01-codzienny-moment.md`): telefon leżący ekranem w dół
  obok kubka i notesu na parapecie w porannym świetle, dłonie poza kadrem. Zero fałszywego
  zrzutu ekranu apki.
- `hero_image_alt`: „A phone, a notebook and a warm cup on a windowsill in morning light,
  the start of a first week with MindSync".

**8. Źródła i fakty do weryfikacji**
- Wszystkie opisy funkcji biorą się z `blog/app-features.json` (statusy live), nie ze strony
  www, która jest nieaktualna.
- Kwestia nagrywania: sprawdź i napisz wprost, że pytasz terapeutę o zgodę, a przepisy
  o nagrywaniu rozmów różnią się między stanami i krajami. Bez porad prawnych.
- Brak twierdzeń badawczych w tym wpisie oznacza brak potrzeby cytowań. Nie doklejaj badań
  na siłę.

**9. Czego NIE robić**
- Nie opisuj ekranów, których nie ma w katalogu funkcji. Nazwa ekranu bez pokrycia =
  `[VERIFY-UI: ...]`.
- Nie obiecuj wysyłki raportu do terapeuty ani serii i odznak.
- Nie wchodź w temat „is therapy working" ani w metodykę mierzenia postępu (to 04).
- Nie podawaj cen ani długości trialu liczbowo, jeśli nie potwierdzi ich operator.

---

# 05. How to prepare for a therapy session when your mind goes blank

**1. Meta**
- `seo_url`: `how-to-prepare-for-a-therapy-session`
- kategoria: `MindSync Tips` | `kolor`: `#1f3d38` | `planowana_data`: **2026-08-28**
- `tagi`: `["getting-more-from-therapy", "session-prep"]`
- tytuł roboczy: „How to Prepare for a Therapy Session When Your Mind Goes Blank"
- meta_title: „How to Prepare for a Therapy Session | MindSync"

**2. Frazy i intencja**
- główna: `how to prepare for a therapy session`
- poboczne: `what to talk about in therapy`, `what to say in therapy when you have nothing
  to say`, `questions to ask your therapist`, `therapy session checklist`,
  `blanking out in therapy`, `what to bring to therapy`, `how to get more out of therapy`
- intencja: praktyczna, przed sesją, najczęściej tego samego dnia. **Kluczowe:** to NIE jest
  wpis o pierwszej sesji. Odbiorca jest w terapii od kilku miesięcy i traci pierwszy
  kwadrans na rozgrzewkę.
- luka: ChoosingTherapy, Grow Therapy, US News, Two Chairs, Project Healthy Minds obsługują
  wyłącznie pierwszą sesję i kończą radą „zrób listę". Nikt nie mówi, skąd wziąć treść tej
  listy, kiedy nic nie pamiętasz z tygodnia.

**3. Struktura**
- Lead: siadasz, pada „how was your week", i wtorek staje się nieosiągalny.
- H2: Why your best material disappears in the waiting room
  - pamięć zależna od kontekstu, plus zniekształcenie pamięci tygodnia (peak-end)
- H2: The problem with preparing the night before
  - rekonstrukcja tygodnia z pamięci wybiera to, co najświeższe i najintensywniejsze
- H2: Capture during the week, not the night before
  - H3: The two line rule
  - H3: What is worth capturing (a moment, a reaction, a sentence you could not say)
- H2: Build the session agenda in ten minutes
  - H3: One main topic, two backups
  - H3: Turn a vague feeling into an opening sentence
  - H3: Questions worth asking your therapist
- H2: What to do when you still go blank
  - opcje: powiedz to na głos, wróć do ostatniej sesji, zacznij od ciała
- H2: Frequently asked questions
  - H3: What should I talk about in therapy?
  - H3: Is it okay to bring notes to a therapy session?
  - H3: What do I say when I have nothing to talk about?
  - H3: How early should I prepare for a therapy session?
  - H3: Should I tell my therapist I prepared?

**4. Karty funkcji** (id z werdyktów: session-prep, workspace)
- inline w „Capture during the week":
  `[FEATURE: workspace | Anything you flag during the week lands on your agenda for next time, so the list writes itself.]`
- inline w „Build the session agenda":
  `[FEATURE: session-prep | The prep card pulls your week into one screen: topics, questions worth asking, and how your mood actually ran.]`
- bez bloku `[FEATURES:]`, dwie karty wystarczą.

**5. Linkowanie wewnętrzne**
- do 02 (istnieje): anchor „calm your nervous system before you walk in"
  → `/journal/regulate-nervous-system-between-therapy-sessions`
- `/features` anchorem „the prep card"
- `[LINK-LATER: 06]` anchor „what to do after the session, when the same memory problem
  works against you"; `[LINK-LATER: 07]` anchor „what to do between therapy sessions"

**6. GEO**
- Odpowiedź na `what to talk about in therapy`, 45-60 słów, w formie listy trzech źródeł
  tematu: co wracało w tygodniu, co przerwaliście na ostatniej sesji, czego unikasz.
- Cytowalny mikro-protokół „ten minutes before a session" (3 kroki, 40-55 słów).

**7. Hero**
- „Codzienny moment": otwarty notes i telefon na stole w poczekalni, miękkie boczne światło,
  dłoń w kadrze bez twarzy.
- alt: „An open notebook and a phone on a table before a therapy session, soft daylight".

**8. Źródła do weryfikacji** (twierdzenie + kandydat na źródło)
- „Wspomnienie tygodnia jest zniekształcone przez najintensywniejszy i ostatni moment"
  → peak-end rule, Redelmeier i Kahneman, 1996, *Pain* (albo Kahneman i wsp. 1993,
  *Psychological Science*). Zweryfikuj, który cytujesz.
- „Zapis w momencie zdarzenia jest dokładniejszy niż odtwarzanie po tygodniu"
  → ecological momentary assessment, Shiffman, Stone i Hufford, 2008,
  *Annual Review of Clinical Psychology*.
- „Zaangażowanie między sesjami wiąże się z lepszym efektem terapii" → metaanaliza prac
  domowych w CBT, Kazantzis i wsp. (sprawdź rok i czasopismo: 2010 *Clinical Psychology:
  Science and Practice* albo 2016 *Cognitive Therapy and Research*). Podaj wielkość efektu
  tylko jeśli potwierdzisz ją w abstrakcie.

**9. Czego NIE robić**
- Nie pisz przewodnika po pierwszej sesji (inna intencja, inny wpis w przyszłości).
- Nie wchodź w recall po sesji ani w nagrywanie (to 06).
- Nie rozbudowuj sekcji o regulacji układu nerwowego, jeden akapit i link do 02.
- Nie sugeruj, że prep card zastępuje rozmowę z terapeutą.

---

# 06. How to remember what you talk about in therapy

**1. Meta**
- `seo_url`: `how-to-remember-what-you-talk-about-in-therapy`
- kategoria: `Therapy` | `kolor`: `#3c67a5` | `planowana_data`: **2026-08-29**
- `tagi`: `["getting-more-from-therapy", "session-recall"]`
- tytuł roboczy: „How to Remember What You Talk About in Therapy"
- meta_title: „How to Remember What You Talk About in Therapy | MindSync"

**2. Frazy i intencja**
- główna: `how to remember what you talk about in therapy`
- poboczne: `why do I forget what my therapist says`, `forgetting therapy sessions`,
  `should I take notes in therapy`, `can I record my therapy session`,
  `therapy session notes for clients`, `what to write down after therapy`,
  `journal after therapy session`
- intencja: ulga plus rozwiązanie. Człowiek podejrzewa, że coś z nim nie tak. Pierwsze
  zdanie po lidzie ma normalizować, dalej idzie mechanizm i protokół.
- luka: Psychology Today (2021) i wątki na Quora opisują zjawisko; poradniki mają dwie
  konkurencyjne apki (Undertone, Therapy Mallard), ale nikt nie domyka tematu nagrywania:
  zgody, granic i tego, co zrobić z nagraniem.

**3. Struktura**
- Lead: wychodzisz z sesji z poczuciem, że coś się przesunęło, a wieczorem nie umiesz
  powiedzieć, co konkretnie padło.
- H2: You are not the problem, the format is
  - ile treści zapamiętuje przeciętny człowiek z konsultacji (patrz źródła)
- H2: Why emotional sessions are the hardest to recall
  - pobudzenie emocjonalne zawęża uwagę: środek sceny pamiętasz, szczegóły znikają
- H2: Four things worth keeping from every session
  - H3: The sentence that landed
  - H3: The question your therapist asked twice
  - H3: What you agreed to try
  - H3: What you avoided saying
- H2: The twenty minute debrief
  - H3: Do it before you get back to your day
  - H3: Speak it instead of writing it, if writing kills it
- H2: Recording your sessions: how to ask, and what to do with it
  - H3: Ask first, always
  - H3: What recording changes (and what it does not)
- H2: Frequently asked questions
  - H3: Why do I forget everything my therapist says?
  - H3: Is it normal to not remember a therapy session?
  - H3: Can I record my therapy session?
  - H3: Should I take notes during therapy or after?
  - H3: What should I write down after a therapy session?

**4. Karty funkcji** (id z werdyktów: session-recording, session-debrief, timeline)
- inline w „The twenty minute debrief":
  `[FEATURE: session-debrief | Capture what mattered while it is still fresh, in text or out loud, and it stays on your timeline.]`
- inline w „Recording your sessions":
  `[FEATURE: session-recording | With your therapist's permission, MindSync records the session and gives you the transcript, the key takeaways and the questions they asked.]`
- blok przed FAQ:
  `[FEATURES: Keeping more from every session || session-recording | The full record, not your best guess at it. || session-debrief | Five minutes after the session, while it is still warm. || timeline | Every session, note and realization in one place you can search later.]`
  (blok jest opcjonalny: jeśli dwie karty inline wystarczą, zostaw dwie i pomiń blok)

**5. Linkowanie wewnętrzne**
- do 05 (opublikowany 08-28): anchor „prepare the session so there is less to lose"
  → `/journal/how-to-prepare-for-a-therapy-session`
- do 02 (istnieje): anchor „if you leave sessions wired and cannot settle"
- `/features` anchorem „session recording and summaries"
- `[LINK-LATER: 07]`

**6. GEO**
- Cytowalna odpowiedź na „why do I forget", 45-60 słów, z liczbą z badania nad
  zapamiętywaniem treści konsultacji, plus zdanie normalizujące.
- Cytowalny protokół debriefu: cztery pytania w liście numerowanej, 50-70 słów.

**7. Hero**
- „Codzienny moment": telefon w dłoni z dyktafonem w tle rozmytych schodów po wyjściu
  z gabinetu, ciepłe światło późnego popołudnia. Bez twarzy, bez ekranu apki.
- alt: „A person holding a phone on the steps outside after a therapy session".

**8. Źródła do weryfikacji**
- „Ludzie zapominają dużą część treści konsultacji niemal natychmiast, a część tego,
  co pamiętają, jest przekręcona" → Kessels, 2003, *Journal of the Royal Society of
  Medicine*, „Patients' memory for medical information". Zweryfikuj przedział procentowy
  i napisz uczciwie, że to badania nad konsultacjami medycznymi, jeśli nie znajdziesz
  odpowiednika stricte psychoterapeutycznego.
- „Pobudzenie emocjonalne wzmacnia pamięć centralnego elementu sceny kosztem szczegółów"
  → Mather i Sutherland, 2011, *Perspectives on Psychological Science* (arousal-biased
  competition) albo klasyczna hipoteza Easterbrooka. Wybierz jedno i sprawdź.
- „Klienci pamiętają z sesji głównie momenty, które sami uznali za ważne" → Martin
  i Stelmaczonek, 1988, *Journal of Counseling Psychology*. Jeśli nie potwierdzisz
  dostępu do abstraktu, twierdzenie wypada.
- Wątek prawny: nagrywanie rozmów podlega przepisom stanowym i krajowym, zgoda terapeuty
  jest warunkiem. Formułuj jako zasadę praktyczną, nie jako poradę prawną.

**9. Czego NIE robić**
- Nie rób z tego wpisu poradnika „co robić po ciężkiej sesji" (therapy hangover to osobny
  temat z backlogu partii 2, żeby nie kanibalizować).
- Nie sugeruj nagrywania bez zgody, nawet w formie „jeśli nie chce, to...".
- Nie obiecuj udostępniania nagrania ani transkryptu terapeucie z poziomu apki.
- Nie wchodź w prep (to 05).

---

# 04. How to know if therapy is working (duet → /pre-order/tracking-therapy-effectiveness)

**1. Meta**
- `seo_url`: `how-to-know-if-therapy-is-working`
- kategoria: `Therapy` | `kolor`: `#e8af0a` | `planowana_data`: **2026-08-30**
- `tagi`: `["getting-more-from-therapy", "measurement"]`
- tytuł roboczy: „How to Know If Therapy Is Working (Beyond a Gut Feeling)"
- meta_title: „How to Know If Therapy Is Working | MindSync"

**2. Frazy i intencja**
- główna: `how to know if therapy is working`
- poboczne: `signs therapy is working`, `is my therapy working`,
  `how long does therapy take to work`, `therapy not working what to do`,
  `how to measure progress in therapy`, `outcome measures in therapy`,
  `should I switch therapists`
- intencja: ocena i decyzja. Człowiek płaci, chodzi od kilku miesięcy i nie wie, czy to ma
  sens. Ryzyko emocjonalne wysokie, ton szczególnie ostrożny.
- luka: Headspace, Alma, Psych Central, Project Healthy Minds, Beck Institute publikują
  listy odczuć („bounce back faster", „better relationships"). Nikt nie tłumaczy laikowi,
  że w badaniach istnieje pomiar (routine outcome monitoring, feedback-informed treatment)
  i jak zrobić jego domową wersję. To jest nasz konkret i nasz klaster różnicujący.

**3. Struktura**
- Lead: szósty miesiąc, rachunek co tydzień, i pytanie, którego nie umiesz zadać na głos.
- H2: Why „do I feel better" is a bad measuring stick
  - pamięć nastroju, dobre i złe tygodnie, brak punktu odniesienia
- H2: What therapists actually measure
  - H3: Symptom questionnaires (PHQ-9, GAD-7 i co znaczy zmiana o kilka punktów)
  - H3: Session by session feedback (ORS/SRS, feedback-informed treatment)
  - H3: The working alliance, and why it predicts outcome
- H2: A home version you can run in fifteen minutes a month
  - H3: Pick three markers that matter to you
  - H3: Same question, same scale, same day of the month
  - H3: Compare months, not days
- H2: Progress is not a straight line
  - uczciwe zastrzeżenie: gorsze tygodnie zdarzają się także wtedy, gdy terapia działa;
    część osób nie poprawia się i to jest znane w badaniach
- H2: When the data says something is off
  - jak rozmawiać o tym z terapeutą, zanim podejmiesz decyzję o zmianie; zero namawiania
    do odejścia
- H2: Frequently asked questions
  - H3: How long does therapy take to work?
  - H3: What are the signs that therapy is working?
  - H3: Is it normal to feel worse before you feel better?
  - H3: How do I tell my therapist that therapy is not working?
  - H3: How often should I check my progress?

**4. Karty funkcji** (id z werdyktów: mood-trends, summaries, health-check, goals)
- inline w „A home version you can run":
  `[FEATURE: mood-trends | Your ratings become a line you can actually read, week over week, instead of a feeling you argue with.]`
- inline w „When the data says something is off":
  `[FEATURE: health-check | A short check on how therapy itself is going, so the conversation with your therapist starts from something concrete.]`
- blok przed FAQ:
  `[FEATURES: Making progress visible || goals | What you are working on, with evidence collecting underneath it. || summaries | A monthly read on where the month actually went. || mood-trends | The long view, so one bad week stops looking like failure.]`

**5. Linkowanie wewnętrzne**
- **duet, anchor frazowy:** „tracking talk therapy effectiveness over time"
  → `https://mindsync.app/pre-order/tracking-therapy-effectiveness` (jeden raz, w sekcji
  „A home version", naturalnie w zdaniu)
- do 06 (opublikowany 08-29): anchor „if you cannot remember what changed between sessions"
- `/features`, `/faq` przy wątku danych
- `[LINK-LATER: 09]` anchor „why mood tracking stops working after two weeks"

**6. GEO**
- Cytowalna odpowiedź na `how to know if therapy is working`, 50-70 słów: trzy warstwy
  (objawy mierzone tym samym narzędziem, funkcjonowanie w życiu, relacja z terapeutą) plus
  ramy czasowe.
- Cytowalna definicja measurement-based care w jednym zdaniu, po ludzku.

**7. Hero**
- „Abstrakcja" (`hero-02-abstrakcja.md`): miękka linia trendu ułożona z gradientu w palecie
  mint i sand, bez siatki wykresu i bez cyfr, spokojna kompozycja.
- alt: „A soft rising line in mint and sand tones, progress seen over months not days".

**8. Źródła do weryfikacji**
- „Informacja zwrotna o postępie pacjenta poprawia wyniki, zwłaszcza u osób, którym idzie
  gorzej" → Lambert i Shimokawa, 2011, *Psychotherapy* (albo nowszy przegląd
  feedback-informed treatment). Sprawdź wielkość efektu przed podaniem.
- „Część osób w terapii nie poprawia się, a część pogarsza" → Hansen, Lambert i Forman,
  2002, *Clinical Psychology: Science and Practice*. Podaj przedział procentowy tylko po
  weryfikacji, i podaj go delikatnie, z ramką „dlatego mierzymy, nie po to, żeby się bać".
- „Sojusz terapeutyczny wiąże się z wynikiem terapii" → metaanaliza Flückiger, Del Re,
  Wampold i Horvath, 2018, *Psychotherapy*. Zweryfikuj współczynnik.
- „PHQ-9 i GAD-7 to standardowe narzędzia przesiewowe" → Kroenke, Spitzer i Williams, 2001,
  *Journal of General Internal Medicine* (PHQ-9); Spitzer i wsp., 2006, *Archives of
  Internal Medicine* (GAD-7). **Zastrzeżenie obowiązkowe:** to narzędzia przesiewowe,
  nie diagnoza, a wyniku nie interpretuje się samodzielnie.

**9. Czego NIE robić**
- Nie namawiaj do zmiany terapeuty ani do przerwania terapii. Kierunek zawsze:
  „porozmawiaj o tym z terapeutą".
- Nie podawaj progów punktowych PHQ-9/GAD-7 jako instrukcji samooceny.
- Nie wchodź w metodykę codziennego logowania nastroju (to 09) ani w triggery (to 08).
- Nie powtarzaj obietnicy landingu o PDF dla terapeuty.

---

# 03. Which coping skills actually work for you (duet → /pre-order/track-interventions)

**1. Meta**
- `seo_url`: `which-coping-skills-actually-work`
- kategoria: `Therapy` | `kolor`: `#339499` | `planowana_data`: **2026-08-31**
- `tagi`: `["between-sessions", "measurement"]`
- tytuł roboczy: „Which Coping Skills Actually Work for You (and How to Find Out)"
- meta_title: „Which Coping Skills Actually Work for You | MindSync"

**2. Frazy i intencja**
- główna: `how to know which coping skills work for you`
- poboczne: `coping skills that actually work`, `do coping skills work`,
  `how to track coping skills`, `what helps my anxiety`,
  `behavioral experiment anxiety`, `does meditation work for me`,
  `tracking habits and mood`
- intencja: zmęczenie listami. Człowiek zna dwadzieścia technik, żadnej nie ufa, chce
  wiedzieć, które działają u niego.
- luka: cały SERP to listy „13 coping skills" (Talkspace, GoodRx, Spring Health,
  ChoosingTherapy, Stacker). Katalog technik, zero pomiaru. **Nie piszemy kolejnej listy.**
  Piszemy metodę sprawdzania.

**3. Struktura**
- Lead: masz w telefonie sześć aplikacji do oddechu i nadal nie wiesz, czy oddech ci pomaga.
- H2: Why the lists do not help anymore
  - to, co działa średnio w populacji, nie musi działać u ciebie
- H2: The one variable rule
  - H3: Pick one thing, not four
  - H3: Two weeks is the minimum
- H2: Choose the measure before you start
  - H3: Rate the thing you are trying to change, not your mood in general
  - H3: Same scale, same time of day
  - H3: Write the prediction down first
- H2: Read the result honestly
  - H3: What a real signal looks like
  - H3: What noise looks like (a good week is not proof)
  - H3: When to stop, when to extend
- H2: A worked example, start to finish
  - jeden przykład przeprowadzony od hipotezy do wniosku, konkretne liczby przykładowe
    (jasno oznaczone jako przykład, nie jako dane badawcze)
- H2: Frequently asked questions
  - H3: How long should I try a coping skill before giving up on it?
  - H3: What if nothing seems to help?
  - H3: Can I test two things at once?
  - H3: How do I know if it is the skill or just a good week?
  - H3: Should I tell my therapist what I am testing?

**4. Karty funkcji** (id z werdyktów: check-ins, mood-trends, summaries, homework)
- inline w „Choose the measure before you start":
  `[FEATURE: check-ins | Rate the one thing you are testing in under a minute, at the same time every day.]`
- inline w „Read the result honestly":
  `[FEATURE: mood-trends | Two weeks of ratings next to each other, so a good day stops passing for progress.]`
- blok przed FAQ (opcjonalny, tylko jeśli tekst tego nie przeładuje):
  `[FEATURES: Running the experiment || check-ins | The daily rating that takes under a minute. || homework | What your therapist suggested, waiting on your home screen instead of in your memory. || summaries | The week read back to you, so the comparison is not from memory.]`

**5. Linkowanie wewnętrzne**
- **duet, anchor frazowy:** „see if the small things actually help you"
  → `https://mindsync.app/pre-order/track-interventions` (jeden raz, w sekcji „Read the
  result honestly" albo w worked example)
- do 02 (istnieje): anchor „the regulation exercises worth testing first"
- do 04 (opublikowany 08-30): anchor „how to know if therapy is working", w kontekście
  „to samo podejście, ale dla całej terapii"
- `/features`

**6. GEO**
- Cytowalny protokół eksperymentu jednoosobowego, 60-80 słów, w pięciu krokach: jedna
  zmienna, jedna miara, dwa tygodnie, zapisana prognoza, porównanie tygodni.
- Cytowalna odpowiedź na „how long should I try a coping skill", 40-55 słów.

**7. Hero**
- „Codzienny moment": dwa kubki i dwie karteczki na blacie w porannym świetle, sugestia
  porównania dwóch tygodni, bez tekstu w kadrze.
- alt: „Two small notes on a kitchen counter in morning light, comparing two weeks".

**8. Źródła do weryfikacji**
- „Samo monitorowanie zachowania zmienia to zachowanie (reaktywność samoobserwacji)"
  → Korotitsch i Nelson-Gray, 1999, *Psychological Assessment*. To ważne zastrzeżenie
  metodologiczne: pomiar sam w sobie jest interwencją.
- „Eksperymenty behawioralne są standardowym elementem CBT" → podręcznikowo, Bennett-Levy
  i wsp., 2004, *Oxford Guide to Behavioural Experiments in Cognitive Therapy*.
  Zweryfikuj tytuł i rok.
- „Zapis w momencie zdarzenia jest dokładniejszy niż retrospekcja" → Shiffman, Stone
  i Hufford, 2008, *Annual Review of Clinical Psychology*.
- Jeżeli podajesz jakąkolwiek liczbę o skuteczności konkretnej techniki (oddech,
  medytacja, ruch), musi mieć własne źródło. Bez źródła: opisujesz mechanizm testowania,
  nie skuteczność.

**9. Czego NIE robić**
- Nie pisz listy „X coping skills" ani rankingu technik.
- Nie sugeruj odstawiania czegokolwiek, co zalecił terapeuta albo lekarz, na podstawie
  dwóch tygodni własnych pomiarów. To zdanie musi paść wprost.
- Nie wchodź w mierzenie skuteczności terapii jako całości (to 04).
- Nie powtarzaj obietnic landingu (automatyczne etykietowanie spacerów i suplementów,
  PDF dla bliskich). Linkujemy anchorem, nie obietnicą.

---

# 08. How to identify your emotional triggers

**1. Meta**
- `seo_url`: `how-to-identify-emotional-triggers`
- kategoria: `Therapy` | `kolor`: `#ff9f8a` | `planowana_data`: **2026-09-01**
- `tagi`: `["understanding-patterns"]`
- tytuł roboczy: „How to Identify Your Emotional Triggers (Without Turning It Into Homework)"
- meta_title: „How to Identify Your Emotional Triggers | MindSync"

**2. Frazy i intencja**
- główna: `how to identify your emotional triggers`
- poboczne: `what are emotional triggers`, `how to find your triggers`,
  `emotional trigger examples`, `why do I overreact to small things`,
  `body signs of a trigger`, `trigger tracking`,
  `how to respond to a trigger instead of reacting`
- intencja: samopoznanie po incydencie. Ktoś zareagował mocniej, niż chciał, i szuka
  wzoru, nie definicji.
- luka: SERP bez giganta (Ellie Mental Health, TalktoAngel, blogi małych praktyk). Wszyscy
  piszą „zauważaj wzorce", nikt nie daje schematu zapisu w momencie wzbudzenia ani tego,
  co zrobić z zapisami po miesiącu.

**3. Struktura**
- Lead: komentarz o zmywarce, a reakcja jak na zwolnienie z pracy.
- H2: A trigger is not the thing that annoyed you
  - definicja robocza: bodziec, który uruchamia reakcję nieproporcjonalną do sytuacji,
    zwykle przez skojarzenie
- H2: Your body notices first
  - fizjologia wyprzedza świadomą interpretację; co obserwować
- H2: The five second capture
  - H3: Situation
  - H3: Body
  - H3: Thought
  - H3: What you did
  - H3: What it cost
- H2: Why writing it later does not work
  - retrospekcja wygładza i racjonalizuje
- H2: What to do with a month of these
  - H3: Group by situation, not by emotion
  - H3: Look for the sentence underneath (the belief that keeps repeating)
  - H3: Bring the pattern to your therapist, not the incident
- H2: Frequently asked questions
  - H3: What are emotional triggers?
  - H3: Why do I overreact to small things?
  - H3: How do I know if it is a trigger or just a bad mood?
  - H3: Can you get rid of a trigger?
  - H3: How long does it take to spot a pattern?

**4. Karty funkcji** (id z werdyktów: reflect, check-ins, mood-trends, workspace,
personal-bio)
- inline w „The five second capture":
  `[FEATURE: reflect | When something sets you off, Reflect asks the follow-up questions a blank note never will, in text or out loud.]`
- inline w „What to do with a month of these":
  `[FEATURE: mood-trends | A month of entries next to your ratings, so the pattern shows up as a shape instead of a suspicion.]`
- blok przed FAQ (opcjonalny):
  `[FEATURES: From incident to pattern || check-ins | The daily rating that gives the incidents a background. || workspace | The realizations worth keeping, in one place. || reflect | The guided version, for the days when you cannot name it yourself.]`

**5. Linkowanie wewnętrzne**
- **anchor frazowy do landingu:** „understand the behavioural patterns underneath"
  → `https://mindsync.app/pre-order/understand-behavioural-patterns`
- do 02 (istnieje): anchor „settle the body first, then look at the pattern"
- do 05 (opublikowany 08-28): anchor „bring the pattern to your next session"
- `/features`

**6. GEO**
- Cytowalna definicja triggera, 35-50 słów, neutralna klinicznie, bez języka traumy.
- Cytowalny schemat zapisu pięciopolowego, 50-70 słów, tak żeby dał się przepisać
  jako gotowa lista.

**7. Hero**
- „Abstrakcja": powtarzający się motyw w palecie coral i mint, jedno pole wyraźnie inne
  niż reszta, spokojna kompozycja bez dramaturgii.
- alt: „A repeating soft pattern in mint and coral with one element standing out".

**8. Źródła do weryfikacji**
- „Retrospektywne relacje są zniekształcone, zapis w momencie zdarzenia jest dokładniejszy"
  → Shiffman, Stone i Hufford, 2008, *Annual Review of Clinical Psychology*.
- „Nazwanie emocji obniża reaktywność ciała migdałowatego" → Lieberman i wsp., 2007,
  *Psychological Science* („Putting feelings into words"). Zweryfikuj i **nie** obiecuj
  efektu terapeutycznego, opisuj mechanizm.
- „Analiza funkcjonalna sytuacja-myśl-emocja-zachowanie jest standardem CBT"
  → podręcznikowo, Beck, *Cognitive Behavior Therapy: Basics and Beyond*. Sprawdź wydanie.
- „Ludzie różnią się precyzją nazywania emocji, a większa precyzja wiąże się z lepszą
  regulacją" → emotional granularity, Barrett i wsp., 2001, *Cognition and Emotion*
  (albo Kashdan, Barrett i McKnight, 2015, *Current Directions in Psychological Science*).

**9. Czego NIE robić**
- Zero języka traumy i zero sugestii diagnozy (PTSD, CPTSD). To wpis o codziennych
  reakcjach, nie o traumie. Jeśli wątek się pcha, jedno zdanie: to temat na rozmowę
  z terapeutą.
- Nie zamieniaj tego w wpis o samym trackingu nastroju (to 09).
- Nie obiecuj, że apka wykryje triggery za czytelnika. Wzorzec widzi człowiek, dane mu
  w tym pomagają.

---

# 09. Why mood tracking stops working after two weeks

**1. Meta**
- `seo_url`: `why-mood-tracking-stops-working`
- kategoria: `Therapy` | `kolor`: `#3c67a5` | `planowana_data`: **2026-09-02**
- `tagi`: `["understanding-patterns", "measurement"]`
- tytuł roboczy: „Why Mood Tracking Stops Working After Two Weeks"
- meta_title: „Why Mood Tracking Stops Working After Two Weeks | MindSync"

**2. Frazy i intencja**
- główna: `why mood tracking doesn't work`
- poboczne: `does mood tracking actually work`, `I stopped using my mood tracker`,
  `how to track mood properly`, `mood tracking fatigue`,
  `what to do with mood tracking data`, `mood tracker for therapy`,
  `mood tracking benefits`
- intencja: sceptyczna. Ktoś próbował, porzucił, i chce wiedzieć, czy to jego wina, czy
  metody. Ton: przyznajemy rację, potem naprawiamy metodę.
- luka: SERP dzieli się na komercyjne listy aplikacji i ogólniki o korzyściach. Dane leżą
  w badaniach, do których nikt nie linkuje. Wpis ma być tym, który je pokazuje.

**3. Struktura**
- Lead: siedemnaście dni z rzędu, potem dwa puste, potem odinstalowane.
- H2: Three reasons tracking dies
  - H3: You tracked a number nobody was going to read
  - H3: You tracked too much
  - H3: You tracked the wrong thing (mood in general instead of what you are working on)
- H2: What the research actually says
  - dowody, że samo monitorowanie ma wartość, i dowody, gdzie aplikacje zawodzą
    (brak wsparcia w interpretacji własnych danych)
- H2: When tracking makes things worse
  - uczciwe zastrzeżenie: drobiazgowe monitorowanie objawów u części osób nasila
    skupienie na objawie; kiedy odpuścić i o czym powiedzieć terapeucie
- H2: A version that survives
  - H3: Under a minute, same moment every day
  - H3: Three markers maximum
  - H3: One reading session a week
  - H3: A reason to look back (the next session)
- H2: What a month of data can tell you (and what it cannot)
- H2: Frequently asked questions
  - H3: Does mood tracking actually work?
  - H3: How often should I track my mood?
  - H3: What should I track instead of mood?
  - H3: Why do I keep forgetting to log my mood?
  - H3: What do I do with all this mood data?

**4. Karty funkcji** (id z werdyktów: check-ins, mood-trends, summaries, smart-reminders)
- inline w „A version that survives":
  `[FEATURE: check-ins | Rate the two or three areas you are actually working on, in under a minute, and the trend line builds itself.]`
- inline w „What a month of data can tell you":
  `[FEATURE: summaries | A weekly summary reads the entries back to you, which is the step most tracking apps skip.]`
- blok przed FAQ:
  `[FEATURES: Tracking that survives month two || check-ins | Under a minute, only the areas that matter to you. || mood-trends | The picture, not the pile of entries. || smart-reminders | A nudge at the moment that fits your week, and a switch to turn it off.]`

**5. Linkowanie wewnętrzne**
- do 04 (opublikowany 08-30): anchor „how to know if therapy is working"
- do 08 (opublikowany 09-01): anchor „how to spot the triggers underneath the numbers"
- do 03 (opublikowany 08-31): anchor „testing one thing at a time"
- `/faq` anchorem „where your entries are stored"

**6. GEO**
- Cytowalna odpowiedź na `does mood tracking actually work`, 50-70 słów: działa, gdy
  spełnia trzy warunki (krótkie, wybrane wskaźniki, ktoś to potem czyta), i dlaczego
  najczęściej upada.
- Cytowalne zastrzeżenie o nasilaniu objawów, 35-50 słów, ostrożne i konkretne.

**7. Hero**
- „Abstrakcja": kalendarzowa siatka miękkich kropek w palecie mint, gęsta na początku
  i rzedniejąca, bez cyfr i bez tekstu.
- alt: „A soft grid of dots fading out over time, mood tracking that quietly stopped".

**8. Źródła do weryfikacji**
- „Użytkownicy aplikacji do śledzenia nastroju zgłaszają brak wsparcia w interpretacji
  własnych danych" → badanie wywiadowcze w *JMIR Mental Health*, 2021 (rekord PMC8387890).
  **Zweryfikuj autorów, rok i dokładny wniosek w rekordzie PMC** przed cytowaniem.
- „Zaangażowanie w codzienne logowanie spada w ciągu kilku tygodni" → potrzebne źródło
  pierwotne z liczbą. Jeśli nie potwierdzisz konkretnego badania z procentem, napisz
  o zjawisku bez liczby albo pomiń.
- „Samo monitorowanie zmienia mierzone zachowanie" → Korotitsch i Nelson-Gray, 1999,
  *Psychological Assessment*.
- „Nazywanie emocji zmienia sposób ich przetwarzania" → Lieberman i wsp., 2007,
  *Psychological Science*.
- „Zbyt drobiazgowe monitorowanie objawów może u części osób nasilać skupienie na objawie"
  → poszukaj przeglądu o symptom monitoring i attentional focus. Bez potwierdzonego
  źródła formułuj to jako obserwację kliniczną zgłaszaną przez terapeutów, a nie jako
  wynik badania.

**9. Czego NIE robić**
- Nie obiecuj poprawy nastroju z samego śledzenia.
- Nie wchodź w ocenę skuteczności terapii (to 04) ani w metodę wykrywania triggerów (to 08).
- Nie promuj serii i odznak jako sposobu na wytrwałość (`streaks` = planned).
- Nie porównuj się nazwą z konkretnymi aplikacjami konkurencji.

---

# 07. PILLAR: What to do between therapy sessions

**1. Meta**
- `seo_url`: `what-to-do-between-therapy-sessions`
- kategoria: `Therapy` | `kolor`: `#1f3d38` | `planowana_data`: **2026-09-03**
- `tagi`: `["between-sessions", "pillar"]`
- tytuł roboczy: „What to Do Between Therapy Sessions: A Weekly System That Fits Real Life"
- meta_title: „What to Do Between Therapy Sessions | MindSync"
- **Rola:** hub klastra 2. Publikuje się jako ostatni w partii, żeby linkować w dół
  do wpisów już opublikowanych. Długość 1500-1900 słów.

**2. Frazy i intencja**
- główna: `what to do between therapy sessions`
- poboczne: `how to make therapy more effective`, `journaling between therapy sessions`,
  `how to keep therapy momentum`, `weekly therapy routine`,
  `therapy homework ideas for clients`, `apps to use between therapy sessions`
- intencja: zaangażowany klient terapii, który chce, żeby te 167 godzin poza gabinetem
  na coś się przełożyły.
- luka: Talkspace, SonderMind i dziesiątki blogów praktyk powtarzają tę samą listę
  („journal, self-care, sleep, support system"), Rosebud obstawia format listy aplikacji.
  **Nikt nie daje jednego rytmu tygodnia.** To jest cała przewaga tego wpisu.

**3. Struktura**
- Lead: godzina w gabinecie, sto sześćdziesiąt siedem godzin poza nim (arytmetyka tygodnia,
  nie badanie).
- H2: Why the week matters more than the hour
  - co mówią badania o zaangażowaniu między sesjami
- H2: The rhythm, not the checklist
  - H3: Session day: twenty minutes after
  - H3: The next 48 hours: let it settle, capture what surfaces
  - H3: Midweek: one honest check-in
  - H3: The day before: build the agenda
- H2: What to capture (and what to skip)
  - H3: Moments, not essays
  - H3: The thing you almost said
  - H3: What the homework actually cost you
- H2: When the week goes sideways
  - opuszczone dni, gorszy tydzień, brak energii; zasada „wróć do jednego wskaźnika"
- H2: If you only do one thing
  - jedna rekomendacja, wybrana i uzasadniona
- H2: Frequently asked questions
  - H3: What should I do between therapy sessions?
  - H3: How do I keep making progress between sessions?
  - H3: Should I journal every day between therapy sessions?
  - H3: What if I forget everything by the next session?
  - H3: Is it okay to contact my therapist between sessions?

**4. Karty funkcji** (id z werdyktów: session-prep, voice-notes, check-ins, summaries,
workspace)
- inline w „The next 48 hours":
  `[FEATURE: voice-notes | Say it out loud when it comes up, and it is transcribed and waiting for you later.]`
- inline w „The day before":
  `[FEATURE: workspace | Everything you flagged during the week is already sitting on your agenda for next time.]`
- blok przed FAQ:
  `[FEATURES: The week, in one place || check-ins | One honest minute midweek. || summaries | The week read back to you before you walk in. || session-prep | The prep card that turns seven days into one screen.]`

**5. Linkowanie wewnętrzne (pillar linkuje w dół, to jego główna funkcja SEO)**
- do 02: anchor „regulate your nervous system between therapy sessions"
  → `/journal/regulate-nervous-system-between-therapy-sessions`
- do 06: anchor „remember what you talked about"
  → `/journal/how-to-remember-what-you-talk-about-in-therapy`
- do 05: anchor „prepare for the next session"
  → `/journal/how-to-prepare-for-a-therapy-session`
- do 03: anchor „test which coping skills actually work for you"
  → `/journal/which-coping-skills-actually-work`
- do 09: anchor „tracking that survives past week two"
  → `/journal/why-mood-tracking-stops-working`
- do 08 (opcjonalnie): anchor „spot your emotional triggers"
- `/features` raz, w sekcji „If you only do one thing"
- **Zwrotnie:** po publikacji 07 `webflow-publisher` dopina link „w górę" do pillara
  w wpisach 05, 06, 03, 09 i 08 (`[LINK-LATER: 07]` w ich briefach).

**6. GEO**
- Cytowalna odpowiedź na `what to do between therapy sessions`, 60-80 słów, w formie
  czterech punktów rytmu tygodnia z ramami czasowymi. To jest fragment, który ma szansę
  trafić do AI Overviews, więc musi działać wyjęty z kontekstu.
- Cytowalne zdanie o proporcji: jedna godzina terapii wobec reszty tygodnia, bez patosu.

**7. Hero**
- „Codzienny moment": tydzień widziany jako spokojna sekwencja codziennych przedmiotów
  na parapecie (kubek, klucze, notes, telefon) w porannym świetle, kompozycja pozioma.
- alt: „Everyday objects lined up on a windowsill, a week between therapy sessions".

**8. Źródła do weryfikacji**
- „Praca między sesjami wiąże się z lepszymi wynikami terapii" → metaanalizy prac domowych
  w CBT, Kazantzis i wsp. (sprawdź: 2010 *Clinical Psychology: Science and Practice*
  i 2016 *Cognitive Therapy and Research*). Podaj wielkość efektu tylko po weryfikacji.
- „Niewykonywanie zadań między sesjami jest jedną z częstszych przyczyn nieskuteczności
  CBT" → przegląd o between-session homework, 2024, *PMC11303922*. Zweryfikuj autorów
  i sformułowanie, nie przesadzaj z siłą twierdzenia.
- „Zapis w momencie zdarzenia bije retrospekcję" → Shiffman, Stone i Hufford, 2008,
  *Annual Review of Clinical Psychology*.
- Arytmetyka 1 wobec 167 godzin to arytmetyka, nie cytat. Nie przypisuj jej badaniu.

**9. Czego NIE robić**
- **Zero sekcji how-to o regulacji układu nerwowego.** Jeden akapit plus link do 02.
  To jest twarda granica kanibalizacji, wpis 02 stoi na tej frazie od miesięcy.
- Nie rozbudowuj sekcji prep (to 05) ani sekcji recall (to 06). Jeden akapit i link.
- Nie zamieniaj wpisu w listę aplikacji ani w listę „20 things to try".
- Nie sugeruj kontaktu z terapeutą poza sesją jako normy: w FAQ odpowiadasz, że to zależy
  od ustaleń z terapeutą i jego zasad kontaktu.

---

# 02. ROZBUDOWA istniejącego wpisu: regulate your nervous system between therapy sessions

**Tryb pracy: EDYCJA ITEMU W CMS, nie kolejka dripu.** Wpis istnieje pod
`https://mindsync.app/journal/regulate-nervous-system-between-therapy-sessions`
i ma historię w GSC (43 wyświetlenia, poz. 14.7). Nie tworzymy pliku w `blog/queue/`,
nie nadajemy `planowana_data`. Zmiany wprowadza `webflow-publisher` w istniejącym itemie
kolekcji Blog Posts po akceptach; slug, data publikacji i hero **zostają bez zmian**
(zmiana sluga zresetowałaby dorobek pozycyjny). Sugerowane okno wykonania:
2026-08-28..2026-08-30.

**1. Cel rozbudowy**
Wpis jest w striking distance (poz. 14.7). Dokładamy objętość i pokrycie fraz sąsiednich,
żeby wypchnąć go do top 10, plus FAQ pod GEO. Fraza główna po rozbudowie:
`how to regulate your nervous system`.

**2. Frazy do pokrycia nowymi sekcjami**
`nervous system regulation exercises`, `how to calm your nervous system fast`,
`signs of a dysregulated nervous system`, `how long does it take to regulate your nervous
system`, `vagus nerve exercises for anxiety`, `somatic exercises for anxiety at home`,
`window of tolerance`, `nervous system regulation before therapy session`.

**3. Co DODAĆ (nowe sekcje, w tej kolejności w tekście)**
- **Nowe H2 po sekcji wprowadzającej: „What dysregulation actually feels like"**
  - H3: In the body (co ludzie zgłaszają: napięcie, płytki oddech, nieustanne skanowanie)
  - H3: In your head (natłok, pustka, drażliwość)
  - **Zastrzeżenie obowiązkowe:** to nie jest lista diagnostyczna i nie służy do
    stawiania sobie rozpoznania.
- **Nowe H2: „How long does it take?"**
  - uczciwa odpowiedź o różnicy między pojedynczym ćwiczeniem (minuty) a zmianą
    reaktywności bazowej (tygodnie regularnej praktyki), z zastrzeżeniem, że dane są
    ograniczone.
- **Nowe H2: „A quick comparison of what to try"**
  - tabela w RichText-safe HTML nie jest dostępna, więc lista `ul` z jednolitym wzorem:
    nazwa ćwiczenia, ile trwa, gdzie da się zrobić, co pokazuje badanie, dla kogo bywa
    nieprzyjemne. Minimum cztery pozycje, w tym co najmniej jedna z uczciwym „u części
    osób nasila lęk" (dotyczy m.in. skupienia na oddechu).
- **Nowe H2: „Before and after a session"**
  - H3: Twenty minutes before (co realnie da się zrobić w poczekalni)
  - H3: The hour after (dlaczego ciało bywa rozregulowane po dobrej sesji)
  - to jest mostek do 05 i 06
- **Nowa sekcja H2 „Frequently asked questions"** jeśli wpis jej nie ma, albo rozbudowa
  istniejącej do 5 pytań:
  - H3: How do I calm my nervous system quickly?
  - H3: What are the signs of a dysregulated nervous system?
  - H3: How long does it take to regulate your nervous system?
  - H3: Do vagus nerve exercises actually work?
  - H3: Can I do this before a therapy session?

**4. Karty funkcji do wstawienia** (id z werdyktów: session-debrief, voice-notes, reflect,
check-ins, mood-trends; **therapist-sharing wypadł z trafień jako PLANNED, nie używać**)
- w sekcji „A quick comparison of what to try", po liście:
  `[FEATURE: check-ins | Rate how wound up you were before and after, so you find out which exercise does anything for you.]`
- w sekcji „Before and after a session":
  `[FEATURE: session-debrief | Catch what came up right after the session, while your body is still telling you something.]`
- **Nie dokładaj bloku `[FEATURES:]`**, jeśli wpis ma już kartę. Sufit trzech kart dotyczy
  całego wpisu po rozbudowie. Przed edycją policz karty, które już tam są.

**5. Linkowanie wewnętrzne do dodania**
- do 07 (po jego publikacji 09-03): anchor „the rest of the week between sessions"
- do 05: anchor „walking into the session with something to say"
- do 06: anchor „keeping what the session gave you"
- `/features` jeśli w tekście jeszcze go nie ma

**6. GEO**
- Cytowalna odpowiedź na `how long does it take to regulate your nervous system`,
  45-60 słów, z uczciwym rozróżnieniem doraźne kontra bazowe.
- Cytowalna lista objawów dysregulacji, 40-60 słów, z zastrzeżeniem, że to nie diagnoza.

**7. Czego NIE ruszać**
- Slug, tytuł H1, hero, data publikacji, istniejące akapity o teorii poliwagalnej wraz
  z zastrzeżeniem („clinically useful but scientifically debated") i istniejące cytowanie
  Laborde i wsp., 2022, *Psychophysiology*. Rozbudowa jest addytywna.
- Nie usuwaj istniejących kart funkcji.
- Nie przenoś wpisu do innej kategorii.

**8. Źródła do weryfikacji dla nowych sekcji**
- „Powolny oddech około sześciu oddechów na minutę wpływa na zmienność rytmu serca"
  → Lehrer i Gevirtz, 2014, *Frontiers in Psychology* (HRV biofeedback). Zweryfikuj.
- „Ćwiczenia oddechowe u części osób nasilają lęk" → poszukaj źródła o interoceptive
  exposure i o reakcjach paradoksalnych na relaksację (relaxation-induced anxiety, Heide
  i Borkovec, 1983, *Journal of Consulting and Clinical Psychology*). Bez źródła podaj
  jako powszechnie zgłaszaną obserwację i tak to opisz.
- „Teoria poliwagalna jest naukowo dyskutowana" → krytyka Grossmana i Taylora, 2007,
  *Biological Psychology*, oraz nowsze polemiki. Zastrzeżenie w tekście już jest,
  rozbudowa go nie osłabia.
- Terminu „window of tolerance" używaj z atrybucją do Siegela i jako modelu klinicznego,
  nie jako zmierzonej wielkości.

**9. Czego NIE robić**
- Nie obiecuj efektu leczniczego ani „resetu układu nerwowego".
- Nie wchodź w tematy kryzysowe ani w traumę jako diagnozę.
- Nie przejmuj fraz należących do 07 (`what to do between therapy sessions`) w nowych
  H2. Rozbudowa trzyma się rodziny „nervous system / regulate / calm / grounding".

---

## Checklista przed oddaniem partii do publikacji

1. Każdy wpis: `humanizer` → akcept `brand-voice-manager` → `schema_jsonld` od
   `seo-tech-lead` → hero od `graphic-designer` (frazy do alt są w briefach) → `status: gotowy`.
2. `python scripts/blog-queue-gate.py` przed pierwszym uruchomieniem dripu.
3. Kontrola em-dash na plikach kolejki (bramka dripu i tak odrzuci, ale taniej złapać wcześniej).
4. Kontrola kart: żaden wpis nie przekracza trzech, wszystkie id ze statusem `live`.
5. Kontrola linków: zero surowych `[LINK: ...]`, zero linków do wpisów jeszcze
   nieopublikowanych.
6. Po miesiącu: `scripts/gsc/blog-tematy.py` i `blog-partia-frazy.py`, podmiana pytań FAQ
   na realne zapytania, decyzje o rozbudowach zamiast nowych wpisów.
