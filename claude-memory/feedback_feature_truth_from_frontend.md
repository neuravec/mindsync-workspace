---
name: feedback-feature-truth-from-frontend
description: "What features exist and what is premium-gated must be checked in the Flutter frontend, not backend (backend has legacy code); current feature names"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 11ef1d1a-7b6d-4b0b-b417-08a34feccc91
  modified: 2026-10-02T12:01:52.315Z
---

When listing app features or Free vs Premium (paywall copy, marketing, blog cards), verify against what is ACTIVE in the frontend (`premiumGateTrigger(...)` call sites, screens actually wired), not backend endpoints or old l10n keys. Backend and arb contain legacy features (e.g. "Therapy tracking insights", `stats_goalPremiumLock`, `stats_therapyTrackingPremiumTitle` are unused).

**Why:** 2026-10-02 subscription redesign: operator corrected me twice for using backend/legacy names ("therapy tracking nie ma, moze na backendzie jakis legacy kod jest. na froncie sprawdzaj co jest aktywne").

**How to apply:** Current names per operator: "Before therapy" / "After therapy" (not "debrief"), "Weekly / Monthly therapy summary" (not "progress snapshots"), "Mood & symptom trends" (plural; not "therapy tracking"), "Goal progress story" (not "AI goal narratives"). Active FE premium gates (2026-10-02): session_recording (2 free), reflect_messages (30/mo), reflect voice, habits (1 free), monthly_audit. Before/After/between-session notes share a backend AI limit of 5/month. See [[project-subscription-redesign-2026-10-02]].
