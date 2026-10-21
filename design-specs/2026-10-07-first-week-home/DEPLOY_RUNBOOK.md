# First-week Home: production deploy runbook

Prepared 2026-10-11 by integration-devops. **Nothing in this file has been run.** No push, no migration, no config change and no Heroku command was executed while writing it.

Sources: `audit-security-delta-2026-10-11.md` (verdict GO with conditions, section "Conditions for this deploy"), `audit-security-wp1-4-backend.md` (M-2, M-3, deploy conditions), `API_CONTRACT.md` section 12 and 14.2, `COPY.md` 14.8 to 14.10, the root `CLAUDE.md` (no release phase on Heroku, manual migrations), `mindsync-frontend/codemagic.yaml`.

## 0. What ships

| Side | What | Where |
|---|---|---|
| Backend | Branch `feat/first-week-home`, head `6bd0e3e` at the time of writing (security-reviewed code `5843db4` plus qa-testing test-only commits), plus `fw/be11-env` (`f976177`, `.env.example` only) once the lead merges it | GitHub `neuravec/MindSync`, branch `main` auto-deploys to Heroku app `mindsync` |
| Backend | 24 commits ahead of `origin/main` (`8eb8d3f`), and `origin/main` is an ancestor, so the push is a fast-forward | |
| Migrations | `m317a1b2c3d4` (enum labels `AUTO`, `MOOD_TREND`; already on `main`, may not have run on prod yet) then `m318a1b2c3d4` (first-week schema: `users.first_week_started_at`, `user_preferences.skipped_dates`, tables `first_week_plan_state` and `first_week_follow_ups`, `moment_type_enum` label `FIRST_WEEK_STEP`) | `MindSync/alembic/versions/` |
| New cron | `mindsync_first_week_follow_up_purge`, daily 04:40 UTC, queue `default`, registered from the web lifespan | `app/core/rq_scheduler_setup.py` |
| New config | `ART9_SCHEDULE_GATE_MIN_APP_VERSION` (unset), `ART9_SCHEDULE_GATE_ALL_CLIENTS` (false). Defaults gate nobody, so the backend deploy changes nothing for apps already in the stores | Heroku Config Vars only, never the tracked `.env` |
| Frontend | Branch `feat/first-week-home` (FE integration worktree, head `bed441f` at the time of writing), 17 commits ahead of `origin/dev` (`6f2c168`, version `2.0.108+181`), fast-forward | GitHub `neuravec/mindsync-frontend`, branch `dev` triggers Codemagic and TestFlight |

Order is fixed (contract 12): backend push, then migrate right away, then the read-only checks, and only then the frontend to `dev`. The Art. 9 gate config comes after the frontend version name is known.

## 1. Operator steps at a glance

Steps marked **[heroku login]** need the operator's Heroku session (`heroku login`, or the API key the CLI stores in `~/_netrc`). The agent permission classifier blocks `heroku run ... alembic upgrade head` on prod even when the lead relays approval, so the operator runs that step personally.

| # | Step | Who | Needs |
|---|---|---|---|
| P5 | Record the live release and `alembic current` before the push | operator or integration-devops | **[heroku login]** |
| B1 | `git push origin feat/first-week-home:main` (backend) | lead or integration-devops, on operator go | GitHub write access |
| B2 | Wait until the new release is live, check the boot | operator or integration-devops | **[heroku login]** |
| B3 | `heroku run alembic upgrade head -a mindsync`, then `alembic current` | **operator** | **[heroku login]** |
| B4 | Read-only checks | integration-devops, database-administrator, posthog-data-extractor; items 5 and 6 need a Firebase ID token | **[heroku login]** for logs and `alembic current` |
| F1 | `git push origin feat/first-week-home:dev` (frontend) | lead or integration-devops, on operator go | GitHub write access |
| F3 | Read the new version name from the `app_*` tag | anyone | git only |
| F4 | `heroku config:set ART9_SCHEDULE_GATE_MIN_APP_VERSION=<version> -a mindsync` | **operator** | **[heroku login]** |
| R | Rollback, if needed (section 4) | operator | **[heroku login]** |

## 2. Preflight (before B1)

- **P1. Full backend suite** on the exact commit that will be pushed (delta audit condition 1). qa-testing. Known pre-existing failures per the 2026-06-01 baseline are not regressions.
- **P2. Security:** delta audit verdict GO with conditions; no Critical, High or Medium finding blocks this push. Nothing else to wait for on the backend side.
- **P3. Merge `fw/be11-env`** into `feat/first-week-home` (docs only, lead). Optional for the deploy, but it keeps `.env.example` in step with `config.py`.
- **P4. Fast-forward check:**
  ```
  git -C MindSync fetch origin
  git -C MindSync merge-base --is-ancestor origin/main feat/first-week-home && echo fast-forward
  git -C MindSync rev-parse --short=8 feat/first-week-home   # note this; B2 matches the release on it
  git -C MindSync rev-parse --short=8 origin/main            # pre-push main (8eb8d3f on 2026-10-11): the revert target
  ```
  If `origin/main` moved since 2026-10-11, merge it into the branch and rerun P1.
- **P5. Record the rollback target and migration state** **[heroku login]**:
  ```
  heroku releases -a mindsync -n 3 < /dev/null      # note the current vNNN: this is the rollback target
  heroku run alembic current -a mindsync            # expect m316a1b2c3d4 or m317a1b2c3d4
  heroku config:get ART9_SCHEDULE_GATE_MIN_APP_VERSION -a mindsync < /dev/null   # expect empty
  heroku config:get ART9_SCHEDULE_GATE_ALL_CLIENTS -a mindsync < /dev/null       # expect empty or false
  ```
  The tracked `MindSync/.env` holds no `ART9_*` or `FIRST_WEEK_*` key (checked 2026-10-11 by key name, no values read). Keep it that way: a key there that the rolled-back code does not declare crash-loops the web dyno.
- **P6. Timing:** push when someone can watch for about an hour. The gap between B2 and B3 should be minutes, not hours (see B2, "In the gap").

## 3. Backend deploy

### B1. Push

```
git -C MindSync push origin feat/first-week-home:main
```

GitHub `neuravec/MindSync` `main` auto-deploys to Heroku app `mindsync`. Do not also `git push heroku`; one path only.

### B2. Wait for the release, then check the boot **[heroku login]**

```
heroku releases -a mindsync -n 5 < /dev/null
```

The new top release reads `Deploy <sha8>`, where `<sha8>` is the value noted in P4. Match on that hash, not on a hash copied from a plan. Poll about every 45 s; a build takes a few minutes. A failed build creates no release and changes nothing (the previous release keeps serving); its log is in the Heroku dashboard under Activity. If the CLI hangs, the Platform API answers the same question: `GET https://api.heroku.com/apps/mindsync/releases` with `Accept: application/vnd.heroku+json; version=3` and `Range: version ..; order=desc, max=5`.

Then:

```
heroku ps -a mindsync < /dev/null
heroku logs -a mindsync -n 800 < /dev/null | grep -E "first-week router not mounted|Traceback|code=H10|Error R1[0-9]|Scheduled first-week follow-up purge"
```

Expect `web.1`, `worker.1` and `scheduler.1` up with a fresh start time. Expect no `first-week router not mounted`, no H10 or R10, and one `[Scheduler] Scheduled first-week follow-up purge daily at 04:40 UTC` line per web boot. Raw `heroku logs` print the Redis URL with its password in the `Starting process with command` lines: redact before quoting anything.

Router probes, no token and no Heroku login needed:

```
BASE=https://mindsync-829f3f05ed43.herokuapp.com/api/v1
for p in first-week/plan first-week/recap first-week/follow-up; do printf "%s " "$p"; curl -s -o /dev/null -w "%{http_code}\n" "$BASE/$p"; done
printf "therapy-schedule/change "; curl -s -o /dev/null -w "%{http_code}\n" -X POST "$BASE/users/therapy-schedule/change"
```

Each must answer 403 (or 401), the auth refusal. A 404 means that router's guarded import failed and the route is missing: boot is fine, but find the traceback in the logs and stop before the frontend step.

**In the gap between B2 and B3** (expected, harmless if short): every first-week read answers `503 first_week_unavailable`; the change route answers `503 schedule_change_unavailable`; the plan-step generator logs `[PLAN_STEP] plan-step reminders skipped this run (first-week store not ready)` once per hourly orchestrator run; an account that finishes onboarding in the gap gets no first-week anchor (its onboarding still succeeds). Shipped apps never call the first-week routes, so users see nothing.

### B3. Migrate **[heroku login]**, operator

Run only after B2 shows the new release live. `heroku run` boots a one-off dyno from the current release's slug; before B2 that slug has no m318 file and the upgrade would stop at m317.

```
heroku run alembic upgrade head -a mindsync
heroku run alembic current -a mindsync
```

Expect `m318a1b2c3d4 (head)`. The upgrade runs m317 first if P5 showed m316. Both migrations are idempotent. m318 sets `lock_timeout = '5s'` before its DDL on `users` and `user_preferences`; if it fails with a lock timeout, run it again. m317 needs no operator decision any more (security M-3 is fixed in this code: the AUTO prep-card cron now checks Art. 9 consent).

### B4. Read-only checks (within about two hours)

| # | Check | Who | Expected |
|---|---|---|---|
| 1 | Migration state | operator or integration-devops **[heroku login]** | `m318a1b2c3d4 (head)` |
| 2 | Plan-step skip line stops (orchestrator runs at minute 0) | **[heroku login]**, after the next full hour | No skip line newer than the migration time |
| 3 | No 500 on `GET /moments/upcoming` or `POST /users/therapy-schedule/change` | **[heroku login]** for logs; posthog-data-extractor for `api_error` events with a 5xx status on these two routes since the push | No match in the logs; zero `schedule_change_unavailable` after the migration; zero 5xx events |
| 4 | Auto prep-card cron is consent-gated (runs at minute 30) | **[heroku login]**, after the next run | The DONE line carries `skipped_no_consent=` (counts only, no user id) |
| 5 | Old account gets no plan | anyone with a Firebase ID token of an account created before the push | `204`. Without a token at hand, database-administrator proxy: the count of users created before the push with `first_week_started_at IS NOT NULL` is 0 (204 means "no anchor", contract 14.1 item 1) |
| 6 | `/users/usage` carries Free limits | same token | Every feature object has an integer `free_limit` |
| 7 | `notification_logs` stores template keys | database-administrator, aggregate only: rows since the push grouped by `title`, plus the count of new rows with a non-null `body` | Every `title` is a template key, never push text; `body` is null on every new row |
| 8 | Worker drains jobs | **[heroku login]** | `deliver_due_moments finished` every 5 minutes, `failed=0` or low |

Commands (run with `< /dev/null` so the CLI does not wait for input):

```
heroku run alembic current -a mindsync                                                        # 1
heroku logs -a mindsync -n 1500 < /dev/null | grep "PLAN_STEP] plan-step reminders skipped this run"   # 2
heroku logs -a mindsync -n 1500 < /dev/null | grep -E '"(GET|POST) /api/v1/(moments/upcoming|users/therapy-schedule/change)[^"]*" 5[0-9][0-9]'   # 3
heroku logs -a mindsync -n 1500 < /dev/null | grep schedule_change_unavailable                 # 3
heroku logs -a mindsync -n 1500 < /dev/null | grep "\[AUTO-GEN\] auto_generate_prep_cards DONE"   # 4
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $TOKEN" "$BASE/first-week/plan"   # 5
curl -s -H "Authorization: Bearer $TOKEN" "$BASE/users/usage"                                     # 6
heroku logs -a mindsync -n 1500 < /dev/null | grep "deliver_due_moments finished"              # 8
```

Keep the Firebase ID token out of every report, ticket and log.

### B5. Watch

Watch the logs for about 30 minutes after B3 (the Logplex buffer holds roughly 1500 lines, about 30 minutes; Papertrail history is not reachable from here). Look for `Traceback`, `LookupError`, `UndefinedColumn`, `[ScheduleGate]` warnings and any 5xx on `/api/v1/first-week/`, `/api/v1/users/` and `/api/v1/moments/`.

## 4. Backend rollback

**Code.** Fastest **[heroku login]**:

```
heroku rollback vNNN -a mindsync      # vNNN from P5
```

`main` on GitHub still holds the code, so the next push redeploys it. Follow with a revert on `main` (lead), or fix forward. The pushed range contains merge commits, so a plain `git revert <range>` fails; one commit that restores the pre-push tree is simpler:

```
git -C MindSync checkout -b revert/first-week origin/main
git -C MindSync read-tree -u --reset <pre-push main sha from P4>
git -C MindSync checkout <pushed sha> -- alembic/versions/m318a1b2c3d4_add_first_week_home_schema.py   # trap 2
git -C MindSync commit -m "revert: first-week Home backend (keep m318 migration file)"
```

Contract 12.5's path (revert plus push) reaches the same state through a new build. A revert commit may also keep `FIRST_WEEK_STEP` in `MomentTypeEnum` (backend-api), which defuses trap 1 below without touching data; `heroku rollback` cannot do that, because it reuses the old slug.

**Migrations: no downgrade.** m318 is additive: two nullable columns that the old mappers do not know, two new tables the old code never reads, one enum label. Old code boots and runs against the m318 schema. Running `alembic downgrade` is not needed and not recommended: m318's downgrade drops `first_week_plan_state` and `first_week_follow_ups`, which loses the plan state of every tester for nothing, and the enum label stays anyway (Postgres has no DROP VALUE). m317's downgrade is a no-op by design.

**Rollback traps, check every one:**

1. **`FIRST_WEEK_STEP` rows break the old notification code.** Old code maps `notification_moments.moment_type` as `SQLEnum(MomentTypeEnum)` without that member, so loading such a row raises `LookupError`. `deliver_due_moments` loads every due PENDING row with no type filter, so one PENDING plan-step row stops push delivery for everyone every 5 minutes; the expiry job, `GET /moments/upcoming` for that person and the per-type stats break the same way. Rows exist only after a first-week build is in testers' hands and someone turned the plan-step reminder on. Before rolling back, database-administrator counts them (aggregate only):
   ```
   SELECT status, count(*) FROM notification_moments WHERE moment_type = 'FIRST_WEEK_STEP' GROUP BY status;
   ```
   Zero rows: the plain rollback is clean (this is the case for any rollback before F1). Any rows: prefer a fix forward. If the rollback must happen anyway, the operator approves deleting those rows right after it (`notification_logs.moment_id` is `ON DELETE SET NULL`, so the delete is FK-safe; the rows hold neutral reminder copy and their removal also shrinks the D-L1 trace).
2. **Keep the migration files in any revert.** If a revert deletes `m318a1b2c3d4_*.py` while prod `alembic_version` says m318, every later `alembic upgrade head` and `alembic current` fails with "Can't locate revision". Restore the file with `git checkout <sha> -- alembic/versions/m318a1b2c3d4_add_first_week_home_schema.py` and commit it with the revert.
3. **Cancel the boot-registered cron.** `heroku rollback` leaves `mindsync_first_week_follow_up_purge` in Redis, and the old worker cannot import `app.tasks.first_week_follow_up` (it fails daily at 04:40 UTC). Cancel it with a one-off **[heroku login]**:
   ```
   heroku run -a mindsync -- python -c "import os; from redis import Redis; from rq_scheduler import Scheduler; s = Scheduler(connection=Redis.from_url(os.getenv('REDISGREEN_URL'))); [s.cancel(j) for j in s.get_jobs() if j.id == 'mindsync_first_week_follow_up_purge']; print('CANCEL_DONE')"
   ```
   `heroku run` may report exit 1 although the dyno exited 0: look for `CANCEL_DONE`.
4. **Config Vars.** Old code ignores `ART9_SCHEDULE_GATE_*` Config Vars, so they need no action for a rollback. Unset them afterwards for hygiene (`heroku config:unset ... -a mindsync`).
5. **Redis keys** `fw:*` stay until their TTL (at most 21 days); harmless.
6. **Clients.** A first-week build talking to the rolled-back backend gets 404 on the first-week routes and shows the legacy Home (contract 12.5). The session sheet's change route also answers 404: the sheet shows its error toast and nothing changes.

**Art. 9 gate only, no deploy:** `heroku config:unset ART9_SCHEDULE_GATE_MIN_APP_VERSION -a mindsync` (or set it to `99.0.0`) switches the version gate off; the dynos restart. `POST /users/therapy-schedule/change` stays gated regardless.

## 5. Frontend: TestFlight build

### F0. Preconditions

- B4 checks 1 to 4 passed (contract 12 step 2). Frontend never goes to `dev` against a backend without the routes.
- flutter-mobile's open work is merged into the FE `feat/first-week-home`. At the time of writing, `fw/fe8-ux-home` and `fw/fe9-ux-session` hold uncommitted changes that close contract 14.2 items 10, 12 and 14 and add `session_date` and `replaces_date` to the analytics guard (delta condition 5). See section 8.
- `flutter analyze` (filter on `error •`) and `flutter test` per directory are green on the merged head; generated code (`build_runner`, l10n) is committed; the German ARB mojibake fix (COPY 14.10) is in.
- Never `git add .` in the FE worktrees: the integration worktree carries local, uncommitted plugin-registrant changes (`linux/`, `macos/`, `windows/`) that must not ship.

### F1. Push

```
git -C mindsync-frontend fetch origin
git -C mindsync-frontend merge-base --is-ancestor origin/dev feat/first-week-home && echo fast-forward
git -C mindsync-frontend push origin feat/first-week-home:dev
```

Opening a PR into `dev` and merging it works too: `pr-builder` runs on the PR, and the merge is the push event.

### F2. What Codemagic does

- `app-create-version` triggers on every push to `dev` (`triggering.events: push`, `branch_patterns: dev`, `source: true`). It exits at once when the head commit message contains `Pre-release updates` (its own bump commit).
- It runs `humm release --tag-prefix app --branch dev`: bumps `version:` in `mindsync_app/pubspec.yaml`, commits `Pre-release updates` to `dev` as Codemagic Bot, and pushes the tag `app_<version>`. So far every release bumped the patch number (`app_2.0.106`, `app_2.0.107`, `app_2.0.108`), so the next one is expected to be `2.0.109`. Read it, do not assume it (F3).
- It then starts `app-release` through the Codemagic API. If that call fails it writes `APP_RELEASE_AUTO_TRIGGER_FAILED.txt` as a build artifact: the operator starts "IOS and Android release" by hand in Codemagic with build tag `app_<version>`, once (a second build collides on build numbers).
- `app-release` builds the Android bundle (Google Play `internal` track) and the iOS IPA (App Store Connect, then TestFlight after Apple's processing). Build numbers come from the stores (Play latest + 1, TestFlight latest + 1); the version name comes from `pubspec.yaml`. There is no Codemagic API token on the dev machine, so build status is read in the Codemagic dashboard and in App Store Connect.

### F3. Read the version name

```
git -C mindsync-frontend fetch origin --tags
git -C mindsync-frontend tag --list "app_*" --sort=-creatordate | head -1          # app_2.0.109 -> version name 2.0.109
git -C mindsync-frontend show origin/dev:mindsync_app/pubspec.yaml | grep "^version"   # 2.0.109+NNN; the part before "+" is the version name
```

The client sends exactly this version name in `X-App-Version` (`lib/api/app_info_headers.dart`, the pubspec version name, the same on iOS and Android). TestFlight shows it as `2.0.109 (<build>)`. This build is the first one that sends the header at all (`origin/dev` does not have it today) and the first with the Art. 9 consent step.

### F4. Turn on the Art. 9 version gate **[heroku login]**, operator

As soon as the `app_<version>` tag exists, and no later than the build becoming available in TestFlight (WP-1..4 M-2, delta condition 4):

```
heroku config:set ART9_SCHEDULE_GATE_MIN_APP_VERSION=2.0.109 -a mindsync    # use the version from F3
heroku config:get ART9_SCHEDULE_GATE_MIN_APP_VERSION -a mindsync < /dev/null
```

Setting it once the version is fixed is safe even before the build exists: no client sends that version yet, so nobody is gated until the build arrives. The comparison is "at or above", so if this build fails and a retry produces `2.0.110`, the gate still covers it. The dynos restart on `config:set`. Afterwards no `[ScheduleGate] ... is not major.minor.patch` warning may appear in the logs.

`ART9_SCHEDULE_GATE_ALL_CLIENTS=true` (gate old builds too) stays off until database-administrator's count of schedule edits without consent (contract 14.1 item 3, SPEC 13.8) and an operator decision.

### F5. TestFlight smoke (operator or tester)

1. Account without Art. 9 consent: add session times from a side card. The consent step appears first, then `SessionSetupScreen`. Decline: nothing is saved and the local schedule rolls back.
2. Same account, Settings schedule editor: the consent step appears; with consent the schedule saves.
3. An App Store build (no header) still saves a schedule (not gated).
4. "Session moved?" on a prep card, "Just this once": saves; the plan refreshes.
5. Free account with no Reflect messages left: the `rest` and `open` cards lead to the quick check-in, never to a paywall.

## 6. PostHog verification after TestFlight (posthog-data-extractor)

Filter on `$app_version` = the F3 version and `$lib = posthog-flutter`. TestFlight volume is small: report "flowing / not flowing" and counts only, never per person.

Client events to confirm flowing, with only the listed properties:

| Event | Properties | Fires when |
|---|---|---|
| `today_card_viewed` | `plan_active` | Today card visible, once per app session per local day |
| `today_card_tapped` | `plan_active` | Primary button |
| `today_card_deferred`, `today_card_defer_undone` | none | "Not today" and its undo accepted |
| `first_week_plan_toggled` | `expanded` | "See the week" / "Show less" |
| `first_week_plan_hidden` | none | "Hide this plan" accepted |
| `side_card_tapped`, `side_card_dismissed` | none | Side card |
| `reminder_optin_result` | `result` (`on`, `off`, `denied_settings`) | Day-0 reminder row |
| `session_sheet_completed` | none | Session sheet change accepted |
| `quick_checkin_completed` | `areas_count`, `skipped_count` | Check-in finished |
| `checkin_next_step_tapped` | none | Mirror next-step CTA |
| `follow_up_started` | none | First message (text) or voice session started from the follow-up question |
| `first_week_recap_viewed` | none | Recap on screen after a 200 |
| `rhythm_sheet_opened`, `rhythm_selected` | `count` on `rhythm_selected` | Rhythm sheet, "Keep this rhythm" |
| `trial_reminder_sheet_shown`, `trial_reminder_sheet_result` | `result` may be `starter` | Day-3 sheet |
| `paywall_shown` | `trigger_feature` = `trial_reminder_starter` (only after a tap on the starter offer) or `today_card` ("See Premium" on a quota card) | Paywall entries from first week |

Backend: `moment.scheduled` and `moment.sent` for `FIRST_WEEK_STEP` must arrive person-less (fresh random `distinct_id`, `$process_person_profile: false`) with only the allowlisted properties of `moment_privacy.PERSONLESS_MOMENT_EVENT_PROPERTIES` (`moment_type` is allowed there; `moment_id`, user id and dedup key are not). The FCM payload of the push itself carries no `moment_type`.

Negative checks (any hit is a privacy bug for flutter-mobile or backend-api): no `session_date`, `replaces_date`, `tone`, `step`, `variant` or `copy_key` property on any first-week client event; no `moment_type` on any client event about the plan-step push; no impression event for the starter offer on the day-3 sheet; the plan-step push's `moment_id` never on an identified event.

Known coverage gap at the time of writing: the Art. 9 consent step (side cards, Settings editor) fires no PostHog event on the integration branch or in the fe9 changes, so "consent shown, allowed, not now" cannot be counted. `consent_granted` exists only for the onboarding GDPR step. A consent decision is close to a health signal, so the lead and security-guardian decide the shape (person-less counts, or accept the gap) before flutter-mobile adds it.

## 7. What waits for the App Store release

- **Lawyer, COPY.md 14.8:** (1) two consent texts resting on one ARTICLE9_HEALTH record, and which text and source the record stores (today every editor sends `source: 'settings'`); (2) completeness of the purposes, once backend owners list every use of session dates and the in-therapy status (AI prompts, connected therapist, summaries); (3) the in-therapy status inferred from a schedule write; (4) what withdrawal does to stored session times, then the `settings_confirmWithdrawArt9` and `settings_useTherapyDataSubtitle` copy; (5) US consumer-health-data laws (for example Washington's My Health My Data Act); (6) the German consent text mojibake (fix shipped in this build per 14.10, lawyer confirms the repaired text); (7) formal versus informal register of consent texts in de and fr.
- **Privacy notice** (WP-0 L-6 and delta "Transparency"): plan-step reminders and their timing, the follow-up question, the day-7 observation.
- **Lead:** record the D-L1 acceptance next to SPEC 5 and in the lawyer bundle.
- **backend-api, this sprint, not blocking TestFlight:** D-L1 fix 1 (cap reservation without the tone rule) and fix 2 (schedule `purge_old_terminal_moments`); I-8, I-9, I-10.
- **Operator decisions:** gentle tone and the starter offer (contract 14.1 item 6); store setup of `ms_starter_package` as non-consumable on both stores (14.1 item 8); `ART9_SCHEDULE_GATE_ALL_CLIENTS`.
- **security-guardian:** `symptom_scored` sending `score_bucket` per person (contract 14 item 9), before the WP-4 release.
- **Store promotion itself** is manual: App Store Connect (TestFlight to review) and Play Console (internal to production). `app-release` stops at TestFlight and the Play internal track.

## 8. Contract status, backend versus Flutter (14.2 items 10 to 14, checked 2026-10-11)

Backend: `feat/first-week-home` at `6bd0e3e`. Flutter: the FE integration worktree at `bed441f`, read-only; uncommitted work in `fw/fe8-ux-home` and `fw/fe9-ux-session` read with `git diff`, not run.

| Item | Backend | FE integration branch | In flight |
|---|---|---|---|
| 10. Side cards open `SessionSetupScreen` | Contract only | **Gap:** `side_card.dart` opens the session sheet (`FirstWeekSessionSheetEntry.addSession`) | fe9 routes `addSession` to the consent step, then `SessionSetupScreen` (uncommitted) |
| 11. `rest` and `open` lead to `/first-week/check-in` on Free without Reflect messages | `_open_rest_route` in `plan_engine.py` | **Matches:** the card follows `cta_route` through the allowlist, and the CTA label switches to the quick check-in. Copy nit: the `open` body (`firstWeek_hiddenBody`, "Talk about whatever is on your mind...") and the gentle bodies still invite a talk above a check-in button | |
| 12. `today.session_date`, sent as `replaces_date` | `FirstWeekTodayCard.session_date` (`Optional[date]`, key always present) | **Gap:** `TodayCard` has no `sessionDate`. `replaces_date` comes from `plan.nextSessionAt` in the device zone, or from the `after` step's date. Wrong for "Session moved?" on an `after` card, and off by a day when the device zone differs from the profile zone; the server then answers 422 `replaces_date_not_a_session` | fe9 adds `sessionDate`, prefers it in `sessionDateForEntry`, and adds both keys to `reflect_analytics_guard.dart` (uncommitted) |
| 13. Plan `rhythm.available[].free_limits` and `rhythm.on_free` | `FirstWeekRhythm` in `schemas/first_week.py` | **Matches:** the plan and the recap share one parser, so the plan's rhythm sheet gets the limits too. Doc comments still say "recap only" | |
| 14. Drop accepts an open `prep` ("Session moved?" then "Not sure yet") | `drop_today` drops `prep` and that session's `after`; route docstring still says "after" only | **Gap:** "Not sure yet" sends the drop only on the "It didn't happen" path (`movedFromAsk`) | fe9 drops on every "Not sure yet" (uncommitted) |

Backend deploys first, so a client never meets a backend without item 14 (no 409 fallback is needed in production).
