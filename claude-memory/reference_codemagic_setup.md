---
name: Codemagic CI/CD setup
description: Stan setupu Codemagic dla neuravec/mindsync-frontend — co zostało zrobione w repo, co wciąż user musi zrobić w Codemagic UI
type: reference
originSessionId: dd3ab50d-9f30-4428-b8c3-87eb126c886b
---
# Codemagic CI/CD — stan na 2026-04-21

## Zrobione w repo (gałąź `dev`, niezacommitowane)

### Pliki w git (do commitu)
- `mindsync-frontend/.gitignore` — nowy root-level, ignoruje `.p12`, `.p8`, `.mobileprovision`, service-account JSONs, `.env.*` (oprócz `.env.example`)
- `mindsync-frontend/codemagic.yaml` — usunięto hardcoded SLACK_WEBHOOK, dodano grupa `slack`, `Send notification` skrypt z `set -o pipefail`, case-based routing (success/failed/unknown), `emit_warning` funkcja pisze artefakt do `$CM_BUILD_DIR/mindsync_app/build/NOTIFICATION_FAILED_BUT_RELEASE_LIVE.txt` (w artifacts glob), `exit 0` żeby build stayed green (red badge zapraszał do re-trigger → version clash)
- `mindsync-frontend/mindsync_app/android/app/build.gradle` — sentinel `CM_KEYSTORE_PATH` zamiast `CI` (unikamy kolizji z GitHub Actions/VSCode)
- `mindsync-frontend/docs/codemagic_setup.md` — kompletny setup guide (9 sekcji: rotacja Slack/prereq/Codemagic UI/fresh clone/local build/dry-run/rotation/follow-ups/troubleshooting)

### Pliki tylko lokalne (ignored, NIE committed)
- `mindsync_app/android/app/upload-keystore-ms.jks` — kopia z `Heroku/itmesh/`
- `mindsync_app/android/key.properties` — kopia z `Heroku/itmesh/`

## Zadania usera (w Codemagic UI — nie da się przez kod)

### MUST-DO przed commitem
1. **Rotuj stary Slack webhook** — `hooks.slack.com/services/<REDACTED>` jest w git history codemagic.yaml, rewoke w Slack Apps → Incoming Webhooks → Remove/Regenerate. Szczegóły w docs/codemagic_setup.md sekcja 0.1.
2. **Weryfikacja keystore fingerprint** — `keytool -list -v -keystore .../upload-keystore-ms.jks -alias upload`, porównaj SHA-1/SHA-256 z Play Console → App integrity → Upload key certificate. Jeśli mismatch → napisz do ITMesh. Sekcja 0.3.

### Setup w Codemagic UI (szczegóły w docs sekcje 2.2-2.5)
1. Apps → Add neuravec/mindsync-frontend jako Flutter App (codemagic.yaml)
2. Team integrations → Code signing → Android keystores → upload `upload-keystore-ms.jks` z reference name `ms_upload_keystore` (wartości z `Heroku/itmesh/key (2).properties`)
3. Team integrations → Environment variables → 4 grupy:
   - `git` — pusta, placeholder (referencjonowana przez pr-builder + app-create-version)
   - `gcloud` — `GCLOUD_SERVICE_ACCOUNT_CREDENTIALS` = zawartość `Heroku/itmesh/mindsync-8f534-aff21dba3bf7.json`
   - `appstoreconnect` — `APP_APPLE_ID` = numeryczny (10 cyfr) z ASC → My Apps → MindSync → App Information
   - `slack` — `SLACK_WEBHOOK` = NOWY URL po rotacji
4. Globalne / workflow-level vars: `KEYSTORE_NAME=ms_upload_keystore`, `POSTHOG_API_KEY` (z PostHog dashboard)
5. Team integrations → Apple Developer Portal → App Store Connect API → Add key:
   - Nazwa MUSI być `MIndSync Appstore Connect` (z typo capital I — matches codemagic.yaml:102)
   - Issuer ID + Key ID + .p8 content z ASC (user musi wygenerować sam, sekcja 2.4.1)
6. Team integrations → Code signing → iOS certificates → Generate new → reference name `ms-cm-cert`, Distribution. Codemagic sam wygeneruje profile `MindSync App distribution profile`.
7. Team integrations → SSH keys → Add (+ GitHub Deploy key z write access)

### Setup poza Codemagic (Play Console / ASC)
1. Play Console → Users and permissions → Invite `codemagic-job@mindsync-8f534.iam.gserviceaccount.com` jako Release manager. **Ważne: SA nie dostaje emaila, status "Invited" jest końcowy, nie czekaj na acceptance.**
2. Play Console: aplikacja `com.mindsync.app` musi mieć pierwszy manual release przed próbą CI publish (Play API constraint).
3. ASC: bundle ID `com.mindsync.app` + Paid Apps Agreement + TestFlight enabled.

## Follow-ups (zebrane w docs sekcja 7)

### Pre-release (decide before first tag)
- **Humm CLI supply chain** — `git clone https://github.com/hummlab/humm_flutter_cli.git` bez SHA pinning → każdy build ciągnie HEAD. Jeśli upstream przejęty → leak wszystkich env vars CI.
- **Humm env var name** — nie zweryfikowane że humm czyta `SLACK_WEBHOOK` (nie np. `SLACK_WEBHOOK_URL`). Zrób `grep -r SLACK_WEBHOOK /tmp/humm_check/lib/` przed pierwszym release.

### Nice-to-have (po pierwszym release)
- Rename `MIndSync Appstore Connect` → `mindsync_asc` (yaml + UI w osobnym PR)
- `when.changeset` gate może blokować emergency releases bez pubspec bump
- Smoke test: invalid `SLACK_WEBHOOK` → verify badge stays green, artifact appears (TODO w codemagic.yaml:224-230)

## Wiele iteracji DA review

Setup przeszedł przez ~8 devils-advocate reviews (batch per file-change). Kluczowe findings które zostały naprawione:
- CRIT: password `<REDACTED>` w docs git-tracked (usunięte)
- CRIT: artefakt ostrzegawczy pisany poza artifacts glob (przeniesione do `$CM_BUILD_DIR/mindsync_app/build/`)
- CRIT: Slack rotation advisory buried (teraz sekcja 0.1 na samej górze)
- HIGH: `CI=true` env collision (sentinel zmieniony na `CM_KEYSTORE_PATH`)
- HIGH: `exit 1` po failed notification → Retry button → version clash (flip na `exit 0` + artifact)
- HIGH: case branch routowało "unknown" BUILD_STATUS do error notify (false ping fix)
- HIGH: scan w docs sekcji 0.2 miss'ował deleted paths (widened na `git log --all -p`)
