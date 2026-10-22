# Loops: budowa programów P1-P9 (21.10.2026)

Zbudowane przez Loops API (MCP) jako szkice. Nic nie zostało uruchomione, opublikowane ani wysłane:
zero podglądów, zero zdarzeń, zero startów workflow, kampania P7 w Draft. Istniejących workflowów
(Onboarding mailing list, INACTIVE SURVEY 2 WEEKS, No Note Reminder, Survey + Calendly, Freebie,
Premium trial ending, First-value activation, Win-back ladder) nie ruszałem. Pełna mapa ID: `loops-build.json`.

## Co zrobione

- **Cechy kontaktu** (nowe, custom): `emailHoldout` (boolean), `hasFirstConversation` (boolean),
  `isPremium` (boolean), `inTrial` (boolean), `emailPref` (string), `emailPausedUntil` (date),
  `emailLinkToken` (string). Istniejące (np. `is_premium`) bez zmian.
- **Grupa workflowów** "Lifecycle 2026-10" (`cmviie18501du0j0kk4tqrkaq`).
- **11 workflowów w Draft**, bez listy mailingowej (tak jak "Onboarding mailing list", który też ma `mailingListId = null`).
  Każdy ma EventTrigger po nazwie zdarzenia i filtr startowy z `appliesDownstream = true`:
  `emailHoldout isFalse AND emailPref notEquals "paused"` (P9 tylko `emailHoldout isFalse`).

| Kod | Workflow | Trigger (reEligible) | Ścieżka |
|---|---|---|---|
| P1 | [P1 Powitanie](https://app.loops.so/workflows/cmviie4cr01cg0jyzusbblift) | signupCompleted (nie) | filtr → P1 |
| P2 | [P2 Pierwsza wartość](https://app.loops.so/workflows/cmviihkov01co0jyznwz7n3ui) | signupCompleted (nie) | filtr → 24 h → hasFirstConversation false → P2a → 96 h → hasFirstConversation false → P2b |
| P3a | [P3a Trial połowa](https://app.loops.so/workflows/cmviihkx301gg0jzl5gsmkfw6) | trialStarted (nie) | filtr → 48 h → inTrial true i isPremium false → P3a |
| P3b | [P3b Trial koniec](https://app.loops.so/workflows/cmviihl5901db0jxcv9yqq84h) | trialEndingSoon (nie) | filtr → P3b |
| P3b-quiet | [P3b Trial koniec (cisza)](https://app.loops.so/workflows/cmviihldt00on0jwu3zfzpket) | trialEndingSoonQuiet (nie) | filtr → P3b-quiet |
| P4 | [P4 Po zakupie](https://app.loops.so/workflows/cmviihllb01cp0kzcihpcolms) | subscriptionPurchased (nie) | filtr → P4a → 14 dni → isPremium true → P4b |
| P5 | [P5 Rezygnacja](https://app.loops.so/workflows/cmviihlt600np0j14gd49pv3o) | subscriptionCancelled (nie) | filtr → 1 h → P5 |
| P5-expired | [P5 Wygaśnięcie](https://app.loops.so/workflows/cmviihm0s01di0jyih1q5l909) | subscriptionExpired (nie) | filtr → 1 h → P5-expired |
| P6a | [P6a Powrót d14](https://app.loops.so/workflows/cmviihmd801fj0jxgl8f1uqfo) | inactive14d (tak) | filtr → P6a |
| P6b | [P6b Powrót d30](https://app.loops.so/workflows/cmviihmnj00o90jxi7uq1nv2l) | inactive30d (tak) | filtr → P6b |
| P9 | [P9 Wygaszanie](https://app.loops.so/workflows/cmviihmuz01ge0j08aphr8ckm) | repermissionDue (nie) | filtr (tylko holdout) → P9 |

- **13 maili workflowów**: temat, preview, nadawca "Darek from MindSync" `darek@`, reply-to `darek@mindsync.app`,
  treść LMX z szablonu domowego (theme `cmkn0tkkw0opg0i2ftjg46o8d`, grafiki nagłówka, divider, latarnia,
  pasek ikon, pigułki, przyciski i stopka jak w mailu z 21.10) plus linia kryzysowa (mała, wyśrodkowana) przed ©.
  Tekst 1:1 z `copy/*.json`, bez przeróbek. Zgodność treści w Loops z plikami sprawdzona skryptem (GET po zapisie).
- **Fallbacki ustawione przez API**: P1 `firstName = there`; P3b `reflects = 0`, `agendaItems = 0`, `activeDays = 1`
  (zdarzenie); P4b, P5, P5-expired, P6a, P9, P7 `emailLinkToken = none`.
- **Guardian**: 14/14 maili (13 workflow + P7) bez błędów i bez ostrzeżeń.
- **P7**: kampania [P7 Newsletter Moniki: szablon](https://app.loops.so/campaigns/cmviirg9i003q0j4hte30s3rs) w Draft,
  nadawca "Monika from MindSync" `monika@`, reply-to `monika@mindsync.app`, szablon z placeholderami `[...]`,
  bez odbiorców i bez harmonogramu.
- **Segment** "Newsletter: subscribed, not holdout, not paused" (`cmviisfax00590j3tlfimjumo`):
  `emailHoldout isFalse AND emailPref notEquals "paused"`.

## Co się nie udało / odstępstwa

- Nic nie zostało odrzucone. Wszystkie 10 wzorców zdarzeń przyjęło EventTrigger po nazwie.
- `languageCode` odrzucony ("Translations are not enabled for this team"), więc go nie wysyłam; maile i tak mają `en`.
- Kafelki statystyk w P3b nie są siatką 3 kolumn jak w makiecie: LMX nie ma kolumn, więc to trzy kolorowe
  bloki jeden pod drugim (liczba H2 + etykieta, kolory #ff9f8a, #ffc88a, #DBF0ED). Loops usunął `paddingTop="0"` (kosmetyka).
- Przycisk "mint-outline" (I FINISHED THERAPY, NOT NOW, PAUSE EMAILS...) ma tło #DBF0ED, ale bez ramki 2 px #113237
  z makiety, bo nie znam atrybutu ramki przycisku w LMX.
- Segment nie ma warunku "subscribed": Loops wysyła kampanie tylko do zapisanych kontaktów, więc nie dodawałem go.

## Do zrobienia w panelu / przez leada

1. **Przejrzeć wygląd** każdego maila w edytorze (szczególnie kafelki P3b i przyciski mint-outline; ewentualnie dodać ramkę ręcznie).
2. **Start workflowów** dopiero po wdrożeniu backendu (zdarzenia + cechy) i wyłączeniu starych automatów z SPEC §7.
3. **Wartości boolean muszą być jawne.** Filtry używają `isFalse` / `isTrue`. Nie sprawdzałem, jak Loops traktuje
   cechę pustą (nieustawioną) przy `isFalse`. Backend powinien w każdym wywołaniu zdarzenia ustawiać
   `emailHoldout`, `hasFirstConversation`, `isPremium`, `inTrial` na true/false, nie zostawiać pustych;
   inaczej kontakt może nie przejść filtra i mail nie wyjdzie.
4. **P5 i P5-expired mają reEligible = false**, czyli każdy dostaje każdy z tych maili najwyżej raz w życiu konta.
   Jeśli ankieta ma iść raz na cykl subskrypcji (SPEC §1), przestawić na reEligible = true i oprzeć się na
   deduplikacji w `email_lifecycle_log`. Zalecenie BVM nr 3 (P5-expired tylko, gdy w cyklu nie poszło P5)
   nie jest zrobione w Loops; najprościej załatwić to w backendzie (nie wysyłać `subscriptionExpired`, gdy w tym cyklu poszło `subscriptionCancelled`).
5. **P7 przed każdym wydaniem**: wypełnić placeholdery, `[issue-slug]` w obu linkach, podmienić zrzut, ustawić
   odbiorców (segment wyżej) i dodatkowo wykluczyć `emailPref = updates_only`, ustawić harmonogram.
   Kampania pokazuje domyślne `scheduling: now`, ale jest w Draft i nic nie wysyła, dopóki ktoś jej nie wyśle.
6. **P8** (kampania o nowościach) nie była w zakresie; używa tego samego segmentu.
7. Backend (z werdyktu BVM nr 2): P9 `a=updates` musi też ustawiać `repermission_answer`, inaczej job wypisze kontakt po 14 dniach.
8. Test: wysłać podgląd każdego maila na własny adres z panelu (ja nie wysyłałem żadnych podglądów).

Źródło LMX: generator w scratchpadzie sesji (`loops_build/gen_lmx.py`) czyta `copy/*.json` i składa bloki
według `email/2026-10-23-new-look/email.lmx`.
