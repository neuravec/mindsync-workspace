# Kontrola indeksacji bloga, 7 dni po naprawie z 15.09

**Data:** 2026-09-22
**Pytanie:** czy nowe wpisy indeksują się same, czy zaindeksowały się tylko te ręcznie zgłoszone, a potem nic
**Źródła:** GSC URL Inspection API (41 adresów, www i goła domena), GSC Sitemaps API, GSC Search Analytics, żywa sitemapa, żywy HTML `/` i `/blog`

---

## Odpowiedź

Przeczucie jest trafne. **Od 15.09 nie zaindeksował się ani jeden nowy wpis.** Google zna dokładnie te adresy, które dostał w dwóch zdarzeniach: pobranie sitemapy 13.09 i ręczne zgłoszenia 15.09. Po 15.09 blog nie dostał żadnego nowego wpisu do indeksu.

Twardy dowód, dlaczego: **Google nie pobrał sitemapy od 13.09 o 13:51**, czyli od 9 dni.

```
GSC Sitemaps API, sc-domain:mindsync.app
lastDownloaded : 2026-09-13T13:51:48Z
warnings       : 145        <- liczba sprzed sprzątania pre-orderów, jeszcze nieprzeliczona
submitted      : 34
```

Wszystkie wpisy opublikowane po 13.09 nie istnieją w kopii sitemapy, którą Google ma u siebie. A sitemapa jest u nas jedynym realnie działającym kanałem odkrywania.

---

## Bilans 22 wpisów

| Stan | Liczba | Wpisy |
|---|---|---|
| W indeksie | 14 | patrz niżej |
| `Discovered`, nie odwiedzony | 0 | - |
| **Nieznane Google** | **8** | doomscrolling, tracking-mood-on-antidepressants, are-mental-health-apps-private, therapy-hangover, how-long-therapy-takes-to-work, how-to-do-therapy-homework, how-to-identify-emotional-triggers, what-to-do-between-therapy-sessions |

Wśród nieznanych są **wszystkie 5 wpisów opublikowanych po naprawie** (16, 17, 18, 21 i 22.09). Cztery z nich mają już 3-6 dni.

### Skąd wzięło się te 14 w indeksie

| Data crawlu | Ile | Skąd | Wpisy |
|---|---|---|---|
| 2026-05-29 i 2026-09-18 | 2 | stare wpisy demo, znane wcześniej | regulate-nervous-system, digital-burnout |
| **2026-09-13** | 7 | **pobranie sitemapy** | how-to-choose-a-therapist, how-to-know-if-therapy-is-working, how-to-remember-what-you-talk-about, is-therapy-worth-the-money, which-coping-skills, how-to-prepare-for-a-therapy-session (goła domena), why-mood-tracking (goła domena, 14.09) |
| **2026-09-15** | 5 | **ręczne „Request indexing"** | how-to-use-mindsync, journaling-vs-voice-notes, sunday-scaries, what-to-do-when-your-therapist-is-not-the-right-fit, racing-thoughts-at-night |

Podpis ręcznego zgłoszenia jest widoczny w danych: cztery z pięciu wpisów z 15.09 mają `referringUrls = 0` **i** `sitemap = 0`. Google je zaindeksował, choć nie zna żadnej ścieżki, która do nich prowadzi. Tak wygląda wpis wepchnięty ręcznie.

---

## Co z trzech napraw z 15.09 zadziałało, a co nie

| Naprawa | Stan | Dowód |
|---|---|---|
| 301 na martwe URL-e | **Działa** | 4 wpisy demo → `/blog`, `/copy/sign-in` → `/`, `/admin---under-construction/...` → `/about`, wszystkie 301 |
| 6 stron `pre-order` poza sitemapą | **Wdrożone, ale niepoliczone** | sitemapa ma 34 URL zamiast 35, ale GSC dalej raportuje 145 ostrzeżeń, bo nie przeczytał jej od 13.09 |
| Odmrożenie `lastmod` na `/blog` | **Zadziałało raz i już się zestarzało** | `/blog` ma w sitemapie `lastmod = 2026-09-15T10:45`, mimo 5 publikacji po tej dacie |
| Sekcja „Latest from the journal" na `/` | **Żyje, ale nie odkryła ani jednego wpisu** | sekcja jest w HTML server-side, linki względne, bez `nofollow`, `/` scrawlowany 21.09, a `how-to-do-therapy-homework` (linkowany stamtąd od 15.09) dalej „unknown to Google". Żaden adres w całym audycie nie ma `/` ani `/blog` w `referringUrls` |

Sekcja na stronie głównej ma jeszcze drugą wadę: jest statyczna i wciąż pokazuje wybór z 15.09. Nie linkuje do żadnego z pięciu nowych wpisów.

---

## Czy cokolwiek się poprawiło

Tak, po stronie wyświetleń. To efekt tych 10 wpisów, które weszły do indeksu 13 i 15.09.

| Okno | Wyświetlenia bloga dziennie | Kliknięcia |
|---|---|---|
| 01-13.09 | 1-3 | 0 |
| 14-19.09 | 40-60, na 9-10 wpisach | pierwsze 1 kliknięcie, 19.09 |

Cała domena też urosła: ze 190-210 wyświetleń tygodniowo do 250-260. Najlepiej radzi sobie `how-to-remember-what-you-talk-about-in-therapy` (91 wyświetleń, średnia pozycja 5,7).

Czyli: **treść działa, kiedy wejdzie do indeksu.** Zator jest wyłącznie na wejściu.

---

## Co zrobić, w kolejności zwrotu

1. **Wymusić ponowne pobranie sitemapy.** GSC → Sitemaps → wpisz `sitemap.xml` → Submit. To jedno kliknięcie, nie zżera limitu 10 zgłoszeń dziennie i naraz udostępnia Google wszystkie 5 nowych wpisów plus przelicza 145 ostrzeżeń. Największy pojedynczy zysk. (Uwaga: `google.com/ping?sitemap=` już nie działa, Google wyłączył ten endpoint w 2023.)
2. **Zgłosić ręcznie 4 wpisy**, które mają już kilka dni: `therapy-hangover`, `are-mental-health-apps-private`, `tracking-mood-on-antidepressants`, `how-to-stop-doomscrolling`. Plus dwa zaległe: `how-to-do-therapy-homework`, `what-to-do-between-therapy-sessions`.
3. **Zamknąć pętlę w skrypcie dripu.** `blog-publish.ps1` po każdej publikacji powinien robić realną zmianę w ustawieniach strony `/blog` (żeby `lastmod` był świeży) i podmieniać 3 linki w sekcji na stronie głównej. Dopóki to jest ręczne, ten sam zator wróci za tydzień.
4. **Sekcja na `/` jako Collection List z CMS** zamiast statycznych kart. Wtedy punkt 3 znika sam.
5. **Bing Webmaster Tools + IndexNow.** Bing indeksuje łagodniej i zasila ChatGPT Search, a IndexNow daje to, czego Google nie daje: programistyczne zgłoszenie URL-a. Nie pomoże w Google, ale odkorkuje drugi kanał.

Punkt 7 z raportu z 15.09 zostaje aktualny: sufitem jest autorytet domeny, a ten ruszą tylko linki zewnętrzne.

---

## Metryka do pilnowania

Nie kliknięcia. **`lastDownloaded` sitemapy w GSC Sitemaps API.** Dopóki stoi w miejscu, nowe wpisy nie mają jak trafić do Google, niezależnie od tego, ile ich napiszemy.

---

# Weryfikacja po wykonaniu kroków 1 i 2 (operator, 2026-09-22)

Ponowne zgłoszenie sitemapy zadziałało natychmiast:

```
lastSubmitted  : 2026-09-22T09:34:01Z
lastDownloaded : 2026-09-22T09:34:02Z    <- pobranie sekundę po zgłoszeniu
warnings       : 0                        <- było 145
submitted      : 34
```

Dwie rzeczy naraz:

1. **Google ma wreszcie aktualną listę.** Wszystkie 34 adresy, w tym 5 wpisów, o których wcześniej nie wiedział. Zator na wejściu zdjęty.
2. **145 ostrzeżeń zeszło do zera.** To dowód, że wrześniowe wyrzucenie sześciu stron `pre-order` z sitemapy było trafne. Ostrzeżenia nie znikały wcześniej nie dlatego, że naprawa nie zadziałała, tylko dlatego, że Google nie przeczytał sitemapy po zmianie.

Pole `contents.indexed = 0` w tym API jest przestarzałe i zawsze zwraca 0. Nie czytaj go jako sygnału.

**Kiedy mierzyć efekt:** crawl nowych wpisów powinien ruszyć w ciągu 1-3 dni, indeksacja w ciągu kilku. Pierwszy uczciwy odczyt około 26-29.09. Metryka: liczba wpisów `Submitted and indexed`, dziś 14 z 22.
