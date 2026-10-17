---
paths:
  - "source/**/*.{c,cc,cpp,h,hh}"
  - "tests/**/*.{cc,hh}"
---

# ID types: deregistered types, allocation and Main listbases

Loaded when working on C/C++ sources. Moved verbatim from Scar 10 in PR #253; the story behind it is in `docs/scars.md` (Scars 2, 10, 25).

## Deregistered ID types

These ID codes have no `IDTypeInfo`: `ID_SCR_LEGACY`, `ID_WM_LEGACY`, `ID_WS_LEGACY` (runtime UI), `ID_PA`, `ID_GD_LEGACY`, `ID_LS`, `ID_MB`, `ID_TE`, `ID_CU_LEGACY`, `ID_CF` (0.4.0 removals), `ID_LP`, `ID_PAL`, `ID_LT`, `ID_MSK`, `ID_VF`, `ID_BR` (0.5.0 fold-downs). The authority is `idtype.cc` (`INIT_TYPE`) against `DNA_ID_enums.h`; `tools/check_blended.py` derives the list the same way. Any generic ID API that goes through the type info fails for them: allocation (`BKE_libblock_alloc`, `BKE_id_new`, `BKE_id_new_nomain`), naming (`BKE_id_new_name_validate`, the namemap), copying (`BKE_id_copy`), freeing (`BKE_id_free` / `id_free`, except screens, which `id_free` routes to `id_free_runtime_screen`), relinking and remapping (`IDRemapper::add` asserts). Use a type-specific path instead, as `BKE_curve_new_nomain` / `BKE_curve_free_nomain` do.

**Keep the `Main` listbase (Scar 2).** Removing an ID type removes it from the registration machinery (`IDTypeInfo`, `INIT_TYPE`, the `INDEX_ID_*` enum, `BKE_main_lists_get`), not the `Main` field. `which_libbase` keeps its `case ID_XX:` so runtime code and the allocators below still find the listbase.

## Allocating a deregistered type

**The fix pattern:** Replace `BKE_libblock_alloc(bmain, ID_XX, name, 0)` with manual allocation in the add-new function itself:
```cpp
T *obj = MEM_new<T>("TypeName");
BKE_libblock_runtime_ensure(obj->id);
*(reinterpret_cast<short *>(obj->id.name)) = ID_XX;
obj->id.us = 1;
{
  ListBaseT<ID> *lb = which_libbase(bmain, ID_XX);  /* Scar 2 routing still intact */
  BKE_main_lock(bmain);
  BLI_addtail(lb, obj);
  BLI_strncpy_utf8(obj->id.name + 2, name, sizeof(obj->id.name) - 2);
  BLI_uniquename_cb(
      [&](const StringRef check_name) {
        for (const ID *id_iter = static_cast<const ID *>(lb->first); id_iter;
             id_iter = static_cast<const ID *>(id_iter->next)) {
          if (id_iter != &obj->id && id_iter->lib == obj->id.lib &&
              check_name == (id_iter->name + 2)) {
            return true;
          }
        }
        return false;
      },
      name, '.', obj->id.name + 2, sizeof(obj->id.name) - 2);
  id_sort_by_name(lb, &obj->id, nullptr);
  bmain->is_memfile_undo_written = false;
  BKE_main_unlock(bmain);
}
BKE_lib_libblock_session_uid_ensure(&obj->id);
```
Requires `BKE_lib_id.hh` (for `BKE_libblock_runtime_ensure`, `BKE_lib_libblock_session_uid_ensure`, `id_sort_by_name`), `BKE_main.hh` (for `which_libbase`, `BKE_main_lock/unlock`), `BLI_string_utf8.h` (for `BLI_strncpy_utf8`), and `BLI_string_utils.hh` (for `BLI_uniquename_cb`).

**Why not `BKE_id_new_name_validate`:** This function routes into `BKE_main_namemap_get_unique_name` → `namemap_get_name`, which indexes `maps[BKE_idtype_idcode_to_index(type)]`. For deregistered types, `BKE_idtype_idcode_to_index` returns -1, and `maps[-1]` is `0xFFFFFFFFFFFFFFF8` — reading garbage as a `Map<string>`, crashing in the string slot destructor. **Never call `BKE_id_new_name_validate` for a deregistered type.**

**Why `BLI_uniquename_cb` over `BLI_uniquename`:** `BLI_uniquename` has two gaps: (1) it doesn't call `id_sort_by_name` — the listbase is left unsorted; (2) it checks all IDs regardless of `id.lib` — a local "Foo" incorrectly gets renamed "Foo.001" if a linked library also has "Foo". `BKE_id_new_name_validate` scopes to `id.lib`; the lambda above preserves that behavior.

**Cannot restore INIT_TYPE as the fix:** `INDEX_ID_XX` was also removed from the `IDIndex` enum. `MainListsArray` is `std::array<ListBaseT<ID>*, INDEX_ID_MAX - 1>` — `BKE_main_free` dereferences every slot. An unset `lb[INDEX_ID_XX]` nullptr crashes there. Restoring `INDEX_ID_PA` would require also restoring `lb[INDEX_ID_PA]` in `BKE_main_lists_get`, which fully restores the type to the indexed system — undoing the chisel.


**Allocator decision tree:**
- Trivially constructible T (all POD fields, no in-class initializers): `MEM_new_zeroed<T>` (zero-init + no constructor)
- Non-trivial T (any in-class initializer, `DNA_DEFINE_CXX_METHODS`, std:: members): `MEM_new<T>` (runs constructor)
- Never `MEM_callocN` for C++ types with constructors

**Mandatory post-chisel greps (run after removing INIT_TYPE for any type):**

Grep 1 — catch `BKE_libblock_alloc` calls for the deregistered type:
```bash
grep -rn "BKE_libblock_alloc.*ID_XX" source/ --include="*.cc" --include="*.c"
```
Every hit is a potential crash. Each allocation function must be patched to the manual pattern above, or the caller must be removed entirely if the path is truly dead.

Grep 2 — catch `BKE_id_new_name_validate` calls in the same allocators:
```bash
grep -rn "BKE_id_new_name_validate" source/ --include="*.cc" --include="*.c"
```
Every hit in a deregistered-type allocator is a second-generation namemap crash. The Scar 10 template formerly showed `BKE_id_new_name_validate` as the correct fix — it is not. All calls in Scar 10 allocators must be replaced with the `BLI_strncpy_utf8` + `BLI_uniquename_cb` + `id_sort_by_name` pattern above.

**Retroactivity note (Scar 25):** When this rule was first written (2026-05-01, during 0.4.0 work), it was framed as going forward — run it after each future INIT_TYPE removal. It was not run retroactively against all previously deregistered types. `ID_WM_LEGACY` and `ID_SCR_LEGACY` were deregistered in 0.3.0; their `BKE_libblock_alloc` callers (`wm_add_default`, `screen_add`, test helper) shipped crashing in every build from 0.3.0 through 0.9.0. The Phase 1 audit found all three. **When this rule is first added (or re-read for the first time in a new session), run both full sweeps now:**
```bash
grep -rn "BKE_libblock_alloc\b" source/ --include="*.cc" --include="*.c" | grep -v "alloc_notest\|get_alloc_info\|alloc_in_lib" | grep "ID_"
grep -rn "BKE_id_new_name_validate" source/ --include="*.cc" --include="*.c"
```
Cross-reference every `ID_XX` in the first output against the `IDTypeInfo` registry. Any call using a deregistered type is a crash waiting to happen. For the second grep: any hit in a deregistered-type allocator (check against the registry) must be replaced with the correct pattern.

**Automated since 1.0.0-dev:** `tools/check_blended.py` runs the first sweep on every PR. It reads the deregistered types from `idtype.cc` and `DNA_ID_enums.h`, skips comments, and also covers `BKE_libblock_alloc_in_lib`, `BKE_id_new` and `BKE_id_new_nomain`. The grep above misses those three, and that gap hid the render-curve crash (`docs/runtime-audit.md`, "Found by `tools/check_blended.py`"). The `BKE_id_new_name_validate` sweep still has to be run by hand.
