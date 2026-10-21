# Partia 7: nowa wersja aplikacji (2 wpisy). Ściąga faktów z kodu + briefy A i B

> Data: 2026-10-21. Autor: `seo-content-writer`. Wykonawca prozy: `blog-writer` przez skill
> `blog-write` (humanizer z próbką `docs/blog/voice-sample-monika.md`, `scripts/blog-voice-check.py`,
> akcept `brand-voice-manager` wg §2.5, schema `seo-tech-lead`, hero `graphic-designer`).
> **Treść po ANGIELSKU.** Format kolejki: `blog/queue/_format.md`. Głos: `docs/blog/brand-mindsync.md` §2.
>
> **Źródło faktów:** kod frontu z worktree `mindsync-frontend-wt-store-shots` (branch
> `feat/store-shots-a3v2` = origin/dev + testy), plik `mindsync_app/lib/l10n/app_en.arb` i ekrany
> (ścieżki FE niżej względem `mindsync_app/`), plus backend `MindSync/app/` tam, gdzie front tylko
> wyświetla to, co ustala serwer (kolejność kroków planu, progi Character, auto karta przed sesją).
> Teksty zaakceptowane, z którymi briefy są spójne: `store/listing.md` A6 i B4,
> `social/queue/2026-10-27-new-main.json`, `2026-10-23-character-tab.json`,
> `2026-10-21-therapy-cards-redesign.json`, `email/2026-10-23-new-look/copy.json`.
>
> **Status bramki KROK 0:** lista w §6 (format preflight). Wynik policzony ręcznie wg logiki
> `scripts/blog-coverage-preflight.py`: **2x OK, 0 RYZYKO, 0 BRAK** już na obecnym katalogu
> (keywordy to dosłowne podciągi funkcji `live`, sprawdzone przeciw blobom `streaks`
> i `therapist-sharing`). Lider uruchamia po zapisaniu §6 jako `blog/queue/_preflight-partia7.json`:
> `python scripts/blog-coverage-preflight.py --temat blog/queue/_preflight-partia7.json`.

---

## 0. Najważniejsze w 10 punktach (przeczytaj przed resztą)

1. **Warunek twardy przed pisaniem: aktualizacja katalogu `blog/app-features.json`.** Brand doc §2.3
   każe pisać nazwami z katalogu, a katalog nadal mówi „Prep Card", „After-therapy debrief",
   „Wellbeing check-ins" i nie zna Main, planu pierwszego tygodnia, Character, Orki ani What Orca
   remembers. Bez aktualizacji wpis musiałby albo przeczyć apce, albo nazwom na kartach. Propozycje
   nowych pozycji i korekt: §5. Gdy katalog nie zdąży, briefy podają karty zastępcze (tylko
   istniejące id).
2. **Wpis A:** slug `whats-new-in-mindsync`, H1 „What's New in MindSync: Your Whole Therapy Week on
   One Screen". Strona „żywa": przy kolejnym dużym wydaniu przepisujemy ją w miejscu (ten sam slug).
3. **Wpis B:** slug, H1 i intencja zostają. Tytuł „How to Use MindSync: Your First Week, Step by
   Step" pasuje TERAZ lepiej niż wcześniej, bo apka ma dosłownie plan „Your first week" z 8 krokami.
   Warunek: numerowane „kroki" we wpisie = kroki planu w apce 1:1 (kolejność i tytuły), a rady wokół
   sesji (Before therapy, nagranie, After therapy) idą jako osobna sekcja bez numerów kroków.
4. **Plan pierwszego tygodnia ma dwa warianty** (serwer): pozycje 3 i 6 zależą od tego, czy osoba
   jest w terapii I dała zgodę „Personalise to your therapy". Wpis B opisuje wariant „w terapii"
   i jednym zdaniem zamianę dla reszty.
5. **Character (nowy, KE) w kodzie jest domyślnie WYŁĄCZONY** (`MindSync/app/core/config.py:508`).
   Według pamięci projektu operator włączył go wszystkim 19.10 (Heroku v576). Nie zweryfikowałem
   tego na prodzie. Przed publikacją potwierdzić (NIEPEWNE nr 2).
6. **„Transcript" z nagrania sesji:** w kodzie karty nagrania nie ma widoku transkrypcji (jest
   Summary, Questions, To-do, Threads, Realizations, Other speaker). Stary wpis B i katalog obiecują
   „transcript". W nowych tekstach: „summary card", nie „transcript".
7. **Trial i Free:** 4 dni Premium za darmo po rejestracji, potem Free z miesięcznymi limitami. Stare
   FAQ „full access, does not ask for a card" jest nieaktualne. Bez liczb limitów i bez cen.
8. **Orca:** zawsze „MindSync's AI therapy assistant" + „between sessions" + „isn't a therapist"
   (`social/brand-instagram.md` §4.1). Zero „companion", „AI therapist", „AI therapy".
9. **Kolejność:** najpierw A (nowy wpis), potem aktualizacja B ze zwykłym linkiem do A. Bez
   `[LINK-LATER:]` (pamięć projektu: nigdy się nie odrabia). A dopiero, gdy wersja jest w obu
   sklepach, a Google Play ma 100% rolloutu (ten sam warunek co mail z 23.10).
10. **Stare zrzuty:** obie ilustracje w treści B (`app-ios-3.webp`, `app-ios-4.webp`) i zrzuty
    w katalogu (`app-ios-1..6.webp`, pole `screenshot`) pokazują STARY interfejs. Karty `[FEATURE:]`
    na obu wpisach pokażą stare ekrany, dopóki operator nie podmieni plików (kandydaci: §1.17).

---

## 1. Ściąga faktów z kodu (z odwołaniami)

Oznaczenia: **[FE]** front, **[BE]** backend, **[NIEPEWNE]** do potwierdzenia. arb = `lib/l10n/app_en.arb`.

### 1.1 Dolna nawigacja i przycisk „+"
- 5 zakładek, w tej kolejności: **Main, Timeline, Reflect, Workspace, Character** [FE]
  `lib/screens/main_page/main_page_body.dart:487-493` (pager) i `:798-826` (pasek); etykiety arb
  815 `nav_main` „Main", 816 `nav_therapy` „Timeline", 817 „Reflect", 2891 „Workspace", 819 „Character".
- Przycisk **„+"** jest globalny, na każdej zakładce **oprócz Reflect** (`main_page_body.dart:675-677`,
  warunek `selectedIndex != 2`). Otwiera cztery: **After Therapy, Prepare for Therapy, Between
  Sessions, Record Session** (arb 2238-2241; obsługa `main_page_body.dart:693-755`). Ekran About Main
  mówi to samo zdaniem: „Use the + button to add an After Therapy note, prepare for a session, write
  between sessions or record a session." (arb 4259 `mc_aboutP4`).
- ⚠ Stary wpis B: „The big button on the Main tab opens four things". Cztery opcje się zgadzają,
  ale przycisk nie jest już przyciskiem Main, tylko całej apki, a etykiety to „Prepare for Therapy"
  i „After Therapy".

### 1.2 Main (nowy ekran startowy)
- Main MC v3 jest ciałem zakładki Main **dla każdego konta** (`lib/screens/main_tab/main_tab_screen.dart:44-51, 139`).
- **8 kafelków, dwa w rzędzie, w tej kolejności** (`lib/screens/main_tab/mc/mc_main_screen.dart:66-75`;
  etykiety arb 4131-4145): **Next therapy session, Therapy Agenda, To-do, Habits, Focus Areas,
  Therapy Relationship, Weekly observations, Daily affirmation.**
- Nad nimi, póki plan trwa, szeroki kafel **„Your first week"** (arb 4147; `mc_main_screen.dart:1011-1052`).
- Nagłówek: powitanie, Menu (szuflada), ikona info „About Main" (arb 4125-4127). Pod kafelkami
  wiersz statusu trialu albo Free (`mc_main_screen.dart:955-965`).
- **Niebieska kropka:** „A blue dot means something is waiting today or this week, or something new
  has arrived." (arb 4255). Kafel otwiera swoją funkcję w wysuwanym panelu (`openSheet`, `mc_main_screen.dart:501-540`).
- Kafel sesji zmienia się z czasem (`lib/screens/main_tab/mc/tiles/mc_tile_models.dart:347-449`):
  bez sesji „Not set / Set up your session"; do 2 dni przed sesją kropka i „Prepare your notes"
  (`mcPrepDotDays = 2`, `:251`); „Prep card on the way", „Prep card ready"; po sesji kropka
  i „After therapy / Note your takeaways"; między sesjami „Capture your thoughts" (arb 4165-4183).
  Pusty stan: „Add it once, weekly or one-off. Main then helps you prepare the day before and note
  what you took away after." (arb 4273).
- Habits: ostatnie 7 dni, „Missed one? Tap it to check it off." (arb 4331); dobre i złe nawyki
  (arb 4353-4359); **Free: 1 nawyk** („Free includes 1 habit. Adding more opens the Premium plans.",
  arb 4341, `lib/screens/main_tab/mc/sheets/habits/mc_habits_sheet.dart:370`).
- Focus Areas: „Track anything you want to keep an eye on: a feeling, a symptom or a behavior. Each
  day, rate how strong it was from 1 to 10." (arb 4381); wykres „Last 14 ratings" (arb 4417); opis
  trendu słowami po „Refresh description" (arb 4413-4415); edycja: dodaj, archiwizuj, usuń, przywróć
  (arb 4423-4441). Zmiany nazwy obszaru w panelu nie widać.
- Therapy Relationship: krótki check-in dzień po sesji, „It shows up a day after a session, until
  you answer." (arb 4275, 4281). Weekly observations: pierwsze „after your next session or on Monday"
  (arb 4283). Daily affirmation: „Comes each morning" (arb 4251).

### 1.3 Plan pierwszego tygodnia (8 kroków)
- Kolejność i warianty ustala serwer [BE] `MindSync/app/services/first_week/step_plan.py:58-90`.
  Tytuły i opisy kroków w apce: arb 4489-4627, mapowanie `lib/screens/main_tab/mc/week/mc_week_steps.dart:55-147`.
- **Wariant „w terapii"** (zgoda ART9 aktywna ORAZ status terapii albo zapisany termin sesji,
  `step_plan.py:233-237`):

| # | Tytuł w apce (arb) | Meta w apce | Przycisk w apce | Co go zalicza [BE] `step_plan.py:263-288` |
|---|---|---|---|---|
| 1 | **Set up your account** (4489) | Setup · 3 min | brak | koniec onboardingu (zawsze zaliczony, gdy widzisz plan) |
| 2 | **Answer Orca's question** (4503) | Reflect · 3 min | „See the question" (po pierwszej rozmowie) albo nowa rozmowa w Reflect (gdy pierwszą pominięto) | pierwsza rozmowa w Reflect PO onboardingu (sama pierwsza rozmowa się nie liczy) |
| 3 | **Add your next session** (4517) | Next therapy session · 1 min | „Add my session" | zapisany termin sesji (jeśli podany w setupie, krok jest zaliczony od razu) |
| 4 | **Leave a voice note** (4531) | Between Sessions · 1 min | „Record a voice note" | dowolna notatka Between Sessions |
| 5 | **Quick check-in** (4545) | Focus Areas · 30 sec | „Start check-in" | dowolna ocena w Focus Areas |
| 6 | **Save one thing for therapy** (4559) | Therapy Agenda · 1 min | „Add to my agenda" | dowolny punkt na agendzie |
| 7 | **Keep a small habit** (4573) | Habits · 1 min | „Open Habits" | odhaczenie dowolnego nawyku |
| 8 | **Your first week** (4587) | Weekly recap · 2 min read | „See my week" | otwarcie podsumowania tygodnia |

- **Wariant „nie w terapii albo bez zgody ART9"** (`STEPS_NOT_IN_THERAPY`, `step_plan.py:70-80`):
  krok 3 = **Talk with Orca again** (Reflect · 3 min, arb 4601; zalicza druga rozmowa w Reflect),
  krok 6 = **Save a question for later** (Workspace · 1 min, arb 4615). Reszta bez zmian.
- Wstęp planu: „Eight small steps for your first week. Each takes a few minutes and helps you get
  more out of therapy." (arb 4455). Stany wierszy: Done / Today / Coming up (arb 4459-4463).
- Krok nie ma dnia. Zalicza go realne działanie, także zrobione poza planem, w dowolnej kolejności
  (`step_plan.py:26-27, 263-288`). Plan pokazuje pierwszy niezaliczony jako „Today" i daje jeden
  pomarańczowy przycisk do niego (`mc_week_plan_sheet.dart:249-288`). Kroki nie są blokowane.
- Po zaliczeniu kroku okienko **„One step forward!"** (arb 4467) z następnym krokiem; po ostatnim
  **„You did every step!"** i „Your first week is done, and you're ready to go. Explore the rest of
  MindSync at your own pace." (arb 4483-4485).
- **Przypomnienie opcjonalne:** wiersz „Remind me about my next step / A daily nudge until your steps
  are done" w planie i „Remind me tomorrow" w okienku (arb 4473-4477; `mc_week_cubit.dart:217-293`
  prosi o zgodę systemu na powiadomienia). W tonie „gentle" przypomnienia nie ma.
- Szeroki kafel znika, gdy wszystkie 8 zaliczone (`mc_week_state.dart:69-73`). Plan jest aktywny do
  27. dnia od rejestracji, czyli około czterech tygodni (`step_plan.py:89-90, 319-324`).
- **Krok 8 (podsumowanie)** otwiera się od 7. dnia albo wcześniej, gdy kroki 1-7 są zaliczone [BE]
  `MindSync/app/services/first_week/recap.py:10-19`. Treść: „What you did", „Where things are"
  (setup vs ostatni check-in), „{Orca} noticed", „You mentioned" (z „Not right"), „Your rhythm from
  here" z opcjami „Before and after each session", „Quick check-in on Mondays", „A talk with Orca on
  Wednesdays", „A voice note on Fridays" i przyciskami „Keep this rhythm" / „I'll find my own way"
  (arb 3921-4006).
- Kto widzi plan: konta z kotwicą pierwszego tygodnia (nowe). Starsze konta dostają 204 i plan się nie
  pokazuje (`mc_week_cubit.dart:29, 95-97`). Mail z 23.10 mówi to samo („consider yourself graduated").

### 1.4 Po rejestracji: setup i pierwsza rozmowa z Orką
- Setup (onboarding, arb 80-239 i 2835-2848): ekran prawny („MindSync is not a medical device",
  zgoda, 16+), „What do you want to keep an eye on?" (Depression, Anxiety, Relationships, Trauma,
  Self-esteem, Burnout, Grief albo własne), „How strong is each one right now?" (1-10, „This is your
  starting point"), „Are you in therapy right now?", „Personalise to your therapy" (zgoda ART9),
  „What kind of therapy is it?", „When is your next session?" (Weekly / Every 2 weeks / Custom albo
  „I don't have a date yet"), „Meet your orca... Give it a name" (domyślnie Orca, można nadać inne
  imię), „How should Orca talk to you?" (Realist, Coach, Friend, Sage, Explorer), skąd o nas wiesz.
  [NIEPEWNE] dokładna kolejność ekranów; nie podawać jej w tekście.
- Potem przepływ `/wow` (`lib/screens/wow/wow_screen.dart:34-39`): **Build → Reveal → Intro →
  First conversation → Offer step 1 (recap + 2-week starter pack) → Offer step 2 (wszystkie plany)
  → Reminders (opcjonalnie) → Home (Main).**
- Reveal: „Next: meet Orca", „A 3-minute voice conversation", „About 3 minutes · You can stop
  anytime" (arb 3198-3205).
- **Pierwsza rozmowa:** „{Orca} starts with three short questions to get to know you, then the
  conversation is yours." (arb 3210; wariant gdy setup wypełniony 3208). Pasek „Getting to know you
  · 1 of 3" (arb 3233). Domyślnie głos („Start talking", mikrofon), alternatywa „Can't talk right
  now? Type instead" (arb 3228-3230). „Then, talk about anything. As long as you like. You end it,
  not Orca." (arb 3222-3223). „Private to you." (3225). „{Orca} keeps short notes from your
  conversations so it can remember you. You can see or delete them anytime in Settings." (3226).
  Można pominąć („Skip for now", 3276; „Your first talk with Orca can wait until you're ready.", 3621).
- Tematy trzech pytań zależą od setupu: np. „How {area} showed up this week", „What has helped, even
  a little", „What you want from {weekday}'s session" (arb 3212-3221).
- Po rozmowie ekran „What {Orca} heard" (3283) i „Saved in Reflect. Your next Before therapy card
  starts from this." (3289-3291).
- Głos poza trialem: „Voice conversations are part of Premium. You can keep going here in writing."
  (arb 3370).

### 1.5 Orca: nazwa i rama
- W kodzie Orca to imię, które użytkownik może zmienić (setup arb 216; zmiana później:
  `character_renameOrca` arb 1202, `lib/screens/character_tab/widgets/pet_hero_card.dart:315`;
  [NIEPEWNE] czy ten przycisk jest osiągalny w nowym Character). We wpisach: „Orca" i raz zdanie, że
  w setupie można nadać inne imię.
- Ramowanie (decyzja Darka 19.10, `social/brand-instagram.md` §4.1): „MindSync's AI therapy
  assistant", „between sessions", „isn't a therapist", czasowniki asks, listens, remembers, sums up,
  helps you prepare. ⚠ Apka sama w paru miejscach pisze „Companion" (np. arb 4725 `ke_companionLabel`):
  nie przenosimy tego do prozy.

### 1.6 What Orca remembers
- **Gdzie:** Settings (Menu → Settings), wiersz „What {Orca} remembers" pod sekcją Persona, nad
  powiadomieniami (`lib/screens/settings/settings_body.dart:196-223`; arb 3312).
- **Co pokazuje:** „{Orca} keeps short notes from your conversations, so the next one can pick up
  where you left off and feel more personal." (3316). Grupy: On your mind, What helps, Goals,
  Routines, People, For therapy, Other (`lib/screens/orca_memory/orca_memory_screen.dart:576-582`,
  arb 3336-3342, 3395-3398). Źródło notatki: First conversation, After therapy, Before therapy,
  Journal, Between Sessions, Session recording, Past entries (`:600-615`, arb 3399-3408). Filtr.
- **Gdzie Orca ich używa:** Conversations i Before therapy cards (pigułki, `:489-499`), tekst arb
  3372 dodaje Personal Bio.
- **Co pozwala:** usunąć pojedynczą notatkę („Forget this note") albo wszystkie („Forget everything",
  arkusz potwierdzenia, „This can't be undone"). „Forgotten notes are deleted for good, and {Orca}
  won't learn them again from past conversations. If you bring something up again later, {Orca} may
  remember it again." (arb 3318, 3331-3335, 3401-3403; sekcja „You're in control", `:897-926`).

### 1.7 Karty Before therapy, After therapy, Session recording
- **Before therapy** (`lib/screens/therapy_capture/widgets/prep_card_widget.dart:20-36, 499-504`):
  nagłówek (data sesji, terapeuta, chip „Based on limited data"), **Summary**, **Questions** (do
  3 pytań, numerowane), **To-do** („Suggested for this week"), **Threads**, **Realizations**,
  **Patterns**, **Focus Areas** („Feelings, symptoms and behaviors you track, this week", trend
  słowem easing / steady / heavier). Puste sekcje się nie pokazują. Jedna edycja całej karty („Edit
  this card") i udostępnianie jako obraz. Etykieta typu „Before therapy" (arb 4007).
- **After therapy** (`lib/screens/debrief_capture/widgets/session_card_widget.dart:19-29`):
  nagłówek z datą i panelem **„Your progress in therapy"**, Summary, Questions, To-do,
  Threads, Realizations. Edycja i obraz jak wyżej.
- **„Your progress in therapy"** (arb 4039-4074; `therapy_progress_panel.dart`): linia ostatnich
  sesji z punktem „Today", status słowny **„Getting steadier" / „Holding steady" / „A harder
  stretch"** (opis w arb: „Descriptive only, never a score", „Must never read as failure"), chipy
  „Focus areas easing / steady / feel heavier", liczba notatek, nagrań, rozmów z Orką, stopka „Based
  on your focus areas, notes and recordings since {date}." **Zablokowany do 3 sesji:** kłódka,
  „Unlocks after 3 sessions" i „2 of 3" (`therapy_progress_panel.dart:66-69, 168-210`; liczbę podaje
  serwer). Bez zgody PROFILING: „Profiling consent is required to show your progress" (arb 4063).
- **Session recording card** (`lib/screens/therapy_tab/widgets/recording_summary_widget.dart:19-30, 298-323`):
  Summary, chip długości i „2 speakers", Questions (to są **pytania zadane przez terapeutę**,
  pole `therapistQuestions`), To-do, Threads, Realizations, Other speaker. Bez edycji.
  **Widoku transkrypcji nie znalazłem** (grep „transcript" w `lib/screens/therapy_tab` = 0 trafień
  poza komentarzem notatki).
- **Auto karta przed sesją [BE]** `MindSync/app/tasks/prep_card_auto_generate.py:3-20, 83-90`:
  co godzinę; jeśli sesja jest za 23-25 godzin, osoba ma aktywną subskrypcję, zapisany termin i zgodę
  ART9, a karty jeszcze nie ma, serwer robi kartę sam. Na Free kartę robisz ręcznie z „+" →
  Prepare for Therapy (miesięczny limit). Zgodne z ekranem oferty „A Before therapy card the day
  before each session" (arb 3298) jako korzyść Premium.

### 1.8 Timeline
- Filtry (kolejność z kodu, `lib/screens/therapy_tab/therapy_tab_screen.dart:504-519`; etykiety arb
  1797-1818, 4007): **All, Before therapy, After therapy, Reflect, Recording, Between sessions,
  Realization, Weekly, Monthly, Therapy Relationship.**
- „Generate now" przy podsumowaniu tygodnia (arb 1843). Usunięte wpisy można przywrócić w ciągu
  24 godzin (arb 1854, 1895-1900).
- Tygodniowe podsumowania generują się dla Free i Premium [BE] `MindSync/app/tasks/weekly_therapy_summary.py:302`.
- ⚠ Check-iny Focus Areas NIE są na Timeline (nie ma takiego filtra). Stary wpis B i katalog
  (`timeline`) mówią „every session, note, check-in and realization": do poprawki.

### 1.9 Workspace
- Stała kolejność modułów (`lib/screens/workspace/workspace_screen.dart:37-45`): **Next session
  agenda → To-do → Questions → Goals → Threads → Realizations → Therapy relationship.** Etykiety:
  „Agenda" z nadtytułem „Next session agenda" (arb 2954, 3001), „To-do", „Questions", „Goals",
  „Threads", „Realizations" (2935, 2955-2957, 3098). Białe karty, jedna kolorowa (agenda).

### 1.10 Character (nowy, „KE")
- About (arb 4651): „Character shows what you are learning about yourself, built from your notes,
  talks with Orca and sessions. Change is hard to see from the inside. Here you can see it, and bring
  it to your next session."
- **6 mocnych stron** z definicjami z apki (arb 4755-4777): **Courage** („Doing or saying the hard
  thing, even while scared."), **Insight** („Working out what you feel and what sets it off."),
  **Honesty** („Saying how things really are, to yourself and to others."), **Resilience** („Going
  back to something after a setback."), **Kindness** („Treating yourself the way you'd treat a
  friend."), **Commitment** („Sticking with what matters to you, in small steps.").
- Liczą momenty z notatek, rozmów i sesji, „They only go up", „Opening the app on its own does not
  count" (arb 4653, 4665, 4789). **Not quite** usuwa moment („Removed. This moment no longer
  counts.", arb 4779-4783); dla umiejętności „This isn't me, remove it" (5045).
- **Mapa:** uczucia, nad którymi pracujesz (Worry, Anger, Sadness, Guilt, Shame, Fear, Loneliness,
  Overwhelm, Grief, Joy, Calm, Pride, Closeness; arb 4899-4923), a pod nimi umiejętności. Zakładki
  **Stats, Skills, Tools** (4749-4753). **Cztery etapy umiejętności: Discovered, Practicing, Growing,
  Yours** (arb 4655, 4819-4825; posty IG wymieniają trzy ostatnie, apka sama mówi o czterech).
  Progi [BE] `MindSync/app/services/ke/constants.py:206-210`: Growing = 3 razy w 2 różnych
  tygodniach, Yours = 6 razy w 4 różnych tygodniach, w tym raz, gdy było trudno.
- Ideas (kropka przy umiejętności, „Not now" chowa na 2 tygodnie, arb 4659), Tools („Ways of coping
  you have actually used", 4661), Level (krok za każdy awans etapu, 4665), „Save as image, without
  your words" (5093).
- Wymaga zgody PROFILING (bez niej widok blokady, `lib/screens/character_tab/character_tab_screen.dart:809-812`);
  gdy serwer nie obsługuje KE, apka pokazuje starszą wersję (`:137-145, 199-200`).
- [NIEPEWNE] patrz §1.16 pkt 2 (przełącznik na prodzie) i pkt 3 (historia tylko dla Premium).

### 1.11 Reflect: dawne rozmowy
- Z listy rozmów w Reflect stuknięcie otwiera podgląd tylko do odczytu: Summary, Conversation (głos
  albo pisana), przycisk „Continue this conversation" (arb 4075-4098; trasa
  `lib/navigation/ms_routes.dart:836-850`, wywołanie w `lib/screens/reflect_tab/reflect_tab_screen.dart`).

### 1.12 Nagrywanie sesji
- Przed pierwszym nagraniem ekran prywatności i zgody z polem: „I confirm that I have my therapist's
  explicit consent to transcribe our sessions..." i przycisk „I Agree, Let's Record" (arb 2174-2177);
  arkusz „Recording Consent & Privacy" o zgodzie wszystkich stron i o kasowaniu nagrania po
  podsumowaniu (2180-2181); przypomnienie „Make sure your therapist has consented." (2183).
- „Sessions shorter than 10 minutes won't be processed." (2187, 2199).
- Na Free nagrania mają limit łączny (nie miesięczny); po wyczerpaniu zamiast nagrywania otwiera się
  paywall (`main_page_body.dart:731-739`; arb 2209, 3905 „Session recordings: {n} in total").

### 1.13 Free i Premium (tylko to, co jednoznaczne w kodzie; bez cen i bez liczb limitów)
- Po rejestracji **4 dni Premium za darmo** („Your free 4 days have already started", arb 3309;
  „Your free 4 days are on.", 3311; „Keep {Orca} with you after day 4", 3293). Bez zakupu.
- Po trialu **Free z limitami miesięcznymi**: Before therapy, After therapy, Between Sessions,
  wiadomości Reflect (pisanie); nagrania sesji limit łączny (arb 3905). Liczby podaje serwer
  (`GET /users/usage`), więc ich nie cytujemy (stan z `store/listing.md` D9: 1/1/3/15 i 2 nagrania).
- **Rozmowa głosowa z Orką = Premium** po trialu; pisanie zostaje na Free (arb 3903, 3370).
- **Free: 1 nawyk** (arb 4341). **Quick check-in zawsze darmowy** (arb 3577, 3603, 3981), **agenda
  zawsze darmowa** (3975).
- Oferta jednorazowa „2 weeks of Premium, one payment... Nothing renews." (arb 3907-3909): we wpisach
  nie opisujemy, od cen i ofert jest `/membership`.

### 1.14 Setup a starszy wpis B: co się zmieniło
- „Pick two or three areas" zostaje prawdziwe (setup + skala 1-10 jako punkt startu).
- „Areas can be added, renamed or removed later in settings" → teraz w panelu Focus Areas na Main:
  dodaj, archiwizuj, usuń, przywróć. Zmiany nazwy nie widać (nie obiecywać).
- „Put your next session date in the app" zostaje (setup albo krok 3).

### 1.15 Rozbieżności z tekstami już zaakceptowanymi (do wiadomości BVM)
- `store/listing.md` A6/B4 i IG: „Finish one and the next one opens." Kod: kroki nie są blokowane,
  każdy zalicza realne działanie w dowolnej kolejności, a plan wskazuje pierwszy niezaliczony.
  Nie jest to sprzeczność dla czytelnika, ale we wpisie B piszemy „the plan points you to the next
  open step", a nie „the next one unlocks".
- IG Character: trzy etapy (Practicing, Growing, Yours). Apka: cztery (z Discovered). Wpis A podaje
  cztery, bo tak mówi ekran About.
- Mail: „It lists every note Orca keeps about you" vs ekran: notatki „from your conversations"
  (i wpisów). Wpis A pisze „every note Orca keeps", jak listing.

### 1.16 NIEPEWNE (nie pisać jako fakt, dopóki ktoś nie potwierdzi)
1. **Układ filtrów Timeline w wersji ze sklepu.** Kod ma zawijane pigułki A3 v2 (zatwierdzone
   19.10), ale `social/queue/2026-10-21-therapy-cards-redesign.json` pole `ekrany_aktualne` mówi
   o jednym przewijanym rzędzie „jak w wersji 2.0.56". We wpisach: „filters at the top of Timeline",
   bez opisu układu.
2. **Czy nowy Character jest włączony na prodzie dla wszystkich.** Kod: `CHARACTER_KE_ENABLED` i
   `CHARACTER_KE_EXTRACTION_ENABLED` domyślnie `False` (`MindSync/app/core/config.py:498-512`).
   Pamięć projektu: operator ustawił je 19.10 13:49 (v576) z `CHARACTER_KE_REQUIRE_PROFILING_OPT_IN=false`.
   Nie sprawdziłem configu Heroku. Potwierdzić (`integration-devops`: `heroku config:get`) przed
   publikacją A.
3. **Historia w Character.** Według pamięci projektu Premium ma wczytane 90 dni wstecz, reszta kont
   zaczyna od pierwszego otwarcia zakładki („Your map starts with your first note or talk.", arb 4747).
   We wpisach: „it fills in from what you share", bez obietnicy, że pokaże przeszłość.
4. **Auto karta Before therapy dzień przed sesją:** backend robi ją dla aktywnej subskrypcji (czy
   trial się liczy, nie sprawdziłem) z zapisanym terminem i zgodą ART9. We wpisach: „open Prepare
   for Therapy" jako ścieżka główna, auto karta najwyżej jako „on Premium, it can be ready the day
   before".
5. **Transkrypcja nagrania:** brak widoku w apce (patrz §1.7). Nie pisać „you get the transcript".
6. **Co liczy się jako „sesja" do odblokowania wykresu** (opis arb 4060: „sessions of any kind").
   Pisać „after three sessions", bez wyjaśniania, które wpisy się liczą.
7. **Wariant planu zależy też od zgody ART9**, nie tylko od odpowiedzi „Are you in therapy". Osoba
   w terapii bez tej zgody dostaje wariant „nie w terapii". Zdanie we wpisie B: „If you're not in
   therapy right now, or you skipped the step that personalises the app to your therapy, steps 3
   and 6 are different" (do akceptu BVM, bo to długie).
8. **Czy trial wymaga karty.** Kod nadaje trial przy rejestracji bez zakupu (arb 3311), więc
   „no card" jest prawdopodobne, ale bezpieczniej słowami listingu: „nothing is charged automatically".
9. **Personal Bio w nowym Character:** istnieje (arb 1214, 3372), ale miejsce w nowym widoku
   niepotwierdzone (prawdopodobnie przez wiersz „Companion"). We wpisach nie opisujemy.
10. **Zmiana imienia Orki po setupie:** przycisk jest w starym widoku Character; w nowym niepewne.
11. **Twierdzenia o prywatności** (AES-256, kasowanie audio): `store/listing.md` D5 blokuje je, dopóki
    stara polityka v1 wisi na stronie. We wpisach tylko link do `/faq` i `/privacy-policy`.
12. **Monthly recap i „Generate now":** czy są tylko na Premium, nie sprawdziłem. Nie pisać.
13. **Wersje 2.0.56 (iOS) i 2.0.117 (Android) i 100% rolloutu na Play:** sprawdzić przed publikacją A.
    Numerów wersji nie wpisujemy w tekst (decyzja BVM w mailu).
14. **Katalog `smart-reminders` „Thirteen notification types":** nie weryfikowałem w nowej wersji.

### 1.17 Prawdziwe ekrany nowej wersji (kandydaci na ilustracje i pole `screenshot`; wybór i upload: operator)
- `store/renders/ios/store_main.png`, `store_prep.png`, `store_after_therapy.png`, `store_recording.png`,
  `store_character.png`, `store_timeline.png`, `store_workspace.png`, `store_reflect.png`.
- `social/images/app-shots/main_v3_home.png`, `main_v3_first_week.png`, `main_v3_week_plan.png`,
  `main_v3_step_done.png`, `main_v3_habits_sheet.png`, `after_card_v2.png`,
  `after_card_progress_locked.png`, `prep_card_v2.png`, `first_conversation_intro.png`,
  `first_conversation_recap.png`, `orca_memory.png`. ⚠ Starsze pliki w tym katalogu (np.
  `check_ins.png`, `mood_trends.png`, `session_prep.png`) to stary interfejs: nie używać.

---

## 2. Zasady wspólne dla A i B

1. **Szkielet Moniki** (§2.2) dostosowany do wpisu produktowego: otwarcie-rozpoznanie bez H2 →
   „skąd to się bierze" (dlaczego to zbudowano / po co jest apka) → krótka sekcja badań (2 badania już
   zweryfikowane na blogu) → „jak to wygląda" (opis ekranów) → „co spróbować" (kroki w trybie
   rozkazującym, jedno gotowe zdanie do powiedzenia) → akapit o apce w rytmie „This is what... Log...
   Give it time... Then..." → jedno osobiste pytanie → `[FEATURES:]` → FAQ.
2. **Badania tylko te, które blog już zweryfikował** (spójność, zero nowego ryzyka): Kessels 2003,
   *Journal of the Royal Society of Medicine* (40% do 80% informacji medycznej zapominane od razu,
   prawie połowa zapamiętanego błędnie; już na `how-to-remember-what-you-talk-about-in-therapy`);
   Kazantzis, Whittington i Dattilio 2010, *Clinical Psychology: Science and Practice* (46 badań,
   1 072 osoby, zadania domowe d = 0.48; już na `how-to-do-therapy-homework`); dla A opcjonalnie
   Jensen-Doss i wsp. 2018, *Administration and Policy in Mental Health* (504 klinicystów z USA,
   13.9% używało standardowego kwestionariusza postępów co najmniej raz w miesiącu; już w
   `store/listing.md` D1 z DOI 10.1007/s10488-016-0763-0). Uczciwe granice: Kessels dotyczy wizyt
   medycznych, nie terapii; badania zadań domowych nie dotyczą aplikacji; nasz wykres to nie
   kwestionariusz kliniczny.
3. **YMYL:** Orca nie jest terapeutą i nie prowadzi terapii; wykres „Your progress in therapy" to
   obraz własnych wpisów, nie ocena zdrowia psychicznego i nic nie mówi o terapeucie; Character
   liczy momenty, nie ocenia; MindSync uzupełnia terapię. Zero obietnic efektów.
4. **Nazwy z apki dosłownie, wielkimi literami jak w apce:** Main, Timeline, Reflect, Workspace,
   Character, Next therapy session, Therapy Agenda, To-do, Habits, Focus Areas, Therapy Relationship,
   Weekly observations, Daily affirmation, Your first week, Before therapy, After therapy, Between
   Sessions, Prepare for Therapy, Record Session, Your progress in therapy, What Orca remembers,
   Not quite, Forget everything. Gdy katalog nie zmieni nazw (§5), nazwa z karty i nazwa z apki się
   rozjadą: to blokuje publikację, nie pisanie.
5. **Bez cen, bez liczb limitów, bez numerów wersji.** Free i Premium opisowo, link `/membership`.
6. **Zakaz U+2014 i U+2013** wszędzie (tytuł, meta, zajawka, treść, karty, schema, alt). Zakres
   liczbowy zwykłym łącznikiem.
7. **Linki wewnętrzne względne** (`/journal/slug`, `/features`, `/faq`, `/membership`, `/audience`,
   `/privacy-policy`). Linki do sklepów zwykłe (`https://apps.apple.com/us/app/mindsync-ai-health-journal/id6739644256`,
   `https://play.google.com/store/apps/details?id=com.mindsync.app`); parametry atrybucji dokleja
   skrypt strony `blogattribution`, nie wpisujemy ich ręcznie.
8. **Karty:** 1-2 inline + jeden blok `[FEATURES:]` z trzema pozycjami. Id wyłącznie z katalogu ze
   statusem `live`; nowe id z §5 dopiero po wpisaniu do katalogu. Zdania kart nowe (nie z partii 1-6).
9. **FAQ:** H2 dokładnie „Frequently asked questions", H3 dosłownie jak w briefie, odpowiedź 40-70
   słów, pierwsze zdanie samodzielną odpowiedzią (GEO, `_format.md` „Odpowiedź do zacytowania").
   Dla tych intencji **GSC nie ma żadnych zapytań w formie pytań** (wpis B: zapytania zanonimizowane),
   więc pytania pochodzą z intencji brandowej i z faktów aktualizacji. Po 4 tygodniach od publikacji:
   `scripts/gsc/blog-partia-frazy.py` i podmiana na dosłowne zapytania z liczbami.
10. **Pole `glos`: `"monika-v1"`.** Humor najwyżej 2-4 obrazki, zero w akapitach o Orce i prywatności.
11. **Jedno zdanie o pierwszej osobie marki** (założyciel, 10 lat, około 130 000 USD) tylko w B (było
    już w B; w A nie powtarzamy).

---

# A. NOWY WPIS: co nowego w MindSync

**1. Meta**
- `seo_url`: **`whats-new-in-mindsync`** | plik: `blog/queue/2026-10-23_whats-new-in-mindsync.json`
  (alternatywa, jeśli operator woli wpis per wydanie: `mindsync-update-october-2026`; rekomenduję
  slug bez daty, żeby fraza brandowa „what's new" miała jeden stały adres).
- kategoria: `MindSync Tips` | `tagi`: `["mindsync-tips", "whats-new"]` | `kolor`: `#ff9f8a`
  (ostatni wpis na żywo `does-insurance-cover-therapy` ma `#339499`, B zostaje przy `#339499`).
- `planowana_data`: **2026-10-23** (dzień maila „new look"), WARUNEK: wersja w obu sklepach,
  Google Play 100% rolloutu. Inaczej przesuń.
- H1: **„What's New in MindSync: Your Whole Therapy Week on One Screen"** (obietnica w duchu §2.1
  pkt 12; „Main" w H1 nic nie mówi komuś, kto nie widział ekranu, ta sama decyzja co w listingu).
- `meta_title` (47 zn.): **„What's New in MindSync: The October 2026 Update"**
  (wariant bez daty, 48 zn.: „What's New in MindSync: Main, Character and Orca"; przy kolejnym
  wydaniu miesiąc w meta zmieniamy razem z treścią).
- `meta_description` (152 zn.): **„MindSync's update: a new home screen, a first-week plan, clearer
  therapy cards, a rebuilt Character and Orca, an AI therapy assistant (not a therapist)."**
- `zajawka_html` (szkic do humanizera): „MindSync opens on a new home screen now. Here's everything
  that changed in this update, from the first-week plan and the new therapy cards to Character and
  Orca, and what to try first."
- długość: 900-1300 słów bez FAQ.

**2. Frazy i intencja**
- główna: `what's new in mindsync` (**brak danych GSC**, nowa intencja brandowa po aktualizacji)
- poboczne: `mindsync update`, `mindsync new features`, `mindsync orca`, `what orca remembers`,
  `mindsync character` (wszystkie bez danych GSC; nie podajemy wolumenów)
- kontekst brandowy z GSC (`migracja/gsc/baseline-2026-09-28/queries.csv`, okno 2025-05-28..2026-09-25):
  `mindsync` 15 805 wyśw. (poz. 4,1), `mindsync app` 1 323 (4,0), `mindsync ai` 994 (5,3),
  `mind sync app` 394 (4,2). **Te frazy trzyma strona główna** (`baseline-2026-09-15/query-page.csv`:
  `mindsync app` i `mindsync ai` na `/` poz. ok. 2,4). ⚠ Kanibalizacja: A NIE celuje w nie w H1 ani
  meta; „MindSync app" może paść raz naturalnie w treści.
- intencja: (1) obecny użytkownik po aktualizacji: „gdzie jest to, co znałem, co to są te kafelki,
  kim jest Orca"; (2) ktoś, kto szuka „mindsync" z dopiskiem „new/update/ai" i chce wiedzieć, czym
  apka jest dziś; (3) asystenci AI, którzy odpowiadają na „what is Orca in MindSync".
- luka: na mindsync.app nie ma żadnej strony, która opisuje Main, plan pierwszego tygodnia,
  Character, Orkę i What Orca remembers (`/features` jest nieaktualne wg katalogu). Ten wpis staje się
  cytowalnym opisem produktu (GEO).

**3. Struktura (H2/H3)**
- **Otwarcie (bez H2, 60-120 słów):** „Do any of these sound familiar?" z trzema scenkami z tygodnia
  między sesjami, ostatnia krótka z mrugnięciem. Materiał (nie kopiuj maila): to-do zapisane
  w jednym rogu telefonu, nawyk zrobiony w czwartek, którego nikt nie odhaczył, pytanie wymyślone pod
  prysznicem, które nie mieszka nigdzie. Potem 1-2 zdania: MindSync to aplikacja dla osób w terapii;
  ta aktualizacja jest o tym, żeby tydzień między sesjami dało się zobaczyć na jednym ekranie.
- **H2: „Why we rebuilt it:"** (skąd to się bierze, 150-200 słów)
  - mechanizm: terapia trwa godzinę, a tydzień rozprasza rzeczy po aplikacjach, kalendarzu
    i pamięci; poprzednia wersja miała je, ale trzeba było wiedzieć, gdzie szukać.
  - Kessels 2003 jednym zdaniem jak historia z rokiem na początku, link w nazwę czasopisma do źródła
    i anchor do wpisu (mapa niżej); granica: wizyty medyczne, nie terapia.
  - Kazantzis i wsp. 2010 jednym zdaniem (praca między sesjami ma znaczenie, d = 0.48); granica:
    badania zadań domowych, nie aplikacji.
  - puenta w stylu: „If the week does the work, the week needs a place to live."
- **H2: „What's new in MindSync, screen by screen:"** (fraza główna w H2; „jak to wygląda"; H3 krótkie,
  60-110 słów każde)
  - **H3 „Main: your therapy week on one screen"**: 8 kafelków po nazwie (lista z §1.2), kropka,
    stuknięcie otwiera panel, „+" na każdej zakładce oprócz Reflect z czterema opcjami, ikona
    About Main. Kafel sesji: dzień przed „Prepare your notes", po sesji „After therapy".
    Inline karta: `[FEATURE: main-home | ...]` (niżej).
  - **H3 „A first-week plan for new accounts"**: 8 małych kroków, kilka minut każdy, bez
    wyznaczonych dni; okienko „One step forward!"; opcjonalne przypomnienie najwyżej raz dziennie;
    plan znika z Main, gdy wszystkie kroki są zrobione. Starsze konta planu nie dostają. Link do B
    (cała lista kroków jest tam, tu jej NIE powtarzamy: granica kanibalizacji).
  - **H3 „Before and after therapy cards, rebuilt"**: Before: Summary i do trzech numerowanych pytań,
    potem To-do, Threads, Realizations, Patterns, Focus Areas. After: „Your progress in therapy" ze
    statusem słownym („Getting steadier", „Holding steady" albo „A harder stretch"), zbudowany z Focus
    Areas, notatek i nagrań, pojawia się po trzech sesjach (wcześniej kłódka i „2 of 3"). **Rama YMYL
    obowiązkowa w tym akapicie:** odbicie twoich wpisów, nie ocena zdrowia psychicznego, nic o
    terapeucie. Opcjonalnie Jensen-Doss 2018 jednym zdaniem + „your chart isn't one of those
    questionnaires". Link do `how-to-know-if-therapy-is-working`.
  - **H3 „Timeline and Workspace, tidied up"**: Timeline z filtrami na górze (wymień etykiety
    z §1.8, bez opisu układu, NIEPEWNE nr 1); Workspace w stałej kolejności (§1.9), jaśniejsze kolory.
    Jedno zdanie, jak to się przydaje („when your therapist asks when this started").
  - **H3 „Character: strengths that grow from your own words"**: 6 mocnych stron z jednozdaniowymi
    definicjami z apki (§1.10; wolno skrócić do listy nazw + jednego przykładu: Courage = „doing or
    saying the hard thing, even while scared"); liczą momenty, otwieranie apki nie liczy się wcale
    (miejsce na jeden obrazek humoru); Not quite; mapa: uczucia, a pod nimi umiejętności; cztery etapy
    Discovered, Practicing, Growing, Yours z progami; Tools; Level; „Save as image, without your
    words". Zdanie „it fills in from what you share" (NIEPEWNE nr 3). Rama: liczba to licznik, nie
    ocena. Linki do `which-coping-skills-actually-work` i `how-to-name-what-you-feel`.
    ⚠ Publikować tę sekcję tylko po potwierdzeniu NIEPEWNE nr 2.
  - **H3 „Meet Orca, MindSync's AI therapy assistant between sessions"**: imię AI w Reflect; „Orca
    isn't a therapist and doesn't replace yours"; nowe konta zaczynają od pierwszej rozmowy: trzy
    krótkie pytania, głosem albo pisząc, około 3 minut, potem rozmowa należy do ciebie; ekran „What
    Orca heard"; pierwsza karta Before therapy startuje z tego podsumowania; dawne rozmowy w Reflect
    można otworzyć i przeczytać; po trialu rozmowa głosowa jest w Premium, pisanie zostaje na Free;
    w setupie można nadać inne imię. Zero humoru w tej sekcji.
  - **H3 „What Orca remembers, in Settings"**: lista notatek, grupy, źródło każdej notatki, usuwanie
    pojedynczo albo „Forget everything"; usunięte znikają na dobre i Orca nie wyczyta ich ponownie ze
    starych rozmów, ale może zapamiętać na nowo, jeśli wrócisz do tematu (uczciwie, słowami z apki).
    Gdzie Orca ich używa: rozmowy i karty Before therapy. Linki do `is-it-safe-to-talk-to-ai-about-mental-health`
    i `are-mental-health-apps-private` **[NA-PROGU]**.
- **H2: „What to try first after you update:"** (co spróbować; 4-5 kroków w trybie rozkazującym)
  1. Open Main and tap whatever has a blue dot.
  2. Add your next session, if it isn't there yet, so the session tile can nudge you the day before
     and after.
  3. Open Character and tap Not quite on any moment that doesn't sound like you (miejsce na obrazek:
     wykres przyjmuje poprawki bez obrażania się).
  4. Visit What Orca remembers once and delete anything you'd rather it didn't keep.
  5. After your next session, open After therapy while it's fresh. Gotowe zdanie na sesję, np.:
     „I wrote a few things down this week. Can we start with the one that stuck?"
  - puenta jednym zdaniem.
- **Akapit o apce (rytm §2.1 pkt 9):** „This is what MindSync's new Main is for. Log the to-do your
  therapist mentioned, the habit you kept on Thursday, the question from the shower. Give it time,
  and the tiles turn those entries into something you can see: what's waiting today, how your Focus
  Areas are moving, which strengths keep showing up. Then take the agenda into the room." (szkic,
  autor przepisuje głosem Moniki)
- **Pytanie do czytelnika:** np. „What's the one thing from your last session you wish had a place to
  wait for you?" (nie kopiować „Which box would you open first?" z IG).
- blok `[FEATURES:]`
- **H2: Frequently asked questions** (5)
  - H3: **What's new in the MindSync update?** → pierwsze zdanie: lista sześciu zmian (GEO A3 niżej).
  - H3: **What is Orca in MindSync?** → definicja GEO A2.
  - H3: **Is Orca a therapist?** → „No." + AI therapy assistant between sessions, nie prowadzi terapii,
    nie zastępuje terapeuty; MindSync is not a medical device (arb 95). Rekomendacja: dopisać „MindSync
    isn't a crisis service. In the US, call or text 988 any time." (zdanie zaakceptowane w listingu;
    decyzja BVM, bo to wpis niekryzysowy).
  - H3: **Can I see and delete what Orca remembers?** → „Yes." + Settings, What Orca remembers,
    pojedynczo albo Forget everything, co się dzieje z usuniętą notatką.
  - H3: **Do I need to update MindSync to see the new home screen?** → „Yes." + aktualizacja w App Store
    albo Google Play, Main jest pierwszym ekranem; plan pierwszego tygodnia i pierwsza rozmowa są dla
    nowych kont. Bez numerów wersji.

**4. Karty funkcji**
- inline w H3 „Main...":
  `[FEATURE: main-home | Everything waiting between sessions on one screen, and a blue dot on the tile that needs you today.]`
- blok przed FAQ:
  `[FEATURES: New in this update || first-week-plan | Eight small steps for your first week, a few minutes each, with no set days. || character | Six strengths that grow from what you write and say, with a Not quite button for the moments that don't fit. || orca-memory | Every note Orca keeps, in one list you can read and clear.]`
- **Zastępcze, gdy katalog nie zdąży** (tylko istniejące id): inline `[FEATURE: workspace | ...]`;
  blok `session-prep`, `session-debrief`, `reflect`. Wtedy jednak nazwy kart („Prep Card", „After-therapy
  debrief") rozjadą się z tekstem: publikacja dopiero po korekcie nazw w katalogu (§5).

**5. Mapa linkowania** (wszystko na żywo, linki względne)
- `<a href="/journal/how-to-use-mindsync">` anchor „how to use MindSync in your first week, step by
  step" (H3 o planie). B jest opublikowany, link działa od razu, także przed aktualizacją B.
- `<a href="/journal/how-to-remember-what-you-talk-about-in-therapy">` anchor „why most of a session
  is gone by Thursday" (H2 „Why we rebuilt it").
- `<a href="/journal/what-to-do-between-therapy-sessions">` **[NA-PROGU, poz. 13,1]** anchor „what the
  days between sessions are actually for" (H2 „Why we rebuilt it").
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „what a progress line can and can't
  tell you" (H3 o kartach).
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` **[NA-PROGU, poz. 15,8]** anchor „walking
  in knowing where to start" (H3 o kartach, Before therapy).
- `<a href="/journal/which-coping-skills-actually-work">` anchor „which coping skills actually work for
  you" (H3 Character, Tools).
- `<a href="/journal/how-to-name-what-you-feel">` anchor „naming what you feel" (H3 Character, mapa).
- `<a href="/journal/is-it-safe-to-talk-to-ai-about-mental-health">` anchor „what happens to what you
  tell an AI" (H3 What Orca remembers).
- `<a href="/journal/are-mental-health-apps-private">` **[NA-PROGU, poz. 8,8]** anchor „what to check
  before you type anything into an app" (H3 What Orca remembers).
- `<a href="/membership">` anchor „what's free and what's Premium" (H3 Orca, zdanie o głosie).
- `<a href="/features">` (karty prowadzą tam same; w tekście opcjonalnie raz).
- **Landing partner:** brak.
- **PATCH po publikacji A** (dla `webflow-publisher`, tylko linki): z `is-it-safe-to-talk-to-ai-about-mental-health`
  do A (anchor „what MindSync's Orca keeps, and how to delete it") i z `are-mental-health-apps-private`
  do A (ten sam anchor albo „an example of an AI memory you can clear").

**6. GEO (szkice EN do humanizera, cytowalne bez kontekstu)**
- **A1 „What is MindSync?" (do akapitu otwierającego H2 albo FAQ 1):** „MindSync is a mobile app for
  people in therapy. It helps you prepare before each session, keep what came up afterward and use
  the days in between, with Before and After therapy cards, voice notes, Focus Areas check-ins and
  Orca, an AI therapy assistant. It supports therapy and doesn't replace it."
- **A2 „What is Orca in MindSync?":** „Orca is MindSync's AI therapy assistant for the days between
  sessions. It asks questions in Reflect, by voice or in writing, keeps short notes so the next talk
  can pick up where you left off, and helps build your Before therapy cards. Orca isn't a therapist
  and doesn't replace one."
- **A3 „What changed in the MindSync update (October 2026)?"** (lista do FAQ 1):
  Main, a new home screen with eight tiles; a first-week plan of eight small steps for new accounts;
  redesigned Before therapy and After therapy cards, with a progress chart after three sessions;
  filters at the top of Timeline and a reordered Workspace; Character rebuilt around six strengths
  and a map of skills; Orca, with a first conversation after sign-up, What Orca remembers in
  Settings, and past Reflect talks you can read again.

**7. Hero i ilustracje**
- Hero (bez ekranów, §4 brand doc): codzienny moment, kilka kolorowych karteczek ułożonych w równą
  siatkę na stole obok telefonu ekranem w dół i kubka, miękkie poranne światło, paleta mint i sand.
- `hero_image_alt`: „Colorful sticky notes in a neat grid beside a phone and a mug on a sunlit table"
- nazwa pliku: `whats-new-in-mindsync-hero.webp`
- Ilustracje w treści (realne rendery, wybór i zgoda operatora, §1.17): `store_main.png` (H3 Main,
  alt „The new MindSync home screen, Main, with eight tiles for the therapy week"),
  `main_v3_week_plan.png` (H3 plan, alt „The Your first week plan in MindSync with eight small
  steps"), `after_card_v2.png` (H3 karty, alt „The After therapy card with the Your progress in
  therapy chart"), `store_character.png` (H3 Character, alt „The MindSync Character tab with six
  strengths on one chart"), `orca_memory.png` (H3 pamięć, alt „The What Orca remembers page in
  MindSync Settings"). Najwyżej 3-4 obrazy.

**8. Schema (dla `seo-tech-lead`)**
- BlogPosting + FAQPage, host zgodnie z konwencją z partii 3 (www). `dateModified` przy każdej
  przyszłej przeróbce „w miejscu". Bez SoftwareApplication z ocenami.

---

# B. PRZEPISANIE: How to Use MindSync (slug bez zmian)

**1. Meta i stan wejściowy**
- plik: `blog/queue/2026-08-25_how-to-use-mindsync.json` (przepisuje `blog-writer`, status na czas
  pracy `szkic`, po akceptach `gotowy`), `seo_url` **`how-to-use-mindsync`** (bez zmian),
  `item_id` **`6a8dd78d9711593bac37a6f8`**: aktualizacja istniejącego itemu w CMS przez `blog-publish`
  (tryb aktualizacji, za zgodą operatora), nie nowy wpis. `datePublished` 2026-08-25 zostaje,
  dochodzi `dateModified`.
- kategoria `MindSync Tips`, `tagi` bez zmian, `kolor` `#339499` bez zmian, hero bez zmian (nie ma
  w nim interfejsu), `hero_image_alt` bez zmian.
- Stan w GSC (`seo/blog/gsc-wyniki/BLOG-WYNIKI-2026-10-21.md`): 26 wyśw., 0 klik., poz. 4,7;
  **zapytania w całości zanonimizowane**; dzienne wiersze w JSON kończą się 2026-09-30 (od 1.10
  zero wyświetleń, ta sama suma 26 co w raporcie z 7.10). Do sprawdzenia przez lidera: URL
  Inspection i ponowne zgłoszenie do indeksu po aktualizacji.
- **Decyzja o tytule:** H1 **zostaje** „How to Use MindSync: Your First Week, Step by Step". Apka
  ma teraz plan, który się dosłownie nazywa „Your first week" i ma kroki, więc tytuł opisuje to,
  co czytelnik zobaczy. Warunek zgodności z apką: sekcja z numerowanymi krokami ma te same 8 tytułów
  w tej samej kolejności co plan (wariant „w terapii"), a cała reszta wpisu (setup, sesja, tydzień,
  po tygodniu) nie używa słowa „step" z numerem. Krok 1 w apce jest zaliczony, zanim czytelnik
  zobaczy plan: wpis to mówi wprost, żeby nie było „u mnie krok 1 jest już odhaczony, a wpis każe
  go robić".
- `meta_title` (50 zn.): **„How to Use MindSync: Your First Week, Step by Step"** (było „How to Use
  MindSync: Your First Week | MindSync": usuwamy podwójną markę; CTR 0% przy poz. 4,7 uzasadnia
  zmianę).
- `meta_description` (146 zn.): **„Just downloaded MindSync? Your first week step by step: the
  eight-step plan, your first talk with Orca, and what to do before and after a session."**
- `zajawka_html` (szkic): „You opened the app and Main greeted you with colored tiles and a plan
  called Your first week. Here's the order that works: setup and your first talk with Orca, the eight
  steps, your first session, and what shows up after a week or two."
- długość: **1200-1600 słów bez FAQ** (świadome odstępstwo od 900-1400 z §2.2: przewodnik z ośmioma
  krokami i sesją; rozstrzyga BVM).

**2. Frazy i intencja**
- główna: `how to use mindsync` (+ wariant `how to use mindsync app`: 37 wyśw., poz. 3,5 na stronie
  głównej w oknie do 2026-08-22, `migracja/gsc/baseline-2026-08-25/query-page.csv:75`; 9 wyśw., poz. 4,0
  w oknie do 2026-09-25). To jedyna potwierdzona fraza tej intencji i powód powstania wpisu.
- poboczne (bez danych): `mindsync first week`, `mindsync getting started`, `how does mindsync work`
- **Granica z A:** B trzyma „how to use / first week / getting started / kroki". A trzyma „what's
  new / update / new features / What Orca remembers / czym jest Orka". B wspomina Orkę i Character
  tylko tyle, ile potrzeba do kroków i odsyła do A. FAQ się nie dublują (B nie ma „What is Orca" ani
  „Is Orca a therapist").
- intencja: świeżo zainstalowana apka, ktoś chce kolejności działań; albo przed instalacją: ile to
  roboty w pierwszym tygodniu.

**3. Co zostaje, co wypada, co dochodzi**

| Stary element | Decyzja | Co zrobić |
|---|---|---|
| Otwarcie („five tabs and one big button") | PRZEPISAĆ | Pięć zakładek nadal jest (Main, Timeline, Reflect, Workspace, Character), ale pierwszy widok to kafelki Main i szeroki kafel „Your first week". Rozpoznanie w stylu Moniki: apka zainstalowana we wtorek, sesja o szóstej, osiem kolorowych kafelków i plan, który pyta o odpowiedź na pytanie Orki. |
| H2 „What MindSync is for (and what it is not)" | ZOSTAJE | Dopisać Orkę jednym zdaniem w ramie §4.1. Usunąć „records sessions... transcript", zostawić „summaries". Fakt założyciela i psycholożki zostaje. Link `/audience` względny. |
| (brak) | DOCHODZI H2 „Why small steps between sessions matter:" | 120-180 słów: Kessels 2003 i Kazantzis 2010 (§2 pkt 2), z granicami. Bez twierdzenia, że „pierwszy tydzień decyduje". |
| H2 „Day one: the 10 minutes that set everything up" | PRZEBUDOWA | Nowy H2 „Day one: setup and your first talk with Orca". Lista: (1) setup: focus areas, siła 1-10 jako punkt startu, terapia, termin sesji, imię i styl Orki; (2) pierwsza rozmowa: trzy krótkie pytania, głos albo pisanie, około 3 minut, można pominąć; (3) ekran „What Orca heard" i lądowanie na Main z planem. „Ten minutes, and you haven't written a paragraph" zostaje jako puenta, jeśli pasuje. |
| H3 „Pick the two or three things you are actually working on" | ZOSTAJE | Fakty prawdziwe. Poprawić: zmiany później w kafelku Focus Areas na Main (dodaj, archiwizuj, usuń), nie „in settings", bez „renamed". |
| H3 „Do your first check-in" | PRZENIESIONE | Treść idzie do kroku 5 (Quick check-in) w nowej sekcji kroków. „One rating tells you nothing... the first dot" zostaje. |
| (brak) | DOCHODZI H3 „Your first talk with Orca" | W H2 „Day one". Rama §4.1 obowiązkowa (Orca jest tematem akapitu). Link do `is-it-safe-to-talk-to-ai-about-mental-health`. |
| (brak) | DOCHODZI H2 „The eight steps of Your first week:" | Fraza „first week" w H2. Lista numerowana 1:1 z apką (tabela niżej), krótko, cytowalnie. Pod listą zasady planu (bez dni, liczy się realne działanie w dowolnej kolejności, okienko „One step forward!", przypomnienie najwyżej raz dziennie, krok 8 od 7. dnia albo po krokach 1-7, plan znika po ośmiu albo po około czterech tygodniach, starsze konta go nie widzą) i jedno zdanie o wariancie bez terapii. Inline karta `first-week-plan`. |
| H2 „Your first session with the app" | ZOSTAJE (nowy nagłówek) | „Around your first session: before, during, after". Poprawić zdanie o przycisku: „+" na każdej zakładce oprócz Reflect, cztery opcje z nazwami z apki. Dodać kafel sesji (dzień przed: „Prepare your notes", po: „After therapy"). Bez numerów kroków. |
| H3 „Before: the prep card" | PRZEPISAĆ | „Before: the Before therapy card". Sekcje z §1.7. „Your first one will be thin" zostaje, ale teraz pierwsza karta startuje z pierwszej rozmowy z Orką, więc „thin, but not empty". Auto karta tylko zgodnie z NIEPEWNE nr 4. Zamienić `[LINK-LATER: how-to-prepare-for-a-therapy-session ...]` na zwykły link. |
| H3 „During: recording (and asking your therapist first)" | ZOSTAJE | Fakty prawdziwe (pytanie przed sesją, różne prawo w krajach i stanach, terapeuta może odmówić). Dopisać: apka przed pierwszym nagraniem prosi o potwierdzenie zgody terapeuty; sesje krótsze niż 10 minut nie są przetwarzane. **Usunąć „transcript"**: zostaje karta Session recording z podsumowaniem, pytaniami, które zadał terapeuta, to-do, wątkami i realizacjami. Inline karta `session-recording` zostaje (z nowym zdaniem). |
| H3 „After: the debrief while it is still fresh" | ZOSTAJE (nowa nazwa) | „After: the After therapy card while it's fresh". Dopisać „Your progress in therapy" po trzech sesjach z ramą YMYL i linkiem do `therapy-hangover` **[NA-PROGU]** („if you feel worse after a session"). Zamienić `[LINK-LATER: how-to-remember-what-you-talk-about-in-therapy ...]` na zwykły link. |
| H2 „The week between sessions" | ZOSTAJE | Intencja klastra 2. H3 niżej. |
| H3 „Voice notes when something comes up" | ZOSTAJE | „+" → Between Sessions, przegląd tekstu („Review your transcript" to ekran notatki głosowej, wolno), = krok 4 (bez numeru w tej sekcji, najwyżej „the voice note from your plan"). „Read back", nigdy „listen back" (lekcja z partii 4). |
| H3 „Homework that lands on your home screen" | PRZEPISAĆ | „To-dos and your agenda on Main": kafel To-do („From your therapist", „From Orca"), kafel Therapy Agenda (= krok 6), Workspace w stałej kolejności. Link `how-to-do-therapy-homework`. |
| Akapit o Reflect | PRZEPISAĆ | Reflect = rozmowy z Orką, tekst albo głos (głos w Premium po trialu), dawne rozmowy da się przeczytać. |
| (brak) | DOCHODZI zdanie albo krótki H3 „One small habit" | Krok 7 istnieje, więc wpis musi go nazwać. Zasada partii 6 „Habit Tracker poza katalogiem: zero zdań" przestaje działać z chwilą dodania `habits` do katalogu (§5). Bez katalogu: tylko nazwa kroku i kafla, bez opisu funkcji. |
| H2 „What you get after two weeks" | PRZEBUDOWA | „What shows up after a week or two:". Krok 8 „Your first week" (co jest w podsumowaniu, rytm na kolejne tygodnie), Focus Areas: ostatnie 14 ocen i trend słowami, Weekly summary w Timeline z „Generate now", filtry Timeline (bez układu), Character wypełnia się z tego, co piszesz (NIEPEWNE nr 2-3), wykres po trzech sesjach. **Akapit ostrożności zostaje prawie dosłownie** („Two weeks of ratings is a hint, not proof...") i link `why-mood-tracking-stops-working`. Poprawić: na Timeline nie ma check-inów Focus Areas. Ilustrację `app-ios-4.webp` (stara oś czasu) wymienić. |
| H2 „Getting the app" | ZOSTAJE (fakty nowe) | Sklepy jak było. Trial: 4 dni Premium po rejestracji, nic nie pobiera się automatycznie; potem Free z miesięcznymi limitami; rozmowa głosowa z Orką i bez limitów w Premium; szczegóły na `/membership`. Link do A („everything that changed in the latest update"). Usunąć „full access and does not ask for a card". Linki `/membership`, `/features`, `/faq` względne. |
| Ilustracja `app-ios-3.webp` (stara Prep Card) | WYPADA | Zastąpić `store_prep.png` albo `prep_card_v2.png` (decyzja operatora), alt: „The Before therapy card in MindSync with a summary and numbered questions to bring". |
| Ilustracja `app-ios-4.webp` (stara oś czasu) | WYPADA | Zastąpić `main_v3_week_plan.png` w sekcji kroków (alt „The Your first week plan in MindSync with eight small steps") albo `store_timeline.png` w sekcji „after a week or two". |
| `[FEATURES: What to set up in the first week ...]` | ZOSTAJE nagłówek, ZMIANA id | Patrz karty niżej. |
| Akapit o apce + pytanie do czytelnika | DOCHODZĄ | Stary wpis ich nie miał (sprzed głosu Moniki). Rytm §2.1 pkt 9 i jedno pytanie przed FAQ. |

**4. Struktura docelowa (kolejność)**
1. Otwarcie (bez H2, 60-120 słów).
2. H2 „What MindSync is for (and what it is not)".
3. H2 „Why small steps between sessions matter:" (badania).
4. H2 „Day one: setup and your first talk with Orca" → H3 „Pick the two or three things you are
   actually working on", H3 „Your first talk with Orca".
5. H2 **„The eight steps of Your first week:"** z listą (tytuły dokładnie jak w apce, meta w nawiasie):
   1. **Set up your account** (Setup · 3 min): already done by the time you see the plan.
   2. **Answer Orca's question** (Reflect · 3 min): one question about your first talk.
   3. **Add your next session** (Next therapy session · 1 min): already done if you gave a date in setup.
   4. **Leave a voice note** (Between Sessions · 1 min): say how your week is going.
   5. **Quick check-in** (Focus Areas · 30 sec): rate what you picked in setup.
   6. **Save one thing for therapy** (Therapy Agenda · 1 min): one question or topic for next time.
   7. **Keep a small habit** (Habits · 1 min): check one off, or add one.
   8. **Your first week** (Weekly recap · 2 min read): a short look back and a rhythm for the weeks ahead.
   - zdanie o wariancie: „If you're not in therapy right now, step 3 becomes Talk with Orca again
     and step 6 becomes Save a question for later." (+ NIEPEWNE nr 7 do decyzji BVM)
   - zasady planu jednym akapitem (patrz tabela wyżej), inline karta.
6. H2 „Around your first session: before, during, after" → H3 Before / During / After.
7. H2 „The week between sessions" → H3 voice notes / To-dos and your agenda on Main / (habit) /
   akapit Reflect.
8. H2 „What shows up after a week or two:".
9. H2 „Getting the app".
10. Akapit o apce: „This is what MindSync's first-week plan is for. Log the question you didn't get to,
    the voice note from the stairwell, the habit you kept on a bad day. Give it time, and Main and
    your After therapy cards turn those entries into something you can see: what's waiting today,
    and, after three sessions, a line of your own entries. Then walk into session two already past the
    recap." (szkic; ostatnia kropka obrazu może zostać z dawnego „Five minutes in the car beats 40
    minutes on Sunday")
11. Pytanie do czytelnika, np. „Which of the eight steps do you already know you'll put off, and what
    would make it a one-minute job?"
12. `[FEATURES:]`, potem FAQ.

**5. FAQ (5, wszystkie pytania ZOSTAJĄ dosłownie; odpowiedzi do przepisania tam, gdzie fakty się zmieniły)**
- H3: **What is MindSync used for?** → ZOSTAJE, odpowiedź poprawić: zamiast „record... get a transcript"
  „record sessions with your therapist's permission and get a summary card"; dodać Before/After
  therapy cards i Orkę („an AI therapy assistant for the days between sessions, not a therapist");
  „It supports therapy and does not replace it" zostaje.
- H3: **Is MindSync free?** → ZOSTAJE, odpowiedź **PRZEPISAĆ**: „You start with 4 days of Premium for
  free, and nothing is charged automatically. After that, the Free plan keeps a limited number of
  cards, notes and Reflect messages each month, plus a small number of session recordings; Premium
  removes the limits and adds voice talks with Orca. Current prices are on the membership page."
  (szkic, liczby celowo pominięte).
- H3: **Can I record my therapy session with MindSync?** → ZOSTAJE, dopisać potwierdzenie zgody
  w apce i minimum 10 minut; „If your therapist says no, the After therapy card captures most of the
  same material from your side." (nazwa zamiast „debrief").
- H3: **Does MindSync work without a therapist?** → ZOSTAJE, odpowiedź poprawić: Focus Areas, voice
  notes, Reflect z Orką, Habits i Character działają samodzielnie; plan pierwszego tygodnia zamienia
  dwa kroki, gdy nie jesteś w terapii; karty Before i After therapy oraz nagranie mają sens tylko
  przy sesjach.
- H3: **Do I have to journal every day for it to be useful?** → ZOSTAJE, odpowiedź poprawić:
  codzienny element to opcjonalny check-in w Focus Areas (30 sekund); kroki planu nie mają dni;
  w Habits można odhaczyć dzień, który przegapiłeś; brak dni niczego nie psuje.
- Bez nowego szóstego pytania (lista kroków w H2 jest cytowalna sama). Pytania o Orkę są w A.

**6. Karty funkcji**
- inline w H2 „The eight steps...":
  `[FEATURE: first-week-plan | The eight steps of your first week on Main, each one a few minutes, none of them tied to a day.]`
- inline w H3 „During..." (zostaje id, nowe zdanie):
  `[FEATURE: session-recording | With your therapist's okay, record the session and get a summary card with the questions they asked you.]`
- blok przed FAQ:
  `[FEATURES: What to set up in the first week || session-prep | A Before therapy card, so the first five minutes go to the thing that matters instead of a recap. || session-debrief | An After therapy card while the session is fresh, and a progress line once you have three sessions. || voice-notes | The thing you'd forget by Friday, said out loud on Tuesday and waiting in text.]`
- **Zastępcze, gdy `first-week-plan` nie trafi do katalogu:** inline `[FEATURE: check-ins | ...]` przy
  kroku 5 zamiast karty planu. ⚠ Karty `session-prep` i `session-debrief` pokazują dziś nazwy
  „Prep Card" i „After-therapy debrief" oraz stare zrzuty: bez korekty katalogu (§5) tekst i karta
  się rozjadą.

**7. Mapa linkowania** (wszystko na żywo, linki względne; stare absolutne `https://mindsync.app/...` zamienić na względne)
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` **[NA-PROGU]** anchor „how to prepare for
  a therapy session when your mind goes blank" (H3 Before; zastępuje `[LINK-LATER:]`).
- `<a href="/journal/how-to-remember-what-you-talk-about-in-therapy">` anchor „why you forget most of
  what your therapist says" (H3 After; zastępuje `[LINK-LATER:]`).
- `<a href="/journal/therapy-hangover">` **[NA-PROGU, poz. 10,6]** anchor „if you feel worse after a
  session" (H3 After).
- `<a href="/journal/what-to-do-between-therapy-sessions">` **[NA-PROGU, poz. 13,1]** anchor „a weekly
  system that fits real life" (H2 „The week between sessions").
- `<a href="/journal/journaling-vs-voice-notes">` anchor „why talking beats typing for most people"
  (H3 voice notes).
- `<a href="/journal/how-to-do-therapy-homework">` anchor „getting therapy homework done when the week
  eats it" (H3 To-dos).
- `<a href="/journal/why-mood-tracking-stops-working">` anchor „why mood tracking stops working after
  two weeks" (H2 „after a week or two").
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „what a progress line can and can't
  tell you" (H3 After albo akapit ostrożności).
- `<a href="/journal/is-it-safe-to-talk-to-ai-about-mental-health">` anchor „what happens to what you
  tell an AI" (H3 first talk).
- `<a href="/journal/whats-new-in-mindsync">` anchor „everything that changed in the latest update"
  (H2 „Getting the app" albo „What MindSync is for"). Zwykły link, bo A wychodzi pierwszy.
- `<a href="/audience">`, `<a href="/faq">` (anchor „how your data is stored and who can see it",
  zostaje), `<a href="/membership">`, `<a href="/features">`.

**8. GEO (szkice EN do humanizera)**
- **B1 „What is the MindSync first-week plan?":** „Your first week is a plan of eight small steps
  that new MindSync accounts see on Main. Each step takes a few minutes and has no set day. A step
  counts as soon as you do the thing it describes, a short screen marks your progress, and the plan
  leaves Main once all eight are done."
- **B2:** sama lista ośmiu kroków z H2 (ordered list, tytuły z apki) jest fragmentem do cytowania.

**9. Schema (dla `seo-tech-lead`)**
- Aktualizacja istniejącego grafu: `headline` bez zmian, nowy `description` (= zajawka), `dateModified`,
  FAQPage z nowymi odpowiedziami (pytania te same). Host wg konwencji z partii 3 (www); obecny graf ma
  `https://mindsync.app/...`, do ujednolicenia przy tej aktualizacji.

---

## 5. Katalog `blog/app-features.json`: propozycje (NIE edytowałem pliku)

### 5.1 Nowe pozycje (format istniejący; `screenshot` puste do czasu uploadu renderów)

```json
[
  {
    "id": "main-home",
    "name": "Main home screen",
    "short": "MindSync opens on Main: eight tiles for your next session, Therapy Agenda, to-dos, the last seven days of your habits, Focus Areas, therapy relationship, weekly observations and a daily affirmation. A blue dot means something is waiting.",
    "status": "live",
    "cta_url": "https://mindsync.app/features",
    "screenshot": "",
    "keywords": ["home screen", "main screen", "new home screen", "therapy week at a glance", "next therapy session", "what is waiting today", "mindsync update", "new features"]
  },
  {
    "id": "first-week-plan",
    "name": "Your first week plan",
    "short": "New accounts get a plan of eight small steps on Main, a few minutes each and with no set days, from answering Orca's question to adding your next session, a voice note, a quick check-in and a short look back at the week. A reminder is optional and comes at most once a day.",
    "status": "live",
    "cta_url": "https://mindsync.app/features",
    "screenshot": "",
    "keywords": ["first week", "getting started", "how to use mindsync", "first steps", "eight steps", "week plan", "new to the app", "onboarding plan"]
  },
  {
    "id": "first-conversation",
    "name": "First conversation with Orca",
    "short": "Right after sign-up, Orca, MindSync's AI therapy assistant for the days between sessions, asks three short questions by voice or in writing, then the conversation is yours. Orca isn't a therapist. Your first Before therapy card starts from what it heard.",
    "status": "live",
    "cta_url": "https://mindsync.app/features",
    "screenshot": "",
    "keywords": ["orca", "ai therapy assistant", "first conversation", "mindsync ai", "three questions", "voice conversation", "talk between sessions"]
  },
  {
    "id": "orca-memory",
    "name": "What Orca remembers",
    "short": "A page in Settings that lists every note Orca keeps from your conversations and entries, grouped by what's on your mind, what helps, goals, routines and people. Delete any note, or tap Forget everything.",
    "status": "live",
    "cta_url": "https://mindsync.app/features",
    "screenshot": "",
    "keywords": ["what orca remembers", "ai memory", "delete ai memory", "what does the app remember", "forget everything", "control what the ai knows", "ai privacy"]
  },
  {
    "id": "character",
    "name": "Character: strengths and skills",
    "short": "Six strengths (Courage, Insight, Honesty, Resilience, Kindness and Commitment) grow from moments in what you write and say, never from just opening the app. Your map shows the skills you're building under the feelings they help with. Tap Not quite on any moment that doesn't fit.",
    "status": "live",
    "cta_url": "https://mindsync.app/features",
    "screenshot": "",
    "keywords": ["strengths", "character strengths", "skills map", "coping skills", "emotional skills", "see your growth", "what you are learning about yourself", "not quite"]
  },
  {
    "id": "habits",
    "name": "Habits",
    "short": "Track small daily things you want to do, or want to stay free of. The Habits tile on Main shows the last seven days, so you can still check off a day you missed.",
    "status": "live",
    "cta_url": "https://mindsync.app/features",
    "screenshot": "",
    "keywords": ["habit tracker", "daily habits", "small habits", "good habit", "bad habit", "habits between sessions"]
  }
]
```

Uwagi do 5.1:
- Id Orki: zaproponowałem `first-conversation` (konkretna funkcja), a nie ogólne `orca`, bo rozmowy
  z Orką w Reflect ma już `reflect`. Jeśli operator woli jedno `orca`, to samo `short` + słowa
  z `reflect`.
- `character` ma status `live` pod warunkiem NIEPEWNE nr 2. Gdyby KE było wyłączone, `character`
  dostaje `beta` (karta krucha) i wpis A nie opisuje sześciu mocnych stron.
- `habits`: dochodzi, bo krok 7 planu i kafel Main go wymagają. W kafelku miesiąca każdego nawyku
  jest licznik „day streak" (`lib/screens/main_tab/mc/sheets/habits/mc_habits_month.dart:160`);
  świadomie bez słowa „streak" w keywords, żeby nie mieszać z `streaks` (planned).
- Kandydaci na `screenshot` (po uploadzie do CDN Webflow): `main-home` ← `store_main.png`,
  `first-week-plan` ← `main_v3_week_plan.png`, `first-conversation` ← `first_conversation_intro.png`,
  `orca-memory` ← `orca_memory.png`, `character` ← `store_character.png`, `habits` ← `main_v3_habits_sheet.png`.
- Wszystkie `short` to proza: przed wpisaniem do katalogu przez humanizer.

### 5.2 Korekty istniejących pozycji (rozjazd z nową apką; każda zmiana nazwy przerenderuje karty na wcześniejszych wpisach)
- `session-prep`: `name` „Prep Card" → **„Before therapy card"**; `short` → „Before each session, a
  one-page card with a short summary of what came up since last time, up to three numbered questions
  to bring, to-do ideas, threads, patterns and your Focus Areas." Uwaga: „Prep Card" pada w prozie co
  najmniej w `how-to-use-mindsync`, `how-to-afford-therapy`, `online-vs-in-person-therapy`,
  `starting-over-with-a-new-therapist` (grep w `blog/queue`): po zmianie nazwy osobna drobna
  poprawka tych wpisów.
- `session-debrief`: `name` „After-therapy debrief" → **„After therapy card"**; `short` → „Note what
  you took away right after a session. The card keeps the summary, questions, to-dos and
  realizations, and after three sessions it adds Your progress in therapy, a chart of your own
  entries, not a score."
- `session-recording`: `short` bez „transcript" → „Record a session with your therapist's permission
  and get a summary card with the questions your therapist asked, to-dos, threads and realizations."
- `reflect`: `short` → „Talk things through with Orca, MindSync's AI therapy assistant, in writing,
  or by voice on Premium. It asks the follow-up questions a blank journal never will, and past talks
  stay readable."
- `check-ins`: `name` „Wellbeing check-ins" → **„Focus Areas check-ins"**; `short` → „Rate what you're
  keeping an eye on (sleep, worry, anything you pick) from 1 to 10. It takes under a minute."
- `mood-trends`: `short` → „Focus Areas on Main chart your last 14 ratings for each area and describe
  the trend in plain words."
- `timeline`: `short` → „Every card, note, recording, realization and summary on one timeline with
  filters at the top, and a recycle bin for 24 hours." (bez „check-in": check-iny Focus Areas nie są
  na Timeline).
- `personal-bio`: `name` „Personal bio & companion" → **„Personal Bio"**; `short` bez „companion
  character that grows as you show up" (sprzeczne z nowym Character, w którym otwieranie apki nic nie
  daje, i z zakazem „companion"). Miejsce Bio w nowym Character: NIEPEWNE nr 9.
- `streaks` (planned): `short` usunąć „showing up is rewarded via the companion character instead"
  (nieprawda od 19.10). Status `planned` zostaje dla serii aplikacyjnych; seria per nawyk istnieje
  w Habits (wyżej).
- `smart-reminders`: „Thirteen notification types" do weryfikacji (NIEPEWNE nr 14).
- `screenshot` w `session-recording`, `session-prep`, `session-debrief`, `reflect`, `timeline`,
  `workspace`: stary interfejs (`app-ios-1..6.webp`, sierpień 2026). Podmienić po uploadzie renderów.

---

## 6. Lista tematów do bramki (format preflight; zapisać jako `blog/queue/_preflight-partia7.json`)

```json
{
  "_opis": "KROK 0 partii 7 bloga MindSync (2026-10-21): wpisy o nowej wersji aplikacji (App Store 2.0.56, Google Play 2.0.117). A = nowy wpis whats-new-in-mindsync, B = przepisanie opublikowanego how-to-use-mindsync (item 6a8dd78d9711593bac37a6f8). Keywordy EN to doslowne podciagi blobow funkcji live z OBECNEGO katalogu (id+name+short+keywords), plus slowa nowych pozycji z briefu par. 5.1, ktore zaczna trafiac po aktualizacji katalogu. Brief: blog/queue/_brief-partia7-nowa-wersja.md.",
  "_wynik_bramki": "Policzone recznie wg logiki skryptu, oczekiwane: 2x OK, 0 RYZYKO, 0 BRAK na obecnym katalogu. A: session-prep i workspace ('therapy agenda'), timeline ('therapy timeline'), session-prep ('session preparation'), session-debrief ('after therapy'), check-ins ('focus areas'), reflect ('ai journaling'), summaries ('weekly summary'), daily-affirmation ('daily affirmation'), health-check ('therapeutic alliance'), mood-trends, homework i daily-affirmation ('home screen' w polu short). B: session-prep ('prepare for therapy'), session-debrief ('after therapy'), session-recording ('session recording'), voice-notes ('voice note'), check-ins ('focus areas'), homework ('therapy homework'), timeline ('therapy timeline'), reflect ('ai journaling'), mood-trends i homework ('home screen'). Po aktualizacji katalogu dochodza: main-home, first-week-plan, first-conversation, orca-memory, character ('first week', 'strengths', 'what orca remembers', 'ai therapy assistant', 'how to use mindsync', 'orca'). Zadne slowo nie trafia w bloby planned: streaks ('character tab', 'companion', 'habit streak', 'journaling habit') i therapist-sharing ('between sessions data', 'consent', 'share with therapist'); dlatego brak golego 'character', 'companion', 'habit', 'between sessions' i 'consent'.",
  "A KLASTER1 [2026-10-23]: what's new in MindSync (new home screen, first-week plan, therapy cards, Character, Orca)": [
    "therapy agenda",
    "therapy timeline",
    "session preparation",
    "after therapy",
    "focus areas",
    "ai journaling",
    "weekly summary",
    "daily affirmation",
    "therapeutic alliance",
    "home screen",
    "first week",
    "strengths",
    "what orca remembers",
    "ai therapy assistant"
  ],
  "B KLASTER1 [aktualizacja po A]: how to use MindSync, your first week step by step": [
    "prepare for therapy",
    "after therapy",
    "session recording",
    "voice note",
    "focus areas",
    "therapy homework",
    "therapy timeline",
    "ai journaling",
    "home screen",
    "how to use mindsync",
    "first week",
    "orca"
  ]
}
```

---

## 7. Dane do pobrania w sesji głównej (subagent nie ma Ahrefs ani powłoki)

- **GSC:** zapytania strony `/journal/how-to-use-mindsync` (oba hosty) od 2026-08-25
  (`scripts/gsc/frazy-brief.py` albo `blog-partia-frazy.py` dla slugu); raport z 21.10 pokazuje je
  jako zanonimizowane, więc wynik zapewne będzie pusty, ale warto to potwierdzić. **URL Inspection**
  tej strony (zero wyświetleń od 1.10) i po aktualizacji prośba o ponowne zaindeksowanie; to samo
  dla A po publikacji.
- **Ahrefs Keywords Explorer** (US i global), jeśli plan na to pozwala (`store/listing.md` D10 mówi,
  że Keywords Explorer nie wchodzi w obecny plan): `mindsync`, `mindsync app`, `mindsync ai`,
  `mindsync update`, `mindsync new features`, `what's new in mindsync`, `how to use mindsync`,
  `mindsync review`, `mindsync orca`. Reguła: jeśli `mindsync update` ma wolumen, a `what's new in
  mindsync` zero, zamieniamy je miejscami w H2 i meta_description; H1 bez zmian.
- **Ahrefs Site Explorer → Organic keywords** dla `mindsync.app` z filtrem „mindsync": które strony
  rankują na brand + „how to/use/app" (kontrola kanibalizacji A i B ze stroną główną).
- **Potwierdzenia przed publikacją A:** `integration-devops` (flagi KE na Heroku, NIEPEWNE nr 2),
  operator (rollout Google Play 100%, wybór renderów, decyzja o nazwach w katalogu).

## 8. Kolejność i zależności

1. Katalog: nowe pozycje §5.1 i korekty §5.2 (operator, ewentualnie `backend-api` jako współwłaściciel
   katalogu), humanizer na `short`. Upload renderów i pola `screenshot`.
2. Bramka §6 (lider uruchamia skrypt).
3. A: `blog-write` → humanizer → `blog-voice-check.py` → BVM → schema → hero → status `gotowy`
   wyłącznie na polecenie operatora → publikacja po spełnieniu warunku rolloutu.
4. B: przepisanie po publikacji A (zwykły link do A) → te same bramki → aktualizacja itemu
   `6a8dd78d9711593bac37a6f8` za zgodą operatora → URL Inspection.
5. PATCH linków po A (§A.5) i drobne poprawki prozy na wpisach z „Prep Card" po zmianie nazwy w katalogu.
6. Dziennik partii w `blog/kalendarz-tresci.md`: wiersz „Partia 7 (nowa wersja apki)" do dopisania
   przez lidera po akcepcie briefów (nie edytowałem kalendarza).
