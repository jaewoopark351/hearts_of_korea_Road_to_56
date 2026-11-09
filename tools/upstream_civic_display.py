"""Replay the reviewed 2026-11-08 civic display delta over existing port bytes.

The caller supplies the frozen donor runtime root. This module never writes
runtime files, reads the live donor, or changes gameplay and saved identifiers.
"""

from __future__ import annotations

import difflib
import hashlib
from pathlib import Path
import re


#20261108_kpopmodder: Keep civic display metadata separate from prior gameplay and English integration layers.
_NUMERIC_NOTE = "#20261108_kpopmodder: Expose existing civic numeric conditions and effects without changing their execution."
_SYNC_NOTE = "#20261108_kpopmodder: Hide derived spirit synchronisation text while preserving the existing call and effect order."
_LOCALE_NOTE = "#20261108_kpopmodder: Name civic values and evidence while preserving all numeric conditions, effects and saved state."
_SCHOOL_NOTE = "#20261108_kpopmodder: Align descriptions with current recipient states and whole-region requirements; preserve rewards and lifecycle."
_CODE = {
    "common/decisions/HOK_KOR_civic_decisions.txt": (
        18, 11, "65958AB0D5CA22AAB617447E42AB29BB176ECEDEA4F54916E57FD2C5BAA93419",
        "5FD38E8F6B79BBEBCB5413E5C917854A4625C1AD7C3FBC038C1CA1A5209AA8CE"),
    "common/scripted_triggers/HOK_KOR_civic_triggers.txt": (
        1, 1, "9112E1395C0A0AF74B7663AA36CF1276D19CAAADD0319DB65C9FBC826FFDAA69",
        "DAFA368AA51AC8B674EE18A624888DF2B1C5981AA8BD662804C5B95D9A4D977E"),
    "events/HOK_KOR_civic_events.txt": (
        10, 6, "891DBD408AF6BEF80B4ABDB1A0325904A1992A15BE5E23452F51606A3B95D6BB",
        "C299AB32A34572B21570E233507DB1E2A3D8F8B660EE465C081CD12758A93A38"),
}
_VARIABLES = (
    "HOK_KOR_chaebol_influence", "HOK_KOR_civic_influence",
    "HOK_KOR_institutional_capture", "HOK_KOR_procurement_corruption",
)
_KEYS = _VARIABLES + ("HOK_KOR_prosecutor_defence_prepared",) + (
    "HOK_KOR_chaebol_influence_below_tt", "HOK_KOR_chaebol_influence_above_tt",
    "HOK_KOR_chaebol_influence_at_least_tt", "HOK_KOR_civic_influence_below_tt",
    "HOK_KOR_civic_influence_above_tt", "HOK_KOR_civic_influence_at_least_tt",
    "HOK_KOR_institutional_capture_below_tt", "HOK_KOR_civic_influence_change_tt",
    "HOK_KOR_institutional_capture_change_tt", "HOK_KOR_procurement_corruption_change_tt",
)
_ENGLISH = dict(zip(_KEYS[:5], (
    "Chaebol Influence", "Civil Society Influence", "Institutional Capture",
    "Procurement Corruption", "Evidence preservation completed",
)))
for _variable, _comparison in (
    (_VARIABLES[0], "below"), (_VARIABLES[0], "above"), (_VARIABLES[0], "at_least"),
    (_VARIABLES[1], "below"), (_VARIABLES[1], "above"), (_VARIABLES[1], "at_least"),
    (_VARIABLES[2], "below"),
):
    _words = _comparison.replace("_", " ")
    _ENGLISH[f"{_variable}_{_comparison}_tt"] = (
        f"${_variable}$ is {_words} §Y$RIGHT|0$§! (currently [?{_variable}|Y0])")
for _variable in _VARIABLES[1:]:
    _format = "+=0" if _variable == _VARIABLES[1] else "-=0"
    _ENGLISH[f"{_variable}_change_tt"] = f"${_variable}$: $RIGHT|{_format}$"
_STATE_LOCALES = tuple(
    f"localisation/{locale}/HOK_KOR_civic_state_l_{locale}.yml"
    for locale in ("english", "korean")
)
_SCHOOL_LOCALES = tuple(
    f"localisation/{locale}/HOK_KOR_democratic_expansion_l_{locale}.yml"
    for locale in ("english", "korean")
)
_SCHOOL_KEY = "HOK_KOR_technical_civic_schools_desc"
_SCHOOL_KOREAN_OLD = "기계의 눈금과 시민의 권리를 함께 가르치겠습니다.\\n경기·전라·충청의 소유·완전통제·부지가 필요합니다. 각 주에 슬롯·민간공장 2개씩, 전자공학 연구 25% 1회를 얻습니다."
_SCHOOL_ENGLISH_OLD = "We will teach people to read a machine's gauges and understand their rights as citizens.\\nRequires ownership, full control and construction space in Gyeonggi, Jeolla and Chungcheong. Each state receives two building slots and two civilian factories, alongside one 25% electronics research bonus."
_SCHOOL_ENGLISH_NEW = "We will teach people to read a machine's gauges and understand their rights as citizens.\\nRequires ownership and full control of Gyeonggi, both Jeolla states and both Chungcheong states. Gyeonggi, North Jeolla and South Chungcheong need building space; each gains two building slots and two civilian factories. Grants one 25% electronics research bonus."
_ROW = re.compile(r'^ ([A-Za-z0-9_.]+):0 "([^\r\n]*)"$', re.MULTILINE)
_METADATA = re.compile(r" tooltip = (HOK_KOR_[A-Za-z0-9_]+_tt)")
_SYNC = "hidden_effect = { HOK_KOR_sync_civic_state = yes }"
_RECOVERY_NOTE = "#20261109_kpopmodder: Hide recovery synchronisation expansion so the existing acknowledgement remains accessible."


def _hide_recovery_sync(text: str) -> str:
    """Wrap only the two confirmed overflowing recovery immediate calls."""
    pattern = re.compile(r"(?ms)(^country_event = \{\n\tid = HOK_KOR_CIVIC\.(3|13)\n.*?^\timmediate = \{\n)(.*?)(^\t\})")
    found = []

    def replace(match: re.Match[str]) -> str:
        body = match[3]
        call = "\t\tHOK_KOR_sync_civic_state = yes\n"
        if body.count(call) != 1 or "hidden_effect" in body:
            raise ValueError("recovery immediate sync differs from the reviewed single call")
        found.append(int(match[2]))
        replacement = "\t\t" + _RECOVERY_NOTE + "\n\t\t" + _SYNC + "\n"
        return match[1] + body.replace(call, replacement, 1) + match[4]

    result = pattern.sub(replace, text)
    if found != [3, 13]:
        raise ValueError("recovery event allowlist differs from .3/.13")
    return result


def civic_paths() -> tuple[str, ...]:
    return tuple(_CODE) + _STATE_LOCALES + _SCHOOL_LOCALES


def _text(data: bytes) -> str:
    return data.decode("utf-8").replace("\r\n", "\n")


def _encode(text: str, template: bytes) -> bytes:
    newline = "\r\n" if b"\r\n" in template else "\n"
    return text.replace("\n", newline).encode("utf-8")


def _rows(text: str) -> dict[str, str]:
    matches = _ROW.findall(text)
    result = dict(matches)
    if len(result) != len(matches):
        raise ValueError("duplicate civic localisation keys")
    return result


def _note(text: str, note: str, count: int) -> str:
    pattern = re.compile(r"(?m)^[ \t]*" + re.escape(note) + r"\n")
    text, removed = pattern.subn("", text)
    if removed != count:
        raise ValueError(f"civic source note count differs: {removed} != {count}")
    return text


def _before_code(relative: str, after: str) -> str:
    metadata_count, note_count, before_hash, after_hash = _CODE[relative]
    if hashlib.sha256(after.encode("utf-8")).hexdigest().upper() != after_hash:
        raise ValueError(f"unreviewed civic display source: {relative}")
    before = _note(after, _NUMERIC_NOTE, note_count)
    metadata = _METADATA.findall(before)
    if len(metadata) != metadata_count or not set(metadata) <= set(_KEYS[5:]):
        raise ValueError(f"unreviewed civic numeric metadata: {relative}")
    before = _METADATA.sub("", before)
    if relative == "events/HOK_KOR_civic_events.txt":
        events = re.split(r"(?m)(?=^country_event = \{\n)", after)
        found = {}
        for event in events:
            event_id = re.search(r"(?m)^\tid = HOK_KOR_CIVIC\.(\d+)$", event)
            if event_id and _SYNC in event:
                found[int(event_id[1])] = event.count(_SYNC)
        if found != {1: 1, 2: 3, 11: 1, 12: 3}:
            raise ValueError("civic sync wrappers extend beyond the eight reviewed calls")
        before = _note(before, _SYNC_NOTE, 8)
        before = before.replace(_SYNC, "HOK_KOR_sync_civic_state = yes")
    if hashlib.sha256(before.encode("utf-8")).hexdigest().upper() != before_hash:
        raise ValueError(f"civic donor changed outside the reviewed display delta: {relative}")
    return before


def _replay(target: str, before: str, after: str) -> str:
    old, new = before.splitlines(keepends=True), after.splitlines(keepends=True)
    edits = []
    for tag, i, j, a, b in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        for context in (0, 1, 3, 6, 12, 24, 48, 96):
            left, right = max(0, i - context), min(len(old), j + context)
            anchor = "".join(old[left:right])
            if anchor and target.count(anchor) == 1:
                start = target.index(anchor) + len("".join(old[left:i]))
                end = start + len("".join(old[i:j]))
                edits.append((start, end, "".join(new[a:b])))
                break
        else:
            raise ValueError("civic display delta has no unique unchanged port anchor")
    for (start, end, _), (next_start, _, _) in zip(edits, edits[1:]):
        if end > next_start:
            raise ValueError("overlapping civic display edits")
    for start, end, replacement in reversed(edits):
        target = target[:start] + replacement + target[end:]
    return target


def _locale_header(text: str, note: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or not re.fullmatch("\ufeffl_(?:english|korean):\n", lines[0]):
        raise ValueError("civic localisation requires its existing BOM and locale header")
    if note in text:
        raise ValueError("civic display note already present")
    lines.insert(1, note + "\n")
    return "".join(lines)


def _state_locale(relative: str, base: str, donor_root: Path) -> str:
    donor = _text((donor_root / relative).read_bytes())
    rows = _rows(donor)
    if not set(_KEYS) <= rows.keys() or set(_KEYS) & _rows(base).keys():
        raise ValueError("missing donor or already defined civic display keys")
    if not base.endswith("\n"):
        raise ValueError("civic localisation ancestor requires its existing final newline")
    values = _ENGLISH if relative in _STATE_LOCALES[:1] else rows
    #20261108_kpopmodder: Preserve the donor's substitution and numeric colour tokens in actual English text.
    for key in _KEYS[5:]:
        tokens = lambda value: re.findall(r"\$[^$]+\$|\[\?[^]]+\]|§.", value)
        if tokens(values[key]) != tokens(rows[key]):
            raise ValueError(f"civic display substitution tokens differ: {key}")
    result = _locale_header(base, _LOCALE_NOTE)
    result += "".join(f' {key}:0 "{values[key]}"\n' for key in _KEYS)
    return result


def _school_locale(relative: str, base: str, donor_root: Path) -> str:
    korean_relative = _SCHOOL_LOCALES[1]
    donor_value = _rows(_text((donor_root / korean_relative).read_bytes()))[_SCHOOL_KEY]
    if "경기·전라남북·충청남북" not in donor_value or "경기·전라북도·충청남도" not in donor_value:
        raise ValueError("unreviewed civic education region description")
    english = relative == _SCHOOL_LOCALES[0]
    old = _SCHOOL_ENGLISH_OLD if english else _SCHOOL_KOREAN_OLD
    new = _SCHOOL_ENGLISH_NEW if english else donor_value
    if _rows(base).get(_SCHOOL_KEY) != old:
        raise ValueError("civic education description differs from the reviewed port ancestor")
    old_line, new_line = (f' {_SCHOOL_KEY}:0 "{value}"' for value in (old, new))
    if base.count(old_line) != 1:
        raise ValueError("civic education description is not unique")
    return _locale_header(base.replace(old_line, new_line), _SCHOOL_NOTE)


def apply_civic_display(relative: str, base: bytes, donor_root: Path) -> bytes:
    """Apply only the reviewed civic UI delta; unrelated paths retain exact bytes."""
    relative = relative.replace("\\", "/")
    if relative not in civic_paths():
        return base
    text = _text(base)
    if relative in _CODE:
        after = _text((donor_root / relative).read_bytes())
        before = _before_code(relative, after)
        result = _replay(text, before, after)
        if _replay(result, after, before) != text:
            raise ValueError("civic display reversal did not preserve the caller's bytes")
        #20261109_kpopmodder: Keep the engine-confirmed recovery UI repair separate from immutable donor display bytes.
        if relative == "events/HOK_KOR_civic_events.txt":
            result = _hide_recovery_sync(result)
    elif relative in _STATE_LOCALES:
        result = _state_locale(relative, text, donor_root)
    else:
        result = _school_locale(relative, text, donor_root)
    return _encode(result, base)


def civic_additions(donor_root: Path) -> dict[str, bytes]:
    """The display delta adds keys to existing files, never new runtime paths."""
    return {}
