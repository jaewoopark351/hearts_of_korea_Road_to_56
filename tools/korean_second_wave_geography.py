#!/usr/bin/env python3
"""Deterministic regional adaptations for the selected second-wave HOK content.

This module never writes runtime files. The Korean update builder owns them.
See ADR-0005 for the distinction between policy areas and stronghold gates.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from migrate_hok_ids import identified_block_span, matching_brace


REPO_ROOT = Path(__file__).resolve().parents[1]
ROOTS = {
    "vanilla": Path(r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"),
    "rt56": Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968"),
    "donor": Path(r"C:\hoi\hearts_of_korea"),
}

#20260923_kpopmodder: Fail closed if the physical geography used by ADR-0005 changes.
GEOGRAPHY_HASHES = {
    "vanilla/history/states/328-Manchukuo.txt": "921AEF182C9D5FC8BD4DA7798BF346FF33017ADBD17CEC4A5170AA4ADF889F78",
    "vanilla/history/states/610-China 9.txt": "AEAD28E96028163C7945C340E7BB28629F1F48003D1253A6F93AC897CAE57BBC",
    "vanilla/history/states/714-Heilungkiang.txt": "995EE98D4151F9FA4AA04C0F8CE949250A256C19BC4CBFCD39ACB7E8F4674F00",
    "vanilla/history/states/715-Liaoning.txt": "9F9F136867CA734BF45896C2590AE56920EAAB4787AAA3088388D0E0CFBA27BA",
    "vanilla/history/states/716-Liaotung.txt": "1FF3BBE697116617B9DC5DDD5BC7CD2513C7D8AE2D029B3DD71E17CB2A8B83E8",
    "vanilla/history/states/717-Chuho.txt": "BAE825BCE6062E941F223AC29AFCB18C00B193E34EE76A6A8C6798922E0822A2",
    "vanilla/history/states/745-Dalian.txt": "7A40919EAABC7ACBCB3BBA47DD10E11CF3467EA1D7EA5DF27DEAC8B426FDAA10",
    "vanilla/history/states/761-Hulunbuir.txt": "7CA441AE866EFACD714EB684A2DFB7205AA8EDB9E016061B11BCC3BF4AC024B4",
    "rt56/history/states/328-Manchukuo.txt": "046F0C560A4113FE4ECEBE7AF555223B30D6768721B63A59C4C1F1837481CBDC",
    "rt56/history/states/609-China 8.txt": "4DE1B89404CFD908D9643522CCF780A47B2029D8F105C924B8CA710BCFE8D5F4",
    "rt56/history/states/610-China 9.txt": "C3E4EAC51CA9353C54EA19D3D9A64050E10F8B519222D636E56F90A06FBC3336",
    "rt56/history/states/714-Heilungkiang.txt": "8B3B5106D7905CD85900FE96E0EA58730D3244FD0E69CBA1483B33B609FEE492",
    "rt56/history/states/715-Liaoning.txt": "36370D4CE0B756711757DB686B29247E3BB77541609B207E4591E984CD79268F",
    "rt56/history/states/716-Liaotung.txt": "22227E0070197368526DFDE9966E210A06B504D22DF9809CFCBA44BF15FBFC0D",
    "rt56/history/states/717-Chuho.txt": "C0E36D7A29EC40FF3EE996F6F2F4CAF243F98641FD4494883E783B8FEB08C40A",
    "rt56/history/states/745-Dalian.txt": "FC117A18D0508CE7896444EB9610D4FD291E192AB32D4E97BD3B961B6A03356E",
    "rt56/history/states/761-Hulunbuir.txt": "DB15AB5D36745F029974BBC6E2E1C76557F3FE834940978FFF2265C974145826",
    "rt56/history/states/941-Andong.txt": "8A8C80BBCF4B8BC84CDDBE053ED717662DECEFC4BFD563F280812DAAFFAD8708",
    "rt56/history/states/942-Jiandao.txt": "518D44DE6ECA56DBC2CDF9D8D79E4BF6FCA24D65EC8500D19363D25E1A5316B3",
    "rt56/history/states/943-Binjiang.txt": "021EAB70095A9905DA4D8E38CE08AA2D528F79477092B0D8F9962930E69524E1",
    "rt56/history/states/944-Longjiang.txt": "DFA2C74B954ABC0E979B0B56019538B4D901D5304786E8C7D87703E781F5E40E",
    "rt56/history/states/945-Heihe.txt": "0A5E1954B5A1021CD6B4A029263AEED6AFAA5F418F35982474EBB74146FE1A0B",
    "rt56/history/states/946-West Xing'an.txt": "E6B59FE8F0D63D5E376F0B711D1774FA92A9A28B0F184CF077BCDE7DDDCB021F",
    "rt56/history/states/947-Jinzhou.txt": "C3C799D6AF19BB54AFA1BA40BDC436C42DEE82A2ACCACB2012193214D7FEB5C5",
    "donor/map/provinces.bmp": "A00EC0E8C18E9F405FC7E7EA59A77848870F03C79E9E5F78CF6E12272D867600",
    "donor/map/definition.csv": "0DD53CE40928593FA59C4661863EA4257BDC1E3EC8FDA6D3F790C319A2F8F228",
    "rt56/map/provinces.bmp": "B41B67B844407C70EB393E6979DCB8EE718BA76596ECEB2A9CCD38171156580F",
    "rt56/map/definition.csv": "005BB6052AEDBAA85FFE4607B21398A33055624A78C2F822F116AE895B58393E",
}

#20260923_kpopmodder: Expand complete policy lifecycles over the reviewed host regions.
STATE_GROUPS = {328: (328, 941), 714: (714, 944, 945), 717: (717, 942, 943)}
POLICY_FOCUS_GROUPS = (
    ("county_dossiers", "payroll_registers", "service_counters", "dispute_records", "service_calendar"),
    ("interpreter_desks", "residence_certificates", "municipal_consultation", "shared_service_manuals", "community_mediation"),
    ("workshop_inventory", "metallurgical_trials", "material_recovery", "foundry_batches", "integrated_recovery"),
    ("tenancy_records", "sanitation_rounds", "housing_repairs", "market_inspections", "settled_municipality"),
)
POLICY_NAMES = ("local_services", "community_services", "material_recovery", "municipal_routine")
POLICY_SOURCE_STATES = ((328,), (328,), (328, 714, 717), (328,))
POLICY_TARGET_STATES = tuple(
    tuple(target for source in sources for target in STATE_GROUPS[source])
    for sources in POLICY_SOURCE_STATES
)
FOCUS_IDS = tuple("HOK_KOR_mc_" + suffix for group in POLICY_FOCUS_GROUPS for suffix in group)
HW_FOCUS_IDS = tuple("HOK_KOR_hw_" + suffix for suffix in (
    "provincial_inventory", "provision_accounts", "inspection_circuits", "supply_returns",
    "dispatch_codes", "courier_relays", "signal_logs", "relay_exercises",
    "postwar_dockets", "reconstruction_priorities", "civil_accountability",
    "veteran_rolls", "demobilization_schedule", "peacetime_training",
))

#20260923_kpopmodder: Keep one OR alternative per source region, requiring its complete reviewed host group.
STRONGHOLD_GROUPS = {
    716: (716,),
    745: (745,),
    328: (328, 941),
    717: (717, 942, 943),
    714: (714, 944, 945),
    761: (761,),
    715: (715, 946),
    610: (610, 947),
}
FOCUS_PATH = "common/national_focus/korea.txt"
DECISION_PATH = "common/decisions/HOK_KOR_manchurian_followup.txt"
LOCALISATION_PATHS = tuple(
    f"localisation/{language}/HOK_KOR_manchurian_followup_l_{language}.yml"
    for language in ("english", "korean")
)
TRANSFORM_PATHS = (FOCUS_PATH, DECISION_PATH, *LOCALISATION_PATHS)
LOCALISATION_NOTE = "#20260923_kpopmodder: Name the complete RT56 policy regions required by the imported operating projects."


def verify_geography_inputs() -> None:
    """Validate the evidence pins without changing the sources or production tree."""
    for key, expected in GEOGRAPHY_HASHES.items():
        root, relative = key.split("/", 1)
        source = ROOTS[root] / relative
        actual = hashlib.sha256(source.read_bytes()).hexdigest().upper()
        if actual != expected:
            raise ValueError(f"ADR-0005 source drift: {source}: expected {expected}, got {actual}")
    # These regions are inherited from vanilla, not from donor state overrides.
    for state_id in STRONGHOLD_GROUPS:
        for path in (ROOTS["donor"] / "history/states").glob("*.txt"):
            text = re.sub(r"#[^\n]*", "", path.read_text(encoding="utf-8-sig"))
            if re.search(rf"\bid\s*=\s*{state_id}\b", text):
                raise ValueError(f"new donor override invalidates ADR-0005: {path}")
    source_provinces = {}
    target_provinces = {}
    for key in GEOGRAPHY_HASHES:
        if "/history/states/" not in key:
            continue
        root, relative = key.split("/", 1)
        state_id = int(Path(relative).name.split("-", 1)[0])
        (source_provinces if root == "vanilla" else target_provinces)[state_id] = _state_provinces(ROOTS[root] / relative)
    for source, group in STRONGHOLD_GROUPS.items():
        for target in group:
            overlaps = {candidate: len(provinces & target_provinces[target]) for candidate, provinces in source_provinces.items()}
            winners = [candidate for candidate, count in overlaps.items() if count == max(overlaps.values())]
            if winners != [source]:
                raise ValueError(f"ADR-0005 dominant-province decision no longer holds for {target}: {overlaps}")


def _expand_state_scopes(text: str, expected: dict[int, int]) -> str:
    """Clone only reviewed state scopes; preserve nested effects and command order."""
    pattern = re.compile(r"(?<![A-Za-z_\d])(328|714|717)([ \t]*=[ \t]*\{)")
    matches = list(pattern.finditer(text))
    counts = {state: sum(int(match[1]) == state for match in matches) for state in expected}
    if counts != expected or any(int(match[1]) not in expected for match in matches):
        raise ValueError(f"unexpected source state scopes: expected {expected}, found {counts}")
    if re.search(r"\b(?:941|942|943|944|945)\s*=\s*\{", text):
        raise ValueError("refusing to re-expand an already adapted regional block")
    for match in reversed(matches):
        end = matching_brace(text, text.index("{", match.start(), match.end()))
        original = text[match.start():end]
        if re.search(pattern, original[match.end() - match.start():]):
            raise ValueError("nested regional state scopes require an explicit merge review")
        newline = "\r\n" if "\r\n" in text else "\n"
        prefix = text[text.rfind("\n", 0, match.start()) + 1:match.start()]
        separator = newline + prefix if "\n" in original else " "
        clones = [str(target) + original[len(match[1]):] for target in STATE_GROUPS[int(match[1])]]
        text = text[:match.start()] + separator.join(clones) + text[end:]
    return text


def _expand_strongholds(text: str) -> str:
    for source, targets in STRONGHOLD_GROUPS.items():
        original = f"AND = {{ owns_state = {source} has_full_control_of_state = {source} }}"
        if text.count(original) != 1:
            raise ValueError(f"expected exactly one original Hwan stronghold {source}")
        replacement = "AND = { " + " ".join(
            f"owns_state = {target} has_full_control_of_state = {target}" for target in targets
        ) + " }"
        text = text.replace(original, replacement, 1)
    return text


def _transform_focus(text: str) -> str:
    for index, group in enumerate(POLICY_FOCUS_GROUPS):
        for position, suffix in enumerate(group):
            identifier = "HOK_KOR_mc_" + suffix
            start, end = identified_block_span(text, "focus", identifier)
            count = 2 if position in (1, 4) else 1
            adapted = _expand_state_scopes(text[start:end], {state: count for state in POLICY_SOURCE_STATES[index]})
            text = text[:start] + adapted + text[end:]
    for identifier in HW_FOCUS_IDS:
        start, end = identified_block_span(text, "focus", identifier)
        text = text[:start] + _expand_strongholds(text[start:end]) + text[end:]
    return text


def _transform_decisions(text: str) -> str:
    text = _expand_state_scopes(text, {328: 20, 714: 5, 717: 5})
    for source, count in ((328, 4), (714, 1), (717, 1)):
        pattern = rf"\bstate = {source}\b"
        if len(re.findall(pattern, text)) != count:
            raise ValueError(f"unexpected map highlight coverage for {source}")
        text = re.sub(pattern, " ".join(f"state = {target}" for target in STATE_GROUPS[source]), text)
    return text


def localisation_suffix(states: tuple[int, ...]) -> str:
    return " 대상 지역: " + ", ".join(f"$STATE_{state}$" for state in states) + ". 모든 대상 지역을 소유하고 완전히 통제해야 합니다."


def _transform_localisation(text: str) -> str:
    for index, group in enumerate(POLICY_FOCUS_GROUPS):
        keys = ["HOK_KOR_mc_" + suffix + "_desc" for suffix in group]
        keys.append("HOK_KOR_mc_" + POLICY_NAMES[index] + "_project_desc")
        for key in keys:
            #20260926_kpopmodder: Preserve escaped dialogue quotes in the revised donor descriptions.
            pattern = re.compile(rf'(?m)^([ \t]*{key}:0 "(?:[^"\\\r\n]|\\[^\r\n])*)("[ \t]*\r?$)')
            matches = list(pattern.finditer(text))
            if len(matches) != 1 or "$STATE_" in matches[0][1]:
                raise ValueError(f"unexpected regional localisation source: {key}")
            text = pattern.sub(lambda match: match[1] + localisation_suffix(POLICY_TARGET_STATES[index]) + match[2], text)
    newline = "\r\n" if "\r\n" in text else "\n"
    header_end = text.index(newline) + len(newline)
    return text[:header_end] + LOCALISATION_NOTE + newline + text[header_end:]


def apply_second_wave_geography(relative: str | Path, data: bytes) -> bytes:
    """Adapt one pinned donor file after the existing ID and cross-border fixes.

    Source hash validation belongs to the caller. This function is intentionally
    not idempotent: a second pass or partial prior edit fails its source guards.
    Unselected files, including state-local dynamic modifiers, remain byte exact.
    """
    relative = Path(relative).as_posix()
    if relative not in TRANSFORM_PATHS:
        return data
    text = data.decode("utf-8")  # Keep the BOM as a codepoint.
    if relative == FOCUS_PATH:
        text = _transform_focus(text)
    elif relative == DECISION_PATH:
        text = _transform_decisions(text)
    else:
        text = _transform_localisation(text)
    return text.encode("utf-8")


def run_self_checks() -> None:
    """Exercise negative gates, scope copying, formatting and drift rejection."""
    sample = "available = { 328 = { is_owned_by = ROOT is_fully_controlled_by = ROOT } }"
    expanded = _expand_state_scopes(sample, {328: 1})
    if expanded != "available = { 328 = { is_owned_by = ROOT is_fully_controlled_by = ROOT } 941 = { is_owned_by = ROOT is_fully_controlled_by = ROOT } }":
        raise AssertionError("the complete original AND must apply to both policy successors")
    multiline = "\t328 = {\r\n\t\tadd_dynamic_modifier = { modifier = example days = 90 }\r\n\t}"
    clones = _expand_state_scopes(multiline, {328: 1})
    if clones != multiline + "\r\n" + multiline.replace("328 =", "941 =", 1):
        raise AssertionError("multiline effects or CRLF were not preserved")
    for malformed in (expanded, sample.replace("328", "714"), sample + " " + sample):
        try:
            _expand_state_scopes(malformed, {328: 1})
        except ValueError:
            pass
        else:
            raise AssertionError("partial, repeated or drifted input was accepted")
    original_gate = "OR = { " + " ".join(
        f"AND = {{ owns_state = {state} has_full_control_of_state = {state} }}"
        for state in (716, 745, 328, 717, 714, 761, 715, 610)
    ) + " }"
    expanded_gate = _expand_strongholds(original_gate)
    branches = re.findall(r"AND = \{([^{}]*)\}", expanded_gate)
    if len(branches) != 8:
        raise AssertionError("eight source alternatives must remain separate")
    qualifies = lambda owned, controlled: any(
        set(map(int, re.findall(r"\bowns_state = (\d+)", branch))) <= owned
        and set(map(int, re.findall(r"\bhas_full_control_of_state = (\d+)", branch))) <= controlled
        for branch in branches
    )
    if qualifies({941}, {941}) or qualifies({328}, {328}):
        raise AssertionError("a split fragment incorrectly unlocks a complete original stronghold")
    if not qualifies({328, 941}, {328, 941}) or not qualifies({745}, {745}):
        raise AssertionError("complete source regions must still satisfy any-one stronghold")
    if qualifies({328, 941}, {328}) or qualifies({328}, {328, 941}):
        raise AssertionError("lost control of one fragment must block its whole region")
    states = set(POLICY_TARGET_STATES[2])
    if len(states) != 8 or 9803 not in _state_provinces(ROOTS["rt56"] / "history/states/941-Andong.txt"):
        raise AssertionError("regional coverage lost the Guknaeseong center or expanded to all Manchuria")
    union_source = " ".join(f"{state} = {{ is_owned_by = ROOT is_fully_controlled_by = ROOT }}" for state in (328, 714, 717))
    union_expanded = _expand_state_scopes(union_source, {328: 1, 714: 1, 717: 1})
    required = set(map(int, re.findall(r"(\d+) = \{ is_owned_by = ROOT is_fully_controlled_by = ROOT \}", union_expanded)))
    if required != {328, 941, 714, 944, 945, 717, 942, 943}:
        raise AssertionError("M3 target conjunction has a missing or extraneous state")


def _state_provinces(path: Path) -> set[int]:
    text = re.sub(r"#[^\n]*", "", path.read_text(encoding="utf-8-sig"))
    match = re.search(r"\bprovinces\s*=\s*\{([^}]+)\}", text)
    if match is None:
        raise ValueError(f"missing province list: {path}")
    return set(map(int, re.findall(r"\d+", match[1])))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify geography evidence and bounded transformation contracts")
    parser.parse_args()
    verify_geography_inputs()
    run_self_checks()
    print("PASS: ADR-0005 geography pins and transformation contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
