#!/usr/bin/env python3
"""Run the reproducible, read-only static gate for the HOK–RT56 port.

This validator does not launch Hearts of Iron IV and therefore cannot prove
engine parsing, launcher load order, gameplay behavior, or localisation UI.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COMPAT_REMOTE_FILE_ID = "3796816200"

GENERATOR_CHECKS = (
    ("map synthesis", "build_rt56_map.py", "--check"),
    ("shared overrides", "build_shared_overrides.py", "--check"),
    ("East Asia overrides", "build_east_asia_overrides.py", "--check"),
    ("HOK-first Korean assets", "build_korean_assets.py", "--check"),
    ("RT56-owned pruning", "prune_rt56_owned_files.py", "--check"),
    ("Korea-only pruning", "prune_non_korean_content.py", "--check"),
    ("HOK ID migration", "migrate_hok_ids.py", "--list"),
    ("doctrine migration", "migrate_doctrines.py", "--check"),
    ("1,014-file integration manifest", "build_integration_manifest.py", "--check"),
)

SCRIPT_SUFFIXES = {".txt", ".gfx", ".asset", ".gui"}
SCRIPT_ROOTS = (
    "common",
    "events",
    "gfx",
    "history",
    "interface",
    "music",
    "portraits",
    "sound",
)

# The line-oriented global map databases are checked by build_rt56_map.py.
# Only Paradox-script strategic-region files need the generic structure scan.
EXTRA_SCRIPT_ROOTS = ("map/strategicregions",)

EXPECTED_COMPAT_STATE_IDS = {
    525,
    527,
    528,
    917,
    918,
    919,
    920,
    1144,
    1145,
    1146,
    1147,
}

RT56_MANCHURIA_SPLIT_STATE_IDS = frozenset(range(941, 948))
MANCHURIA_STATE_IDS = frozenset((716, 745, 328, 717, 714, 761, 715, 610)) | (
    RT56_MANCHURIA_SPLIT_STATE_IDS
)
KOREA_CONTROL_STATE_IDS = frozenset((919, 918, 525, 1144, 1145, 920, 527, 917))
ACQUISITION_CONTROL_STATE_IDS = MANCHURIA_STATE_IDS | KOREA_CONTROL_STATE_IDS

LEGACY_HOK_STATE_IDS = (1028, 1029, 1030, 1031, 1082, 1083, 1084, 1085)

BANNED_TOKEN_PATTERNS = {
    "original Workshop upload identity": re.compile(r"(?<![0-9])2898629778(?![0-9])"),
    "donor Workshop upload identity": re.compile(r"(?<![0-9])3793992662(?![0-9])"),
    "obsolete HOK achievement namespace": re.compile(
        r"(?<![A-Za-z0-9_])HoK_achievements_2898629778(?![A-Za-z0-9_])"
    ),
    "removed equipment ID": re.compile(
        r"(?<![A-Za-z0-9_])supersonic_fighter_equipment_1(?![A-Za-z0-9_])"
    ),
    "retired RT56 transport technology": re.compile(
        r"(?<![A-Za-z0-9_])(?:bba_early_transport_plane|early_transport_plane)"
        r"(?![A-Za-z0-9_])"
    ),
    "stale Kim Gu character ID": re.compile(
        r"(?<![A-Za-z0-9_])KOR_kim_gu(?![A-Za-z0-9_])"
    ),
    "missing RT56 focus ID": re.compile(
        r"(?<![A-Za-z0-9_])KOR_cement_monarchic_rule(?![A-Za-z0-9_])"
    ),
    "invalid division-name casing": re.compile(
        r"(?<![A-Za-z0-9_])KOR_Inf_01(?![A-Za-z0-9_])"
    ),
    "invalid ship type casing": re.compile(
        r"(?<![A-Za-z0-9_])Light_cruiser(?![A-Za-z0-9_])"
    ),
    "removed FIN challenge flag": re.compile(
        r"(?<![A-Za-z0-9_])fin_finnppong_option_enabled(?![A-Za-z0-9_])"
    ),
    "removed FIN/MON/SIB rule localisation": re.compile(
        r"(?<![A-Za-z0-9_])(?:FINNPPONG|MONGPPONG|SIBBPPONG)[A-Za-z0-9_]*(?![A-Za-z0-9_])"
    ),
    "removed MON country-name override": re.compile(
        r"(?m)^[ \t]*MON_(?:fascism|democratic|neutrality|communism)(?:_DEF)?:[0-9]+"
    ),
    "removed orphan Japan cosmetic tag": re.compile(
        r"(?<![A-Za-z0-9_])JAP_(?:yamato_kyowakoku|daiwa_mingoku|fuso_gasshukoku)(?:_DEF|_ADJ)?(?![A-Za-z0-9_])"
    ),
    "removed orphan RAJ cosmetic tag": re.compile(
        r"(?<![A-Za-z0-9_])RAJ_bharat_democratic(?![A-Za-z0-9_])"
    ),
    "removed unregistered Japan music": re.compile(
        r"(?<![A-Za-z0-9_])Minshu_ikki(?![A-Za-z0-9_])"
    ),
    "removed orphan Japan GFX": re.compile(
        r"(?<![A-Za-z0-9_])(?:GFX_focus_JAP_(?:proclaim_the_republic|oppose_peace_preservation_law|integrate_nanyo_gunto|joint_staff_office|demand_sagaren|free_election_in_taiwan|memories_of_taisho_democracy|purge_the_militarists|rok_jpn_free_trade_agreement|develop_home_island)(?:_shine)?|GFX_idea_jap_(?:joint_staff_office|tachikawa)|GFX_report_event_(?:jap_fuse_tatsuji|japanese_people_protest)|GFX_Portrait_JAP_(?:japanese_national_liberation_committee|tatsuji_fuse|tadamichi_kuribayashi(?:_small)?|sigesaburo_miyazaki(?:_small)?|shin_yoshida(?:_small)?|mitsumasa_yonai_navy(?:_small)?|masatomi_kimura(?:_small)?|renya_mutaguchi(?:_small)?))(?![A-Za-z0-9_])"
    ),
    "removed orphan Japan traits": re.compile(
        r"(?<![A-Za-z0-9_])(?:JAP_japanese_national_liberation_committee_trait|JAP_champion)(?![A-Za-z0-9_])"
    ),
    "removed orphan Korea/Japan GFX": re.compile(
        r"(?<![A-Za-z0-9_])(?:GFX_decision_cat_jap_unite_karafuto|GFX_report_event_jap_rok_jpn_talks|GFX_focus_KOR_japanese_trade(?:_shine)?)(?![A-Za-z0-9_])"
    ),
    "removed FIN challenge news event": re.compile(
        r"(?<![A-Za-z0-9_.])newsk\.27(?:\.[A-Za-z0-9_]+)?(?![A-Za-z0-9_.])"
    ),
    "removed FIN challenge news picture": re.compile(
        r"(?<![A-Za-z0-9_])GFX_newsk_event_022(?![A-Za-z0-9_])"
    ),
    "removed dead Japan-news event": re.compile(
        r"(?<![A-Za-z0-9_.])newsj\.[1-4](?:\.[A-Za-z0-9_]+)?(?![A-Za-z0-9_.])"
    ),
    "empty event-picture token": re.compile(
        r"(?m)^[ \t]*picture[ \t]*=[ \t]*GFX_[ \t]*(?:#.*)?\r?$"
    ),
}

HOK_EVENT_FILES = (
    "events/korea.txt",
    "events/NewsEvents_KOR.txt",
    "events/HoK_ragnarok.txt",
)

RT56_ROOT = Path(
    r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968"
)
VANILLA_ROOT = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def passed(self, message: str) -> None:
        self.passes.append(message)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_utf8(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig")


def iter_script_files() -> list[Path]:
    paths: list[Path] = []
    for root_name in (*SCRIPT_ROOTS, *EXTRA_SCRIPT_ROOTS):
        directory = ROOT / root_name
        if not directory.is_dir():
            continue
        paths.extend(
            path
            for path in directory.rglob("*")
            if path.is_file() and path.suffix.lower() in SCRIPT_SUFFIXES
        )
    return sorted(set(paths))


def iter_runtime_text_files() -> list[Path]:
    paths = set(iter_script_files())
    for directory_name in (*SCRIPT_ROOTS, "map"):
        directory = ROOT / directory_name
        if not directory.is_dir():
            continue
        paths.update(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".txt", ".yml", ".csv", ".gfx", ".asset", ".gui"}
        )
    paths.add(ROOT / "descriptor.mod")
    return sorted(paths)


def run_generator_checks(result: Validation) -> None:
    for label, script, mode in GENERATOR_CHECKS:
        completed = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools" / script), mode],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode == 0:
            result.passed(f"{label}: reproducible output matches pinned sources")
            continue
        detail = (completed.stderr or completed.stdout).strip().splitlines()
        tail = " | ".join(detail[-4:]) if detail else "no diagnostic output"
        result.error(f"{label} check failed (exit {completed.returncode}): {tail}")


def scan_structure(path: Path, result: Validation) -> None:
    try:
        text = read_utf8(path)
    except UnicodeDecodeError as exc:
        result.error(f"{relative(path)}: not valid UTF-8 ({exc})")
        return

    depth = 0
    quoted = False
    escaped = False
    comment = False
    line = 1
    opening_lines: list[int] = []
    for char in text:
        if char == "\n":
            line += 1
            if comment:
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
            opening_lines.append(line)
        elif char == "}":
            if depth == 0:
                result.error(f"{relative(path)}:{line}: unmatched closing brace")
                return
            depth -= 1
            opening_lines.pop()
    if quoted:
        result.error(f"{relative(path)}:{line}: unterminated quoted string")
    if depth:
        result.error(
            f"{relative(path)}:{opening_lines[-1]}: {depth} unclosed brace(s) at EOF"
        )


def check_script_structure(result: Validation) -> None:
    files = iter_script_files()
    before = len(result.errors)
    for path in files:
        scan_structure(path, result)
    if len(result.errors) == before:
        result.passed(f"Paradox-script structure: {len(files)} UTF-8 files balanced")


def check_descriptor(result: Validation) -> None:
    path = ROOT / "descriptor.mod"
    text = read_utf8(path)
    dependencies = re.search(r"(?s)dependencies\s*=\s*\{(.*?)\}", text)
    names = re.findall(r'"([^"]+)"', dependencies.group(1)) if dependencies else []
    expected_dependencies = ["The Road to 56", "Korean Language"]
    if names != expected_dependencies:
        result.error(
            "descriptor.mod: expected the recorded development dependencies "
            f"{expected_dependencies}, got {names}"
        )
    if not re.search(r'(?m)^version\s*=\s*"0\.1\.0-dev"\s*$', text):
        result.error("descriptor.mod: development version must be 0.1.0-dev")
    if not re.search(r'(?m)^supported_version\s*=\s*"1\.19\.\*"\s*$', text):
        result.error("descriptor.mod: supported_version must be 1.19.*")
    remote_ids = re.findall(r'(?m)^remote_file_id\s*=\s*"([0-9]+)"\s*$', text)
    if remote_ids != [EXPECTED_COMPAT_REMOTE_FILE_ID]:
        result.error(
            "descriptor.mod: expected recorded compatibility remote_file_id "
            f"{EXPECTED_COMPAT_REMOTE_FILE_ID}, got {remote_ids}"
        )
    for forbidden in ("replace_path", "path="):
        if re.search(rf"(?m)^\s*{re.escape(forbidden)}", text):
            result.error(f"descriptor.mod: forbidden active field {forbidden}")
    if not any(error.startswith("descriptor.mod:") for error in result.errors):
        result.passed(
            "descriptor: RT56 + recorded Korean Language dependency; "
            f"compatibility item {EXPECTED_COMPAT_REMOTE_FILE_ID}; no path/replace_path"
        )


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def check_banned_tokens(result: Validation) -> None:
    before = len(result.errors)
    for path in iter_runtime_text_files():
        try:
            text = read_utf8(path)
        except UnicodeDecodeError:
            continue
        for label, pattern in BANNED_TOKEN_PATTERNS.items():
            match = pattern.search(text)
            if match:
                result.error(
                    f"{relative(path)}:{line_number(text, match.start())}: {label} remains"
                )

    # Old HOK state IDs are valid RT56 IDs elsewhere in the world, so this
    # assertion is intentionally limited to non-map compat scripts.  Pinned
    # host-rebased files and map topology receive their own generator checks.
    state_pattern = re.compile(
        r"(?<![0-9])(?:" + "|".join(map(str, LEGACY_HOK_STATE_IDS)) + r")(?![0-9])"
    )
    for path in iter_script_files():
        if relative(path).startswith("map/"):
            continue
        text = read_utf8(path)
        match = state_pattern.search(text)
        if match:
            result.error(
                f"{relative(path)}:{line_number(text, match.start())}: legacy HOK state ID "
                f"{match.group(0)} remains in a compat script"
            )
    if len(result.errors) == before:
        result.passed("retired IDs/modules: no stale runtime token remains")


def check_localisation(result: Validation) -> None:
    root = ROOT / "localisation"
    keys_by_locale: dict[str, dict[str, list[tuple[str, int]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    file_count = 0
    key_count = 0
    before = len(result.errors)
    key_pattern = re.compile(r"^[ \t]*([^#\s][^:]*):[0-9]+(?:[ \t]+|$)")

    for path in sorted(root.rglob("*.yml")):
        file_count += 1
        raw = path.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            result.error(f"{relative(path)}: localisation file lacks UTF-8 BOM")
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            result.error(f"{relative(path)}: invalid UTF-8 ({exc})")
            continue
        parts = path.relative_to(root).parts
        locale = parts[0] if parts else "unknown"
        expected_header = f"l_{locale}:"
        first_content = next(
            (line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")),
            "",
        )
        if first_content != expected_header:
            result.error(
                f"{relative(path)}: expected header {expected_header!r}, got {first_content!r}"
            )

        seen_in_file: dict[str, int] = {}
        for number, line in enumerate(text.splitlines(), start=1):
            match = key_pattern.match(line)
            if not match:
                continue
            key = match.group(1).strip()
            key_count += 1
            if key in seen_in_file:
                result.error(
                    f"{relative(path)}:{number}: duplicate localisation key {key!r}; "
                    f"first at line {seen_in_file[key]}"
                )
            else:
                seen_in_file[key] = number
            keys_by_locale[locale][key].append((relative(path), number))

    for locale, keys in sorted(keys_by_locale.items()):
        for key, locations in sorted(keys.items()):
            unique_files = {location[0] for location in locations}
            if len(unique_files) > 1:
                rendered = ", ".join(f"{path}:{line}" for path, line in locations[:4])
                result.error(
                    f"localisation/{locale}: key {key!r} defined in multiple compat files: {rendered}"
                )

    if len(result.errors) == before:
        result.passed(
            f"localisation: {file_count} files, {key_count} keys; BOM/header/uniqueness pass"
        )


def localisation_keys(root: Path, locale: str) -> set[str]:
    keys: set[str] = set()
    pattern = re.compile(r"^[ \t]*([^#\s][^:]*):[0-9]+(?:[ \t]+|$)")
    directory = root / "localisation" / locale
    if not directory.is_dir():
        return keys
    for path in directory.rglob("*.yml"):
        try:
            text = path.read_bytes().decode("utf-8-sig")
        except UnicodeDecodeError:
            continue
        for line in text.splitlines():
            match = pattern.match(line)
            if match:
                keys.add(match.group(1).strip())
    return keys


def check_hok_event_assets_and_localisation(result: Validation) -> None:
    before = len(result.errors)
    locale_sets = {
        locale: localisation_keys(ROOT, locale) for locale in ("english", "korean")
    }
    loc_reference = re.compile(
        r"(?m)^[ \t]*(?:title|desc|name)[ \t]*=[ \t]*"
        r"((?:kor_events|KOR_events|newsk|hokRagnarok)\.[A-Za-z0-9_.-]+)"
    )
    picture_reference = re.compile(
        r"(?m)^[ \t]*picture[ \t]*=[ \t]*([A-Za-z0-9_.-]+)"
    )

    used_pictures: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for relative_name in HOK_EVENT_FILES:
        path = ROOT / relative_name
        text = read_utf8(path)
        for match in loc_reference.finditer(text):
            key = match.group(1)
            for locale, keys in locale_sets.items():
                if key not in keys:
                    result.error(
                        f"{relative_name}:{line_number(text, match.start())}: "
                        f"missing compat {locale} localisation key {key!r}"
                    )
        for match in picture_reference.finditer(text):
            used_pictures[match.group(1)].append(
                (relative_name, line_number(text, match.start()))
            )

    defined_pictures: set[str] = set()
    sprite_pattern = re.compile(r'(?m)^[ \t]*name[ \t]*=[ \t]*"([A-Za-z0-9_.-]+)"')
    for source_root in (ROOT, RT56_ROOT, VANILLA_ROOT):
        interface_root = source_root / "interface"
        if not interface_root.is_dir():
            continue
        for path in interface_root.rglob("*.gfx"):
            try:
                text = path.read_bytes().decode("utf-8-sig")
            except UnicodeDecodeError:
                continue
            defined_pictures.update(sprite_pattern.findall(text))

    for picture, locations in sorted(used_pictures.items()):
        if picture in defined_pictures:
            continue
        rendered = ", ".join(f"{path}:{line}" for path, line in locations)
        result.error(f"undefined event picture {picture!r}: {rendered}")

    if len(result.errors) == before:
        result.passed(
            "HOK events: English/Korean localisation and picture references resolve"
        )


def mask_comments(text: str) -> str:
    chars = list(text)
    quoted = False
    escaped = False
    comment = False
    for index, char in enumerate(text):
        if char == "\n":
            comment = False
            continue
        if comment:
            chars[index] = " "
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
            chars[index] = " "
        elif char == '"':
            quoted = True
    return "".join(chars)


def matching_brace(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for index in range(opening, len(text)):
        char = text[index]
        if char == "\n":
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
    raise ValueError(f"unclosed brace at {opening}")


def block_depth_at_line_starts(block: str) -> dict[int, int]:
    depths = {0: 0}
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for index, char in enumerate(block):
        if char == "\n":
            comment = False
            depths[index + 1] = depth
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
    return depths


def direct_scalar(block: str, key: str, depth: int = 1) -> str | None:
    depths = block_depth_at_line_starts(block)
    pattern = re.compile(
        rf"(?m)^([ \t]*){re.escape(key)}[ \t]*=[ \t]*(\"[^\"]+\"|[^\s#}}]+)"
    )
    for match in pattern.finditer(mask_comments(block)):
        start = block.rfind("\n", 0, match.start()) + 1
        if depths.get(start) == depth:
            return match.group(2).strip('"')
    return None


def unique_assignment_block(path: Path, key: str, definition_depth: int) -> str:
    text = read_utf8(path)
    clean = mask_comments(text)
    depths = block_depth_at_line_starts(text)
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*\{{")
    matches = []
    for match in pattern.finditer(clean):
        line_start = text.rfind("\n", 0, match.start()) + 1
        if depths.get(line_start) == definition_depth:
            matches.append(match)
    if len(matches) != 1:
        raise ValueError(
            f"{relative(path)}: expected one {key} block, got {len(matches)}"
        )
    match = matches[0]
    opening = clean.find("{", match.start(), match.end())
    return text[match.start():matching_brace(text, opening)]


def unique_identified_block(
    path: Path, kind: str, identifier: str, definition_depth: int
) -> str:
    text = read_utf8(path)
    clean = mask_comments(text)
    depths = block_depth_at_line_starts(text)
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(kind)}[ \t]*=[ \t]*\{{")
    found: list[str] = []
    for match in pattern.finditer(clean):
        line_start = text.rfind("\n", 0, match.start()) + 1
        if depths.get(line_start) != definition_depth:
            continue
        opening = clean.find("{", match.start(), match.end())
        end = matching_brace(text, opening)
        block = text[match.start():end]
        if direct_scalar(block, "id", 1) == identifier:
            found.append(block)
    if len(found) != 1:
        raise ValueError(
            f"{relative(path)}: expected one {kind} {identifier} block, got {len(found)}"
        )
    return found[0]


def structural_depth_at(text: str, offset: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for char in text[:offset]:
        if char == "\n":
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
    return depth


def scalar_values_at_depth(block: str, key: str, depth: int) -> list[str]:
    clean = mask_comments(block)
    pattern = re.compile(
        rf"(?<![A-Za-z0-9_]){re.escape(key)}[ \t]*=[ \t]*"
        r"(\"(?:\\.|[^\"])*\"|[A-Za-z0-9_.:-]+)"
    )
    values: list[str] = []
    for match in pattern.finditer(clean):
        if structural_depth_at(block, match.start()) != depth:
            continue
        values.append(match.group(1).strip('"'))
    return values


def numeric_values_at_depth(block: str, key: str, depth: int) -> list[int]:
    values = scalar_values_at_depth(block, key, depth)
    if any(not value.isdigit() for value in values):
        raise ValueError(f"{key}: expected only numeric values, got {values}")
    return [int(value) for value in values]


def assignment_blocks_at_depth(block: str, key: str, depth: int) -> list[str]:
    clean = mask_comments(block)
    pattern = re.compile(
        rf"(?<![A-Za-z0-9_]){re.escape(key)}[ \t]*=[ \t]*\{{"
    )
    found: list[str] = []
    for match in pattern.finditer(clean):
        if structural_depth_at(block, match.start()) != depth:
            continue
        opening = clean.find("{", match.start(), match.end())
        found.append(block[match.start():matching_brace(block, opening)])
    return found


def unique_nested_block(block: str, key: str, depth: int, label: str) -> str:
    found = assignment_blocks_at_depth(block, key, depth)
    if len(found) != 1:
        raise ValueError(f"{label}: expected one {key} block, got {len(found)}")
    return found[0]


def unique_named_nested_block(
    block: str,
    key: str,
    name_key: str,
    name_value: str,
    depth: int,
    label: str,
) -> str:
    found = [
        candidate
        for candidate in assignment_blocks_at_depth(block, key, depth)
        if scalar_values_at_depth(candidate, name_key, 1) == [name_value]
    ]
    if len(found) != 1:
        raise ValueError(
            f"{label}: expected one {key} block with {name_key}={name_value}, "
            f"got {len(found)}"
        )
    return found[0]


def require_nested_event_call(block: str, event_id: str, label: str) -> None:
    event_call = unique_nested_block(block, "country_event", 1, label)
    if scalar_values_at_depth(event_call, "id", 1) != [event_id]:
        raise ValueError(f"{label}: expected country_event id {event_id}")
    if scalar_values_at_depth(event_call, "days", 1) != ["1"]:
        raise ValueError(f"{label}: expected a one-day event delay")


def matching_state_scopes(
    block: str,
    *,
    scalars: tuple[tuple[str, tuple[str, ...]], ...] = (),
    nested_scalars: tuple[tuple[str, str, str], ...] = (),
) -> list[int]:
    clean = mask_comments(block)
    pattern = re.compile(r"(?m)^[ \t]*([0-9]+)[ \t]*=[ \t]*\{")
    found: list[int] = []
    for match in pattern.finditer(clean):
        if structural_depth_at(block, match.start()) != 1:
            continue
        opening = clean.find("{", match.start(), match.end())
        end = matching_brace(block, opening)
        candidate = block[match.start():end]
        if not all(
            scalar_values_at_depth(candidate, key, 1) == list(expected)
            for key, expected in scalars
        ):
            continue
        if not all(
            len(nested := assignment_blocks_at_depth(candidate, nested_key, 1)) == 1
            and scalar_values_at_depth(nested[0], scalar_key, 1) == [expected]
            for nested_key, scalar_key, expected in nested_scalars
        ):
            continue
        found.append(int(match.group(1)))
    return found


def state_scope_scalar_uses(block: str, key: str) -> list[tuple[int, str]]:
    clean = mask_comments(block)
    pattern = re.compile(r"(?m)^[ \t]*([0-9]+)[ \t]*=[ \t]*\{")
    found: list[tuple[int, str]] = []
    for match in pattern.finditer(clean):
        opening = clean.find("{", match.start(), match.end())
        end = matching_brace(block, opening)
        candidate = block[match.start():end]
        for value in scalar_values_at_depth(candidate, key, 1):
            found.append((int(match.group(1)), value))
    return found


def delete_unit_state_values(block: str) -> list[int]:
    values: list[int] = []
    for unit_block in assignment_blocks_at_depth(block, "delete_unit", 1):
        states = numeric_values_at_depth(unit_block, "state", 1)
        if len(states) != 1:
            raise ValueError(f"delete_unit: expected one state, got {states}")
        values.extend(states)
    return values


def require_state_set(
    result: Validation,
    label: str,
    values: list[int],
    expected: frozenset[int] = MANCHURIA_STATE_IDS,
) -> None:
    actual = set(values)
    duplicates = sorted(state_id for state_id in actual if values.count(state_id) > 1)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra or duplicates:
        result.error(
            f"{label}: reviewed state coverage mismatch; "
            f"missing={missing} extra={extra} duplicates={duplicates}"
        )


def _check_manchuria_state_coverage(result: Validation) -> None:
    before = len(result.errors)
    decisions = ROOT / "common/decisions/KOR_decision.txt"
    events = ROOT / "events/korea.txt"
    on_actions = ROOT / "common/on_actions/gookppong_on_actions.txt"
    focuses = ROOT / "common/national_focus/korea.txt"

    try:
        triumph_category = unique_assignment_block(
            decisions, "KOR_triumph_for_the_manchuria_category", 0
        )
        triumph = unique_nested_block(
            triumph_category,
            "kor_triumph_for_the_manchuria",
            1,
            "Manchuria triumph category",
        )
        triumph_available = unique_nested_block(
            triumph, "available", 1, "Manchuria triumph"
        )
        triumph_effect = unique_nested_block(
            triumph, "complete_effect", 1, "Manchuria triumph"
        )
        triumph_transfer = unique_nested_block(
            triumph_effect, "hidden_effect", 1, "Manchuria triumph"
        )

        defeat_category = unique_assignment_block(
            decisions, "KOR_defeat_japan_category", 0
        )
        defeat_japan = unique_nested_block(
            defeat_category, "KOR_defeat_japan", 1, "Defeat Japan category"
        )
        defeat_available = unique_nested_block(
            defeat_japan, "available", 1, "Defeat Japan"
        )
        defeat_visible = unique_nested_block(
            defeat_japan, "visible", 1, "Defeat Japan"
        )
        defeat_visible_not = unique_nested_block(
            defeat_visible, "NOT", 1, "Defeat Japan visibility"
        )
        defeat_available_kor = unique_nested_block(
            defeat_available, "KOR", 1, "Defeat Japan availability"
        )
        if scalar_values_at_depth(defeat_available, "has_war_with", 1) != ["JAP"]:
            raise ValueError("Defeat Japan: availability must require war with JAP")
        if scalar_values_at_depth(defeat_visible, "has_war_with", 1) != ["JAP"]:
            raise ValueError("Defeat Japan: visibility must require war with JAP")
        if scalar_values_at_depth(defeat_available_kor, "is_in_faction", 1) != ["no"]:
            raise ValueError("Defeat Japan: availability must require KOR factionlessness")
        if scalar_values_at_depth(defeat_visible_not, "has_global_flag", 1) != [
            "kor_defeat_japanese_army"
        ]:
            raise ValueError("Defeat Japan: unexpected completion-flag visibility gate")
        if re.search(
            r"(?<![A-Za-z0-9_])MAN(?![A-Za-z0-9_])",
            mask_comments(defeat_available),
        ):
            raise ValueError(
                "Defeat Japan: availability must not depend on MAN's subject status"
            )
        if re.search(
            r"(?<![A-Za-z0-9_])MAN(?![A-Za-z0-9_])",
            mask_comments(defeat_visible),
        ):
            raise ValueError(
                "Defeat Japan: visibility must not depend on MAN's subject status"
            )
        if scalar_values_at_depth(defeat_japan, "fire_only_once", 1) != ["yes"]:
            raise ValueError("Defeat Japan: decision must remain fire-only-once")
        defeat_effect = unique_nested_block(
            defeat_japan, "complete_effect", 1, "Defeat Japan"
        )
        defeat_tooltip = unique_nested_block(
            defeat_effect, "effect_tooltip", 1, "Defeat Japan"
        )
        defeat_request = unique_nested_block(
            defeat_effect, "JAP", 1, "Defeat Japan"
        )
        if scalar_values_at_depth(defeat_request, "country_event", 1) != [
            "kor_events.1"
        ]:
            raise ValueError("Defeat Japan: expected JAP to receive kor_events.1")

        japan_peace = unique_identified_block(
            events, "country_event", "kor_events.1", 0
        )
        peace_accept = unique_named_nested_block(
            japan_peace,
            "option",
            "name",
            "KOR_events.1.a",
            1,
            "Japan peace",
        )
        peace_recipient = unique_nested_block(
            peace_accept, "FROM", 1, "Japan peace acceptance"
        )
        if scalar_values_at_depth(peace_recipient, "white_peace", 1) != ["JAP"]:
            raise ValueError(
                "Japan peace acceptance: recipient must make white peace with JAP"
            )
        if assignment_blocks_at_depth(peace_accept, "MAN", 1):
            raise ValueError(
                "Japan peace acceptance: MAN core cleanup must use state scopes"
            )
        if re.search(
            r"(?<![A-Za-z0-9_])remove_state_core[ \t]*=",
            mask_comments(japan_peace),
        ):
            raise ValueError(
                "Japan peace acceptance: legacy country-scope core removal remains"
            )
        peace_man_core_states = matching_state_scopes(
            peace_accept, scalars=(("remove_core_of", ("MAN",)),)
        )
        all_core_removal_targets = re.findall(
            r"(?<![A-Za-z0-9_])remove_core_of[ \t]*=[ \t]*"
            r"([A-Za-z0-9_.:-]+)",
            mask_comments(japan_peace),
        )
        if all_core_removal_targets != ["MAN"] * len(MANCHURIA_STATE_IDS):
            raise ValueError(
                "Japan peace acceptance: expected exactly 15 MAN core removals, "
                f"got {all_core_removal_targets}"
            )

        annex_country_count = len(
            re.findall(
                r"(?<![A-Za-z0-9_])annex_country[ \t]*=[ \t]*\{",
                mask_comments(japan_peace),
            )
        )
        if annex_country_count != 1:
            raise ValueError(
                "Japan peace acceptance: expected exactly one annex_country block, "
                f"got {annex_country_count}"
            )

        guarded_man_peaces: list[str] = []
        for conditional in assignment_blocks_at_depth(peace_accept, "if", 1):
            limits = assignment_blocks_at_depth(conditional, "limit", 1)
            if len(limits) != 1:
                continue
            man_guards = assignment_blocks_at_depth(limits[0], "MAN", 1)
            if len(man_guards) != 1:
                continue
            man_guard = man_guards[0]
            if scalar_values_at_depth(man_guard, "exists", 1) != ["yes"]:
                continue
            if scalar_values_at_depth(man_guard, "has_war_with", 1) != ["KOR"]:
                continue
            man_effects = assignment_blocks_at_depth(conditional, "MAN", 1)
            if len(man_effects) != 1:
                continue
            if scalar_values_at_depth(man_effects[0], "white_peace", 1) != ["KOR"]:
                continue
            guarded_man_peaces.append(conditional)
        if len(guarded_man_peaces) != 1:
            raise ValueError(
                "Japan peace acceptance: expected one existing/warring MAN "
                f"white-peace guard, got {len(guarded_man_peaces)}"
            )
        man_war_trigger_count = len(
            re.findall(
                r"(?<![A-Za-z0-9_])has_war_with[ \t]*=[ \t]*KOR"
                r"(?![A-Za-z0-9_])",
                mask_comments(japan_peace),
            )
        )
        if man_war_trigger_count != 1:
            raise ValueError(
                "Japan peace acceptance: expected exactly one MAN-KOR war guard, "
                f"got {man_war_trigger_count}"
            )

        guarded_man_annexes: list[str] = []
        guarded_man_annex_conditionals: list[str] = []
        for conditional in assignment_blocks_at_depth(peace_accept, "if", 1):
            limits = assignment_blocks_at_depth(conditional, "limit", 1)
            if len(limits) != 1:
                continue
            man_guards = assignment_blocks_at_depth(limits[0], "MAN", 1)
            if len(man_guards) != 1:
                continue
            man_guard = man_guards[0]
            if scalar_values_at_depth(man_guard, "exists", 1) != ["yes"]:
                continue
            if scalar_values_at_depth(man_guard, "is_subject_of", 1) != ["JAP"]:
                continue
            japan_scopes = assignment_blocks_at_depth(conditional, "JAP", 1)
            if len(japan_scopes) != 1:
                continue
            annexes = assignment_blocks_at_depth(
                japan_scopes[0], "annex_country", 1
            )
            if len(annexes) != 1:
                continue
            annex = annexes[0]
            if scalar_values_at_depth(annex, "target", 1) != ["MAN"]:
                continue
            if scalar_values_at_depth(annex, "transfer_troops", 1) != ["yes"]:
                continue
            guarded_man_annexes.append(annex)
            guarded_man_annex_conditionals.append(conditional)
        if len(guarded_man_annexes) != 1:
            raise ValueError(
                "Japan peace acceptance: expected one MAN-exists/Japanese-subject "
                f"guarded annex, got {len(guarded_man_annexes)}"
            )
        unguarded_man_annexes = [
            annex
            for japan_scope in assignment_blocks_at_depth(peace_accept, "JAP", 1)
            for annex in assignment_blocks_at_depth(japan_scope, "annex_country", 1)
            if scalar_values_at_depth(annex, "target", 1) == ["MAN"]
        ]
        if unguarded_man_annexes:
            raise ValueError(
                "Japan peace acceptance: unguarded top-level JAP annex remains"
            )
        target_man_count = len(
            re.findall(
                r"(?<![A-Za-z0-9_])target[ \t]*=[ \t]*MAN(?![A-Za-z0-9_])",
                mask_comments(peace_accept),
            )
        )
        if target_man_count != 1:
            raise ValueError(
                "Japan peace acceptance: expected exactly one annex target MAN, "
                f"got {target_man_count}"
            )
        if peace_accept.find(guarded_man_peaces[0]) >= peace_accept.find(
            guarded_man_annex_conditionals[0]
        ):
            raise ValueError(
                "Japan peace acceptance: MAN white peace must precede guarded annex"
            )

        manschluss_request = unique_identified_block(
            events, "country_event", "kor_events.13", 0
        )
        manschluss_request_accept = unique_named_nested_block(
            manschluss_request,
            "option",
            "name",
            "kor_events.13.a",
            1,
            "Manschluss request",
        )
        manschluss_request_recipient = unique_nested_block(
            manschluss_request_accept, "KOR", 1, "Manschluss request acceptance"
        )
        require_nested_event_call(
            manschluss_request_recipient,
            "kor_events.14",
            "Manschluss request acceptance",
        )

        manschluss_accept = unique_identified_block(
            events, "country_event", "kor_events.14", 0
        )
        manschluss_option = unique_named_nested_block(
            manschluss_accept,
            "option",
            "name",
            "kor_events.14.a",
            1,
            "Manschluss acceptance",
        )
        manschluss_recipient = unique_nested_block(
            manschluss_option, "KOR", 1, "Manschluss acceptance"
        )

        gookppong = unique_assignment_block(on_actions, "on_actions", 0)
        startup = unique_nested_block(gookppong, "on_startup", 1, "Gookppong")
        startup_effect = unique_nested_block(startup, "effect", 1, "Gookppong startup")
        enabled_branch = unique_nested_block(
            startup_effect, "if", 1, "Gookppong startup"
        )
        enabled_limit = unique_nested_block(
            enabled_branch, "limit", 1, "Gookppong startup"
        )
        enabled_rule = unique_nested_block(
            enabled_limit, "has_game_rule", 1, "Gookppong startup"
        )
        if scalar_values_at_depth(enabled_rule, "rule", 1) != ["kor_gookppong_status"]:
            raise ValueError("Gookppong startup: unexpected game-rule key")
        if scalar_values_at_depth(enabled_rule, "option", 1) != ["GOOKPPONG_ENABLED"]:
            raise ValueError("Gookppong startup: unexpected game-rule option")
        gookppong_kor_blocks = [
            candidate
            for candidate in assignment_blocks_at_depth(enabled_branch, "KOR", 1)
            if numeric_values_at_depth(candidate, "transfer_state", 1)
        ]
        if len(gookppong_kor_blocks) != 1:
            raise ValueError(
                "Gookppong startup: expected one transferring KOR block, "
                f"got {len(gookppong_kor_blocks)}"
            )
        gookppong_kor = gookppong_kor_blocks[0]
        japan_cleanup = unique_nested_block(
            enabled_branch, "JAP", 1, "Gookppong startup"
        )
        man_cleanup = unique_nested_block(
            enabled_branch, "MAN", 1, "Gookppong startup"
        )

        multiethnic = unique_identified_block(
            focuses, "focus", "KOR_multiethnic_embrace", 1
        )
        multiethnic_reward = unique_nested_block(
            multiethnic, "completion_reward", 1, "Multiethnic embrace"
        )
        korean_dream = unique_identified_block(
            focuses, "focus", "KOR_korean_dream", 1
        )
        korean_dream_reward = unique_nested_block(
            korean_dream, "completion_reward", 1, "Korean dream"
        )
        teaching = unique_identified_block(
            focuses, "focus", "KOR_teaching_korean_to_manchurians", 1
        )
        teaching_reward = unique_nested_block(
            teaching, "completion_reward", 1, "Teaching Korean to Manchurians"
        )

        manschluss_focus = unique_identified_block(
            focuses, "focus", "KOR_manchulus", 1
        )
        manschluss_focus_reward = unique_nested_block(
            manschluss_focus, "completion_reward", 1, "Manschluss focus"
        )
        manschluss_focus_if = unique_nested_block(
            manschluss_focus_reward, "if", 1, "Manschluss focus"
        )
        manschluss_focus_japan = unique_nested_block(
            manschluss_focus_if, "JAP", 1, "Manschluss focus Japan branch"
        )
        require_nested_event_call(
            manschluss_focus_japan, "kor_events.13", "Manschluss focus Japan branch"
        )
        manschluss_focus_else = unique_nested_block(
            manschluss_focus_reward, "else", 1, "Manschluss focus"
        )
        manschluss_focus_man = unique_nested_block(
            manschluss_focus_else, "MAN", 1, "Manschluss focus Manchukuo branch"
        )
        require_nested_event_call(
            manschluss_focus_man,
            "kor_events.13",
            "Manschluss focus Manchukuo branch",
        )
    except (OSError, UnicodeError, ValueError) as exc:
        result.error(f"Manchuria acquisition coverage: cannot inspect reviewed blocks ({exc})")
        return

    checks = (
        (
            "Manchuria triumph control condition",
            numeric_values_at_depth(triumph_available, "controls_state", 1),
            ACQUISITION_CONTROL_STATE_IDS,
        ),
        (
            "Manchuria triumph transfer",
            numeric_values_at_depth(triumph_transfer, "transfer_state", 1),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Manchuria triumph Korean cores",
            matching_state_scopes(
                triumph_effect, scalars=(("add_core_of", ("ROOT",)),)
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Manchuria triumph separatism",
            matching_state_scopes(
                triumph_effect,
                nested_scalars=(
                    ("add_dynamic_modifier", "modifier", "chinese_separatism"),
                ),
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Defeat Japan control condition",
            numeric_values_at_depth(
                defeat_available, "has_full_control_of_state", 1
            ),
            ACQUISITION_CONTROL_STATE_IDS,
        ),
        (
            "Defeat Japan transfer tooltip",
            numeric_values_at_depth(defeat_tooltip, "transfer_state", 1),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Japan peace transfer",
            numeric_values_at_depth(peace_recipient, "transfer_state", 1),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Japan peace Manchukuo core removal",
            peace_man_core_states,
            MANCHURIA_STATE_IDS,
        ),
        (
            "Manschluss acceptance transfer",
            numeric_values_at_depth(manschluss_recipient, "transfer_state", 1),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Gookppong transfer",
            numeric_values_at_depth(gookppong_kor, "transfer_state", 1),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Gookppong Korean cores",
            matching_state_scopes(
                gookppong_kor, scalars=(("add_core_of", ("KOR",)),)
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Gookppong separatism",
            matching_state_scopes(
                gookppong_kor,
                nested_scalars=(
                    ("add_dynamic_modifier", "modifier", "chinese_separatism"),
                ),
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Gookppong Chinese core removal",
            matching_state_scopes(
                gookppong_kor,
                scalars=(("remove_core_of", ("MAN", "CHI", "PRC")),),
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Gookppong Japanese unit cleanup",
            delete_unit_state_values(japan_cleanup),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Gookppong Manchukuo unit cleanup",
            delete_unit_state_values(man_cleanup),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Multiethnic embrace strong separatism removal",
            matching_state_scopes(
                multiethnic_reward,
                nested_scalars=(
                    ("remove_dynamic_modifier", "modifier", "chinese_separatism"),
                ),
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Multiethnic embrace weakened separatism",
            matching_state_scopes(
                multiethnic_reward,
                nested_scalars=(
                    (
                        "add_dynamic_modifier",
                        "modifier",
                        "weakened_chinese_separatism",
                    ),
                ),
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Korean dream weakened separatism removal",
            matching_state_scopes(
                korean_dream_reward,
                nested_scalars=(
                    (
                        "remove_dynamic_modifier",
                        "modifier",
                        "weakened_chinese_separatism",
                    ),
                ),
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Teaching Korean strong separatism removal",
            matching_state_scopes(
                teaching_reward,
                nested_scalars=(
                    ("remove_dynamic_modifier", "modifier", "chinese_separatism"),
                ),
            ),
            MANCHURIA_STATE_IDS,
        ),
        (
            "Teaching Korean weakened separatism",
            matching_state_scopes(
                teaching_reward,
                nested_scalars=(
                    (
                        "add_dynamic_modifier",
                        "modifier",
                        "weakened_chinese_separatism",
                    ),
                ),
            ),
            MANCHURIA_STATE_IDS,
        ),
    )
    for label, values, expected in checks:
        require_state_set(result, label, values, expected)

    for path in iter_script_files():
        text = read_utf8(path)
        for state_id, name_key in state_scope_scalar_uses(text, "set_state_name"):
            if state_id not in RT56_MANCHURIA_SPLIT_STATE_IDS:
                continue
            result.error(
                f"{relative(path)}: state {state_id} must retain its RT56 name; "
                f"found set_state_name={name_key}"
            )

    invented_key = re.compile(
        r"(?m)^[ \t]*STATE_KR_(?:941|942|943|944|945|946|947)"
        r"[A-Za-z0-9_]*[ \t]*:"
    )
    host_key_override = re.compile(
        r"(?m)^[ \t]*STATE_(?:941|942|943|944|945|946|947)[ \t]*:"
    )
    for path in sorted((ROOT / "localisation").rglob("*.yml")):
        text = read_utf8(path)
        for pattern in (invented_key, host_key_override):
            for match in pattern.finditer(text):
                result.error(
                    f"{relative(path)}:{line_number(text, match.start())}: "
                    "compat localisation must not replace an RT56 Manchuria split-state name"
                )

    if len(result.errors) == before:
        result.passed(
            "Manchuria acquisition paths: all 15 states have consistent transfer, "
            "control, core, separatism, and unit-cleanup coverage; wartime peace "
            "survives MAN subject loss, with state-scoped core cleanup, surviving-MAN "
            "white peace, and guarded surviving-subject annex; RT56 names retained"
        )


def check_manchuria_state_coverage(result: Validation) -> None:
    try:
        _check_manchuria_state_coverage(result)
    except (OSError, UnicodeError, ValueError) as exc:
        result.error(f"Manchuria acquisition coverage: inspection failed ({exc})")


def identified_blocks(
    path: Path, kinds: tuple[str, ...], allowed_depths: set[int]
) -> list[tuple[str, int]]:
    text = read_utf8(path)
    clean = mask_comments(text)
    depths = block_depth_at_line_starts(text)
    pattern = re.compile(
        rf"(?m)^[ \t]*(?:{'|'.join(map(re.escape, kinds))})[ \t]*=[ \t]*\{{"
    )
    found: list[tuple[str, int]] = []
    for match in pattern.finditer(clean):
        start = text.rfind("\n", 0, match.start()) + 1
        if depths.get(start) not in allowed_depths:
            continue
        opening = clean.find("{", match.start(), match.end())
        end = matching_brace(text, opening)
        block = text[opening:end]
        identifier = direct_scalar(block, "id", 1)
        if identifier:
            found.append((identifier, line_number(text, match.start())))
    return found


def direct_block_keys(path: Path, outer: str, target_depth: int) -> list[tuple[str, int]]:
    text = read_utf8(path)
    clean = mask_comments(text)
    outer_match = re.search(rf"(?m)^[ \t]*{re.escape(outer)}[ \t]*=[ \t]*\{{", clean)
    if not outer_match:
        return []
    opening = clean.find("{", outer_match.start(), outer_match.end())
    end = matching_brace(text, opening)
    block = text[opening:end]
    depths = block_depth_at_line_starts(block)
    assignment = re.compile(r"(?m)^[ \t]*([A-Za-z0-9_.:-]+)[ \t]*=[ \t]*\{")
    found: list[tuple[str, int]] = []
    for match in assignment.finditer(mask_comments(block)):
        start = block.rfind("\n", 0, match.start()) + 1
        if depths.get(start) == target_depth:
            absolute = opening + match.start()
            found.append((match.group(1), line_number(text, absolute)))
    return found


def top_level_block_keys(path: Path) -> list[tuple[str, int]]:
    text = read_utf8(path)
    clean = mask_comments(text)
    depths = block_depth_at_line_starts(text)
    assignment = re.compile(r"(?m)^[ \t]*([A-Za-z0-9_.:-]+)[ \t]*=[ \t]*\{")
    found: list[tuple[str, int]] = []
    for match in assignment.finditer(clean):
        start = text.rfind("\n", 0, match.start()) + 1
        if depths.get(start) == 0:
            found.append((match.group(1), line_number(text, match.start())))
    return found


def report_duplicates(
    result: Validation,
    label: str,
    registry: dict[str, list[tuple[str, int]]],
) -> None:
    for identifier, locations in sorted(registry.items()):
        if len(locations) < 2:
            continue
        rendered = ", ".join(f"{path}:{line}" for path, line in locations)
        result.error(f"duplicate {label} ID {identifier!r}: {rendered}")


def check_logical_ids(result: Validation) -> None:
    before = len(result.errors)

    states: dict[str, list[tuple[str, int]]] = defaultdict(list)
    actual_state_ids: set[int] = set()
    for path in sorted((ROOT / "history/states").glob("*.txt")):
        text = read_utf8(path)
        match = re.search(r"(?m)^[ \t]*id[ \t]*=[ \t]*([0-9]+)", text)
        if not match:
            result.error(f"{relative(path)}: missing state id")
            continue
        identifier = match.group(1)
        actual_state_ids.add(int(identifier))
        states[identifier].append((relative(path), line_number(text, match.start())))
    report_duplicates(result, "state", states)
    if actual_state_ids != EXPECTED_COMPAT_STATE_IDS:
        result.error(
            "history/states: unexpected compat state set; "
            f"missing={sorted(EXPECTED_COMPAT_STATE_IDS - actual_state_ids)} "
            f"extra={sorted(actual_state_ids - EXPECTED_COMPAT_STATE_IDS)}"
        )

    events: dict[str, list[tuple[str, int]]] = defaultdict(list)
    event_kinds = (
        "country_event",
        "news_event",
        "state_event",
        "unit_leader_event",
        "operative_leader_event",
        "border_war_event",
    )
    for path in sorted((ROOT / "events").glob("*.txt")):
        for identifier, line in identified_blocks(path, event_kinds, {0}):
            events[identifier].append((relative(path), line))
    report_duplicates(result, "event", events)

    focuses: dict[str, list[tuple[str, int]]] = defaultdict(list)
    focus_trees: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for path in sorted((ROOT / "common/national_focus").glob("*.txt")):
        for identifier, line in identified_blocks(path, ("focus", "shared_focus"), {0, 1}):
            focuses[identifier].append((relative(path), line))
        for identifier, line in identified_blocks(path, ("focus_tree",), {0}):
            focus_trees[identifier].append((relative(path), line))
    report_duplicates(result, "focus", focuses)
    report_duplicates(result, "focus tree", focus_trees)

    characters: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for path in sorted((ROOT / "common/characters").glob("*.txt")):
        for identifier, line in direct_block_keys(path, "characters", 1):
            characters[identifier].append((relative(path), line))
    report_duplicates(result, "character", characters)

    mios: dict[str, list[tuple[str, int]]] = defaultdict(list)
    mio_root = ROOT / "common/military_industrial_organization/organizations"
    for path in sorted(mio_root.glob("*.txt")):
        for identifier, line in top_level_block_keys(path):
            mios[identifier].append((relative(path), line))
    report_duplicates(result, "MIO", mios)

    achievements: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for path in sorted((ROOT / "common/achievements").glob("*.txt")):
        for identifier, line in top_level_block_keys(path):
            achievements[identifier].append((relative(path), line))
    report_duplicates(result, "achievement", achievements)

    if len(result.errors) == before:
        result.passed(
            "logical IDs: state/event/focus/tree/character/MIO/achievement uniqueness pass"
        )


def check_required_content(result: Validation) -> None:
    assertions = {
        "common/achievements/HoK_achievements.txt": ("unique_id = hok_rt56_achievements",),
        "common/characters/KOR.txt": (
            "KOR_syngman_rhee={",
            "KOR_yi_kang = {",
            "KOR_kim_il_sung = {",
            "KOR_yi_un={",
            "KOR_pak_hon_yong = {",
        ),
        "common/ai_strategy/r56_KOR.txt": ("KOR_Gu_Kim",),
        "common/military_industrial_organization/organizations/KOR_organization.txt": (
            "KOR_hanjin_air_organization = {",
            "original_tag = NKR",
            "controls_state = 525",
        ),
        "common/units/names_divisions/KOR_names_divisions.txt": ("KOR_MOT_01",),
        "history/countries/KOR - Korea.txt": (
            "RT56 globally activates transport_plane_equipment_1",
        ),
        "sound/r56_vo_Korean.asset": (
            "compressor =",
            'name = "kor_Positive_005"',
            "volume = 1.0",
        ),
        "gfx/entities/kor_planes.gfx": (
            'name = "hok_rt56_KOR_plane_light_mesh"',
            'name = "hok_rt56_KOR_plane_medium_mesh"',
            'name = "hok_rt56_KOR_plane_heavy_mesh"',
        ),
        "gfx/entities/_HoK_units_planes.asset": (
            'name = "hok_rt56_KOR_light_plane_entity"',
            'name = "hok_rt56_KOR_medium_plane_entity"',
            'name = "hok_rt56_KOR_heavy_plane_entity"',
            'name = "supply"',
        ),
        "gfx/interface/equipmentdesigner/graphic_db/00_hok_plane_icons.txt": (
            "hok_rt56_KOR_light_plane_entity",
            "hok_rt56_KOR_medium_plane_entity",
            "hok_rt56_KOR_heavy_plane_entity",
        ),
        "localisation/english/replace/HoK_countries_l_english.yml": (
            "PHI_free_democratic:",
            "PHI_free_democratic_DEF:",
            "PHI_free_democratic_ADJ:",
        ),
        "localisation/korean/replace/HoK_countries_l_korean.yml": (
            "PHI_free_democratic:",
            "PHI_free_democratic_DEF:",
            "PHI_free_democratic_ADJ:",
        ),
        "map/definition.csv": ("13535;", "13568;"),
    }
    before = len(result.errors)
    for relative_name, needles in assertions.items():
        path = ROOT / relative_name
        if not path.is_file():
            result.error(f"{relative_name}: required output missing")
            continue
        text = read_utf8(path)
        for needle in needles:
            if needle not in text:
                result.error(f"{relative_name}: required merged content missing: {needle!r}")
    if len(result.errors) == before:
        result.passed("required KOR merge assertions: present")


def main() -> int:
    result = Validation()
    run_generator_checks(result)
    check_script_structure(result)
    check_descriptor(result)
    check_banned_tokens(result)
    check_localisation(result)
    check_hok_event_assets_and_localisation(result)
    check_logical_ids(result)
    check_manchuria_state_coverage(result)
    check_required_content(result)

    print("STATIC PORT VALIDATION")
    for message in result.passes:
        print(f"PASS  {message}")
    for message in result.warnings:
        print(f"WARN  {message}")
    for message in result.errors:
        print(f"ERROR {message}")
    print(
        f"SUMMARY pass={len(result.passes)} warning={len(result.warnings)} "
        f"error={len(result.errors)}"
    )
    print(
        "RUNTIME NOT PROVEN: launcher discovery/load order, engine parse/load, main menu, "
        "new game, unpause, DLC paths, localisation UI, save compatibility, and multiplayer."
    )
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
