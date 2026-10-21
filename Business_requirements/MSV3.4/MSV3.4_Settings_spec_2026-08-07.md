MindSync Change Spec: MSV3.4 (menu boczne, 
Ustawienia, onboarding → Goals) 
For Claude Code · compiled 2026-08-07 · author: Darek (notes 07.08 + answer round 07.08, 
question feature) · zero open questions 
Summary 
- 
Total items: 16 (FIX: 2 · CHANGE: 14 · DELETE: 0; the Settings deletions live inside 
CS-10 as sub-points) 
- 
Areas touched: Onboarding · Main · Mood Trend · Workspace · menu boczne (szuflada) 
· Konto · Moja terapia · Subskrypcja · Ustawienia · app-wide strings 
- 
Intent: this batch rebuilds the side menu into four clusters with the account header on 
top, turns Ustawienia from an accordion stack into hub-and-spoke, moves the Settings 
Therapy section out into a "Moja terapia" hub, gives Subskrypcja its own menu entry, 
and wires the onboarding therapy goal into Workspace Goals. On top of that it takes 
over the two Main items from the unimplemented MSV3.3 spec, repairs the review 
button, and swaps the contact mail app-wide. 
Global guardrails (read before touching anything) 
- 
MSV3.3 (spec of 05.08) is NOT implemented yet. CS-02 and CS-03 below take over 
MSV3.3 CS-01 and CS-02. If MSV3.3 ships first anyway, skip CS-02 and CS-03 here 
and only verify them. 
- 
Polityka prywatności, Regulamin, FAQ and Udostępnij MindSync change nothing but 
their position in the new menu order (CS-06). Do not touch their screens or logic. 
- 
Two different therapist features exist. Do not mix them up, and do not delete either. Moja 
terapia (CS-08) receives the therapist list that belongs to the Settings Therapy schedule. 
The "Therapists" section inside Settings → Account is the unfinished therapist-panel 
linking and only gets hidden (CS-11). 
- 
Removing the Focus Areas section from Settings (CS-10) must not break the "Manage 
Focus Areas" / "Edit focus areas" sheet in Mood Trend (CS-04). The sheet and its data 
stay. 
- 
The menu target list in CS-06 is meant to be complete. The screens on Drive do not 
show today's drawer, so the from-state was not verified row by row. If today's drawer 
holds an entry this spec does not name, stop and flag it to Darek instead of deleting it. 
- 
Do NOT touch the Goals module itself. CS-01 only feeds goals through the existing 
creation path. The MSV3.3 guardrail on Goals as a design reference still stands. 
- 
After each item, run the app on Android and iOS and confirm no dead references and no 
broken navigation. 

 
 
A · Onboarding → Workspace 
CS-01 · FIX · [Onboarding → Cel terapeutyczny] · Cel z 
onboardingu trafia do Workspace → Goals 
- 
Type: FIX 
- 
Location: Onboarding → section "cel terapeutyczny" (goals) → the text the user types 
there. Target: Workspace → Goals module (the "THERAPY GOAL" cards with "+ Add 
goal" at the bottom). Lead: the goal creation path behind "+ Add goal". 
- 
Now (wrong): The goal typed during onboarding is lost. It reaches no feature. 
- 
Expected: Finishing onboarding creates a new goal in Workspace → Goals from the 
typed text, through the same path "+ Add goal" uses. A repeated onboarding creates 
another new goal; nothing is overwritten. Goals already supports many goals, so this 
item wires the input to the existing feature and adds nothing to Goals itself. 
- 
AI: Input: the goal text from onboarding. Trigger: goal creation when onboarding 
completes. Output: the standard goal card with the weekly narrative refresh, same as a 
manually added goal. Failure: the goal stays saved even when the narrative call fails, 
exactly like "+ Add goal". 
- 
Do NOT touch: The Goals module UI and its narrative pipeline; goals the user already 
has. 
- 
Done when: A fresh onboarding with goal text "X" ends with "X" visible as a goal card in 
Workspace → Goals; running Reset Onboarding and entering "Y" adds a second card 
next to "X"; both platforms. 
 
 
B · Main 
CS-02 · CHANGE · [Main] · Ikona "tune" → ikona "i" (info); "Edit 
Layout" usunięty 
- 
Type: CHANGE. Takes over MSV3.3 CS-01, which never shipped. Skip if MSV3.3 lands 
first. 
- 
Location: Main → top bar → right corner icon (currently the "tune" / sliders icon). 
Reached: open app → Main. The icon opens a view holding the screen description plus 
the "edit layout" mode. 

- 
What it is: Main's info panel: a description of the screen and an "edit layout" capability 
that lets the user reorder Main's modules. 
- 
Action: Replace the icon with the "i" info icon used on Timeline, Reflect, Workspace and 
Character. Inside, keep only the Main screen description. Remove the "edit layout" 
reordering entirely, UI and backend: entry points, saved layout state, persistence. 
- 
Logic: "i" → tap → the same info-view pattern as the other tabs, with Main's own 
description text (per the author, 07.08: the pattern is shared, the content is not) → close 
→ back on Main. 
- 
Outcome: Main behaves like every other tab: an "i" that explains the screen. Module 
order is fixed for everyone. 
- 
Value: Consistency across tabs, and one less feature to maintain. 
- 
Do NOT touch: The info icons and views of Timeline, Reflect, Workspace, Character 
(they are the model, not the target); the Main modules themselves. 
- 
Done when: Main's top-right icon is the "i"; its view shows only the description; no 
edit-layout entry point exists anywhere; grep for the edit-layout code returns no live 
references; users who had a custom order see the default order; both platforms. 
CS-03 · CHANGE · [Main → Mood Trend] · Ikona toggle/suwaczki 
→ ołówek (edit) 
- 
Type: CHANGE. Takes over MSV3.3 CS-02, which never shipped. Skip if MSV3.3 lands 
first. 
- 
Location: Main → Mood Trend module → its edit icon (currently the toggle/sliders icon). 
- 
Action: Swap the icon for a pencil (edit) icon, min. 24 px. Behavior stays the same: it 
opens the sheet redesigned in CS-04. 
- 
Logic: Pencil → tap → the "Edit focus areas" sheet slides up from the bottom (CS-04). 
- 
Do NOT touch: Mood Trend content, narratives, AI Summary. 
- 
Done when: Mood Trend shows a pencil of at least 24 px, the old icon is gone, and tap 
opens the sheet. 
CS-04 · CHANGE · [Main → Mood Trend] · Szuflada "Manage 
Focus Areas" → "Edit focus areas": nazwa, Safe Space, "+Add 
new" 
- 
Type: CHANGE 
- 
Location: Main → Mood Trend → pencil icon (CS-03) → the bottom sheet currently 
titled "Manage Focus Areas". 
- 
What it is: The sheet where the user manages the tracked moods and symptoms 
behind Mood Trend, split into Active and Archived sections. 
- 
UI anatomy (target, top to bottom): 
1. Sheet title: "Edit focus areas" (renamed from "Manage Focus Areas") 

2. Sections Active and Archived, unchanged 
3. New button "+Add new", for typing the name of a new mood or a new symptom 
4. Bottom margin with safe area: the sheet content must not overlap the system gesture 
bar ("szary kolor wyszarzenia telefonu") 
- 
Logic: 
- 
"+Add new" → tap → an inline text field opens inside the sheet → the user types 
a name and confirms → the item lands in Active and Mood Trend starts tracking 
it right away, chart and narratives included, like any tracked item. One flat list: the 
user does not pick a mood-vs-symptom type (decision 07.08). 
- 
Active and Archived rows → unchanged behavior. 
- 
Outcome: The user can add their own tracked item without leaving Mood Trend, and the 
sheet no longer collides with the gesture bar. 
- 
Value: Focus-area management lives next to the data it feeds; the Settings section that 
pretended to manage it goes away in CS-10. 
- 
Do NOT touch: The sheet's list data and backend (they must survive the Settings Focus 
Areas removal); the Mood Trend module beyond the icon (CS-03). 
- 
Done when: The title reads "Edit focus areas"; a name typed into "+Add new" shows up 
in Active and starts tracking; the sheet bottom respects the safe area on a gesture-nav 
device; Active and Archived work as before; both platforms. 
 
 
C · Workspace 
CS-05 · CHANGE · [Workspace → Next Session Agenda] · Ikona 
Edit Square przy dacie → Moja terapia 
- 
Type: CHANGE 
- 
Blocked by: CS-08 
- 
Location: Workspace → "NEXT SESSION AGENDA" → the date line of the next 
session (in the 22.07 screens: "Sunday, 10:00 · in 4 days") → new small icon next to the 
date. 
- 
Action: Add an Edit Square icon next to the session date. 
- 
Logic: Edit Square → tap → opens the Moja terapia hub (CS-08), main view → back 
returns to Workspace. 
- 
Outcome: One tap from the agenda date to the place where sessions are managed. 
- 
Value: The date stops being a dead label; a wrong session date can be fixed on the 
spot. 
- 
Do NOT touch: The agenda content, its topics list, "+ Add topic", the flag contract. 
- 
Done when: The icon renders next to the date, tap lands on Moja terapia, back returns 
to Workspace; both platforms. 

 
 
D · Menu boczne (szuflada) 
CS-06 · CHANGE · [Menu boczne] · Nowa struktura i kolejność 
- 
Type: CHANGE 
- 
Blocked by: CS-07, CS-08, CS-09 
- 
Location: The side drawer (hamburger menu) → all rows. 
- 
What it is: The app's main menu. Today it holds its entries in a different order, without 
the cluster dividers. Make sure all the names in settings are in the English version and 
Polish version respectively.  
- 
UI anatomy (target, top to bottom, order verbatim from the notes): 
1. Konto → AccountHeader 
2. ──── Divider (Klaster osobisty) 
3. Moja terapia 
4. Subskrypcja 
5. Ustawienia 
6. ──── Divider (Klaster info) 
7. Polityka prywatności 
8. Regulamin 
9. FAQ 
10. O MindSync 
11. ──── Divider (Klaster społeczność) 
12. Dołącz do społeczności (icon: Discord, CS-15) 
13. Zostaw recenzję 
14. Udostępnij MindSync 
15. ──── Divider 
16. Wyloguj się 
- 
Logic: 
- 
AccountHeader → tap → Konto screen (CS-07) 
- 
Moja terapia → tap → Moja terapia hub (CS-08) 
- 
Subskrypcja → tap → subscription screen (CS-09) 
- 
Ustawienia → tap → Settings (CS-10) 
- 
Polityka prywatności / Regulamin / FAQ → unchanged targets 
- 
O MindSync → unchanged target, row gets a chevron (CS-12) 
- 
Dołącz do społeczności → unchanged target, new icon (CS-15) 
- 
Zostaw recenzję → fixed flow (CS-14) 
- 
Udostępnij MindSync → unchanged 
- 
Wyloguj się → confirmation pop-out (CS-16) 

- 
Outcome: A menu in four readable clusters: personal, info, community, logout In English 
for English version and Polish for Polish version  
- 
Value: Today's menu mixes personal hubs with legal links; the clusters make it 
scannable. 
- 
Do NOT touch: The screens behind Polityka prywatności, Regulamin, FAQ and 
Udostępnij MindSync. Any drawer entry not named in anatomy 1-16: stop and flag 
(guardrail), do not delete silently. 
- 
Done when: The drawer matches anatomy 1-16 exactly, dividers included; every row 
opens its target; nothing unlisted disappeared without a flag; both platforms. 
CS-07 · CHANGE · [Menu boczne → Konto] · "Usuń konto" na 
dole ekranu Konto 
- 
Type: CHANGE 
- 
Location: Drawer → AccountHeader → the existing Konto screen → new element at the 
very bottom. Source of the move: Settings → Account & Support → "Usuń konto". 
- 
What it is: The account screen behind the drawer header. It exists today and stays as it 
is, build version info included (decision 07.08). 
- 
Action: Add a red "Usuń konto" button at the very bottom of the screen. Move the 
delete-account capability out of Settings → Account & Support; same backend, new 
entry point. 
- 
Logic: 
- 
"Usuń konto" → tap → pop-out: header "Usuń konto", body "Tej operacji nie 
można cofnąć. Wszystkie Twoje dane zostaną trwale usunięte.", red button 
"Usuń konto", ghost button "Anuluj" (copy approved 07.08). 
- 
Red "Usuń konto" → deletes the account and its data immediately → the app 
lands on the login/registration screen. No extra safeguard: no password re-entry, 
no typed confirmation (decision 07.08). 
- 
"Anuluj" → closes the pop-out, nothing changes. 
- 
Outcome: Account deletion sits where users expect it, on the account screen, behind 
one clear warning. 
- 
Value: Deletion buried in a Settings accordion was hard to find; the stores require it to be 
reachable. 
- 
Do NOT touch: The rest of the Konto screen; the build version info (stays where it is); 
the deletion backend (relocation only). 
- 
Done when: The red button sits at the bottom of Konto; the pop-out shows the exact 
copy above; confirm deletes and lands on login; Anuluj backs out; the old entry in 
Settings is gone (CS-10); both platforms. 

CS-08 · CHANGE · [Menu boczne → Moja terapia] · Hub 
zarządzania terapią (z Settings → Therapy) 
- 
Type: CHANGE 
- 
Location: Drawer → new entry "Moja terapia" → hub screen. Source: the whole 
Therapy section sitting in Settings today (the set-therapy hub-and-spoke: date, time, 
cadence). 
- 
What it is: Session scheduling currently lives inside Settings. This item moves it out into 
its own hub in the menu and adds the therapy modality picked at onboarding. 
- 
Content of the hub: 
1. Harmonogram terapii: adding and removing sessions, calendar; the existing Settings 
→ Therapy functionality moved 1:1. "Częstotliwość terapii" from the notes is the cadence 
element of this schedule, not a separate feature (decision 07.08, derived: "przenoszone 
zgodnie z opisem, więc to ta sama"). 
2. Lista terapeutów: the therapist list used by scheduling. This is NOT the hidden 
"Therapists" section from Account (CS-11). 
3. Nurt terapii: the modality chosen in onboarding. The value is saved today; here the user 
sees it and can change it. AI does not read it yet; this screen only stores and shows it 
(decision 07.08). 
- 
Logic: Drawer row → tap → hub with the three areas above. Schedule and therapist 
controls keep their current behavior, relocated. Nurt terapii → tap → edit the stored value 
(same options as onboarding) → save. 
- 
Outcome: One place to manage sessions, therapists and modality, reachable from the 
menu instead of the bottom of Settings. 
- 
Value: Therapy management is a core loop of the app, not a setting. 
- 
Do NOT touch: The scheduling logic and data layer (this is a relocation, not a rewrite); 
the Account "Therapists" section (CS-11 hides it separately); the notification logic that 
reads session dates (the MSV3.3 CS-18 contract: weekly, biweekly and custom dates all 
count). 
- 
Done when: The hub opens from the drawer; sessions can be added and removed with 
the calendar as before; the therapist list works; Nurt terapii shows the onboarding value 
and saves an edit; Settings no longer shows the Therapy section (CS-10); both 
platforms. 
CS-09 · CHANGE · [Menu boczne → Subskrypcja] · Ekran 
subskrypcji za pozycją menu 
- 
Type: CHANGE 
- 
Location: Drawer → new entry "Subskrypcja" → the existing subscription screen. Reuse 
it, do not build a new one (decision 07.08). The Settings "subskrypcja" banner that opens 
it today goes away in CS-10. 

- 
What it is: The subscription screen the app already has, now shown in one of two tier 
states. 
- 
Action: 
- 
Free tier: the freemium view, plus a field for typing a promo code. The field 
moved from Settings → Account & Support and keeps the same backend. 
- 
Premium tier: the premium view, with the information that the subscription is 
active. No promo code field here. 
- 
Logic: Drawer row → tap → the screen in the state matching the user's tier. Promo code 
field → enter code → the existing promo backend validates and applies it, same as it 
does today from Settings. 
- 
Outcome: Subscription has a permanent home in the menu; free users can redeem 
codes there. 
- 
Value: The Settings banner was the only route to the paywall; the menu is where users 
look for it. 
- 
Do NOT touch: The paywall/purchase flow itself; the promo backend (relocation only); 
store-side subscription management. 
- 
Done when: On a free account the drawer entry shows the freemium view with a 
working promo field; on premium it shows the premium view with the active info and no 
promo field; the Settings banner is gone (CS-10); both platforms. 
CS-10 · CHANGE · [Ustawienia] · Przebudowa: akordeony → 
hub-and-spoke, nowa zawartość 
- 
Type: CHANGE 
- 
Blocked by: CS-07, CS-08, CS-09 
- 
Location: Drawer → Ustawienia → the whole Settings screen. Today it is a stack of 
accordions. 
- 
What it is: The settings screen. After this item it holds only what is listed below; 
everything else either moved out (CS-07, CS-08, CS-09) or is deleted here. 
- 
UI anatomy (target, top to bottom, per the author's answers of 07.08): 
 
1. Week Starts On (pill, directly on the screen, as today) 
2. Select Voice (pill, as today) 
3. Select AI Language (pill, as today) 
4. Persona AI (pill, as today) 
5. Notyfikacje: the full list of notification settings, expanded, no accordion 
6. Show App Tour (button, moved from Account & Support) 
7. Reset Onboarding (button, moved from Account & Support) 
 
The two buttons sit BELOW notifications. The author confirmed this on 07.08 and it overrides 
the notes' "nad notyfikacjami". 
 

- 
Removed in this item: 
- 
the "subskrypcja" banner (replaced by the drawer entry, CS-09) 
- 
section Focus Areas: frontend removal only. It was supposed to manage the 
Mood Trend sheet but does not work. The sheet (CS-04) and its data stay. 
- 
section Privacy & Data: full removal, UI and backend. Nothing moves out of it 
(decision 07.08). 
- 
section "Main tab Widget": full removal. 
- 
"Give feedback" from Account & Support: full removal. 
- 
whatever remains of Account & Support after the moves: the emptied section 
disappears. 
- 
Outcome: Settings is one flat, short screen: account, four pills, notifications, two buttons. 
- 
Value: The accordion stack hid basic settings behind extra taps and mixed them with 
features that were not settings at all. 
- 
Do NOT touch: The behavior behind the pills; the notification settings and their logic; the 
Mood Trend sheet data (the Focus Areas removal is frontend only); anything already 
relocated by CS-07, CS-08, CS-09. 
- 
Done when: Settings matches anatomy 1-7; the removed pieces are gone (Focus Areas 
from the frontend only; Privacy & Data and Main tab Widget with their backends; Give 
feedback; the banner; the emptied Account & Support); grep finds no live references to 
the removed sections; notifications render expanded; both platforms. 
CS-11 · CHANGE · [Account] · Sekcja Therapists schowana (kod 
zostaje) 
- 
Type: CHANGE (hide, not delete) 
- 
Location Account section → "Therapists": the unfinished functionality for linking the 
account with the therapist panel. 
- 
Action: Hide the section and every user-facing entry point of the therapist-panel linking. 
Keep all the code, frontend and backend. The feature is unfinished and comes back 
once it is. 
- 
Known suspect entry point: the "Share my check-ins with my therapist" toggle seen 
in July builds under Therapy Relationship. If it is wired to the panel linking, hide it under 
this item; if it is something else, leave it and flag it. 
- 
Logic: No user-facing element of the panel linking stays tappable anywhere. 
- 
Outcome: Users stop finding a door to a feature that does not work yet. 
- 
Value: A half-built linking flow in Account erodes trust. 
- 
Do NOT touch: The code (front and back stays in the tree); the therapist list inside Moja 
terapia (CS-08), which is a different feature. 
- 
Done when: No screen shows the Therapists section or any other entry to the panel 
linking; the code still compiles and stays; the Moja terapia therapist list still works; both 
platforms. 

CS-12 · CHANGE · [Menu boczne → O MindSync] · Chevron 
right 
- 
Type: CHANGE 
- 
Location: Drawer → "O MindSync" row → right edge. 
- 
Action: Add a chevron right, the same one the Subskrypcja and Ustawienia rows have. 
- 
Logic: Unchanged: tap opens the O MindSync screen. 
- 
Do NOT touch: The O MindSync screen content (its mail changes app-wide via CS-13). 
- 
Done when: The row shows the chevron and matches Subskrypcja and Ustawienia. 
CS-13 · CHANGE · [App-wide] · support@mindsync.app → 
hello@mindsync.app 
- 
Type: CHANGE 
- 
Location: Every place the app shows or uses support@mindsync.app. The one named 
in the notes is the contact mail on O MindSync; the author widened it to the whole app 
(07.08). 
- 
Action: Replace the address with hello@mindsync.app everywhere: visible strings and 
mailto links, both locales. 
- 
Do NOT touch: Anything else on the O MindSync screen. 
- 
Done when: grep for "support@mindsync.app" returns no live references; O MindSync 
shows hello@mindsync.app; both platforms. 
CS-14 · FIX · [Menu boczne → Zostaw recenzję] · Natywny 
in-app review 
- 
Type: FIX 
- 
Location: Drawer → "Zostaw recenzję" row. 
- 
Now (wrong): The button does not get the user to a review. The author marked it 
"napraw guzik"; how exactly it fails today was not recorded, so confirm the current 
behavior during QA and note it in the PR. 
- 
Expected: Tap → the native in-app review dialog: on iOS the StoreKit review prompt 
(SKStoreReviewController / requestReview), on Android the Google Play In-App Review 
API. The "Enjoying MindSync" pop-out from the notes is this system dialog, not a custom 
screen (decision 07.08). Both APIs are quota-limited and can silently show nothing; 
when the system suppresses the dialog, open the app's store review page directly as a 
fallback (compiler call, flagged for veto). 
- 
Do NOT touch: Udostępnij MindSync next to it; the drawer structure (CS-06). 

- 
Done when: Where the quota allows it, tap shows the native rating dialog, on iOS and 
on Android; when the system suppresses it, the store review page opens; no tap ends in 
nothing. 
CS-15 · CHANGE · [Menu boczne → Dołącz do społeczności] · 
Ikona Discord 
- 
Type: CHANGE 
- 
Location: Drawer → "Dołącz do społeczności"  
- 
Action: Swap the icon for the Discord icon. Link and behavior stay as they are. 
- 
Logic: Unchanged: tap opens the community invite as today. 
- 
Do NOT touch: The invite link target. 
- 
Done when: The row shows the Discord icon and still opens the same invite. 
CS-16 · CHANGE · [Menu boczne → Wyloguj się] · Pop-out 
potwierdzenia 
- 
Type: CHANGE 
- 
Location: Drawer → "Wyloguj się" row. 
- 
Action: Tap no longer logs out directly. It opens a confirmation pop-out first. 
- 
UI anatomy (pop-out, strings verbatim from the notes): 
1. Header: PL "Wyloguj", ENG “Log out”  
2. Subtitle: "Na pewno chcesz się wylogować?" 
3. Button "Wyloguj", accent colour 
4. Ghost button "Anuluj" 
- 
Logic: 
- 
Row → tap → pop-out opens. 
- 
"Wyloguj" → logs out; the spinner runs and the app lands on the login/registration 
screen by itself. 
- 
"Anuluj" → closes the pop-out, the user stays logged in. 
- 
Note: the July notes recorded a bug where the logout spinner spun forever and only an 
app restart reached the login screen. If that still happens, fixing it is inside this item, 
because the Done-when below fails otherwise. 
- 
Outcome: No accidental logouts, and logout actually ends on the login screen. 
- 
Value: Logout sat one tap away with no confirmation. 
- 
Do NOT touch: Session and auth handling beyond what landing on the login screen 
requires. 
- 
Done when: Tap shows the pop-out with the exact strings above; Anuluj backs out; 
Wyloguj ends on the login screen without restarting the app; both platforms. 
 
 
