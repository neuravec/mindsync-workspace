# Wspólny workspace MindSync: start dla nowej osoby

Ten folder to wspólne środowisko pracy z Claude Code: zasady projektu (`CLAUDE.md`), agenci
i skille (`.claude/`), pamięć Claude (`claude-memory/`), blog, brand i głos marki, zasady
grafiki, sklepy, maile, raporty i skrypty publikacji. Kod aplikacji i Instagram żyją
w osobnych repozytoriach, które klonujesz do środka tego folderu.

```
<workspace>/                  repo neuravec/mindsync-workspace (ten folder)
  CLAUDE.md, ONBOARDING.md
  .claude/                    agenci, skille, komendy, wspólne ustawienia i hooki
  claude-memory/              pamięć Claude, wspólna dla obu osób
  blog/  docs/  store/  email/  seo/  design-specs/  ...
  scripts/                    publikacja bloga (Webflow), GSC, grafiki, ClickUp, PostHog, sync
  MindSync/                   repo backendu (FastAPI, Heroku), gałąź main
  mindsync-frontend/          repo aplikacji (Flutter), gałąź dev
  social/                     repo Instagrama (kolejka postów, szablony)
  therapist-deck/  Mindsync-fleet/
```

## 1. Dostępy, które musisz mieć

| Co | Po co | Jak |
|---|---|---|
| GitHub, organizacja neuravec | wszystkie repozytoria | zaproszenie do repo mindsync-workspace, MindSync, mindsync-frontend, mindsync-social, therapist-deck, Mindsync-fleet |
| Claude (Max) i Claude Code | praca z agentami | własna subskrypcja; artefakty i kanwy są prywatne, udostępnia się je z menu Share |
| Heroku, aplikacja mindsync | logi, migracje, dostęp do bazy przez dyno | zaproszenie jako collaborator, potem własny token (`heroku auth:token`) |
| Webflow, strona mindsync.app | blog i strona | członek workspace Webflow; token API własny albo z menedżera haseł |
| Loops | maile do użytkowników | członek zespołu MindSync w Loops; logowanie przez `/mcp` w Claude Code |
| PostHog (projekt 141170, EU) | analityka | członek projektu + własny Personal API Key |
| ClickUp | tickety | członek workspace; własny token do `.env` |
| Google Search Console | wyniki bloga | dodanie użytkownika do `sc-domain:mindsync.app`, potem własny `token.json` |
| App Store Connect, Google Play Console | sklepy | role w obu konsolach |
| Instagram @mindsync.app, Cloudinary | publikacja postów | wspólny token i klucze z menedżera haseł |
| Gemini (Google AI) | grafiki do bloga i IG | własny klucz albo wspólny z menedżera haseł |

Sekrety przekazujemy wyłącznie przez menedżer haseł. Nigdy przez git, czat, maila ani Claude.

## 2. Instalacja (raz)

1. Zainstaluj Git for Windows (z Git Bash), Python 3.12+, Node.js LTS i Claude Code.
   Flutter tylko, jeśli będziesz pracować na aplikacji.
2. Sklonuj workspace, np.:
   ```
   git clone https://github.com/neuravec/mindsync-workspace.git C:\Users\<ty>\Notebooks\MindSync\Heroku
   ```
3. W PowerShell w tym folderze:
   ```
   Set-ExecutionPolicy -Scope Process Bypass
   & .\scripts\workspace\setup.ps1
   ```
   Skrypt sklonuje repozytoria kodu obok, utworzy puste pliki `.env` z szablonów,
   zainstaluje zależności Pythona, skopiuje agentów i skille SEO do twojego profilu Claude,
   dopisze globalne zasady pisania i skieruje pamięć Claude do `claude-memory/`.
4. Uzupełnij pliki `.env`, które skrypt wypisał, wartościami z menedżera haseł.
5. Ustaw token Heroku: `setx HEROKU_API_KEY "<token z heroku auth:token>"` i zrestartuj terminal.
6. Uruchom `claude` w folderze workspace, wpisz `/mcp` i zaloguj Loops oraz ClickUp.
   Zatwierdź pluginy firebase, posthog i chrome-devtools, gdy Claude o nie zapyta.
7. Search Console: `scripts/gsc/INSTRUKCJA-autoryzacja-mindsync.md`.

Na starcie każdej sesji zobaczysz komunikat o synchronizacji. To znak, że hook działa.

## 3. Zasady współpracy (te same w CLAUDE.md, Claude ich pilnuje)

- **Start pracy:** hook sam robi `git pull` we wszystkich repo
  (`scripts/workspace/sync.py pull`). Konflikt albo pominięty pull Claude zgłasza na początku.
- **Koniec pracy:** Claude pokazuje, co zmieniło się w workspace i w social, i pyta, czy
  zrobić commit i push. Po zgodzie: `python scripts/workspace/sync.py push -m "opis"`.
  Skrypt przed commitem skanuje zmiany pod kątem sekretów i przerywa przy trafieniu.
- **Kod to osobny świat.** `sync.py` nigdy nie wypycha backendu ani frontu. Push na `main`
  backendu to od razu deploy na produkcję, push na `dev` frontu to build na TestFlight.
  Tam obowiązują zasady z CLAUDE.md: gałąź, testy, zgoda.
- **Publikuje jedna maszyna.** Dripy bloga (07:00) i Instagrama (co godzinę) działają
  z Harmonogramu zadań na komputerze Mikołaja. Nie rejestruj ich u siebie, bo posty
  wyszłyby dwa razy. Ręczna publikacja: najpierw pull, po publikacji od razu push,
  bo statusy w kolejce i `published-log.json` to stan współdzielony.
- **Pamięć Claude jest wspólna** (`claude-memory/`). Co Claude zapamięta u jednej osoby,
  druga dostanie po pull. Wiedza stała idzie do `CLAUDE.md` i `docs/`.

## 4. Czego nie ma w repo i dlaczego

- Klucze podpisu aplikacji i konta serwisowe (`itmesh/`): tylko menedżer haseł.
- Pliki `.env`, `token.json`, `client_secret*.json`: każdy ma własne.
- Logi Heroku i notatki robocze z katalogu głównego: mogą zawierać dane użytkowników.
- Worktree, kopie `*-live` i backupy: lokalne kopie robocze.
