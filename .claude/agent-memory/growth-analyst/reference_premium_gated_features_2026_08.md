---
name: premium-gated-features-denominator
description: Which MindSync features are premium-gated (so the correct denominator is the ~16 active subscribers, not all users), and why gate-hit demand is unmeasurable today
metadata:
  type: reference
---

# Premium gates = the denominator trap (verified 2026-08-10, task B7)

**Rule: before judging any feature as "unused", grep the Flutter client for `isPremium` on its entry path.**
A premium-gated feature measured against the all-users denominator will always look dead, because
the real premium base is tiny. This already produced one wrong framing (B7 brief judged voice chat
against ~94 active app users; the correct denominator was 16).

## Real premium denominators (Postgres, 2026-08-10)
- `user_subscription.is_active = True` → 34 rows, **but** `is_active AND end_date > now()` → **16**.
  The 18-row gap = expired-but-still-flagged-active (hourly deactivation job suspected lagging;
  flagged to `backend-api`). **Always use the `end_date > now()` form.**
- `user_subscription_trial.had_trial = True` → 554 (ever-trialled = the widest "could have used premium" set).
- PostHog `subscription_purchase_completed` distinct persons all-time = **2**. This is NOT the
  premium base; PostHog undercounts purchases badly. Revenue/premium truth = Postgres only.

## Known premium gates (client-side, `premiumGateTrigger(...)` call sites)
| Gate | Location | Notes |
|---|---|---|
| `reflect_voice` | `reflect_tab_screen.dart:619` | **hard gate**, snackbar + early return; mic icon always visible, no lock badge |
| `reflect_messages` | `reflect_tab_screen.dart:523`, `reflect_usage_indicator.dart:64` | soft limit (`reflect_limit_hit`) |
| `session_recording` | `record_session_flow.dart:246` | |
| `monthly_audit` | `therapy_tab_screen.dart:791`, `monthly_audit_widget.dart:914` | |

## THE INSTRUMENTATION HOLE: gate hits are invisible
- Hitting a gate shows a snackbar and **returns without emitting any event**. We cannot count demand.
- `subscription_screen_opened` carries **no `trigger_feature` property at all** (verified by full
  JSONExtractKeys enumeration over its 220-event history). Only the standard envelope + `user_id`.
  So even the "Upgrade" tap is unattributable to a feature.
- `paywall_shown` has **never fired**; `paywall_dismissed` exists only from 2026-08-07.
- Net: for any gated feature, "nobody wants it" and "everybody bounces off the gate" look identical.
  Recommended fix (owner `flutter-mobile`): emit `premium_gate_hit {feature}` at the snackbar, and
  add `trigger_feature` to `subscription_screen_opened`.

## Incongruity worth remembering
Voice is gated in Reflect but the Settings voice picker (`settings_cubit.dart:135 changeSelectedVoice`)
has **no premium check** – 13 lifetime users configured a voice vs 11 who ever used voice chat.
Also: voice mode appears in **none** of the 10 paywall benefit strings – gated but never sold.

See also [[voice-chat-b7-verdict]], [[posthog-flowing-events-baselines]].
