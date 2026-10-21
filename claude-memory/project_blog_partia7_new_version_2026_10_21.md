---
name: project-blog-partia7-new-version-2026-10-21
description: "Blog pod nową wersję apki 21.10: nowy wpis whats-new-in-mindsync (gotowy, czeka na drip/operatora), how-to-use przepisany NA ŻYWO, 35 wpisów z nowymi zrzutami, tryb -Republish w publikatorze"
metadata:
  node_type: memory
  type: project
  originSessionId: db1e99c7-e101-428c-8d00-812c9a1c6024
  modified: 2026-10-21T11:24:50.182Z
---

21.10 operator: "zrób end2end" (nowy wpis o zmianach + przepisanie how-to-use + nowe zrzuty na blogu).

- Zrzuty: nowe slajdy sklepowe (store/out/appstore, styl starych) -> blog/images/app-screenshots-v2/app-ios-v2-*.webp, wgrane do Webflow (mapa _webflow-urls.json). Katalog blog/app-features.json: 6 starych URL podmienione + main-home, character; nowe id main-home, first-week-plan, first-conversation, orca-memory, character, habits; nazwy kart: "Before therapy card", "After therapy card", "Focus Areas check-ins", "Personal Bio". 35 opublikowanych wpisów odświeżonych LIVE (-Republish -BodyOnly), 0 błędów; przy okazji weszło 11 zaległych linków LINK-LATER.
- Timeline w sklepie (build 2.0.117+190) ma filtry A3 v2 (zawijane pigułki, cae29d8), NIE jeden rząd. Shot store_timeline przerenderowany na lokalnym froncie feat/store-shots-a3v2 (commit f554c83, niewypchnięty), store/renders + store/out/*/07-timeline zaktualizowane, IG 2026-10-21 slajd 5 i mail też.
- Publikator: scripts/webflow/blog-publish.ps1 ma -Republish (-Plik/-All, -BodyOnly, -KeepHero) i -UploadAssets, DryRun domyślnie; opis w scripts/webflow/README.md.
- how-to-use-mindsync v2 NA ŻYWO 21.10 (lastPublished 11:02 UTC), kopia starej: blog/queue/_backup-2026-08-25_how-to-use-mindsync.pre-v2.json. Link do nowego wpisu jako [LINK-LATER: whats-new-in-mindsync], dziś renderowany jako sam tekst.
- whats-new-in-mindsync: NA ŻYWO 21.10 (operator uruchomił publikację sam, bo klasyfikator auto mode blokuje Create Public Surface; komenda z otwartej sesji PS przez `& .\scripts\webflow\blog-publish.ps1 ... -DryRun:$false`, NIE `powershell -File`, bo -File robi z $false string). Link w how-to-use działa (sprawdzone curlem).

**Why:** blog opisywał starą apkę (five tabs, big button) i pokazywał sierpniowe zrzuty.
**How to apply:** po publikacji whats-new odśwież body how-to-use (`blog-publish.ps1 -Republish -Plik 2026-08-25_how-to-use-mindsync.json -BodyOnly -DryRun:$false`), żeby LINK-LATER stał się linkiem. Przy kolejnej zmianie UI: harness store_* -> render_store.py -> webp v3 -> -UploadAssets -> katalog -> -Republish -All -BodyOnly. Powiązane: [[project-store-screenshots-2026-10-19]], [[project-email-new-look-2026-10-21]].
