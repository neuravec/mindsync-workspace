---
name: onboarding-profiling-plan-4-waves-planning-2026-05-27
description: "Plan rozszerzenia onboardingu o profilowanie userów. 4 wave'y. Wave 1 (GDPR fix + age band + inclusive gender) zatwierdzony do startu, Wave 2 (challenges reframe + behavioral PostHog), Wave 3 (Article 9 currently_in_therapy + withdrawal flow), Wave 4 (lead source) — równolegle po Wave 1."
metadata: 
  node_type: memory
  type: project
  originSessionId: dc69bc9d-1cbe-403f-a209-03b7adc35779
---

**STATUS 2026-05-28: ALL 4 WAVES COMMITTED, NIE pushnięte.** 4 BE + 8 FE commitów na `dev`. Final QA verdict: READY TO DEPLOY po fix Art.9 dedicated endpoint (commit e57f6ac).

## Wave 2-4 — committed (2026-05-28)
- Backend `MindSync/`: `7fe29ca` (Wave 2 — premium_intent_score weekly job + behavioral PostHog props subscription_tier/streak_max/conversations_last_30d, 32 testów), `93023c2` (Wave 3+4 — migration pp6q7r8s9t0u: currently_in_therapy + lead_source + consent_records table, Art.9 health gate na profile update 403, 54 testów)
- Frontend `mindsync-frontend/`: `2b43026` (Wave 2 — Challenges reframe "What do you want more of?" × 7 lang, progress bar always-on totalSteps=7, AuthCubit behavioral PostHog identify, 16 testów), `52a424a` (Wave 3 — inline Art.9 consent banner w Journey, "Currently in therapy?" 4-opt question conditional, Settings privacy section z 2 toggles + withdraw flow, ConsentManager API class, Freezed ConsentRecord/ConsentStatus, 17 ARB keys × 7 lang, 19 testów), `3fb7d17` (Wave 4 — OnboardingLeadSourceView 5 chips + Other + skip, Companion → LeadSource → completeOnboarding sequence, PostHog event NOT person property, 9 ARB keys × 7 lang, 17 testów), `e57f6ac` (fix — ConsentManager.getArt9HealthStatus dedicated endpoint call, naprawia Settings Art.9 toggle + Journey Art.9 banner state pre-existing bug z Wave 3 FE)

## Final flow po 4 wave'ach
1. Sign-up (Firebase email/password lub Apple/Google)
2. **PersonaliseView** (sign-up flow): full_name + email + **age_band** + 5-opt gender + pronouns → save TO SHARED_PREFS (pending_profile_json)
3. **Legal Gate**: GDPR consent → **PostHog identify FIRST** (age_band/gender/country/platform/language z pending JSON) → **createUserProfile** (flush pending) → screen 1
4. Challenges (strengths-based copy reframe)
5. Intensity (severity sliders)
6. **Journey z inline Art.9 banner**: tick Art.9 checkbox → grantArt9HealthConsent. JEŚLI Art.9 active → pokazuje "Currently in therapy?" 4-opt question. therapy_duration ukryte jeśli currently_in_therapy IN [not_right_now, never_been]. POST profile gated 403 if currently_in_therapy set bez Art.9 consent.
7. Modality
8. Schedule
9. Companion
10. **LeadSource (NEW Wave 4)**: 5 chips + Other text + skip → PostHog event capture NOT identify → completeOnboarding → WowScreen

## Settings withdraw
- "Personalisation profiling" toggle → grant/withdraw PROFILING consent
- "Use therapy treatment data" toggle → grant/withdraw ARTICLE9_HEALTH consent (DELETE side-effect: clears currently_in_therapy w profile + property-level PostHog delete)
- 2 confirm dialogs + snackbar feedback

## Migration chain
`nn4o5p6q7r8s` → `oo5p6q7r8s9t` (Wave 1 age_band) → `pp6q7r8s9t0u` (Wave 3+4 currently_in_therapy + lead_source + consent_records). Single head verified.

## Known follow-ups (non-blocking, can deploy)
- **Test bug** `app/tests/test_onboarding_v2.py:393` — `test_preserves_therapy_data` sprzeczny z aktualnym `reset_therapy_onboarding` behavior (clears). Pre-existing pre-Wave 1, nie regression. Assign: qa-testing.
- Splash recovery dla pending profile jeśli user zamknie apkę między PersonaliseView i Legal Gate.
- Pre-existing `_timer.cancel()` late init bug w SignUpCubit close().
- gen-l10n pre-existing PL ARB `=4` syntax — manual sync w generated files (workaround).
- `loadExistingContext()` clamp do 6 — resuming user nie ląduje na LeadSource (screen 7), wraca do Companion (screen 6). Functionally OK (LeadSource skippable).
- Wave 3+4 BE decyzja: currently_in_therapy NIE wysyłane do PostHog (tylko Postgres). Jeśli okaże się potrzebne dla cohort analysis — follow-up Wave 5 po Art.9 explicit consent.

## Co user musi zrobić
1. **Code review** wszystkich 12 commitów
2. **`git push`** w obu repo (lokalne tylko, nie pushnięte)
3. **Heroku deploy backendu**: `alembic upgrade head` po push (chain do pp6q7r8s9t0u)
4. **PostHog UI**: utworzyć 5 sample cohorts:
   - Women 25-34 PL
   - Young US users (18-34)
   - Non-binary (gender=OTHER)
   - Mature users (45+)
   - Demographic unknown
5. **Privacy Policy update** — dodać sekcję o profiling consent + Art.9 health data + lead source attribution
6. **PostHog DPA review** — verify covers health-category data (nawet jeśli currently_in_therapy nie jest tam wysyłane, behavioral data + age_band + gender + intent z mental health context = quasi-health profile)
7. **Codemagic** uruchomić nowy build TestFlight + Play po push frontu

## Wave 1 — committed (5 commits, 2026-05-27)
- Backend `MindSync/`: `58dd2ad` (age_band migration oo5p6q7r8s9t, model, schema, endpoint, 21 testów), `1f3adc1` (PostHog server-side identify in POST /users/profile, 5 testów)
- Frontend `mindsync-frontend/`: `2156b03` (AgeBandSelector widget, 5-opt GenderPronounsSelector, refactored PersonaliseView, SignUpCubit defers createUserProfile to post-consent via SharedPreferences pending_profile_json, TherapyOnboardingCubit._flushPendingProfile in acceptConsent, 13 ARB keys × 7 lang, 18 testów), `44b36fb` (PostHog identify Flutter side — age_band/gender/country/platform/language, AuthCubit + splash + acceptConsent identify calls, 9 testów), `1e3cb49` (QA integration tests Phase A + Phase B, 8 testów + 7 pre-existing fixes), `7e2af71` (BUG FIX: reorder _identifyPostHogNewUser BEFORE _flushPendingProfile in acceptConsent — flush was clearing JSON before identify read demographics on success path)

## Wave 1 — key implementation details
- **GDPR fix**: SignUpCubit no longer calls createUserProfile pre-consent. Saves {full_name, pronouns, gender, age_band} as `pending_profile_json` in SharedPreferences. TherapyOnboardingCubit.acceptConsent() → identify PostHog (reads JSON for demographics) → flush (calls createUserProfile + clears JSON on success). On failure, JSON retained for retry on next acceptConsent call.
- **Backend gender enum**: pozostawiony 3-wartościowy (MALE/FEMALE/OTHER). Frontend mapuje 5 opcji UI → 3 backend: Woman→FEMALE, Man→MALE, Non-binary→OTHER, Self-describe→OTHER (z pronouns text), Prefer not to say→null.
- **PostHog person properties**: `age_band`, `gender` (backend value), `country` (z Platform.localeName), `platform` (ios/android), `language` (locale code). NIE wysłane: health-category (currently_in_therapy, primary_intent — Wave 3).
- **Cohorts dla user'a do utworzenia w PostHog UI**: Women 25-34 PL, Young US users (18-34), Non-binary, Mature users (45+), Demographic unknown.

## Known follow-ups (non-blocking)
- Splash recovery dla pending profile (jeśli user zamknie apkę między register() i acceptConsent()) — jeszcze nie zaimplementowane.
- Pre-existing `_timer` late init bug w SignUpCubit close() — out of scope tego PR, oddzielne zadanie.
- gen-l10n nie odpala czysto przez pre-existing PL ARB `=4` syntax — ARB keys dodane ręcznie też w generated files (workaround).

## Kontekst biznesowy
Email survey z 14d gratis miał 3% open / 0% completion. Strategia: in-app profiling w onboardingu zaraz po rejestracji (najwyższy engagement window).

## Główne odkrycie audytu
**`PersonaliseView` (sign-up flow) zbiera gender + name PRZED Legal Gate.** To pre-existing GDPR Art. 6 violation już dziś — łamiemy consent-before-collect przy każdej rejestracji. Profiling expansion go nie wprowadza, ale czyni palącym. Verdict security-guardian: GO-WITH-CONDITIONS.

## Co JUŻ mamy w sign-up/onboarding
- `PersonaliseView` (sign-up, przed Legal Gate): full_name, email, gender (3 opcje: male/female/other), pronouns
- `UserProfile.age` (Integer): kolumna istnieje w modelu ALE nigdy nie była zbierana z UI
- Locale + timezone: auto z device (`time_zone`, `ai_language`)
- therapy_onboarding (7 screens): Legal Gate → Challenges → Intensity → Journey → Modality → Schedule → Companion

## Decyzje podjęte (subiektywna ocena 3 agentów)
1. **GDPR fix PIERWSZY**: defer `createUserProfile()` do POST-consent (lub Legal Gate przed PersonaliseView). Pre-existing High risk.
2. **Age band TAK**, na PersonaliseView (rozsmarowanie zamiast nowego ekranu). Wrap chipów 5+1 (z "Prefer not to say"). Per UI-UX spec.
3. **Inclusive gender 3 → 5 opcji**: Woman/Man/Non-binary/Self-describe/Prefer not to say. Backend.gender to `String?` — bez migracji.
4. **Country/locale auto**: zero UI, tylko PostHog person property.
5. **"Currently in therapy?" → Wave 3** (Art. 9 special category, wymaga osobnego explicit consent).
6. **Lead source: backend only, NIE PostHog** (re-identification risk per security punkt D). 5 opcji + Other.
7. **Challenges reframe**: "What do you want more of?" — strengths-based (Headspace +7.6pp). Zero GDPR koszt.
8. **PostHog person properties split**: demografia + behavioral OK, health-category (currently_in_therapy, primary_intent) tylko backend do Wave 3.

## Wave 1 — GDPR foundation + demografia (STARTUJEMY)
- Backend: defer `createUserProfile()` do post-consent (najmniej inwazyjna opcja: SignUpCubit zbiera dane lokalnie, Legal Gate `acceptConsent()` wywołuje API z połączonymi danymi)
- Backend: Alembic migration — `user_profiles.age_band: String(16)` nullable
- Backend: endpoint update przyjmuje age_band, walidacja enum (18-24/25-34/35-44/45-54/55+)
- Flutter: `AgeBandSelector` widget — Wrap chipów (5 + "Prefer not to say"), per UI-UX spec
- Flutter: `GenderPronounsSelector` — 5 opcji zamiast 3
- Flutter: `PersonaliseView` layout per spec (name → email → age → gender/pronouns)
- Flutter: `SignUpCubit` przekazuje age_band, NIE wywołuje createUserProfile() przed consent
- Flutter: 8 nowych ARB kluczy × 7 języków
- Analytics: PostHog person properties `age_band`, `gender`, `country`
- Tests: widget + cubit + GDPR sequencing integration

**Effort**: 2-3 dni. **Risk reduction**: pre-existing High GDPR → Low.

## Wave 2 — Conversion polish (po Wave 1, równolegle z 3+4)
- Flutter: Challenges screen copy "What do you want more of?" + ARB × 7
- Flutter: progress bar always-on
- Analytics: behavioral PostHog props (subscription_tier, first_conversation_within_24h, streak_max, conversations_last_30d, premium_intent_score, platform)
- Backend: background job refresh premium_intent_score weekly
- Tests: PostHog property + analytics events

## Wave 3 — Article 9 health data (po Wave 1, równolegle)
- Backend: Alembic — `user_profiles.currently_in_therapy: String?` + `consent_records` tabela (audit trail)
- Backend: endpoints `POST /users/consent/profiling`, `DELETE /users/consent/profiling`
- Flutter: Article 9 explicit consent screen przed Journey
- Flutter: Journey screen — "Are you currently in therapy?" (single-select 4 opcje)
- Flutter: Settings screen — "Withdraw profiling consent" toggle + flow
- Backend: PostHog property-level deletion handler
- Legal: PostHog DPA review dla health data (BLOCKER), Privacy Policy update
- Tests: consent withdrawal E2E, audit trail

**Effort**: 4-5 dni + 1 tydz legal review.

## Wave 4 — Lead source (po Wave 1, równolegle z 2+3)
- Backend: Alembic — `user_profiles.lead_source: String(32)` nullable
- Backend: endpoint `PATCH /users/profile` przyjmuje lead_source
- Flutter: nowy screen po Companion (single question, single screen, skip)
- Flutter: 6 ARB kluczy × 7 języków
- **NIE wysyłamy do PostHog** — backend Postgres + Metabase/PostHog SQL ad-hoc
- Privacy Policy update: attribution mention

## Source materials
- ui-ux-designer agentId aa368ae90c749d048 — full design spec for PersonaliseView extension
- security-guardian agentId ad9159cb57ae1174e — GDPR audit z verdyktem
- data-analytics agentId a672520191896a0ff — install attribution + person properties
- Explore agent — therapy_onboarding flow audit (8 screens, Legal Gate → ... → Companion)

## Powiązane memory
- [[reference_posthog_integration]] — PostHog person properties pattern
- [[reference_posthog_gdpr_delete]] — bulk_delete API (potencjalnie property-level potrzebne w Wave 3)
- [[feedback_memory_write_after_commit]] — lesson z F1-F5 (zapisuj po commit, nie przed)
