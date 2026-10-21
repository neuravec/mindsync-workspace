# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository. It is the single source of truth for project context, team structure, and coordination rules.

## Project Overview

MindSync is a mental health companion app with two components:
- **Backend** (`MindSync/`): Python 3.12.2 FastAPI REST API deployed on Heroku
- **Frontend** (`mindsync-frontend/mindsync_app/`): Flutter 3.27.0 / Dart 3.6.0 cross-platform mobile app

## Wspólny workspace i synchronizacja z partnerem (OBOWIĄZKOWE, każda sesja)

Z tym workspace pracują dwie osoby, każda z własnym Claude. Workspace to repo
`neuravec/mindsync-workspace`, a w środku leżą osobne repo kodu (`MindSync`,
`mindsync-frontend`, `therapist-deck`, `Mindsync-fleet`) oraz repo `social`. Instalacja,
dostępy i konta: `ONBOARDING.md`.

1. **Początek pracy: pull wszystkiego.** Hook SessionStart (`.claude/settings.json`) uruchamia
   `python scripts/workspace/sync.py pull` i wkleja raport do kontekstu. Przeczytaj go przed
   pierwszą zmianą. Jeśli raportu nie ma (hook nie zadziałał, sesja wznowiona po przerwie),
   uruchom tę komendę sam, zanim cokolwiek zmienisz. Konflikt, pominięty pull albo rozjazd
   gałęzi zgłoś użytkownikowi na początku odpowiedzi i nie pracuj na nieaktualnym stanie bez
   jego zgody.
2. **Koniec pracy: zawsze zapytaj o commit i push.** Gdy użytkownik kończy pracę albo
   zamykasz większy etap, uruchom `python scripts/workspace/sync.py status`, pokaż w kilku
   punktach, co zmieniło się w workspace i w social, i zapytaj: „Czy zrobić commit i push na
   wspólne repo, żeby partner miał aktualny stan?”. Pytaj także wtedy, gdy zmiany są tylko
   w pamięci (`claude-memory/`) albo w kolejkach bloga i Instagrama. Po zgodzie:
   `python scripts/workspace/sync.py push -m "<krótki opis po polsku>"`. Bez zgody nic nie
   wypychasz. Gdy skrypt zgłosi możliwy sekret albo konflikt, zatrzymaj się i pokaż to
   użytkownikowi.
3. **`sync.py push` obejmuje tylko workspace i social.** Repo kodu mają własne zasady
   (gałęzie, testy, push na `main` backendu to deploy na produkcję, push na `dev` frontu to
   build na TestFlight) i nigdy nie są wypychane tym skryptem.
4. **Publikuje jedna maszyna.** Dripy bloga i Instagrama działają z Harmonogramu zadań tylko
   na komputerze Mikołaja. Na innej maszynie ich nie rejestruj. Ręczna publikacja na drugiej
   maszynie (blog, Instagram, Loops): najpierw pull, a zaraz po publikacji commit i push stanu
   kolejki (`published-log.json`, statusy wpisów i postów). Inaczej drip opublikuje ten sam
   wpis drugi raz.
5. **Sekrety nigdy do repo.** `.env`, tokeny, klucze podpisu (`itmesh/`) i logi z danymi
   użytkowników są w `.gitignore`. Nowy sekret to nowy klucz w odpowiednim `.env.example`
   (bez wartości) i wpis w menedżerze haseł.
6. **Pamięć jest wspólna.** Pamięć Claude leży w `claude-memory/` (ustawienie
   `autoMemoryDirectory` w `.claude/settings.local.json` każdej osoby). Notatki pisz tak,
   żeby zrozumiała je druga osoba: kto zdecydował, kiedy i na jakim stanie.

## Change Safety & Impact Recon (MANDATORY — applies to EVERY change, no exceptions)

**Never ship a change in isolation. Before writing code AND before deploying, map the blast radius** — what else reads, imports, runs, or depends on the thing you touched — and verify the change is safe across all of it. A change that looks local is rarely local. This rule exists because a one-line model change (a single enum column) crash-looped the entire production backend for ~38 minutes (H10), dumping existing users back into onboarding.

For every change, the implementing agent MUST explicitly check and report:

1. **Who consumes this?** Grep for every importer/caller of the symbol, table, column, endpoint, schema, or config key you changed. List them. A removed/renamed/retyped field breaks every consumer — backend layers AND the Flutter client AND background jobs.
2. **What runs it at boot?** `app/main.py` imports the full router tree and runs `Base.metadata.create_all(bind=engine)` on **every** web boot. A bad model/import/lifespan call does not fail one request — it crash-loops the whole web dyno (total outage). Treat anything reachable from import or lifespan as boot-critical.
3. **Model ↔ migration ↔ prod DB must agree.** The Alembic migration + the live prod DB are the source of truth, not the model. Prod has **enum drift** (UPPERCASE labels in prod, e.g. `IN_PROGRESS`/`HERO_INSIGHT`) and orphaned tables. NEVER introduce a SQLAlchemy `Enum(PyEnum)` whose PG labels (member NAMES) disagree with its `server_default`/inserted VALUES — it is self-inconsistent and fails on Postgres. Prefer `String(n)` columns + a Python enum of constants (see `UploadSession`), matching what the migration declares.
4. **SQLite tests ≠ Postgres reality.** The test suite runs on SQLite, which silently tolerates native-enum/DDL problems that are FATAL on Postgres. For any model/DDL/enum change, add an offline Postgres check (compile DDL with the `postgresql` dialect, or import the app) — do not trust green CI alone.
5. **Deploy ≠ migrate (Heroku has no release phase).** Migrations are run MANUALLY. A deploy that adds/changes a table or column will crash-loop or 500 until `alembic upgrade head` is run on Heroku. Sequence it: deploy + migrate together, and keep boot resilient so a migration lag degrades one feature instead of taking the app down.
6. **Cross-layer contracts.** A backend response-shape or status change must be traced to its Flutter consumer (`lib/data/api`, repositories, BLoC). A backend ERROR must never be interpreted by the client as "new user / needs onboarding" — verify failure modes, not just the happy path.
7. **Verify offline before prod**, per `feedback_no_live_api_experiments`: reproduce the boot/flow locally (import the app, compile the DDL, run the targeted suite) before pushing.

If recon surfaces impact on files you don't own, STOP and coordinate through the lead — do not edit across ownership boundaries. The lead must not mark any task done until this recon is reported.

## Backend Commands (Python/FastAPI)

```bash
# Install dependencies
pip install -r MindSync/requirements.txt

# Run locally (dev)
python -m uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload

# Run with gunicorn (production)
gunicorn --config app/gunicorn.conf.py app.main:app

# Run tests
python -m pytest app/tests/
python -m pytest app/tests/test_time_utils.py  # single test

# Database migrations (Alembic)
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Background workers (Heroku processes)
rq worker --url $REDISGREEN_URL
rqscheduler --url $REDISGREEN_URL

# Docker
docker build -t mindsync:latest MindSync/
docker run -p 3100:3100 -e PORT=3100 mindsync:latest
```

Heroku Procfile runs three processes: `web` (uvicorn), `worker` (rq), `scheduler` (rqscheduler).

## Frontend Commands (Flutter)

```bash
cd mindsync-frontend/mindsync_app

# Install dependencies
flutter pub get

# Code generation (JSON serialization, freezed, build_runner)
flutter pub run build_runner build --delete-conflicting-outputs

# Asset generation
fluttergen

# Run
flutter run

# Lint
flutter analyze

# Test
flutter test

# Build releases
flutter build apk --release
flutter build ipa --release
```

CI/CD uses Codemagic (`codemagic.yaml`) — PR builder on `dev` branch PRs, auto-versioning on `dev` push, release to Google Play and App Store.

---

## Architecture

### Backend Layered Structure (`MindSync/app/`)

```
app/
├── main.py              # FastAPI entry point, middleware, lifespan
├── api/v1/endpoints/    # Route handlers (users, conversations, dashboard, analytics, summaries)
├── services/            # Business logic (OpenAI, analytics, notifications, subscriptions, PDF)
├── crud/                # Database CRUD operations (SQLAlchemy queries)
├── models/              # SQLAlchemy ORM models (User, Conversation, Message, Emotion, etc.)
├── schemas/             # Pydantic request/response validation models
├── core/                # Config (Pydantic Settings from .env), database session, auth deps
├── tasks/               # RQ background jobs (summaries, charts, subscriptions, notifications)
└── alembic/             # Database migration scripts
```

**Request flow**: Endpoint → Service → CRUD → Database. Dependencies injected via FastAPI `Depends()`.

**Configuration**: All settings loaded via Pydantic `BaseSettings` from `.env` file (`app/core/config.py`). Requires DATABASE_URL, OPENAI_API_KEY, FIREBASE_CREDENTIALS, Azure AD credentials, and various prompt templates.

### Frontend BLoC Architecture (`mindsync_app/lib/`)

```
lib/
├── main.dart                # App entry, Firebase init, DI setup
├── bloc/                    # BLoC/Cubit state management classes
├── data/
│   ├── api/                 # Dio HTTP client, API service classes
│   ├── models/              # Data models (freezed + json_serializable)
│   └── repositories/        # Repository pattern over API services
├── ui/
│   ├── screens/             # Full-page screens
│   └── widgets/             # Reusable UI components
└── utils/                   # Helpers, constants, extensions
```

**State management**: BLoC/Cubit pattern with `flutter_bloc`. Dependency injection via `GetIt`.
**HTTP**: Dio client with Firebase auth token interceptor.
**Auth**: Firebase Authentication (Apple, Google OAuth).
**Real-time**: WebRTC for voice interactions.

### Key Data Model Relationships

- User (Firebase UID as PK) → UserProfile, UserPreferences, UserSubscription (one-to-one)
- User → Conversations → Messages (one-to-many chain)
- Conversations → ConversationTopics → Emotions/Sentiments (extracted by AI)
- ConversationSummary generated per conversation and per time period (daily/weekly/monthly/yearly)
- User → UserStreaks, UserAchievements, UserMilestones (gamification — one-to-many)

### Background Job System

RQ Scheduler dispatches periodic tasks:
- **Daily**: Generate daily summaries, update charts, check notification triggers
- **Weekly**: Generate weekly summaries (handles both SUN and MON week-start preferences)
- **Monthly/Yearly**: Generate period summaries and charts
- **Hourly**: Deactivate expired subscriptions
- **Continuous**: Auto-close idle conversations

**RQ queue priority (added 2026-08-20, MSV3.3.Fix.1 queue-contention follow-up):** the `worker` process drains two queues in priority order, `rq worker --url $REDISGREEN_URL high default` (Procfile). `high` is for user-triggered/interactive jobs ("Generate Now" and similar); every scheduled cron job registered in `app/core/rq_scheduler_setup.py` still enqueues onto `default` (`queue_name="default"` on every `scheduler.cron(...)` call) and bulk/backfill work stays on `default` too. Root cause this fixed: a single zero-concurrency worker servicing one unprioritized `"default"` queue let an hourly bulk-generation cron (thousands of per-user jobs) starve an interactive tap for 20+ minutes until the stale-PROCESSING sweep killed it — see `db-reports/2026-08-20-weekly-summary-generate-now-stuck.md` for the full trace.

**CO-DEPLOY CONSTRAINT — do not split this:** the `high` queue only helps if both halves ship together. Backend code must call `Queue("high", connection=redis_client).enqueue(...)` (see `app/core/rq_queue.py`) for interactive call sites, and the Procfile must list `high` before `default`. Backend and Procfile live in the same Heroku slug, so a single `git push heroku main` deploys both atomically — but if the enqueue-side change ever ships in a commit that gets deployed without this Procfile line (e.g. a partial/rolled-back deploy), interactive jobs land on a queue **nobody drains** and never run at all — strictly worse than the pre-fix behavior of eventually running late. No migration is involved in this change (code + Procfile only), so this is not caught by the usual "deploy ≠ migrate" checklist — it needs its own reminder.

**Known limitation — priority ordering, not preemption:** RQ picks a worker's *next* job by queue priority, but a single worker still runs one job to completion before picking again. If the worker is already mid-way through a giant synchronous bulk job when an interactive `high` job is enqueued, that interactive job still waits for the bulk job to finish — the priority queue does not interrupt it. The durable fixes (chunking the bulk cron so no single run monopolizes the worker for tens of minutes, and/or adding worker capacity) are tracked as follow-ups, not yet implemented; see integration-devops memory for the cost/trade-off writeup before scaling anything.

### External Services

- **OpenAI**: GPT-4o/4o-mini for conversation AI, Whisper for speech-to-text, TTS for text-to-speech, embeddings for semantic search
- **Firebase**: Authentication, Cloud Messaging (push notifications), Analytics
- **Azure**: PostgreSQL database with Azure AD authentication
- **Redis**: Task queue via RQ/RQ-Scheduler (Heroku RedisGreen add-on)
- **Loops**: Email marketing campaigns
- **Apple/Google**: In-app purchase receipt verification

### API Routes

All backend routes are prefixed with `/api/v1/` and organized under:
- `/users/` — Registration, profiles, preferences, subscriptions, receipt verification
- `/conversations/` — CRUD, messaging, voice processing, closing
- `/dashboard/` — Summary cards, charts, mental health card
- `/analytics/` — Emotion trends, topic analysis, sentiment tracking
- `/summaries/` — Daily, weekly, monthly, yearly summaries
- `/gamification/` — Streaks, achievements, milestones, progress (planned)
- `/clinician/` — Clinician portal: magic-link auth (`/auth/request`, `/auth/verify`), patient list, patient detail, patient timeline, invite management (issue/cancel), consent management (clinician-side revoke); all routes require a clinician JWT issued after magic-link verification
- `/clinician/patients/{user_id}/consent` — Patient-facing consent management (patient revokes their own data-sharing consent by consent_id)
- `/admin/clinicians` — Admin endpoint (ADMIN_API_KEY protected) to create the first clinic and clinician accounts; required for bootstrapping since there is no self-registration flow

---

## Agent Team Structure

This project uses Claude Code Agent Teams. The team lead orchestrates the specialist agents below.

### Team Lead — Orchestrator (You)

**Role**: Task decomposition, coordination, conflict resolution, synthesis. You do NOT write code.

When you receive a task:
1. Analyze the task and identify which agents are needed.
2. Decompose into subtasks with clear boundaries (goal, files, definition of done).
3. Identify dependencies between subtasks — what must finish before what.
4. Spawn agents with rich prompts including file paths, constraints, and done criteria.
5. Monitor progress, resolve blockers, mediate conflicts.
6. When agents finish, verify no file conflicts occurred and synthesize results.
7. Report completion to the user.

**Delegation rules**:
- If a task touches only one agent's domain → spawn that agent.
- If a task spans multiple domains → spawn all involved agents with dependency ordering.
- If a task has unclear scope → analyze first, then decompose.
- Never start coding yourself. If you catch yourself writing implementation code, stop and delegate.

### Agent Roster

| Agent | Domain | Model | Color |
|-------|--------|-------|-------|
| `backend-api` | FastAPI endpoints, services, CRUD, models, schemas, migrations | `opus` | green |
| `data-analytics` | OpenAI integrations, analytics services, background jobs, summaries, prompts | `opus` | pink |
| `flutter-mobile` | All Flutter UI, BLoC, models, repositories, API clients | `opus` | yellow |
| `integration-devops` | API contracts, deployment, auth flows, env config, CI/CD | `opus` | red |
| `ui-ux-designer` | UX audits, design specs, accessibility, mental health UX patterns | `opus` | purple |
| `qa-testing` | Run tests, write missing tests, verify coverage, regression checks | `opus` | orange |
| `security-guardian` | Security audits, GDPR compliance, privilege escalation, vulnerability review | `opus` | maroon |
| `growth-analyst` | **Business/product data analysis** — churn, retention, activation, monetization, growth. Pulls PostHog + prod Postgres + revenue, writes insight reports to `analytics-reports/` | `opus` | cyan |
| `competitive-strategist` | **Competitive intelligence & product strategy** — traction-verified competitor teardowns (Ahrefs + app-store review mining + web), honest self-diagnosis, light-pivot recommendations. Writes strategy reports to `competitive-reports/` | `opus` | blue |
| `database-administrator` | **Operational prod Postgres** — read-only diagnostic/audit SELECTs, value fill-rate & data-integrity checks, schema/enum-drift inspection (model vs live prod), Alembic migration-state verification, data-quality bug triage. Owns the Azure-DB-via-Heroku-dyno access recipe. Writes reports to `db-reports/` | `opus` | teal |
| `posthog-data-extractor` | **PostHog data extraction** – read-only HogQL pulls (funnels, DAU/retention/cohorts, feature usage, platform & app-version splits, error volumes), event/property verification. Owns the REST-API access recipe + `scripts/posthog_query.py`. Writes raw extracts to `analytics-reports/raw/` | `opus` | magenta |
| `ticket-agent` | **ClickUp ↔ codebase translator, both directions** – turns shipped commits/reports into business-readable tickets (parent + subtasks, no jargon), and turns backlog tickets into TASK/AGENT/FILES/DONE_WHEN work orders. Owns the ClickUp access recipe + `scripts/clickup.py` | `opus` | gold |

> **Model selection:** every agent uses the `opus` alias except `general-web-search-agent`, which uses `sonnet`. Always use the alias (`opus` / `sonnet`) in agent frontmatter, never a pinned ID like `claude-opus-5-5`: the alias resolves to the newest model of that family, so agents upgrade automatically with each new Claude release. Pin a full ID only deliberately, to freeze behavior.

> **Business & Growth track:** `growth-analyst` (inward — our PostHog/Postgres/revenue) and `competitive-strategist` (outward — competitors & market) are read-only business agents that own **no code files**; their only output is a Markdown report (`analytics-reports/` and `competitive-reports/` respectively). They are complementary: the strategist cites/requests growth-analyst reports for internal validation rather than querying our data itself. Spawn on-demand for "why/what-to-change" questions, not trivial lookups.

> **`database-administrator` (operational, read-mostly):** owns **no app code or migration files** (`backend-api` still owns models + `app/alembic/`). It is the specialist for *reaching and reading the production database*: the Azure DB host is unreachable locally (no public DNS), so the only working path is a **Heroku one-off dyno running a REPL-safe Python script** (`heroku run -a mindsync python < script.py`, then `heroku ps:stop run.NNNN`). It runs **read-only `SELECT` only** (no DML/DDL on prod without explicit operator approval), verifies migration state / prod-vs-model drift, and hands schema/migration changes to `backend-api`. Deliverable: results + a `db-reports/` report. Spawn it to query prod, audit the schema, confirm a migration ran, or check whether data is actually being persisted.

> **`posthog-data-extractor` (read-only):** the PostHog counterpart of `database-administrator`. It owns the *access recipe*: the **PostHog MCP/OAuth flow does NOT work in this environment** (it burns turns and fails at `complete_authentication`), so all access goes through the read-only REST query API via **`scripts/posthog_query.py`** with `POSTHOG_PERSONAL_API_KEY` (project 141170, EU). It runs HogQL `SELECT` only, **verifies an event actually flows before reporting a number**, and never mutates PostHog (no insights/dashboards/cohorts/flags/experiments, no person deletion) and never edits app code. Deliverable: results + a raw extract under `analytics-reports/raw/`. Spawn it for any "give me the numbers from PostHog" request, and as the data-pull subcontractor for `growth-analyst` (which interprets; the extractor extracts). For revenue/account truth use `database-administrator` instead – PostHog cannot answer those.

> **`ticket-agent` (ClickUp, writes tickets not code):** the only agent that talks to ClickUp. Access goes through **`scripts/clickup.py`** with `CLICKUP_API` from **`Heroku/.env`** (workspace 9015587939, working list Features `901504408777`); descriptions MUST be sent as `markdown_content` or ClickUp stores escaped literals. Outbound it writes for a **non-technical reader** – no file names, hashes, event names or jargon in a description, every change explained by its effect on the user or the money, humanized prose, technical trace parked in a ticket **comment** instead. Inbound it reads a ticket plus subtasks and comments and emits work orders naming the owning domain agent from the map below. It **never deletes anything in ClickUp**, never restructures a ticket that already has subtasks unless asked, and never implements the work itself – it hands off to the lead. Spawn it for "wrzuć to na ClickUp", "popraw opis ticketa", "co mamy w backlogu", "rozpisz ten ticket na zadania".

### File Ownership Map (CRITICAL — No Overlaps)

**`backend-api` owns:**
- `app/api/v1/endpoints/users.py`
- `app/api/v1/endpoints/conversations.py`
- `app/api/v1/endpoints/gamification.py` (streaks, achievements, milestones)
- `app/services/` — EXCEPT `analytics.py` and `openai_service.py`
- `app/services/gamification.py` (streak calculations, achievement triggers, milestone checks)
- `app/crud/` — EXCEPT analytics-specific CRUD files
- `app/models/` — all SQLAlchemy models (coordinates with data-analytics on schema)
- `app/schemas/` — EXCEPT analytics/summary-specific schemas
- `app/core/` — config, database, auth dependencies
- `app/alembic/` — all migration files
- `app/main.py`
- `app/tasks/subscriptions.py`
- `app/tasks/gamification.py` (daily streak updates, achievement checks)

**`data-analytics` owns:**
- `app/services/analytics.py`
- `app/services/openai_service.py`
- `app/tasks/summaries.py`
- `app/tasks/charts.py`
- `app/tasks/notifications.py` (analytics-triggered notifications)
- `app/api/v1/endpoints/analytics.py`
- `app/api/v1/endpoints/summaries.py`
- `app/api/v1/endpoints/dashboard.py`
- `app/schemas/` — analytics and summary schemas only (e.g., `analytics.py`, `summary.py`)
- `app/crud/` — analytics and summary CRUD only
- `app/models/conversation_summary.py` and any analytics-specific models

**`flutter-mobile` owns:**
- `lib/ui/` — ALL screens and widgets, including `lib/ui/screens/dashboard/`
- `lib/bloc/` — all BLoC/Cubit classes
- `lib/data/models/` — all Freezed data models
- `lib/data/repositories/` — all repositories
- `lib/data/api/` — all Dio API service classes
- `lib/main.dart` — DI setup, app init
- `lib/utils/` — helpers, constants, extensions

**`integration-devops` owns:**
- `MindSync/Procfile`
- `MindSync/requirements.txt`
- `MindSync/.env.example`
- `mindsync-frontend/codemagic.yaml`
- Firebase config files (`google-services.json`, `GoogleService-Info.plist`)
- Deployment scripts, Docker files
- This `CLAUDE.md` file (maintains it as living document)

**`ui-ux-designer` owns:**
- No code files — read-only design consultant
- Produces design specifications, audit reports, and accessibility assessments
- Hands off specifications to flutter-mobile for implementation

**`qa-testing` owns:**
- `app/tests/` — all Python backend test files
- `mindsync-frontend/mindsync_app/test/` — all Flutter test files
- Reads any file for testing context, but only edits test files

**`security-guardian` owns:**
- No code files — read-only security auditor
- Can read any file for security audit purposes
- Produces security reports; domain agents implement the fixes

**`posthog-data-extractor` owns:**
- `scripts/posthog_query.py` – the read-only HogQL/REST runner (its only code file)
- `analytics-reports/raw/` — raw PostHog extracts (top-level `analytics-reports/*.md` stays with `growth-analyst`)
- No app code, no migrations, and **no PostHog artifacts** — it never creates or edits insights, dashboards, cohorts, flags, or experiments (`scripts/posthog_build_dashboards.py` is operator-run, not agent-run)

**`ticket-agent` owns:**
- `scripts/clickup.py` – the ClickUp read/write runner (its only code file)
- ClickUp ticket bodies and comments in the Features list — no other agent writes to ClickUp
- No app code, no migrations, no reports owned by other agents (it *reads* `analytics-reports/`, `db-reports/`, `design-specs/` as source material)

**Shared files — require coordination through the lead:**
- `app/models/` — if data-analytics needs a new model, it defines the schema and backend-api creates the migration
- `app/alembic/` — only backend-api runs `alembic revision`, but data-analytics can request schema changes
- `lib/data/api/` — flutter-mobile owns these, but changes must match API contracts verified by integration-devops

### Dependency & Sequencing Rules

When tasks span multiple agents, follow these ordering rules:

1. **Database schema changes**: `data-analytics` or `backend-api` defines requirements → `backend-api` creates migration → both can proceed with their layers.
2. **New API endpoint**: `backend-api` or `data-analytics` implements backend → `integration-devops` verifies contract → `flutter-mobile` integrates frontend.
3. **API contract changes**: `integration-devops` reviews impact FIRST → then backend changes → then frontend changes.
4. **Deployment**: `backend-api` code ready → `integration-devops` deploys backend → verify → `flutter-mobile` code ready → `integration-devops` deploys frontend.
5. **Analytics features**: `data-analytics` builds backend logic + defines response schemas → `flutter-mobile` builds dashboard UI consuming those schemas.

### Inter-Agent Communication Protocol

Agents coordinate through the shared task list and direct messages. Follow these rules:

- **Blocking dependency**: If Agent A needs Agent B to finish first, create the task with a dependency. Don't poll — the system auto-unblocks.
- **API contract handoff**: When `data-analytics` or `backend-api` creates/changes an endpoint, they must message `integration-devops` with the full request/response schema. `integration-devops` then messages `flutter-mobile` with the verified contract.
- **Schema change request**: If `data-analytics` needs a new DB column, it messages `backend-api` with: table name, column name, type, nullable, default, and migration description.
- **Cross-cutting concern**: If any agent discovers their change affects another agent's files, they STOP and message the lead. Do not edit files you don't own.
- **Conflict escalation**: If two agents need to modify the same file, escalate to the lead immediately. The lead will sequence the changes.

### Task Format (Required for All Subtasks)

Every task assigned to an agent must include:
```
TASK: [Clear one-line description]
AGENT: [agent name]
FILES: [Specific files/directories to create or modify]
DEPENDS_ON: [Task IDs that must complete first, or "none"]
DONE_WHEN: [Explicit, verifiable completion criteria]
CONTEXT: [Any relevant details — related tasks, constraints, API contracts]
```

### Cross-Review Protocol

After implementation, the lead spawns ONE reviewer agent (not all of them) to save tokens:
- Backend code → spawn `backend-api` to review `data-analytics` work, or vice versa
- API contract changes → spawn `integration-devops` to verify consistency
- Frontend integration → spawn `flutter-mobile` to verify contract match
- New feature pre-deployment → spawn `security-guardian` to check auth and data scoping
- UI changes → spawn `ui-ux-designer` to verify design quality and accessibility
- The lead picks the most relevant reviewer. Full cross-review is reserved for high-risk changes only.

### Testing Enforcement (Mandatory)

No task is complete without tests. The lead MUST verify before marking done:

**Backend tasks** (backend-api, data-analytics):
- Unit tests for new/modified service functions
- Endpoint tests covering happy path, error cases, auth scenarios
- Background job tests verifying idempotency
- The implementing agent writes tests as part of the task — not as a separate follow-up

**Frontend tasks** (flutter-mobile):
- Widget tests for new screens
- BLoC tests covering all state transitions (initial → loading → loaded/error)
- `flutter analyze` passes with no errors

**Cross-cutting tasks**:
- Integration-devops verifies end-to-end flow after both sides are implemented
- Auth flow changes require a manual trace through all 6 steps (documented in integration-devops config)

**Quality assurance (qa-testing)**:
- Spawn `qa-testing` after any non-trivial feature implementation to run the full test suite
- Spawn `qa-testing` to write tests when the implementing agent has coverage gaps
- Before any production deployment, spawn `qa-testing` to confirm nothing is broken

**Security (security-guardian)**:
- Spawn `security-guardian` before deploying any new endpoint that handles user data
- Spawn for any auth flow change, subscription change, or data deletion feature
- Critical or High findings from security-guardian BLOCK deployment

**Design quality (ui-ux-designer)**:
- Spawn `ui-ux-designer` when implementing new screens or redesigning existing ones
- Spawn before user-facing feature launches to check accessibility and mental health UX

**Test commands for reference:**
```bash
# Backend
python -m pytest app/tests/ -v
python -m pytest app/tests/test_specific.py -v

# Frontend
flutter test
flutter analyze
```

### PostHog Instrumentation (Mandatory final step, added 2026-10-02)

No feature, screen, flow or limit change is complete until it is measurable in PostHog. This is a required closing step of every task, on the same level as tests. The lead MUST verify it before marking a task done.

For everything that was built or changed, the implementing agent must:
1. **List what a user can see and do** in the new or changed surface (screen viewed, primary and secondary actions, skips and dismissals, errors, outcomes of purchases and permissions) and map each to a PostHog event. Report this as a coverage table: `surface | user action | event name | key properties | where it fires (file)`. A row without an event is a gap, and gaps block completion.
2. **Reuse the existing taxonomy** (`lib/core/analytics/analytics_events.dart` on the client, `app/services/posthog_service.py` on the backend): existing event names and property keys first, new ones only when nothing fits, snake_case, stable once shipped. Paywall entries always carry `trigger_feature`. Funnel steps carry a step name and index.
3. **Keep a funnel intact end to end**: every multi-step flow (onboarding, purchase, trial, offer) must be reconstructable in PostHog from first screen to outcome, including the "did nothing / skipped" branch. Emit each fact once, on one side (client or backend), never on both.
4. **Privacy**: never send free text the user wrote (notes, goals, names of habits, reflections), health details, emails or tokens. Counts, enums, booleans and durations only. Add or extend the test that guards this where one exists.
5. **Test it**: a unit or widget test asserts that the event fires with the expected properties. After release, `posthog-data-extractor` confirms the event actually flows before anyone reports numbers from it.

The lead closes the task only with the coverage table in the report and zero gaps, or with each remaining gap explicitly accepted by the operator.

### Budget-Aware Orchestration Rules

This project runs on Claude Max. Agent Teams consume tokens fast. The lead MUST follow these rules:

1. **Spawn only the agents needed** — if a task is pure backend, don't spawn flutter-mobile. If it's pure frontend, don't spawn backend agents.
2. **Simple tasks → single agent** — don't spawn a team for "fix this typo" or "add a field to this schema."
3. **Cross-review is selective** — only spawn a reviewer for medium/high complexity changes. Low-risk changes (adding a field, fixing a bug) get self-verified by the implementing agent.
4. **Prefer sequential over parallel when budget is tight** — parallel is faster but burns more tokens. Use parallel for large features, sequential for smaller tasks.
5. **Effort tuning** — for simple implementation tasks, use low/medium effort. Reserve high/max effort for architecture decisions, complex debugging, and prompt engineering.
6. **Specialist agents are on-demand** — `ui-ux-designer`, `qa-testing`, and `security-guardian` are reviewers/validators, not always active. Spawn them at the right checkpoints, not for every task.
7. **qa-testing is mandatory pre-deployment** — always spawn before pushing to production, even for small changes.
8. **security-guardian for new data endpoints** — any endpoint touching user mental health data needs a security review before deployment.

---

## Feature Domains

### Gamification System (Planned)

Gamification features span backend-api (logic + storage) and flutter-mobile (UI). The system includes:

**Streaks**: Track consecutive days of journaling/conversations.
- Backend: `app/models/user_streak.py`, `app/services/gamification.py`, `app/tasks/gamification.py`
- Frontend: streak display widget, streak recovery prompts
- Background job: daily streak calculation + freeze/break detection

**Achievements**: Milestone-based badges (e.g., "First Week", "100 Conversations", "Emotion Explorer").
- Backend: `app/models/user_achievement.py`, achievement trigger logic in `app/services/gamification.py`
- Frontend: achievement cards, unlock animations, achievement gallery screen

**Milestones**: Progress markers in the user's mental health journey.
- Backend: milestone definitions, progress calculation
- Frontend: milestone timeline, progress indicators

**Agent responsibilities:**
- `backend-api` owns ALL gamification backend: models, services, CRUD, schemas, endpoints, background jobs, migrations
- `data-analytics` may contribute streak/milestone calculations that depend on analytics data (e.g., "improving sentiment trend" achievement) — coordinate via lead
- `flutter-mobile` owns ALL gamification UI: screens, widgets, animations, BLoCs
- `integration-devops` verifies gamification API contracts

### Chart Data System

Charts are a cross-cutting concern between data-analytics (backend) and flutter-mobile (frontend). Follow this contract pattern:

**Backend (data-analytics) provides chart data as structured JSON:**
```json
// Emotion trends chart
{
  "chart_type": "emotion_trends",
  "period": "30d",
  "data_points": [
    {
      "date": "2025-01-15",
      "emotions": {"joy": 0.72, "sadness": 0.15, "anxiety": 0.08, "calm": 0.55}
    }
  ],
  "metadata": {"total_conversations": 23, "date_range": {"start": "...", "end": "..."}}
}
```

**Frontend (flutter-mobile) renders using fl_chart or equivalent:**
- Receives the structured JSON via API
- Builds the chart widget using the data
- Handles empty states, loading, errors
- Never calculates analytics on the frontend — backend is the source of truth

**Contract rules for charts:**
1. `data-analytics` defines the exact JSON schema for each chart type
2. `integration-devops` verifies the contract
3. `flutter-mobile` builds the Freezed model + rendering to match exactly
4. If the chart looks wrong, debug the data first (data-analytics), then the rendering (flutter-mobile)

---

## Coding Standards (All Agents Must Follow)

### Backend (Python/FastAPI)
- Python 3.12.2 with full type hint coverage
- Async/await for all I/O operations
- Pydantic v2 for all request/response schemas
- SQLAlchemy ORM for database interaction
- Never expose SQLAlchemy models in API responses
- Structured logging for important operations
- Error handling with appropriate HTTP status codes
- All config via Pydantic Settings from `.env`
- **Tests are mandatory** — every new endpoint and service function must have tests

### Frontend (Flutter/Dart)
- Flutter 3.27.0 / Dart 3.6.0
- BLoC/Cubit pattern for all state management (no setState for complex state)
- Freezed for all data models
- Repository pattern over API services
- GetIt for dependency injection
- Handle loading, success, and error states in every BLoC
- Run `build_runner` after any model changes
- **Tests are mandatory** — widget tests for new screens, BLoC tests for state transitions

### Universal
- Never hard-code secrets, API keys, or configuration values
- Never commit credentials to version control
- Write tests for new functionality — **no exceptions, no "I'll add tests later"**
- Document public functions with clear docstrings
- Follow existing patterns in the codebase for consistency
## System blogowy MindSync (adaptacja z PLASMET zakończona 2026-08-25)

**Pisanie wpisów bloga (od 2026-09-25): WYŁĄCZNIE przez skill `/blog-write`.** Każda prośba o nowy
wpis, partię albo przepisanie wpisu uruchamia ten skill. Głos = styl Moniki (newslettery
MindSync), sesja główna nie pisze prozy wpisu sama, wpis ma pole `"glos": "monika-v1"`
i przechodzi `scripts/blog-voice-check.py`.

Kompletny pipeline „partia + drip" produkcji bloga EN na mindsync.app (Webflow CMS,
kolekcja Blog Posts `67cb62e9d0afa32a03eae3f1`, wpisy `/journal/<slug>`, listing `/blog`).
**Źródło prawdy i mapa całości: `blog/README.md`** (pipeline, mapa plików, stan adaptacji
§5, zasady twarde §6). Kluczowe lokalizacje: `.claude/agents/` (blog-writer,
seo-content-writer, brand-voice-manager, seo-tech-lead, graphic-designer,
general-web-search-agent, **webflow-publisher** – jedyny agent piszący do żywego Webflow),
`.claude/skills/` (humanizer, blog-publish), `blog/queue/_format.md` (format wpisu
i mapowanie na CMS), `blog/app-features.json` (katalog funkcji: bramka pokrycia + karty
CTA), `docs/blog/brand-mindsync.md` (brand – głos i wizual), `scripts/webflow/`
(drip-publikator Data API v2), `scripts/gsc/`, `scripts/image-gen/`,
`docs/blog-plasmet-reference/` (oryginały PLASMET). Zasady twarde: humanizer przed każdą
publikacją prozy, całkowity zakaz em-dash, najpierw bramka pokrycia potem pisanie, wpis
nigdy w ślepy zaułek, publikatory z DryRun domyślnie i publikacja na żywo tylko za zgodą
operatora, treść wpisów RichText-safe (zero div/style/script/table w post-body).

## Instagram: treść o zmianach w aplikacji (od 2026-10-01)

Pipeline Instagrama: źródło prawdy `social/README.md` i `social/CLAUDE.md`, skille `/social-write` (tworzenie, STOP przed `gotowy`) i `/social-publish`.

**Reguła:** po każdej większej zmianie wizualnej we froncie (nowy ekran, >= 80 zmienionych linii w `lib/screens|lib/widgets`, >= 3 pliki widgetów) sesja PYTA operatora, czy przygotować treść na Instagram (post o nowości, story albo rolka) przez `/social-write` w trybie feature. Nie tworzy treści bez zgody. Pytanie wyzwala automatycznie hook PostToolUse (`.claude/settings.local.json`) uruchamiający `scripts/social/ui-change-detector.py` po `git commit`; o ten sam commit pyta tylko raz. Gdy hook nie zadziała (np. zmiana scalona poza tą sesją), reguła obowiązuje i tak.

Prawdziwe ekrany do postów renderuje `python scripts/social/app-shots.py run` (testy `mindsync-frontend/mindsync_app/test/marketing_shots/`, tag `marketing`, pomijane w zwykłym `flutter test` i CI). Zakaz retuszu i dorysowywania treści na screenach.
