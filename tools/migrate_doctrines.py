#!/usr/bin/env python3
"""Migrate HOK country-history technologies to the pinned HOI4/RT56 schema.

The five outputs remain HOK-owned country histories.  Their doctrine-only
delta and KOR's retired transport-plane unlock cleanup are generated from the
pinned donor files and checked against current vanilla/RT56 definitions before
being written.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


COMPAT_ROOT = Path(__file__).resolve().parents[1]
# [2026-09-22]_kpopmodder: Use the reviewed donor snapshot, excluding unrelated updates.
from source_snapshot import HOK_ROOT
RT56_ROOT = Path(
    r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968"
)
VANILLA_ROOT = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
)

COUNTRY_FILES = (
    Path("history/countries/KOR - Korea.txt"),
    Path("history/countries/KCH - Korean China.txt"),
    Path("history/countries/KJP - Korean Japan.txt"),
    Path("history/countries/RKY - Ryukyu.txt"),
    Path("history/countries/TWN - Taiwan.txt"),
)

EXPECTED_SHA256 = {
    HOK_ROOT / "history/countries/KOR - Korea.txt":
        "5E31EA03F90C7FFF687627668EF893C8DCD4377442928078199E5A9E83C73DD0",
    HOK_ROOT / "history/countries/KCH - Korean China.txt":
        "930B15B3687BE9098E776BBBE87F9A28BB89CF099E68181E5A3ADF5A17AD69A8",
    HOK_ROOT / "history/countries/KJP - Korean Japan.txt":
        "34A0B87BF2247A66384CE2B4A1D984A6FD8D4499516D8F67985EA333606FA8D9",
    HOK_ROOT / "history/countries/RKY - Ryukyu.txt":
        "AB91A9FF26D892CACF92837D65CBEC096B31E3D288ED27B6500CECC5A5B5C230",
    HOK_ROOT / "history/countries/TWN - Taiwan.txt":
        "0E1C43295F72F039C2E54743189CAB007282DDC86BDE1ED3AC6FB24D3ADD6A8F",
    VANILLA_ROOT / "history/countries/GER - Germany.txt":
        "5E903C2B485B48D8BBA38ADBE0B6FD5CADC868DF4A575D526A1EF2DAC4AB66D7",
    RT56_ROOT / "history/countries/GER - Germany.txt":
        "563BBCD053E90E193DD30A9D1BF515609E2E260451E911AA81D3A1012F074101",
    VANILLA_ROOT / "common/doctrines/grand_doctrines/land_grand_doctrines.txt":
        "CD81A877366C582F096422320CD7FCF9FB259AFCC8D45D3DBB887B37792B329D",
    # [2026-09-22]_kpopmodder: Re-pin 1.19.3 reference; active new_convoy_raiding ID remains valid.
    VANILLA_ROOT / "common/doctrines/grand_doctrines/sea_grand_doctrines.txt":
        "110FDEAD1B621C4C54B54E58D9A78EF40A1EF4113A976FD3F6680E7A5BE0B5CF",
    VANILLA_ROOT / "common/doctrines/grand_doctrines/air_grand_doctrines.txt":
        "C06B6B1AD7C9B67D9F55B70FA9A26A9BA5830956D50EC94F33817755BAACE5A2",
    RT56_ROOT / "common/doctrines/subdoctrines/land/infantry_subdoctrines.txt":
        "CE92B913F15D9A0882B943E21FDD837BD08FACD7F1A9BD7D01AA7801DFA4972F",
    RT56_ROOT / "common/doctrines/subdoctrines/land/operations_subdoctrines.txt":
        "0A9E90E63A2EEE53326AB43A94D65FC5721FB5A6F0B6731894678130AF68AFBA",
    RT56_ROOT / "common/doctrines/subdoctrines/land/combat_support_subdoctrines.txt":
        "5804594751D9E256C628A364882ED2E4DB69C77717444F800D1CFD961B995F19",
    RT56_ROOT / "common/technologies/bba_air_techs.txt":
        "553D20A00D9BEA05C995D66438263AAA6ABB65121500C4D3FA9610A856309E57",
    RT56_ROOT / "common/technologies/air_techs.txt":
        "37E7575F4ED8380CD5D874AB133E073562868A5999F9C1B39D7A60375059A8A6",
    RT56_ROOT / "common/units/equipment/quad_engine_airframe.txt":
        "00F0B134D3CDB1EE451702A6213AF9ABF2E9AE6A6E204ABA2B332A231FA7FEA4",
    VANILLA_ROOT / "common/doctrines/subdoctrines/air/air_fighter_aircraft_subdoctrines.txt":
        "CDC9D22A4DC3DFD7501AB0A8253DDB9AE37CEFC5769C7D14727915C0A3B20BC8",
    VANILLA_ROOT / "common/doctrines/subdoctrines/air/air_strike_aircraft_subdoctrines.txt":
        "9B74B2BC87BE02798DB035FDF6C3AE107BA870007FB241E386A36CA50F6F815F",
}

MOBILE_ROOTS = (
    "set_grand_doctrine = new_mobile_warfare\n"
    "set_grand_doctrine = new_convoy_raiding\n"
    "set_grand_doctrine = new_battlefield_support"
)

KOR_ROOTS = (
    "set_grand_doctrine = superior_firepower\n"
    "set_grand_doctrine = new_convoy_raiding\n"
    "set_grand_doctrine = new_battlefield_support"
)

# This is the current vanilla GER 1939 conversion of the same legacy
# mobile-warfare / dive-bombing progression inherited by the four HOK tags.
MOBILE_1939_PROGRESS = (
    "\tset_grand_doctrine = new_mobile_warfare\n"
    "\tset_grand_doctrine = new_convoy_raiding\n"
    "\tset_grand_doctrine = new_battlefield_support\n"
    "\tset_sub_doctrine = mobile_infantry\n"
    "\tadd_mastery = {\n"
    "\t\tamount = 200\n"
    "\t\tsub_doctrine = mobile_infantry\n"
    "\t}\n"
    "\tset_sub_doctrine = mission_type_tactics\n"
    "\tadd_mastery = {\n"
    "\t\tamount = 100\n"
    "\t\tsub_doctrine = mission_type_tactics\n"
    "\t}\n"
    "\tset_sub_doctrine = mobile_recon_and_assault\n"
    "\tadd_mastery = {\n"
    "\t\tamount = 150\n"
    "\t\tsub_doctrine = mobile_recon_and_assault\n"
    "\t}\n"
    "\tset_sub_doctrine = air_subdoctrine_tactical_flexibility\n"
    "\tadd_mastery = {\n"
    "\t\tamount = 100\n"
    "\t\tsub_doctrine = air_subdoctrine_tactical_flexibility\n"
    "\t}\n"
    "\tset_sub_doctrine = air_subdoctrine_dive_bombers\n"
    "\tadd_mastery = {\n"
    "\t\tamount = 50\n"
    "\t\tsub_doctrine = air_subdoctrine_dive_bombers\n"
    "\t}"
)

LEGACY_TECH_IDS = {
    "superior_firepower",
    "mobile_warfare",
    "trade_interdiction",
    "formation_flying",
    "delay",
    "elastic_defence",
    "armored_spearhead",
    "schwerpunk",
    "blitzkrieg",
    "convoy_interdiction_ti",
    "unrestricted_submarine_warfare",
    "raider_patrols",
    "dive_bombing",
    "direct_ground_support",
}

RETIRED_RT56_TRANSPORT_TECH_IDS = {
    "bba_early_transport_plane",
    "early_transport_plane",
}

# The first port already generated KOR history with the doctrine migration.
# Only that exact prior output is a valid in-place input for this follow-up.
ACCEPTED_PRIOR_OUTPUT_SHA256 = {
    Path("history/countries/KOR - Korea.txt"):
        "C4FE10100779AFC9A28148A5105099A22A0016F1AB64DFF2AA063B214CA31813",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def verify_sources() -> None:
    errors = []
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            errors.append(f"missing source: {path}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(
                f"source drift: {path}\n  expected {expected}\n  actual   {actual}"
            )
    if errors:
        raise RuntimeError("\n".join(errors))


def normalized_source(path: Path) -> tuple[str, bool, str]:
    data = path.read_bytes()
    bom = data.startswith(b"\xef\xbb\xbf")
    text = (data[3:] if bom else data).decode("utf-8")
    if "\r" in text.replace("\r\n", ""):
        raise ValueError(f"unsupported lone CR in {path}")
    newline = "\r\n" if "\r\n" in text else "\n"
    return text.replace("\r\n", "\n"), bom, newline


def encode_like(text: str, bom: bool, newline: str) -> bytes:
    payload = text.replace("\n", newline).encode("utf-8")
    return (b"\xef\xbb\xbf" if bom else b"") + payload


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected one migration anchor, found {count}")
    return text.replace(old, new, 1)


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
    raise ValueError(f"unclosed block at offset {opening}")


def set_technology_blocks(text: str) -> list[str]:
    blocks = []
    pattern = re.compile(r"(?m)^[ \t]*set_technology[ \t]*=[ \t]*\{")
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        blocks.append(text[match.start():matching_brace(text, opening)])
    return blocks


def assert_no_legacy_doctrine_tech(text: str, label: Path) -> None:
    assignment = re.compile(
        r"(?m)^[ \t]*(" + "|".join(sorted(LEGACY_TECH_IDS)) + r")[ \t]*=[ \t]*1(?:[ \t]*#.*)?$"
    )
    for block in set_technology_blocks(text):
        match = assignment.search(block)
        if match:
            raise ValueError(
                f"{label}: legacy doctrine {match.group(1)!r} remains in set_technology"
            )


def assert_no_retired_transport_tech(text: str, label: Path) -> None:
    assignment = re.compile(
        r"(?m)^[ \t]*("
        + "|".join(sorted(RETIRED_RT56_TRANSPORT_TECH_IDS))
        + r")[ \t]*=[ \t]*1(?:[ \t]*#.*)?$"
    )
    for block in set_technology_blocks(text):
        match = assignment.search(block)
        if match:
            raise ValueError(
                f"{label}: retired RT56 technology {match.group(1)!r} remains "
                "in set_technology"
            )


def top_level_ids(path: Path) -> set[str]:
    text, _, _ = normalized_source(path)
    return set(re.findall(r"(?m)^([A-Za-z0-9_]+)[ \t]*=[ \t]*\{", text))


def active_block_ids(path: Path) -> set[str]:
    """Return uncommented block-assignment IDs at any indentation depth."""
    text, _, _ = normalized_source(path)
    return set(
        re.findall(r"(?m)^[ \t]*([A-Za-z0-9_]+)[ \t]*=[ \t]*\{", text)
    )


def verify_reference_contract() -> None:
    vanilla_ger, _, _ = normalized_source(
        VANILLA_ROOT / "history/countries/GER - Germany.txt"
    )
    rt56_ger, _, _ = normalized_source(
        RT56_ROOT / "history/countries/GER - Germany.txt"
    )
    if MOBILE_ROOTS not in vanilla_ger or MOBILE_1939_PROGRESS not in vanilla_ger:
        raise ValueError("vanilla GER doctrine migration example changed")
    if MOBILE_ROOTS not in rt56_ger:
        raise ValueError("RT56 GER grand-doctrine example changed")

    grand_sources = {
        "superior_firepower": VANILLA_ROOT / "common/doctrines/grand_doctrines/land_grand_doctrines.txt",
        "new_mobile_warfare": VANILLA_ROOT / "common/doctrines/grand_doctrines/land_grand_doctrines.txt",
        "new_convoy_raiding": VANILLA_ROOT / "common/doctrines/grand_doctrines/sea_grand_doctrines.txt",
        "new_battlefield_support": VANILLA_ROOT / "common/doctrines/grand_doctrines/air_grand_doctrines.txt",
    }
    sub_sources = {
        "mobile_infantry": RT56_ROOT / "common/doctrines/subdoctrines/land/infantry_subdoctrines.txt",
        "mission_type_tactics": RT56_ROOT / "common/doctrines/subdoctrines/land/operations_subdoctrines.txt",
        "mobile_recon_and_assault": RT56_ROOT / "common/doctrines/subdoctrines/land/combat_support_subdoctrines.txt",
        "air_subdoctrine_tactical_flexibility": VANILLA_ROOT / "common/doctrines/subdoctrines/air/air_fighter_aircraft_subdoctrines.txt",
        "air_subdoctrine_dive_bombers": VANILLA_ROOT / "common/doctrines/subdoctrines/air/air_strike_aircraft_subdoctrines.txt",
    }
    for identifier, path in {**grand_sources, **sub_sources}.items():
        if identifier not in top_level_ids(path):
            raise ValueError(f"doctrine ID {identifier!r} missing from {path}")

    for identifier, path in {
        "bba_early_transport_plane": RT56_ROOT / "common/technologies/bba_air_techs.txt",
        "early_transport_plane": RT56_ROOT / "common/technologies/air_techs.txt",
    }.items():
        if identifier in active_block_ids(path):
            raise ValueError(f"retired transport technology {identifier!r} is active in {path}")

    equipment_path = RT56_ROOT / "common/units/equipment/quad_engine_airframe.txt"
    equipment_text, _, _ = normalized_source(equipment_path)
    match = re.search(
        r"(?m)^[ \t]*transport_plane_equipment_1[ \t]*=[ \t]*\{",
        equipment_text,
    )
    if not match:
        raise ValueError(f"transport_plane_equipment_1 missing from {equipment_path}")
    opening = equipment_text.find("{", match.start(), match.end())
    block = equipment_text[match.start():matching_brace(equipment_text, opening)]
    if not re.search(r"(?m)^[ \t]*active[ \t]*=[ \t]*yes(?:[ \t]*#.*)?$", block):
        raise ValueError("RT56 transport_plane_equipment_1 is no longer globally active")


def build_kor(source: Path) -> bytes:
    text, bom, newline = normalized_source(source)
    text = replace_once(
        text,
        '\nif = {\n\tlimit = { has_dlc = "By Blood Alone" }\n'
        '\t\tset_technology = {\n\t\t\taa_lmg = 1\n',
        '\n# RT56 globally activates transport_plane_equipment_1; its former unlock '\
        'technologies are not registered.\n'
        'if = {\n\tlimit = { has_dlc = "By Blood Alone" }\n'
        '\t\tset_technology = {\n\t\t\taa_lmg = 1\n',
        f"{source.name} RT56 transport-plane contract comment",
    )
    text = replace_once(
        text,
        "\t\t\tbba_early_transport_plane = 1\n",
        "",
        f"{source.name} retired BBA transport technology",
    )
    text = replace_once(
        text,
        "\t\t\tearly_transport_plane = 1\n",
        "",
        f"{source.name} retired legacy transport technology",
    )
    old = (
        "\tfuel_silos = 1\n"
        "\t\n"
        "\t#doctrines#\n"
        "\tsuperior_firepower = 1\n"
        "\ttrade_interdiction = 1\n"
        "\tformation_flying = 1\n"
        "}\n"
    )
    new = "\tfuel_silos = 1\n}\n\n" + KOR_ROOTS + "\n"
    text = replace_once(text, old, new, source.name)
    assert_no_legacy_doctrine_tech(text, source.relative_to(HOK_ROOT))
    assert_no_retired_transport_tech(text, source.relative_to(HOK_ROOT))
    return encode_like(text, bom, newline)


def build_mobile_country(source: Path) -> bytes:
    text, bom, newline = normalized_source(source)
    old_roots = (
        "\tinterwar_antiair = 1\n"
        "\tmobile_warfare = 1\n"
        "\ttrade_interdiction = 1\n"
        "\tformation_flying = 1\n"
        "\tfuel_silos = 1"
    )
    text = replace_once(
        text,
        old_roots,
        "\tinterwar_antiair = 1\n\tfuel_silos = 1",
        f"{source.name} 1936 doctrine technologies",
    )
    text = replace_once(
        text,
        "\tfuel_refining = 1\n}\nif = {",
        "\tfuel_refining = 1\n}\n\n" + MOBILE_ROOTS + "\nif = {",
        f"{source.name} 1936 grand doctrines",
    )

    legacy_progress = (
        "\t\t#doctrines\n"
        "\t\tdelay = 1\n"
        "\t\telastic_defence = 1\n"
        "\t\tarmored_spearhead = 1\n"
        "\t\tschwerpunk = 1\n"
        "\t\tblitzkrieg = 1\n"
        "\t\tconvoy_interdiction_ti = 1\n"
        "\t\tunrestricted_submarine_warfare = 1\n"
        "\t\traider_patrols = 1\n"
        "\t\t#air\n"
        "\t\tformation_flying = 1\t\t\n"
        "\t\tdive_bombing = 1\n"
        "\t\tdirect_ground_support = 1\n\n"
    )
    text = replace_once(
        text,
        legacy_progress,
        "",
        f"{source.name} 1939 doctrine technologies",
    )
    text = replace_once(
        text,
        "\t\tdispersed_industry4 = 1\n\n\t}\n}",
        "\t\tdispersed_industry4 = 1\n\n\t}\n\n" + MOBILE_1939_PROGRESS + "\n}",
        f"{source.name} 1939 doctrine progress",
    )
    assert_no_legacy_doctrine_tech(text, source.relative_to(HOK_ROOT))
    return encode_like(text, bom, newline)


def build_outputs() -> dict[Path, bytes]:
    verify_sources()
    verify_reference_contract()
    outputs = {}
    for relative in COUNTRY_FILES:
        source = HOK_ROOT / relative
        outputs[relative] = (
            build_kor(source) if relative.name.startswith("KOR ") else build_mobile_country(source)
        )
    return outputs


def apply(outputs: dict[Path, bytes]) -> None:
    for relative, expected in outputs.items():
        destination = (COMPAT_ROOT / relative).resolve()
        destination.relative_to(COMPAT_ROOT)
        source = HOK_ROOT / relative
        current = destination.read_bytes() if destination.is_file() else None
        if current == expected:
            print(f"unchanged: {relative}")
            continue
        if current is not None and current != source.read_bytes():
            accepted = ACCEPTED_PRIOR_OUTPUT_SHA256.get(relative)
            if accepted is None or hashlib.sha256(current).hexdigest().upper() != accepted:
                raise RuntimeError(f"refusing to overwrite independently changed file: {relative}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".doctrine.tmp")
        temporary.write_bytes(expected)
        temporary.replace(destination)
        print(f"wrote: {relative}")


def check(outputs: dict[Path, bytes]) -> bool:
    ok = True
    for relative, expected in outputs.items():
        destination = COMPAT_ROOT / relative
        if not destination.is_file():
            print(f"MISSING: {relative}")
            ok = False
        elif destination.read_bytes() != expected:
            print(f"MISMATCH: {relative}")
            ok = False
        else:
            print(f"OK: {relative}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.apply:
        apply(outputs)
        return 0
    return 0 if check(outputs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
