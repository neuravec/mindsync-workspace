---
name: feedback-myslniki-total-ban-i-humanizer-fork
description: "Od 2026-09-17 zakaz obejmuje TAKZE polpauze (U+2013), nie tylko em-dash; humanizer to lokalny fork 2.13.0-mindsync.1 z 44 wzorcami"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e8b2f500-73a1-4057-a03a-e7863aaaca6a
  modified: 2026-09-17T05:26:24.692Z
---

**Zakaz myslnikow obejmuje OBA znaki, nie tylko em-dash.** Do 2026-09-17 globalne `CLAUDE.md` kazalo zastepowac em-dash (U+2014) polpauza (U+2013) ze spacjami. To bylo sprzeczne z sekcja 14 lokalnego skilla `humanizer`, ktora od 2026-07-07 zakazywala rowniez polpauzy uzytej jako wtracenie lub pauza. Operator rozstrzygnal spor na korzysc skilla, wiec `CLAUDE.md` zostal przepisany.

**Why:** podmiana em-dasha na polpauze nie usuwa sygnalu AI, tylko zamienia jeden na drugi. Stary zapis wrecz zalecal mechaniczny `find&replace "—" → "–"`, czyli instruowal, jak obejsc wlasna regule. Dwa zrodla prawdy mowiace co innego dawaly niespojny output zaleznie od tego, ktore akurat zadzialalo.

**How to apply:** dozwolony jest **wylacznie zwykly lacznik (U+002D)**, w wyrazach zlozonych i zakresach liczbowych bez spacji (`7-10 m2`, `strony 20-30`). Wtracenie przepisz na przecinki lub nawias, definicje po myslniku na dwukropek, dluga pauze na kropke i dwa zdania. **Nigdy nie podmieniaj znaku na inny znak** – przepisz zdanie. Przed oddaniem dowolnego tekstu przeszukaj go pod katem U+2014 i U+2013; trafienie znaczy, ze tekst nie jest gotowy. Dotyczy to takze odpowiedzi w czacie, nie tylko plikow.

## Humanizer to lokalny fork, nie czysty upstream
`Heroku/.claude/skills/humanizer/SKILL.md` = **`2.13.0-mindsync.1`**, 44 wzorce, 733 linie. Backup poprzedniej wersji: `SKILL.md.bak-2.6.0`. Upstream: [jooray/humanizer](https://github.com/jooray/humanizer).

Trzy roznice wobec upstreamu, do powtorzenia przy kazdym podbiciu wersji (sa opisane w komentarzu HTML na gorze pliku):
1. Upstreamowa sekcja 15 (em dash jako "overuse") **zastapiona lokalna regula TOTAL BAN** z 2.6.0. Tresc bit w bit ta sama, zmieniony tylko numer z 14 na 15, bo upstream dolozyl wczesniej wzorzec "Staccato Contrast".
2. **Wycieta sekcja `SLOVAK AND CZECH TEXT`** (wzorce 45-54) i 6 odwolan krzyzowych do niej (§45, §47, §48, §49 x2, §46 w "Process and Output"). Zostaje ciagla numeracja 1-44.
3. **Przywrocony rozdzial `Full Example`**, ktory upstream wyrzucil, a ktory byl w 2.6.0.

Co przyszlo nowego z 2.7-2.13 (28 wzorcow): warstwa sladow rozumowania modelu, ktorej nie ma w artykule Wikipedii – `Reasoning-Chain Artifacts`, `Argument Residue`, `Forensic Residue`, `Performed Rigor and Candor`, `False Agency`, `Diff-Anchored Writing`, `The Treadmill Effect`, `Structural Uniformity`, `Connective Tissue Pile-Up` – plus warstwa retoryczna: `Manufactured Punchlines`, `Aphorism Formulas`, `Colon-Reveal Constructions`, `Conversational Rhetorical Openers`, `Staccato Contrast (wzorzec "Not X")`, `Hedged-Enumeration Openers`. Doszly tez tryby `Invocation Modes` i `Detect Mode` oraz rozdzial `DETECTION GUIDANCE`.

**Drobiazg do ewentualnej poprawki:** naglowek sekcji 15 nadal zawiera em-dash (`### 15. Em Dash — TOTAL BAN`), czyli sekcja zakazujaca znaku sama go uzywa. Zostawione bez zmian na wyrazne zyczenie operatora.

## Bramki automatyczne NIE egzekwuja tej reguly w calosci (ustalone 2026-09-21)
`scripts/blog-queue-gate.py` (bloker "DLUGI MYSLNIK U+2014") oraz bramka nr 2 w
`scripts/webflow/blog-publish.ps1` (`$EMDASH = [char]0x2014`) sprawdzaja **wylacznie em-dash**.
Polpauza U+2013 przechodzi przez obie bez sladu, wiec zielona bramka kolejki NIE jest dowodem,
ze tekst spelnia regule. Do czasu poprawki obu skryptow sprawdzaj oba znaki recznie przed kazda
publikacja. Wzorzec, ktory sie sprawdzil: `raw.count(chr(0x2014))` i `raw.count(chr(0x2013))`
na calym pliku JSON, nie tylko na `tresc_html`.

## Deklaracja przejscia humanizera to nie dowod (partia 3, 3 z 3 przypadkow)
`brand-voice-manager` po redakcji dwa razy uznal bramke humanizera za spelniona swoimi recznymi
poprawkami ("traktuje bramke za spelniona i biore to na siebie"). Wymuszony przebieg weryfikacyjny
znalazl realne rzeczy we **wszystkich trzech** wpisach: metronom kontrastowy "X rather than Y"
(7 wystapien po redakcji), konstrukcje bezpodmiotowe, falszywa sprawczosc (§39), tautologie (§44).
Zasada z `blog/README.md` §6 "takze po poprawkach" jest wiazaca takze wtedy, gdy poprawki byly
reczne. Nie przyjmuj zwolnienia z bramki od agenta, ktory sam ja obchodzi.

Powiazane: [[project-blog-adaptacja-mindsync-2026-08-25]], [[project-blog-partia3-2026-09-21]], [[project-blog-partia2-i-audyt-2026-09-03]]
