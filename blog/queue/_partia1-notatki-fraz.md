# Partia 1 – notatki frazowe (ETAP A, robocze; wsad do briefów w ETAPIE B)

> Data: 2026-08-25. Autor: `seo-content-writer`. Status: **przed bramką KROK 0**.
> Bramka: `python scripts/blog-coverage-preflight.py --temat blog/queue/_preflight-partia1.json`
> Frazy główne: pozycja 01 z GSC (realne zapytanie + liczba wyświetleń), pozycje 02-09
> z researchu konkurencji (świeża właściwość, sekcje LUKI/RANKINGI w GSC puste –
> `seo/blog/gsc-analiza-2026-08-25.md` §1). Po miesiącu dripu: weryfikacja fraz przez
> `scripts/gsc/blog-partia-frazy.py` i korekta H2/FAQ.
> Wszystkie frazy i cała treść po ANGIELSKU. Zakaz em-dash także w tym pliku.

## Zasady wspólne partii

- **Nie obiecujemy funkcji `planned`:** `streaks` (brak UI) i `therapist-sharing` (portal
  ukryty w MSV3.4 CS-11). Oba landingi `/pre-order/*` obiecują PDF dla terapeuty –
  **wpisy tego nie powtarzają**, linkują wyłącznie frazowym anchorem.
- **YMYL:** zero obietnic leczenia, zero tematów kryzysowych, każda liczba z badania ma
  nazwisko + rok + czasopismo (wzorzec: dwa żywe wpisy na `/journal`).
- **Karty:** 1-2 `[FEATURE:]` inline + jeden blok `[FEATURES:]` przed FAQ. Sufit 3 karty.
- **FAQ:** nagłówek dokładnie „Frequently asked questions", 4-5 pytań H3 w formie
  dosłownych zapytań (po miesiącu podmieniamy na realne zapytania z GSC).

## Granice kanibalizacji wewnątrz partii (twarde)

| Rodzina fraz | Właściciel | Kto NIE dotyka |
|---|---|---|
| nervous system, regulate, grounding, vagus, somatic | 02 (rozbudowa) | 07 (tylko link, zero sekcji how-to) |
| is therapy working, therapy progress, outcome measures | 04 | 09, 03 |
| mood tracking, mood log, tracking fatigue | 09 | 04, 08 (08 bierze triggery, nie sam log) |
| what to talk about, prep, agenda | 05 | 07 (tylko akapit + link) |
| forgetting, session recall, notes after session | 06 | 05, 07 |

---

## 01. How to use MindSync (getting started)

- **Kategoria:** MindSync Tips. **Klaster:** brand / onboarding.
- **Fraza główna:** `how to use mindsync app` (GSC: 37 wyświetleń, poz. 3.5, 0 kliknięć).
- **Poboczne:** `mindsync app`, `how does mindsync work`, `mindsync ai journal`,
  `therapy journaling app`, `ai journaling app for therapy`, `record therapy session app`,
  `mindsync app download`, `is mindsync free`.
- **Uwaga z GSC:** `mindsync download` (74 wyśw.) + `mindsync app download` (48 wyśw.) nie
  mają celu – wpis daje sekcję „Getting the app" z linkami do App Store i Google Play
  (bogaty blok badge jest w szablonie, w treści zwykłe linki).
- **Struktura robocza:** pierwsze 10 minut, pierwszy tydzień, pierwszy cykl sesji.
- **Linkowanie:** `/features`, `/faq` (prywatność), `/membership` (bez cen w treści),
  wpisy 05 i 06 gdy powstaną.

## 02. ROZBUDOWA: regulate your nervous system between therapy sessions

- **Nie nowy wpis.** Istniejący URL `/journal/regulate-nervous-system-between-therapy-sessions`
  (GSC: 43 wyświetlenia, poz. 14.7). Zadanie: dobudowa sekcji i FAQ pod frazy sąsiednie.
- **Fraza główna po rozbudowie:** `how to regulate your nervous system`.
- **Poboczne do nowych H2/H3:** `nervous system regulation exercises`,
  `how to calm your nervous system fast`, `signs of a dysregulated nervous system`,
  `how long does it take to regulate your nervous system`, `vagus nerve exercises for anxiety`,
  `somatic exercises for anxiety at home`, `window of tolerance`,
  `nervous system regulation before therapy session`.
- **Co dołożyć:** (a) sekcja „What dysregulation actually feels like" (objawy, bez
  diagnozowania); (b) tabela ćwiczeń: czas trwania, gdzie się da zrobić, co mówi badanie;
  (c) sekcja „Before and after a session" (mostek do 05 i 06); (d) FAQ 5 pytań;
  (e) karta `[FEATURE: check-ins]` i `[FEATURE: mood-trends]` (sprawdzenie, czy ćwiczenie
  cokolwiek zmienia), bez powtarzania kart już obecnych.
- **Uczciwe zastrzeżenie zostaje:** teoria poliwagalna jest klinicznie użyteczna, ale
  naukowo dyskutowana.

## 03. DUET → /pre-order/track-interventions

- **Robocza fraza główna:** `how to know which coping skills work for you`.
- **Poboczne:** `coping skills that actually work`, `do coping skills work`,
  `how to track coping skills`, `what helps my anxiety`, `behavioral experiment anxiety`,
  `n of 1 experiment mental health`, `tracking habits and mood`,
  `does meditation work for me`.
- **Luka:** SERP to listy „13 coping skills" (Talkspace, GoodRx, Spring Health,
  ChoosingTherapy). Wszyscy dają katalog technik, **nikt nie uczy pomiaru**, czy dana
  technika działa u tego konkretnego człowieka. Nasz konkret: protokół jednoosobowego
  eksperymentu (jedna zmienna, dwa tygodnie, ten sam pomiar, porównanie tygodni).
- **Anchor do landingu (frazowy):** „see if the small things actually help you" albo
  „track which interventions actually move your mood" → `/pre-order/track-interventions`.
- **Karty:** `check-ins`, `mood-trends`, `summaries` (+ `homework` jeśli o zadaniach
  od terapeuty).

## 04. DUET → /pre-order/tracking-therapy-effectiveness

- **Robocza fraza główna:** `how to know if therapy is working`.
- **Poboczne:** `signs therapy is working`, `how long does therapy take to work`,
  `is my therapy working`, `therapy not working what to do`,
  `how to measure progress in therapy`, `outcome measures in therapy`,
  `PHQ-9 GAD-7 explained`, `should I switch therapists`.
- **Luka:** Headspace, Alma, Psych Central, Project Healthy Minds dają listy odczuć
  („bounce back faster", „better relationships"). Nikt nie tłumaczy laikowi
  **measurement-based care / routine outcome monitoring** (badania Lamberta nad
  feedback-informed treatment, ORS/SRS, PHQ-9, GAD-7) i tego, jak zrobić własny pomiar
  co 4-6 tygodni. To jest nasz konkret i nasz różnicujący klaster 6.
- **Anchor do landingu:** „tracking talk therapy effectiveness over time"
  → `/pre-order/tracking-therapy-effectiveness`.
- **Karty:** `mood-trends`, `summaries`, `goals`; `health-check` przy wątku sojuszu
  terapeutycznego. **Bez** obietnicy wysyłki raportu do terapeuty.
- **Zastrzeżenie YMYL:** postęp w terapii nie jest liniowy, gorsze tygodnie to nie dowód
  porażki; decyzję o zmianie terapeuty omawia się z terapeutą.

## 05. How to prepare for a therapy session (klaster 1)

- **Robocza fraza główna:** `how to prepare for a therapy session`.
- **Poboczne:** `what to talk about in therapy`, `what to say in therapy when you have
  nothing to say`, `how to prepare for your first therapy session`,
  `questions to ask your therapist`, `therapy session checklist`,
  `blanking out in therapy`, `what to bring to therapy`.
- **Luka:** ChoosingTherapy, Grow Therapy, US News, Two Chairs piszą pod **pierwszą**
  sesję i kończą na radzie „zrób listę". Nikt nie obsługuje osoby, która jest w terapii
  od pół roku, ma sesję jutro i pustkę w głowie. Nasz konkret: skąd wziąć tematy, gdy
  nic nie pamiętasz z tygodnia (ślady z tygodnia zamiast wysilania pamięci) plus reguła
  „jeden temat główny, dwa zapasowe".
- **Karty:** `session-prep` (Prep Card), `workspace` (agenda i wątki), `voice-notes`.
- **Linkowanie:** do 07 (pillar), do 06 (co zrobić po sesji), do `/features`.

## 06. How to remember what you talk about in therapy (klaster 1)

- **Robocza fraza główna:** `how to remember what you talk about in therapy`.
- **Poboczne:** `why do I forget what my therapist says`, `forgetting therapy sessions`,
  `should I take notes in therapy`, `can I record my therapy session`,
  `therapy session notes for clients`, `what to write down after therapy`,
  `journal after therapy session`.
- **Luka:** Psychology Today (2021) i blogi praktyk opisują zjawisko; dwie aplikacje
  konkurencyjne (Undertone, Therapy Mallard) mają już poradniki, ale ogólne. Konkret,
  którego brakuje: liczba z badań nad zapamiętywaniem treści leczenia (pacjenci
  odtwarzają około jednej trzeciej materiału; pobudzenie emocjonalne pogarsza recall),
  plus **etyka i prawo nagrywania**: pytasz terapeutę o zgodę, nagrywasz siebie, nie
  publikujesz, prawo do nagrywania rozmów różni się między stanami i krajami.
- **Karty:** `session-recording`, `session-debrief`, `timeline`.
- **Zastrzeżenie:** zgoda terapeuty przed nagrywaniem, zawsze.

## 07. PILLAR: what to do between therapy sessions (klaster 2)

- **Robocza fraza główna:** `what to do between therapy sessions`.
- **Poboczne:** `how to make therapy more effective`, `therapy homework ideas for clients`,
  `journaling between therapy sessions`, `how to keep therapy momentum`,
  `167 hours between sessions`, `weekly therapy routine`, `apps to use between therapy sessions`.
- **Luka:** Talkspace, SonderMind i dziesiątki blogów praktyk dają tę samą listę
  („journal, self-care, sleep, support system"), Rosebud obstawia format listy aplikacji.
  Nikt nie daje **jednego prostego systemu tygodniowego** z konkretnym rytmem: dzień sesji,
  24 godziny po, środek tygodnia, dzień przed następną. To rola pillara: hub klastra 2,
  linkuje w dół do 02, 03, 05, 06, 09.
- **Karty:** `workspace`, `voice-notes`, `homework` (blok `[FEATURES:]` przed FAQ).
- **Granica:** zero sekcji how-to o regulacji układu nerwowego (to 02), zero rozbudowanej
  sekcji prep (to 05). Jeden akapit plus link.

## 08. How to identify your emotional triggers (klaster 3)

- **Robocza fraza główna:** `how to identify your emotional triggers`.
- **Poboczne:** `what are emotional triggers`, `how to find your triggers`,
  `emotional trigger examples`, `trigger tracking worksheet`,
  `why do I overreact to small things`, `body signs of a trigger`,
  `how to respond to a trigger instead of reacting`.
- **Luka:** SERP to blogi małych praktyk i Ellie Mental Health, TalktoAngel; brak
  giganta z autorytetem, więc temat jest realnie do wygrania. Wszyscy powtarzają
  „zauważaj wzorce", nikt nie daje **schematu zapisu w momencie wzbudzenia**
  (sytuacja, myśl, ciało, reakcja, koszt) i tego, co robić z takim zapisem po miesiącu.
- **Anchor pomocniczy:** `/pre-order/understand-behavioural-patterns` (landing bez
  partnera, 84 wyświetlenia @ poz. 13.1 – wpis daje mu punkt zaczepienia).
- **Karty:** `check-ins`, `reflect`, `mood-trends`.

## 09. Why mood tracking stops working after two weeks (klaster 3)

- **Robocza fraza główna:** `why mood tracking doesn't work`.
- **Poboczne:** `does mood tracking actually work`, `mood tracking benefits research`,
  `I stopped using my mood tracker`, `how to track mood properly`,
  `mood tracking fatigue`, `what to do with mood tracking data`,
  `mood tracker for therapy`.
- **Luka:** SERP dzieli się na listy aplikacji (komercyjne) i ogólniki o korzyściach.
  Twarde dane leżą w badaniach, do których nikt nie linkuje: wywiadówka JMIR
  (Schueller i wsp., aplikacje nie pomagają zinterpretować własnych danych), spadek
  zaangażowania około 15% w ciągu 20 dni, ryzyko nasilenia objawów przy zbyt drobiazgowym
  monitorowaniu, oraz affect labeling (Lieberman, UCLA). Nasz konkret: log ma sens tylko
  wtedy, gdy ktoś go potem czyta i wyciąga wniosek.
- **Karty:** `check-ins`, `mood-trends`, `summaries` (+ `smart-reminders` przy wątku
  utrzymania nawyku; **nie** `streaks`, funkcja planned).
- **Granica:** zero fraz o skuteczności terapii (to 04).

---

## Backlog do partii 2 (odpad z rankingu ETAPU A)

- **Therapy homework: why it never gets done** – mocna baza badawcza (compliance,
  Kazantzis i wsp.), idealne pokrycie funkcją `homework` + `smart-reminders`, ale SERP jest
  dziś w całości terapeutyczny (PositivePsychology, Psychology Today for professionals,
  GoodTherapy) i intencja B2C dopiero się kształtuje. Bierzemy w partii 2 z kątem
  klienckim „your therapist gave you homework, here is how to actually do it".
- **What to do after a therapy session / therapy hangover** – wysoki potencjał emocjonalny,
  ale zachodzi na 06 (post-session). Bierzemy dopiero po publikacji 06, jako wpis
  wspierający z linkiem, nie równolegle.
- **What is MindSync (and what it isn't)** – porządkuje konfuzję brandową
  (`mindsync.co` 665 wyśw., `mind sync meaning` 443). Niska wartość konwersyjna,
  koniec kolejki.

## Wsad do Ahrefs (do pobrania w sesji głównej, zlecenie ETAP B)

Keywords Explorer (US, EN) dla walidacji wolumenu i KD fraz głównych 03-09:
`how to know if therapy is working`, `what to do between therapy sessions`,
`how to prepare for a therapy session`, `what to talk about in therapy`,
`how to remember what you talk about in therapy`, `emotional triggers`,
`does mood tracking work`, `coping skills that actually work`.
Organic keywords konkurencji (top 100, filtr pozycja 1-20): `rosebud.app/blog`,
`talkspace.com/blog`, `betterhelp.com/advice`, `helloalma.com/blog`,
`headspace.com/articles`, `choosingtherapy.com`, `verywellmind.com` (filtr „therapy session").
