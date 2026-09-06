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

from build_rt56_map import (
    HOK_ROOT,
    PROVINCE_ID_MAP,
    REPO_ROOT,
    STATE_ID_MAP,
)


TEXT_ROOTS = ("common", "events", "history", "localisation")
TEXT_SUFFIXES = {".txt", ".yml", ".gui", ".gfx", ".asset", ".csv"}

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

    required = {"kor_events.44", "kor_events.51", "kor_events.55"}
    if required - set(identified):
        raise ValueError(
            f"missing reviewed Korea event blocks: {sorted(required - set(identified))}"
        )

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
        if block.count("picture = GFX_") != 1:
            raise ValueError(f"unexpected picture placeholder count in {identifier}")
        block = block.replace("picture = GFX_", f"picture = {picture}")
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
