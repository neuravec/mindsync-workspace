---
name: project-notification-moments-redesign-2026-05-14
description: "Redesign systemu notyfikacji — dwa systemy (push moments + in-app pop-upy), hybrid AI/templated, hard cutover legacy. Zatwierdzony 2026-05-14 po audycie wykrywającym P0 bugi."
metadata: 
  node_type: memory
  type: project
  originSessionId: 0440417d-53d8-4f1f-9b47-3c74e8e8e8aa
---

# Notification Moments Redesign — strategiczny plan

Zatwierdzony 2026-05-14 po audycie pokazującym 2 critical bugi (singleton FCM brak resetu po logoucie + 22:00 generic spam z health_check fallback) i ~10 P1/P2 problemów (zombie jobs, hardcoded EN text, brak observability, FCM token overflow exception).

**Why:** obecny system to scheduler-driven push z hardcoded textem, 11 togglei (3 zombie) i firowaniem o 22:00 dla wszystkich. Anty-mental-health, generic, frustrujące. User chce WOW.

**How to apply:** każda zmiana w notyfikacjach po 2026-05-14 powinna iść w kierunku Notification Moments. Nie dodawać nowych hardcoded jobów. Nie rozszerzać statycznych template'ów. Wszystkie nowe push i in-app surfaces mają iść przez Orchestrator + Detector.

## Architektura — dwa systemy równolegle

### System A — Push notifications (zewnętrzne, smart)
- **Hybrid generation**: część AI, część templated
- AI dla: post_session_reflection, mood_dip_alert, pattern_insight, weekly_recap
- Templated dla: streak_celebration, therapy_prep, symptom_check, achievement_unlock
- **Smart timing per-user**: orchestrator uczy się max engagement hour z PostHog activity, nie hardcoded 22:00
- Max 1-2 dziennie, scoring layer wybiera 1 najlepszego kandydata z puli ~8 typów
- Nowa tabela `notification_moments`: moment_type, payload, scheduled_at, sent_at, opened_at, dismissed_at, acted_at, expires_at
- `NotificationOrchestrator` service zastępuje 7 hourly cronów

### System B — In-app micro pop-upy (wewnętrzne, częste, WOW)
- Pop-up wyzwalany kiedy user już jest w apce, kontekstowy do akcji
- Bez permission gate, bez schedulera, działa zawsze
- Tabela `app_insights_shown` (dedup, żeby nie spamować tym samym)
- `InAppInsightDetector` service wykrywa triggery (np. po debrief save, po wejściu w Stats tab, przy app open jeśli pending insight)

**Form factor — mix wszystkich trzech:**
| Form | Use case | Behavior |
|------|----------|----------|
| Toast | Reveal (quick stat) | Top, 4s auto-dismiss |
| Inline banner | Notice (subtelna obserwacja) | Top of tab, sticky do swipe-dismiss |
| Bottom sheet 40% | Pattern / Recovery (heavy insight) | Modal, manual dismiss, CTA |

**Hybrid AI w pop-upach:**
- Pattern + Recovery moments → AI-generated (wymagają RAG context)
- Reveal + Celebrate-tease + Notice + Comparative → templated z dynamic data

**Pop-up archetypes:**
- Reveal — "Lęk ↓ 35% vs poprzedni tydzień 🎉"
- Pattern — "3. raz w tym tygodniu 'mama'. Zobacz wzorzec →"
- Notice — "Średnio jesteś najlżejszy o 18-20 💡"
- Celebrate-tease — "Jeszcze 1 dzień do tygodnia 🌊"
- Recovery moment — "3 tygodnie temu pisałeś o lęku. Od 14 dni żadnej wzmianki."
- Comparative — "To twój 23. debrief tego miesiąca. 2× więcej niż średnia."

**Rate limit pop-upy**: max 1 per app session, dedup przez `app_insights_shown`.

## Decyzje strategiczne (locked 2026-05-14)

1. **NIE ma nowego "Today" tab** — pop-upy są in-context, nie w dedykowanej zakładce
2. **Hard cutover** — Faza 2 wyłącza wszystkie legacy hardcoded jobs jednocześnie (feature flag rollback path)
3. **Hybrid form-factor** — toast + banner + sheet, decyzja per insight weight
4. **Hybrid AI** — pattern/recovery AI, reszta templated
5. **Faza 2 start scope**: 1 push (post_session_reflection) + 2 pop-upy (Reveal + Celebrate-tease)

## Plan rollout — 4 fazy

**Faza 1 — Foundation (~1-2 sesje):**
- Migracja `notification_moments` + `app_insights_shown`
- `NotificationOrchestrator` + `InAppInsightDetector` services
- Flutter: `MomentBottomSheet` / `InsightToast` / `InlineNoticeBanner` widgety
- Feature flag `SETTINGS.use_legacy_notifications` (rollback path)
- PostHog events `moment.*` + `inapp_insight.*`
- Backend logging dla orchestrator decisions

**Faza 2 — Pierwsze WOW (~2-3 sesje):**
- 1× push: post_session_reflection (AI-generated, leverages PostSessionNudge + RAG)
- 3× pop-upy: Reveal (Stats trend), Celebrate-tease (streak 6→7), Pattern (recurring topic z RAG, AI-generated)
- Hard cutover starych jobs

**Faza 3 — Expansion (~3-4 sesje):**
- Push: mood_dip_alert, streak_celebration, pattern_insight
- Pop-upy: Notice, Recovery moment, Comparative
- Adaptive scoring (uczy się z dismissals)
- Settings UI redesign: 11 togglei → ON/OFF + slider intensywności + interest chips

**Faza 4 — Cleanup (~1 sesja):**
- Usunięcie starych RQ jobs + hardcoded EN text
- Wyczyszczenie zombie preferences (streaks/milestones/between_sessions toggles)

## P0 bugi z audytu już naprawione (2026-05-14)

1. ✅ Frontend: FCMTokenService.reset() + signOut() wiring (fcm_token_service.dart, main_page_cubit.dart)
2. ✅ Backend: health_check.py fallback path — 3 gates (is_banner_suppressed + 30d window + 14d activity) — 7 nowych testów pass
3. ✅ Backend: add_fcm_token LRU rotation zamiast Exception — 13/13 testów pass

## P1/P2 bugi do dorobienia (kontekst dla Fazy 1)

- iOS APNS retry on null token (TODO comment już w kodzie)
- DELETE FCM token endpoint przy logoucie
- Backend logging gdy user has 0 FCM tokens (silent failure obecnie)
- Zombie jobs `notify_journal_reminder` / `notify_inactivity_reminder` — będą usunięte przy hard cutover
- Timezone regex bug (CET/EST → UTC) w `get_users_eligible_for_notification`
- PostHog events dla token registration + permission denied

Linkuje do: [[reference_posthog_integration]] (analytics for moment events), [[feedback_no_live_api_experiments]] (test before deploy).
