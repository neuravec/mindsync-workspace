---
name: voice-chat-b7-verdict
description: B7 verdict — keep voice chat without investment, block the Gemini Live migration, decision gate 2026-09-10; plus the numbers behind it
metadata:
  type: project
---

# B7 verdict: realtime voice chat (2026-08-10)

**Decision: UTRZYMAĆ BEZ INWESTYCJI + hard decision gate 2026-09-10. Gemini Live migration: NO, frozen.**
Report: `analytics-reports/2026-08-10-voice-chat-assessment.md`.

**Why:** estimated lifetime realtime API bill is **$10–80 over 4 months** (~$3–20/mo) against
~140–175 lifetime voice minutes. Even 70% savings = $25–170/yr vs 2–5 engineer-days across two
platforms. You do not optimize the unit cost of a feature with 11 lifetime users.

**How to apply:** if the Gemini Live / STT-engine migration comes up again, this is already
answered – reopen only if the R4 gate below shows real demand. Note the brief conflated two
different features; keep them separate in future asks.

## Numbers worth remembering
- `voice_chat_started`: **11 distinct persons / 65 events lifetime** (2026-04-22 → 2026-08-04).
  4 of 11 are TestFlight testers; 2 ever purchased. Last fired 2026-08-04, silent since.
- **Never fired on build 2.0.76** (31 active users/30d) → possible entry-point regression, UNRESOLVED (H4).
- `audioChat` screen: 18th of 22 by 60d reach. 64/74 entries from `mainPage`. 74/74 have no next screen.
- **39% of sessions end under 30s** (20/51). Frequency: 6 of 11 users went 6+ times.
- Adoption vs correct denominator: 11 / 554 ever-trialled = **2.0%**.
- Retention cohort A (voice) n=6 → **suppressed, not used**; selection bias runs the wrong way anyway
  (you had to already be paying+engaged to touch a premium feature). Never cite it as "voice drives retention".

## Root cause: NOT discoverability
The mic icon sits permanently in the Reflect composer, no lock badge. It is a **premium gate**
(`reflect_tab_screen.dart:619`) against a base of 16 active subscriptions, plus the feature is
absent from all 10 paywall benefit strings. Gated but never sold, and gate hits are unmeasured.
Details in [[premium-gated-features-denominator]].

## Open follow-ups (owners assigned in the report)
1. `flutter-mobile` – emit `premium_gate_hit {feature}` + add `trigger_feature` to `subscription_screen_opened`. **This is the number that decides the feature's fate.**
2. `flutter-mobile` – 30-min check whether the 2.0.76 entry path is broken (4 failure points before the event fires).
3. **Gate 2026-09-10**: ≥25 unique gate-hitters/mo → promote; <10 → sunset (remove mic, Settings voice section, `audioChat`, `AudioChatCubit`, `RealtimeAPIManager`, ephemeral-key endpoint); 10–25 → hold.
4. `data-analytics` – split the REALTIME_VOICE feature label (see [[ai-cost-model-2026-08]]).
5. **Deliberately deferred**: do NOT build realtime cost instrumentation until the feature survives the gate.
6. Separate/bigger lead: `SYSTEM` = 93% of AI spend, unaudited.

## Voice NOTES are a different product – do not conflate
`voice_transcription_*` fires from `debrief_capture_cubit.dart:715` + `health_check_flow_cubit.dart:342`,
is **not premium-gated**, and sits on the therapy-capture path tied to 3.41x retention
(`analytics-reports/2026-08-10-activation-definition.md`). But it was only instrumented 2026-08-05
(8 events / 3 users) and `voice_transcription_failed` has never fired. **Re-measure after ~2026-09-05**
before any AssemblyAI/STT spend decision. This – not realtime chat – is where voice money belongs.
