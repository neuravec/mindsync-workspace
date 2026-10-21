---
name: feedback-claim-not-verified-until-state-reproduced
description: Twierdzenie o bezpieczenstwie wdrozenia jest niezweryfikowane, dopoki ktos fizycznie nie odtworzyl stanu, ktorego dotyczy
metadata:
  type: feedback
---

W batchu Reflect entry (2026-09-17/18) zapewnilem operatora, ze okno miedzy pushem a reczna migracja jest
bezpieczne. Podstawa byl odczyt deklaracji w modelu i komentarza w migracji. Teza byla falszywa i groziala
wylaczeniem zakladania rozmow w calej aplikacji. Szczegoly techniczne:
[[reference-orm-deferred-does-not-protect-insert]].

**Why:** przeczytanie deklaracji mowi, co autor zamierzal, a nie co system robi. Komentarz opisujacy
wlasnosc bezpieczenstwa jest gorszy niz jego brak, bo nastepna osoba mu zaufa. Trzy zadania implementacyjne
przepuscily ten blad, bo kazde czytalo ten sam komentarz.

**How to apply:** zanim potwierdzisz operatorowi bezpieczenstwo wdrozenia, odtworz stan. Dla okna
migracyjnego znaczy to: usun kolumny z bazy i przepusc prawdziwe trasy, a nie skompiluj zapytanie.
Dla poprawki nawigacji: wylacz poprawke i sprawdz, czy test czerwienieje. Dla straznika prywatnosci:
wstrzyknij wyciek i sprawdz, czy pakiet pada. Agenci w tym projekcie robia to dobrze, kiedy sie im to
jawnie zleci ("udowodnij mutacja"), i pomijaja, kiedy sie nie zleci.

Druga rzecz z tego samego batcha: przy dlugim batchu zamrazaj repo przed bramka weryfikacyjna. Audytorowi
wjechaly dwa commity w trakcie przebiegu i musial odrzucic wyniki. Slusznie to zglosil.
