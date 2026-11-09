"""Apply the bounded civic numeric-display repair to caller-supplied bytes.

This module has no filesystem, live-source or lock reads. Its caller owns exact
input/output fingerprints, output writes and the final-layer history contract.
"""

from __future__ import annotations


#20261109_kpopmodder: Expose only guarded legacy civic deltas while retaining their commands and saved-state lifecycle.
EFFECTS_PATH = "common/scripted_effects/HOK_KOR_civic_effects.txt"
LOCALE_PATHS = (
    "localisation/english/HOK_KOR_civic_state_l_english.yml",
    "localisation/korean/HOK_KOR_civic_state_l_korean.yml",
)
CIVIC_NUMERIC_PATHS = (EFFECTS_PATH, *LOCALE_PATHS)
CHAEBOL_CHANGE_KEY = "HOK_KOR_chaebol_influence_change_tt"
CHAEBOL_CHANGE_VALUE = "$HOK_KOR_chaebol_influence$: $RIGHT|=0$"
_NOTE = "#20261109_kpopmodder: Display guarded legacy civic changes without changing values, order or once-only registration."
_LOCALE_NOTE = "#20261109_kpopmodder: Name the signed chaebol influence change without assigning a positive or negative policy judgement."

_COOPERATION = """HOK_KOR_legacy_cooperation_adjustment = {
\tHOK_KOR_initialize_civic_system = yes
\tif = {
\t\tlimit = { tag = KOR NOT = { has_country_flag = HOK_KOR_legacy_cooperation_registered } }
\t\tadd_to_variable = { HOK_KOR_chaebol_influence = 10 }
\t\tadd_to_variable = { HOK_KOR_procurement_corruption = 5 }
\t\tadd_to_variable = { HOK_KOR_institutional_capture = 5 }
\t\tset_country_flag = HOK_KOR_legacy_cooperation_registered
\t\tHOK_KOR_sync_civic_state = yes
\t}
}"""
_TAMING = """HOK_KOR_legacy_taming_adjustment = {
\tHOK_KOR_initialize_civic_system = yes
\tif = {
\t\tlimit = { tag = KOR NOT = { has_country_flag = HOK_KOR_legacy_taming_registered } }
\t\tadd_to_variable = { HOK_KOR_chaebol_influence = -10 }
\t\tadd_to_variable = { HOK_KOR_civic_influence = 5 }
\t\tadd_to_variable = { HOK_KOR_procurement_corruption = -5 }
\t\tset_country_flag = HOK_KOR_legacy_taming_registered
\t\tHOK_KOR_sync_civic_state = yes
\t}
}"""
_HUNKS = (
    (_COOPERATION, (
        ("HOK_KOR_chaebol_influence", "10", CHAEBOL_CHANGE_KEY),
        ("HOK_KOR_procurement_corruption", "5", "HOK_KOR_procurement_corruption_change_tt"),
        ("HOK_KOR_institutional_capture", "5", "HOK_KOR_institutional_capture_change_tt"),
    )),
    (_TAMING, (
        ("HOK_KOR_chaebol_influence", "-10", CHAEBOL_CHANGE_KEY),
        ("HOK_KOR_civic_influence", "5", "HOK_KOR_civic_influence_change_tt"),
        ("HOK_KOR_procurement_corruption", "-5", "HOK_KOR_procurement_corruption_change_tt"),
    )),
)
_EXISTING_DISPLAY_VALUES = {
    "HOK_KOR_civic_influence_change_tt": "$HOK_KOR_civic_influence$: $RIGHT|+=0$",
    "HOK_KOR_institutional_capture_change_tt": "$HOK_KOR_institutional_capture$: $RIGHT|-=0$",
    "HOK_KOR_procurement_corruption_change_tt": "$HOK_KOR_procurement_corruption$: $RIGHT|-=0$",
}


def civic_numeric_paths() -> tuple[str, ...]:
    """Return the three paths owned by this display-only transformation."""
    return CIVIC_NUMERIC_PATHS


def _newline(data: bytes) -> bytes:
    if b"\r\n" in data:
        remainder = data.replace(b"\r\n", b"")
        if b"\r" in remainder or b"\n" in remainder:
            raise ValueError("mixed line endings in civic follow-up input")
        return b"\r\n"
    if b"\r" in data:
        raise ValueError("unsupported line ending in civic follow-up input")
    return b"\n"


def _effects(data: bytes, newline: bytes) -> bytes:
    if _NOTE.encode() in data:
        raise ValueError("legacy civic numeric display repair already present")
    result = data
    for before, changes in _HUNKS:
        after = before
        for variable, value, tooltip in changes:
            old = f"add_to_variable = {{ {variable} = {value} }}"
            new = f"add_to_variable = {{ {variable} = {value} tooltip = {tooltip} }}"
            if after.count(old) != 1:
                raise ValueError("legacy civic display hunk is not unique")
            after = after.replace(old, new, 1)
        after = after.replace("\t\tadd_to_variable", "\t\t" + _NOTE + "\n\t\tadd_to_variable", 1)
        old_bytes = before.replace("\n", newline.decode()).encode("utf-8")
        new_bytes = after.replace("\n", newline.decode()).encode("utf-8")
        if result.count(old_bytes) != 1:
            raise ValueError("legacy civic helper differs from the reviewed guarded input")
        result = result.replace(old_bytes, new_bytes, 1)
    return result


def _locale(relative: str, data: bytes, newline: bytes) -> bytes:
    locale = "english" if relative == LOCALE_PATHS[0] else "korean"
    header = b"\xef\xbb\xbf" + f"l_{locale}:".encode() + newline
    if not data.startswith(header) or not data.endswith(newline):
        raise ValueError("civic locale requires its existing BOM, header and final newline")
    if CHAEBOL_CHANGE_KEY.encode() in data or _LOCALE_NOTE.encode() in data:
        raise ValueError("chaebol numeric display localisation already present")
    for key, value in _EXISTING_DISPLAY_VALUES.items():
        row = f' {key}:0 "{value}"'.encode("utf-8") + newline
        if data.count(row) != 1:
            raise ValueError(f"reviewed civic numeric localisation differs: {key}")
    result = header + _LOCALE_NOTE.encode() + newline + data[len(header):]
    return result + f' {CHAEBOL_CHANGE_KEY}:0 "{CHAEBOL_CHANGE_VALUE}"'.encode("utf-8") + newline


def apply_civic_numeric(relative: str, data: bytes) -> bytes:
    """Add six metadata fields and one paired key; unknown paths are unchanged.

    Already-patched or structurally changed owned inputs fail closed. The outer
    registered layer must recognise its exact final bytes before calling again.
    """
    name = str(relative).replace("\\", "/")
    if name not in CIVIC_NUMERIC_PATHS:
        return data
    newline = _newline(data)
    if name == EFFECTS_PATH:
        return _effects(data, newline)
    return _locale(name, data, newline)


def apply_followup_content(relative: str, data: bytes) -> bytes:
    """Compose the currently approved content repair without speculative UI edits."""
    return apply_civic_numeric(relative, data)
