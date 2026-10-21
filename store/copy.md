# MindSync: copy screenshotów App Store i Google Play (odświeżony UI)

Status: **AKCEPT brand-voice-manager, 2026-10-19** (dotyczy tekstu nagłówków i podtytułów).
Humanizer przeszedł wszystkie nowe i zmienione linie w trybie embedded. Każdy slajd przeszedł test
zimnego czytania. W tym pliku nie ma znaków U+2014 ani U+2013 (sprawdzone mechanicznie).

Copy jest po angielsku (pisownia US), notatki po polsku. Konwencja: `**bold**` = pogrubiona fraza,
` / ` = złamanie linii w nagłówku.

Skąd brałem fakty: `mindsync-frontend-wt-store-shots/mindsync_app/lib/l10n/app_en.arb` (stan
z nowym Main i Character), `blog/app-features.json`, obecne screeny `ios-1..8.png`.

## 1. Copy, kolejność App Store

| slide | headline | subtitle | status | reason |
|---|---|---|---|---|
| 1 (nowy) | Your therapy week / **at a glance** | **Next session**, agenda, to-dos, and habits, right on your home screen | new | Nowa zakładka Main. Lista to dokładnie pierwsze kafle z apki (`mc_tileSession`, `mc_tileAgenda`, `mc_tileTodo`, `mc_tileHabits`). Słowo "therapy" w pierwszym nagłówku od razu mówi, dla kogo jest apka. Bez "New" (Play go odradza) i bez "one screen", bo "in one feed" i "in one space" już są na dwóch innych slajdach. Wariant podtytułu tylko wtedy, gdy screen pokazuje kafel "Your first week": `**Next session**, agenda, to-dos, habits, and eight small steps to start` (`mc_weekPlanIntro`). |
| 2 (było 1) | **Never forget** / a session again | Take a note **After Therapy** by voice or text | kept | Sprawdzony hook o głównym bólu. "After Therapy" wielkimi literami to nazwa przycisku w menu + (`fab_afterTherapy`), więc zostaje. |
| 3 (było 5) | **Be present** / We'll take notes | **Record your session** and get a summary with topics and to-dos | changed | Nagłówek bez zmian. W podtytule: "Record session" bez zaimka brzmi jak etykieta, a nie zdanie. "to-do's" poprawione na "to-dos" (bez apostrofu). "realisations" wypada z dwóch powodów: to pisownia UK, a realizacje z nagrania pojawiają się tylko warunkowo (`realization_detection` po diaryzacji), więc obietnica była szersza niż funkcja. Ekran pokazuje Summary, Topics & Questions i To-do, czyli dokładnie to, co mówi nowa linia. Jedna sesja daje jedno podsumowanie, stąd "a summary" zamiast "detailed summaries". |
| 4 (było 2) | Make every session / **count twice** | **Reflect** using AI that knows your therapy history | kept | Bez uwag. Nazwa Reflect zgodna ze słownikiem marki. |
| 5 (było 3) | **Always know** / what to talk about | **Prepare for every session** in under a minute | kept | Bez uwag. Prep card składa się automatycznie (`mc_sessionPrepBody`), więc "under a minute" jest uczciwe. |
| 6 (bez zmian) | All your **therapy work** / in one space | **Workspace** gathers goals, questions, and to-dos from your sessions | changed | Nagłówek bez zmian. Stary podtytuł miał "to-do's", listę bez spójnika, powtórzone "All" i żargon produktowy "fueled by your therapy context". Nowa linia mówi to samo prosto ("from your sessions") i mieści się w 2 liniach (wcześniej 3). "threads" wypadło, bo przy zimnym czytaniu kojarzy się z aplikacją Threads. "Questions" to nazwa sekcji w apce (`workspace_topicsTitle`). |
| 7 (było 4) | See your / **therapy timeline** | Every session, note, and breakthrough **in one feed** | kept | Nowe kompaktowe filtry nie wymagają zmiany tekstu. "breakthrough" zostaje: opisuje wpis użytkownika i nie obiecuje efektu terapii (backend też mówi o "breakthrough realizations"). |
| 8 (było 7) | Watch your / **strengths grow** | **Character** turns your notes and sessions into a map of your skills | changed | Character nie liczy już aktywności. Pokazuje radar mocnych stron (Courage, Insight, Honesty, Resilience, Kindness, Commitment), poziom z kroków umiejętności i "Your map", a wszystko powstaje z treści wpisów (`ke_aboutIntro`, `ke_aboutMapBody`, `ke_aboutLevelBody`). Orka nie jest już w centrum, więc "grow your orca" jest nieaktualne. "Level up your therapy" sugerowało, że apka ulepsza samą terapię. Nowy nagłówek opisuje to, co widać na ekranie, a statystyki radaru tylko rosną ("Stats only go up"), więc "grow" jest prawdą. |
| 9 (było 8) | (testimonial) | (testimonial, treść bez zmian) | kept | Treść opinii bez zmian. Jedna poprawka w layoucie, nie w opinii: w podpisie przed "Rachel K." stoi em-dash (U+2014). Usuń sam znak i zostaw `Rachel K., Austin, TX` w osobnej linii; kursywa wystarczy jako znak podpisu. Tylko App Store. |

Uwagi do screenów pod nowe copy:
- Slajd 1: Main z wypełnionymi kaflami (sesja, agenda z liczbą tematów, to-do, nawyki). Jeśli na screenie jest kafel "Your first week", użyj wariantu podtytułu z tabeli.
- Slajd 8: karta z radarem i odznaką poziomu, z wypełnionymi wartościami. Nie pokazuj stanu pustego ("Strengths: none yet").

## 2. Rekomendowana kolejność

**App Store (9 slajdów):**
1. Main: Your therapy week / at a glance
2. After Therapy: Never forget / a session again
3. Session recording: Be present / We'll take notes
4. Reflect: Make every session / count twice
5. Prep card: Always know / what to talk about
6. Workspace: All your therapy work / in one space
7. Timeline: See your / therapy timeline
8. Character: Watch your / strengths grow
9. Testimonial

Dlaczego tak: w wynikach wyszukiwania App Store widać trzy pierwsze pionowe screeny. Te trzy
mają powiedzieć, że to apka do terapii, i pokazać dwie najmocniejsze funkcje: notatkę po sesji
i nagranie sesji. Dalej idzie rytm tygodnia: refleksja między sesjami, przygotowanie, porządek,
historia, wzrost. Testimonial zostaje na końcu, tak jak w obecnym zestawie.
Kolejność "Main na 1" kontra "Never forget na 1" można sprawdzić testem Product Page Optimization
w App Store Connect.

**Google Play (8 slajdów, bez testimonialu):**
1. Main
2. After Therapy
3. Session recording
4. Reflect
5. Prep card
6. Workspace
7. Timeline
8. Character

## 3. Flagi polityki Google Play

Źródło: Play Console Help, "Add preview assets to showcase your app"
(https://support.google.com/googleplay/android-developer/answer/9866151). Zasady tekstu na
screenshotach są tam w sekcji "Highly recommended", a nie "Requirements". Naruszenie nie zdejmuje
listingu, ale może zmienić sposób wyświetlania grafik albo zablokować promocję w sklepie.

1. **Testimonial (slajd 9) łamie dwie zasady naraz.** Ma opinię użytkownika i 5 gwiazdek (sugestia
   oceny), a do tego nie pokazuje apki, choć Play chce na screenach "actual in-app experience".
   Na Play go nie wgrywamy (zgodnie z planem).
2. **Słowo "New" jest na liście Play** razem z "Best", "#1", "Top" i "Million Downloads". W nowym
   zestawie go nie ma. Na Play nie dodawaj też plakietek "New" ani "Now with" przy Main i Character
   (to również tekst, który szybko się dezaktualizuje).
3. **Tekst ma zajmować najwyżej 20% obrazu.** Trzylinijkowy podtytuł Workspace był na granicy.
   Teraz wszystkie podtytuły mają do około 70 znaków, czyli 2 linie przy obecnym rozmiarze fontu.
   Nie powiększaj fontu.
4. **Bez wezwań do akcji** ("Download now", "Try now"): w zestawie ich nie ma. Nie przenoś na
   screeny blogowego "Try it free in MindSync".
5. **Rankingi, nagrody i ceny:** w copy ich nie ma. Jedyna kwota to "$100 a week" w testimonialu,
   czyli koszt terapeuty w cytacie, a nie cena apki. Ten slajd idzie tylko do App Store.

## 4. Pozostałe flagi (oba sklepy, poza samym copy)

- **Kiedy wgrywać:** Main v3 i Character v2 są dziś w buildzie z origin/dev (TestFlight). Backend
  działa od v574/v576, a KE jest włączone od 19.10. Nowe screeny wgrywaj dopiero razem z wersją
  sklepową, która ma te ekrany. Screeny muszą pokazywać aplikację, którą użytkownik faktycznie
  pobierze (Apple 2.3.3, Play "actual in-app experience").
- **Apple 2.3.10:** w obecnym zestawie slajdy Reflect i Character mają androidowy pasek statusu
  w ramce iPhone'a. Screeny do App Store renderuj z paskiem iOS.
- **Do przerenderowania z obecnego zestawu:**
  - Reflect i Character mają starą nawigację (Therapy, Stats). Aktualna to Main, Timeline, Reflect, Workspace, Character.
  - Na slajdzie Character jest polski tekst ("W ostatnich 2 tygodniach...").
  - Na slajdzie nagrania podsumowanie przeczy samo sobie ("Duration is unclear... short, brief recording" obok "1h 20min"), a temat (śmierć na raka mózgu) jest za ciężki na sklep. Użyj spokojniejszej sesji demo.
  - Na Workspace widać "in 1 days" (stary string, nowy `ws_agendaSessionMeta` ma już liczbę mnogą).
- **Myślniki w samym UI:** karta na Timeline pokazuje "From Prep" i em-dash przed datą. W
  `app_en.arb` (worktree store-shots) jest 42 wystąpienia U+2014/U+2013, np. w
  `recording_privacyBody`. To nie jest copy sklepu, ale te znaki widać na screenach, więc zgłaszam
  to do `flutter-mobile` przez leada. Tutaj nic nie ruszałem.
- **Testimonial:** trzymaj go tylko wtedy, gdy masz zapisaną zgodę autorki na publikację i opinia
  jest prawdziwa i nieopłacona. Wymaga tego reguła FTC o fałszywych opiniach i rekomendacjach
  z 2024 roku. Treści nie edytujemy.
- **Katalog funkcji:** w `blog/app-features.json` brakuje Main, Habits, planu pierwszego tygodnia
  i Character v2 (mocne strony, mapa). Wpis `personal-bio` nadal opisuje towarzysza, który rośnie
  z aktywnością. Trzeba to zaktualizować (właściciel: operator + backend-api), zanim blog i IG
  zaczną używać tych nazw.

## 5. Kontrole przed akceptem

**Humanizer (embedded, nowe i zmienione linie).** Usunięte w trakcie:
- powtórzenie "one ..." na trzech slajdach (Main miał najpierw "on one screen");
- żargon "fueled by your therapy context" i podwójne "All";
- wieloznaczne "threads";
- dorozumiana obietnica w "Level up your therapy".

Sprawdzenie faktów: każda nazwa w nowych liniach ma pokrycie w kluczach arb wymienionych w tabeli.
Nie dodałem żadnej liczby ani funkcji spoza apki.

**Zimne czytanie (czy w 2 sekundy wiadomo, o co chodzi):**

| slajd | odczyt |
|---|---|
| 1 | Apka porządkuje mój tydzień terapii: najbliższa sesja, tematy, zadania, nawyki. OK |
| 2 | Nie zapomnę, co było na sesji, bo nagram albo napiszę notatkę. OK |
| 3 | Nagrywam sesję i dostaję podsumowanie z tematami i zadaniami. OK |
| 4 | Rozmowa z AI, które zna moją terapię. OK ("count twice" jest lekko abstrakcyjne, ale podtytuł to domyka) |
| 5 | Przygotuję się do sesji w minutę. OK |
| 6 | Cele, pytania i zadania z sesji w jednym miejscu. OK |
| 7 | Cała historia terapii w jednym feedzie. OK |
| 8 | Widzę swoje mocne strony i umiejętności, zbudowane z moich notatek i sesji. OK (radar na screenie pomaga) |

**Checklista (wszystko spełnione):**
- [x] pisownia US (to-dos, realizations)
- [x] zero superlatywów, "#1", "Best", "Top", "New"
- [x] zero cen w copy
- [x] zero CTA typu "Download now"
- [x] YMYL: brak obietnic leczenia i diagnoz, MindSync opisany jako narzędzie do pracy między sesjami
- [x] słownik marki: Reflect, Workspace, MindSync
- [x] tylko funkcje obecne w apce, sprawdzone w arb
- [x] zero U+2014 i U+2013
