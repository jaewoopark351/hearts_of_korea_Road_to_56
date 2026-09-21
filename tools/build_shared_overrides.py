#!/usr/bin/env python3
"""Build audited HOK deltas for shared/global HOI4 databases.

The HOK donor and Road to 56/vanilla sources are immutable inputs.  This
builder deliberately emits only the HOK-owned records for accumulating
databases, and rebases unavoidable whole-file overrides on pinned current
host files.
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

EXPECTED_SHA256 = {
    HOK_ROOT / "common/countries/colors.txt":
        "D683D49FE16717D32004243D9A7DB10725BA048F4747F0BFB82769EC5CCED45A",
    HOK_ROOT / "common/countries/cosmetic.txt":
        "BB2D7E182094282A50E4E3F1A89EF65E88758D8CC5306251DFD9A729CABD74BC",
    HOK_ROOT / "common/names/00_names.txt":
        "1740DBAC9207B3711FC0D7F9EE5FCBCE2B9A27228BF88CA167AC149610B577AF",
    HOK_ROOT / "common/intelligence_agencies/00_intelligence_agencies.txt":
        "0F24DEF3E78CB521CC37F28D395645277441045D3126AD3CDBF033F3B0D3FBC4",
    HOK_ROOT / "common/difficulty_settings/00_difficulty.txt":
        "E5701B6EC59A5C4781BD596291C301A185088AC5F796DD99E840B7D2E972C401",
    HOK_ROOT / "common/military_industrial_organization/organizations/00_generic_organization.txt":
        "830D892C148A8DEDB894E37C72BF9A9ABFEBD1B41EDB504C74CF238E1B00A5E8",
    HOK_ROOT / "common/scripted_triggers/unit_medals_scripted_triggers.txt":
        "D2E0AED9A58F39B7883866B100C18975643DCB7283F0FDF122A1286D05BDEAD2",
    HOK_ROOT / "common/bookmarks/the_gathering_storm.txt":
        "A834B48B0791C82B4DE719639D6951D64EA45176478B76115AA4D7211ADF6DDE",
    HOK_ROOT / "common/scripted_effects/SP_scripted_effects.txt":
        "6F70BC269BB7F30166E51B337FCF675FC3523C004A91161E8AE7CB8EFFEBAD0B",
    HOK_ROOT / "history/general/generic_advisors.txt":
        "B20723056B2A3DD2D258ACC04D05E63B5A345F6562F2E9843C51ADDC6591B219",
    RT56_ROOT / "common/difficulty_settings/00_difficulty.txt":
        "3DBB427D97C056A6F78566D57078EF91D96AB2D941D65453EE195856485D34AF",
    # [2026-09-22]_kpopmodder: Rebase reviewed shared host updates while preserving existing KOR hooks.
    RT56_ROOT / "common/military_industrial_organization/organizations/00_generic_organization.txt":
        "C701A3CFF92AF46925932241E156B9B5F340FAEDCF228BB103F74B985F6F5D35",
    RT56_ROOT / "common/scripted_triggers/unit_medals_scripted_triggers.txt":
        "A103BF15A3BA3F4A0788A7C14F97A575307C28DFFCEFBC2EAEE1718070E503BB",
    RT56_ROOT / "common/bookmarks/the_gathering_storm.txt":
        "064C1ABB1475B8EBFD4E53CAB3D4DCE77CE37B4BE0A0A9EE6EA53988FB36F3B9",
    RT56_ROOT / "history/general/generic_advisors.txt":
        "4EA203FEF355255ABB28A7E59DCEDD3926C764D5CC4844C2B3D9B2269A65923C",
    # [2026-09-22]_kpopmodder: Pin the host character defining MAN's cross-country idea token.
    RT56_ROOT / "common/characters/KOR.txt":
        "979185140DA5A9CA57AC8399A47DA5EBFA9157C9FD2F2AACBD51E7E4E8C078CA",
    # [2026-09-22]_kpopmodder: Preserve all MAN content except the two unrecruited-KOR advisor checks.
    RT56_ROOT / "common/characters/MAN.txt":
        "CFE4943CF980417F047F90E920B1171E1ABBBF1647AEF1E7DC58AE37B7F53BF0",
    VANILLA_ROOT / "common/scripted_effects/SP_scripted_effects.txt":
        "4BC05E35FF893F6D5E2A54321A546416D8BA45777B7404A59A9C40B9083A510E",
    VANILLA_ROOT / "common/decisions/KOR.txt":
        "2B30A4D2B68D254D1123CFD40A0DA0BEC3219B026659621AD272F76006F050D0",
}

STALE_WHOLE_FILES = (
    Path("common/countries/colors.txt"),
    Path("common/countries/cosmetic.txt"),
    Path("common/names/00_names.txt"),
    Path("common/intelligence_agencies/00_intelligence_agencies.txt"),
    Path("common/difficulty_settings/00_difficulty.txt"),
)

KOR_SP_EFFECTS = (
    "SP_create_variant_based_on_country_assault_engineer",
    "SP_create_variant_based_on_country_armored_engineer",
    "SP_create_variant_based_on_country_armored_maintenance",
    "SP_create_variant_based_on_country_armored_signal",
)


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
            errors.append(f"source drift: {path}\n  expected {expected}\n  actual   {actual}")
    if errors:
        raise RuntimeError("\n".join(errors))


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig")


def newline_of(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def normalize_newlines(text: str, newline: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", newline)


def matching_brace(text: str, opening: int) -> int:
    if text[opening] != "{":
        raise ValueError(f"not an opening brace at {opening}")
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for index in range(opening, len(text)):
        char = text[index]
        if comment:
            if char in "\r\n":
                comment = False
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
                return index
            if depth < 0:
                break
    raise ValueError(f"unclosed block beginning at {opening}")


def validate_balanced(text: str, label: Path) -> None:
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        for char in line:
            if comment:
                if char in "\r\n":
                    comment = False
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
                if depth < 0:
                    raise ValueError(f"extra closing brace in {label} at line {line_number}")
    if quoted:
        raise ValueError(f"unterminated quote in {label}")
    if depth:
        raise ValueError(f"unbalanced braces in {label}: final depth {depth}")


def block_spans(text: str, key: str, *, top_level: bool) -> list[tuple[int, int]]:
    indent = "" if top_level else r"[ \t]*"
    pattern = re.compile(rf"(?m)^{indent}{re.escape(key)}\s*=\s*\{{")
    spans = []
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        closing = matching_brace(text, opening)
        spans.append((match.start(), closing + 1))
    return spans


def one_block(text: str, key: str, *, top_level: bool = True) -> str:
    spans = block_spans(text, key, top_level=top_level)
    if len(spans) != 1:
        raise ValueError(f"expected one {key!r} block, found {len(spans)}")
    start, end = spans[0]
    return text[start:end]


def generated_additive_file(source: Path, keys: tuple[str, ...], label: str) -> bytes:
    text = read_text(source)
    blocks = [one_block(text, key).rstrip() for key in keys]
    header = (
        f"# {label}\n"
        "# Generated by tools/build_shared_overrides.py from the pinned HOK donor.\n\n"
    )
    return (header + "\n\n".join(blocks) + "\n").encode("utf-8")


def build_intelligence_agency() -> bytes:
    source = read_text(HOK_ROOT / "common/intelligence_agencies/00_intelligence_agencies.txt")
    candidates = []
    for start, end in block_spans(source, "intelligence_agency", top_level=True):
        block = source[start:end]
        if re.search(r"default\s*=\s*\{\s*tag\s*=\s*KOR\s*\}", block):
            candidates.append(block.rstrip())
    if len(candidates) != 1:
        raise ValueError(f"expected one HOK KOR intelligence agency, found {len(candidates)}")
    result = (
        "# HOK-owned Korean intelligence agency.\n"
        "# Generated by tools/build_shared_overrides.py from the pinned HOK donor.\n\n"
        + candidates[0]
        + "\n"
    )
    return result.encode("utf-8")


def validate_rt56_difficulty_ownership() -> None:
    required = (
        'key = "custom_diff_strong_kor"',
        "modifier = diff_strong_ai_generic",
        "countries = { KOR }",
        "multiplier = 2.0",
    )
    for source in (
        HOK_ROOT / "common/difficulty_settings/00_difficulty.txt",
        RT56_ROOT / "common/difficulty_settings/00_difficulty.txt",
    ):
        text = read_text(source)
        matches = []
        for start, end in block_spans(text, "difficulty_setting", top_level=False):
            block = text[start:end]
            if 'key = "custom_diff_strong_kor"' in block:
                matches.append(block)
        if len(matches) != 1 or any(token not in matches[0] for token in required):
            raise ValueError(f"unexpected Korean difficulty definition in {source}")


def build_generic_mio() -> bytes:
    host_path = RT56_ROOT / "common/military_industrial_organization/organizations/00_generic_organization.txt"
    text = read_text(host_path)
    newline = newline_of(text)
    start, end = block_spans(text, "generic_tank_organization", top_level=True)[0]
    block = text[start:end]
    if "tag = KOR" in block:
        raise ValueError("RT56 generic tank MIO already mentions KOR; review merge manually")
    anchor = f"\tallowed = {{{newline}"
    if block.count(anchor) != 1:
        raise ValueError("generic tank MIO allowed-block anchor changed")
    addition = f"\t\tNOT = {{ tag = KOR }} # HOK provides dedicated tank MIOs{newline}"
    merged = block.replace(anchor, anchor + addition, 1)
    return (text[:start] + merged + text[end:]).encode("utf-8")


def build_medal_triggers() -> bytes:
    host = read_text(RT56_ROOT / "common/scripted_triggers/unit_medals_scripted_triggers.txt")
    donor = read_text(HOK_ROOT / "common/scripted_triggers/unit_medals_scripted_triggers.txt")
    newline = newline_of(host)
    korean = normalize_newlines(one_block(donor, "should_have_korean_medals_trigger"), newline)

    any_spans = block_spans(host, "should_have_any_unique_medals_trigger", top_level=True)
    if len(any_spans) != 1 or "should_have_korean_medals_trigger" in host:
        raise ValueError("RT56 medal trigger structure changed")
    start, end = any_spans[0]
    aggregate = host[start:end]
    suffix = f"\t}}{newline}}}"
    if not aggregate.endswith(suffix):
        raise ValueError("unique-medal aggregate closing structure changed")
    aggregate = aggregate[: -len(suffix)] + (
        f"\t\tshould_have_korean_medals_trigger = yes{newline}" + suffix
    )
    return (
        host[:start]
        + korean
        + newline * 2
        + aggregate
        + host[end:]
    ).encode("utf-8")


def find_indented_block(text: str, marker: str) -> tuple[int, int]:
    matches = list(re.finditer(rf"(?m)^[ \t]*{re.escape(marker)}\s*=\s*\{{[^\r\n]*", text))
    if len(matches) != 1:
        raise ValueError(f"expected one indented {marker!r} block, found {len(matches)}")
    match = matches[0]
    opening = text.find("{", match.start(), match.end())
    return match.start(), matching_brace(text, opening) + 1


def build_bookmark() -> bytes:
    host = read_text(RT56_ROOT / "common/bookmarks/the_gathering_storm.txt")
    donor = read_text(HOK_ROOT / "common/bookmarks/the_gathering_storm.txt")
    newline = newline_of(host)
    start, end = find_indented_block(donor, "KOR")
    korean = donor[start:end]
    if 'history = "KOR_GATHERING_STORM_DESC"' not in korean:
        raise ValueError("selected donor bookmark block is not Korea")
    if "label =" not in korean:
        ideology = "\t\t\tideology = democratic\n"
        if korean.count(ideology) != 1:
            raise ValueError("Korean bookmark ideology anchor changed")
        korean = korean.replace(
            ideology,
            ideology + "\t\t\tlabel = { country_asia new_r56_content }\n",
            1,
        )
    korean = normalize_newlines(korean, newline)

    if re.search(r'(?m)^\s*KOR\s*=\s*\{', host):
        raise ValueError("RT56 bookmark now contains Korea; review merge manually")
    anchor = f"\t\tCAN = {{{newline}"
    if host.count(anchor) != 1:
        raise ValueError("RT56 bookmark CAN insertion anchor changed")
    return host.replace(anchor, korean + newline * 2 + anchor, 1).encode("utf-8")


def branch_from_effect(effect_block: str) -> str:
    marker = "\telse_if = { # Hearts of Korea"
    if effect_block.count(marker) != 1:
        raise ValueError("HOK SP effect branch marker changed")
    start = effect_block.index(marker)
    opening = effect_block.index("{", start)
    end = matching_brace(effect_block, opening) + 1
    return effect_block[start:end]


def build_sp_effects() -> bytes:
    host = read_text(VANILLA_ROOT / "common/scripted_effects/SP_scripted_effects.txt")
    donor = read_text(HOK_ROOT / "common/scripted_effects/SP_scripted_effects.txt")
    newline = newline_of(host)
    merged = host
    for effect in KOR_SP_EFFECTS:
        donor_block = one_block(donor, effect)
        korean_branch = normalize_newlines(branch_from_effect(donor_block), newline)

        spans = block_spans(merged, effect, top_level=True)
        if len(spans) != 1:
            raise ValueError(f"vanilla SP effect {effect} changed")
        start, end = spans[0]
        host_block = merged[start:end]
        anchor = "\telse = { #GENERIC"
        if host_block.count(anchor) != 1 or "# Hearts of Korea" in host_block:
            raise ValueError(f"generic insertion point changed in {effect}")
        host_block = host_block.replace(anchor, korean_branch + newline + anchor, 1)
        merged = merged[:start] + host_block + merged[end:]
    if merged.count("else_if = { # Hearts of Korea") != len(KOR_SP_EFFECTS):
        raise ValueError("unexpected number of generated Korean SP branches")
    return merged.encode("utf-8")


def build_kor_decisions() -> bytes:
    """Rebase the Korean core-state target list on current vanilla."""
    host = read_text(VANILLA_ROOT / "common/decisions/KOR.txt")
    newline = newline_of(host)
    old = newline.join(
        (
            "\t\t\t\t\tstate = 525",
            "\t\t\t\t\tstate = 1031",
            "\t\t\t\t\tstate = 1030",
            "\t\t\t\t\tstate = 1029",
            "\t\t\t\t\tstate = 1028",
            "\t\t\t\t\tstate = 527",
        )
    )
    new = newline.join(
        (
            "\t\t\t\t\tstate = 525",
            "\t\t\t\t\tstate = 1145",
            "\t\t\t\t\tstate = 920",
            "\t\t\t\t\tstate = 1144",
            "\t\t\t\t\tstate = 918",
            "\t\t\t\t\tstate = 527",
            "\t\t\t\t\tstate = 919 # HoK: Jeolla",
            "\t\t\t\t\tstate = 917 # HoK: Hwanghae",
            "\t\t\t\t\tstate = 1146 # HoK: Jeju",
        )
    )
    if host.count(old) != 1:
        raise ValueError("vanilla KOR core-state decision list changed")
    merged = host.replace(old, new, 1)
    if any(f"state = {identifier}" in merged for identifier in (1028, 1029, 1030, 1031)):
        raise ValueError("legacy HOK state remains in generated vanilla KOR decisions")
    return merged.encode("utf-8")


def build_generic_advisors() -> bytes:
    """Keep RT56's current global generators while excluding HOK-owned KOR roles."""
    host = read_text(RT56_ROOT / "history/general/generic_advisors.txt")
    newline = newline_of(host)
    restrictions = {
        "generic_communist_revolutionary": "NOT = { tag = KOR } # HOK provides this adviser",
        "generic_fascist_demagogue": "NOT = { tag = KOR } # HOK provides this adviser",
        "generic_head_of_intelligence": "NOT = { original_tag = KOR } # HOK provides this adviser",
    }
    merged = host
    for token, restriction in restrictions.items():
        candidates = []
        for start, end in block_spans(merged, "every_possible_country", top_level=True):
            block = merged[start:end]
            if f"token_base = {token}" in block:
                candidates.append((start, end, block))
        if len(candidates) != 1:
            raise ValueError(f"expected one RT56 generic-adviser generator for {token}")
        start, end, block = candidates[0]
        if re.search(r"(?:original_)?tag\s*=\s*KOR", block):
            raise ValueError(f"RT56 {token} generator already handles KOR")
        anchor = f"\t\tis_dynamic_country = no{newline}"
        if block.count(anchor) != 1:
            raise ValueError(f"RT56 {token} dynamic-country anchor changed")
        block = block.replace(anchor, f"\t\t{restriction}{newline}" + anchor, 1)
        merged = merged[:start] + block + merged[end:]

    # RT56 already excludes KOR from its democratic-reformer generator and
    # does not whitelist it for the generic military-adviser generator.
    if merged.count("tag = KOR") != host.count("tag = KOR") + 3:
        raise ValueError("unexpected KOR exclusion count in generic advisers")
    return merged.encode("utf-8")


# [2026-09-22]_kpopmodder: Restore registration hidden by HOK's KOR.txt without recruiting anyone.
def build_kor_host_references() -> bytes:
    host = read_text(RT56_ROOT / "common/characters/KOR.txt")
    block = one_block(host, "KOR_kim_chang_ryong", top_level=False)
    newline = newline_of(host)
    header = newline.join((
        "# [2026-09-22]_kpopmodder: Preserve the RT56 idea token referenced by MAN characters.",
        "# Generated by tools/build_shared_overrides.py; host character block is unchanged.",
        "characters = {",
    ))
    return (header + newline + block + newline + "}" + newline).encode("utf-8")


# [2026-09-22]_kpopmodder: A declared but unrecruited character does not register its dynamic idea.
def build_man_characters() -> bytes:
    host = read_text(RT56_ROOT / "common/characters/MAN.txt")
    block = one_block(host, "MAN_kim_chang_ryong", top_level=False)
    newline = newline_of(host)
    old = newline.join((
        "\t\t\t\tKOR = {",
        "\t\t\t\t\tNOT = {",
        "\t\t\t\t\t\thas_idea = kim_chang_ryong",
        "\t\t\t\t\t}",
        "\t\t\t\t}",
    ))
    new = newline.join((
        "\t\t\t\tKOR = {",
        "\t\t\t\t\t# [2026-09-22]_kpopmodder: HOK does not recruit this RT56 advisor; query a character only when owned.",
        "\t\t\t\t\tif = {",
        "\t\t\t\t\t\tlimit = { has_character = KOR_kim_chang_ryong }",
        "\t\t\t\t\t\tNOT = { KOR_kim_chang_ryong = { is_hired_as_advisor = yes } }",
        "\t\t\t\t\t}",
        "\t\t\t\t}",
    ))
    if block.count(old) != 2 or host.count(old) != 2:
        raise ValueError("expected only the two MAN Kim advisor/commander KOR checks")
    merged = host.replace(block, block.replace(old, new), 1)
    if merged.replace(new, old) != host or "has_idea = kim_chang_ryong" in merged:
        raise ValueError("MAN merge changed content outside the two reviewed KOR conditions")
    return merged.encode("utf-8")


def build_outputs() -> dict[Path, bytes]:
    verify_sources()
    validate_rt56_difficulty_ownership()
    outputs = {
        Path("common/countries/zz_hok_rt56_colors.txt"): generated_additive_file(
            HOK_ROOT / "common/countries/colors.txt",
            ("KOR", "KJP", "KCH", "RKY", "TWN"),
            "HOK-owned country colours; KOR intentionally overrides the RT56 colour.",
        ),
        Path("common/countries/zz_hok_rt56_cosmetic.txt"): generated_additive_file(
            HOK_ROOT / "common/countries/cosmetic.txt",
            ("KOR_Goguryeo", "KOR_PRK_communism", "KJP_PSJ"),
            "HOK-owned cosmetic-tag colours.",
        ),
        Path("common/names/zz_hok_rt56_names.txt"): generated_additive_file(
            HOK_ROOT / "common/names/00_names.txt",
            ("KOR", "KJP", "KCH", "RKY", "TWN"),
            "HOK-owned random-name pools; KOR intentionally overrides the RT56 pool.",
        ),
        Path("common/intelligence_agencies/zz_hok_rt56_intelligence_agencies.txt"):
            build_intelligence_agency(),
        Path("common/military_industrial_organization/organizations/00_generic_organization.txt"):
            build_generic_mio(),
        Path("common/scripted_triggers/unit_medals_scripted_triggers.txt"):
            build_medal_triggers(),
        Path("common/bookmarks/the_gathering_storm.txt"): build_bookmark(),
        Path("common/scripted_effects/SP_scripted_effects.txt"): build_sp_effects(),
        Path("common/decisions/KOR.txt"): build_kor_decisions(),
        Path("history/general/generic_advisors.txt"): build_generic_advisors(),
        Path("common/characters/zz_hok_rt56_kor_host_references.txt"):
            build_kor_host_references(),
        Path("common/characters/MAN.txt"): build_man_characters(),
    }
    for relative, payload in outputs.items():
        validate_balanced(payload.decode("utf-8"), relative)
    return outputs


def apply(outputs: dict[Path, bytes]) -> None:
    for relative in STALE_WHOLE_FILES:
        path = COMPAT_ROOT / relative
        if path.exists():
            path.unlink()
            print(f"removed stale whole file: {relative}")
    for relative, expected in outputs.items():
        path = COMPAT_ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file() and path.read_bytes() == expected:
            print(f"unchanged: {relative}")
            continue
        path.write_bytes(expected)
        print(f"wrote: {relative}")


def check(outputs: dict[Path, bytes]) -> bool:
    ok = True
    for relative in STALE_WHOLE_FILES:
        if (COMPAT_ROOT / relative).exists():
            print(f"STALE: {relative}")
            ok = False
    for relative, expected in outputs.items():
        path = COMPAT_ROOT / relative
        if not path.is_file():
            print(f"MISSING: {relative}")
            ok = False
        elif path.read_bytes() != expected:
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
