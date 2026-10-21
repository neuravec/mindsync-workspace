# MSV3.10 \- User Feedback Fix (13.08.2026)

## Summary

- Items: 3 (DELETE: 0 · FIX: 2 · CHANGE: 1\)  
- Areas: therapy session recording, next-appointment notifications, Workspace  
- Intent: three things from the [użytkowniczka V] call get touched now. Two bugs break flows that already work. Session audio comes out unusable when the telehealth call runs on the same phone, and the app pushes a "you haven't set a time" reminder even after the user sets the time. The third item is the strongest ask from the call: let users bring in documents from their therapist so the AI works from real material instead of only what the user remembers to type. The recording bug enters this round as an investigation, not a fix. We need to know what is actually happening and whether it comes back before anyone writes a patch.

## Global guardrails (read before touching anything)

- The session reminder already has its own logic and stays as it is. CS-02 covers only the false "you haven't set a time" push. Do not add new notifications and do not rebuild the existing reminder schedule.  
- After each item, run the app and confirm there are no dead references or broken navigation.  
- UI strings: the app ships in Polish and English. Where this spec names a new label, treat it as a working name and produce both locales. Existing strings quoted here are verbatim, use them for grep.

---

## CS-01 · FIX · \[Session recording\] · Microphone conflict when telehealth runs on the same device

- **Type:** FIX, phase 1: investigation only. No production code changes in this item.  
- **Location:** Therapy session recording → audio layer (capture plus preparation of the audio for transcription) → the whole path from recording start to transcription result. User path: the user starts a session recording in MindSync while running a telehealth call on the same phone. Lead: grep the code that starts a session recording and the audio session setup (iOS: `AVAudioSession` category, mode and options; Android: `AudioManager`, `MediaRecorder` / `AudioRecord`, `audioSource`). Recording specs from versions up to 3.2 live in the **tech** folder. Read them first, they define how this was supposed to behave.  
- **Now (wrong):** When the user runs a telehealth session on the same phone that is running MindSync, the recording comes out "too garbled" and no transcription is produced. Report: [użytkowniczka V], iPhone, telehealth call in parallel with a MindSync recording. The symptom looks like a microphone sharing or audio routing conflict, but that is a hypothesis, not a finding.  
- **Expected (what this item delivers):** A diagnostic report that answers Darek's three questions directly. What is this bug, why does it happen, and will it cause problems later.  
- **Action:** Run the investigation across the full audio matrix and hand back a report. Required coverage:  
  1. Platforms: iOS and Android separately. Do not assume the behaviour is shared.  
  2. Audio session setup: which category, mode and options we use today for session recording, and what happens to them when another app takes the microphone.  
  3. Active VoIP call in the background: how the OS splits the microphone between our app and the telehealth app, and what exactly we receive as input in that state.  
  4. Bluetooth and headsets: behaviour with a headset, on speaker, and when the audio route changes mid-recording.  
  5. Signal parameters: sample rate, codec, channel count. Check whether the conflict drops us into a low-quality telephony mode.  
  6. System processing: echo cancellation, noise suppression, automatic gain control. Check whether any of them eats the signal in this scenario.  
  7. OS limits: what is a hard platform restriction and what is our own misconfiguration.  
- **Deliverable, report structure:**  
  - Root cause, named plainly.  
  - Which layer holds the problem: our configuration, a library, or an OS restriction.  
  - Reproduction: exact steps and conditions where the bug appears, and where it does not.  
  - Future risk: whether the same mechanism will hit other scenarios (a phone call in the background, music playing, a second Bluetooth microphone), and whether upcoming iOS and Android releases make it worse.  
  - Fix options: at least two, each with cost, risk, and what it actually gives the user.  
  - Recommendation with reasoning.  
- **Do NOT touch:** No production code changes in this item. No audio configuration tweaks, no error copy, no UI. Leave voice notes and Droga terapeutyczna recording alone. Keep experimental code on a separate branch and label it in the report as evidence, not as a merge candidate.  
- **Done when:** The report is delivered, contains all six structure points above, and every one of the seven matrix items has an answer (including "checked, no effect"). Darek picks a fix path from it. The fix ships as a separate item after that decision.

---

## CS-02 · FIX · \[Notifications\] · False push about an unset appointment time

- **Type:** FIX  
- **Location:** Push notifications → reminder to set the next session time → the condition that triggers it. User path: the user enters the date and time of the next session (for example Wednesday 15:00) and still receives the push. Lead: grep the notification string **"You haven't set a time for your next therapy appointment"** and its Polish equivalent. Find the appointment screen and the storage for that date yourself: **read the specs for versions up to 3.2 in the tech folder**, they document where the session time is set and where it is stored. Do not infer the location from a widget name.  
- **Now (wrong):** After saving the date and time of the next session, the app still sends "You haven't set a time for your next therapy appointment". Report: [użytkowniczka V], session set for Wednesday 15:00.  
- **Expected:** The notification fires only when the next session time is genuinely not set. Saving the time cancels or invalidates the scheduled notification immediately, with no app restart required.  
- **Action:** Find out why the condition does not see the saved time. Check in this order: whether the saved date reaches the source the notification scheduler reads; whether the notification is scheduled locally on the device and never cancelled after the save; whether the backend sends the push from stale state; whether this is a time zone problem that makes a future appointment evaluate as past. Fix the cause, not the symptom. If the notification is scheduled locally, the save has to cancel it in the same place the date is written.  
- **Logic after the fix:**  
  - Next session time saved → the scheduled "unset time" notification is cancelled → the user stops receiving that push.  
  - Appointment time cleared or removed → the notification can be scheduled again under the existing rule.  
  - Appointment time set → the trigger condition returns false regardless of the device time zone.  
- **Do NOT touch:** The session reminder has its own logic and stays unchanged. Do not add notifications, do not change lead times on existing ones, do not touch the notification settings screen. Do not edit the notification string itself, only the condition that fires it.  
- **Done when:** After saving the date and time of the next session, the "unset time" push does not arrive once, verified on iOS and Android. After clearing the appointment, the notification returns under the existing rule. The session reminder behaves exactly as before. The test also passes after changing the device time zone.

