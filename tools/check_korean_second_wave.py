#!/usr/bin/env python3
"""Read-only contracts for the pinned 134-focus second wave; no engine proof."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
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
    git_command, prose_update_lock, read_prose_source,
    focus_tooltip_update_lock, remove_focus_tooltip_update,
    prerequisite_update_lock, remove_focus_prerequisite_update,
    royal_update_lock, remove_royal_update,
    CIVIC_UPDATE_RUNTIME_PATHS, civic_update_lock, read_civic_source, remove_civic_update,
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


#20261003_kpopmodder: Keep the prose import bounded to the fourteen reviewed module pairs and six protected descriptions.
PROSE_CHANGED_COUNTS = {
    "industry_expansion": 16, "military_expansion": 10, "democratic_expansion": 14,
    "communist_policy": 13, "communist_governance": 9, "communist_development": 8,
    "fascist_procurement": 5, "fascist_staff": 2, "fascist_mobilization": 3,
    "fascist_followup": 8, "constitutional_followup": 7, "royal_followup": 15,
    "common_followup": 9, "manchurian_followup": 5,
}
PROSE_PATHS = frozenset(
    f"localisation/{language}/HOK_KOR_{module}_l_{language}.yml"
    for language in ("english", "korean") for module in PROSE_CHANGED_COUNTS
)
PROSE_PROTECTED = frozenset(identifier + "_desc" for identifier in (
    *MATERIAL_TIERS, MATERIAL_BOOST, MATERIAL_DECISION,
    "HOK_KOR_rapid_repairs_spirit", "HOK_KOR_air_maintenance_spirit",
))
PROSE_NOTE = "#20261003_kpopmodder: Explain new decision and spirit policies through concrete circumstances; preserve gameplay and lifecycle rules."
PROSE_TONE_NOTE = "#20261003_kpopmodder: Apply varied HOI4 fascist and communist voices to description narrative; preserve effects and explicit rules."
PROSE_COAST_NOTE = "#20261003_kpopmodder: Clarify Gyeongsang coastal-state wording without changing construction requirements."
PROSE_TONE_MODULES = frozenset((
    "communist_policy", "communist_governance", "communist_development",
    "fascist_procurement", "fascist_staff", "fascist_mobilization", "fascist_followup",
))
PROSE_ROW = re.compile(rb'([ \t]+(?P<key>[A-Za-z0-9_.-]+):(?P<version>\d+) ")(?P<value>(?:[^"\\\r\n]|\\.)*)("[ \t]*)')

#20261010_kpopmodder: Audit only the six frozen prerequisite edits; retain later policy gates and every unrelated focus field.
PREREQUISITE_MINING = "HOK_KOR_cmn_ore_classification"
PREREQUISITE_REMOVALS = {
    "HOK_KOR_cmn_export_invoices": "KOR_support_light_industry_export",
    "HOK_KOR_cm_court_clerks": "KOR_reaffirming_the_independence_of_the_judiciary",
    "HOK_KOR_cm_public_patronage": "KOR_modern_sejong_the_great",
    "HOK_KOR_nrsc_military_administration": "KOR_korea_reigns_above_the_world",
    "HOK_KOR_nrsc_interservice_liaison": "KOR_prussia_in_the_far_east",
}
PREREQUISITE_IDS = frozenset((PREREQUISITE_MINING, *PREREQUISITE_REMOVALS))
PREREQUISITE_PARENTS = {
    PREREQUISITE_MINING: ("KOR_develop_unsan_gold_mine", "KOR_hamgyeong_underground_resources"),
    "HOK_KOR_cmn_export_invoices": ("KOR_devalue_the_won",),
    "HOK_KOR_cm_court_clerks": ("KOR_nomination_prime_minister",),
    "HOK_KOR_cm_public_patronage": ("KOR_nomination_prime_minister",),
    "HOK_KOR_nrsc_military_administration": ("HOK_KOR_nrsc_staff_regulations",),
    "HOK_KOR_nrsc_interservice_liaison": ("KOR_empowering_the_nrsc",),
}
PREREQUISITE_AVAILABLE = {
    PREREQUISITE_MINING: "has_civil_war = no",
    "HOK_KOR_cmn_export_invoices": "has_civil_war = no",
    "HOK_KOR_cm_court_clerks": "has_government = democratic has_civil_war = no has_completed_focus = KOR_nomination_prime_minister",
    "HOK_KOR_cm_public_patronage": "has_government = democratic has_civil_war = no has_completed_focus = KOR_nomination_prime_minister",
    "HOK_KOR_nrsc_military_administration": "has_government = fascism has_civil_war = no has_completed_focus = KOR_establishment_of_the_national_salvation_army any_controlled_state = { NOT = { is_core_of = ROOT } is_fully_controlled_by = ROOT }",
    "HOK_KOR_nrsc_interservice_liaison": "has_government = fascism has_civil_war = no has_completed_focus = KOR_establishment_of_the_national_salvation_army",
}
PREREQUISITE_LATER_GATES = {
    "KOR_korea_reigns_above_the_world": (
        "HOK_KOR_nrsc_civil_supply_offices", "HOK_KOR_nrsc_claims_accounts", "HOK_KOR_nrsc_civil_administration_rules",
    ),
    "KOR_prussia_in_the_far_east": (
        "HOK_KOR_nrsc_joint_logistics_board", "HOK_KOR_nrsc_joint_dispatch_records", "HOK_KOR_nrsc_service_supply_rules",
    ),
}


def focus_prerequisite_contract(block: Block) -> Block:
    """Reconstruct the reviewed edit in ordered AST form, independently of the text builder."""
    identifier = scalar(block, "id")
    if identifier not in PREREQUISITE_IDS:
        return block
    removed = ("KOR_hamgyeong_underground_resources" if identifier == PREREQUISITE_MINING
               else PREREQUISITE_REMOVALS[identifier])
    gate = one(block, "available")
    require(sum(entry == Entry("has_completed_focus", "=", removed) for entry in gate) == 1,
            f"prerequisite update baseline gate missing or duplicated: {identifier}")
    body = replace_entry(block, ("available",), tuple(
        entry for entry in gate if entry != Entry("has_completed_focus", "=", removed)))
    if identifier == PREREQUISITE_MINING:
        require(children(body, "prerequisite") == [parse("focus = KOR_develop_unsan_gold_mine")],
                "prerequisite update mining baseline changed")
        body = tuple(item for entry in body for item in (
            (entry, Entry("prerequisite", "=", parse("focus = KOR_hamgyeong_underground_resources")))
            if entry.key == "prerequisite" else (entry,)))
    return body

#20261010_kpopmodder: Keep the new royal gate, supply-anchor and courier-lifetime delta independent of prior source contracts.
ROYAL_IDEA_PATH = "common/ideas/HOK_KOR_royal_followup.txt"
ROYAL_AM_IDS = tuple("HOK_KOR_am_" + suffix for suffix in (
    "petition_calendar", "granary_ledgers", "relief_dispatches", "regimental_returns",
    "nco_examinations", "reserve_cadre", "mobilization_review", "technical_memorials",
    "civil_service_practicum", "merit_registers",
))
ROYAL_H2_IDS = tuple("HOK_KOR_hw_" + suffix for suffix in (
    "dispatch_codes", "courier_relays", "signal_logs", "relay_exercises",
))
ROYAL_REMOVALS = {
    identifier: ("KOR_reconstruction_confusian_order",) +
    (("KOR_reform_military",) if identifier == "HOK_KOR_am_regimental_returns" else
     ("KOR_revive_bibyeonsa",) if identifier == "HOK_KOR_am_technical_memorials" else ())
    for identifier in ROYAL_AM_IDS
}
ROYAL_REMOVALS.update({identifier: ("KOR_empire_of_hwan",) for identifier in ROYAL_H2_IDS})
ROYAL_SUPPLY_ROOT = "HOK_KOR_hw_provincial_inventory"
ROYAL_SUPPLY_OFFSETS = {
    ROYAL_SUPPLY_ROOT: (0, 0), "HOK_KOR_hw_provision_accounts": (-1, 1),
    "HOK_KOR_hw_inspection_circuits": (1, 1), "HOK_KOR_hw_supply_returns": (0, 2),
}
ROYAL_FOCUS_IDS = frozenset((*ROYAL_REMOVALS, ROYAL_SUPPLY_ROOT))
ROYAL_COURIER_IDEAS = tuple("HOK_KOR_hw_courier_service_" + str(tier) for tier in (1, 2))
ROYAL_OFFSET_ROOT = "KOR_urihwangsilsaranghoe"


def royal_focus_contract(block: Block, *, reverse: bool = False) -> Block:
    """Apply or reverse only the reviewed ordered-AST royal fields; retain all state scopes."""
    identifier = scalar(block, "id")
    if identifier in ROYAL_REMOVALS:
        removed = tuple(Entry("has_completed_focus", "=", value) for value in ROYAL_REMOVALS[identifier])
        gate = one(block, "available")
        if reverse:
            require(not any(entry in gate for entry in removed), f"royal removed gate unexpectedly retained: {identifier}")
            anchor = Entry("has_civil_war", "=", "no") if identifier in ROYAL_AM_IDS else Entry("is_subject", "=", "no")
            require(gate.count(anchor) == 1, f"royal retained availability anchor missing: {identifier}")
            gate = tuple(item for entry in gate for item in ((entry, *removed) if entry == anchor else (entry,)))
        else:
            require(all(gate.count(entry) == 1 for entry in removed), f"royal baseline completion gate changed: {identifier}")
            gate = tuple(entry for entry in gate if entry not in removed)
        block = replace_entry(block, ("available",), gate)
    if identifier == ROYAL_SUPPLY_ROOT:
        old_parent, new_parent = ("KOR_empire_of_hwan", "KOR_return_of_the_king") if reverse else ("KOR_return_of_the_king", "KOR_empire_of_hwan")
        old_x, new_x = ("6", "25") if reverse else ("25", "6")
        require(scalar(block, "relative_position_id") == old_parent and scalar(block, "x") == old_x
                and scalar(block, "y") == "1" and children(block, "prerequisite") == [parse(f"focus = {old_parent}")],
                "royal supply-root ancestor or layout fields changed")
        block = replace_entry(replace_entry(replace_entry(block, ("relative_position_id",), new_parent),
                                            ("x",), new_x), ("prerequisite",), parse(f"focus = {new_parent}"))
    return block


def royal_idea_contract(identifier: str, block: Block) -> Block:
    if identifier not in ROYAL_COURIER_IDEAS:
        return block
    require(one(block, "cancel") == parse("NOT = { has_completed_focus = KOR_empire_of_hwan }"),
            f"royal courier baseline lifetime changed: {identifier}")
    return replace_entry(block, ("cancel",), None)



def runtime_paths() -> tuple[str, ...]:
    return tuple(dict.fromkeys((*SECOND_WAVE_RUNTIME_PATHS, *material_cycle_lock()["runtime_text"])))


def previous_prose_source(relative: str) -> bytes:
    if relative in material_cycle_lock()["runtime_text"]:
        return read_material_cycle_source(relative)
    #20260926_kpopmodder: Compare the revised prose against its own immutable source before regional adaptation.
    if relative in localisation_update_lock()["runtime_text"]:
        return read_localisation_source(relative)
    return read_policy_source(relative) if relative in policy_update_lock()["runtime_text"] else read_second_wave_source(relative)


def selected_source(relative: str) -> bytes:
    if relative in prose_update_lock()["runtime_text"]:
        return read_prose_source(relative)
    return previous_prose_source(relative)


def expected_payload(relative: str) -> bytes:
    from korean_second_wave_geography import apply_second_wave_geography
    data = selected_source(relative)
    if relative == FOCUS_PATH:
        data = apply_post_migration_fixes(relative, replace_tokens(data, {**PROVINCE_ID_MAP, **STATE_ID_MAP}))
    if relative.endswith(".gfx"):
        data = data.replace(DONOR_OVERLAY.encode(), SHINE_OVERLAY.encode())
    return apply_second_wave_geography(relative, data)


def expected_script(relative: str, *, prerequisite_update: bool = True, royal_update: bool = True) -> Block:
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
        #20261005_kpopmodder: Add only the frozen decision notice to the independent ordered focus contract.
        tooltip = focus_tooltip_update_lock()
        require((tooltip["path"], tooltip["focus_id"], tooltip["decision_id"]) ==
                (FOCUS_PATH, MATERIAL_FOCUS, MATERIAL_DECISION), "unreviewed focus-tooltip overlay target")
        tree = []
        for entry in one(source, "focus_tree"):
            if entry.key == "focus" and isinstance(entry.value, tuple):
                identifier = scalar(entry.value, "id")
                body = policy(entry.value) if identifier in FOCUS_IDS else stronghold(entry.value) if identifier in HW_FOCUS_IDS else entry.value
                if identifier == MATERIAL_FOCUS:
                    body = replace_entry(body, ("completion_reward",), one(body, "completion_reward") +
                                         (Entry("unlock_decision_tooltip", "=", MATERIAL_DECISION),))
                #20261010_kpopmodder: Layer the six entry edits after the independent geography and decision-notice contracts.
                if prerequisite_update:
                    body = focus_prerequisite_contract(body)
                #20261010_kpopmodder: Apply the reviewed royal delta after retaining every earlier gameplay and geography layer.
                if royal_update:
                    body = royal_focus_contract(body)
                tree.append(Entry(entry.key, entry.op, body))
            else:
                tree.append(entry)
        return replace_entry(source, ("focus_tree",), tuple(tree))
    if relative == ROYAL_IDEA_PATH and royal_update:
        ideas = one(one(source, "ideas"), "country")
        revised = tuple(Entry(entry.key, entry.op, royal_idea_contract(entry.key, entry.value))
                        if isinstance(entry.value, tuple) else entry for entry in ideas)
        return replace_entry(source, ("ideas", "country"), revised)
    return policy(source) if relative == DECISION_PATH else source


#20261010_kpopmodder: Separate the intentional entry-gate changes from prior rewards, geography, layout and tooltip contracts.
def check_focus_prerequisite_update(groups: dict[str, dict[str, Block]]) -> None:
    lock = prerequisite_update_lock()
    require((lock["path"], lock["source_commit"], lock["base_commit"]) == (
        FOCUS_PATH, "af6fccf2248311c01565c796555ed334ec685015", "062a60287e00ac11352c38bca0fca1ae556e7801"),
        "unreviewed focus-prerequisite source revision or target")
    identifiers = [edit["focus_id"] for edit in lock["edits"]]
    require(len(identifiers) == 6 and set(identifiers) == PREREQUISITE_IDS,
            "focus-prerequisite update must contain exactly the six reviewed focuses")
    base = parse(subprocess.check_output(git_command() + ["cat-file", "blob", lock["base_blob"]]).decode("utf-8-sig"))
    source = parse(subprocess.check_output(git_command() + ["cat-file", "blob", lock["blob"]]).decode("utf-8-sig"))
    tree = tuple(Entry(entry.key, entry.op, focus_prerequisite_contract(entry.value))
                 if entry.key == "focus" and isinstance(entry.value, tuple) else entry
                 for entry in one(base, "focus_tree"))
    require(source == replace_entry(base, ("focus_tree",), tree),
            "donor prerequisite update changed an unrelated field, definition or declaration order")

    #20261010_kpopmodder: Audit the earlier six-focus delta underneath the strictly reversed royal AST layer.
    focuses = {identifier: royal_focus_contract(block, reverse=True) for identifier, block in groups["focus"].items()}
    previous = focus_blocks(expected_script(FOCUS_PATH, prerequisite_update=False, royal_update=False))
    require(list(focuses) == list(previous), "prerequisite update changed focus IDs or declaration order")
    changed = {identifier for identifier in focuses if focuses[identifier] != previous[identifier]}
    require(changed == PREREQUISITE_IDS, f"prerequisite update changed the wrong focuses: {sorted(changed)}")
    for identifier, block in focuses.items():
        require(block == focus_prerequisite_contract(previous[identifier]),
                f"prerequisite update changed unrelated ordered focus fields: {identifier}")
        if identifier not in PREREQUISITE_IDS:
            continue
        unchanged = lambda body: tuple(entry for entry in body if entry.key not in ("prerequisite", "available"))
        require(unchanged(block) == unchanged(previous[identifier]),
                f"prerequisite update changed rewards, timing, layout, AI or lifecycle: {identifier}")
        required = [parse(f"focus = {parent}") for parent in PREREQUISITE_PARENTS[identifier]]
        require(children(block, "prerequisite") == required,
                f"prerequisite update changed parent order or AND grouping: {identifier}")
        require(one(block, "available") == parse(PREREQUISITE_AVAILABLE[identifier]),
                f"prerequisite update removed a retained gate or kept the obsolete entry gate: {identifier}")
        require(all(parent in focuses for parent in PREREQUISITE_PARENTS[identifier]),
                f"prerequisite update references a missing focus: {identifier}")
    # Later occupation and logistics rewards retain their original world/military-first conditions.
    for gate, later in PREREQUISITE_LATER_GATES.items():
        for identifier in later:
            require(one(focuses[identifier], "available") == one(previous[identifier], "available")
                    and Entry("has_completed_focus", "=", gate) in one(focuses[identifier], "available"),
                    f"prerequisite update removed a later policy completion gate: {identifier}/{gate}")

#20261010_kpopmodder: Model relative coordinates and the one inherited royal HIDE offset separately from engine rendering.
def focus_base_positions(focuses: dict[str, Block]) -> dict[str, tuple[float, float]]:
    positions: dict[str, tuple[float, float]] = {}
    visiting: set[str] = set()
    def resolve(identifier: str) -> tuple[float, float]:
        require(identifier in focuses, f"missing royal layout anchor: {identifier}")
        require(identifier not in visiting, f"cyclic royal layout anchor: {identifier}")
        if identifier in positions:
            return positions[identifier]
        visiting.add(identifier)
        block = focuses[identifier]
        anchors = [entry.value for entry in block if entry.key == "relative_position_id"]
        require(len(anchors) <= 1, f"multiple royal layout anchors: {identifier}")
        x, y = float(scalar(block, "x")), float(scalar(block, "y"))
        if anchors:
            parent_x, parent_y = resolve(anchors[0])
            x, y = x + parent_x, y + parent_y
        visiting.remove(identifier)
        positions[identifier] = (x, y)
        return positions[identifier]
    for identifier in focuses:
        resolve(identifier)
    return positions


def check_royal_layout(focuses: dict[str, Block], previous: dict[str, Block]) -> None:
    require(len(focuses) == len(previous) == 460 and list(focuses) == list(previous),
            "royal layout must preserve all 460 IDs and declaration order")
    check_layout(focuses, set(ROYAL_FOCUS_IDS))
    before, positions = focus_base_positions(previous), focus_base_positions(focuses)
    moved = {identifier for identifier in positions if positions[identifier] != before[identifier]}
    require(moved == set(ROYAL_SUPPLY_OFFSETS), f"royal layout moved the wrong focuses: {sorted(moved)}")
    empire_x, empire_y = positions["KOR_empire_of_hwan"]
    root = (empire_x + 6, empire_y + 1)
    for identifier, (x, y) in ROYAL_SUPPLY_OFFSETS.items():
        require(positions[identifier] == (root[0] + x, root[1] + y),
                f"royal supply diamond coordinate changed: {identifier}")
        if identifier != ROYAL_SUPPLY_ROOT:
            require(tuple(entry for entry in focuses[identifier] if entry.key in ("relative_position_id", "x", "y")) ==
                    tuple(entry for entry in previous[identifier] if entry.key in ("relative_position_id", "x", "y")),
                    f"royal supply child-local offset changed: {identifier}")
    for identifier in focuses:
        require(children(focuses[identifier], "offset") == children(previous[identifier], "offset"),
                f"royal update changed a conditional offset: {identifier}")
    offset = parse("x = -101 y = 0 trigger = { AND = { has_game_rule = { rule = obsolete_focus_branches_visibility option = HIDE } has_completed_focus = KOR_urihwangsilsaranghoe } }")
    require(children(focuses[ROYAL_OFFSET_ROOT], "offset") == [offset],
            "royal conditional HIDE/completion contract changed")
    affected = set(ROYAL_REMOVALS) | set(ROYAL_SUPPLY_OFFSETS)
    for identifier in affected:
        ancestors, node = [], identifier
        while True:
            require(node not in ancestors, f"cyclic royal offset inheritance: {identifier}")
            ancestors.append(node)
            anchor = [entry.value for entry in focuses[node] if entry.key == "relative_position_id"]
            if not anchor:
                break
            node = anchor[0]
        require([node for node in ancestors if children(focuses[node], "offset")] == [ROYAL_OFFSET_ROOT],
                f"royal branch must inherit the political offset exactly once: {identifier}")
        # These four static cases model the explicit source condition; they are not UI observations.
        for option, completed, displacement in (("SHOW", False, 0), ("SHOW", True, 0),
                                                ("HIDE", False, 0), ("HIDE", True, -101)):
            shifted = tuple(positions[identifier][axis] + sum(
                float(scalar(item, ("x", "y")[axis])) for node in ancestors for item in children(focuses[node], "offset")
                if option == "HIDE" and completed) for axis in (0, 1))
            require(shifted == (positions[identifier][0] + displacement, positions[identifier][1]),
                    f"royal SHOW/HIDE offset applied early, twice or on SHOW: {identifier}/{option}/{completed}")

#20261010_kpopmodder: Keep the maintained coordinate record tied to the actual port ancestor and reconstructed output.
def check_royal_coordinate_spec(focuses: dict[str, Block], previous: dict[str, Block]) -> None:
    spec = json.loads((ROOT / "docs/data/HOK_KOREAN_ROYAL_LAYOUT_COORDINATES.json").read_text(encoding="utf-8"))
    require(spec["schema_version"] == 1 and spec["status"] == "STATIC_SPEC_RUNTIME_UNPROVEN"
            and spec["source"] == FOCUS_PATH and spec["donor_commit"] == "4d8241e3cd33ebbceaca9650ab36b9891a22b56d"
            and spec["count"] == 460 and spec["absolute_anchors"] == 7 and spec["relative_nodes"] == 453,
            "royal coordinate record identity or inventory changed")
    require(spec["baseline_source_sha256"] == royal_update_lock()["runtime_text"][FOCUS_PATH]["previous_output_sha256"],
            "royal coordinate record has the wrong port ancestor")
    nodes = spec["nodes"]
    require([node["id"] for node in nodes] == list(focuses)
            and [node["declaration_order"] for node in nodes] == list(range(460)),
            "royal coordinate record must retain all IDs in declaration order")
    before, after = focus_base_positions(previous), focus_base_positions(focuses)
    for node in nodes:
        identifier = node["id"]
        for label, documents, positions in (("before", previous, before), ("after", focuses, after)):
            body, record = documents[identifier], node[label]
            anchors = [entry.value for entry in body if entry.key == "relative_position_id"]
            require(record["relative_position_id"] == (anchors[0] if anchors else None)
                    and record["script_xy"] == {"x": float(scalar(body, "x")), "y": float(scalar(body, "y"))}
                    and record["base_absolute"] == dict(zip(("x", "y"), positions[identifier]))
                    and record["prerequisite_groups"] == [[entry.value for entry in relation] for relation in children(body, "prerequisite")],
                    f"royal coordinate record differs from the ordered AST: {identifier}/{label}")
        if identifier in set(ROYAL_REMOVALS) | set(ROYAL_SUPPLY_OFFSETS):
            x, y = after[identifier]
            require(node["conditional_positions"] == {"SHOW": {"x": x, "y": y},
                    "HIDE_INITIAL": {"x": x, "y": y}, "HIDE_ROYAL_COMPLETED": {"x": x - 101, "y": y}},
                    f"royal coordinate record misstates conditional political movement: {identifier}")



#20261010_kpopmodder: Verify the new source delta and every unchanged field against an independent ordered-AST ancestor.
def check_royal_update(groups: dict[str, dict[str, Block]]) -> None:
    lock = royal_update_lock()
    require((lock["source_commit"], lock["base_commit"]) == (
        "4d8241e3cd33ebbceaca9650ab36b9891a22b56d", "af6fccf2248311c01565c796555ed334ec685015"),
        "unreviewed royal update source revision")
    require(set(lock["runtime_text"]) == {FOCUS_PATH, ROYAL_IDEA_PATH}, "royal runtime allowlist changed")
    for relative, record in lock["runtime_text"].items():
        base = parse(subprocess.check_output(git_command() + ["cat-file", "blob", record["base_blob"]]).decode("utf-8-sig"))
        source = parse(subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]]).decode("utf-8-sig"))
        identifiers = {edit["id"] for edit in record["edits"]}
        if relative == FOCUS_PATH:
            require(identifiers == ROYAL_FOCUS_IDS, "royal source focus edit inventory changed")
            tree = tuple(Entry(entry.key, entry.op, royal_focus_contract(entry.value))
                         if entry.key == "focus" and isinstance(entry.value, tuple) else entry
                         for entry in one(base, "focus_tree"))
            expected = replace_entry(base, ("focus_tree",), tree)
        else:
            require(identifiers == set(ROYAL_COURIER_IDEAS), "royal source idea edit inventory changed")
            country = tuple(Entry(entry.key, entry.op, royal_idea_contract(entry.key, entry.value))
                            if isinstance(entry.value, tuple) else entry for entry in one(one(base, "ideas"), "country"))
            expected = replace_entry(base, ("ideas", "country"), country)
        require(source == expected, f"royal donor update changed an unreviewed field or declaration order: {relative}")
    require(len(ROYAL_REMOVALS) == 14 and sum(map(len, ROYAL_REMOVALS.values())) == 16,
            "royal update must remove exactly sixteen completion gates in fourteen focuses")
    focuses = groups["focus"]
    previous = focus_blocks(expected_script(FOCUS_PATH, royal_update=False))
    require(list(focuses) == list(previous), "royal update changed focus IDs or declaration order")
    changed = {identifier for identifier in focuses if focuses[identifier] != previous[identifier]}
    require(changed == ROYAL_FOCUS_IDS, f"royal update changed the wrong focuses: {sorted(changed)}")
    for identifier, block in focuses.items():
        require(block == royal_focus_contract(previous[identifier]),
                f"royal update changed rewards, timing, AI, lifecycle, geography or unrelated fields: {identifier}")
        if identifier in ROYAL_AM_IDS:
            require(one(block, "available") == parse("original_tag = KOR has_government = neutrality has_civil_war = no"),
                    f"royal original-tag, neutrality or civil-war gate changed: {identifier}")
        if identifier in ROYAL_H2_IDS:
            require(one(block, "available") == parse("original_tag = KOR has_civil_war = no is_subject = no") +
                    (Entry("OR", "=", one(one(previous[identifier], "available"), "OR")),),
                    f"royal subject, civil-war or whole-region stronghold gate changed: {identifier}")
        if identifier != ROYAL_SUPPLY_ROOT:
            require(children(block, "prerequisite") == children(previous[identifier], "prerequisite"),
                    f"royal internal prerequisite or AND grouping changed: {identifier}")
    check_royal_layout(focuses, previous)
    check_royal_coordinate_spec(focuses, previous)
    previous_ideas = named(one(one(expected_script(ROYAL_IDEA_PATH, royal_update=False), "ideas"), "country"))
    changed_ideas = {identifier for identifier, block in previous_ideas.items() if groups["idea"][identifier] != block}
    require(changed_ideas == set(ROYAL_COURIER_IDEAS), "royal update changed an unrelated national spirit")
    for identifier, block in previous_ideas.items():
        require(groups["idea"][identifier] == royal_idea_contract(identifier, block),
                f"royal idea modifiers, tiers, ownership or unrelated cancellation changed: {identifier}")
    for identifier, reward in zip(ROYAL_COURIER_IDEAS, (
        "initiative_factor = 0.10 army_speed_factor = 0.05",
        "initiative_factor = 0.15 army_speed_factor = 0.10",
    )):
        idea = groups["idea"][identifier]
        require(not any(entry.key == "cancel" for entry in idea) and one(idea, "modifier") == parse(reward),
                f"royal acquired courier tier cancels or has incorrect modifiers: {identifier}")



def documents() -> tuple[dict[str, Block], dict[str, Block]]:
    expected, current = {}, {}
    for path in runtime_paths():
        relative = Path(path).as_posix()
        if Path(relative).suffix not in (".txt", ".gfx"):
            continue
        expected[relative] = expected_script(relative)
        current[relative] = parse(historical_civic_payload(relative, (ROOT / relative).read_bytes()).decode("utf-8-sig"))
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


#20261011_kpopmodder: Recover the exact pre-missile map beneath only the three audited removals and one HOK restoration.
def historical_map_buildings(data: bytes) -> bytes:
    baseline_hash = "839486E33E51AB800BB8930A11AB5F7A9F6C779FE8F9CADB1E54E5D147733841"
    if hashlib.sha256(data).hexdigest().upper() == baseline_hash:
        return data
    rows = data.split(b"\r\n")
    require(not any(b"\r" in row or b"\n" in row for row in rows),
            "missile map overlay changed preserved row endings")
    added = b"918;rocket_site_spawn;4816.00;9.70;1333.00;1.13;0"
    require(rows.count(added) == 1, "missile map overlay must add the canonical HOK Hamgyong row once")
    rows.remove(added)
    removals = (
        (b"527;special_project_facility_spawn;4787.00;12.62;1308.00;3.44;0",
         b"918;rocket_site_spawn;4784.00;12.82;1312.00;5.72;0",
         b"528;steel_mill;4854.00;11.50;1200.00;5.26;0"),
        (b"918;special_project_facility_spawn;4839.00;9.60;1368.00;2.34;0",
         b"918;rocket_site_spawn;4827.00;9.65;1341.00;1.39;0",
         b"918;naval_base_spawn;4839.00;9.50;1365.00;0.64;7028"),
        (b"919;special_project_facility_spawn;4784.00;9.60;1224.00;1.71;0",
         b"1145;rocket_site_spawn;4788.00;9.70;1254.00;2.71;0",
         b"1146;naval_base_spawn;4780.00;9.53;1203.00;1.57;2708"),
    )
    for before, removed, after in removals:
        require(rows.count(before) == rows.count(after) == 1,
                f"missile map overlay changed a unique preservation anchor: {removed!r}")
        require(removed not in rows, f"missile map overlay retained an audited RT56 rocket row: {removed!r}")
        index = rows.index(before)
        require(index + 1 < len(rows) and rows[index + 1] == after,
                f"missile map overlay changed adjacent preserved rows: {removed!r}")
        rows.insert(index + 1, removed)
    historical = b"\r\n".join(rows)
    require(hashlib.sha256(historical).hexdigest().upper() == baseline_hash,
            "missile map overlay changed unrelated preserved building rows")
    return historical

#20261003_kpopmodder: Require the intended permanent rewards and bounded PP-only timed effect independently of frozen-source equality.
def check_material_cycle(groups: dict[str, dict[str, Block]], payloads: dict[str, bytes] | None = None) -> None:
    lock = material_cycle_lock()
    require(set(lock["runtime_text"]) == {MATERIAL_IDEA_PATH, MATERIAL_DECISION_PATH, MATERIAL_CATEGORY_PATH,
                                          MATERIAL_GFX_PATH, *MATERIAL_LOCALES},
            "material-cycle runtime allowlist must remain six text files without map or on_action changes")
    require(set(lock["runtime_assets"]) == set(MATERIAL_SPRITES.values()), "material-cycle artwork allowlist changed")
    require(FOCUS_PATH in lock["preserved_runtime"], "material-cycle update must pin the pre-tooltip focus tree")
    for relative, digest in lock["preserved_runtime"].items():
        #20261010_kpopmodder: Reverse both strict overlays before checking the original material-cycle preservation pins.
        data = historical_civic_payload(relative, (ROOT / relative).read_bytes())
        #20261010_kpopmodder: Recover both the focus and royal-idea ancestors before testing unchanged historical pins.
        if relative in (FOCUS_PATH, ROYAL_IDEA_PATH):
            data = remove_royal_update(relative, data)
        if relative == FOCUS_PATH:
            data = remove_focus_tooltip_update(remove_focus_prerequisite_update(data))
        #20261011_kpopmodder: Preserve immutable historical map pins beneath the narrowly audited missile placement repair.
        if relative == "map/buildings.txt":
            data = historical_map_buildings(data)
        require(hashlib.sha256(data).hexdigest().upper() == digest.upper(),
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
        f"else = {{ add_ideas = {MATERIAL_TIERS[1]} }} unlock_decision_tooltip = {MATERIAL_DECISION}"),
        "material-cycle II must replace I without stacking the lower tier and retain the decision notice")
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

    #20261003_kpopmodder: This historical contract uses the frozen material prose; the newest actual output is checked separately.
    payloads = {relative: read_material_cycle_source(relative) for relative in MATERIAL_LOCALES} if payloads is None else payloads
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


def prose_entries(data: bytes, relative: str) -> list[tuple[str, str, bytes]]:
    language = Path(relative).parts[1]
    require(data.startswith(b"\xef\xbb\xbf" + f"l_{language}:".encode()), f"prose BOM/header drift: {relative}")
    result = []
    for number, line in enumerate(data.replace(b"\r\n", b"\n").splitlines()[1:], 2):
        if not line.strip() or line.lstrip().startswith(b"#"):
            continue
        match = PROSE_ROW.fullmatch(line)
        require(match is not None, f"malformed prose localisation row: {relative}:{number}")
        result.append((match["key"].decode(), match["version"].decode(), match["value"]))
    require(len(result) == len({key for key, _, _ in result}), f"duplicate prose localisation key: {relative}")
    return result


def prose_description_keys() -> set[str]:
    definitions = {kind: set() for kind in ("idea", "decision", "category")}
    for module in PROSE_CHANGED_COUNTS:
        for kind, directory in (("idea", "common/ideas"), ("decision", "common/decisions"),
                                ("category", "common/decisions/categories")):
            path = ROOT / directory / f"HOK_KOR_{module}.txt"
            if not path.exists():
                continue
            block = read(path)
            if kind == "idea":
                identifiers = named(one(one(block, "ideas"), "country"))
            elif kind == "decision":
                identifiers = {identifier: body for category in named(block).values()
                               for identifier, body in named(category).items()}
            else:
                identifiers = named(block)
            require(not definitions[kind] & identifiers.keys(), f"duplicate prose {kind} consumer IDs: {path}")
            definitions[kind].update(identifiers)
    require({kind: len(ids) for kind, ids in definitions.items()} == {"idea": 93, "decision": 29, "category": 8},
            "prose consumers must remain 93 country ideas, 29 decisions and eight categories")
    descriptions = {identifier + "_desc" for ids in definitions.values() for identifier in ids}
    require(len(descriptions) == 130 and PROSE_PROTECTED <= descriptions,
            "prose consumer namespace or protected descriptions changed")
    return descriptions - PROSE_PROTECTED


def check_prose_update(payloads: dict[str, bytes] | None = None) -> None:
    from korean_second_wave_geography import apply_second_wave_geography
    lock = prose_update_lock()
    require(lock["base_commit"] == "43dbb38ac2553942e898e6093a2a46f0430995fc",
            "prose donor baseline must remain immutable 43dbb38")
    require(set(lock["runtime_text"]) == PROSE_PATHS, "prose update must remain the explicit fourteen localisation pairs")
    require(lock["changed_descriptions_per_channel"] == {"english": 124, "korean": 124},
            "prose update count metadata changed")
    preserved = lock["preserved_runtime"]
    require({FOCUS_PATH, MATERIAL_IDEA_PATH, MATERIAL_DECISION_PATH, MATERIAL_CATEGORY_PATH, MATERIAL_GFX_PATH,
             "descriptor.mod"} <= preserved.keys(), "prose import lacks required unchanged gameplay/presentation pins")
    require(not PROSE_PATHS & preserved.keys(), "prose preserved-runtime pins include approved description outputs")
    for relative, digest in preserved.items():
        #20261005_kpopmodder: Preserve the prose import's historical pins underneath the later decision notice.
        #20261010_kpopmodder: Reverse the six prerequisite edits before applying the historical tooltip reversal.
        data = historical_civic_payload(relative, (ROOT / relative).read_bytes())
        #20261010_kpopmodder: Recover both the focus and royal-idea ancestors before testing unchanged historical pins.
        if relative in (FOCUS_PATH, ROYAL_IDEA_PATH):
            data = remove_royal_update(relative, data)
        if relative == FOCUS_PATH:
            data = remove_focus_tooltip_update(remove_focus_prerequisite_update(data))
        #20261011_kpopmodder: Preserve immutable historical map pins beneath the narrowly audited missile placement repair.
        if relative == "map/buildings.txt":
            data = historical_map_buildings(data)
        require(hashlib.sha256(data).hexdigest().upper() == digest.upper(),
                f"prose update changed preserved gameplay/presentation: {relative}")
    allowed = prose_description_keys()
    payloads = {relative: (ROOT / relative).read_bytes() for relative in PROSE_PATHS} if payloads is None else payloads
    require(set(payloads) == PROSE_PATHS, "actual prose localisation inventory changed")
    changed_by_language = {language: set() for language in ("english", "korean")}
    for relative, record in lock["runtime_text"].items():
        language = Path(relative).parts[1]
        module = Path(relative).name.removeprefix("HOK_KOR_").removesuffix(f"_l_{language}.yml")
        source = read_prose_source(relative)
        base = subprocess.check_output(git_command() + ["cat-file", "blob", record["base_blob"]])
        previous = previous_prose_source(relative)
        require(base.replace(b"\r\n", b"\n") == previous.replace(b"\r\n", b"\n"),
                f"prose donor baseline differs from the previously imported content: {relative}")
        previous_output = apply_second_wave_geography(relative, previous)
        require(hashlib.sha256(previous_output).hexdigest().upper() == record["previous_output_sha256"].upper(),
                f"prose previous port-output provenance drift: {relative}")
        old_entries, entries = prose_entries(base, relative), prose_entries(source, relative)
        require([(key, version) for key, version, _ in entries] == [(key, version) for key, version, _ in old_entries],
                f"prose key/version/order drift: {relative}")
        old_values, values = {key: value for key, _, value in old_entries}, {key: value for key, _, value in entries}
        changed = {key for key in values if values[key] != old_values[key]}
        require(len(changed) == PROSE_CHANGED_COUNTS[module] and changed == set(record["changed_description_keys"]),
                f"prose description change inventory drift: {relative}: {sorted(changed)}")
        require(changed <= allowed and not changed & PROSE_PROTECTED,
                f"prose touched a name, focus, event, tooltip or protected description: {relative}: {sorted(changed - allowed)}")
        require(not changed_by_language[language] & changed, f"prose changed key appears in multiple modules: {relative}")
        changed_by_language[language].update(changed)
        notes = ([PROSE_COAST_NOTE] if module == "industry_expansion" else [])
        notes += ([PROSE_TONE_NOTE] if module in PROSE_TONE_MODULES else []) + [PROSE_NOTE]
        lines = source.replace(b"\r\n", b"\n").splitlines()
        require(lines[1:1 + len(notes)] == [note.encode() for note in notes],
                f"prose contributor notes missing or displaced: {relative}")
        without_notes = [lines[0], *lines[1 + len(notes):]]
        def unchanged_lines(rows: list[bytes]) -> list[bytes]:
            result = []
            for line in rows:
                match = PROSE_ROW.fullmatch(line)
                if match and match["key"].decode() in changed:
                    line = match[1] + b"<reviewed-description>" + match[5]
                result.append(line)
            return result
        require(unchanged_lines(without_notes) == unchanged_lines(base.replace(b"\r\n", b"\n").splitlines()),
                f"prose changed text, comments or formatting outside reviewed description values: {relative}")
        previous_values = {key: value for key, _, value in prose_entries(previous_output, relative)}
        actual = payloads[relative]
        require(actual == apply_second_wave_geography(relative, source),
                f"actual prose differs from frozen source/ADR-0005 region contract: {relative}")
        actual_values = {key: value for key, _, value in prose_entries(actual, relative)}
        for key in PROSE_PROTECTED & previous_values.keys():
            require(actual_values[key] == previous_values[key], f"prose changed a protected existing description: {relative}/{key}")
        if language == "english":
            counterpart = relative.replace("/english/", "/korean/").replace("_l_english.yml", "_l_korean.yml")
            require(source.decode("utf-8-sig").splitlines()[1:] == read_prose_source(counterpart).decode("utf-8-sig").splitlines()[1:],
                    f"frozen prose language bodies diverged: {relative}")
            require(actual.decode("utf-8-sig").splitlines()[1:] == payloads[counterpart].decode("utf-8-sig").splitlines()[1:],
                    f"actual prose language bodies diverged: {relative}")
    require(all(keys == allowed for keys in changed_by_language.values()) and len(allowed) == 124,
            "prose import must change exactly the same 124 permitted descriptions in both channels")


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



#20261012_kpopmodder: Validate the complete civic source layer separately, recovering strict ancestors for all historical contracts.
CIVIC_DECISIONS = "common/decisions/HOK_KOR_civic_decisions.txt"
CIVIC_IDEAS = "common/ideas/HOK_KOR_civic_ideas.txt"
CIVIC_EFFECTS = "common/scripted_effects/HOK_KOR_civic_effects.txt"
CIVIC_TRIGGERS = "common/scripted_triggers/HOK_KOR_civic_triggers.txt"
CIVIC_ACTIONS = "common/on_actions/HOK_KOR_civic_on_actions.txt"
CIVIC_EVENTS = "events/HOK_KOR_civic_events.txt"
CIVIC_INLAY = "common/focus_inlay_windows/HOK_KOR_civic_influence_inlay_window.txt"
CIVIC_GUI = "interface/HOK_KOR_civic_influence.gui"
CIVIC_LEGACY = "common/national_focus/HOK_KOR_civic_legacy_focus.txt"
CIVIC_REMOVED = "KOR_cooperation_with_the_jaebeol"
CIVIC_FOCUS_IDS = frozenset("HOK_KOR_civic_" + suffix for suffix in (
    "industrial_compact", "chaebol_cooperation", "nationalization", "break_monopolies",
    "sunkyong_investment", "samsung_electronics", "goldstar_mass_production", "labor_compact",
    "mass_conscription", "public_accountability", "social_settlement", "public_procurement", "procurement_inspections",
))
CIVIC_VARIABLES = ("HOK_KOR_chaebol_influence", "HOK_KOR_civic_influence",
                   "HOK_KOR_procurement_corruption", "HOK_KOR_institutional_capture")
CIVIC_POLICIES = ("HOK_KOR_policy_cooperation", "HOK_KOR_policy_civic_reform", "HOK_KOR_policy_public_ownership")
CIVIC_BUTTONS = tuple("HOK_KOR_" + suffix for suffix in ("support_chaebol", "suppress_chaebol", "support_civic", "suppress_civic"))


def historical_civic_payload(relative: str, data: bytes) -> bytes:
    record = civic_update_lock()["runtime_text"].get(relative, {})
    return remove_civic_update(relative, data) if "previous_output_sha256" in record else data


def civic_documents() -> tuple[dict[str, bytes], dict[str, Block]]:
    payloads = {relative: (ROOT / relative).read_bytes() for relative in CIVIC_UPDATE_RUNTIME_PATHS}
    return payloads, {relative: parse(data.decode("utf-8-sig")) for relative, data in payloads.items()
                      if Path(relative).suffix in (".txt", ".gfx", ".gui")}


def civic_expected_payload(relative: str, data: bytes) -> bytes:
    """Reconstruct reviewed hunks independently of the production apply helper."""
    record = civic_update_lock()["runtime_text"].get(relative, civic_update_lock()["runtime_assets"].get(relative))
    if "previous_output_sha256" in record:
        ancestor = remove_civic_update(relative, data)
        if relative == FOCUS_PATH:
            require(parse(ancestor.decode("utf-8-sig")) == expected_script(relative),
                    "civic overlay changed the historical ordered focus ancestor")
        result = ancestor
        newline = b"\r\n" if b"\r\n" in ancestor else b"\n"
        for edit in record["edits"]:
            before = ("\n".join(edit["before_lines"]) + "\n").encode().replace(b"\n", newline)
            after = ("\n".join(edit["after_lines"]) + "\n").encode().replace(b"\n", newline)
            require(before and result.count(before) == 1, f"civic hunk anchor missing or duplicated: {relative}")
            result = result.replace(before, after, 1)
        return result
    result = read_civic_source(relative)
    for edit in record.get("transformations", ()):
        before, after = edit["before"].encode(), edit["after"].encode()
        require(result.count(before) == edit["count"], f"civic transformation source count changed: {relative}")
        result = result.replace(before, after)
    return result


def check_civic_source(payloads: dict[str, bytes], documents: dict[str, Block]) -> None:
    lock = civic_update_lock()
    records = {**lock["runtime_text"], **lock["runtime_assets"]}
    require(len(lock["runtime_text"]) == 23 and len(lock["runtime_assets"]) == 8
            and len(records) == 31 and set(payloads) == set(records), "civic 23-text/8-asset source allowlist changed")
    require({path for path, row in lock["runtime_text"].items() if "previous_output_sha256" in row}
            == {FOCUS_PATH, "common/decisions/KOR_decision.txt"}, "civic existing-file delta changed")
    expected_docs = {}
    for relative, data in payloads.items():
        require(hashlib.sha256(data).hexdigest().upper() == records[relative]["output_sha256"],
                f"civic pinned output differs: {relative}")
        expected = civic_expected_payload(relative, data)
        require(data == expected, f"civic complete immutable source delta differs: {relative}")
        if Path(relative).suffix in (".txt", ".gfx", ".gui"):
            expected_docs[relative] = parse(expected.decode("utf-8-sig"))
    # Every historical generated output and the three separately shipped sources stay byte-exact.
    for relative, digest in {**lock["preserved_outputs"], **lock["preserved_runtime"]}.items():
        require(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest().upper() == digest,
                f"civic update changed an unselected output: {relative}")
    require(documents.keys() == expected_docs.keys(), "civic ordered script inventory changed")
    for relative, expected in expected_docs.items():
        require(documents[relative] == expected, f"civic entire ordered AST differs: {relative}")


def civic_flat_decisions(document: Block) -> dict[str, Block]:
    result = {}
    for category in named(document).values():
        definitions = named(category)
        require(not result.keys() & definitions.keys(), "duplicate civic decision ID")
        result.update(definitions)
    return result


def check_civic_semantics(documents: dict[str, Block]) -> None:
    focuses = focus_blocks(documents[FOCUS_PATH])
    require(len(focuses) == 472 and CIVIC_FOCUS_IDS <= focuses.keys() and CIVIC_REMOVED not in focuses,
            "civic tree must contain 472 playable IDs, thirteen civic additions and no legacy cooperation node")
    tree = one(documents[FOCUS_PATH], "focus_tree")
    require(not children(tree, "shared_focus"), "legacy shared focus was imported into the playable tree")
    legacy = one(documents[CIVIC_LEGACY], "shared_focus")
    require(scalar(legacy, "id") == CIVIC_REMOVED and one(legacy, "available") == parse("always = no")
            and one(legacy, "ai_will_do") == parse("factor = 0") and one(legacy, "completion_reward") == (),
            "legacy focus lookup must remain registered, unavailable and reward-free")
    for identifier in CIVIC_FOCUS_IDS:
        focus = focuses[identifier]
        require(scalar(focus, "cost") == "5" and scalar(focus, "cancel_if_invalid") == "yes"
                and scalar(focus, "continue_if_invalid") == "no" and scalar(focus, "available_if_capitulated") == "no",
                f"civic 35-day cancellation contract changed: {identifier}")
        require(one(focus, "ai_will_do") and scalar(one(focus, "ai_will_do"), "factor") == "2",
                f"civic base AI weight changed: {identifier}")
        for entry in walk(focus):
            if entry.key in ("focus", "relative_position_id") and isinstance(entry.value, str):
                require(entry.value in focuses, f"unresolved civic focus link: {identifier}/{entry.value}")
    policy_focuses = {"HOK_KOR_civic_" + suffix for suffix in ("chaebol_cooperation", "nationalization", "break_monopolies")}
    for identifier in policy_focuses:
        excluded = {entry.value for entry in one(focuses[identifier], "mutually_exclusive") if entry.key == "focus"}
        require(excluded == policy_focuses - {identifier}, f"civic policy mutual exclusion changed: {identifier}")
    require(one(focuses["HOK_KOR_civic_industrial_compact"], "prerequisite")
            == parse("focus = KOR_liberal_party_sole_power focus = KOR_independent_party_in_power"),
            "civic democratic entry OR prerequisite changed")
    require(one(one(tree, "inlay_window"), "position") == parse("x = 1050 y = 1400")
            and scalar(one(tree, "inlay_window"), "id") == "HOK_KOR_civic_influence_inlay_window",
            "civic inlay placement/registration changed")
    effects = named(documents[CIVIC_EFFECTS])
    require(len(effects) == 18, "civic helper inventory changed")
    seed = one(effects["HOK_KOR_initialize_civic_system"], "if")
    require(one(seed, "limit") == parse("tag = KOR NOT = { has_country_flag = HOK_KOR_civic_system_initialized }"),
            "civic initialization lost its Korean once-only guard")
    require(children(seed, "set_variable") == [parse(f"{variable} = {value}")
            for variable, value in zip(CIVIC_VARIABLES, (60, 35, 20, 40))], "civic independent seed values changed")
    require(scalar(seed, "set_country_flag") == "HOK_KOR_civic_system_initialized"
            and scalar(seed, "HOK_KOR_sync_civic_state") == "yes", "civic initialization lifecycle changed")
    sync = effects["HOK_KOR_sync_civic_state"]
    require(children(sync, "clamp_variable") == [parse(f"var = {variable} min = 0 max = 100") for variable in CIVIC_VARIABLES],
            "civic four-variable 0..100 clamp changed")
    for faction in ("chaebol", "civic"):
        variable = f"HOK_KOR_{faction}_influence"
        branches = [entry.value for entry in sync if entry.key in ("if", "else_if") and isinstance(entry.value, tuple)
                    and any(item.key == "check_variable" and isinstance(item.value, tuple)
                            and scalar(item.value, "var") == variable for item in one(entry.value, "limit"))]
        require(len(branches) == 3, f"civic influence tier branch count changed: {faction}")
        for branch, threshold, tier in zip(branches, (75, 50, 25), ("dominant", "interfering", "established")):
            require(one(branch, "limit") == parse(f"check_variable = {{ var = {variable} value = {threshold} compare = greater_than_or_equals }}"),
                    f"civic tier threshold/order changed: {faction}/{tier}")
            ideas = {entry.value for entry in walk(branch) if entry.key == "add_ideas"}
            removed = {entry.value for entry in branch if entry.key == "remove_ideas"}
            require(ideas == {f"HOK_KOR_{faction}_{tier}"} and removed == {f"HOK_KOR_{faction}_{other}"
                    for other in ("dominant", "interfering", "established") if other != tier},
                    f"civic influence tier stacking changed: {faction}/{tier}")
    corruption_branches = [entry.value for entry in sync if entry.key in ("if", "else_if")
                           and isinstance(entry.value, tuple) and any(item.key == "check_variable"
                           and isinstance(item.value, tuple) and scalar(item.value, "var") == CIVIC_VARIABLES[2]
                           for item in one(entry.value, "limit"))]
    require([scalar(one(one(branch, "limit"), "check_variable"), "value") for branch in corruption_branches] == ["70", "40"],
            "civic corruption severe/moderate threshold order changed")
    for helper, selected in zip(("chaebol_cooperation", "civic_reform", "public_ownership"), CIVIC_POLICIES):
        choice = one(effects["HOK_KOR_select_" + helper], "if")
        require(one(choice, "limit") == parse("tag = KOR")
                and [entry.value for entry in choice if entry.key == "clr_country_flag"] == list(CIVIC_POLICIES)
                and selected in [entry.value for entry in choice if entry.key == "set_country_flag"],
                f"civic saved policy replacement changed: {helper}")
    actions = one(documents[CIVIC_ACTIONS], "on_actions")
    require([entry.key for entry in actions] == ["on_startup", "on_monthly_KOR"], "civic callback cadence changed")
    for callback, helper in (("on_startup", "HOK_KOR_register_legacy_civic_state"), ("on_monthly_KOR", "HOK_KOR_monthly_civic_update")):
        require(one(one(actions, callback), "effect") == parse(f"KOR = {{ {helper} = yes }}"),
                f"civic callback lost explicit Korean country scope: {callback}")
    registry = effects["HOK_KOR_register_legacy_civic_state"]
    require(registry[0] == Entry("HOK_KOR_initialize_civic_system", "=", "yes"), "legacy registration must initialize first")
    require({entry.value for entry in walk(registry) if entry.key == "has_completed_focus"}
            == {CIVIC_REMOVED, "HOK_KOR_civic_chaebol_cooperation", "KOR_taming_the_jaebeol", "KOR_confiscation_of_chaebol_assets"},
            "civic legacy/new completion lookup closure changed")
    for suffix in ("cooperation", "taming", "nationalization"):
        body = effects[f"HOK_KOR_legacy_{suffix}_adjustment"]
        guard = f"HOK_KOR_legacy_{suffix}_registered"
        require(one(one(body, "if"), "limit") == parse(f"tag = KOR NOT = {{ has_country_flag = {guard} }}")
                and scalar(one(body, "if"), "set_country_flag") == guard,
                f"civic legacy adjustment can repeat: {suffix}")
    require(effects["HOK_KOR_monthly_civic_update"][0] == Entry("HOK_KOR_register_legacy_civic_state", "=", "yes"),
            "monthly civic update lost legacy registration")
    decisions = civic_flat_decisions(documents[CIVIC_DECISIONS])
    require(len(decisions) == 13 and len(named(documents["common/decisions/categories/HOK_KOR_civic_categories.txt"])) == 2,
            "civic decision/category inventory must remain 13/2")
    for identifier, cost, duration in (
        ("secure_prosecutorial_records", "150", "45"), ("break_capture_networks", "200", "60"),
        ("restore_civilian_mandate", "200", "90"), ("independent_procurement_audit", "100", "60"),
        ("recover_air_procurement", "150", "60"), ("recover_rocket_procurement", "150", "60"),
    ):
        body = decisions["HOK_KOR_" + identifier]
        require(scalar(body, "cost") == cost and scalar(body, "days_remove") == duration,
                f"civic timed policy cost/duration changed: {identifier}")
    require(scalar(decisions["HOK_KOR_prosecutor_coup_countdown"], "days_mission_timeout") == "90",
            "civic coup warning mission must remain ninety days")
    for identifier in ("fast_track_air_contracts", "fast_track_rocket_contracts"):
        require(scalar(decisions["HOK_KOR_" + identifier], "cost") == "75", f"civic procurement cost changed: {identifier}")
    inlay = one(documents[CIVIC_INLAY], "HOK_KOR_civic_influence_inlay_window")
    require(scalar(inlay, "window_name") == "HOK_KOR_civic_influence_window"
            and one(inlay, "visible") == parse("tag = KOR has_country_flag = HOK_KOR_civic_system_initialized"),
            "civic inlay scope or initialization gate changed")
    buttons = named(one(inlay, "scripted_buttons"))
    require(set(buttons) == {identifier + "_button" for identifier in CIVIC_BUTTONS}, "civic four-button inventory changed")
    triggers = named(documents[CIVIC_TRIGGERS])
    require(triggers["HOK_KOR_civic_action_state_available"] == parse("tag = KOR has_country_flag = HOK_KOR_civic_system_initialized has_country_flag = HOK_KOR_civic_panel_unlocked has_capitulated = no has_civil_war = no NOT = { has_country_flag = HOK_KOR_civic_action_cooldown }"),
            "civic action state gate changed")
    require(triggers["HOK_KOR_civic_action_available"] == parse("HOK_KOR_civic_action_state_available = yes NOT = { has_political_power < 50 }"),
            "civic GUI readiness must retain the separate PP gate")
    for identifier in CIVIC_BUTTONS:
        wrapper = effects[identifier]
        require([entry.value for entry in walk(wrapper) if entry.key == "add_political_power"] == ["-50"],
                f"civic GUI action must charge PP50 once: {identifier}")
        require(scalar(decisions[identifier], "cost") == "50"
                and not any(entry.key == "add_political_power" for entry in walk(decisions[identifier])),
                f"civic decision duplicated or removed its engine charge: {identifier}")
        require(one(buttons[identifier + "_button"], "click_effect") == parse(identifier + " = yes"),
                f"civic inlay click helper changed: {identifier}")
        helper = effects[identifier.replace("HOK_KOR_", "HOK_KOR_apply_", 1)]
        require(children(one(helper, "if"), "set_country_flag") == [parse("flag = HOK_KOR_civic_action_cooldown value = 1 days = 90")]
                and scalar(one(helper, "if"), "HOK_KOR_sync_civic_state") == "yes",
                f"civic action lost shared cooldown/sync: {identifier}")
    ideas = named(one(one(documents[CIVIC_IDEAS], "ideas"), "country"))
    require(len(ideas) == 20 and all(one(idea, "allowed_civil_war") == parse("always = no") for idea in ideas.values()),
            "civic twenty country spirits/civil-war exclusion changed")
    events_list = children(documents[CIVIC_EVENTS], "country_event")
    events = {scalar(event, "id"): event for event in events_list}
    require(len(events) == len(events_list) == 11
            and set(events) == {f"HOK_KOR_CIVIC.{number}" for number in (1, 2, 3, 11, 12, 13, 20, 21, 22, 23, 24)},
            "civic event namespace/inventory changed")
    for identifier, event in events.items():
        require(scalar(event, "is_triggered_only") == "yes" and Entry("tag", "=", "KOR") in one(event, "trigger"),
                f"civic event lost triggered-only Korean scope: {identifier}")
    scope_forbidden = {"every_country", "any_country", "random_country", "every_state", "any_state", "random_state",
                       "every_owned_state", "every_controlled_state", "capital_scope", "owner", "controller"}
    for relative in (CIVIC_EFFECTS, CIVIC_TRIGGERS, CIVIC_EVENTS, CIVIC_ACTIONS, CIVIC_DECISIONS, CIVIC_INLAY):
        require(not any(entry.key in scope_forbidden for entry in walk(documents[relative])),
                f"civic country logic gained a broad/foreign/state scope: {relative}")
    orders = named(one(documents["common/decisions/KOR_decision.txt"], "KOR_jaebeol_category"))
    for identifier in ("KOR_order_to_samsung", "KOR_order_to_hyundai", "KOR_order_to_sk"):
        expected = parse("OR = { has_completed_focus = HOK_KOR_civic_chaebol_cooperation has_country_flag = HOK_KOR_legacy_cooperation_registered has_completed_focus = KOR_cooperation_with_the_jaebeol has_completed_focus = KOR_taming_the_jaebeol }")
        require(one(orders[identifier], "available") == expected and one(orders[identifier], "visible") == expected,
                f"civic company-order access regression: {identifier}")


def check_civic_presentation(payloads: dict[str, bytes], documents: dict[str, Block]) -> None:
    locales = {relative: data for relative, data in payloads.items() if relative.endswith(".yml")}
    require(len(locales) == 6, "civic localisation must remain three bilingual pairs")
    keys = {language: set() for language in ("english", "korean")}
    for relative, data in locales.items():
        language = Path(relative).parts[1]
        require(data.startswith(b"\xef\xbb\xbf" + f"l_{language}:".encode()), f"civic localisation BOM/header changed: {relative}")
        found = re.findall(r"(?m)^\s+([A-Za-z0-9_.-]+):\d*\s", data.decode("utf-8-sig"))
        require(len(found) == len(set(found)) and not keys[language] & set(found), f"duplicate civic localisation: {relative}")
        keys[language].update(found)
    require(keys["english"] == keys["korean"], "civic bilingual key sets differ")
    focuses = focus_blocks(documents[FOCUS_PATH])
    ideas = named(one(one(documents[CIVIC_IDEAS], "ideas"), "country"))
    decisions = civic_flat_decisions(documents[CIVIC_DECISIONS])
    required = set(CIVIC_FOCUS_IDS) | set(ideas) | set(decisions) | {"HOK_KOR_civic_balance", "HOK_KOR_procurement_integrity"}
    required |= {identifier + "_desc" for identifier in required}
    require(required <= keys["english"], f"civic missing definition descriptions: {sorted(required - keys['english'])}")
    sprites = {}
    for path in effective_files("interface", "*.gfx"):
        text = path.read_bytes().decode("utf-8-sig")
        for match in re.finditer(r'\bname\s*=\s*"?([A-Za-z0-9_]+)"?', mask_comments(text)):
            sprites[match.group(1)] = path
    consumed = {scalar(focuses[identifier], "icon") for identifier in CIVIC_FOCUS_IDS}
    consumed |= {"GFX_idea_" + scalar(idea, "picture") for idea in ideas.values()}
    consumed |= {scalar(decision, "icon") for decision in decisions.values()}
    for relative in (CIVIC_GUI, CIVIC_INLAY):
        consumed |= {entry.value for entry in walk(documents[relative])
                     if entry.key.lower() in ("spritetype", "quadtexturesprite") and isinstance(entry.value, str)}
    require(consumed <= sprites.keys(), f"unresolved civic sprite: {sorted(consumed - sprites.keys())}")
    selected_sprites = {}
    for relative, block in documents.items():
        if relative.endswith(".gfx"):
            for sprite in children(block, "spriteTypes"):
                for entry in sprite:
                    require(isinstance(entry.value, tuple), "civic invalid sprite registration")
                    identifier = scalar(entry.value, "name")
                    require(identifier not in selected_sprites, "civic duplicate sprite ID")
                    selected_sprites[identifier] = entry.value
                    for item in walk(entry.value):
                        if item.key.lower() in ("texturefile", "animationmaskfile", "animationtexturefile"):
                            texture = Path(item.value)
                            require(any((base / texture).is_file() for base in (ROOT, RT56_ROOT, VANILLA_ROOT)),
                                    f"missing civic presentation dependency: {identifier}/{texture}")
                        if item.key.lower() == "effectfile":
                            # The target vanilla registry uses the historical .lua effect key with a physical .shader provider.
                            provider = {SHINE_EFFECT: "interface/goals_shine.gfx",
                                        "gfx/FX/buttonstate_nodowneffect.lua": "interface/core.gfx"}
                            require(item.value in provider
                                    and (VANILLA_ROOT / Path(item.value).with_suffix(".shader")).is_file()
                                    and item.value in mask_comments((VANILLA_ROOT / provider[item.value]).read_text(encoding="utf-8-sig")),
                                    "civic shine effect differs from the target vanilla registration/provider")
                        if item.key.lower() == "animationtexturefile":
                            require(item.value == SHINE_OVERLAY, "civic shine must use the host/vanilla shared overlay")
    for relative, data in payloads.items():
        if relative.endswith(".dds"):
            require(data[:4] == b"DDS " and len(data) >= 128 and struct.unpack("<I", data[4:8])[0] == 124,
                    f"invalid civic DDS header: {relative}")
    for relative in (CIVIC_INLAY, "common/scripted_localisation/HOK_KOR_civic_influence_scripted_loc.txt", CIVIC_GUI):
        for entry in walk(documents[relative]):
            if entry.key in ("localization_key", "buttonText", "context_aware_text", "context_aware_tooltip") and isinstance(entry.value, str) and entry.value.startswith("HOK_KOR_"):
                require(entry.value in keys["english"], f"unresolved civic UI localisation: {entry.value}")


def check_civic_update(payloads: dict[str, bytes] | None = None, documents: dict[str, Block] | None = None) -> None:
    if payloads is None or documents is None:
        payloads, documents = civic_documents()
    check_civic_source(payloads, documents)
    check_civic_semantics(documents)
    check_civic_presentation(payloads, documents)


def run_civic_checks() -> None:
    check_civic_update()
    print("PASS civic source/contracts: 31 selected outputs, 472 playable focuses plus legacy lookup, 13 decisions, 20 ideas, 11 events; seeds/clamps/tier replacement, PP/cooldown, country callbacks, inlay/localisation/artwork closure; 405 earlier generated outputs unchanged")
    print("STATIC ONLY: no engine evaluation, UI, progression, save, AI, DLC or multiplayer proof.")


def run_civic_self_tests() -> None:
    payloads, current = civic_documents()
    check_civic_update(payloads, current)
    caught = []
    def rejects(label, action):
        try:
            action()
        except (ValueError, KeyError, StopIteration, UnicodeError):
            caught.append(label)
        else:
            raise ValueError(f"civic mutation was not detected: {label}")
    def mutation(relative, path, value):
        return {**current, relative: replace_entry(current[relative], path, value)}
    for variable in CIVIC_VARIABLES:
        clamps = children(named(current[CIVIC_EFFECTS])["HOK_KOR_sync_civic_state"], "clamp_variable")
        index = CIVIC_VARIABLES.index(variable)
        changed = list(named(current[CIVIC_EFFECTS])["HOK_KOR_sync_civic_state"])
        changed[index] = Entry("clamp_variable", "=", replace_entry(clamps[index], ("max",), "101"))
        rejects("clamp-" + variable, lambda changed=changed: check_civic_semantics(mutation(CIVIC_EFFECTS, ("HOK_KOR_sync_civic_state",), tuple(changed))))
    for path, value, label in (
        (("HOK_KOR_initialize_civic_system", "if", "limit"), parse("tag = KOR"), "once-only-init"),
        (("HOK_KOR_select_chaebol_cooperation", "if", "limit"), parse("always = yes"), "policy-scope"),
        (("HOK_KOR_support_chaebol", "if", "add_political_power"), "-25", "gui-cost"),
        (("HOK_KOR_legacy_cooperation_adjustment", "if", "limit"), parse("tag = KOR"), "legacy-repeat"),
    ):
        rejects(label, lambda path=path, value=value: check_civic_semantics(mutation(CIVIC_EFFECTS, path, value)))
    for callback in ("on_startup", "on_monthly_KOR"):
        rejects("country-scope-" + callback, lambda callback=callback: check_civic_semantics(mutation(CIVIC_ACTIONS, ("on_actions", callback, "effect"), parse("HOK_KOR_monthly_civic_update = yes"))))
    rejects("legacy-rewards", lambda: check_civic_semantics(mutation(CIVIC_LEGACY, ("shared_focus", "completion_reward"), parse("add_political_power = 150"))))
    rejects("legacy-playable", lambda: check_civic_semantics(mutation(CIVIC_LEGACY, ("shared_focus", "available"), parse("always = yes"))))
    rejects("inlay-country-leak", lambda: check_civic_semantics(mutation(CIVIC_INLAY, ("HOK_KOR_civic_influence_inlay_window", "visible"), parse("always = yes"))))
    for identifier in CIVIC_BUTTONS:
        rejects("decision-cost-" + identifier, lambda identifier=identifier: check_civic_semantics(mutation(CIVIC_DECISIONS, ("HOK_KOR_civic_balance", identifier, "cost"), "0")))
    rejects("inlay-position", lambda: check_civic_semantics(mutation(FOCUS_PATH, ("focus_tree", "inlay_window", "position"), parse("x = 0 y = 0"))))
    rejects("missing-decision", lambda: check_civic_semantics(mutation(CIVIC_DECISIONS, ("HOK_KOR_civic_balance", "HOK_KOR_support_civic"), None)))
    for relative in (CIVIC_EVENTS, CIVIC_GUI, "interface/HOK_KOR_civic_focus.gfx", FOCUS_PATH):
        changed = {**current, relative: current[relative] + parse("unexpected_civic_regression = yes")}
        rejects("ordered-AST-" + relative, lambda changed=changed: check_civic_source(payloads, changed))
    locale = "localisation/korean/HOK_KOR_civic_ui_l_korean.yml"
    rejects("locale-header", lambda: check_civic_presentation({**payloads, locale: payloads[locale][3:]}, current))
    asset = next(relative for relative in payloads if relative.endswith(".dds"))
    rejects("asset-source", lambda: check_civic_source({**payloads, asset: payloads[asset][:-1] + bytes([payloads[asset][-1] ^ 1])}, current))
    rejects("missing-path", lambda: check_civic_source({relative: data for relative, data in payloads.items() if relative != asset}, current))
    print(f"PASS civic mutation self-test: {len(caught)} regressions rejected; exact immutable-source fixture accepted; no production writes")
    print("SCOPED STATIC ONLY: 472 playable focuses and one legacy lookup; 13 decisions, 20 country spirits, 11 events; lifecycle/scope/presentation contracts only. Historical aggregate assertions remain enforced; no engine, UI, progression, save, AI or multiplayer proof.")


def run_checks() -> None:
    check_civic_update()
    current, expected = documents()
    compare_documents(current, expected)
    groups = collect(current)
    added = check_inventory(groups)
    check_layout(groups["focus"], added)
    check_projects(groups)
    check_regional_gates(groups)
    check_material_cycle(groups)
    check_focus_prerequisite_update(groups)
    check_royal_update(groups)
    check_prose_update()
    check_assets(groups, added)
    check_localisation(localisation_payloads(), groups, added)
    check_references(groups, added)
    print("PASS second wave plus material cycle: pinned 460 focuses (134 new), 64 ideas, 19 projects, 5 categories, 12 state modifiers; ordered source/port contracts")
    print("PASS material cycle: focus gameplay and unrelated content preserved; closed-cycle decision notice added; +30%/+60% tiers, one PP150/90-day boost, no stacking or cooldown, temporary-only cleanup")
    print("PASS second-wave artwork/localisation: 234 exact DDS, 368 sprites, 17 registries, 11 paired language files; vanilla shine fallback")
    print("PASS prerequisite update: six focuses only; two separate mining AND parents, five entry gates removed; rewards, timing, layout, AI and later policy gates preserved")
    print("PASS royal update: sixteen gates removed in fourteen focuses; supply diamond only four coordinates move; two courier lifetimes updated; rewards, tiers, AI, regional AND gates and conditional offsets preserved")
    print("PASS prose update: 124 descriptions per channel, fourteen frozen pairs; keys, six protected descriptions, gameplay and ADR-0005 regions preserved")
    print("STATIC ONLY: no HOI4 evaluation, geography lifecycle, layout rendering, AI, save or multiplayer proof.")


def prerequisite_mutation_checks(groups, rejects, focus_mutation) -> None:
    #20261010_kpopmodder: Reject lost mining conjunctions, retained obsolete gates and changes outside the six-entry delta.
    mining = groups["focus"][PREREQUISITE_MINING]
    mining_parents = children(mining, "prerequisite")
    def mining_or(body: Block) -> Block:
        merged = tuple(entry for relation in children(body, "prerequisite") for entry in relation)
        result, inserted = [], False
        for entry in body:
            if entry.key == "prerequisite":
                if not inserted:
                    result.append(Entry("prerequisite", "=", merged))
                    inserted = True
            else:
                result.append(entry)
        return tuple(result)
    collapsed = focus_mutation(PREREQUISITE_MINING, mining_or)
    rejects("mining AND parents collapsed into OR", lambda: check_focus_prerequisite_update(collect(collapsed)))
    missing_mining = focus_mutation(PREREQUISITE_MINING, lambda body: tuple(
        entry for entry in body if entry != Entry("prerequisite", "=", mining_parents[1])))
    rejects("mining second parent removed", lambda: check_focus_prerequisite_update(collect(missing_mining)))
    for identifier, removed in PREREQUISITE_REMOVALS.items():
        stale_gate = focus_mutation(identifier, lambda body, removed=removed: replace_entry(
            body, ("available",), one(body, "available") + parse(f"has_completed_focus = {removed}")))
        rejects(f"obsolete entry gate restored: {identifier}",
                lambda stale_gate=stale_gate: check_focus_prerequisite_update(collect(stale_gate)))
    liaison = "HOK_KOR_nrsc_interservice_liaison"
    lost_coup = focus_mutation(liaison, lambda body: replace_entry(
        body, ("available",), parse("has_government = fascism has_civil_war = no")))
    rejects("liaison coup gate removed", lambda: check_focus_prerequisite_update(collect(lost_coup)))
    occupation = "HOK_KOR_nrsc_military_administration"
    lost_control = focus_mutation(occupation, lambda body: replace_entry(body, ("available",),
        parse("has_government = fascism has_civil_war = no has_completed_focus = KOR_establishment_of_the_national_salvation_army")))
    rejects("occupation actual non-core control gate removed", lambda: check_focus_prerequisite_update(collect(lost_control)))
    for gate, later in PREREQUISITE_LATER_GATES.items():
        for identifier in later:
            relaxed = focus_mutation(identifier, lambda body, gate=gate: replace_entry(body, ("available",), tuple(
                entry for entry in one(body, "available") if entry != Entry("has_completed_focus", "=", gate))))
            rejects(f"later policy gate removed: {identifier}",
                    lambda relaxed=relaxed: check_focus_prerequisite_update(collect(relaxed)))
    reward_drift = focus_mutation(PREREQUISITE_MINING, lambda body: replace_entry(body, ("completion_reward",), parse("add_political_power = 1")))
    rejects("prerequisite update mining reward drift", lambda: check_focus_prerequisite_update(collect(reward_drift)))



def royal_mutation_checks(groups, rejects, focus_mutation) -> None:
    #20261010_kpopmodder: Exercise newly early access, acquired-spirit persistence and the relocated four-node supply diamond.
    previous = focus_blocks(expected_script(FOCUS_PATH, royal_update=False))
    for identifier, removed in ROYAL_REMOVALS.items():
        retained = focus_mutation(identifier, lambda body, removed=removed: replace_entry(
            body, ("available",), one(body, "available") + tuple(Entry("has_completed_focus", "=", value) for value in removed)))
        rejects(f"royal obsolete gates restored: {identifier}", lambda retained=retained: check_royal_update(collect(retained)))
    for identifier, guard in (
        (ROYAL_AM_IDS[0], "original_tag"), (ROYAL_AM_IDS[0], "has_government"), (ROYAL_AM_IDS[0], "has_civil_war"),
        (ROYAL_H2_IDS[0], "original_tag"), (ROYAL_H2_IDS[0], "has_civil_war"), (ROYAL_H2_IDS[0], "is_subject"),
    ):
        relaxed = focus_mutation(identifier, lambda body, guard=guard: replace_entry(
            body, ("available",), tuple(entry for entry in one(body, "available") if entry.key != guard)))
        rejects(f"royal retained guard removed: {identifier}/{guard}", lambda relaxed=relaxed: check_royal_update(collect(relaxed)))
    fragment = focus_mutation(ROYAL_H2_IDS[0], lambda body: replace_entry(body, ("available", "OR"),
                              parse("AND = { owns_state = 941 has_full_control_of_state = 941 }")))
    rejects("royal split-region fragment accepted", lambda: check_royal_update(collect(fragment)))
    for identifier in ROYAL_COURIER_IDEAS:
        body = groups["idea"][identifier]
        restored = {**groups, "idea": {**groups["idea"], identifier: body + parse("cancel = { NOT = { has_completed_focus = KOR_empire_of_hwan } }")}}
        rejects(f"royal acquired courier cancels: {identifier}", lambda restored=restored: check_royal_update(restored))
        weak = {**groups, "idea": {**groups["idea"], identifier: replace_entry(body, ("modifier",), parse("initiative_factor = 0.01 army_speed_factor = 0.01"))}}
        rejects(f"royal courier modifier drift: {identifier}", lambda weak=weak: check_royal_update(weak))
    other = next(identifier for identifier, body in named(one(one(expected_script(ROYAL_IDEA_PATH, royal_update=False), "ideas"), "country")).items()
                 if identifier not in ROYAL_COURIER_IDEAS and children(body, "cancel"))
    lost_cancel = {**groups, "idea": {**groups["idea"], other: replace_entry(groups["idea"][other], ("cancel",), None)}}
    rejects("royal unrelated spirit cancellation removed", lambda: check_royal_update(lost_cancel))
    for identifier in ("HOK_KOR_am_mobilization_review", "HOK_KOR_hw_supply_returns", "HOK_KOR_hw_relay_exercises"):
        body = groups["focus"][identifier]
        parents = children(body, "prerequisite")
        collapsed = focus_mutation(identifier, lambda body, parents=parents: tuple(entry for entry in body if entry.key != "prerequisite") +
                                  (Entry("prerequisite", "=", tuple(item for parent in parents for item in parent)),))
        rejects(f"royal internal AND collapsed: {identifier}", lambda collapsed=collapsed: check_royal_update(collect(collapsed)))
    stacked = focus_mutation("HOK_KOR_hw_relay_exercises", lambda body: replace_entry(body, ("completion_reward",), parse("add_ideas = HOK_KOR_hw_courier_service_2")))
    rejects("royal courier upgrade retains lower tier", lambda: check_royal_update(collect(stacked)))
    old_parent = focus_mutation(ROYAL_SUPPLY_ROOT, lambda body: replace_entry(body, ("prerequisite",), parse("focus = KOR_return_of_the_king")))
    rejects("royal supply parent remains at king return", lambda: check_royal_update(collect(old_parent)))
    layout_changes = (
        ("root horizontal shift", ROYAL_SUPPLY_ROOT, ("x",), "7"),
        ("root vertical shift", ROYAL_SUPPLY_ROOT, ("y",), "2"),
        ("child local shift", "HOK_KOR_hw_provision_accounts", ("x",), "-2"),
        ("unrelated focus shift", ROYAL_AM_IDS[0], ("x",), "5"),
        ("cyclic root anchor", ROYAL_SUPPLY_ROOT, ("relative_position_id",), ROYAL_SUPPLY_ROOT),
        ("forward cyclic anchor", ROYAL_SUPPLY_ROOT, ("relative_position_id",), "HOK_KOR_hw_supply_returns"),
        ("missing anchor", ROYAL_SUPPLY_ROOT, ("relative_position_id",), "hok_rt56_missing_royal_anchor"),
        ("offset before royal completion", ROYAL_OFFSET_ROOT, ("offset", "trigger"), parse("always = yes")),
        ("offset applies on SHOW", ROYAL_OFFSET_ROOT, ("offset", "trigger"), parse("has_game_rule = { rule = obsolete_focus_branches_visibility option = SHOW }")),
    )
    for label, identifier, location, value in layout_changes:
        altered = focus_mutation(identifier, lambda body, location=location, value=value: replace_entry(body, location, value))
        rejects(f"royal layout {label}", lambda altered=altered: check_royal_layout(collect(altered)["focus"], previous))
    doubled = focus_mutation(ROYAL_SUPPLY_ROOT, lambda body: body + parse("offset = { x = -101 y = 0 trigger = { always = yes } }"))
    rejects("royal political offset inherited twice", lambda: check_royal_layout(collect(doubled)["focus"], previous))


def run_royal_self_tests() -> None:
    #20261010_kpopmodder: Keep focused royal/prerequisite evidence available without weakening unrelated historical descriptor assertions.
    current, expected = documents()
    compare_documents(current, expected)
    groups = collect(current)
    check_inventory(groups)
    check_regional_gates(groups)
    check_focus_prerequisite_update(groups)
    check_royal_update(groups)
    caught = []
    def rejects(label, action):
        try:
            action()
        except (ValueError, KeyError, StopIteration):
            caught.append(label)
        else:
            raise ValueError(f"royal/prerequisite mutation was not detected: {label}")
    def focus_mutation(identifier, transform):
        tree = one(current[FOCUS_PATH], "focus_tree")
        modified = tuple(Entry(entry.key, entry.op, transform(entry.value))
                         if entry.key == "focus" and scalar(entry.value, "id") == identifier else entry for entry in tree)
        return {**current, FOCUS_PATH: replace_entry(current[FOCUS_PATH], ("focus_tree",), modified)}
    prerequisite_mutation_checks(groups, rejects, focus_mutation)
    royal_mutation_checks(groups, rejects, focus_mutation)
    print(f"PASS royal/prerequisite mutation self-test: {len(caught)} regressions rejected; current immutable-source fixture accepted; no production writes")
    print("SCOPED STATIC ONLY: historical descriptor/material/prose assertions remain enforced by --check and --self-test; no UI, progression, AI, save or multiplayer proof.")



def run_self_tests() -> None:
    # [2026-09-23]_kpopmodder: Inject bounded in-memory faults against immutable-source expectations; never mutate production files.
    current, expected = documents()
    compare_documents(current, expected)
    groups = collect(current)
    added = check_inventory(groups)
    check_projects(groups)
    check_material_cycle(groups)
    check_focus_prerequisite_update(groups)
    check_royal_update(groups)
    check_prose_update()
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

    prerequisite_mutation_checks(groups, rejects, focus_mutation)
    royal_mutation_checks(groups, rejects, focus_mutation)

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
    frozen_material = {relative: read_material_cycle_source(relative) for relative in MATERIAL_LOCALES}
    missing_material_key = {**frozen_material, locale: re.sub(
        rb"(?m)^ " + MATERIAL_BOOST.encode() + rb"_desc:[^\r\n]*\r?\n?", b"", frozen_material[locale])}
    rejects("material-cycle temporary spirit description removed", lambda: check_material_cycle(groups, missing_material_key))
    print(f"PASS second-wave mutation self-test: {len(caught)} regressions rejected; immutable-source positive fixture accepted; no production writes")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--royal-self-test", action="store_true")
    mode.add_argument("--civic-self-test", action="store_true")
    mode.add_argument("--civic-check", action="store_true")
    args = parser.parse_args()
    try:
        run_civic_checks() if args.civic_check else run_civic_self_tests() if args.civic_self_test else run_royal_self_tests() if args.royal_self_test else run_self_tests() if args.self_test else run_checks()
    except (OSError, UnicodeError, ValueError, KeyError, StopIteration) as exc:
        print(f"ERROR Korean second-wave contract: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
