---
name: project-reflect-entry-batch-2026-09-18
description: Ekran wyboru trybu Reflect (glos/tekst) wdrozony; BE v550 zmigrowany na prodzie, FE na dev; otwarte device-QA i dwa pilne tickety
metadata:
  type: project
---

Batch "Reflect entry" WDROZONY 2026-09-18. Backend: 7 commitow, `origin/main` na `b189514`, Heroku **v550**,
migracja **m314b2c3d4e5** uruchomiona i zweryfikowana na prodzie (3 kolumny obecne, 1771 rozmow nietknietych,
0 z modalnoscia bo zero tur od deployu). Front: 9 commitow, `origin/dev` na `81773ba`, po rebasie na commit
bota Codemagic. Plan i macierz 34 przypadkow: `TASKS-reflect-entry.md` w katalogu Heroku.

**Co zmienia dla uzytkownika:** wejscie w nowa rozmowe Reflect prowadzi przez pelnoekranowy wybor glos/tekst
plus sheet z 3 tematami z kontekstu terapii. Glos ma klodke dla nie-premium i prowadzi prosto na paywall.
Kontynuacja omija wybor i wraca do trybu zapisanego w `conversations.modality`; watek z pustym modality
(kazdy historyczny) pyta o tryb raz i sam sie leczy po pierwszej turze. Ikonka telefonu i automatyczne chipy
znikly z czatu. Agent odzywa sie pierwszy po wybraniu tematu.

**Decyzje operatora:** klodka plus paywall od razu; wiersze sheeta to tematy z kart terapii (nie watki Reflect);
agent otwiera pytaniem; puste modality pyta o tryb; sesja analityczna NIE zamyka sie przy blokadzie ekranu
w trakcie rozmowy glosowej (nowy `end_reason` = `voice_interrupted`).

**OTWARTE, wymaga operatora:**
- Device QA: gest cofania na Androidzie 14+ (predictive back) na ekranie glosowym i wyboru. Testy pokrywaja
  kanal przycisku wstecz, nie gest. Tryb bledu, ktory to naprawialo, to kasowanie rozmowy w trakcie mowienia.
- Device QA: sciezka pustego modality wymaga konta z watkami sprzed migracji, na swiezej instalacji jest
  nieosiagalna.
- `voice_interrupted` to nowa wartosc `end_reason`. Insighty w PostHogu, ktore wyliczaja wartosci zamiast
  grupowac, po cichu ja zgubia.

**Dwa pilne tickety obok tej funkcji:**
1. `POST /api/v1/audio-v2/realtime-session` mintuje klucz OpenAI BEZ sprawdzenia premium. Zastane. Obejscie
   platnego uprawnienia, przez ktore nowa klodka jest w czesci dekoracja.
2. Blok voice-directora w `send_reflect_message` (~linia 932): brak `db.rollback()` przed commitem handlera,
   ostatnie realnie osiagalne 500 w `reflect.py`. Wymaga wlasnego QA (Redis + kilka tabel + flaga DIRECTOR_ENABLED).

Baseline testow po batchu: backend **9** zastanych failujacych (bylo 14, piec martwych testow RAG ozywionych
w b189514). Front: 30 zastanych, wszystkie poza obszarem tej funkcji.
