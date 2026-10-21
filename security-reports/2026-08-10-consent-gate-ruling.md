## Security Audit Report - Inverted Cookie-Consent Gate (www.mindsync.app) - 2026-08-10

Zrodlo zlecenia: `analytics-reports/2026-08-10-acquisition-collapse.md` (F5, F2, rekomendacja #3). Znalezisko zweryfikowane samodzielnie na zywej stronie (nie tylko na podstawie raportu ponizej).

### Executive Summary

Zywa strona `www.mindsync.app` laduje Meta Pixel (init + PageView + zdarzenie Purchase) oraz GA4 bezwarunkowo w `<head>`, przed jakakolwiek interakcja uzytkownika z bannerem zgody - podczas gdy PostHog, Contentsquare, Google Ads i GTM sa poprawnie zbramkowane za "Accept all"/zaznaczeniem checkboxa. To odwrocenie ryzyka: narzedzie o najwyzszym profilu ryzyka (piksel reklamowy trzeciej strony, na stronie produktu zdrowia psychicznego, z odbiorcami z UE) dziala bez zgody, a narzedzia analityczne pierwszej potrzeby sa zablokowane. Nagliwek to zdarzenie `fbq('track','Purchase', ...)` odpalane na klikniecie linku do sklepu, zabezpieczone WYLACZNIE sprawdzeniem `typeof window.fbq === "function"` - nie flaga zgody `window.__msM`. To narusza ePrivacy Art. 5(3) (zasada "zgoda przed przetwarzaniem") oraz nie ma waznej podstawy z Art. 6/7 GDPR dla wysylanych danych; na stronie firmy prezentujacej sie jako "AI therapy journal" domniemanie zainteresowania zdrowiem psychicznym podnosi ryzyko do strefy adjacency Art. 9. **Deployment kolejnych zmian bannera (np. poprawa opt-in rate) powinien byc wstrzymany do czasu naprawy tych dwoch tagow. To nie jest nowa regresja z 25.07 - luka w GA4/Meta istnieje odkad te tagi sa w kodzie strony (bramka z 25.07 objela tylko PostHog/Contentsquare/Ads/GTM), wiec skala ekspozycji jest szersza niz sam incydent z raportu wzrostu.**

### Weryfikacja stanu live (2026-08-10, ten audyt)

Pobrano `https://www.mindsync.app/` (curl, surowy HTML) oraz `https://cdn.prod.website-files.com/676ed8d44b863915ae191f41/6a64a2ac4d90955d5c396842_msconsent-1.0.0.js` (surowy JS, 7885 B) i przeczytano w calosci.

| Tag | Ladowanie | Bramka | Weryfikacja |
|---|---|---|---|
| GA4 `gtag('config','G-DWNVZNWCT5')` + `google_tags_first_party` push + async proxy `/nvhc9u4gxsag.../MOi6FWrF_...` | Bezwarunkowe, w `<head>`, przed jakimkolwiek klikiem | **BRAK** | Widoczne wprost w HTML `<head>` strony glownej, przed komentarzem "load only after cookie consent" |
| Meta Pixel `fbq('init','1768966087001664')` + `fbq('track','PageView')` + `connect.facebook.net/en_US/fbevents.js` | Bezwarunkowe, w `<head>` | **BRAK** | j.w. |
| Meta Pixel `fbq('track','Purchase',{store,app_id,url})` na klik linku do sklepu | Warunkowe na `typeof window.fbq==="function"` (linia 58 `msconsent.js`) | **POZOROWANA** - fbq jest zawsze zaladowany (bo init jest bezwarunkowy), wiec warunek jest zawsze prawdziwy; NIE sprawdza `window.__msM` (flaga zgody na Advertising) | Przeczytano zrodlo `msconsent.js` linia 58: `if(typeof window.fbq==="function"&&link.closest("a.div-button-store")){...fbq("track","Purchase",...)}` |
| PostHog (`phc_N2K7...`) + Contentsquare | W `loadAnalytics()`, wywolane tylko gdy `c.a` (checkbox Analytics, domyslnie odznaczony) | OK | `msconsent.js` linia 9-14, 25, 61-66 |
| Google Ads `AW-17877628667` + GTM `GTM-5CTMS8S7` | W `loadAds()`, wywolane tylko gdy `c.m` (checkbox Advertising) i respektuje Global Privacy Control (`GPC` wylacza checkbox) | OK | `msconsent.js` linia 15-24 |
| `app_store_click` (PostHog) | Gate na `window.posthog && window.__msA` | OK - poprawny wzorzec (kontrast z linia 58 dla fbq) | `msconsent.js` linia 57 |
| Komentarz w `<head>`: "Analytics and advertising tags (PostHog, Contentsquare, Google Ads, GTM, Meta) now load only after cookie consent" | - | **Falszywy w stosunku do implementacji** dla GA4 i Meta | Ten sam plik HTML, ten sam komentarz cytowany w tresci raportu wzrostu |

Global Privacy Control (GPC): obslugiwany WYLACZNIE w `loadAds()` (kategoria Advertising). Poniewaz GA4 i Meta nie przechodza w ogole przez `applyC()`, sygnal GPC dzisiaj nie ma na nie zadnego wplywu - kolejny efekt tej samej luki, nie osobny blad.

### Ruling per tag - severity i podstawa prawna

**CRIT-001 - Meta Pixel init + PageView bez zgody**
- Severity: **Critical**
- Lokalizacja: `<head>` strony glownej (Webflow global head code), poza `msconsent.js`
- Podstawa: ePrivacy Art. 5(3) (transpozycja krajowa, np. pl. Prawo telekomunikacyjne art. 173) - wymog uprzedniej zgody przed odczytem/zapisem plikow cookie lub podobnych technologii do celow innych niz scisle techniczne; Meta Pixel to cel marketingowy/reklamowy, nie techniczny. GDPR Art. 6/7 - brak wazniej podstawy przetwarzania (nie "prawnie uzasadniony interes" dla targetowania reklamowego wg wytycznych EDPB). Adjacency do Art. 9: strona opisuje sie jako "AI therapy journal" ("track emotional patterns", "share progress with your therapist") - samo odwiedzenie strony przez uzytkownika z UE i przekazanie tego kontekstu (URL, referrer, zachowanie) do platformy reklamowej trzeciej strony podnosi ryzyko wnioskowania o zainteresowaniu zdrowiem psychicznym.
- Impact: kazdy odwiedzajacy z UE, ktory jeszcze nie kliknal bannera (czyli 100% ruchu przed pierwsza interakcja, i cala reszta jesli olal banner) ma odpalony fbq init + PageView bez zgody. Dane trafiaja do Meta (transfer poza UE, choc w ramach DPF - nie jest to glowny problem tutaj, tylko brak podstawy prawnej w ogole).
- Remediacja: patrz "Kolejnosc napraw" ponizej, krok 1.
- Owner: **integration-devops** (zmiana w Webflow) + operator (zatwierdzenie zmiany produkcyjnej na stronie publicznej).

**CRIT-002 - Meta Pixel zdarzenie Purchase bez realnej bramki zgody**
- Severity: **Critical** (wyzszy priorytet naprawy niz CRIT-001, mimo tej samej klasy severity)
- Lokalizacja: `msconsent.js`, `clicks()`, linia 58
- Podstawa: jak wyzej, ale pogorszone dwoma czynnikami: (1) to zdarzenie konwersji/purchase-intent, nie tylko PageView - niesie wiecej sygnalu do modelu reklamowego Meta; (2) deweloper jawnie zamierzal je zbramkowac (wzorowany na poprawnym gate dla `app_store_click` w linii 57, `window.posthog&&window.__msA`) ale w linii 58 sprawdzil istnienie funkcji zamiast flagi zgody - blad projektowy, nie brak swiadomosci wymogu.
- Impact: kazde klikniecie linku do App Store/Google Play na stronie generuje zdarzenie Purchase do Meta z URL i identyfikatorem sklepu, niezaleznie od wyboru w bannerze, w tym dla uzytkownikow ktorzy jawnie kliknęli "Only essential".
- Remediacja: zmienic warunek na `window.fbq && window.__msM` (krok 2 ponizej).
- Owner: **integration-devops**.

**HIGH-001 - GA4 bez bramki zgody**
- Severity: **High** (nizej niz Meta, bo GA4 to analityka pierwszej strony wg deklarowanego celu, mniejsze ryzyko profilowania reklamowego niz piksel ad-tech - ale nadal narusza ePrivacy Art. 5(3))
- Lokalizacja: `<head>` strony glownej, poza `msconsent.js`
- Podstawa: jak CRIT-001, bez skladnika Art. 9-adjacency w tym samym stopniu (GA4 nie buduje z zalozenia audiencji reklamowych do targetowania, choc moze byc polaczony z Google Ads via linkage - nie zweryfikowano w tym audycie, do sprawdzenia przez integration-devops).
- Remediacja: krok 3 ponizej.
- Owner: **integration-devops**.

**HIGH-002 - falszywy komentarz w `<head>` (deceptive-comment angle)**
- Severity: High (integrity/governance, nie tylko kosmetyka)
- Opis: komentarz twierdzi, ze "Analytics and advertising tags (PostHog, Contentsquare, Google Ads, GTM, **Meta**) now load only after cookie consent" - to nieprawda dla GA4 i Meta od momentu wdrozenia tego komentarza. Dokumentuje zamierzony stan zgodny z prawem, ktorego implementacja nie spelnia - to gorsze niz brak komentarza, bo w razie kontroli/audytu regulatora stanowi dowod swiadomosci wymogu bez jego spelnienia.
- Remediacja: nie zmieniac komentarza teraz - dopiero PO poprawieniu kodu tak, by byl prawdziwy (krok 6).
- Owner: **integration-devops**.

**MED-001 - GPC honorowany tylko czesciowo**
- Severity: Medium
- Opis: sygnal Global Privacy Control dzis wylacza wylacznie kategorie Advertising (`loadAds`). Po naprawie GA4/Meta (przeniesieniu do gate'owanych funkcji) GPC automatycznie zacznie obejmowac rowniez te tagi - nie wymaga osobnej pracy poza krokami 1-3, ale nalezy to zweryfikowac w QA.
- Owner: **integration-devops** (weryfikacja w ramach tej samej zmiany).

### Zgodnosc GDPR / ePrivacy - stan obecny

| Wymog | Status | Uwagi |
|---|---|---|
| Zgoda przed non-essential cookies (ePrivacy Art. 5(3)) | Nie spelniony | GA4 + Meta ladowane bezwarunkowo |
| Podstawa prawna przetwarzania (Art. 6/7) | Nie spelniona dla GA4/Meta | Brak zgody = brak podstawy dla tych dwoch |
| Domyslny stan "opt-out" (checkbox Analytics odznaczony domyslnie) | Spelniony (dla PostHog/Contentsquare) | Poprawny wzorzec, warto zachowac przy naprawie GA4 |
| Zdarzenia konwersji bez zgody | Nie spelniony | `fbq Purchase` - patrz CRIT-002 |
| Honorowanie GPC | Czesciowy | Tylko kategoria Advertising dzis; rozwiazuje sie automatycznie po fix |
| Spojnosc dokumentacji z implementacja | Nie spelniona | Falszywy komentarz w `<head>` |

### Kolejnosc napraw (dokladna, tag-po-tagu) - integration-devops/operator wdraza w Webflow

**Krok 0 (rownolegle, nie blokuje ponizszych krokow Meta) - jednorazowy odczyt historii GA4.**
Wykonac PRZED krokiem 3 (zanim GA4 trafi za bramke i przestanie generowac niezaklocona serie). To zadanie z listy zadan #22 / rekomendacji #2 raportu wzrostu - pobrac dzienne sesje GA4 `G-DWNVZNWCT5` dla okna 2026-07-01 -> 2026-08-10, wylacznie zagregowane/statystyczne dane (bez eksportu rekordow na poziomie pojedynczego uzytkownika), jako jednorazowa diagnostyke wewnetrzna do zamkniecia hipotezy H5. Nie czeka na krok 3 ani nie blokuje krokow 1-2 (Meta) - to niezalezna sciezka czasowa. Owner: **integration-devops** (dostep do GA4) + operator.

**Krok 1 (natychmiast, najwyzszy priorytet, nie czeka na krok 0) - zbramkuj Meta Pixel init/PageView.**
Przenies inicjalizacje Meta Pixel (`fbq('init', '1768966087001664')`, `fbq('track','PageView')`, wstawienie `fbevents.js`) z bezwarunkowego `<head>` do nowej funkcji analogicznej do `loadAnalytics()`/`loadAds()` w `msconsent.js`, wywolywanej z `applyC(c)` gdy `c.m` (kategoria Advertising) jest prawdziwe - a nie z globalnego head code Webflow. Usun caly blok fbq z sekcji "Custom Code -> Head" w ustawieniach strony Webflow.

**Krok 2 (natychmiast, razem z krokiem 1) - napraw gate zdarzenia Purchase.**
W `msconsent.js`, `clicks()`, linia 58: zmien warunek z `typeof window.fbq==="function"` na `window.fbq && window.__msM` (wzorem linii 57 dla PostHog: `window.posthog&&window.__msA`). Bez tej zmiany krok 1 sam w sobie nie wystarczy - fbq nadal bedzie dostepny po pierwszym `loadAds()`, a warunek dalej bedzie zawsze prawdziwy dla kazdego kto kiedykolwiek zaakceptowal cokolwiek.

**Krok 3 (po zakonczeniu kroku 0) - zbramkuj GA4.**
Przenies `google_tags_first_party` push, tag async proxy `/nvhc9u4gxsag.../MOi6FWrF_...` oraz blok `gtag('js', ...); gtag('config','G-DWNVZNWCT5')` z bezwarunkowego `<head>` do `loadAnalytics()`, gate na `c.a` (ta sama kategoria co PostHog/Contentsquare - GA4 jest analityka, nie reklama).

*Alternatywa: Google Consent Mode v2.* Dopuszczalna WYLACZNIE jesli spelnione lacznie: (a) `gtag('consent','default',{analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'})` jest PIERWSZYM wywolaniem gtag, wykonanym przed jakimkolwiek `config`/`event`; (b) uzyty jest tryb "Advanced" (nie "Basic") lub jednoznacznie udokumentowana i zaakceptowana prawnie decyzja o cookieless pingach w trybie Basic; (c) zaktualizowanie zgody (`gtag('consent','update',...)`) nastepuje natychmiast po kliknieciu bannera, tym samym mechanizmem co dzis `c.a`. Obecna implementacja NIE realizuje Consent Mode v2 (wywoluje `config` bez zadnej wczesniejszej deklaracji `consent`) - wiec dzisiejszy stan nie kwalifikuje sie pod ten wyjatek. Rekomendacja: nie wprowadzac Consent Mode v2 teraz - uzyc tego samego twardego gate co dla PostHog/Ads (prostszy, jeden wzorzec, mniejsza szansa powtorki tego samego bledu). Jesli integration-devops/operator mimo to wybiora Consent Mode v2 dla GA4, wymagany jest ponowny przeglad security-guardian przed wdrozeniem.

**Krok 4 - weryfikacja GPC.**
Po krokach 1-3, potwierdzic w QA ze swiezy odwiedzajacy z ustawionym `navigator.globalPrivacyControl=true` NIE laduje GA4 ani Meta (obecnie GPC blokuje tylko Advertising `loadAds`; po przeniesieniu Meta do kategorii Advertising bedzie chroniony automatycznie - ale GA4 idzie do kategorii Analytics, ktora GPC dzis NIE wylacza. Do decyzji: albo GA4 zostaje w Analytics i GPC go nie blokuje (bo GPC to sygnal "no sale/no targeted ads", niekoniecznie "no analytics"), albo swiadomie rozszerzyc obsluge GPC na obie kategorie. Rekomendacja: GA4 w Analytics, GPC nie musi go wylaczac - ale to musi byc swiadoma decyzja zapisana, nie przypadek jak dzisiaj.

**Krok 5 - weryfikacja techniczna przed uznaniem za naprawione.**
Swiezy, prywatny profil przegladarki (brak `localStorage['msconsent']`), zaladowac `https://www.mindsync.app/`, sprawdzic w karcie Network: ZERO requestow do `connect.facebook.net`, `googletagmanager.com`, oraz do proxy `/nvhc9u4gxsag...`, i ZERO wywolan `gtag('config', ...)` w konsoli - przed jakimkolwiek klikiem w banner. Dopiero klik "Accept all" powinien je odpalic. To jest test akceptacyjny zastepujacy "no request to X before consent" z rekomendacji #3 raportu wzrostu.

**Krok 6 - aktualizacja komentarza i wersjonowanie.**
Dopiero gdy krok 5 przejdzie: (a) zaktualizowac/potwierdzic komentarz w `<head>` (jest juz poprawny tresciowo, tylko wymagal implementacji - nie trzeba go zmieniac, tylko sprawic by byl prawdziwy); (b) podbic wersje pliku do `msconsent-1.1.0.js` (nowy asset ID w Webflow, zeby CDN/cache nie serwowal starej, podatnej wersji 1.0.0 nikomu).

### Dane historyczne juz zebrane bez zgody - keep/purge

- **Meta Pixel (PageView + Purchase, caly okres od uruchomienia strony do naprawy)**: **PURGE**. Zbierane bez jakiejkolwiek podstawy prawnej przez caly czas dzialania strony (nie tylko od 25.07 - luka istniala zanim powstal msconsent.js). Zdarzenie Purchase niesie dodatkowo URL i kontekst klikniecia na stronie "AI therapy journal" - najwyzsze ryzyko wsrod zebranych danych. Rekomendacja: zlozyc wniosek o usuniecie danych zdarzen Pixela dla domeny mindsync.app przez narzedzia Meta Business (Data Deletion Request), obejmujacy caly okres do daty wdrozenia poprawki. Nie da sie tego cofnac z profili odbiorcow juz zbudowanych po stronie Meta (custom/lookalike audiences), wiec dodatkowo nalezy sprawdzic i wylaczyc/usunac wszelkie audiences zbudowane na tych zdarzeniach.
- **GA4 (`G-DWNVZNWCT5`), caly okres do naprawy**: **PURGE po wykonaniu kroku 0**, z jednym udokumentowanym wyjatkiem - jednorazowy, juz zaplanowany odczyt zagregowanych/statystycznych danych sesji (krok 0) na potrzeby domkniecia diagnostyki wzrostu (H5). Ten jeden odczyt nalezy potraktowac jako dochodzenie przyczyny incydentu (podobna logika do "legitimate interest" w kontekscie bezpieczenstwa/integralnosci systemu), udokumentowac w tym pliku i nie powtarzac. Po jego wykonaniu: skrocic okres retencji danych GA4 do najkrotszego dostepnego w ustawieniach property (2 miesiace) i nie przedluzac, co naturalnie wygasi pozostale dane historyczne bez dodatkowej akcji recznej.
- Uzasadnienie ogolne: zgoda na przetwarzanie danych osobowych nie dziala wstecz (nie mozna "uzyskac zgody po fakcie" dla juz zebranych danych) - jedyna zgodna z prawem sciezka to (1) ograniczone, udokumentowane wykorzystanie do celu, ktory juz w toku (diagnostyka incydentu w tym raporcie), (2) nastepnie usuniecie/wygaszenie.

### Kto wdraza

Cala zmiana kodu strony (Webflow custom code + `msconsent.js`) nalezy do **integration-devops**, jako zmiana produkcyjna na publicznej stronie marketingowej wymagajaca zatwierdzenia operatora przed wdrozeniem (nie backend/nie Flutter - poza mapa wlasnosci plikow tego zespolu, ale w zakresie integration-devops wg CLAUDE.md: "Firebase config files", "Deployment scripts" i ogolna rola bramki miedzy systemami; strona Webflow jest poza repo, wiec operator jest jedynym wykonawca zmiany w samym Webflow, integration-devops przygotowuje dokladna tresc zmiany do wklejenia). Wniosek o usuniecie danych w Meta Business i zmiana retencji GA4 - operator (wymaga dostepu do kont reklamowych/analitycznych, ktorych ten agent nie ma i nie powinien miec).

### Weryfikacja po wdrozeniu

Po wdrozeniu przez integration-devops/operatora, security-guardian ma ponownie przeczytac zywy HTML + `msconsent.js` (ten sam sposob co w tym audycie) i potwierdzic krok 5 (test siecowy w prywatnej przegladarce) przed zamknieciem tego znaleziska.
