## **MindSync Change Spec — Restore "Goals" in Stats, simplified to description \+ progress (keep deleted from Main)**

*For Claude Code · 2026-07-03 · author: Darek*  
 *Corrects over-execution of master spec D-01. Goals returns in Stats, trimmed to description \+ progress; Main stays without Goals.*

### **Summary**

* Total items: 2 (DELETE: 0 · FIX: 1 · CHANGE: 1\)  
* Areas touched: Stats (restore \+ trim), Main (confirm stays removed)  
* Intent: Recover the "Goals" feature deleted under D-01, surface it in **Stats**, and present each goal as **only its description and its progress** (no tags). **Main stays free of Goals.**

  ### **Global guardrails (read before touching anything)**

* This is a **restore**, not a rebuild. **Recover the original code from git history** (the D-01 commit) so the Goals data model, logic, and any endpoint come back intact — then re-home the UI in Stats.  
* **Do NOT re-add Goals to Main.** Only the Stats surface comes back.  
* ⚠️ **When trimming (CS-02), remove ONLY the tags.** Never delete the goals, their descriptions, or their progress. (This is the same trap that deleted "Główne tematy" — a "remove the tags" instruction was read as "remove the feature." Do not repeat it.)  
* If D-01 dropped a Goals table/migration, the restore must bring the schema/data back too.  
* After each item: run the app (Android \+ iOS); confirm Goals works in Stats, shows description \+ progress only, and is absent on Main.  
  ---

  ### **CS-01 · FIX · \[Stats\] Restore the "Goals" feature, surfaced in Stats**

* **Type:** FIX (restore feature deleted in error, relocated to Stats)  
* **Location:** Stats screen. Source of truth: the git commit that removed `Goals` under D-01. Lead: `git log`/`git show` for the Goals widget \+ data model \+ endpoint; grep `Goals` in history.  
* **Action:**  
  1. Recover from git the Goals feature D-01 deleted — data model, logic, and any backend/endpoint — to a working state.  
  2. Surface the Goals feature **in Stats**.  
  3. Do **not** restore the Main-screen Goals section or its entry point.  
* **Why:** Removed entirely by mistake; it should exist and be viewed from Stats.  
* **Do NOT touch:** The Main screen — no Goals there. Don't duplicate Goals if a remnant survived — restore one clean instance.  
* **Done when:** Goals is present and functional in Stats (reads/writes its real data); Main has no Goals section or entry point; app builds; no duplicate/orphaned Goals widgets.  
* **Risk:** Medium — depends on whether data/schema was dropped (git-restore vs. rebuild).

  ### **CS-02 · CHANGE · \[Stats\] Trim each goal to description \+ progress, remove the tags**

* **Type:** CHANGE (simplify presentation)  
* **Location:** Stats — the restored Goals section (from CS-01), each goal card/row.  
* **Action:** Present each goal as **only** its **description** and its **progress** (e.g. progress bar / %). **Remove the tags** displayed on each goal.  
* **Why:** Simpler Goals presentation in Stats.  
* **Do NOT touch:** ⚠️ The goals themselves, their descriptions, or their progress data — remove **only** the tag chips/labels. Do not delete goal entries or the Goals feature. The tag *data* can stay in the model; this is about the **presentation**.  
* **Done when:** Each goal in Stats shows its description \+ progress and **no tags**; all goals, descriptions, and progress remain intact; app builds.  
* **Risk:** Low–Medium — the one real risk is "remove tags" cascading into removing goals; the guardrail above prevents it.


