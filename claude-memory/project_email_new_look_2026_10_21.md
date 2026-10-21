---
name: project-email-new-look-2026-10-21
description: "Mail Loops o nowej wersji (2.0.56): analiza 33 wysyłek, projekt na kanwie, plan czw 23.10 23:30 UTC; czeka na akcept operatora, w Loops nic nie założone"
metadata:
  node_type: memory
  type: project
  originSessionId: db1e99c7-e101-428c-8d00-812c9a1c6024
  modified: 2026-10-21T11:24:47.820Z
---

21.10 operator: "najpierw sprawdź co było wysyłane i jak, potem /design nowy mail z treścią i plan wysyłki zgodny z poprzednimi". Loops MCP podłączony przez operatora (OAuth, team cmbhkwdyy14eeyc0hgckxd10a).

- Analiza: 71 kampanii, 33 wysłane; od kwietnia co tydzień newsletter Moniki + aktualizacje "This Month In MindSync"; ostatnia wysyłka 24.09. Średnio 10,0% otwarć, 0,22% kliknięć, 5,1% soft bounce (80-90 adresów stale), 0,15% wypisów. Najlepsza duża aktualizacja 3.2 (27.07): 12,9%.
- Jak: from MindSync monika@mindsync.app, reply-to monika@, temat od 🐋, preview pusty w 32/33, cała lista zapisanych (filtr userGroup contains ""), czw/pt 23:30 UTC, motyw "MindSync - mother template" (cmkn0tkkw0opg0i2ftjg46o8d), układ 3.2 (nagłówek z orką, pigułki, stopka z latarnią + ikony).
- Kanwa: https://claude.ai/artifact/PTC1STNoRFYa87Kfu6cYsX (analiza, makieta 1:1, plan). Treść: blog-writer + humanizer, BVM AKCEPT WARUNKOWY (reply-to, Android 100%, cta_buttons zamiast cta_button). Pliki: `email/2026-10-23-new-look/` (copy.json, img/ 4 kompozyty z prawdziwych ekranów, makieta, metryki).
- Plan: kampania "Newsletter: Feature Update new look" w grupie 3.2 (cmoh8ka8001pd0i2zwpmjxb6i), czw 23.10 23:30 UTC, linki do sklepów oznaczone (ct=email-new-look, utm_source=email). Publikację klika operator w panelu (API nie ma publish).

- 21.10 operator: treść skrócona do ok. 334 słów (BVM AKCEPT WARUNKOWY), nadawca i reply-to darek@mindsync.app, podpis "Darek from MindSync", sekcja "Rate us on Google Play and the App Store. It really helps us do better." z dwoma przyciskami (Play showAllReviews, App Store action=write-review). Źródło: email/2026-10-23-new-look/copy.json (pola sender, rate_line, rate_buttons).

- 21.10 ~11:00 UTC operator zatwierdził i kazał wysłać DZIŚ 23:30 UTC. Szkic w Loops: kampania cmvhzynzl04l40jzvlkwuajng (https://app.loops.so/campaigns/cmvhzynzl04l40jzvlkwuajng), email message cmvhzynzq04l50jzvmbo35p82, grupa 3.2, filtr userGroup contains "", scheduling 2026-10-21T23:30Z, from MindSync darek@, reply-to darek@mindsync.app, 4 obrazki wgrane do Loops (images.vialoops.com/.../cmvhzw*.jpg), Guardian 0/0, preview wysłany na skrzynkę operatora. Operator kliknął Schedule 21.10 11:21 UTC: status Scheduled potwierdzony przez API (wysyłka 2026-10-21T23:30Z). LMX: email/2026-10-23-new-look/email.lmx. Po 48 h: metryki vs baza (otwarcia 10%, kliknięcia 0,22%).

**Why:** Loops przez API robi tylko szkic; masowa wysyłka do ~1730 realnych osób wymaga akceptu.
**How to apply:** po akcepcie: create campaign + upload 4 obrazków + LMX w stylu 3.2 (theme id) + Guardian + preview na skrzynkę operatora; nie wysyłać. Powiązane: [[reference-loops-access-2026-10-21]].
