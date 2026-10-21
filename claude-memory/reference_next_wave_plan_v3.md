---
name: MindSync Next Wave — zatwierdzony plan funkcji WOW
description: Plan v3 zatwierdzony przez devil's advocate (2026-04-21) po 2 iteracjach. 5 funkcji + PR #0 foundation + 2 deferred do Q3.
type: project
originSessionId: 6edfa719-e437-4c95-9e02-54b8bc777ca9
---
Plan wygenerowany z brainstormu 5 agentów (ui-ux, data-analytics, flutter-mobile, backend-api, integration-devops), przeszedł 3 rundy devil's advocate review.

**Why:** user poprosił o orchestrowany brainstorm z DA-gate. v1 miał 4 CRIT + 5 HIGH (notification fatigue, duplikaty z istniejącymi funkcjami, halucynacje listu), v2 conditional approval z 7 warunków, v3 final approval bez warunków.

**How to apply:** Gdy user wraca do tych funkcji w przyszłych rozmowach — to jest zatwierdzone acceptance criteria. NIE zaczynać od zera.

## Sekwencja wdrożenia

**PR #0 MUST SHIP FIRST** — `user_notification_budget` (daily cap 4, weekly cap 14 respektujący user week_start_day). Helper `can_send_notification(user_id, priority)` retrofituje WSZYSTKIE 13 istniejących FCM call-sites + wszystkie przyszłe. Priority queue z bypass dla IMMEDIATE_USER_SCHEDULED (future letters). Owner: backend-api.

**Wave 1 — Merged Extensions (nie nowe funkcje, rozszerzenia istniejących)**
- 1.1 **Moment of Clarity** = 3rd nudge w `post_session_nudges` (delay 24-30h, mutex z followup). Free. Owner: data-analytics + backend-api.
- 1.2 **Delta Severity Push** = kolumna `delta_severity` w `therapy_tracking_signals`, push tylko przy spike green/amber→red AND ≥21 distinct days activity w 30d window. Free. Owner: data-analytics.
- 1.3 **Long-term Clusters** = kolumna `long_term_clusters` w `period_snapshots` 90d (k-means deterministic na 12m RAG embeddings, top-3 z citations, GPT-4o-mini włącza w existing narrative). Free. Owner: data-analytics.

**Wave 2 — Nowe funkcje z safeguards**
- 2.1 **Letter From Future/Past Self (Premium, raz/miesiąc)**:
  - Future: nowa tabela `scheduled_future_letters` z FK CASCADE, hourly worker z `FOR UPDATE SKIP LOCKED` + `delivery_attempt_started_at` 10min reservation TTL (idempotency). Azure Blob z lifecycle auto-delete 30d po delivery. Priority IMMEDIATE_USER_SCHEDULED bypassuje budget.
  - Past: GPT-4o + RAG top-10, validation pipeline (regex quote extract + cosine 0.85 vs RAG source OR substring, max 3 regen, `quality_issue=true` jeśli fail). Admin review dashboard pierwszy miesiąc — **owner: integration-devops, SLA <24h, Slack alert >10, auto-reject 48h**. UX disclaimer "ćwiczenie wyobraźni" + flag-wrong button.
  - Owners: backend-api (schema + worker), data-analytics (validation), security-guardian (pre-launch), ui-ux-designer (disclaimer).
- 2.2 **Relationship Map (Premium)**:
  - Extraction GPT-4.1-mini function calling na new AND updated debrief z 5-min debounce + DELETE before INSERT per debrief_id.
  - Tabele `relationship_mentions` + `relationship_aliases` z FK CASCADE ON DELETE.
  - Dedupe: `normalized_hash` (plain SHA-256 lowercased) kolumny dla O(1) equality lookup. `all_variant_hashes` plain JSON. Levenshtein ≤2 tylko na pre-filtered soundex candidates w Pythonie.
  - UI: brak numerical sentiment — tylko kolory + narrative. Flutter confirm UI "Czy to ta sama osoba?" przed auto-merge.
  - Owners: data-analytics (extraction), backend-api (tabele + dedupe endpoint), flutter-mobile (confirm UI).

**Q3 Deferred (blokery pre-work)**
- HealthKit/Health Connect: blocked on BAA/DPA z Azure OpenAI dla health data (GDPR Art. 9), korelacja bez GPT, dedicated consent, security-guardian approval. Owners: integration-devops + security-guardian.
- Home Screen Widget: blocked on ui-ux-designer frozen-frame orca design (9 PNGs: 3 stages × 3 happiness). iOS-first MVP. Owners: ui-ux-designer → flutter-mobile.

## Cross-cutting rules (WSZYSTKIE nowe funkcje)
- i18n: AI teksty w user `ai_language`, fallback EN
- `data_hash` cache na każdej AI funkcji
- RAG indexing: past letters (post-approval), long-term clusters. NIE: future letters, moment_of_clarity (ephemeral)
- GDPR CASCADE na wszystkich user_id FK
- Sequencing: PR #0 deploy+verify → Wave 1 serial (1.1→1.2→1.3) → Wave 2 parallel (2.1+2.2)

## Odrzucone z v1 (nie wracać do nich bez nowego uzasadnienia)
- Separate Drift Alert system (duplikuje therapy_tracking_signal)
- Separate Moment of Clarity push (duplikuje post_session follow-up)
- Separate Echo Patterns table (duplikuje period_snapshots)
- Home Widget z animowaną orką (mismatch z CustomPainter — statyczny PNG zawsze będzie wyglądał źle)
