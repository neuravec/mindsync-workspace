# Security review: first-week Home PostHog client events, 2026-10-11

Auditor: security-guardian (read-only). No code, git, PostHog or prod changes were made. This file is the only write.

Scope: the client events added to close the first-week PostHog gaps, on `feat/first-week-home` in `mindsync-frontend-wt-fw-int`. Requested commit 2c312c2 (merge of 9ebdc0a). During the review the branch moved to fa8985c, which merges ac2350b with the three load-failure events the brief listed as "being added"; those were reviewed too, so this report covers all 20 events at fa8985c.

Read: `analytics_events.dart` (first-week, check-in, session sheet, Art. 9, follow-up, recap blocks; `logEvent`), `first_week_analytics.dart`, `first_week_cubit.dart`, `session_sheet_cubit.dart`, `show_session_sheet.dart`, `art9_consent_sheet.dart`, `follow_up_cubit.dart`, `follow_up_screen.dart`, `follow_up_first_message_watcher.dart`, `recap_cubit.dart`, `quick_check_in_cubit.dart`, `reminder_opt_in_cubit.dart`, `day0_reminder_row.dart`, the three sign-out / account-reset sites, `test/support/reflect_analytics_guard.dart` and its self-test, `test/support/posthog_capture.dart`. Backend (reference): `_first_week_http.py`, `first_week_follow_up.py`, `first_week_recap.py`, `follow_up.resolve_follow_up`, `plan_service` 409 rules, `consent.py` events.

Baseline: `audit-security-design.md` (H-1, M-1, section 12 item 3), `audit-security-wp1-4-backend.md` (L-2), `audit-security-delta-2026-10-11.md`, SPEC 3.2 to 3.6 and 8, API_CONTRACT 10.

## Verdict

**GO with changes.** No Critical, no High.

| ID | Sev | Finding | Owner | Blocks |
|---|---|---|---|---|
| E-M1 | Medium | `art9_consent_step_shown` / `art9_consent_declined` with `source: settings` or `session_sheet` re-identify the person-less 403 `art9_consent_required` and process a therapy proxy for people without Art. 9 consent | flutter-mobile | Store release |
| E-L1 | Low | `first_week_action_failed {action: drop}` encodes the step class (prep or after, so variant A) and the session outcome | flutter-mobile | Store release |
| E-L2 | Low | Events after sign-out land on the next account: the shared follow-up watcher, and the session sheet's after-close reporting | flutter-mobile | No (recommended before store release) |
| E-L3 | Low | `session_sheet_opened` / `_dismissed` widen the accepted variant-A residual of `session_sheet_completed` | lead (lawyer bundle) | No code change |

TestFlight is not blocked. The store release needs E-M1 and E-L1 fixed, with the guard updated.

## Per-event verdicts

| Event | Verdict | Required change |
|---|---|---|
| `first_week_plan_hide_undone` | OK | none |
| `side_card_dismiss_undone` | OK | none (B/C only, same as shipped `side_card_dismissed`) |
| `reminder_time_changed` | OK | none (no time; positive-only standard-tone action, I-1) |
| `reminder_open_settings_tapped` | OK | none |
| `art9_consent_step_shown {source}` | CHANGE (E-M1) | Send only from the side card's consent step. Never after a 403: remove `session_sheet_cubit.dart:306`; in `showArt9ConsentSheet` log only for `Art9ConsentPlace.sideCard` (`art9_consent_sheet.dart:100`), so the Settings editors (`settings_cubit.dart:232`) send nothing. With one source left, drop the `source` property (no properties). |
| `art9_consent_declined {source}` | CHANGE (E-M1) | Same: remove `session_sheet_cubit.dart:270` and `:406`; `art9_consent_sheet.dart:116` only for `sideCard`; no properties. |
| `session_sheet_opened` | OK, accepted residual (E-L3) | none in code; lawyer-bundle entry |
| `session_sheet_dismissed` | OK, accepted residual (E-L3) | none for the event itself; the after-close path gets the account check from E-L2 |
| `follow_up_dismissed` | OK with E-L2 fix | disarm the shared watcher on every account reset |
| `follow_up_failed {status_class}` | OK | none (404 is tone-independent; gentle tone gets 200 with the calm question) |
| `follow_up_check_in_tapped` | OK | none (the "Quick check-in" swap depends on quota, not tone) |
| `first_week_recap_dismissed` | OK | none (I-2) |
| `first_week_recap_failed {status_class}` | OK | none |
| `first_week_recap_retry_tapped` | OK | none |
| `checkin_empty_trends_tapped` | OK | none |
| `quick_checkin_abandoned {areas_count, rated_count}` | OK | none (counts of the person's own cards; no score, area, step, variant or tone) |
| `first_week_action_failed {action, status_class}` | CHANGE (E-L1) | Remove the `drop` value: `dropToday()` (`first_week_cubit.dart:186`) sends no failure event. Every other action value is OK. |
| `first_week_plan_failed {status_class}` | OK | none (inside the generation check, once per process, `unavailable`/`error` only, never for 204) |
| `quick_checkin_load_failed {status_class}` | OK | none (404 sends nothing) |
| `quick_checkin_retry_tapped` | OK | none |

## E-M1: consent-step events after a 403 (Medium)

- **Where:** `session_sheet_cubit.dart:270`, `:306`, `:406`; `art9_consent_sheet.dart:100`, `:116` with the default `Art9ConsentPlace.settings`, reached from `SettingsCubit._askArt9ConsentOnTop` (`settings_cubit.dart:232`) after `PUT /users/therapy-schedule` throws `Art9ConsentRequiredException`.
- **What:** the `settings` and `session_sheet` sources fire only after the server refused a schedule write with 403 `art9_consent_required`. The backend sends exactly that 403 person-less on purpose (WP-1..4 L-2, verified closed in the delta review): the per-person version reads "tried to store a therapy schedule without Art. 9 consent". The client events put the same fact back on the person, under a purpose-built name, plus the refusal. `source: session_sheet` also says variant A, because the sheet only opens from prep and after cards.
- **Why Medium:** the step appears only when Art. 9 consent is not active, so every subject of these events has not consented to processing of health data, and the fact (entering or moving therapy session times) is a therapy proxy. Precedent: design M-1 (a variant-A proxy in identified events) was Medium. The events also go to Firebase Analytics (I-3).
- **Why `side_card` stays:** that step is shown before any write (status read, no 403), so nothing person-less is undone. For a person without consent the side card is always C, which shipped `side_card_tapped` already records (I-4); the consent events add only the refusal.
- **Remediation (flutter-mobile):**
  1. Delete the three calls in `FirstWeekSessionSheetCubit` (`declineConsent`, the consent branch of `_write`, `close`).
  2. `showArt9ConsentSheet`: send both events only when `place == Art9ConsentPlace.sideCard` (or make `place` nullable, null meaning no events, and pass `sideCard` from `_askArt9Consent` in `show_session_sheet.dart` only).
  3. Drop `source`: `logArt9ConsentStepShown()` / `logArt9ConsentDeclined()` without parameters; remove `art9ConsentSourceParam` and the three source constants.
  4. Guard: `kFirstWeekPropertyKeys` for both events becomes `{}`; remove the three source values from `kFirstWeekAllowedStringValues` and `kFirstWeekPropertyStringValues`; delete `_kArt9ConsentSources`. Tests: the Settings 403 consent step and the sheet's consent step capture no `art9_*` event; the side-card step captures both with `{}`.
  5. The refusal after a 403 is then visible only in aggregate (backend person-less 403 count minus `consent_granted`), as SPEC 8 had it before today. Operator accepts that gap.

## E-L1: `first_week_action_failed {action: drop}` (Low)

- **Where:** `first_week_cubit.dart:186`; `analytics_events.dart:726`; guard `reflect_analytics_guard.dart:413`, `:432`.
- **What:** `drop` comes only from the session sheet's "It didn't happen this time" and "Not sure yet", which exist only on the prep card (day S-1) and the after card (day S), so only in variant A. The value names the step class and the outcome "the session did not take place / no new date": the split SPEC 8, decision 13.5 and API_CONTRACT 10 keep server side in aggregate, and the reason the design review reduced `session_sheet_result` (section 12 item 3). With `status_class: conflict` it even says "Not sure yet on a prep card against an older server".
- **Why Low:** failures only, and only people with active Art. 9 consent (variant A requires it).
- **Why not a generic value:** the sheet's other write (the change route) is deliberately not reported per person (L-2), so any shared value would still mean `drop`.
- **Remediation (flutter-mobile):** make `action` nullable in `_mutate` and call `_reportFailure` only when it is set; `dropToday()` passes none. Remove `firstWeekActionDrop` from `analytics_events.dart`, `_kFirstWeekActions` and `kFirstWeekAllowedStringValues`; in the guard self-test, change the control row from `'drop'` to another action and add `'drop'` to the rejected rows. Add a test: a failed drop (503, 409, offline) captures no `first_week_action_failed`. A person who leaves after a failed drop still sends `session_sheet_dismissed`; failure volume can be read from the backend's NoStoreRoute logs.

## E-L2: events after sign-out land on the next account (Low)

- **Shared follow-up watcher:** `FollowUpFirstMessageWatcher.shared` is static and outlives both the screen and the account. No reset site disarms it (`main_page_cubit.dart:91`, `settings_cubit.dart:1086`, `splash_screen.dart:260` reset `FirstWeekCubit` only), and `ReflectChatCubit` is a lazy singleton that is not reset on sign-out. After A opened the follow-up thread and signs out, the 2 h timer (`follow_up_first_message_watcher.dart:64`) or B's Reflect tab load (`:92`, `:112`, with `_seenOpen` still true) sends `follow_up_dismissed` after `PostHogService.reset()`: on the fresh anonymous id, which PostHog merges into whoever identifies next on the device, or directly under B. Propertyless and not health data, but on the wrong person.
- **Session sheet after close:** when the sheet is swiped away with a write on the wire, `_logCompleted` / `_logDismissedAfterClose` (`session_sheet_cubit.dart:297`, `:311`, `:324`, `:330`, `:366`, `:368`) run when the request settles, with no account check. A sign-out in that window sends `session_sheet_completed` or `session_sheet_dismissed`, both variant-A proxies, on the post-reset identity. On the drop path it is certain once the reset ran: `dropToday()` returns false after a generation change, so `:368` reports a dismissal. Narrow window (request latency), but a therapy proxy attributed to another data subject.
- **Remediation (flutter-mobile):**
  1. Call `FollowUpFirstMessageWatcher.shared.disarm()` (the silent stop) next to each `FirstWeekCubit.reset()`, before `PostHogService.reset()`. In the account deletion path of `SettingsCubit`, move both resets above `:1077`; `signOut` already resets first.
  2. Give `FirstWeekCubit` a read-only `int get generation`. The sheet cubit stores it in its constructor; `_logCompleted` and `_logDismissedAfterClose` return when it changed.
  3. Same guard, one line, at `first_week_cubit.dart:290`: `if (accepted && generation == _generation) waiting.onAccepted?.call();` (it fires the shipped `first_week_plan_hidden` / `side_card_dismissed`).

## E-L3: `session_sheet_opened` / `session_sheet_dismissed` (Low, accepted residual)

Both fire only from "Session moved?" (prep, day S-1) and "It didn't happen" (after, day S). Their presence says variant A (in therapy, a session on plan days 1 to 6, active Art. 9 consent) and dates a session to S or S-1. That is the class of the shipped `session_sheet_completed`, which the design review accepted into the lawyer bundle with prior M-3, and of the backend `prep_card_created` / `debrief_created`. What widens: people who open without completing are now included, and variant A becomes one event filter instead of a sequence query. Every subject has active Art. 9 consent, so the open question is the same as prior M-3 (does that consent cover product analytics), not a missing legal basis. No code change. **Lead:** extend the lawyer-bundle entry of `session_sheet_completed` to `opened` and `dismissed`, name both recipients (PostHog, Firebase Analytics), and record the operator's 2026-10-11 approval in SPEC 8.

## Answers to the four questions

### 1. Is each new event acceptable as is?

Yes for 17 of 20 (table above). Two need a change: `art9_consent_*` (no events after a 403, no `source`) and `first_week_action_failed` (no `drop`). The line I used: a therapy proxy about a person with active Art. 9 consent is the accepted prior-M-3 residual (lawyer bundle). A therapy proxy about a person without that consent, or one that undoes a deliberate backend de-identification, is not acceptable. `session_sheet_opened` / `_dismissed` fall on the first side; the post-403 consent events on the second.

### 2. Does anything encode step, variant, tone or a session date or time indirectly?

- **Step:** `action: drop` (prep or after, plus the outcome; E-L1). `session_sheet_opened` / `_dismissed` and the sheet's consent events by their existence (prep or after today, never which of the two). `defer` is step-neutral: the 409 `nothing_to_defer` means "today's card is not open", whatever the step.
- **Variant:** `source: session_sheet` means A; `source: side_card` means C without consent (already derivable from consent events and `side_card_tapped`); `action: dismiss_side_card` and `side_card_dismiss_undone` mean B or C, as the shipped side-card events do. After E-M1 and E-L1 no property value encodes a variant.
- **Tone:** no new event exists only in gentle tone. Positive-only standard-tone markers, allowed by design H-1 item 1 as user-initiated actions with no tone property: `first_week_action_failed {defer, defer_undo}` on plan days 0 to 2, `reminder_time_changed`, `reminder_open_settings_tapped`, `first_week_action_failed {set_reminder}` (the day-0 row is standard-only). Same class as shipped `today_card_deferred` and `reminder_optin_result` (I-1).
- **Date or time:** no property carries one; `reminder_time_changed` carries no time. Timestamps of the session sheet events place a session on S or S-1 (E-L3), as the shipped `session_sheet_completed` does.
- **`status_class`:** tone- and variant-neutral. Follow-up 404 means no open talk step today (gentle tone gets a 200 with the calm question, `follow_up.resolve_follow_up`); the recap and baseline 404s send nothing; 503s are infrastructure. The only combination that said more was `drop` with `conflict`, gone with E-L1.
- **`areas_count` / `rated_count`:** counts of the person's own rating cards (top three plus "Also rate"). No step, variant or tone. Check-in timing (A: first free day from day 5; B/C: day 4) is the same weak M-1-class signal as the shipped `quick_checkin_completed`.

### 3. Do the new close()/dispose() hooks risk an event after logout or for another account?

Yes, in two places (E-L2): the shared follow-up watcher, and the session sheet's reporting once an in-flight write settles after the sheet closed. Not at risk: the route-scoped hooks (recap `close`, check-in `close`, follow-up `dispose`, sheet `close` itself), because those screens are top-level full-screen routes over Home and sign-out lives in Home's drawer, so they always fire before a sign-out; `FirstWeekCubit` failure reports (generation-checked); Undo events (synchronous taps); `ReminderOptInCubit` (through `setReminder`'s generation check); `first_week_plan_failed` (inside the generation check, once per process, so it under-reports after an account switch but never misattributes). Residual: account deletion resets PostHog before `FirstWeekCubit`, the opposite of `signOut` (fixed by E-L2 item 1).

### 4. Does the guard enforce exact key and value sets for every first-week event?

Yes, for all 20 at fa8985c: exact key sets (`kFirstWeekPropertyKeys`, asserted equal to `kFirstWeekEvents`), a value set per string property per event (`kFirstWeekPropertyStringValues`), declared types for the rest, the global forbidden keys, values and tone substrings, and self-tests for an extra key, a missing key, a value borrowed from another event, wrong types and step, entry, date, time or detail strings. Every new event is driven by at least one test that calls `assertReflectFunnelPrivacy`; `debug_mode` is stripped by `test/support/posthog_capture.dart:32`. Gaps (Low, not blocking):

- Test time only. A branch no test drives can still send anything. Cheap hardening: move the shape maps from `test/support` into `lib` and `assert` them in `AnalyticsEvents.logEvent` in debug builds, so the same table serves both.
- Registration discipline. A first-week event missing from `kFirstWeekEvents` skips the shape check silently (`if (exact == null) continue`). Add a check in the first-week test files that every captured event is in `kFirstWeekPropertyKeys` or in an explicit list of foreign events (memory, paywall, trial sheet).
- After E-M1 and E-L1 the domains must shrink (`drop`, the three sources) with negative tests, as listed above.

## Info

- **I-1:** tone markers listed in answer 2; accepted class, no change.
- **I-2:** `first_week_recap_dismissed` counts "viewed, none of keep rhythm, own way, Not right". Which sections (and so which actions) the recap shows depends on server content; this shifts the rate a little but is no deterministic marker.
- **I-3:** `AnalyticsEvents.logEvent` also forwards every event to Firebase Analytics in release builds (`_sendToFirebase`). The lawyer bundle should list Google as a recipient of the session sheet and consent events, not only PostHog.
- **I-4 (pre-existing):** `side_card_tapped` from a person without Art. 9 consent is necessarily the C card ("Seeing a therapist? Add sessions"), a therapy-interest signal about a non-consenting person. For the lawyer bundle; no change requested here.
- **I-5 (pre-existing, out of scope):** the splash definitive-404 sign-out (`splash_screen.dart:256`) does not call `PostHogService.reset()`.
- **I-6:** API_CONTRACT 10 and SPEC 8 do not list the 20 new events yet. Add the rows with E-M1 and E-L1 applied (lead, integration-devops).
- **I-7:** `first_week_plan_failed` folds parse failures into `error` with network failures (good). Forward note: a new wire value that only some people get (a tone, a step key) would fail old builds only for them during a rollout; keep adding enum values only after a client that parses them has shipped.

## TestFlight versus store release

- **TestFlight:** not blocked. TestFlight events reach the production PostHog project, so landing E-M1 and E-L1 first saves a fix-forward, but it is not required.
- **Store release:** E-M1 and E-L1 fixed, guard domains and negative tests updated, qa-testing green. E-L2 recommended in the same pass (three small edits). Lead: E-L3 lawyer-bundle entry and SPEC 8 note, I-3 recipient, I-6 contract rows, operator acceptance of the post-403 consent-refusal gap.
- **After TestFlight:** posthog-data-extractor confirms that no `art9_*` event carries `source`, no `first_week_action_failed` carries `drop`, and gentle and standard sessions show the same event names.
