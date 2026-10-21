# Mail do wspólnika + checklista przed wysyłką

## A. Zanim wyślesz – 3 rzeczy do sprawdzenia

Jeśli któraś nie jest spełniona, on utknie na `auth` i wróci z błędem.

**1. Czy jego konto Google widzi właściwość mindsync.app w Search Console?**
GSC → Settings → Users and permissions. Musi tam być jego adres z poziomem
`Full` lub `Restricted` (`Owner` też oczywiście działa).
⚠ Uwaga: my mamy na tej właściwości poziom `siteFullUser`, a nie `siteOwner`.
Użytkownik typu Full **nie może dodawać kolejnych użytkowników** – to potrafi tylko
właściciel właściwości. Jeśli lista użytkowników jest u nas wyszarzona, dodanie musi
zrobić właściciel domeny (to samo konto, które trzyma weryfikację przez DNS).

**2. W jakim trybie jest ekran zgody OAuth w projekcie Google Cloud, z którego pochodzi
`client_secret.json`?**
console.cloud.google.com → wybierz projekt → APIs & Services → OAuth consent screen
(nowy interfejs: Google Auth Platform → Audience).
- Status **In production** – nic nie robisz, jego refresh token będzie żył bezterminowo.
- Status **Testing** – masz dwie opcje:
  a) dopisać jego adres Google w sekcji **Test users** (szybkie, ale refresh token
     wygasa mu po 7 dniach i co tydzień będzie musiał powtarzać `auth`),
  b) kliknąć **Publish app** i potwierdzić przejście do produkcji (zalecane, token
     nie wygasa; aplikacja zostaje „niezweryfikowana" przez Google, co daje tylko
     ostrzeżenie przy logowaniu, i to jest w porządku dla użytku wewnętrznego).

**3. Załącz właściwy plik.**
Wysyłasz **wyłącznie `scripts/gsc/client_secret.json`**.
**Nie wysyłaj `token.json`** – to jest Twój osobisty token do Twojego konta Google.
Klient OAuth jest wspólny, token nie.

Alternatywa, jeśli wolisz nie wysyłać sekretu mailem: niech założy własny projekt
w Google Cloud i własny OAuth client typu Desktop (10 minut, opis kroków jest
w `scripts/gsc/INSTRUKCJA-autoryzacja-mindsync.md`). Reszta paczki działa bez zmian.

## B. Co wysyłasz

1. `paczka-wspolnik.zip` (spakowana zawartość katalogu `scripts/gsc/paczka-wspolnik/`)
2. `client_secret.json` jako osobny załącznik

## C. Treść maila

---

**Temat:** Dostęp do Google Search Console (mindsync.app) – paczka + klucz

Cześć,

w załączniku masz komplet do podpięcia Google Search Console dla mindsync.app pod
Twojego Claude Code. To dostęp **tylko do odczytu**: frazy, adresy URL, kliknięcia,
wyświetlenia, CTR i pozycje. Nic nie zapisuje ani w Google, ani na stronie.

Co zrobić:

1. Rozpakuj `paczka-wspolnik.zip`, na przykład do `C:\mindsync-gsc`. Zachowaj strukturę
   katalogów, bo od niej zależy, gdzie lądują wyniki.
2. Drugi załącznik, `client_secret.json`, wrzuć do `scripts\gsc\`. Nazwy nie zmieniaj.
3. Otwórz `START-TUTAJ.md` i przejdź punkty 1-5. W skrócie: `python pull_gsc.py auth`
   (loguje przeglądarką), potem `python pull_gsc.py sites` (test dostępu) i
   `python pull_gsc.py pull --months 3 --full` (pobranie danych).
4. Potem odpal Claude Code w katalogu `mindsync-gsc`. Leży tam `CLAUDE.md`, który sam
   się wczyta i Claude będzie wiedział, jakich komend używać i gdzie szukać wyników.

Trzy rzeczy, które zaoszczędzą Ci nerwów:

- Przy logowaniu Google pokaże **„Google hasn't verified this app"**. To jest oczekiwane,
  bo to nasza wewnętrzna aplikacja. Klikasz Advanced → Go to ... (unsafe) i akceptujesz
  dostęp read-only.
- Zaloguj się kontem Google, które ma dostęp do mindsync.app w Search Console. Jeśli
  `python pull_gsc.py sites` nie pokaże mindsync.app, to znaczy, że wpadło złe konto
  albo brakuje uprawnień. Napisz, poprawimy.
- Dane w GSC mają opóźnienie około 3 dni, a sensowna ocena zmian w SEO to 4-6 tygodni.
  Skoki z jednego czy dwóch dni to szum, nie sygnał.

`client_secret.json` i powstający później `token.json` to sekrety. Nie wrzucaj ich do
repozytorium ani na dysk współdzielony. Gdybyś kiedyś chciał odciąć ten dostęp, robi się
to na https://myaccount.google.com/permissions.

Daj znać, jak przejdzie `sites`.

---

## D. Po jego stronie – co ma potwierdzić, że działa

Wynik `python pull_gsc.py sites` zawierający wiersz z `mindsync.app` i poziomem
uprawnień innym niż `siteUnverifiedUser`. To jest jedyny wiarygodny dowód, że dostęp gra.
