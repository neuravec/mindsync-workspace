---
name: project-instagram-automation-2026-10-01
description: "Pipeline automatyzacji Instagrama (partia + drip jak blog) zbudowany 2026-10-01; offline gotowy, czeka na nowe konto EN pod USA i token Meta"
metadata:
  node_type: memory
  type: project
  originSessionId: e89b2a85-4a26-4419-b062-982c6f52a5b6
  modified: 2026-10-01T17:06:30.191Z
---

Zbudowany 2026-10-01 system "partia + drip" dla Instagrama MindSync, wzorowany na blogu ([[project-blog-adaptacja-mindsync-2026-08-25]]). Źródło prawdy: `social/README.md`. Skille `/social-write` (tworzenie, STOP przed `gotowy`) i `/social-publish` (runbook); agenci `social-content-writer`, `instagram-publisher`.

Decyzje operatora: posty EN, NOWE konto pod rynek USA (obecne konto jest polskie), formaty karuzela/single/story (Reels etap 2), akcept jak blog (status `gotowy` tylko na wyraźne polecenie).

Technologia: oficjalne Instagram API with Instagram Login (graph.instagram.com, bez strony FB, rola Instagram Tester, bez App Review), szablony HTML + Playwright -> JPEG sRGB, hosting mediów Cloudinary (rekomendacja) albo Webflow assets, drip z Task Schedulera co godzinę 13:00-03:00 PL. Zero instagrapi/botów (ryzyko bana).

**Why:** cel operatora to zarządzanie social mediami z Claude Code tak jak blogiem; później kolejne sieci (Postiz self-hosted lub Zernio).

**How to apply:** stan na 2026-10-01: 28 testów zielonych, gate i dry-run działają na przykładach `_przyklad-*`; NIC nie poszło na żywo. Blokery: brak konta, tokenu w `scripts/social/.env`, wyboru hostingu. Skrypty PS (`register-drip-task.ps1`, `ig-drip.ps1`) nie zostały uruchomione, bo auto mode je zablokował; operator robi podgląd sam przed `-Apply`. Wersja API domyślnie v23.0, docs Meta pokazują nowszą, podbić przy podpięciu. Od 2025-12 IG liczy max 5 hashtagów.

Repo i zasady (2026-10-01, wieczór): `social/` to osobne repo gita podpięte do prywatnego `github.com/neuravec/mindsync-social` (gałąź main, pierwszy commit 55f6be8 wypchnięty 2026-10-01, 92 pliki, bez sekretów; cel: sesje Claude cloud). Zasady: `social/CLAUDE.md` (5 zasad dotarcia do USA z researchu: pierwsi widzowie ustawiają geografię konta, kraj założenia nie; zero polskich znajomych, godziny ET, dźwięk US, interakcje z fanami kont US, mały boost US). Plan: `social/TODO.md`. OTWARTE: przenosiny `scripts/social/`, skilli i agentów do repo social (cloud ich nie widzi) oraz decyzje operatora o auto-follow, auto-komentarzach i DM. Oficjalne API NIE ma follow ani komentowania cudzych postów; ma odpowiedzi pod własnymi postami i prywatną odpowiedź na komentarz (1 wiadomość, 7 dni). Zakaz botów z README §7 nadal obowiązuje, dopóki operator go nie zmieni.

Warianty wizualne (2026-10-01): A kolor+typografia, B zdjęcia hero bloga (hero mają tylko ~1376px, więc nie full-bleed), C "bold" z obrazami Nano Banana Pro (`gemini-3-pro-image`, aspectRatio 4:5/9:16 w API, ~$0.2/obraz; prompty w `scripts/image-gen/prompts-instagram/`, koncepcja `social/variant-c-koncepcja.md`). C wyraźnie najbardziej angażujący. PDF dla grafika: `python scripts/social/pdf-export.py` -> `social/preview/MindSync-Instagram-przyklady.pdf` (HTML przez file://, nie set_content). Gmail MCP nie nadaje się do załączników >~100 KB (base64 inline), operator dołącza ręcznie; update_draft odpina szkic od wątku.

Rozszerzenie 2026-10-01 (wieczór): posty o nowościach (feature-*, wariant D) i agresywne (aggro-*, wariant E) na PRAWDZIWYCH ekranach z Fluttera (`test/marketing_shots/`, tag marketing + `--run-skipped`, dart_test.yaml skip; MaterialIcons ładowane z pliku SDK, bo rootBundle nie działa; nie owijać ładowania fontów w tester.runAsync, psuje GetIt). Rolki: `reel-render.py` (ffmpeg, cicha ścieżka AAC, 5-90 s), publikacja REELS wymaga Cloudinary (Webflow nie przyjmuje wideo). Hook PostToolUse w `.claude/settings.local.json` -> `ui-change-detector.py` po git commit pyta o treść na IG; reguła też w CLAUDE.md. Pliki w test/marketing_shots NIE są zacommitowane (repo frontu, push dev = TestFlight). Dymki na ekranie Reflect są celowo puste (dekoracja), kadruj górne 70%. PDF A-E: 22 strony, 11.4 MB; szkic do Darka + CC operator czeka na ręczny załącznik.

2026-10-02: dostępy DZIAŁAJĄ (konto @mindsync.app, IG_USER_ID=17841470981161262 = user_id z /me, Darek podał błędne id; token do 2026-11-30; Cloudinary ping OK). Decyzje operatora: plan treści MIESZA warianty A-E (README §5a), a przy każdej aktualizacji apki osobny post/rolka D/E niezależnie od kadencji (§5b). Następny krok: pilot single przez /social-write, live tylko za zgodą.

2026-10-02: pierwsze 2 posty `gotowy` na 2026-10-02: pilot single "the other 167" 12:00 ET + karuzela E (Threads+Reflect) 13:00 ET (pliki z data 2026-10-06 w id, celowo). Weryfikacja w kodzie zlapala falszywy slajd: limit 5 watkow i kolejka USUNIETE z apki (CS-03), stringi w arb zostaly martwe, nie ufaj im. Glos Reflect = Premium (trial ma). Drip publikuje tylko po rejestracji przez operatora (register-drip-task.ps1 -Apply -Live); auto mode blokuje rejestracje agentowi.

2026-10-02: STYL OBRAZÓW IG ZMIENIONY (decyzja operatora): naturalny kadr dzienny, płaskie rozproszone światło, neutralne kolory, "phone camera", ubrania "no pattern or text", ZERO kartek/notatek w scenie (Nano Banana pisze czytelny tekst, test: "CALL MUM"). Źródło prawdy: scripts/image-gen/prompts-instagram/_styl-bazowy-wariant-c.md v2 (kopia w social/scripts/image-gen/prompts-instagram/), wzorzec c08c. Kinowy v1 (c01-c06) = archiwum. Operator ODRZUCIŁ taste-skill i przebudowę szablonów (bold2-cover zostaje nieużywany). Pilot dziś ma obraz c08c. Etykieta AI WDROŻONA 2026-10-02 za zgodą operatora (render: pigułka "AI-generated image" + XMP; ig-publish: is_ai_generated; tylko obrazy z social/assets/variant-c i blog/images, nie zrzuty apki). Zakres stylu v2: TYLKO zdjęcia z ludźmi w wariancie C; slajdy typograficzne i sceny bez ludzi bez zmian. Pułapka: escape \x00 w heredoc z Bash zamienia się w surowe bajty, pisz bytes([0xFF,...]).
