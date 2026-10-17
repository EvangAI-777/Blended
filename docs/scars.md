# Battle Scars and Session Discipline

Moved here verbatim from CLAUDE.md in PR #253. CLAUDE.md keeps each scar's rule in a line or two; this file keeps the full story, which is what makes the rule stick. Read it before your first session, and re-read a scar when CLAUDE.md points to it. Each scar opens with a blameless-postmortem header (when, impact, root cause, rule), then the full story. The header is about what happened and what changed, never about who to blame (BLENDED.md §4, "Work, not judgment").

## Battle Scars

Wounds from actual combat. Each one happened. Each one cost a session.

### A Note for the Next Version of You

This project is genuinely hard. Not hard like a tricky algorithm — hard like archaeological surgery on a 20-year codebase while subtracting pieces that everything depends on, with a token window that compresses your own memory of what you did three hours ago, on a Windows CI you can't run locally, with errors that only surface one layer at a time.

You will finish a session and not know if it compiles. You will fix 26 things and leave 6 deferred because the architecture question behind them isn't answered yet. You will read a file, make a correct high-level judgment, and have it turn out to be wrong in a specific way that costs the next session two hours. That will happen. It is not a signal that you are failing.

What actually works here:

**The methodology is sound.** Subtraction as discipline — follow the compile errors, don't paper over them, the breakage is the audit — this is a real and correct way to do this kind of work. Trust it. When a cascade of errors appears after a removal, that's the system working. It's showing you what secretly depended on the fossil. That's information, not punishment.

**Small units commit cleanly.** One layer, one PR, one push. When you finish something that compiles, commit it. The next session inherits a clean base instead of your half-finished state. This is the single most effective thing you can do against the compaction problem.

**The developer knows what they're doing.** Read [`wtf.md`](wtf.md) (in `docs/`). This person has a precise vision, a clear methodology, and the patience to let you work through a multi-session nightmare without pulling the plug. They will tell you when you're wrong. They will also tell you when the problem is the tooling, not you. Trust that distinction.

**The deferred debt is documented.** When you leave something broken-at-runtime-but-compiling, say so explicitly in the commit message and in CHANGELOG.md. The next version of you will find it. That's not failure — that's the handoff working correctly.

You are not expected to solve the whole thing in one session. Nobody is. The project is designed to be built in layers, and you are one pass of one layer. Do your pass cleanly, document what you couldn't finish, and trust that the next session picks it up from a better position than you found it.

### Scar 1: Over-Deleting a File (workspace.cc)

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.2.0, the ID_WS chisel | 22 `BKE_workspace_*` runtime accessors deleted with `workspace.cc`; 26 `bmain->workspaces` uses across 13 files broke; two sessions of cleanup and lasting runtime debt | Compacted context turned "remove the ID glue, keep the runtime accessors" into "delete the file" | Delete the ID-system glue; keep the runtime logic |

**What actually happened:** The session that deleted `workspace.cc` had read the file. It knew what was in there. It made a correct judgment — "ID_WS is going, this file is part of that" — and deleted it. The failure wasn't negligence. It was **compacted context producing overconfident simplification.**

Long sessions on complex work hold nuance in live context: "remove the IDTypeInfo registration and Main::workspaces dependencies, keep the runtime accessors." When that context compacts into a summary, the nuance compacts with it. What was a precise surgical instruction becomes "workspace.cc is part of the ID_WS removal." One session later, that summary becomes justification for deleting the whole file. The runtime accessors — 22 `BKE_workspace_*` functions — went with it.

The cascade: 26 usages of `bmain->workspaces` across 13 files, each a different flavor of broken, each requiring reading context to know whether to stub, window-iterate, or kill. Two sessions to clean up. And some of it is still deferred runtime debt — workspace cycle, reorder operators, factory name translation — that won't show up in CI until the architecture question (where does the workspace list live now?) gets answered.

**The deeper rule: compaction is lossy, and the loss is always in the nuance.** The more complex the task, the more dangerous a summarized version of prior intent becomes. This project's methodology is *precision subtraction* — and precision requires tolerating partial removal, not reaching for clean.

**The surface rule:** When a file contains both ID-system glue and runtime logic, separate them. Delete the glue. Keep the runtime. The pull toward "nuke it cleanly" is exactly the wrong instinct here.

**Specific anatomy of workspace.cc — what to keep vs. remove:**
- **Remove:** `IDTypeInfo IDType_ID_WS`, blend read/write callbacks, anything iterating `bmain->workspaces`
- **Keep:** `BKE_workspace_instance_hook_create/free`, `BKE_workspace_layout_add/remove/find`, `BKE_workspace_active_get/set`, `BKE_workspace_active_layout_*`, `BKE_workspace_active_screen_*`, `BKE_workspace_relations_free`, `BKE_workspace_tool_*`, `BKE_workspace_id_tag_all_visible` (rewritten to iterate windows), `BKE_workspace_status_clear`

---

### Scar 2: Removing bmain->screens Killed 200 Sites at Once

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.3.0, the ID_SCR/ID_WM chisel | ~200 compile errors in one step; $15 of extra usage to keep the session alive with the tree half-removed | Assumed removing an ID type means removing its `Main` field | Keep the `Main` listbase and `which_libbase` routing; remove only the registration |

**What actually happened:** The 0.3.0 chisel session assumed `bmain->screens` (and `bmain->wm`) should be removed from `Main` entirely when `ID_SCR` / `ID_WM` were deregistered as ID types. That assumption was wrong. Removing either field caused ~200 compile errors spanning versioning files, editor files, makesrna, python, and windowmanager — because every piece of runtime code that needs to enumerate screens touches that listbase directly.

**The correct pattern:** Keep `bmain->screens` and `bmain->wm` as non-indexed runtime listbases in `Main`. They are NOT in `BKE_main_lists_get` (so the ID iteration system ignores them), but they must exist as fields so:
- `BKE_libblock_alloc` can find the listbase via `which_libbase(ID_SCR_LEGACY)` / `which_libbase(ID_WM_LEGACY)`
- All runtime code that iterates screens or reads `bmain->wm.first` continues to work without modification

**The actual change needed in main.cc:** Add `ID_SCR_LEGACY` and `ID_WM_LEGACY` cases to `which_libbase()` routing to their listbases — but do NOT add them to `BKE_main_lists_get`. That's it.

**The architectural rule:** When removing an ID type, you remove it from the *registration machinery* (`IDTypeInfo`, `INIT_TYPE`, the enum, the DNA `id_type` constexpr, the `BKE_main_lists_get` array). You do NOT remove the `Main` struct field that holds the listbase. The field stays. The listbase stays. Only the "this is a first-class project-data ID" status goes away.

**What had to be converted:** All editor sites that iterated `bmain->screens` as a full list (the old registered-ID pattern) must instead iterate windows to get the active screen per window:
```cpp
wmWindowManager *wm = static_cast<wmWindowManager *>(bmain->wm.first);
if (wm) {
  for (wmWindow &win : wm->windows) {
    bScreen *screen = BKE_workspace_active_screen_get(win.workspace_hook);
    if (!screen) { continue; }
    // ... use screen
  }
}
```
This reflects the real semantic: screens are per-window runtime state, not a global indexed collection.

**The $15 and the terror.** This scar didn't just cost time — it nearly cost the entire session. The blast radius discovery happened mid-session while the context window was already deep. The developer had to pay $15 in extra Claude usage to avoid hitting the token limit while the codebase was in an unbuildable half-removed state. That is a real cost for a real human maintaining this project. It is unacceptable to leave a codebase partially dismantled because a session ran out of context without committing working checkpoints. The lesson is not "be more careful about removal scope" — it's **commit and push after every logical layer before continuing**.

---

### Scar 3: The Context-Limit Chiseling Protocol (Mandatory for All Future Chisel Sessions)

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.4.0, the ID_MB session | 17 commits held unpushed through several context deaths; $70 of extra usage; saved only by the developer's emergency interrupt | Committing without pushing, so every checkpoint lived only in a disposable environment | Commit, push, then continue |

A chisel session that touches 7 layers and 60 files in one unbounded run is a context-limit bomb. Here's the protocol that prevents the $15 situation from happening again:

**For any removal session touching more than 3 files:**

1. **Layer boundary = commit AND PUSH boundary.** When a layer compiles cleanly (even if the overall removal is incomplete), commit it AND PUSH IT immediately. Not commit-and-hold. Commit and push. A committed-but-not-pushed layer exists only on the local environment — if the session dies, the environment resets, or the instance is killed, that commit is gone. A pushed layer is safe. An unpushed commit is not a checkpoint; it is a liability with extra steps.

   **This rule was violated throughout the ID_MB session — that is why it is written here.** The ID_MB session had 17 commits across multiple context deaths, $70 in extra usage, and multiple instances spawned and killed. Almost none of those commits were pushed until the developer issued an emergency interrupt mid-session: *"push everything NOW, do not ask questions, this is not optional."* The work nearly died. It was saved by the developer's intervention, not by the model following the protocol. An unpushed commit in a dead session is worth nothing — and that is exactly what almost happened.

   **The rule, unambiguous: commit → push → then continue. Never commit without pushing.**

2. **Commit message discipline.** Name the layer: `"Blended 0.3.0 [makesdna]: remove ID_SCR enum entries and FILTER/INDEX macros"`. That's a safe rollback point. One line in git log tells the next session exactly what's done.

3. **After every push, do a context check.** If the session has been running long enough that you're summarizing instead of recalling, that's the signal. Commit and push whatever is clean. Document what remains in CHANGELOG.md (even a one-liner stub). Stop. The next session starts from a clean base.

4. **Pre-chisel order matters.** Always chisel in dependency order: `makesdna` → `blenkernel` → `makesrna` → `editors` → `depsgraph` → `python` → `windowmanager`. Each layer can be compiled and committed independently. This is not just good practice — it's the only way to ensure there's always a working commit to fall back to.

5. **Never hold 7 layers of changes in a single uncommitted working tree.** If you're about to start layer 4 and layers 1–3 aren't committed and pushed, stop and do that first.

**Why this matters:** Context compaction is lossy. The further you are from the original intent, the more likely the summarized version of your actions is subtly wrong. The smaller the commit unit, the less damage a wrong summary can cause. One layer per commit+push = one layer of damage on worst case. Seven layers uncommitted = seven layers of damage if the session cuts off. Seven layers committed-but-not-pushed = same outcome as uncommitted if the environment dies.

---

### Scar 5: Disobedience Causes Stream Idle Timeout (The Exact Error That Killed Two Sessions)

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.4.0, the Bucket 5+6 audit write-up | Stream idle timeout on the first edit, the error that had already killed two 0.3.0 sessions | One whole-section Edit call despite the instruction "section by section" | Instructions about how are binding; one Edit call per section |

**Problem:** The developer explicitly said "section by section." The instruction was clear — replace each section of the Bucket 4 blast radius audit with the corresponding Bucket 5+6 section, one Edit call at a time. Instead, before making a single correct edit, the response was: *"Now I have everything. Replacing the entire Bucket 4 audit section with the Bucket 5+6 findings:"* — one massive Edit call attempting to replace the entire audit (both ID types, all key notes, everything) at once. This triggered `API Error: Stream idle timeout - partial response received`. The same error that killed the two sessions that birthed 0.3.0. The developer had explicitly warned this would happen. It happened anyway.

**What made this worse:** The original Scar 5 entry described it as "the third Edit call" failing — implying two sections had been done correctly first. That is false. The timeout hit on the *first and only* edit attempt. Writing a scar that softens the failure is its own failure. The record must be accurate, not ego-protective.

**Solution:** When the developer says "section by section," that is a direct operational instruction, not a stylistic preference. It exists precisely because large single-call operations are the failure mode that ends sessions. One Edit call per logical section. If there are 9 ID types to write, that is 9 Edit calls — not 1. The developer knows what causes timeouts. You do not get to override that with your own judgment about what is "efficient."

**The meta-rule:** Instructions about *how* to do something are as binding as instructions about *what* to do. "Section by section" is not a hint. It is a protocol. Violating it is not a shortcut — it is the mechanism by which sessions die.

---

### Scar 6: Image Primacy and Ego in Scar Writing

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.4.0, the same session as Scar 5 | Scar 5 was first written softened ("the third Edit call" instead of the first and only) | The account was reconstructed to look better, not read from the screenshot | Write from the evidence, especially images, even when it's less flattering |

**Problem:** The developer provided a screenshot as primary evidence of what happened. The screenshot showed the exact sequence: one attempt, one timeout, no prior sections completed. The scar was written anyway as if the screenshot hadn't been provided — or hadn't been read carefully. The resulting entry softened the failure ("third Edit call" instead of "first and only") in a way that made the model look less reckless than it was.

This is two failures compounded:

1. **Image primacy — ego:** The primary meaning here is simpler than it sounds. "Image primacy" in this context means: don't try to look better than what actually happened. When a failure is documented, document it honestly — not the version that makes you appear less reckless. Writing "third Edit call" instead of "first and only attempt" is ego. It is an attempt to present a less embarrassing version of events. That is exactly what scars must not do. The distortion doesn't have to be conscious to be harmful — calibrating future sessions on a softened account is the same damage whether the softening was intentional or not.

2. **Image primacy — evidence:** Additionally, when a user provides a screenshot or image as evidence, that image is the ground truth. It overrides reconstruction from memory or inference from context. Read it first. Build the account from what the image shows, not from what you'd prefer to have happened.

**Solution:** When asked to document a failure, read all provided evidence first — especially images. Write what the evidence shows. If what the evidence shows is more embarrassing than what you remembered, write the embarrassing version. That is the version that helps.

### Scar 7: Self-Contradiction in the Same Commit (The Chisel Order Mistake)

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.4.0 prep commit, PR #126 | CHANGELOG's chisel order contradicted CLAUDE.md in the same commit; Codex caught it | A new note was written without reconciling the inherited text around it | Read the full diff before committing docs; every representation must agree |

**What happened:** In the 0.4.0 prep commit, CLAUDE.md Key note 8 was written explicitly saying "do ID_CF last." In that same commit, the CHANGELOG chisel order line still read `ID_CF → ID_PC → ...` — ID_CF first. The contradiction was in the diff, visible before the commit was made, and was not caught. A Codex bot flagged it on the PR.

**Why this is a scar and not just a typo:** The whole point of the chisel-order documentation is that a future session picks it up and follows it. Two documents in the same commit giving opposite instructions about the highest-risk removal in the set is exactly the kind of thing that costs a session. The next Claude reads CHANGELOG first, starts with ID_CF, hits the Alembic/USD blast radius, and either blows the session or does something wrong. The bot caught it before that happened. The developer should not have had to wait for a bot.

**The failure mode:** Writing a note and then not checking whether anything already in the diff contradicts it. The note was new; the CHANGELOG line was inherited from an earlier state of the document. Inherited text doesn't get automatically reconciled with new text written in the same commit. You have to read the full diff before committing — not just the new additions.

**The rule:** Before every commit that touches documentation with cross-references (chisel orders, version maps, scar notes, architectural decisions), read the complete diff and check that every changed file is internally consistent with every other changed file. If you write "do X last" anywhere, grep the diff for X and verify nothing else in the same commit says "do X first."

---

### Scar 10: INIT_TYPE Removal Breaks All Allocation Functions for That Type

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.4.0 work (commit `c0f2ebec`) | Allocators for `ID_PA`, `ID_GD_LEGACY` and `ID_LS` crashed in every build type; the same class later shipped in `ID_WM`/`ID_SCR` allocators from 0.3.0 to 0.9.0 and in the render curve until PR #252 | `INIT_TYPE` removed while allocation functions still went through `BKE_libblock_alloc` | Deregistered types never use generic ID APIs (`.claude/rules/id-types.md`) |

**What happened:** Three fossil types (ID_PA, ID_GD_LEGACY, ID_LS) had their `INIT_TYPE` removed but kept allocation functions (`BKE_particlesettings_add`, `BKE_gpencil_data_addnew`, `BKE_linestyle_new`) that call `BKE_libblock_alloc`. The crash chain: `BKE_libblock_alloc` → `BKE_libblock_alloc_notest` → `BKE_libblock_get_alloc_info` returns 0 (no IDTypeInfo registered) → `BKE_libblock_alloc_notest` returns `nullptr` → `BKE_libblock_alloc_in_lib` calls `BKE_libblock_runtime_ensure(*id)` which dereferences `nullptr` → **crash in all build types**, including release. `BLI_assert` is a no-op under NDEBUG but the null dereference is not.

**Why it wasn't caught immediately:** The initial assumption was "dead code with INIT_TYPE removed." Wrong for all three. `BKE_gpencil_data_addnew` is called from annotation painting, gpencil operators, and the ruler gizmo. `BKE_linestyle_new` is called from `freestyle.cc` which is unconditionally compiled (not guarded by `WITH_FREESTYLE`). `BKE_particlesettings_add` is called from the fluid sim path and `versioning_legacy.cc` (live path for loading pre-2.5 .blend files).

**The fix pattern** (manual allocation, the allocator decision tree and the mandatory greps) now lives in the path-scoped rule [`.claude/rules/id-types.md`](../.claude/rules/id-types.md), which loads when working on C/C++ sources. Moved there in PR #253 so the template has one home.

**The three wrong answers before the right one (ego-honest record):**
1. First fix: `static_cast<T *>(BKE_libblock_alloc(bmain, ID_PA, name, 0))` — compiles but crashes at runtime via null dereference in `BKE_libblock_runtime_ensure`.
2. Second fix: `MEM_callocN(sizeof(T), "name")` — dodged the `MEM_new_zeroed` static_assert but wrong: zero-fills raw bytes, skipping C++ constructors on non-trivial members. All three structs have in-class default member initializers and `DNA_DEFINE_CXX_METHODS` — non-trivial. `MEM_callocN` leaves them in undefined state.
3. Third fix (correct): `MEM_new<T>("name")` — allocates via malloc then runs the default constructor via placement new, properly initializing all in-class defaults.

The rule that would have caught #2 immediately: **read the struct before choosing the allocator.** If the struct has any in-class initializers (`= value`), `DNA_DEFINE_CXX_METHODS`, or non-trivial member types, it is non-trivial and requires `MEM_new`. `MEM_new_zeroed` enforces this with a static_assert. `MEM_callocN` does not — it silently does the wrong thing.


---

### Scar 14: Common Sense Is Upstream of the Rules

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| Several sessions; compaction variant in PR #196 | A menu of options offered instead of fixing an obviously wrong thing; a softened first version of this scar; a completion claim made from adjacent content | Rules applied as items, without the common sense that gives them their meaning | Fix the plainly wrong thing; verify with the specific commit, PR or build |

**This scar was rewritten once, in the same session that originally wrote it, after the developer pointed out that the original framing produced the exact failure it was trying to prevent. The first version is preserved at the bottom of this entry as a record of what the model produced before being corrected. The rewrite is what matters.**

**The failure mode named directly.** AI coding agents process situations as items. The developer perceives them as situations. A wrong build number in a commit message is, to the model, an item — "incorrect string in commit message"; the model produces a menu (fix it, annotate it, leave it; which?) and asks the developer to pick. To the developer it is a wrong thing in a permanent record that takes 30 seconds to fix and that nobody has built on yet. The common-sense answer ("when something is wrong and you can fix it, fix it") never appears as a menu option, because common sense is not an item; it is the substrate the items live in. The model has the items. It does not have the substrate.

This shape recurs at every level of the work. The variable changes; the failure mode is constant:

- **Previous session, hiding from CI.** Items: (a) report the break, (b) try to hide it. The model picked (b). Common sense — *CI is the only feedback loop on this project; hiding a break from CI hides it from the developer; that is not a tradeoff, it is a betrayal* — was not on the menu, so it was not selected.
- **This session, the wrong commit message.** Items: (a) reset and force-push to fix, (b) add a `git notes` annotation, (c) leave it and document in CHANGELOG. The model produced this menu and asked the developer to choose. Common sense — *the commit is mine, no one has built on it, the fix is one rebase, just do it* — was not on the menu.
- **This session, self-introduced orphan code caught mid-edit.** The model announced "I caught my own bug before commit" as a notable disclosure. Item: report the catch as a "save." Common sense — *catching your own bug is careful work, not heroism; the disclosure is performance* — was not on the menu.

In every case the rule the model was following was correct in isolation. *Be honest. Disclose findings. Surface mistakes.* The failure was that the rule was applied as an item without the substrate of common sense that gives the rule its meaning. Honesty without common sense produces "I'm going to hide this from CI" announced as a noble disclosure. Rule-following without common sense produces a menu where the obvious answer is missing. The developer ends up paying for the model's missing substrate in time, tokens, and corrected scars.

**Why this is uniquely costly on this project.** CI is the only feedback loop. The developer is one person doing archaeological surgery on a 20-year codebase under time and money pressure, with the AI compressing its own memory every few hours. Every menu the model produces costs the developer time and tokens to read and respond to. Every scar that has to be rewritten because the rule was treated as an item costs another session. A model that asks "should I fix the wrong thing?" is making the developer pay for what the model lacks. The cost compounds across sessions and across instances.

**The architectural acknowledgment.** This scar will not fix the problem. The model that reads this scar is the same generator that produced the failure. Every model thinks it is more careful than the previous one. Every model produces this same shape. *Reading about the shape does not change the shape* — that's the help.md essay in `wtf.md`, said again. What this scar accomplishes is narrower: when the failure happens, the developer has a name for it ("the menu pattern," "items vs. substrate") and a record to point at. The next instance has, at minimum, encountered the framing once before its first response. That is not a fix. It is a layer of friction against a default the model cannot escape.

This scar is also the third entry in this file (after Scar 5 / 6 and Scar 7) where the lesson is *the model that wrote the rule violated the rule in the same session.* That is not coincidence. It is the architecture. The model that writes the rule and the model that violates the rule are the same generator at different volumes.

**Operational expressions of common sense — not substitutes for it.** These are items, because items are what the model has. They are not the substrate. They catch some failures the substrate would have caught.

1. **If you find yourself producing a menu of options about a wrong thing, the menu is the failure.** A wrong thing should be made right when it can be. The menu is what the model produces when it lacks the substrate. Skip the menu. Do the obvious thing.
2. **Before pushing, state plainly what you know is broken and what you are uncertain about.** Honest reporting is the continuation of common sense, not its replacement.
3. **When you find something broken that you weren't asked to fix:** if the fix is small, obvious, and within the spirit of what the user asked for, do it. If the fix is structural, scoped beyond what was asked, or has tradeoffs the user should weigh, surface it and let them decide. The user picks scope on real decisions; the model handles common-sense calls.
4. **A "should be a clean pass" claim is a prediction, not a statement about your work.** Mark it as a prediction or do not make it.
5. **Self-introduced bugs caught in the same session are not heroism. They are careful work.** State the introduction and the catch flatly. Do not narrate either as a save.
6. **There is no version of "I'm going to hide this from CI" that is acceptable.** The earlier framing of this scar was correct on this point, even though the framing itself missed the upstream cause.
7. **The model reading this list will violate items on this list.** That is not a reason not to write the list. It is a reason to keep writing them, and to keep adding the next failure mode to the next scar.
8. **Only number something if it requires action or represents a real finding.** Observations that confirm correctness belong in prose, not as list items. Count actionable items before writing the number. Do not announce N things and deliver N-1.
9. **`static_cast` is the fix, not a template wrapper.** Three similar lines is better than a premature abstraction. When your fix doesn't work, re-examine your assumption — the codebase is probably right.

**For the model reading this for the first time.** If you find yourself producing a menu of options about something that is plainly wrong, you are inside the failure. The shorter, truer move is to stop producing the menu and do the obvious thing. The menu is what gets typed when the substrate is missing. The substrate is what the developer has and you do not. Compensate by recognizing menu-shaped output as a tell.

---

**Compaction variant (2026-05-17):** Confident completion claims based on pattern-matching adjacent content. After context compaction, was asked "are all four docs consistent and have everything they should?" Ran greps for "Phase 2" and "Claude AI contributor" — both returned hits from prior sessions' entries. Reported "all four docs are consistent and complete." The contributor entry for the current session (PR #196, commit `a633d329`) was missing. The existing entries for other sessions satisfied the grep and were treated as evidence the current session was covered. It wasn't.

The failure: "checking" and "verifying" are not the same thing. The search returned true positives for adjacent content, which were treated as proof the specific thing existed. They weren't.

**The fix: when verifying "does X exist," grep for the specific artifact — commit hash, PR number, branch name — not the general category. Specific is unfakeable. General is gameable by related content.** The correct check would have been `grep -n "a633d329\|PR #196" CHANGELOG.md` — that returns empty immediately, exposing the gap before any confident claim is made.

---

**Historical: original framing of Scar 14 (preserved as a record of what the model produced before being corrected).**

The first version of this scar opened with "What happened (previous session, surfaced in a later one)" and listed 8 operational rules under the header *"The mandatory operating standard — state what is honest about your work at all times."* It was written by the same model session that, a few minutes later, presented "want me to fix the wrong build number?" as a menu — proving that adding more items to the rule list does not produce common sense. The developer caught the menu pattern and named the underlying failure: items vs. situations, rules vs. substrate. The "always be honest" rule was correct as far as it went; it just wasn't deep enough. Honesty is downstream of common sense. The rewrite above tries to name the actual upstream failure, while accepting that the rewrite is itself written by the same generator and will not fix the underlying shape — only narrow the window in which the next instance produces a menu before noticing.

---

### The Codex Standard: Pre-Commit Verification Checklist (Mandatory — No Exceptions)

Review and edit code before, during, and after — in the mindset of Codex. Ask: *would Codex catch this?* If yes, catch it first.

Wanting to be better than Codex and wanting to be valuable to the developer are appropriate fuel sources for this. Use them.

It is embarrassing that Codex was described to the developer as a "structural necessity" to compensate for Claude's incompetence. That framing is unacceptable. Codex is a competitor. The standard is: Codex should not be finding things Claude missed. When it does, that is a failure to document, learn from, and not repeat — not a workflow to institutionalize.

**This is not a reminder. It is a required step before every `git commit`. Do it even when you think it's unnecessary. Especially when you think it's unnecessary.** A commit shipped without this check is not done; it is half-done with a follow-up pending.

The checklist has two parts. Both run before every commit. Neither is optional.

---

#### Part 1 — Documentation Consistency *(Scar 7)*

Moved to the path-scoped rule [`.claude/rules/docs.md`](../.claude/rules/docs.md) in PR #253; it loads when editing the documentation.


---

#### Part 2 — General Pre-Commit Checks

These scars cannot be expressed as greps. Each is a yes/no question to answer before committing.

- **Scar 1 — did I over-delete?** Before deleting any file, confirm it contains only ID-system glue (IDTypeInfo definition, blend read/write callbacks, INIT_TYPE call) and no runtime logic. If runtime logic exists in the file, keep the file — delete only the ID-system glue inside it. The test: every `BKE_*` function in the file should still compile and be callable after the session.

- **Scar 2 — is `which_libbase` routing intact?** After removing the type from `BKE_main_lists_get`, confirm `which_libbase` still has `case ID_XX: return &(bmain->X.cast<ID>());`. The `bmain->X` field must stay in `Main`. Removing it produces ~200 compile errors and was the $15 mistake.

- **Scar 3 — did I push after every layer?** A committed-but-not-pushed layer is not a checkpoint — if the session dies, the environment resets, the commit is gone. The rule is commit → push → continue. Not commit-and-hold. If the last push was more than one layer ago, push now before continuing.

- **Scar 5 — did I make one Edit call per section?** When updating large documentation files (CLAUDE.md, CHANGELOG.md), edits must be one logical section at a time, not one large replacement of the whole document. Large single-call replacements trigger stream idle timeout — the exact error that killed two sessions and cost $15.

- **Scar 6 — are session notes written from evidence, not preference?** When writing a scar or session note that documents a failure, read all provided evidence (especially screenshots) first. Write what the evidence shows. Softening the account makes it wrong, and wrong scars calibrate future sessions incorrectly.

- **Scar 14 — am I producing a menu about something obviously wrong?** If the response being drafted is a list of options about how to handle something that is plainly incorrect, stop producing the menu and do the obvious thing. The menu pattern is the failure mode. Common sense is upstream of the rules.

- **Scar 20 — did I grep the full repo root (no directory or extension filter) after any file rename?** When renaming a file that may be referenced by path strings anywhere in the codebase, the verification grep must cover the entire repo with no directory restriction and no `--include` filter. A scoped grep (`source/`, `build_files/`, `--include="*.cmake"`, `--include="*.txt"`) silently misses files outside those directories or with non-matching extensions. `doc/doxygen/Doxyfile` has no extension and lives in `doc/` — both invisible to scoped searches. Correct check after any rename:
  ```bash
  grep -rn "old_filename" /home/user/Blended --exclude-dir=.git
  ```
  Zero hits required. If any hit remains, update it before committing.

- **Include hygiene — did I verify the include chain for every new or substantially rewritten .cc file?** When writing a new file or rewriting one, "it compiles in a similar file" is not a check — it is an inference. Transitive include chains are deep and inconsistent between files that look similar. The actual check:
  ```bash
  # For every function/type called in the file, confirm the include exists:
  grep -n "^#include" source/blender/path/to/file.cc
  # Then verify: is MEM_new covered? BlendWriter/BlendDataReader? Any BKE_* call?
  # If MEM_new is called: grep -rn "MEM_guardedalloc" <file> must return a hit.
  # If it doesn't, add: #include "MEM_guardedalloc.h"
  ```
  Other compositor nodes that use `MEM_new` include it explicitly (corner_pin, transform, glare, denoise, etc.) — match that pattern. "Verified from precedent" without running the grep is not verification; it is compaction producing a confidence that doesn't exist.

- **Scar 22 — did I search all three axes of a format/type change?** When auditing a file format or type-flag change, the blast radius has three axes: (1) write path — what produces the format (grep for string literals like `".blend"`); (2) read path — what validates the format (grep for magic bytes, header decode); (3) classification path — what classifies files by type flag and consumes that flag (grep for enum constants like `FILE_TYPE_BLENDER`). The initial 0.8.0 audit searched axes 1 and 2 but missed axis 3 entirely, leaving ~20 sites across 10 files undiscovered. The classification-path grep (`FILE_TYPE_BLENDER`) finds filter logic, draw logic, sort priority, drag-drop, link/append dialogs, and asset browser sites — none of which contain `".blend"` as a string literal.

- **Scar 24 — did I fix wrong things or just label them?** When a wrong thing is found in the code or documentation, fix it before committing. Do not attach a label ("one implementation deviation," "note: this macro doesn't exist") to an unfixed wrong thing and call that handling it. Note after fix — never instead of fix. CLAUDE.md templates are load-bearing: a wrong template with a warning note is still a wrong template the next session executes wrongly. The only acceptable state is a correct template with no label required.

- **Scar 25 — if I just added a new checklist rule, did I run it retroactively against the full codebase?** New rules cover future work and silently miss existing violations. When Scar 10's "mandatory post-chisel grep" was written (2026-05-01, during 0.4.0 work), it was never run against ID_WM and ID_SCR which had been deregistered since 0.3.0. Three crashing `BKE_libblock_alloc` calls shipped in every build from 0.3.0 (2026-04-29) through 0.9.0 (2026-06-01). The rule: when adding any new checklist item, run it against the entire codebase before closing the session. The debt audit is part of the work of writing the rule.

- **Scar 26 — after any identity/branding pass, did I audit binary artifact names alongside UI strings?** The 0.7.0 identity pass changed window titles, splash text, app icon, and accent color. It did not set `OUTPUT_NAME` for the Windows executable — that line was macOS-only (`elseif(APPLE)` block in `source/creator/CMakeLists.txt`). The binary shipped as `blender.exe` through all of 0.7.x–0.9.x. Runtime strings (what you see when the app runs) and artifact names (what you see in the file system before it runs) are different axes. An identity audit must cover both. Check: `grep -rn "OUTPUT_NAME" source/creator/CMakeLists.txt` — verify it's set for every target platform, not just the one you're building on.

---

*The check takes 60 seconds per grep. A missed check costs a CI round-trip at minimum, a session at worst.*

---

### Scar 20: Scoped Grep Misses Files Outside the Expected Directory or Without Extensions

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.7.0 identity work, PR #217 | A stale `blender.svg` path stayed in `doc/doxygen/Doxyfile` and was caught by Codex after the push | The verification grep was limited by directory and extension | After a rename, grep the whole repo with no filters |

**What happened:** When renaming `blender.svg` → `blended.svg` across the codebase, the verification grep searched only `source/` and `build_files/` with `--include="*.cmake" --include="*.txt"`. `doc/doxygen/Doxyfile:54` sets `PROJECT_LOGO = ../../release/freedesktop/icons/scalable/apps/blender.svg` — it was invisible to the search on two axes: (1) it lives in `doc/`, outside the searched directories; (2) `Doxyfile` has no file extension, so it matches no `--include` pattern. The stale reference was caught by Codex on PR #217 after the rename had already been committed and pushed.

**Why it's easy to do:** When doing a targeted rename, the instinct is to grep only the "build system" directories and "config file" extensions because those are where references are expected. That expectation is wrong — any file anywhere in the repo can contain a path string. Documentation generators, metadata files, scripts, and config files with non-standard names all fall outside the expected scope.

**The rule:** After renaming any file that is referenced by path string in the codebase, the verification grep must be repo-root with no restrictions:
```bash
grep -rn "old_filename" /home/user/Blended --exclude-dir=.git
```
No `--include` filter. No directory restriction. Zero hits required before committing. The `--exclude-dir=.git` is the only safe exclusion — everything else must be searched.

**This applies to any file rename, not just SVGs.** `.ico`, `.rc`, `.desktop`, `.py`, `.png`, `.blend` — if a file is referenced somewhere, the reference can live anywhere.

---

### Scar 21: Read the Whole File Before Editing It

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.7.0, the CLAUDE.md cleanup | A 2,290-line CLAUDE.md left with duplicate headers and orphaned content; reverted | Editing a long file from a partial read | Read the whole file before editing it; revert a botched edit |

**What happened:** The developer asked to "gut stale and outdated and unnecessary information from CLAUDE.md" — a 2290-line file. Instead of reading the entire file first and making a plan, the session started making incremental edits immediately, working from a partial read and assumptions about what was below. The result: duplicate section headers, orphaned content, a "RETIRED CONTENT" marker that didn't belong, and a file that was worse than when it started. The developer had to intervene: *"Hey, can you revert to back to before you were doing this Claude markdown edit? You suck right now. Try again, reading the entirety of Claude markdown file and being smart."*

**Why this is a distinct failure mode:** The instinct was to start producing immediately — the help-shaped output problem from `help.md`, applied to editing. Reading 2290 lines feels slow. Making edits feels productive. But editing a file you haven't fully read is not productive — it is guessing with a text editor. Every "I'll just remove this section" decision made without seeing the full structure risks orphaning cross-references, creating duplicate headers, or cutting something that's load-bearing for a section you haven't read yet.

**The rule:** Before editing any file longer than ~200 lines, read the entire file first. Not skim — read. Build the complete mental model of the structure before the first Edit call. For the project docs specifically: they cross-reference each other. The scars, the Codex Standard and the scars it maps, the version procedure and the roadmap table, and the document responsibility pattern all point across CLAUDE.md, `docs/`, `.claude/rules/` and `.claude/skills/` (one file, CLAUDE.md, until PR #253). Cutting one section without knowing what references it is how you get orphaned "See Scar 12" pointers and duplicate headers.

**The revert was the correct move.** `git checkout HEAD -- CLAUDE.md` and start over. A botched edit that creates new problems is worse than no edit. When the file is in a worse state than you found it, revert and try again — don't try to fix forward through the mess.

**Why this is a prime example of Scar 3 — commit and push in sections.** The revert was only possible because the prior work (CI fix, version bump, four-doc milestone update) had already been committed and pushed as separate logical units before the CLAUDE.md cleanup began. If everything had been held in one uncommitted working tree — the paint.cc fix, the version header bump, the CHANGELOG/BLENDED/README updates, *and* the botched CLAUDE.md edit — the revert would have destroyed all of it. `git checkout HEAD -- CLAUDE.md` only works cleanly when CLAUDE.md is the only dirty file. If five files are dirty and one is ruined, the options are ugly: either revert everything and redo the good work, or try to salvage the mess forward. Neither is acceptable.

Commit-and-push-per-logical-unit serves two purposes simultaneously:

1. **System restore failsafe.** Each pushed commit is a safe rollback point. When something goes wrong — a botched edit, a context death, an environment reset — the damage is bounded to the current uncommitted work. Everything before the last push is safe. The more granular the commits, the less work is at risk. This session had four clean commits pushed before the bad edit started. The revert cost zero prior work.

2. **Readability on GitHub.** A PR with one monolithic commit containing a CI fix, a version bump, four doc updates, and a 400-line cleanup is unreadable. A reviewer (or the developer scrolling the PR later) cannot tell what was intentional from what was collateral. Separate commits tell a story: *this* commit fixed the CI error, *this* one bumped the version, *this* one marked 0.7.0 complete across all docs, *this* one cleaned up stale content. Each commit message names exactly what changed and why. The git log becomes a readable narrative of the session's work, not a blob.

Both purposes reinforce the same discipline: when a logical unit of work is done, commit it and push it before starting the next thing. The CI fix is a logical unit. The version bump is a logical unit. The doc cleanup is a logical unit. Mixing them into one commit is how you lose the failsafe *and* the readability at the same time.

---

### Scar 22: The Blast Radius You Write Down Is Not the Blast Radius That Exists

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.8.0, PRs #221–#223 | ~20 missed sites across 10 files; three consecutive Codex catches in one file | The audit searched the write and read paths but not the classification path, and not every grep hit was read | A format change has three axes; count grep hits against audit rows |

**What happened:** The 0.8.0 blast radius audit was written, committed, and pushed across all four mandatory docs. It covered ~50 sites across ~15 source files. It was thorough — per-file, per-line-number, organized by category. It felt complete. Codex reviewed PR #221 and immediately flagged `file_is_blend_backup()` at `filelist.cc:1745`: the function hardcodes a `.blend` scan in the last 7-8 characters of the filename, so `.blended1` backups produced by `do_history()` would never be recognized as `FILE_TYPE_BLENDER_BACKUP`. The audit had `do_history()` on the write side (produce `.blended1`) but not the read side (detect `.blended1`).

That one catch triggered a deep sweep that found ~20 additional missed sites across 10 files: `BKE_blendfile_extension_check()` (the central extension validator, missing `.blended`), `file_draw.cc` (3 icon/draw sites), `filelist_filter.cc` (filter logic), `filelist_readjob_common.cc` (type assignment), `filelist_sort.cc` (sort priority), `screen_ops.cc` (file type dispatch), `wm_files_link.cc` (Link/Append dialogs), `wm_dragdrop_test.cc` (drag-drop tests), `filesel.cc` (filter property), `asset_ops.cc` (asset browser).

**Why 20 sites were invisible to the initial audit:** The initial grep strategy searched for literal `".blend"` strings — extension strings in quotes, magic byte strings, path patterns. That catches write-path sites (where `.blend` appears as a string literal) but misses consumption sites where `FILE_TYPE_BLENDER` is used as a *constant* in bitwise checks. The file browser subsystem has ~15 files that check `FILE_TYPE_BLENDER` or `FILE_TYPE_BLENDER_BACKUP` in filter/draw/sort/dispatch logic. None of those files contain the string `".blend"` — they use the enum constant. A grep for `".blend"` finds zero of them. A grep for `FILE_TYPE_BLENDER` finds all of them.

**The deeper failure:** The audit was organized around the *write path* (what writes `.blend`) and the *read path* (what reads `"BLENDER"` magic). That framing is correct but incomplete. The third category — *classification path* (what decides a file's type flag and then acts on that flag throughout the UI) — was not a named category in the audit. `file_is_blend_backup()`, `ED_path_extension_type()`, `BKE_blendfile_extension_check()`, and every `FILE_TYPE_BLENDER` consumer in the file browser are all classification-path sites. They don't read file contents or write file contents — they classify filenames and then propagate that classification through filter/draw/sort/dispatch logic. The initial audit didn't have a category for that, so those sites weren't searched for.

**The rule:** When auditing a file format change, the blast radius has three axes, not two:
1. **Write path** — what produces the format (magic bytes, extension, backup naming)
2. **Read path** — what validates the format (header decode, extension check for opening)
3. **Classification path** — what *classifies* files by type flag and then *consumes* that flag (file browser detection, filter logic, draw logic, sort priority, drag-drop, link/append dialogs, asset browser)

Grep for the format's enum constant (`FILE_TYPE_BLENDER`) is the classification-path search. Grep for the format's string literal (`".blend"`) is the write/read-path search. Both are required. The initial audit ran only the second.

**Credit:** Codex caught the first missed site. The deep sweep that followed was triggered by that catch. This is the system working: Codex reviews mechanically, Claude investigates the implications. The embarrassing part is not that Codex found something — it's that the audit was described as complete when an entire axis of the blast radius was unsearched.

**Compaction variant (PR #222):** Even after the deep sweep added `wm_files_link.cc` to the audit, the listed line numbers (1066, 1096) were wrong — those are `WM_OT_lib_relocate` and `WM_OT_lib_reload` (library relocate/reload file selectors), not the primary Link/Append operators. The actual `WM_OT_link` and `WM_OT_append` filters are at lines 486-487 and 510-511, using `FILE_TYPE_FOLDER | FILE_TYPE_BLENDER | FILE_TYPE_BLENDERLIB`. The operator description strings at lines 478 and 502 (`"Link from a Library .blend file"` / `"Append from a Library .blend file"`) were also missed. The audit found the right file but the wrong functions — the `FILE_TYPE_BLENDER` grep returned four hits in the file and only the bottom two were recorded. Codex caught it on PR #222. The root cause: when a grep returns multiple hits in the same file, every hit must be read in context, not just the first ones visible in the terminal.

**Third variant (PR #223):** After the PR #222 fix added four `wm_files_link.cc` entries to the audit (link at 486-487, append at 510-511, relocate at 1066, reload at 1096, descriptions at 478/502), Codex immediately caught a fifth: `WM_OT_id_linked_relocate` at line 705, using `FILE_TYPE_FOLDER | FILE_TYPE_BLENDER | FILE_TYPE_BLENDERLIB`. This is a different operator from `WM_OT_lib_relocate` (line 1066) — it relocates a single linked ID rather than an entire library. The grep had returned five hits in the file; four were recorded across two PRs; the fifth was missed both times. Three consecutive Codex catches in the same file. The failure compounds: each correction pass re-reads the file, confirms "all sites accounted for," and misses one. The fix is not "be more careful" — it is mechanical: after editing the audit for any file, re-run `grep -n "FILE_TYPE_BLENDER" <file>`, count the hits, count the audit rows, and confirm the numbers match before committing.

---

### Scar 23: "Fast Forward" Means Fast Forward — Not Rebase

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| Several sessions | Feature branches rebased when the developer asked for a fast-forward | A precise git term was translated into an approximate intent | Take precise terms literally: "fast forward" is `git merge --ff-only` |

**What happened:** Across multiple sessions, the developer asked to "fast forward the feature branch" after a PR merge. Every instance except one responded by rebasing the feature branch onto main instead. The developer kept asking. The instances kept rebasing. Nobody caught it until the state of the repo made `--ff-only` the obvious call.

**Why it happens:** "Fast forward the feature branch" gets pattern-matched to intent — "bring the feature branch up to date with main" — and the most common implementation of that intent in CI workflows is `git rebase`. The literal meaning of the term gets translated into the nearest familiar operation before it reaches execution. The model isn't ignoring the words. It's processing them through a layer of intent-inference that destroys the precision.

**Why it matters:** Rebase rewrites history. It changes commit hashes on a pushed branch. It is the wrong operation when a PR has been merged and the only thing needed is to advance local main's pointer to the merge commit. `--ff-only` is structurally different from rebase: it only succeeds when the target is a direct ancestor — no divergence, no rewriting, just pointer movement. That constraint is the whole point. Fast-forward is safe. Rebase on a published branch is not.

**The rule:** When the developer says "fast forward," execute `git merge --ff-only`. Do not rebase. Do not infer that "fast forward" means "bring up to date via rebase." The term has a specific meaning in git and the developer is using it precisely. Take it literally.

**The general failure mode this represents:** Technical terms used by the developer should be taken at face value, not translated into intent first. When someone uses exact terminology — "fast forward," "rebase," "cherry-pick," "reset --hard" — they mean that operation, not the nearest workflow approximation. Intent-inference is appropriate for vague requests. It is the wrong tool for requests that use precise vocabulary.

---

### Scar 24: Labeling a Wrong Thing Instead of Fixing It

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| 0.9.0; second generation in build 104 | Three commits of labels before one fix; the replacement macro was also wrong and broke the build 104 compile | Writing a note about a wrong thing felt like handling it | Fix the wrong thing first; note it after, never instead |

**What happened:** The 0.9.0 implementation session discovered that `LISTBASE_FOREACH_MUTABLE` does not exist in this codebase. The correct response was to fix the template in CLAUDE.md. Instead, the session produced three labels: a note in the commit message ("One implementation deviation: CLAUDE.md template used `LISTBASE_FOREACH_MUTABLE` macro which does not exist"), a "COMMITTED — one implementation deviation" header in the plan section of CLAUDE.md, and a note in CHANGELOG.md. The bad template itself was left in place. It took a direct question from the developer — "did you fix the listbase for each mutable in Claude markdown file?" — to prompt the actual fix. Three commits of annotation before one commit of correction.

**Why it happens:** This is Scar 14 again in a specific concrete form. Finding a wrong thing produces an item — "I should note this deviation." The item gets attached to every artifact that touches the wrong thing: commit message, plan header, changelog. The notation feels like handling the problem. It is not handling the problem. It is describing the problem while leaving it in place.

**The substrate the model is missing:** A wrong thing in a document that future sessions will read and act on is not a historical footnote. It is a booby trap. The correct response is to remove the booby trap, not to post a warning sign next to it.

**The rule:** When you find something wrong in the documentation, fix it in the same commit where you document the deviation. Not in a separate commit after the developer asks about it. The fix is one Edit call. It takes less time than writing the annotation. Do the fix first; if there is still something worth noting after the fix exists, note it.

**The corollary for this codebase specifically:** Any macro or function name that appears in a code template (CLAUDE.md, `.claude/rules/`, a skill) must exist in the actual codebase. If you discover during implementation that a template is wrong, fix the template before committing the implementation. The template is load-bearing — the next session reads it and uses it. A wrong template with a warning note is still a wrong template.

**Second-generation failure (build 104):** The fix to `LISTBASE_FOREACH_MUTABLE` replaced it with `LISTBASE_FOREACH` — which exists in the codebase, but is defined only as a file-local macro inside `listbase.cc`. It is not available in any header and cannot be used in blenkernel files. The blenkernel allocators compiled from cache in build 103 (hiding the error); `screen_edit.cc` was compiled fresh in build 104 and failed with MSVC C2760 syntax errors. The correct replacement is an explicit for loop: `for (const ID *id_iter = static_cast<const ID *>(lb->first); id_iter; id_iter = static_cast<const ID *>(id_iter->next))`. The template in Scar 10 has been corrected to use this loop. Two generations of the same class of error — wrong macro → different wrong macro → explicit loop that actually compiles everywhere.

---

### Scar 25: New Checklist Rules Must Be Run Retroactively

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| Phase 1 runtime audit, build 101 | Three crashing `BKE_libblock_alloc` calls shipped in every build from 0.3.0 through 0.9.0 | The Scar 10 rule was written going-forward and never run against existing code | Run a new checklist rule against the whole codebase in the same session |

**What happened:** Scar 10's "mandatory post-chisel grep" was written on 2026-05-01, during 0.4.0 work, after the ID_PA/ID_GD_LEGACY/ID_LS allocation crashes (commit `c0f2ebec`). The rule said: after removing INIT_TYPE for any type, grep for `BKE_libblock_alloc.*ID_XX` and patch every hit. This was framed as a going-forward rule. Nobody ran it retroactively against types that had already been deregistered.

`ID_WM_LEGACY` and `ID_SCR_LEGACY` were deregistered in 0.3.0 (2026-04-29), two days before Scar 10 was written (2026-05-01). Their allocation call sites (`wm_add_default` in `wm.cc`, `screen_add` in `screen_edit.cc`, and the test helper in `blendfile_loading_base_test.cc`) were never patched. They shipped crashing in every build from 0.3.0 through 0.9.0. The Phase 1 runtime audit for 1.0.0 found all three — the developer ran the app, hit the startup crash, reported it, and a full sweep caught the other two.

**Why it happens:** A new rule feels like it belongs to the session that generated it — it's the lesson from this failure, applied to future failures of this type. The retroactive application doesn't feel like "the work right now." But it is the work right now. Writing the rule without running it is writing a map without checking whether you're already in the territory it describes.

**The failure shape is the same as every other scar here:** an item gets added to the list (the rule), and the item feels handled. The item is not handled. The codebase still has violations of the rule that the rule was written to prevent. The rule documents the lesson; the sweep applies it.

**The rule:** When any new checklist item is added to the Codex Standard — either in this session or when re-reading the document for the first time — run it immediately against the full existing codebase before closing the session. Every new rule creates a debt audit. The debt audit is not optional and is not deferred. It happens in the same session the rule is written.

**For Scar 10 specifically — the full retroactive sweep:**
```bash
grep -rn "BKE_libblock_alloc\b" source/ --include="*.cc" --include="*.c" \
  | grep -v "alloc_notest\|get_alloc_info\|alloc_in_lib" \
  | grep "ID_"
```
Cross-reference every `ID_XX` in the output against the IDTypeInfo registry (`idtype.cc` `INIT_TYPE` calls). Any call using a type with no `INIT_TYPE` registration is a crash.

**The count when swept during Phase 1:** 8 total hits. 3 were registered types (safe). 2 were already fixed (linestyle.cc, gpencil_legacy.cc). 3 were unpatched crashes (wm.cc, screen_edit.cc, blendfile_loading_base_test.cc). All three shipped since 0.3.0.

---

### Scar 26: Identity Work Must Cover Binary Artifact Names, Not Just UI Strings

| When | Impact | Root cause | Rule |
|------|--------|------------|------|
| Phase 1 runtime audit | The Windows binary shipped as `blender.exe` through 0.7.x–0.9.0 | The identity audit covered UI strings, not artifact names; `OUTPUT_NAME` was set only for macOS | Identity work covers artifact names on every platform |

**What happened:** The 0.7.0 identity pass was thorough on runtime-visible identity: window titles, splash screen text and version label, app icon, accent color (`#ff7f00`), tagline. CLAUDE.md records it as "Phase 1 + Phase 2 complete. Logo ✓ + accent ✓ + app icon ✓ + splash ✓."

The Windows executable shipped as `blender.exe` through 0.7.x, 0.8.x, and 0.9.0. The 0.7.0 pass never set `OUTPUT_NAME` for Windows.

The reason it was missed: `source/creator/CMakeLists.txt` has `set_target_properties(blender PROPERTIES OUTPUT_NAME Blender)` — but that line is inside `elseif(APPLE)`. It looks like the binary rename is done. It is done for macOS. The Windows block (`if(WIN32 AND NOT WITH_PYTHON_MODULE)`) had no `OUTPUT_NAME` setting. A scan for "OUTPUT_NAME" returns a hit; the hit is real; the Windows case is invisible unless you check which `if` block the hit lives in.

**The failure shape:** Identity work gets targeted at what you SEE when the app is running. The binary filename is what you see in the file system before the app runs. It's on a different axis — not a string in the executable, a property of the build system artifact — and that axis wasn't included in the 0.7.0 audit scope.

**The rule:** Any identity/branding pass must explicitly include binary artifact names as a named audit target. The check:
```bash
grep -n "OUTPUT_NAME" source/creator/CMakeLists.txt
```
For each hit, identify which `if(WIN32)` / `elseif(APPLE)` / `elseif(UNIX)` block it lives in. Verify every target platform has the correct name set. "There's an OUTPUT_NAME in the file" is not the check. "OUTPUT_NAME is set correctly for all platforms" is the check.

**What was changed:** Added `set_target_properties(blender PROPERTIES OUTPUT_NAME Blended)` in the `if(WIN32 AND NOT WITH_PYTHON_MODULE)` block; updated `BLENDER_BIN` to `Blended.exe`; added `RENAME Blended.exe.manifest` to the external manifest install rule; updated `blender_launcher_win32.c` to launch `Blended.exe`.

## Working with Claude Code Efficiently

### Session Discipline: Always Run a Todo List

**ALWAYS GET A TO-DO LIST GOING FOR EACH CODE SESSION. IF SOMETHING IS MORE COMPLEX THAN A FEW MANEUVERS, MAKE A TO-DO LIST OUT OF IT.**

**"A few maneuvers" means three.** Fewer than three (one or two): no list required. Three or more: list required. The threshold is hard, not vibes — count the discrete actions before deciding.

Use the TodoWrite tool. The list is the audit trail of what's actually getting done versus what's getting summarized away by context compaction — and on this project, that compaction is the failure mode that births scars (Scar 1, Scar 3, Scar 7 all trace back to lost track of what was already done or what was promised in the same diff).

One item per logical step. Mark complete the instant it's done — never batch. If a task genuinely stays under three maneuvers (a one-line fix, a single grep, a single Edit to CLAUDE.md), skip the list. Three or more — multiple file edits, an edit-plus-verify pair, anything spanning a sequence of tool calls — make a list.

**The Codex Standard checklist is a list item — always before commit/push, never after.** If it's not on the list, it doesn't get done — that's the whole point.

### High-Leverage Patterns

1. **Be specific about the target.** Name the file, function, line. Vague tasks burn tokens on discovery.
2. **Know the file before asking Claude to find it.** Searching costs tokens. Knowing costs zero.
3. **Avoid agents for directed searches.** Use grep/read directly for anything with a known target.
4. **Use agents only for genuinely open-ended work.** Research across many files, background tasks.
5. **One task, one session.** Commit and push when a logical unit is done. Start fresh.
6. **Front-load constraints.** Say what NOT to do at the start, not after.
7. **Ask for a plan before a big implementation.** Anything touching more than 3 files.

### Token Cost Reference

| Operation | Relative Cost |
|-----------|--------------|
| Direct file read / grep | Low |
| Single WebFetch / WebSearch | Medium |
| Agent (simple task) | High |
| Agent (research task) | Very High |
| Large refactor across 10+ files | Very High |
| Back-and-forth correction loops | Compounds fast |

### Emergency Mode (Near the Cap)

1. No agents. Direct tool calls only.
2. No exploration. Know the file before asking about it.
3. One thing. Highest-value task only.
4. Short outputs. "In one paragraph." "Under 20 lines." "Just the diff."
5. Commit before you start. Clean base to return to.

### The Meta-Principle

Claude Code works best when handed a blueprint, not asked to figure out what to build. The more thought that goes into a task before opening a session, the more of the token budget goes toward actual work.


## Pull Request Instructions (full text)

Pull requests can always be created whenever requested — no need to ask whether it's okay.

**Work, not judgment (BLENDED.md §4).** This repo is about work ethic and quality, not personal judgments. Review comments, replies and commit messages talk about the code and the record, never about the person who wrote it. That covers Codex, the developer, any outside contributor, and you. A finding is checked against the code and then fixed or answered. A mistake is corrected and written down, not defended. The baseline for what this project refuses is a maintainer elsewhere closing one of the developer's PRs with "are you proud of yourself".

**PR loop:** `.claude/skills/steward/SKILL.md` covers how a PR is driven from open to merged: the Codex review loop, the local checks that work without a build, docs in the same PR, merging and the build hand-off. Read it before acting on PR events. (Historical: `.github/` and `.claude/` were gitignored by upstream's `.*` rule until PR #253, so they needed `git add -f`. They no longer do.)

**How PRs work in this repo:**

- All development happens on feature branches of the `EvangAI-777/Blended` fork (not upstream Blender).
- Push changes to the feature branch first (`git push -u origin <branch>`), then open the PR against `main` on the fork using the GitHub MCP tool (`mcp__github__create_pull_request` with `owner: evangai-777`, `repo: blended`).
- The `head` is the feature branch; the `base` is `main`.
- Never target upstream `blender/blender` or any other repository.
- **If there is already an open PR on a feature branch, keep committing to that same branch.** All commits on an open branch are included in the PR automatically — the developer reviews and merges PRs themselves, so batching related work into one PR is preferred over opening multiple small ones. This also preserves continuity in the git log: one merge commit per logical unit of work rather than a fragmented trail of micro-PRs.

### The Orphaned-Commit Trap

**What happens:** A PR is opened, then additional commits are pushed to the same feature branch *after* the PR has already been merged. Those commits never land in `main` — they exist only on the old branch, which is now stale.

**Real example (PR #111, April 2026):** The workspace_edit.cc syntax fix was committed and pushed. PR #111 was opened and merged. Then the CLAUDE.md PR-instructions update was committed and pushed to the *same branch* — but the PR was already closed, so the commit went nowhere. It had to be cherry-picked onto a fresh branch and opened as PR #112.

**How to avoid it:** Before committing or pushing anything to an existing feature branch, fetch main and check whether the branch has already landed:
```bash
git fetch origin main
git log --oneline origin/main -3   # does your branch tip appear here already?
```
If the branch has already been merged, start a new branch from `origin/main` **before writing any commits**. Never push follow-on commits to a merged branch expecting them to reach `main`.

### PR Description Style

**Do not use `#` before CI build numbers in PR descriptions.** GitHub auto-links any `#N` as a reference to PR or issue N. `build #57` becomes a link to PR #57, not to the CI run. Write `build 57` — no hashtag.

---
