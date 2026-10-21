# Rejestr fixupów linków (LINK-LATER zdegradowane do samego anchora)

> Wpisy opublikowane zanim ich cele wyszły mają w treści sam tekst anchora bez linku.
> Po opublikowaniu celu trzeba dopiąć `<a href>` PATCH-em itemu (webflow-publisher).
> Log degradacji na bieżąco: `scripts/webflow/_drip-log.txt` (wiersze „LINK-LATER pominiety").

## Partia 1 – DO ZROBIENIA (cele już opublikowane, fixup wymagalny od 2026-09-03)

Potwierdzone 2026-09-03 na żywym HTML-u: te linki faktycznie NIE istnieją na stronie.
Wszystkie 5 celów jest już opublikowanych, więc fixup można zrobić od razu, jedną edycją per wpis.

| wpis (item) | anchor bez linku | cel (slug) | stan celu |
|---|---|---|---|
| how-to-use-mindsync (6a8dd78d9711593bac37a6f8) | „build a simple prep habit" (brzmienie sprawdź w body) | how-to-prepare-for-a-therapy-session | opublikowany 2026-08-26 |
| how-to-use-mindsync (6a8dd78d…) | anchor do remember-what-you-talk-about | how-to-remember-what-you-talk-about-in-therapy | opublikowany 2026-08-27 |
| regulate-nervous-system… (69c039b1bf339e69ca1e9d49) | „walking into the session with something to say" | how-to-prepare-for-a-therapy-session | opublikowany 2026-08-26 |
| regulate-nervous-system… (69c039b1…) | „keeping what the session gave you" | how-to-remember-what-you-talk-about-in-therapy | opublikowany 2026-08-27 |
| regulate-nervous-system… (69c039b1…) | „the rest of the week between sessions" | what-to-do-between-therapy-sessions | opublikowany 2026-09-01 |

⚠ Weryfikacja z 2026-09-03: `how-to-use-mindsync` ma **zero** linków do innych wpisów `/journal/`,
mimo że plan zakładał dwa. To najgorszy przypadek w partii 1 i jednocześnie wpis wejściowy
(„jak używać apki"), więc ma największy sens do naprawy w pierwszej kolejności.

## Partia 2 – DO ZROBIENIA PO 2026-09-13 (drip jeszcze trwa)

Zbiorczy fixup zaplanuj **po 2026-09-13**, gdy wyjdzie ostatni wpis partii.
Poniższe wynikają z kolejności dripu i są nieuniknione: wpis linkuje do siostry,
która wychodzi później. Anchory są dosłowne, wzięte z pól `tresc_html` w kolejce.

| wpis (slug) | anchor bez linku | cel (slug) | cel wychodzi |
|---|---|---|---|
| how-to-choose-a-therapist | „what to do when the fit turns out to be wrong" | what-to-do-when-your-therapist-is-not-the-right-fit | 2026-09-05 |
| how-to-choose-a-therapist | „what therapy costs, and how to judge what you get for it" | is-therapy-worth-the-money | 2026-09-06 |
| what-to-do-when-your-therapist-is-not-the-right-fit | „what you are paying for, and how to judge it" | is-therapy-worth-the-money | 2026-09-06 |
| journaling-vs-voice-notes | „when the loop shows up at one in the morning" | racing-thoughts-at-night | 2026-09-09 |
| racing-thoughts-at-night | „the Sunday night version of the same thing" | sunday-scaries | 2026-09-10 |

Wpisy publikowane przez drip PO wyjściu celu dostają pełny link automatycznie
(publikator sprawdza status w kolejce) – ich tu nie ma. W partii 2 jest to 14 z 19
linków wewnątrzpartyjnych, bo kolejność dat ustawiono tak, żeby huby wychodziły pierwsze.

## Dlaczego ten rejestr w ogóle istnieje

`[LINK-LATER:]` chroni przed 404: publikator degraduje link do samego anchora, gdy cel
jeszcze nie istnieje. Cena jest taka, że **nikt tego nie odrabia automatycznie** i wpis
zostaje z tekstem, który miał być linkiem. Partia 1 przeleżała tak od 25.08 do 03.09.
Jeśli ma to przestać wracać, docelowo publikator powinien po każdej publikacji sprawdzać
ten rejestr i domykać linki PATCH-em. Do tego czasu: pozycja w kalendarzu po zamknięciu
każdej partii.
