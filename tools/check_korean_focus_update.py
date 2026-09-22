#!/usr/bin/env python3
"""Read-only semantic checks for the audited Korean focus update.

This checks ordered source blocks and a deliberately limited Boolean model.
It does not execute HOI4 scripts or prove runtime scope, AI scheduling, load
precedence, repeatable-decision lifecycle, or DLC behaviour.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path

from build_rt56_map import PROVINCE_ID_MAP, STATE_ID_MAP
from migrate_hok_ids import apply_post_migration_fixes, replace_tokens
from source_snapshot import FOCUS_UPDATE_PATHS, read_source_file
from validate_port import ROOT, RT56_ROOT, VANILLA_ROOT, localisation_keys, mask_comments, matching_brace


# [2026-09-22]_kpopmodder: Preserve repeated keys and order; this reader never serializes production scripts.
@dataclass(frozen=True)
class Entry:
    key: str
    op: str | None = None
    value: str | tuple["Entry", ...] | None = None


Block = tuple[Entry, ...]
LEXER = re.compile(r'\s+|\#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|[<>=!]+|[^\s{}<>=!"#]+')
PREFIX = "HOK_KOR_"
FOCUS_PATH = "common/national_focus/korea.txt"
AI_PATH = "common/ai_strategy_plans/KOR_historical_strategy_plan.txt"
IDEA_PATHS = tuple(f"common/ideas/HOK_KOR_{part}_expansion.txt" for part in ("industry", "military", "democratic"))
DECISION_PATHS = tuple(f"common/decisions/HOK_KOR_{part}_expansion.txt" for part in ("industry", "democratic"))
EVENT_PATH = "events/HOK_KOR_democratic_expansion.txt"
# [2026-09-22]_kpopmodder: Audit the precise visual delta independently of the production builder.
ICON_MANIFEST = ROOT / "docs/data/HOK_KOREAN_FOCUS_ICON_MANIFEST.json"
ICON_GFX_PATHS = (
    "interface/HOK_KOR_focus_icons.gfx",
    "interface/HOK_KOR_focus_icons_shine.gfx",
    "interface/HOK_KOR_spirit_icons.gfx",
)
SHINE_OVERLAY = "gfx/interface/goals/shine_overlay.dds"
SHINE_EFFECT = "gfx/FX/buttonstate.lua"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def parse(text: str) -> Block:
    tokens = []
    end = 0
    for match in LEXER.finditer(text):
        require(match.start() == end, f"unrecognized script token at {end}")
        token = match.group()
        end = match.end()
        if not token.isspace() and not token.startswith("#"):
            tokens.append(token[1:-1] if token.startswith('"') else token)
    require(end == len(text), "unrecognized trailing script token")
    index = 0

    def consume(nested: bool = False) -> Block:
        nonlocal index
        entries = []
        while index < len(tokens):
            key = tokens[index]
            index += 1
            if key == "}":
                require(nested, "unexpected closing brace")
                return tuple(entries)
            if index < len(tokens) and tokens[index] in ("=", ">", "<", ">=", "<=", "!=", "=="):
                op = tokens[index]
                index += 1
                require(index < len(tokens), f"missing value for {key}")
                value = tokens[index]
                index += 1
                if value == "{":
                    value = consume(True)
                entries.append(Entry(key, op, value))
            else:
                entries.append(Entry(key))
        require(not nested, "unclosed script block")
        return tuple(entries)

    return consume()


def read(path: Path) -> Block:
    try:
        return parse(path.read_bytes().decode("utf-8-sig"))
    except ValueError as exc:
        raise ValueError(f"{path}: {exc}") from exc


def children(block: Block, key: str) -> list[Block]:
    return [entry.value for entry in block if entry.key == key and isinstance(entry.value, tuple)]


def one(block: Block, key: str) -> Block:
    found = children(block, key)
    require(len(found) == 1, f"expected one {key} block, got {len(found)}")
    return found[0]


def scalar(block: Block, key: str) -> str:
    found = [entry.value for entry in block if entry.key == key and isinstance(entry.value, str)]
    require(len(found) == 1, f"expected one scalar {key}, got {found}")
    return found[0]


def walk(block: Block):
    for entry in block:
        yield entry
        if isinstance(entry.value, tuple):
            yield from walk(entry.value)


def named(block: Block) -> dict[str, Block]:
    entries = [entry for entry in block if isinstance(entry.value, tuple)]
    require(len({entry.key for entry in entries}) == len(entries), "duplicate named definition")
    return {entry.key: entry.value for entry in entries}


def focus_blocks(block: Block) -> dict[str, Block]:
    focuses = children(one(block, "focus_tree"), "focus")
    ids = [scalar(focus, "id") for focus in focuses]
    require(len(set(ids)) == len(ids), "duplicate Korean focus ID")
    return dict(zip(ids, focuses))


def mapped(block: Block) -> Block:
    mapping = {str(old): str(new) for old, new in {**PROVINCE_ID_MAP, **STATE_ID_MAP}.items()}
    return tuple(Entry(mapping.get(entry.key, entry.key), entry.op,
                       mapped(entry.value) if isinstance(entry.value, tuple)
                       else mapping.get(entry.value, entry.value)) for entry in block)


def check_focus_contract(current: dict[str, Block], baseline: dict[str, Block], source: dict[str, Block]) -> set[str]:
    require(len(baseline) == 266 and len(current) == 326, "expected original 266 and updated 326 focuses")
    require(set(current) == set(source) and set(baseline) <= set(current), "inherited or updated focus IDs changed")
    added = set(current) - set(baseline)
    require(len(added) == 60 and all(identifier.startswith(PREFIX) for identifier in added), "expected exactly 60 namespaced additions")
    shortened: set[str] = set()
    for identifier, old in baseline.items():
        old_cost = scalar(old, "cost")
        expected = "5" if old_cost == "10" else old_cost
        require(scalar(current[identifier], "cost") == expected, f"inherited duration changed: {identifier}")
        if old_cost == "10":
            shortened.add(identifier)
    # [2026-09-22]_kpopmodder: The 152-focus batch followed two uncommitted donor reductions, both present in da81530.
    earlier_reductions = {"KOR_the_vanguard_of_asian_democracy", "KOR_stop_moderate_diplomacy"}
    require(earlier_reductions <= shortened and len(shortened - earlier_reductions) == 152,
            "expected the two earlier democratic reductions plus 152 expansion reductions from the Git baseline")
    for identifier in added:
        focus = current[identifier]
        require(scalar(focus, "cost") == "5", f"new focus duration: {identifier}")
        # The generator owns bytes; this independently preserves ordered rewards after ID mapping.
        require(one(focus, "completion_reward") == mapped(one(source[identifier], "completion_reward")), f"new focus reward differs from audited donor: {identifier}")
        for key, value in (("cancel_if_invalid", "yes"), ("continue_if_invalid", "no"), ("available_if_capitulated", "no")):
            require(scalar(focus, key) == value, f"new focus cancellation contract: {identifier}/{key}")
    for identifier, focus in current.items():
        for entry in focus:
            if entry.key == "relative_position_id":
                require(entry.value in current, f"missing layout anchor: {identifier}/{entry.value}")
            if entry.key in ("prerequisite", "mutually_exclusive") and isinstance(entry.value, tuple):
                for target in entry.value:
                    require(target.key == "focus" and target.value in current, f"missing focus relationship: {identifier}/{target.value}")
        if identifier in baseline:
            require(not any(entry.key == "focus" and entry.value in added for parent in children(focus, "prerequisite") for entry in parent), f"new prerequisite inserted into inherited focus: {identifier}")
    for relation in ("relative_position_id", "prerequisite"):
        visiting: set[str] = set()
        finished: set[str] = set()

        def visit(identifier: str) -> None:
            require(identifier not in visiting, f"{relation} cycle at {identifier}")
            if identifier in finished:
                return
            visiting.add(identifier)
            block = current[identifier]
            parents = ([entry.value for entry in block if entry.key == relation] if relation == "relative_position_id"
                       else [entry.value for group in children(block, relation) for entry in group])
            for parent in parents:
                visit(parent)
            visiting.remove(identifier)
            finished.add(identifier)

        for identifier in current:
            visit(identifier)
    # [2026-09-22]_kpopmodder: Preserve this inherited reward and allow only the approved guarded economy-law follow-up.
    identifier = "KOR_independent_party_in_power"
    original_reward = mapped(one(source[identifier], "completion_reward"))
    reward = one(current[identifier], "completion_reward")
    require(reward[:len(original_reward)] == original_reward, "independent-party original reward changed or reordered")
    follow_up = reward[len(original_reward):]
    require(follow_up == parse("""
        if = {
            limit = { OR = { has_idea = civilian_economy has_idea = low_economic_mobilisation } }
            add_ideas = partial_economic_mobilisation
        }
    """), "independent-party reward must append exactly one guarded partial-mobilization effect")
    guard = one(one(follow_up, "if"), "limit")
    eligible = ("civilian_economy", "low_economic_mobilisation")
    unchanged = ("partial_economic_mobilisation", "war_economy", "tot_economic_mobilisation", "other_economy_law")
    for law in eligible + unchanged:
        require(evaluate(guard, {"has_idea": law}) == (law in eligible), f"independent-party economy guard changed: {law}")
    return added


# [2026-09-22]_kpopmodder: The model rejects unsupported predicates rather than assuming engine semantics.
def evaluate(block: Block, context: dict, mode: str = "AND") -> bool:
    values = []
    for entry in block:
        key, value = entry.key, entry.value
        if isinstance(value, tuple):
            if key in ("AND", "OR", "NOT"):
                result = evaluate(value, context, "OR" if key == "OR" else "AND")
                values.append(not result if key == "NOT" else result)
            elif key == "has_game_rule":
                require(scalar(value, "rule") == "KOR_AI_BEHAVIOR", "unexpected AI game rule")
                values.append(context["rule"] == scalar(value, "option"))
            elif key.isdigit():
                values.append(evaluate(value, context["states"][int(key)]))
            elif key == "free_building_slots":
                require(scalar(value, "include_locked") == "yes", "building-space locked-slot contract")
                threshold = next(item for item in value if item.key == "size")
                require(threshold.op == ">", "unsupported building-space operator")
                values.append(context["slots"].get(scalar(value, "building"), 0) > int(threshold.value))
            else:
                raise ValueError(f"unsupported Boolean block {key}")
        elif key == "has_completed_focus":
            values.append(value in context["completed"])
        elif key == "has_global_flag":
            values.append(value in context["flags"])
        elif key == "num_of_civilian_factories_available_for_projects":
            require(entry.op == ">", "unsupported project-factory operator")
            values.append(context["civilian_factories"] > int(value))
        else:
            require(key in context, f"unsupported Boolean predicate {key}")
            values.append(str(context[key]) == value)
    return any(values) if mode == "OR" else all(values)


def ai_context(**overrides) -> dict:
    context = dict(rule="DEFAULT", is_historical_focus_on="yes", has_government="democratic",
                   has_defensive_war="yes", is_subject="no", is_in_faction="no", is_faction_leader="yes",
                   completed={"KOR_president_kim_gu", "KOR_national_unity", "KOR_expend_military_budget"},
                   flags={"kor_triumph_for_the_manchuria_flag"})
    context.update(overrides)
    return context


def check_ai(plans: dict[str, Block], focuses: dict[str, Block], added: set[str]) -> None:
    expected = {"KOR_historical_plan", "HOK_KOR_historical_defense_plan", "HOK_KOR_historical_asian_union_formation_plan", "HOK_KOR_historical_asian_cooperation_plan"}
    require(set(plans) == expected, "expected one historical plan and three support plans")
    basic = plans["KOR_historical_plan"]
    order = [entry.key for entry in one(basic, "ai_national_focuses")]
    require(len(order) == len(set(order)) == 106 and set(order) <= set(focuses), "historical AI focus list must contain 106 unique existing focuses")
    seen: set[str] = set()
    for identifier in order:
        focus = focuses[identifier]
        for alternatives in children(focus, "prerequisite"):
            require(any(entry.value in seen for entry in alternatives), f"historical AI unmet prerequisite ordering: {identifier}")
        require(not any(entry.value in seen for group in children(focus, "mutually_exclusive") for entry in group), f"historical AI mutually-exclusive selections: {identifier}")
        seen.add(identifier)
    zeros = one(basic, "focus_factors")
    require({entry.key: entry.value for entry in zeros} == {"HOK_KOR_flexible_production_lines": "0", "HOK_KOR_foreign_aircraft_designs": "0"}, "historical AI policy choices changed")
    positive = set(order)
    for identifier, plan in plans.items():
        if identifier == "KOR_historical_plan":
            continue
        for entry in one(plan, "focus_factors"):
            require(entry.key in focuses and float(entry.value) > 0, f"unresolved/nonpositive support focus: {identifier}/{entry.key}")
            positive.add(entry.key)
        require(scalar(one(plan, "allowed"), "original_tag") == "KOR", f"support plan country gate: {identifier}")
        enable, abort = one(plan, "enable"), one(plan, "abort")
        require(one(one(abort, "NOT"), "AND") == enable, f"support plan abort is not the inverse of enable: {identifier}")
        context = ai_context()
        if identifier.endswith("cooperation_plan"):
            context["completed"].add("KOR_founding_of_the_asian_union")
        require(evaluate(enable, context), f"positive AI case rejected: {identifier}")
        cases = [dict(has_government="fascism"), dict(rule="FASCIST"), dict(is_historical_focus_on="no"),
                 dict(completed=context["completed"] - {"KOR_president_kim_gu"})]
        if identifier.endswith("defense_plan"):
            cases += [dict(has_defensive_war="no"), dict(completed=context["completed"] - {"KOR_national_unity"}),
                      dict(completed=context["completed"] | {"KOR_call_up_the_rokrf", "KOR_homeland_defence_special_act"})]
        elif identifier.endswith("formation_plan"):
            cases += [dict(is_subject="yes"), dict(is_in_faction="yes"), dict(flags=set()),
                      dict(completed=context["completed"] | {"KOR_founding_of_the_asian_union"}),
                      dict(completed=context["completed"] | {"KOR_liberation_of_the_europe"})]
        else:
            cases += [dict(is_subject="yes"), dict(is_faction_leader="no"),
                      dict(completed=context["completed"] - {"KOR_founding_of_the_asian_union"}),
                      dict(completed=context["completed"] | {entry.key for entry in one(plan, "focus_factors")})]
        for overrides in cases:
            negative = {**context, **overrides}
            require(not evaluate(enable, negative) and evaluate(abort, negative), f"blocked AI condition not enforced: {identifier}/{overrides}")
        explicit = {**context, "rule": "DEMOCRATIC", "is_historical_focus_on": "no"}
        require(evaluate(enable, explicit) and not evaluate(abort, explicit), f"explicit democratic rule blocked: {identifier}")
    require(len(positive) == 118 and len(positive & added) == 53, "historical AI target coverage must be 118 total / 53 additions")
    start, stop = order.index("KOR_strengthen_government_support"), order.index("KOR_national_unity")
    require(stop - start - 1 == 12 and all(scalar(focuses[item], "cost") == "5" for item in order[start + 1:stop]), "government-support interval must retain twelve 35-day focuses")


def state_context(building: str, slots: int = 2) -> dict:
    return {"is_owned_by": "ROOT", "is_fully_controlled_by": "ROOT", "is_coastal": "yes", "slots": {building: slots}}


def check_regional_projects(decisions: dict[str, Block]) -> None:
    contracts = {
        "HOK_KOR_pyeongan_industry_project": (527, "arms_factory"),
        "HOK_KOR_gangwon_industry_project": (1144, "industrial_complex"),
        "HOK_KOR_chungcheong_industry_project": (1145, "industrial_complex"),
        "HOK_KOR_gyeongsang_shipbuilding_project": (920, "dockyard"),
    }
    for identifier, (state_id, building) in contracts.items():
        block = decisions[identifier]
        for key, expected in (("cost", "150"), ("days_remove", "90"), ("fire_only_once", "no")):
            require(scalar(block, key) == expected, f"regional contract changed: {identifier}/{key}")
        require(scalar(one(block, "modifier"), "civilian_factory_use") == "5", f"regional factory cost: {identifier}")
        require(not one(block, "cancel_effect"), f"cancellation grants a reward: {identifier}")
        require(scalar(one(one(block, "highlight_states"), "highlight_state_targets"), "state") == str(state_id), f"incorrect highlighted state: {identifier}")
        available, cancel = one(block, "available"), one(block, "cancel_trigger")
        finish = one(one(block, "remove_effect"), "if")
        completion = one(finish, "limit")
        reward = one(finish, str(state_id))
        require(scalar(reward, "add_extra_state_shared_building_slots") == "1", f"regional slot reward: {identifier}")
        require(one(reward, "add_building_construction") == parse(f"type = {building} level = 1 instant_build = yes"), f"regional construction reward: {identifier}")
        require(sum(entry.key == "add_building_construction" for entry in walk(block)) == 1, f"duplicate regional construction effect: {identifier}")
        require(not any(entry.key in ("has_country_flag", "check_variable") for section in (available, one(block, "visible")) for entry in walk(section)), f"historical completion marker still locks repeatability: {identifier}")
        context = {"has_capitulated": "no", "civilian_factories": 5, "states": {state_id: state_context(building)}}
        require(evaluate(available, context) and evaluate(completion, context) and not evaluate(cancel, context), f"positive regional contract rejected: {identifier}")
        for property_name, value in (("is_owned_by", "OTHER"), ("is_fully_controlled_by", "OTHER"), ("slots", {building: 0})):
            negative = copy.deepcopy(context)
            negative["states"][state_id][property_name] = value
            require(not evaluate(available, negative) and not evaluate(completion, negative) and evaluate(cancel, negative), f"regional loss/space guard missing: {identifier}/{property_name}")
        require(not evaluate(available, {**context, "civilian_factories": 4}), f"regional cost precondition missing: {identifier}")
        defeated = {**context, "has_capitulated": "yes"}
        require(not evaluate(available, defeated) and not evaluate(completion, defeated) and evaluate(cancel, defeated), f"regional capitulation guard missing: {identifier}")


def check_school(focus: Block) -> None:
    available = one(focus, "available")
    finish = one(one(focus, "completion_reward"), "if")
    guard = one(finish, "limit")
    states = {525, 919, 1145}
    require({int(entry.key) for entry in finish if entry.key.isdigit()} == states, "civic-school factory recipients changed")
    for state_id in states:
        reward = one(finish, str(state_id))
        require(scalar(reward, "add_extra_state_shared_building_slots") == "2", "civic-school slot reward changed")
        require(one(reward, "add_building_construction") == parse("type = industrial_complex level = 2 instant_build = yes"), "civic-school factory reward changed")
    context = {"has_government": "democratic", "states": {state_id: state_context("industrial_complex") for state_id in states}}
    require(evaluate(available, context) and evaluate(guard, context), "positive civic-school condition rejected")
    for state_id in states:
        for key, value in (("is_owned_by", "OTHER"), ("is_fully_controlled_by", "OTHER"), ("slots", {"industrial_complex": 1})):
            negative = copy.deepcopy(context)
            negative["states"][state_id][key] = value
            require(not evaluate(available, negative) and not evaluate(guard, negative), f"civic-school all-recipient guard missing: {state_id}/{key}")


def check_allied_projects(decisions: dict[str, Block]) -> None:
    block = decisions["HOK_KOR_finance_allied_industry"]
    for key, expected in (("cost", "75"), ("days_remove", "180"), ("fire_only_once", "no")):
        require(scalar(block, key) == expected, f"allied investment contract changed: {key}")
    require(scalar(one(block, "modifier"), "civilian_factory_use") == "2", "allied investment factory cost changed")
    require(not one(block, "cancel_effect"), "allied cancellation grants a reward")
    for key in ("available", "visible", "target_trigger", "cancel_trigger"):
        require(not any(entry.key in ("has_country_flag", "check_variable") for entry in walk(one(block, key))), f"allied historical flags/counter lock repeats in {key}")
    available = one(one(block, "available"), "FROM")
    eligible = one(available, "any_owned_state")
    require(eligible == parse("is_core_of = PREV is_fully_controlled_by = PREV free_building_slots = { building = industrial_complex size > 0 include_locked = yes }"), "allied investment recipient eligibility changed")
    cancel_from = one(one(one(block, "cancel_trigger"), "OR"), "FROM")
    negative_space = [child for child in children(one(cancel_from, "OR"), "NOT") if children(child, "any_owned_state")]
    require(len(negative_space) == 1 and one(negative_space[0], "any_owned_state") == eligible, "allied project must cancel when no eligible recipient state remains")
    finish = one(one(block, "remove_effect"), "if")
    chosen = one(one(finish, "FROM"), "random_owned_state")
    require(one(chosen, "limit") == eligible, "allied reward must recheck recipient core/control/space")
    require(scalar(chosen, "add_extra_state_shared_building_slots") == "1", "allied investment slot reward changed")
    require(one(chosen, "add_building_construction") == parse("type = industrial_complex level = 1 instant_build = yes"), "allied investment construction reward changed")
    require(sum(entry.key == "add_building_construction" for entry in walk(block)) == 1, "allied project grants construction more than once")
    for identifier, equipment, amount in (("HOK_KOR_send_medical_equipment", "support_equipment", 50), ("HOK_KOR_send_relief_equipment", "infantry_equipment", 100)):
        aid = decisions[identifier]
        finish = one(one(aid, "complete_effect"), "if")
        expected_stockpile = parse(f"{equipment} > {amount - 1}")
        require(one(one(aid, "available"), "has_equipment") == expected_stockpile and one(one(finish, "limit"), "has_equipment") == expected_stockpile, f"aid stockpile check missing: {identifier}")
        require(one(finish, "send_equipment") == parse(f"type = {equipment} amount = {amount} target = FROM"), f"aid transfer changed: {identifier}")
        require(not any(entry.key == "add_equipment_to_stockpile" for entry in walk(aid)), f"aid creates free equipment: {identifier}")


def effective_files(directory: str, suffix: str = "*.txt") -> list[Path]:
    """Project same-relative-path definitions; actual engine precedence remains unproven."""
    files: dict[str, Path] = {}
    for root in (VANILLA_ROOT, RT56_ROOT, ROOT):
        base = root / directory
        if base.is_dir():
            for path in sorted(base.rglob(suffix)):
                files[path.relative_to(base).as_posix()] = path
    return list(files.values())


def definition_ids(path: Path, kind: str) -> set[str]:
    text = path.read_bytes().decode("utf-8-sig")
    if PREFIX not in text:
        return set()
    block = read(path)
    if kind == "focus":
        return {scalar(entry.value, "id") for entry in walk(block) if entry.key in ("focus", "shared_focus") and isinstance(entry.value, tuple) and any(item.key == "id" for item in entry.value)}
    if kind == "idea":
        return {entry.key for ideas in children(block, "ideas") for group in ideas if isinstance(group.value, tuple) for entry in group.value if isinstance(entry.value, tuple)}
    if kind == "decision":
        return {entry.key for category in block if isinstance(category.value, tuple) for entry in category.value if isinstance(entry.value, tuple)}
    if kind == "event":
        return {scalar(entry.value, "id") for entry in block if entry.key == "country_event" and isinstance(entry.value, tuple)}
    return set(named(block))


# [2026-09-22]_kpopmodder: Check fresh IDs against physical host/schema databases and the compat definition closure.
def check_new_id_collisions(groups: dict[str, tuple[set[str], str]], expected_paths: set[str]) -> None:
    for kind, (identifiers, directory) in groups.items():
        for root in (ROOT, RT56_ROOT, VANILLA_ROOT):
            for path in (root / directory).rglob("*.txt"):
                relative = path.relative_to(root).as_posix()
                if kind == "decision" and "/categories/" in relative:
                    continue
                if root == ROOT and relative in expected_paths:
                    continue
                clashes = identifiers & definition_ids(path, kind)
                require(not clashes, f"new {kind} IDs collide in {path}: {sorted(clashes)}")


def source_equivalence(manifest: dict) -> None:
    """Allow only the manifest's exact icon substitutions and earlier port edits."""
    # [2026-09-22]_kpopmodder: Compare complete ordered blocks; never discard all icon/picture fields.
    for relative in (FOCUS_PATH, *IDEA_PATHS):
        data = read_source_file(relative, updated=True)
        data = replace_tokens(data, {**PROVINCE_ID_MAP, **STATE_ID_MAP})
        expected = parse(apply_post_migration_fixes(relative, data).decode("utf-8-sig"))
        if relative == FOCUS_PATH:
            focuses = focus_blocks(expected)
            entries = {row["id"]: row for row in manifest["focuses"]}
            tree = one(expected, "focus_tree")
            updated = []
            for entry in tree:
                if entry.key != "focus" or not isinstance(entry.value, tuple):
                    updated.append(entry)
                    continue
                block = entry.value
                identifier = scalar(block, "id")
                if identifier in entries:
                    row = entries[identifier]
                    require(scalar(block, "icon") == row["previous_reference"], f"unreviewed prior focus icon: {identifier}")
                    block = replace_entry(block, ("icon",), row["new_reference"])
                if identifier == "KOR_independent_party_in_power":
                    reward = one(block, "completion_reward") + parse("""
                        if = {
                            limit = { OR = { has_idea = civilian_economy has_idea = low_economic_mobilisation } }
                            add_ideas = partial_economic_mobilisation
                        }
                    """)
                    block = replace_entry(block, ("completion_reward",), reward)
                updated.append(Entry(entry.key, entry.op, block))
            require(set(entries) <= set(focuses), "manifest refers to an unknown source focus")
            expected = replace_entry(expected, ("focus_tree",), tuple(updated))
        else:
            ideas = named(one(one(expected, "ideas"), "country"))
            for row in (item for item in manifest["ideas"] if item["source_file"] == relative):
                identifier = row["id"]
                require(scalar(ideas[identifier], "picture") == row["previous_reference"], f"unreviewed prior idea picture: {identifier}")
                expected = replace_entry(expected, ("ideas", "country", identifier, "picture"), row["new_reference"])
        require(read(ROOT / relative) == expected, f"script differs beyond approved icon/map/MAN/economy edits: {relative}")


def check_icon_assets(focuses: dict[str, Block], added: set[str], ideas: dict[str, Block]) -> None:
    # [2026-09-22]_kpopmodder: Require full consumer, DDS, registry and animation-reference closure.
    manifest = json.loads(ICON_MANIFEST.read_text(encoding="utf-8-sig"))
    textures: set[str] = set()
    expected_sprites: dict[str, str] = {}
    for kind, definitions, field, count, dimensions in (
        ("focuses", {identifier: focuses[identifier] for identifier in added}, "icon", 60, (100, 88)),
        ("ideas", ideas, "picture", 29, (60, 68)),
    ):
        rows = manifest[kind]
        require(len(rows) == count and {row["id"] for row in rows} == set(definitions), f"icon manifest {kind} coverage differs")
        for row in rows:
            identifier, reference, texture = row["id"], row["new_reference"], row["texture"]
            require(row["source_file"] == FOCUS_PATH if kind == "focuses" else row["source_file"] in IDEA_PATHS,
                    f"unexpected icon consumer source: {identifier}")
            require(scalar(definitions[identifier], field) == reference, f"wrong {field} mapping: {identifier}")
            directory = "goals" if kind == "focuses" else "ideas"
            require(texture.startswith(f"gfx/interface/{directory}/HOK_KOR/") and texture.endswith(".dds")
                    and ".." not in Path(texture).parts and "\\" not in texture, f"unsafe icon texture path: {texture}")
            require(texture not in textures, f"icon texture reused unexpectedly: {texture}")
            textures.add(texture)
            data = (ROOT / texture).read_bytes()
            require(hashlib.sha256(data).hexdigest() == row["sha256"].lower(), f"icon DDS hash differs: {texture}")
            require(len(data) >= 128 and data[:4] == b"DDS ", f"invalid DDS header: {texture}")
            header = struct.unpack("<31I", data[4:128])
            width, height = dimensions
            require(header[0] == 124 and (header[3], header[2]) == dimensions
                    and header[18:26] == (32, 65, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
                    and header[6] in (0, 1) and len(data) == 128 + width * height * 4,
                    f"expected {width}x{height} BGRA32 alpha DDS: {texture}")
            sprite = reference if kind == "focuses" else "GFX_idea_" + reference
            require(sprite not in expected_sprites, f"icon sprite reused: {sprite}")
            expected_sprites[sprite] = texture
            if kind == "focuses":
                expected_sprites[sprite + "_shine"] = texture
    require(len(textures) == 89 and len(expected_sprites) == 149, "expected 89 textures and 149 icon sprites")
    sprites: dict[str, Block] = {}
    for relative, expected_count in zip(ICON_GFX_PATHS, (60, 60, 29)):
        registry = one(read(ROOT / relative), "spriteTypes")
        require(len(registry) == expected_count, f"unexpected sprite count: {relative}")
        for entry in registry:
            require(entry.key.lower() == "spritetype" and isinstance(entry.value, tuple), f"unexpected sprite registry entry: {relative}")
            identifier = scalar(entry.value, "name")
            require(identifier in expected_sprites and identifier not in sprites, f"unknown/duplicate imported sprite: {identifier}")
            sprites[identifier] = entry.value
    require(set(sprites) == set(expected_sprites), "imported sprite registry coverage differs")
    vanilla_shine = (VANILLA_ROOT / "interface/goals_shine.gfx").read_text(encoding="utf-8-sig")
    template_start = re.search(r'(?mi)^[ \t]*spriteType\s*=\s*\{\s*name\s*=\s*"GFX_focus_generic_electrification_shine"', vanilla_shine)
    require(template_start is not None, "missing target-version electrification shine template")
    opening = vanilla_shine.index("{", template_start.start(), template_start.end())
    template = parse(vanilla_shine[template_start.start():matching_brace(vanilla_shine, opening)])[0].value
    require(isinstance(template, tuple) and scalar(template, "effectFile") == SHINE_EFFECT, "target-version shared shine effect differs")
    for identifier, block in sprites.items():
        texture = expected_sprites[identifier]
        require(scalar(block, "texturefile") == texture, f"sprite texture mapping differs: {identifier}")
        if identifier.endswith("_shine"):
            # [2026-09-22]_kpopmodder: Vanilla registers buttonstate.lua as an effect ID, not a literal installed file.
            require(scalar(block, "effectFile") == SHINE_EFFECT, f"unreviewed shared shine effect: {identifier}")
            animations = children(block, "animation")
            require(len(animations) == 2, f"expected two shine animations: {identifier}")
            for animation in animations:
                require(scalar(animation, "animationmaskfile") == texture, f"shine mask is not the local icon DDS: {identifier}")
                require(scalar(animation, "animationtexturefile") == SHINE_OVERLAY
                        and (VANILLA_ROOT / SHINE_OVERLAY).is_file(), f"missing shared vanilla shine overlay: {identifier}")
        for entry in walk(block):
            if entry.key.lower() in ("texturefile", "animationmaskfile", "animationtexturefile", "effectfile"):
                allowed = {texture, SHINE_OVERLAY, SHINE_EFFECT} if identifier.endswith("_shine") else {texture}
                require(entry.value in allowed, f"unreviewed sprite dependency: {identifier}/{entry.value}")
    declarations = re.compile(r'\bname\s*=\s*"?([A-Za-z0-9_]+)"?')
    for root in (ROOT, RT56_ROOT, VANILLA_ROOT):
        for path in (root / "interface").rglob("*.gfx"):
            if root == ROOT and path.relative_to(root).as_posix() in ICON_GFX_PATHS:
                continue
            found = set(declarations.findall(mask_comments(path.read_bytes().decode("utf-8-sig"))))
            require(not found & sprites.keys(), f"imported sprite ID collides in {path}: {sorted(found & sprites.keys())}")
    source_equivalence(manifest)


def check_reference_closure(focuses: dict[str, Block], added: set[str], ideas: dict[str, Block], decisions: dict[str, Block], categories: dict[str, Block], events: dict[str, Block], relation: dict[str, Block], blocks: list[Block]) -> None:
    locales = {locale: localisation_keys(ROOT, locale) for locale in ("english", "korean")}
    required_loc = set(added) | set(ideas) | set(decisions) | set(categories)
    required_loc |= {identifier + "_desc" for identifier in required_loc}
    for entry in (item for block in blocks for item in walk(block)):
        if entry.key in ("custom_effect_tooltip", "custom_modifier_tooltip") and isinstance(entry.value, str):
            required_loc.add(entry.value)
        if entry.key in ("title", "desc", "name") and isinstance(entry.value, str) and entry.value.startswith(PREFIX + "democratic_expansion."):
            required_loc.add(entry.value)
        targets = {"has_completed_focus": focuses, "relative_position_id": focuses, "unlock_decision_tooltip": decisions,
                   "add_idea": ideas, "remove_idea": ideas, "has_idea": ideas, "add_ideas": ideas, "idea": ideas}
        if entry.key in targets and isinstance(entry.value, str) and entry.value.startswith(PREFIX):
            require(entry.value in targets[entry.key], f"unresolved {entry.key}: {entry.value}")
        if entry.key == "country_event" and isinstance(entry.value, tuple):
            identifier = scalar(entry.value, "id")
            if identifier.startswith(PREFIX):
                require(identifier in events, f"unresolved new event: {identifier}")
        if entry.key in ("add_relation_modifier", "remove_relation_modifier") and isinstance(entry.value, tuple):
            require(scalar(entry.value, "modifier") in relation, "unresolved bilateral relation modifier")
    for locale, keys in locales.items():
        require(not required_loc - keys, f"missing {locale} expansion strings: {sorted(required_loc - keys)}")
    for part in ("democratic_expansion", "expansion_navigation", "industry_expansion", "military_expansion"):
        payloads = []
        for locale in ("english", "korean"):
            path = ROOT / f"localisation/{locale}/HOK_KOR_{part}_l_{locale}.yml"
            raw = path.read_bytes()
            require(raw.startswith(b"\xef\xbb\xbf"), f"new localisation lacks BOM: {path}")
            lines = raw.decode("utf-8-sig").splitlines()
            require(lines[0].strip() == f"l_{locale}:", f"new localisation header changed: {path}")
            payloads.append(lines[1:])
        require(payloads[0] == payloads[1], f"paired HOK Korean text diverges: {part}")
    required_sprites = {scalar(focuses[identifier], "icon") for identifier in added}
    required_sprites |= {scalar(event, "picture") for event in events.values()}
    required_sprites |= {"GFX_idea_" + scalar(idea, "picture") for idea in ideas.values()}
    # Vanilla SWE.txt uses decision_generic_construction; other decisions use generic_* suffixes.
    decision_icons = {scalar(decision, "icon") for decision in decisions.values()}
    required_sprites |= {("GFX_" if icon.startswith("decision_") else "GFX_decision_") + icon for icon in decision_icons}
    required_sprites |= {"GFX_decision_category_" + scalar(category, "icon") for category in categories.values()}
    # [2026-09-22]_kpopmodder: Inspect referenced sprite blocks, not unrelated host UI roots with upstream brace defects.
    sprites: dict[str, Block] = {}
    sprite_start = re.compile(r"(?mi)^[ \t]*spriteType\s*=\s*\{")
    for path in effective_files("interface", "*.gfx"):
        text = path.read_bytes().decode("utf-8-sig")
        clean = mask_comments(text)
        if not any(identifier in clean for identifier in required_sprites):
            continue
        for match in sprite_start.finditer(clean):
            opening = clean.find("{", match.start(), match.end())
            end = matching_brace(text, opening)
            parsed = parse(text[match.start():end])
            require(len(parsed) == 1 and isinstance(parsed[0].value, tuple), f"invalid referenced sprite block in {path}")
            block = parsed[0].value
            identifier = scalar(block, "name")
            if identifier in required_sprites:
                sprites[identifier] = block
    for sprite in required_sprites:
        require(sprite in sprites, f"missing expansion sprite: {sprite}")
        textures = [entry.value for entry in sprites[sprite] if entry.key.lower() == "texturefile"]
        require(bool(textures), f"sprite lacks texture: {sprite}")
        for texture in textures:
            require(any((root / texture).is_file() for root in (ROOT, RT56_ROOT, VANILLA_ROOT)), f"sprite texture missing: {sprite}/{texture}")
    tech_ids, categories_used = set(), set()
    for path in effective_files("common/technologies"):
        for technology in children(read(path), "technologies"):
            for entry in technology:
                if isinstance(entry.value, tuple):
                    tech_ids.add(entry.key)
                    for category_block in children(entry.value, "categories"):
                        categories_used.update(item.key for item in category_block)
    wanted_mios = {entry.key[4:] for identifier in added for entry in walk(focuses[identifier]) if entry.key.startswith("mio:")}
    mio_ids = set()
    for path in effective_files("common/military_industrial_organization/organizations"):
        text = path.read_bytes().decode("utf-8-sig")
        if any(identifier in mask_comments(text) for identifier in wanted_mios):
            mio_ids.update(entry.key for entry in read(path) if isinstance(entry.value, tuple))
    for identifier in added:
        for entry in walk(focuses[identifier]):
            if entry.key == "technology":
                require(entry.value in tech_ids, f"missing current technology: {identifier}/{entry.value}")
            elif entry.key == "category":
                require(entry.value in categories_used, f"unused current technology category: {identifier}/{entry.value}")
            elif entry.key == "set_technology" and isinstance(entry.value, tuple):
                require(all(item.key == "popup" or item.key in tech_ids for item in entry.value), f"missing granted technology: {identifier}")
            elif entry.key.startswith("mio:"):
                require(entry.key[4:] in mio_ids, f"missing current MIO: {identifier}/{entry.key}")


def check_ideas(ideas: dict[str, Block]) -> None:
    expected = {
        "energy_coordination_1": ("factory_energy_consumption", "-0.10"),
        "energy_coordination_2": ("factory_energy_consumption", "-0.20"),
        "energy_coordination_3": ("factory_energy_consumption", "-0.30"),
        "workforce_1": ("production_factory_efficiency_gain_factor", "0.30"),
        "workforce_2": ("production_factory_efficiency_gain_factor", "0.60"),
        "night_school_spirit": ("research_speed_factor", "0.10"),
        "mass_production_1": ("production_factory_max_efficiency_factor", "0.15"),
        "mass_production_2": ("production_factory_max_efficiency_factor", "0.30"),
        "flexible_production_1": ("line_change_production_efficiency_factor", "0.20"),
        "flexible_production_2": ("line_change_production_efficiency_factor", "0.40"),
        "quality_control": ("production_factory_start_efficiency_factor", "0.10"),
        "procurement_spirit_2": ("production_factory_max_efficiency_factor", "0.10"),
        "accountable_administration_idea": ("political_power_gain", "0.25"),
        "public_accounts_idea": ("political_power_gain", "0.25"),
        "rural_education_idea": ("research_speed_factor", "0.10"),
        "volunteer_supply_idea": ("supply_consumption_factor", "-0.10"),
        "formation_spirit_1": ("air_mission_efficiency", "0.10"),
        "formation_spirit_2": ("air_mission_efficiency", "0.30"),
    }
    require(len(ideas) == 29, "expected 29 expansion ideas")
    for suffix, (modifier, value) in expected.items():
        require(scalar(one(ideas[PREFIX + suffix], "modifier"), modifier) == value, f"latest idea reward changed: {suffix}/{modifier}")
    for stage in (1, 2):
        require(scalar(one(ideas[f"HOK_KOR_mass_production_{stage}"], "modifier"), "line_change_production_efficiency_factor") == "-0.05", "mass-production tradeoff removed")
        require(scalar(one(ideas[f"HOK_KOR_flexible_production_{stage}"], "modifier"), "production_factory_max_efficiency_factor") == "-0.025", "flexible-production tradeoff removed")
    for suffix in ("procurement_spirit_1", "procurement_spirit_2"):
        require(not any(entry.key in ("equipment_bonus", "production_factory_efficiency_gain_factor", "industrial_capacity_factory") for entry in walk(ideas[PREFIX + suffix])), "unapproved infantry-production bonus was introduced")
    treaty = ideas["HOK_KOR_license_participant_idea"]
    for callback, effect in (("on_add", "add_relation_modifier"), ("on_remove", "remove_relation_modifier")):
        body = one(treaty, callback)
        require(one(body, effect) == parse("target = KOR modifier = HOK_KOR_asian_license_relation"), f"treaty direct callback changed: {callback}")
        require(one(one(body, "KOR"), effect) == parse("target = PREV modifier = HOK_KOR_asian_license_relation"), f"treaty reciprocal callback changed: {callback}")


def check_consent_events(events: dict[str, Block], ideas: dict[str, Block]) -> None:
    # [2026-09-22]_kpopmodder: Keep acceptance, repeated eligibility checks, finite duration and refusal separate.
    eligibility = parse("NOT = { tag = KOR } FROM = { tag = KOR exists = yes is_faction_leader = yes has_government = democratic } is_in_faction_with = FROM NOT = { has_war_with = FROM }")
    cancellation = parse("OR = { NOT = { country_exists = KOR } NOT = { is_in_faction_with = KOR } has_war_with = KOR KOR = { is_faction_leader = no } KOR = { NOT = { has_government = democratic } } }")
    for number, idea, accepted, refused in ((1, "HOK_KOR_customs_participant_idea", 2, 3), (4, "HOK_KOR_license_participant_idea", 5, 6)):
        options = children(events[f"HOK_KOR_democratic_expansion.{number}"], "option")
        require(len(options) == 2, "treaty needs separate acceptance/refusal options")
        accept, decline = options
        expected = (parse('has_dlc = "Death or Dishonor"') if number == 4 else ()) + eligibility
        require(one(accept, "trigger") == expected, "treaty acceptance eligibility changed")
        effect = one(accept, "if")
        require(one(effect, "limit") == expected + parse(f"NOT = {{ has_idea = {idea} }}"), "treaty completion must recheck faction/peace/leader and existing agreement")
        require(one(effect, "add_timed_idea") == parse(f"idea = {idea} days = 730"), "treaty duration/grant changed")
        require(one(one(effect, "FROM"), "country_event") == parse(f"id = HOK_KOR_democratic_expansion.{accepted} hours = 6"), "acceptance notice receiver changed")
        reject_effect = one(decline, "if")
        require(one(reject_effect, "limit") == parse("FROM = { exists = yes }"), "refusal must guard a surviving inviter")
        require(one(one(reject_effect, "FROM"), "country_event") == parse(f"id = HOK_KOR_democratic_expansion.{refused} hours = 6"), "refusal notice receiver changed")
        require(not any(entry.key in ("add_ideas", "add_timed_idea", "add_relation_modifier") for entry in walk(decline)), "declining a treaty grants its benefits")
        require(one(ideas[idea], "cancel") == cancellation, "treaty cancellation on relationship/government loss changed")


def replace_entry(block: Block, path: tuple[str, ...], value: str | Block | None) -> Block:
    """Change one in-memory fixture only; no files are written by mutation tests."""
    require(sum(entry.key == path[0] for entry in block) == 1, f"ambiguous mutation path {path}")
    result = []
    for entry in block:
        if entry.key != path[0]:
            result.append(entry)
        elif len(path) > 1:
            require(isinstance(entry.value, tuple), f"non-block mutation path {path}")
            result.append(Entry(entry.key, entry.op, replace_entry(entry.value, path[1:], value)))
        elif value is not None:
            result.append(Entry(entry.key, entry.op, value))
    return tuple(result)


def run_self_tests() -> None:
    # [2026-09-22]_kpopmodder: Fail if a guard regression survives; fixtures are immutable in-memory copies.
    focuses = focus_blocks(read(ROOT / FOCUS_PATH))
    baseline = focus_blocks(parse(read_source_file(FOCUS_PATH, updated=False).decode("utf-8-sig")))
    source = focus_blocks(parse(read_source_file(FOCUS_PATH, updated=True).decode("utf-8-sig")))
    added = check_focus_contract(focuses, baseline, source)
    plans = named(read(ROOT / AI_PATH))
    check_ai(plans, focuses, added)
    decisions = {identifier: body for relative in DECISION_PATHS for category in named(read(ROOT / relative)).values() for identifier, body in named(category).items()}
    ideas = {identifier: body for relative in IDEA_PATHS for identifier, body in named(one(one(read(ROOT / relative), "ideas"), "country")).items()}
    events = {scalar(body, "id"): body for body in children(read(ROOT / EVENT_PATH), "country_event")}
    check_regional_projects(decisions)
    check_allied_projects(decisions)
    check_school(focuses["HOK_KOR_technical_civic_schools"])
    check_ideas(ideas)
    check_consent_events(events, ideas)
    caught = []

    def rejects(label, action):
        try:
            action()
        except (ValueError, KeyError, StopIteration):
            caught.append(label)
        else:
            raise ValueError(f"mutation was not detected: {label}")

    regional = "HOK_KOR_gangwon_industry_project"
    mutations = (
        ("regional ownership guard", ("available", "1144", "is_owned_by"), None),
        ("regional control guard", ("available", "1144", "is_fully_controlled_by"), None),
        ("regional completion space guard", ("remove_effect", "if", "limit", "1144", "free_building_slots"), None),
        ("regional mapped highlight", ("highlight_states", "highlight_state_targets", "state"), "1029"),
        ("regional repeatability", ("fire_only_once",), "yes"),
        ("regional cancellation reward", ("cancel_effect",), parse("add_political_power = 150")),
        ("regional duplicate construction reward", ("remove_effect", "if", "1144", "add_building_construction", "level"), "2"),
    )
    for label, path, value in mutations:
        changed = {**decisions, regional: replace_entry(decisions[regional], path, value)}
        rejects(label, lambda changed=changed: check_regional_projects(changed))
    ally = "HOK_KOR_finance_allied_industry"
    locked = replace_entry(decisions[ally], ("available",), one(decisions[ally], "available") + parse("NOT = { has_country_flag = HOK_KOR_industrial_project_completed }"))
    rejects("allied historical flag lock", lambda: check_allied_projects({**decisions, ally: locked}))
    school = replace_entry(focuses["HOK_KOR_technical_civic_schools"], ("completion_reward", "if", "limit", "919", "is_fully_controlled_by"), None)
    rejects("school completion ownership loss", lambda: check_school(school))
    first = sorted(added)[0]
    duration = {**focuses, first: replace_entry(focuses[first], ("cost",), "10")}
    rejects("new focus duration", lambda: check_focus_contract(duration, baseline, source))
    defense = "HOK_KOR_historical_defense_plan"
    bad_abort = {**plans, defense: replace_entry(plans[defense], ("abort",), parse("always = no"))}
    rejects("AI support never aborts", lambda: check_ai(bad_abort, focuses, added))
    workforce = "HOK_KOR_workforce_2"
    bad_reward = {**ideas, workforce: replace_entry(ideas[workforce], ("modifier", "production_factory_efficiency_gain_factor"), "0.20")}
    rejects("stale workforce reward", lambda: check_ideas(bad_reward))
    customs = "HOK_KOR_democratic_expansion.1"
    options = children(events[customs], "option")
    changed_option = replace_entry(options[0], ("if", "add_timed_idea", "days"), "7300")
    changed_event = tuple(Entry(entry.key, entry.op, changed_option) if entry.key == "option" and entry.value == options[0] else entry for entry in events[customs])
    rejects("treaty duration drift", lambda: check_consent_events({**events, customs: changed_event}, ideas))
    print(f"PASS mutation self-test: {len(caught)} regressions rejected; positive fixtures accepted; no production writes")


def run_checks() -> None:
    focus_doc = read(ROOT / FOCUS_PATH)
    focuses = focus_blocks(focus_doc)
    baseline = focus_blocks(parse(read_source_file(FOCUS_PATH, updated=False).decode("utf-8-sig")))
    source = focus_blocks(parse(read_source_file(FOCUS_PATH, updated=True).decode("utf-8-sig")))
    added = check_focus_contract(focuses, baseline, source)
    check_ai(named(read(ROOT / AI_PATH)), focuses, added)
    ideas = {}
    counts = []
    for relative in IDEA_PATHS:
        definitions = named(one(one(read(ROOT / relative), "ideas"), "country"))
        counts.append(len(definitions))
        require(not ideas.keys() & definitions.keys(), "duplicate new idea")
        ideas.update(definitions)
    require(counts == [11, 12, 6], "expected industrial/military/democratic ideas 11/12/6")
    check_icon_assets(focuses, added, ideas)
    decisions, category_definitions, category_consumers = {}, {}, set()
    for relative in DECISION_PATHS:
        for category, body in named(read(ROOT / relative)).items():
            category_consumers.add(category)
            entries = named(body)
            require(not decisions.keys() & entries.keys(), "duplicate new decision")
            decisions.update(entries)
        category_definitions.update(named(read(ROOT / relative.replace("common/decisions/", "common/decisions/categories/"))))
    require(len(decisions) == 10 and len(category_definitions) == 3 and category_consumers == set(category_definitions), "decision/category closure must be 10/3")
    event_blocks = children(read(ROOT / EVENT_PATH), "country_event")
    events = {scalar(event, "id"): event for event in event_blocks}
    require(len(events) == len(event_blocks) == 6 and set(events) == {f"HOK_KOR_democratic_expansion.{number}" for number in range(1, 7)}, "expected six unique expansion events")
    require(all(scalar(event, "is_triggered_only") == "yes" for event in events.values()), "expansion event can fire unsolicited")
    relation = named(read(ROOT / "common/modifiers/HOK_KOR_democratic_expansion.txt"))
    require(set(relation) == {"HOK_KOR_asian_license_relation"}, "unexpected expansion relation modifier")
    check_regional_projects(decisions)
    check_school(focuses["HOK_KOR_technical_civic_schools"])
    check_allied_projects(decisions)
    check_ideas(ideas)
    check_consent_events(events, ideas)
    blocks = [focuses[identifier] for identifier in added] + list(ideas.values()) + list(decisions.values()) + list(category_definitions.values()) + list(events.values())
    groups = {"focus": (added, "common/national_focus"), "idea": (set(ideas), "common/ideas"),
              "decision": (set(decisions), "common/decisions"), "category": (set(category_definitions), "common/decisions/categories"),
              "event": (set(events), "events"), "modifier": (set(relation), "common/modifiers"),
              "AI": (set(named(read(ROOT / AI_PATH))) - {"KOR_historical_plan"}, "common/ai_strategy_plans")}
    check_new_id_collisions(groups, set(FOCUS_UPDATE_PATHS))
    check_reference_closure(focuses, added, ideas, decisions, category_definitions, events, relation, blocks)
    print("PASS Korean update: 266+60 focuses / 2 earlier + 152 expansion durations / 106+3 AI plans; reference and new-ID closure")
    print("PASS Korean contracts: 29 ideas / 10 decisions / 3 categories / 6 events; regional, civic-school, aid and bilateral guards")
    print("PASS Korean icons: exact 60 focus / 29 idea mappings; 89 BGRA32 DDS hashes; 149 unique sprites and local mask/shared shine closure")
    print("STATIC ONLY: These checks do not prove engine evaluation, decision repetition, AI timing, icon rendering, or gameplay.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        run_self_tests() if args.self_test else run_checks()
    except (OSError, UnicodeError, ValueError, KeyError, StopIteration) as exc:
        print(f"ERROR Korean expansion contract: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
