---
name: reference-ga4-revenue-pull-scripts
description: GA4 + App Store Connect + Google Play read-only pull scripts (2026-10-22): where creds live, deps, unverified API details
metadata:
  type: reference
---

Written 2026-10-22, never run against real APIs (no creds existed yet; operator Darek was creating them).

- `scripts/ga4/pull_ga4.py`: stdlib, reuses `scripts/gsc/client_secret.json` (Desktop client, project mindsync-8f534), own `scripts/ga4/token.json`. Needs Analytics Data API + Admin API enabled in mindsync-8f534.
- `scripts/revenue/asc_reports.py`: needs `pip install --user "pyjwt[crypto]"`; env in `scripts/revenue/.env`.
- `scripts/revenue/play_reports.py`: needs `pip install --user google-auth requests`; PLAY_BUCKET (gs:// URI from Play Console) overrides PLAY_DEVELOPER_ID.
- Output under `analytics-reports/raw/revenue/` is gitignored (financial data).

Unverified at write time, check on first real run: SUBSCRIPTION report version default 1_3 (overridable `--version`), Play `financial-stats/subscriptions/` and `stats/installs/` filename patterns (script matches YYYYMM in basename), whether bucket is `pubsite_prod_rev_<id>` or `pubsite_prod_<id>` for this account.
