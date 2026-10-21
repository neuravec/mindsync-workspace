# blog-attribution: atrybucja instalacji z bloga (mindsync.app)

Mały skrypt strony (vanilla JS, zero zależności, zero cookies/localStorage/sessionStorage),
który dopisuje do linków sklepowych informację, z którego wpisu bloga przyszedł użytkownik.

Stan: **PRZYGOTOWANY, NIEWDROŻONY** (2026-10-01). Nic nie zostało zapisane do żywego Webflow.

## Pliki

| Plik | Rola |
|---|---|
| `blog-attribution.js` | wersja źródłowa, czytelna (2685 B), do przeglądu i ewentualnego wdrożenia jako hosted |
| `blog-attribution.min.js` | ta sama logika ręcznie zminifikowana (1949 B), mieści się w limicie 2000 znaków skryptu inline Webflow; **to jest plik do wdrożenia** |
| `test.js` | harness Node (bez zależności, `vm` + atrapa DOM); uruchamia te same 10 testów na obu wersjach |
| `test.html` | test w prawdziwej przeglądarce (prawdziwy DOM i `URL`) |

Przy każdej zmianie logiki zmień OBA pliki JS i puść `node test.js` (testy idą na obu buildach).

## Co robi skrypt

1. **Ustala slug wpisu.** Na `/journal/<slug>` bierze slug ze ścieżki (musi pasować do
   `^[a-z0-9-]{1,80}$`, inaczej nic nie robi). Na innych stronach czyta parametr
   `?from=blog-<slug>`. Brak sluga oznacza, że skrypt kończy działanie bez dotykania strony.
2. **Na wpisie: linki do „hubów" dostają `?from=blog-<slug>`.** Huby to strony z badge'ami
   sklepów: `/` i `/features` (lista `HUBS` w kodzie, można rozszerzyć). Obsługiwane hosty:
   `mindsync.app` i `www.mindsync.app` oraz linki względne. Linki do `/journal/*`, `/faq`
   i stron zewnętrznych nie są zmieniane. **Przepisanie dzieje się dopiero przy interakcji**
   (`pointerdown` lub `click`), nie przy ładowaniu: `/` i `/features` nie mają dziś tagu
   canonical, więc Googlebot (który renderuje JS, ale nie klika) nie zobaczy wariantów
   z parametrem. Goły host robi 301 na www z zachowaniem query (sprawdzone 2026-10-01).
3. **Linki sklepowe (gdy slug znany) dostają parametry:**
   - Google Play (`play.google.com/store/apps/details?id=com.mindsync.app`):
     `referrer=utm_source%3Dblog%26utm_medium%3D<medium>%26utm_campaign%3D<slug>`.
     Apka Android czyta to z Play Install Referrer (`install_attribution_service.dart`,
     zdarzenie `app_install_attributed`, property `install_source`).
   - App Store (`apps.apple.com/.../id6739644256`): `ct=blog-<slug>` (ucięte do 40 znaków)
     oraz `pt=<token>` **tylko** gdy stała `APPLE_PROVIDER_TOKEN` (w min: `T`) nie jest pusta.
     Bez `pt` Apple nie pokaże kampanii w App Analytics, więc `ct` zacznie działać dopiero
     po wpisaniu tokena (App Store Connect, App Analytics, Campaigns, Generate link).
   - Istniejące parametry są zachowane; jeśli link ma już `referrer` / `ct` / `pt`,
     skrypt ich nie nadpisuje. Każdy link jest dekorowany raz (atrybut `data-msb`).
4. **`medium`, prosta heurystyka:**
   - wpis, link wewnątrz treści (`.w-richtext`, czyli post-body) = `inline`;
   - wpis, link poza treścią (blok CTA szablonu `.blog-cta-card`, stopka) = `badge`;
   - inna strona, na którą użytkownik przeszedł z wpisu przez `?from=` (np. karta
     `[FEATURE:]` prowadzi na `/features`) = `card`.
5. **Zdarzenie PostHog.** Przy kliknięciu udekorowanego linku sklepowego:
   `blog_store_click {store, blog_slug, medium, page_path}`, **tylko** gdy
   `window.posthog && window.__msA` (zgoda Analytics z `msconsent-1.0.0.js`). Nigdy
   `identify`, nic nie jest wysyłane bez zgody. Dekoracja samego URL działa także bez zgody:
   to parametr w adresie, bez zapisu czegokolwiek na urządzeniu.
6. **Koegzystencja z `msconsent-1.0.0.js`.** msconsent ma własny listener `click`
   (capture na `document`), który wysyła `app_store_click` i Meta `Purchase`. Nasz skrypt
   go nie dotyka i niczego nie duplikuje: wysyła inne zdarzenie (`blog_store_click`),
   a href jest udekorowany już przy `DOMContentLoaded`, więc msconsent widzi docelowy URL.
   Linki dorenderowane później łapie jednorazowy rescan na `load`, a link, który i tak
   się prześlizgnął, jest dekorowany w momencie kliknięcia.

## Test lokalny

```powershell
node scripts/webflow/blog-attribution/test.js
```

Wynik z 2026-10-01: `ALL 10 TESTS PASSED` dla `blog-attribution.js` (2685 B)
i `blog-attribution.min.js` (1949 B).

Test w przeglądarce (opcjonalny):

```powershell
python -m http.server 8765 --directory scripts/webflow/blog-attribution
# http://localhost:8765/test.html                 (udaje /journal/demo-post)
# http://localhost:8765/test.html?mode=features   (udaje /features?from=blog-demo-post)
```

Strona wypisuje linie `PASS`/`FAIL`. Wynik z 2026-10-01 w headless Chrome: 9/9 i 5/5 PASS.

## Wdrożenie (WYMAGA ZGODY OPERATORA, nie wykonane)

Token z `scripts/webflow/.env` (token dripu CMS) **nie ma dostępu do Custom Code API**:
`GET /v2/sites/{site}/registered_scripts` i `/custom_code` zwracają `invalid_auth_version`
(sprawdzone 2026-10-01, tylko odczyt). Dlatego wdrożenie idzie przez **MCP Webflow
w sesji głównej** (OAuth z zakresem `custom_code`), albo przez nowy token z zakresami
`custom_code:read` + `custom_code:write`.

Site: `676ed8d44b863915ae191f41`. Rekomendacja: **skrypt zarejestrowany na poziomie całej
strony, lokalizacja `footer`**, żeby działał na `/journal/*`, `/features` i `/`.

1. **Odczyt stanu (bez zapisu).**
   - MCP `data_scripts_tool`: lista zarejestrowanych skryptów
     (API: `GET /v2/sites/676ed8d44b863915ae191f41/registered_scripts`).
   - MCP `data_scripts_tool`: lista skryptów zastosowanych na stronie
     (API: `GET /v2/sites/676ed8d44b863915ae191f41/custom_code`).
     **Zapisz odpowiedź jako snapshot** (scratchpad) do ewentualnego rollbacku.
     Oczekiwane wpisy: m.in. `msconsent` 1.0.0 oraz skrypty `mobilefixesv7`,
     `actionsdiscord`, `actionssmallfixes`, `actionscarousel`, `actionstextfixes`.
2. **Rejestracja skryptu inline** (zapis, za zgodą):
   `POST /v2/sites/676ed8d44b863915ae191f41/registered_scripts/inline`
   ```json
   {"sourceCode": "<pełna zawartość blog-attribution.min.js>",
    "version": "1.0.0", "displayName": "blogattribution", "canCopy": false}
   ```
3. **Zastosowanie na stronie** (zapis, za zgodą):
   `PUT /v2/sites/676ed8d44b863915ae191f41/custom_code`
   ```json
   {"scripts": [ ...WSZYSTKIE wpisy ze snapshotu z kroku 1 bez zmian...,
     {"id": "blogattribution", "version": "1.0.0", "location": "footer"} ]}
   ```
   **UWAGA:** ten PUT zastępuje całą listę. Wysłanie samego nowego wpisu zdjęłoby
   msconsent (banner zgody) i pozostałe skrypty. Jeśli narzędzie MCP robi
   „dodaj skrypt" w jednym kroku, po nim natychmiast zweryfikuj krok 4, czy lista nadal
   zawiera wszystkie wpisy ze snapshotu.
4. **Weryfikacja zapisu:** ponowny `GET .../custom_code` = snapshot + `blogattribution`.
5. **Publikacja strony: TAK, wymagana.** Custom code zastosowany przez API trafia na żywą
   stronę dopiero po site publish. Site publish robi **wyłącznie operator** (przycisk Publish
   w Designerze). Przed publikacją operator sprawdza, czy w Designerze nie wiszą inne,
   niezatwierdzone zmiany, bo publish wypchnie je wszystkie.

Wariant zapasowy (hosted, wzorem msconsent): upload `blog-attribution.js` jako asset
(`asset_tool`), potem `POST .../registered_scripts/hosted` z `hostedLocation` = URL assetu
i `integrityHash` = `sha384-ZA0cUXB3XK1GRbHtV5K1vlwRRg/Yp6DjIgzYo6YgHS7yi2JXGUVVw1a09gqdcljy`
(policz ponownie, jeśli plik się zmienił: `openssl dgst -sha384 -binary blog-attribution.js | openssl base64 -A`),
dalej kroki 3-5 bez zmian.

**Rollback (bez usuwania czegokolwiek):** `PUT .../custom_code` ze snapshotem z kroku 1,
potem publish przez operatora. Zarejestrowany skrypt zostaje w rejestrze (nie kasujemy).

**Wpisanie tokena Apple później:** zmień `T=''` w min (i `APPLE_PROVIDER_TOKEN` w pełnej
wersji), `node test.js`, zarejestruj jako `version: "1.0.1"`, w PUT podmień wersję wpisu
`blogattribution`, publish.

## Checklista po publikacji

1. Prywatne okno, `https://www.mindsync.app/journal/<dowolny-slug>`, bez klikania bannera:
   - badge Google Play w bloku CTA ma `referrer=utm_source%3Dblog%26utm_medium%3Dbadge%26utm_campaign%3D<slug>`;
   - link sklepowy w treści wpisu ma `utm_medium%3Dinline`;
   - badge App Store ma `ct=blog-<slug>`, bez `pt`;
   - w Network **zero** requestów do PostHoga (nadal brak zgody).
2. Klik (środkowy przycisk albo Ctrl) w kartę `[FEATURE:]` otwiera
   `https://www.mindsync.app/features?from=blog-<slug>`; tam badge'e mają `utm_medium%3Dcard`.
3. view-source wpisu i `/features`: w surowym HTML linki do `/features` i `/` są **bez**
   `?from=` (przepisanie tylko przy interakcji).
4. Po „Accept all": klik w badge, w PostHog Live events widać `blog_store_click`
   z `store`, `blog_slug`, `medium`, `page_path` **oraz** dotychczasowe `app_store_click`
   (po jednym, bez duplikatów).
5. `/`, `/blog`, `/features` bez `?from=`: linki sklepowe bez zmian (skrypt nic nie robi).
6. Konsola bez błędów; banner zgody działa jak wcześniej.
7. Android end-to-end (opcjonalnie, internal testing): instalacja z udekorowanego linku,
   w PostHog `app_install_attributed` z `utm_campaign` = slug.

## Uwagi dla właścicieli innych obszarów

- **GA4 bez bramki zgody** (CRIT/HIGH z `security-reports/2026-08-10-consent-gate-ruling.md`,
  jeśli nadal otwarte): po wdrożeniu `page_location` na `/features?from=blog-<slug>` trafi
  do GA4 także bez zgody. Treść to tylko slug publicznego wpisu, ale warto, by
  security-guardian rzucił okiem przed publikacją.
- **Canonical na `/` i `/features`** (brak, stan 2026-10-01): do `seo-tech-lead`.
  Skrypt i tak nie wystawia crawlerom URL-i z parametrem.
