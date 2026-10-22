# Programy maili Loops: kontrakt wdrożenia (21.10.2026)

Źródło projektu: doc https://claude.ai/artifact/D62cGuX3Muu9SaFFg49ajU i kanwa
https://claude.ai/artifact/CAFirna19ZHZ59J95Yo9b7 (makiety w scratchpadzie sesji, kopia w `mockups/`).
Decyzja operatora (Mikołaj, 21.10): wdrożyć całość end-to-end i włączyć.

## 1. Zasady

- Backend wysyła do Loops **zdarzenia** (`POST /v1/events/send`, z `email` i `userId` = Firebase UID)
  w chwili przejścia stanu. Zero backfillu: nic nie jest wysyłane wstecz dla istniejących kont.
- Każde zdarzenie wysyłane najwyżej raz na (user, event, cycle_key): tabela `email_lifecycle_log`.
- Holdout 10%: `email_holdout = (sha256(user_id) mod 10 == 0)`, stały. Backend wysyła zdarzenie do Loops
  także dla holdoutu (Loops filtruje w workflow), a do PostHog zawsze leci `email_program_entered`
  z `program`, `holdout` (bool). To pozwala porównać powrót w 72 h.
- Nie wysyłamy zdarzeń do kont: usuniętych, bez emaila, z emailem relay Apple bez zgody? (wysyłamy, relay działa),
  kontom testowym z listy `LOOPS_EXCLUDED_EMAILS` (env, CSV), oraz gdy `LOOPS_LIFECYCLE_ENABLED != true`
  (kill switch, domyślnie false w kodzie, true w env produkcji).
- Limit częstotliwości: zdarzenia z dziennych jobów (P6, P9) nie idą, gdy użytkownik dostał inne zdarzenie
  programu w ostatnich 48 h (sprawdzane w `email_lifecycle_log`).
- Prywatność: w zdarzeniach i cechach tylko liczby, enumy, daty, booleany. Zero treści użytkownika.

## 2. Zdarzenia (nazwy stabilne, camelCase jak w Loops)

| Program | Zdarzenie Loops | Kiedy backend je wysyła | eventProperties |
|---|---|---|---|
| P1 Powitanie, P2 Pierwsza wartość | `signupCompleted` | po utworzeniu profilu (koniec rejestracji), raz | `platform` |
| P2 stop | (cecha) `hasFirstConversation=true` | w chwili zakończenia pierwszej rozmowy/Reflect/notatki | - |
| P3a Trial start | `trialStarted` | w chwili przyznania trialu (każde źródło) | `trialDays` (int), `trialEndsAt` (ISO date) |
| P3b Trial koniec | `trialEndingSoon` | job godzinowy: trial kończy się za 20-28 h, użytkownik nie kupił | `reflects`, `agendaItems`, `activeDays` (int, liczone z czasu trialu) |
| P4a Zakup | `subscriptionPurchased` | pierwsza zweryfikowana płatna subskrypcja (nie odnowienie) | `plan` (`monthly`/`yearly`) |
| P5 Rezygnacja | `subscriptionCancelled` | wykrycie wyłączonego auto-renew albo wygaśnięcia płatnej (nie trialu), raz na cykl | `plan` |
| P6a Powrót d14 | `inactive14d` | job dzienny 10:00 UTC: ostatnia **realna** aktywność dokładnie 14 dni temu (okno dnia), użytkownik miał min. 1 aktywność | - |
| P6b Powrót d30 | `inactive30d` | job dzienny: jak wyżej, 30 dni | - |
| P9 Wygaszanie | `repermissionDue` | job dzienny: 90 dni bez aktywności **i** bez kliknięcia w mail (z webhooka), subskrybowany | - |

Kontrola P9: jeśli 14 dni po `repermissionDue` brak odpowiedzi (`email_contact_state.repermission_answer IS NULL`),
job ustawia w Loops `subscribed=false` i zapisuje `repermission_answer='expired'`.

## 3. Cechy kontaktu (real-time, przez `PUT /v1/contacts/update`, oraz w nocnym syncu)

| Cecha | Typ | Znaczenie |
|---|---|---|
| `userId` | string | Firebase UID (już jest) |
| `emailHoldout` | boolean | holdout 10% |
| `hasFirstConversation` | boolean | pierwsza wartość osiągnięta |
| `isPremium` | boolean | aktywna płatna subskrypcja (trial = false) |
| `inTrial` | boolean | trwa trial |
| `emailPref` | string | `all` / `updates_only` / `paused` |
| `emailPausedUntil` | date | koniec pauzy 30 dni z P6a |
| `emailLinkToken` | string | token HMAC do linków akcji (pkt 4), stały per user |

Workflowy w Loops filtrują na starcie: `emailHoldout = false`, `emailPref != paused`.
P7 i P8 (kampanie ręczne) idą do segmentu `Newsletter: subscribed, not holdout, emailPref != paused`.
P7 dodatkowo wyklucza `emailPref = updates_only`.

## 4. Linki akcji w mailach (1 klik, bez logowania)

`GET {PUBLIC_API_BASE_URL}/api/v1/email/a?t={emailLinkToken}&p=<program>&a=<answer>`

- `t` = base64url(HMAC-SHA256(EMAIL_LINK_SECRET, user_id))[:22] + "." + user_id_hash_prefix? Backend decyduje o formacie,
  ale token musi mapować się na usera bez listowania wszystkich (np. `<uid>.<hmac>`; uid to nie sekret, HMAC tak).
- Odpowiedź: prosta strona HTML w stylu maila (Figtree, #bbe4de, karta #f6fffd z ramką #113237), tekst EN:
  "Thanks, got it." i zdanie zależne od akcji. Idempotentne. Zły token = ta sama neutralna strona bez zapisu.
- Dozwolone (p, a):
  - `P4b` × `very`/`somewhat`/`not` (ankieta 14 dni)
  - `P5` × `price`/`not_using`/`missing`/`therapy_ended`/`other` (powód rezygnacji)
  - `P6a` × `pause` (ustawia `emailPref=paused`, `emailPausedUntil=+30 dni`; job zdejmuje pauzę)
  - `P7` × `yes`/`no` (czy numer był przydatny), plus opcjonalny `i=<issue>`
  - `P9` × `keep` (repermission_answer=keep) / `updates` (emailPref=updates_only)
- Każda akcja: PostHog `email_action_clicked` {program, answer, issue?}, zapis w `email_contact_state`.
- Do adresu dodaje się `{emailLinkToken}` jako zmienną LMX kontaktu.

## 5. Webhook Loops → PostHog

`POST /api/v1/webhooks/loops` (bez auth Firebase, podpis Standard Webhooks:
nagłówki `webhook-id`, `webhook-timestamp`, `webhook-signature`, sekret `LOOPS_WEBHOOK_SECRET` w formacie `whsec_...`;
odrzucenie przy złym podpisie albo timestamp starszym niż 5 min; idempotencja po `webhook-id`).

Mapowanie typów Loops na PostHog (distinct_id = userId kontaktu, gdy brak: pomiń PostHog, zaloguj):
`email.delivered`→`email_delivered`, `email.softBounced`→`email_soft_bounced`, `email.hardBounced`→`email_hard_bounced`,
`email.opened`→`email_opened`, `email.clicked`→`email_clicked`, `email.unsubscribed`→`email_unsubscribed`,
`email.spamReported`→`email_spam_reported`, `contact.unsubscribed`→`email_unsubscribed`.
Właściwości: `source_type` (campaign/workflow/transactional), `campaign_id`/`workflow_id`, `email_id`, `program`
(z nazwy workflow/kampanii: prefiks `P1`..`P9`, inaczej `other`). Zero adresów email w PostHog.
`email_clicked` aktualizuje `email_contact_state.last_click_at`. Hard bounce/spam: log + `subscribed=false` nie jest
potrzebne (Loops sam wstrzymuje), tylko zapis stanu.

## 6. Tabele (jedna migracja, idempotentna, kolumny String, bez natywnych enumów)

`email_lifecycle_log`: id (uuid/str pk), user_id (str, index), event_name (str 64), cycle_key (str 64, domyślnie `once`),
sent_at (timestamptz), holdout (bool), loops_ok (bool). UNIQUE(user_id, event_name, cycle_key).

`email_contact_state`: user_id (str pk), last_click_at, last_open_at (timestamptz null),
email_pref (str 16, default 'all'), paused_until (date null), repermission_sent_at, repermission_answer (str 16 null),
last_survey (str 32 null), updated_at.

`loops_webhook_receipts`: webhook_id (str pk), received_at. Czyszczenie >30 dni w jobie dziennym.

## 7. Programy w Loops (workflowy)

Nazwy workflowów zaczynają się od kodu programu (webhook mapuje po prefiksie):

| Workflow | Trigger | Węzły |
|---|---|---|
| `P1 Powitanie` | event `signupCompleted` | filtr start → mail P1 |
| `P2 Pierwsza wartość` | event `signupCompleted` | filtr start → timer 24 h → filtr `hasFirstConversation=false` → mail P2a → timer 48 h → filtr → mail P2b |
| `P3 Trial` start | event `trialStarted` | filtr start → mail P3a |
| `P3 Trial koniec` | event `trialEndingSoon` | filtr start → mail P3b |
| `P4 Po zakupie` | event `subscriptionPurchased` | filtr start → mail P4a → timer 14 dni → filtr `isPremium=true` → mail P4b |
| `P5 Rezygnacja` | event `subscriptionCancelled` | filtr start → timer 1 h → mail P5 |
| `P6 Powrót d14` / `P6 Powrót d30` | `inactive14d` / `inactive30d` | filtr start → mail |
| `P9 Wygaszanie` | event `repermissionDue` | mail P9 (bez filtra emailPref, bo pyta o zgodę) |

Stare automaty do zatrzymania przy włączeniu (pokrywają się): `Onboarding mailing list` (zastępuje P1+P2),
`INACTIVE SURVEY 2 WEEKS` (P6), `No Note Reminder` (P2), `Survey + Calendly` (sprawdzić, czy wciąż potrzebny).
`Freebie PDF delivery` zostaje.

## 8. Zmiany po iteracji 1 (21.10, decyzje leada)

- Harmonogram nowej osoby: P1 dzień 0; P2a +24 h (bez pierwszej rozmowy); P3a ok. 36 h po `trialStarted`
  (połowa 4-dniowego trialu); P3b 24 h przed końcem trialu; P2b dzień 5 (po trialu, nadal bez rozmowy).
- Trial to 4 dni przyznawane przez serwer przy rejestracji, bez automatycznego obciążenia.
- `trialEndingSoon` (jest aktywność, kafelki statystyk) albo `trialEndingSoonQuiet` (zero aktywności, bez kafelków).
  Tylko jedno z nich na trial.
- P5: `subscriptionCancelled` (wyłączone auto-renew, płatne trwa) i `subscriptionExpired` (płatne wygasło).
  Dwa workflowy, te same przyciski powodu (p=P5).
- `emailLinkToken`, `emailHoldout`, `userId` jadą jako cechy kontaktu w każdym wywołaniu zdarzenia; nocny sync
  uzupełnia je wszystkim kontaktom. Fallback w Loops dla `emailLinkToken` = `none` (neutralna strona).
- Stopka kryzysowa: "MindSync isn't a crisis service. If you're in crisis, call or text 988 in the US, or find a local
  helpline at findahelpline.com." na wszystkich mailach poza P8.
