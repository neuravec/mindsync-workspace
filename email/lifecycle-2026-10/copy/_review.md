# Przegląd treści maili P1-P9 (21.10.2026, wersja 2 po decyzjach leada)

Wejście: makiety `mockups/*.dc.html`, kontrakt `SPEC.md`, prawda o funkcjach z `blog/app-features.json`
i `mindsync-frontend/mindsync_app/lib` (paywall, `lib/l10n/app_en.arb`). P8 pominięty (wysłany 21.10).
Wszystkie teksty przeszły humanizer (tryb embedded), zmienione w wersji 2 ponownie. Kontrola mechaniczna:
zero U+2014 i U+2013 we wszystkich plikach `copy/`. Niczego nie wysłano, żadnego wywołania zapisu do Loops.

Pliki: P1, P2a, P2b, P3a, P3b, P3b-quiet, P4a, P4b, P5, P5-expired, P6a, P6b, P7 (szablon), P9.

## Decyzje leada z 21.10 (wdrożone w wersji 2)

| # | Decyzja | Gdzie |
|---|---|---|
| 1 | Harmonogram: P1 dzień 0; P2a +24 h bez pierwszej rozmowy; P3a ok. 36 h po `trialStarted`; P3b 24 h przed końcem trialu; P2b dzień 5 (po trialu) | pola `trigger`; P3a przepisany na "halfway through your Premium trial"; P2b bez wzmianek o trialu i bez trybu głosowego |
| 2 | P3b dzielony: `P3b` (aktywność, kafelki) i `P3b-quiet` (zdarzenie `trialEndingSoonQuiet`, bez statystyk) | P3b.json, P3b-quiet.json |
| 3 | Zero liczby dni w tematach; `{event.trialDays}` usunięty wszędzie, w treści "your trial" | P3a |
| 4 | P4b: trzy odpowiedzi | P4b.json |
| 5 | P5 dzielony: `P5` (wyłączony auto-renew) i `P5-expired` (Premium wygasło), te same przyciski z `p=P5` | P5.json, P5-expired.json |
| 6 | P6b ponadczasowy | P6b.json |
| 7 | Fallback `emailLinkToken` = `none` | pole `fallbacks` w każdym mailu z linkami akcji, `_variables.md` |
| 8 | Nowa linia kryzysowa z 988 | wszystkie maile |

## Zmiany wspólne

- **CTA "otwórz aplikację" to para przycisków sklepowych** `OPEN ON IPHONE` / `OPEN ON ANDROID` (jak P8).
  Aplikacja nie ma universal links, więc przycisk w stylu "START A 5-MINUTE REFLECT" i tak otwierałby stronę
  w sklepie. Wezwanie do działania zostało w tekście nad przyciskami. App Store: `...id6739644256?ct=<KOD>`
  (w repo nie ma provider tokena `pt=`, więc `ct` nie trafi do raportów App Store Connect). Google Play:
  `&referrer=utm_source%3Dloops%26utm_medium%3Demail%26utm_campaign%3D<KOD>`.
- Stopka: ikony Play, App Store, Discord, Instagram (URL-e z P8, sklepy oznaczone kodem maila).
- Linia kryzysowa (decyzja leada): "MindSync isn't a crisis service. If you're in crisis, call or text 988
  in the US, or find a local helpline at findahelpline.com."
- Obrazki: adresy `images.vialoops.com` z P8; pole `key` w bloku `image` mapuje blob z makiety.
- Zmienne w składni LMX (`{contact.x}`, `{event.x}`); składnia edytora i fallbacki w `_variables.md`.
- Temat z 🐋 zostawiony, to stały znak rozpoznawczy dotychczasowych kampanii.

## Najważniejsze odkrycie: trial nie jest trialem sklepowym

Trial to 4 dni przyznawane przez serwer przy rejestracji (`granted_via=signup_trial`), bez subskrypcji
w sklepie. Aplikacja mówi "Nothing is charged automatically" (`app_en.arb:1767`, `premium_view.dart:159`).
Makiety P3a i P3b mówiły, że trzeba anulować w ustawieniach sklepu i że Premium samo się przedłuży. To
nieprawda o pieniądzach, więc P3a, P3b i P3b-quiet mówią: żeby zostać w Premium, wybierz plan w aplikacji
pod Subscription (`app_en.arb:821`); jeśli nie, nic nie rób, konto przejdzie na wersję Free, dane zostają.

## Per mail

### P1 Powitanie (dzień 0)
- "it keeps track of what matters and helps you get it ready" na zdanie zgodne z aplikacją: Orca trzyma
  krótkie notatki, żeby cię pamiętać, można je czytać i usuwać w Settings (`app_en.arb:3226`, `3312`).
- `Hi {firstName}` na `{contact.firstName}` z fallbackiem `there` (fallback zapisany w bloku akapitu).
- "I read every answer myself" to deklaracja Darka; wymaga, żeby skrzynka darek@ odbierała odpowiedzi.

### P2a Start d1
- "summary you can keep or delete" na "reread the conversation later, or delete it" (`app_en.arb:265`).
- "lands on your Therapy Agenda" sugerowało automat; temat dodaje się ręcznie (`app_en.arb:2942`).
- Preview z trójką i przeczeniem przepisany. "in a couple of days" na "in a few days", bo P2b idzie w dniu 5.

### P2b Start d5 (po trialu, nadal bez rozmowy)
- Odbiorca jest już na Free. Usunięte "Out loud" (tryb głosowy Reflect jest Locked na Free,
  `premium_comparison_table.dart:33`); "Say what stuck" na "Write down what stuck".
- Dodane: "All three work on the free version of MindSync, so you can start today." Before therapy i After
  therapy mają na Free 1 na miesiąc, Reflect 15 wiadomości (`sources` w pliku).
- "Before a session": opis karty zgodny z `app-features.json` session-prep (summary, up to three numbered questions).

### P3a Trial w połowie (ok. 36 h po `trialStarted`)
- Nowy temat "You're halfway through your Premium trial", H1 "Halfway there." / "Here's what Premium
  unlocks while your trial lasts." Bez liczby dni.
- Lista korzyści to **prawdziwa tabela paywalla** "What Premium changes" (`premium_comparison_table.dart:28-37`,
  renderowana w `subscription_body.dart:169`), słowo w słowo: "wiersz: wartość Premium (Free: wartość Free)".
  Pominięte dwa wiersze Included w obu planach. Plik:linia dla każdej pozycji w polu `sources`.
- Plan skrócony do dwóch kroków na pozostałe dni ("Today", "Tomorrow").

### P3b Trial koniec, z aktywnością
- Kafelki `{event.reflects}`, `{event.agendaItems}`, `{event.activeDays}`, fallbacki 0/0/1.
- Bez "in 3 days". Usunięte "Premium continues tomorrow", "cancel ... won't be charged", przycisk "HOW TO CANCEL".
- **"usually the same day" usunięte** (brak SLA w repo); teraz "Hit reply. It comes straight to me."

### P3b-quiet Trial koniec, bez aktywności (nowy)
- Zdarzenie `trialEndingSoonQuiet`. Bez statystyk: łagodnie, że trial kończy się jutro, jeden mały krok
  (Reflect, można na głos, bo voice mode działa do jutra), potem plan pod Subscription albo Free, dane zostają.

### P4a Zakup
- Bez zmian merytorycznych, tylko CTA sklepowe.

### P4b Ankieta d14
- Trzy odpowiedzi (decyzja leada): YES, A LOT = very, A LITTLE = somewhat, NOT REALLY = not.
  "TOO EARLY TO SAY" z makiety usunięte.

### P5 Rezygnacja: wyłączony auto-renew
- "You've turned off auto-renew, so Premium stays on until the end of the period you've already paid for."
- **"no new trial maze" usunięte** (trial jest jeden na konto). Teraz "pick a plan again any time in the app,
  under Subscription". Przyciski price/not_using/missing/therapy_ended/other.

### P5-expired Premium wygasło (nowy)
- Mówi, że konto jest teraz na Free, dane zostają (`app_en.arb:1645`), limity Free odnawiają się 1. dnia
  miesiąca (`app_en.arb:1696`). Te same przyciski z `p=P5`; linki w stopce oznaczone `P5-expired`.
- Zdarzenie nazwane roboczo `subscriptionExpired`. SPEC §2 ma dziś jedno zdarzenie `subscriptionCancelled`
  na oba przypadki, więc backend musi je rozdzielić (albo wysłać właściwość `reason` i rozgałęzić workflow).

### P6a Powrót d14
- "No guilt trip, promise." na "This isn't a guilt trip, promise."; przycisk pauzy to link `a=pause`.

### P6b Powrót d30 (ponadczasowy)
- Usunięte odniesienia do wydania 2.0.56 (nowy Main, "AI got a name"). Teraz trzy pigułki o tym, w czym
  MindSync pomaga: przed sesją (Before therapy), po sesji (After therapy i Your progress in therapy po trzech
  sesjach, bez oceniania), w dni pomiędzy (Reflect z Orką, notatki do przeczytania i usunięcia w Settings),
  plus "Update it in the App Store or Google Play to see what's new since your last visit."
- Nowy temat "Still here for the days between sessions".

### P7 Newsletter (szablon)
- Nadawca **monika@mindsync.app**, reply-to monika@. Dotychczasowe kampanie wychodziły z tego adresu
  (`claude-memory/project_email_new_look_2026_10_21.md`), więc nadawca istnieje. Nie sprawdzałem w Loops,
  czy skrzynka odbiera odpowiedzi.
- Placeholdery dla Moniki, przyciski feedbacku z `&i=[issue-slug]`, instrukcje w `template_notes`.

### P9 Wygaszanie
- Nadawca Darek. "stop sending newsletters" na "stop emailing you", bo `subscribed=false` wyłącza cały marketing.

## Otwarte ryzyka

1. Backend musi wysyłać trzy nowe lub zmienione zdarzenia: `trialEndingSoonQuiet`, `subscriptionExpired`
   (nazwa robocza) oraz P3a z opóźnieniem 36 h (timer w workflow Loops albo osobne zdarzenie). SPEC §2 i §7
   trzeba zaktualizować.
2. P2b w dniu 5 zakłada, że każdy nowy użytkownik dostaje 4-dniowy trial przy rejestracji. Jeśli ktoś
   kupi plan w trialu, P2b nadal się zgadza (nie wspomina o planie).
3. Fallback `none` dla tokenu: mail wyjdzie do kontaktu bez tokenu, ale jego kliknięcie nic nie zapisze.
   Warto nadać token wszystkim kontaktom przed włączeniem P7 i P9.
4. Brak provider tokena App Store, więc `ct=<KOD>` nie zmierzy instalacji z iOS.
5. Skrzynki darek@ i monika@ muszą odbierać odpowiedzi, bo prawie każdy mail prosi o "hit reply".
