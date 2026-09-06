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
    for forbidden in ("replace_path", "remote_file_id", "path="):
        if re.search(rf"(?m)^\s*{re.escape(forbidden)}", text):
            result.error(f"descriptor.mod: forbidden active field {forbidden}")
    if not any(error.startswith("descriptor.mod:") for error in result.errors):
        result.passed(
            "descriptor: RT56 + recorded Korean Language dependency; "
            "no path/replace_path/remote_file_id"
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
