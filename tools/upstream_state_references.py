#!/usr/bin/env python3
"""Apply reviewed HOK reference fixes over the already integrated RT56 tree.

The caller supplies frozen donor inputs and owns output writes/provenance.
Foreign region IDs below are the reviewed RT56 geography, not donor IDs.
General Japanese/Chinese host repairs and the excluded MON challenge remain
with RT56.  This module does not read the live donor or write runtime files.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from korean_state_split_shared import Node, parse, walk


#20261108_kpopmodder: Restore Korean route geography without replacing RT56 world data.
_DONOR_HASHES = {
    "common/decisions/KOR_decision.txt": "9A22D108DC50533BFF5E9DED621B4DB826A1D29709F9996CFC629A3E6E7EC9E4",
    "common/national_focus/korea.txt": "1E465973FC220C227F91DCEF7DAE1E30D99E811C462F00198CEA30CCF0CB5365",
    "common/national_focus/japan.txt": "1A9E1135F0123E752D206A82420F716227402DD49EB0E8BF369931FA57423DAE",
    "events/korea.txt": "ABE66AF64D6FB0BF15FB18FCBB7BCBAC50306EB6B60E79D77B486401CA398206",
    "history/countries/KCH - Korean China.txt": "D2C3846411A246DED91481DFE8931B64CC6D4CBB56219EA6EF363944118B1984",
    "common/scripted_effects/00_HOK_KOR_state_reference_effects.txt": "5210AC742976AADC47D2B75CACB8F5FE01D4E544F2244959F167A6E1C8757B74",
    "common/script_constants/zzzz_HOK_KOR_state_reference_constants.txt": "F0C0D7C645E2C8381B96C77FF986DF03908874E791E535851253E4F6F5B8F72F",
}
_HOST_INPUTS = {
    "common/scripted_effects/SOV_scripted_effects.txt": (
        "rt56", "B9D5AC00450D561069C15E664A78DBCFF38D7D43F2F441F3CCE5572586BC82CD"),
    "common/script_constants/state_groups.txt": (
        "vanilla", "7B920231ED30F856E4BF8503C50115BBD961176E72465DEB2859FAC6EC4757B9"),
}

JAPAN_ADDITIONS = (1105, 1106, 1107)
CHINA_CORE_ADDITIONS = tuple(range(1111, 1126))
# RT56 geography was checked against state provinces, names and undated
# ownership/cores.  High province IDs reused in Brazil/Ethiopia are excluded.
REGIONS = {
    "KOR_liberation_of_indochina": ((671, 670, 741, 286), (924, 925, 926, 927, 928)),
    "KOR_liberation_of_philippine": ((623, 327, 625, 624, 627, 626), (628, 1108, 1109, 1110)),
    "KOR_liberation_of_indonesia": ((672, 334, 335, 673, 667, 668, 669),
        (446, 738, 909, 974, 975, 976, 977, 978, 1126, 1127, 1128, 1135, 1137, 1142, 1143)),
    "KOR_liberation_of_maleisia": ((336, 333), (914, 915, 916, 951, 960, 1014, 1129, 1130, 1131)),
    "KOR_liberation_of_pamanyungan": ((522, 520, 519, 521, 285, 517, 518), (674, 870, 871, 872, 873)),
    "KOR_liberation_of_aotearoa": ((723, 284), (1136, 1139, 1140)),
}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def _donor(root: Path, relative: str) -> bytes:
    data = (root / relative).read_bytes()
    if _sha(data) != _DONOR_HASHES[relative]:
        raise ValueError(f"reference donor input drift: {relative}")
    return data


def _host(root: Path, relative: str) -> bytes:
    provider, expected = _HOST_INPUTS[relative]
    data = (root.parent / "host" / provider / relative).read_bytes()
    if _sha(data) != expected:
        raise ValueError(f"reference host input drift: {provider}/{relative}")
    return data


def _decode(data: bytes) -> tuple[str, bytes]:
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    return data[len(bom):].decode("utf-8"), bom


def _newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _indent(text: str, position: int) -> str:
    return re.match(r"[ \t]*", text[text.rfind("\n", 0, position) + 1:position]).group()


def _splice(text: str, edits: list[tuple[int, int, str]]) -> str:
    boundary = len(text)
    for start, end, replacement in sorted(edits, reverse=True):
        if not 0 <= start <= end <= boundary:
            raise ValueError("overlapping reference transformations")
        text = text[:start] + replacement + text[end:]
        boundary = start
    return text


def _unique(nodes, predicate, label: str) -> Node:
    selected = [node for node in walk(nodes) if predicate(node)]
    if len(selected) != 1:
        raise ValueError(f"{label}: expected one block, found {len(selected)}")
    return selected[0]


def _block(text: str, identifier: str) -> Node:
    return _unique(parse(text), lambda n: n.block and
        (n.key == identifier or any(c.key == "id" and c.value == identifier for c in n.children)), identifier)


def _edit_block(text: str, identifier: str, transform) -> str:
    node = _block(text, identifier)
    return text[:node.start] + transform(text[node.start:node.end]) + text[node.end:]


def _insert_after_line(text: str, node: Node, lines: list[str]) -> tuple[int, int, str]:
    end = text.find("\n", node.end)
    if end < 0:
        raise ValueError("reference anchor has no following line")
    # An anchor occupying a line with a parent closing brace is not safe to
    # extend.  The reviewed old lists have one assignment/block per line.
    tail = text[node.end:end].strip()
    if tail and not tail.startswith("#"):
        raise ValueError(f"reference anchor has an unexpected line tail: {tail!r}")
    newline = _newline(text)
    indent = _indent(text, node.start)
    return end + 1, end + 1, "".join(indent + line + newline for line in lines)


def _expand_lists(text: str, keys: tuple[str, ...], old: tuple[int, ...], additions: tuple[int, ...], expected: int) -> str:
    edits = []
    groups = 0
    for parent in walk(parse(text)):
        if not parent.block:
            continue
        for key in keys:
            members = [n for n in parent.children if not n.block and n.key == key and n.value.isdigit()]
            if not members:
                continue
            values = tuple(int(n.value) for n in members)
            if set(values) != set(old) or len(values) != len(old):
                raise ValueError(f"unexpected {key} region list: {values}, expected {old}")
            groups += 1
            edits.append(_insert_after_line(text, members[-1], [
                "#20261108_kpopmodder: Include the reviewed RT56 successor states in the same regional path.",
                *[f"{key} = {state}" for state in additions],
            ]))
    if groups != expected:
        raise ValueError(f"region {old}: expected {expected} lists, found {groups}")
    return _splice(text, edits)


def _expand_cores(text: str, target: str, anchor: int, additions: tuple[int, ...]) -> str:
    matches = [node for node in walk(parse(text)) if node.block and node.key == str(anchor)
        and any(c.key == "add_core_of" and c.value == target for c in node.children)]
    if len(matches) != 1:
        raise ValueError(f"{target} core anchor {anchor}: expected one, found {len(matches)}")
    for node in walk(parse(text)):
        if node.block and node.key in {str(s) for s in additions} and any(c.key == "add_core_of" and c.value == target for c in node.children):
            raise ValueError(f"{target}: added core already present: {node.key}")
    return _splice(text, [_insert_after_line(text, matches[0], [
        "#20261108_kpopmodder: Preserve the existing regional core policy on its RT56 successors.",
        *[f"{state} = {{ add_core_of = {target} }}" for state in additions],
    ])])


def _replace_once(text: str, before: str, after: str, label: str) -> str:
    if text.count(before) != 1:
        raise ValueError(f"{label}: expected one source fragment, found {text.count(before)}")
    return text.replace(before, after, 1)


def _decision_references(text: str) -> str:
    #20261108_kpopmodder: Complete all matching condition/controller/civil-war/ordinary paths together.
    for identifier, (old, additions) in REGIONS.items():
        text = _edit_block(text, identifier, lambda block, old=old, additions=additions:
            _expand_lists(block, ("controls_state", "set_state_controller", "transfer_state"), old, additions, 4))
    def japan(block: str) -> str:
        old = (282, 528, 529, 530, 531, 532, 533, 534, 535, 536)
        block = _expand_lists(block, ("controls_state", "transfer_state"), old, JAPAN_ADDITIONS, 3)
        return _expand_cores(block, "KJP", 536, JAPAN_ADDITIONS)
    text = _edit_block(text, "KOR_establish_protectorate_states_of_japan", japan)
    text = _edit_block(text, "KOR_New_China_Government", lambda b: _expand_cores(b, "KCH", 756, CHINA_CORE_ADDITIONS))
    def tsushima(block: str) -> str:
        block = _replace_once(block, "set_state_name = STATE_KR_992", "set_state_name = STATE_KR_1027", "Tsushima name")
        return _replace_once(block, "transfer_state = 992", "transfer_state = 1147", "Tsushima transfer")
    return _edit_block(text, "KOR_admission_tsushima_to_the_federation", tsushima)


def _korean_focus_references(text: str) -> str:
    def haeju(block: str) -> str:
        candidates = [n for n in walk(parse(block)) if n.block and n.key == "1144" and
            any(c.key == "province" and c.value == "13540" for c in walk(n.children))]
        if len(candidates) != 1:
            raise ValueError("Haeju fort: expected one old Gangwon scope")
        node = candidates[0]
        original = block[node.start:node.end]
        replacement = _replace_once(original, "1144", "917", "Haeju state")
        replacement = _replace_once(replacement, "province = 13540", "province = 13559", "Haeju coastal province")
        replacement = ("#20261108_kpopmodder: Keep Haeju's three coastal-fort levels at its actual coastal province."
            + _newline(block) + _indent(block, node.start) + replacement)
        return _splice(block, [(node.start, node.end, replacement)])
    text = _edit_block(text, "KOR_port_fortification", haeju)
    text = _edit_block(text, "KOR_fall_of_the_sun", lambda b:
        _expand_lists(b, ("controls_state",), (282, 528, 529, 530, 531, 532, 533, 534, 535, 536), JAPAN_ADDITIONS, 1))
    def indochina(block: str) -> str:
        block = _expand_lists(block, ("has_full_control_of_state",), (670, 671, 286, 741), (924, 925, 926, 927, 928), 1)
        vin = _unique(parse(block), lambda n: n.block and n.key == "VIN" and
            any(c.key == "is_subject_of" and c.value == "FRA" for c in n.children), "Vietnam colonial alternative")
        if vin.parent is None or vin.parent.key != "OR":
            raise ValueError("Indochina request: unexpected colonial alternatives")
        lines = ["#20261108_kpopmodder: Support RT56's existing French Indochina subject without weakening its territorial checks.",
            "FRI = {", "\tis_subject_of = FRA"]
        for state in (670, 671, 286, 741, 924, 925, 926, 927, 928):
            lines.extend((f"\towns_state = {state}", f"\thas_full_control_of_state = {state}"))
        lines.append("}")
        return _splice(block, [_insert_after_line(block, vin, lines)])
    text = _edit_block(text, "KOR_freedom_to_indochina", indochina)
    return text


def _indochina_acceptance_guard() -> list[str]:
    #20261108_kpopmodder: Recheck the request's colonial owner and all nine states at acceptance, so a stale window cannot seize third-party land.
    lines = ["OR = {"]
    for holder in ("FRA", "VIN", "FRI"):
        lines.append(f"\t{holder} = {{")
        if holder != "FRA":
            lines.append("\t\tis_subject_of = FRA")
        for state in (670, 671, 286, 741, 924, 925, 926, 927, 928):
            lines.extend((f"\t\towns_state = {state}", f"\t\thas_full_control_of_state = {state}"))
        lines.append("\t}")
    lines.append("}")
    return lines


def _guard_indochina_acceptance(text: str) -> str:
    option = _unique(parse(text), lambda n: n.block and n.key == "option" and
        any(c.key == "name" and c.value == "kor_events.62.a" for c in n.children), "Indochina acceptance option")
    effects = [n for n in option.children if n.block and n.key in {"VIN", "KOR"}]
    if [n.key for n in effects] != ["VIN", "KOR"] or any(n.key == "available" for n in option.children):
        raise ValueError("Indochina acceptance: unexpected original effect order/availability")
    start, end = effects[0].start, effects[-1].end
    indent = _indent(text, start)
    nl = _newline(text)
    original = text[start:end].splitlines()
    nested = ["\t" + (line if index == 0 else line[len(indent):]) for index, line in enumerate(original)]
    guard = _indochina_acceptance_guard()
    lines = ["#20261108_kpopmodder: Recheck colonial ownership, full control and the French subject relation before transferring the region.",
        "trigger = {", *["\t" + line for line in guard], "}",
        "if = {", "\tlimit = {", *["\t\t" + line for line in guard], "\t}", *nested, "}"]
    replacement = nl.join(line if index == 0 else indent + line for index, line in enumerate(lines))
    return text[:start] + replacement + text[end:]


def _event_references(text: str) -> str:
    def indochina(block: str) -> str:
        block = _expand_lists(block, ("transfer_state",), (671, 286, 741, 670), (924, 925, 926, 927, 928), 1)
        # Retain the original federation-core policy for Laos/Cambodia only;
        # the Vietnamese successor states already have VIN cores in RT56.
        block = _expand_cores(block, "VIN", 741, (924, 925, 926))
        return _guard_indochina_acceptance(block)
    text = _edit_block(text, "kor_events.62", indochina)
    def malaya(block: str) -> str:
        nodes = parse(block)
        mal = _unique(nodes, lambda n: n.block and n.key == "MAL", "Malaya acceptance")
        anchor = _unique(mal.children, lambda n: not n.block and n.key == "set_cosmetic_tag", "Malaya cosmetic tag")
        indent = _indent(block, anchor.start)
        nl = _newline(block)
        lines = [
            "#20261108_kpopmodder: Transfer only the British-controlled RT56 Singapore state; Penang is already in MAL-owned Kedah.",
            "if = {", "\tlimit = { 336 = { is_owned_by = ENG is_core_of = MAL is_fully_controlled_by = ENG } }",
            "\ttransfer_state = 336", "}",
        ]
        addition = nl.join(indent + line for line in lines) + nl + indent
        return block[:anchor.start] + addition + block[anchor.start:]
    return _edit_block(text, "kor_events.63", malaya)


def _japanese_korean_fort(text: str) -> str:
    def fort(block: str) -> str:
        targets = [n for n in walk(parse(block)) if n.block and n.key == "add_building_construction" and
            any(c.key == "1003" or (c.key == "id" and c.value == "1003") for c in walk(n.children))]
        if len(targets) != 1:
            raise ValueError("Japanese Korean fort: expected one Haeju grant")
        grant = targets[0]
        if grant.parent is None or grant.parent.key != "527":
            raise ValueError("Japanese Korean fort: Haeju grant no longer under Pyongyang")
        provinces = _unique(grant.children, lambda n: n.block and n.key == "province", "Pyongyang fort provinces")
        ids = [(n.key, n.value) for n in provinces.children]
        if ids != [("id", "4052"), ("id", "1003")]:
            raise ValueError(f"Japanese Korean fort: unexpected province pool {ids}")
        haeju = provinces.children[1]
        line_start = block.rfind("\n", 0, haeju.start) + 1
        line_end = block.find("\n", haeju.end) + 1
        if line_end <= 0:
            raise ValueError("Japanese Korean fort: missing line ending")
        parent = grant.parent
        indent = _indent(block, parent.start)
        nl = _newline(block)
        lines = [
            "#20261108_kpopmodder: Keep Haeju's original three fort levels under its migrated state and actual control guard.",
            "IF = {", "\tlimit = { 917 = { state_is_fully_controlled_by_ROOT_subject_or_faction_member = yes } }",
            "\t917 = {", "\t\tadd_building_construction = {", "\t\t\ttype = bunker", "\t\t\tlevel = 3",
            "\t\t\tprovince = { id = 1003 }", "\t\t\tinstant_build = yes", "\t\t}", "\t}", "}",
        ]
        insertion = nl + nl.join(indent + line for line in lines)
        return _splice(block, [(line_start, line_end, ""), (parent.end, parent.end, insertion)])
    return _edit_block(text, "JAP_prepare_for_peninsular_warfare", fort)


def _soviet_effect(data: bytes) -> bytes:
    text, bom = _decode(data)
    node = _block(text, "SOV_start_civil_war")
    entries = [n for n in walk(node.children) if not n.block and n.key in {"attacker", "defender"} and n.value == "918"]
    if len(entries) != 4:
        raise ValueError(f"Soviet civil-war cleanup: expected four Korean endpoints, got {len(entries)}")
    edits = [(n.end - len(n.value), n.end, "1152") for n in entries]
    note = "#20261108_kpopmodder: Keep RT56 civil-war cleanup on the migrated North Hamgyeong border." + _newline(text)
    edits.append((node.start, node.start, note))
    return bom + _splice(text, edits).encode("utf-8")


def _border_constants(data: bytes) -> bytes:
    text, bom = _decode(data)
    node = _block(text, "comintern_starting_border")
    old = [n for n in node.children if n.key == "1028" and not n.op]
    if len(old) != 1:
        raise ValueError("Comintern border: expected the one inherited Korean entry")
    entry = old[0]
    note = "#20261108_kpopmodder: Track the Soviet border in North Hamgyeong after the HOK state split." + _newline(text) + _indent(text, entry.start)
    return bom + _splice(text, [(entry.start, entry.end, note + "1152")]).encode("utf-8")


def apply_references(relative: str, base: bytes, donor_root: Path) -> bytes:
    """Transform only reviewed reference consumers; leave other bytes intact."""
    if relative not in {
        "common/decisions/KOR_decision.txt", "common/national_focus/korea.txt",
        "common/national_focus/japan.txt", "events/korea.txt",
        "history/countries/KCH - Korean China.txt",
    }:
        return base
    _donor(donor_root, relative)
    text, bom = _decode(base)
    if relative == "common/decisions/KOR_decision.txt":
        text = _decision_references(text)
    elif relative == "common/national_focus/korea.txt":
        text = _korean_focus_references(text)
    elif relative == "common/national_focus/japan.txt":
        text = _japanese_korean_fort(text)
    elif relative == "events/korea.txt":
        text = _event_references(text)
    else:
        text = _replace_once(text, "capital = 613 # Nanjing",
            "#20261108_kpopmodder: Keep the intended Nanjing capital at its actual RT56 state parent."
            + _newline(text) + "capital = 1114 # Nanjing", "KCH Nanjing capital")
    return bom + text.encode("utf-8")


def reference_additions(donor_root: Path) -> dict[str, bytes]:
    """Return two same-path full-host merges, avoiding duplicate global IDs."""
    _donor(donor_root, "common/scripted_effects/00_HOK_KOR_state_reference_effects.txt")
    _donor(donor_root, "common/script_constants/zzzz_HOK_KOR_state_reference_constants.txt")
    soviet = "common/scripted_effects/SOV_scripted_effects.txt"
    constants = "common/script_constants/state_groups.txt"
    return {soviet: _soviet_effect(_host(donor_root, soviet)), constants: _border_constants(_host(donor_root, constants))}
