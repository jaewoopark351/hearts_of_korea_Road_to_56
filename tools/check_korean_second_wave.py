#!/usr/bin/env python3
"""Read-only contracts for the pinned 134-focus second wave; no engine proof."""
from __future__ import annotations

import argparse
import hashlib
import re
import struct
from pathlib import Path

from check_korean_focus_update import (
    Block, Entry, FOCUS_PATH, PREFIX, SHINE_EFFECT, SHINE_OVERLAY,
    ROOT, RT56_ROOT, VANILLA_ROOT, children, effective_files, focus_blocks,
    check_new_id_collisions, check_pp_only_project, named, one, parse, read, replace_entry,
    require, scalar, walk,
)
from validate_port import localisation_keys, mask_comments
from build_rt56_map import PROVINCE_ID_MAP, STATE_ID_MAP
from migrate_hok_ids import apply_post_migration_fixes, replace_tokens
from source_snapshot import (
    SECOND_WAVE_ASSET_PATHS, SECOND_WAVE_RUNTIME_PATHS,
    SECOND_WAVE_SPRITE_PATHS, read_second_wave_source, read_source_file,
    policy_update_lock, read_policy_source, second_wave_lock,
    localisation_update_lock, read_localisation_source,
    material_cycle_lock, read_material_cycle_source,
)

# [2026-09-23]_kpopmodder: Compare immutable donor input with only reviewed port transformations, never builder output.
DONOR_OVERLAY = "gfx/interface/goals/HOK_KOR/shine_overlay.dds"
OVERLAY_HASH = "BB416649358C73D34AACD46BAD61BC44211FAC8111627B56E25F385AD98F4448"


#20261003_kpopmodder: Audit the frozen material-cycle delta without relaxing earlier focus, geography or source contracts.
MATERIAL_IDEA_PATH = "common/ideas/HOK_KOR_common_followup.txt"
MATERIAL_DECISION_PATH = "common/decisions/HOK_KOR_common_followup.txt"
MATERIAL_CATEGORY_PATH = "common/decisions/categories/HOK_KOR_common_followup.txt"
MATERIAL_GFX_PATH = "interface/HOK_KOR_material_cycle_icons.gfx"
MATERIAL_LOCALES = tuple(f"localisation/{language}/HOK_KOR_common_followup_l_{language}.yml"
                        for language in ("english", "korean"))
MATERIAL_TIERS = ("HOK_KOR_cmn_material_cycle_1", "HOK_KOR_cmn_material_cycle_2")
MATERIAL_BOOST = "HOK_KOR_cmn_emergency_material_cycle_boost"
MATERIAL_DECISION = "HOK_KOR_cmn_emergency_material_cycle"
MATERIAL_CATEGORY = "HOK_KOR_cmn_material_cycle_projects"
MATERIAL_FOCUS = "HOK_KOR_cmn_closed_material_cycle"
MATERIAL_SPRITES = {
    "GFX_idea_HOK_KOR_icon_cmn_emergency_material_cycle_boost":
        "gfx/interface/ideas/HOK_KOR/material_cycle/cmn_emergency_material_cycle_boost.dds",
    "GFX_HOK_KOR_decision_cmn_emergency_material_cycle":
        "gfx/interface/decisions/HOK_KOR/material_cycle/cmn_emergency_material_cycle.dds",
    "GFX_HOK_KOR_decision_category_cmn_material_cycle_projects":
        "gfx/interface/decisions/HOK_KOR/material_cycle/cmn_material_cycle_projects.dds",
}


def runtime_paths() -> tuple[str, ...]:
    return tuple(dict.fromkeys((*SECOND_WAVE_RUNTIME_PATHS, *material_cycle_lock()["runtime_text"])))


def selected_source(relative: str) -> bytes:
    if relative in material_cycle_lock()["runtime_text"]:
        return read_material_cycle_source(relative)
    #20260926_kpopmodder: Compare the revised prose against its own immutable source before regional adaptation.
    if relative in localisation_update_lock()["runtime_text"]:
        return read_localisation_source(relative)
    return read_policy_source(relative) if relative in policy_update_lock()["runtime_text"] else read_second_wave_source(relative)


def expected_payload(relative: str) -> bytes:
    from korean_second_wave_geography import apply_second_wave_geography
    data = selected_source(relative)
    if relative == FOCUS_PATH:
        data = apply_post_migration_fixes(relative, replace_tokens(data, {**PROVINCE_ID_MAP, **STATE_ID_MAP}))
    if relative.endswith(".gfx"):
        data = data.replace(DONOR_OVERLAY.encode(), SHINE_OVERLAY.encode())
    return apply_second_wave_geography(relative, data)


def expected_script(relative: str) -> Block:
    # [2026-09-23]_kpopmodder: Reconstruct geography with an independent ordered-AST algorithm, not the generator's text replacements.
    from korean_second_wave_geography import DECISION_PATH, FOCUS_IDS, HW_FOCUS_IDS, STATE_GROUPS, STRONGHOLD_GROUPS
    require(STATE_GROUPS == {328: (328, 941), 714: (714, 944, 945), 717: (717, 942, 943)}, "unreviewed M policy geography contract")
    require(STRONGHOLD_GROUPS == {716: (716,), 745: (745,), 328: (328, 941), 717: (717, 942, 943),
                                 714: (714, 944, 945), 761: (761,), 715: (715, 946), 610: (610, 947)},
            "unreviewed H whole-region stronghold contract")
    #20260923_kpopmodder: Layer only the immutable reviewed cost update over the unchanged second-wave source contracts.
    data = selected_source(relative)
    if relative == FOCUS_PATH:
        data = apply_post_migration_fixes(relative, replace_tokens(data, {**PROVINCE_ID_MAP, **STATE_ID_MAP}))
    if relative.endswith(".gfx"):
        data = data.replace(DONOR_OVERLAY.encode(), SHINE_OVERLAY.encode())
    source = parse(data.decode("utf-8-sig"))

    def policy(block: Block) -> Block:
        result = []
        for entry in block:
            if entry.key.isdigit() and int(entry.key) in STATE_GROUPS and isinstance(entry.value, tuple):
                result.extend(Entry(str(state), entry.op, entry.value) for state in STATE_GROUPS[int(entry.key)])
            elif entry.key == "state" and isinstance(entry.value, str) and entry.value.isdigit() and int(entry.value) in STATE_GROUPS:
                result.extend(Entry(entry.key, entry.op, str(state)) for state in STATE_GROUPS[int(entry.value)])
            else:
                result.append(Entry(entry.key, entry.op, policy(entry.value)) if isinstance(entry.value, tuple) else entry)
        return tuple(result)

    def stronghold(block: Block) -> Block:
        result = []
        for entry in block:
            if entry.key == "AND" and isinstance(entry.value, tuple) and len(entry.value) == 2:
                owner, control = entry.value
                if owner.key == "owns_state" and control.key == "has_full_control_of_state" and owner.value == control.value and str(owner.value).isdigit() and int(owner.value) in STRONGHOLD_GROUPS:
                    result.append(Entry("AND", "=", tuple(item for state in STRONGHOLD_GROUPS[int(owner.value)]
                                  for item in (Entry("owns_state", "=", str(state)), Entry("has_full_control_of_state", "=", str(state))))))
                    continue
            result.append(Entry(entry.key, entry.op, stronghold(entry.value)) if isinstance(entry.value, tuple) else entry)
        return tuple(result)

    if relative == FOCUS_PATH:
        tree = []
        for entry in one(source, "focus_tree"):
            if entry.key == "focus" and isinstance(entry.value, tuple):
                identifier = scalar(entry.value, "id")
                body = policy(entry.value) if identifier in FOCUS_IDS else stronghold(entry.value) if identifier in HW_FOCUS_IDS else entry.value
                tree.append(Entry(entry.key, entry.op, body))
            else:
                tree.append(entry)
        return replace_entry(source, ("focus_tree",), tuple(tree))
    return policy(source) if relative == DECISION_PATH else source


def documents() -> tuple[dict[str, Block], dict[str, Block]]:
    expected, current = {}, {}
    for path in runtime_paths():
        relative = Path(path).as_posix()
        if Path(relative).suffix not in (".txt", ".gfx"):
            continue
        expected[relative] = expected_script(relative)
        current[relative] = read(ROOT / relative)
    return current, expected


def compare_documents(current: dict[str, Block], expected: dict[str, Block]) -> None:
    require(current.keys() == expected.keys(), "second-wave script inventory changed")
    for relative, block in expected.items():
        require(current[relative] == block, f"second-wave ordered source contract differs: {relative}")


def collect(current: dict[str, Block]) -> dict[str, dict[str, Block]]:
    result = {kind: {} for kind in ("focus", "idea", "decision", "category", "dynamic", "sprite")}
    result["focus"] = focus_blocks(current[FOCUS_PATH])
    for relative, block in current.items():
        kind, definitions = None, {}
        if relative.startswith("common/ideas/"):
            kind, definitions = "idea", named(one(one(block, "ideas"), "country"))
        elif relative.startswith("common/decisions/categories/"):
            kind, definitions = "category", named(block)
        elif relative.startswith("common/decisions/"):
            kind = "decision"
            for category in named(block).values():
                for identifier, body in named(category).items():
                    require(identifier not in definitions, f"duplicate decision: {identifier}")
                    definitions[identifier] = body
        elif relative.startswith("common/dynamic_modifiers/"):
            kind, definitions = "dynamic", named(block)
        elif relative.endswith(".gfx"):
            kind = "sprite"
            for entry in one(block, "spriteTypes"):
                require(entry.key.lower() == "spritetype" and isinstance(entry.value, tuple), "unreviewed GFX root")
                identifier = scalar(entry.value, "name")
                require(identifier not in definitions, f"duplicate sprite: {identifier}")
                definitions[identifier] = entry.value
        if kind:
            require(not definitions.keys() & result[kind].keys(), f"duplicate {kind} definitions across selected files")
            result[kind].update(definitions)
    return result


def check_inventory(groups: dict[str, dict[str, Block]]) -> set[str]:
    legacy = focus_blocks(parse(read_source_file(FOCUS_PATH, updated=True).decode("utf-8-sig")))
    focuses = groups["focus"]
    added = focuses.keys() - legacy.keys()
    require(len(focuses) == 460 and len(added) == 134 and legacy.keys() <= focuses.keys(), "460-focus/134-addition identity contract")
    require(all(identifier.startswith(PREFIX) for identifier in added), "unprefixed second-wave focus")
    for kind, count in (("idea", 64), ("decision", 19), ("category", 5), ("dynamic", 12), ("sprite", 368)):
        require(len(groups[kind]) == count, f"expected {count} second-wave {kind} definitions")
    for identifier in added:
        block = focuses[identifier]
        require(scalar(block, "cost") == "5", f"second-wave 35-day duration changed: {identifier}")
        for key, value in (("cancel_if_invalid", "yes"), ("continue_if_invalid", "no"), ("available_if_capitulated", "no")):
            require(scalar(block, key) == value, f"second-wave focus cancellation changed: {identifier}/{key}")
    return set(added)


def check_layout(focuses: dict[str, Block], added: set[str]) -> None:
    # [2026-09-23]_kpopmodder: Declaration order is checked separately from existence and gameplay prerequisites.
    declared: set[str] = set()
    for identifier, block in focuses.items():
        anchors = [entry.value for entry in block if entry.key == "relative_position_id"]
        require(len(anchors) <= 1, f"multiple relative anchors: {identifier}")
        require(not anchors or anchors[0] in declared, f"relative anchor is missing, forward or cyclic: {identifier}")
        declared.add(identifier)
        for key in ("prerequisite", "mutually_exclusive"):
            for relation in children(block, key):
                require(all(entry.key == "focus" and entry.value in focuses for entry in relation), f"unknown {key}: {identifier}")
                if key == "mutually_exclusive" and identifier in added:
                    for entry in relation:
                        inverse = {item.value for peer in children(focuses[entry.value], key) for item in peer}
                        require(identifier in inverse, f"asymmetric new mutual exclusion: {identifier}/{entry.value}")
    require(sum(not any(entry.key == "relative_position_id" for entry in block) for block in focuses.values()) == 7,
            "second-wave absolute layout anchor count changed")


def check_projects(groups: dict[str, dict[str, Block]]) -> None:
    for identifier, block in groups["decision"].items():
        #20261003_kpopmodder: Keep the independent emergency program out of the older shared-cooldown contract.
        if identifier == MATERIAL_DECISION:
            continue
        require(scalar(block, "days_remove") == "90" and scalar(block, "fire_only_once") == "no", f"project lifetime changed: {identifier}")
        for key in ("available", "complete_effect", "cancel_trigger", "cancel_effect", "remove_effect"):
            require(bool(one(block, key)), f"project lacks {key}: {identifier}")
        for key in ("cancel_effect", "remove_effect"):
            require(not any(entry.key == "add_political_power" for entry in walk(one(block, key))), f"unreviewed project refund: {identifier}")
            cooldowns = [entry.value for entry in walk(one(block, key)) if entry.key == "set_country_flag" and isinstance(entry.value, tuple)]
            require(len(cooldowns) == 1 and scalar(cooldowns[0], "days") == "90", f"project cooldown changed: {identifier}/{key}")
    #20260923_kpopmodder: Preserve the two policy effects and PP-aware AI while removing every factory charge and gate.
    for identifier, modifier in (("HOK_KOR_yeo_rural_credit_project", "production_speed_buildings_factor"),
                                 ("HOK_KOR_pak_current_output_project", "industrial_capacity_factory")):
        block = groups["decision"][identifier]
        check_pp_only_project(identifier, block)
        require(one(block, "modifier") == parse(f"{modifier} = 0.10"), f"PP-only project effect changed: {identifier}")
        require(one(block, "ai_will_do") == parse("factor = 0.5 modifier = { factor = 0 NOT = { has_political_power > 149 } }"),
                f"PP-only project AI cost guard or weight changed: {identifier}")
    for identifier, block in groups["dynamic"].items():
        require(bool(one(block, "enable")) and bool(one(block, "remove_trigger")), f"state modifier lifetime missing: {identifier}")
        require(any(entry.key == "is_owned_by" and entry.value == "KOR" for entry in walk(one(block, "enable"))), f"state modifier owner gate missing: {identifier}")
        require(any(entry.key == "is_fully_controlled_by" and entry.value == "KOR" for entry in walk(one(block, "enable"))), f"state modifier control gate missing: {identifier}")


def check_regional_gates(groups: dict[str, dict[str, Block]]) -> None:
    # [2026-09-23]_kpopmodder: Model only the explicit ownership/control conjunctions; do not infer engine lifecycle.
    strongholds = ((716,), (745,), (328, 941), (717, 942, 943), (714, 944, 945), (761,), (715, 946), (610, 947))
    expected = tuple(Entry("AND", "=", tuple(item for state in region for item in (
        Entry("owns_state", "=", str(state)), Entry("has_full_control_of_state", "=", str(state))))) for region in strongholds)
    hwan = {identifier: block for identifier, block in groups["focus"].items() if identifier.startswith("HOK_KOR_hw_")}
    require(len(hwan) == 14, "expected fourteen Hwan stronghold consumers")
    for identifier, block in hwan.items():
        gate = one(one(block, "available"), "OR")
        require(gate == expected, f"Hwan must retain eight whole-region alternatives: {identifier}")
        alternatives = [entry.value for entry in gate]
        qualifies = lambda owned, controlled: any(
            {int(entry.value) for entry in region if entry.key == "owns_state"} <= owned
            and {int(entry.value) for entry in region if entry.key == "has_full_control_of_state"} <= controlled
            for region in alternatives)
        require(not qualifies(set(), set()), f"empty stronghold unexpectedly eligible: {identifier}")
        for region in strongholds:
            whole = set(region)
            require(qualifies(whole, whole), f"complete Hwan stronghold rejected: {identifier}/{region}")
            for state in region:
                require(not qualifies(whole - {state}, whole) and not qualifies(whole, whole - {state}),
                        f"partial Hwan ownership/control accepted: {identifier}/{region}/{state}")
    for policy, targets in (("local_services", {328, 941}), ("community_services", {328, 941}),
                            ("material_recovery", {328, 941, 714, 944, 945, 717, 942, 943}), ("municipal_routine", {328, 941})):
        identifier = f"HOK_KOR_mc_{policy}_project"
        block = groups["decision"][identifier]
        available_states = {int(entry.key) for entry in one(block, "available") if entry.key.isdigit()}
        require(available_states == targets, f"M project target conjunction changed: {identifier}")
        for state in targets:
            require(one(one(block, "available"), str(state)) == parse("is_owned_by = ROOT is_fully_controlled_by = ROOT"),
                    f"M project ownership/control weakened: {identifier}/{state}")
        for callback in ("cancel_effect", "remove_effect"):
            cleanup = one(block, callback)
            require({int(entry.key) for entry in cleanup if entry.key.isdigit()} == targets,
                    f"M project leaves temporary effects in other regions: {identifier}/{callback}")
            removed = {scalar(entry.value, "modifier") for entry in walk(cleanup)
                       if entry.key == "remove_dynamic_modifier" and isinstance(entry.value, tuple)}
            require(removed == {f"HOK_KOR_mc_{policy}_concentrated"}, f"M project removes permanent institution: {identifier}/{callback}")


def exact_case(relative: str, inventory: set[str]) -> None:
    require(relative in inventory, f"missing or case-mismatched local HOK asset: {relative}")
    require(not Path(relative).is_absolute() and ".." not in Path(relative).parts and "\\" not in relative, f"unsafe asset reference: {relative}")


def check_assets(groups: dict[str, dict[str, Block]], added: set[str], payloads: dict[str, bytes] | None = None) -> None:
    historical_assets = {Path(path).as_posix() for path in SECOND_WAVE_ASSET_PATHS}
    material_assets = set(material_cycle_lock()["runtime_assets"])
    require(len(historical_assets) == 231 and material_assets == set(MATERIAL_SPRITES.values())
            and not historical_assets & material_assets, "expected 231 historical and three material-cycle DDS payloads")
    assets = historical_assets | material_assets
    disk_paths = {path.relative_to(ROOT).as_posix() for base in ("goals", "ideas", "decisions")
                  for path in (ROOT / "gfx/interface" / base / "HOK_KOR").rglob("*.dds")}
    supplied = {relative: (ROOT / relative).read_bytes() for relative in assets} if payloads is None else payloads
    require(set(supplied) == assets, "missing or extra second-wave DDS payload")
    records = {**second_wave_lock()["runtime_assets"], **material_cycle_lock()["runtime_assets"]}
    category_textures = {scalar(groups["sprite"][scalar(block, "icon")], "texturefile") for block in groups["category"].values()}
    for relative, data in supplied.items():
        exact_case(relative, disk_paths)
        require(hashlib.sha256(data).hexdigest().upper() == records[relative]["sha256"].upper(), f"DDS source hash changed: {relative}")
        dimensions = ((100, 88) if "/goals/" in relative else (60, 68) if "/ideas/" in relative
                      else (51, 40) if relative in category_textures else (32, 32))
        require(data[:4] == b"DDS " and len(data) >= 128, f"invalid DDS header: {relative}")
        header = struct.unpack("<31I", data[4:128])
        require(header[0] == 124 and (header[3], header[2]) == dimensions
                and header[18:26] == (32, 65, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
                and header[6] in (0, 1) and len(data) == 128 + dimensions[0] * dimensions[1] * 4,
                f"DDS dimensions/BGRA/alpha/frame contract changed: {relative}")
    sprites = groups["sprite"]
    consumed = {scalar(groups["focus"][identifier], "icon") for identifier in added}
    consumed |= {"GFX_idea_" + scalar(block, "picture") for block in groups["idea"].values()}
    consumed |= {scalar(block, "icon") for kind in ("decision", "category", "dynamic") for block in groups[kind].values()}
    require(consumed <= sprites.keys(), f"unresolved HOK sprite consumer: {sorted(consumed - sprites.keys())}")
    require(sprites.keys() == consumed | {scalar(groups["focus"][identifier], "icon") + "_shine" for identifier in added}, "unconsumed or missing second-wave sprite")
    require({scalar(block, "texturefile") for block in sprites.values()} == assets, "DDS consumer coverage differs")
    for identifier, block in sprites.items():
        texture = scalar(block, "texturefile")
        exact_case(texture, assets)
        for entry in walk(block):
            if entry.key.lower() in ("texturefile", "animationmaskfile"):
                require(entry.value == texture, f"HOK sprite/mask does not use its local image: {identifier}")
            elif entry.key.lower() == "animationtexturefile":
                require(entry.value == SHINE_OVERLAY, f"unreviewed shared overlay: {identifier}")
            elif entry.key.lower() == "effectfile":
                require(entry.value == SHINE_EFFECT, f"unreviewed shine effect: {identifier}")
        if identifier.endswith("_shine"):
            require(len(children(block, "animation")) == 2, f"shine animation count changed: {identifier}")
    # [2026-09-23]_kpopmodder: Check physical registries independently of the selected source allowlist.
    declarations = re.compile(r'\bname\s*=\s*"?([A-Za-z0-9_]+)"?')
    selected = {Path(path).as_posix() for path in SECOND_WAVE_SPRITE_PATHS} | {MATERIAL_GFX_PATH}
    for root in (ROOT, RT56_ROOT, VANILLA_ROOT):
        for path in (root / "interface").rglob("*.gfx"):
            if root == ROOT and path.relative_to(root).as_posix() in selected:
                continue
            found = set(declarations.findall(mask_comments(path.read_bytes().decode("utf-8-sig"))))
            require(not found & sprites.keys(), f"new sprite IDs collide in {path}: {sorted(found & sprites.keys())}")
    require(hashlib.sha256((VANILLA_ROOT / SHINE_OVERLAY).read_bytes()).hexdigest().upper() == OVERLAY_HASH, "vanilla shared overlay source drift")
    require(not (ROOT / DONOR_OVERLAY).exists(), "unapproved local vanilla overlay copy")


def localisation_payloads() -> dict[str, bytes]:
    return {Path(path).as_posix(): (ROOT / path).read_bytes() for path in SECOND_WAVE_RUNTIME_PATHS if Path(path).suffix == ".yml"}


def check_localisation(payloads: dict[str, bytes], groups: dict[str, dict[str, Block]], added: set[str]) -> None:
    require(len(payloads) == 22, "expected eleven localisation pairs")
    keys = {language: set() for language in ("english", "korean")}
    for relative, data in payloads.items():
        language = Path(relative).parts[1]
        expected = expected_payload(relative)
        require(data == expected, f"localisation differs from immutable source/geography contract: {relative}")
        require(data.startswith(b"\xef\xbb\xbf" + f"l_{language}:".encode()), f"localisation BOM/header changed: {relative}")
        found = re.findall(r"(?m)^\s+([A-Za-z0-9_.-]+):\d*\s", data.decode("utf-8-sig"))
        require(len(found) == len(set(found)) and not keys[language] & set(found), f"duplicate new localisation: {relative}")
        keys[language].update(found)
        if language == "english":
            counterpart = relative.replace("/english/", "/korean/").replace("_l_english.yml", "_l_korean.yml")
            require(counterpart in payloads and data.decode("utf-8-sig").splitlines()[1:] == payloads[counterpart].decode("utf-8-sig").splitlines()[1:], f"paired Korean-content localisation diverged: {relative}")
    required = added | set(groups["idea"]) | set(groups["decision"]) | set(groups["category"]) | set(groups["dynamic"])
    required |= {identifier + "_desc" for identifier in required}
    for language in keys:
        require(required <= keys[language], f"missing {language} new definition keys: {sorted(required - keys[language])}")


#20261003_kpopmodder: Require the intended permanent rewards and bounded PP-only timed effect independently of frozen-source equality.
def check_material_cycle(groups: dict[str, dict[str, Block]], payloads: dict[str, bytes] | None = None) -> None:
    lock = material_cycle_lock()
    require(set(lock["runtime_text"]) == {MATERIAL_IDEA_PATH, MATERIAL_DECISION_PATH, MATERIAL_CATEGORY_PATH,
                                          MATERIAL_GFX_PATH, *MATERIAL_LOCALES},
            "material-cycle runtime allowlist must remain six text files without map or on_action changes")
    require(set(lock["runtime_assets"]) == set(MATERIAL_SPRITES.values()), "material-cycle artwork allowlist changed")
    require(FOCUS_PATH in lock["preserved_runtime"], "material-cycle update must pin the unchanged focus tree")
    for relative, digest in lock["preserved_runtime"].items():
        require(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest().upper() == digest.upper(),
                f"material-cycle update changed preserved runtime: {relative}")

    original = named(one(one(parse(read_second_wave_source(MATERIAL_IDEA_PATH).decode("utf-8-sig")), "ideas"), "country"))
    ideas = groups["idea"]
    selected_ideas = named(one(one(read(ROOT / MATERIAL_IDEA_PATH), "ideas"), "country"))
    require(selected_ideas.keys() == original.keys() | {MATERIAL_BOOST}, "material-cycle update changed inherited idea IDs")
    for identifier, baseline in original.items():
        if identifier in MATERIAL_TIERS:
            amount = "0.3" if identifier == MATERIAL_TIERS[0] else "0.6"
            baseline = replace_entry(baseline, ("modifier",), parse(
                f"local_resources_factor = {amount} production_lack_of_resource_penalty_factor = -{amount}"))
        require(ideas[identifier] == baseline, f"material-cycle update changed an unrelated idea or tier field: {identifier}")
    boost = ideas[MATERIAL_BOOST]
    require(one(boost, "allowed") == parse("original_tag = KOR")
            and one(boost, "allowed_civil_war") == parse("always = no")
            and scalar(boost, "removal_cost") == "-1", "temporary material-cycle idea ownership/civil-war contract changed")
    require(one(boost, "modifier") == parse("local_resources_factor = 0.3 production_lack_of_resource_penalty_factor = -0.3"),
            "temporary material-cycle reward must remain +30%/-30%")
    require(one(boost, "cancel") == parse(
        f"OR = {{ has_civil_war = yes has_capitulated = yes NOT = {{ has_idea = {MATERIAL_TIERS[1]} }} }}"),
        "temporary material-cycle idea must expire on civil war, capitulation or base-II loss")

    focuses = groups["focus"]
    require(one(focuses["HOK_KOR_cmn_scrap_collection"], "completion_reward") == parse(f"add_ideas = {MATERIAL_TIERS[0]}"),
            "scrap collection no longer grants only material-cycle I")
    require(one(focuses[MATERIAL_FOCUS], "completion_reward") == parse(
        f"if = {{ limit = {{ has_idea = {MATERIAL_TIERS[0]} }} swap_ideas = {{ remove_idea = {MATERIAL_TIERS[0]} add_idea = {MATERIAL_TIERS[1]} }} }} "
        f"else = {{ add_ideas = {MATERIAL_TIERS[1]} }}"), "material-cycle II must replace I without stacking the lower tier")
    require(one(focuses[MATERIAL_FOCUS], "prerequisite") == parse("focus = HOK_KOR_cmn_foundry_exchange"),
            "closed material-cycle prerequisite changed")
    for identifier, reward in (
        ("HOK_KOR_cmn_ore_classification", "add_tech_bonus = { name = HOK_KOR_cmn_ore_classification bonus = 1.5 uses = 1 category = industry }"),
        ("HOK_KOR_cmn_coke_testing", "add_tech_bonus = { name = HOK_KOR_cmn_coke_testing bonus = 1.0 uses = 1 category = excavation_tech }"),
        ("HOK_KOR_cmn_foundry_exchange", "add_political_power = 150"),
    ):
        require(one(focuses[identifier], "completion_reward") == parse(reward), f"material-cycle update lost an existing secondary reward: {identifier}")

    decision = groups["decision"][MATERIAL_DECISION]
    category = groups["category"][MATERIAL_CATEGORY]
    require(one(decision, "allowed") == one(category, "allowed") == parse("original_tag = KOR"),
            "material-cycle decision/category must remain KOR-owned")
    require(one(decision, "visible") == one(category, "visible") == parse(f"has_completed_focus = {MATERIAL_FOCUS}"),
            "material-cycle decision/category must unlock from the existing II focus")
    require(one(decision, "available") == parse(
        f"has_completed_focus = {MATERIAL_FOCUS} has_idea = {MATERIAL_TIERS[1]} has_civil_war = no has_capitulated = no "
        f"NOT = {{ has_idea = {MATERIAL_BOOST} }}"), "material-cycle availability must forbid active reuse and invalid country states")
    check_pp_only_project(MATERIAL_DECISION, decision)
    for field, value in (("cost", "150"), ("days_remove", "90"), ("days_re_enable", "0"), ("fire_only_once", "no")):
        require(scalar(decision, field) == value, f"material-cycle cost/duration/repeat contract changed: {field}")
    require(one(decision, "complete_effect") == parse(f"add_timed_idea = {{ idea = {MATERIAL_BOOST} days = 90 }}"),
            "material-cycle program must grant exactly one 90-day temporary idea without a second charge")
    require(one(decision, "cancel_trigger") == parse(
        f"OR = {{ NOT = {{ has_idea = {MATERIAL_TIERS[1]} }} has_civil_war = yes has_capitulated = yes }}"),
        "material-cycle project cancellation conditions changed")
    cleanup = parse(f"if = {{ limit = {{ has_idea = {MATERIAL_BOOST} }} remove_ideas = {MATERIAL_BOOST} }}")
    require(one(decision, "cancel_effect") == one(decision, "remove_effect") == cleanup,
            "material-cycle cleanup must remove only the temporary idea without a refund, permanent removal or cooldown")
    require(one(decision, "ai_will_do") == parse("factor = 0.5 modifier = { factor = 0 NOT = { has_political_power > 149 } }"),
            "material-cycle AI weight or PP guard changed")
    allowed_keys = {
        "allowed", "original_tag", "allowed_civil_war", "always", "removal_cost", "picture", "modifier",
        "local_resources_factor", "production_lack_of_resource_penalty_factor", "cancel", "OR", "NOT",
        "has_civil_war", "has_capitulated", "has_idea", "icon", "visible", "has_completed_focus", "available",
        "cost", "days_remove", "days_re_enable", "fire_only_once", "complete_effect", "add_timed_idea", "idea", "days",
        "cancel_trigger", "cancel_effect", "remove_effect", "if", "limit", "remove_ideas", "ai_will_do", "factor", "has_political_power",
    }
    require(all(entry.key in allowed_keys for block in (boost, decision, category) for entry in walk(block)),
            "material-cycle program introduced a scope switch, map target, persistent flag/variable or unreviewed command")
    for identifier, texture in MATERIAL_SPRITES.items():
        require(groups["sprite"][identifier] == parse(f'name = "{identifier}" texturefile = "{texture}"'),
                f"material-cycle sprite mapping changed: {identifier}")
    require(scalar(boost, "picture") == "HOK_KOR_icon_cmn_emergency_material_cycle_boost"
            and scalar(decision, "icon") == "GFX_HOK_KOR_decision_cmn_emergency_material_cycle"
            and scalar(category, "icon") == "GFX_HOK_KOR_decision_category_cmn_material_cycle_projects",
            "material-cycle artwork consumer changed")

    payloads = localisation_payloads() if payloads is None else payloads
    new_keys = {identifier + suffix for identifier in (MATERIAL_BOOST, MATERIAL_DECISION, MATERIAL_CATEGORY) for suffix in ("", "_desc")}
    changed_descriptions = {identifier + "_desc" for identifier in MATERIAL_TIERS}
    pattern = re.compile(r'(?m)^\s+([A-Za-z0-9_.-]+):\d+ "((?:[^"\\\r\n]|\\.)*)"\s*$')
    for relative in MATERIAL_LOCALES:
        baseline = read_localisation_source(relative)
        data = payloads[relative]
        old_entries = pattern.findall(baseline.decode("utf-8-sig"))
        new_entries = pattern.findall(data.decode("utf-8-sig"))
        old_order, new_order = [key for key, _ in old_entries], [key for key, _ in new_entries]
        require(new_order[:len(old_order)] == old_order and set(new_order[len(old_order):]) == new_keys
                and len(new_order) == len(old_order) + 6, f"material-cycle localisation changed old key order or its six-key addition: {relative}")
        values = dict(new_entries)
        require(all(values[key] == value for key, value in old_entries if key not in changed_descriptions),
                f"material-cycle localisation changed unrelated prose: {relative}")
        require(all(values[key].strip() for key in new_keys | changed_descriptions), f"empty material-cycle description: {relative}")
        old_notes = [line for line in baseline.decode("utf-8-sig").splitlines() if line.lstrip().startswith("#")]
        require(all(note in data.decode("utf-8-sig").splitlines() for note in old_notes), f"material-cycle localisation lost contributor notes: {relative}")


def check_references(groups: dict[str, dict[str, Block]], added: set[str]) -> None:
    focuses = groups["focus"]
    all_ideas = set()
    for path in (ROOT / "common/ideas").glob("*.txt"):
        for container in children(read(path), "ideas"):
            for group in container:
                if isinstance(group.value, tuple):
                    all_ideas.update(named(group.value))
    blocks = [focuses[identifier] for identifier in added] + [block for kind in ("idea", "decision", "category", "dynamic") for block in groups[kind].values()]
    for entry in (item for block in blocks for item in walk(block)):
        if isinstance(entry.value, str):
            targets = {"focus": focuses, "has_completed_focus": focuses, "relative_position_id": focuses,
                       "unlock_decision_tooltip": groups["decision"], "add_ideas": all_ideas,
                       "remove_ideas": all_ideas, "add_idea": all_ideas, "remove_idea": all_ideas,
                       "has_idea": all_ideas, "idea": all_ideas}
            if entry.key in targets and entry.value.startswith(PREFIX):
                require(entry.value in targets[entry.key], f"unresolved second-wave {entry.key}: {entry.value}")
        if entry.key in ("add_dynamic_modifier", "remove_dynamic_modifier", "has_dynamic_modifier") and isinstance(entry.value, tuple):
            identifier = scalar(entry.value, "modifier")
            if identifier.startswith(PREFIX):
                require(identifier in groups["dynamic"], f"unresolved state modifier: {identifier}")
    tooltip_keys = {entry.value for block in blocks for entry in walk(block)
                    if entry.key in ("custom_effect_tooltip", "custom_modifier_tooltip", "tooltip")
                    and isinstance(entry.value, str) and entry.value.startswith(PREFIX)}
    for language in ("english", "korean"):
        require(tooltip_keys <= localisation_keys(ROOT, language), f"missing {language} second-wave tooltip keys")
    # [2026-09-23]_kpopmodder: Resolve research rewards against the actual host/schema databases, separately from source equivalence.
    tech_ids, tech_categories = set(), set()
    for path in effective_files("common/technologies"):
        for container in children(read(path), "technologies"):
            for entry in container:
                if isinstance(entry.value, tuple):
                    tech_ids.add(entry.key)
                    for categories in children(entry.value, "categories"):
                        tech_categories.update(item.key for item in categories)
    wanted_mios = {entry.key[4:] for block in blocks for entry in walk(block) if entry.key.startswith("mio:")}
    mio_ids = set()
    for path in effective_files("common/military_industrial_organization/organizations"):
        text = path.read_bytes().decode("utf-8-sig")
        if any(identifier in mask_comments(text) for identifier in wanted_mios):
            mio_ids.update(named(parse(text)))
    for entry in (item for block in blocks for item in walk(block)):
        if entry.key == "technology":
            require(entry.value in tech_ids, f"missing host technology: {entry.value}")
        elif entry.key == "category" and isinstance(entry.value, str):
            require(entry.value in tech_categories, f"missing host research category: {entry.value}")
        elif entry.key == "set_technology" and isinstance(entry.value, tuple):
            require(all(item.key == "popup" or item.key in tech_ids for item in entry.value), "missing granted host technology")
        elif entry.key.startswith("mio:"):
            require(entry.key[4:] in mio_ids, f"missing host MIO: {entry.key}")
    collisions = {kind: (set(groups[kind]) if kind != "focus" else added, directory) for kind, directory in (
        ("focus", "common/national_focus"), ("idea", "common/ideas"), ("decision", "common/decisions"),
        ("category", "common/decisions/categories"), ("dynamic", "common/dynamic_modifiers"))}
    check_new_id_collisions(collisions, {Path(path).as_posix() for path in runtime_paths()})


def run_checks() -> None:
    current, expected = documents()
    compare_documents(current, expected)
    groups = collect(current)
    added = check_inventory(groups)
    check_layout(groups["focus"], added)
    check_projects(groups)
    check_regional_gates(groups)
    check_material_cycle(groups)
    check_assets(groups, added)
    check_localisation(localisation_payloads(), groups, added)
    check_references(groups, added)
    print("PASS second wave plus material cycle: pinned 460 focuses (134 new), 64 ideas, 19 projects, 5 categories, 12 state modifiers; ordered source/port contracts")
    print("PASS material cycle: unchanged focuses and unrelated content; +30%/+60% tiers, one PP150/90-day boost, no stacking or cooldown, temporary-only cleanup")
    print("PASS second-wave artwork/localisation: 234 exact DDS, 368 sprites, 17 registries, 11 paired language files; vanilla shine fallback")
    print("STATIC ONLY: no HOI4 evaluation, geography lifecycle, layout rendering, AI, save or multiplayer proof.")


def run_self_tests() -> None:
    # [2026-09-23]_kpopmodder: Inject bounded in-memory faults against immutable-source expectations; never mutate production files.
    current, expected = documents()
    compare_documents(current, expected)
    groups = collect(current)
    added = check_inventory(groups)
    check_projects(groups)
    check_material_cycle(groups)
    caught = []

    def rejects(label, action):
        try:
            action()
        except (ValueError, KeyError, StopIteration):
            caught.append(label)
        else:
            raise ValueError(f"second-wave mutation was not detected: {label}")

    def focus_mutation(identifier, transform):
        tree = one(current[FOCUS_PATH], "focus_tree")
        modified = tuple(Entry(entry.key, entry.op, transform(entry.value)) if entry.key == "focus" and scalar(entry.value, "id") == identifier else entry for entry in tree)
        return {**current, FOCUS_PATH: replace_entry(current[FOCUS_PATH], ("focus_tree",), modified)}

    and_focus = next(identifier for identifier in added if len(children(groups["focus"][identifier], "prerequisite")) == 2)
    first_parent = children(groups["focus"][and_focus], "prerequisite")[0]
    dropped = focus_mutation(and_focus, lambda block: tuple(entry for entry in block if not (entry.key == "prerequisite" and entry.value == first_parent)))
    rejects("missing AND parent", lambda: compare_documents(dropped, expected))
    cyclic = focus_mutation(and_focus, lambda block: replace_entry(block, ("relative_position_id",), and_focus))
    rejects("relative anchor cycle", lambda: check_layout(collect(cyclic)["focus"], added))
    offset = focus_mutation(and_focus, lambda block: block + parse("offset = { x = -84 y = 0 trigger = { always = yes } }"))
    rejects("double inherited political offset", lambda: compare_documents(offset, expected))
    spirit_path = next(relative for relative in current if relative.startswith("common/ideas/"))
    spirit = next(iter(named(one(one(current[spirit_path], "ideas"), "country"))))
    missing_modifier = replace_entry(current[spirit_path], ("ideas", "country", spirit, "modifier"), parse("stability_factor = 9"))
    rejects("spirit reward drift", lambda: compare_documents({**current, spirit_path: missing_modifier}, expected))
    path = "common/decisions/HOK_KOR_manchurian_followup.txt"
    category = next(iter(named(current[path])))
    project = "HOK_KOR_mc_material_recovery_project"
    body = named(one(current[path], category))[project]
    refund = replace_entry(current[path], (category, project, "cancel_effect"), one(body, "cancel_effect") + parse("add_political_power = 150"))
    rejects("cancellation PP refund", lambda: compare_documents({**current, path: refund}, expected))
    dropped_cleanup = replace_entry(current[path], (category, project, "cancel_effect"), ())
    rejects("M3 remaining regional temporary effects", lambda: check_regional_gates(collect({**current, path: dropped_cleanup})))
    wrong_flag = replace_entry(current[path], (category, project, "remove_effect"), parse("set_country_flag = wrong_cooldown"))
    rejects("shared cooldown typo", lambda: compare_documents({**current, path: wrong_flag}, expected))
    for identifier in ("HOK_KOR_yeo_rural_credit_project", "HOK_KOR_pak_current_output_project"):
        body = groups["decision"][identifier]
        mutations = (
            ("factory charge", ("modifier",), one(body, "modifier") + parse("civilian_factory_use = 2")),
            ("factory availability gate", ("available",), one(body, "available") + parse("num_of_civilian_factories_available_for_projects > 1")),
            ("AI factory gate", ("ai_will_do",), one(body, "ai_will_do") + parse("modifier = { factor = 0 NOT = { num_of_civilian_factories_available_for_projects > 5 } }")),
            ("stale political-power cost", ("cost",), "75"),
            ("lost PP AI guard", ("ai_will_do",), parse("factor = 0.5")),
        )
        for label, location, value in mutations:
            changed = {**groups, "decision": {**groups["decision"], identifier: replace_entry(body, location, value)}}
            rejects(f"communist {label}: {identifier}", lambda changed=changed: check_projects(changed))
    stale_state = focus_mutation(and_focus, lambda block: replace_entry(block, ("available",), parse("1031 = { is_owned_by = ROOT }")))
    rejects("obsolete Korean state ID", lambda: compare_documents(stale_state, expected))
    law = focus_mutation("KOR_independent_party_in_power", lambda block: replace_entry(block, ("completion_reward",), one(block, "completion_reward") + parse("add_ideas = partial_economic_mobilisation")))
    rejects("unguarded duplicate partial mobilization", lambda: compare_documents(law, expected))
    downgrade = focus_mutation(and_focus, lambda block: replace_entry(block, ("completion_reward",), one(block, "completion_reward") + parse("add_ideas = HOK_KOR_cmn_export_practice_1")))
    rejects("lower spirit added after upgrade", lambda: compare_documents(downgrade, expected))
    fragment = focus_mutation("HOK_KOR_hw_provincial_inventory", lambda block: replace_entry(block, ("available", "OR"),
                              parse("AND = { owns_state = 941 has_full_control_of_state = 941 }")))
    rejects("H stronghold accepts one split fragment", lambda: check_regional_gates(collect(fragment)))
    local = localisation_payloads()
    first = next(iter(local))
    missing_key = {**local, first: local[first].split(b"\n", 1)[0] + b"\n"}
    rejects("missing one language key", lambda: check_localisation(missing_key, groups, added))
    rejects("DDS exact-case mismatch", lambda: exact_case("gfx/interface/goals/HOK_KOR/Missing.dds", {Path(path).as_posix() for path in SECOND_WAVE_ASSET_PATHS}))
    rejects("missing local DDS", lambda: check_assets(groups, added, {}))
    #20261003_kpopmodder: Reject lifecycle and preservation regressions using bounded in-memory material-cycle mutations.
    emergency = groups["decision"][MATERIAL_DECISION]
    material_mutations = (
        ("active reuse", ("available",), parse(
            f"has_completed_focus = {MATERIAL_FOCUS} has_idea = {MATERIAL_TIERS[1]} has_civil_war = no has_capitulated = no")),
        ("double charge", ("complete_effect",), one(emergency, "complete_effect") + parse("add_political_power = -150")),
        ("stacked boost", ("complete_effect",), one(emergency, "complete_effect") + one(emergency, "complete_effect")),
        ("wrong cost", ("cost",), "75"),
        ("wrong duration", ("days_remove",), "45"),
        ("post-expiry cooldown", ("days_re_enable",), "90"),
        ("permanent-II cleanup", ("remove_effect",), parse(f"remove_ideas = {MATERIAL_TIERS[1]}")),
        ("persistent shared flag", ("cancel_effect",), one(emergency, "cancel_effect") + parse("set_country_flag = material_cycle_busy")),
    )
    for label, location, value in material_mutations:
        changed = {**groups, "decision": {**groups["decision"], MATERIAL_DECISION: replace_entry(emergency, location, value)}}
        rejects(f"material-cycle {label}", lambda changed=changed: check_material_cycle(changed))
    charged = {**groups, "decision": {**groups["decision"], MATERIAL_DECISION: emergency + parse("modifier = { civilian_factory_use = 2 }")}}
    rejects("material-cycle factory charge", lambda: check_material_cycle(charged))
    changed_ideas = {**groups, "idea": {**groups["idea"], MATERIAL_TIERS[1]: replace_entry(
        groups["idea"][MATERIAL_TIERS[1]], ("modifier",), parse("local_resources_factor = 0.9 production_lack_of_resource_penalty_factor = -0.9"))}}
    rejects("material-cycle permanent tier stacks emergency value", lambda: check_material_cycle(changed_ideas))
    locale = MATERIAL_LOCALES[0]
    missing_material_key = {**local, locale: re.sub(
        rb"(?m)^ " + MATERIAL_BOOST.encode() + rb"_desc:[^\r\n]*\r?\n?", b"", local[locale])}
    rejects("material-cycle temporary spirit description removed", lambda: check_material_cycle(groups, missing_material_key))
    print(f"PASS second-wave mutation self-test: {len(caught)} regressions rejected; immutable-source positive fixture accepted; no production writes")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        run_self_tests() if args.self_test else run_checks()
    except (OSError, UnicodeError, ValueError, KeyError, StopIteration) as exc:
        print(f"ERROR Korean second-wave contract: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
