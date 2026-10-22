# Werdykt brand-voice-manager: maile P1-P9 (21.10.2026)

Zakres: 14 plików `copy/*.json` (wersja 2 po decyzjach leada). Sprawdzone względem `SPEC.md` §1-8,
`copy/_review.md`, `docs/blog/brand-mindsync.md` (§2.5, zakazy, §5) i maila z 21.10
(`email/2026-10-23-new-look/email.lmx`). Fakty o planach wyrywkowo potwierdzone w
`mindsync-frontend/mindsync_app/lib/l10n/app_en.arb` (wiersze 821, 1645, 1657, 1673-1696, 1767, 1769):
tabela Premium/Free w P3a zgadza się słowo w słowo, "Nothing is charged automatically" i "stays saved"
też.

Poprawki zrobione w plikach, schemat i adresy linków akcji bez zmian (zmieniłem tylko etykiety przycisków
i teksty). Kontrola mechaniczna po poprawkach: 0 x U+2014, 0 x U+2013 w całym `copy/`.

## Werdykty

| Mail | Werdykt | Powód |
|---|---|---|
| P1 | APPROVED AFTER FIXES | "they decide a lot of what we build" na "they shape a lot of what we build" (bez przesadnej obietnicy). Reszta: ciepłe otwarcie, Orca jasno "isn't a therapist", fallback `there` jest. |
| P2a | APPROVED AFTER FIXES | "We'll check in once more in a few days, then leave you be." było nieprawdą: 12 h później ta sama osoba dostaje P3a, potem P3b. Teraz "MindSync will be here when you are." |
| P2b | APPROVED AFTER FIXES | "Write as much or as little as you like" było nieprawdą na Free (Reflect 15 wiadomości miesięcznie). Teraz "A few lines are enough, and you can stop whenever you want." |
| P3a | APPROVED AFTER FIXES | "Most people find it easier" (niesprawdzalne twierdzenie) na "On a tired evening, that can be a lot easier than typing." Krok "Today: one voice Reflect, about five minutes" przepisany, bo "five minutes" było już w P1, P2a i P3b-quiet. Uwaga do harmonogramu niżej (pkt 1). |
| P3b | APPROVED AFTER FIXES | Etykiety kafelków zmienione na neutralne liczbowo i bez oceniania: "Reflect conversations", "Therapy Agenda topics", "active days" (wcześniej "1 days you showed up" przy fallbacku i ton frekwencji). Prawda o pieniądzach bez zarzutu. |
| P3b-quiet | APPROVED AFTER FIXES | Otwarcie "Starting is usually the hardest part, so here's the smallest version" powtarzało P2a słowo w słowo dwa dni później. Nowe: "Maybe the timing just hasn't worked out this week. That happens." Preview nie dubluje już H1. Niezgrabne "voice mode is part of Premium until tomorrow" na "included in your trial until it ends tomorrow". |
| P4a | APPROVED AFTER FIXES | Rada "Reflect right after each session" kłóciła się z P2b i P6b (po sesji służy karta After therapy). Teraz "Open your After therapy card right after each session". Nazwa wykresu ujednolicona: "Your progress in therapy" (jak P6b i mail 21.10). |
| P4b | APPROVED AFTER FIXES | Tylko interpunkcja (comma splice w zdaniu o grumpy answers). |
| P5 | APPROVED AFTER FIXES | (a) "Finished therapy? That's genuinely good news." zakładało, że koniec terapii jest zawsze dobry (bywa przez koszt, ubezpieczenie, odejście terapeuty). Teraz "If it's because things got better, we're genuinely glad." (b) "pick a plan again ... under Subscription" przy wciąż aktywnym Premium było mylące; teraz włączenie auto-renew w ustawieniach App Store / Google Play. (c) Dodane, co się stanie po końcu okresu (Free, dane zostają). (d) Preview "then we'll leave you be" usunięty (obietnica, której workflowy P6/P9 nie gwarantują). (e) Przycisk "I WASN'T USING IT ENOUGH" na "I DIDN'T USE IT MUCH" (bez wydźwięku winy), `a=not_using` bez zmian. |
| P5-expired | APPROVED AFTER FIXES | Te same poprawki co P5 (a, d, e). Dodane zdanie na wygaśnięcie niezamierzone (nieudana płatność): sprawdź subskrypcję w sklepie albo odpisz. Bez tego mail pytałby "why?" kogoś, kto niczego nie zdecydował. Uwaga do workflow niżej (pkt 3). |
| P6a | APPROVED AFTER FIXES | Preview powtarzał pigułkę "Coming back takes about five minutes". Teraz "Three small steps, if you'd like to pick things back up." Ton bez winy, link pauzy jest. |
| P6b | APPROVED AFTER FIXES | "you'll only get the occasional newsletter" pomijało maile o dużych aktualizacjach (P8). Teraz "a newsletter or a big app update". |
| P7 (szablon) | APPROVED | Struktura, nadawca Monika, placeholdery i `template_notes` w porządku. Każde wypełnione wydanie przechodzi osobny akcept BVM (głos Moniki, humanizer, źródła z rokiem). |
| P9 | APPROVED | Uczciwy, bez presji, jasne skutki braku odpowiedzi, konto zostaje. Uwaga techniczna niżej (pkt 2) jest po stronie backendu, nie treści. |

Żaden mail nie jest BLOCKED: po poprawkach nic nie jest nieprawdą ani niebezpieczne przy wysyłce.
Wszystkie 14 mają linię kryzysową z 988 i findahelpline.com, bez diagnozowania, bez obietnic leczenia,
bez fałszywej pilności.

## Sekwencja nowej osoby (P1, P2a, P3a, P3b/P3b-quiet, P2b)

Po poprawkach nie ma już powtórzonych zdań między mailami. "Five minutes" zostaje tylko w P1 i P2a
(dzień 0 i 1), "Hit reply" występuje w każdym mailu, ale to stały, osobisty kanał Darka (jak w mailu 21.10),
a nie powielona fraza. Nowe zdania po poprawkach są krótkie i proste; humanizer warto puścić na nie
jeszcze raz przy budowie w Loops (zmiany są drobne, wzorców AI-slop nie dodałem).

## Do leada / backendu (nie treść, ale wpływa na prawdziwość)

1. **P3a o 36 h to nie "halfway".** 36 h z 96 h to ok. 37%, a P2a idzie o 24 h, więc P2a i P3a dzielą tylko
   12 h. Rekomendacja: timer P3a na 48 h po `trialStarted`. Wtedy temat "You're halfway through your Premium
   trial" jest dosłownie prawdą i maile idą równo co 24 h (P2a d1, P3a d2, P3b d3). Jeśli `trialStarted`
   przychodzi też z innych źródeł trialu o innej długości, P3a trzeba ograniczyć do `signup_trial`.
2. **P9 `a=updates` musi też ustawiać `repermission_answer`** (np. `updates`). SPEC §2 wygasza kontakt, gdy
   `repermission_answer IS NULL` po 14 dniach. Jeśli przycisk "ONLY BIG APP UPDATES, PLEASE" zmienia tylko
   `emailPref`, osoba, która właśnie poprosiła o aktualizacje, zostanie wypisana. To byłoby sprzeczne z
   treścią maila.
3. **P5 i P5-expired dla tej samej osoby.** Kto wyłączy auto-renew (P5), a potem Premium wygaśnie
   (P5-expired), dostanie dwa razy tę samą ankietę. Rekomendacja: P5-expired tylko gdy w tym cyklu nie
   poszło P5 (filtr w workflow albo w `email_lifecycle_log`).
4. P3b: kafelek z zerem ("0 Therapy Agenda topics") wyjdzie, gdy ktoś miał tylko Reflect. Etykiety są teraz
   neutralne, więc to akceptowalne; lepiej byłoby nie wysyłać kafelka z 0, jeśli backend może rozróżnić.
