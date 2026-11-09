"""Independently check the bounded 2026-11-09 review follow-up.

Only standard-library code is used. No generator or transformation module is
imported, and historical projection accepts only the exact registered final
bytes after independently checking the permitted delta.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys


#20261109_kpopmodder: Check the narrow display and placement delta independently of its generators.
ROOT = Path(__file__).resolve().parents[1]
LOCK_RELATIVE = "tools/hok_review_followup_lock.json"
SNAPSHOT_RELATIVE = "docs/upstream/hok-review-followup-20261109"
EFFECTS = "common/scripted_effects/HOK_KOR_civic_effects.txt"
ENGLISH = "localisation/english/HOK_KOR_civic_state_l_english.yml"
KOREAN = "localisation/korean/HOK_KOR_civic_state_l_korean.yml"
BUILDINGS = "map/buildings.txt"
PATHS = frozenset((EFFECTS, ENGLISH, KOREAN, BUILDINGS))
BASE_COMMIT = "f8fdd821cf80dd291b02a59b55e8d85fe558a9b3"
REVISION = "2026-11-09-review-followup-v1"
MANIFEST = "1963361040482473746"
CHANGE_KEY = "HOK_KOR_chaebol_influence_change_tt"
CHANGE_VALUE = "$HOK_KOR_chaebol_influence$: $RIGHT|=0$"
EFFECT_NOTE = (
    "#20261109_kpopmodder: Display guarded legacy civic changes without changing "
    "values, order or once-only registration."
)
LOCALE_NOTE = (
    "#20261109_kpopmodder: Name the signed chaebol influence change without "
    "assigning a positive or negative policy judgement."
)
MAP_ROW = b"1153;floating_harbor;4725.00;9.50;1289.00;-4.47;10065\r\n"
_CHANGES = {
    "HOK_KOR_legacy_cooperation_adjustment": (
        ("HOK_KOR_chaebol_influence", "10", CHANGE_KEY),
        ("HOK_KOR_procurement_corruption", "5", "HOK_KOR_procurement_corruption_change_tt"),
        ("HOK_KOR_institutional_capture", "5", "HOK_KOR_institutional_capture_change_tt"),
    ),
    "HOK_KOR_legacy_taming_adjustment": (
        ("HOK_KOR_chaebol_influence", "-10", CHANGE_KEY),
        ("HOK_KOR_civic_influence", "5", "HOK_KOR_civic_influence_change_tt"),
        ("HOK_KOR_procurement_corruption", "-5", "HOK_KOR_procurement_corruption_change_tt"),
    ),
}
_LEXER = re.compile(
    rb'(?P<space>\s+)|(?P<comment>#[^\r\n]*)|'
    rb'(?P<string>"(?:\\.|[^"\\])*")|(?P<operator>[{}=<>!])|'
    rb'(?P<atom>[^\s{}=<>!"#]+)'
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def _name(relative: str | Path) -> str:
    name = str(relative).replace("\\", "/")
    return next((protected for protected in PATHS if protected.casefold() == name.casefold()), name)


def _load_lock() -> dict:
    config = json.loads((ROOT / LOCK_RELATIVE).read_text(encoding="utf-8"))
    _require(config.get("format") == 1 and config.get("revision") == REVISION,
             "unreviewed follow-up lock format or revision")
    _require(config.get("base_commit") == BASE_COMMIT,
             "unreviewed follow-up base commit")
    _require(str(config.get("workshop_manifest")) == MANIFEST,
             "unreviewed follow-up Workshop manifest")
    records = config.get("outputs", {})
    _require(set(records) == PATHS, "follow-up output allowlist changed")
    for name, record in records.items():
        _require(record.get("previous_snapshot") == "before/" + name,
                 f"follow-up ancestor path changed: {name}")
        for key in ("previous_sha256", "sha256"):
            _require(isinstance(record.get(key), str)
                     and re.fullmatch(r"[0-9A-F]{64}", record[key]) is not None,
                     f"invalid follow-up {key}: {name}")
        _require(record["previous_sha256"] != record["sha256"],
                 f"follow-up has no actual delta: {name}")
        _require(record.get("classification") in {
            "ADD", "USE_RT56", "THREE_WAY_MERGE", "OVERRIDE", "BINARY_MERGE", "ASSET_COPY"
        }, f"missing follow-up integration classification: {name}")
    return config


def _frozen_before(name: str, record: dict) -> bytes:
    snapshot = (ROOT / SNAPSHOT_RELATIVE).resolve()
    source = (snapshot / record["previous_snapshot"]).resolve()
    source.relative_to(snapshot)
    payload = source.read_bytes()
    _require(_sha(payload) == record["previous_sha256"],
             f"follow-up frozen ancestor hash mismatch: {name}")
    return payload


def _newline(payload: bytes) -> bytes:
    if b"\r\n" in payload:
        remainder = payload.replace(b"\r\n", b"")
        _require(b"\r" not in remainder and b"\n" not in remainder,
                 "mixed follow-up text line endings")
        return b"\r\n"
    _require(b"\r" not in payload, "unsupported follow-up text line ending")
    return b"\n"


def _tokens(payload: bytes) -> list[tuple[str, int, int]]:
    """Tokenise bytes without discarding quoted strings or their escapes."""
    tokens = []
    position = 3 if payload.startswith(b"\xef\xbb\xbf") else 0
    while position < len(payload):
        match = _LEXER.match(payload, position)
        _require(match is not None, f"unreadable script token at byte {position}")
        assert match is not None
        if match.lastgroup not in {"space", "comment"}:
            tokens.append((match.group().decode("utf-8"), match.start(), match.end()))
        position = match.end()
    return tokens


def _closing(tokens: list[tuple[str, int, int]], opening: int) -> int:
    _require(tokens[opening][0] == "{", "script block lacks opening brace")
    depth = 0
    for index in range(opening, len(tokens)):
        token = tokens[index][0]
        if token == "{":
            depth += 1
        elif token == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unclosed script block")


def _helpers(tokens: list[tuple[str, int, int]]) -> dict[str, tuple[int, int]]:
    helpers = {}
    depth = 0
    for index, (token, _start, _end) in enumerate(tokens):
        if depth == 0 and token in _CHANGES:
            _require(token not in helpers and index + 2 < len(tokens)
                     and [item[0] for item in tokens[index + 1:index + 3]] == ["=", "{"],
                     f"missing or duplicated legacy helper: {token}")
            helpers[token] = (index + 3, _closing(tokens, index + 2))
        if token == "{":
            depth += 1
        elif token == "}":
            depth -= 1
            _require(depth >= 0, "unexpected script closing brace")
    _require(depth == 0 and set(helpers) == set(_CHANGES),
             "legacy civic helper inventory or script balance changed")
    return helpers


def _helper_commands(tokens: list[tuple[str, int, int]], bounds: tuple[int, int]) -> list[tuple[int, int]]:
    commands = []
    start, stop = bounds
    for index in range(start, stop):
        if tokens[index][0] != "add_to_variable":
            continue
        _require(index + 2 < stop
                 and [token[0] for token in tokens[index + 1:index + 3]] == ["=", "{"],
                 "unexpected legacy variable-effect syntax")
        closing = _closing(tokens, index + 2)
        _require(closing < stop, "variable effect escapes legacy helper")
        commands.append((index + 3, closing))
    return commands


def _check_effects(before: bytes, after: bytes) -> None:
    newline = _newline(before)
    _require(_newline(after) == newline, "legacy effect line endings changed")
    note = EFFECT_NOTE.encode("utf-8")
    note_line = b"\t\t" + note + newline
    _require(note not in before and after.count(note) == 2 and after.count(note_line) == 2,
             "legacy display repair must add exactly two prescribed helper notes")
    old_tokens, new_tokens = _tokens(before), _tokens(after)
    old_helpers, new_helpers = _helpers(old_tokens), _helpers(new_tokens)
    removals = []
    counts: Counter[str] = Counter()
    for helper, expected in _CHANGES.items():
        old_commands = _helper_commands(old_tokens, old_helpers[helper])
        new_commands = _helper_commands(new_tokens, new_helpers[helper])
        _require(len(old_commands) == len(new_commands) == 3,
                 f"legacy helper must keep its three effects: {helper}")
        helper_start, helper_stop = new_helpers[helper]
        helper_bytes = after[new_tokens[helper_start - 1][1]:new_tokens[helper_stop][2]]
        _require(helper_bytes.count(note_line) == 1
                 and note_line + b"\t\tadd_to_variable" in helper_bytes,
                 f"legacy helper note is outside its first variable effect: {helper}")
        for (old_start, old_stop), (new_start, new_stop), (variable, value, tooltip) in zip(
            old_commands, new_commands, expected
        ):
            _require([token[0] for token in old_tokens[old_start:old_stop]] == [variable, "=", value],
                     f"unreviewed legacy ancestor effect: {helper}/{variable}")
            _require([token[0] for token in new_tokens[new_start:new_stop]]
                     == [variable, "=", value, "tooltip", "=", tooltip],
                     f"legacy effect value, order or metadata changed: {helper}/{variable}")
            left = new_tokens[new_start + 2][2]
            right = new_tokens[new_start + 5][2]
            _require(after[left:right] == b" tooltip = " + tooltip.encode("utf-8"),
                     f"unreviewed tooltip metadata bytes: {helper}/{variable}")
            removals.append((left, right))
            counts[tooltip] += 1
    _require(counts == Counter({CHANGE_KEY: 2, "HOK_KOR_civic_influence_change_tt": 1,
                               "HOK_KOR_procurement_corruption_change_tt": 2,
                               "HOK_KOR_institutional_capture_change_tt": 1}),
             "legacy display metadata inventory changed")
    restored = after
    for start, stop in sorted(removals, reverse=True):
        restored = restored[:start] + restored[stop:]
    restored = restored.replace(note_line, b"")
    _require(restored == before, "legacy display repair changed bytes beyond six metadata fields and two notes")
    _require([token[0] for token in _tokens(restored)] == [token[0] for token in old_tokens],
             "legacy display repair changed ordered script tokens or quoted strings")


def _check_locale(name: str, before: bytes, after: bytes) -> None:
    newline = _newline(before)
    locale = "english" if name == ENGLISH else "korean"
    header = b"\xef\xbb\xbf" + ("l_" + locale + ":").encode("ascii") + newline
    _require(before.startswith(header) and after.startswith(header),
             f"follow-up localisation BOM/header changed: {name}")
    _require(before.endswith(newline) and _newline(after) == newline,
             f"follow-up localisation line endings changed: {name}")
    note = LOCALE_NOTE.encode("utf-8") + newline
    row = f' {CHANGE_KEY}:0 "{CHANGE_VALUE}"'.encode("utf-8") + newline
    _require(CHANGE_KEY.encode() not in before and LOCALE_NOTE.encode() not in before,
             f"follow-up locale ancestor already contains the new key/note: {name}")
    _require(after.count(CHANGE_KEY.encode()) == 1 and after.count(note) == 1
             and after[len(header):].startswith(note) and after.endswith(row),
             f"follow-up locale must add one neutral key and one header note: {name}")
    restored = header + after[len(header) + len(note):-len(row)]
    _require(restored == before,
             f"follow-up locale changed existing keys, values, comments or bytes: {name}")


def _check_map(before: bytes, after: bytes) -> None:
    _require(before.count(MAP_ROW) == 1 and before.count(b"1153;floating_harbor;") == 1,
             "follow-up map ancestor does not contain the unique reviewed placement")
    _require(b"1153;floating_harbor;" not in after,
             "follow-up map retains or replaces the inland placement")
    _require(before.replace(MAP_ROW, b"", 1) == after,
             "follow-up map changed rows or bytes beyond the one reviewed removal")


def verify_pair(name: str | Path, before: bytes, after: bytes) -> None:
    """Check the permitted delta independently, without consulting generators."""
    relative = _name(name)
    _require(relative in PATHS, f"unreviewed follow-up output: {relative}")
    if relative == EFFECTS:
        _check_effects(before, after)
    elif relative in {ENGLISH, KOREAN}:
        _check_locale(relative, before, after)
    else:
        _check_map(before, after)


def historical_bytes(relative: str | Path, payload: bytes) -> bytes:
    """Project only an exact independently checked final output to its ancestor.

    Unknown and already-ancestral bytes pass through unchanged so the calling
    historical gate retains its own strict mismatch handling.
    """
    name = _name(relative)
    if name not in PATHS or not (ROOT / LOCK_RELATIVE).is_file():
        return payload
    record = _load_lock()["outputs"][name]
    if _sha(payload) != record["sha256"]:
        return payload
    before = _frozen_before(name, record)
    verify_pair(name, before, payload)
    return before


def _check_current_geography() -> None:
    state = (ROOT / "history/states/1153-Hwanghaebuk.txt").read_bytes()
    tokens = _tokens(state)
    province_blocks = []
    for index, (token, _start, _end) in enumerate(tokens):
        if token == "provinces" and index + 2 < len(tokens):
            _require([item[0] for item in tokens[index + 1:index + 3]] == ["=", "{"],
                     "unexpected Hwanghaebuk province syntax")
            stop = _closing(tokens, index + 2)
            province_blocks.append([item[0] for item in tokens[index + 3:stop]])
    _require(province_blocks == [["7070", "10065", "11915", "13560"]],
             "reviewed Hwanghaebuk province membership changed")
    _require(sum([item[0] for item in tokens[index:index + 3]] == ["id", "=", "1153"]
                 for index in range(max(0, len(tokens) - 2))) == 1,
             "reviewed Hwanghaebuk state ID changed")
    required = {"7070", "10065", "11915", "13560"}
    rows: dict[str, list[bytes]] = {}
    for row in (ROOT / "map/definition.csv").read_bytes().splitlines():
        fields = row.split(b";")
        identifier = fields[0].decode("ascii")
        if identifier in required:
            _require(identifier not in rows, f"duplicate reviewed province definition: {identifier}")
            rows[identifier] = fields
    _require(set(rows) == required and all(len(fields) >= 6 and fields[4:6] == [b"land", b"false"]
                                         for fields in rows.values()),
             "reviewed Hwanghaebuk provinces are not all inland land provinces")


def verify_current() -> dict[str, int]:
    """Read and check the actual four outputs; do not write or launch anything."""
    config = _load_lock()
    for name, record in config["outputs"].items():
        before = _frozen_before(name, record)
        after = (ROOT / name).read_bytes()
        _require(_sha(after) == record["sha256"], f"follow-up current output hash mismatch: {name}")
        verify_pair(name, before, after)
    _check_current_geography()
    return {"outputs": 4, "guarded_metadata_fields": 6, "bilingual_key_pairs": 1, "removed_map_rows": 1}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    try:
        verify_current()
        print("PASS review follow-up: four exact outputs; six guarded display fields; one bilingual key; one placement row removed; source checks only")
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
