"""Build the selected CNDP update over already integrated RT56 port bytes.

The caller supplies a frozen donor runtime root and owns all writing, source
locks and host collision checks.  These functions never read the live donor or
write files.  Existing regional contracts retain their post-split port bytes.
"""

from __future__ import annotations

import re
import struct
from pathlib import Path
from typing import NamedTuple


#20261108_kpopmodder: Port independent CNDP projects without changing legacy contracts or RT56 world data.
COUNTRY_FLAG = "HOK_KOR_cndp_state_projects_v1"
SUCCESS_FLAG = "HOK_KOR_cndp_developed_v1"
FOCUS_ID = "KOR_comprehensive_national_development_plan"
DECISIONS = "common/decisions/KOR_decision.txt"
FOCUSES = "common/national_focus/korea.txt"
HISTORY = "history/countries/KOR - Korea.txt"
TRIGGERS = "common/scripted_triggers/HOK_KOR_cndp_triggers.txt"
GFX = "interface/HOK_KOR_cndp_icons.gfx"
REGIONS = (
    "jeollabuk", "jeollanam", "gyeongsangbuk", "gyeongsangnam",
    "chungcheongnam", "chungcheongbuk", "hwanghaenam", "hwanghaebuk",
    "pyeongannam", "pyeonganbuk", "hamgyeongnam", "hamgyeongbuk", "gangwon",
)
LEGACY_IDS = tuple("KOR_develop_" + region for region in (
    "jeolla", "gyeongsang", "chungcheong", "hwanghae", "pyeongan", "gangwon", "hamgyeong",
))
NEW_IDS = tuple("HOK_KOR_cndp_develop_" + region for region in REGIONS)
STATE_MAP = {
    527: 527, 1028: 918, 1029: 1144, 1030: 920, 1031: 1145,
    1082: 919, 1083: 917, 1086: 1148, 1087: 1149, 1088: 1150,
    1089: 1151, 1090: 1152, 1091: 1153,
}
PROVINCE_MAP = {source: source + 121 for source in range(13414, 13448)}
_STATES = (1082, 1088, 1030, 1086, 1031, 1087, 1083, 1091, 527, 1089, 1028, 1090, 1029)
_PROVINCES = ((13429,), (10110,), (7121,), (12060, 13435), (7204,),
              (13446,), (), (11915,), (9790,), (), (), (6944,), (1148,))
_TOKEN = re.compile(r'#[^\r\n]*|"(?:\\.|[^"\\])*"|[{}=<>]|[^\s{}=<>#"\ufeff]+')
_ROW = re.compile(r'(?m)^(?P<prefix>[ \t]*(?P<key>[A-Za-z0-9_]+):0 )"(?P<value>(?:\\.|[^"\\\r\n])*)"(?P<suffix>[ \t]*\r?)$')
_NOTE = "#20261108_kpopmodder: Integrate the independent CNDP projects with RT56 geography and English localisation."
_LEGACY_NOTE = "#20261108_kpopmodder: Keep original regional contracts exclusively for unversioned saves."
_HISTORY_NOTE = "#20261108_kpopmodder: Use independent CNDP projects in new games without migrating existing regional contracts."


class _Token(NamedTuple):
    value: str
    start: int
    end: int


class _Block(NamedTuple):
    start: int
    opening: int
    closing: int
    end: int


def _tokens(text: str) -> list[_Token]:
    return [_Token(m.group(), m.start(), m.end()) for m in _TOKEN.finditer(text)
            if not m.group().startswith("#")]


def _blocks(text: str, key: str) -> list[_Block]:
    tokens = _tokens(text)
    result = []
    for index, token in enumerate(tokens[:-2]):
        if token.value != key or [t.value for t in tokens[index + 1:index + 3]] != ["=", "{"]:
            continue
        depth = 0
        for closing in tokens[index + 2:]:
            depth += closing.value == "{"
            depth -= closing.value == "}"
            if depth == 0:
                result.append(_Block(token.start, tokens[index + 2].start, closing.start, closing.end))
                break
        else:
            raise ValueError(f"unclosed CNDP block: {key}")
    return result


def _one(text: str, key: str) -> _Block:
    matches = _blocks(text, key)
    if len(matches) != 1:
        raise ValueError(f"expected exactly one CNDP block {key}, found {len(matches)}")
    return matches[0]


def _focus(text: str) -> _Block:
    matches = [block for block in _blocks(text, "focus")
               if re.search(r"(?m)^\s*id\s*=\s*" + FOCUS_ID + r"\s*$", text[block.start:block.end])]
    if len(matches) != 1:
        raise ValueError("CNDP focus ID is missing or duplicated")
    return matches[0]


def _newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _lines_like(text: str, template: str) -> str:
    return text.replace("\r\n", "\n").replace("\n", _newline(template))


def _read(donor_root: Path, relative: str) -> bytes:
    return (Path(donor_root) / relative).read_bytes()


def _values(text: str, key: str) -> list[str]:
    tokens = _tokens(text)
    return [tokens[i + 2].value for i in range(len(tokens) - 2)
            if tokens[i].value == key and tokens[i + 1].value == "="]


def _map_geography(text: str) -> str:
    """Map numeric state scopes, highlight targets and province fields only."""
    tokens = _tokens(text)
    edits = []
    for index, token in enumerate(tokens):
        if not token.value.isdecimal():
            continue
        value = int(token.value)
        if index + 2 < len(tokens) and [t.value for t in tokens[index + 1:index + 3]] == ["=", "{"]:
            if value not in STATE_MAP:
                raise ValueError(f"unreviewed CNDP numeric state scope: {value}")
            mapped = STATE_MAP[value]
        elif index >= 2 and tokens[index - 1].value == "=" and tokens[index - 2].value in {"state", "province"}:
            mapping = STATE_MAP if tokens[index - 2].value == "state" else PROVINCE_MAP
            if tokens[index - 2].value == "state" and value not in mapping:
                raise ValueError(f"unreviewed CNDP highlighted state: {value}")
            mapped = mapping.get(value, value)
        else:
            continue
        if mapped != value:
            edits.append((token.start, token.end, str(mapped)))
    for start, end, replacement in reversed(edits):
        text = text[:start] + replacement + text[end:]
    # These donor notes name state scopes, not logical-ID suffixes or provinces.
    return re.sub(r"(?m)(^\s*#20261108_kpopmodder: Develop state )(\d+)( independently)",
                  lambda m: m[1] + str(STATE_MAP[int(m[2])]) + m[3], text)


def _source_project(text: str, region: str, state: int, provinces: tuple[int, ...]) -> str:
    key = "HOK_KOR_cndp_develop_" + region
    block = _one(text, key)
    start = text.rfind("\n", 0, block.start) + 1
    preceding = text.rfind("\n", 0, max(0, start - 1)) + 1
    if text[preceding:start].lstrip().startswith("#20261108_kpopmodder: Develop state "):
        start = preceding
    result = text[start:block.end]
    expected = {"cost": "150" if region == "gangwon" else "75",
                "days_remove": "180" if region == "gangwon" else "90",
                "civilian_factory_use": "5", "fire_only_once": "no",
                "tag": "KOR", "state": str(state)}
    if any(_values(result, name) != [value] for name, value in expected.items()):
        raise ValueError(f"unreviewed donor CNDP project contract: {region}")
    if tuple(map(int, _values(result, "province"))) != provinces:
        raise ValueError(f"unreviewed donor CNDP victory points: {region}")
    if _values(result, "set_state_flag") != [SUCCESS_FLAG]:
        raise ValueError(f"unreviewed donor CNDP completion flag: {region}")
    if any(name in _values(result, "type") for name in ("industrial_complex", "arms_factory", "dockyard")):
        raise ValueError(f"unexpected direct CNDP factory reward: {region}")
    return result


def _decisions(base: bytes, donor_root: Path) -> bytes:
    text = base.decode("utf-8")
    if COUNTRY_FLAG in text or any(_blocks(text, key) for key in NEW_IDS):
        raise ValueError("CNDP update already present or unexpected generation flag in base decisions")
    category = _one(text, "KOR_decision_CNDP_category")
    old = text[category.start:category.end]
    current = old
    edits = []
    for key in LEGACY_IDS:
        block = _one(old, key)
        original = old[block.start:block.end]
        visible = _one(original, "visible")
        body = original[visible.opening + 1:visible.closing]
        if [t.value for t in _tokens(body)] != ["has_completed_focus", "=", FOCUS_ID]:
            raise ValueError(f"unreviewed legacy CNDP visibility: {key}")
        at = block.start + visible.start
        line_start = old.rfind("\n", 0, at) + 1
        indent = old[line_start:at]
        if indent.strip():
            raise ValueError(f"legacy CNDP visible block is not on its own line: {key}")
        edits.append((line_start, line_start, indent + _LEGACY_NOTE + _newline(text)))
        insert = block.start + visible.closing
        edits.append((insert, insert, "NOT = { has_country_flag = " + COUNTRY_FLAG + " } "))
    for start, end, replacement in sorted(edits, reverse=True):
        current = current[:start] + replacement + current[end:]
    source = _read(donor_root, DECISIONS).decode("utf-8")
    projects = [_map_geography(_source_project(source, region, state, provinces))
                for region, state, provinces in zip(REGIONS, _STATES, _PROVINCES)]
    nl = _newline(text)
    insertion = nl + (nl + nl).join(_lines_like(project, text) for project in projects) + nl
    current = current[:-1] + insertion + current[-1:]
    return (text[:category.start] + current + text[category.end:]).encode("utf-8")


def _focuses(base: bytes, donor_root: Path) -> bytes:
    text = base.decode("utf-8")
    target = _focus(text)
    focus = text[target.start:target.end]
    reward = _one(focus, "completion_reward")
    actual = [t.value for t in _tokens(focus[reward.opening + 1:reward.closing])]
    expected = [value for key in LEGACY_IDS for value in ("unlock_decision_tooltip", "=", key)]
    if actual != expected:
        raise ValueError("CNDP base focus no longer contains exactly the seven legacy unlocks")
    source = _read(donor_root, FOCUSES).decode("utf-8")
    source_focus = _focus(source)
    donor = source[source_focus.start:source_focus.end]
    donor_reward = _one(donor, "completion_reward")
    replacement = donor[donor_reward.start:donor_reward.end]
    if _values(replacement, "unlock_decision_tooltip") != list(NEW_IDS) + list(LEGACY_IDS):
        raise ValueError("unreviewed donor CNDP focus unlock branches")
    replacement = _lines_like(replacement, text)
    start, end = target.start + reward.start, target.start + reward.end
    return (text[:start] + replacement + text[end:]).encode("utf-8")


def _history(base: bytes, donor_root: Path) -> bytes:
    text = base.decode("utf-8")
    if COUNTRY_FLAG in text:
        raise ValueError("CNDP new-game marker already present in base history")
    source = _read(donor_root, HISTORY).decode("utf-8")
    if _values(source, "set_country_flag").count(COUNTRY_FLAG) != 1:
        raise ValueError("donor CNDP new-game marker is missing or duplicated")
    matches = list(re.finditer(r"(?m)^\ufeff?capital[ \t]*=[ \t]*525[ \t]*\r?\n", text))
    if len(matches) != 1:
        raise ValueError("unexpected KOR initial capital anchor")
    position = matches[0].end()
    nl = _newline(text)
    addition = nl + _HISTORY_NOTE + nl + "set_country_flag = " + COUNTRY_FLAG + nl
    return (text[:position] + addition + text[position:]).encode("utf-8")


def apply_cndp(relative: str, base: bytes, donor_root: Path) -> bytes:
    """Apply the CNDP layer once; return unrelated paths byte-for-byte."""
    operation = {DECISIONS: _decisions, FOCUSES: _focuses, HISTORY: _history}.get(relative)
    return operation(base, donor_root) if operation else base


_NAMES = ("North Jeolla", "South Jeolla", "North Gyeongsang", "South Gyeongsang",
          "South Chungcheong", "North Chungcheong", "South Hwanghae", "North Hwanghae",
          "South Pyeongan", "North Pyeongan", "South Hamgyeong", "North Hamgyeong", "Gangwon")
_DESCRIPTIONS = (
    "Support the growth of Gunsan and inland centres to strengthen North Jeolla's development base.",
    "Support coastal centres, including Mokpo, to lay the foundations for South Jeolla's growth.",
    "Support industrial centres, including Pohang, to expand North Gyeongsang's development capacity.",
    "Promote development around Masan and Ulsan to support South Gyeongsang's growing towns.",
    "Support inland centres, including Jochiwon, to expand South Chungcheong's development capacity.",
    "Promote development around Cheongju to strengthen North Chungcheong's urban foundations.",
    "Expand development capacity around Haeju to support South Hwanghae's growth.",
    "Promote development around Sariwon to strengthen North Hwanghae's urban foundations.",
    "Support industrial centres, including Anju, to strengthen South Pyeongan's development base.",
    "Develop Unsan and industrial centres in the northern interior to expand North Pyeongan's development capacity.",
    "Support industrial growth around Hamhung to strengthen South Hamgyeong's development base.",
    "Support Najin and northern industrial centres to strengthen North Hamgyeong's development base.",
    "Support east-coast towns and inland resource centres to expand Gangwon's development capacity.",
)


def _localisation(donor_root: Path, language: str) -> bytes:
    relative = f"localisation/{language}/HOK_KOR_cndp_state_development_l_{language}.yml"
    raw = _read(donor_root, relative)
    if not raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"CNDP localisation lacks its BOM: {relative}")
    text = raw.decode("utf-8-sig")
    rows = list(_ROW.finditer(text))
    keys = [row["key"] for row in rows]
    expected = {"HOK_KOR_cndp_project_rules", "HOK_KOR_cndp_meaningful_space", SUCCESS_FLAG}
    expected.update(key + suffix for key in NEW_IDS for suffix in ("", "_desc"))
    if len(keys) != 29 or set(keys) != expected:
        raise ValueError(f"unexpected CNDP localisation key set: {relative}")
    if language == "english":
        translations = {
            "HOK_KOR_cndp_project_rules": "Cancelled projects can be restarted, but Political Power is not refunded. Completion rewards are granted once per state.",
            "HOK_KOR_cndp_meaningful_space": "There must be room to expand factory construction capacity.",
            SUCCESS_FLAG: "The state's national development project is complete",
        }
        for region, name, description in zip(REGIONS, _NAMES, _DESCRIPTIONS):
            key = "HOK_KOR_cndp_develop_" + region
            if region in {"hwanghaenam", "pyeonganbuk", "hamgyeongnam"}:
                description += " This project cannot begin unless additional capacity can be demonstrated within the factory construction limits."
            translations[key] = "Develop " + name
            translations[key + "_desc"] = description + "\\n\\n$HOK_KOR_cndp_project_rules$"
        text = _ROW.sub(lambda row: row["prefix"] + '"' + translations[row["key"]] + '"' + row["suffix"], text)
        if re.search(r"[\uac00-\ud7a3]", text):
            raise ValueError("untranslated Korean text in English CNDP output")
    header, body = text.split("\n", 1)
    text = header + "\n" + _NOTE + _newline(text) + body
    return b"\xef\xbb\xbf" + text.encode("utf-8")


def cndp_additions(donor_root: Path) -> dict[str, bytes]:
    """Return 17 source-derived new paths; write nothing and preserve DDS bytes."""
    trigger = _read(donor_root, TRIGGERS).decode("utf-8")
    for region in REGIONS:
        _one(trigger, "HOK_KOR_cndp_" + region + "_territory_trigger")
    additions = {TRIGGERS: _map_geography(trigger).encode("utf-8"), GFX: _read(donor_root, GFX)}
    for region in REGIONS:
        relative = f"gfx/interface/decisions/HOK_KOR/cndp/cndp_{region}.dds"
        data = _read(donor_root, relative)
        if len(data) != 4224 or data[:4] != b"DDS " or struct.unpack_from("<II", data, 12) != (32, 32):
            raise ValueError(f"unexpected CNDP DDS dimensions/length: {relative}")
        additions[relative] = data
    for language in ("english", "korean"):
        relative = f"localisation/{language}/HOK_KOR_cndp_state_development_l_{language}.yml"
        additions[relative] = _localisation(donor_root, language)
    return additions
