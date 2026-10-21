---
name: social-publish
description: >
  Runbook publikacji postów Instagram MindSync (nowe konto EN pod USA) przez oficjalne
  Instagram API with Instagram Login (graph.instagram.com): preflight (token, bramka,
  media), dry-run, publikacja na żywo tylko za zgodą operatora, pilot (single → karuzela
  → story → rolka), rejestracja dripu w Harmonogramie zadań, weryfikacja permalinku i obsługa
  błędów (token wygasł, kontener ERROR, media URL nieosiągalny, limit publikacji, wideo
  rolki długo IN_PROGRESS, host wideo).
  Używaj, gdy trzeba opublikować post z social/queue/, zrobić pilota, włączyć albo
  naprawić drip, odświeżyć token („opublikuj post na IG", „puść drip", „token IG wygasł",
  „/social-publish"). Tworzenie postów to skill `social-write`.
---

# Publikacja na Instagram MindSync: runbook

Kanał: `scripts/social/ig-publish.py` (agent B, szczegóły techniczne:
`scripts/social/README.md`). Wykonawca: agent `instagram-publisher` albo sesja główna.
Format kolejki: `social/queue/_format.md`. Konfiguracja konta i tokenu:
`social/SETUP-konto-instagram.md`.

## Zasady twarde

- **Dry-run domyślnie.** `ig-publish.py` bez `--live` niczego nie wysyła do Instagrama.
- **`--live` tylko za jawną zgodą operatora** dla tej operacji. Drip zarejestrowany po
  udanym pilocie = zgoda stała na posty ze statusem `gotowy`.
- Publikujemy tylko posty `gotowy` (status nadany przez operatora, skill `social-write`).
- **Niczego nie usuwamy** z Instagrama. Usunięcie albo archiwizację posta robi operator
  ręcznie w aplikacji.
- Idempotencja po `id`: post `opublikowany` albo obecny w `social/published-log.json`
  nie wychodzi drugi raz.
- Sekrety tylko w `scripts/social/.env`; nigdy w czacie, logach do operatora ani w repo.
- Zero instagrapi, prywatnego API i automatyzacji interakcji.

## 1. Preflight (przed każdą publikacją ręczną i po każdej zmianie w kanale)

```
python scripts/social/ig-token.py status       # ważność tokenu (dni do wygaśnięcia)
python scripts/social/ig-token.py check        # token działa, uprawnienia OK
python scripts/social/ig-token.py whoami       # właściwe konto (nowe, Business), IG user id
python scripts/social/social-gate.py --id <id> # 0 blokerów
```

Sprawdź też: `status` posta = `gotowy`, pliki z `media[]` istnieją
(`social/media/<id>/NN.jpg`), termin w ET ma sens. Token z mniej niż 14 dniami ważności:
najpierw `ig-token.py refresh` (sekcja 6).

## 2. Dry-run

```
python scripts/social/ig-publish.py --id <id>
```

Przeczytaj plan: typ, liczba kontenerów (karuzela = N dzieci + 1 rodzic), caption
z dopisanymi hashtagami (do 2200 znaków), alt per slajd, adresy mediów po hostingu.
Pokaż operatorowi skrót i zapytaj o zgodę na `--live`.

## 3. Publikacja na żywo (za zgodą)

```
python scripts/social/ig-publish.py --id <id> --live
```

Skrypt: wystawia JPEG-i pod publicznym URL (`media_host.py`) → tworzy kontener(y)
→ czeka na status `FINISHED` → publikuje → zapisuje `publikacja{ig_container_id, ig_media_id,
permalink, opublikowano}`, ustawia `opublikowany`, dopisuje `social/published-log.json`
i `social/_drip-log.txt`.

## 3a. Rolka (`typ: reel`)

- Preflight jak wyżej, plus: `social-gate.py --id <id>` przy statusie `gotowy` sprawdza MP4
  ffprobe (H.264 yuv420p, 1080x1920, 23-60 fps, 5-90 s, do 300 MB, AAC) i świeżość renderu;
  stara rolka = `python scripts/social/reel-render.py <id>`.
- Host wideo: `SOCIAL_VIDEO_HOST=cloudinary` w `scripts/social/.env` (Webflow nie przyjmuje
  wideo; dry-run pokazuje ostrzeżenie przy uploadzie MP4). Okładka JPEG idzie hostem obrazów.
- Dry-run pokazuje kontener `media_type=REELS`, `video_url`, `cover_url`, `caption`,
  `share_to_feed=true` i polling co `IG_VIDEO_POLL_INTERVAL_SEC` do `IG_VIDEO_POLL_MAX_SEC`
  (domyślnie 15 s / 900 s): wideo przetwarza się minutami, to normalne.
- Na żywo jak post: `ig-publish.py --id <id> --live` za zgodą operatora. Drip traktuje rolkę
  jak post feed (najwyżej 1 feed albo rolka + 1 story na przebieg).
- Dźwięk: wychodzi cicha ścieżka. Jeśli operator chce dźwięk popularny w USA
  (`social/CLAUDE.md` §2.3), publikuje tę rolkę ręcznie w aplikacji, z `reel.mp4`, i oznacza
  post w kolejce ręcznie; drip nie dodaje muzyki.
- Pilot: rolka jako czwarty krok pilota (po single, karuzeli i story), też za osobną zgodą.

## 4. Weryfikacja po publikacji (obowiązkowa)

- Otwórz `publikacja.permalink`: post jest na właściwym koncie, slajdy w dobrej kolejności,
  bez przycięcia tekstu, caption i hashtagi kompletne, zero znaków U+2014 i U+2013.
- Alt: w aplikacji (post → … → Accessibility / alt text) albo przez API, jeśli skrypt to raportuje.
- Story: znika po 24 h; sprawdź od razu marginesy (interfejs IG zasłania górę i dół).
- Raport dla operatora: id, permalink, godzina publikacji (ET i czas polski).

## 5. Pilot (raz, przed włączeniem dripu)

Kolejność, każdy krok za osobną zgodą operatora, każdy z weryfikacją z sekcji 4:
1. `single` na żywo.
2. `carousel` na żywo.
3. `story` na żywo.
4. Rejestracja dripu:
   ```
   powershell -ExecutionPolicy Bypass -File scripts\social\register-drip-task.ps1
   ```
   (parametry, częstotliwość wyzwalacza i tryb próbny: `scripts/social/README.md`).
   Zadanie uruchamia `python scripts/social/ig-publish.py --due --live`, które publikuje
   posty `gotowy` z terminem ET, który minął. Brak takich postów = wyjście bez błędu.
5. Pierwszy przebieg: sprawdź `social/_drip-log.txt` i permalink.

Zaznacz wynik pilota w raporcie dla operatora i w notatce projektu.

## 6. Błędy i co robić

| Objaw | Przyczyna | Co robić |
|---|---|---|
| `ig-token.py status` pokazuje mało dni / błąd OAuth (kod 190) przy publikacji | token wygasa albo wygasł | Ważny: `ig-token.py refresh` (token musi mieć min. 24 h; po odświeżeniu 60 dni). Wygasły: operator generuje nowy w panelu Meta (SETUP krok c.6), wkleja do `.env`, potem `whoami` + `check`. Posty czekają w kolejce, nic nie ginie. |
| Kontener ze statusem `ERROR` | zły format obrazu (nie JPEG, proporcje poza 4:5-1.91:1 dla feed, ponad 8 MB), uszkodzony plik | Sprawdź plik w `social/media/<id>/`; ponowny `render.py <id>` + `social-gate.py --id <id>`; problem szablonu → `graphic-designer`. Nie ponawiaj w pętli. |
| Rolka: kontener długo `IN_PROGRESS`, w logu „brak FINISHED po 900s" | Instagram przetwarza wideo dłużej niż limit | Post zostaje `gotowy` i wraca w kolejnym przebiegu; przy powtórkach zwiększ `IG_VIDEO_POLL_MAX_SEC` i sprawdź parametry MP4 (`social-gate.py --id`). |
| Rolka: „Webflow Assets API nie przyjmuje wideo" | `SOCIAL_MEDIA_HOST=webflow` bez hosta wideo | Ustaw `SOCIAL_VIDEO_HOST=cloudinary` + klucze `CLOUDINARY_*` w `scripts/social/.env`. |
| Kontener `EXPIRED` | kontener starszy niż 24 h bez publikacji | Uruchom publikację od nowa (skrypt tworzy nowy kontener). |
| Kontener długo `IN_PROGRESS` | Instagram przetwarza media | Skrypt odpytuje status (Meta zaleca raz na minutę, maks. 5 minut); po limicie post zostaje `gotowy` i wraca w następnym przebiegu. |
| Błąd pobrania mediów (media URL nieosiągalny) | hosting nie wystawił pliku publicznie, wygasły link, zły `SOCIAL_MEDIA_HOST` albo klucze | Otwórz URL z logu w przeglądarce bez logowania; popraw konfigurację hostingu w `scripts/social/.env`; ponów. |
| Limit publikacji | Instagram pozwala na 100 postów przez API w ruchomym oknie 24 h (karuzela = 1) i 400 kontenerów na 24 h | Przy naszej kadencji nie powinno wystąpić; jeśli wystąpi, to pętla w skrypcie: zatrzymaj drip (wyłącz zadanie), sprawdź `_drip-log.txt`, zgłoś operatorowi. `GET /<IG_ID>/content_publishing_limit` pokazuje zużycie. |
| Błąd uprawnień (np. brak `instagram_business_content_publish`) | token bez uprawnienia, konto bez roli testera, tryb aplikacji | `ig-token.py check`; SETUP krok c.4-c.6 i c.10. |
| Post opublikowany, ale skrypt nie zapisał statusu | przerwanie po publikacji | NIE publikuj ponownie. Sprawdź konto (najnowszy post) i log; uzupełnij `publikacja{}` ręcznie albo trybem naprawczym skryptu, jeśli istnieje (`scripts/social/README.md`). |
| Drip nic nie publikuje | brak postów `gotowy` z minionym terminem, komputer wyłączony, zadanie wyłączone | `_drip-log.txt`, Harmonogram zadań (ostatni wynik), `social-gate.py --all`. |

Źródła limitów i statusów: https://developers.facebook.com/docs/instagram-platform/content-publishing/ ,
https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media/ ,
https://developers.facebook.com/docs/instagram-platform/reference/refresh_access_token/ .

## 7. Utrzymanie

- Co tydzień: `ig-token.py status`, przegląd `social/_drip-log.txt`, ile postów `gotowy`
  zostało w kolejce (gdy mniej niż na tydzień: czas na `/social-write`).
- Wstrzymanie dripu: wyłącz zadanie w Harmonogramie zadań albo zmień status posta na `szkic`.
- Zmiana terminu posta `gotowy`: edycja `planowana_data`/`planowana_godzina_et` + `social-gate.py --id`.
