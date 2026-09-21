#!/usr/bin/env python3
"""Rewrite HOK-owned script/localisation references to the RT56 map IDs.

This is deliberately separate from shared-file rebasing.  Files owned by RT56
or vanilla are excluded here and must be rebuilt from their current host copy,
with only the reviewed HOK delta applied.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from source_snapshot import FOCUS_UPDATE_PATHS

from build_rt56_map import (
    HOK_ROOT,
    PROVINCE_ID_MAP,
    REPO_ROOT,
    STATE_ID_MAP,
)


TEXT_ROOTS = ("common", "events", "history", "localisation")
TEXT_SUFFIXES = {".txt", ".yml", ".gui", ".gfx", ".asset", ".csv"}

HOK_MANCHURIA_STATE_IDS = (716, 745, 328, 717, 714, 761, 715, 610)
RT56_MANCHURIA_SPLIT_STATE_IDS = tuple(range(941, 948))
MANCHURIA_STATE_IDS = (
    *HOK_MANCHURIA_STATE_IDS,
    *RT56_MANCHURIA_SPLIT_STATE_IDS,
)

# These are rebased from RT56 in a separate integration step.  Migrating the
# donor whole-file copy would reintroduce the exact stale overrides this port
# is designed to remove.
SHARED_MERGE_PATHS = {
    "common/decisions/KOR.txt",
    "common/decisions/JAP.txt",
    "common/national_focus/china_shared_TSR.txt",
    "common/on_actions/14_sea_on_actions.txt",
    "common/peace_conference/ai_peace/SOV.txt",
    "common/peace_conference/ai_peace/USA.txt",
    "common/scripted_triggers/JAP_scripted_triggers.txt",
    "events/SEA_Japan.txt",
    "events/WTT_Japan.txt",
    "history/countries/JAP - Japan.txt",
}

def replace_tokens(data: bytes, mapping: dict[int, int]) -> bytes:
    result = data
    for old, new in sorted(mapping.items(), reverse=True):
        result = re.sub(
            rb"(?<![0-9])" + str(old).encode() + rb"(?![0-9])",
            str(new).encode(),
            result,
        )
    return result


def apply_post_migration_fixes(relative: str, data: bytes) -> bytes:
    """Apply reviewed identity/reference fixes after numeric ID migration."""
    if relative == "events/korea.txt":
        data = re.sub(
            rb"(?m)^(\xef\xbb\xbf)?([ \t]*add_namespace[ \t]*=[ \t]*)KOR_events([ \t]*\r?$)",
            rb"\1\2kor_events\3",
            data,
        )
        data = re.sub(
            rb"(\bid[ \t]*=[ \t]*)KOR_events\.(?=[0-9])",
            rb"\1kor_events.",
            data,
        )
        data = repair_korea_events(data)
    elif relative == "common/decisions/KOR_decision.txt":
        data = re.sub(
            rb"(\bcountry_event[ \t]*=[ \t]*)KOR_events\.(?=[0-9])",
            rb"\1kor_events.",
            data,
        )
    elif relative == "common/achievements/HoK_achievements.txt":
        data = data.replace(
            b"HoK_achievements_2898629778", b"hok_rt56_achievements"
        )
    elif relative in {
        "localisation/english/HoK_achievements_l_english.yml",
        "localisation/korean/HoK_achievements_l_korean.yml",
    }:
        data = data.replace(
            b"HoK_achievements_2898629778", b"hok_rt56_achievements"
        )
    elif relative in {
        "localisation/english/replace/HoK_countries_l_english.yml",
        "localisation/korean/replace/HoK_countries_l_korean.yml",
    }:
        data = repair_country_localisation(relative, data)
    if relative in {
        "common/decisions/KOR_decision.txt",
        "common/national_focus/korea.txt",
        "common/on_actions/gookppong_on_actions.txt",
        "events/korea.txt",
    }:
        data = repair_manchuria_state_coverage(relative, data)
    return data


def add_phi_free_localisation(relative: str, data: bytes) -> bytes:
    """Complete the reachable Philippine liberation cosmetic tag."""
    phi_keys = (
        b"PHI_free_democratic:",
        b"PHI_free_democratic_DEF:",
        b"PHI_free_democratic_ADJ:",
    )
    present = tuple(key in data for key in phi_keys)
    if all(present):
        return data
    if any(present):
        raise ValueError(f"partial pre-existing PHI_free localisation in {relative}")
    marker = b' NZL_aotearoa_democratic:0 "'
    marker_start = data.find(marker)
    if marker_start < 0:
        raise ValueError(f"missing Asia-liberation localisation marker in {relative}")
    line_feed = data.find(b"\n", marker_start)
    if line_feed < 0:
        raise ValueError(f"unterminated localisation marker in {relative}")
    line_end = line_feed + 1
    newline = b"\r\n" if data[line_feed - 1:line_end] == b"\r\n" else b"\n"
    if relative.endswith("_english.yml"):
        lines = (
            ' PHI_free_democratic:0 "Free Republic of the Philippines"',
            ' PHI_free_democratic_DEF:0 "the Free Republic of the Philippines"',
            ' PHI_free_democratic_ADJ:0 "Philippine"',
        )
    else:
        lines = (
            ' PHI_free_democratic:0 "필리핀 자유 공화국"',
            ' PHI_free_democratic_DEF:0 "필리핀 자유 공화국"',
            ' PHI_free_democratic_ADJ:0 "필리핀"',
        )
    addition = newline.join(line.encode("utf-8") for line in lines) + newline
    return data[:line_end] + addition + data[line_end:]


def repair_country_localisation(relative: str, data: bytes) -> bytes:
    data = add_phi_free_localisation(relative, data)
    mon_keys = {
        b"MON_fascism",
        b"MON_fascism_DEF",
        b"MON_democratic",
        b"MON_democratic_DEF",
        b"MON_neutrality",
        b"MON_neutrality_DEF",
        b"MON_communism",
        b"MON_communism_DEF",
    }
    pattern = re.compile(rb"^[ \t]*([A-Za-z0-9_]+):[0-9]+")
    removed: set[bytes] = set()
    kept: list[bytes] = []
    for line in data.splitlines(keepends=True):
        match = pattern.match(line)
        if match and match.group(1) in mon_keys:
            removed.add(match.group(1))
            continue
        if line.strip() == b"#MON countrie name":
            continue
        kept.append(line)
    if removed and removed != mon_keys:
        missing = sorted(key.decode() for key in mon_keys - removed)
        raise ValueError(f"partial MON localisation block in {relative}: missing {missing}")
    result = b"".join(kept)
    if any(key + b":" in result for key in mon_keys):
        raise ValueError(f"MON localisation override remains in {relative}")
    jap_keys = {
        b"JAP_yamato_kyowakoku",
        b"JAP_yamato_kyowakoku_DEF",
        b"JAP_yamato_kyowakoku_ADJ",
        b"JAP_daiwa_mingoku",
        b"JAP_daiwa_mingoku_DEF",
        b"JAP_daiwa_mingoku_ADJ",
        b"JAP_fuso_gasshukoku",
        b"JAP_fuso_gasshukoku_DEF",
        b"JAP_fuso_gasshukoku_ADJ",
    }
    removed_jap: set[bytes] = set()
    kept = []
    for line in result.splitlines(keepends=True):
        match = pattern.match(line)
        if match and match.group(1) in jap_keys:
            removed_jap.add(match.group(1))
            continue
        if line.strip() == b"#JAP Republican Japan":
            continue
        kept.append(line)
    if removed_jap and removed_jap != jap_keys:
        missing = sorted(key.decode() for key in jap_keys - removed_jap)
        raise ValueError(f"partial orphan JAP localisation block in {relative}: missing {missing}")
    result = b"".join(kept)
    if any(key + b":" in result for key in jap_keys):
        raise ValueError(f"orphan JAP localisation remains in {relative}")
    raj_key = b"RAJ_bharat_democratic"
    removed_raj = False
    kept = []
    for line in result.splitlines(keepends=True):
        match = pattern.match(line)
        if match and match.group(1) == raj_key:
            if removed_raj:
                raise ValueError(f"duplicate orphan RAJ localisation in {relative}")
            removed_raj = True
            continue
        kept.append(line)
    result = b"".join(kept)
    if raj_key + b":" in result:
        raise ValueError(f"orphan RAJ localisation remains in {relative}")
    return result


def canonical_text_bytes(data: bytes) -> bytes:
    """Ignore only newline convention and a final newline during comparison."""
    return data.replace(b"\r\n", b"\n").rstrip(b"\n")


def matching_brace(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for index in range(opening, len(text)):
        char = text[index]
        if char in "\r\n":
            comment = False
            continue
        if comment:
            continue
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == "#":
            comment = True
        elif char == '"':
            quoted = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index + 1
    raise ValueError(f"unclosed event block at offset {opening}")


def stripped_line(line: str) -> str:
    return line.rstrip("\r\n").strip()


def replace_unique_line(
    block: str, old: str, new: str, label: str
) -> str:
    lines = block.splitlines(keepends=True)
    old_indexes = [index for index, line in enumerate(lines) if stripped_line(line) == old]
    new_indexes = [index for index, line in enumerate(lines) if stripped_line(line) == new]
    if not old_indexes and len(new_indexes) == 1:
        return block
    if len(old_indexes) != 1 or new_indexes:
        raise ValueError(
            f"{label}: expected one old line and no new line; "
            f"old={len(old_indexes)} new={len(new_indexes)}"
        )
    index = old_indexes[0]
    line = lines[index]
    body = line.rstrip("\r\n")
    ending = line[len(body):]
    indentation = body[: len(body) - len(body.lstrip(" \t"))]
    lines[index] = indentation + new + ending
    return "".join(lines)


def insert_lines_after_unique(
    block: str, anchor: str, additions: tuple[str, ...], label: str
) -> str:
    lines = block.splitlines(keepends=True)
    anchors = [index for index, line in enumerate(lines) if stripped_line(line) == anchor]
    if len(anchors) != 1:
        raise ValueError(f"{label}: expected one anchor, got {len(anchors)}")
    index = anchors[0]
    following = tuple(
        stripped_line(line) for line in lines[index + 1:index + 1 + len(additions)]
    )
    if following == additions:
        return block
    present = {
        addition: sum(stripped_line(line) == addition for line in lines)
        for addition in additions
    }
    if any(present.values()):
        raise ValueError(f"{label}: partial or displaced additions: {present}")
    anchor_line = lines[index]
    body = anchor_line.rstrip("\r\n")
    ending = anchor_line[len(body):]
    if not ending:
        ending = "\r\n" if "\r\n" in block else "\n"
    indentation = body[: len(body) - len(body.lstrip(" \t"))]
    inserted = [indentation + addition + ending for addition in additions]
    lines[index + 1:index + 1] = inserted
    return "".join(lines)


def assignment_block_span(text: str, key: str) -> tuple[int, int]:
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*\{{")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError(f"{key}: expected one assignment block, got {len(matches)}")
    match = matches[0]
    opening = text.find("{", match.start(), match.end())
    return match.start(), matching_brace(text, opening)


def assignment_block_spans_with_lines(
    text: str, key: str, required_lines: tuple[str, ...]
) -> list[tuple[int, int]]:
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*\{{")
    spans: list[tuple[int, int]] = []
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        end = matching_brace(text, opening)
        candidate = text[match.start():end]
        candidate_lines = {stripped_line(line) for line in candidate.splitlines()}
        if all(required in candidate_lines for required in required_lines):
            spans.append((match.start(), end))
    return spans


def identified_block_span(text: str, kind: str, identifier: str) -> tuple[int, int]:
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(kind)}[ \t]*=[ \t]*\{{")
    identifier_pattern = re.compile(
        rf"(?m)^[ \t]*id[ \t]*=[ \t]*{re.escape(identifier)}[ \t]*(?:#.*)?\r?$"
    )
    spans: list[tuple[int, int]] = []
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        end = matching_brace(text, opening)
        if identifier_pattern.search(text[match.start():end]):
            spans.append((match.start(), end))
    if len(spans) != 1:
        raise ValueError(
            f"{kind} {identifier}: expected one identified block, got {len(spans)}"
        )
    return spans[0]


def update_block(
    text: str,
    span: tuple[int, int],
    transform,
) -> str:
    start, end = span
    return text[:start] + transform(text[start:end]) + text[end:]


def state_block_spans(
    text: str, state_id: int, required_lines: tuple[str, ...]
) -> list[tuple[int, int]]:
    pattern = re.compile(rf"(?m)^[ \t]*{state_id}[ \t]*=[ \t]*\{{")
    spans: list[tuple[int, int]] = []
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        end = matching_brace(text, opening)
        candidate = text[match.start():end]
        candidate_lines = {stripped_line(line) for line in candidate.splitlines()}
        if all(required in candidate_lines for required in required_lines):
            spans.append((match.start(), end))
    return spans


def insert_state_blocks_after(
    text: str,
    anchor_state: int,
    additions: tuple[int, ...],
    required_lines: tuple[str, ...],
    label: str,
) -> str:
    anchor_spans = state_block_spans(text, anchor_state, required_lines)
    if len(anchor_spans) != 1:
        raise ValueError(f"{label}: expected one anchor state block, got {len(anchor_spans)}")
    present = {
        state_id: len(state_block_spans(text, state_id, required_lines))
        for state_id in additions
    }
    if all(count == 1 for count in present.values()):
        return text
    if any(present.values()):
        raise ValueError(f"{label}: partial added state blocks: {present}")

    start, end = anchor_spans[0]
    while end < len(text) and text[end] in " \t":
        end += 1
    if text[end:end + 2] == "\r\n":
        end += 2
    elif text[end:end + 1] in {"\r", "\n"}:
        end += 1
    template = text[start:end]
    header = re.search(rf"(?m)^([ \t]*){anchor_state}([ \t]*=[ \t]*\{{)", template)
    if header is None:
        raise ValueError(f"{label}: cannot identify anchor block header")
    generated: list[str] = []
    for state_id in additions:
        generated_block = (
            template[:header.start()]
            + header.group(1)
            + str(state_id)
            + header.group(2)
            + template[header.end():]
        )
        generated.append(re.sub(r"[ \t]+(?=\r?$)", "", generated_block, flags=re.MULTILINE))
    return text[:end] + "".join(generated) + text[end:]


def repair_manchuria_state_coverage(relative: str, data: bytes) -> bytes:
    """Rebase HOK's Manchuria acquisition paths onto RT56's state model."""
    bom = data.startswith(b"\xef\xbb\xbf")
    text = (data[3:] if bom else data).decode("utf-8")
    split_controls = tuple(
        f"controls_state = {state_id}" for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
    )
    split_full_controls = tuple(
        f"has_full_control_of_state = {state_id}"
        for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
    )
    split_transfers = tuple(
        f"transfer_state = {state_id}" for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
    )
    split_core_scopes = tuple(
        f"{state_id} = {{ add_core_of = ROOT }}"
        for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
    )
    split_separatism_scopes = tuple(
        f"{state_id} = {{ add_dynamic_modifier = {{ modifier = chinese_separatism }} }}"
        for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
    )

    if relative == "common/decisions/KOR_decision.txt":
        def repair_triumph(block: str) -> str:
            block = replace_unique_line(
                block,
                "#controls_state = 745 #dalian",
                "controls_state = 745 #dalian",
                "Manchuria triumph Dalian control",
            )
            block = insert_lines_after_unique(
                block,
                "controls_state = 715 #liaoning",
                ("controls_state = 610", *split_controls),
                "Manchuria triumph control set",
            )
            block = insert_lines_after_unique(
                block,
                "610 = { add_core_of = ROOT }",
                split_core_scopes,
                "Manchuria triumph core set",
            )
            block = insert_lines_after_unique(
                block,
                "610 = { add_dynamic_modifier = { modifier = chinese_separatism } }",
                split_separatism_scopes,
                "Manchuria triumph separatism set",
            )
            block = replace_unique_line(
                block,
                "#transfer_state = 610",
                "transfer_state = 610",
                "Manchuria triumph Jehol transfer",
            )
            block = insert_lines_after_unique(
                block,
                "transfer_state = 716",
                ("transfer_state = 745",),
                "Manchuria triumph Dalian transfer",
            )
            return insert_lines_after_unique(
                block,
                "transfer_state = 610",
                split_transfers,
                "Manchuria triumph split-state transfers",
            )

        text = update_block(
            text,
            assignment_block_span(text, "kor_triumph_for_the_manchuria"),
            repair_triumph,
        )

        def repair_defeat_japan(block: str) -> str:
            subject_gate_comment = (
                "# Keep the peace decision available if RT56 ends MAN's Japanese "
                "subject relationship first."
            )
            for section_name in ("available", "visible"):
                block = update_block(
                    block,
                    assignment_block_span(block, section_name),
                    lambda section, section_name=section_name: replace_unique_line(
                        section,
                        "MAN = { is_subject_of = JAP }",
                        subject_gate_comment,
                        f"Defeat Japan {section_name} Manchukuo subject gate",
                    ),
                )
            block = replace_unique_line(
                block,
                "#has_full_control_of_state = 610",
                "has_full_control_of_state = 610",
                "Defeat Japan Jehol control",
            )
            block = insert_lines_after_unique(
                block,
                "has_full_control_of_state = 610",
                split_full_controls,
                "Defeat Japan control set",
            )
            return insert_lines_after_unique(
                block,
                "transfer_state = 610",
                split_transfers,
                "Defeat Japan transfer tooltip",
            )

        text = update_block(
            text,
            assignment_block_span(text, "KOR_defeat_japan"),
            repair_defeat_japan,
        )

    elif relative == "events/korea.txt":
        def repair_peace(block: str) -> str:
            block = insert_lines_after_unique(
                block,
                "transfer_state = 610",
                split_transfers,
                "Japan peace split-state transfers",
            )

            state_core_line = "remove_core_of = MAN"
            state_core_counts = {
                state_id: sum(
                    stripped_line(candidate_line)
                    == f"{state_id} = {{ {state_core_line} }}"
                    for candidate_line in block.splitlines()
                )
                for state_id in MANCHURIA_STATE_IDS
            }
            legacy_core_lines = tuple(
                f"remove_state_core = {state_id}"
                for state_id in MANCHURIA_STATE_IDS
            )
            legacy_core_counts = {
                line: sum(
                    stripped_line(candidate_line) == line
                    for candidate_line in block.splitlines()
                )
                for line in legacy_core_lines
            }
            if all(count == 1 for count in state_core_counts.values()):
                if any(legacy_core_counts.values()):
                    raise ValueError(
                        "Japan peace Manchukuo core removal: legacy country-scope "
                        "effects remain beside state-scope effects"
                    )
            elif any(state_core_counts.values()):
                raise ValueError(
                    "Japan peace Manchukuo core removal: partial state-scope "
                    f"conversion: {state_core_counts}"
                )
            else:
                block = insert_lines_after_unique(
                    block,
                    "remove_state_core = 610",
                    tuple(
                        f"remove_state_core = {state_id}"
                        for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
                    ),
                    "Japan peace Manchukuo core removal",
                )
                legacy_core_counts = {
                    line: sum(
                        stripped_line(candidate_line) == line
                        for candidate_line in block.splitlines()
                    )
                    for line in legacy_core_lines
                }
                if any(count != 1 for count in legacy_core_counts.values()):
                    raise ValueError(
                        "Japan peace Manchukuo core removal: unexpected legacy "
                        f"effect counts: {legacy_core_counts}"
                    )
                man_core_spans = assignment_block_spans_with_lines(
                    block, "MAN", legacy_core_lines
                )
                if len(man_core_spans) != 1:
                    raise ValueError(
                        "Japan peace Manchukuo core removal: expected one legacy "
                        f"MAN block, got {len(man_core_spans)}"
                    )
                start, end = man_core_spans[0]
                header = re.match(r"([ \t]*)MAN[ \t]*=[ \t]*\{", block[start:end])
                if header is None:
                    raise ValueError(
                        "Japan peace Manchukuo core removal: cannot identify "
                        "legacy MAN block indentation"
                    )
                newline = "\r\n" if "\r\n" in block else "\n"
                indentation = header.group(1)
                replacement = newline.join(
                    f"{indentation}{state_id} = {{ {state_core_line} }}"
                    for state_id in MANCHURIA_STATE_IDS
                )
                block = block[:start] + replacement + block[end:]

            annex_lines = (
                "annex_country = {",
                "target = MAN",
                "transfer_troops = yes",
            )
            annex_spans = assignment_block_spans_with_lines(
                block, "JAP", annex_lines
            )
            if len(annex_spans) != 1:
                raise ValueError(
                    "Japan peace Manchukuo annex: expected one JAP annex block, "
                    f"got {len(annex_spans)}"
                )
            guard_lines = (
                "limit = {",
                "MAN = {",
                "exists = yes",
                "is_subject_of = JAP",
                "JAP = {",
                *annex_lines,
            )
            guard_spans = assignment_block_spans_with_lines(
                block, "if", guard_lines
            )
            annex_start, annex_end = annex_spans[0]
            if len(guard_spans) == 1:
                guard_start, guard_end = guard_spans[0]
                if not (guard_start < annex_start and annex_end < guard_end):
                    raise ValueError(
                        "Japan peace Manchukuo annex: annex block is outside its guard"
                    )
            elif guard_spans:
                raise ValueError(
                    "Japan peace Manchukuo annex: expected at most one guard, "
                    f"got {len(guard_spans)}"
                )
            else:
                containing_if_blocks = [
                    span
                    for span in assignment_block_spans_with_lines(block, "if", ())
                    if span[0] < annex_start and annex_end < span[1]
                ]
                if containing_if_blocks:
                    raise ValueError(
                        "Japan peace Manchukuo annex: refusing to wrap an "
                        "unexpected nested annex block"
                    )

                annex_block = block[annex_start:annex_end]
                header = re.match(r"([ \t]*)JAP[ \t]*=[ \t]*\{", annex_block)
                if header is None:
                    raise ValueError(
                        "Japan peace Manchukuo annex: cannot identify JAP indentation"
                    )
                newline = "\r\n" if "\r\n" in block else "\n"
                indentation = header.group(1)
                indented_annex = newline.join(
                    "\t" + line for line in annex_block.splitlines()
                )
                guarded_annex = newline.join(
                    (
                        f"{indentation}# Safely handle a surviving MAN if RT56 changes its Japanese subject status.",
                        f"{indentation}if = {{",
                        f"{indentation}\tlimit = {{",
                        f"{indentation}\t\tMAN = {{",
                        f"{indentation}\t\t\texists = yes",
                        f"{indentation}\t\t\tis_subject_of = JAP",
                        f"{indentation}\t\t}}",
                        f"{indentation}\t}}",
                        indented_annex,
                        f"{indentation}}}",
                    )
                )
                block = (
                    block[:annex_start] + guarded_annex + block[annex_end:]
                )

            block = replace_unique_line(
                block,
                "# RT56 can end MAN's Japanese subject relationship first.",
                "# Safely handle a surviving MAN if RT56 changes its Japanese subject status.",
                "Japan peace Manchukuo survival comment",
            )
            guard_spans = assignment_block_spans_with_lines(
                block, "if", guard_lines
            )
            if len(guard_spans) != 1:
                raise ValueError(
                    "Japan peace Manchukuo annex: guarded output is not unique"
                )
            guard_start, guard_end = guard_spans[0]

            man_peace_guard_lines = (
                "limit = {",
                "MAN = {",
                "exists = yes",
                "has_war_with = KOR",
                "white_peace = KOR",
            )
            man_peace_guard_spans = assignment_block_spans_with_lines(
                block, "if", man_peace_guard_lines
            )
            if len(man_peace_guard_spans) == 1:
                peace_start, peace_end = man_peace_guard_spans[0]
                if not (peace_start < peace_end < guard_start):
                    raise ValueError(
                        "Japan peace Manchukuo war cleanup: guard must precede annex"
                    )
                return block
            if man_peace_guard_spans:
                raise ValueError(
                    "Japan peace Manchukuo war cleanup: expected at most one guard, "
                    f"got {len(man_peace_guard_spans)}"
                )
            partial_man_peace = assignment_block_spans_with_lines(
                block, "MAN", ("white_peace = KOR",)
            ) + assignment_block_spans_with_lines(
                block, "MAN", ("exists = yes", "has_war_with = KOR")
            )
            if partial_man_peace:
                raise ValueError(
                    "Japan peace Manchukuo war cleanup: partial or displaced guard"
                )

            guard_block = block[guard_start:guard_end]
            header = re.match(r"([ \t]*)if[ \t]*=[ \t]*\{", guard_block)
            if header is None:
                raise ValueError(
                    "Japan peace Manchukuo war cleanup: cannot identify indentation"
                )
            newline = "\r\n" if "\r\n" in block else "\n"
            indentation = header.group(1)
            guarded_man_peace = newline.join(
                (
                    f"{indentation}# A surviving MAN may still be at war with Korea.",
                    f"{indentation}if = {{",
                    f"{indentation}\tlimit = {{",
                    f"{indentation}\t\tMAN = {{",
                    f"{indentation}\t\t\texists = yes",
                    f"{indentation}\t\t\thas_war_with = KOR",
                    f"{indentation}\t\t}}",
                    f"{indentation}\t}}",
                    f"{indentation}\tMAN = {{",
                    f"{indentation}\t\twhite_peace = KOR",
                    f"{indentation}\t}}",
                    f"{indentation}}}",
                )
            )
            return (
                block[:guard_start]
                + guarded_man_peace
                + newline
                + block[guard_start:]
            )

        text = update_block(
            text,
            identified_block_span(text, "country_event", "kor_events.1"),
            repair_peace,
        )

        def repair_manschluss_accept(block: str) -> str:
            block = insert_lines_after_unique(
                block,
                "transfer_state = 716",
                ("transfer_state = 745",),
                "Manschluss Dalian transfer",
            )
            return insert_lines_after_unique(
                block,
                "transfer_state = 610",
                split_transfers,
                "Manschluss split-state transfers",
            )

        text = update_block(
            text,
            identified_block_span(text, "country_event", "kor_events.14"),
            repair_manschluss_accept,
        )

    elif relative == "common/on_actions/gookppong_on_actions.txt":
        text = insert_lines_after_unique(
            text,
            "transfer_state = 610",
            split_transfers,
            "Gookppong split-state transfers",
        )
        text = insert_lines_after_unique(
            text,
            "610 = { add_core_of = KOR }",
            tuple(
                f"{state_id} = {{ add_core_of = KOR }}"
                for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
            ),
            "Gookppong split-state Korean cores",
        )
        text = insert_lines_after_unique(
            text,
            "610 = { add_dynamic_modifier = { modifier = chinese_separatism } }",
            split_separatism_scopes,
            "Gookppong split-state separatism",
        )
        text = insert_state_blocks_after(
            text,
            610,
            RT56_MANCHURIA_SPLIT_STATE_IDS,
            ("remove_core_of = MAN", "remove_core_of = CHI", "remove_core_of = PRC"),
            "Gookppong split-state Chinese core removal",
        )
        split_unit_cleanup = tuple(
            f"delete_unit = {{ state = {state_id} }}"
            for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
        )
        for country in ("JAP", "MAN"):
            text = update_block(
                text,
                assignment_block_span(text, country),
                lambda block, country=country: insert_lines_after_unique(
                    block,
                    "delete_unit = { state = 610 }",
                    split_unit_cleanup,
                    f"Gookppong {country} split-state unit cleanup",
                ),
            )

    elif relative == "common/national_focus/korea.txt":
        def extend_modifier_set(
            block: str, action: str, modifier: str, label: str
        ) -> str:
            return insert_lines_after_unique(
                block,
                f"610 = {{ {action} = {{ modifier = {modifier} }} }}",
                tuple(
                    f"{state_id} = {{ {action} = {{ modifier = {modifier} }} }}"
                    for state_id in RT56_MANCHURIA_SPLIT_STATE_IDS
                ),
                label,
            )

        def repair_multiethnic(block: str) -> str:
            block = extend_modifier_set(
                block,
                "remove_dynamic_modifier",
                "chinese_separatism",
                "Multiethnic embrace strong separatism removal",
            )
            return extend_modifier_set(
                block,
                "add_dynamic_modifier",
                "weakened_chinese_separatism",
                "Multiethnic embrace weakened separatism",
            )

        text = update_block(
            text,
            identified_block_span(text, "focus", "KOR_multiethnic_embrace"),
            repair_multiethnic,
        )
        text = update_block(
            text,
            identified_block_span(text, "focus", "KOR_korean_dream"),
            lambda block: extend_modifier_set(
                block,
                "remove_dynamic_modifier",
                "weakened_chinese_separatism",
                "Korean dream weakened separatism removal",
            ),
        )
        text = update_block(
            text,
            identified_block_span(
                text, "focus", "KOR_teaching_korean_to_manchurians"
            ),
            repair_multiethnic,
        )

    payload = text.encode("utf-8")
    return (b"\xef\xbb\xbf" if bom else b"") + payload


def repair_korea_events(data: bytes) -> bytes:
    bom = data.startswith(b"\xef\xbb\xbf")
    text = (data[3:] if bom else data).decode("utf-8")
    event_start = re.compile(r"(?m)^[ \t]*country_event[ \t]*=[ \t]*\{")

    def find_event_span(identifier: str) -> tuple[int, int] | None:
        for event_match in event_start.finditer(text):
            event_opening = text.find("{", event_match.start(), event_match.end())
            event_end = matching_brace(text, event_opening)
            event_block = text[event_match.start():event_end]
            event_id = re.search(
                r"(?m)^[ \t]*id[ \t]*=[ \t]*(kor_events\.[0-9]+)[ \t]*\r?$",
                event_block,
            )
            if event_id and event_id.group(1) == identifier:
                return event_match.start(), event_end
        return None

    identified: dict[str, tuple[int, int]] = {}
    for match in event_start.finditer(text):
        opening = text.find("{", match.start(), match.end())
        end = matching_brace(text, opening)
        block = text[match.start():end]
        id_match = re.search(
            r"(?m)^[ \t]*id[ \t]*=[ \t]*(kor_events\.[0-9]+)[ \t]*\r?$",
            block,
        )
        if id_match:
            identified[id_match.group(1)] = (match.start(), end)

    required = {"kor_events.51", "kor_events.55"}
    if required - set(identified):
        raise ValueError(
            f"missing reviewed Korea event blocks: {sorted(required - set(identified))}"
        )

    if "kor_events.44" in identified:
        start, end = identified["kor_events.44"]
        while end < len(text) and text[end] in " \t\r\n":
            end += 1
        text = text[:start] + text[end:]

    for identifier, picture in (
        ("kor_events.51", "GFX_report_event_usa_destroyers"),
        ("kor_events.55", "GFX_report_event_merchant_ship_01"),
    ):
        # Re-find after the preceding deletion changed offsets.
        span = find_event_span(identifier)
        if span is None:
            raise ValueError(f"cannot re-find event {identifier}")
        block_start, block_end = span
        block = text[block_start:block_end]
        placeholder = re.compile(
            r"(?m)^([ \t]*picture[ \t]*=[ \t]*)GFX_[ \t]*\r?$"
        )
        resolved = re.compile(
            rf"(?m)^[ \t]*picture[ \t]*=[ \t]*{re.escape(picture)}[ \t]*\r?$"
        )
        placeholder_count = len(placeholder.findall(block))
        resolved_count = len(resolved.findall(block))
        if placeholder_count == 0 and resolved_count == 1:
            continue
        if placeholder_count != 1 or resolved_count:
            raise ValueError(f"unexpected picture placeholder count in {identifier}")
        placeholder_match = placeholder.search(block)
        if placeholder_match is None:
            raise ValueError(f"cannot locate picture placeholder in {identifier}")
        replacement = placeholder_match.group(0).replace("GFX_", picture, 1)
        block = (
            block[:placeholder_match.start()]
            + replacement
            + block[placeholder_match.end():]
        )
        text = text[:block_start] + block + text[block_end:]

    if "picture = GFX_\r" in text or "picture = GFX_\n" in text:
        raise ValueError("empty event picture placeholder remains")
    payload = text.encode("utf-8")
    return (b"\xef\xbb\xbf" if bom else b"") + payload


def source_targets() -> list[tuple[str, bytes, bytes]]:
    mapping = {**PROVINCE_ID_MAP, **STATE_ID_MAP}
    targets: list[tuple[str, bytes, bytes]] = []
    for root_name in TEXT_ROOTS:
        source_root = HOK_ROOT / root_name
        for source in source_root.rglob("*"):
            if not source.is_file() or source.suffix.lower() not in TEXT_SUFFIXES:
                continue
            relative = source.relative_to(HOK_ROOT).as_posix()
            # [2026-09-22]_kpopmodder: The Korean update builder owns all 20 selected files.
            if relative in FOCUS_UPDATE_PATHS:
                continue
            if relative.startswith("history/states/") or relative in SHARED_MERGE_PATHS:
                continue
            destination = REPO_ROOT / Path(relative)
            if not destination.is_file():
                continue
            original = source.read_bytes()
            migrated = replace_tokens(original, mapping)
            if relative.endswith("HoK_state_name_l_english.yml") or relative.endswith(
                "HoK_state_name_l_korean.yml"
            ):
                migrated = migrated.replace(b"STATE_1088", b"STATE_1147")
            migrated = apply_post_migration_fixes(relative, migrated)
            if migrated != original:
                targets.append((relative, original, migrated))
    return sorted(targets)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write the reviewed ID migration")
    parser.add_argument("--list", action="store_true", help="list affected HOK-owned files")
    args = parser.parse_args()
    if not args.apply and not args.list:
        parser.error("choose --apply or --list")

    targets = source_targets()
    changed = 0
    for relative, original, migrated in targets:
        destination = (REPO_ROOT / Path(relative)).resolve()
        destination.relative_to(REPO_ROOT)
        current = destination.read_bytes()
        legacy_migrated = replace_tokens(original, {**PROVINCE_ID_MAP, **STATE_ID_MAP})
        if relative.endswith("HoK_state_name_l_english.yml") or relative.endswith(
            "HoK_state_name_l_korean.yml"
        ):
            legacy_migrated = legacy_migrated.replace(b"STATE_1088", b"STATE_1147")
        if current == migrated:
            status = "already-migrated"
        elif canonical_text_bytes(current) == canonical_text_bytes(migrated):
            status = "would-normalize"
            if args.apply:
                temporary = destination.with_name(destination.name + ".hok-id.tmp")
                temporary.write_bytes(migrated)
                temporary.replace(destination)
                status = "normalized"
                changed += 1
        elif canonical_text_bytes(apply_post_migration_fixes(relative, current)) == canonical_text_bytes(
            migrated
        ):
            status = "would-finish-migration"
            if args.apply:
                temporary = destination.with_name(destination.name + ".hok-id.tmp")
                temporary.write_bytes(migrated)
                temporary.replace(destination)
                status = "migration-finished"
                changed += 1
        elif current == original or current == legacy_migrated:
            status = "would-migrate"
            if args.apply:
                temporary = destination.with_name(destination.name + ".hok-id.tmp")
                temporary.write_bytes(migrated)
                temporary.replace(destination)
                status = "migrated"
                changed += 1
        else:
            print(
                f"ERROR: refusing to overwrite independently changed file: {relative}",
                file=sys.stderr,
            )
            return 2
        print(f"{status:16} {relative}")
    print(f"files={len(targets)} newly-written={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
