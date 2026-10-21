# GA4: grupa treści (filtrowanie bloga w Analytics)

> Cel biznesowy: móc w GA4 jednym kliknięciem odfiltrować ruch na blogu (wpisy + hub + kategorie + tagi) i porównać go z produktami/kategoriami sklepu.
> Data ustaleń: 2026-08-11, wszystko zweryfikowane na żywym sklepie.
> Decyzja: **opcja A** (grupa treści w GTM), zamiast zmiany przestrzeni adresowej bloga. Uzasadnienie w §1.

## 1. Dlaczego NIE zmiana przestrzeni adresowej bloga

Panel Shopera (Wygląd i treści → Blog → Ustawienia bloga → SEO → Przestrzeń adresowa) daje wybór
`/:lang/n/*` (obecnie) albo `/:lang/blog/*`. **Ta opcja nie dotyczy wpisów.**

Stan faktyczny (sprawdzone 2026-08-11):

| Element | URL | Kod |
|---|---|---|
| Wpis bloga (58 szt. w sitemapie) | `/klucz-udarowy-czy-zakretarka-udarowa-roznice` | 200, canonical = ten sam |
| Ten sam wpis w przestrzeni `n` | `/pl/n/<slug>` | **404** |
| Hub bloga | `/pl/n/list` | 200 |
| Kategoria bloga | `/pl/n/category/Porownania/8` | 200 |
| Tag | `/pl/n/tag/elektronarzedzia` | 200 |

Wpisy siedzą na **roocie domeny**, poza przestrzenią `n`. Przełącznik zmienia tylko hub, kategorie i tagi,
czyli ~60 URL-i pomocniczych, a 58 artykułów zostałoby bez słowa „blog" w ścieżce. Cel (filtr w Analytics)
nie zostałby osiągnięty, a doszłyby koszty: nieznane zachowanie 301 na starych URL-ach hubu, ręczna poprawka
linku „Blog" w menu (Wygląd i treści → Linki w nagłówku i stopce, wpisane na sztywno `/pl/n/list`),
regeneracja breadcrumbów i ponowne przeindeksowanie.

Realna zmiana URL-i wpisów wymagałaby przepisania `translations.pl_PL.permalink` 58 wpisów na `blog/<slug>`
(nietestowane: czy Shoper przyjmuje ukośnik w permalinku), 58 reguł 301, przepisania linkowania wewnętrznego
i wejścia w znany bug 301 vs query string. Odłożone jako osobna decyzja, nie jako rozwiązanie problemu z GA4.

## 2. Jak faktycznie leci pomiar (zweryfikowane w przeglądarce)

- Moduł integracji **123** (`google_analytics`): `{"trackingId":"G-M5MLW9YV9T","containerId":"GTM-KB4PFMJZ","isGTM":"1"}`
  → GA4 jest **zarządzana z GTM**, nie natywnie. Potwierdzenie: `region1.analytics.google.com/g/collect?v=2&tid=G-M5MLW9YV9T&gtm=45je...`
  (sygnatura `je` = tag odpalony z kontenera GTM). Czyli `content_group` ustawiony w GTM zadziała.
- Moduł **175** (legacy): `{"trackingId":"G-6B2TM0L99H","isGTM":"0"}` → biblioteka `gtag/js` się ładuje,
  ale **brak wysyłki `page_view`** dla tego ID. Zgodne z ustaleniem z audytu pocutoverowego. Nie ruszać.
- Google Ads `AW-16556614665` odpala się z tego samego kontenera (ccm/collect, remarketing, 1p-user-list).
- ⚠ **Drugi, obcy kontener:** `GTM-T68LWS` ładowany z `l=shopLayer`, a przez niego GA4 `G-7BS8B27X65`.
  To warstwa platformowa Shopera (WONTFIX), osobna od naszej. Nie dubluje naszej właściwości, ale warto
  o niej wiedzieć przy debugowaniu.
- ⚠ Stary Universal Analytics (`analytics.js` + `plugins/ua/linkid.js`) nadal się ładuje. Martwy kod,
  do sprzątnięcia przy okazji (perf, nie pomiar).

## 3. Wdrożenie: zmienna + pole w tagu Google

### 3a. Nowa zmienna GTM

Kontener **GTM-KB4PFMJZ** → Zmienne → Zmienne zdefiniowane przez użytkownika → Nowa
→ typ **Własny kod JavaScript** → nazwa: `JS - Typ tresci`

```js
function() {
  var p = location.pathname.replace(/\/+$/, '') || '/';

  // blog: najpierw ścieżki modułu, potem sam wpis (root domeny)
  if (/^\/pl\/n\/list/.test(p))        return 'Blog - lista';
  if (/^\/pl\/n\/category\//.test(p))  return 'Blog - kategoria';
  if (/^\/pl\/n\/tag\//.test(p))       return 'Blog - tag';
  if (document.querySelector('h1.blog-article-title')) return 'Blog - wpis';

  // sklep
  if (/^\/pl\/p\//.test(p))            return 'Produkt';
  if (/^\/pl\/c\//.test(p))            return 'Kategoria';
  if (/^\/pl\/i\//.test(p))            return 'Strona informacyjna';
  if (/^\/pl\/searchquery/.test(p))    return 'Wyszukiwanie';
  if (/^\/pl\/(basket|order|checkout|payment)/.test(p)) return 'Koszyk i zamowienie';
  if (/^\/pl\/(login|register|account|client)/.test(p)) return 'Konto';
  if (p === '/' || p === '/pl')         return 'Strona glowna';

  return 'Inne';
}
```

Dlaczego `h1.blog-article-title`, a nie `article.blog-article`: klasa `blog-article` występuje także na
liście i na kategorii bloga (kafelki zapowiedzi), więc dawałaby fałszywe trafienia. `h1.blog-article-title`
jest tylko na stronie wpisu (sprawdzone: wpis 1, lista 0, kategoria 0). Kolejność warunków ma znaczenie.

### 3b. Podanie wartości do GA4

Tagi → tag typu **Tag Google** z ID `G-M5MLW9YV9T` (w specyfikacji buildu: `GT - Google Tag (GA4)`)
→ **Ustawienia konfiguracji** → dodaj wiersz:

| Nazwa parametru | Wartość |
|---|---|
| `content_group` | `{{JS - Typ tresci}}` |

To wystarcza: parametr z konfiguracji tagu Google propaguje się na wszystkie kolejne zdarzenia GA4
tego strumienia na danej stronie (w tym `page_view` i zdarzenia e-commerce). **Nie trzeba** rejestrować
wymiaru niestandardowego, bo „Grupa treści" (`content_group`) to wymiar wbudowany GA4.

### 3c. QA przed publikacją

1. Tryb Podgląd GTM na `sklep.plasmet.pl/klucz-udarowy-czy-zakretarka-udarowa-roznice` → zmienna
   `JS - Typ tresci` = `Blog - wpis`.
2. Powtórzyć na: `/pl/n/list` (`Blog - lista`), `/pl/n/category/Porownania/8` (`Blog - kategoria`),
   dowolnym `/pl/p/...` (`Produkt`), `/pl/c/...` (`Kategoria`), home (`Strona glowna`).
3. GA4 DebugView: `page_view` niesie `content_group`.
4. Publikacja z nazwą wersji `content_group - typ tresci`, wpis do `docs/google-ads-zmiany.md`.
5. Po publikacji weryfikacja z zewnątrz: w żądaniu `g/collect` musi pojawić się parametr `ep.content_group`
   (albo `cg1`). Sprawdzalne bez panelu.

### 3d. Gdzie potem klikać w GA4

- Raporty → Zaangażowanie → **Strony i ekrany** → zmiana wymiaru głównego na **Grupa treści**.
- Eksploracje / dowolny raport → filtr **Grupa treści zawiera `Blog`** = cały blog w jednym worku.

## 4. Historia (dane od 13.07 do dnia wdrożenia)

Grupa treści działa od momentu publikacji kontenera, wstecz nie policzy. Do historii filtr strukturalny,
bo tylko wpisy bloga są jednosegmentowymi ścieżkami w roocie (produkty `/pl/p/`, kategorie `/pl/c/`,
CMS `/pl/i/`, hub `/pl/n/`):

```
Ścieżka strony pasuje do wyrażenia regularnego:  ^/[a-z0-9][a-z0-9-]{4,}$
```

Działa retroaktywnie w Eksploracjach i w Looker Studio. Przy pierwszym użyciu przejrzeć górne wiersze,
czy nie wpadło coś poza blogiem.

## 5. Próba wdrożenia i DECYZJA (2026-08-11)

### Co zostało zrobione i co się nie udało

1. Zmienna `JS - Typ tresci` (Custom JS, id 33) **utworzona w kontenerze** i działa poprawnie.
2. Tag Google `G-M5MLW9YV9T` (id 27) **nie pokazuje w UI sekcji „Ustawienia konfiguracji"**.
   Eksport kontenera potwierdza: tag ma tylko jeden parametr, `tagId`. Nie ma czego wypełnić w panelu.
3. **Obejście przez `gtag('set')` w tagu Niestandardowy kod HTML: NIE DZIAŁA.** Tag odpala się poprawnie
   i w odpowiedniej kolejności (`dataLayer[5] = CMD set {"content_group":"Blog - wpis"}`, przed `config`),
   ale w `dataLayer` **nie ma polecenia `config` dla `G-M5MLW9YV9T`** — tylko dla legacy `G-6B2TM0L99H`
   i `AW-16556614665`. Nasza właściwość jest konfigurowana wewnątrz piaskownicy kontenera GTM, która
   ignoruje `set` wykonany na stronie. Payload `g/collect?tid=G-M5MLW9YV9T` wyszedł bez `content_group`.
   Tag `HTML - content_group (set)` (id 34) został **wstrzymany**, nie usunięty.
4. Przygotowany, **NIEWDROŻONY** import chirurgiczny: `GTM/kontener-export/GTM-KB4PFMJZ_content-group.json`
   = eksport kontenera + jedno pole `configSettingsTable` (`content_group` = `{{JS - Typ tresci}}`) w tagu 27.
   Weryfikacja pliku: JSON parsuje się, liczby zgodne (16 tagów / 10 reguł / 5 zmiennych), porównanie
   tag po tagu wykazuje dokładnie 1 różnicę. Pewność co do kształtu pola `configSettingsTable`
   oszacowana na ~85-90% (standard eksportu GTM, ale brak drugiego przykładu w tym kontenerze).

### Decyzja usera: NIE ROBIMY tego w GTM

Powód: modyfikacja głównego taga Google przy pomiarze, od którego zależą konwersje Ads, przy nie w pełni
potwierdzonym schemacie = ryzyko nieproporcjonalne do korzyści. **Ruch na blogu monitorujemy w GSC**
(filtr po stronach), a nie przez grupę treści w GA4.

Filtr do GSC / GA4, gotowy do użycia (tylko wpisy bloga są jednosegmentowymi ścieżkami w roocie):

```
^https://sklep\.plasmet\.pl/[a-z0-9][a-z0-9-]{4,}$      (GSC: Strona > Filtr niestandardowy > wyrażenie regularne)
^/[a-z0-9][a-z0-9-]{4,}$                                 (GA4: Ścieżka strony > pasuje do wyrażenia regularnego)
```

GSC ma tu przewagę: działa retroaktywnie i bez żadnej zmiany w pomiarze. Ograniczenie: pokazuje tylko
ruch organiczny z Google, bez pozostałych kanałów. Do porównań blog vs sklep w GA4 zostaje regex wyżej.

Jeśli kiedyś wracamy do grupy treści, plik importu i cała diagnostyka są gotowe w tym dokumencie.
Nie zaczynać od `gtag('set')` w Custom HTML, to udowodniona ślepa uliczka.

### Efekt uboczny wart zapamiętania

Legacy `G-6B2TM0L99H` **wysyła** `page_view` (zaobserwowane na home), więc notatka z audytu
pocutoverowego „legacy GA4 nie zbiera" jest nieaktualna. Osobna właściwość, nie dubluje danych
`G-M5MLW9YV9T`, ale przy sprzątaniu tagów trzeba o tym wiedzieć.
