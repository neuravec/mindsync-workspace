# Research: Czy Claude Design pozwoli zrobić animacje dla MindSync (maskotka orka + gamifikacja)

*2026-07-04 · agent badawczy (Sonnet + web search), zlecony przez Mikołaja*

## 1. Czym jest "Claude design" — stan na lipiec 2026

Pod tą nazwą kryje się kilka odrębnych, ale powiązanych produktów Anthropic:

**Claude Design (Anthropic Labs)** — właściwy produkt "Claude design". Uruchomiony 17 kwietnia 2026, oparty na Claude Opus 4.7, dostępny w ramach subskrypcji Pro/Max/Team/Enterprise (research preview). To narzędzie do tworzenia wizualnych materiałów przez konwersację: prototypów, landing page'y, prezentacji, one-pagerów, materiałów marketingowych. Powstał we współpracy z Canvą — output można eksportować jako edytowalny plik Canva, PDF, PPTX lub samodzielny HTML. W czerwcu 2026 dodano `/design-sync` — dwukierunkową synchronizację z Claude Code (import design systemu z repo → generowanie ekranów w realnych tokenach/komponentach; oraz push zaimplementowanego kodu z powrotem na canvas).

Kluczowe fakty:
- **To narzędzie web-first.** Wszystkie przykłady w oficjalnym ogłoszeniu to strony/prototypy HTML+CSS+JS, prezentacje, dokumenty. Brak natywnego wsparcia mobile/Flutter.
- "Frontier design capabilities" (voice, video, shaders, 3D) dotyczą interaktywnych prototypów webowych (np. shadery WebGL), nie natywnych apek mobilnych.
- Animacje w materiałach Anthropic to animacje **webowe** (CSS/JS, hover states, przejścia w prezentacjach) — bo jedyny output Claude Design to kod.

**Inne pokrewne rzeczy mylone z "Claude design":**
- *Imagine with Claude* — krótkotrwały research-preview generujący UI "na żywo"; eksperyment, nie produkt do animacji produkcyjnych.
- *Figma MCP + Claude Code* (od lutego 2026) — dwukierunkowy most design↔kod (Figma ↔ kod); bez dedykowanego eksportu do Flutter/Rive.
- *Canva w Claude Design* — mechanizm eksportu/edycji, nie generator animacji.

**Wniosek:** "Claude design" to narzędzie do prototypowania UI/materiałów marketingowych **na webie**, sprzężone z Claude Code. Nie jest to narzędzie do produkcji assetów animacyjnych dla aplikacji mobilnej we Flutterze.

## 2. Twarda odpowiedź: TAK / NIE / CZĘŚCIOWO — per typ animacji

| Typ animacji | Odpowiedź | Komentarz |
|---|---|---|
| Kod animacji CSS/SVG/JS (web) | TAK | Mocna strona Claude Design i Claude Code — ale nie trafia bezpośrednio do Fluttera. |
| Kod animacji Flutter (implicit/explicit, AnimationController, Hero, staggered, physics) | TAK | Claude Code świetnie pisze natywny kod animacji Flutter — "solved problem". |
| Lottie JSON generowany przez Claude | CZĘŚCIOWO | Proste animacje UI (loadery, ikony, pętle, mikro-interakcje na bazie gotowych SVG) działają nieźle w pętli "napisz JSON → wyrenderuj → popraw" (skill `text-to-lottie`). Złożone, wielowarstwowe sceny — poza zasięgiem one-shotu, trzeba iterować lub kończyć w After Effects. |
| Lottie dla ryglowanej postaci (character rig — orka z wieloma częściami ciała) | RACZEJ NIE | Wsparcie dla hierarchical layer parenting w praktyce zawodne dla prawdziwych rigów postaci; praktycy kończą ręcznie (Illustrator/AE) lub animują dostarczone SVG. |
| Pliki .riv (Rive) | CZĘŚCIOWO | .riv to format binarny z edytora — Claude go nie "pisze". ALE istnieje oficjalny **Rive Editor MCP Server** (early access, na razie tylko macOS): AI steruje edytorem i tworzy state machine'y, kształty, przejścia, inputy. Realny podział: AI dobrze robi **logikę/interaktywność** (stany idle/happy/celebrate, przejścia, inputy), **rysowanie i rigging orki zostaje pracą artysty**. |
| Raster/wideo (GIF, sprite sheet, wideo maskotki) | NIE (natywnie) | Anthropic nie ma modelu generacji obrazu/wideo (świadoma decyzja). Możliwe wyłącznie przez integracje MCP z modelami trzecimi (FLUX/SD dla obrazów, Runway/Pika/Kling dla wideo, Spriteflow/Spritesheets.ai dla sprite sheetów) — Claude orkiestruje pipeline, kreację robi inny silnik. |
| Animacje osiągnięć/celebracji we Flutterze (confetti, progress, unlock) | TAK | Pakiet `confetti`, `flutter_animate`, AnimatedContainer/Hero/staggered — Claude Code generuje to samodzielnie, szybko i dobrze. |

**Podsumowanie: CZĘŚCIOWO.** Claude jest bardzo mocny w generowaniu **kodu animującego** (Flutter, CSS/SVG/JS, logika Lottie/Rive), ale **nie tworzy grafiki/rastra/wideo postaci** i ma udokumentowane ograniczenia przy złożonych rigach w Lottie. Prosta gamifikacja to zadanie w pełni w zasięgu samego Claude Code.

## 3. Rekomendowany pipeline

### A) Maskotka-orka (idle, reakcje, celebracje) — rekomendacja: **Rive, nie Lottie**

Rive działa na state machine (idle → reakcja → celebracja jako sterowalne stany/inputy), a nie liniowej osi czasu — dokładnie model potrzebny dla postaci reagującej na zdarzenia w apce (streak, osiągnięcie, koniec sesji).

1. **Artysta/ilustrator** projektuje orkę i tworzy bazowy rig w edytorze Rive (kształty, kości/meshe, artboardy). **Niezastępowalny krok ludzki** — nawet Anthropic swoją maskotkę animował ręcznie (4 dni ilustracji klatka po klatce).
2. **Claude Code + oficjalny Rive Editor MCP** (early access, macOS) buduje warstwę logiki: state machine z inputami (idle/happy/sad/celebrate), przejścia, ViewModel do bindowania danych z aplikacji (np. streak count → intensywność animacji).
3. **Integracja we Flutterze** przez pakiet `rive` — Claude Code pisze kod integracyjny (ładowanie .riv, sterowanie inputami z Cubita w reakcji na zdarzenia domenowe).
4. **Plan B bez budżetu na rigging:** prostsza orka z niezależnie animowanych kształtów SVG animowana kodem Flutter (CustomPainter + AnimationController) — Claude Code zrobi w pełni sam, ale efekt będzie prostszy (bardziej geometryczny, mniej "postaciowy").
5. **Nie polecane:** generowanie złożonego ryglowanego charakteru wprost jako Lottie JSON przez Claude.

### B) Animacje osiągnięć / celebracji — **w pełni wykonalne samym Claude Code**

1. Confetti/particle burst → pakiet `confetti` (pub.dev).
2. Karty osiągnięć, odznaki, progress bary → `flutter_animate` + implicit/explicit animations.
3. Ikona/odznaka z pętlą (np. "błyszczące" osiągnięcie) → prosty Lottie JSON wygenerowany przez Claude **na bazie dostarczonego SVG** (grounding w realnym assecie znacząco poprawia jakość).
4. Nie potrzeba tu Rive ani zewnętrznego generatora obrazu.

## 4. Czego Claude sam NIE zrobi + co wpiąć

- **Nie narysuje i nie zryguje orki** — potrzebny ilustrator/animator (freelancer/agencja) lub ktoś z umiejętnościami Rive/Illustrator/AE. Najbardziej krytyczny brakujący element pipeline'u.
- **Nie wygeneruje natywnie obrazu, GIF-a ani wideo** — zewnętrzny model przez MCP (FLUX/SD; Runway/Pika/Kling; Spriteflow/Spritesheets.ai).
- **Nie wyprodukuje złożonego Lottie one-shotem** — iteracja z człowiekiem lub dokończenie w AE/LottieFiles Creator.
- **Rive Editor MCP = early access, tylko macOS** — na Windows (nasze środowisko) dziś praktyczna blokada dla automatyzacji AI; klasyczny edytor Rive działa też na Windows, tylko bez wspomagania MCP.
- **LottieFiles AI (Motion Copilot)** — dojrzalsza platforma AI do prostszych animacji UI; warto rozważyć równolegle.

## 5. Bottom line

- **Gamifikacja (confetti, unlock, progress): TAK** — samym Claude Code, bez "Claude design" w ogóle.
- **Orka — logika/interaktywność animacji: TAK** — Claude Code (docelowo z Rive MCP, gdy dostępny na Windows) obsłuży state machine i integrację Flutter.
- **Orka — grafika i rigging postaci: NIE** — wymaga artysty; Claude Design (produkt webowy do prototypów/prezentacji) tego nie zastąpi.
- **Rekomendacja:** zlecić rigging orki w Rive (jednorazowy koszt), a logikę stanów i integrację z Flutterem oddać Claude Code — najlepszy stosunek jakości do wysiłku.

## Źródła

- https://www.anthropic.com/news/claude-design-anthropic-labs
- https://explainx.ai/blog/claude-design-june-2026-update-design-sync-2026
- https://venturebeat.com/technology/anthropic-ships-major-claude-design-overhaul-with-design-system-imports-code-round-trips-and-a-fix-for-its-token-burning-problem
- https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/
- https://www.canva.com/newsroom/news/canva-claude-design/
- https://www.testingcatalog.com/anthropic-experiments-with-an-agent-for-gereating-ui-on-the-fly/
- https://blog.laozhang.ai/en/posts/can-claude-generate-images
- https://github.com/diffusionstudio/lottie
- https://mcp.directory/blog/claude-text-to-lottie-skill-guide
- https://tympanus.net/codrops/2026/05/05/reverse-engineering-claude-ais-mascot-animations-with-svg-and-gsap/
- https://dev.to/uianimation/the-complete-guide-to-building-ai-powered-rive-agents-for-web-apps-4dc1
- https://dev.to/uianimation/building-high-performance-interactive-mascots-in-flutter-with-rive-production-guide-for-2026-17c6
- https://skywork.ai/skypage/en/unlocking-rive-ai-editor/1981622296102629376
- https://rive.app/docs/runtimes/advanced-topic/format
- https://github.com/Im5tu/claude/blob/main/skills/flutter-animations/SKILL.md
- https://pub.dev/packages/confetti
- https://www.figma.com/blog/introducing-claude-code-to-figma/
- https://lottiefiles.com/ai
