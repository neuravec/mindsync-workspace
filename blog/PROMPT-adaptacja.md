# Prompt: adaptacja systemu blogowego PLASMET → MindSync

Do wklejenia w sesji Claude Code w tym repo (albo po prostu: „wykonaj blog/PROMPT-adaptacja.md").

---

W tym repo jest kompletny, sprawdzony pipeline produkcji bloga przeniesiony z innego
mojego projektu (PLASMET, sklep z narzędziami budowlanymi na platformie Shoper).
Twoje zadanie: przerobić warstwę KONTEKSTU z budowlano-sklepowej na MindSync,
zachowując architekturę procesu w całości.

## Krok 1. Wczytaj się, zanim cokolwiek zmienisz

1. `blog/README.md` – przeczytaj W CAŁOŚCI, to źródło prawdy o systemie (pipeline,
   mapa plików, checklist adaptacji w §5, zasady twarde w §6).
2. `blog/queue/_format.md` – format wpisu w kolejce.
3. `docs/blog-plasmet-reference/zespol-agentow.md` – jak agenci współpracują.
4. Kontekst MindSync: główny `CLAUDE.md` repo, `Business_requirements/`, `docs/`,
   oraz struktura strony na Webflow (jest podpięty MCP Webflow – obejrzyj site,
   kolekcje CMS i style, zanim coś zaprojektujesz).

## Krok 2. Dopytaj mnie, zanim zaczniesz pisać

Nie wymyślaj faktów o MindSync. Zadaj mi na start pytania o wszystko, czego nie da
się pewnie wyczytać z repo/Webflow, co najmniej o:

- Kto jest odbiorcą bloga (użytkownik apki? terapeuci? oba segmenty?) i jaki cel
  biznesowy ma blog (rejestracje, pobrania, leady B2B do gabinetów?).
- Język bloga: polski, angielski czy oba.
- Gdzie blog fizycznie żyje: która kolekcja CMS w Webflow, jaka domena/ścieżka URL.
- Brandbook: kolory, typografia, styl ilustracji hero (albo skąd mam je wziąć).
- Jakie CTA zastępują kafelki produktowe (funkcja apki, ekran, plan cenowy, App Store/Google Play?).
- Czy strona MindSync ma już właściwość w Google Search Console i na jakim koncie.
- Ton głosu marki: 2-3 przykłady tekstów, które brzmią „po naszemu".

## Krok 3. Zakres przeróbek (po akceptacji odpowiedzi)

Pracuj etapami wg checklisty w `blog/README.md` §5; po każdym etapie krótki raport
i dopiero potem następny. Do przerobienia:

1. **Agenci** (`.claude/agents/`): `blog-writer`, `seo-content-writer`,
   `brand-voice-manager`, `seo-tech-lead`, `graphic-designer` – wymień branżę,
   odbiorcę, przykłady, terminologię i odwołania do Shoper/PLASMET na MindSync/Webflow.
   `general-web-search-agent` zostaw prawie bez zmian.
2. **Skill `blog-publish`**: przepisz kroki publikacji z webapi Shoper (`news`) na
   Webflow CMS (MCP Webflow albo Data API v2), z zachowaniem wzorców z oryginału:
   DryRun domyślnie, idempotencja po slugu, retry/backoff, log dripu.
3. **Bramka pokrycia** (`scripts/blog-asortyment-preflight.py`): z „czy sklep ma
   produkt" na „czy MindSync ma funkcję/ekran/plan, do którego wpis prowadzi".
   Źródłem niech będzie plik z katalogiem funkcji apki – załóż go i wypełnij ze mną.
4. **Kafelki**: wzorzec HTML kafelka produktowego z przykładowych wpisów przerób na
   kartę CTA MindSync (screenshot/ikona funkcji + przycisk). Odpowiednik
   `product-cards.ps1` napisz pod nowe źródło danych.
5. **Prompty hero** (`scripts/image-gen/prompts-kategorie/`): nowa biblioteka promptów
   pod styl wizualny MindSync; mechanika (gemini-generate → png-to-webp) bez zmian.
6. **Format kolejki** (`blog/queue/_format.md`): usuń pola i sekcje specyficzne dla
   Shoper, dodaj pola pod Webflow; zaktualizuj `_przyklad.json`.
7. **GSC**: popraw `scripts/gsc/gsc.config.json` na właściwość MindSync i przetestuj
   `pull_gsc.py` (jeśli plików z poświadczeniami brakuje, przypomnij mi o komendzie
   z `blog/README.md` §4).
8. **Porządek na końcu**: przenieś przykłady PLASMET (wpisy 22/81, published-log,
   kalendarz, obrazy) do `docs/blog-plasmet-reference/przyklady/`, wyzeruj
   `published-log.json` i `kalendarz-tresci.md`, zaktualizuj `blog/README.md` tak,
   żeby opisywał stan MindSync, oraz sekcję blogową w `CLAUDE.md`.

## Czego NIE zmieniać (zasady twarde z §6 README)

- Podział ról agentów i przepływ przekazań między nimi.
- Humanizer jako bramka twarda przed każdą publikacją prozy, także po poprawkach.
- Całkowity zakaz em-dash „—" w generowanym tekście.
- Najpierw bramka pokrycia na LIŚCIE tematów, potem pisanie; wpis nigdy w ślepy zaułek.
- Publikatory z DryRun domyślnie TRUE; na żywo tylko jawnym przełącznikiem.
- Kolejka plikowa ze statusami jako jedyne źródło prawdy o publikacjach.
- Tematy i frazy z danych (GSC), dyrektywy frazowe nadrzędne nad kreatywnością.

Niczego nie publikuj na żywym Webflow bez mojej wyraźnej zgody; do tego momentu
wszystko w trybie projekt + DryRun.
