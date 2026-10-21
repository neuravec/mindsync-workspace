---
name: project-blog-partia3-2026-09-21
description: "Partia 3 bloga (3 wpisy, drip 21-23.09); therapy-hangover OPUBLIKOWANY; schema przeszla na host www; png-to-webp.py NIE dla hero bloga"
metadata:
  node_type: memory
  type: project
  originSessionId: fe163dde-e669-4286-9cb7-5ff213534e9c
  modified: 2026-09-21T06:36:13.713Z
---

**Partia 3 bloga MindSync, 3 wpisy, po pustej kolejce i 3 dniach przestoju dripu (19-21.09).**
Bramka pokrycia KROK 0: 6 kandydatow, 6x OK. Zrealizowane 3, pozostale 3 zostaja w
`blog/queue/_preflight-partia3.json` jako gotowy material na partie 4 (morning anxiety,
restart check-in habit, the same argument).

| wpis | data | stan |
|---|---|---|
| `therapy-hangover` | 21.09 | **OPUBLIKOWANY** na zywo, item `6ab0cf0fe7c4bc869f50bdc9`, zweryfikowany (200, karty, schema, 0 myslnikow) |
| `how-long-therapy-takes-to-work` | 22.09 | `gotowy`, komplet, czeka na drip 07:00 |
| `how-to-name-what-you-feel` | 23.09 | `gotowy`, komplet, czeka na drip 07:00 |

## Schema przeszla na host `www` (zmiana wzgledem calego starszego korpusu)
Od wpisu `therapy-hangover` wszystkie `@id`, `url` i `mainEntityOfPage`, **lacznie z `@id`
Organization**, uzywaja `https://www.mindsync.app/...`. Powod zweryfikowany na zywo: goly host
zwraca **301 na www**, a strona glowna deklaruje Organization pod `@id` z `www`, wiec 18 starszych
wpisow z golym hostem produkowalo **druga, osobna encje Organization** zamiast podpinac wpis pod
wlasciwa. Starsze wpisy warto wyrownac przy zbiorczym fixupie.

**Konsekwencja pomiarowa:** GSC raportuje `/journal/*` pod OBOMA hostami naraz (starsze wpisy
goly host, nowsze `www`). Regex pomiaru ruchu bloga musi lapac oba warianty, inaczej zaniza blog.

## `png-to-webp.py` NIE obsluguje hero bloga (pulapka)
Ma **zaszyta na sztywno** sciezke `szablon/design-claude/strona-glowna-2026-06/banery`, konwertuje
wszystkie PNG z tamtego katalogu i **kasuje zrodla**. Uruchomiony przypadkiem dla bloga zrobi szkode
w banerach. Cala konwersja i oba kadry hero robi ImageMagick wewnatrz `gemini-generate.ps1`.
Wzmianka o tym skrypcie w brand doc §4 jest mylaca.

**Wywolanie generatora:** `-DryRun:$false` NIE dziala przez `powershell -File` (argument leci jako
string, `Cannot convert value "System.String" to type "System.Boolean"`). Wolaj skrypt operatorem `&`
w biezacej sesji PowerShell. Miniatura 800x600 tnie sie `-gravity East`, czyli zostaje **prawe 75%**,
wiec nic istotnego nie moze siedziec w lewej cwiartce kadru.

## Lekcja o promptach do generatora obrazow
Hero wpisu 02 wyszedl jako wykres **trzy razy z rzedu**, w tym raz na `gemini-3-pro-image`. Przyczyna
nie byla w modelu: prompt w czesci pozytywnej zamawial "one thin hairline arc tracing underneath the
slope" i "a single small coral glow at the point where the rise begins to ease", czyli doslownie linie
z markerem danych, przy jednoczesnej dlugiej liscie zakazow ("no data points, no dots connected by a
line"). **Model rozstrzyga sprzecznosc na korzysc instrukcji pozytywnej.** Lista zakazow nie uniewazni
tego, o co prompt prosi wprost. Po usunieciu obu elementow z czesci pozytywnej pierwszy render byl OK.

## OTWARTE: kolizja FAQ `How many therapy sessions do I need?`
To pytanie istnieje teraz w dwoch wpisach z roznymi liczbami naglowkowymi: opublikowany
`/journal/is-therapy-worth-the-money` (13-18 sesji, Hansen 2002) i nowy wpis 02 (4-26, Robinson 2020).
Nie jest to sprzecznosc merytoryczna, ale oba ida do FAQPage pod tym samym stringiem, wiec silnik
odpowiedzi cytuje losowa wartosc. Rekomendacja `seo-tech-lead`: przestawic FAQ w **starszym** wpisie
na rame kosztowa (`How many sessions should I budget for?`) w `tresc_html` **i** `schema_jsonld`
jednoczesnie, plus republikacja. Koszt dzis zerowy (GSC: 0 wyswietlen na tej frazie w calej
wlasciwosci), za kilka miesiecy juz nie. **Czeka na decyzje operatora.**

Uwaga: rich resulty FAQ sa wygaszone od 09.2023, dokumentacja usunieta 06.2026, wiec ta kolizja nie
daje dzis widocznego problemu w SERP-ach. Realnym konsumentem markupu sa silniki odpowiedzi (GEO).

## Follow-upy poza zakresem partii
1. `blog/app-features.json` nie zna **Habit Trackera** (dziala od 02.09) ani ekranu wyboru trybu w
   Reflect (18.09). Bramka pokrycia zwroci dla nich BRAK, wiec zaden temat o nawykach nie moze
   oprzec na nich karty CTA. Do uzupelnienia przed briefami partii 4.
2. Katalog nazywa `session-debrief` "After-therapy debrief", wpisy pisza "after-session debrief".
3. `docs/blog/brand-mindsync.md` §5 opisuje konwencje liczebnikow, ktorej blog realnie nie stosuje.
   Realna konwencja jest lepsza: cyfry dla danych z badan, slowa dla potocznych czasow trwania.
4. `blog/queue/_link-fixup.md` ma **10 nieodrobionych pozycji** z partii 1 i 2, wymagalnych od 13.09.
   Partia 3 nie dolozyla dlugu (wszystkie linki wsteczne).

Powiazane: [[feedback-myslniki-total-ban-i-humanizer-fork]], [[project-blog-partia2-i-audyt-2026-09-03]],
[[project-blog-indexing-baseline-2026-09-15]], [[project-blog-adaptacja-mindsync-2026-08-25]]
