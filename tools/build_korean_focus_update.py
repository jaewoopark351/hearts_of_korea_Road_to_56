#!/usr/bin/env python3
"""Build only the pinned September 2026 HOK Korean focus update.

Keep the historical inputs intact and layer only the pinned be5fb40 Korean
second wave over their generated outputs. This builder never writes to the
donor or prepares its own inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from build_rt56_map import HOK_ROOT, PROVINCE_ID_MAP, REPO_ROOT, STATE_ID_MAP
from migrate_hok_ids import apply_post_migration_fixes, replace_tokens
from source_snapshot import (
    ICON_MANIFEST, icon_lock, read_icon_source, SECOND_WAVE_RUNTIME_PATHS,
    SECOND_WAVE_FOCUS_PATH, read_second_wave_source, second_wave_lock,
    policy_update_lock, read_policy_source,
)
from korean_second_wave_geography import apply_second_wave_geography, verify_geography_inputs, LOCALISATION_PATHS


# [2026-09-22]_kpopmodder: Pin the approved Korean update separately from the historical donor base.
FOCUS_COMMIT = "da815305e3ce00186a487b3a378bf8536ff59146"
AI_COMMIT = "118d7b53dfdbc120fcfe4b9d6792e66b2b519be7"
SOURCE_HASHES = {
    Path("common/decisions/HOK_KOR_democratic_expansion.txt"):
        "C798B0EB016CB22DA409C66E54FFDB65FE1860DA78C2B41C5889D334AC2AAD2B",
    Path("common/decisions/HOK_KOR_industry_expansion.txt"):
        "2872F4781FF6828E74902CAA10B107DF1B15EE3877717CEEAEED66B58D98E1C0",
    Path("common/decisions/categories/HOK_KOR_democratic_expansion.txt"):
        "0BD424CFADD58693EB6083F7CEF1E7F916E64EEFFD792CF762AAEF40FEB7C06E",
    Path("common/decisions/categories/HOK_KOR_industry_expansion.txt"):
        "140234E91FC12703F5263A80583EF5452B3D1B96E0B8C09931D4037B6225894D",
    Path("common/ideas/HOK_KOR_democratic_expansion.txt"):
        "B9AFBF64FFC29C83DDECE0B251A8C862190CDCD85E24435E42C65BB8ACDE3AFC",
    Path("common/ideas/HOK_KOR_industry_expansion.txt"):
        "067B1CB40D071A2962090C621F63A7E8DA12B9AB66043CF7AB0B79E7928E1828",
    Path("common/ideas/HOK_KOR_military_expansion.txt"):
        "FB2C18AC3BE0DEAAD30714B8F4624324B646F294D9094D35871DAC0E441D7578",
    Path("common/ideas/korea.txt"):
        "DE22B2B0F7733AE5BC5A1564D9BBA8F47AE439456F893E6238903AC8BE953254",
    Path("common/modifiers/HOK_KOR_democratic_expansion.txt"):
        "E91E6E987B2AE60597C805180B657112E3ADF2A4DB1C41BAF09275681B40A64B",
    Path("common/national_focus/korea.txt"):
        "49EC715410B6931E51A6ABB297F7BE17E85D75A1AF72F4A70155E7824A54F903",
    Path("events/HOK_KOR_democratic_expansion.txt"):
        "62264F2E2AAEC8A2826427BB3C5D64D04194DA840616C1E4A0DD6CBD489999DF",
    Path("localisation/english/HOK_KOR_democratic_expansion_l_english.yml"):
        "472FD3CF3D03C2F3A4B50146EB0BA751EB372E049D29715573B1F7E065C6E442",
    Path("localisation/english/HOK_KOR_expansion_navigation_l_english.yml"):
        "EBAEB4761AB88B5549F8892EA32B5A991C00B7F11E6306ED517174113E5A43B7",
    Path("localisation/english/HOK_KOR_industry_expansion_l_english.yml"):
        "0D88A0FB1B87A16AE4F16463929D7FA2A049E1237A18D02B716CE644FC94CB0B",
    Path("localisation/english/HOK_KOR_military_expansion_l_english.yml"):
        "F685247B25DD78F4A001B7277E22807D2A2719032D58E73EFEFE671BD49B2725",
    Path("localisation/korean/HOK_KOR_democratic_expansion_l_korean.yml"):
        "E409D69E52AA702A6A80CFE31BD23C354AA062B609492441FBD2B6F211F089F5",
    Path("localisation/korean/HOK_KOR_expansion_navigation_l_korean.yml"):
        "3385ECE1AA8169FFA6B44CAEDFAAD70E6DE5DDAEF3804847EED920404CD353BE",
    Path("localisation/korean/HOK_KOR_industry_expansion_l_korean.yml"):
        "9FABB9B080EAD1E6C7C35B6459A488360C9192EBBDFDF1135C9D9C03D1123F9E",
    Path("localisation/korean/HOK_KOR_military_expansion_l_korean.yml"):
        "73C8678935B6D09DBE6C82A306B790CB4CDB31656AD43BF243F26D33C66AA4E2",
    Path("common/ai_strategy_plans/KOR_historical_strategy_plan.txt"):
        "18C56A24FF5C93A944E58D71BB81AFFADC332601861D980EF243ACF028D2A3E8",
}
GAMEPLAY_PATHS = tuple(SOURCE_HASHES)
ICON_ASSET_PATHS = tuple(Path(relative) for relative in icon_lock()["runtime_assets"])
# [2026-09-23]_kpopmodder: Extend the reviewed allowlist without repinning unrelated historical generators.
OUTPUT_PATHS = tuple(dict.fromkeys(GAMEPLAY_PATHS + ICON_ASSET_PATHS + tuple(Path(p) for p in SECOND_WAVE_RUNTIME_PATHS)))
SOURCE_COMMITS = {
    relative: AI_COMMIT if relative.parts[1] == "ai_strategy_plans" else FOCUS_COMMIT
    for relative in GAMEPLAY_PATHS
}

# [2026-09-22]_kpopmodder: Refuse to overwrite any work beyond the three reviewed pre-update outputs.
ACCEPTED_PRIOR_OUTPUT_HASHES = {
    # [2026-09-22]_kpopmodder: Accept the reviewed generated tree before the independent-party reward update.
    Path("common/national_focus/korea.txt"):
        "1E14EBB08B466214967FEA0463A23D981716CE376A8A562172C979D299182F30",
    Path("common/ideas/korea.txt"):
        "BB53994155D4800B86AD260E32572D54A4FD8D21DEDBE97A8F05B6B8B40F0927",
    Path("common/ai_strategy_plans/KOR_historical_strategy_plan.txt"):
        "09AED7585E784FC4C87FA938862AF7DC053D7A2064C244F77AC2006E6561AC6D",
}
# [2026-09-22]_kpopmodder: Accept only the reviewed pre-artwork outputs, including the user's existing reward change.
ACCEPTED_PRIOR_OUTPUT_HASHES.update({
    Path(relative): digest for relative, digest in icon_lock()["prior_output_sha256"].items()
})
ACCEPTED_PRIOR_OUTPUT_HASHES.update({
    Path(relative): digest for relative, digest in second_wave_lock()["accepted_previous_outputs"].items()
})
# [2026-09-23]_kpopmodder: Permit only byte-identical imported regional text before adding the reviewed RT56 descriptions.
ACCEPTED_PRIOR_OUTPUT_HASHES.update({
    Path(relative): second_wave_lock()["runtime_text"][relative]["sha256"] for relative in LOCALISATION_PATHS
})
#20260923_kpopmodder: Accept only the ten reviewed pre-policy outputs, preserving unrelated user changes.
ACCEPTED_PRIOR_OUTPUT_HASHES.update({
    Path(relative): record["previous_output_sha256"]
    for relative, record in policy_update_lock()["runtime_text"].items()
})
PORT_NOTES = {
    Path("common/national_focus/korea.txt"):
        "# [2026-09-22]_kpopmodder: Preserve the approved RT56 map IDs and fifteen-state Manchurian integration in the updated HOK tree.",
    Path("common/decisions/HOK_KOR_industry_expansion.txt"):
        "# [2026-09-22]_kpopmodder: Use the approved RT56 Korean state IDs for project conditions, rewards, cancellation and highlighting.",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def verify_inputs() -> dict[Path, bytes]:
    """Read all approved inputs once and reject missing or drifted bytes."""
    inputs = {}
    errors = []
    for relative, expected in SOURCE_HASHES.items():
        source = HOK_ROOT / relative
        if not source.is_file():
            errors.append(f"missing pinned source: {source}")
            continue
        data = source.read_bytes()
        actual = sha256_bytes(data)
        if actual != expected:
            errors.append(
                f"source drift: {source}\n  expected {expected}\n  actual   {actual}"
            )
            continue
        if relative.suffix == ".yml":
            language = relative.parts[1]
            if not data.startswith(b"\xef\xbb\xbf" + f"l_{language}:".encode()):
                errors.append(f"unexpected localisation BOM/header: {relative}")
                continue
        inputs[relative] = data
    if errors:
        raise RuntimeError("\n".join(errors))
    return inputs


def add_port_note(data: bytes, note: str) -> bytes:
    """Add the migration note while preserving the source BOM and line ends."""
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    payload = data[len(bom):]
    newline = b"\r\n" if b"\r\n" in payload else b"\n"
    return bom + note.encode("utf-8") + newline + payload


def add_independent_party_reward(data: bytes) -> bytes:
    # [2026-09-22]_kpopmodder: Port only the reviewed reward from donor 698b6eb, retaining the pinned tree.
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    start = b"\tfocus = {" + newline + b"\t\tid = KOR_independent_party_in_power" + newline
    if data.count(start) != 1:
        raise ValueError("expected one independent-party focus")
    offset = data.index(start)
    end = data.index(newline + b"\t}" + newline, offset) + len(newline + b"\t}")
    focus = data[offset:end]
    tail = newline + b"\t\t}" + newline + b"\t}"
    if not focus.endswith(tail) or b"partial_economic_mobilisation" in focus:
        raise ValueError("independent-party reward no longer matches the reviewed source")
    reward = newline.join((
        b"",
        b"",
        b"\t\t\t# [2026-09-22]_kpopmodder: Grant partial mobilization without downgrading higher economy laws.",
        b"\t\t\tif = {",
        b"\t\t\t\tlimit = {",
        b"\t\t\t\t\tOR = {",
        b"\t\t\t\t\t\thas_idea = civilian_economy",
        b"\t\t\t\t\t\thas_idea = low_economic_mobilisation",
        b"\t\t\t\t\t}",
        b"\t\t\t\t}",
        b"\t\t\t\tadd_ideas = partial_economic_mobilisation",
        b"\t\t\t}",
    ))
    return data[:offset] + focus[:-len(tail)] + reward + tail + data[end:]


def apply_icon_references(relative: Path, data: bytes) -> bytes:
    # [2026-09-22]_kpopmodder: Apply only the reviewed artwork fields after all existing gameplay migrations.
    manifest = json.loads(read_icon_source(ICON_MANIFEST).decode("utf-8-sig"))
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    for group, field in (("focuses", "icon"), ("ideas", "picture")):
        for entry in manifest[group]:
            if entry["source_file"] != relative.as_posix():
                continue
            identifier = re.escape(entry["id"].encode())
            head = rb"id[ \t]*=[ \t]*" + identifier if group == "focuses" else identifier + rb"[ \t]*=[ \t]*\{"
            prefix_lines = rb"(?:[ \t]{3,}[^\r\n]*\r?\n)*?" if group == "ideas" else rb""
            pattern = rb"(?m)(^[ \t]*" + head + rb"[ \t]*\r?\n" + prefix_lines + rb")([ \t]*)" + field.encode() + rb"[ \t]*=[ \t]*" + re.escape(entry["previous_reference"].encode()) + rb"(?=[ \t]*\r?$)"
            match = re.search(pattern, data)
            if match is None or len(list(re.finditer(pattern, data))) != 1:
                raise ValueError(f"expected one original artwork field: {relative}/{entry['id']}")
            source = read_icon_source(relative)
            donor_pattern = rb"(?m)^[ \t]*" + head + rb"[ \t]*\r?\n" + prefix_lines + rb"(?:[ \t]*#[^\r\n]*\r?\n)*[ \t]*" + field.encode() + rb"[ \t]*=[ \t]*" + re.escape(entry["new_reference"].encode()) + rb"[ \t]*\r?$"
            if len(list(re.finditer(donor_pattern, source))) != 1:
                raise ValueError(f"reviewed donor reference missing: {relative}/{entry['id']}")
            replacement = (match[1] + match[2] + b"# [2026-09-22]_kpopmodder: Import the reviewed HOK policy icon." + newline
                           + match[2] + field.encode() + b" = " + entry["new_reference"].encode())
            data = data[:match.start()] + replacement + data[match.end():]
    return data


def build_all() -> dict[Path, bytes]:
    """Return deterministic relative-path outputs without writing any files."""
    inputs = verify_inputs()
    mapping = {**PROVINCE_ID_MAP, **STATE_ID_MAP}
    outputs = {}
    changed = set()
    for relative, original in inputs.items():
        migrated = replace_tokens(original, mapping)
        migrated = apply_post_migration_fixes(relative.as_posix(), migrated)
        if relative == Path("common/national_focus/korea.txt"):
            migrated = add_independent_party_reward(migrated)
        if migrated != original:
            changed.add(relative)
        if relative in PORT_NOTES:
            migrated = add_port_note(migrated, PORT_NOTES[relative])
        outputs[relative] = apply_icon_references(relative, migrated)
    # [2026-09-22]_kpopmodder: Gameplay migrations remain confined to these two files; artwork is checked separately.
    if changed != set(PORT_NOTES):
        unexpected = sorted(path.as_posix() for path in changed ^ set(PORT_NOTES))
        raise ValueError(f"unexpected Korean update transformation coverage: {unexpected}")
    for relative in ICON_ASSET_PATHS:
        outputs[relative] = read_icon_source(relative)
    # [2026-09-23]_kpopmodder: The latest tree already contains its icons and guarded partial-mobilisation reward.
    verify_geography_inputs()
    for name in SECOND_WAVE_RUNTIME_PATHS:
        relative = Path(name)
        original = read_second_wave_source(relative)
        migrated = original
        if relative.suffix == ".txt":
            migrated = replace_tokens(original, mapping)
            migrated = apply_post_migration_fixes(name, migrated)
        migrated = apply_second_wave_geography(name, migrated)
        if name == SECOND_WAVE_FOCUS_PATH:
            migrated = add_port_note(migrated, "# [2026-09-23]_kpopmodder: Merge pinned HOK second-wave content with RT56 IDs, legacy Manchuria integration and ADR-0005 regional conditions.")
        if relative.suffix == ".gfx":
            # Shared shine remains supplied by vanilla; all HOK-owned masks/payloads stay local.
            migrated = migrated.replace(b"gfx/interface/goals/HOK_KOR/shine_overlay.dds", b"gfx/interface/goals/shine_overlay.dds")
        if relative.suffix == ".yml" and not migrated.startswith(b"\xef\xbb\xbf" + f"l_{relative.parts[1]}:".encode()):
            raise ValueError(f"unexpected second-wave localisation BOM/header: {relative}")
        outputs[relative] = migrated
    #20260923_kpopmodder: Apply the PP-only projects and daily-PP reward after historical layers, retaining RT56 state migration.
    for name in policy_update_lock()["runtime_text"]:
        relative = Path(name)
        if relative not in outputs:
            raise ValueError(f"policy update cannot introduce an unreviewed output: {name}")
        migrated = read_policy_source(name)
        if relative.suffix == ".txt":
            migrated = apply_post_migration_fixes(name, replace_tokens(migrated, mapping))
        if relative in PORT_NOTES:
            migrated = add_port_note(migrated, PORT_NOTES[relative])
        if name == "common/ideas/HOK_KOR_democratic_expansion.txt":
            #20260923_kpopmodder: Retain the existing port's six icon contributor notes while updating only policy rewards.
            pattern = rb"(?m)^[ \t]*#[^\r\n]*\r?\n([ \t]*picture = HOK_KOR_[^\r\n]+)"
            prior_notes = {match[1]: match[0] for match in re.finditer(pattern, outputs[relative])}
            if len(prior_notes) != 6 or set(prior_notes) != {match[1] for match in re.finditer(pattern, migrated)}:
                raise ValueError("democratic policy icon comments no longer match the reviewed six references")
            migrated = re.sub(pattern, lambda match: prior_notes[match[1]], migrated)
        outputs[relative] = migrated
    verify_geography_inputs()
    verify_inputs()
    return outputs


def preflight(outputs: dict[Path, bytes]) -> None:
    if set(outputs) != set(OUTPUT_PATHS):
        raise ValueError("Korean update outputs must match the 400 reviewed historical and second-wave paths")
    errors = []
    for relative, expected in outputs.items():
        destination = (REPO_ROOT / relative).resolve()
        destination.relative_to(REPO_ROOT)
        temporary = destination.with_name(destination.name + ".hok-focus.tmp")
        if temporary.exists():
            errors.append(f"refusing to overwrite existing temporary file: {temporary}")
        if not destination.exists():
            continue
        if not destination.is_file():
            errors.append(f"output is not a regular file: {relative}")
            continue
        current = destination.read_bytes()
        if current == expected:
            continue
        accepted = ACCEPTED_PRIOR_OUTPUT_HASHES.get(relative)
        if accepted is None or sha256_bytes(current) != accepted:
            errors.append(f"refusing to overwrite independently changed file: {relative}")
    if errors:
        raise RuntimeError("\n".join(errors))


def apply(outputs: dict[Path, bytes]) -> None:
    preflight(outputs)
    verify_inputs()
    for relative, expected in outputs.items():
        destination = (REPO_ROOT / relative).resolve()
        destination.relative_to(REPO_ROOT)
        if destination.is_file() and destination.read_bytes() == expected:
            print(f"unchanged: {relative.as_posix()}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".hok-focus.tmp")
        with temporary.open("xb") as handle:
            handle.write(expected)
        temporary.replace(destination)
        print(f"wrote: {relative.as_posix()}")


def check(outputs: dict[Path, bytes]) -> bool:
    ok = True
    for relative, expected in outputs.items():
        destination = REPO_ROOT / relative
        if not destination.is_file():
            print(f"MISSING: {relative.as_posix()}")
            ok = False
        elif destination.read_bytes() != expected:
            print(f"MISMATCH: {relative.as_posix()}")
            ok = False
        else:
            print(f"OK: {relative.as_posix()}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare without writing outputs")
    args = parser.parse_args()
    try:
        outputs = build_all()
        if args.check:
            return 0 if check(outputs) else 1
        apply(outputs)
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
