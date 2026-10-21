# GSC dla mindsync.app – autoryzacja na właściwym koncie Google (instrukcja operatora)

Stan 2026-08-25: `token.json` w tym katalogu jest z konta PLASMET i widzi tylko
sklep.plasmet.pl. Właściwość mindsync.app żyje na INNYM koncie Google. Poniżej ścieżka
zalecana (własny projekt Google Cloud na koncie MindSync + aplikacja „In production",
żeby refresh token NIE wygasał po 7 dniach) i skrót alternatywny.

## Ścieżka zalecana: własny OAuth client na koncie MindSync (~10 minut, jednorazowo)

1. Zaloguj się w przeglądarce na konto Google, które MA właściwość mindsync.app w GSC.
2. Wejdź na https://console.cloud.google.com → utwórz nowy projekt (nazwa np. `mindsync-gsc`).
3. **APIs & Services → Library** → wyszukaj **„Google Search Console API"** → Enable.
4. **APIs & Services → OAuth consent screen** (Google Auth Platform):
   - User type: **External** → Create.
   - App name: `mindsync-gsc`, support e-mail i developer e-mail: Twój. Reszta pusta → Save.
   - Zakładka **Audience** → przycisk **Publish app** → potwierdź (status „In production").
     ⚠ To jest ten krok „żeby klucz nie wygasał": w trybie Testing refresh token umiera
     po 7 dniach; w Production żyje bezterminowo. Aplikacja będzie „niezweryfikowana"
     przez Google – dla własnego użytku to tylko ostrzeżenie przy logowaniu (patrz krok 7),
     weryfikacji NIE robimy.
   - (Scope `webmasters.readonly` skrypt poda sam przy logowaniu – nie trzeba nic dodawać.)
5. **APIs & Services → Credentials → Create credentials → OAuth client ID**:
   - Application type: **Desktop app**, nazwa dowolna → Create → **Download JSON**.
6. Pobrany plik zapisz jako `scripts/gsc/client_secret.json` (NADPISZ plik PLASMET;
   oryginał i tak żyje w repo plasmet). Stary token odsuń:
   `Rename-Item scripts\gsc\token.json token.plasmet.json`
7. W terminalu repo: `python scripts/gsc/pull_gsc.py auth`
   → otworzy się przeglądarka → wybierz konto MindSync → Google pokaże
   „Google hasn't verified this app" → **Advanced → Go to mindsync-gsc (unsafe)** →
   zaakceptuj dostęp read-only do Search Console. Skrypt sam zapisze nowy `token.json`.
8. Weryfikacja: `python scripts/gsc/pull_gsc.py sites`
   → na liście musi być mindsync.app. Zanotuj DOKŁADNĄ formę
   (`sc-domain:mindsync.app` czy `https://www.mindsync.app/`) i poziom uprawnień.
9. Popraw `scripts/gsc/gsc.config.json` → `site_url` = dokładna forma z kroku 8.
10. Test danych: `python scripts/gsc/pull_gsc.py pull` (wynik w `migracja/gsc/baseline-*/`).

## Skrót alternatywny (mniej kroków, ale wiąże MindSync z projektem GCP PLASMET)

W projekcie Google Cloud PLASMET (tam, gdzie powstał obecny `client_secret.json`):
OAuth consent screen → **Publish app** (Testing → In production). Potem lokalnie kroki
6b-10 z powyższej listy (rename token → `auth` logując się kontem MindSync → `sites` →
config → `pull`). Działa, bo OAuth client może autoryzować dowolne konto Google;
minus: konfiguracja MindSync zależy od cudzego projektu GCP.

## Po odblokowaniu – sanity check właściwości

- Jeśli `sites` pokaże `permissionLevel: siteUnverifiedUser` → właściwość jest
  niezweryfikowana i dane NIE spływają; trzeba ją zweryfikować (domain property = rekord
  TXT w DNS; URL-prefix = meta tag, który można wstawić przez Webflow Site Settings →
  Custom code head). Jeśli `siteOwner`/`siteFullUser` – wszystko gra.
- Zgłoś sitemapę: GSC → Sitemaps → `https://www.mindsync.app/sitemap.xml`
  (Webflow generuje ją automatycznie).
