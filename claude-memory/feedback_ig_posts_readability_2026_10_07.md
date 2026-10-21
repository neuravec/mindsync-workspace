---
name: feedback-ig-posts-readability-2026-10-07
description: "Operator dostał negatywny feedback \"nie da się tego czytać\" o postach IG z 5-6.10; humanizer i brand-voice przeszły, ale nikt nie sprawdza zrozumiałości"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c5c34d6b-7dc4-456e-ba0f-e1f87f029347
  modified: 2026-10-07T12:35:13.845Z
---

Posty IG z 5.10 (story before-your-session) i 6.10 (karuzela forget-half-your-session) dostały negatywny feedback: "nie da się tego czytać". Oba przeszły humanizer (wywołany przez samego social-content-writera) i akcept brand-voice-manager z re-checkiem, więc proces był formalnie zachowany.

**Why:** bramki mierzą co innego niż zrozumiałość. Humanizer usuwa wzorce AI i pcha w krótkie, hasłowe fragmenty; checklista §9 w social/brand-instagram.md nie ma kryterium "zrozumiałe przy pierwszym czytaniu, bez kontekstu". Limity znaków na slajdach i poprawki pod błąd renderu (okładka skrócona do "Tuesday: therapy. Thursday: blank?") dodatkowo kompresowały tekst w zagadki.

**How to apply:** przy każdej partii IG tekst slajdów musi przejść test zimnego czytania (ktoś bez kontekstu streszcza slajd; rozjazd = poprawka), pełne zdania zamiast aforyzmów, bez metafor do rozszyfrowania i zaimków odsyłających do innych slajdów. Słów nie zmieniamy pod błąd szablonu, naprawiamy szablon. Powiązane: [[feedback-myslniki-total-ban-i-humanizer-fork]], [[project-instagram-automation-2026-10-01]].

Stan 2026-10-07 (wdrożone): krok 3b „test zimnego czytania" w skillu social-write, sekcja „Czytelność przed stylem" w .claude/agents/social-content-writer.md, twardy punkt Czytelność w §9 social/brand-instagram.md, fix bold.js (interpunkcja sklejona z akcentem). Przepisane i zaakceptowane: beyond-fine (07.10), people-pleasing (08.10), worse-after-therapy (10.10), sunday-scaries (11.10), status gotowy. Posty o Orce (13 i 15.10) przepisane, ale szkic do wydania w sklepach i polityki prywatności; przed `gotowy` potrzebny akcept brand-voice.
