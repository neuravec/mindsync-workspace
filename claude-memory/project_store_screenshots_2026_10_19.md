---
name: project-store-screenshots-2026-10-19
description: "App Store / Google Play screenshot refresh pipeline (store/, render_store.py, harness store_* shots) and its open points"
metadata:
  node_type: memory
  type: project
  originSessionId: 3db298d3-320b-4d06-a645-197780005c6a
  modified: 2026-10-19T18:59:11.702Z
---

2026-10-19: store screenshots refreshed in the old App Store style (mint gradient, 2-line headline with one bold phrase, iPhone frame).
- Pipeline: harness shots `store_*` (mindsync-frontend test/marketing_shots/store_*_shot_test.dart + store_shot.dart, branch feat/store-shots b0db599, NOT pushed) -> PNGs in `store/renders/{ios,android}` -> `python scripts/store/render_store.py` -> `store/out/appstore` 1290x2796 (9 slides) and `store/out/play` 1080x1920 (8, no testimonial). Copy in `store/copy.md` (brand-voice approved), spec `store/slides.json`.
- Order: main, after_therapy, recording, reflect, prep, workspace, timeline, character (+ testimonial App Store only).
- Review artifact: https://claude.ai/artifact/PmoQMzjg6K1PvBVRG7CUt2 (page Sklepy + page Instagram with 7 IG drafts and status labels).
- Old store set (600px webp) lives in blog/images/app-screenshots; the operator's Drive folder is not reachable from the connected Google account.
- Open: upload only with the store release that has the new Main and Character (Apple 2.3.3); keep the testimonial only with the author's consent; re-render store_timeline after the Timeline A3 v2 implementation (wrapped chips).

- 2026-10-19 (later): store LISTING copy (name, subtitle, promo text, description, keywords, What's New; Play title, short/full description, release notes) lives in `store/listing.md`, written by seo-content-writer, AKCEPT brand-voice-manager after fixes. Current live listings were scraped to scratchpad `store-copy/{apple,play}-listing.txt` (Apple JSON-LD has the full description; WebFetch refuses verbatim quotes). Decisions left to operator: name change to "MindSync: Therapy Journal" (both stores), "2,000+" claim, testimonials (FTC), old privacy-policy v1 on mindsync.app blocks upload. Ahrefs Keywords Explorer is NOT in the plan ("Insufficient plan").

**Why:** next time screens change, one harness run + one render command refreshes both stores.
**How to apply:** rerun the harness shots in a worktree, then render_store.py; never retouch screens. Related: [[project-redesign-v3-teams-2026-10-18]], [[project-instagram-automation-2026-10-01]].
