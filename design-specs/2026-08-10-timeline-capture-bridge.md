# Timeline Capture Bridge - Design Specification

Author: ui-ux-designer (design consultant, read-only)
Date: 2026-08-10
Implements: Timeline -> therapy-loop capture bridge (activation/retention lever)
Consumer: flutter-mobile

---

## 1. Placement decision (read this first)

**Upgrade the existing "All" filter empty-state in Timeline** (`_EmptyState` in
`mindsync-frontend/mindsync_app/lib/screens/therapy_tab/therapy_tab_screen.dart`,
lines 567-826) by adding one new CTA block beneath the current title/subtitle.
No new screen, no modal, no inline card injected into a populated feed.

Three-sentence justification:

1. For a genuinely zero-capture user, the "All" filter timeline is, by
   construction, always empty (it is the unfiltered feed, so an empty response
   there means zero items exist across all 8 capture types) - meaning every
   single zero-capture user who visits Timeline lands on exactly this state,
   making it the highest-precision, zero-extra-plumbing place to intercept
   them.
2. Today that empty state is confirmed to be passive text only ("Your therapy
   journey starts here. Tap the + button...") with no tappable element, which
   is the most direct explanation for why Timeline's wide reach (46 users/14d)
   isn't converting into captures - the fix is to literally add the CTA that
   is missing, not to invent a new surface.
3. An empty state is inherently non-interruptive (there is no content to
   interrupt - the user opened Timeline and found nothing, so offering the one
   obvious next action there is additive, not intrusive), which fits the
   "gentle, easily dismissible" requirement for a mental-health app better
   than any overlay on a populated list.

An inline card injected after the most recent entry was considered and
rejected: a user with zero captures has no "most recent entry" to attach to,
so that placement structurally cannot reach the target segment at all.

---

## 2. Trigger condition and cap logic

### 2.1 Trigger (exact, self-contained - no cross-cubit reads needed)

Show the bridge when `TherapyTabState` is:

```
TherapyTabEmptyState(
  activeFilter: TherapyFilter.all,
  hasItemsInOtherFilters: false,   // always false for filter==all when empty
)
```

This is computed today in `TherapyTabCubit._fetchStateForFilter` (line 164):
`hasItemsInOtherFilters: filter != TherapyFilter.all`. For `filter ==
TherapyFilter.all` this is always `false`, and because the "All" feed is
unfiltered, an empty response there is proof of zero items of any of the 8
types (`debrief`, `between_session`, `prep_card`, `weekly_summary`,
`recording`, `monthly_audit`, `realization`, `health_check`). No new state,
no new API call, no read into `MainTabCubit` is required.

**Note on the brief's "reuse GettingStartedCard's approximation" instruction:**
GettingStartedCard's gate (`latestRealization == null && latestDebrief == null
&& latestPrepCard == null` on `MainTabState`) only checks 3 of the 8 capture
types and lives on a different cubit. The Timeline-native signal above is
strictly more complete (all 8 types) and requires no coupling to
`MainTabCubit`. Use it as the definitive trigger. Because it is a materially
tighter definition of "zero captures," track it under its own `entry_point`
(`timeline_empty_state`, see SS5) rather than conflating it with
`home_empty_state`'s numbers.

### 2.2 Frequency cap / permanent dismiss

- The bridge only ever renders while the trigger above holds. The moment the
  user completes ANY capture (of any of the 8 types), Timeline's state moves
  to `TherapyTabLoadedState` and the bridge disappears on its own - no manual
  "seen" bookkeeping needed for that path.
- Add one new boolean preference, `timelineCaptureBridgeDismissed`, written
  the first time the user taps the small "Not now" dismiss affordance. While
  `true`, the CTA block is not rendered, but the existing passive
  title/subtitle/illustration for the "All" empty state still renders
  unchanged (dismissing the bridge must not blank the screen).
- No session-count or time-based re-prompt: this is a static empty-state
  element, not a popup, so there is nothing to "cap" beyond the one permanent
  opt-out. Do not re-show it after dismissal even across app reinstalls-that
  would require server-side state and is out of scope (SS8).

---

## 3. Layout - widget tree sketch

Everything below is ADDITIVE inside `_EmptyStateState.build()` in
`therapy_tab_screen.dart`, inserted after the existing subtitle `Text` widget
and before the current `if (_isGeneratable && ...)` block. The existing
illustration, title, and subtitle for the "All" empty state are UNCHANGED.

```
Center
 -> SingleChildScrollView
     -> Padding (32)
         -> Column (existing, unchanged)
             |- SvgPicture (emptyNoData illustration)          [unchanged]
             |- Text: therapy_emptyAllTitle                    [unchanged]
             |- Text: therapy_emptyAllSubtitle                 [unchanged]
             |
             |- ── NEW: _TimelineCaptureBridge ─────────────────────────
             |   (only when filter==all && !hasItemsInOtherFilter
             |    && !dismissed)
             |
             |   SizedBox(height: 24)
             |   AnimatedOpacity (200ms fade-in, skipped if
             |     MediaQuery.disableAnimations)
             |     -> Container                                 [card]
             |         color: MsColors.aquaBreeze
             |         borderRadius: 16
             |         padding: EdgeInsets.all(16)
             |         -> Column
             |             |- Row
             |             |   |- Icon(Icons.lightbulb_outline,  <- matches
             |             |   |     size: 20, color: deepOcean)    between_session
             |             |   |- SizedBox(width: 8)                dot/icon used
             |             |   |- Expanded(Text: bridge microcopy)  elsewhere in
             |             |                                        Timeline
             |             |- SizedBox(height: 12)
             |             |- Semantics(
             |             |     button: true,
             |             |     label: <full sentence, SS7>)
             |             |   -> SizedBox(width: double.infinity, height: 48)
             |             |       -> ElevatedButton.icon           <- same
             |             |           icon: Icons.edit_note_rounded   visual
             |             |           label: Text(CTA label)          pattern as
             |             |           style: backgroundColor:         "Generate
             |             |             MsColors.deepOcean,           now" button
             |             |           foregroundColor: mainWhite,     already in
             |             |           shape: RoundedRectangleBorder(  this file
             |             |             borderRadius: 12)
             |             |- SizedBox(height: 8)
             |             |- Center
             |                 -> Semantics(button: true, label: <SS7>)
             |                     -> SizedBox(minHeight: 48, minWidth: 48)
             |                         -> TextButton(
             |                             "Not now" / dismiss,
             |                             style: minimumSize (48,48))
```

Recommended file: new widget class in
`lib/screens/therapy_tab/widgets/timeline_capture_bridge_card.dart`
(matches the existing pattern of extracting Timeline sub-widgets, e.g.
`weekly_summary_widget.dart`, `between_session_note_widget.dart`), imported
into `therapy_tab_screen.dart`. Keep it a `StatefulWidget` so it can own the
one-time `first_capture_prompt_shown` log in `initState` and the dwell-time
clock for `first_capture_prompt_dismissed`, exactly mirroring
`GettingStartedCard`'s and `wow_screen.dart`'s existing pattern.

---

## 4. States

| State | Trigger | Visual |
|---|---|---|
| **Default (shown)** | `TherapyTabEmptyState(all, hasItemsInOtherFilters:false)` AND `!timelineCaptureBridgeDismissed` | Card renders as above; fades in once (200ms), or appears instantly if reduced-motion is on |
| **Pressed (CTA)** | User taps the primary button | Standard `ElevatedButton` ink/pressed feedback (Material default - no custom animation needed); on release, launches the between-session capture flow (SS6) |
| **Pressed (dismiss)** | User taps "Not now" | `timelineCaptureBridgeDismissed` written to prefs; card is removed from the tree immediately (no exit animation needed - keep it simple/cheap; a quick 150ms fade-out is a nice-to-have, not required) |
| **Dismissed / hidden** | `timelineCaptureBridgeDismissed == true`, OR the state is no longer the exact trigger state (user has >=1 capture, or is on a different filter) | Card does not render at all; rest of the empty state (illustration/title/subtitle) is unaffected |
| **Not applicable** | Any other `_EmptyState` variant (a specific filter empty with items elsewhere, generating, premium-locked, generate-failed) | Bridge never renders - guarded strictly to `filter == TherapyFilter.all && !hasItemsInOtherFilter` |

There is no loading or error state for the bridge itself - it renders from
already-loaded cubit state and a synchronous `SharedPreferences` read; it has
no network call of its own.

---

## 5. Trigger + cap logic (implementation-ready pseudocode)

```dart
// Inside _EmptyStateState (or the new _TimelineCaptureBridge widget, which
// receives `filter` and `hasItemsInOtherFilter` from its parent):

bool get _bridgeEligible =>
    widget.filter == TherapyFilter.all &&
    !widget.hasItemsInOtherFilter;

// Read once in initState of _TimelineCaptureBridge:
final bool _dismissed = sl<SharedPreferencesManager>()
    .hasDismissedTimelineCaptureBridge(); // new method, SS9

// Render condition in the parent _EmptyStateState.build():
if (_bridgeEligible && !_dismissed) const _TimelineCaptureBridge(),
```

---

## 6. CTA destination

Single CTA, no in-card choice between debrief/between-session (per "one
bridge, not a campaign" - a picker would be a second decision point). Route
straight into the **between-session note** flow:

- Rationale: among the broad-reach capture-lift candidates, `between_session`
  has the highest measured d2-7 retention lift (33.3%) alongside `reflect`
  (35.7%, out of scope - not a therapy-loop capture per this task); it is
  also the lowest-friction of the two in-scope capture types (a quick note,
  no assumption that the user just finished a therapy session, which
  `debrief` implies and many Timeline-browsing-only users won't have).
- Implementation: reuse the exact call already used by the FAB's
  `FabFlowType.betweenSessions` case in
  `lib/screens/main_page/main_page_body.dart` (lines 508-519) and by
  `TherapyFlowLauncher` - do not reinvent this:

```dart
await TherapyFlowLauncher.launch(
  context,
  route: MsRoutes.betweenSessionsFlowRoute,
  noteType: 'between-session note',
  getLatest: () => sl<BetweenSessionManager>().getLatestNote(),
  isUnfinished: (item) => item != null && item.processingStatus != 'completed',
  toTimelineItem: (item) => TherapyTimelineItem.betweenSession(item),
);
if (context.mounted) {
  context.read<TherapyTabCubit>().loadTimeline(); // refresh so the new
                                                    // entry appears and the
                                                    // bridge naturally
                                                    // disappears
}
```

This also means the CTA tap does not need its own analytics event - the
destination flow's own existing capture-started/submitted instrumentation
(`captureFunnelParams()`, `is_first_capture`, etc.) already measures what
happens next, exactly as `GettingStartedCard` and `wow_screen.dart` already
rely on for their own CTAs (no local "tapped" event exists for either; only
shown/dismissed do - see SS5 of the analytics report and the two existing
call sites).

---

## 7. Copy table (PL + EN)

Add new ARB keys to `lib/l10n/app_en.arb` and `lib/l10n/app_pl.arb` (and
propagate to the other 5 locales per the existing l10n process -
`flutter gen-l10n` after adding keys; other locales can temporarily fall back
to English if translation isn't ready before ship, per existing project
practice for new strings).

| Key | EN | PL |
|---|---|---|
| `therapy_captureBridgeMicrocopy` | "One quick note is often the easiest way to start." | "Jedna krotka notatka to czesto najprostszy poczatek." |
| `therapy_captureBridgeCtaLabel` | "Write your first note" | "Napisz swoja pierwsza notatke" |
| `therapy_captureBridgeDismiss` | "Not now" | "Nie teraz" |

Tone check against existing Timeline copy (`therapy_emptyAllTitle`:
"Your therapy journey starts here." / PL "Twoja droga terapeutyczna zaczyna
sie tutaj."; `therapy_emptyNotesSubtitle`: "Capture a thought between
sessions with the + button." / PL "Zapisz mysl miedzy sesjami przyciskiem
+."): warm, second-person, no clinical vocabulary, no urgency/guilt language,
short sentences. The new copy matches this register and deliberately avoids
words like "streak," "must," "should," or "missing" - it is an invitation,
not a nudge toward a quota.

No em dash is used in the shipped copy (project-wide typography rule).

---

## 8. Analytics table

Reuses the existing `first_capture_prompt_shown` / `_dismissed` contract
(`AnalyticsEvents.firstCapturePromptShown` / `firstCapturePromptDismissed` in
`lib/core/analytics/analytics_events.dart`, lines 382-383) - the same two
events already fired by `GettingStartedCard` (`home_empty_state`) and
`wow_screen.dart` (`post_onboarding`). Do not add a third event name.

### `first_capture_prompt_shown` - fired once in `initState` of the new widget

| Property | Value |
|---|---|
| `entry_point` | `'timeline_empty_state'` (new value - distinct from `home_empty_state` / `post_onboarding`) |
| `prompt_variant` | `'default'` (single variant, no A/B at launch) |
| `capture_types_offered` | `['between_session']` |
| `hours_since_signup` | `AnalyticsEvents.hoursSinceSignup()` - omit key entirely if null, never send a fabricated value (existing contract) |

### `first_capture_prompt_dismissed` - fired only on the explicit "Not now" tap

| Property | Value |
|---|---|
| `entry_point` | `'timeline_empty_state'` |
| `prompt_variant` | `'default'` |
| `dwell_ms` | `DateTime.now().difference(shownAt).inMilliseconds` (0 if `shownAt` unset) |
| `dismiss_method` | `'explicit_close'` (matches `wow_screen.dart`'s vocabulary - the only dismiss path here, no swipe/back-gesture dismiss) |

Do not fire `_dismissed` when the bridge simply stops rendering because the
user captured something (that is a success path, not a dismissal) or when
they navigate away without tapping "Not now" (matches `GettingStartedCard`'s
existing rule that only an explicit close counts).

---

## 9. Accessibility checklist

- **Touch targets**: primary CTA button is full-width x 48dp minimum height
  (`SizedBox(height: 48)` wrapping the `ElevatedButton.icon`, consistent with
  the existing `therapy_generateNow` button pattern in this same file, which
  already uses 12v/24h padding producing >48dp). The "Not now" text button
  gets an explicit `ConstrainedBox(minWidth: 48, minHeight: 48)` - the exact
  same fix already applied to the retry link in `_SummaryRetryFailedRowState`
  (`therapy_tab_screen.dart` lines 1813-1814) for CS-06 - reuse that pattern
  verbatim rather than relying on default `TextButton` padding.
- **Spacing**: >=8dp between the CTA button and the dismiss button
  (`SizedBox(height: 8)` as sketched in SS3) so mis-taps between the two
  primary/secondary actions are unlikely.
- **Contrast**: card background `MsColors.aquaBreeze` (#DBF0ED) with
  `MsColors.deepOcean` (#113237) text/icon exceeds 4.5:1 (both already used
  together elsewhere in this codebase, e.g. `_QuickCta` in
  `getting_started_card.dart`). CTA button reuses the existing
  `deepOcean`-background / `mainWhite`-text combination already used by the
  "Generate now" button in this same file - already established as
  accessible by precedent, no new contrast pair introduced.
- **Semantic labels**: wrap both buttons in explicit `Semantics(button: true,
  label: '...')` rather than relying on the visible label text alone, so a
  screen reader announces the full sentence, not just the truncated visible
  string (e.g. CTA label: "Write your first note, opens a between-session
  note"; dismiss label: "Not now, hide this suggestion"). Do NOT rely on
  color/icon alone to convey affordance - both actions have explicit text
  labels already, satisfying "no information by color alone."
  - Do not add a `Semantics` header/live-region announcement for the card
    appearing - it is not time-sensitive or interruptive, and an unsolicited
    screen-reader announcement on a background state change would be a
    startle risk in a mental-health context.
- **Reduced motion**: gate the 200ms fade-in behind
  `!MediaQuery.of(context).disableAnimations`; when disabled, render the card
  at full opacity immediately with no animation. No other motion is used (no
  scale/bounce/confetti - this is a quiet, supportive element, not a
  celebratory one).
- **Text scaling**: use the existing `MsStyles`/inline `TextStyle` sizes
  already in this file (13-15sp body text) and let them scale with the
  system font size setting normally (no hard-coded `textScaleFactor` override
  anywhere in this widget).
- **Focus order**: card content should sit in natural reading/tab order after
  the existing title/subtitle and before any other empty-state content (there
  is none for the "All" filter today), i.e. no custom `FocusTraversalOrder`
  needed - default widget-tree order is already correct given the sketch in
  SS3.

---

## 10. Out of scope (explicit)

- No modal, popup, snackbar, or push notification variant of this bridge.
- No dual-choice picker between debrief and between-session capture (single
  CTA only, per SS6).
- No re-prompt after dismissal, no time-decayed re-surfacing, no
  server-side/cross-device dismiss state - local `SharedPreferences` only,
  same durability model as `hasCapturedBefore` / `swipeDeleteHintShown`.
- No changes to the "All" filter's existing illustration, title, or subtitle
  copy (`therapy_emptyAllTitle` / `therapy_emptyAllSubtitle`) - purely
  additive.
- No changes to any other filter's empty state (debrief/prep/notes/
  recordings/weekly/monthly/realizations/health-check) - the bridge is
  strictly gated to `filter == TherapyFilter.all`.
- No new/renamed analytics event - reuses `first_capture_prompt_shown` /
  `_dismissed` exactly as already defined.
- No attribution wiring from this CTA into the destination flow's own
  funnel events (e.g. adding a `source`/`entry_point` param to whatever event
  the between-session capture screen itself fires on open) - flagged as a
  reasonable fast-follow if growth-analyst later wants entry-point-level
  attribution beyond the shown/dismissed pair, but not required for this
  bridge to be measurable end-to-end (a `first_capture_prompt_shown
  (timeline_empty_state)` followed within a session by the user's first
  ever capture is already inferable from existing events).
- No changes to the global FAB (`MsFab`) menu, its copy, or its flow options.

---

## 11. Flutter implementation notes (for flutter-mobile)

**New/changed files:**
1. `lib/screens/therapy_tab/widgets/timeline_capture_bridge_card.dart` (new)
   - `StatefulWidget _TimelineCaptureBridge` (or public
     `TimelineCaptureBridgeCard` if a widget test wants to reach it directly).
   - `initState`: log `first_capture_prompt_shown` once, mirroring
     `GettingStartedCard`'s `_GettingStartedCardState.initState` exactly
     (same call shape, different `entry_point`/`capture_types_offered`).
   - Dismiss handler: write `timelineCaptureBridgeDismissed = true` via the
     new `SharedPreferencesManager` methods (below), log
     `first_capture_prompt_dismissed`, then call a `VoidCallback onDismissed`
     passed in from the parent so `_EmptyStateState` can `setState` and stop
     rendering it (simplest: make `_TimelineCaptureBridge` itself
     `StatefulWidget` owning a local `_dismissed` bool, so no parent
     `setState` plumbing is needed at all - self-contained).
2. `lib/screens/therapy_tab/therapy_tab_screen.dart` - insert
   `if (widget.filter == TherapyFilter.all && !widget.hasItemsInOtherFilter)
   const _TimelineCaptureBridge(),` (or the public widget name) into
   `_EmptyStateState.build()` after the subtitle `Text`, before the
   `_isGeneratable` block (see SS3 for exact position).
3. `lib/services/preference_keys.dart` - add
   `timelineCaptureBridgeDismissed` to the `PreferenceKey` enum and its
   `bool` case in the `type` switch (follow the `hasCapturedBefore` /
   `swipeDeleteHintShown` pattern exactly - both are the closest precedent).
4. `lib/services/shared_preferences_manager.dart` - add two methods
   mirroring `hasSeenSwipeDeleteHint()` / `markSwipeDeleteHintShown()`:
   ```dart
   bool hasDismissedTimelineCaptureBridge() {
     return _sharedPreferencesService.getValue<bool>(
           key: PreferenceKey.timelineCaptureBridgeDismissed,
         ) ??
         false;
   }

   Future<void> markTimelineCaptureBridgeDismissed() async {
     await _sharedPreferencesService.saveValue(
       key: PreferenceKey.timelineCaptureBridgeDismissed,
       value: true,
     );
   }
   ```
5. `lib/l10n/app_en.arb`, `lib/l10n/app_pl.arb` (+ other locale ARBs) - add
   the three keys from SS7, then run
   `flutter pub run build_runner build --delete-conflicting-outputs` /
   `flutter gen-l10n` per the project's standard codegen step, and commit the
   generated `lib/l10n/generated/*` output (project convention - generated
   l10n is committed, per CLAUDE.md/memory notes).

**Testing (mandatory per CLAUDE.md):**
- Widget test: `_TimelineCaptureBridge` renders when
  `TherapyTabEmptyState(activeFilter: all, hasItemsInOtherFilters: false)`
  and `timelineCaptureBridgeDismissed == false`; does NOT render for any
  other filter's empty state, nor when `hasItemsInOtherFilter == true`, nor
  when the dismiss flag is `true`.
- Widget test: tapping "Not now" removes the card and persists the
  preference (mock `SharedPreferencesManager`).
- Widget test: tapping the CTA invokes `TherapyFlowLauncher.launch` with the
  between-session route/params from SS6 (verify via a mocked
  `BetweenSessionManager`/navigator observer, following existing FAB-flow
  test patterns if any exist under `test/`).
- Verify `first_capture_prompt_shown`/`_dismissed` fire with the exact
  property sets in SS8 (mock `AnalyticsEvents`/`PostHogService` the same way
  existing tests for `GettingStartedCard`/`wow_screen.dart` do, if such tests
  exist - otherwise this is a new coverage gap qa-testing should close).
- `flutter analyze` must pass with no new errors/warnings.

**Do not touch:** `_TimelineList`, `_DotRailRow`, `_TimelineCard`, the
Weekly/Monthly dedicated card lists, or any filter other than `all`'s empty
state. This is a strictly additive, single-file-plus-one-new-widget change.
