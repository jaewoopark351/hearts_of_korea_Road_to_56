#!/usr/bin/env python3
"""Replay the reviewed Korean state-split delta over existing port outputs.

The donor snapshots supply a delta, never a replacement for the compatibility
tree.  All untouched bytes, including earlier RT56/English integration, stay in
the caller's input.  This module does not write files or inspect the live donor.
"""

from __future__ import annotations

import difflib
import re
from typing import Callable


#20261107_kpopmodder: Apply only frozen state-split hunks after prior Korean port layers.
_CONTENT_PATHS = (
    "common/achievements/HoK_achievements.txt",
    "common/ai_strategy/KOR.txt",
    "common/decisions/HOK_KOR_industry_expansion.txt",
    "common/decisions/HOK_KOR_resource_prospecting.txt",
    "common/decisions/KOR_decision.txt",
    "common/national_focus/korea.txt",
    "common/on_actions/gookppong_middle_power_on_actions.txt",
    "common/on_actions/gookppong_on_actions.txt",
    "common/scripted_effects/HOK_KOR_research_network_effects.txt",
    "events/korea.txt",
    "history/units/KOR_1936_air_bba.txt",
    "history/units/KOR_1936_air_legacy.txt",
    "history/units/gookppong_middle_power_KOR_air_bba.txt",
    "history/units/gookppong_middle_power_KOR_air_legacy.txt",
    "localisation/english/HOK_KOR_industry_expansion_l_english.yml",
    "localisation/korean/HOK_KOR_industry_expansion_l_korean.yml",
)
_LOCALE_PATHS = (
    "localisation/english/HOK_KOR_state_split_l_english.yml",
    "localisation/korean/HOK_KOR_state_split_l_korean.yml",
)
_NUMBER = re.compile(r"(?<![A-Za-z0-9_.])-?\d+(?![A-Za-z0-9_.])")
_ROW = re.compile(r'(?m)^([ \t]*([A-Za-z0-9_]+):0 ")([^\r\n]*)("[ \t]*\n?)$')
_INDUSTRY_NOTE = "#20261107_kpopmodder: Name the successor receiving construction and retain whole-region ownership/control cancellation.\n"
_CANCELLATION = "Cancelled if ownership or full control of the state is lost, if no building slots remain or if Korea capitulates."
_ENGLISH_EDITS = {
    "HOK_KOR_pyeongan_industry_project_desc": (
        ("military factory in Pyeongan.", "military factory in South Pyeongan."),
        (_CANCELLATION, "Cancelled if ownership or full control of either North or South Pyeongan is lost, if no building slots remain in South Pyeongan or if Korea capitulates."),
    ),
    "HOK_KOR_chungcheong_industry_project_desc": (
        ("civilian factory in Chungcheong.", "civilian factory in South Chungcheong."),
        (_CANCELLATION, "Cancelled if ownership or full control of either North or South Chungcheong is lost, if no building slots remain in South Chungcheong or if Korea capitulates."),
    ),
    "HOK_KOR_gyeongsang_shipbuilding_project_desc": (
        ("Requires building space in the coastal state of Gyeongsang.", "Requires building space in coastal South Gyeongsang."),
        ("§G1§! dockyard.", "§G1§! dockyard in South Gyeongsang."),
        (_CANCELLATION, "Cancelled if ownership or full control of either North or South Gyeongsang is lost, if no building slots remain in South Gyeongsang or if Korea capitulates."),
    ),
}
_ENGLISH_NAMES = {
    "HOK_KOR_STATE_1030": ("경상북도", "North Gyeongsang"),
    "HOK_KOR_STATE_1086": ("경상남도", "South Gyeongsang"),
    "HOK_KOR_STATE_1031": ("충청남도", "South Chungcheong"),
    "HOK_KOR_STATE_1087": ("충청북도", "North Chungcheong"),
    "HOK_KOR_STATE_1082": ("전라북도", "North Jeolla"),
    "HOK_KOR_STATE_1088": ("전라남도", "South Jeolla"),
    "HOK_KOR_STATE_527": ("평안남도", "South Pyeongan"),
    "HOK_KOR_STATE_1089": ("평안북도", "North Pyeongan"),
    "HOK_KOR_STATE_1028": ("함경남도", "South Hamgyeong"),
    "HOK_KOR_STATE_1090": ("함경북도", "North Hamgyeong"),
    "HOK_KOR_STATE_1083": ("황해남도", "South Hwanghae"),
    "HOK_KOR_STATE_1091": ("황해북도", "North Hwanghae"),
}


def content_paths() -> tuple[str, ...]:
    return _CONTENT_PATHS


def locale_paths() -> tuple[str, ...]:
    return _LOCALE_PATHS


def _text(data: bytes) -> str:
    return data.decode("utf-8").replace("\r\n", "\n")


def _encode(text: str, template: bytes) -> bytes:
    newline = "\r\n" if b"\r\n" in template else "\n"
    return text.replace("\n", newline).encode("utf-8")


def _map_text(text: str, mapping: dict[int, int]) -> str:
    # Names such as HOK_KOR_STATE_1086 are stable logical IDs, not numeric scopes.
    return _NUMBER.sub(lambda m: str(mapping[int(m.group())]) if int(m.group()) in mapping else m.group(), text)


def _inputs(relative: str, before: bytes | None, after: bytes | None,
            mapping: dict[int, int] | None) -> tuple[bytes, bytes, dict[int, int]]:
    if before is None or after is None or mapping is None:
        from korean_state_split import read_before, read_after, state_mapping
        before = read_before(relative) if before is None else before
        after = read_after(relative) if after is None else after
        mapping = state_mapping() if mapping is None else mapping
    return before, after, mapping


def _apply_hunks(relative: str, data: bytes, before: bytes, after: bytes,
                 mapping: dict[int, int], reverse: bool) -> bytes:
    old = _map_text(_text(before), mapping)
    new = _map_text(_text(after), mapping)
    if reverse:
        old, new = new, old
    target = _text(data)
    old_lines, new_lines = old.splitlines(keepends=True), new.splitlines(keepends=True)
    edits = []
    for index, (tag, i, j, a, b) in enumerate(
            difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_opcodes(), 1):
        if tag == "equal":
            continue
        for context in (0, 1, 3, 6, 12, 24, 48, 96):
            left, right = max(0, i - context), min(len(old_lines), j + context)
            anchor = "".join(old_lines[left:right])
            if anchor and target.count(anchor) == 1:
                start = target.index(anchor) + len("".join(old_lines[left:i]))
                edits.append((start, start + len("".join(old_lines[i:j])),
                              "".join(new_lines[a:b])))
                break
        else:
            raise ValueError(f"state-split content hunk {relative} #{index}: no unique exact anchor")
    for start, end, replacement in sorted(edits, reverse=True):
        target = target[:start] + replacement + target[end:]
    return _encode(target, data)


def _english_industry(data: bytes, before: bytes, after: bytes, reverse: bool) -> bytes:
    previous_rows = {m.group(2): m.group(3) for m in _ROW.finditer(_text(before))}
    next_rows = {m.group(2): m.group(3) for m in _ROW.finditer(_text(after))}
    changed = {key for key in previous_rows.keys() | next_rows.keys()
               if previous_rows.get(key) != next_rows.get(key)}
    if changed != set(_ENGLISH_EDITS) or _INDUSTRY_NOTE not in _text(after):
        raise ValueError("unreviewed donor industry localisation delta")
    text = _text(data)
    if reverse:
        if text.count(_INDUSTRY_NOTE) != 1:
            raise ValueError("missing state-split English contributor note")
        text = text.replace(_INDUSTRY_NOTE, "", 1)
    else:
        if _INDUSTRY_NOTE in text:
            raise ValueError("state-split English contributor note already present")
        header, body = text.split("\n", 1)
        text = header + "\n" + _INDUSTRY_NOTE + body
    seen = set()

    def update(match: re.Match) -> str:
        key, value = match.group(2), match.group(3)
        if key not in _ENGLISH_EDITS:
            return match.group()
        if key in seen:
            raise ValueError(f"duplicate industry localisation key: {key}")
        seen.add(key)
        for old, new in _ENGLISH_EDITS[key]:
            if reverse:
                old, new = new, old
            if value.count(old) != 1:
                raise ValueError(f"unreviewed English industry fragment: {key}")
            value = value.replace(old, new, 1)
        return match.group(1) + value + match.group(4)

    text = _ROW.sub(update, text)
    if seen != set(_ENGLISH_EDITS):
        raise ValueError("incomplete English industry localisation keys")
    return _encode(text, data)


def apply_content(relative: str, data: bytes, *, before: bytes | None = None,
                  after: bytes | None = None,
                  mapping: dict[int, int] | None = None) -> bytes:
    """Apply selected donor changes over the already integrated port output."""
    if relative not in _CONTENT_PATHS:
        return data
    before, after, mapping = _inputs(relative, before, after, mapping)
    if relative == "localisation/english/HOK_KOR_industry_expansion_l_english.yml":
        return _english_industry(data, before, after, False)
    return _apply_hunks(relative, data, before, after, mapping, False)


def remove_content(relative: str, data: bytes, *, before: bytes | None = None,
                   after: bytes | None = None,
                   mapping: dict[int, int] | None = None) -> bytes:
    """Recover the exact preceding port layer for historical lock checks."""
    if relative not in _CONTENT_PATHS:
        return data
    before, after, mapping = _inputs(relative, before, after, mapping)
    if relative == "localisation/english/HOK_KOR_industry_expansion_l_english.yml":
        return _english_industry(data, before, after, True)
    return _apply_hunks(relative, data, before, after, mapping, True)


def additions(*, read_after=None) -> dict[str, bytes]:
    """Return the two frozen HOK-specific state-name files, without writing."""
    if read_after is None:
        from korean_state_split import read_after
    outputs = {}
    for relative in _LOCALE_PATHS:
        source = read_after(relative)
        text = _text(source)
        rows = {m.group(2): m.group(3) for m in _ROW.finditer(text)}
        if rows != {key: names[0] for key, names in _ENGLISH_NAMES.items()}:
            raise ValueError(f"unreviewed state-split localisation: {relative}")
        if relative.startswith("localisation/english/"):
            text = _ROW.sub(lambda m: m.group(1) + _ENGLISH_NAMES[m.group(2)][1] + m.group(4), text)
        outputs[relative] = _encode(text, source)
    return outputs


#20261107_kpopmodder: Keep exact facility-location tooltips aligned with the two successor states used by the port.
_RESEARCH_LOCALE_PATHS = (
    "localisation/english/HOK_KOR_research_network_l_english.yml",
    "localisation/korean/HOK_KOR_research_network_l_korean.yml",
)
_RESEARCH_LOCALE_NOTE = (
    "#20261107_kpopmodder: Name the exact successor state preferred by each research facility.\n"
)
_RESEARCH_LOCALE_EDITS = {
    "HOK_KOR_naval_research_network_tt": ("$STATE_920$", "$HOK_KOR_STATE_1086$"),
    "HOK_KOR_nuclear_research_network_tt": ("$STATE_918$", "$HOK_KOR_STATE_1028$"),
}


def _research_locale_output(relative: str, data: bytes) -> bytes:
    if relative not in _RESEARCH_LOCALE_PATHS:
        raise ValueError(f"unreviewed research-location locale: {relative}")
    if not data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"research-location locale lost its UTF-8 BOM: {relative}")
    if b"\r\n" in data and b"\n" in data.replace(b"\r\n", b""):
        raise ValueError(f"mixed research-location locale line endings: {relative}")
    text = _text(data)
    locale = "english" if relative.startswith("localisation/english/") else "korean"
    header, separator, body = text.partition("\n")
    if not separator or header != f"\ufeffl_{locale}:":
        raise ValueError(f"research-location locale header changed: {relative}")
    if _RESEARCH_LOCALE_NOTE in text:
        raise ValueError(f"research-location locale update already applied: {relative}")
    seen: set[str] = set()

    def update(match: re.Match) -> str:
        key, value = match.group(2), match.group(3)
        if key not in _RESEARCH_LOCALE_EDITS:
            return match.group()
        if key in seen:
            raise ValueError(f"duplicate research-location tooltip: {relative}: {key}")
        seen.add(key)
        old, new = _RESEARCH_LOCALE_EDITS[key]
        if value.count(old) != 1 or new in value:
            raise ValueError(f"research-location tooltip source changed: {relative}: {key}")
        return match.group(1) + value.replace(old, new, 1) + match.group(4)

    body = _ROW.sub(update, body)
    if seen != set(_RESEARCH_LOCALE_EDITS):
        raise ValueError(f"incomplete research-location tooltip pair: {relative}")
    result = _encode(header + "\n" + _RESEARCH_LOCALE_NOTE + body, data)
    if result.replace(_encode(_RESEARCH_LOCALE_NOTE, data), b"", 1).replace(
            b"$HOK_KOR_STATE_1086$", b"$STATE_920$", 1).replace(
            b"$HOK_KOR_STATE_1028$", b"$STATE_918$", 1) != data:
        raise ValueError(f"research-location locale changed unrelated bytes: {relative}")
    return result


def port_localisation_outputs(read_compat_before: Callable[[str], bytes]) -> dict[str, bytes]:
    """Return the paired port-only presentation change without writing runtime files."""
    return {relative: _research_locale_output(relative, read_compat_before(relative))
            for relative in _RESEARCH_LOCALE_PATHS}


def remove_port_localisation(relative: str, data: bytes, *, before: bytes) -> bytes:
    """Recover exact frozen predecessor bytes after strict forward replay."""
    if _research_locale_output(relative, before) != data:
        raise ValueError(f"research-location locale output drift: {relative}")
    return before
