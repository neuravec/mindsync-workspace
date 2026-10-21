# Wyniki bloga i kontrola indeksacji, 3 dni po resubmicie sitemapy

**Data:** 2026-09-25
**Źródła:** GSC URL Inspection API (48 adresów: 23 wpisy pod www i gołą domeną, `/blog`, `/`), GSC Sitemaps API, GSC Search Analytics (dane do 24.09), żywa sitemapa, `_drip-log.txt`
**Surowe dane:** scratchpad sesji, `gsc_2026-09-25.json`

---

## Odpowiedź w skrócie

1. **Zator z 22.09 jest zdjęty.** W indeksie jest **21 z 23 wpisów** (22.09: 14 z 22). Resubmit sitemapy zadziałał w kilka godzin: 7 wpisów scrawlowanych 22.09 między 09:38 a 13:45 i wszystkie zaindeksowane.
2. **Przyczyna źródłowa nie zniknęła.** Google znowu nie pobrał sitemapy od 22.09 09:34 (3 dni), a `lastmod` `/blog` stoi na 15.09. Jedyny wpis opublikowany po resubmicie (`how-to-name-what-you-feel`, 23.09) jest `unknown to Google`. Bez ręcznego ruchu po każdej publikacji zator wróci.
3. **Blog zaczął realnie pracować.** Wyświetlenia bloga: 13 → 15 → **402 tygodniowo**, a 22-24.09 już ~100 dziennie. Kliknięć jest mało: **11 od 14.09**.

---

## Indeksacja: 23 wpisy

| Stan | Ile | Wpisy |
|---|---|---|
| W indeksie (www) | 19 | wszystkie poza trzema niżej i poza `how-to-prepare-for-a-therapy-session` |
| W indeksie tylko pod gołą domeną | 2 | `how-to-prepare-for-a-therapy-session`, `why-mood-tracking-stops-working` (www = `Discovered`) |
| `Discovered`, nieodwiedzony | 1 | `how-to-identify-emotional-triggers` |
| Nieznany Google | 1 | `how-to-name-what-you-feel` (opublikowany 23.09, po ostatnim pobraniu sitemapy) |

```
GSC Sitemaps API
lastSubmitted  : 2026-09-22T09:34:01Z
lastDownloaded : 2026-09-22T09:34:02Z   <- od tamtej pory bez pobrania
warnings       : 0
/blog lastmod w sitemapie : 2026-09-15T10:45:58Z   <- znowu zamrożony
/blog ostatni crawl       : 2026-09-15
```

**Kanały odkrywania.** Sitemapa jest dalej głównym źródłem (17 wskazań w `referringUrls`). Pierwszy raz pojawiły się linki wewnętrzne: z innych wpisów, z `/features`, z `/regulamin`. Nadal ani jeden wpis nie ma w `referringUrls` strony `/` ani `/blog`, czyli sekcja „Latest from the journal" dalej nie pomaga w odkrywaniu.

**Drip stoi.** Kolejka pusta od 24.09 (`BRAK wpisow gotowych` 24 i 25.09). Nowych wpisów do zindeksowania nie ma, więc zator nie boli w tej chwili, ale wróci przy partii 4.

---

## Wyniki (GSC, dane do 24.09)

### Tydzień do tygodnia (okna 7-dniowe)

| Okno | Blog: wyśw. | Blog: klik. | Domena: wyśw. | Domena: klik. |
|---|---|---|---|---|
| 01-07.09 | 13 | 0 | 648 | 22 |
| 08-14.09 | 15 | 0 | 712 | 21 |
| 15-21.09 | **402** | 3 | 927 | 22 |
| 22-24.09 (3 dni) | **311** | 5 | 482 | 17 |

Wzrost wyświetleń całej domeny (+43% tydzień do tygodnia) to niemal w całości blog. Kliknięcia domeny nadal stoją na ~3 dziennie i dalej są brandowe; blog dokłada 1-2 dziennie.

### Wpisy od 14.09 (top 10 z 20 z wyświetleniami)

| Wpis | Wyśw. | Klik. | Poz. |
|---|---|---|---|
| how-to-remember-what-you-talk-about-in-therapy | 173 | 3 | 5,5 |
| sunday-scaries | 116 | 0 | 8,3 |
| journaling-vs-voice-notes | 83 | 1 | 8,6 |
| is-therapy-worth-the-money | 82 | 1 | 6,8 |
| what-to-do-when-your-therapist-is-not-the-right-fit | 54 | 0 | 11,9 |
| racing-thoughts-at-night | 28 | 0 | 4,5 |
| how-to-prepare-for-a-therapy-session | 27 | 0 | 12,3 |
| why-mood-tracking-stops-working | 25 | 1 | 5,1 |
| are-mental-health-apps-private | 23 | 0 | 9,2 |
| how-to-stop-doomscrolling | 19 | 0 | 6,2 |

Świeże wpisy z 21-22.09 łapią wyświetlenia w 1-2 dni od indeksacji (`therapy-hangover` 18 wyśw. i 1 klik., `how-long-therapy-takes-to-work` 1 klik.).

### Co mówią zapytania

- Widać tylko ~115 z ~700 wyświetleń bloga; reszta to zapytania zanonimizowane przez Google.
- `sunday-scaries` zbiera wyświetlenia prawie wyłącznie z `sundays feel like saturday` (37, poz. 8,5, 0 klik.). To inna intencja (pomylony dzień tygodnia), więc 116 wyświetleń tego wpisu jest w dużej części pustych.
- Klaster kosztowy działa: `is therapy worth the cost?` / `...actually worth the cost?` / `is therapy worth the money` na poz. 5-9.
- CTR bloga ~1,5% przy średniej pozycji 5-9. Na tych pozycjach to nisko, więc warto przejrzeć title i description wpisów z top 3 wyświetleń.

---

## Co zrobić

1. **Teraz:** resubmit `sitemap.xml` w GSC (jedno kliknięcie) albo ręczne „Request indexing" dla `how-to-name-what-you-feel` i `how-to-identify-emotional-triggers`.
2. **Zamknąć pętlę w `blog-publish.ps1`.** Skrypt już wykrywa problem (`DISCOVERY UWAGA: /blog lastUpdated ... starszy niz ostatni wpis`), ale go nie naprawia. Po publikacji powinien realnie zmienić ustawienia strony `/blog`, żeby odświeżyć `lastmod`. To usuwa potrzebę ręcznego resubmitu po każdym wpisie.
3. **Duplikat host www / goły:** 2 wpisy siedzą w indeksie pod gołą domeną, a wersja www jest `Discovered`. Samo się ułoży, bo goła domena robi 301 na www, ale warto sprawdzić przy kolejnym pomiarze.
4. **Partia 4**, bo drip stoi od 24.09. Materiał jest w `blog/queue/_preflight-partia3.json`.
5. **CTR:** przepisać title/description `how-to-remember...`, `is-therapy-worth-the-money`, `journaling-vs-voice-notes` (pozycje 5-9, CTR ~1-2%).

**Następny pomiar:** po partii 4 albo ok. 02.10. Metryki: `lastDownloaded` sitemapy i liczba wpisów w indeksie.
