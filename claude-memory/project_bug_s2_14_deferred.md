---
name: BUG-S2-14 Implemented — Calendar Date Picker for Therapy Frequency
description: Calendar-based custom therapy scheduling — implemented 2026-03-30
type: project
---

BUG-S2-14: Calendar-Based Custom Therapy Scheduling — IMPLEMENTED (2026-03-30)

**What was built:**
- Backend: new `custom_therapy_sessions` column on `user_preferences` (JSON), migration `j6d7e8f9g0h1`
- Backend: `CustomTherapySession` Pydantic schema, dual-path utility functions (calendar sessions first, interval fallback)
- Backend: prep card + post-session nudge + therapy helpers all updated to pass `custom_sessions`
- Frontend: `CustomTherapySession` Freezed model, `CustomCalendarView` widget using `table_calendar`
- Frontend: month-view calendar, tap-to-add bottom sheet with time picker + therapist dropdown, session list below
- 64 backend tests for the new feature, all passing

**How to apply:** Feature is complete end-to-end. Backward compatible — existing "Every N days" users continue working via fallback logic until they save calendar sessions.
