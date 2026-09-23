# AGENTS.md

## Scope and mission

This file applies to the repository root and all descendant directories unless a closer `AGENTS.md` or `AGENTS.override.md` provides more specific instructions.

This repository is the authoritative working source for a **new, separately identified Hearts of Korea × The Road to 56 compatibility port**.

Project facts:

- The runtime host is **The Road to 56** (Workshop item `820260968`).
- `C:\hoi\hearts_of_korea` is a read-only HOK donor/provenance snapshot, not this repository and not a default runtime dependency. Its descriptor identifies revision item `3793992662`.
- Historical HOK Workshop item `2898629778` remains provenance only. Do not confuse it with the supplied donor revision.
- Vanilla HOI4 is the engine syntax/schema baseline; the exact target RT56 snapshot is the host-content baseline.
- Only this compatibility worktree is writable by default. Donor, Workshop, game-installation, user-data, log, save, and launcher sources are read-only unless the user explicitly authorizes a separately scoped action.
- The current production tree began as a near-complete donor copy and is not presumed compatible merely because its name or `supported_version` says so.

Primary objectives:

1. Rebase the intended HOK content onto the explicitly recorded target RT56 snapshot.
2. Preserve HOK identity, authorship, intended Korean content, stable IDs, balance, and gameplay behavior where they do not conflict with RT56.
3. Preserve RT56 world data, shared systems, non-Korean content, and host behavior except where an explicit, documented HOK integration decision requires a change.
4. Resolve confirmed exact-path, logical-ID, map, dependency, localisation, load-order, and runtime defects with auditable merges.
5. Keep restoration, compatibility glue, original bug fixes, refactors, rebalance, and new content as distinct workstreams.
6. Prepare and publish only a separately identified compatibility release when the user explicitly authorizes the concrete publication action.

The target is `current RT56 + audited HOK delta`, not `full HOK donor copy + RT56`. HOK-specific and RT56-specific changes to the same Korean subsystem require an explicit merge decision; neither side wins automatically. Do not silently turn a compatibility port into a redesign.

---

## 1. Obey the requested operating mode

Determine the task mode from the user's request before using tools or changing files.

### Review-only

When asked only for review, analysis, planning, comparison, or a verdict:

- Do not edit files or generate patches.
- Do not launch HOI4 or run tests, validators, formatters, or scripts unless requested.
- Do not change Git state, commit, push, publish, or upload.
- Report findings with evidence, file paths, and line numbers where available.

### Documentation-only

When explicitly asked to document or update documentation, edit only the requested documentation. Read relevant sources as needed, but do not change game code, assets, runtime configuration, or Git state; do not generate artwork, launch HOI4, or run gameplay validators/tests. Describe proposed behavior and previously observed results separately. Documentation of a future implementation does not authorize that implementation.

### Diagnostics-only

When diagnostics are authorized but behavior changes are forbidden:

- Preserve gameplay behavior.
- Add only the minimum bounded instrumentation needed to distinguish concrete hypotheses.
- Do not refactor surrounding systems.
- Do not convert a suspected failure directly into a speculative fix.
- Mark temporary diagnostics and state how they should be removed or disabled.

### Implementation

When implementation is explicitly authorized:

- For compatibility or bug repair, make the smallest patch that addresses the demonstrated cause.
- For explicitly requested continuation development, state the intended behavior change and keep it separate from restoration work.
- Keep unrelated cleanup, formatting, and unrequested balance changes out of the diff.
- Preserve IDs, namespaces, filenames, load order, attribution, and save behavior whenever possible; document deliberate migrations.
- Validate the modified subsystem and expand testing according to risk.

### Continuing authorized focus development

- Interpret follow-up requests together with the active task and the latest explicit scope. When implementation is already authorized, requests such as "하던 거 계속해줘" or "AGENTS.md, /docs 읽고 구현해줘" continue that work through specification, implementation, integration, appropriate validation, and recording. Do not repeatedly ask whether to stop at documentation when that choice has already been settled. A quoted plan or status question alone is not new implementation authorization.
- Explicit limits such as "문서화 작업만", "설명만", or "코드 수정하지 말고" take precedence. Follow the requested mode and do not silently resume implementation while answering a review or documentation request.
- Establish the current source, branch/commit, working-tree changes, implemented modules, and remaining validation from the latest records. Preserve existing work and resume the next unfinished task within scope; do not restart an old baseline merely because an earlier plan is quoted again.
- Follow [the second-wave working sequence](../hearts_of_korea/docs/HOK_KOREAN_SECOND_WAVE_PLAN.md#작업-순서와-요청-범위). Specify and complete coherent policy modules, usually around 3-5 focuses, including their needed ideas, decisions, localisation, artwork, layout, and AI integration. This is a delivery unit, not a quota or a reason to leave an explicitly requested larger scope unfinished. Candidate counts and the final tree-size target do not authorize applying draft content wholesale.
- Resolve routine design and integration details within the authorized scope. Ask only when missing information or a material unresolved choice prevents a sound decision, and continue independent work while waiting. Existing authorization remains valid within its stated scope.
- Record static checks, forced-effect diagnostics, actual UI observations, normal progression, and long-term/save/DLC/multiplayer validation separately. Finish the validation required for the scoped change; if an actual blocker prevents it, record the blocker and unverified cases without claiming completion. Commit, push, and publication remain separate actions requiring explicit authorization.

### Release preparation

When asked to prepare a release:

- Prepare only the package, descriptors, metadata, credits, changelog, dependency list, and validation record requested.
- Use a clean staging directory or explicit allowlist; exclude `.git`, `AGENTS.md`, editor state, logs, saves, crash dumps, caches, credentials, and private records unless deliberately shipped.
- Keep Workshop IDs `2898629778`, `3793992662`, and `820260968` as provenance/dependency identities only; remove stale donor upload identity from the compatibility package.
- Stop before any external upload unless that exact action is explicitly requested.

### Publication

Publishing a new compatibility item is an intended project outcome. When publication or an update is explicitly requested:

- First publication must create a **new** Workshop item.
- Never upload to, overwrite, impersonate, or reuse HOK item `2898629778`, donor revision item `3793992662`, or RT56 item `820260968`.
- Later updates may target only the recorded compatibility-item ID after verifying it.
- Credit the original HOK creator, donor-revision contributors, RT56 contributors, localisation contributors, and new port contributions separately.
- Do not call it “official” unless the user approves that wording and project records support it.
- Record the source state, RT56 snapshot, release version, dependency set, target HOI4 version, resulting compatibility-item ID, and external actions performed.

Never commit, amend, rebase, merge, reset, clean, push, tag, publish, or upload merely because implementation or preparation was requested. Each Git-changing or external action requires explicit authorization for that action.

---

## 2. Project baseline

Canonical roots:

| Alias | Path | Role |
|---|---|---|
| `<COMPAT_ROOT>` | `C:\hoi\hearts_of_korea_Road_to_56` | authoritative compatibility source and only default write target |
| `<HOK_DONOR>` | `C:\hoi\hearts_of_korea` | read-only HOK intent, assets, history, and provenance |
| `<RT56_SOURCE>` | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968` | read-only, Steam-managed host snapshot |
| `<VANILLA_SOURCE>` | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV` | read-only engine syntax/schema reference |
| `<HOI4_LOGS>` | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV\logs` | read-only runtime evidence |

Identity baseline:

- Historical HOK Workshop item: `2898629778` (provenance only).
- Supplied HOK donor revision: `3793992662`, declared for HOI4 `1.19.*` and dependent on `Korean Language`; do not describe it as an untouched copy of the historical item.
- RT56 host: `820260968`, currently declaring `replace_path="history/states"` and `replace_path="map/strategicregions"`.
- Compatibility item: unassigned until first publication; never assume or copy any source ID.

Current confirmed baseline on 2026-09-06:

- Target run: HOI4 `1.19.2.0.a729`; the exact supported target must be re-recorded for later work.
- Observed RT56 Workshop manifest: `3323396725579032799`; treat it as a point-in-time value and recheck it before every implementation or validation batch.
- The compatibility root is Git repository `main@70aaba43a98fd429378ec1a67d4398f16330e101`; the 1차 port implementation is an uncommitted working-tree change set based on that commit.
- Before implementation, 1,013 of 1,014 shared production/root files were byte-identical to the supplied HOK donor; only `descriptor.mod` differed. This is a historical pre-port snapshot, not the current tree.
- The pre-port tree had 73 same-relative-path files against RT56. All 73 and every donor production/root file are now explicitly classified in the generated 1,014-row ledger; this does not replace runtime collision testing.
- The repository `descriptor.mod` and external launcher `.mod` currently declare both `The Road to 56` and `Korean Language`; the repository descriptor has no `replace_path`, `remote_file_id`, or launcher-only `path`, while the external launcher descriptor points to this compatibility root.
- The 2026-09-06 19:20 target run used RT56 Korean Translation (`2769576030`) rather than the declared Korean Language (`2743487021`). The later 21:28 and 21:30 C0 runs loaded only RT56 and the compatibility port and still crashed, so a localisation layer is not required to reproduce this incident; the final release localisation contract nevertheless remains unresolved.
- HOK province IDs `13414-13447` were migrated to `13535-13568`. Conflicting HOK state IDs were migrated to `917-920` and `1144-1147` under ADR-0002. Treat the result as new-game-only until save migration is separately proven.
- The latest 2026-09-06 21:28 non-KOR and 21:30 KOR C0 runs load 13,569 provinces, execute history, and request a 1936 singleplayer launch, then crash with the same `C0000005` stack before paused-map entry. The earlier malformed province/state errors and Korean sound duplicate/load errors are absent; unpause, localisation UI, gameplay, save, AI, and multiplayer remain unproven.
- The invalid KOR history assignments to `bba_early_transport_plane` and `early_transport_plane` were removed without a replacement technology because pinned RT56 globally activates `transport_plane_equipment_1`. The five related log records are absent from the 21:28/21:30 runs but the crash persists, disproving those stale references as the direct cause; production access remains unproven.
- ADR-0004 now uses donor-identical HOK WAVs and basic-aircraft mesh/textures. `sound/r56_vo_Korean.asset` is the single merged voice registry, and HOK basic-aircraft mesh/entity definitions use collision-free `hok_rt56_` IDs consumed only by the HOK KOR graphic database. The 21:28/21:30 logs contain no Korean sound duplicate/load error, but actual sound/GFX behavior remains unproven.
- A confirmed map-generator defect skipped seven vanilla-identical HOK `naval_base_spawn` rows that RT56 had removed even though the restored HOK coastline needs them. `tools/build_rt56_map.py` now restores only those seven audited rows and asserts that the generated map introduces no coastal province without a port spawn beyond the pinned RT56 baseline. The defect-to-crash link is strongly supported by an identical 14-frame stack in older runs with explicit `map.cpp:1679` likely-crash port warnings, but remains unconfirmed until new GER and KOR cold runs pass.
- Deterministic build/audit scripts live under `tools/`. ADR-0004 is implemented in the Korean-asset builder, pruning policy, integration manifest, and aggregate validator. The 2026-09-06 follow-up static run passed all Korean asset/technology gates but ended at `15 PASS / 0 WARNING / 1 ERROR` because the concurrently restored Japan-democracy-themed `music/Minshu_ikki.ogg` is not registered by the donor's current song list and violates the existing Korea-only pruning rule. A KOR focus shares its name but does not play the song; preserve the possible user change until the intended asset ownership is confirmed. A clean future static result still will not be engine/runtime proof.

Additional project context recorded on 2026-09-22:

- The user identifies themself as the original HOK creator and has authorized bringing the updated HOK artwork and applicable image guidelines into this compatibility port. Treat that authorship and task authorization as established context; do not carry forward earlier assumptions that the creator is deceased or unavailable.
- This artwork update concerns the new 60-focus/29-national-spirit icon set and its HOK-specific sprite mappings, source records, and palette rules. It does not authorize copying the donor's entire runtime tree, changing gameplay, recoloring legacy artwork, or replacing RT56's shared image systems.
- The 2026-09-06 baseline above remains a historical record. The artwork update does not establish a new runtime result or supersede the requirement to fingerprint current sources before implementation and validation.

Additional instruction sync recorded on 2026-09-23:

- This documentation-only sync imports the donor's general workflow, focus reward/layout, artwork, decision-icon, contributor-note, and commit-message rules from `C:\hoi\hearts_of_korea\AGENTS.md` at donor commit `be5fb40dbd8de33e5adbf65e808bcb0e8c283560` (source SHA-256 `CF34F606EB0DAEC9CAC422C2E5002CADD9556573FD8FB7B2C8E928240B5736AC`). It does not import runtime content or authorize the pending focus/artwork port.
- Links beginning `../hearts_of_korea/docs/` refer to read-only donor specifications and evidence, not documents shipped in this repository. Donor counts, coordinates, and runtime results are source-specific history, not the compatibility tree's current state or validation. Resolve the latest source and the port's integration records before implementing them.
- The compatibility repository's identity, RT56 host-preservation rules, source pins, generated-file ownership, map-ID migrations, shared-host artwork exceptions, attribution, and publication boundaries remain in force. The donor's project identity, superseded baseline claims, and conflicting personal-history claims are not imported.

Treat the continuation mandate and the compatibility-port request as established project context. Do not require another original-author approval for work the user has already authorized; escalate only concrete contradictory evidence, a specific third-party restriction, or a required user decision.

Do not infer the current target version from memory or from `supported_version` alone. Before compatibility work, record when available:

- exact HOI4 version and build/checksum
- enabled DLC
- launcher playset
- required and optional mods in load order
- language/localisation setup
- operating system and actual HOI4 user-data directory
- repository branch, commit, and working-tree state
- exact HOK donor revision and file hashes used
- exact RT56 Workshop manifest/date and relevant file hashes

When the target version is unknown, perform non-destructive inventory work only and state that version-dependent conclusions remain unproven.

---

## 3. Evidence hierarchy

Use question-specific authority and this general order:

1. Observed engine behavior in a clean, recorded control or target playset.

2. Current runtime logs and crash data tied to that exact run.

3. The physical files and dependency order actually loaded by the launcher.

4. Exact target-version vanilla files for engine syntax, schema, scope, and lifecycle.

5. The fingerprinted target RT56 snapshot for host content, world data, shared systems, and RT56-owned definitions.

6. The fingerprinted HOK donor for HOK design intent, inherited identifiers, assets, and provenance.

7. Current HOI4/RT56 documentation, followed by historical examples, forum posts, or model memory.

Vanilla and RT56 have different authority: installed target-version vanilla is canonical for engine syntax/schema, while the exact RT56 snapshot is canonical for the host content the port must preserve. The HOK donor explains intended HOK deltas but is not proof that its implementation remains legal or compatible. Do not import syntax from EU4, CK3, Victoria 3, Stellaris, or another HOI4 era merely because it looks similar.

Classify conclusions:

- `CONFIRMED`: directly demonstrated by source, log, or reproduction.
- `STRONGLY_SUPPORTED`: multiple pieces of evidence agree, but runtime proof is incomplete.
- `UNPROVEN`: plausible hypothesis requiring more evidence.
- `DISPROVEN`: contradicted by observed evidence.

Never present an inference as a confirmed engine fact.

---

## 4. Required inspection before production edits

Before editing a production mod file:

1. Read the task and identify explicit prohibitions.

2. Locate all applicable agent instruction files.

3. Record the compatibility worktree's Git branch/commit/status, or explicitly record that it has no Git metadata.

4. Fingerprint the HOK donor revision and the exact RT56 Workshop snapshot before using comparisons.

5. Inspect the compatibility, HOK donor, RT56, localisation, and relevant launcher `.mod` descriptors.

6. Identify `supported_version`, dependencies, `replace_path`, `remote_file_id`, and launcher `path` entries.

7. Confirm which physical mod copies the launcher loads and distinguish recorded list order from proven effective precedence.

8. Confirm the HOK donor is disabled in the target compatibility playset.

9. Inventory same-relative-path collisions and same-logical-ID collisions across the compatibility root, RT56, donor, and relevant vanilla databases.

10. Classify every touched donor definition as `ADD`, `USE_RT56`, `THREE_WAY_MERGE`, `OVERRIDE`, `BINARY_MERGE`, or `ASSET_COPY`.

11. For an override or merge, record the RT56 base hash, donor source/hash, intended HOK delta, affected logical IDs, and expected behavior.

12. Preserve relevant baseline logs before a new launch overwrites them.

13. Reproduce the failure with the smallest valid playset when runtime access is authorized, including an RT56-only control when practical.

14. Find both the target-version vanilla schema counterpart and the target RT56 content counterpart when either exists.

15. Identify the earliest failure, not merely the largest cluster of cascading errors.

16. When the cause is unclear, form competing hypotheses and define the observation that distinguishes them.

17. Verify that the RT56 snapshot did not change during the comparison.

Do not edit the HOK donor, Steam Workshop directory, base-game installation, user-data, logs, saves, or launcher settings directly. Work only in the compatibility repository unless the user explicitly authorizes a separate bounded target.

---

## 5. Root-cause classification

Classify the failure before choosing a fix. Typical categories:

- parser or syntax error
- illegal trigger/effect for the current scope
- changed, removed, or renamed engine key
- missing referenced ID
- duplicate ID or silent override
- file load-order collision
- unsafe `replace_path`
- descriptor, dependency, language-mod, or DLC-gating error
- localisation encoding, header, key, or load-order error
- map, state, province, strategic-region, railway, supply, or adjacency error
- country history, OOB, equipment, technology, character, or bookmark error
- GFX, model, animation, sound, or interface path error
- AI weight, strategy, or evaluation error
- performance or event-spam loop
- save incompatibility
- original upstream bug unrelated to the HOI4 update

Many later errors may be cascades from one early load failure. Fix and retest the earliest proven cause before mass-editing downstream references.

---

## 6. Paradox Script rules

Treat Paradox Script as context-sensitive game logic, not generic configuration text.

### Language and evaluation model

Paradox Script is a family of directory- and context-specific declarative DSLs, not a single general-purpose language. Syntax that works in one database, block, or game version is not evidence that it is legal or equivalent in another. Before introducing, moving, or generating syntax, verify the target directory's root schema, loader and merge behavior, lifecycle, and a target-version vanilla example from the same context.

- Treat a script block as an ordered multi-map, not a JSON/YAML object or programming-language dictionary. Repeated keys can be meaningful, and effect order can change behavior. Do not sort, deduplicate, merge, or generically round-trip blocks unless that exact transformation is proven semantics-preserving for that file type.
- Do not import C, C++, or Java operators, statement syntax, or comment syntax. `=` is context-dependent; do not substitute `==`, `&&`, `||`, `!`, semicolons, `//`, or `/* ... */`. Use `#` comments and only syntax demonstrated for the target HOI4 version.
- In ordinary trigger contexts, sibling conditions form a declarative condition set. Do not rely on left-to-right evaluation or short-circuit behavior to make a later condition safe. In effect contexts, earlier commands can change the state or scope used by later commands, so preserve and test command order. A `limit` block remains trigger context even when nested inside an effect construct.
- Brace nesting alone does not prove a scope change. Identify the enclosing command's actual scope contract. Treat `any_*`, `all_*`, `every_*`, and `random_*` constructs as distinct engine operations rather than interchangeable loop forms.
- Treat scripted trigger/effect parameters as context-sensitive expansion, not statically typed function arguments. At every caller, verify required parameters, resulting tokens, entry scope, and the meaning of `ROOT`, `THIS`, `PREV`, and `FROM`.
- Distinguish runtime variables, flags, event targets, saved scopes, and scripted parameters. For state-bearing constructs, verify owning scope, lifetime, unset or default behavior, save persistence, and multiplayer implications. Do not assume lexical block scope or automatic initialization.
- Do not infer numeric semantics from notation alone. For modifiers, weights, costs, durations, and cadences, verify units, additive versus multiplicative behavior, defaults, clamps, and legal ranges against target-version evidence.

### Load and runtime model

Paradox Script has no Java/C++-style compile, type-check, and link barrier. A brace checker, parser, external schema, or linter proves only the conditions it actually checks and may not match the target game version.

- Validate separately that the intended physical file was discovered and loaded, the definition parsed and registered, the block evaluated in the intended runtime scope, and the observable game behavior occurred. A clean parser result or quiet log does not prove all four stages.
- Before splitting, renaming, or duplicating files, determine the target directory's actual accumulation, filename precedence, duplicate-ID, dependency-order, and `replace_path` behavior. Do not assume a later file inherits from or extends an earlier definition.
- Do not infer effective precedence from `dlc_load.json` array order alone. Confirm the actual physical source and observed result for the relevant definition.
- In the target playset, load RT56 and the compatibility port without the HOK donor. If a donor-dependent architecture is proposed later, treat it as an explicit architecture change and repeat the collision audit.
- Classify the relevant lifecycle: load-time definition, new-game or history initialization, repeated trigger/AI/UI evaluation, sequential effect execution, or localisation/UI rendering. Do not infer runtime execution order merely from file order.
- Before changing a high-frequency trigger, AI weight, decision visibility/availability block, scripted GUI, or `on_action`, identify its call cadence and worst-case scope count. Do not assume caching or short-circuit evaluation without target-version evidence.
- Treat console reload and hot reload as exploratory diagnostics only. Final validation must use a full process restart and a clean run appropriate to the changed subsystem.
- Treat changes to random-selection sites, weights, and ordering as behavior changes rather than harmless refactors. When multiplayer compatibility is claimed, validate synchronized runtime behavior and inspect out-of-sync evidence in addition to comparing checksums.

### Scope correctness

For every changed trigger or effect, determine:

- expected input scope
- scope produced by each iterator or scope switch
- meaning of `ROOT`, `THIS`, `PREV`, `FROM`, event targets, saved scopes, and variables at that location
- whether the trigger/effect is legal for that scope in the target version

Do not hide a scope error by deleting the condition, adding `always = yes`, changing the target arbitrarily, or wrapping the block in a broad existence check unless that exact change is proven to preserve intent.

### Stable IDs and namespaces

Preserve existing identifiers unless an explicit migration is required, including:

- country tags and cosmetic tags
- event namespaces and IDs
- focus, decision, mission, idea, character, technology, and equipment IDs
- scripted trigger/effect/localisation names
- OOB, template, ship, variant, modifier, flag, variable, and event-target names
- sprite/asset names
- state, province, strategic-region, and supply-network IDs
- localisation keys

Before adding a glue ID, discover and follow the existing project prefix; prefer a compatibility-specific prefix such as `hok_rt56_` only after confirming the namespace is unused. Do not rename inherited HOK IDs merely for aesthetics.

Duplicate definitions may silently override earlier content. Search the compatibility root, exact RT56 snapshot, HOK donor, relevant localisation dependency, and vanilla files before declaring an ID unique.

Preserve an inherited HOK ID only when it is not already used incompatibly by RT56. Current confirmed collisions include HOK province IDs `13414-13447` and HOK state IDs `1028-1031` and `1082-1085`. These numbers must not be preserved at the cost of changing the RT56 entities that already own them; any reassignment is a documented persistent-ID migration with a complete reference closure.

### Preserve behavior

Do not casually alter:

- `ai_will_do` factors and modifiers
- random-list weights
- focus prerequisites, bypasses, cancellation, mutual exclusion, or rewards
- event cadence, triggers, options, or follow-up chains
- decision visibility, availability, cost, duration, cooldown, cancel, or remove rules
- national spirit and dynamic modifier values
- equipment statistics
- state resources, factories, infrastructure, supply, ownership, cores, or claims
- starting OOB, research, politics, laws, stability, or war support
- shared scripted constants

Compatibility repair, refactoring, rebalance, and new port content are separate tasks. Intentional changes require explicit scope and documentation; a parser-clean file can still be a gameplay regression.

### Focus reward design for continuation content

- For authorized new focus development and reward strengthening, design strong, noticeable rewards that make the focus worth its time and branch commitment. Do not default to token bonuses merely because a focus takes 35 days. Follow [the Korean focus reward guidelines](../hearts_of_korea/docs/HOK_KOREAN_FOCUS_REWARD_GUIDELINES.md).
- Preserve existing benefits unless their change is explicitly scoped. Increasing a headline modifier must not silently remove research bonuses, experience, political power, decision unlocks, DLC alternatives, or other secondary effects.
- Treat user-specified reward numbers as final values unless explicitly described as additions. Distinguish flat daily political power, percentage modifiers, research bonus magnitude and uses, and permanent versus temporary benefits.
- Donor continuation examples include one industry research bonus of 150%, one electronics research bonus of 100%, factory construction speed of +15%, military factory output of +10%, and flat daily political power of +0.5 or +1.2. These are concrete design references, not a mandatory minimum or a bundle granted to every focus.
- Carry strengthened lower-tier benefits into the matching upper-tier national spirit, preserve its other benefits, and check every mutually exclusive path. Replacing a spirit must not accidentally weaken the selected policy or stack obsolete tiers.
- Evaluate decision costs and opportunity costs against the benefit actually available to the player. When factory costs are explicitly removed, also review availability gates, AI gates, and descriptions; do not extend that removal to unrelated decisions.
- Record branch timing, cumulative rewards, and validation limits. This preference applies within authorized continuation or rebalance work; it does not authorize blanket changes to existing focuses during restoration, compatibility repair, or documentation-only tasks.

### Editing discipline

- Files owned by a deterministic script under `tools/` must be changed through that script and regenerated; do not hand-edit a generated output into a state its `--check` mode cannot reproduce.
- Treat a pinned donor/RT56/vanilla hash mismatch as source drift requiring a new baseline and merge review, not as a reason to weaken or silently update the assertion.
- Run `python tools\validate_port.py` after implementation changes that touch runtime files, generators, pruning rules, the descriptor, or the integration manifest. Keep its static result distinct from HOI4 runtime proof.
- Do not apply broad search-and-replace without reviewing every affected context.
- Do not reformat an entire file for a local fix.
- Preserve comments explaining historical intent or engine quirks.
- Any modified production text-code file must include a nearby contributor note in the exact form `#YYYYMMDD_kpopmodder: <brief reason/intent>`. Put it immediately above or at the end of the changed statement or block, keep one note per coherent change, preserve earlier notes, and do not add it to binary, generated, byte-exact, or documentation files. Use valid comment syntax for the file; generated runtime output remains owned by its generator and must not be hand-edited to add a note.
- For paired localisation files, put the identical contributor note immediately after each locale header and preserve UTF-8 BOM.
- Except for the required contributor note above, add explanatory comments only for non-obvious compatibility constraints.
- Do not delete an unknown key merely to quiet `error.log`; determine whether it was renamed, moved, DLC-gated, or replaced.
- Preserve exact filename and path casing, including on Windows.
- Check braces, quotes, list structure, and block placement after edits.

---

## 7. File-specific critical rules

### Descriptors

For `descriptor.mod` and launcher `.mod` files:

- Changing `supported_version` is not a compatibility fix.
- The release architecture requires RT56 as the host dependency. The repository descriptor declares it, but the external launcher `.mod` does not yet match; do not call the package ready until descriptor, launcher playset, physical path, and documentation agree.
- The HOK donor is not a default runtime dependency and must not be enabled alongside the compatibility port in target tests.
- Treat `Korean Language` versus `The Road to 56 Korean Translation` as unresolved until the localisation contract is tested. Do not silently preserve, replace, or combine those dependencies.
- Audit every `replace_path`; it can unload broad vanilla databases and cause distant failures.
- Never add `replace_path` merely to hide duplicate or stale content.
- Do not copy RT56's `history/states` or `map/strategicregions` replace paths into this compatibility mod. Adding any broad replacement requires a demonstrated need, a complete shadowed-file inventory, and explicit approval.
- Treat HOK IDs `2898629778` and `3793992662` as provenance only, and RT56 ID `820260968` as dependency/provenance only. A compatibility release must never inherit or target any of them.
- Do not invent a compatibility `remote_file_id`; record it only after a first, explicitly authorized new publication assigns one.
- Do not change compatibility upload identity or Workshop metadata without an explicit release task.
- Keep launcher, repository, staging, and release descriptors logically consistent while respecting their different path fields.
- Record the RT56 Workshop manifest/date and relevant hashes because Steam can update the source in place.

### `common/`

- Check global ID uniqueness and overwrite behavior.
- Compare changed definitions with the target-version vanilla schema.
- Verify DLC-dependent types and modifiers.
- Trace scripted triggers/effects transitively, not only the immediate caller.
- Treat `on_actions` as high risk because small errors can cause global repeated execution or silently remove callbacks.

### Events, decisions, and focuses

- Preserve namespaces and IDs.
- Verify receiving scope and every scope transition.
- Verify focus prerequisites, bypass, cancel, mutual exclusion, rewards, and AI selection.
- Verify decision visibility separately from availability and completion/removal.
- Check recurring content for accidental daily firing or unbounded event chains.

#### Focus placement, x/y, and relative coordinates

Before adding or moving Korean focuses, read [the layout plan](../hearts_of_korea/docs/HOK_KOREAN_FOCUS_LAYOUT_PLAN.md), [the coordinate specification](../hearts_of_korea/docs/HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md), and [the compact-layout incident record](../hearts_of_korea/docs/incidents/2026-09-21-korean-focus-compact.md). These record the earlier distant parent/child placements, conditional movement mismatches, and the subsequent layout that became excessively wide. Use the current source and latest specification together; do not reuse historical coordinates as current positions.

- Use a small set of stable absolute anchors and `relative_position_id` with relative `x`, `y` for related focuses. A sector root may itself be relative to another anchor; do not require every sector root to be absolute or create dummy focuses solely as anchors. Follow the documented vanilla Japan structure without copying its IDs, coordinates, offsets, or political conditions.
- Declare a relative-position anchor before every focus that references it. An existing ID later in the same file is insufficient: the donor 2026-09-22 HOI4 1.19.3 baseline logged “Relative focus must be scripted before this” for two Korean focuses. Check declaration order in addition to existence and cycles; if changing anchors, recalculate relative values to preserve the intended base position. See [the second-wave record](../hearts_of_korea/docs/HOK_KOREAN_SECOND_WAVE_PLAN.md).
- Focus `x`, `y` values use the focus grid, not screen pixels. Without `relative_position_id`, they specify the base absolute position; with it, they specify displacement from the referenced focus. Resolve the entire anchor chain: `base_position(focus) = base_position(anchor) + (x, y)`. Keep this base position separate from conditional final display positions.
- When converting absolute coordinates to relative coordinates, calculate `relative_xy = desired_base_position - resolved_anchor_base_position`. Do not retain the old absolute numbers or mistake an anchor's own relative numbers for its resolved position. Record the anchor ID, source x/y, resolved base position, and relevant conditional offsets in the layout specification.
- Keep placement references separate from progression. `relative_position_id` does not replace `prerequisite` and need not identify a prerequisite. A focus with several prerequisites still uses one placement anchor; retain all prerequisite groups and their AND/OR structure. For placement-only work, preserve IDs, costs, rewards, mutual exclusions, bypass/cancel/start/visibility conditions, and AI behavior. Do not delete connections or hide branches to conceal layout defects.
- Verify that each anchor ID exists uniquely, no focus references itself, no reference cycle exists, and every chain reaches an absolute anchor. When moving an anchor, inspect every dependent focus, all affected prerequisite and mutual-exclusion connections, and adjacent sectors. Include states where the anchor is hidden or its mutually exclusive alternative was chosen.
- Place new modules near their actual parents within recognizable policy/ideology sectors. Avoid collecting new focuses on distant lower rows or inflating spacing across the whole tree. Account for all parents of a merge, Korean title plates, icon borders, mutual-exclusion marks, and space for connecting lines. Relative coordinates alone do not prevent overlaps or excessive width; compare the overall bounds and scrolling burden before and after the change.
- Trace each `offset` condition and which anchor handles movement. Do not automatically duplicate a parent's offset on its children or bulk-delete offsets. Compare final positions before and after the full conditions become true under both SHOW and HIDE; HIDE alone does not imply that a completion-dependent offset already applies. Check double movement, leftover compensation, and collisions with neighboring sectors. Distinguish hidden focuses from visible but unavailable focuses, which still occupy space.
- Follow [the donor political-route compaction plan](../hearts_of_korea/docs/HOK_KOREAN_POLITICAL_COMPACTION_PLAN.md) and [its implementation record](../hearts_of_korea/docs/incidents/2026-09-22-korean-political-compaction.md) as source intent. Identify the route-completion conditions and apply each movement once through its anchor chain. Preserve hiding rules, gameplay, internal parallel modules, and unrelated common-sector positions unless their change is in scope. Recalculate positions against the compatibility tree rather than importing historical offsets or donor runtime claims as port facts.
- Treat `continuous_focus_position` as a separate panel coordinate setting, not the ordinary focus grid. Check panel clearance, shortcut destinations, scroll limits, and access to the full branch after a layout change.
- Check the actual icon/title rectangles and the engine-rendered connections, not just duplicate center coordinates or a straight-line approximation. Prevent unrelated lines from obscuring focuses, minimize unnecessary line crossings, and retain legitimate shared branch/merge lines. Judge spacing at the recorded resolution and GUI scale; a previously successful grid gap is not a universal pixel or font guarantee.
- Update the compatibility repository's coordinate documentation and machine-readable layout specification for implemented changes, using [the donor layout specification](../hearts_of_korea/docs/data/HOK_KOREAN_SECOND_WAVE_COORDINATES.json) as a read-only reference. If the port has no corresponding specification yet, add it within the authorized layout implementation; do not update the donor file. Separate static reference/position checks from in-game visual validation. When runtime execution is authorized, inspect affected sectors and their neighbors in initial and post-choice SHOW/HIDE states, including hidden anchors, panels, and shortcuts. Record the states, resolution, GUI scale, and remaining limitations; initial-state screenshots do not prove every later state.

#### Avoid long serial policy branches in future expansions

- Apply the communist parallel-branch lesson to future fascist and non-aligned content, including constitutional monarchy, absolute monarchy, and Hwan Empire follow-ups. Do not append every new policy module to the previous module's final focus in one long column. Plan independent policy modules beside an appropriate shared entry point before implementation. Use roughly 3-5 focuses per coherent module as a design guide, not an engine limit or a quota; justify longer serial dependencies in the specification.
- Parallel policy modules within the selected political route should normally remain independently accessible and jointly completable. Preserve genuine internal prerequisites, national-spirit upgrade order, formation/territory gates, and existing political-route exclusions. Do not add mutual exclusions merely to create a fork, or replace a long vertical chain with the same dependency chain snaking sideways. Distinguish new-content design from changes to existing prerequisites; this documentation rule does not authorize changing existing progression or rewards outside the implementation scope.
- For every proposed fork, record its entry requirements, longest required chain, resolved width/height, earliest major rewards and decision unlocks, and total completion time. Check both module orders, shared category visibility versus individual decision unlocks, spirit replacement, shared project limits, and AI timing. A module must not silently require completion of its sibling unless that dependency is explicitly designed and documented.
- Follow [the future-branch layout rules](../hearts_of_korea/docs/HOK_KOREAN_FOCUS_LAYOUT_PLAN.md#46-후속-정치-확장의-긴-직렬-가지-방지) and [the second-wave policy groups](../hearts_of_korea/docs/HOK_KOREAN_SECOND_WAVE_PLAN.md). Keep each route compact without trading excessive depth for excessive width or distant merge lines. The [communist parallel layout](../hearts_of_korea/docs/incidents/2026-09-22-korean-communist-parallel.md) is a structural example, not fixed coordinates or proof of future in-game layout quality.

### History, OOB, characters, and bookmarks

- Preserve date blocks and supported start dates.
- Verify ownership, control, cores, claims, buildings, resources, and victory points.
- Verify character definition, recruitment, roles, traits, portraits, assignment, and retirement/death rules.
- Verify OOB references to templates, equipment, technologies, variants, leaders, states, and provinces.
- Do not solve a missing reference by deleting starting content unless removal is the intended design.

### AI

- Separate “the AI can parse/evaluate this” from “the AI behaves as intended.”
- Inspect the combination of focus weights, strategy plans, templates, equipment, research, diplomacy, and other competing priorities.
- Do not infer final behavior from one isolated factor.
- Avoid unbounded logging in high-frequency AI evaluation paths.

### GFX, interface, models, and sound

- Verify exact asset name, file path, extension, casing, frame count, texture format, and referenced entity.
- Do not mass-convert or recompress binary assets.
- Do not replace missing art with placeholders unless requested.
- Keep asset compatibility changes separate from gameplay changes unless evidence connects them.

#### HOK artwork copies, sprite ownership, and relative paths

- Newly imported or created HOK focus and national-spirit image payloads, together with any HOK-specific masks and overlays, must exist inside this compatibility repository's runtime asset directories. Copy only the selected assets required for the authorized task, preserving the read-only donor, Workshop, and game sources.
- Use mod-root-relative paths such as `gfx/interface/goals/HOK_KOR/example.dds` and `gfx/interface/ideas/HOK_KOR/example.dds` for `texturefile`, `animationmaskfile`, `animationtexturefile`, and equivalent references. Do not use absolute paths, external URLs, `..` escapes, or links to files outside the repository.
- New HOK focus `icon = GFX_...` and idea `picture = ...` references must resolve through HOK-specific sprite definitions to the local HOK image payload. Preserve the established `HOK_KOR_` naming convention, check same-path and logical-ID collisions against the pinned RT56 and relevant vanilla sources, and do not override a shared global sprite merely to redirect one HOK icon. Keep gameplay IDs and behavior unchanged in an artwork-only task.
- This local-copy requirement does not extend to all vanilla or RT56 shared UI assets. The existing `gfx/interface/goals/shine_overlay.dds` reference may continue to use the vanilla host fallback. Other existing shared focus-shine masks, animation textures, and host UI helpers may remain external when their provider is recorded and checked. Require a separate scoped review before localizing or replacing them. Do not claim the image chain is wholly self-contained while a shared host reference remains.
- Preserve format, dimensions, alpha, frame layout, and exact filename casing unless conversion is explicitly within scope. Record the donor/source revision and path, applicable reuse basis, original credits, input/output hashes, and any edits. User authorship of HOK does not erase existing third-party artwork credits or artwork-specific terms.
- Trace the complete content-to-sprite-to-image chain, including masks and overlays. Every HOK-owned payload must resolve locally with exact casing; every retained shared host reference must have a recorded provider. Apply the existing deterministic-generator, integration-classification, pruning, and pinned-source rules to imported assets and registries.

#### Create and integrate artwork with new HOK content

When an authorized implementation adds HOK focuses, national spirits, decisions, or other content that needs an image, include suitable artwork creation and integration in that implementation. The user permits both newly drawn/generated artwork (including AI image generation) and copying/adapting open-source or explicitly reusable public artwork; combining the two is also allowed. Choose the method per asset based on subject fit, visual consistency, readability, and effort. External-source research and the existing source-component composer are options, not mandatory prerequisites for new artwork. Save the final assets inside this project and connect them through project-owned GFX and relative paths. Routine drawing/generation, permitted source research/downloads, composition, and integration within authorized implementation do not require a separate artwork request. Review-only and documentation-only requests do not authorize image generation, downloads, asset edits, or game-code changes. Follow [the donor updated artwork policy](../hearts_of_korea/docs/HOK_KOREAN_FOCUS_SPIRIT_ICON_PLAN.md). Shared RT56 content and the documented shared-host artwork exceptions above remain under the compatibility preservation rules.

1. Identify the content's meaning, branch or policy field, central motif, linked focus/spirit relationship, and genuine upgrade stages before selecting artwork. Follow the background-color rules below. Avoid repeating one generic icon for unrelated policies merely because it already exists.
2. For new artwork, draw or generate the needed illustration directly. For reused artwork, search suitable open-source or explicitly reusable public image packs and creators' repositories; the documented Ultimate HOI4 GFX components are one available source, not a required first step. Existing downloaded materials may be reused when their recorded terms cover the use. Use a mixed approach when a new central illustration fits an existing reusable frame or background.
3. For every external image or component reused or adapted, verify that its actual licence or explicit permission covers the intended reuse, modification, and distribution. Public visibility or availability for download alone is not permission. A repository's code licence does not automatically cover its artwork; check artwork-specific terms and third-party exceptions. Keep permission limited to the identified pack/files; do not infer permission for an entire mod or invent a licence. If a candidate cannot be used, select a permitted alternative or create new artwork. Generating or redrawing from a third-party image does not erase that source or its restrictions.
4. Keep selected source files and final selected generated originals in a project-local working directory. Compose or refine them as needed, managing background, frame, central illustration, and stage marks separately where practical. Match the agreed colors, metal treatment, proportions, and small-size readability across directly generated and reused assets. The existing composer remains suitable for component work and background-only recoloring; the earlier choice of that method for the 60-focus/29-spirit recolor does not restrict future new artwork to external components. Preserve source attribution and distinguish new drawing/generation from selection, composition, recoloring, and added marks.
5. Export the finished image to the appropriate runtime directory inside the repository, using the dimensions, alpha, frame layout, and DDS format required by the target-version UI. Keep source downloads and temporary working files separate from runtime outputs. Add or update project-owned sprite mappings, including required local HOK image masks and overlays while retaining the documented shared-host exceptions above, and connect the content using the internal relative-path rules above. Do not leave HOK artwork delivery at unapproved external sprite references, unintegrated previews, or unrequested placeholders.
6. Record whether each asset is newly drawn/generated, reused, or mixed. For reused parts, retain the source URL/path, fixed revision when available, reuse evidence, contributors, and source hash. For AI-generated parts, record the generation tool, actual model if exposed, date, prompt, reference images if any, and selected original path/hash; label them as AI-generated rather than an open-source download or a named artist's work. For every method, record the content ID, subsequent edits, final project path, sprite reference, and output hash in the relevant documentation and asset manifest. Reuse [the current icon manifest](docs/data/HOK_KOREAN_FOCUS_ICON_MANIFEST.json) pattern where applicable; preserve historical attribution, record compatibility-port selection separately from donor provenance, and do not record proposed artwork as already integrated.
7. Inspect the finished artwork at actual display size, compare related focuses and spirits, and check background contrast, central motifs, stage readability, transparency, exact paths, file format, and sprite collisions. Validate in-game states when runtime execution is authorized and record untested states honestly. Keep gameplay logic, existing legacy artwork, and unrelated assets outside the image change unless the task explicitly includes them.

#### Decisions must use dedicated small artwork

When adding or replacing decision-row or decision-category header icons, create a separate small image for the decision UI. Follow the [decision icon size repair](../hearts_of_korea/docs/incidents/2026-09-22-korean-decision-icon-size.md) and [small-icon manifest](../hearts_of_korea/docs/data/HOK_KOREAN_SMALL_DECISION_ICON_MANIFEST.json).

- Do not point decision/category sprites directly at large focus or national-spirit textures, such as the 100×88 focus DDS. Do not assume the decision UI automatically scales them down. Keep the original focus and spirit images unchanged and export dedicated small DDS files.
- Use **32×32 for individual decision-row icons** and **51×40 for decision-category header icons** as the donor-derived baseline for new HOK decision artwork. These sizes fit the donor-inspected HOI4 1.19.3 UI; verify the target RT56 UI's row/header bounds, icon anchor, title position, and scaling before adopting these dimensions, choosing different dimensions, or adapting to a changed UI. Keep category description pictures and other UI artwork at their separately verified dimensions. Do not enlarge rows or replace the global decision GUI just to accommodate an oversized icon.
- Recompose the central motif for small-size readability. Preserve the linked content's branch/field colors, recognizable symbols, component aspect ratios, and alpha; simplify large wreaths and ribbons, and retain a visible metal border and transparent margins. Do not merely shrink a detailed focus icon until its subject becomes unreadable, or add I/II/III marks without actual upgrade stages.
- Store the finished assets under `gfx/interface/decisions/HOK_KOR/<module>/` and reference them through project-owned `GFX_HOK_KOR_decision_*` sprites with mod-root-relative paths. Preserve existing sprite names when replacing artwork; keep decision IDs, costs, rewards, durations, unlocks, and AI unchanged during image-only work.
- Record the source, reuse permission or generation method, composition changes, dimensions, sprite mapping, and final hash in the asset documentation. Check DDS format, alpha, exact paths, and actual-size previews against the header/row and nearby text. When runtime validation is authorized, check category, available/unavailable, and active decision displays after a full restart; distinguish static bounds checks from actual game-screen verification.

#### HOK focus and national-spirit background colors

Color represents the focus's political branch or policy field, not the country's current government. Shared industry and military artwork must not change color with the ruling ideology.

| Political branch or policy field | Background and ornament direction |
|---|---|
| Democracy | Muted deep blue |
| Communism | Deep red rather than vivid primary red |
| Fascism | Brown with black ornaments, or charcoal with bronze ornaments |
| Non-aligned | Light gray and silver rather than pure white |
| Industry and production | Neutral gray with bronze or gold ornaments |
| Education and research | Light gray and silver |
| Army, ordnance, logistics, and staff | Dark green and olive |
| Navy | Navy blue and slate blue-gray |
| Air force | Silver and pale blue |

- Apply political-branch color first for route-specific content. Democratic education, medical aid, volunteer support, and economic or armaments agreements remain blue. Foreign agreement participant spirits retain their originating branch's color regardless of the recipient's ideology; do not introduce gameplay conditions for artwork choices.
- For shared HOK content, use its policy field. Service-specific schools, research, and maintenance retain the service color. Resolve overlaps from the actual branch, policy, and linked spirit, not a recipe's `family` or `category` alone. The regional Gyeongsang shipbuilding-industry focus uses industry colors.
- Keep linked focuses and spirits in the same color family with a shared central motif. Preserve `I`, `II`, and `III` marks for genuine upgrade chains and intentional badge omissions; do not invent stages for unrelated content.
- Edit background layers separately, preserving central illustrations, metal borders, ornaments, stage marks, alpha, and recognizable symbols. Do not recolor the whole finished icon with a hue filter. Color must complement the motif and shape rather than act as the only identifier.
- Preserve dark outlines against the UI and metallic shading in light gray/silver backgrounds so icons do not resemble disabled content. Distinguish democracy from navy and education from air force through motifs and frames as well as color.
- Record exact palettes, per-ID assignments, sources, color processing, and output hashes in [the color plan](docs/HOK_KOREAN_FOCUS_ICON_COLOR_PLAN.md) and icon manifest. Inspect actual-size previews and report locked, available, active, completed, shine, and spirit-display runtime checks separately.
- The current applied scope is the new 60 focuses and 29 national-spirit definitions. Existing communist, fascist, non-aligned, and other legacy artwork is outside this update. Palette entries for those branches guide future explicitly scoped artwork; they do not authorize recoloring legacy HOK or RT56 content.

---

## 8. Localisation and encoding

HOI4 localisation files are not ordinary YAML. Do not run a generic YAML formatter on them.

- Preserve UTF-8 with BOM for localisation `.yml` files.
- Preserve each file's established language header while the localisation contract is investigated; do not assume the donor's Korean-language dependency remains the final port dependency.
- Do not invent or replace a locale header without confirming how the active dependency loads it.
- Preserve the expected key form, such as `KEY:0 "Text"`, unless the project has a verified alternative.
- Preserve `$KEY$` substitution, scripted tokens, colour codes, icon tokens, newline escapes, and quote escaping.
- Check duplicate keys and exact casing.
- Keep keys stable for translation and compatibility submods.
- Do not mass-normalize BOMs, encoding, line endings, whitespace, or Unicode.
- Verify Korean text in game, not only in an editor.

Missing text may be a reference or load-order failure rather than a missing string. Trace the caller, key, language header, loaded file, and dependency order.

The 2026-09-06 baseline has `Korean Language` installed but not active, while `The Road to 56 Korean Translation` is active and declares `replace_path="localisation"`. Before choosing a release dependency, test the HOK `l_english`/`l_korean` contract and whether that replacement hides compatibility localisation. Do not assume the two localisation mods are interchangeable.

---

## 9. Map and state work is high risk

Do not modify map-related files unless the task explicitly concerns the map or evidence proves a map definition is the root cause.

Map work includes province definitions/bitmaps, terrain and height data, states, strategic regions, supply nodes, railways, adjacencies, buildings, unit positions, victory points, and ownership.

Required rules:

- Use the fingerprinted current RT56 world map as the canonical integration base. Vanilla remains a schema reference, not the content base for an RT56-owned map.
- Extract the intended HOK Korean-map delta from the donor and, where possible, its historical base. Do not treat every donor-versus-RT56 difference as an HOK design requirement.
- Never ship the donor `definition.csv` or `provinces.bmp` unchanged. If the engine requires a monolithic file, synthesize it from the current RT56 file plus the reviewed HOK delta.
- Preserve every RT56 province, state, strategic region, RGB, and non-Korean geometry unless a specific integration decision says otherwise.
- Re-scan the complete current RT56 ID and RGB sets immediately before allocating anything. Do not hardcode “current maximum + 1” as future-safe across Workshop updates.
- Preserve globally unique province IDs and colours.
- Do not renumber an RT56 state or province for HOK convenience.
- Current HOK donor province IDs `13414-13447` are all semantically occupied by different RT56 provinces. Current HOK state IDs `1028-1031` and `1082-1085` are occupied by different RT56 states. Reusing those IDs unchanged is forbidden.
- Any HOK ID reassignment requires an explicit migration plan covering state and strategic-region membership, script references, history, OOB, localisation, save impact, and third-party compatibility.
- Because RT56 replaces `history/states` and `map/strategicregions`, rebase affected HOK states and regions from the current RT56 definitions, not vanilla or donor whole files.
- Verify province-to-state and province-to-strategic-region membership.
- Verify land/sea/lake/coastal classification and adjacency consistency.
- Verify supply, railway, naval-base, victory-point, building, unit-stack, and position references after topology changes.
- Do not infer `buildings.txt` solely from a donor-versus-vanilla two-way delta. Verify each required placement against the actual RT56 row set and the synthesized bitmap, and require that the compatibility map adds no coastal land province without a sampled `naval_base_spawn` relative to the pinned RT56 baseline.
- Compare global ID/RGB/reference sets against the pinned RT56 baseline so a Korea change cannot silently remove distant RT56 content.
- Nudger output may be written to the HOI4 user-data directory, not the repository. Do not run Nudger without authorization; inspect output and copy only intended files into the compatibility root.
- Never copy a whole vanilla, donor, or RT56 map folder or add broad `replace_path` as a bandage.
- Main-menu load is insufficient. When authorized, load a new game, select Korea, enter the map, unpause, inspect affected regions and supply, and compare logs with an RT56-only control.

---

## 10. Diagnostics and logs

The common Windows user-data location is:

`\<Documents>/Paradox Interactive/Hearts of Iron IV/`

The actual path may be redirected through OneDrive or a custom user directory. Resolve the directory used by the running game.

Relevant evidence may include:

- `logs/error.log`
- `logs/game.log`
- `logs/setup.log`
- `logs/system.log`
- exception and crash logs when present
- launcher logs when discovery or loading fails
- crash dumps
- reproduction-specific saves

Rules:

- Copy or rotate logs before a clean reproduction so stale output is not mistaken for current output.
- Compare against a vanilla or dependency-only control run when possible.
- Separate pre-existing vanilla/DLC/dependency warnings from mod-introduced failures.
- Inspect surrounding and preceding lines; the final message may be a cascade symptom.
- Use `-debug` only when runtime execution is authorized.
- Add script logging only to answer a stated diagnostic question.
- Prefix temporary messages consistently, for example `[HOK][FOCUS][scenario-id]`.
- Log stable identifiers and state transitions, not every daily evaluation.
- Rate-limit or cap repeated diagnostics.
- Remove or disable noisy temporary logging before release unless permanent observability is requested.

Never claim a root cause merely because deleting content made an error disappear.

---

## 11. Compatibility workflow

For each compatibility problem:

1. **Pin sources**: record the target HOI4 build, HOK donor revision, RT56 Workshop manifest/date/hashes, localisation source, and compatibility worktree state.

2. **Reproduce controls** when authorized: use RT56-only and the smallest target compatibility playset, each from a clean process start.

3. **Capture** the earliest relevant log evidence, visible behavior, physical loaded paths, and run-specific hashes.

4. **Locate** the affected definition and its full reference closure.

5. **Compare four ways**: compatibility output, HOK donor intent, exact RT56 host definition, and target vanilla schema/example.

6. **Classify the file/definition** as `ADD`, `USE_RT56`, `THREE_WAY_MERGE`, `OVERRIDE`, `BINARY_MERGE`, or `ASSET_COPY`.

7. **Classify the failure** and competing hypotheses, distinguishing stale whole-file shadowing from genuine HOK-specific changes.

8. **Patch** the smallest reviewed HOK delta onto the current RT56 base. Do not patch an old donor base and call it merged.

9. **Retest** the exact reproduction before broad smoke testing.

10. **Compare logs and behavior** with the matching RT56-only/localisation control, not merely with the prior crashing compatibility run.

11. **Review the diff** for lost RT56 content, accidental ID/balance/encoding changes, unexplained whole-file copies, and unrelated cleanup.

12. **Record provenance, uncertainty, and untested paths**, then verify the RT56 source fingerprint still matches the pinned baseline.

Do not jump from “old mod” to “rewrite with current syntax.” Old syntax may still be valid, and newer syntax may have different semantics.

---

## 12. Validation requirements

Use the smallest relevant subset first, then expand according to risk.

When runtime validation is authorized, distinguish these configurations:

- `V0`: vanilla control
- `R0`: RT56-only control
- `R1`: RT56 plus the selected localisation layer
- `C0`: RT56 plus the compatibility port
- `C1`: RT56 plus the selected localisation layer and compatibility port

Do not enable the HOK donor in `C0` or `C1`. Run only the smallest configurations needed for the scoped question, but do not claim RT56 compatibility without comparing against an RT56 control.

### Static checks

- no unintended additions or deletions
- valid braces, quotes, and block placement
- no newly introduced duplicate IDs
- no broken event/focus/decision/character/idea/equipment/technology/map/asset/localisation references
- descriptor and dependency consistency
- localisation BOM/header/key integrity
- no accidental whole-file encoding or line-ending conversion
- no unexplained same-path or logical-ID collision with the pinned RT56 snapshot
- every shipped file has an integration classification and provenance
- no unintended loss of RT56 world IDs, shared definitions, or assets

### Launcher and load checks

- launcher detects the intended local mod copy
- exact playset and load order are recorded
- the correct physical source is loaded
- the HOK donor is disabled in target compatibility configurations
- the RT56 snapshot matches the pinned fingerprint
- main menu loads without a new relevant fatal error
- declared `supported_version` is not confused with demonstrated compatibility

### New-game smoke checks

For every supported bookmark relevant to the change:

- Korea loads in the intended state
- leader, government, parties, laws, ideas, research, and resources load
- focus tree opens and key branches remain connected
- decisions and events appear under intended conditions
- starting OOB and equipment load
- custom states, ownership, cores, claims, supply, and victory points are correct
- portraits, icons, models, names, and localisation resolve
- unpausing does not immediately produce a crash, event spam, or severe error growth

### Targeted and regression checks

- demonstrate the pre-patch failure when possible
- demonstrate the intended post-patch behavior
- test a positive path and an important blocked/negative path
- inspect AI runtime behavior when AI logic changes
- inspect save/load when persistent IDs, flags, variables, history, or map data changes
- Distinguish a new-save round trip from backward compatibility. To claim existing-save compatibility, load a representative pre-change save in the patched build, advance the game, save again, and reload it. Any one-time migration must be version-gated and idempotent.
- check multiplayer checksum/synchronization only when multiplayer compatibility is claimed

Risk examples:

- focus: prerequisites, bypass, cancel, mutual exclusion, rewards, AI path
- event: trigger, scope, options, repeat firing, localisation, follow-up chain
- decision: visibility, availability, cost, duration, cancel/remove, target scope
- character: recruitment, role, portrait, traits, advisor/leader assignment
- map/state: load, unpause, supply, railway, adjacency, ownership, buildings, positions
- equipment/OOB: production, deployment, templates, variants, starting stockpile
- localisation: active language setup and translation-submod key stability

A successful launch is not sufficient evidence that the mod is repaired.

---

## 13. Definition of done

A compatibility fix is complete only when:

- target HOI4 version and test playset are recorded
- original failure is precisely described
- root cause is confirmed, or remaining uncertainty is explicitly bounded
- patch is limited to the demonstrated cause
- intended behavior is preserved, or intentional changes are documented
- the exact reproduction no longer fails
- no new relevant errors appear compared with the baseline/control
- affected IDs, scopes, localisation, dependencies, and load-order effects are reviewed
- diff contains no unrelated cleanup or mass formatting
- runtime validation status is stated honestly

A compatibility release is ready only when:

- the source commit or immutable source snapshot is recorded
- the exact RT56 Workshop snapshot and required localisation configuration are recorded
- the staged package contains only intended public/runtime files
- no upload configuration targets HOK `2898629778`, donor revision `3793992662`, or RT56 `820260968`
- HOK authorship, donor-revision provenance, RT56/localisation/third-party credits, and compatibility contributions are represented accurately
- the description identifies the item as an independent compatibility continuation without impersonating HOK or RT56
- target version, dependencies, changelog, known limitations, and actual validation status are documented
- every shipped donor/RT56-derived file has provenance and redistribution status recorded
- the donor HOK is absent from the required runtime playset
- the RT56-only comparison shows no unexplained host-content loss
- first publication remains a new item; later updates target only the recorded compatibility ID

Not sufficient by itself:

- updating `supported_version`
- reaching the main menu
- reducing raw log-line count
- deleting content until `error.log` becomes quieter
- passing a text parser
- observing one happy path
- renaming and uploading an unverified copy
- inheriting any source `remote_file_id`

---

## 14. File, Git, attribution, and publication safety

- By default, create and modify files only under `C:\hoi\hearts_of_korea_Road_to_56` for this project.
- Never modify `C:\hoi\hearts_of_korea`, the base-game installation, the RT56 Workshop directory, HOI4 user data/logs, saves, or launcher files without separate explicit authorization.
- Never use a Workshop-managed copy or HOK donor as the authoritative working tree.
- Never overwrite user saves, playsets, or settings without explicit authorization and backup.
- Do not commit logs, crash dumps, saves, caches, credentials, account data, or personal launcher data unless requested as sanitized fixtures.
- Do not use destructive Git commands such as `git reset --hard`, `git clean`, forced checkout, or force-push.
- Do not discard pre-existing user changes, rename large trees for aesthetics, or mass-convert binary assets.
- When commits are explicitly requested, write every commit subject and body in English. Commit or push only within the requested scope; a completed earlier commit/push request is not standing authorization for later work.
- Do not add tools, dependencies, generators, or formatters unless approved and materially useful.
- Keep restoration and compatibility patches small; keep intentional redesign/new-content changes separately attributable whenever practical.
- Publication of a new compatibility item is permitted only when explicitly directed.
- HOK items `2898629778` and `3793992662` remain provenance references, and RT56 item `820260968` remains a dependency/provenance reference; none is this project's upload target.
- Do not impersonate the original HOK creator, donor-revision maintainers, or RT56 team, or present inherited work as newly authored.
- Preserve original names, credits, notices, licences, and third-party attributions; do not invent or remove a licence.
- Prefer depending on RT56 rather than redistributing its files. If an engine-required merged monolithic file contains RT56 content, record the exact source version/hash, applied delta, notice/licence status, and why redistribution is necessary.
- Attribute the user's original HOK work accurately and preserve separate donor-revision, RT56, localisation, and third-party contributions; do not repeat unsupported personal-history claims about contributors.
- Never expose credentials or perform an upload, update, visibility change, deletion, or metadata mutation without an explicit instruction for that exact target and action.

---

## 15. Reporting format

For implementation or diagnostics work, report:

1. **Scope**: what was and was not authorized.

2. **Baseline**: compatibility Git state, target version, HOK donor revision, RT56 fingerprint, playset, dependencies, and reproduction.

3. **Evidence**: relevant logs, source locations, and observed behavior.

4. **Root cause**: confirmed fact versus inference.

5. **Changes**: files and logic changed, with integration classification and provenance.

6. **Behavior impact**: preserved HOK behavior, preserved RT56 behavior, and intentional differences.

7. **Validation**: checks actually run and results.

8. **Remaining risk**: untested DLC, bookmarks, branches, submods, multiplayer, saves, or map paths.

9. **Git state**: working-tree changes and whether any commit/push occurred.

For release-preparation or publication work, additionally report:

- preparation only, first compatibility publication, or compatibility-item update
- source state, RT56 snapshot, package path/hash when practical, release version, and target HOI4 version
- HOK historical ID, HOK donor revision ID, RT56 dependency ID, and compatibility target ID, clearly distinguished
- dependency, metadata, credit, changelog, and validation status
- external account/Workshop actions actually performed

For review-only work:

- Put findings first, ordered by severity.
- Cite paths and line numbers where possible.
- Explain concrete failure modes, not style preferences.
- Separate confirmed defects from suggestions.
- State when runtime evidence is missing.
- Do not claim “no issues” when only a subset was inspected.

---

## 16. Hearts of Korea × RT56 preservation and integration rules

- Preserve the original HOK vanilla-friendly, multiplayer-conscious balance during restoration unless rebalance is explicitly requested, while documenting where RT56's systems necessarily change the context.
- Preserve the Korean identity, alternate-history premise, ideological routes, formables, leaders, names, custom assets, comments, credits, and design history.
- Follow `docs/decisions/0004-hok-korean-content-priority.md`: final KOR gameplay and Korean presentation are HOK-first; ordinary Chinese/Japanese gameplay and global/shared systems are RT56-first; cross-border Korean hooks are minimal reviewed merges.
- Determine Korean ownership by entry point and consumer, not filename alone. HOK downstream tags such as KCH/KJP remain Korean-owned when produced by a KOR route, while a normal JAP/CHI definition remains RT56-owned.
- Separate binary presentation payload from logical registry ownership. Prefer HOK Korean `.wav`, `.dds`, and `.tga` payloads after format/reference checks, but keep `.asset`, `.gfx`, soundeffect, sprite, entity, attachment, and animation IDs under one effective merged definition.
- Do not restore donor `sound/voice_korea.asset` unchanged alongside the generated `sound/r56_vo_Korean.asset`. The latter is the single effective registry: it retains the pinned RT56 category/compressor and merges HOK sound definitions, playback lists, weights, volume, and all 18 HOK WAV payloads.
- `tools/build_korean_assets.py` owns the HOK Korean WAVs, the basic-aircraft mesh/texture set, compatibility-local mesh/entity IDs, their graphic-database consumers, and the merged sound registry. The pruning and manifest rules must continue to preserve the 18 WAVs and three KOR diffuse textures.
- Treat the custom Korean map/state layout as a high-risk migration onto the RT56 world map, not as a standalone file copy.
- Preserve localisation keys used by translation and compatibility submods whenever possible.
- Do not assume the old Korean-language-mod contract survives RT56 localisation replacement; preserve or migrate it only after the supported configuration is designed and tested.
- Do not remove content merely because vanilla or a DLC changed; identify the target-version replacement mechanism first.
- Do not collapse custom content into vanilla placeholders merely to make the mod load.
- Preserve RT56's world changes and shared features unless a documented Korean integration choice intentionally changes them.
- For a Korean subsystem modified by both projects, document the HOK intent, RT56 behavior, chosen merged behavior, and rejected alternative.
- Distinguish inherited HOK content, donor-revision content, RT56-derived merge content, compatibility glue, restoration fixes, intentional redesigns, and new content in history and release notes.
- Do not imply that inherited work was created by the compatibility team or that any HOK/RT56 Workshop identity transferred to the new item.
- New content, modernization, and rebalance are allowed when explicitly requested, but must preserve attribution and be tested independently from compatibility claims.

---

## 17. Safe stopping conditions

Stop modifying and report the evidence instead of guessing when:

- the exact target version materially affects the fix but cannot be determined
- the launcher loads a different copy than the repository under review
- unknown dependency/load order directly affects the failure
- the HOK donor is enabled in a target compatibility playset without an explicit architecture change
- the RT56 Workshop snapshot changes during comparison or implementation
- a production file has no integration classification or an unexplained same-path/logical-ID collision remains
- multiple root causes remain equally plausible
- a fix requires additional unrecorded persistent map-ID renumbering, or the approved migration's reference closure cannot be demonstrated
- the proposed map merge cannot preserve the current RT56 global ID/RGB/reference set
- a `replace_path` migration would unload broad vanilla or RT56 content
- required binary source/format information is unavailable
- save compatibility needs an explicit migration decision
- an upload command or descriptor would target `2898629778`, `3793992662`, or `820260968`
- the intended compatibility item/account/action is unresolved at the external-action boundary
- a concrete third-party licence or attribution conflict is discovered
- donor/RT56-derived redistribution permission is required but cannot be established
- the staged package contains credentials, personal data, or files whose publication status cannot be determined safely

Do not stop merely because this is a compatibility continuation or a new Workshop item is required; those are established project conditions. The user's original HOK authorship and authorization for this task are recorded above.

When blocked, make the safest non-destructive progress possible: inventory the subsystem, identify missing evidence, and provide the next concrete diagnostic or release-preparation step. Do not manufacture certainty to keep moving.
