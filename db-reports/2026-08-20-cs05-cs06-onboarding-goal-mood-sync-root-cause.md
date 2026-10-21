# CS-05 + CS-06 root-cause check: onboarding → Goals / Mood Trend sync (MSV3.4 Fix.1)

**Date:** 2026-08-20 · **Agent:** database-administrator · **Access:** Heroku one-off dyno (`heroku run --no-tty -a mindsync python`), read-only, `SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY`, zero writes.

**Deployed code verified:** local `MindSync` HEAD `a817b772` = Heroku `v542` (current release, confirmed via `heroku releases -a mindsync`). `4bb9b2c` (CS-01 goal sync, shipped 2026-08-15) is an ancestor of HEAD, so the code read locally (`app/api/v1/endpoints/users.py:1206-1289`, `app/crud/crud.py::sync_goals_from_onboarding`, `::sync_symptoms_from_onboarding`, `::create_goal`, `::get_user_symptoms`) is exactly what is live. Alembic head on prod: `pp7q8r9s0t1u` (matches memory). Schema for `user_therapy_context`, `user_goals`, `user_symptoms`, `symptom_scores` matches `models.py` — no drift found on these four tables.

## Method

Per-account identity (Firebase UID) is never printed. Accounts are referenced only by `user_therapy_context.id` (an internal surrogate row id, not the account's identity) — "ctx-label". No goal/focus-area text was read into any output; only presence/absence, counts, timestamps, and boolean flags.

**Candidate set:** the 60 most-recently-*updated* `user_therapy_context` rows with non-empty `goals_text` (for CS-05), and separately the 60 most-recently-updated rows with a non-empty `focus_areas` JSON array (for CS-06). I could not identify a single "operator's account" from data alone (no email/name field ties to Firebase UID) — per instructions I did not guess one. One row did surface as a very likely match by pattern (see CS-06 §3) and is flagged as an inference, not a fact.

Queries (paraphrased, full runnable scripts left in scratchpad, not committed):
```sql
-- candidate accounts (goals)
SELECT ctx.id, ctx.user_id, ctx.created_at, ctx.updated_at, length(ctx.goals_text)
FROM user_therapy_context ctx
WHERE ctx.goals_text IS NOT NULL AND trim(ctx.goals_text) <> ''
ORDER BY ctx.updated_at DESC LIMIT 60;

-- per-account goal counts
SELECT user_id, count(*) FILTER (WHERE status='ACTIVE') AS active_ct, count(*) AS total_ct
FROM user_goals WHERE user_id IN (...) GROUP BY user_id;

-- active goals ordered as the Workspace Goals module would sort them (display_order ASC, take(3))
SELECT user_id, id, display_order, created_at FROM user_goals
WHERE user_id IN (...) AND status='ACTIVE' ORDER BY user_id, display_order ASC;

-- candidate accounts (focus areas) + symptom match
SELECT ctx.id, ctx.user_id, ctx.focus_areas, ctx.severity_ratings, ctx.updated_at
FROM user_therapy_context ctx
WHERE ctx.focus_areas IS NOT NULL AND trim(ctx.focus_areas) <> '' AND trim(ctx.focus_areas) <> '[]'
  AND ctx.focus_areas LIKE '[%'
ORDER BY ctx.updated_at DESC LIMIT 60;

SELECT user_id, name, is_visible FROM user_symptoms WHERE user_id IN (...);
SELECT us.user_id, us.name, count(ss.id) FROM user_symptoms us
LEFT JOIN symptom_scores ss ON ss.symptom_id = us.id
WHERE us.user_id IN (...) GROUP BY us.user_id, us.name;
```
Focus-area names were parsed client-side (Python, from `focus_areas` JSON) only to compare against `user_symptoms.name` and were never printed.

---

## CS-05 — Goal sync results

| Metric | Result |
|---|---|
| Candidate accounts (non-empty `goals_text`, all-time) | 60 |
| Accounts with **zero** `user_goals` rows despite `goals_text` set | **6 / 60 (10%)** |
| ...of which updated **after** CS-01 shipped (2026-08-15) | **0 / 6** — all 6 are Feb–Mar 2026, i.e. predate the goal-sync feature entirely |
| Accounts where newest active goal's `display_order` rank falls **outside the top 3** (invisible under the Workspace Goals `take(3)`) | **2 / 60 (3.3%)** |
| Accounts with ≥1 goal AND newest goal ranked **within** top 3 (structurally visible) | 52 / 60 (86.7%) |

**Interpretation:**
- **Mechanism 3 (poisoned session / silent 200, no rollback) — not observed firing on goals in this sample.** Every zero-goal-row account is from before the sync code existed (`4bb9b2c`, 2026-08-15); there is no post-deploy case of "`goals_text` set, zero goals created." This doesn't rule the bug out (it's a session-handling race that wouldn't be visible in every account), but the data gives no positive evidence for it on the goal side, across the most recent 60 goal-bearing accounts.
- **Mechanism 1 (created but buried past `take(3)`) — confirmed, but narrow.** It requires the account to already have 3+ active goals before the onboarding-sync appends one more (append-only, `display_order = max+1`, per `crud.py:5419-5422`). Only 2 of 60 accounts meet that precondition in this sample — which is exactly why it's rare in the general population but *exactly* Darek's repro steps (Reset Onboarding on an account that already has 3+ goals). This mechanism is real and reproduces the reported symptom, just not broadly.
- The remaining 52/60 accounts (86.7%) show a goal that **is** structurally visible right now. This is the honest, slightly counter-intuitive part of the finding: most `goals_text`-bearing accounts are *not* currently in a broken state at the DB level. The bug is real but concentrated in the "returning user, 3+ existing goals, re-onboards" edge case CS-05 targets — it is not a universal failure of the sync path.

**Best candidate for "the operator's test account":** ctx-label `9` — the single most-recently-*updated* row in the entire 60-account goals sample (`updated_at = 2026-08-18 17:26:27+00:00`, squarely in Darek's 17–18.08 window), yet its `user_therapy_context.id` is very low (9), meaning the underlying account is one of the very earliest in the table (consistent with a long-lived internal/QA account reused for repeated onboarding tests). This is an *inference from the access pattern*, not a confirmed identity — no PII was queried to establish it. On this account, right now: 3 active goals, newest ranks **3rd** (still inside `take(3)`, i.e. would currently render). This does not confirm mechanism 1 was the cause of what Darek saw on 17–18.08 — either the goal count has changed since (an achieve/drop shifted the rank), or something else was at play at the time. Flagged as inconclusive, not a smoking gun, for this specific account.

---

## CS-06 — Symptom/mood sync results

| Metric | Result |
|---|---|
| Candidate accounts (non-empty `focus_areas`, all-time) | 60 |
| Total focus-area mentions across those accounts | 214 |
| Matched an **active** (`is_visible=true`) `user_symptoms` row | **211 / 214 (98.6%)** |
| Matched an **archived** (`is_visible=false`) `user_symptoms` row — the archived-skip hypothesis | **1 / 214 (0.5%)** |
| No `user_symptoms` row at all (name never synced) | **2 / 214 (0.9%)** |
| Matched symptom rows with **zero** `symptom_scores` (row created, initial score missing) | **0** |
| Accounts with `focus_areas` set but *zero* `user_symptoms` rows entirely | 1 / 60 |
| Accounts with `focus_areas` set but `severity_ratings` null/empty (sync gate `if stored_focus and stored_ratings` never true → sync never even attempted) | **1 / 60** (ctx-label 8318, 2026-07-13) |

**sync_symptoms_from_onboarding has existed since 2026-03-02** (`git log -S`), long before CS-01's goal sync — so none of the anomalies below can be explained by "feature too new."

**Interpretation:**
- The symptom sync backend is **not broadly broken** — it succeeds for 98.6% of the 214 focus-area mentions measured, and every symptom row that *was* created has a real initial score (0 "row exists but no score" cases). This is a materially different picture than CS-05's goal sync headline symptom, and it means CS-06's reported failure is unlikely to be a wholesale backend outage.
- **Archived-skip (mechanism b) — confirmed, on the same likely-operator account.** ctx-label `9` (the same row flagged above as the probable test account, `updated_at = 2026-08-18 17:26:27+00:00` — squarely inside Darek's report window) has exactly one focus-area mention matching an existing `user_symptoms` row with `is_visible=false`. `get_user_symptoms`'s dedupe check (`crud.py:3200-3205`, called with default `visible_only=False`) treats that archived row as "already exists" and skips creating a new score entirely, per the code path documented in the spec. This is the strongest single piece of evidence in this whole investigation: it fires on the right account, at the right time, doing the right thing the bug predicts.
- **Missing-entirely / shared-swallow (mechanism a) — confirmed, rare, but real and post-existing-feature.** 2 mentions (ctx-labels 8548 and 8318, dated 2026-07-24 and 2026-07-13 — both well after the symptom-sync code has existed since March) have no `user_symptoms` row whatsoever. This is consistent with the `except Exception: logger.warning(...)` swallow at `users.py:1237-1238` (no `db.rollback()`) eating a real failure silently. It is not high-frequency in this sample (2/214), but it does exist independent of the archived-skip case, on different accounts/dates.
- One additional mechanism not named in the spec's two candidates, found while checking: the sync only runs `if stored_focus and stored_ratings` (`users.py:1229`) — **both** must be truthy in the *same* read-back of the row. 1 account has `focus_areas` populated with `severity_ratings` empty/null, meaning the sync block is never entered at all (not an exception — a silent no-op at the gate). Worth folding into CS-06's `db.rollback()`/logging fix as a third failure path to make visible (e.g. log when the gate doesn't fire despite one side being present), since it currently produces zero trace of any kind.

---

## Heroku log check (item 4)

`heroku logs -a mindsync -n 1500` returned **1500 lines spanning only ~1 hour** (`2026-08-20T08:06` → `2026-08-20T09:02`, i.e. today, not the 17–18.08 window Darek tested in). Grep for both warning strings (`"Symptom sync from onboarding failed"`, `"Goal sync from onboarding failed"`) inside that window: **zero hits**. This is expected and **not evidence the warnings never fired** — Heroku's platform log retention (no logging add-on configured) does not reach back three days at this app's log volume. The absence here cannot be used to rule anything in or out; stating this plainly rather than inferring silence = no bug.

---

## What this does and doesn't answer

**Ruled in, with direct evidence:**
- CS-06 archived-skip (mechanism b) — confirmed, and very likely fired on the actual reporter's account at the actual report time.
- CS-06 shared-swallow / missing-entirely (mechanism a) — confirmed present, low frequency, on accounts unrelated to the archived-skip case (so it's a second, independent failure mode, not a restatement of the first).
- CS-06 severity_ratings-gate-never-true — a third, previously unnamed failure path, confirmed present (1 account), silent (no log line at all, not even a swallowed exception).
- CS-05 buried-goal (mechanism 1) — confirmed present in the population (2/60), structurally requires 3+ pre-existing active goals, matches Darek's specific repro shape even though it's rare overall.

**Ruled out / not supported by this data:**
- CS-05 poisoned-session silent-swallow (mechanism 3) on the goal side — zero post-deploy occurrences found across the 60 most recent goal-bearing accounts. Cannot fully rule out (it's a race, and 60 accounts is not exhaustive), but there is no positive evidence for it here, in contrast to CS-06 where the analogous mechanism (a) *does* have 2 confirmed hits.

**Could not confirm either way:**
- Whether mechanism 1 (buried goal) was specifically what Darek saw on 17–18.08 — the best-guess account (ctx-label 9) currently shows the goal at rank 3 (still visible), which doesn't match the "invisible" story as measured *today*; state may have changed since (an achieve/drop event would shift ranks) and this can't be reconstructed without goal-history/audit data this schema doesn't retain.
- Any log-level confirmation of either swallow warning actually firing around 17–18.08 — Heroku's short retention makes this unmeasurable from logs; would need a logging add-on (Papertrail/Logtail) with real retention to close this gap going forward.

## Handoff to backend-api

1. Add `db.rollback()` to both `except` blocks in `users.py` (`:1238`, `:1286`) per the spec's own point 2 — confirmed necessary regardless of which mechanism is primary, since it's cheap insurance against the cross-contamination case (mechanism 3) even though this sample didn't catch it live.
2. CS-06 fix should explicitly handle the `stored_focus and stored_ratings` gate-never-true case — either log when only one side is present (currently silent), or reconsider whether severity should default rather than block the whole sync.
3. Recommend a logging add-on with >24h retention (Papertrail/Logtail) — the current ~1hr Heroku platform retention makes any future "did the warning fire" question unanswerable after the fact, which is exactly the gap hit in step 4 of this investigation.
