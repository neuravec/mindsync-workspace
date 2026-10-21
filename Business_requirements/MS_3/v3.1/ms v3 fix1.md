# **MindSync Change Spec — Renames \+ Main/Reflect/Output fixes**

*For Claude Code · 2026-07-03 · author: Darek*

## **Summary**

* Total items: 12 (DELETE: 0 · FIX: 7 · CHANGE: 5\)  
* Areas touched: FAB, Character, Main/Home, Reflect, Timeline, Therapy Relationship output, Check-in output  
* Intent: fix the Polish localization (renames, persona names) and a batch of behavior bugs: wrong navigation targets on Main/Home, empty reflections getting saved, a timezone bug, an invisible icon, and output formatting on the Therapy Relationship and Check-in cards.

## **Global guardrails (read before touching anything)**

* Do NOT touch the "Zobacz źródło" flow inside Timeline/Odkrycia/Zapisane odkrycie. It works correctly and is the reference behavior for CS-06.  
* Do NOT touch Reflect's back-navigation discard behavior. Closing a new empty reflection via back already correctly discards it; CS-07 is only about the app-close path.  
* Renames (CS-01..03) apply to the Polish locale only. English strings stay as they are.  
* No item in this batch is a deletion. Nothing gets removed except the collapse behavior in CS-12.  
* After each item, run the app and confirm no dead references and no broken navigation.

---

## **CS-01 · CHANGE · \[FAB\] "Przygotuj się do terapii"**

* **Type:** CHANGE  
* **Location:** FAB label. Search PL strings/ARB for "Przygotuj się do terapii".  
* **Action:** Rename "Przygotuj się do terapii" → "Przygotuj się do sesji".  
* **Why:** Naming consistency. The flow prepares for a session, not therapy as a whole.  
* **Do NOT touch:** The FAB's behavior and target screen. Label only.  
* **Done when:** FAB shows "Przygotuj się do sesji" in PL; grep for "Przygotuj się do terapii" returns no live references.  
* **Risk:** Low. String change.

## **CS-02 · CHANGE · \[Character\] "Overview" in PL version**

* **Type:** CHANGE  
* **Location:** Character screen, tab/section labelled "Overview" when app language is Polish. Probably an unlocalized string; search for a hardcoded "Overview" in the Character widgets.  
* **Action:** In the PL locale, "Overview" → "Podsumowanie".  
* **Why:** English string leaking into the Polish UI.  
* **Do NOT touch:** The English locale, which keeps "Overview".  
* **Done when:** Character screen in PL shows "Podsumowanie"; ENG still shows "Overview".  
* **Risk:** Low.

## **CS-03 · CHANGE · \[Character\] Persona AI names in PL**

* **Type:** CHANGE  
* **Location:** Character → Persona AI selection. Persona names currently display in English regardless of locale, probably rendered from an unlocalized enum or config.  
* **Action:** In the PL locale, display persona names in Polish, exactly as in hub-and-spoke:  
  * Realist → Realista  
  * Coach → Trener  
  * Friend → Przyjaciel  
  * Sage → Mędrzec  
  * Explorer → Odkrywca  
* **Why:** PL app version should show PL persona names; hub-and-spoke already uses these.  
* **Do NOT touch:** Internal persona identifiers/keys used in logic, storage, or analytics. Localize the display name only. ENG locale keeps English names.  
* **Done when:** All five persona names render in Polish in the PL app; switching to ENG still shows English names; persona selection and AI behavior unchanged.  
* **Risk:** Medium. If names double as keys anywhere, translating the wrong layer breaks persona selection.

---

## **CS-04 · FIX · \[Main/Home\] Kafelek z datą najbliższej sesji — button "Przygotuj się"**

* **Type:** FIX  
* **Location:** Main/Home, tile showing the next session date, its "Przygotuj się" button.  
* **Action:** Currently navigates to Timeline. Expected: opens the "Przygotuj się do sesji" form, the exact same destination as the FAB "Przygotuj się do sesji" (CS-01). Reuse the FAB's navigation call rather than duplicating it.  
* **Why:** Button label promises session prep but lands on Timeline.  
* **Do NOT touch:** The FAB itself; the tile's other content (date display).  
* **Done when:** Tapping "Przygotuj się" on the tile opens the same form as the FAB; Timeline still reachable through its own entry points.  
* **Risk:** Low. Navigation target swap.

## **CS-05 · FIX · \[Main/Home\] Kafelek "Next Therapy Session" — brak ustawionej sesji**

* **Type:** FIX (includes a small new UI piece, see Open Questions)  
* **Location:** Main/Home, the "Next Therapy Session" tile, in the state where no upcoming session is set.  
* **Action:** Currently: tapping the tile in this state navigates to Therapy Timeline, with no way to add a session. Expected (per Darek, 2026-07-03): tapping opens an add-session flow directly in place. The user can add either a recurring or a single upcoming therapy session and pick the therapist. Functionally the same as the session setup in Settings, but designed to fit the Main/Home UI. Not a redirect to Settings.  
* **Why:** Dead-end state. A user with no session set has no path to add one from Main.  
* **Do NOT touch:** The existing session setup in Settings. It stays and remains the source of the underlying logic; reuse its logic/data layer and build only the Main-fitting UI on top. The tile's populated state (session already set) is covered by CS-04, not this item.  
* **Done when:** With no session set, tapping the tile opens the inline add-session flow; user can create a recurring or one-off session and select a therapist; the tile then shows the new session; no navigation to Therapy Timeline from this state.  
* **Risk:** Medium. New UI surface plus shared logic with Settings. Blast radius limited to the tile's empty state.

## **CS-06 · FIX · \[Main/Home\] Karta "Najnowsze odkrycie" → "Zobacz źródło"**

* **Type:** FIX  
* **Location:** Main/Home → card "Najnowsze odkrycie" → opened output card → button "Zobacz źródło".  
* **Action:** Currently navigates back to Main. Expected: opens the saved source the insight came from. Reference implementation that works correctly: Timeline → Odkrycia → Zapisane odkrycie → Zobacz źródło. Mirror that behavior. The Main entry point probably isn't passing the source reference to the output card.  
* **Why:** Button does nothing useful from the Main path; the identical button works from Timeline.  
* **Do NOT touch:** The working Timeline/Odkrycia flow. Fix the Main path only.  
* **Done when:** From Main, "Najnowsze odkrycie" → "Zobacz źródło" opens the same source screen as the Timeline path does for the same insight.  
* **Risk:** Medium. Shared card component; verify the Timeline path still works after the fix.

## **CS-07 · FIX · \[Reflect\] Pusta refleksja zapisywana przy zamknięciu aplikacji**

* **Type:** FIX  
* **Location:** Reflect, new-reflection editor, on app close/kill while a new empty reflection is open.  
* **Action:** Currently: back-navigation correctly discards an empty reflection, but closing the app persists it. Expected: an empty reflection is never saved, on any exit path (back, app close, app kill, backgrounding). The app-lifecycle save handler probably skips the is-empty check the back path has.  
* **Why:** Users end up with blank entries in their journal.  
* **Do NOT touch:** The back-navigation path, which already behaves correctly. Auto-save of non-empty drafts (if it exists) stays.  
* **Done when:** Opening a new reflection, typing nothing, and killing the app leaves no new entry in Reflect. A reflection with content is still saved as before.  
* **Risk:** Low. Guard clause on the lifecycle save path.

## **CS-08 · FIX · \[Reflect\] Błędna godzina zapisu refleksji**

* **Type:** FIX  
* **Location:** Reflect, saved-reflection timestamps.  
* **Action:** Currently: reflections save with a time 2 hours earlier than device time (e.g. 19:15 saves as 17:15). This matches storing UTC and displaying it without converting to local time (Poland is UTC+2 in summer). Expected: displayed time matches the device's local time. Recommended fix: keep storage as-is (UTC is fine) and convert to local timezone on display. Don't rewrite stored historical data.  
* **Why:** Every reflection shows a wrong time.  
* **Do NOT touch:** Timestamps in other features unless they share the same formatting utility. If they do, verify them after the change rather than leaving them inconsistent.  
* **Done when:** A reflection saved at 19:15 device time displays 19:15. Verify with a manual save and check an older entry also displays a sensible time.  
* **Risk:** Medium. Timezone fixes tend to live in a shared date formatter; check all screens that display reflection times.

## **CS-09 · FIX · \[Timeline/chipsy kategorii\] Ikona ptaszka na zaznaczonym chipie**

* **Type:** FIX  
* **Location:** Timeline, category filter chips, selected state. The checkmark ("ptaszek") icon on a selected chip.  
* **Action:** Currently: icon is black, invisible against the dark green selected-chip background. Expected: icon uses the same light color as the selected category's label text.  
* **Why:** Invisible icon.  
* **Do NOT touch:** Unselected chip styling; chip selection logic.  
* **Done when:** Selected chip shows a clearly visible checkmark in the label color, verified on the dark green background (both themes if the app has them).  
* **Risk:** Low. One color token.

---

## **CS-10 · CHANGE · \[Therapy Relationship \- Output\] Struktura tekstu outputu**

* **Type:** CHANGE  
* **Location:** Therapy Relationship output card, the generated text body. Probably an LLM prompt template change, not Flutter code.  
* **Action:** Currently a single block of text. Expected: output split into paragraphs, each with its own job, in this order:  
  1. Bullet points with the most important things.  
  2. Comparison of the current score to previous entries, with an explanation why (only if prior context exists).  
  3. Description of what the patient noticed about their therapeutic relationship.  
  4. The single most important thing recognized from this therapeutic relationship.  
* **Why:** Unstructured wall of text is hard to read.  
* **Do NOT touch:** Other output types (Check-in, Odkrycia, etc.) unless they share the same prompt template. If shared, split the template first.  
* **Done when:** A newly generated Therapy Relationship output renders in the four sections above; section 2 is omitted gracefully when there's no prior entry to compare against.  
* **Risk:** Medium. Prompt changes affect all future outputs; test with and without prior-entry context, in PL and ENG.

## **CS-11 · FIX · \[Therapy Relationship \- Output\] Niepełny transkrypt w "Twoje Odpowiedzi"**

* **Type:** FIX  
* **Location:** Therapy Relationship output card → expandable section "Twoje Odpowiedzi". Repro: record a voice note, close the conversation before the transcribed text appears on screen.  
* **Action:** Currently: the section shows only a fragment of what the summary was based on (in testing, a single word of the recorded voice note). Expected: the full transcript of the recording is shown. The UI likely captures whatever transcript text had streamed in before close, instead of the final complete transcript the summary itself used.  
* **Why:** User can't see what the AI based its summary on.  
* **Do NOT touch:** The summary generation itself. The summary appears to use the full input; this is about what's displayed in "Twoje Odpowiedzi".  
* **Done when:** Repro steps above show the complete transcript in "Twoje Odpowiedzi", matching the full recording content.  
* **Risk:** Medium. Touches the voice transcription lifecycle; verify the normal path (waiting for text before closing) still shows the full transcript too.

## **CS-12 · CHANGE · \[Output/Check-in\] "Twoje odpowiedzi" — usunąć zwijanie**

* **Type:** CHANGE  
* **Location:** Check-in output card, section labelled "Twoje odpowiedzi" (PL) / "Your Answers" (ENG). Currently collapsed behind a chevron.  
* **Action:** Remove the collapse/expand behavior. The answers are always visible; remove the chevron.  
* **Why:** Answers should be readable without an extra tap.  
* **Do NOT touch:** The section's content or the rest of the card layout. If the same collapsible widget is reused elsewhere (e.g. CS-11's "Twoje Odpowiedzi" on Therapy Relationship), confirm scope before changing it globally. See Open Questions.  
* **Done when:** Check-in output shows the answers expanded with no chevron, in PL and ENG; card scrolls correctly with long answers.  
* **Risk:** Medium. Depends on whether the collapsible is shared across output types.

### 

### **CS-13 · CHANGE · \[Timeline\] "Preps" in ENG version**

* **Type:** CHANGE  
* **Location:** Timeline section, label currently reading "Preps" when app language is English. Search ENG strings/ARB for "Preps".  
* **Action:** In the ENG locale, rename "Preps" → "Prep cards". Match the casing convention of surrounding Timeline labels (e.g. "Prep cards" vs "Prep Cards").  
* **Why:** Clearer name for what the section contains.  
* **Do NOT touch:** The PL locale label; the section's content, filtering, and navigation. Label only.  
* **Done when:** Timeline in ENG shows "Prep cards"; PL unchanged; grep for the old "Preps" string returns no live references in the ENG locale.  
* **Risk:** Low. String change.

---

## **Open Questions (resolve before or during execution)**

1. **CS-05:** Scoped as a fix but includes a small new inline add-session UI for Main/Home. If Mikołaj wants a fuller UX description (states, validation, recurring-session options), Darek can produce a feature-brief for it. Flag before building if needed.   
2. **CS-12 vs CS-11:** Does removing collapsing apply only to the Check-in card, or also to "Twoje Odpowiedzi" on the Therapy Relationship card? Spec assumes Check-in only, per the item's \[Output/Check-in\] tag.   
3. **CS-10:** Assumed this is a prompt-template change. If output formatting is post-processed in app code instead, apply the structure there.  
4. **CS-08:** Assumed store-UTC/display-local is the right fix. If timestamps are stored already shifted, the fix is at write time instead. Check stored values first.

## **Suggested execution order**

1. CS-01, CS-02, CS-03: locale string changes, no logic risk.  
2. CS-09: one color token.  
3. CS-04: navigation target swap (reuses CS-01's destination).  
4. CS-06: mirror the working Timeline path.  
5. CS-07: empty-reflection guard on app close.  
6. CS-08: timezone fix; check shared formatter fallout.  
7. CS-12: after resolving Open Questions 2 and 3\.  
8. CS-11: transcript lifecycle.  
9. CS-10: prompt change; test both locales, with and without prior context.  
10. CS-05: last; new UI surface, largest scope.

