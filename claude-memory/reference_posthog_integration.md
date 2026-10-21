---
name: PostHog Integration
description: PostHog analytics implementation status — 0% done, comprehensive 89-event plan exists in POSTHOG_ANALYTICS_PLAN.md
type: reference
originSessionId: f9fa1844-5648-4eeb-af89-1f864b4cb1fd
---
PostHog analytics is NOT yet integrated (as of 2026-04-16). A comprehensive plan exists:

## Plan Document
- `POSTHOG_ANALYTICS_PLAN.md` at repo root — 89 events, 12 business scenarios, 9 dashboards, feature flags
- Covers: event taxonomy, person properties, architecture, privacy rules, dashboards, sprints

## Current State
- Zero PostHog code in Flutter or FastAPI
- Only Firebase Analytics with ~20 basic events (notifications, subscriptions, errors, analytics views)
- `analytics_events.dart` has `logEvent()` for Firebase only — needs dual-send extension
- No PostHog SDK packages, no service files, no config vars

## Implementation Plan
- 11 phases: backend foundation → frontend foundation → identity chain → backend events (34) → frontend events (55) → person properties → testing → privacy audit → integration verification → dashboards → post-deploy audit
- Agents: backend-api, flutter-mobile, integration-devops, qa-testing, security-guardian

## Privacy (Critical — mental health data)
- NEVER send therapy content, symptom names, health scores, error messages
- Session replay: maskAllTexts + maskAllImages
- EU Cloud: eu.i.posthog.com
- Scores bucketed (low/mid/high), durations bucketed
