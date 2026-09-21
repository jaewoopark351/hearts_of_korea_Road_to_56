#!/usr/bin/env python3
"""Rebase East-Asia shared scripts on the pinned RT56 snapshot.

The original HOK copies of these files are intentionally not used as runtime
bases.  They predate the current RT56 databases and contain Korean state IDs
that RT56 now assigns to unrelated parts of the world.  This builder starts
from current RT56 (or current vanilla where RT56 has no file), then applies
only the reviewed HOK behaviour and the generated Korea state layout.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from build_rt56_map import HOK_ROOT, REPO_ROOT, RT56_ROOT, VANILLA_ROOT


EXPECTED_SHA256 = {
    # [2026-09-22]_kpopmodder: Preserve reviewed RT56 border-war flag updates; retain Korean merge.
    RT56_ROOT / "events/WTT_Japan.txt": "E843DB20E3166F74D8303798ADB1CF5D3DE31475CC1C941051592F90362919C5",
    RT56_ROOT / "events/SEA_Japan.txt": "AC5BEB9F0A9BAEED124F0FE97050497A7B58EE6A59852932F84DBB40D67246F5",
    RT56_ROOT / "events/ElectionEvents.txt": "50E876EA21720E006E9D70BD6BA308E96151EAA35C0194A4CF9ADA293181AD26",
    RT56_ROOT / "events/r56_japan.txt": "ACC5132D1D920575D2090931E0FB446E87C4F5FED911EE33659606221BA1F1A3",
    RT56_ROOT / "events/WTT_PRC.txt": "3946061312480D42FC0AA8E3A37E75CF24D688BA23755C2A9C343B9661FD4C86",
    RT56_ROOT / "common/decisions/JAP.txt": "1FADB70D82C806EFE8A3112B81FDE3665E52B96160376AD7D74784BAC2A9B5F3",
    RT56_ROOT / "common/national_focus/china_shared_TSR.txt": "AFC2636E2D7702DD4A4888B6ED8A133E990AEB3DB1C5DF1C77759AE49EA87B78",
    RT56_ROOT / "common/on_actions/14_sea_on_actions.txt": "29B155F61A0D20279115D37470650FC2C323C20058F461D11ABDF91186B049D1",
    RT56_ROOT / "history/countries/JAP - Japan.txt": "799186C2BC9B9CD45340AEBD6038DC7B29DAFD89DB5B4E3E77BC9AF62F62E405",
    VANILLA_ROOT / "common/scripted_triggers/JAP_scripted_triggers.txt": "A22EDEA8C581F460E898EF01601F98CAA2ECEC0398BDE662C596DFA618FAD25E",
    VANILLA_ROOT / "history/units/JAP_1936.txt": "6A205B9574F61980DB43F8B630202AA8117C24332CC48FD6B8E71EF85AD0F566",
    VANILLA_ROOT / "history/units/JAP_1936_nsb.txt": "73178BF3E2A4DFFE8622BE3F07AC153155688BFBC3F34603EA352DD5130C8127",
    VANILLA_ROOT / "history/units/JAP_1936_naval_legacy.txt": "472AE515312D469388B718801594A461E0F7F87E949C2CA0171261B20C08F42B",
    VANILLA_ROOT / "common/peace_conference/ai_peace/SOV.txt": "2D48354458C9A0FDA9C3CE6E4A1349C973696F339DEABFDACCE47EC7197DD2A6",
    VANILLA_ROOT / "common/peace_conference/ai_peace/USA.txt": "3C1FDFD4610162AE6AB133EB576CEB2A73B23DA538A4905EBCF99D47B27D3FB5",
    HOK_ROOT / "events/WTT_Japan.txt": "654092BF27DF32226C54EF425617196467B93FF4D8E861B637A92D0C92C5A013",
    HOK_ROOT / "events/SEA_Japan.txt": "6EB21D08B03729FDEA1D00944EF4F9FCA8574FC0EE801DD631257EC2F8A31320",
    HOK_ROOT / "events/ElectionEvents.txt": "4D51DFF85831EA917B6A1FECD94F41D7A3CCF1177FC2CF823BF0892142E6F4E3",
    HOK_ROOT / "common/decisions/JAP.txt": "5D1765671AC227C5CB4B32F188F744BD69F3384E55F6EA8F6145253B4BFA856E",
    HOK_ROOT / "common/national_focus/china_shared_TSR.txt": "CA376A6498F46748B785FBD425C31B96E99E1EE9C6F70E11C197D58A9A3CA0BA",
    HOK_ROOT / "common/scripted_triggers/JAP_scripted_triggers.txt": "49FE6E728583B47E706100669339CA47203A3FA0542E4BFA835F8C0413226EA2",
    HOK_ROOT / "common/on_actions/14_sea_on_actions.txt": "418F7F23543A227F010F029383BFF4CDBE822F7D404EB80EAD07098E7386F903",
    HOK_ROOT / "history/countries/JAP - Japan.txt": "13D7038F109ECA94B75B0BA02FD35FFFBE37EFBD709AC59460D48BA25D5B0BD5",
    HOK_ROOT / "history/units/JAP_1936.txt": "A1F21C5BF0BB800431E86C585A187483AA048BD3700BBA1E9D2F1BAEBAD5AFBF",
    HOK_ROOT / "history/units/JAP_1936_nsb.txt": "26AD4DE240387F45C4F35C22108DDB5615E73A40AEA83AC3C129DBAE13E014AE",
    HOK_ROOT / "history/units/JAP_1936_naval_legacy.txt": "41736D03C38690A38B391895E871D5BC791D809654677ADEA8B8ECD2991FDAFB",
    HOK_ROOT / "common/peace_conference/ai_peace/SOV.txt": "B99150C98F1F0A3AB8196320A0D1C447FB66A3206F8585A16BC55C773DC98143",
    HOK_ROOT / "common/peace_conference/ai_peace/USA.txt": "9B554F2D48F5D5CE02A95F1044A9579F1BB3D65C42087DD6CC7086E1147B0EF2",
}

OLD_HOK_STATE_IDS = {1028, 1029, 1030, 1031, 1082, 1083, 1084, 1085}
SOUTH_KOREA = (525, 919, 920, 1144, 1145, 1146)
NORTH_KOREA = (527, 917, 918)
ALL_KOREA = SOUTH_KOREA + NORTH_KOREA


class BuildError(RuntimeError):
    pass


@dataclass(frozen=True)
class TextFormat:
    newline: str
    bom: bool
    final_newline: bool


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def verify_inputs() -> None:
    failures: list[str] = []
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            failures.append(f"missing: {path}")
            continue
        actual = sha256(path.read_bytes())
        if actual != expected:
            failures.append(f"changed: {path}\n  expected {expected}\n  actual   {actual}")
    if failures:
        raise BuildError("Pinned source verification failed:\n" + "\n".join(failures))


def read_text(path: Path) -> tuple[str, TextFormat]:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    body = raw[3:] if bom else raw
    text = body.decode("utf-8")
    crlf = text.count("\r\n")
    bare_lf = len(re.findall(r"(?<!\r)\n", text))
    if crlf and bare_lf:
        raise BuildError(f"mixed line endings in pinned source: {path}")
    newline = "\r\n" if crlf else "\n"
    final_newline = text.endswith(("\n", "\r"))
    return text.replace("\r\n", "\n"), TextFormat(newline, bom, final_newline)


def encode_text(text: str, fmt: TextFormat) -> bytes:
    normalized = text.replace("\r\n", "\n")
    if fmt.final_newline and not normalized.endswith("\n"):
        normalized += "\n"
    if not fmt.final_newline:
        normalized = normalized.rstrip("\n")
    body = normalized.replace("\n", fmt.newline).encode("utf-8")
    return (b"\xef\xbb\xbf" if fmt.bom else b"") + body


def match_closing_brace(text: str, opening: int) -> int:
    depth = 0
    in_quote = False
    escaped = False
    in_comment = False
    for index in range(opening, len(text)):
        char = text[index]
        if in_comment:
            if char == "\n":
                in_comment = False
            continue
        if in_quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = False
            continue
        if char == "#":
            in_comment = True
        elif char == '"':
            in_quote = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index + 1
            if depth < 0:
                break
    raise BuildError(f"unclosed block starting at offset {opening}")


def assignment_blocks(text: str, key: str) -> list[tuple[int, int]]:
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*\{{")
    result: list[tuple[int, int]] = []
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        result.append((match.start(), match_closing_brace(text, opening)))
    return result


def identified_block(text: str, kind: str, identifier: str) -> tuple[int, int]:
    matches: list[tuple[int, int]] = []
    id_pattern = re.compile(
        rf"(?m)^[ \t]*id[ \t]*=[ \t]*{re.escape(identifier)}[ \t]*(?:#.*)?$"
    )
    for start, end in assignment_blocks(text, kind):
        if id_pattern.search(text[start:end]):
            matches.append((start, end))
    if len(matches) != 1:
        raise BuildError(f"expected one {kind} id={identifier}, found {len(matches)}")
    return matches[0]


def named_block(text: str, key: str) -> tuple[int, int]:
    matches = assignment_blocks(text, key)
    if len(matches) != 1:
        raise BuildError(f"expected one block {key}, found {len(matches)}")
    return matches[0]


def replace_named_block(text: str, key: str, replacement: str) -> str:
    start, end = named_block(text, key)
    return text[:start] + replacement + text[end:]


def replace_exact(text: str, old: str, new: str, expected: int, label: str) -> str:
    count = text.count(old)
    if count != expected:
        raise BuildError(f"{label}: expected {expected} matches, found {count}")
    return text.replace(old, new)


def replace_numeric_token(text: str, old: int, new: int) -> str:
    return re.sub(rf"(?<![0-9]){old}(?![0-9])", str(new), text)


def expand_command_sequence(
    text: str,
    command: str,
    existing: tuple[int, ...],
    additions: tuple[int, ...],
    expected: int,
    label: str,
) -> str:
    parts = [
        rf"(?P<indent>^[ \t]*){re.escape(command)}[ \t]*=[ \t]*{existing[0]}[ \t]*$"
    ]
    parts.extend(
        rf"(?P=indent){re.escape(command)}[ \t]*=[ \t]*{state_id}[ \t]*$"
        for state_id in existing[1:]
    )
    pattern = re.compile("\n".join(parts), re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) != expected:
        raise BuildError(f"{label}: expected {expected} sequences, found {len(matches)}")

    def expand(match: re.Match[str]) -> str:
        indent = match.group("indent")
        suffix = "".join(f"\n{indent}{command} = {state_id}" for state_id in additions)
        return match.group(0) + suffix

    return pattern.sub(expand, text)


def clone_filtered_blocks(
    text: str,
    key: str,
    predicate,
    new_ids: tuple[int, ...],
    expected: int,
    label: str,
) -> str:
    matches = [item for item in assignment_blocks(text, key) if predicate(text[item[0] : item[1]])]
    if len(matches) != expected:
        raise BuildError(f"{label}: expected {expected} blocks, found {len(matches)}")
    for start, end in reversed(matches):
        block = text[start:end]
        clones = "\n".join(replace_numeric_token(block, int(key), value) for value in new_ids)
        text = text[:end] + "\n" + clones + text[end:]
    return text


def replace_state_assignments(
    text: str,
    mapping: dict[int, tuple[int, ...]],
    expected_each: int,
    label: str,
) -> str:
    replacements: list[tuple[int, int, str]] = []
    for old, new_ids in mapping.items():
        blocks = assignment_blocks(text, str(old))
        if len(blocks) != expected_each:
            raise BuildError(
                f"{label}: state {old} expected {expected_each} assignment blocks, found {len(blocks)}"
            )
        for start, end in blocks:
            block = text[start:end]
            replacement = "\n".join(replace_numeric_token(block, old, new) for new in new_ids)
            replacements.append((start, end, replacement))
    for start, end, replacement in sorted(replacements, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def replace_inner_block(outer: str, key: str, transform) -> str:
    start, end = named_block(outer, key)
    return outer[:start] + transform(outer[start:end]) + outer[end:]


def validate_braces(text: str, label: str) -> None:
    depth = 0
    in_quote = False
    escaped = False
    in_comment = False
    for char in text:
        if in_comment:
            if char == "\n":
                in_comment = False
            continue
        if in_quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = False
            continue
        if char == "#":
            in_comment = True
        elif char == '"':
            in_quote = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                raise BuildError(f"{label}: closing brace without opener")
    if depth or in_quote:
        raise BuildError(f"{label}: unbalanced braces/quotes (depth={depth}, quote={in_quote})")


def build_jap_scripted_triggers() -> tuple[str, TextFormat]:
    text, fmt = read_text(VANILLA_ROOT / "common/scripted_triggers/JAP_scripted_triggers.txt")
    home_start, home_end = named_block(text, "JAP_is_home_islands_state")
    home = text[home_start:home_end]
    home = replace_exact(
        home,
        "\t\t\tstate = 526 # Okinawa",
        "\t\t\tstate = 526 # Okinawa\n\t\t\tstate = 1147 # HOK-RT56: Tsushima split from state 528",
        1,
        "JAP home-islands Tsushima hook",
    )
    text = text[:home_start] + home + text[home_end:]
    korean = """is_korean_state = {
\tOR = {
""" + "".join(f"\t\tstate = {state_id}\n" for state_id in ALL_KOREA) + "\t}\n}"
    south = """is_south_korean_state = {
\tOR = {
""" + "".join(f"\t\tstate = {state_id}\n" for state_id in SOUTH_KOREA) + "\t}\n}"
    north = """is_north_korean_state = {
\tOR = {
""" + "".join(f"\t\tstate = {state_id}\n" for state_id in NORTH_KOREA) + "\t}\n}"
    text = replace_named_block(text, "is_korean_state", korean)
    text = replace_named_block(text, "is_south_korean_state", south)
    text = replace_named_block(text, "is_north_korean_state", north)
    return text, fmt


def build_wtt_japan() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "events/WTT_Japan.txt")
    text = replace_exact(
        text,
        "\t\t\t\t\t\tcontrols_state = 921",
        "\t\t\t\t\t\tcontrols_state = 920",
        1,
        "RT56 WTT Japan Gyeongsang typo",
    )
    text = expand_command_sequence(text, "controls_state", (525, 527, 917, 918, 919, 920), (1144, 1145, 1146), 4, "WTT Japan control sets")
    text = expand_command_sequence(text, "transfer_state", (525, 527, 917, 918, 919, 920), (1144, 1145, 1146), 5, "WTT Japan transfer sets")
    text = expand_command_sequence(text, "state", (525, 527, 917, 918, 919, 920), (1144, 1145, 1146), 1, "WTT Japan exclusion set")
    text = expand_command_sequence(
        text,
        "transfer_state",
        (528,),
        (1147,),
        2,
        "WTT Japan Japanese-mainland Tsushima transfers",
    )
    return text, fmt


def build_sea_japan() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "events/SEA_Japan.txt")
    pattern = re.compile(r"(?m)^(?P<indent>[ \t]*)state[ \t]*=[ \t]*917[^\n]*$")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise BuildError(
            f"SEA Japan Korean civil-war south filter: expected state 917 once, found {len(matches)}"
        )
    text = pattern.sub(
        lambda match: match.group(0)
        + "".join(
            f"\n{match.group('indent')}state = {state_id} # HOK-RT56 Korean split"
            for state_id in (1144, 1145, 1146)
        ),
        text,
    )
    return text, fmt


def build_election_events() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "events/ElectionEvents.txt")
    event_ids = tuple(range(2, 9)) + tuple(range(11, 18))
    exclusion = (
        "\n\t\t# HOK owns Korea's post-focus election flow.\n"
        "\t\tNOT = {\n"
        "\t\t\tAND = {\n"
        "\t\t\t\ttag = KOR\n"
        "\t\t\t\thas_completed_focus = KOR_democracy_advance_forward\n"
        "\t\t\t}\n"
        "\t\t}"
    )
    for event_id in event_ids:
        start, end = identified_block(text, "country_event", f"election.{event_id}")
        event = text[start:end]
        triggers = [
            item
            for item in assignment_blocks(event, "trigger")
            if event[item[0] : item[1]].startswith("\ttrigger")
        ]
        if len(triggers) != 1:
            raise BuildError(
                f"election.{event_id}: expected one event-level trigger, found {len(triggers)}"
            )
        trigger_start, trigger_end = triggers[0]
        trigger = event[trigger_start:trigger_end]
        if "KOR_democracy_advance_forward" in trigger:
            raise BuildError(f"election.{event_id} already contains HOK exclusion")
        opening = trigger.find("{")
        trigger = trigger[: opening + 1] + exclusion + trigger[opening + 1 :]
        event = event[:trigger_start] + trigger + event[trigger_end:]
        text = text[:start] + event + text[end:]
    if text.count("KOR_democracy_advance_forward") != len(event_ids):
        raise BuildError("election exclusion count mismatch")
    return text, fmt


def build_jap_decisions() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "common/decisions/JAP.txt")
    text = replace_state_assignments(
        text,
        {1029: (1144,), 1030: (920,), 1031: (1145, 919, 1146)},
        3,
        "JAP Korean surrender state lists",
    )
    text = clone_filtered_blocks(
        text,
        "918",
        lambda block: "is_controlled_by_ROOT_or_ally = no" in block,
        (917,),
        3,
        "JAP Korean surrender Hwanghae states",
    )
    old = "\t\t\thas_full_control_of_state = 525\n\t\t\thas_full_control_of_state = 527"
    new = "\n".join(f"\t\t\thas_full_control_of_state = {state_id}" for state_id in ALL_KOREA)
    text = replace_exact(text, old, new, 1, "JAP release-Korea full-control requirement")
    return text, fmt


def build_hok_jap_decisions() -> tuple[str, TextFormat]:
    donor, _ = read_text(HOK_ROOT / "common/decisions/JAP.txt")
    start, end = named_block(donor, "JAP_war_on_korea_category")
    block = donor[start:end]
    text = (
        "# HOK-only Japan warning/ultimatum chain, extracted from the historical donor.\n"
        "# The shared JAP decision database is rebased separately from current RT56.\n\n"
        + block
        + "\n"
    )
    return text, TextFormat("\r\n", False, True)


def transform_china_state_block(block: str) -> str:
    return replace_state_assignments(
        block,
        {
            527: (527, 917),
            1028: (918,),
            1029: (1144,),
            1030: (920,),
            1031: (1145, 919, 1146),
        },
        1,
        "China shared Korean state scopes",
    )


def transform_china_controls(block: str) -> str:
    mapping = {
        527: (527, 917),
        1028: (918,),
        1029: (1144,),
        1030: (920,),
        1031: (1145, 919, 1146),
    }
    for old, new_ids in mapping.items():
        pattern = re.compile(rf"(?m)^(?P<indent>[ \t]*)controls_state[ \t]*=[ \t]*{old}[ \t]*$")
        matches = list(pattern.finditer(block))
        if len(matches) != 1:
            raise BuildError(f"China secure bypass state {old}: expected once, found {len(matches)}")
        block = pattern.sub(
            lambda match: "\n".join(
                f"{match.group('indent')}controls_state = {state_id}" for state_id in new_ids
            ),
            block,
        )
    return block


def build_china_shared() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "common/national_focus/china_shared_TSR.txt")
    start, end = identified_block(text, "shared_focus", "CHI_sea_commit_to_korean_independence")
    focus = text[start:end]
    focus = replace_inner_block(focus, "bypass", transform_china_state_block)
    text = text[:start] + focus + text[end:]

    start, end = identified_block(text, "shared_focus", "CHI_sea_secure_the_peninsula")
    focus = text[start:end]
    focus = replace_inner_block(focus, "available", transform_china_state_block)
    focus = replace_inner_block(focus, "bypass", transform_china_controls)
    text = text[:start] + focus + text[end:]
    return text, fmt


def build_on_actions() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "common/on_actions/14_sea_on_actions.txt")
    text = expand_command_sequence(
        text,
        "state",
        (918, 917, 919, 920, 527),
        (1144, 1145, 1146),
        1,
        "SEA resistance state initialization",
    )
    return text, fmt


def build_wtt_prc() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "events/WTT_PRC.txt")
    text = expand_command_sequence(
        text,
        "controls_state",
        (525, 527, 917, 918, 919, 920),
        (1144, 1145, 1146),
        2,
        "WTT PRC Korea control lists",
    )
    text = replace_exact(
        text,
        "prioritize = { 525 527 917 918 919 920 }",
        "prioritize = { 525 527 917 918 919 920 1144 1145 1146 }",
        3,
        "WTT PRC Korea priority lists",
    )
    candidates = [
        item
        for item in assignment_blocks(text, "if")
        if "controls_state = 920" in text[item[0] : item[1]]
        and "KOR = { transfer_state = 920 }" in text[item[0] : item[1]]
    ]
    if len(candidates) != 1:
        raise BuildError(f"WTT PRC state-transfer block expected once, found {len(candidates)}")
    start, end = candidates[0]
    block = text[start:end]
    clones = "\n".join(replace_numeric_token(block, 920, state_id) for state_id in (1144, 1145, 1146))
    text = text[:end] + "\n" + clones + text[end:]
    return text, fmt


def build_r56_japan() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "events/r56_japan.txt")
    text = clone_filtered_blocks(
        text,
        "920",
        lambda block: "tag = JAP" in block and "is_puppet_of = JAP" in block,
        (1144, 1145, 1146),
        1,
        "r56 Japan loss-state trigger scopes",
    )
    pair = (
        "\t\t\t920 = { is_controlled_by = JAP }\n"
        "\t\t\t920 = { controller = { is_puppet_of = JAP } } "
    )
    extra_pairs = "\n".join(
        f"\t\t\t{state_id} = {{ is_controlled_by = JAP }}\n"
        f"\t\t\t{state_id} = {{ controller = {{ is_puppet_of = JAP }} }} "
        for state_id in (1144, 1145, 1146)
    )
    text = replace_exact(text, pair, pair + "\n" + extra_pairs, 1, "r56 Japan loss-state trigger pairs")

    candidates = [
        item
        for item in assignment_blocks(text, "if")
        if text[item[0] : item[1]].count("920 = {") == 2
        and "sfl_kor_fired" in text[item[0] : item[1]]
    ]
    if len(candidates) != 1:
        raise BuildError(f"r56 Japan controller-dispatch block expected once, found {len(candidates)}")
    start, end = candidates[0]
    block = text[start:end]
    clones = "\n".join(replace_numeric_token(block, 920, state_id) for state_id in (1144, 1145, 1146))
    text = text[:end] + "\n" + clones + text[end:]

    text = clone_filtered_blocks(
        text,
        "920",
        lambda block: "is_controlled_by = ROOT" in block and "is_owned_by = ROOT" not in block,
        (1144, 1145, 1146),
        2,
        "r56 Japan controlled south-state scopes",
    )
    text = clone_filtered_blocks(
        text,
        "920",
        lambda block: "is_owned_by = ROOT" in block and "is_controlled_by = ROOT" not in block,
        (1144, 1145, 1146),
        1,
        "r56 Japan owned south-state scopes",
    )
    text = clone_filtered_blocks(
        text,
        "920",
        lambda block: "is_owned_by = ROOT" in block and "is_controlled_by = ROOT" in block,
        (1144, 1145, 1146),
        1,
        "r56 Japan owned-and-controlled south-state scopes",
    )
    text = expand_command_sequence(
        text,
        "transfer_state",
        (525, 919, 920),
        (1144, 1145, 1146),
        3,
        "r56 Japan south-state transfers",
    )
    text = expand_command_sequence(
        text,
        "set_state_controller",
        (525, 920, 919),
        (1144, 1145, 1146),
        1,
        "r56 Japan occupation-zone controllers",
    )
    return text, fmt


def build_jap_history() -> tuple[str, TextFormat]:
    text, fmt = read_text(RT56_ROOT / "history/countries/JAP - Japan.txt")
    source_ids = (527, 917, 918, 919, 920, 525)
    found: list[tuple[int, int, str]] = []
    for state_id in source_ids:
        candidates = [
            (start, end, text[start:end])
            for start, end in assignment_blocks(text, str(state_id))
            if "start_resistance = yes" in text[start:end]
            and "set_compliance = 15" in text[start:end]
            and "set_resistance = 1" in text[start:end]
        ]
        if len(candidates) != 1:
            raise BuildError(f"JAP history state {state_id} resistance block expected once, found {len(candidates)}")
        found.append(candidates[0])
    ordered = sorted(found)
    start = ordered[0][0]
    end = ordered[-1][1]
    between = text[start:end]
    for state_id in source_ids:
        if between.count(f"{state_id} = {{") != 1:
            raise BuildError("JAP history Korean resistance blocks are no longer contiguous")
    template = found[0][2]
    template_body_start = template.find("{") + 1
    template_body_end = template.rfind("}")
    body = template[template_body_start:template_body_end]
    body = re.sub(r"^\n", "", body)
    body = re.sub(r"\n$", "", body)
    body_lines = body.split("\n")
    date_lines = [
        "# HOK starts independent in 1936; initialize RT56-equivalent resistance on annexation.",
        "1939.3.14 = {",
    ]
    for state_id in ALL_KOREA:
        date_lines.append(f"\t{state_id} = {{")
        date_lines.extend("\t" + line for line in body_lines)
        date_lines.append("\t}")
    date_lines.append("}")
    text = text[:start] + "\n".join(date_lines) + text[end:]
    return text, fmt


def build_jap_land_oob(filename: str) -> tuple[str, TextFormat]:
    text, fmt = read_text(VANILLA_ROOT / "history/units" / filename)
    replacements = (
        (
            "\t\tlocation = 4052 #Pyongyang",
            "\t\tlocation = 7169 #Sendai; HoK keeps Korea independent in 1936",
        ),
        (
            "\t\tlocation = 7125 #Seoul",
            "\t\tlocation = 12031 #Kobe; HoK keeps Korea independent in 1936",
        ),
        (
            "\t\tlocation = 4056 #Pusan",
            "\t\tlocation = 10011 #Tsushima; HoK keeps Korea independent in 1936",
        ),
    )
    for old, new in replacements:
        text = replace_exact(text, old, new, 1, f"{filename} independent-Korea OOB")
    return text, fmt


def build_jap_1936_oob() -> tuple[str, TextFormat]:
    return build_jap_land_oob("JAP_1936.txt")


def build_jap_1936_nsb_oob() -> tuple[str, TextFormat]:
    return build_jap_land_oob("JAP_1936_nsb.txt")


def build_jap_1936_naval_legacy_oob() -> tuple[str, TextFormat]:
    text, fmt = read_text(
        VANILLA_ROOT / "history/units/JAP_1936_naval_legacy.txt"
    )
    text = replace_exact(
        text,
        "\t\t\tlocation = 4056  # Pusan",
        "\t\t\tlocation = 10011  # Tsushima; HoK keeps Korea independent in 1936",
        1,
        "JAP_1936_naval_legacy independent-Korea OOB",
    )
    return text, fmt


def build_sov_peace_ai() -> tuple[str, TextFormat]:
    text, fmt = read_text(
        VANILLA_ROOT / "common/peace_conference/ai_peace/SOV.txt"
    )
    text = replace_exact(
        text,
        "                state = 527\n                state = 1028",
        "                state = 527\n"
        "                state = 918\n"
        "\t\t\t\tstate = 917 # HoK: Hwanghae",
        1,
        "SOV northern Korea peace AI",
    )
    text = replace_exact(
        text,
        "                state = 525\n"
        "                state = 1029\n"
        "                state = 1031\n"
        "                state = 1030",
        "                state = 525\n"
        "                state = 1144\n"
        "                state = 1145\n"
        "                state = 920\n"
        "\t\t\t\tstate = 919 # HoK: Jeolla\n"
        "\t\t\t\tstate = 1146 # HoK: Jeju",
        1,
        "SOV southern Korea peace AI",
    )
    return text, fmt


def build_usa_peace_ai() -> tuple[str, TextFormat]:
    text, fmt = read_text(
        VANILLA_ROOT / "common/peace_conference/ai_peace/USA.txt"
    )
    text = replace_exact(
        text,
        "                    state = 525\n"
        "                    state = 1029\n"
        "                    state = 1031\n"
        "                    state = 1030",
        "                    state = 525\n"
        "                    state = 1144\n"
        "                    state = 1145\n"
        "                    state = 920\n"
        "\t\t\t\t\tstate = 919 # HoK: Jeolla\n"
        "\t\t\t\t\tstate = 1146 # HoK: Jeju",
        2,
        "USA southern Korea peace AI",
    )
    text = replace_exact(
        text,
        "                    state = 527\n                    state = 1028",
        "                    state = 527\n"
        "                    state = 918\n"
        "\t\t\t\t\tstate = 917 # HoK: Hwanghae",
        1,
        "USA northern Korea peace AI",
    )
    return text, fmt


def build_all() -> dict[str, bytes]:
    builders = {
        "common/scripted_triggers/JAP_scripted_triggers.txt": build_jap_scripted_triggers,
        "events/WTT_Japan.txt": build_wtt_japan,
        "events/SEA_Japan.txt": build_sea_japan,
        "events/ElectionEvents.txt": build_election_events,
        "common/decisions/JAP.txt": build_jap_decisions,
        "common/decisions/HOK_RT56_JAP.txt": build_hok_jap_decisions,
        "common/national_focus/china_shared_TSR.txt": build_china_shared,
        "common/on_actions/14_sea_on_actions.txt": build_on_actions,
        "events/WTT_PRC.txt": build_wtt_prc,
        "events/r56_japan.txt": build_r56_japan,
        "history/countries/JAP - Japan.txt": build_jap_history,
        "history/units/JAP_1936.txt": build_jap_1936_oob,
        "history/units/JAP_1936_nsb.txt": build_jap_1936_nsb_oob,
        "history/units/JAP_1936_naval_legacy.txt": build_jap_1936_naval_legacy_oob,
        "common/peace_conference/ai_peace/SOV.txt": build_sov_peace_ai,
        "common/peace_conference/ai_peace/USA.txt": build_usa_peace_ai,
    }
    outputs: dict[str, bytes] = {}
    old_state_alternatives = "|".join(map(str, sorted(OLD_HOK_STATE_IDS)))
    old_pattern = re.compile(rf"(?<![0-9])(?:{old_state_alternatives})(?![0-9])")
    for relative, builder in builders.items():
        text, fmt = builder()
        validate_braces(text, relative)
        match = old_pattern.search(re.sub(r"#.*", "", text))
        if match:
            raise BuildError(f"{relative}: stale HOK state ID remains: {match.group(0)}")
        outputs[relative] = encode_text(text, fmt)
    return outputs


def write_if_changed(relative: str, data: bytes, apply: bool) -> str:
    path = (REPO_ROOT / Path(relative)).resolve()
    try:
        path.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise BuildError(f"output escapes repository: {path}") from exc
    current = path.read_bytes() if path.is_file() else None
    status = "unchanged" if current == data else "would-write"
    if apply and current != data:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".hok-east-asia.tmp")
        temporary.write_bytes(data)
        temporary.replace(path)
        status = "written"
    return f"{status:11} {relative} {sha256(data)}"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        verify_inputs()
        outputs = build_all()
        messages = [write_if_changed(path, data, args.apply) for path, data in sorted(outputs.items())]
        if args.check and any(message.startswith("would-write") for message in messages):
            print("Generated-output mismatches:", file=sys.stderr)
            print("\n".join(message for message in messages if message.startswith("would-write")), file=sys.stderr)
            return 1
        print("\n".join(messages))
        print(f"east-asia-overrides {len(outputs)}; korea-states {len(ALL_KOREA)}; tsushima-state 1147")
        return 0
    except BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
