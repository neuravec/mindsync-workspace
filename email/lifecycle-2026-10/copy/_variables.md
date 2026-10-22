# Zmienne Loops w mailach P1-P9 (sprawdzone 21.10.2026)

Źródła: https://loops.so/docs/creating-emails/lmx, https://loops.so/docs/creating-emails/personalizing-emails,
https://loops.so/docs/events/properties (pobrane 21.10.2026).

## Dwie składnie, zależnie od tego, gdzie budujemy mail

| Co | LMX (budowa przez API / plik .lmx) | Edytor Loops (ręcznie w panelu) |
|---|---|---|
| Cecha kontaktu | `{contact.firstName}`, `{contact.emailLinkToken}` | `{firstName}`, `{emailLinkToken}` |
| Właściwość zdarzenia | `{event.reflects}`, `{event.trialDays}` | `{EVENT_PROPERTY:reflects}` |
| Zmienna transakcyjna | `{data.resetLink}` | `{DATA_VARIABLE:resetLink}` |

Pliki `copy/*.json` używają składni **LMX** (`{contact.x}`, `{event.x}`), bo tak zbudowano P8
(`email/2026-10-23-new-look/email.lmx`). W LMX forma bez prefiksu (`{firstName}`) oraz
`{EVENT_PROPERTY:...}` są **nieprawidłowe**. Przy budowie w edytorze trzeba przepisać na kolumnę po prawej.

## Zasady, które wpływają na treść

- **Brak wartości = mail się nie wysyła** (personalizing-emails: "the email will not be sent"), chyba że
  ustawimy fallback. W LMX nie ma fallbacku w tekście (`{contact.firstName|there}` jest nieprawidłowe);
  fallback ustawia się w panelu edytora albo przez `eventPropertiesFallbacks` w Content API.
- Właściwości zdarzeń działają **tylko w mailach workflowów** (nie w kampaniach). Muszą być wcześniej
  dodane w Loops i Loops musi dostać choć jedno zdarzenie z nimi, zanim pojawią się w edytorze.
- Nazwy są case-sensitive i muszą się zgadzać z API name (SPEC §2: `reflects`, `agendaItems`, `activeDays`,
  `trialDays`, `trialEndsAt`, `plan`, `platform`).
- `{event.trialDays}` nie jest już używany w żadnym mailu (decyzja leada: zero liczby dni w tematach, w treści "your trial").
- Zmienne działają w `href` przycisków i linków (`<Button href="https://...{contact.userId}">`), wpisane ręcznie.
- Link wypisu dokleja Loops sam w stopce, nie dodajemy go do treści.
- W atrybutach LMX `&` w URL zapisujemy jako `&amp;` (tak jak w P8). W JSON-ach jest surowe `&`.

## Użyte zmienne i wymagane fallbacki

| Mail | Zmienna | Typ | Fallback do ustawienia | Uwagi |
|---|---|---|---|---|
| P1 | `{contact.firstName}` | cecha | `there` | bez fallbacku mail nie wyjdzie do kont bez imienia |
| P3b | `{event.reflects}` | zdarzenie | `0` | kafelek statystyk |
| P3b | `{event.agendaItems}` | zdarzenie | `0` | kafelek statystyk |
| P3b | `{event.activeDays}` | zdarzenie | `1` | kafelek statystyk |
| P4b, P5, P5-expired, P6a, P7, P9 | `{contact.emailLinkToken}` | cecha | `none` | decyzja leada 21.10: fallback `none`, backend pokazuje dla niego neutralną stronę bez zapisu. Mail wychodzi także do kontaktu bez tokenu, ale kliknięcie nic nie zapisze |

## Szablon linku akcji

```
https://mindsync-829f3f05ed43.herokuapp.com/api/v1/email/a?t={contact.emailLinkToken}&p=<KOD>&a=<odpowiedź>
```

P7 dodatkowo `&i=<issue-slug>`. Dozwolone pary (p, a) zgodnie ze SPEC §4:
P4b very/somewhat/not; P5 price/not_using/missing/therapy_ended/other; P6a pause; P7 yes/no; P9 keep/updates.
