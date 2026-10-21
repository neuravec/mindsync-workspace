> Kopia robocza specu Darka z 02.09.2026 (plik .docx: `MSV3.12__Change_Spec_Your_Session_flow__Custom_frequency_cleanup.docx`).
> Numer batcha przemianowany na **MSV3.13**, bo MSV3.12 jest zajęty przez Habit Tracker (spec: "rename freely"). Flagged for veto.
> Em-dash z oryginału zamienione na półpauzę (reguła globalna typografii).

# MindSync Change Spec – MSV3.12 "Your Session flow + Custom frequency cleanup"

For Claude Code · 02.09.2026 · author: Darek (WhatsApp notes 01.09 + one question round 02.09) · zero open questions


## Context

Source notes: Darek → Mikołaj, WhatsApp 01.09 22:43–22:44 (with screenshots), found during release QA on main ("Działa wszystko, robię relesy" – these two items are what was still wrong).

This round comes directly after MSV3.11 "Threads, Reflect & Grace fixes" (31.08). MSV3.11 · CS-10 (Therapy Schedule end-to-end) overlaps both items below – check its landing state first and build on it, not around it.

Code leads below are quoted from MSV3.11 (grounded against both repos on 31.08); re-verify against the current heads before editing.

Version number MSV3.12 assigned by the compiler as the next in the series; rename freely.


## Summary

Total items: 2 (DELETE: 1 · FIX: 1)

Areas touched: Main → "Your Session" module · Moja terapia (My Therapy) → Therapy Frequency (Custom) · therapy-schedule compute chain (backend)

Intent: two findings from Darek's release QA. First, the "Your Session" card on Main gets stuck after a completed After Therapy – the state chain already specced in MSV3.2 Fix 2 · CS-09 must simply run again, end to end ("Chodzi tylko o to, żeby to przetkać i żeby znów działała logika."). Second, the Custom frequency mode loses its redundant "Every X days" interval: in Custom the user picks dates by hand, so an automatic interval is a second, competing source of truth – full removal, UI down to the data field.


## Global guardrails (read before touching anything)

The canonical Your Session state chain is MSV3.2 Fix 2 · CS-09, quoted verbatim inside CS-01 below. Do NOT redesign it, do not add states, do not rename buttons – make the existing design run.

The old guardrail "the settings session data model stays untouched" (protected since the MSV3.2 Fix chain) is lifted for exactly one field: custom_interval_days and its logic (CS-02, Darek's explicit decision 02.09). Everything else in the schedule data model keeps the protection.

Do NOT touch the Weekly and Biweekly frequency modes, the Custom calendar picker and its saved dates, the Therapists section, or anything else in Moja terapia.

Do NOT touch notification types, copy, or lead times (MSV3.10/MSV3.11 guardrail stands): CS-02 only changes which dates the existing generators compute from.

After each item: flutter analyze clean, run the app on Android + iOS, confirm no dead references / broken navigation.


## CS-01 · FIX · [Main → Your Session] · Card stuck after After Therapy – make the specced state chain run

Type: FIX

Blocked by: CS-02 (soft) – Custom mode's definition of "a next session is known" changes when the interval goes; land CS-02 first so this chain is validated against the final schedule model.

Re-work of: MSV3.2 Fix 2 · CS-09 ("State machine: unstick the post-debrief flow, add the Between Sessions window"), re-worked again in MSV3.2 Fix 3 (still broken on iOS then). Sibling: MSV3.11 · CS-10 (schedule persistence / compute / display / notifications) – if the module still misbehaves after CS-10 landed, the remaining defect is this item.

Location: Main → module 1 "Your Session" → the state-dependent card (headline + button) and its transitions. Reached: open app → Main. Leads (from MSV3.11): frontend lib/screens/main_tab/cubit/main_tab_cubit.dart → _computeNextSession (~line 618; computes client-side from SharedPreferences, flagged in MSV3.11 as the most likely divergence point), main_tab_screen.dart; backend recompute app/crud/crud.py:1201-1370 and app/utils/therapy_schedule_utils.py. Grep: "Your Session", "Session has ended", "After Therapy", "Between Sessions".

What it is: The countdown module that walks the user through the session cycle with one state-dependent button.

Now (wrong): Observed by Darek 01.09 on main (release candidate): the card shows "Session has ended" ("Aug 26, 2026 6:00 PM · [terapeutka]") with button "After Therapy". The user completes After Therapy. The card does not advance – no "Between Sessions", no prompt to enter the next therapy day. A week after the session date it still sits in the same state.

Expected (target chain – verbatim from MSV3.2 Fix 2 · CS-09; source of truth, unchanged):

No therapy set → button opens the hub-and-spoke to set therapy (date, time, cadence, with whom); writes the same fields as settings.

Session upcoming, no prep done → button "Prepare".

Prep done, session upcoming → button "View prep card", flipping immediately after the prep card is created, with no latency.

Session start time reached → button "After Therapy" (opens the debrief flow; no "Debrief" label survives anywhere in the module).

After Therapy completed and a next session is known (cadence or explicit date) → button "Between Sessions" (opens the Between Sessions capture). This state stays visible the whole time, however many between-session notes the user adds, until 3 days before the next session. If no next session is known (a one-off session, no cadence), the module does not sit in this state: it returns to the start of the flow, state 1, the set-therapy prompt. Setting the next date is always the beginning of the cycle (Darek); Between Sessions stays reachable from the FAB.

3 days before the next session → button back to "Prepare"; the countdown retargets to the next session. If the next session is already under 3 days away when After Therapy completes, skip state 5 and show "Prepare" straight away.

Each later session shows its own date and its own time, never the nearest session's hour. The cycle restarts.

Action: Diagnose why the post-After-Therapy transition never fires (frontend state flip, backend next_session_date recompute, or both) and restore the full chain above. Fix causes, not symptoms. For Custom frequency, "a next session is known" means: a future date exists among the user's manually picked dates (custom_therapy_sessions) – after CS-02 nothing is derived from an interval.

Do NOT touch: The countdown time formats; the reminder elements; the far-out-date display; the After Therapy and Between Sessions capture flows themselves (this item touches their entry points only).

Done when: On Android + iOS: completing After Therapy – from the module or from the FAB – flips the card to "Between Sessions" when a next session is known, or to the set-therapy state when none is; "Between Sessions" holds until exactly 3 days before the next session, then "Prepare" with the countdown retargeted; the full cycle loops across a session boundary in all three frequency modes (Custom = manual dates); Darek's repro (Aug 26 session, After Therapy filled) shows the card advanced instead of sitting on "Session has ended".

Value: "Do poprawy Feature na mainie, żeby działał zgodnie z Flow, który był zaproponowany wcześniej." (Darek, 01.09)

Risk: Medium – time edge cases (session starting right now, gaps shorter than 3 days, day boundaries) and the frontend/backend split flagged in MSV3.11 CS-10.


## CS-02 · DELETE · [Moja terapia → Therapy Frequency → Custom] · "Every X days" interval – full removal

Type: DELETE (full removal: UI + logic + data field – decision, 02.09)

Location: Moja terapia (My Therapy) → Therapy Schedule → Therapy Frequency → segment "Custom" → the input row "Every [ 6 ] days (1–365)" rendered between the Weekly/Biweekly/Custom segmented control and the calendar. Reached: side menu → Moja terapia → Therapy Frequency → tap "Custom". Leads (from MSV3.11): frontend lib/screens/settings/widgets/therapy_schedule_section.dart (reused by my_therapy_screen.dart) and lib/screens/main_tab/widgets/session_setup_screen.dart (verify whether the Main add-session flow renders the same interval input – if yes, it goes there too); backend UserPreferences.custom_interval_days (app/models/models.py:214-219), _compute_next_custom in app/utils/therapy_schedule_utils.py, recompute in app/crud/crud.py:1201-1370, PUT/GET /users/therapy-schedule (app/api/v1/endpoints/users.py:1403/1427).

What it is: In Custom mode the user hand-picks session dates on the calendar. The "Every X days" input on top of that defines an automatic every-N-days cadence – a second, competing source of truth for the same schedule. "W Custom jest to bez sensu, bo tam się wybiera daty z ręki." (Darek, 01.09)

Action: Remove the "Every X days" input from every surface that renders it. Remove the interval from the Custom computation: with frequency = custom, the next session is the nearest future date among the manually picked dates (custom_therapy_sessions) – nothing is generated from an interval. Remove custom_interval_days end-to-end: model field, request/response schemas, and the Alembic migration dropping the column (backend-api owns the migration). Weekly and Biweekly stay exactly as they are.

History note: MSV3.3.Fix.1 · CS-08 fixed "the Custom therapy interval field never renders" – that repair is deliberately reversed here; this item supersedes it, so "the field doesn't render" is the goal now, not a regression.

Data (decision, 02.09): Existing users keep their manually picked dates untouched; a stored interval value is simply dropped. No recomputation of their schedules, nothing generated or deleted in their calendars.

Do NOT touch: The Custom calendar picker and its saved dates; Weekly/Biweekly modes and their logic; the Therapists section; notification types/copy/lead times (the generators just read the computed next session, which after this item comes from manual dates).

Done when: The Custom segment shows only the calendar (no "Every … days" row) in Moja terapia and in every other schedule editor; grep for custom_interval_days and the "Every … days (1–365)" strings returns no live references in either repo; saving a Custom schedule persists the manual dates; Main's Your Session card (CS-01) and session notifications compute from those manual dates; an existing user who had an interval stored sees their picked dates unchanged; builds pass Android + iOS.

Value: One source of truth for Custom scheduling; removes a setting that contradicts the whole point of the mode. ("Every X days do wyrzucenia" – Darek, 01.09)

Risk: Low-Medium – the UI removal is trivial; care sits in the compute path (_compute_next_custom) and the column drop, both shared with CS-01's validation.


## Decisions log

02.09 – What should the card show after After Therapy is filled? → Darek: the flow is already written up in a Drive change spec; the task is only to unstick it ("Chodzi tylko o to, żeby to przetkać i żeby znów działała logika."). Found and quoted verbatim: MSV3.2 Fix 2 · CS-09.

02.09 – Where is the flow documented? → Google Drive: doc "MSV3.2 Fix2" (MSV3.2 Fix2 Fix.2, 22.07), item CS-09; re-worked in "MSV3.2 Fix 3" (23.07).

02.09 – Scope of the "Every X days" removal? → Full removal: UI + logic + data field (recommended option accepted).

02.09 – Existing users with a stored interval? → Interval disappears, manually picked dates stay; no extra migration of dates (recommended option accepted).

02.09 – Version number → MSV3.12 assigned by the compiler as next after MSV3.11; flagged for veto.
